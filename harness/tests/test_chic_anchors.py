"""Schema + smoke tests for the CHIC paleographic anchor pool (mg-362d, chic-v2).

Validates the artifacts produced by `scripts/build_chic_anchors.py`:

  pools/cretan_hieroglyphic_anchors.yaml          anchor pool
  pools/cretan_hieroglyphic_anchors.README.md     anchor-tier rule + citations
  pools/schemas/chic_anchors.v1.schema.json       JSON Schema
  results/chic_partial_readings.md                per-inscription map
  results/chic_anchor_density_leaderboard.md      top-30 by coverage
  results/chic_mg_perplexity_sanity_check.md      MG-LM cross-check

Run directly:
  python3 -m harness.tests.test_chic_anchors
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

_ANCHORS_YAML = _REPO_ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"
_ANCHORS_README = _REPO_ROOT / "pools" / "cretan_hieroglyphic_anchors.README.md"
_ANCHORS_SCHEMA = _REPO_ROOT / "pools" / "schemas" / "chic_anchors.v1.schema.json"
_PARTIAL_READINGS = _REPO_ROOT / "results" / "chic_partial_readings.md"
_LEADERBOARD = _REPO_ROOT / "results" / "chic_anchor_density_leaderboard.md"
_PERPLEXITY = _REPO_ROOT / "results" / "chic_mg_perplexity_sanity_check.md"

_CHIC_ID_RE = re.compile(r"^#\d{3}$")
_AB_ID_RE = re.compile(r"^AB\d+$")
_TIERS = {"tier-1", "tier-2"}
_CHIC_V1_CONFIDENCES = {"consensus", "proposed", "debated"}


# ---------------------------------------------------------------------------
# Tiny, layout-aware YAML reader for the anchors yaml. The build script
# emits a stable shape (top-level scalars + a single `|` block per
# multi-line field + a flat `anchors:` list of dicts), so we can parse
# without depending on PyYAML.
# ---------------------------------------------------------------------------


def _coerce_scalar(s: str) -> object:
    s = s.strip()
    if s == "":
        return ""
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1].replace("''", "'")
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


def _load_anchors_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    out: dict = {"anchors": []}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ln.startswith("anchors:"):
            anchors, i = _parse_anchor_list(lines, i + 1)
            out["anchors"] = anchors
            continue
        m = re.match(r"^(\w+):\s*(.*)$", ln)
        if m:
            key, val = m.group(1), m.group(2)
            if val == "|":
                buf: list[str] = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""):
                    buf.append(lines[i][2:] if lines[i].startswith("  ") else "")
                    i += 1
                out[key] = "\n".join(buf).rstrip("\n")
                continue
            out[key] = _coerce_scalar(val)
        i += 1
    return out


def _parse_anchor_list(lines: list[str], start: int) -> tuple[list[dict], int]:
    out: list[dict] = []
    cur: dict | None = None
    i = start
    while i < len(lines):
        ln = lines[i]
        if ln and not ln.startswith(" ") and not ln.startswith("-"):
            break
        m_dash = re.match(r"^- (\w+):\s*(.*)$", ln)
        if m_dash:
            if cur is not None:
                out.append(cur)
            cur = {m_dash.group(1): _coerce_scalar(m_dash.group(2))}
            i += 1
            continue
        m = re.match(r"^  (\w+):\s*(.*)$", ln)
        if m and cur is not None:
            cur[m.group(1)] = _coerce_scalar(m.group(2))
        i += 1
    if cur is not None:
        out.append(cur)
    return out, i


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestChicAnchorsArtifacts(unittest.TestCase):

    def test_anchor_files_exist(self) -> None:
        for path in (
            _ANCHORS_YAML,
            _ANCHORS_README,
            _ANCHORS_SCHEMA,
            _PARTIAL_READINGS,
            _LEADERBOARD,
            _PERPLEXITY,
        ):
            self.assertTrue(path.is_file(), f"missing artifact: {path}")

    def test_schema_is_valid_json(self) -> None:
        schema = json.loads(_ANCHORS_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "Cretan Hieroglyphic paleographic anchor pool (v1)")
        self.assertEqual(schema["properties"]["catalog"]["const"], "cretan_hieroglyphic_anchors")
        self.assertEqual(schema["properties"]["version"]["const"], 1)
        self.assertIn("anchors", schema["properties"])

    def test_anchors_yaml_shape(self) -> None:
        data = _load_anchors_yaml(_ANCHORS_YAML)
        self.assertEqual(data.get("catalog"), "cretan_hieroglyphic_anchors")
        self.assertEqual(data.get("version"), 1)
        self.assertIsInstance(data.get("anchors"), list)
        self.assertGreaterEqual(len(data["anchors"]), 10, "ticket asks for ≥10 anchors")

    def test_each_anchor_well_formed(self) -> None:
        data = _load_anchors_yaml(_ANCHORS_YAML)
        seen_chic: set[str] = set()
        n_t1 = 0
        n_t2 = 0
        for a in data["anchors"]:
            chic = a["chic_sign"]
            self.assertRegex(chic, _CHIC_ID_RE.pattern, f"bad chic_sign: {chic!r}")
            self.assertNotIn(chic, seen_chic, f"duplicate anchor for {chic}")
            seen_chic.add(chic)
            self.assertRegex(
                a["linear_a_sign"], _AB_ID_RE.pattern,
                f"bad linear_a_sign: {a['linear_a_sign']!r}",
            )
            self.assertIsInstance(a["linear_b_carryover_phonetic"], str)
            self.assertGreater(len(a["linear_b_carryover_phonetic"]), 0)
            self.assertIn(a["confidence_tier"], _TIERS)
            self.assertIn(a["chic_v1_confidence"], _CHIC_V1_CONFIDENCES)
            self.assertIsInstance(a["paleographic_citation"], str)
            self.assertGreater(len(a["paleographic_citation"]), 10)
            self.assertIsInstance(a["linear_b_citation"], str)
            self.assertIn("Ventris", a["linear_b_citation"])
            if a["confidence_tier"] == "tier-1":
                n_t1 += 1
                self.assertEqual(
                    a["chic_v1_confidence"], "consensus",
                    "tier-1 should map only to chic-v1 consensus",
                )
            else:
                n_t2 += 1
                self.assertIn(
                    a["chic_v1_confidence"], {"proposed", "debated"},
                    "tier-2 should map to chic-v1 proposed/debated",
                )
        self.assertEqual(data.get("n_tier_1"), n_t1)
        self.assertEqual(data.get("n_tier_2"), n_t2)
        self.assertEqual(data.get("n_anchors_total"), n_t1 + n_t2)

    def test_partial_readings_table_present(self) -> None:
        text = _PARTIAL_READINGS.read_text(encoding="utf-8")
        # Table header.
        self.assertIn("| CHIC id |", text)
        self.assertIn("| coverage |", text)
        # Corpus rollup line.
        self.assertIn("Corpus-wide anchor coverage", text)
        # At least one anchored phoneme row should appear (`ra` anchor).
        self.assertIn(" ra ", text)

    def test_leaderboard_has_top_30(self) -> None:
        text = _LEADERBOARD.read_text(encoding="utf-8")
        # Count rank rows (starts with `| 1 |`, `| 2 |`, ...).
        rank_rows = [
            ln for ln in text.splitlines()
            if re.match(r"^\| \d+ \| CHIC ", ln)
        ]
        self.assertEqual(len(rank_rows), 30, "leaderboard should have 30 rows")
        # Top-1 rank line should report coverage 1.0000 (the corpus has
        # many short, fully-anchored inscriptions).
        self.assertIn("1.0000", rank_rows[0])

    def test_perplexity_table_present(self) -> None:
        text = _PERPLEXITY.read_text(encoding="utf-8")
        self.assertIn("Mean per-char log-likelihood", text)
        # 30 scored rows.
        rank_rows = [
            ln for ln in text.splitlines()
            if re.match(r"^\| \d+ \| CHIC ", ln)
        ]
        self.assertEqual(len(rank_rows), 30, "perplexity table should have 30 rows")
        # NOT a decipherment claim — the document explicitly disclaims this.
        self.assertIn("NOT a decipherment claim", text)

    def test_readme_lists_all_anchors(self) -> None:
        readme = _ANCHORS_README.read_text(encoding="utf-8")
        data = _load_anchors_yaml(_ANCHORS_YAML)
        for a in data["anchors"]:
            self.assertIn(
                f"| {a['chic_sign']} |", readme,
                f"README missing {a['chic_sign']}",
            )


class TestDeterminism(unittest.TestCase):

    def test_yaml_byte_identical_on_rebuild(self) -> None:
        """Re-running the build script produces byte-identical artifacts."""
        import subprocess
        original = _ANCHORS_YAML.read_bytes()
        original_partial = _PARTIAL_READINGS.read_bytes()
        original_leaderboard = _LEADERBOARD.read_bytes()
        original_perplexity = _PERPLEXITY.read_bytes()
        result = subprocess.run(
            ["python3", "-m", "scripts.build_chic_anchors"],
            cwd=_REPO_ROOT,
            check=True,
            capture_output=True,
        )
        self.assertEqual(_ANCHORS_YAML.read_bytes(), original, "anchors.yaml drifted on rebuild")
        self.assertEqual(_PARTIAL_READINGS.read_bytes(), original_partial)
        self.assertEqual(_LEADERBOARD.read_bytes(), original_leaderboard)
        self.assertEqual(_PERPLEXITY.read_bytes(), original_perplexity)


if __name__ == "__main__":
    unittest.main()
