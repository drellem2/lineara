#!/usr/bin/env python3
"""Build pools/linear_b_carryover.yaml from the curated anchor hypotheses.

The 20 ``anchor_*.yaml`` and ``v4_anchor_*.yaml`` curated hypotheses
under ``hypotheses/curated/`` carry ``source_pool: linear_b_carryover``
and pin Linear-B carryover values (Ventris-Chadwick 1956, Younger 2020)
to specific Linear-A sign sequences. mg-4664 promotes those anchors to
a first-class pool so the existing v8 / v9 / v10 / v11 pipeline can
treat them as a positive-control substrate (the anchors propose
KNOWN-correct readings under the Linear-B sister-syllabary, so under a
Mycenaean-Greek LM they MUST clear the right-tail bayesian gate or
the framework is broken on a known case).

Idempotent: re-runs produce a byte-identical YAML. Entries are sorted
by ``surface`` and dedup'd; if multiple anchor YAMLs propose the same
``surface`` (e.g. ``kupa`` and ``kupa3``), each unique surface gets one
pool entry.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CURATED = _REPO_ROOT / "hypotheses" / "curated"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_anchor_hypotheses(curated_dir: Path) -> list[dict]:
    out: list[dict] = []
    for path in sorted(curated_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=_StringDateLoader)
        if not doc:
            continue
        if doc.get("source_pool") != "linear_b_carryover":
            continue
        out.append(doc)
    return out


def _entry_from_anchor(anchor: dict) -> dict:
    """Project an anchor hypothesis onto a pool-entry dict.

    Pool entries are unordered surfaces; the inscription-pinning is
    rebuilt by the bulk generator against the Linear-A corpus.
    """
    surface = anchor["root"]["surface"]
    phonemes = list(anchor["root"]["phonemes"])
    entry = {
        "surface": surface,
        "phonemes": phonemes,
    }
    gloss_hint = anchor["root"].get("gloss_hint")
    if gloss_hint:
        # Pool schema's "gloss" is the human-readable English gloss; the
        # anchor calls it ``gloss_hint``. Normalize to the schema key.
        entry["gloss"] = gloss_hint
    citation = anchor["root"].get("citation")
    if citation:
        entry["citation"] = citation
    # Region tag: the substrate identity is "Linear-B carryover" — every
    # entry shares the same region so the GG1 metric can find them via
    # the existing _GG1_REGION_COMPAT 'linear_b' rows.
    entry["region"] = "linear_b_carryover"
    return entry


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(
        doc, sort_keys=False, allow_unicode=True, default_flow_style=False
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--curated-dir", type=Path, default=_DEFAULT_CURATED)
    ap.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS_DIR)
    ap.add_argument("--repo-root", type=Path, default=_REPO_ROOT)
    args = ap.parse_args(argv)

    anchors = _load_anchor_hypotheses(args.curated_dir)
    if not anchors:
        print(
            f"no anchor hypotheses with source_pool=linear_b_carryover under "
            f"{args.curated_dir}",
            file=sys.stderr,
        )
        return 2

    # Deterministic dedup by surface; first-seen anchor wins for the
    # gloss/citation. The walk order is alphabetical on filename so
    # duplicates resolve consistently across re-runs.
    seen: dict[str, dict] = {}
    for anchor in anchors:
        entry = _entry_from_anchor(anchor)
        seen.setdefault(entry["surface"], entry)
    entries = [seen[s] for s in sorted(seen)]

    pool_doc = {
        "pool": "linear_b_carryover",
        "source_citation": (
            "Linear-B carryover values from the canonical Linear-A → Linear-B "
            "syllabogram identification (Ventris & Chadwick 1956). Per-anchor "
            "citations to Younger 2020 (Linear A texts in phonetic transcription, "
            "online edition), Schoep 2002 (The Administration of Neopalatial "
            "Crete), Salgarella 2020 (Aegean Linear Script(s)), and Palmer 1995 "
            "(\"ku-ro and ki-ro in Linear A\"). The anchors are committed under "
            "hypotheses/curated/{anchor,v4_anchor}_*.yaml; this pool is a "
            "promotion of the same surfaces to a first-class substrate pool so "
            "the v8/v9/v10/v11 pipeline can score them under a Mycenaean-Greek "
            "external phoneme LM as a positive control (mg-4664).\n"
        ),
        "license": (
            "Cited fair-use of secondary sources for compilation of the "
            "Linear-B carryover values. Underlying inscriptions and the "
            "Ventris-Chadwick 1956 syllabogram identifications are in the "
            "public domain.\n"
        ),
        "fetched_at": "2026-05-04T00:00:00Z",
        "entries": entries,
    }

    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(pool_doc)

    out_path = args.pools_dir / "linear_b_carryover.yaml"
    text = _dump_yaml(pool_doc)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != text:
        out_path.write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "pool_path": str(out_path.relative_to(args.repo_root)),
                "n_entries": len(entries),
                "surfaces": [e["surface"] for e in entries],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
