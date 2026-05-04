"""Hypothesis loading, validation, and canonical hashing.

Three shapes are supported:

* ``hypothesis.v0`` — *implicit* (no ``schema_version`` field). A partial
  corpus-global sign→phoneme mapping. Scored by ``compression_delta_v0``.
  This is the original shape.

* ``candidate_equation.v1`` — opt-in via ``schema_version: candidate_equation.v1``.
  A *local* hypothesis pinning a span of one inscription to a single
  candidate substrate root.

* ``candidate_signature.v1`` (mg-bef2, harness v9) — opt-in via
  ``schema_version: candidate_signature.v1``. A multi-root signature over a
  window of one inscription. The union of the roots' sign_to_phoneme entries
  is a non-conflicting partial sign→phoneme mapping that downstream metrics
  (notably ``external_phoneme_perplexity_v0``) consume directly.

The loader dispatches on the ``schema_version`` field and routes to the
appropriate JSON-Schema validator. All shapes coexist; existing v0/v1
hypothesis files do not need to be edited.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_SCHEMA_DIR = Path(__file__).parent / "schemas"
_V0_SCHEMA_PATH = _SCHEMA_DIR / "hypothesis.v0.schema.json"
_CANDIDATE_EQUATION_V1_SCHEMA_PATH = (
    _SCHEMA_DIR / "hypothesis.candidate_equation.v1.schema.json"
)
_CANDIDATE_SIGNATURE_V1_SCHEMA_PATH = (
    _SCHEMA_DIR / "hypothesis.candidate_signature.v1.schema.json"
)

SHAPE_V0 = "v0"
SHAPE_CANDIDATE_EQUATION_V1 = "candidate_equation.v1"
SHAPE_CANDIDATE_SIGNATURE_V1 = "candidate_signature.v1"


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


def _load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_V0_VALIDATOR = Draft202012Validator(_load_schema(_V0_SCHEMA_PATH))
_CANDIDATE_EQUATION_V1_VALIDATOR = Draft202012Validator(
    _load_schema(_CANDIDATE_EQUATION_V1_SCHEMA_PATH)
)
_CANDIDATE_SIGNATURE_V1_VALIDATOR = Draft202012Validator(
    _load_schema(_CANDIDATE_SIGNATURE_V1_SCHEMA_PATH)
)


def detect_shape(doc: dict) -> str:
    """Return the canonical shape tag for a parsed hypothesis dict."""
    sv = doc.get("schema_version")
    if sv is None:
        return SHAPE_V0
    if sv == "candidate_equation.v1":
        return SHAPE_CANDIDATE_EQUATION_V1
    if sv == "candidate_signature.v1":
        return SHAPE_CANDIDATE_SIGNATURE_V1
    raise ValueError(f"unknown hypothesis schema_version: {sv!r}")


def load_and_validate(path: Path) -> dict:
    """Load a hypothesis YAML, validate against the right schema, return the dict.

    Dispatches on the optional ``schema_version`` field. Files without one
    are treated as the original ``hypothesis.v0`` shape. Files with
    ``schema_version: candidate_equation.v1`` are validated against the
    candidate-equation schema.

    Raises ``jsonschema.ValidationError`` on schema mismatch, or ``ValueError``
    on an unknown schema_version.
    """
    with path.open("r", encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=_StringDateLoader)
    if doc is None:
        raise ValueError(f"hypothesis file is empty: {path}")
    if not isinstance(doc, dict):
        raise ValueError(f"hypothesis root must be a mapping: {path}")

    shape = detect_shape(doc)
    if shape == SHAPE_V0:
        _V0_VALIDATOR.validate(doc)
    elif shape == SHAPE_CANDIDATE_EQUATION_V1:
        _CANDIDATE_EQUATION_V1_VALIDATOR.validate(doc)
        _validate_candidate_equation_semantics(doc, path)
    elif shape == SHAPE_CANDIDATE_SIGNATURE_V1:
        _CANDIDATE_SIGNATURE_V1_VALIDATOR.validate(doc)
        _validate_candidate_signature_semantics(doc, path)
    else:  # pragma: no cover - guarded by detect_shape
        raise ValueError(f"unhandled hypothesis shape: {shape}")
    return doc


def _validate_candidate_equation_semantics(doc: dict, path: Path) -> None:
    """Enforce constraints the JSON Schema can't express on its own."""
    eq = doc["equation"]
    span = eq["span"]
    if span[0] > span[1]:
        raise ValueError(
            f"{path}: equation.span start ({span[0]}) must be <= end ({span[1]})"
        )
    phonemes = doc["root"]["phonemes"]
    sign_to_phoneme = eq["sign_to_phoneme"]
    if len(sign_to_phoneme) != len(phonemes):
        raise ValueError(
            f"{path}: sign_to_phoneme has {len(sign_to_phoneme)} entries; "
            f"root.phonemes has {len(phonemes)}; lengths must match"
        )
    # Order check: the phonemes listed (in insertion order) in sign_to_phoneme
    # must equal root.phonemes element-wise. This catches typos where the YAML
    # author writes the right phonemes in the wrong order.
    sign_to_phoneme_values = list(sign_to_phoneme.values())
    if sign_to_phoneme_values != phonemes:
        raise ValueError(
            f"{path}: sign_to_phoneme values {sign_to_phoneme_values!r} must equal "
            f"root.phonemes {phonemes!r} in order"
        )


