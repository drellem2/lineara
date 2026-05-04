"""Corpus-derived phoneme cluster model (mg-ddee, harness v7).

What this builds.
=================

Given the 761-record SigLA Linear-A corpus, group signs by their *corpus
distributional behavior* into k=8 latent clusters. Each cluster acts as a
proxy for a phoneme class (vowel-ish / consonant-ish / sonorant-ish /
special-token-ish). The model has three artifacts:

* ``sign_to_cluster``: dict ``AB-id → cluster_id ∈ {0..7}``.
* ``bigram_log_probs``: 8x8 matrix of add-1 Laplace-smoothed bigram
  log-probabilities over cluster-ids, learned from adjacent (sign_i,
  sign_{i+1}) pairs in each inscription.
* ``phoneme_to_modal_cluster``: hand-derived ``phoneme → cluster_id``
  mapping. The mapping is derived ONCE at build time using each cluster's
  mean position-in-word fingerprint and the per-phoneme position priors
  carried over from local_fit_v0 (Trask 1997 ch. 3 phonotactics). This is
  the only place where any prior crosses the corpus → phoneme bridge.
  *No substrate-pool identity enters the model.*

Why no substrate-pool prior in the cluster model.
=================================================

The diagnosis from mg-f419 was that v6's leaderboard-ranked-phonotactics
problem made the substrate identity of the pool add no signal on top of
phonotactic distribution. v7 (this ticket) breaks that by pulling the
clustering signal from the corpus itself, not from a substrate pool, and
by introducing paired-difference scoring as the primary view (substrate
score minus matched control score) so phonotactic baseline is subtracted
out by construction.

Design choices.
===============

* k = 8. A v0 hyperparameter; rough phoneme-class granularity (5-7
  vowel/consonant classes plus 1-3 special-token classes). Future
  tickets may revisit.
* Features per sign (all per-sign counts; concatenated then L2-normalized):
    - 4-bin position-in-word fingerprint (initial / medial / final /
      standalone) — the strongest phoneme-class signal, given a
      heavy weight (x5) so it dominates the clustering geometry;
    - 3-bin position-in-inscription distribution (start third / middle
      third / end third) — weight x2;
    - 3-bin inscription-genre distribution (accountancy / votive /
      other; "other" pools 'unknown' + 'administrative' + anything else
      so the bin width is bounded) — weight x1;
    - top-K most-frequent left-neighbors + 1 "other" bin
      (K = NEIGHBOR_TOP_K, weight x1);
    - top-K most-frequent right-neighbors + 1 "other" bin (weight x1).
  Neighbor-feature truncation keeps dimensionality low enough that
  position-in-word remains the dominant signal under L2 normalization;
  with the full vocab as neighbor dims, the neighbor block (~280 dims)
  drowns out the 4-dim position-in-word block and clustering collapses
  to "is this an AB-prefixed syllabogram or a logogram" — well-known
  but uninteresting for phoneme-class proxying.
* L2-normalize each feature vector before clustering.
* k-means with deterministic seed=42; sample k initial centroids from
  the sorted-by-id sign list (no k-means++; simpler and fully byte-stable
  given the seed).
* 100 max iterations or until assignments stop changing.

Determinism.
============

Same input corpus → same JSON. Tested by running ``--write`` twice and
comparing the file. The byte-stability is enforced by:
  * sorted vocab in feature dimensions;
  * deterministic Random(42) for centroid init;
  * pure-Python float arithmetic (no numpy);
  * sorted-key JSON serialization.

Module API.
===========

``build_model(records) -> ClusterModel``: end-to-end build from corpus
records (e.g. ``harness.corpus.load_records('corpus/all.jsonl')``).

``ClusterModel.dump_json(path)``: write the JSON artifact.

``ClusterModel.load_json(path)``: read the JSON artifact back into a
ClusterModel. Used by ``sign_prediction_perplexity_v0`` at scoring time.

CLI.
====

``python3 -m harness.corpus_phoneme_model --corpus corpus/all.jsonl
  --out harness/corpus_phoneme_model.json
  --readme harness/corpus_phoneme_model.README.md``

Re-running with the same corpus produces byte-identical JSON.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import INSCRIPTION_BOUNDARY


# ---------------------------------------------------------------------------
# Constants / hyperparameters
# ---------------------------------------------------------------------------

CLUSTER_K = 8
KMEANS_SEED = 42
KMEANS_MAX_ITERS = 100
BIGRAM_LAPLACE = 1.0  # add-1

# Genre-bin order is fixed for reproducibility.
GENRE_BINS = ("accountancy", "votive_or_inscription", "other")

# Feature weights. Position-in-word carries the strongest phoneme-class
# signal so it gets the heaviest weight; the other axes contribute texture.
W_POS_IN_WORD = 5.0
W_POS_IN_INSCRIPTION = 2.0
W_GENRE = 1.0
W_NEIGHBORS = 1.0

# Number of top-frequency neighbors to keep as explicit dims (one bin
# each side); everything else collapses into a single "other" bin per side.
NEIGHBOR_TOP_K = 30


# Position priors used to derive phoneme→cluster bridging. These are the
# same per-phoneme [initial, medial, final, standalone] distributions used
# by local_fit_v0's _PHON_POSITION_OVERRIDES (Trask 1997 ch. 3 + Hualde &
# de Urbina 2003). They enter the build of `phoneme_to_modal_cluster` only;
# they do NOT enter the cluster model itself.
PHONEME_POSITION_PROFILES: dict[str, list[float]] = {
    "a": [0.10, 0.30, 0.55, 0.05],
    "e": [0.10, 0.40, 0.45, 0.05],
    "i": [0.20, 0.45, 0.30, 0.05],
    "o": [0.05, 0.25, 0.65, 0.05],
    "u": [0.10, 0.30, 0.55, 0.05],
    "l": [0.10, 0.55, 0.30, 0.05],
    "r": [0.05, 0.65, 0.25, 0.05],
    "n": [0.20, 0.45, 0.30, 0.05],
    "m": [0.25, 0.55, 0.15, 0.05],
    "b": [0.45, 0.50, 0.02, 0.03],
    "d": [0.30, 0.65, 0.02, 0.03],
    "g": [0.35, 0.60, 0.02, 0.03],
    "k": [0.40, 0.55, 0.02, 0.03],
    "p": [0.35, 0.60, 0.02, 0.03],
    "t": [0.30, 0.65, 0.02, 0.03],
    "s": [0.30, 0.50, 0.15, 0.05],
    "z": [0.30, 0.50, 0.15, 0.05],
    "x": [0.25, 0.55, 0.15, 0.05],
    "h": [0.50, 0.40, 0.05, 0.05],
    "j": [0.40, 0.50, 0.05, 0.05],
    "w": [0.45, 0.50, 0.02, 0.03],
    # Multi-character phonemes are treated by their first character at
    # build time (we only need the position profile to derive
    # phoneme_to_modal_cluster, and the lookup is only used by that
    # bridge step).
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClusterModel:
    """Container for the corpus-derived phoneme cluster model.

    Re-built deterministically from the corpus. ``meta`` holds the
    hyperparameters used to build the model so artifacts can be diffed
    across versions.
    """

    sign_to_cluster: dict[str, int]
    cluster_position_means: dict[int, list[float]]  # cluster_id → [init, med, fin, sta]
    bigram_counts: list[list[int]]                  # 8x8 raw counts
    bigram_log_probs: list[list[float]]             # 8x8 log P(j|i) (add-1)
    phoneme_to_modal_cluster: dict[str, int]
    cluster_members: dict[int, list[str]]
    meta: dict = field(default_factory=dict)

    def dump_json(self, path: Path) -> None:
        payload = {
            "meta": self.meta,
            "sign_to_cluster": dict(sorted(self.sign_to_cluster.items())),
            "cluster_position_means": {
                str(k): self.cluster_position_means[k]
                for k in sorted(self.cluster_position_means)
            },
            "cluster_members": {
                str(k): self.cluster_members[k]
                for k in sorted(self.cluster_members)
            },
            "bigram_counts": self.bigram_counts,
            "bigram_log_probs": self.bigram_log_probs,
            "phoneme_to_modal_cluster": dict(
                sorted(self.phoneme_to_modal_cluster.items())
            ),
        }
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    @classmethod
    def load_json(cls, path: Path) -> "ClusterModel":
        data = json.loads(path.read_text(encoding="utf-8"))
        cluster_position_means = {
            int(k): list(v) for k, v in data["cluster_position_means"].items()
        }
        cluster_members = {
            int(k): list(v) for k, v in data["cluster_members"].items()
        }
        return cls(
            sign_to_cluster={k: int(v) for k, v in data["sign_to_cluster"].items()},
            cluster_position_means=cluster_position_means,
            bigram_counts=[list(row) for row in data["bigram_counts"]],
            bigram_log_probs=[list(row) for row in data["bigram_log_probs"]],
            phoneme_to_modal_cluster={
                k: int(v) for k, v in data["phoneme_to_modal_cluster"].items()
            },
            cluster_members=cluster_members,
            meta=data.get("meta", {}),
        )


# ---------------------------------------------------------------------------
# Token classification
# ---------------------------------------------------------------------------


def _is_sign_token(tok: str) -> bool:
    """A token participates in clustering iff it is not a divider, boundary,
    or compound non-syllabogram form (LOG:..., FRAC:..., [?])."""
    if tok in ("DIV", INSCRIPTION_BOUNDARY):
        return False
    if tok == "[?]":
        return False
    if ":" in tok:
        return False  # LOG:..., FRAC:..., [?:... etc
    if tok.startswith("[") or tok.endswith("]"):
        return False
    return True


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------


def _per_inscription_signs(records: list[dict]) -> list[list[str]]:
    """Per-inscription, the in-order list of sign tokens (filters out
    dividers / non-syllabograms). Records with no sign tokens drop out.

    Sorted lexicographically by inscription id for byte-stable iteration."""
    out: list[list[str]] = []
    for rec in sorted(records, key=lambda r: r["id"]):
        signs = [t for t in rec["tokens"] if _is_sign_token(t)]
        if signs:
            out.append(signs)
    return out


def _genre_bin(rec_genre: str | None) -> int:
    """Map a record's genre_hint to a fixed bin index."""
    if rec_genre == "accountancy":
        return 0
    if rec_genre == "votive_or_inscription":
        return 1
    return 2  # 'unknown' / 'administrative' / anything else


