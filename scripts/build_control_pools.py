#!/usr/bin/env python3
"""Build phonotactically-matched scramble *control* pools (mg-f419).

For each substrate pool (``aquitanian``, ``etruscan``, ``toponym``), emit a
parallel control pool with:

  * the same number of entries
  * the same length distribution (one control per substrate entry, same N)
  * phonemes sampled from the substrate pool's per-pool phoneme-frequency
    histogram (so the control's marginal phoneme distribution matches)
  * surface = concatenation of sampled phonemes (orthographic)
  * ``region`` = ``phonotactic_control_<pool_name>``
  * ``semantic_field`` unset (gg1 falls back to neutral 0.5)

The output is **deterministic and idempotent**: the seed is derived from
the substrate pool name (``hashlib.sha256(name).hexdigest()[:16]``), and
re-running produces byte-identical YAMLs. Surfaces within a control pool
are forced unique; if a collision occurs we redraw the offending entry up
to ``_REDRAW_LIMIT`` times, then bump the seed deterministically.

The control pool is a first-class pool (``pool: control_<name>``) and is
designed to flow through the same generator + sweep pipeline as the
substrate pools — see ``mg-f419`` ticket and the per-pool README.

Usage:
    python3 scripts/build_control_pools.py
    python3 scripts/build_control_pools.py --pool aquitanian
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"

_SUBSTRATE_POOLS = (
    "aquitanian",
    "etruscan",
    "toponym",
    "linear_b_carryover",
    "polluted_aquitanian",
)
_REDRAW_LIMIT = 50


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings (mirror of
    ``scripts/generate_candidates.py``)."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _seed_for(pool_name: str) -> int:
    """Deterministic 64-bit seed derived from the substrate pool name."""
    digest = hashlib.sha256(f"control_pool:{pool_name}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _load_substrate_pool(pool_path: Path) -> dict:
    with pool_path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def phoneme_histogram(pool: dict) -> Counter:
    """Counter of phoneme → count across every entry's phonemes list."""
    counter: Counter = Counter()
    for entry in pool["entries"]:
        for ph in entry["phonemes"]:
            counter[ph] += 1
    return counter


def length_distribution(pool: dict) -> Counter:
    """Counter of length → count across the pool's entries."""
    return Counter(len(e["phonemes"]) for e in pool["entries"])


def _weighted_sample(
    rng: random.Random, items: list[str], weights: list[float], k: int
) -> list[str]:
    """Sample ``k`` phonemes with replacement from ``items`` weighted by
    ``weights``. Uses ``random.choices`` so the sampling is reproducible
    given a seeded RNG."""
    return rng.choices(items, weights=weights, k=k)


def _build_control_entries(
    *,
    substrate_pool_name: str,
    substrate_pool: dict,
    region_tag: str,
) -> list[dict]:
    """Generate the control entries for one substrate pool.

    For each substrate entry we emit one control entry of the same length;
    phonemes are sampled from the substrate's marginal phoneme distribution.
    Surfaces are forced unique within the control pool by retrying up to
    ``_REDRAW_LIMIT`` times per entry; if a unique draw cannot be produced
    we bump the seed and continue (deterministic chain — same pool ⇒ same
    final entries).
    """
    histogram = phoneme_histogram(substrate_pool)
    phonemes = sorted(histogram.keys())
    weights = [float(histogram[p]) for p in phonemes]
    seed = _seed_for(substrate_pool_name)
    rng = random.Random(seed)

    control_entries: list[dict] = []
    surfaces_seen: set[str] = set()

    for idx, sub_entry in enumerate(substrate_pool["entries"]):
        n = len(sub_entry["phonemes"])
        attempts = 0
        while True:
            sampled = _weighted_sample(rng, phonemes, weights, n)
            surface = "".join(sampled)
            if surface not in surfaces_seen:
                break
            attempts += 1
            if attempts >= _REDRAW_LIMIT:
                # Deterministic seed bump: append the attempt count so we
                # eventually escape any local collision cluster without
                # introducing nondeterminism.
                rng = random.Random(seed + idx * 1009 + attempts)
                attempts = 0
        surfaces_seen.add(surface)
        control_entries.append(
            {
                "surface": surface,
                "phonemes": sampled,
                "region": region_tag,
                "citation": (
                    f"Synthetic phonotactic control entry generated by "
                    f"scripts/build_control_pools.py from the {substrate_pool_name} "
                    f"pool's marginal phoneme distribution and length distribution."
                ),
            }
        )
    return control_entries


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


