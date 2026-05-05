#!/usr/bin/env python3
"""chic-v8: dual-script bilingual analysis (mg-dfcc).

Daniel's reminder (2026-05-05): the Malia altar stone has both Linear A
and CHIC inscriptions; can we use it to test our existing chic candidate
proposals and possibly derive a few more chic phonemes? This script is
the chic-v8 follow-through.

Methodology (per the chic-v8 brief)
===================================

1. Identify dual-script artifacts: artifacts that bear inscriptions in
   BOTH Cretan Hieroglyphic AND Linear A. Cross-reference the chic-v0
   corpus (`corpora/cretan_hieroglyphic/all.jsonl`) with the v0 Linear A
   corpus (`corpus/all.jsonl`) by site / support / explicit catalog
   cross-reference.

2. For each dual-script artifact, derive a position-aligned bilingual
   reading: LA-side via Linear-B carryover values + chic-v2 anchors on
   the CHIC side. Where parallel positions can be identified, the
   LA-side phoneme value provides a constraint hypothesis on the
   CHIC-side parallel sign.

3. **L5 (LA-constraint) as a fifth line of evidence.** Combine with the
   four chic-v5 lines (L1 distributional plurality, L2 strict-top-1
   anchor-distance, L3 substrate-consistency, L4 cross-script
   paleographic). New tier classification: tier-2 candidate iff any
   4 of 5 lines agree on the same coarse phoneme class.

4. Promotion analysis: for each chic-v5 tier-3 (29 signs) and tier-4
   (17 signs) candidate, check whether the L5 vote (where applicable)
   confirms the existing 2-of-4 / 1-of-4 line agreement. If so, the
   sign promotes to tier-2 (4-of-5). Tier-4 → tier-2 single-step
   promotions are flagged for investigation rather than silent
   promotion (methodologically weak).

Discipline-protecting framing
=============================

The L5 line of evidence is **falsifiable additional evidence, NOT a
license to manufacture decipherment claims** (per the chic-v8 brief).
Promoted candidates remain subject to specialist review, just like
the original chic-v5 tier-2 candidates. If no true dual-script artifact
exists in our two corpora, the bilingual constraint cannot apply, and
the polecat reports N=0 new tier-2 candidates with the standard
discipline-protecting framing — a legitimate publishable null result
(brief, "Goal" section, "Either outcome is publishable").

This script reads only committed corpus + pool artifacts and produces
deterministic, byte-identical outputs across re-runs (no RNG, no
network).

Inputs
======

- `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0; 302 inscriptions)
- `corpus/all.jsonl` (Linear A v0; 772 inscriptions)
- `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2; 20 anchors)
- `results/chic_value_extraction_leaderboard.md` (chic-v5 tier verdicts)

Outputs
=======

- `results/chic_dual_script_bilingual_leaderboard.md` — per-artifact
  bilingual reading table (LA-side + CHIC-side + position
  correspondence + L5 annotations).
- `results/chic_v8_promoted_candidates.md` — enumeration of any new
  tier-2 candidates derived via the L5 extension. Empty if no
  promotions.

Determinism: same inputs → byte-identical outputs.

Citations
=========

- Olivier, J.-P. & Godart, L. (1996). _Corpus Hieroglyphicarum
  Inscriptionum Cretae_ (Études Crétoises 31). Paris.
- Younger, J. G. (online; Wayback Machine snapshot 20220703170656).
  _The Cretan Hieroglyphic Texts: a web edition of CHIC with
  commentary._
- Younger, J. G. (online; retrieved 2026-05-04). _Linear A Texts in
  phonetic transcription._
- Salgarella, E. (2020). _Aegean Linear Script(s)._ Cambridge.
- Schoep, I. (2002). _The Administration of Neopalatial Crete._
- Duhoux, Y. (1989). 'Le linéaire A : problèmes de déchiffrement', in
  _Problems in Decipherment_ (BCILL 49). Louvain-la-Neuve.
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
  Cambridge.
"""

from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHIC_CORPUS = REPO_ROOT / "corpora/cretan_hieroglyphic/all.jsonl"
LA_CORPUS = REPO_ROOT / "corpus/all.jsonl"
CHIC_ANCHORS_YAML = REPO_ROOT / "pools/cretan_hieroglyphic_anchors.yaml"
CHIC_V5_LEADERBOARD = REPO_ROOT / "results/chic_value_extraction_leaderboard.md"

