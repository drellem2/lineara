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

    def test_pool_size_is_the_v32_registration(self) -> None:
        # The gate was pre-registered and run against the v32 pool of 72
        # hand-keyed forms. mg-7f4db rebuilt pools/hattic.yaml from
        # published editions (124 entries), so the registered constant no
        # longer matches the YAML. It stays pinned as the v32 record; a
        # re-run on the rebuilt pool needs its own pre-registration.
        self.assertEqual(self.gate._N_POOL_ENTRIES, 72)
        text = (_REPO_ROOT / "pools" / "hattic.yaml").read_text(encoding="utf-8")
        self.assertEqual(text.count("surface:"), 124)

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


class PoolLoaderSkipsNonPoolYamlTest(unittest.TestCase):
    """pools/ also holds CHIC sign / anchor YAMLs with no ``pool`` key;
    the run_sweep registry and the rollup loader must skip them rather
    than KeyError (mg-7b882)."""

    def test_real_pools_dir_loads(self) -> None:
        rollup = _load_module(
            "per_surface_bayesian_rollup",
            _REPO_ROOT / "scripts" / "per_surface_bayesian_rollup.py",
        )
        sweep = _load_module("run_sweep", _REPO_ROOT / "scripts" / "run_sweep.py")
        pools_dir = _REPO_ROOT / "pools"
        # Positive control: at least one YAML in pools/ lacks a pool key.
        missing = [
            p for p in pools_dir.glob("*.yaml")
            if not any(l.startswith("pool:") for l in p.read_text(encoding="utf-8").splitlines())
        ]
        self.assertTrue(missing)
        phonemes = rollup._load_pool_phonemes(pools_dir)
        self.assertIn("hattic", phonemes)
        n_yaml = (pools_dir / "hattic.yaml").read_text(encoding="utf-8").count("surface:")
        self.assertEqual(len(phonemes["hattic"]), n_yaml)
        registry = sweep.build_pool_registry(pools_dir)
        self.assertIn("control_hattic_bigram", registry)


if __name__ == "__main__":
    unittest.main()
