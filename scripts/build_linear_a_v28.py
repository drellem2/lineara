#!/usr/bin/env python3
"""v28: Linear A side analogous LOO validation of the chic-v5 framework
on LB-carryover anchors (mg-4a7b).

Daniel's reframing (2026-05-06) closes the methodology paper's CHIC/LA
asymmetry on held-out validation. chic-v9 (mg-18cb) showed that
chic-v5's L1+L2+L3 framework recovers known CHIC anchor values at
**20% accuracy** (chance baseline ~16.7% for the 6-class taxonomy) —
squarely in the low-agreement / not-validated band. v28 runs the
symmetric Linear A side analog: apply the same chic-v5 per-sign
value-extraction framework to Linear B carryover anchors on the
Linear A corpus, leave-one-out each anchor, compute recovery
accuracy.

Method
======

For each Linear A AB sign S with a known Linear-B carryover phonetic
value V (parsed from ``pools/linear_b_carryover.yaml``'s 21 well-
attested anchors; AB123 is excluded as conjectural per Younger's
own caveat):

1. Remove S from the 21-anchor LB-carryover pool (yielding a reduced
   20-anchor pool).
2. Treat S as unknown by the chic-v5 framework. Rebuild the
   candidate-value pool from the reduced 20-anchor pool plus bare
   vowels (filtered by the Eteocretan phoneme inventory, just like
   chic-v5).
3. Compute L1 (distributional plurality vote on the top-3 nearest
   anchors), L2 (strict-top-1 anchor distance), and L3 (substrate-
   consistency under the v21 Eteocretan LM) for S, against the
   reduced pool. Per-AB-sign distributional fingerprints
   (`left_neighbor`, `right_neighbor`, `position`, `support`) are
   computed over the full 772-inscription Linear A corpus
   (`corpus/all.jsonl`). The substrate-consistency line uses the
   same corpus tokens directly as the partial-mapping run (tokens
   outside the mapping become `<unk>` boundaries; `DIV` / `LOG:*`
   / `NUM:*` / `FRAC:*` / `[?]` / non-AB syllabograms also break
   the run, matching the chic-v5 substrate-consistency convention).
4. L4 (cross-script paleographic) is **deliberately excluded**: the
   LB-carryover anchor pool's known values are themselves derived
   via paleographic similarity to deciphered Linear B signs, so for
   any anchor S the L4 line trivially recovers V by construction.
   Including L4 would make the LOO test circular and inflate
   accuracy.
5. Apply chic-v5's tier classification using only L1+L2+L3:
   tier-2  3-of-3 unanimity on the top class
   tier-3  2-of-3 agreement
   tier-4  1-of-3 (single line of evidence)
   untiered  0 voting lines
6. Compare the framework's proposed phoneme class to S's known
   scholarly phoneme class. Aggregate per-anchor agreement,
   per-line accuracy, and tier-classification accuracy.

Per the brief, the candidate value pool is rebuilt from the reduced
20-anchor pool. This is the strict LOO setup: the held-out anchor's
value is removed from the candidate-value pool unless another anchor
shares the same value. Where the held-out class itself disappears
from the rebuilt pool (the only `wa`/glide value in the LB-carryover
pool would be such a case if `wa` were present, but the LB-carryover
pool has no `wa`/glide value), L3 cannot recover the class either;
this is a structural property of the LOO setup and is reported
honestly per anchor in the result table.

LM choice for L3
================

The v21 Eteocretan LM is used for L3, in direct symmetry with
chic-v9. The methodologically-symmetric alternative would be to
pick a per-anchor LM keyed on the candidate's substrate pool, but
LB-carryover anchors are not naturally partitioned across the
v10/v18/v21 substrate pools — they are paleographic carryovers
from deciphered Linear B signs, not predictions from any single
substrate. Eteocretan was the strongest pool on Linear A (v21
PASSed at +0.20 gap) and the strongest pool on CHIC, so the LM-
bias profile is symmetric across scripts. Using it here keeps
the LA-side comparison apples-to-apples with chic-v9's LM choice.

Inputs
======

- ``corpus/all.jsonl``                                    (Linear A
                                                            corpus, 772
                                                            inscriptions)
- ``pools/linear_b_carryover.yaml``                       (21 LB-carryover
                                                            anchors via
                                                            citation-string
                                                            extraction;
                                                            see also
                                                            ``scripts/
                                                            build_linear_a_v26.py``
                                                            ::``parse_lb_carryover_anchors``
                                                            for the
                                                            same parser)
- ``pools/eteocretan.yaml``                               (Eteocretan
                                                            substrate-pool
                                                            phoneme inventory
                                                            for the L3
                                                            candidate-value
                                                            pool filter)
- ``harness/external_phoneme_models/eteocretan.json``     (v21 LM
                                                            artifact)

Outputs
=======

- ``results/v28_la_loo_validation.md``  per-anchor LOO result
  table, aggregate accuracy, per-line decomposition, tier-2
  classification accuracy, implications for the chic-v5 framework's
  cross-script credibility.

Determinism
===========

No RNG. Same inputs → byte-identical output across re-runs. The
control-phoneme selection in ``compute_substrate_consistency``
inherits chic-v5's sha256-keyed permutation construction (no
``random.Random(seed)`` draw).

Usage
=====

    python3 scripts/build_linear_a_v28.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from harness.external_phoneme_model import ExternalPhonemeModel  # noqa: E402

from harness.metrics import external_phoneme_perplexity_v0  # noqa: E402

from scripts.build_chic_v5 import (  # noqa: E402
    aggregate_class_means,
    bhattacharyya,
    classify_value,
    control_phoneme_for,
    fingerprint_similarity,
)

CORPUS = ROOT / "corpus" / "all.jsonl"
LB_CARRYOVER_YAML = ROOT / "pools" / "linear_b_carryover.yaml"
ETEO_POOL_YAML = ROOT / "pools" / "eteocretan.yaml"
ETEO_LM = ROOT / "harness" / "external_phoneme_models" / "eteocretan.json"

OUT_MD = ROOT / "results" / "v28_la_loo_validation.md"

FETCHED_AT = "2026-05-06T00:00:00Z"

TOP_K_NEAREST = 3

_FP_DIMS = ("left_neighbor", "right_neighbor", "position", "support")

_AB_TOKEN_RE = re.compile(r"^AB[0-9]+[a-z]*$")
_AB_UNCERTAIN_RE = re.compile(r"^\[\?:AB[0-9]+[a-z]*\]$")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_la_records(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])
    return records


def parse_lb_carryover_anchors(yaml_path: Path) -> dict[str, str]:
    """Parse the LB-carryover AB-sign → phoneme map from the pool's
    citation strings.

    Each surface entry's citation contains "AB##=phon" pairs (the
    canonical Ventris-Chadwick 1956 carryover values); the union is
    the per-AB-sign anchor map. Mirrors the parser in
    ``scripts/build_linear_a_v26.py::parse_lb_carryover_anchors`` so
    the two scripts stay byte-stable on the same yaml input.

    Returns 21 anchored signs (AB01=da, AB02=ro, ..., AB81=ku). The
    AB123 sign mentioned in v4_anchor_taina_HT39's ``sign_to_phoneme``
    map is excluded by the regex because Younger's own citation flags
    AB123 as conjectural and the pool yaml's citation does not embed
    "AB123=na" — the pool maintainers' inclusion criterion. v28
    inherits that inclusion criterion verbatim: well-attested LB-
    carryover values (the citation-embedded subset) only.
    """
    text = yaml_path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for ab, phon in re.findall(r"AB([0-9]+[a-z]*)=([a-z0-9_]+)", text):
        sign = "AB" + ab
        if sign not in out:
            out[sign] = phon
    return dict(sorted(out.items()))


def normalize_la_sign_token(tok: str) -> tuple[str | None, bool]:
    """Map an LA corpus token to ('AB##', is_uncertain) or (None, False).

    Both clean ``AB##`` and uncertain ``[?:AB##]`` forms map to the same
    AB sign id. Non-AB tokens (``DIV``, ``[?]``, ``LOG:*``, ``NUM:*``,
    ``FRAC:*``, A301/A302 non-AB syllabograms) return (None, False);
    these are skipped for fingerprint accumulation but break neighbor
    sequences (BOS / EOS sentinels are inserted at sequence ends).
    """
    if _AB_TOKEN_RE.match(tok):
        return tok, False
    if _AB_UNCERTAIN_RE.match(tok):
        return tok[3:-1], True
    return None, False


# ---------------------------------------------------------------------------
# Fingerprint computation (LA flavour)
# ---------------------------------------------------------------------------


def compute_la_fingerprints(
    records: list[dict],
    *,
    ab_ids: set[str],
) -> dict[str, dict]:
    """Per-AB-sign distributional fingerprints over the full LA corpus.

    Per-sign fingerprint dimensions:
      left_neighbor   Counter over neighboring AB sign IDs (or "BOS"
                      at sequence start). Non-AB tokens are NOT
                      neighbors — DIV / [?] / LOG / NUM / FRAC / A301
                      / A302 break the AB-only sequence; the sequence
                      runs across all AB tokens of a single inscription
                      regardless of intervening DIV.
      right_neighbor  Counter over neighboring AB sign IDs (or "EOS"
                      at sequence end).
      position        Counter over {start, middle, end, single} —
                      per-AB-sign-position bucket within the inscription's
                      AB-only sequence.
      support         Counter over inscription support type (tablet /
                      roundel / nodule / sealing / vase / ...).
      frequency       Total clean+uncertain AB-token occurrences.

    The position bucketing follows chic-v1's third-thirds convention:
    ``idx < n/3`` → start; ``idx >= 2*n/3`` → end; otherwise middle;
    n=1 → single.
    """
    fps: dict[str, dict] = {}
    for sid in ab_ids:
        fps[sid] = {
            "left_neighbor": Counter(),
            "right_neighbor": Counter(),
            "position": Counter(),
            "support": Counter(),
            "frequency": 0,
            "inscription_count": 0,
            "inscription_ids": set(),
        }

    for rec in records:
        tokens = rec["tokens"]
        ab_positions: list[tuple[str, bool]] = []
        for tok in tokens:
            sid, is_unc = normalize_la_sign_token(tok)
            if sid is not None:
                ab_positions.append((sid, is_unc))
        n = len(ab_positions)
        if n == 0:
            continue
        for idx, (sid, _is_unc) in enumerate(ab_positions):
            if sid not in fps:
                continue
            cell = fps[sid]
            cell["frequency"] += 1
            cell["inscription_ids"].add(rec["id"])
            cell["support"][rec.get("support") or "unknown"] += 1
            if n == 1:
                bucket = "single"
            elif idx < n / 3:
                bucket = "start"
            elif idx >= 2 * n / 3:
                bucket = "end"
            else:
                bucket = "middle"
            cell["position"][bucket] += 1
            if idx == 0:
                cell["left_neighbor"]["BOS"] += 1
            else:
                cell["left_neighbor"][ab_positions[idx - 1][0]] += 1
            if idx == n - 1:
                cell["right_neighbor"]["EOS"] += 1
            else:
                cell["right_neighbor"][ab_positions[idx + 1][0]] += 1

    out: dict[str, dict] = {}
    for sid, cell in fps.items():
        out[sid] = {
            "frequency": cell["frequency"],
            "inscription_count": len(cell["inscription_ids"]),
            "left_neighbor": dict(sorted(cell["left_neighbor"].items())),
            "right_neighbor": dict(sorted(cell["right_neighbor"].items())),
            "position": dict(sorted(cell["position"].items())),
            "support": dict(sorted(cell["support"].items())),
        }
    return out


# ---------------------------------------------------------------------------
# LOO machinery
# ---------------------------------------------------------------------------


def _ab_sort_key(sid: str) -> tuple[int, str]:
    m = re.match(r"^AB([0-9]+)([a-z]*)$", sid)
    if not m:
        return (10**9, sid)
    return (int(m.group(1)), m.group(2))


def compute_la_anchor_distance_map(
    fingerprints: dict[str, dict],
    *,
    anchor_map: dict[str, str],
    target_id: str,
    top_k: int = TOP_K_NEAREST,
) -> list[dict]:
    """Top-K nearest anchors to target_id by mean Bhattacharyya
    similarity over the four fingerprint dimensions. Returns rows
    sorted by similarity desc, anchor-id asc."""
    if target_id not in fingerprints:
        return []
    ranked: list[tuple[float, str, dict[str, float]]] = []
    for anchor_id, value in anchor_map.items():
        if anchor_id == target_id:
            continue
        if anchor_id not in fingerprints:
            continue
        sim, per_dim = fingerprint_similarity(
            fingerprints[target_id], fingerprints[anchor_id], dimensions=_FP_DIMS,
        )
        ranked.append((sim, anchor_id, per_dim))
    ranked.sort(key=lambda t: (-t[0], _ab_sort_key(t[1])))
    out: list[dict] = []
    for sim, anchor_id, per_dim in ranked[:top_k]:
        value = anchor_map[anchor_id]
        out.append({
            "anchor_id": anchor_id,
            "anchor_value": value,
            "anchor_class": classify_value(value),
            "similarity": round(sim, 6),
            "per_dim": {k: round(v, 6) for k, v in per_dim.items()},
        })
    return out


def build_la_anchor_mapping(anchor_map: dict[str, str]) -> dict[str, str]:
    """Build the corpus token → phoneme mapping for an anchor-only
    partial render. Both the clean ``AB##`` and uncertain ``[?:AB##]``
    forms map to the same value, mirroring the chic-v5 convention.
    """
    out: dict[str, str] = {}
    for sid, val in anchor_map.items():
        out[sid] = val
        out[f"[?:{sid}]"] = val
    return out


def la_candidate_value_pool(
    anchor_map: dict[str, str],
    eteocretan_pool: dict,
    *,
    extra_vowels: tuple[str, ...] = ("a", "e", "i", "o", "u"),
) -> list[str]:
    """Candidate phoneme values to try for each held-out unknown sign.

    Built as the union of:
      - every distinct LB-carryover phoneme value in the reduced
        anchor pool;
      - bare-vowel phonemes a/e/i/o/u (so the vowel class is fully
        covered even when no anchor in the reduced pool is bare-V).

    The Eteocretan pool is consulted only as a sanity check that
    every candidate value's first character is in the pool's
    phoneme inventory (so the LM has bigram support for it). This
    is the chic-v5 candidate-pool convention applied verbatim.
    """
    pool_values: set[str] = set()
    for v in anchor_map.values():
        pool_values.add(v)
    for v in extra_vowels:
        pool_values.add(v)

    eteo_phonemes: set[str] = set()
    for entry in eteocretan_pool["entries"]:
        for ph in entry["phonemes"]:
            eteo_phonemes.add(ph)

    out: list[str] = []
    for v in sorted(pool_values):
        if v[0] in eteo_phonemes or v[0] in extra_vowels:
            out.append(v)
    return out


def compute_la_substrate_consistency(
    *,
    la_records: list[dict],
    anchor_mapping: dict[str, str],
    target_sid: str,
    value_pool: list[str],
    lm: ExternalPhonemeModel,
) -> list[dict]:
    """Score every (target_sid → candidate) pair under the Eteocretan
    LM and return per-candidate paired_diff rows.

    Mirrors ``scripts.build_chic_v5.compute_substrate_consistency`` for
    a single target sign, but uses the LA corpus's own stream-build
    convention (records sorted by id; INS_BOUNDARY between records;
    tokens emitted verbatim — DIV / LOG:* / NUM:* / FRAC:* / [?] /
    A301-style non-AB syllabograms break runs as ``<unk>`` in the
    perplexity metric). The chic-v5 function's CHIC-specific sign-id
    sort key (``int(s.lstrip("#"))``) is incompatible with LA's AB
    sign IDs; this function avoids that sort by accepting a single
    target sign per call.

    The control-phoneme selection is delegated to chic-v5's
    ``control_phoneme_for`` (sha256-keyed, deterministic).
    """
    stream: list[str] = []
    la_sorted = sorted(la_records, key=lambda r: r["id"])
    for rec in la_sorted:
        if int(rec.get("n_signs", 0)) <= 0:
            continue
        if stream:
            stream.append("INS_BOUNDARY")
        stream.extend(rec["tokens"])

    per_candidate: list[dict] = []
    for cand in value_pool:
        cand_class = classify_value(cand)
        if cand_class == "unknown":
            continue
        ctrl = control_phoneme_for(target_sid, cand, cand_class, value_pool)
        ctrl_class = classify_value(ctrl)

        sub_map = dict(anchor_mapping)
        sub_map[target_sid] = cand
        sub_map[f"[?:{target_sid}]"] = cand

        ctrl_map = dict(anchor_mapping)
        ctrl_map[target_sid] = ctrl
        ctrl_map[f"[?:{target_sid}]"] = ctrl

        sub_res = external_phoneme_perplexity_v0(
            stream=stream, mapping=sub_map, language_model=lm,
        )
        ctrl_res = external_phoneme_perplexity_v0(
            stream=stream, mapping=ctrl_map, language_model=lm,
        )
        per_candidate.append({
            "candidate": cand,
            "candidate_class": cand_class,
            "control": ctrl,
            "control_class": ctrl_class,
            "substrate_score": float(sub_res.score),
            "control_score": float(ctrl_res.score),
            "paired_diff": float(sub_res.score - ctrl_res.score),
            "n_chars_substrate": int(sub_res.n_chars_scored),
            "n_chars_control": int(ctrl_res.n_chars_scored),
        })
    per_candidate.sort(key=lambda c: (-c["paired_diff"], c["candidate"]))
    return per_candidate


def _plurality_class(top_anchors: list[dict]) -> str | None:
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
    construction). 3-of-3 → tier-2; 2-of-3 → tier-3; 1-of-3 → tier-4;
    0 → untiered. Tiebreak alphabetically (chic-v9 convention)."""
    votes: Counter = Counter()
    for cls in (l1_class, l2_class, l3_class):
        if cls and cls != "unknown":
            votes[cls] += 1
    if not votes:
        return None, None
    top_class, top_count = sorted(
        votes.items(), key=lambda kv: (-kv[1], kv[0]),
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
    full_anchor_map: dict[str, str],
    fingerprints: dict[str, dict],
    la_records: list[dict],
    eteo_pool: dict,
    lm: ExternalPhonemeModel,
) -> dict:
    """L1+L2+L3 LOO test for a single LB-carryover anchor sign."""
    known_value = full_anchor_map[target_sid]
    known_class = classify_value(known_value)

    reduced_anchor_map = {
        s: v for s, v in full_anchor_map.items() if s != target_sid
    }

    nearest = compute_la_anchor_distance_map(
        fingerprints,
        anchor_map=reduced_anchor_map,
        target_id=target_sid,
        top_k=TOP_K_NEAREST,
    )
    if nearest:
        l1_class = _plurality_class(nearest)
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

    reduced_mapping = build_la_anchor_mapping(reduced_anchor_map)
    reduced_value_pool = la_candidate_value_pool(reduced_anchor_map, eteo_pool)
    sub_rows = compute_la_substrate_consistency(
        la_records=la_records,
        anchor_mapping=reduced_mapping,
        target_sid=target_sid,
        value_pool=reduced_value_pool,
        lm=lm,
    )
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

    target_freq = fingerprints[target_sid]["frequency"] if target_sid in fingerprints else 0

    return {
        "anchor": target_sid,
        "known_value": known_value,
        "known_class": known_class,
        "frequency": target_freq,
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


# ---------------------------------------------------------------------------
# Markdown writer
# ---------------------------------------------------------------------------


def write_loo_validation_md(
    rows: list[dict],
    *,
    n_anchors: int,
    chic_v9_summary: dict,
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

    chic_pct_total = chic_v9_summary["pct_total"]
    chic_pct_l1 = chic_v9_summary["pct_l1"]
    chic_pct_l2 = chic_v9_summary["pct_l2"]
    chic_pct_l3 = chic_v9_summary["pct_l3"]
    chic_n_tier_2 = chic_v9_summary["n_tier_2"]
    chic_n_tier_2_correct = chic_v9_summary["n_tier_2_correct"]
    chic_pct_tier_2 = (
        100.0 * chic_n_tier_2_correct / chic_n_tier_2 if chic_n_tier_2 else 0.0
    )

    delta_total = pct_total - chic_pct_total
    delta_l1 = pct_l1 - chic_pct_l1
    delta_l2 = pct_l2 - chic_pct_l2
    delta_l3 = pct_l3 - chic_pct_l3

    lines: list[str] = []
    a = lines.append
    a("# Linear A side leave-one-out validation of the chic-v5 framework "
      "on LB-carryover anchors (v28; mg-4a7b)")
    a("")
    a("## Method")
    a("")
    a(f"For each of the {n_anchors} Linear A LB-carryover anchors S "
      "(parsed from `pools/linear_b_carryover.yaml`'s 21 well-attested "
      "AB-sign → phoneme citations; AB123 excluded as conjectural per "
      "Younger), S is removed from the LB-carryover pool (yielding a "
      f"reduced {n_anchors - 1}-anchor pool), then S is treated as "
      "unknown by the chic-v5 framework and the three non-circular "
      "lines of evidence are recomputed against the reduced pool. The "
      "framework's proposed phoneme class is then compared to V's "
      "known class.")
    a("")
    a("- **L1 distributional plurality** — top-3 nearest anchors by "
      "mean Bhattacharyya similarity over four per-AB-sign fingerprint "
      "dimensions (`left_neighbor`, `right_neighbor`, `position`, "
      "`support`); plurality vote on phoneme class. Fingerprints are "
      "computed over the full 772-inscription Linear A corpus.")
    a("- **L2 strict-top-1 anchor distance** — single nearest anchor's "
      "phoneme class.")
    a("- **L3 substrate-consistency under the v21 Eteocretan LM** — "
      "for each candidate value V in the rebuilt candidate-value "
      "pool, score (LB-carryover anchors ∪ {S → V}) under the v21 "
      "Eteocretan LM via `external_phoneme_perplexity_v0`; per-class "
      "mean paired_diff picks the winning class. Same machinery as "
      "chic-v5/chic-v9; the LM choice is symmetric with chic-v9.")
    a("- **L4 cross-script paleographic** is **deliberately excluded**: "
      "the LB-carryover anchor pool's known values are themselves "
      "derived via paleographic similarity to deciphered Linear B "
      "signs (Ventris-Chadwick 1956), so for any anchor S the L4 "
      "line trivially recovers V by construction. Including L4 would "
      "make the LOO test circular and inflate accuracy. With L4 "
      "excluded the framework's tier classification reduces from the "
      "chic-v5 4-line scheme to a 3-line scheme:")
    a("")
    a("- **tier-2** — 3-of-3 unanimity on the top class.")
    a("- **tier-3** — 2-of-3 agreement.")
    a("- **tier-4** — 1-of-3 (single line of evidence).")
    a("- **untiered** — 0 voting lines (no fingerprint signal).")
    a("")
    a("### LM choice for L3")
    a("")
    a("The v21 Eteocretan LM is used, in **direct symmetry with "
      "chic-v9** (mg-18cb). The methodologically-symmetric alternative "
      "would be to pick a per-anchor LM keyed on the candidate's "
      "substrate pool, but LB-carryover anchors are not naturally "
      "partitioned across the v10/v18/v21 substrate pools — they are "
      "paleographic carryovers from deciphered Linear B signs, not "
      "predictions from any single substrate. Eteocretan was the "
      "strongest pool on Linear A (v21 PASSed at +0.20 gap) and the "
      "strongest pool on CHIC, so the LM-bias profile is symmetric "
      "across scripts. Using it here keeps the LA-side comparison "
      "apples-to-apples with chic-v9.")
    a("")
    a("### Inclusion criterion for the anchor pool")
    a("")
    a("The anchor pool is the set of AB signs whose Linear-B carryover "
      "phonetic value is embedded as an `AB##=phon` pair in the "
      "`pools/linear_b_carryover.yaml` source citations. This is the "
      "**well-attested-citation** subset: the citation strings on "
      "every entry follow Younger 2020 (online edition) plus Ventris-"
      "Chadwick 1956 carryover values. AB123 (proposed `na` in the "
      "v4_anchor_taina_HT39 hypothesis) is **excluded** because Younger's "
      "own citation flags AB123 as conjectural and the pool yaml's "
      "citation does not embed it as a stable `AB123=na` entry. v28 "
      f"inherits that inclusion criterion verbatim, yielding {n_anchors} "
      "well-attested anchors. (For comparison: chic-v9 ran 20 anchors "
      "from chic-v2's paleographic-candidate pool; the LA-side anchor "
      f"pool size of {n_anchors} is comparable.)")
    a("")
    a("The candidate-value pool for L3 is rebuilt from the reduced "
      f"{n_anchors - 1}-anchor pool's distinct LB-carryover values "
      "plus bare vowels a/e/i/o/u, filtered to values whose first "
      "character is in the Eteocretan phoneme inventory (chic-v5 "
      "convention). Where the rebuild removes the held-out value "
      "entirely (typical when the held-out value has no other "
      "anchor sharing it), L3 can still recover the *class* if "
      "another candidate in the pool shares it. Where the held-out "
      "class itself has no other representative in the rebuilt pool, "
      "L3 cannot recover the class by construction; this is flagged "
      "with ⚠ in the per-anchor table.")
    a("")
    a("## Aggregate accuracy")
    a("")
    a(f"Of the {n_total} LB-carryover anchors run blind under L1+L2+L3, "
      f"the framework's proposed class agrees with the known class on "
      f"**{n_agreement}/{n_total} ({pct_total:.1f}%)**. This is the "
      f"headline LA-side LOO validation number.")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(f"| n anchors run blind | {n_total} |")
    a(f"| n with framework_class == known_class | {n_agreement} |")
    a(f"| **aggregate LA-side LOO accuracy** | **{pct_total:.1f}%** |")
    a(f"| chance baseline (6-class taxonomy) | ~16.7% |")
    a(f"| chic-v9 (CHIC-side) aggregate LOO accuracy | "
      f"{chic_pct_total:.1f}% |")
    a(f"| **delta (LA − CHIC)** | **{delta_total:+.1f}%** |")
    a(f"| n LOO tier-2 (3-of-3 unanimity) | {n_tier_2} |")
    a(f"| n LOO tier-3 (2-of-3) | {n_tier_3} |")
    a(f"| n LOO tier-4 (1-of-3) | {n_tier_4} |")
    a(f"| n LOO untiered (0 votes) | {n_untiered} |")
    a("")
    a(f"Validation regime: **{regime_word}** — at the chic-v9 brief's "
      "thresholds (>70% high; 40-70% moderate; <40% low), the "
      f"framework's L1+L2+L3 recovery accuracy of {pct_total:.1f}% on "
      f"the LA side places this LOO test in the **{regime}-agreement** "
      f"band.")
    a("")
    a("## Per-anchor LOO results")
    a("")
    a("Each row below is one LOO run: the named anchor was removed "
      "from the LB-carryover pool and treated as unknown; the three "
      "lines voted on its class against the reduced "
      f"{n_anchors - 1}-anchor pool. Tier here is the L1+L2+L3-only "
      "tier (3-of-3 = tier-2, 2-of-3 = tier-3, etc.). The agreement "
      "column is whether the framework's proposed class matches the "
      "known class.")
    a("")
    a("| anchor | freq | known phoneme | known class | framework "
      "class | tier | agreement | L1 | L2 | L3 |")
    a("|---|---:|---|---|---|:---:|:---:|:---:|:---:|:---:|")
    rows_sorted = sorted(rows, key=lambda r: _ab_sort_key(r["anchor"]))
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
    a(f"⚠ marker on L3 indicates that the held-out anchor's class had "
      "no other representative in the rebuilt candidate-value pool, so "
      "L3 was structurally unable to recover that class. Total such "
      f"cases: {n_target_class_unrecoverable_l3}/{n_total}.")
    a("")
    a("## Per-line accuracy decomposition")
    a("")
    a("How accurately does each line, run in isolation, recover the "
      "known class on the LOO test? This decomposition diagnoses "
      "which lines carry the signal and which are noise — and lets "
      "us compare per-line behaviour to chic-v9's CHIC-side LOO.")
    a("")
    a("| line | LA-side n_correct/n_total | LA-side accuracy | "
      "chic-v9 (CHIC-side) accuracy | delta (LA − CHIC) |")
    a("|---|:---:|---:|---:|---:|")
    a(f"| L1 (distributional plurality, top-3 nearest anchors) | "
      f"{n_l1_correct}/{n_total} | {pct_l1:.1f}% | "
      f"{chic_pct_l1:.1f}% | {delta_l1:+.1f}% |")
    a(f"| L2 (strict-top-1 anchor distance) | "
      f"{n_l2_correct}/{n_total} | {pct_l2:.1f}% | "
      f"{chic_pct_l2:.1f}% | {delta_l2:+.1f}% |")
    a(f"| L3 (substrate-consistency under Eteocretan LM) | "
      f"{n_l3_correct}/{n_total} | {pct_l3:.1f}% | "
      f"{chic_pct_l3:.1f}% | {delta_l3:+.1f}% |")
    a(f"| **L1+L2+L3 consensus (framework class)** | "
      f"**{n_agreement}/{n_total}** | **{pct_total:.1f}%** | "
      f"**{chic_pct_total:.1f}%** | **{delta_total:+.1f}%** |")
    a("")
    a("Per-line cross-script comparison reads directly: positive "
      "deltas mean the line recovers more accurately on LA than on "
      "CHIC (i.e. LA's larger and more distributionally-rich corpus "
      "lets the line carry more signal); negative deltas mean the "
      "line does worse on LA. The bottom row's delta is the headline "
      "LA-vs-CHIC framework-validation comparison; if it is positive "
      "and large, the chic-v5 framework is structurally portable but "
      "CHIC-corpus-limited; if it is small or negative, the at-chance "
      "behaviour observed on chic-v9 is structural to the framework "
      "rather than CHIC-specific.")
    a("")
    a("## Tier-classification accuracy")
    a("")
    a("The chic-v5 framework's tier-2 criterion requires 3-of-3 "
      "unanimity on the top class (with L4 silent for all chic-v5 "
      "unknowns by construction). The LOO equivalent — 3-of-3 "
      "unanimity on L1+L2+L3 — is the same operational criterion. "
      "How accurately does the framework correctly tier-2-classify "
      "anchors as their known class, on the LA side?")
    a("")
    a("| metric | value |")
    a("|---|---:|")
    a(f"| n LOO tier-2 (3-of-3 unanimous) | {n_tier_2} |")
    a(f"| n LOO tier-2 with framework_class == known_class | "
      f"{n_tier_2_correct} |")
    a(f"| **tier-2 classification accuracy (n_correct / n_tier_2)** | "
      f"**{pct_tier_2_correct:.1f}%** |")
    a(f"| chic-v9 tier-2 classification accuracy | "
      f"{chic_n_tier_2_correct}/{chic_n_tier_2} = "
      f"{chic_pct_tier_2:.1f}% |")
    a(f"| **tier-2-or-3 with framework_class == known_class (≥2 of 3 "
      f"voting lines agreeing on the known class)** | "
      f"**{n_tier_2_or_3_correct}/{n_total} = "
      f"{(100.0 * n_tier_2_or_3_correct / n_total) if n_total else 0.0:.1f}%"
      f"** |")
    a("")
    a("The tier-2 row tells us whether the chic-v5 tier-2 criterion "
      "(3-of-3 unanimity) is reliable when applied to known cases on "
      "the LA side. The tier-2-or-3 row is the looser test (at least "
      "2 of 3 lines agreeing on the *known* class), which captures "
      "cases where L1+L2+L3 detect a partial signal but one line "
      "dissents.")
    a("")
    a("## Implication for the chic-v5 / v22 / v26 framework's per-sign credibility")
    a("")
    if regime == "high":
        a(f"The LA-side aggregate LOO accuracy of {pct_total:.1f}% is "
          "**above the 70% threshold**, placing the framework's "
          "L1+L2+L3 recovery in the **high-agreement / validated** "
          f"band on the Linear A side. Combined with chic-v9's "
          f"{chic_pct_total:.1f}% on the CHIC side, the methodology "
          "paper's reading becomes: **the framework validates on LA "
          "but not on CHIC**. The 20% chic-v9 result reflects a "
          "**CHIC-specific limitation** — the smaller corpus size, "
          "the sparser syllabographic distributional fingerprints "
          "(CHIC is heavily sealstone-dominated and short), the "
          "smaller chic-v2 anchor pool — rather than a structural "
          "limitation of the framework. The chic-v5 tier-2 candidates "
          "remain downgraded per chic-v9 / chic-v10's CHIC-specific "
          "verdict, but the framework itself recovers known LB-"
          "carryover values on the LA side at validating accuracy. "
          "**The methodology paper's framing closes**: framework "
          "validates on LA, framework-output-on-corpus-too-small-to-"
          "validate on CHIC.")
    elif regime == "moderate":
        a(f"The LA-side aggregate LOO accuracy of {pct_total:.1f}% is "
          "**between 40% and 70%**, placing the framework's L1+L2+L3 "
          "recovery in the **moderate-agreement / partially-"
          "validated** band on the Linear A side. Combined with "
          f"chic-v9's {chic_pct_total:.1f}% on the CHIC side, the "
          "methodology paper's reading becomes: **the framework "
          "partially validates on LA, fails on CHIC**. The chic-v5 "
          "framework detects substrate-LM-phonotactic kinship at the "
          "population level (cf. v10/v18/v21 PASSes) but per-sign "
          "value extraction is at moderate accuracy on LA's larger / "
          "richer corpus and at chance on CHIC's smaller / sparser "
          "one. The chic-v5 tier-2 candidates' downgrade per chic-v9 "
          "/ chic-v10 stands; the methodology paper hedges the "
          "framework's per-sign reliability accordingly across both "
          "scripts.")
    else:
        a(f"The LA-side aggregate LOO accuracy of {pct_total:.1f}% is "
          "**below 40%**, placing the framework's L1+L2+L3 recovery "
          "in the **low-agreement / not-validated** band on the "
          f"Linear A side. The chance baseline for a 6-class taxonomy "
          "is ~16.7%, so this is "
          + ("close to chance" if pct_total < 25.0 else "modestly above chance")
          + ", far below what would be expected if the framework "
          "reliably recovered known phoneme values when run blind.")
        a("")
        a(f"Combined with chic-v9's {chic_pct_total:.1f}% on the "
          "CHIC side, the methodology paper's reading becomes: **the "
          "at-chance behaviour is structural to the chic-v5 framework, "
          "not CHIC-specific**. The framework detects substrate-LM-"
          "phonotactic kinship at the **population level** (the v10/"
          "v18/v21 PASSes on Linear A; the chic-v3 right-tail bayesian "
          "gate PASS for Eteocretan against CHIC at p=7.33e-04) but "
          "**per-sign value extraction is below the noise floor on "
          "both scripts** under our held-out validation. The "
          "implication for the broader chic-v5 / v22 / v26 / leader-"
          "board top-K framework is a **substantial downgrade across "
          "both scripts**:")
        a("")
        a("- **The chic-v5 tier-2 candidates' credibility downgrade "
          "(per chic-v9 / chic-v10) extends to the v22 + v26 leaderboard "
          "top-K mechanical-verification results' per-sign-value "
          "claims.** The leaderboard top-K substrates were detected by "
          "the same population-level kinship machinery whose per-sign "
          "extraction is at chance; v26's tier-1 → tier-2 mechanical "
          "lift on Linear A and chic-v6's analogous +3-inscription / "
          "+20-hit lift on CHIC are **mechanical findings about the "
          "framework's sign-coverage ladder**, not independent "
          "evidence for the per-sign phoneme-class assignments.")
        a("- **The population-level cross-script claim survives "
          "intact.** chic-v3 / chic-v4's right-tail bayesian gate "
          "PASS and Spearman ρ=+1.000 cross-script ranking are "
          "population-level signals that do not depend on the "
          "per-sign machinery; the v28 LA-side null does not move "
          "those numbers.")
        a("- **v28 closes the methodology paper's CHIC/LA asymmetry "
          "on held-out validation.** v26 (mg-c202) closed the "
          "asymmetry on mechanical-verification (LA top-K vs chic-v6 "
          "tier-2 lift) by adding a §4.6 paragraph parallel to "
          "§4.7's chic-v6 paragraph; v28 closes the analogous "
          "asymmetry on per-sign-recovery validation by adding a "
          "§4.6 paragraph parallel to §4.7's chic-v9 paragraph.")
    a("")
    a("## Caveats")
    a("")
    a("- **L4 exclusion is non-negotiable methodologically.** The "
      "LB-carryover anchor pool's known values are themselves derived "
      "via paleographic similarity to deciphered Linear B signs; "
      "including L4 would inflate accuracy by construction. The "
      "L1+L2+L3-only LOO is the honest test.")
    a("- **Class-level resolution.** The agreement predicate is exact "
      "phoneme-class identity (vowel / stop / nasal / liquid / "
      "fricative / glide). The framework's per-sign resolution is "
      "class-level, so this is the correct evaluation granularity. "
      "The LOO test does not adjudicate whether the framework could "
      "correctly recover the **specific phoneme value** within the "
      "class.")
    a(f"- **L3 candidate-pool reduction.** Where the held-out value "
      "is the only representative of its class in the rebuilt pool, "
      "L3 cannot recover the class by construction. The "
      f"{n_target_class_unrecoverable_l3} cases where the held-out "
      "class has no other representative in the candidate pool are "
      "flagged with ⚠ in the per-anchor table; for these anchors L3 "
      "cannot recover the class by construction.")
    a(f"- **N = {n_total} anchors.** The sample is comparable in "
      "size to chic-v9's 20 CHIC anchors; ±5% differences fall within "
      "the binomial noise floor. The headline accuracy should be read "
      "as a point estimate with substantial uncertainty.")
    a("- **Anchor-pool composition bias.** The LB-carryover anchors "
      "are paleographically-derived AB signs, not a random sample of "
      "Linear A syllabograms; the LOO test measures recovery accuracy "
      "on this specific population, which may differ systematically "
      "from the broader 56 non-anchored AB signs the framework would "
      "be applied to in a hypothetical chic-v5-on-LA per-sign "
      "extraction run.")
    a("- **LM symmetry.** The v21 Eteocretan LM is used in direct "
      "symmetry with chic-v9. The alternative — per-pool LM swap — "
      "would couple the L3 score to candidate-substrate identity, "
      "which is methodologically odd for an LB-carryover anchor pool "
      "that is not naturally partitioned across the v10/v18/v21 "
      "substrate pools.")
    a("")
    a("## Determinism")
    a("")
    a("- No RNG. The L3 control-phoneme selection inherits chic-v5's "
      "sha256-keyed permutation construction (deterministic, no "
      "`random.Random(seed)` draw).")
    a("- Same inputs → byte-identical output. Re-running this script "
      "overwrites the result file with identical content.")
    a("")
    a("## Citations")
    a("")
    a("- Younger, J. G. (2020). *Linear A texts in phonetic "
      "transcription* (online edition).")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")
    a("- Schoep, I. (2002). *The Administration of Neopalatial Crete.* "
      "Liège.")
    a("")
    a("## Build provenance")
    a("")
    a(f"- Generated by `scripts/build_linear_a_v28.py` (mg-4a7b).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpus/all.jsonl` (LA corpus, 772 inscriptions); "
      "`pools/linear_b_carryover.yaml` (21 LB-carryover anchors via "
      "citation-string extraction); `pools/eteocretan.yaml` "
      "(Eteocretan phoneme inventory for the L3 candidate-pool "
      "filter); `harness/external_phoneme_models/eteocretan.json` "
      "(v21 LM artifact).")
    a("- Cross-script comparison numbers (chic-v9 / mg-18cb): "
      f"aggregate {chic_pct_total:.1f}%; per-line "
      f"L1={chic_pct_l1:.1f}% L2={chic_pct_l2:.1f}% "
      f"L3={chic_pct_l3:.1f}%; tier-2 unanimity "
      f"{chic_n_tier_2_correct}/{chic_n_tier_2} = "
      f"{chic_pct_tier_2:.1f}%.")

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


# ---------------------------------------------------------------------------
# chic-v9 numbers (hand-stable; loaded from the published md, not regenerated)
# ---------------------------------------------------------------------------


CHIC_V9_RESULT_MD = ROOT / "results" / "chic_v9_loo_validation.md"


def parse_chic_v9_summary() -> dict:
    """Read chic-v9's published numbers from
    ``results/chic_v9_loo_validation.md`` so v28's cross-script
    comparison stays consistent with the canonical chic-v9 artifact.

    Pulls aggregate accuracy, per-line accuracies, and tier-2
    classification accuracy via simple regex on the published table
    cells. Falls back to the hard-coded chic-v9 numbers if the file
    cannot be parsed (defensive guard for fresh checkouts).
    """
    fallback = {
        "pct_total": 20.0,
        "pct_l1": 20.0,
        "pct_l2": 20.0,
        "pct_l3": 5.0,
        "n_tier_2": 3,
        "n_tier_2_correct": 0,
    }
    if not CHIC_V9_RESULT_MD.exists():
        return fallback
    text = CHIC_V9_RESULT_MD.read_text(encoding="utf-8")
    out = dict(fallback)
    m = re.search(
        r"\| \*\*aggregate LOO accuracy\*\* \| \*\*([0-9.]+)%\*\* \|", text
    )
    if m:
        out["pct_total"] = float(m.group(1))
    for line_label, key in (
        ("L1", "pct_l1"),
        ("L2", "pct_l2"),
        ("L3", "pct_l3"),
    ):
        m = re.search(
            rf"\| {line_label} \([^)]+\) \| \d+/\d+ \| ([0-9.]+)% \|", text
        )
        if m:
            out[key] = float(m.group(1))
    m = re.search(
        r"\| n LOO tier-2 \(3-of-3 unanimous\) \| (\d+) \|", text
    )
    if m:
        out["n_tier_2"] = int(m.group(1))
    m = re.search(
        r"\| n LOO tier-2 with framework_class == known_class \| (\d+) \|",
        text,
    )
    if m:
        out["n_tier_2_correct"] = int(m.group(1))
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(*, progress: bool = True) -> dict:
    if progress:
        print("v28: loading inputs...", file=sys.stderr)
    la_records = load_la_records(CORPUS)
    full_anchor_map = parse_lb_carryover_anchors(LB_CARRYOVER_YAML)
    eteo_pool = _load_yaml(ETEO_POOL_YAML)
    lm = ExternalPhonemeModel.load_json(ETEO_LM)
    chic_v9_summary = parse_chic_v9_summary()

    if progress:
        print(
            f"  corpus_records={len(la_records)} "
            f"anchors={len(full_anchor_map)} "
            f"chic_v9_pct_total={chic_v9_summary['pct_total']:.1f}%",
            file=sys.stderr,
        )

    if progress:
        print(
            "v28: computing per-AB-sign distributional fingerprints...",
            file=sys.stderr,
        )
    anchor_ids = set(full_anchor_map.keys())
    fingerprints = compute_la_fingerprints(la_records, ab_ids=anchor_ids)

    rows: list[dict] = []
    anchors_sorted = sorted(full_anchor_map.keys(), key=_ab_sort_key)
    for i, target_sid in enumerate(anchors_sorted):
        if progress:
            print(
                f"v28: LOO {i + 1}/{len(anchors_sorted)} "
                f"holding out {target_sid} "
                f"(known={full_anchor_map[target_sid]})...",
                file=sys.stderr,
            )
        row = loo_validate_anchor(
            target_sid=target_sid,
            full_anchor_map=full_anchor_map,
            fingerprints=fingerprints,
            la_records=la_records,
            eteo_pool=eteo_pool,
            lm=lm,
        )
        rows.append(row)

    if progress:
        print("v28: writing LOO validation markdown...", file=sys.stderr)
    summary = write_loo_validation_md(
        rows,
        n_anchors=len(anchors_sorted),
        chic_v9_summary=chic_v9_summary,
        out_path=OUT_MD,
    )
    if progress:
        print(
            f"v28 done | n={summary['n_total']} "
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
