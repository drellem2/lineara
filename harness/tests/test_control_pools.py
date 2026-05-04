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
    build_one,
    length_distribution,
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
