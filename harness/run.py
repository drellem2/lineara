"""Harness CLI: validate a hypothesis, score it, append a row to the result stream."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import uuid
from pathlib import Path

from jsonschema import Draft202012Validator

from . import HARNESS_VERSION
from .corpus import build_stream, corpus_snapshot, load_records, sign_position_fingerprints
from .hypothesis import (
    SHAPE_CANDIDATE_EQUATION_V1,
    SHAPE_V0,
    canonical_hash,
    detect_shape,
    load_and_validate,
)
from .metrics import (
    METRICS,
    EmpiricalBigramModel,
    _sign_corpus_counts,
    compression_delta_v0,
    geographic_genre_fit_v1,
    local_fit_v0,
    local_fit_v1,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_RESULT_SCHEMA_PATH = Path(__file__).parent / "schemas" / "result.v0.schema.json"


# Each shape pins its default metric. Users can still pass --metric to override
# (e.g. for diagnostic reasons), but the dispatch below makes the common case
# zero-configuration.
_DEFAULT_METRIC_FOR_SHAPE = {
    SHAPE_V0: "compression_delta_v0",
    SHAPE_CANDIDATE_EQUATION_V1: "local_fit_v0",
}


_LOCAL_FIT_METRICS = {"local_fit_v0", "local_fit_v1"}
_CANDIDATE_EQUATION_METRICS = _LOCAL_FIT_METRICS | {"geographic_genre_fit_v1"}


def _load_result_validator() -> Draft202012Validator:
    with _RESULT_SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        return Draft202012Validator(json.load(fh))


def _resolve_inscription(records: list[dict], inscription_id: str) -> dict:
    for r in records:
        if r.get("id") == inscription_id:
            return r
    raise KeyError(f"inscription not found in corpus: {inscription_id!r}")


def _signs_from_equation(record: dict, equation: dict) -> list[str]:
    """Pull the signs at ``equation.span`` whose token matches a key in
    ``equation.sign_to_phoneme``, in span order.

    Non-syllabogram tokens (DIV, LOG:, FRAC:, [?]) inside the span are
    *skipped* — they do not consume a phoneme. The hypothesis author is
    responsible for picking a span that contains exactly as many syllabogram
    tokens as there are phonemes.
    """
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


def _build_v0_row(
    *,
    hypothesis: dict,
    h_hash: str,
    rel_hyp: str,
    metric_name: str,
    stream: list[str],
    n_records: int,
    snapshot: str,
    ran_at: str,
    duration_ms: int,
    note: str,
) -> dict:
    if metric_name != "compression_delta_v0":
        raise ValueError(
            f"hypothesis.v0 shape requires metric=compression_delta_v0; got {metric_name!r}"
        )
    result = compression_delta_v0(stream, hypothesis.get("mapping", {}))
    return {
        "run_id": str(uuid.uuid4()),
        "hypothesis_path": rel_hyp,
        "hypothesis_hash": h_hash,
        "harness_version": HARNESS_VERSION,
        "metric": metric_name,
        "score": result.score,
        "bits_per_sign_baseline": result.bits_per_sign_baseline,
        "bits_per_sign_mapped": result.bits_per_sign_mapped,
        "corpus_records_used": n_records,
        "corpus_snapshot": snapshot,
        "ran_at": ran_at,
        "duration_ms": duration_ms,
        "notes": note,
    }


def _load_pool_for(pool_path: Path | None, hypothesis: dict, repo_root: Path) -> dict | None:
    """Load and pre-compute a pool context for v1 metrics.

    Inference order:
      1. Explicit ``pool_path`` argument.
      2. ``hypothesis['source_pool']`` if a matching ``pools/<name>.yaml``
         exists.
      3. None (caller must error out if a v1 metric is selected).
    """
    import yaml

    class _StringDateLoader(yaml.SafeLoader):
        pass

    _StringDateLoader.yaml_implicit_resolvers = {
        k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    candidates: list[Path] = []
    if pool_path is not None:
        candidates.append(pool_path)
    src_pool = hypothesis.get("source_pool")
    if src_pool:
        candidates.append(repo_root / "pools" / f"{src_pool}.yaml")
        # Curated hypotheses can have source_pool tags like "linear_b_carryover"
        # or "random_scramble" with no matching pool YAML. Fall back to the
        # aquitanian pool so the empirical bigram model has data; the
        # geographic compat tables include a 'linear_b' region row.
        candidates.append(repo_root / "pools" / "aquitanian.yaml")

    for c in candidates:
        if c.exists():
            with c.open("r", encoding="utf-8") as fh:
                pool = yaml.load(fh, Loader=_StringDateLoader)
            sequences = [list(e["phonemes"]) for e in pool.get("entries", [])]
            return {
                "path": c,
                "pool": pool,
                "bigram_model": EmpiricalBigramModel.from_sequences(sequences),
                "by_surface": {e["surface"]: e for e in pool.get("entries", [])},
            }
    return None


def _build_candidate_equation_row(
    *,
    hypothesis: dict,
    h_hash: str,
    rel_hyp: str,
    metric_name: str,
    stream: list[str],
    records: list[dict],
    n_records: int,
    snapshot: str,
    ran_at: str,
    duration_ms: int,
    note: str,
    pool_ctx: dict | None,
) -> dict:
    if metric_name not in _CANDIDATE_EQUATION_METRICS:
        raise ValueError(
            f"candidate_equation.v1 shape requires one of "
            f"{sorted(_CANDIDATE_EQUATION_METRICS)}; got {metric_name!r}"
        )
    equation = hypothesis["equation"]
    record = _resolve_inscription(records, equation["inscription_id"])
    signs = _signs_from_equation(record, equation)
    phonemes = list(hypothesis["root"]["phonemes"])

    base = {
        "run_id": str(uuid.uuid4()),
        "hypothesis_path": rel_hyp,
        "hypothesis_hash": h_hash,
        "harness_version": HARNESS_VERSION,
        "metric": metric_name,
        "corpus_records_used": n_records,
        "corpus_snapshot": snapshot,
        "ran_at": ran_at,
        "duration_ms": duration_ms,
        "notes": note,
    }

    if metric_name == "local_fit_v0":
        result = local_fit_v0(stream, signs, phonemes)
        base.update(
            {
                "score": float(result.score),
                "score_control_z": float(result.score_control_z),
                "metric_notes": result.metric_notes,
            }
        )
    elif metric_name == "local_fit_v1":
        if pool_ctx is None:
            raise ValueError("local_fit_v1 requires a pool context (--pool)")
        fingerprints = sign_position_fingerprints(stream)
        sign_counts = _sign_corpus_counts(stream)
        result = local_fit_v1(
            stream,
            signs,
            phonemes,
            pool_ctx["bigram_model"],
            sign_counts=sign_counts,
            fingerprints=fingerprints,
        )
        base.update(
            {
                "score": float(result.score),
                "metric_notes": result.metric_notes,
                "position_term": float(result.position_term),
                "bigram_term": float(result.bigram_term),
                "length_penalty": float(result.length_penalty),
                "rare_sign_correction": float(result.rare_sign_correction),
            }
        )
    elif metric_name == "geographic_genre_fit_v1":
        if pool_ctx is None:
            raise ValueError(
                "geographic_genre_fit_v1 requires a pool context (--pool)"
            )
        surface = hypothesis["root"]["surface"]
        entry = pool_ctx["by_surface"].get(surface)
        region = entry.get("region") if entry else None
        semantic_field = entry.get("semantic_field") if entry else None
        result = geographic_genre_fit_v1(
            region=region,
            semantic_field=semantic_field,
            site=record.get("site"),
            genre_hint=record.get("genre_hint"),
        )
        base.update(
            {
                "score": float(result.score),
                "metric_notes": result.metric_notes,
                "region_compat": float(result.region_compat),
                "semantic_compat": float(result.semantic_compat),
            }
        )
    return base


def score_hypothesis(
    hypothesis_path: Path,
    metric_name: str | None = None,
    note: str = "",
    corpus_path: Path = _DEFAULT_CORPUS,
    repo_root: Path = _REPO_ROOT,
    pool_path: Path | None = None,
) -> dict:
    """Run one scoring pass and return the result row dict (not yet persisted).

    If ``metric_name`` is None, dispatches based on the hypothesis shape:
    ``hypothesis.v0`` → ``compression_delta_v0``, ``candidate_equation.v1``
    → ``local_fit_v0``.

    For v1 metrics (local_fit_v1, geographic_genre_fit_v1), a pool YAML is
    needed; ``pool_path`` overrides inference. When omitted, falls back
    to ``hypothesis.source_pool`` → ``pools/<src>.yaml`` and finally to
    ``pools/aquitanian.yaml`` so curated cross-pool hypotheses still score.
    """
    hypothesis = load_and_validate(hypothesis_path)
    h_hash = canonical_hash(hypothesis)
    shape = detect_shape(hypothesis)

    if metric_name is None:
        metric_name = _DEFAULT_METRIC_FOR_SHAPE[shape]
    if metric_name not in METRICS:
        raise ValueError(f"unknown metric {metric_name!r}; have: {sorted(METRICS)}")

    records = load_records(corpus_path)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(corpus_path, repo_root)

    started = time.monotonic()
    ran_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        rel_hyp = str(hypothesis_path.resolve().relative_to(repo_root))
    except ValueError:
        rel_hyp = str(hypothesis_path)

    if shape == SHAPE_V0:
        row = _build_v0_row(
            hypothesis=hypothesis,
            h_hash=h_hash,
            rel_hyp=rel_hyp,
            metric_name=metric_name,
            stream=stream,
            n_records=n_records,
            snapshot=snapshot,
            ran_at=ran_at,
            duration_ms=0,  # filled in below
            note=note,
        )
    elif shape == SHAPE_CANDIDATE_EQUATION_V1:
        pool_ctx: dict | None = None
        if metric_name in ("local_fit_v1", "geographic_genre_fit_v1"):
            pool_ctx = _load_pool_for(pool_path, hypothesis, repo_root)
        row = _build_candidate_equation_row(
            hypothesis=hypothesis,
            h_hash=h_hash,
            rel_hyp=rel_hyp,
            metric_name=metric_name,
            stream=stream,
            records=records,
            n_records=n_records,
            snapshot=snapshot,
            ran_at=ran_at,
            duration_ms=0,
            note=note,
            pool_ctx=pool_ctx,
        )
    else:  # pragma: no cover - guarded earlier
        raise ValueError(f"unhandled hypothesis shape: {shape}")

    row["duration_ms"] = int((time.monotonic() - started) * 1000)
    _load_result_validator().validate(row)
    return row


def append_row(row: dict, results_path: Path = _DEFAULT_RESULTS) -> None:
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with results_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.run")
    parser.add_argument("hypothesis", type=Path, help="Path to a hypothesis YAML.")
    parser.add_argument(
        "--metric",
        default=None,
        choices=sorted(METRICS),
        help="Scoring metric name. Defaults to the metric paired with the hypothesis shape.",
    )
    parser.add_argument("--note", default="", help="Free-form note attached to the result row.")
    parser.add_argument(
        "--corpus",
        type=Path,
        default=_DEFAULT_CORPUS,
        help="Path to corpus JSONL (default: corpus/all.jsonl).",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=_DEFAULT_RESULTS,
        help="Path to append-only result stream (default: results/experiments.jsonl).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="Repo root used to resolve relative paths and the corpus snapshot.",
    )
    parser.add_argument(
        "--pool",
        type=Path,
        default=None,
        help="Pool YAML path (used by v1 metrics; inferred from "
        "hypothesis.source_pool when omitted).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Score and print the row, but do not append to the result stream.",
    )
    args = parser.parse_args(argv)

    row = score_hypothesis(
        hypothesis_path=args.hypothesis,
        metric_name=args.metric,
        note=args.note,
        corpus_path=args.corpus,
        repo_root=args.repo_root,
        pool_path=args.pool,
    )
    if not args.dry_run:
        append_row(row, args.results)
    print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
