"""Smoke + invariant tests for the chic-v8 dual-script bilingual driver
(mg-dfcc).

Validates the artifacts produced by `scripts/build_chic_v8.py`:

  results/chic_dual_script_bilingual_leaderboard.md
  results/chic_v8_promoted_candidates.md

The chic-v8 driver is fast (~1s; pure markdown rendering plus a small
hand-verified AB → phonetic mapping); the tests assert framework-level
invariants on the outputs rather than re-deriving the analysis.

Run directly:
  python3 -m unittest harness.tests.test_build_chic_v8
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts import build_chic_v8  # noqa: E402

LEADERBOARD = REPO_ROOT / "results" / "chic_dual_script_bilingual_leaderboard.md"
PROMOTED = REPO_ROOT / "results" / "chic_v8_promoted_candidates.md"


class ClassifyValueTest(unittest.TestCase):
    """The phoneme class taxonomy must be consistent with chic-v5's."""

    def test_known_la_carryover_values_classify_consistently(self):
        # Subset of AB carryovers that appear in PS Za 2 / SY Za 4.
        cases = {
            "ta": "stop",
            "na": "nasal",
            "i": "vowel",
            "ti": "stop",
            "ja": "glide",
            "sa": "fricative",
            "ra": "liquid",
            "me": "nasal",
            "re": "liquid",
            "ke": "stop",
            "a": "vowel",
            "wa": "glide",
            "wi": "glide",
            "ni": "nasal",
            "pa3": "stop",
        }
        for value, expected_class in cases.items():
            self.assertEqual(
                build_chic_v8.classify_value(value),
                expected_class,
                f"value {value!r} → expected {expected_class}, "
                f"got {build_chic_v8.classify_value(value)!r}",
            )

    def test_classify_value_handles_none_and_empty(self):
        self.assertIsNone(build_chic_v8.classify_value(None))
        self.assertIsNone(build_chic_v8.classify_value(""))


class ChicAnchorsLoaderTest(unittest.TestCase):
    """The chic-v2 anchor loader must produce the same 20 anchors as
    `pools/cretan_hieroglyphic_anchors.yaml`'s n_anchors_total field."""

    def test_loads_twenty_anchors(self):
        anchors = build_chic_v8.load_chic_anchors()
        self.assertEqual(
            len(anchors), 20,
            f"chic-v2 anchor pool size is 20 by construction; got {len(anchors)}"
        )

    def test_anchors_include_chic_328_relevant_signs(self):
        # CHIC #328 (Mallia altar stone) carries 7 anchored positions:
        # #070=ra, #025=ta, #019=ke, #077=ma, #049=de, #038=i; and #062
        # is NOT an anchor (uncertain reading at position 1).
        anchors = build_chic_v8.load_chic_anchors()
        for sign, expected in [
            ("#070", "ra"),
            ("#025", "ta"),
            ("#019", "ke"),
            ("#077", "ma"),
            ("#049", "de"),
            ("#038", "i"),
        ]:
            self.assertEqual(
                anchors.get(sign), expected,
                f"anchor for {sign} expected {expected!r}, got {anchors.get(sign)!r}"
            )
        self.assertNotIn("#062", anchors)


class ChicV5LoaderTest(unittest.TestCase):
    """The chic-v5 leaderboard parser must produce 76 unknown signs."""

    def test_loads_seventy_six_unknown_signs(self):
        v5 = build_chic_v8.load_chic_v5_tiers()
        self.assertEqual(
            len(v5), 76,
            f"chic-v5 has 76 unknown CHIC syllabographic signs by construction;"
            f" got {len(v5)}"
        )

    def test_tier_2_signs_are_three(self):
        v5 = build_chic_v8.load_chic_v5_tiers()
        tier2 = [s for s, v in v5.items() if v["tier"] == "tier-2"]
        self.assertEqual(set(tier2), {"#001", "#012", "#032"})


