#!/usr/bin/env python3
"""Parse cached LiBER tablet HTML into per-inscription JSON + a flat
Mycenaean-Greek word-form corpus.

Each cached page (``.cache/liber/tablet/<id>.html``) carries the
inscription's name and Mycenaean-Greek (Linear-B) transliteration in a
single ``<meta name="description" content="<NAME>, <TRANS>" />`` tag.
The transliteration uses lowercase syllabograms separated by hyphens
(``ku-ne-u``); uppercase logograms (``OVIS``, ``CROC``, ``LANA``,
``P``, ``M``); editorial / damage markers (``[``, ``]``, ``_``, ``$``,
``°``, ``↓``, ``‹ ›``, ``$vac.``, ``$vest.``, ``$mut.``, ``$inf.``).

What this script keeps for the Mycenaean-Greek LM corpus:

* lowercase ASCII letter sequences and hyphens, e.g. ``ku-ne-u``
* hyphens are then stripped to produce the contiguous phoneme word
  ``kuneu`` — that's exactly the form a char-bigram model wants

What this script drops:

* uppercase logograms (``OVIS``, ``CROC``, ``P``, ``M``, ``N``)
* digits, ``*``, ``$…``, ``°``, ``[``, ``]``, ``_``, ``↓``, ``‹``, ``›``
* the damage / vacat editorial markers
* single-character "words" (no bigram information)

Outputs (idempotent):

* ``corpora/linear_b/inscriptions/<id>.json`` — one JSON record per
  Linear-B tablet with ``name``, ``site`` (LiBER site prefix),
  ``words`` (list of lowercase phoneme words with no hyphens), and the
  raw transliteration line for traceability
* ``corpora/linear_b/all.jsonl`` — the same, one JSON object per line,
  sorted by ``(site, name, id)``
* ``corpora/linear_b/words.txt`` — flat sorted list of unique word
  forms, one per line. **This is the input the bigram-model builder
  reads.** This file is gitignored; the per-inscription JSON files and
  ``all.jsonl`` are committed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "liber"
DEFAULT_OUT = ROOT / "corpora" / "linear_b"

# Lowercase ASCII syllabogram clusters separated by hyphens. Each match
# is one Mycenaean-Greek "word".
WORD_RE = re.compile(r"[a-z]+(?:-[a-z]+)*")
# Pull NAME and TRANSLITERATION out of the meta description tag. The
# tablet name does NOT contain a comma; the transliteration may, so we
# split on the FIRST ", ".
META_DESC_RE = re.compile(
    r'<meta[^>]*\bname="description"[^>]*\bcontent="([^"]+)"',
    re.IGNORECASE,
)


def parse_one(html: str) -> tuple[str, str, list[str]]:
    """Return (name, raw_transliteration, [phoneme_word, ...])."""
    m = META_DESC_RE.search(html)
    if not m:
        return "", "", []
    desc = m.group(1)
    if ", " in desc:
        name, trans = desc.split(", ", 1)
    else:
        name, trans = desc, ""
    name = name.strip()
    trans = trans.strip()
    # Find lowercase syllabogram clusters; drop hyphens; require ≥2
    # chars so we don't end up training the bigram model on noise like
    # bare ``a`` or ``e`` markers.
    words: list[str] = []
    for tok in WORD_RE.findall(trans):
        joined = tok.replace("-", "")
        if len(joined) >= 2:
            words.append(joined)
    return name, trans, words


def site_prefix(name: str) -> str:
    """Return the LiBER site prefix from the tablet name (KN, PY, ...)."""
    return name.split()[0] if name else ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, default=CACHE)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)

    tablet_dir = args.cache / "tablet"
    if not tablet_dir.exists():
        print(f"missing tablet cache at {tablet_dir}", file=sys.stderr)
        return 2

    files = sorted(tablet_dir.glob("*.html"), key=lambda p: int(p.stem))
    if not files:
        print(f"no tablets cached at {tablet_dir}", file=sys.stderr)
        return 2

    inscriptions_dir = args.out_dir / "inscriptions"
    inscriptions_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    n_words_total = 0
    n_unique_words: set[str] = set()
    site_counts: dict[str, int] = {}
    n_skipped = 0

    for path in files:
        tablet_id = int(path.stem)
        html = path.read_text(encoding="utf-8", errors="replace")
        name, trans, words = parse_one(html)
        if not name:
            n_skipped += 1
            continue
        site = site_prefix(name)
        site_counts[site] = site_counts.get(site, 0) + 1
        rec = {
            "id": tablet_id,
            "name": name,
            "site": site,
            "transliteration": trans,
            "words": words,
        }
        records.append(rec)
        n_words_total += len(words)
        n_unique_words.update(words)

    # Sort by (site, name, id) for deterministic output ordering.
    records.sort(key=lambda r: (r["site"], r["name"], r["id"]))

    # Per-inscription JSON files.
    for rec in records:
        per_path = inscriptions_dir / f"{rec['id']}.json"
        per_path.write_text(
            json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    # Aggregate JSONL.
    all_path = args.out_dir / "all.jsonl"
    with all_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(
                json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n"
            )

    # Flat sorted unique word-form list, gitignored, fed into the LM
    # builder.
    words_path = args.out_dir / "words.txt"
    with words_path.open("w", encoding="utf-8") as fh:
        for w in sorted(n_unique_words):
            fh.write(w + "\n")

    print(
        json.dumps(
            {
                "n_inscriptions": len(records),
                "n_skipped": n_skipped,
                "n_words_total": n_words_total,
                "n_words_unique": len(n_unique_words),
                "sites": dict(sorted(site_counts.items(), key=lambda kv: -kv[1])),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
