#!/usr/bin/env python3
"""Build a *polluted* substrate pool by mixing real entries with deliberately-
conjectural ones (mg-6b73, harness v14 — held-out pool-curation test;
extended in mg-7ecb, harness v15 — cross-language pollution test).

The polluted pool is a **test artifact**, not a research claim. Its purpose
is to test the framework's selectivity to substrate-distribution-shape:

  * **Same-distribution pollution (v14 default).** Conjecturals are drawn
    from the substrate pool's *own* marginal phoneme histogram. v14 found
    that the v10 right-tail bayesian PASS on Aquitanian survives 50%
    same-distribution pollution; the framework's PASS does not depend on
    every entry being a real substrate root.
  * **Cross-language pollution (v15, ``--source-lm`` flag).** Conjecturals
    are drawn from a *different* language's character-bigram distribution
    (e.g. Mycenaean Greek), but their lengths still match the substrate
    pool's length distribution. v15 asks: does the framework PASS for any
    phonotactic match, or only same-distribution? A PASS on the cross-
    language polluted pool means the framework's PASS signal is essentially
    trivial — any phonotactic-shape overlap with the LM produces a PASS.
    A FAIL means the gate respects substrate-distribution shape.

For one substrate pool (default ``aquitanian``):

  * **Real half.** Every entry from the substrate pool is carried over with
    its original surface, phonemes, gloss, semantic_field, region, etc.,
    and tagged ``provenance: real``.
  * **Conjectural half.** Same number of entries (153 for Aquitanian),
    drawn from either:
    - the substrate pool's marginal phoneme-frequency histogram (default,
      v14 behavior — same algorithm as ``scripts/build_control_pools.py``),
      tagged ``provenance: conjectural``; OR
    - an external char-bigram language model loaded via ``--source-lm
      <path>`` (v15), tagged ``provenance: conjectural_<prefix>`` where
      ``<prefix>`` comes from the ``--prefix`` flag (e.g. ``greek`` →
      ``conjectural_greek``). Each character is sampled from the model
      conditional on the previous character, with the first character
      sampled from the model's unigram marginal restricted to the alphabet
      (the ``<W>`` boundary token and the space character are filtered out
      of the next-character distribution at every step, since substrate
      surfaces are content-only words). Lengths still match the substrate
      pool's length distribution so length is not a confound.
    Both pollution modes use a **distinct seed** keyed on the *full*
    polluted-pool name (``sha256("<pool>:conjectural")[:16]``) so the
    conjectural surfaces do not collide with the matched control pool's
    surfaces. Each conjectural entry is tagged ``region: aquitania`` (so
    it is indistinguishable from real entries to the candidate generator's
    source_pool routing) and its ``semantic_field`` is left unset.
  * **Surface uniqueness.** Conjectural surfaces are forced unique against
    real surfaces *and* prior conjectural surfaces. Collisions trigger a
    deterministic redraw, then a deterministic seed bump if redraws
    exhaust ``_REDRAW_LIMIT``. Re-running produces a byte-identical YAML.
  * **Phoneme-class filter.** The candidate generator skips entries whose
    phonemes span fewer than two distinct phoneme classes (V/S/C). The
    builder applies the same filter to conjectural draws so every emitted
    conjectural entry actually generates candidates downstream.

Output:

  * ``pools/<prefix>_polluted_<base>.yaml`` (or ``polluted_<base>.yaml``
    when ``--prefix`` is omitted) — 306 entries (153 real + 153
    conjectural), schema-valid, deterministic.
  * ``pools/<prefix>_polluted_<base>.README.md`` — construction
    documentation that prominently warns this pool is a test artifact,
    not a substrate claim.

Idempotent. Re-running with the same substrate pool + LM ⇒ byte-identical
outputs.

Usage:
    # v14 default — same-distribution pollution.
    python3 scripts/build_polluted_pool.py
    python3 scripts/build_polluted_pool.py --pool aquitanian

    # v15 cross-language pollution (Greek-shape conjecturals).
    python3 scripts/build_polluted_pool.py --pool aquitanian \\
        --source-lm harness/external_phoneme_models/mycenaean_greek.json \\
        --prefix greek
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


def _ratio_suffix(ratio_pct: int | None) -> str:
    """Suffix for a polluted pool keyed on its conjectural-entry share.

    ``ratio_pct=None`` (v14 default) ⇒ no suffix; the polluted pool is
    the canonical 50% same-distribution pool. Any explicit integer
    percentage produces ``_<n>pct`` (e.g. 10 → ``_10pct``).
    """
    if ratio_pct is None:
        return ""
    return f"_{ratio_pct}pct"


def _polluted_pool_name(
    base_pool: str,
    prefix: str | None,
    ratio_pct: int | None = None,
) -> str:
    """Compose the polluted-pool name from a base name, optional prefix,
    and optional pollution-ratio percentage.

    ``prefix=None, ratio_pct=None`` (v14 default) ⇒ ``polluted_<base>``
    (e.g. ``polluted_aquitanian``, the canonical 50% same-distribution
    pool).
    ``prefix='greek', ratio_pct=None`` (v15) ⇒ ``greek_polluted_<base>``.
    ``prefix=None, ratio_pct=10`` (v18) ⇒ ``polluted_<base>_10pct``.
    """
    suffix = _ratio_suffix(ratio_pct)
    if prefix:
        return f"{prefix}_polluted_{base_pool}{suffix}"
    return f"polluted_{base_pool}{suffix}"


def _provenance_tag(prefix: str | None) -> str:
    """Provenance tag for conjectural entries.

    ``prefix=None`` ⇒ ``conjectural`` (v14 same-distribution pollution).
    ``prefix='greek'`` ⇒ ``conjectural_greek`` (v15 cross-language
    pollution, schema-validated against the ``conjectural_<lang>``
    pattern in pools/schemas/pool.v1.schema.json).
    """
    if prefix:
        return f"conjectural_{prefix}"
    return "conjectural"


def _seed_for(polluted_pool_name: str) -> int:
    """Deterministic 64-bit seed for the conjectural draws.

    Keyed on the *full* polluted-pool name so different pollution sources
    (same-distribution vs cross-language) get disjoint random streams.
    Distinct from the matched-control seed
    (``sha256("control_pool:<pool>")[:16]``) so conjectural surfaces and
    matched-control surfaces also draw from disjoint random streams.
    """
    digest = hashlib.sha256(
        f"{polluted_pool_name}:conjectural".encode("utf-8")
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


def _load_external_lm(path: Path):
    """Lazy import of harness.external_phoneme_model so the builder runs
    without harness on PYTHONPATH for the v14 default code path."""
    import sys as _sys

    _sys.path.insert(0, str(_REPO_ROOT))
    from harness.external_phoneme_model import (  # type: ignore
        ALPHABET,
        VOCAB_INDEX,
        ExternalPhonemeModel,
    )

    model = ExternalPhonemeModel.load_json(path)
    return model, ALPHABET, VOCAB_INDEX


def _sample_word_from_external_lm(
    *,
    model,
    alphabet: tuple,
    vocab_index: dict,
    length: int,
    rng: random.Random,
) -> list[str]:
    """Sample a length-``length`` content-only word from a char-bigram LM.

    Sampling procedure (mg-7ecb):
      * The first character is drawn from the model's *unigram marginal*
        restricted to the alphabet (``a..z``); the ``<W>`` boundary token
        and the space character are filtered out so the word starts with
        a content character. Weights = ``unigram_count + alpha`` so
        alphabet characters never observed under the unigram still get
        non-zero (smoothed) probability.
      * Each subsequent character is drawn conditional on the previous
        character via the bigram counts ``count(prev, c) + alpha``,
        again restricted to ``a..z`` (the ``<W>``/space tokens are
        excluded so we never produce an early word-end). This is the
        "regenerate to match length" interpretation of the brief —
        rather than sampling whole words and rejecting those that
        don't match the target length, we constrain the next-token
        distribution to alphabet characters at every step. The
        *relative* frequencies of alphabet bigrams are preserved.
      * Each sampled character becomes a single-character phoneme
        (matching how ``external_phoneme_perplexity_v0`` decomposes
        phoneme streams to chars at scoring time, see
        ``harness.external_phoneme_model.char_decompose_phonemes``).
    """
    candidate_chars = list(alphabet)
    candidate_indices = [vocab_index[c] for c in candidate_chars]

    unigram_weights = [
        float(model.unigram_counts[j]) + float(model.alpha)
        for j in candidate_indices
    ]
    if sum(unigram_weights) <= 0:
        unigram_weights = [1.0] * len(candidate_chars)
    first = rng.choices(candidate_chars, weights=unigram_weights, k=1)[0]
    chars = [first]
    prev_idx = vocab_index[first]

    for _ in range(length - 1):
        weights = [
            float(model.bigram_counts[prev_idx][j]) + float(model.alpha)
            for j in candidate_indices
        ]
        if sum(weights) <= 0:
            weights = [1.0] * len(candidate_chars)
        c = rng.choices(candidate_chars, weights=weights, k=1)[0]
        chars.append(c)
        prev_idx = vocab_index[c]
    return chars


def _conjectural_lengths(real_pool: dict, n_conjectural: int) -> list[int]:
    """Length sequence for ``n_conjectural`` conjecturals, cycling through
    the real pool's per-entry lengths so the realized length sequence
    preserves the real pool's length distribution.

    For ``n_conjectural == len(real_pool['entries'])`` this is exactly the
    v14 behavior: i-th conjectural matches i-th real. For other values
    (the v18 pollution-level sweep at 10%/25%/75%), we cycle:
    ``conjectural[i].length = real[i % len(real)].length``. So:

      * 10% (17 conjecturals on a 153-entry pool): the first 17 reals'
        lengths.
      * 25% (51 conjecturals): the first 51 reals' lengths.
      * 50% (153 conjecturals, v14 default): exactly the real pool's
        lengths.
      * 75% (459 = 3 × 153 conjecturals): the real pool's lengths
        repeated three times — exact length-distribution match.

    Lengths within the substrate pool are pre-sorted by entry index, so
    cycling preserves a deterministic length sequence across re-runs.
    """
    real_lengths = [len(e["phonemes"]) for e in real_pool["entries"]]
    if not real_lengths:
        return []
    return [real_lengths[i % len(real_lengths)] for i in range(n_conjectural)]


def build_conjectural_entries(
    *,
    base_pool_name: str,
    base_pool: dict,
    region_tag: str,
    polluted_pool_name: str,
    provenance_tag: str,
    citation_blurb: str,
    source_lm_path: Path | None = None,
    n_conjectural: int | None = None,
) -> list[dict]:
    """Generate ``n_conjectural`` conjectural entries (default: one per
    real entry, v14 / v15 behavior).

    Each conjectural entry's length matches the corresponding real entry's
    length under cyclic indexing (see :func:`_conjectural_lengths`); the
    polluted pool's realized length distribution is therefore exactly
    ``ceil(n_conjectural / len(real)) ×`` the real pool's distribution at
    the *first ``n_conjectural`` entries*, which is the real pool's
    distribution itself when ``n_conjectural`` is a multiple of
    ``len(real)``.

    Phonemes are sampled from either:

      * the real pool's marginal phoneme-frequency histogram
        (``source_lm_path=None``, v14 default); OR
      * an external char-bigram LM at ``source_lm_path`` (v15 cross-
        language pollution; see ``_sample_word_from_external_lm``).

    Surfaces are forced unique against real surfaces and prior
    conjecturals; entries that fail the two-class phoneme filter are
    also redrawn so every emitted entry will produce candidates
    downstream. The seed is keyed on the *full* polluted-pool name so
    same-distribution and cross-language pollutions of the same base
    pool draw from disjoint streams.
    """
    real_surfaces = {e["surface"] for e in base_pool["entries"]}
    seed = _seed_for(polluted_pool_name)
    rng = random.Random(seed)

    if source_lm_path is None:
        histogram = _phoneme_histogram(base_pool)
        phonemes = sorted(histogram.keys())
        weights = [float(histogram[p]) for p in phonemes]

        def _draw(n: int) -> list[str]:
            return _weighted_sample(rng, phonemes, weights, n)
    else:
        model, alphabet, vocab_index = _load_external_lm(source_lm_path)

        def _draw(n: int) -> list[str]:
            return _sample_word_from_external_lm(
                model=model,
                alphabet=alphabet,
                vocab_index=vocab_index,
                length=n,
                rng=rng,
            )

    if n_conjectural is None:
        n_conjectural = len(base_pool["entries"])
    lengths = _conjectural_lengths(base_pool, n_conjectural)

    out: list[dict] = []
    seen_conjectural: set[str] = set()

    for idx, n in enumerate(lengths):
        attempts = 0
        bumps = 0
        while True:
            sampled = _draw(n)
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
                # Both ``_draw`` closures look up ``rng`` from the
                # enclosing scope at call time, so the rebind above is
                # picked up on the next iteration without redefining
                # the closure.
        seen_conjectural.add(surface)
        out.append(
            {
                "surface": surface,
                "phonemes": sampled,
                "region": region_tag,
                "provenance": provenance_tag,
                "citation": citation_blurb,
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


def _n_conjectural_for_ratio(n_real: int, ratio_pct: int) -> int:
    """Number of conjectural entries needed for a given ratio (percent of
    polluted pool that is conjectural).

    ratio_pct = 100 * n_conjectural / (n_real + n_conjectural), so
    n_conjectural = round(n_real * ratio_pct / (100 - ratio_pct)).
    """
    if ratio_pct < 0 or ratio_pct >= 100:
        raise ValueError(
            f"ratio_pct must be in [0, 100); got {ratio_pct!r}"
        )
    return int(round(n_real * ratio_pct / (100 - ratio_pct)))


def build_polluted_pool(
    base_pool_name: str,
    pools_dir: Path,
    *,
    source_lm_path: Path | None = None,
    prefix: str | None = None,
    ratio_pct: int | None = None,
) -> dict:
    """Build, validate, and write the polluted pool YAML.

    ``source_lm_path=None`` (v14 default) uses the substrate pool's own
    marginal phoneme histogram for conjectural draws and tags them
    ``provenance: conjectural``. ``source_lm_path=<path>`` (v15) draws
    chars from an external LM and tags them ``provenance: conjectural_
    <prefix>`` (with ``prefix`` derived from the model's ``name`` field
    when not explicitly given). The full polluted-pool name is
    ``<prefix>_polluted_<base>`` when ``prefix`` is provided, else
    ``polluted_<base>``.

    ``ratio_pct=None`` (v14 default) keeps the 50% same-distribution
    pool. ``ratio_pct=N`` (v18 pollution-level sweep) builds an N%
    conjectural / (100−N)% real pool with the corresponding name
    suffix ``_<N>pct``; the conjectural count is computed by
    :func:`_n_conjectural_for_ratio`.

    Returns a summary dict.
    """
    base_path = pools_dir / f"{base_pool_name}.yaml"
    base_pool = _load_pool(base_path)

    if source_lm_path is not None and prefix is None:
        # Derive a sensible default prefix from the LM filename stem.
        # The user can always override with --prefix.
        prefix = source_lm_path.stem.split("_")[-1]

    polluted_pool_name = _polluted_pool_name(
        base_pool_name, prefix, ratio_pct
    )
    provenance_tag = _provenance_tag(prefix)

    real_entries = build_real_entries(base_pool)
    if ratio_pct is None:
        n_conjectural = len(base_pool["entries"])
    else:
        n_conjectural = _n_conjectural_for_ratio(
            len(base_pool["entries"]), ratio_pct
        )

    if source_lm_path is None:
        citation_blurb = (
            f"Synthetic conjectural entry generated by "
            f"scripts/build_polluted_pool.py from the "
            f"{base_pool_name} pool's marginal phoneme distribution "
            f"and length distribution. Test artifact for the held-"
            f"out pool-curation test (mg-6b73); not a substrate "
            f"claim."
        )
    else:
        try:
            lm_rel = source_lm_path.resolve().relative_to(_REPO_ROOT).as_posix()
        except ValueError:
            lm_rel = str(source_lm_path)
        citation_blurb = (
            f"Synthetic conjectural entry generated by "
            f"scripts/build_polluted_pool.py from the char-bigram "
            f"distribution of the external phoneme LM at {lm_rel} "
            f"and the {base_pool_name} pool's length distribution. "
            f"Test artifact for the v15 cross-language pollution "
            f"test (mg-7ecb); not a substrate claim."
        )

    conjectural_entries = build_conjectural_entries(
        base_pool_name=base_pool_name,
        base_pool=base_pool,
        region_tag="aquitania" if base_pool_name == "aquitanian" else base_pool_name,
        polluted_pool_name=polluted_pool_name,
        provenance_tag=provenance_tag,
        citation_blurb=citation_blurb,
        source_lm_path=source_lm_path,
        n_conjectural=n_conjectural,
    )
    entries = real_entries + conjectural_entries

    seed_hex = f"{_seed_for(polluted_pool_name):016x}"
    realized_ratio = (
        100 * len(conjectural_entries) / max(len(entries), 1)
    )
    if source_lm_path is None:
        if ratio_pct is None:
            # Preserve the v14 source_citation byte-for-byte so re-runs
            # of the canonical 50% same-distribution pool stay clean.
            source_citation = (
                f"DELIBERATELY POLLUTED test pool generated from "
                f"{base_pool_name}.yaml (mg-6b73). Half real, half "
                f"conjectural — a test artifact for the held-out pool-"
                f"curation test, NOT a substrate claim. Conjectural "
                f"surfaces are drawn from the {base_pool_name} pool's "
                f"marginal phoneme-frequency histogram and length "
                f"distribution under deterministic seed 0x{seed_hex} "
                f"(sha256(\"{polluted_pool_name}:conjectural\")"
                f"[:16]). See pools/{polluted_pool_name}.README.md for "
                f"the full construction algorithm and a prominent warning "
                f"that this pool exists only to test the framework's "
                f"curation-sensitivity.\n"
            )
        else:
            source_citation = (
                f"DELIBERATELY POLLUTED test pool generated from "
                f"{base_pool_name}.yaml (mg-9f18 / harness v18 "
                f"pollution-level sweep). {len(real_entries)} real + "
                f"{len(conjectural_entries)} conjectural "
                f"({realized_ratio:.0f}% conjectural; target "
                f"{ratio_pct}%) — a test artifact for the v18 "
                f"curation-sensitivity gradient characterization, NOT "
                f"a substrate claim. Conjectural surfaces are drawn "
                f"from the {base_pool_name} pool's marginal phoneme-"
                f"frequency histogram and length distribution under "
                f"deterministic seed 0x{seed_hex} "
                f"(sha256(\"{polluted_pool_name}:conjectural\")"
                f"[:16]). See pools/{polluted_pool_name}.README.md for "
                f"the full construction algorithm and a prominent warning "
                f"that this pool exists only to test the framework's "
                f"curation-sensitivity.\n"
            )
        license_blurb = (
            "Mixed: real entries inherit the underlying "
            f"{base_pool_name} pool's license (cited fair-use of "
            "Trask 1997 and Gorrochategui 1984). Conjectural entries "
            "are synthetic data with no source-text content, "
            "released under the same terms as the lineara repo.\n"
        )
    else:
        source_citation = (
            f"DELIBERATELY POLLUTED test pool generated from "
            f"{base_pool_name}.yaml (mg-7ecb, harness v15 cross-"
            f"language pollution test). Half real {base_pool_name} "
            f"entries, half synthetic conjecturals drawn from the "
            f"char-bigram distribution of the external phoneme LM at "
            f"{lm_rel}. The {base_pool_name} length distribution is "
            f"preserved so length is not a confound; the phoneme "
            f"distribution is the *source LM's*, NOT "
            f"{base_pool_name}'s. Test artifact, NOT a substrate "
            f"claim. Conjecturals tagged provenance: "
            f"{provenance_tag} so the rollup can compute the "
            f"per-provenance breakdown of the right-tail leaderboard. "
            f"Deterministic seed 0x{seed_hex} (sha256(\""
            f"{polluted_pool_name}:conjectural\")[:16]). See "
            f"pools/{polluted_pool_name}.README.md for the full "
            f"sampling procedure and a prominent warning that this "
            f"pool exists only to test the framework's distribution-"
            f"shape selectivity.\n"
        )
        license_blurb = (
            f"Mixed: real entries inherit the underlying "
            f"{base_pool_name} pool's license (cited fair-use of "
            f"Trask 1997 and Gorrochategui 1984). Conjectural entries "
            f"are synthetic data sampled from the {source_lm_path.name} "
            f"char-bigram model (statistical derivative; underlying "
            f"corpus license recorded in {lm_rel}'s meta block) and "
            f"are released under the same terms as the lineara repo.\n"
        )

    polluted_doc = {
        "pool": polluted_pool_name,
        "source_citation": source_citation,
        "license": license_blurb,
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
    n_conjectural = sum(
        1
        for e in entries
        if str(e.get("provenance", "")).startswith("conjectural")
    )

    return {
        "base_pool": base_pool_name,
        "polluted_pool": polluted_pool_name,
        "prefix": prefix,
        "ratio_pct": ratio_pct,
        "provenance_tag": provenance_tag,
        "source_lm": str(source_lm_path) if source_lm_path else None,
        "n_entries": len(entries),
        "n_real": n_real,
        "n_conjectural": n_conjectural,
        "realized_pct_conjectural": round(realized_ratio, 1),
        "polluted_path": rel_out,
        "seed_hex": f"0x{seed_hex}",
    }


def write_readme(
    base_pool_name: str,
    pools_dir: Path,
    *,
    source_lm_path: Path | None = None,
    prefix: str | None = None,
    ratio_pct: int | None = None,
) -> Path:
    """Write the per-pool README documenting the construction algorithm
    and prominently warning that this pool is a test artifact."""
    if source_lm_path is not None and prefix is None:
        prefix = source_lm_path.stem.split("_")[-1]

    polluted_pool_name = _polluted_pool_name(base_pool_name, prefix, ratio_pct)
    provenance_tag = _provenance_tag(prefix)
    is_cross_language = source_lm_path is not None
    is_ratio_variant = ratio_pct is not None

    base_path = pools_dir / f"{base_pool_name}.yaml"
    polluted_path = pools_dir / f"{polluted_pool_name}.yaml"
    base_pool = _load_pool(base_path)
    polluted_pool = _load_pool(polluted_path)

    real_entries = [
        e for e in polluted_pool["entries"] if e.get("provenance") == "real"
    ]
    conj_entries = [
        e
        for e in polluted_pool["entries"]
        if str(e.get("provenance", "")).startswith("conjectural")
    ]

    sub_hist = _phoneme_histogram(base_pool)
    pol_hist = _phoneme_histogram(polluted_pool)
    sub_lens = _length_distribution(base_pool)
    pol_lens = _length_distribution(polluted_pool)

    seed_hex = f"0x{_seed_for(polluted_pool_name):016x}"
    try:
        lm_rel = (
            source_lm_path.resolve().relative_to(_REPO_ROOT).as_posix()
            if source_lm_path
            else None
        )
    except ValueError:
        lm_rel = str(source_lm_path) if source_lm_path else None

    lines: list[str] = []
    lines.append(f"# {polluted_pool_name} — DELIBERATELY POLLUTED TEST POOL\n")
    if is_cross_language:
        lines.append(
            "> ⚠️ **This pool is a test artifact, not a research "
            f"claim.** Half of its {len(polluted_pool['entries'])} "
            f"entries are real {base_pool_name} substrate roots; the "
            f"other half are synthetic conjectural surfaces drawn "
            f"from a *different* language's char-bigram distribution "
            f"(`{lm_rel}`), with lengths matched to the real "
            f"{base_pool_name} pool. Do **NOT** use this pool to "
            f"make substrate claims, build derived dictionaries, or "
            f"train downstream models. It exists solely for the "
            f"harness v15 / mg-7ecb cross-language pollution test: "
            f"does the framework PASS for ANY phonotactic match, or "
            f"only when the polluting distribution matches the "
            f"substrate's own?\n"
        )
        lines.append("## Why this pool exists\n")
        lines.append(
            f"v14 (mg-6b73) found that the right-tail bayesian gate "
            f"on the clean `{base_pool_name}` pool **PASSes** even "
            f"when 50% of the pool is conjectural — *provided the "
            f"conjecturals are drawn from the substrate's own "
            f"phoneme + length distribution.* The polecat's "
            f"manuscript-shape claim distilled from v14:\n\n"
            f"> The framework detects substrate-LM-phonotactic "
            f"kinship at the population level for **any pool whose "
            f"phoneme + length distribution is drawn from the "
            f"substrate's own marginal distribution.** It does NOT "
            f"detect 'real substrate vocabulary,' and does NOT "
            f"support per-sign reading claims.\n\n"
            f"That claim's validity hinges on the *'drawn from the "
            f"substrate's own marginal distribution'* clause. v15 "
            f"tests it by **deliberately violating** that clause: "
            f"conjecturals are drawn from a Mycenaean-Greek char-"
            f"bigram model (`{lm_rel}`) instead. The binary outcome:\n\n"
            f"- **Cross-language polluted pool PASSes** under the "
            f"substrate's own LM → the framework's PASS signal is "
            f"essentially trivial; any phonotactic-shape overlap "
            f"with the LM produces a PASS, regardless of distribution-"
            f"shape match.\n"
            f"- **Cross-language polluted pool FAILS** under the "
            f"substrate's own LM → the framework's PASS has real "
            f"selectivity to substrate-distribution shape; v14's "
            f"PASS-on-same-distribution-pollution holds because the "
            f"conjecturals shared {base_pool_name} shape, and the "
            f"v14 manuscript-shape claim stands as written.\n"
        )
    elif is_ratio_variant:
        realized_pct = round(
            100 * len(conj_entries) / max(len(polluted_pool["entries"]), 1)
        )
        lines.append(
            "> ⚠️ **This pool is a test artifact, not a research claim.** "
            f"Of its {len(polluted_pool['entries'])} entries, "
            f"{len(real_entries)} are real {base_pool_name} substrate "
            f"roots and {len(conj_entries)} are deliberately-conjectural "
            f"surfaces tagged as if they were real (≈{realized_pct}% "
            f"conjectural; target {ratio_pct}%). Do **NOT** use this "
            f"pool to make substrate claims, build derived dictionaries, "
            f"or train downstream models. It exists solely for the "
            f"harness v18 / mg-9f18 pollution-level sweep, which "
            f"characterizes how the right-tail bayesian gate's p-value "
            f"scales with curation noise across 10%/25%/50%/75% "
            f"conjectural pollution.\n"
        )
        lines.append("## Why this pool exists\n")
        lines.append(
            f"v14 (mg-6b73) found that the right-tail bayesian gate on "
            f"the clean `{base_pool_name}` pool **PASSes** at the same "
            f"v10-magnitude p-value even when 50% of the pool is "
            f"conjectural-same-distribution. The polecat noted that "
            f"this leaves an open question: is the gate essentially "
            f"insensitive to pollution within the substrate's "
            f"phonotactic distribution, or is there a sharp threshold "
            f"(e.g. ≥90% conjectural) at which the gate finally fails? "
            f"v18 (mg-9f18) characterizes the gate's sensitivity "
            f"gradient by sweeping the conjectural ratio across 10%, "
            f"25%, and 75% same-distribution pollution. This pool is "
            f"the **{realized_pct}% / target {ratio_pct}%** variant; "
            f"the 50% pool is `pools/polluted_aquitanian.yaml`.\n\n"
            f"The full sweep table lands in "
            f"`results/rollup.pollution_level_sweep.md`.\n"
        )
    else:
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
    if is_cross_language:
        lines.append(
            f"1. **Real half.** All {len(real_entries)} entries from "
            f"`pools/{base_pool_name}.yaml` are carried over verbatim "
            f"(surface, phonemes, gloss, semantic_field, region, "
            f"attestations, citation) and tagged `provenance: real`.\n"
            f"2. **Conjectural half.** {len(conj_entries)} synthetic "
            f"entries are drawn from the external char-bigram LM at "
            f"`{lm_rel}` under the following sampling procedure:\n"
            f"   - **Length:** same as the i-th real entry, so the "
            f"polluted pool's length distribution is exactly 2× the "
            f"real pool's. Length is **not** a confound between "
            f"provenances.\n"
            f"   - **First character:** sampled from the LM's "
            f"unigram-marginal restricted to the alphabet a..z (the "
            f"`<W>` boundary token and the space character are filtered "
            f"out so the word starts with a content character). "
            f"Weights = `unigram_count + alpha`.\n"
            f"   - **Subsequent characters:** sampled conditional on "
            f"the previous character via the bigram counts "
            f"`count(prev, c) + alpha`, again restricted to a..z so "
            f"the word never produces an early word-end. The relative "
            f"frequencies of alphabet bigrams are preserved; the "
            f"`<W>`/space boundary tokens are excluded at every step "
            f"(this is the *'regenerate to match length'* "
            f"interpretation of the brief).\n"
            f"   - **Phonemes:** each sampled character becomes a "
            f"single-character phoneme. This matches how the v8 "
            f"metric (`external_phoneme_perplexity_v0`) decomposes "
            f"phonemes to chars at scoring time.\n"
            f"   - **Region tag:** `region: aquitania` (same as real "
            f"entries — the conjecturals are deliberately indistinguishable "
            f"from real ones to the candidate generator's source_pool "
            f"routing).\n"
            f"   - **Provenance tag:** `provenance: {provenance_tag}` "
            f"(so the rollup post-processing can compute the per-"
            f"provenance breakdown of the top-20).\n"
            f"   - **No semantic_field, no gloss.** Conjecturals have "
            f"no real-world semantics.\n"
            f"3. **Uniqueness.** Conjectural surfaces are forced "
            f"unique against (a) the real pool's surfaces and (b) "
            f"prior conjecturals. Collisions trigger redraws up to "
            f"{_REDRAW_LIMIT} times, then a deterministic seed bump — "
            f"the output stays reproducible.\n"
            f"4. **Phoneme-class filter.** Every conjectural entry "
            f"must span at least two distinct phoneme classes "
            f"(V/S/C); single-class draws are redrawn so the candidate "
            f"generator does not skip any conjectural entry.\n"
            f"5. **Determinism.** Seed = `{seed_hex}` "
            f"(`sha256(\"{polluted_pool_name}:conjectural\")[:16]`). "
            f"Re-running the builder produces a byte-identical YAML. "
            f"Asserted by `harness/tests/test_polluted_pool.py`.\n"
        )
    else:
        if is_ratio_variant:
            length_note = (
                f"Length: matches `real[i mod {len(real_entries)}]` "
                f"under cyclic indexing, so the realized length "
                f"distribution preserves the real pool's distribution "
                f"in expectation (and is exact when `n_conjectural` is "
                f"a multiple of `n_real`)."
            )
        else:
            length_note = (
                "Length: same length as the i-th real entry (so the "
                "length distribution doubles exactly)."
            )
        lines.append(
            f"1. **Real half.** All {len(real_entries)} entries from "
            f"`pools/{base_pool_name}.yaml` are carried over verbatim "
            f"(surface, phonemes, gloss, semantic_field, region, "
            f"attestations, citation) and tagged `provenance: real`.\n"
            f"2. **Conjectural half.** {len(conj_entries)} synthetic "
            f"entries are drawn under the same algorithm as "
            f"`scripts/build_control_pools.py`:\n"
            f"   - {length_note}\n"
            f"   - Phonemes: sampled with replacement from the real pool's "
            f"marginal phoneme-frequency histogram.\n"
            f"   - Surface: concatenation of sampled phonemes.\n"
            f"   - **Region tag:** `region: aquitania` (so the conjectural "
            f"entries are indistinguishable from real ones to the candidate "
            f"generator's source_pool routing — the test asks whether the "
            f"framework can detect the conjecturals despite that "
            f"camouflage).\n"
            f"   - **Provenance tag:** `provenance: {provenance_tag}` "
            f"(so the rollup post-processing can compute the provenance "
            f"breakdown of the top-20).\n"
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
            f"(sha256(\"{polluted_pool_name}:conjectural\")[:16]). "
            f"Re-running the builder produces a byte-identical YAML. "
            f"Asserted by `harness/tests/test_polluted_pool.py`.\n"
        )

    lines.append("## Pool counts\n")
    lines.append(f"- Real entries:         **{len(real_entries)}**")
    lines.append(f"- Conjectural entries:  **{len(conj_entries)}**")
    lines.append(f"- Total entries:        **{len(polluted_pool['entries'])}**")
    lines.append("")

    lines.append("## Length distribution\n")
    if is_ratio_variant:
        lines.append(
            f"Real and conjectural entries share length under cyclic "
            f"indexing (`conjectural[i].length = real[i mod "
            f"{len(real_entries)}].length`). The polluted pool's "
            f"length distribution preserves the real pool's "
            f"distribution in expectation; it is exact when "
            f"`n_conjectural` is a multiple of `n_real` (e.g. 75% "
            f"pollution = 3× real_n). Length is **not** a confound "
            f"between the real and conjectural halves.\n"
        )
    else:
        lines.append("Real and conjectural entries share length pairwise (i-th "
                     "conjectural matches i-th real). The polluted pool's "
                     "length distribution is exactly 2× the real pool's.\n")
    lines.append("| length | real pool | polluted pool |")
    lines.append("|---:|---:|---:|")
    for L in sorted(set(sub_lens) | set(pol_lens)):
        lines.append(f"| {L} | {sub_lens.get(L, 0)} | {pol_lens.get(L, 0)} |")
    lines.append("")

    lines.append("## Phoneme inventory and frequency\n")
    if is_cross_language:
        lines.append(
            f"The conjectural draw uses the **{lm_rel}** char-bigram "
            f"distribution, NOT the real pool's. The polluted pool's "
            f"overall histogram is therefore the union of the real "
            f"pool's marginal distribution and the source LM's "
            f"alphabet-restricted bigram-derived marginal, which "
            f"can differ substantially. Realized counts are exact "
            f"for the realized 153 conjectural draws.\n"
        )
    else:
        if is_ratio_variant:
            ratio_factor = (
                len(conj_entries) / max(len(real_entries), 1)
            )
            lines.append(
                f"The conjectural draw uses the real pool's marginal "
                f"phoneme frequency, so the polluted pool's overall "
                f"histogram should track ~{1 + ratio_factor:.2f}× "
                f"(real + {ratio_factor:.2f}×conjectural) the real "
                f"pool's in expectation. Realized counts are "
                f"approximate due to finite sample size.\n"
            )
        else:
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
    if is_cross_language:
        lines.append(
            "- **IS:** A test fixture for the framework's distribution-"
            "shape selectivity (mg-7ecb cross-language pollution test).\n"
            "- **IS NOT:** A research claim. Conjectural surfaces are "
            "synthetic. Do not cite, do not gloss, do not derive secondary "
            "artifacts.\n"
            f"- **IS NOT:** A replacement for `pools/{base_pool_name}.yaml`. "
            f"The clean substrate pool remains the substrate-claim pool; "
            f"this polluted pool is parallel scaffolding.\n"
            f"- **Matched control:** `pools/control_{polluted_pool_name}.yaml`, "
            "built by `scripts/build_control_pools.py`. Length and "
            "phoneme-inventory matched to the polluted pool's *combined* "
            "(real + cross-language-conjectural) distribution, drawn "
            "under a distinct seed.\n"
        )
    elif is_ratio_variant:
        lines.append(
            f"- **IS:** A test fixture for the v18 pollution-level sweep "
            f"(mg-9f18). Characterizes how the right-tail bayesian "
            f"gate's p-value scales with curation noise; this is the "
            f"{ratio_pct}%-conjectural variant.\n"
            f"- **IS NOT:** A research claim. Conjectural surfaces are "
            f"synthetic. Do not cite, do not gloss, do not derive "
            f"secondary artifacts.\n"
            f"- **IS NOT:** A replacement for `pools/{base_pool_name}.yaml`. "
            f"The clean substrate pool remains the substrate-claim "
            f"pool; this polluted pool is parallel scaffolding.\n"
            f"- **Matched control:** `pools/control_{polluted_pool_name}.yaml`, "
            f"built by `scripts/build_control_pools.py`. Length and "
            f"phoneme-inventory matched to the polluted pool, drawn "
            f"under a distinct seed.\n"
        )
    else:
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

    out_path = pools_dir / f"{polluted_pool_name}.README.md"
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
    parser.add_argument(
        "--source-lm",
        type=Path,
        default=None,
        help=(
            "Optional path to an external char-bigram phoneme model JSON "
            "(format: harness.external_phoneme_model.ExternalPhonemeModel). "
            "When provided, conjectural surfaces are sampled from this LM's "
            "char-bigram distribution instead of from the substrate pool's "
            "own phoneme histogram. Used by the v15 cross-language "
            "pollution test (mg-7ecb)."
        ),
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=None,
        help=(
            "Pool-name prefix to apply when --source-lm is set. The "
            "polluted pool name becomes <prefix>_polluted_<base> and the "
            "conjectural provenance tag becomes 'conjectural_<prefix>'. "
            "Defaults to the LM filename's last underscore-segment "
            "(e.g. mycenaean_greek.json → 'greek')."
        ),
    )
    parser.add_argument(
        "--ratio-pct",
        type=int,
        default=None,
        help=(
            "Optional conjectural-share percentage in [0, 100). When "
            "set, the polluted pool's name is suffixed with `_<N>pct` "
            "and the number of conjectural entries is "
            "n_real * N / (100 - N). Used by the v18 pollution-level "
            "sweep (mg-9f18) to characterize the gate's curation-"
            "sensitivity gradient at 10/25/75 percent (50 percent "
            "remains the v14 default with --ratio-pct unset)."
        ),
    )
    args = parser.parse_args(argv)

    summary = build_polluted_pool(
        args.pool,
        args.pools_dir,
        source_lm_path=args.source_lm,
        prefix=args.prefix,
        ratio_pct=args.ratio_pct,
    )
    readme = write_readme(
        args.pool,
        args.pools_dir,
        source_lm_path=args.source_lm,
        prefix=args.prefix,
        ratio_pct=args.ratio_pct,
    )
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
