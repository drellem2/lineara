# Cretan Hieroglyphic inscription corpus (mg-99df, chic-v0)

External inscription corpus for the **chic-v** sub-program, the
methodologically-distinct second leg of the lineara research line.
While the main lineara/v0-v25 work tests substrate-language
hypotheses against Linear A at the population level, the chic-v
program targets per-sign syllable-value extraction for the older,
less-well-attested Cretan Hieroglyphic script — leveraging
paleographic anchors carrying over from Linear A, substrate
consistency, and cross-script consistency. The infrastructure
(external phoneme LMs, paired-difference scoring, control pools,
bayesian rollups) is shared with the Linear A program; the
corpora differ.

This is the **chic-v0** ticket: ingest only. No analysis, no
filtering, no per-sign reading hypotheses — those land in
chic-v1+.

## Provenance

- **Younger, J. G.** (2005-2022). *The Cretan Hieroglyphic Texts: a
  web edition of CHIC with commentary.* Originally hosted at
  `people.ku.edu/~jyounger/Hiero/` (the personal-page subdomain
  was retired sometime between mid-2022 and the chic-v0 build
  date; the live URL no longer resolves). We fetch from the
  Internet Archive Wayback Machine snapshot
  `20220703170656` (2022-07-03), which is the last complete
  capture of all five index pages.
- **Underlying print authority.** Olivier, J.-P. & Godart, L.
  (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études
  Crétoises 31). Paris: École française d'Athènes (= **CHIC**).
  Younger's web edition retransnumerates each entry sign-by-sign,
  preserving CHIC's catalog numbering exactly (#001-#331); we
  preserve those numbers verbatim in the `id` field so any
  future cross-reference back to the print catalogue works
  one-to-one.
