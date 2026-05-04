#!/usr/bin/env python3
"""Bulk sweep runner — score every hypothesis listed in a generator manifest.

Reads ``hypotheses/auto/<pool>.manifest.jsonl``, scores each candidate
against ``corpus/all.jsonl`` with one or more metrics, and appends one row
per (hypothesis, metric) scoring run to ``results/experiments.jsonl``.

The runner is **resumable**. Before scoring, it builds a set of
``(hypothesis_hash, corpus_snapshot, metric)`` triples from the existing
result stream and skips any (manifest entry × selected metric) pair that
already appears. So a re-run after a partial sweep only re-scores the new
work; if neither the candidates nor the corpus nor the metric set has
changed, the re-run is a no-op.

Performance. The full corpus, token stream, sign-position fingerprints,
sign-corpus counts, corpus snapshot, and pool-derived empirical bigram
model are computed once at startup and reused across all hypothesis
scorings. Per-hypothesis work for ``local_fit_v0`` is dominated by the 200
permutation rescores; ``local_fit_v1`` and ``geographic_genre_fit_v1`` are
both O(equation length) at scoring time.

Usage:
    python3 scripts/run_sweep.py --manifest hypotheses/auto/aquitanian.manifest.jsonl
    python3 scripts/run_sweep.py --manifest <path> \\
        --metrics local_fit_v1,geographic_genre_fit_v1
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import time
import uuid
from pathlib import Path

# Allow running as `python3 scripts/run_sweep.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml
from jsonschema import Draft202012Validator

from harness import HARNESS_VERSION
from harness.corpus import (
    build_stream,
    corpus_snapshot,
    load_records,
    sign_position_fingerprints,
)
from harness.corpus_phoneme_model import ClusterModel
from harness.hypothesis import (
    SHAPE_CANDIDATE_EQUATION_V1,
    canonical_hash,
    detect_shape,
    load_and_validate,
)
from harness.metrics import (
    EmpiricalBigramModel,
    _sign_corpus_counts,
    geographic_genre_fit_v1,
    local_fit_v0,
    local_fit_v1,
    partial_mapping_compression_delta_v0,
    sign_prediction_perplexity_v0,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_RESULT_SCHEMA_PATH = _REPO_ROOT / "harness" / "schemas" / "result.v0.schema.json"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_DEFAULT_CLUSTER_MODEL = _REPO_ROOT / "harness" / "corpus_phoneme_model.json"

# Metrics that emit enough rows to need a per-metric sidecar stream
# (committed at results/experiments.<metric>.jsonl). The primary
# results/experiments.jsonl is shared across metrics; sidecars exist
# because the cumulative file is bumping into GitHub's 100 MB push
# limit. Sidecar metrics still resume off the same (hash, snapshot,
# metric) seen-set, so a re-run is no-op.
_SIDECAR_METRICS = frozenset({"sign_prediction_perplexity_v0"})


def _sidecar_path(repo_root: Path, metric: str) -> Path:
    return repo_root / "results" / f"experiments.{metric}.jsonl"

_SUPPORTED_METRICS = (
    "local_fit_v0",
    "local_fit_v1",
    "geographic_genre_fit_v1",
    "partial_mapping_compression_delta_v0",
    "sign_prediction_perplexity_v0",
)


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_pool(pool_path: Path) -> dict:
    with pool_path.open("r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StringDateLoader)


def build_pool_context(pool: dict) -> dict:
    """Pre-compute the bigram model + surface→entry lookup from a pool YAML.

    Returns:
        ``{"bigram_model": EmpiricalBigramModel,
           "by_surface": {surface: entry_dict}}``
    """
    sequences = [list(e["phonemes"]) for e in pool.get("entries", [])]
    bigram_model = EmpiricalBigramModel.from_sequences(sequences)
    by_surface = {e["surface"]: e for e in pool.get("entries", [])}
    return {"bigram_model": bigram_model, "by_surface": by_surface}


def build_pool_registry(pools_dir: Path) -> dict[str, dict]:
    """Load every ``pools/*.yaml`` and return ``{pool_name: pool_ctx}``.

    Pool-specific bigram dispatch (mg-c2af). Each candidate hypothesis
    declares its ``source_pool`` and the runner selects the matching
    bigram model from this registry; falling back to a single sweep-wide
    pool produced uninterpretable rare-sign penalties for cross-pool
    candidates (mg-7c8c). Files are loaded in sorted basename order so
    the resulting models are byte-identical across re-runs.
    """
    registry: dict[str, dict] = {}
    if not pools_dir.exists():
        return registry
    for path in sorted(pools_dir.glob("*.yaml")):
        pool = load_pool(path)
        registry[pool["pool"]] = build_pool_context(pool)
    return registry


def _existing_runs(
    results_path: Path, metrics: list[str], repo_root: Path
) -> set[tuple[str, str, str]]:
    """Return the (hypothesis_hash, corpus_snapshot, metric) triples already
    present in the result stream(s). Used to skip re-scoring during a resume.

    Reads the primary ``results/experiments.jsonl`` and, for any
    sidecar-resident metric in ``metrics``, the per-metric sidecar
    ``results/experiments.<metric>.jsonl`` as well. The metric set comes
    from the run config so we don't open every sidecar that might
    eventually exist."""
    seen: set[tuple[str, str, str]] = set()
    paths: list[Path] = [results_path]
    for m in metrics:
        if m in _SIDECAR_METRICS:
            sp = _sidecar_path(repo_root, m)
            if sp.resolve() != results_path.resolve():
                paths.append(sp)
    for p in paths:
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                seen.add(
                    (
                        row["hypothesis_hash"],
                        row.get("corpus_snapshot", ""),
                        row.get("metric", ""),
                    )
                )
    return seen


def _load_manifest(manifest_path: Path) -> list[dict]:
    rows: list[dict] = []
    with manifest_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _resolve_inscription(records: list[dict], inscription_id: str) -> dict:
    for r in records:
        if r.get("id") == inscription_id:
            return r
    raise KeyError(f"inscription not found in corpus: {inscription_id!r}")


def _signs_from_equation(record: dict, equation: dict) -> list[str]:
    """Pull syllabogram tokens within ``equation.span`` whose strings appear in
    ``equation.sign_to_phoneme``. Mirrors ``harness.run._signs_from_equation``."""
    tokens = record["tokens"]
    start, end = equation["span"]
    if start < 0 or end >= len(tokens):
        raise ValueError(
            f"equation.span {equation['span']!r} out of range for "
            f"{record['id']!r} (n_tokens={len(tokens)})"
        )
    sign_to_phoneme = equation["sign_to_phoneme"]
    expected_signs = list(sign_to_phoneme.keys())
    picked: list[str] = []
    for tok in tokens[start : end + 1]:
        if tok in sign_to_phoneme:
            picked.append(tok)
    if picked != expected_signs:
        raise ValueError(
            f"signs picked from {record['id']!r} span {equation['span']!r} "
            f"are {picked!r}, but equation.sign_to_phoneme keys are "
            f"{expected_signs!r}; the span must contain those signs in that order"
        )
    return picked


def _base_row(
    *,
    metric_name: str,
    hypothesis_path: Path,
    h_hash: str,
    n_records: int,
    snapshot: str,
    ran_at: str,
    note: str,
    repo_root: Path,
) -> dict:
    try:
        rel_hyp = str(hypothesis_path.resolve().relative_to(repo_root))
    except ValueError:
        rel_hyp = str(hypothesis_path)
    return {
        "run_id": str(uuid.uuid4()),
        "hypothesis_path": rel_hyp,
        "hypothesis_hash": h_hash,
        "harness_version": HARNESS_VERSION,
        "metric": metric_name,
        "corpus_records_used": n_records,
        "corpus_snapshot": snapshot,
        "ran_at": ran_at,
        "duration_ms": 0,
        "notes": note,
    }


def _score_one(
    *,
    metric_name: str,
    hypothesis_path: Path,
    hypothesis: dict,
    h_hash: str,
    record: dict,
    signs: list[str],
    phonemes: list[str],
    stream: list[str],
    fingerprints: dict[str, list[int]],
    sign_counts: dict[str, int],
    pool_ctx: dict | None,
    cluster_model: ClusterModel | None,
    snapshot: str,
    n_records: int,
    note: str,
    repo_root: Path,
    result_validator: Draft202012Validator,
) -> dict:
    started = time.monotonic()
    ran_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = _base_row(
        metric_name=metric_name,
        hypothesis_path=hypothesis_path,
        h_hash=h_hash,
        n_records=n_records,
        snapshot=snapshot,
        ran_at=ran_at,
        note=note,
        repo_root=repo_root,
    )

    if metric_name == "local_fit_v0":
        result = local_fit_v0(stream, signs, phonemes)
        row["score"] = float(result.score)
        row["score_control_z"] = float(result.score_control_z)
        row["metric_notes"] = result.metric_notes
    elif metric_name == "local_fit_v1":
        # Pool-specific dispatch (mg-c2af): pool_ctx may be None for
        # hypotheses whose source_pool has no matching pool YAML; the
        # metric handles that by skipping the bigram term and rescaling
        # the position weight.
        bigram_model = pool_ctx["bigram_model"] if pool_ctx is not None else None
        result = local_fit_v1(
            stream,
            signs,
            phonemes,
            bigram_model,
            sign_counts=sign_counts,
            fingerprints=fingerprints,
        )
        row["score"] = float(result.score)
        row["metric_notes"] = result.metric_notes
        row["position_term"] = float(result.position_term)
        row["bigram_term"] = (
            float(result.bigram_term) if result.bigram_term is not None else None
        )
        row["length_penalty"] = float(result.length_penalty)
        row["rare_sign_correction"] = float(result.rare_sign_correction)
    elif metric_name == "partial_mapping_compression_delta_v0":
        result = partial_mapping_compression_delta_v0(stream, signs, phonemes)
        row["score"] = float(result.score)
        row["metric_notes"] = result.metric_notes
        row["bits_per_sign_baseline"] = float(result.bits_per_sign_baseline)
        row["bits_per_sign_mapped"] = float(result.bits_per_sign_mapped)
    elif metric_name == "sign_prediction_perplexity_v0":
        if cluster_model is None:
            raise ValueError(
                "sign_prediction_perplexity_v0 requires --cluster-model "
                "to be loaded; pass --cluster-model harness/corpus_phoneme_model.json"
            )
        result = sign_prediction_perplexity_v0(
            record=record, equation=hypothesis["equation"], cluster_model=cluster_model
        )
        row["score"] = float(result.score)
        row["metric_notes"] = result.metric_notes
        row["cluster_agreement"] = int(result.cluster_agreement)
        row["window_bigram_loglik"] = float(result.window_bigram_loglik)
        row["n_pairs_scored"] = int(result.n_pairs_scored)
        row["n_window_bigrams"] = int(result.n_window_bigrams)
    elif metric_name == "geographic_genre_fit_v1":
        # Pool-specific dispatch (mg-c2af): if pool_ctx is None, fall
        # back to the hypothesis's source_pool tag for the region (the
        # _GG1_REGION_COMPAT lookup table covers cross-pool tags like
        # 'linear_b'). Semantic_field becomes None and falls back to
        # neutral 0.5 — anchors and scrambles don't carry semantic_field
        # since they aren't pool entries.
        surface = hypothesis["root"]["surface"]
        entry = (
            pool_ctx["by_surface"].get(surface) if pool_ctx is not None else None
        )
        region = entry.get("region") if entry else hypothesis.get("source_pool")
        if region == "linear_b_carryover":
            region = "linear_b"
        elif region == "pre_greek_toponym":
            region = "pre_greek"
        semantic_field = entry.get("semantic_field") if entry else None
        result = geographic_genre_fit_v1(
            region=region,
            semantic_field=semantic_field,
            site=record.get("site"),
            genre_hint=record.get("genre_hint"),
        )
        row["score"] = float(result.score)
        row["metric_notes"] = result.metric_notes
        row["region_compat"] = float(result.region_compat)
        row["semantic_compat"] = float(result.semantic_compat)
    else:
        raise ValueError(
            f"unsupported metric for sweep: {metric_name!r}; have {_SUPPORTED_METRICS}"
        )

    row["duration_ms"] = int((time.monotonic() - started) * 1000)
    result_validator.validate(row)
    return row


def _ascii_histogram(values: list[float], buckets: int = 10, width: int = 40) -> list[str]:
    if not values:
        return ["(no values)"]
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [f"  all values == {lo:.4f}  (n={len(values)})"]
    bucket_w = (hi - lo) / buckets
    counts = [0] * buckets
    for v in values:
        idx = min(int((v - lo) / bucket_w), buckets - 1)
        counts[idx] += 1
    peak = max(counts) or 1
    lines: list[str] = []
    for i, c in enumerate(counts):
        b_lo = lo + i * bucket_w
        b_hi = lo + (i + 1) * bucket_w
        bar = "#" * int(width * c / peak)
        lines.append(f"  [{b_lo:+.3f}, {b_hi:+.3f})  {bar:<{width}}  {c}")
    return lines


def _summary_block(rows_by_metric: dict[str, list[dict]]) -> list[str]:
    lines: list[str] = []
    if not rows_by_metric:
        return ["No new rows scored."]
    for metric_name, rows in rows_by_metric.items():
        if not rows:
            continue
        is_local_v0 = metric_name == "local_fit_v0"
        score_key = "score_control_z" if is_local_v0 else "score"
        zs = [float(r.get(score_key, 0.0)) for r in rows]
        n = len(zs)
        mean = sum(zs) / n
        sd = math.sqrt(sum((z - mean) ** 2 for z in zs) / n)
        median = sorted(zs)[n // 2]
        top5 = sorted(rows, key=lambda r: -float(r.get(score_key, 0.0)))[:5]

        lines.append("=" * 72)
        lines.append(f"sweep summary  ({n} runs, metric={metric_name})")
        lines.append("-" * 72)
        lines.append(f"  mean ({score_key}):   {mean:+.4f}")
        lines.append(f"  median:              {median:+.4f}")
        lines.append(f"  std:                 {sd:.4f}")
        lines.append(f"  min:                 {min(zs):+.4f}")
        lines.append(f"  max:                 {max(zs):+.4f}")
        lines.append("-" * 72)
        lines.append(f"top 5 by {score_key}:")
        for i, r in enumerate(top5, 1):
            lines.append(
                f"  {i}. {score_key}={float(r.get(score_key, 0.0)):+.4f}  "
                f"score={r['score']:+.4f}  {r['hypothesis_path']}"
            )
        lines.append("-" * 72)
        lines.append(f"{score_key} histogram (10 buckets):")
        lines.extend(_ascii_histogram(zs, buckets=10))
        lines.append("=" * 72)
    return lines


def run(
    *,
    manifest_path: Path,
    corpus_path: Path,
    results_path: Path,
    note: str,
    progress_every: int,
    repo_root: Path,
    metrics: list[str] | None = None,
    pool_path: Path | None = None,
    pools_dir: Path | None = None,
    force_rescore: bool = False,
    cluster_model_path: Path | None = None,
) -> dict:
    """Drive the bulk sweep and return a summary dict.

    Pool-specific bigram dispatch (mg-c2af): the runner builds a registry
    of all pools under ``pools_dir`` and selects each hypothesis's
    bigram model via its ``source_pool`` tag. ``pool_path``, when
    supplied, becomes a single-pool override applied to every
    hypothesis (legacy behavior; useful for diagnostic re-runs that
    deliberately ignore source_pool).
    """
    if not metrics:
        metrics = ["local_fit_v0"]
    for m in metrics:
        if m not in _SUPPORTED_METRICS:
            raise ValueError(
                f"unsupported metric {m!r}; supported: {_SUPPORTED_METRICS}"
            )

    manifest = _load_manifest(manifest_path)
    if not manifest:
        print(f"manifest is empty: {manifest_path}", file=sys.stderr)
        return {"manifest_rows": 0, "scored": 0, "skipped_resumed": 0}

    records = load_records(corpus_path)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(corpus_path, repo_root)
    fingerprints = sign_position_fingerprints(stream)
    sign_counts = _sign_corpus_counts(stream)

    if pools_dir is None:
        pools_dir = _DEFAULT_POOLS_DIR

    forced_pool_ctx: dict | None = None
    if pool_path is not None and pool_path.exists():
        forced_pool_ctx = build_pool_context(load_pool(pool_path))
        try:
            display = pool_path.relative_to(repo_root)
        except ValueError:
            display = pool_path
        print(
            f"forced pool override: {display}  |  "
            f"entries: {len(forced_pool_ctx['by_surface'])}  |  "
            f"bigram vocab: {len(forced_pool_ctx['bigram_model'].vocab)}",
            file=sys.stderr,
        )

    cluster_model: ClusterModel | None = None
    if "sign_prediction_perplexity_v0" in metrics:
        path = cluster_model_path or _DEFAULT_CLUSTER_MODEL
        if not path.exists():
            raise ValueError(
                f"sign_prediction_perplexity_v0 requires the cluster model at {path}; "
                f"build with `python3 -m harness.corpus_phoneme_model`."
            )
        cluster_model = ClusterModel.load_json(path)
        print(
            f"loaded cluster model: {path}  |  k={cluster_model.meta.get('k')}  |  "
            f"signs={len(cluster_model.sign_to_cluster)}",
            file=sys.stderr,
        )

    pool_registry = build_pool_registry(pools_dir)
    if pool_registry:
        print(
            "pool registry: "
            + ", ".join(
                f"{name}({len(ctx['by_surface'])})"
                for name, ctx in sorted(pool_registry.items())
            ),
            file=sys.stderr,
        )
    elif forced_pool_ctx is None and any(
        m in ("local_fit_v1", "geographic_genre_fit_v1") for m in metrics
    ):
        raise ValueError(
            "v1 metrics require pool YAMLs under pools/; none found and no "
            "--pool override given."
        )

    result_validator = Draft202012Validator(
        json.loads(_RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
    )

    seen = (
        set()
        if force_rescore
        else _existing_runs(results_path, list(metrics), repo_root)
    )
    n_already = sum(
        1
        for r in manifest
        for m in metrics
        if (r["hypothesis_hash"], snapshot, m) in seen
    )
    print(
        f"manifest: {len(manifest)} candidates × {len(metrics)} metric(s)  |  "
        f"already in result stream for this snapshot+metric: {n_already}",
        file=sys.stderr,
    )

    results_path.parent.mkdir(parents=True, exist_ok=True)
    rows_by_metric: dict[str, list[dict]] = {m: [] for m in metrics}
    skipped = 0
    started = time.monotonic()
    scored_total = 0

    # Open the primary stream + any per-metric sidecars. Sidecar metrics
    # (e.g. sign_prediction_perplexity_v0) write to their own file; all
    # other metrics still go to the primary stream. The sidecars exist
    # because the primary file is approaching GitHub's push-size limit.
    metric_streams: dict[str, "object"] = {}
    primary_fh = results_path.open("a", encoding="utf-8")
    sidecar_fhs: list = [primary_fh]
    for m in metrics:
        if m in _SIDECAR_METRICS:
            sp = _sidecar_path(repo_root, m)
            sp.parent.mkdir(parents=True, exist_ok=True)
            fh = sp.open("a", encoding="utf-8")
            metric_streams[m] = fh
            sidecar_fhs.append(fh)
        else:
            metric_streams[m] = primary_fh

    try:
        for i, manifest_row in enumerate(manifest, 1):
            hyp_path = repo_root / manifest_row["hypothesis_path"]
            hypothesis = None
            h_hash = None
            record = None
            signs = None
            phonemes = None
            pool_ctx: dict | None = None
            for metric_name in metrics:
                key = (manifest_row["hypothesis_hash"], snapshot, metric_name)
                if key in seen:
                    skipped += 1
                    continue
                if hypothesis is None:
                    hypothesis = load_and_validate(hyp_path)
                    h_hash = canonical_hash(hypothesis)
                    shape = detect_shape(hypothesis)
                    if shape != SHAPE_CANDIDATE_EQUATION_V1:
                        raise ValueError(
                            f"sweep runner expects candidate_equation.v1 hypotheses; "
                            f"{hyp_path} has shape {shape!r}"
                        )
                    if h_hash != manifest_row["hypothesis_hash"]:
                        raise RuntimeError(
                            f"manifest hash {manifest_row['hypothesis_hash']!r} "
                            f"!= recomputed {h_hash!r} for {hyp_path}; manifest is "
                            f"stale, regenerate with scripts/generate_candidates.py"
                        )
                    equation = hypothesis["equation"]
                    record = _resolve_inscription(records, equation["inscription_id"])
                    signs = _signs_from_equation(record, equation)
                    phonemes = list(hypothesis["root"]["phonemes"])
                    # Pool-specific bigram dispatch (mg-c2af). Forced
                    # override wins when supplied; otherwise look up
                    # by hypothesis.source_pool. Unmatched ⇒ None,
                    # which the v1 metric handles by skipping bigram.
                    if forced_pool_ctx is not None:
                        pool_ctx = forced_pool_ctx
                    else:
                        src_pool = hypothesis.get("source_pool")
                        pool_ctx = (
                            pool_registry.get(src_pool) if src_pool else None
                        )
                row = _score_one(
                    metric_name=metric_name,
                    hypothesis_path=hyp_path,
                    hypothesis=hypothesis,
                    h_hash=h_hash,
                    record=record,
                    signs=signs,
                    phonemes=phonemes,
                    stream=stream,
                    fingerprints=fingerprints,
                    sign_counts=sign_counts,
                    pool_ctx=pool_ctx,
                    cluster_model=cluster_model,
                    snapshot=snapshot,
                    n_records=n_records,
                    note=note,
                    repo_root=repo_root,
                    result_validator=result_validator,
                )
                target_fh = metric_streams[metric_name]
                target_fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                target_fh.flush()
                rows_by_metric[metric_name].append(row)
                seen.add(key)
                scored_total += 1
                if progress_every and scored_total % progress_every == 0:
                    elapsed = time.monotonic() - started
                    rate = scored_total / elapsed if elapsed > 0 else 0.0
                    print(
                        f"  scored {scored_total}  "
                        f"({rate:.1f}/s, {elapsed:.0f}s elapsed)",
                        file=sys.stderr,
                    )
    finally:
        for fh in sidecar_fhs:
            fh.close()

    elapsed = time.monotonic() - started
    print(file=sys.stderr)
    for line in _summary_block(rows_by_metric):
        print(line, file=sys.stderr)

    return {
        "manifest_rows": len(manifest),
        "metrics": list(metrics),
        "scored": scored_total,
        "skipped_resumed": skipped,
        "elapsed_s": round(elapsed, 2),
        "snapshot": snapshot,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, required=True, help="Manifest JSONL path.")
    parser.add_argument(
        "--corpus", type=Path, default=_DEFAULT_CORPUS, help="Corpus JSONL path."
    )
    parser.add_argument(
        "--results", type=Path, default=_DEFAULT_RESULTS, help="Result stream path."
    )
    parser.add_argument(
        "--note", default="", help="Free-form note attached to every result row."
    )
    parser.add_argument(
        "--metrics",
        default="local_fit_v0",
        help=(
            "Comma-separated list of metric names. "
            f"Supported: {','.join(_SUPPORTED_METRICS)}. Default: local_fit_v0."
        ),
    )
    parser.add_argument(
        "--pool",
        type=Path,
        default=None,
        help="Path to a single pool YAML to FORCE for every hypothesis. "
        "Default behavior (recommended) is per-hypothesis dispatch via "
        "source_pool against pools/ — this flag exists for diagnostic "
        "re-runs that deliberately ignore source_pool.",
    )
    parser.add_argument(
        "--pools-dir",
        type=Path,
        default=_DEFAULT_POOLS_DIR,
        help="Directory of pool YAMLs used for per-hypothesis source_pool "
        "dispatch (default: pools/).",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=200,
        help="Print a progress line every N scored runs (default: %(default)s).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="Repo root used for hypothesis-path resolution and corpus snapshot.",
    )
    parser.add_argument(
        "--force-rescore",
        action="store_true",
        help="Always append; ignore the (hash, snapshot, metric) resume cache. "
        "Used by mg-c2af to re-score under the fixed pool-bigram dispatch.",
    )
    parser.add_argument(
        "--cluster-model",
        type=Path,
        default=_DEFAULT_CLUSTER_MODEL,
        help="Path to the corpus-derived phoneme cluster model JSON used by "
        "sign_prediction_perplexity_v0 (default: %(default)s).",
    )
    args = parser.parse_args(argv)

    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    summary = run(
        manifest_path=args.manifest,
        corpus_path=args.corpus,
        results_path=args.results,
        note=args.note,
        progress_every=args.progress_every,
        repo_root=args.repo_root,
        metrics=metrics,
        pool_path=args.pool,
        pools_dir=args.pools_dir,
        force_rescore=args.force_rescore,
        cluster_model_path=args.cluster_model,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
