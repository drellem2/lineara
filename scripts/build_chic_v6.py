#!/usr/bin/env python3
"""chic-v6: mechanical verification of chic-v5 candidate proposals (mg-a557).

Daniel's reframing (2026-05-05) repositioned chic-v6 from "domain-expert
review" (out of polecat scope) to **mechanical verification before
specialist review** (in scope). Verification of "is this doing
something?" is much easier than hypothesis generation: chic-v5 generated
candidate proposals from internal evidence (4 lines converging on
phoneme classes). chic-v6 mechanically checks whether *applying* those
proposals to the corpus produces hits against three external-scholarship
sources we already have ingested.

The output is **NOT a decipherment claim**. It is a verification-rate
report: per-tier match counts against three pre-registered match
sources. If chic-v5 extensions produce no additional matches beyond
the chic-v2 anchors, the framework's per-sign extraction does not
survive external verification (consistent with the v13 / v22 / v24
internal-vs-external pattern). If it does, the marginal lift is the
chic-v5 framework's verification-grade contribution. Either outcome
is publishable.

Pre-registered match criteria
=============================

Match criteria are pre-registered before any match counts are computed
(per the chic-v6 brief). They are NOT relaxed mid-analysis to
manufacture hits.

  Source A — scholar-proposed Linear-A readings
    A scholar entry with `ab_sequence` of length k matches a CHIC
    inscription iff there exists a contiguous run of k
    syllabographic-class tokens (CHIC #NNN positions, classified by
    chic-v1) within a single DIV-bounded segment such that for each
    position i in the run:
      - if the token is anchored at the active tier (tier-1
        chic-v2 anchor or tier-2 chic-v6 specific-phoneme override),
        the token's literal first-phoneme equals
        `scholarly_first_phoneme[i]`  (exact-phoneme match);
      - if the token is a class-placeholder (tier-3 or tier-4
        class proposal), the token's phoneme class equals
        `classify_value(scholarly_first_phoneme[i])` (class-level
        match);
      - otherwise (token is unanchored at the active tier), the
        position cannot match.
    All k positions must successfully match.

  Source B — toponym substring
    For every toponym surface in `pools/toponym.yaml`, generate the
    set of contiguous substrings of length L ∈ [3, 5]. A substring s
    of length L matches a CHIC inscription iff there exists a window
    of L contiguous phoneme slots in a single DIV-bounded phoneme
    stream of the inscription such that for each i ∈ [0, L):
      - if slot i is a literal char, slot i == s[i];
      - if slot i is a class-onset (placeholder consonant slot),
        s[i] is in the consonant set of that class;
      - if slot i is a class-vowel (placeholder vowel slot), s[i]
        is a vowel (a/e/i/o/u).
    Substring length 1–2 is excluded as a noise-floor convention
    (random 2-letter hits would dominate); substring length >5 is
    excluded because no chic-v6 inscription has a contiguous
    DIV-bounded phoneme stream that long after applying the four-tier
    extensions, so the bound has no operational effect.

  Source C — item-location consistency
    Per-inscription site metadata (`site` field in
    `corpora/cretan_hieroglyphic/all.jsonl`). For each inscription,
    take its site name lowercased; generate substrings of length
    3–5 from the surface; apply the source-B match procedure but
    against ONLY the inscription's own phoneme stream and ONLY
    against substrings of its own site name.

Class → consonant set
=====================
  vowel     a e i o u
  stop      p b t d k g q
  nasal     m n
  liquid    l r
  fricative s f h x z
  glide     j w y

Tier-2 phoneme overrides (per chic-v6 brief)
============================================
The chic-v5 leaderboard tiers #001, #012, #032 as tier-2 candidates
with proposed classes (glide, glide, stop). The brief specifies
specific-phoneme values from the L3 substrate-consistency analysis:
  #001 → `wa` (glide)
  #012 → `wa` (glide)
  #032 → `ki` (stop)
These are the chic-v5-best values within the proposed class for each
sign (top of `results/chic_substrate_consistency.md` per-sign top-K
table). These overrides apply ONLY at tier-2 and above; tier-1
extensions retain only the chic-v2 anchor pool.

Tier-3 / tier-4 class placeholders
==================================
Tier-3 (29 signs) and tier-4 (17 signs) classifications are read
mechanically from `results/chic_value_extraction_leaderboard.md`
(chic-v5; mg-7c6d). Each such sign is rendered in the extended
reading as `[CLASS:#NNN]` (or `[?:CLASS:#NNN]` when uncertain).
For phoneme-stream / substring matching, a class-placeholder
represents 2 phoneme slots (consonant + vowel) for non-vowel classes
and 1 slot (vowel) for the `vowel` class.

Determinism
===========
- No RNG. Same (CHIC corpus, anchor pool, leaderboard markdown,
  scholar entries, toponym pool) → byte-identical artifacts.
- Output ordering is deterministic (sorted by inscription id, tier
  level, source, etc.).

Inputs
======
  corpora/cretan_hieroglyphic/all.jsonl                    chic-v0
  pools/cretan_hieroglyphic_anchors.yaml                   chic-v2
  results/chic_value_extraction_leaderboard.md             chic-v5
  corpora/scholar_proposed_readings/all.jsonl              v22
  pools/toponym.yaml                                       v18

Outputs
=======
  results/chic_extended_partial_readings.md
  results/chic_verification_match_rates.md
  results/experiments.chic_verification_v0.jsonl

Usage
=====
  python3 scripts/build_chic_v6.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from scripts.build_chic_signs import classify_sign  # type: ignore  # noqa: E402

CHIC_CORPUS = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"
LEADERBOARD_MD = ROOT / "results" / "chic_value_extraction_leaderboard.md"
SCHOLAR_JSONL = ROOT / "corpora" / "scholar_proposed_readings" / "all.jsonl"
TOPONYM_YAML = ROOT / "pools" / "toponym.yaml"

EXTENDED_MD = ROOT / "results" / "chic_extended_partial_readings.md"
MATCH_RATES_MD = ROOT / "results" / "chic_verification_match_rates.md"
EXPERIMENTS_JSONL = ROOT / "results" / "experiments.chic_verification_v0.jsonl"

FETCHED_AT = "2026-05-05T17:00:00Z"
RUN_ID = "chic_verification_v0"
EXPERIMENT_ID = "mg-a557"

# Tier-2 specific phoneme overrides per chic-v6 brief.
TIER2_OVERRIDES: dict[str, str] = {
    "#001": "wa",
    "#012": "wa",
    "#032": "ki",
}

PHONEME_CLASSES: dict[str, str] = {
    "a": "vowel", "e": "vowel", "i": "vowel", "o": "vowel", "u": "vowel",
    "p": "stop", "b": "stop", "t": "stop", "d": "stop",
    "k": "stop", "g": "stop", "q": "stop",
    "m": "nasal", "n": "nasal",
    "l": "liquid", "r": "liquid",
    "s": "fricative", "f": "fricative", "h": "fricative",
    "x": "fricative", "z": "fricative",
    "j": "glide", "w": "glide", "y": "glide",
}
CLASS_TO_CHARS: dict[str, set[str]] = {
    "vowel": set("aeiou"),
    "stop": set("pbtdkgq"),
    "nasal": set("mn"),
    "liquid": set("lr"),
    "fricative": set("sfhxz"),
    "glide": set("jwy"),
}
VOWEL_CHARS: set[str] = CLASS_TO_CHARS["vowel"]

SUBSTR_MIN_LEN = 3
SUBSTR_MAX_LEN = 5

TIER_LEVELS = ("tier-1", "tier-2", "tier-3", "tier-4")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def classify_value(value: str) -> str | None:
    if not value:
        return None
    return PHONEME_CLASSES.get(value[0].lower())


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_anchors() -> dict[str, dict]:
    data = load_yaml(ANCHORS_YAML)
    return {a["chic_sign"]: a for a in data["anchors"]}


def load_leaderboard_tiers() -> dict[str, dict[str, str | None]]:
    """Parse `chic_value_extraction_leaderboard.md` for the per-sign tier
    verdict table.

    The table header is:
      | sign | freq | tier | proposed | L1 ... | L2 ... | L3 ... | L4 ... |

    Returns sign_id → {"tier": "tier-N" | "—", "class": str | None}.
    """
    text = LEADERBOARD_MD.read_text(encoding="utf-8")
    tier_map: dict[str, dict[str, str | None]] = {}
    lines = text.splitlines()
    in_verdict = False
    for line in lines:
        # Match the header that starts the per-sign verdict table.
        if line.startswith("| sign | freq | tier "):
            in_verdict = True
            continue
        if not in_verdict:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            in_verdict = False
            continue
        # Cell parse.
        # Strip leading/trailing pipes, split on |, strip whitespace.
        inner = line.strip()
        if inner.startswith("|"):
            inner = inner[1:]
        if inner.endswith("|"):
            inner = inner[:-1]
        cells = [c.strip() for c in inner.split("|")]
        # Sign cell is wrapped in backticks: e.g. `#001`.
        sign_cell = cells[0]
        if not (sign_cell.startswith("`#") and sign_cell.endswith("`")):
            # Not a sign row.
            continue
        sign = sign_cell.strip("`")
        tier = cells[2]
        proposed = cells[3]
        proposed_class = None if proposed in ("—", "-", "") else proposed
        tier_map[sign] = {"tier": tier, "class": proposed_class}
    return tier_map


def load_scholar() -> list[dict]:
    return load_jsonl(SCHOLAR_JSONL)


def load_toponyms() -> list[tuple[str, str]]:
    """Return list of (surface, gloss) tuples, lowercased."""
    data = load_yaml(TOPONYM_YAML)
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for e in data.get("entries", []):
        s = (e.get("surface") or "").strip().lower()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append((s, e.get("gloss") or ""))
    return sorted(out)


def normalize_token(tok: str) -> tuple[str, str | None]:
    if tok == "DIV":
        return "div", None
    if tok == "[?]":
        return "illegible", None
    if tok.startswith("[?:#") and tok.endswith("]"):
        return "sign_uncertain", tok[3:-1]
    if tok.startswith("#"):
        return "sign_clean", tok
    return "other", None


# ---------------------------------------------------------------------------
# Per-tier sign maps
# ---------------------------------------------------------------------------


def build_sign_state_for_tier(
    tier_level: str,
    anchors: dict[str, dict],
    leaderboard: dict[str, dict[str, str | None]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Return (literal_map, class_map) for the tier level.

    literal_map: sign → phoneme value (e.g. "ro"). Anchored with a
    specific phoneme value at this tier.
    class_map:   sign → class label (e.g. "stop"). Class-only
    placeholder at this tier.

    The two maps are disjoint by construction: a sign that is in
    literal_map is excluded from class_map, even if it had a tier-N
    proposal at a higher tier.
    """
    literal: dict[str, str] = {
        sid: a["linear_b_carryover_phonetic"] for sid, a in anchors.items()
    }
    cls: dict[str, str] = {}

    if tier_level == "tier-1":
        return literal, cls

    # tier-2 adds specific-phoneme overrides for #001, #012, #032.
    for sid, val in TIER2_OVERRIDES.items():
        literal[sid] = val
    if tier_level == "tier-2":
        return literal, cls

    # tier-3 adds 29 class placeholders.
    for sid, rec in leaderboard.items():
        if rec["tier"] == "tier-3" and rec["class"] and sid not in literal:
            cls[sid] = rec["class"]
    if tier_level == "tier-3":
        return literal, cls

    # tier-4 adds 17 more class placeholders.
    for sid, rec in leaderboard.items():
        if rec["tier"] == "tier-4" and rec["class"] and sid not in literal:
            cls[sid] = rec["class"]
    return literal, cls


