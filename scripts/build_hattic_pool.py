#!/usr/bin/env python3
"""Build the Hattic substrate root pool YAML (mg-7f4db; v32 probe).

Reads the page-cited lexicon ``corpora/hattic/sources/lexicon.tsv`` and
emits one pool entry per lexeme. The output ``pools/hattic.yaml``
validates against ``pools/schemas/pool.v1.schema.json``.

Hattic is a Bronze Age central-Anatolian isolate with no relationship
to the Aegean / old-European pools. It enters the program as a
**specificity probe** (handoff 2026-05-06 §D.3), not as a candidate
Linear A substrate. See pools/hattic.README.md.

The lexicon (what v32 lacked)
-----------------------------
Every row of ``lexicon.tsv`` is one form as printed in a published
edition that was opened and read during mg-7f4db (or, for rows marked
"mg-78856", during that ticket under the same rule):

  * Kammenhuber, A. (1969). 'Hattisch.' HdO I/2.1-2/2: 428-546.
    Internet Archive scan
    ``friedrich-reiner-kammenhuber-neumann-heubeck-altkleinasiatische-sprachen-1969``.
  * Schuster, H.-S. (1974). Die hattisch-hethitischen Bilinguen I/1.
    Internet Archive scan ``die-hattisch-hethitischen-bilinguen``.

Each row carries the printed page, the scan leaf (IA ``page/n<leaf>``)
and a ``quote``: a verbatim stretch of the scan's OCR at that leaf.
``scripts/verify_hattic_sources.py`` re-downloads the OCR and checks
every quote; forms were read off the page images, because the OCR
misreads ḫ, š, u̯ and subscripts. A lexeme may have rows from both
works; its surface is the ``keyed`` form, which must normalise
identically on every row of the lexeme.

Pool design (mirrors ``scripts/build_eteocretan_pool.py``):
  * ``surface``: ``normalise(keyed)`` — the same normalisation as the LM
    corpus (``scripts/build_hattic_corpus.normalise``).
  * ``phonemes``: per-character split of the surface.
  * ``gloss``: English rendering of the source's (German) gloss.
  * ``semantic_field``: ``hattic_<category>``.
  * ``attestations``: the forms as printed in each source.
  * ``region``: ``central_anatolia``.
  * ``citation``: work, page and scan URL for every source row.
  * ``notes``: gloss confidence, the gloss as given, and the OCR quote.
  * ``provenance``: ``real`` — every entry is a viewed form.

Filter: entries with fewer than 2 phoneme classes (V / S / C) are
excluded, as in the Eteocretan builder.

Determinism: entries sorted by surface; stable key order.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.build_hattic_corpus import normalise  # noqa: E402


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_LEXICON = _REPO_ROOT / "corpora" / "hattic" / "sources" / "lexicon.tsv"
_DEFAULT_OUT = _REPO_ROOT / "pools" / "hattic.yaml"
_POOL_SCHEMA_PATH = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"

SOURCES: dict[str, dict[str, str]] = {
    "kammenhuber1969": {
        "short": "Kammenhuber 1969",
        "ia": "friedrich-reiner-kammenhuber-neumann-heubeck-altkleinasiatische-sprachen-1969",
    },
    "schuster1974": {
        "short": "Schuster 1974",
        "ia": "die-hattisch-hethitischen-bilinguen",
    },
}
CATEGORIES = frozenset(
    {"verb", "noun", "adjective", "particle", "theonym", "toponym", "title",
     "personal_name"}
)
CONFIDENCE = frozenset({"secure", "doubtful", "unknown_meaning"})

_VOWELS = frozenset("aeiou")
_SONORANTS = frozenset("lrnm")


def _phoneme_class(p: str) -> str:
    """Mirror of ``harness.metrics._class_of``."""
    if not p:
        return "C"
    h = p[0]
    if h in _VOWELS:
        return "V"
    if h in _SONORANTS:
        return "S"
    return "C"


def _has_two_classes(phonemes: list[str]) -> bool:
    return len({_phoneme_class(p) for p in phonemes}) >= 2


def page_url(source: str, leaf: int | str) -> str:
    return f"https://archive.org/details/{SOURCES[source]['ia']}/page/n{leaf}"


_SOURCE_CITATION_BLOCK = """\
Kammenhuber, A. (1969). 'Hattisch.' In Altkleinasiatische Sprachen,
  HdO I/2.1-2/2: 428-546. Leiden: Brill. Viewed as the Internet Archive
  scan friedrich-reiner-kammenhuber-neumann-heubeck-altkleinasiatische-sprachen-1969
  (page images + OCR), pp. 432-530.
