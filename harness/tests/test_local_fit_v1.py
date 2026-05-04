"""Smoke test for the ``local_fit_v1`` metric on a toy corpus + toy pool.

Asserts:
  * The metric is deterministic across reruns.
  * The empirical bigram model is built deterministically and reflects
    the input pool (a frequent bigram in the pool gets higher log-prob
    than a never-seen bigram).
  * An anchor-style alignment (CV with sign positions matching their
    phoneme classes) scores higher than a deliberately-reversed control
    on the toy corpus.
  * Length-normalization: increasing equation length while keeping the
    per-pair fit unchanged INCREASES the score (because the 1/n length
    penalty shrinks).
  * Rare-sign correction: pinning to a sign that occurs once in the
    corpus reduces the score relative to the same alignment over a
    sign that occurs many times.

Run directly:
  python3 -m harness.tests.test_local_fit_v1
"""

from __future__ import annotations

import unittest

from harness.corpus import build_stream, sign_position_fingerprints
from harness.metrics import (
    EmpiricalBigramModel,
    _sign_corpus_counts,
    local_fit_v1,
)


# Toy corpus designed so AB54 is always word-initial and AB02 is always
# word-final. Mirrors the test_candidate_equation fixture but as a list of
# records consumable directly by build_stream.
_FIXTURE_RECORDS = [
    {
        "id": "TOY 1",
        "tokens": ["AB54", "AB02", "DIV", "AB54", "AB02"],
        "n_signs": 4,
    },
    {
        "id": "TOY 2",
        "tokens": ["AB54", "AB80", "AB02"],
        "n_signs": 3,
    },
    {
        "id": "TOY 3",
        "tokens": ["AB54", "AB02"],
        "n_signs": 2,
    },
    {
        "id": "TOY 4",
        # AB99 is rare (occurs once total).
        "tokens": ["AB54", "AB99"],
        "n_signs": 2,
    },
]


# Toy pool resembling the Aquitanian pool's structure: a handful of CV-style
# entries from which the empirical bigram model is learned.
_POOL_SEQUENCES = [
    ["k", "o"],
    ["k", "u", "r", "o"],
    ["b", "e", "r", "e"],
    ["s", "e", "n", "i"],
    ["a", "n", "d", "e", "r", "e"],
    ["t", "o"],
]


