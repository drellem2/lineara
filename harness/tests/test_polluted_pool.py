"""Polluted-pool builder (mg-6b73, harness v14).

Smoke-tests ``scripts/build_polluted_pool.py`` and the committed
``pools/polluted_aquitanian.yaml`` artifact. The polluted pool is a
**test artifact** for the held-out pool-curation test — half real
Aquitanian entries, half synthetic conjecturals drawn from the real
pool's phoneme + length distribution.

Coverage:

  (a) Entry-count correctness: 2 × the underlying substrate pool
      (real + conjectural).
  (b) Provenance tagging: every entry carries
      ``provenance ∈ {real, conjectural}`` and the split is exactly
      50/50.
  (c) Real entries pass through verbatim — surface, phonemes, region,
      semantic_field, gloss, citation, attestations.
  (d) Conjectural entries carry ``region: aquitania`` so the candidate
      generator routes them through the same ``source_pool`` as real
      entries; ``semantic_field`` is omitted.
  (e) Surface uniqueness: no within-pool duplicates, no real ↔
      conjectural collisions.
  (f) Length distribution: polluted pool's length distribution is
      exactly 2 × the real pool's length distribution (i-th
      conjectural matches i-th real).
  (g) Two-class phoneme filter: every conjectural entry spans at
      least 2 distinct phoneme classes (V/S/C); the candidate
      generator therefore won't skip any conjectural entry.
  (h) Determinism: re-building from the same substrate YAML yields a
      byte-identical polluted YAML.
  (i) Schema-validity (the builder calls the validator internally;
      this test re-asserts on the materialized YAML to catch round-
      trip regressions).

The smoke fixture uses a small synthetic substrate pool so the test
is fast and self-contained. The committed ``polluted_aquitanian.yaml``
is also exercised in :class:`CommittedPollutedPoolTest`.
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

from scripts.build_polluted_pool import (  # noqa: E402
    _phoneme_class,
    _seed_for,
    _spans_two_classes,
    build_polluted_pool,
    write_readme,
)


_POOL_SCHEMA_PATH = _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"


def _smoke_substrate_pool() -> dict:
    """A small, deterministic Aquitanian-shaped substrate fixture.

    Surfaces and phonemes mirror the real Aquitanian pool's general
    shape (lengths 2..6, mixed V/S/C inventory) so the conjectural
    draws have enough variety to exercise the redraw paths and the
    two-class filter.
    """
    return {
        "pool": "aquitanian",
        "source_citation": "synthetic test fixture (mg-6b73)",
        "license": "synthetic",
        "fetched_at": "2026-05-04T00:00:00Z",
        "entries": [
            {
                "surface": "ata",
                "phonemes": ["a", "t", "a"],
                "region": "aquitania",
                "semantic_field": "kin",
                "gloss": "father",
                "citation": "fixture",
            },
            {
                "surface": "seme",
                "phonemes": ["s", "e", "m", "e"],
                "region": "aquitania",
                "semantic_field": "kin",
                "gloss": "son",
                "citation": "fixture",
            },
            {
                "surface": "ur",
                "phonemes": ["u", "r"],
                "region": "basque_substrate",
                "semantic_field": "nature",
                "gloss": "water",
                "citation": "fixture",
            },
            {
                "surface": "andere",
                "phonemes": ["a", "n", "d", "e", "r", "e"],
                "region": "aquitania",
                "semantic_field": "kin",
                "gloss": "lady",
                "citation": "fixture",
            },
            {
                "surface": "izar",
                "phonemes": ["i", "z", "a", "r"],
                "region": "basque_substrate",
                "semantic_field": "nature",
                "gloss": "star",
                "citation": "fixture",
            },
            {
                "surface": "lur",
                "phonemes": ["l", "u", "r"],
                "region": "basque_substrate",
                "semantic_field": "nature",
                "gloss": "earth",
                "citation": "fixture",
            },
        ],
    }


class PollutedPoolBuilderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="mg_6b73_"))
        (self.tmp / "schemas").mkdir(parents=True)
        shutil.copy(_POOL_SCHEMA_PATH, self.tmp / "schemas" / "pool.v1.schema.json")
        self.substrate = _smoke_substrate_pool()
        self.substrate_path = self.tmp / "aquitanian.yaml"
        self.substrate_path.write_text(
            yaml.safe_dump(self.substrate, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _load(self, path: Path) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_entry_counts_and_split(self) -> None:
        summary = build_polluted_pool("aquitanian", self.tmp)
        self.assertEqual(summary["n_entries"], 2 * len(self.substrate["entries"]))
        self.assertEqual(summary["n_real"], len(self.substrate["entries"]))
        self.assertEqual(summary["n_conjectural"], len(self.substrate["entries"]))

        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        self.assertEqual(len(polluted["entries"]), 2 * len(self.substrate["entries"]))
        provenances = Counter(e.get("provenance") for e in polluted["entries"])
        self.assertEqual(provenances["real"], len(self.substrate["entries"]))
        self.assertEqual(
            provenances["conjectural"], len(self.substrate["entries"])
        )
        self.assertNotIn(None, provenances)

    def test_real_entries_passthrough(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        real = [e for e in polluted["entries"] if e.get("provenance") == "real"]
        self.assertEqual(len(real), len(self.substrate["entries"]))
        for sub_entry, pol_entry in zip(self.substrate["entries"], real):
            self.assertEqual(sub_entry["surface"], pol_entry["surface"])
            self.assertEqual(sub_entry["phonemes"], pol_entry["phonemes"])
            self.assertEqual(sub_entry["region"], pol_entry["region"])
            self.assertEqual(
                sub_entry["semantic_field"], pol_entry["semantic_field"]
            )
            self.assertEqual(sub_entry["gloss"], pol_entry["gloss"])

    def test_conjectural_tagging_and_no_semantic_field(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        conj = [e for e in polluted["entries"] if e.get("provenance") == "conjectural"]
        self.assertGreater(len(conj), 0)
        for entry in conj:
            self.assertEqual(
                entry["region"],
                "aquitania",
                f"conjectural {entry['surface']!r} should be tagged "
                f"region=aquitania to be indistinguishable from real entries "
                f"to the candidate generator",
            )
            self.assertNotIn(
                "semantic_field",
                entry,
                f"conjectural entry {entry['surface']!r} should NOT carry a "
                f"semantic_field — conjecturals have no real-world semantics",
            )

    def test_surface_uniqueness(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        surfaces = [e["surface"] for e in polluted["entries"]]
        self.assertEqual(
            len(surfaces),
            len(set(surfaces)),
            f"polluted pool has duplicate surfaces: "
            f"{[s for s, c in Counter(surfaces).items() if c > 1]!r}",
        )
        real_surfaces = {
            e["surface"]
            for e in polluted["entries"]
            if e.get("provenance") == "real"
        }
        conj_surfaces = {
            e["surface"]
            for e in polluted["entries"]
            if e.get("provenance") == "conjectural"
        }
        self.assertFalse(
            real_surfaces & conj_surfaces,
            f"conjectural surfaces collided with real surfaces: "
            f"{real_surfaces & conj_surfaces!r}",
        )

    def test_length_distribution_is_double(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        sub_lens = Counter(len(e["phonemes"]) for e in self.substrate["entries"])
        pol_lens = Counter(len(e["phonemes"]) for e in polluted["entries"])
        for L, n in sub_lens.items():
            self.assertEqual(
                pol_lens[L],
                2 * n,
                f"length {L}: substrate has {n}, polluted should have {2 * n}, "
                f"actually has {pol_lens[L]}",
            )

    def test_conjectural_two_class_filter(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        conj = [e for e in polluted["entries"] if e.get("provenance") == "conjectural"]
        for entry in conj:
            self.assertTrue(
                _spans_two_classes(entry["phonemes"]),
                f"conjectural {entry['surface']!r} spans only "
                f"{({_phoneme_class(p) for p in entry['phonemes']})} — "
                f"the candidate generator would skip it",
            )

    def test_determinism_byte_identical(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        path = self.tmp / "polluted_aquitanian.yaml"
        first = path.read_bytes()
        path.unlink()
        build_polluted_pool("aquitanian", self.tmp)
        second = path.read_bytes()
        self.assertEqual(
            first,
            second,
            "polluted pool YAML must be byte-identical across rebuilds",
        )

    def test_schema_valid(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        polluted = self._load(self.tmp / "polluted_aquitanian.yaml")
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(polluted)

    def test_seed_distinct_from_control_seed(self) -> None:
        """Conjectural draws use a *different* seed than the matched-control
        builder so the two synthetic surface populations come from
        independent random streams."""
        import hashlib

        polluted_seed = _seed_for("aquitanian")
        control_seed = int(
            hashlib.sha256(b"control_pool:aquitanian").hexdigest()[:16], 16
        )
        self.assertNotEqual(
            polluted_seed,
            control_seed,
            "polluted-pool conjectural seed must not match the control-pool "
            "seed (otherwise the test artifact draws from the same RNG "
            "stream as its own control)",
        )

    def test_readme_renders_with_warning(self) -> None:
        build_polluted_pool("aquitanian", self.tmp)
        readme_path = write_readme("aquitanian", self.tmp)
        text = readme_path.read_text(encoding="utf-8")
        self.assertIn("polluted_aquitanian", text)
        self.assertIn("test artifact", text.lower())
        # The README's prominent warning must appear early so anyone
        # stumbling on the file sees the test-artifact disclaimer
        # before any technical content.
        warning_pos = text.lower().find("test artifact")
        algo_pos = text.find("Construction algorithm")
        self.assertLess(
            warning_pos,
            algo_pos,
            "the test-artifact warning must appear before the construction "
            "algorithm section, not after",
        )


class CommittedPollutedPoolTest(unittest.TestCase):
    """Sanity check on the committed ``pools/polluted_aquitanian.yaml``
    (only runs if the file exists)."""

    def test_committed_polluted_pool(self) -> None:
        path = _REPO_ROOT / "pools" / "polluted_aquitanian.yaml"
        if not path.exists():
            self.skipTest(f"{path} not built; run scripts/build_polluted_pool.py")
        polluted = yaml.safe_load(path.read_text(encoding="utf-8"))
        # 153 + 153 = 306
        self.assertEqual(
            len(polluted["entries"]), 306,
            "committed polluted_aquitanian must have 306 entries",
        )
        provenances = Counter(e.get("provenance") for e in polluted["entries"])
        self.assertEqual(provenances["real"], 153)
        self.assertEqual(provenances["conjectural"], 153)

        # No duplicate surfaces.
        surfaces = [e["surface"] for e in polluted["entries"]]
        self.assertEqual(len(surfaces), len(set(surfaces)))

        # Schema valid.
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(polluted)

        # Conjectural entries: region=aquitania, no semantic_field.
        for entry in polluted["entries"]:
            if entry.get("provenance") == "conjectural":
                self.assertEqual(entry["region"], "aquitania")
                self.assertNotIn("semantic_field", entry)


if __name__ == "__main__":
    unittest.main()