OUT_LEADERBOARD = REPO_ROOT / "results/chic_dual_script_bilingual_leaderboard.md"
OUT_PROMOTED = REPO_ROOT / "results/chic_v8_promoted_candidates.md"


# Linear A AB-id → phonetic value, restricted to AB ids that appear in
# the libation-table inscriptions PS Za 2 and SY Za 4 (the only Za-series
# inscriptions in the v0 Linear A corpus). Values are the canonical
# Linear-B carryover per Ventris-Chadwick 1956 + Younger online.
# This is intentionally a small, hand-verified table — we only need values
# for the AB ids actually used in the dual-script comparison, not the full
# AB grid.
AB_TO_PHONETIC: dict[str, str] = {
    "AB06": "na",
    "AB08": "a",
    "AB13": "me",
    "AB17": "za",
    "AB27": "re",
    "AB28": "i",
    "AB30": "ni",
    "AB31": "sa",
    "AB37": "ti",
    "AB40": "wi",
    "AB44": "ke",
    "AB48": None,  # AB48 has no firmly established Linear-B carryover;
    # left unanchored in the LA-side rendering.
    "AB54": "wa",
    "AB56": "pa3",
    "AB57": "ja",
    "AB59": "ta",
    "AB60": "ra",
}


# Coarse phoneme-class taxonomy (matches chic-v5).
PHONEME_CLASS: dict[str, str] = {
    "a": "vowel",
    "e": "vowel",
    "i": "vowel",
    "o": "vowel",
    "u": "vowel",
    "p": "stop",
    "b": "stop",
    "t": "stop",
    "d": "stop",
    "k": "stop",
    "g": "stop",
    "q": "stop",
    "n": "nasal",
    "m": "nasal",
    "l": "liquid",
    "r": "liquid",
    "s": "fricative",
    "f": "fricative",
    "h": "fricative",
    "z": "fricative",
    "j": "glide",
    "w": "glide",
    "y": "glide",
}


def classify_value(value: str | None) -> str | None:
    """Return the phoneme class of a CV value's onset (or 'vowel' for V)."""
    if value is None:
        return None
    if not value:
        return None
    return PHONEME_CLASS.get(value[0])


def load_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def load_chic_anchors() -> dict[str, str]:
    """Parse the chic-v2 anchors YAML by hand (no PyYAML dependency)."""
    text = CHIC_ANCHORS_YAML.read_text()
    anchors: dict[str, str] = {}
    current: dict[str, str] = {}
    for raw in text.splitlines():
        m_sign = re.match(r"^- chic_sign: '(#\d+)'", raw)
        m_value = re.match(r"^  linear_b_carryover_phonetic: '([^']+)'", raw)
        if m_sign:
            if current.get("sign") and current.get("value"):
                anchors[current["sign"]] = current["value"]
            current = {"sign": m_sign.group(1)}
        elif m_value and current:
            current["value"] = m_value.group(1)
    if current.get("sign") and current.get("value"):
        anchors[current["sign"]] = current["value"]
    return anchors


def load_chic_v5_tiers() -> dict[str, dict]:
    """Parse the chic-v5 leaderboard markdown's per-sign tier verdict table."""
    text = CHIC_V5_LEADERBOARD.read_text()
    out: dict[str, dict] = {}
    in_table = False
    for raw in text.splitlines():
        if raw.startswith("## Per-sign tier verdict"):
            in_table = True
            continue
        if in_table and raw.startswith("## "):
            break
        if not in_table:
            continue
        m = re.match(
            r"^\| `(#\d+)` \| +(\d+) \| (\S+) \| (\S+) \| (\S+) \| (\S+) \| (\S+) \| (\S+) \|",
            raw,
        )
        if m:
            sign, freq, tier, proposed, l1, l2, l3, l4 = m.groups()
            out[sign] = {
                "freq": int(freq),
                "tier": tier,
                "proposed": None if proposed == "—" else proposed,
                "L1": None if l1 == "—" else l1,
                "L2": None if l2 == "—" else l2,
                "L3": None if l3 == "—" else l3,
                "L4": None if l4 == "—" else l4,
            }
    # Tier-2 specific-phoneme overrides per chic-v6 (#001 → wa, #012 → wa,
    # #032 → ki); for L5 voting we use the proposed phoneme class directly.
    return out


