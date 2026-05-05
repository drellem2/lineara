#!/usr/bin/env python3
"""v15 cross-language pollution analysis (mg-7ecb).

Reads the cross-language polluted Aquitanian pool, the bayesian
posterior rollup state, the v14 same-distribution polluted rollup, and
the v10 clean Aquitanian rollup, then writes a focused analysis
markdown that answers the v15 ticket's binary question:

  **Does the framework PASS for ANY phonotactic match, or only
  same-distribution?**

The headline (gate verdict) is computed by the rollup itself; this
script enriches the rollup with the provenance-aware narrative:

  1. **Provenance breakdown of the polluted-pool top-20.** Of the top-20
     substrate posteriors in the cross-language polluted pool, what
     fraction are `provenance: real` vs `provenance: conjectural_greek`?
     Three regimes (per the ticket):
     - real ≥ 18: framework partially discriminates Aquitanian-shape
       from Greek-shape even when both are mixed — between v14 (no
       discrimination) and full selectivity.
     - real / conj split ~10/10: framework fully tolerates cross-
       language pollution; gate is essentially trivial.
     - real dominates AND gate FAILS: real-surface signal is detectable
       but overwhelmed by Greek-shape noise. Interesting middle case.
  2. **Comparison to v14 and v10.** Cross-language gate p vs same-
     distribution gate p vs clean-pool gate p, with median(top-K
     substrate posterior) and median(top-K control posterior) for each.
  3. **Distribution shift on real surfaces.** Do real Aquitanian
     surfaces' posteriors move when Greek-shape conjecturals are mixed
     in? Compared against v14's distribution-shift result (v14 found
     individual surfaces shuffle dramatically even though the bulk
     barely moves).

Output: ``results/rollup.bayesian_posterior.greek_polluted_aquitanian.provenance.md``
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Allow running as `python3 scripts/v15_cross_language_pollution_analysis.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.per_surface_bayesian_rollup import (  # type: ignore  # noqa: E402
    _DEFAULT_LANGUAGE_DISPATCH,
    _METRIC,
    _load_pool_phonemes,
    _load_score_rows,
    aggregate_per_surface,
    build_posterior_rows,
    build_v8_records,
    build_v9_records,
    mann_whitney_u_one_tail,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"
_DEFAULT_POOLS = _REPO_ROOT / "pools"


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_pool_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def _provenance_map(pool_doc: dict) -> dict[str, str]:
    """surface → provenance (e.g. 'real' or 'conjectural_greek')."""
    out: dict[str, str] = {}
    for entry in pool_doc.get("entries", []):
        out[entry["surface"]] = entry.get("provenance", "real")
    return out


def _build_pool_rows(
    *,
    pool: str,
    auto_dir: Path,
    auto_sig_dir: Path,
    score_rows: dict,
    pool_phonemes: dict,
    n_min: int,
) -> list[dict]:
    """Replicate per_surface_bayesian_rollup.build_posterior_rows for one pool."""
    records: list[dict] = []
    records.extend(
        build_v8_records(
            pool=pool,
            auto_dir=auto_dir,
            score_rows=score_rows,
            pool_phonemes=pool_phonemes,
            language_dispatch=_DEFAULT_LANGUAGE_DISPATCH,
        )
    )
    records.extend(
        build_v9_records(
            pool=pool,
            auto_dir=auto_sig_dir,
            score_rows=score_rows,
            language_dispatch=_DEFAULT_LANGUAGE_DISPATCH,
        )
    )
    aggregates = aggregate_per_surface(records)
    rows = build_posterior_rows(aggregates, n_min=n_min)
    return [r for r in rows if r["substrate_pool"] == pool]


def _split_by_side(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    sub = [r for r in rows if r["side"] == "substrate"]
    ctrl = [r for r in rows if r["side"] == "control"]
    return sub, ctrl


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def _fmt_p(p: float) -> str:
    if math.isnan(p):
        return "nan"
    if p == 0.0:
        return "<1e-300"
    return f"{p:.3e}"


def _gate_summary(
    sub_top: list[dict],
    ctrl_top: list[dict],
) -> tuple[float, float, str]:
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, _, _ = mann_whitney_u_one_tail(sub_means, ctrl_means)
    gate = "PASS" if (not math.isnan(p)) and p < 0.05 else "FAIL"
    return u, p, gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--cross-lang-pool", default="greek_polluted_aquitanian"
    )
    parser.add_argument("--same-dist-pool", default="polluted_aquitanian")
    parser.add_argument("--clean-pool", default="aquitanian")
    parser.add_argument("--n-min", type=int, default=10)
    parser.add_argument("--top-k-gate", type=int, default=20)
    args = parser.parse_args(argv)

    cross_doc = _load_pool_yaml(args.pools_dir / f"{args.cross_lang_pool}.yaml")
    provenance = _provenance_map(cross_doc)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    cross_rows = _build_pool_rows(
        pool=args.cross_lang_pool,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        n_min=args.n_min,
    )
    same_rows = _build_pool_rows(
        pool=args.same_dist_pool,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        n_min=args.n_min,
    )
    clean_rows = _build_pool_rows(
        pool=args.clean_pool,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        n_min=args.n_min,
    )

    cross_sub, cross_ctrl = _split_by_side(cross_rows)
    same_sub, same_ctrl = _split_by_side(same_rows)
    clean_sub, clean_ctrl = _split_by_side(clean_rows)

    cross_top = sorted(cross_sub, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    cross_ctrl_top = sorted(cross_ctrl, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    same_top = sorted(same_sub, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    same_ctrl_top = sorted(same_ctrl, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    clean_top = sorted(clean_sub, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    clean_ctrl_top = sorted(clean_ctrl, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]

    cross_u, cross_p, cross_gate = _gate_summary(cross_top, cross_ctrl_top)
    same_u, same_p, same_gate = _gate_summary(same_top, same_ctrl_top)
    clean_u, clean_p, clean_gate = _gate_summary(clean_top, clean_ctrl_top)

    breakdown: Counter = Counter()
    for r in cross_top:
        breakdown[provenance.get(r["surface"], "unknown")] += 1
    n_real = breakdown.get("real", 0)
    n_conj_greek = breakdown.get("conjectural_greek", 0)
    n_unknown = sum(
        v for k, v in breakdown.items() if k not in ("real", "conjectural_greek")
    )

    real_only_top = sorted(
        (r for r in cross_sub if provenance.get(r["surface"]) == "real"),
        key=lambda r: -r["posterior_mean"],
    )[: args.top_k_gate]
    conj_only_top = sorted(
        (
            r
            for r in cross_sub
            if provenance.get(r["surface"]) == "conjectural_greek"
        ),
        key=lambda r: -r["posterior_mean"],
    )[: args.top_k_gate]
    real_top_means = [r["posterior_mean"] for r in real_only_top]
    conj_top_means = [r["posterior_mean"] for r in conj_only_top]
    rc_u, rc_p, _, _ = mann_whitney_u_one_tail(real_top_means, conj_top_means)

    cross_by_surface = {r["surface"]: r for r in cross_sub}
    clean_by_surface = {r["surface"]: r for r in clean_sub}
    overlap_surfaces = sorted(
        s
        for s in clean_by_surface
        if provenance.get(s) == "real" and s in cross_by_surface
    )
    overlap_cross_means = [
        cross_by_surface[s]["posterior_mean"] for s in overlap_surfaces
    ]
    overlap_clean_means = [
        clean_by_surface[s]["posterior_mean"] for s in overlap_surfaces
    ]
    diffs = [c - p for c, p in zip(overlap_cross_means, overlap_clean_means)]

    lines: list[str] = []
    lines.append(
        "# v15 cross-language pollution — provenance breakdown (mg-7ecb)\n"
    )

    within_tail_discriminates = (
        not math.isnan(rc_p) and rc_p < 0.05
    )

    if cross_gate == "PASS" and n_real >= 18:
        headline = (
            "**The cross-language polluted Aquitanian pool clears the "
            "v10 right-tail bayesian gate, BUT real Aquitanian surfaces "
            "dominate the top-20.** This is a *partial-discrimination* "
            "outcome: the gate has some shape selectivity (Greek-shape "
            "conjecturals are pushed below the right tail relative to "
            "real Aquitanian) but not enough to flip the headline gate "
            "to FAIL. The v14 manuscript-shape claim ('any pool whose "
            "phoneme + length distribution is drawn from the substrate's "
            "own marginal distribution') is **partially** supported: the "
            "framework discriminates substrate-shape from non-substrate-"
            "shape *within* the right tail, but the population gate is "
            "not selective enough to break the PASS."
        )
    elif cross_gate == "PASS" and 8 <= n_real <= 12 and not within_tail_discriminates:
        headline = (
            "**The cross-language polluted Aquitanian pool clears the "
            "v10 right-tail bayesian gate AND real / Greek-shape "
            "conjecturals split roughly 50/50 in the top-20.** This is "
            "the *fully-trivial* outcome: the framework's PASS signal "
            "is essentially a phonotactic-overlap test between the pool "
            "and the LM, regardless of distribution-shape match. The v14 "
            "manuscript-shape claim ('any pool whose phoneme + length "
            "distribution is drawn from the substrate's own marginal "
            "distribution') is **weakened** to 'any pool whose entries "
            "have non-trivial overlap with the LM's char-bigram support'."
        )
    elif cross_gate == "PASS" and within_tail_discriminates:
        # The "neutral-ish" / partial-discrimination outcome flagged in
        # the mg-7ecb brief as "the most interesting case for the
        # manuscript". Headline gate PASSes (so the framework is not
        # *fully* shape-selective) but real surfaces dominate the right
        # tail relative to Greek-shape conjecturals at p<0.05 (so the
        # framework *partially* respects substrate-distribution shape).
        headline = (
            f"**The cross-language polluted Aquitanian pool clears the "
            f"v10 right-tail bayesian gate at p = {_fmt_p(cross_p)} "
            f"(top-20 split: {n_real} real / {n_conj_greek} "
            f"conjectural-greek), AND within the right tail real "
            f"Aquitanian surfaces dominate Greek-shape conjecturals at "
            f"p = {_fmt_p(rc_p)}.** This is the *partial-discrimination* "
            "outcome: the gate has measurable shape selectivity (Greek-"
            "shape conjecturals score lower than real Aquitanian within "
            "the substrate-side right tail) but not enough to flip the "
            "headline gate to FAIL — the LM still rewards Greek-shape "
            "phonotactic strings well enough relative to scramble "
            "controls. The v14 manuscript-shape claim ('any pool whose "
            "phoneme + length distribution is drawn from the substrate's "
            "own marginal distribution') is **refined**: the framework "
            "discriminates substrate-shape from non-substrate-shape "
            "*within* the right tail, but the population gate clears for "
            "any pool with non-trivial char-bigram overlap with the LM."
        )
    elif cross_gate == "PASS":
        headline = (
            f"**The cross-language polluted Aquitanian pool clears the "
            f"v10 right-tail bayesian gate at p = {_fmt_p(cross_p)}, "
            f"with the top-20 split {n_real} real / {n_conj_greek} "
            f"conjectural-greek.** Intermediate outcome — see the "
            "real-vs-conjectural section below for the within-tail "
            "discrimination test."
        )
    elif cross_gate == "FAIL" and n_real >= 18:
        headline = (
            f"**The cross-language polluted Aquitanian pool FAILS the "
            f"v10 right-tail bayesian gate at p = {_fmt_p(cross_p)}, "
            f"but real Aquitanian surfaces dominate the top-20 "
            f"({n_real}/{args.top_k_gate}).** The gate respects "
            "substrate-distribution shape: real Aquitanian roots are "
            "rewarded, Greek-shape conjecturals are not, and the "
            "population gate flips to FAIL because the overall "
            "substrate-side distribution is dragged down by the Greek-"
            "shape half. v14's manuscript-shape claim stands as written: "
            "the PASS depends on the polluting distribution matching "
            "the substrate's own."
        )
    else:
        headline = (
            f"**The cross-language polluted Aquitanian pool FAILS the "
            f"v10 right-tail bayesian gate at p = {_fmt_p(cross_p)} "
            f"(top-20 split: {n_real} real / {n_conj_greek} "
            f"conjectural-greek).** The framework's PASS signal has "
            "real selectivity to substrate-distribution shape — v14's "
            "PASS-on-same-distribution-pollution holds because the "
            f"conjecturals shared Aquitanian shape, and the v14 "
            f"manuscript-shape claim stands as written."
        )
    lines.append(headline + "\n")

    lines.append("## Acceptance gate (cross-language vs same-distribution vs clean)\n")
    lines.append(
        "| pool | n_substrate_top | n_control_top | "
        "median(top substrate posterior) | median(top control posterior) | "
        "MW U | MW p (one-tail, substrate>control) | gate |"
    )
    lines.append("|:--|---:|---:|---:|---:|---:|---:|:--:|")
    for label, sub_top, ctrl_top, u, p, gate in [
        (
            f"{args.cross_lang_pool} (v15, cross-language)",
            cross_top,
            cross_ctrl_top,
            cross_u,
            cross_p,
            cross_gate,
        ),
        (
            f"{args.same_dist_pool} (v14, same-distribution)",
            same_top,
            same_ctrl_top,
            same_u,
            same_p,
            same_gate,
        ),
        (
            f"{args.clean_pool} (v10, clean)",
            clean_top,
            clean_ctrl_top,
            clean_u,
            clean_p,
            clean_gate,
        ),
    ]:
        lines.append(
            "| {label} | {ns} | {nc} | {ms:.4f} | {mc:.4f} | {u:.1f} | {p} | {gate} |".format(
                label=label,
                ns=len(sub_top),
                nc=len(ctrl_top),
                ms=_median([r["posterior_mean"] for r in sub_top]),
                mc=_median([r["posterior_mean"] for r in ctrl_top]),
                u=u,
                p=_fmt_p(p),
                gate=gate,
            )
        )
    lines.append("")

    lines.append(
        f"## Provenance breakdown of the polluted-pool top-{args.top_k_gate}\n"
    )
    lines.append(
        f"Of the **{len(cross_top)}** surfaces with the highest substrate "
        f"posteriors in the cross-language polluted pool:\n"
    )
    lines.append(
        f"- **`provenance: real`:**             **{n_real}** "
        f"({100 * n_real / max(len(cross_top), 1):.1f}%)\n"
        f"- **`provenance: conjectural_greek`:** **{n_conj_greek}** "
        f"({100 * n_conj_greek / max(len(cross_top), 1):.1f}%)\n"
        f"- *unknown* (sanity check, should be 0): **{n_unknown}**\n"
    )
    lines.append(
        f"v14's same-distribution polluted pool top-20 was 9 real / 11 "
        f"conjectural (~50/50); v15's split is {n_real}/{n_conj_greek} = "
        f"{n_real}:{n_conj_greek}.\n"
    )

    lines.append(
        f"## Polluted-pool top-{args.top_k_gate} substrate surfaces, "
        f"with provenance tag\n"
    )
    lines.append(
        "| rank | surface | provenance | n | k | posterior mean | CI low | CI high |"
    )
    lines.append("|---:|---|:--|---:|---:|---:|---:|---:|")
    for i, r in enumerate(cross_top, 1):
        prov = provenance.get(r["surface"], "unknown")
        lines.append(
            f"| {i} | `{r['surface']}` | {prov} | {r['n']} | {r['k']} | "
            f"{r['posterior_mean']:.4f} | {r['posterior_ci_low']:.4f} | "
            f"{r['posterior_ci_high']:.4f} |"
        )
    lines.append("")

    lines.append(
        f"## Real-only vs conjectural-greek-only top-{args.top_k_gate} "
        "(within-tail discrimination)\n"
    )
    lines.append(
        "Splitting the cross-language polluted pool's substrate "
        "posteriors by provenance and ranking each side independently "
        "lets us check whether real Aquitanian surfaces dominate over "
        "Greek-shape conjecturals when both have a level playing field. "
        "If real dominates, the framework discriminates within the "
        "right tail even when it can't break the headline gate.\n"
    )
    lines.append("| | n | median posterior | mean posterior | min | max |")
    lines.append("|:--|---:|---:|---:|---:|---:|")
    if real_top_means:
        lines.append(
            f"| real (top-{args.top_k_gate})              | "
            f"{len(real_top_means)} | {_median(real_top_means):.4f} | "
            f"{_mean(real_top_means):.4f} | {min(real_top_means):.4f} | "
            f"{max(real_top_means):.4f} |"
        )
    if conj_top_means:
        lines.append(
            f"| conjectural_greek (top-{args.top_k_gate}) | "
            f"{len(conj_top_means)} | {_median(conj_top_means):.4f} | "
            f"{_mean(conj_top_means):.4f} | {min(conj_top_means):.4f} | "
            f"{max(conj_top_means):.4f} |"
        )
    lines.append("")
    lines.append(
        f"Mann-Whitney U one-tail (real > conjectural_greek) on the two "
        f"top-{args.top_k_gate} sets: U = {rc_u:.1f}, p = {_fmt_p(rc_p)}.\n"
    )
    if not math.isnan(rc_p) and rc_p < 0.05:
        lines.append(
            "Real surfaces dominate the right tail relative to Greek-"
            "shape conjecturals at p<0.05. **Within-tail discrimination "
            "is detectable** even though the headline gate may PASS or "
            "FAIL depending on aggregation. Combined with v14 (which "
            "found NO within-tail discrimination on same-distribution "
            "pollution, real-vs-conjectural MW p = 0.98), v15 shows the "
            "framework can distinguish substrate-shape from non-"
            "substrate-shape — but only when the polluting distribution "
            "is *different enough*. v14's same-Aquitanian-shape "
            "conjecturals are indistinguishable from real Aquitanian; "
            "v15's Greek-shape conjecturals are distinguishable.\n"
        )
    else:
        lines.append(
            "Real and Greek-shape conjectural surfaces are statistically "
            "indistinguishable in the right tail at the chosen top-K — "
            "the cross-language polluted pool's gate verdict is driven "
            "by phonotactic overlap with the LM, not by distribution-"
            "shape match.\n"
        )

    lines.append(
        f"## Distribution shift on real surfaces "
        f"(clean Aquitanian → cross-language polluted)\n"
    )
    if not overlap_surfaces:
        lines.append(
            "No overlapping real surfaces between the two rollups.\n"
        )
    else:
        lines.append(
            f"Surfaces present in both rollups (real-provenance only): "
            f"**{len(overlap_surfaces)}**.\n"
        )
        lines.append(
            "| | mean posterior | median posterior | min | max |"
        )
        lines.append("|:--|---:|---:|---:|---:|")
        lines.append(
            f"| clean Aquitanian        | {_mean(overlap_clean_means):.4f} | "
            f"{_median(overlap_clean_means):.4f} | "
            f"{min(overlap_clean_means):.4f} | "
            f"{max(overlap_clean_means):.4f} |"
        )
        lines.append(
            f"| cross-language polluted | {_mean(overlap_cross_means):.4f} | "
            f"{_median(overlap_cross_means):.4f} | "
            f"{min(overlap_cross_means):.4f} | "
            f"{max(overlap_cross_means):.4f} |"
        )
        lines.append("")
        lines.append(
            f"- **Mean Δ (cross-language − clean):** {_mean(diffs):+.4f}\n"
            f"- **Median Δ:**                       {_median(diffs):+.4f}\n"
            f"- **Pos / neg counts:** "
            f"+{sum(1 for d in diffs if d > 0)} / "
            f"−{sum(1 for d in diffs if d < 0)} / "
            f"=0: {sum(1 for d in diffs if d == 0)}\n"
        )
        big_shifts = sorted(
            zip(overlap_surfaces, overlap_clean_means, overlap_cross_means, diffs),
            key=lambda t: abs(t[3]),
            reverse=True,
        )[:10]
        lines.append("Top-10 surfaces by absolute posterior shift:\n")
        lines.append(
            "| surface | clean posterior | cross-language posterior | Δ |"
        )
        lines.append("|---|---:|---:|---:|")
        for surf, c, p, d in big_shifts:
            lines.append(f"| `{surf}` | {c:.4f} | {p:.4f} | {d:+.4f} |")
        lines.append("")

    lines.append("## Notes\n")
    lines.append(
        f"- This file is a v15-specific summary on top of "
        f"`results/rollup.bayesian_posterior.{args.cross_lang_pool}.md`. "
        "Re-run with `python3 scripts/v15_cross_language_pollution_analysis.py` "
        "after any change that affects the bayesian rollup.\n"
        "- The provenance map is read from "
        f"`pools/{args.cross_lang_pool}.yaml` directly — every entry has "
        "a `provenance` field (`real` or `conjectural_greek`).\n"
        f"- Metric: `{_METRIC}`. Top-K: {args.top_k_gate}. n_min: "
        f"{args.n_min}. No randomness in this script.\n"
    )

    out_path = (
        args.results_dir
        / f"rollup.bayesian_posterior.{args.cross_lang_pool}.provenance.md"
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "cross_lang_pool": args.cross_lang_pool,
        "same_dist_pool": args.same_dist_pool,
        "clean_pool": args.clean_pool,
        "cross_gate_p": cross_p,
        "cross_gate": cross_gate,
        "same_gate_p": same_p,
        "clean_gate_p": clean_p,
        "cross_top_real": n_real,
        "cross_top_conjectural_greek": n_conj_greek,
        "cross_top_unknown": n_unknown,
        "real_vs_conjectural_greek_top_p_one_tail": rc_p,
        "real_vs_conjectural_greek_top_u": rc_u,
        "overlap_n": len(overlap_surfaces),
        "overlap_mean_delta": _mean(diffs) if diffs else float("nan"),
        "overlap_median_delta": _median(diffs) if diffs else float("nan"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
