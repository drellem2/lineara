"""Char-bigram phoneme prior learned from external substrate-language text.

Built once from a text corpus or a list of word forms (see
``scripts/build_external_phoneme_models.py``); consumed at scoring time
by ``external_phoneme_perplexity_v0`` (see ``harness/metrics.py``).

Vocabulary
----------

A fixed 28-token vocabulary:

* ``a..z`` — the 26-letter Latin alphabet (with non-26-letter chars
  folded at corpus build time; see ``corpora/basque.README.md`` and
  ``corpora/etruscan.README.md``).
* ``" "`` — a single space; collapses runs of whitespace in source
  text.
* ``"<W>"`` — a synthetic word-boundary sentinel inserted by the model
  builder at the start and end of each contiguous word, so the model
  learns both word-initial and word-final char distributions.

That makes 28 tokens × 28 = 784 bigram cells (~700 in the brief).

Smoothing
---------

Add-α Laplace smoothing over the closed vocabulary:

    P(b | a) = (count(a, b) + α) / (count(a) + α * |V|)

Two α values are in use:

* ``α = 0.1`` for the Basque model (large corpus; minimal smoothing
  needed).
* ``α = 1.0`` for the Etruscan model (small corpus; stronger smoothing
  to handle rare bigrams).

The model JSON serializes every bigram cell explicitly (sorted), so a
loader does not need to know α to reproduce the log-probabilities at
scoring time.

Determinism
-----------

The model JSON is byte-identical across re-builds: counts use stable
sort order; floats are rounded to 9 decimal places (well above the
precision needed for bigram log-probs); JSON is emitted with
``separators=(",", ":")`` and ``sort_keys=True``.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# Public constants. Bumping any of these is a model_version bump.
WORD_BOUNDARY = "<W>"
SPACE = " "
ALPHABET = tuple("abcdefghijklmnopqrstuvwxyz")
VOCAB: tuple[str, ...] = ALPHABET + (SPACE, WORD_BOUNDARY)
VOCAB_SIZE = len(VOCAB)
# Stable index for serialization. Used by the JSON model: bigram_log_probs
# is a 2D table of shape (VOCAB_SIZE, VOCAB_SIZE) addressed by VOCAB index.
VOCAB_INDEX = {tok: i for i, tok in enumerate(VOCAB)}
# Round serialized log-probs to this many decimal places (~30 bits).
_LOG_PROB_PRECISION = 9


@dataclass(frozen=True)
class ExternalPhonemeModel:
    """Char-bigram prior over a fixed 28-token vocabulary."""

    name: str
    alpha: float
    bigram_counts: list[list[int]]   # shape (VOCAB_SIZE, VOCAB_SIZE)
    unigram_counts: list[int]        # row sums of bigram_counts
    bigram_log_probs: list[list[float]]
    meta: dict

    def log_prob(self, prev: str, cur: str) -> float:
        """log P(cur | prev). Out-of-vocab tokens are treated as ``<W>``
        (the most-frequent boundary sentinel). The metric should never
        feed OOV chars in practice — the candidate phoneme stream has
        already been char-decomposed against the same a-z vocabulary —
        but the fallback keeps the function total."""
        i = VOCAB_INDEX.get(prev, VOCAB_INDEX[WORD_BOUNDARY])
        j = VOCAB_INDEX.get(cur, VOCAB_INDEX[WORD_BOUNDARY])
        return self.bigram_log_probs[i][j]

    def to_json(self) -> str:
        payload = {
            "name": self.name,
            "alpha": self.alpha,
            "vocab": list(VOCAB),
            "vocab_size": VOCAB_SIZE,
            "bigram_counts": self.bigram_counts,
            "unigram_counts": self.unigram_counts,
            "bigram_log_probs": [
                [round(v, _LOG_PROB_PRECISION) for v in row]
                for row in self.bigram_log_probs
            ],
            "meta": self.meta,
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)

    @classmethod
    def load_json(cls, path: Path) -> "ExternalPhonemeModel":
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        # Vocabulary is fixed; if the file disagrees, it's the wrong
        # generation of the model and should be rebuilt.
        if tuple(data["vocab"]) != VOCAB:
            raise ValueError(
                f"vocab mismatch in {path}; got {data['vocab']!r}, expected {VOCAB!r}"
            )
        return cls(
            name=data["name"],
            alpha=float(data["alpha"]),
            bigram_counts=[list(map(int, row)) for row in data["bigram_counts"]],
            unigram_counts=[int(v) for v in data["unigram_counts"]],
            bigram_log_probs=[[float(v) for v in row] for row in data["bigram_log_probs"]],
            meta=dict(data.get("meta", {})),
        )


def tokenize_text(text: str) -> list[str]:
    """Convert a normalized text stream into a token sequence over VOCAB.

    Each whitespace-separated word becomes ``<W> c1 c2 ... cn <W>``.
    The boundary sentinel is also inserted at the very start and very
    end of the stream, so a single-word input still produces both a
    start- and an end- bigram.
    """
    tokens: list[str] = []
    in_word = False
    for ch in text:
        if ch == " " or ch == "\n" or ch == "\t":
            if in_word:
                tokens.append(WORD_BOUNDARY)
                in_word = False
        else:
            if not in_word:
                tokens.append(WORD_BOUNDARY)
                in_word = True
            tokens.append(ch if ch in VOCAB_INDEX else WORD_BOUNDARY)
    if in_word:
        tokens.append(WORD_BOUNDARY)
    return tokens


def tokenize_word_list(words: Iterable[str]) -> list[str]:
    """Convert a list of words (one per line, no whitespace inside) into
    a token sequence over VOCAB. Each word is wrapped in ``<W>``
    sentinels with no inter-word space."""
    tokens: list[str] = []
    for word in words:
        word = word.strip()
        if not word:
            continue
        tokens.append(WORD_BOUNDARY)
        for ch in word:
            tokens.append(ch if ch in VOCAB_INDEX else WORD_BOUNDARY)
        tokens.append(WORD_BOUNDARY)
    return tokens


def build_model(
    *,
    name: str,
    tokens: list[str],
    alpha: float,
    meta_extra: dict | None = None,
) -> ExternalPhonemeModel:
    """Tally bigrams and emit smoothed log-probabilities.

    ``tokens`` is the flat token sequence from ``tokenize_*`` over
    VOCAB. Bigram counts come from adjacent (a, b) pairs in that
    sequence. Unigram counts are the row sums of the bigram table —
    this matches the conditional-probability denominator
    ``count(a) + α * |V|`` (i.e. ``count(a) = sum_b count(a, b)``;
    bigrams ending the stream are not counted as a separate "saw a"
    observation, which is correct for next-token prediction).
    """
    bigram_counts = [[0] * VOCAB_SIZE for _ in range(VOCAB_SIZE)]
    for prev, cur in zip(tokens[:-1], tokens[1:]):
        i = VOCAB_INDEX.get(prev, VOCAB_INDEX[WORD_BOUNDARY])
        j = VOCAB_INDEX.get(cur, VOCAB_INDEX[WORD_BOUNDARY])
        bigram_counts[i][j] += 1
    unigram_counts = [sum(row) for row in bigram_counts]

    log_probs = [[0.0] * VOCAB_SIZE for _ in range(VOCAB_SIZE)]
    for i in range(VOCAB_SIZE):
        denom = unigram_counts[i] + alpha * VOCAB_SIZE
        for j in range(VOCAB_SIZE):
            num = bigram_counts[i][j] + alpha
            log_probs[i][j] = math.log(num / denom)

    meta = {
        "n_tokens": len(tokens),
        "n_bigrams_observed": sum(unigram_counts),
        "vocab_size": VOCAB_SIZE,
    }
    if meta_extra:
        meta.update(meta_extra)
    return ExternalPhonemeModel(
        name=name,
        alpha=alpha,
        bigram_counts=bigram_counts,
        unigram_counts=unigram_counts,
        bigram_log_probs=log_probs,
        meta=meta,
    )


def char_decompose_phonemes(phonemes: list[str]) -> list[str]:
    """Flatten a phoneme sequence into single-char tokens.

    Multi-char phonemes (``th``, ``ph``, ``ch``, ``ts``, ``tx``, ``tz``)
    are split into their constituent chars. Chars outside the 28-token
    VOCAB are folded to ``<W>`` (the OOV fallback). This keeps the
    char-bigram model aligned with the standard Latin transliteration
    conventions used both here and in the substrate pool YAMLs."""
    out: list[str] = []
    for phoneme in phonemes:
        for ch in phoneme:
            out.append(ch if ch in VOCAB_INDEX else WORD_BOUNDARY)
    return out
