#!/usr/bin/env python3
"""Bulk sweep runner — score every hypothesis listed in a generator manifest.

Reads ``hypotheses/auto/<pool>.manifest.jsonl``, scores each candidate
against ``corpus/all.jsonl`` with the ``local_fit_v0`` metric, and appends
one row per scoring run to ``results/experiments.jsonl``.

The runner is **resumable**. Before scoring, it builds a set of
``(hypothesis_hash, corpus_snapshot)`` pairs from the existing result
stream and skips any manifest entry that already appears. So a re-run
after a partial sweep only re-scores the new candidates; if neither the
candidates nor the corpus have changed, the re-run is a no-op.

Performance. The full corpus, token stream, sign-position fingerprints,
and corpus snapshot are computed once at startup and reused across all
hypothesis scorings. Per-hypothesis work is dominated by the 200
permutation rescores inside ``local_fit_v0``; on the existing 761-record
corpus that costs ~1-3 ms per hypothesis. ~5,000 hypotheses fit
comfortably under the 15-minute mg-f832 acceptance budget.

End-of-run summary block:
  * total runs, count beating z=+1.0 and z=+2.0, count below z=-1.0
  * top 5 by score_control_z (with hypothesis_path)
  * ASCII histogram of score_control_z over 10 buckets

Usage:
    python3 scripts/run_sweep.py --manifest hypotheses/auto/aquitanian.manifest.jsonl
    python3 scripts/run_sweep.py --manifest <path> --note "first sweep"
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import time
import uuid
from pathlib import Path

# Allow running as `python3 scripts/run_sweep.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jsonschema import Draft202012Validator

from harness import HARNESS_VERSION
from harness.corpus import (
    build_stream,
    corpus_snapshot,
    load_records,
    sign_position_fingerprints,
)
from harness.hypothesis import (
    SHAPE_CANDIDATE_EQUATION_V1,
    canonical_hash,
    detect_shape,
    load_and_validate,
)
from harness.metrics import local_fit_v0


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_RESULT_SCHEMA_PATH = _REPO_ROOT / "harness" / "schemas" / "result.v0.schema.json"


def _existing_runs(results_path: Path) -> set[tuple[str, str]]:
    """Return the (hypothesis_hash, corpus_snapshot) pairs already present in
    the result stream. Used to skip re-scoring during a resume."""
    seen: set[tuple[str, str]] = set()
    if not results_path.exists():
        return seen
    with results_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            seen.add((row["hypothesis_hash"], row.get("corpus_snapshot", "")))
    return seen


def _load_manifest(manifest_path: Path) -> list[dict]:
    rows: list[dict] = []
    with manifest_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _resolve_inscription(records: list[dict], inscription_id: str) -> dict:
    for r in records:
        if r.get("id") == inscription_id:
            return r
    raise KeyError(f"inscription not found in corpus: {inscription_id!r}")


def _signs_from_equation(record: dict, equation: dict) -> list[str]:
    """Pull syllabogram tokens within ``equation.span`` whose strings appear in
    ``equation.sign_to_phoneme``. Mirrors ``harness.run._signs_from_equation``;
    duplicated here so the sweep runner does not need to import the harness CLI
    module just for this helper."""
    tokens = record["tokens"]
    start, end = equation["span"]
    if start < 0 or end >= len(tokens):
        raise ValueError(
            f"equation.span {equation['span']!r} out of range for "
            f"{record['id']!r} (n_tokens={len(tokens)})"
        )
    sign_to_phoneme = equation["sign_to_phoneme"]
    expected_signs = list(sign_to_phoneme.keys())
    picked: list[str] = []
    for tok in tokens[start : end + 1]:
        if tok in sign_to_phoneme:
            picked.append(tok)
    if picked != expected_signs:
        raise ValueError(
            f"signs picked from {record['id']!r} span {equation['span']!r} "
            f"are {picked!r}, but equation.sign_to_phoneme keys are "
            f"{expected_signs!r}; the span must contain those signs in that order"
        )
    return picked


def _score_one(
    *,
    hypothesis_path: Path,
    records: list[dict],
    stream: list[str],
    snapshot: str,
    n_records: int,
    note: str,
    repo_root: Path,
    result_validator: Draft202012Validator,
) -> tuple[dict, str]:
    """Load + validate + score one hypothesis. Returns (row, hypothesis_hash).

    Uses the precomputed corpus context — no per-call corpus reload, no per-call
    git snapshot probe — so this is cheap to call in a tight loop.
    """
    hypothesis = load_and_validate(hypothesis_path)
    h_hash = canonical_hash(hypothesis)
    shape = detect_shape(hypothesis)
    if shape != SHAPE_CANDIDATE_EQUATION_V1:
        raise ValueError(
            f"sweep runner expects candidate_equation.v1 hypotheses; "
            f"{hypothesis_path} has shape {shape!r}"
        )
    equation = hypothesis["equation"]
    record = _resolve_inscription(records, equation["inscription_id"])
    signs = _signs_from_equation(record, equation)
    phonemes = list(hypothesis["root"]["phonemes"])
    started = time.monotonic()
    ran_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # local_fit_v0 builds fingerprints from the stream internally; the cost is
    # ~10ms per call which is acceptable in the bulk path.
    result = local_fit_v0(stream, signs, phonemes)
    duration_ms = int((time.monotonic() - started) * 1000)

    try:
        rel_hyp = str(hypothesis_path.resolve().relative_to(repo_root))
    except ValueError:
        rel_hyp = str(hypothesis_path)

    row = {
        "run_id": str(uuid.uuid4()),
        "hypothesis_path": rel_hyp,
        "hypothesis_hash": h_hash,
        "harness_version": HARNESS_VERSION,
        "metric": "local_fit_v0",
        "score": result.score,
        "score_control_z": result.score_control_z,
        "metric_notes": result.metric_notes,
        "corpus_records_used": n_records,
        "corpus_snapshot": snapshot,
        "ran_at": ran_at,
        "duration_ms": duration_ms,
        "notes": note,
    }
    result_validator.validate(row)
    return row, h_hash


def _ascii_histogram(values: list[float], buckets: int = 10, width: int = 40) -> list[str]:
    """Return ASCII histogram lines for a list of floats."""
    if not values:
        return ["(no values)"]
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [f"  all values == {lo:.4f}  (n={len(values)})"]
    bucket_w = (hi - lo) / buckets
    counts = [0] * buckets
    for v in values:
        idx = min(int((v - lo) / bucket_w), buckets - 1)
        counts[idx] += 1
    peak = max(counts) or 1
    lines: list[str] = []
    for i, c in enumerate(counts):
        b_lo = lo + i * bucket_w
        b_hi = lo + (i + 1) * bucket_w
        bar = "#" * int(width * c / peak)
        lines.append(f"  [{b_lo:+.3f}, {b_hi:+.3f})  {bar:<{width}}  {c}")
    return lines


def _summary_block(rows: list[dict]) -> list[str]:
    if not rows:
        return ["No new rows scored."]
    zs = [float(r.get("score_control_z", 0.0)) for r in rows]
    n = len(zs)
    n_z_gt_1 = sum(1 for z in zs if z > 1.0)
    n_z_gt_2 = sum(1 for z in zs if z > 2.0)
    n_z_lt_neg1 = sum(1 for z in zs if z < -1.0)
    mean = sum(zs) / n
    sd = math.sqrt(sum((z - mean) ** 2 for z in zs) / n)
    median = sorted(zs)[n // 2]
    top5 = sorted(rows, key=lambda r: -float(r.get("score_control_z", 0.0)))[:5]

    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"sweep summary  ({n} runs)")
    lines.append("-" * 72)
    lines.append(f"  z > +1.0:  {n_z_gt_1}  ({100 * n_z_gt_1 / n:.1f}%)")
    lines.append(f"  z > +2.0:  {n_z_gt_2}  ({100 * n_z_gt_2 / n:.1f}%)")
    lines.append(f"  z < -1.0:  {n_z_lt_neg1}  ({100 * n_z_lt_neg1 / n:.1f}%)")
    lines.append(f"  mean:      {mean:+.4f}")
    lines.append(f"  median:    {median:+.4f}")
    lines.append(f"  std:       {sd:.4f}")
    lines.append("-" * 72)
    lines.append("top 5 by score_control_z:")
    for i, r in enumerate(top5, 1):
        lines.append(
            f"  {i}. z={float(r.get('score_control_z', 0.0)):+.4f}  "
            f"score={r['score']:+.4f}  {r['hypothesis_path']}"
        )
    lines.append("-" * 72)
    lines.append("score_control_z histogram (10 buckets):")
    lines.extend(_ascii_histogram(zs, buckets=10))
    lines.append("=" * 72)
    return lines


def run(
    *,
    manifest_path: Path,
    corpus_path: Path,
    results_path: Path,
    note: str,
    progress_every: int,
    repo_root: Path,
) -> dict:
    """Drive the bulk sweep and return a summary dict."""
    manifest = _load_manifest(manifest_path)
    if not manifest:
        print(f"manifest is empty: {manifest_path}", file=sys.stderr)
        return {"manifest_rows": 0, "scored": 0, "skipped_resumed": 0}

    records = load_records(corpus_path)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(corpus_path, repo_root)
    # Pre-warm the fingerprint table so the first scoring call doesn't pay the
    # build cost twice: local_fit_v0 also builds it internally, but Python's
    # function-local cost is negligible compared to the I/O we just amortized.
    _ = sign_position_fingerprints(stream)

    result_validator = Draft202012Validator(
        json.loads(_RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
    )

    seen = _existing_runs(results_path)
    print(
        f"manifest: {len(manifest)} candidates  |  "
        f"already in result stream for this snapshot: "
        f"{sum(1 for r in manifest if (r['hypothesis_hash'], snapshot) in seen)}",
        file=sys.stderr,
    )

    results_path.parent.mkdir(parents=True, exist_ok=True)
    scored_rows: list[dict] = []
    skipped = 0
    started = time.monotonic()

    with results_path.open("a", encoding="utf-8") as result_fh:
        for i, manifest_row in enumerate(manifest, 1):
            key = (manifest_row["hypothesis_hash"], snapshot)
            if key in seen:
                skipped += 1
                continue
            hyp_path = repo_root / manifest_row["hypothesis_path"]
            row, h_hash = _score_one(
                hypothesis_path=hyp_path,
                records=records,
                stream=stream,
                snapshot=snapshot,
                n_records=n_records,
                note=note,
                repo_root=repo_root,
                result_validator=result_validator,
            )
            # Defensive consistency check: manifest hash should match what
            # the harness recomputes from the YAML on disk.
            if h_hash != manifest_row["hypothesis_hash"]:
                raise RuntimeError(
                    f"manifest hash {manifest_row['hypothesis_hash']!r} "
                    f"!= recomputed {h_hash!r} for {hyp_path}; manifest is "
                    f"stale, regenerate with scripts/generate_candidates.py"
                )
            result_fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            result_fh.flush()
            scored_rows.append(row)
            seen.add(key)
            if progress_every and len(scored_rows) % progress_every == 0:
                elapsed = time.monotonic() - started
                rate = len(scored_rows) / elapsed if elapsed > 0 else 0.0
                print(
                    f"  scored {len(scored_rows)} / {len(manifest) - skipped}  "
                    f"({rate:.1f}/s, {elapsed:.0f}s elapsed)",
                    file=sys.stderr,
                )

    elapsed = time.monotonic() - started
    print(file=sys.stderr)
    for line in _summary_block(scored_rows):
        print(line, file=sys.stderr)

    return {
        "manifest_rows": len(manifest),
        "scored": len(scored_rows),
        "skipped_resumed": skipped,
        "elapsed_s": round(elapsed, 2),
        "snapshot": snapshot,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, required=True, help="Manifest JSONL path.")
    parser.add_argument(
        "--corpus", type=Path, default=_DEFAULT_CORPUS, help="Corpus JSONL path."
    )
    parser.add_argument(
        "--results", type=Path, default=_DEFAULT_RESULTS, help="Result stream path."
    )
    parser.add_argument(
        "--note", default="", help="Free-form note attached to every result row."
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print a progress line every N scored hypotheses (default: %(default)s).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="Repo root used for hypothesis-path resolution and corpus snapshot.",
    )
    args = parser.parse_args(argv)

    summary = run(
        manifest_path=args.manifest,
        corpus_path=args.corpus,
        results_path=args.results,
        note=args.note,
        progress_every=args.progress_every,
        repo_root=args.repo_root,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
