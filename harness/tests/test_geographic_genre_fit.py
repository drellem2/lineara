"""Smoke test for the ``geographic_genre_fit_v1`` metric.

Asserts:
  * Score is in [0, 1] for in-table inputs.
  * Score is alpha-weighted: setting alpha=0 returns pure semantic
    compat; alpha=1 returns pure region compat.
  * Missing fields fall back to neutral 0.5.
  * Pre-Greek toponym → Crete site scores higher than Aquitanian → Crete
    site (per the brief: pre-Greek substrate is the strongest case for
    Aegean Linear-A sites).
  * The metric is deterministic and pure.

Run directly:
  python3 -m harness.tests.test_geographic_genre_fit
"""

from __future__ import annotations

import unittest

from harness.metrics import geographic_genre_fit_v1


class GeographicGenreFitTest(unittest.TestCase):
    def test_score_in_unit_interval(self) -> None:
        result = geographic_genre_fit_v1(
            region="aquitania",
            semantic_field="agriculture",
            site="Haghia Triada",
            genre_hint="accountancy",
        )
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)

    def test_alpha_extremes(self) -> None:
        kw = {
            "region": "pre_greek",
            "semantic_field": "place",
            "site": "Knossos",
            "genre_hint": "accountancy",
        }
        full_region = geographic_genre_fit_v1(**kw, alpha=1.0)
        full_semantic = geographic_genre_fit_v1(**kw, alpha=0.0)
        # alpha=1 → score == region_compat
        self.assertAlmostEqual(full_region.score, full_region.region_compat)
        # alpha=0 → score == semantic_compat
        self.assertAlmostEqual(full_semantic.score, full_semantic.semantic_compat)

    def test_missing_field_falls_back_to_neutral(self) -> None:
        # Both region and semantic_field missing → 0.5 on each side, score=0.5.
        result = geographic_genre_fit_v1(
            region=None,
            semantic_field=None,
            site="Haghia Triada",
            genre_hint="accountancy",
        )
        self.assertEqual(result.region_compat, 0.5)
        self.assertEqual(result.semantic_compat, 0.5)
        self.assertAlmostEqual(result.score, 0.5)

    def test_pregreek_beats_aquitanian_on_crete(self) -> None:
        # Brief: pre-Greek toponym → Crete = 1.0; Aquitanian → Crete = 0.25.
        # With matching semantic fields, the pre-Greek score must exceed
        # the Aquitanian score on a Cretan site.
        pre_greek = geographic_genre_fit_v1(
            region="pre_greek",
            semantic_field="place",
            site="Haghia Triada",
            genre_hint="accountancy",
        )
        aquit = geographic_genre_fit_v1(
            region="aquitania",
            semantic_field="place",
            site="Haghia Triada",
            genre_hint="accountancy",
        )
        self.assertGreater(pre_greek.score, aquit.score)

    def test_unmapped_pair_falls_back_to_neutral(self) -> None:
        # "weaponry" + "votive_or_inscription" is in the table; "weaponry"
        # + an unknown genre is not. The latter must use the 0.5 fallback.
        unmapped = geographic_genre_fit_v1(
            region="aquitania",
            semantic_field="weaponry",
            site="Haghia Triada",
            genre_hint="never_seen_genre",
        )
        self.assertEqual(unmapped.semantic_compat, 0.5)

    def test_metric_is_deterministic(self) -> None:
        kw = {
            "region": "aquitania",
            "semantic_field": "kin",
            "site": "Khania",
            "genre_hint": "accountancy",
        }
        r1 = geographic_genre_fit_v1(**kw)
        r2 = geographic_genre_fit_v1(**kw)
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.region_compat, r2.region_compat)
        self.assertEqual(r1.semantic_compat, r2.semantic_compat)
        self.assertEqual(r1.metric_notes, r2.metric_notes)

    def test_default_alpha_is_0_4(self) -> None:
        # Brief: alpha defaults to 0.4 ("subject matter ... carries more weight").
        # 0.4 * 1.0 + 0.6 * 0.75 = 0.4 + 0.45 = 0.85
        result = geographic_genre_fit_v1(
            region="pre_greek",
            semantic_field="agriculture",
            site="Haghia Triada",
            genre_hint="accountancy",
        )
        self.assertAlmostEqual(result.score, 0.4 * 1.0 + 0.6 * 0.75, places=6)


if __name__ == "__main__":
    unittest.main()
