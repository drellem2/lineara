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


# ---------------------------------------------------------------------------
# local_fit_v1
# ---------------------------------------------------------------------------
#
# v1 design (mg-7dd1) addresses the discrimination problem documented in
# mg-f832: under v0 the per-hypothesis 200-permutation z-normalization
# collapsed cross-hypothesis variance, and 74.4% of bulk Aquitanian
# candidates landed at z > 1. v1 drops the per-hypothesis z entirely and
# returns a directly-comparable absolute score, builds the bigram prior
# empirically from the active pool's surfaces (so it adapts to whichever
# substrate is being tested), normalizes by length so 2-sign equations do
# not dominate, and penalizes equations whose signs are very rare in the
# corpus.
#
# Formula (constants documented in source — can be tuned without breaking
# the schema):
#
#   local_fit_v1(eq) =
#       + A * mean_position_compat(eq)
#       + B * mean_empirical_bigram_logprob(eq, pool)
#       - C * length_penalty(eq)
#       - D * rare_sign_correction(eq, corpus)
#
# where each term is in roughly comparable per-sign units:
#   * mean_position_compat  ∈ [-7, 0]  (0 = perfect position fit at every sign)
#   * mean_empirical_bigram ∈ [-7, 0]  (0 = bigrams are exactly as common as max-prob bigram)
#   * length_penalty(eq)    = 1/n      so 2-sign eqs lose 0.5 * C, 4-sign eqs lose 0.25 * C
#   * rare_sign_correction  = (# signs with corpus count < RARE_SIGN_THRESHOLD) / n
#
# All four terms are byte-deterministic given (corpus stream, pool, signs,
# phonemes). No randomness, no permutation control — the design target is
# *cross-hypothesis* discrimination, so a per-hypothesis control is not the
# right tool.

# Constants frozen for v1. Bumping any of them is a metric_version bump.
_LF1_A_POSITION = 1.0
_LF1_B_BIGRAM = 1.0
_LF1_C_LENGTH_PENALTY = 1.0
_LF1_D_RARE_SIGN = 0.5
_LF1_RARE_SIGN_THRESHOLD = 5
_LF1_BIGRAM_ALPHA = 1.0  # Laplace smoothing constant for the empirical bigram LM.
_LF1_START = "<S>"  # word-start sentinel for the empirical bigram LM
_LF1_END = "<E>"    # word-end sentinel


@dataclass(frozen=True)
class EmpiricalBigramModel:
    """Empirical phoneme-pair distribution learned from a pool's surfaces.

    Built once from a list-of-phoneme-sequences (the pool entries' phoneme
    lists). Add-`alpha` Laplace smoothing over the closed-vocabulary the
    sequences span (plus the start/end sentinels). The smoothing keeps log
    P bounded for unseen bigrams without the metric having to special-case
    them. ``log_prob(prev, cur)`` is a pure function of the model + inputs.
    """

    bigram_counts: dict[tuple[str, str], int]
    unigram_counts: dict[str, int]
    vocab: tuple[str, ...]  # tuple for stable hashing/printing
    alpha: float

    @classmethod
    def from_sequences(
        cls, sequences: list[list[str]], alpha: float = _LF1_BIGRAM_ALPHA
    ) -> "EmpiricalBigramModel":
        bigram: dict[tuple[str, str], int] = {}
        unigram: dict[str, int] = {}
        vocab_set: set[str] = {_LF1_START, _LF1_END}
        for seq in sequences:
            tokens = [_LF1_START, *seq, _LF1_END]
            for tok in tokens:
                vocab_set.add(tok)
                unigram[tok] = unigram.get(tok, 0) + 1
            for prev, cur in zip(tokens[:-1], tokens[1:]):
                bigram[(prev, cur)] = bigram.get((prev, cur), 0) + 1
        # Sorted vocab for deterministic representation.
        vocab = tuple(sorted(vocab_set))
        return cls(
            bigram_counts=dict(bigram),
            unigram_counts=dict(unigram),
            vocab=vocab,
            alpha=alpha,
        )

    def log_prob(self, prev: str, cur: str) -> float:
        """log P(cur | prev) under add-`alpha` Laplace smoothing."""
        v = len(self.vocab)
        num = self.bigram_counts.get((prev, cur), 0) + self.alpha
        den = self.unigram_counts.get(prev, 0) + self.alpha * v
        # den > 0 always (alpha > 0, v > 0); num > 0 always.
        return math.log(num / den)


@dataclass(frozen=True)
class LocalFitV1Result:
    """Result of ``local_fit_v1`` on one candidate-equation hypothesis.

    ``bigram_term`` is ``None`` when the caller passed ``bigram_model=None``
    (e.g. anchor / scramble / cross-pool curated hypotheses for which no
    matching pool yaml exists). In that case the bigram contribution is
    excluded from ``score`` and the position term is rescaled to occupy
    its weight (see ``local_fit_v1`` for the exact formula). This keeps
    pool-matched and pool-unmatched scores on a comparable scale.
    """

    score: float
    metric_notes: str
    # Diagnostic breakdown (persisted for analysis, not used in the sort key):
    position_term: float
    bigram_term: float | None
    length_penalty: float
    rare_sign_correction: float
    n_pairs_scored: int


def _sign_corpus_counts(stream: list[str]) -> dict[str, int]:
    """Count how many times each token appears anywhere in the corpus stream.

    Used by the rare-sign correction term. Boundary markers are not counted
    (they are not signs)."""
    counts: dict[str, int] = {}
    for tok in stream:
        if tok == "INS_BOUNDARY" or tok == "DIV":
            continue
        counts[tok] = counts.get(tok, 0) + 1
    return counts


def _mean_position_compat(
    signs: list[str], phonemes: list[str], fingerprints: dict[str, list[int]]
) -> float:
    """Mean over (sign, phoneme) pairs of log(Bhattacharyya + floor)."""
    total = sum(
        _position_fit(s, p, fingerprints) for s, p in zip(signs, phonemes)
    )
    return total / max(len(signs), 1)


