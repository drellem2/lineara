#!/usr/bin/env python3
"""Mechanical-vs-scholarly comparison on scholar-proposed Linear A readings (mg-46d5, harness v22).

Extends v19's PS Za 2 ja-sa-sa-ra-me single-entry comparison and v20's
KU-RO/KI-RO null lookup to a population-level external-validation set
drawn from Younger's online catalog (and the Schoep / Salgarella / Palmer
upstream sources Younger references).

For each scholar-proposed contextual reading entry in
``corpora/scholar_proposed_readings/all.jsonl``:

  * Verify the entry's ``ab_sequence`` matches the inscription's
    syllabographic tokens at ``[span_start, span_end]``.
  * Compute the per-inscription consensus mechanical reading: for each
    AB sign in the span, the modal phoneme over all positive-paired-diff
    candidate equations targeting that inscription (the same per-sign
    aggregation v19 used). Local Dirichlet smoothing α=0.5, V = local
    vocabulary.
  * Compare phoneme-by-phoneme to the scholar's proposal. The scholar's
    proposal is a CV syllable per sign (e.g. "ku-ro" → ["ku", "ro"]);
    the substrate-phoneme inventory is letter-level (e.g. "k", "r",
    "th", "tz"). The comparison strategy follows v19's PS Za 2
    convention: compare the mechanical modal phoneme to the
    *first phoneme* of the scholarly CV (the consonant for CV syllables,
    the vowel itself for vowel-initial syllables a/e/i/o/u).
  * Per-entry match score = matches / |span|. Signs with no candidate
    proposals at all (no positive-paired-diff record hit them) count as
    misses (consistent with v19's per-inscription denominator
    convention).

Aggregate match-rate analysis
=============================
  * Aggregate match rate (sum-of-matches / sum-of-phonemes across all
    entries).
  * Per-category match rate.
  * Distribution of per-entry match scores: histogram, mean, median.
  * Highest- and lowest-matching entries.

Acceptance is **descriptive**, not pass/fail. The outcome shapes the
methodology paper's external-validation claim:
  * < 5%  — strong reinforcement of v13 / v19's "internal consensus
            does not imply external correctness"
  * > 20% — finding warranting deeper investigation (partial recovery
            of scholar-meaningful readings)
  * 5–20% — ambiguous middle case; document with hedging

Output
======
  results/rollup.scholar_proposed_readings_comparison.md

Determinism
===========
Byte-identical across re-runs given the same result stream + manifests +
hypothesis YAMLs + scholar_proposed_readings/all.jsonl. No RNG. Tie-
breaking on modal phoneme is alphabetical (inherited from
``per_sign_consensus_local``).

Usage
=====
  python3 scripts/compare_scholar_proposed.py
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.per_inscription_coherence import (  # type: ignore
    collect_per_inscription_proposals,
    per_sign_consensus_local,
    syllabographic_tokens,
)
from scripts.per_surface_bayesian_rollup import (  # type: ignore
    _DEFAULT_AUTO,
    _DEFAULT_AUTO_SIG,
    _DEFAULT_LANGUAGE_DISPATCH,
    _DEFAULT_POOLS,
    _DEFAULT_RESULTS_DIR,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_VALIDATED_POOLS: tuple[str, ...] = ("aquitanian", "etruscan", "toponym")
_DEFAULT_ALPHA = 0.5
_DEFAULT_THRESHOLD = 0.5
_DEFAULT_ENTRIES_PATH = (
    Path("corpora") / "scholar_proposed_readings" / "all.jsonl"
)
_DEFAULT_OUT_PATH = (
    Path("results") / "rollup.scholar_proposed_readings_comparison.md"
)


# ---------------------------------------------------------------------------
# Entry loader
# ---------------------------------------------------------------------------


def load_entries(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


# ---------------------------------------------------------------------------
# Corpus loader
# ---------------------------------------------------------------------------


def load_corpus(path: Path) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            by_id[r["id"]] = r
    return by_id


# ---------------------------------------------------------------------------
# Per-entry comparison
# ---------------------------------------------------------------------------


def compare_entry(
    *,
    entry: dict,
    corpus_by_id: dict[str, dict],
    histograms_by_ins: dict[str, dict[str, dict[str, int]]],
    alpha: float,
    threshold: float,
) -> dict:
    """Compare one scholar-proposed reading entry to the per-inscription consensus.

    Returns a dict with the per-AB-sign comparison + aggregate per-entry
    statistics.
    """
    ins_id = entry["inscription_id"]
    span_start = entry["span_start"]
    span_end = entry["span_end"]
    ab_seq = entry["ab_sequence"]
    scholar_first = entry["scholarly_first_phoneme"]
    scholar_cvs = entry["scholarly_phonemes"]

    rec = corpus_by_id.get(ins_id)
    if rec is None:
        raise ValueError(f"entry {entry['entry_id']}: inscription {ins_id} not in corpus")

    syll = syllabographic_tokens(rec["tokens"])
    actual = syll[span_start:span_end]
    if actual != ab_seq:
        raise ValueError(
            f"entry {entry['entry_id']}: ab_sequence {ab_seq} does not match "
            f"corpus syllabographic tokens at span [{span_start}, {span_end}] "
            f"for inscription {ins_id} (got {actual})"
        )

    histograms = histograms_by_ins.get(ins_id, {})
    per_sign: list[dict] = []
    matches_first = 0
    matches_robust = 0   # match AND modal_posterior > threshold AND n_proposals >= 2
    matches_full = 0     # mechanical == full CV (almost never)
    n_with_proposals = 0
    n_signs = len(ab_seq)

    for pos, (sign, sf, scv) in enumerate(zip(ab_seq, scholar_first, scholar_cvs)):
        h = histograms.get(sign, {})
        info = per_sign_consensus_local(h, alpha=alpha)
        if info is None:
            per_sign.append(
                {
                    "position": pos,
                    "sign": sign,
                    "scholarly_cv": scv,
                    "scholarly_first_phoneme": sf,
                    "mechanical_modal": None,
                    "n_proposals": 0,
                    "modal_posterior": None,
                    "match_first": False,
                    "match_robust": False,
                    "match_full": False,
                }
            )
            continue
        n_with_proposals += 1
        modal = info["modal_phoneme"]
        is_match_first = modal == sf
        is_match_full = modal == scv
        is_match_robust = (
            is_match_first
            and info["modal_posterior"] > threshold
            and info["n_proposals"] >= 2
        )
        if is_match_first:
            matches_first += 1
        if is_match_robust:
            matches_robust += 1
        if is_match_full:
            matches_full += 1
        per_sign.append(
            {
                "position": pos,
                "sign": sign,
                "scholarly_cv": scv,
                "scholarly_first_phoneme": sf,
                "mechanical_modal": modal,
                "n_proposals": info["n_proposals"],
                "modal_posterior": info["modal_posterior"],
                "match_first": is_match_first,
                "match_robust": is_match_robust,
                "match_full": is_match_full,
            }
        )

    return {
        "entry_id": entry["entry_id"],
        "inscription_id": ins_id,
        "span": (span_start, span_end),
        "ab_sequence": ab_seq,
        "scholarly_phonemes": scholar_cvs,
        "scholarly_first_phoneme": scholar_first,
        "category": entry["category"],
        "gloss": entry["gloss"],
        "source_citation": entry["source_citation"],
        "n_signs": n_signs,
        "n_with_proposals": n_with_proposals,
        "matches_first": matches_first,
        "matches_robust": matches_robust,
        "matches_full": matches_full,
        "match_rate_first": matches_first / n_signs,
        "match_rate_robust": matches_robust / n_signs,
        "match_rate_full": matches_full / n_signs,
        "per_sign": per_sign,
    }


# ---------------------------------------------------------------------------
# Aggregate analysis
# ---------------------------------------------------------------------------


def aggregate_results(rows: list[dict]) -> dict:
    """Compute aggregate match rates and per-category breakdown."""
    total_signs = sum(r["n_signs"] for r in rows)
    total_with_proposals = sum(r["n_with_proposals"] for r in rows)
    total_matches_first = sum(r["matches_first"] for r in rows)
    total_matches_robust = sum(r["matches_robust"] for r in rows)
    total_matches_full = sum(r["matches_full"] for r in rows)

    by_cat: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "n_entries": 0,
            "n_signs": 0,
            "n_with_proposals": 0,
            "matches_first": 0,
            "matches_robust": 0,
            "matches_full": 0,
        }
    )
    for r in rows:
        c = by_cat[r["category"]]
        c["n_entries"] += 1
        c["n_signs"] += r["n_signs"]
        c["n_with_proposals"] += r["n_with_proposals"]
        c["matches_first"] += r["matches_first"]
        c["matches_robust"] += r["matches_robust"]
        c["matches_full"] += r["matches_full"]

    per_entry_scores = sorted(r["match_rate_first"] for r in rows)
    if per_entry_scores:
        mean_score = statistics.fmean(per_entry_scores)
        median_score = statistics.median(per_entry_scores)
    else:
        mean_score = float("nan")
        median_score = float("nan")

    histogram_buckets = [0.0, 0.0001, 0.20, 0.40, 0.60, 0.80, 1.0001]
    histogram_labels = [
        "0%",
        "(0%, 20%)",
        "[20%, 40%)",
        "[40%, 60%)",
        "[60%, 80%)",
        "[80%, 100%]",
    ]
    hist = [0] * len(histogram_labels)
    for s in per_entry_scores:
        for j in range(len(histogram_labels)):
            lo = histogram_buckets[j]
            hi = histogram_buckets[j + 1]
            if lo <= s < hi:
                hist[j] += 1
                break

    sorted_rows = sorted(
        rows, key=lambda r: (-r["match_rate_first"], r["entry_id"])
    )
    return {
        "n_entries": len(rows),
        "n_signs_total": total_signs,
        "n_with_proposals_total": total_with_proposals,
        "matches_first_total": total_matches_first,
        "matches_robust_total": total_matches_robust,
        "matches_full_total": total_matches_full,
        "aggregate_match_rate_first": (
            total_matches_first / total_signs if total_signs else float("nan")
        ),
        "aggregate_match_rate_robust": (
            total_matches_robust / total_signs if total_signs else float("nan")
        ),
        "aggregate_match_rate_full": (
            total_matches_full / total_signs if total_signs else float("nan")
        ),
        "by_category": dict(by_cat),
        "per_entry_mean": mean_score,
        "per_entry_median": median_score,
        "per_entry_min": min(per_entry_scores) if per_entry_scores else float("nan"),
        "per_entry_max": max(per_entry_scores) if per_entry_scores else float("nan"),
        "histogram_labels": histogram_labels,
        "histogram_counts": hist,
        "highest_entries": sorted_rows[:5],
        "lowest_entries": list(reversed(sorted_rows))[:5],
    }


def classify_aggregate_outcome(rate: float) -> str:
    """Apply the brief's three-band descriptive classification."""
    if math.isnan(rate):
        return "n/a"
    pct = rate * 100.0
    if pct < 5.0:
        return "STRONG NULL: < 5% (reinforces v13 / v19 verdicts)"
    if pct > 20.0:
        return "INVESTIGATE: > 20% (partial recovery — warrants follow-up)"
    return "AMBIGUOUS: 5–20% (partial; document with hedging)"


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt_pct(x: float, w: int = 2) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x * 100:.{w}f}%"