def _build_features(records: list[dict]) -> tuple[list[str], dict[str, list[float]]]:
    """Build per-sign feature vectors over the corpus.

    Returns:
        ``(vocab, features)`` where ``vocab`` is the sorted-by-id list of
        signs that appear at least once, and ``features`` is a dict
        ``sign → feature_vector`` (list[float], pre-L2-normalization,
        per-axis pre-weighted).

    Feature layout (all blocks pre-multiplied by their axis weight):
      ``[pos_in_word(4) | pos_in_inscription(3) | genre(3) |
         left_neighbor_topK+other(K+1) | right_neighbor_topK+other(K+1)]``.

    The neighbor "other" bin lumps every sign that's not in the top-K
    most-frequent global signs, so the dimension layout is stable across
    re-builds. Top-K is computed from total corpus frequency over signs
    that appear at any position; ties are broken by sorted sign id.
    """
    # Pass 1: collect vocab + global frequencies (for top-K neighbor dims).
    vocab_set: set[str] = set()
    freq: Counter[str] = Counter()
    for rec in records:
        for tok in rec["tokens"]:
            if _is_sign_token(tok):
                vocab_set.add(tok)
                freq[tok] += 1
    vocab = sorted(vocab_set)

    # Top-K most-frequent neighbors; tie-break by sign id for stability.
    top_neighbors = sorted(
        vocab, key=lambda s: (-freq[s], s)
    )[: NEIGHBOR_TOP_K]
    top_set = set(top_neighbors)
    neighbor_to_dim = {s: i for i, s in enumerate(top_neighbors)}
    n_neighbor_dims = NEIGHBOR_TOP_K + 1  # last dim = "other"

    pos_off = 0
    posi_off = 4
    genre_off = posi_off + 3
    left_off = genre_off + 3
    right_off = left_off + n_neighbor_dims
    feature_dim = right_off + n_neighbor_dims

    features: dict[str, list[float]] = {s: [0.0] * feature_dim for s in vocab}

    # Position-in-word counts come from a separate pass over words.
    word_fp = _word_position_fingerprints(records)
    for sign, counts in word_fp.items():
        if sign not in features:
            continue  # logograms / non-syllabogram tokens — not in vocab anyway
        vec = features[sign]
        for i, c in enumerate(counts):
            vec[pos_off + i] += W_POS_IN_WORD * c

    # Pass 2: position-in-inscription, genre, and neighbor counts.
    for rec in records:
        signs = [t for t in rec["tokens"] if _is_sign_token(t)]
        if not signs:
            continue
        n = len(signs)
        gbin = _genre_bin(rec.get("genre_hint"))
        for i, tok in enumerate(signs):
            vec = features[tok]
            # Position-in-inscription thirds.
            third = min(int(3 * i / n), 2)
            vec[posi_off + third] += W_POS_IN_INSCRIPTION
            # Genre bin.
            vec[genre_off + gbin] += W_GENRE
            # Top-K left neighbor.
            if i > 0:
                left = signs[i - 1]
                if left in top_set:
                    vec[left_off + neighbor_to_dim[left]] += W_NEIGHBORS
                else:
                    vec[left_off + NEIGHBOR_TOP_K] += W_NEIGHBORS
            # Top-K right neighbor.
            if i + 1 < n:
                right = signs[i + 1]
                if right in top_set:
                    vec[right_off + neighbor_to_dim[right]] += W_NEIGHBORS
                else:
                    vec[right_off + NEIGHBOR_TOP_K] += W_NEIGHBORS

    return vocab, features


