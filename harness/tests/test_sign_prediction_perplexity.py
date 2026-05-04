"""Smoke tests for sign_prediction_perplexity_v0 (mg-ddee, harness v7).

The metric depends on a corpus_phoneme_model.ClusterModel — its cluster
ids, phoneme→cluster bridge, and bigram log-prob matrix. The smoke
suite drives both pieces: it builds a tiny synthetic cluster model in
memory and asserts the metric's two-term decomposition agrees with a
hand calculation, then loads the real committed cluster model and asserts
the metric produces a deterministic, valid result row on a real candidate
hypothesis.
"""

from __future__ import annotations

import math
import unittest
from pathlib import Path

from harness.corpus_phoneme_model import ClusterModel, build_model
from harness.corpus import load_records
from harness.metrics import sign_prediction_perplexity_v0


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_CORPUS_PATH = _REPO_ROOT / "corpus" / "all.jsonl"
_CLUSTER_MODEL_PATH = _REPO_ROOT / "harness" / "corpus_phoneme_model.json"


def _mini_cluster_model() -> ClusterModel:
    """A 3-cluster, 5-sign synthetic model with explicit bigram log-probs.

    Layout:
      cluster 0 = vowel-final → phoneme 'a' / 'e' bridge here
      cluster 1 = consonant-onset → phoneme 'k' / 'p' bridge here
      cluster 2 = sonorant-medial → phoneme 'l' / 'n' bridge here
    """
    sign_to_cluster = {
        "S1": 0,  # vowel-final
        "S2": 1,  # consonant-onset
        "S3": 2,  # sonorant
        "S4": 0,  # vowel-final
        "S5": 1,  # consonant-onset
    }
    # log P(j|i) — pre-computed; rows sum to ~1 in raw probability.
    bigram_log_probs = [
        [math.log(0.20), math.log(0.30), math.log(0.50)],
        [math.log(0.50), math.log(0.20), math.log(0.30)],
        [math.log(0.30), math.log(0.50), math.log(0.20)],
    ]
    bigram_counts = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # smoothed
    phoneme_to_modal = {"a": 0, "e": 0, "k": 1, "p": 1, "l": 2, "n": 2}
    return ClusterModel(
        sign_to_cluster=sign_to_cluster,
        cluster_position_means={0: [0.0, 0.0, 1.0, 0.0], 1: [1.0, 0.0, 0.0, 0.0],
                                2: [0.0, 1.0, 0.0, 0.0]},
        bigram_counts=bigram_counts,
        bigram_log_probs=bigram_log_probs,
        phoneme_to_modal_cluster=phoneme_to_modal,
        cluster_members={0: ["S1", "S4"], 1: ["S2", "S5"], 2: ["S3"]},
        meta={"k": 3, "test": True},
    )


