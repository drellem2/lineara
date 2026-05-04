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
from .corpus import build_stream, corpus_snapshot, load_records
from .hypothesis import canonical_hash, load_and_validate
from .metrics import METRICS


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_RESULTS = _REPO_ROOT / "results" / "experiments.jsonl"
_RESULT_SCHEMA_PATH = Path(__file__).parent / "schemas" / "result.v0.schema.json"


def _load_result_validator() -> Draft202012Validator:
    with _RESULT_SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        return Draft202012Validator(json.load(fh))


def score_hypothesis(
    hypothesis_path: Path,
    metric_name: str = "compression_delta_v0",
    note: str = "",
    corpus_path: Path = _DEFAULT_CORPUS,
    repo_root: Path = _REPO_ROOT,
) -> dict:
    """Run one scoring pass and return the result row dict (not yet persisted)."""
    if metric_name not in METRICS:
        raise ValueError(f"unknown metric {metric_name!r}; have: {sorted(METRICS)}")

    hypothesis = load_and_validate(hypothesis_path)
    h_hash = canonical_hash(hypothesis)

    records = load_records(corpus_path)
    stream, n_records = build_stream(records)
    snapshot = corpus_snapshot(corpus_path, repo_root)

    metric = METRICS[metric_name]
    started = time.monotonic()
    ran_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = metric(stream, hypothesis.get("mapping", {}))
    duration_ms = int((time.monotonic() - started) * 1000)

    try:
        rel_hyp = str(hypothesis_path.resolve().relative_to(repo_root))
    except ValueError:
        rel_hyp = str(hypothesis_path)

    row = {
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
        default="compression_delta_v0",
        choices=sorted(METRICS),
        help="Scoring metric name (default: compression_delta_v0).",
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
    )
    if not args.dry_run:
        append_row(row, args.results)
    print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
