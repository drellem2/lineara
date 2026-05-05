"""Schema + smoke tests for the CHIC sign inventory (mg-c7e3, chic-v1).

Validates the per-sign metadata file produced by
`scripts/build_chic_signs.py`:

  pools/cretan_hieroglyphic_signs.yaml          per-sign classification
  pools/schemas/chic_signs.v1.schema.json       JSON Schema for the yaml
  pools/cretan_hieroglyphic_signs.README.md     classification rule + citations
  results/chic_sign_inventory.md                inventory table
  results/chic_vs_linear_a_sign_inventory_comparison.md   distribution comparison

Run directly:
  python3 -m harness.tests.test_chic_signs
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
_POOL_YAML = _REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
_POOL_README = _REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.README.md"
_POOL_SCHEMA = _REPO_ROOT / "pools" / "schemas" / "chic_signs.v1.schema.json"
_INV_REPORT = _REPO_ROOT / "results" / "chic_sign_inventory.md"
_COMP_REPORT = (
    _REPO_ROOT / "results" / "chic_vs_linear_a_sign_inventory_comparison.md"
)

_SIGN_ID_RE = re.compile(r"^#\d{3}$")
_AB_ID_RE = re.compile(r"^AB\d+$")
_ALLOWED_CLASSES = {"syllabographic", "ideogram", "ambiguous"}
_ALLOWED_CONFIDENCES = {"consensus", "proposed", "debated"}


def _have_yaml_lib() -> bool:
    try:
        import yaml  # noqa: F401
        return True
    except Exception:
        return False


def _load_yaml(path: Path) -> dict:
    """Load the chic_signs yaml. Falls back to a tiny inline parser if
    PyYAML is not installed (the build script doesn't depend on PyYAML
    either; tests should run on a bare interpreter)."""
    text = path.read_text(encoding="utf-8")
    if _have_yaml_lib():
        import yaml
        return yaml.safe_load(text)
    return _parse_chic_signs_yaml(text)


def _parse_chic_signs_yaml(text: str) -> dict:
    """Minimal parser tuned to the layout emitted by build_chic_signs.py.

    Only handles: top-level scalars, top-level multi-line `|` blocks,
    and the `signs:` list of dicts (one entry per `- id: ...`).
    Sufficient for the schema-validation tests without taking a PyYAML
    dependency.
    """
    out: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip() or ln.lstrip().startswith("#"):
            i += 1
            continue
        if ln.startswith("signs:"):
            signs, i = _parse_signs_list(lines, i + 1)
            out["signs"] = signs
            continue
        m = re.match(r"^(\w+):\s*(.*)$", ln)
        if m:
            key, val = m.group(1), m.group(2)
            if val == "|":
                # Multi-line block scalar.
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


def _parse_signs_list(lines: list[str], start: int) -> tuple[list[dict], int]:
    out: list[dict] = []
    cur: dict | None = None
    cur_paleo: list[dict] | None = None
    cur_paleo_entry: dict | None = None
    cur_subdict_key: str | None = None
    cur_subdict: dict | None = None
    i = start
    while i < len(lines):
        ln = lines[i]
        if not ln.startswith("  ") and not ln.startswith("- "):
            # Hit a new top-level key (or EOF).
            if ln.strip() and not ln.startswith(" "):
                break
        if ln.startswith("- id:"):
            if cur is not None:
                if cur_paleo is not None:
                    cur["paleographic_candidates"] = cur_paleo
                if cur_subdict is not None and cur_subdict_key:
                    cur[cur_subdict_key] = cur_subdict
                out.append(cur)
            m = re.match(r"^- id:\s*(.*)$", ln)
            cur = {"id": _coerce_scalar(m.group(1))}
            cur_paleo = None
            cur_paleo_entry = None
            cur_subdict = None
            cur_subdict_key = None
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        if ln.startswith("  paleographic_candidates:"):
            if cur_subdict is not None and cur_subdict_key:
                cur[cur_subdict_key] = cur_subdict
                cur_subdict = None
                cur_subdict_key = None
            cur_paleo = []
            i += 1
            continue
        if ln.startswith("  - linear_a_sign:"):
            if cur_paleo_entry is not None:
                cur_paleo.append(cur_paleo_entry)
            m = re.match(r"^  - linear_a_sign:\s*(.*)$", ln)
            cur_paleo_entry = {"linear_a_sign": _coerce_scalar(m.group(1))}
            i += 1
            continue
        if cur_paleo_entry is not None and ln.startswith("    "):
            m = re.match(r"^    (\w+):\s*(.*)$", ln)
            if m:
                cur_paleo_entry[m.group(1)] = _coerce_scalar(m.group(2))
                i += 1
                continue
        # Sub-dict (position_fingerprint, genre_fingerprint).
        m = re.match(r"^  (\w+):\s*$", ln)
        if m and ln.endswith(":"):
            if cur_paleo_entry is not None:
                cur_paleo.append(cur_paleo_entry)
                cur_paleo_entry = None
            if cur_subdict is not None and cur_subdict_key:
                cur[cur_subdict_key] = cur_subdict
            cur_subdict_key = m.group(1)
            cur_subdict = {}
            i += 1
            continue
        m_sub = re.match(r"^    (\w+):\s*(.*)$", ln)
        if m_sub and cur_subdict is not None and cur_paleo_entry is None:
            cur_subdict[m_sub.group(1)] = _coerce_scalar(m_sub.group(2))
            i += 1
            continue
        m = re.match(r"^  (\w+):\s*(.*)$", ln)
        if m:
            if cur_paleo_entry is not None:
                cur_paleo.append(cur_paleo_entry)
                cur_paleo_entry = None
            if cur_subdict is not None and cur_subdict_key:
                cur[cur_subdict_key] = cur_subdict
                cur_subdict = None
                cur_subdict_key = None
            key, val = m.group(1), m.group(2)
            if val.endswith("{}"):
                cur[key] = {}
            else:
                cur[key] = _coerce_scalar(val)
        i += 1
    if cur is not None:
        if cur_paleo_entry is not None:
            cur_paleo.append(cur_paleo_entry)
        if cur_paleo is not None:
            cur["paleographic_candidates"] = cur_paleo
        if cur_subdict is not None and cur_subdict_key:
            cur[cur_subdict_key] = cur_subdict
        out.append(cur)
    return out, i


def _coerce_scalar(s: str):
    s = s.strip()
    if not s:
        return ""
    if s == "''":
        return ""
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1].replace("''", "'")
    if s == "null":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if s.startswith("{") and s.endswith("}"):
        return {}
    if s.startswith("[") and s.endswith("]"):
        return []
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


class TestChicSignsArtifacts(unittest.TestCase):
    """All chic-v1 deliverables exist."""

    def test_yaml_exists(self) -> None:
        self.assertTrue(_POOL_YAML.exists(), "pools/cretan_hieroglyphic_signs.yaml missing — run scripts/build_chic_signs.py")

    def test_readme_exists(self) -> None:
        self.assertTrue(_POOL_README.exists())

    def test_schema_exists(self) -> None:
        self.assertTrue(_POOL_SCHEMA.exists())

    def test_inventory_report_exists(self) -> None:
        self.assertTrue(_INV_REPORT.exists())

    def test_comparison_report_exists(self) -> None:
        self.assertTrue(_COMP_REPORT.exists())


class TestChicSignsSchema(unittest.TestCase):
    """Per-entry schema validation across the yaml."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _POOL_YAML.exists():
            raise unittest.SkipTest("pool yaml not built")
        cls.doc = _load_yaml(_POOL_YAML)
        cls.signs: list[dict] = cls.doc["signs"]

    def test_top_level_fields(self) -> None:
        self.assertEqual(self.doc["catalog"], "cretan_hieroglyphic_signs")
        self.assertEqual(self.doc["version"], 1)
        self.assertIsInstance(self.doc.get("classification_rule"), str)
        self.assertGreater(len(self.doc["classification_rule"]), 100)
        self.assertIsInstance(self.doc.get("source_citation"), str)
        self.assertIn("Olivier", self.doc["source_citation"])

    def test_signs_nonempty(self) -> None:
        self.assertGreater(len(self.signs), 0)

    def test_signs_unique_ids(self) -> None:
        ids = [s["id"] for s in self.signs]
        self.assertEqual(len(ids), len(set(ids)))

    def test_sign_ids_well_formed(self) -> None:
        for s in self.signs:
            with self.subTest(id=s["id"]):
                self.assertRegex(s["id"], _SIGN_ID_RE)

    def test_sign_ids_sorted(self) -> None:
        ids_int = [int(s["id"].lstrip("#")) for s in self.signs]
        self.assertEqual(ids_int, sorted(ids_int))

    def test_sign_class_enum(self) -> None:
        for s in self.signs:
            with self.subTest(id=s["id"]):
                self.assertIn(s["sign_class"], _ALLOWED_CLASSES)

    def test_frequency_nonnegative(self) -> None:
        for s in self.signs:
            with self.subTest(id=s["id"]):
                self.assertIsInstance(s["frequency"], int)
                self.assertGreaterEqual(s["frequency"], 1)
                self.assertEqual(
                    s["frequency"],
                    s["frequency_clean"] + s["frequency_uncertain"],
                    "frequency should equal clean + uncertain",
                )

    def test_classification_matches_numeric_range(self) -> None:
        """Per the documented rule, #001-#100 default to syllabographic
        and #101+ default to ideogram. Any deviation must be 'ambiguous'
        (per the override mechanism)."""
        for s in self.signs:
            n = int(s["id"].lstrip("#"))
            with self.subTest(id=s["id"]):
                if 1 <= n <= 100:
                    self.assertIn(s["sign_class"], ("syllabographic", "ambiguous"))
                elif 101 <= n <= 399:
                    self.assertIn(s["sign_class"], ("ideogram", "ambiguous"))
                else:
                    self.assertEqual(s["sign_class"], "ambiguous")

    def test_position_fingerprint_fractions(self) -> None:
        for s in self.signs:
            with self.subTest(id=s["id"]):
                pf = s.get("position_fingerprint") or {}
                if not pf:
                    continue
                total = sum(pf.values())
                self.assertGreater(total, 0)
                # Allow for rounding noise (3-decimal rounding per bucket).
                self.assertAlmostEqual(total, 1.0, delta=0.01)
                for bucket in pf:
                    self.assertIn(
                        bucket,
                        {"start", "middle", "end", "single"},
                    )

    def test_paleographic_candidates_well_formed(self) -> None:
        for s in self.signs:
            cands = s.get("paleographic_candidates")
            if not cands:
                continue
            with self.subTest(id=s["id"]):
                for c in cands:
                    self.assertRegex(c["linear_a_sign"], _AB_ID_RE)
                    self.assertIn(c["confidence"], _ALLOWED_CONFIDENCES)
                    self.assertGreater(len(c["citation"]), 20)
                    self.assertIsInstance(c["linear_b_value"], str)

    def test_paleographic_candidates_only_on_syllabographic_signs(self) -> None:
        """Per ticket §4: paleographic candidates apply to signs classified
        as syllabographic. Catch silent reclassification regressions."""
        for s in self.signs:
            cands = s.get("paleographic_candidates")
            if cands:
                with self.subTest(id=s["id"]):
                    self.assertEqual(
                        s["sign_class"], "syllabographic",
                        f"sign {s['id']} carries paleographic candidates "
                        f"but is classified {s['sign_class']!r}",
                    )

    def test_top_level_counts_consistent(self) -> None:
        """If summary fields are present, they should match the signs list."""
        n_total = self.doc.get("n_signs_total")
        if n_total is not None:
            self.assertEqual(n_total, len(self.signs))
        n_syll = self.doc.get("n_syllabographic")
        if n_syll is not None:
            self.assertEqual(
                n_syll,
                sum(1 for s in self.signs if s["sign_class"] == "syllabographic"),
            )
        n_ideo = self.doc.get("n_ideogram")
        if n_ideo is not None:
            self.assertEqual(
                n_ideo,
                sum(1 for s in self.signs if s["sign_class"] == "ideogram"),
            )


