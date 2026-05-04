"""Smoke tests for scripts/generate_signatures.py and
scripts/generate_signature_controls.py (mg-bef2, harness v9).

Exercises:
  * Greedy multi-root placement on a small toy corpus + pool.
  * Output-schema compliance.
  * Idempotence: re-running the generator produces byte-identical
    YAMLs and manifest entries.
  * Matched-control pairing: each substrate manifest row gets a
    control row whose paired_substrate_hash matches.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_GEN_PATH = _REPO_ROOT / "scripts" / "generate_signatures.py"
_GEN_CTRL_PATH = _REPO_ROOT / "scripts" / "generate_signature_controls.py"


# Small fixture corpus: two inscriptions where multi-root placements are
# possible. The pool below has roots `aa` (a, a) and `bbb` (b, b, b);
# tokens are encoded so the generator's greedy fill produces a 2-root
# signature on at least one record.
_FIXTURE_RECORDS = [
    {
        "id": "TOY 1",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        # 6-syllabogram inscription: aa-aa-aa - bbb-bbb (with DIV in middle).
        # First block aa,aa,aa -> places `aa` at [0,1] then `aa` at [2,3]
        # then `aa` at [4,5] (3 placements). Second block bbb,bbb -> places
        # `bbb` at [0..2] then `bbb` at [3..5] (2 placements).
        "tokens": ["AB01", "AB02", "AB01", "AB02", "AB01", "AB02"],
        "n_signs": 6,
        "n_words": 1,
        "raw_transliteration": "AB01-AB02",
        "source": "toy:test/TOY 1/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
    {
        "id": "TOY 2",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB01", "AB02", "DIV", "AB01", "AB02", "AB01", "AB02"],
        "n_signs": 6,
        "n_words": 2,
        "raw_transliteration": "AB01-AB02 / AB01-AB02-AB01-AB02",
        "source": "toy:test/TOY 2/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
]


_FIXTURE_POOL_YAML = """\
pool: testpool
source_citation: synthetic test pool
license: synthetic test pool
fetched_at: '2026-05-04T00:00:00Z'
entries:
  - surface: ab
    phonemes: [a, b]
    region: testregion
  - surface: aba
    phonemes: [a, b, a]
    region: testregion
"""


_FIXTURE_CONTROL_YAML = """\
pool: control_testpool
source_citation: synthetic test control
license: synthetic test pool
fetched_at: '2026-05-04T00:00:00Z'
entries:
  - surface: xy
    phonemes: [x, y]
    region: phonotactic_control_testpool
  - surface: yzx
    phonemes: [y, z, x]
    region: phonotactic_control_testpool
  - surface: pq
    phonemes: [p, q]
    region: phonotactic_control_testpool