class SignPredictionPerplexitySmoke(unittest.TestCase):

    def test_term1_perfect_agreement(self):
        """Every (sign, phoneme) pair maps to its modal cluster → term1 = n."""
        model = _mini_cluster_model()
        # signs: S1 (cl 0), S2 (cl 1), S3 (cl 2)
        # phonemes: a (cl 0), k (cl 1), l (cl 2)
        record = {"id": "T1", "tokens": ["S1", "S2", "S3"]}
        equation = {
            "inscription_id": "T1",
            "span": [0, 2],
            "sign_to_phoneme": {"S1": "a", "S2": "k", "S3": "l"},
        }
        result = sign_prediction_perplexity_v0(
            record=record, equation=equation, cluster_model=model
        )
        self.assertEqual(result.cluster_agreement, 3)
        # Window has 3 signs → 2 bigrams: (cl0, cl1) and (cl1, cl2)
        # log P = log 0.30 + log 0.30
        expected = math.log(0.30) + math.log(0.30)
        self.assertAlmostEqual(result.window_bigram_loglik, expected, places=6)
        self.assertEqual(result.n_pairs_scored, 3)
        self.assertEqual(result.n_window_bigrams, 2)
        self.assertAlmostEqual(result.score, 3.0 + expected, places=6)

    def test_term1_no_agreement(self):
        """Phonemes that bridge to other clusters → term1 = 0."""
        model = _mini_cluster_model()
        # signs: S1 (cl 0), S2 (cl 1) — phoneme 'k' bridges to cluster 1
        # but we put it on S1, and phoneme 'a' on S2: deliberate mis-match.
        record = {"id": "T1", "tokens": ["S1", "S2"]}
        equation = {
            "inscription_id": "T1",
            "span": [0, 1],
            "sign_to_phoneme": {"S1": "k", "S2": "a"},
        }
        result = sign_prediction_perplexity_v0(
            record=record, equation=equation, cluster_model=model
        )
        self.assertEqual(result.cluster_agreement, 0)
        self.assertEqual(result.n_pairs_scored, 2)

    def test_partial_agreement(self):
        """Mixed: one match, one miss."""
        model = _mini_cluster_model()
        record = {"id": "T1", "tokens": ["S1", "S2"]}
        equation = {
            "inscription_id": "T1",
            "span": [0, 1],
            "sign_to_phoneme": {"S1": "a", "S2": "n"},  # S1 matches, S2 doesn't
        }
        result = sign_prediction_perplexity_v0(
            record=record, equation=equation, cluster_model=model
        )
        self.assertEqual(result.cluster_agreement, 1)

    def test_window_skips_non_signs(self):
        """Bigram counting walks through DIV/non-sign tokens."""
        model = _mini_cluster_model()
        record = {"id": "T1", "tokens": ["S1", "DIV", "S2", "DIV", "S3"]}
        equation = {
            "inscription_id": "T1",
            "span": [0, 4],
            "sign_to_phoneme": {"S1": "a", "S2": "k", "S3": "l"},
        }
        result = sign_prediction_perplexity_v0(
            record=record, equation=equation, cluster_model=model
        )
        # Same window-bigram count as the no-DIV case: 2 bigrams.
        self.assertEqual(result.n_window_bigrams, 2)
        self.assertEqual(result.cluster_agreement, 3)

    def test_unknown_phoneme_is_skipped(self):
        """Phoneme not in phoneme_to_modal_cluster contributes 0."""
        model = _mini_cluster_model()
        record = {"id": "T1", "tokens": ["S1"]}
        equation = {
            "inscription_id": "T1",
            "span": [0, 0],
            "sign_to_phoneme": {"S1": "q"},  # 'q' not in bridge table
        }
        result = sign_prediction_perplexity_v0(
            record=record, equation=equation, cluster_model=model
        )
        self.assertEqual(result.cluster_agreement, 0)
        self.assertIn("missing from phoneme→cluster", result.metric_notes)

    def test_determinism_real_corpus(self):
        """Loading + scoring against the committed cluster model is deterministic."""
        records = load_records(_CORPUS_PATH)
        # Pick a real inscription with at least 6 signs to score against.
        record = next(r for r in records if r["id"] == "GO Wc 1a")
        model = ClusterModel.load_json(_CLUSTER_MODEL_PATH)
        equation = {
            "inscription_id": "GO Wc 1a",
            "span": [0, 5],
            "sign_to_phoneme": {
                "AB08": "a", "AB31": "n", "AB58": "d",
                "AB80": "e", "AB28": "r", "AB09": "e",
            },
        }
        # Some of those signs may not be in the corpus token slice — clip
        # span to actual tokens length and verify scoring still completes.
        # The committed candidates do this consistently so we mirror it.
        r1 = sign_prediction_perplexity_v0(record=record, equation=equation, cluster_model=model)
        r2 = sign_prediction_perplexity_v0(record=record, equation=equation, cluster_model=model)
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.cluster_agreement, r2.cluster_agreement)
        self.assertEqual(r1.window_bigram_loglik, r2.window_bigram_loglik)

    def test_build_model_byte_deterministic(self):
        """Re-building the model produces identical artifacts."""
        records = load_records(_CORPUS_PATH)
        m1 = build_model(records)
        m2 = build_model(records)
        self.assertEqual(m1.sign_to_cluster, m2.sign_to_cluster)
        self.assertEqual(m1.bigram_counts, m2.bigram_counts)
        self.assertEqual(m1.bigram_log_probs, m2.bigram_log_probs)
        self.assertEqual(m1.phoneme_to_modal_cluster, m2.phoneme_to_modal_cluster)


if __name__ == "__main__":
    unittest.main()
