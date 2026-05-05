"""Smoke tests for scripts/per_inscription_coherence.py (mg-3438, harness v19).

Exercises the per-inscription consensus aggregation on a hand-built
minimal inscription with 3 signs and 4 candidate equations:

  Inscription I = AB01 - AB02 - AB03

  Candidate 1:  AB01→a, AB02→s, AB03→i        (positive paired_diff)
  Candidate 2:  AB01→a, AB02→s, AB03→e        (positive paired_diff)
  Candidate 3:  AB01→a, AB02→s, AB03→i        (positive paired_diff)
  Candidate 4:  AB01→o, AB02→l                (NEGATIVE paired_diff — excluded)

Expected per-inscription histograms:
  AB01: {a: 3}                   → modal=a, n=3, modal_posterior=1.0 (V=1)
  AB02: {s: 3}                   → modal=s, n=3, modal_posterior=1.0 (V=1)
  AB03: {i: 2, e: 1}             → modal=i, n=3, modal_posterior=2.5/4 = 0.625

All three signs pass the threshold of 0.5; all three have n_proposals ≥ 2.
fraction_high_coherence_signs = 3/3 = 1.0.
fraction_robust_high_coherence_signs = 3/3 = 1.0.

A second test verifies a 1-sign-no-proposal inscription drops the
fraction proportionally; a third verifies that lone-proposal signs
pass the literal threshold but fail the robust threshold.

Determinism: the aggregation + classification is byte-stable across
re-runs on the same input.
"""

from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PIC_PATH = _REPO_ROOT / "scripts" / "per_inscription_coherence.py"


class SyllabographicTokensTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_drops_div_log_unknown(self) -> None:
        tokens = ["AB01", "DIV", "LOG:AB16", "AB02", "[?]", "AB03"]
        self.assertEqual(
            self.pic.syllabographic_tokens(tokens),
            ["AB01", "AB02", "AB03"],
        )

    def test_keeps_suffixed_variants(self) -> None:
        # AB21f, AB131b appear in the corpus and are valid syllabograms
        # in the sign_to_phoneme keyspace if a candidate proposes them.
        tokens = ["AB21f", "AB131b", "AB01"]
        self.assertEqual(
            self.pic.syllabographic_tokens(tokens),
            ["AB21f", "AB131b", "AB01"],
        )

    def test_drops_a_prefixed(self) -> None:
        # A301, A302 etc are non-AB syllabograms not in the v8/v9 keyspace.
        tokens = ["AB01", "A301", "AB02", "A302"]
        self.assertEqual(
            self.pic.syllabographic_tokens(tokens),
            ["AB01", "AB02"],
        )


class PerSignConsensusLocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_unanimous_n_3_modal_posterior_1(self) -> None:
        # n=3, all "a"; V=1; (3 + 0.5) / (3 + 0.5*1) = 1.0
        info = self.pic.per_sign_consensus_local({"a": 3}, alpha=0.5)
        self.assertEqual(info["modal_phoneme"], "a")
        self.assertEqual(info["modal_count"], 3)
        self.assertEqual(info["n_proposals"], 3)
        self.assertEqual(info["n_distinct_phonemes"], 1)
        self.assertAlmostEqual(info["modal_posterior"], 1.0, places=10)
        self.assertAlmostEqual(info["entropy_bits"], 0.0, places=10)

    def test_2_to_1_split_modal_posterior(self) -> None:
        # {i:2, e:1}; V=2; modal=i; (2 + 0.5) / (3 + 0.5*2) = 2.5/4 = 0.625
        info = self.pic.per_sign_consensus_local({"i": 2, "e": 1}, alpha=0.5)
        self.assertEqual(info["modal_phoneme"], "i")
        self.assertAlmostEqual(info["modal_posterior"], 0.625, places=10)

    def test_1_to_1_split_at_threshold(self) -> None:
        # {a:1, e:1}; V=2; modal=a (alphabetical); (1+0.5)/(2+1) = 0.5
        info = self.pic.per_sign_consensus_local({"e": 1, "a": 1}, alpha=0.5)
        self.assertEqual(info["modal_phoneme"], "a")
        self.assertAlmostEqual(info["modal_posterior"], 0.5, places=10)

    def test_lone_proposal_modal_posterior_1(self) -> None:
        # {x:1}; V=1; (1+0.5)/(1+0.5) = 1.0 — passes the literal-brief
        # threshold trivially. The robust statistic is what excludes
        # this from cascade classification.
        info = self.pic.per_sign_consensus_local({"x": 1}, alpha=0.5)
        self.assertEqual(info["n_proposals"], 1)
        self.assertAlmostEqual(info["modal_posterior"], 1.0, places=10)

    def test_empty_histogram_returns_none(self) -> None:
        self.assertIsNone(self.pic.per_sign_consensus_local({}, alpha=0.5))


