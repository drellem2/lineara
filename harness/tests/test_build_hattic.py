"""Hattic corpus + pool builders (mg-7e7d6, specificity probe).

Asserts the normalisation contract documented in
``corpora/hattic.README.md``, that the committed corpus / pool are
reproducible from the build scripts, and that the pool carries only
real (non-conjectural) entries.

Run directly:
  python3 -m harness.tests.test_build_hattic
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from scripts import build_hattic_corpus as corpus_mod  # noqa: E402
from scripts import build_hattic_pool as pool_mod  # noqa: E402


class NormaliseTest(unittest.TestCase):
    def test_diacritics_and_sibilant_merge(self) -> None:
        self.assertEqual(corpus_mod.normalise("Ḫalmašuit"), "halmasuit")
        self.assertEqual(corpus_mod.normalise("Eštan"), "estan")

    def test_hyphens_dropped_and_voicing_merged(self) -> None:
        self.assertEqual(corpus_mod.normalise("le-binu"), "lepinu")
        self.assertEqual(corpus_mod.normalise("windu"), "wintu")
        self.assertEqual(corpus_mod.normalise("fur"), "wur")

    def test_plene_collapsed_gemination_kept(self) -> None:
        self.assertEqual(corpus_mod.normalise("ka-a-at-te"), "katte")
        self.assertEqual(corpus_mod.normalise("Mezulla"), "mezulla")


class CommittedCorpusTest(unittest.TestCase):
    def test_corpus_rebuild_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            corpus_mod.main(["--out-dir", tmp])
            self.assertEqual(
                (Path(tmp) / "all.jsonl").read_bytes(),
                (_REPO_ROOT / "corpora" / "hattic" / "all.jsonl").read_bytes(),
            )

    def test_every_record_is_cited_and_tiered(self) -> None:
        for rec in corpus_mod.all_records():
            self.assertIn(rec["tier"], ("A", "B"))
            self.assertTrue(rec["source_citation"])
            self.assertTrue(rec["words"], rec["name"])


class CommittedPoolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pool_path = _REPO_ROOT / "pools" / "hattic.yaml"
        self.pool = yaml.safe_load(self.pool_path.read_text(encoding="utf-8"))

    def test_schema_valid(self) -> None:
        schema = json.loads(
            (_REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(self.pool)

    def test_pool_rebuild_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "hattic.yaml"
            pool_mod.main(["--out", str(out)])
            self.assertEqual(out.read_bytes(), self.pool_path.read_bytes())

    def test_no_conjectural_padding(self) -> None:
        for e in self.pool["entries"]:
            self.assertEqual(e["provenance"], "real")
            self.assertEqual(e["region"], "central_anatolia")
            self.assertEqual("".join(e["phonemes"]), e["surface"])

    def test_surfaces_match_lm_corpus_words(self) -> None:
        # Same normalisation for corpus and pool: every pool surface is
        # a corpus word form.
        words = {
            w for r in corpus_mod.all_records() for w in r["words"]
        }
        for e in self.pool["entries"]:
            self.assertIn(e["surface"], words)


if __name__ == "__main__":
    unittest.main()