Schuster, H.-S. (1974). Die hattisch-hethitischen Bilinguen I.
  Einleitung, Texte und Kommentar, Teil 1. Leiden: Brill. Viewed as the
  Internet Archive scan die-hattisch-hethitischen-bilinguen (forms
  sourced by mg-78856 in ~/research/hattic-semitic; spot-checked).
Every entry cites the page and scan leaf it was read from, and carries a
verbatim OCR quote checked by scripts/verify_hattic_sources.py. Nothing
is keyed from memory. Built from corpora/hattic/sources/lexicon.tsv by
scripts/build_hattic_pool.py. The hattic LM is trained on a separate
running-text corpus (TLHdig), not on this pool; see pools/hattic.README.md.
"""

_LICENSE_BLOCK = """\
Cited fair-use of the scholarly literature for the lexical forms and
glosses (short quotations, page-referenced). Underlying tablets PD.
"""


def load_lexicon(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    for r in rows:
        if r["source"] not in SOURCES:
            raise ValueError(f"{r['lex_id']}: unknown source {r['source']!r}")
        if r["category"] not in CATEGORIES:
            raise ValueError(f"{r['lex_id']}: unknown category {r['category']!r}")
        if r["confidence"] not in CONFIDENCE:
            raise ValueError(f"{r['lex_id']}: unknown confidence {r['confidence']!r}")
        for col in ("printed", "keyed", "page", "leaf", "quote", "gloss_as_given"):
            if not r[col].strip():
                raise ValueError(f"{r['lex_id']}: empty {col}")
        int(r["page"]), int(r["leaf"])
    return rows


def group_lexemes(rows: list[dict]) -> dict[str, list[dict]]:
    """lex_id → its rows, in file order. Raises if the rows of one lexeme
    normalise to different surfaces, or two lexemes share a surface."""
    lex: dict[str, list[dict]] = {}
    for r in rows:
        lex.setdefault(r["lex_id"], []).append(r)
    seen: dict[str, str] = {}
    for lid, rs in lex.items():
        surfaces = {normalise(r["keyed"]) for r in rs}
        if len(surfaces) != 1:
            raise ValueError(f"{lid}: rows normalise to {sorted(surfaces)}")
        (s,) = surfaces
        if " " in s or not s:
            raise ValueError(f"{lid}: bad surface {s!r}")
        if s in seen:
            raise ValueError(f"surface {s!r} shared by {seen[s]} and {lid}")
        seen[s] = lid
    return lex


def build_pool_doc(rows: list[dict]) -> dict:
    entries: list[dict] = []
    for lid, rs in group_lexemes(rows).items():
        surface = normalise(rs[0]["keyed"])
        phonemes = list(surface)
        if not _has_two_classes(phonemes):
            continue
        first = rs[0]
        citation = "; ".join(
            f"{SOURCES[r['source']]['short']}, p. {r['page']}, "
            f"{page_url(r['source'], r['leaf'])}"
            for r in rs
        )
        notes = " | ".join(
            f"{SOURCES[r['source']]['short']} p. {r['page']}: {r['gloss_as_given']} "
            f"[{r['confidence']}; OCR quote: \"{r['quote']}\"]"
            + (f" {r['note']}" if r["note"] else "")
            for r in rs
        )
        entries.append(
            {
                "surface": surface,
                "phonemes": phonemes,
                "gloss": first["gloss_en"],
                "semantic_field": f"hattic_{first['category']}",
                "attestations": sorted({r["printed"] for r in rs}),
                "region": "central_anatolia",
                "citation": citation,
                "notes": f"lexicon {lid}. " + notes,
                "provenance": "real",
            }
        )
    entries.sort(key=lambda e: e["surface"])
    return {
        "pool": "hattic",
        "source_citation": _SOURCE_CITATION_BLOCK,
        "license": _LICENSE_BLOCK,
        "fetched_at": "2026-10-03T00:00:00Z",
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lexicon", type=Path, default=_DEFAULT_LEXICON)
    parser.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = parser.parse_args(argv)

    doc = build_pool_doc(load_lexicon(args.lexicon))
    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(doc)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"wrote {len(doc['entries'])} pool entries to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