def _mean_empirical_bigram_logprob(
    phonemes: list[str], model: EmpiricalBigramModel
) -> float:
    """Mean over (n+1) bigrams of log P under the empirical pool LM.

    Bigrams include the (<S>, p_0) start transition and the (p_{n-1}, <E>)
    end transition, so a single-phoneme equation gets 2 bigrams scored. This
    keeps the term well-defined at every length.
    """
    if not phonemes:
        return 0.0
    seq = [_LF1_START, *phonemes, _LF1_END]
    bigrams = list(zip(seq[:-1], seq[1:]))
    total = sum(model.log_prob(a, b) for a, b in bigrams)
    return total / len(bigrams)


def _length_penalty(n: int) -> float:
    """1/n. Short equations pay more. Returns 0 for n=0 (degenerate)."""
    if n <= 0:
        return 0.0
    return 1.0 / n


def _rare_sign_correction(
    signs: list[str], sign_counts: dict[str, int], threshold: int
) -> float:
    """Fraction of the equation's signs that occur fewer than `threshold`
    times anywhere in the corpus stream. Range [0, 1]."""
    if not signs:
        return 0.0
    rare = sum(1 for s in signs if sign_counts.get(s, 0) < threshold)
    return rare / len(signs)


def local_fit_v1(
    stream: list[str],
    signs: list[str],
    phonemes: list[str],
    bigram_model: EmpiricalBigramModel | None,
    *,
    sign_counts: dict[str, int] | None = None,
    fingerprints: dict[str, list[int]] | None = None,
) -> LocalFitV1Result:
    """Score a candidate-equation alignment with the v1 local-fit metric.

    **What it measures.** Same intent as v0 (does this span = this root)
    but with cross-hypothesis-comparable absolute units, an
    empirically-learned bigram prior over the active pool, a length
    penalty, and a rare-sign correction. See the module-level comment block
    above for the formula and constants.

    **Pool-specific bigram dispatch (mg-c2af).** ``bigram_model`` must be
    the bigram model built from the hypothesis's own ``source_pool`` (so
    Aquitanian candidates score against the Aquitanian pool's bigram
    statistics, Etruscan against Etruscan, toponym against toponym).
    Routing a non-pool candidate (anchor / scramble / cross-pool curated
    fragment) through *another* pool's bigram model produces uninterpretable
    rare-sign-style penalties: the candidate's phonemes simply don't
    appear in that pool's vocabulary, so every bigram hits the smoothing
    floor and the term becomes a fixed cross-hypothesis penalty rather
    than a discriminator. mg-7c8c documented the resulting confound: anchor
    (real) candidates scored *lower* than random IPA scrambles because the
    runner had been falling back to the Aquitanian bigram for both.

    The fix: when the runner cannot match the hypothesis's source_pool to
    a pool YAML, it passes ``bigram_model=None`` here. The bigram term
    is then excluded from the metric sum and reported as ``None`` in the
    result row's ``bigram_term`` field. The position term is rescaled to
    weight ``A + B`` (rather than just ``A``) so the absolute score
    remains on the same scale as pool-matched scores: each additive term
    is per-sign in roughly [-7, 0], and skipping one term without
    rescaling would shift unmatched scores upward by ~|B*bigram| relative
    to matched scores.

    **Why no control z.** v0 used per-hypothesis permutation z to isolate
    order-of-phonemes from sign-rarity, but the price was that ranks of
    different hypotheses were no longer directly comparable: every
    hypothesis was standardized by its own permutation distribution. v1's
    target is a leaderboard that *is* directly comparable across
    hypotheses, so we keep the absolute score. (The v0 metric is still
    available unchanged for callers that want the contrastive view.)

    **Why empirical bigrams.** v0's class-bigram LM was hardcoded to a
    Basque-style CV phonotactic prior. That works for an Aquitanian pool
    but is a poor fit for, e.g., a Pre-Greek toponym pool with consonant
    clusters. The empirical model is built from the active pool's
    own surface forms, so it adapts automatically.

    **Why length-normalize and rare-sign-correct.** Both were diagnosed in
    mg-f832: the v0 leaderboard's top is dominated by 2-sign equations
    (cumulative log-prob is less negative when fewer terms are summed),
    and several top entries pin to signs that occur < 5 times in the
    corpus (so the position fingerprint is dominated by 1-2 observations
    and the metric is over-confident). v1 attenuates both effects.

    **Determinism.** Identical inputs ⇒ byte-identical score. The empirical
    bigram model is built deterministically from the pool sequences (in
    insertion order); `_sign_corpus_counts` is order-independent. The
    null-bigram code path is also fully deterministic — it simply skips
    one term and rescales the rest.

    **What invalidates it.**
      * (a) Pool is too small (< ~20 entries) ⇒ empirical bigram is
        dominated by smoothing rather than data.
      * (b) Pool has no overlap with the target script's phoneme inventory
        ⇒ all bigrams hit the smoothing floor and the bigram term goes
        flat across hypotheses.
      * (c) Corpus is fragmentary ⇒ position fingerprints are noisy and
        the position term degenerates toward the floor (same caveat as v0).
    """
    if not signs:
        raise ValueError("local_fit_v1: equation has no signs")
    if len(signs) != len(phonemes):
        raise ValueError(
            f"local_fit_v1: |signs|={len(signs)} != |phonemes|={len(phonemes)}"
        )

    if fingerprints is None:
        fingerprints = sign_position_fingerprints(stream)
    if sign_counts is None:
        sign_counts = _sign_corpus_counts(stream)

    pos_mean = _mean_position_compat(signs, phonemes, fingerprints)
    lp = _length_penalty(len(phonemes))
    rsc = _rare_sign_correction(signs, sign_counts, _LF1_RARE_SIGN_THRESHOLD)

    if bigram_model is None:
        # No matching pool. Skip the bigram term entirely and rescale the
        # position weight so the additive sum stays on the same scale
        # (A + B) * pos rather than A * pos + B * 0. Document via notes.
        bi_mean: float | None = None
        score = (
            (_LF1_A_POSITION + _LF1_B_BIGRAM) * pos_mean
            - _LF1_C_LENGTH_PENALTY * lp
            - _LF1_D_RARE_SIGN * rsc
        )
        notes = (
            f"local_fit_v1: pos={pos_mean:.4f}, bigram=null (no pool match), "
            f"length_penalty={lp:.4f}, rare_sign={rsc:.4f}; "
            f"A_eff={_LF1_A_POSITION + _LF1_B_BIGRAM} (A+B; bigram excluded), "
            f"C={_LF1_C_LENGTH_PENALTY}, D={_LF1_D_RARE_SIGN}, "
            f"rare_threshold={_LF1_RARE_SIGN_THRESHOLD}"
        )
    else:
        bi_mean = _mean_empirical_bigram_logprob(phonemes, bigram_model)
        score = (
            _LF1_A_POSITION * pos_mean
            + _LF1_B_BIGRAM * bi_mean
            - _LF1_C_LENGTH_PENALTY * lp
            - _LF1_D_RARE_SIGN * rsc
        )
        notes = (
            f"local_fit_v1: pos={pos_mean:.4f}, bigram={bi_mean:.4f}, "
            f"length_penalty={lp:.4f}, rare_sign={rsc:.4f}; "
            f"A={_LF1_A_POSITION}, B={_LF1_B_BIGRAM}, "
            f"C={_LF1_C_LENGTH_PENALTY}, D={_LF1_D_RARE_SIGN}, "
            f"rare_threshold={_LF1_RARE_SIGN_THRESHOLD}, "
            f"alpha={_LF1_BIGRAM_ALPHA}, vocab={len(bigram_model.vocab)}"
        )
    return LocalFitV1Result(
        score=float(score),
        metric_notes=notes,
        position_term=float(pos_mean),
        bigram_term=(float(bi_mean) if bi_mean is not None else None),
        length_penalty=float(lp),
        rare_sign_correction=float(rsc),
        n_pairs_scored=len(signs),
    )