# ---------------------------------------------------------------------------
# Extended partial reading rendering + slot/event extraction
# ---------------------------------------------------------------------------


def render_token(
    tok: str,
    literal: dict[str, str],
    cls: dict[str, str],
) -> tuple[str, dict | None]:
    """Render a single token under the tier maps.

    Returns (rendered_string, event_dict or None).

    event_dict, when present, describes the syllabographic event:
        kind:        'literal' or 'class' or 'unanchored'
        sign:        '#NNN'
        certain:     bool
        value:       str | None  (literal phoneme value if literal)
        class_label: str | None  (class label if class)
    None is returned for non-syllabographic tokens (DIV, illegible,
    ideogram, num, ambiguous).
    """
    kind, sid = normalize_token(tok)
    if kind == "div":
        return "/", None
    if kind == "illegible":
        return "[?]", None
    if kind in ("sign_clean", "sign_uncertain"):
        assert sid is not None
        sign_class, _note = classify_sign(sid)
        certain = kind == "sign_clean"
        if sign_class == "syllabographic":
            if sid in literal:
                val = literal[sid]
                rendered = val if certain else f"[?:{val}]"
                evt = {
                    "kind": "literal",
                    "sign": sid,
                    "certain": certain,
                    "value": val,
                    "class_label": classify_value(val),
                }
                return rendered, evt
            if sid in cls:
                lab = cls[sid].upper()
                rendered = f"[{lab}:{sid}]" if certain else f"[?:{lab}:{sid}]"
                evt = {
                    "kind": "class",
                    "sign": sid,
                    "certain": certain,
                    "value": None,
                    "class_label": cls[sid],
                }
                return rendered, evt
            # Unanchored at this tier: stream-break.
            rendered = sid if certain else f"[?:{sid}]"
            evt = {
                "kind": "unanchored",
                "sign": sid,
                "certain": certain,
                "value": None,
                "class_label": None,
            }
            return rendered, evt
        if sign_class == "ideogram":
            rendered = f"IDEO:{sid}" if certain else f"[?:IDEO:{sid}]"
            return rendered, None
        # ambiguous: pass through verbatim.
        rendered = sid if certain else f"[?:{sid}]"
        return rendered, None
    # other (NUM:..., raw ideogram name, etc.): preserve verbatim.
    return tok, None


