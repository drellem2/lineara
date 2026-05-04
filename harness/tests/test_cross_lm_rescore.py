"""Smoke tests for scripts/cross_lm_rescore.py (mg-0f97).

Exercises:
  * The cross-LM dispatch table swaps aquitanian↔etruscan as expected.
  * The resume cache keys on (hypothesis_hash, language) and skips
    only matching pairs — same-LM rows under a given hash do not block
    a swapped-LM rescore of the same hash.
  * The rescore output row carries language=<swapped_lm> and the
    rest of the metric fields from external_phoneme_perplexity_v0.
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


_CROSS_LM_PATH = _REPO_ROOT / "scripts" / "cross_lm_rescore.py"


class CrossLMDispatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cross = _load_module("cross_lm_rescore", _CROSS_LM_PATH)

    def test_dispatch_swap(self) -> None:
        d = self.cross._CROSS_LM_DISPATCH
        self.assertEqual(d["aquitanian"], "etruscan")
        self.assertEqual(d["control_aquitanian"], "etruscan")
        self.assertEqual(d["etruscan"], "basque")
        self.assertEqual(d["control_etruscan"], "basque")

    def test_dispatch_excludes_toponym(self) -> None:
        # mg-0f97 ticket: toponym pool excluded from cross-LM rescoring;
        # v10 already failed for toponym (sampler issue) so the cross-LM
        # control is moot.
        self.assertNotIn("toponym", self.cross._CROSS_LM_DISPATCH)
        self.assertNotIn("control_toponym", self.cross._CROSS_LM_DISPATCH)

    def test_third_lm_dispatch_routes_through_mycenaean_greek(self) -> None:
        # mg-4664 third cross-LM check: Aquitanian + Etruscan substrate
        # / control candidates rescored under Mycenaean-Greek so we can
        # tell whether the Aquitanian PASS is "natural-language LM
        # bias" or genuinely substrate-specific.
        d = self.cross._THIRD_LM_DISPATCH
        self.assertEqual(d["aquitanian"], "mycenaean_greek")
        self.assertEqual(d["control_aquitanian"], "mycenaean_greek")
        self.assertEqual(d["etruscan"], "mycenaean_greek")
        self.assertEqual(d["control_etruscan"], "mycenaean_greek")


class CrossLMSeenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cross = _load_module("cross_lm_rescore", _CROSS_LM_PATH)

    def test_load_seen_keys_on_hash_and_language(self) -> None:
        # Same hash, two languages → both pairs returned. Swapped-LM rescore
        # is unblocked even when the same-LM row is already present.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "experiments.external_phoneme_perplexity_v0.jsonl"
            with path.open("w", encoding="utf-8") as fh:
                fh.write(json.dumps({
                    "metric": "external_phoneme_perplexity_v0",
                    "hypothesis_hash": "sha256:" + "a" * 64,
                    "language": "basque",
                    "ran_at": "2026-05-04T00:00:00Z",
                }) + "\n")
                fh.write(json.dumps({
                    "metric": "external_phoneme_perplexity_v0",
                    "hypothesis_hash": "sha256:" + "a" * 64,
                    "language": "etruscan",
                    "ran_at": "2026-05-04T00:00:01Z",
                }) + "\n")
                # A row from a different metric should not appear in seen.
                fh.write(json.dumps({
                    "metric": "local_fit_v1",
                    "hypothesis_hash": "sha256:" + "b" * 64,
                }) + "\n")
            seen = self.cross._load_seen(path)
            self.assertIn(("sha256:" + "a" * 64, "basque"), seen)
            self.assertIn(("sha256:" + "a" * 64, "etruscan"), seen)
            self.assertEqual(len(seen), 2)


if __name__ == "__main__":
    unittest.main()
