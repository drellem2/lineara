#!/usr/bin/env python3
"""Substrate-vs-control per-surface leaderboard comparison (mg-f419).

For each substrate pool ({aquitanian, etruscan, toponym}) and its phonotactic
control (control_<name>), this script:

  1. Builds per-surface aggregates from results/experiments.jsonl using the
     same machinery as scripts/rollup.py --by surface (median pmcd per
     surface, ≥10 candidates per surface).
  2. Reports the distribution of per-surface medians, Mann-Whitney U,
     two-tail p-value, Cliff's δ, and observed median difference.
  3. Reports the rank of the highest-ranked control surface in the
     substrate pool's pool-only leaderboard.
  4. Emits an interleaved substrate-vs-control leaderboard ranked by median
     pmcd, with each row tagged ``substrate`` or ``control``.

Output: ``results/rollup.surface_aggregated.with_controls.md`` (markdown
leaderboard) and a stats summary printed to stdout.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.rollup import _aggregate_surfaces, load_rows


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_DEFAULT_OUT = _REPO_ROOT / "results" / "rollup.surface_aggregated.with_controls.md"

_PAIRS = (
    ("aquitanian", "control_aquitanian"),
    ("etruscan", "control_etruscan"),
    ("toponym", "control_toponym"),
)


def mann_whitney_u(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Mann-Whitney U with ties (mid-rank), normal-approximation two-tail
    p-value with continuity correction.

    Returns ``(U, p_two_tail, z)``. We use U for the *xs* group and the
    larger-of-(U, n_x*n_y - U) convention is **not** applied — U is reported
    as defined for xs so the caller can read directionality from
    ``cliffs_delta``. p-value is normal-approximation; for the smallest
    case (here xs/ys both ~50) this is conservative-enough for our purposes.
    """
    n_x, n_y = len(xs), len(ys)
    if n_x == 0 or n_y == 0:
        return 0.0, float("nan"), float("nan")
    pooled = sorted(
        [(v, "x") for v in xs] + [(v, "y") for v in ys], key=lambda t: t[0]
    )
    # Compute mid-ranks for ties.
    ranks = [0.0] * len(pooled)
    i = 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg_rank
        i = j + 1
    rank_sum_x = sum(r for r, t in zip(ranks, [g for _, g in pooled]) if t == "x")
    U_x = rank_sum_x - n_x * (n_x + 1) / 2.0

    # Tie-corrected variance.
    counts: dict[float, int] = {}
    for v, _ in pooled:
        counts[v] = counts.get(v, 0) + 1
    tie_term = sum(t**3 - t for t in counts.values())
    n = n_x + n_y
    mu = n_x * n_y / 2.0
    var = (n_x * n_y / 12.0) * ((n + 1) - tie_term / (n * (n - 1))) if n > 1 else 0.0
    if var <= 0:
        return U_x, float("nan"), float("nan")
    # Continuity correction.
    z = (U_x - mu - (0.5 if U_x > mu else -0.5 if U_x < mu else 0)) / math.sqrt(var)
    p_two = 2.0 * (1.0 - _normal_cdf(abs(z)))
    return U_x, p_two, z


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def cliffs_delta(xs: list[float], ys: list[float]) -> float:
    """Cliff's δ = (n_greater - n_less) / (n_x * n_y). Positive → xs > ys."""
    if not xs or not ys:
        return float("nan")
    greater = 0
    less = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x < y:
                less += 1
    return (greater - less) / (len(xs) * len(ys))


def _per_pool_aggregates(rows: list[dict], pool: str) -> list[dict]:
    return _aggregate_surfaces(
        rows, repo_root=_REPO_ROOT, pool_filter=pool, min_candidates=10
    )


