"""Scoring metrics.

v0 ships two:

* ``compression_delta_v0`` — corpus-global zlib-compression delta over a
  partial sign→phoneme mapping (the original v0 metric).
* ``local_fit_v0`` — local-fit metric for ``candidate_equation.v1``
  hypotheses; see the ``local_fit_v0`` docstring for the formula and what it
  does/does-not measure.
"""

from __future__ import annotations

import math
import random
import zlib
from dataclasses import dataclass

from .corpus import apply_mapping, sign_position_fingerprints


# ---------------------------------------------------------------------------
# compression_delta_v0
# ---------------------------------------------------------------------------

# Frozen for v0. Changing any of these is a harness_version bump.
_ZLIB_LEVEL = 9
_ZLIB_WBITS = 15  # default deflate window; explicit so we don't drift
_SYMBOL_BYTES = 2  # big-endian 16-bit token IDs
_MAX_UNIQUE = 1 << (8 * _SYMBOL_BYTES)


@dataclass(frozen=True)
class CompressionResult:
    score: float
    bits_per_sign_baseline: float
    bits_per_sign_mapped: float
    baseline_bits: int
    mapped_bits: int
    stream_length: int


def _encode_to_bytes(stream: list[str]) -> bytes:
    """Map each unique token to a fixed 16-bit ID (sorted-lex order) and emit
    big-endian. Distinct token, distinct symbol; identical per-token cost across
    streams so zlib measures structural redundancy, not name-length."""
    unique = sorted(set(stream))
    if len(unique) > _MAX_UNIQUE:
        raise ValueError(
            f"compression_delta_v0 supports up to {_MAX_UNIQUE} unique tokens; "
            f"stream has {len(unique)}"
        )
    sym = {tok: i for i, tok in enumerate(unique)}
    buf = bytearray(len(stream) * _SYMBOL_BYTES)
    for i, tok in enumerate(stream):
        v = sym[tok]
        buf[i * 2] = (v >> 8) & 0xFF
        buf[i * 2 + 1] = v & 0xFF
    return bytes(buf)


def _zlib_bits(payload: bytes) -> int:
    compressor = zlib.compressobj(_ZLIB_LEVEL, zlib.DEFLATED, _ZLIB_WBITS)
    out = compressor.compress(payload) + compressor.flush(zlib.Z_FINISH)
    return len(out) * 8


def compression_delta_v0(stream: list[str], mapping: dict[str, str]) -> CompressionResult:
    """Score `mapping` against `stream` via zlib compression delta.

    Pipeline (frozen for harness v0):
      1. Encode the raw stream with a 2-byte symbol-id coder + zlib L9.
      2. Apply `mapping` to the stream; encode the mapped stream the same way.
      3. score = baseline_bits - mapped_bits.
    """
    if not stream:
        raise ValueError("compression_delta_v0 requires a non-empty stream")

    baseline_payload = _encode_to_bytes(stream)
    mapped_stream = apply_mapping(stream, mapping)
    mapped_payload = _encode_to_bytes(mapped_stream)

    baseline_bits = _zlib_bits(baseline_payload)
    mapped_bits = _zlib_bits(mapped_payload)

    n = len(stream)
    return CompressionResult(
        score=float(baseline_bits - mapped_bits),
        bits_per_sign_baseline=baseline_bits / n,
        bits_per_sign_mapped=mapped_bits / n,
        baseline_bits=baseline_bits,
        mapped_bits=mapped_bits,
        stream_length=n,
    )


# ---------------------------------------------------------------------------
# local_fit_v0
# ---------------------------------------------------------------------------
#
# Phoneme-class system used by both the position-fit and class-bigram terms.
# Three classes:
#   V — vowels (a, e, i, o, u). Word-final-friendly in Basque and most
#       Mediterranean substrate candidates.
#   S — sonorants (l, r, n, m, ñ). Flexible position; common medially.
#   C — everything else (stops, fricatives, affricates). Initial/medial-friendly,
#       rarely word-final in Basque/Aquitanian.
#
# Multi-character phonemes (e.g. "ts", "kh", "th") are classified by the FIRST
# character; this is a heuristic that works for the substrate roots in scope at
# v0 (Aquitanian, Pre-Greek toponym). Document and revisit when the metric is
# extended.
_VOWELS = frozenset("aeiouAEIOU")
_SONORANTS = frozenset("lrnmñLRNMÑ")