# ---------------------------------------------------------------------------
# geographic_genre_fit_v1
# ---------------------------------------------------------------------------
#
# Categorical compatibility between the pool entry's (region, semantic_field)
# and the inscription's (site, genre_hint). A second, structurally
# orthogonal score column on each result row — used as a cheap-test
# multiplier alongside local_fit_v1.
#
# Score:
#   geographic_genre_fit_v1(eq) = α * region_compat + (1 - α) * semantic_compat
# where α ∈ [0, 1], default 0.4 (semantic carries more weight per the brief
# "subject matter of the tablets it fits").
#
# The lookup tables are deliberately small and opinionated. Each entry is a
# standalone declarative statement with a brief rationale. See the brief for
# the v1 mandate: "a small, opinionated, sourced table is more useful than a
# vast unsourced one."

_GG1_DEFAULT_ALPHA = 0.4
_GG1_NEUTRAL = 0.5  # used for missing/unclassified fields and unmapped pairs


# Region × site compatibility. Sites are SigLA's site labels; regions are
# the pool entry's `region` field. Higher = better fit.
#
# Rationale (per brief):
#   * Aquitanian → Cretan / Aegean Linear-A sites: substrate-hypothesis
#     allows ancient Mediterranean cognates → 0.25 (small but positive).
#   * Pre-Greek toponym → Crete: 1.0 (toponyms are exactly the data class).
#   * Etruscan → Crete: 0.5 (Mediterranean substrate ties; not as direct).
#   * Linear-B carryover → Knossos: 1.0 (Knossos is *the* Linear-B site).
#   * Linear-B carryover → other Linear-A sites: 0.5 (carryover values
#     transfer broadly, but Knossos is privileged).
#   * Random scramble → anything: 0.5 (no claim).
#
# Sources:
#   - Beekes, _Etymological Dictionary of Greek_ (2010), pre-Greek substrate
#     in Aegean toponyms.
#   - Trask 1997 ch. 2 on the Vasconic / Pre-IE substrate hypothesis.
#   - Schoep 2002, Linear-A administrative geography (which sites kept
#     Linear-A vs Linear-B records during the Neopalatial transition).
_GG1_REGION_COMPAT: dict[tuple[str, str], float] = {
    # Aquitanian / Vasconic substrate against Aegean Linear-A sites.
    ("aquitania", "Haghia Triada"): 0.25,
    ("aquitania", "Khania"): 0.25,
    ("aquitania", "Phaistos"): 0.25,
    ("aquitania", "Zakros"): 0.25,
    ("aquitania", "Knossos"): 0.25,
    ("aquitania", "Mallia"): 0.25,
    ("aquitania", "Arkhanes"): 0.25,
    ("aquitania", "Kea"): 0.25,
    ("aquitania", "Tylissos"): 0.25,
    ("aquitania", "Gournia"): 0.25,
    ("aquitania", "Pyrgos"): 0.25,
    ("aquitania", "Haghios Stephanos"): 0.25,
    ("aquitania", "Kythera"): 0.25,
    ("aquitania", "Melos"): 0.25,
    ("aquitania", "Mycenae"): 0.25,
    ("aquitania", "Papoura"): 0.25,
    ("aquitania", "Psykhro"): 0.25,
    ("aquitania", "Syme"): 0.25,
    # Same but for the basque_substrate region tag (kept symmetric with
    # aquitania — both refer to the same substrate hypothesis under the
    # current pool taxonomy).
    ("basque_substrate", "Haghia Triada"): 0.25,
    ("basque_substrate", "Khania"): 0.25,
    ("basque_substrate", "Phaistos"): 0.25,
    ("basque_substrate", "Zakros"): 0.25,
    ("basque_substrate", "Knossos"): 0.25,
    ("basque_substrate", "Mallia"): 0.25,
    ("basque_substrate", "Arkhanes"): 0.25,
    ("basque_substrate", "Kea"): 0.25,
    ("basque_substrate", "Tylissos"): 0.25,
    ("basque_substrate", "Gournia"): 0.25,
    ("basque_substrate", "Pyrgos"): 0.25,
    ("basque_substrate", "Haghios Stephanos"): 0.25,
    ("basque_substrate", "Kythera"): 0.25,
    ("basque_substrate", "Melos"): 0.25,
    ("basque_substrate", "Mycenae"): 0.25,
    ("basque_substrate", "Papoura"): 0.25,
    ("basque_substrate", "Psykhro"): 0.25,
    ("basque_substrate", "Syme"): 0.25,
    # Pre-Greek toponym → Crete is the strongest case. mg-c2af expands
    # this row to every Cretan site that appears in the SigLA corpus
    # so toponym candidates landing on minor sites (Tylissos, Gournia,
    # Pyrgos, Haghios Stephanos, Psykhro, Papoura, Syme) hit the
    # by_surface lookup at full weight (1.0) rather than the unmapped
    # neutral 0.5. The Cycladic / mainland sites stay at 0.75 / 0.5.
    ("pre_greek", "Haghia Triada"): 1.0,
    ("pre_greek", "Khania"): 1.0,
    ("pre_greek", "Phaistos"): 1.0,
    ("pre_greek", "Zakros"): 1.0,
    ("pre_greek", "Knossos"): 1.0,
    ("pre_greek", "Mallia"): 1.0,
    ("pre_greek", "Arkhanes"): 1.0,
    ("pre_greek", "Tylissos"): 1.0,  # mg-c2af: Cretan minor palace
    ("pre_greek", "Gournia"): 1.0,   # mg-c2af: Cretan town
    ("pre_greek", "Pyrgos"): 1.0,    # mg-c2af: Cretan villa site
    ("pre_greek", "Papoura"): 1.0,   # mg-c2af: Cretan inscription site
    ("pre_greek", "Psykhro"): 1.0,   # mg-c2af: Cretan cave (Diktaian)
    ("pre_greek", "Syme"): 1.0,      # mg-c2af: Cretan rural sanctuary
    ("pre_greek", "Haghios Stephanos"): 0.75,  # mg-c2af: Lakonian, off-Crete
    ("pre_greek", "Kythera"): 0.75,  # mg-c2af: Lakonian island, near-Crete
    ("pre_greek", "Melos"): 0.75,    # mg-c2af: Cycladic island, Linear-A site
    ("pre_greek", "Kea"): 0.75,  # Kea is Cycladic but pre-Greek substrate likely
    ("pre_greek", "Mycenae"): 0.5,  # mainland; less direct
    # Etruscan: Mediterranean substrate, plausible but indirect. The
    # `etruscan` rows are the original mg-7dd1 keys (kept for back-compat
    # with curated cross-pool hypotheses); the `etruria` rows are the
    # geographic tag actually used by pools/etruscan.yaml entries (mg-23cc
    # adds the second pool, parallel with `aquitania` for Aquitanian).
    ("etruscan", "Haghia Triada"): 0.5,
    ("etruscan", "Khania"): 0.5,
    ("etruscan", "Phaistos"): 0.5,
    ("etruscan", "Zakros"): 0.5,
    ("etruscan", "Knossos"): 0.5,
    ("etruria", "Haghia Triada"): 0.5,
    ("etruria", "Khania"): 0.5,
    ("etruria", "Phaistos"): 0.5,
    ("etruria", "Zakros"): 0.5,
    ("etruria", "Knossos"): 0.5,
    ("etruria", "Mallia"): 0.5,
    ("etruria", "Arkhanes"): 0.5,
    ("etruria", "Kea"): 0.5,
    ("etruria", "Tylissos"): 0.5,
    ("etruria", "Gournia"): 0.5,
    ("etruria", "Pyrgos"): 0.5,
    ("etruria", "Haghios Stephanos"): 0.5,
    ("etruria", "Kythera"): 0.5,
    ("etruria", "Melos"): 0.5,
    ("etruria", "Mycenae"): 0.5,
    ("etruria", "Papoura"): 0.5,
    ("etruria", "Psykhro"): 0.5,
    ("etruria", "Syme"): 0.5,
    # Linear-B carryover values: Knossos privileged.
    ("linear_b", "Knossos"): 1.0,
    ("linear_b", "Haghia Triada"): 0.5,
    ("linear_b", "Khania"): 0.5,
    ("linear_b", "Phaistos"): 0.5,
    ("linear_b", "Zakros"): 0.5,
    ("linear_b", "Mallia"): 0.5,
    ("linear_b", "Arkhanes"): 0.5,
}


