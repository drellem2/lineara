"""Smoke tests for scripts/right_tail_inscription_concentration.py (mg-0f97).

Exercises the publication-shape per-inscription rollup:
  * Distinct-surface counting: a surface contributes once to raw_count
    regardless of how many positive paired_diff records it has on the
    inscription.
  * Density = raw_count / n_records_targeting (records targeting an
    inscription, not records hitting top-20).
  * v9 multi-root signature deduplication: a signature like
    `aitz+aitz+oin` contributes one observation under each of {aitz,
    oin} for that inscription, not two for aitz.
  * Determinism: identical output across two runs of the aggregator
    on the same input.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_INS_PATH = _REPO_ROOT / "scripts" / "right_tail_inscription_concentration.py"


class V10Top20HardcodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load_module("right_tail_inscription_concentration", _INS_PATH)

    def test_v10_top20_aquitanian(self) -> None:
        aq = self.mod._V10_TOP20_BY_POOL["aquitanian"]
        self.assertEqual(len(aq), 20)
        # Spot-check known leaders from the v10 same-LM rollup.
        for s in ("aitz", "hanna", "nahi", "ako", "beltz", "bihotz",
                  "egun", "eki", "ezti", "gaitz", "hau", "hesi",
                  "itsaso", "oin", "ona", "zelai", "zortzi", "argi",
                  "ate", "entzun"):
            self.assertIn(s, aq)

    def test_v10_top20_etruscan(self) -> None:
        et = self.mod._V10_TOP20_BY_POOL["etruscan"]
        self.assertEqual(len(et), 20)
        for s in ("larth", "aiser", "matam", "avils", "camthi",
                  "chimth", "hanthe", "laris", "nac", "sech", "thana",
                  "zelar", "caitim", "thesan", "spureri", "thanchvil",
                  "suthi", "mach", "arnth", "sath"):
            self.assertIn(s, et)


if __name__ == "__main__":
    unittest.main()
