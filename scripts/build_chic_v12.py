#!/usr/bin/env python3
"""chic-v12: cross-pool L3 robustness on the 29 chic-v5 tier-3 candidates (mg-2035).

Methodologically symmetric extension of chic-v11 (mg-d69c). chic-v11 ran the
chic-v5 L3 substrate-consistency line under each of the 4 substrate-pool
LMs (aquitanian / etruscan / toponym / eteocretan) on the 3 chic-v5
**tier-2** candidate proposals (`#001 → wa`/glide, `#012 → wa`/glide,
`#032 → ki`/stop) and produced sharp per-candidate differentiation:
`#032` weakly corroborated cross-pool (2 of 4 LMs vote stop, including
the chic-v5 default Eteocretan and Etruscan); `#001` and `#012` actively
undermined as Eteocretan-LM-specific glide artifacts (3 of 4 LMs vote
stop instead).

chic-v12 scales the same robustness check to the **29 chic-v5 tier-3
candidates**: signs where 2 of 4 lines of evidence agree but the third
(typically L3 under Eteocretan) disagrees. The methodological question:
does any tier-3 candidate's L1+L2 consensus get independently
corroborated by a non-Eteocretan substrate LM, in the same evidentiary
shape as `#032`'s cross-pool corroboration? If yes, that candidate has
the same evidence structure as the surviving tier-2 (3 independent
lines plus ≥1 non-Eteocretan substrate-LM corroboration). If no, the
tier-3 cutoff was correctly placed and the framework's cross-pool L3
discrimination claim strengthens to n=32 evidence-graded candidates
rather than n=3.

Method (byte-identical to chic-v11 except for candidate count + outputs)
========================================================================

For each of the 29 tier-3 candidates and each of the 4 substrate pools:

  1. Rebuild candidate-value pool from chic-v2 anchor LB-carryover
     values + bare vowels, filtered to values whose first character is
     in the substrate pool's phoneme inventory (chic-v5 convention).
  2. For each candidate value V in the per-pool pool, score
     (chic-v2 anchors ∪ {sign → V}) against a deterministic class-
     disjoint sha256-keyed control under the substrate pool's LM via
     external_phoneme_perplexity_v0.
  3. Per-class mean paired_diff picks the L3 winning class for that
     (candidate, pool) cell.

The 29 × 4 = 116 cells produce the per-candidate cross-pool L3 table.
For each candidate, the chic-v5 L1+L2 consensus is the reference class;
`corroborated_by` enumerates the non-Eteocretan substrate LMs whose L3
vote matches it (analog to chic-v11 #032's etruscan corroboration);
`reclassification` is one of three bands per the chic-v12 brief:

  - `tier-2-equivalent`: ≥1 non-Eteocretan substrate LM corroborates
    the chic-v5 proposed class. Same evidence structure as #032.
  - `tier-3-corroborated`: only Eteocretan-L3 corroborates the chic-v5
    proposed class (no non-Eteocretan LM does). For the 23 tier-3
    candidates where L1+L2 already agree this is structurally
    impossible (Eteocretan-L3 disagrees by chic-v5 construction —
    that is why they are tier-3 and not tier-2). For the 6 tier-3
    candidates where L1+L2 disagree (#006/#017/#021/#033/#050/#063,
    consensus via L1-or-L2 + L3-eteo agreement) this is the chic-v5
    baseline state by construction.
  - `tier-3-uncorroborated`: no LM's L3 corroborates the chic-v5
    proposed class.

Within-window context inspection
=================================

For any tier-3 candidate that reclassifies to `tier-2-equivalent`
(expected ≤ 5; bail and surface the scale signal if > 5), the build
script runs the chic-v11-style within-window context inspection: pick
2–3 high-frequency CHIC inscriptions where the candidate sign occurs,
render the inscription with the candidate's chic-v5 best value applied
on top of the chic-v2 anchors, and note whether the resulting reading
is consistent with surrounding accountancy / sealing structure
(adjacency to NUM:N, LOG:..., FRAC:... tokens within DIV-bounded
segments). The output of this inspection is appended to
`results/chic_v12_cross_pool_l3.md`.

Inputs (all already committed)
==============================

- corpora/cretan_hieroglyphic/all.jsonl                  (chic-v0)
- corpora/cretan_hieroglyphic/syllabographic.jsonl       (chic-v3)
- pools/cretan_hieroglyphic_anchors.yaml                 (chic-v2)
- pools/aquitanian.yaml, pools/etruscan.yaml,
  pools/toponym.yaml, pools/eteocretan.yaml              (substrate pools)
- harness/external_phoneme_models/basque.json,
  harness/external_phoneme_models/etruscan.json,
  harness/external_phoneme_models/eteocretan.json        (LMs)

Outputs
=======

- results/chic_v12_cross_pool_l3.md
- results/chic_v12_tier3_summary.md

Determinism
===========

- No RNG. The L3 control-phoneme selection inherits chic-v5's
  sha256-keyed permutation; cross-pool dispatch + tier-3 candidate
  enumeration are pure iteration over deterministic input order.
- Same (CHIC corpus, anchor pool, substrate-pool yamls, LM artifacts)
  → byte-identical outputs across re-runs.
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
    aggregate_class_means,
    build_anchor_mapping,
    candidate_value_pool,
    classify_value,
    compute_substrate_consistency,
    load_chic_records,
)

CHIC_FULL = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
CHIC_SYLL = ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"

OUT_CROSS_POOL_MD = ROOT / "results" / "chic_v12_cross_pool_l3.md"
OUT_TIER3_SUMMARY_MD = ROOT / "results" / "chic_v12_tier3_summary.md"

FETCHED_AT = "2026-05-06T00:00:00Z"

# (pool_name, pool_yaml_path, lm_path) ordered as in chic-v11.
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

# 29 chic-v5 tier-3 candidates (mg-7c6d leaderboard, "Tier-3 suggestive
# (2 of 4 agree)" section). Order preserved from the leaderboard.
# Tuple: (sign_id, freq, L1_class, L2_class, L3_eteo_class, chic-v5 proposed_class)
TIER3_CANDIDATES: list[tuple[str, int, str, str, str, str]] = [
    ("#002",  7, "liquid",  "liquid",  "nasal",   "liquid"),
    ("#005", 48, "stop",    "stop",    "nasal",   "stop"),
    ("#006", 13, "glide",   "stop",    "glide",   "glide"),
    ("#007",  8, "vowel",   "vowel",   "nasal",   "vowel"),
    ("#008",  7, "glide",   "glide",   "nasal",   "glide"),
    ("#009", 10, "stop",    "stop",    "nasal",   "stop"),
    ("#011", 24, "liquid",  "liquid",  "glide",   "liquid"),
    ("#017",  6, "stop",    "nasal",   "nasal",   "nasal"),
    ("#020",  9, "vowel",   "vowel",   "glide",   "vowel"),
    ("#021",  3, "glide",   "nasal",   "nasal",   "nasal"),
    ("#027",  3, "glide",   "glide",   "nasal",   "glide"),
    ("#033",  3, "stop",    "glide",   "glide",   "glide"),
    ("#037",  3, "liquid",  "liquid",  "glide",   "liquid"),
    ("#039",  7, "stop",    "stop",    "nasal",   "stop"),
    ("#040", 17, "stop",    "stop",    "liquid",  "stop"),
    ("#043",  6, "liquid",  "liquid",  "glide",   "liquid"),
    ("#045",  4, "stop",    "stop",    "nasal",   "stop"),
    ("#050", 23, "glide",   "stop",    "glide",   "glide"),
    ("#055",  5, "stop",    "stop",    "glide",   "stop"),
    ("#056", 52, "stop",    "stop",    "nasal",   "stop"),
    ("#058",  5, "stop",    "stop",    "glide",   "stop"),
    ("#059",  5, "glide",   "glide",   "nasal",   "glide"),
    ("#060",  8, "stop",    "stop",    "nasal",   "stop"),
    ("#063",  7, "glide",   "liquid",  "glide",   "glide"),
    ("#065",  3, "stop",    "stop",    "nasal",   "stop"),
    ("#066",  3, "stop",    "stop",    "nasal",   "stop"),
    ("#069",  3, "stop",    "stop",    "glide",   "stop"),
    ("#072",  7, "stop",    "stop",    "glide",   "stop"),
    ("#078",  3, "stop",    "stop",    "glide",   "stop"),
]

CLASS_ORDER = ("vowel", "stop", "nasal", "liquid", "fricative", "glide")

# Bail threshold per the chic-v12 brief: more than this many tier-2-
# equivalent reclassifications is itself a scale signal worth surfacing
# rather than a mechanical N candidates to inspect.
TIER_2_EQUIVALENT_INSPECTION_BAIL = 5


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ---------------------------------------------------------------------------
# Cross-pool L3 dispatch (same shape as chic-v11)
# ---------------------------------------------------------------------------


def run_cross_pool_l3(
    *,
    syll_records: list[dict],
    anchor_records: list[dict],
    progress: bool = True,
) -> dict:
    """For each (tier-3 candidate, substrate pool) cell, run L3
    substrate-consistency under that pool's LM.

    Returns a dict keyed by sign_id, with per-pool result rows and a
    cross-pool corroboration summary.
    """
    anchor_mapping = build_anchor_mapping(anchor_records)
    pool_yaml_cache: dict[str, dict] = {}
    pool_value_pool_cache: dict[str, list[str]] = {}
    lm_cache: dict[str, ExternalPhonemeModel] = {}

    for pool_name, pool_path, lm_path in POOL_DISPATCH:
        pool_yaml = _load_yaml(pool_path)
        pool_yaml_cache[pool_name] = pool_yaml
        pool_value_pool_cache[pool_name] = candidate_value_pool(
            anchor_records, pool_yaml,
        )
        if str(lm_path) not in lm_cache:
            lm_cache[str(lm_path)] = ExternalPhonemeModel.load_json(lm_path)

    sign_ids = [c[0] for c in TIER3_CANDIDATES]
    candidate_meta = {
        c[0]: {
            "freq": c[1],
            "L1": c[2],
            "L2": c[3],
            "L3_eteocretan_chic_v5": c[4],
            "chic_v5_proposed_class": c[5],
            "L1_L2_consensus": c[2] if c[2] == c[3] else None,
        }
        for c in TIER3_CANDIDATES
    }

    per_sign: dict[str, dict] = {}
    for sid, freq, L1, L2, L3eteo, proposed in TIER3_CANDIDATES:
        per_sign[sid] = {
            "sign": sid,
            "freq": freq,
            "L1": L1,
            "L2": L2,
            "L3_eteocretan_chic_v5": L3eteo,
            "chic_v5_proposed_class": proposed,
            "L1_L2_consensus": L1 if L1 == L2 else None,
            "per_pool": OrderedDict(),
        }

    for pool_name, pool_path, lm_path in POOL_DISPATCH:
        if progress:
            print(
                f"chic-v12: L3 cross-pool: pool={pool_name} lm={lm_path.name} "
                f"n_candidates={len(sign_ids)}",
                file=sys.stderr,
            )
        value_pool = pool_value_pool_cache[pool_name]
        lm = lm_cache[str(lm_path)]
        substrate = compute_substrate_consistency(
            syll_records=syll_records,
            anchor_mapping=anchor_mapping,
            unknown_ids=sign_ids,
            value_pool=value_pool,
            lm=lm,
        )
        for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES:
            sub_rows = substrate.get(sid, [])
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
            per_sign[sid]["per_pool"][pool_name] = {
                "pool_name": pool_name,
                "lm_path": str(lm_path.relative_to(ROOT)),
                "value_pool_size": len(value_pool),
                "winning_class": winning_class,
                "winning_value": winning_value,
                "winning_paired_diff": winning_diff,
                "per_class_mean_paired_diff": class_means,
            }

    # Per-sign corroboration + reclassification.
    for sid in sign_ids:
        info = per_sign[sid]
        proposed = info["chic_v5_proposed_class"]
        per_pool = info["per_pool"]
        eteo_class = per_pool["eteocretan"]["winning_class"]
        non_eteo_lms = [p for p in per_pool if p != "eteocretan"]
        non_eteo_corroborating = [
            p for p in non_eteo_lms
            if per_pool[p]["winning_class"] == proposed
        ]
        eteo_corroborates = (eteo_class == proposed)
        if non_eteo_corroborating:
            reclassification = "tier-2-equivalent"
        elif eteo_corroborates:
            reclassification = "tier-3-corroborated"
        else:
            reclassification = "tier-3-uncorroborated"
        # Per-pool vote tally + cross-pool top.
        votes = Counter()
        for p in per_pool:
            cls = per_pool[p]["winning_class"]
            if cls:
                votes[cls] += 1
        if votes:
            top_class, top_count = sorted(
                votes.items(), key=lambda kv: (-kv[1], kv[0])
            )[0]
        else:
            top_class, top_count = None, 0
        info["corroborated_by"] = non_eteo_corroborating
        info["eteocretan_corroborates"] = eteo_corroborates
        info["reclassification"] = reclassification
        info["cross_pool_votes"] = dict(votes)
        info["cross_pool_top_class"] = top_class
        info["cross_pool_top_count"] = top_count

    return {
        "per_sign": per_sign,
        "pool_value_pools": {
            pool_name: pool_value_pool_cache[pool_name]
            for pool_name, _pp, _lm in POOL_DISPATCH
        },
    }


# ---------------------------------------------------------------------------
# Reclassification accounting helpers
# ---------------------------------------------------------------------------


def reclassification_counts(summary: dict) -> dict[str, int]:
    counts: Counter = Counter()
    for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES:
        counts[summary["per_sign"][sid]["reclassification"]] += 1
    return {
        "tier-2-equivalent": counts["tier-2-equivalent"],
        "tier-3-corroborated": counts["tier-3-corroborated"],
        "tier-3-uncorroborated": counts["tier-3-uncorroborated"],
    }


def tier2_equivalent_signs(summary: dict) -> list[str]:
    return [
        sid
        for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES
        if summary["per_sign"][sid]["reclassification"] == "tier-2-equivalent"
    ]


# ---------------------------------------------------------------------------
# Within-window context inspection (only for tier-2-equivalent reclassifications)
# ---------------------------------------------------------------------------


def _render_chic_token(
    tok: str, anchor_mapping: dict[str, str], extra_overrides: dict[str, str],
) -> str:
    """Render a CHIC corpus token under (chic-v2 anchors + overrides).

    Mirrors chic-v11's _render_chic_token_with_anchors. Class
    placeholders are NOT applied (chic-v12 inspection is about whether
    the rendered partial reading is interpretable around the anchored +
    candidate-overridden values, not class-level extension).
    """
    if tok == "DIV":
        return "/"
    if tok == "[?]":
        return "[?]"
    if tok.startswith("NUM:") or tok.startswith("LOG:") or tok.startswith("FRAC:") or tok.startswith("IDEO:"):
        return tok
    is_unc = False
    sid = tok
    if tok.startswith("[?:#") and tok.endswith("]"):
        is_unc = True
        sid = tok[3:-1]
    if sid in extra_overrides:
        val = extra_overrides[sid]
        return f"[?:{val}]" if is_unc else val
    if sid in anchor_mapping:
        val = anchor_mapping[sid]
        return f"[?:{val}]" if is_unc else val
    return f"[?:{sid}]" if is_unc else sid


def _sign_in_inscription(rec: dict, sid: str) -> bool:
    target_unc = f"[?:{sid}]"
    for tok in rec["tokens"]:
        if tok == sid or tok == target_unc:
            return True
    return False


def _has_accountancy_neighbor(rec: dict, sid: str) -> bool:
    """Return True if some occurrence of `sid` in `rec` is followed
    (allowing a single intervening DIV) by a NUM/LOG/FRAC/IDEO token —
    the canonical CHIC accountancy positional structure (sign-run =
    entry, followed by a quantity / commodity).
    """
    target_unc = f"[?:{sid}]"
    tokens = rec["tokens"]
    for i, tok in enumerate(tokens):
        if tok != sid and tok != target_unc:
            continue
        for off in (1, 2):
            j = i + off
            if j >= len(tokens):
                break
            nxt = tokens[j]
            if off == 1 and nxt == "DIV":
                continue
            if (
                nxt.startswith("NUM:")
                or nxt.startswith("LOG:")
                or nxt.startswith("FRAC:")
                or nxt.startswith("IDEO:")
            ):
                return True
            break
    return False


def _select_inspection_inscriptions(
    chic_records: list[dict], sid: str, k: int = 3,
) -> list[dict]:
    """Pick up to k high-frequency CHIC inscriptions where `sid` occurs.

    Ranking prefers (a) inscriptions where `sid` has an accountancy
    neighbor (NUM/LOG/FRAC/IDEO immediately or DIV-skipping after it),
    then (b) higher n_signs (longer = more context), then (c)
    higher transcription_confidence (clean preferred over partial),
    then (d) deterministic id sort tiebreak.
    """
    candidates: list[tuple[int, int, int, str, dict]] = []
    confidence_rank = {"clean": 0, "partial": 1, "uncertain": 2, "unknown": 3}
    for rec in chic_records:
        if not _sign_in_inscription(rec, sid):
            continue
        accountancy_priority = 0 if _has_accountancy_neighbor(rec, sid) else 1
        n_signs_rank = -int(rec.get("n_signs") or 0)
        conf_rank = confidence_rank.get(
            rec.get("transcription_confidence") or "unknown", 9
        )
        candidates.append(
            (accountancy_priority, n_signs_rank, conf_rank, rec["id"], rec)
        )
    candidates.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
    return [t[4] for t in candidates[:k]]


def run_context_inspection(
    *,
    chic_records: list[dict],
    anchor_records: list[dict],
    summary: dict,
    progress: bool = True,
) -> dict:
    """For each tier-2-equivalent reclassified candidate, render 2-3
    high-frequency CHIC inscriptions where the candidate occurs and note
    whether the context is consistent with accountancy / sealing
    structure.

    The chic-v5 best L3 value (chic-v5's `substrate_best_value`, recovered
    from the eteocretan dispatch via the cross-pool result) is applied
    as an override. For tier-2-equivalent reclassifications where the
    proposed class is the chic-v5 consensus class, this is the
    natural inspection value (it is the chic-v5 default the tier-2-
    equivalent verdict promotes).
    """
    eligible = tier2_equivalent_signs(summary)
    if not eligible:
        return {
            "n_eligible": 0,
            "bail": False,
            "per_sign_inspection": {},
        }
    if len(eligible) > TIER_2_EQUIVALENT_INSPECTION_BAIL:
        # Per the chic-v12 brief: bail and surface the scale signal
        # rather than do a perfunctory inspection on too many candidates.
        if progress:
            print(
                f"chic-v12: tier-2-equivalent count = {len(eligible)} > "
                f"{TIER_2_EQUIVALENT_INSPECTION_BAIL}; bailing on context "
                f"inspection (scale signal worth surfacing).",
                file=sys.stderr,
            )
        return {
            "n_eligible": len(eligible),
            "bail": True,
            "per_sign_inspection": {},
        }

    anchor_mapping = {
        a["chic_sign"]: a["linear_b_carryover_phonetic"]
        for a in anchor_records
    }

    per_sign_inspection: dict[str, dict] = {}
    for sid in eligible:
        info = summary["per_sign"][sid]
        eteo_cell = info["per_pool"]["eteocretan"]
        # The chic-v5 best L3 value is the eteocretan winning_value of
        # this run (cross-pool eteocretan dispatch is byte-identical to
        # chic-v5's L3). For tier-2-equivalent reclassifications, the
        # chic-v5 winning class IS the proposed class, so this value
        # carries the chic-v5 best-value override on the proposed class.
        override_value = eteo_cell.get("winning_value") or "?"
        overrides = {sid: override_value}
        if progress:
            print(
                f"chic-v12: context inspection: {sid} "
                f"override={override_value} class={info['chic_v5_proposed_class']}",
                file=sys.stderr,
            )
        chosen = _select_inspection_inscriptions(chic_records, sid, k=3)
        renderings = []
        for rec in chosen:
            tokens = rec["tokens"]
            rendered = [
                _render_chic_token(tok, anchor_mapping, overrides) for tok in tokens
            ]
            has_accountancy = _has_accountancy_neighbor(rec, sid)
            renderings.append({
                "id": rec["id"],
                "site": rec.get("site"),
                "support": rec.get("support"),
                "transcription_confidence": rec.get("transcription_confidence"),
                "raw_transliteration": rec.get("raw_transliteration"),
                "n_tokens": len(tokens),
                "n_signs": rec.get("n_signs"),
                "tokens": tokens,
                "rendered_tokens": rendered,
                "has_accountancy_neighbor": has_accountancy,
            })
        per_sign_inspection[sid] = {
            "sign": sid,
            "chic_v5_proposed_class": info["chic_v5_proposed_class"],
            "override_value": override_value,
            "n_inspected": len(renderings),
            "any_accountancy_neighbor": any(
                r["has_accountancy_neighbor"] for r in renderings
            ),
            "renderings": renderings,
        }
    return {
        "n_eligible": len(eligible),
        "bail": False,
        "per_sign_inspection": per_sign_inspection,
    }


# ---------------------------------------------------------------------------
# Markdown writers
# ---------------------------------------------------------------------------


def _format_paired_diff(v: float | None) -> str:
    if v is None:
        return "—"
    return f"{v:+.6f}"


def write_cross_pool_md(
    summary: dict, context: dict, out_path: Path,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v5 tier-3 candidates: cross-pool L3 robustness check "
      "(chic-v12; mg-2035)")
    a("")
    a("## Method")
    a("")
    a(f"Methodologically symmetric extension of chic-v11 (mg-d69c). "
      f"chic-v11 ran the chic-v5 L3 substrate-consistency line under each "
      f"of the 4 substrate-pool LMs on the 3 chic-v5 **tier-2** candidate "
      f"proposals. chic-v12 scales the same robustness check to the **29 "
      f"chic-v5 tier-3 candidates** — signs where exactly 2 of the 3 "
      f"non-silent lines of evidence agree (line 4 cross-script paleographic "
      f"is silent for all 76 chic-v5 unknowns by construction).")
    a("")
    a("For each (tier-3 candidate, substrate pool) cell:")
    a("")
    a("1. Rebuild the candidate-value pool from chic-v2 anchor LB-carryover "
      "values + bare vowels, filtered to values whose first character is "
      "in the substrate pool's phoneme inventory (chic-v5 convention).")
    a("2. For each candidate value V, score (chic-v2 anchors ∪ {sign → V}) "
      "against a deterministic class-disjoint sha256-keyed control under "
      "the substrate pool's LM via `external_phoneme_perplexity_v0`.")
    a("3. Per-class mean paired_diff picks the L3 winning class.")
    a("")
    a("The 29 × 4 = 116 cells produce the per-candidate cross-pool L3 "
      "verdict. For each candidate, the chic-v5 proposed class is the "
      "reference; `corroborated_by` lists non-Eteocretan substrate LMs whose "
      "L3 vote matches the chic-v5 proposed class; `reclassification` is one "
      "of three bands per the chic-v12 brief.")
    a("")
    a("## Acceptance bands (chic-v12 brief)")
    a("")
    a("- **`tier-2-equivalent`** — ≥1 non-Eteocretan substrate LM "
      "corroborates the chic-v5 proposed class. Same evidence structure "
      "as the chic-v11 surviving tier-2 (`#032`): three independent lines "
      "of agreement (chic-v5 L1, L2 — or L1/L2 + Eteocretan L3 for the 6 "
      "L1+L2-disagree tier-3 cases) + ≥ 1 non-Eteocretan substrate LM.")
    a("- **`tier-3-corroborated`** — only Eteocretan-L3 corroborates the "
      "chic-v5 proposed class. For the 23 tier-3 candidates where L1+L2 "
      "agree this is structurally impossible (Eteocretan-L3 disagrees by "
      "chic-v5 construction — that is why they are tier-3 and not tier-2). "
      "For the 6 tier-3 candidates where L1+L2 disagree (#006/#017/#021/"
      "#033/#050/#063, consensus via L1-or-L2 + Eteocretan-L3 agreement) "
      "this is the chic-v5 baseline state by construction.")
    a("- **`tier-3-uncorroborated`** — no LM's L3 corroborates the chic-v5 "
      "proposed class. For the 23 L1+L2-agree tier-3 candidates this means "
      "the cross-pool extension produces no additional substrate-LM support "
      "beyond chic-v5's L1+L2 distributional agreement.")
    a("")
    a("## Pool-LM dispatch table")
    a("")
    a("| substrate pool | LM file | candidate-pool size |")
    a("|---|---|---:|")
    for pool_name, pool_path, lm_path in POOL_DISPATCH:
        vp = summary["pool_value_pools"][pool_name]
        a(f"| {pool_name} | `{lm_path.relative_to(ROOT)}` | {len(vp)} |")
    a("")
    a("Per-pool candidate-value pool composition (each pool's filter "
      "differs because the substrate-pool phoneme inventories differ; "
      "byte-identical to chic-v11 since the chic-v2 anchor pool and the "
      "substrate-pool yamls are unchanged):")
    a("")
    for pool_name, _pp, _lm in POOL_DISPATCH:
        vp = summary["pool_value_pools"][pool_name]
        items = " ".join(f"`{v}`" for v in vp)
        a(f"- **{pool_name}** ({len(vp)} values): {items}")
    a("")

    # ---- Headline reclassification counts ----
    counts = reclassification_counts(summary)
    a("## Headline reclassification counts")
    a("")
    a("| reclassification | n |")
    a("|---|---:|")
    a(f"| tier-2-equivalent | **{counts['tier-2-equivalent']}** |")
    a(f"| tier-3-corroborated | {counts['tier-3-corroborated']} |")
    a(f"| tier-3-uncorroborated | {counts['tier-3-uncorroborated']} |")
    a(f"| **total tier-3** | **{sum(counts.values())}** |")
    a("")

    # ---- Per-candidate × per-LM table ----
    a("## Per-candidate cross-pool L3 verdict")
    a("")
    a("Rows ordered by tier-3 leaderboard order. `L1+L2 consensus` is the "
      "class L1 and L2 agree on (`(disagree)` for the 6 cases where they "
      "differ; the chic-v5 proposed class for those rows comes from L1-or-L2 "
      "+ Eteocretan-L3 agreement, listed in the per-LM Eteocretan column). "
      "`corroborated_by` lists non-Eteocretan LMs whose winning class "
      "matches the chic-v5 proposed class; an empty list means none of the "
      "3 non-Eteocretan substrate LMs corroborates.")
    a("")
    a("| sign | freq | L1 | L2 | L1+L2 consensus | chic-v5 proposed | "
      "Eteocretan-L3 | Aquitanian-L3 | Etruscan-L3 | toponym-L3 | "
      "corroborated_by | reclassification |")
    a("|---|---:|---|---|---|---|---|---|---|---|---|---|")
    for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES:
        info = summary["per_sign"][sid]
        L1_L2 = info["L1_L2_consensus"] or "(disagree)"
        eteo = info["per_pool"]["eteocretan"]["winning_class"] or "—"
        aqui = info["per_pool"]["aquitanian"]["winning_class"] or "—"
        etru = info["per_pool"]["etruscan"]["winning_class"] or "—"
        topo = info["per_pool"]["toponym"]["winning_class"] or "—"
        corroborated = ", ".join(info["corroborated_by"]) or "—"
        a(
            f"| `{sid}` | {info['freq']} | {info['L1']} | {info['L2']} | "
            f"{L1_L2} | {info['chic_v5_proposed_class']} | "
            f"{eteo} | {aqui} | {etru} | {topo} | "
            f"{corroborated} | {info['reclassification']} |"
        )
    a("")

    # ---- Per-candidate per-class mean paired_diff details ----
    a("## Per-candidate per-pool per-class mean paired_diff")
    a("")
    a("Detail-table view of the 116 cells. Each row is one (candidate, "
      "pool) cell; columns are per-class mean paired_diff over the surviving "
      "candidate values. `winning class` is the per-class argmax. `—` for "
      "a class indicates the class is empty in the rebuilt candidate-value "
      "pool for that substrate (e.g. `glide` for aquitanian/etruscan/toponym, "
      "since their candidate pools exclude `wa`/`ja`/`je` by inventory "
      "filter; this is a structural property of those pools, not an L3 "
      "finding).")
    a("")
    for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES:
        info = summary["per_sign"][sid]
        a(f"### `{sid}` "
          f"(chic-v5 proposed: {info['chic_v5_proposed_class']}; "
          f"L1={info['L1']}, L2={info['L2']}, L3-eteo={info['L3_eteocretan_chic_v5']}; "
          f"reclassification: **{info['reclassification']}**)")
        a("")
        a("| pool | LM | winning class | winning value | winning paired_diff | "
          + " | ".join(f"mean({c})" for c in CLASS_ORDER) + " |")
        a("|---|---|---|---|---:|"
          + "|".join("---:" for _ in CLASS_ORDER) + "|")
        for pool_name, _pp, lm_path in POOL_DISPATCH:
            cell = info["per_pool"][pool_name]
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

    # ---- Within-window context inspection (only if any tier-2-equivalent) ----
    a("## Within-window context inspection")
    a("")
    if counts["tier-2-equivalent"] == 0:
        a("**No tier-3 candidate reclassifies to `tier-2-equivalent`.** "
          "The within-window context inspection is moot: there are no "
          "non-Eteocretan-corroborated tier-3 candidates whose contextual "
          "interpretability would be the next test. The cross-pool L3 "
          "robustness check on the 29 tier-3 candidates produces 0 "
          "candidates with the same evidence structure as `#032`.")
        a("")
    elif context["bail"]:
        a(f"**`tier-2-equivalent` count = {context['n_eligible']} > "
          f"{TIER_2_EQUIVALENT_INSPECTION_BAIL}; per the chic-v12 brief, "
          f"the context inspection is bailed and the scale signal is "
          f"surfaced instead.** A reclassification rate this large across "
          f"the tier-3 set is itself a methodologically interesting "
          f"observation: it would imply the cross-pool L3 axis is "
          f"systematically more permissive than the Eteocretan-only L3 "
          f"chic-v5 used, and that the tier-3 cutoff was conservative "
          f"rather than exact. Pre-registered next step: a chic-v13 ticket "
          f"that runs the same context inspection on a stratified sample "
          f"of the {context['n_eligible']} candidates and re-evaluates "
          f"the per-candidate evidence weighting under the cross-pool L3 "
          f"axis. Out of chic-v12's polecat budget.")
        a("")
    else:
        a(f"**{context['n_eligible']} tier-3 candidate(s) reclassify to "
          f"`tier-2-equivalent`** (≤ "
          f"{TIER_2_EQUIVALENT_INSPECTION_BAIL}, within the chic-v12 brief's "
          f"inspection budget). For each, 2-3 high-frequency CHIC "
          f"inscriptions where the candidate occurs are rendered with "
          f"chic-v2 anchors + the candidate's chic-v5 best L3 value applied, "
          f"and the surrounding accountancy / sealing structure is noted.")
        a("")
        for sid, info in context["per_sign_inspection"].items():
            a(f"### `{sid}` (chic-v5 proposed: {info['chic_v5_proposed_class']}; "
              f"override: `{info['override_value']}`)")
            a("")
            if info["n_inspected"] == 0:
                a("No CHIC inscriptions found containing this sign — "
                  "anomalous for a tier-3 candidate (frequency ≥ 3 by "
                  "chic-v5 eligibility). Inspection skipped.")
                a("")
                continue
            a(f"Inspected {info['n_inspected']} inscription(s); "
              f"any with accountancy-formula neighbor (NUM/LOG/FRAC/IDEO "
              f"adjacent to `{sid}` after at most one DIV): "
              f"**{info['any_accountancy_neighbor']}**.")
            a("")
            for rendering in info["renderings"]:
                a(f"#### {rendering['id']}")
                a("")
                a(f"- **site**: {rendering['site']}")
                a(f"- **support**: {rendering['support']}")
                a(f"- **transcription_confidence**: "
                  f"{rendering['transcription_confidence']}")
                a(f"- **n_tokens**: {rendering['n_tokens']} "
                  f"(n_signs={rendering['n_signs']})")
                a(f"- **raw_transliteration**: "
                  f"`{rendering['raw_transliteration']}`")
                a(f"- **accountancy-formula neighbor for `{sid}`**: "
                  f"{rendering['has_accountancy_neighbor']}")
                a("")
                a("**Partial reading (chic-v2 anchors + "
                  f"`{sid} → {info['override_value']}`):**")
                a("")
                a("```")
                a(" ".join(rendering["rendered_tokens"]))
                a("```")
                a("")
            verdict = (
                "consistent with surrounding accountancy / sealing structure "
                "(at least one inspected inscription places "
                f"`{sid}` adjacent to a NUM / LOG / FRAC / IDEO token "
                "after at most one DIV)"
                if info["any_accountancy_neighbor"] else
                "no inspected inscription places `"
                + sid + "` adjacent to a NUM / LOG / FRAC / IDEO token; "
                "the candidate's surrounding context does not exhibit the "
                "canonical accountancy-formula positional structure — "
                "weakens the contextual reading on top of the cross-pool "
                "L3 corroboration"
            )
            a(f"**Inspection verdict for `{sid}`**: {verdict}.")
            a("")

    # ---- Discipline notes ----
    a("## Discipline notes")
    a("")
    a("- **Cross-pool L3 corroboration is a partial defence, not a "
      "positive validation** (chic-v11 framing carried over). chic-v9's "
      "leave-one-out test places the chic-v5 framework's mechanical "
      "recovery on known anchor classes at 20.0% aggregate / 0/3 on the "
      "tier-2 unanimity criterion when run blind. A `tier-2-equivalent` "
      "reclassification under chic-v12 means the candidate has the same "
      "evidence structure as `#032` (three independent lines + ≥ 1 "
      "non-Eteocretan substrate-LM corroboration), but the framework's "
      "framework-level validation accuracy is unchanged. Specialist "
      "review remains the load-bearing next step for any candidate.")
    a("- **The chic-v9 framework-level negative is unaffected.** "
      "chic-v12 is an axis-restricted re-test of L3 only on the tier-3 "
      "set; L1+L2 (distributional fingerprint) are not re-run. Even an "
      "all-3-non-Eteocretan-LMs-corroborate L3 verdict here does not lift "
      "the framework's chic-v9 LOO accuracy from 20.0% / 0/3 tier-2 "
      "correct.")
    a("- **No paleographic L4 work.** Line 4 (cross-script paleographic) "
      "is silent for all 76 unknowns in chic-v5 by construction "
      "(documented limitation; the chic-v1 PALEOGRAPHIC_CANDIDATES list "
      "is precisely the seed for the chic-v2 anchor pool). chic-v12 does "
      "not attempt to fill it; that is out of polecat scope.")
    a("- **`tier-3-corroborated` is a chic-v12 baseline-state label, "
      "not a positive verdict.** For the 6 L1+L2-disagree tier-3 "
      "candidates (#006, #017, #021, #033, #050, #063), the chic-v5 "
      "consensus class is precisely the class L1-or-L2 + Eteocretan-L3 "
      "agree on, so Eteocretan-L3 corroborating the chic-v5 proposed "
      "class is true by construction (just like cross-pool L3 stop on "
      "`#032` corroborating the chic-v5 stop class). The "
      "`tier-3-corroborated` band catches them as the inherited chic-v5 "
      "state and contrasts with `tier-2-equivalent` where additional "
      "non-Eteocretan substrate-LM corroboration is added.")
    a("- **`tier-3-uncorroborated` is the structurally expected verdict "
      "for the L1+L2-agree tier-3 majority** if the cross-pool L3 axis "
      "behaves like Eteocretan-L3 (which by chic-v5 construction "
      "disagrees with L1+L2 for these 23 candidates). A non-zero "
      "`tier-2-equivalent` count would indicate the cross-pool L3 axis "
      "is qualitatively different from Eteocretan-L3 for at least some "
      "tier-3 candidates.")
    a("")

    # ---- Determinism + provenance ----
    a("## Determinism")
    a("")
    a("- No RNG. The L3 control-phoneme selection inherits chic-v5's "
      "sha256-keyed permutation construction.")
    a("- Same (CHIC syllabographic stream, chic-v2 anchor mapping, "
      "substrate-pool yamls, LM artifacts) → byte-identical output.")
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v12.py` (mg-2035).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpora/cretan_hieroglyphic/syllabographic.jsonl` "
      "(chic-v3); `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); "
      "`pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); "
      "`pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; "
      "`harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.")
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

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tier3_summary_md(
    summary: dict, context: dict, out_path: Path,
) -> None:
    counts = reclassification_counts(summary)
    n_total = sum(counts.values())
    n_t2e = counts["tier-2-equivalent"]
    n_t3c = counts["tier-3-corroborated"]
    n_t3u = counts["tier-3-uncorroborated"]
    eligible = tier2_equivalent_signs(summary)
    corroborated_only_eteo = [
        sid for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES
        if summary["per_sign"][sid]["reclassification"] == "tier-3-corroborated"
    ]
    uncorroborated = [
        sid for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES
        if summary["per_sign"][sid]["reclassification"] == "tier-3-uncorroborated"
    ]

    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v5 tier-3 cross-pool L3 reclassification summary "
      "(chic-v12; mg-2035)")
    a("")
    a("## Headline counts")
    a("")
    a("| reclassification | n | meaning |")
    a("|---|---:|---|")
    a(f"| **tier-2-equivalent** | **{n_t2e}** | "
      "≥ 1 non-Eteocretan substrate LM corroborates the chic-v5 proposed "
      "class — same evidence structure as the chic-v11 surviving tier-2 "
      "(`#032`). |")
    a(f"| tier-3-corroborated | {n_t3c} | "
      "Only Eteocretan-L3 corroborates the chic-v5 proposed class. "
      "Captures the 6 chic-v5 L1+L2-disagree candidates whose proposed "
      "class is via Eteocretan-L3 + L1-or-L2 by construction. |")
    a(f"| tier-3-uncorroborated | {n_t3u} | "
      "No LM's L3 corroborates the chic-v5 proposed class. The "
      "structurally-expected verdict for the 23 chic-v5 L1+L2-agree "
      "tier-3 candidates if cross-pool L3 behaves like Eteocretan-L3. |")
    a(f"| **total tier-3** | **{n_total}** | (chic-v5 leaderboard) |")
    a("")

    # ---- Verdict (1-2 paragraphs) ----
    a("## Verdict")
    a("")
    if n_t2e == 0:
        a(
            f"**No tier-3 candidate reclassifies to `tier-2-equivalent`.** "
            f"All {n_total} chic-v5 tier-3 candidates fall into one of two "
            f"bands: `tier-3-corroborated` ({n_t3c} candidates: "
            f"{', '.join('`' + s + '`' for s in corroborated_only_eteo) or '—'}) "
            f"— the inherited chic-v5 baseline state for the L1+L2-disagree "
            f"subset where the proposed class is the L1-or-L2 + Eteocretan-L3 "
            f"agreement; or `tier-3-uncorroborated` ({n_t3u} candidates: "
            f"the L1+L2-agree subset where neither Eteocretan-L3 nor any of "
            f"the 3 non-Eteocretan substrate-LM L3 axes pick the chic-v5 "
            f"proposed class). The cross-pool L3 axis does **not** "
            f"independently support any tier-3 candidate's chic-v5 consensus "
            f"class — exactly the structural-permissiveness pattern chic-v11 "
            f"already documented for `#001` and `#012` (Eteocretan-LM "
            f"specific glide artifacts), now extended across the whole "
            f"tier-3 set."
        )
        a("")
        a(
            f"This **strengthens** the chic-v5 framework's discrimination "
            f"claim: the **tier-3 cutoff was correctly placed**. Of the 32 "
            f"chic-v5 candidates with ≥ 2 lines of agreement (3 tier-2 + "
            f"29 tier-3), only `#032` (chic-v11) carries cross-pool L3 "
            f"corroboration; chic-v12 finds 0 additional tier-3 candidates "
            f"with the same evidence structure. The framework's per-sign "
            f"evidence grading therefore spans **n = 32** evidence-graded "
            f"candidates rather than n = 3 — `#032` (tier-2-equivalent, "
            f"cross-pool corroborated, ku-pa context corroborated; "
            f"chic-v11) plus `#001`, `#012` (tier-2 chic-v5 but "
            f"cross-pool L3 actively undermined; chic-v11) plus the "
            f"{n_t3u} L1+L2-agree tier-3 candidates (cross-pool L3 "
            f"uncorroborated; chic-v12) plus the {n_t3c} L1+L2-disagree "
            f"tier-3 candidates (Eteocretan-L3 corroborates by chic-v5 "
            f"construction; cross-pool L3 does not extend the support; "
            f"chic-v12). The chic-v9 framework-level negative remains "
            f"the dominant constraint; chic-v12's contribution is "
            f"per-candidate evidence-grading granularity."
        )
    else:
        # Build a more conditional verdict.
        a(
            f"**{n_t2e} tier-3 candidate(s) reclassify to "
            f"`tier-2-equivalent`** "
            f"({', '.join('`' + s + '`' for s in eligible)}) — "
            f"each has at least one non-Eteocretan substrate-LM L3 vote "
            f"matching the chic-v5 proposed class, the same evidence "
            f"structure as the chic-v11 surviving tier-2 (`#032`). The "
            f"remaining {n_t3c} candidate(s) reclassify to "
            f"`tier-3-corroborated` (only Eteocretan-L3 corroborates, the "
            f"chic-v5 baseline state for the L1+L2-disagree subset) and "
            f"the remaining {n_t3u} candidate(s) reclassify to "
            f"`tier-3-uncorroborated` (no LM's L3 corroborates)."
        )
        a("")
        if context.get("bail"):
            a(
                f"The reclassification rate is large enough "
                f"({n_t2e} > {TIER_2_EQUIVALENT_INSPECTION_BAIL}) that "
                f"the chic-v12 brief's bail rule applies: the "
                f"within-window context inspection is deferred to a "
                f"follow-up ticket (chic-v13 candidate). The scale signal "
                f"itself — that the cross-pool L3 axis is meaningfully "
                f"more permissive than the Eteocretan-only L3 axis "
                f"chic-v5 used — is the chic-v12 finding."
            )
        else:
            a(
                f"For each `tier-2-equivalent` candidate, "
                f"`results/chic_v12_cross_pool_l3.md` includes a within-"
                f"window context inspection: 2-3 high-frequency CHIC "
                f"inscriptions rendered with the candidate's chic-v5 best "
                f"L3 value applied, and a check for accountancy-formula "
                f"neighbor structure (NUM/LOG/FRAC/IDEO adjacent to the "
                f"candidate sign within DIV-bounded segments)."
            )
        a("")
        a(
            f"The framework's per-sign evidence grading now spans **n = 32** "
            f"evidence-graded candidates (3 tier-2 from chic-v5 + 29 "
            f"tier-3) with **{n_t2e} tier-3 reclassifying to "
            f"`tier-2-equivalent`** under cross-pool L3, "
            f"**{n_t3c} as `tier-3-corroborated`**, and **{n_t3u} as "
            f"`tier-3-uncorroborated`**. The chic-v9 framework-level "
            f"negative is unchanged; chic-v12's contribution is "
            f"per-candidate evidence-grading granularity within the "
            f"chic-v9-validated low-accuracy band."
        )
    a("")

    # ---- Per-candidate one-line summary ----
    a("## Per-candidate one-line summary")
    a("")
    a("| sign | freq | chic-v5 proposed | L1+L2 consensus | "
      "corroborated_by | reclassification |")
    a("|---|---:|---|---|---|---|")
    for sid, _f, _l1, _l2, _l3, _p in TIER3_CANDIDATES:
        info = summary["per_sign"][sid]
        L1_L2 = info["L1_L2_consensus"] or "(disagree)"
        corroborated = ", ".join(info["corroborated_by"]) or "—"
        a(
            f"| `{sid}` | {info['freq']} | {info['chic_v5_proposed_class']} | "
            f"{L1_L2} | {corroborated} | {info['reclassification']} |"
        )
    a("")

    a("## Cross-references")
    a("")
    a("- Full per-candidate × per-LM table (and per-class mean paired_diff "
      "details, plus within-window context inspection for any "
      "`tier-2-equivalent` reclassifications): "
      "`results/chic_v12_cross_pool_l3.md`.")
    a("- chic-v5 leaderboard (the source of the 29 tier-3 candidates): "
      "`results/chic_value_extraction_leaderboard.md` "
      "\"Tier-3 suggestive (2 of 4 agree)\" section.")
    a("- chic-v11 cross-pool L3 robustness check on the 3 chic-v5 tier-2 "
      "candidates (`#032` analog): `results/chic_v11_cross_pool_l3.md`.")
    a("- chic-v9 leave-one-out validation (the framework-level negative "
      "this evidence sits within): `results/chic_v9_loo_validation.md`.")
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v12.py` (mg-2035).")
    a(f"- fetched_at: {FETCHED_AT}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(*, progress: bool = True) -> dict:
    if progress:
        print("chic-v12: loading inputs...", file=sys.stderr)
    chic_records = load_chic_records(CHIC_FULL)
    syll_records = load_chic_records(CHIC_SYLL)
    anchors_yaml = _load_yaml(ANCHORS_YAML)
    anchor_records = anchors_yaml["anchors"]

    cross = run_cross_pool_l3(
        syll_records=syll_records,
        anchor_records=anchor_records,
        progress=progress,
    )
    context = run_context_inspection(
        chic_records=chic_records,
        anchor_records=anchor_records,
        summary=cross,
        progress=progress,
    )
    write_cross_pool_md(cross, context, OUT_CROSS_POOL_MD)
    write_tier3_summary_md(cross, context, OUT_TIER3_SUMMARY_MD)

    if progress:
        print("chic-v12: cross-pool L3 reclassifications:", file=sys.stderr)
        counts = reclassification_counts(cross)
        for k, v in counts.items():
            print(f"  {k}: {v}", file=sys.stderr)
    return {"cross_pool": cross, "context": context}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--no-progress", action="store_true")
    args = p.parse_args(argv)
    out = run(progress=not args.no_progress)
    counts = reclassification_counts(out["cross_pool"])
    summary_payload = {
        "n_total_tier3": sum(counts.values()),
        "n_tier2_equivalent": counts["tier-2-equivalent"],
        "n_tier3_corroborated": counts["tier-3-corroborated"],
        "n_tier3_uncorroborated": counts["tier-3-uncorroborated"],
        "tier2_equivalent_signs": tier2_equivalent_signs(out["cross_pool"]),
        "context_inspection_bailed": out["context"].get("bail", False),
    }
    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
