#!/usr/bin/env python3
"""Score every entry in `hypotheses/curated/CONSTRUCTION.manifest.jsonl`
under all three v3 metrics, dispatching the pool-context per-hypothesis
via ``harness.run.score_hypothesis``. Append rows to
``results/experiments.jsonl``; the runner is resumable through
``(hypothesis_hash, corpus_snapshot, metric)``.

Why a separate wrapper? ``scripts/run_sweep.py`` takes one ``--pool``
argument and uses it for every candidate, but the curated set spans
five `source_pool` tags (aquitanian, toponym, linear_b_carryover,
random_scramble, pre_greek_toponym). ``harness.run.score_hypothesis``
already infers the pool per-hypothesis via ``source_pool`` →
``pools/<name>.yaml`` with an aquitanian fallback, so we drive that
function directly here.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.run import append_row, score_hypothesis


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_MANIFEST = _REPO_ROOT / "hypotheses" / "curated" / "CONSTRUCTION.manifest.jsonl"
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_METRICS = (
    "local_fit_v1",
    "partial_mapping_compression_delta_v0",
    "geographic_genre_fit_v1",
)


def _existing_keys(results_path: Path) -> set[tuple[str, str, str]]:
    seen: set[tuple[str, str, str]] = set()
    if not results_path.exists():
        return seen
    with results_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            seen.add(
                (
                    row["hypothesis_hash"],
                    row.get("corpus_snapshot", ""),
                    row.get("metric", ""),
                )
            )
    return seen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, default=_DEFAULT_MANIFEST)
    parser.add_argument("--results", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument(
        "--metrics",
        default=",".join(_METRICS),
        help=f"comma-separated; default {','.join(_METRICS)}",
    )
    parser.add_argument(
        "--note", default="mg-7c8c curated v4 sweep", help="note attached to each row"
    )
    args = parser.parse_args(argv)

    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    manifest_rows: list[dict] = []
    with args.manifest.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            manifest_rows.append(json.loads(line))

    seen = _existing_keys(args.results)
    scored = 0
    skipped = 0
    started = time.monotonic()
    for i, mr in enumerate(manifest_rows, 1):
        hyp_path = _REPO_ROOT / mr["hypothesis_path"]
        for metric in metrics:
            for_skip_check_snapshot = None  # populated after first score
            # First we need the snapshot for the resume check; harness.run
            # computes it. To avoid recomputing, do a probe via
            # score_hypothesis on one hypothesis and read the snapshot back.
            # The simplest reliable path: just score; the score_hypothesis
            # call computes snapshot internally. To be resume-safe, we
            # check (hash, "", metric) and (hash, snapshot, metric); the
            # easiest is to score and post-filter, but that wastes work.
            # Instead: we know the hash from the manifest, but not the
            # snapshot up front. Strategy: score once per (hypothesis,
            # metric) and then check seen using the row's snapshot. If
            # already present, discard.
            row = score_hypothesis(
                hypothesis_path=hyp_path,
                metric_name=metric,
                note=args.note,
            )
            key = (
                row["hypothesis_hash"],
                row.get("corpus_snapshot", ""),
                row.get("metric", ""),
            )
            if key in seen:
                skipped += 1
                continue
            append_row(row, args.results)
            seen.add(key)
            scored += 1
        if i % 20 == 0:
            print(
                f"  {i}/{len(manifest_rows)}  scored={scored}  skipped={skipped}  "
                f"elapsed={time.monotonic() - started:.1f}s",
                file=sys.stderr,
            )
    print(
        json.dumps(
            {
                "manifest_rows": len(manifest_rows),
                "metrics": metrics,
                "scored": scored,
                "skipped_resumed": skipped,
                "elapsed_s": round(time.monotonic() - started, 2),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
