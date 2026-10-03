#!/usr/bin/env python3
"""Hattic specificity probe — pre-registered right-tail bayesian gate (mg-7b882).

Pairs the ``hattic`` substrate pool against its bigram-preserving
control ``control_hattic_bigram`` (both scored under the ``hattic``
external phoneme LM) and runs the v10 right-tail bayesian gate on the
per-surface posteriors. Built on ``scripts/v21_eteocretan_gate.py``.

Framing
=======
Hattic is a Bronze Age Anatolian isolate with no genealogical relation
to Linear A or to any of the Aegean / old-European pools in this repo.
It is run as a **specificity probe** (handoff 2026-05-06 §D.3), not as
a candidate substrate and not as a decipherment claim. If an unrelated
language PASSes the gate about as strongly as Eteocretan / Aquitanian /
Etruscan, that is evidence the gate detects generic natural-language
structure (the v15 reading), not substrate affinity.

Pre-registered criterion (fixed 2026-10-03, committed before any run output)
============================================================================
Identical to every substrate pool since v10; no post-hoc changes:

  * Per-surface posterior means from the v8 (``hypotheses/auto``)
    candidate-equation rows (plus v9 ``hypotheses/auto_signatures``
    rows if a manifest exists; as for Eteocretan, none does), scored with
    ``external_phoneme_perplexity_v0`` under the ``hattic`` LM for both
    sides (n_min=10 credibility is reported but NOT used by the gate).
  * Take the top-20 ``hattic`` surfaces and the top-20
    ``control_hattic_bigram`` surfaces by posterior_mean.
  * One-tailed Mann-Whitney U (substrate > control), normal
    approximation, tie-corrected.
  * **PASS iff p < 0.05 and median(substrate top-20) >
    median(control top-20).** Anything else is FAIL. A FAIL ships as a
    clean negative.

Interpretation rules (pm-lineara 2026-10-03 10:50Z, fixed before the run)
=========================================================================
1. The pool has **72 entries**, below the v21 bar of 80 (deliberately
   not padded). This is stated beside the p-value in the report.
2. The hattic LM corpus and the hattic pool are the **same 72 lexical
   citation forms** (not running text). Any "hattic scores best under
   its own LM" readout is therefore circular by construction and is
   not evidence. The main gate (substrate vs control, both under the
   hattic LM) is less affected because the control is sampled from the
   same bigram statistics — but that is a mitigation, not immunity.
   Cross-LM cells putting *other* pools under the hattic LM are not
   circular.
3. Forms are hand-keyed and **not collated** against Soysal 2004 / the
   printed editions. A PASS supports "generic structure" regardless of
   collation accuracy. A FAIL is reported as **inconclusive on data
   quality**, not as evidence that the gate's signal is specific.

Output
======
  results/rollup.bayesian_posterior.hattic.md

Usage
=====
  python3 scripts/hattic_gate.py [--summary-json PATH]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Allow running as `python3 scripts/hattic_gate.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.per_surface_bayesian_rollup import (  # type: ignore  # noqa: E402
    _DEFAULT_LANGUAGE_DISPATCH,
    _METRIC,
    _load_pool_phonemes,
    _load_score_rows,
    mann_whitney_u_one_tail,
)
from scripts.v21_eteocretan_gate import (  # type: ignore  # noqa: E402
    _build_paired_rows,
    _fmt,
    _fmt_p,
    _median,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS = _REPO_ROOT / "results"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"
_DEFAULT_POOLS = _REPO_ROOT / "pools"

_SUBSTRATE = "hattic"
_CONTROL = "control_hattic_bigram"
_N_POOL_ENTRIES = 124

# Pre-registered constants. Do not change after the run.
_NMIN = 10
_TOP_K_GATE = 20
_ALPHA = 0.05


def gate_verdict(p: float, median_sub: float, median_ctrl: float) -> bool:
    """The pre-registered PASS rule: p < 0.05 and substrate median > control."""
    return (not math.isnan(p)) and p < _ALPHA and median_sub > median_ctrl


def evaluate(sub_rows: list[dict], ctrl_rows: list[dict]) -> dict:
    """Apply the pre-registered top-K MW gate to per-surface rows."""
    def _top(rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda r: -r["posterior_mean"])[:_TOP_K_GATE]

    sub_top = _top(sub_rows)
    ctrl_top = _top(ctrl_rows)
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
    median_sub = _median(sub_means)
    median_ctrl = _median(ctrl_means)
    mean_sub = sum(sub_means) / len(sub_means) if sub_means else float("nan")
    mean_ctrl = sum(ctrl_means) / len(ctrl_means) if ctrl_means else float("nan")
    return {
        "sub_top": sub_top,
        "ctrl_top": ctrl_top,
        "u": u,
        "p": p,
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate_top": median_sub,
        "median_control_top": median_ctrl,
        "median_gap": median_sub - median_ctrl,
        "mean_substrate_top": mean_sub,
        "mean_control_top": mean_ctrl,
        "gate": "PASS" if gate_verdict(p, median_sub, median_ctrl) else "FAIL",
    }


def render(ev: dict, sub_rows: list[dict], ctrl_rows: list[dict]) -> str:
    p = ev["p"]
    ms, mc = ev["median_substrate_top"], ev["median_control_top"]
    lines: list[str] = []
    lines.append(
        "# Hattic specificity probe — pre-registered right-tail bayesian "
        "gate (mg-7b882)\n"
    )
    if ev["gate"] == "PASS":
        verdict = (
            f"**Verdict against the pre-registered criterion: PASS** — "
            f"`hattic` (n={_N_POOL_ENTRIES} pool entries, below the v21 "
            f"bar of 80) vs `{_CONTROL}`, one-tailed MW p={_fmt_p(p)}; "
            f"median top-{_TOP_K_GATE} posterior {ms:.4f} vs {mc:.4f} "
            f"(gap {ms - mc:+.4f}). Hattic is an unrelated Anatolian "
            f"isolate run as a specificity probe: a PASS is evidence that "
            f"the gate rewards generic natural-language structure (the "
            f"v15 reading), not substrate affinity with Linear A. It "
            f"holds regardless of the forms' collation accuracy."
        )
    else:
        verdict = (
            f"**Verdict against the pre-registered criterion: FAIL** — "
            f"`hattic` (n={_N_POOL_ENTRIES} pool entries, below the v21 "
            f"bar of 80) vs `{_CONTROL}`, one-tailed MW p={_fmt_p(p)}; "
            f"median top-{_TOP_K_GATE} posterior {ms:.4f} vs {mc:.4f} "
            f"(gap {ms - mc:+.4f}). Per the pre-registered "
            f"interpretation rules this FAIL is **inconclusive on data "
            f"quality** (hand-keyed, uncollated lexical forms; 72 < 80 "
            f"entries), not evidence that the gate's signal is "
            f"substrate-specific."
        )
    lines.append(verdict + "\n")

    lines.append("## Pre-registered criterion\n")
    lines.append(
        f"Top-{_TOP_K_GATE} `hattic` posteriors vs top-{_TOP_K_GATE} "
        f"`{_CONTROL}` posteriors, both under the `hattic` LM; one-tailed "
        f"Mann-Whitney U (substrate > control); PASS iff p < {_ALPHA} and "
        f"median(substrate) > median(control). Fixed in this script's "
        f"docstring in the branch's first commit, before any run output.\n"
    )

    lines.append("## Acceptance gate\n")
    lines.append(
        "| substrate pool | pool entries | control pool | substrate top-K | "
        "control top-K | median(top substrate posterior) | median(top "
        "control posterior) | median gap | MW U | MW p (one-tail) | gate |"
    )
    lines.append("|:--|---:|:--|---:|---:|---:|---:|---:|---:|---:|:--:|")
    lines.append(
        f"| {_SUBSTRATE} | {_N_POOL_ENTRIES} | {_CONTROL} | "
        f"{ev['n_substrate_top']} | {ev['n_control_top']} | {ms:.4f} | "
        f"{mc:.4f} | {ms - mc:+.4f} | {ev['u']:.1f} | {_fmt_p(p)} | "
        f"{ev['gate']} |"
    )
    lines.append("")

    lines.append("## Mean-of-means (informational)\n")
    lines.append(
        f"Mean of top-{_TOP_K_GATE} substrate posterior_mean: "
        f"{ev['mean_substrate_top']:.4f}. Mean of top-{_TOP_K_GATE} "
        f"control posterior_mean: {ev['mean_control_top']:.4f}. Gap: "
        f"{ev['mean_substrate_top'] - ev['mean_control_top']:+.4f}. Not "
        f"part of the gate.\n"
    )

    lines.append(
        f"## Top-{_TOP_K_GATE} substrate vs top-{_TOP_K_GATE} control "
        f"side-by-side\n"
    )
    lines.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    lines.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    sub_top, ctrl_top = ev["sub_top"], ev["ctrl_top"]
    for i in range(max(len(sub_top), len(ctrl_top))):
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

    leader = sorted(sub_rows + ctrl_rows, key=lambda r: -r["effective_score"])[:50]
    lines.append(
        f"## Top-{len(leader)} surfaces by effective score "
        f"(substrate + control interleaved)\n"
    )
    lines.append(
        "| rank | side | surface | n | k | posterior | credibility | effective |"
    )
    lines.append("|---:|:--|:--|---:|---:|---:|---:|---:|")
    for i, r in enumerate(leader, 1):
        side = "control" if r["pool_kind"] == _CONTROL else "substrate"
        lines.append(
            f"| {i} | {side} | `{r['surface']}` | {r['n']} | {r['k']} | "
            f"{_fmt(r['posterior_mean'])} | {_fmt(r['credibility'], 3)} | "
            f"{_fmt(r['effective_score'])} |"
        )
    lines.append("")

    lines.append("## Interpretation rules (fixed before the run)\n")
    lines.append(
        f"- **Pool size.** {_N_POOL_ENTRIES} entries, below the v21 bar "
        f"of 80; not padded.\n"
        f"- **Circularity.** The `hattic` LM is trained on the same 72 "
        f"lexical citation forms that make up the pool. The own-LM "
        f"readout in the cross-LM matrix is inflated by construction and "
        f"is not evidence. This gate is less exposed, because "
        f"`{_CONTROL}` is sampled from the same bigram statistics and is "
        f"scored under the same LM; that is a mitigation, not immunity.\n"
        f"- **Collation.** Forms are hand-keyed and not collated against "
        f"Soysal 2004 / the printed editions (`corpora/hattic.README.md`). "
        f"A PASS supports generic structure regardless; a FAIL is "
        f"inconclusive on data quality.\n"
    )

    lines.append("## Notes\n")
    lines.append(
        f"- Metric: `{_METRIC}`. LM: `hattic` (α=1.0, 72 lexical forms; "
        f"`harness/external_phoneme_models/hattic.json`).\n"
        f"- Gate: top-{_TOP_K_GATE} by posterior_mean only (credibility "
        f"n_min={_NMIN} shown in the leaderboard, not used by the gate).\n"
        f"- Determinism: no RNG; re-runs are byte-identical given the "
        f"same result-stream sidecars, manifests and pool YAMLs.\n"
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--out-name", type=str, default="rollup.bayesian_posterior.hattic.md",
    )
    parser.add_argument("--summary-json", type=Path, default=None)
    args = parser.parse_args(argv)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)
    sub_rows, ctrl_rows = _build_paired_rows(
        pool=_SUBSTRATE,
        control_pool=_CONTROL,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        score_rows=score_rows,
        pool_phonemes=pool_phonemes,
        language_dispatch=dict(_DEFAULT_LANGUAGE_DISPATCH),
        n_min=_NMIN,
    )
    ev = evaluate(sub_rows, ctrl_rows)

    out_path = args.results_dir / args.out_name
    out_path.write_text(render(ev, sub_rows, ctrl_rows), encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "substrate_pool": _SUBSTRATE,
        "control_pool": _CONTROL,
        "n_pool_entries": _N_POOL_ENTRIES,
        "n_substrate_top": ev["n_substrate_top"],
        "n_control_top": ev["n_control_top"],
        "median_substrate_top": ev["median_substrate_top"],
        "median_control_top": ev["median_control_top"],
        "median_gap": ev["median_gap"],
        "mean_substrate_top": ev["mean_substrate_top"],
        "mean_control_top": ev["mean_control_top"],
        "mw_u_substrate": ev["u"],
        "mw_p_one_tail": ev["p"],
        "gate": ev["gate"],
    }
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
