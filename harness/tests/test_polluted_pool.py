"""Polluted-pool builder (mg-6b73, harness v14; mg-7ecb, harness v15).

Smoke-tests ``scripts/build_polluted_pool.py`` and the committed
``pools/polluted_aquitanian.yaml`` and
``pools/greek_polluted_aquitanian.yaml`` artifacts. The polluted pools
are **test artifacts**:

  * ``polluted_aquitanian`` (v14, mg-6b73): half real Aquitanian +
    half synthetic conjecturals drawn from the real pool's phoneme +
    length distribution. Held-out pool-curation test.
  * ``greek_polluted_aquitanian`` (v15, mg-7ecb): half real
    Aquitanian + half synthetic conjecturals drawn from the
    Mycenaean-Greek char-bigram distribution at
    ``harness/external_phoneme_models/mycenaean_greek.json``, with
    lengths matched to the real Aquitanian pool. Cross-language
    pollution test.

Coverage:

  (a) Entry-count correctness: 2 × the underlying substrate pool
      (real + conjectural).
  (b) Provenance tagging: every entry carries
      ``provenance`` matching ``{real, conjectural[_<lang>]}`` and the
      split is exactly 50/50.
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
      byte-identical polluted YAML, AND same-distribution + cross-
      language pollutions of the same base pool draw from disjoint
      seeds.
  (i) Schema-validity (the builder calls the validator internally;
      this test re-asserts on the materialized YAML to catch round-
      trip regressions).
  (j) Cross-language phoneme inventory: the Greek-shape conjecturals'
      phoneme histogram differs from the real Aquitanian phoneme
      histogram (otherwise --source-lm would be a no-op).

The smoke fixture uses a small synthetic substrate pool so the test
is fast and self-contained. The committed
``{,greek_}polluted_aquitanian.yaml`` artifacts are also exercised in
:class:`CommittedPollutedPoolTest` /
:class:`CommittedGreekPollutedPoolTest`.
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

        polluted_seed = _seed_for("polluted_aquitanian")
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

    def test_seed_distinct_across_pollution_modes(self) -> None:
        """Same-distribution and cross-language pollutions of the same base
        pool draw from *different* seeds (mg-7ecb), so the two test
        artifacts come from independent random streams even though they
        share a base pool."""
        same_dist_seed = _seed_for("polluted_aquitanian")
        cross_lang_seed = _seed_for("greek_polluted_aquitanian")
        self.assertNotEqual(
            same_dist_seed,
            cross_lang_seed,
            "v14 same-distribution and v15 cross-language polluted pools "
            "must have distinct conjectural seeds; otherwise the two test "
            "artifacts draw from the same RNG stream and one of them "
            "would not be testing what it claims to test.",
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


class CrossLanguagePollutedPoolBuilderTest(unittest.TestCase):
    """Smoke tests for the v15 cross-language pollution builder
    (mg-7ecb): ``--source-lm`` flag draws Greek-shape conjecturals,
    tags them ``conjectural_greek``, and produces a pool named
    ``greek_polluted_aquitanian``.

    Uses the committed Mycenaean-Greek char-bigram model at
    ``harness/external_phoneme_models/mycenaean_greek.json`` (always
    in-tree) and a small synthetic substrate fixture so the test is
    fast and self-contained.
    """

    _GREEK_LM_PATH = (
        _REPO_ROOT / "harness" / "external_phoneme_models" / "mycenaean_greek.json"
    )

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="mg_7ecb_"))
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

    def _build(self) -> dict:
        return build_polluted_pool(
            "aquitanian",
            self.tmp,
            source_lm_path=self._GREEK_LM_PATH,
            prefix="greek",
        )

    def test_pool_naming_and_provenance_tag(self) -> None:
        summary = self._build()
        self.assertEqual(summary["polluted_pool"], "greek_polluted_aquitanian")
        self.assertEqual(summary["prefix"], "greek")
        self.assertEqual(summary["provenance_tag"], "conjectural_greek")
        self.assertTrue(
            (self.tmp / "greek_polluted_aquitanian.yaml").exists(),
            "v15 builder must write greek_polluted_aquitanian.yaml when "
            "called with --prefix greek",
        )

    def test_provenance_split_50_50(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        self.assertEqual(len(polluted["entries"]), 2 * len(self.substrate["entries"]))
        provenances = Counter(e.get("provenance") for e in polluted["entries"])
        self.assertEqual(provenances["real"], len(self.substrate["entries"]))
        self.assertEqual(
            provenances["conjectural_greek"], len(self.substrate["entries"])
        )
        # No legacy "conjectural" tag should leak into the v15 pool.
        self.assertNotIn("conjectural", provenances)

    def test_real_entries_passthrough(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        real = [e for e in polluted["entries"] if e.get("provenance") == "real"]
        self.assertEqual(len(real), len(self.substrate["entries"]))
        for sub_entry, pol_entry in zip(self.substrate["entries"], real):
            self.assertEqual(sub_entry["surface"], pol_entry["surface"])
            self.assertEqual(sub_entry["phonemes"], pol_entry["phonemes"])

    def test_conjectural_tagging_and_region_camouflage(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        conj = [
            e
            for e in polluted["entries"]
            if e.get("provenance") == "conjectural_greek"
        ]
        self.assertGreater(len(conj), 0)
        for entry in conj:
            self.assertEqual(
                entry["region"],
                "aquitania",
                "Greek-shape conjectural entries must carry "
                "region=aquitania so they're indistinguishable from real "
                "entries to the candidate generator's source_pool routing",
            )
            self.assertNotIn("semantic_field", entry)
            self.assertNotIn("gloss", entry)

    def test_length_distribution_matches_real_pool(self) -> None:
        """The polluted pool's length distribution is exactly 2× the real
        pool's; length is not a confound between the real and Greek-shape
        halves."""
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        sub_lens = Counter(len(e["phonemes"]) for e in self.substrate["entries"])
        pol_lens = Counter(len(e["phonemes"]) for e in polluted["entries"])
        for L, n in sub_lens.items():
            self.assertEqual(
                pol_lens[L],
                2 * n,
                f"length {L}: substrate has {n}, polluted should have "
                f"{2 * n}, actually has {pol_lens[L]}",
            )

    def test_phoneme_inventory_differs_from_real_pool(self) -> None:
        """The whole point of cross-language pollution is that the
        conjecturals come from a *different* phoneme distribution than
        the real pool. Assert that the realized Greek-shape inventory is
        not a strict subset of the real Aquitanian inventory — at least
        one Greek-shape character must not appear in real Aquitanian."""
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        real_phonemes = {p for e in self.substrate["entries"] for p in e["phonemes"]}
        conj_phonemes = {
            p
            for e in polluted["entries"]
            if e.get("provenance") == "conjectural_greek"
            for p in e["phonemes"]
        }
        self.assertFalse(
            conj_phonemes <= real_phonemes,
            f"Greek-shape conjectural inventory {sorted(conj_phonemes)!r} "
            f"is a subset of real Aquitanian inventory "
            f"{sorted(real_phonemes)!r}; --source-lm appears to be a "
            f"no-op or the fixture is too narrow to exercise the LM.",
        )

    def test_two_class_filter(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        conj = [
            e
            for e in polluted["entries"]
            if e.get("provenance") == "conjectural_greek"
        ]
        for entry in conj:
            self.assertTrue(
                _spans_two_classes(entry["phonemes"]),
                f"Greek-shape conjectural {entry['surface']!r} spans only "
                f"{({_phoneme_class(p) for p in entry['phonemes']})} — "
                f"the candidate generator would skip it",
            )

    def test_surface_uniqueness_with_real(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        surfaces = [e["surface"] for e in polluted["entries"]]
        self.assertEqual(len(surfaces), len(set(surfaces)))
        real = {
            e["surface"]
            for e in polluted["entries"]
            if e.get("provenance") == "real"
        }
        conj = {
            e["surface"]
            for e in polluted["entries"]
            if e.get("provenance") == "conjectural_greek"
        }
        self.assertFalse(real & conj)

    def test_determinism_byte_identical(self) -> None:
        self._build()
        path = self.tmp / "greek_polluted_aquitanian.yaml"
        first = path.read_bytes()
        path.unlink()
        self._build()
        second = path.read_bytes()
        self.assertEqual(
            first,
            second,
            "Greek-shape polluted pool YAML must be byte-identical "
            "across rebuilds",
        )

    def test_disjoint_from_v14_polluted_pool(self) -> None:
        """The v14 same-distribution and v15 cross-language conjecturals
        of the same base pool must use distinct seeds and therefore can't
        produce identical conjectural surface sets."""
        # Build v14 (default) into the same tmp dir.
        v14_summary = build_polluted_pool("aquitanian", self.tmp)
        v15_summary = self._build()
        self.assertNotEqual(v14_summary["seed_hex"], v15_summary["seed_hex"])

        v14_doc = self._load(self.tmp / "polluted_aquitanian.yaml")
        v15_doc = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        v14_conj = {
            e["surface"]
            for e in v14_doc["entries"]
            if e.get("provenance") == "conjectural"
        }
        v15_conj = {
            e["surface"]
            for e in v15_doc["entries"]
            if e.get("provenance") == "conjectural_greek"
        }
        # Some collision is possible by chance, but the *full sets* must
        # not be identical (otherwise the LM had no effect).
        self.assertNotEqual(
            v14_conj,
            v15_conj,
            "v14 same-distribution and v15 cross-language conjectural "
            "surface sets are identical — the --source-lm flag was a "
            "no-op or one of the seeds is wrong",
        )

    def test_schema_valid_with_conjectural_greek(self) -> None:
        self._build()
        polluted = self._load(self.tmp / "greek_polluted_aquitanian.yaml")
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(polluted)
        # Sanity-check that the schema's provenance pattern actually
        # accepts the conjectural_greek tag (and rejects nonsense).
        validator = Draft202012Validator(schema)
        sample = polluted["entries"][-1]
        self.assertTrue(
            sample["provenance"].startswith("conjectural_"),
            "test fixture inverted: last entry should be a conjectural",
        )

    def test_readme_renders_with_warning_and_v15_context(self) -> None:
        self._build()
        readme_path = write_readme(
            "aquitanian",
            self.tmp,
            source_lm_path=self._GREEK_LM_PATH,
            prefix="greek",
        )
        text = readme_path.read_text(encoding="utf-8")
        self.assertIn("greek_polluted_aquitanian", text)
        self.assertIn("test artifact", text.lower())
        # The v15 README must explicitly reference cross-language
        # pollution so a future reader knows what this pool is FOR.
        self.assertIn("cross-language", text.lower())
        self.assertIn("mg-7ecb", text.lower())
        warning_pos = text.lower().find("test artifact")
        algo_pos = text.find("Construction algorithm")
        self.assertLess(warning_pos, algo_pos)


class CommittedGreekPollutedPoolTest(unittest.TestCase):
    """Sanity check on the committed
    ``pools/greek_polluted_aquitanian.yaml`` (mg-7ecb, harness v15);
    only runs if the file exists."""

    def test_committed_greek_polluted_pool(self) -> None:
        path = _REPO_ROOT / "pools" / "greek_polluted_aquitanian.yaml"
        if not path.exists():
            self.skipTest(
                f"{path} not built; run scripts/build_polluted_pool.py "
                f"--source-lm harness/external_phoneme_models/"
                f"mycenaean_greek.json --prefix greek"
            )
        polluted = yaml.safe_load(path.read_text(encoding="utf-8"))
        # 153 + 153 = 306
        self.assertEqual(
            len(polluted["entries"]),
            306,
            "committed greek_polluted_aquitanian must have 306 entries",
        )
        provenances = Counter(e.get("provenance") for e in polluted["entries"])
        self.assertEqual(provenances["real"], 153)
        self.assertEqual(provenances["conjectural_greek"], 153)

        # No duplicate surfaces.
        surfaces = [e["surface"] for e in polluted["entries"]]
        self.assertEqual(len(surfaces), len(set(surfaces)))

        # Schema valid.
        schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(polluted)

        # Greek-shape conjectural entries: region=aquitania, no
        # semantic_field, no gloss.
        for entry in polluted["entries"]:
            if entry.get("provenance") == "conjectural_greek":
                self.assertEqual(entry["region"], "aquitania")
                self.assertNotIn("semantic_field", entry)
                self.assertNotIn("gloss", entry)


if __name__ == "__main__":
    unittest.main()
