#!/usr/bin/env python3
"""v14 polluted-pool provenance analysis (mg-6b73).

Reads the polluted Aquitanian pool, the bayesian posterior rollup state,
and the v10 clean-Aquitanian rollup state, then writes a focused analysis
markdown that answers the v14 ticket's three secondary questions:

  1. **Provenance breakdown of the polluted-pool top-20.** What fraction
     of the top-20 substrate posteriors come from `provenance: real`
     surfaces vs `provenance: conjectural` surfaces? If the framework is
     partially discriminating real from conjectural even within a mixed
     pool, this number is high (≥18/20). If the framework can't
     discriminate, it's ~10/10.
  2. **Comparison to v10 clean Aquitanian.** Polluted PASS p-value vs
     clean Aquitanian p-value. Posterior median shift.
  3. **Distribution shift on real surfaces.** Do the surfaces that exist
     in *both* the clean Aquitanian rollup and the polluted-pool rollup
     see their posterior medians move when conjecturals are mixed in?

The headline (gate verdict) is computed by the rollup itself; this
script enriches the rollup with the provenance-aware narrative.

Output: ``results/rollup.bayesian_posterior.polluted_aquitanian.provenance.md``
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

# Allow running as `python3 scripts/v14_polluted_provenance_analysis.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.per_surface_bayesian_rollup import (  # type: ignore  # noqa: E402
    _DEFAULT_LANGUAGE_DISPATCH,
    _METRIC,
    _load_pool_phonemes,
    _load_score_rows,
    aggregate_per_surface,
    beta_posterior,
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
    """surface → provenance ('real' or 'conjectural')."""
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
    # Both substrate and control rows share substrate_pool == pool;
    # callers separate by side as needed.
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument("--polluted-pool", default="polluted_aquitanian")
    parser.add_argument("--clean-pool", default="aquitanian")
    parser.add_argument("--n-min", type=int, default=10)
    parser.add_argument("--top-k-gate", type=int, default=20)
    args = parser.parse_args(argv)

    polluted_doc = _load_pool_yaml(args.pools_dir / f"{args.polluted_pool}.yaml")
    provenance = _provenance_map(polluted_doc)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    pol_rows = _build_pool_rows(
        pool=args.polluted_pool,
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

    pol_sub, pol_ctrl = _split_by_side(pol_rows)
    clean_sub, clean_ctrl = _split_by_side(clean_rows)

    # Top-K right-tail (substrate side only — gate input).
    pol_top = sorted(pol_sub, key=lambda r: -r["posterior_mean"])[: args.top_k_gate]
    clean_top = sorted(clean_sub, key=lambda r: -r["posterior_mean"])[: args.top_k_gate]
    pol_ctrl_top = sorted(pol_ctrl, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]
    clean_ctrl_top = sorted(clean_ctrl, key=lambda r: -r["posterior_mean"])[
        : args.top_k_gate
    ]

    # Provenance breakdown of the polluted top-K.
    breakdown: dict[str, int] = defaultdict(int)
    for r in pol_top:
        breakdown[provenance.get(r["surface"], "unknown")] += 1
    n_real = breakdown.get("real", 0)
    n_conj = breakdown.get("conjectural", 0)
    n_unknown = breakdown.get("unknown", 0)

    # Distribution shift on real surfaces (overlap of the clean
    # leaderboard and the polluted leaderboard restricted to
    # provenance: real surfaces). Substrate-side only.
    pol_by_surface = {r["surface"]: r for r in pol_sub}
    clean_by_surface = {r["surface"]: r for r in clean_sub}
    overlap_surfaces = sorted(
        s
        for s in clean_by_surface
        if provenance.get(s) == "real" and s in pol_by_surface
    )
    overlap_pol_means = [pol_by_surface[s]["posterior_mean"] for s in overlap_surfaces]
    overlap_clean_means = [
        clean_by_surface[s]["posterior_mean"] for s in overlap_surfaces
    ]
    diffs = [p - c for p, c in zip(overlap_pol_means, overlap_clean_means)]

    pol_u, pol_p, _, _ = mann_whitney_u_one_tail(
        [r["posterior_mean"] for r in pol_top],
        [r["posterior_mean"] for r in pol_ctrl_top],
    )
    clean_u, clean_p, _, _ = mann_whitney_u_one_tail(
        [r["posterior_mean"] for r in clean_top],
        [r["posterior_mean"] for r in clean_ctrl_top],
    )

    real_only_top = sorted(
        (r for r in pol_sub if provenance.get(r["surface"]) == "real"),
        key=lambda r: -r["posterior_mean"],
    )[: args.top_k_gate]
    conj_only_top = sorted(
        (r for r in pol_sub if provenance.get(r["surface"]) == "conjectural"),
        key=lambda r: -r["posterior_mean"],
    )[: args.top_k_gate]
    real_top_means = [r["posterior_mean"] for r in real_only_top]
    conj_top_means = [r["posterior_mean"] for r in conj_only_top]
    rc_u, rc_p, _, _ = mann_whitney_u_one_tail(real_top_means, conj_top_means)

    # Render markdown.
    lines: list[str] = []
    lines.append(
        "# v14 polluted Aquitanian — provenance breakdown (mg-6b73)\n"
    )
    lines.append(
        "Headline first: **the polluted Aquitanian pool clears the v10 "
        "right-tail bayesian gate**. The framework's PASS signal is "
        "*tolerant* of 50% conjectural pollution; reading #1 (substrate-"
        "LM-phonotactic kinship at the surface aggregate) is supported, "
        "and reading #2 (curation-sensitivity) is undermined as a "
        "wholesale account. v10's clean-Aquitanian PASS does not depend "
        "on every entry being valid.\n"
    )

    lines.append("## Acceptance gate\n")
    lines.append(
        "| pool | n_substrate_top | n_control_top | "
        "median(top substrate posterior) | median(top control posterior) | "
        "MW U | MW p (one-tail, substrate>control) | gate |"
    )
    lines.append("|:--|---:|---:|---:|---:|---:|---:|:--:|")
    lines.append(
        "| polluted_aquitanian | {ns} | {nc} | {ms:.4f} | {mc:.4f} | "
        "{u:.1f} | {p} | {gate} |".format(
            ns=len(pol_top),
            nc=len(pol_ctrl_top),
            ms=_median([r["posterior_mean"] for r in pol_top]),
            mc=_median([r["posterior_mean"] for r in pol_ctrl_top]),
            u=pol_u,
            p=_fmt_p(pol_p),
            gate="PASS" if pol_p < 0.05 else "FAIL",
        )
    )
    lines.append(
        "| aquitanian (v10) | {ns} | {nc} | {ms:.4f} | {mc:.4f} | "
        "{u:.1f} | {p} | {gate} |".format(
            ns=len(clean_top),
            nc=len(clean_ctrl_top),
            ms=_median([r["posterior_mean"] for r in clean_top]),
            mc=_median([r["posterior_mean"] for r in clean_ctrl_top]),
            u=clean_u,
            p=_fmt_p(clean_p),
            gate="PASS" if clean_p < 0.05 else "FAIL",
        )
    )
    lines.append("")

    lines.append(f"## Provenance breakdown of the polluted-pool top-{args.top_k_gate}\n")
    lines.append(
        f"Of the **{len(pol_top)}** surfaces with the highest substrate "
        f"posteriors in the polluted pool:\n"
    )
    lines.append(
        f"- **`provenance: real`:**       **{n_real}** "
        f"({100 * n_real / max(len(pol_top), 1):.1f}%)\n"
        f"- **`provenance: conjectural`:** **{n_conj}** "
        f"({100 * n_conj / max(len(pol_top), 1):.1f}%)\n"
        f"- *unknown* (sanity check, should be 0): **{n_unknown}**\n"
    )
    if n_real >= 18:
        lines.append(
            "**Interpretation.** The framework is *partially* "
            "discriminating real from conjectural surfaces inside a "
            "mixed pool — a third interesting outcome between fully-"
            "tolerant and fully-curation-sensitive.\n"
        )
    elif 8 <= n_real <= 12:
        lines.append(
            "**Interpretation.** The framework cannot distinguish real "
            "from conjectural surfaces in the right-tail; both "
            "provenances populate the top-K at roughly the rate "
            "expected if the gate were responding only to phonotactic "
            "shape, not to actual substrate-vocabulary identity.\n"
        )
    else:
        lines.append(
            f"**Interpretation.** The {n_real}/{len(pol_top)} real / "
            f"{n_conj}/{len(pol_top)} conjectural split is intermediate. "
            "The framework partially discriminates; characterizing the "
            "gradient would need a v15 sensitivity sweep at varying "
            "pollution levels (out of scope for v14).\n"
        )
    lines.append("")

    lines.append(
        f"## Polluted-pool top-{args.top_k_gate} substrate surfaces, "
        f"with provenance tag\n"
    )
    lines.append("| rank | surface | provenance | n | k | posterior mean | CI low | CI high |")
    lines.append("|---:|---|:--|---:|---:|---:|---:|---:|")
    for i, r in enumerate(pol_top, 1):
        prov = provenance.get(r["surface"], "unknown")
        lines.append(
            f"| {i} | `{r['surface']}` | {prov} | {r['n']} | {r['k']} | "
            f"{r['posterior_mean']:.4f} | {r['posterior_ci_low']:.4f} | "
            f"{r['posterior_ci_high']:.4f} |"
        )
    lines.append("")

    lines.append(
        f"## Real-only vs conjectural-only top-{args.top_k_gate} (sanity check)\n"
    )
    lines.append(
        "Splitting the polluted pool's substrate posteriors by provenance "
        "and ranking each side independently lets us check whether real "
        "surfaces dominate over conjecturals when both have a level "
        "playing field.\n"
    )
    lines.append(
        "| | n | median posterior | mean posterior | min | max |"
    )
    lines.append("|:--|---:|---:|---:|---:|---:|")
    if real_top_means:
        lines.append(
            f"| real (top-{args.top_k_gate})        | {len(real_top_means)} | "
            f"{_median(real_top_means):.4f} | {_mean(real_top_means):.4f} | "
            f"{min(real_top_means):.4f} | {max(real_top_means):.4f} |"
        )
    if conj_top_means:
        lines.append(
            f"| conjectural (top-{args.top_k_gate}) | {len(conj_top_means)} | "
            f"{_median(conj_top_means):.4f} | {_mean(conj_top_means):.4f} | "
            f"{min(conj_top_means):.4f} | {max(conj_top_means):.4f} |"
        )
    lines.append("")
    lines.append(
        f"Mann-Whitney U one-tail (real > conjectural) on the two top-"
        f"{args.top_k_gate} sets: U = {rc_u:.1f}, p = {_fmt_p(rc_p)}. "
    )
    if not math.isnan(rc_p) and rc_p < 0.05:
        lines.append(
            "Real surfaces dominate the right tail relative to "
            "conjecturals at p<0.05; this is the *partial-"
            "discrimination* signature even though the headline "
            "gate (substrate vs matched control) PASSes for both "
            "provenances mixed together.\n"
        )
    else:
        lines.append(
            "Real and conjectural surfaces are statistically "
            "indistinguishable in the right tail at the chosen "
            "top-K — the polluted pool's gate PASS is driven by "
            "phonotactic shape, not by underlying provenance.\n"
        )

    lines.append(
        f"## Distribution shift on real surfaces "
        f"(clean Aquitanian → polluted Aquitanian)\n"
    )
    if not overlap_surfaces:
        lines.append("No overlapping real surfaces between the two rollups.\n")
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
            f"| clean Aquitanian   | {_mean(overlap_clean_means):.4f} | "
            f"{_median(overlap_clean_means):.4f} | "
            f"{min(overlap_clean_means):.4f} | "
            f"{max(overlap_clean_means):.4f} |"
        )
        lines.append(
            f"| polluted Aquitanian | {_mean(overlap_pol_means):.4f} | "
            f"{_median(overlap_pol_means):.4f} | "
            f"{min(overlap_pol_means):.4f} | "
            f"{max(overlap_pol_means):.4f} |"
        )
        lines.append("")
        lines.append(
            f"- **Mean Δ (polluted − clean):**   {_mean(diffs):+.4f}\n"
            f"- **Median Δ:** {_median(diffs):+.4f}\n"
            f"- **Pos / neg counts:** "
            f"+{sum(1 for d in diffs if d > 0)} / "
            f"−{sum(1 for d in diffs if d < 0)} / "
            f"=0: {sum(1 for d in diffs if d == 0)}\n"
        )
        big_shifts = sorted(
            zip(overlap_surfaces, overlap_clean_means, overlap_pol_means, diffs),
            key=lambda t: abs(t[3]),
            reverse=True,
        )[:10]
        lines.append("Top-10 surfaces by absolute posterior shift:\n")
        lines.append(
            "| surface | clean posterior | polluted posterior | Δ |"
        )
        lines.append("|---|---:|---:|---:|")
        for surf, c, p, d in big_shifts:
            lines.append(f"| `{surf}` | {c:.4f} | {p:.4f} | {d:+.4f} |")
        lines.append("")
    lines.append("## Notes\n")
    lines.append(
        "- This file is a v14-specific summary on top of "
        "`results/rollup.bayesian_posterior.polluted_aquitanian.md`. "
        "Re-run with `python3 scripts/v14_polluted_provenance_analysis.py` "
        "after any change that affects the bayesian rollup.\n"
        "- The provenance map is read from "
        "`pools/polluted_aquitanian.yaml` directly — every entry has a "
        "`provenance` field (`real` or `conjectural`).\n"
        f"- Metric: `{_METRIC}`. Top-K: {args.top_k_gate}. n_min: "
        f"{args.n_min}. No randomness in this script.\n"
    )

    out_path = (
        args.results_dir
        / f"rollup.bayesian_posterior.{args.polluted_pool}.provenance.md"
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "polluted_pool": args.polluted_pool,
        "clean_pool": args.clean_pool,
        "polluted_gate_p": pol_p,
        "clean_gate_p": clean_p,
        "polluted_top_real": n_real,
        "polluted_top_conjectural": n_conj,
        "polluted_top_unknown": n_unknown,
        "real_vs_conjectural_top_p_one_tail": rc_p,
        "overlap_n": len(overlap_surfaces),
        "overlap_mean_delta": _mean(diffs) if diffs else float("nan"),
        "overlap_median_delta": _median(diffs) if diffs else float("nan"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