def _class_of(phoneme: str) -> str:
    if not phoneme:
        return "C"
    head = phoneme[0]
    if head in _VOWELS:
        return "V"
    if head in _SONORANTS:
        return "S"
    return "C"


# Hardcoded substrate phonotactic priors for v0. Numbers were chosen from the
# qualitative descriptions in Trask (1997, _The History of Basque_) chapter 3
# on Basque phonotactics: CV-preference, vowel-finality, sonorant flexibility.
# They are *priors*, not measurements — published frequency tables are a v0+
# follow-up. Two distributions are needed:
#
# 1. ``_PHON_POSITION`` — expected position-class distribution
#    [initial, medial, final, standalone] for a phoneme of each class. Used by
#    the *position-fit term*: how well does the corpus-wide position fingerprint
#    of each sign match the position profile of its proposed phoneme?
#
# 2. ``_PHON_CLASS_TRANSITIONS`` — class bigram probabilities. Used by the
#    *bigram-LM term*: how plausible is the proposed phoneme sequence under
#    Basque-style CV phonotactics?
#
# Smoothing: every probability is bounded below by ``_FLOOR`` so log-prob never
# returns -inf even when the corpus is small.
_FLOOR = 1e-3

_PHON_POSITION: dict[str, list[float]] = {
    # initial, medial, final, standalone
    "V": [0.10, 0.30, 0.55, 0.05],
    "S": [0.20, 0.55, 0.20, 0.05],
    "C": [0.40, 0.55, 0.02, 0.03],
}

# Per-phoneme overrides — finer-grained position profiles for common
# Basque/Aquitanian/Pre-Greek letters. Numbers are working priors derived
# from Trask 1997 ch. 3 phonotactics and Hualde & de Urbina 2003 prosody.
# The point of the overrides is to break intra-class degeneracies: with
# class-only profiles, /a/ and /i/ behave identically under the metric, so
# permuting /a-i/ to /i-a/ gives an unchanged score (z=0). Letter-specific
# profiles distinguish the two and produce meaningful permutation-z values.
_PHON_POSITION_OVERRIDES: dict[str, list[float]] = {
    # vowels
    "a": [0.10, 0.30, 0.55, 0.05],
    "e": [0.10, 0.40, 0.45, 0.05],
    "i": [0.20, 0.45, 0.30, 0.05],   # less final than other vowels
    "o": [0.05, 0.25, 0.65, 0.05],   # most final-friendly
    "u": [0.10, 0.30, 0.55, 0.05],
    # sonorants
    "l": [0.10, 0.55, 0.30, 0.05],
    "r": [0.05, 0.65, 0.25, 0.05],   # rare word-initial in Basque
    "n": [0.20, 0.45, 0.30, 0.05],
    "m": [0.25, 0.55, 0.15, 0.05],
    # stops
    "b": [0.45, 0.50, 0.02, 0.03],
    "d": [0.30, 0.65, 0.02, 0.03],
    "g": [0.35, 0.60, 0.02, 0.03],
    "k": [0.40, 0.55, 0.02, 0.03],
    "p": [0.35, 0.60, 0.02, 0.03],
    "t": [0.30, 0.65, 0.02, 0.03],
    # fricatives / sibilants / glides
    "s": [0.30, 0.50, 0.15, 0.05],
    "z": [0.30, 0.50, 0.15, 0.05],
    "x": [0.25, 0.55, 0.15, 0.05],
    "h": [0.50, 0.40, 0.05, 0.05],
    "j": [0.40, 0.50, 0.05, 0.05],
    "w": [0.45, 0.50, 0.02, 0.03],
}

_PHON_CLASS_TRANSITIONS: dict[tuple[str, str], float] = {
    # from-state '#': start of root
    ("#", "V"): 0.30,
    ("#", "S"): 0.15,
    ("#", "C"): 0.55,
    # from V: vowel-final-friendly, but next syllable usually starts with C
    ("V", "V"): 0.05,
    ("V", "S"): 0.40,
    ("V", "C"): 0.55,
    # from S: typically followed by V (sonorant-vowel onset)
    ("S", "V"): 0.50,
    ("S", "S"): 0.10,
    ("S", "C"): 0.40,
    # from C: strong C->V preference (CV is the canonical Basque syllable)
    ("C", "V"): 0.85,
    ("C", "S"): 0.10,
    ("C", "C"): 0.05,
}

