#!/usr/bin/env python3
"""chic-v3: apply the Linear A substrate framework (4 pools) to CHIC.

End-to-end driver for mg-9700. Walks each of the 4 validated substrate
pools (Aquitanian, Etruscan, toponym, Eteocretan) against the CHIC
syllabographic-only token stream, generates substrate + matched-control
candidate equations against CHIC inscription windows, scores each under
its own external phoneme LM, and runs the v10 right-tail bayesian gate
on per-surface posteriors.

Mirrors the Linear A pipeline (mg-d26d / v10, mg-9f18 / v18, mg-6ccd /
v21) — same generator rules, same metric (external_phoneme_perplexity_v0
from harness.metrics), same gate criterion. The novelty is the **target
corpus**: candidate equations are pinned to CHIC windows, not Linear A
windows. Substrate phoneme inventories and matched controls are reused
verbatim from the Linear A pools so the substrate-vs-control comparison
isolates the substrate-LM-vs-control-LM-fit signal.

**Matched-control choice** (per the chic-v3 brief). The brief offers
two options: (a) build CHIC-specific bigram-preserving controls keyed
on CHIC window distributions, or (b) reuse the Linear-A-shape controls
verbatim. We pick **(b)** here: matched controls are about substrate
*phoneme shape*, not target-corpus shape; the per-surface bayesian
posterior compares substrate vs control under the *same* LM applied to
the *same* inscription windows, so corpus-shape effects cancel in the
paired diff. Reusing the existing controls keeps the chic-v3 result
directly comparable to the Linear A v10 / v18 / v21 numbers.

**Sidecar isolation.** All chic-v3 score rows go to a dedicated
sidecar ``results/experiments.external_phoneme_perplexity_v0.chic.jsonl``
so they don't intermix with the Linear A result stream. Per-pool
markdown rollups are emitted at
``results/rollup.bayesian_posterior.<pool>.chic.md``.

**Determinism.** No RNG. Same (CHIC corpus, pool YAMLs, LMs) ⇒
byte-identical hypothesis YAMLs, manifests, and rollup tables.
Score-row ``run_id`` and ``ran_at`` fields vary per run (per the
existing sweep convention); the rollup keeps the latest-by-ran_at row
per (hypothesis_hash, language) so re-runs converge to the same
verdict.

Usage:
    python3 scripts/chic_substrate_run.py
    python3 scripts/chic_substrate_run.py --pool aquitanian
    python3 scripts/chic_substrate_run.py --cap-per-entry 25 --top-k-gate 20
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
import time
import uuid
from collections import Counter, defaultdict
from pathlib import Path

# Allow running as `python3 scripts/chic_substrate_run.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

from harness import HARNESS_VERSION  # noqa: E402
from harness.corpus import build_stream, corpus_snapshot, load_records  # noqa: E402
from harness.external_phoneme_model import ExternalPhonemeModel  # noqa: E402
from harness.metrics import external_phoneme_perplexity_v0  # noqa: E402

from scripts.per_surface_bayesian_rollup import (  # noqa: E402
    beta_posterior,
    mann_whitney_u_one_tail,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CHIC_CORPUS = (
    _REPO_ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
)
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_DEFAULT_HYPOTHESES_DIR = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_RESULTS_DIR = _REPO_ROOT / "results"
_DEFAULT_EXT_MODEL_DIR = _REPO_ROOT / "harness" / "external_phoneme_models"
_HYPOTHESIS_SCHEMA = (
    _REPO_ROOT / "harness" / "schemas"
    / "hypothesis.candidate_equation.v1.schema.json"
)
_RESULT_SCHEMA = (
    _REPO_ROOT / "harness" / "schemas" / "result.v0.schema.json"
)
_POOL_SCHEMA = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"

_METRIC = "external_phoneme_perplexity_v0"
_CHIC_RESULTS_SIDECAR = (
    _DEFAULT_RESULTS_DIR / f"experiments.{_METRIC}.chic.jsonl"
)

# Pool → external phoneme LM name. Mirrors run_sweep._EXT_POOL_LANGUAGE
# for the 4 substrate pools the brief targets. Controls share their
# substrate's LM so the paired_diff cancels the LM choice.
_POOL_LANGUAGE: dict[str, str] = {
    "aquitanian": "basque",
    "control_aquitanian": "basque",
    "etruscan": "etruscan",
    "control_etruscan": "etruscan",
    "toponym": "basque",
    "control_toponym_bigram": "basque",
    "eteocretan": "eteocretan",
    "control_eteocretan_bigram": "eteocretan",
}

# Pool → matched-control pool. Mirrors the v18 / v21 default for each
# substrate (bigram-preserving controls where available).
_POOL_TO_CONTROL: dict[str, str] = {
    "aquitanian": "control_aquitanian",
    "etruscan": "control_etruscan",
    "toponym": "control_toponym_bigram",
    "eteocretan": "control_eteocretan_bigram",
}

_SUBSTRATE_POOLS = ("aquitanian", "etruscan", "toponym", "eteocretan")

# CHIC syllabogram regex (#NNN where NNN is a 3-digit ID). The window
# generator filters CHIC tokens through this; non-matching tokens
# (DIV, residual structural breaks) are not syllabograms.
_CHIC_SYLLABOGRAM_RE = re.compile(r"^#\d{3}$")

_VOWELS = frozenset("aeiouAEIOU")
_SONORANTS = frozenset("lrnmñLRNMÑ")


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def _load_pool(pool_name: str, pools_dir: Path) -> dict:
    pool_path = pools_dir / f"{pool_name}.yaml"
    with pool_path.open("r", encoding="utf-8") as fh:
        pool = yaml.load(fh, Loader=_StringDateLoader)
    schema = json.loads(_POOL_SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(pool)
    return pool


def _phoneme_class(p: str) -> str:
    if not p:
        return "C"
    h = p[0]
    if h in _VOWELS:
        return "V"
    if h in _SONORANTS:
        return "S"
    return "C"


def _is_syllabogram(tok: str) -> bool:
    return bool(_CHIC_SYLLABOGRAM_RE.fullmatch(tok))


def _load_chic_records(corpus_path: Path) -> list[dict]:
    records: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])
    return records


# ---------------------------------------------------------------------------
# Window enumeration
# ---------------------------------------------------------------------------


def _candidate_windows(
    tokens: list[str], n_phonemes: int
) -> list[tuple[int, int, list[int]]]:
    """Mirror of ``scripts.generate_candidates._candidate_windows`` but
    using the CHIC syllabogram regex. Returns
    ``(span_start, span_end, syllabogram_indices)`` tuples; both
    endpoints are syllabograms; no DIV is crossed.
    """
    if n_phonemes <= 0:
        return []
    windows: list[tuple[int, int, list[int]]] = []
    block: list[int] = []
    for i, tok in enumerate(tokens):
        if tok == "DIV":
            if len(block) >= n_phonemes:
                for j in range(0, len(block) - n_phonemes + 1):
                    idxs = block[j : j + n_phonemes]
                    windows.append((idxs[0], idxs[-1], idxs))
            block = []
        elif _is_syllabogram(tok):
            block.append(i)
    if len(block) >= n_phonemes:
        for j in range(0, len(block) - n_phonemes + 1):
            idxs = block[j : j + n_phonemes]
            windows.append((idxs[0], idxs[-1], idxs))
    return windows


# ---------------------------------------------------------------------------
# Hypothesis emission
# ---------------------------------------------------------------------------


_NAME_RE = re.compile(r"[^A-Za-z0-9_]")


def _slug(s: str) -> str:
    return _NAME_RE.sub("_", s)


def _trim_name(name: str, limit: int = 80) -> str:
    if len(name) <= limit:
        return name
    head = name[: limit - 9]
    tail_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    return f"{head}_{tail_hash}"


def _canonical_hash(doc: dict) -> str:
    payload = json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _build_hypothesis_doc(
    *,
    pool_name: str,
    entry: dict,
    inscription: dict,
    span_start: int,
    span_end: int,
    syllabogram_indices: list[int],
) -> dict:
    tokens = inscription["tokens"]
    signs = [tokens[i] for i in syllabogram_indices]
    phonemes = list(entry["phonemes"])
    sign_to_phoneme = dict(zip(signs, phonemes))
    surface = entry["surface"]
    name = (
        f"chic_{pool_name}_{_slug(surface)}_"
        f"{_slug(inscription['id'])}_{span_start}_{span_end}"
    )
    name = _trim_name(name)
    description = (
        f"chic-v3 candidate equation: pool={pool_name!r} entry "
        f"surface={surface!r} pinned to {inscription['id']} tokens "
        f"[{span_start}..{span_end}]."
    )
    doc = {
        "schema_version": "candidate_equation.v1",
        "name": name,
        "description": description,
        "author": "scripts/chic_substrate_run.py",
        "created": "2026-05-05",
        "source_pool": pool_name,
        "root": {
            "surface": surface,
            "phonemes": phonemes,
        },
        "equation": {
            "inscription_id": inscription["id"],
            "span": [span_start, span_end],
            "sign_to_phoneme": sign_to_phoneme,
        },
    }
    if entry.get("gloss"):
        doc["root"]["gloss_hint"] = entry["gloss"]
    doc["root"]["citation"] = entry.get("citation") or "see pool source_citation"
    return doc


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------


def generate_pool_candidates(
    *,
    pool_name: str,
    pool: dict,
    records: list[dict],
    cap_per_entry: int,
    out_dir: Path,
    progress: bool,
    schema_validator: Draft202012Validator,
    repo_root: Path = _REPO_ROOT,
) -> list[dict]:
    """Generate candidate-equation YAMLs for one pool against CHIC.

    Returns the manifest rows in deterministic
    (pool_entry_index, inscription_id, span_start) order.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict] = []
    expected_filenames: set[str] = set()

    for entry_idx, entry in enumerate(pool["entries"]):
        phonemes = list(entry["phonemes"])
        n = len(phonemes)
        classes = {_phoneme_class(p) for p in phonemes}
        if len(classes) < 2:
            continue
        per_entry_count = 0
        for record in records:
            if record.get("transcription_confidence") == "fragmentary":
                continue
            if int(record.get("n_signs", 0)) < n:
                continue
            tokens = record["tokens"]
            for span_start, span_end, syll_idxs in _candidate_windows(tokens, n):
                signs = [tokens[i] for i in syll_idxs]
                if len(set(signs)) != n:
                    continue
                if per_entry_count >= cap_per_entry:
                    break
                doc = _build_hypothesis_doc(
                    pool_name=pool_name,
                    entry=entry,
                    inscription=record,
                    span_start=span_start,
                    span_end=span_end,
                    syllabogram_indices=syll_idxs,
                )
                schema_validator.validate(doc)
                h = _canonical_hash(doc)
                sha8 = h.split(":", 1)[1][:8]
                yaml_path = out_dir / f"{sha8}.yaml"
                yaml_text = _dump_yaml(doc)
                if (
                    not yaml_path.exists()
                    or yaml_path.read_text(encoding="utf-8") != yaml_text
                ):
                    yaml_path.write_text(yaml_text, encoding="utf-8")
                expected_filenames.add(yaml_path.name)
                try:
                    rel_path = yaml_path.relative_to(repo_root).as_posix()
                except ValueError:
                    rel_path = yaml_path.as_posix()
                manifest_rows.append(
                    {
                        "pool": pool_name,
                        "pool_entry_index": entry_idx,
                        "pool_entry_surface": entry["surface"],
                        "inscription_id": record["id"],
                        "span_start": span_start,
                        "span_end": span_end,
                        "hypothesis_path": rel_path,
                        "hypothesis_hash": h,
                    }
                )
                per_entry_count += 1
            else:
                continue
            break
        if progress and (entry_idx + 1) % 25 == 0:
            print(
                f"  {pool_name} entry {entry_idx + 1}/{len(pool['entries'])} "
                f"({entry['surface']}): {per_entry_count} candidates",
                file=sys.stderr,
            )

    manifest_rows.sort(
        key=lambda r: (r["pool_entry_index"], r["inscription_id"], r["span_start"])
    )

    # Prune orphaned YAMLs from prior runs of this pool.
    for existing in sorted(out_dir.glob("*.yaml")):
        if existing.name not in expected_filenames:
            existing.unlink()
    return manifest_rows


