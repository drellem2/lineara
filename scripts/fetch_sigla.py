#!/usr/bin/env python3
"""Fetch SigLA HTML pages (sign view + word view) for every inscription.

Polite throttled scraper that caches every response to disk so re-runs are free.
SigLA dataset & drawings are CC BY-NC-SA 4.0 (https://sigla.phis.me/about.html).
We hit only the public HTML the site already serves to browsers.

Usage: python3 fetch_sigla.py [--limit N] [--workers K]

Outputs land in <repo>/.cache/sigla/<urlencoded-id>.{sign,word}.html and a
manifest at <repo>/.cache/sigla/manifest.json listing the inscription IDs we
were able to reach.
"""

import argparse
import concurrent.futures
import html as html_lib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "sigla"
BASE = "https://sigla.phis.me"
USER_AGENT = (
    "lineara-research/0.1 (https://github.com/drellem2/lineara; "
    "academic Linear A research; contact via repo issues)"
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


def cache_path(doc_id: str, view: str) -> Path:
    safe = urllib.parse.quote(doc_id, safe="")
    return CACHE / f"{safe}.{view}.html"


def fetch_doc(doc_id: str) -> tuple[str, bool, bool]:
    """Fetch sign and word views for one inscription, caching to disk.

    Returns (doc_id, sign_ok, word_ok). Word view may legitimately 404 for
    inscriptions with zero words (rare).
    """
    enc = urllib.parse.quote(doc_id, safe="")
    sign_url = f"{BASE}/document/{enc}/"
    word_url = f"{BASE}/document/{enc}/index-word.html"

    sign_path = cache_path(doc_id, "sign")
    word_path = cache_path(doc_id, "word")

    sign_ok = sign_path.exists() and sign_path.stat().st_size > 1000
    word_ok = word_path.exists() and word_path.stat().st_size > 500

    if not sign_ok:
        try:
            sign_path.write_bytes(http_get(sign_url))
            sign_ok = True
        except Exception as e:  # noqa: BLE001
            print(f"  sign fetch failed for {doc_id}: {e}", file=sys.stderr)

    if not word_ok:
        try:
            word_path.write_bytes(http_get(word_url))
            word_ok = True
        except Exception as e:  # noqa: BLE001
            # Word view is allowed to be missing.
            word_ok = False

    return doc_id, sign_ok, word_ok


def list_documents() -> list[str]:
    browse_path = CACHE / "browse.html"
    if not browse_path.exists() or browse_path.stat().st_size < 100000:
        browse_path.write_bytes(http_get(f"{BASE}/browse.html"))
    html = browse_path.read_text(encoding="utf-8", errors="replace")
    raw_ids = re.findall(r'href="document/([^"/]+)/"', html)
    seen, unique = set(), []
    for d in raw_ids:
        # Some IDs contain literal angle brackets that browse.html encodes as
        # &lt;/&gt;. Decode before URL-encoding so the server resolves them.
        d = html_lib.unescape(d)
        if d not in seen:
            seen.add(d)
            unique.append(d)
    return unique


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="fetch only first N (0 = all)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--sleep", type=float, default=0.15, help="per-request throttle")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    docs = list_documents()
    print(f"discovered {len(docs)} documents on browse.html", file=sys.stderr)
    if args.limit:
        docs = docs[: args.limit]

    manifest: dict[str, dict] = {}
    start = time.time()

    def task(d: str) -> tuple[str, bool, bool]:
        time.sleep(args.sleep)
        return fetch_doc(d)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, (doc_id, sign_ok, word_ok) in enumerate(pool.map(task, docs), 1):
            manifest[doc_id] = {"sign_ok": sign_ok, "word_ok": word_ok}
            if i % 50 == 0:
                elapsed = time.time() - start
                rate = i / elapsed if elapsed else 0
                print(
                    f"  {i}/{len(docs)} fetched ({rate:.1f}/s)",
                    file=sys.stderr,
                )

    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    n_sign = sum(1 for v in manifest.values() if v["sign_ok"])
    n_word = sum(1 for v in manifest.values() if v["word_ok"])
    print(f"done: {n_sign}/{len(manifest)} sign views, {n_word}/{len(manifest)} word views", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
