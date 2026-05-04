#!/usr/bin/env python3
"""Parse cached SigLA HTML pages into per-inscription JSON records.

Reads .cache/sigla/<urlencoded-id>.{sign,word}.html and writes:
- corpus/<site>/<inscription-id>.json   (canonical, source of truth)
- corpus/all.jsonl                      (aggregate, deterministic rebuild)

Tokenization is documented in corpus_status.md; the rules are intentionally
simple so downstream experiments can re-run alternative rules over the cache.
"""

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "sigla"
CORPUS = ROOT / "corpus"
SCHEMA_PATH = ROOT / "schema" / "inscription.schema.json"

# Fixed timestamp keeps build deterministic; corpus_status.md records ingest date.
FETCHED_AT = "2026-05-04T00:00:00Z"

ROLE_TO_TOKEN_PREFIX = {
    "Syllabogram": "",
    "Transaction sign": "",  # treated as syllabogram-like; see corpus_status.md
    "Logogram": "LOG:",
    "Fraction": "FRAC:",
    "Erasure (Unknown?)": None,  # emitted as [?]
}

# Inscription kinds we know about; everything else falls through to "other".
KIND_TO_SUPPORT = {
    "Tablet": "tablet",
    "Sealing": "sealing",
    "Roundel": "roundel",
    "Bar": "bar",
    "Nodulus": "nodulus",
    "Noduli": "nodulus",
    "Disk": "disk",
    "Vase": "vase",
    "Stone": "stone",
    "Inscription": "inscription",
    "Cup": "vase",
    "Pithos": "vase",
    "Stirrup jar": "vase",
    "Hanging nodule": "nodule",
    "Flat-based nodule": "nodule",
    "Architectural": "architectural",
    "Libation table": "libation_table",
    "Loomweight": "loomweight",
    "Bowl": "vase",
    "Plaque": "plaque",
}


