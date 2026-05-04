# Corpus status — Linear A v1

This document is the source of truth for what's in `corpus/`, where it came from, what was dropped, and what experimental harnesses can rely on. It also feeds the `corpus-status` PM-sweep source declared in `~/.pogo/agents/pm/lineara.toml`.

Last refresh: **2026-05-04** (run `scripts/fetch_sigla.py` then `scripts/parse_sigla.py` to rebuild).

## Source

- **SigLA** — *The signs of Linear A: a paleographical database* by Ester Salgarella & Simon Castellan. https://sigla.phis.me
- License: **CC BY-NC-SA 4.0** (dataset and drawings).
- Underlying print authority: GORILA (Godart & Olivier, *Recueil des inscriptions en linéaire A*, 1976–85). SigLA tokens line up with GORILA/SigLA's canonical AB-numbers; per-inscription `corpus_link` fields point back to the GORILA / EtCret edition page where SigLA provides one.
- Access mode: SigLA does not advertise a JSON API, but every inscription is served as a static HTML page (the in-page database is shipped via `database.js`, an OCaml `js_of_ocaml` bytecode bundle that we did not attempt to decode). We scrape both the **sign view** (`/document/<id>/`) and the **word view** (`/document/<id>/index-word.html`) for each inscription. Both URLs are public and served without auth or robots.txt restrictions; our fetcher honors a polite throttle and identifies itself with a descriptive User-Agent.
- Two-stage pipeline:
  1. `scripts/fetch_sigla.py` — discovers IDs from `/browse.html`, fetches sign + word views, caches under `.cache/sigla/`. Idempotent (skips already-cached files). Failed fetches are retried up to 3×.
  2. `scripts/parse_sigla.py` — parses cached HTML, applies v1 tokenization, writes per-inscription JSON under `corpus/<site>/` and aggregates into `corpus/all.jsonl`.
  3. `scripts/build_corpus.py --strict` — round-trips per-inscription JSON → `corpus/all.jsonl` deterministically and validates every record against `schema/inscription.schema.json`.
  4. `scripts/check_corpus.py` — verifies SigLA's word-view seq-patterns are recoverable from our token stream after the v1 inverse mapping.

## Coverage

| Metric | Count |
|---|---|
| Documents listed in SigLA's `/browse.html` | **772** |
| Inscriptions ingested as records | **772** (100%) |
| Inscriptions with at least one transcribed sign | **761** (98.6%) |
| Inscriptions where SigLA shows a drawing but no signs (kept as `n_signs=0`) | 11 |
| Total transcribed sign occurrences | 4,935 |
| Distinct sign IDs observed | 356 |

The acceptance criterion in the ticket asked for ≥ 80% of SigLA's coverage (≥ ~1,100 records out of an estimated ~1,400). SigLA's actual public corpus is smaller than the ticket estimated — 772 documents — and we ingested all of them. Coverage relative to the *true* SigLA size is ~98.6% with transcriptions plus 1.4% drawing-only stubs.

### Sites
| Site | Inscriptions |
|---|---|
| Haghia Triada | 372 |
| Khania | 213 |
| Phaistos | 63 |
| Zakros | 44 |
| Knossos | 31 |
| Mallia | 20 |
| Arkhanes | 10 |
| Kea | 5 |
| Tylissos | 3 |
| Gournia, Pyrgos | 2 each |
| Haghios Stephanos, Kythera, Melos, Mycenae, Papoura, Psykhro, Syme | 1 each |

### Supports
tablet 426, nodule 166, roundel 146, vase 8, sealing 7, sherd 4, graffiti 3, libation_table 2, plus 1 each of: plaque, lamp, pithoid_jar, clay_vase, architecture, jewellery, stone_weight, clay_weight, metal_engraving, label.

### Transcription confidence
- `clean` (530, 68.7%) — no erasures, unreadable, or uncertain readings.
- `partial` (145, 18.8%) — at least one damaged sign, but < 30% damaged.
- `fragmentary` (97, 12.5%) — ≥ 30% damaged signs **or** zero signs (drawing-only).

### Genre hint
A heuristic from kind + sign-class evidence; **not** authoritative:
- `accountancy` (742) — tablets, roundels, bars, nodules, and any tablet bearing logograms / fractions / transaction signs. The dominant Linear A genre.
- `votive_or_inscription` (10) — vases, libation tables, stone objects.
- `administrative` (7) — sealings.
- `unknown` (13) — supports we have no kind-rule for.

### Token role distribution
| Role / token | Count |
|---|---|
| Bare `AB##` syllabogram | 2,906 |
| `DIV` word divider | 2,212 |
| `LOG:<id>` logogram | 1,119 |
| `[?]` unreadable / erasure | 388 |
| `FRAC:<id>` fraction | 310 |
| Bare `A###` Linear-A-only sign | 133 |
| `[?:<id>]` uncertain reading | 44 |

## Tokenization rules (v1)

These are documented as **rules-as-data** so a future harness can re-run alternative tokenizations directly off the cached HTML in `.cache/sigla/` without re-scraping.

