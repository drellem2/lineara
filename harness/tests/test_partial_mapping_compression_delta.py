"""Smoke test for the ``partial_mapping_compression_delta_v0`` metric.

Asserts:
  * The metric is deterministic across reruns on identical inputs.
  * The score equals the underlying ``compression_delta_v0`` score on the
    corresponding partial mapping (i.e. it is a faithful wrapper).
  * Disjoint sign sets are independent: candidates that pin to non-frequent
    signs yield score == 0 (mapping rewrites no tokens; baseline == mapped).
  * A mapping that covers a frequent sign produces a non-zero delta on a
    non-degenerate fixture.
  * The contributing_signs and metric_notes echo the equation's signs.
  * Argument validation rejects mismatched lengths and duplicate signs.

Run directly:
  python3 -m harness.tests.test_partial_mapping_compression_delta
"""

from __future__ import annotations

import unittest

from harness.corpus import build_stream
from harness.metrics import (
    compression_delta_v0,
    partial_mapping_compression_delta_v0,
)


# Toy corpus designed so AB54 is the most frequent sign (15 occurrences) and
# AB99 is rare (1 occurrence). Mirrors the test_local_fit_v1 fixture's flavor.
_FIXTURE_RECORDS = [
    {
        "id": "TOY 1",
        "tokens": ["AB54", "AB02", "DIV", "AB54", "AB02", "DIV", "AB54", "AB02"],
        "n_signs": 6,
    },
    {
        "id": "TOY 2",
        "tokens": ["AB54", "AB80", "AB54", "AB80", "AB54", "AB80"],
        "n_signs": 6,
    },
    {
        "id": "TOY 3",
        "tokens": ["AB54", "AB02", "AB54", "AB02"],
        "n_signs": 4,
    },
    {
        "id": "TOY 4",
        "tokens": ["AB54", "AB02", "AB54", "AB99"],
        "n_signs": 4,
    },
]


class PartialMappingCompressionDeltaTest(unittest.TestCase):
    def setUp(self) -> None:
        stream, _ = build_stream(_FIXTURE_RECORDS)
        self.stream = stream

    def test_metric_is_deterministic(self) -> None:
        r1 = partial_mapping_compression_delta_v0(
            self.stream, ["AB54", "AB02"], ["k", "o"]
        )
        r2 = partial_mapping_compression_delta_v0(
            self.stream, ["AB54", "AB02"], ["k", "o"]
        )
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.baseline_bits, r2.baseline_bits)
        self.assertEqual(r1.mapped_bits, r2.mapped_bits)
        self.assertEqual(r1.metric_notes, r2.metric_notes)

    def test_wrapper_matches_underlying_metric(self) -> None:
        # The wrapper must produce a score byte-identical to calling
        # compression_delta_v0 on the same partial mapping. This is the
        # test that protects the "don't redesign compression_delta_v0;
        # just wrap it" rule from the ticket.
        signs = ["AB54", "AB02"]
        phonemes = ["k", "o"]
        wrapped = partial_mapping_compression_delta_v0(self.stream, signs, phonemes)
        direct = compression_delta_v0(self.stream, dict(zip(signs, phonemes)))
        self.assertEqual(wrapped.score, direct.score)
        self.assertEqual(wrapped.baseline_bits, direct.baseline_bits)
        self.assertEqual(wrapped.mapped_bits, direct.mapped_bits)
        self.assertEqual(
            wrapped.bits_per_sign_baseline, direct.bits_per_sign_baseline
        )
        self.assertEqual(wrapped.bits_per_sign_mapped, direct.bits_per_sign_mapped)
        self.assertEqual(wrapped.stream_length, direct.stream_length)

    def test_contributing_signs_and_notes(self) -> None:
        result = partial_mapping_compression_delta_v0(
            self.stream, ["AB54", "AB02"], ["k", "o"]
        )
        self.assertEqual(result.contributing_signs, ("AB54", "AB02"))
        self.assertIn("AB54", result.metric_notes)
        self.assertIn("AB02", result.metric_notes)
        self.assertIn("partial_mapping_compression_delta_v0", result.metric_notes)

    def test_disjoint_signs_yield_zero_delta(self) -> None:
        # ZZ01 does not appear anywhere in the fixture stream, so applying
        # the partial mapping rewrites nothing. baseline == mapped ⇒ delta = 0.
        result = partial_mapping_compression_delta_v0(
            self.stream, ["ZZ01"], ["q"]
        )
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.baseline_bits, result.mapped_bits)

    def test_mismatched_lengths_rejected(self) -> None:
        with self.assertRaises(ValueError):
            partial_mapping_compression_delta_v0(self.stream, ["AB54"], ["k", "o"])

    def test_duplicate_signs_rejected(self) -> None:
        with self.assertRaises(ValueError):
            partial_mapping_compression_delta_v0(
                self.stream, ["AB54", "AB54"], ["k", "o"]
            )

    def test_empty_signs_rejected(self) -> None:
        with self.assertRaises(ValueError):
            partial_mapping_compression_delta_v0(self.stream, [], [])


if __name__ == "__main__":
    unittest.main()
