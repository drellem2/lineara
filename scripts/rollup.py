#!/usr/bin/env python3
"""Render a markdown leaderboard from results/experiments.jsonl to stdout.

Not committed as state — regenerate on demand. Append-only result history is
the source of truth; this is a view over it.

Per-metric ordering:
  * compression_delta_v0 — sorted by ``score`` desc.
  * local_fit_v0         — sorted by ``score_control_z`` desc.

Examples:
  python3 scripts/rollup.py
  python3 scripts/rollup.py --metric compression_delta_v0
  python3 scripts/rollup.py --metric local_fit_v0
  python3 scripts/rollup.py --top 20
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _sort_key(row: dict) -> float:
    """Per-metric sort key. Higher = better; we sort descending."""
    if row["metric"] == "local_fit_v0":
        return float(row.get("score_control_z", 0.0))
    return float(row["score"])


def _render_compression_delta(group: list[dict]) -> list[str]:
    out = ["| rank | score | bps_baseline | bps_mapped | hypothesis | run_id | ran_at |"]
    out.append("|---:|---:|---:|---:|---|---|---|")
    for i, r in enumerate(group, 1):
        out.append(
            "| {rank} | {score:.4f} | {bb:.4f} | {bm:.4f} | `{hyp}` | `{rid}` | {at} |".format(
                rank=i,
                score=r["score"],
                bb=r.get("bits_per_sign_baseline", float("nan")),
                bm=r.get("bits_per_sign_mapped", float("nan")),
                hyp=r["hypothesis_path"],
                rid=r["run_id"][:8],
                at=r["ran_at"],
            )
        )
    return out


def _render_local_fit(group: list[dict]) -> list[str]:
    out = ["| rank | score_control_z | score | hypothesis | run_id | ran_at |"]
    out.append("|---:|---:|---:|---|---|---|")
    for i, r in enumerate(group, 1):
        out.append(
            "| {rank} | {z:.4f} | {score:.4f} | `{hyp}` | `{rid}` | {at} |".format(
                rank=i,
                z=float(r.get("score_control_z", 0.0)),
                score=r["score"],
                hyp=r["hypothesis_path"],
                rid=r["run_id"][:8],
                at=r["ran_at"],
            )
        )
    return out


def render(rows: list[dict], metric_filter: str | None, top: int | None) -> str:
    by_metric: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        m = row.get("metric")
        if metric_filter and m != metric_filter:
            continue
        by_metric[m].append(row)

    if not by_metric:
        return "_(no result rows match)_\n"

    out: list[str] = []
    for metric in sorted(by_metric):
        group = sorted(by_metric[metric], key=_sort_key, reverse=True)
        n_total = len(by_metric[metric])
        if top is not None:
            group = group[:top]
        out.append(f"## {metric} ({n_total} rows)\n")
        if metric == "local_fit_v0":
            out.extend(_render_local_fit(group))
        else:
            out.extend(_render_compression_delta(group))
        out.append("")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--results",
        type=Path,
        default=_DEFAULT_RESULTS,
        help="Path to results/experiments.jsonl (default: %(default)s).",
    )
    parser.add_argument("--metric", default=None, help="Restrict to a single metric name.")
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Show only the top N rows per metric (default: all).",
    )
    args = parser.parse_args(argv)

    rows = load_rows(args.results)
    sys.stdout.write(render(rows, args.metric, args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