def _l2_normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm <= 1e-12:
        return [0.0] * len(vec)
    return [v / norm for v in vec]


# ---------------------------------------------------------------------------
# K-means
# ---------------------------------------------------------------------------


def _sq_dist(a: list[float], b: list[float]) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def _vector_mean(vectors: list[list[float]], dim: int) -> list[float]:
    if not vectors:
        return [0.0] * dim
    out = [0.0] * dim
    for v in vectors:
        for i in range(dim):
            out[i] += v[i]
    n = len(vectors)
    return [x / n for x in out]


def _kmeans(
    vocab: list[str],
    feature_matrix: list[list[float]],
    k: int,
    seed: int,
    max_iters: int,
) -> tuple[list[int], list[list[float]]]:
    """Plain Lloyd's k-means on L2-normalized vectors.

    Initialization: ``random.Random(seed).sample(range(n), k)`` over the
    sorted-vocab order. This is fully deterministic given seed + vocab
    order. No k-means++; simpler and good enough for k=8 over ~200 points.
    """
    rng = random.Random(seed)
    n = len(feature_matrix)
    if k > n:
        raise ValueError(f"k={k} > n_signs={n}")
    init_idx = sorted(rng.sample(range(n), k))
    centroids = [list(feature_matrix[i]) for i in init_idx]
    dim = len(feature_matrix[0])

    assignments = [-1] * n
    for it in range(max_iters):
        # Assign step.
        new_assign = []
        for i, vec in enumerate(feature_matrix):
            best_c = 0
            best_d = _sq_dist(vec, centroids[0])
            for c in range(1, k):
                d = _sq_dist(vec, centroids[c])
                if d < best_d:
                    best_d = d
                    best_c = c
            new_assign.append(best_c)
        if new_assign == assignments:
            break
        assignments = new_assign

        # Update step.
        new_centroids: list[list[float]] = []
        for c in range(k):
            members = [feature_matrix[i] for i in range(n) if assignments[i] == c]
            if members:
                new_centroids.append(_vector_mean(members, dim))
            else:
                # Empty cluster — re-seat at the point furthest from any centroid.
                # Deterministic tie-break: lowest index wins.
                best_i = 0
                best_d = -1.0
                for i in range(n):
                    d = min(_sq_dist(feature_matrix[i], cc) for cc in centroids)
                    if d > best_d:
                        best_d = d
                        best_i = i
                new_centroids.append(list(feature_matrix[best_i]))
        centroids = new_centroids

    return assignments, centroids