# Number of random phoneme permutations used to build the control distribution.
# Frozen for v0; reproducibility hinges on it together with _CONTROL_SEED.
_CONTROL_PERMUTATIONS = 200
_CONTROL_SEED = 42


@dataclass(frozen=True)
class LocalFitResult:
    """Result of ``local_fit_v0`` on a single candidate-equation hypothesis."""

    score: float
    score_control_z: float
    metric_notes: str
    # Diagnostic breakdown (not persisted to the result row):
    position_term: float
    bigram_term: float
    control_mean: float
    control_std: float
    n_pairs_scored: int


def _expected_position_for_phoneme(phoneme: str) -> list[float]:
    """Per-phoneme override → class default → uniform fallback."""
    if not phoneme:
        return _PHON_POSITION["C"]
    head = phoneme[0]
    if head in _PHON_POSITION_OVERRIDES:
        return _PHON_POSITION_OVERRIDES[head]
    return _PHON_POSITION[_class_of(phoneme)]


def _normalize(counts: list[int]) -> list[float]:
    total = sum(counts)
    if total <= 0:
        # Sign never observed in any word — fall back to uniform.
        return [0.25, 0.25, 0.25, 0.25]
    return [c / total for c in counts]


def _bhattacharyya_coefficient(p: list[float], q: list[float]) -> float:
    """BC = sum sqrt(p_i * q_i). 1.0 = identical; 0.0 = disjoint."""
    return sum(math.sqrt(max(0.0, a) * max(0.0, b)) for a, b in zip(p, q))


def _position_fit(
    sign: str, phoneme: str, fingerprints: dict[str, list[int]]
) -> float:
    """Per-(sign, phoneme) position-fit term.

    Returns ``log(BC + floor)`` where BC is the Bhattacharyya coefficient
    between the sign's empirical position distribution and the proposed
    phoneme's expected position distribution. Bounded above by 0
    (BC <= 1 ⇒ log <= 0); higher = better fit.
    """
    actual = _normalize(fingerprints.get(sign, [0, 0, 0, 0]))
    expected = _expected_position_for_phoneme(phoneme)
    bc = _bhattacharyya_coefficient(actual, expected)
    return math.log(bc + _FLOOR)


def _class_bigram_logprob(phonemes: list[str]) -> float:
    """Log-likelihood of the phoneme sequence under the hardcoded class LM."""
    if not phonemes:
        return 0.0
    classes = ["#"] + [_class_of(p) for p in phonemes]
    total = 0.0
    for prev, cur in zip(classes[:-1], classes[1:]):
        prob = _PHON_CLASS_TRANSITIONS.get((prev, cur), _FLOOR)
        total += math.log(max(prob, _FLOOR))
    return total


def _score_alignment(
    signs: list[str], phonemes: list[str], fingerprints: dict[str, list[int]]
) -> tuple[float, float, float]:
    """Score one (signs, phonemes) alignment. Returns (total, position, bigram)."""
    position = sum(
        _position_fit(s, p, fingerprints) for s, p in zip(signs, phonemes)
    )
    bigram = _class_bigram_logprob(phonemes)
    return position + bigram, position, bigram