# Semantic-field × genre compatibility. Genre comes from the inscription's
# `genre_hint`; semantic_field from the pool entry. Most Linear-A
# inscriptions are accountancy (742/772 in SigLA), so most of the table is
# about how well a given semantic field fits an accountancy tablet.
#
# Rationale: agriculture/food/animal/place/function/number all directly fit
# accountancy ledgers (commodities, totals, recipients); kin (people) fits
# moderately (recipient names but not the subject); descriptor/morphology
# are weakly relevant; weaponry / religious-dedication fit votive/inscription
# genre but not accountancy.
_GG1_SEMANTIC_COMPAT: dict[tuple[str, str], float] = {
    # Strong fits to accountancy tablets.
    ("agriculture", "accountancy"): 0.75,
    ("food", "accountancy"): 0.75,
    ("animal", "accountancy"): 0.75,
    ("place", "accountancy"): 0.75,
    ("function", "accountancy"): 0.75,
    ("number", "accountancy"): 1.0,
    ("commodity", "accountancy"): 1.0,
    # Moderate fits to accountancy tablets.
    ("kin", "accountancy"): 0.5,
    ("dwelling", "accountancy"): 0.5,
    ("nature", "accountancy"): 0.5,
    ("body", "accountancy"): 0.5,
    ("time", "accountancy"): 0.5,
    # Weak fits to accountancy tablets.
    ("descriptor", "accountancy"): 0.25,
    ("morphology", "accountancy"): 0.25,
    ("weaponry", "accountancy"): 0.25,
    ("religious", "accountancy"): 0.25,
    # Votive / inscription genre.
    ("religious", "votive_or_inscription"): 1.0,
    ("kin", "votive_or_inscription"): 0.75,
    ("descriptor", "votive_or_inscription"): 0.5,
    ("place", "votive_or_inscription"): 0.5,
    ("nature", "votive_or_inscription"): 0.5,
    ("agriculture", "votive_or_inscription"): 0.25,
    ("food", "votive_or_inscription"): 0.25,
    ("animal", "votive_or_inscription"): 0.25,
    ("number", "votive_or_inscription"): 0.25,
    # Administrative genre — similar to accountancy but slightly different
    # focus (records of decisions / personnel rather than commodities).
    ("function", "administrative"): 0.75,
    ("kin", "administrative"): 0.75,
    ("place", "administrative"): 0.75,
    ("number", "administrative"): 0.75,
    ("descriptor", "administrative"): 0.5,
    ("agriculture", "administrative"): 0.5,
    ("food", "administrative"): 0.5,
    ("animal", "administrative"): 0.5,
    ("nature", "administrative"): 0.25,
    ("dwelling", "administrative"): 0.5,
    ("body", "administrative"): 0.25,
    ("religious", "administrative"): 0.5,
    ("morphology", "administrative"): 0.25,
    ("time", "administrative"): 0.5,
    ("weaponry", "administrative"): 0.5,
}


