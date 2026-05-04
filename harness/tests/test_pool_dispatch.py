"""Pool-specific bigram dispatch (mg-c2af).

mg-7c8c surfaced a confound: when ``score_hypothesis`` fell back to the
Aquitanian bigram for non-Aquitanian candidates (anchors, scrambles,
toponym fragments), ``local_fit_v1`` scores became non-comparable across
pools — anchor < scramble direction-flipped because anchors hit
rare-sign penalties under the wrong pool's vocabulary.

This test asserts the fix:
  (a) Aquitanian hypothesis → Aquitanian bigram.
  (b) Etruscan hypothesis    → Etruscan bigram.
  (c) Toponym hypothesis     → Toponym bigram.
  (d) Anchor / scramble      → null bigram (term excluded; bigram_term
      field in the result row is None and metric_notes records the
      fallback).

Equality of the bigram model is tested via the empirical log-prob of a
diagnostic bigram that differs strongly between pools (each test pool
fixture is built so a probe bigram has a distinctive log-prob).

Run directly:
  python3 -m harness.tests.test_pool_dispatch
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import run_sweep  # noqa: E402
from harness.metrics import EmpiricalBigramModel  # noqa: E402
from harness.run import _load_pool_for, score_hypothesis  # noqa: E402


# Three minimal pools whose bigram statistics differ enough to be told
# apart at the model level.
_AQUI_YAML = textwrap.dedent(
    """\
    pool: aquitanian
    source_citation: synthetic Aquitanian fixture (test_pool_dispatch)
    license: synthetic
    fetched_at: "2026-05-04T00:00:00Z"
    entries:
      - surface: kupa
        phonemes: [k, u, p, a]
        gloss: synthetic
        semantic_field: kin
        region: aquitania
        citation: synthetic
      - surface: bere
        phonemes: [b, e, r, e]
        gloss: synthetic
        semantic_field: kin
        region: aquitania
        citation: synthetic
    """
)

_ETRU_YAML = textwrap.dedent(
    """\
    pool: etruscan
    source_citation: synthetic Etruscan fixture (test_pool_dispatch)
    license: synthetic
    fetched_at: "2026-05-04T00:00:00Z"
    entries:
      - surface: lautn
        phonemes: [l, a, u, t, n]
        gloss: synthetic
        semantic_field: kin
        region: etruria
        citation: synthetic
      - surface: zilath
        phonemes: [z, i, l, a, th]
        gloss: synthetic
        semantic_field: function
        region: etruria
        citation: synthetic
    """
)

_TOPO_YAML = textwrap.dedent(
    """\
    pool: toponym
    source_citation: synthetic toponym fixture (test_pool_dispatch)
    license: synthetic
    fetched_at: "2026-05-04T00:00:00Z"
    entries:
      - surface: knossos
        phonemes: [k, n, o, s, s, o, s]
        gloss: synthetic
        semantic_field: place
        region: pre_greek
        citation: synthetic
      - surface: korinthos
        phonemes: [k, o, r, i, n, th, o, s]
        gloss: synthetic
        semantic_field: place
        region: pre_greek
        citation: synthetic
    """
)


_HYP_AQUI = textwrap.dedent(
    """\
    schema_version: candidate_equation.v1
    name: probe_aquitanian
    description: synthetic Aquitanian candidate (test_pool_dispatch)
    author: test_pool_dispatch
    created: "2026-05-04"
    source_pool: aquitanian
    root:
      surface: bere
      phonemes: [b, e, r, e]
      gloss_hint: synthetic
      citation: synthetic
    equation:
      inscription_id: TOY 1
      span: [0, 3]
      sign_to_phoneme:
        AB54: b
        AB02: e
        AB80: r
        AB81: e
    """
)

_HYP_ETRU = textwrap.dedent(
    """\
    schema_version: candidate_equation.v1
    name: probe_etruscan
    description: synthetic Etruscan candidate (test_pool_dispatch)
    author: test_pool_dispatch
    created: "2026-05-04"
    source_pool: etruscan
    root:
      surface: lautn
      phonemes: [l, a, u, t, n]
      gloss_hint: synthetic
      citation: synthetic
    equation:
      inscription_id: TOY 1
      span: [0, 4]
      sign_to_phoneme:
        AB54: l
        AB02: a
        AB80: u
        AB81: t
        AB28: n
    """
)

_HYP_TOPO = textwrap.dedent(
    """\
    schema_version: candidate_equation.v1
    name: probe_toponym
    description: synthetic toponym candidate (test_pool_dispatch)
    author: test_pool_dispatch
    created: "2026-05-04"
    source_pool: toponym
    root:
      surface: knoso
      phonemes: [k, n, o, s, o]
      gloss_hint: synthetic
      citation: synthetic
    equation:
      inscription_id: TOY 1
      span: [0, 4]
      sign_to_phoneme:
        AB54: k
        AB02: n
        AB80: o
        AB81: s
        AB28: o
    """
)

_HYP_ANCHOR = textwrap.dedent(
    """\
    schema_version: candidate_equation.v1
    name: probe_anchor
    description: synthetic Linear-B anchor (test_pool_dispatch)
    author: test_pool_dispatch
    created: "2026-05-04"
    source_pool: linear_b_carryover
    root:
      surface: kuro
      phonemes: [ku, ro]
      gloss_hint: synthetic
      citation: synthetic
    equation:
      inscription_id: TOY 1
      span: [0, 1]
      sign_to_phoneme:
        AB54: ku
        AB02: ro
    """
)

_HYP_SCRAMBLE = textwrap.dedent(
    """\
    schema_version: candidate_equation.v1
    name: probe_scramble
    description: synthetic random scramble (test_pool_dispatch)
    author: test_pool_dispatch
    created: "2026-05-04"
    source_pool: random_scramble
    root:
      surface: qz
      phonemes: [q, z]
      gloss_hint: synthetic
      citation: synthetic
    equation:
      inscription_id: TOY 1
      span: [0, 1]
      sign_to_phoneme:
        AB54: q
        AB02: z
    """
)


class _PoolDispatchFixture(unittest.TestCase):
    """Shared tempdir fixture for the dispatch tests."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="lineara-dispatch-"))
        self.repo = self.tmp
        self.pools_dir = self.repo / "pools"
        self.pools_dir.mkdir(parents=True)
        (self.pools_dir / "aquitanian.yaml").write_text(_AQUI_YAML, encoding="utf-8")
        (self.pools_dir / "etruscan.yaml").write_text(_ETRU_YAML, encoding="utf-8")
        (self.pools_dir / "toponym.yaml").write_text(_TOPO_YAML, encoding="utf-8")

        self.hyp_dir = self.repo / "hypotheses" / "curated"
        self.hyp_dir.mkdir(parents=True)
        (self.hyp_dir / "probe_aquitanian.yaml").write_text(_HYP_AQUI, encoding="utf-8")
        (self.hyp_dir / "probe_etruscan.yaml").write_text(_HYP_ETRU, encoding="utf-8")
        (self.hyp_dir / "probe_toponym.yaml").write_text(_HYP_TOPO, encoding="utf-8")
        (self.hyp_dir / "probe_anchor.yaml").write_text(_HYP_ANCHOR, encoding="utf-8")
        (self.hyp_dir / "probe_scramble.yaml").write_text(_HYP_SCRAMBLE, encoding="utf-8")

        # Toy corpus that exercises every sign in the probes.
        self.corpus_dir = self.repo / "corpus"
        self.corpus_dir.mkdir()
        self.corpus_path = self.corpus_dir / "all.jsonl"
        records = [
            {
                "id": "TOY 1",
                "site": "Knossos",
                "support": "tablet",
                "genre_hint": "accountancy",
                "transcription_confidence": "clean",
                "tokens": ["AB54", "AB02", "AB80", "AB81", "AB28", "AB04", "AB28b"],
                "n_signs": 7,
                "n_words": 1,
                "raw_transliteration": "AB54-AB02-AB80-AB81-AB28-AB04-AB28b",
                "source": "synthetic",
                "fetched_at": "2026-05-04T00:00:00Z",
            },
        ]
        with self.corpus_path.open("w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r) + "\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class PoolDispatchUnitTest(_PoolDispatchFixture):
    """The bigram model picked by ``_load_pool_for`` matches source_pool."""

    def _bigram_model_for(self, hyp_yaml: str) -> EmpiricalBigramModel | None:
        # _load_pool_for inspects hypothesis.source_pool only.
        import yaml

        hypothesis = yaml.safe_load(hyp_yaml)
        ctx = _load_pool_for(None, hypothesis, self.repo)
        return ctx["bigram_model"] if ctx is not None else None

    def test_aquitanian_hypothesis_picks_aquitanian_bigram(self) -> None:
        m = self._bigram_model_for(_HYP_AQUI)
        self.assertIsNotNone(m)
        # Aquitanian fixture pool has the bigram (b, e) in entry "bere":
        # the smoothed log-prob of (b, e) must exceed the log-prob of a
        # bigram only present in the toponym pool, e.g. (k, n).
        self.assertGreater(m.log_prob("b", "e"), m.log_prob("k", "n"))

    def test_etruscan_hypothesis_picks_etruscan_bigram(self) -> None:
        m = self._bigram_model_for(_HYP_ETRU)
        self.assertIsNotNone(m)
        # Etruscan fixture has (l, a) in entry "lautn"; (b, e) is
        # Aquitanian-only.
        self.assertGreater(m.log_prob("l", "a"), m.log_prob("b", "e"))

    def test_toponym_hypothesis_picks_toponym_bigram(self) -> None:
        m = self._bigram_model_for(_HYP_TOPO)
        self.assertIsNotNone(m)
        # Toponym fixture has (k, n) in "knossos"; (l, a) is Etruscan-only.
        self.assertGreater(m.log_prob("k", "n"), m.log_prob("l", "a"))

    def test_anchor_resolves_to_no_pool(self) -> None:
        # source_pool="linear_b_carryover" — there is no pools/linear_b_carryover.yaml,
        # so the dispatcher returns None.
        m = self._bigram_model_for(_HYP_ANCHOR)
        self.assertIsNone(m)

    def test_scramble_resolves_to_no_pool(self) -> None:
        m = self._bigram_model_for(_HYP_SCRAMBLE)
        self.assertIsNone(m)


class PoolDispatchEndToEndTest(_PoolDispatchFixture):
    """End-to-end ``score_hypothesis`` rows under each dispatch path."""

    def _score(self, hyp_filename: str, metric: str = "local_fit_v1") -> dict:
        return score_hypothesis(
            hypothesis_path=self.hyp_dir / hyp_filename,
            metric_name=metric,
            corpus_path=self.corpus_path,
            repo_root=self.repo,
        )

    def test_aquitanian_row_has_real_bigram_term(self) -> None:
        row = self._score("probe_aquitanian.yaml")
        self.assertEqual(row["metric"], "local_fit_v1")
        self.assertIsNotNone(row["bigram_term"])
        # vocabulary note from the metric mentions "vocab=" — only when
        # a model was used.
        self.assertIn("vocab=", row["metric_notes"])

    def test_etruscan_row_has_real_bigram_term(self) -> None:
        row = self._score("probe_etruscan.yaml")
        self.assertIsNotNone(row["bigram_term"])
        self.assertIn("vocab=", row["metric_notes"])

    def test_toponym_row_has_real_bigram_term(self) -> None:
        row = self._score("probe_toponym.yaml")
        self.assertIsNotNone(row["bigram_term"])
        self.assertIn("vocab=", row["metric_notes"])

    def test_anchor_row_has_null_bigram_term(self) -> None:
        row = self._score("probe_anchor.yaml")
        self.assertIsNone(row["bigram_term"])
        # Notes carry the explicit fallback signal.
        self.assertIn("bigram=null", row["metric_notes"])
        self.assertIn("no pool match", row["metric_notes"])

    def test_scramble_row_has_null_bigram_term(self) -> None:
        row = self._score("probe_scramble.yaml")
        self.assertIsNone(row["bigram_term"])
        self.assertIn("bigram=null", row["metric_notes"])

    def test_anchor_score_is_finite_and_score_field_is_set(self) -> None:
        # The score must remain a real number even with the bigram term
        # excluded — the position term carries the (A+B) weight.
        row = self._score("probe_anchor.yaml")
        import math

        self.assertTrue(math.isfinite(float(row["score"])))


class SweepRunnerDispatchTest(_PoolDispatchFixture):
    """The bulk sweep runner dispatches per-hypothesis from source_pool."""

    def _write_manifest(self, name: str, items: list[tuple[str, str]]) -> Path:
        from harness.hypothesis import canonical_hash, load_and_validate

        path = self.hyp_dir.parent / f"{name}.manifest.jsonl"
        with path.open("w", encoding="utf-8") as fh:
            for hyp_filename, source_pool in items:
                hyp_path = self.hyp_dir / hyp_filename
                doc = load_and_validate(hyp_path)
                fh.write(
                    json.dumps(
                        {
                            "pool": source_pool,
                            "pool_entry_index": 0,
                            "pool_entry_surface": doc["root"]["surface"],
                            "inscription_id": doc["equation"]["inscription_id"],
                            "span_start": doc["equation"]["span"][0],
                            "span_end": doc["equation"]["span"][1],
                            "hypothesis_path": str(hyp_path.relative_to(self.repo)),
                            "hypothesis_hash": canonical_hash(doc),
                        }
                    )
                    + "\n"
                )
        return path

    def test_mixed_manifest_dispatches_per_hypothesis(self) -> None:
        manifest = self._write_manifest(
            "mixed",
            [
                ("probe_aquitanian.yaml", "aquitanian"),
                ("probe_etruscan.yaml", "etruscan"),
                ("probe_toponym.yaml", "toponym"),
                ("probe_anchor.yaml", "linear_b_carryover"),
                ("probe_scramble.yaml", "random_scramble"),
            ],
        )
        results_path = self.repo / "results" / "experiments.jsonl"
        run_sweep.run(
            manifest_path=manifest,
            corpus_path=self.corpus_path,
            results_path=results_path,
            note="dispatch test",
            progress_every=0,
            repo_root=self.repo,
            metrics=["local_fit_v1"],
            pools_dir=self.pools_dir,
        )
        with results_path.open("r", encoding="utf-8") as fh:
            rows = [json.loads(l) for l in fh if l.strip()]
        by_path = {Path(r["hypothesis_path"]).name: r for r in rows}

        # Pool-matched rows have a real bigram_term.
        self.assertIsNotNone(by_path["probe_aquitanian.yaml"]["bigram_term"])
        self.assertIsNotNone(by_path["probe_etruscan.yaml"]["bigram_term"])
        self.assertIsNotNone(by_path["probe_toponym.yaml"]["bigram_term"])
        # Anchor / scramble rows have null bigram_term.
        self.assertIsNone(by_path["probe_anchor.yaml"]["bigram_term"])
        self.assertIsNone(by_path["probe_scramble.yaml"]["bigram_term"])
        # Notes preserve the dispatch reason.
        self.assertIn("bigram=null", by_path["probe_anchor.yaml"]["metric_notes"])

    def test_dispatch_is_deterministic_byte_identical_across_reruns(self) -> None:
        # Re-running the same hypothesis set under fixed dispatch must
        # produce byte-identical scores. (Brief: "preserve determinism".)
        manifest = self._write_manifest(
            "det",
            [
                ("probe_aquitanian.yaml", "aquitanian"),
                ("probe_anchor.yaml", "linear_b_carryover"),
            ],
        )
        results1 = self.repo / "results" / "first.jsonl"
        results2 = self.repo / "results" / "second.jsonl"
        for path in (results1, results2):
            run_sweep.run(
                manifest_path=manifest,
                corpus_path=self.corpus_path,
                results_path=path,
                note="det test",
                progress_every=0,
                repo_root=self.repo,
                metrics=["local_fit_v1"],
                pools_dir=self.pools_dir,
            )
        with results1.open() as fh:
            rows1 = [json.loads(l) for l in fh if l.strip()]
        with results2.open() as fh:
            rows2 = [json.loads(l) for l in fh if l.strip()]
        self.assertEqual(len(rows1), len(rows2))
        by_h1 = {r["hypothesis_hash"]: r for r in rows1}
        by_h2 = {r["hypothesis_hash"]: r for r in rows2}
        self.assertEqual(set(by_h1), set(by_h2))
        for h, r1 in by_h1.items():
            r2 = by_h2[h]
            self.assertEqual(r1["score"], r2["score"])
            self.assertEqual(r1["position_term"], r2["position_term"])
            self.assertEqual(r1["bigram_term"], r2["bigram_term"])
            self.assertEqual(r1["length_penalty"], r2["length_penalty"])
            self.assertEqual(r1["rare_sign_correction"], r2["rare_sign_correction"])


if __name__ == "__main__":
    unittest.main()
