#!/usr/bin/env python3
"""chic-v9: leave-one-out held-out validation of chic-v5 framework on
chic-v2 anchors (mg-18cb).

Daniel's observation (2026-05-05): the strong result of the chic
sub-program would be proposing 3 new values for Cretan Hieroglyphs
(chic-v5 tier-2: ``#001 -> wa``, ``#012 -> wa``, ``#032 -> ki/stop``)
"especially if we independently hypothesised known values". This is
the methodological move chic-v0..v5 never made: held-out validation
of the chic-v5 framework against the chic-v2 anchor pool, where the
known scholarly phoneme values let us measure the framework's
recovery accuracy on cases with ground truth.

Method
======

For each chic-v2 anchor sign S with known scholarly value V:

1. Remove S from the chic-v2 anchor pool (reduced 19-anchor pool).
2. Treat S as unknown in the chic-v5 framework. Rebuild the
   candidate-value pool from the reduced 19-anchor pool plus bare
   vowels (filtered by the Eteocretan phoneme inventory, just like
   chic-v5).
3. Compute L1 (distributional plurality vote on the top-K nearest
   anchors), L2 (strict-top-1 anchor distance), L3 (substrate-
   consistency under the v21 Eteocretan LM) for S, against the
   reduced pool.
4. L4 (cross-script paleographic) is **deliberately excluded**: L4
   is the source of the anchor pool itself; including it would be
   circular for the LOO test.
5. Apply chic-v5's tier classification using only L1+L2+L3:
   tier-2  3-of-3 unanimity on the top class
   tier-3  2-of-3 agreement
   tier-4  1-of-3 (single line of evidence)
   untiered  0 voting lines
6. Compare the framework's proposed phoneme class to S's known
   scholarly phoneme class. Aggregate per-anchor agreement,
   per-line accuracy, and tier-classification accuracy.

Per the brief, the candidate value pool is rebuilt from the reduced
19-anchor pool. This is the strict LOO setup: the held-out anchor's
value is removed from the candidate-value pool unless another anchor
shares the value (in this corpus only ``ke`` is shared, between
``#019`` and ``#092``). For 18 of 20 LOO runs the held-out value is
fully removed from the candidate pool, so L3 cannot recover the
value's specific phoneme — but it can still recover the *class* if
the class has another representative in the candidate pool. Where
the class itself disappears (e.g. holding out ``#042 = wa`` removes
the only glide value), L3 cannot recover the class either; this is a
structural property of the LOO setup and is reported honestly.

Inputs
======

- ``corpora/cretan_hieroglyphic/all.jsonl``           (chic-v0)
- ``corpora/cretan_hieroglyphic/syllabographic.jsonl`` (chic-v3)
- ``pools/cretan_hieroglyphic_signs.yaml``            (chic-v1)
- ``pools/cretan_hieroglyphic_anchors.yaml``          (chic-v2)
- ``pools/eteocretan.yaml``                           (Eteocretan
                                                       substrate-pool
                                                       phoneme inventory)
- ``harness/external_phoneme_models/eteocretan.json`` (v21 LM artifact)

Outputs
=======

- ``results/chic_v9_loo_validation.md``  per-anchor LOO result table,
  aggregate accuracy, per-line decomposition, tier-classification
  accuracy, implications for chic-v5 tier-2 candidates.

Determinism
===========

No RNG. Same inputs -> byte-identical outputs across re-runs. The
control-phoneme selection in compute_substrate_consistency uses a
sha256-keyed permutation (chic-v5 convention).

Usage
=====

    python3 scripts/build_chic_v9.py

The script is idempotent: re-running overwrites ``results/
chic_v9_loo_validation.md`` with byte-identical content given the
same inputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
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
ETEO_POOL_YAML = ROOT / "pools" / "eteocretan.yaml"
ETEO_LM = ROOT / "harness" / "external_phoneme_models" / "eteocretan.json"

OUT_MD = ROOT / "results" / "chic_v9_loo_validation.md"

FETCHED_AT = "2026-05-05T22:00:00Z"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _plurality_class(top_anchors: list[dict]) -> str | None:
    """Plurality class over the top-K nearest anchors. Tiebreak
    alphabetically (matches chic-v5)."""
    votes = Counter(
        a["anchor_class"] for a in top_anchors if a["anchor_class"] != "unknown"
    )
    if not votes:
        return None
    return sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def _classify_loo_tier(
    *,
    l1_class: str | None,
    l2_class: str | None,
    l3_class: str | None,
) -> tuple[int | None, str | None]:
    """LOO tier classification using L1+L2+L3 only (L4 excluded by
    construction). 3-of-3 -> tier-2; 2-of-3 -> tier-3; 1-of-3 ->
    tier-4; 0 -> untiered. Tiebreak alphabetically.
    """
    votes: Counter = Counter()
    for cls in (l1_class, l2_class, l3_class):
        if cls and cls != "unknown":
            votes[cls] += 1
    if not votes:
        return None, None
    top_class, top_count = sorted(
        votes.items(), key=lambda kv: (-kv[1], kv[0])
    )[0]
    if top_count >= 3:
        tier = 2
    elif top_count == 2:
        tier = 3
    elif top_count == 1:
        tier = 4
    else:
        tier = None
    return tier, top_class


def loo_validate_anchor(
    *,
    target_sid: str,
    anchor_records_full: list[dict],
    fingerprints: dict[str, dict],
    syll_records: list[dict],
    eteo_pool: dict,
    lm: ExternalPhonemeModel,
) -> dict:
    """Run the L1+L2+L3 LOO test for a single chic-v2 anchor sign.

    Returns a result dict containing the held-out anchor's known
    phoneme/class, the per-line LOO classes, the consensus class,
    and the LOO tier verdict.
    """
    target_meta = next(
        a for a in anchor_records_full if a["chic_sign"] == target_sid
    )
    known_value = target_meta["linear_b_carryover_phonetic"]
    known_class = classify_value(known_value)

    reduced_anchors = [
        a for a in anchor_records_full if a["chic_sign"] != target_sid
    ]

    # L1 + L2: anchor-distance against the reduced 19-anchor pool.
    anchor_distance = compute_anchor_distance_map(
        fingerprints,
        anchor_records=reduced_anchors,
        unknown_ids=[target_sid],
        top_k=TOP_K_NEAREST,
    )
    nearest = anchor_distance.get(target_sid, [])

    if nearest:
        l1_class = _plurality_class(nearest)
        # L2: strict top-1.
        top1 = nearest[0]
        l2_class = top1["anchor_class"] if top1["anchor_class"] != "unknown" else None
        l2_anchor = top1["anchor_id"]
        l2_value = top1["anchor_value"]
        l2_sim = top1["similarity"]
    else:
        l1_class = None
        l2_class = None
        l2_anchor = None
        l2_value = None
        l2_sim = None

    # L3: substrate-consistency under Eteocretan LM with reduced
    # 19-anchor mapping and reduced candidate-value pool.
    reduced_mapping = build_anchor_mapping(reduced_anchors)
    reduced_value_pool = candidate_value_pool(reduced_anchors, eteo_pool)
    substrate = compute_substrate_consistency(
        syll_records=syll_records,
        anchor_mapping=reduced_mapping,
        unknown_ids=[target_sid],
        value_pool=reduced_value_pool,
        lm=lm,
    )
    sub_rows = substrate.get(target_sid, [])
    l3_class = None
    l3_best_value = None
    l3_best_diff = None
    l3_target_class_in_pool = any(
        classify_value(v) == known_class for v in reduced_value_pool
    )
    if sub_rows:
        class_agg = aggregate_class_means(sub_rows)
        if class_agg:
            l3_class = class_agg[0]["class"]
            l3_best_value = class_agg[0]["best_candidate"]
            l3_best_diff = class_agg[0]["mean_paired_diff"]

    tier, framework_class = _classify_loo_tier(
        l1_class=l1_class, l2_class=l2_class, l3_class=l3_class,
    )

    return {
        "anchor": target_sid,
        "known_value": known_value,
        "known_class": known_class,
        "frequency": target_meta["frequency"],
        "confidence_tier": target_meta["confidence_tier"],
        "l1_class": l1_class,
        "l2_class": l2_class,
        "l2_top_anchor": l2_anchor,
        "l2_top_value": l2_value,
        "l2_top_similarity": l2_sim,
        "l3_class": l3_class,
        "l3_best_value": l3_best_value,
        "l3_best_paired_diff": l3_best_diff,
        "l3_target_class_in_pool": l3_target_class_in_pool,
        "tier": tier,
        "framework_class": framework_class,
        "agreement": framework_class is not None and framework_class == known_class,
    }


def write_loo_validation_md(
    rows: list[dict],
    *,
    n_anchors: int,
    out_path: Path,
) -> dict:
    """Write the LOO validation markdown and return a summary dict."""
    n_total = len(rows)
    n_agreement = sum(1 for r in rows if r["agreement"])
    n_l1_correct = sum(
        1 for r in rows if r["l1_class"] == r["known_class"]
    )
    n_l2_correct = sum(
        1 for r in rows if r["l2_class"] == r["known_class"]
    )
    n_l3_correct = sum(
        1 for r in rows if r["l3_class"] == r["known_class"]
    )
    n_tier_2 = sum(1 for r in rows if r["tier"] == 2)
    n_tier_3 = sum(1 for r in rows if r["tier"] == 3)
    n_tier_4 = sum(1 for r in rows if r["tier"] == 4)
    n_untiered = sum(1 for r in rows if r["tier"] is None)
    n_tier_2_correct = sum(
        1 for r in rows
        if r["tier"] == 2 and r["framework_class"] == r["known_class"]
    )
    n_tier_2_or_3_correct = sum(
        1 for r in rows
        if r["tier"] in (2, 3) and r["framework_class"] == r["known_class"]
    )
    n_target_class_unrecoverable_l3 = sum(
        1 for r in rows if not r["l3_target_class_in_pool"]
    )

    pct_total = 100.0 * n_agreement / n_total if n_total else 0.0
    pct_l1 = 100.0 * n_l1_correct / n_total if n_total else 0.0
    pct_l2 = 100.0 * n_l2_correct / n_total if n_total else 0.0
    pct_l3 = 100.0 * n_l3_correct / n_total if n_total else 0.0
    pct_tier_2_correct = (
        100.0 * n_tier_2_correct / n_tier_2 if n_tier_2 else 0.0
    )

    if pct_total >= 70.0:
        regime = "high"
        regime_word = "validated"
    elif pct_total >= 40.0:
        regime = "moderate"
        regime_word = "partially validated"
    else:
        regime = "low"
        regime_word = "not validated"

    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v5 framework leave-one-out validation against "
      "chic-v2 anchors (chic-v9; mg-18cb)")
    a("")
    a("## Method")
    a("")
    a(f"For each of the {n_anchors} chic-v2 paleographic anchors S "
      "with a known scholarly Linear-B carryover value V, S is removed "
      "from the chic-v2 anchor pool (yielding a reduced "
      f"{n_anchors - 1}-anchor pool), then S is treated as unknown by "
      "the chic-v5 framework and the three non-circular lines of "
      "evidence (L1 distributional plurality, L2 strict-top-1 "
      "anchor distance, L3 substrate-consistency under the v21 "
      "Eteocretan LM) are recomputed against the reduced pool. The "
      "framework's proposed phoneme class is then compared to V's "
      "known class.")
    a("")
    a("L4 (cross-script paleographic) is **deliberately excluded** "
      "from this LOO test: chic-v1's PALEOGRAPHIC_CANDIDATES list "
      "is the source of the chic-v2 anchor pool, so for any anchor "
      "S the L4 line trivially recovers V by construction. Including "
      "L4 would make the test circular and inflate accuracy. With "
      "L4 excluded the framework's tier classification reduces from "
      "the chic-v5 4-line scheme to a 3-line scheme:")
    a("")
    a("- **tier-2** — 3-of-3 unanimity on the top class.")
    a("- **tier-3** — 2-of-3 agreement.")
    a("- **tier-4** — 1-of-3 (single line of evidence).")
    a("- **untiered** — 0 voting lines (no fingerprint signal).")
    a("")
    a("The candidate-value pool for L3 is rebuilt from the reduced "
      f"{n_anchors - 1}-anchor pool's distinct Linear-B carryover "
      "values plus bare vowels a/e/i/o/u, filtered to values whose "
      "first character is in the Eteocretan phoneme inventory "
      "(chic-v5 convention). For 18 of 20 LOO runs this strict-LOO "
      "rebuild removes the held-out value entirely; L3 can therefore "
      "still recover the *class* (if another candidate in the pool "
      "shares it) but cannot recover the *value*. The class is the "
      "framework's per-sign resolution unit, so this is the relevant "
      "LOO target. Where the held-out class has no other "
      "representative in the candidate pool, L3 cannot recover the "
      "class either; this is a structural property of the LOO setup "
      "and is flagged in the per-anchor table.")
    a("")
    a("## Aggregate accuracy")
    a("")
    a(f"Of the {n_total} chic-v2 anchors run blind under L1+L2+L3, "
      f"the framework's proposed class agrees with the known class "
      f"on **{n_agreement}/{n_total} ({pct_total:.1f}%)**. This is "
      f"the headline LOO validation number.")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(f"| n anchors run blind | {n_total} |")
    a(f"| n with framework_class == known_class | {n_agreement} |")
    a(f"| **aggregate LOO accuracy** | **{pct_total:.1f}%** |")
    a(f"| n LOO tier-2 (3-of-3 unanimity) | {n_tier_2} |")
    a(f"| n LOO tier-3 (2-of-3) | {n_tier_3} |")
    a(f"| n LOO tier-4 (1-of-3) | {n_tier_4} |")
    a(f"| n LOO untiered (0 votes) | {n_untiered} |")
    a("")
    a(f"Validation regime: **{regime_word}** — at the chic-v9 brief's "
      "thresholds (>70% high; 40-70% moderate; <40% low), the "
      f"framework's L1+L2+L3 recovery accuracy of {pct_total:.1f}% "
      f"places this LOO test in the **{regime}-agreement** band.")
    a("")
    a("## Per-anchor LOO results")
    a("")
    a("Each row below is one LOO run: the named anchor was removed "
      "from the chic-v2 pool and treated as unknown; the three "
      "lines voted on its class against the reduced 19-anchor pool. "
      "Tier here is the L1+L2+L3-only tier (3-of-3 = tier-2, "
      "2-of-3 = tier-3, etc.). The agreement column is whether the "
      "framework's proposed class matches the known class.")
    a("")
    a("| anchor | freq | known phoneme | known class | framework "
      "class | tier | agreement | L1 | L2 | L3 |")
    a("|---|---:|---|---|---|:---:|:---:|:---:|:---:|:---:|")
    rows_sorted = sorted(rows, key=lambda r: int(r["anchor"].lstrip("#")))
    for r in rows_sorted:
        tier_str = f"tier-{r['tier']}" if r["tier"] is not None else "—"
        agreement = "✓" if r["agreement"] else "✗"
        l1 = r["l1_class"] or "—"
        l2 = r["l2_class"] or "—"
        l3 = r["l3_class"] or "—"
        if not r["l3_target_class_in_pool"]:
            l3 = f"{l3} ⚠"
        framework = r["framework_class"] or "—"
        a(
            f"| `{r['anchor']}` | {r['frequency']} | "
            f"`{r['known_value']}` | {r['known_class']} | "
            f"{framework} | {tier_str} | {agreement} | "
            f"{l1} | {l2} | {l3} |"
        )
    a("")
    a(f"⚠ marker on L3 indicates that the held-out anchor's class "
      "had no other representative in the rebuilt 19-anchor "
      "candidate-value pool, so L3 was structurally unable to "
      f"recover that class. Total such cases: "
      f"{n_target_class_unrecoverable_l3}/{n_total}.")
    a("")
    a("## Per-line accuracy decomposition")
    a("")
    a("How accurately does each line, run in isolation, recover the "
      "known class on the LOO test? This decomposition diagnoses "
      "which lines carry the signal and which are noise.")
    a("")
    a("| line | n_correct/n_total | accuracy |")
    a("|---|:---:|---:|")
    a(f"| L1 (distributional plurality, top-3 nearest anchors) | "
      f"{n_l1_correct}/{n_total} | {pct_l1:.1f}% |")
    a(f"| L2 (strict-top-1 anchor distance) | "
      f"{n_l2_correct}/{n_total} | {pct_l2:.1f}% |")
    a(f"| L3 (substrate-consistency under Eteocretan LM) | "
      f"{n_l3_correct}/{n_total} | {pct_l3:.1f}% |")
    a(f"| **L1+L2+L3 consensus (framework class)** | "
      f"**{n_agreement}/{n_total}** | **{pct_total:.1f}%** |")
    a("")
    a("L3's known systematic class bias under the Eteocretan LM "
      "(chic-v5 finding: L3 favours nasal/glide due to the Eteocretan "
      "vocabulary's onset distribution) carries through to this LOO "
      f"test. Per-line accuracies of L1={pct_l1:.1f}%, L2={pct_l2:.1f}%, "
      f"L3={pct_l3:.1f}% read directly: if L1 and L2 substantially "
      "exceed L3, then the distributional fingerprint machinery is "
      "the load-bearing part of the framework, and L3 functions as "
      "a noisy tiebreaker rather than as independent confirmatory "
      "evidence. The consensus accuracy "
      f"({pct_total:.1f}%) reads against this backdrop.")
    a("")
    a("## Tier-classification accuracy")
    a("")
    a("The chic-v5 framework's tier-2 criterion requires 3-of-3 "
      "unanimity on the top class (with L4 silent for all chic-v5 "
      "unknowns by construction). The LOO equivalent — 3-of-3 "
      "unanimity on L1+L2+L3 — is the same operational criterion. "
      "How accurately does the framework correctly tier-2-classify "
      "anchors as their known class?")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(f"| n LOO tier-2 (3-of-3 unanimous) | {n_tier_2} |")
    a(f"| n LOO tier-2 with framework_class == known_class | "
      f"{n_tier_2_correct} |")
    a(f"| **tier-2 classification accuracy (n_correct / n_tier_2)** | "
      f"**{pct_tier_2_correct:.1f}%** |")
    a(f"| **tier-2-or-3 with framework_class == known_class (≥2 of 3 "
      f"voting lines agreeing on the known class)** | "
      f"**{n_tier_2_or_3_correct}/{n_total} = "
      f"{(100.0 * n_tier_2_or_3_correct / n_total) if n_total else 0.0:.1f}%"
      f"** |")
    a("")
    a("The tier-2 row tells us whether the chic-v5 tier-2 criterion "
      "(3-of-3 unanimity) is reliable when applied to known cases: "
      "of the anchors that the framework would call tier-2 under "
      "L1+L2+L3, what fraction match the scholarly value's class? "
      "The tier-2-or-3 row is the looser test (at least 2 of 3 "
      "lines agreeing on the *known* class), which captures cases "
      "where L1+L2+L3 detect a signal but one line dissents.")
    a("")
    a("## Implication for chic-v5 tier-2 candidates")
    a("")
    if regime == "high":
        a("The aggregate LOO accuracy is **above the 70% threshold**, "
          "placing the chic-v5 framework's L1+L2+L3 recovery in the "
          "**high-agreement band** the chic-v9 brief pre-registered. "
          "The framework's mechanical machinery, when run blind on "
          "anchors with known scholarly values, recovers the known "
          f"class on {n_agreement} of {n_total} anchors "
          f"({pct_total:.1f}%). This validates the chic-v5 "
          "methodology on known cases.")
        a("")
        a("**Implication for the chic-v5 tier-2 candidates (`#001 → "
          "wa`/glide, `#012 → wa`/glide, `#032 → ki`/stop):** these "
          "three new proposals were derived by the same machinery "
          f"that recovers known anchor classes at {pct_total:.1f}% "
          "accuracy. They inherit elevated credibility relative to "
          "tier-3 / tier-4 candidates: the framework that proposed "
          "them is not a black box that produces arbitrary phoneme "
          "classes — it is a mechanism with measured recovery "
          "accuracy on cases where ground truth is known. The "
          "methodology paper's framing should reflect this validated "
          "recovery rate alongside the candidate proposals.")
    elif regime == "moderate":
        a("The aggregate LOO accuracy is **between 40% and 70%**, "
          "placing the framework's L1+L2+L3 recovery in the "
          "**moderate-agreement band** the chic-v9 brief "
          "pre-registered. The framework recovers the known class "
          f"on {n_agreement} of {n_total} anchors "
          f"({pct_total:.1f}%) — better than chance for a "
          "6-class taxonomy (~16.7% chance baseline), but well "
          "short of the >70% high-agreement threshold the brief set "
          "for elevated tier-2-candidate credibility.")
        a("")
        a("**Implication for the chic-v5 tier-2 candidates (`#001 → "
          "wa`/glide, `#012 → wa`/glide, `#032 → ki`/stop):** the "
          "three new proposals carry **moderate evidentiary basis**. "
          "The same framework that proposed them recovers known "
          f"classes at {pct_total:.1f}% accuracy on the LOO test — "
          "well above chance, indicating real signal in the "
          "framework, but not at a level that justifies treating "
          "the candidates as near-certain. They remain **candidate "
          "proposals pending domain-expert review**, with the chic-v9 "
          "LOO accuracy providing one mechanical handle on their "
          "prior credibility.")
    else:
        a("The aggregate LOO accuracy is **below 40%**, placing the "
          "framework's L1+L2+L3 recovery in the **low-agreement band** "
          f"the chic-v9 brief pre-registered. The framework recovers "
          f"the known class on only {n_agreement} of {n_total} "
          f"anchors ({pct_total:.1f}%); for a 6-class taxonomy the "
          "chance baseline is ~16.7%, so this is "
          + ("close to chance"
             if pct_total < 25.0 else "modestly above chance")
          + ", far below what would be expected if the framework "
          "reliably recovered known phoneme values when run blind.")
        a("")
        a("**Implication for the chic-v5 tier-2 candidates (`#001 → "
          "wa`/glide, `#012 → wa`/glide, `#032 → ki`/stop):** these "
          "three new proposals **lose substantial credibility under "
          "this LOO test**. The same framework that proposed them "
          f"recovers known anchor classes at only {pct_total:.1f}% "
          "accuracy when run blind; the methodology paper's framing "
          "must downgrade the three candidates from 'mechanical "
          "proposals deserving specialist review' to 'candidate "
          "proposals contingent on the framework's currently-low "
          "validation accuracy'. The chic-v9 LOO test is what would "
          "have caught a mis-specified framework before publication; "
          "honest reporting on the negative result is the discipline-"
          "protecting outcome the chic-v0..v8 sub-program has "
          "consistently emphasised (cf. chic-v1's missed-update "
          "incident mg-c7e3 backfilled by mg-0ea1).")
    a("")
    a("## Caveats")
    a("")
    a("- **L4 exclusion is non-negotiable methodologically.** "
      "Including L4 would inflate accuracy by construction; the "
      "L1+L2+L3-only LOO is the honest test.")
    a("- **Class-level resolution.** The agreement predicate is "
      "exact phoneme-class identity (vowel / stop / nasal / liquid "
      "/ fricative / glide). The framework's per-sign resolution is "
      "class-level, so this is the correct evaluation granularity. "
      "The LOO test does not adjudicate whether the framework "
      "could correctly recover the **specific phoneme value** "
      "(`ja` vs `je` vs `wa` within glide; `pa` vs `ta` vs `ka` "
      "within stop) — at the LOO test level the framework's "
      "verdict is class-level only.")
    a("- **L3 candidate-pool reduction.** For 18 of 20 LOO runs "
      "the held-out anchor's value is removed from the rebuilt "
      "candidate-value pool, so L3 can no longer score the held-"
      "out value directly. The class is still recoverable if "
      "another candidate in the pool shares it. The "
      f"{n_target_class_unrecoverable_l3} cases where the "
      "held-out class has no other representative in the candidate "
      "pool are flagged with ⚠ in the per-anchor table; for these "
      "anchors L3 cannot recover the class by construction.")
    a("- **Small N (20 anchors).** A 20-anchor LOO test produces "
      "limited statistical resolution. Differences of ±5% between "
      "lines or between this LOO test and a hypothetical larger LOO "
      "test on an expanded anchor pool fall within the binomial "
      "noise floor for this sample size. The headline accuracy "
      "should be read as a point estimate with substantial "
      "uncertainty, not as a precise calibration figure.")
    a("- **Anchor-pool composition bias.** The chic-v2 anchor pool "
      "is itself a curated set (the chic-v1 paleographic-candidate "
      "list); the LOO test measures recovery accuracy on this "
      "specific population, which may differ systematically from "
      "the 76 unknown signs the framework targets. The relevant "
      "comparison is the methodology's recovery on **anchor-shaped** "
      "signs, which is what this test reports.")
    a("")
    a("## Determinism")
    a("")
    a("- No RNG. The L3 control-phoneme selection inherits chic-v5's "
      "sha256-keyed permutation construction (deterministic, "
      "no `random.Random(seed)` draw).")
    a("- Same inputs → byte-identical output. Re-running this script "
      "overwrites the result file with identical content.")
    a("")
    a("## Citations")
    a("")
    a("- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum "
      "Inscriptionum Cretae* (Études Crétoises 31). Paris.")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")
    a("")
    a("## Build provenance")
    a("")
    a(f"- Generated by `scripts/build_chic_v9.py` (mg-18cb).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); "
      "`corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); "
      "`pools/cretan_hieroglyphic_signs.yaml` (chic-v1); "
      "`pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); "
      "`pools/eteocretan.yaml`; "
      "`harness/external_phoneme_models/eteocretan.json` (v21).")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "n_total": n_total,
        "n_agreement": n_agreement,
        "pct_total": pct_total,
        "n_l1_correct": n_l1_correct,
        "n_l2_correct": n_l2_correct,
        "n_l3_correct": n_l3_correct,
        "pct_l1": pct_l1,
        "pct_l2": pct_l2,
        "pct_l3": pct_l3,
        "n_tier_2": n_tier_2,
        "n_tier_3": n_tier_3,
        "n_tier_4": n_tier_4,
        "n_untiered": n_untiered,
        "n_tier_2_correct": n_tier_2_correct,
        "pct_tier_2_correct": pct_tier_2_correct,
        "n_target_class_unrecoverable_l3": n_target_class_unrecoverable_l3,
        "regime": regime,
    }


def run(*, progress: bool = True) -> dict:
    if progress:
        print("chic-v9: loading inputs...", file=sys.stderr)
    full_records = load_chic_records(CHIC_FULL)
    syll_records = load_chic_records(CHIC_SYLL)
    signs_yaml = _load_yaml(SIGNS_YAML)
    anchors_yaml = _load_yaml(ANCHORS_YAML)
    eteo_pool = _load_yaml(ETEO_POOL_YAML)
    lm = ExternalPhonemeModel.load_json(ETEO_LM)

    syllabographic_ids = {
        s["id"] for s in signs_yaml["signs"]
        if s["sign_class"] == "syllabographic"
    }
    anchor_records_full = anchors_yaml["anchors"]

    if progress:
        print(
            f"  syllabographic={len(syllabographic_ids)} "
            f"anchors={len(anchor_records_full)}",
            file=sys.stderr,
        )

    if progress:
        print("chic-v9: computing per-sign distributional fingerprints...",
              file=sys.stderr)
    fingerprints = compute_fingerprints(
        full_records, syllabographic_ids=syllabographic_ids,
    )

    rows: list[dict] = []
    for i, anchor in enumerate(
        sorted(anchor_records_full, key=lambda a: int(a["chic_sign"].lstrip("#")))
    ):
        target_sid = anchor["chic_sign"]
        if progress:
            print(
                f"chic-v9: LOO {i + 1}/{len(anchor_records_full)} "
                f"holding out {target_sid} "
                f"(known={anchor['linear_b_carryover_phonetic']})...",
                file=sys.stderr,
            )
        row = loo_validate_anchor(
            target_sid=target_sid,
            anchor_records_full=anchor_records_full,
            fingerprints=fingerprints,
            syll_records=syll_records,
            eteo_pool=eteo_pool,
            lm=lm,
        )
        rows.append(row)

    if progress:
        print("chic-v9: writing LOO validation markdown...", file=sys.stderr)
    summary = write_loo_validation_md(
        rows, n_anchors=len(anchor_records_full), out_path=OUT_MD,
    )
    if progress:
        print(
            f"chic-v9 done | n={summary['n_total']} "
            f"agreement={summary['pct_total']:.1f}% "
            f"L1={summary['pct_l1']:.1f}% "
            f"L2={summary['pct_l2']:.1f}% "
            f"L3={summary['pct_l3']:.1f}% "
            f"tier-2_correct={summary['n_tier_2_correct']}/"
            f"{summary['n_tier_2']} regime={summary['regime']}",
            file=sys.stderr,
        )
    return summary


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--no-progress", action="store_true")
    args = p.parse_args(argv)
    summary = run(progress=not args.no_progress)
    print(json.dumps({
        "n_total": summary["n_total"],
        "n_agreement": summary["n_agreement"],
        "pct_total": round(summary["pct_total"], 4),
        "pct_l1": round(summary["pct_l1"], 4),
        "pct_l2": round(summary["pct_l2"], 4),
        "pct_l3": round(summary["pct_l3"], 4),
        "n_tier_2": summary["n_tier_2"],
        "n_tier_2_correct": summary["n_tier_2_correct"],
        "regime": summary["regime"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
