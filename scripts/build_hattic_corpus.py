#!/usr/bin/env python3
"""Build the Hattic lexical-attestation corpus (mg-7e7d6, specificity probe).

Hattic is the non-Indo-European isolate of Bronze Age central Anatolia,
known only through the Hittite state archives at Ḫattuša: Hattic cult
recitations, Hattic-Hittite bilinguals (CTH 725-745) and Hattic words
and names embedded in Hittite ritual and festival texts. It has no
genealogical relationship to any of the Aegean / old-European pools in
this repo (Aquitanian, Etruscan, Eteocretan, Mycenaean Greek). It is run
through the lineara program as a **specificity probe** (handoff
2026-05-06 §D.3): if the framework PASSes on Hattic as readily as on the
Aegean-adjacent pools, the PASS is evidence of generic structure, not of
substrate affinity. This corpus makes no decipherment claim.

What this corpus is
-------------------
A **manual, lexical** corpus: one record per attested Hattic lexeme,
theonym, or Hattic-area place / personal name, keyed by hand from the
standard scholarly literature (Soysal 2004; Klinger 1996; Kammenhuber
1969; Taracha 2009; del Monte & Tischler 1978; Bischoff 2023; see
``_CITATIONS``). It is NOT a corpus of connected Hattic running text.
Keying continuous passages of the bilinguals requires collating the
printed editions line by line, which the compiler could not do; keying
them from memory would fabricate text. Lexical entries are the
defensible unit.

Every record carries a confidence ``tier``:
  * ``A`` — core, widely cited Hattic lexeme or theonym whose Hattic
    status and reading are uncontroversial in the literature.
  * ``B`` — Hattic attribution conventional but argued (Hittite words of
    probable Hattic origin, Hattic-area toponyms / personal names whose
    linguistic layer is inferred from geography and cult context, or a
    recent single-author proposal).

The forms have NOT been collated against the printed editions; the
per-record citation names the work that standardly treats the form.
See ``corpora/hattic.README.md``.

Normalisation (applied identically to corpus and pool)
------------------------------------------------------
Hattic "phonemes" are a transliteration convention over Hittite scribal
cuneiform, not a phonetic transcription. ``normalise`` maps the cited
scholarly form to lowercase ASCII a-z:
  * diacritics stripped: š → s (s/š merged), ḫ → h, ē → e;
  * morpheme hyphens removed (``le-binu`` → ``lebinu``);
  * stop voicing merged to the voiceless series (b → p, d → t, g → k):
    cuneiform does not reliably write Hattic stop voicing;
  * the labial "f" of some modern citations (Wikipedia's ``fur``,
    ``findu``) is written with the cuneiform WA-series and maps to w;
  * plene vowel runs collapsed (``aa`` → ``a``);
  * consonant gemination retained as conventionally cited.

Output (mirrors corpora/eteocretan/):
  corpora/hattic/inscriptions/<id>.json   one per lexical record
  corpora/hattic/all.jsonl                aggregate (sorted by id)
  corpora/hattic/words.txt                flat word list (gitignored)

Determinism: records sorted by id; JSON dumped with sort_keys=True;
words.txt sorted-unique. Re-runs produce byte-identical output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT_DIR = _REPO_ROOT / "corpora" / "hattic"


_CITATIONS: dict[str, str] = {
    "soysal": (
        "Soysal, O. (2004). Hattischer Wortschatz in hethitischer "
        "Textüberlieferung. HdO I/74. Leiden: Brill."
    ),
    "klinger": (
        "Klinger, J. (1996). Untersuchungen zur Rekonstruktion der "
        "hattischen Kultschicht. StBoT 37. Wiesbaden: Harrassowitz."
    ),
    "kammenhuber": (
        "Kammenhuber, A. (1969). 'Hattisch.' In Altkleinasiatische "
        "Sprachen, HdO I/2.1-2/2: 428-546. Leiden: Brill."
    ),
    "taracha": (
        "Taracha, P. (2009). Religions of Second Millennium Anatolia. "
        "Dresdner Beiträge zur Hethitologie 27. Wiesbaden: Harrassowitz."
    ),
    "rgtc": (
        "del Monte, G. F. & Tischler, J. (1978). Die Orts- und "
        "Gewässernamen der hethitischen Texte. RGTC 6. Wiesbaden: "
        "Reichert."
    ),
    "bischoff": (
        "Bischoff, A. M. (2023). 'Some new Hattian-Hittite "
        "correspondences from the quasi-bilingual text of CTH 733.' "
        "Hungarian Assyriological Review 4: 95-109 (CC BY-NC 4.0)."
    ),
    "dewiki": (
        "'Hattische Sprache', de.wikipedia.org (accessed 2026-10-03), "
        "summarising the morphological analysis of Soysal 2004; forms "
        "cross-checked against Soysal 2004 by citation only."
    ),
}


def _strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfd if not unicodedata.combining(ch))


_VOICING = str.maketrans({"b": "p", "d": "t", "g": "k", "f": "w"})


def normalise(cited: str) -> str:
    """Cited scholarly form → normalised lowercase ASCII (see module
    docstring). Whitespace separates words; everything else non a-z is
    dropped."""
    s = _strip_diacritics(cited).lower()
    s = s.replace("-", "")
    s = s.translate(_VOICING)
    s = re.sub(r"[^a-z\s]", "", s)
    s = re.sub(r"([aeiou])\1+", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def words_from(translit: str) -> list[str]:
    """Word tokens of length >= 2 (single chars carry no bigram)."""
    return [w for w in translit.split() if len(w) >= 2 and w.isalpha()]


# ---------------------------------------------------------------------------
# Lexical records. Tuple: (id, cited_form, category, gloss, tier,
# citation_key, is_bilingual, note). ``is_bilingual`` = the gloss rests on
# a Hattic-Hittite bilingual / quasi-bilingual correspondence.
# IDs are stable across rebuilds.
#   1-29   theonyms (Hattic pantheon in Hittite-archive cult texts)
#   30-59  lexemes (common words, titles, analysed word forms)
#   60-89  Hattic-area toponyms and personal names (onomastics)
# ---------------------------------------------------------------------------

RECORDS: list[tuple[int, str, str, str, str, str, bool, str]] = [
    # ---- theonyms ---------------------------------------------------------
    (1, "Eštan", "theonym", "sun god", "A", "soysal", True,
     "Hattic sun deity; Hittite Ištanu is the loan."),
    (2, "Wurunšemu", "theonym", "sun goddess of Arinna", "A", "taracha", False,
     "Head of the Hattic pantheon; Hittite Arinnitti."),
    (3, "Taru", "theonym", "storm god", "A", "soysal", True,
     "Hattic storm god; equated with Hittite Tarḫunna."),
    (4, "Kašku", "theonym", "moon god", "A", "klinger", True,
     "Protagonist of the bilingual 'Moon that fell from heaven' (CTH 727)."),
    (5, "Wurunkatte", "theonym", "'king of the land', war god", "A", "soysal", True,
     "Compound wur-un 'of the land' + katte 'king'."),
    (6, "Ḫalmašuit", "theonym", "throne goddess", "A", "klinger", True,
     "Hittite-tradition form of Hattic ḫanwašuit 'throne'."),
    (7, "Ḫapantali", "theonym", "tutelary goddess", "A", "taracha", False, ""),
    (8, "Kataḫzipuri", "theonym", "goddess (Hittite Kamrušepa)", "A", "taracha", False, ""),
    (9, "Kait", "theonym", "grain goddess", "A", "taracha", False, ""),
    (10, "Tetešḫapi", "theonym", "'great goddess'", "A", "soysal", False,
     "tete 'great' + šḫap 'god(dess)'."),
    (11, "Šulinkatte", "theonym", "war god", "A", "taracha", False, ""),
    (12, "Telipinu", "theonym", "vegetation / fertility god", "A", "taracha", False,
     "Hattic-origin god of the vanishing-god myth."),
    (13, "Inar", "theonym", "tutelary goddess", "A", "taracha", False,
     "Inar(a) of the Illuyanka myth."),
    (14, "Mezulla", "theonym", "daughter of the sun goddess", "A", "taracha", False, ""),
    (15, "Zintuḫi", "theonym", "granddaughter of the sun goddess", "A", "taracha", False, ""),
    (16, "Ḫašammili", "theonym", "god", "A", "taracha", False, ""),
    (17, "Zilipuri", "theonym", "god", "A", "klinger", False, ""),
    (18, "Wašezzili", "theonym", "god", "A", "klinger", False, ""),
    (19, "Kataḫḫa", "theonym", "goddess 'the queen'", "A", "klinger", False,
     "Deified title; cf. kataḫ 'queen'."),
    (20, "Zaḫpuna", "theonym", "goddess", "B", "taracha", False, ""),
    (21, "Zašḫapuna", "theonym", "chief goddess of Kaštama", "B", "taracha", False, ""),
    (22, "Ištuštaya", "theonym", "fate goddess", "B", "taracha", False,
     "Paired with Papaya in the Hattic-tradition foundation ritual."),
    (23, "Papaya", "theonym", "fate goddess", "B", "taracha", False, ""),
    (24, "Kuzanišu", "theonym", "goddess", "B", "klinger", False, ""),
    (25, "Ḫatepinu", "theonym", "goddess, consort of Telipinu", "B", "taracha", False, ""),
    # ---- lexemes ----------------------------------------------------------
    (30, "katte", "lexeme", "king", "A", "soysal", True, ""),
    (31, "kataḫ", "lexeme", "queen", "A", "soysal", True, ""),
    (32, "pinu", "lexeme", "child", "A", "soysal", True, ""),
    (33, "ašḫap", "lexeme", "god", "A", "soysal", True, ""),
    (34, "wa-šḫap", "lexeme", "gods (collective wa- + šḫap)", "A", "soysal", True, ""),
    (35, "wur", "lexeme", "land", "A", "soysal", True, ""),
    (36, "wur-un", "lexeme", "of the land (genitive -un)", "A", "soysal", True, ""),
    (37, "wel", "lexeme", "house", "A", "soysal", True, ""),
    (38, "windu", "lexeme", "wine", "A", "soysal", True, ""),
    (39, "alep", "lexeme", "tongue, word", "A", "soysal", True, ""),
    (40, "zari", "lexeme", "mortal, man", "A", "soysal", True, ""),
    (41, "wa-zari", "lexeme", "humankind (collective)", "A", "soysal", True, ""),
    (42, "ḫilamar", "lexeme", "temple gate-house", "A", "soysal", True,
     "Hittite ḫilammar is the loan."),
    (43, "tete", "lexeme", "great", "A", "soysal", True, ""),
    (44, "ḫanwašuit", "lexeme", "throne", "A", "soysal", True,
     "Source of the theonym Ḫalmašuit."),
    (45, "tuḫkanti", "lexeme", "crown prince (title)", "B", "kammenhuber", False,
     "Hittite title of probable Hattic origin."),
    (46, "tawananna", "lexeme", "queen (title)", "B", "kammenhuber", False,
     "Hittite royal title of probable Hattic origin."),
    (47, "tabarna", "lexeme", "king (title)", "B", "kammenhuber", False,
     "Hittite royal title (labarna/tabarna) of probable Hattic origin."),
    (48, "ḫalentu", "lexeme", "palace", "B", "kammenhuber", False,
     "Hittite ḫalentu(wa) of probable Hattic origin."),
    (49, "ḫapalki", "lexeme", "iron", "B", "kammenhuber", False,
     "Hittite ḫapalki of probable Hattic origin."),
    (50, "ištarazzil", "lexeme", "earth", "B", "soysal", True, ""),
    (51, "le-binu", "lexeme", "children (le- plural)", "A", "dewiki", False, ""),
    (52, "le-i-binu", "lexeme", "his children", "A", "dewiki", False, ""),
    (53, "le-zuḫ", "lexeme", "cloths", "A", "dewiki", False, ""),
    (54, "le-wae", "lexeme", "implements", "A", "dewiki", False, ""),
    (55, "nuwa", "lexeme", "come (verb stem)", "A", "dewiki", False, ""),
    (56, "taš-te-nuwa", "lexeme", "he should not come", "A", "dewiki", False, ""),
    (57, "šul", "lexeme", "let, leave (verb stem)", "A", "dewiki", False, ""),
    (58, "tu-ḫ-ta-šul", "lexeme", "he let (it) go after him", "A", "dewiki", False, ""),
    (59, "an", "lexeme", "sea", "B", "bischoff", True,
     "Proposed reading replacing earlier †ḫan (CTH 733)."),
    (60, "il", "lexeme", "to prosper", "B", "bischoff", True,
     "Proposed reading replacing earlier †ḫil (CTH 733)."),
    # ---- onomastics (Hattic-area toponyms, personal names) ---------------
    (70, "Ḫattuš", "toponym", "Ḫattuša (pre-Hittite name)", "B", "rgtc", False, ""),
    (71, "Nerik", "toponym", "cult city of the storm god", "B", "rgtc", False, ""),
    (72, "Zippalanda", "toponym", "cult city", "B", "rgtc", False, ""),
    (73, "Arinna", "toponym", "cult city of the sun goddess", "B", "rgtc", False, ""),
    (74, "Tawiniya", "toponym", "town", "B", "rgtc", False, ""),
    (75, "Zalpa", "toponym", "town on the Black Sea coast", "B", "rgtc", False, ""),
    (76, "Liḫzina", "toponym", "cult town", "B", "rgtc", False, ""),
    (77, "Ḫakmiš", "toponym", "town (also Ḫakpiš)", "B", "rgtc", False, ""),
    (78, "Ankuwa", "toponym", "town", "B", "rgtc", False, ""),
    (79, "Kaštama", "toponym", "cult town", "B", "rgtc", False, ""),
    (80, "Ḫanḫana", "toponym", "cult town", "B", "rgtc", False, ""),
    (81, "Taḫurpa", "toponym", "cult town", "B", "rgtc", False, ""),
    (82, "Kammama", "toponym", "town", "B", "rgtc", False, ""),
    (83, "Katapa", "toponym", "town", "B", "rgtc", False, ""),
    (84, "Pamba", "personal_name", "king of Ḫatti in the Narām-Sîn tradition",
     "B", "kammenhuber", False, ""),
    (85, "Ḫuzziya", "personal_name", "Old Hittite royal name", "B", "kammenhuber",
     False, "Hattic origin of the name is argued, not secure."),
]


def all_records() -> list[dict]:
    out: list[dict] = []
    for iid, cited, cat, gloss, tier, cite_key, biling, note in RECORDS:
        translit = normalise(cited)
        out.append(
            {
                "id": iid,
                "name": cited,
                "category": cat,
                "gloss": gloss,
                "tier": tier,
                "text": cited,
                "transliteration": translit,
                "words": words_from(translit),
                "provenance": note or f"Hattic {cat}; see citation.",
                "source_citation": _CITATIONS[cite_key],
                "is_bilingual": biling,
            }
        )
    out.sort(key=lambda r: r["id"])
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, default=_DEFAULT_OUT_DIR)
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    rec_dir = out_dir / "inscriptions"
    rec_dir.mkdir(parents=True, exist_ok=True)

    records = all_records()
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate record id")
    for rec in records:
        (rec_dir / f"{rec['id']}.json").write_text(
            json.dumps(rec, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    with (out_dir / "all.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    words = sorted({w for r in records for w in r["words"]})
    (out_dir / "words.txt").write_text("\n".join(words) + "\n", encoding="utf-8")

    print(
        f"wrote {len(records)} records  |  {len(words)} unique word forms  |  "
        f"{sum(len(r['words']) for r in records)} word tokens",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