"""


_POOL_SCHEMA = """\
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["pool", "entries"],
  "additionalProperties": true,
  "properties": {
    "pool": {"type": "string"},
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["surface", "phonemes"],
        "additionalProperties": true,
        "properties": {
          "surface": {"type": "string"},
          "phonemes": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
"""


def _set_up_fixture(tmp: Path) -> None:
    """Lay out a self-contained tree under ``tmp`` with corpus, pools,
    and an empty hypotheses dir."""
    (tmp / "corpus").mkdir(parents=True)
    with (tmp / "corpus" / "all.jsonl").open("w", encoding="utf-8") as fh:
        for rec in _FIXTURE_RECORDS:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    (tmp / "pools" / "schemas").mkdir(parents=True)
    (tmp / "pools" / "schemas" / "pool.v1.schema.json").write_text(
        _POOL_SCHEMA, encoding="utf-8"
    )
    (tmp / "pools" / "testpool.yaml").write_text(_FIXTURE_POOL_YAML, encoding="utf-8")
    (tmp / "pools" / "control_testpool.yaml").write_text(
        _FIXTURE_CONTROL_YAML, encoding="utf-8"
    )

    (tmp / "hypotheses" / "auto_signatures").mkdir(parents=True)


class SignatureGeneratorSmoke(unittest.TestCase):

    def test_generator_runs_and_emits_signatures(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _set_up_fixture(tmp)
            gen = _load_module("generate_signatures_under_test", _GEN_PATH)
            summary = gen.generate(
                pool_name="testpool",
                cap_per_inscription=5,
                cap_per_root_set=3,
                coverage_threshold=0.5,
                min_roots=2,
                window_lengths=(6, 8, 10),
                corpus_path=tmp / "corpus" / "all.jsonl",
                pools_dir=tmp / "pools",
                hypotheses_dir=tmp / "hypotheses" / "auto_signatures",
                progress=False,
                repo_root=tmp,
            )
            self.assertGreater(summary["candidates_emitted"], 0)
            manifest_path = tmp / summary["manifest_path"]
            with manifest_path.open("r", encoding="utf-8") as fh:
                rows = [json.loads(line) for line in fh if line.strip()]
            self.assertEqual(len(rows), summary["candidates_emitted"])

            # Each emitted signature has >= 2 roots and a coverage fraction
            # of >= 0.5.
            for row in rows:
                self.assertGreaterEqual(row["n_roots"], 2)
                self.assertGreaterEqual(row["coverage_fraction"], 0.5)
                hyp_path = tmp / row["hypothesis_path"]
                self.assertTrue(hyp_path.exists(), f"{hyp_path} missing")

    def test_generator_is_idempotent(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _set_up_fixture(tmp)
            gen = _load_module("generate_signatures_idem", _GEN_PATH)
            kwargs = dict(
                pool_name="testpool",
                cap_per_inscription=5,
                cap_per_root_set=3,
                coverage_threshold=0.5,
                min_roots=2,
                window_lengths=(6, 8, 10),
                corpus_path=tmp / "corpus" / "all.jsonl",
                pools_dir=tmp / "pools",
                hypotheses_dir=tmp / "hypotheses" / "auto_signatures",
                progress=False,
                repo_root=tmp,  # type: ignore[arg-type]
            )
            s1 = gen.generate(**kwargs)
            manifest_path = tmp / s1["manifest_path"]
            text1 = manifest_path.read_text(encoding="utf-8")
            yamls1 = sorted(
                (p, p.read_text(encoding="utf-8"))
                for p in (tmp / "hypotheses" / "auto_signatures" / "testpool").glob(
                    "*.yaml"
                )
            )
            # Re-run.
            s2 = gen.generate(**kwargs)
            text2 = manifest_path.read_text(encoding="utf-8")
            yamls2 = sorted(
                (p, p.read_text(encoding="utf-8"))
                for p in (tmp / "hypotheses" / "auto_signatures" / "testpool").glob(
                    "*.yaml"
                )
            )
            self.assertEqual(text1, text2)
            self.assertEqual(yamls1, yamls2)
            self.assertEqual(s1["candidates_emitted"], s2["candidates_emitted"])

    def test_control_pairing_one_to_one(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _set_up_fixture(tmp)
            gen = _load_module("gen_under_test_pairing", _GEN_PATH)
            ctrl = _load_module("gen_ctrl_under_test", _GEN_CTRL_PATH)
            sub_summary = gen.generate(
                pool_name="testpool",
                cap_per_inscription=5,
                cap_per_root_set=3,
                coverage_threshold=0.5,
                min_roots=2,
                window_lengths=(6, 8, 10),
                corpus_path=tmp / "corpus" / "all.jsonl",
                pools_dir=tmp / "pools",
                hypotheses_dir=tmp / "hypotheses" / "auto_signatures",
                progress=False,
                repo_root=tmp,
            )
            self.assertGreater(sub_summary["candidates_emitted"], 0)

            ctrl_summary = ctrl.generate(
                substrate_pool_name="testpool",
                pools_dir=tmp / "pools",
                corpus_path=tmp / "corpus" / "all.jsonl",
                hypotheses_dir=tmp / "hypotheses" / "auto_signatures",
                progress=False,
                repo_root=tmp,
            )
            self.assertEqual(
                ctrl_summary["substrate_signatures"],
                sub_summary["candidates_emitted"],
            )
            # Every emitted control points to a substrate hypothesis_hash.
            substrate_hashes = set()
            with (
                tmp / sub_summary["manifest_path"]
            ).open("r", encoding="utf-8") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    substrate_hashes.add(json.loads(line)["hypothesis_hash"])
            with (
                tmp / ctrl_summary["manifest_path"]
            ).open("r", encoding="utf-8") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    self.assertIn(row["paired_substrate_hash"], substrate_hashes)


if __name__ == "__main__":
    unittest.main()