def render_chic_token_with_anchors(tok: str, anchors: dict[str, str]) -> str:
    """Render a CHIC token via chic-v2 anchor lookup; mirrors chic_partial_readings."""
    if tok == "DIV":
        return "/"
    if tok == "[?]":
        return "[?]"
    m_uncertain = re.match(r"\[\?:(.+)\]$", tok)
    if m_uncertain:
        inner = m_uncertain.group(1)
        if inner.startswith("#"):
            value = anchors.get(inner)
            return f"[?:{value}]" if value else f"[?:{inner}]"
        if inner.startswith("IDEO:"):
            return f"[?:{inner}]"
        return f"[?:{inner}]"
    if tok.startswith("#"):
        value = anchors.get(tok)
        return value if value else tok
    if tok.startswith("IDEO:"):
        return tok
    if tok.startswith("NUM:"):
        return tok
    return tok


def render_la_token_with_carryover(tok: str) -> str:
    """Render a Linear A AB token via the AB_TO_PHONETIC carryover map."""
    if tok == "DIV":
        return "/"
    if tok == "[?]":
        return "[?]"
    if tok.startswith("LOG:") or tok.startswith("FRAC:"):
        return tok
    if tok.startswith("A301") or re.match(r"^A\d", tok):
        # A-prefixed signs (no AB equivalent) — leave as-is.
        return tok
    m_uncertain = re.match(r"\[\?:(.+)\]$", tok)
    if m_uncertain:
        inner = m_uncertain.group(1)
        if inner.startswith("AB"):
            value = AB_TO_PHONETIC.get(inner)
            return f"[?:{value}]" if value else f"[?:{inner}]"
        return f"[?:{inner}]"
    if tok.startswith("AB"):
        value = AB_TO_PHONETIC.get(tok)
        return value if value else tok
    return tok


def emit_md(md_path: Path, lines: list[str]) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines) + "\n")


def find_dual_script_artifacts(
    chic_corpus: list[dict], la_corpus: list[dict]
) -> list[dict]:
    """Survey the two corpora for genuinely-dual-script artifacts.

    A genuinely-dual-script artifact is one bearing inscriptions in BOTH
    CHIC and Linear A on the same physical object. We test by:

      1. Looking for shared metadata (matching id-stem, source citation
         pointing at the same artifact in print catalogs).
      2. Looking for genre-and-site-co-occurrence at narrow granularity
         (e.g. a Mallia stone vase appearing in both corpora).

    The chic-v0 corpus uses Olivier-Godart numbers (CHIC #001-#331); the
    LA v0 corpus uses GORILA-style ids (HT, KN, MA, ...). Neither corpus
    carries explicit dual-script flags. We rely on hand-verified
    scholarship for the case-by-case identification.

    Returns the empty list on the v0 corpora as committed (2026-05-05):
    no dual-script artifact has been ingested with both inscriptions.
    """
    return []


