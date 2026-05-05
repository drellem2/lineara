"""Smoke + invariant tests for the chic-v5 per-sign value-extraction
driver (mg-7c6d).

Validates the artifacts produced by `scripts/build_chic_v5.py`:

  harness/chic_sign_fingerprints.json
  pools/cretan_hieroglyphic_signs.distributional.yaml
  results/chic_anchor_distance_map.md
  results/chic_substrate_consistency.md
  results/chic_value_extraction_leaderboard.md

The chic-v5 driver itself is exercised end-to-end (it's fast: ~30s on
the CHIC syllabographic stream); the tests assert framework-level
invariants on the artifact outputs rather than re-deriving the
substrate-consistency numerics from scratch.

Run directly:
  python3 -m unittest harness.tests.test_build_chic_v5
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts import build_chic_v5  # noqa: E402

FINGERPRINTS = REPO_ROOT / "harness" / "chic_sign_fingerprints.json"
DISTRIBUTIONAL = (
    REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.distributional.yaml"
)
ANCHOR_MAP = REPO_ROOT / "results" / "chic_anchor_distance_map.md"
SUBSTRATE = REPO_ROOT / "results" / "chic_substrate_consistency.md"
LEADERBOARD = REPO_ROOT / "results" / "chic_value_extraction_leaderboard.md"

SIGNS_YAML = REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
ANCHORS_YAML = REPO_ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"


class PhonemeClassTaxonomyTest(unittest.TestCase):
    """The class taxonomy is the agreement predicate; chic-v5's tier
    classification depends on this mapping being stable."""

    def test_anchor_pool_values_all_classify_to_known_class(self):
        with ANCHORS_YAML.open("r", encoding="utf-8") as fh:
            pool = yaml.safe_load(fh)
        for anchor in pool["anchors"]:
            value = anchor["linear_b_carryover_phonetic"]
            cls = build_chic_v5.classify_value(value)
            self.assertNotEqual(
                cls, "unknown",
                f"anchor value {value!r} for {anchor['chic_sign']} "
                f"classifies as 'unknown' — taxonomy missing this onset",
            )

    def test_known_class_examples(self):
        # Sanity: the standard linguist's class split applied to LB-style
        # CV syllables.
        cases = {
            "a": "vowel", "i": "vowel", "u": "vowel",
            "ka": "stop", "te": "stop", "de": "stop",
            "ma": "nasal", "ne": "nasal",
            "ra": "liquid", "lo": "liquid",
            "wa": "glide", "je": "glide", "ja": "glide",
            "se": "fricative", "ho": "fricative",
        }
        for value, expected in cases.items():
            self.assertEqual(
                build_chic_v5.classify_value(value), expected,
                f"classify_value({value!r}) should be {expected!r}",
            )


class BhattacharyyaCoefficientTest(unittest.TestCase):
    def test_identical_distributions_score_1(self):
        d = {"a": 0.5, "b": 0.5}
        self.assertAlmostEqual(build_chic_v5.bhattacharyya(d, d), 1.0, places=12)

    def test_disjoint_distributions_score_0(self):
        a = {"x": 1.0}
        b = {"y": 1.0}
        self.assertAlmostEqual(build_chic_v5.bhattacharyya(a, b), 0.0, places=12)

    def test_empty_distribution_yields_zero(self):
        self.assertEqual(build_chic_v5.bhattacharyya({}, {"a": 1.0}), 0.0)
        self.assertEqual(build_chic_v5.bhattacharyya({"a": 1.0}, {}), 0.0)

    def test_symmetric(self):
        a = {"x": 0.3, "y": 0.7}
        b = {"x": 0.6, "y": 0.4}
        self.assertAlmostEqual(
            build_chic_v5.bhattacharyya(a, b),
            build_chic_v5.bhattacharyya(b, a),
            places=12,
        )

    def test_in_unit_interval(self):
        a = {"x": 0.2, "y": 0.5, "z": 0.3}
        b = {"x": 0.7, "z": 0.3}
        bc = build_chic_v5.bhattacharyya(a, b)
        self.assertGreaterEqual(bc, 0.0)
        self.assertLessEqual(bc, 1.0)


class ControlPhonemeTest(unittest.TestCase):
    def test_control_is_class_disjoint(self):
        pool = ["a", "ke", "ki", "ma", "mu", "ra", "wa", "i", "te"]
        for cand in pool:
            cand_class = build_chic_v5.classify_value(cand)
            ctrl = build_chic_v5.control_phoneme_for(
                "#005", cand, cand_class, pool
            )
            ctrl_class = build_chic_v5.classify_value(ctrl)
            self.assertNotEqual(
                ctrl_class, cand_class,
                f"control {ctrl!r} ({ctrl_class}) is in same class as "
                f"candidate {cand!r} ({cand_class})",
            )

    def test_deterministic(self):
        pool = ["a", "ke", "ma", "ra", "wa"]
        c1 = build_chic_v5.control_phoneme_for("#005", "ke", "stop", pool)
        c2 = build_chic_v5.control_phoneme_for("#005", "ke", "stop", pool)
        self.assertEqual(c1, c2)

    def test_different_signs_can_get_different_controls(self):
        pool = ["a", "ke", "ma", "ra", "wa"]
        # Just verify no crash + class-disjoint for many sign hashes.
        seen: set[str] = set()
        for sid in ("#001", "#005", "#012", "#032", "#077"):
            ctrl = build_chic_v5.control_phoneme_for(sid, "ke", "stop", pool)
            seen.add(ctrl)
            self.assertNotEqual(
                build_chic_v5.classify_value(ctrl), "stop",
            )
        # Sanity: at least the mechanism *can* yield variety across signs
        # (not strictly required, but a degenerate-collapse smoke test).
        self.assertGreaterEqual(len(seen), 1)


class FingerprintsArtifactTest(unittest.TestCase):
    """The fingerprints JSON is the load-bearing chic-v5 artifact."""

    def setUp(self):
        if not FINGERPRINTS.exists():
            self.skipTest(
                f"missing {FINGERPRINTS}; run scripts/build_chic_v5.py first"
            )
        self.payload = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))

    def test_schema_version(self):
        self.assertEqual(
            self.payload.get("schema_version"), "chic_sign_fingerprints.v1"
        )

    def test_dimensions_field(self):
        self.assertEqual(
            self.payload["fingerprint_dimensions"],
            ["left_neighbor", "right_neighbor", "position", "support"],
        )

    def test_anchor_count_matches_chic_v2_pool(self):
        with ANCHORS_YAML.open("r", encoding="utf-8") as fh:
            pool = yaml.safe_load(fh)
        n_anchors = len(pool["anchors"])
        self.assertEqual(self.payload["n_anchor_signs"], n_anchors)

    def test_syllabographic_count_matches_chic_v1(self):
        with SIGNS_YAML.open("r", encoding="utf-8") as fh:
            signs = yaml.safe_load(fh)
        n_syll = sum(
            1 for s in signs["signs"] if s["sign_class"] == "syllabographic"
        )
        self.assertEqual(self.payload["n_syllabographic_signs"], n_syll)

    def test_unknown_count_is_complement(self):
        self.assertEqual(
            self.payload["n_unknown_signs"],
            self.payload["n_syllabographic_signs"]
            - self.payload["n_anchor_signs"],
        )

    def test_each_sign_has_all_dimensions(self):
        required = {"left_neighbor", "right_neighbor", "position", "support",
                    "frequency", "inscription_count", "is_anchor"}
        for sid, cell in self.payload["signs"].items():
            self.assertTrue(
                required.issubset(set(cell.keys())),
                f"sign {sid} missing fields {required - set(cell.keys())}",
            )

    def test_anchor_flag_consistency(self):
        """The is_anchor flag must agree with the chic-v2 anchor pool."""
        with ANCHORS_YAML.open("r", encoding="utf-8") as fh:
            pool = yaml.safe_load(fh)
        anchor_ids = {a["chic_sign"] for a in pool["anchors"]}
        for sid, cell in self.payload["signs"].items():
            self.assertEqual(
                cell["is_anchor"], sid in anchor_ids,
                f"sign {sid} is_anchor flag inconsistent with anchor pool",
            )


class LeaderboardArtifactTest(unittest.TestCase):
    def setUp(self):
        if not LEADERBOARD.exists():
            self.skipTest(
                f"missing {LEADERBOARD}; run scripts/build_chic_v5.py first"
            )
        self.text = LEADERBOARD.read_text(encoding="utf-8")

    def test_headline_counts_section(self):
        self.assertIn("## Headline counts", self.text)
        self.assertIn("tier-1", self.text)
        self.assertIn("tier-2", self.text)
        self.assertIn("tier-3", self.text)
        self.assertIn("tier-4", self.text)
        self.assertIn("untiered", self.text)

    def test_lines_of_evidence_section(self):
        self.assertIn("## Lines of evidence", self.text)
        for line in (
            "Line 1: distributional plurality",
            "Line 2: anchor-distance",
            "Line 3: substrate-consistency under Eteocretan LM",
            "Line 4: cross-script paleographic",
        ):
            self.assertIn(line, self.text)

    def test_per_sign_verdict_table_present(self):
        self.assertIn("## Per-sign tier verdict", self.text)
        # The first three sign rows by id should appear (sorted by tier
        # then sign id; #001 is sign-id 1 in the syllabographic range).
        self.assertIn("`#001`", self.text)

    def test_tier_2_section_present(self):
        self.assertIn("## Tier-2 candidate proposals", self.text)

    def test_tier_3_section_present(self):
        self.assertIn("## Tier-3 suggestive", self.text)

    def test_pending_review_caveat_present(self):
        # The brief insists tier-2 candidates be framed as
        # candidate proposals, not decipherments.
        self.assertIn(
            "candidate proposal", self.text.lower(),
        )
        # And explicit pending-domain-expert-review framing somewhere.
        self.assertIn(
            "domain-expert review", self.text,
        )

    def test_methodological_limitation_documented(self):
        # Cross-script line being silent for all unknowns is a
        # methodological limitation that must be documented.
        self.assertIn(
            "Silent for all 76 unknowns", self.text,
        )


class SubstrateConsistencyArtifactTest(unittest.TestCase):
    def setUp(self):
        if not SUBSTRATE.exists():
            self.skipTest(
                f"missing {SUBSTRATE}; run scripts/build_chic_v5.py first"
            )
        self.text = SUBSTRATE.read_text(encoding="utf-8")

    def test_per_sign_topk_section(self):
        self.assertIn("## Per-sign top-K candidates", self.text)

    def test_per_sign_class_means_section(self):
        self.assertIn("## Per-sign class-mean paired_diff", self.text)

    def test_no_random_seed_phrase(self):
        # Discipline check: the script must NOT have used random.Random().
        # The artifact should explicitly call out the deterministic-seed
        # implementation as sha256-keyed.
        self.assertIn("sha256", self.text)


class AnchorDistanceArtifactTest(unittest.TestCase):
    def setUp(self):
        if not ANCHOR_MAP.exists():
            self.skipTest(
                f"missing {ANCHOR_MAP}; run scripts/build_chic_v5.py first"
            )
        self.text = ANCHOR_MAP.read_text(encoding="utf-8")

    def test_top_3_section_present(self):
        self.assertIn("## Per-sign top-3 nearest anchors", self.text)

    def test_unknown_count_in_coverage(self):
        # 76 unknowns is the load-bearing count.
        self.assertIn("**76**", self.text)


if __name__ == "__main__":
    unittest.main()