def write_manifest(manifest_rows: list[dict], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as fh:
        for row in manifest_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _existing_score_rows(
    sidecar: Path,
) -> dict[tuple[str, str], dict]:
    """(hypothesis_hash, language) → most-recent-by-ran_at row in the
    chic sidecar. Used to skip rescoring on resume runs."""
    out: dict[tuple[str, str], dict] = {}
    if not sidecar.exists():
        return out
    with sidecar.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("metric") != _METRIC:
                continue
            key = (row.get("hypothesis_hash", ""), row.get("language", ""))
            cur = out.get(key)
            if cur is None or row.get("ran_at", "") > cur.get("ran_at", ""):
                out[key] = row
    return out


def score_candidates(
    *,
    manifest_rows: list[dict],
    pool_name: str,
    stream: list[str],
    snapshot: str,
    n_records: int,
    sidecar: Path,
    lm: ExternalPhonemeModel,
    note: str,
    progress_every: int,
    result_validator: Draft202012Validator,
    repo_root: Path,
    seen: set[tuple[str, str, str]],
) -> list[dict]:
    """Score every manifest row under ``lm`` and append rows to the
    chic sidecar. Skip rows already present (resume support).
    """
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    new_rows: list[dict] = []
    started = time.monotonic()
    with sidecar.open("a", encoding="utf-8") as fh:
        for i, m_row in enumerate(manifest_rows, 1):
            key = (m_row["hypothesis_hash"], snapshot, _METRIC)
            if key in seen:
                continue
            hyp_path = repo_root / m_row["hypothesis_path"]
            with hyp_path.open("r", encoding="utf-8") as hh:
                hypothesis = yaml.load(hh, Loader=_StringDateLoader)
            mapping = dict(hypothesis["equation"]["sign_to_phoneme"])
            ran_at = dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            t0 = time.monotonic()
            result = external_phoneme_perplexity_v0(
                stream=stream, mapping=mapping, language_model=lm
            )
            duration_ms = int((time.monotonic() - t0) * 1000)
            row = {
                "run_id": str(uuid.uuid4()),
                "hypothesis_path": m_row["hypothesis_path"],
                "hypothesis_hash": m_row["hypothesis_hash"],
                "harness_version": HARNESS_VERSION,
                "metric": _METRIC,
                "corpus_records_used": n_records,
                "corpus_snapshot": snapshot,
                "ran_at": ran_at,
                "duration_ms": duration_ms,
                "notes": note,
                "score": float(result.score),
                "metric_notes": result.metric_notes,
                "n_runs": int(result.n_runs),
                "n_chars_scored": int(result.n_chars_scored),
                "n_phonemes_scored": int(result.n_phonemes_scored),
                "total_loglik": float(result.total_loglik),
                "language": result.language,
            }
            result_validator.validate(row)
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            seen.add(key)
            new_rows.append(row)
            if progress_every and len(new_rows) % progress_every == 0:
                elapsed = time.monotonic() - started
                rate = len(new_rows) / elapsed if elapsed > 0 else 0.0
                print(
                    f"  {pool_name}: scored {len(new_rows)}/{len(manifest_rows)} "
                    f"({rate:.1f}/s)",
                    file=sys.stderr,
                )
    return new_rows


# ---------------------------------------------------------------------------
# Bayesian rollup
# ---------------------------------------------------------------------------


def _build_paired_records(
    *,
    pool_name: str,
    sub_manifest: list[dict],
    ctrl_manifest: list[dict],
    score_rows: dict[tuple[str, str], dict],
    language: str,
) -> list[dict]:
    """Pair substrate and control candidates by (inscription, span)
    and compute paired_diff = sub_score - ctrl_score for every window
    where both sides scored. Substrate / control surface come from the
    matched manifest rows."""
    by_window: dict[tuple[str, int, int], list[dict]] = defaultdict(list)
    for row in ctrl_manifest:
        key = (row["inscription_id"], int(row["span_start"]), int(row["span_end"]))
        by_window[key].append(row)

    records: list[dict] = []
    for sub in sub_manifest:
        sub_score_row = score_rows.get((sub["hypothesis_hash"], language))
        if sub_score_row is None:
            continue
        key = (sub["inscription_id"], int(sub["span_start"]), int(sub["span_end"]))
        candidates = by_window.get(key, [])
        if not candidates:
            continue
        # Stable tiebreak by hash (deterministic without the
        # phoneme-edit-distance heuristic the v8 rollup uses; for
        # chic-v3 we keep it simple — the matched control pool's
        # phoneme inventory is already shape-matched, so any mate
        # gives an apples-to-apples paired_diff).
        candidates_sorted = sorted(candidates, key=lambda r: r["hypothesis_hash"])
        ctrl = None
        for c in candidates_sorted:
            if (c["hypothesis_hash"], language) in score_rows:
                ctrl = c
                break
        if ctrl is None:
            continue
        ctrl_score_row = score_rows[(ctrl["hypothesis_hash"], language)]
        sub_score = float(sub_score_row.get("score", 0.0))
        ctrl_score = float(ctrl_score_row.get("score", 0.0))
        records.append(
            {
                "kind": "v8",
                "pool": pool_name,
                "control_pool": ctrl["pool"],
                "substrate_surfaces": (sub["pool_entry_surface"],),
                "control_surfaces": (ctrl["pool_entry_surface"],),
                "substrate_score": sub_score,
                "control_score": ctrl_score,
                "paired_diff": sub_score - ctrl_score,
                "substrate_hash": sub["hypothesis_hash"],
                "control_hash": ctrl["hypothesis_hash"],
                "inscription_id": sub["inscription_id"],
                "span_start": int(sub["span_start"]),
                "span_end": int(sub["span_end"]),
            }
        )
    return records


def _aggregate_per_surface(records: list[dict]) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"n": 0, "k": 0, "paired_diffs": []}
    )
    for rec in records:
        pd = rec["paired_diff"]
        for s in set(rec["substrate_surfaces"]):
            cell = out[(rec["pool"], s)]
            cell["n"] += 1
            cell["paired_diffs"].append(pd)
            if pd > 0:
                cell["k"] += 1
        for s in set(rec["control_surfaces"]):
            cell = out[(rec["control_pool"], s)]
            cell["n"] += 1
            cell["paired_diffs"].append(-pd)
            if pd < 0:
                cell["k"] += 1
    return out


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def _fmt(x: float, w: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "  nan"
    return f"{x:.{w}f}"


def _fmt_p(p: float) -> str:
    if math.isnan(p):
        return "nan"
    if p == 0.0:
        return "<1e-300"
    return f"{p:.3e}"


def render_pool_rollup(
    *,
    pool_name: str,
    control_pool: str,
    language: str,
    sub_rows: list[dict],
    ctrl_rows: list[dict],
    paired_records: list[dict],
    n_min: int,
    top_k_gate: int,
    top_per_pool: int,
) -> tuple[str, dict]:
    sub_top = sorted(sub_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    ctrl_top = sorted(ctrl_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
    median_sub = _median(sub_means)
    median_ctrl = _median(ctrl_means)
    gate = (not math.isnan(p)) and p < 0.05 and median_sub > median_ctrl
    gate_str = "PASS" if gate else "FAIL"
    mean_sub = (
        sum(sub_means) / len(sub_means) if sub_means else float("nan")
    )
    mean_ctrl = (
        sum(ctrl_means) / len(ctrl_means) if ctrl_means else float("nan")
    )

    lines: list[str] = []
    lines.append(
        f"# chic-v3 — pool={pool_name} right-tail bayesian gate on CHIC "
        f"(mg-9700)\n"
    )
    if gate:
        verdict = (
            f"**Headline: the {pool_name} substrate pool PASSes the "
            f"v10 right-tail bayesian gate against {control_pool} on "
            f"the CHIC syllabographic corpus at p={_fmt_p(p)}** "
            f"(median substrate posterior {median_sub:.4f} vs median "
            f"control posterior {median_ctrl:.4f}). Linear A v10 / "
            f"v18 / v21 framework PASS reproduces on CHIC."
        )
    else:
        verdict = (
            f"**Headline: the {pool_name} substrate pool FAILs the "
            f"v10 right-tail bayesian gate against {control_pool} on "
            f"the CHIC syllabographic corpus at p={_fmt_p(p)}** "
            f"(median substrate posterior {median_sub:.4f} vs median "
            f"control posterior {median_ctrl:.4f}). Cross-script "
            f"transfer of the Linear A {pool_name} signal to CHIC is "
            f"not detected at the gate threshold; CHIC's smaller "
            f"corpus reduces the framework's discriminating power "
            f"and a borderline p-value should be read with that "
            f"caveat in mind."
        )
    lines.append(verdict + "\n")

    lines.append("## Acceptance gate\n")
    lines.append(
        "| substrate pool | control pool | LM | n paired windows | "
        "substrate top-K | control top-K | median(top substrate "
        "posterior) | median(top control posterior) | MW U "
        "(substrate) | MW p (one-tail) | gate |"
    )
    lines.append(
        "|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|"
    )
    lines.append(
        f"| {pool_name} | {control_pool} | {language} | "
        f"{len(paired_records)} | {na} | {nb} | {median_sub:.4f} | "
        f"{median_ctrl:.4f} | {u:.1f} | {_fmt_p(p)} | {gate_str} |"
    )
    lines.append("")

    lines.append("## Mean-of-means (informational)\n")
    lines.append(
        f"Mean of top-{top_k_gate} substrate posterior_mean: "
        f"{mean_sub:.4f}. Mean of top-{top_k_gate} control "
        f"posterior_mean: {mean_ctrl:.4f}. Gap: "
        f"{mean_sub - mean_ctrl:+.4f}. The gate uses the rank-based "
        f"MW U test rather than the mean gap, so this number is "
        f"shown for orientation only.\n"
    )

    lines.append(
        f"## Top-{top_k_gate} substrate vs top-{top_k_gate} control "
        f"side-by-side (gate input)\n"
    )
    lines.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    lines.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    pad = max(len(sub_top), len(ctrl_top))
    for i in range(pad):
        s = sub_top[i] if i < len(sub_top) else None
        c = ctrl_top[i] if i < len(ctrl_top) else None
        lines.append(
            "| {r} | {ss} | {sn} | {sk} | {sm} | {cs} | {cn} | {ck} | {cm} |".format(
                r=i + 1,
                ss=f"`{s['surface']}`" if s else "—",
                sn=s["n"] if s else "—",
                sk=s["k"] if s else "—",
                sm=_fmt(s["posterior_mean"]) if s else "—",
                cs=f"`{c['surface']}`" if c else "—",
                cn=c["n"] if c else "—",
                ck=c["k"] if c else "—",
                cm=_fmt(c["posterior_mean"]) if c else "—",
            )
        )
    lines.append("")

    all_rows = sub_rows + ctrl_rows
    leader = sorted(all_rows, key=lambda r: -r["effective_score"])[:top_per_pool]
    lines.append(
        f"## Top-{len(leader)} surfaces by effective score "
        f"(substrate + control interleaved)\n"
    )
    lines.append(
        "| rank | side | surface | n | k | posterior | credibility | effective |"
    )
    lines.append("|---:|:--|:--|---:|---:|---:|---:|---:|")
    for i, r in enumerate(leader, 1):
        side = "control" if r["pool_kind"] == control_pool else "substrate"
        lines.append(
            "| {r} | {side} | `{surface}` | {n} | {k} | {m} | {c} | {e} |".format(
                r=i, side=side, surface=r["surface"],
                n=r["n"], k=r["k"],
                m=_fmt(r["posterior_mean"]),
                c=_fmt(r["credibility"], 3),
                e=_fmt(r["effective_score"]),
            )
        )
    lines.append("")

    lines.append("## Notes\n")
    lines.append(
        f"- Metric: `{_METRIC}`. LM: `{language}`.\n"
        f"- Target corpus: CHIC syllabographic-only stream "
        f"(`corpora/cretan_hieroglyphic/syllabographic.jsonl`, "
        f"chic-v3 / mg-9700).\n"
        f"- Substrate pool: `{pool_name}`. Control pool: "
        f"`{control_pool}` — Linear-A-shape control reused verbatim "
        f"per the chic-v3 brief; matched controls are about substrate "
        f"phoneme shape, not target-corpus shape, so reusing the "
        f"existing controls keeps the chic-v3 result directly "
        f"comparable to the Linear A v10 / v18 / v21 numbers.\n"
        f"- Gate: top-{top_k_gate} by posterior_mean only (no "
        f"credibility shrinkage); one-tail Mann-Whitney U with "
        f"normal-approximation tie-corrected p-value. PASS at "
        f"p<0.05 with median(substrate top-K) > median(control top-K).\n"
        f"- Determinism: identical rows across re-runs given the "
        f"same CHIC corpus, pool YAMLs, and LM. No RNG anywhere in "
        f"the pipeline.\n"
        f"- Corpus-size caveat: CHIC's syllabographic-only stream "
        f"is roughly an order of magnitude smaller than Linear A's "
        f"(see `corpora/cretan_hieroglyphic/syllabographic_stats.md`); "
        f"the framework's discriminating power is corpus-size-"
        f"dependent. Borderline p-values (0.04 < p < 0.10) should be "
        f"read as informative-but-underpowered rather than "
        f"definitive.\n"
    )
    summary = {
        "pool": pool_name,
        "control_pool": control_pool,
        "language": language,
        "n_paired_windows": len(paired_records),
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate_top": median_sub,
        "median_control_top": median_ctrl,
        "mean_substrate_top": mean_sub,
        "mean_control_top": mean_ctrl,
        "mw_u_substrate": u,
        "mw_p_one_tail": p,
        "gate": gate_str,
        "top_k_gate": top_k_gate,
    }
    return "\n".join(lines) + "\n", summary


def build_posterior_rows(
    aggregates: dict[tuple[str, str], dict],
    *,
    n_min: int,
) -> list[dict]:
    out: list[dict] = []
    for (pool_kind, surface), cell in sorted(aggregates.items()):
        n = cell["n"]
        k = cell["k"]
        mean, lo, hi = beta_posterior(n, k)
        cred = min(1.0, n / n_min) if n_min > 0 else 1.0
        eff = cred * mean + (1.0 - cred) * 0.5
        out.append(
            {
                "pool_kind": pool_kind,
                "surface": surface,
                "n": n,
                "k": k,
                "posterior_mean": mean,
                "posterior_ci_low": lo,
                "posterior_ci_high": hi,
                "credibility": cred,
                "effective_score": eff,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Combined view
# ---------------------------------------------------------------------------


def render_combined_md(
    summaries: list[dict],
    *,
    chic_corpus_summary: dict,
    top_k_gate: int,
) -> str:
    lines: list[str] = []
    lines.append(
        "# chic-v3 — combined right-tail bayesian gate on CHIC "
        "(mg-9700)\n"
    )
    lines.append(
        "Generated by `scripts/chic_substrate_run.py`. Applies the "
        "Linear A substrate framework (Aquitanian, Etruscan, "
        "toponym, Eteocretan — the 4 validated pools from v10 / "
        "v18 / v21) to the CHIC syllabographic-only corpus, with the "
        "same per-pool right-tail bayesian gate.\n"
    )
    lines.append("## CHIC syllabographic corpus\n")
    lines.append(
        f"- {chic_corpus_summary['n_records']} inscriptions, "
        f"{chic_corpus_summary['n_sign_tokens']} syllabographic "
        f"tokens, {chic_corpus_summary['n_blocks']} maximal "
        f"syllabographic blocks (between DIVs); see "
        f"`corpora/cretan_hieroglyphic/syllabographic_stats.md` for "
        f"the block-length histogram and Linear A comparison.\n"
    )
    lines.append("## Per-pool acceptance gate\n")
    lines.append(
        f"| pool | control pool | LM | n paired windows | n_substrate_top | "
        f"n_control_top | median(top-{top_k_gate} substrate posterior) | "
        f"median(top-{top_k_gate} control posterior) | MW U | MW p | gate |"
    )
    lines.append("|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|")
    for s in summaries:
        lines.append(
            "| {pool} | {ctrl} | {lang} | {nw} | {ns} | {nc} | "
            "{mss:.4f} | {msc:.4f} | {u:.1f} | {p} | {gate} |".format(
                pool=s["pool"], ctrl=s["control_pool"], lang=s["language"],
                nw=s["n_paired_windows"],
                ns=s["n_substrate_top"], nc=s["n_control_top"],
                mss=s["median_substrate_top"], msc=s["median_control_top"],
                u=s["mw_u_substrate"], p=_fmt_p(s["mw_p_one_tail"]),
                gate=s["gate"],
            )
        )
    lines.append("")
    lines.append("## Pre-registered prediction (chic-v3 brief)\n")
    lines.append(
        "Based on Linear A's monotonic-with-relatedness ordering "
        "(Eteocretan > toponym > Etruscan > Aquitanian), CHIC was "
        "expected to show similar or stronger Eteocretan + toponym "
        "signal (closest-genealogical-relative substrates for a "
        "Cretan script) and weaker Etruscan + Aquitanian. The "
        "table above is the data; see "
        "`docs/findings.md` (Findings from mg-9700) for the "
        "interpretation of which pre-registered pattern the "
        "results match.\n"
    )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(
    *,
    chic_corpus: Path,
    pools_dir: Path,
    hypotheses_dir: Path,
    results_dir: Path,
    ext_model_dir: Path,
    cap_per_entry: int,
    top_k_gate: int,
    top_per_pool: int,
    n_min: int,
    pools: list[str] | None = None,
    progress: bool = True,
    note: str = "chic-v3",
    repo_root: Path = _REPO_ROOT,
) -> dict:
    pools = list(pools) if pools else list(_SUBSTRATE_POOLS)
    for p in pools:
        if p not in _SUBSTRATE_POOLS:
            raise ValueError(
                f"unknown pool {p!r}; supported: {_SUBSTRATE_POOLS}"
            )

    records = _load_chic_records(chic_corpus)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(chic_corpus, repo_root)
    n_sign_tokens = sum(
        1 for tok in stream if tok != "DIV" and tok != "INS_BOUNDARY"
    )
    n_blocks = 0
    block: list[str] = []
    for tok in stream:
        if tok in ("DIV", "INS_BOUNDARY"):
            if block:
                n_blocks += 1
                block = []
        else:
            block.append(tok)
    if block:
        n_blocks += 1
    chic_corpus_summary = {
        "n_records": n_records,
        "n_sign_tokens": n_sign_tokens,
        "n_blocks": n_blocks,
        "snapshot": snapshot,
    }

    hyp_schema = json.loads(_HYPOTHESIS_SCHEMA.read_text(encoding="utf-8"))
    hyp_validator = Draft202012Validator(hyp_schema)
    result_schema = json.loads(_RESULT_SCHEMA.read_text(encoding="utf-8"))
    result_validator = Draft202012Validator(result_schema)

    # Pre-load LMs for the languages we need.
    needed_langs = sorted({_POOL_LANGUAGE[p] for p in pools})
    lms: dict[str, ExternalPhonemeModel] = {}
    for lang in needed_langs:
        lm_path = ext_model_dir / f"{lang}.json"
        lms[lang] = ExternalPhonemeModel.load_json(lm_path)

    # Prep score-row resume cache.
    sidecar = results_dir / f"experiments.{_METRIC}.chic.jsonl"
    score_rows = _existing_score_rows(sidecar)
    seen: set[tuple[str, str, str]] = {
        (h, snapshot, _METRIC) for (h, _lang) in score_rows.keys()
    }

    summaries: list[dict] = []
    pool_summary: dict[str, dict] = {}

    for pool_name in pools:
        ctrl_name = _POOL_TO_CONTROL[pool_name]
        lang = _POOL_LANGUAGE[pool_name]
        sub_pool = _load_pool(pool_name, pools_dir)
        ctrl_pool = _load_pool(ctrl_name, pools_dir)

        if progress:
            print(f"--- {pool_name} (vs {ctrl_name}) | LM: {lang} ---", file=sys.stderr)

        # Generate substrate + control candidates against CHIC windows.
        sub_out_dir = hypotheses_dir / f"chic_{pool_name}"
        ctrl_out_dir = hypotheses_dir / f"chic_{ctrl_name}"
        sub_manifest = generate_pool_candidates(
            pool_name=pool_name,
            pool=sub_pool,
            records=records,
            cap_per_entry=cap_per_entry,
            out_dir=sub_out_dir,
            progress=progress,
            schema_validator=hyp_validator,
            repo_root=repo_root,
        )
        ctrl_manifest = generate_pool_candidates(
            pool_name=ctrl_name,
            pool=ctrl_pool,
            records=records,
            cap_per_entry=cap_per_entry,
            out_dir=ctrl_out_dir,
            progress=progress,
            schema_validator=hyp_validator,
            repo_root=repo_root,
        )
        write_manifest(
            sub_manifest,
            hypotheses_dir / f"chic_{pool_name}.manifest.jsonl",
        )
        write_manifest(
            ctrl_manifest,
            hypotheses_dir / f"chic_{ctrl_name}.manifest.jsonl",
        )

        if progress:
            print(
                f"  generated: substrate={len(sub_manifest)}  "
                f"control={len(ctrl_manifest)}",
                file=sys.stderr,
            )

        # Score both sides.
        score_candidates(
            manifest_rows=sub_manifest,
            pool_name=pool_name,
            stream=stream,
            snapshot=snapshot,
            n_records=n_records,
            sidecar=sidecar,
            lm=lms[lang],
            note=note,
            progress_every=200,
            result_validator=result_validator,
            repo_root=repo_root,
            seen=seen,
        )
        score_candidates(
            manifest_rows=ctrl_manifest,
            pool_name=ctrl_name,
            stream=stream,
            snapshot=snapshot,
            n_records=n_records,
            sidecar=sidecar,
            lm=lms[lang],
            note=note,
            progress_every=200,
            result_validator=result_validator,
            repo_root=repo_root,
            seen=seen,
        )

        # Reload the resume cache so newly-written rows participate.
        score_rows = _existing_score_rows(sidecar)

        # Pair, aggregate, gate, render.
        paired = _build_paired_records(
            pool_name=pool_name,
            sub_manifest=sub_manifest,
            ctrl_manifest=ctrl_manifest,
            score_rows=score_rows,
            language=lang,
        )
        aggregates = _aggregate_per_surface(paired)
        rows = build_posterior_rows(aggregates, n_min=n_min)
        sub_rows = [r for r in rows if r["pool_kind"] == pool_name]
        ctrl_rows = [r for r in rows if r["pool_kind"] == ctrl_name]

        for r in sub_rows + ctrl_rows:
            # Used for leaderboard rendering only.
            pass

        md, summary = render_pool_rollup(
            pool_name=pool_name,
            control_pool=ctrl_name,
            language=lang,
            sub_rows=sub_rows,
            ctrl_rows=ctrl_rows,
            paired_records=paired,
            n_min=n_min,
            top_k_gate=top_k_gate,
            top_per_pool=top_per_pool,
        )
        out_md = results_dir / f"rollup.bayesian_posterior.{pool_name}.chic.md"
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(md, encoding="utf-8")
        summaries.append(summary)
        pool_summary[pool_name] = {
            "n_substrate_candidates": len(sub_manifest),
            "n_control_candidates": len(ctrl_manifest),
            "n_paired_windows": len(paired),
            "verdict": summary,
        }
        if progress:
            print(
                f"  gate: {summary['gate']} "
                f"(p={summary['mw_p_one_tail']:.3e}, "
                f"median_sub={summary['median_substrate_top']:.4f}, "
                f"median_ctrl={summary['median_control_top']:.4f})",
                file=sys.stderr,
            )

    combined = render_combined_md(
        summaries,
        chic_corpus_summary=chic_corpus_summary,
        top_k_gate=top_k_gate,
    )
    combined_path = results_dir / "rollup.bayesian_posterior.chic.md"
    combined_path.write_text(combined, encoding="utf-8")

    try:
        rel_combined = str(combined_path.relative_to(repo_root))
    except ValueError:
        rel_combined = str(combined_path)
    return {
        "chic_corpus": chic_corpus_summary,
        "pools": pool_summary,
        "summaries": summaries,
        "combined_path": rel_combined,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--chic-corpus", type=Path, default=_DEFAULT_CHIC_CORPUS)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS_DIR)
    parser.add_argument(
        "--hypotheses-dir", type=Path, default=_DEFAULT_HYPOTHESES_DIR
    )
    parser.add_argument(
        "--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR
    )
    parser.add_argument(
        "--ext-model-dir", type=Path, default=_DEFAULT_EXT_MODEL_DIR
    )
    parser.add_argument("--cap-per-entry", type=int, default=50)
    parser.add_argument("--top-k-gate", type=int, default=20)
    parser.add_argument("--top-per-pool", type=int, default=50)
    parser.add_argument("--n-min", type=int, default=10)
    parser.add_argument(
        "--pool",
        choices=list(_SUBSTRATE_POOLS),
        action="append",
        default=None,
        help="Restrict to one or more substrate pools (default: all 4).",
    )
    parser.add_argument("--note", default="chic-v3")
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args(argv)

    summary = run(
        chic_corpus=args.chic_corpus,
        pools_dir=args.pools_dir,
        hypotheses_dir=args.hypotheses_dir,
        results_dir=args.results_dir,
        ext_model_dir=args.ext_model_dir,
        cap_per_entry=args.cap_per_entry,
        top_k_gate=args.top_k_gate,
        top_per_pool=args.top_per_pool,
        n_min=args.n_min,
        pools=args.pool,
        progress=not args.no_progress,
        note=args.note,
    )
    print(json.dumps(summary["summaries"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
