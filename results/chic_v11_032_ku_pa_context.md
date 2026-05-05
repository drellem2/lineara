# CHIC `#032 -> ki` ku-pa context inspection (chic-v11; mg-d69c)

## Method

chic-v6 produced a tier-1 -> tier-2 verification lift of +3 inscriptions / +20 hits on the source-A scholar-proposed-Linear-A-readings test (`results/chic_verification_match_rates.md`). The portion of that lift attributable to `#032 -> ki` (combined with the chic-v2 anchor `#013 -> pa`) is the set of new tier-2 hits where the chic-v6 source-A match is on the literal/literal token pair `(#032, #013)` against scholar entries from the ku-pa name family / ka-pa transaction-term family attested in the four Linear A tablets HT 1, HT 16, HT 102, HT 110a (scholar entry IDs `kupa3_HT1`, `kupa_HT16`, `kapa_HT102`, `kupa_HT110a`).

This document does two mechanical inspections:

1. **Source Linear A context.** For each of the four Linear A source tablets, record the `genre_hint`, `support`, `period`, and `site` from the Linear A corpus (`corpus/all.jsonl`, v0). The chic-v6 source-A test takes the scholar's reading as a probe pattern; if the source tablet is an accountancy genre tablet, the scholarly reading `ku-pa` / `ka-pa` / `ku-pa3` is in its native context (the readings are the standard Younger-online-edition entries for accountancy / name-family / transaction-term elements on Hagia Triada tablets). If the source tablet is votive or unknown, the scholar's reading is less load-bearing as an accountancy probe.

2. **Matched CHIC inscription context.** For each CHIC inscription where the chic-v6 lift landed, render the partial reading with chic-v2 anchors + `#032 -> ki` applied (no class-placeholder extension), locate the position of the literal `(#032, #013)` token run within the inscription, and inspect whether the surrounding context — adjacent numerals, support type, DIV-bounded segment structure — is consistent with the kind of accountancy-formula structure that scholar readings like `ku-pa` / `ka-pa` are extracted from on the Linear A side.

**Determinism.** All inputs are committed; the procedure is a single pass over the chic-v6 experiments JSONL with literal filters on `scholar_entry_id`, `matched_signs`, `matched_kinds`, and `tier_level`. No RNG.

## Source Linear A tablet metadata

All four ku-pa-family scholar entries reference Linear A tablets at Haghia Triada. The tabulated metadata (from `corpus/all.jsonl`):

| Linear A id | site | support | genre_hint | period | n_signs | transcription_confidence | scholar entry id | scholar reading |
|---|---|---|---|---|---:|---|---|---|
| HT 1 | Haghia Triada | tablet | accountancy | LM IB | 18 | clean | `kupa3_HT1` | `ku-pa3` |
| HT 16 | Haghia Triada | tablet | accountancy | LM IB | 16 | clean | `kupa_HT16` | `ku-pa` |
| HT 102 | Haghia Triada | tablet | accountancy | LM IB | 22 | partial | `kapa_HT102` | `ka-pa` |
| HT 110a | Haghia Triada | tablet | accountancy | LM IB | 12 | partial | `kupa_HT110a` | `ku-pa` |

**Source-side verdict.** All four source Linear A tablets are **accountancy-genre tablets** (`genre_hint = accountancy`) on the **tablet** support type, dated to **LM IB**, from **Haghia Triada**. The scholarly readings `ku-pa` (name family / commodity prefix), `ku-pa3` (variant of the same family), and `ka-pa` (recurring transaction term) are exactly the kind of readings the Younger online edition extracts from Hagia Triada accountancy tablets, attested in their native-corpus genre. As a probe pattern for the chic-v6 source-A test, the readings are in their native context.

## Raw transliterations of the source Linear A tablets

Each tablet's `raw_transliteration` field, for direct inspection of the scholarly-reading position relative to numerals, logograms, and DIV breaks. (Numerical entries are denoted by the `LOG:` and `FRAC:` prefixes; AB syllabograms are the phonetic positions.)

- **HT 1** (accountancy, tablet, n_signs=18): `AB78-AB76-AB10 / AB67-AB02 / AB79-AB58 / AB07-AB07-AB17-AB44 / AB81-AB56-AB55 / AB08-AB60-AB06-AB27`
- **HT 16** (accountancy, tablet, n_signs=16): `AB77-AB81-AB03 / AB07-AB06-AB10 / FRAC:A705 / LOG:AB54 / FRAC:A702 / LOG:A604 / FRAC:A704 / FRAC:A705 / AB31-AB11 / LOG:AB74 / FRAC:A708`
- **HT 102** (accountancy, tablet, n_signs=22): `AB77-AB03 / AB31-AB76 / LOG:AB120 / AB56-AB30 / LOG:A574 / [?:A705] / LOG:AB100 / LOG:A574 / [?] / AB07-AB53-AB06 / AB80-AB79 / LOG:AB40 / AB28-AB77 / AB81-AB02`
- **HT 110a** (accountancy, tablet, n_signs=12): `AB41-AB51-AB34-AB81-AB73 / LOG:A626 / AB81-AB03 / AB81-AB02 / LOG:AB30 / [?]`