def render_inscription(
    tokens: list[str],
    literal: dict[str, str],
    cls: dict[str, str],
) -> tuple[list[str], list[dict | None]]:
    """Render every token; return (rendered_strings, events).

    events[i] is None for non-syllabographic tokens (DIV, illegible,
    ideogram, num, ambiguous), and an event dict for syllabographic
    tokens.

    Stream-segmentation note: syllabographic events are *positions* in
    the rendered token list. DIV / illegible / ideogram / num / unanchored
    syllabographic tokens act as stream breaks for source-A token-run
    matching and for source-B/C phoneme-slot construction. Unanchored
    tokens are syllabographic but contribute no class info under the
    active tier, so they break the stream.
    """
    rendered: list[str] = []
    events: list[dict | None] = []
    for tok in tokens:
        r, e = render_token(tok, literal, cls)
        rendered.append(r)
        events.append(e)
    return rendered, events


def split_segments(events: list[dict | None]) -> list[list[tuple[int, dict]]]:
    """Split events into DIV-bounded segments of syllabographic events.

    A segment is a maximal contiguous run of (kind ∈ {literal, class}).
    Unanchored syllabographic events break the segment, as do DIV /
    illegible / ideogram / num tokens.

    Returns a list of segments; each segment is a list of (index_in_events, event_dict).
    """
    segs: list[list[tuple[int, dict]]] = []
    cur: list[tuple[int, dict]] = []
    for i, e in enumerate(events):
        if e is None:
            if cur:
                segs.append(cur)
                cur = []
            continue
        if e["kind"] == "unanchored":
            if cur:
                segs.append(cur)
                cur = []
            continue
        cur.append((i, e))
    if cur:
        segs.append(cur)
    return segs


# ---------------------------------------------------------------------------
# Phoneme slot stream construction (for source B / C substring matching)
# ---------------------------------------------------------------------------


def event_to_slots(evt: dict) -> list[dict]:
    """Translate one syllabographic event into one or more phoneme slots.

    Each slot is one of:
      {"type": "literal", "char": "r"}
      {"type": "class_onset", "class": "stop"}
      {"type": "vowel"}
    A literal CV value contributes 2 literal slots ("r","o" → 2 slots).
    A literal vowel value (one char in {a,e,i,o,u}) contributes 1
    literal slot.
    A class placeholder with class != 'vowel' contributes a class_onset
    slot followed by a vowel slot.
    A class placeholder with class == 'vowel' contributes a single
    vowel slot.
    """
    out: list[dict] = []
    if evt["kind"] == "literal":
        val = evt["value"] or ""
        for ch in val:
            out.append({"type": "literal", "char": ch})
        return out
    if evt["kind"] == "class":
        lab = evt["class_label"]
        if lab == "vowel":
            out.append({"type": "vowel"})
        else:
            out.append({"type": "class_onset", "class": lab})
            out.append({"type": "vowel"})
        return out
    # Unanchored should not be passed; return [].
    return out


