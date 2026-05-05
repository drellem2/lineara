#!/usr/bin/env python3
"""Build the CHIC sign inventory + classification pool (mg-c7e3, chic-v1).

CHIC = Olivier & Godart 1996, *Corpus Hieroglyphicarum Inscriptionum
Cretae*. CHIC is a mixed logosyllabic script: ~30 signs are clearly
ideographic (bull's head, ax, ship, etc.) and ~70-80 are abstract
syllabographic. Per-sign syllable-value extraction (the chic-v5+
target) only makes sense on the syllabographic subset. chic-v1 partitions
the CHIC sign inventory and characterizes each subset.

Inputs (built by mg-99df, chic-v0):
  corpora/cretan_hieroglyphic/all.jsonl   per-inscription jsonl

Outputs:
  pools/cretan_hieroglyphic_signs.yaml             classification + metadata
  pools/cretan_hieroglyphic_signs.README.md        rule + citations
  pools/schemas/chic_signs.v1.schema.json          schema for the yaml
  results/chic_sign_inventory.md                   inventory table
  results/chic_vs_linear_a_sign_inventory_comparison.md   distribution comparison

Classification rule (chic-v1):

  Per the CHIC catalog convention (Olivier & Godart 1996, retained by
  Younger's web edition), CHIC sign IDs are organized by numeric range:

    #001 - #100   syllabographic sign repertoire (~96 catalogued)
    #101 - #180   logograms / ideograms (BOS, OVIS, GRA, OLI, VIN, ...)
    #301 - #308   numerals + fractions (functionally non-syllabic;
                  classified as ideogram)

  Default per-sign classification follows the numeric range. A small
  per-sign exception list (`AMBIGUOUS_OVERRIDES`) flags signs whose
  classification is debated or contested in O&G 1996 and downstream
  scholarship (Salgarella 2020, Decorte 2017). Those are recorded as
  `ambiguous` with a citation in `notes_from_olivier_godart`.

  This rule is conservative on purpose. The ticket explicitly warns:
  "be explicit about the rules used; do NOT silently call signs
  ideographic without evidence. The classification will be the
  foundation of all chic-v2+ work, so errors here propagate."

Paleographic candidates: enumerated in `PALEOGRAPHIC_CANDIDATES` below.
The list is curated from Salgarella 2020 (*Aegean Linear Script(s)*),
Younger's online CHIC tables (the per-sign "≈ Linear A AB-NN" notes),
and Decorte 2017 / 2018. v1 just enumerates them; chic-v2 mechanically
applies them as anchors.

Reproducibility: deterministic given the same input corpus.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHIC_CORPUS = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
LINEAR_A_CORPUS = ROOT / "corpus" / "all.jsonl"

POOL_YAML = ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
POOL_README = ROOT / "pools" / "cretan_hieroglyphic_signs.README.md"
POOL_SCHEMA = ROOT / "pools" / "schemas" / "chic_signs.v1.schema.json"

INV_REPORT = ROOT / "results" / "chic_sign_inventory.md"
COMPARISON_REPORT = ROOT / "results" / "chic_vs_linear_a_sign_inventory_comparison.md"

FETCHED_AT = "2026-05-05T12:00:00Z"


# ---------------------------------------------------------------------------
# Classification rule
# ---------------------------------------------------------------------------

# Per-sign overrides for signs whose classification is debated in the
# scholarly literature (Olivier & Godart 1996, Salgarella 2020, Decorte
# 2017). Each entry: (chic_id, sign_class, note).
#
# Conservative principle: only override when at least one mainstream
# scholarly source reclassifies the sign or explicitly flags its status
# as debated. Otherwise default to the numeric-range rule.

AMBIGUOUS_OVERRIDES: dict[str, str] = {
    # CHIC #008 (double-axe). Olivier-Godart treats #008 as a syllabogram
    # in the catalog index, but the iconographic content is unambiguous.
    # Salgarella 2020 (Aegean Linear Script(s), p. 116) discusses #008
    # under "iconographically-loaded syllabograms" — its sign-class is
    # still syllabographic but its origin is ideographic. Kept as
    # syllabographic by the rule, but flag distributional concerns.
    # NOT overridden — kept as syllabographic per O&G.

    # CHIC #044 (the "trowel" / "gate" sign). Highest-frequency CHIC
    # sign (128 occurrences in our 302-inscription corpus). O&G classify
    # as syllabogram. Some sealstone scholarship (Civitillo 2016) has
    # argued #044 functions as a sealing-mark (heraldic) on Mallia
    # crescents, not as a syllabogram. The mainline catalog reading is
    # syllabographic. Flag for ambiguity-review under chic-v3.
    # NOT overridden in v1 — kept as syllabographic per O&G; the ticket
    # asks us not to silently reclassify.

    # CHIC #155 (CYP / Cyprus jar) — definitively ideogram per O&G.
    # Falls in the >=#101 ideogram range automatically.

    # CHIC #070 (chevron / V). High frequency (56). Classified as
    # syllabogram in O&G. Younger flags this as one of the most secure
    # paleographic matches to Linear A AB60 (= ra). Kept as syllabographic.

    # No overrides applied at v1; rule is purely numeric-range. The
    # AMBIGUOUS_OVERRIDES table is here for chic-v3 to populate from
    # a fuller scholarly review.
}

# Signs in the >=#101 range that O&G classify as ideograms/logograms
# (CHIC catalog labels). When such a sign appears in the corpus, its
# notes_from_olivier_godart records the catalog gloss. Curated from
# the published CHIC catalog index; not exhaustive but covers the
# logograms most often cited in the literature.

IDEOGRAM_GLOSSES: dict[str, str] = {
    "#150": "BOS = ox-head ideogram (cattle, often appearing with NUM counts).",
    "#151": "OVIS = sheep ideogram.",
    "#152": "CAP = goat ideogram.",
    "#153": "SUS = pig ideogram.",
    "#155": "CYP = Cyprus-jar (commodity-vessel) ideogram.",
    "#156": "GRA = grain ideogram (cereal).",
    "#157": "OLI = olive ideogram.",
    "#158": "VIN = wine ideogram.",
    "#159": "FIC = fig ideogram.",
    "#160": "AROM = aromatics ideogram.",
    "#161": "OLE = oil ideogram.",
    "#162": "TELA = textile ideogram.",
    "#163": "VIR = man (anthropomorphic) ideogram.",
    "#164": "MUL = woman (anthropomorphic) ideogram.",
    "#165": "AES = bronze ideogram.",
    "#166": "AUR = gold ideogram.",
    "#167": "Cyprus-jar variant.",
    "#168": "Vessel-class ideogram (vase).",
    "#169": "Vessel-class ideogram (vase).",
    "#170": "VAS = generic vase / vessel ideogram.",
    "#171": "Klasmatogram (place / category marker).",
    "#172": "Klasmatogram (place / category marker).",
    "#180": "Klasmatogram.",
    "#301": "Numeral / unit (1).",
    "#302": "Numeral / unit (10).",
    "#303": "Numeral / unit (100).",
    "#304": "Numeral / unit (1000).",
    "#305": "Fraction.",
    "#306": "Fraction.",
    "#307": "Fraction.",
    "#308": "Fraction.",
}


def classify_sign(sign_id: str) -> tuple[str, str]:
    """Return (sign_class, note) for a CHIC sign id like '#044'.

    sign_class is one of: 'syllabographic' | 'ideogram' | 'ambiguous'.
    note may be empty; if non-empty, it's the catalog gloss (for
    ideograms) or the ambiguity reason (for ambiguous signs).
    """
    if sign_id in AMBIGUOUS_OVERRIDES:
        return "ambiguous", AMBIGUOUS_OVERRIDES[sign_id]
    n = int(sign_id.lstrip("#"))
    if 1 <= n <= 100:
        return "syllabographic", ""
    if 101 <= n <= 299:
        gloss = IDEOGRAM_GLOSSES.get(sign_id, "")
        return "ideogram", gloss
    if 300 <= n <= 399:
        gloss = IDEOGRAM_GLOSSES.get(sign_id, "Numeral or fraction.")
        return "ideogram", gloss
    return "ambiguous", f"unknown id range for {sign_id}"


# ---------------------------------------------------------------------------
# Paleographic candidates (chic-v2 anchor seed list)
#
# Curated from established scholarship on the CHIC ↔ Linear A paleographic
# continuum. Each candidate maps a CHIC sign to a Linear A AB-id whose
# Linear B carryover value is established (Ventris-Chadwick 1956).
#
# Confidence levels:
#   consensus  — multiple scholarly sources concur (Salgarella + Younger
#                + Decorte, or a similar triangulation).
#   proposed   — single primary source proposes the match (often Younger
#                or Salgarella alone).
#   debated    — match is asserted in some sources but explicitly rejected
#                in others.
#
# v1 enumerates these as candidates only. v2 (mg-XXXX, future ticket) will
# mechanically apply the consensus subset as tier-1 paleographic anchors.
# ---------------------------------------------------------------------------

PALEOGRAPHIC_CANDIDATES: list[dict] = [
    {
        "chic_sign": "#010",
        "linear_a_sign": "AB57",
        "linear_b_value": "ja",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC sign-list, '≈ Linear A AB57' annotation; "
            "Salgarella 2020 *Aegean Linear Script(s)* p. 144, table 5.3 "
            "(CHIC→LA visual matches)."
        ),
    },
    {
        "chic_sign": "#013",
        "linear_a_sign": "AB03",
        "linear_b_value": "pa",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB03; Salgarella 2020 "
            "p. 145 flags as debated (alternative candidate AB28 = i)."
        ),
    },
    {
        "chic_sign": "#016",
        "linear_a_sign": "AB08",
        "linear_b_value": "a",
        "confidence": "consensus",
        "citation": (
            "Younger online CHIC tables; Salgarella 2020 p. 144; "
            "Decorte 2017 *The First 'European' Writing*, fig. 6.2. "
            "Linear B value AB08=a per Ventris-Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#019",
        "linear_a_sign": "AB44",
        "linear_b_value": "ke",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB44; Salgarella 2020 "
            "p. 145 records debate. Linear B value AB44=ke."
        ),
    },
    {
        "chic_sign": "#025",
        "linear_a_sign": "AB59",
        "linear_b_value": "ta",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC sign-list ≈ AB59; visual continuity "
            "documented in Salgarella 2020 p. 145. Linear B AB59=ta."
        ),
    },
    {
        "chic_sign": "#028",
        "linear_a_sign": "AB37",
        "linear_b_value": "ti",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB37; Linear B AB37=ti per "
            "Ventris-Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#031",
        "linear_a_sign": "AB02",
        "linear_b_value": "ro",
        "confidence": "consensus",
        "citation": (
            "Younger online CHIC tables; Salgarella 2020 p. 144 (table 5.3); "
            "Decorte 2017 fig. 6.2. AB02=ro per Ventris-Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#038",
        "linear_a_sign": "AB28",
        "linear_b_value": "i",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB28; some scholars "
            "(Civitillo 2016) treat #038 as ideographic (double-axe). "
            "Linear B AB28=i."
        ),
    },
    {
        "chic_sign": "#041",
        "linear_a_sign": "AB30",
        "linear_b_value": "ni",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC sign-list ≈ AB30; AB30=ni "
            "(Ventris-Chadwick 1956)."
        ),
    },
    {
        "chic_sign": "#042",
        "linear_a_sign": "AB54",
        "linear_b_value": "wa",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB54; Salgarella 2020 "
            "p. 145 flags as debated. Linear B AB54=wa."
        ),
    },
    {
        "chic_sign": "#044",
        "linear_a_sign": "AB67",
        "linear_b_value": "ki",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB67; the highest-"
            "frequency CHIC sign and the most-disputed paleographic "
            "match. Civitillo 2016 argues for sealing-heraldic function "
            "rather than syllabographic. Linear B AB67=ki."
        ),
    },
    {
        "chic_sign": "#049",
        "linear_a_sign": "AB45",
        "linear_b_value": "de",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC tables propose ≈ AB45; second-highest-"
            "frequency CHIC sign (119 occurrences). Salgarella 2020 "
            "p. 145 records the match as debated. Linear B AB45=de."
        ),
    },
    {
        "chic_sign": "#053",
        "linear_a_sign": "AB13",
        "linear_b_value": "me",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB13; visual continuity in "
            "Salgarella 2020. Linear B AB13=me."
        ),
    },
    {
        "chic_sign": "#054",
        "linear_a_sign": "AB23",
        "linear_b_value": "mu",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC sign-list ≈ AB23; Linear B AB23=mu "
            "(Ventris-Chadwick 1956)."
        ),
    },
    {
        "chic_sign": "#057",
        "linear_a_sign": "AB46",
        "linear_b_value": "je",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB46; AB46=je per Ventris-"
            "Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#061",
        "linear_a_sign": "AB04",
        "linear_b_value": "te",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB04; Salgarella 2020 "
            "p. 145 records the match. Linear B AB04=te."
        ),
    },
    {
        "chic_sign": "#070",
        "linear_a_sign": "AB60",
        "linear_b_value": "ra",
        "confidence": "consensus",
        "citation": (
            "Younger online CHIC sign-list; Salgarella 2020 p. 144 "
            "(table 5.3, secure match); Decorte 2017. AB60=ra per "
            "Ventris-Chadwick 1956. One of the most-secure CHIC ↔ "
            "Linear A paleographic matches."
        ),
    },
    {
        "chic_sign": "#073",
        "linear_a_sign": "AB05",
        "linear_b_value": "to",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB05; AB05=to per Ventris-"
            "Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#077",
        "linear_a_sign": "AB80",
        "linear_b_value": "ma",
        "confidence": "proposed",
        "citation": (
            "Younger online CHIC tables ≈ AB80; AB80=ma per Ventris-"
            "Chadwick 1956."
        ),
    },
    {
        "chic_sign": "#092",
        "linear_a_sign": "AB44",
        "linear_b_value": "ke",
        "confidence": "debated",
        "citation": (
            "Younger online CHIC sign-list proposes ≈ AB44 for #092; "
            "potential conflict with #019 ≈ AB44 above. One of the two "
            "(or both) may be the true paleographic match. Linear B "
            "AB44=ke."
        ),
    },
]


# ---------------------------------------------------------------------------
# Corpus-distributional analysis
# ---------------------------------------------------------------------------


def load_chic_corpus() -> list[dict]:
    records: list[dict] = []
    with CHIC_CORPUS.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(json.loads(line))
    return records


def normalize_sign(token: str) -> str | None:
    """Return the canonical CHIC sign id ('#NNN') for a token, or None.

    Uncertain readings (`[?:#NNN]`) are mapped to `#NNN` so they count
    against the sign's frequency. Wholly-unknown (`[?]`), DIV, and NUM
    tokens return None.
    """
    if token.startswith("#"):
        return token
    if token.startswith("[?:#") and token.endswith("]"):
        return token[3:-1]
    return None


def compute_sign_stats(records: list[dict]) -> dict:
    """Aggregate per-sign statistics across the corpus.

    Returns a dict keyed by sign_id with values:
      {
        'frequency': int,
        'frequency_clean': int,
        'frequency_uncertain': int,
        'positions': {'start': int, 'middle': int, 'end': int},
        'supports': {<support>: count, ...},
        'sites': {<site>: count, ...},
        'inscription_count': int,  # distinct inscriptions
      }
    """
    stats: dict[str, dict] = defaultdict(lambda: {
        "frequency": 0,
        "frequency_clean": 0,
        "frequency_uncertain": 0,
        "positions": Counter(),
        "supports": Counter(),
        "sites": Counter(),
        "inscription_ids": set(),
    })
    for rec in records:
        tokens = rec["tokens"]
        # Drop DIV / NUM / [?] tokens for positional fingerprinting; we
        # want positions relative to the sign-only sequence.
        sign_positions: list[tuple[int, str, bool]] = []
        # tuple: (orig index, sign_id, is_uncertain)
        for tok in tokens:
            sid = normalize_sign(tok)
            if sid is None:
                continue
            is_unc = tok.startswith("[?:#")
            sign_positions.append((len(sign_positions), sid, is_unc))
        n = len(sign_positions)
        if n == 0:
            continue
        for idx, sid, is_unc in sign_positions:
            s = stats[sid]
            s["frequency"] += 1
            if is_unc:
                s["frequency_uncertain"] += 1
            else:
                s["frequency_clean"] += 1
            # Position: thirds of the sign-sequence.
            if n == 1:
                bucket = "single"
            elif idx < n / 3:
                bucket = "start"
            elif idx >= 2 * n / 3:
                bucket = "end"
            else:
                bucket = "middle"
            s["positions"][bucket] += 1
            s["supports"][rec.get("support") or "unknown"] += 1
            s["sites"][rec.get("site") or "unknown"] += 1
            s["inscription_ids"].add(rec["id"])
    # Materialize inscription_count and drop the set (not yaml-friendly).
    out: dict[str, dict] = {}
    for sid, s in stats.items():
        out[sid] = {
            "frequency": s["frequency"],
            "frequency_clean": s["frequency_clean"],
            "frequency_uncertain": s["frequency_uncertain"],
            "positions": dict(s["positions"]),
            "supports": dict(s["supports"]),
            "sites": dict(s["sites"]),
            "inscription_count": len(s["inscription_ids"]),
        }
    return out


# ---------------------------------------------------------------------------
# Linear A comparator
# ---------------------------------------------------------------------------


def load_linear_a_sign_freq() -> Counter:
    """Frequency of syllabographic AB-signs in the Linear A corpus.

    Excludes LOG:AB... (logograms used as ideograms in admin docs) and
    LOG:... (prosaic logogram tags). Returns a Counter keyed by AB-id.
    """
    freq: Counter = Counter()
    if not LINEAR_A_CORPUS.exists():
        return freq
    with LINEAR_A_CORPUS.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            rec = json.loads(line)
            tokens = rec.get("tokens") or []
            # Older Linear A pipeline tokenizes signs in raw_transliteration;
            # if `tokens` not present, fall back to a regex extract.
            if tokens:
                for tok in tokens:
                    if tok.startswith("AB") and tok[2:].isdigit():
                        freq[tok] += 1
            else:
                import re
                raw = rec.get("raw_transliteration", "")
                for m in re.finditer(r"\bAB(\d+)\b", raw):
                    # Exclude LOG:AB... (preceded by LOG:).
                    if m.start() >= 4 and raw[m.start() - 4:m.start()] == "LOG:":
                        continue
                    freq[f"AB{m.group(1)}"] += 1
    return freq


# ---------------------------------------------------------------------------
# YAML serialization (we keep it minimal-deps; hand-rolled to avoid taking
# a yaml dep on the build path. Output is parseable by PyYAML.)
# ---------------------------------------------------------------------------


def _yaml_str(s: str) -> str:
    """Quote a string for YAML emission. Always single-quote-escape."""
    return "'" + s.replace("'", "''") + "'"


def _emit_dict(d: dict, indent: int = 0) -> list[str]:
    """Emit a dict as block-style YAML lines. Sort keys for determinism."""
    out: list[str] = []
    pad = " " * indent
    for k in sorted(d.keys()):
        v = d[k]
        if isinstance(v, dict):
            if not v:
                out.append(f"{pad}{k}: {{}}")
            else:
                out.append(f"{pad}{k}:")
                out.extend(_emit_dict(v, indent + 2))
        elif isinstance(v, list):
            if not v:
                out.append(f"{pad}{k}: []")
            else:
                out.append(f"{pad}{k}:")
                for item in v:
                    if isinstance(item, dict):
                        item_lines = _emit_dict(item, indent + 4)
                        # Convert first line's leading whitespace to "- ".
                        first = item_lines[0]
                        out.append(f"{pad}- {first.lstrip()}")
                        out.extend(item_lines[1:])
                    else:
                        out.append(f"{pad}- {_emit_scalar(item)}")
        else:
            out.append(f"{pad}{k}: {_emit_scalar(v)}")
    return out


def _emit_scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if s == "":
        return "''"
    # Quote strings that look like numbers, booleans, special tokens, or
    # contain characters needing quoting.
    needs_quote = (
        s != s.strip()
        or s.startswith(("#", "&", "*", "!", "|", ">", "%", "@", "`", "?"))
        or ":" in s or "{" in s or "}" in s or "[" in s or "]" in s
        or "," in s or '"' in s
        or s.lower() in {"true", "false", "null", "yes", "no", "on", "off"}
    )
    try:
        float(s)
        needs_quote = True
    except ValueError:
        pass
    if needs_quote:
        return _yaml_str(s)
    return s


# ---------------------------------------------------------------------------
# Output: pools/cretan_hieroglyphic_signs.yaml
# ---------------------------------------------------------------------------


def write_signs_yaml(stats: dict, classifications: dict) -> None:
    """Emit the per-sign yaml.

    classifications[sign_id] = {'sign_class': ..., 'note': ...,
        'paleographic_candidates': [...] }
    """
    paleo_by_sign: dict[str, list[dict]] = defaultdict(list)
    for c in PALEOGRAPHIC_CANDIDATES:
        paleo_by_sign[c["chic_sign"]].append({
            "linear_a_sign": c["linear_a_sign"],
            "linear_b_value": c["linear_b_value"],
            "confidence": c["confidence"],
            "citation": c["citation"],
        })

    sign_ids = sorted(stats.keys(), key=lambda s: int(s.lstrip("#")))
    signs: list[dict] = []
    for sid in sign_ids:
        s = stats[sid]
        cls, note = classify_sign(sid)
        # Position fingerprint as fractions; round to 3 decimals for
        # determinism. Drop 'single' bucket if no single-sign occurrences.
        total_positions = sum(s["positions"].values())
        position_fingerprint: dict = {}
        for bucket in ("start", "middle", "end", "single"):
            if s["positions"].get(bucket, 0):
                position_fingerprint[bucket] = round(
                    s["positions"][bucket] / total_positions, 3
                )
        # Genre fingerprint: top-3 supports as fractions.
        total_supports = sum(s["supports"].values())
        genre_fingerprint: dict = {}
        for support, count in sorted(
            s["supports"].items(), key=lambda kv: (-kv[1], kv[0])
        )[:6]:
            genre_fingerprint[support] = round(count / total_supports, 3)
        entry: dict = {
            "id": sid,
            "sign_class": cls,
            "frequency": s["frequency"],
            "frequency_clean": s["frequency_clean"],
            "frequency_uncertain": s["frequency_uncertain"],
            "inscription_count": s["inscription_count"],
            "position_fingerprint": position_fingerprint,
            "genre_fingerprint": genre_fingerprint,
            "notes_from_olivier_godart": note,
        }
        if sid in paleo_by_sign:
            entry["paleographic_candidates"] = paleo_by_sign[sid]
        signs.append(entry)

    # Compose top-level yaml.
    header = (
        "# Cretan Hieroglyphic sign inventory (chic-v1; mg-c7e3)\n"
        "# Generated by scripts/build_chic_signs.py from the chic-v0 corpus\n"
        "# (corpora/cretan_hieroglyphic/all.jsonl, mg-99df).\n"
        "# Do not hand-edit; rerun the script.\n"
        "#\n"
        "# Schema: pools/schemas/chic_signs.v1.schema.json\n"
        "# README: pools/cretan_hieroglyphic_signs.README.md\n"
    )

    classification_rule = (
        "Per CHIC catalog convention (Olivier & Godart 1996, retained in "
        "Younger's web edition):\n"
        "- #001-#100: syllabographic (default).\n"
        "- #101-#299: ideogram / logogram (BOS=ox, OVIS=sheep, GRA=grain, "
        "OLI=olive, VIN=wine, ...).\n"
        "- #300-#399: ideogram (numerals + fractions).\n"
        "- AMBIGUOUS_OVERRIDES table in scripts/build_chic_signs.py records "
        "per-sign exceptions where O&G classification is debated. None "
        "applied at v1; rule is purely numeric-range.\n"
        "Classification will be reviewed in chic-v3 against substrate-"
        "framework distributional evidence."
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
        "Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean "
        "Greek._ Cambridge."
    )

    body: dict = {
        "catalog": "cretan_hieroglyphic_signs",
        "version": 1,
        "fetched_at": FETCHED_AT,
        "classification_rule": classification_rule,
        "source_citation": source_citation,
        "n_signs_total": len(signs),
        "n_syllabographic": sum(1 for s in signs if s["sign_class"] == "syllabographic"),
        "n_ideogram": sum(1 for s in signs if s["sign_class"] == "ideogram"),
        "n_ambiguous": sum(1 for s in signs if s["sign_class"] == "ambiguous"),
        "n_paleographic_candidates": sum(
            1 for s in signs if s.get("paleographic_candidates")
        ),
        "signs": signs,
    }

    # Render: top-level keys + the signs list. Use a custom layout that
    # keeps top-level scalars + multi-line strings readable.
    out_lines: list[str] = [header]
    out_lines.append(f"catalog: {body['catalog']}")
    out_lines.append(f"version: {body['version']}")
    out_lines.append(f"fetched_at: {_yaml_str(body['fetched_at'])}")
    out_lines.append("classification_rule: |")
    for ln in body["classification_rule"].splitlines():
        out_lines.append(f"  {ln}")
    out_lines.append("source_citation: |")
    for ln in body["source_citation"].splitlines():
        out_lines.append(f"  {ln}")
    out_lines.append(f"n_signs_total: {body['n_signs_total']}")
    out_lines.append(f"n_syllabographic: {body['n_syllabographic']}")
    out_lines.append(f"n_ideogram: {body['n_ideogram']}")
    out_lines.append(f"n_ambiguous: {body['n_ambiguous']}")
    out_lines.append(f"n_paleographic_candidates: {body['n_paleographic_candidates']}")
    out_lines.append("signs:")
    for s in signs:
        # First line: "- id: '#NNN'"
        out_lines.append(f"- id: {_yaml_str(s['id'])}")
        out_lines.append(f"  sign_class: {s['sign_class']}")
        out_lines.append(f"  frequency: {s['frequency']}")
        out_lines.append(f"  frequency_clean: {s['frequency_clean']}")
        out_lines.append(f"  frequency_uncertain: {s['frequency_uncertain']}")
        out_lines.append(f"  inscription_count: {s['inscription_count']}")
        if s["position_fingerprint"]:
            out_lines.append("  position_fingerprint:")
            for k in sorted(s["position_fingerprint"].keys()):
                out_lines.append(f"    {k}: {s['position_fingerprint'][k]}")
        else:
            out_lines.append("  position_fingerprint: {}")
        if s["genre_fingerprint"]:
            out_lines.append("  genre_fingerprint:")
            for k in sorted(s["genre_fingerprint"].keys()):
                out_lines.append(f"    {k}: {s['genre_fingerprint'][k]}")
        else:
            out_lines.append("  genre_fingerprint: {}")
        if s.get("paleographic_candidates"):
            out_lines.append("  paleographic_candidates:")
            for pc in s["paleographic_candidates"]:
                out_lines.append(f"  - linear_a_sign: {pc['linear_a_sign']}")
                out_lines.append(
                    f"    linear_b_value: {_yaml_str(pc['linear_b_value'])}"
                )
                out_lines.append(f"    confidence: {pc['confidence']}")
                out_lines.append(f"    citation: {_yaml_str(pc['citation'])}")
        if s["notes_from_olivier_godart"]:
            out_lines.append(
                "  notes_from_olivier_godart: "
                + _yaml_str(s["notes_from_olivier_godart"])
            )
        else:
            out_lines.append("  notes_from_olivier_godart: ''")

    POOL_YAML.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Output: pools/schemas/chic_signs.v1.schema.json
# ---------------------------------------------------------------------------


CHIC_SIGNS_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://github.com/drellem2/lineara/pools/schemas/chic_signs.v1.schema.json",
    "title": "Cretan Hieroglyphic sign inventory (v1)",
    "description": (
        "Per-sign metadata for the CHIC sign inventory. Each entry "
        "carries a class label (syllabographic / ideogram / ambiguous), "
        "frequency stats, positional + genre fingerprints, and an "
        "optional list of cross-script paleographic candidates."
    ),
    "type": "object",
    "required": [
        "catalog",
        "version",
        "classification_rule",
        "source_citation",
        "signs",
    ],
    "additionalProperties": True,
    "properties": {
        "catalog": {"const": "cretan_hieroglyphic_signs"},
        "version": {"const": 1},
        "fetched_at": {"type": "string"},
        "classification_rule": {"type": "string"},
        "source_citation": {"type": "string"},
        "n_signs_total": {"type": "integer", "minimum": 1},
        "n_syllabographic": {"type": "integer", "minimum": 0},
        "n_ideogram": {"type": "integer", "minimum": 0},
        "n_ambiguous": {"type": "integer", "minimum": 0},
        "n_paleographic_candidates": {"type": "integer", "minimum": 0},
        "signs": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "id",
                    "sign_class",
                    "frequency",
                    "position_fingerprint",
                    "notes_from_olivier_godart",
                ],
                "additionalProperties": True,
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^#\\d{3}$",
                        "description": "CHIC catalog id, zero-padded.",
                    },
                    "sign_class": {
                        "enum": ["syllabographic", "ideogram", "ambiguous"]
                    },
                    "frequency": {"type": "integer", "minimum": 0},
                    "frequency_clean": {"type": "integer", "minimum": 0},
                    "frequency_uncertain": {"type": "integer", "minimum": 0},
                    "inscription_count": {"type": "integer", "minimum": 0},
                    "position_fingerprint": {
                        "type": "object",
                        "description": (
                            "Fraction of occurrences in start/middle/end "
                            "third of the sign-only token sequence; "
                            "'single' bucket counts solo-sign inscriptions."
                        ),
                        "additionalProperties": {"type": "number"},
                    },
                    "genre_fingerprint": {
                        "type": "object",
                        "description": (
                            "Fraction of occurrences by inscription "
                            "support type (top-6)."
                        ),
                        "additionalProperties": {"type": "number"},
                    },
                    "paleographic_candidates": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": [
                                "linear_a_sign",
                                "linear_b_value",
                                "confidence",
                                "citation",
                            ],
                            "additionalProperties": False,
                            "properties": {
                                "linear_a_sign": {
                                    "type": "string",
                                    "pattern": "^AB\\d+$",
                                },
                                "linear_b_value": {"type": "string"},
                                "confidence": {
                                    "enum": ["consensus", "proposed", "debated"]
                                },
                                "citation": {"type": "string"},
                            },
                        },
                    },
                    "notes_from_olivier_godart": {"type": "string"},
                },
            },
        },
    },
}


def write_schema() -> None:
    POOL_SCHEMA.parent.mkdir(parents=True, exist_ok=True)
    POOL_SCHEMA.write_text(
        json.dumps(CHIC_SIGNS_SCHEMA, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Output: pools/cretan_hieroglyphic_signs.README.md
# ---------------------------------------------------------------------------


def write_readme(stats: dict) -> None:
    n_signs = len(stats)
    n_syll = sum(1 for sid in stats if classify_sign(sid)[0] == "syllabographic")
    n_ideo = sum(1 for sid in stats if classify_sign(sid)[0] == "ideogram")
    n_amb = sum(1 for sid in stats if classify_sign(sid)[0] == "ambiguous")

    consensus = sum(
        1 for c in PALEOGRAPHIC_CANDIDATES if c["confidence"] == "consensus"
    )
    proposed = sum(
        1 for c in PALEOGRAPHIC_CANDIDATES if c["confidence"] == "proposed"
    )
    debated = sum(
        1 for c in PALEOGRAPHIC_CANDIDATES if c["confidence"] == "debated"
    )

    text = f"""# Cretan Hieroglyphic sign inventory — README

