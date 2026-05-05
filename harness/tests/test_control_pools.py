"""Phonotactic control pool builder (mg-f419).

Validates that ``scripts/build_control_pools.py`` produces phonotactically-
equivalent control pools:

  (a) Same number of entries as the substrate pool.
  (b) Identical length distribution (one control entry per substrate
      entry, same N).
  (c) Inventory subset: every phoneme in the control pool appears in the
      substrate pool's inventory.
  (d) Determinism: re-building from the same substrate YAML yields a
      byte-identical control YAML.
  (e) Region tag: every control entry carries
      ``region: phonotactic_control_<substrate_pool_name>``.
  (f) Schema-validity (the builder calls the validator internally; this
      test re-asserts on the materialized YAML to catch round-trip
      regressions).

Smoke set: a small synthetic substrate pool (8 entries, 3 phonemes) so the
test is fast and self-contained — does not depend on the real Aquitanian /
Etruscan / toponym files. The builder's behavior on the real pools is
exercised by the ``./test.sh`` integration run (or by hand via
``python3 scripts/build_control_pools.py`` and inspecting the generated
READMEs).
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from scripts.build_control_pools import (  # noqa: E402
    _seed_for,
    build_one,
    length_distribution,
    phoneme_bigram_histogram,
    phoneme_first_histogram,
    phoneme_histogram,
    write_readme,
)


_POOL_SCHEMA_PATH = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"


def _smoke_pool() -> dict:
    """A small, deterministic substrate-pool fixture for the smoke test.

    8 entries with mixed lengths (2..6) over a small phoneme inventory
    {a, b, c, l, n, t}. Picks deliberate length-distribution variety so
    the test exercises the per-entry length matching, not just the bulk
    count.
    """
    return {
        "pool": "smoke_substrate",
        "source_citation": "synthetic test fixture",
        "license": "synthetic",
        "fetched_at": "2026-05-04T00:00:00Z",
        "entries": [
            {"surface": "ab", "phonemes": ["a", "b"], "region": "fixture"},
            {"surface": "abc", "phonemes": ["a", "b", "c"], "region": "fixture"},
            {"surface": "lan", "phonemes": ["l", "a", "n"], "region": "fixture"},
            {"surface": "tata", "phonemes": ["t", "a", "t", "a"], "region": "fixture"},
            {"surface": "atan", "phonemes": ["a", "t", "a", "n"], "region": "fixture"},
            {"surface": "lacala", "phonemes": ["l", "a", "c", "a", "l", "a"], "region": "fixture"},
            {"surface": "tabac", "phonemes": ["t", "a", "b", "a", "c"], "region": "fixture"},
            {"surface": "ban", "phonemes": ["b", "a", "n"], "region": "fixture"},
        ],
    }


class ControlPoolBuilderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="mg_f419_"))
        # Build the smoke pools dir layout the builder expects.
        (self.tmp / "schemas").mkdir(parents=True)
        shutil.copy(_POOL_SCHEMA_PATH, self.tmp / "schemas" / "pool.v1.schema.json")
        self.substrate = _smoke_pool()
        self.substrate_path = self.tmp / "smoke_substrate.yaml"
        self.substrate_path.write_text(
            yaml.safe_dump(self.substrate, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _load(self, path: Path) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_phonotactic_match_and_metadata(self) -> None:
        summary = build_one("smoke_substrate", self.tmp)
        self.assertEqual(summary["n_entries"], len(self.substrate["entries"]))

        ctrl_path = self.tmp / "control_smoke_substrate.yaml"
        self.assertTrue(ctrl_path.exists())
        ctrl = self._load(ctrl_path)

        # (a) entry count
        self.assertEqual(len(ctrl["entries"]), len(self.substrate["entries"]))

        # (b) length distribution
        self.assertEqual(
            length_distribution(ctrl), length_distribution(self.substrate)
        )

        # (c) inventory subset
        sub_inv = set(phoneme_histogram(self.substrate))
        ctrl_inv = set(phoneme_histogram(ctrl))
        self.assertTrue(
            ctrl_inv <= sub_inv,
            f"control inventory {ctrl_inv} not subset of substrate {sub_inv}",
        )

        # (e) region tag on every entry
        for entry in ctrl["entries"]:
            self.assertEqual(
                entry["region"], "phonotactic_control_smoke_substrate"
            )
            # No semantic_field on controls (gg1 falls back to neutral 0.5)
            self.assertNotIn("semantic_field", entry)

        # (f) schema-valid
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(ctrl)

    def test_determinism_byte_identical(self) -> None:
        build_one("smoke_substrate", self.tmp)
        ctrl_path = self.tmp / "control_smoke_substrate.yaml"
        first = ctrl_path.read_bytes()
        # Touch + rebuild
        ctrl_path.unlink()
        build_one("smoke_substrate", self.tmp)
        second = ctrl_path.read_bytes()
        self.assertEqual(
            first, second, "control pool YAML must be byte-identical across rebuilds"
        )

    def test_readme_renders_and_lists_inventory(self) -> None:
        build_one("smoke_substrate", self.tmp)
        readme_path = write_readme("smoke_substrate", self.tmp)
        text = readme_path.read_text(encoding="utf-8")
        self.assertIn("# control_smoke_substrate", text)
        self.assertIn("## Matching algorithm", text)
        self.assertIn("## Phoneme inventory and frequency", text)
        # All substrate phonemes should appear in the table.
        for ph in phoneme_histogram(self.substrate):
            self.assertIn(f"`{ph}`", text)
        # The seed should be reported.
        self.assertIn("Seed", text)

    def test_no_within_pool_surface_collisions(self) -> None:
        build_one("smoke_substrate", self.tmp)
        ctrl = self._load(self.tmp / "control_smoke_substrate.yaml")
        surfaces = [e["surface"] for e in ctrl["entries"]]
        self.assertEqual(
            len(surfaces), len(set(surfaces)), f"control pool has duplicate surfaces: {surfaces}"
        )


class BigramSamplerTest(unittest.TestCase):
    """v18 (mg-9f18) bigram-preserving control sampler.

    Smoke-tests that the bigram sampler produces phonotactically-
    distinguishable controls relative to the unigram sampler:

      (a) Pool naming honors --suffix; the bigram pool exists at the
          expected path and does not overwrite the unigram pool.
      (b) The bigram pool's seed is *distinct* from the unigram pool's
          seed (sampler-suffixed key) so the two control pools draw
          from disjoint random streams.
      (c) The bigram pool is byte-identical across rebuilds.
      (d) The bigram pool's surface set differs from the unigram
          pool's, on a fixture rich enough to expose both samplers.
      (e) The bigram histogram derived by ``phoneme_bigram_histogram``
          matches what a hand-rolled count would produce.
    """

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="mg_9f18_"))
        (self.tmp / "schemas").mkdir(parents=True)
        shutil.copy(_POOL_SCHEMA_PATH, self.tmp / "schemas" / "pool.v1.schema.json")
        # Use the larger smoke pool so the bigram histogram has enough
        # transition variety to produce visibly different output from
        # the unigram pool.
        self.substrate = _smoke_pool()
        self.substrate_path = self.tmp / "smoke_substrate.yaml"
        self.substrate_path.write_text(
            yaml.safe_dump(self.substrate, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _load(self, path: Path) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_pool_naming_with_suffix(self) -> None:
        summary = build_one(
            "smoke_substrate", self.tmp, sampler="bigram", suffix="_bigram"
        )
        self.assertEqual(summary["control_pool"], "control_smoke_substrate_bigram")
        self.assertEqual(summary["sampler"], "bigram")
        self.assertEqual(summary["alpha"], 0.1)
        self.assertTrue(
            (self.tmp / "control_smoke_substrate_bigram.yaml").exists(),
            "bigram pool must be written when --suffix is supplied",
        )

    def test_seed_distinct_from_unigram_seed(self) -> None:
        unigram_seed = _seed_for("smoke_substrate", sampler="unigram")
        bigram_seed = _seed_for("smoke_substrate", sampler="bigram")
        self.assertNotEqual(
            unigram_seed,
            bigram_seed,
            "v6 unigram and v18 bigram samplers must use distinct "
            "seeds — same seed would mean the two control pools draw "
            "from the same random stream",
        )

    def test_determinism_byte_identical(self) -> None:
        build_one(
            "smoke_substrate", self.tmp, sampler="bigram", suffix="_bigram"
        )
        path = self.tmp / "control_smoke_substrate_bigram.yaml"
        first = path.read_bytes()
        path.unlink()
        build_one(
            "smoke_substrate", self.tmp, sampler="bigram", suffix="_bigram"
        )
        second = path.read_bytes()
        self.assertEqual(
            first,
            second,
            "bigram-sampler control pool must be byte-identical across rebuilds",
        )

    def test_bigram_distinct_from_unigram_surfaces(self) -> None:
        """The bigram pool's realized surfaces must not be identical to
        the unigram pool's (they share inventory + length distribution
        but draw from different conditional structures)."""
        build_one("smoke_substrate", self.tmp, sampler="unigram")
        build_one(
            "smoke_substrate", self.tmp, sampler="bigram", suffix="_bigram"
        )
        unigram = self._load(self.tmp / "control_smoke_substrate.yaml")
        bigram = self._load(self.tmp / "control_smoke_substrate_bigram.yaml")
        unigram_surfaces = sorted(e["surface"] for e in unigram["entries"])
        bigram_surfaces = sorted(e["surface"] for e in bigram["entries"])
        # On the smoke fixture (8 entries, small inventory) collision
        # of a few surfaces is possible by chance; the *full sets* must
        # not be identical.
        self.assertNotEqual(
            unigram_surfaces,
            bigram_surfaces,
            "v6 unigram and v18 bigram realized surface sets are "
            "identical; the --sampler flag is a no-op or one of the "
            "seeds is wrong",
        )

    def test_bigram_inventory_subset_and_length_match(self) -> None:
        """The bigram pool still satisfies the v6 invariants — it only
        tightens the control's phonotactic match, never broadens the
        inventory or breaks the length distribution."""
        build_one(
            "smoke_substrate", self.tmp, sampler="bigram", suffix="_bigram"
        )
        bigram = self._load(self.tmp / "control_smoke_substrate_bigram.yaml")
        self.assertEqual(len(bigram["entries"]), len(self.substrate["entries"]))
        self.assertEqual(
            length_distribution(bigram), length_distribution(self.substrate)
        )
        self.assertTrue(
            set(phoneme_histogram(bigram)) <= set(phoneme_histogram(self.substrate))
        )
        # Region tag carries the suffix so it stays unmapped in
        # _GG1_REGION_COMPAT.
        for entry in bigram["entries"]:
            self.assertEqual(
                entry["region"], "phonotactic_control_smoke_substrate_bigram"
            )

    def test_bigram_histogram_is_correct(self) -> None:
        """``phoneme_bigram_histogram`` must produce the same counts a
        hand-rolled walk over adjacent pairs would."""
        bigram = phoneme_bigram_histogram(self.substrate)
        # First entry: ['a', 'b']. One transition: a → b.
        # Second entry: ['a', 'b', 'c']. Transitions: a→b, b→c.
        # ... etc. The fixture has 8 entries; total transitions =
        # sum(len(phonemes) - 1 for entry).
        expected_total = sum(
            max(0, len(e["phonemes"]) - 1) for e in self.substrate["entries"]
        )
        actual_total = sum(sum(c.values()) for c in bigram.values())
        self.assertEqual(expected_total, actual_total)

    def test_first_histogram_matches_position_zero_counts(self) -> None:
        """``phoneme_first_histogram`` must count each entry's [0]
        phoneme exactly once."""
        first = phoneme_first_histogram(self.substrate)
        expected: Counter = Counter(
            e["phonemes"][0] for e in self.substrate["entries"] if e["phonemes"]
        )
        self.assertEqual(first, expected)

    def test_unsuffixed_bigram_overwrites_unigram(self) -> None:
        """When --suffix is *not* supplied the bigram pool name is
        ``control_<pool>`` (no suffix), which collides with the unigram
        path. This is intended (the user opted in by choosing the
        bigram sampler without a suffix), but the test asserts the
        builder doesn't silently keep the unigram seed key when this
        happens — the surface set must reflect the bigram seed."""
        build_one("smoke_substrate", self.tmp, sampler="unigram")
        unigram_surfaces = sorted(
            e["surface"]
            for e in self._load(
                self.tmp / "control_smoke_substrate.yaml"
            )["entries"]
        )
        build_one("smoke_substrate", self.tmp, sampler="bigram")
        bigram_surfaces = sorted(
            e["surface"]
            for e in self._load(
                self.tmp / "control_smoke_substrate.yaml"
            )["entries"]
        )
        self.assertNotEqual(unigram_surfaces, bigram_surfaces)


class CommittedBigramToponymControlTest(unittest.TestCase):
    """Sanity check on the committed pools/control_toponym_bigram.yaml
    (mg-9f18, harness v18); only runs if the file exists."""

    def test_committed_bigram_toponym_pool(self) -> None:
        path = _REPO_ROOT / "pools" / "control_toponym_bigram.yaml"
        if not path.exists():
            self.skipTest(
                f"{path} not built; run scripts/build_control_pools.py "
                f"--pool toponym --sampler bigram --suffix _bigram"
            )
        ctrl = yaml.safe_load(path.read_text(encoding="utf-8"))
        substrate_path = _REPO_ROOT / "pools" / "toponym.yaml"
        substrate = yaml.safe_load(substrate_path.read_text(encoding="utf-8"))

        # Same entry count + length distribution as the substrate.
        self.assertEqual(len(ctrl["entries"]), len(substrate["entries"]))
        self.assertEqual(
            length_distribution(ctrl), length_distribution(substrate)
        )

        # Inventory subset of substrate.
        self.assertTrue(
            set(phoneme_histogram(ctrl)) <= set(phoneme_histogram(substrate))
        )

        # Region tag carries the bigram suffix so the bigram pool is
        # routed to its own provenance bucket.
        for entry in ctrl["entries"]:
            self.assertEqual(
                entry["region"], "phonotactic_control_toponym_bigram"
            )
            self.assertNotIn("semantic_field", entry)

        # Schema valid.
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(ctrl)

        # No within-pool surface duplicates.
        surfaces = [e["surface"] for e in ctrl["entries"]]
        self.assertEqual(len(surfaces), len(set(surfaces)))


class CommittedControlPoolsTest(unittest.TestCase):
    """Sanity check on the committed control_*.yaml pools (Aquitanian,
    Etruscan, toponym). These should already exist on disk after running
    ``python3 scripts/build_control_pools.py``; this test only inspects
    them (no rewrites)."""

    def test_committed_control_pool_shape(self) -> None:
        for sub_name in ("aquitanian", "etruscan", "toponym"):
            sub = yaml.safe_load(
                (_REPO_ROOT / "pools" / f"{sub_name}.yaml").read_text(encoding="utf-8")
            )
            ctrl_path = _REPO_ROOT / "pools" / f"control_{sub_name}.yaml"
            if not ctrl_path.exists():
                self.skipTest(f"{ctrl_path} not built; run scripts/build_control_pools.py")
            ctrl = yaml.safe_load(ctrl_path.read_text(encoding="utf-8"))
            with self.subTest(pool=sub_name):
                self.assertEqual(
                    len(ctrl["entries"]), len(sub["entries"]),
                    "control pool entry count must match substrate",
                )
                self.assertEqual(
                    length_distribution(ctrl), length_distribution(sub),
                    "control pool length distribution must match substrate",
                )
                # Inventory subset
                self.assertTrue(
                    set(phoneme_histogram(ctrl)) <= set(phoneme_histogram(sub)),
                    f"control_{sub_name} inventory must be subset of substrate",
                )
                # Region tag
                for entry in ctrl["entries"]:
                    self.assertEqual(
                        entry["region"], f"phonotactic_control_{sub_name}",
                    )


if __name__ == "__main__":
    unittest.main()
