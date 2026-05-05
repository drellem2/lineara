#!/usr/bin/env python3
"""Build the Cretan Hieroglyphic (CHIC) inscription corpus (mg-99df, chic-v0).

CHIC = Olivier & Godart 1996, *Corpus Hieroglyphicarum Inscriptionum Cretae*
(Études Crétoises 31). The print catalogue numbers ~331 inscriptions; we
ingest from John Younger's web edition of CHIC, which retransnumerates
each entry sign-by-sign and adds post-CHIC additions (Petras, recent
finds). Younger's site (people.ku.edu/~jyounger/Hiero/) is offline; we
fetch from the Internet Archive Wayback Machine snapshot of 2022-07-03,
which is the last complete capture before the personal-page subdomain
was retired.

Output structure (mirrors corpora/eteocretan/, corpora/linear_b/):
  corpora/cretan_hieroglyphic/inscriptions/<id>.json   per-inscription
  corpora/cretan_hieroglyphic/all.jsonl                  aggregate
  corpus_status.chic.md                                  coverage stats

Per-inscription JSON (CHIC v0 schema; matches the ticket spec):
  {
    "id": "CHIC #001",
    "site": "Knossos" | "Mallia" | ...,
    "support": "crescent" | "bar" | "tablet" | "medallion" | "cone" | ...,
    "period": null | "MM IA-IB" | "MM II-III" | ...,
    "transcription_confidence": "clean" | "partial" | "fragmentary",
    "tokens": ["#011", "DIV", "#036", ...],
    "raw_transliteration": "<verbatim transnumeration string from Younger>",
    "source": "younger_online",
    "source_citation": "<Wayback Machine URL>",
    "fetched_at": "2026-05-05T11:00:00Z"
  }

Tokenization rules (CHIC v0; see corpus_status.chic.md for the full
spec, kept rules-as-data for re-tokenization in chic-v1):

  Source (Younger transnumeration)   → token form
  ---------------------------------    ---------------------
  bare three-digit `NNN`            → `#NNN` (zero-padded, preserves
                                       CHIC catalog convention #001-#100
                                       syllabographic, #101+ logo/ideo,
                                       #301-#308 fractions; classification
                                       deferred to chic-v1)
  underlined `<u>NNN</u>`           → `[?:#NNN]` (Younger uses underline
                                       to mark a doubtful reading of an
                                       otherwise-attested sign)
  asterisked `*NNN`                 → `#NNN` (asterisk-prefix is
                                       Younger's notation for "logogram
                                       form *NNN"; same sign id, kept as
                                       `#NNN` for v0; chic-v1 will mark
                                       logogram class)
  damage marker `]NNN`/`[NNN`/`>?`  → `[?:#NNN]` if id known, else `[?]`
  bold count `<b>N...N</b>`         → `NUM:N` (numeric quantity; kept
                                       only when distinguishable from
                                       a sign id by the absence of a
                                       leading hyphen / sign group)
  literal `X` orientation marker    → skipped (decorative cross /
                                       writing-axis indicator, not a
                                       syllabogram in CHIC)
  word divider (whitespace between
    sign-groups in a side row,
    or between sides)               → `DIV`
  empty `vacat` row                 → no tokens, no DIV
  Ideogram name (e.g., BOS, VAS)    → not emitted as text; the same
                                       sign carries a numeric id in the
                                       transnumeration column, which we
                                       capture instead. IDEO:<name>
                                       extraction deferred to chic-v1.

Reproducibility: idempotent; deterministic byte-identical output given
the same cached HTML; safe to re-run.

Usage:
  python3 scripts/build_chic_corpus.py            # build from cache
  python3 scripts/build_chic_corpus.py --fetch    # also (re-)download
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "younger_chic"
OUT_DIR = ROOT / "corpora" / "cretan_hieroglyphic"
INSCRIPTIONS_DIR = OUT_DIR / "inscriptions"
ALL_JSONL = OUT_DIR / "all.jsonl"
STATUS_PATH = ROOT / "corpus_status.chic.md"

# Wayback snapshot id; fixed to make the build deterministic. The 2022-07-03
# snapshot is the last full capture of Younger's CHIC pages before the
# personal-page subdomain was retired.
WAYBACK_SNAPSHOT = "20220703170656"
SOURCE_BASE = "http://www.people.ku.edu/~jyounger/Hiero"
WAYBACK_URL_FMT = "http://web.archive.org/web/{snap}/{src}/{name}"

# Page → (filename, default site). The default site is the *file's* primary
# site assignment; we override per-entry with the site code parsed from the
# heading line (since misc/seals files mix sites).
PAGES: list[tuple[str, str]] = [
    ("KNtexts.html", "knossos"),
    ("MAtexts.html", "mallia"),
    ("PEtexts.html", "petras"),
    ("misctexts.html", "misc"),
    ("SealsImps.html", "seals_imps"),
]

USER_AGENT = (
    "lineara/0.1 (chic-v0 corpus build; https://github.com/drellem2/lineara)"
)
THROTTLE_SECONDS = 1.0
FETCHED_AT = "2026-05-05T11:00:00Z"  # fixed for determinism

# Site code (from CHIC catalog conventions) → human-readable site name.
# Two-letter prefixes appear at the start of the heading line after the
# CHIC #; the "/" suffix denotes a sub-area (e.g., MA/M = Mallia,
# Quartier Mu).
SITE_CODES: dict[str, str] = {
    "KN": "Knossos",
    "MA": "Mallia",
    "KH": "Khania",
    "PH": "Phaistos",
    "PE": "Petras",
    "AR": "Arkhanes",
    "MO": "Mochlos",
    "TY": "Tylissos",
    "ZA": "Zakros",
    "GO": "Gournia",
    "MY": "Myrtos-Pyrgos",
    "PA": "Palaikastro",
    "PK": "Palaikastro",
    "PS": "Psychro",
    "PY": "Pyrgos (Myrtos)",
    "VA": "Vrysinas",
    "SY": "Symi",
    "MI": "Mochlos",
    "QU": "Quartier Mu (Mallia)",
    "SK": "Skoteino",
    "SI": "Sitia",
    "CR": "Crete (unprovenanced)",
    "AB": "Abydos (Egypt, exported seal)",
    "SA": "Samothrace (exported seal)",
    "PL": "Platanos",
    "LA": "Lasithi",
    "HT": "Haghia Triada",
    "KA": "Kalo Horio",
    "ZI": "Ziros",
    "AV": "Avdou",
    "LI": "Lithines",
    "PR": "Praisos",
    "KR": "Kritsa",
    "IR": "Heraklion",
    "KO": "Kordakia",
    "KY": "Kydonia",
    "PI": "Pinakiano",
    "AD": "Adromili",
    "XI": "Xida",
    "NE": "Neapolis",
}

# Support type vocabulary; matches against the heading text after the
# museum reference, using a longest-match-first scan.
SUPPORT_KEYWORDS: list[tuple[str, str]] = [
    ("crescent", "crescent"),
    ("nodulus", "nodulus"),
    ("noduli", "nodulus"),
    ("medallion", "medallion"),
    ("medaillon", "medallion"),
    ("roundel", "roundel"),
    ("tablet", "tablet"),
    ("4-sided bar", "bar"),
    ("4 sided bar", "bar"),
    ("barre", "bar"),
    ("bar", "bar"),
    ("cone", "cone"),
    ("chamaizi vase", "chamaizi_vase"),
    ("vase", "vase"),
    ("offering table", "offering_table"),
    ("libation table", "libation_table"),
    ("libation", "libation_table"),
    ("seal impression", "sealing"),
    ("imp cres", "sealing"),
    ("imp dir-obj", "sealing"),
    ("imp don", "sealing"),
    ("imp roun", "sealing"),
    ("nodule", "sealing"),
    ("sealing", "sealing"),
    ("sealstone", "seal"),
    ("3epr", "seal"),  # CMS seal shape codes (3-sided prism, 4-prism, etc.)
    ("4ep ", "seal"),
    ("4epr", "seal"),
    ("4pr ", "seal"),
    ("3pr ", "seal"),
    ("8pr", "seal"),
    ("amyg", "seal"),  # amygdaloid sealstone
    ("prism", "seal"),
    ("petsch", "seal"),  # petschaft (signet seal)
    ("signet", "seal"),
    ("scarab", "seal"),
    ("agate", "seal"),
    ("jasper", "seal"),
    ("carnelian", "seal"),
    ("cornelian", "seal"),
    ("chalcedony", "seal"),
    ("sardonyx", "seal"),
    ("steatite", "seal"),
    ("hematite", "seal"),
    ("serpentine", "seal"),
    ("bone", "seal"),  # bone seal
    ("ivory", "seal"),
    ("rock crystal", "seal"),
    ("seal", "seal"),
    ("axe", "stone_axe"),
    ("amphora handle", "potsherd"),
    ("amphora", "potsherd"),
    ("sherd", "potsherd"),
    ("ostracon", "potsherd"),
    ("pithos cover", "pithos"),
    ("pithos", "pithos"),
    ("pithoid", "pithos"),
    ("stone block", "stone_inscription"),
    ("stone", "stone_inscription"),
    ("ring", "metal_ring"),
    ("bronze", "bronze"),
    ("copper", "bronze"),
    ("clay", "clay_document"),
    ("inscription", "stone_inscription"),
    ("plaque", "plaque"),
    ("lame", "lame"),  # CHIC Hf = lame (flat 4-sided strip-tablet)
    ("hi ", "tablet"),  # MA Hi = tablet class
]


# ---------------------------------------------------------------------------
# Fetch (one-time, cached)
# ---------------------------------------------------------------------------


def wayback_url(filename: str) -> str:
    return WAYBACK_URL_FMT.format(
        snap=WAYBACK_SNAPSHOT, src=SOURCE_BASE, name=filename
    )


def fetch_pages(force: bool = False) -> None:
    """Download the five Younger CHIC index pages from Wayback Machine.

    Idempotent: skips files already present unless `force` is set.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    for filename, _site in PAGES:
        path = CACHE / filename
        if path.exists() and path.stat().st_size > 1000 and not force:
            continue
        url = wayback_url(filename)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        path.write_bytes(data)
        time.sleep(THROTTLE_SECONDS)