## CHIC inscriptions where the lift landed

chic-v6's tier-2 ku-pa-family lift via `#032 -> ki + #013 -> pa` (literal/literal `(#032, #013)`) lands on **1 CHIC inscription(s)** with **4 total scholar-entry hits** across the 4 ku-pa-family scholars. (The full chic-v6 tier-1 -> tier-2 lift of +3 inscriptions / +20 hits also includes a separate `(#032, #070)` family of k-r-onset matches against `ku-ro` / `ki-ro` / `ku-ra` / `ki-ra` / `ka-ru` scholar entries on a different inscription; that family is outside the ku-pa scope of this inspection.)

### CHIC #057

- **site**: Knossos
- **support**: bar
- **transcription_confidence**: partial
- **raw_transliteration**: `042-029-032-011 10 / X 079-032-013 20 | vacat / X 038-_054_-034 20 | vacat / X 011-029-037 50 | vacat`
- **n_tokens**: 24

**Partial reading (chic-v2 anchors + `#032 -> ki`):**

```
wa #029 ki #011 / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50
```

**Match position**: tokens 8..9 (the `(#032, #013)` literal pair, rendered as `ki pa` under the chic-v2 anchors + chic-v5 tier-2 override).

- before: `wa #029 ki #011 / NUM:10 / #079`
- **match**: `ki pa`
- after: `/ NUM:20 / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50`

**Immediate post-match token**: `NUM:20` (numerical entry; a positional structure consistent with **accountancy formula** — sign-run followed by a quantity).

**Scholar entries that contribute lift to this inscription**:

| scholar id | scholar reading | category | LA source | match kinds |
|---|---|---|---|---|
| `kupa3_HT1` | `ku-pa3` | name_family | HT 1 | literal/literal |
| `kupa_HT16` | `ku-pa` | name_family | HT 16 | literal/literal |
| `kapa_HT102` | `ka-pa` | transaction_term | HT 102 | literal/literal |
| `kupa_HT110a` | `ku-pa` | name_family | HT 110a | literal/literal |

## Combined verdict

- **Source-side context**: all 4 Linear A source tablets (HT 1, HT 16, HT 102, HT 110a) are accountancy-genre tablets at Haghia Triada (LM IB). The scholarly readings `ku-pa` / `ku-pa3` / `ka-pa` are in their native Hagia Triada accountancy-tablet context.
- **CHIC-side context**: the matched `(#032, #013)` token run is followed (after the immediate DIV break) by a numerical / logogram entry in at least one matched CHIC inscription. This is **the canonical accountancy-formula structure** (sign-run = entry, followed by a quantity / commodity) on which the Linear A scholar readings `ku-pa` / `ka-pa` are themselves extracted. The CHIC inscription's support type and DIV-bounded structure (per the per-inscription tables above) reinforce the accountancy reading.
- **Combined**: the chic-v6 ku-pa-family mechanical lift is **corroborated by inscription-level context on both sides of the match**: scholarly readings in their native LM IB Hagia Triada accountancy context on the Linear A source side; matched CHIC inscription with accountancy-consistent positional structure on the CHIC target side. **This is contextual corroboration of the chic-v6 mechanical lift specifically for `#032 -> ki`**, not validation of the chic-v5 framework as a whole — the chic-v9 framework-level negative (LOO accuracy 20.0%, 0/3 tier-2 unanimity correct) stands.

## Discipline notes

- **What this inspection does NOT do.** It does not run specialist judgment on whether `(#032 #013) = ki pa` is a plausible scribal Hieroglyph reading in CHIC #057's accountancy context — that is squarely out of polecat scope. It runs the mechanical metadata cross-check the brief asks for: do the scholar source tablets carry accountancy-genre metadata, and does the matched CHIC inscription exhibit accountancy-formula positional structure?
- **What this inspection does NOT lift.** The chic-v9 LOO framework-level accuracy (20.0% / 0/3 tier-2 correct) does not improve from contextual corroboration of a single candidate's mechanical-match lift. chic-v11 contextual corroboration of the chic-v6 ku-pa lift is the strongest additional evidence available within polecat scope for `#032 -> ki` specifically; it is consistent with the chic-v9 verdict that the framework's per-sign machinery is at-chance but is positive evidence axially restricted to the chic-v6 verification line for one candidate.

## Build provenance

- Generated by `scripts/build_chic_v11.py` (mg-d69c).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs: `corpus/all.jsonl` (Linear A v0); `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); `results/experiments.chic_verification_v0.jsonl` (chic-v6); `corpora/scholar_proposed_readings/all.jsonl` (v22).

## Citations

- Younger, J. G. (online). *Linear A texts in phonetic transcription* (retrieved 2026-05-04). Includes the `ku-pa` / `ku-pa3` / `ka-pa` Hagia Triada accountancy entries.
- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