class PerInscriptionCoherenceTest(unittest.TestCase):
    """End-to-end on the hand-built 3-sign / 4-candidate example from the docstring."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_three_sign_inscription_all_high_coherence(self) -> None:
        # Histograms after dropping the negative-paired-diff candidate 4:
        #   AB01: {a: 3}        ← unanimous
        #   AB02: {s: 3}        ← unanimous
        #   AB03: {i: 2, e: 1}  ← 2/1 split, modal=i, posterior=0.625
        histograms = {
            "AB01": {"a": 3},
            "AB02": {"s": 3},
            "AB03": {"i": 2, "e": 1},
        }
        out = self.pic.per_inscription_coherence(
            inscription_id="TEST 1",
            tokens=["AB01", "AB02", "AB03"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["n_tokens_syllabographic"], 3)
        self.assertEqual(out["n_tokens_with_proposals"], 3)
        self.assertEqual(out["n_tokens_high_coherence"], 3)
        self.assertEqual(out["n_tokens_robust_high_coherence"], 3)
        self.assertAlmostEqual(out["fraction_high_coherence_signs"], 1.0, places=10)
        self.assertAlmostEqual(
            out["fraction_robust_high_coherence_signs"], 1.0, places=10
        )
        self.assertEqual(out["mechanical_reading"], "a-s-i")
        # AB03 modal_posterior 0.625; AB01 / AB02 unanimous.
        self.assertAlmostEqual(
            out["per_sign"]["AB03"]["modal_posterior"], 0.625, places=10
        )

    def test_uncovered_sign_drops_fraction(self) -> None:
        # 4-token inscription where only 3 signs have proposals: the 4th
        # is rendered "·" and counts in the denominator but not the
        # numerator.
        histograms = {
            "AB01": {"a": 3},
            "AB02": {"s": 3},
            "AB03": {"i": 3},
        }
        out = self.pic.per_inscription_coherence(
            inscription_id="TEST 2",
            tokens=["AB01", "AB02", "AB03", "AB99"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["n_tokens_syllabographic"], 4)
        self.assertEqual(out["n_tokens_with_proposals"], 3)
        self.assertEqual(out["n_tokens_high_coherence"], 3)
        self.assertAlmostEqual(out["fraction_high_coherence_signs"], 0.75, places=10)
        self.assertAlmostEqual(
            out["fraction_robust_high_coherence_signs"], 0.75, places=10
        )
        self.assertEqual(out["mechanical_reading"], "a-s-i-·")

    def test_lone_proposal_passes_literal_fails_robust(self) -> None:
        # AB01 has a lone proposal: literal pass (modal_posterior=1.0)
        # but fails robust (n_proposals=1 < 2). AB02 has 2 unanimous.
        histograms = {
            "AB01": {"x": 1},
            "AB02": {"y": 2},
        }
        out = self.pic.per_inscription_coherence(
            inscription_id="TEST 3",
            tokens=["AB01", "AB02"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["n_tokens_high_coherence"], 2)
        self.assertEqual(out["n_tokens_robust_high_coherence"], 1)
        self.assertAlmostEqual(out["fraction_high_coherence_signs"], 1.0, places=10)
        self.assertAlmostEqual(
            out["fraction_robust_high_coherence_signs"], 0.5, places=10
        )
        # Mechanical reading: lone-proposal flagged with `*`, robust bare.
        self.assertEqual(out["mechanical_reading"], "x*-y")

    def test_repeated_sign_is_per_token_weighted(self) -> None:
        # Sign AB01 appears 3× and is high-coherence; AB02 once and
        # below threshold. Per-token fraction = 3/4 = 0.75.
        histograms = {
            "AB01": {"a": 3},
            "AB02": {"e": 1, "i": 1},  # 1/1 → modal_posterior = 0.5 (NOT > 0.5)
        }
        out = self.pic.per_inscription_coherence(
            inscription_id="TEST 4",
            tokens=["AB01", "AB02", "AB01", "AB01"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["n_tokens_syllabographic"], 4)
        self.assertEqual(out["n_tokens_high_coherence"], 3)
        self.assertAlmostEqual(out["fraction_high_coherence_signs"], 0.75, places=10)

    def test_below_threshold_in_parens(self) -> None:
        # 1/1 split → modal_posterior = 0.5 (not > 0.5) → parens.
        histograms = {"AB01": {"a": 1, "e": 1}}
        out = self.pic.per_inscription_coherence(
            inscription_id="TEST 5",
            tokens=["AB01"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["mechanical_reading"], "(a)")
        self.assertEqual(out["n_tokens_high_coherence"], 0)


class ClassifyCascadeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_thresholds(self) -> None:
        self.assertEqual(
            self.pic.classify_cascade(0.5, cascade_bar=0.5, partial_bar=0.25),
            "Cascade candidate",
        )
        self.assertEqual(
            self.pic.classify_cascade(0.49, cascade_bar=0.5, partial_bar=0.25),
            "Partial cascade",
        )
        self.assertEqual(
            self.pic.classify_cascade(0.25, cascade_bar=0.5, partial_bar=0.25),
            "Partial cascade",
        )
        self.assertEqual(
            self.pic.classify_cascade(0.24, cascade_bar=0.5, partial_bar=0.25),
            "Noise",
        )
        self.assertEqual(
            self.pic.classify_cascade(0.0, cascade_bar=0.5, partial_bar=0.25),
            "Noise",
        )

    def test_nan_passthrough(self) -> None:
        self.assertEqual(
            self.pic.classify_cascade(float("nan"), cascade_bar=0.5, partial_bar=0.25),
            "n/a",
        )


class PopulationCNeedleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_libation_needle_canonical(self) -> None:
        self.assertEqual(
            self.pic._LIBATION_NEEDLE,
            ("AB57", "AB31", "AB31", "AB60", "AB13"),
        )

    def test_subseq_match_with_div_skipped(self) -> None:
        tokens = [
            "AB59", "AB06", "AB28", "DIV", "[?]", "DIV",
            "AB57", "AB37", "DIV",
            "AB57", "AB31", "AB31", "AB60", "AB13", "DIV",
            "AB27", "AB28", "AB44",
        ]
        self.assertTrue(
            self.pic._find_subseq_with_div(tokens, ("AB57", "AB31", "AB31", "AB60", "AB13"))
        )

    def test_subseq_no_match(self) -> None:
        tokens = ["AB01", "AB02", "AB03"]
        self.assertFalse(
            self.pic._find_subseq_with_div(tokens, ("AB57", "AB31", "AB31", "AB60", "AB13"))
        )


class PopulationBSelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_filters_by_n_signs_and_sorts_by_candidate_count(self) -> None:
        corpus = [
            {"id": "A", "n_signs": 3},
            {"id": "B", "n_signs": 5},
            {"id": "C", "n_signs": 6},  # too long
            {"id": "D", "n_signs": 0},  # zero excluded
            {"id": "E", "n_signs": 2},
        ]
        n_pos = {"A": 100, "B": 50, "C": 999, "D": 1, "E": 75}
        selected = self.pic.select_population_b(
            corpus=corpus,
            n_pos_records_by_ins=n_pos,
            max_signs=5,
            top_n=10,
        )
        # Order: A (100), E (75), B (50). C excluded (n_signs > 5);
        # D excluded (n_signs == 0).
        self.assertEqual(selected, ["A", "E", "B"])

    def test_excludes_zero_record_inscriptions(self) -> None:
        corpus = [{"id": "X", "n_signs": 3}, {"id": "Y", "n_signs": 4}]
        n_pos = {"X": 0, "Y": 5}
        selected = self.pic.select_population_b(
            corpus=corpus, n_pos_records_by_ins=n_pos, max_signs=5, top_n=10,
        )
        self.assertEqual(selected, ["Y"])


class DeterminismTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_idempotent_per_inscription(self) -> None:
        histograms = {
            "AB01": {"a": 5, "e": 2},
            "AB02": {"s": 8},
            "AB03": {"i": 3, "e": 3},
        }
        a = self.pic.per_inscription_coherence(
            inscription_id="X",
            tokens=["AB01", "AB02", "AB03"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        b = self.pic.per_inscription_coherence(
            inscription_id="X",
            tokens=["AB01", "AB02", "AB03"],
            histograms=histograms,
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(a, b)


class EmptyTokensTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pic = _load_module("per_inscription_coherence", _PIC_PATH)

    def test_empty_tokens_yields_nan_fraction(self) -> None:
        out = self.pic.per_inscription_coherence(
            inscription_id="EMPTY",
            tokens=[],
            histograms={"AB01": {"a": 3}},
            alpha=0.5,
            threshold=0.5,
        )
        self.assertEqual(out["n_tokens_syllabographic"], 0)
        self.assertTrue(math.isnan(out["fraction_high_coherence_signs"]))
        self.assertTrue(math.isnan(out["fraction_robust_high_coherence_signs"]))


if __name__ == "__main__":
    unittest.main()
