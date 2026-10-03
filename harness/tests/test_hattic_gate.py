"""Tests for the pre-registered Hattic gate (mg-7b882).

Pins the pre-registered constants and the PASS rule so they cannot be
tuned after the run without a test failure.
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


class HatticGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = _load_module(
            "hattic_gate", _REPO_ROOT / "scripts" / "hattic_gate.py"
        )

    def test_preregistered_constants(self) -> None:
        self.assertEqual(self.gate._TOP_K_GATE, 20)
        self.assertEqual(self.gate._ALPHA, 0.05)
        self.assertEqual(self.gate._SUBSTRATE, "hattic")
        self.assertEqual(self.gate._CONTROL, "control_hattic_bigram")

    def test_pool_size_matches_yaml(self) -> None:
        text = (_REPO_ROOT / "pools" / "hattic.yaml").read_text(encoding="utf-8")
        self.assertEqual(text.count("surface:"), self.gate._N_POOL_ENTRIES)

    def test_gate_rule(self) -> None:
        v = self.gate.gate_verdict
        self.assertTrue(v(0.01, 0.9, 0.8))
        self.assertFalse(v(0.05, 0.9, 0.8))  # strict p < 0.05
        self.assertFalse(v(0.01, 0.8, 0.8))  # median must be strictly above
        self.assertFalse(v(float("nan"), 0.9, 0.8))

    def _rows(self, means: list[float]) -> list[dict]:
        return [
            {"surface": f"s{i}", "n": 10, "k": 5, "posterior_mean": m}
            for i, m in enumerate(means)
        ]

    def test_evaluate_separated_passes(self) -> None:
        sub = self._rows([0.9 + 0.001 * i for i in range(30)])
        ctrl = self._rows([0.5 + 0.001 * i for i in range(30)])
        ev = self.gate.evaluate(sub, ctrl)
        self.assertEqual(ev["n_substrate_top"], 20)
        self.assertEqual(ev["n_control_top"], 20)
        self.assertEqual(ev["gate"], "PASS")
        self.assertGreater(ev["median_gap"], 0)

    def test_evaluate_identical_fails(self) -> None:
        rows = self._rows([0.5 + 0.01 * i for i in range(30)])
        ev = self.gate.evaluate(rows, list(rows))
        self.assertEqual(ev["gate"], "FAIL")

    def test_fail_text_is_inconclusive_on_data_quality(self) -> None:
        rows = self._rows([0.5 + 0.01 * i for i in range(30)])
        for r in rows:
            r.update(pool_kind="hattic", credibility=1.0, effective_score=r["posterior_mean"])
        ev = self.gate.evaluate(rows, list(rows))
        text = self.gate.render(ev, rows, [])
        self.assertIn("inconclusive on data quality", text)
        self.assertIn("72", text)


if __name__ == "__main__":
    unittest.main()
