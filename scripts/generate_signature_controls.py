#!/usr/bin/env python3
"""Matched-control signature generator (mg-bef2, harness v9).

For each substrate signature in
``hypotheses/auto_signatures/<pool>.manifest.jsonl``, emits a paired
control signature in ``hypotheses/auto_signatures/control_<pool>/`` that:

  * pins the same window (inscription, span);
  * uses the same number of roots, with the same root lengths and the
    same span_within_window placements;
  * substitutes each substrate root with the closest-phoneme-inventory
    entry of equal length from ``pools/control_<pool>.yaml``;
  * keeps the resulting union sign_to_phoneme non-conflicting.

The pairing key is the (inscription_id, window_start, window_end) +
the per-root span_within_window tuple, recorded in the control
manifest's ``paired_substrate_hash`` field. Substrate signatures whose
matched-control construction fails (no consistent control assignment
exists) are dropped from the analysis (paired_diff null per the
ticket's matched-control protocol).

Algorithm
=========
1. For each substrate root R_i (in declared order within the
   signature), recover the per-position sign sequence from the
   inscription's tokens at the substrate's window-relative offsets.
2. Build the candidate-control list: every control_<pool> entry of
   the same length as R_i, sorted by (phoneme-set edit-distance to
   R_i's phoneme sequence) then by surface.
3. Walk the candidate list and pick the first control entry whose
   phoneme assignment is consistent with the partial control
   mapping built so far (no sign mapped to two phonemes).
4. If every substrate root finds a consistent control, emit the
   matched control signature. Otherwise drop the substrate signature.

Output
======
  hypotheses/auto_signatures/control_<pool>/<sha8>.yaml
  hypotheses/auto_signatures/control_<pool>.manifest.jsonl

Re-runs are deterministic given the substrate manifest and the
control pool YAML.

Usage:
    python3 scripts/generate_signature_controls.py --pool aquitanian
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_DEFAULT_HYPOTHESES_DIR = _REPO_ROOT / "hypotheses" / "auto_signatures"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"
_SIGNATURE_SCHEMA_PATH = (
    _REPO_ROOT
    / "harness"
    / "schemas"
    / "hypothesis.candidate_signature.v1.schema.json"
)

_SYLLABOGRAM_RE = re.compile(r"^A[B]?\d+$")


def _is_syllabogram(tok: str) -> bool:
    return bool(_SYLLABOGRAM_RE.fullmatch(tok))


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def _load_pool(pool_name: str, pools_dir: Path) -> dict:
    pool_path = pools_dir / f"{pool_name}.yaml"
    with pool_path.open("r", encoding="utf-8") as fh:
        pool = yaml.load(fh, Loader=_StringDateLoader)
    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(pool)
    if pool["pool"] != pool_name:
        raise ValueError(
            f"pool YAML declares pool={pool['pool']!r}, but file basename is {pool_name!r}"
        )
    return pool


def _load_signature(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def _load_corpus(corpus_path: Path) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            by_id[rec["id"]] = rec
    return by_id


def _canonical_hash(doc: dict) -> str:
    payload = json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


_NAME_RE = re.compile(r"[^A-Za-z0-9_]")


def _slug(s: str) -> str:
    return _NAME_RE.sub("_", s)


def _trim_name(name: str, limit: int = 80) -> str:
    if len(name) <= limit:
        return name
    head = name[: limit - 9]
    tail_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    return f"{head}_{tail_hash}"


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def _phoneme_seq_edit_distance(a: list[str], b: list[str]) -> int:
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[m]


def _control_candidates_for(
    substrate_phonemes: list[str],
    control_entries_by_length: dict[int, list[tuple[int, list[str], dict]]],
) -> list[tuple[int, list[str], dict]]:
    """Return control entries of the same length as the substrate root,
    sorted by (edit distance to substrate phonemes, surface, entry index).
    """
    candidates = control_entries_by_length.get(len(substrate_phonemes), [])
    decorated = [
        (
            _phoneme_seq_edit_distance(substrate_phonemes, ph),
            entry["surface"],
            idx,
            ph,
            entry,
        )
        for idx, ph, entry in candidates
    ]
    decorated.sort(key=lambda t: (t[0], t[1], t[2]))
    return [(idx, ph, entry) for _d, _s, idx, ph, entry in decorated]


def _per_position_signs(
    inscription_tokens: list[str],
    window_start: int,
    span_within_window: list[int],
    n_phonemes: int,
) -> list[str] | None:
    """Recover the per-position sign sequence for one root placement."""
    s_off, e_off = span_within_window
    abs_start = window_start + s_off
    abs_end = window_start + e_off
    if abs_end >= len(inscription_tokens):
        return None
    signs: list[str] = []
    for i in range(abs_start, abs_end + 1):
        tok = inscription_tokens[i]
        if _is_syllabogram(tok):
            signs.append(tok)
    if len(signs) != n_phonemes:
        return None
    return signs


def _try_assign_controls(
    substrate_doc: dict,
    inscription_tokens: list[str],
    control_entries_by_length: dict[int, list[tuple[int, list[str], dict]]],
) -> list[dict] | None:
    """Try to find a consistent control assignment for a substrate signature.

    Returns the control roots[] list (same order, span_within_window, length
    distribution as substrate) or None if no consistent assignment exists.
    """
    sub_roots = substrate_doc["roots"]
    window_start = substrate_doc["window"]["span"][0]
    chosen: list[dict] = []
    combined: dict[str, str] = {}

    for sub_root in sub_roots:
        sub_phonemes = list(sub_root["phonemes"])
        signs = _per_position_signs(
            inscription_tokens=inscription_tokens,
            window_start=window_start,
            span_within_window=sub_root["span_within_window"],
            n_phonemes=len(sub_phonemes),
        )
        if signs is None:
            return None
        candidates = _control_candidates_for(sub_phonemes, control_entries_by_length)
        chosen_for_root: dict | None = None
        for _idx, ctrl_phonemes, entry in candidates:
            local_assign: dict[str, str] = {}
            ok = True
            for sign, ctrl_p in zip(signs, ctrl_phonemes):
                existing = local_assign.get(sign)
                if existing is not None and existing != ctrl_p:
                    ok = False
                    break
                local_assign[sign] = ctrl_p
            if not ok:
                continue
            conflict = False
            for s, p in local_assign.items():
                existing = combined.get(s)
                if existing is not None and existing != p:
                    conflict = True
                    break
            if conflict:
                continue
            chosen_for_root = {
                "surface": entry["surface"],
                "phonemes": list(ctrl_phonemes),
                "sign_to_phoneme": local_assign,
                "span_within_window": list(sub_root["span_within_window"]),
                "citation": entry.get(
                    "citation",
                    "Synthetic phonotactic control entry (see scripts/build_control_pools.py).",
                ),
            }
            for s, p in local_assign.items():
                combined[s] = p
            break
        if chosen_for_root is None:
            return None
        chosen.append(chosen_for_root)
    return chosen


def _build_control_doc(
    *,
    substrate_doc: dict,
    substrate_hash: str,
    control_pool_name: str,
    control_roots: list[dict],
) -> dict:
    window = substrate_doc["window"]
    inscription_id = window["inscription_id"]
    w_start, w_end = window["span"]
    surfaces = [_slug(r["surface"]) for r in control_roots]
    name = (
        f"sigctl_{control_pool_name}_{_slug(inscription_id)}_{w_start}_{w_end}_"
        + "_".join(surfaces)
    )
    name = _trim_name(name)
    description = (
        f"Auto-generated matched-control signature: pool={control_pool_name!r} "
        f"window [{w_start}..{w_end}] of {inscription_id}; "
        f"paired with substrate hypothesis {substrate_hash}."
    )
    n_window_syll = substrate_doc["coverage"]["n_window_syllabograms"]
    n_covered = substrate_doc["coverage"]["n_covered_syllabograms"]
    return {
        "schema_version": "candidate_signature.v1",
        "name": name,
        "description": description,
        "author": "scripts/generate_signature_controls.py",
        "created": "2026-05-04",
        "source_pool": control_pool_name,
        "window": {
            "inscription_id": inscription_id,
            "span": [w_start, w_end],
        },
        "roots": control_roots,
        "coverage": {
            "n_window_syllabograms": n_window_syll,
            "n_covered_syllabograms": n_covered,
            "fraction": round(
                n_covered / n_window_syll if n_window_syll else 0.0, 6
            ),
        },
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def generate(
    *,
    substrate_pool_name: str,
    pools_dir: Path,
    corpus_path: Path,
    hypotheses_dir: Path,
    progress: bool = True,
    repo_root: Path | None = None,
) -> dict:
    if repo_root is None:
        repo_root = _REPO_ROOT
    control_pool_name = f"control_{substrate_pool_name}"
    control_pool = _load_pool(control_pool_name, pools_dir)
    control_entries_by_length: dict[int, list[tuple[int, list[str], dict]]] = {}
    for idx, entry in enumerate(control_pool["entries"]):
        ph = list(entry["phonemes"])
        control_entries_by_length.setdefault(len(ph), []).append((idx, ph, entry))

    corpus_by_id = _load_corpus(corpus_path)

    substrate_manifest_path = (
        hypotheses_dir / f"{substrate_pool_name}.manifest.jsonl"
    )
    if not substrate_manifest_path.exists():
        raise FileNotFoundError(
            f"substrate manifest not found: {substrate_manifest_path}; "
            f"run scripts/generate_signatures.py --pool {substrate_pool_name} first"
        )

    schema = json.loads(_SIGNATURE_SCHEMA_PATH.read_text(encoding="utf-8"))
    sig_validator = Draft202012Validator(schema)

    out_dir = hypotheses_dir / control_pool_name
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = hypotheses_dir / f"{control_pool_name}.manifest.jsonl"

    manifest_rows: list[dict] = []
    paired = 0
    dropped_no_match = 0

    with substrate_manifest_path.open("r", encoding="utf-8") as fh:
        substrate_rows = [json.loads(line) for line in fh if line.strip()]

    for sub_row in substrate_rows:
        sub_path = repo_root / sub_row["hypothesis_path"]
        substrate_doc = _load_signature(sub_path)
        record = corpus_by_id.get(substrate_doc["window"]["inscription_id"])
        if record is None:
            dropped_no_match += 1
            continue
        control_roots = _try_assign_controls(
            substrate_doc, record["tokens"], control_entries_by_length
        )
        if control_roots is None:
            dropped_no_match += 1
            continue
        ctrl_doc = _build_control_doc(
            substrate_doc=substrate_doc,
            substrate_hash=sub_row["hypothesis_hash"],
            control_pool_name=control_pool_name,
            control_roots=control_roots,
        )
        sig_validator.validate(ctrl_doc)
        h = _canonical_hash(ctrl_doc)
        sha8 = h.split(":", 1)[1][:8]
        yaml_path = out_dir / f"{sha8}.yaml"
        yaml_text = _dump_yaml(ctrl_doc)
        if not yaml_path.exists() or yaml_path.read_text(
            encoding="utf-8"
        ) != yaml_text:
            yaml_path.write_text(yaml_text, encoding="utf-8")
        rel_path = yaml_path.relative_to(repo_root).as_posix()
        manifest_rows.append(
            {
                "pool": control_pool_name,
                "substrate_pool": substrate_pool_name,
                "inscription_id": ctrl_doc["window"]["inscription_id"],
                "window_start": ctrl_doc["window"]["span"][0],
                "window_end": ctrl_doc["window"]["span"][1],
                "n_roots": len(control_roots),
                "root_surfaces": sorted(r["surface"] for r in control_roots),
                "n_window_syllabograms": ctrl_doc["coverage"][
                    "n_window_syllabograms"
                ],
                "n_covered_syllabograms": ctrl_doc["coverage"][
                    "n_covered_syllabograms"
                ],
                "coverage_fraction": ctrl_doc["coverage"]["fraction"],
                "hypothesis_path": rel_path,
                "hypothesis_hash": h,
                "paired_substrate_hash": sub_row["hypothesis_hash"],
            }
        )
        paired += 1

    manifest_rows.sort(
        key=lambda r: (
            r["inscription_id"],
            r["window_start"],
            r["window_end"],
            tuple(r["root_surfaces"]),
            r["hypothesis_hash"],
        )
    )

    expected = {Path(r["hypothesis_path"]).name for r in manifest_rows}
    pruned = 0
    for existing in sorted(out_dir.glob("*.yaml")):
        if existing.name not in expected:
            existing.unlink()
            pruned += 1

    with manifest_path.open("w", encoding="utf-8") as fh:
        for row in manifest_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {
        "substrate_pool": substrate_pool_name,
        "control_pool": control_pool_name,
        "substrate_signatures": len(substrate_rows),
        "controls_emitted": paired,
        "dropped_no_consistent_match": dropped_no_match,
        "controls_pruned_orphaned": pruned,
        "manifest_path": manifest_path.relative_to(repo_root).as_posix(),
        "out_dir": out_dir.relative_to(repo_root).as_posix(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pool", required=True, help="Substrate pool name.")
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS_DIR)
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument(
        "--hypotheses-dir", type=Path, default=_DEFAULT_HYPOTHESES_DIR
    )
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args(argv)

    summary = generate(
        substrate_pool_name=args.pool,
        pools_dir=args.pools_dir,
        corpus_path=args.corpus,
        hypotheses_dir=args.hypotheses_dir,
        progress=not args.no_progress,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