class SignViewParser(HTMLParser):
    """Pulls ordered (sign-id, role, parity, x, y, w, h) tuples from sign view.

    SigLA sign view structure: <a href="../../document/X/index-N.html"><rect class="sign syllabogram even|odd" x.. y.. width.. height../></a>
    followed later by popups <span class="popup ... " id="occ-N"><span class="info-title">#N: <a href="...reading-pattern:(SIGNID, ..."><span class="sure-reading">READ</span></a></span><span class="role">ROLE</span>...
    """

    def __init__(self) -> None:
        super().__init__()
        # rect_n -> dict(role, parity, coord)
        self.rects: dict[int, dict] = {}
        # occ_n -> sign_id, role
        self.popups: dict[int, dict] = {}
        # which occ-N rect we're inside (sign view nests each rect inside <a href=".../index-N.html">)
        self._inside_a_index: int | None = None
        self._next_rect_idx: int = 0
        self._inside_popup: int | None = None
        self._inside_role: bool = False
        self._inside_sure: bool = False
        self._inside_info_title: bool = False
        self._role_buf: list[str] = []
        self._sure_buf: list[str] = []
        self._title_buf: list[str] = []
        self.metadata: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            href = a.get("href", "")
            m = re.search(r"/index-(\d+)\.html$", href)
            if m:
                self._inside_a_index = int(m.group(1))
            # Capture metadata link targets.
            for kind in ("location", "kind", "period"):
                m2 = re.search(rf"\.\./\.\./{kind}/([^/]+)/?$", href)
                if m2:
                    val = urllib.parse.unquote(m2.group(1))
                    self.metadata.setdefault(kind, val)
        elif tag == "rect":
            cls = a.get("class", "")
            if "sign" in cls.split():
                role_class = None
                parity = None
                tokens = cls.split()
                # tokens like ["sign", "syllabogram", "even"] or ["sign", "logogram"]
                if len(tokens) >= 2:
                    role_class = tokens[1]
                if len(tokens) >= 3 and tokens[2] in ("even", "odd"):
                    parity = tokens[2]
                try:
                    coord = (
                        int(a.get("x", "0")),
                        int(a.get("y", "0")),
                        int(a.get("width", "0")),
                        int(a.get("height", "0")),
                    )
                except ValueError:
                    coord = (0, 0, 0, 0)
                idx = self._inside_a_index if self._inside_a_index is not None else self._next_rect_idx
                self._next_rect_idx += 1
                self.rects[idx] = {
                    "role_class": role_class,
                    "parity": parity,
                    "coord": coord,
                    "order": idx,
                }
        elif tag == "span":
            cls = a.get("class", "")
            sid = a.get("id", "")
            classes = cls.split()
            if "popup" in classes and sid.startswith("occ-"):
                try:
                    self._inside_popup = int(sid.split("-", 1)[1])
                    self.popups.setdefault(
                        self._inside_popup,
                        {"sign_id": None, "role": None, "sure_reading": None},
                    )
                except ValueError:
                    self._inside_popup = None
            elif self._inside_popup is not None and "role" in classes:
                self._inside_role = True
                self._role_buf = []
            elif self._inside_popup is not None and "sure-reading" in classes:
                self._inside_sure = True
                self._sure_buf = []
            elif self._inside_popup is not None and "info-title" in classes:
                self._inside_info_title = True
                self._title_buf = []

    def handle_endtag(self, tag):
        if tag == "a":
            if self._inside_a_index is not None:
                self._inside_a_index = None
        elif tag == "span":
            if self._inside_role:
                self._inside_role = False
                if self._inside_popup is not None:
                    self.popups[self._inside_popup]["role"] = "".join(self._role_buf).strip()
            elif self._inside_sure:
                self._inside_sure = False
                if self._inside_popup is not None:
                    self.popups[self._inside_popup]["sure_reading"] = "".join(self._sure_buf).strip()
            elif self._inside_info_title:
                self._inside_info_title = False
            elif self._inside_popup is not None:
                # Closing the popup span itself only when class includes "popup"; we
                # cheat a little: detect close of a span when its info-title parsing is done.
                pass

    def handle_data(self, data):
        if self._inside_role:
            self._role_buf.append(data)
        if self._inside_sure:
            self._sure_buf.append(data)
        if self._inside_info_title:
            self._title_buf.append(data)


# SigLA pages have one popup per sign, marked id="occ-N". We carve the page
# into popup chunks and pull (sign_id, role, unreadable, unsure) out of each.
RE_POPUP_BLOCK = re.compile(
    r'id="occ-(\d+)"[^>]*>(.*?)(?=id="occ-\d+"|<footer)',
    re.S,
)
RE_UNREADABLE_MARK = re.compile(r">#\d+:\s*\[\?\]")
RE_READING_PATTERN = re.compile(r"reading-pattern:\(([A-Za-z0-9*]+),")
RE_ROLE_INNER = re.compile(r'class="role">([^<]+)')
RE_RECT = re.compile(
    r'href="\.\./\.\./document/[^"]*/index-(\d+)\.html"\s*>\s*<rect [^>]*class="sign\s+([a-z]+)(?:\s+(even|odd))?"[^>]*x="(\d+)"\s+y="(\d+)"\s+width="(\d+)"\s+height="(\d+)"',
    re.S,
)
RE_KIND = re.compile(r'href="\.\./\.\./kind/([^/]+)/?"')
RE_LOC = re.compile(r'href="\.\./\.\./location/([^/]+)/?"')
RE_PERIOD = re.compile(r'href="\.\./\.\./period/([^/]+)/?"')
RE_TITLE = re.compile(r"<title>([^<]+)</title>")
RE_DIMS = re.compile(r"\(([\d.,]+\s*cm[^)]*)\)")
RE_CORPUS_LINK = re.compile(r'<a href="(https?://[^"]+)">Link to corpus</a>')

