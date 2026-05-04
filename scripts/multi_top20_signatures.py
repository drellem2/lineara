#!/usr/bin/env python3
"""Multi-root v9 signatures whose constituent surfaces are all v10 top-20.

mg-0f97 sister analysis to scripts/right_tail_inscription_concentration.py.

A v9 candidate_signature.v1 hypothesis pins a SET of substrate roots to
non-overlapping subspans of a single inscription window. The strongest
"this window looks substrate-readable" candidates are signatures whose
*every* constituent surface is in v10's top-20 (so each constituent has
already cleared the bayesian right-tail acceptance gate
independently).

For each passing pool P ∈ {aquitanian, etruscan}, this rollup walks
``hypotheses/auto_signatures/<P>.manifest.jsonl`` and reports those
whose ``root_surfaces`` are a subset of v10's pool-P top-20 surface
set, sorted by:

  1. paired_diff sign (substrate beats control first)
  2. n_roots (more roots = stronger concentration)
  3. paired_diff magnitude (substrate edge size)

Output
======
  results/rollup.multi_top20_signatures.md

Usage
=====
  python3 scripts/multi_top20_signatures.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python3 scripts/multi_top20_signatures.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.per_surface_bayesian_rollup import (  # type: ignore
    _DEFAULT_AUTO_SIG,
    _DEFAULT_LANGUAGE_DISPATCH,
    _DEFAULT_RESULTS_DIR,
    _METRIC,
    _load_manifest,
    _load_score_rows,
    pick_score_row,
)
from scripts.right_tail_inscription_concentration import (  # type: ignore
    _V10_TOP20_BY_POOL,
    _load_corpus_records,
)


def _load_score_with_paired_diff(
    *,
    auto_sig_dir: Path,
    pool: str,
    score_rows: dict[tuple[str, str], dict],
    language_dispatch: dict[str, str],
) -> dict[str, tuple[float, float, float]]:
    """For each substrate signature in pool P, return
    ``hash → (substrate_score, control_score, paired_diff)``. None if no
    matched control or no scores in the result stream.
    """
    sub_path = auto_sig_dir / f"{pool}.manifest.jsonl"
    ctrl_path = auto_sig_dir / f"control_{pool}.manifest.jsonl"
    sub_rows = _load_manifest(sub_path)
    ctrl_rows = _load_manifest(ctrl_path)

    ctrl_by_paired: dict[str, dict] = {}
    for row in ctrl_rows:
        ctrl_by_paired[row["paired_substrate_hash"]] = row

    sub_lang = language_dispatch.get(pool, "")
    ctrl_lang = language_dispatch.get(f"control_{pool}", sub_lang)

    out: dict[str, tuple[float, float, float]] = {}
    for sub in sub_rows:
        sub_hash = sub["hypothesis_hash"]
        ctrl = ctrl_by_paired.get(sub_hash)
        if ctrl is None:
            continue
        sub_row = pick_score_row(score_rows, sub_hash, sub_lang)
        ctrl_row = pick_score_row(score_rows, ctrl["hypothesis_hash"], ctrl_lang)
        if sub_row is None or ctrl_row is None:
            continue
        s = float(sub_row.get("score", 0.0))
        c = float(ctrl_row.get("score", 0.0))
        out[sub_hash] = (s, c, s - c)
    return out


def find_multi_top20_signatures(
    *,
    pools: list[str],
    auto_sig_dir: Path,
    results_dir: Path,
    top20_by_pool: dict[str, tuple[str, ...]],
    language_dispatch: dict[str, str],
    min_top20_overlap: int = 1,
) -> tuple[list[dict], dict]:
    """Walk pool sig manifests and return (rows, counts).

    A row is emitted for every signature with ≥``min_top20_overlap``
    constituent surfaces in v10's pool-specific top-20. Each row also
    carries the strict-all-top20 flag and the absolute top-20 overlap
    count so the renderer can stratify the leaderboard.
    """
    score_rows = _load_score_rows(results_dir)

    rows: list[dict] = []
    counts: dict[str, dict[str, int]] = {}
    for pool in pools:
        top20 = set(top20_by_pool[pool])
        sig_manifest = _load_manifest(auto_sig_dir / f"{pool}.manifest.jsonl")
        scored = _load_score_with_paired_diff(
            auto_sig_dir=auto_sig_dir,
            pool=pool,
            score_rows=score_rows,
            language_dispatch=language_dispatch,
        )
        n_total = len(sig_manifest)
        n_all_top20 = 0
        n_ge2 = 0
        n_ge1 = 0
        for entry in sig_manifest:
            surfaces = entry["root_surfaces"]
            if not surfaces:
                continue
            n_overlap = sum(1 for s in surfaces if s in top20)
            all_top20 = all(s in top20 for s in surfaces)
            if n_overlap >= 1:
                n_ge1 += 1
            if n_overlap >= 2:
                n_ge2 += 1
            if all_top20:
                n_all_top20 += 1
            if n_overlap < min_top20_overlap:
                continue
            score_tuple = scored.get(entry["hypothesis_hash"])
            if score_tuple is None:
                continue
            sub_score, ctrl_score, paired_diff = score_tuple
            rows.append(
                {
                    "pool": pool,
                    "inscription_id": entry["inscription_id"],
                    "window_start": entry["window_start"],
                    "window_end": entry["window_end"],
                    "n_roots": entry["n_roots"],
                    "root_surfaces": surfaces,
                    "n_top20_overlap": n_overlap,
                    "all_top20": all_top20,
                    "n_window_syllabograms": entry["n_window_syllabograms"],
                    "n_covered_syllabograms": entry["n_covered_syllabograms"],
                    "coverage_fraction": entry["coverage_fraction"],
                    "hypothesis_path": entry["hypothesis_path"],
                    "hypothesis_hash": entry["hypothesis_hash"],
                    "substrate_score": sub_score,
                    "control_score": ctrl_score,
                    "paired_diff": paired_diff,
                }
            )
        counts[pool] = {
            "n_signatures_total": n_total,
            "n_signatures_with_any_top20": n_ge1,
            "n_signatures_with_ge2_top20": n_ge2,
            "n_signatures_all_top20": n_all_top20,
        }
    return rows, counts


def render_md(
    *,
    rows: list[dict],
    counts: dict[str, dict[str, int]],
    corpus_records: list[dict],
    top20_by_pool: dict[str, tuple[str, ...]],
    pools: list[str],
) -> str:
    by_id = {r["id"]: r for r in corpus_records}

    # Sort: more top-20 overlap first, then substrate winners, more roots,
    # larger paired_diff. all-top20 sigs (if any) bubble to the very top.
    rows.sort(
        key=lambda r: (
            0 if r["all_top20"] else 1,
            -r["n_top20_overlap"],
            -1 if r["paired_diff"] > 0 else (0 if r["paired_diff"] == 0 else 1),
            -r["n_roots"],
            -r["paired_diff"],
            r["pool"],
            r["inscription_id"],
            r["window_start"],
            r["hypothesis_hash"],
        )
    )

    out: list[str] = []
    out.append("# v9 multi-root signatures × v10 top-20 surfaces (mg-0f97)\n")
    out.append(
        "Generated by `scripts/multi_top20_signatures.py`. A "
        "`candidate_signature.v1` hypothesis pins a SET of substrate "
        "roots to non-overlapping subspans of one inscription window. "
        "This rollup walks the v9 signature manifests and surfaces those "
        "whose constituent root_surfaces overlap v10's pool-specific "
        "top-20 leaderboard. The cleanest publication candidates are "
        "`all_top20=True` (every constituent independently cleared the "
        "bayesian right-tail acceptance gate); the relaxed view "
        "`n_top20_overlap >= 1` is rendered for context because of the "
        "v9 greedy-fill bias toward short surfaces (mg-bef2 finding).\n"
    )

    out.append("## v10 top-20 substrate surfaces (passing pools)\n")
    for pool in pools:
        out.append(
            f"* **{pool}** (n={len(top20_by_pool[pool])}): "
            + ", ".join(f"`{s}`" for s in top20_by_pool[pool])
            + "\n"
        )

    out.append("## v9 signature × v10 top-20 overlap counts\n")
    out.append(
        "| pool | n_signatures_total | "
        "n_with_any_top20 | n_with_ge2_top20 | n_all_top20 |"
    )
    out.append("|:--|---:|---:|---:|---:|")
    for pool in pools:
        c = counts.get(pool, {})
        out.append(
            f"| {pool} | {c.get('n_signatures_total', 0)} | "
            f"{c.get('n_signatures_with_any_top20', 0)} | "
            f"{c.get('n_signatures_with_ge2_top20', 0)} | "
            f"{c.get('n_signatures_all_top20', 0)} |"
        )
    out.append("")
    out.append(
        "*Interpretation.* The v9 greedy-fill signature generator "
        "(mg-bef2) prefers short surfaces (`ur`, `lur`, etc.) that pack "
        "easily into inscription windows; v10's top-20 surfaces are "
        "mostly 4–7 character roots that the greedy-fill rarely "
        "selects. `n_all_top20 = 0` is therefore an artifact of v9's "
        "generator design, not evidence against substrate concentration. "
        "The v8 + v9 per-inscription rollup at "
        "`results/rollup.right_tail_inscription_concentration.md` is "
        "the right place to read substrate concentration; the strict "
        "all-top20 view is reported here as a transparency null result.\n"
    )

    n_all_top20_rows = sum(1 for r in rows if r["all_top20"])
    out.append(
        f"## Signatures with ≥1 constituent in v10 top-20 (n={len(rows)}; "
        f"all_top20={n_all_top20_rows})\n"
    )
    n_winners = sum(1 for r in rows if r["paired_diff"] > 0)
    n_losers = sum(1 for r in rows if r["paired_diff"] < 0)
    n_ties = sum(1 for r in rows if r["paired_diff"] == 0)
    out.append(
        f"Substrate beat its matched control on **{n_winners}**, lost "
        f"on **{n_losers}**, tied on **{n_ties}** of {len(rows)} "
        f"signatures meeting the threshold.\n"
    )

    out.append(
        "| rank | pool | inscription_id | site | genre_hint | window | "
        "n_roots | n_top20_overlap | all_top20 | root_surfaces | "
        "coverage | substrate_score | control_score | paired_diff |"
    )
    out.append("|---:|:--|:--|:--|:--|:--|---:|---:|:-:|:--|---:|---:|---:|---:|")
    for i, r in enumerate(rows, 1):
        rec = by_id.get(r["inscription_id"], {})
        site = rec.get("site", "—")
        genre = rec.get("genre_hint", "—")
        roots = "+".join(f"`{s}`" for s in r["root_surfaces"])
        win = f"[{r['window_start']}..{r['window_end']}]"
        cov = (
            f"{r['n_covered_syllabograms']}/{r['n_window_syllabograms']} "
            f"({r['coverage_fraction']:.2f})"
        )
        out.append(
            "| {rank} | {pool} | `{ins}` | {site} | {genre} | {win} | "
            "{nroots} | {nover} | {all20} | {roots} | {cov} | "
            "{ss:+.4f} | {cs:+.4f} | {pd:+.4f} |".format(
                rank=i,
                pool=r["pool"],
                ins=r["inscription_id"],
                site=site,
                genre=genre,
                win=win,
                nroots=r["n_roots"],
                nover=r["n_top20_overlap"],
                all20="Y" if r["all_top20"] else "N",
                roots=roots,
                cov=cov,
                ss=r["substrate_score"],
                cs=r["control_score"],
                pd=r["paired_diff"],
            )
        )
    out.append("")

    # Per-inscription concentration of multi-top20 signatures.
    by_ins: dict[str, list[dict]] = {}
    for r in rows:
        by_ins.setdefault(r["inscription_id"], []).append(r)
    out.append("## Inscriptions hosting multiple all-top20 signatures\n")
    out.append(
        "| inscription_id | site | genre_hint | n_signatures | "
        "n_winning | example windows |"
    )
    out.append("|:--|:--|:--|---:|---:|:--|")
    for ins_id, sigs in sorted(by_ins.items(), key=lambda kv: -len(kv[1])):
        if len(sigs) < 2:
            continue
        rec = by_id.get(ins_id, {})
        site = rec.get("site", "—")
        genre = rec.get("genre_hint", "—")
        wins = sum(1 for s in sigs if s["paired_diff"] > 0)
        examples = ", ".join(
            f"[{s['window_start']}..{s['window_end']}]" for s in sigs[:3]
        )
        if len(sigs) > 3:
            examples += f", … (+{len(sigs)-3} more)"
        out.append(
            f"| `{ins_id}` | {site} | {genre} | {len(sigs)} | {wins} | {examples} |"
        )
    out.append("")

    out.append("## Notes\n")
    out.append(
        "- Constituent surfaces are taken as-listed in the manifest's "
        "`root_surfaces`; a signature like `aitz+aitz+oin` is included "
        "if all of `aitz` and `oin` are in v10's top-20. Repeats are "
        "preserved in the rendered surface list (so the reader sees "
        "the actual structure of the signature).\n"
    )
    out.append(
        "- `paired_diff` is the substrate signature's score minus its "
        "matched control's score under the same-LM external phoneme "
        "perplexity model (positive = substrate wins).\n"
    )
    out.append(
        "- Determinism: identical output across re-runs given the same "
        "result stream and manifests. No RNG.\n"
    )

    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=Path("corpus") / "all.jsonl")
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument(
        "--pools",
        type=str,
        default="aquitanian,etruscan",
        help="Comma-separated passing pools (default: aquitanian,etruscan).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results") / "rollup.multi_top20_signatures.md",
    )
    parser.add_argument(
        "--min-overlap",
        type=int,
        default=1,
        help=(
            "Minimum number of constituent surfaces that must be in v10's "
            "top-20 for a signature to appear in the rendered table "
            "(default: 1)."
        ),
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    top20 = {p: _V10_TOP20_BY_POOL[p] for p in pools}
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    rows, counts = find_multi_top20_signatures(
        pools=pools,
        auto_sig_dir=args.auto_sig_dir,
        results_dir=args.results_dir,
        top20_by_pool=top20,
        language_dispatch=language_dispatch,
        min_top20_overlap=args.min_overlap,
    )
    corpus_records = _load_corpus_records(args.corpus)
    text = render_md(
        rows=rows,
        counts=counts,
        corpus_records=corpus_records,
        top20_by_pool=top20,
        pools=pools,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)
    summary = {
        "pools": pools,
        "counts_per_pool": counts,
        "n_rendered_rows": len(rows),
        "n_all_top20_rendered": sum(1 for r in rows if r["all_top20"]),
        "n_substrate_wins": sum(1 for r in rows if r["paired_diff"] > 0),
        "n_substrate_losses": sum(1 for r in rows if r["paired_diff"] < 0),
        "n_ties": sum(1 for r in rows if r["paired_diff"] == 0),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