@dataclass(frozen=True)
class GeographicGenreFitResult:
    """Result of ``geographic_genre_fit_v1`` on one candidate equation."""

    score: float
    metric_notes: str
    region_compat: float
    semantic_compat: float
    # Inputs the score was derived from (handy for diagnostics).
    region: str
    semantic_field: str
    site: str
    genre_hint: str


def _lookup_compat(
    table: dict[tuple[str, str], float], a: str | None, b: str | None
) -> tuple[float, str]:
    """Look up a compat score in the table. Returns (score, source) where
    `source` is one of {"table", "missing-a", "missing-b", "unmapped"}.

    Missing or empty fields → neutral 0.5; unmapped pairs → neutral 0.5
    (with a note so the caller can distinguish 'no data' from 'in table').
    """
    if not a:
        return _GG1_NEUTRAL, "missing-a"
    if not b:
        return _GG1_NEUTRAL, "missing-b"
    if (a, b) in table:
        return table[(a, b)], "table"
    return _GG1_NEUTRAL, "unmapped"


def geographic_genre_fit_v1(
    *,
    region: str | None,
    semantic_field: str | None,
    site: str | None,
    genre_hint: str | None,
    alpha: float = _GG1_DEFAULT_ALPHA,
) -> GeographicGenreFitResult:
    """Categorical compatibility between (region, semantic_field) and
    (site, genre_hint).

    Score in [0, 1]. Deterministic. No control distribution — this is a
    structural score, not a contrastive one. Missing/empty inputs and
    unmapped pairs both fall back to a 0.5 neutral.

    α defaults to 0.4: semantic carries more weight because the genre_hint
    (accountancy / votive / administrative / unknown) is a stronger signal
    of subject-matter fit than the site-level region mapping in the
    current taxonomy.
    """
    if not (0.0 <= alpha <= 1.0):
        raise ValueError(f"alpha must be in [0,1]; got {alpha}")
    region_v, region_src = _lookup_compat(_GG1_REGION_COMPAT, region, site)
    semantic_v, semantic_src = _lookup_compat(
        _GG1_SEMANTIC_COMPAT, semantic_field, genre_hint
    )
    score = alpha * region_v + (1.0 - alpha) * semantic_v
    notes = (
        f"geographic_genre_fit_v1: alpha={alpha}, "
        f"region_compat={region_v:.4f} ({region_src}, "
        f"region={region!r}, site={site!r}), "
        f"semantic_compat={semantic_v:.4f} ({semantic_src}, "
        f"semantic_field={semantic_field!r}, genre_hint={genre_hint!r})"
    )
    return GeographicGenreFitResult(
        score=float(score),
        metric_notes=notes,
        region_compat=float(region_v),
        semantic_compat=float(semantic_v),
        region=region or "",
        semantic_field=semantic_field or "",
        site=site or "",
        genre_hint=genre_hint or "",
    )


# ---------------------------------------------------------------------------
# partial_mapping_compression_delta_v0
# ---------------------------------------------------------------------------
#
# Wrapper around compression_delta_v0 that scores a candidate_equation.v1
# hypothesis as if its sign_to_phoneme dict were a global partial mapping.
# Lifted as its own metric (not just a re-call of compression_delta_v0)
# because the dispatch sites distinguish on metric *name* and the result row
# carries `metric` verbatim — so the same numeric machinery, viewed under
# this name, is a structurally orthogonal axis to local_fit_v1
# (corpus-side compression delta vs corpus-side per-sign position fit).
#
# Per mg-23cc rationale: within one Aquitanian surface (e.g. "ur") the
# bigram term is identical across all 47 candidates that share the surface,
# so within-surface discrimination MUST come from a corpus-side metric. The
# signed delta is the discriminator: positive deltas indicate the candidate's
# partial mapping compresses the corpus better; negative deltas indicate it
# makes things worse. Both are informative, and both can vary within a
# surface because different inscription windows pin the candidate to
# different sign sets.


@dataclass(frozen=True)
class PartialMappingCompressionResult:
    """Result of ``partial_mapping_compression_delta_v0`` on one candidate-
    equation hypothesis."""

    score: float
    bits_per_sign_baseline: float
    bits_per_sign_mapped: float
    baseline_bits: int
    mapped_bits: int
    stream_length: int
    contributing_signs: tuple[str, ...]
    metric_notes: str


