#!/usr/bin/env python3
"""chic-v5: per-sign syllable-value extraction framework (mg-7c6d).

End-to-end driver. For every CHIC syllabographic sign that is NOT in the
chic-v2 paleographic-anchor pool (the "unknown" set), this script runs
four independent lines of evidence and combines them into a tier
classification:

  Line 1 — distributional (top-3 nearest anchor plurality vote on
           phoneme class, by Bhattacharyya coefficient over four
           per-sign fingerprint dimensions)
  Line 2 — anchor-distance (top-1 nearest anchor's phoneme class,
           a strict-winner variant of line 1)
  Line 3 — substrate-consistency (per (sign, candidate-phoneme)
           paired_diff under the Eteocretan LM via
           external_phoneme_perplexity_v0; aggregated by class)
  Line 4 — cross-script paleographic (where the chic-v1
           PALEOGRAPHIC_CANDIDATES list flags a paleographic Linear A
           counterpart for the unknown sign; in practice silent for
           all 76 unknowns, since the curated list is the same one
           that became the anchor pool)

Tier classification (mechanically computed):

  tier-1   chic-v2 anchor (already established; carried over for
           leaderboard completeness)
  tier-2   ≥3 of 4 lines agree on the same proposed phoneme class
  tier-3   2 of 4 agree
  tier-4   1 of 4 (single line of evidence; not a candidate proposal)
  untiered no line of evidence yields a proposal (e.g. very low
           frequency unknown signs where the distributional
           fingerprint is too thin)

The "agreement" predicate is exact phoneme-class identity; phoneme
classes are coarser than phonemes (the framework's per-sign resolution
is unlikely to be more granular than class-level). Class taxonomy
follows the standard linguist's split applied to the Eteocretan
phoneme inventory:

  vowel:    a e i o u
  stop:     p b t d k g
  nasal:    m n
  liquid:   l r
  fricative: s f h x z
  glide:    j w y

For Linear-A-style CV syllable values like ``ka``, ``mu``, ``ja`` —
the kind of value the anchor pool carries — the class is determined
by the consonant (or by ``vowel`` if the syllable is a bare vowel).

Determinism: no RNG. Same (CHIC corpus, anchor pool, Eteocretan LM,
chic-v1 sign yaml) ⇒ byte-identical artifacts on every re-run. Where
the brief mentions a "deterministic seed" for the substrate-consistency
control, that is implemented as a hash-derived deterministic phoneme
choice (`sha256(sign_id || candidate_class)` indexes into the
class-disjoint pool), not a `random.Random(seed)` draw.

Inputs (all already committed):

  corpora/cretan_hieroglyphic/all.jsonl                    chic-v0
  corpora/cretan_hieroglyphic/syllabographic.jsonl         chic-v3
  pools/cretan_hieroglyphic_signs.yaml                     chic-v1
  pools/cretan_hieroglyphic_anchors.yaml                   chic-v2
  pools/eteocretan.yaml                                    Eteocretan
                                                            substrate-pool
                                                            phoneme inventory
  harness/external_phoneme_models/eteocretan.json          v21 LM artifact

Outputs (committed by this script):

  harness/chic_sign_fingerprints.json
  pools/cretan_hieroglyphic_signs.distributional.yaml
  results/chic_anchor_distance_map.md
  results/chic_substrate_consistency.md
  results/chic_value_extraction_leaderboard.md

Usage:
  python3 scripts/build_chic_v5.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from harness.external_phoneme_model import ExternalPhonemeModel  # noqa: E402
from harness.metrics import external_phoneme_perplexity_v0  # noqa: E402

CHIC_FULL = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
CHIC_SYLL = ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
SIGNS_YAML = ROOT / "pools" / "cretan_hieroglyphic_signs.yaml"
ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"
ETEO_POOL_YAML = ROOT / "pools" / "eteocretan.yaml"
ETEO_LM = ROOT / "harness" / "external_phoneme_models" / "eteocretan.json"

FINGERPRINTS_JSON = ROOT / "harness" / "chic_sign_fingerprints.json"
DISTRIBUTIONAL_YAML = (
    ROOT / "pools" / "cretan_hieroglyphic_signs.distributional.yaml"
)
ANCHOR_MAP_MD = ROOT / "results" / "chic_anchor_distance_map.md"
SUBSTRATE_MD = ROOT / "results" / "chic_substrate_consistency.md"
LEADERBOARD_MD = ROOT / "results" / "chic_value_extraction_leaderboard.md"

FETCHED_AT = "2026-05-05T12:00:00Z"

# Top-K nearest anchors used for the line-1 distributional plurality
# vote. The brief specifies "top-3 closest anchors" for the per-sign
# anchor-distance map; we use the same K for line-1 voting.
TOP_K_NEAREST = 3

# Frequency floor for an unknown sign to be eligible for any line of
# evidence beyond enumeration. Below this floor the per-sign
# fingerprint is too thin and the distributional / anchor-distance
# lines would be reading noise. Substrate-consistency would still be
# computable but with very few corpus hits, so we apply the floor
# uniformly. ``--min-frequency`` overrides at the CLI.
DEFAULT_MIN_FREQ = 3

# Phoneme class taxonomy. Class lookup is on the *consonant* of a CV
# syllable; bare-vowel surfaces are class ``vowel``. Multi-char surfaces
# are classified by their first consonantal char (or by their first
# char if it is a vowel).
PHONEME_CLASSES: dict[str, str] = {
    # vowels
    "a": "vowel", "e": "vowel", "i": "vowel", "o": "vowel", "u": "vowel",
    # stops
    "p": "stop", "b": "stop", "t": "stop", "d": "stop",
    "k": "stop", "g": "stop", "q": "stop",
    # nasals
    "m": "nasal", "n": "nasal",
    # liquids
    "l": "liquid", "r": "liquid",
    # fricatives
    "s": "fricative", "f": "fricative", "h": "fricative",
    "x": "fricative", "z": "fricative",
    # glides
    "j": "glide", "w": "glide", "y": "glide",
}


def classify_value(value: str) -> str:
    """Return the phoneme class of an LB-style syllable value or single
    phoneme. Looks at the first character only.
    """
    if not value:
        return "unknown"
    h = value[0].lower()
    return PHONEME_CLASSES.get(h, "unknown")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_chic_records(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])
    return records


def normalize_sign_token(tok: str) -> tuple[str | None, bool]:
    """Map a CHIC corpus token to ('#NNN', is_uncertain) or (None, False).

    Mirrors scripts/build_chic_signs.py::normalize_sign but also returns
    the uncertain flag.
    """
    if tok.startswith("#"):
        return tok, False
    if tok.startswith("[?:#") and tok.endswith("]"):
        return tok[3:-1], True
    return None, False


# ---------------------------------------------------------------------------
# Step 1 — Distributional fingerprints
# ---------------------------------------------------------------------------


def compute_fingerprints(
    records: list[dict],
    *,
    syllabographic_ids: set[str],
) -> dict[str, dict]:
    """Compute per-sign distributional fingerprints from the full CHIC
    corpus.

    Per-sign fingerprint dimensions:
      left_neighbor   Counter over neighboring sign IDs (or "BOS").
                      Sign IDs include both syllabographic and
                      ideographic neighbors observed in-corpus, since
                      the syntactic context is informative even when
                      the neighbor itself isn't a syllabogram.
      right_neighbor  Counter over neighboring sign IDs (or "EOS").
      position        Counter over {start, middle, end, single} —
                      per-block position in the syllabographic-only
                      block (DIV-bounded). Mirrors chic-v1's position
                      bucketing exactly.
      support         Counter over inscription support type (seal /
                      crescent / medallion / bar / sealing / ...).
      frequency       Total clean+uncertain occurrences in the
                      syllabographic-only stream.

    Only syllabographic signs (per ``syllabographic_ids``) get a
    fingerprint entry. Neighbor histograms span every sign-or-DIV
    token, but for purposes of "is this sign a fingerprintable
    syllabogram" we use chic-v1's classification.
    """
    fps: dict[str, dict] = {}
    for sid in syllabographic_ids:
        fps[sid] = {
            "left_neighbor": Counter(),
            "right_neighbor": Counter(),
            "position": Counter(),
            "support": Counter(),
            "frequency": 0,
            "inscription_count": 0,
            "inscription_ids": set(),
        }

    for rec in records:
        tokens = rec["tokens"]
        # Build the sign-only sequence for position bucketing (matching
        # chic-v1's logic exactly).
        sign_positions: list[tuple[str, bool]] = []  # (sign_id, is_unc)
        for tok in tokens:
            sid, is_unc = normalize_sign_token(tok)
            if sid is not None:
                sign_positions.append((sid, is_unc))
        n = len(sign_positions)
        if n == 0:
            continue
        for idx, (sid, is_unc) in enumerate(sign_positions):
            if sid not in fps:
                continue
            cell = fps[sid]
            cell["frequency"] += 1
            cell["inscription_ids"].add(rec["id"])
            cell["support"][rec.get("support") or "unknown"] += 1
            # Position thirds (chic-v1 convention).
            if n == 1:
                bucket = "single"
            elif idx < n / 3:
                bucket = "start"
            elif idx >= 2 * n / 3:
                bucket = "end"
            else:
                bucket = "middle"
            cell["position"][bucket] += 1
            # Neighbors. Use BOS / EOS sentinels at sequence ends; use
            # raw sign IDs (or the sentinel "DIV" / "[?]" tokens) as
            # neighbor labels — anything carries syntactic information.
            if idx == 0:
                cell["left_neighbor"]["BOS"] += 1
            else:
                left_sid, _ = normalize_sign_token(
                    f"#{sign_positions[idx - 1][0].lstrip('#')}"
                )
                cell["left_neighbor"][sign_positions[idx - 1][0]] += 1
            if idx == n - 1:
                cell["right_neighbor"]["EOS"] += 1
            else:
                cell["right_neighbor"][sign_positions[idx + 1][0]] += 1

    # Materialize counts: drop the inscription_ids set, record its size.
    out: dict[str, dict] = {}
    for sid, cell in fps.items():
        out[sid] = {
            "frequency": cell["frequency"],
            "inscription_count": len(cell["inscription_ids"]),
            "left_neighbor": dict(sorted(cell["left_neighbor"].items())),
            "right_neighbor": dict(sorted(cell["right_neighbor"].items())),
            "position": dict(sorted(cell["position"].items())),
            "support": dict(sorted(cell["support"].items())),
        }
    return out


def write_fingerprints_json(
    fingerprints: dict[str, dict],
    *,
    anchor_ids: set[str],
    syllabographic_ids: set[str],
    chic_corpus_path: Path,
    out_path: Path,
) -> None:
    payload = {
        "schema_version": "chic_sign_fingerprints.v1",
        "generated_by": "scripts/build_chic_v5.py",
        "ticket": "mg-7c6d",
        "fetched_at": FETCHED_AT,
        "input_corpus": str(chic_corpus_path.relative_to(ROOT)),
        "n_syllabographic_signs": len(syllabographic_ids),
        "n_anchor_signs": len(anchor_ids),
        "n_unknown_signs": len(syllabographic_ids - anchor_ids),
        "fingerprint_dimensions": [
            "left_neighbor",
            "right_neighbor",
            "position",
            "support",
        ],
        "signs": {
            sid: {
                "is_anchor": sid in anchor_ids,
                "frequency": cell["frequency"],
                "inscription_count": cell["inscription_count"],
                "left_neighbor": cell["left_neighbor"],
                "right_neighbor": cell["right_neighbor"],
                "position": cell["position"],
                "support": cell["support"],
            }
            for sid, cell in sorted(fingerprints.items())
        },
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Step 1 (cont.) — distributional yaml extension
# ---------------------------------------------------------------------------


def write_distributional_yaml(
    fingerprints: dict[str, dict],
    *,
    anchor_ids: set[str],
    out_path: Path,
) -> None:
    """Extend chic-v1's signs yaml with the chic-v5 fingerprint data.

    Emits a parallel yaml that carries only the fingerprint extension
    (left/right neighbor histograms, full position + support tallies,
    is_anchor flag). Keeps chic-v1's signs.yaml unmodified — the
    original is a chic-v1 artifact and shouldn't change.
    """
    out_lines: list[str] = []
    a = out_lines.append
    a("# Cretan Hieroglyphic per-sign distributional fingerprints "
      "(chic-v5; mg-7c6d)")
    a("# Extends chic-v1's pools/cretan_hieroglyphic_signs.yaml with the")
    a("# left/right-neighbor histograms + per-block position + support")
    a("# distributions used as input to the chic-v5 distributional and")
    a("# anchor-distance lines of evidence.")
    a("#")
    a("# Generated by scripts/build_chic_v5.py — do not hand-edit.")
    a("")
    a("catalog: cretan_hieroglyphic_signs_distributional")
    a("version: 1")
    a(f"fetched_at: '{FETCHED_AT}'")
    a("source_pool: cretan_hieroglyphic_signs.yaml")
    a("source_anchors: cretan_hieroglyphic_anchors.yaml")
    a("fingerprint_dimensions:")
    a("- left_neighbor")
    a("- right_neighbor")
    a("- position")
    a("- support")
    a(f"n_signs: {len(fingerprints)}")
    a(f"n_anchor_signs: {len(anchor_ids)}")
    a("signs:")
    for sid in sorted(fingerprints.keys(), key=lambda s: int(s.lstrip('#'))):
        cell = fingerprints[sid]
        a(f"- id: '{sid}'")
        a(f"  is_anchor: {'true' if sid in anchor_ids else 'false'}")
        a(f"  frequency: {cell['frequency']}")
        a(f"  inscription_count: {cell['inscription_count']}")
        for dim in ("left_neighbor", "right_neighbor", "position", "support"):
            d = cell[dim]
            if not d:
                a(f"  {dim}: {{}}")
                continue
            a(f"  {dim}:")
            for k, v in sorted(d.items()):
                # YAML-safe key quoting for sign-id-shaped tokens.
                key = f"'{k}'" if (
                    not k.replace("_", "").replace("-", "").isalnum()
                ) else k
                a(f"    {key}: {v}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 2 — Bhattacharyya coefficient + anchor-distance map
# ---------------------------------------------------------------------------


def _normalize(counts: dict) -> dict[str, float]:
    """Convert a count dict to a probability distribution. Empty → empty."""
    total = sum(counts.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}


def bhattacharyya(p: dict[str, float], q: dict[str, float]) -> float:
    """BC(p, q) = sum_x sqrt(p[x] * q[x]) over the union support.

    Symmetric, in [0, 1]; 1 = identical distributions. If either side
    is empty, returns 0.
    """
    if not p or not q:
        return 0.0
    keys = set(p.keys()) | set(q.keys())
    return sum(math.sqrt(p.get(k, 0.0) * q.get(k, 0.0)) for k in keys)


def fingerprint_similarity(
    fp_a: dict, fp_b: dict, *, dimensions: tuple[str, ...]
) -> tuple[float, dict[str, float]]:
    """Average Bhattacharyya coefficient across the four fingerprint
    dimensions. Returns (mean_BC, per-dim BC dict).
    """
    per_dim: dict[str, float] = {}
    for dim in dimensions:
        per_dim[dim] = bhattacharyya(
            _normalize(fp_a[dim]), _normalize(fp_b[dim])
        )
    mean_bc = sum(per_dim.values()) / len(per_dim) if per_dim else 0.0
    return mean_bc, per_dim


_FP_DIMS = ("left_neighbor", "right_neighbor", "position", "support")


def compute_anchor_distance_map(
    fingerprints: dict[str, dict],
    *,
    anchor_records: list[dict],
    unknown_ids: list[str],
    top_k: int = TOP_K_NEAREST,
) -> dict[str, list[dict]]:
    """For each unknown sign, return the top-K nearest anchors by mean
    Bhattacharyya similarity, sorted descending.
    """
    anchor_by_id = {a["chic_sign"]: a for a in anchor_records}
    results: dict[str, list[dict]] = {}
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        if sid not in fingerprints:
            continue
        ranked: list[tuple[float, str, dict[str, float]]] = []
        for anchor_id, anchor_meta in anchor_by_id.items():
            if anchor_id not in fingerprints:
                # Anchor not attested in the syllabographic stream —
                # rare; skip.
                continue
            sim, per_dim = fingerprint_similarity(
                fingerprints[sid], fingerprints[anchor_id], dimensions=_FP_DIMS
            )
            ranked.append((sim, anchor_id, per_dim))
        # Sort by similarity desc, then by anchor_id asc for determinism.
        ranked.sort(key=lambda t: (-t[0], int(t[1].lstrip("#"))))
        top = []
        for sim, anchor_id, per_dim in ranked[:top_k]:
            anchor_meta = anchor_by_id[anchor_id]
            value = anchor_meta["linear_b_carryover_phonetic"]
            top.append({
                "anchor_id": anchor_id,
                "anchor_value": value,
                "anchor_class": classify_value(value),
                "anchor_tier": anchor_meta["confidence_tier"],
                "anchor_freq": anchor_meta["frequency"],
                "similarity": round(sim, 6),
                "per_dim": {k: round(v, 6) for k, v in per_dim.items()},
            })
        results[sid] = top
    return results


def write_anchor_distance_md(
    anchor_distance: dict[str, list[dict]],
    *,
    fingerprints: dict[str, dict],
    unknown_ids: list[str],
    out_path: Path,
    top_k: int,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC anchor-distance map for unknown syllabographic signs "
      "(chic-v5; mg-7c6d)")
    a("")
    a(f"Per-unknown-sign top-{top_k} nearest anchors by mean Bhattacharyya "
      f"coefficient over four fingerprint dimensions "
      f"(`left_neighbor`, `right_neighbor`, `position`, `support`). "
      f"Each anchor proposes its phoneme class for the unknown sign. "
      f"This is the input to lines 1 (distributional plurality vote) "
      f"and 2 (anchor-distance / strict top-1) of the chic-v5 four-line "
      f"evidence framework.")
    a("")
    a("Distance is computed as 1 − BC; the table reports BC directly "
      "(higher = more distributionally similar).")
    a("")
    a(f"## Coverage")
    a("")
    a(f"- Unknown syllabographic signs (chic-v1 syllabographic minus chic-v2 "
      f"anchor pool): **{len(unknown_ids)}**")
    a(f"- Unknowns with ≥1 fingerprint occurrence: **"
      f"{sum(1 for s in unknown_ids if s in fingerprints and fingerprints[s]['frequency'] > 0)}**")
    a("")
    a("## Per-sign top-3 nearest anchors")
    a("")
    a(
        "| sign | freq | top-1 anchor / value / class / BC | "
        "top-2 anchor / value / class / BC | "
        "top-3 anchor / value / class / BC |"
    )
    a("|---|---:|---|---|---|")
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        if sid not in anchor_distance:
            continue
        freq = fingerprints[sid]["frequency"] if sid in fingerprints else 0
        cells = anchor_distance[sid]
        cell_strs: list[str] = []
        for c in cells:
            cell_strs.append(
                f"`{c['anchor_id']}` / `{c['anchor_value']}` / "
                f"{c['anchor_class']} / {c['similarity']:.4f}"
            )
        while len(cell_strs) < top_k:
            cell_strs.append("—")
        a(f"| `{sid}` | {freq} | " + " | ".join(cell_strs) + " |")
    a("")
    a("## Methodology notes")
    a("")
    a("- Fingerprint dimensions are computed over the full CHIC corpus "
      "(`corpora/cretan_hieroglyphic/all.jsonl`, chic-v0): `left_neighbor` "
      "and `right_neighbor` count adjacent sign IDs in the sign-only "
      "sequence (DIV / `[?]` are skipped); `position` buckets per-sign "
      "occurrences into start/middle/end/single thirds of the sign-only "
      "block (chic-v1 convention); `support` is the inscription support "
      "type histogram.")
    a("- Bhattacharyya coefficient is computed per dimension over the "
      "union of observed keys, after L1-normalizing each side to a "
      "probability distribution. The four per-dimension BCs are averaged "
      "to produce the final similarity score.")
    a("- An unknown sign with no fingerprint occurrences (frequency = 0) "
      "is omitted; this only happens for syllabographic signs whose "
      "every corpus occurrence is an uncertain reading collapsed to "
      "[?] without a `[?:#NNN]` annotation, which doesn't occur in the "
      "current CHIC corpus.")
    a("- Anchor-distance is symmetric and absolute; we do not normalize "
      "by the anchor's own self-similarity (which is always 1.0 by "
      "construction).")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 3 — substrate-consistency scoring
# ---------------------------------------------------------------------------


def build_anchor_mapping(anchor_records: list[dict]) -> dict[str, str]:
    """Build the chic-v2 sign→Linear-B-value mapping from the anchor pool.

    Both the clean (`#NNN`) and uncertain (`[?:#NNN]`) corpus token
    forms map to the same value, so consumers of the mapping should
    apply via the existing CHIC token convention (the
    external_phoneme_perplexity_v0 metric reads tokens raw, so we
    register both forms here).
    """
    mapping: dict[str, str] = {}
    for a in anchor_records:
        sid = a["chic_sign"]
        value = a["linear_b_carryover_phonetic"]
        mapping[sid] = value
        mapping[f"[?:{sid}]"] = value
    return mapping


def candidate_value_pool(
    anchor_records: list[dict],
    eteocretan_pool: dict,
    *,
    extra_vowels: tuple[str, ...] = ("a", "e", "i", "o", "u"),
) -> list[str]:
    """The set of candidate phoneme values to try for each unknown sign.

    Built as the union of:
      - every distinct Linear-B carryover value in the anchor pool
        (`a`, `i`, `ja`, `pa`, `ke`, `ta`, `ti`, `ro`, `ni`, `wa`,
         `ki`, `de`, `me`, `mu`, `je`, `te`, `ra`, `to`, `ma`)
      - bare-vowel phonemes a/e/i/o/u (these aren't all in the
        anchor pool; including them gives the line-3 substrate
        gate access to all 6 phoneme classes including the
        full vowel inventory)

    The Eteocretan pool is consulted only as a sanity check that
    every candidate value's first character is in the pool's
    phoneme inventory (so the LM has bigram support for it).
    """
    pool_values: set[str] = set()
    for a in anchor_records:
        pool_values.add(a["linear_b_carryover_phonetic"])
    for v in extra_vowels:
        pool_values.add(v)

    eteo_phonemes: set[str] = set()
    for entry in eteocretan_pool["entries"]:
        for ph in entry["phonemes"]:
            eteo_phonemes.add(ph)

    out: list[str] = []
    for v in sorted(pool_values):
        # Sanity: candidate's first char should be a phoneme the
        # Eteocretan LM has any bigram support for. This is a no-op
        # for the standard anchor-value set, but we keep it as a guard.
        if v[0] in eteo_phonemes or v[0] in extra_vowels:
            out.append(v)
    return out


def control_phoneme_for(
    sign_id: str, candidate: str, candidate_class: str, value_pool: list[str]
) -> str:
    """Deterministic class-disjoint control phoneme for a (sign, candidate)
    pair. Picks the value in ``value_pool`` whose class differs from
    ``candidate_class``, ranked by the sha256 hash of (sign_id, candidate)
    to spread choices across the pool reproducibly.
    """
    disjoint = [v for v in value_pool if classify_value(v) != candidate_class]
    if not disjoint:
        return candidate  # degenerate; should not happen for our pool
    seed = hashlib.sha256(
        f"{sign_id}::{candidate}".encode("utf-8")
    ).hexdigest()
    # Rank disjoint values by (hash mixed with their string), pick the
    # smallest. Deterministic, no RNG.
    keyed = sorted(
        disjoint,
        key=lambda v: hashlib.sha256(f"{seed}::{v}".encode("utf-8")).hexdigest(),
    )
    return keyed[0]


def compute_substrate_consistency(
    *,
    syll_records: list[dict],
    anchor_mapping: dict[str, str],
    unknown_ids: list[str],
    value_pool: list[str],
    lm: ExternalPhonemeModel,
) -> dict[str, list[dict]]:
    """For each unknown sign, score every (sign → candidate) pair under
    the Eteocretan LM and return per-class aggregates.

    Returns: ``{sign_id: [{class, candidate, paired_diff, ...}, ...]}``
    sorted by paired_diff descending within each sign.
    """
    # Build the syllabographic-only token stream once.
    stream: list[str] = []
    syll_records_sorted = sorted(syll_records, key=lambda r: r["id"])
    for i, rec in enumerate(syll_records_sorted):
        if int(rec.get("n_signs", 0)) <= 0:
            continue
        if stream:
            stream.append("INS_BOUNDARY")
        stream.extend(rec["tokens"])

    out: dict[str, list[dict]] = {}
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        per_candidate: list[dict] = []
        for cand in value_pool:
            cand_class = classify_value(cand)
            if cand_class == "unknown":
                continue
            ctrl = control_phoneme_for(sid, cand, cand_class, value_pool)
            ctrl_class = classify_value(ctrl)

            # Substrate mapping: chic-v2 anchors PLUS the candidate for
            # this single unknown sign (both clean and uncertain forms).
            sub_map = dict(anchor_mapping)
            sub_map[sid] = cand
            sub_map[f"[?:{sid}]"] = cand

            ctrl_map = dict(anchor_mapping)
            ctrl_map[sid] = ctrl
            ctrl_map[f"[?:{sid}]"] = ctrl

            sub_res = external_phoneme_perplexity_v0(
                stream=stream, mapping=sub_map, language_model=lm
            )
            ctrl_res = external_phoneme_perplexity_v0(
                stream=stream, mapping=ctrl_map, language_model=lm
            )
            per_candidate.append({
                "candidate": cand,
                "candidate_class": cand_class,
                "control": ctrl,
                "control_class": ctrl_class,
                "substrate_score": float(sub_res.score),
                "control_score": float(ctrl_res.score),
                "paired_diff": float(sub_res.score - ctrl_res.score),
                "n_chars_substrate": int(sub_res.n_chars_scored),
                "n_chars_control": int(ctrl_res.n_chars_scored),
            })
        per_candidate.sort(
            key=lambda c: (-c["paired_diff"], c["candidate"])
        )
        out[sid] = per_candidate
    return out


def aggregate_class_means(
    per_candidate_rows: list[dict],
) -> list[dict]:
    """Aggregate per-candidate paired_diff into per-class mean +
    membership stats. Returns rows sorted by mean_paired_diff desc."""
    by_class: dict[str, list[dict]] = defaultdict(list)
    for row in per_candidate_rows:
        by_class[row["candidate_class"]].append(row)
    out: list[dict] = []
    for cls, rows in by_class.items():
        diffs = [r["paired_diff"] for r in rows]
        mean = sum(diffs) / len(diffs)
        out.append({
            "class": cls,
            "n_candidates": len(rows),
            "mean_paired_diff": mean,
            "max_paired_diff": max(diffs),
            "best_candidate": max(rows, key=lambda r: r["paired_diff"])["candidate"],
        })
    out.sort(key=lambda r: (-r["mean_paired_diff"], r["class"]))
    return out


def write_substrate_consistency_md(
    substrate: dict[str, list[dict]],
    *,
    fingerprints: dict[str, dict],
    unknown_ids: list[str],
    value_pool: list[str],
    out_path: Path,
    top_k: int = 5,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC substrate-consistency scoring under Eteocretan LM "
      "(chic-v5; mg-7c6d)")
    a("")
    a("Per-unknown-sign substrate-consistency analysis. For every "
      "candidate phoneme value V drawn from the candidate-value pool "
      f"({len(value_pool)} values), the Eteocretan-anchored partial "
      "mapping is extended with `(unknown_sign → V)` and scored under "
      "the v21 Eteocretan LM via `external_phoneme_perplexity_v0`. "
      "The control is the same mapping with V replaced by a "
      "deterministic class-disjoint value from the same pool "
      "(seed: sha256(sign_id || candidate)). The paired_diff "
      "(substrate − control) is the per-candidate substrate-consistency "
      "score; class-level scores aggregate per-candidate diffs.")
    a("")
    a("## Candidate-value pool")
    a("")
    a("Built from the union of (a) every Linear-B carryover value in "
      "the chic-v2 anchor pool and (b) bare vowels a/e/i/o/u so the "
      "vowel class is fully covered.")
    a("")
    a("| value | class |")
    a("|---|---|")
    for v in value_pool:
        a(f"| `{v}` | {classify_value(v)} |")
    a("")
    a("## Per-sign top-K candidates")
    a("")
    a(f"Showing the top-{top_k} candidates per unknown sign by "
      "paired_diff. Positive paired_diff means the candidate scored "
      "better under the Eteocretan LM than its class-disjoint control "
      "(i.e. the candidate value, when mixed with the anchor mapping, "
      "produces phoneme runs that look more Eteocretan-like than runs "
      "produced by a non-class-matched control).")
    a("")
    a("| sign | freq | top-K candidates (value/class/paired_diff) |")
    a("|---|---:|---|")
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        if sid not in substrate:
            continue
        freq = fingerprints[sid]["frequency"] if sid in fingerprints else 0
        rows = substrate[sid][:top_k]
        cells = []
        for r in rows:
            cells.append(
                f"`{r['candidate']}` / {r['candidate_class']} / "
                f"{r['paired_diff']:+.6f}"
            )
        a(f"| `{sid}` | {freq} | " + " ; ".join(cells) + " |")
    a("")
    a("## Per-sign class-mean paired_diff")
    a("")
    a("Per-class aggregate: mean paired_diff over every candidate value "
      "in the class. The winning class for the substrate line of "
      "evidence is the one with the highest mean.")
    a("")
    a(
        "| sign | freq | "
        "vowel | stop | nasal | liquid | fricative | glide | winning class |"
    )
    a("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    cls_order = ("vowel", "stop", "nasal", "liquid", "fricative", "glide")
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        if sid not in substrate:
            continue
        freq = fingerprints[sid]["frequency"] if sid in fingerprints else 0
        agg = aggregate_class_means(substrate[sid])
        agg_by_class = {r["class"]: r for r in agg}
        row_cells = []
        for c in cls_order:
            if c in agg_by_class:
                row_cells.append(f"{agg_by_class[c]['mean_paired_diff']:+.6f}")
            else:
                row_cells.append("—")
        win = agg[0]["class"] if agg else "—"
        a(
            f"| `{sid}` | {freq} | " + " | ".join(row_cells)
            + f" | {win} |"
        )
    a("")
    a("## Methodology notes")
    a("")
    a("- Target corpus: CHIC syllabographic-only stream "
      "(`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 "
      "/ mg-9700). Same stream the chic-v3 substrate gate ran against.")
    a("- Mapping: chic-v2 anchor mapping (20 sign→Linear-B-value pairs) "
      "PLUS the candidate (or control) for the single unknown sign. "
      "Both the clean `#NNN` and uncertain `[?:#NNN]` corpus token "
      "forms are mapped to the same value.")
    a("- LM: `harness/external_phoneme_models/eteocretan.json` "
      "(v21 artifact, mg-6ccd). The chic-v3 right-tail bayesian gate "
      "PASSed for Eteocretan against CHIC at p=7.33e-04, which is "
      "the empirical justification for treating Eteocretan as the "
      "natural substrate-LM choice for chic-v5.")
    a("- Control selection is deterministic (sha256-keyed permutation "
      "of the candidate-value pool restricted to class-disjoint "
      "values); the brief's 'deterministic seed' specification is "
      "implemented as a pure hash function rather than a "
      "`random.Random(seed)` draw, eliminating any RNG dependency.")
    a("- Per-candidate `n_chars_scored` varies across candidates "
      "(the substrate run grows when the unknown sign is high-"
      "frequency); the metric's per-char normalization keeps the "
      "score comparable, but for very low-frequency unknowns the "
      "paired_diff signal is itself low-magnitude. The line-3 "
      "winning class is taken regardless of magnitude — the tier "
      "classification (line agreement) handles the noise floor.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 4 — Cross-script paleographic consistency
# ---------------------------------------------------------------------------


def cross_script_proposal(
    sid: str, signs_yaml: dict
) -> tuple[str | None, str | None, str]:
    """Look up the cross-script paleographic proposal for an unknown
    CHIC sign in chic-v1's signs yaml.

    Returns ``(proposed_value, proposed_class, note)``. For unknown
    signs that ARE in the chic-v1 PALEOGRAPHIC_CANDIDATES list (none
    of the 76 unknowns are; that list became the chic-v2 anchor pool),
    the candidates are returned. For all other unknowns, returns
    ``(None, None, "no scholarly paleographic counterpart in chic-v1
    PALEOGRAPHIC_CANDIDATES")``.
    """
    for s in signs_yaml["signs"]:
        if s["id"] == sid:
            cands = s.get("paleographic_candidates")
            if not cands:
                return None, None, "silent (no paleographic counterpart in chic-v1 catalog)"
            # Pick the highest-confidence candidate.
            confidence_rank = {"consensus": 0, "proposed": 1, "debated": 2}
            cands_sorted = sorted(
                cands, key=lambda c: confidence_rank.get(c["confidence"], 9)
            )
            top = cands_sorted[0]
            return (
                top["linear_b_value"],
                classify_value(top["linear_b_value"]),
                f"paleographic counterpart {top['linear_a_sign']} "
                f"= `{top['linear_b_value']}` "
                f"(confidence: {top['confidence']})",
            )
    return None, None, "sign not in chic-v1 signs yaml"


# ---------------------------------------------------------------------------
# Step 5 — Tier classification + leaderboard
# ---------------------------------------------------------------------------


def classify_tier(
    sid: str,
    *,
    distributional_class: str | None,
    anchor_distance_class: str | None,
    substrate_class: str | None,
    cross_script_class: str | None,
) -> tuple[int | None, str | None, dict]:
    """Compute the tier (2/3/4 or None=untiered) and proposed phoneme
    class given the four lines of evidence.

    Returns (tier, proposed_class, votes) where votes is a dict
    summarizing how many lines pointed at each class.
    """
    votes: Counter = Counter()
    line_classes = {
        "distributional": distributional_class,
        "anchor_distance": anchor_distance_class,
        "substrate": substrate_class,
        "cross_script": cross_script_class,
    }
    for cls in line_classes.values():
        if cls and cls != "unknown":
            votes[cls] += 1
    if not votes:
        return None, None, dict(line_classes)
    # Top-vote class. Tiebreak alphabetically for determinism.
    top_class, top_count = sorted(
        votes.items(), key=lambda kv: (-kv[1], kv[0])
    )[0]
    if top_count >= 3:
        tier = 2
    elif top_count == 2:
        tier = 3
    elif top_count == 1:
        tier = 4
    else:
        tier = None
    return tier, top_class, dict(line_classes)


def write_leaderboard_md(
    *,
    unknown_ids: list[str],
    fingerprints: dict[str, dict],
    anchor_distance: dict[str, list[dict]],
    substrate: dict[str, list[dict]],
    signs_yaml: dict,
    anchor_records: list[dict],
    min_freq: int,
    out_path: Path,
) -> dict:
    """Compute the per-sign tier classification and emit the leaderboard.

    Returns the rollup summary dict (counts per tier).
    """
    rows: list[dict] = []
    for sid in sorted(unknown_ids, key=lambda s: int(s.lstrip("#"))):
        freq = fingerprints[sid]["frequency"] if sid in fingerprints else 0

        # Line 1 — distributional plurality vote on top-K nearest anchors.
        nearest = anchor_distance.get(sid, [])
        if nearest and freq >= min_freq:
            class_votes = Counter(
                a["anchor_class"] for a in nearest if a["anchor_class"] != "unknown"
            )
            if class_votes:
                # Plurality; tiebreak alphabetically.
                distributional_class = sorted(
                    class_votes.items(), key=lambda kv: (-kv[1], kv[0])
                )[0][0]
                distributional_top = nearest[0]["anchor_id"]
            else:
                distributional_class = None
                distributional_top = None
        else:
            distributional_class = None
            distributional_top = None

        # Line 2 — anchor-distance: top-1 nearest anchor's class.
        if nearest and freq >= min_freq and nearest[0]["anchor_class"] != "unknown":
            anchor_distance_class = nearest[0]["anchor_class"]
            anchor_distance_top_value = nearest[0]["anchor_value"]
            anchor_distance_top_anchor = nearest[0]["anchor_id"]
            anchor_distance_top_sim = nearest[0]["similarity"]
        else:
            anchor_distance_class = None
            anchor_distance_top_value = None
            anchor_distance_top_anchor = None
            anchor_distance_top_sim = None

        # Line 3 — substrate-consistency: per-class mean paired_diff.
        sub_rows = substrate.get(sid, [])
        if sub_rows and freq >= min_freq:
            class_agg = aggregate_class_means(sub_rows)
            substrate_class = class_agg[0]["class"] if class_agg else None
            substrate_best_diff = class_agg[0]["mean_paired_diff"] if class_agg else None
            substrate_best_value = (
                class_agg[0]["best_candidate"] if class_agg else None
            )
        else:
            substrate_class = None
            substrate_best_diff = None
            substrate_best_value = None

        # Line 4 — cross-script paleographic.
        cross_value, cross_class, cross_note = cross_script_proposal(sid, signs_yaml)

        tier, proposed_class, votes = classify_tier(
            sid,
            distributional_class=distributional_class,
            anchor_distance_class=anchor_distance_class,
            substrate_class=substrate_class,
            cross_script_class=cross_class,
        )

        rows.append({
            "sign": sid,
            "frequency": freq,
            "tier": tier,
            "proposed_class": proposed_class,
            "distributional_class": distributional_class,
            "distributional_top_anchor": distributional_top,
            "anchor_distance_class": anchor_distance_class,
            "anchor_distance_top_anchor": anchor_distance_top_anchor,
            "anchor_distance_top_value": anchor_distance_top_value,
            "anchor_distance_top_sim": anchor_distance_top_sim,
            "substrate_class": substrate_class,
            "substrate_best_value": substrate_best_value,
            "substrate_best_diff": substrate_best_diff,
            "cross_script_class": cross_class,
            "cross_script_value": cross_value,
            "cross_script_note": cross_note,
            "votes": votes,
        })

    # Tier counts.
    tier_counts: Counter = Counter()
    for r in rows:
        if r["tier"] is None:
            tier_counts["untiered"] += 1
        else:
            tier_counts[f"tier-{r['tier']}"] += 1

    n_tier_2 = tier_counts.get("tier-2", 0)
    n_tier_3 = tier_counts.get("tier-3", 0)
    n_tier_4 = tier_counts.get("tier-4", 0)
    n_untiered = tier_counts.get("untiered", 0)

    # Build markdown.
    lines: list[str] = []
    a = lines.append
    a("# CHIC value-extraction leaderboard (chic-v5; mg-7c6d)")
    a("")
    a("Per-sign tier classification combining four independent lines of "
      "evidence into a single proposal-or-no-proposal verdict for "
      "every unknown CHIC syllabographic sign. Built by "
      "`scripts/build_chic_v5.py`.")
    a("")
    a("## Headline counts")
    a("")
    a("| tier | meaning | n |")
    a("|---|---|---:|")
    a(f"| tier-1 | chic-v2 anchor (already established) | "
      f"{len(anchor_records)} |")
    a(f"| tier-2 | ≥3 of 4 lines agree on a phoneme class — "
      f"**candidate proposal pending domain-expert review** | "
      f"**{n_tier_2}** |")
    a(f"| tier-3 | 2 of 4 lines agree — suggestive but insufficient "
      f"for a candidate proposal | {n_tier_3} |")
    a(f"| tier-4 | 1 of 4 lines yields a class — single line of "
      f"evidence; not a proposal | {n_tier_4} |")
    a(f"| untiered | no line of evidence yields a class (e.g. very "
      f"low-frequency signs below the n≥{min_freq} threshold) | "
      f"{n_untiered} |")
    a(f"| **total unknowns** | (chic-v1 syllabographic minus chic-v2 "
      f"anchors) | **{len(unknown_ids)}** |")
    a("")
    a("## Lines of evidence")
    a("")
    a("Four independent lines, mechanically derived per the chic-v5 "
      "brief (mg-7c6d). Phoneme classes are coarse: `vowel`, `stop`, "
      "`nasal`, `liquid`, `fricative`, `glide`. The tier-2 / tier-3 "
      "/ tier-4 thresholds are exact phoneme-class identity across "
      "the lines that yield a vote; lines that are silent (no signal) "
      "do not vote.")
    a("")
    a("- **Line 1: distributional plurality.** Per-sign Bhattacharyya "
      "similarity to every chic-v2 anchor across four fingerprint "
      f"dimensions; the top-{TOP_K_NEAREST} nearest anchors vote on "
      "phoneme class by plurality. See "
      "`results/chic_anchor_distance_map.md`.")
    a("- **Line 2: anchor-distance (strict top-1).** The single "
      "closest anchor's phoneme class. Same fingerprint machinery as "
      "line 1; differs in the aggregation. Lines 1 and 2 *can* "
      "diverge when the top-1 anchor's class differs from the "
      f"plurality of the top-{TOP_K_NEAREST}.")
    a("- **Line 3: substrate-consistency under Eteocretan LM.** For "
      "every candidate phoneme value V, mapping = "
      "(chic-v2 anchors ∪ {sign → V}) is scored against a "
      "class-disjoint deterministic-permutation control mapping. "
      "Per-class mean paired_diff picks the winning class. See "
      "`results/chic_substrate_consistency.md`.")
    a("- **Line 4: cross-script paleographic.** Where the chic-v1 "
      "PALEOGRAPHIC_CANDIDATES list flags a Linear A counterpart "
      "for the unknown sign with a known/proposed value. **Silent "
      "for all 76 unknowns in chic-v5**, because the curated "
      "paleographic-candidate list is precisely the seed for the "
      "chic-v2 anchor pool — every candidate became an anchor, so "
      "by construction no unknown carries a paleographic note. "
      "This is a documented methodological limitation: extending "
      "line 4 requires hand-curated additional paleographic "
      "associations from O&G 1996, Salgarella 2020, etc., which is "
      "out of scope for chic-v5 (and would land in chic-v6 if it "
      "were prioritised). For the leaderboard, line 4 contributes "
      "0 votes for every unknown sign.")
    a("")
    a("## Eligibility threshold")
    a("")
    a(f"Unknown signs with corpus frequency below n={min_freq} are "
      "marked **untiered** and excluded from line 1 / 2 / 3 voting; "
      "their distributional fingerprints are too thin (≤2 occurrences) "
      "to support meaningful Bhattacharyya similarity, and their "
      "substrate-consistency paired_diffs are below the noise floor. "
      "We report the count for transparency rather than dropping the "
      "rows.")
    a("")
    a("## Per-sign tier verdict")
    a("")
    a("Sorted by tier (2, 3, 4, untiered), then by sign id. Each row "
      "shows the per-line vote and the consensus proposal (where one "
      "exists).")
    a("")
    a(
        "| sign | freq | tier | proposed | "
        "L1 distributional | L2 anchor-distance | L3 substrate | "
        "L4 cross-script |"
    )
    a("|---|---:|:--:|:---:|:---:|:---:|:---:|:---:|")

    def _row_str(r: dict) -> str:
        tier = r["tier"]
        tier_str = f"tier-{tier}" if tier is not None else "—"
        proposed = r["proposed_class"] or "—"
        l1 = r["distributional_class"] or "—"
        l2 = r["anchor_distance_class"] or "—"
        l3 = r["substrate_class"] or "—"
        l4 = r["cross_script_class"] or "—"
        return (
            f"| `{r['sign']}` | {r['frequency']} | {tier_str} | "
            f"{proposed} | {l1} | {l2} | {l3} | {l4} |"
        )

    def _tier_sort(r: dict) -> tuple[int, int]:
        t = r["tier"] if r["tier"] is not None else 99
        return (t, int(r["sign"].lstrip("#")))

    rows_sorted = sorted(rows, key=_tier_sort)
    for r in rows_sorted:
        a(_row_str(r))
    a("")
    a("## Tier-2 candidate proposals (detailed)")
    a("")
    if n_tier_2 == 0:
        a("**No tier-2 candidates emerged.** Per the chic-v5 brief, "
          "this is a publishable result in its own right: mechanical "
          "per-sign value extraction with the four-line-of-evidence "
          "discipline is below the noise floor for CHIC, even with "
          "the strongest substrate (Eteocretan) PASSing the "
          "population-level right-tail bayesian gate (chic-v3, "
          "p=7.33e-04). The corpus-size caveat from chic-v3 / chic-v4 "
          "is the proximate cause: ~1420 syllabographic positions "
          "across 288 partly-fragmentary inscriptions is small for "
          "per-sign value extraction even when the substrate-pool-"
          "level signal is strong. Domain-expert review of the "
          "tier-3 candidates remains the next step; a methodological "
          "extension that would plausibly raise tier-2 yield is to "
          "add hand-curated additional paleographic associations "
          "(line 4) from O&G 1996 / Salgarella 2020, deferred to "
          "chic-v6.")
    else:
        a("Each tier-2 row below is a candidate decipherment proposal: "
          "≥3 of 4 lines of evidence (line 4 always silent for "
          "chic-v5; agreement is across lines 1, 2, 3) point at the "
          "same phoneme class for this sign. **These are candidate "
          "proposals pending domain-expert review.**")
        a("")
        a(
            "| sign | freq | proposed class | "
            "L1 nearest-anchor | L2 nearest-anchor (sim) | "
            "L3 best-value (paired_diff) | L4 paleo |"
        )
        a("|---|---:|---|---|---|---|---|")
        for r in rows_sorted:
            if r["tier"] != 2:
                continue
            l1 = (
                r["distributional_top_anchor"] or "—"
            )
            if r["anchor_distance_top_anchor"]:
                l2 = (
                    f"`{r['anchor_distance_top_anchor']}` "
                    f"(`{r['anchor_distance_top_value']}`, "
                    f"BC={r['anchor_distance_top_sim']:.4f})"
                )
            else:
                l2 = "—"
            if r["substrate_best_value"]:
                l3 = (
                    f"`{r['substrate_best_value']}` "
                    f"({r['substrate_best_diff']:+.6f})"
                )
            else:
                l3 = "—"
            l4 = r["cross_script_value"] or "—"
            a(
                f"| `{r['sign']}` | {r['frequency']} | "
                f"{r['proposed_class']} | {l1} | {l2} | {l3} | {l4} |"
            )
    a("")
    a("## Tier-3 suggestive (2 of 4 agree)")
    a("")
    if n_tier_3 == 0:
        a("None.")
    else:
        a("Same per-line columns as the main verdict table; the "
          "consensus class here has only 2 of the 3 voting lines "
          "(line 4 is silent for all chic-v5 unknowns), so it does "
          "not clear the tier-2 bar.")
        a("")
        a(
            "| sign | freq | proposed class | "
            "L1 distributional | L2 anchor-distance | L3 substrate | "
            "L4 cross-script |"
        )
        a("|---|---:|---|:---:|:---:|:---:|:---:|")
        for r in rows_sorted:
            if r["tier"] != 3:
                continue
            l1 = r["distributional_class"] or "—"
            l2 = r["anchor_distance_class"] or "—"
            l3 = r["substrate_class"] or "—"
            l4 = r["cross_script_class"] or "—"
            proposed = r["proposed_class"] or "—"
            a(
                f"| `{r['sign']}` | {r['frequency']} | "
                f"{proposed} | {l1} | {l2} | {l3} | {l4} |"
            )
    a("")
    a("## Disagreements with chic-v2 paleographic anchors")
    a("")
    a("By construction, no unknown sign is also an anchor; "
      "disagreement here means a chic-v5 line points at a phoneme "
      "class that conflicts with a *paleographically-proposed* value "
      "for the same sign. Since line 4 is silent for all 76 unknowns "
      "in chic-v5, no such disagreement is possible at the per-sign "
      "level. The chic-v6 cross-script extension would surface "
      "disagreements as a dedicated reporting column.")
    a("")
    a("## Determinism + reproducibility")
    a("")
    a("- No RNG. The brief's 'deterministic seed' for the line-3 "
      "control is implemented as a pure sha256-keyed selection from "
      "the candidate-value pool.")
    a("- Same (CHIC corpus, anchor pool, signs yaml, Eteocretan LM) "
      "→ byte-identical leaderboard. Re-running the script overwrites "
      "this file with the same content.")
    a("")
    a("## Citations")
    a("")
    a("- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum "
      "Inscriptionum Cretae* (Études Crétoises 31). Paris.")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Decorte, R. (2017, 2018). The First 'European' Writing.")
    a("- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* "
      "Amsterdam: J. C. Gieben.")
    a("- Whittaker, H. (2017). 'Of linguistic alterity in Crete: the "
      "Eteocretan inscriptions.' *Scripta Classica Israelica* 36.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "n_unknown": len(unknown_ids),
        "n_tier_2": n_tier_2,
        "n_tier_3": n_tier_3,
        "n_tier_4": n_tier_4,
        "n_untiered": n_untiered,
        "rows": rows_sorted,
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(min_freq: int = DEFAULT_MIN_FREQ, *, progress: bool = True) -> dict:
    if progress:
        print("chic-v5: loading inputs...", file=sys.stderr)
    full_records = load_chic_records(CHIC_FULL)
    syll_records = load_chic_records(CHIC_SYLL)
    signs_yaml = _load_yaml(SIGNS_YAML)
    anchors_yaml = _load_yaml(ANCHORS_YAML)
    eteo_pool = _load_yaml(ETEO_POOL_YAML)
    lm = ExternalPhonemeModel.load_json(ETEO_LM)

    syllabographic_ids = {
        s["id"] for s in signs_yaml["signs"] if s["sign_class"] == "syllabographic"
    }
    anchor_ids = {a["chic_sign"] for a in anchors_yaml["anchors"]}
    unknown_ids = sorted(syllabographic_ids - anchor_ids,
                         key=lambda s: int(s.lstrip("#")))
    if progress:
        print(
            f"  syllabographic={len(syllabographic_ids)} "
            f"anchors={len(anchor_ids)} unknowns={len(unknown_ids)}",
            file=sys.stderr,
        )

    if progress:
        print("chic-v5: computing per-sign distributional fingerprints...",
              file=sys.stderr)
    fingerprints = compute_fingerprints(
        full_records, syllabographic_ids=syllabographic_ids
    )

    write_fingerprints_json(
        fingerprints,
        anchor_ids=anchor_ids,
        syllabographic_ids=syllabographic_ids,
        chic_corpus_path=CHIC_FULL,
        out_path=FINGERPRINTS_JSON,
    )
    write_distributional_yaml(
        fingerprints, anchor_ids=anchor_ids, out_path=DISTRIBUTIONAL_YAML
    )

    if progress:
        print("chic-v5: computing anchor-distance map...", file=sys.stderr)
    anchor_distance = compute_anchor_distance_map(
        fingerprints,
        anchor_records=anchors_yaml["anchors"],
        unknown_ids=unknown_ids,
        top_k=TOP_K_NEAREST,
    )
    write_anchor_distance_md(
        anchor_distance,
        fingerprints=fingerprints,
        unknown_ids=unknown_ids,
        out_path=ANCHOR_MAP_MD,
        top_k=TOP_K_NEAREST,
    )

    if progress:
        print("chic-v5: computing substrate-consistency under Eteocretan LM...",
              file=sys.stderr)
    anchor_mapping = build_anchor_mapping(anchors_yaml["anchors"])
    value_pool = candidate_value_pool(anchors_yaml["anchors"], eteo_pool)
    substrate = compute_substrate_consistency(
        syll_records=syll_records,
        anchor_mapping=anchor_mapping,
        unknown_ids=unknown_ids,
        value_pool=value_pool,
        lm=lm,
    )
    write_substrate_consistency_md(
        substrate,
        fingerprints=fingerprints,
        unknown_ids=unknown_ids,
        value_pool=value_pool,
        out_path=SUBSTRATE_MD,
    )

    if progress:
        print("chic-v5: classifying tiers + writing leaderboard...",
              file=sys.stderr)
    summary = write_leaderboard_md(
        unknown_ids=unknown_ids,
        fingerprints=fingerprints,
        anchor_distance=anchor_distance,
        substrate=substrate,
        signs_yaml=signs_yaml,
        anchor_records=anchors_yaml["anchors"],
        min_freq=min_freq,
        out_path=LEADERBOARD_MD,
    )
    if progress:
        print(
            f"chic-v5 done | unknowns={summary['n_unknown']} "
            f"tier-2={summary['n_tier_2']} tier-3={summary['n_tier_3']} "
            f"tier-4={summary['n_tier_4']} untiered={summary['n_untiered']}",
            file=sys.stderr,
        )
    return summary


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--min-frequency", type=int, default=DEFAULT_MIN_FREQ,
        help="Frequency floor for an unknown sign to participate in "
        "lines 1/2/3 voting (default: 3).",
    )
    p.add_argument("--no-progress", action="store_true")
    args = p.parse_args(argv)
    summary = run(
        min_freq=args.min_frequency, progress=not args.no_progress,
    )
    print(json.dumps({
        "n_unknown": summary["n_unknown"],
        "n_tier_2": summary["n_tier_2"],
        "n_tier_3": summary["n_tier_3"],
        "n_tier_4": summary["n_tier_4"],
        "n_untiered": summary["n_untiered"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
