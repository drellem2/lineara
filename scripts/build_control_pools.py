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

Sampler choice (``--sampler {unigram,bigram}``)
-----------------------------------------------
``--sampler unigram`` (default, mg-f419 / v6 backward-compatible) draws
each phoneme independently from the substrate's marginal histogram.

``--sampler bigram`` (mg-9f18 / v18) draws each phoneme conditional on the
previous phoneme using the substrate pool's *bigram* counts:

  * The first phoneme is drawn from the substrate's unigram-marginal
    (smoothed by ``alpha = 0.1`` so phonemes that never appear at
    position 0 in the substrate still receive non-zero probability).
  * Each subsequent phoneme c is drawn with weight
    ``bigram_count(prev, c) + alpha``, so the realized control surfaces
    inherit the substrate pool's adjacent-phoneme structure (CV
    transitions, vowel hiatus rates, etc.) rather than just its
    marginal distribution.

The bigram sampler addresses the v10 toponym-pool failure (mg-d26d): the
unigram sampler produced control surfaces like ``eoao`` and ``aathei``
that the Basque LM scored extremely well by sheer phoneme-frequency
match, even though those strings violate Basque (and natural-language)
phonotactics. A bigram-preserving control aligns the phonotactic shape
of the control with the substrate, eliminating that drift.

Both samplers share the same length-distribution matching, deterministic
seed derivation, surface-uniqueness redraw policy, and output schema.

Usage:
    python3 scripts/build_control_pools.py
    python3 scripts/build_control_pools.py --pool aquitanian
    python3 scripts/build_control_pools.py --pool toponym --sampler bigram \\
        --suffix _bigram
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
    # mg-7ecb (harness v15): cross-language polluted Aquitanian pool —
    # 153 real Aquitanian + 153 Greek-shape conjecturals. Matched
    # control samples from the *combined* phoneme distribution (half
    # Aquitanian shape, half Greek shape) so the control mirrors what
    # the polluted pool actually contains.
    "greek_polluted_aquitanian",
    # mg-9f18 (harness v18): pollution-level sweep variants. The 50%
    # pool is `polluted_aquitanian` above; these three round out the
    # 4-row gradient table.
    "polluted_aquitanian_10pct",
    "polluted_aquitanian_25pct",
    "polluted_aquitanian_75pct",
)
_REDRAW_LIMIT = 50

# Default Laplace-smoothing alpha for the bigram sampler. Matches the
# default alpha used by ``harness.external_phoneme_model`` and the v15
# cross-language LM sampler (``scripts/build_polluted_pool._sample_word_
# from_external_lm``), so the smoothing knob is consistent across every
# bigram-conditional draw in the pipeline.
_DEFAULT_BIGRAM_ALPHA = 0.1

_SAMPLERS = ("unigram", "bigram")


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings (mirror of
    ``scripts/generate_candidates.py``)."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _seed_for(pool_name: str, sampler: str = "unigram") -> int:
    """Deterministic 64-bit seed derived from the substrate pool name.

    The unigram sampler keeps the legacy seed key
    ``"control_pool:<pool>"`` so v6 control pools rebuild byte-identical.
    The bigram sampler uses a sampler-suffixed key
    ``"control_pool:<pool>:<sampler>"`` so it draws from a disjoint
    random stream — same-pool unigram and bigram controls never collide.
    """
    if sampler == "unigram":
        key = f"control_pool:{pool_name}"
    else:
        key = f"control_pool:{pool_name}:{sampler}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
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


def phoneme_first_histogram(pool: dict) -> Counter:
    """Counter of pool-position-0 phoneme → count.

    Used by the bigram sampler to seed each conjectural surface's first
    phoneme from the substrate's *positional* unigram marginal (i.e.
    "what does the first phoneme of a substrate root look like?"),
    which is more representative of word-onset phonotactics than the
    overall marginal would be. Smoothed with the same alpha as the
    bigram step so phonemes that never appear at position 0 in the
    substrate still receive non-zero probability.
    """
    counter: Counter = Counter()
    for entry in pool["entries"]:
        if entry["phonemes"]:
            counter[entry["phonemes"][0]] += 1
    return counter


