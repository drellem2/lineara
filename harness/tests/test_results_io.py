"""Tests for the sharded result-stream layout (mg-1c82a).

GitHub refuses pushed blobs over 100 MB and ``results/*.jsonl`` only
grows, so streams roll into ``<name>.shards/NNNN.jsonl``. These tests
pin (a) every committed results file stays under 50 MB, (b) the
appender rolls before the cap and never splits a row, and (c) loaders
see the sharded stream exactly as they saw the single file, including
newest-by-``ran_at`` / first-seen-on-tie selection.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from harness import results_io  # noqa: E402

_LIMIT_BYTES = 50 * 1000 * 1000


def _committed_results_files() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--", "results"],
            cwd=_REPO_ROOT, capture_output=True, check=True,
        ).stdout.decode("utf-8")
        files = [_REPO_ROOT / p for p in out.split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        files = [p for p in (_REPO_ROOT / "results").rglob("*") if p.is_file()]
    return [p for p in files if p.exists()]


def _row(h: str, ran_at: str, score: float, lang: str = "basque") -> str:
    return json.dumps({
        "metric": "external_phoneme_perplexity_v0",
        "hypothesis_hash": h,
        "language": lang,
        "ran_at": ran_at,
        "score": score,
    }) + "\n"


class CommittedResultsSizeTest(unittest.TestCase):
    def test_every_committed_results_file_under_50mb(self) -> None:
        files = _committed_results_files()
        # Positive control: the instrument must actually see the streams.
        self.assertIn(_REPO_ROOT / "results" / "experiments.jsonl", files)
        over = [
            (str(p.relative_to(_REPO_ROOT)), p.stat().st_size)
            for p in files
            if p.stat().st_size >= _LIMIT_BYTES
        ]
        self.assertEqual(over, [], "results files at/over 50 MB; shard them "
                         "with harness.results_io.reshard")

    def test_shard_cap_is_below_test_limit(self) -> None:
        self.assertLess(results_io.SHARD_MAX_BYTES, _LIMIT_BYTES)


class ShardedAppenderTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_rolls_without_splitting_rows_and_preserves_order(self) -> None:
        base = self.dir / "experiments.m.under_x_lm.jsonl"
        rows = [_row(f"h{i:03d}", "2026-01-01T00:00:00Z", i) for i in range(50)]
        cap = len(rows[0]) * 7 + 3
        with results_io.ShardedAppender(base, max_bytes=cap) as fh:
            for r in rows[:20]:
                fh.write(r)
        # A second run resumes on the last shard rather than the base.
        with results_io.ShardedAppender(base, max_bytes=cap) as fh:
            for r in rows[20:]:
                fh.write(r)
        phys = results_io.physical_paths(base)
        self.assertEqual(phys[0], base)
        self.assertGreater(len(phys), 2)
        self.assertEqual(
            [p.name for p in phys[1:]],
            [f"{i:04d}.jsonl" for i in range(1, len(phys))],
        )
        for p in phys:
            self.assertLessEqual(p.stat().st_size, cap)
            self.assertTrue(p.read_text().endswith("\n"))
        self.assertEqual("".join(results_io.iter_lines(base)), "".join(rows))

    def test_shard_dir_not_matched_by_tag_glob(self) -> None:
        base = self.dir / "experiments.m.jsonl"
        tagged = self.dir / "experiments.m.t.jsonl"
        for p in (base, tagged):
            with results_io.ShardedAppender(p, max_bytes=10) as fh:
                fh.write(_row("a", "x", 1))
                fh.write(_row("b", "x", 2))
        self.assertEqual(
            results_io.metric_stream_paths(self.dir, "m"),
            [self.dir / "experiments.jsonl", base, tagged],
        )

    def test_reshard_is_byte_identical(self) -> None:
        base = self.dir / "experiments.jsonl"
        rows = [_row(f"h{i}", f"2026-01-0{i % 9 + 1}T00:00:00Z", i)
                for i in range(40)]
        base.write_text("".join(rows), encoding="utf-8")
        before = base.read_bytes()
        phys = results_io.reshard(base, max_bytes=len(rows[0]) * 5)
        self.assertGreater(len(phys), 1)
        self.assertEqual(b"".join(p.read_bytes() for p in phys), before)
        with self.assertRaises(FileExistsError):
            results_io.reshard(base)

    def test_missing_stream_reads_empty(self) -> None:
        missing = self.dir / "nope.jsonl"
        self.assertFalse(results_io.exists(missing))
        self.assertEqual(list(results_io.iter_lines(missing)), [])


class LoaderSemanticsTest(unittest.TestCase):
    """per_surface_bayesian_rollup._load_score_rows (shared by hattic_gate,
    v23_cross_lm_matrix and the other gates) must pick the same row from
    a sharded stream as from the single file it was split from."""

    def test_newest_by_ran_at_and_tie_order_survive_sharding(self) -> None:
        from scripts.per_surface_bayesian_rollup import _load_score_rows

        rows = [
            _row("h1", "2026-01-01T00:00:00Z", 1.0),
            _row("h2", "2026-01-01T00:00:00Z", 2.0),
            _row("h1", "2026-02-01T00:00:00Z", 3.0),  # newer: wins
            _row("h2", "2026-01-01T00:00:00Z", 4.0),  # tie: first-seen wins
            _row("h1", "2026-02-01T00:00:00Z", 5.0, lang="hattic"),
            _row("h3", "2026-03-01T00:00:00Z", 6.0),
        ]
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            single = Path(a) / "experiments.external_phoneme_perplexity_v0.under_hattic_lm.jsonl"
            single.write_text("".join(rows), encoding="utf-8")
            sharded = Path(b) / single.name
            with results_io.ShardedAppender(sharded, max_bytes=len(rows[0]) + 1) as fh:
                for r in rows:
                    fh.write(r)
            self.assertGreater(len(results_io.physical_paths(sharded)), 3)
            got_single = _load_score_rows(Path(a))
            got_sharded = _load_score_rows(Path(b))
        self.assertEqual(got_sharded, got_single)
        self.assertEqual(got_sharded[("h1", "basque")]["score"], 3.0)
        self.assertEqual(got_sharded[("h2", "basque")]["score"], 2.0)
        self.assertEqual(got_sharded[("h3", "basque")]["score"], 6.0)


if __name__ == "__main__":
    unittest.main()
