#!/usr/bin/env python3
"""Fetch a fixed-revision Basque text corpus from eu.wikipedia.org.

This script powers the Basque char-bigram phoneme prior used by
``external_phoneme_perplexity_v0`` (mg-ee18). Determinism comes from the
``corpora/basque.fetch_manifest.txt`` file, which pins each article to a
specific revision id (``oldid``). Wikipedia article revisions are
immutable, so a re-run against the same manifest fetches identical
content.

Two modes:

* **default** — read the committed manifest and fetch each pinned
  revision. Writes the cleaned text to ``corpora/basque/text.txt``.
  This is what re-runs do.
* ``--resolve-revids`` — for each title in the BUILT-IN slug list below,
  query the API for the *current* latest revision id and write
  ``(oldid, title)`` rows to the manifest. Used once at corpus authoring
  time; commit the resulting manifest. Re-running this mode bumps the
  pins to whatever is current — the operator decides when to do so.

Normalization:

* Lowercase.
* Fold ``ñ`` → ``n``, ``ü`` → ``u``, ``ç`` → ``s`` (rare loanword
  letters; folding keeps the alphabet at 26 chars per the mg-ee18 brief).
* Strip everything outside ``[a-z]`` and whitespace.
* Collapse whitespace runs to a single space.

The output is one long lowercase string of Basque text, deterministic
under the manifest. Modern Basque orthography is largely phonemic
(Trask 1997 ch. 1 §1.4), so the cleaned text doubles as a phoneme stream
for char-bigram modeling.

License + provenance documented in ``corpora/basque.README.md``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_MANIFEST = _REPO_ROOT / "corpora" / "basque.fetch_manifest.txt"
_DEFAULT_OUT = _REPO_ROOT / "corpora" / "basque" / "text.txt"
_API_URL = "https://eu.wikipedia.org/w/api.php"
_USER_AGENT = (
    "lineara-research/0.1 (mg-ee18 Basque corpus fetch; "
    "https://github.com/drellem2/lineara)"
)
# Rate-limit between API calls to stay polite (Wikipedia recommends < 100 RPS
# for unauthenticated extracts; we use a much smaller cadence).
_REQUEST_INTERVAL_S = 0.25
# Folding map for non-26-letter Basque/loanword characters. Applied after
# lowercasing.
_FOLDING = {"ñ": "n", "ü": "u", "ç": "s"}
_KEEP_RE = re.compile(r"[^a-z\s]+")
_WS_RE = re.compile(r"\s+")


# Hand-curated slug list spanning topical breadth (geography, history,
# linguistics, science, biology, culture, sports, economy). The exact
# list is what makes the corpus reproducible end-to-end: re-running
# ``--resolve-revids`` writes the current revid for each title in this
# list, and commits a manifest that pins each one. The list itself is
# committed inline here so the manifest can be reconstructed from
# scratch (modulo Wikipedia content drift) if needed.
SLUGS: tuple[str, ...] = (
    # Language and people
    "Euskara", "Euskal Herria", "Euskaldun", "Euskal alfabetoa",
    "Euskararen historia", "Euskal kultura", "Euskaltzaindia",
    "Euskara batua", "Euskalkiak", "Bizkaiera", "Gipuzkera", "Lapurtera",
    "Zuberera", "Aitzineuskara",
    # Geography (Basque Country provinces and cities)
    "Bizkaia", "Gipuzkoa", "Araba", "Nafarroa Garaia", "Lapurdi",
    "Nafarroa Beherea", "Zuberoa",
    "Bilbo", "Donostia", "Iruñea", "Gasteiz", "Baiona", "Maule",
    "Tolosa", "Eibar", "Errenteria", "Irun", "Zarautz", "Bermeo",
    # Geography (broader)
    "Pirinioak", "Bizkaiko Golkoa", "Iberiar penintsula", "Europa",
    "Asia", "Afrika", "Amerika", "Ozeania", "Mediterraneo itsasoa",
    "Atlantiko ozeanoa", "Lurra", "Eguzkia", "Ilargia",
    "Espainia", "Frantzia", "Italia", "Portugal", "Alemania",
    "Erresuma Batua", "Estatu Batuak", "Japonia", "Txina", "India",
    # History
    "Erdi Aroa", "Antzinaroa", "Aro Modernoa", "Erromatar Inperioa",
    "Nafarroako Erresuma", "Frankismoa",
    "Lehenengo Mundu Gerra", "Bigarren Mundu Gerra",
    "Gernikako bonbardaketa", "Karlistadak",
    # Science and nature
    "Fisika", "Matematika", "Biologia", "Kimika", "Astronomia",
    "Geologia", "Geografia", "Historia", "Filosofia", "Psikologia",
    "Soziologia", "Ekonomia", "Politika",
    "Ura", "Sua", "Airea", "Erregaia", "Argia", "Energia",
    "Animalia", "Landare", "Zuhaitza", "Lorea", "Hartza", "Otsoa",
    "Txakurra", "Katua", "Behia", "Zaldia", "Arraina", "Hegaztia",
    # Culture, arts, sports
    "Literatura", "Musika", "Antzerkia", "Pintura", "Eskultura",
    "Arkitektura", "Sinema", "Bertsolaritza",
    "Futbola", "Saskibaloia", "Txirrindularitza", "Pilota",
    "Athletic Club", "Real Sociedad",
    # Notable people
    "Sabino Arana", "Resurreccion Maria Azkue", "Jose Miguel Barandiaran",
    "Bernardo Atxaga", "Koldo Mitxelena", "Joan Mari Lekuona",
    # Concepts
    "Etxea", "Hiria", "Mendia", "Ibaia", "Itsasoa", "Basoa",
    "Eskola", "Unibertsitatea", "Liburua", "Hizkuntza",
)


def _http_get_json(params: dict) -> dict:
    """Make a GET request to the Wikipedia API with our user-agent."""
    qs = urllib.parse.urlencode(params)
    url = f"{_API_URL}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def resolve_revids(slugs: tuple[str, ...]) -> list[tuple[int, str]]:
    """Look up the current latest revid for each title.

    Wikipedia's ``titles=`` parameter accepts up to 50 titles per query, so
    we batch. Returns a list of ``(revid, title)`` pairs in the same
    topical order as ``slugs`` (sorted by manifest convention afterwards).
    """
    out: list[tuple[int, str]] = []
    batch_size = 30
    for i in range(0, len(slugs), batch_size):
        batch = slugs[i : i + batch_size]
        # ``prop=info`` returns ``lastrevid`` for every page in the
        # query in a single batched call (``rvlimit`` is incompatible
        # with multi-title queries — see the MW API docs).
        params = {
            "action": "query",
            "format": "json",
            "prop": "info",
            "titles": "|".join(batch),
            "redirects": "1",
        }
        data = _http_get_json(params)
        title_to_revid: dict[str, int] = {}
        pages = (data.get("query") or {}).get("pages") or {}
        for page in pages.values():
            if "missing" in page:
                continue
            revid = page.get("lastrevid")
            if revid:
                title_to_revid[page["title"]] = int(revid)
        # Honor the redirect map so the slug list can use ergonomic
        # names ("Pilota") even when the canonical title differs
        # ("Pilota joko").
        redirects = (data.get("query") or {}).get("redirects") or []
        rewrites = {r["from"]: r["to"] for r in redirects}
        for slug in batch:
            resolved = rewrites.get(slug, slug)
            revid = title_to_revid.get(resolved)
            if revid is None:
                print(
                    f"  warn: no revid for {slug!r} (resolved={resolved!r})",
                    file=sys.stderr,
                )
                continue
            out.append((revid, resolved))
        time.sleep(_REQUEST_INTERVAL_S)
    return out


def fetch_extract(revid: int) -> str:
    """Fetch the plain-text extract for a specific revision id."""
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "revids": str(revid),
        "explaintext": "1",
        "exsectionformat": "plain",
    }
    data = _http_get_json(params)
    pages = (data.get("query") or {}).get("pages") or {}
    for page in pages.values():
        return str(page.get("extract") or "")
    return ""


def normalize(text: str) -> str:
    """Lowercase, fold non-26-letter chars, strip non-letters, collapse ws."""
    s = text.lower()
    for ch, repl in _FOLDING.items():
        s = s.replace(ch, repl)
    s = _KEEP_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def write_manifest(path: Path, entries: list[tuple[int, str]]) -> None:
    """Write the manifest in deterministic sorted order: by revid asc."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{revid}\t{title}\n" for revid, title in sorted(entries)]
    path.write_text("".join(lines), encoding="utf-8")


