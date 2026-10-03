#!/usr/bin/env python3
"""Build the Hattic running-text corpus from TLHdig (mg-7f4db; v32 probe).

Hattic is the non-Indo-European isolate of Bronze Age central Anatolia,
known only through the Hittite state archives at Ḫattuša. It has no
genealogical relationship to any of the Aegean / old-European pools in
this repo. It is run through the lineara program as a **specificity
probe** (handoff 2026-05-06 §D.3) and makes no decipherment claim.

What this corpus is (and what it replaced)
------------------------------------------
v32 (mg-7e7d6) keyed 72 lexical forms from memory and trained the LM on
exactly the pool's forms. mg-7f4db replaced that with **running text**:
every intact Hattic word of the TLHdig transliterations (Thesaurus
Linguarum Hethaeorum digitalis, Beta 0.2; Zenodo DOI
10.5281/zenodo.15459134, CC BY 4.0), which digitises the published
editions of the Boğazköy tablets — the Hattic-Hittite bilinguals and
Hattic cult texts of CTH 725-746, and the Hattic recitations embedded in
Hittite festival texts. The TLHdig XML is reduced to
``corpora/hattic/sources/tlhdig_hattic_lines.tsv`` by
``scripts/extract_tlhdig_hattic.py`` (see there for which words count as
intact); this script reads only that TSV. The pool
(``pools/hattic.yaml``) is built from a separate, page-cited lexicon
(``scripts/build_hattic_pool.py``) and is **not** part of this corpus.

Normalisation (applied identically to corpus and pool)
------------------------------------------------------
``normalise`` maps a transliteration to lowercase ASCII a-z. The v32
rules are kept:
  * diacritics stripped: š → s (s/š merged), ḫ → h, ú/í/é/á → u/i/e/a;
  * hyphens removed (``ka-a-at-te`` → ``katte``);
  * stop voicing merged to the voiceless series (b → p, d → t, g → k):
    cuneiform does not reliably write Hattic stop voicing;
  * the labial "f" maps to w;
  * plene vowel runs collapsed (``aa`` → ``a``);
  * consonant gemination retained.
mg-7f4db adds three rules for the printed editions' "bound
transcription" (Kammenhuber 1969, Schuster 1974), which the v32 forms
never used:
  * u̯ (u with inverted breve below, the WA-series sign) → w;
  * i̯ (the IA-series sign) → i, as TLHdig writes it (``ia``);
  * Schuster's v (his transcription of the same WA sign) → w;
subscript vowel indices (``u̯aₐ``) are dropped with the other non-letters.

Output (mirrors corpora/eteocretan/):
  corpora/hattic/inscriptions/<id>.json   one per TLHdig manuscript
  corpora/hattic/all.jsonl                aggregate (sorted by id)
  corpora/hattic/words.txt                flat word list (gitignored)

Determinism: manuscripts numbered in TSV order; JSON dumped with
sort_keys=True; words.txt sorted-unique. Re-runs produce byte-identical
output.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT_DIR = _REPO_ROOT / "corpora" / "hattic"
_DEFAULT_SOURCE = _DEFAULT_OUT_DIR / "sources" / "tlhdig_hattic_lines.tsv"

TLHDIG_CITATION = (
    "Thesaurus Linguarum Hethaeorum digitalis (TLHdig), Beta Version 0.2. "
    "Hethitologie-Portal Mainz. XML dataset, Zenodo, "
    "https://doi.org/10.5281/zenodo.15459134 (CC BY 4.0); online at "
    "https://www.hethport.uni-wuerzburg.de/TLHdig/."
)
TLHDIG_URL = "https://doi.org/10.5281/zenodo.15459134"


def _strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfd if not unicodedata.combining(ch))


_VOICING = str.maketrans({"b": "p", "d": "t", "g": "k", "f": "w", "v": "w"})
_INV_BREVE = "̯"


def normalise(cited: str) -> str:
    """Transliteration → normalised lowercase ASCII (see module
    docstring). Whitespace separates words; everything else non a-z is
    dropped."""
    s = unicodedata.normalize("NFD", cited).lower()
    s = s.replace("u" + _INV_BREVE, "w").replace("i" + _INV_BREVE, "i")
    s = _strip_diacritics(s)
    s = s.replace("-", "")
    s = s.translate(_VOICING)
    s = re.sub(r"[^a-z\s]", "", s)
    s = re.sub(r"([aeiou])\1+", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def words_from(translit: str) -> list[str]:
    """Word tokens of length >= 2 (single chars carry no bigram)."""
    return [w for w in translit.split() if len(w) >= 2 and w.isalpha()]


def load_lines(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))


def all_records(source: Path = _DEFAULT_SOURCE) -> list[dict]:
    """One record per TLHdig manuscript that has at least one intact
    Hattic word. Lines without an intact word are kept in ``lines`` (for
    the line count) but contribute no words."""
    by_ms: dict[tuple[str, str], list[dict]] = {}
    for row in load_lines(source):
        by_ms.setdefault((row["cth"], row["manuscript"]), []).append(row)

    out: list[dict] = []
    for iid, ((cth, ms), rows) in enumerate(by_ms.items(), start=1):
        lines = []
        words: list[str] = []
        for row in rows:
            intact = row["intact"].split()
            lw = words_from(normalise(" ".join(intact)))
            lines.append(
                {
                    "line": row["line"],
                    "raw": row["raw"],
                    "intact": intact,
                    "words": lw,
                }
            )
            words.extend(lw)
        if not words:
            continue
        out.append(
            {
                "id": iid,
                "cth": cth,
                "manuscript": ms,
                "lines": lines,
                "words": words,
                "source_citation": TLHDIG_CITATION,
                "url": TLHDIG_URL,
            }
        )
    out.sort(key=lambda r: r["id"])
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, default=_DEFAULT_SOURCE)
    parser.add_argument("--out-dir", type=Path, default=_DEFAULT_OUT_DIR)
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    rec_dir = out_dir / "inscriptions"
    rec_dir.mkdir(parents=True, exist_ok=True)
    for stale in rec_dir.glob("*.json"):
        stale.unlink()

    records = all_records(args.source)
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
        f"wrote {len(records)} manuscripts  |  {len(words)} unique word forms  |  "
        f"{sum(len(r['words']) for r in records)} word tokens",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
