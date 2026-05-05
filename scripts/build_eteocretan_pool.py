#!/usr/bin/env python3
"""Build the Eteocretan substrate root pool YAML (mg-6ccd, harness v21).

Walks ``corpora/eteocretan/all.jsonl`` and emits one pool entry per
unique attested word form, with attestations linking back to the
inscription IDs the form appears in. The output ``pools/eteocretan.yaml``
validates against ``pools/schemas/pool.v1.schema.json``.

Pool design:
  * ``surface``: the lowercase-ASCII word form as transliterated.
  * ``phonemes``: per-character split of the surface (single-char
    phonemes; the Eteocretan transliteration uses the standard Latin
    mapping with multi-char digraphs ``th``, ``ph``, ``kh``, ``ks``
    treated as bigrams of their constituent letters, matching the
    Etruscan / Basque convention in this codebase).
  * ``gloss``: ``"unknown"`` for almost every form — Eteocretan is
    undeciphered. The two partial bilinguals (Praisos 2, Dreros 1)
    do not give word-by-word translations even for the words they
    attest, so we do not assert glosses we cannot defend.
  * ``attestations``: list of inscription names where the form
    appears.
  * ``region``: ``crete`` (eastern Cretan provenance, Praisos +
    Dreros + Psychro).
  * ``citation``: per-entry pointer to the catalog entry.

Filter: pool entries with fewer than 2 distinct phoneme classes
(V / S / C) are excluded — `scripts/generate_candidates.py` skips them
wholesale because ``local_fit_v0`` would force ``control_std=0``.
That filter drops ~3 V-only / V+V tokens from the 87-form word list.

Determinism: entries sorted by surface; YAML emitted with
``sort_keys=False`` and a stable per-entry key order. Re-runs produce
byte-identical output.
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
_DEFAULT_CORPUS = _REPO_ROOT / "corpora" / "eteocretan" / "all.jsonl"
_DEFAULT_OUT = _REPO_ROOT / "pools" / "eteocretan.yaml"
_POOL_SCHEMA_PATH = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"


_VOWELS = frozenset("aeiou")
_SONORANTS = frozenset("lrnm")


def _phoneme_class(p: str) -> str:
    """Mirror of ``harness.metrics._class_of`` (and
    ``scripts/generate_candidates._phoneme_class``)."""
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
Duhoux, Y. (1982). L'Étéocrétois: les textes — la langue. Amsterdam:
  J. C. Gieben. — the canonical scholarly edition of the Eteocretan
  inscriptional record (Praisos 1-7, Dreros 1-2, Psychro stone).
Whittaker, H. (2017). 'Of linguistic alterity in Crete: the Eteocretan
  inscriptions.' Scripta Classica Israelica 36: 7-31. — supplementary
  Praisos area minor inscriptions whose language is non-Greek.
Younger, J. G. (2000-present). 'Linear A: text and inscriptions.'
  https://people.ku.edu/~jyounger/LinearA/  — Eteocretan annex covering
  iron-age Cretan short inscriptions.
Underlying inscriptions are public domain (~7th-3rd c. BCE Cretan
  stone-cut and pottery texts). Manual transcription via
  scripts/build_eteocretan_corpus.py.
"""

_LICENSE_BLOCK = """\
Cited fair-use of Duhoux 1982 and Whittaker 2017 for transcription
conventions and scholarly editing. Underlying inscriptions PD.
"""


def load_corpus(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def build_pool_doc(corpus: list[dict]) -> dict:
    """Aggregate corpus → pool document. Returns a YAML-ready dict."""
    by_surface: dict[str, set[str]] = defaultdict(set)
    bilingual_inscriptions: set[str] = set()
    for rec in corpus:
        for w in rec["words"]:
            by_surface[w].add(rec["name"])
        if rec.get("is_bilingual"):
            bilingual_inscriptions.add(rec["name"])

    entries: list[dict] = []
    for surface in sorted(by_surface):
        phonemes = list(surface)
        if not _has_two_classes(phonemes):
            continue
        attestations = sorted(by_surface[surface])
        # Per-entry citation tag: name the first inscription, plus
        # bilingual flag if any source is bilingual.
        first = attestations[0]
        bilingual_attestation = any(
            a in bilingual_inscriptions for a in attestations
        )
        citation = (
            f"Attested in {len(attestations)} inscription(s) "
            f"(first: {first}). "
        )
        if bilingual_attestation:
            citation += (
                "At least one attestation is from a partial bilingual "
                "(Praisos 2 / Dreros 1); see corpora/eteocretan/inscriptions/. "
            )
        citation += (
            "Source: Duhoux 1982 / Whittaker 2017 / Younger online "
            "catalog (see corpora/eteocretan.README.md)."
        )
        entries.append(
            {
                "surface": surface,
                "phonemes": phonemes,
                "gloss": "unknown",
                "semantic_field": "eteocretan_root",
                "attestations": attestations,
                "region": "crete",
                "citation": citation,
            }
        )

    return {
        "pool": "eteocretan",
        "source_citation": _SOURCE_CITATION_BLOCK,
        "license": _LICENSE_BLOCK,
        "fetched_at": "2026-05-05T00:00:00Z",
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = parser.parse_args(argv)

    corpus = load_corpus(args.corpus)
    doc = build_pool_doc(corpus)

    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(doc)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(
        doc, sort_keys=False, allow_unicode=True, default_flow_style=False
    )
    args.out.write_text(text, encoding="utf-8")

    print(
        f"wrote {len(doc['entries'])} pool entries to {args.out}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