# ---------------------------------------------------------------------------
# Bigram model over cluster-ids
# ---------------------------------------------------------------------------


def _build_bigram_model(
    records: list[dict],
    sign_to_cluster: dict[str, int],
    k: int,
) -> tuple[list[list[int]], list[list[float]]]:
    """Build the cluster-id bigram model from adjacent (sign, sign) pairs.

    Adjacency is defined within each inscription, over the
    syllabogram-only sign stream (DIV/INS_BOUNDARY/non-syllabograms are
    skipped, so a (DIV) between two signs does NOT block a bigram).
    Cross-inscription bigrams are NOT included.

    Counts are add-1 Laplace-smoothed before being log-normalized.
    """
    counts = [[0 for _ in range(k)] for _ in range(k)]
    for rec in sorted(records, key=lambda r: r["id"]):
        signs = [t for t in rec["tokens"] if _is_sign_token(t)]
        cluster_ids = [sign_to_cluster[s] for s in signs if s in sign_to_cluster]
        for a, b in zip(cluster_ids[:-1], cluster_ids[1:]):
            counts[a][b] += 1

    smoothed = [[c + BIGRAM_LAPLACE for c in row] for row in counts]
    log_probs: list[list[float]] = []
    for row in smoothed:
        total = sum(row)
        log_probs.append([math.log(v / total) for v in row])
    return counts, log_probs