def slots_for_segment(segment: list[tuple[int, dict]]) -> list[dict]:
    out: list[dict] = []
    for _idx, evt in segment:
        out.extend(event_to_slots(evt))
    return out


# ---------------------------------------------------------------------------
# Substring matching machinery
# ---------------------------------------------------------------------------


def slot_matches_char(slot: dict, target: str) -> bool:
    target = target.lower()
    if slot["type"] == "literal":
        return slot["char"] == target
    if slot["type"] == "class_onset":
        return target in CLASS_TO_CHARS.get(slot["class"], set())
    if slot["type"] == "vowel":
        return target in VOWEL_CHARS
    return False


def find_substring_matches(
    slot_streams: list[list[dict]],
    needle: str,
) -> list[tuple[int, int]]:
    """Return list of (segment_index, start_offset) matches of `needle`.

    Only literal-char inputs in `needle` are accepted (lowercased
    a–z); other chars produce no match.
    """
    needle = needle.lower()
    if not needle or any(ch not in (set("abcdefghijklmnopqrstuvwxyz")) for ch in needle):
        return []
    L = len(needle)
    matches: list[tuple[int, int]] = []
    for si, stream in enumerate(slot_streams):
        if len(stream) < L:
            continue
        for off in range(0, len(stream) - L + 1):
            ok = True
            for k in range(L):
                if not slot_matches_char(stream[off + k], needle[k]):
                    ok = False
                    break
            if ok:
                matches.append((si, off))
    return matches


def all_substrings(surface: str, lo: int, hi: int) -> list[str]:
    surface = surface.lower()
    out: set[str] = set()
    for L in range(lo, hi + 1):
        if L > len(surface):
            break
        for i in range(0, len(surface) - L + 1):
            out.add(surface[i : i + L])
    return sorted(out)


# ---------------------------------------------------------------------------
# Source-A: token-run match against scholar AB-sequence
# ---------------------------------------------------------------------------


def find_source_a_matches(
    segments: list[list[tuple[int, dict]]],
    scholar_phonemes: list[str],
) -> list[dict]:
    """Walk each segment and return matches for the scholar phoneme sequence.

    Returns list of {"segment_index": ..., "offset_in_segment": ...,
    "events": [ ... ]}.
    """
    out: list[dict] = []
    k = len(scholar_phonemes)
    if k == 0:
        return out
    for si, seg in enumerate(segments):
        if len(seg) < k:
            continue
        for off in range(0, len(seg) - k + 1):
            ok = True
            for i in range(k):
                evt = seg[off + i][1]
                target_first = scholar_phonemes[i][0].lower() if scholar_phonemes[i] else None
                if target_first is None:
                    ok = False
                    break
                if evt["kind"] == "literal":
                    val = (evt["value"] or "").lower()
                    if not val or val[0] != target_first:
                        ok = False
                        break
                elif evt["kind"] == "class":
                    target_class = PHONEME_CLASSES.get(target_first)
                    if target_class != evt["class_label"]:
                        ok = False
                        break
                else:
                    ok = False
                    break
            if ok:
                out.append({
                    "segment_index": si,
                    "offset_in_segment": off,
                    "events": [seg[off + i][1] for i in range(k)],
                })
    return out


# ---------------------------------------------------------------------------
# Per-tier verification pass
# ---------------------------------------------------------------------------