def phoneme_bigram_histogram(pool: dict) -> dict[str, Counter]:
    """Map prev_phoneme → Counter of next_phoneme counts.

    Built from every adjacent (p_i, p_{i+1}) pair across every entry's
    phonemes list. The bigram sampler uses this map (with Laplace
    smoothing alpha) to draw each conjectural phoneme conditional on
    the previous one.
    """
    out: dict[str, Counter] = {}
    for entry in pool["entries"]:
        phonemes = entry["phonemes"]
        for i in range(len(phonemes) - 1):
            prev = phonemes[i]
            nxt = phonemes[i + 1]
            out.setdefault(prev, Counter())[nxt] += 1
    return out


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


def _draw_bigram_word(
    *,
    rng: random.Random,
    inventory: list[str],
    first_weights: list[float],
    bigram_weights: dict[str, list[float]],
    n: int,
) -> list[str]:
    """Draw a length-``n`` phoneme sequence under the bigram sampler.

    ``inventory`` is the sorted list of every phoneme that appears
    anywhere in the substrate pool. ``first_weights`` aligns to that
    inventory and gives the smoothed positional-onset distribution.
    ``bigram_weights[prev]`` is a precomputed
    ``[count(prev, c) + alpha for c in inventory]`` weight vector for
    each ``prev`` actually observed mid-substrate (and the empty key
    ``""`` falls back to onset weights when ``prev`` is unseen, which
    happens for word-final-only phonemes).
    """
    if n <= 0:
        return []
    sampled = [rng.choices(inventory, weights=first_weights, k=1)[0]]
    fallback = first_weights
    for _ in range(n - 1):
        weights = bigram_weights.get(sampled[-1], fallback)
        sampled.append(rng.choices(inventory, weights=weights, k=1)[0])
    return sampled


def _build_control_entries(
    *,
    substrate_pool_name: str,
    substrate_pool: dict,
    region_tag: str,
    sampler: str = "unigram",
    alpha: float = _DEFAULT_BIGRAM_ALPHA,
) -> list[dict]:
    """Generate the control entries for one substrate pool.

    For each substrate entry we emit one control entry of the same length;
    phonemes are sampled from the substrate's marginal phoneme distribution
    (``sampler='unigram'``, default) or from the substrate's bigram
    distribution conditional on the previous phoneme (``sampler='bigram'``,
    mg-9f18 / v18). Surfaces are forced unique within the control pool by
    retrying up to ``_REDRAW_LIMIT`` times per entry; if a unique draw
    cannot be produced we bump the seed and continue (deterministic chain
    — same pool ⇒ same final entries).
    """
    if sampler not in _SAMPLERS:
        raise ValueError(
            f"unknown sampler {sampler!r}; supported: {_SAMPLERS}"
        )

    histogram = phoneme_histogram(substrate_pool)
    inventory = sorted(histogram.keys())
    seed = _seed_for(substrate_pool_name, sampler=sampler)
    rng = random.Random(seed)

    if sampler == "unigram":
        unigram_weights = [float(histogram[p]) for p in inventory]

        def _draw(n: int) -> list[str]:
            return _weighted_sample(rng, inventory, unigram_weights, n)

        citation_blurb = (
            f"Synthetic phonotactic control entry generated by "
            f"scripts/build_control_pools.py from the {substrate_pool_name} "
            f"pool's marginal phoneme distribution and length distribution."
        )
    else:
        # Bigram sampler (mg-9f18 / v18). Precompute weight vectors so
        # the per-draw work is just a single ``random.choices`` call,
        # not a Counter lookup × inventory_size on every position.
        first_hist = phoneme_first_histogram(substrate_pool)
        first_weights = [float(first_hist.get(p, 0)) + alpha for p in inventory]
        bigram_hist = phoneme_bigram_histogram(substrate_pool)
        bigram_weights: dict[str, list[float]] = {}
        for prev, counter in bigram_hist.items():
            bigram_weights[prev] = [float(counter.get(p, 0)) + alpha for p in inventory]

        def _draw(n: int) -> list[str]:
            return _draw_bigram_word(
                rng=rng,
                inventory=inventory,
                first_weights=first_weights,
                bigram_weights=bigram_weights,
                n=n,
            )

        citation_blurb = (
            f"Synthetic phonotactic control entry generated by "
            f"scripts/build_control_pools.py (mg-9f18, harness v18) from "
            f"the {substrate_pool_name} pool's bigram phoneme distribution "
            f"(alpha={alpha}) and length distribution. Each phoneme is "
            f"drawn conditional on the previous phoneme so the realized "
            f"control surfaces preserve the substrate's adjacent-phoneme "
            f"structure, not just its marginal histogram."
        )

    control_entries: list[dict] = []
    surfaces_seen: set[str] = set()

    for idx, sub_entry in enumerate(substrate_pool["entries"]):
        n = len(sub_entry["phonemes"])
        attempts = 0
        bumps = 0
        while True:
            sampled = _draw(n)
            surface = "".join(sampled)
            if surface not in surfaces_seen:
                break
            attempts += 1
            if attempts >= _REDRAW_LIMIT:
                # Deterministic seed bump: append the attempt count so we
                # eventually escape any local collision cluster without
                # introducing nondeterminism.
                bumps += 1
                rng = random.Random(seed + idx * 1009 + bumps)
                attempts = 0
                # ``_draw`` looks up ``rng`` from this enclosing scope at
                # call time, so the rebind takes effect on the next loop
                # iteration without redefining the closure.
        surfaces_seen.add(surface)
        control_entries.append(
            {
                "surface": surface,
                "phonemes": sampled,
                "region": region_tag,
                "citation": citation_blurb,
            }
        )
    return control_entries


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


