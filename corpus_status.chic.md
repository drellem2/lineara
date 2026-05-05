# Corpus status — Cretan Hieroglyphic v0 (chic-v0)

This document is the source of truth for what's in `corpora/cretan_hieroglyphic/`, where it came from, what was dropped, and what experimental harnesses can rely on. It mirrors the format of `corpus_status.md` (Linear A) and is produced by `scripts/build_chic_corpus.py`.

Last refresh: **2026-05-05**.

## Source

- **Younger, J. G.** *The Cretan Hieroglyphic Texts: a web edition of CHIC with commentary.* Originally hosted at `people.ku.edu/~jyounger/Hiero/` (offline since 2022); we fetch from the Internet Archive Wayback Machine snapshot `20220703170656` (2022-07-03), the last complete capture.
- **Underlying print authority.** Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris. CHIC catalog numbers (#001-#331) are preserved verbatim from this edition.
- **Five index pages cached** under `.cache/younger_chic/`: KNtexts.html (Knossos clay docs), MAtexts.html (Mallia clay docs), PEtexts.html (Petras post-CHIC additions), misctexts.html (misc additions), SealsImps.html (sealstones + impressions, the bulk of the corpus).

## Coverage

| Metric | Count |
|---|---|
| CHIC numbered entries (catalog range #001-#331) | 331 |
| Inscriptions ingested | **302** |
| Distinct CHIC sign IDs observed | 131 |
| Total sign-token occurrences (clean + uncertain) | 1489 |
| Word-divider (`DIV`) tokens | 598 |
| Numeric quantity (`NUM:N`) tokens | 162 |
| Uncertain-reading (`[?:#NNN]`) tokens | 178 |
| Wholly-unknown (`[?]`) tokens | 208 |

Acceptance criterion (≥250 inscriptions): **met**.

### Known gaps in CHIC numbering (29 of 331 absent)

Missing CHIC numbers are entries where Younger's web edition carries only a commentary cross-reference, not a substantive transnumeration table. CHIC catalog numbering is also not fully contiguous in the print edition — some numbers are skipped or retired. Manual transcription from Olivier & Godart 1996 for these gaps is deferred to a future ticket.

Missing: #050, #094, #095, #096, #099, #100, #101, #102, #112, #114, #119, #122, #132, #139, #146, #147, #156, #164, #176, #185, #190, #192, #206, #222, #228, #230, #275, #292, #307.

### Sites
| Site | Inscriptions |
|---|---|
| Knossos | 95 |
| Mallia | 92 |
| Crete (unprovenanced) | 58 |
| Sitia | 6 |
| Mirabelo | 5 |
| Arkhanes | 4 |
| Palaikastro | 4 |
| Pyrgos (Myrtos) | 4 |
| Zakros | 4 |
| Lasithi | 3 |
| Samothrace | 3 |
| Mochlos | 2 |
| Ziros | 2 |
| Adromili | 1 |
| Avdou | 1 |
| Crete (seal/sealing, mixed sites) | 1 |
| Gortys | 1 |
| Haghia Triada | 1 |
| Heraklion | 1 |
| Kalo Horio | 1 |
| Kasteli | 1 |
| Kordakia | 1 |
| Kritsa | 1 |
| Kydonia | 1 |
| Lakonia | 1 |
| Lastros | 1 |
| Lithines | 1 |
| Neapolis | 1 |
| Phaistos | 1 |
| Pinakiano | 1 |
| Praisos | 1 |
| Prodromos | 1 |
| Xida | 1 |

### Supports
| Support | Inscriptions |
|---|---|
| seal | 126 |
| crescent | 49 |
| medallion | 34 |
| bar | 26 |
| sealing | 16 |
| lame | 15 |
| nodulus | 11 |
| chamaizi_vase | 8 |
| pithos | 3 |
| potsherd | 3 |
| tablet | 3 |
| cone | 2 |
| roundel | 2 |
| vase | 2 |
| offering_table | 1 |
| unknown | 1 |

### Transcription confidence
| Confidence | Inscriptions |
|---|---|
| clean | 167 |
| partial | 35 |
| fragmentary | 100 |

### Period (where stated in heading)
| Period | Inscriptions |
|---|---|
| (unstated) | 292 |
| EM III | 2 |
| MM I | 2 |
| MM IA-IB | 2 |
| MM IIB | 2 |
| MM IA | 1 |
| MM III | 1 |

Most CHIC inscriptions date to MM IIA-MM IIB; explicit per-entry dating is sparse in Younger's transnumeration. Per-inscription period inheritance from Olivier & Godart 1996 is deferred to chic-v1.

### Sources used (per-inscription provenance)
| Source | Inscriptions |
|---|---|
| younger_online | 302 |

### Top-30 most frequent sign IDs
| Sign | Count |
|---|---|
| #044 | 128 |
| #049 | 119 |
| #038 | 75 |
| #031 | 65 |
| #042 | 57 |
| #070 | 56 |
| #056 | 52 |
| #019 | 50 |
| #010 | 50 |
| #005 | 48 |
| #034 | 41 |
| #061 | 39 |
| #092 | 37 |
| #057 | 35 |
| #036 | 28 |
| #013 | 26 |
| #011 | 24 |
| #050 | 23 |
| #054 | 22 |
| #028 | 22 |
| #016 | 20 |
| #041 | 20 |
| #047 | 19 |
| #029 | 18 |
| #040 | 17 |
| #053 | 14 |
| #077 | 13 |
| #006 | 13 |
| #023 | 12 |
| #018 | 12 |

## Tokenization rules (chic-v0)

Documented as rules-as-data so that a future harness can re-run alternative tokenizations directly off the cached HTML in `.cache/younger_chic/` without re-scraping.

| Source (Younger transnumeration) | Token form | Notes |
|---|---|---|
| bare digit-group `NNN` | `#NNN` | Zero-padded to 3 digits. Preserves CHIC catalog convention #001-#100 (syllabographic), #101-#308 (logograms / ideograms / fractions). Classification deferred to chic-v1. |
| underlined `<u>NNN</u>` | `[?:#NNN]` | Younger marks doubtful readings of attested sign ids with underline. |
| asterisked `*NNN` | `#NNN` | Younger marks logogram-form ids with `*`; same numeric id, kept as `#NNN`. |
| damage marker `]NNN`, `[NNN`, `?` | `[?:#NNN]` if id known, else `[?]` | Bracket markers attach to the adjacent sign id. |
| bold quantity `<b>N...N</b>` | `NUM:N` | Numeric counts in administrative documents (e.g., `7000`). |
| literal `X` orientation marker | (skipped) | Decorative cross / writing-axis indicator, not a CHIC sign. |
| whitespace between sign-groups within a side | `DIV` | Word boundary. |
| between non-empty sides | `DIV` | Word boundary. |
| `vacat` row | (no tokens) | Empty side; no DIV emitted. |
| ideogram name (BOS, VAS, etc.) | (skipped) | Same sign carries a numeric id elsewhere in the row; `IDEO:<name>` extraction deferred to chic-v1. |

## Out of scope for chic-v0

- Logogram vs syllabographic sign filtering — chic-v1.
- Paleographic anchor inheritance from Linear A → chic-v2.
- Substrate framework application to CHIC corpus → chic-v3.
- Cross-script correlation analysis → chic-v4.
- Per-sign syllable-value extraction framework → chic-v5+.