def per_inscription_pass(
    record: dict,
    literal: dict[str, str],
    cls: dict[str, str],
    scholar_entries: list[dict],
    toponym_surfaces: list[tuple[str, str]],
) -> dict:
    """Run all three sources for a single inscription at one tier level."""
    tokens = record["tokens"]
    rendered, events = render_inscription(tokens, literal, cls)
    segments = split_segments(events)
    slot_streams = [slots_for_segment(seg) for seg in segments]

    # --- Source A: scholar-proposed reading hits.
    a_hits: list[dict] = []
    for entry in scholar_entries:
        phonemes = entry.get("scholarly_first_phoneme") or []
        if not phonemes:
            continue
        matches = find_source_a_matches(segments, phonemes)
        for m in matches:
            a_hits.append({
                "scholar_entry_id": entry["entry_id"],
                "ab_sequence": entry["ab_sequence"],
                "scholarly_phonemes": entry["scholarly_phonemes"],
                "scholarly_first_phoneme": entry["scholarly_first_phoneme"],
                "category": entry.get("category", ""),
                "segment_index": m["segment_index"],
                "offset_in_segment": m["offset_in_segment"],
                "matched_signs": [evt["sign"] for evt in m["events"]],
                "matched_kinds": [evt["kind"] for evt in m["events"]],
            })

    # --- Source B: toponym substring hits.
    b_hits: list[dict] = []
    seen_b: set[tuple[str, str]] = set()
    for surface, gloss in toponym_surfaces:
        for sub in all_substrings(surface, SUBSTR_MIN_LEN, SUBSTR_MAX_LEN):
            ms = find_substring_matches(slot_streams, sub)
            if ms and (surface, sub) not in seen_b:
                seen_b.add((surface, sub))
                first = ms[0]
                b_hits.append({
                    "toponym": surface,
                    "gloss": gloss,
                    "substring": sub,
                    "n_match_positions": len(ms),
                    "first_segment_index": first[0],
                    "first_offset": first[1],
                })

    # --- Source C: own-site substring hits.
    site = (record.get("site") or "").strip().lower()
    site_norm = "".join(ch for ch in site if ch.isalpha())
    c_hits: list[dict] = []
    if site_norm and len(site_norm) >= SUBSTR_MIN_LEN:
        for sub in all_substrings(site_norm, SUBSTR_MIN_LEN, SUBSTR_MAX_LEN):
            ms = find_substring_matches(slot_streams, sub)
            if ms:
                first = ms[0]
                c_hits.append({
                    "site": record.get("site") or "",
                    "site_normalized": site_norm,
                    "substring": sub,
                    "n_match_positions": len(ms),
                    "first_segment_index": first[0],
                    "first_offset": first[1],
                })

    # Per-position counts for the rollup.
    n_syll = sum(1 for e in events if e is not None and e["kind"] in ("literal", "class", "unanchored"))
    n_anchored_literal = sum(1 for e in events if e is not None and e["kind"] == "literal")
    n_class_placeholder = sum(1 for e in events if e is not None and e["kind"] == "class")
    n_unanchored = sum(1 for e in events if e is not None and e["kind"] == "unanchored")
    coverage = ((n_anchored_literal + n_class_placeholder) / n_syll) if n_syll > 0 else 0.0

    return {
        "id": record["id"],
        "site": record.get("site") or "",
        "support": record.get("support") or "",
        "n_syllabographic": n_syll,
        "n_anchored_literal": n_anchored_literal,
        "n_class_placeholder": n_class_placeholder,
        "n_unanchored": n_unanchored,
        "extended_coverage_rate": round(coverage, 4),
        "extended_partial_reading": " ".join(rendered),
        "rendered_tokens": rendered,
        "source_a_hits": a_hits,
        "source_b_hits": b_hits,
        "source_c_hits": c_hits,
        "n_a_hits": len(a_hits),
        "n_b_hits": len(b_hits),
        "n_c_hits": len(c_hits),
    }


def run_tier(
    tier_level: str,
    records: list[dict],
    anchors: dict[str, dict],
    leaderboard: dict[str, dict[str, str | None]],
    scholar_entries: list[dict],
    toponym_surfaces: list[tuple[str, str]],
) -> list[dict]:
    literal, cls = build_sign_state_for_tier(tier_level, anchors, leaderboard)
    out: list[dict] = []
    for rec in records:
        row = per_inscription_pass(
            rec, literal, cls, scholar_entries, toponym_surfaces,
        )
        row["tier_level"] = tier_level
        row["n_anchored_signs"] = len(literal)
        row["n_class_signs"] = len(cls)
        out.append(row)
    return out


# ---------------------------------------------------------------------------
# Aggregate roll-ups
# ---------------------------------------------------------------------------


