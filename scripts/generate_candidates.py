#!/usr/bin/env python3
"""Bulk candidate-equation generator.

Walks one substrate-root pool against the Linear A corpus and emits a
candidate-equation hypothesis YAML per surviving (pool entry × inscription
× window) triple. Output paths:

    hypotheses/auto/<pool>/<sha8>.yaml          one YAML per candidate
    hypotheses/auto/<pool>.manifest.jsonl       one manifest line per YAML

The generator is **deterministic and idempotent** — re-running with the
same pool YAML and the same corpus snapshot produces byte-identical output.
Manifest entries are sorted by (pool_entry_index, inscription_id, span_start)
before they are written; YAML filenames are content-addressed (sha8 of the
canonical hypothesis hash) so the same window always yields the same path.

Skip rules (mg-fb23 / mg-f832 acceptance):
  * Pool entries whose phonemes span fewer than 2 distinct phoneme classes
    (V/S/C) are skipped wholesale; running them would force ``control_std=0``
    in ``local_fit_v0``.
  * Inscriptions with ``transcription_confidence == 'fragmentary'`` are
    skipped, as are those with ``n_signs < len(phonemes)``.
  * Windows containing a DIV token are skipped (they would cross a SigLA
    word boundary).
  * Windows whose participating syllabograms are not pairwise distinct are
    skipped (``sign_to_phoneme`` is a dict and cannot carry duplicate keys).

The cap ``--cap-per-entry K`` (default 50) bounds the number of candidates
emitted for any single pool entry, so a 100-entry pool produces at most
~5,000 hypotheses on the existing 761-record SigLA corpus.

Usage:
    python3 scripts/generate_candidates.py --pool aquitanian
    python3 scripts/generate_candidates.py --pool aquitanian --cap-per-entry 25
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_DEFAULT_HYPOTHESES_DIR = _REPO_ROOT / "hypotheses" / "auto"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"

# Bare-syllabogram pattern: AB## or A###. Anything else (DIV, LOG:*, FRAC:*,
# [?], [?:*]) is *not* a syllabogram for the generator's purposes.
_SYLLABOGRAM_RE = re.compile(r"^A[B]?\d+$")
_DIV_TOKEN = "DIV"

_VOWELS = frozenset("aeiouAEIOU")
_SONORANTS = frozenset("lrnmñLRNMÑ")


def _phoneme_class(p: str) -> str:
    """Mirror of ``harness.metrics._class_of`` — duplicated here to keep the
    generator self-contained and to avoid importing the metric module just
    for a 5-line classifier."""
    if not p:
        return "C"
    h = p[0]
    if h in _VOWELS:
        return "V"
    if h in _SONORANTS:
        return "S"
    return "C"


def _is_syllabogram(tok: str) -> bool:
    return bool(_SYLLABOGRAM_RE.fullmatch(tok))


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings; mirrors the loader
    in ``harness.hypothesis`` so dates round-trip rather than becoming
    ``datetime`` objects."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_pool(pool_name: str, pools_dir: Path) -> dict:
    pool_path = pools_dir / f"{pool_name}.yaml"
    with pool_path.open("r", encoding="utf-8") as fh:
        pool = yaml.load(fh, Loader=_StringDateLoader)
    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(pool)
    if pool["pool"] != pool_name:
        raise ValueError(
            f"pool YAML declares pool={pool['pool']!r}, but file basename is {pool_name!r}"
        )
    return pool


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


def _candidate_windows(
    tokens: list[str], n_phonemes: int
) -> list[tuple[int, int, list[int]]]:
    """Return all windows in ``tokens`` whose syllabogram-only count equals
    ``n_phonemes`` and which do not cross a DIV.

    Each window is returned as ``(span_start, span_end, syllabogram_indices)``
    with ``span_start`` and ``span_end`` inclusive token indices and
    ``syllabogram_indices`` listing the absolute token positions of the N
    syllabograms picked up. The two endpoints are always syllabograms (so the
    span is the tightest one consistent with the count).
    """
    if n_phonemes <= 0:
        return []
    windows: list[tuple[int, int, list[int]]] = []
    # Partition tokens into DIV-bounded blocks; record absolute indices of the
    # syllabograms in each block.
    block_syllabograms: list[int] = []
    for i, tok in enumerate(tokens):
        if tok == _DIV_TOKEN:
            if len(block_syllabograms) >= n_phonemes:
                _emit_windows_in_block(block_syllabograms, n_phonemes, windows)
            block_syllabograms = []
        elif _is_syllabogram(tok):
            block_syllabograms.append(i)
        # other tokens (LOG:*, FRAC:*, [?], [?:*]) are kept inside the block
        # without advancing the syllabogram index list.
    if len(block_syllabograms) >= n_phonemes:
        _emit_windows_in_block(block_syllabograms, n_phonemes, windows)
    return windows


def _emit_windows_in_block(
    syllabograms: list[int],
    n_phonemes: int,
    out: list[tuple[int, int, list[int]]],
) -> None:
    for i in range(0, len(syllabograms) - n_phonemes + 1):
        idxs = syllabograms[i : i + n_phonemes]
        out.append((idxs[0], idxs[-1], idxs))


def _canonical_hash(doc: dict) -> str:
    """Mirror of ``harness.hypothesis.canonical_hash`` — kept inline so the
    generator does not need to import the harness package (the harness module
    eagerly opens schema files and instantiates validators on import, which
    we don't need for the generator)."""
    payload = json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _build_hypothesis_doc(
    *,
    pool_name: str,
    entry: dict,
    inscription: dict,
    span_start: int,
    span_end: int,
    syllabogram_indices: list[int],
) -> dict:
    """Construct one candidate-equation hypothesis dict.

    Field order is fixed for human readability when the YAML is written; the
    canonical hash uses sort_keys=True so order has no effect on the hash."""
    tokens = inscription["tokens"]
    signs = [tokens[i] for i in syllabogram_indices]
    phonemes = list(entry["phonemes"])
    sign_to_phoneme = dict(zip(signs, phonemes))

    citation = entry.get("citation") or "see pool source_citation"
    surface = entry["surface"]
    # Slug the surface too: pools may carry non-ASCII characters in the
    # surface form (e.g. Etruscan śuthina), but the hypothesis-name schema
    # restricts ``name`` to [A-Za-z0-9_]. The surface itself is preserved
    # verbatim under ``root.surface``; only the name slug is sanitized.
    name = f"auto_{pool_name}_{_slug(surface)}_{_slug(inscription['id'])}_{span_start}_{span_end}"
    name = _trim_name(name)

    description = (
        f"Auto-generated candidate equation: pool={pool_name!r} entry "
        f"surface={surface!r} pinned to {inscription['id']} tokens "
        f"[{span_start}..{span_end}]."
    )

    doc = {
        "schema_version": "candidate_equation.v1",
        "name": name,
        "description": description,
        "author": "scripts/generate_candidates.py",
        "created": "2026-05-04",
        "source_pool": pool_name,
        "root": {
            "surface": surface,
            "phonemes": phonemes,
        },
        "equation": {
            "inscription_id": inscription["id"],
            "span": [span_start, span_end],
            "sign_to_phoneme": sign_to_phoneme,
        },
    }
    if entry.get("gloss"):
        doc["root"]["gloss_hint"] = entry["gloss"]
    doc["root"]["citation"] = citation
    return doc


_NAME_RE = re.compile(r"[^A-Za-z0-9_]")


def _slug(s: str) -> str:
    return _NAME_RE.sub("_", s)


def _trim_name(name: str, limit: int = 80) -> str:
    """Schema constrains hypothesis name to <= 80 chars. Long inscription IDs
    plus long surface forms can blow past that; we hash the overflow tail and
    splice in a short suffix so the trimmed name remains unique and stable.
    """
    if len(name) <= limit:
        return name
    head = name[: limit - 9]  # leave 9 chars for "_" + 8-hex tail
    tail_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    return f"{head}_{tail_hash}"


def _dump_yaml(doc: dict) -> str:
    """Stable YAML dump for hypothesis files. ``sort_keys=False`` preserves
    the field-order we built; flow_style=False keeps it human-readable."""
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


def generate(
    *,
    pool_name: str,
    cap_per_entry: int,
    corpus_path: Path,
    pools_dir: Path,
    hypotheses_dir: Path,
    progress: bool = True,
) -> dict:
    """Drive the bulk generator. Returns a summary dict."""
    pool = _load_pool(pool_name, pools_dir)
    records = _load_corpus(corpus_path)

    out_dir = hypotheses_dir / pool_name
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = hypotheses_dir / f"{pool_name}.manifest.jsonl"

    manifest_rows: list[dict] = []
    skipped_single_class = 0
    emitted = 0
    capped = 0

    for entry_idx, entry in enumerate(pool["entries"]):
        phonemes = list(entry["phonemes"])
        n = len(phonemes)
        classes = {_phoneme_class(p) for p in phonemes}
        if len(classes) < 2:
            skipped_single_class += 1
            continue

        per_entry_count = 0
        # Records are pre-sorted by id; deterministic ordering follows.
        for record in records:
            if record.get("transcription_confidence") == "fragmentary":
                continue
            if int(record.get("n_signs", 0)) < n:
                continue
            tokens = record["tokens"]
            for span_start, span_end, syll_idxs in _candidate_windows(tokens, n):
                signs = [tokens[i] for i in syll_idxs]
                if len(set(signs)) != n:
                    continue  # duplicate sign would collapse the dict
                if per_entry_count >= cap_per_entry:
                    capped += 1
                    break
                doc = _build_hypothesis_doc(
                    pool_name=pool_name,
                    entry=entry,
                    inscription=record,
                    span_start=span_start,
                    span_end=span_end,
                    syllabogram_indices=syll_idxs,
                )
                h = _canonical_hash(doc)
                sha8 = h.split(":", 1)[1][:8]
                yaml_path = out_dir / f"{sha8}.yaml"
                yaml_text = _dump_yaml(doc)
                # Atomic-style write: only rewrite if content differs (keeps
                # mtimes stable across no-op runs and reduces git churn).
                if not yaml_path.exists() or yaml_path.read_text(
                    encoding="utf-8"
                ) != yaml_text:
                    yaml_path.write_text(yaml_text, encoding="utf-8")
                rel_path = yaml_path.relative_to(_REPO_ROOT).as_posix()
                manifest_rows.append(
                    {
                        "pool": pool_name,
                        "pool_entry_index": entry_idx,
                        "pool_entry_surface": entry["surface"],
                        "inscription_id": record["id"],
                        "span_start": span_start,
                        "span_end": span_end,
                        "hypothesis_path": rel_path,
                        "hypothesis_hash": h,
                    }
                )
                per_entry_count += 1
                emitted += 1
            else:
                continue
            break  # cap reached for this pool entry; advance to next entry
        if progress and (entry_idx + 1) % 25 == 0:
            print(
                f"  pool entry {entry_idx + 1}/{len(pool['entries'])} "
                f"({entry['surface']}): {per_entry_count} candidates",
                file=sys.stderr,
            )

    # Sort manifest deterministically.
    manifest_rows.sort(
        key=lambda r: (r["pool_entry_index"], r["inscription_id"], r["span_start"])
    )

    # Detect orphaned YAML files in the output directory and prune them. This
    # keeps the directory consistent with the manifest after pool edits.
    expected = {Path(r["hypothesis_path"]).name for r in manifest_rows}
    pruned = 0
    for existing in sorted(out_dir.glob("*.yaml")):
        if existing.name not in expected:
            existing.unlink()
            pruned += 1

    with manifest_path.open("w", encoding="utf-8") as fh:
        for row in manifest_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {
        "pool": pool_name,
        "pool_entries": len(pool["entries"]),
        "skipped_single_class_entries": skipped_single_class,
        "candidates_emitted": emitted,
        "candidates_pruned_orphaned": pruned,
        "entries_capped": capped,
        "manifest_path": manifest_path.relative_to(_REPO_ROOT).as_posix(),
        "out_dir": out_dir.relative_to(_REPO_ROOT).as_posix(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--pool",
        required=True,
        help="Pool name (matches pools/<name>.yaml basename).",
    )
    parser.add_argument(
        "--cap-per-entry",
        type=int,
        default=50,
        help="Maximum candidates emitted per pool entry (default: %(default)s).",
    )
    parser.add_argument(
        "--corpus", type=Path, default=_DEFAULT_CORPUS, help="Corpus JSONL path."
    )
    parser.add_argument(
        "--pools-dir",
        type=Path,
        default=_DEFAULT_POOLS_DIR,
        help="Directory containing pool YAMLs.",
    )
    parser.add_argument(
        "--hypotheses-dir",
        type=Path,
        default=_DEFAULT_HYPOTHESES_DIR,
        help="Directory under which generated hypotheses are written.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Suppress progress messages on stderr.",
    )
    args = parser.parse_args(argv)

    summary = generate(
        pool_name=args.pool,
        cap_per_entry=args.cap_per_entry,
        corpus_path=args.corpus,
        pools_dir=args.pools_dir,
        hypotheses_dir=args.hypotheses_dir,
        progress=not args.no_progress,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