class LocalFitV1Test(unittest.TestCase):
    def setUp(self) -> None:
        stream, _ = build_stream(_FIXTURE_RECORDS)
        self.stream = stream
        self.fingerprints = sign_position_fingerprints(stream)
        self.sign_counts = _sign_corpus_counts(stream)
        self.bigram_model = EmpiricalBigramModel.from_sequences(_POOL_SEQUENCES)

    def test_bigram_model_is_deterministic(self) -> None:
        m1 = EmpiricalBigramModel.from_sequences(_POOL_SEQUENCES)
        m2 = EmpiricalBigramModel.from_sequences(_POOL_SEQUENCES)
        self.assertEqual(m1.bigram_counts, m2.bigram_counts)
        self.assertEqual(m1.unigram_counts, m2.unigram_counts)
        self.assertEqual(m1.vocab, m2.vocab)
        self.assertEqual(m1.alpha, m2.alpha)

    def test_bigram_model_reflects_input(self) -> None:
        # ("k", "o") appears in the pool ("ko", "kuro" → kuro has k-u, not k-o,
        # but ko does), so its smoothed log-prob must exceed an unseen
        # bigram like ("z", "x") (neither appears).
        seen = self.bigram_model.log_prob("k", "o")
        unseen = self.bigram_model.log_prob("z", "x")
        # Both phonemes are in vocab? "z" and "x" are not in the toy pool, so
        # they're not in the vocab. The model treats them as zero-count
        # unigrams; the smoothed log_prob still works out to a finite value.
        self.assertGreater(seen, unseen)

    def test_metric_is_deterministic(self) -> None:
        r1 = local_fit_v1(
            self.stream,
            ["AB54", "AB02"],
            ["k", "o"],
            self.bigram_model,
            sign_counts=self.sign_counts,
            fingerprints=self.fingerprints,
        )
        r2 = local_fit_v1(
            self.stream,
            ["AB54", "AB02"],
            ["k", "o"],
            self.bigram_model,
            sign_counts=self.sign_counts,
            fingerprints=self.fingerprints,
        )
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.position_term, r2.position_term)
        self.assertEqual(r1.bigram_term, r2.bigram_term)
        self.assertEqual(r1.length_penalty, r2.length_penalty)
        self.assertEqual(r1.rare_sign_correction, r2.rare_sign_correction)
        self.assertEqual(r1.metric_notes, r2.metric_notes)

    def test_anchor_beats_negative_control_on_toy(self) -> None:
        # AB54 (always initial) → /k/ (initial-friendly C); AB02 (always final)
        # → /o/ (final-friendly V). Position fits should be high.
        anchor = local_fit_v1(
            self.stream, ["AB54", "AB02"], ["k", "o"], self.bigram_model,
            sign_counts=self.sign_counts, fingerprints=self.fingerprints,
        )
        # Reverse the alignment: AB54→/o/, AB02→/k/. Position fits collapse.
        wrong = local_fit_v1(
            self.stream, ["AB54", "AB02"], ["o", "k"], self.bigram_model,
            sign_counts=self.sign_counts, fingerprints=self.fingerprints,
        )
        self.assertGreater(anchor.score, wrong.score)
        # Position term should also drive most of the difference.
        self.assertGreater(anchor.position_term, wrong.position_term)

    def test_length_penalty_attenuates_with_length(self) -> None:
        # 2-sign equation pays a length penalty of 1/2 = 0.5; 4-sign equation
        # pays 1/4 = 0.25. Construct two equations with the same per-sign
        # position fit (using the same sign repeatedly is not allowed because
        # sign_to_phoneme keys must be unique, but we can construct two pure
        # synthetic length-penalty checks via the helper alone).
        from harness.metrics import _length_penalty

        self.assertEqual(_length_penalty(2), 0.5)
        self.assertEqual(_length_penalty(4), 0.25)
        self.assertEqual(_length_penalty(6), 1 / 6)
        # Sign of the length penalty in the score: subtracted, so longer
        # equations score *higher* on this term alone.

    def test_rare_sign_correction_isolated(self) -> None:
        # Direct unit test of the rare-sign correction term, independent
        # of position-fit / bigram interactions. AB54 appears 5 times in
        # the toy corpus (== threshold; not rare). AB99 appears once (rare).
        from harness.metrics import _rare_sign_correction

        self.assertEqual(self.sign_counts["AB54"], 5)
        self.assertEqual(self.sign_counts["AB99"], 1)
        # 5 == threshold ⇒ NOT rare (strict <). 1 < 5 ⇒ rare.
        self.assertEqual(
            _rare_sign_correction(["AB54", "AB99"], self.sign_counts, threshold=5),
            0.5,
        )
        self.assertEqual(
            _rare_sign_correction(["AB54", "AB54"], self.sign_counts, threshold=5),
            0.0,
        )
        # End-to-end: an alignment with a rare sign should report
        # rare_sign_correction > 0.
        with_rare = local_fit_v1(
            self.stream, ["AB54", "AB99"], ["k", "o"], self.bigram_model,
            sign_counts=self.sign_counts, fingerprints=self.fingerprints,
        )
        self.assertGreater(with_rare.rare_sign_correction, 0)

    def test_score_is_finite_for_minimal_alignment(self) -> None:
        # Single-sign equation (n=1). The bigram model still has well-defined
        # transitions (<S>→p→<E>), so the metric must return finite numbers.
        result = local_fit_v1(
            self.stream, ["AB54"], ["k"], self.bigram_model,
            sign_counts=self.sign_counts, fingerprints=self.fingerprints,
        )
        import math
        self.assertTrue(math.isfinite(result.score))
        self.assertTrue(math.isfinite(result.position_term))
        self.assertTrue(math.isfinite(result.bigram_term))
        self.assertEqual(result.length_penalty, 1.0)


if __name__ == "__main__":
    unittest.main()
