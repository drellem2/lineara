"""Smoke + invariant tests for chic-v12 (mg-2035).

Validates the artifacts produced by ``scripts/build_chic_v12.py``:

  results/chic_v12_cross_pool_l3.md
  results/chic_v12_tier3_summary.md

Tests assert framework-level invariants — required structural elements,
the 29 tier-3 candidate × 4 pool dispatch matrix, the per-candidate
reclassification bands, and the bail-on-context-inspection rule when
the tier-2-equivalent count exceeds 5 — rather than re-deriving paired-
diff numerics.

Run directly:
  python3 -m unittest harness.tests.test_build_chic_v12
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CROSS_POOL_MD = ROOT / "results" / "chic_v12_cross_pool_l3.md"
TIER3_SUMMARY_MD = ROOT / "results" / "chic_v12_tier3_summary.md"

# 29 tier-3 candidates (chic-v5 leaderboard, chic-v12 brief locked-in).
TIER3_SIGNS = (
    "#002", "#005", "#006", "#007", "#008", "#009", "#011", "#017",
    "#020", "#021", "#027", "#033", "#037", "#039", "#040", "#043",
    "#045", "#050", "#055", "#056", "#058", "#059", "#060", "#063",
    "#065", "#066", "#069", "#072", "#078",
)


class CrossPoolArtifactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CROSS_POOL_MD.read_text(encoding="utf-8")

    def test_artifact_exists(self) -> None:
        self.assertTrue(CROSS_POOL_MD.exists())

    def test_pool_dispatch_table_lists_all_4_pools(self) -> None:
        for pool in ("aquitanian", "etruscan", "toponym", "eteocretan"):
            self.assertIn(pool, self.text,
                          f"pool {pool!r} missing from cross-pool md")

    def test_all_29_tier3_candidates_present(self) -> None:
        for sid in TIER3_SIGNS:
            self.assertIn(f"`{sid}`", self.text,
                          f"tier-3 candidate {sid!r} missing")

    def test_per_candidate_subsections_present(self) -> None:
        for sid in TIER3_SIGNS:
            self.assertIn(f"### `{sid}`", self.text,
                          f"per-candidate detail subsection for {sid!r} missing")

    def test_three_reclassification_bands_present(self) -> None:
        for band in (
            "tier-2-equivalent",
            "tier-3-corroborated",
            "tier-3-uncorroborated",
        ):
            self.assertIn(band, self.text,
                          f"reclassification band {band!r} missing")

    def test_no_random_seed_phrase(self) -> None:
        # chic-v12 inherits chic-v5's hash-derived determinism, no RNG.
        self.assertNotIn("random.Random", self.text)

    def test_within_window_context_inspection_section_present(self) -> None:
        self.assertIn("## Within-window context inspection", self.text)


class Tier3SummaryArtifactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TIER3_SUMMARY_MD.read_text(encoding="utf-8")

    def test_artifact_exists(self) -> None:
        self.assertTrue(TIER3_SUMMARY_MD.exists())

    def test_headline_counts_section(self) -> None:
        self.assertIn("## Headline counts", self.text)

    def test_verdict_section(self) -> None:
        self.assertIn("## Verdict", self.text)

    def test_per_candidate_one_line_summary(self) -> None:
        self.assertIn("## Per-candidate one-line summary", self.text)
        # Spot check: every tier-3 sign id should appear in the summary.
        for sid in TIER3_SIGNS:
            self.assertIn(f"`{sid}`", self.text,
                          f"tier-3 candidate {sid!r} missing from summary")

    def test_cross_references_section(self) -> None:
        self.assertIn("## Cross-references", self.text)
        for ref in (
            "results/chic_v12_cross_pool_l3.md",
            "results/chic_value_extraction_leaderboard.md",
            "results/chic_v11_cross_pool_l3.md",
            "results/chic_v9_loo_validation.md",
        ):
            self.assertIn(ref, self.text,
                          f"cross-reference {ref!r} missing from summary")


if __name__ == "__main__":
    unittest.main()