RE_WORD_GROUP = re.compile(
    r'<a class="(?:even|odd) word"[^>]*href="\.\./\.\./document/[^"]*/index-word-(\d+)\.html"[^>]*>(.*?)</a>',
    re.S,
)
RE_WORD_RECT = re.compile(
    r'<rect [^>]*x="(\d+)"\s+y="(\d+)"\s+width="(\d+)"\s+height="(\d+)"',
    re.S,
)


def parse_sign_view(html: str) -> dict:
    out: dict = {}
    out["kind"] = urllib.parse.unquote(RE_KIND.search(html).group(1)) if RE_KIND.search(html) else None
    out["location"] = (
        urllib.parse.unquote(RE_LOC.search(html).group(1)) if RE_LOC.search(html) else None
    )
    out["period"] = (
        urllib.parse.unquote(RE_PERIOD.search(html).group(1)) if RE_PERIOD.search(html) else None
    )
    title = RE_TITLE.search(html)
    out["title"] = title.group(1).strip() if title else None
    dims = RE_DIMS.search(html)
    out["dimensions"] = dims.group(1).strip() if dims else None
    cl = RE_CORPUS_LINK.search(html)
    out["corpus_link"] = cl.group(1) if cl else None

    # Build occ-N -> (sign_id, role, unreadable, unsure) map by carving popups.
    sign_id_by_occ: dict[int, str | None] = {}
    role_by_occ: dict[int, str] = {}
    unreadable_by_occ: dict[int, bool] = {}
    unsure_by_occ: dict[int, bool] = {}
    for m in RE_POPUP_BLOCK.finditer(html):
        n = int(m.group(1))
        body = m.group(2)
        unreadable = bool(RE_UNREADABLE_MARK.search(body))
        sm = RE_READING_PATTERN.search(body)
        rm = RE_ROLE_INNER.search(body)
        sign_id_by_occ[n] = sm.group(1) if sm else None
        role_by_occ[n] = rm.group(1).strip() if rm else None
        unreadable_by_occ[n] = unreadable
        unsure_by_occ[n] = ("unsure-reading" in body) and not unreadable

    # Build ordered list of rects in document order.
    rects: list[dict] = []
    for m in RE_RECT.finditer(html):
        idx = int(m.group(1))
        rects.append(
            {
                "occ": idx,
                "role_class": m.group(2),
                "parity": m.group(3),
                "x": int(m.group(4)),
                "y": int(m.group(5)),
                "w": int(m.group(6)),
                "h": int(m.group(7)),
                "sign_id": sign_id_by_occ.get(idx),
                "role": role_by_occ.get(idx),
                "unreadable": unreadable_by_occ.get(idx, False),
                "unsure": unsure_by_occ.get(idx, False),
            }
        )
    rects.sort(key=lambda r: r["occ"])
    out["rects"] = rects
    return out


def parse_word_view(html: str) -> list[list[tuple[int, int, int, int]]]:
    """Return list of words; each word is a list of (x, y, w, h) rect tuples."""
    words: list[list[tuple[int, int, int, int]]] = []
    for m in RE_WORD_GROUP.finditer(html):
        coords = []
        for r in RE_WORD_RECT.finditer(m.group(2)):
            coords.append((int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4))))
        words.append(coords)
    return words


def assign_words(rects: list[dict], words: list[list[tuple[int, int, int, int]]]) -> list[int | None]:
    """Map each rect (in occ order) to a word index, or None if standalone.

    Unreadable / erasure signs that fall *between* two signs in the same SigLA
    word group inherit that word, matching SigLA's seq-pattern semantics
    (where unreadable in-word signs don't break the word).
    """
    coord_to_word: dict[tuple[int, int, int, int], int] = {}
    for wi, coords in enumerate(words):
        for c in coords:
            coord_to_word[c] = wi
    out: list[int | None] = [coord_to_word.get((r["x"], r["y"], r["w"], r["h"])) for r in rects]

    # If a standalone sign sits between two signs that belong to the SAME word
    # (with no other word boundaries between them), pull it into that word.
    # SigLA's word view drops fractions / logograms / erasures from seq-patterns
    # but visually keeps them inside the word region; this re-creates that.
    n = len(out)
    for i in range(n):
        if out[i] is not None:
            continue
        prev_w = next((out[j] for j in range(i - 1, -1, -1) if out[j] is not None), None)
        next_w = next((out[j] for j in range(i + 1, n) if out[j] is not None), None)
        if prev_w is not None and prev_w == next_w:
            out[i] = prev_w
    return out


