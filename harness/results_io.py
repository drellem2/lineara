"""Sharded, append-only result streams (mg-1c82a).

GitHub refuses any pushed blob over 100 MB, and the ``results/*.jsonl``
streams only ever grow. A *logical* stream ``results/<name>.jsonl`` is
therefore stored as the base file plus zero or more continuation
shards::

    results/<name>.jsonl                 rows 1..k   (shard 0)
    results/<name>.shards/0001.jsonl     rows k+1..m
    results/<name>.shards/0002.jsonl     ...

Concatenating the physical files in :func:`physical_paths` order gives
the logical stream byte-for-byte, so every loader that keeps
"newest-by-``ran_at``, first-seen wins on ties" semantics produces the
same output as it did against the single file. Rows are never split
across shards and never rewritten; :class:`ShardedAppender` only ever
appends to the last shard and starts a new one once the last shard
would pass :data:`SHARD_MAX_BYTES`.

The shard directory deliberately does not end in ``.jsonl``, so the
existing ``results_dir.glob("experiments.<metric>.*.jsonl")`` tag
globs never match it: tagged sidecars and shards stay separate.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterator

# Roll to a new shard before any shard passes this. Well under GitHub's
# 100 MB hard cap and its 50 MB warning; harness/tests/test_results_size
# asserts every committed results file is under 50 MB.
SHARD_MAX_BYTES = 40 * 1024 * 1024


def shard_dir(path: Path) -> Path:
    """``results/<name>.jsonl`` → ``results/<name>.shards``."""
    path = Path(path)
    return path.with_name(path.stem + ".shards")


def physical_paths(path: Path) -> list[Path]:
    """The physical files holding the logical stream ``path``, in stream
    order: the base file (if it exists) then its shards by number.
    Returns ``[]`` when neither exists."""
    path = Path(path)
    out = [path] if path.exists() else []
    d = shard_dir(path)
    if d.is_dir():
        out.extend(sorted(d.glob("[0-9][0-9][0-9][0-9].jsonl")))
    return out


def metric_stream_paths(results_dir: Path, metric: str) -> list[Path]:
    """The logical streams that may carry rows for ``metric``, in the
    order loaders have always read them: the primary
    ``experiments.jsonl``, the per-metric sidecar
    ``experiments.<metric>.jsonl``, then every tagged sidecar
    ``experiments.<metric>.<tag>.jsonl`` sorted by name. Expand each
    with :func:`iter_lines` / :func:`physical_paths`."""
    results_dir = Path(results_dir)
    paths = [
        results_dir / "experiments.jsonl",
        results_dir / f"experiments.{metric}.jsonl",
    ]
    paths.extend(sorted(results_dir.glob(f"experiments.{metric}.*.jsonl")))
    return paths


def exists(path: Path) -> bool:
    """True if the logical stream ``path`` has any physical file."""
    return bool(physical_paths(path))


def iter_lines(path: Path) -> Iterator[str]:
    """Every line of the logical stream ``path``, in stream order (raw,
    newline included — callers strip/skip blanks as they always have)."""
    for p in physical_paths(path):
        with p.open("r", encoding="utf-8") as fh:
            yield from fh


class ShardedAppender:
    """Append-only writer for a logical stream. Mirrors the subset of the
    file API the writers use (``write``/``flush``/``close``, context
    manager). Each ``write`` must be whole rows (``...\\n``) so a row is
    never split across shards."""

    def __init__(self, path: Path, max_bytes: int = SHARD_MAX_BYTES):
        self.path = Path(path)
        self.max_bytes = max_bytes
        phys = physical_paths(self.path)
        self._cur = phys[-1] if phys else self.path
        self._cur.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self._cur.open("a", encoding="utf-8")
        self._size = self._cur.stat().st_size

    @property
    def current_path(self) -> Path:
        return self._cur

    def _roll(self) -> None:
        self._fh.close()
        d = shard_dir(self.path)
        d.mkdir(parents=True, exist_ok=True)
        existing = sorted(d.glob("[0-9][0-9][0-9][0-9].jsonl"))
        n = int(existing[-1].stem) + 1 if existing else 1
        self._cur = d / f"{n:04d}.jsonl"
        self._fh = self._cur.open("a", encoding="utf-8")
        self._size = self._cur.stat().st_size

    def write(self, s: str) -> int:
        n = len(s.encode("utf-8"))
        if self._size > 0 and self._size + n > self.max_bytes:
            self._roll()
        self._size += n
        return self._fh.write(s)

    def flush(self) -> None:
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()

    @property
    def closed(self) -> bool:
        return self._fh.closed

    def __enter__(self) -> "ShardedAppender":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def reshard(path: Path, max_bytes: int = SHARD_MAX_BYTES) -> list[Path]:
    """Split an existing over-sized single-file stream into base + shards
    without changing its logical content (rows kept whole and in order).
    Refuses if ``path`` already has shards. Returns the physical paths."""
    path = Path(path)
    if shard_dir(path).exists():
        raise FileExistsError(f"{shard_dir(path)} already exists")
    if path.stat().st_size <= max_bytes:
        return [path]
    tmp = path.with_name(path.name + ".reshard-tmp")
    path.rename(tmp)
    try:
        app = ShardedAppender(path, max_bytes=max_bytes)
        with tmp.open("r", encoding="utf-8", newline="") as src, app:
            for line in src:
                app.write(line)
    except BaseException:
        shutil.rmtree(shard_dir(path), ignore_errors=True)
        tmp.rename(path)
        raise
    tmp.unlink()
    return physical_paths(path)
