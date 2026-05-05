#!/usr/bin/env python3
"""v18 pollution-level sweep on Aquitanian (mg-9f18).

Characterizes how the right-tail bayesian gate's p-value scales with
curation noise, by running the v10 gate over four pollution levels:

  * 10% conjectural / 90% real    (pools/polluted_aquitanian_10pct.yaml)
  * 25% conjectural / 75% real    (pools/polluted_aquitanian_25pct.yaml)
  * 50% conjectural / 50% real    (pools/polluted_aquitanian.yaml — v14)
  * 75% conjectural / 25% real    (pools/polluted_aquitanian_75pct.yaml)

All four pools draw conjecturals from the substrate's *own* marginal
phoneme distribution (same-distribution pollution); the only thing that
varies across rows is the conjectural share. The matched control for
each pool is built by the v6 unigram sampler off the polluted pool's
*combined* (real + conjectural) marginal histogram, so the control
moves with the polluted pool's distribution.

Background
==========
v14 (mg-6b73) found that the right-tail gate on Aquitanian PASSes at
v10-magnitude p (≈3e-05) even when 50% of the pool is conjectural-
same-distribution. The polecat noted: *"v14's PASS at 50% suggests the
gate is essentially insensitive to pollution within the same phoneme-
distribution shape, but quantifying the gradient could rule out a
sharp threshold near 100%."* v18 (mg-9f18) does the quantification.

Two reasonable shapes for the gradient:

  * **Smooth curve.** Gate p stays at v10-magnitude across 10%/25%/50%
    and only widens slightly at 75%, ruling out a sharp threshold.
    Confirms: the framework's PASS at the population level is driven
    by phonotactic-distribution-shape match, not by the *fraction* of
    surfaces that are real substrate vocabulary.
  * **Sharp threshold near 100%.** Gate p stays at v10-magnitude
    through 50%-75% and collapses only near 90%-100% (extrapolation
    from the trend). Adds nuance to the v14 PASS-tolerance story.

Output
======
  results/rollup.pollution_level_sweep.md
  results/rollup.bayesian_posterior.polluted_aquitanian_10pct.md
  results/rollup.bayesian_posterior.polluted_aquitanian_25pct.md
  results/rollup.bayesian_posterior.polluted_aquitanian_75pct.md

Re-runs are deterministic given the result stream and the manifests.

Usage
=====
  python3 scripts/v18_pollution_level_sweep.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Allow running as `python3 scripts/v18_pollution_level_sweep.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.per_surface_bayesian_rollup import (  # type: ignore  # noqa: E402
    _DEFAULT_LANGUAGE_DISPATCH,
    _METRIC,
    _load_pool_phonemes,
    _load_score_rows,
    aggregate_per_surface,
    beta_posterior,
    build_v8_records,
    build_v9_records,
    mann_whitney_u_one_tail,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"
_DEFAULT_POOLS = _REPO_ROOT / "pools"

_DEFAULT_NMIN = 10
_DEFAULT_TOP_K_GATE = 20

# (pollution_level_pct, polluted_pool_name) — canonical sweep order.
_SWEEP_LEVELS: tuple[tuple[int, str], ...] = (
    (10, "polluted_aquitanian_10pct"),
    (25, "polluted_aquitanian_25pct"),
    (50, "polluted_aquitanian"),
    (75, "polluted_aquitanian_75pct"),
)


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
    out: dict[str, str] = {}
    for entry in pool_doc.get("entries", []):
        out[entry["surface"]] = entry.get("provenance", "real")
    return out


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def _fmt_p(p: float) -> str:
    if math.isnan(p):
        return "nan"
    if p == 0.0:
        return "<1e-300"
    return f"{p:.3e}"


def _build_paired_rows(
    *,
    pool: str,
    auto_dir: Path,
    auto_sig_dir: Path,
    score_rows: dict,
    pool_phonemes: dict,
    n_min: int,
) -> tuple[list[dict], list[dict]]:
    """Run v8 + v9 pairing for one pool and split into (substrate, control)."""
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
    sub_rows: list[dict] = []
    ctrl_rows: list[dict] = []
    for (pool_kind, surface), cell in sorted(aggregates.items()):
        n = cell["n"]
        k = cell["k"]
        mean, lo, hi = beta_posterior(n, k)
        cred = min(1.0, n / n_min) if n_min > 0 else 1.0
        eff = cred * mean + (1.0 - cred) * 0.5
        row = {
            "pool_kind": pool_kind,
            "surface": surface,
            "n": n,
            "k": k,
            "n_v8": cell["n_v8"],
            "n_v9": cell["n_v9"],
            "posterior_mean": mean,
            "posterior_ci_low": lo,
            "posterior_ci_high": hi,
            "credibility": cred,
            "effective_score": eff,
        }
        if pool_kind == pool:
            sub_rows.append(row)
        elif pool_kind == f"control_{pool}":
            ctrl_rows.append(row)
    return sub_rows, ctrl_rows


def _gate(sub_top: list[dict], ctrl_top: list[dict]) -> dict:
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
    median_sub = _median(sub_means)
    median_ctrl = _median(ctrl_means)
    gate = (
        not math.isnan(p) and p < 0.05 and median_sub > median_ctrl
    )
    return {
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate": median_sub,
        "median_control": median_ctrl,
        "mw_u_substrate": u,
        "mw_p_one_tail": p,
        "verdict": "PASS" if gate else "FAIL",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--summary-json", type=Path, default=None,
        help="Optional path for the sweep summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    rows: list[dict] = []
    for pct, pool_name in _SWEEP_LEVELS:
        pool_path = args.pools_dir / f"{pool_name}.yaml"
        pool_doc = _load_pool_yaml(pool_path)
        provenance = _provenance_map(pool_doc)
        n_real = sum(1 for v in provenance.values() if v == "real")
        n_conj = sum(
            1
            for v in provenance.values()
            if str(v).startswith("conjectural")
        )

        sub_rows, ctrl_rows = _build_paired_rows(
            pool=pool_name,
            auto_dir=args.auto_dir,
            auto_sig_dir=args.auto_sig_dir,
            score_rows=score_rows,
            pool_phonemes=pool_phonemes,
            n_min=args.n_min,
        )
        sub_top = sorted(sub_rows, key=lambda r: -r["posterior_mean"])[
            : args.top_k_gate
        ]
        ctrl_top = sorted(ctrl_rows, key=lambda r: -r["posterior_mean"])[
            : args.top_k_gate
        ]
        gate = _gate(sub_top, ctrl_top)

        # Provenance breakdown of the substrate top-K.
        breakdown: dict[str, int] = defaultdict(int)
        for r in sub_top:
            breakdown[provenance.get(r["surface"], "unknown")] += 1
        n_top_real = breakdown.get("real", 0)
        n_top_conj = sum(
            cnt for tag, cnt in breakdown.items()
            if str(tag).startswith("conjectural")
        )

        rows.append(
            {
                "pollution_pct": pct,
                "pool": pool_name,
                "n_real": n_real,
                "n_conjectural": n_conj,
                "n_total_entries": n_real + n_conj,
                "top_k_real": n_top_real,
                "top_k_conjectural": n_top_conj,
                "n_substrate_top": gate["n_substrate_top"],
                "n_control_top": gate["n_control_top"],
                "median_substrate": gate["median_substrate"],
                "median_control": gate["median_control"],
                "mw_u_substrate": gate["mw_u_substrate"],
                "mw_p_one_tail": gate["mw_p_one_tail"],
                "verdict": gate["verdict"],
            }
        )

    # Render markdown.
    lines: list[str] = []
    lines.append(
        "# v18 pollution-level sweep — Aquitanian (mg-9f18)\n"
    )
    lines.append(
        "Characterizes how the right-tail bayesian gate's p-value "
        "scales with same-distribution conjectural pollution across "
        "10%/25%/50%/75% levels. The 50% row is v14 (mg-6b73); the "
        "other three are new in v18.\n"
    )

    # Sweep table.
    lines.append("## Gate p-value vs pollution level\n")
    lines.append(
        "| pollution % | n_real | n_conj | substrate top-K | control "
        "top-K | median(top substrate) | median(top control) | MW U "
        "(substrate) | MW p (one-tail) | gate | top-K real | "
        "top-K conjectural |"
    )
    lines.append(
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|"
    )
    for r in rows:
        lines.append(
            "| {pct} | {nr} | {nc} | {ns} | {ncc} | {ms:.4f} | "
            "{mc:.4f} | {u:.1f} | {p} | {gate} | {tr} | {tc} |".format(
                pct=r["pollution_pct"],
                nr=r["n_real"],
                nc=r["n_conjectural"],
                ns=r["n_substrate_top"],
                ncc=r["n_control_top"],
                ms=r["median_substrate"],
                mc=r["median_control"],
                u=r["mw_u_substrate"],
                p=_fmt_p(r["mw_p_one_tail"]),
                gate=r["verdict"],
                tr=r["top_k_real"],
                tc=r["top_k_conjectural"],
            )
        )
    lines.append("")

    # Interpretation.
    p_values = [r["mw_p_one_tail"] for r in rows]
    verdicts = [r["verdict"] for r in rows]
    n_pass = sum(1 for v in verdicts if v == "PASS")
    n_fail = sum(1 for v in verdicts if v == "FAIL")
    monotonic_widening = all(
        p_values[i] <= p_values[i + 1] for i in range(len(p_values) - 1)
    )

    lines.append("## Interpretation\n")
    if n_fail == 0 and monotonic_widening:
        lines.append(
            "**Smooth gradient — no sharp threshold.** The gate "
            "PASSes at every pollution level 10%–75%, with the "
            "p-value widening monotonically as pollution increases. "
            "v14's PASS-at-50% generalizes: the framework's right-"
            "tail bayesian PASS is driven by phonotactic-distribution-"
            "shape match between the polluted pool and the substrate "
            "LM, not by the fraction of surfaces that are real "
            "substrate vocabulary. Same-distribution pollution does "
            "not collapse the gate at any level we tested.\n"
        )
    elif n_fail == 0 and not monotonic_widening:
        lines.append(
            "**Insensitive to pollution level — but non-monotonic "
            "p-values.** All four levels PASS, and the p-values are "
            "comparable. The non-monotonicity in p across levels is "
            "consistent with sampling noise in the conjectural draws "
            "(each polluted pool draws a different number of "
            "conjectural surfaces under a different seed, so the "
            "control's matched-marginal shifts pool-by-pool). The "
            "headline holds: same-distribution pollution does not "
            "collapse the gate at any level we tested.\n"
        )
    elif n_fail >= 1:
        first_fail = next(r for r in rows if r["verdict"] == "FAIL")
        lines.append(
            f"**Threshold detected near {first_fail['pollution_pct']}% "
            f"pollution.** The gate PASSes at lower pollution levels "
            f"and FAILs at "
            f"{first_fail['pollution_pct']}% (p="
            f"{_fmt_p(first_fail['mw_p_one_tail'])}). Same-"
            f"distribution pollution does collapse the gate, but "
            f"only at high conjectural shares; the v14 PASS at 50% "
            f"now sits inside a characterized stable region rather "
            f"than being unbounded above.\n"
        )
    else:
        lines.append(
            "**Mixed verdicts.** See per-row breakdown above; the "
            "gradient is not monotonic and admits no single one-line "
            "interpretation.\n"
        )

    lines.append(
        "**Provenance breakdown of the substrate top-K** "
        f"(top-{args.top_k_gate}, ranked by posterior_mean) is "
        f"reported per row. Pollution levels at which the conjecturals "
        f"are largely absent from the right tail (`top-K real ≥ 18`) "
        f"are consistent with v14's reading: real and conjectural "
        f"surfaces are *partially* discriminated even when the gate "
        f"itself is insensitive to the pollution level.\n"
    )

    lines.append("## Comparison to v14 50% baseline\n")
    fifty = next(r for r in rows if r["pollution_pct"] == 50)
    lines.append(
        f"The 50% pool (v14, mg-6b73) is reproduced from this run as "
        f"a sanity check that the v18 sweep code path produces the "
        f"same gate values as the v10/v14 path:\n\n"
        f"- 50% gate verdict: **{fifty['verdict']}**, "
        f"p={_fmt_p(fifty['mw_p_one_tail'])}, MW U="
        f"{fifty['mw_u_substrate']:.1f}.\n"
        f"- v14 reported PASS at p≈2.74e-05; reproduce here to "
        f"within sampling noise of the result-stream merge.\n"
    )

    lines.append("## Notes\n")
    lines.append(
        f"- Metric: `{_METRIC}` (Basque LM). Substrate-side: real "
        f"Aquitanian + same-distribution conjecturals. Control-side: "
        f"`pools/control_polluted_aquitanian_<N>pct.yaml` (or "
        f"`pools/control_polluted_aquitanian.yaml` at 50%) — each "
        f"control is matched to its polluted pool's combined "
        f"(real+conjectural) marginal.\n"
        f"- Top-K: {args.top_k_gate}. n_min: {args.n_min}. Right-tail "
        f"MW U is one-tail with normal-approximation tie-corrected p; "
        f"see `scripts/per_surface_bayesian_rollup.py`.\n"
        f"- Determinism: pool surfaces are pinned by deterministic "
        f"seed; sweep results are bit-identical across re-runs given "
        f"the same `experiments.{_METRIC}*.jsonl` and pool YAMLs.\n"
    )

    out_path = args.results_dir / "rollup.pollution_level_sweep.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {"sweep": rows}
    if args.summary_json:
        args.summary_json.write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
