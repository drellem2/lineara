"""Smoke tests for external_phoneme_perplexity_v0 (mg-ee18, harness v8).

Two layers of coverage:

1. ``ExternalLMSmoke`` builds a tiny synthetic char-bigram model in
   memory and asserts the run-extraction + per-char-loglik formula
   agrees with a hand calculation. No reliance on the committed Basque /
   Etruscan models — the metric is exercised purely through its
   contract.
2. ``CommittedModelsSmoke`` loads the two committed external models and
   asserts they (a) load without errors, (b) have the documented
   vocabulary + α, (c) produce a deterministic non-zero score on a
   small Linear-A token stream with a representative partial mapping.
"""

from __future__ import annotations

import math
import unittest
from pathlib import Path

from harness.external_phoneme_model import (
    ExternalPhonemeModel,
    VOCAB,
    VOCAB_INDEX,
    WORD_BOUNDARY,
    build_model,
    char_decompose_phonemes,
    tokenize_text,
    tokenize_word_list,
)
from harness.metrics import external_phoneme_perplexity_v0


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_BASQUE_MODEL = _REPO_ROOT / "harness" / "external_phoneme_models" / "basque.json"
_ETRUSCAN_MODEL = (
    _REPO_ROOT / "harness" / "external_phoneme_models" / "etruscan.json"
)


def _mini_model() -> ExternalPhonemeModel:
    """3-token char-bigram model over only ``a``, ``b``, ``<W>``.

    Counts:
      <W> -> a : 4
      <W> -> b : 1
      a   -> <W>: 3
      a   -> a : 1
      a   -> b : 1
      b   -> a : 1
      b   -> <W>: 1
    Tokens: <W> a a b a <W> <W> a <W> <W> b a <W>  (built deterministically).
    """
    tokens = ["<W>", "a", "a", "b", "a", "<W>", "<W>", "a", "<W>", "<W>", "b", "a", "<W>"]
    return build_model(name="mini", tokens=tokens, alpha=1.0)


class ExternalLMSmoke(unittest.TestCase):

    def test_log_prob_normalization(self):
        """Each row of the smoothed table sums to 1 in raw probability."""
        model = _mini_model()
        for i in range(len(model.bigram_log_probs)):
            row_total = sum(math.exp(lp) for lp in model.bigram_log_probs[i])
            self.assertAlmostEqual(row_total, 1.0, places=6)

    def test_run_extraction_and_score(self):
        """One mapped run between two unmapped tokens; score = avg per-char loglik."""
        model = _mini_model()
        # Stream: A0 (mapped→a), A1 (mapped→ba), A2 (unmapped), A3 (mapped→a)
        # Run 1: "a", "ba"  (chars: a, b, a)
        # Run 2: "a"        (chars: a)
        stream = ["A0", "A1", "A2", "A3"]
        mapping = {"A0": "a", "A1": "ba", "A3": "a"}
        result = external_phoneme_perplexity_v0(
            stream=stream, mapping=mapping, language_model=model
        )
        # Run 1 chars: a, b, a → bracketed seq <W> a b a <W> → 4 bigrams
        # Run 2 chars: a → bracketed seq <W> a <W> → 2 bigrams
        # Hand-compute total loglik:
        log_probs = model.bigram_log_probs
        i = VOCAB_INDEX
        expected = (
            log_probs[i["<W>"]][i["a"]]
            + log_probs[i["a"]][i["b"]]
            + log_probs[i["b"]][i["a"]]
            + log_probs[i["a"]][i["<W>"]]
            + log_probs[i["<W>"]][i["a"]]
            + log_probs[i["a"]][i["<W>"]]
        )
        self.assertEqual(result.n_runs, 2)
        self.assertEqual(result.n_phonemes_scored, 3)  # "a", "ba", "a"
        self.assertEqual(result.n_chars_scored, 4)     # a, b, a, a
        self.assertAlmostEqual(result.total_loglik, expected, places=6)
        self.assertAlmostEqual(result.score, expected / 4, places=6)
        self.assertEqual(result.language, "mini")

    def test_div_breaks_run(self):
        """DIV between mapped tokens splits the run into two."""
        model = _mini_model()
        stream = ["A0", "DIV", "A1"]
        mapping = {"A0": "a", "A1": "a"}
        result = external_phoneme_perplexity_v0(
            stream=stream, mapping=mapping, language_model=model
        )
        # DIV is not in mapping → end-of-run between A0 and A1.
        self.assertEqual(result.n_runs, 2)
        self.assertEqual(result.n_chars_scored, 2)

    def test_empty_mapping_yields_no_runs(self):
        model = _mini_model()
        stream = ["A0", "A1", "A2"]
        result = external_phoneme_perplexity_v0(
            stream=stream, mapping={}, language_model=model
        )
        self.assertEqual(result.n_runs, 0)
        self.assertEqual(result.n_chars_scored, 0)
        self.assertEqual(result.score, 0.0)

    def test_tokenize_text_inserts_boundaries(self):
        tokens = tokenize_text("ab cd")
        self.assertEqual(tokens, ["<W>", "a", "b", "<W>", "<W>", "c", "d", "<W>"])

    def test_tokenize_word_list_wraps_each(self):
        tokens = tokenize_word_list(["ab", "c"])
        self.assertEqual(tokens, ["<W>", "a", "b", "<W>", "<W>", "c", "<W>"])

    def test_char_decompose_multichar_phonemes(self):
        self.assertEqual(
            char_decompose_phonemes(["a", "th", "e"]), ["a", "t", "h", "e"]
        )

    def test_oov_char_folds_to_boundary(self):
        """A non-vocab char in the candidate's phoneme stream folds to <W>.

        This keeps the metric total even if a future pool sneaks a
        non-a-z phoneme through validation. The folding should not
        crash; the resulting bigram lookup falls back to <W>'s row."""
        model = _mini_model()
        stream = ["A0"]
        mapping = {"A0": "ñ"}  # fold to <W>
        result = external_phoneme_perplexity_v0(
            stream=stream, mapping=mapping, language_model=model
        )
        # One run, char-decomposes to one <W> char, scored as <W>→<W>→<W>
        # which is 2 bigrams (start-boundary, end-boundary).
        self.assertEqual(result.n_runs, 1)
        self.assertEqual(result.n_phonemes_scored, 1)


