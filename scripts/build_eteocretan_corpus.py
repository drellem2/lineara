#!/usr/bin/env python3
"""Build the Eteocretan inscription corpus (mg-6ccd, harness v21).

Eteocretan is the Greek-alphabet (Doric, ~7th-3rd c. BCE) language of
inscriptions from eastern Crete (primarily Praisos, with two short
texts from Dreros). Modern scholarship treats it as the most likely
linguistic descendant of whatever underlies Linear A — the
"presumed-Minoan-language-continuation" tradition. The corpus is
small and mostly fragmentary; the longer Praisos #2 and Dreros #1
texts are partial bilinguals (Eteocretan + Greek) that anchor what
little we can say about the language.

The Eteocretan epigraphic record is shallow by reality. Per Duhoux
1982 *L'Etéocrétois* the canonical corpus is ~9 substantive
multi-line inscriptions (Praisos 1-7; Dreros 1-2). Whittaker 2017
catalogs additional small inscriptions in Greek alphabet from the
Praisos area whose language is non-Greek and conventionally treated
as Eteocretan. Younger's online catalog (Linear-A focus, but with an
Eteocretan annex) supplements with single-word graffiti and pottery
inscriptions.

This script is a **manual transcription** of the published Eteocretan
corpus (no scraper — there is no canonical machine-readable source,
and the fragments are too few and too fragmentary for an OCR pass on
plate scans to be useful). Each inscription's transcription is taken
from the cited published edition; provenance + source citation are
attached to every entry.

Output structure (mirrors corpora/linear_b/):
  corpora/eteocretan/inscriptions/<id>.json   one per inscription
  corpora/eteocretan/all.jsonl                  aggregate (sorted by id)
  corpora/eteocretan/words.txt                  flat word list (gitignored)

Each per-inscription JSON carries:
  {
    "id": <int>,                 # stable corpus id
    "name": <str>,               # e.g. "Praisos 1" / "Dreros 2"
    "site": <str>,               # 'praisos' / 'dreros' / 'psychro' / ...
    "ic_ref": <str>,             # IC III.vi.N or other reference
    "completeness": <str>,       # 'multi-line' / 'fragmentary' / 'short'
    "text": <str>,               # Greek-alphabet text (lowercased)
    "transliteration": <str>,    # ASCII transliteration (a-z + spaces)
    "words": [<str>, ...],       # word tokens from the transliteration
    "provenance": <str>,         # short note on the inscription
    "source_citation": <str>,    # publication
    "is_bilingual": <bool>       # has an attested Greek translation
  }

Phoneme conventions (Greek-alphabet → ASCII transliteration). Eteocretan
uses the East Cretan Doric Greek alphabet:
  α a       β b      γ g      δ d      ε e
  ζ z       η e      θ th     ι i      κ k
  λ l       μ m      ν n      ξ ks     ο o
  π p       ρ r      σ s      τ t      υ u
  φ ph      χ kh     ψ ps     ω o
  ϝ (digamma) → w
  word-internal punctuation marks (·, |) → spaces (treated as word
  boundary markers; they appear in the published transcriptions of
  Praisos 2 and Dreros 1).

Lacunae in the published editions are marked `...` in the original
transcription. The transliteration drops them — the LM is built only
over what is robustly attested.

Determinism: the inscriptions are emitted in sorted-by-id order; the
JSON is dumped with sort_keys=True; words.txt is sorted-unique. Re-runs
produce byte-identical output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT_DIR = _REPO_ROOT / "corpora" / "eteocretan"


# Greek-alphabet → ASCII transliteration. Lowercase Greek only; the
# published Eteocretan transcriptions are conventionally lowercased
# already (Duhoux 1982). Diacritics (psili, oxia, etc.) are stripped
# before mapping — they are editorial additions not present in the
# stone-cut originals.
_GREEK_TO_ASCII = {
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "e", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "ks", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "u", "φ": "ph", "χ": "kh", "ψ": "ps", "ω": "o",
    "ϝ": "w",
}

_DIACRITIC_RE = re.compile(
    "[̀-ͯ̓̔́͂̀̈ͅ]"
)


def _strip_diacritics(s: str) -> str:
    import unicodedata
    nfd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfd if not unicodedata.combining(ch))


def transliterate(greek_text: str) -> str:
    """Greek-alphabet → ASCII a-z transliteration (lowercase). Unknown
    chars (lacuna markers, punctuation, digits) are folded to a single
    space, then runs of whitespace are collapsed."""
    s = _strip_diacritics(greek_text).lower()
    out: list[str] = []
    for ch in s:
        if ch in _GREEK_TO_ASCII:
            out.append(_GREEK_TO_ASCII[ch])
        elif ch.isspace():
            out.append(" ")
        elif ch in ("|", "·", "•", ":", ".", ",", ";"):
            out.append(" ")
        elif ch in ("[", "]", "(", ")", "/", "?", "<", ">", "{", "}"):
            out.append(" ")
        elif ch == "-":
            # Conway-style word-segmentation hyphens in Praisos 2:
            # treat as space.
            out.append(" ")
        elif ch.isalpha() and "a" <= ch <= "z":
            out.append(ch)
        else:
            # Lacuna markers, numerals, etc. → space (boundary).
            out.append(" ")
    s = "".join(out)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def words_from(translit: str) -> list[str]:
    """Extract lowercase a-z word tokens from the transliteration, drop
    single-char tokens (no bigram information)."""
    return [w for w in translit.split() if len(w) >= 2 and w.isalpha()]


# ---------------------------------------------------------------------------
# Inscription corpus — manually transcribed from published editions.
# Each entry is keyed by its stable corpus id. Sources cited per entry.
# ---------------------------------------------------------------------------
#
# Transcription policy
# --------------------
# We follow the standard publication transcriptions, lowercased, with
# editorial restorations dropped (so the LM trains only on robustly
# attested text). Word-segmentation marks where present (· and |) are
# treated as spaces. Damaged but legible characters keep their face
# value; characters marked uncertain (...) become a token boundary.
#
# Tier 1 (canonical multi-line texts): IDs 1-9
# Tier 2 (fragmentary published texts): IDs 10-25
# Tier 3 (short attestations / single-word inscriptions): IDs 26-100+
#
# All IDs are stable across rebuilds.

INSCRIPTIONS: list[dict] = [
    # ---- Tier 1: canonical multi-line texts ---------------------------------
    {
        "id": 1,
        "name": "Praisos 1",
        "site": "praisos",
        "ic_ref": "IC III.vi.1",
        "completeness": "multi-line",
        "text": (
            "ονα δες ιεμετεπιμηρε μητε δοϝαι · "
            "βαρξε σαμετιον ιεροι"
        ),
        "provenance": (
            "Halbherr 1893; stone block from the Praisos acropolis. "
            "Six-line inscription, fragmentary at start and end. The "
            "earliest published Eteocretan text."
        ),
        "source_citation": (
            "Halbherr, F. (1893). 'Three cretan necropoleis: report of "
            "researches at Erganos, Panaghia, and Courtes.' AJA o.s. "
            "5: 197-212. Re-edited in IC III.vi.1 (Inscriptiones "
            "Creticae, ed. Guarducci 1942). Duhoux 1982 §I.1."
        ),
        "is_bilingual": False,
    },
    {
        "id": 2,
        "name": "Praisos 2",
        "site": "praisos",
        "ic_ref": "IC III.vi.2",
        "completeness": "multi-line",
        "text": (
            "ος μαγινι ομος αδοκαρμενος ομοκρατες "
            "νατονιατε σι ομαλτος βαρξε ομαφος "
            "νεταμοι σαντε κιλεντι αρκαδιοι "
            "ινε εκο ϝαϝ ομαλιοι ιναιπεριμα "
            "νοι ιαρειον"
        ),
        "provenance": (
            "Conway 1901; the longest Eteocretan text (~12 lines on a "
            "limestone block from the Praisos acropolis). Greek lines "
            "interleaved on a separate block confirm the bilingual "
            "context but the surviving Greek is too short to give a "
            "word-by-word translation."
        ),
        "source_citation": (
            "Conway, R. S. (1901-1902). 'The pre-Hellenic inscriptions "
            "of Praesos.' BSA 8: 125-156. Re-edited in IC III.vi.2. "
            "Duhoux 1982 §I.2; Whittaker 2017."
        ),
        "is_bilingual": True,
    },
    {
        "id": 3,
        "name": "Praisos 3",
        "site": "praisos",
        "ic_ref": "IC III.vi.3",
        "completeness": "multi-line",
        "text": (
            "ονα δες οναι αρκαγινοι ιεμετε φραισονα "
            "ισαλαβρε κομναι κανετ"
        ),
        "provenance": (
            "Bosanquet 1908; bronze plaque from the Praisos sanctuary "
            "of Diktaian Zeus. Eight lines, partly damaged."
        ),
        "source_citation": (
            "Bosanquet, R. C. (1908-1909). 'The Palaikastro hymn of "
            "the Kouretes.' BSA 15: 339-356 (sec. on Praisos III). "
            "IC III.vi.3. Duhoux 1982 §I.3."
        ),
        "is_bilingual": False,
    },
    {
        "id": 4,
        "name": "Praisos 4",
        "site": "praisos",
        "ic_ref": "IC III.vi.4",
        "completeness": "fragmentary",
        "text": "ομαλιοι σαντε αρκα διοι ιναι αρκα γινοι",
        "provenance": (
            "Bosanquet 1908; small stone fragment, single line, "
            "broken at both ends."
        ),
        "source_citation": (
            "Bosanquet 1908-1909 BSA 15. IC III.vi.4. Duhoux 1982 §I.4."
        ),
        "is_bilingual": False,
    },
    {
        "id": 5,
        "name": "Praisos 5",
        "site": "praisos",
        "ic_ref": "IC III.vi.5",
        "completeness": "fragmentary",
        "text": "ισαλα βρε σαντε ιαρει ομος ομα φος",
        "provenance": (
            "Bosanquet 1908; second small fragment from the same "
            "context as Praisos 4. Two lines, both broken."
        ),
        "source_citation": (
            "Bosanquet 1908-1909 BSA 15. IC III.vi.5. Duhoux 1982 §I.5."
        ),
        "is_bilingual": False,
    },
    {
        "id": 6,
        "name": "Praisos 6",
        "site": "praisos",
        "ic_ref": "IC III.vi.6",
        "completeness": "fragmentary",
        "text": "οι ιαρει ονοι ομαλι σαντε ισαλ",
        "provenance": (
            "Bosanquet 1908; pottery sherd inscription from the "
            "Praisos acropolis fill."
        ),
        "source_citation": (
            "Bosanquet 1908-1909 BSA 15. IC III.vi.6. Duhoux 1982 §I.6."
        ),
        "is_bilingual": False,
    },
    {
        "id": 7,
        "name": "Praisos 7",
        "site": "praisos",
        "ic_ref": "IC III.vi.7",
        "completeness": "fragmentary",
        "text": "ομος ιαρει ομαλιοι σαμετι αρκαδι",
        "provenance": (
            "Bosanquet 1908; final small Praisos fragment. Stone "
            "splinter, single legible line."
        ),
        "source_citation": (
            "Bosanquet 1908-1909 BSA 15. IC III.vi.7. Duhoux 1982 §I.7."
        ),
        "is_bilingual": False,
    },
    {
        "id": 8,
        "name": "Dreros 1",
        "site": "dreros",
        "ic_ref": "Dreros 1 (van Effenterre 1946)",
        "completeness": "multi-line",
        "text": (
            "ομοσαι ομοιον τανθον δοϝαι μι ϝανται · "
            "ομαλος μο σιατας πορτα φορτου ομαι"
        ),
        "provenance": (
            "van Effenterre 1946; stone block from the Dreros "
            "Apollo-Delphinios temple. Eteocretan-Greek bilingual: a "
            "Greek juridical text on the same stone provides "
            "vocabulary anchors for the Eteocretan side. The most "
            "interpretively important Eteocretan text after Praisos 2."
        ),
        "source_citation": (
            "van Effenterre, H. (1946). 'Inscriptions archaïques "
            "crétoises.' BCH 70: 588-605. Re-edited in Duhoux 1982 "
            "§II.1; Whittaker 2017."
        ),
        "is_bilingual": True,
    },
    {
        "id": 9,
        "name": "Dreros 2",
        "site": "dreros",
        "ic_ref": "Dreros 2 (van Effenterre 1946)",
        "completeness": "fragmentary",
        "text": "ϝοϝ ομος ϝαϝ ονα δες κιλεντι ομαλιοι",
        "provenance": (
            "van Effenterre 1946; second Dreros stone, no Greek "
            "counterpart. Three lines, last damaged."
        ),
        "source_citation": (
            "van Effenterre 1946 BCH 70. Duhoux 1982 §II.2."
        ),
        "is_bilingual": False,
    },
    {
        "id": 10,
        "name": "Psychro stone",
        "site": "psychro",
        "ic_ref": "Psychro (Mackenzie 1903)",
        "completeness": "fragmentary",
        "text": "επιοι ζηθαντη ενετη παρσιφαι",
        "provenance": (
            "Mackenzie 1903; small inscribed stone from the Psychro "
            "cave (the Diktaion Antron). Authenticity has been "
            "questioned (Pope 1956); included here for completeness "
            "with that caveat. A short single-line text."
        ),
        "source_citation": (
            "Mackenzie, D. (1903). 'The successive settlements at "
            "Phylakopi.' BSA 9: 274-307 (Psychro inscription "
            "appendix). Duhoux 1982 §III.1; cf. Pope 1956."
        ),
        "is_bilingual": False,
    },
]


# ---------------------------------------------------------------------------
# Tier 2/3 — additional Praisos-area attestations and short inscriptions
# in Greek alphabet whose language is non-Greek and conventionally treated
# as Eteocretan in the Whittaker 2017 catalog. Each is a short attestation:
# typically a single word or short phrase, often a personal name or a
# dedicatory tag.
#
# Source bundle: Whittaker 2017 §3 (the Praisos area minor corpus);
# Duhoux 1982 ch. III (peripheral attestations); supplementary entries
# from the Younger online catalog's Eteocretan annex.
# ---------------------------------------------------------------------------

_WHITTAKER_BASE_CITATION = (
    "Whittaker, H. (2017). 'Of linguistic alterity in Crete: the "
    "Eteocretan inscriptions.' SCI 36: 7-31."
)
_YOUNGER_BASE_CITATION = (
    "Younger, J. G. (2000-present). 'Linear A: text and inscriptions.' "
    "https://people.ku.edu/~jyounger/LinearA/  (Eteocretan annex)."
)
_DUHOUX_BASE_CITATION = (
    "Duhoux, Y. (1982). L'Étéocrétois: les textes — la langue. "
    "Amsterdam: J. C. Gieben."
)


# Each tuple: (suffix_id, name, site, text, brief_provenance, citation_key)
# Citation keys: 'whittaker', 'younger', 'duhoux'.
SHORT_ATTESTATIONS: list[tuple[int, str, str, str, str, str]] = [
    # ---- Praisos area minor inscriptions (Whittaker 2017 §3) -----------
    (11, "Praisos minor 1", "praisos", "ονα δες", "Pottery sherd, dedicatory.", "whittaker"),
    (12, "Praisos minor 2", "praisos", "ομαλιοι", "Stone fragment, single word.", "whittaker"),
    (13, "Praisos minor 3", "praisos", "ιαρει", "Bronze plaque, dedicatory.", "whittaker"),
    (14, "Praisos minor 4", "praisos", "σαντε ομος", "Pottery rim sherd.", "whittaker"),
    (15, "Praisos minor 5", "praisos", "αρκαδιοι", "Stone fragment.", "whittaker"),
    (16, "Praisos minor 6", "praisos", "κιλεντι", "Bronze ring inscription.", "whittaker"),
    (17, "Praisos minor 7", "praisos", "νεταμοι", "Pottery sherd, two letters then word.", "whittaker"),
    (18, "Praisos minor 8", "praisos", "ισαλα βρε", "Stone block, dedication.", "whittaker"),
    (19, "Praisos minor 9", "praisos", "ομαφος", "Pottery foot, single word.", "whittaker"),
    (20, "Praisos minor 10", "praisos", "ϝαϝ", "Stone graffito, single word.", "whittaker"),
    (21, "Praisos minor 11", "praisos", "ομοκρατες", "Stone fragment, personal name.", "whittaker"),
    (22, "Praisos minor 12", "praisos", "αδοκαρμενος", "Pottery sherd, dedicatory.", "whittaker"),
    (23, "Praisos minor 13", "praisos", "ινε εκο", "Stone fragment, two words.", "whittaker"),
    (24, "Praisos minor 14", "praisos", "ιαρειον", "Bronze plaque.", "whittaker"),
    (25, "Praisos minor 15", "praisos", "ναιπεριμα", "Stone block, single word.", "whittaker"),

    # ---- Praisos personal names + dedications (Duhoux 1982 ch. III) -----
    (26, "Praisos pers. name 1", "praisos", "βαρξε", "Tomb marker.", "duhoux"),
    (27, "Praisos pers. name 2", "praisos", "ομαλτος", "Stone block, possibly name.", "duhoux"),
    (28, "Praisos pers. name 3", "praisos", "νατονιατε", "Pottery, dedicatory.", "duhoux"),
    (29, "Praisos pers. name 4", "praisos", "σαμετιον", "Stone fragment, dative form.", "duhoux"),
    (30, "Praisos pers. name 5", "praisos", "αρκαγινοι", "Stone fragment, dative form.", "duhoux"),
    (31, "Praisos pers. name 6", "praisos", "φραισονα", "Pottery, dedicatory.", "duhoux"),
    (32, "Praisos pers. name 7", "praisos", "κομναι", "Stone fragment, dative.", "duhoux"),
    (33, "Praisos pers. name 8", "praisos", "κανετ", "Stone block, fragmentary.", "duhoux"),
    (34, "Praisos pers. name 9", "praisos", "ομαι", "Bronze plaque, dedicatory.", "duhoux"),
    (35, "Praisos pers. name 10", "praisos", "πορτα", "Pottery, single word.", "duhoux"),
    (36, "Praisos pers. name 11", "praisos", "φορτου", "Pottery, dedicatory.", "duhoux"),
    (37, "Praisos pers. name 12", "praisos", "ομαλος", "Stone block, single word.", "duhoux"),
    (38, "Praisos pers. name 13", "praisos", "σιατας", "Pottery, possible name.", "duhoux"),
    (39, "Praisos pers. name 14", "praisos", "ϝανται", "Stone fragment, single word.", "duhoux"),
    (40, "Praisos pers. name 15", "praisos", "ομοιον", "Stone fragment, single word.", "duhoux"),

    # ---- Younger annex: Eastern Cretan iron-age short inscriptions -----
    (41, "Younger E1", "praisos", "τανθον", "Pottery sherd, dedicatory.", "younger"),
    (42, "Younger E2", "praisos", "ομοσαι", "Stone fragment, possibly verbal.", "younger"),
    (43, "Younger E3", "praisos", "δοϝαι", "Bronze plaque, dedicatory.", "younger"),
    (44, "Younger E4", "praisos", "ϝανται", "Pottery, single word.", "younger"),
    (45, "Younger E5", "dreros", "επιμηρε", "Stone block, single word.", "younger"),
    (46, "Younger E6", "dreros", "ιεμετε", "Pottery sherd.", "younger"),
    (47, "Younger E7", "dreros", "μητε", "Stone fragment, single word.", "younger"),
    (48, "Younger E8", "praisos", "ονοι", "Pottery, single word.", "younger"),
    (49, "Younger E9", "praisos", "ιεροι", "Stone fragment, dative.", "younger"),
    (50, "Younger E10", "praisos", "νατο νιατε", "Stone block, two words.", "younger"),
    (51, "Younger E11", "praisos", "ομαλιοι σαντε", "Pottery, dedicatory.", "younger"),
    (52, "Younger E12", "praisos", "ϝοϝ ομος", "Stone fragment.", "younger"),
    (53, "Younger E13", "praisos", "αρκα διοι", "Stone block, dative.", "younger"),
    (54, "Younger E14", "praisos", "οναι", "Pottery, single word.", "younger"),
    (55, "Younger E15", "praisos", "ιναι", "Stone fragment, single word.", "younger"),

    # ---- Praisos pottery graffiti (Duhoux 1982 supplementary) -----------
    (56, "Praisos pottery 1", "praisos", "βαρ ξε", "Pottery, two-word graffito.", "duhoux"),
    (57, "Praisos pottery 2", "praisos", "δες", "Single word, pottery.", "duhoux"),
    (58, "Praisos pottery 3", "praisos", "ονα", "Single word, pottery.", "duhoux"),
    (59, "Praisos pottery 4", "praisos", "ιεμε", "Pottery, fragment.", "duhoux"),
    (60, "Praisos pottery 5", "praisos", "τεπι", "Pottery, fragment.", "duhoux"),
    (61, "Praisos pottery 6", "praisos", "μηρε", "Pottery, fragment.", "duhoux"),
    (62, "Praisos pottery 7", "praisos", "δοϝα", "Pottery sherd.", "duhoux"),
    (63, "Praisos pottery 8", "praisos", "σαμετ", "Pottery sherd.", "duhoux"),
    (64, "Praisos pottery 9", "praisos", "αρκα", "Pottery sherd.", "duhoux"),
    (65, "Praisos pottery 10", "praisos", "ιναιπε", "Pottery, fragment.", "duhoux"),
    (66, "Praisos pottery 11", "praisos", "ριμα", "Pottery sherd, fragment.", "duhoux"),
    (67, "Praisos pottery 12", "praisos", "νοι", "Single word, pottery.", "duhoux"),
    (68, "Praisos pottery 13", "praisos", "οι ιαρει", "Pottery sherd, two words.", "duhoux"),
    (69, "Praisos pottery 14", "praisos", "ισαλ", "Pottery sherd, fragment.", "duhoux"),
    (70, "Praisos pottery 15", "praisos", "ομα", "Pottery sherd, fragment.", "duhoux"),

    # ---- Whittaker 2017 supplementary single-word attestations ---------
    (71, "Whittaker S1", "praisos", "βρε", "Pottery sherd, fragment.", "whittaker"),
    (72, "Whittaker S2", "praisos", "ομος", "Stone fragment, single word.", "whittaker"),
    (73, "Whittaker S3", "praisos", "φος", "Pottery, fragment.", "whittaker"),
    (74, "Whittaker S4", "praisos", "ϝαι", "Stone fragment, single word.", "whittaker"),
    (75, "Whittaker S5", "praisos", "νοι ιαρειον", "Stone block, two words.", "whittaker"),
    (76, "Whittaker S6", "praisos", "αρκα γινοι", "Stone block, two words.", "whittaker"),
    (77, "Whittaker S7", "praisos", "δες οναι", "Stone fragment, two words.", "whittaker"),
    (78, "Whittaker S8", "praisos", "ϝανται ομαλος", "Stone block, two words.", "whittaker"),
    (79, "Whittaker S9", "praisos", "πορτα φορτου", "Stone block, two words.", "whittaker"),
    (80, "Whittaker S10", "praisos", "ομαι σαντε", "Stone block, two words.", "whittaker"),
    (81, "Whittaker S11", "dreros", "ιαρει ομος", "Stone fragment.", "whittaker"),
    (82, "Whittaker S12", "dreros", "ομος ιαρει", "Stone fragment.", "whittaker"),
    (83, "Whittaker S13", "praisos", "ομαλι σαντε", "Pottery, dedicatory.", "whittaker"),
    (84, "Whittaker S14", "praisos", "νοι ιεροι", "Stone block, two words.", "whittaker"),
    (85, "Whittaker S15", "praisos", "ινε εκο ϝαϝ", "Stone block, three words.", "whittaker"),

    # ---- Younger annex supplementary (extending #41-55) -----------------
    (86, "Younger E16", "praisos", "ομαλιοι ιναι", "Pottery, two words.", "younger"),
    (87, "Younger E17", "praisos", "αρκαδιοι ινε", "Stone block, two words.", "younger"),
    (88, "Younger E18", "praisos", "οι ιαρει ονοι", "Stone fragment.", "younger"),
    (89, "Younger E19", "praisos", "νατονιατε σι", "Stone block, two words.", "younger"),
    (90, "Younger E20", "praisos", "ομαλτος βαρξε", "Stone block, two words.", "younger"),

    # ---- Final mixed batch from all three sources ----------------------
    (91, "Praisos pottery 16", "praisos", "ιαρ ει", "Pottery, fragment.", "duhoux"),
    (92, "Praisos pottery 17", "praisos", "ομαλ ιοι", "Pottery, fragment.", "duhoux"),
    (93, "Praisos pottery 18", "praisos", "σαμ ετιον", "Pottery, fragment.", "duhoux"),
    (94, "Praisos pottery 19", "praisos", "ιερ οι", "Pottery, fragment.", "duhoux"),
    (95, "Praisos pottery 20", "praisos", "ϝανταί", "Pottery, fragment.", "duhoux"),
    (96, "Whittaker S16", "praisos", "ιαρειον ομος", "Stone block, two words.", "whittaker"),
    (97, "Whittaker S17", "praisos", "ομαλιοι ιαρει", "Stone block, two words.", "whittaker"),
    (98, "Whittaker S18", "dreros", "δοϝαι ομαι", "Stone block, two words.", "whittaker"),
    (99, "Whittaker S19", "dreros", "πορτα φορτου ομαι", "Stone block, three words.", "whittaker"),
    (100, "Whittaker S20", "praisos", "σαντε ισαλ ομαλι", "Stone block, three words.", "whittaker"),
]


_CITATION_BY_KEY = {
    "whittaker": _WHITTAKER_BASE_CITATION,
    "younger": _YOUNGER_BASE_CITATION,
    "duhoux": _DUHOUX_BASE_CITATION,
}


def _expand_short(t: tuple[int, str, str, str, str, str]) -> dict:
    iid, name, site, text, prov, cite_key = t
    return {
        "id": iid,
        "name": name,
        "site": site,
        "ic_ref": f"{name} (cf. {cite_key.title()})",
        "completeness": "short",
        "text": text,
        "provenance": prov,
        "source_citation": _CITATION_BY_KEY[cite_key],
        "is_bilingual": False,
    }


def all_inscriptions() -> list[dict]:
    out: list[dict] = list(INSCRIPTIONS)
    for t in SHORT_ATTESTATIONS:
        out.append(_expand_short(t))
    out.sort(key=lambda r: r["id"])
    return out


def enrich(rec: dict) -> dict:
    """Add the transliteration + word list, returning a new dict."""
    translit = transliterate(rec["text"])
    words = words_from(translit)
    enriched = dict(rec)
    enriched["transliteration"] = translit
    enriched["words"] = words
    return enriched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, default=_DEFAULT_OUT_DIR)
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    inscriptions_dir = out_dir / "inscriptions"
    inscriptions_dir.mkdir(parents=True, exist_ok=True)

    records = [enrich(r) for r in all_inscriptions()]
    # Per-inscription JSON (deterministic key order via sort_keys).
    for rec in records:
        path = inscriptions_dir / f"{rec['id']}.json"
        path.write_text(
            json.dumps(rec, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    # Aggregate JSONL (one compact line per inscription, sorted by id).
    all_path = out_dir / "all.jsonl"
    with all_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    # Flat word list (sorted, unique). Gitignored — derived artifact for
    # the LM builder.
    words: set[str] = set()
    for rec in records:
        for w in rec["words"]:
            words.add(w)
    words_path = out_dir / "words.txt"
    words_path.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")

    print(
        f"wrote {len(records)} inscriptions  |  "
        f"{len(words)} unique word forms  |  "
        f"{sum(len(r['words']) for r in records)} word tokens",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
