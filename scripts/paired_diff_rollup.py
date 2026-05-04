#!/usr/bin/env python3
"""Paired-difference rollup (mg-ddee, harness v7).

For each substrate candidate, locate the matched control candidate and
compute ``paired_diff = substrate_score − matched_control_score``. The
matching is rollup-time, so the raw result stream stays append-only and
matching policy can evolve without re-scoring.

Match rule
==========

For substrate candidate (pool=P, surface=S, inscription=I, span=[s,e],
phonemes=[...]):

  1. Pick controls in pool ``control_<P>`` whose manifest row matches
     ``(inscription, span_start, span_end)`` exactly.
  2. Among those, pick the one whose pool-entry phoneme sequence has the
     minimum *edit distance* to the substrate's phoneme sequence. Ties
     are broken by sorted hypothesis_hash for stable output.
  3. If no control candidate exists at the same (inscription, span),
     paired_diff is null and the row is dropped from the per-surface
     aggregation.

The matching is over the full sweep result for the chosen metric. A row
with no ran_at-latest score under the metric is skipped.

Acceptance gate
===============

The rollup also emits a per-pool summary block reporting:

  * count of (pool, surface) groups with at least 1 paired_diff entry;
  * each (pool, surface) group's median paired_diff;
  * one-tail Wilcoxon signed-rank test on the per-surface medians
    against zero (alternative: median > 0; substrate beats control);
  * one-tail sign test as a non-parametric robustness check.

The ticket calls for "Mann-Whitney U", but the unit of observation here
is the per-surface paired-diff median (a single number per surface), so
the right test is one-tail Wilcoxon signed-rank against zero
(signed-rank handles paired data; the surface medians are themselves
paired-difference statistics). The sign test is reported alongside as a
distribution-free robustness check.

Output
======

  * ``results/rollup.paired_diff.<metric>.md`` — markdown leaderboard
    with per-pool median paired-diff tables and the acceptance-gate
    statistics.

Re-runs are deterministic given the result stream and the manifests.

Usage
=====

  python3 scripts/paired_diff_rollup.py --metric sign_prediction_perplexity_v0
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import yaml


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_POOLS = _REPO_ROOT / "pools"

# Per-metric sidecar streams. Some metrics emit so many rows that piling
# them into the primary stream would push the committed file over
# GitHub's 100 MB push limit. mg-ddee's sign_prediction_perplexity_v0 is
# the first such metric — its 32,172 rows live under
# results/experiments.<metric>.jsonl as a sidecar. The rollup transparently
# reads both files for the requested metric, oldest first.
_SIDECAR_DIR = _REPO_ROOT / "results"


def _sidecar_path(metric: str) -> Path:
    return _SIDECAR_DIR / f"experiments.{metric}.jsonl"


# Substrate ↔ control pool pairing (mg-ddee).
_PAIRS: tuple[tuple[str, str], ...] = (
    ("aquitanian", "control_aquitanian"),
    ("etruscan", "control_etruscan"),
    ("toponym", "control_toponym"),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_manifest_rows(auto_dir: Path) -> dict[str, dict]:
    """Hash → manifest row, across all pool manifests."""
    out: dict[str, dict] = {}
    for path in sorted(auto_dir.glob("*.manifest.jsonl")):
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                out[row["hypothesis_hash"]] = row
    return out


def _load_pool_entries(pools_dir: Path) -> dict[str, list[dict]]:
    """pool_name → list[entry_dict] (preserves original index order)."""
    out: dict[str, list[dict]] = {}
    for path in sorted(pools_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=_StringDateLoader)
        if not doc:
            continue
        out[doc["pool"]] = list(doc.get("entries", []))
    return out


def _load_result_rows(results_path: Path, metric: str) -> dict[str, dict]:
    """hash → most-recent-by-ran_at result row for the given metric.

    Reads the primary stream and (if present) the per-metric sidecar
    stream ``results/experiments.<metric>.jsonl``. Rows in the sidecar
    are ran_at-merged with the primary stream so the resume cache and
    "latest row wins" semantics work uniformly.
    """
    out: dict[str, dict] = {}
    paths = [results_path]
    sidecar = _sidecar_path(metric)
    if sidecar.exists() and sidecar.resolve() != results_path.resolve():
        paths.append(sidecar)
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row.get("metric") != metric:
                    continue
                h = row.get("hypothesis_hash")
                if not h:
                    continue
                cur = out.get(h)
                if cur is None or row.get("ran_at", "") > cur.get("ran_at", ""):
                    out[h] = row
    return out


def _edit_distance(a: list[str], b: list[str]) -> int:
    """Standard Levenshtein over phoneme sequences, treating each phoneme
    string atomically (so 'ts' is a single token, not 's' + 't'). O(|a|*|b|)."""
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
            cur[j] = min(
                cur[j - 1] + 1,
                prev[j] + 1,
                prev[j - 1] + cost,
            )
        prev = cur
    return prev[m]


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def wilcoxon_signed_rank_one_tail(diffs: list[float]) -> tuple[float, float, int]:
    """One-tail Wilcoxon signed-rank test (alternative: median(diffs) > 0).

    Returns ``(W_plus, p_one_tail, n_nonzero)``. Normal-approximation
    p-value with continuity correction; for n_nonzero < ~10 it is
    conservative but the test still has clear directionality. Zero
    diffs are dropped per Wilcoxon convention.
    """
    nonzero = [d for d in diffs if d != 0.0]
    n = len(nonzero)
    if n == 0:
        return 0.0, float("nan"), 0
    abs_vals = sorted(((abs(d), 1 if d > 0 else -1) for d in nonzero), key=lambda t: t[0])
    # Mid-rank for ties.
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
    p_one = 1.0 - _normal_cdf(z)  # alternative: W+ > mu
    return w_plus, p_one, n


def sign_test_one_tail(diffs: list[float]) -> tuple[int, int, float]:
    """One-tail sign test (alternative: P(diff > 0) > 0.5).

    Returns ``(n_pos, n_total_nonzero, p)``. Exact tail using cumulative
    binomial.
    """
    n_pos = sum(1 for d in diffs if d > 0)
    n_neg = sum(1 for d in diffs if d < 0)
    n = n_pos + n_neg
    if n == 0:
        return 0, 0, float("nan")
    # Exact one-tail: P(X >= n_pos | n, p=0.5).
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
# Pairing logic
# ---------------------------------------------------------------------------


def build_paired_diffs(
    *,
    metric: str,
    results_path: Path,
    auto_dir: Path,
    pools_dir: Path,
) -> list[dict]:
    """Compute a paired_diff row per substrate candidate that has a match.

    Returns one record per substrate candidate with these keys:

      * ``substrate_pool`` / ``control_pool``
      * ``surface`` (substrate side, used for grouping)
      * ``inscription_id`` / ``span_start`` / ``span_end``
      * ``substrate_score`` / ``control_score`` / ``paired_diff``
      * ``substrate_phonemes`` / ``control_phonemes``
      * ``edit_distance`` between the two phoneme sequences
      * ``substrate_hash`` / ``control_hash``

    Substrate candidates with no exact-window control match are dropped
    (paired_diff null per the spec) and counted in a sidecar diagnostic.
    """
    manifest = _load_manifest_rows(auto_dir)
    pools = _load_pool_entries(pools_dir)
    rows = _load_result_rows(results_path, metric)

    # Index control rows by (control_pool, inscription_id, span_start, span_end).
    by_window: dict[tuple[str, str, int, int], list[tuple[str, dict]]] = defaultdict(list)
    for h, row in rows.items():
        m = manifest.get(h)
        if m is None:
            continue
        pool = m.get("pool", "")
        if not pool.startswith("control_"):
            continue
        key = (pool, m["inscription_id"], int(m["span_start"]), int(m["span_end"]))
        by_window[key].append((h, row))

    def substrate_phonemes(m: dict) -> list[str]:
        return list(pools[m["pool"]][m["pool_entry_index"]]["phonemes"])

    out: list[dict] = []
    for h, row in rows.items():
        m = manifest.get(h)
        if m is None:
            continue
        sub_pool = m.get("pool", "")
        if sub_pool.startswith("control_"):
            continue
        ctrl_pool = "control_" + sub_pool
        key = (ctrl_pool, m["inscription_id"], int(m["span_start"]), int(m["span_end"]))
        candidates = by_window.get(key, [])
        if not candidates:
            continue
        sub_phonemes = substrate_phonemes(m)
        # Pick best control by min edit distance; tie-break by sorted hash.
        best_h: str | None = None
        best_row: dict | None = None
        best_phonemes: list[str] | None = None
        best_d = math.inf
        for ch, crow in sorted(candidates, key=lambda t: t[0]):
            cm = manifest[ch]
            ph = list(pools[ctrl_pool][cm["pool_entry_index"]]["phonemes"])
            d = _edit_distance(sub_phonemes, ph)
            if d < best_d:
                best_d = d
                best_h = ch
                best_row = crow
                best_phonemes = ph
        if best_h is None:
            continue
        sub_score = float(row.get("score", 0.0))
        ctrl_score = float(best_row.get("score", 0.0))
        out.append(
            {
                "substrate_pool": sub_pool,
                "control_pool": ctrl_pool,
                "surface": m["pool_entry_surface"],
                "inscription_id": m["inscription_id"],
                "span_start": int(m["span_start"]),
                "span_end": int(m["span_end"]),
                "substrate_score": sub_score,
                "control_score": ctrl_score,
                "paired_diff": sub_score - ctrl_score,
                "substrate_phonemes": sub_phonemes,
                "control_phonemes": best_phonemes,
                "edit_distance": int(best_d),
                "substrate_hash": h,
                "control_hash": best_h,
            }
        )
    return out


def aggregate_per_surface(records: list[dict]) -> list[dict]:
    """Group paired-diff records by (substrate_pool, surface) and compute
    the per-surface median paired_diff. Returns one row per surface."""
    by_key: dict[tuple[str, str], list[float]] = defaultdict(list)
    for rec in records:
        by_key[(rec["substrate_pool"], rec["surface"])].append(rec["paired_diff"])
    out: list[dict] = []
    for (pool, surface), diffs in sorted(by_key.items()):
        out.append(
            {
                "pool": pool,
                "surface": surface,
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


def render_markdown(
    *,
    metric: str,
    records: list[dict],
    aggregates: list[dict],
    top_per_pool: int = 50,
) -> str:
    out: list[str] = []
    out.append(f"# Paired-difference leaderboard — {metric}\n")
    out.append(
        "Generated by `scripts/paired_diff_rollup.py` (mg-ddee). For each "
        "substrate candidate, the matched control candidate is the one in the "
        "phonotactically-matched control pool that pins to the SAME "
        "(inscription, span). Among those, the closest phoneme sequence "
        "(by edit distance) wins. The substrate − control delta is the "
        "primary score. Substrate candidates without an exact-window control "
        "match are dropped from the aggregate.\n"
    )
    out.append(
        "**Acceptance gate (mg-ddee):** for at least one substrate pool, the "
        "per-surface paired_diff medians must have median > 0 with one-tail "
        "p < 0.05. The Wilcoxon signed-rank test (preferred for paired-difference "
        "statistics on per-surface medians) is the primary; the sign test is "
        "reported alongside as a distribution-free robustness check.\n"
    )

    # Per-pool acceptance gate.
    out.append("## Per-pool acceptance gate\n")
    out.append(
        "| substrate pool | n_surfaces | median(median paired_diff) | mean | "
        "frac surfaces > 0 | Wilcoxon W+ | Wilcoxon p (one-tail) | "
        "sign-test n+/n | sign-test p (one-tail) |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    by_pool: dict[str, list[dict]] = defaultdict(list)
    for agg in aggregates:
        by_pool[agg["pool"]].append(agg)
    pool_summaries: list[dict] = []
    for pool, group in sorted(by_pool.items()):
        meds = [g["median_paired_diff"] for g in group]
        wp_w, wp_p, wp_n = wilcoxon_signed_rank_one_tail(meds)
        sn_pos, sn_n, sn_p = sign_test_one_tail(meds)
        med_of_meds = median(meds)
        mean_of_meds = sum(meds) / len(meds) if meds else float("nan")
        frac_pos = sum(1 for v in meds if v > 0) / len(meds) if meds else float("nan")
        out.append(
            "| {p} | {n} | {med:+.4f} | {mean:+.4f} | {fp:.3f} | {w:.1f} | "
            "{wp:.4f} | {snp}/{snn} | {sp:.4f} |".format(
                p=pool, n=len(meds), med=med_of_meds, mean=mean_of_meds,
                fp=frac_pos, w=wp_w, wp=wp_p, snp=sn_pos, snn=sn_n, sp=sn_p,
            )
        )
        pool_summaries.append(
            {
                "pool": pool,
                "n_surfaces": len(meds),
                "median_of_medians": med_of_meds,
                "mean_of_medians": mean_of_meds,
                "frac_surfaces_positive": frac_pos,
                "wilcoxon_W_plus": wp_w,
                "wilcoxon_p_one_tail": wp_p,
                "wilcoxon_n_nonzero": wp_n,
                "sign_test_n_pos": sn_pos,
                "sign_test_n_total": sn_n,
                "sign_test_p_one_tail": sn_p,
            }
        )
    out.append("")

    # Per-pool: top-K surface leaderboards.
    for pool, group in sorted(by_pool.items()):
        ranked = sorted(group, key=lambda a: -a["median_paired_diff"])[:top_per_pool]
        out.append(f"## {pool} — top {len(ranked)} surfaces by median paired_diff\n")
        out.append(
            "| rank | surface | n | median paired_diff | mean | min | max | frac > 0 |"
        )
        out.append("|---:|---|---:|---:|---:|---:|---:|---:|")
        for i, a in enumerate(ranked, 1):
            out.append(
                "| {i} | `{s}` | {n} | {med:+.4f} | {mean:+.4f} | {mn:+.4f} | "
                "{mx:+.4f} | {fp:.3f} |".format(
                    i=i, s=a["surface"], n=a["n"], med=a["median_paired_diff"],
                    mean=a["mean_paired_diff"], mn=a["min_paired_diff"],
                    mx=a["max_paired_diff"], fp=a["frac_positive"],
                )
            )
        out.append("")

    out.append("## Notes\n")
    out.append(
        f"- Total substrate candidates with an exact-window control match: "
        f"**{len(records)}**.\n"
        f"- A `paired_diff` of +N means the substrate candidate scored N "
        f"higher than its phonotactically-matched control. The leaderboard "
        f"ranks substrate identity by the size of that gap, after "
        f"phonotactic baseline is subtracted by construction.\n"
        f"- Wilcoxon W+ is the sum of positive ranks under the signed-rank "
        f"transform; the one-tail p-value tests `median > 0`.\n"
        f"- Sign-test counts surfaces with positive paired-diff median; the "
        f"one-tail p-value tests `P(median > 0) > 0.5` against a 0.5 null.\n"
    )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--metric", required=True, help="Metric name to roll up.")
    parser.add_argument("--results", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--write",
        type=Path,
        default=None,
        help="Write the rendered markdown to this path. Defaults to "
        "results/rollup.paired_diff.<metric>.md.",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path to write the per-pool acceptance-gate stats as JSON.",
    )
    parser.add_argument("--top-per-pool", type=int, default=50)
    args = parser.parse_args(argv)

    records = build_paired_diffs(
        metric=args.metric,
        results_path=args.results,
        auto_dir=args.auto_dir,
        pools_dir=args.pools_dir,
    )
    aggregates = aggregate_per_surface(records)
    text = render_markdown(
        metric=args.metric,
        records=records,
        aggregates=aggregates,
        top_per_pool=args.top_per_pool,
    )

    out_path = args.write or (
        _REPO_ROOT / "results" / f"rollup.paired_diff.{args.metric}.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    # Build a per-pool summary for stdout / optional JSON sidecar.
    by_pool: dict[str, list[dict]] = defaultdict(list)
    for agg in aggregates:
        by_pool[agg["pool"]].append(agg)
    summary: list[dict] = []
    for pool, group in sorted(by_pool.items()):
        meds = [g["median_paired_diff"] for g in group]
        wp_w, wp_p, wp_n = wilcoxon_signed_rank_one_tail(meds)
        sn_pos, sn_n, sn_p = sign_test_one_tail(meds)
        summary.append(
            {
                "pool": pool,
                "n_surfaces": len(meds),
                "median_of_medians": median(meds),
                "frac_surfaces_positive": (
                    sum(1 for v in meds if v > 0) / len(meds) if meds else float("nan")
                ),
                "wilcoxon_W_plus": wp_w,
                "wilcoxon_p_one_tail": wp_p,
                "wilcoxon_n_nonzero": wp_n,
                "sign_test_n_pos": sn_pos,
                "sign_test_n_total": sn_n,
                "sign_test_p_one_tail": sn_p,
            }
        )
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
