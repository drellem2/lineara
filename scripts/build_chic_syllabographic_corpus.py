#!/usr/bin/env python3
"""Build the CHIC syllabographic-only corpus stream (mg-9700, chic-v3).

Reads ``corpora/cretan_hieroglyphic/all.jsonl`` (the chic-v0 corpus) and
filters each inscription's token list to syllabographic-class signs only,
per ``pools/cretan_hieroglyphic_signs.yaml`` (chic-v1 classification).
Non-syllabographic content (ideograms, fractions, numerals, uncertain
sign IDs, wholly-unknown markers) is rewritten to ``DIV`` so it acts as
a structural break for the substrate framework's window splitter and
the external-LM run extractor.

Output: ``corpora/cretan_hieroglyphic/syllabographic.jsonl`` — same
record schema as the chic-v0 corpus, but with a filtered ``tokens``
array and a refreshed ``n_signs`` count. Inscriptions whose filtered
token list contains zero syllabograms are dropped.

This stream is the analogue of Linear A's ``corpus/all.jsonl`` for the
chic-v3 substrate framework run; the run scripts read the *filtered*
stream rather than re-filtering on every load.

Determinism: byte-identical output given the same chic-v0 corpus +
sign-classification YAML. No RNG.

Usage:
    python3 scripts/build_chic_syllabographic_corpus.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_INPUT = _REPO_ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
_DEFAULT_OUTPUT = (
    _REPO_ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
)
_DEFAULT_STATS = (
    _REPO_ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic_stats.md"
)
_DEFAULT_SIGNS_YAML = _REPO_ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"


class _StringDateLoader(yaml.SafeLoader):
    pass


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_syllabographic_signs(signs_yaml: Path) -> set[str]:
    """Return the set of CHIC sign IDs classified syllabographic.

    The chic-v1 classification (#001-#100 syllabographic; #101+ ideogram)
    is materialised in ``pools/cretan_hieroglyphic_signs.yaml`` with
    per-sign override capability. We honour that file rather than the
    numeric-range heuristic so future ambiguous-sign re-classifications
    flow through automatically.
    """
    with signs_yaml.open("r", encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=_StringDateLoader)
    syllabographic: set[str] = set()
    for entry in doc.get("signs", []):
        if entry.get("sign_class") == "syllabographic":
            syllabographic.add(entry["id"])
    return syllabographic


def filter_tokens(
    tokens: list[str], syllabographic: set[str]
) -> list[str]:
    """Filter a chic-v0 token list to syllabograms-and-DIVs only.

    Rewrite rules:
      - ``#NNN`` → kept iff #NNN is in ``syllabographic`` (else → DIV).
      - ``[?:#NNN]`` → DIV (uncertain readings drop out of the framework).
      - ``[?]`` → DIV (wholly-unknown marker).
      - ``NUM:N`` → DIV (numeric quantity is not a syllabogram).
      - ``DIV`` → DIV (preserved).

    Consecutive DIVs are collapsed; leading/trailing DIVs are trimmed.
    """
    out: list[str] = []
    for tok in tokens:
        if tok in syllabographic:
            out.append(tok)
        else:
            # Everything else collapses to a structural break.
            if out and out[-1] != "DIV":
                out.append("DIV")
            # else: skip leading DIVs / consecutive DIVs.
    while out and out[-1] == "DIV":
        out.pop()
    return out


def build(
    *,
    input_jsonl: Path,
    output_jsonl: Path,
    stats_md: Path,
    signs_yaml: Path,
) -> dict:
    """Load chic-v0, filter to syllabographic stream, write outputs."""
    syllabographic = load_syllabographic_signs(signs_yaml)
    if not syllabographic:
        raise SystemExit(
            f"no syllabographic signs found in {signs_yaml}; refusing to "
            "produce an empty stream"
        )

    records: list[dict] = []
    with input_jsonl.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])

    out_records: list[dict] = []
    dropped_no_signs = 0
    sign_counter: Counter = Counter()
    div_count = 0

    for rec in records:
        filtered = filter_tokens(rec["tokens"], syllabographic)
        n_signs = sum(1 for t in filtered if t != "DIV")
        if n_signs == 0:
            dropped_no_signs += 1
            continue
        new = dict(rec)
        new["tokens"] = filtered
        new["n_signs"] = n_signs
        new["raw_transliteration_chic_v0"] = rec.get("raw_transliteration", "")
        new["raw_transliteration"] = " ".join(filtered)
        new["filter_provenance"] = (
            "chic-v3 syllabographic-only filter; non-syllabographic "
            "tokens (ideograms, fractions, numerals, uncertain readings, "
            "wholly-unknown markers) collapsed to DIV"
        )
        out_records.append(new)
        for tok in filtered:
            if tok == "DIV":
                div_count += 1
            else:
                sign_counter[tok] += 1

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as fh:
        for rec in out_records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    total_sign_tokens = sum(sign_counter.values())
    distinct_signs = len(sign_counter)
    block_lengths: list[int] = []
    for rec in out_records:
        block: list[str] = []
        for tok in rec["tokens"]:
            if tok == "DIV":
                if block:
                    block_lengths.append(len(block))
                    block = []
            else:
                block.append(tok)
        if block:
            block_lengths.append(len(block))

    stats: dict = {
        "input_records": len(records),
        "output_records": len(out_records),
        "dropped_no_signs": dropped_no_signs,
        "total_sign_tokens": total_sign_tokens,
        "distinct_syllabographic_signs": distinct_signs,
        "syllabographic_signs_in_inventory": len(syllabographic),
        "div_tokens": div_count,
        "blocks": len(block_lengths),
        "max_block_length": max(block_lengths) if block_lengths else 0,
        "mean_block_length": (
            sum(block_lengths) / len(block_lengths) if block_lengths else 0.0
        ),
        "block_length_histogram": dict(Counter(block_lengths)),
    }

    md_lines: list[str] = []
    a = md_lines.append
    a("# CHIC syllabographic-only corpus (chic-v3, mg-9700)")
    a("")
    a(
        "Generated by `scripts/build_chic_syllabographic_corpus.py` from "
        "`corpora/cretan_hieroglyphic/all.jsonl` (chic-v0) using the "
        "sign-class assignments in "
        "`pools/cretan_hieroglyphic_signs.yaml` (chic-v1)."
    )
    a("")
    a(
        "Filter: keep `#NNN` tokens classified syllabographic; rewrite "
        "everything else (ideograms, fractions, numerals, uncertain "
        "readings, wholly-unknown markers) to `DIV` so it acts as a "
        "structural break in the substrate framework's window splitter "
        "and the external-LM run extractor."
    )
    a("")
    a("## Coverage")
    a("")
    a("| Metric | Count |")
    a("|---|---|")
    a(f"| Input chic-v0 inscriptions | {stats['input_records']} |")
    a(f"| Filtered output inscriptions | **{stats['output_records']}** |")
    a(f"| Dropped (no syllabograms after filter) | {stats['dropped_no_signs']} |")
    a(f"| Syllabographic sign tokens kept | **{stats['total_sign_tokens']}** |")
    a(
        f"| Distinct syllabographic signs observed | "
        f"{stats['distinct_syllabographic_signs']} of "
        f"{stats['syllabographic_signs_in_inventory']} in inventory |"
    )
    a(f"| `DIV` tokens | {stats['div_tokens']} |")
    a(f"| Maximal-syllabographic-run blocks (between DIVs) | {stats['blocks']} |")
    a(f"| Max block length | {stats['max_block_length']} |")
    a(
        f"| Mean block length | {stats['mean_block_length']:.2f} |"
    )
    a("")
    a("## Block-length histogram")
    a("")
    a("| length | blocks |")
    a("|---:|---:|")
    for L in sorted(stats["block_length_histogram"]):
        a(f"| {L} | {stats['block_length_histogram'][L]} |")
    a("")
    a("## Comparison with Linear A")
    a("")
    a(
        "Linear A's `corpus/all.jsonl` carries ~5,000 syllabogram "
        "tokens across ~760 inscriptions (mg-99df, mg-d5ef). CHIC's "
        "syllabographic-only stream is roughly an order of magnitude "
        "smaller. Per the chic-v3 brief: lower statistical power for "
        "the right-tail bayesian gate is expected; per-pool p-values "
        "should be interpreted with this corpus-size caveat in mind."
    )
    a("")

    stats_md.parent.mkdir(parents=True, exist_ok=True)
    stats_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=_DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT)
    parser.add_argument("--stats", type=Path, default=_DEFAULT_STATS)
    parser.add_argument(
        "--signs-yaml", type=Path, default=_DEFAULT_SIGNS_YAML
    )
    args = parser.parse_args(argv)

    stats = build(
        input_jsonl=args.input,
        output_jsonl=args.output,
        stats_md=args.stats,
        signs_yaml=args.signs_yaml,
    )
    print(json.dumps(stats, indent=2, sort_keys=True))
    print(
        f"wrote {args.output} ({stats['output_records']} records, "
        f"{stats['total_sign_tokens']} syllabographic tokens, "
        f"{stats['blocks']} blocks)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