def _summarize_distribution(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    sv = sorted(values)
    n = len(sv)
    return {
        "n": n,
        "min": sv[0],
        "p25": sv[max(0, n // 4)],
        "median": median(sv),
        "p75": sv[min(n - 1, (3 * n) // 4)],
        "max": sv[-1],
        "mean": sum(sv) / n,
    }


def compare_pair(rows: list[dict], substrate: str, control: str) -> dict:
    sub_aggs = _per_pool_aggregates(rows, substrate)
    ctrl_aggs = _per_pool_aggregates(rows, control)
    sub_meds = [a["median_pmcd"] for a in sub_aggs]
    ctrl_meds = [a["median_pmcd"] for a in ctrl_aggs]
    U, p, z = mann_whitney_u(sub_meds, ctrl_meds)
    delta = cliffs_delta(sub_meds, ctrl_meds)

    sub_dist = _summarize_distribution(sub_meds)
    ctrl_dist = _summarize_distribution(ctrl_meds)

    median_diff = (
        sub_dist.get("median", 0.0) - ctrl_dist.get("median", 0.0)
        if sub_meds and ctrl_meds
        else float("nan")
    )

    # Top-K substrate ranks vs highest-ranked control rank (in the
    # interleaved leaderboard sorted by median pmcd, descending).
    interleaved = sorted(
        [(a, "substrate") for a in sub_aggs] + [(a, "control") for a in ctrl_aggs],
        key=lambda t: -t[0]["median_pmcd"],
    )
    top_control_rank: int | None = None
    for i, (_a, kind) in enumerate(interleaved, 1):
        if kind == "control":
            top_control_rank = i
            break

    # Top-20 substrate-only median ranks.
    substrate_top_20_median = sorted(sub_meds, reverse=True)[:20]
    substrate_top_20_median_min = (
        substrate_top_20_median[-1] if substrate_top_20_median else float("nan")
    )

    return {
        "substrate_pool": substrate,
        "control_pool": control,
        "n_substrate_surfaces": len(sub_meds),
        "n_control_surfaces": len(ctrl_meds),
        "substrate_distribution": sub_dist,
        "control_distribution": ctrl_dist,
        "median_difference": median_diff,
        "mann_whitney_U": U,
        "mann_whitney_z": z,
        "mann_whitney_p_two_tail": p,
        "cliffs_delta": delta,
        "top_control_rank_in_interleaved": top_control_rank,
        "substrate_top_20_median_min": substrate_top_20_median_min,
        "interleaved": [
            {
                "kind": kind,
                "pool": a["pool"],
                "surface": a["surface"],
                "n": a["n_candidates"],
                "median_pmcd": a["median_pmcd"],
                "mean_pmcd": a["mean_pmcd"],
                "best_pmcd": a["best_score"],
                "best_inscription": a["best_inscription"],
                "geo_mean": a["geographic_mean"],
            }
            for a, kind in interleaved
        ],
    }


def render_markdown(comparisons: list[dict], top_per_pool: int = 30) -> str:
    """Render the substrate-vs-control interleaved leaderboard markdown."""
    out: list[str] = []
    out.append("# Substrate vs phonotactic-control per-surface leaderboard\n")
    out.append(
        "Generated by `scripts/compare_substrate_vs_control.py` (mg-f419). "
        "Compares each substrate pool's per-surface median pmcd leaderboard "
        "against a same-phoneme-inventory, same-length-distribution scramble "
        "control pool. Each control pool was generated by "
        "`scripts/build_control_pools.py` from the matching substrate pool.\n"
    )
    out.append(
        "**Reading guide.** A meaningful substrate signal has substrate surfaces "
        "ranking *above* the highest-ranked control surface, with a positive "
        "Cliff's δ on the per-surface medians and a two-tail Mann-Whitney "
        "p < 0.05. If `top_control_rank` is small (e.g. 1-5) the substrate "
        "leaderboard is barely separated from the control. If the substrate "
        "and control distributions of per-surface medians overlap, the "
        "substrate signal at this aggregation level is plausibly artifactual.\n"
    )

    for comp in comparisons:
        out.append(
            f"## {comp['substrate_pool']} vs {comp['control_pool']}\n"
        )
        sd = comp["substrate_distribution"]
        cd = comp["control_distribution"]
        out.append("### Per-surface median pmcd distributions\n")
        out.append(
            "| pool | n_surfaces | min | p25 | median | p75 | max | mean |"
        )
        out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        out.append(
            "| substrate | {n} | {mn:+.2f} | {p25:+.2f} | {med:+.2f} | {p75:+.2f} | "
            "{mx:+.2f} | {mean:+.2f} |".format(
                n=sd["n"], mn=sd["min"], p25=sd["p25"], med=sd["median"],
                p75=sd["p75"], mx=sd["max"], mean=sd["mean"],
            )
        )
        out.append(
            "| control   | {n} | {mn:+.2f} | {p25:+.2f} | {med:+.2f} | {p75:+.2f} | "
            "{mx:+.2f} | {mean:+.2f} |".format(
                n=cd["n"], mn=cd["min"], p25=cd["p25"], med=cd["median"],
                p75=cd["p75"], mx=cd["max"], mean=cd["mean"],
            )
        )
        out.append("")

        out.append("### Statistical comparison (per-surface medians, unit of obs.)\n")
        out.append(
            f"- **Median difference (substrate − control):** "
            f"{comp['median_difference']:+.4f}\n"
            f"- **Mann-Whitney U (substrate vs control):** {comp['mann_whitney_U']:.1f} "
            f"(z = {comp['mann_whitney_z']:+.3f})\n"
            f"- **Two-tail p-value (normal approx., continuity-corrected):** "
            f"{comp['mann_whitney_p_two_tail']:.4f}\n"
            f"- **Cliff's δ (substrate vs control):** {comp['cliffs_delta']:+.4f}\n"
            f"- **Top-control rank in interleaved leaderboard:** "
            f"#{comp['top_control_rank_in_interleaved']}\n"
            f"- **Substrate top-20 median (cutoff):** "
            f"{comp['substrate_top_20_median_min']:+.4f}\n"
        )
        out.append("")

        out.append(f"### Interleaved leaderboard (top {top_per_pool})\n")
        out.append(
            "| rank | kind | pool | surface | n | median_pmcd | mean_pmcd | "
            "best_pmcd | best_inscription | geo_mean |"
        )
        out.append("|---:|---|---|---|---:|---:|---:|---:|---|---:|")
        for i, row in enumerate(comp["interleaved"][:top_per_pool], 1):
            out.append(
                "| {i} | {kind} | {p} | `{s}` | {n} | {med:+.4f} | {mean:+.4f} | "
                "{best:+.4f} | {ins} | {gg:+.4f} |".format(
                    i=i, kind=row["kind"], p=row["pool"], s=row["surface"],
                    n=row["n"], med=row["median_pmcd"], mean=row["mean_pmcd"],
                    best=row["best_pmcd"], ins=row["best_inscription"],
                    gg=row["geo_mean"],
                )
            )
        out.append("")

        # All-control rows under top_per_pool — list them so the file is
        # self-contained for a reader checking "where do controls land".
        ctrl_rows = [
            (i, r)
            for i, r in enumerate(comp["interleaved"], 1)
            if r["kind"] == "control"
        ]
        out.append(
            f"### All control surfaces in interleaved order "
            f"(n={len(ctrl_rows)}, top 20 shown)\n"
        )
        out.append(
            "| rank | pool | surface | n | median_pmcd | best_pmcd | best_inscription |"
        )
        out.append("|---:|---|---|---:|---:|---:|---|")
        for rank_i, row in ctrl_rows[:20]:
            out.append(
                "| {i} | {p} | `{s}` | {n} | {med:+.4f} | {best:+.4f} | {ins} |".format(
                    i=rank_i, p=row["pool"], s=row["surface"], n=row["n"],
                    med=row["median_pmcd"], best=row["best_pmcd"],
                    ins=row["best_inscription"],
                )
            )
        out.append("")

    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--write", type=Path, default=_DEFAULT_OUT)
    parser.add_argument("--top-per-pool", type=int, default=30)
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path to write a JSON summary of the comparison stats.",
    )
    args = parser.parse_args(argv)

    rows = load_rows(args.results)
    comparisons = [
        compare_pair(rows, sub, ctrl) for sub, ctrl in _PAIRS
    ]

    text = render_markdown(comparisons, top_per_pool=args.top_per_pool)
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(text, encoding="utf-8")
    print(f"wrote {args.write}", file=sys.stderr)

    summary = []
    for comp in comparisons:
        c = {k: v for k, v in comp.items() if k != "interleaved"}
        summary.append(c)
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