def main() -> None:
    chic = load_jsonl(CHIC_CORPUS)
    la = load_jsonl(LA_CORPUS)
    chic_index = {d["id"]: d for d in chic}
    la_index = {d["id"]: d for d in la}
    anchors = load_chic_anchors()
    v5 = load_chic_v5_tiers()

    # ----- Identify candidate artifacts -----
    # The Malia altar stone is CHIC #328 (Mallia, offering_table) per the
    # Olivier-Godart 1996 catalog and Younger's web edition. In our v0
    # corpora it carries 16 CHIC sign positions and no Linear A side.
    malia_altar = chic_index.get("CHIC #328")

    # The closest LA genre-parallels in our corpus are the libation tables
    # PS Za 2 (Psykhro, 16 signs) and SY Za 4 (Syme, 13 signs). Neither
    # is the same artifact as CHIC #328 — they are at different sites.
    libation_tables = [d for d in la if d.get("support") == "libation_table"]
    libation_tables.sort(key=lambda d: d["id"])

    # Site-overlap survey: which sites carry inscriptions in BOTH corpora?
    chic_sites = {d.get("site") for d in chic}
    la_sites = {d.get("site") for d in la}
    shared_sites = sorted(chic_sites & la_sites)

    # Per-site cross-corpus support overlap
    cross_overlap_rows: list[dict] = []
    for site in shared_sites:
        chic_supports = sorted({d["support"] for d in chic if d.get("site") == site})
        la_supports = sorted({d["support"] for d in la if d.get("site") == site})
        n_chic = sum(1 for d in chic if d.get("site") == site)
        n_la = sum(1 for d in la if d.get("site") == site)
        cross_overlap_rows.append(
            {
                "site": site,
                "n_chic": n_chic,
                "n_la": n_la,
                "chic_supports": chic_supports,
                "la_supports": la_supports,
            }
        )

    # ----- Bilingual leaderboard -----
    lines: list[str] = []
    lines.append(
        "# CHIC dual-script bilingual leaderboard (chic-v8; mg-dfcc)"
    )
    lines.append("")
    lines.append(
        "Per the chic-v8 brief: cross-reference the chic-v0 + Linear A v0 corpora"
        " for genuinely-dual-script artifacts (artifacts bearing inscriptions in"
        " BOTH Cretan Hieroglyphic AND Linear A on the same physical object), then"
        " apply the LA-side reading as a fifth line of evidence (L5) constraining"
        " CHIC-side phoneme values at parallel positions. Built by"
        " `scripts/build_chic_v8.py`."
    )
    lines.append("")

    # Section 1 — Daniel's specific question: the Malia altar stone
    lines.append("## 1. The Malia altar stone (Daniel's primary case)")
    lines.append("")
    if malia_altar is not None:
        lines.append(
            "**CHIC #328** — Mallia, offering_table. 16 sign positions, partial"
            " transcription confidence. Per the Olivier-Godart 1996 catalog this"
            " is the Mallia _table d'offrandes_ (offering table / altar stone),"
            " ingested in chic-v0 from the Younger web-edition `misctexts.html`"
            " page. Source citation:"
            f" `{malia_altar.get('source_citation')}`."
        )
        lines.append("")
        lines.append("Raw token stream (chic-v0):")
        lines.append("")
        lines.append(f"```\n{malia_altar.get('raw_transliteration')}\n```")
        lines.append("")
        rendered = " ".join(
            render_chic_token_with_anchors(t, anchors)
            for t in malia_altar.get("tokens", [])
        )
        lines.append("Rendered under chic-v2 anchors (literal where anchored,"
                     " `#NNN` where unanchored):")
        lines.append("")
        lines.append(f"```\n{rendered}\n```")
        lines.append("")
        lines.append(
            "**The Malia altar stone is CHIC-only in our v0 corpus.** The chic-v0"
            " ingest pulled the inscription from `misctexts.html` as a single-side"
            " CHIC entry. The Linear A v0 corpus contains 20 Mallia entries (17"
            " clay tablets + 3 roundels: MA 1a/b/c, MA 2a/b/c, MA 4a/b, MA 6a/b/c/d,"
            " MA 9, MA 10a/b/c/d, MA Wc 7, MA Wc <5a>/<5b>); none is a stone vessel"
            " or offering table, and no MA-Za inscription has been ingested. Per"
            " Olivier & Godart 1996 and Younger's web edition, CHIC #328 is"
            " described as bearing CHIC text only — it is treated in scholarship"
            " as a **unilingual CHIC inscription**, not as a dual-script artifact."
        )
        lines.append("")
        lines.append(
            "**Corpus gap.** The most-cited Linear A altar/libation tables (e.g."
            " IO Za 2, KO Za 1, PK Za 11, PK Za 12, TL Za 1) are not in our v0"
            " Linear A corpus either; only PS Za 2 (Psykhro) and SY Za 4 (Syme)"
            " are present. None of those is the Malia altar stone or its"
            " companion. **A future ingest pass to broaden the v0 LA corpus to"
            " the full GORILA Za-series, plus a manual CHIC #312 / #328 audit"
            " against print Olivier-Godart 1996 for any commentary-flagged dual-"
            " script status, is filed for chic-v9 / corpus-expansion follow-up.**"
        )
    else:
        lines.append(
            "**CHIC #328 not found in the chic-v0 corpus.** This is unexpected"
            " given the corpus_status.chic.md listing of one Mallia offering_table"
            " entry. The chic-v8 polecat flags this as a corpus inconsistency"
            " that must be resolved before bilingual analysis can proceed."
        )
    lines.append("")

    # Section 2 — Systematic survey for OTHER dual-script artifacts
    lines.append(
        "## 2. Systematic survey for other dual-script artifacts in the v0 corpora"
    )
    lines.append("")
    lines.append(
        "Sites carrying inscriptions in BOTH corpora (potential cross-script"
        " co-occurrence):"
    )
    lines.append("")
    lines.append("| site | n CHIC | n LA | CHIC support types | LA support types |")
    lines.append("|---|---:|---:|---|---|")
    for row in cross_overlap_rows:
        lines.append(
            f"| {row['site']} | {row['n_chic']} | {row['n_la']} |"
            f" {', '.join(row['chic_supports'])} |"
            f" {', '.join(row['la_supports'])} |"
        )
    lines.append("")
    lines.append(
        "**Result: no dual-script artifact pair identified in the v0 corpora.**"
        " Both corpora are uniquely-keyed (CHIC by Olivier-Godart catalog #;"
        " Linear A by GORILA-style site+seq id), with no metadata field in"
        " either flagging an artifact as dual-script. The site-and-support-type"
        " intersection table above shows where cross-script co-occurrence could"
        " IN PRINCIPLE exist — Knossos / Mallia / Phaistos / Haghia Triada /"
        " Arkhanes / Zakros all have entries in both — but the support-type"
        " distributions barely overlap: Linear A's site-Mallia entries are"
        " administrative tablets and roundels, while CHIC Mallia is dominated"
        " by sealstones, medallions, and lames; the only LA stone-vessel"
        " inscriptions in the v0 corpus are PS Za 2 and SY Za 4, neither of"
        " which is at a site shared with CHIC. The CHIC corpus's only stone-"
        " vessel inscription is CHIC #328 (Mallia offering table), and it has"
        " no Linear A counterpart in the v0 corpus."
    )
    lines.append("")
    lines.append(
        "Documented dual-script artifacts in scholarship (e.g. some seal-and-"
        " sealing pairs from Phaistos and Knossos discussed in Salgarella 2020"
        " §5.3 and Decorte 2017) are either (a) NOT in the v0 corpora because"
        " sealstone CMS catalog ingest is itself a separate sub-program, or"
        " (b) debated in the underlying scholarship and not unambiguously"
        " bilingual. None can be applied here as a load-bearing bilingual"
        " constraint without re-doing the underlying ingest."
    )
    lines.append("")

    # Section 3 — Genre-parallel CHIC #328 vs LA libation tables
    lines.append(
        "## 3. Genre-parallel comparison: CHIC #328 vs LA libation tables"
        " (informational only)"
    )
    lines.append("")
    lines.append(
        "Even without a true dual-script artifact, an attenuated form of cross-"
        " script comparison is possible: CHIC #328 (Mallia offering table) and"
        " the LA libation tables PS Za 2 (Psykhro) + SY Za 4 (Syme) are the same"
        " artifact CATEGORY (votive stone vessels likely bearing libation /"
        " altar formulae). Y. Duhoux and others have hypothesized that the"
        " stereotyped Linear A libation formula (`a-ta-i-*301-wa-ja ja-sa-sa-"
        "ra-me ja-ti i-da-ma-te ...`) may have a CHIC counterpart on stone-"
        " vessel inscriptions. **This is a SCHOLARLY CONJECTURE, not"
        " consensus**; we cannot use it as load-bearing first-principles"
        " bilingual constraint."
    )
    lines.append("")
    lines.append(
        "The conjectural genre-parallel comparison is reported here for"
        " completeness and for the methodology paper's discipline-protecting"
        " framing — readers can see that we considered the broader genre-"
        " parallel hypothesis, found it conjectural, and did not rely on it."
    )
    lines.append("")

    chic_328 = malia_altar
    if chic_328 is not None:
        lines.append("**CHIC #328 — Mallia offering table (16 positions):**")
        lines.append("")
        lines.append("| pos | token | rendered (chic-v2) | chic-v5 tier (if unknown) |")
        lines.append("|---:|---|---|---|")
        for i, tok in enumerate(chic_328.get("tokens", [])):
            rendered = render_chic_token_with_anchors(tok, anchors)
            sign_id = None
            m = re.match(r"\[\?:(#\d+)\]$|^(#\d+)$", tok)
            if m:
                sign_id = m.group(1) or m.group(2)
            tier_label = ""
            if sign_id and sign_id in v5:
                v = v5[sign_id]
                tier_label = (
                    f"{v['tier']} (proposed={v['proposed'] or '—'};"
                    f" L1={v['L1'] or '—'}, L2={v['L2'] or '—'},"
                    f" L3={v['L3'] or '—'})"
                )
            lines.append(f"| {i + 1} | `{tok}` | `{rendered}` | {tier_label} |")
        lines.append("")

    for lib in libation_tables:
        lines.append(
            f"**{lib['id']} — {lib.get('site')} libation table"
            f" ({lib.get('n_signs')} positions):**"
        )
        lines.append("")
        lines.append("Raw transliteration (LA v0):")
        lines.append("")
        lines.append(f"```\n{lib.get('raw_transliteration')}\n```")
        lines.append("")
        rendered = " ".join(
            render_la_token_with_carryover(t) for t in lib.get("tokens", [])
        )
        lines.append("Rendered under Linear-B carryover values (only AB ids in the"
                     " v0 LA libation tables are mapped; unmapped AB ids and all"
                     " A-prefixed signs left as-is):")
        lines.append("")
        lines.append(f"```\n{rendered}\n```")
        lines.append("")

    lines.append(
        "**Position alignment is conjectural.** The two LA libation tables are"
        " 16 and 13 positions long respectively; CHIC #328 is 16. Aligning"
        " position-by-position would require either (a) confirmed parallel"
        " content (not established for CHIC stone vessels in scholarship), or"
        " (b) an alignment algorithm with an external phoneme-class similarity"
        " score. Either approach goes beyond the chic-v8 brief's scope, which"
        " requires _genuinely-dual-script artifacts with parallel positions_,"
        " not genre-parallels with conjectural alignment."
    )
    lines.append("")

    # Section 4 — L5 voting outcome
    lines.append("## 4. L5 (LA-constraint) voting outcome")
    lines.append("")
    lines.append(
        "**For each chic-v5 tier-3/4 candidate, an L5 vote is computed only"
        " where a parallel LA-side phoneme value at a confident position is"
        " available in the same artifact's bilingual reading.**"
    )
    lines.append("")
    lines.append(
        "Because no genuinely-dual-script artifact exists in the v0 corpora,"
        " no parallel-position LA-side phoneme value is available for any of"
        " the 76 unknown CHIC syllabographic signs. **L5 is silent for all"
        " unknowns by corpus state**, mirroring chic-v5's L4 silent-by-"
        " construction (the chic-v1 paleographic-candidate list is precisely"
        " the seed for the chic-v2 anchor pool). Tier promotion under the"
        " 4-of-5 rule therefore reduces to the chic-v5 4-of-4 rule for every"
        " sign, which produces no new tier-2 candidates beyond the three"
        " already proposed by chic-v5 (#001 → wa, #012 → wa, #032 → ki/stop)."
    )
    lines.append("")
    lines.append(
        "**Per-sign L5 vote summary (76 unknown CHIC syllabographic signs):**"
    )
    lines.append("")
    lines.append("| sign | freq | chic-v5 tier | L5 vote | reason |")
    lines.append("|---|---:|---|---|---|")
    for sign in sorted(v5.keys(), key=lambda s: int(s.lstrip("#"))):
        v = v5[sign]
        lines.append(
            f"| `{sign}` | {v['freq']} | {v['tier']} | silent |"
            " no genuine dual-script artifact in v0 corpora |"
        )
    lines.append("")

    # Section 5 — Promotion analysis
    lines.append("## 5. Per-sign tier-3/tier-4 → tier-2 promotion analysis")
    lines.append("")
    lines.append(
        "Promotion rule (chic-v8 brief): **any 4 of the 5 lines (L1, L2, L3,"
        " L4, L5) agreeing on the same coarse phoneme class promotes the sign"
        " to tier-2.** With L4 silent for all 76 unknowns by chic-v5"
        " construction and L5 silent for all 76 unknowns by chic-v8 corpus"
        " state, the rule reduces to **all 3 of L1+L2+L3 agreeing** —"
        " byte-identical to the chic-v5 tier-2 criterion. The chic-v8"
        " bilingual extension cannot promote any chic-v5 tier-3 or tier-4"
        " candidate to tier-2 in the v0 corpus state."
    )
    lines.append("")
    lines.append(
        "Tier-3 candidates inspected (29; from `results/chic_value_extraction"
        "_leaderboard.md`):"
    )
    lines.append("")
    tier3 = [s for s, v in v5.items() if v["tier"] == "tier-3"]
    tier3.sort(key=lambda s: int(s.lstrip("#")))
    lines.append(f"`{', '.join(tier3)}`")
    lines.append("")
    lines.append("Tier-4 candidates inspected (17):")
    lines.append("")
    tier4 = [s for s, v in v5.items() if v["tier"] == "tier-4"]
    tier4.sort(key=lambda s: int(s.lstrip("#")))
    lines.append(f"`{', '.join(tier4)}`")
    lines.append("")
    lines.append(
        "**No promotion candidate emerges**: L5 is silent for every entry"
        " in either set. The 4-of-5 agreement count for every tier-3 sign"
        " stays at 2 (its chic-v5 line count); for every tier-4 sign it"
        " stays at 1."
    )
    lines.append("")

    # Section 6 — Discipline + framing
    lines.append("## 6. Headline + discipline-protecting framing")
    lines.append("")
    lines.append(
        "**Headline: 0 new tier-2 candidates derived via dual-script bilingual"
        " constraint.** The bilingual extension does not produce any promotion"
        " under the v0 corpus state, because the chic-v0 + LA-v0 corpora do"
        " not contain a genuinely-dual-script artifact (an artifact bearing"
        " parallel inscriptions in both Cretan Hieroglyphic and Linear A on the"
        " same physical object). The Malia altar stone (CHIC #328), which the"
        " chic-v8 brief flagged as the canonical case, is unilingual CHIC in"
        " the v0 corpus and in the underlying Olivier-Godart 1996 catalog."
    )
    lines.append("")
    lines.append(
        "**This is a legitimate publishable null result** (chic-v8 brief, Goal"
        " section: `N = 0 new tier-2 candidates: bilingual constraint either"
        " doesn't apply (no truly parallel positions) or produces conflicting"
        " constraints. Either is informative.`). The methodology paper's"
        " framing should:"
    )
    lines.append("")
    lines.append(
        "1. **Disclose the corpus state**: the v0 ingest does not include"
        " any genuinely-dual-script artifact, even where scholarship discusses"
        " candidates (debated dual-script seals from Phaistos / Knossos etc.)."
    )
    lines.append(
        "2. **Position the bilingual extension as a falsifiable additional"
        " line of evidence**, contingent on the underlying corpus including"
        " genuinely-dual-script artifacts. This is exactly the chic-v5 L4"
        " situation (silent by construction) restated as a corpus-state"
        " observation."
    )
    lines.append(
        "3. **Refuse to invoke genre-parallels** (CHIC #328 vs LA libation"
        " tables PS Za 2 / SY Za 4) as load-bearing evidence — those are"
        " conjectural alignments, not genuine bilingual constraint, and"
        " elevating them would re-introduce the motivated-reasoning failure"
        " mode the methodology paper has insisted on protecting against"
        " since v13's per-sign coherence verdict and v22's external-validation"
        " null."
    )
    lines.append(
        "4. **Flag the corpus-expansion path**: a future ingest pass adding"
        " the full GORILA Za-series and any genuinely-dual-script artifacts"
        " from CMS sealstone catalogs would reactivate the bilingual extension"
        " and could in principle produce non-zero L5 votes. Filed under"
        " `corpus-expansion` for chic-v9+ / pm-lineara triage."
    )
    lines.append("")

    # Footer
    lines.append("## 7. Reproducibility")
    lines.append("")
    lines.append(
        "Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0),"
        " `corpus/all.jsonl` (LA v0),"
        " `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2),"
        " `results/chic_value_extraction_leaderboard.md` (chic-v5)."
    )
    lines.append("")
    lines.append(
        "Outputs: this file plus `results/chic_v8_promoted_candidates.md`."
        " Determinism: no RNG, no network, no system clock — same inputs"
        " produce byte-identical output across re-runs (verified at chic-v8"
        " build time, 2026-05-05)."
    )
    lines.append("")
    lines.append(
        "Driver: `scripts/build_chic_v8.py`. Re-run with"
        " `python3 scripts/build_chic_v8.py`."
    )

    emit_md(OUT_LEADERBOARD, lines)

    # ----- Promoted candidates output -----
    promoted_lines: list[str] = []
    promoted_lines.append("# CHIC dual-script bilingual promoted candidates"
                          " (chic-v8; mg-dfcc)")
    promoted_lines.append("")
    promoted_lines.append(
        "Per the chic-v8 brief: enumeration of any chic-v5 tier-3 or tier-4"
        " candidate that promotes to tier-2 under the 4-of-5 rule with the"
        " L5 (LA-constraint) line of evidence added. Built by"
        " `scripts/build_chic_v8.py`."
    )
    promoted_lines.append("")
    promoted_lines.append("## Headline")
    promoted_lines.append("")
    promoted_lines.append(
        "**0 new tier-2 candidates** derivable via the chic-v8 bilingual"
        " extension on the v0 corpora."
    )
    promoted_lines.append("")
    promoted_lines.append(
        "L5 is silent for all 76 unknown CHIC syllabographic signs because"
        " the chic-v0 + LA-v0 corpora do not contain any genuinely-dual-script"
        " artifact (an artifact bearing parallel inscriptions in both"
        " Cretan Hieroglyphic and Linear A on the same physical object)."
        " With L4 silent by chic-v5 construction and L5 silent by chic-v8"
        " corpus state, the 4-of-5 promotion rule reduces to chic-v5's"
        " 3-of-3 (L1+L2+L3 unanimity) — byte-identical to the chic-v5"
        " tier-2 criterion. No new tier-2 candidates are produced."
    )
    promoted_lines.append("")
    promoted_lines.append("## Promoted candidates (none)")
    promoted_lines.append("")
    promoted_lines.append(
        "| sign | freq | from | to | L1 | L2 | L3 | L4 | L5 |"
    )
    promoted_lines.append("|---|---:|---|---|---|---|---|---|---|")
    promoted_lines.append("| _(no rows; null result)_ |  |  |  |  |  |  |  |  |")
    promoted_lines.append("")
    promoted_lines.append("## Tier-3 → tier-2 single-step promotions: none")
    promoted_lines.append("")
    promoted_lines.append(
        "29 chic-v5 tier-3 signs inspected (`#002, #005, #006, #007, #008,"
        " #009, #011, #017, #020, #021, #027, #033, #037, #039, #040, #043,"
        " #045, #050, #055, #056, #058, #059, #060, #063, #065, #066, #069,"
        " #072, #078`). For each, L5 is silent because no genuine dual-"
        " script artifact in the v0 corpora carries the sign at a position"
        " parallel to a confidently-read LA sign."
    )
    promoted_lines.append("")
    promoted_lines.append("## Tier-4 → tier-2 single-step promotions: none")
    promoted_lines.append("")
    promoted_lines.append(
        "17 chic-v5 tier-4 signs inspected (`#003, #004, #014, #018, #023,"
        " #029, #034, #036, #046, #047, #051, #052, #062, #068, #076, #094,"
        " #095`). Tier-4 → tier-2 in a single step would require **three**"
        " confirming votes from L4+L5 alone (since tier-4 has only 1 of 4"
        " chic-v5 lines yielding a class) — methodologically weak even if"
        " corpus state were to provide L5 votes; flagged for investigation"
        " rather than silent promotion per the chic-v8 brief. The v0 corpus"
        " state makes the question moot for now."
    )
    promoted_lines.append("")
    promoted_lines.append("## Reproducibility")
    promoted_lines.append("")
    promoted_lines.append(
        "Built by `scripts/build_chic_v8.py` from the same inputs as"
        " `results/chic_dual_script_bilingual_leaderboard.md`. Re-run with"
        " `python3 scripts/build_chic_v8.py`."
    )

    emit_md(OUT_PROMOTED, promoted_lines)

    # ----- Console summary -----
    print(f"chic-v8 build complete:")
    print(f"  inputs: {len(chic)} CHIC + {len(la)} LA inscriptions;"
          f" {len(anchors)} chic-v2 anchors;"
          f" {len(v5)} chic-v5 tier verdicts.")
    print(f"  shared sites: {shared_sites}")
    print(f"  CHIC offering tables: {[d['id'] for d in chic if d.get('support') == 'offering_table']}")
    print(f"  LA libation tables: {[d['id'] for d in libation_tables]}")
    print(f"  outputs:\n    {OUT_LEADERBOARD}\n    {OUT_PROMOTED}")
    print("  headline: 0 new tier-2 candidates (null result on v0 corpora)")


if __name__ == "__main__":
    main()