def build_one(
    substrate_pool_name: str,
    pools_dir: Path,
) -> dict:
    """Build, validate, and write one control pool YAML.

    Returns a summary dict with substrate/control entry counts, length-
    distribution match, and inventory match.
    """
    sub_path = pools_dir / f"{substrate_pool_name}.yaml"
    substrate_pool = _load_substrate_pool(sub_path)

    control_pool_name = f"control_{substrate_pool_name}"
    region_tag = f"phonotactic_control_{substrate_pool_name}"
    control_entries = _build_control_entries(
        substrate_pool_name=substrate_pool_name,
        substrate_pool=substrate_pool,
        region_tag=region_tag,
    )

    seed_hex = f"{_seed_for(substrate_pool_name):016x}"
    control_doc = {
        "pool": control_pool_name,
        "source_citation": (
            f"Phonotactic control pool generated from {substrate_pool_name}.yaml "
            f"(mg-f419). Each control entry shares the substrate entry's length "
            f"and is sampled from the substrate pool's per-pool phoneme-frequency "
            f"distribution.  Deterministic seed: 0x{seed_hex} (sha256(\"control_pool:"
            f"{substrate_pool_name}\")[:16]). See pools/control_{substrate_pool_name}."
            f"README.md for the matching algorithm and per-pool histograms.\n"
        ),
        "license": (
            "Synthetic data; no source-text content. Released under the same terms "
            "as the lineara repo.\n"
        ),
        "fetched_at": "2026-05-04T00:00:00Z",
        "entries": control_entries,
    }

    # Schema-validate.
    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(control_doc)

    # Write deterministically (atomic-ish: only rewrite if content changed,
    # so re-runs don't churn mtimes).
    out_path = pools_dir / f"{control_pool_name}.yaml"
    yaml_text = _dump_yaml(control_doc)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != yaml_text:
        out_path.write_text(yaml_text, encoding="utf-8")

    try:
        rel_out = out_path.resolve().relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        rel_out = str(out_path)

    # Self-check: phonotactic match on length distribution.
    sub_lens = length_distribution(substrate_pool)
    ctrl_lens = length_distribution(control_doc)
    assert sub_lens == ctrl_lens, (
        f"length distribution mismatch for {substrate_pool_name}: "
        f"substrate={dict(sub_lens)} vs control={dict(ctrl_lens)}"
    )

    sub_hist = phoneme_histogram(substrate_pool)
    ctrl_hist = phoneme_histogram(control_doc)
    inventory_match = set(ctrl_hist) <= set(sub_hist)

    # Total phonemes count is always equal because length distribution is matched.
    total = sum(sub_hist.values())
    return {
        "substrate_pool": substrate_pool_name,
        "control_pool": control_pool_name,
        "n_entries": len(control_entries),
        "control_path": rel_out,
        "seed_hex": f"0x{seed_hex}",
        "length_distribution_match": True,
        "phoneme_inventory_subset_of_substrate": inventory_match,
        "substrate_phoneme_inventory_size": len(sub_hist),
        "control_phoneme_inventory_size": len(ctrl_hist),
        "total_phoneme_tokens": total,
    }


