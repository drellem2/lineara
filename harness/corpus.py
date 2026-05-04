"""Corpus loader, deterministic token-stream construction, and corpus-level
sign statistics that the local-fit metric reads."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Iterable

from . import INSCRIPTION_BOUNDARY


# Token classes from corpus_status.md tokenization rules. We treat any token
# that is **not** a word-divider or boundary marker as part of the surrounding
# word for position-in-word fingerprinting; non-syllabogram in-word tokens
# (LOG:, FRAC:, [?]) participate in the word's length but are not themselves
# fingerprinted as signs.
WORD_BREAK_TOKENS = frozenset({"DIV", INSCRIPTION_BOUNDARY})


def load_records(corpus_path: Path) -> list[dict]:
    """Load every record from a JSONL corpus file, in source order."""
    records: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def build_stream(records: Iterable[dict]) -> tuple[list[str], int]:
    """Build the deterministic token stream from corpus records.

    Filters out records with `n_signs == 0`. Sorts the remaining records by `id`
    (stable lexicographic). Concatenates each record's `tokens` array, inserting
    `INSCRIPTION_BOUNDARY` between adjacent records (no leading or trailing
    boundary marker).

    Returns the flat token list and the count of records that contributed.
    """
    kept = [r for r in records if int(r.get("n_signs", 0)) > 0]
    kept.sort(key=lambda r: r["id"])

    stream: list[str] = []
    for i, record in enumerate(kept):
        if i > 0:
            stream.append(INSCRIPTION_BOUNDARY)
        stream.extend(record["tokens"])
    return stream, len(kept)


def apply_mapping(stream: list[str], mapping: dict[str, str]) -> list[str]:
    """Replace each token in the mapping's domain with its phoneme value.

    Tokens outside the mapping (including INSCRIPTION_BOUNDARY) are left
    unchanged. The mapping is applied independently to each token; no rewriting
    of phoneme outputs.
    """
    if not mapping:
        return list(stream)
    return [mapping.get(t, t) for t in stream]


def iter_words(stream: list[str]) -> Iterable[list[str]]:
    """Yield each maximal run of non-break tokens between word-break markers.

    A "word" is the contiguous run between any two of {DIV, INSCRIPTION_BOUNDARY}
    (or between such a marker and the start/end of the stream). Empty runs
    (back-to-back markers) are skipped. The yielded list contains tokens
    verbatim, including non-syllabogram in-word tokens (LOG:, FRAC:, [?]).
    """
    buf: list[str] = []
    for tok in stream:
        if tok in WORD_BREAK_TOKENS:
            if buf:
                yield buf
                buf = []
        else:
            buf.append(tok)
    if buf:
        yield buf


def sign_position_fingerprints(stream: list[str]) -> dict[str, list[int]]:
    """Compute per-sign in-word position counts across the corpus.

    Returns a dict mapping each token observed in any word to a 4-tuple of
    integer counts ``[initial, medial, final, standalone]``:

    * ``initial`` — first token of a word of length >= 2.
    * ``medial`` — neither first nor last in a word of length >= 3.
    * ``final``  — last token of a word of length >= 2.
    * ``standalone`` — sole token in a word of length 1.

    Word boundaries are ``DIV`` and ``INSCRIPTION_BOUNDARY`` (see ``iter_words``).
    Non-syllabogram in-word tokens (LOG:, FRAC:, [?]) appear as their own
    keys; the metric only ever queries syllabogram entries, but counting them
    keeps the function self-contained.
    """
    counts: dict[str, list[int]] = {}
    for word in iter_words(stream):
        n = len(word)
        if n == 0:
            continue
        if n == 1:
            tok = word[0]
            counts.setdefault(tok, [0, 0, 0, 0])[3] += 1
            continue
        for i, tok in enumerate(word):
            row = counts.setdefault(tok, [0, 0, 0, 0])
            if i == 0:
                row[0] += 1
            elif i == n - 1:
                row[2] += 1
            else:
                row[1] += 1
    return counts


def corpus_snapshot(corpus_path: Path, repo_root: Path) -> str:
    """Return a stable identifier for the corpus snapshot.

    Prefers the git tree-sha of the directory containing the corpus file
    (typically ``corpus/``), provided that directory is committed and clean
    relative to HEAD. Falls back to a content hash of the corpus file when no
    git tree is available (e.g. ad-hoc test fixtures). Returned string format:
      - "git:<40-hex>"      (corpus directory tree at HEAD, clean)
      - "sha256:<64-hex>"   (corpus file content hash, fallback)
    """
    try:
        rel_dir = corpus_path.parent.relative_to(repo_root)
    except ValueError:
        rel_dir = None

    if rel_dir is not None:
        try:
            tree_sha = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", f"HEAD:{rel_dir.as_posix()}"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            diff = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo_root),
                    "diff",
                    "--quiet",
                    "HEAD",
                    "--",
                    rel_dir.as_posix(),
                ],
                capture_output=True,
                text=True,
            )
            if tree_sha and diff.returncode == 0:
                return f"git:{tree_sha}"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    import hashlib

    h = hashlib.sha256()
    with corpus_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"
