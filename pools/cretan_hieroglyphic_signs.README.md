# Cretan Hieroglyphic sign inventory — README

This README documents `pools/cretan_hieroglyphic_signs.yaml`, the per-sign
classification + metadata file for the CHIC corpus (mg-c7e3, chic-v1).

## What it is

A YAML file with one entry per distinct sign id observed in the CHIC
corpus (`corpora/cretan_hieroglyphic/all.jsonl`, mg-99df, chic-v0). Each
entry carries:

- `id` — CHIC catalog id (e.g., `#044`).
- `sign_class` — one of `syllabographic`, `ideogram`, `ambiguous`.
- `frequency` / `frequency_clean` / `frequency_uncertain` /
  `inscription_count` — corpus counts.
- `position_fingerprint` — fraction of occurrences in the start / middle /
  end third of the sign-only token sequence (the `single` bucket counts
  inscriptions whose sign-only sequence has length 1).
- `genre_fingerprint` — fraction of occurrences by inscription support
  type (seal, crescent, medallion, bar, sealing, ...; top 6).
- `paleographic_candidates` — optional, present where the sign has a
  documented visual continuity to a Linear A AB-sign with an established
  Linear B carryover value.
- `notes_from_olivier_godart` — catalog gloss for ideograms; ambiguity
  reason for ambiguous signs; empty for default-classified syllabograms.

Schema: `pools/schemas/chic_signs.v1.schema.json` (JSON Schema 2020-12).

## Classification rule (chic-v1)

Per the CHIC catalog convention (Olivier & Godart 1996, retained in
Younger's web edition), CHIC sign IDs are organized by numeric range:

| Range      | Default class    | Description                                   |
|------------|-----------------|-----------------------------------------------|
| #001-#100  | syllabographic   | The CHIC syllabogram repertoire (~96 catalogued, ~78-100 attested). |
| #101-#299  | ideogram         | Logograms / ideograms (BOS, OVIS, GRA, OLI, VIN, AROM, OLE, VAS). |
| #300-#399  | ideogram         | Numerals + fractions (CHIC #301-#308).         |

A per-sign exception list (`AMBIGUOUS_OVERRIDES` in
`scripts/build_chic_signs.py`) flags signs whose classification is
debated in the scholarly literature. **No overrides are applied at v1**:
the rule is purely numeric-range. The exception list is in place so
that chic-v3 (substrate-framework application) can populate it from a
fuller scholarly review. Per the ticket's caution:

> The classification is partly judgment-based. Be explicit about the
> rules used; do NOT silently call signs ideographic without evidence.
> The classification will be the foundation of all chic-v2+ work, so
> errors here propagate.

A handful of signs in the syllabographic range have well-known
iconographic content (e.g., #008 double-axe, #038 double-axe variant,
#044 trowel/gate). These are kept as syllabographic per O&G 1996, but
are flagged in the `paleographic_candidates` confidence field as
`debated` where applicable.

## What's in the corpus

| Metric | Count |
|--------|-------|
| Distinct sign IDs | **131** |
| Syllabographic | 96 |
| Ideogram | 35 |
| Ambiguous | 0 |
| Paleographic candidates (CHIC ↔ Linear A) | 20 |
| ↳ consensus | 3 |
| ↳ proposed | 10 |
| ↳ debated | 7 |

## Paleographic candidates

`paleographic_candidates` enumerates CHIC signs with documented visual
continuity to Linear A AB-signs that have established Linear B
carryover values. Each candidate is curated from one or more of:

- **Younger, J. G.** Online CHIC sign-list (offline since 2022; cached
  Wayback snapshot 20220703170656). Each Younger sign-list entry
  carries an "≈ Linear A AB-NN" annotation where the visual match is
  scholarly consensus.
- **Salgarella, E. (2020).** *Aegean Linear Script(s).* Cambridge.
  Table 5.3 (CHIC ↔ Linear A visual matches). The most-recent
  monograph-length treatment.
- **Decorte, R. (2017, 2018).** *The First 'European' Writing*; also
  Decorte's CHIC paleography papers.
- **Civitillo, M. (2016).** *La scrittura geroglifica minoica sui
  sigilli.* For the contested signs (#044, #008, #038).

Confidence levels:

| Confidence | Meaning |
|------------|---------|
| `consensus` | Multiple sources concur (Salgarella + Younger + Decorte). Suitable as a tier-1 anchor in chic-v2. |
| `proposed`  | Single primary source proposes the match. Treat as a candidate; do not promote to anchor without corroboration. |
| `debated`   | Match is asserted in some sources but rejected in others. Useful for negative-control work; not a v2 anchor. |

The candidates are committed in this file for transparency and for
chic-v2 (mechanical anchor inheritance). v1 does NOT apply them as
anchors.

## How to regenerate

```bash
python3 scripts/build_chic_signs.py
```

Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0).
Outputs: this directory's `cretan_hieroglyphic_signs.yaml` + the
two `results/` reports.

## Out of scope for chic-v1

- **Mechanical anchor inheritance** (apply paleographic candidates as
  tier-1 anchors, propagate readings) — chic-v2.
- **Substrate framework application** to CHIC syllabographic subset —
  chic-v3.
- **Per-sign value extraction framework** — chic-v5+.
- **Cross-script correlation analysis** — chic-v4.
- **Visual paleography work** beyond enumeration of scholarly-curated
  candidates — out of scope; the framework treats CHIC sign IDs as
  opaque tokens.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum
  Inscriptionum Cretae* (Études Crétoises 31). Paris. **Print only;
  not available online.** The canonical CHIC catalog.
- Younger, J. G. *The Cretan Hieroglyphic Texts: a web edition of CHIC
  with commentary.* Originally `people.ku.edu/~jyounger/Hiero/`;
  fetched from Wayback Machine snapshot 20220703170656.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge UP.
- Decorte, R. (2017). "The First 'European' Writing: Redefining the
  Archanes Script." *Oxford Journal of Archaeology* 36 (4).
- Decorte, R. (2018). "Cretan Hieroglyphic and the Nature of Script."
  In *Paths into Script Formation in the Ancient Mediterranean.*
- Civitillo, M. (2016). *La scrittura geroglifica minoica sui sigilli.*
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.*
  Cambridge UP. The basis of all Linear A → Linear B carryover values.
- Schoep, I. (2002). *The Administration of Neopalatial Crete.*
- Palmer, L. (1995). "ku-ro and ki-ro in Linear A."