class TestPaleographicCandidates(unittest.TestCase):
    """Spot checks on the curated CHIC ↔ Linear A candidate list."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _POOL_YAML.exists():
            raise unittest.SkipTest("pool yaml not built")
        cls.doc = _load_yaml(_POOL_YAML)
        cls.signs = {s["id"]: s for s in cls.doc["signs"]}

    def test_candidate_count_in_expected_range(self) -> None:
        """Ticket says expected ~10-20 per scholarly literature."""
        n = sum(
            len(s.get("paleographic_candidates") or [])
            for s in self.signs.values()
        )
        self.assertGreaterEqual(n, 10, "too few paleographic candidates")
        self.assertLessEqual(n, 30, "too many paleographic candidates (sanity bound)")

    def test_at_least_one_consensus_match(self) -> None:
        """Ticket §4 expects some matches strong enough to act as v2 anchors."""
        consensus = []
        for s in self.signs.values():
            for c in s.get("paleographic_candidates") or []:
                if c["confidence"] == "consensus":
                    consensus.append((s["id"], c["linear_a_sign"]))
        self.assertGreater(
            len(consensus), 0,
            "no consensus paleographic candidates flagged",
        )

    def test_chic_070_maps_to_AB60_ra(self) -> None:
        """CHIC #070 ↔ Linear A AB60 (= ra) is one of the most-secure
        scholarly matches (Salgarella 2020 p. 144). Catch regressions in
        the curated candidate list."""
        if "#070" not in self.signs:
            self.skipTest("#070 not in corpus")
        cands = self.signs["#070"].get("paleographic_candidates") or []
        self.assertTrue(
            any(c["linear_a_sign"] == "AB60" and c["linear_b_value"] == "ra"
                for c in cands),
            "expected #070 ↔ AB60 (ra) candidate",
        )


class TestSchemaJsonStructure(unittest.TestCase):
    """Static checks on pools/schemas/chic_signs.v1.schema.json."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _POOL_SCHEMA.exists():
            raise unittest.SkipTest("schema file not built")
        cls.schema = json.loads(_POOL_SCHEMA.read_text(encoding="utf-8"))

    def test_schema_is_jsonschema_2020_12(self) -> None:
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_schema_top_level_required(self) -> None:
        req = set(self.schema["required"])
        for k in ("catalog", "version", "classification_rule", "signs"):
            self.assertIn(k, req)

    def test_schema_sign_class_enum(self) -> None:
        sign_item = self.schema["properties"]["signs"]["items"]
        cls_enum = set(sign_item["properties"]["sign_class"]["enum"])
        self.assertEqual(cls_enum, _ALLOWED_CLASSES)


class TestSchemaValidatesYaml(unittest.TestCase):
    """If jsonschema is installed, run a real validation pass."""

    @classmethod
    def setUpClass(cls) -> None:
        try:
            import jsonschema  # noqa: F401
        except Exception:
            raise unittest.SkipTest("jsonschema not available")
        if not _POOL_YAML.exists() or not _POOL_SCHEMA.exists():
            raise unittest.SkipTest("artifacts not built")
        cls.schema = json.loads(_POOL_SCHEMA.read_text(encoding="utf-8"))
        cls.doc = _load_yaml(_POOL_YAML)

    def test_yaml_validates_against_schema(self) -> None:
        import jsonschema
        # Drop None values that arose from minimal-parser fallback (which
        # may emit "" where pyyaml emits None).
        jsonschema.validate(instance=self.doc, schema=self.schema)


if __name__ == "__main__":
    unittest.main()