def partial_mapping_compression_delta_v0(
    stream: list[str],
    signs: list[str],
    phonemes: list[str],
) -> PartialMappingCompressionResult:
    """Score a candidate equation by treating its sign_to_phoneme dict as a
    partial global mapping and computing ``compression_delta_v0``.

    **What it measures.** Given an equation that pins one inscription span to
    a candidate substrate root, take the local sign→phoneme dict and apply
    it *globally* across the whole corpus stream. The resulting compression
    delta (``baseline_bits − mapped_bits``) is the corpus-side score: how
    much better (positive) or worse (negative) does this partial mapping
    compress the entire corpus, not just the one window the equation was
    derived from?

    **Why this is structurally orthogonal to local_fit_v1.** local_fit_v1
    asks "does this span fit this root well *here*?". This metric asks
    "does this implied partial mapping compress *globally*?". Two equations
    that share a surface (e.g. all ~47 Aquitanian "ur" candidates) have
    identical local position/bigram terms but pin to different sign sets,
    so they disagree on this metric — the within-surface discriminator that
    mg-7dd1 diagnosed missing.

    **Determinism.** Identical (stream, signs, phonemes) ⇒ byte-identical
    score. Reuses the frozen-for-v0 zlib-L9 + 2-byte symbol encoder.

    **What invalidates it.**
      * (a) Most candidate equations cover signs that occur few times in the
        corpus, so the mapped stream is ~99% identical to the baseline and
        the delta is ~0. That is the *expected* behavior; the discriminator
        is the small fraction of equations whose mapping covers frequent
        signs. The distribution being mostly-zero is a feature.
      * (b) DEFLATE's byte-aligned output rounds away small permutation
        effects on tiny corpora; on the 761-record SigLA snapshot the
        signal is well above the rounding floor for high-frequency signs,
        but a fragmentary corpus would degrade discrimination.
    """
    if not signs:
        raise ValueError("partial_mapping_compression_delta_v0: equation has no signs")
    if len(signs) != len(phonemes):
        raise ValueError(
            f"partial_mapping_compression_delta_v0: |signs|={len(signs)} != "
            f"|phonemes|={len(phonemes)}"
        )
    mapping = dict(zip(signs, phonemes))
    if len(mapping) != len(signs):
        raise ValueError(
            f"partial_mapping_compression_delta_v0: signs must be pairwise distinct; got {signs!r}"
        )
    base = compression_delta_v0(stream, mapping)
    notes = (
        f"partial_mapping_compression_delta_v0: signs=[{','.join(signs)}], "
        f"phonemes=[{','.join(phonemes)}]; "
        f"baseline_bits={base.baseline_bits}, mapped_bits={base.mapped_bits}; "
        f"bits_per_sign_baseline={base.bits_per_sign_baseline:.4f}, "
        f"bits_per_sign_mapped={base.bits_per_sign_mapped:.4f}"
    )
    return PartialMappingCompressionResult(
        score=float(base.score),
        bits_per_sign_baseline=float(base.bits_per_sign_baseline),
        bits_per_sign_mapped=float(base.bits_per_sign_mapped),
        baseline_bits=int(base.baseline_bits),
        mapped_bits=int(base.mapped_bits),
        stream_length=int(base.stream_length),
        contributing_signs=tuple(signs),
        metric_notes=notes,
    )


# ---------------------------------------------------------------------------
# sign_prediction_perplexity_v0  (mg-ddee, harness v7)
# ---------------------------------------------------------------------------
#
# Re-frames the question. Existing metrics ask "given this substrate
# hypothesis, does the corpus look right?" — the per-phoneme position
# priors and the pool-derived bigrams encode "what corpus *should* look
# like under the hypothesis." mg-f419 found that this lets phonotactics
# alone account for the leaderboard, so the substrate identity adds no
# signal.
#
# This metric flips the direction. The corpus' own distributional
# structure produces a clustering of signs (corpus_phoneme_model.py),
# without using any substrate-pool prior. The metric then asks: does
# the candidate equation's (sign → phoneme) assignment AGREE with the
# cluster model's implicit class assignments? If so, mapping signs to
# their phonemes preserves predictability — substrate-real candidates
# should produce *better* agreement than random-control candidates if
# the corpus' structural patterns reflect a real underlying phonology.
#
# Formulation (two terms, summed; documented in detail in the docstring):
#
#   Term 1 (cluster agreement). Count over (sign, phoneme) pairs where
#     cluster_id(sign) == phoneme_to_modal_cluster(phoneme).
#     Range: integer in [0, n_pairs].
#
#   Term 2 (window bigram log-likelihood). Sum over adjacent sign pairs
#     in the equation's inscription window of
#     log P(cluster_id(sign_{i+1}) | cluster_id(sign_i))
#     under the corpus-derived bigram model.
#     Range: roughly [-7n, 0] in nats (n = window length - 1).
#
# Term 2 is a window-quality prior — it doesn't depend on the proposed
# phonemes, only on which signs the equation pins. Two candidates that
# happen to pick the same window get identical term-2 contributions,
# but the window IS chosen by the equation, so the term still discriminates
# between candidates that differ on which inscription/span they pin to.
# Term 1 is the phoneme-side discriminator and is the term where
# substrate-vs-control should differ if the metric works.


@dataclass(frozen=True)
class SignPredictionPerplexityResult:
    """Result of ``sign_prediction_perplexity_v0`` on a single equation."""

    score: float                       # term1 + term2
    cluster_agreement: int             # term1 (raw count in [0, n_pairs])
    window_bigram_loglik: float        # term2 (log P sum, nats)
    metric_notes: str
    n_pairs_scored: int
    n_window_bigrams: int