# ---------------------------------------------------------------------------
# Parsing: split each cached HTML into per-CHIC-# entries
# ---------------------------------------------------------------------------

# Canonical entry heading patterns (Younger's web edition):
#
#   <p><br>\n<b>#NNN</b>.  KN Ha ...      (KN/MA clay docs — period after bold)
#   <p>\n<b>#NNN</b>.  KN Ha ...
#   <p>#<b>NNN</b>  KN Imp ...             (sealstones/impressions)
#   <p>#<b>NNN</b>  MA/M (...) Yb 01 ...  (misc additions)
#
# A canonical entry starts at a paragraph boundary (preceded by `<p>`,
# `<br>`, `<center>`, or BOF) and is followed within a few characters by
# a 2-letter site code. Commentary cross-references like
# `(#<b>123</b>)` or `cf. #<b>225</b>` mid-sentence do NOT match.
_HEADING_RE = re.compile(
    r"""(?x)
    (?:^|<p\b[^>]*>|<br\b[^>]*>|</center>)\s*
    (?:<b>\#(\d{1,3})</b>\s*\.|\#<b>(\d{1,3})</b>(?!\d))
    \s*
    (?=[A-Z]{2})    # immediately followed by a 2-letter site code
    """,
)


def split_entries(text: str) -> list[tuple[int, str]]:
    """Return [(chic_num, entry_html), ...] in document order.

    An entry runs from one canonical heading match up to the next
    canonical heading match. Entries whose body has no `transnumeration`
    table are dropped.
    """
    matches = list(_HEADING_RE.finditer(text))
    out: list[tuple[int, str]] = []
    for i, m in enumerate(matches):
        chic_num = int(m.group(1) or m.group(2))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        if "transnumeration" not in body.lower():
            continue
        out.append((chic_num, body))
    return out


