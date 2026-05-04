#!/usr/bin/env python3
"""Round-trip build: regenerate corpus/all.jsonl from per-inscription files.

Per-inscription JSON files under corpus/<site>/<id>.json are the source of
truth. This script re-aggregates them into corpus/all.jsonl in deterministic
(id-sorted) order, then validates every record against the schema.

Usage: python3 scripts/build_corpus.py [--strict]

Exits non-zero if any record fails schema validation, or if an inscription
file is malformed.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
SCHEMA = ROOT / "schema" / "inscription.schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA.read_text())


def load_records() -> list[dict]:
    records: list[dict] = []
    for path in sorted(CORPUS.rglob("*.json")):
        if path.name in {"all.jsonl"}:
            continue
        if path.parent == CORPUS:
            # Top-level non-record files (e.g. _skipped.json) live in CORPUS.
            continue
        try:
            rec = json.loads(path.read_text())
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"malformed JSON at {path}: {e}")
        records.append(rec)
    return records


def _type_match(value, schema_type) -> bool:
    types = [schema_type] if isinstance(schema_type, str) else list(schema_type)
    for t in types:
        if t == "null" and value is None:
            return True
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "object" and isinstance(value, dict):
            return True
        if t == "boolean" and isinstance(value, bool):
            return True
    return False


def validate(rec: dict, schema: dict) -> list[str]:
    """Tiny inline validator covering the subset of JSON Schema we use.

    We intentionally avoid an external dependency so the build script runs in
    a clean Python install.
    """
    errors: list[str] = []
    rid = rec.get("id", "<no id>")
    required = schema.get("required", [])
    for key in required:
        if key not in rec:
            errors.append(f"{rid}: missing required field '{key}'")
    props = schema.get("properties", {})
    additional = schema.get("additionalProperties", True)
    if additional is False:
        for key in rec:
            if key not in props:
                errors.append(f"{rid}: unexpected field '{key}'")
    for key, val in rec.items():
        sub = props.get(key)
        if not sub:
            continue
        if "type" in sub and not _type_match(val, sub["type"]):
            errors.append(f"{rid}: field '{key}' wrong type (got {type(val).__name__})")
            continue
        if "enum" in sub and val not in sub["enum"]:
            errors.append(f"{rid}: field '{key}' value {val!r} not in enum")
        if "minLength" in sub and isinstance(val, str) and len(val) < sub["minLength"]:
            errors.append(f"{rid}: field '{key}' shorter than minLength")
        if "minimum" in sub and isinstance(val, (int, float)) and val < sub["minimum"]:
            errors.append(f"{rid}: field '{key}' below minimum")
        if "pattern" in sub and isinstance(val, str):
            import re

            if not re.search(sub["pattern"], val):
                errors.append(f"{rid}: field '{key}' fails pattern {sub['pattern']}")
        if sub.get("type") == "array" and isinstance(val, list):
            item_schema = sub.get("items", {})
            for i, item in enumerate(val):
                if "type" in item_schema and not _type_match(item, item_schema["type"]):
                    errors.append(f"{rid}: tokens[{i}] wrong type")
                if "minLength" in item_schema and isinstance(item, str) and len(item) < item_schema["minLength"]:
                    errors.append(f"{rid}: tokens[{i}] shorter than minLength")
    return errors


def write_aggregate(records: list[dict]) -> None:
    out = CORPUS / "all.jsonl"
    sorted_recs = sorted(records, key=lambda r: r.get("id", ""))
    with out.open("w", encoding="utf-8") as f:
        for r in sorted_recs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit non-zero on any validation error")
    args = ap.parse_args()

    schema = load_schema()
    records = load_records()
    print(f"loaded {len(records)} records", file=sys.stderr)

    errors: list[str] = []
    for r in records:
        errors.extend(validate(r, schema))
    if errors:
        print(f"validation: {len(errors)} errors", file=sys.stderr)
        for e in errors[:50]:
            print(f"  {e}", file=sys.stderr)
        if args.strict or len(errors) > 0:
            return 1
    else:
        print("validation: all records valid", file=sys.stderr)

    write_aggregate(records)
    print(f"wrote corpus/all.jsonl ({len(records)} records)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