def token_for(rect: dict) -> str:
    sid = rect["sign_id"]
    role = (rect["role"] or "").strip()
    if rect.get("unreadable") or sid is None:
        return "[?]"
    if rect.get("unsure"):
        return f"[?:{sid}]"
    if role.startswith("Erasure"):
        # SigLA distinguishes Erasure (Fraction|Logogram|Unknown|Unknown?);
        # for v1 we collapse all to [?] — the underlying sign is rubbed out.
        return "[?]"
    # SigLA marks role-uncertain entries with a trailing "?". The sign-id is
    # still known, so we fold them into the same prefix as the certain role.
    role_clean = role.rstrip("?").strip()
    if role_clean == "Logogram":
        return f"LOG:{sid}"
    if role_clean == "Fraction":
        return f"FRAC:{sid}"
    if role_clean == "Transaction sign":
        return sid
    if role_clean in ("Syllabogram", "", None):
        return sid
    return sid  # unknown role -> emit bare sign-id; harness can re-tag


def build_tokens(rects: list[dict], words: list[list[tuple[int, int, int, int]]]) -> tuple[list[str], list[str]]:
    """Return (tokens, raw_word_patterns_for_transliteration)."""
    word_idx = assign_words(rects, words)
    tokens: list[str] = []
    last_group: object = "INIT"
    for r, wi in zip(rects, word_idx):
        # Group key: a word index if part of a word, else a unique standalone marker.
        if wi is not None:
            group = ("W", wi)
        else:
            group = ("S", r["occ"])
        if last_group != "INIT" and group != last_group:
            tokens.append("DIV")
        tokens.append(token_for(r))
        last_group = group
    raw_words: list[str] = []
    seen_word_indices: set[int] = set()
    current: list[str] = []
    last_g: object = None
    for r, wi in zip(rects, word_idx):
        g = ("W", wi) if wi is not None else ("S", r["occ"])
        if last_g is not None and g != last_g:
            raw_words.append("-".join(current))
            current = []
        current.append(token_for(r))
        last_g = g
    if current:
        raw_words.append("-".join(current))
    return tokens, raw_words


def site_dir_name(location: str | None) -> str:
    if not location:
        return "_unknown"
    s = location.replace("/", "_").strip()
    return s


def support_for(kind: str | None) -> str:
    if not kind:
        return "unknown"
    return KIND_TO_SUPPORT.get(kind, kind.lower().replace(" ", "_"))


def genre_hint_for(kind: str | None, has_logogram: bool, has_fraction: bool, has_transaction: bool) -> str:
    """Heuristic from kind + sign-class evidence.

    Linear A is overwhelmingly accountancy on tablets/roundels/bars; sealings
    are administrative; vase/stone inscriptions are typically votive or
    dedicatory. We hint, never decide.
    """
    if not kind:
        return "unknown"
    k = kind.lower()
    if k in {"tablet", "roundel", "bar", "nodulus", "noduli"} or k.endswith("nodule"):
        return "accountancy"
    if k == "sealing":
        return "administrative"
    if k in {"libation table", "vase", "stone", "cup", "pithos", "bowl", "stirrup jar"}:
        return "votive_or_inscription"
    if has_logogram or has_fraction or has_transaction:
        return "accountancy"
    return "unknown"


def confidence_for(rects: list[dict]) -> str:
    if not rects:
        return "fragmentary"
    n = len(rects)
    n_damaged = sum(
        1
        for r in rects
        if (r["role"] or "").startswith("Erasure")
        or r.get("unreadable")
        or r.get("unsure")
    )
    if n_damaged == 0:
        return "clean"
    if n_damaged / n >= 0.30:
        return "fragmentary"
    return "partial"


