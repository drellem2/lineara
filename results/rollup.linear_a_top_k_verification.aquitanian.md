# Linear A top-K verification — pool=aquitanian (mg-c202)

v26 mechanical verification of the v10/v18/v21 leaderboard top-20 substrate surfaces for the **aquitanian** pool. Built by `scripts/build_linear_a_v26.py`. Methodology mirrors chic-v6 (mg-a557) verbatim — three pre-registered match sources, no post-hoc relaxation. The candidate-value source is the per-pool leaderboard top-20 (substrate side) rather than the chic-v5 tier-2 specific-phoneme override set; the corpus is Linear A (`corpus/all.jsonl`) rather than CHIC.

## Pre-registered match criteria (chic-v6 verbatim)

- **Source A.** Scholar-proposed Linear-A reading match. A scholar entry's `ab_sequence` (length k) matches a Linear A inscription iff there exists a contiguous run of k literal-anchored syllabographic events within a single DIV-bounded segment such that for each position i, the literal phoneme value's first character equals the scholar's `scholarly_first_phoneme[i]`.
- **Source B.** Toponym substring match (`pools/toponym.yaml`, length L ∈ [3, 5]).
- **Source C.** Item-location consistency. Per-inscription `site` field (lowercased; alphabetical chars only); substrings length 3..5; matched against the inscription's own phoneme stream.

## Candidate-value source — pool top-20 substrate surfaces

| rank | surface |
|---:|:--|
| 1 | `aitz` |
| 2 | `hanna` |
| 3 | `nahi` |
| 4 | `ako` |
| 5 | `beltz` |
| 6 | `bihotz` |
| 7 | `egun` |
| 8 | `eki` |
| 9 | `ezti` |
| 10 | `gaitz` |
| 11 | `hau` |
| 12 | `hesi` |
| 13 | `itsaso` |
| 14 | `oin` |
| 15 | `ona` |
| 16 | `zelai` |
| 17 | `zortzi` |
| 18 | `argi` |
| 19 | `ate` |
| 20 | `entzun` |

## Per-pool aggregate

Inputs: 772 Linear A inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| metric | value |
|:--|--:|
| n top-20 surfaces with ≥1 positive paired-diff record | 20 |
| n positive paired-diff records (post-filter) | 1005 |
| n distinct inscriptions extended | 40 |
| n distinct inscriptions with ≥1 source-A/B/C match | 38 |
| match rate (over extended inscriptions) | 0.9500 |
| total source-A hits | 7808 |
| total source-B hits | 1790 |
| total source-C hits | 69 |
| total a+b+c hits | 9667 |

## Per-surface verification status

| rank | surface | n records | n inscriptions extended | n inscriptions w/ match | a hits | b hits | c hits | status |
|---:|:--|---:|---:|---:|---:|---:|---:|:--|
| 1 | `aitz` | 53 | 12 | 9 | 445 | 40 | 3 | verified |
| 2 | `hanna` | 51 | 24 | 19 | 179 | 62 | 6 | verified |
| 3 | `nahi` | 51 | 22 | 14 | 532 | 127 | 5 | verified |
| 4 | `ako` | 50 | 12 | 9 | 391 | 32 | 3 | verified |
| 5 | `beltz` | 50 | 21 | 14 | 513 | 131 | 5 | verified |
| 6 | `bihotz` | 50 | 24 | 13 | 172 | 50 | 1 | verified |
| 7 | `egun` | 50 | 21 | 15 | 511 | 126 | 5 | verified |
| 8 | `eki` | 50 | 12 | 10 | 399 | 49 | 3 | verified |
| 9 | `ezti` | 50 | 21 | 21 | 617 | 131 | 5 | verified |
| 10 | `gaitz` | 50 | 21 | 14 | 519 | 119 | 5 | verified |
| 11 | `hau` | 50 | 12 | 9 | 389 | 32 | 3 | verified |
| 12 | `hesi` | 50 | 21 | 20 | 507 | 172 | 5 | verified |
| 13 | `itsaso` | 50 | 24 | 23 | 174 | 153 | 2 | verified |
| 14 | `oin` | 50 | 12 | 10 | 390 | 41 | 3 | verified |
| 15 | `ona` | 50 | 12 | 10 | 393 | 44 | 3 | verified |
| 16 | `zelai` | 50 | 24 | 15 | 176 | 61 | 1 | verified |
| 17 | `zortzi` | 50 | 24 | 24 | 266 | 105 | 1 | verified |
| 18 | `argi` | 51 | 22 | 21 | 665 | 194 | 5 | verified |
| 19 | `ate` | 50 | 12 | 10 | 395 | 51 | 4 | verified |
| 20 | `entzun` | 49 | 24 | 15 | 175 | 70 | 1 | verified |

