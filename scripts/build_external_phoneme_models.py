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
_DEFAULT_MYC_WORDS = _REPO_ROOT / "corpora" / "linear_b" / "words.txt"
_DEFAULT_ETEOCRETAN_WORDS = _REPO_ROOT / "corpora" / "eteocretan" / "words.txt"
_OUT_DIR = _REPO_ROOT / "harness" / "external_phoneme_models"

_BASQUE_ALPHA = 0.1
_ETRUSCAN_ALPHA = 1.0
# mg-4664. Mycenaean-Greek LM is built from the LiBER corpus's
# syllabogram-derived Mycenaean-Greek transliterations. The corpus is
# well-resourced (>5,000 inscriptions, >100 k phoneme tokens), so a low
# smoothing constant matches the Basque side rather than the Etruscan
# side. The brief asked for α=0.1.
_MYCENAEAN_GREEK_ALPHA = 0.1
# mg-6ccd. Eteocretan LM is built from the manually-transcribed
# Praisos / Dreros / minor-attestation corpus (~100 inscriptions, ~87
# unique word forms). Smaller than Etruscan (~700 forms); α=1.0 keeps
# unobserved bigrams bounded away from -inf. The brief explicitly asked
# for α=1.0 (matches the Etruscan setting).
_ETEOCRETAN_ALPHA = 1.0


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


def build_mycenaean_greek(words_path: Path) -> tuple[str, dict]:
    """Build the Mycenaean-Greek char-bigram model from the LiBER
    corpus's per-inscription syllabogram-derived transliterations
    (``corpora/linear_b/words.txt``). One word per line, lowercase
    ASCII, hyphens already stripped (``ku-ne-u`` → ``kuneu``)."""
    words = [
        line.strip()
        for line in words_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    tokens = tokenize_word_list(words)
    model = build_model(
        name="mycenaean_greek",
        tokens=tokens,
        alpha=_MYCENAEAN_GREEK_ALPHA,
        meta_extra={
            "source": (
                "corpora/linear_b/words.txt (LiBER, https://liber.cnr.it; "
                "syllabogram-derived Mycenaean-Greek transliterations from "
                "the per-inscription HTML, hyphens stripped)."
            ),
            "license": (
                "LiBER © CNR / Sapienza Università di Roma; CC BY-NC-SA 4.0 "
                "for academic use. Underlying Linear-B inscriptions are PD "
                "(Bronze Age). The committed model JSON is a statistical "
                "derivative."
            ),
            "n_words": len(words),
            "n_chars": sum(len(w) for w in words),
            "alpha_rationale": (
                "0.1 — well-resourced corpus (≥5,000 inscriptions, ≥100k "
                "phoneme tokens); minimal smoothing keeps rare-bigram "
                "log-probs informative (matches the Basque setting)."
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


def build_eteocretan(words_path: Path) -> tuple[str, dict]:
    """Build the Eteocretan char-bigram model from the manually-
    transcribed Praisos / Dreros / minor-attestation corpus
    (``corpora/eteocretan/words.txt``). One word per line, lowercase
    ASCII, derived from the Greek-alphabet → Latin transliteration
    pipeline in ``scripts/build_eteocretan_corpus.py``."""
    words = [
        line.strip()
        for line in words_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    tokens = tokenize_word_list(words)
    model = build_model(
        name="eteocretan",
        tokens=tokens,
        alpha=_ETEOCRETAN_ALPHA,
        meta_extra={
            "source": (
                "corpora/eteocretan/words.txt (Duhoux 1982, Whittaker "
                "2017, Younger online catalog; manual transcription "
                "via scripts/build_eteocretan_corpus.py)."
            ),
            "license": (
                "Cited fair-use of secondary sources for transcription; "
                "underlying inscriptions PD (~7th-3rd c. BCE)."
            ),
            "n_words": len(words),
            "n_chars": sum(len(w) for w in words),
            "alpha_rationale": (
                "1.0 — small corpus (~87 unique word forms; substantive "
                "textual material concentrated in ~9 multi-line texts). "
                "Stronger smoothing than Basque (0.1) or Mycenaean Greek "
                "(0.1); matches the Etruscan setting (1.0). The "
                "downstream LM is noisier than the larger external "
                "models — this is a documented limitation of the "
                "Eteocretan epigraphic record, not a methodology choice."
            ),
        },
    )
    return model.to_json(), model.meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--only",
        choices=("basque", "etruscan", "mycenaean_greek", "eteocretan"),
        default=None,
        help="Build only one model (default: all).",
    )
    parser.add_argument(
        "--basque-text", type=Path, default=_DEFAULT_BASQUE_TEXT
    )
    parser.add_argument(
        "--etruscan-words", type=Path, default=_DEFAULT_ETRUSCAN_WORDS
    )
    parser.add_argument(
        "--mycenaean-greek-words", type=Path, default=_DEFAULT_MYC_WORDS
    )
    parser.add_argument(
        "--eteocretan-words", type=Path, default=_DEFAULT_ETEOCRETAN_WORDS
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

    if args.only in (None, "mycenaean_greek"):
        if not args.mycenaean_greek_words.exists():
            print(
                f"missing Mycenaean-Greek corpus: {args.mycenaean_greek_words}\n"
                "run scripts/fetch_liber.py + scripts/parse_liber.py first.",
                file=sys.stderr,
            )
            return 2
        text, meta = build_mycenaean_greek(args.mycenaean_greek_words)
        out = args.out_dir / "mycenaean_greek.json"
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}  meta={meta}", file=sys.stderr)

    if args.only in (None, "eteocretan"):
        if not args.eteocretan_words.exists():
            print(
                f"missing Eteocretan corpus: {args.eteocretan_words}\n"
                "run scripts/build_eteocretan_corpus.py first.",
                file=sys.stderr,
            )
            return 2
        text, meta = build_eteocretan(args.eteocretan_words)
        out = args.out_dir / "eteocretan.json"
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}  meta={meta}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
