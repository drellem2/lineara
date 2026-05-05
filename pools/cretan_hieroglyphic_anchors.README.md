# Cretan Hieroglyphic paleographic anchors

Tier-1 / tier-2 paleographic anchors mapping CHIC syllabographic signs to Linear B carryover phonetic values via Linear A intermediaries. Built by chic-v2 (mg-362d) from chic-v1's (`mg-c7e3`) curated `PALEOGRAPHIC_CANDIDATES` list (`scripts/build_chic_signs.py`).

## Confidence tiers

- **tier-1** — paleographic similarity well-established (chic-v1 confidence=consensus) AND Linear B carryover stable.
- **tier-2** — paleographic similarity debated, or proposed in a single source (chic-v1 confidence in {proposed, debated}).

Linear B carryover is stable for every AB-id listed (the AB inventory's grid values are established under Ventris-Chadwick 1956), so the tier-1 / tier-2 split reduces to a paleographic-confidence collapse.

## Counts

- Total anchors: **20**
- Tier-1: **3** anchors, 141 corpus occurrences
- Tier-2: **17** anchors, 723 corpus occurrences
- CHIC inscriptions in the corpus: **302**

## Anchor list

| CHIC | Linear A | Linear B value | Tier | chic-v1 confidence | freq |
|------|----------|----------------|------|--------------------|------|
| #010 | AB57 | ja | tier-2 | proposed | 50 |
| #013 | AB03 | pa | tier-2 | debated | 26 |
| #016 | AB08 | a | tier-1 | consensus | 20 |
| #019 | AB44 | ke | tier-2 | debated | 50 |
| #025 | AB59 | ta | tier-2 | proposed | 11 |
| #028 | AB37 | ti | tier-2 | proposed | 22 |
| #031 | AB02 | ro | tier-1 | consensus | 65 |
| #038 | AB28 | i | tier-2 | debated | 75 |
| #041 | AB30 | ni | tier-2 | proposed | 20 |
| #042 | AB54 | wa | tier-2 | debated | 57 |
| #044 | AB67 | ki | tier-2 | debated | 128 |
| #049 | AB45 | de | tier-2 | debated | 119 |
| #053 | AB13 | me | tier-2 | proposed | 14 |
| #054 | AB23 | mu | tier-2 | proposed | 22 |
| #057 | AB46 | je | tier-2 | proposed | 35 |
| #061 | AB04 | te | tier-2 | proposed | 39 |
| #070 | AB60 | ra | tier-1 | consensus | 56 |
| #073 | AB05 | to | tier-2 | proposed | 5 |
| #077 | AB80 | ma | tier-2 | proposed | 13 |
| #092 | AB44 | ke | tier-2 | debated | 37 |

## Inheritance application convention

For each CHIC inscription's `tokens[]`, sign positions are walked and rendered:

- `#NNN` (clean) → if anchored, emit the phonetic value; else `#NNN`.
- `[?:#NNN]` (uncertain) → if anchored, `[?:VALUE]`; else `[?:#NNN]`.
- `DIV` → `/` (word-divider).
- `[?]` (illegible) → `[?]`.

Anchor coverage = anchored syllabographic positions / total syllabographic positions per chic-v1 classification (`pools/cretan_hieroglyphic_signs.yaml`). Ideogram, ambiguous, DIV, and illegible tokens are excluded from both numerator and denominator.

## Source citations

- Olivier, J.-P. & Godart, L. (1996). _CHIC._
- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._
- Salgarella, E. (2020). _Aegean Linear Script(s)._
- Decorte, R. (2017). _The First 'European' Writing._
- Civitillo, M. (2016). _La scrittura geroglifica minoica sui sigilli._
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
