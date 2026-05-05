"""Smoke + invariant tests for chic-v11 (mg-d69c).

Validates the artifacts produced by ``scripts/build_chic_v11.py``:

  results/chic_v11_cross_pool_l3.md
  results/chic_v11_032_ku_pa_context.md

The chic-v11 driver is fast (~30s end-to-end on the CHIC syllabographic
stream and the chic-v6 experiments JSONL). Tests assert framework-level
invariants — required structural elements, the 3 candidate × 4 pool
dispatch matrix, the ku-pa-family lift identification on CHIC #057,
and per-candidate verdicts — rather than re-deriving paired-diff numerics.

Run directly:
  python3 -m unittest harness.tests.test_build_chic_v11
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CROSS_POOL_MD = ROOT / "results" / "chic_v11_cross_pool_l3.md"
KU_PA_MD = ROOT / "results" / "chic_v11_032_ku_pa_context.md"


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

    def test_three_candidate_subsections_present(self) -> None:
        for cand in ("#001", "#012", "#032"):
            self.assertIn(f"### Candidate `{cand}`", self.text,
                          f"candidate {cand!r} subsection missing")

    def test_summary_table_present(self) -> None:
        self.assertIn("## Cross-candidate cross-pool summary", self.text)

    def test_no_random_seed_phrase(self) -> None:
        # chic-v11 inherits chic-v5's hash-derived determinism, no RNG.
        self.assertNotIn("random.Random", self.text)


class KuPaArtifactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = KU_PA_MD.read_text(encoding="utf-8")

    def test_artifact_exists(self) -> None:
        self.assertTrue(KU_PA_MD.exists())

    def test_all_four_la_source_tablets_listed(self) -> None:
        for tab in ("HT 1", "HT 16", "HT 102", "HT 110a"):
            self.assertIn(tab, self.text,
                          f"LA source tablet {tab!r} missing from ku-pa md")

    def test_chic_057_lift_inscription_listed(self) -> None:
        self.assertIn("CHIC #057", self.text,
                      "CHIC #057 (the ku-pa-family lift inscription) missing")

    def test_partial_reading_under_032_override(self) -> None:
        # The chic-v2 anchors + #032 -> ki override should produce the
        # `ki pa` literal pair in the partial reading at the matched
        # position. The full rendered string includes `#079 ki pa /
        # NUM:20` (NUM:20 follows after the next DIV).
        self.assertIn("ki pa", self.text)
        self.assertIn("NUM:20", self.text)

    def test_all_four_scholar_entries_referenced(self) -> None:
        for sid in ("kupa3_HT1", "kupa_HT16", "kapa_HT102", "kupa_HT110a"):
            self.assertIn(sid, self.text,
                          f"scholar entry {sid!r} missing from ku-pa md")

    def test_combined_verdict_section(self) -> None:
        self.assertIn("## Combined verdict", self.text)

    def test_accountancy_genre_called_out(self) -> None:
        # All 4 source LA tablets are accountancy-genre; the md should
        # surface this verdict.
        self.assertIn("accountancy", self.text.lower())


if __name__ == "__main__":
    unittest.main()
