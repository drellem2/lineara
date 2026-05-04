"""Smoke tests for scripts/per_surface_bayesian_rollup.py (mg-d26d).

Exercises:
  * Beta posterior mean = (1+k)/(2+n) and 95% CI lies within (0, 1)
    and contains the posterior mean for a hand-built minimal dataset.
  * The posterior aggregation correctly deduplicates a surface that
    appears multiple times in a single multi-root signature.
  * The control side flips the binary observation: a record with
    paired_diff > 0 is a substrate success and a control failure on
    that record's control surface(s).
  * Mann-Whitney U one-tail p < 0.05 on a hand-built right-tail
    where substrate posteriors strictly dominate control posteriors.
  * Determinism: identical posterior + p-values across two runs of
    ``aggregate_per_surface`` + ``build_posterior_rows`` on the same
    records.
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


_BAYES_PATH = _REPO_ROOT / "scripts" / "per_surface_bayesian_rollup.py"


def _record(*, kind, pool, sub, ctrl, paired_diff, sub_hash="s", ctrl_hash="c"):
    return {
        "kind": kind,
        "pool": pool,
        "control_pool": f"control_{pool}",
        "substrate_surfaces": tuple(sub),
        "control_surfaces": tuple(ctrl),
        "substrate_score": float(paired_diff),
        "control_score": 0.0,
        "paired_diff": float(paired_diff),
        "substrate_hash": sub_hash,
        "control_hash": ctrl_hash,
    }


class BetaPosteriorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_posterior_mean_formula(self) -> None:
        # n=10, k=7 → mean = (1+7)/(2+10) = 8/12 = 2/3
        mean, lo, hi = self.bayes.beta_posterior(10, 7)
        self.assertAlmostEqual(mean, 8.0 / 12.0, places=12)
        self.assertGreater(mean, lo)
        self.assertLess(mean, hi)
        self.assertGreater(lo, 0.0)
        self.assertLess(hi, 1.0)

    def test_posterior_for_zero_records_is_uniform_prior(self) -> None:
        # n=0, k=0 → Beta(1,1) = Uniform(0,1); mean = 0.5; CI ≈ [0.025, 0.975]
        mean, lo, hi = self.bayes.beta_posterior(0, 0)
        self.assertAlmostEqual(mean, 0.5, places=12)
        self.assertAlmostEqual(lo, 0.025, places=2)
        self.assertAlmostEqual(hi, 0.975, places=2)

    def test_posterior_concentrates_with_n(self) -> None:
        # k/n = 0.8 in both, but n=100 has a tighter CI than n=10.
        _m1, lo1, hi1 = self.bayes.beta_posterior(10, 8)
        _m2, lo2, hi2 = self.bayes.beta_posterior(100, 80)
        self.assertGreater(hi1 - lo1, hi2 - lo2)


class AggregationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_signature_with_repeated_surface_counts_once(self) -> None:
        # A v9 signature with surfaces ("ur","ur","ur") on one window
        # contributes a single observation under "ur".
        records = [
            _record(kind="v9", pool="aquitanian",
                    sub=("ur", "ur", "ur"), ctrl=("an",), paired_diff=+1.0),
        ]
        agg = self.bayes.aggregate_per_surface(records)
        ur = agg[("aquitanian", "ur")]
        self.assertEqual(ur["n"], 1)
        self.assertEqual(ur["k"], 1)
        self.assertEqual(ur["n_v9"], 1)
        self.assertEqual(ur["n_v8"], 0)

    def test_control_side_flips_observation(self) -> None:
        # paired_diff > 0 → substrate success; control surface gets a
        # failure. paired_diff < 0 → reverse.
        records = [
            _record(kind="v8", pool="aquitanian",
                    sub=("itsaso",), ctrl=("xxx",), paired_diff=+0.5),
            _record(kind="v8", pool="aquitanian",
                    sub=("itsaso",), ctrl=("yyy",), paired_diff=-0.5),
        ]
        agg = self.bayes.aggregate_per_surface(records)
        sub_cell = agg[("aquitanian", "itsaso")]
        self.assertEqual(sub_cell["n"], 2)
        self.assertEqual(sub_cell["k"], 1)  # only paired_diff>0 counts
        ctrl_xxx = agg[("control_aquitanian", "xxx")]
        self.assertEqual(ctrl_xxx["n"], 1)
        self.assertEqual(ctrl_xxx["k"], 0)  # control LOST the +0.5 record
        ctrl_yyy = agg[("control_aquitanian", "yyy")]
        self.assertEqual(ctrl_yyy["n"], 1)
        self.assertEqual(ctrl_yyy["k"], 1)  # control WON the -0.5 record

    def test_paired_diff_zero_is_failure_for_both_sides(self) -> None:
        records = [
            _record(kind="v8", pool="aquitanian",
                    sub=("a",), ctrl=("b",), paired_diff=0.0),
        ]
        agg = self.bayes.aggregate_per_surface(records)
        self.assertEqual(agg[("aquitanian", "a")]["k"], 0)
        self.assertEqual(agg[("control_aquitanian", "b")]["k"], 0)

    def test_v8_and_v9_sources_are_summed(self) -> None:
        # Same surface S appears in both a v8 and a v9 record; both
        # contribute to its (n, k), with separate v8/v9 split tallies.
        records = [
            _record(kind="v8", pool="aquitanian",
                    sub=("itsaso",), ctrl=("c1",), paired_diff=+1.0),
            _record(kind="v9", pool="aquitanian",
                    sub=("itsaso", "lur"), ctrl=("c2", "c3"), paired_diff=+1.0),
            _record(kind="v9", pool="aquitanian",
                    sub=("itsaso",), ctrl=("c4",), paired_diff=-1.0),
        ]
        agg = self.bayes.aggregate_per_surface(records)
        cell = agg[("aquitanian", "itsaso")]
        self.assertEqual(cell["n"], 3)
        self.assertEqual(cell["k"], 2)
        self.assertEqual(cell["n_v8"], 1)
        self.assertEqual(cell["k_v8"], 1)
        self.assertEqual(cell["n_v9"], 2)
        self.assertEqual(cell["k_v9"], 1)


class CredibilityShrinkageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_small_n_surface_gets_shrunk_below_high_n_surface(self) -> None:
        # Surface A: 1 record, +1 → posterior mean = 2/3 ≈ 0.667;
        #   credibility = 1/10 = 0.1; effective = 0.1 * 0.667 + 0.9 * 0.5 ≈ 0.517.
        # Surface B: 50 records, 49 wins → posterior mean ≈ 0.962;
        #   credibility = 1.0; effective = 0.962.
        # B should rank above A.
        records = [
            _record(kind="v8", pool="aquitanian",
                    sub=("a",), ctrl=("ctrl_a",), paired_diff=+1.0,
                    sub_hash="A1", ctrl_hash="cA1"),
        ]
        records += [
            _record(kind="v8", pool="aquitanian",
                    sub=("b",), ctrl=("ctrl_b",), paired_diff=+1.0,
                    sub_hash=f"B{i}", ctrl_hash=f"cB{i}")
            for i in range(49)
        ]
        records += [
            _record(kind="v8", pool="aquitanian",
                    sub=("b",), ctrl=("ctrl_b",), paired_diff=-1.0,
                    sub_hash="Bneg", ctrl_hash="cBneg"),
        ]
        agg = self.bayes.aggregate_per_surface(records)
        rows = self.bayes.build_posterior_rows(agg, n_min=10)
        by_surf = {(r["pool_kind"], r["surface"]): r for r in rows}
        a = by_surf[("aquitanian", "a")]
        b = by_surf[("aquitanian", "b")]
        self.assertEqual(a["n"], 1)
        self.assertAlmostEqual(a["credibility"], 0.1, places=12)
        self.assertEqual(b["n"], 50)
        self.assertEqual(b["credibility"], 1.0)
        self.assertGreater(b["effective_score"], a["effective_score"])
        # Raw posterior of A would put it ahead of an n=10 50/50 surface;
        # shrinkage moves A behind any high-credibility surface near 0.5.
        self.assertLess(a["effective_score"], 0.6)
        self.assertGreater(b["effective_score"], 0.9)


class MannWhitneyGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_strict_dominance_passes_gate(self) -> None:
        # Substrate posteriors strictly dominate control posteriors;
        # one-tail MW p must be very small.
        a = [0.95, 0.94, 0.93, 0.92, 0.91]
        b = [0.85, 0.84, 0.83, 0.82, 0.81]
        u, p, na, nb = self.bayes.mann_whitney_u_one_tail(a, b)
        self.assertEqual(na, 5)
        self.assertEqual(nb, 5)
        self.assertEqual(u, 25.0)  # all 5*5 pairs favor a
        self.assertLess(p, 0.05)

    def test_no_dominance_fails_gate(self) -> None:
        # Identical right-tail distributions — p ≈ 0.5.
        a = [0.95, 0.94, 0.93]
        b = [0.95, 0.94, 0.93]
        u, p, na, nb = self.bayes.mann_whitney_u_one_tail(a, b)
        self.assertGreater(p, 0.4)
        self.assertEqual(na, 3)
        self.assertEqual(nb, 3)


class DeterminismTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bayes = _load_module("per_surface_bayesian_rollup", _BAYES_PATH)

    def test_idempotent_aggregation_and_posteriors(self) -> None:
        records = [
            _record(kind="v8", pool="aquitanian",
                    sub=("itsaso",), ctrl=("xxx",), paired_diff=+0.5),
            _record(kind="v9", pool="aquitanian",
                    sub=("itsaso", "lur"), ctrl=("yyy", "zzz"), paired_diff=-0.3),
            _record(kind="v9", pool="aquitanian",
                    sub=("ur",), ctrl=("aa",), paired_diff=+0.1),
        ]
        agg1 = self.bayes.aggregate_per_surface(records)
        agg2 = self.bayes.aggregate_per_surface(records)
        rows1 = self.bayes.build_posterior_rows(agg1, n_min=5)
        rows2 = self.bayes.build_posterior_rows(agg2, n_min=5)
        self.assertEqual(len(rows1), len(rows2))
        for r1, r2 in zip(rows1, rows2):
            self.assertEqual(r1["surface"], r2["surface"])
            self.assertEqual(r1["pool_kind"], r2["pool_kind"])
            self.assertEqual(r1["n"], r2["n"])
            self.assertEqual(r1["k"], r2["k"])
            self.assertEqual(r1["posterior_mean"], r2["posterior_mean"])
            self.assertEqual(r1["posterior_ci_low"], r2["posterior_ci_low"])
            self.assertEqual(r1["posterior_ci_high"], r2["posterior_ci_high"])
            self.assertEqual(r1["effective_score"], r2["effective_score"])


if __name__ == "__main__":
    unittest.main()