def to_record(doc_id: str, sign_html: str, word_html: str | None) -> dict | None:
    parsed = parse_sign_view(sign_html)
    rects = parsed["rects"]
    words = parse_word_view(word_html) if word_html else []
    if not rects:
        # Drawing-only entries — SigLA tracks the inscription but has no
        # transcription. Emit a fragmentary record so the corpus pointer count
        # still matches SigLA, and downstream filters can drop them by n_signs=0.
        tokens, raw_words = [], []
    else:
        tokens, raw_words = build_tokens(rects, words)
    has_log = any((r["role"] or "") == "Logogram" for r in rects)
    has_frac = any((r["role"] or "") == "Fraction" for r in rects)
    has_txn = any((r["role"] or "") == "Transaction sign" for r in rects)
    rec = {
        "id": doc_id,
        "site": parsed["location"] or "Unknown",
        "support": support_for(parsed["kind"]),
        "kind_raw": parsed["kind"],
        "period": parsed["period"],
        "dimensions": parsed["dimensions"],
        "genre_hint": genre_hint_for(parsed["kind"], has_log, has_frac, has_txn),
        "transcription_confidence": confidence_for(rects),
        "n_signs": len(rects),
        "n_words": len(words),
        "tokens": tokens,
        "raw_transliteration": " / ".join(raw_words),
        "source": f"sigla:document/{urllib.parse.quote(doc_id, safe='')}/",
        "source_url": f"https://sigla.phis.me/document/{urllib.parse.quote(doc_id, safe='')}/",
        "corpus_link": parsed["corpus_link"],
        "fetched_at": FETCHED_AT,
    }
    return rec


def write_records(records: list[dict]) -> None:
    CORPUS.mkdir(parents=True, exist_ok=True)
    # Per-inscription files.
    written = 0
    for rec in records:
        site = site_dir_name(rec["site"])
        site_dir = CORPUS / site
        site_dir.mkdir(parents=True, exist_ok=True)
        # File name uses URL-encoded id to avoid OS-illegal characters.
        safe = urllib.parse.quote(rec["id"], safe="")
        path = site_dir / f"{safe}.json"
        path.write_text(json.dumps(rec, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
        written += 1
    # Aggregate JSONL — sorted by id so the build is deterministic.
    sorted_recs = sorted(records, key=lambda r: r["id"])
    with (CORPUS / "all.jsonl").open("w", encoding="utf-8") as f:
        for r in sorted_recs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"wrote {written} per-inscription files + corpus/all.jsonl", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    manifest_path = CACHE / "manifest.json"
    if not manifest_path.exists():
        print("no manifest; run scripts/fetch_sigla.py first", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text())
    doc_ids = sorted(manifest.keys())
    if args.limit:
        doc_ids = doc_ids[: args.limit]

    records: list[dict] = []
    skipped: list[tuple[str, str]] = []
    for d in doc_ids:
        sign_path = CACHE / f"{urllib.parse.quote(d, safe='')}.sign.html"
        word_path = CACHE / f"{urllib.parse.quote(d, safe='')}.word.html"
        if not sign_path.exists():
            skipped.append((d, "no sign view cached"))
            continue
        try:
            sign_html = sign_path.read_text(encoding="utf-8", errors="replace")
            word_html = word_path.read_text(encoding="utf-8", errors="replace") if word_path.exists() else None
            rec = to_record(d, sign_html, word_html)
            if rec is None:
                skipped.append((d, "no signs parsed"))
                continue
            if rec["n_signs"] == 0:
                skipped.append((d, "no transcription on SigLA (drawing-only)"))
            records.append(rec)
        except Exception as e:  # noqa: BLE001
            skipped.append((d, f"parse error: {e}"))

    write_records(records)
    skip_log = ROOT / "corpus" / "_skipped.json"
    skip_log.write_text(json.dumps(skipped, indent=2, ensure_ascii=False))
    print(f"records: {len(records)}; skipped: {len(skipped)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