# Heading line: skip any leading paragraph-boundary markers, then capture
# from the bold-CHIC-# through the first <br>/<p>/<table>.
_HEADING_LINE_RE = re.compile(
    r"^\s*(?:<p\b[^>]*>|<br\b[^>]*>|</center>)?\s*"
    r"(?:<b>#\d{1,3}</b>\s*\.|#<b>\d{1,3}</b>)"
    r"(.*?)(?=<br\b|<p\b|<table\b|$)",
    re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
# Site code: 2 uppercase letters, optionally followed by /letter (sub-area).
# Anchor to the first token of the heading to avoid matching CMS-volume
# Roman numerals that appear later in the line (`VI`, `II`, `IV`, etc.).
_SITE_CODE_RE = re.compile(r"^\s*([A-Z]{2})(?:/[A-Z])?\b")
# Full-word site name (CHIC sealstones often write out the village name in
# all caps, e.g. KALO HORIO, MOCHLOS, PRESOS). Longest match wins.
_FULL_NAME_TO_SITE: dict[str, str] = {
    "MOCHLOS": "Mochlos",
    "KALO HORIO": "Kalo Horio",
    "PRESOS": "Praisos",
    "PRAISOS": "Praisos",
    "SITIA": "Sitia",
    "ZIROS": "Ziros",
    "AVDOU": "Avdou",
    "LITHINES": "Lithines",
    "LASITHI": "Lasithi",
    "LAKONIA": "Lakonia",
    "MIRABELO": "Mirabelo",
    "MIRABELLO": "Mirabelo",
    "KASTELI": "Kasteli",
    "KORDAKIA": "Kordakia",
    "IRAKLIO": "Heraklion",
    "HERAKLION": "Heraklion",
    "KRITSA": "Kritsa",
    "ADROMILI": "Adromili",
    "PINAKIANO": "Pinakiano",
    "PRODROMOS": "Prodromos",
    "NEAPOLIS": "Neapolis",
    "XIDA": "Xida",
    "MONI OD": "Moni Odigitrias",
    "MONI ODIGITRIAS": "Moni Odigitrias",
    "PYR": "Pyrgos (Myrtos)",
    "GORTIS": "Gortys",
    "GORTYS": "Gortys",
    "GORTYN": "Gortys",
    "ARKH": "Arkhanes",
    "MOHLOS": "Mochlos",
    "LASTROS": "Lastros",
    "ARCHANES": "Arkhanes",
    "ARKHANES": "Arkhanes",
    "MALIA": "Mallia",
    "MALLIA": "Mallia",
    "KNOSSOS": "Knossos",
    "PHAISTOS": "Phaistos",
    "ZAKROS": "Zakros",
    "PALAIKASTRO": "Palaikastro",
    "TYLISSOS": "Tylissos",
    "GOURNIA": "Gournia",
    "PETRAS": "Petras",
    "KHANIA": "Khania",
    "CHANIA": "Khania",
    "PSYCHRO": "Psychro",
    "PYRGOS": "Pyrgos (Myrtos)",
    "PLATANOS": "Platanos",
    "SYME": "Symi",
    "VRYSINAS": "Vrysinas",
    "SKOTEINO": "Skoteino",
    "SAM": "Samothrace",
    "SAMOTHRACE": "Samothrace",
    "ABYDOS": "Abydos (Egypt)",
}
_FULL_NAMES_SORTED = sorted(_FULL_NAME_TO_SITE.keys(), key=len, reverse=True)


def _strip_html(s: str) -> str:
    s = _TAG_RE.sub("", s)
    s = html.unescape(s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def parse_heading_line(entry_html: str) -> str:
    """Return the heading line as plain text (after the bold CHIC #)."""
    m = _HEADING_LINE_RE.match(entry_html)
    if not m:
        return ""
    return _strip_html(m.group(1))


def detect_site(heading_text: str, default: str) -> str:
    """Map the leading site code or full-word place name to a human site.

    Priority:
      1. Full-word all-caps place name at heading start (sealstone style:
         `KALO HORIO S: ...`, `PRESOS S: ...`).
      2. Two-letter site code at heading start (clay-doc style:
         `KN Ha (...)`, `MA/M Hd (...)`).
      3. File-default fallback.
    """
    head = heading_text.lstrip()
    upper = head.upper()
    for name in _FULL_NAMES_SORTED:
        if upper.startswith(name + " ") or upper.startswith(name + ":"):
            return _FULL_NAME_TO_SITE[name]
    m = _SITE_CODE_RE.match(head)
    if m:
        code = m.group(1)
        if code in SITE_CODES:
            return SITE_CODES[code]
    return {
        "knossos": "Knossos",
        "mallia": "Mallia",
        "petras": "Petras",
        "misc": "Crete (miscellaneous)",
        "seals_imps": "Crete (seal/sealing, mixed sites)",
    }.get(default, default)


# Fallback support derivation from CHIC's H-class code. Younger uses these
# class codes after the site code: Ha = crescent, Hb = bar (long-string),
# Hc = roundel, Hd = cone, He = medallion, Hf = lame (4-sided flat
# tablet-strip), Hg = bar, Hh = tablet, Hi = tablet (a fragment),
# Imp = clay sealing impressed by a sealstone.
_HCLASS_RE = re.compile(r"\b(?:[A-Z]{2}(?:/[A-Z])?)\s+(H[a-i]|Imp|Y[a-c]|Z[a-z])\b")
_HCLASS_TO_SUPPORT = {
    "Ha": "crescent",
    "Hb": "bar",
    "Hc": "roundel",
    "Hd": "cone",
    "He": "medallion",
    "Hf": "lame",
    "Hg": "bar",
    "Hh": "tablet",
    "Hi": "tablet",
    "Imp": "sealing",
    "Ya": "stone_inscription",  # MA/M Ya = inscribed stone object
    "Yb": "chamaizi_vase",      # MA/M Yb = Chamaizi-style stone vase
    "Yc": "potsherd",
    "Za": "stone_inscription",
    "Zb": "stone_inscription",
}


def detect_support(heading_text: str) -> str:
    """Match a support-type keyword against the heading line.

    Falls back to the CHIC H-class code (Ha, Hb, ..., Hi, Imp, Ya, Yb)
    when no descriptive keyword matches; falls back to 'seal' if the
    heading contains 'CMS' (Corpus der Minoischen Siegel) but no other
    cue, since CMS-numbered objects in this corpus are sealstones.
    """
    low = heading_text.lower()
    for keyword, support in SUPPORT_KEYWORDS:
        if keyword in low:
            return support
    m = _HCLASS_RE.search(heading_text)
    if m:
        cls = m.group(1)
        if cls in _HCLASS_TO_SUPPORT:
            return _HCLASS_TO_SUPPORT[cls]
    if "cms " in low:
        return "seal"
    return "unknown"


# Period detection: pulls "MM I-III" / "MM IIA" / "MM IB-IIB" style strings
# out of the heading line where present. CHIC inscriptions span MM IA-LM I
# but most are MM II; explicit per-entry dating in the catalog is sparse.
_PERIOD_RE = re.compile(
    r"\b(?:MM|EM|LM|MMM)\s*[IVX]+(?:[A-C])?(?:\s*[-/]\s*[IVX]+(?:[A-C])?)?\b"
)


def detect_period(heading_text: str) -> str | None:
    m = _PERIOD_RE.search(heading_text)
    if m:
        return m.group(0)
    return None


# ---------------------------------------------------------------------------
# Table extraction: pull the first transnumeration table after the heading.
# ---------------------------------------------------------------------------

# A row's transnumeration cell is the LAST <td> in the row when the table
# header includes "transnumeration". For multi-table entries (commentary +
# JGY normalize), we want only the FIRST data table.
_TABLE_RE = re.compile(r"<table\b[^>]*>(.*?)</table>", re.IGNORECASE | re.DOTALL)
_ROW_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
_CELL_RE = re.compile(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", re.IGNORECASE | re.DOTALL)


def extract_first_data_table(entry_html: str) -> list[list[str]] | None:
    """Find the first table whose header row mentions 'transnumeration'.

    Returns a list of rows, each a list of cell strings (HTML retained
    so the tokenizer can read <u>NNN</u> markers).
    """
    for tab_m in _TABLE_RE.finditer(entry_html):
        body = tab_m.group(1)
        rows: list[list[str]] = []
        for row_m in _ROW_RE.finditer(body):
            cells = [c.group(1) for c in _CELL_RE.finditer(row_m.group(1))]
            rows.append(cells)
        if not rows:
            continue
        # Header row contains 'transnumeration' (case-insensitive, after
        # stripping HTML).
        header_text = " ".join(_strip_html(c) for c in rows[0]).lower()
        if "transnumeration" in header_text:
            return rows
    return None


# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

# Sub/sup markers — we want to keep the digits inside, not strip them.
# Numbered subscripts (e.g., RO<sub>2</sub>) appear in NORMALIZATION columns,
# never in transnumeration; safe to drop here.
_SUB_SUP_RE = re.compile(r"</?(?:sub|sup)[^>]*>", re.IGNORECASE)
# Underlined sign id → uncertain reading marker
_UNDERLINE_RE = re.compile(
    r"<u(?:\s[^>]*)?>(\d{1,3})</u>", re.IGNORECASE
)
# Bold-wrapped numeric quantity (e.g., <b>7000</b>) inside transnumeration
_BOLD_NUM_RE = re.compile(
    r"<b(?:\s[^>]*)?>(\d{2,5})</b>", re.IGNORECASE
)


def tokenize_transnumeration(rows: list[list[str]]) -> tuple[
    list[str], str, str
]:
    """Convert the transnumeration cells of a CHIC entry into tokens.

    Returns (tokens, raw_transliteration, transcription_confidence).

    Token rules (see module docstring):
      - bare or underlined digit-group → `#NNN` (zero-padded to 3 digits)
      - underlined → `[?:#NNN]`
      - bracket / damage marker → `[?]` or `[?:#NNN]`
      - bold numeric → `NUM:NNN`
      - X orientation marker → skipped
      - whitespace between sign-groups within a side → DIV
      - between non-empty sides → DIV
      - empty (vacat) sides → no tokens, no DIV
    """
    sides: list[list[str]] = []  # list of token-lists, one per non-empty side
    raw_parts: list[str] = []  # for raw_transliteration (verbatim cell text)
    confidence_marks = 0
    total_signs = 0

    for row in rows:
        if not row:
            continue
        # Skip header row(s): rows where any cell text contains
        # "transnumeration" or "inscription" header labels.
        header_test = " ".join(_strip_html(c) for c in row).lower()
        if "transnumeration" in header_test:
            # First-row header.
            continue
        # Transnumeration cell = the LAST cell with substantive content.
        # Some rows have only "no seal impression" / "vacat" / etc.
        cell = row[-1] if row else ""
        cell_clean = _strip_html(cell).strip()
        if not cell_clean:
            continue
        if cell_clean.lower().startswith(
            ("vacat", "[vacat", "no seal", "&nbsp;")
        ):
            continue
        if cell_clean in {"&nbsp;", "—", "-", ""}:
            continue
        side_html = cell
        # Extract markers BEFORE stripping HTML
        # 1. Mark underlined digit groups
        marked = _UNDERLINE_RE.sub(r"@@U:\1@@", side_html)
        # 2. Mark bold numerals (counts/quantities)
        marked = _BOLD_NUM_RE.sub(r"@@NUM:\1@@", marked)
        # 3. Strip remaining sub/sup tags
        marked = _SUB_SUP_RE.sub("", marked)
        # 4. Strip remaining HTML tags (images etc.)
        marked = _TAG_RE.sub(" ", marked)
        # 5. Decode entities
        marked = html.unescape(marked)
        # 6. Normalize whitespace
        marked = _WS_RE.sub(" ", marked).strip()
        if not marked:
            continue
        # raw_transliteration: convert internal markers back to a readable
        # form for the per-inscription record. `@@U:NNN@@` → `_NNN_`
        # (underline-as-underscore convention common in epigraphic
        # publications); `@@NUM:NNN@@` → `NNN` (drop the marker since the
        # context already tells the reader it's a count).
        readable = re.sub(r"@@U:(\d{1,3})@@", r"_\1_", marked)
        readable = re.sub(r"@@NUM:(\d{1,5})@@", r"\1", readable)
        raw_parts.append(readable)
        # Tokenize: split on whitespace into "groups", each group is a
        # word boundary; within a group, hyphens separate signs.
        side_tokens: list[str] = []
        groups = marked.split(" ")
        first_group = True
        for grp in groups:
            grp = grp.strip()
            if not grp:
                continue
            grp_tokens = _tokenize_group(grp)
            if not grp_tokens:
                continue
            if not first_group and side_tokens:
                side_tokens.append("DIV")
            side_tokens.extend(grp_tokens)
            for t in grp_tokens:
                if t == "[?]" or t.startswith("[?:"):
                    confidence_marks += 1
                if t.startswith("#") or t.startswith("[?:#"):
                    total_signs += 1
            first_group = False
        if side_tokens:
            sides.append(side_tokens)

    tokens: list[str] = []
    for i, st in enumerate(sides):
        if i > 0:
            tokens.append("DIV")
        tokens.extend(st)

    raw_translit = " / ".join(raw_parts)

    if total_signs == 0:
        confidence = "fragmentary"
    else:
        damage_ratio = confidence_marks / max(total_signs, 1)
        if damage_ratio == 0:
            confidence = "clean"
        elif damage_ratio < 0.30:
            confidence = "partial"
        else:
            confidence = "fragmentary"

    return tokens, raw_translit, confidence


_GROUP_TOKEN_RE = re.compile(
    r"""(?x)
    @@U:(\d{1,3})@@          # underlined sign id
    | @@NUM:(\d{2,5})@@      # bold quantity
    | \*?(\d{1,3})\b         # bare or asterisked sign id
    | (\])                   # right bracket = damage to right
    | (\[)                   # left bracket = damage to left
    | (vacat)                # vacat marker (already filtered usually)
    | ([A-Z]+(?:\d|<sub>)?)  # logogram name (e.g., BOS, VAS)
    | (.)                    # one-character fallback (X, &, ?, >, etc.)
    """
)


def _tokenize_group(grp: str) -> list[str]:
    """Tokenize one whitespace-delimited group of the transnumeration cell.

    Within a group, signs are typically hyphen-joined (e.g., "070-031-034").
    Numeric quantities appear as standalone (no hyphens) digit strings.
    A `*NNN` prefix always marks a logogram (sign ID).

    Disambiguation rule (CHIC v0):
      - hyphen-joined → all digit-groups treated as sign IDs
      - `*NNN` standalone → sign ID
      - bare `NNN` standalone → numeric count (NUM:N) — NOT a sign ID,
        because Younger always hyphen-joins sign IDs in the canonical
        transnumeration column
      - explicit @@NUM:NNN@@ marker (from <b> in source) → numeric count
    """
    is_hyphen_group = "-" in grp
    pieces = grp.split("-")
    out: list[str] = []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        out.extend(_tokenize_piece(piece, in_hyphen_group=is_hyphen_group))
    return out


def _tokenize_piece(piece: str, *, in_hyphen_group: bool) -> list[str]:
    out: list[str] = []
    pos = 0
    pending_damage = False
    saw_star = False
    while pos < len(piece):
        m = _GROUP_TOKEN_RE.match(piece, pos)
        if not m:
            ch = piece[pos]
            if ch == "*":
                saw_star = True
            pos += 1
            continue
        pos = m.end()
        u, num, sign, rb, lb, vac, name, fb = m.groups()
        if u:
            out.append(f"[?:#{int(u):03d}]")
            pending_damage = False
            saw_star = False
        elif num:
            out.append(f"NUM:{int(num)}")
            pending_damage = False
            saw_star = False
        elif sign:
            sign_int = int(sign)
            star_prefix = m.group(0).startswith("*") or saw_star
            # Was this digit-group preceded by `*`? Two paths to true:
            # the regex captures `\*?(\d{1,3})` so m.group(0) starts with
            # `*` if so; OR a stray `*` was scanned by the fallback path.
            if in_hyphen_group or star_prefix:
                sign_id = f"#{sign_int:03d}"
                if pending_damage:
                    out.append(f"[?:{sign_id}]")
                else:
                    out.append(sign_id)
            else:
                # Standalone bare digits = count (NUM:N).
                if pending_damage:
                    out.append("[?]")
                else:
                    out.append(f"NUM:{sign_int}")
            pending_damage = False
            saw_star = False
        elif rb or lb:
            pending_damage = True
        elif vac:
            pass
        elif name:
            # Logogram names like BOS, VAS appear in the raw text but are
            # also covered by the numeric *NNN logogram id; skip in v0.
            pass
        elif fb:
            # Fallback chars: X (orientation), ?, >, <, &, etc. The "?"
            # alone marks an unidentified sign.
            if fb == "?":
                if not pending_damage:
                    out.append("[?]")
                pending_damage = False
            elif fb == "*":
                saw_star = True
    if pending_damage:
        out.append("[?]")
    return out


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


def parse_file(path: Path, default_site: str) -> list[dict]:
    """Parse one cached HTML page into a list of CHIC entry records."""
    text = path.read_bytes().decode("latin-1")
    records: list[dict] = []
    for chic_num, entry_html in split_entries(text):
        heading_text = parse_heading_line(entry_html)
        site = detect_site(heading_text, default_site)
        support = detect_support(heading_text)
        period = detect_period(heading_text)
        rows = extract_first_data_table(entry_html)
        if rows is None:
            continue
        tokens, raw_translit, confidence = tokenize_transnumeration(rows)
        if not tokens:
            # Entries with a transnumeration table but no recoverable
            # signs (all-vacat, all-commentary) are dropped at v0; record
            # them in corpus_status.chic.md as a known gap.
            continue
        rec = {
            "id": f"CHIC #{chic_num:03d}",
            "site": site,
            "support": support,
            "period": period,
            "transcription_confidence": confidence,
            "tokens": tokens,
            "raw_transliteration": raw_translit,
            "source": "younger_online",
            "source_citation": wayback_url(path.name),
            "fetched_at": FETCHED_AT,
        }
        records.append(rec)
    return records


def build_corpus() -> list[dict]:
    """Walk all cached pages, parse, dedupe by CHIC #, return sorted list.

    Dedupe rule: an entry can appear in more than one Younger page (a
    commentary block re-cites #225, etc.). We keep the FIRST occurrence in
    the page-priority order declared in PAGES, which matches Younger's
    section-of-canonical-record convention:
      KN clay → KNtexts.html
      MA clay → MAtexts.html
      PE additions → PEtexts.html
      misc additions → misctexts.html
      sealstones/impressions → SealsImps.html
    """
    all_records: dict[int, dict] = {}
    for filename, default_site in PAGES:
        path = CACHE / filename
        if not path.exists():
            raise SystemExit(
                f"missing cache file {path}; run with --fetch first"
            )
        for rec in parse_file(path, default_site):
            chic_num = int(rec["id"].rsplit("#", 1)[-1])
            # Prefer entries from a "matching" file (file that actually
            # owns this CHIC range): KN owns 1-69-ish, MA owns 70-122, etc.
            # In practice the FIRST match across PAGES is canonical because
            # commentary cross-references appear later in document order.
            if chic_num not in all_records:
                all_records[chic_num] = rec
            else:
                # Prefer the entry with more sign tokens (i.e., the
                # canonical entry over a brief commentary recap).
                existing = all_records[chic_num]
                if len(rec["tokens"]) > len(existing["tokens"]):
                    all_records[chic_num] = rec
    return sorted(all_records.values(), key=lambda r: r["id"])


# ---------------------------------------------------------------------------
# Status report (corpus_status.chic.md)
# ---------------------------------------------------------------------------


def render_status(records: list[dict]) -> str:
    from collections import Counter

    sites = Counter(r["site"] for r in records)
    supports = Counter(r["support"] for r in records)
    confidences = Counter(r["transcription_confidence"] for r in records)
    periods = Counter(r["period"] or "(unstated)" for r in records)
    sources = Counter(r["source"] for r in records)
    sign_counter: Counter = Counter()
    role_counter: Counter = Counter()
    for r in records:
        for t in r["tokens"]:
            if t == "DIV":
                role_counter["DIV"] += 1
            elif t.startswith("#"):
                sign_counter[t] += 1
                role_counter["sign_clean"] += 1
            elif t.startswith("[?:#"):
                sign_counter[t[3:-1]] += 1
                role_counter["sign_uncertain"] += 1
            elif t == "[?]":
                role_counter["unknown"] += 1
            elif t.startswith("NUM:"):
                role_counter["num"] += 1
            else:
                role_counter["other"] += 1
    distinct_signs = len(sign_counter)
    total_sign_tokens = role_counter["sign_clean"] + role_counter["sign_uncertain"]

    chic_nums = sorted(int(r["id"].rsplit("#", 1)[-1]) for r in records)
    missing = sorted(set(range(1, 332)) - set(chic_nums))

    lines: list[str] = []
    a = lines.append
    a("# Corpus status — Cretan Hieroglyphic v0 (chic-v0)")
    a("")
    a(
        "This document is the source of truth for what's in "
        "`corpora/cretan_hieroglyphic/`, where it came from, what was "
        "dropped, and what experimental harnesses can rely on. It mirrors "
        "the format of `corpus_status.md` (Linear A) and is produced by "
        "`scripts/build_chic_corpus.py`."
    )
    a("")
    a(f"Last refresh: **{FETCHED_AT[:10]}**.")
    a("")
    a("## Source")
    a("")
    a(
        "- **Younger, J. G.** *The Cretan Hieroglyphic Texts: a web edition "
        "of CHIC with commentary.* Originally hosted at "
        "`people.ku.edu/~jyounger/Hiero/` (offline since 2022); we "
        "fetch from the Internet Archive Wayback Machine snapshot "
        f"`{WAYBACK_SNAPSHOT}` (2022-07-03), the last complete capture."
    )
    a(
        "- **Underlying print authority.** Olivier, J.-P. & Godart, L. "
        "(1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* "
        "(Études Crétoises 31). Paris. CHIC catalog numbers "
        "(#001-#331) are preserved verbatim from this edition."
    )
    a(
        "- **Five index pages cached** under `.cache/younger_chic/`: "
        "KNtexts.html (Knossos clay docs), MAtexts.html (Mallia clay "
        "docs), PEtexts.html (Petras post-CHIC additions), misctexts.html "
        "(misc additions), SealsImps.html (sealstones + impressions, the "
        "bulk of the corpus)."
    )
    a("")
    a("## Coverage")
    a("")
    a("| Metric | Count |")
    a("|---|---|")
    a("| CHIC numbered entries (catalog range #001-#331) | 331 |")
    a(f"| Inscriptions ingested | **{len(records)}** |")
    a(f"| Distinct CHIC sign IDs observed | {distinct_signs} |")
    a(f"| Total sign-token occurrences (clean + uncertain) | {total_sign_tokens} |")
    a(f"| Word-divider (`DIV`) tokens | {role_counter['DIV']} |")
    a(f"| Numeric quantity (`NUM:N`) tokens | {role_counter['num']} |")
    a(f"| Uncertain-reading (`[?:#NNN]`) tokens | {role_counter['sign_uncertain']} |")
    a(f"| Wholly-unknown (`[?]`) tokens | {role_counter['unknown']} |")
    a("")
    a(
        "Acceptance criterion (≥250 inscriptions): "
        f"**{'met' if len(records) >= 250 else 'NOT met'}**."
    )
    a("")
    if missing:
        a(
            f"### Known gaps in CHIC numbering ({len(missing)} of 331 absent)"
        )
        a("")
        a(
            "Missing CHIC numbers are entries where Younger's web edition "
            "carries only a commentary cross-reference, not a substantive "
            "transnumeration table. CHIC catalog numbering is also not "
            "fully contiguous in the print edition — some numbers are "
            "skipped or retired. Manual transcription from Olivier & "
            "Godart 1996 for these gaps is deferred to a future ticket."
        )
        a("")
        miss_lines = ", ".join(f"#{n:03d}" for n in missing)
        a(f"Missing: {miss_lines}.")
        a("")
    a("### Sites")
    a("| Site | Inscriptions |")
    a("|---|---|")
    for site, n in sorted(sites.items(), key=lambda kv: (-kv[1], kv[0])):
        a(f"| {site} | {n} |")
    a("")
    a("### Supports")
    a("| Support | Inscriptions |")
    a("|---|---|")
    for s, n in sorted(supports.items(), key=lambda kv: (-kv[1], kv[0])):
        a(f"| {s} | {n} |")
    a("")
    a("### Transcription confidence")
    a("| Confidence | Inscriptions |")
    a("|---|---|")
    for c in ("clean", "partial", "fragmentary"):
        a(f"| {c} | {confidences.get(c, 0)} |")
    a("")
    a("### Period (where stated in heading)")
    a("| Period | Inscriptions |")
    a("|---|---|")
    for p, n in sorted(periods.items(), key=lambda kv: (-kv[1], kv[0])):
        a(f"| {p} | {n} |")
    a(
        "\nMost CHIC inscriptions date to MM IIA-MM IIB; explicit per-entry "
        "dating is sparse in Younger's transnumeration. Per-inscription "
        "period inheritance from Olivier & Godart 1996 is deferred to "
        "chic-v1."
    )
    a("")
    a("### Sources used (per-inscription provenance)")
    a("| Source | Inscriptions |")
    a("|---|---|")
    for s, n in sources.items():
        a(f"| {s} | {n} |")
    a("")
    a("### Top-30 most frequent sign IDs")
    a("| Sign | Count |")
    a("|---|---|")
    for sign, n in sign_counter.most_common(30):
        a(f"| {sign} | {n} |")
    a("")
    a("## Tokenization rules (chic-v0)")
    a("")
    a(
        "Documented as rules-as-data so that a future harness can re-run "
        "alternative tokenizations directly off the cached HTML in "
        "`.cache/younger_chic/` without re-scraping."
    )
    a("")
    a("| Source (Younger transnumeration) | Token form | Notes |")
    a("|---|---|---|")
    a("| bare digit-group `NNN` | `#NNN` | Zero-padded to 3 digits. Preserves CHIC catalog convention #001-#100 (syllabographic), #101-#308 (logograms / ideograms / fractions). Classification deferred to chic-v1. |")
    a("| underlined `<u>NNN</u>` | `[?:#NNN]` | Younger marks doubtful readings of attested sign ids with underline. |")
    a("| asterisked `*NNN` | `#NNN` | Younger marks logogram-form ids with `*`; same numeric id, kept as `#NNN`. |")
    a("| damage marker `]NNN`, `[NNN`, `?` | `[?:#NNN]` if id known, else `[?]` | Bracket markers attach to the adjacent sign id. |")
    a("| bold quantity `<b>N...N</b>` | `NUM:N` | Numeric counts in administrative documents (e.g., `7000`). |")
    a("| literal `X` orientation marker | (skipped) | Decorative cross / writing-axis indicator, not a CHIC sign. |")
    a("| whitespace between sign-groups within a side | `DIV` | Word boundary. |")
    a("| between non-empty sides | `DIV` | Word boundary. |")
    a("| `vacat` row | (no tokens) | Empty side; no DIV emitted. |")
    a("| ideogram name (BOS, VAS, etc.) | (skipped) | Same sign carries a numeric id elsewhere in the row; `IDEO:<name>` extraction deferred to chic-v1. |")
    a("")
    a("## Out of scope for chic-v0")
    a("")
    a("- Logogram vs syllabographic sign filtering — chic-v1.")
    a("- Paleographic anchor inheritance from Linear A → chic-v2.")
    a("- Substrate framework application to CHIC corpus → chic-v3.")
    a("- Cross-script correlation analysis → chic-v4.")
    a("- Per-sign syllable-value extraction framework → chic-v5+.")
    a("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--fetch", action="store_true",
        help="(Re-)fetch cached HTML from the Wayback Machine before parsing.",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=OUT_DIR,
        help="Output directory (default: corpora/cretan_hieroglyphic/).",
    )
    parser.add_argument(
        "--status", type=Path, default=STATUS_PATH,
        help="Where to write corpus_status.chic.md.",
    )
    args = parser.parse_args(argv)

    if args.fetch:
        fetch_pages()

    if not CACHE.exists() or not any(CACHE.iterdir()):
        # Try a one-shot fetch if the cache is missing.
        fetch_pages()

    inscriptions_dir = args.out_dir / "inscriptions"
    inscriptions_dir.mkdir(parents=True, exist_ok=True)

    records = build_corpus()
    if len(records) < 250:
        print(
            f"WARNING: ingested {len(records)} inscriptions; "
            "ticket asks for >=250.",
            file=sys.stderr,
        )

    # Per-inscription JSON.
    for rec in records:
        # Filename from CHIC #: zero-padded.
        filename = rec["id"].replace("CHIC ", "").replace("#", "") + ".json"
        path = inscriptions_dir / filename
        path.write_text(
            json.dumps(rec, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n",
            encoding="utf-8",
        )

    # Aggregate JSONL.
    all_path = args.out_dir / "all.jsonl"
    with all_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(
                json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n"
            )

    # Corpus status.
    args.status.write_text(render_status(records), encoding="utf-8")

    print(
        f"wrote {len(records)} CHIC inscriptions  |  "
        f"{sum(1 for r in records for t in r['tokens'] if t.startswith('#'))} "
        f"clean sign tokens  |  "
        f"{sum(1 for r in records for t in r['tokens'] if t.startswith('[?:#'))} "
        f"uncertain  |  "
        f"{sum(1 for r in records for t in r['tokens'] if t == 'DIV')} dividers",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
