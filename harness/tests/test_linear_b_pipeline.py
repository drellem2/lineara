"""Smoke tests for the mg-4664 Linear-B / Mycenaean-Greek pipeline pieces.

Covers:

* `scripts/parse_liber.py` — the LiBER HTML → (name, transliteration,
  words) extractor. Logograms are dropped, hyphens stripped, single-
  character tokens dropped, broken syllabograms surfaced verbatim.
* `scripts/build_linear_b_carryover_pool.py` — promotion of the
  `hypotheses/curated/{anchor,v4_anchor}_*.yaml` anchors into a
  pool YAML; entries deduplicated by surface.
* `scripts/run_sweep._EXT_POOL_LANGUAGE` — the linear_b_carryover and
  control_linear_b_carryover pools dispatch to the
  ``mycenaean_greek`` LM (so the v8 / v10 pipeline routes them
  correctly).
* `scripts/per_surface_bayesian_rollup._DEFAULT_LANGUAGE_DISPATCH` —
  the same-LM filter recognizes the linear_b_carryover pools.
"""

from __future__ import annotations

import importlib.util
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


_PARSE_PATH = _REPO_ROOT / "scripts" / "parse_liber.py"
_RUN_SWEEP_PATH = _REPO_ROOT / "scripts" / "run_sweep.py"
_BAYES_PATH = _REPO_ROOT / "scripts" / "per_surface_bayesian_rollup.py"


class ParseLiberTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parse = _load_module("parse_liber", _PARSE_PATH)

    def _parse(self, html: str) -> tuple[str, str, list[str]]:
        return self.parse.parse_one(html)

    def test_basic_syllabogram_extraction(self) -> None:
        html = '<meta name="description" content="ARM Z 1, wi-na-jo" />'
        name, trans, words = self._parse(html)
        self.assertEqual(name, "ARM Z 1")
        self.assertEqual(trans, "wi-na-jo")
        self.assertEqual(words, ["winajo"])

    def test_logograms_dropped(self) -> None:
        # OVIS, M, P, ZE, $vest. should all be dropped — only lowercase
        # syllabogram clusters survive.
        html = (
            '<meta name="description" content="KN Da 1396, '
            '____________________ OVIS^m 100 ____ [ ku-ne-u / _ da-wo '
            '__________________ [" />'
        )
        name, _trans, words = self._parse(html)
        self.assertEqual(name, "KN Da 1396")
        self.assertEqual(words, ["kuneu", "dawo"])

    def test_short_words_dropped(self) -> None:
        # Single-letter "words" carry no bigram information and are
        # dropped; the multi-syllabogram cluster survives.
        html = '<meta name="description" content="SAMPLE 1, a / ku-ne-u" />'
        _name, _trans, words = self._parse(html)
        self.assertEqual(words, ["kuneu"])

    def test_broken_syllabogram_with_brackets(self) -> None:
        # The transliteration carries `]wo-ni-jo[` for partly-broken
        # tablets; the parser should still emit `wonijo`.
        html = '<meta name="description" content="KN Ag 322, ]wo-ni-jo[" />'
        _name, _trans, words = self._parse(html)
        self.assertEqual(words, ["wonijo"])

    def test_no_meta_description_returns_empty(self) -> None:
        name, trans, words = self._parse("<html><body>no meta</body></html>")
        self.assertEqual(name, "")
        self.assertEqual(trans, "")
        self.assertEqual(words, [])


class RunSweepLinearBDispatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # run_sweep.py imports the harness package eagerly. Loading it
        # via importlib.util triggers that import; make sure the repo
        # root is on sys.path first (already done at module scope).
        cls.run_sweep = _load_module("run_sweep", _RUN_SWEEP_PATH)

    def test_linear_b_carryover_routes_to_mycenaean_greek(self) -> None:
        d = self.run_sweep._EXT_POOL_LANGUAGE
        self.assertEqual(d["linear_b_carryover"], "mycenaean_greek")
        self.assertEqual(d["control_linear_b_carryover"], "mycenaean_greek")
        # Pre-existing dispatches are not perturbed.
        self.assertEqual(d["aquitanian"], "basque")
        self.assertEqual(d["control_aquitanian"], "basque")
        self.assertEqual(d["etruscan"], "etruscan")


class BayesianRollupLinearBDispatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_linear_b_carryover_in_substrate_pools(self) -> None:
        self.assertIn("linear_b_carryover", self.bayes._SUBSTRATE_POOLS)

    def test_default_language_dispatch_includes_linear_b_carryover(self) -> None:
        d = self.bayes._DEFAULT_LANGUAGE_DISPATCH
        self.assertEqual(d["linear_b_carryover"], "mycenaean_greek")
        self.assertEqual(d["control_linear_b_carryover"], "mycenaean_greek")


if __name__ == "__main__":
    unittest.main()
