"""Schema + smoke tests for the Cretan Hieroglyphic corpus (mg-99df, chic-v0).

Validates the per-inscription record shape and exercises a 5-record
sample drawn from the four corners of CHIC's catalog:
  - #001  (Knossos crescent, the canonical first entry)
  - #070  (Mallia cone, classic MA/M Quartier Mu inscription)
  - #118  (Mallia bar, longest administrative document, NUM tokens)
  - #225  (Crete sealstone, sealstone-style entry from SealsImps)
  - #331  (final Chamaizi vase entry, post-CHIC misc addition)

Run directly:
  python3 -m harness.tests.test_chic_corpus
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
_CHIC_DIR = _REPO_ROOT / "corpora" / "cretan_hieroglyphic"
_INSCRIPTIONS_DIR = _CHIC_DIR / "inscriptions"
_ALL_JSONL = _CHIC_DIR / "all.jsonl"

# CHIC v0 schema (encoded inline; a stand-alone JSON Schema for CHIC will
# land with chic-v1 once tokenization is finalised).
REQUIRED_FIELDS = {
    "id",
    "site",
    "support",
    "period",
    "transcription_confidence",
    "tokens",
    "raw_transliteration",
    "source",
    "source_citation",
    "fetched_at",
}
ALLOWED_CONFIDENCE = {"clean", "partial", "fragmentary"}
ALLOWED_SOURCES = {"younger_online", "olivier_godart_1996", "damos", "liber"}
TOKEN_RE = re.compile(
    r"^(?:#\d{3}|\[\?:#\d{3}\]|\[\?\]|NUM:\d+|DIV)$"
)
ID_RE = re.compile(r"^CHIC #\d{3}$")
ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# 5-record smoke sample.
SMOKE_IDS = ["CHIC #001", "CHIC #070", "CHIC #118", "CHIC #225", "CHIC #331"]


def _load_record(chic_num: int) -> dict:
    path = _INSCRIPTIONS_DIR / f"{chic_num:03d}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_aggregate() -> list[dict]:
    return [
        json.loads(line)
        for line in _ALL_JSONL.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TestChicCorpusSchema(unittest.TestCase):
    """Per-record schema validation across the entire corpus."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _ALL_JSONL.exists():
            raise unittest.SkipTest(
                "corpora/cretan_hieroglyphic/all.jsonl not built; "
                "run scripts/build_chic_corpus.py first"
            )
        cls.records = _load_aggregate()

    def test_corpus_size_meets_acceptance(self) -> None:
        """Ticket asks for >= 250 inscriptions; we should clear it."""
        self.assertGreaterEqual(
            len(self.records),
            250,
            "chic-v0 acceptance criterion: >=250 inscriptions",
        )

    def test_required_fields_present(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec.get("id")):
                missing = REQUIRED_FIELDS - set(rec.keys())
                self.assertFalse(
                    missing,
                    f"missing fields in {rec.get('id')}: {sorted(missing)}",
                )

    def test_id_format(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertRegex(rec["id"], ID_RE)

    def test_ids_unique(self) -> None:
        ids = [r["id"] for r in self.records]
        self.assertEqual(
            len(ids), len(set(ids)),
            "duplicate CHIC ids in the corpus",
        )

    def test_ids_sorted_in_aggregate(self) -> None:
        ids = [r["id"] for r in self.records]
        self.assertEqual(
            ids, sorted(ids),
            "all.jsonl is not sorted by CHIC id",
        )

    def test_confidence_enum(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertIn(
                    rec["transcription_confidence"], ALLOWED_CONFIDENCE
                )

    def test_source_enum(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertIn(rec["source"], ALLOWED_SOURCES)

    def test_period_is_string_or_null(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertTrue(
                    rec["period"] is None
                    or isinstance(rec["period"], str)
                )

    def test_fetched_at_iso8601(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertRegex(rec["fetched_at"], ISO8601_RE)

    def test_token_grammar(self) -> None:
        for rec in self.records:
            for tok in rec["tokens"]:
                with self.subTest(id=rec["id"], token=tok):
                    self.assertRegex(
                        tok, TOKEN_RE,
                        f"unrecognized token shape in {rec['id']}: {tok!r}",
                    )

    def test_no_empty_token_streams(self) -> None:
        """Every committed inscription has at least one token."""
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                self.assertGreater(len(rec["tokens"]), 0)

    def test_no_consecutive_dividers(self) -> None:
        """A `DIV DIV` pair is a tokenizer bug — collapse word boundaries."""
        for rec in self.records:
            for i in range(1, len(rec["tokens"])):
                if rec["tokens"][i] == "DIV":
                    with self.subTest(id=rec["id"], pos=i):
                        self.assertNotEqual(
                            rec["tokens"][i - 1], "DIV",
                            f"consecutive DIVs at {rec['id']} pos {i}",
                        )

    def test_no_leading_or_trailing_divider(self) -> None:
        for rec in self.records:
            with self.subTest(id=rec["id"]):
                if rec["tokens"]:
                    self.assertNotEqual(rec["tokens"][0], "DIV")
                    self.assertNotEqual(rec["tokens"][-1], "DIV")

    def test_per_inscription_files_round_trip(self) -> None:
        """Aggregate matches per-inscription JSON files byte-for-byte."""
        per_file: dict[str, dict] = {}
        for path in sorted(_INSCRIPTIONS_DIR.glob("*.json")):
            rec = json.loads(path.read_text(encoding="utf-8"))
            per_file[rec["id"]] = rec
        agg_by_id = {r["id"]: r for r in self.records}
        self.assertEqual(
            sorted(per_file.keys()),
            sorted(agg_by_id.keys()),
            "per-inscription files and all.jsonl have different id sets",
        )
        for cid, rec in agg_by_id.items():
            with self.subTest(id=cid):
                self.assertEqual(rec, per_file[cid])


class TestChicCorpusSmoke(unittest.TestCase):
    """5-record smoke sample of CHIC catalog corners."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _INSCRIPTIONS_DIR.exists():
            raise unittest.SkipTest(
                "corpora/cretan_hieroglyphic/inscriptions/ not built; "
                "run scripts/build_chic_corpus.py first"
            )
        cls.smoke: dict[str, dict] = {}
        for cid in SMOKE_IDS:
            num = int(cid.rsplit("#", 1)[-1])
            cls.smoke[cid] = _load_record(num)

    def test_smoke_records_exist(self) -> None:
        for cid in SMOKE_IDS:
            with self.subTest(id=cid):
                self.assertIn(cid, self.smoke)
                self.assertEqual(self.smoke[cid]["id"], cid)

    def test_chic_001_is_knossos_crescent(self) -> None:
        """CHIC #001 = KN Ha (HMs 183), unimpressed crescent (CHIC p. 26)."""
        rec = self.smoke["CHIC #001"]
        self.assertEqual(rec["site"], "Knossos")
        self.assertEqual(rec["support"], "crescent")
        # The reading is X *053 070-031-034 (read retrograde per JGY); the
        # transnumeration column gives the four-sign canonical form. We
        # don't pin exact tokens (tokenization may evolve in chic-v1) but
        # we do require >=3 sign tokens and that #034 / #031 / #070 all
        # appear.
        sign_tokens = [
            t for t in rec["tokens"] if t.startswith("#")
        ]
        self.assertGreaterEqual(len(sign_tokens), 3)
        clean_or_uncertain = set()
        for t in rec["tokens"]:
            if t.startswith("#"):
                clean_or_uncertain.add(t[1:])
            elif t.startswith("[?:#"):
                clean_or_uncertain.add(t[3:-1].lstrip("#"))
        for sign in ("034", "031", "070"):
            self.assertIn(sign, clean_or_uncertain, f"#{sign} missing")

    def test_chic_070_is_mallia_cone(self) -> None:
        """CHIC #070 = MA/M Hd (HM 1091), Quartier Mu cone."""
        rec = self.smoke["CHIC #070"]
        self.assertEqual(rec["site"], "Mallia")
        self.assertEqual(rec["support"], "cone")

    def test_chic_118_has_numeric_quantities(self) -> None:
        """CHIC #118 is an MA/M four-sided bar with many NUM tokens."""
        rec = self.smoke["CHIC #118"]
        self.assertEqual(rec["site"], "Mallia")
        self.assertEqual(rec["support"], "bar")
        nums = [t for t in rec["tokens"] if t.startswith("NUM:")]
        self.assertGreater(
            len(nums), 5,
            "expected the MM #118 bar to carry several numeric counts",
        )

    def test_chic_225_is_sealstone(self) -> None:
        """CHIC #225 = CR (?) S (CMS XII 93), 3-sided prism sealstone."""
        rec = self.smoke["CHIC #225"]
        self.assertEqual(rec["support"], "seal")
        # site is "Crete (unprovenanced)" or one of the seal/sealing
        # defaults — accept either.
        self.assertIn("Crete", rec["site"])

    def test_chic_331_is_misc_chamaizi(self) -> None:
        """CHIC #331 is the last entry, a Prodromos Chamaizi vase."""
        rec = self.smoke["CHIC #331"]
        self.assertEqual(rec["support"], "chamaizi_vase")

    def test_smoke_token_round_trip(self) -> None:
        """Each smoke record's tokens parse back into the declared
        token grammar (defense-in-depth against schema regressions)."""
        for cid, rec in self.smoke.items():
            for tok in rec["tokens"]:
                with self.subTest(id=cid, token=tok):
                    self.assertRegex(tok, TOKEN_RE)


if __name__ == "__main__":
    unittest.main()
