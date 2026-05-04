"""Smoke tests for the candidate_signature.v1 hypothesis shape (mg-bef2).

Exercises:
  * Schema-level validation: required fields, empty roots[] rejection.
  * Semantic checks (overlapping spans, conflicting sign_to_phoneme,
    out-of-window placements).
  * The ``signature_combined_mapping`` helper.
  * Shape-dispatch on a candidate_signature.v1 file.
"""

from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from jsonschema import ValidationError

from harness.hypothesis import (
    SHAPE_CANDIDATE_SIGNATURE_V1,
    canonical_hash,
    detect_shape,
    load_and_validate,
    signature_combined_mapping,
)


_GOOD_SIGNATURE = """\
schema_version: candidate_signature.v1
name: smoke_signature
description: smoke test
author: harness/tests/test_signature_schema.py
created: '2026-05-04'
source_pool: aquitanian
window:
  inscription_id: TOY 1
  span:
    - 0
    - 11
roots:
  - surface: etxe
    phonemes: [e, tx, e]
    sign_to_phoneme:
      AB37: e
      AB54: tx
    span_within_window:
      - 0
      - 2
  - surface: ama
    phonemes: [a, m, a]
    sign_to_phoneme:
      AB05: a
      AB10: m
    span_within_window:
      - 4
      - 6
  - surface: "on"
    phonemes: [o, n]
    sign_to_phoneme:
      AB39: o
      AB31: n
    span_within_window:
      - 9
      - 10
coverage:
  n_window_syllabograms: 8
  n_covered_syllabograms: 8
  fraction: 1.0
"""


class SignatureSchemaSmoke(unittest.TestCase):

    def _write(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        )
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    def test_good_signature_loads_and_validates(self):
        path = self._write(_GOOD_SIGNATURE)
        doc = load_and_validate(path)
        self.assertEqual(detect_shape(doc), SHAPE_CANDIDATE_SIGNATURE_V1)
        self.assertEqual(doc["window"]["inscription_id"], "TOY 1")
        self.assertEqual(len(doc["roots"]), 3)

    def test_combined_mapping_unions_roots(self):
        path = self._write(_GOOD_SIGNATURE)
        doc = load_and_validate(path)
        m = signature_combined_mapping(doc)
        self.assertEqual(
            m,
            {
                "AB37": "e",
                "AB54": "tx",
                "AB05": "a",
                "AB10": "m",
                "AB39": "o",
                "AB31": "n",
            },
        )

    def test_overlapping_spans_rejected(self):
        bad = _GOOD_SIGNATURE.replace(
            "      - 4\n      - 6", "      - 2\n      - 4"
        )
        path = self._write(bad)
        with self.assertRaises(ValueError) as ctx:
            load_and_validate(path)
        self.assertIn("overlap", str(ctx.exception).lower())

    def test_conflicting_sign_to_phoneme_rejected(self):
        # Make root[1]'s AB37 map to 'a' (root[0] mapped AB37 -> 'e').
        bad = _GOOD_SIGNATURE.replace(
            "    sign_to_phoneme:\n      AB05: a\n      AB10: m",
            "    sign_to_phoneme:\n      AB37: a\n      AB10: m",
        )
        path = self._write(bad)
        with self.assertRaises(ValueError) as ctx:
            load_and_validate(path)
        self.assertIn("AB37", str(ctx.exception))

    def test_span_outside_window_rejected(self):
        bad = _GOOD_SIGNATURE.replace(
            "    span_within_window:\n      - 9\n      - 10",
            "    span_within_window:\n      - 9\n      - 999",
        )
        path = self._write(bad)
        with self.assertRaises(ValueError) as ctx:
            load_and_validate(path)
        self.assertIn("window length", str(ctx.exception).lower())

    def test_empty_roots_rejected_by_schema(self):
        bad = textwrap.dedent(
            """\
            schema_version: candidate_signature.v1
            name: empty_roots
            window:
              inscription_id: TOY 1
              span: [0, 5]
            roots: []
            """
        )
        path = self._write(bad)
        with self.assertRaises(ValidationError):
            load_and_validate(path)

    def test_canonical_hash_determinism(self):
        path = self._write(_GOOD_SIGNATURE)
        doc1 = load_and_validate(path)
        doc2 = load_and_validate(path)
        self.assertEqual(canonical_hash(doc1), canonical_hash(doc2))


if __name__ == "__main__":
    unittest.main()