def sign_prediction_perplexity_v0(
    *,
    record: dict,
    equation: dict,
    cluster_model: "object",
) -> SignPredictionPerplexityResult:
    """Score a candidate equation against the corpus-derived cluster model.

    **What it measures.**

    Two terms, summed:

    1. *Cluster agreement.* For each (sign, phoneme) pair in the
       equation's ``sign_to_phoneme`` dict:
         - look up ``cluster_id(sign)`` from ``cluster_model.sign_to_cluster``;
         - look up ``modal_cluster(phoneme)`` from
           ``cluster_model.phoneme_to_modal_cluster``;
         - increment if the two are equal.
       The raw integer count is term-1. A candidate whose phoneme
       assignment puts each sign in a cluster *consistent with the
       phoneme's expected position behavior* scores high; a candidate
       that maps a vowel-final-friendly sign to a stop-onset phoneme
       scores low. Because the cluster model is pure-corpus, this
       discrimination does NOT come from substrate-pool identity — the
       phoneme-to-cluster bridge is the only place position priors enter,
       and they enter once at model build time, not per-candidate.

    2. *Window bigram log-likelihood.* For each adjacent (sign_i,
       sign_{i+1}) pair within the equation's inscription window
       (skipping intervening dividers / non-syllabograms), compute
       ``log P(cluster_id(sign_{i+1}) | cluster_id(sign_i))`` under the
       corpus-derived bigram. Sum.

    The metric value is ``score = term1 + term2``. Term 1 is in raw
    count units (~0..6 for a typical 6-sign equation); term 2 is a
    log-probability in nats (typically -1 to -3 per bigram). The two
    are deliberately on different scales — term 1 is the *phoneme-side*
    discriminator (substrate-vs-control should differ here), term 2 is a
    *window quality* prior. They are reported separately on the result
    row so analysis can lift either out.

    **Determinism.** Same (record, equation, cluster_model) ⇒
    byte-identical score. No randomness, no permutations.

    **What invalidates it.**
      * (a) Cluster model is degenerate (all signs in one cluster) ⇒
        term 1 collapses to "phoneme matches the dominant cluster" for
        every candidate, leaving term 2 as the only discriminator.
        Mitigated at build time by feature-axis weighting that keeps
        position-in-word as the dominant signal.
      * (b) Corpus is fragmentary ⇒ bigram counts get noisy and
        term 2 hits the smoothing floor.
      * (c) phoneme_to_modal_cluster's bridge mis-assigns a phoneme ⇒
        term 1 is consistently wrong for that phoneme; substrate
        candidates with that phoneme suffer along with controls so the
        paired-difference is unaffected (this is the design intent of
        paired-diff scoring).
    """
    sign_to_cluster: dict[str, int] = cluster_model.sign_to_cluster
    phoneme_to_modal: dict[str, int] = cluster_model.phoneme_to_modal_cluster
    log_probs: list[list[float]] = cluster_model.bigram_log_probs

    sign_to_phoneme = equation["sign_to_phoneme"]
    n_pairs = len(sign_to_phoneme)

    # Term 1: cluster agreement.
    cluster_agreement = 0
    missing_in_cluster: list[str] = []
    missing_in_phoneme_table: list[str] = []
    for sign, phoneme in sign_to_phoneme.items():
        if sign not in sign_to_cluster:
            missing_in_cluster.append(sign)
            continue
        # Phoneme bridging: take first character if multi-char (matches
        # the build-time PHONEME_POSITION_PROFILES handling).
        head = phoneme[:1] if phoneme else ""
        target_cluster = phoneme_to_modal.get(head)
        if target_cluster is None:
            missing_in_phoneme_table.append(phoneme)
            continue
        if sign_to_cluster[sign] == target_cluster:
            cluster_agreement += 1

    # Term 2: window bigram log-likelihood.
    tokens = record["tokens"]
    span = equation["span"]
    start, end = span[0], span[1]
    window = tokens[start : end + 1]
    # Filter to syllabograms that have cluster ids.
    window_clusters: list[int] = []
    for tok in window:
        if tok in sign_to_cluster:
            window_clusters.append(sign_to_cluster[tok])
    bigram_loglik = 0.0
    n_bigrams = 0
    for a, b in zip(window_clusters[:-1], window_clusters[1:]):
        bigram_loglik += log_probs[a][b]
        n_bigrams += 1

    score = float(cluster_agreement) + bigram_loglik
    diag_bits: list[str] = []
    if missing_in_cluster:
        diag_bits.append(
            f"signs missing from cluster model: {missing_in_cluster!r}"
        )
    if missing_in_phoneme_table:
        diag_bits.append(
            f"phonemes missing from phoneme→cluster table: "
            f"{missing_in_phoneme_table!r}"
        )
    notes = (
        f"sign_prediction_perplexity_v0: term1_cluster_agreement={cluster_agreement} "
        f"of {n_pairs}, term2_window_bigram_loglik={bigram_loglik:.4f} "
        f"over {n_bigrams} bigrams; n_pairs={n_pairs}"
    )
    if diag_bits:
        notes += "; " + "; ".join(diag_bits)
    return SignPredictionPerplexityResult(
        score=score,
        cluster_agreement=cluster_agreement,
        window_bigram_loglik=bigram_loglik,
        metric_notes=notes,
        n_pairs_scored=n_pairs,
        n_window_bigrams=n_bigrams,
    )


# ---------------------------------------------------------------------------
# external_phoneme_perplexity_v0  (mg-ee18, harness v8)
# ---------------------------------------------------------------------------
#
# Reframes the question one more level. mg-ddee's
# sign_prediction_perplexity_v0 used a corpus-derived cluster model
# whose phoneme→cluster bridge collapsed most of the inventory to one
# class, killing discrimination. v8 replaces the corpus-derived bridge
# with a *learned char-bigram model* trained on real text in the
# proposed substrate language (Basque for Aquitanian; Etruscan for
# Etruscan; Basque-as-stand-in for toponym, since no pre-Greek text
# corpus is available).
#
# Pipeline for one candidate equation (sign_to_phoneme partial mapping):
#
#   1. Apply the partial mapping to the entire Linear-A corpus stream.
#      Each token in the mapping's domain is replaced by its proposed
#      phoneme; tokens outside the domain stay as their AB-id.
#   2. The mapped stream is now an interleaving of phoneme strings,
#      AB-ids (treated as <unk>), and DIV / INSCRIPTION_BOUNDARY
#      markers.
#   3. Walk the stream extracting maximal contiguous *runs* of phoneme
#      tokens — runs are split by any of {<unk>, DIV, INSCRIPTION_BOUNDARY}.
#      Per the brief, runs are the unit on which the language model is
#      scored: the LM looks at "what does the phoneme stream look like
#      between un-mapped breaks?".
#   4. Char-decompose each run's phonemes (so multi-char ``th``, ``ph``,
#      ``ts`` become 2-char sequences). Wrap each run with the
#      ``<W>`` word-boundary sentinel. Score char-bigram log-likelihood
#      under the chosen model. Sum across runs.
#   5. Normalize by total scored characters across all runs. Report the
#      per-char average log-likelihood (in nats). Higher = more
#      language-like; substrate-real mappings should produce higher
#      values than random-control mappings of the same phonotactics.
#
# Pool-to-language dispatch:
#
#   * source_pool = "aquitanian"  → basque model
#   * source_pool = "etruscan"    → etruscan model
#   * source_pool = "toponym"     → basque model (substrate-style stand-in;
#                                    documented in the mg-ee18 brief as the
#                                    pre-Greek-text-unavailable case)
#   * any control_* pool          → its substrate's model (so the paired
#                                    diff is computed against the same
#                                    language model as the substrate side)
#   * unmatched (anchor / scramble / cross-pool) → metric is skipped
#
# The dispatch lives in scripts/run_sweep.py; the metric here is
# language-model-agnostic and accepts an external model object.