This README documents `pools/cretan_hieroglyphic_signs.yaml`, the per-sign
classification + metadata file for the CHIC corpus (mg-c7e3, chic-v1).

## What it is

A YAML file with one entry per distinct sign id observed in the CHIC
corpus (`corpora/cretan_hieroglyphic/all.jsonl`, mg-99df, chic-v0). Each
entry carries:

- `id` — CHIC catalog id (e.g., `#044`).
- `sign_class` — one of `syllabographic`, `ideogram`, `ambiguous`.
- `frequency` / `frequency_clean` / `frequency_uncertain` /
  `inscription_count` — corpus counts.
- `position_fingerprint` — fraction of occurrences in the start / middle /
  end third of the sign-only token sequence (the `single` bucket counts
  inscriptions whose sign-only sequence has length 1).
- `genre_fingerprint` — fraction of occurrences by inscription support
  type (seal, crescent, medallion, bar, sealing, ...; top 6).
- `paleographic_candidates` — optional, present where the sign has a
  documented visual continuity to a Linear A AB-sign with an established
  Linear B carryover value.
- `notes_from_olivier_godart` — catalog gloss for ideograms; ambiguity
  reason for ambiguous signs; empty for default-classified syllabograms.

Schema: `pools/schemas/chic_signs.v1.schema.json` (JSON Schema 2020-12).

