"""Smoke tests for the chic-v3 pipeline (mg-9700).

Validates the end-to-end driver in
``scripts/chic_substrate_run.py``: syllabographic-stream filtering,
candidate generation against CHIC windows, scoring under each pool's
external phoneme LM, per-surface bayesian aggregation, and the
right-tail bayesian gate.

The smoke test runs against a 5-record toy CHIC corpus with a
2-entry substrate pool + matched 2-entry control pool and a
2-character LM, all built in-memory in a tmpdir. The full pipeline
is exercised end-to-end; we assert artifact shape (manifests,
hypothesis YAMLs, sidecar rows, rollup markdown) rather than
specific gate verdicts (toy-corpus posteriors are not stable enough
for verdict assertions).

Run directly:
  python3 -m harness.tests.test_chic_substrate_run
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from harness.external_phoneme_model import build_model
from scripts.chic_substrate_run import (
    _CHIC_SYLLABOGRAM_RE,
    _candidate_windows,
    run as chic_run,
)
from scripts.build_chic_syllabographic_corpus import (
    filter_tokens,
    load_syllabographic_signs,
)


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent


# ---------------------------------------------------------------------------
# Filter unit tests
# ---------------------------------------------------------------------------


class FilterTokensSmoke(unittest.TestCase):
    """Tests the syllabographic-only filter from build_chic_syllabographic_corpus."""

    SYLL = {"#001", "#005", "#031", "#044", "#070"}

    def test_keeps_syllabographic_only(self):
        toks = ["#005", "#031", "#070", "#044"]
        self.assertEqual(filter_tokens(toks, self.SYLL), toks)

    def test_collapses_non_syllabographic_to_div(self):
        toks = ["#005", "#150", "#031"]  # #150 is not in SYLL
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005", "DIV", "#031"])

    def test_uncertain_marker_collapses_to_div(self):
        toks = ["#005", "[?:#031]", "#044"]
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005", "DIV", "#044"])

    def test_unknown_marker_collapses_to_div(self):
        toks = ["#005", "[?]", "#044"]
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005", "DIV", "#044"])

    def test_numeric_collapses_to_div(self):
        toks = ["#005", "NUM:7000", "#044"]
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005", "DIV", "#044"])

    def test_consecutive_breaks_collapse(self):
        toks = ["#005", "[?]", "[?]", "DIV", "NUM:5", "#044"]
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005", "DIV", "#044"])

    def test_leading_trailing_div_trimmed(self):
        toks = ["[?]", "#005", "DIV"]
        out = filter_tokens(toks, self.SYLL)
        self.assertEqual(out, ["#005"])

    def test_loads_real_inventory(self):
        signs_yaml = _REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
        if not signs_yaml.exists():
            self.skipTest("CHIC signs YAML not present")
        syll = load_syllabographic_signs(signs_yaml)
        self.assertGreater(len(syll), 0)
        # Default chic-v1 rule: #001-#100 syllabographic, #101+ ideogram.
        self.assertIn("#001", syll)
        self.assertNotIn("#150", syll)


# ---------------------------------------------------------------------------
# Window enumeration
# ---------------------------------------------------------------------------


class CandidateWindowsSmoke(unittest.TestCase):

    def test_recognises_chic_signs(self):
        self.assertTrue(_CHIC_SYLLABOGRAM_RE.fullmatch("#005"))
        self.assertTrue(_CHIC_SYLLABOGRAM_RE.fullmatch("#031"))
        self.assertFalse(_CHIC_SYLLABOGRAM_RE.fullmatch("DIV"))
        # Linear A signs aren't CHIC syllabograms.
        self.assertFalse(_CHIC_SYLLABOGRAM_RE.fullmatch("AB54"))

    def test_div_splits_block(self):
        toks = ["#005", "#031", "DIV", "#044", "#070"]
        wins = _candidate_windows(toks, n_phonemes=2)
        # Two blocks of 2 syllabograms each → one length-2 window per block.
        self.assertEqual(len(wins), 2)
        self.assertEqual(wins[0], (0, 1, [0, 1]))
        self.assertEqual(wins[1], (3, 4, [3, 4]))

    def test_within_block_sliding(self):
        toks = ["#005", "#031", "#044", "#070"]
        wins = _candidate_windows(toks, n_phonemes=3)
        self.assertEqual(len(wins), 2)

    def test_too_few_signs_emits_zero(self):
        toks = ["#005", "DIV", "#031"]
        wins = _candidate_windows(toks, n_phonemes=3)
        self.assertEqual(wins, [])


# ---------------------------------------------------------------------------
# End-to-end pipeline smoke
# ---------------------------------------------------------------------------


def _toy_chic_records() -> list[dict]:
    """5-record toy CHIC corpus. Each token list is already filtered
    to syllabographic + DIV (i.e. it's the post-filter shape that
    ``build_stream`` ingests directly)."""
    return [
        {
            "id": "CHIC #001",
            "site": "Knossos",
            "support": "crescent",
            "period": None,
            "transcription_confidence": "clean",
            "tokens": ["#005", "#031", "#044", "#070"],
            "raw_transliteration": "#005 #031 #044 #070",
            "n_signs": 4,
            "source": "younger_online",
            "source_citation": "test",
            "fetched_at": "2026-05-05T00:00:00Z",
        },
        {
            "id": "CHIC #002",
            "site": "Mallia",
            "support": "bar",
            "period": None,
            "transcription_confidence": "clean",
            "tokens": ["#031", "#044", "DIV", "#005", "#070"],
            "raw_transliteration": "#031 #044 / #005 #070",
            "n_signs": 4,
            "source": "younger_online",
            "source_citation": "test",
            "fetched_at": "2026-05-05T00:00:00Z",
        },
        {
            "id": "CHIC #003",
            "site": "Knossos",
            "support": "seal",
            "period": None,
            "transcription_confidence": "partial",
            "tokens": ["#005", "#070", "#044", "#031", "#005"],
            "raw_transliteration": "#005 #070 #044 #031 #005",
            "n_signs": 5,
            "source": "younger_online",
            "source_citation": "test",
            "fetched_at": "2026-05-05T00:00:00Z",
        },
        {
            "id": "CHIC #004",
            "site": "Mallia",
            "support": "medallion",
            "period": None,
            "transcription_confidence": "clean",
            "tokens": ["#070", "#031"],
            "raw_transliteration": "#070 #031",
            "n_signs": 2,
            "source": "younger_online",
            "source_citation": "test",
            "fetched_at": "2026-05-05T00:00:00Z",
        },
        {
            "id": "CHIC #005",
            "site": "Petras",
            "support": "nodulus",
            "period": None,
            "transcription_confidence": "clean",
            "tokens": ["#044", "#005", "#070", "DIV", "#031", "#005"],
            "raw_transliteration": "#044 #005 #070 / #031 #005",
            "n_signs": 5,
            "source": "younger_online",
            "source_citation": "test",
            "fetched_at": "2026-05-05T00:00:00Z",
        },
    ]


def _toy_pool_yaml(pool_name: str, entries: list[dict]) -> dict:
    return {
        "pool": pool_name,
        "source_citation": "test fixture",
        "license": "test fixture",
        "fetched_at": "2026-05-05T00:00:00Z",
        "entries": entries,
    }


def _toy_substrate_entries() -> list[dict]:
    return [
        {
            "surface": "abe",
            "phonemes": ["a", "b", "e"],
            "region": "test",
            "citation": "toy fixture",
        },
        {
            "surface": "ban",
            "phonemes": ["b", "a", "n"],
            "region": "test",
            "citation": "toy fixture",
        },
    ]


def _toy_control_entries() -> list[dict]:
    return [
        {
            "surface": "eba",
            "phonemes": ["e", "b", "a"],
            "region": "phonotactic_control_test",
            "citation": "toy fixture",
        },
        {
            "surface": "nab",
            "phonemes": ["n", "a", "b"],
            "region": "phonotactic_control_test",
            "citation": "toy fixture",
        },
    ]


def _toy_lm_json_text(name: str = "basque") -> str:
    """Build a tiny LM via build_model and dump it to its canonical JSON."""
    tokens = ["<W>", "a", "b", "a", "n", "<W>", "<W>", "b", "a", "<W>"]
    model = build_model(name=name, tokens=tokens, alpha=1.0)
    return model.to_json()


class ChicSubstrateRunSmoke(unittest.TestCase):
    """End-to-end driver on a 5-record toy."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="chic_v3_smoke_"))
        # Tmp layout (mirrors repo).
        self.corpora = self.tmp / "corpora" / "cretan_hieroglyphic"
        self.pools = self.tmp / "pools"
        self.pool_schemas = self.pools / "schemas"
        self.hypotheses = self.tmp / "hypotheses" / "auto"
        self.results = self.tmp / "results"
        self.lm_dir = self.tmp / "harness" / "external_phoneme_models"
        for d in (
            self.corpora,
            self.pools,
            self.pool_schemas,
            self.hypotheses,
            self.results,
            self.lm_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)

        # Toy CHIC corpus.
        chic_path = self.corpora / "syllabographic.jsonl"
        with chic_path.open("w") as fh:
            for rec in _toy_chic_records():
                fh.write(json.dumps(rec, sort_keys=True) + "\n")

        # Pool schema is needed; copy the real one in.
        real_schema = (
            _REPO_ROOT / "pools" / "schemas" / "pool.v1.schema.json"
        )
        shutil.copy(real_schema, self.pool_schemas / "pool.v1.schema.json")

        # Toy pool YAMLs (substrate + control for one of the 4 pools).
        # We use 'aquitanian' so the chic_substrate_run dispatch table
        # picks the basque LM with the matching control name.
        sub = _toy_pool_yaml("aquitanian", _toy_substrate_entries())
        ctrl = _toy_pool_yaml("control_aquitanian", _toy_control_entries())
        (self.pools / "aquitanian.yaml").write_text(
            yaml.safe_dump(sub, sort_keys=False), encoding="utf-8"
        )
        (self.pools / "control_aquitanian.yaml").write_text(
            yaml.safe_dump(ctrl, sort_keys=False), encoding="utf-8"
        )

        # Toy basque LM.
        (self.lm_dir / "basque.json").write_text(
            _toy_lm_json_text("basque"), encoding="utf-8"
        )

        # The hypothesis schema is also referenced by the orchestrator;
        # keep the absolute reference into the real repo by using
        # repo_root pointed at the real repo root, but write outputs
        # into the tmpdir.

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_pipeline_produces_artifacts(self):
        chic_path = self.corpora / "syllabographic.jsonl"
        result = chic_run(
            chic_corpus=chic_path,
            pools_dir=self.pools,
            hypotheses_dir=self.hypotheses,
            results_dir=self.results,
            ext_model_dir=self.lm_dir,
            cap_per_entry=10,
            top_k_gate=2,
            top_per_pool=10,
            n_min=1,
            pools=["aquitanian"],
            progress=False,
            note="smoke",
            repo_root=_REPO_ROOT,  # for hypothesis-path relativisation
        )

        # Manifest + hypothesis YAMLs.
        sub_manifest = self.hypotheses / "chic_aquitanian.manifest.jsonl"
        ctrl_manifest = self.hypotheses / "chic_control_aquitanian.manifest.jsonl"
        self.assertTrue(sub_manifest.exists())
        self.assertTrue(ctrl_manifest.exists())
        sub_rows = [
            json.loads(l) for l in sub_manifest.read_text().splitlines() if l
        ]
        self.assertGreater(len(sub_rows), 0)
        # YAMLs are content-addressed; manifest hash must match a file.
        for row in sub_rows[:5]:
            sha8 = row["hypothesis_hash"].split(":", 1)[1][:8]
            yaml_path = self.hypotheses / "chic_aquitanian" / f"{sha8}.yaml"
            self.assertTrue(yaml_path.exists())

        # Score sidecar.
        sidecar = self.results / "experiments.external_phoneme_perplexity_v0.chic.jsonl"
        self.assertTrue(sidecar.exists())
        rows = [
            json.loads(l) for l in sidecar.read_text().splitlines() if l
        ]
        self.assertGreater(len(rows), 0)
        for r in rows:
            self.assertEqual(r["metric"], "external_phoneme_perplexity_v0")
            self.assertEqual(r["language"], "basque")
            self.assertIn("score", r)
            self.assertIn("hypothesis_hash", r)

        # Per-pool rollup markdown.
        rollup = self.results / "rollup.bayesian_posterior.aquitanian.chic.md"
        self.assertTrue(rollup.exists())
        text = rollup.read_text()
        self.assertIn("Acceptance gate", text)
        self.assertIn("`aquitanian`", text)

        # Combined view.
        combined = self.results / "rollup.bayesian_posterior.chic.md"
        self.assertTrue(combined.exists())

        # Summary returned by run().
        self.assertEqual(len(result["summaries"]), 1)
        s = result["summaries"][0]
        self.assertEqual(s["pool"], "aquitanian")
        self.assertEqual(s["control_pool"], "control_aquitanian")
        self.assertEqual(s["language"], "basque")
        self.assertIn(s["gate"], ("PASS", "FAIL"))
        self.assertGreater(s["n_paired_windows"], 0)

    def test_rerun_is_idempotent(self):
        """Re-running with the same inputs should produce byte-identical
        manifests and the same gate verdict (deterministic pipeline)."""
        chic_path = self.corpora / "syllabographic.jsonl"
        first = chic_run(
            chic_corpus=chic_path,
            pools_dir=self.pools,
            hypotheses_dir=self.hypotheses,
            results_dir=self.results,
            ext_model_dir=self.lm_dir,
            cap_per_entry=5,
            top_k_gate=2,
            top_per_pool=10,
            n_min=1,
            pools=["aquitanian"],
            progress=False,
            note="smoke",
            repo_root=_REPO_ROOT,
        )
        sub_manifest = self.hypotheses / "chic_aquitanian.manifest.jsonl"
        sidecar = self.results / "experiments.external_phoneme_perplexity_v0.chic.jsonl"
        first_manifest = sub_manifest.read_bytes()
        first_rows = sidecar.read_text().count("\n")

        second = chic_run(
            chic_corpus=chic_path,
            pools_dir=self.pools,
            hypotheses_dir=self.hypotheses,
            results_dir=self.results,
            ext_model_dir=self.lm_dir,
            cap_per_entry=5,
            top_k_gate=2,
            top_per_pool=10,
            n_min=1,
            pools=["aquitanian"],
            progress=False,
            note="smoke",
            repo_root=_REPO_ROOT,
        )
        # Manifest is byte-identical (content-addressed).
        self.assertEqual(sub_manifest.read_bytes(), first_manifest)
        # Sidecar grew by zero rows on the resume run (resume cache hit).
        self.assertEqual(sidecar.read_text().count("\n"), first_rows)
        # Gate verdict matches.
        self.assertEqual(
            first["summaries"][0]["gate"], second["summaries"][0]["gate"]
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
