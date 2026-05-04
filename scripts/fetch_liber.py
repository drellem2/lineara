#!/usr/bin/env python3
"""Fetch Linear-B tablet pages from LiBER (Linear B Electronic Resources).

Source: https://liber.cnr.it (CNR / Università di Roma; CC BY-NC-SA 4.0,
academic use). LiBER's tablet ``view`` HTML embeds the Mycenaean-Greek
transliteration in the page's ``<meta name="description" ... />`` tag,
e.g.::

    <meta name="description" content="KN Da 1396, [ ku-ne-u / _ da-wo ..." />

so we cache the HTML on disk and let the parser pull the transliteration
out of that stable hook.

Polite throttled scraper. Re-runs are free (cache-hit).

Usage::

    python3 scripts/fetch_liber.py             # fetch the full index + every tablet
    python3 scripts/fetch_liber.py --limit 100 # smoke test
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "liber"
BASE = "https://liber.cnr.it"
USER_AGENT = (
    "lineara-research/0.1 (https://github.com/drellem2/lineara; "
    "academic Linear-A research / Linear-B positive-control corpus; "
    "contact via repo issues)"
)


def http_get(url: str, retries: int = 3, sleep: float = 0.4) -> bytes:
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(sleep * (attempt + 1))
    raise RuntimeError(f"GET {url} failed after {retries} retries: {last_err}")


def list_tablets(force: bool = False) -> list[dict]:
    """Return [{"id": int, "name": str}, ...] for all LiBER tablets."""
    idx_path = CACHE / "tablet_index.json"
    if idx_path.exists() and not force and idx_path.stat().st_size > 1000:
        return json.loads(idx_path.read_text(encoding="utf-8"))
    raw = http_get(f"{BASE}/database/api/tablet?query=*")
    rows = json.loads(raw.decode("utf-8"))
    rows.sort(key=lambda r: int(r["id"]))
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(json.dumps(rows, indent=0), encoding="utf-8")
    return rows


def cache_path(tablet_id: int) -> Path:
    return CACHE / "tablet" / f"{tablet_id}.html"


def fetch_one(tablet_id: int) -> tuple[int, bool]:
    p = cache_path(tablet_id)
    if p.exists() and p.stat().st_size > 1000:
        return tablet_id, True
    try:
        data = http_get(f"{BASE}/tablet/view/{tablet_id}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return tablet_id, True
    except Exception as e:  # noqa: BLE001
        print(f"  fetch failed for {tablet_id}: {e}", file=sys.stderr)
        return tablet_id, False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--sleep", type=float, default=0.05)
    ap.add_argument("--refresh-index", action="store_true")
    args = ap.parse_args(argv)

    CACHE.mkdir(parents=True, exist_ok=True)
    rows = list_tablets(force=args.refresh_index)
    print(f"discovered {len(rows)} tablets", file=sys.stderr)
    if args.limit:
        rows = rows[: args.limit]

    start = time.time()

    def task(r: dict) -> tuple[int, bool]:
        time.sleep(args.sleep)
        return fetch_one(int(r["id"]))

    n_ok = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, (_tablet_id, ok) in enumerate(pool.map(task, rows), 1):
            n_ok += int(ok)
            if i % 200 == 0:
                elapsed = time.time() - start
                rate = i / elapsed if elapsed else 0.0
                print(f"  {i}/{len(rows)} ({rate:.1f}/s)", file=sys.stderr)

    print(
        f"done: {n_ok}/{len(rows)} ok; cache at {CACHE}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
