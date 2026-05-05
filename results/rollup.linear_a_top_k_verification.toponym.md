# Linear A top-K verification — pool=toponym (mg-c202)

v26 mechanical verification of the v10/v18/v21 leaderboard top-20 substrate surfaces for the **toponym** pool. Built by `scripts/build_linear_a_v26.py`. Methodology mirrors chic-v6 (mg-a557) verbatim — three pre-registered match sources, no post-hoc relaxation. The candidate-value source is the per-pool leaderboard top-20 (substrate side) rather than the chic-v5 tier-2 specific-phoneme override set; the corpus is Linear A (`corpus/all.jsonl`) rather than CHIC.

## Pre-registered match criteria (chic-v6 verbatim)

- **Source A.** Scholar-proposed Linear-A reading match. A scholar entry's `ab_sequence` (length k) matches a Linear A inscription iff there exists a contiguous run of k literal-anchored syllabographic events within a single DIV-bounded segment such that for each position i, the literal phoneme value's first character equals the scholar's `scholarly_first_phoneme[i]`.
- **Source B.** Toponym substring match (`pools/toponym.yaml`, length L ∈ [3, 5]).
- **Source C.** Item-location consistency. Per-inscription `site` field (lowercased; alphabetical chars only); substrings length 3..5; matched against the inscription's own phoneme stream.

## Candidate-value source — pool top-20 substrate surfaces

| rank | surface |
|---:|:--|
| 1 | `aksos` |
| 2 | `aso` |
| 3 | `assos` |
| 4 | `kno` |
| 5 | `lukia` |
| 6 | `tarra` |
| 7 | `ala` |
| 8 | `iassos` |
| 9 | `itanos` |
| 10 | `keos` |
| 11 | `lebena` |
| 12 | `naxos` |
| 13 | `andos` |
| 14 | `minoa` |
| 15 | `kuzikos` |
| 16 | `mnos` |
| 17 | `aspendos` |
| 18 | `tenos` |
| 19 | `aios` |
| 20 | `lykabettos` |

## Per-pool aggregate

Inputs: 772 Linear A inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| metric | value |
|:--|--:|
| n top-20 surfaces with ≥1 positive paired-diff record | 20 |
| n positive paired-diff records (post-filter) | 751 |
| n distinct inscriptions extended | 39 |
| n distinct inscriptions with ≥1 source-A/B/C match | 39 |
| match rate (over extended inscriptions) | 1.0000 |
| total source-A hits | 4527 |
| total source-B hits | 9794 |
| total source-C hits | 203 |
| total a+b+c hits | 14524 |

## Per-surface verification status

| rank | surface | n records | n inscriptions extended | n inscriptions w/ match | a hits | b hits | c hits | status |
|---:|:--|---:|---:|---:|---:|---:|---:|:--|
| 1 | `aksos` | 50 | 24 | 24 | 196 | 983 | 22 | verified |
| 2 | `aso` | 50 | 12 | 12 | 391 | 119 | 3 | verified |
| 3 | `assos` | 50 | 24 | 24 | 172 | 2260 | 60 | verified |
| 4 | `kno` | 50 | 12 | 12 | 418 | 139 | 3 | verified |
| 5 | `lukia` | 50 | 24 | 24 | 184 | 323 | 1 | verified |
| 6 | `tarra` | 50 | 24 | 24 | 313 | 427 | 1 | verified |
| 7 | `ala` | 49 | 12 | 12 | 383 | 174 | 3 | verified |
| 8 | `iassos` | 24 | 9 | 9 | 49 | 1025 | 41 | verified |
| 9 | `itanos` | 24 | 9 | 9 | 51 | 316 | 15 | verified |
| 10 | `keos` | 49 | 21 | 21 | 593 | 260 | 5 | verified |
| 11 | `lebena` | 24 | 9 | 9 | 49 | 231 | 0 | verified |
| 12 | `naxos` | 24 | 9 | 8 | 61 | 426 | 15 | verified |
| 13 | `andos` | 48 | 24 | 24 | 174 | 622 | 1 | verified |
| 14 | `minoa` | 48 | 24 | 24 | 176 | 468 | 1 | verified |
| 15 | `kuzikos` | 13 | 3 | 3 | 28 | 124 | 1 | verified |
| 16 | `mnos` | 46 | 20 | 20 | 606 | 718 | 5 | verified |
| 17 | `aspendos` | 8 | 2 | 2 | 12 | 118 | 1 | verified |
| 18 | `tenos` | 45 | 23 | 23 | 162 | 626 | 19 | verified |
| 19 | `aios` | 44 | 19 | 18 | 503 | 287 | 5 | verified |
| 20 | `lykabettos` | 5 | 1 | 1 | 6 | 148 | 1 | verified |

## Inverse-verification (sign-level contradictions vs scholar set)

Substrate hypothesis proposes phoneme value at an AB sign covered by a scholar-proposed reading at the same span; the first character of the substrate proposal differs from the scholar's. This is **negative evidence** at the sign level — the substrate proposal disagrees with the published scholarly proposal.

