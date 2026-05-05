"""Smoke tests for chic-v4 cross-script correlation analysis (mg-c769).

Exercises:
  * The Spearman rank-correlation primitive handles average-rank ties.
  * The Pearson primitive is a closed-form correlation on small data.
  * The acceptance-gate row parser pulls (median_sub, median_ctrl,
    mw_p, gate) from each of the three column layouts the input
    rollups use (LA v10 8-col, v18/v21 9-col, chic-v3 11-col).
  * The top-20 side-by-side parser pulls 20 rows of (sub_surface,
    sub_p, ctrl_surface, ctrl_p) and stops there even when the
    section is followed by other tables.

These tests do not require the script to actually have been run end-
to-end on the committed rollups; they exercise the primitives on
synthetic markdown so the test stays valid after any future rollup
file evolves.
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


class ChicV4PrimitivesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load_module(
            "chic_v4_cross_script_correlation",
            _REPO_ROOT / "scripts" / "chic_v4_cross_script_correlation.py",
        )

    # ---------- Spearman ----------

    def test_spearman_perfect_positive(self) -> None:
        rho = self.mod._spearman_with_ties([1.0, 2.0, 3.0, 4.0], [10.0, 20.0, 30.0, 40.0])
        self.assertAlmostEqual(rho, 1.0, places=10)

    def test_spearman_perfect_negative(self) -> None:
        rho = self.mod._spearman_with_ties([1.0, 2.0, 3.0, 4.0], [40.0, 30.0, 20.0, 10.0])
        self.assertAlmostEqual(rho, -1.0, places=10)

    def test_spearman_handles_ties_in_x(self) -> None:
        # Two pairs tied in x; should not blow up to nan as long as y
        # has variance.
        rho = self.mod._spearman_with_ties([1.0, 1.0, 2.0, 3.0], [10.0, 20.0, 30.0, 40.0])
        self.assertFalse(math.isnan(rho))
        self.assertGreater(rho, 0.5)

    def test_spearman_zero_variance_returns_nan(self) -> None:
        rho = self.mod._spearman_with_ties([1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0])
        self.assertTrue(math.isnan(rho))

    # ---------- Pearson ----------

    def test_pearson_perfect_positive(self) -> None:
        r = self.mod._pearson([1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.0])
        self.assertAlmostEqual(r, 1.0, places=10)

    def test_pearson_perfect_negative(self) -> None:
        r = self.mod._pearson([1.0, 2.0, 3.0, 4.0], [8.0, 6.0, 4.0, 2.0])
        self.assertAlmostEqual(r, -1.0, places=10)

    def test_pearson_zero_for_uncorrelated_balanced(self) -> None:
        r = self.mod._pearson([-1.0, 1.0, -1.0, 1.0], [-1.0, -1.0, 1.0, 1.0])
        self.assertAlmostEqual(r, 0.0, places=10)

    # ---------- gate-row parser ----------

    def test_parse_gate_row_la_v10_8col(self) -> None:
        text = (
            "## Pool acceptance gate\n"
            "\n"
            "| pool | n_substrate_top | n_control_top | median(top substrate posterior) | "
            "median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |\n"
            "|:--|---:|---:|---:|---:|---:|---:|:--:|\n"
            "| aquitanian | 20 | 20 | 0.9808 | 0.9512 | 345.0 | 0.0000 | PASS |\n"
        )
        sub, ctrl, p, gate = self.mod._parse_gate_row(text)
        self.assertAlmostEqual(sub, 0.9808, places=4)
        self.assertAlmostEqual(ctrl, 0.9512, places=4)
        self.assertAlmostEqual(p, 0.0, places=4)
        self.assertEqual(gate, "PASS")

    def test_parse_gate_row_v18_takes_first_pass_row(self) -> None:
        # v18 toponym rollup carries two gate rows (bigram PASS, unigram
        # FAIL). The parser should return the bigram row.
        text = (
            "## Acceptance gate (v18 vs v10)\n"
            "\n"
            "| variant | substrate top-K | control top-K | median(top substrate posterior) "
            "| median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |\n"
            "|:--|---:|---:|---:|---:|---:|---:|:--:|\n"
            "| bigram (v18) | 20 | 20 | 0.9615 | 0.8525 | 337.5 | 9.988e-05 | PASS |\n"
            "| unigram (v6/v10) | 20 | 20 | 0.9186 | 0.9464 | 149.5 | 9.165e-01 | FAIL |\n"
        )
        sub, ctrl, p, gate = self.mod._parse_gate_row(text)
        self.assertAlmostEqual(sub, 0.9615, places=4)
        self.assertAlmostEqual(ctrl, 0.8525, places=4)
        self.assertEqual(gate, "PASS")

    def test_parse_gate_row_v21_9col(self) -> None:
        text = (
            "## Acceptance gate\n"
            "\n"
            "| substrate pool | control pool | substrate top-K | control top-K | "
            "median(top substrate posterior) | median(top control posterior) | "
            "MW U (substrate) | MW p (one-tail, substrate>control) | gate |\n"
            "|:--|:--|---:|---:|---:|---:|---:|---:|:--:|\n"
            "| eteocretan | control_eteocretan_bigram | 20 | 20 | 0.9712 | 0.7697 | 364.0 | 4.096e-06 | PASS |\n"
        )
        sub, ctrl, p, gate = self.mod._parse_gate_row(text)
        self.assertAlmostEqual(sub, 0.9712, places=4)
        self.assertAlmostEqual(ctrl, 0.7697, places=4)
        self.assertAlmostEqual(p, 4.096e-06, places=10)
        self.assertEqual(gate, "PASS")

    def test_parse_gate_row_chic_v3_11col(self) -> None:
        text = (
            "## Acceptance gate\n"
            "\n"
            "| substrate pool | control pool | LM | n paired windows | substrate top-K | "
            "control top-K | median(top substrate posterior) | median(top control posterior) | "
            "MW U (substrate) | MW p (one-tail) | gate |\n"
            "|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|\n"
            "| aquitanian | control_aquitanian | basque | 5746 | 20 | 20 | 0.8739 | 0.9106 | 144.0 | 9.369e-01 | FAIL |\n"
        )
        sub, ctrl, p, gate = self.mod._parse_gate_row(text)
        self.assertAlmostEqual(sub, 0.8739, places=4)
        self.assertAlmostEqual(ctrl, 0.9106, places=4)
        self.assertAlmostEqual(p, 9.369e-01, places=6)
        self.assertEqual(gate, "FAIL")

    # ---------- top-20 parser ----------

    def test_parse_top20_table_returns_20_rows(self) -> None:
        rows = ["## eteocretan — top-20 substrate vs top-20 control side-by-side (gate input)", ""]
        rows.append(
            "| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |"
        )
        rows.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
        for i in range(20):
            sub_p = 0.99 - 0.01 * i
            ctrl_p = 0.95 - 0.01 * i
            rows.append(
                f"| {i+1} | `sub{i}` | 50 | 50 | {sub_p:.4f} | `ctrl{i}` | 50 | 50 | {ctrl_p:.4f} |"
            )
        rows.append("")
        rows.append("## next section")
        rows.append("| anything else |")
        text = "\n".join(rows) + "\n"
        out = self.mod._parse_top20_table(text)
        self.assertEqual(len(out), 20)
        self.assertEqual(out[0][0], "sub0")
        self.assertEqual(out[0][2], "ctrl0")
        self.assertAlmostEqual(out[0][1], 0.99, places=4)
        self.assertAlmostEqual(out[19][3], 0.95 - 0.01 * 19, places=4)


class ChicV4PoolsTest(unittest.TestCase):
    """Sanity-check the canonical pool ordering matches the brief."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load_module(
            "chic_v4_cross_script_correlation",
            _REPO_ROOT / "scripts" / "chic_v4_cross_script_correlation.py",
        )

    def test_pool_order_is_la_relatedness_ordering(self) -> None:
        # Linear A monotonic-with-relatedness ordering established in
        # v10 / v18 / v21: eteocretan (closest) > toponym > etruscan >
        # aquitanian (most distant).
        self.assertEqual(
            self.mod._POOLS, ("eteocretan", "toponym", "etruscan", "aquitanian")
        )

    def test_la_path_set_covers_4_pools(self) -> None:
        self.assertEqual(set(self.mod._LA_PATHS.keys()), set(self.mod._POOLS))

    def test_chic_path_set_covers_4_pools(self) -> None:
        self.assertEqual(set(self.mod._CHIC_PATHS.keys()), set(self.mod._POOLS))

    def test_la_toponym_path_is_v18_bigram_control_rollup(self) -> None:
        # v18 (mg-9f18) is the rollup that holds the toponym-pool gate
        # PASS; the v6/v10 unigram-control rollup is FAIL and not the
        # methodology-paper-canonical toponym rollup.
        self.assertTrue(
            self.mod._LA_PATHS["toponym"].name
            == "rollup.bayesian_posterior.toponym_bigram_control.md"
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
