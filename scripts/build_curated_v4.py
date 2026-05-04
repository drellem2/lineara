#!/usr/bin/env python3
"""Deterministic builder for the curated-v4 hypothesis set (mg-7c8c).

Expands each of the five hypothesis-quality buckets from n=4 to n=20 by
emitting **16 new YAMLs per bucket** under ``hypotheses/curated/`` plus a
``hypotheses/curated/CONSTRUCTION.manifest.jsonl`` manifest covering all
100 hypotheses (the existing 20 plus the 80 new ones).

The script is **deterministic and idempotent**: re-running with the same
corpus snapshot, same toponym pool, and same input lists produces
byte-identical YAMLs and manifest. Selection rules are documented in
``hypotheses/curated/CONSTRUCTION.md``; the hardcoded data tables below
are the per-bucket inputs the rules consume.

Usage:
    python3 scripts/build_curated_v4.py
    python3 scripts/build_curated_v4.py --no-write    # dry run

The output YAMLs validate against
``harness/schemas/hypothesis.candidate_equation.v1.schema.json``; the
manifest follows the format of ``scripts/generate_candidates.py`` so
``scripts/run_sweep.py`` can consume it directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_AQUITANIAN_POOL = _REPO_ROOT / "pools" / "aquitanian.yaml"
_DEFAULT_TOPONYM_POOL = _REPO_ROOT / "pools" / "toponym.yaml"
_CURATED_DIR = _REPO_ROOT / "hypotheses" / "curated"
_MANIFEST_PATH = _CURATED_DIR / "CONSTRUCTION.manifest.jsonl"
_SCHEMA_PATH = (
    _REPO_ROOT / "harness" / "schemas" / "hypothesis.candidate_equation.v1.schema.json"
)

_SYLL_RE = re.compile(r"^A[B]?\d+$")
_DIV = "DIV"
_NAME_RE = re.compile(r"[^A-Za-z0-9_]")
_RANDOM_SEED = 4242  # frozen for the v4 scramble bucket; do not edit


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _slug(s: str) -> str:
    return _NAME_RE.sub("_", s)


def _is_syllabogram(tok: str) -> bool:
    return bool(_SYLL_RE.fullmatch(tok))


def _canonical_hash(doc: dict) -> str:
    payload = json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _load_corpus(corpus_path: Path) -> list[dict]:
    records: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])
    return records


def _load_pool(pool_path: Path) -> dict:
    with pool_path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def _sign_corpus_counts(records: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in records:
        if int(r.get("n_signs", 0)) <= 0:
            continue
        for t in r["tokens"]:
            if _is_syllabogram(t):
                counts[t] = counts.get(t, 0) + 1
    return counts


def _candidate_windows(
    tokens: list[str], n_phonemes: int
) -> list[tuple[int, int, list[int]]]:
    """All windows containing exactly ``n_phonemes`` syllabograms with no DIV
    crossing. Endpoints inclusive; returned as (span_start, span_end, indices).
    """
    if n_phonemes <= 0:
        return []
    windows: list[tuple[int, int, list[int]]] = []
    block: list[int] = []
    for i, tok in enumerate(tokens):
        if tok == _DIV:
            _emit_block(block, n_phonemes, windows)
            block = []
        elif _is_syllabogram(tok):
            block.append(i)
    _emit_block(block, n_phonemes, windows)
    return windows


def _emit_block(
    syllabograms: list[int],
    n: int,
    out: list[tuple[int, int, list[int]]],
) -> None:
    for i in range(0, len(syllabograms) - n + 1):
        idxs = syllabograms[i : i + n]
        out.append((idxs[0], idxs[-1], idxs))


def _find_window(
    record: dict, n_phonemes: int, *, distinct: bool = True
) -> tuple[int, int, list[int]] | None:
    """Return the first valid window of ``n_phonemes`` syllabograms in
    ``record`` whose syllabograms are pairwise distinct (when ``distinct``).
    None if no such window exists.
    """
    tokens = record["tokens"]
    for span_start, span_end, idxs in _candidate_windows(tokens, n_phonemes):
        signs = [tokens[i] for i in idxs]
        if distinct and len(set(signs)) != n_phonemes:
            continue
        return span_start, span_end, idxs
    return None


def _find_window_with_signs(
    record: dict, target_signs: list[str]
) -> tuple[int, int, list[int]] | None:
    """Return the first window in ``record`` where the syllabogram sub-sequence
    equals ``target_signs`` exactly (no DIV crossing, signs may repeat in the
    target). None if no such window exists.
    """
    n = len(target_signs)
    tokens = record["tokens"]
    for span_start, span_end, idxs in _candidate_windows(tokens, n):
        signs = [tokens[i] for i in idxs]
        if signs == target_signs:
            return span_start, span_end, idxs
    return None


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(
        doc, sort_keys=False, allow_unicode=True, default_flow_style=False
    )


def _build_doc(
    *,
    name: str,
    description: str,
    source_pool: str,
    surface: str,
    phonemes: list[str],
    gloss_hint: str,
    citation: str,
    inscription_id: str,
    span: tuple[int, int],
    sign_to_phoneme: dict[str, str],
    notes: str,
) -> dict:
    return {
        "schema_version": "candidate_equation.v1",
        "name": name,
        "description": description,
        "author": "scripts/build_curated_v4.py",
        "created": "2026-05-04",
        "source_pool": source_pool,
        "root": {
            "surface": surface,
            "phonemes": phonemes,
            "gloss_hint": gloss_hint,
            "citation": citation,
        },
        "equation": {
            "inscription_id": inscription_id,
            "span": [span[0], span[1]],
            "sign_to_phoneme": sign_to_phoneme,
        },
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Bucket A: 16 new Linear-B carryover anchors
# ---------------------------------------------------------------------------
#
# Each anchor is a 2- or 3-sign Linear-A sequence whose Linear-B carryover
# values are accepted in Younger's online edition of "Linear A texts in
# phonetic transcription" (https://people.ku.edu/~jyounger/LinearA/).
#
# Rules:
#   * Each anchor's signs occur ≥10 times in the SigLA corpus.
#   * Each anchor's signs are pairwise distinct.
#   * Placement: prefer Knossos clean accountancy inscription
#     (region_compat=1.0 for linear_b × Knossos); else any clean
#     accountancy inscription.
#   * Each placement window contains the target sign sequence in order.

# Surfaces, phonemes, sign sequences, and per-anchor citations.
# Sign frequencies (from `_sign_corpus_counts` on the SigLA corpus):
#   AB01=99, AB02=89, AB03=82, AB04=75, AB05=11, AB06=96, AB07=78, AB08=135,
#   AB09=47, AB13=19, AB17=28, AB23=8 (skip), AB24=18, AB26=69, AB27=89,
#   AB28=93, AB30=48, AB31=83, AB37=71, AB38=16, AB39=37, AB41=86, AB44=9
#   (skip), AB45=30, AB51=65, AB54=17, AB57=85, AB58=40, AB59=106, AB60=85,
#   AB67=91, AB69=57, AB73=68, AB77=92, AB78=36, AB80=84, AB81=138.
#
_ANCHOR_SPECS: list[dict] = [
    # 2-sign anchors (14) — short, high-frequency Linear-A lexemes per Younger.
    # Each sign-pair has been verified to occur as adjacent syllabograms
    # (no DIV between them) in at least one clean accountancy inscription.
    {
        "surface": "kupa",
        "phonemes": ["ku", "pa"],
        "signs": ["AB81", "AB03"],
        "gloss": "kupa- name family / commodity-prefix (Linear-A recurring)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04), entries indexing "
            "Linear-A ku-pa- sequence; AB81=ku, AB03=pa per Ventris-Chadwick "
            "1956 Linear-B carryover values."
        ),
    },
    {
        "surface": "kapa",
        "phonemes": ["ka", "pa"],
        "signs": ["AB77", "AB03"],
        "gloss": "ka-pa Linear-A recurring transaction term",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB77=ka, AB03=pa per "
            "the Ventris-Chadwick carryover."
        ),
    },
    {
        "surface": "karu",
        "phonemes": ["ka", "ru"],
        "signs": ["AB77", "AB26"],
        "gloss": "ka-ru recurring lexeme on transaction tablets",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB77=ka, AB26=ru."
        ),
    },
    {
        "surface": "mate",
        "phonemes": ["ma", "te"],
        "signs": ["AB80", "AB04"],
        "gloss": "ma-te (cf. Linear-B ma-te 'mater'; substrate kinship term)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB80=ma, AB04=te; "
            "Linear-B carryover ma-te = mater (Ventris-Chadwick 1956)."
        ),
    },
    {
        "surface": "tana",
        "phonemes": ["ta", "na"],
        "signs": ["AB59", "AB06"],
        "gloss": "ta-na (libation-formula and name suffix; Younger lex)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB59=ta, AB06=na."
        ),
    },
    {
        "surface": "dina",
        "phonemes": ["di", "na"],
        "signs": ["AB07", "AB06"],
        "gloss": "di-na recurring Linear-A lexeme",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB07=di, AB06=na."
        ),
    },
    {
        "surface": "kupa3",
        "phonemes": ["ku", "pa3"],
        "signs": ["AB81", "AB56"],
        "gloss": "ku-pa3 name family (variant of kupa)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB81=ku, AB56=pa3 (pa2)."
        ),
    },
    {
        "surface": "mina",
        "phonemes": ["mi", "na"],
        "signs": ["AB73", "AB06"],
        "gloss": "mi-na (cumin termination; cf. ku-mi-na)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB73=mi, AB06=na; "
            "cf. ku-mi-na cumin."
        ),
    },
    {
        "surface": "kira",
        "phonemes": ["ki", "ra"],
        "signs": ["AB67", "AB60"],
        "gloss": "ki-ra recurring suffix variant",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB67=ki, AB60=ra."
        ),
    },
    {
        "surface": "dare",
        "phonemes": ["da", "re"],
        "signs": ["AB01", "AB27"],
        "gloss": "da-re (libation-formula continuation, da-ta-re paradigm)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB01=da, AB27=re; "
            "Schoep 2002 ch. 4 on libation-table da-re paradigm."
        ),
    },
    {
        "surface": "data",
        "phonemes": ["da", "ta"],
        "signs": ["AB01", "AB59"],
        "gloss": "da-ta libation-formula prefix",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB01=da, AB59=ta; "
            "Schoep 2002 ch. 4 on libation-table formulae."
        ),
    },
    {
        "surface": "tare",
        "phonemes": ["ta", "re"],
        "signs": ["AB59", "AB27"],
        "gloss": "ta-re libation-formula continuation",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB59=ta, AB27=re."
        ),
    },
    {
        "surface": "paja",
        "phonemes": ["pa", "ja"],
        "signs": ["AB03", "AB57"],
        "gloss": "pa-ja name-family / votive prefix",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB03=pa, AB57=ja."
        ),
    },
    {
        "surface": "kuse",
        "phonemes": ["ku", "se"],
        "signs": ["AB81", "AB09"],
        "gloss": "ku-se Linear-A recurring lexeme",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB81=ku, AB09=se."
        ),
    },
    # 3-sign anchors (2) — longer Younger-listed sequences.
    {
        "surface": "kumina",
        "phonemes": ["ku", "mi", "na"],
        "signs": ["AB81", "AB73", "AB06"],
        "gloss": "ku-mi-na (cumin commodity, Linear-A spice term)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04), s.v. ku-mi-na (cumin); "
            "AB81=ku, AB73=mi, AB06=na."
        ),
    },
    {
        "surface": "pitaja",
        "phonemes": ["pi", "ta", "ja"],
        "signs": ["AB39", "AB59", "AB57"],
        "gloss": "pi-ta-ja (Younger's standard 3-sign Linear-A name)",
        "citation": (
            "Younger, J. G., 'Linear A texts in phonetic transcription' "
            "(online edition, retrieved 2026-05-04); AB39=pi, AB59=ta, "
            "AB57=ja."
        ),
    },
]


def build_anchors(records: list[dict]) -> list[dict]:
    """Place each anchor in the first matching window of the first matching
    inscription, preferring Knossos accountancy clean inscriptions."""
    # Two-pass placement: prefer Knossos, then any clean accountancy.
    knossos_first = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and r.get("genre_hint") == "accountancy"
            and r.get("site") == "Knossos"
        ],
        key=lambda r: r["id"],
    )
    fallback = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and r.get("genre_hint") == "accountancy"
            and r.get("site") != "Knossos"
        ],
        key=lambda r: r["id"],
    )
    placed: list[dict] = []
    used_keys: set[tuple[str, int, int]] = set()
    for spec in _ANCHOR_SPECS:
        signs = spec["signs"]
        chosen: tuple[dict, int, int, list[int]] | None = None
        for record_pool in (knossos_first, fallback):
            for record in record_pool:
                w = _find_window_with_signs(record, signs)
                if w is None:
                    continue
                span_start, span_end, idxs = w
                key = (record["id"], span_start, span_end)
                if key in used_keys:
                    continue
                chosen = (record, span_start, span_end, idxs)
                break
            if chosen is not None:
                break
        if chosen is None:
            raise RuntimeError(
                f"could not place anchor {spec['surface']!r} (signs={signs})"
            )
        record, span_start, span_end, idxs = chosen
        used_keys.add((record["id"], span_start, span_end))

        sign_to_phoneme = dict(zip(signs, spec["phonemes"]))
        name = f"v4_anchor_{_slug(spec['surface'])}_{_slug(record['id'])}"
        notes = (
            f"v4 bucket A (linear_b_carryover_anchor; mg-7c8c). "
            f"Site={record['site']}; genre_hint={record.get('genre_hint')}; "
            f"confidence={record.get('transcription_confidence')}. "
            f"Pre-placement Linear-B value: {' '.join(spec['phonemes'])}. "
            f"Signs picked from {record['id']} tokens "
            f"[{span_start}..{span_end}]."
        )
        description = (
            f"v4 Linear-B carryover anchor: {' '.join(signs)} = "
            f"/{'-'.join(spec['phonemes'])}/ in {record['id']} "
            f"tokens [{span_start}..{span_end}]. {spec['gloss']}."
        )
        doc = _build_doc(
            name=name,
            description=description,
            source_pool="linear_b_carryover",
            surface=spec["surface"],
            phonemes=list(spec["phonemes"]),
            gloss_hint=spec["gloss"],
            citation=spec["citation"],
            inscription_id=record["id"],
            span=(span_start, span_end),
            sign_to_phoneme=sign_to_phoneme,
            notes=notes,
        )
        placed.append({"doc": doc, "bucket": "A_linear_b_anchor", "spec": spec})
    return placed


# ---------------------------------------------------------------------------
# Bucket B: 16 new plausible Aquitanian candidates.
# Bucket C: 16 new deliberately-wrong Aquitanian candidates (same surfaces).
# ---------------------------------------------------------------------------
#
# Selection rules:
#   * The 16 surfaces are drawn from pools/aquitanian.yaml entries whose
#     semantic_field is in {agriculture, food, animal, number} so that:
#        plausible (clean accountancy)             ≥ 0.5 (typically 0.75-1.0)
#        wrong    (clean votive_or_inscription)    = 0.25
#     This is the cleanest *flip* under
#     `harness.metrics._GG1_SEMANTIC_COMPAT`. The Aquitanian pool has
#     surfaces in food, animal, number; agriculture has none.
#   * Phoneme length 2-5.
#   * Plausible: first clean accountancy inscription where the surface fits
#     a window with pairwise-distinct signs. Records sorted by id so the
#     selection is deterministic.
#   * Wrong: same surface, first clean votive_or_inscription inscription
#     with a fitting window (also deterministic by id-sort).
#   * The wrong placement is NOT phonotactically wrong — we don't filter
#     for sign-position-mismatch. The phoneme order, sign set, and
#     resulting sign_to_phoneme dict can produce a perfectly typical
#     V/S/C alternation; the only thing distinguishing wrong from
#     plausible is the inscription's genre_hint.

# 16 selected surfaces (from pools/aquitanian.yaml). The numbers/letters
# in the trailing comment are the surface's semantic_field (for trace).
_PLAUSIBLE_AQUIT_SURFACES = [
    # food (semantic_field=food → 0.75 vs accountancy, 0.25 vs votive)
    "gari",   # 4 phonemes
    "arto",   # 4
    "ogi",    # 3
    "esne",   # 4
    "ardo",   # 4
    "olio",   # 4
    "ezti",   # 4
    "sagar",  # 5
    # animal (0.75 vs accountancy, 0.25 vs votive)
    "ardi",   # 4
    "behi",   # 4
    "katu",   # 4
    "zaldi",  # 5
    # number (1.0 vs accountancy, 0.25 vs votive)
    "bat",    # 3
    "hiru",   # 4
    "lau",    # 3
    "hamar",  # 5
]


def _surface_to_pool_entry(pool: dict, surface: str) -> dict:
    for e in pool["entries"]:
        if e["surface"] == surface:
            return e
    raise KeyError(f"surface {surface!r} not in pool {pool['pool']!r}")


def build_aquit_plausible_and_wrong(
    records: list[dict], pool: dict
) -> tuple[list[dict], list[dict]]:
    plausible_pool = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and r.get("genre_hint") == "accountancy"
        ],
        key=lambda r: r["id"],
    )
    wrong_pool = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and r.get("genre_hint") == "votive_or_inscription"
        ],
        key=lambda r: r["id"],
    )

    placed_plausible: list[dict] = []
    placed_wrong: list[dict] = []
    used_plausible: set[tuple[str, int, int]] = set()
    used_wrong: set[tuple[str, int, int]] = set()

    for surface in _PLAUSIBLE_AQUIT_SURFACES:
        entry = _surface_to_pool_entry(pool, surface)
        phonemes = list(entry["phonemes"])
        n = len(phonemes)
        # Plausible placement
        chosen_p = _pick_unused(plausible_pool, n, used_plausible)
        if chosen_p is None:
            raise RuntimeError(
                f"plausible: could not place {surface!r} in any clean accountancy inscription"
            )
        record_p, span_p_start, span_p_end, idxs_p = chosen_p
        used_plausible.add((record_p["id"], span_p_start, span_p_end))
        placed_plausible.append(
            _aquit_doc(
                surface=surface,
                phonemes=phonemes,
                entry=entry,
                record=record_p,
                span=(span_p_start, span_p_end),
                idxs=idxs_p,
                bucket_label="B_aquit_plausible",
                bucket_descr=(
                    f"v4 plausible Aquitanian candidate: surface {surface!r} "
                    f"placed in clean accountancy inscription {record_p['id']} "
                    f"(semantic_compat ≥ 0.5)."
                ),
            )
        )
        # Wrong placement (same surface, votive_or_inscription)
        chosen_w = _pick_unused(wrong_pool, n, used_wrong)
        if chosen_w is None:
            raise RuntimeError(
                f"wrong: could not place {surface!r} in any clean votive inscription"
            )
        record_w, span_w_start, span_w_end, idxs_w = chosen_w
        used_wrong.add((record_w["id"], span_w_start, span_w_end))
        placed_wrong.append(
            _aquit_doc(
                surface=surface,
                phonemes=phonemes,
                entry=entry,
                record=record_w,
                span=(span_w_start, span_w_end),
                idxs=idxs_w,
                bucket_label="C_aquit_wrong",
                bucket_descr=(
                    f"v4 deliberately-wrong Aquitanian candidate: surface "
                    f"{surface!r} placed in clean votive_or_inscription "
                    f"{record_w['id']} (semantic_compat ≤ 0.25). The phoneme "
                    f"order is unchanged from the plausible bucket; only the "
                    f"inscription's genre context differs."
                ),
            )
        )
    return placed_plausible, placed_wrong


def _pick_unused(
    record_pool: list[dict],
    n_phonemes: int,
    used: set[tuple[str, int, int]],
) -> tuple[dict, int, int, list[int]] | None:
    """First (record, window) where the syllabograms in the window are pairwise
    distinct and the (id, span_start, span_end) triple is not yet used."""
    for record in record_pool:
        tokens = record["tokens"]
        for span_start, span_end, idxs in _candidate_windows(tokens, n_phonemes):
            signs = [tokens[i] for i in idxs]
            if len(set(signs)) != n_phonemes:
                continue
            key = (record["id"], span_start, span_end)
            if key in used:
                continue
            return record, span_start, span_end, idxs
    return None


def _aquit_doc(
    *,
    surface: str,
    phonemes: list[str],
    entry: dict,
    record: dict,
    span: tuple[int, int],
    idxs: list[int],
    bucket_label: str,
    bucket_descr: str,
) -> dict:
    tokens = record["tokens"]
    signs = [tokens[i] for i in idxs]
    sign_to_phoneme = dict(zip(signs, phonemes))
    bucket_kind = "plausible" if "plausible" in bucket_label else "wrong"
    name = f"v4_aquit_{bucket_kind}_{_slug(surface)}_{_slug(record['id'])}"
    notes = (
        f"v4 bucket {bucket_label} (mg-7c8c). "
        f"Source pool entry: surface={surface!r} "
        f"(semantic_field={entry.get('semantic_field')!r}, "
        f"region={entry.get('region')!r}). "
        f"Site={record['site']}; genre_hint={record.get('genre_hint')}; "
        f"confidence={record.get('transcription_confidence')}. "
        f"The phoneme order is the pool entry's; the wrong-bucket variant "
        f"differs from the plausible-bucket variant ONLY in the inscription's "
        f"genre context."
    )
    citation = entry.get("citation") or "see pool source_citation"
    return {
        "doc": _build_doc(
            name=name,
            description=bucket_descr,
            source_pool="aquitanian",
            surface=surface,
            phonemes=phonemes,
            gloss_hint=entry.get("gloss") or "",
            citation=citation,
            inscription_id=record["id"],
            span=span,
            sign_to_phoneme=sign_to_phoneme,
            notes=notes,
        ),
        "bucket": bucket_label,
        "spec": {"surface": surface, "phonemes": phonemes},
    }


# ---------------------------------------------------------------------------
# Bucket D: 16 new plausible pre-Greek toponym candidates.
# ---------------------------------------------------------------------------
#
# Each candidate has a 2-5 phoneme surface drawn from a longer toponym in
# pools/toponym.yaml (prefix, suffix, or substring), with the toponym
# itself cited per Beekes 2010. Placement: first clean accountancy
# inscription on Crete (region_compat=1.0 for pre_greek × Crete) where
# the surface's phoneme count fits a distinct-sign window. The pool
# entry itself is the citation source.

# Each tuple is (candidate_surface, phonemes, source_toponym_in_pool, gloss_hint).
_TOPONYM_FRAGMENT_SPECS: list[tuple[str, list[str], str, str]] = [
    # 3-phoneme prefixes from canonical Aegean substrate toponyms.
    ("kno", ["k", "n", "o"], "knossos", "Knossos prefix; pre-Greek substrate -ssos toponym"),
    ("phai", ["p", "h", "a", "i"], "phaistos", "Phaistos prefix; pre-Greek -stos suffix"),
    ("amn", ["a", "m", "n"], "amnisos", "Amnisos prefix; pre-Greek -isos suffix"),
    ("tul", ["t", "u", "l"], "tulissos", "Tylissos prefix; pre-Greek -ssos toponym"),
    ("kud", ["k", "u", "d"], "kudonia", "Kydonia prefix"),
    ("ita", ["i", "t", "a"], "itanos", "Itanos prefix"),
    ("leb", ["l", "e", "b"], "lebena", "Lebena prefix"),
    ("prai", ["p", "r", "a", "i"], "praisos", "Praisos prefix; Eteocretan associations"),
    ("gor", ["g", "o", "r"], "gortyn", "Gortyn prefix"),
    # 3-4 phoneme prefixes from broader Aegean / mainland substrate.
    ("kor", ["k", "o", "r"], "korinthos", "Korinthos prefix; pre-Greek -nthos suffix"),
    ("par", ["p", "a", "r"], "parnassos", "Parnassos prefix"),
    ("hum", ["h", "u", "m"], "hymettos", "Hymettos prefix; pre-Greek -ttos suffix"),
    ("eru", ["e", "r", "u"], "erymanthos", "Erymanthos prefix"),
    ("muk", ["m", "u", "k"], "mukenai", "Mukenai prefix"),
    # 4-5 phoneme placements drawn from longer toponyms.
    ("paro", ["p", "a", "r", "o"], "paros", "Paros (4-phoneme prefix; Cycladic substrate)"),
    ("mel", ["m", "e", "l"], "melos", "Melos prefix; Cycladic island with Linear-A finds"),
]


def build_toponyms(records: list[dict], pool: dict) -> list[dict]:
    cretan_sites = {
        "Haghia Triada",
        "Khania",
        "Phaistos",
        "Zakros",
        "Knossos",
        "Mallia",
        "Arkhanes",
        "Tylissos",
        "Gournia",
        "Pyrgos",
        "Papoura",
        "Psykhro",
        "Syme",
    }
    record_pool = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and r.get("genre_hint") == "accountancy"
            and r.get("site") in cretan_sites
        ],
        key=lambda r: r["id"],
    )
    placed: list[dict] = []
    used: set[tuple[str, int, int]] = set()
    for surface, phonemes, source_toponym, gloss_hint in _TOPONYM_FRAGMENT_SPECS:
        n = len(phonemes)
        chosen = _pick_unused(record_pool, n, used)
        if chosen is None:
            raise RuntimeError(
                f"could not place toponym candidate {surface!r}"
            )
        record, span_start, span_end, idxs = chosen
        used.add((record["id"], span_start, span_end))
        tokens = record["tokens"]
        signs = [tokens[i] for i in idxs]
        sign_to_phoneme = dict(zip(signs, phonemes))
        toponym_entry = next(
            e for e in pool["entries"] if e["surface"] == source_toponym
        )
        citation = (
            f"Beekes 2010 _Etymological Dictionary of Greek_ vol. 2 "
            f"appendix s.v. {source_toponym} (cf. pools/toponym.yaml entry); "
            f"this candidate proposes the {surface!r} fragment of the "
            f"{source_toponym!r} toponym pinned at {record['id']} tokens "
            f"[{span_start}..{span_end}]."
        )
        notes = (
            f"v4 bucket D_toponym_plausible (mg-7c8c). "
            f"Source toponym in pools/toponym.yaml: {source_toponym!r} "
            f"(full phonemes={toponym_entry['phonemes']}). "
            f"Site={record['site']} (Cretan; pre_greek × Crete = 1.0); "
            f"genre_hint={record.get('genre_hint')}; "
            f"confidence={record.get('transcription_confidence')}. "
            f"Expected geographic_genre_fit_v1 ≈ 0.4*1.0 + 0.6*0.75 = 0.85."
        )
        description = (
            f"v4 plausible pre-Greek toponym candidate: {surface!r} "
            f"({'-'.join(phonemes)}) — {gloss_hint}. Pinned at {record['id']} "
            f"tokens [{span_start}..{span_end}]."
        )
        name = f"v4_pgreek_{_slug(surface)}_{_slug(record['id'])}"
        doc = _build_doc(
            name=name,
            description=description,
            source_pool="toponym",
            surface=surface,
            phonemes=phonemes,
            gloss_hint=gloss_hint,
            citation=citation,
            inscription_id=record["id"],
            span=(span_start, span_end),
            sign_to_phoneme=sign_to_phoneme,
            notes=notes,
        )
        placed.append({"doc": doc, "bucket": "D_toponym_plausible", "spec": surface})
    return placed


# ---------------------------------------------------------------------------
# Bucket E: 16 new random scrambles.
# ---------------------------------------------------------------------------
#
# Random IPA strings of length 2-5; placed in clean inscriptions chosen
# uniformly at random from the corpus. Seed=4242 frozen for v4. The
# alphabet is a fixed list of IPA glyphs that are unlikely to be the
# canonical reading of any AB sign under existing substrate hypotheses,
# matching the existing mg-fb23 scramble bucket's qʁ/wj/ɣɲ choices.

_SCRAMBLE_IPA_INVENTORY: tuple[str, ...] = (
    "q",  # voiceless uvular stop — not in any substrate hypothesis here
    "ʁ",  # voiced uvular fricative
    "ɣ",  # voiced velar fricative
    "ɲ",  # palatal nasal
    "ʔ",  # glottal stop
    "ʕ",  # voiced pharyngeal fricative
    "ʐ",  # voiced retroflex fricative
    "ʂ",  # voiceless retroflex fricative
    "ɖ",  # voiced retroflex stop
    "ʈ",  # voiceless retroflex stop
)


def build_scrambles(records: list[dict]) -> list[dict]:
    rng = random.Random(_RANDOM_SEED)
    record_pool = sorted(
        [
            r
            for r in records
            if r.get("transcription_confidence") == "clean"
            and int(r.get("n_signs", 0)) >= 5
        ],
        key=lambda r: r["id"],
    )
    placed: list[dict] = []
    used_records: set[str] = set()
    attempts = 0
    while len(placed) < 16:
        attempts += 1
        if attempts > 500:
            raise RuntimeError(
                "scramble builder: exhausted attempts; pool exhausted or rule misconfigured"
            )
        # Random length in [2, 5].
        n = rng.randint(2, 5)
        # Sample n distinct phoneme labels by sampling without replacement;
        # this guarantees the resulting sign_to_phoneme dict can map distinct
        # signs to distinct random phonemes (mirrors the dict-distinct-keys
        # invariant we enforce at scoring time).
        phonemes = rng.sample(_SCRAMBLE_IPA_INVENTORY, n)
        # Random clean inscription with a fitting distinct-sign window.
        # Re-shuffle a copy of the pool so the choice is deterministic from
        # the rng state.
        shuffled = list(record_pool)
        rng.shuffle(shuffled)
        chosen: tuple[dict, int, int, list[int]] | None = None
        for record in shuffled:
            if record["id"] in used_records:
                continue
            w = _find_window(record, n, distinct=True)
            if w is None:
                continue
            chosen = (record, *w)
            break
        if chosen is None:
            # Try without used_records constraint (so multiple scrambles can
            # share an inscription if necessary, still seed-deterministic).
            for record in shuffled:
                w = _find_window(record, n, distinct=True)
                if w is None:
                    continue
                chosen = (record, *w)
                break
        if chosen is None:
            continue
        record, span_start, span_end, idxs = chosen
        used_records.add(record["id"])

        tokens = record["tokens"]
        signs = [tokens[i] for i in idxs]
        sign_to_phoneme = dict(zip(signs, phonemes))
        surface = "".join(phonemes)
        seed_label = f"v4E{len(placed) + 1:02d}"
        name = f"v4_scramble_{_slug(record['id'])}_{seed_label}"
        notes = (
            f"v4 bucket E_scramble (mg-7c8c). Random IPA from "
            f"_SCRAMBLE_IPA_INVENTORY of length {n}; rng seed=4242 "
            f"(_RANDOM_SEED in scripts/build_curated_v4.py). "
            f"Site={record['site']}; genre_hint={record.get('genre_hint')}; "
            f"confidence={record.get('transcription_confidence')}. "
            f"Expected: control_z near 0 (random IPA has no a-priori reason "
            f"to align with corpus position fingerprints)."
        )
        description = (
            f"v4 random-scramble baseline. {n} random IPA phonemes "
            f"({'-'.join(phonemes)}) at {record['id']} tokens "
            f"[{span_start}..{span_end}]. Not a real lexeme."
        )
        citation = (
            f"Random IPA selection from "
            f"`_SCRAMBLE_IPA_INVENTORY` (scripts/build_curated_v4.py); "
            f"seed=4242. Not a real lexeme."
        )
        doc = _build_doc(
            name=name,
            description=description,
            source_pool="random_scramble",
            surface=surface,
            phonemes=phonemes,
            gloss_hint="(no semantic content; randomly selected IPA characters)",
            citation=citation,
            inscription_id=record["id"],
            span=(span_start, span_end),
            sign_to_phoneme=sign_to_phoneme,
            notes=notes,
        )
        placed.append({"doc": doc, "bucket": "E_scramble", "spec": surface})
    return placed


# ---------------------------------------------------------------------------
# Manifest assembly + write
# ---------------------------------------------------------------------------


_BUCKET_TAG_MAP = {
    "A_linear_b_anchor": ("linear_b_carryover", "anchor"),
    "B_aquit_plausible": ("aquitanian", "plausible"),
    "C_aquit_wrong": ("aquitanian", "wrong"),
    "D_toponym_plausible": ("toponym", "plausible"),
    "E_scramble": ("random_scramble", "scramble"),
}


_EXISTING_CURATED_TO_BUCKET = {
    # The 4 mg-fb23 anchors
    "anchor_kuro_HT100": "A_linear_b_anchor",
    "anchor_kiro_HT1": "A_linear_b_anchor",
    "anchor_ara_HT1": "A_linear_b_anchor",
    "anchor_taina_HT39": "A_linear_b_anchor",
    # The 4 mg-fb23 plausible Aquitanian
    "aquit_ai_HT115b": "B_aquit_plausible",
    "aquit_in_PH6": "B_aquit_plausible",
    "aquit_ir_HTWa1006": "B_aquit_plausible",
    "aquit_ur_HT25a": "B_aquit_plausible",
    # The 4 mg-fb23 deliberately-wrong Aquitanian
    "aquit_wrong_ai_GO_Wc_1a": "C_aquit_wrong",
    "aquit_wrong_in_HT89": "C_aquit_wrong",
    "aquit_wrong_ir_HT10a": "C_aquit_wrong",
    "aquit_wrong_ur_PA1": "C_aquit_wrong",
    # The 4 mg-fb23 pgreek toponyms (now treated as bucket D priors)
    "pgreek_assos_HT20": "D_toponym_plausible",
    "pgreek_inthos_HT95a": "D_toponym_plausible",
    "pgreek_korinth_HT17": "D_toponym_plausible",
    "pgreek_uros_HT11a": "D_toponym_plausible",
    # The 4 mg-fb23 scrambles
    "scramble_HT100_E1": "E_scramble",
    "scramble_HT17_E3": "E_scramble",
    "scramble_HT1_E4": "E_scramble",
    "scramble_HT25a_E2": "E_scramble",
}


def _load_existing_curated() -> list[dict]:
    rows: list[dict] = []
    for hyp_path in sorted(_CURATED_DIR.glob("*.yaml")):
        if hyp_path.name.startswith("v4_"):
            continue
        with hyp_path.open("r", encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=_StringDateLoader)
        if doc is None or doc.get("schema_version") != "candidate_equation.v1":
            continue
        bucket = _EXISTING_CURATED_TO_BUCKET.get(doc["name"])
        if bucket is None:
            raise RuntimeError(
                f"unknown bucket for existing curated hypothesis {doc['name']!r}"
            )
        h = _canonical_hash(doc)
        equation = doc["equation"]
        rows.append(
            {
                "bucket": bucket,
                "source_pool": _BUCKET_TAG_MAP[bucket][0],
                "bucket_kind": _BUCKET_TAG_MAP[bucket][1],
                "hypothesis_name": doc["name"],
                "inscription_id": equation["inscription_id"],
                "span_start": equation["span"][0],
                "span_end": equation["span"][1],
                "hypothesis_path": hyp_path.relative_to(_REPO_ROOT).as_posix(),
                "hypothesis_hash": h,
                "is_v4_new": False,
            }
        )
    return rows


def _validate_doc(doc: dict, validator: Draft202012Validator) -> None:
    validator.validate(doc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument(
        "--aquitanian-pool", type=Path, default=_DEFAULT_AQUITANIAN_POOL
    )
    parser.add_argument(
        "--toponym-pool", type=Path, default=_DEFAULT_TOPONYM_POOL
    )
    parser.add_argument(
        "--curated-dir", type=Path, default=_CURATED_DIR
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Don't write any files; just exercise the builders and print a summary.",
    )
    args = parser.parse_args(argv)

    records = _load_corpus(args.corpus)
    counts = _sign_corpus_counts(records)
    aq_pool = _load_pool(args.aquitanian_pool)
    top_pool = _load_pool(args.toponym_pool)
    schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    # Acceptance check: each anchor sign occurs ≥10 times.
    for spec in _ANCHOR_SPECS:
        for s in spec["signs"]:
            if counts.get(s, 0) < 10:
                raise RuntimeError(
                    f"anchor {spec['surface']!r} sign {s} has corpus count "
                    f"{counts.get(s, 0)} (< 10 acceptance threshold)"
                )

    new_anchor_rows = build_anchors(records)
    new_plausible_rows, new_wrong_rows = build_aquit_plausible_and_wrong(
        records, aq_pool
    )
    new_toponym_rows = build_toponyms(records, top_pool)
    new_scramble_rows = build_scrambles(records)

    new_rows = (
        new_anchor_rows
        + new_plausible_rows
        + new_wrong_rows
        + new_toponym_rows
        + new_scramble_rows
    )
    assert len(new_rows) == 80, f"expected 80 new entries, got {len(new_rows)}"

    # Validate and prepare write list.
    written_files: list[tuple[Path, str]] = []
    new_manifest_rows: list[dict] = []
    for row in new_rows:
        doc = row["doc"]
        _validate_doc(doc, validator)
        h = _canonical_hash(doc)
        out_path = args.curated_dir / f"{doc['name']}.yaml"
        yaml_text = _dump_yaml(doc)
        written_files.append((out_path, yaml_text))
        new_manifest_rows.append(
            {
                "bucket": row["bucket"],
                "source_pool": _BUCKET_TAG_MAP[row["bucket"]][0],
                "bucket_kind": _BUCKET_TAG_MAP[row["bucket"]][1],
                "hypothesis_name": doc["name"],
                "inscription_id": doc["equation"]["inscription_id"],
                "span_start": doc["equation"]["span"][0],
                "span_end": doc["equation"]["span"][1],
                "hypothesis_path": out_path.relative_to(_REPO_ROOT).as_posix(),
                "hypothesis_hash": h,
                "is_v4_new": True,
            }
        )

    # Existing curated rows.
    existing_rows = _load_existing_curated()
    if len(existing_rows) != 20:
        raise RuntimeError(
            f"expected 20 existing curated rows, got {len(existing_rows)}"
        )

    manifest_rows = existing_rows + new_manifest_rows
    bucket_order = [
        "A_linear_b_anchor",
        "B_aquit_plausible",
        "C_aquit_wrong",
        "D_toponym_plausible",
        "E_scramble",
    ]
    manifest_rows.sort(
        key=lambda r: (
            bucket_order.index(r["bucket"]),
            not r["is_v4_new"],  # existing first within bucket → False sorts first
            r["hypothesis_name"],
        )
    )
    # Actually we want existing-then-new sorted by name within each.
    manifest_rows.sort(
        key=lambda r: (
            bucket_order.index(r["bucket"]),
            r["is_v4_new"],  # False(existing) sorts before True(new)
            r["hypothesis_name"],
        )
    )

    # Acceptance check: 100 hypotheses across 5 buckets, 20 each.
    by_bucket: dict[str, list[dict]] = {}
    for r in manifest_rows:
        by_bucket.setdefault(r["bucket"], []).append(r)
    for b in bucket_order:
        if len(by_bucket.get(b, [])) != 20:
            raise RuntimeError(
                f"bucket {b} has {len(by_bucket.get(b, []))} entries; expected 20"
            )

    if args.no_write:
        print(json.dumps({"new": len(new_rows), "total": len(manifest_rows)}, indent=2))
        return 0

    args.curated_dir.mkdir(parents=True, exist_ok=True)
    for out_path, yaml_text in written_files:
        # Idempotent write: only rewrite if content differs.
        if out_path.exists() and out_path.read_text(encoding="utf-8") == yaml_text:
            continue
        out_path.write_text(yaml_text, encoding="utf-8")

    with _MANIFEST_PATH.open("w", encoding="utf-8") as fh:
        for row in manifest_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "new_entries_written": len(written_files),
        "manifest_rows": len(manifest_rows),
        "by_bucket": {b: len(by_bucket[b]) for b in bucket_order},
        "manifest_path": _MANIFEST_PATH.relative_to(_REPO_ROOT).as_posix(),
        "scramble_rng_seed": _RANDOM_SEED,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