def tier_rollup(rows: list[dict]) -> dict:
    n_inscriptions = len(rows)
    n_with_any_a = sum(1 for r in rows if r["n_a_hits"] > 0)
    n_with_any_b = sum(1 for r in rows if r["n_b_hits"] > 0)
    n_with_any_c = sum(1 for r in rows if r["n_c_hits"] > 0)
    n_with_any = sum(
        1 for r in rows
        if r["n_a_hits"] > 0 or r["n_b_hits"] > 0 or r["n_c_hits"] > 0
    )
    total_a = sum(r["n_a_hits"] for r in rows)
    total_b = sum(r["n_b_hits"] for r in rows)
    total_c = sum(r["n_c_hits"] for r in rows)
    return {
        "n_inscriptions": n_inscriptions,
        "n_inscriptions_with_any_match": n_with_any,
        "match_rate_any": round(n_with_any / n_inscriptions, 4) if n_inscriptions else 0.0,
        "n_inscriptions_with_a": n_with_any_a,
        "n_inscriptions_with_b": n_with_any_b,
        "n_inscriptions_with_c": n_with_any_c,
        "total_a_hits": total_a,
        "total_b_hits": total_b,
        "total_c_hits": total_c,
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def write_extended_partial_readings(
    per_tier: dict[str, list[dict]],
) -> None:
    rows_t1 = sorted(per_tier["tier-1"], key=lambda r: r["id"])
    n_inscriptions = len(rows_t1)
    lines: list[str] = []
    a = lines.append
    a("# CHIC extended partial readings under chic-v6 tier extensions (mg-a557)")
    a("")
    a(
        "Extended partial readings of every CHIC inscription in "
        "`corpora/cretan_hieroglyphic/all.jsonl`, rendered at four "
        "tier levels of sign-value extension. Built by "
        "`scripts/build_chic_v6.py`."
    )
    a("")
    a("## Tier levels")
    a("")
    a("- **tier-1** — chic-v2 paleographic-anchor pool only "
      "(20 anchors; same as `results/chic_partial_readings.md`).")
    a("- **tier-2** — tier-1 ∪ chic-v5 tier-2 candidates with chic-v6 "
      "specific-phoneme overrides "
      "(`#001 → wa`, `#012 → wa`, `#032 → ki`).")
    a("- **tier-3** — tier-2 ∪ chic-v5 tier-3 candidates as "
      "class-level placeholders "
      "(`[STOP:#NNN]`, `[GLIDE:#NNN]`, …); 29 added signs.")
    a("- **tier-4** — tier-3 ∪ chic-v5 tier-4 candidates as "
      "class-level placeholders; 17 more added signs.")
    a("")
    a("## Rendering convention")
    a("")
    a("- Anchored clean: emit phonetic value (e.g. `ra`).")
    a("- Anchored uncertain: emit `[?:value]`.")
    a("- Class-placeholder clean: emit `[CLASS:#NNN]` "
      "(e.g. `[STOP:#005]`).")
    a("- Class-placeholder uncertain: emit `[?:CLASS:#NNN]`.")
    a("- Unanchored clean: emit `#NNN`.")
    a("- Unanchored uncertain: emit `[?:#NNN]`.")
    a("- DIV: emit `/`.")
    a("- Illegible: emit `[?]`.")
    a("- Ideogram: emit `IDEO:#NNN`.")
    a("")
    a("## Per-tier coverage rollup")
    a("")
    a("Coverage = (anchored literal positions + class-placeholder positions) / total syllabographic positions, per chic-v1 sign classification. Per-inscription numerator-denominator detail is in `results/experiments.chic_verification_v0.jsonl`.")
    a("")
    a("| tier | n anchored signs (literal) | n class-placeholder signs | n inscriptions w/ ≥1 syllabographic | mean extended coverage |")
    a("|---|---:|---:|---:|---:|")
    for tier in TIER_LEVELS:
        rows = per_tier[tier]
        n_signs_lit = rows[0]["n_anchored_signs"] if rows else 0
        n_signs_cls = rows[0]["n_class_signs"] if rows else 0
        elig = [r for r in rows if r["n_syllabographic"] > 0]
        n_elig = len(elig)
        mean_cov = (sum(r["extended_coverage_rate"] for r in elig) / n_elig) if n_elig else 0.0
        a(f"| {tier} | {n_signs_lit} | {n_signs_cls} | {n_elig} | "
          f"{mean_cov:.4f} |")
    a("")
    a("## Per-inscription extended readings")
    a("")
    a("Per-inscription readings are tabulated below. For each inscription, "
      "the four tier-level readings are listed in successive rows.")
    a("")
    a("| CHIC id | Site | Support | tier | n_syll | n_lit | n_cls | n_unanch | coverage | partial reading |")
    a("|---|---|---|---|--:|--:|--:|--:|--:|---|")
    by_id: dict[str, dict[str, dict]] = defaultdict(dict)
    for tier in TIER_LEVELS:
        for r in per_tier[tier]:
            by_id[r["id"]][tier] = r
    for cid in sorted(by_id.keys()):
        for tier in TIER_LEVELS:
            r = by_id[cid][tier]
            a(f"| {r['id']} | {r['site']} | {r['support']} | {tier} | "
              f"{r['n_syllabographic']} | {r['n_anchored_literal']} | "
              f"{r['n_class_placeholder']} | {r['n_unanchored']} | "
              f"{r['extended_coverage_rate']:.4f} | "
              f"`{r['extended_partial_reading']}` |")
    a("")
    a("## Citations")
    a("")
    a("- Olivier, J.-P. & Godart, L. (1996). _CHIC._")
    a("- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._")
    a("- Salgarella, E. (2020). _Aegean Linear Script(s)._")
    a("- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._")
    a("")
    EXTENDED_MD.write_text("\n".join(lines), encoding="utf-8")


def write_match_rates(
    per_tier: dict[str, list[dict]],
    n_scholar_entries: int,
    n_toponym_surfaces: int,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v6 verification match rates (mg-a557)")
    a("")
    a("Mechanical verification-rate report for chic-v5 candidate "
      "proposals, per the chic-v6 brief. Built by "
      "`scripts/build_chic_v6.py`. Discipline note: this is a "
      "verification-rate report against three external-scholarship "
      "sources, NOT a decipherment claim. Specialist judgment is "
      "still required to advance any matched candidate from "
      "`matched` to `decipherment`.")
    a("")
    a("## Pre-registered match criteria")
    a("")
    a("Match criteria fixed BEFORE computing match counts (per the "
      "chic-v6 brief, to prevent post-hoc relaxation). They are "
      "preserved verbatim in the `scripts/build_chic_v6.py` "
      "module-level docstring; the abbreviated form below mirrors "
      "the script.")
    a("")
    a("- **Source A — scholar-proposed Linear-A reading match.** "
      "A scholar entry's `ab_sequence` (length k) matches a CHIC "
      "inscription iff there exists a contiguous run of k "
      "syllabographic-class tokens within a single DIV-bounded segment "
      "of the inscription such that for each position i: (a) the "
      "token is a tier-1/2 anchored sign whose literal first-phoneme "
      "equals the scholar's `scholarly_first_phoneme[i]`, OR (b) "
      "the token is a tier-3/4 class placeholder whose class equals "
      "`classify_value(scholarly_first_phoneme[i])`. All k positions "
      "must match.")
    a("- **Source B — toponym substring match.** For every toponym "
      "surface in `pools/toponym.yaml`, generate substrings of "
      f"length L ∈ [{SUBSTR_MIN_LEN}, {SUBSTR_MAX_LEN}]. Match in a "
      "single DIV-bounded phoneme stream, char-by-char: literal char "
      "matches by string equality; class-onset slot matches if the "
      "target char is in that class's consonant set; vowel slot "
      "matches if the target char is a vowel.")
    a("- **Source C — item-location consistency.** Per-inscription "
      "`site` field, lowercased (alphabetical chars only). Generate "
      "substrings of length 3–5 from the site surface; apply the "
      "source-B match procedure but only against the inscription's "
      "own phoneme stream and only against substrings of its own "
      "site name.")
    a("")
    a("## Class → consonant set")
    a("")
    a("| class | consonants |")
    a("|---|---|")
    for cls in ("vowel", "stop", "nasal", "liquid", "fricative", "glide"):
        chars = "".join(sorted(CLASS_TO_CHARS[cls]))
        a(f"| {cls} | `{chars}` |")
    a("")
    a("## Per-tier match-rate table")
    a("")
    a(f"Inputs: {len(per_tier['tier-1'])} CHIC inscriptions; "
      f"{n_scholar_entries} scholar-proposed entries; "
      f"{n_toponym_surfaces} toponym surfaces.")
    a("")
    a("| tier | n_inscriptions | n_with_any_match | match_rate_any | n_with_a | n_with_b | n_with_c | total_a | total_b | total_c |")
    a("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    rollups: dict[str, dict] = {}
    for tier in TIER_LEVELS:
        ru = tier_rollup(per_tier[tier])
        rollups[tier] = ru
        a(f"| {tier} | {ru['n_inscriptions']} | "
          f"{ru['n_inscriptions_with_any_match']} | "
          f"{ru['match_rate_any']:.4f} | "
          f"{ru['n_inscriptions_with_a']} | "
          f"{ru['n_inscriptions_with_b']} | "
          f"{ru['n_inscriptions_with_c']} | "
          f"{ru['total_a_hits']} | "
          f"{ru['total_b_hits']} | "
          f"{ru['total_c_hits']} |")
    a("")
    a("## Tier-over-tier verification lift")
    a("")
    a(
        "The `lift` from tier-(N-1) to tier-N is the difference in "
        "`n_inscriptions_with_any_match`. A positive lift means the "
        "tier-N extension produced verification matches not "
        "attainable under tier-(N-1)."
    )
    a("")
    a("| from | to | lift (n_inscriptions_with_any_match) | lift (total a+b+c hits) |")
    a("|---|---|--:|--:|")
    pairs = [("tier-1", "tier-2"), ("tier-2", "tier-3"), ("tier-3", "tier-4")]
    for src, dst in pairs:
        d_n = rollups[dst]["n_inscriptions_with_any_match"] - rollups[src]["n_inscriptions_with_any_match"]
        d_h = (
            rollups[dst]["total_a_hits"] + rollups[dst]["total_b_hits"] + rollups[dst]["total_c_hits"]
        ) - (
            rollups[src]["total_a_hits"] + rollups[src]["total_b_hits"] + rollups[src]["total_c_hits"]
        )
        a(f"| {src} | {dst} | {d_n:+d} | {d_h:+d} |")
    a("")
    a("## Per-match enumeration (tier-4, the maximally extended tier)")
    a("")
    a(
        "For each verified match at tier-4 (the strict superset of "
        "all earlier tiers), the inscription, source, matched signs, "
        "and matched substring/scholar reading are listed. This "
        "enumeration provides the concrete list of "
        "candidate-with-external-verification cases; specialist "
        "judgment is still required to elevate any of these from "
        "matched to decipherment."
    )
    a("")
    a("### Source A enumeration (scholar-proposed reading hits)")
    a("")
    rows_t4 = per_tier["tier-4"]
    a_count = 0
    a_rows = []
    for r in sorted(rows_t4, key=lambda x: x["id"]):
        for h in r["source_a_hits"]:
            a_count += 1
            a_rows.append((r, h))
    if not a_rows:
        a("**No source-A matches at tier-4.** Scholar-proposed "
          "Linear-A readings (`ku-ro`, `ki-ro`, `ja-sa-sa-ra-me`, "
          "etc.) do not appear as token-run patterns in any CHIC "
          "inscription's extended reading at any tier level. This is "
          "consistent with chic-v0's framing that CHIC and Linear A "
          "share only ~20 paleographic-anchor signs out of ~80 "
          "syllabographic CHIC signs, so the canonical Linear-A "
          "scholar lexicon (built almost exclusively from the AB "
          "inventory) does not transfer mechanically to CHIC.")
    else:
        a("| CHIC id | Site | Tier-4 reading (excerpt) | Scholar entry | "
          "Phonemes | AB-sequence | Matched CHIC signs | Match modes |")
        a("|---|---|---|---|---|---|---|---|")
        for r, h in a_rows:
            phonemes = " ".join(h["scholarly_phonemes"])
            ab = " ".join(h["ab_sequence"])
            signs = " ".join(h["matched_signs"])
            modes = "/".join(h["matched_kinds"])
            excerpt = r["extended_partial_reading"]
            if len(excerpt) > 80:
                excerpt = excerpt[:77] + "..."
            a(f"| {r['id']} | {r['site']} | `{excerpt}` | "
              f"{h['scholar_entry_id']} | `{phonemes}` | `{ab}` | "
              f"`{signs}` | {modes} |")
    a("")
    a("### Source B enumeration (toponym substring hits, tier-4)")
    a("")
    b_rows: list[tuple[dict, dict]] = []
    for r in sorted(rows_t4, key=lambda x: x["id"]):
        for h in r["source_b_hits"]:
            b_rows.append((r, h))
    if not b_rows:
        a("**No source-B matches at tier-4.** No toponym substring "
          "of length 3–5 hits any CHIC extended reading.")
    else:
        a(f"Total source-B match cells (inscription × distinct "
          f"toponym × distinct substring): **{len(b_rows)}**.")
        a("")
        a("| CHIC id | Site | Toponym | Substring | n match positions |")
        a("|---|---|---|---|--:|")
        for r, h in b_rows:
            a(f"| {r['id']} | {r['site']} | {h['toponym']} | "
              f"`{h['substring']}` | {h['n_match_positions']} |")
    a("")
    a("### Source C enumeration (item-location consistency, tier-4)")
    a("")
    c_rows: list[tuple[dict, dict]] = []
    for r in sorted(rows_t4, key=lambda x: x["id"]):
        for h in r["source_c_hits"]:
            c_rows.append((r, h))
    if not c_rows:
        a("**No source-C matches at tier-4.** No CHIC inscription's "
          "extended reading contains any substring of length 3–5 "
          "drawn from its own find-spot's name.")
    else:
        a(f"Total source-C match cells: **{len(c_rows)}**.")
        a("")
        a("| CHIC id | Site | Substring of site | n match positions |")
        a("|---|---|---|--:|")
        for r, h in c_rows:
            a(f"| {r['id']} | {r['site']} | `{h['substring']}` | "
              f"{h['n_match_positions']} |")
    a("")
    a("## Discipline framing")
    a("")
    a(
        "Per the chic-v6 brief: this is a verification-rate report "
        "(mechanical match against external scholarship; NOT "
        "specialist judgment). The match criteria are pre-registered "
        "above to prevent post-hoc relaxation. Per-tier verification "
        "lift is the chic-v5 framework's verification-grade "
        "contribution: zero lift means the framework's per-sign "
        "extraction does not survive external verification (consistent "
        "with the v13 / v22 / v24 internal-vs-external pattern); "
        "positive lift is publishable as a reinforcement of the "
        "chic-v5 candidate-proposal framework. Either outcome is "
        "publishable."
    )
    a("")
    a("## Determinism")
    a("")
    a(
        "- No RNG. Same (CHIC corpus, anchor pool, leaderboard "
        "markdown, scholar entries, toponym pool) → byte-identical "
        "artifacts."
    )
    a("- All sortings are deterministic.")
    a("")
    a("## Citations")
    a("")
    a("- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._")
    a("- Younger, J. G. (online). _Linear A texts in phonetic transcription._")
    a("- Olivier, J.-P. & Godart, L. (1996). _CHIC._")
    a("- Beekes, R. S. P. (2010). _Etymological Dictionary of Greek._ (Pre-Greek substrate appendix.)")
    a("- Furnée, E. J. (1972). _Die wichtigsten konsonantischen Erscheinungen des Vorgriechischen._")
    a("- Salgarella, E. (2020). _Aegean Linear Script(s)._")
    a("- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._")
    a("")
    MATCH_RATES_MD.write_text("\n".join(lines), encoding="utf-8")


def write_experiments_jsonl(
    per_tier: dict[str, list[dict]],
) -> None:
    rows: list[dict] = []
    for tier in TIER_LEVELS:
        for r in per_tier[tier]:
            rows.append({
                "experiment_id": EXPERIMENT_ID,
                "run_id": RUN_ID,
                "tier_level": tier,
                "inscription_id": r["id"],
                "site": r["site"],
                "support": r["support"],
                "n_syllabographic": r["n_syllabographic"],
                "n_anchored_literal": r["n_anchored_literal"],
                "n_class_placeholder": r["n_class_placeholder"],
                "n_unanchored": r["n_unanchored"],
                "extended_coverage_rate": r["extended_coverage_rate"],
                "extended_partial_reading": r["extended_partial_reading"],
                "n_a_hits": r["n_a_hits"],
                "n_b_hits": r["n_b_hits"],
                "n_c_hits": r["n_c_hits"],
                "source_a_hits": r["source_a_hits"],
                "source_b_hits": r["source_b_hits"],
                "source_c_hits": r["source_c_hits"],
                "fetched_at": FETCHED_AT,
            })

    EXPERIMENTS_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with EXPERIMENTS_JSONL.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    records = load_jsonl(CHIC_CORPUS)
    anchors = load_anchors()
    leaderboard = load_leaderboard_tiers()
    scholar_entries = load_scholar()
    toponym_surfaces = load_toponyms()

    per_tier: dict[str, list[dict]] = {}
    for tier_level in TIER_LEVELS:
        per_tier[tier_level] = run_tier(
            tier_level,
            records,
            anchors,
            leaderboard,
            scholar_entries,
            toponym_surfaces,
        )

    write_extended_partial_readings(per_tier)
    write_match_rates(per_tier, len(scholar_entries), len(toponym_surfaces))
    write_experiments_jsonl(per_tier)

    # Console summary.
    print("chic-v6 verification pass complete (mg-a557)")
    print(f"  inscriptions:            {len(records)}")
    print(f"  scholar entries:         {len(scholar_entries)}")
    print(f"  toponym surfaces:        {len(toponym_surfaces)}")
    print(f"  tier-3 candidates:       "
          f"{sum(1 for r in leaderboard.values() if r['tier'] == 'tier-3' and r['class'])}")
    print(f"  tier-4 candidates:       "
          f"{sum(1 for r in leaderboard.values() if r['tier'] == 'tier-4' and r['class'])}")
    for tier in TIER_LEVELS:
        ru = tier_rollup(per_tier[tier])
        print(f"  [{tier}] match_rate_any={ru['match_rate_any']:.4f} "
              f"a={ru['total_a_hits']} b={ru['total_b_hits']} "
              f"c={ru['total_c_hits']}")


if __name__ == "__main__":
    main()
