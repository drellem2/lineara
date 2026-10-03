#!/usr/bin/env python3
"""Build the Hattic substrate root pool YAML (mg-7e7d6, specificity probe).

Walks ``corpora/hattic/all.jsonl`` and emits one pool entry per unique
normalised word form. The output ``pools/hattic.yaml`` validates against
``pools/schemas/pool.v1.schema.json``.

Hattic is a Bronze Age central-Anatolian isolate with no relationship
to the Aegean / old-European pools. It enters the program as a
**specificity probe** (handoff 2026-05-06 §D.3), not as a candidate
Linear A substrate: a PASS on Hattic as ready as the Aegean pools' is
evidence the gate measures generic structure. See pools/hattic.README.md.

Pool design (mirrors ``scripts/build_eteocretan_pool.py``):
  * ``surface``: the normalised lowercase-ASCII form (same normalisation
    as the corpus / LM — see ``scripts/build_hattic_corpus.normalise``).
  * ``phonemes``: per-character split of the surface.
  * ``gloss``: the scholarly gloss carried on the corpus record.
  * ``semantic_field``: ``hattic_<category>`` (theonym / lexeme /
    toponym / personal_name).
  * ``attestations``: the cited scholarly form(s) the surface derives
    from.
  * ``region``: ``central_anatolia``.
  * ``provenance``: ``real`` — no conjectural entries are added.
  * ``notes``: confidence tier (A / B, see corpora/hattic.README.md).

Filter: entries with fewer than 2 phoneme classes (V / S / C) are
excluded, as in the Eteocretan builder.

Determinism: entries sorted by surface; stable key order.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpora" / "hattic" / "all.jsonl"
_DEFAULT_OUT = _REPO_ROOT / "pools" / "hattic.yaml"
_POOL_SCHEMA_PATH = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"


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


_SOURCE_CITATION_BLOCK = """\
Soysal, O. (2004). Hattischer Wortschatz in hethitischer
  Textüberlieferung. HdO I/74. Leiden: Brill. — the standard Hattic
  lexicon; primary reference for the lexemes.
Klinger, J. (1996). Untersuchungen zur Rekonstruktion der hattischen
  Kultschicht. StBoT 37. Wiesbaden: Harrassowitz.
Kammenhuber, A. (1969). 'Hattisch.' HdO I/2.1-2/2: 428-546.
Taracha, P. (2009). Religions of Second Millennium Anatolia. DBH 27.
del Monte, G. F. & Tischler, J. (1978). RGTC 6 (toponyms).
Bischoff, A. M. (2023). Hungarian Assyriological Review 4: 95-109.
Underlying Hittite-archive tablets (CTH 725-745 and Hattic passages in
  Hittite ritual / festival texts) are Bronze Age, public domain. Manual
  lexical transcription via scripts/build_hattic_corpus.py; forms not
  collated against the printed editions (see corpora/hattic.README.md).
"""

_LICENSE_BLOCK = """\
Cited fair-use of the scholarly literature for the lexical forms and
glosses. Underlying tablets PD.
"""


def load_corpus(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_pool_doc(corpus: list[dict]) -> dict:
    by_surface: dict[str, list[dict]] = defaultdict(list)
    for rec in corpus:
        for w in rec["words"]:
            by_surface[w].append(rec)

    entries: list[dict] = []
    for surface in sorted(by_surface):
        phonemes = list(surface)
        if not _has_two_classes(phonemes):
            continue
        recs = sorted(by_surface[surface], key=lambda r: r["id"])
        first = recs[0]
        tiers = sorted({r["tier"] for r in recs})
        citation = (
            f"Corpus record(s) {', '.join(str(r['id']) for r in recs)} "
            f"(corpora/hattic/inscriptions/). {first['source_citation']}"
        )
        if any(r.get("is_bilingual") for r in recs):
            citation += " Gloss rests on a Hattic-Hittite bilingual correspondence."
        entries.append(
            {
                "surface": surface,
                "phonemes": phonemes,
                "gloss": first["gloss"],
                "semantic_field": f"hattic_{first['category']}",
                "attestations": sorted({r["name"] for r in recs}),
                "region": "central_anatolia",
                "citation": citation,
                "notes": f"confidence tier {'/'.join(tiers)}",
                "provenance": "real",
            }
        )

    return {
        "pool": "hattic",
        "source_citation": _SOURCE_CITATION_BLOCK,
        "license": _LICENSE_BLOCK,
        "fetched_at": "2026-10-03T00:00:00Z",
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = parser.parse_args(argv)

    doc = build_pool_doc(load_corpus(args.corpus))
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