## Inverse-verification (sign-level contradictions vs scholar set)

Substrate hypothesis proposes phoneme value at an AB sign covered by a scholar-proposed reading at the same span; the first character of the substrate proposal differs from the scholar's. This is **negative evidence** at the sign level — the substrate proposal disagrees with the published scholarly proposal.

| pool | surface | inscription | scholar entry | AB sign | substrate proposed | scholar first phoneme | scholarly CV |
|:--|:--|:--|:--|:--|:--|:--|:--|
| aquitanian | `aitz` | ARKH 5 | tana_ARKH5 | AB59 | `i` | `t` | `ta` |
| aquitanian | `aitz` | HT 108 | tana_HT108 | AB59 | `i` | `t` | `ta` |
| aquitanian | `ako` | ARKH 5 | tana_ARKH5 | AB59 | `c` | `t` | `ta` |
| aquitanian | `ako` | HT 108 | tana_HT108 | AB59 | `c` | `t` | `ta` |
| aquitanian | `argi` | ARKH 5 | tana_ARKH5 | AB59 | `g` | `t` | `ta` |
| aquitanian | `argi` | HT 108 | tana_HT108 | AB59 | `g` | `t` | `ta` |
| aquitanian | `beltz` | ARKH 5 | tana_ARKH5 | AB59 | `l` | `t` | `ta` |
| aquitanian | `beltz` | HT 108 | tana_HT108 | AB59 | `l` | `t` | `ta` |
| aquitanian | `bihotz` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| aquitanian | `egun` | ARKH 5 | tana_ARKH5 | AB59 | `u` | `t` | `ta` |
| aquitanian | `egun` | HT 108 | tana_HT108 | AB59 | `u` | `t` | `ta` |
| aquitanian | `eki` | ARKH 5 | tana_ARKH5 | AB59 | `k` | `t` | `ta` |
| aquitanian | `eki` | HT 108 | tana_HT108 | AB59 | `k` | `t` | `ta` |
| aquitanian | `entzun` | ARKH 5 | tana_ARKH5 | AB59 | `u` | `t` | `ta` |
| aquitanian | `gaitz` | ARKH 5 | tana_ARKH5 | AB59 | `i` | `t` | `ta` |
| aquitanian | `gaitz` | HT 108 | tana_HT108 | AB59 | `i` | `t` | `ta` |
| aquitanian | `hanna` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| aquitanian | `hau` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| aquitanian | `hau` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| aquitanian | `hesi` | ARKH 5 | tana_ARKH5 | AB59 | `s` | `t` | `ta` |
| aquitanian | `hesi` | HT 108 | tana_HT108 | AB59 | `s` | `t` | `ta` |
| aquitanian | `itsaso` | ARKH 5 | tana_ARKH5 | AB59 | `s` | `t` | `ta` |
| aquitanian | `nahi` | ARKH 5 | tana_ARKH5 | AB59 | `h` | `t` | `ta` |
| aquitanian | `nahi` | HT 108 | tana_HT108 | AB59 | `h` | `t` | `ta` |
| aquitanian | `oin` | ARKH 5 | tana_ARKH5 | AB59 | `i` | `t` | `ta` |
| aquitanian | `oin` | HT 108 | tana_HT108 | AB59 | `i` | `t` | `ta` |
| aquitanian | `ona` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| aquitanian | `ona` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| aquitanian | `zelai` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |

## First-match enumeration (up to 3 inscriptions per surface)