def _validate_candidate_signature_semantics(doc: dict, path: Path) -> None:
    """Enforce constraints the JSON Schema can't express on its own.

    Checked here:
      * window.span[0] <= window.span[1].
      * Each root's span_within_window is well-formed and lies within the
        window.
      * Roots' spans are non-overlapping (sorted disjoint intervals).
      * sign_to_phoneme entries are consistent across roots — a sign that
        appears in multiple roots must map to the same phoneme everywhere.
      * Each root's sign_to_phoneme matches the phoneme inventory of
        root.phonemes (every distinct phoneme listed appears as a value).
    """
    window = doc["window"]
    w0, w1 = window["span"]
    if w0 > w1:
        raise ValueError(
            f"{path}: window.span start ({w0}) must be <= end ({w1})"
        )
    window_len = w1 - w0 + 1

    roots = doc["roots"]
    placed: list[tuple[int, int]] = []
    combined: dict[str, str] = {}
    for i, root in enumerate(roots):
        s, e = root["span_within_window"]
        if s > e:
            raise ValueError(
                f"{path}: roots[{i}] span_within_window start ({s}) must be "
                f"<= end ({e})"
            )
        if e >= window_len:
            raise ValueError(
                f"{path}: roots[{i}] span_within_window {[s, e]!r} extends "
                f"beyond the window length {window_len}"
            )
        for j, (ps, pe) in enumerate(placed):
            if not (e < ps or s > pe):
                raise ValueError(
                    f"{path}: roots[{i}] span_within_window {[s, e]!r} "
                    f"overlaps roots[{j}] span_within_window {[ps, pe]!r}"
                )
        placed.append((s, e))
        for sign, phoneme in root["sign_to_phoneme"].items():
            existing = combined.get(sign)
            if existing is not None and existing != phoneme:
                raise ValueError(
                    f"{path}: sign {sign!r} mapped to two different phonemes "
                    f"across roots: {existing!r} (earlier) vs {phoneme!r} "
                    f"(roots[{i}].surface={root['surface']!r})"
                )
            combined[sign] = phoneme


def signature_combined_mapping(doc: dict) -> dict[str, str]:
    """Build the union sign->phoneme mapping from a candidate_signature.v1 doc.

    Pre-validated by ``_validate_candidate_signature_semantics`` to be
    non-conflicting; this function does not re-check, only collects.
    """
    out: dict[str, str] = {}
    for root in doc["roots"]:
        for sign, phoneme in root["sign_to_phoneme"].items():
            out[sign] = phoneme
    return out


def canonical_hash(hypothesis: dict) -> str:
    """sha256 over a canonical JSON serialization of the hypothesis.

    Canonicalization: keys sorted, no whitespace, ensure_ascii=False.
    Comments and YAML-specific formatting are intentionally lost — the hash
    reflects the *meaning* of the hypothesis, not its presentation.
    """
    payload = json.dumps(hypothesis, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
