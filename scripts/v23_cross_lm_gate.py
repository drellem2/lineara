#!/usr/bin/env python3
"""v23 generic cross-LM right-tail bayesian gate runner (mg-b599).

Generalises v21_eteocretan_gate.py to an arbitrary
``(substrate_pool, control_pool, language_dispatch)`` combination so
the v23 cross-LM matrix can be filled with one tool. The script:

* Pairs the substrate pool against the named control pool (default
  ``control_<substrate>``; pass ``--control`` to override).
* Resolves each side's LM via ``language_dispatch`` (defaults to the
  same-LM table; pass ``--language-dispatch`` JSON to swap LMs).
* Computes the v10 right-tail bayesian gate (top-K Mann-Whitney U on
  per-surface posterior means) and writes a per-pool markdown report
  + optional summary JSON.

Output naming follows the v18 / v21 / v23 convention:
``rollup.bayesian_posterior.<substrate>.<lm-suffix>.md``.

Usage
=====
    # eteocretan substrate under Mycenaean Greek LM
    python3 scripts/v23_cross_lm_gate.py \\
        --substrate eteocretan --control control_eteocretan_bigram \\
        --language-dispatch '{"eteocretan":"mycenaean_greek","control_eteocretan_bigram":"mycenaean_greek"}' \\
        --out-name rollup.bayesian_posterior.eteocretan.under_mg_lm.md \\
        --title-suffix " — under Mycenaean Greek LM (cross-LM negative control)" \\
        --lm-label "Mycenaean Greek"

    # toponym substrate (paired against bigram-preserving control) under Eteocretan LM
    python3 scripts/v23_cross_lm_gate.py \\
        --substrate toponym --control control_toponym_bigram \\
        --language-dispatch '{"toponym":"eteocretan","control_toponym_bigram":"eteocretan"}' \\
        --out-name rollup.bayesian_posterior.toponym.under_eteocretan_lm.md \\
        --title-suffix " — under Eteocretan LM (cross-LM check)" \\
        --lm-label "Eteocretan"
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Allow running as `python3 scripts/v23_cross_lm_gate.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


def _fmt(x: float, w: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "  nan"
    return f"{x:.{w}f}"


def _build_paired_rows(
    *,
    pool: str,
    control_pool: str,
    auto_dir: Path,
    auto_sig_dir: Path,
    score_rows: dict,
    pool_phonemes: dict,
    language_dispatch: dict[str, str],
    n_min: int,
) -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    records.extend(
        build_v8_records(
            pool=pool,
            auto_dir=auto_dir,
            score_rows=score_rows,
            pool_phonemes=pool_phonemes,
            language_dispatch=language_dispatch,
            control_pool=control_pool,
        )
    )
    records.extend(
        build_v9_records(
            pool=pool,
            auto_dir=auto_sig_dir,
            score_rows=score_rows,
            language_dispatch=language_dispatch,
            control_pool=control_pool,
        )
    )

    aggregates = aggregate_per_surface(records)
    substrate_rows: list[dict] = []
    control_rows: list[dict] = []
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
            substrate_rows.append(row)
        elif pool_kind == control_pool:
            control_rows.append(row)
    return substrate_rows, control_rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument("--substrate", required=True)
    parser.add_argument(
        "--control", default=None,
        help="Control pool (default ``control_<substrate>``).",
    )
    parser.add_argument(
        "--language-dispatch", type=str, default=None,
        help=(
            "JSON object mapping pool name → external phoneme LM name. "
            "Overrides the same-LM default for this run; required for "
            "cross-LM cells."
        ),
    )
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--out-name", type=str, required=True,
        help="Filename of the markdown report under --results-dir.",
    )
    parser.add_argument(
        "--title-suffix", type=str, default="",
        help="Suffix appended to the markdown title.",
    )
    parser.add_argument(
        "--lm-label", type=str, default="",
        help=(
            "Human-readable label for the LM under which both sides "
            "are scored (e.g. 'Mycenaean Greek', 'Eteocretan'). Used "
            "only in the rendered narrative."
        ),
    )
    parser.add_argument(
        "--summary-json", type=Path, default=None,
        help="Optional path for the gate summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    control = args.control or f"control_{args.substrate}"

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    if args.language_dispatch:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)
        language_dispatch.update(json.loads(args.language_dispatch))
    else:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    sub_lang = language_dispatch.get(args.substrate, "")
    ctrl_lang = language_dispatch.get(control, sub_lang)
    if sub_lang != ctrl_lang:
        # Mixed-LM gate is not a supported configuration: paired_diff
        # only cancels the LM out when both sides score under the
        # same LM. Refuse rather than silently producing a meaningless
        # result.
        raise ValueError(
            f"substrate ({args.substrate!r} → {sub_lang!r}) and "
            f"control ({control!r} → {ctrl_lang!r}) are dispatched "
            f"to different LMs; cross-LM gate requires both sides on "
            f"the same LM"
        )

    sub_rows, ctrl_rows = _build_paired_rows(
        pool=args.substrate,
        control_pool=control,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        language_dispatch=language_dispatch,
        n_min=args.n_min,
    )

    def _top(rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda r: -r["posterior_mean"])[: args.top_k_gate]

    sub_top = _top(sub_rows)
    ctrl_top = _top(ctrl_rows)

    u, p, na, nb = mann_whitney_u_one_tail(
        [r["posterior_mean"] for r in sub_top],
        [r["posterior_mean"] for r in ctrl_top],
    )
    median_sub = _median([r["posterior_mean"] for r in sub_top])
    median_ctrl = _median([r["posterior_mean"] for r in ctrl_top])
    gate = (not math.isnan(p)) and p < 0.05 and median_sub > median_ctrl
    gate_str = "PASS" if gate else "FAIL"

    mean_sub = (
        sum(r["posterior_mean"] for r in sub_top) / len(sub_top)
        if sub_top else float("nan")
    )
    mean_ctrl = (
        sum(r["posterior_mean"] for r in ctrl_top) / len(ctrl_top)
        if ctrl_top else float("nan")
    )
    median_gap = median_sub - median_ctrl

    lm_label = args.lm_label or sub_lang or "<unknown>"

    lines: list[str] = []
    lines.append(
        f"# v23 cross-LM gate — {args.substrate} substrate under "
        f"{lm_label} LM (mg-b599){args.title_suffix}\n"
    )
    if gate:
        verdict = (
            f"**Headline: the {args.substrate} substrate pool PASSes "
            f"the v10 right-tail bayesian gate against {control} when "
            f"both sides are scored under the {lm_label} LM at "
            f"p={_fmt_p(p)}** (median substrate posterior "
            f"{median_sub:.4f} vs median control posterior "
            f"{median_ctrl:.4f}; gap {median_gap:+.4f})."
        )
    else:
        verdict = (
            f"**Headline: the {args.substrate} substrate pool FAILs "
            f"the v10 right-tail bayesian gate against {control} when "
            f"both sides are scored under the {lm_label} LM at "
            f"p={_fmt_p(p)}** (median substrate posterior "
            f"{median_sub:.4f} vs median control posterior "
            f"{median_ctrl:.4f}; gap {median_gap:+.4f}). The "
            f"substrate-vs-control posterior median ordering does not "
            f"clear the gate under this LM."
        )
    lines.append(verdict + "\n")

    lines.append("## Acceptance gate\n")
    lines.append(
        "| substrate pool | control pool | LM | substrate top-K | "
        "control top-K | median(top substrate posterior) | "
        "median(top control posterior) | MW U (substrate) | "
        "MW p (one-tail, substrate>control) | gate |"
    )
    lines.append("|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|")
    lines.append(
        "| {sub} | {ctrl} | {lm} | {ns} | {nc} | {mss:.4f} | "
        "{msc:.4f} | {u:.1f} | {p} | {gate} |".format(
            sub=args.substrate, ctrl=control, lm=lm_label,
            ns=na, nc=nb,
            mss=median_sub, msc=median_ctrl,
            u=u, p=_fmt_p(p),
            gate=gate_str,
        )
    )
    lines.append("")

    lines.append("## Mean-of-means (informational)\n")
    lines.append(
        f"Mean of top-{args.top_k_gate} substrate posterior_mean: "
        f"{mean_sub:.4f}. "
        f"Mean of top-{args.top_k_gate} control posterior_mean: "
        f"{mean_ctrl:.4f}. "
        f"Gap (median, gate-relevant): {median_gap:+.4f}; "
        f"gap (mean): {mean_sub - mean_ctrl:+.4f}. The gate uses the "
        f"rank-based MW U test rather than the mean gap, so this "
        f"number is shown for orientation only.\n"
    )

    lines.append(
        f"## Top-{args.top_k_gate} substrate vs top-{args.top_k_gate} "
        f"control side-by-side\n"
    )
    lines.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    lines.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    pad = max(len(sub_top), len(ctrl_top))
    for i in range(pad):
        s = sub_top[i] if i < len(sub_top) else None
        c = ctrl_top[i] if i < len(ctrl_top) else None
        lines.append(
            "| {r} | {ss} | {sn} | {sk} | {sm} | {cs} | {cn} | {ck} | {cm} |".format(
                r=i + 1,
                ss=f"`{s['surface']}`" if s else "—",
                sn=s["n"] if s else "—",
                sk=s["k"] if s else "—",
                sm=_fmt(s["posterior_mean"]) if s else "—",
                cs=f"`{c['surface']}`" if c else "—",
                cn=c["n"] if c else "—",
                ck=c["k"] if c else "—",
                cm=_fmt(c["posterior_mean"]) if c else "—",
            )
        )
    lines.append("")

    all_rows = sub_rows + ctrl_rows
    leader = sorted(all_rows, key=lambda r: -r["effective_score"])[:50]
    lines.append(
        f"## Top-{len(leader)} surfaces by effective score "
        f"(substrate + control interleaved)\n"
    )
    lines.append(
        "| rank | side | surface | n | k | posterior | credibility | "
        "effective |"
    )
    lines.append("|---:|:--|:--|---:|---:|---:|---:|---:|")
    for i, r in enumerate(leader, 1):
        side = "control" if r["pool_kind"] == control else "substrate"
        lines.append(
            "| {r} | {side} | `{surface}` | {n} | {k} | {m} | {c} | {e} |".format(
                r=i, side=side, surface=r["surface"],
                n=r["n"], k=r["k"],
                m=_fmt(r["posterior_mean"]),
                c=_fmt(r["credibility"], 3),
                e=_fmt(r["effective_score"]),
            )
        )
    lines.append("")

    lines.append("## Notes\n")
    lines.append(
        f"- Metric: `{_METRIC}`. LM: `{sub_lang}` "
        f"(label: {lm_label}). Substrate pool: `{args.substrate}` "
        f"({na} top surfaces). Control pool: `{control}` "
        f"({nb} top surfaces).\n"
        f"- Gate: top-{args.top_k_gate} by posterior_mean only "
        f"(no credibility shrinkage); one-tail Mann-Whitney U with "
        f"normal-approximation tie-corrected p-value. PASS at p<0.05 "
        f"with median(substrate top-K) > median(control top-K).\n"
        f"- Determinism: identical rows across re-runs given the "
        f"same `experiments.{_METRIC}*.jsonl`, the substrate / "
        f"control manifests, and the pool YAMLs. No RNG.\n"
    )

    out_path = args.results_dir / args.out_name
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "substrate_pool": args.substrate,
        "control_pool": control,
        "lm": sub_lang,
        "lm_label": lm_label,
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate_top": median_sub,
        "median_control_top": median_ctrl,
        "median_gap": median_gap,
        "mean_substrate_top": mean_sub,
        "mean_control_top": mean_ctrl,
        "mean_gap": mean_sub - mean_ctrl,
        "mw_u_substrate": u,
        "mw_p_one_tail": p,
        "gate": gate_str,
    }
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
