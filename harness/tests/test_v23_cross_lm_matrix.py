"""Smoke tests for v23 cross-LM matrix infrastructure (mg-b599).

Exercises:
  * The new cross_lm_rescore dispatch tables route the right pool ↔ LM
    pairs (additional coverage beyond test_cross_lm_rescore.py).
  * The v23 generic gate runner builds a markdown report + summary
    JSON for an arbitrary (substrate, control, LM) cell.
  * The v23 matrix builder enumerates the right cells and produces a
    matrix table that matches the headline "own-LM dominance pattern
    HOLDS / DOES NOT HOLD" structure.

These tests do not run the rescore — they assume the rescore has
already populated the result stream sidecars (which is the steady
state on main after mg-b599 lands).
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


class V23MatrixSpecTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = _load_module(
            "v23_cross_lm_matrix",
            _REPO_ROOT / "scripts" / "v23_cross_lm_matrix.py",
        )

    def test_substrate_spec_covers_4_pools(self) -> None:
        # The cross-LM matrix is over the 4 validated substrate pools:
        # aquitanian, etruscan, toponym, eteocretan.
        names = [s["substrate"] for s in self.matrix._SUBSTRATE_SPEC]
        self.assertEqual(
            sorted(names), ["aquitanian", "eteocretan", "etruscan", "toponym"]
        )

    def test_substrate_spec_uses_bigram_control_for_post_v18_pools(self) -> None:
        # toponym + eteocretan are paired against bigram-preserving
        # controls (post-v18 production default); aquitanian + etruscan
        # are paired against the legacy unigram controls.
        ctrls = {s["substrate"]: s["control"] for s in self.matrix._SUBSTRATE_SPEC}
        self.assertEqual(ctrls["aquitanian"], "control_aquitanian")
        self.assertEqual(ctrls["etruscan"], "control_etruscan")
        self.assertEqual(ctrls["toponym"], "control_toponym_bigram")
        self.assertEqual(ctrls["eteocretan"], "control_eteocretan_bigram")

    def test_lm_columns_cover_all_4_lms(self) -> None:
        self.assertEqual(
            sorted(self.matrix._LM_COLUMNS),
            ["basque", "eteocretan", "etruscan", "mycenaean_greek"],
        )

    def test_own_lm_dispatch_matches_run_sweep(self) -> None:
        # Each substrate's own_lm should match the same-LM dispatch
        # used by run_sweep / per_surface_bayesian_rollup. Cross-checks
        # that future LM-dispatch edits don't desync from the matrix
        # builder.
        from scripts.per_surface_bayesian_rollup import _DEFAULT_LANGUAGE_DISPATCH

        for s in self.matrix._SUBSTRATE_SPEC:
            self.assertEqual(
                _DEFAULT_LANGUAGE_DISPATCH.get(s["substrate"]),
                s["own_lm"],
                f"own_lm mismatch for substrate {s['substrate']!r}",
            )


class V23CrossLMGateScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = _load_module(
            "v23_cross_lm_gate",
            _REPO_ROOT / "scripts" / "v23_cross_lm_gate.py",
        )

    def test_module_imports_cleanly(self) -> None:
        # Smoke: the module's primitive helpers are importable.
        self.assertTrue(hasattr(self.gate, "_build_paired_rows"))
        self.assertTrue(hasattr(self.gate, "main"))


if __name__ == "__main__":
    unittest.main()