def local_fit_v0(
    stream: list[str],
    signs: list[str],
    phonemes: list[str],
) -> LocalFitResult:
    """Score a candidate-equation alignment locally.

    **What it measures.** A candidate-equation hypothesis pins one inscription
    span to a substrate root. ``local_fit_v0`` asks two questions about that
    pinning, and combines the answers:

    * *Position fit.* For each (sign, phoneme) pair, how close is the sign's
      corpus-wide position-in-word distribution to the position profile we
      *expect* of a phoneme of that class (V/S/C)?
      Term: ``log(Bhattacharyya(actual, expected) + floor)``, summed over the
      pairs in the equation. Range: roughly [-7, 0] per pair (0 = perfect).
    * *Phoneme-class bigram plausibility.* How likely is the proposed phoneme
      sequence under a hardcoded Basque-style CV phonotactic transition model
      over phoneme classes (V/S/C)? Term: ``sum log P(class_i | class_{i-1})``.

    The total score is ``position_term + bigram_term``.

    **Control z.** ``score_control_z = (score - mean(controls)) / std(controls)``
    where the control distribution comes from ``_CONTROL_PERMUTATIONS`` random
    phoneme-only permutations of the same alignment, seeded from
    ``_CONTROL_SEED``. The signs (and hence position fingerprints) stay put;
    only the phoneme labels move. This isolates the *order-of-phonemes* signal
    from the (per-sign-rarity, per-corpus-snapshot) baseline.

    **What it does NOT measure.** It is *not* a translation likelihood — the
    expected-position profiles are hardcoded substrate priors, not learned
    distributions, and the class system collapses ``a/e/i/o/u`` together (and
    likewise all stops). Two equations that propose different vowels at the
    same position cannot be distinguished by this metric. Use it to *triage*
    candidate equations against random and phonotactically-implausible
    controls; do not over-read absolute score values.

    **Known v0 limitations.** With ``k=2`` phonemes the control distribution
    has only 2 unique permutations, so ``score_control_z`` collapses to one
    of {+~1.14, 0, -~1.14} depending on whether the original ordering was
    the better of the two, identical (degenerate), or worse. Use 3+ phonemes
    when finer-grained z is needed. The class system also collapses
    {a, e, i, o, u} into a single V profile by default; per-letter overrides
    in ``_PHON_POSITION_OVERRIDES`` partially break this for common
    Basque/Aquitanian letters but not for all phoneme inventories.

    **What would invalidate it.** (a) The Linear-A signs in scope being a
    non-syllabary system (e.g. logographic) — the position fingerprint would
    mean nothing in that case. (b) Substrate phonotactics genuinely at odds
    with the hardcoded class transitions — the class LM would mis-rank
    real-substrate hypotheses. (c) A mostly-fragmentary corpus — sign position
    fingerprints get noisy and the position term collapses toward the floor.

    **Determinism.** Same ``stream`` + ``signs`` + ``phonemes`` always produce
    the same numeric result; the control permutation rng is seeded with
    ``_CONTROL_SEED`` and consumed in a fixed order.
    """
    if not signs:
        raise ValueError("local_fit_v0: equation has no signs")
    if len(signs) != len(phonemes):
        raise ValueError(
            f"local_fit_v0: |signs|={len(signs)} != |phonemes|={len(phonemes)}"
        )

    fingerprints = sign_position_fingerprints(stream)

    score, pos_term, bi_term = _score_alignment(signs, phonemes, fingerprints)

    # Build control distribution. Seed and permutation count are fixed.
    rng = random.Random(_CONTROL_SEED)
    control_scores: list[float] = []
    for _ in range(_CONTROL_PERMUTATIONS):
        permuted = list(phonemes)
        rng.shuffle(permuted)
        ctrl_total, _, _ = _score_alignment(signs, permuted, fingerprints)
        control_scores.append(ctrl_total)

    mean = sum(control_scores) / len(control_scores)
    var = sum((s - mean) ** 2 for s in control_scores) / len(control_scores)
    std = math.sqrt(var)
    if std < 1e-12:
        # All permutations gave the same score (e.g. equation has only one
        # phoneme, or all phonemes share the same class). Z is undefined; we
        # report 0.0 and document this in metric_notes.
        z = 0.0
        z_note = (
            f"control std=0 over {_CONTROL_PERMUTATIONS} permutations "
            f"(z forced to 0; equation likely has fewer than two distinct phoneme classes)"
        )
    else:
        z = (score - mean) / std
        z_note = (
            f"z=(score - mean)/std over {_CONTROL_PERMUTATIONS} permutations, "
            f"seed={_CONTROL_SEED}"
        )

    notes = (
        f"local_fit_v0: position_term={pos_term:.4f}, bigram_term={bi_term:.4f}, "
        f"control_mean={mean:.4f}, control_std={std:.4f}; {z_note}"
    )
    return LocalFitResult(
        score=float(score),
        score_control_z=float(z),
        metric_notes=notes,
        position_term=float(pos_term),
        bigram_term=float(bi_term),
        control_mean=float(mean),
        control_std=float(std),
        n_pairs_scored=len(signs),
    )


METRICS = {
    "compression_delta_v0": compression_delta_v0,
    "local_fit_v0": local_fit_v0,
}