def build_one(
    substrate_pool_name: str,
    pools_dir: Path,
    *,
    sampler: str = "unigram",
    suffix: str = "",
    alpha: float = _DEFAULT_BIGRAM_ALPHA,
) -> dict:
    """Build, validate, and write one control pool YAML.

    ``sampler='unigram'`` (default, v6 backward-compatible) preserves the
    legacy output filename ``pools/control_<pool>.yaml`` and the legacy
    seed key. ``sampler='bigram'`` (mg-9f18 / v18) honors a non-empty
    ``suffix`` (e.g. ``'_bigram'``) so the new pool can be committed
    side-by-side with the v6 control without overwriting it.

    Returns a summary dict with substrate/control entry counts, length-
    distribution match, and inventory match.
    """
    if sampler not in _SAMPLERS:
        raise ValueError(
            f"unknown sampler {sampler!r}; supported: {_SAMPLERS}"
        )
    sub_path = pools_dir / f"{substrate_pool_name}.yaml"
    substrate_pool = _load_substrate_pool(sub_path)

    control_pool_name = f"control_{substrate_pool_name}{suffix}"
    region_tag = f"phonotactic_control_{substrate_pool_name}{suffix}"
    control_entries = _build_control_entries(
        substrate_pool_name=substrate_pool_name,
        substrate_pool=substrate_pool,
        region_tag=region_tag,
        sampler=sampler,
        alpha=alpha,
    )

    seed_hex = f"{_seed_for(substrate_pool_name, sampler=sampler):016x}"
    if sampler == "unigram":
        # Preserve the legacy v6 source_citation byte-for-byte so the
        # committed pools/control_*.yaml YAMLs from mg-f419 round-trip
        # unchanged on a default rebuild (no downstream churn from this
        # cleanup).
        source_citation = (
            f"Phonotactic control pool generated from {substrate_pool_name}.yaml "
            f"(mg-f419). Each control entry shares the substrate entry's length "
            f"and is sampled from the substrate pool's per-pool phoneme-frequency "
            f"distribution.  Deterministic seed: 0x{seed_hex} (sha256(\"control_pool:"
            f"{substrate_pool_name}\")[:16]). See pools/control_{substrate_pool_name}."
            f"README.md for the matching algorithm and per-pool histograms.\n"
        )
    else:
        source_citation = (
            f"Phonotactic control pool generated from {substrate_pool_name}.yaml "
            f"(mg-9f18 / harness v18, bigram-preserving sampler). Each control "
            f"entry shares the substrate entry's length and is sampled from the "
            f"substrate pool's bigram phoneme distribution with Laplace "
            f"alpha={alpha}. Each phoneme is drawn conditional on the previous "
            f"phoneme so the realized control surfaces inherit the substrate's "
            f"adjacent-phoneme structure (CV transitions, vowel hiatus rates, "
            f"etc.), not just its marginal histogram. Deterministic seed: "
            f"0x{seed_hex} (sha256(\"control_pool:{substrate_pool_name}:"
            f"{sampler}\")[:16]). See pools/{control_pool_name}.README.md for "
            f"the matching algorithm and per-pool histograms.\n"
        )
    control_doc = {
        "pool": control_pool_name,
        "source_citation": source_citation,
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
        "sampler": sampler,
        "alpha": alpha if sampler == "bigram" else None,
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
    *,
    sampler: str = "unigram",
    suffix: str = "",
    alpha: float = _DEFAULT_BIGRAM_ALPHA,
) -> Path:
    """Write the per-pool README documenting the matching algorithm and the
    side-by-side phoneme histogram."""
    sub_path = pools_dir / f"{substrate_pool_name}.yaml"
    ctrl_path = pools_dir / f"control_{substrate_pool_name}{suffix}.yaml"
    substrate_pool = _load_substrate_pool(sub_path)
    control_pool = _load_substrate_pool(ctrl_path)

    sub_hist = phoneme_histogram(substrate_pool)
    ctrl_hist = phoneme_histogram(control_pool)
    sub_lens = length_distribution(substrate_pool)
    ctrl_lens = length_distribution(control_pool)

    seed_hex = f"0x{_seed_for(substrate_pool_name, sampler=sampler):016x}"
    region_tag = f"phonotactic_control_{substrate_pool_name}{suffix}"
    is_bigram = sampler == "bigram"
    pool_name = f"control_{substrate_pool_name}{suffix}"

    lines: list[str] = []
    lines.append(f"# {pool_name} — phonotactic control pool\n")
    if is_bigram:
        lines.append(
            f"Generated by `scripts/build_control_pools.py --sampler bigram` "
            f"from `pools/{substrate_pool_name}.yaml`. Created for **mg-9f18 / "
            f"harness v18** to address the v10 toponym-pool gate failure: the "
            f"v6 unigram sampler produced control surfaces like `eoao` and "
            f"`aathei` that the Basque LM scored extremely well by raw "
            f"phoneme-frequency match. The bigram-preserving sampler draws "
            f"each phoneme conditional on the previous phoneme, so the "
            f"realized control surfaces inherit the substrate's adjacent-"
            f"phoneme structure rather than just its marginal histogram.\n"
        )
    else:
        lines.append(
            f"Generated by `scripts/build_control_pools.py` from "
            f"`pools/{substrate_pool_name}.yaml`. Created for **mg-f419** to test "
            f"whether the substrate signal observed at the per-surface level (mg-c2af) "
            f"clears a same-phonotactics randomized baseline.\n"
        )

    lines.append("## Matching algorithm\n")
    if is_bigram:
        lines.append(
            "1. **Inventory.** Compute the phoneme-frequency histogram and the "
            f"bigram-frequency map (one Counter per `prev_phoneme`) across all "
            f"entries in `pools/{substrate_pool_name}.yaml`.\n"
            "2. **Length distribution.** For each substrate entry of length L, "
            "emit exactly one control entry of length L. The control pool is "
            "therefore byte-equal in entry count and length distribution to "
            "the substrate pool.\n"
            f"3. **First-phoneme sampling.** The first phoneme of each control "
            f"surface is drawn from the substrate's *positional-onset* unigram "
            f"distribution (i.e. counts of phonemes at position 0 in the "
            f"substrate's `phonemes[]` lists), Laplace-smoothed by "
            f"alpha={alpha}: `weight(p) = onset_count(p) + alpha`. Phonemes that "
            "never appear at position 0 in the substrate still receive non-zero "
            "probability, so the sampler can produce any inventory phoneme as "
            "an onset.\n"
            f"4. **Subsequent-phoneme sampling.** Each subsequent phoneme c is "
            f"drawn conditional on the previous phoneme `prev` with weight "
            f"`bigram_count(prev, c) + alpha`. For phonemes that appear only "
            f"word-finally in the substrate (so `prev` has no observed "
            f"successors), the sampler falls back to the onset distribution "
            "from step 3 — this is rare in practice but keeps the draw well-"
            "defined.\n"
            "5. **Surface.** The control surface is the concatenation of the "
            "sampled phonemes — purely orthographic, no semantic content. "
            "Within-pool uniqueness is enforced by redrawing collisions up to "
            f"{_REDRAW_LIMIT} times; if uniqueness still fails the RNG seed is "
            "bumped deterministically (so the output remains reproducible).\n"
            "6. **Region tag.** Every control entry carries "
            f"`region: {region_tag}`. This is deliberately unmapped in "
            "`harness/metrics._GG1_REGION_COMPAT`, so geographic_genre_fit_v1 "
            "falls back to neutral 0.5 across the whole control pool — "
            "controls have no semantic content and should not be flattered by "
            "the geographic prior.\n"
            "7. **Semantic field.** Unset on every control entry (gg1 also "
            "falls back to 0.5).\n"
            "8. **Determinism.** Seed = "
            f"`{seed_hex}` "
            f"(sha256(\"control_pool:{substrate_pool_name}:{sampler}\")[:16]). "
            "The bigram-sampler key is suffixed with `:bigram` so this pool "
            "draws from a disjoint random stream relative to the v6 unigram "
            f"control. Re-running the builder produces a byte-identical YAML. "
            "Asserted by `harness/tests/test_control_pools.py`.\n"
        )
    else:
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
            f"`region: {region_tag}`. This is "
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
    if is_bigram:
        lines.append(
            "Substrate counts are exact; control counts are realized (drawn "
            "under the substrate's bigram distribution). The control inventory "
            "is a subset of the substrate inventory by construction. The "
            "marginal histogram below masks the actual signal — what the "
            "bigram sampler matches is the *transition* structure, not just "
            "the marginal — but the marginal is included for direct comparison "
            "with the v6 unigram control pool.\n"
        )
    else:
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
    if is_bigram:
        lines.append(
            "- Not a *Linear-A surface* control. The substrate pool's surfaces "
            "are real lexemes from a real attested language; control surfaces "
            "are synthetic concatenations with no semantic content.\n"
            "- Not a *trigram* (or higher-order) control. Adjacent-phoneme "
            "structure is matched, but three-phoneme spans and longer-range "
            "dependencies are not preserved. v18's design choice was to "
            "address the most prominent unigram-sampler artifact (control "
            "surfaces with extreme phonotactic violations) without absorbing "
            "the substrate signal entirely; matching trigrams + longer would "
            "encode the substrate's word-shape statistics so completely that "
            "any LM trained on related material would fail to discriminate.\n"
            "- Not a *position* control beyond first-phoneme onset weighting. "
            "Mid-word positional dependencies (e.g. `r` is more likely than "
            "`d` to appear in the final position) are partially captured by "
            "the bigram transitions but not enforced as a separate term.\n"
            "\n"
            "What the control DOES match: phoneme inventory, length "
            "distribution, and adjacent-phoneme transitions. The null "
            "hypothesis it lets us test is *\"the substrate per-surface "
            "leaderboard is just an artifact of phoneme-inventory + bigram-"
            "phonotactics overlap with the syllabogram set\"* — strictly "
            "stronger than the unigram null v6 tested.\n"
        )
    else:
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

    out_path = pools_dir / f"{pool_name}.README.md"
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
    parser.add_argument(
        "--sampler",
        choices=_SAMPLERS,
        default="unigram",
        help=(
            "Sampler used to draw conjectural phonemes. 'unigram' "
            "(default, mg-f419 / v6 backward-compatible) draws each "
            "phoneme independently from the substrate's marginal. "
            "'bigram' (mg-9f18 / v18) draws each phoneme conditional "
            "on the previous phoneme using the substrate's bigram "
            "distribution; addresses the v10 toponym gate failure by "
            "preserving CV-transition structure in the control."
        ),
    )
    parser.add_argument(
        "--suffix",
        default="",
        help=(
            "Optional suffix appended to the output pool name "
            "(e.g. '_bigram' produces pools/control_<pool>_bigram.yaml). "
            "Use this when building a non-default-sampler control "
            "side-by-side with the legacy unigram control. The empty "
            "default preserves the v6 filename layout."
        ),
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=_DEFAULT_BIGRAM_ALPHA,
        help=(
            "Laplace smoothing alpha for the bigram sampler "
            f"(default: {_DEFAULT_BIGRAM_ALPHA}). Ignored for "
            "--sampler unigram. Matches the default alpha used by the "
            "external phoneme LM and the v15 cross-language sampler."
        ),
    )
    args = parser.parse_args(argv)

    targets: Iterable[str] = (
        (args.pool,) if args.pool else _SUBSTRATE_POOLS
    )
    summaries: list[dict] = []
    for name in targets:
        summary = build_one(
            name,
            args.pools_dir,
            sampler=args.sampler,
            suffix=args.suffix,
            alpha=args.alpha,
        )
        readme = write_readme(
            name,
            args.pools_dir,
            sampler=args.sampler,
            suffix=args.suffix,
            alpha=args.alpha,
        )
        try:
            summary["readme_path"] = readme.resolve().relative_to(_REPO_ROOT).as_posix()
        except ValueError:
            summary["readme_path"] = str(readme)
        summaries.append(summary)
        print(
            f"built control pool: {summary['control_path']}  "
            f"(n={summary['n_entries']}, sampler={summary['sampler']}, "
            f"seed={summary['seed_hex']})",
            file=sys.stderr,
        )
    print(json.dumps(summaries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