def write_readme(
    substrate_pool_name: str,
    pools_dir: Path,
) -> Path:
    """Write the per-pool README documenting the matching algorithm and the
    side-by-side phoneme histogram."""
    sub_path = pools_dir / f"{substrate_pool_name}.yaml"
    ctrl_path = pools_dir / f"control_{substrate_pool_name}.yaml"
    substrate_pool = _load_substrate_pool(sub_path)
    control_pool = _load_substrate_pool(ctrl_path)

    sub_hist = phoneme_histogram(substrate_pool)
    ctrl_hist = phoneme_histogram(control_pool)
    sub_lens = length_distribution(substrate_pool)
    ctrl_lens = length_distribution(control_pool)

    seed_hex = f"0x{_seed_for(substrate_pool_name):016x}"

    lines: list[str] = []
    lines.append(f"# control_{substrate_pool_name} — phonotactic control pool\n")
    lines.append(
        f"Generated by `scripts/build_control_pools.py` from "
        f"`pools/{substrate_pool_name}.yaml`. Created for **mg-f419** to test "
        f"whether the substrate signal observed at the per-surface level (mg-c2af) "
        f"clears a same-phonotactics randomized baseline.\n"
    )
    lines.append("## Matching algorithm\n")
    lines.append(
        "1. **Inventory.** Compute the phoneme-frequency histogram across all "
        f"entries in `pools/{substrate_pool_name}.yaml` (sum of phoneme counts "
        "across `phonemes[]` lists).\n"
        "2. **Length distribution.** For each substrate entry of length L, emit "
        "exactly one control entry of length L. The control pool is therefore "
        "byte-equal in entry count and length distribution to the substrate pool.\n"
        "3. **Sampling.** Each control phoneme is drawn with replacement from the "
        "substrate inventory weighted by inventory frequency (Python "
        "`random.choices`). The marginal distribution of phonemes in the control "
        "pool matches the substrate pool in expectation; the realized counts are "
        "approximate due to finite sample size (see histogram below).\n"
        "4. **Surface.** The control surface is the concatenation of the sampled "
        "phonemes — purely orthographic, no semantic content. Within-pool "
        "uniqueness is enforced by redrawing collisions up to "
        f"{_REDRAW_LIMIT} times; if uniqueness still fails the RNG seed is "
        "bumped deterministically (so the output remains reproducible).\n"
        "5. **Region tag.** Every control entry carries "
        f"`region: phonotactic_control_{substrate_pool_name}`. This is "
        "deliberately unmapped in `harness/metrics._GG1_REGION_COMPAT`, so "
        "geographic_genre_fit_v1 falls back to neutral 0.5 across the whole "
        "control pool — controls have no semantic content and should not be "
        "flattered by the geographic prior.\n"
        "6. **Semantic field.** Unset on every control entry (gg1 also falls "
        "back to 0.5).\n"
        "7. **Determinism.** Seed = "
        f"`{seed_hex}` (sha256(\"control_pool:{substrate_pool_name}\")[:16]). "
        "Re-running the builder produces a byte-identical YAML. Asserted by "
        "`harness/tests/test_control_pools.py`.\n"
    )

    lines.append("## Length distribution match\n")
    lines.append("| length | substrate | control |")
    lines.append("|---:|---:|---:|")
    for L in sorted(set(sub_lens) | set(ctrl_lens)):
        lines.append(f"| {L} | {sub_lens.get(L, 0)} | {ctrl_lens.get(L, 0)} |")
    lines.append("")

    lines.append("## Phoneme inventory and frequency\n")
    lines.append(
        "Substrate counts are exact; control counts are realized (drawn under "
        "the substrate's frequency distribution). The control inventory is a "
        "subset of the substrate inventory by construction.\n"
    )
    lines.append("| phoneme | substrate count | substrate % | control count | control % |")
    lines.append("|---|---:|---:|---:|---:|")
    sub_total = sum(sub_hist.values()) or 1
    ctrl_total = sum(ctrl_hist.values()) or 1
    for ph in sorted(set(sub_hist) | set(ctrl_hist)):
        s = sub_hist.get(ph, 0)
        c = ctrl_hist.get(ph, 0)
        lines.append(
            f"| `{ph}` | {s} | {100 * s / sub_total:.1f}% | {c} | {100 * c / ctrl_total:.1f}% |"
        )
    lines.append("")

    lines.append("## Pool counts\n")
    lines.append(f"- Substrate entries: **{len(substrate_pool['entries'])}**")
    lines.append(f"- Control entries:   **{len(control_pool['entries'])}**")
    lines.append("")

    lines.append("## What the control is NOT\n")
    lines.append(
        "- Not a *Linear-A surface* control. The substrate pool's surfaces are real "
        "lexemes from a real attested language; control surfaces are synthetic "
        "concatenations with no semantic content.\n"
        "- Not a *bigram* control. The control samples each phoneme position "
        "independently from the marginal — it does not preserve adjacent-phoneme "
        "structure (CV transitions, etc.). This is intentional: matching higher-"
        "order phonotactics would also encode a substrate signal we are trying "
        "to test for.\n"
        "- Not a *position* control. Phonemes are uniform-position-likelihood "
        "draws from the substrate inventory; positional dependencies in the "
        "substrate are not preserved.\n"
        "\n"
        "What the control DOES match: phoneme inventory and length distribution. "
        "The null hypothesis it lets us test is *“the substrate per-surface "
        "leaderboard is just an artifact of phoneme-inventory overlap with the "
        "syllabogram set”*.\n"
    )

    out_path = pools_dir / f"control_{substrate_pool_name}.README.md"
    text = "\n".join(lines)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != text:
        out_path.write_text(text, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--pool",
        choices=_SUBSTRATE_POOLS,
        default=None,
        help="Restrict to one substrate pool (default: build all).",
    )
    parser.add_argument(
        "--pools-dir",
        type=Path,
        default=_DEFAULT_POOLS_DIR,
        help="Directory containing pool YAMLs.",
    )
    args = parser.parse_args(argv)

    targets: Iterable[str] = (
        (args.pool,) if args.pool else _SUBSTRATE_POOLS
    )
    summaries: list[dict] = []
    for name in targets:
        summary = build_one(name, args.pools_dir)
        readme = write_readme(name, args.pools_dir)
        try:
            summary["readme_path"] = readme.resolve().relative_to(_REPO_ROOT).as_posix()
        except ValueError:
            summary["readme_path"] = str(readme)
        summaries.append(summary)
        print(
            f"built control pool: {summary['control_path']}  "
            f"(n={summary['n_entries']}, seed={summary['seed_hex']})",
            file=sys.stderr,
        )
    print(json.dumps(summaries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
