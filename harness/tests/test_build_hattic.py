"""Hattic corpus + pool builders (mg-7e7d6; rebuilt from sources, mg-7f4db).

Asserts the normalisation contract documented in
``corpora/hattic.README.md``, that the committed corpus / pool are
reproducible from the committed source files, that every pool entry is
a page-cited form from a viewed edition, and that the LM corpus is not
the pool (the v32 circularity).

The quotes in ``corpora/hattic/sources/lexicon.tsv`` are checked against
the scans by ``scripts/verify_hattic_sources.py`` (needs network; not run
here).

Run directly:
  python3 -m harness.tests.test_build_hattic
"""

from __future__ import annotations

import csv
import json
import re
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
from scripts import extract_tlhdig_hattic as extract_mod  # noqa: E402

_LEXICON = _REPO_ROOT / "corpora" / "hattic" / "sources" / "lexicon.tsv"
_POOL = _REPO_ROOT / "pools" / "hattic.yaml"


class NormaliseTest(unittest.TestCase):
    def test_diacritics_and_sibilant_merge(self) -> None:
        self.assertEqual(corpus_mod.normalise("Ḫalmašuit"), "halmasuit")
        self.assertEqual(corpus_mod.normalise("Eštan"), "estan")
        self.assertEqual(corpus_mod.normalise("šu-ú-wa"), "suwa")

    def test_hyphens_dropped_and_voicing_merged(self) -> None:
        self.assertEqual(corpus_mod.normalise("le-binu"), "lepinu")
        self.assertEqual(corpus_mod.normalise("windu"), "wintu")
        self.assertEqual(corpus_mod.normalise("fur"), "wur")

    def test_plene_collapsed_gemination_kept(self) -> None:
        self.assertEqual(corpus_mod.normalise("ka-a-at-te"), "katte")
        self.assertEqual(corpus_mod.normalise("Mezulla"), "mezulla")

    def test_bound_transcription(self) -> None:
        # mg-7f4db: u̯ → w, i̯ → i, Schuster's v → w, subscripts dropped.
        self.assertEqual(corpus_mod.normalise("kuu̯a"), "kuwa")
        self.assertEqual(corpus_mod.normalise("šuu̯aₐ"), "suwa")
        self.assertEqual(corpus_mod.normalise("U̯uᵤrun-šemu"), "wurunsemu")
        self.assertEqual(corpus_mod.normalise("taḫai̯a"), "tahaia")
        self.assertEqual(corpus_mod.normalise("vae"), "wae")
        # The edition's bound form and TLHdig's syllabic spelling meet.
        self.assertEqual(
            corpus_mod.normalise("ḫanu̯aₐšuit"),
            corpus_mod.normalise("ḫa-an-wa-šu-it"),
        )


class ExtractTest(unittest.TestCase):
    """The TLHdig extractor on hand-made XML in TLHdig's markup."""

    _XML = (
        '<AOxml><AOHeader><docID>KUB 99.1</docID></AOHeader><body>'
        '<lb lnr="1" lg="Hattian"/> <w>ka-a-at-te</w> <w>ta-<del_in/>ba</w> '
        '<lb lnr="2" lg="Hattian"/> <w>ar<del_fin/>-na</w> <w>pí-i-ip</w> '
        '<w lg="Hit"><sGr>LUGAL</sGr></w> '
        '<lb lnr="3" lg="Hit"/> <w>nu</w> <w lg="Hat"><d>D</d>ta-ru</w> '
        '<w lg="Hat">ša-<laes_in/>ak<laes_fin/>-tu-nu</w> <w lg="Hat">-ḫu</w> '
        '<lb lnr="4" lg="Hit"/> <w>ma-a-an</w> '
        '</body></AOxml>'
    )

    def test_lines_languages_and_breaks(self) -> None:
        rows = extract_mod.extract_document(self._XML)
        self.assertEqual([r[1] for r in rows], ["1", "2", "3"])
        intact = {r[1]: r[3] for r in rows}
        # A break inside a word, and one carried across the line end,
        # both make the word not intact.
        self.assertEqual(intact["1"], ["ka-a-at-te"])
        self.assertEqual(intact["2"], ["pí-i-ip"])
        # Word-level lg overrides the line; determinative and damage
        # marks dropped; a fragment ("-ḫu") is not intact.
        self.assertEqual(intact["3"], ["ta-ru", "ša-ak-tu-nu"])
        self.assertEqual(rows[0][0], "KUB 99.1")