- **Five Younger index pages** are fetched and cached:
  - `KNtexts.html` — Knossos clay documents (~CHIC #001-#069)
  - `MAtexts.html` — Mallia clay documents (~CHIC #070-#122)
  - `PEtexts.html` — Petras post-CHIC additions (Tsipopoulou &
    Hallager 2010)
  - `misctexts.html` — miscellaneous additions (Chamaizi vases,
    misc. inscribed objects, ~#316+)
  - `SealsImps.html` — sealstones and impressions (CHIC #123-
    #179 = impressions on clay; #180-#331 = sealstones; this is
    the bulk of the corpus by entry count)
- **Source priority for deduplication.** A CHIC # may appear in
  more than one Younger page when one entry's commentary
  cross-references another. The build script keeps the first
  occurrence whose body actually carries a transnumeration table;
  in practice this resolves to the canonical home page for each
  CHIC # (KN, MA, PE, misc, or SealsImps).

## License

The underlying inscriptions are public domain (Bronze Age and Iron
Age Cretan archaeology, ~MM IA-LM I, c. 2000-1450 BCE). Cited
fair-use of Olivier & Godart 1996 and Younger 2005-2022 for the
catalog numbering, sign-by-sign transnumeration, and editorial
conventions.

This repository commits:
- `corpora/cretan_hieroglyphic/inscriptions/<NNN>.json` —
  per-inscription metadata (CHIC #, site, support, period,
  tokens, raw transliteration, source citation, fetched-at
  timestamp).
- `corpora/cretan_hieroglyphic/all.jsonl` — aggregate, sorted by
  CHIC #.
- `scripts/build_chic_corpus.py` — idempotent, deterministic
  build script.
- `corpus_status.chic.md` — coverage statistics, sourcing notes,
  tokenization rules table, known gaps in CHIC numbering.
- `harness/tests/test_chic_corpus.py` — schema validation +
  smoke check on a 5-record sample.

The cached HTML pages under `.cache/younger_chic/` are
**not** committed (gitignored); rebuild with
`python3 scripts/build_chic_corpus.py --fetch`.

## Reproducibility

```bash
# One-shot build (uses cached HTML if present, fetches if missing)
python3 scripts/build_chic_corpus.py

# Force re-fetch from Wayback Machine, then rebuild
python3 scripts/build_chic_corpus.py --fetch
```

The build is **deterministic**: byte-identical `all.jsonl` and
per-inscription JSON across re-runs given the same cached HTML.
Verified at chic-v0 build time (2026-05-05).

## Format

Per-inscription JSON (matches the chic-v0 schema declared in the
ticket):

```json
{
  "id": "CHIC #001",
  "site": "Knossos",
  "support": "crescent",
  "period": null,
  "transcription_confidence": "partial",
  "tokens": ["[?:#053]", "#034", "#031", "#070"],
  "raw_transliteration": "X _053_-034-031-070",
  "source": "younger_online",
  "source_citation": "http://web.archive.org/web/20220703170656/http://www.people.ku.edu/~jyounger/Hiero/KNtexts.html",
  "fetched_at": "2026-05-05T11:00:00Z"
}
```

Field semantics:
- `id`: `CHIC #NNN` with three-digit zero-padded catalog number.
  Preserves CHIC's catalog convention exactly — do **not**
  renumber.
- `site`: human-readable find-spot (Knossos, Mallia, Khania,
  Phaistos, ...). Derived from the leading site code (or
  full-word place name in the case of post-1996 sealstone
  publications) in the heading line.
- `support`: physical support category — crescent, bar, tablet,
  medallion, cone, lame, roundel, nodulus, sealing, seal,
  chamaizi_vase, pithos, vase, potsherd, offering_table,
  stone_inscription, plaque, bronze, metal_ring, stone_axe.
  Derived from heading keyword scan, with H-class code
  (Ha=crescent, Hd=cone, He=medallion, Hf=lame, Hg=bar,
  Hh=tablet, Imp=sealing, Yb=chamaizi_vase) as fallback.
- `period`: archaeological dating where the heading line states
  it (e.g., `MM IA-IB`, `MM IIB`, `EM III`); otherwise `null`.
  Per-entry period inheritance from Olivier & Godart 1996 is
  deferred to chic-v1.
- `transcription_confidence`: `clean` (no damage markers),
  `partial` (some damage but < 30% of sign tokens), `fragmentary`
  (≥ 30% damaged or zero clean signs).
- `tokens`: ordered token sequence per the chic-v0 tokenization
  rules (see `corpus_status.chic.md`).
- `raw_transliteration`: human-readable verbatim string of the
  transnumeration column from Younger's table, with sides joined
  by ` / `. Underlined-doubtful sign IDs are rendered as `_NNN_`.
- `source`: provenance pointer — `younger_online` for v0; future
  tickets may add `olivier_godart_1996` (manual transcription of
  print-only entries), `damos`, or `liber` records.
- `source_citation`: stable URL to the Wayback snapshot of the
  Younger page that supplied this entry.
- `fetched_at`: ISO-8601 timestamp; fixed at the chic-v0 build
  date for determinism.

## Tokenization rules (chic-v0)

The full rules-as-data table lives in `corpus_status.chic.md`.
Summary:

| Source (Younger transnumeration) | Token form |
|---|---|
| bare digit-group, hyphen-joined `NNN-NNN-NNN` | `#NNN` per sign (zero-padded to 3 digits) |
| underlined `<u>NNN</u>` | `[?:#NNN]` |
| asterisked `*NNN` (logogram form) | `#NNN` |
| damage marker `]NNN`, `[NNN`, `?` | `[?:#NNN]` if id known, else `[?]` |
| bold-wrapped quantity `<b>N...N</b>` | `NUM:N` |
| standalone bare digit string | `NUM:N` (counts, not signs) |
| literal `X` orientation marker | (skipped — not a CHIC sign) |
| whitespace between groups within a side | `DIV` |
| between non-empty sides | `DIV` |
| `vacat` row | (no tokens, no DIV) |

CHIC sign IDs preserve the catalog convention: #001-#100 are
syllabographic (some doubling as logograms), #101-#308 are
logograms / ideograms / fractions. **Logogram vs
syllabographic-sign filtering is deferred to chic-v1.** v0 just
ingests; the sign-classification question is chic-v1's job.

## Coverage summary

302 of 331 CHIC catalog entries ingested (~91%). The 29
missing CHIC numbers are entries where Younger's web edition
carries only a commentary cross-reference, not a substantive
transnumeration table; CHIC catalog numbering is also not fully
contiguous in the print edition. See `corpus_status.chic.md` for
the explicit gap list and per-site / per-support / per-period /
top-30-sign-frequency distributions.

## Out of scope for chic-v0

Listed for clarity; do **not** add any of these in chic-v0:
- Logogram vs syllabographic sign filtering — chic-v1.
- Paleographic anchor inheritance from Linear A — chic-v2.
- Substrate framework application to CHIC corpus — chic-v3.
- Cross-script correlation analysis — chic-v4.
- Per-sign syllable-value extraction framework — chic-v5+.
- AGENTS.md update to acknowledge the chic sub-program — small
  follow-up ticket.