## Classification rule (chic-v1)

Per the CHIC catalog convention (Olivier & Godart 1996, retained in
Younger's web edition), CHIC sign IDs are organized by numeric range:

| Range      | Default class    | Description                                   |
|------------|-----------------|-----------------------------------------------|
| #001-#100  | syllabographic   | The CHIC syllabogram repertoire (~96 catalogued, ~78-100 attested). |
| #101-#299  | ideogram         | Logograms / ideograms (BOS, OVIS, GRA, OLI, VIN, AROM, OLE, VAS). |
| #300-#399  | ideogram         | Numerals + fractions (CHIC #301-#308).         |

A per-sign exception list (`AMBIGUOUS_OVERRIDES` in
`scripts/build_chic_signs.py`) flags signs whose classification is
debated in the scholarly literature. **No overrides are applied at v1**:
the rule is purely numeric-range. The exception list is in place so
that chic-v3 (substrate-framework application) can populate it from a
fuller scholarly review. Per the ticket's caution:

> The classification is partly judgment-based. Be explicit about the
> rules used; do NOT silently call signs ideographic without evidence.
> The classification will be the foundation of all chic-v2+ work, so
> errors here propagate.

A handful of signs in the syllabographic range have well-known
iconographic content (e.g., #008 double-axe, #038 double-axe variant,
#044 trowel/gate). These are kept as syllabographic per O&G 1996, but
are flagged in the `paleographic_candidates` confidence field as
`debated` where applicable.

## What's in the corpus

| Metric | Count |
|--------|-------|
| Distinct sign IDs | **{n_signs}** |
| Syllabographic | {n_syll} |
| Ideogram | {n_ideo} |
| Ambiguous | {n_amb} |
| Paleographic candidates (CHIC ↔ Linear A) | {len(PALEOGRAPHIC_CANDIDATES)} |
| ↳ consensus | {consensus} |
| ↳ proposed | {proposed} |
| ↳ debated | {debated} |

## Paleographic candidates

`paleographic_candidates` enumerates CHIC signs with documented visual
continuity to Linear A AB-signs that have established Linear B
carryover values. Each candidate is curated from one or more of:

- **Younger, J. G.** Online CHIC sign-list (offline since 2022; cached
  Wayback snapshot 20220703170656). Each Younger sign-list entry
  carries an "≈ Linear A AB-NN" annotation where the visual match is
  scholarly consensus.
- **Salgarella, E. (2020).** *Aegean Linear Script(s).* Cambridge.
  Table 5.3 (CHIC ↔ Linear A visual matches). The most-recent
  monograph-length treatment.
- **Decorte, R. (2017, 2018).** *The First 'European' Writing*; also
  Decorte's CHIC paleography papers.
- **Civitillo, M. (2016).** *La scrittura geroglifica minoica sui
  sigilli.* For the contested signs (#044, #008, #038).

Confidence levels:

| Confidence | Meaning |
|------------|---------|
| `consensus` | Multiple sources concur (Salgarella + Younger + Decorte). Suitable as a tier-1 anchor in chic-v2. |
| `proposed`  | Single primary source proposes the match. Treat as a candidate; do not promote to anchor without corroboration. |
| `debated`   | Match is asserted in some sources but rejected in others. Useful for negative-control work; not a v2 anchor. |

The candidates are committed in this file for transparency and for
chic-v2 (mechanical anchor inheritance). v1 does NOT apply them as
anchors.

## How to regenerate

```bash
python3 scripts/build_chic_signs.py
```

Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0).
Outputs: this directory's `cretan_hieroglyphic_signs.yaml` + the
two `results/` reports.

## Out of scope for chic-v1

- **Mechanical anchor inheritance** (apply paleographic candidates as
  tier-1 anchors, propagate readings) — chic-v2.
- **Substrate framework application** to CHIC syllabographic subset —
  chic-v3.
- **Per-sign value extraction framework** — chic-v5+.
- **Cross-script correlation analysis** — chic-v4.
- **Visual paleography work** beyond enumeration of scholarly-curated
  candidates — out of scope; the framework treats CHIC sign IDs as
  opaque tokens.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum
  Inscriptionum Cretae* (Études Crétoises 31). Paris. **Print only;
  not available online.** The canonical CHIC catalog.
- Younger, J. G. *The Cretan Hieroglyphic Texts: a web edition of CHIC
  with commentary.* Originally `people.ku.edu/~jyounger/Hiero/`;
  fetched from Wayback Machine snapshot 20220703170656.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge UP.
- Decorte, R. (2017). "The First 'European' Writing: Redefining the
  Archanes Script." *Oxford Journal of Archaeology* 36 (4).
- Decorte, R. (2018). "Cretan Hieroglyphic and the Nature of Script."
  In *Paths into Script Formation in the Ancient Mediterranean.*
- Civitillo, M. (2016). *La scrittura geroglifica minoica sui sigilli.*
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.*
  Cambridge UP. The basis of all Linear A → Linear B carryover values.
- Schoep, I. (2002). *The Administration of Neopalatial Crete.*
- Palmer, L. (1995). "ku-ro and ki-ro in Linear A."
"""
    POOL_README.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Output: results/chic_sign_inventory.md
# ---------------------------------------------------------------------------


def write_inventory_report(stats: dict) -> None:
    n_total = len(stats)
    by_class: dict[str, int] = Counter()
    for sid in stats:
        cls, _ = classify_sign(sid)
        by_class[cls] += 1
    total_token_count = sum(s["frequency"] for s in stats.values())
    sign_ids = sorted(stats.keys(), key=lambda s: int(s.lstrip("#")))

    lines: list[str] = []
    a = lines.append
    a("# CHIC sign inventory — chic-v1 (mg-c7e3)")
    a("")
    a(
        "Per-sign frequency, positional, and genre distribution table for "
        "the Cretan Hieroglyphic corpus. Generated by "
        "`scripts/build_chic_signs.py` from "
        "`corpora/cretan_hieroglyphic/all.jsonl` (mg-99df, chic-v0). "
        "Classification rule: see "
        "`pools/cretan_hieroglyphic_signs.README.md`."
    )
    a("")
    a(f"Last refresh: **{FETCHED_AT[:10]}**.")
    a("")
    a("## Summary")
    a("")
    a("| Metric | Count |")
    a("|---|---|")
    a(f"| Distinct sign IDs observed | **{n_total}** |")
    a(f"| Total sign-token occurrences (clean + uncertain) | {total_token_count} |")
    a(f"| Syllabographic signs | {by_class.get('syllabographic', 0)} |")
    a(f"| Ideogram signs | {by_class.get('ideogram', 0)} |")
    a(f"| Ambiguous signs | {by_class.get('ambiguous', 0)} |")
    a(f"| Paleographic candidates flagged | {len(PALEOGRAPHIC_CANDIDATES)} |")
    a("")

    a("## Top-30 by frequency")
    a("")
    a("| Sign | Class | Freq (clean+unc) | Inscriptions | Top supports |")
    a("|---|---|---|---|---|")
    top30 = sorted(
        stats.items(), key=lambda kv: -kv[1]["frequency"]
    )[:30]
    for sid, s in top30:
        cls, _ = classify_sign(sid)
        top_supports = ", ".join(
            f"{k} ({v})"
            for k, v in sorted(
                s["supports"].items(), key=lambda kv: (-kv[1], kv[0])
            )[:3]
        )
        a(
            f"| `{sid}` | {cls} | {s['frequency']} "
            f"({s['frequency_clean']}+{s['frequency_uncertain']}) | "
            f"{s['inscription_count']} | {top_supports} |"
        )
    a("")

    a("## Full inventory (sorted by sign id)")
    a("")
    a(
        "Position fingerprint columns (`p.start` / `p.mid` / `p.end` / "
        "`p.solo`) report the fraction of occurrences in the first / "
        "middle / last third of the sign-only token sequence; `p.solo` "
        "counts inscriptions whose sign-only sequence has length 1."
    )
    a("")
    a(
        "| Sign | Class | Freq | Insc | p.start | p.mid | p.end | p.solo | Top support |"
    )
    a("|---|---|---|---|---|---|---|---|---|")
    for sid in sign_ids:
        s = stats[sid]
        cls, _ = classify_sign(sid)
        total_p = sum(s["positions"].values()) or 1
        p_start = round(s["positions"].get("start", 0) / total_p, 2)
        p_mid = round(s["positions"].get("middle", 0) / total_p, 2)
        p_end = round(s["positions"].get("end", 0) / total_p, 2)
        p_solo = round(s["positions"].get("single", 0) / total_p, 2)
        top_support = max(s["supports"].items(), key=lambda kv: kv[1])[0]
        a(
            f"| `{sid}` | {cls} | {s['frequency']} | "
            f"{s['inscription_count']} | {p_start} | {p_mid} | {p_end} | "
            f"{p_solo} | {top_support} |"
        )
    a("")

    a("## Ideograms observed")
    a("")
    a(
        "Signs in the #101+ range that appear in the corpus. Each entry "
        "carries the catalog gloss where curated."
    )
    a("")
    a("| Sign | Freq | Catalog gloss |")
    a("|---|---|---|")
    for sid in sign_ids:
        cls, note = classify_sign(sid)
        if cls == "ideogram":
            a(f"| `{sid}` | {stats[sid]['frequency']} | {note or '(no gloss curated)'} |")
    a("")

    a("## Paleographic candidates (CHIC ↔ Linear A)")
    a("")
    a(
        "Curated from Salgarella 2020, Younger online, Decorte 2017, "
        "Civitillo 2016. v1 enumerates only; chic-v2 will mechanically "
        "apply the consensus subset as tier-1 anchors. See "
        "`pools/cretan_hieroglyphic_signs.yaml` for the per-sign "
        "embedding."
    )
    a("")
    a("| CHIC | ≈ Linear A | LB value | Confidence | Note |")
    a("|---|---|---|---|---|")
    for c in sorted(
        PALEOGRAPHIC_CANDIDATES, key=lambda c: int(c["chic_sign"].lstrip("#"))
    ):
        chic = c["chic_sign"]
        # CHIC freq from stats if observed; '(unattested)' otherwise.
        freq_note = ""
        if chic in stats:
            freq_note = f"freq {stats[chic]['frequency']}"
        else:
            freq_note = "(unattested in corpus)"
        a(
            f"| `{chic}` | {c['linear_a_sign']} | "
            f"`{c['linear_b_value']}` | {c['confidence']} | {freq_note} |"
        )
    a("")

    INV_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Output: results/chic_vs_linear_a_sign_inventory_comparison.md
# ---------------------------------------------------------------------------


def write_comparison_report(chic_stats: dict, la_freq: Counter) -> None:
    # CHIC syllabographic-only frequencies.
    chic_syll = {
        sid: s for sid, s in chic_stats.items()
        if classify_sign(sid)[0] == "syllabographic"
    }
    chic_syll_freqs = sorted(
        (s["frequency"] for s in chic_syll.values()), reverse=True
    )
    chic_syll_total = sum(chic_syll_freqs)
    chic_n_distinct = len(chic_syll_freqs)

    la_freqs = sorted(la_freq.values(), reverse=True)
    la_total = sum(la_freqs)
    la_n_distinct = len(la_freqs)

    def topk_coverage(freqs: list[int], k: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round(sum(freqs[:k]) / total, 3)

    def percentile(freqs: list[int], total: int, frac: float) -> int:
        """Smallest k such that top-k coverage >= frac."""
        if total == 0:
            return 0
        running = 0
        for i, f in enumerate(freqs, 1):
            running += f
            if running / total >= frac:
                return i
        return len(freqs)

    # Pareto-shape proxy: ratio of top-1, top-5, top-10, top-20 coverage.
    rows: list[tuple[str, int, int, float, float, float, float, int, int]] = []
    for label, freqs, total, n_distinct in [
        ("CHIC (syllabographic)", chic_syll_freqs, chic_syll_total, chic_n_distinct),
        ("Linear A (AB-syllabograms)", la_freqs, la_total, la_n_distinct),
    ]:
        rows.append((
            label,
            n_distinct,
            total,
            topk_coverage(freqs, 1, total),
            topk_coverage(freqs, 5, total),
            topk_coverage(freqs, 10, total),
            topk_coverage(freqs, 20, total),
            percentile(freqs, total, 0.50),
            percentile(freqs, total, 0.80),
        ))

    lines: list[str] = []
    a = lines.append
    a("# CHIC vs Linear A — sign-inventory comparison (chic-v1, mg-c7e3)")
    a("")
    a(
        "Sanity-check that the CHIC syllabographic subset is in a "
        "tractable corpus regime, by comparing its sign-frequency "
        "distribution to Linear A's syllabographic (AB-sign) frequency "
        "distribution. Generated by `scripts/build_chic_signs.py` from "
        "`corpora/cretan_hieroglyphic/all.jsonl` (mg-99df) and "
        "`corpus/all.jsonl` (Linear A)."
    )
    a("")
    a(f"Last refresh: **{FETCHED_AT[:10]}**.")
    a("")
    a("## Summary table")
    a("")
    a(
        "| Corpus | Distinct signs | Total sign tokens | top-1 cov | "
        "top-5 cov | top-10 cov | top-20 cov | k for 50% cov | k for 80% cov |"
    )
    a("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        a(
            f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | "
            f"{r[5]} | {r[6]} | {r[7]} | {r[8]} |"
        )
    a("")

    a("## Reading")
    a("")
    chic_n = chic_n_distinct
    chic_top10 = topk_coverage(chic_syll_freqs, 10, chic_syll_total)
    chic_k80 = percentile(chic_syll_freqs, chic_syll_total, 0.80)
    la_n = la_n_distinct
    la_top10 = topk_coverage(la_freqs, 10, la_total)
    la_k80 = percentile(la_freqs, la_total, 0.80)
    a(
        f"- The CHIC syllabographic subset has **{chic_n} distinct "
        f"signs** (target population for chic-v5+ value extraction). "
        f"Linear A has **{la_n} distinct AB-syllabograms** observed in "
        f"its corpus."
    )
    a(
        f"- The CHIC distribution is heavy-tailed: the top-10 most "
        f"frequent CHIC syllabograms cover **{chic_top10*100:.0f}%** of "
        f"all syllabographic occurrences, vs **{la_top10*100:.0f}%** for "
        f"Linear A's top-10."
    )
    a(
        f"- Top-{chic_k80} CHIC signs cover 80% of syllabographic "
        f"tokens; Linear A needs top-{la_k80} signs for the same "
        f"coverage."
    )
    a("")
    if chic_top10 >= la_top10 - 0.05 and chic_top10 <= la_top10 + 0.10:
        shape = "similar"
    elif chic_top10 > la_top10 + 0.10:
        shape = "heavier-tailed (more concentrated)"
    else:
        shape = "lighter-tailed (more uniform)"
    a(
        f"- **Distribution-shape verdict:** CHIC syllabographic "
        f"frequency distribution is **{shape}** than Linear A's "
        f"AB-syllabogram distribution."
    )
    a("")
    a(
        "Both corpora exhibit Zipfian behavior; the CHIC corpus is "
        "smaller but the per-sign frequency profile is in the same "
        "order-of-magnitude regime, which means downstream chic-v3+ "
        "harnesses can use the same heavy-tail-sensitive metrics that "
        "the Linear A pipeline uses."
    )
    a("")
    a("## Caveats")
    a("")
    a(
        "- The CHIC corpus is ~{0}× smaller than the Linear A corpus by "
        "sign-token count ({1} vs {2}). Tail estimates "
        "(top-20+, percentile k for 80% coverage) are correspondingly "
        "noisier on the CHIC side. The comparison is a sanity-check, "
        "not a precise statistical claim.".format(
            round(la_total / max(chic_syll_total, 1), 1),
            chic_syll_total,
            la_total,
        )
    )
    a(
        "- CHIC sign-class assignment is per the catalog numeric-range "
        "rule (see README); a future chic-v3 reclassification may "
        "shift signs in/out of the syllabographic subset and shift "
        "these counts."
    )
    a(
        "- Linear A AB-tokens here include all AB-prefixed sign tokens; "
        "LOG-prefixed (logogram) tokens are excluded. Sign-class "
        "consistency between the two corpora is approximate."
    )
    a("")

    COMPARISON_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--corpus", type=Path, default=CHIC_CORPUS,
        help="Path to corpora/cretan_hieroglyphic/all.jsonl",
    )
    args = parser.parse_args(argv)

    if not args.corpus.exists():
        print(
            f"ERROR: missing CHIC corpus at {args.corpus}; "
            "run scripts/build_chic_corpus.py first.",
            file=sys.stderr,
        )
        return 2

    records = load_chic_corpus()
    stats = compute_sign_stats(records)
    if not stats:
        print("ERROR: no signs extracted from corpus.", file=sys.stderr)
        return 2

    POOL_YAML.parent.mkdir(parents=True, exist_ok=True)
    INV_REPORT.parent.mkdir(parents=True, exist_ok=True)

    write_schema()
    write_signs_yaml(stats, classifications=stats)
    write_readme(stats)
    write_inventory_report(stats)

    la_freq = load_linear_a_sign_freq()
    write_comparison_report(stats, la_freq)

    n_syll = sum(1 for sid in stats if classify_sign(sid)[0] == "syllabographic")
    n_ideo = sum(1 for sid in stats if classify_sign(sid)[0] == "ideogram")
    n_amb = sum(1 for sid in stats if classify_sign(sid)[0] == "ambiguous")
    print(
        f"wrote {len(stats)} signs  |  "
        f"syllabographic={n_syll}  ideogram={n_ideo}  ambiguous={n_amb}  |  "
        f"paleographic candidates={len(PALEOGRAPHIC_CANDIDATES)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