_EXT_OOV = "<unk>"


@dataclass(frozen=True)
class ExternalPhonemePerplexityResult:
    """Result of ``external_phoneme_perplexity_v0`` on one equation."""

    score: float                  # per-char average log-likelihood (nats)
    metric_notes: str
    n_runs: int
    n_chars_scored: int
    n_phonemes_scored: int
    total_loglik: float
    language: str                 # which LM was applied (e.g. "basque")


def external_phoneme_perplexity_v0(
    *,
    stream: list[str],
    mapping: dict[str, str],
    language_model: "object",
) -> ExternalPhonemePerplexityResult:
    """Score a candidate's partial sign→phoneme mapping under an external
    char-bigram language model.

    **What it measures.** After applying the mapping to the whole
    Linear-A corpus, what's the average char-bigram log-probability of
    the resulting phoneme runs under a model learned from real text in
    the proposed substrate language? "Substrate-real" mappings should
    produce phoneme streams that look like real Basque (or Etruscan)
    text, which the LM scores higher than mappings whose output is
    phonotactically arbitrary.

    **Run extraction.** Tokens outside the mapping become a synthetic
    ``<unk>`` boundary; ``DIV`` and ``INSCRIPTION_BOUNDARY`` are also
    treated as boundaries. A "run" is a maximal contiguous sequence of
    mapped phoneme tokens. Each run is char-decomposed (so ``"th"``
    becomes ``["t", "h"]``) and bracketed with ``<W>`` sentinels;
    char-bigram log-prob is summed over (n_chars + 1) bigrams per run.

    **Normalization.** ``score = total_loglik / n_chars_scored``. The
    per-char convention keeps the metric on a comparable scale across
    candidates that produce different total run lengths (a candidate
    that pins a frequent sign generates many more scored chars than
    one that pins a rare sign).

    **Determinism.** Same (stream, mapping, language_model) ⇒
    byte-identical score. No randomness, no permutations.

    **What invalidates it.**
      * (a) The mapping covers very few signs of the corpus ⇒ runs are
        short and few; scoring noise dominates. Most candidate
        equations sit here, which is fine — the discriminator is the
        small fraction of mapping configurations that produce many
        long runs.
      * (b) The language model was trained on a corpus too distant
        phonotactically from the substrate-as-realized-in-Linear-A.
        For Etruscan the corpus is small; α=1.0 in the model build
        widens the smoothing floor in compensation but leaves the
        LM noisy at the rare-bigram tail.
      * (c) Toponym candidates are scored against the Basque model as
        a substrate-style stand-in (no pre-Greek text corpus exists);
        a strong negative result there could mean either (i) the
        toponym hypothesis is wrong or (ii) Basque is the wrong
        stand-in. Future work could swap Linear-B carryover or a
        different substrate stand-in.
    """
    if language_model is None:
        raise ValueError(
            "external_phoneme_perplexity_v0: language_model is required; "
            "pass the substrate's pre-built ExternalPhonemeModel"
        )
    if not stream:
        raise ValueError("external_phoneme_perplexity_v0: empty stream")

    # Walk the stream once, accumulating runs of mapped phonemes.
    # Anything outside the mapping (or a structural break) ends a run.
    runs: list[list[str]] = []
    cur: list[str] = []
    for tok in stream:
        if tok in mapping:
            cur.append(mapping[tok])
        else:
            if cur:
                runs.append(cur)
                cur = []
    if cur:
        runs.append(cur)

    # Lazy import to avoid a top-level circular dependency between
    # metrics.py and external_phoneme_model.py (the latter imports
    # nothing from this module today, but keeping the import local
    # also makes the metric file's top stable for the other metrics
    # that don't touch the LM at all).
    from .external_phoneme_model import (
        WORD_BOUNDARY,
        char_decompose_phonemes,
    )

    total_loglik = 0.0
    n_chars = 0
    n_phonemes = 0
    for run in runs:
        chars = char_decompose_phonemes(run)
        if not chars:
            continue
        n_phonemes += len(run)
        n_chars += len(chars)
        # Bracketed sequence: <W> c1 c2 ... cn <W>
        seq = [WORD_BOUNDARY, *chars, WORD_BOUNDARY]
        for prev, cur_tok in zip(seq[:-1], seq[1:]):
            total_loglik += language_model.log_prob(prev, cur_tok)

    score = (total_loglik / n_chars) if n_chars > 0 else 0.0
    name = getattr(language_model, "name", "unknown")
    notes = (
        f"external_phoneme_perplexity_v0: language={name}, "
        f"n_runs={len(runs)}, n_phonemes={n_phonemes}, "
        f"n_chars_scored={n_chars}, total_loglik={total_loglik:.4f}, "
        f"per_char={score:.6f}"
    )
    return ExternalPhonemePerplexityResult(
        score=float(score),
        metric_notes=notes,
        n_runs=len(runs),
        n_chars_scored=n_chars,
        n_phonemes_scored=n_phonemes,
        total_loglik=float(total_loglik),
        language=str(name),
    )


METRICS = {
    "compression_delta_v0": compression_delta_v0,
    "local_fit_v0": local_fit_v0,
    "local_fit_v1": local_fit_v1,
    "geographic_genre_fit_v1": geographic_genre_fit_v1,
    "partial_mapping_compression_delta_v0": partial_mapping_compression_delta_v0,
    "sign_prediction_perplexity_v0": sign_prediction_perplexity_v0,
    "external_phoneme_perplexity_v0": external_phoneme_perplexity_v0,
}