# ---------------------------------------------------------------------------
# Cluster summary statistics & phoneme bridging
# ---------------------------------------------------------------------------


def _word_position_fingerprints(records: list[dict]) -> dict[str, list[int]]:
    """Per-sign in-word position counts (initial, medial, final, standalone).

    A 'word' here is a maximal run of syllabogram tokens between DIVs and
    inscription boundaries (matches harness.corpus.iter_words on the
    sign-only stream). Used for the phoneme→modal-cluster bridge so the
    bridging compares like-for-like with the per-phoneme position priors.
    """
    counts: dict[str, list[int]] = {}
    for rec in records:
        word: list[str] = []
        for tok in rec["tokens"]:
            if tok == "DIV":
                if word:
                    _accumulate_word(word, counts)
                word = []
            elif _is_sign_token(tok):
                word.append(tok)
            # logograms / fractions inside a word break it up here; treat
            # them as word-breaks for the position-fingerprint purpose.
            else:
                if word:
                    _accumulate_word(word, counts)
                word = []
        if word:
            _accumulate_word(word, counts)
    return counts


def _accumulate_word(word: list[str], counts: dict[str, list[int]]) -> None:
    n = len(word)
    if n == 1:
        counts.setdefault(word[0], [0, 0, 0, 0])[3] += 1
        return
    for i, tok in enumerate(word):
        row = counts.setdefault(tok, [0, 0, 0, 0])
        if i == 0:
            row[0] += 1
        elif i == n - 1:
            row[2] += 1
        else:
            row[1] += 1


def _normalize_to_distribution(counts: list[int]) -> list[float]:
    total = sum(counts)
    if total <= 0:
        return [0.25, 0.25, 0.25, 0.25]
    return [c / total for c in counts]