class CommittedCorpusTest(unittest.TestCase):
    def test_corpus_rebuild_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            corpus_mod.main(["--out-dir", tmp])
            self.assertEqual(
                (Path(tmp) / "all.jsonl").read_bytes(),
                (_REPO_ROOT / "corpora" / "hattic" / "all.jsonl").read_bytes(),
            )

    def test_every_record_is_tlhdig_with_line_refs(self) -> None:
        records = corpus_mod.all_records()
        self.assertGreater(len(records), 300)
        for rec in records:
            self.assertIn("10.5281/zenodo.15459134", rec["source_citation"])
            self.assertTrue(rec["manuscript"])
            self.assertTrue(re.fullmatch(r"\d+(\.\d+)?", rec["cth"]))
            self.assertTrue(rec["words"])
            for line in rec["lines"]:
                self.assertTrue(line["line"])
            self.assertEqual(rec["words"], [w for ln in rec["lines"] for w in ln["words"]])

    def test_running_text_size(self) -> None:
        words = [w for r in corpus_mod.all_records() for w in r["words"]]
        self.assertGreater(len(words), 3000)
        self.assertGreater(len(set(words)), 1500)


class LexiconTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = pool_mod.load_lexicon(_LEXICON)

    def test_every_row_has_page_leaf_and_quote(self) -> None:
        for r in self.rows:
            self.assertIn(r["source"], pool_mod.SOURCES)
            self.assertGreater(int(r["page"]), 0)
            self.assertGreaterEqual(int(r["leaf"]), 0)
            self.assertGreaterEqual(len(r["quote"].strip()), 4, r)

    def test_scan_leaf_offsets(self) -> None:
        # Kammenhuber's Hattic chapter sits at a constant leaf offset in
        # the IA scan (verified page by page by verify_hattic_sources).
        for r in self.rows:
            if r["source"] == "kammenhuber1969":
                self.assertEqual(int(r["leaf"]) - int(r["page"]), 15, r)

    def test_lexemes_group_cleanly(self) -> None:
        lex = pool_mod.group_lexemes(self.rows)
        self.assertEqual(len(lex), 125)


class CommittedPoolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pool = yaml.safe_load(_POOL.read_text(encoding="utf-8"))

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
            self.assertEqual(out.read_bytes(), _POOL.read_bytes())

    def test_every_entry_real_and_page_cited(self) -> None:
        self.assertEqual(len(self.pool["entries"]), 124)
        for e in self.pool["entries"]:
            self.assertEqual(e["provenance"], "real")
            self.assertEqual(e["region"], "central_anatolia")
            self.assertEqual("".join(e["phonemes"]), e["surface"])
            self.assertRegex(
                e["citation"],
                r"^(Kammenhuber 1969|Schuster 1974), p\. \d+, "
                r"https://archive\.org/details/[\w-]+/page/n\d+",
            )
            self.assertIn("OCR quote:", e["notes"])

    def test_lm_corpus_is_not_the_pool(self) -> None:
        # v32's LM corpus was the pool. Now the LM is TLHdig running
        # text: it shares some forms with the pool (it is the same
        # language) but is not the pool. Numbers pinned in the README.
        surfaces = {e["surface"] for e in self.pool["entries"]}
        tokens = [w for r in corpus_mod.all_records() for w in r["words"]]
        types = set(tokens)
        self.assertEqual(len(surfaces & types), 56)
        self.assertEqual(sum(1 for w in tokens if w in surfaces), 291)
        self.assertLess(len(surfaces & types), len(surfaces))
        self.assertLess(len(surfaces & types) / len(types), 0.05)

    def test_lexicon_and_pool_agree(self) -> None:
        with _LEXICON.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
        keyed = {corpus_mod.normalise(r["keyed"]) for r in rows}
        self.assertTrue({e["surface"] for e in self.pool["entries"]} <= keyed)


if __name__ == "__main__":
    unittest.main()
