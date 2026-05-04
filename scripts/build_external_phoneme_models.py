#!/usr/bin/env python3
"""Build the external phoneme bigram models (mg-ee18, harness v8).

Reads the cleaned external corpora and emits two byte-deterministic
JSON models under ``harness/external_phoneme_models/``:

* ``basque.json`` — built from ``corpora/basque/text.txt`` (≥100 k
  chars; α = 0.1).
* ``etruscan.json`` — built from ``corpora/etruscan/words.txt`` (≥500
  word forms; α = 1.0).

The α choices are documented in
``harness/external_phoneme_model.py``: Basque is well-resourced so
minimal smoothing suffices; Etruscan is corpus-limited so larger α
keeps log-probs bounded for rare bigrams.

Idempotent. Re-runs against the same corpora produce byte-identical
JSON. The corpora themselves are reproducible from the committed
fetch / build scripts (see ``corpora/basque.README.md`` and
``corpora/etruscan.README.md``).

Usage::

    python3 scripts/build_external_phoneme_models.py
    python3 scripts/build_external_phoneme_models.py --only basque
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as a top-level script from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.external_phoneme_model import (
    build_model,
    tokenize_text,
    tokenize_word_list,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_BASQUE_TEXT = _REPO_ROOT / "corpora" / "basque" / "text.txt"
_DEFAULT_ETRUSCAN_WORDS = _REPO_ROOT / "corpora" / "etruscan" / "words.txt"
_OUT_DIR = _REPO_ROOT / "harness" / "external_phoneme_models"

_BASQUE_ALPHA = 0.1
_ETRUSCAN_ALPHA = 1.0


def build_basque(text_path: Path) -> tuple[str, dict]:
    text = text_path.read_text(encoding="utf-8")
    tokens = tokenize_text(text)
    n_chars = sum(1 for ch in text if ch.isalpha())
    n_words = sum(1 for w in text.split() if w)
    model = build_model(
        name="basque",
        tokens=tokens,
        alpha=_BASQUE_ALPHA,
        meta_extra={
            "source": "corpora/basque/text.txt (eu.wikipedia.org pinned revisions)",
            "license": "CC BY-SA 4.0",
            "n_alpha_chars": n_chars,
            "n_words": n_words,
            "alpha_rationale": (
                "0.1 — well-resourced corpus, minimal smoothing keeps "
                "rare-bigram log-probs informative."
            ),
        },
    )
    return model.to_json(), model.meta


def build_etruscan(words_path: Path) -> tuple[str, dict]:
    words = [
        line.strip()
        for line in words_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    tokens = tokenize_word_list(words)
    model = build_model(
        name="etruscan",
        tokens=tokens,
        alpha=_ETRUSCAN_ALPHA,
        meta_extra={
            "source": "corpora/etruscan/words.txt (Bonfante & Bonfante 2002 + TLE + supplementary)",
            "license": "fair-use citation of secondary sources; underlying inscriptions PD",
            "n_words": len(words),
            "n_chars": sum(len(w) for w in words),
            "alpha_rationale": (
                "1.0 — small corpus (~500-700 word forms); stronger smoothing "
                "keeps unobserved bigrams bounded away from -inf."
            ),
        },
    )
    return model.to_json(), model.meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--only",
        choices=("basque", "etruscan"),
        default=None,
        help="Build only one model (default: both).",
    )
    parser.add_argument(
        "--basque-text", type=Path, default=_DEFAULT_BASQUE_TEXT
    )
    parser.add_argument(
        "--etruscan-words", type=Path, default=_DEFAULT_ETRUSCAN_WORDS
    )
    parser.add_argument("--out-dir", type=Path, default=_OUT_DIR)
    args = parser.parse_args(argv)

    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.only in (None, "basque"):
        if not args.basque_text.exists():
            print(
                f"missing Basque corpus: {args.basque_text}\n"
                "run scripts/fetch_basque_corpus.py first.",
                file=sys.stderr,
            )
            return 2
        text, meta = build_basque(args.basque_text)
        out = args.out_dir / "basque.json"
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}  meta={meta}", file=sys.stderr)

    if args.only in (None, "etruscan"):
        if not args.etruscan_words.exists():
            print(
                f"missing Etruscan corpus: {args.etruscan_words}\n"
                "run scripts/build_etruscan_corpus.py first.",
                file=sys.stderr,
            )
            return 2
        text, meta = build_etruscan(args.etruscan_words)
        out = args.out_dir / "etruscan.json"
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}  meta={meta}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