class LeaderboardOutputTest(unittest.TestCase):
    """The leaderboard markdown must include the load-bearing sections."""

    def setUp(self):
        self.text = LEADERBOARD.read_text()

    def test_headline_is_zero_new_tier_2_candidates(self):
        self.assertIn("0 new tier-2 candidates", self.text)

    def test_section_headers_present(self):
        for header in [
            "## 1. The Malia altar stone (Daniel's primary case)",
            "## 2. Systematic survey for other dual-script artifacts",
            "## 3. Genre-parallel comparison",
            "## 4. L5 (LA-constraint) voting outcome",
            "## 5. Per-sign tier-3/tier-4 → tier-2 promotion analysis",
            "## 6. Headline + discipline-protecting framing",
            "## 7. Reproducibility",
        ]:
            self.assertIn(header, self.text, f"missing section: {header}")

    def test_chic_328_identified_correctly(self):
        # The Malia altar stone is CHIC #328, Mallia, offering_table.
        self.assertIn("CHIC #328", self.text)
        self.assertIn("Mallia", self.text)
        self.assertIn("offering_table", self.text)

    def test_la_libation_tables_identified(self):
        # The two LA libation tables in the v0 corpus.
        self.assertIn("PS Za 2", self.text)
        self.assertIn("SY Za 4", self.text)

    def test_l5_silent_for_all_unknowns(self):
        # The L5 vote summary table should have one "silent" row per chic-v5
        # unknown sign (76 rows).
        silent_count = self.text.count("| silent |")
        self.assertEqual(
            silent_count, 76,
            f"L5 should be silent for all 76 chic-v5 unknowns; got {silent_count}"
        )

    def test_genre_parallel_disclaimer_present(self):
        # Anti-motivated-reasoning discipline: the genre-parallel comparison
        # is informational only, not load-bearing.
        self.assertIn("SCHOLARLY CONJECTURE", self.text)
        self.assertIn("informational only", self.text)


class PromotedCandidatesOutputTest(unittest.TestCase):
    """The promoted candidates file must enumerate the null result clearly."""

    def setUp(self):
        self.text = PROMOTED.read_text()

    def test_zero_promoted_candidates_in_headline(self):
        self.assertIn("0 new tier-2 candidates", self.text)

    def test_no_promoted_rows_in_table(self):
        # The table should have a placeholder row, not real data rows. The
        # null-result placeholder is `_(no rows; null result)_`.
        self.assertIn("_(no rows; null result)_", self.text)

    def test_tier_3_count_matches(self):
        # 29 chic-v5 tier-3 signs inspected.
        self.assertIn("29 chic-v5 tier-3 signs inspected", self.text)

    def test_tier_4_count_matches(self):
        # 17 chic-v5 tier-4 signs inspected.
        self.assertIn("17 chic-v5 tier-4 signs inspected", self.text)


class DeterminismTest(unittest.TestCase):
    """Re-running the chic-v8 build script produces byte-identical outputs."""

    def test_byte_identical_re_run(self):
        before_lb = LEADERBOARD.read_bytes()
        before_pr = PROMOTED.read_bytes()
        # Run the script directly (it is the canonical entry point).
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "build_chic_v8.py")],
            capture_output=True,
            cwd=str(REPO_ROOT),
            text=True,
        )
        self.assertEqual(
            result.returncode, 0,
            f"build_chic_v8.py returned non-zero: stderr={result.stderr}"
        )
        after_lb = LEADERBOARD.read_bytes()
        after_pr = PROMOTED.read_bytes()
        self.assertEqual(
            before_lb, after_lb,
            "leaderboard markdown changed across re-run — chic-v8 is non-deterministic"
        )
        self.assertEqual(
            before_pr, after_pr,
            "promoted candidates markdown changed across re-run — chic-v8 is non-deterministic"
        )


class FindingsUpdateTest(unittest.TestCase):
    """AGENTS.md non-negotiable: chic-v8 must update both findings docs."""

    def test_findings_md_has_mg_dfcc_entry(self):
        text = (REPO_ROOT / "docs" / "findings.md").read_text()
        self.assertIn("## Findings from mg-dfcc", text)
        self.assertIn("0 new tier-2 candidates", text)

    def test_findings_summary_md_has_chic_v8_subsection(self):
        text = (REPO_ROOT / "docs" / "findings_summary.md").read_text()
        self.assertIn("#### chic-v8", text)
        # Brief's required framing element: the L5-as-fifth-line discipline.
        self.assertIn("L5", text)


if __name__ == "__main__":
    unittest.main()
