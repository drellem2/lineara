#!/usr/bin/env python3
"""Compute Mann-Whitney U + Cliff's delta + power-calculation report
for the curated-v4 buckets, under each of the three v3 metrics. Renders
``results/statistics_v4.md`` as a markdown report.

Inputs:
- ``hypotheses/curated/CONSTRUCTION.manifest.jsonl`` (100 entries x bucket tags)
- ``results/experiments.jsonl`` (the mg-7c8c v4 sweep + prior mg-fb23/mg-7dd1/mg-23cc rows)

Outputs:
- ``results/statistics_v4.md`` (committed; tables + power calc + bottom-line)

The statistics implementation is intentionally self-contained — no scipy
dependency. Mann-Whitney U follows Hollander, Wolfe & Chicken (3rd ed.)
§4.2; Cliff's δ follows Cliff 1993; the normal-approximation p-value is
computed with a continuity correction; Wilcoxon rank-sum equivalence
(Mann-Whitney U with mid-rank ties) yields the same statistic. The
power calculation uses the standard normal-approximation formula:

    n* = 2 (z_{1-α/2} + z_{1-β})^2 σ^2 / Δ^2

with α = 0.05, β = 0.20, σ = pooled within-group SD, Δ = observed
between-group difference of medians (signed). Inverting gives the
detectable Δ at n=20:

    Δ_min = (z_{1-α/2} + z_{1-β}) σ √(2/n)
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_MANIFEST = (
    _REPO_ROOT / "hypotheses" / "curated" / "CONSTRUCTION.manifest.jsonl"
)
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_DEFAULT_OUT = _REPO_ROOT / "results" / "statistics_v4.md"


_METRICS = (
    "local_fit_v1",
    "partial_mapping_compression_delta_v0",
    "geographic_genre_fit_v1",
)
_METRIC_LABEL = {
    "local_fit_v1": "local_fit_v1",
    "partial_mapping_compression_delta_v0": "partial_mapping_compression_delta_v0",
    "geographic_genre_fit_v1": "geographic_genre_fit_v1",
}


def _load_manifest(path: Path) -> dict[str, dict]:
    by_hash: dict[str, dict] = {}
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            by_hash[row["hypothesis_hash"]] = row
    return by_hash


def _load_results(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _scores_by_bucket_metric(
    manifest_by_hash: dict[str, dict], rows: list[dict]
) -> dict[str, dict[str, list[float]]]:
    """Returns {metric: {bucket: [score, ...]}}, taking the most-recent row
    for each (hypothesis_hash, metric) so re-runs on the same snapshot are
    idempotent."""
    # Pick the row with the highest ran_at per (hash, metric).
    latest: dict[tuple[str, str], dict] = {}
    for r in rows:
        h = r.get("hypothesis_hash")
        m = r.get("metric")
        if h not in manifest_by_hash:
            continue
        if m not in _METRICS:
            continue
        key = (h, m)
        prev = latest.get(key)
        if prev is None or r.get("ran_at", "") > prev.get("ran_at", ""):
            latest[key] = r
    out: dict[str, dict[str, list[float]]] = {m: {} for m in _METRICS}
    for (h, m), r in latest.items():
        bucket = manifest_by_hash[h]["bucket"]
        out[m].setdefault(bucket, []).append(float(r["score"]))
    return out


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
#
# Mann-Whitney U (two-sided), with mid-rank ties and normal-approximation
# p-value (continuity correction). Self-contained — no scipy dependency.


def _ranks_with_ties(values: list[float]) -> list[float]:
    """Mid-rank assignments, 1-indexed."""
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    n = len(indexed)
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        midrank = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = midrank
        i = j + 1
    return ranks


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _mann_whitney(a: list[float], b: list[float]) -> dict:
    """Two-sided Mann-Whitney U with mid-rank ties; returns U_a, U_b, p
    (normal-approximation with continuity correction), z, n_a, n_b. Cliff's
    delta is reported alongside as a non-parametric effect size."""
    n_a, n_b = len(a), len(b)
    if n_a == 0 or n_b == 0:
        return {
            "U_a": float("nan"),
            "U_b": float("nan"),
            "p": float("nan"),
            "z": float("nan"),
            "n_a": n_a,
            "n_b": n_b,
            "cliffs_delta": float("nan"),
        }
    combined = a + b
    ranks = _ranks_with_ties(combined)
    rank_a = sum(ranks[:n_a])
    U_a = rank_a - n_a * (n_a + 1) / 2.0
    U_b = n_a * n_b - U_a

    # Normal approximation with mid-rank tie correction.
    mu = n_a * n_b / 2.0
    # Tie-correction term:
    tie_correction = 0.0
    counts: dict[float, int] = {}
    for v in combined:
        counts[v] = counts.get(v, 0) + 1
    n = n_a + n_b
    for c in counts.values():
        if c > 1:
            tie_correction += (c**3 - c) / (n * (n - 1))
    sigma_sq = n_a * n_b / 12.0 * ((n + 1) - tie_correction)
    sigma = math.sqrt(sigma_sq) if sigma_sq > 0 else 0.0
    if sigma == 0:
        z = 0.0
        p = 1.0
    else:
        # Continuity correction.
        diff = U_a - mu
        if diff > 0:
            diff -= 0.5
        elif diff < 0:
            diff += 0.5
        z = diff / sigma
        p = 2.0 * (1.0 - _normal_cdf(abs(z)))

    # Cliff's δ = (#(a > b) - #(a < b)) / (n_a * n_b)
    gt = lt = 0
    for x in a:
        for y in b:
            if x > y:
                gt += 1
            elif x < y:
                lt += 1
    cliffs_delta = (gt - lt) / (n_a * n_b)

    return {
        "U_a": float(U_a),
        "U_b": float(U_b),
        "p": float(p),
        "z": float(z),
        "n_a": n_a,
        "n_b": n_b,
        "cliffs_delta": float(cliffs_delta),
    }


# Inverse normal for two specific z values used in the power calc.
# z_{0.975} = 1.95996 (α/2 = 0.025); z_{0.80} = 0.84162 (β = 0.20).
_Z_ALPHA_2 = 1.95996398454005
_Z_BETA = 0.8416212335729143


def _detectable_delta(
    a: list[float], b: list[float], alpha: float = 0.05, beta: float = 0.20
) -> dict:
    """Two-sample two-sided power calculation (normal approximation).

    Returns the minimum effect size (Δ) detectable at the observed n_a, n_b
    and pooled within-group SD, given α and 1-β. Also reports the observed
    Δ (mean_a − mean_b and median_a − median_b).
    """
    n_a, n_b = len(a), len(b)
    if n_a < 2 or n_b < 2:
        return {
            "n_a": n_a,
            "n_b": n_b,
            "pooled_sd": float("nan"),
            "delta_means": float("nan"),
            "delta_medians": float("nan"),
            "detectable_delta": float("nan"),
            "is_underpowered_for_observed": True,
        }
    sd_a = statistics.pstdev(a) if n_a > 1 else 0.0
    sd_b = statistics.pstdev(b) if n_b > 1 else 0.0
    pooled_var = ((n_a - 1) * sd_a**2 + (n_b - 1) * sd_b**2) / (n_a + n_b - 2)
    pooled_sd = math.sqrt(pooled_var)
    delta_means = statistics.mean(a) - statistics.mean(b)
    delta_medians = statistics.median(a) - statistics.median(b)
    if pooled_sd == 0:
        detectable = 0.0
    else:
        detectable = (
            (_Z_ALPHA_2 + _Z_BETA)
            * pooled_sd
            * math.sqrt(1.0 / n_a + 1.0 / n_b)
        )
    return {
        "n_a": n_a,
        "n_b": n_b,
        "pooled_sd": pooled_sd,
        "delta_means": delta_means,
        "delta_medians": delta_medians,
        "detectable_delta": detectable,
        # Bool: is the observed effect *smaller* than what we could detect?
        "is_underpowered_for_observed": abs(delta_means) < detectable,
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def _bucket_summary(values: list[float]) -> str:
    if not values:
        return "n=0"
    n = len(values)
    return (
        f"n={n} median={statistics.median(values):+.4f} "
        f"mean={statistics.mean(values):+.4f} "
        f"sd={statistics.pstdev(values):.4f}"
    )


def _u_test_table(
    by_metric_bucket: dict[str, dict[str, list[float]]],
    *,
    label_a: str,
    bucket_a: str,
    label_b: str,
    bucket_b: str,
) -> list[str]:
    lines = [
        f"### {label_a} (bucket={bucket_a}) vs {label_b} (bucket={bucket_b})",
        "",
        "| metric | n_a | n_b | median_a | median_b | Δ_medians | Mann-Whitney U_a | z | p | Cliff's δ | detectable Δ (n=20, α=.05, β=.2) | underpowered? |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for metric in _METRICS:
        a = by_metric_bucket[metric].get(bucket_a, [])
        b = by_metric_bucket[metric].get(bucket_b, [])
        if not a or not b:
            lines.append(
                f"| `{metric}` | {len(a)} | {len(b)} | (no data) | (no data) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"
            )
            continue
        u = _mann_whitney(a, b)
        d = _detectable_delta(a, b)
        med_a = statistics.median(a)
        med_b = statistics.median(b)
        lines.append(
            f"| `{metric}` | {len(a)} | {len(b)} | "
            f"{med_a:+.4f} | {med_b:+.4f} | {med_a - med_b:+.4f} | "
            f"{u['U_a']:.1f} | {u['z']:+.3f} | {u['p']:.4f} | "
            f"{u['cliffs_delta']:+.3f} | {d['detectable_delta']:.4f} | "
            f"{'yes' if d['is_underpowered_for_observed'] else 'no'} |"
        )
    lines.append("")
    return lines


def _bucket_distributions_table(
    by_metric_bucket: dict[str, dict[str, list[float]]],
) -> list[str]:
    lines = ["### Bucket distributions (raw)", ""]
    for metric in _METRICS:
        lines.append(f"#### `{metric}`")
        lines.append("")
        lines.append("| bucket | n | median | mean | sd | min | max |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for bucket in (
            "A_linear_b_anchor",
            "B_aquit_plausible",
            "C_aquit_wrong",
            "D_toponym_plausible",
            "E_scramble",
        ):
            v = by_metric_bucket[metric].get(bucket, [])
            if not v:
                lines.append(f"| `{bucket}` | 0 | n/a | n/a | n/a | n/a | n/a |")
                continue
            lines.append(
                f"| `{bucket}` | {len(v)} | {statistics.median(v):+.4f} | "
                f"{statistics.mean(v):+.4f} | "
                f"{statistics.pstdev(v):.4f} | "
                f"{min(v):+.4f} | {max(v):+.4f} |"
            )
        lines.append("")
    return lines


def _build_report(
    by_metric_bucket: dict[str, dict[str, list[float]]],
    manifest_count: int,
    seed_note: str,
) -> str:
    lines: list[str] = []
    lines.append("# mg-7c8c statistics: curated v4 (n=20 per bucket)")
    lines.append("")
    lines.append(
        f"Mann-Whitney U + Cliff's δ + power-calculation report on the "
        f"100-row curated set defined by "
        f"`hypotheses/curated/CONSTRUCTION.manifest.jsonl` "
        f"({manifest_count} entries) under three v3 metrics. {seed_note}"
    )
    lines.append("")
    lines.append("## Headline acceptance gate")
    lines.append("")
    lines.append(
        "**Plausible Aquitanian (B; n=20) vs deliberately-wrong Aquitanian "
        "(C; n=20)** under the v3 metrics. The mg-fb23 / mg-7dd1 / mg-23cc "
        "n=4 buckets all missed this gate (identical medians, +0.14 v1-units, "
        "and -20 bits respectively); this is the same test re-run at n=20."
    )
    lines.append("")
    lines.extend(
        _u_test_table(
            by_metric_bucket,
            label_a="plausible Aquitanian",
            bucket_a="B_aquit_plausible",
            label_b="deliberately-wrong Aquitanian",
            bucket_b="C_aquit_wrong",
        )
    )
    lines.append("## Anchor vs scramble (sanity check)")
    lines.append("")
    lines.append(
        "**Linear-B anchor (A; n=20) vs random scramble (E; n=20)**. "
        "mg-fb23's gate (anchor median > scramble median) cleared at n=4; "
        "verifying it holds at n=20 is reassurance that the metrics still "
        "separate something well-grounded from random."
    )
    lines.append("")
    lines.extend(
        _u_test_table(
            by_metric_bucket,
            label_a="Linear-B carryover anchor",
            bucket_a="A_linear_b_anchor",
            label_b="random scramble",
            bucket_b="E_scramble",
        )
    )
    lines.append("## Toponym (third pool) vs scramble")
    lines.append("")
    lines.append(
        "**Pre-Greek toponym (D; n=20) vs random scramble (E; n=20)**. "
        "Tests whether the toponym pool's third-pool axis carries any "
        "discriminative signal at all (independent of any plausible-vs-wrong "
        "claim)."
    )
    lines.append("")
    lines.extend(
        _u_test_table(
            by_metric_bucket,
            label_a="pre-Greek toponym",
            bucket_a="D_toponym_plausible",
            label_b="random scramble",
            bucket_b="E_scramble",
        )
    )
    lines.append("## Plausible Aquitanian vs anchor (control sanity)")
    lines.append("")
    lines.append(
        "**Plausible Aquitanian (B; n=20) vs Linear-B anchor (A; n=20)**. "
        "Both buckets are 'plausible'; metrics should NOT separate them "
        "strongly. A large effect here would suggest a confound."
    )
    lines.append("")
    lines.extend(
        _u_test_table(
            by_metric_bucket,
            label_a="plausible Aquitanian",
            bucket_a="B_aquit_plausible",
            label_b="Linear-B anchor",
            bucket_b="A_linear_b_anchor",
        )
    )
    lines.extend(_bucket_distributions_table(by_metric_bucket))
    lines.append("## Methodology notes")
    lines.append("")
    lines.append(
        "- **Mann-Whitney U.** Two-sided, with mid-rank tie correction. "
        "p-value via normal approximation with continuity correction "
        "(Hollander, Wolfe & Chicken §4.2). Self-contained implementation "
        "in `scripts/curated_v4_stats.py`; no scipy."
    )
    lines.append(
        "- **Cliff's δ.** `(#(a>b) − #(a<b)) / (n_a × n_b)`. Range "
        "[-1, +1]; +1 = every value in *a* exceeds every value in *b*; "
        "-1 = the reverse; 0 = stochastic equivalence. |δ| ≥ 0.474 is "
        "'large' (Cliff 1993)."
    )
    lines.append(
        "- **Power calculation.** Two-sample two-sided z-test "
        "approximation: detectable Δ at α=0.05, 1-β=0.80 is "
        "`(z_{1-α/2} + z_{1-β}) × pooled_sd × √(1/n_a + 1/n_b)`. "
        "If observed |Δ_means| < detectable Δ, the comparison is "
        "underpowered for the observed effect even at n=20."
    )
    lines.append(
        "- **Bucket C heterogeneity.** The 4 mg-fb23 wrong-Aquitanian "
        "entries embed a phonotactic-position-mismatch rule; the 16 v4 "
        "entries embed a genre-context-mismatch rule. Mann-Whitney U is "
        "rank-based, so this mixed bucket is fine for testing the central "
        "question (does the metric rank plausible above wrong, period?)."
    )
    lines.append(
        "- **Score sources.** Most-recent row per `(hypothesis_hash, "
        "metric)` from `results/experiments.jsonl` (in case of duplicate "
        "rows from re-runs). Curation is deterministic and corpus-stable, "
        "so under normal conditions there is exactly one row per "
        "(hash, metric) on the current snapshot."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, default=_DEFAULT_MANIFEST)
    parser.add_argument("--results", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = parser.parse_args(argv)

    manifest_by_hash = _load_manifest(args.manifest)
    rows = _load_results(args.results)
    by_metric_bucket = _scores_by_bucket_metric(manifest_by_hash, rows)

    # Validate every bucket has 20 entries per metric.
    bucket_order = (
        "A_linear_b_anchor",
        "B_aquit_plausible",
        "C_aquit_wrong",
        "D_toponym_plausible",
        "E_scramble",
    )
    for metric in _METRICS:
        for bucket in bucket_order:
            n = len(by_metric_bucket[metric].get(bucket, []))
            if n != 20:
                print(
                    f"WARNING: metric {metric} bucket {bucket} has n={n} (expected 20)",
                    file=sys.stderr,
                )

    seed_note = (
        "Power-calc constants: α=0.05, β=0.20. Scramble bucket RNG "
        "seed=4242 (curated v4); mg-fb23 scrambles used seed=42."
    )
    report = _build_report(by_metric_bucket, len(manifest_by_hash), seed_note)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
