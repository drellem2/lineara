"""Smoke test for the candidate_equation.v1 hypothesis shape and the
``local_fit_v0`` metric on a 3-record toy corpus.

Exercises:
  - YAML loading + schema dispatch on schema_version
  - candidate_equation.v1 semantic checks (phoneme/sign-key length parity,
    ordering)
  - sign_position_fingerprints over a small fixture corpus
  - local_fit_v0 determinism (same input -> identical score and z)
  - bucket-separation sanity: a Linear-B-style "anchor" alignment scores
    higher than a deliberately-mismatched "negative-control" alignment
    on the toy corpus.

Run directly:
  python3 -m harness.tests.test_candidate_equation
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from harness.corpus import build_stream, load_records, sign_position_fingerprints
from harness.hypothesis import (
    SHAPE_CANDIDATE_EQUATION_V1,
    SHAPE_V0,
    detect_shape,
    load_and_validate,
)
from harness.metrics import local_fit_v0
from harness.run import score_hypothesis, append_row


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

# Three toy records. Designed so that:
#   - AB54 always appears at word-initial position (high "initial" mass)
#   - AB02 always appears at word-final position (high "final" mass)
#   - The (AB54, AB02) pair occupies the canonical Basque CV-then-V-final
#     positions when assigned class C and V respectively.
_FIXTURE_RECORDS = [
    {
        "id": "TOY 1",
        "site": "Toy",
        "support": "tablet",
        "genre_hint": "accountancy",
        "transcription_confidence": "clean",
        "tokens": ["AB54", "AB02", "DIV", "AB54", "AB02"],
        "n_signs": 4,
        "n_words": 2,
        "raw_transliteration": "AB54-AB02 / AB54-AB02",
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
        "tokens": ["AB54", "AB02"],
        "n_signs": 2,
        "n_words": 1,
        "raw_transliteration": "AB54-AB02",
        "source": "toy:test/TOY 3/",
        "fetched_at": "2026-05-04T00:00:00Z",
    },
]


# Anchor-style hypothesis: AB54 (initial-friendly) -> /k/, AB02 (final-friendly)
# -> /o/. C-V class structure matches Basque CV preference; positions match.
_HYP_ANCHOR_YAML = """\
schema_version: candidate_equation.v1
name: toy_anchor
description: anchor hypothesis on toy corpus
source_pool: toy_anchor
root:
  surface: "ko"
  phonemes:
    - "k"
    - "o"
equation:
  inscription_id: "TOY 3"
  span: [0, 1]
  sign_to_phoneme:
    AB54: k
    AB02: o
"""

# Negative-control hypothesis: same root /ko/, but assigned to (AB02, AB54)
# — i.e., the order is REVERSED relative to the anchor. AB02 (final-friendly)
# now hosts the consonant /k/ and AB54 (initial-friendly) hosts the vowel /o/.
# This deliberately scrambles the position-class match, so should score lower
# than the anchor.
_HYP_WRONG_YAML = """\
schema_version: candidate_equation.v1
name: toy_wrong
description: deliberately reversed alignment on toy corpus
source_pool: toy_negative_control
root:
  surface: "ko"
  phonemes:
    - "k"
    - "o"
equation:
  inscription_id: "TOY 1"
  span: [1, 3]
  sign_to_phoneme:
    AB02: k
    AB54: o
"""


class CandidateEquationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="lineara-cand-eq-"))
        self.corpus = self.tmp / "corpus.jsonl"
        with self.corpus.open("w", encoding="utf-8") as fh:
            for rec in _FIXTURE_RECORDS:
                fh.write(json.dumps(rec) + "\n")
        self.hyp_anchor = self.tmp / "anchor.yaml"
        self.hyp_anchor.write_text(_HYP_ANCHOR_YAML, encoding="utf-8")
        self.hyp_wrong = self.tmp / "wrong.yaml"
        self.hyp_wrong.write_text(_HYP_WRONG_YAML, encoding="utf-8")
        self.results = self.tmp / "experiments.jsonl"

        schema_path = _REPO_ROOT / "harness" / "schemas" / "result.v0.schema.json"
        self.result_validator = Draft202012Validator(json.loads(schema_path.read_text()))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_shape_dispatch(self) -> None:
        anchor_doc = load_and_validate(self.hyp_anchor)
        self.assertEqual(detect_shape(anchor_doc), SHAPE_CANDIDATE_EQUATION_V1)

        # An old-style v0 mapping still loads and dispatches to v0.
        v0_yaml = self.tmp / "old.yaml"
        v0_yaml.write_text("name: legacy\nmapping:\n  AB54: ti\n", encoding="utf-8")
        v0_doc = load_and_validate(v0_yaml)
        self.assertEqual(detect_shape(v0_doc), SHAPE_V0)

    def test_schema_rejects_phoneme_count_mismatch(self) -> None:
        bad = self.tmp / "bad_count.yaml"
        bad.write_text(
            """\