| surface | inscription | n_a | n_b | n_c |
|:--|:--|---:|---:|---:|
| `aitz` | ARKH 1a | 2 | 1 | 0 |
| `aitz` | ARKH 1a | 2 | 1 | 0 |
| `aitz` | ARKH 1a | 2 | 2 | 0 |
| `hanna` | ARKH 2 | 12 | 1 | 1 |
| `hanna` | ARKH 2 | 12 | 0 | 0 |
| `hanna` | ARKH 5 | 1 | 1 | 1 |
| `nahi` | ARKH 1a | 2 | 1 | 0 |
| `nahi` | ARKH 2 | 12 | 0 | 0 |
| `nahi` | ARKH 2 | 12 | 0 | 0 |
| `ako` | ARKH 1a | 2 | 1 | 0 |
| `ako` | ARKH 1a | 2 | 1 | 0 |
| `ako` | ARKH 1a | 2 | 1 | 0 |
| `beltz` | ARKH 1a | 2 | 1 | 0 |
| `beltz` | ARKH 2 | 12 | 0 | 0 |
| `beltz` | ARKH 2 | 14 | 0 | 0 |
| `bihotz` | ARKH 2 | 12 | 0 | 0 |
| `bihotz` | ARKH 2 | 12 | 0 | 0 |
| `bihotz` | ARKH 5 | 1 | 1 | 0 |
| `egun` | ARKH 1a | 0 | 4 | 0 |
| `egun` | ARKH 1a | 2 | 1 | 0 |
| `egun` | ARKH 2 | 12 | 0 | 0 |
| `eki` | ARKH 1a | 2 | 1 | 0 |
| `eki` | ARKH 1a | 0 | 4 | 0 |
| `eki` | ARKH 1a | 2 | 1 | 0 |
| `ezti` | ARKH 1a | 4 | 1 | 0 |
| `ezti` | ARKH 1a | 2 | 3 | 0 |
| `ezti` | ARKH 2 | 12 | 0 | 0 |
| `gaitz` | ARKH 1a | 0 | 1 | 0 |
| `gaitz` | ARKH 1a | 2 | 1 | 0 |
| `gaitz` | ARKH 2 | 12 | 0 | 0 |
| `hau` | ARKH 1a | 0 | 1 | 0 |
| `hau` | ARKH 1a | 2 | 1 | 0 |
| `hau` | ARKH 1a | 2 | 2 | 0 |
| `hesi` | ARKH 1a | 2 | 2 | 0 |
| `hesi` | ARKH 1a | 0 | 1 | 0 |
| `hesi` | ARKH 2 | 12 | 1 | 0 |
| `itsaso` | ARKH 2 | 12 | 1 | 0 |
| `itsaso` | ARKH 2 | 12 | 0 | 0 |
| `itsaso` | ARKH 5 | 1 | 3 | 0 |
| `oin` | ARKH 1a | 2 | 1 | 0 |
| `oin` | ARKH 1a | 2 | 2 | 0 |
| `oin` | ARKH 1a | 2 | 1 | 0 |
| `ona` | ARKH 1a | 2 | 2 | 0 |
| `ona` | ARKH 1a | 0 | 1 | 0 |
| `ona` | ARKH 1a | 2 | 1 | 0 |
| `zelai` | ARKH 2 | 12 | 0 | 0 |
| `zelai` | ARKH 2 | 12 | 0 | 0 |
| `zelai` | ARKH 5 | 1 | 1 | 0 |
| `zortzi` | ARKH 2 | 14 | 1 | 0 |
| `zortzi` | ARKH 2 | 12 | 0 | 0 |
| `zortzi` | ARKH 5 | 3 | 2 | 0 |
| `argi` | ARKH 1a | 4 | 2 | 0 |
| `argi` | ARKH 1a | 4 | 2 | 0 |
| `argi` | ARKH 2 | 12 | 0 | 0 |
| `ate` | ARKH 1a | 2 | 1 | 0 |
| `ate` | ARKH 1a | 2 | 1 | 0 |
| `ate` | ARKH 1a | 2 | 1 | 0 |
| `entzun` | ARKH 2 | 12 | 0 | 0 |
| `entzun` | ARKH 2 | 12 | 0 | 0 |
| `entzun` | ARKH 5 | 1 | 1 | 0 |

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
