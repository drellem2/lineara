#!/usr/bin/env python3
"""v18 toponym pool re-evaluation under bigram-preserving control (mg-9f18).

Pairs the substrate ``toponym`` pool against the bigram-preserving
control pool ``control_toponym_bigram`` (built by the v18 sampler in
``scripts/build_control_pools.py``) and runs the v10 right-tail bayesian
gate on the per-surface posteriors.

Background
==========
v10 (mg-d26d) found that the toponym pool **failed** the right-tail gate
at p=0.92, dominated by control surfaces like ``eoao``, ``aathei``, and
``kllzua`` that the Basque LM scored extremely well by raw phoneme-
frequency match. The v6 control sampler draws each phoneme independently
from the substrate's marginal histogram, so it can produce arbitrarily
extreme phonotactic violations as long as the phoneme inventory is
matched. mg-7ecb's polecat flagged this as the most likely cause of the
toponym failure: *"a bigram-preserving control would tighten the gate
further."*

v18 (mg-9f18) tests that hypothesis. The bigram-preserving sampler in
``build_control_pools.py --sampler bigram`` draws each control phoneme
conditional on the previous phoneme using the substrate's bigram
counts (Laplace alpha=0.1), so the realized control surfaces inherit
the substrate's adjacent-phoneme structure rather than just its marginal
histogram. The bigram pool ``pools/control_toponym_bigram.yaml``
replaces strings like ``eoao`` with surfaces like ``akaintha`` and
``inaletos`` that respect Greek-style CV transitions.

Two outcomes are possible:

  * **Toponym now PASSes (p < 0.05).** The v10 failure was a control-
    sampler artifact: the framework genuinely detects substrate-LM-
    phonotactic kinship in the toponym pool, but the unigram control
    was *too phonotactically extreme* (over-flattering itself under the
    LM). The toponym pool joins Aquitanian + Etruscan as a third
    validated cross-LM-checkable pool.
  * **Toponym still FAILs.** The failure is deeper than control-sampler
    choice: even a phonotactically-realistic control out-scores the
    substrate, which means the substrate signal in the toponym pool is
    weaker than in Aquitanian/Etruscan (perhaps because Greek-style
    toponym surfaces drift toward LM-preferred phoneme distributions
    intrinsically — the polecat noted this as a fallback explanation).

Output
======
  results/rollup.bayesian_posterior.toponym_bigram_control.md

Re-runs are deterministic given the result stream and the manifests.

Usage
=====
  python3 scripts/v18_toponym_bigram_gate.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

# Allow running as `python3 scripts/v18_toponym_bigram_gate.py`.
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

_DEFAULT_SUBSTRATE = "toponym"
_DEFAULT_BIGRAM_CONTROL = "control_toponym_bigram"
_DEFAULT_UNIGRAM_CONTROL = "control_toponym"
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
    """Run the v8 + v9 pairing for one (substrate, control) combination
    and return ``(substrate_rows, control_rows)``.

    Each row is ``{surface, n, k, posterior_mean, posterior_ci_low,
    posterior_ci_high, credibility, effective_score}``. The substrate
    rows track ``pool``; the control rows track ``control_pool``.
    """
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
    parser.add_argument("--substrate", default=_DEFAULT_SUBSTRATE)
    parser.add_argument(
        "--bigram-control", default=_DEFAULT_BIGRAM_CONTROL,
        help="Bigram-preserving matched control pool name (mg-9f18).",
    )
    parser.add_argument(
        "--unigram-control", default=_DEFAULT_UNIGRAM_CONTROL,
        help=(
            "Legacy unigram-marginal matched control pool (mg-f419). "
            "The rollup includes a unigram-vs-bigram comparison block "
            "side-by-side with the v18 gate."
        ),
    )
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--summary-json", type=Path, default=None,
        help="Optional path for the gate summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    sub_rows_bigram, ctrl_rows_bigram = _build_paired_rows(
        pool=args.substrate,
        control_pool=args.bigram_control,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        language_dispatch=_DEFAULT_LANGUAGE_DISPATCH,
        n_min=args.n_min,
    )
    sub_rows_unigram, ctrl_rows_unigram = _build_paired_rows(
        pool=args.substrate,
        control_pool=args.unigram_control,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        language_dispatch=_DEFAULT_LANGUAGE_DISPATCH,
        n_min=args.n_min,
    )

    # Top-K right-tail by posterior_mean only (matches v10 gate
    # convention; credibility shrinkage drives the leaderboard, not the
    # gate).
    def _top(rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda r: -r["posterior_mean"])[: args.top_k_gate]

    sub_top_b = _top(sub_rows_bigram)
    ctrl_top_b = _top(ctrl_rows_bigram)
    sub_top_u = _top(sub_rows_unigram)
    ctrl_top_u = _top(ctrl_rows_unigram)

    u_b, p_b, na_b, nb_b = mann_whitney_u_one_tail(
        [r["posterior_mean"] for r in sub_top_b],
        [r["posterior_mean"] for r in ctrl_top_b],
    )
    u_u, p_u, na_u, nb_u = mann_whitney_u_one_tail(
        [r["posterior_mean"] for r in sub_top_u],
        [r["posterior_mean"] for r in ctrl_top_u],
    )

    median_sub_b = _median([r["posterior_mean"] for r in sub_top_b])
    median_ctrl_b = _median([r["posterior_mean"] for r in ctrl_top_b])
    median_sub_u = _median([r["posterior_mean"] for r in sub_top_u])
    median_ctrl_u = _median([r["posterior_mean"] for r in ctrl_top_u])
    gate_b = (
        not math.isnan(p_b) and p_b < 0.05 and median_sub_b > median_ctrl_b
    )
    gate_u = (
        not math.isnan(p_u) and p_u < 0.05 and median_sub_u > median_ctrl_u
    )

    # Render markdown.
    lines: list[str] = []
    lines.append(
        "# v18 toponym pool — bigram-preserving control gate (mg-9f18)\n"
    )
    if gate_b:
        verdict = (
            "**Headline: the toponym pool PASSes the v10 right-tail "
            "bayesian gate against the bigram-preserving control.** "
            "v10's toponym failure was a control-sampler artifact — "
            "the v6 unigram-marginal control produced phonotactically "
            "extreme surfaces (`eoao`, `aathei`, `kllzua`) that the "
            "Basque LM scored well by raw phoneme-frequency match. "
            "Replacing it with a bigram-preserving control "
            "tightens the gate enough that the substrate signal in "
            "real toponym roots clears the right-tail comparison. The "
            "toponym pool now joins Aquitanian + Etruscan as a third "
            "validated cross-LM-checkable substrate pool."
        )
    else:
        verdict = (
            "**Headline: the toponym pool still FAILs the v10 right-"
            "tail bayesian gate, even against the bigram-preserving "
            "control.** Tightening the control's phonotactic match "
            "from unigram to bigram does not flip the verdict; the "
            "toponym pool's failure has a deeper cause than the "
            "control-sampler choice. The most likely remaining "
            "explanation (per mg-d26d / mg-7ecb fallback): real "
            "Greek-style toponym surfaces drift toward LM-preferred "
            "phoneme distributions intrinsically, so the substrate-vs-"
            "control gap is small even when the control respects "
            "natural phonotactics. The toponym pool's place in §5 "
            "Limitations stands."
        )
    lines.append(verdict + "\n")

    lines.append("## Acceptance gate (v18 vs v10)\n")
    lines.append(
        "| variant | substrate top-K | control top-K | "
        "median(top substrate posterior) | "
        "median(top control posterior) | MW U (substrate) | "
        "MW p (one-tail, substrate>control) | gate |"
    )
    lines.append("|:--|---:|---:|---:|---:|---:|---:|:--:|")
    lines.append(
        "| bigram (v18) | {ns} | {nc} | {mss:.4f} | {msc:.4f} | "
        "{u:.1f} | {p} | {gate} |".format(
            ns=na_b, nc=nb_b,
            mss=median_sub_b, msc=median_ctrl_b,
            u=u_b, p=_fmt_p(p_b),
            gate="PASS" if gate_b else "FAIL",
        )
    )
    lines.append(
        "| unigram (v6/v10) | {ns} | {nc} | {mss:.4f} | {msc:.4f} | "
        "{u:.1f} | {p} | {gate} |".format(
            ns=na_u, nc=nb_u,
            mss=median_sub_u, msc=median_ctrl_u,
            u=u_u, p=_fmt_p(p_u),
            gate="PASS" if gate_u else "FAIL",
        )
    )
    lines.append("")

    # Side-by-side top-K with both controls.
    lines.append(
        f"## Top-{args.top_k_gate} substrate vs top-{args.top_k_gate} "
        f"control side-by-side (v18 bigram-preserving control)\n"
    )
    lines.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    lines.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    pad = max(len(sub_top_b), len(ctrl_top_b))
    for i in range(pad):
        s = sub_top_b[i] if i < len(sub_top_b) else None
        c = ctrl_top_b[i] if i < len(ctrl_top_b) else None
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

    lines.append(
        f"## Side-by-side: v6 unigram control top-{args.top_k_gate} "
        f"(reproduced from mg-d26d for comparison)\n"
    )
    lines.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    lines.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    pad_u = max(len(sub_top_u), len(ctrl_top_u))
    for i in range(pad_u):
        s = sub_top_u[i] if i < len(sub_top_u) else None
        c = ctrl_top_u[i] if i < len(ctrl_top_u) else None
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

    # Diagnostic: which extreme v6 control surfaces are absent under bigram?
    extreme_unigram = {r["surface"] for r in ctrl_top_u}
    extreme_bigram = {r["surface"] for r in ctrl_top_b}
    dropped = sorted(extreme_unigram - extreme_bigram)
    added = sorted(extreme_bigram - extreme_unigram)
    lines.append("## Control top-K composition shift\n")
    lines.append(
        "Surfaces in the v6 unigram control top-K that are **absent** "
        "from the v18 bigram control top-K:\n"
    )
    if dropped:
        lines.append("- " + "\n- ".join(f"`{s}`" for s in dropped))
    else:
        lines.append("- _(none — all unigram top-K surfaces survive)_")
    lines.append("")
    lines.append(
        "Surfaces in the v18 bigram control top-K that are **new** "
        "(absent from the v6 unigram control top-K):\n"
    )
    if added:
        lines.append("- " + "\n- ".join(f"`{s}`" for s in added))
    else:
        lines.append("- _(none — all bigram top-K surfaces appeared under unigram too)_")
    lines.append("")

    lines.append("## Notes\n")
    lines.append(
        f"- Metric: `{_METRIC}` (Basque LM). Substrate pool: "
        f"`{args.substrate}`. Bigram control: "
        f"`{args.bigram_control}`. Unigram control: "
        f"`{args.unigram_control}`.\n"
        f"- Top-K: {args.top_k_gate}. n_min: {args.n_min}. Right-tail "
        f"MW U is one-tail with normal-approximation tie-corrected p; "
        f"see `scripts/per_surface_bayesian_rollup.py`.\n"
        f"- Determinism: identical rows + posterior + p across re-runs "
        f"given the same `experiments.{_METRIC}*.jsonl`, "
        f"`hypotheses/auto/{args.substrate}.manifest.jsonl`, and "
        f"`hypotheses/auto/{{control_pool}}.manifest.jsonl`. No RNG.\n"
    )

    out_path = (
        args.results_dir / "rollup.bayesian_posterior.toponym_bigram_control.md"
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "substrate_pool": args.substrate,
        "bigram_control": args.bigram_control,
        "unigram_control": args.unigram_control,
        "bigram_gate_p": p_b,
        "bigram_gate_u": u_b,
        "bigram_gate_verdict": "PASS" if gate_b else "FAIL",
        "bigram_median_substrate": median_sub_b,
        "bigram_median_control": median_ctrl_b,
        "unigram_gate_p": p_u,
        "unigram_gate_u": u_u,
        "unigram_gate_verdict": "PASS" if gate_u else "FAIL",
        "unigram_median_substrate": median_sub_u,
        "unigram_median_control": median_ctrl_u,
        "control_top_k_unigram_only": dropped,
        "control_top_k_bigram_only": added,
    }
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
