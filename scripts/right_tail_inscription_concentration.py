#!/usr/bin/env python3
"""Per-inscription right-tail concentration analysis (mg-0f97).

Identifies the Linear A inscriptions on which the v10 top-20 substrate
surfaces concentrate. For each Linear A inscription i and each pool P
∈ {aquitanian, etruscan} that PASSed the v10 right-tail bayesian gate:

* Count the number of distinct v10-top-20 substrate surfaces (across
  both passing pools, deduplicated by surface string) that have at
  least one *positive paired_diff* record on inscription i. (A
  paired_diff record comes from either a v8 single-root candidate or a
  v9 multi-root signature; substrate side wins when paired_diff > 0.)

* Compute "right-tail evidence density":
    density = (# distinct top-20 surfaces with positive evidence on i)
              / (# v8 + v9 substrate records targeting i)

Inscriptions where multiple top-20 surfaces show concurrent positive
evidence are the strongest "this inscription looks substrate-readable"
candidates — the publication-shape research output of v11.

Output
======
  results/rollup.right_tail_inscription_concentration.md  (top-30 by raw count)

This is *descriptive statistics on existing data* — no new metric, no
new corpus ingest. Pure analysis layer over the v8 + v9 paired-diff
records already in the result stream.

Usage
=====
  python3 scripts/right_tail_inscription_concentration.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

# Allow `python3 scripts/right_tail_inscription_concentration.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.per_surface_bayesian_rollup import (  # type: ignore
    _DEFAULT_AUTO,
    _DEFAULT_AUTO_SIG,
    _DEFAULT_LANGUAGE_DISPATCH,
    _DEFAULT_POOLS,
    _DEFAULT_RESULTS_DIR,
    _METRIC,
    _load_manifest,
    _load_pool_phonemes,
    _load_score_rows,
    build_v8_records,
    build_v9_records,
)


# v10 (mg-d26d) top-20 substrate surfaces, by passing pool. These are the
# right-tail leaderboard entries from results/rollup.bayesian_posterior.{
# aquitanian,etruscan}.md committed under mg-d26d. Toponym is excluded
# (failed the gate). Hardcoded here so the per-inscription rollup is
# reproducible *as a downstream analysis of v10's published results* and
# does not silently shift if upstream ranks reshuffle by a tie-breaking
# update.
_V10_TOP20_BY_POOL: dict[str, tuple[str, ...]] = {
    "aquitanian": (
        "aitz", "hanna", "nahi", "ako", "beltz", "bihotz", "egun", "eki",
        "ezti", "gaitz", "hau", "hesi", "itsaso", "oin", "ona", "zelai",
        "zortzi", "argi", "ate", "entzun",
    ),
    "etruscan": (
        "larth", "aiser", "matam", "avils", "camthi", "chimth", "hanthe",
        "laris", "nac", "sech", "thana", "zelar", "caitim", "thesan",
        "spureri", "thanchvil", "suthi", "mach", "arnth", "sath",
    ),
}


def _load_corpus_records(corpus_path: Path) -> list[dict]:
    rows: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _v8_inscription_index(auto_dir: Path, pool: str) -> dict[str, str]:
    """v8 substrate hypothesis_hash → inscription_id."""
    out: dict[str, str] = {}
    for row in _load_manifest(auto_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = row["inscription_id"]
    return out


def _v9_inscription_index(auto_sig_dir: Path, pool: str) -> dict[str, str]:
    """v9 substrate hypothesis_hash → inscription_id."""
    out: dict[str, str] = {}
    for row in _load_manifest(auto_sig_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = row["inscription_id"]
    return out


def build_per_inscription_concentration(
    *,
    pools: list[str],
    auto_dir: Path,
    auto_sig_dir: Path,
    pools_dir: Path,
    results_dir: Path,
    top20_by_pool: dict[str, tuple[str, ...]],
    language_dispatch: dict[str, str],
) -> dict[str, dict]:
    """Walk v8 + v9 substrate records and aggregate per inscription.

    Returns ``inscription_id → {
      "raw_count": int,        # # distinct top-20 surfaces with ≥1 positive evidence record
      "n_records_targeting": int,
      "density": float,
      "top20_surfaces_present": dict[surface, dict[pool, n_positive]],
      "n_records_by_pool": dict[pool, int],
    }``
    """
    score_rows = _load_score_rows(results_dir)
    pool_phonemes = _load_pool_phonemes(pools_dir)

    # Substrate paired_diff records, restricted to passing pools.
    sub_records: list[dict] = []
    for pool in pools:
        sub_records.extend(
            build_v8_records(
                pool=pool,
                auto_dir=auto_dir,
                score_rows=score_rows,
                pool_phonemes=pool_phonemes,
                language_dispatch=language_dispatch,
            )
        )
        sub_records.extend(
            build_v9_records(
                pool=pool,
                auto_dir=auto_sig_dir,
                score_rows=score_rows,
                language_dispatch=language_dispatch,
            )
        )

    # Substrate hash → inscription_id, per kind. Each substrate record's
    # source (v8 vs v9) determines which manifest holds the inscription
    # mapping. We pre-index per (kind, pool) so lookups are O(1).
    v8_index: dict[str, dict[str, str]] = {p: _v8_inscription_index(auto_dir, p) for p in pools}
    v9_index: dict[str, dict[str, str]] = {p: _v9_inscription_index(auto_sig_dir, p) for p in pools}

    # All-pool flat top-20 set (deduped). Surfaces are deduplicated
    # *across pools*; if a surface appears in both pools' top-20 (none do
    # in v10, but the dedup is principled), it counts once.
    flat_top20: set[str] = set()
    for surfaces in top20_by_pool.values():
        flat_top20.update(surfaces)

    # Per-inscription accumulator.
    per_ins: dict[str, dict] = defaultdict(
        lambda: {
            "raw_count": 0,
            "n_records_targeting": 0,
            "density": 0.0,
            "top20_surfaces_present": {},  # surface → {pool: n_positive}
            "n_records_by_pool": defaultdict(int),
            "n_positive_records": 0,
        }
    )
    # Track which (inscription, surface, pool) combinations have a
    # positive observation; raw_count is the number of distinct
    # surfaces (regardless of pool) with ≥1 positive at that inscription.
    surface_positive_at: dict[str, set[str]] = defaultdict(set)

    for rec in sub_records:
        pool = rec["pool"]
        # Resolve the inscription_id: a v8 substrate record maps via
        # v8_index[pool][substrate_hash]; a v9 via v9_index[pool][...].
        sub_hash = rec["substrate_hash"]
        if rec["kind"] == "v8":
            ins_id = v8_index[pool].get(sub_hash)
        else:
            ins_id = v9_index[pool].get(sub_hash)
        if ins_id is None:
            continue
        cell = per_ins[ins_id]
        cell["n_records_targeting"] += 1
        cell["n_records_by_pool"][pool] += 1
        if rec["paired_diff"] > 0:
            cell["n_positive_records"] += 1
        for s in set(rec["substrate_surfaces"]):
            if s not in flat_top20:
                continue
            if rec["paired_diff"] <= 0:
                continue
            surface_positive_at[ins_id].add(s)
            slot = cell["top20_surfaces_present"].setdefault(s, defaultdict(int))
            slot[pool] += 1

    # Finalize raw_count and density.
    for ins_id, cell in per_ins.items():
        cell["raw_count"] = len(surface_positive_at.get(ins_id, set()))
        n = cell["n_records_targeting"]
        cell["density"] = (cell["raw_count"] / n) if n > 0 else 0.0
        # Convert defaultdicts to plain dicts for stable serialization.
        cell["n_records_by_pool"] = dict(cell["n_records_by_pool"])
        cell["top20_surfaces_present"] = {
            s: dict(slots) for s, slots in cell["top20_surfaces_present"].items()
        }
    return per_ins


def render_md(
    *,
    per_ins: dict[str, dict],
    corpus_records: list[dict],
    top_per_view: int,
    top20_by_pool: dict[str, tuple[str, ...]],
) -> str:
    by_id = {r["id"]: r for r in corpus_records}
    rows: list[dict] = []
    for ins_id, cell in per_ins.items():
        rec = by_id.get(ins_id, {})
        rows.append(
            {
                "id": ins_id,
                "site": rec.get("site", ""),
                "genre_hint": rec.get("genre_hint", ""),
                "raw_count": cell["raw_count"],
                "n_records_targeting": cell["n_records_targeting"],
                "n_positive_records": cell["n_positive_records"],
                "density": cell["density"],
                "top20_surfaces_present": cell["top20_surfaces_present"],
                "n_records_by_pool": cell["n_records_by_pool"],
            }
        )

    # Two complementary views: by raw count (concentration), by density.
    by_count = sorted(rows, key=lambda r: (-r["raw_count"], -r["density"], r["id"]))
    by_density = sorted(
        [r for r in rows if r["raw_count"] >= 2],  # density only meaningful with ≥2
        key=lambda r: (-r["density"], -r["raw_count"], r["id"]),
    )

    flat_top20: set[str] = set()
    for s in top20_by_pool.values():
        flat_top20.update(s)

    out: list[str] = []
    out.append(
        "# Right-tail per-inscription concentration of v10 top-20 substrate surfaces (mg-0f97)\n"
    )
    out.append(
        "Generated by `scripts/right_tail_inscription_concentration.py`. "
        "For each Linear A inscription i, counts the number of *distinct* "
        "v10-top-20 substrate surfaces (across the Aquitanian + Etruscan "
        "pools that PASSed the v10 right-tail gate) for which i has at "
        "least one *positive paired_diff* record from a v8 single-root "
        "candidate or a v9 multi-root signature. Density divides by the "
        "number of v8 + v9 substrate records that target i.\n"
    )
    out.append(
        f"Universe: {len(flat_top20)} distinct top-20 surfaces "
        f"({len(top20_by_pool['aquitanian'])} aquitanian + "
        f"{len(top20_by_pool['etruscan'])} etruscan, deduplicated). "
        f"{sum(1 for r in rows if r['raw_count'] > 0)} of "
        f"{len(rows)} inscriptions in the working set have at least one "
        f"top-20 surface with positive evidence; "
        f"{sum(1 for r in rows if r['raw_count'] >= 2)} have ≥2.\n"
    )

    out.append("## v10 top-20 substrate surfaces (passing pools)\n")
    out.append(
        "* **Aquitanian** (n=20): "
        + ", ".join(f"`{s}`" for s in top20_by_pool["aquitanian"])
        + "\n"
    )
    out.append(
        "* **Etruscan** (n=20): "
        + ", ".join(f"`{s}`" for s in top20_by_pool["etruscan"])
        + "\n"
    )

    out.append("## Top-30 inscriptions by raw count (concentration)\n")
    out.append(
        "| rank | inscription_id | site | genre_hint | "
        "n_top20_surfaces_positive | n_records_targeting | "
        "n_positive_records | density | top_substrate_surfaces_present |"
    )
    out.append("|---:|:--|:--|:--|---:|---:|---:|---:|:--|")
    for i, r in enumerate(by_count[:top_per_view], 1):
        present = ", ".join(
            f"`{s}` ({sum(slots.values())})"
            for s, slots in sorted(
                r["top20_surfaces_present"].items(),
                key=lambda kv: (-sum(kv[1].values()), kv[0]),
            )
        ) or "—"
        out.append(
            "| {rank} | `{ins}` | {site} | {genre} | {raw} | {n_rec} | "
            "{n_pos} | {dens} | {present} |".format(
                rank=i,
                ins=r["id"],
                site=r["site"] or "—",
                genre=r["genre_hint"] or "—",
                raw=r["raw_count"],
                n_rec=r["n_records_targeting"],
                n_pos=r["n_positive_records"],
                dens=f"{r['density']:.4f}" if not math.isnan(r["density"]) else "nan",
                present=present,
            )
        )
    out.append("")

    out.append("## Top-30 inscriptions by density (raw_count ≥ 2)\n")
    out.append(
        "| rank | inscription_id | site | genre_hint | "
        "n_top20_surfaces_positive | n_records_targeting | density | "
        "top_substrate_surfaces_present |"
    )
    out.append("|---:|:--|:--|:--|---:|---:|---:|:--|")
    for i, r in enumerate(by_density[:top_per_view], 1):
        present = ", ".join(
            f"`{s}` ({sum(slots.values())})"
            for s, slots in sorted(
                r["top20_surfaces_present"].items(),
                key=lambda kv: (-sum(kv[1].values()), kv[0]),
            )
        ) or "—"
        out.append(
            "| {rank} | `{ins}` | {site} | {genre} | {raw} | {n_rec} | "
            "{dens} | {present} |".format(
                rank=i,
                ins=r["id"],
                site=r["site"] or "—",
                genre=r["genre_hint"] or "—",
                raw=r["raw_count"],
                n_rec=r["n_records_targeting"],
                dens=f"{r['density']:.4f}" if not math.isnan(r["density"]) else "nan",
                present=present,
            )
        )
    out.append("")

    out.append("## Notes\n")
    out.append(
        "- A surface counts toward an inscription's `raw_count` once "
        "regardless of how many positive records it has on that "
        "inscription; the parenthesized number after each surface in "
        "`top_substrate_surfaces_present` is the total count of "
        "positive paired_diff records over all (v8, v9) records pinning "
        "that surface to that inscription.\n"
    )
    out.append(
        "- A v9 signature like `lur+lur+ur` covering one window "
        "contributes one observation under each unique constituent "
        "surface (`lur`, `ur`) for that inscription, not two for `lur`.\n"
    )
    out.append(
        "- `density` is the per-record fraction of substrate records "
        "targeting the inscription that contributed at least one top-20 "
        "surface with positive evidence; `raw_count` is the *distinct-"
        "surface* count and does not double-count the same surface.\n"
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
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--pools",
        type=str,
        default="aquitanian,etruscan",
        help=(
            "Comma-separated passing pools to aggregate over. Default: "
            "aquitanian,etruscan (v10 PASSes; toponym FAILED so it is "
            "excluded by default)."
        ),
    )
    parser.add_argument("--top-per-view", type=int, default=30)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results") / "rollup.right_tail_inscription_concentration.md",
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    top20 = {p: _V10_TOP20_BY_POOL[p] for p in pools}
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    per_ins = build_per_inscription_concentration(
        pools=pools,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        pools_dir=args.pools_dir,
        results_dir=args.results_dir,
        top20_by_pool=top20,
        language_dispatch=language_dispatch,
    )
    corpus_records = _load_corpus_records(args.corpus)
    text = render_md(
        per_ins=per_ins,
        corpus_records=corpus_records,
        top_per_view=args.top_per_view,
        top20_by_pool=top20,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)

    summary = {
        "n_inscriptions_with_evidence": sum(
            1 for cell in per_ins.values() if cell["raw_count"] > 0
        ),
        "n_inscriptions_multi_top20": sum(
            1 for cell in per_ins.values() if cell["raw_count"] >= 2
        ),
        "max_raw_count": max((c["raw_count"] for c in per_ins.values()), default=0),
        "n_inscriptions_total": len(per_ins),
        "pools": pools,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