| Source (SigLA) | Token form | Notes |
|---|---|---|
| Syllabogram (sure reading) | `AB78`, `A302`, … | Bare sign id from SigLA's `reading-pattern:(...)` URL. |
| Syllabogram (unsure reading) | `[?:AB17]` | Sign id known but reading uncertain. |
| Unreadable sign (`#N: [?]`) | `[?]` | SigLA shows a placeholder; sign id not extractable. |
| Erasure (any sub-kind) | `[?]` | Collapsed; underlying sign deliberately rubbed out. |
| Logogram (commodity sign) | `LOG:<id>` | Includes `Logogram?` (uncertain role) at same prefix. |
| Fraction sign | `FRAC:<id>` | Includes `Fraction` Erasures collapsed to `[?]`. |
| Transaction sign | `<id>` (bare) | Phonetic AB-numbered signs in transaction-marker position. The role is metadata; the token form intentionally collapses with syllabograms because they share orthography. SigLA's `Transaction sign?` (uncertain role) folds in the same way. |
| Word divider | `DIV` | Inserted between SigLA-defined word groups. Standalone non-word signs (fractions, isolated logograms) are also bracketed by `DIV`. |
| Numeral | (not emitted) | SigLA does not encode numerals as signs — only the sign categories above. The `NUM:<value>` token from the v1 spec is reserved for a future pull from a corpus that records them (e.g., GORILA OCR or Younger). |
| Line break / `BREAK` | (not emitted) | SigLA preserves spatial layout via SVG coordinates but does not mark line breaks as discrete tokens. The harness can recover lines from the per-sign coordinates if needed (we drop these from the token stream to keep v1 minimal). |

### Word-boundary semantics
SigLA's word view groups signs by alternating-color word membership. We map each sign rect's coordinates to the word group it appears in. **An "in-word" non-syllabogram (fraction, logogram, erasure) inherits the surrounding word's group when it is sandwiched between two same-word signs**, mirroring how SigLA visually preserves word integrity across embedded fractions. Standalone non-word signs (e.g., a string of fractions following a word) are emitted as their own `DIV`-delimited groups.

### Cross-check
`scripts/check_corpus.py` confirms that **all 761 transcribed inscriptions** round-trip perfectly: every `word-match @ !seq-pattern:` annotation in SigLA's word view is present in our token stream after applying the inverse tokenization (DIV → `/`, drop `[?]`/`LOG:`/`FRAC:`, keep `[?:X]` as `X`). This is the v1 spot-check requirement satisfied programmatically across the entire corpus rather than on a 10-record sample.

## Known gaps & caveats

1. **Eleven drawing-only inscriptions.** SigLA renders the tablet image but has no sign transcription. We emit them as records with `n_signs=0`, `tokens=[]`, `transcription_confidence="fragmentary"` so the corpus pointer count matches SigLA. Harnesses should filter on `n_signs > 0` before running phonetic experiments.
   - HT 136b, HT 154L, HT Wa 1172, KH 56, KH 66, KH 78, MA 9, PH 22a, ZA 18b, ZA 30, ZA 33.
2. **No numerals.** SigLA's data model does not include numerals as a sign category. Many Linear A tablets that look like commodity records will appear sparser than they actually are. To get numerals, ingest GORILA directly (out of scope for v1) or wait on the Younger pull (separate ticket).
3. **No line-break preservation.** SigLA's HTML lays out signs by absolute SVG coordinates rather than discrete line tokens. Reconstructing line breaks would require a y-coordinate clustering pass over the rect data, which we did not implement for v1.
4. **HT 22 metadata mismatch.** SigLA's `<x> signs / <y> words` text on `/document/HT 22/` claims 3 signs, but only 2 sign rects are rendered. Our parser captures the rendered 2; the count text is a SigLA-side inconsistency.
5. **Genre hint is heuristic.** "Accountancy" covers 742/772 records purely because tablets/roundels/nodules dominate Linear A. The label is intended for coarse filtering, not as ground truth. Expect to override with a smarter classifier downstream.
6. **Transaction signs and logograms are emitted with role markers but no role-disambiguation field.** The schema records `n_signs`/`n_words` aggregates; the per-sign role is not preserved alongside the token. If a harness needs per-token role, re-parse the cached HTML with `parse_sign_view` and align by occurrence order.
7. **The `corpus_link` field carries `&amp;` HTML entities** because we extracted it verbatim from SigLA's HTML. Decoding is left to consumers (a single `html.unescape` call).
8. **Token-stream `BREAK` entries from the v1 spec are not emitted** because SigLA does not mark them. The schema permits future records to include `BREAK` tokens without revision.

## Reproducibility

```bash
# Full corpus rebuild from scratch (idempotent; cache is reused across runs)
python3 scripts/fetch_sigla.py            # ~1 min on a fresh cache
python3 scripts/parse_sigla.py            # < 5 s, fully local
python3 scripts/build_corpus.py --strict  # validates every record
python3 scripts/check_corpus.py           # SigLA round-trip cross-check
```

`corpus/all.jsonl` is sorted by inscription id; identical inputs produce byte-identical output.

## Attribution

When publishing experiments, cite:
- Salgarella, E. & Castellan, S. *SigLA: The signs of Linear A* (https://sigla.phis.me, CC BY-NC-SA 4.0).
- Godart, L. & Olivier, J.-P. *Recueil des inscriptions en linéaire A*, 1976–85 (GORILA), as the underlying authority.
