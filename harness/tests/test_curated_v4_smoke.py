"""Smoke test for the mg-7c8c curated v4 expansion.

Validates that:
  - the construction manifest exists and lists exactly 100 entries
    (20 existing + 80 new), 20 per bucket;
  - every YAML it points at loads + validates against the
    candidate_equation.v1 schema and the manifest's `hypothesis_hash`
    matches the loaded hypothesis's canonical hash;
  - a small sampled subset (one per bucket) scores cleanly under each
    of the three v3 metrics with no exceptions, returning rows that
    validate against the result schema.

Run directly:
  python3 -m harness.tests.test_curated_v4_smoke
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from harness.hypothesis import canonical_hash, load_and_validate
from harness.run import score_hypothesis


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_MANIFEST = _REPO_ROOT / "hypotheses" / "curated" / "CONSTRUCTION.manifest.jsonl"
_BUCKET_ORDER = (
    "A_linear_b_anchor",
    "B_aquit_plausible",
    "C_aquit_wrong",
    "D_toponym_plausible",
    "E_scramble",
)


def _load_manifest() -> list[dict]:
    rows: list[dict] = []
    with _MANIFEST.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


class CuratedV4SmokeTest(unittest.TestCase):
    def test_manifest_layout(self) -> None:
        rows = _load_manifest()
        self.assertEqual(len(rows), 100, "manifest must contain 100 rows")
        by_bucket: dict[str, list[dict]] = {}
        for r in rows:
            by_bucket.setdefault(r["bucket"], []).append(r)
        for bucket in _BUCKET_ORDER:
            self.assertEqual(
                len(by_bucket.get(bucket, [])),
                20,
                f"bucket {bucket} must have 20 entries",
            )
        self.assertEqual(set(by_bucket), set(_BUCKET_ORDER))

    def test_every_yaml_loads_and_hash_matches(self) -> None:
        rows = _load_manifest()
        for r in rows:
            hyp_path = _REPO_ROOT / r["hypothesis_path"]
            self.assertTrue(hyp_path.exists(), f"missing YAML: {hyp_path}")
            doc = load_and_validate(hyp_path)
            h = canonical_hash(doc)
            self.assertEqual(
                h,
                r["hypothesis_hash"],
                f"manifest hash drift for {r['hypothesis_path']}",
            )

    def test_sampled_scoring_one_per_bucket(self) -> None:
        """Score one v4-new entry per bucket under each v3 metric."""
        rows = _load_manifest()
        sampled: dict[str, dict] = {}
        for r in rows:
            if not r.get("is_v4_new"):
                continue
            sampled.setdefault(r["bucket"], r)
        self.assertEqual(set(sampled), set(_BUCKET_ORDER))

        metrics = (
            "local_fit_v1",
            "partial_mapping_compression_delta_v0",
            "geographic_genre_fit_v1",
        )
        for bucket, manifest_row in sampled.items():
            hyp_path = _REPO_ROOT / manifest_row["hypothesis_path"]
            for metric in metrics:
                row = score_hypothesis(
                    hypothesis_path=hyp_path,
                    metric_name=metric,
                    note="smoke-curated-v4",
                )
                self.assertIn("score", row, f"{bucket}/{metric} missing score")
                self.assertEqual(row["metric"], metric)
                self.assertEqual(row["hypothesis_hash"], manifest_row["hypothesis_hash"])

    def test_existing_entries_preserved(self) -> None:
        """The 4 mg-fb23 entries per bucket remain in the manifest."""
        rows = _load_manifest()
        existing_names = {r["hypothesis_name"] for r in rows if not r["is_v4_new"]}
        self.assertEqual(len(existing_names), 20)
        # spot-check a couple
        self.assertIn("anchor_kuro_HT100", existing_names)
        self.assertIn("aquit_in_PH6", existing_names)
        self.assertIn("scramble_HT100_E1", existing_names)


if __name__ == "__main__":
    unittest.main()
