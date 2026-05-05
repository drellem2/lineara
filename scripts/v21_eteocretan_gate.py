#!/usr/bin/env python3
"""v21 Eteocretan substrate pool — right-tail bayesian gate (mg-6ccd).

Pairs the substrate ``eteocretan`` pool against the bigram-preserving
control pool ``control_eteocretan_bigram`` and runs the v10 right-tail
bayesian gate on the per-surface posteriors.

The v18 (mg-9f18) toponym work made bigram-preserving controls the
production default for new pools — Eteocretan inherits that as the
sole matched-control comparison (no legacy v6 unigram pool exists for
Eteocretan).

Background
==========
Eteocretan is the 4th external-validation candidate substrate after
Aquitanian (PASS), Etruscan (PASS), and toponym (PASS under v18
bigram-preserving control). Its uniquely-strong a-priori position:
scholarly consensus treats Eteocretan as the linguistic descendant
of whatever underlies Linear A — the closest-genealogical-relative
candidate. If substrate-LM-phonotactic kinship between a candidate
substrate and Linear A is meaningful, Eteocretan should produce the
cleanest signal.

Both gate outcomes are publishable:
  * **PASS** — 4th external-validation point with the strongest
    a-priori support. The PASS magnitude relative to Aquitanian /
    Etruscan / toponym becomes the headline finding (does the
    closest-relative hypothesis produce stronger signal?).
  * **FAIL** — the most informative outcome. If the closest-relative
    substrate hypothesis fails the gate, the framework's PASS on
    Aquitanian / Etruscan is harder to interpret as "substrate
    continuity detection." Forces a rewrite of the methodology
    paper's interpretive framing.

Per-LM caveat: the Eteocretan LM is built from a small, fragmentary
corpus (~87 unique word forms, α=1.0 smoothing), so it is noisier
than the Basque / Mycenaean-Greek / Etruscan LMs used in v8-v18.
Whether that noise floor swamps the gate is a v21 finding.

Output
======
  results/rollup.bayesian_posterior.eteocretan.md

Re-runs are deterministic given the result stream and the manifests.

Usage
=====
  python3 scripts/v21_eteocretan_gate.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Allow running as `python3 scripts/v21_eteocretan_gate.py`.
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

_DEFAULT_SUBSTRATE = "eteocretan"
_DEFAULT_CONTROL = "control_eteocretan_bigram"
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
    parser.add_argument("--substrate", default=_DEFAULT_SUBSTRATE)
    parser.add_argument("--control", default=_DEFAULT_CONTROL)
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--language-dispatch", type=str, default=None,
        help=(
            "JSON object mapping pool name → external phoneme LM name. "
            "Overrides the same-LM default (used for the cross-LM "
            "negative-control sketch: pass "
            "'{\"eteocretan\":\"basque\",\"control_eteocretan_bigram\":"
            "\"basque\"}' to score under the wrong LM)."
        ),
    )
    parser.add_argument(
        "--out-name", type=str,
        default="rollup.bayesian_posterior.eteocretan.md",
        help="Filename of the markdown report under --results-dir.",
    )
    parser.add_argument(
        "--title-suffix", type=str, default="",
        help="Suffix appended to the markdown title (e.g. ' (under Basque LM)').",
    )
    parser.add_argument(
        "--summary-json", type=Path, default=None,
        help="Optional path for the gate summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    if args.language_dispatch:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)
        language_dispatch.update(json.loads(args.language_dispatch))
    else:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    sub_rows, ctrl_rows = _build_paired_rows(
        pool=args.substrate,
        control_pool=args.control,
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

    # Mean-of-means gap (informational; not part of the gate).
    mean_sub = (
        sum(r["posterior_mean"] for r in sub_top) / len(sub_top) if sub_top else float("nan")
    )
    mean_ctrl = (
        sum(r["posterior_mean"] for r in ctrl_top) / len(ctrl_top) if ctrl_top else float("nan")
    )

    # ----- Markdown -----
    lines: list[str] = []
    title_suffix = args.title_suffix
    lines.append(
        f"# v21 Eteocretan substrate pool — right-tail bayesian gate "
        f"(mg-6ccd){title_suffix}\n"
    )
    if gate:
        verdict = (
            f"**Headline: the Eteocretan substrate pool PASSes the v10 "
            f"right-tail bayesian gate against the bigram-preserving "
            f"control at p={_fmt_p(p)}** (median substrate posterior "
            f"{median_sub:.4f} vs median control posterior "
            f"{median_ctrl:.4f}). Eteocretan — the closest-genealogical-"
            f"relative candidate substrate (presumed Linear-A "
            f"continuation) — joins Aquitanian + Etruscan + toponym as "
            f"the 4th external-validation pool to clear the gate. "
            f"Methodology paper §3.14 narrative: the framework detects "
            f"phonotactic kinship between Linear A and the candidate "
            f"substrate that the consensus already treats as its "
            f"linguistic descendant — the strongest a-priori case in "
            f"the validation series."
        )
    else:
        verdict = (
            f"**Headline: the Eteocretan substrate pool FAILs the v10 "
            f"right-tail bayesian gate against the bigram-preserving "
            f"control at p={_fmt_p(p)}** (median substrate posterior "
            f"{median_sub:.4f} vs median control posterior "
            f"{median_ctrl:.4f}). Eteocretan — the closest-genealogical-"
            f"relative candidate substrate, the strongest a-priori case "
            f"in the validation series — does not produce a substrate-"
            f"vs-control gap clean enough to clear the gate. This is "
            f"the *most* informative possible negative result: it "
            f"forces a rewrite of the methodology paper's interpretive "
            f"framing. Possible readings include (a) the small-corpus "
            f"Eteocretan LM (~87 word forms, α=1.0) is too noisy to "
            f"resolve a real signal, (b) Eteocretan's phonotactic "
            f"shape is too far drifted from Linear-A by 1000+ years "
            f"of linguistic change to register, (c) the framework's "
            f"PASSes on Aquitanian / Etruscan / toponym detect "
            f"something other than substrate continuity. Methodology "
            f"paper §3.14 + §4 must address which reading the data "
            f"supports."
        )
    lines.append(verdict + "\n")

    lines.append("## Acceptance gate\n")
    lines.append(
        "| substrate pool | control pool | substrate top-K | control "
        "top-K | median(top substrate posterior) | median(top control "
        "posterior) | MW U (substrate) | MW p (one-tail, "
        "substrate>control) | gate |"
    )
    lines.append("|:--|:--|---:|---:|---:|---:|---:|---:|:--:|")
    lines.append(
        "| {sub} | {ctrl} | {ns} | {nc} | {mss:.4f} | {msc:.4f} | "
        "{u:.1f} | {p} | {gate} |".format(
            sub=args.substrate, ctrl=args.control,
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
        f"Gap: {mean_sub - mean_ctrl:+.4f}. The gate uses "
        f"the rank-based MW U test rather than the mean gap, so "
        f"this number is shown for orientation only.\n"
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

    # All-surfaces leaderboard, interleaved by effective score.
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
        side = "control" if r["pool_kind"] == args.control else "substrate"
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
        f"- Metric: `{_METRIC}`. LM: `eteocretan` (α=1.0, ~87 word "
        f"forms; see `harness/external_phoneme_models/eteocretan.json`).\n"
        f"- Substrate pool: `{args.substrate}` ({na} top surfaces of "
        f"~84 entries). Control pool: `{args.control}` ({nb} top "
        f"surfaces of ~84 entries; bigram-preserving sampler — the "
        f"v18 production default for new pools).\n"
        f"- Gate: top-{args.top_k_gate} by posterior_mean only "
        f"(no credibility shrinkage); one-tail Mann-Whitney U with "
        f"normal-approximation tie-corrected p-value. PASS at p<0.05 "
        f"with median(substrate top-K) > median(control top-K).\n"
        f"- Determinism: identical rows across re-runs given the same "
        f"`experiments.{_METRIC}*.jsonl`, the substrate / control "
        f"manifests, and the pool YAMLs. No RNG anywhere in the "
        f"pipeline.\n"
        f"- Small-corpus caveat: the Eteocretan LM is built from ~87 "
        f"unique word forms, ~6× smaller than Etruscan and ~80× "
        f"smaller than Basque. Per-surface posteriors are correspond-"
        f"ingly noisier than in v10-v18 work; the gate tolerates this "
        f"tolerable by using the *right-tail* (top-K) comparison "
        f"rather than the bulk-distribution Wilcoxon.\n"
    )

    out_path = args.results_dir / args.out_name
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    summary = {
        "substrate_pool": args.substrate,
        "control_pool": args.control,
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate_top": median_sub,
        "median_control_top": median_ctrl,
        "mean_substrate_top": mean_sub,
        "mean_control_top": mean_ctrl,
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
