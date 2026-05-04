#!/usr/bin/env python3
"""Cross-check: every SigLA word-view seq-pattern must appear in our tokens.

Walks every cached SigLA word view, extracts the `word-match @ !seq-pattern:`
annotations, and verifies they are present (as substrings) in our generated
token stream after applying the documented inverse of v1 tokenization rules:

  - DIV         → '/'
  - [?]         → dropped (SigLA seq-patterns omit unreadable signs in-word)
  - [?:X]       → 'X'  (SigLA shows X in seq-pattern even if our reading is uncertain)
  - LOG:X       → dropped (SigLA seq-patterns omit logograms)
  - FRAC:X      → dropped (SigLA seq-patterns omit fractions)
  - X (other)   → 'X'

Exits 0 if every transcribed inscription matches; non-zero otherwise.
"""

import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "sigla"
ALL_JSONL = ROOT / "corpus" / "all.jsonl"


def main() -> int:
    if not ALL_JSONL.exists():
        print("corpus/all.jsonl missing; run scripts/parse_sigla.py first", file=sys.stderr)
        return 1
    if not CACHE.exists():
        print(".cache/sigla missing; run scripts/fetch_sigla.py first", file=sys.stderr)
        return 1

    recs = [json.loads(l) for l in ALL_JSONL.open(encoding="utf-8")]
    fail = 0
    examples: list[tuple[str, list[str]]] = []
    for r in recs:
        if r["n_signs"] == 0:
            continue
        enc = urllib.parse.quote(r["id"], safe="")
        word_path = CACHE / f"{enc}.word.html"
        if not word_path.exists():
            continue
        seqs = re.findall(
            r"word-match @ !seq-pattern:([A-Za-z0-9*\-]+)",
            word_path.read_text(encoding="utf-8", errors="replace"),
        )
        flat_parts: list[str] = []
        for t in r["tokens"]:
            if t == "DIV":
                flat_parts.append("/")
            elif t == "[?]":
                continue
            elif t.startswith("LOG:") or t.startswith("FRAC:"):
                continue
            elif t.startswith("[?:") and t.endswith("]"):
                flat_parts.append(t[3:-1])
            else:
                flat_parts.append(t.split(":", 1)[1] if ":" in t else t)
        flat = re.sub(r"(/+)", "/", "-".join(flat_parts)).strip("-/")
        missing = [
            s
            for s in seqs
            if s.replace("unclassified", "").replace("--", "-").strip("-") not in flat
        ]
        if missing:
            fail += 1
            if len(examples) < 5:
                examples.append((r["id"], missing[:3]))
    total = sum(1 for r in recs if r["n_signs"] > 0)
    print(f"{total - fail} / {total} records pass the SigLA seq-pattern cross-check")
    for rid, miss in examples:
        print(f"  fail {rid}: missing {miss}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