def _bhattacharyya(p: list[float], q: list[float]) -> float:
    return sum(math.sqrt(max(0.0, a) * max(0.0, b)) for a, b in zip(p, q))


def _cluster_position_means(
    sign_to_cluster: dict[str, int],
    word_fingerprints: dict[str, list[int]],
    k: int,
) -> dict[int, list[float]]:
    """Mean of L1-normalized per-sign word-position fingerprints, per cluster."""
    sums: dict[int, list[float]] = {c: [0.0, 0.0, 0.0, 0.0] for c in range(k)}
    counts: dict[int, int] = {c: 0 for c in range(k)}
    for sign, cluster_id in sign_to_cluster.items():
        dist = _normalize_to_distribution(word_fingerprints.get(sign, [0, 0, 0, 0]))
        sums[cluster_id] = [a + b for a, b in zip(sums[cluster_id], dist)]
        counts[cluster_id] += 1
    out: dict[int, list[float]] = {}
    for c in range(k):
        n = counts[c] or 1
        out[c] = [v / n for v in sums[c]]
    return out


def _phoneme_to_modal_cluster(
    cluster_position_means: dict[int, list[float]],
) -> dict[str, int]:
    """For each phoneme in PHONEME_POSITION_PROFILES, pick the cluster
    whose mean word-position fingerprint has the highest Bhattacharyya
    overlap with the phoneme's expected position profile.

    This is the only step where any prior crosses the corpus → phoneme
    bridge. The position priors come from local_fit_v0 (Trask 1997 ch. 3
    phonotactics); the bridge uses *only* per-cluster aggregate
    fingerprints, never substrate-pool identity.
    """
    out: dict[str, int] = {}
    cluster_ids = sorted(cluster_position_means)
    for phoneme, expected in PHONEME_POSITION_PROFILES.items():
        best_c = cluster_ids[0]
        best_bc = -1.0
        for c in cluster_ids:
            bc = _bhattacharyya(cluster_position_means[c], expected)
            if bc > best_bc:
                best_bc = bc
                best_c = c
        out[phoneme] = best_c
    return out


# ---------------------------------------------------------------------------
# Top-level build
# ---------------------------------------------------------------------------


def build_model(records: list[dict], *, k: int = CLUSTER_K, seed: int = KMEANS_SEED) -> ClusterModel:
    """Build the cluster model end-to-end from corpus records."""
    vocab, features = _build_features(records)
    feature_matrix = [_l2_normalize(features[s]) for s in vocab]

    assignments, _centroids = _kmeans(vocab, feature_matrix, k=k, seed=seed, max_iters=KMEANS_MAX_ITERS)
    sign_to_cluster = {s: assignments[i] for i, s in enumerate(vocab)}

    counts, log_probs = _build_bigram_model(records, sign_to_cluster, k=k)

    word_fingerprints = _word_position_fingerprints(records)
    cluster_position_means = _cluster_position_means(
        sign_to_cluster, word_fingerprints, k=k
    )
    phoneme_to_modal_cluster = _phoneme_to_modal_cluster(cluster_position_means)

    cluster_members: dict[int, list[str]] = {c: [] for c in range(k)}
    for sign, cluster_id in sorted(sign_to_cluster.items()):
        cluster_members[cluster_id].append(sign)

    meta = {
        "model_version": "v0",
        "k": k,
        "kmeans_seed": seed,
        "kmeans_max_iters": KMEANS_MAX_ITERS,
        "bigram_smoothing": "add-1 Laplace",
        "n_signs": len(vocab),
        "n_records_used": sum(1 for r in records if any(_is_sign_token(t) for t in r["tokens"])),
    }

    return ClusterModel(
        sign_to_cluster=sign_to_cluster,
        cluster_position_means=cluster_position_means,
        bigram_counts=counts,
        bigram_log_probs=log_probs,
        phoneme_to_modal_cluster=phoneme_to_modal_cluster,
        cluster_members=cluster_members,
        meta=meta,
    )


