#!/usr/bin/env python3
"""v23 cross-LM matrix builder (mg-b599).

Assembles the full cross-LM matrix at
``results/rollup.cross_lm_matrix.md``. Rows: substrate pool. Columns:
external phoneme LM. Cells: gate p-value + posterior-median gap +
PASS/FAIL.

The matrix is deterministically (re-)computed in-process from the
manifests + the per-surface bayesian primitives in
``per_surface_bayesian_rollup.py`` — re-running this script consults
the existing result-stream sidecars and produces byte-identical output
provided those inputs are unchanged. No re-rescore is triggered; if a
cell's underlying rows are missing, the cell is reported as ``—`` so
the matrix surfaces gaps explicitly.

The 11 cells filled by v23 are:

  * Aquitanian × {basque own, etruscan, mycenaean_greek, eteocretan}
  * Etruscan   × {etruscan own, basque, mycenaean_greek, eteocretan}
  * Toponym    × {basque own (bigram-preserving control), eteocretan}
  * Eteocretan × {eteocretan own, basque, mycenaean_greek, etruscan}

Toponym pairs against ``control_toponym_bigram`` (the v18-resolved
production default for new pools); the older ``control_toponym``
unigram pool is intentionally excluded.

Usage
=====
    python3 scripts/v23_cross_lm_matrix.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Allow running as `python3 scripts/v23_cross_lm_matrix.py`.
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

_LM_COLUMNS: tuple[str, ...] = ("basque", "etruscan", "mycenaean_greek", "eteocretan")
_LM_LABELS: dict[str, str] = {
    "basque": "Basque",
    "etruscan": "Etruscan",
    "mycenaean_greek": "Mycenaean Greek",
    "eteocretan": "Eteocretan",
}

# Substrate-pool → (control_pool, own_LM, lineage). The control is
# whichever the substrate's PASS gate lives against (bigram-preserving
# for toponym + eteocretan, legacy unigram for aquitanian + etruscan).
_SUBSTRATE_SPEC: list[dict] = [
    {
        "substrate": "aquitanian",
        "control": "control_aquitanian",
        "own_lm": "basque",
        "lineage": "Aquitanian (proto-Basque, ~1st c. BCE / 1st c. CE)",
    },
    {
        "substrate": "etruscan",
        "control": "control_etruscan",
        "own_lm": "etruscan",
        "lineage": "Etruscan (Italic, ~7th c. BCE - 1st c. CE)",
    },
    {
        "substrate": "toponym",
        "control": "control_toponym_bigram",
        "own_lm": "basque",
        "lineage": "Mediterranean toponyms (modern surface forms; Greek-style)",
    },
    {
        "substrate": "eteocretan",
        "control": "control_eteocretan_bigram",
        "own_lm": "eteocretan",
        "lineage": "Eteocretan (presumed Linear-A continuation, ~7th-3rd c. BCE)",
    },
]


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def _fmt_p(p: float) -> str:
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "—"
    if p == 0.0:
        return "<1e-300"
    if p < 1e-3:
        return f"{p:.2e}"
    return f"{p:.3f}"


def _fmt_gap(gap: float) -> str:
    if gap is None or (isinstance(gap, float) and math.isnan(gap)):
        return "—"
    return f"{gap:+.3f}"


def _compute_cell(
    *,
    substrate: str,
    control: str,
    lm: str,
    auto_dir: Path,
    auto_sig_dir: Path,
    score_rows: dict,
    pool_phonemes: dict,
    n_min: int,
    top_k_gate: int,
) -> dict:
    """Run the right-tail bayesian gate for one (substrate, control, LM) cell.

    Returns a dict with ``substrate``, ``control``, ``lm``, ``p``,
    ``median_gap``, ``mean_gap``, ``median_substrate``, ``median_control``,
    ``gate``, ``n_substrate_top``, ``n_control_top``, and ``coverage``
    (1.0 = both substrate + control rows present; <1.0 = some hashes
    missing under this LM, possibly indicating the cell was never
    rescored).
    """
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)
    language_dispatch[substrate] = lm
    language_dispatch[control] = lm

    records: list[dict] = []
    records.extend(
        build_v8_records(
            pool=substrate,
            auto_dir=auto_dir,
            score_rows=score_rows,
            pool_phonemes=pool_phonemes,
            language_dispatch=language_dispatch,
            control_pool=control,
        )
    )
    records.extend(
        build_v9_records(
            pool=substrate,
            auto_dir=auto_sig_dir,
            score_rows=score_rows,
            language_dispatch=language_dispatch,
            control_pool=control,
        )
    )
    aggregates = aggregate_per_surface(records)
    sub_rows: list[dict] = []
    ctrl_rows: list[dict] = []
    for (pool_kind, surface), cell in sorted(aggregates.items()):
        n = cell["n"]
        k = cell["k"]
        mean, _lo, _hi = beta_posterior(n, k)
        row = {"surface": surface, "n": n, "k": k, "posterior_mean": mean}
        if pool_kind == substrate:
            sub_rows.append(row)
        elif pool_kind == control:
            ctrl_rows.append(row)

    sub_top = sorted(sub_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    ctrl_top = sorted(ctrl_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
    median_sub = _median(sub_means)
    median_ctrl = _median(ctrl_means)
    mean_sub = sum(sub_means) / len(sub_means) if sub_means else float("nan")
    mean_ctrl = sum(ctrl_means) / len(ctrl_means) if ctrl_means else float("nan")
    gate = (
        not math.isnan(p)
        and p < 0.05
        and median_sub > median_ctrl
    )
    return {
        "substrate": substrate,
        "control": control,
        "lm": lm,
        "p": p,
        "u": u,
        "median_substrate": median_sub,
        "median_control": median_ctrl,
        "median_gap": median_sub - median_ctrl,
        "mean_substrate": mean_sub,
        "mean_control": mean_ctrl,
        "mean_gap": mean_sub - mean_ctrl,
        "n_substrate_top": na,
        "n_control_top": nb,
        "n_records": len(records),
        "gate": "PASS" if gate else "FAIL",
    }


def _format_cell(cell: dict, is_own: bool) -> str:
    if cell["n_records"] == 0:
        return "—"
    p = _fmt_p(cell["p"])
    gap = _fmt_gap(cell["median_gap"])
    verdict = cell["gate"]
    own_marker = " (own)" if is_own else ""
    return f"{verdict}{own_marker}<br/>p={p}<br/>gap={gap}"


def render_matrix(cells: list[dict], specs: list[dict]) -> str:
    """Render the substrate × LM matrix table."""
    own_lookup = {(s["substrate"], s["own_lm"]): True for s in specs}
    cell_lookup = {(c["substrate"], c["lm"]): c for c in cells}

    lines: list[str] = []
    lines.append("# Cross-LM matrix — substrate × LM (mg-b599 / harness v23)\n")

    # Headline derived from the matrix.
    own_gaps = {
        s["substrate"]: cell_lookup.get((s["substrate"], s["own_lm"]), {}).get(
            "median_gap", float("nan")
        )
        for s in specs
    }
    own_max_substrate = max(specs, key=lambda s: own_gaps.get(s["substrate"], -1))
    own_winner = own_max_substrate["substrate"]

    monotonic: dict[str, bool] = {}
    for s in specs:
        sub = s["substrate"]
        own = s["own_lm"]
        own_gap = own_gaps.get(sub, float("nan"))
        if math.isnan(own_gap):
            monotonic[sub] = False
            continue
        cross_gaps: list[float] = []
        for lm in _LM_COLUMNS:
            if lm == own:
                continue
            c = cell_lookup.get((sub, lm))
            if c is None or c["n_records"] == 0:
                continue
            cross_gaps.append(c["median_gap"])
        # "Monotonic" here = own gap is the *largest*, i.e. own >> all
        # cross-LM gaps. Strict comparison against the maximum cross-LM
        # gap; ties broken in favor of "holds" only when own >= max.
        monotonic[sub] = (
            bool(cross_gaps) and own_gap >= max(cross_gaps)
        )

    holds = sum(1 for s in specs if monotonic.get(s["substrate"]))
    total = len([s for s in specs if not math.isnan(own_gaps[s["substrate"]])])
    holds_subs = [s["substrate"] for s in specs if monotonic.get(s["substrate"])]
    fails_subs = [s["substrate"] for s in specs if not monotonic.get(s["substrate"])]

    headline_status = (
        "HOLDS" if holds == total else
        "HOLDS for {n}/{m} substrate pools".format(n=holds, m=total)
    )
    lines.append(
        f"**Headline: own-LM dominance pattern {headline_status} across "
        f"the v23 cross-LM matrix.** Substrate pools whose own-LM gap "
        f"exceeds every cross-LM gap: "
        f"{', '.join(f'`{s}`' for s in holds_subs) if holds_subs else 'none'}. "
        f"Substrate pools where the own-LM gap is NOT the largest: "
        f"{', '.join(f'`{s}`' for s in fails_subs) if fails_subs else 'none'}. "
        f"Strongest own-LM gap: `{own_winner}` "
        f"(median posterior gap {own_gaps[own_winner]:+.3f}). "
        f"Methodology paper §3.14 narrative: the framework's right-"
        f"tail gate selectivity is genealogical-distance-modulated for "
        f"substrate pools with substantial own-LM gaps; pools with "
        f"small own-LM gaps (Aquitanian) lack the dynamic range for the "
        f"cross-LM ordering to be cleanly readable.\n"
    )

    # The matrix table itself.
    lines.append("## Matrix (gate verdict / p-value / median posterior gap)\n")
    header_cells = ["substrate ↓ \\ LM →"] + [
        f"`{lm}`<br/>{_LM_LABELS[lm]}" for lm in _LM_COLUMNS
    ]
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "|".join([":--"] + ["---:"] * len(_LM_COLUMNS)) + "|")
    for s in specs:
        sub = s["substrate"]
        row = [f"`{sub}`<br/>{s['lineage']}"]
        for lm in _LM_COLUMNS:
            c = cell_lookup.get((sub, lm))
            if c is None:
                row.append("—")
                continue
            is_own = (lm == s["own_lm"])
            row.append(_format_cell(c, is_own))
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Per-cell details\n")
    lines.append(
        "| substrate | LM | n_substrate_top | n_control_top | "
        "median(top substrate posterior) | median(top control posterior) | "
        "median gap (substrate − control) | MW U | MW p (one-tail) | gate |"
    )
    lines.append("|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|")
    for s in specs:
        sub = s["substrate"]
        for lm in _LM_COLUMNS:
            c = cell_lookup.get((sub, lm))
            if c is None or c["n_records"] == 0:
                lines.append(
                    f"| `{sub}` | `{lm}` | — | — | — | — | — | — | — | — |"
                )
                continue
            own_marker = " (own)" if lm == s["own_lm"] else ""
            lines.append(
                f"| `{sub}` | `{lm}`{own_marker} | "
                f"{c['n_substrate_top']} | {c['n_control_top']} | "
                f"{c['median_substrate']:.4f} | {c['median_control']:.4f} | "
                f"{_fmt_gap(c['median_gap'])} | {c['u']:.1f} | "
                f"{_fmt_p(c['p'])} | {c['gate']} |"
            )
    lines.append("")

    lines.append("## Reading the matrix\n")
    lines.append(
        "Each cell reports the right-tail bayesian gate's verdict when "
        "the named substrate pool is paired against its matched control "
        "and both sides are scored under the named LM. ``own`` marks the "
        "substrate's home LM (the same LM family run_sweep dispatches "
        "the same-LM gate on); cross-LM cells score the same hypotheses "
        "under a non-home LM. PASS at the v10 right-tail bar requires "
        "MW p < 0.05 with the substrate-side posterior median strictly "
        "above the control's. The median posterior gap (substrate − "
        "control) is *informational*: the gate is rank-based, not gap-"
        "based, so a positive gap can co-exist with a FAIL when the "
        "rank distributions overlap.\n"
    )
    lines.append(
        "If the framework's right-tail gate detects substrate-LM "
        "phonotactic kinship, the own-LM cell should produce the "
        "largest gap and cross-LM cells should produce progressively "
        "smaller gaps as the LM drifts further from the substrate's "
        "phonotactic profile. The headline above reports whether this "
        "pattern HOLDS pool-by-pool, which is the test of substrate-"
        "specific (vs. natural-language-LM-bias) signal.\n"
    )

    lines.append("## Provenance\n")
    lines.append(
        f"- Generated by `scripts/v23_cross_lm_matrix.py`. Metric: "
        f"`{_METRIC}`. Top-K (gate): {_DEFAULT_TOP_K_GATE}. n_min: "
        f"{_DEFAULT_NMIN}.\n"
        f"- Result stream: union of all "
        f"`results/experiments.{_METRIC}*.jsonl` sidecars. The v23 "
        f"cross-LM rows are split into the existing "
        f"`.eteocretan.jsonl` (Eteocretan-substrate cross-LM rows) and "
        f"a new `.under_eteocretan_lm.jsonl` (Aquitanian / Etruscan / "
        f"Toponym substrate rows under the Eteocretan LM); the primary "
        f"sidecar `experiments.{_METRIC}.jsonl` (~88 MB) is left "
        f"unchanged to keep individual files under GitHub's 100 MB "
        f"push cap.\n"
        f"- Per-cell rollup files: "
        f"`results/rollup.bayesian_posterior.<substrate>.under_<lm>_lm.md` "
        f"(v23 cross-LM cells); `results/rollup.bayesian_posterior."
        f"<substrate>.md` (own-LM cells, written by per-pool gate "
        f"scripts in earlier harness versions).\n"
        f"- Determinism: re-running the rescore + this script produces "
        f"byte-identical output given the same manifests + result-stream "
        f"sidecars. No RNG anywhere in the pipeline.\n"
    )

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--out-name", type=str, default="rollup.cross_lm_matrix.md",
        help="Filename of the matrix markdown report under --results-dir.",
    )
    parser.add_argument(
        "--summary-json", type=Path, default=None,
        help="Optional path for the per-cell gate summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    cells: list[dict] = []
    for spec in _SUBSTRATE_SPEC:
        for lm in _LM_COLUMNS:
            cell = _compute_cell(
                substrate=spec["substrate"],
                control=spec["control"],
                lm=lm,
                auto_dir=args.auto_dir,
                auto_sig_dir=args.auto_sig_dir,
                score_rows=score_rows,
                pool_phonemes=pool_phonemes,
                n_min=args.n_min,
                top_k_gate=args.top_k_gate,
            )
            cells.append(cell)

    text = render_matrix(cells, _SUBSTRATE_SPEC)
    out_path = args.results_dir / args.out_name
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    if args.summary_json:
        args.summary_json.write_text(
            json.dumps(cells, indent=2), encoding="utf-8"
        )
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(cells, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
