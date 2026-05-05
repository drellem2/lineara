# CHIC anchor-density leaderboard, top-30 (chic-v2; mg-362d)

Top-K most-anchored CHIC inscriptions, ranked by `anchor_coverage_rate` (anchored syllabographic positions / total syllabographic positions). Tiebreakers: anchored count (desc), then syllabographic count (desc), then CHIC id (asc).

These are the inscriptions chic-v3+ work has the most existing constraint to leverage — the natural starting population for substrate framework application and per-sign-value extraction. Built by `scripts/build_chic_anchors.py`.

## Leaderboard

| Rank | CHIC id | Site | Support | conf | n_syll | n_anch | coverage | partial reading |
|--:|---|---|---|---|--:|--:|--:|---|
| 1 | CHIC #293 | Adromili | seal | partial | 10 | 10 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| 2 | CHIC #270 | Lasithi | seal | clean | 8 | 8 | 1.0000 | `ra i / ki de / i ro ja te` |
| 3 | CHIC #284 | Crete (unprovenanced) | seal | clean | 5 | 5 | 1.0000 | `ki de / i ja ro` |
| 4 | CHIC #207 | Mallia | seal | fragmentary | 4 | 4 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| 5 | CHIC #249 | Sitia | seal | clean | 4 | 4 | 1.0000 | `i ja / ki de` |
| 6 | CHIC #011 | Knossos | crescent | fragmentary | 3 | 3 | 1.0000 | `de de / [?:ti] / [?]` |
| 7 | CHIC #069 | Knossos | tablet | fragmentary | 3 | 3 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| 8 | CHIC #133 | Pyrgos (Myrtos) | vase | clean | 3 | 3 | 1.0000 | `ra ti ni / NUM:0` |
| 9 | CHIC #162 | Knossos | crescent | clean | 3 | 3 | 1.0000 | `i ja ro` |
| 10 | CHIC #163 | Knossos | crescent | clean | 3 | 3 | 1.0000 | `wa ra i` |
| 11 | CHIC #167 | Knossos | crescent | clean | 3 | 3 | 1.0000 | `de ra ra` |
| 12 | CHIC #169 | Knossos | sealing | clean | 3 | 3 | 1.0000 | `i ja ro` |
| 13 | CHIC #172 | Mallia | crescent | clean | 3 | 3 | 1.0000 | `ja ke ti` |
| 14 | CHIC #179 | Knossos | sealing | fragmentary | 3 | 3 | 1.0000 | `wa ke / ke [?]` |
| 15 | CHIC #184 | Crete (unprovenanced) | seal | clean | 3 | 3 | 1.0000 | `ki pa ra` |
| 16 | CHIC #195 | Crete (unprovenanced) | seal | clean | 3 | 3 | 1.0000 | `i ja ro` |
| 17 | CHIC #218 | Crete (unprovenanced) | seal | clean | 3 | 3 | 1.0000 | `i ja ro` |
| 18 | CHIC #279 | Crete (unprovenanced) | seal | clean | 3 | 3 | 1.0000 | `i ja ro` |
| 19 | CHIC #012 | Knossos | crescent | fragmentary | 2 | 2 | 1.0000 | `[?] / ti de [?]` |
| 20 | CHIC #035 | Knossos | medallion | fragmentary | 2 | 2 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| 21 | CHIC #081 | Mallia | medallion | clean | 2 | 2 | 1.0000 | `ti ra` |
| 22 | CHIC #088 | Mallia | lame | fragmentary | 2 | 2 | 1.0000 | `[?:ro] ni` |
| 23 | CHIC #106 | Mallia | lame | fragmentary | 2 | 2 | 1.0000 | `[?:pa] de` |
| 24 | CHIC #134 | Knossos | sealing | clean | 2 | 2 | 1.0000 | `wa ke` |
| 25 | CHIC #135 | Samothrace | roundel | clean | 2 | 2 | 1.0000 | `wa ke` |
| 26 | CHIC #136 | Samothrace | roundel | clean | 2 | 2 | 1.0000 | `wa ke` |
| 27 | CHIC #137 | Samothrace | nodulus | clean | 2 | 2 | 1.0000 | `wa ke` |
| 28 | CHIC #150 | Mallia | sealing | clean | 2 | 2 | 1.0000 | `ki de` |
| 29 | CHIC #151 | Phaistos | sealing | clean | 2 | 2 | 1.0000 | `wa me` |
| 30 | CHIC #152 | Zakros | sealing | clean | 2 | 2 | 1.0000 | `mu ki` |

## Sanity checks

- Top-1 coverage: **1.0000** (CHIC #293).
- Top-30 coverage cutoff: **1.0000** (CHIC #152).
- Inscriptions in top-30 with full anchor coverage (≥0.999): **30**.
- Total inscriptions with ≥1 anchored position: **263** of 302.
