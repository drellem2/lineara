"""Hypothesis loading, validation, and canonical hashing."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_SCHEMA_PATH = Path(__file__).parent / "schemas" / "hypothesis.v0.schema.json"


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates/timestamps as plain strings.

    PyYAML's default resolver promotes things like ``2026-05-04`` to
    ``datetime.date``; that breaks JSON-Schema validation against our string
    'created' field and means hypothesis authors have to remember to quote
    every date. We strip the timestamp resolver so unquoted dates round-trip
    as the literal string the author wrote.
    """


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_schema() -> dict:
    with _SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_VALIDATOR = Draft202012Validator(_load_schema())


def load_and_validate(path: Path) -> dict:
    """Load a hypothesis YAML, validate against the v0 schema, return the dict.

    Raises jsonschema.ValidationError on schema mismatch.
    """
    with path.open("r", encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=_StringDateLoader)
    if doc is None:
        raise ValueError(f"hypothesis file is empty: {path}")
    if not isinstance(doc, dict):
        raise ValueError(f"hypothesis root must be a mapping: {path}")
    _VALIDATOR.validate(doc)
    return doc


def canonical_hash(hypothesis: dict) -> str:
    """sha256 over a canonical JSON serialization of the hypothesis.

    Canonicalization: keys sorted, no whitespace, ensure_ascii=False.
    Comments and YAML-specific formatting are intentionally lost — the hash
    reflects the *meaning* of the hypothesis, not its presentation.
    """
    payload = json.dumps(hypothesis, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
