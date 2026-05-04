#!/usr/bin/env python3
"""Paired-difference rollup for candidate_signature.v1 (mg-bef2, harness v9).

For each substrate signature, the paired control signature is the entry
in the matched ``control_<pool>`` manifest whose ``paired_substrate_hash``
points back to the substrate's hypothesis_hash. This pairing is exact
by construction (both pin the same window with the same per-root
span_within_window placements; only surfaces, phonemes, and the
resulting sign->phoneme mapping change).

Per-window paired_diff = substrate_score − matched_control_score.

Aggregation
===========
Per-(substrate_pool, sorted root-surface tuple) median paired_diff. The
"surface-set" is the multiset of root surfaces in the signature; the
aggregation key is the sorted tuple of those surfaces (so the same set
of roots produces the same key regardless of placement order). One row
per (pool, surface-set) — independent of the inscription the signature
was placed on.

Acceptance gate (mg-bef2)
=========================
For at least one substrate pool, the per-surface-set medians must
satisfy:
  * Wilcoxon signed-rank one-tail p < 0.05 (alternative: median > 0)
  * mean per-surface-set median > 0

Both conditions must hold; the sign-test is reported as a robustness
check.

Output
======
  results/rollup.paired_diff.signature.<pool>.md  (per pool)
  results/rollup.paired_diff.signature.md         (combined)

Re-runs are deterministic given the result stream and the manifests.

Usage
=====
  python3 scripts/paired_diff_signature_rollup.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS_DIR = _REPO_ROOT / "results"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"

_METRIC = "external_phoneme_perplexity_v0"


_SUBSTRATE_POOLS = ("aquitanian", "etruscan", "toponym")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def _load_manifest(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _load_score_rows(results_dir: Path) -> dict[str, dict]:
    """Hash -> latest-by-ran_at result row for the metric.

    Reads the primary stream + the per-metric sidecar.
    """
    out: dict[str, dict] = {}
    paths = [
        results_dir / "experiments.jsonl",
        results_dir / f"experiments.{_METRIC}.jsonl",
    ]
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
                if not h:
                    continue
                cur = out.get(h)
                if cur is None or row.get("ran_at", "") > cur.get("ran_at", ""):
                    out[h] = row
    return out


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def wilcoxon_signed_rank_one_tail(diffs: list[float]) -> tuple[float, float, int]:
    nonzero = [d for d in diffs if d != 0.0]
    n = len(nonzero)
    if n == 0:
        return 0.0, float("nan"), 0
    abs_vals = sorted(((abs(d), 1 if d > 0 else -1) for d in nonzero), key=lambda t: t[0])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs_vals[j + 1][0] == abs_vals[i][0]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    w_plus = sum(r for r, (_v, s) in zip(ranks, abs_vals) if s > 0)
    mu = n * (n + 1) / 4.0
    var = n * (n + 1) * (2 * n + 1) / 24.0
    if var <= 0:
        return w_plus, float("nan"), n
    z = (w_plus - mu - 0.5) / math.sqrt(var)
    p_one = 1.0 - _normal_cdf(z)
    return w_plus, p_one, n


def sign_test_one_tail(diffs: list[float]) -> tuple[int, int, float]:
    n_pos = sum(1 for d in diffs if d > 0)
    n_neg = sum(1 for d in diffs if d < 0)
    n = n_pos + n_neg
    if n == 0:
        return 0, 0, float("nan")
    p = 0.0
    for k in range(n_pos, n + 1):
        p += math.comb(n, k) * (0.5 ** n)
    return n_pos, n, p


def median(values: list[float]) -> float:
    if not values:
        return float("nan")
    sv = sorted(values)
    n = len(sv)
    if n % 2 == 1:
        return sv[n // 2]
    return 0.5 * (sv[n // 2 - 1] + sv[n // 2])


# ---------------------------------------------------------------------------
# Pairing + aggregation
# ---------------------------------------------------------------------------


def build_paired_diffs(
    *,
    substrate_pool: str,
    auto_dir: Path,
    score_rows: dict[str, dict],
) -> list[dict]:
    """One paired_diff record per substrate signature with a matched
    control. Each record carries:
      * pool, inscription_id, window_start, window_end
      * surface_set (sorted tuple of root surfaces, substrate side)
      * substrate_score, control_score, paired_diff
      * substrate_hash, control_hash
    """
    sub_manifest_path = auto_dir / f"{substrate_pool}.manifest.jsonl"
    ctrl_manifest_path = auto_dir / f"control_{substrate_pool}.manifest.jsonl"
    if not sub_manifest_path.exists() or not ctrl_manifest_path.exists():
        return []

    sub_rows = _load_manifest(sub_manifest_path)
    ctrl_rows = _load_manifest(ctrl_manifest_path)

    # Index control rows by paired_substrate_hash.
    ctrl_by_paired: dict[str, dict] = {}
    for row in ctrl_rows:
        ctrl_by_paired[row["paired_substrate_hash"]] = row

    out: list[dict] = []
    for sub_row in sub_rows:
        sub_hash = sub_row["hypothesis_hash"]
        ctrl_row = ctrl_by_paired.get(sub_hash)
        if ctrl_row is None:
            continue
        sub_score_row = score_rows.get(sub_hash)
        ctrl_score_row = score_rows.get(ctrl_row["hypothesis_hash"])
        if sub_score_row is None or ctrl_score_row is None:
            continue
        sub_score = float(sub_score_row.get("score", 0.0))
        ctrl_score = float(ctrl_score_row.get("score", 0.0))
        out.append(
            {
                "pool": substrate_pool,
                "inscription_id": sub_row["inscription_id"],
                "window_start": int(sub_row["window_start"]),
                "window_end": int(sub_row["window_end"]),
                "n_roots": int(sub_row["n_roots"]),
                "surface_set": tuple(sub_row["root_surfaces"]),
                "substrate_score": sub_score,
                "control_score": ctrl_score,
                "paired_diff": sub_score - ctrl_score,
                "substrate_hash": sub_hash,
                "control_hash": ctrl_row["hypothesis_hash"],
                "n_window_syllabograms": int(sub_row["n_window_syllabograms"]),
                "n_covered_syllabograms": int(sub_row["n_covered_syllabograms"]),
                "coverage_fraction": float(sub_row["coverage_fraction"]),
            }
        )
    return out


def aggregate_per_surface_set(records: list[dict]) -> list[dict]:
    by_key: dict[tuple[str, tuple[str, ...]], list[float]] = defaultdict(list)
    for rec in records:
        by_key[(rec["pool"], rec["surface_set"])].append(rec["paired_diff"])
    out: list[dict] = []
    for (pool, surface_set), diffs in sorted(by_key.items()):
        out.append(
            {
                "pool": pool,
                "surface_set": list(surface_set),
                "surface_set_str": "+".join(surface_set),
                "n": len(diffs),
                "median_paired_diff": median(diffs),
                "mean_paired_diff": sum(diffs) / len(diffs),
                "min_paired_diff": min(diffs),
                "max_paired_diff": max(diffs),
                "frac_positive": sum(1 for d in diffs if d > 0) / len(diffs),
            }
        )
    return out


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def render_pool_md(
    *,
    pool: str,
    records: list[dict],
    aggregates: list[dict],
    top_per_pool: int = 50,
) -> tuple[str, dict]:
    out: list[str] = []
    out.append(f"# Paired-difference leaderboard — multi-root signatures, pool={pool}\n")
    out.append(
        f"Generated by `scripts/paired_diff_signature_rollup.py` (mg-bef2). "
        f"Metric: `{_METRIC}`. Aggregation: per-surface-set median over "
        f"per-window paired_diff (substrate_score − matched_control_score).\n"
    )
    out.append(
        "**Acceptance gate (mg-bef2):** `Wilcoxon p < 0.05` AND "
        "`mean per-surface-set median > 0`. Sign test reported alongside "
        "as a distribution-free robustness check.\n"
    )

    pool_records = [r for r in records if r["pool"] == pool]
    pool_aggs = [a for a in aggregates if a["pool"] == pool]

    out.append("## Pool acceptance gate\n")
    if pool_aggs:
        meds = [a["median_paired_diff"] for a in pool_aggs]
        wp_w, wp_p, wp_n = wilcoxon_signed_rank_one_tail(meds)
        sn_pos, sn_n, sn_p = sign_test_one_tail(meds)
        med_of_meds = median(meds)
        mean_of_meds = sum(meds) / len(meds)
        frac_pos = sum(1 for v in meds if v > 0) / len(meds)
        out.append(
            "| substrate pool | n_surface_sets | n_paired_records | "
            "median(median paired_diff) | mean(median paired_diff) | "
            "frac surface-sets > 0 | Wilcoxon W+ | Wilcoxon p (one-tail) | "
            "sign-test n+/n | sign-test p (one-tail) | gate |"
        )
        out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        gate = (wp_p < 0.05 if not math.isnan(wp_p) else False) and mean_of_meds > 0
        out.append(
            "| {pool} | {nss} | {nr} | {med:+.4f} | {mean:+.4f} | {fp:.3f} | "
            "{w:.1f} | {wp:.4f} | {snp}/{snn} | {sp:.4f} | {gate} |".format(
                pool=pool,
                nss=len(meds),
                nr=len(pool_records),
                med=med_of_meds,
                mean=mean_of_meds,
                fp=frac_pos,
                w=wp_w,
                wp=wp_p,
                snp=sn_pos,
                snn=sn_n,
                sp=sn_p,
                gate="PASS" if gate else "FAIL",
            )
        )
        summary = {
            "pool": pool,
            "n_surface_sets": len(meds),
            "n_paired_records": len(pool_records),
            "median_of_medians": med_of_meds,
            "mean_of_medians": mean_of_meds,
            "frac_surface_sets_positive": frac_pos,
            "wilcoxon_W_plus": wp_w,
            "wilcoxon_p_one_tail": wp_p,
            "wilcoxon_n_nonzero": wp_n,
            "sign_test_n_pos": sn_pos,
            "sign_test_n_total": sn_n,
            "sign_test_p_one_tail": sn_p,
            "acceptance_gate": "PASS" if gate else "FAIL",
        }
    else:
        summary = {"pool": pool, "n_surface_sets": 0, "n_paired_records": 0}
        out.append("(no aggregates)")
    out.append("")

    # Top surface-sets.
    ranked = sorted(pool_aggs, key=lambda a: -a["median_paired_diff"])[:top_per_pool]
    out.append(f"## {pool} — top {len(ranked)} surface-sets by median paired_diff\n")
    out.append(
        "| rank | surface set | n | median paired_diff | mean | min | max | frac > 0 |"
    )
    out.append("|---:|---|---:|---:|---:|---:|---:|---:|")
    for i, a in enumerate(ranked, 1):
        out.append(
            "| {i} | `{ss}` | {n} | {med:+.4f} | {mean:+.4f} | {mn:+.4f} | "
            "{mx:+.4f} | {fp:.3f} |".format(
                i=i,
                ss=a["surface_set_str"],
                n=a["n"],
                med=a["median_paired_diff"],
                mean=a["mean_paired_diff"],
                mn=a["min_paired_diff"],
                mx=a["max_paired_diff"],
                fp=a["frac_positive"],
            )
        )
    out.append("")

    # Top per-window signatures.
    by_diff = sorted(pool_records, key=lambda r: -r["paired_diff"])[:25]
    out.append(f"## {pool} — top {len(by_diff)} per-window signatures by paired_diff\n")
    out.append(
        "| rank | inscription | window | surface set | n_roots | "
        "substrate score | control score | paired_diff | coverage |"
    )
    out.append("|---:|---|---|---|---:|---:|---:|---:|---:|")
    for i, r in enumerate(by_diff, 1):
        out.append(
            "| {i} | `{ins}` | [{ws}..{we}] | `{ss}` | {nr} | {ss_:+.4f} | "
            "{cs:+.4f} | {pd:+.4f} | {cov}/{nws} |".format(
                i=i,
                ins=r["inscription_id"],
                ws=r["window_start"],
                we=r["window_end"],
                ss="+".join(r["surface_set"]),
                nr=r["n_roots"],
                ss_=r["substrate_score"],
                cs=r["control_score"],
                pd=r["paired_diff"],
                cov=r["n_covered_syllabograms"],
                nws=r["n_window_syllabograms"],
            )
        )
    out.append("")

    return "\n".join(out) + "\n", summary


def render_combined_md(
    *,
    records: list[dict],
    aggregates: list[dict],
    pool_summaries: list[dict],
) -> str:
    out: list[str] = []
    out.append("# Multi-root signature paired-difference leaderboard (mg-bef2)\n")
    out.append(
        f"Generated by `scripts/paired_diff_signature_rollup.py`. Metric: "
        f"`{_METRIC}`. One signature pairs to one matched control by "
        f"`paired_substrate_hash`; per-window paired_diff = "
        f"`substrate_score − control_score`. Aggregation key: sorted "
        f"tuple of root surfaces (the multi-root analogue of v8's "
        f"per-surface aggregation).\n"
    )
    out.append("## Per-pool acceptance gate\n")
    out.append(
        "| pool | n_surface_sets | n_paired_records | "
        "median(median paired_diff) | mean(median paired_diff) | "
        "frac surface-sets > 0 | Wilcoxon p (one-tail) | "
        "sign-test n+/n | sign-test p | acceptance gate |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for s in pool_summaries:
        if "median_of_medians" not in s:
            continue
        out.append(
            "| {pool} | {nss} | {nr} | {med:+.4f} | {mean:+.4f} | {fp:.3f} | "
            "{wp:.4f} | {snp}/{snn} | {sp:.4f} | {gate} |".format(
                pool=s["pool"],
                nss=s["n_surface_sets"],
                nr=s["n_paired_records"],
                med=s["median_of_medians"],
                mean=s["mean_of_medians"],
                fp=s["frac_surface_sets_positive"],
                wp=s["wilcoxon_p_one_tail"],
                snp=s["sign_test_n_pos"],
                snn=s["sign_test_n_total"],
                sp=s["sign_test_p_one_tail"],
                gate=s["acceptance_gate"],
            )
        )
    out.append("")

    # Top-20 substrate signatures across pools.
    by_diff = sorted(records, key=lambda r: -r["paired_diff"])[:20]
    out.append("## Top-20 per-window signatures across pools by paired_diff\n")
    out.append(
        "| rank | pool | inscription | window | surface set | n_roots | "
        "substrate | control | paired_diff |"
    )
    out.append("|---:|---|---|---|---|---:|---:|---:|---:|")
    for i, r in enumerate(by_diff, 1):
        out.append(
            "| {i} | {pool} | `{ins}` | [{ws}..{we}] | `{ss}` | {nr} | "
            "{ss_:+.4f} | {cs:+.4f} | {pd:+.4f} |".format(
                i=i,
                pool=r["pool"],
                ins=r["inscription_id"],
                ws=r["window_start"],
                we=r["window_end"],
                ss="+".join(r["surface_set"]),
                nr=r["n_roots"],
                ss_=r["substrate_score"],
                cs=r["control_score"],
                pd=r["paired_diff"],
            )
        )
    out.append("")

    out.append("## Notes\n")
    out.append(
        f"- Records: substrate signatures with a matched control: "
        f"**{len(records)}** total across pools.\n"
        f"- Aggregation: per-(pool, sorted root-surface tuple) median over "
        f"the per-window paired_diff. Surface-sets that appear at multiple "
        f"windows contribute multiple paired_diff entries; the median over "
        f"those is the surface-set's row in the per-pool table.\n"
        f"- Acceptance gate (mg-bef2): for at least one pool, Wilcoxon "
        f"signed-rank one-tail p < 0.05 on per-surface-set medians AND "
        f"mean per-surface-set median > 0.\n"
    )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument(
        "--pools",
        type=str,
        default=",".join(_SUBSTRATE_POOLS),
        help="Comma-separated list of substrate pools to roll up.",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path for a JSON sidecar holding the per-pool summary.",
    )
    parser.add_argument("--top-per-pool", type=int, default=50)
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    score_rows = _load_score_rows(args.results_dir)

    all_records: list[dict] = []
    for pool in pools:
        recs = build_paired_diffs(
            substrate_pool=pool,
            auto_dir=args.auto_dir,
            score_rows=score_rows,
        )
        all_records.extend(recs)
    aggregates = aggregate_per_surface_set(all_records)

    pool_summaries: list[dict] = []
    for pool in pools:
        text, summary = render_pool_md(
            pool=pool,
            records=all_records,
            aggregates=aggregates,
            top_per_pool=args.top_per_pool,
        )
        out_path = (
            args.results_dir / f"rollup.paired_diff.signature.{pool}.md"
        )
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path}", file=sys.stderr)
        pool_summaries.append(summary)

    combined = render_combined_md(
        records=all_records, aggregates=aggregates, pool_summaries=pool_summaries
    )
    combined_path = args.results_dir / "rollup.paired_diff.signature.md"
    combined_path.write_text(combined, encoding="utf-8")
    print(f"wrote {combined_path}", file=sys.stderr)

    if args.summary_json:
        args.summary_json.write_text(
            json.dumps(pool_summaries, indent=2), encoding="utf-8"
        )
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(pool_summaries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
