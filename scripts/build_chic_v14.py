#!/usr/bin/env python3
"""chic-v14: leave-one-out held-out validation of the chic-v12 cross-pool
L3 reclassification methodology (mg-7f57).

Methodologically symmetric to chic-v9 (mg-18cb): chic-v9 closed the
LOO-on-the-chic-v5-four-line-framework gap; chic-v14 closes the
analogous gap for the chic-v12 cross-pool L3 axis.

Background
==========

chic-v12 (mg-2035) introduced a candidate-generation methodology: a
chic-v5 tier-3 candidate reclassifies to ``tier-2-equivalent`` if at
least one non-Eteocretan substrate LM's L3 vote matches the L1+L2
distributional consensus on phoneme class. 8 of 29 tier-3 candidates
passed (27.6%).

The held-out validation question chic-v12 does not answer: when run
blind on **known** chic-v2 anchors, what fraction reclassify to
``tier-2-equivalent`` if the reference class is the anchor's *known*
phoneme class? That rate is the cross-pool L3 LOO baseline against
which chic-v12's 27.6% reads as above-baseline / at-baseline /
below-baseline.

Method
======

For each of the 20 chic-v2 anchors S with known LB-carryover value V:

1. Hold out S in-memory (the chic-v2 anchor pool yaml is read-only).
2. Build the reduced 19-anchor pool, the reduced anchor mapping, and
   for each of the 4 substrate pools (aquitanian, etruscan, toponym,
   eteocretan) rebuild the candidate-value pool from the reduced
   19-anchor pool's distinct LB-carryover values + bare vowels,
   filtered by that substrate pool's phoneme inventory (chic-v5
   convention).
3. Treat S as the single unknown sign and run
   ``compute_substrate_consistency`` against the reduced 19-anchor
   mapping under each of the 4 substrate-pool LMs. The class-disjoint
   sha256-keyed control mapping is regenerated per (LOO iteration,
   pool) cell because the candidate-value pool is rebuilt per
   iteration; no caching across iterations (which would leak the
   held-out anchor).
4. Per pool, the per-class mean paired_diff picks the L3 winning
   class for that (anchor, pool) cell.
5. Apply the chic-v12 reclassification rule with the **known class**
   as reference (in chic-v12 the reference was the chic-v5 proposed
   class):

   - ``corroborated_by`` = list of non-Eteocretan substrate LMs
     whose winning class matches S's known class.
   - ``eteocretan_corroborates`` = (eteocretan winning class ==
     known class).
   - ``reclassification`` =
       * ``tier-2-equivalent`` if ``corroborated_by`` is non-empty.
       * ``tier-3-corroborated`` if only Eteocretan-L3 corroborates.
       * ``tier-3-uncorroborated`` if no LM corroborates.

L1 (distributional plurality, top-3 nearest anchors) and L2 (strict-
top-1 anchor distance) are also recomputed per LOO iteration for
audit context (same machinery as chic-v9), but the chic-v14 verdict
is purely a function of the cross-pool L3 reclassification — L1+L2
are surfaced in the per-anchor table for the reader's reference and
to make chic-v14 visibly methodologically symmetric to chic-v9 (the
"same machinery as chic-v9" clause of the brief).

L4 (cross-script paleographic) is excluded by construction (chic-v9
precedent): the chic-v1 PALEOGRAPHIC_CANDIDATES list is the source of
the chic-v2 anchor pool, so for any anchor S the L4 line trivially
recovers V — including L4 would inflate accuracy by construction.
Cross-pool L3 does not consult L4, so the exclusion is automatic.

Aggregate metrics (per the chic-v14 brief)
==========================================

- ``cross_pool_l3_recovery_rate``  = fraction reclassifying to
  ``tier-2-equivalent`` under LOO. The baseline rate against which
  chic-v12's 8/29 = 27.6% reads.
- ``eteocretan_only_recovery_rate`` = fraction reclassifying to
  ``tier-3-corroborated`` (Eteocretan-L3 corroborates only).
- ``no_corroboration_rate`` = fraction reclassifying to
  ``tier-3-uncorroborated``.

Comparison verdict (per the chic-v14 brief): the chic-v14 cross-pool
L3 LOO recovery rate vs chic-v12's 27.6% reclassification rate. Above
baseline / at baseline / below baseline:

- LOO rate **>= 27.6%**: the chic-v12 27.6% is at or below baseline.
  Specifically, if LOO rate is much higher (e.g. 80%), the cross-pool
  L3 axis corroborates ground-truth-class far more often than it
  corroborates the chic-v5 proposed class on the tier-3 set, so
  chic-v12's reclassification is below the rate we'd see if the
  proposed classes were correct — anti-evidentiary on the tier-3 set.
- LOO rate **< 27.6%**: the chic-v12 27.6% exceeds the LOO baseline,
  meaning the chic-v12 reclassification picks up a band of
  candidates that get cross-pool corroboration at a higher rate than
  even ground-truth-on-known-anchors does — meaningfully above
  baseline.

This is the chic-v14 brief's interpretation framework. The script
reports both rates and lets the data speak.

Inputs (all already committed)
==============================

- ``corpora/cretan_hieroglyphic/all.jsonl``           (chic-v0)
- ``corpora/cretan_hieroglyphic/syllabographic.jsonl`` (chic-v3)
- ``pools/cretan_hieroglyphic_signs.yaml``            (chic-v1)
- ``pools/cretan_hieroglyphic_anchors.yaml``          (chic-v2;
                                                       READ-ONLY)
- ``pools/{aquitanian,etruscan,toponym,eteocretan}.yaml``
- ``harness/external_phoneme_models/{basque,etruscan,eteocretan}.json``

Outputs
=======

- ``results/chic_v14_loo_validation.md`` — per-anchor LOO table +
  aggregate metrics + comparison to chic-v12's 27.6%.
- ``results/chic_v14_summary.md`` — 1-paragraph plain-English
  verdict + headline-count table.

Determinism
===========

No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-
keyed permutation construction; LOO iteration order is sorted by
anchor numeric id; cross-pool dispatch is fixed in POOL_DISPATCH.
Same inputs → byte-identical outputs.

Usage
=====

    python3 scripts/build_chic_v14.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from harness.external_phoneme_model import ExternalPhonemeModel  # noqa: E402

from scripts.build_chic_v5 import (  # noqa: E402
    TOP_K_NEAREST,
    aggregate_class_means,
    build_anchor_mapping,
    candidate_value_pool,
    classify_value,
    compute_anchor_distance_map,
    compute_fingerprints,
    compute_substrate_consistency,
    load_chic_records,
)

CHIC_FULL = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
CHIC_SYLL = ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
SIGNS_YAML = ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"

OUT_LOO_MD = ROOT / "results" / "chic_v14_loo_validation.md"
OUT_SUMMARY_MD = ROOT / "results" / "chic_v14_summary.md"

FETCHED_AT = "2026-05-06T08:33:06Z"

# (pool_name, pool_yaml_path, lm_path) — fixed dispatch order, byte-
# identical to chic-v11 / chic-v12.
POOL_DISPATCH: list[tuple[str, Path, Path]] = [
    ("aquitanian",
     ROOT / "pools" / "aquitanian.yaml",
     ROOT / "harness" / "external_phoneme_models" / "basque.json"),
    ("etruscan",
     ROOT / "pools" / "etruscan.yaml",
     ROOT / "harness" / "external_phoneme_models" / "etruscan.json"),
    ("toponym",
     ROOT / "pools" / "toponym.yaml",
     ROOT / "harness" / "external_phoneme_models" / "basque.json"),
    ("eteocretan",
     ROOT / "pools" / "eteocretan.yaml",
     ROOT / "harness" / "external_phoneme_models" / "eteocretan.json"),
]

CLASS_ORDER = ("vowel", "stop", "nasal", "liquid", "fricative", "glide")

# chic-v12 baseline: 8 of 29 tier-3 candidates reclassified to
# tier-2-equivalent. Stored as a tuple (numerator, denominator) so the
# comparison report computes the rate symbolically.
CHIC_V12_BASELINE: tuple[int, int] = (8, 29)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _plurality_class(top_anchors: list[dict]) -> str | None:
    """Plurality class over the top-K nearest anchors. Tiebreak
    alphabetically (matches chic-v5 / chic-v9)."""
    votes = Counter(
        a["anchor_class"] for a in top_anchors if a["anchor_class"] != "unknown"
    )
    if not votes:
        return None
    return sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


# ---------------------------------------------------------------------------
# Per-anchor LOO cross-pool L3 driver
# ---------------------------------------------------------------------------


def loo_cross_pool_l3_anchor(
    *,
    target_sid: str,
    anchor_records_full: list[dict],
    fingerprints: dict[str, dict],
    syll_records: list[dict],
    pool_yaml_cache: dict[str, dict],
    lm_cache: dict[str, ExternalPhonemeModel],
) -> dict:
    """Run LOO + cross-pool L3 reclassification on a single chic-v2
    anchor. Returns a result dict with per-pool L3 winning classes,
    ``corroborated_by``, and the chic-v14 reclassification verdict.
    """
    target_meta = next(
        a for a in anchor_records_full if a["chic_sign"] == target_sid
    )
    known_value = target_meta["linear_b_carryover_phonetic"]
    known_class = classify_value(known_value)

    reduced_anchors = [
        a for a in anchor_records_full if a["chic_sign"] != target_sid
    ]
    reduced_mapping = build_anchor_mapping(reduced_anchors)

    # L1 + L2 — chic-v9 machinery, kept here for audit / table context.
    anchor_distance = compute_anchor_distance_map(
        fingerprints,
        anchor_records=reduced_anchors,
        unknown_ids=[target_sid],
        top_k=TOP_K_NEAREST,
    )
    nearest = anchor_distance.get(target_sid, [])
    if nearest:
        l1_class = _plurality_class(nearest)
        top1 = nearest[0]
        l2_class = (
            top1["anchor_class"] if top1["anchor_class"] != "unknown" else None
        )
    else:
        l1_class = None
        l2_class = None

    # L3 cross-pool — rebuild candidate-value pool per (LOO iteration,
    # substrate pool); the class-disjoint control mapping inside
    # ``compute_substrate_consistency`` is therefore automatically
    # rebuilt per cell (chic-v14 brief: "do not cache controls across
    # iterations").
    per_pool: OrderedDict[str, dict] = OrderedDict()
    for pool_name, _pool_path, lm_path in POOL_DISPATCH:
        pool_yaml = pool_yaml_cache[pool_name]
        value_pool = candidate_value_pool(reduced_anchors, pool_yaml)
        lm = lm_cache[str(lm_path)]
        substrate = compute_substrate_consistency(
            syll_records=syll_records,
            anchor_mapping=reduced_mapping,
            unknown_ids=[target_sid],
            value_pool=value_pool,
            lm=lm,
        )
        sub_rows = substrate.get(target_sid, [])
        class_agg = aggregate_class_means(sub_rows)
        if class_agg:
            winning_class = class_agg[0]["class"]
            winning_value = class_agg[0]["best_candidate"]
            winning_diff = class_agg[0]["mean_paired_diff"]
        else:
            winning_class = None
            winning_value = None
            winning_diff = None
        class_means: dict[str, float | None] = {c: None for c in CLASS_ORDER}
        for row in class_agg:
            class_means[row["class"]] = row["mean_paired_diff"]
        per_pool[pool_name] = {
            "pool_name": pool_name,
            "lm_path": str(lm_path.relative_to(ROOT)),
            "value_pool_size": len(value_pool),
            "known_class_in_value_pool": any(
                classify_value(v) == known_class for v in value_pool
            ),
            "winning_class": winning_class,
            "winning_value": winning_value,
            "winning_paired_diff": winning_diff,
            "per_class_mean_paired_diff": class_means,
        }

    # chic-v12 reclassification rule, with reference = known class.
    eteo_class = per_pool["eteocretan"]["winning_class"]
    non_eteo_lms = [p for p in per_pool if p != "eteocretan"]
    corroborated_by = [
        p for p in non_eteo_lms
        if per_pool[p]["winning_class"] == known_class
    ]
    eteo_corroborates = (eteo_class == known_class)
    if corroborated_by:
        reclassification = "tier-2-equivalent"
    elif eteo_corroborates:
        reclassification = "tier-3-corroborated"
    else:
        reclassification = "tier-3-uncorroborated"

    # Per-pool vote tally (informational).
    votes: Counter = Counter()
    for p in per_pool:
        cls = per_pool[p]["winning_class"]
        if cls:
            votes[cls] += 1

    return {
        "anchor": target_sid,
        "frequency": target_meta["frequency"],
        "confidence_tier": target_meta["confidence_tier"],
        "known_value": known_value,
        "known_class": known_class,
        "l1_class": l1_class,
        "l2_class": l2_class,
        "per_pool": per_pool,
        "corroborated_by": corroborated_by,
        "eteocretan_corroborates": eteo_corroborates,
        "reclassification": reclassification,
        "is_tier_2_equivalent": reclassification == "tier-2-equivalent",
        "cross_pool_votes": dict(votes),
    }


# ---------------------------------------------------------------------------
# Aggregate accounting
# ---------------------------------------------------------------------------


def aggregate_metrics(rows: list[dict]) -> dict:
    n_total = len(rows)
    counts: Counter = Counter(r["reclassification"] for r in rows)
    n_t2e = counts["tier-2-equivalent"]
    n_t3c = counts["tier-3-corroborated"]
    n_t3u = counts["tier-3-uncorroborated"]

    pct_t2e = (100.0 * n_t2e / n_total) if n_total else 0.0
    pct_t3c = (100.0 * n_t3c / n_total) if n_total else 0.0
    pct_t3u = (100.0 * n_t3u / n_total) if n_total else 0.0

    baseline_n, baseline_d = CHIC_V12_BASELINE
    baseline_pct = 100.0 * baseline_n / baseline_d

    # Comparison band (per the chic-v14 brief). The LOO recovery rate
    # is THE baseline; chic-v12's 27.6% is the test value being
    # compared to the baseline. ``above-baseline`` = chic-v12 above
    # the LOO baseline (meaningful: chic-v12's tier-3 reclassifications
    # get cross-pool corroboration at a higher rate than even ground-
    # truth-on-known-anchors does). ``below-baseline`` = chic-v12 below
    # the LOO baseline (anti-evidentiary: cross-pool L3 recovers known
    # classes far more often than it corroborates the chic-v5 proposed
    # class on the tier-3 set, so chic-v12's 27.6% is a low-power
    # subsampling of what cross-pool L3 reliably corroborates).
    chic_v12_minus_loo_pct = baseline_pct - pct_t2e
    if abs(chic_v12_minus_loo_pct) <= 5.0:
        comparison = "at-baseline"
    elif chic_v12_minus_loo_pct > 5.0:
        comparison = "above-baseline"
    else:
        comparison = "below-baseline"

    return {
        "n_total": n_total,
        "n_tier_2_equivalent": n_t2e,
        "n_tier_3_corroborated": n_t3c,
        "n_tier_3_uncorroborated": n_t3u,
        "cross_pool_l3_recovery_rate": pct_t2e,
        "eteocretan_only_recovery_rate": pct_t3c,
        "no_corroboration_rate": pct_t3u,
        "chic_v12_baseline_pct": baseline_pct,
        "chic_v12_baseline_n": baseline_n,
        "chic_v12_baseline_d": baseline_d,
        "chic_v12_minus_loo_pct": chic_v12_minus_loo_pct,
        "comparison": comparison,
    }


# ---------------------------------------------------------------------------
# Markdown writers
# ---------------------------------------------------------------------------


def _format_paired_diff(v: float | None) -> str:
    if v is None:
        return "—"
    return f"{v:+.6f}"


def _comparison_phrase(comparison: str) -> str:
    """Phrase for the inline summary line. The comparison band is
    expressed *from chic-v12's perspective*: ``above-baseline`` =
    chic-v12 above the chic-v14 LOO baseline (meaningful);
    ``below-baseline`` = chic-v12 below the chic-v14 LOO baseline
    (anti-evidentiary).
    """
    if comparison == "above-baseline":
        return "**above** the chic-v14 LOO baseline"
    if comparison == "below-baseline":
        return "**below** the chic-v14 LOO baseline"
    return "**at** the chic-v14 LOO baseline (within ±5pp)"


def write_loo_validation_md(
    rows: list[dict], summary: dict, *, n_anchors: int, out_path: Path,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v12 cross-pool L3 reclassification leave-one-out "
      "validation against chic-v2 anchors (chic-v14; mg-7f57)")
    a("")
    a("## Method")
    a("")
    a(
        f"For each of the {n_anchors} chic-v2 paleographic anchors S "
        f"with known LB-carryover value V (and known phoneme class C), "
        f"S is held out in-memory (the chic-v2 anchor pool yaml is "
        f"read-only) and treated as the single unknown sign by the "
        f"chic-v12 cross-pool L3 reclassification machinery, run "
        f"against the reduced {n_anchors - 1}-anchor pool. For each of "
        f"the 4 substrate pools (aquitanian / etruscan / toponym / "
        f"eteocretan) a fresh candidate-value pool is built from the "
        f"reduced anchor pool's distinct LB-carryover values + bare "
        f"vowels, filtered by the substrate pool's phoneme inventory "
        f"(chic-v5 convention). The class-disjoint sha256-keyed control "
        f"mapping inside ``compute_substrate_consistency`` is "
        f"regenerated per (LOO iteration, pool) cell because the "
        f"candidate-value pool is rebuilt per iteration; controls are "
        f"not cached across iterations (chic-v14 brief)."
    )
    a("")
    a(
        "Per-pool L3 winning class is the per-class argmax of the mean "
        "paired_diff over surviving candidate values. The chic-v12 "
        "reclassification rule is then applied with the held-out "
        "anchor's **known** class as the reference class (in chic-v12 "
        "the reference was the chic-v5 proposed class):"
    )
    a("")
    a("- ``corroborated_by`` = list of non-Eteocretan substrate LMs "
      "whose winning class matches the held-out anchor's known class.")
    a("- ``eteocretan_corroborates`` = (Eteocretan-L3 winning class == "
      "known class).")
    a("- ``reclassification`` = ``tier-2-equivalent`` if "
      "``corroborated_by`` is non-empty; ``tier-3-corroborated`` if "
      "only Eteocretan-L3 corroborates; ``tier-3-uncorroborated`` "
      "otherwise.")
    a("")
    a(
        "L1 (distributional plurality, top-3 nearest anchors) and L2 "
        "(strict-top-1 anchor distance) are recomputed per LOO iteration "
        "for audit context (same machinery as chic-v9), but the "
        "chic-v14 verdict is purely a function of the cross-pool L3 "
        "reclassification — L1 + L2 are surfaced in the per-anchor "
        "table only. L4 (cross-script paleographic) is excluded by "
        "construction (chic-v9 precedent): the chic-v1 "
        "PALEOGRAPHIC_CANDIDATES list is the source of the chic-v2 "
        "anchor pool, so for any anchor S the L4 line trivially "
        "recovers V — including L4 would inflate accuracy by "
        "construction."
    )
    a("")

    # ---- Headline aggregate metrics ----
    a("## Headline aggregate metrics")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(f"| n anchors run blind | {summary['n_total']} |")
    a(
        f"| **cross_pool_l3_recovery_rate** "
        f"(fraction reclassifying to tier-2-equivalent under LOO) | "
        f"**{summary['n_tier_2_equivalent']}/{summary['n_total']} = "
        f"{summary['cross_pool_l3_recovery_rate']:.1f}%** |"
    )
    a(
        f"| eteocretan_only_recovery_rate (fraction reclassifying to "
        f"tier-3-corroborated) | "
        f"{summary['n_tier_3_corroborated']}/{summary['n_total']} = "
        f"{summary['eteocretan_only_recovery_rate']:.1f}% |"
    )
    a(
        f"| no_corroboration_rate (fraction reclassifying to "
        f"tier-3-uncorroborated) | "
        f"{summary['n_tier_3_uncorroborated']}/{summary['n_total']} = "
        f"{summary['no_corroboration_rate']:.1f}% |"
    )
    a(
        f"| chic-v12 reclassification rate (8 of 29 tier-3 candidates) | "
        f"{summary['chic_v12_baseline_n']}/"
        f"{summary['chic_v12_baseline_d']} = "
        f"{summary['chic_v12_baseline_pct']:.1f}% |"
    )
    a(
        f"| **chic-v12 minus LOO baseline** | "
        f"**{summary['chic_v12_minus_loo_pct']:+.1f}pp "
        f"({summary['comparison']})** |"
    )
    a("")
    a(
        f"The chic-v12 reclassification rate "
        f"({summary['chic_v12_baseline_pct']:.1f}%) is "
        f"{_comparison_phrase(summary['comparison'])} "
        f"({summary['chic_v12_baseline_pct']:.1f}% chic-v12 vs "
        f"{summary['cross_pool_l3_recovery_rate']:.1f}% chic-v14 LOO; "
        f"chic-v12 minus LOO = "
        f"{summary['chic_v12_minus_loo_pct']:+.1f}pp; "
        f"|delta| ≤ 5pp = at-baseline). "
        f"See the verdict subsection below for the implication."
    )
    a("")

    # ---- Per-anchor LOO results ----
    a("## Per-anchor LOO results")
    a("")
    a(
        "Each row is one LOO iteration: the named anchor was removed "
        "from the chic-v2 pool and treated as the single unknown sign; "
        "the 4 substrate-pool LMs each computed an L3 winning class for "
        "the held-out anchor against the reduced 19-anchor mapping. "
        "``corroborated_by`` lists non-Eteocretan substrate LMs whose "
        "winning class matches the held-out anchor's known class. "
        "``reclassification`` is the chic-v12 verdict with the known "
        "class as reference. L1 + L2 columns are chic-v9 audit context."
    )
    a("")
    a("| anchor | freq | known phoneme | known class | L1 | L2 | "
      "Eteocretan-L3 | Aquitanian-L3 | Etruscan-L3 | toponym-L3 | "
      "corroborated_by | reclassification |")
    a("|---|---:|---|---|---|---|---|---|---|---|---|---|")
    rows_sorted = sorted(rows, key=lambda r: int(r["anchor"].lstrip("#")))
    for r in rows_sorted:
        l1 = r["l1_class"] or "—"
        l2 = r["l2_class"] or "—"
        eteo = r["per_pool"]["eteocretan"]["winning_class"] or "—"
        aqui = r["per_pool"]["aquitanian"]["winning_class"] or "—"
        etru = r["per_pool"]["etruscan"]["winning_class"] or "—"
        topo = r["per_pool"]["toponym"]["winning_class"] or "—"
        # Mark held-out class as unrecoverable in a pool's value pool
        # with ⚠ on that pool's column so the reader sees it.
        for pool_name, col_label in (
            ("eteocretan", "eteo"),
            ("aquitanian", "aqui"),
            ("etruscan", "etru"),
            ("toponym", "topo"),
        ):
            if not r["per_pool"][pool_name]["known_class_in_value_pool"]:
                if col_label == "eteo":
                    eteo = f"{eteo} ⚠"
                elif col_label == "aqui":
                    aqui = f"{aqui} ⚠"
                elif col_label == "etru":
                    etru = f"{etru} ⚠"
                elif col_label == "topo":
                    topo = f"{topo} ⚠"
        corroborated = ", ".join(r["corroborated_by"]) or "—"
        a(
            f"| `{r['anchor']}` | {r['frequency']} | "
            f"`{r['known_value']}` | {r['known_class']} | "
            f"{l1} | {l2} | "
            f"{eteo} | {aqui} | {etru} | {topo} | "
            f"{corroborated} | {r['reclassification']} |"
        )
    a("")
    n_unrecoverable = sum(
        1 for r in rows
        if not all(
            r["per_pool"][p]["known_class_in_value_pool"]
            for p in ("eteocretan", "aquitanian", "etruscan", "toponym")
        )
    )
    a(
        f"⚠ on a pool's L3 column indicates that the held-out anchor's "
        f"class had no representative in that pool's rebuilt 19-anchor "
        f"candidate-value pool, so the L3 vote for that pool was "
        f"structurally unable to recover the class. Total LOO "
        f"iterations with at least one such pool: {n_unrecoverable}/"
        f"{summary['n_total']}."
    )
    a("")

    # ---- Per-anchor per-pool per-class detail ----
    a("## Per-anchor per-pool per-class mean paired_diff")
    a("")
    a(
        "Detail-table view of the 20 × 4 = 80 cells. Each row is one "
        "(LOO iteration, pool) cell; columns are per-class mean "
        "paired_diff over the surviving candidate values for that "
        "pool's filter. ``winning class`` is the per-class argmax. "
        "``—`` for a class indicates the class is empty in the rebuilt "
        "candidate-value pool for that substrate (e.g. ``glide`` for "
        "aquitanian / etruscan / toponym, since their candidate pools "
        "exclude `wa` / `ja` / `je` by inventory filter; this is a "
        "structural property of those pools, not an L3 finding)."
    )
    a("")
    for r in rows_sorted:
        a(
            f"### `{r['anchor']}` (known: `{r['known_value']}`, "
            f"class: {r['known_class']}; reclassification: "
            f"**{r['reclassification']}**; corroborated_by: "
            f"{', '.join(r['corroborated_by']) or '—'})"
        )
        a("")
        a(
            "| pool | LM | winning class | winning value | "
            "winning paired_diff | "
            + " | ".join(f"mean({c})" for c in CLASS_ORDER) + " |"
        )
        a(
            "|---|---|---|---|---:|"
            + "|".join("---:" for _ in CLASS_ORDER) + "|"
        )
        for pool_name, _pp, lm_path in POOL_DISPATCH:
            cell = r["per_pool"][pool_name]
            wc = cell["winning_class"] or "—"
            wv = f"`{cell['winning_value']}`" if cell["winning_value"] else "—"
            wd = _format_paired_diff(cell["winning_paired_diff"])
            cls_cells = [
                _format_paired_diff(cell["per_class_mean_paired_diff"].get(c))
                for c in CLASS_ORDER
            ]
            a(
                f"| {pool_name} | `{lm_path.name}` | {wc} | {wv} | "
                f"{wd} | " + " | ".join(cls_cells) + " |"
            )
        a("")

    # ---- Verdict ----
    a("## Verdict — chic-v12 vs chic-v14 LOO baseline")
    a("")
    if summary["comparison"] == "above-baseline":
        a(
            f"**The chic-v14 LOO cross-pool L3 recovery rate on known "
            f"anchors is {summary['cross_pool_l3_recovery_rate']:.1f}%, "
            f"so chic-v12's {summary['chic_v12_baseline_pct']:.1f}% "
            f"reclassification rate on the 29 tier-3 candidates is "
            f"{summary['chic_v12_minus_loo_pct']:+.1f}pp ABOVE the LOO "
            f"baseline.** Cross-pool L3 corroborates ground-truth class "
            f"on known anchors at a *lower* rate than chic-v12 "
            f"corroborates the chic-v5 proposed class on the tier-3 "
            f"set. Read against the chic-v14 brief's interpretation "
            f"framework (\"if LOO shows 5%, the 27.6% is meaningfully "
            f"above baseline\"): the chic-v12 reclassification picks up "
            f"a band of candidates that get cross-pool corroboration "
            f"at a higher rate than even ground-truth-on-known-anchors "
            f"does. Provisionally **above-baseline / meaningful**, but "
            f"at small N (20 anchors) and with the chic-v9 framework-"
            f"level negative still in force (LOO accuracy 20.0% on "
            f"the L1+L2+L3 framework), the signal must be read in "
            f"that wider context."
        )
    elif summary["comparison"] == "below-baseline":
        a(
            f"**The chic-v14 LOO cross-pool L3 recovery rate on known "
            f"anchors is {summary['cross_pool_l3_recovery_rate']:.1f}%, "
            f"so chic-v12's {summary['chic_v12_baseline_pct']:.1f}% "
            f"reclassification rate on the 29 tier-3 candidates is "
            f"{summary['chic_v12_minus_loo_pct']:+.1f}pp BELOW the LOO "
            f"baseline.** Cross-pool L3 corroborates the held-out "
            f"anchor's known class **more often** than chic-v12 "
            f"corroborates the chic-v5 proposed class on the tier-3 "
            f"set. Read against the chic-v14 brief's interpretation "
            f"framework (\"if LOO shows 80%, the 27.6% is below "
            f"baseline and the reclassification is anti-evidentiary\"): "
            f"the cross-pool L3 axis recovers ground-truth class far "
            f"more often than it corroborates the chic-v5 proposed "
            f"class on the tier-3 set, so chic-v12's reclassification "
            f"is below the rate we'd see if the proposed classes were "
            f"correct — **anti-evidentiary on the tier-3 set**. "
            f"chic-v13's context inspection (sibling ticket) becomes "
            f"the load-bearing pillar; cross-pool L3 alone is no longer "
            f"the dominant evidence axis on the tier-3 set."
        )
    else:
        a(
            f"**The chic-v14 LOO cross-pool L3 recovery rate on known "
            f"anchors is {summary['cross_pool_l3_recovery_rate']:.1f}%, "
            f"and chic-v12's {summary['chic_v12_baseline_pct']:.1f}% "
            f"reclassification rate on the 29 tier-3 candidates differs "
            f"by {summary['chic_v12_minus_loo_pct']:+.1f}pp — within "
            f"the ±5pp at-baseline band.** The cross-pool L3 axis "
            f"corroborates ground-truth class on known anchors at "
            f"approximately the same rate that chic-v12 corroborates "
            f"the chic-v5 proposed class on the tier-3 set. Read "
            f"against the chic-v14 brief's interpretation framework: "
            f"this is consistent with the cross-pool L3 axis being a "
            f"low-discrimination test — both ground-truth and chic-v5 "
            f"proposals get corroborated at roughly the same rate, so "
            f"the chic-v12 27.6% reclassification rate is **not above-"
            f"baseline evidence** of any specific candidate's class "
            f"correctness. The chic-v9 framework-level negative remains "
            f"the dominant constraint; chic-v13's context inspection "
            f"(sibling ticket) becomes load-bearing."
        )
    a("")

    # ---- Caveats ----
    a("## Caveats")
    a("")
    a(
        "- **Cross-pool L3 only — L1+L2 columns are audit context.** "
        "The chic-v14 verdict is computed from cross-pool L3 alone, "
        "matching the chic-v12 reclassification rule's structure. "
        "L1+L2 LOO accuracy is reported by chic-v9 (mg-18cb) and is "
        "not re-summarized here."
    )
    a(
        "- **Class-level resolution.** The reclassification predicate "
        "is class-level (vowel / stop / nasal / liquid / fricative / "
        "glide), matching chic-v12's class-level resolution. The LOO "
        "test does not adjudicate specific phoneme value (`ja` vs "
        "`je` vs `wa` within glide; `pa` vs `ta` vs `ka` within stop)."
    )
    a(
        "- **Per-pool candidate-pool reduction.** Each pool's "
        "rebuilt-per-iteration candidate-value pool removes the held-"
        "out anchor's value (unless another anchor shares it; in "
        "this corpus only `ke` is shared, between `#019` and `#092`). "
        "When the held-out class has no other representative in a "
        "specific pool's rebuilt candidate pool, that pool's L3 vote "
        "cannot recover the class by construction — flagged with ⚠ "
        "in the per-anchor table."
    )
    a(
        "- **Class-disjoint deterministic-permutation control.** The "
        "control phoneme for each (sign, candidate) pair is a sha256-"
        "keyed class-disjoint pick from the per-iteration candidate-"
        "value pool. The pool itself is rebuilt per LOO iteration, so "
        "controls are automatically per-iteration; no caching across "
        "iterations (chic-v14 brief)."
    )
    a(
        "- **Small N (20 anchors).** The LOO baseline is a 20-anchor "
        "rate; binomial noise on 20 trials is substantial. A ±5pp "
        "at-baseline band is a coarse approximation to that noise "
        "floor — finer comparisons should not be drawn from this "
        "test alone. The chic-v9 framework-level negative (LOO "
        "accuracy 20.0% on the L1+L2+L3 framework) sets the upper "
        "bound on what chic-v14's per-axis LOO can establish."
    )
    a(
        "- **Anchor-pool composition bias.** The chic-v2 anchor pool "
        "is the chic-v1 paleographic-candidate list (curated). The "
        "LOO baseline measures cross-pool L3 corroboration on "
        "**anchor-shaped** signs, which may differ systematically from "
        "the 76 unknown signs the chic-v5 framework targets. The "
        "comparison to chic-v12's 27.6% on the tier-3 set is the "
        "intended axis of read."
    )
    a(
        "- **Comparison band semantics.** The LOO recovery rate is the "
        "**baseline**; chic-v12's 27.6% is the test value. "
        "``above-baseline`` = chic-v12 above LOO by > 5pp (meaningful: "
        "chic-v12 reclassifies *more* than ground-truth-LOO does, "
        "picking up a high-corroboration band). ``below-baseline`` = "
        "chic-v12 below LOO by > 5pp (anti-evidentiary: cross-pool L3 "
        "corroborates ground-truth more often than it corroborates "
        "chic-v12 proposals). ``at-baseline`` = |chic-v12 − LOO| ≤ 5pp."
    )
    a("")

    # ---- Determinism + provenance ----
    a("## Determinism")
    a("")
    a(
        "- No RNG. The L3 control-phoneme selection inherits chic-v5's "
        "sha256-keyed permutation construction; LOO iteration order is "
        "sorted by anchor numeric id; cross-pool dispatch is fixed in "
        "POOL_DISPATCH."
    )
    a(
        "- Same inputs → byte-identical output. Re-running this script "
        "overwrites the result files with byte-identical content."
    )
    a("")
    a("## Citations")
    a("")
    a("- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum "
      "Inscriptionum Cretae* (Études Crétoises 31). Paris.")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")
    a("- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* "
      "Amsterdam: J. C. Gieben.")
    a("- Trask, R. L. (1997). *The History of Basque.* London: Routledge.")
    a("- Bonfante, G. & Bonfante, L. (2002). *The Etruscan Language: "
      "An Introduction* (revised ed.). Manchester / New York.")
    a("- Beekes, R. S. P. (2010). *Etymological Dictionary of Greek*, "
      "vol. 2 appendix on Pre-Greek substrate. Leiden: Brill.")
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v14.py` (mg-7f57).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); "
      "`corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); "
      "`pools/cretan_hieroglyphic_signs.yaml` (chic-v1); "
      "`pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); "
      "`pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; "
      "`harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary_md(
    rows: list[dict], summary: dict, *, out_path: Path,
) -> None:
    """1-paragraph plain-English verdict + headline-count table."""
    rows_sorted = sorted(rows, key=lambda r: int(r["anchor"].lstrip("#")))
    t2e = [r["anchor"] for r in rows_sorted if r["reclassification"] == "tier-2-equivalent"]
    t3c = [r["anchor"] for r in rows_sorted if r["reclassification"] == "tier-3-corroborated"]
    t3u = [r["anchor"] for r in rows_sorted if r["reclassification"] == "tier-3-uncorroborated"]

    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v12 cross-pool L3 reclassification LOO summary "
      "(chic-v14; mg-7f57)")
    a("")
    a("## Headline counts")
    a("")
    a("| reclassification | n | meaning |")
    a("|---|---:|---|")
    a(
        f"| **tier-2-equivalent** | **{summary['n_tier_2_equivalent']}** "
        f"| ≥ 1 non-Eteocretan substrate LM corroborates the "
        f"held-out anchor's known class. |"
    )
    a(
        f"| tier-3-corroborated | {summary['n_tier_3_corroborated']} | "
        f"Only Eteocretan-L3 corroborates the known class. |"
    )
    a(
        f"| tier-3-uncorroborated | "
        f"{summary['n_tier_3_uncorroborated']} | "
        f"No LM's L3 corroborates the known class. |"
    )
    a(f"| **total LOO iterations** | **{summary['n_total']}** | "
      "(20 chic-v2 anchors) |")
    a("")
    a("## Comparison to chic-v12 baseline")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(
        f"| **chic-v14 cross_pool_l3_recovery_rate** | "
        f"**{summary['n_tier_2_equivalent']}/{summary['n_total']} = "
        f"{summary['cross_pool_l3_recovery_rate']:.1f}%** |"
    )
    a(
        f"| chic-v12 reclassification rate (8 of 29 tier-3) | "
        f"{summary['chic_v12_baseline_n']}/"
        f"{summary['chic_v12_baseline_d']} = "
        f"{summary['chic_v12_baseline_pct']:.1f}% |"
    )
    a(
        f"| **delta (chic-v12 − chic-v14 LOO)** | "
        f"**{summary['chic_v12_minus_loo_pct']:+.1f}pp** |"
    )
    a(
        f"| **comparison band** | **{summary['comparison']}** |"
    )
    a("")
    a("## Plain-English verdict")
    a("")
    if summary["comparison"] == "above-baseline":
        verdict_p = (
            f"chic-v14's leave-one-out test of the chic-v12 cross-pool "
            f"L3 reclassification rule on the 20 chic-v2 paleographic "
            f"anchors recovers the held-out anchor's known class "
            f"(reclassifies to ``tier-2-equivalent``) on "
            f"{summary['n_tier_2_equivalent']} of {summary['n_total']} "
            f"runs ({summary['cross_pool_l3_recovery_rate']:.1f}%). "
            f"chic-v12's {summary['chic_v12_baseline_pct']:.1f}% rate "
            f"on the 29 tier-3 candidates is therefore "
            f"{summary['chic_v12_minus_loo_pct']:+.1f}pp **above** the "
            f"LOO baseline: chic-v12 reclassifies tier-3 candidates "
            f"to tier-2-equivalent more often than cross-pool L3 "
            f"corroborates ground-truth class on known anchors, so "
            f"the chic-v12 reclassification picks up a band of "
            f"candidates with elevated cross-pool support relative to "
            f"the LOO noise floor. Read provisionally as **above-"
            f"baseline / meaningful**, caveated by 20-anchor noise on "
            f"the LOO baseline and the chic-v9 framework-level LOO "
            f"accuracy of 20.0%."
        )
    elif summary["comparison"] == "below-baseline":
        verdict_p = (
            f"chic-v14's leave-one-out test of the chic-v12 cross-pool "
            f"L3 reclassification rule on the 20 chic-v2 paleographic "
            f"anchors recovers the held-out anchor's known class "
            f"(reclassifies to ``tier-2-equivalent``) on "
            f"{summary['n_tier_2_equivalent']} of {summary['n_total']} "
            f"runs ({summary['cross_pool_l3_recovery_rate']:.1f}%). "
            f"chic-v12's {summary['chic_v12_baseline_pct']:.1f}% rate "
            f"on the 29 tier-3 candidates is therefore "
            f"{summary['chic_v12_minus_loo_pct']:+.1f}pp **below** the "
            f"LOO baseline: cross-pool L3 corroborates ground-truth "
            f"class on known anchors more often than chic-v12 "
            f"corroborates the chic-v5 proposed class on the tier-3 "
            f"set, so the chic-v12 reclassification is below the rate "
            f"we'd see if the proposed classes were correct — "
            f"**anti-evidentiary on the tier-3 set**. chic-v13's "
            f"context inspection (sibling ticket) becomes the load-"
            f"bearing pillar; cross-pool L3 alone is no longer the "
            f"dominant evidence axis on the tier-3 set."
        )
    else:
        verdict_p = (
            f"chic-v14's leave-one-out test of the chic-v12 cross-pool "
            f"L3 reclassification rule on the 20 chic-v2 paleographic "
            f"anchors recovers the held-out anchor's known class "
            f"(reclassifies to ``tier-2-equivalent``) on "
            f"{summary['n_tier_2_equivalent']} of {summary['n_total']} "
            f"runs ({summary['cross_pool_l3_recovery_rate']:.1f}%). "
            f"chic-v12's {summary['chic_v12_baseline_pct']:.1f}% rate "
            f"on the 29 tier-3 candidates differs from this LOO "
            f"baseline by {summary['chic_v12_minus_loo_pct']:+.1f}pp — "
            f"**within the ±5pp at-baseline band**. The cross-pool L3 "
            f"axis corroborates ground-truth class on known anchors at "
            f"approximately the same rate that chic-v12 corroborates "
            f"the chic-v5 proposed class on the tier-3 set; the "
            f"chic-v12 27.6% is consistent with a generic property of "
            f"the cross-pool L3 axis, not above-baseline evidence of "
            f"any specific candidate's class correctness. The chic-v9 "
            f"framework-level negative remains the dominant constraint; "
            f"chic-v13's context inspection (sibling ticket) becomes "
            f"load-bearing."
        )
    a(verdict_p)
    a("")

    # Cite specific anchors that did and did not reclassify (per the
    # chic-v14 brief).
    a("## Specific anchors")
    a("")
    a(
        f"- **Reclassified to tier-2-equivalent** "
        f"({len(t2e)}): "
        f"{', '.join('`' + s + '`' for s in t2e) or '(none)'}."
    )
    a(
        f"- **Reclassified to tier-3-corroborated** "
        f"({len(t3c)}): "
        f"{', '.join('`' + s + '`' for s in t3c) or '(none)'}."
    )
    a(
        f"- **Reclassified to tier-3-uncorroborated** "
        f"({len(t3u)}): "
        f"{', '.join('`' + s + '`' for s in t3u) or '(none)'}."
    )
    a("")

    a("## Cross-references")
    a("")
    a(
        "- Per-anchor LOO table + per-pool per-class mean paired_diff "
        "details: `results/chic_v14_loo_validation.md`."
    )
    a(
        "- chic-v12 cross-pool L3 reclassification of the 29 chic-v5 "
        "tier-3 candidates (the methodology this LOO tests): "
        "`results/chic_v12_cross_pool_l3.md`, "
        "`results/chic_v12_tier3_summary.md`."
    )
    a(
        "- chic-v9 LOO validation of the chic-v5 four-line framework "
        "(the methodologically symmetric prior LOO): "
        "`results/chic_v9_loo_validation.md`."
    )
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v14.py` (mg-7f57).")
    a(f"- fetched_at: {FETCHED_AT}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(*, progress: bool = True) -> dict:
    if progress:
        print("chic-v14: loading inputs...", file=sys.stderr)
    full_records = load_chic_records(CHIC_FULL)
    syll_records = load_chic_records(CHIC_SYLL)
    signs_yaml = _load_yaml(SIGNS_YAML)
    anchors_yaml = _load_yaml(ANCHORS_YAML)

    syllabographic_ids = {
        s["id"] for s in signs_yaml["signs"]
        if s["sign_class"] == "syllabographic"
    }
    anchor_records_full = anchors_yaml["anchors"]

    # Cache pool yamls and LM artifacts (read-only across LOO; the
    # candidate-value pool itself is rebuilt per iteration).
    pool_yaml_cache: dict[str, dict] = {}
    lm_cache: dict[str, ExternalPhonemeModel] = {}
    for pool_name, pool_path, lm_path in POOL_DISPATCH:
        pool_yaml_cache[pool_name] = _load_yaml(pool_path)
        if str(lm_path) not in lm_cache:
            lm_cache[str(lm_path)] = ExternalPhonemeModel.load_json(lm_path)

    if progress:
        print(
            f"  syllabographic={len(syllabographic_ids)} "
            f"anchors={len(anchor_records_full)} "
            f"pools={len(POOL_DISPATCH)} lms={len(lm_cache)}",
            file=sys.stderr,
        )

    if progress:
        print(
            "chic-v14: computing per-sign distributional fingerprints "
            "(for L1+L2 audit context)...",
            file=sys.stderr,
        )
    fingerprints = compute_fingerprints(
        full_records, syllabographic_ids=syllabographic_ids,
    )

    rows: list[dict] = []
    sorted_anchors = sorted(
        anchor_records_full, key=lambda a: int(a["chic_sign"].lstrip("#")),
    )
    for i, anchor in enumerate(sorted_anchors):
        target_sid = anchor["chic_sign"]
        if progress:
            print(
                f"chic-v14: LOO {i + 1}/{len(sorted_anchors)} "
                f"holding out {target_sid} "
                f"(known={anchor['linear_b_carryover_phonetic']}, "
                f"class={classify_value(anchor['linear_b_carryover_phonetic'])})...",
                file=sys.stderr,
            )
        row = loo_cross_pool_l3_anchor(
            target_sid=target_sid,
            anchor_records_full=anchor_records_full,
            fingerprints=fingerprints,
            syll_records=syll_records,
            pool_yaml_cache=pool_yaml_cache,
            lm_cache=lm_cache,
        )
        rows.append(row)

    summary = aggregate_metrics(rows)

    if progress:
        print(
            "chic-v14: writing outputs...",
            file=sys.stderr,
        )
    write_loo_validation_md(
        rows, summary, n_anchors=len(anchor_records_full), out_path=OUT_LOO_MD,
    )
    write_summary_md(rows, summary, out_path=OUT_SUMMARY_MD)

    if progress:
        print(
            f"chic-v14 done | n={summary['n_total']} "
            f"tier-2-equivalent="
            f"{summary['n_tier_2_equivalent']}/{summary['n_total']} "
            f"({summary['cross_pool_l3_recovery_rate']:.1f}%) "
            f"vs chic-v12 baseline "
            f"({summary['chic_v12_baseline_pct']:.1f}%) "
            f"chic_v12_minus_loo={summary['chic_v12_minus_loo_pct']:+.1f}pp "
            f"comparison={summary['comparison']}",
            file=sys.stderr,
        )
    return {"rows": rows, "summary": summary}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--no-progress", action="store_true")
    args = p.parse_args(argv)
    out = run(progress=not args.no_progress)
    summary = out["summary"]
    payload = {
        "n_total": summary["n_total"],
        "n_tier_2_equivalent": summary["n_tier_2_equivalent"],
        "n_tier_3_corroborated": summary["n_tier_3_corroborated"],
        "n_tier_3_uncorroborated": summary["n_tier_3_uncorroborated"],
        "cross_pool_l3_recovery_rate": round(
            summary["cross_pool_l3_recovery_rate"], 4
        ),
        "eteocretan_only_recovery_rate": round(
            summary["eteocretan_only_recovery_rate"], 4
        ),
        "no_corroboration_rate": round(summary["no_corroboration_rate"], 4),
        "chic_v12_baseline_pct": round(summary["chic_v12_baseline_pct"], 4),
        "chic_v12_minus_loo_pct": round(summary["chic_v12_minus_loo_pct"], 4),
        "comparison": summary["comparison"],
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