| pool | surface | inscription | scholar entry | AB sign | substrate proposed | scholar first phoneme | scholarly CV |
|:--|:--|:--|:--|:--|:--|:--|:--|
| toponym | `aios` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `aios` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |
| toponym | `aksos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `ala` | ARKH 5 | tana_ARKH5 | AB59 | `l` | `t` | `ta` |
| toponym | `ala` | HT 108 | tana_HT108 | AB59 | `l` | `t` | `ta` |
| toponym | `andos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `aso` | ARKH 5 | tana_ARKH5 | AB59 | `s` | `t` | `ta` |
| toponym | `aso` | HT 108 | tana_HT108 | AB59 | `s` | `t` | `ta` |
| toponym | `assos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `keos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `keos` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |
| toponym | `kno` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| toponym | `kno` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| toponym | `lukia` | ARKH 5 | tana_ARKH5 | AB59 | `i` | `t` | `ta` |
| toponym | `minoa` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `mnos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| toponym | `mnos` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |
| toponym | `tarra` | ARKH 5 | tana_ARKH5 | AB59 | `r` | `t` | `ta` |
| toponym | `tenos` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |

## First-match enumeration (up to 3 inscriptions per surface)

| surface | inscription | n_a | n_b | n_c |
|:--|:--|---:|---:|---:|
| `aksos` | ARKH 2 | 12 | 0 | 0 |
| `aksos` | ARKH 2 | 12 | 22 | 0 |
| `aksos` | ARKH 5 | 1 | 23 | 0 |
| `aso` | ARKH 1a | 2 | 2 | 0 |
| `aso` | ARKH 1a | 2 | 2 | 0 |
| `aso` | ARKH 1a | 2 | 2 | 0 |
| `assos` | ARKH 2 | 12 | 52 | 0 |
| `assos` | ARKH 2 | 12 | 0 | 0 |
| `assos` | ARKH 5 | 1 | 53 | 0 |
| `kno` | ARKH 1a | 2 | 3 | 0 |
| `kno` | ARKH 1a | 2 | 3 | 0 |
| `kno` | ARKH 1a | 2 | 3 | 0 |
| `lukia` | ARKH 2 | 12 | 0 | 0 |
| `lukia` | ARKH 2 | 12 | 7 | 0 |
| `lukia` | ARKH 5 | 1 | 7 | 0 |
| `tarra` | ARKH 2 | 12 | 0 | 0 |
| `tarra` | ARKH 2 | 16 | 9 | 0 |
| `tarra` | ARKH 5 | 3 | 9 | 0 |
| `ala` | ARKH 1a | 2 | 4 | 0 |
| `ala` | ARKH 1a | 2 | 5 | 0 |
| `ala` | ARKH 1a | 2 | 4 | 0 |
| `iassos` | GO Wc 1a | 0 | 55 | 0 |
| `iassos` | HT 122b | 25 | 55 | 0 |
| `iassos` | HT 95a | 2 | 55 | 0 |
| `itanos` | GO Wc 1a | 0 | 16 | 0 |
| `itanos` | HT 122b | 25 | 16 | 0 |
| `itanos` | HT 95a | 2 | 16 | 0 |
| `keos` | ARKH 1a | 17 | 3 | 0 |
| `keos` | ARKH 1a | 2 | 4 | 0 |
| `keos` | ARKH 2 | 12 | 0 | 0 |
| `lebena` | GO Wc 1a | 0 | 11 | 0 |
| `lebena` | HT 122b | 25 | 11 | 0 |
| `lebena` | HT 95a | 2 | 11 | 0 |
| `naxos` | GO Wc 1a | 0 | 22 | 0 |
| `naxos` | HT 122b | 25 | 22 | 0 |
| `naxos` | HT 95a | 2 | 22 | 0 |
| `andos` | ARKH 2 | 12 | 14 | 0 |
| `andos` | ARKH 2 | 12 | 0 | 0 |
| `andos` | ARKH 5 | 1 | 15 | 0 |
| `minoa` | ARKH 2 | 12 | 0 | 0 |
| `minoa` | ARKH 2 | 12 | 13 | 0 |
| `minoa` | ARKH 5 | 1 | 10 | 0 |
| `kuzikos` | KN Zc 6 | 0 | 8 | 0 |
| `kuzikos` | KN Zc 6 | 0 | 12 | 0 |
| `kuzikos` | KN Zc 7 | 0 | 14 | 0 |
| `mnos` | ARKH 1a | 2 | 14 | 0 |
| `mnos` | ARKH 1a | 4 | 15 | 0 |
| `mnos` | ARKH 2 | 12 | 0 | 0 |
| `aspendos` | KN Zc 7 | 0 | 21 | 0 |
| `aspendos` | KN Zf 13 | 2 | 18 | 0 |
| `aspendos` | KN Zf 13 | 2 | 17 | 1 |
| `tenos` | ARKH 2 | 12 | 0 | 0 |
| `tenos` | ARKH 5 | 1 | 16 | 0 |
| `tenos` | GO Wc 1a | 0 | 17 | 0 |
| `aios` | ARKH 1a | 2 | 5 | 0 |
| `aios` | ARKH 1a | 2 | 5 | 0 |
| `aios` | ARKH 2 | 12 | 4 | 0 |
| `lykabettos` | KN Zf 13 | 0 | 29 | 0 |
| `lykabettos` | KN Zf 13 | 2 | 32 | 1 |
| `lykabettos` | KN Zf 13 | 0 | 20 | 0 |

## Determinism

- No RNG. Same (Linear A corpus, linear_b_carryover.yaml, leaderboard markdown for this pool, manifests, hypothesis YAMLs, scholar set, toponym pool) → byte-identical output.
- Tie-breaking is alphabetical / lexicographic throughout.

## Citations

- Younger, J. G. (online). _Linear A texts in phonetic transcription._
- Olivier, J.-P. & Godart, L. (1996). _CHIC._
- Salgarella, E. (2020). _Aegean Linear Script(s)._
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
- Beekes, R. S. P. (2010). _Etymological Dictionary of Greek._ (Pre-Greek substrate appendix.)
- Furnée, E. J. (1972). _Die wichtigsten konsonantischen Erscheinungen des Vorgriechischen._
