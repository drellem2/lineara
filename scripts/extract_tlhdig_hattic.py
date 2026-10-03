#!/usr/bin/env python3
"""Extract the Hattic words of the TLHdig transliterations (mg-7f4db).

Source: Thesaurus Linguarum Hethaeorum digitalis (TLHdig), Beta Version
0.2, XML dataset on Zenodo, DOI 10.5281/zenodo.15459134 (CC BY 4.0;
online at https://www.hethport.uni-wuerzburg.de/TLHdig/). The
transliterations are those of the published Boğazköy editions, gathered
by the Hethitologie-Portal Mainz.

This script is run by hand against the downloaded zip. It writes
``corpora/hattic/sources/tlhdig_hattic_lines.tsv``, which is committed
and is the only input of ``scripts/build_hattic_corpus.py``; the zip
itself (64 MB) is not committed.

What counts as a Hattic word
----------------------------
TLHdig tags the language of every line (``<lb lg="Hattian">`` or
``lg="Hat"``) and, where it differs from the line, of single words
(``<w lg="Hat">``). A word is Hattic if its own ``lg`` says so, or it has
none and its line's does.

Which Hattic words are kept as *intact*
---------------------------------------
TLHdig marks a break with ``<del_in/>`` … ``<del_fin/>``, and the break
can run across words and lines. Any sign inside a break is lost or
restored by the editor, so a word that touches a break is not intact.
Also not intact: a word that begins or ends with a hyphen (a fragment),
contains an illegible sign (``x``), an ellipsis, a Sumerogram (``<sGr>``)
or an Akkadogram (``<aGr>``), or has no letters left. So is a word with
a sign the scribe omitted and the editor supplied (``〈…〉``) or a
superfluous sign the editor deletes (``〈〈…〉〉``), an unread
sign given as a cuneiform glyph, or a ``+``. Determinatives (``<d>``),
damage marks on readable signs (``<laes_in/>`` …), editorial
``<corr>``/``<note>`` marks, ``(-)``/``(?)``/``(!)`` and sign-index
numbers (``ša₄`` → ``ša``) are dropped from an intact word, which keeps
its hyphenated syllabic transliteration.

Output columns (one row per line with at least one Hattic word):
  cth, manuscript, line, n_hattic_words, raw, intact
``raw`` lists every Hattic word of the line with broken stretches shown
as ``[…]``; ``intact`` lists the intact words only, space-separated.
Rows are sorted by (CTH number, manuscript, file order of the line).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT = _REPO_ROOT / "corpora" / "hattic" / "sources" / "tlhdig_hattic_lines.tsv"

_HATTIC = {"Hat", "Hattian"}
_TOKEN = re.compile(r"<lb\b[^>]*/>|<w\b[^>]*/>|<w\b[^>]*>.*?</w>", re.S)
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_CTH = re.compile(r"CTH (\d+(?:\.\d+)?)_XML/")


def _attrs(tag: str) -> dict[str, str]:
    head = tag[: tag.index(">") + 1]
    return dict(_ATTR.findall(head))


def _render_word(inner: str, broken: bool) -> tuple[str, str | None, bool]:
    """Walk one word's inner XML.

    Returns ``(raw, intact_or_None, broken_after)``: ``raw`` shows broken
    stretches as ``[…]``; ``intact`` is the clean transliteration or None
    when the word is not intact (see module docstring).
    """
    raw: list[str] = []
    clean: list[str] = []
    ok = True
    if broken:
        ok = False
        raw.append("[")
    pos = 0
    in_d = False
    for m in re.finditer(r"<[^>]*>", inner):
        text = html.unescape(inner[pos : m.start()])
        pos = m.end()
        if text:
            raw.append(text)
            if broken:
                ok = False
            elif not in_d:
                clean.append(text)
        tag = m.group(0)
        name = re.match(r"</?([A-Za-z_:]+)", tag)
        name = name.group(1) if name else ""
        if name == "del_in":
            broken = True
            ok = False
            raw.append("[")
        elif name == "del_fin":
            broken = False
            raw.append("]")
        elif name == "d":
            in_d = not tag.startswith("</")
        elif name in ("sGr", "aGr", "space"):
            ok = False
    text = html.unescape(inner[pos:])
    if text:
        raw.append(text)
        if broken:
            ok = False
        elif not in_d:
            clean.append(text)
    raw_s = "".join(raw).replace("[]", "").replace("][", "")
    word = "".join(clean)
    if ok:
        word = re.sub(r"\((?:-|\?|!)\)", "", word)  # (-) (?) (!) marks
        word = re.sub(r"[?!⌈⌉⸢⸣˹˺()]", "", word)
        word = re.sub(r"[0-9₀-₉ₓ]", "", word)  # sign-index numbers
        if (
            not word
            or word.startswith("-")
            or word.endswith("-")
            or "x" in word
            or "…" in word
            or "..." in word
            # sign supplied (〈…〉) or deleted (〈〈…〉〉) by the editor
            or any(c in word for c in "\u2329\u232a\u3008\u3009\u27e8\u27e9<>+")
            # raw cuneiform glyphs (unread sign)
            or any("\U00012000" <= c <= "\U0001254f" for c in word)
            or any(c.isupper() for c in word)
            or not any(c.isalpha() for c in word)
        ):
            ok = False
    return raw_s, (word if ok else None), broken


def extract_document(xml: str) -> list[tuple[str, str, list[str], list[str]]]:
    """Return ``[(manuscript, line, raw_words, intact_words)]`` for the
    lines of one TLHdig document that carry Hattic words."""
    m = re.search(r"<docID>(.*?)</docID>", xml)
    doc = html.unescape(m.group(1)).strip() if m else ""
    out: list[tuple[str, str, list[str], list[str]]] = []
    line_lg = ""
    line_nr = ""
    cur: tuple[str, list[str], list[str]] | None = None
    broken = False
    for tok in _TOKEN.finditer(xml):
        t = tok.group(0)
        if t.startswith("<lb"):
            a = _attrs(t)
            line_lg = a.get("lg", "")
            line_nr = html.unescape(a.get("lnr", ""))
            if cur and cur[1]:
                out.append((doc, cur[0], cur[1], cur[2]))
            cur = (line_nr, [], [])
            continue
        a = _attrs(t)
        inner = t[t.index(">") + 1 : -len("</w>")] if t.endswith("</w>") else ""
        raw, intact, broken = _render_word(inner, broken)
        lang = a.get("lg", line_lg)
        if lang not in _HATTIC or cur is None or not raw.strip():
            continue
        cur[1].append(raw)
        if intact:
            cur[2].append(intact)
    if cur and cur[1]:
        out.append((doc, cur[0], cur[1], cur[2]))
    return out


def _cth_key(cth: str) -> tuple[float, str]:
    try:
        return (float(cth), cth)
    except ValueError:
        return (float("inf"), cth)


def extract_zip(zip_path: Path) -> list[list[str]]:
    rows: list[tuple[tuple, list[str]]] = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in sorted(zf.namelist()):
            if "__MACOSX" in name or not name.endswith(".xml"):
                continue
            cm = _CTH.search(name)
            if not cm:
                continue
            xml = zf.read(name).decode("utf-8", errors="replace")
            if 'lg="Hat' not in xml:
                continue
            cth = cm.group(1)
            for i, (doc, line, raw, intact) in enumerate(extract_document(xml)):
                rows.append(
                    (
                        (_cth_key(cth), doc, name, i),
                        [cth, doc, line, str(len(raw)), " ".join(raw), " ".join(intact)],
                    )
                )
    rows.sort(key=lambda r: r[0])
    return [r[1] for r in rows]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("zip", type=Path, help="TLHdig_0.2.0-beta.zip from Zenodo")
    parser.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = parser.parse_args(argv)

    rows = extract_zip(args.zip)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        fh.write("cth\tmanuscript\tline\tn_hattic_words\traw\tintact\n")
        for r in rows:
            for field in r:
                if "\t" in field or "\n" in field:
                    raise SystemExit(f"tab/newline in field: {r!r}")
            fh.write("\t".join(r) + "\n")
    n_words = sum(int(r[3]) for r in rows)
    n_intact = sum(len(r[5].split()) for r in rows)
    print(
        f"wrote {len(rows)} lines | {n_words} Hattic words | {n_intact} intact",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