def _fmt_modal(info: dict) -> str:
    if info["mechanical_modal"] is None:
        return "·"
    return info["mechanical_modal"]


def _fmt_per_sign_compact(per_sign: list[dict]) -> str:
    return "-".join(_fmt_modal(p) for p in per_sign)


def _fmt_scholar_compact(per_sign: list[dict]) -> str:
    return "-".join(p["scholarly_phonemes"] if isinstance(p, dict) and "scholarly_phonemes" in p else p["scholarly_cv"] for p in per_sign)


def render_md(
    *,
    rows: list[dict],
    aggregate: dict,
    pools: list[str],
    alpha: float,
    threshold: float,
    entries_path: Path,
) -> str:
    out: list[str] = []
    out.append("# Scholar-proposed-reading external-validation comparison (mg-46d5, harness v22)\n")
    out.append(
        "Generated by `scripts/compare_scholar_proposed.py`. Extends v19's "
        "single-entry libation-formula comparison (PS Za 2: 0/5 match against "
        "scholarly `ja-sa-sa-ra-me`) and v20's KU-RO/KI-RO null lookup on the "
        "v19 cascade-candidate accountancy tablets to a population-level "
        f"external-validation set of {aggregate['n_entries']} scholar-proposed "
        "contextual readings drawn from Younger's online catalog (Younger, "
        "*Linear A texts in phonetic transcription*, retrieved 2026-05-04) "
        "and the Schoep / Salgarella / Palmer / Davis upstream sources.\n"
    )
    out.append(
        "**Comparison strategy.** For each scholar-proposed reading entry, "
        "verify its ``ab_sequence`` matches the inscription's syllabographic "
        "tokens at the recorded span; for each AB sign in the span, compute "
        "the per-inscription modal phoneme (the same v19 per-sign consensus "
        f"under local Dirichlet smoothing, α={alpha:g}, V = local "
        "vocabulary, over all positive-paired-diff candidate equations "
        f"targeting that inscription across the {len(pools)} validated "
        f"substrate pools — {', '.join(pools)} — under the same-LM "
        "`external_phoneme_perplexity_v0` metric); compare to the *first "
        "phoneme* of the scholarly CV (consonant for CV syllables, vowel "
        "itself for vowel-initial syllables a/e/i/o/u). The per-AB-sign "
        "comparison strategy follows v19's PS Za 2 convention exactly so "
        "results are continuous with the prior single-entry result.\n"
    )
    out.append(
        "**What is and isn't a scholar-proposed reading.** A scholar-proposed "
        "reading is a *contextual* claim that this AB-sequence in this "
        "inscription means this thing in this language (e.g. ``KU-RO`` on an "
        "accountancy tablet means total/sum). It is **not** a sign-value "
        "transliteration in isolation (``AB67 = ki``) — those are phoneme "
        "carryovers from Linear B, not contextual readings. The set here "
        "draws strictly from Younger's contextual entries; sign-value-only "
        "transliterations are excluded by construction.\n"
    )
    out.append(
        "**Acceptance is descriptive, not pass/fail.** The aggregate match "
        "rate is the headline statistic. The outcome shapes the methodology "
        "paper's external-validation claim:\n\n"
        "* < 5%  — strong reinforcement of v13 / v19's verdict that internal "
        "consensus does not imply external correctness;\n"
        "* > 20% — partial recovery of scholar-meaningful readings, "
        "warranting deeper investigation;\n"
        "* 5–20% — ambiguous middle case; document with appropriate "
        "hedging.\n"
    )
    out.append(
        "**Determinism.** Byte-identical output across re-runs given the same "
        "`results/experiments.external_phoneme_perplexity_v0.jsonl`, "
        "`hypotheses/auto/*`, `hypotheses/auto_signatures/*`, `pools/*`, and "
        f"`{entries_path}`. No RNG. Tie-breaking on modal phoneme is "
        "alphabetical.\n"
    )

    # Headline.
    out.append("## Headline\n")
    rate_first = aggregate["aggregate_match_rate_first"]
    rate_robust = aggregate["aggregate_match_rate_robust"]
    rate_full = aggregate["aggregate_match_rate_full"]
    classification = classify_aggregate_outcome(rate_first)
    out.append(
        f"* **Aggregate match rate (consonant of scholarly CV):** "
        f"{aggregate['matches_first_total']}/{aggregate['n_signs_total']} "
        f"= **{_fmt_pct(rate_first, 2)}** — {classification}.\n"
        f"* **Aggregate match rate (robust: consonant + modal_posterior > "
        f"{threshold} + n_proposals ≥ 2):** "
        f"{aggregate['matches_robust_total']}/{aggregate['n_signs_total']} = "
        f"{_fmt_pct(rate_robust, 2)}.\n"
        f"* **Aggregate match rate (full CV — strict; mechanical phoneme equals "
        f"the entire scholarly syllable):** "
        f"{aggregate['matches_full_total']}/{aggregate['n_signs_total']} = "
        f"{_fmt_pct(rate_full, 2)}. (Substrate-pool phoneme inventory is "
        "letter-level, not syllabic, so this strict rate is structurally "
        "near-zero and reported only for completeness.)\n"
        f"* **n entries:** {aggregate['n_entries']}; "
        f"**n AB-sign comparison points:** {aggregate['n_signs_total']}; "
        f"**n with at least one substrate proposal:** "
        f"{aggregate['n_with_proposals_total']}.\n"
        f"* **Per-entry match-rate distribution:** mean "
        f"{_fmt_pct(aggregate['per_entry_mean'], 2)}, median "
        f"{_fmt_pct(aggregate['per_entry_median'], 2)}, min "
        f"{_fmt_pct(aggregate['per_entry_min'], 2)}, max "
        f"{_fmt_pct(aggregate['per_entry_max'], 2)}.\n"
    )

    # Distribution histogram.
    out.append("## Per-entry match-rate distribution\n")
    out.append("| bucket | n entries |")
    out.append("|:--|---:|")
    for label, count in zip(
        aggregate["histogram_labels"], aggregate["histogram_counts"]
    ):
        out.append(f"| {label} | {count} |")
    out.append("")

    # Per-category breakdown.
    out.append("## Per-category breakdown\n")
    out.append(
        "| category | n entries | n signs | n with proposals | matches (first) | "
        "match rate (first) | matches (robust) | match rate (robust) |"
    )
    out.append("|:--|---:|---:|---:|---:|---:|---:|---:|")
    cats_sorted = sorted(
        aggregate["by_category"].items(),
        key=lambda kv: (-kv[1]["n_entries"], kv[0]),
    )
    for cat, c in cats_sorted:
        rate_c_first = (
            c["matches_first"] / c["n_signs"] if c["n_signs"] else float("nan")
        )
        rate_c_robust = (
            c["matches_robust"] / c["n_signs"] if c["n_signs"] else float("nan")
        )
        out.append(
            f"| `{cat}` | {c['n_entries']} | {c['n_signs']} | "
            f"{c['n_with_proposals']} | {c['matches_first']} | "
            f"{_fmt_pct(rate_c_first, 2)} | {c['matches_robust']} | "
            f"{_fmt_pct(rate_c_robust, 2)} |"
        )
    out.append("")

    # Highest- and lowest-matching entries.
    out.append("## Highest-matching entries (top 5 by per-entry match rate)\n")
    out.append(
        "| entry_id | inscription | category | scholarly | mechanical | "
        "matches/total | match rate |"
    )
    out.append("|:--|:--|:--|:--|:--|:--|---:|")
    for r in aggregate["highest_entries"]:
        scholar_str = "-".join(r["scholarly_phonemes"])
        mech_str = _fmt_per_sign_compact(r["per_sign"])
        out.append(
            f"| `{r['entry_id']}` | `{r['inscription_id']}` | `{r['category']}` | "
            f"{scholar_str} | {mech_str} | "
            f"{r['matches_first']}/{r['n_signs']} | "
            f"{_fmt_pct(r['match_rate_first'], 2)} |"
        )
    out.append("")

    out.append("## Lowest-matching entries (bottom 5 by per-entry match rate)\n")
    out.append(
        "| entry_id | inscription | category | scholarly | mechanical | "
        "matches/total | match rate |"
    )
    out.append("|:--|:--|:--|:--|:--|:--|---:|")
    for r in aggregate["lowest_entries"]:
        scholar_str = "-".join(r["scholarly_phonemes"])
        mech_str = _fmt_per_sign_compact(r["per_sign"])
        out.append(
            f"| `{r['entry_id']}` | `{r['inscription_id']}` | `{r['category']}` | "
            f"{scholar_str} | {mech_str} | "
            f"{r['matches_first']}/{r['n_signs']} | "
            f"{_fmt_pct(r['match_rate_first'], 2)} |"
        )
    out.append("")

    # Full per-entry table.
    out.append("## Per-entry comparison (full table)\n")
    out.append(
        "| entry_id | inscription | span | category | ab_sequence | "
        "scholarly | mechanical | matches/total | match rate |"
    )
    out.append("|:--|:--|:--|:--|:--|:--|:--|:--|---:|")
    for r in sorted(rows, key=lambda r: (r["inscription_id"], r["span"][0], r["entry_id"])):
        scholar_str = "-".join(r["scholarly_phonemes"])
        mech_str = _fmt_per_sign_compact(r["per_sign"])
        ab_str = "-".join(r["ab_sequence"])
        span_str = f"[{r['span'][0]}, {r['span'][1]})"
        out.append(
            f"| `{r['entry_id']}` | `{r['inscription_id']}` | {span_str} | "
            f"`{r['category']}` | {ab_str} | {scholar_str} | {mech_str} | "
            f"{r['matches_first']}/{r['n_signs']} | "
            f"{_fmt_pct(r['match_rate_first'], 2)} |"
        )
    out.append("")

    # Per-AB-sign breakdown for entries that match at least one sign.
    matching_rows = [r for r in rows if r["matches_first"] > 0]
    out.append(
        f"## Per-AB-sign breakdown for entries with at least one match (n="
        f"{len(matching_rows)})\n"
    )
    if not matching_rows:
        out.append(
            "_No entries scored any matches against the scholar-proposed "
            "reading. Internal consensus does not recover the scholarly "
            "consonantal first segment for any sign in any of the "
            f"{aggregate['n_entries']} entries._\n"
        )
    else:
        out.append(
            "Each row: one (entry, position, sign) tuple. "
            "``modal_posterior`` is the local-Dirichlet smoothed posterior "
            "of the modal mechanical phoneme; ``n_proposals`` is the number "
            "of positive-paired-diff candidates contributing a phoneme for "
            "that sign at that inscription.\n"
        )
        out.append(
            "| entry_id | inscription | pos | sign | scholarly cv | "
            "scholarly first | mechanical modal | n_proposals | "
            "modal_posterior | match (first) | match (robust) |"
        )
        out.append("|:--|:--|---:|:--|:--|:--|:--|---:|---:|:--|:--|")
        for r in matching_rows:
            for ps in r["per_sign"]:
                if not ps["match_first"]:
                    continue
                mp_str = (
                    "n/a"
                    if ps["modal_posterior"] is None
                    else f"{ps['modal_posterior']:.4f}"
                )
                out.append(
                    f"| `{r['entry_id']}` | `{r['inscription_id']}` | "
                    f"{ps['position']} | `{ps['sign']}` | "
                    f"{ps['scholarly_cv']} | {ps['scholarly_first_phoneme']} | "
                    f"`{ps['mechanical_modal']}` | {ps['n_proposals']} | "
                    f"{mp_str} | {'✓' if ps['match_first'] else '✗'} | "
                    f"{'✓' if ps['match_robust'] else '✗'} |"
                )
        out.append("")

    out.append("## Notes\n")
    out.append(
        "- *Comparison granularity.* The per-inscription consensus emits "
        "ONE phoneme per AB sign; the scholarly proposal is a CV syllable "
        "per sign. The headline `match (first)` rate compares the "
        "mechanical modal phoneme to the *first phoneme* of the scholarly "
        "CV — the consonant for CV syllables, the vowel itself for vowel-"
        "initial syllables (a/e/i/o/u). This is the same convention v19 "
        "applied to the PS Za 2 ja-sa-sa-ra-me comparison; v22 applies it "
        f"uniformly across the {aggregate['n_entries']}-entry external-"
        "validation set so the result is continuous with v19's single-"
        "entry headline.\n"
    )
    out.append(
        "- *Robust comparison.* `match (robust)` is the stricter variant: "
        f"requires `match_first` AND modal_posterior > {threshold} AND "
        "n_proposals ≥ 2. This drops trivial-pass signs whose only "
        "supporting candidate happens to propose the right consonant "
        "(no genuine consensus).\n"
    )
    out.append(
        "- *Misses are misses.* A sign with no candidate proposals (no "
        "positive-paired-diff record hit it in this inscription) counts "
        "as a miss in the per-entry denominator, mirroring v19's "
        "per-inscription denominator convention. The brief asks for a "
        "headline match rate, not a conditional-on-coverage rate; "
        "reporting only the conditional rate would mask coverage gaps.\n"
    )
    out.append(
        "- *Continuity with v19 / v20.* PS Za 2 (entry "
        "`jasarame_PSZa2`) is the v19 PS Za 2 libation-formula entry; "
        "its 0/5 match here is a regression test on v19's reported "
        "headline. KU-RO and KI-RO entries on the v19 cascade-candidate "
        "tablets KH 5 and KH 10 are *absent* by v20's null finding "
        "(neither sequence appears in those inscriptions); v22's set "
        "draws KU-RO/KI-RO from inscriptions where they actually appear "
        "(predominantly Haghia Triada accountancy).\n"
    )
    out.append(
        "- *Why no v9 root-surface filtering?* v22 inherits v19's "
        "all-positive-paired-diff aggregation: every positive-paired-diff "
        "candidate targeting an inscription contributes to the "
        "per-inscription histogram, regardless of whether its root "
        "surface is in the v10 top-20. The brief frames v22 as extending "
        "v19's footprint, not as substituting a v13-style top-20 "
        "restriction; restricting here would inject a different "
        "selection criterion than v19 used.\n"
    )
    out.append(
        "- *Scholar set ceiling.* Linear A is mostly undeciphered; "
        "Younger's contextual reading proposals number in the dozens, "
        "not hundreds. The brief sets ≥25 as the realistic ceiling for "
        "this kind of population-level scholarly-comparison set; v22 "
        f"ships {aggregate['n_entries']} entries across "
        f"{len(aggregate['by_category'])} categories. Sign-value-only "
        "transliterations (`AB67 = ki`) are excluded by construction "
        "because they are not contextual readings.\n"
    )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=Path("corpus") / "all.jsonl")
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="Repo root (used to resolve hypothesis_path entries).",
    )
    parser.add_argument(
        "--pools",
        type=str,
        default=",".join(_DEFAULT_VALIDATED_POOLS),
        help=(
            "Comma-separated substrate pools to aggregate over. Default: "
            "the three validated pools (aquitanian, etruscan, toponym)."
        ),
    )
    parser.add_argument("--alpha", type=float, default=_DEFAULT_ALPHA)
    parser.add_argument("--threshold", type=float, default=_DEFAULT_THRESHOLD)
    parser.add_argument(
        "--entries",
        type=Path,
        default=_DEFAULT_ENTRIES_PATH,
        help="Path to the scholar_proposed_readings JSONL.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=_DEFAULT_OUT_PATH,
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path for a summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    proposals = collect_per_inscription_proposals(
        pools=pools,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        pools_dir=args.pools_dir,
        results_dir=args.results_dir,
        repo_root=args.repo_root,
        language_dispatch=language_dispatch,
    )
    histograms_by_ins = proposals["histograms_by_ins"]

    corpus_by_id = load_corpus(args.corpus)
    entries = load_entries(args.entries)

    rows: list[dict] = []
    for entry in entries:
        rows.append(
            compare_entry(
                entry=entry,
                corpus_by_id=corpus_by_id,
                histograms_by_ins=histograms_by_ins,
                alpha=args.alpha,
                threshold=args.threshold,
            )
        )

    aggregate = aggregate_results(rows)

    text = render_md(
        rows=rows,
        aggregate=aggregate,
        pools=pools,
        alpha=args.alpha,
        threshold=args.threshold,
        entries_path=args.entries,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)

    summary = {
        "pools": pools,
        "alpha": args.alpha,
        "threshold": args.threshold,
        "entries_path": str(args.entries),
        "n_entries": aggregate["n_entries"],
        "n_signs_total": aggregate["n_signs_total"],
        "n_with_proposals_total": aggregate["n_with_proposals_total"],
        "matches_first_total": aggregate["matches_first_total"],
        "matches_robust_total": aggregate["matches_robust_total"],
        "matches_full_total": aggregate["matches_full_total"],
        "aggregate_match_rate_first": aggregate["aggregate_match_rate_first"],
        "aggregate_match_rate_robust": aggregate["aggregate_match_rate_robust"],
        "aggregate_match_rate_full": aggregate["aggregate_match_rate_full"],
        "per_entry_mean": aggregate["per_entry_mean"],
        "per_entry_median": aggregate["per_entry_median"],
        "per_entry_min": aggregate["per_entry_min"],
        "per_entry_max": aggregate["per_entry_max"],
        "outcome_band": classify_aggregate_outcome(
            aggregate["aggregate_match_rate_first"]
        ),
        "by_category": {
            cat: {
                **c,
                "match_rate_first": (
                    c["matches_first"] / c["n_signs"]
                    if c["n_signs"]
                    else float("nan")
                ),
                "match_rate_robust": (
                    c["matches_robust"] / c["n_signs"]
                    if c["n_signs"]
                    else float("nan")
                ),
            }
            for cat, c in aggregate["by_category"].items()
        },
    }
    if args.summary_json:
        args.summary_json.write_text(
            json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
        )
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
