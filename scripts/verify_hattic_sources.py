#!/usr/bin/env python3
"""Check every lexicon row against the scan it cites (mg-7f4db).

For each row of ``corpora/hattic/sources/lexicon.tsv`` this checks, on
the Internet Archive scan named by its ``source``:

  1. the scan leaf ``leaf`` carries the printed page number ``page``
     (IA ``*_page_numbers.json``), and
  2. ``quote`` is a verbatim substring of that leaf's OCR text (IA
     ``*_hocr.html``), after collapsing runs of whitespace.

The quotes are OCR text, not corrected text: the OCR misreads ḫ, š, u̯
and subscripts, which is why the ``printed`` and ``keyed`` columns were
read off the page images instead. This is the same machine check
mg-78856 applied in ~/research/hattic-semitic.

Needs network access on the first run; downloads are cached in
``.cache/hattic_sources/`` (gitignored). Not part of the unit tests.

  python3 scripts/verify_hattic_sources.py
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.build_hattic_pool import SOURCES  # noqa: E402


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_LEXICON = _REPO_ROOT / "corpora" / "hattic" / "sources" / "lexicon.tsv"
_CACHE = _REPO_ROOT / ".cache" / "hattic_sources"


def _fetch(url: str, dest: Path, tries: int = 5) -> Path:
    """Download ``url`` to ``dest`` once (cached). IA's download
    redirects drop connections now and then, so retry."""
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:  # noqa: S310
                data = r.read()
            break
        except OSError as exc:  # URLError, SSL EOF, timeouts
            if attempt == tries:
                raise
            print(f"retry {attempt} for {url}: {exc}", file=sys.stderr)
            time.sleep(5 * attempt)
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(dest)
    return dest


def _item_files(ia_id: str) -> dict[str, str]:
    """suffix → download URL for the item's hOCR and page-number map."""
    meta_path = _fetch(
        f"https://archive.org/metadata/{ia_id}", _CACHE / f"{ia_id}.metadata.json"
    )
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    out = {}
    for f in meta["files"]:
        for suffix in ("_hocr.html", "_page_numbers.json"):
            if f["name"].endswith(suffix):
                out[suffix] = (
                    f"https://archive.org/download/{ia_id}/"
                    + urllib.parse.quote(f["name"])
                )
    return out


def load_scan(ia_id: str) -> tuple[list[str], dict[int, str]]:
    """Return (OCR text per leaf, printed page number per leaf)."""
    files = _item_files(ia_id)
    hocr = _fetch(files["_hocr.html"], _CACHE / f"{ia_id}_hocr.html")
    pnum = _fetch(files["_page_numbers.json"], _CACHE / f"{ia_id}_page_numbers.json")
    text = hocr.read_text(encoding="utf-8")
    pages = re.split(r"<div class=['\"]ocr_page['\"]", text)[1:]
    leaves = []
    for p in pages:
        words = re.findall(r"<span class=['\"]ocrx_word['\"][^>]*>(.*?)</span>", p, re.S)
        leaves.append(" ".join(html.unescape(re.sub("<[^>]+>", "", w)) for w in words))
    numbers = {
        int(p["leafNum"]): str(p.get("pageNumber", ""))
        for p in json.loads(pnum.read_text(encoding="utf-8"))["pages"]
    }
    return leaves, numbers


def _collapse(s: str) -> str:
    return " ".join(s.split())


def verify(lexicon: Path) -> list[str]:
    with lexicon.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    scans = {key: load_scan(src["ia"]) for key, src in SOURCES.items()}
    problems = []
    for r in rows:
        leaves, numbers = scans[r["source"]]
        leaf = int(r["leaf"])
        if numbers.get(leaf) != r["page"]:
            problems.append(
                f"{r['lex_id']} {r['source']}: leaf {leaf} is printed page "
                f"{numbers.get(leaf)!r}, row says {r['page']}"
            )
        if _collapse(r["quote"]) not in _collapse(leaves[leaf]):
            problems.append(
                f"{r['lex_id']} {r['source']} p. {r['page']}: quote not on leaf "
                f"{leaf}: {r['quote']!r}"
            )
    print(f"checked {len(rows)} rows: {len(problems)} problem(s)", file=sys.stderr)
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lexicon", type=Path, default=_DEFAULT_LEXICON)
    args = parser.parse_args(argv)
    problems = verify(args.lexicon)
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