class CommittedModelsSmoke(unittest.TestCase):

    def test_load_basque(self):
        model = ExternalPhonemeModel.load_json(_BASQUE_MODEL)
        self.assertEqual(model.name, "basque")
        self.assertAlmostEqual(model.alpha, 0.1)
        self.assertEqual(tuple(VOCAB), VOCAB)
        self.assertEqual(len(model.bigram_log_probs), len(VOCAB))

    def test_load_etruscan(self):
        model = ExternalPhonemeModel.load_json(_ETRUSCAN_MODEL)
        self.assertEqual(model.name, "etruscan")
        self.assertAlmostEqual(model.alpha, 1.0)
        self.assertEqual(len(model.bigram_log_probs), len(VOCAB))

    def test_score_under_basque_is_deterministic(self):
        model = ExternalPhonemeModel.load_json(_BASQUE_MODEL)
        # Tiny synthetic Linear-A stream with a partial mapping.
        stream = ["AB08", "AB28", "AB59", "DIV", "AB80", "AB60"]
        mapping = {"AB08": "a", "AB28": "n", "AB80": "d", "AB60": "e"}
        r1 = external_phoneme_perplexity_v0(
            stream=stream, mapping=mapping, language_model=model
        )
        r2 = external_phoneme_perplexity_v0(
            stream=stream, mapping=mapping, language_model=model
        )
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.total_loglik, r2.total_loglik)
        self.assertEqual(r1.language, "basque")

    def test_basque_prefers_basque_like_streams(self):
        """A Basque-like phoneme stream should score better under the Basque
        model than a phonotactically-unfriendly random one."""
        model = ExternalPhonemeModel.load_json(_BASQUE_MODEL)
        # Map AB ids to a sequence that resembles a real Basque word
        # ("andere") versus a sequence that is intentionally cluster-heavy
        # and Basque-unfriendly ("xzqxbk").
        basque_stream = ["X1", "X2", "X3", "X4", "X5", "X6"]
        basque_map = {"X1": "a", "X2": "n", "X3": "d", "X4": "e", "X5": "r", "X6": "e"}
        bad_map = {"X1": "x", "X2": "z", "X3": "q", "X4": "x", "X5": "b", "X6": "k"}
        good = external_phoneme_perplexity_v0(
            stream=basque_stream, mapping=basque_map, language_model=model
        )
        bad = external_phoneme_perplexity_v0(
            stream=basque_stream, mapping=bad_map, language_model=model
        )
        self.assertGreater(good.score, bad.score)


if __name__ == "__main__":
    unittest.main()
