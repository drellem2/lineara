#!/usr/bin/env python3
"""Build a *polluted* substrate pool by mixing real entries with deliberately-
conjectural ones (mg-6b73, harness v14 — held-out pool-curation test).

The polluted pool is a **test artifact**, not a research claim. Its purpose
is to test the framework's curation-sensitivity: does the v10 right-tail
bayesian PASS on Aquitanian survive when we deliberately inject 50% phono-
tactically-matched conjectural surfaces tagged as if they were real
substrate roots?

For one substrate pool (default ``aquitanian``):

  * **Real half.** Every entry from the substrate pool is carried over with
    its original surface, phonemes, gloss, semantic_field, region, etc.,
    and tagged ``provenance: real``.
  * **Conjectural half.** Same number of entries (153 for Aquitanian),
    drawn from the substrate pool's marginal phoneme-frequency histogram
    and length distribution — same algorithm as
    ``scripts/build_control_pools.py`` — but with a **distinct seed**
    (``sha256("polluted_<pool>:conjectural")[:16]``) so the conjectural
    surfaces do not collide with the matched control pool. Each
    conjectural entry is tagged ``provenance: conjectural``, ``region:
    aquitania`` (so it is indistinguishable from real entries to the
    candidate generator's source_pool routing), and its ``semantic_field``
    is left unset (``null``).
  * **Surface uniqueness.** Conjectural surfaces are forced unique against
    real surfaces *and* prior conjectural surfaces. Collisions trigger a
    deterministic redraw, then a deterministic seed bump if redraws
    exhaust ``_REDRAW_LIMIT``. Re-running produces a byte-identical YAML.
  * **Phoneme-class filter.** The candidate generator skips entries whose
    phonemes span fewer than two distinct phoneme classes (V/S/C). The
    builder applies the same filter to conjectural draws so every emitted
    conjectural entry actually generates candidates downstream.

Output:

  * ``pools/polluted_aquitanian.yaml`` — 306 entries (153 real + 153
    conjectural), schema-valid, deterministic.
  * ``pools/polluted_aquitanian.README.md`` — construction documentation
    that prominently warns this pool is a test artifact, not a substrate
    claim.

Idempotent. Re-running with the same substrate pool ⇒ byte-identical
outputs.

Usage:
    python3 scripts/build_polluted_pool.py
    python3 scripts/build_polluted_pool.py --pool aquitanian
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"

_SUPPORTED_BASES = ("aquitanian",)
_REDRAW_LIMIT = 50

# Mirror of generate_candidates._phoneme_class — kept inline to avoid
# importing the generator (which loads the corpus at import time).
_VOWELS = frozenset("aeiouAEIOU")
_SONORANTS = frozenset("lrnmñLRNMÑ")


def _phoneme_class(p: str) -> str:
    if not p:
        return "C"
    h = p[0]
    if h in _VOWELS:
        return "V"
    if h in _SONORANTS:
        return "S"
    return "C"


def _spans_two_classes(phonemes: list[str]) -> bool:
    return len({_phoneme_class(p) for p in phonemes}) >= 2


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings (mirror of
    ``scripts/generate_candidates.py``)."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _seed_for(base_pool: str) -> int:
    """Deterministic 64-bit seed for the conjectural draws.

    Distinct from the matched-control seed
    (``sha256("control_pool:<pool>")[:16]``) so conjectural surfaces and
    matched-control surfaces draw from disjoint random streams.
    """
    digest = hashlib.sha256(
        f"polluted_{base_pool}:conjectural".encode("utf-8")
    ).hexdigest()
    return int(digest[:16], 16)


def _load_pool(pool_path: Path) -> dict:
    with pool_path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def _phoneme_histogram(pool: dict) -> Counter:
    counter: Counter = Counter()
    for entry in pool["entries"]:
        for ph in entry["phonemes"]:
            counter[ph] += 1
    return counter


def _length_distribution(pool: dict) -> Counter:
    return Counter(len(e["phonemes"]) for e in pool["entries"])


def _weighted_sample(
    rng: random.Random, items: list[str], weights: list[float], k: int
) -> list[str]:
    return rng.choices(items, weights=weights, k=k)


def build_conjectural_entries(
    *,
    base_pool_name: str,
    base_pool: dict,
    region_tag: str,
) -> list[dict]:
    """Generate len(base_pool['entries']) conjectural entries.

    Each conjectural entry shares its length with the corresponding real
    entry (so the polluted pool's overall length distribution is exactly
    2× the real pool's). Phonemes are sampled from the real pool's
    marginal phoneme-frequency histogram. Surfaces are forced unique
    against real surfaces and prior conjecturals; entries that fail the
    two-class phoneme filter are also redrawn so every emitted entry
    will produce candidates downstream.
    """
    histogram = _phoneme_histogram(base_pool)
    phonemes = sorted(histogram.keys())
    weights = [float(histogram[p]) for p in phonemes]

    real_surfaces = {e["surface"] for e in base_pool["entries"]}
    seed = _seed_for(base_pool_name)
    rng = random.Random(seed)

    out: list[dict] = []
    seen_conjectural: set[str] = set()

    for idx, real_entry in enumerate(base_pool["entries"]):
        n = len(real_entry["phonemes"])
        attempts = 0
        bumps = 0
        while True:
            sampled = _weighted_sample(rng, phonemes, weights, n)
            surface = "".join(sampled)
            collides = (
                surface in real_surfaces or surface in seen_conjectural
            )
            two_classes_ok = _spans_two_classes(sampled)
            if not collides and two_classes_ok:
                break
            attempts += 1
            if attempts >= _REDRAW_LIMIT:
                bumps += 1
                rng = random.Random(seed + idx * 1009 + bumps)
                attempts = 0
        seen_conjectural.add(surface)
        out.append(
            {
                "surface": surface,
                "phonemes": sampled,
                "region": region_tag,
                "provenance": "conjectural",
                "citation": (
                    f"Synthetic conjectural entry generated by "
                    f"scripts/build_polluted_pool.py from the "
                    f"{base_pool_name} pool's marginal phoneme distribution "
                    f"and length distribution. Test artifact for the held-"
                    f"out pool-curation test (mg-6b73); not a substrate "
                    f"claim."
                ),
            }
        )
    return out


def build_real_entries(base_pool: dict) -> list[dict]:
    """Carry every base-pool entry over verbatim, tagging
    ``provenance: real`` (and preserving every other field)."""
    out: list[dict] = []
    for entry in base_pool["entries"]:
        copy = dict(entry)
        copy["provenance"] = "real"
        out.append(copy)
    return out


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(
        doc, sort_keys=False, allow_unicode=True, default_flow_style=False
    )


def build_polluted_pool(
    base_pool_name: str,
    pools_dir: Path,
) -> dict:
    """Build, validate, and write the polluted pool YAML.

    Returns a summary dict.
    """
    base_path = pools_dir / f"{base_pool_name}.yaml"
    base_pool = _load_pool(base_path)

    polluted_pool_name = f"polluted_{base_pool_name}"
    real_entries = build_real_entries(base_pool)
    conjectural_entries = build_conjectural_entries(
        base_pool_name=base_pool_name,
        base_pool=base_pool,
        region_tag="aquitania" if base_pool_name == "aquitanian" else base_pool_name,
    )
    entries = real_entries + conjectural_entries

    seed_hex = f"{_seed_for(base_pool_name):016x}"
    polluted_doc = {
        "pool": polluted_pool_name,
        "source_citation": (
            f"DELIBERATELY POLLUTED test pool generated from "
            f"{base_pool_name}.yaml (mg-6b73). Half real, half "
            f"conjectural — a test artifact for the held-out pool-"
            f"curation test, NOT a substrate claim. Conjectural "
            f"surfaces are drawn from the {base_pool_name} pool's "
            f"marginal phoneme-frequency histogram and length "
            f"distribution under deterministic seed 0x{seed_hex} "
            f"(sha256(\"polluted_{base_pool_name}:conjectural\")"
            f"[:16]). See pools/{polluted_pool_name}.README.md for "
            f"the full construction algorithm and a prominent warning "
            f"that this pool exists only to test the framework's "
            f"curation-sensitivity.\n"
        ),
        "license": (
            "Mixed: real entries inherit the underlying "
            f"{base_pool_name} pool's license (cited fair-use of "
            "Trask 1997 and Gorrochategui 1984). Conjectural entries "
            "are synthetic data with no source-text content, "
            "released under the same terms as the lineara repo.\n"
        ),
        "fetched_at": "2026-05-04T00:00:00Z",
        "entries": entries,
    }

    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(polluted_doc)

    out_path = pools_dir / f"{polluted_pool_name}.yaml"
    yaml_text = _dump_yaml(polluted_doc)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != yaml_text:
        out_path.write_text(yaml_text, encoding="utf-8")

    try:
        rel_out = out_path.resolve().relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        rel_out = str(out_path)

    surfaces = [e["surface"] for e in entries]
    duplicates = [s for s, c in Counter(surfaces).items() if c > 1]
    if duplicates:
        raise RuntimeError(
            f"polluted pool {polluted_pool_name!r} has duplicate surfaces: "
            f"{duplicates[:5]!r}"
        )

    n_real = sum(1 for e in entries if e.get("provenance") == "real")
    n_conjectural = sum(1 for e in entries if e.get("provenance") == "conjectural")

    return {
        "base_pool": base_pool_name,
        "polluted_pool": polluted_pool_name,
        "n_entries": len(entries),
        "n_real": n_real,
        "n_conjectural": n_conjectural,
        "polluted_path": rel_out,
        "seed_hex": f"0x{seed_hex}",
    }


def write_readme(
    base_pool_name: str,
    pools_dir: Path,
) -> Path:
    """Write the per-pool README documenting the construction algorithm
    and prominently warning that this pool is a test artifact."""
    base_path = pools_dir / f"{base_pool_name}.yaml"
    polluted_path = pools_dir / f"polluted_{base_pool_name}.yaml"
    base_pool = _load_pool(base_path)
    polluted_pool = _load_pool(polluted_path)

    real_entries = [e for e in polluted_pool["entries"] if e.get("provenance") == "real"]
    conj_entries = [e for e in polluted_pool["entries"] if e.get("provenance") == "conjectural"]

    sub_hist = _phoneme_histogram(base_pool)
    pol_hist = _phoneme_histogram(polluted_pool)
    sub_lens = _length_distribution(base_pool)
    pol_lens = _length_distribution(polluted_pool)

    seed_hex = f"0x{_seed_for(base_pool_name):016x}"

    lines: list[str] = []
    lines.append(f"# polluted_{base_pool_name} — DELIBERATELY POLLUTED TEST POOL\n")
    lines.append(
        "> ⚠️ **This pool is a test artifact, not a research claim.** "
        f"Half of its {len(polluted_pool['entries'])} entries are real "
        f"{base_pool_name} substrate roots; the other half are "
        f"deliberately-conjectural surfaces tagged as if they were real. "
        f"Do **NOT** use this pool to make substrate claims, build "
        f"derived dictionaries, or train downstream models. It exists "
        f"solely for the harness v14 / mg-6b73 held-out pool-curation "
        f"test: does the v10 right-tail bayesian PASS on the clean "
        f"`{base_pool_name}` pool survive 50% conjectural pollution?\n"
    )
    lines.append("## Why this pool exists\n")
    lines.append(
        "v10 (mg-d26d) found that the per-surface bayesian posterior "
        f"on the clean `{base_pool_name}` pool clears the right-tail "
        "Mann-Whitney U gate against its phonotactic control. v12+v13 "
        "narrowed the interpretation of that PASS to two readings:\n\n"
        "1. **Substrate-LM-phonotactic kinship.** The framework "
        "genuinely detects that real Aquitanian surfaces are more "
        "Basque-LM-likely than random Aquitanian-shaped surfaces — "
        "tolerant of mixed-cleanness pools.\n"
        "2. **Curation-sensitivity.** The framework's PASS depends on "
        "the substrate pool being uniformly real; pollution by "
        "conjectural-but-phonotactically-matched surfaces would "
        "collapse the PASS.\n\n"
        "This polluted pool is the binary discriminator for the "
        "two readings. See mg-6b73 for the full pre-registered analysis "
        "plan.\n"
    )
    lines.append("## Construction algorithm\n")
    lines.append(
        f"1. **Real half.** All {len(real_entries)} entries from "
        f"`pools/{base_pool_name}.yaml` are carried over verbatim "
        f"(surface, phonemes, gloss, semantic_field, region, "
        f"attestations, citation) and tagged `provenance: real`.\n"
        f"2. **Conjectural half.** {len(conj_entries)} synthetic "
        f"entries are drawn under the same algorithm as "
        f"`scripts/build_control_pools.py`:\n"
        f"   - Length: same length as the i-th real entry (so the "
        f"length distribution doubles exactly).\n"
        f"   - Phonemes: sampled with replacement from the real pool's "
        f"marginal phoneme-frequency histogram.\n"
        f"   - Surface: concatenation of sampled phonemes.\n"
        f"   - **Region tag:** `region: aquitania` (so the conjectural "
        f"entries are indistinguishable from real ones to the candidate "
        f"generator's source_pool routing — the test asks whether the "
        f"framework can detect the conjecturals despite that "
        f"camouflage).\n"
        f"   - **Provenance tag:** `provenance: conjectural` (so the "
        f"rollup post-processing can compute the provenance breakdown "
        f"of the top-20).\n"
        f"   - **No semantic_field.** Conjecturals have no real-world "
        f"semantics; the field is omitted entirely (treated as null by "
        f"the geographic_genre_fit_v1 metric, which falls back to "
        f"neutral 0.5 — irrelevant for the v8 metric this pool is "
        f"actually scored under).\n"
        f"3. **Uniqueness.** Conjectural surfaces are forced unique "
        f"against (a) the real pool's surfaces and (b) prior "
        f"conjecturals. Collisions trigger redraws up to "
        f"{_REDRAW_LIMIT} times, then a deterministic seed bump — the "
        f"output stays reproducible.\n"
        "4. **Phoneme-class filter.** Every conjectural entry must "
        "span at least two distinct phoneme classes (V/S/C); single-"
        "class draws are redrawn so the candidate generator does not "
        "skip any conjectural entry.\n"
        f"5. **Determinism.** Seed = `{seed_hex}` "
        f"(sha256(\"polluted_{base_pool_name}:conjectural\")[:16]). "
        f"Re-running the builder produces a byte-identical YAML. "
        f"Asserted by `harness/tests/test_polluted_pool.py`.\n"
    )

    lines.append("## Pool counts\n")
    lines.append(f"- Real entries:         **{len(real_entries)}**")
    lines.append(f"- Conjectural entries:  **{len(conj_entries)}**")
    lines.append(f"- Total entries:        **{len(polluted_pool['entries'])}**")
    lines.append("")

    lines.append("## Length distribution\n")
    lines.append("Real and conjectural entries share length pairwise (i-th "
                 "conjectural matches i-th real). The polluted pool's "
                 "length distribution is exactly 2× the real pool's.\n")
    lines.append("| length | real pool | polluted pool |")
    lines.append("|---:|---:|---:|")
    for L in sorted(set(sub_lens) | set(pol_lens)):
        lines.append(f"| {L} | {sub_lens.get(L, 0)} | {pol_lens.get(L, 0)} |")
    lines.append("")

    lines.append("## Phoneme inventory and frequency\n")
    lines.append(
        "The conjectural draw uses the real pool's marginal phoneme "
        "frequency, so the polluted pool's overall histogram should "
        "track ~2× the real pool's in expectation. Realized counts are "
        "approximate due to finite sample size.\n"
    )
    lines.append("| phoneme | real pool count | real pool % | polluted pool count | polluted pool % |")
    lines.append("|---|---:|---:|---:|---:|")
    sub_total = sum(sub_hist.values()) or 1
    pol_total = sum(pol_hist.values()) or 1
    for ph in sorted(set(sub_hist) | set(pol_hist)):
        s = sub_hist.get(ph, 0)
        p = pol_hist.get(ph, 0)
        lines.append(
            f"| `{ph}` | {s} | {100 * s / sub_total:.1f}% | "
            f"{p} | {100 * p / pol_total:.1f}% |"
        )
    lines.append("")

    lines.append("## What this pool is and is not\n")
    lines.append(
        "- **IS:** A test fixture for the framework's curation-"
        "sensitivity. Half-conjectural by design.\n"
        "- **IS NOT:** A research claim. Conjectural surfaces are "
        "synthetic. Do not cite, do not gloss, do not derive secondary "
        "artifacts.\n"
        "- **IS NOT:** A replacement for `pools/aquitanian.yaml`. The "
        "clean Aquitanian pool remains the substrate-claim pool; this "
        "polluted pool is parallel scaffolding.\n"
        f"- **Matched control:** `pools/control_polluted_{base_pool_name}.yaml`, "
        "built by `scripts/build_control_pools.py`. Length and "
        "phoneme-inventory matched to the polluted pool, drawn under a "
        "distinct seed.\n"
    )

    out_path = pools_dir / f"polluted_{base_pool_name}.README.md"
    text = "\n".join(lines)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != text:
        out_path.write_text(text, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--pool",
        choices=_SUPPORTED_BASES,
        default="aquitanian",
        help="Substrate pool to pollute (default: aquitanian).",
    )
    parser.add_argument(
        "--pools-dir",
        type=Path,
        default=_DEFAULT_POOLS_DIR,
        help="Directory containing pool YAMLs.",
    )
    args = parser.parse_args(argv)

    summary = build_polluted_pool(args.pool, args.pools_dir)
    readme = write_readme(args.pool, args.pools_dir)
    try:
        summary["readme_path"] = readme.resolve().relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        summary["readme_path"] = str(readme)
    print(
        f"built polluted pool: {summary['polluted_path']}  "
        f"(n={summary['n_entries']}, real={summary['n_real']}, "
        f"conjectural={summary['n_conjectural']}, seed={summary['seed_hex']})",
        file=sys.stderr,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