def read_manifest(path: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        revid_s, _, title = line.partition("\t")
        out.append((int(revid_s), title))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--manifest",
        type=Path,
        default=_DEFAULT_MANIFEST,
        help="Path to the (revid, title) manifest. Default: %(default)s.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=_DEFAULT_OUT,
        help="Path for the cleaned corpus text. Default: %(default)s.",
    )
    parser.add_argument(
        "--resolve-revids",
        action="store_true",
        help="Look up the current latest revision id for each built-in slug "
        "and rewrite the manifest. Use sparingly — re-running pins to whatever "
        "is current today.",
    )
    args = parser.parse_args(argv)

    if args.resolve_revids:
        print(
            f"resolving current revids for {len(SLUGS)} built-in slugs...",
            file=sys.stderr,
        )
        entries = resolve_revids(SLUGS)
        write_manifest(args.manifest, entries)
        print(
            f"wrote {len(entries)} entries to {args.manifest}", file=sys.stderr
        )
        return 0

    if not args.manifest.exists():
        print(
            f"manifest not found: {args.manifest}\n"
            f"first-time setup: run with --resolve-revids to populate it, "
            f"then commit the manifest.",
            file=sys.stderr,
        )
        return 2

    entries = read_manifest(args.manifest)
    print(
        f"manifest: {len(entries)} pinned revisions; fetching extracts...",
        file=sys.stderr,
    )

    parts: list[str] = []
    for i, (revid, title) in enumerate(entries, 1):
        try:
            raw = fetch_extract(revid)
        except Exception as exc:
            print(
                f"  warn: fetch failed for revid {revid} ({title!r}): {exc}",
                file=sys.stderr,
            )
            continue
        cleaned = normalize(raw)
        if cleaned:
            parts.append(cleaned)
        if i % 20 == 0:
            print(
                f"  {i}/{len(entries)} fetched  "
                f"(cumulative chars after norm: {sum(len(p) for p in parts):,})",
                file=sys.stderr,
            )
        time.sleep(_REQUEST_INTERVAL_S)

    text = " ".join(parts)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text + "\n", encoding="utf-8")
    print(
        f"wrote {len(text):,} chars to {args.out}", file=sys.stderr
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
