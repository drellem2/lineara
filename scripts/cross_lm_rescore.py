#!/usr/bin/env python3
"""Cross-substrate negative-control rescore (mg-0f97, harness v11).

Validates the v10 (mg-d26d) right-tail bayesian PASS by re-scoring every
existing v8 + v9 substrate + control hypothesis under the *other*
substrate's external phoneme language model:

* aquitanian + control_aquitanian → etruscan LM
* etruscan   + control_etruscan   → basque LM

If v10's substrate-vs-control separation is real substrate signal, the
separation should *collapse* under the wrong LM (the LM no longer
matches the substrate's phonotactics). If the separation persists, the
v10 metric is preferring some character distribution regardless of the
substrate-LM relationship, which would invalidate the substrate
specificity claim.

Each (hypothesis, swapped-LM) pair appends one row to
``results/experiments.external_phoneme_perplexity_v0.jsonl`` with
``language=`` set to the swapped LM (so the existing v10 same-LM rollup
can still select its rows by language). Idempotent: skips
``(hypothesis_hash, language)`` pairs already present in the result
stream(s).

Toponym pool is intentionally excluded (v10 already failed for toponym
controls; the cross-LM control would be moot).

Usage
=====
    python3 scripts/cross_lm_rescore.py
    python3 scripts/cross_lm_rescore.py --pools aquitanian
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import uuid
from pathlib import Path

# Allow running as `python3 scripts/cross_lm_rescore.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jsonschema import Draft202012Validator

from harness import HARNESS_VERSION
from harness.corpus import build_stream, corpus_snapshot, load_records
from harness.external_phoneme_model import ExternalPhonemeModel
from harness.hypothesis import (
    SHAPE_CANDIDATE_EQUATION_V1,
    SHAPE_CANDIDATE_SIGNATURE_V1,
    canonical_hash,
    detect_shape,
    load_and_validate,
    signature_combined_mapping,
)
from harness.metrics import external_phoneme_perplexity_v0


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_RESULTS_DIR = _REPO_ROOT / "results"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"
_DEFAULT_EXT_MODEL_DIR = _REPO_ROOT / "harness" / "external_phoneme_models"
_RESULT_SCHEMA_PATH = _REPO_ROOT / "harness" / "schemas" / "result.v0.schema.json"
_METRIC = "external_phoneme_perplexity_v0"
_SIDECAR_PATH = _DEFAULT_RESULTS_DIR / f"experiments.{_METRIC}.jsonl"
_PRIMARY_PATH = _DEFAULT_RESULTS_DIR / "experiments.jsonl"


# Cross-LM dispatch: substrate pool → swapped LM. The control side
# inherits its substrate's swapped LM so the paired_diff cancels the LM
# choice out of the comparison (same logic as run_sweep's same-LM
# dispatch). Toponym is intentionally absent — v10 already failed for
# toponym controls (sampler issue, not substrate-side issue), so the
# cross-LM negative control is not informative there.
_CROSS_LM_DISPATCH: dict[str, str] = {
    "aquitanian": "etruscan",
    "control_aquitanian": "etruscan",
    "etruscan": "basque",
    "control_etruscan": "basque",
}

# mg-4664: third cross-LM check. Re-routes the same Aquitanian +
# Etruscan substrate / control candidates through the Mycenaean-Greek
# LM (a third natural-language LM, neither own-LM nor cross-LM
# Etruscan/Basque). If Aquitanian still beats its control under
# Mycenaean-Greek, that's "natural-language LM bias" — Aquitanian
# surfaces have a phonotactic profile that any natural-language LM
# rewards. If Aquitanian no longer beats its control, the v11 partial
# cross-LM separation is a Basque-Etruscan kinship artifact and the
# v10 Aquitanian PASS is more genuinely substrate-specific than v11
# suggested. Etruscan under Mycenaean-Greek is a sanity check — should
# NOT beat its control under an unrelated LM.
_THIRD_LM_DISPATCH: dict[str, str] = {
    "aquitanian": "mycenaean_greek",
    "control_aquitanian": "mycenaean_greek",
    "etruscan": "mycenaean_greek",
    "control_etruscan": "mycenaean_greek",
}

# mg-6ccd (harness v21): Eteocretan cross-LM negative control. Routes
# the v21 Eteocretan substrate + bigram-preserving control candidates
# through the Basque LM (a natural-language LM unrelated to the
# Eteocretan corpus). If the v21 PASS is real Eteocretan-LM signal,
# the substrate-vs-control gap should shrink or invert under Basque.
# If the gap survives, the v21 separation is "natural-language LM
# preference for whichever surfaces happen to look phonotactically
# clean," not Eteocretan-specific signal.
_ETEOCRETAN_CROSS_LM_DISPATCH: dict[str, str] = {
    "eteocretan": "basque",
    "control_eteocretan_bigram": "basque",
}

# mg-b599 (harness v23): full cross-LM matrix for Eteocretan. Five
# additional dispatch tables fill out the LM × pool grid:
#
# (1) ``eteocretan_under_mg`` — Eteocretan + control under Mycenaean
#     Greek LM. A truly unrelated LM (Indo-European, Bronze-Age
#     Greek). Should NOT reward Eteocretan-shaped phonemes if the v21
#     PASS reflects substrate-LM-phonotactic kinship rather than a
#     generic natural-language-LM bias.
# (2) ``eteocretan_under_etruscan`` — Eteocretan + control under
#     Etruscan LM. Both are Mediterranean substrate-style LMs but
#     historically unrelated (Etruscan is Italic; Eteocretan is
#     presumed Linear-A continuation in Crete). A PASS here would
#     suggest Mediterranean-natural-language-LM bias in general; a
#     FAIL would corroborate the Eteocretan-specific signal.
# (3-5) ``{aquitanian,etruscan,toponym}_under_eteocretan`` — the
#     reverse direction: do other substrate pools score well under
#     the closest-genealogical-relative LM? If yes, the Eteocretan
#     LM is detecting general substrate-style phonotactics; if no,
#     the Eteocretan LM has Eteocretan-specific selectivity. Either
#     is informative for the methodology paper's "what does the LM
#     detect" framing.
_ETEOCRETAN_UNDER_MG_DISPATCH: dict[str, str] = {
    "eteocretan": "mycenaean_greek",
    "control_eteocretan_bigram": "mycenaean_greek",
}

_ETEOCRETAN_UNDER_ETRUSCAN_DISPATCH: dict[str, str] = {
    "eteocretan": "etruscan",
    "control_eteocretan_bigram": "etruscan",
}

_AQUITANIAN_UNDER_ETEOCRETAN_DISPATCH: dict[str, str] = {
    "aquitanian": "eteocretan",
    "control_aquitanian": "eteocretan",
}

_ETRUSCAN_UNDER_ETEOCRETAN_DISPATCH: dict[str, str] = {
    "etruscan": "eteocretan",
    "control_etruscan": "eteocretan",
}

_TOPONYM_UNDER_ETEOCRETAN_DISPATCH: dict[str, str] = {
    "toponym": "eteocretan",
    "control_toponym_bigram": "eteocretan",
}


def _load_manifest(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _load_seen(*paths: Path) -> set[tuple[str, str]]:
    """Return the (hypothesis_hash, language) pairs already present in
    the result stream(s) for the LM metric. Used to skip rescoring
    during a resume."""
    seen: set[tuple[str, str]] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row.get("metric") != _METRIC:
                    continue
                h = row.get("hypothesis_hash")
                lang = row.get("language", "")
                if not h:
                    continue
                seen.add((h, lang))
    return seen


def _all_metric_paths(results_dir: Path) -> list[Path]:
    """All result-stream files that may contain rows for ``_METRIC``.

    Mirrors the per_surface_bayesian_rollup loader: the primary
    ``experiments.jsonl``, the per-metric primary sidecar, plus every
    tagged sidecar matching ``experiments.{_METRIC}.*.jsonl``. mg-b599
    extends the resume cache to honour all of these so a re-run with
    ``--sidecar-tag <tag>`` does not duplicate rows that already exist
    in a different (e.g. legacy) sidecar.
    """
    out: list[Path] = [
        results_dir / "experiments.jsonl",
        results_dir / f"experiments.{_METRIC}.jsonl",
    ]
    out.extend(sorted(results_dir.glob(f"experiments.{_METRIC}.*.jsonl")))
    # Deduplicate while preserving order.
    seen: set[Path] = set()
    deduped: list[Path] = []
    for p in out:
        if p in seen:
            continue
        seen.add(p)
        deduped.append(p)
    return deduped


def _build_row(
    *,
    hypothesis_path: Path,
    h_hash: str,
    snapshot: str,
    n_records: int,
    note: str,
    repo_root: Path,
    score: float,
    metric_notes: str,
    n_runs: int,
    n_chars_scored: int,
    n_phonemes_scored: int,
    total_loglik: float,
    language: str,
    duration_ms: int,
) -> dict:
    try:
        rel_hyp = str(hypothesis_path.resolve().relative_to(repo_root))
    except ValueError:
        rel_hyp = str(hypothesis_path)
    return {
        "run_id": str(uuid.uuid4()),
        "hypothesis_path": rel_hyp,
        "hypothesis_hash": h_hash,
        "harness_version": HARNESS_VERSION,
        "metric": _METRIC,
        "score": float(score),
        "corpus_records_used": int(n_records),
        "corpus_snapshot": snapshot,
        "ran_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_ms": int(duration_ms),
        "notes": note,
        "metric_notes": metric_notes,
        "n_runs": int(n_runs),
        "n_chars_scored": int(n_chars_scored),
        "n_phonemes_scored": int(n_phonemes_scored),
        "total_loglik": float(total_loglik),
        "language": language,
    }


def run(
    *,
    corpus_path: Path,
    results_dir: Path,
    auto_dir: Path,
    auto_sig_dir: Path,
    ext_model_dir: Path,
    pools: list[str],
    note: str,
    progress_every: int,
    repo_root: Path,
    dispatch: dict[str, str] | None = None,
    sidecar_tag: str | None = None,
) -> dict:
    if dispatch is None:
        dispatch = _CROSS_LM_DISPATCH
    # Validate dispatch coverage upfront.
    unknown = [p for p in pools if p not in dispatch]
    if unknown:
        raise ValueError(
            f"unknown pools for cross-LM rescore: {unknown!r}; supported: "
            f"{sorted(dispatch.keys())}"
        )

    records = load_records(corpus_path)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(corpus_path, repo_root)
    print(
        f"corpus: {len(records)} records  |  stream length: {len(stream)}  |  "
        f"snapshot: {snapshot}",
        file=sys.stderr,
    )

    # Load every LM we'll need.
    languages = sorted({dispatch[p] for p in pools})
    external_models: dict[str, ExternalPhonemeModel] = {}
    for lang in languages:
        ext_path = ext_model_dir / f"{lang}.json"
        if not ext_path.exists():
            raise ValueError(
                f"external LM {lang!r} not found at {ext_path}; build with "
                f"scripts/build_external_phoneme_models.py"
            )
        external_models[lang] = ExternalPhonemeModel.load_json(ext_path)
        m = external_models[lang]
        print(
            f"loaded external LM: {ext_path}  |  α={m.alpha}  |  "
            f"vocab={len(m.bigram_log_probs)}  |  meta={m.meta}",
            file=sys.stderr,
        )

    if sidecar_tag:
        sidecar_path = results_dir / f"experiments.{_METRIC}.{sidecar_tag}.jsonl"
    else:
        sidecar_path = results_dir / f"experiments.{_METRIC}.jsonl"
    # Resume cache: include every result-stream file that may contain
    # rows for this metric (primary + per-metric sidecar + every tagged
    # sidecar). Without this, a tagged-sidecar re-run would re-rescore
    # rows that legacy runs wrote to a different file.
    seen_paths = _all_metric_paths(results_dir)
    seen = _load_seen(*seen_paths)
    print(
        f"seen ({_METRIC}): {len(seen)} (hash, language) pairs across "
        f"{len(seen_paths)} files; writing to {sidecar_path.name}",
        file=sys.stderr,
    )

    result_validator = Draft202012Validator(
        json.loads(_RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
    )

    # Build the work list. v8 manifests live under auto/<pool>; v9
    # signature manifests under auto_signatures/<pool>. Both pool ids
    # appear under both directories (substrate + control_<pool>).
    work: list[tuple[dict, str]] = []  # (manifest_row, target_language)
    for pool in pools:
        target_lang = dispatch[pool]
        v8_path = auto_dir / f"{pool}.manifest.jsonl"
        v9_path = auto_sig_dir / f"{pool}.manifest.jsonl"
        v8_rows = _load_manifest(v8_path)
        v9_rows = _load_manifest(v9_path)
        print(
            f"pool={pool!r}  v8={len(v8_rows)}  v9={len(v9_rows)}  "
            f"target_LM={target_lang!r}",
            file=sys.stderr,
        )
        for r in v8_rows + v9_rows:
            work.append((r, target_lang))

    print(f"work: {len(work)} hypotheses to rescore", file=sys.stderr)

    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    fh = sidecar_path.open("a", encoding="utf-8")
    started = time.monotonic()
    scored = 0
    skipped = 0
    try:
        for i, (manifest_row, target_lang) in enumerate(work, 1):
            h_hash = manifest_row["hypothesis_hash"]
            key = (h_hash, target_lang)
            if key in seen:
                skipped += 1
                continue

            hyp_path = repo_root / manifest_row["hypothesis_path"]
            hypothesis = load_and_validate(hyp_path)
            shape = detect_shape(hypothesis)
            if shape not in (
                SHAPE_CANDIDATE_EQUATION_V1,
                SHAPE_CANDIDATE_SIGNATURE_V1,
            ):
                raise ValueError(
                    f"cross_lm_rescore: unsupported hypothesis shape {shape!r} "
                    f"for {hyp_path}"
                )
            recomputed = canonical_hash(hypothesis)
            if recomputed != h_hash:
                raise RuntimeError(
                    f"manifest hash {h_hash!r} != recomputed {recomputed!r} for "
                    f"{hyp_path}; manifest is stale"
                )
            if shape == SHAPE_CANDIDATE_EQUATION_V1:
                mapping = dict(hypothesis["equation"]["sign_to_phoneme"])
            else:
                mapping = dict(signature_combined_mapping(hypothesis))

            lm = external_models[target_lang]
            t0 = time.monotonic()
            result = external_phoneme_perplexity_v0(
                stream=stream, mapping=mapping, language_model=lm
            )
            duration_ms = int((time.monotonic() - t0) * 1000)

            row = _build_row(
                hypothesis_path=hyp_path,
                h_hash=h_hash,
                snapshot=snapshot,
                n_records=n_records,
                note=note,
                repo_root=repo_root,
                score=result.score,
                metric_notes=result.metric_notes,
                n_runs=result.n_runs,
                n_chars_scored=result.n_chars_scored,
                n_phonemes_scored=result.n_phonemes_scored,
                total_loglik=result.total_loglik,
                language=result.language,
                duration_ms=duration_ms,
            )
            result_validator.validate(row)
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            seen.add(key)
            scored += 1

            if progress_every and scored % progress_every == 0:
                elapsed = time.monotonic() - started
                rate = scored / elapsed if elapsed > 0 else 0.0
                remaining = len(work) - skipped - scored
                eta = remaining / rate if rate > 0 else float("inf")
                print(
                    f"  scored {scored}/{len(work) - skipped}  "
                    f"({rate:.1f}/s, {elapsed:.0f}s elapsed, eta {eta:.0f}s)",
                    file=sys.stderr,
                )
    finally:
        fh.close()

    elapsed = time.monotonic() - started
    summary = {
        "metric": _METRIC,
        "pools": pools,
        "cross_lm_dispatch": {p: dispatch[p] for p in pools},
        "n_work": len(work),
        "scored": scored,
        "skipped_resumed": skipped,
        "elapsed_s": round(elapsed, 2),
        "snapshot": snapshot,
        "sidecar": str(sidecar_path.relative_to(repo_root))
        if sidecar_path.is_relative_to(repo_root)
        else str(sidecar_path),
    }
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--ext-model-dir", type=Path, default=_DEFAULT_EXT_MODEL_DIR)
    parser.add_argument(
        "--pools",
        type=str,
        default="aquitanian,control_aquitanian,etruscan,control_etruscan",
        help="Comma-separated substrate pools to rescore under their swapped LM.",
    )
    parser.add_argument(
        "--mode",
        choices=(
            "cross",
            "third",
            "eteocretan_under_basque",
            "eteocretan_under_mg",
            "eteocretan_under_etruscan",
            "aquitanian_under_eteocretan",
            "etruscan_under_eteocretan",
            "toponym_under_eteocretan",
        ),
        default="cross",
        help=(
            "Which dispatch to use. ``cross`` (default) is mg-0f97's "
            "Aquitanian↔Etruscan swap. ``third`` is mg-4664's Mycenaean-"
            "Greek third-LM rescore for both Aquitanian and Etruscan. "
            "``eteocretan_under_basque`` (mg-6ccd, v21) routes the "
            "Eteocretan substrate + bigram-preserving control through "
            "the Basque LM — the v21 cross-LM negative control sketch. "
            "``eteocretan_under_mg``, ``eteocretan_under_etruscan``, "
            "``aquitanian_under_eteocretan``, ``etruscan_under_eteocretan``, "
            "``toponym_under_eteocretan`` (mg-b599, v23) fill out the "
            "full cross-LM matrix for Eteocretan: the substrate pool is "
            "rescored under the named non-own LM."
        ),
    )
    parser.add_argument(
        "--note",
        default="mg-0f97 harness v11 cross-LM negative control",
        help="Free-form note attached to every result row.",
    )
    parser.add_argument(
        "--sidecar-tag",
        type=str,
        default=None,
        help=(
            "Optional sidecar tag. When set, rescore rows are appended "
            "to ``results/experiments.<metric>.<tag>.jsonl`` rather than "
            "the primary metric sidecar. Used by mg-b599 / v23 to keep "
            "the ~42 MB of cross-LM matrix rows off the 88 MB primary "
            "sidecar (which is approaching GitHub's 100 MB push cap)."
        ),
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=500,
        help="Print a progress line every N scored rows (default: %(default)s).",
    )
    parser.add_argument("--repo-root", type=Path, default=_REPO_ROOT)
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    if args.mode == "third":
        dispatch = _THIRD_LM_DISPATCH
    elif args.mode == "eteocretan_under_basque":
        dispatch = _ETEOCRETAN_CROSS_LM_DISPATCH
    elif args.mode == "eteocretan_under_mg":
        dispatch = _ETEOCRETAN_UNDER_MG_DISPATCH
    elif args.mode == "eteocretan_under_etruscan":
        dispatch = _ETEOCRETAN_UNDER_ETRUSCAN_DISPATCH
    elif args.mode == "aquitanian_under_eteocretan":
        dispatch = _AQUITANIAN_UNDER_ETEOCRETAN_DISPATCH
    elif args.mode == "etruscan_under_eteocretan":
        dispatch = _ETRUSCAN_UNDER_ETEOCRETAN_DISPATCH
    elif args.mode == "toponym_under_eteocretan":
        dispatch = _TOPONYM_UNDER_ETEOCRETAN_DISPATCH
    else:
        dispatch = _CROSS_LM_DISPATCH
    summary = run(
        corpus_path=args.corpus,
        results_dir=args.results_dir,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        ext_model_dir=args.ext_model_dir,
        pools=pools,
        note=args.note,
        progress_every=args.progress_every,
        repo_root=args.repo_root,
        dispatch=dispatch,
        sidecar_tag=args.sidecar_tag,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
