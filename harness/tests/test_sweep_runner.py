"""Smoke test for the bulk candidate generator + sweep runner on a 5-record
toy corpus and a 3-entry toy pool.

Asserts:
  * Generator is deterministic: two back-to-back runs produce byte-identical
    YAML files and a byte-identical manifest.
  * Sweep runner is deterministic: the per-row ``score`` and
    ``score_control_z`` are identical across runs (only ``run_id`` and
    ``ran_at`` are allowed to differ).
  * Sweep runner is resumable: a second run with the same corpus and result
    stream scores zero new rows and skips every manifest entry.
  * Generator skip rules fire as documented:
      - single-phoneme-class pool entries are dropped
      - fragmentary inscriptions are dropped
      - DIV-crossing windows are dropped
      - duplicate-sign windows are dropped

Run directly:
  python3 -m harness.tests.test_sweep_runner
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

# scripts/ is not a package; insert the repo root so we can import the
# generator and sweep modules by file path.
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import generate_candidates  # noqa: E402  (path-dependent import)
import run_sweep  # noqa: E402


_FIXTURE_RECORDS = [
    {
        "id": "TOY 1",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB54", "AB02", "AB81", "DIV", "AB54", "AB80", "AB02"],
        "n_signs": 6,
        "n_words": 2,
        "raw_transliteration": "AB54-AB02-AB81 / AB54-AB80-AB02",
        "source": "toy:test/TOY 1/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
    {
        "id": "TOY 2",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB54", "AB80", "AB02"],
        "n_signs": 3,
        "n_words": 1,
        "raw_transliteration": "AB54-AB80-AB02",
        "source": "toy:test/TOY 2/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
    {
        "id": "TOY 3",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB02", "AB54"],
        "n_signs": 2,
        "n_words": 1,
        "raw_transliteration": "AB02-AB54",
        "source": "toy:test/TOY 3/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
    {
        "id": "TOY 4",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "fragmentary",
        "tokens": ["AB54", "AB02", "AB81"],
        "n_signs": 3,
        "n_words": 1,
        "raw_transliteration": "AB54-AB02-AB81",
        "source": "toy:test/TOY 4/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
    {
        "id": "TOY 5",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB54", "AB54", "DIV", "AB02", "AB80"],
        "n_signs": 4,
        "n_words": 2,
        "raw_transliteration": "AB54-AB54 / AB02-AB80",
        "source": "toy:test/TOY 5/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
]


# 3 toy pool entries:
#   ko    — 2 phonemes, classes C+V (ok)
#   bere  — 4 phonemes, classes C+V+S (ok); cf. modern Basque "his"
#   aaa   — 3 phonemes, all class V (single-class — generator must skip)
_TOY_POOL_YAML = """\
pool: toy_pool
source_citation: |
  Synthetic test fixture for harness/tests/test_sweep_runner.py.
license: synthetic, no real source
fetched_at: "2026-05-04T00:00:00Z"
entries:
  - surface: ko
    phonemes: [k, o]
    gloss: synthetic CV
    semantic_field: synthetic
    region: synthetic
    citation: synthetic
  - surface: bere
    phonemes: [b, e, r, e]
    gloss: synthetic 4-phoneme
    semantic_field: synthetic
    region: synthetic
    citation: synthetic
  - surface: aaa
    phonemes: [a, a, a]
    gloss: single-class (must be skipped)
    semantic_field: synthetic
    region: synthetic
    citation: synthetic