schema_version: candidate_equation.v1
name: bad_count
root:
  surface: "ku"
  phonemes:
    - "k"
    - "u"
    - "z"
equation:
  inscription_id: "TOY 3"
  span: [0, 1]
  sign_to_phoneme:
    AB54: k
    AB02: u
""",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            load_and_validate(bad)

    def test_schema_rejects_phoneme_order_mismatch(self) -> None:
        bad = self.tmp / "bad_order.yaml"
        bad.write_text(
            """\
schema_version: candidate_equation.v1
name: bad_order
root:
  surface: "ku"
  phonemes:
    - "k"
    - "u"
equation:
  inscription_id: "TOY 3"
  span: [0, 1]
  sign_to_phoneme:
    AB54: u
    AB02: k
""",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            load_and_validate(bad)

    def test_position_fingerprints(self) -> None:
        records = load_records(self.corpus)
        stream, _ = build_stream(records)
        fp = sign_position_fingerprints(stream)
        # AB54 occurs 4 times in the toy corpus. All occurrences are word-initial.
        self.assertEqual(fp["AB54"][0], 4)
        # AB02 occurs 4 times. All occurrences are word-final.
        self.assertEqual(fp["AB02"][2], 4)
        # AB80 occurs once, in the medial slot of TOY 2's three-sign word.
        self.assertEqual(fp["AB80"][1], 1)

    def test_local_fit_deterministic(self) -> None:
        records = load_records(self.corpus)
        stream, _ = build_stream(records)
        r1 = local_fit_v0(stream, ["AB54", "AB02"], ["k", "o"])
        r2 = local_fit_v0(stream, ["AB54", "AB02"], ["k", "o"])
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.score_control_z, r2.score_control_z)
        self.assertEqual(r1.metric_notes, r2.metric_notes)

    def test_anchor_beats_negative_control_on_toy(self) -> None:
        anchor_row = score_hypothesis(
            self.hyp_anchor,
            corpus_path=self.corpus,
            repo_root=self.tmp,
        )
        wrong_row = score_hypothesis(
            self.hyp_wrong,
            corpus_path=self.corpus,
            repo_root=self.tmp,
        )
        # Both rows must validate.
        self.result_validator.validate(anchor_row)
        self.result_validator.validate(wrong_row)
        # local_fit_v0 metric was selected.
        self.assertEqual(anchor_row["metric"], "local_fit_v0")
        self.assertEqual(wrong_row["metric"], "local_fit_v0")
        # Anchor (AB54-initial→k, AB02-final→o) MUST score higher than
        # the reversed negative control on the toy corpus, which is the
        # whole point of the metric design.
        self.assertGreater(anchor_row["score"], wrong_row["score"])

    def test_full_run_appends_valid_row_and_is_byte_identical(self) -> None:
        row1 = score_hypothesis(
            self.hyp_anchor,
            corpus_path=self.corpus,
            repo_root=self.tmp,
            note="cand-eq-1",
        )
        append_row(row1, self.results)
        row2 = score_hypothesis(
            self.hyp_anchor,
            corpus_path=self.corpus,
            repo_root=self.tmp,
            note="cand-eq-2",
        )
        append_row(row2, self.results)

        for row in (row1, row2):
            self.result_validator.validate(row)

        # Determinism: score and control z are byte-identical across re-runs.
        self.assertEqual(row1["score"], row2["score"])
        self.assertEqual(row1["score_control_z"], row2["score_control_z"])
        self.assertEqual(row1["hypothesis_hash"], row2["hypothesis_hash"])
        # run_id must differ (uuid4 per call).
        self.assertNotEqual(row1["run_id"], row2["run_id"])

        with self.results.open("r", encoding="utf-8") as fh:
            stored = [json.loads(line) for line in fh if line.strip()]
        self.assertEqual(len(stored), 2)
        self.assertIn("score_control_z", stored[0])
        self.assertIn("metric_notes", stored[0])

    def test_v0_row_omits_local_fit_fields(self) -> None:
        # Ensure the existing v0 mapping shape produces a row that does NOT
        # contain score_control_z (those fields are reserved for local_fit_v0).
        v0_yaml = self.tmp / "legacy.yaml"
        v0_yaml.write_text("name: legacy\nmapping:\n  AB54: ti\n", encoding="utf-8")
        row = score_hypothesis(
            v0_yaml,
            corpus_path=self.corpus,
            repo_root=self.tmp,
        )
        self.assertEqual(row["metric"], "compression_delta_v0")
        self.assertNotIn("score_control_z", row)
        self.assertNotIn("metric_notes", row)
        self.assertIn("bits_per_sign_baseline", row)
        self.result_validator.validate(row)


if __name__ == "__main__":
    unittest.main()