# ---------------------------------------------------------------------------
# README rendering
# ---------------------------------------------------------------------------


def render_readme(model: ClusterModel) -> str:
    out: list[str] = []
    out.append("# corpus_phoneme_model — corpus-derived phoneme cluster model\n")
    out.append(
        "Generated by `harness/corpus_phoneme_model.py` (mg-ddee, harness v7). "
        "k-means over per-sign distributional fingerprints (left/right neighbors, "
        "position-in-inscription thirds, inscription genre). No substrate-pool prior.\n"
    )
    out.append("## Build hyperparameters\n")
    for key in sorted(model.meta):
        out.append(f"- **{key}**: `{model.meta[key]}`")
    out.append("")
    out.append("## Cluster compositions\n")
    out.append("Per-cluster: mean per-sign in-word position fingerprint "
               "[initial, medial, final, standalone] over the cluster's signs, "
               "followed by the sign membership list.\n")
    for c in sorted(model.cluster_members):
        means = model.cluster_position_means[c]
        members = model.cluster_members[c]
        out.append(
            f"### Cluster {c}  (n={len(members)})\n"
            f"- Mean position fingerprint: `[init={means[0]:.3f}, med={means[1]:.3f}, "
            f"fin={means[2]:.3f}, sta={means[3]:.3f}]`\n"
            f"- Members: {', '.join(f'`{s}`' for s in members)}\n"
        )
    out.append("## Phoneme → modal cluster\n")
    out.append("Bridge between phonemes and clusters. Built once at model "
               "build time using each cluster's mean position fingerprint and the "
               "per-phoneme position priors from local_fit_v0 (Trask 1997 ch. 3). "
               "This is the only step where a phoneme-side prior enters; the "
               "cluster model itself is pure-corpus.\n")
    out.append("| phoneme | modal cluster |")
    out.append("|---|---:|")
    for ph in sorted(model.phoneme_to_modal_cluster):
        out.append(f"| `{ph}` | {model.phoneme_to_modal_cluster[ph]} |")
    out.append("")
    out.append("## Cluster bigram log-probabilities\n")
    out.append(
        "Add-1 Laplace-smoothed log P(cluster_j | cluster_i) over adjacent "
        "(sign_i, sign_{i+1}) pairs in each inscription's syllabogram-only "
        "sign stream. Rows = i, cols = j.\n"
    )
    header = "|       | " + " | ".join(f"j={j}" for j in range(len(model.bigram_log_probs))) + " |"
    out.append(header)
    out.append("|" + "---:|" * (len(model.bigram_log_probs) + 1))
    for i, row in enumerate(model.bigram_log_probs):
        cells = [f"{v:+.3f}" for v in row]
        out.append(f"| **i={i}** | " + " | ".join(cells) + " |")
    out.append("")
    out.append("## Bigram raw counts\n")
    out.append("Pre-smoothing counts for diagnostic transparency.\n")
    out.append(header)
    out.append("|" + "---:|" * (len(model.bigram_counts) + 1))
    for i, row in enumerate(model.bigram_counts):
        cells = [str(v) for v in row]
        out.append(f"| **i={i}** | " + " | ".join(cells) + " |")
    out.append("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--corpus", type=Path, default=repo_root / "corpus" / "all.jsonl"
    )
    parser.add_argument(
        "--out", type=Path, default=repo_root / "harness" / "corpus_phoneme_model.json"
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=repo_root / "harness" / "corpus_phoneme_model.README.md",
    )
    parser.add_argument("--k", type=int, default=CLUSTER_K)
    parser.add_argument("--seed", type=int, default=KMEANS_SEED)
    args = parser.parse_args(argv)

    from .corpus import load_records

    records = load_records(args.corpus)
    model = build_model(records, k=args.k, seed=args.seed)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    model.dump_json(args.out)
    args.readme.write_text(render_readme(model), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {args.readme}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
