#!/usr/bin/env python3
"""Build the CHIC paleographic-anchor pool + partial-reading map (mg-362d, chic-v2).

chic-v1 (mg-c7e3) classified CHIC signs into syllabographic / ideogram /
ambiguous and enumerated 20 paleographic anchor candidates — CHIC
syllabographic signs that are visually similar to Linear A signs with
established Linear B carryover values. chic-v2 mechanically applies
those anchors to the CHIC corpus and produces a partial-reading map.

Inputs (from chic-v1):
  pools/cretan_hieroglyphic_signs.yaml             per-sign classification
  scripts/build_chic_signs.py::PALEOGRAPHIC_CANDIDATES   anchor seed list
  corpora/cretan_hieroglyphic/all.jsonl            CHIC corpus (chic-v0)
  harness/external_phoneme_models/mycenaean_greek.json   v12 LM artifact

Outputs:
  pools/cretan_hieroglyphic_anchors.yaml           anchor pool
  pools/schemas/chic_anchors.v1.schema.json        schema for the pool
  results/chic_partial_readings.md                 per-inscription map
  results/chic_anchor_density_leaderboard.md       top-30 by coverage
  results/chic_mg_perplexity_sanity_check.md       MG-LM cross-check

Confidence tiers
----------------

Per the chic-v2 ticket:
  tier-1   paleographic similarity well-established AND Linear B carryover stable.
  tier-2   paleographic similarity debated OR Linear B carryover uncertain.

The chic-v1 PALEOGRAPHIC_CANDIDATES list uses three confidence labels
(consensus / proposed / debated) where the Linear B carryover is stable
for every AB-id in the list (Ventris-Chadwick 1956 grid). So the
tier-mapping reduces to a paleographic-confidence collapse:

  consensus  → tier-1
  proposed   → tier-2  (paleographic match documented in one source)
  debated    → tier-2  (paleographic match disputed or contested)

Application convention
----------------------

For each CHIC inscription's tokens[], walk the sign positions:
  - clean sign (#NNN) → if anchored, emit phonetic value; else emit #NNN
  - uncertain (`[?:#NNN]`) → if anchored, emit `[?:VALUE]`; else `[?:#NNN]`
  - DIV → emit `/`
  - `[?]` (illegible) → emit `[?]`

Anchor coverage rate is computed over **syllabographic** sign positions
only (so an inscription that is mostly ideograms is not penalized for
having low anchor coverage on positions where anchors do not apply).

  numerator   = anchored syllabographic positions
  denominator = syllabographic positions (clean + uncertain readings)
  coverage    = numerator / denominator         (0.0 if no syll. positions)

Mycenaean-Greek LM perplexity sanity check
------------------------------------------

This is a *cross-check that the anchor inheritance machinery produces
well-formed phoneme strings*, not a decipherment claim. For each
top-30 most-anchored inscription:

  1. Walk the partial reading.
  2. Extract maximal contiguous runs of anchored phoneme tokens (runs
     are split by unanchored signs, DIV, `[?]`).
  3. Char-decompose each run; bracket with `<W>` sentinels.
  4. Score char-bigram log-probability under
     `harness/external_phoneme_models/mycenaean_greek.json` (the v12 MG
     LM trained on Linear-B-derived Mycenaean Greek transliterations).
  5. Normalize by total scored characters → per-char log-likelihood
     (nats).

This mirrors `external_phoneme_perplexity_v0` in `harness/metrics.py`,
but the runs come from anchor-application instead of partial-mapping
candidate scoring. Higher = more language-like under MG; lower = more
phonotactic distance from Mycenaean Greek. Both directions are
*informational, not evidential* — the substrate hypothesis for CHIC
remains pre-Greek substrate, not Mycenaean Greek itself.

Reproducibility: deterministic given the same inputs.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Re-use chic-v1's curated paleographic-candidate list as the single
# source of truth. The chic-v1 yaml carries the same data, but the
# Python list is the authoritative form (the yaml is a
# build-script-emitted derivative).
from scripts.build_chic_signs import (  # type: ignore  # noqa: E402
    PALEOGRAPHIC_CANDIDATES,
    classify_sign,
)

CHIC_CORPUS = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
SIGNS_YAML = ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
MG_LM_JSON = ROOT / "harness" / "external_phoneme_models" / "mycenaean_greek.json"

ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"
ANCHORS_SCHEMA = ROOT / "pools" / "schemas" / "chic_anchors.v1.schema.json"
ANCHORS_README = ROOT / "pools" / "cretan_hieroglyphic_anchors.README.md"
PARTIAL_READINGS_MD = ROOT / "results" / "chic_partial_readings.md"
LEADERBOARD_MD = ROOT / "results" / "chic_anchor_density_leaderboard.md"
PERPLEXITY_MD = ROOT / "results" / "chic_mg_perplexity_sanity_check.md"

FETCHED_AT = "2026-05-05T12:00:00Z"
TOP_K = 30  # leaderboard size + perplexity-check population


# ---------------------------------------------------------------------------
# Tier mapping
# ---------------------------------------------------------------------------


def confidence_to_tier(confidence: str) -> str:
    """consensus → tier-1; proposed/debated → tier-2."""
    if confidence == "consensus":
        return "tier-1"
    if confidence in ("proposed", "debated"):
        return "tier-2"
    raise ValueError(f"unknown confidence label: {confidence!r}")


# ---------------------------------------------------------------------------
# Anchor pool construction
# ---------------------------------------------------------------------------


def build_anchor_records(sign_freq: dict[str, int]) -> list[dict]:
    """Build the anchor records, sorted deterministically by chic_sign.

    sign_freq maps CHIC sign id → corpus frequency (from chic-v1 stats).
    """
    out: list[dict] = []
    for cand in sorted(PALEOGRAPHIC_CANDIDATES, key=lambda c: int(c["chic_sign"].lstrip("#"))):
        chic_sign = cand["chic_sign"]
        out.append({
            "chic_sign": chic_sign,
            "linear_a_sign": cand["linear_a_sign"],
            "linear_b_carryover_phonetic": cand["linear_b_value"],
            "confidence_tier": confidence_to_tier(cand["confidence"]),
            "chic_v1_confidence": cand["confidence"],
            "frequency": sign_freq.get(chic_sign, 0),
            "paleographic_citation": cand["citation"],
            "linear_b_citation": (
                "Ventris, M. & Chadwick, J. (1956). _Documents in "
                "Mycenaean Greek._ Cambridge. The Linear B grid value "
                f"{cand['linear_a_sign']}={cand['linear_b_value']} is "
                "established for syllabograms shared by Linear A and "
                "Linear B (the AB inventory)."
            ),
        })
    return out


def write_anchors_schema() -> None:
    schema = {
        "$id": "https://github.com/drellem2/lineara/pools/schemas/chic_anchors.v1.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Cretan Hieroglyphic paleographic anchor pool (v1)",
        "description": (
            "Tier-1 / tier-2 paleographic anchors mapping CHIC syllabographic "
            "signs to Linear B carryover phonetic values via Linear A "
            "intermediaries. Built by chic-v2 (mg-362d) from chic-v1's "
            "PALEOGRAPHIC_CANDIDATES list."
        ),
        "type": "object",
        "additionalProperties": True,
        "required": [
            "catalog",
            "version",
            "anchor_pool_rule",
            "source_citation",
            "anchors",
        ],
        "properties": {
            "catalog": {"const": "cretan_hieroglyphic_anchors"},
            "version": {"const": 1},
            "fetched_at": {"type": "string"},
            "anchor_pool_rule": {"type": "string"},
            "source_citation": {"type": "string"},
            "n_anchors_total": {"type": "integer", "minimum": 0},
            "n_tier_1": {"type": "integer", "minimum": 0},
            "n_tier_2": {"type": "integer", "minimum": 0},
            "anchors": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "chic_sign",
                        "linear_a_sign",
                        "linear_b_carryover_phonetic",
                        "confidence_tier",
                        "paleographic_citation",
                        "linear_b_citation",
                    ],
                    "properties": {
                        "chic_sign": {"type": "string", "pattern": "^#\\d{3}$"},
                        "linear_a_sign": {"type": "string", "pattern": "^AB\\d+$"},
                        "linear_b_carryover_phonetic": {"type": "string", "minLength": 1},
                        "confidence_tier": {"enum": ["tier-1", "tier-2"]},
                        "chic_v1_confidence": {"enum": ["consensus", "proposed", "debated"]},
                        "frequency": {"type": "integer", "minimum": 0},
                        "paleographic_citation": {"type": "string"},
                        "linear_b_citation": {"type": "string"},
                    },
                },
            },
        },
    }
    ANCHORS_SCHEMA.parent.mkdir(parents=True, exist_ok=True)
    ANCHORS_SCHEMA.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_anchors_yaml(anchors: list[dict]) -> None:
    n_t1 = sum(1 for a in anchors if a["confidence_tier"] == "tier-1")
    n_t2 = sum(1 for a in anchors if a["confidence_tier"] == "tier-2")

    header = (
        "# Cretan Hieroglyphic paleographic anchors (chic-v2; mg-362d)\n"
        "# Generated by scripts/build_chic_anchors.py from chic-v1's curated\n"
        "# PALEOGRAPHIC_CANDIDATES list (scripts/build_chic_signs.py).\n"
        "# Do not hand-edit; rerun the script.\n"
        "#\n"
        "# Schema: pools/schemas/chic_anchors.v1.schema.json\n"
        "# README: pools/cretan_hieroglyphic_anchors.README.md\n"
    )

    anchor_pool_rule = (
        "tier-1: paleographic similarity well-established (chic-v1 "
        "confidence=consensus) AND Linear B carryover stable.\n"
        "tier-2: paleographic similarity debated OR proposed in a single "
        "source (chic-v1 confidence in {proposed, debated}). Linear B "
        "carryover is stable for every AB-id in this pool (the AB "
        "inventory's Linear B grid values are established under "
        "Ventris-Chadwick 1956), so the tier collapses to a "
        "paleographic-confidence label."
    )

    source_citation = (
        "Olivier, J.-P. & Godart, L. (1996). _Corpus Hieroglyphicarum "
        "Inscriptionum Cretae_ (Études Crétoises 31). Paris.\n"
        "Younger, J. G. (online). _The Cretan Hieroglyphic Texts: a web "
        "edition of CHIC with commentary._ Wayback Machine snapshot "
        "20220703170656.\n"
        "Salgarella, E. (2020). _Aegean Linear Script(s)._ Cambridge.\n"
        "Decorte, R. (2017). _The First 'European' Writing._\n"
        "Civitillo, M. (2016). _La scrittura geroglifica minoica sui "
        "sigilli._\n"
        "Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._ "
        "Cambridge."
    )

    body: list[str] = []
    body.append("catalog: cretan_hieroglyphic_anchors")
    body.append("version: 1")
    body.append(f"fetched_at: {_yaml_str(FETCHED_AT)}")
    body.append("anchor_pool_rule: |")
    for line in anchor_pool_rule.splitlines():
        body.append(f"  {line}")
    body.append("source_citation: |")
    for line in source_citation.splitlines():
        body.append(f"  {line}")
    body.append(f"n_anchors_total: {len(anchors)}")
    body.append(f"n_tier_1: {n_t1}")
    body.append(f"n_tier_2: {n_t2}")
    body.append("anchors:")
    for a in anchors:
        body.append(f"- chic_sign: {_yaml_str(a['chic_sign'])}")
        body.append(f"  linear_a_sign: {_yaml_str(a['linear_a_sign'])}")
        body.append(
            f"  linear_b_carryover_phonetic: {_yaml_str(a['linear_b_carryover_phonetic'])}"
        )
        body.append(f"  confidence_tier: {_yaml_str(a['confidence_tier'])}")
        body.append(f"  chic_v1_confidence: {_yaml_str(a['chic_v1_confidence'])}")
        body.append(f"  frequency: {a['frequency']}")
        body.append(f"  paleographic_citation: {_yaml_str(a['paleographic_citation'])}")
        body.append(f"  linear_b_citation: {_yaml_str(a['linear_b_citation'])}")

    ANCHORS_YAML.parent.mkdir(parents=True, exist_ok=True)
    ANCHORS_YAML.write_text(header + "\n" + "\n".join(body) + "\n", encoding="utf-8")


def write_anchors_readme(anchors: list[dict], inscription_count: int) -> None:
    n_t1 = sum(1 for a in anchors if a["confidence_tier"] == "tier-1")
    n_t2 = sum(1 for a in anchors if a["confidence_tier"] == "tier-2")
    total_freq_t1 = sum(a["frequency"] for a in anchors if a["confidence_tier"] == "tier-1")
    total_freq_t2 = sum(a["frequency"] for a in anchors if a["confidence_tier"] == "tier-2")

    lines: list[str] = []
    lines.append("# Cretan Hieroglyphic paleographic anchors")
    lines.append("")
    lines.append(
        "Tier-1 / tier-2 paleographic anchors mapping CHIC syllabographic "
        "signs to Linear B carryover phonetic values via Linear A "
        "intermediaries. Built by chic-v2 (mg-362d) from chic-v1's "
        "(`mg-c7e3`) curated `PALEOGRAPHIC_CANDIDATES` list "
        "(`scripts/build_chic_signs.py`)."
    )
    lines.append("")
    lines.append("## Confidence tiers")
    lines.append("")
    lines.append(
        "- **tier-1** — paleographic similarity well-established "
        "(chic-v1 confidence=consensus) AND Linear B carryover stable."
    )
    lines.append(
        "- **tier-2** — paleographic similarity debated, or proposed in a "
        "single source (chic-v1 confidence in {proposed, debated})."
    )
    lines.append("")
    lines.append(
        "Linear B carryover is stable for every AB-id listed (the AB "
        "inventory's grid values are established under Ventris-Chadwick "
        "1956), so the tier-1 / tier-2 split reduces to a "
        "paleographic-confidence collapse."
    )
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- Total anchors: **{len(anchors)}**")
    lines.append(f"- Tier-1: **{n_t1}** anchors, {total_freq_t1} corpus occurrences")
    lines.append(f"- Tier-2: **{n_t2}** anchors, {total_freq_t2} corpus occurrences")
    lines.append(f"- CHIC inscriptions in the corpus: **{inscription_count}**")
    lines.append("")
    lines.append("## Anchor list")
    lines.append("")
    lines.append("| CHIC | Linear A | Linear B value | Tier | chic-v1 confidence | freq |")
    lines.append("|------|----------|----------------|------|--------------------|------|")
    for a in anchors:
        lines.append(
            f"| {a['chic_sign']} | {a['linear_a_sign']} | "
            f"{a['linear_b_carryover_phonetic']} | "
            f"{a['confidence_tier']} | {a['chic_v1_confidence']} | "
            f"{a['frequency']} |"
        )
    lines.append("")
    lines.append("## Inheritance application convention")
    lines.append("")
    lines.append(
        "For each CHIC inscription's `tokens[]`, sign positions are walked "
        "and rendered:"
    )
    lines.append("")
    lines.append("- `#NNN` (clean) → if anchored, emit the phonetic value; else `#NNN`.")
    lines.append("- `[?:#NNN]` (uncertain) → if anchored, `[?:VALUE]`; else `[?:#NNN]`.")
    lines.append("- `DIV` → `/` (word-divider).")
    lines.append("- `[?]` (illegible) → `[?]`.")
    lines.append("")
    lines.append(
        "Anchor coverage = anchored syllabographic positions / total "
        "syllabographic positions per chic-v1 classification "
        "(`pools/cretan_hieroglyphic_signs.yaml`). Ideogram, ambiguous, "
        "DIV, and illegible tokens are excluded from both numerator and "
        "denominator."
    )
    lines.append("")
    lines.append("## Source citations")
    lines.append("")
    lines.append("- Olivier, J.-P. & Godart, L. (1996). _CHIC._")
    lines.append("- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._")
    lines.append("- Salgarella, E. (2020). _Aegean Linear Script(s)._")
    lines.append("- Decorte, R. (2017). _The First 'European' Writing._")
    lines.append("- Civitillo, M. (2016). _La scrittura geroglifica minoica sui sigilli._")
    lines.append("- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._")
    lines.append("")
    ANCHORS_README.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Partial reading + leaderboard
# ---------------------------------------------------------------------------


def normalize_token(tok: str) -> tuple[str, str | None]:
    """Return (kind, sign_id_or_none).

    kind is one of:
      'sign_clean'      → tok was '#NNN'; sign_id_or_none = '#NNN'.
      'sign_uncertain'  → tok was '[?:#NNN]'; sign_id_or_none = '#NNN'.
      'div'             → tok was 'DIV'.
      'illegible'       → tok was '[?]'.
      'other'           → fallback (ideogram name, NUM:..., etc.); preserved as-is.
    """
    if tok == "DIV":
        return "div", None
    if tok == "[?]":
        return "illegible", None
    if tok.startswith("[?:#") and tok.endswith("]"):
        return "sign_uncertain", tok[3:-1]
    if tok.startswith("#"):
        return "sign_clean", tok
    return "other", None


def render_partial_reading(
    tokens: list[str],
    anchor_map: dict[str, str],
) -> tuple[list[str], int, int, int]:
    """Apply anchors to a token sequence; return (rendered, anchored,
    syllabographic_positions, ideogram_positions).

    syllabographic_positions counts both clean and uncertain readings of
    syllabographic CHIC signs; ideogram_positions counts ideogram
    readings (clean + uncertain) for context.
    """
    rendered: list[str] = []
    anchored = 0
    n_syll = 0
    n_ideo = 0
    for tok in tokens:
        kind, sid = normalize_token(tok)
        if kind == "div":
            rendered.append("/")
            continue
        if kind == "illegible":
            rendered.append("[?]")
            continue
        if kind in ("sign_clean", "sign_uncertain"):
            assert sid is not None
            cls, _note = classify_sign(sid)
            if cls == "syllabographic":
                n_syll += 1
                if sid in anchor_map:
                    val = anchor_map[sid]
                    if kind == "sign_uncertain":
                        rendered.append(f"[?:{val}]")
                    else:
                        rendered.append(val)
                    anchored += 1
                else:
                    if kind == "sign_uncertain":
                        rendered.append(f"[?:{sid}]")
                    else:
                        rendered.append(sid)
            elif cls == "ideogram":
                n_ideo += 1
                # Ideogram positions are not anchored — they're not the
                # target of paleographic anchor inheritance. Render with
                # an explicit IDEO: prefix so future readers see the
                # logogram class call.
                if kind == "sign_uncertain":
                    rendered.append(f"[?:IDEO:{sid}]")
                else:
                    rendered.append(f"IDEO:{sid}")
            else:
                # ambiguous — keep raw form
                if kind == "sign_uncertain":
                    rendered.append(f"[?:{sid}]")
                else:
                    rendered.append(sid)
            continue
        # other (NUM:..., raw ideogram name, etc.) — preserve verbatim.
        rendered.append(tok)
    return rendered, anchored, n_syll, n_ideo


def compute_partial_readings(
    records: list[dict],
    anchor_map: dict[str, str],
) -> list[dict]:
    out: list[dict] = []
    for rec in records:
        tokens = rec["tokens"]
        rendered, n_anch, n_syll, n_ideo = render_partial_reading(tokens, anchor_map)
        coverage = (n_anch / n_syll) if n_syll > 0 else 0.0
        out.append({
            "id": rec["id"],
            "site": rec.get("site") or "",
            "support": rec.get("support") or "",
            "transcription_confidence": rec.get("transcription_confidence") or "",
            "n_tokens": len(tokens),
            "n_syllabographic": n_syll,
            "n_ideogram": n_ideo,
            "n_anchored": n_anch,
            "anchor_coverage_rate": round(coverage, 4),
            "partial_reading": " ".join(rendered),
            "raw_tokens": list(tokens),
            "rendered_tokens": rendered,
        })
    return out


def write_partial_readings_md(rows: list[dict], anchors: list[dict]) -> None:
    rows_sorted = sorted(rows, key=lambda r: r["id"])
    n = len(rows_sorted)
    n_with_syll = sum(1 for r in rows_sorted if r["n_syllabographic"] > 0)
    n_with_anchor = sum(1 for r in rows_sorted if r["n_anchored"] > 0)
    total_syll = sum(r["n_syllabographic"] for r in rows_sorted)
    total_anchored = sum(r["n_anchored"] for r in rows_sorted)
    overall_coverage = (total_anchored / total_syll) if total_syll > 0 else 0.0

    lines: list[str] = []
    lines.append(
        "# CHIC partial readings under paleographic anchor inheritance "
        "(chic-v2; mg-362d)"
    )
    lines.append("")
    lines.append(
        "Partial readings of every CHIC inscription in "
        "`corpora/cretan_hieroglyphic/all.jsonl`, with each "
        "syllabographic sign position replaced by its anchor's Linear B "
        "carryover phonetic value (where the anchor pool covers the "
        "sign), or left as `#NNN` (where it does not). Built by "
        "`scripts/build_chic_anchors.py` from "
        "`pools/cretan_hieroglyphic_anchors.yaml`."
    )
    lines.append("")
    lines.append("## Rendering convention")
    lines.append("")
    lines.append("- Anchored clean reading: emit phonetic value (e.g. `ra`).")
    lines.append("- Anchored uncertain reading: emit `[?:value]`.")
    lines.append("- Unanchored clean reading: emit `#NNN`.")
    lines.append("- Unanchored uncertain reading: emit `[?:#NNN]`.")
    lines.append("- DIV: emit `/`.")
    lines.append("- Illegible: emit `[?]`.")
    lines.append("- Ideogram (chic-v1 sign_class=ideogram): emit `IDEO:#NNN`.")
    lines.append("")
    lines.append(
        "**Anchor coverage rate** = anchored syllabographic positions / "
        "total syllabographic positions (per chic-v1's classification). "
        "Ideogram, ambiguous, DIV, and illegible tokens are excluded from "
        "both numerator and denominator. An inscription with zero "
        "syllabographic positions reports coverage = 0.0 and is "
        "leaderboard-ineligible by convention."
    )
    lines.append("")
    lines.append("## Corpus rollup")
    lines.append("")
    lines.append(f"- Inscriptions: **{n}**")
    lines.append(f"- With ≥1 syllabographic position: **{n_with_syll}**")
    lines.append(f"- With ≥1 anchored position: **{n_with_anchor}**")
    lines.append(f"- Total syllabographic sign positions: **{total_syll}**")
    lines.append(f"- Total anchored positions: **{total_anchored}**")
    lines.append(
        f"- Corpus-wide anchor coverage: **{overall_coverage:.4f}** "
        f"({total_anchored}/{total_syll})"
    )
    lines.append(f"- Anchor pool size: **{len(anchors)}** "
                 f"({sum(1 for a in anchors if a['confidence_tier']=='tier-1')} tier-1, "
                 f"{sum(1 for a in anchors if a['confidence_tier']=='tier-2')} tier-2)")
    lines.append("")
    lines.append("## Per-inscription partial readings")
    lines.append("")
    lines.append(
        "| CHIC id | Site | Support | n_syll | n_anch | coverage | "
        "partial reading |"
    )
    lines.append("|---|---|---|--:|--:|--:|---|")
    for r in rows_sorted:
        reading = r["partial_reading"].replace("|", "\\|")
        if not reading:
            reading = "—"
        lines.append(
            f"| {r['id']} | {r['site']} | {r['support']} | "
            f"{r['n_syllabographic']} | {r['n_anchored']} | "
            f"{r['anchor_coverage_rate']:.4f} | `{reading}` |"
        )
    lines.append("")
    PARTIAL_READINGS_MD.parent.mkdir(parents=True, exist_ok=True)
    PARTIAL_READINGS_MD.write_text("\n".join(lines), encoding="utf-8")


def write_leaderboard_md(rows: list[dict], top_k: int) -> list[dict]:
    """Write the top-K leaderboard. Returns the top-K row list (for
    downstream MG-LM scoring)."""
    eligible = [r for r in rows if r["n_syllabographic"] > 0]
    # Stable sort: coverage descending, then n_anchored descending,
    # then n_syllabographic descending (tiebreaker for high-coverage
    # short inscriptions: prefer the more-anchored one), then id
    # ascending.
    eligible.sort(
        key=lambda r: (
            -r["anchor_coverage_rate"],
            -r["n_anchored"],
            -r["n_syllabographic"],
            r["id"],
        )
    )
    top = eligible[:top_k]

    lines: list[str] = []
    lines.append(
        f"# CHIC anchor-density leaderboard, top-{top_k} (chic-v2; mg-362d)"
    )
    lines.append("")
    lines.append(
        "Top-K most-anchored CHIC inscriptions, ranked by "
        "`anchor_coverage_rate` (anchored syllabographic positions / "
        "total syllabographic positions). Tiebreakers: anchored count "
        "(desc), then syllabographic count (desc), then CHIC id (asc)."
    )
    lines.append("")
    lines.append(
        "These are the inscriptions chic-v3+ work has the most "
        "existing constraint to leverage — the natural starting "
        "population for substrate framework application and "
        "per-sign-value extraction. Built by "
        "`scripts/build_chic_anchors.py`."
    )
    lines.append("")
    lines.append("## Leaderboard")
    lines.append("")
    lines.append(
        "| Rank | CHIC id | Site | Support | conf | n_syll | n_anch | "
        "coverage | partial reading |"
    )
    lines.append("|--:|---|---|---|---|--:|--:|--:|---|")
    for i, r in enumerate(top, start=1):
        reading = r["partial_reading"].replace("|", "\\|")
        if not reading:
            reading = "—"
        lines.append(
            f"| {i} | {r['id']} | {r['site']} | {r['support']} | "
            f"{r['transcription_confidence']} | "
            f"{r['n_syllabographic']} | {r['n_anchored']} | "
            f"{r['anchor_coverage_rate']:.4f} | `{reading}` |"
        )
    lines.append("")
    lines.append("## Sanity checks")
    lines.append("")
    if top:
        lines.append(f"- Top-1 coverage: **{top[0]['anchor_coverage_rate']:.4f}** ({top[0]['id']}).")
        lines.append(
            f"- Top-{len(top)} coverage cutoff: "
            f"**{top[-1]['anchor_coverage_rate']:.4f}** ({top[-1]['id']})."
        )
    n_perfect = sum(1 for r in top if r["anchor_coverage_rate"] >= 0.999)
    lines.append(f"- Inscriptions in top-{top_k} with full anchor coverage (≥0.999): **{n_perfect}**.")
    n_with_anchor_total = sum(1 for r in rows if r["n_anchored"] > 0)
    lines.append(
        f"- Total inscriptions with ≥1 anchored position: "
        f"**{n_with_anchor_total}** of {len(rows)}."
    )
    lines.append("")
    LEADERBOARD_MD.write_text("\n".join(lines), encoding="utf-8")
    return top


# ---------------------------------------------------------------------------
# Mycenaean-Greek LM perplexity sanity check
# ---------------------------------------------------------------------------


WORD_BOUNDARY = "<W>"
SPACE = " "
ALPHABET = tuple("abcdefghijklmnopqrstuvwxyz")
VOCAB: tuple[str, ...] = ALPHABET + (SPACE, WORD_BOUNDARY)
VOCAB_INDEX = {tok: i for i, tok in enumerate(VOCAB)}


def load_mg_lm() -> tuple[list[list[float]], dict]:
    with MG_LM_JSON.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if tuple(data["vocab"]) != VOCAB:
        raise ValueError(
            f"vocab mismatch in {MG_LM_JSON}: got {data['vocab']!r}, "
            f"expected {VOCAB!r}"
        )
    return [[float(v) for v in row] for row in data["bigram_log_probs"]], data.get("meta", {})


def char_decompose_phonemes(phonemes: list[str]) -> list[str]:
    out: list[str] = []
    for p in phonemes:
        for ch in p:
            out.append(ch if ch in VOCAB_INDEX else WORD_BOUNDARY)
    return out


def extract_anchor_runs(
    tokens: list[str],
    anchor_map: dict[str, str],
) -> list[list[str]]:
    """Walk a CHIC inscription's raw token sequence; return maximal
    contiguous runs of *anchored* phoneme tokens. Runs are split by
    unanchored signs, DIV, and `[?]`. Uncertain anchored readings are
    included in their run (the anchor still applies; chic-v1's
    frequency_uncertain count carries the uncertainty marker)."""
    runs: list[list[str]] = []
    cur: list[str] = []
    for tok in tokens:
        kind, sid = normalize_token(tok)
        if kind in ("sign_clean", "sign_uncertain") and sid is not None:
            cls, _note = classify_sign(sid)
            if cls == "syllabographic" and sid in anchor_map:
                cur.append(anchor_map[sid])
                continue
        # boundary
        if cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def score_runs_under_lm(
    runs: list[list[str]],
    bigram_log_probs: list[list[float]],
) -> tuple[float, int, int, int, float]:
    """Returns (per_char_loglik_nats, n_runs, n_phonemes, n_chars, total_loglik)."""
    n_runs = len(runs)
    n_phonemes = 0
    n_chars = 0
    total_loglik = 0.0
    for run in runs:
        chars = char_decompose_phonemes(run)
        if not chars:
            continue
        n_phonemes += len(run)
        n_chars += len(chars)
        seq = [WORD_BOUNDARY, *chars, WORD_BOUNDARY]
        for prev, cur in zip(seq[:-1], seq[1:]):
            i = VOCAB_INDEX.get(prev, VOCAB_INDEX[WORD_BOUNDARY])
            j = VOCAB_INDEX.get(cur, VOCAB_INDEX[WORD_BOUNDARY])
            total_loglik += bigram_log_probs[i][j]
    score = (total_loglik / n_chars) if n_chars > 0 else 0.0
    return score, n_runs, n_phonemes, n_chars, total_loglik


def write_perplexity_md(
    top_rows: list[dict],
    anchor_map: dict[str, str],
    raw_records_by_id: dict[str, dict],
) -> None:
    bigram_log_probs, meta = load_mg_lm()

    scored: list[dict] = []
    for r in top_rows:
        rec = raw_records_by_id[r["id"]]
        runs = extract_anchor_runs(rec["tokens"], anchor_map)
        score, n_runs, n_phon, n_chars, total = score_runs_under_lm(
            runs, bigram_log_probs
        )
        # Per-char perplexity (in nats → exp(-score))
        if n_chars > 0:
            perplexity = math.exp(-score)
        else:
            perplexity = float("nan")
        scored.append({
            **r,
            "n_runs": n_runs,
            "n_phonemes_scored": n_phon,
            "n_chars_scored": n_chars,
            "mg_loglik_per_char_nats": round(score, 6) if n_chars > 0 else None,
            "mg_perplexity_per_char": round(perplexity, 4) if n_chars > 0 else None,
            "mg_total_loglik_nats": round(total, 4) if n_chars > 0 else None,
        })

    # Aggregates
    scored_with_chars = [s for s in scored if s["n_chars_scored"] > 0]
    if scored_with_chars:
        mean_loglik = sum(s["mg_loglik_per_char_nats"] for s in scored_with_chars) / len(scored_with_chars)
        mean_perp = math.exp(-mean_loglik)
    else:
        mean_loglik = float("nan")
        mean_perp = float("nan")

    lines: list[str] = []
    lines.append(
        f"# CHIC partial-reading × Mycenaean Greek LM cross-check "
        f"(chic-v2; mg-362d)"
    )
    lines.append("")
    lines.append(
        "**Sanity check, NOT a decipherment claim.** This document scores "
        "the anchored portion of the top-30 most-anchored CHIC "
        "inscriptions (from "
        "`results/chic_anchor_density_leaderboard.md`) under the v12 "
        "Mycenaean-Greek char-bigram LM "
        "(`harness/external_phoneme_models/mycenaean_greek.json`). The "
        "purpose is to confirm that the anchor inheritance machinery "
        "produces *well-formed phoneme strings* — not to assert that "
        "CHIC encodes Mycenaean Greek. The substrate hypothesis for "
        "CHIC remains pre-Greek; high or low MG perplexity here is "
        "informational, not evidential for any specific reading."
    )
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append(
        "For each leaderboard inscription, walk the raw `tokens[]`. "
        "Extract maximal contiguous **runs** of anchored phoneme tokens "
        "(runs split by unanchored signs, DIV, and `[?]`). "
        "Char-decompose each run; bracket with `<W>` boundary sentinels. "
        "Score char-bigram log-probability under the MG LM. "
        "Normalize by total scored characters → per-char log-likelihood "
        "(nats). Per-char perplexity is `exp(-loglik)`."
    )
    lines.append("")
    lines.append(
        "This mirrors `external_phoneme_perplexity_v0` in "
        "`harness/metrics.py` (mg-ee18, harness v8); the only difference "
        "is run extraction comes from anchor application instead of "
        "candidate-equation scoring."
    )
    lines.append("")
    lines.append("## LM artifact")
    lines.append("")
    lines.append(f"- Source: `harness/external_phoneme_models/mycenaean_greek.json`")
    lines.append(f"- α (smoothing): {meta.get('alpha_rationale', 'n/a')}")
    lines.append(
        f"- Trained on: {meta.get('source', 'n/a')} "
        f"(n_words={meta.get('n_words', 'n/a')}, "
        f"n_chars={meta.get('n_chars', 'n/a')}, "
        f"n_bigrams_observed={meta.get('n_bigrams_observed', 'n/a')})"
    )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append(f"- Inscriptions scored: **{len(scored_with_chars)}** of {len(scored)}")
    if scored_with_chars:
        lines.append(f"- Mean per-char log-likelihood (nats): **{mean_loglik:.4f}**")
        lines.append(f"- Mean per-char perplexity: **{mean_perp:.4f}**")
    lines.append("")
    lines.append("## Per-inscription scores")
    lines.append("")
    lines.append(
        "| Rank | CHIC id | n_anch | n_runs | n_chars | "
        "loglik/char (nats) | perplexity/char | anchored phonemes |"
    )
    lines.append("|--:|---|--:|--:|--:|--:|--:|---|")
    for i, s in enumerate(scored, start=1):
        # Render the anchored-only phoneme stream for transparency.
        rec = raw_records_by_id[s["id"]]
        runs = extract_anchor_runs(rec["tokens"], anchor_map)
        run_str = " | ".join("-".join(r) for r in runs) if runs else "—"
        run_str = run_str.replace("|", "\\|")
        loglik_str = (
            f"{s['mg_loglik_per_char_nats']:.4f}"
            if s["mg_loglik_per_char_nats"] is not None
            else "n/a"
        )
        perp_str = (
            f"{s['mg_perplexity_per_char']:.4f}"
            if s["mg_perplexity_per_char"] is not None
            else "n/a"
        )
        lines.append(
            f"| {i} | {s['id']} | {s['n_anchored']} | {s['n_runs']} | "
            f"{s['n_chars_scored']} | {loglik_str} | {perp_str} | "
            f"`{run_str}` |"
        )
    lines.append("")
    lines.append("## Interpretation notes")
    lines.append("")
    lines.append(
        "- Per-char log-likelihood is in nats; **higher = more "
        "language-like** under the MG LM. The MG LM is trained on "
        "Linear-B-derived Mycenaean Greek transliterations (LiBER "
        "corpus, ~5.1k words / ~31k chars / α=0.1), so it scores "
        "highest on phoneme strings that look like Mycenaean Greek."
    )
    lines.append(
        "- A value far from MG-typical (toward higher perplexity) could "
        "mean either (a) the underlying CHIC language is *not* "
        "Mycenaean Greek (the working substrate hypothesis), or (b) the "
        "anchor pool is too small to produce stable runs (most CHIC "
        "inscriptions have very few anchored positions). Both readings "
        "are consistent with chic-v3+ continuing on a substrate-language "
        "framework rather than an MG framework."
    )
    lines.append(
        "- A value near MG-typical does *not* establish that CHIC "
        "encodes Mycenaean Greek. The MG LM's smoothing floor is high "
        "enough that short, low-information runs can score "
        "near-baseline under any input — see `harness/metrics.py` "
        "discussion of the small-coverage failure mode."
    )
    lines.append("")
    PERPLEXITY_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _yaml_str(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def load_chic_corpus() -> list[dict]:
    records: list[dict] = []
    with CHIC_CORPUS.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(json.loads(line))
    return records


def compute_sign_freq_from_corpus(records: list[dict]) -> dict[str, int]:
    """Count how many times each #NNN sign id (clean + uncertain) appears
    in the corpus token stream. Mirrors chic-v1's `frequency` field."""
    freq: dict[str, int] = {}
    for rec in records:
        for tok in rec["tokens"]:
            kind, sid = normalize_token(tok)
            if kind in ("sign_clean", "sign_uncertain") and sid is not None:
                freq[sid] = freq.get(sid, 0) + 1
    return freq


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=CHIC_CORPUS)
    parser.add_argument("--top-k", type=int, default=TOP_K)
    args = parser.parse_args(argv)

    if not args.corpus.exists():
        print(f"ERROR: missing CHIC corpus at {args.corpus}", file=sys.stderr)
        return 2
    if not MG_LM_JSON.exists():
        print(f"ERROR: missing MG LM at {MG_LM_JSON}", file=sys.stderr)
        return 2

    records = load_chic_corpus()
    sign_freq = compute_sign_freq_from_corpus(records)
    anchors = build_anchor_records(sign_freq)
    anchor_map: dict[str, str] = {
        a["chic_sign"]: a["linear_b_carryover_phonetic"] for a in anchors
    }

    write_anchors_schema()
    write_anchors_yaml(anchors)
    write_anchors_readme(anchors, inscription_count=len(records))

    rows = compute_partial_readings(records, anchor_map)
    write_partial_readings_md(rows, anchors)
    top_rows = write_leaderboard_md(rows, args.top_k)

    raw_records_by_id = {rec["id"]: rec for rec in records}
    write_perplexity_md(top_rows, anchor_map, raw_records_by_id)

    n_t1 = sum(1 for a in anchors if a["confidence_tier"] == "tier-1")
    n_t2 = sum(1 for a in anchors if a["confidence_tier"] == "tier-2")
    cutoff = top_rows[-1]["anchor_coverage_rate"] if top_rows else 0.0
    print(
        f"wrote {len(anchors)} anchors ({n_t1} tier-1, {n_t2} tier-2)  |  "
        f"{len(records)} inscriptions; "
        f"top-{args.top_k} leaderboard cutoff {cutoff:.4f}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