"""


class SweepRunnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="lineara-sweep-"))
        # Toy corpus.
        self.corpus_dir = self.tmp / "corpus"
        self.corpus_dir.mkdir()
        self.corpus_path = self.corpus_dir / "all.jsonl"
        with self.corpus_path.open("w", encoding="utf-8") as fh:
            for rec in _FIXTURE_RECORDS:
                fh.write(json.dumps(rec) + "\n")
        # Toy pool.
        self.pools_dir = self.tmp / "pools"
        (self.pools_dir / "schemas").mkdir(parents=True)
        # Reuse the real pool schema so the test fixture validates against
        # production rules, not a custom test schema.
        shutil.copy(
            _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json",
            self.pools_dir / "schemas" / "pool.v1.schema.json",
        )
        (self.pools_dir / "toy_pool.yaml").write_text(_TOY_POOL_YAML, encoding="utf-8")
        self.hypotheses_dir = self.tmp / "hypotheses" / "auto"
        self.results_path = self.tmp / "results" / "experiments.jsonl"

        # Patch the generator's pool-schema constant to point at our copy. The
        # generator resolves the schema relative to the pools_dir argument we
        # pass it, so this is the cleanest way to run it inside a tempdir.
        self._orig_schema_path = generate_candidates._POOL_SCHEMA_PATH
        generate_candidates._POOL_SCHEMA_PATH = (
            self.pools_dir / "schemas" / "pool.v1.schema.json"
        )
        # The generator records repo-relative paths; redirect its repo root
        # to our tempdir so the manifest is self-consistent.
        self._orig_repo_root = generate_candidates._REPO_ROOT
        generate_candidates._REPO_ROOT = self.tmp

    def tearDown(self) -> None:
        generate_candidates._POOL_SCHEMA_PATH = self._orig_schema_path
        generate_candidates._REPO_ROOT = self._orig_repo_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _generate(self) -> dict:
        return generate_candidates.generate(
            pool_name="toy_pool",
            cap_per_entry=50,
            corpus_path=self.corpus_path,
            pools_dir=self.pools_dir,
            hypotheses_dir=self.hypotheses_dir,
            progress=False,
        )

    def _sweep(self, note: str = "test") -> dict:
        manifest = self.hypotheses_dir / "toy_pool.manifest.jsonl"
        return run_sweep.run(
            manifest_path=manifest,
            corpus_path=self.corpus_path,
            results_path=self.results_path,
            note=note,
            progress_every=0,
            repo_root=self.tmp,
            pools_dir=self.pools_dir,
        )

    def _read_yaml_dir(self) -> dict[str, str]:
        d = self.hypotheses_dir / "toy_pool"
        if not d.exists():
            return {}
        return {p.name: p.read_text(encoding="utf-8") for p in sorted(d.glob("*.yaml"))}

    def _read_manifest(self) -> str:
        return (self.hypotheses_dir / "toy_pool.manifest.jsonl").read_text(encoding="utf-8")

    def _read_results(self) -> list[dict]:
        if not self.results_path.exists():
            return []
        with self.results_path.open("r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def test_generator_skip_rules_fire(self) -> None:
        summary = self._generate()
        # The single-class entry "aaa" must have been skipped.
        self.assertEqual(summary["skipped_single_class_entries"], 1)
        # Some candidates must have been emitted from the other two entries.
        self.assertGreater(summary["candidates_emitted"], 0)

        # Inspect the manifest: no entry should reference TOY 4 (fragmentary)
        # and no equation should pick a span with a duplicate sign.
        with (self.hypotheses_dir / "toy_pool.manifest.jsonl").open() as fh:
            manifest = [json.loads(l) for l in fh if l.strip()]
        for row in manifest:
            self.assertNotEqual(row["inscription_id"], "TOY 4")
        # TOY 5 has [AB54, AB54] which shares the only 2-syllabogram window in
        # its first block; that window has duplicate AB54 and must be dropped
        # for the 2-phoneme "ko" entry. The valid 2-phon window in TOY 5 is
        # [AB02, AB80] from the second block.
        toy5_ko = [
            r for r in manifest
            if r["inscription_id"] == "TOY 5" and r["pool_entry_surface"] == "ko"
        ]
        for r in toy5_ko:
            self.assertEqual([r["span_start"], r["span_end"]], [3, 4])

    def test_generator_is_deterministic(self) -> None:
        first_summary = self._generate()
        first_yaml = self._read_yaml_dir()
        first_manifest = self._read_manifest()

        second_summary = self._generate()
        second_yaml = self._read_yaml_dir()
        second_manifest = self._read_manifest()

        # Re-running on the same pool + corpus must produce the same manifest
        # bytes and the same set of YAMLs with identical content.
        self.assertEqual(first_summary["candidates_emitted"], second_summary["candidates_emitted"])
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(set(first_yaml), set(second_yaml))
        for name, body in first_yaml.items():
            self.assertEqual(body, second_yaml[name], f"YAML drift on {name}")

    def test_sweep_runner_resumable_and_deterministic(self) -> None:
        self._generate()
        first = self._sweep(note="first")
        first_rows = self._read_results()
        self.assertGreater(first["scored"], 0)
        self.assertEqual(first["skipped_resumed"], 0)
        self.assertEqual(len(first_rows), first["scored"])

        # Re-run: every manifest entry should be skipped now.
        second = self._sweep(note="second")
        second_rows = self._read_results()
        self.assertEqual(second["scored"], 0)
        self.assertEqual(second["skipped_resumed"], first["scored"])
        self.assertEqual(len(second_rows), len(first_rows))  # nothing appended

        # Drop the result stream and rerun from scratch — scores must be
        # byte-identical to the first sweep on a per-hypothesis basis.
        self.results_path.unlink()
        self._sweep(note="third")
        third_rows = self._read_results()
        self.assertEqual(len(third_rows), len(first_rows))
        first_by_hash = {r["hypothesis_hash"]: r for r in first_rows}
        third_by_hash = {r["hypothesis_hash"]: r for r in third_rows}
        self.assertEqual(set(first_by_hash), set(third_by_hash))
        for h, r1 in first_by_hash.items():
            r3 = third_by_hash[h]
            self.assertEqual(r1["score"], r3["score"])
            self.assertEqual(r1["score_control_z"], r3["score_control_z"])
            self.assertEqual(r1["metric"], "local_fit_v0")
            self.assertEqual(r3["metric"], "local_fit_v0")
            self.assertEqual(r1["corpus_snapshot"], r3["corpus_snapshot"])
            # run_id and ran_at are expected to differ between runs.
            self.assertNotEqual(r1["run_id"], r3["run_id"])

    def test_manifest_sort_order(self) -> None:
        self._generate()
        with (self.hypotheses_dir / "toy_pool.manifest.jsonl").open() as fh:
            manifest = [json.loads(l) for l in fh if l.strip()]
        # Manifest must be sorted by (pool_entry_index, inscription_id, span_start)
        keys = [(r["pool_entry_index"], r["inscription_id"], r["span_start"]) for r in manifest]
        self.assertEqual(keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
