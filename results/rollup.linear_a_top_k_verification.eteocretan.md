# Linear A top-K verification — pool=eteocretan (mg-c202)

v26 mechanical verification of the v10/v18/v21 leaderboard top-20 substrate surfaces for the **eteocretan** pool. Built by `scripts/build_linear_a_v26.py`. Methodology mirrors chic-v6 (mg-a557) verbatim — three pre-registered match sources, no post-hoc relaxation. The candidate-value source is the per-pool leaderboard top-20 (substrate side) rather than the chic-v5 tier-2 specific-phoneme override set; the corpus is Linear A (`corpus/all.jsonl`) rather than CHIC.

## Pre-registered match criteria (chic-v6 verbatim)

- **Source A.** Scholar-proposed Linear-A reading match. A scholar entry's `ab_sequence` (length k) matches a Linear A inscription iff there exists a contiguous run of k literal-anchored syllabographic events within a single DIV-bounded segment such that for each position i, the literal phoneme value's first character equals the scholar's `scholarly_first_phoneme[i]`.
- **Source B.** Toponym substring match (`pools/toponym.yaml`, length L ∈ [3, 5]).
- **Source C.** Item-location consistency. Per-inscription `site` field (lowercased; alphabetical chars only); substrings length 3..5; matched against the inscription's own phoneme stream.

## Candidate-value source — pool top-20 substrate surfaces

| rank | surface |
|---:|:--|
| 1 | `iar` |
| 2 | `iarei` |
| 3 | `ine` |
| 4 | `isala` |
| 5 | `mi` |
| 6 | `noi` |
| 7 | `os` |
| 8 | `sam` |
| 9 | `si` |
| 10 | `wai` |
| 11 | `des` |
| 12 | `ona` |
| 13 | `wantai` |
| 14 | `arka` |
| 15 | `dioi` |
| 16 | `iareion` |
| 17 | `netamoi` |
| 18 | `ier` |
| 19 | `wow` |
| 20 | `epimere` |

## Per-pool aggregate

Inputs: 772 Linear A inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| metric | value |
|:--|--:|
| n top-20 surfaces with ≥1 positive paired-diff record | 20 |
| n positive paired-diff records (post-filter) | 849 |
| n distinct inscriptions extended | 42 |
| n distinct inscriptions with ≥1 source-A/B/C match | 37 |
| match rate (over extended inscriptions) | 0.8810 |
| total source-A hits | 6030 |
| total source-B hits | 1513 |
| total source-C hits | 47 |
| total a+b+c hits | 7590 |

## Per-surface verification status

| rank | surface | n records | n inscriptions extended | n inscriptions w/ match | a hits | b hits | c hits | status |
|---:|:--|---:|---:|---:|---:|---:|---:|:--|
| 1 | `iar` | 50 | 12 | 12 | 500 | 97 | 3 | verified |
| 2 | `iarei` | 50 | 24 | 24 | 278 | 107 | 1 | verified |
| 3 | `ine` | 50 | 12 | 10 | 391 | 48 | 3 | verified |
| 4 | `isala` | 50 | 24 | 24 | 172 | 314 | 1 | verified |
| 5 | `mi` | 50 | 9 | 5 | 230 | 47 | 0 | verified |
| 6 | `noi` | 50 | 12 | 10 | 398 | 66 | 3 | verified |
| 7 | `os` | 50 | 9 | 5 | 228 | 28 | 0 | verified |
| 8 | `sam` | 50 | 12 | 12 | 401 | 111 | 3 | verified |
| 9 | `si` | 50 | 9 | 4 | 228 | 29 | 0 | verified |
| 10 | `wai` | 50 | 12 | 10 | 389 | 42 | 3 | verified |
| 11 | `des` | 49 | 12 | 9 | 379 | 41 | 3 | verified |
| 12 | `ona` | 49 | 12 | 10 | 381 | 42 | 3 | verified |
| 13 | `wantai` | 24 | 9 | 8 | 55 | 47 | 0 | verified |
| 14 | `arka` | 48 | 21 | 20 | 701 | 148 | 13 | verified |
| 15 | `dioi` | 48 | 21 | 14 | 501 | 122 | 5 | verified |
| 16 | `iareion` | 13 | 3 | 3 | 46 | 34 | 0 | verified |
| 17 | `netamoi` | 13 | 3 | 3 | 22 | 33 | 0 | verified |
| 18 | `ier` | 47 | 12 | 12 | 366 | 102 | 3 | verified |
| 19 | `wow` | 46 | 12 | 9 | 346 | 25 | 3 | verified |
| 20 | `epimere` | 12 | 3 | 3 | 18 | 30 | 0 | verified |

## Inverse-verification (sign-level contradictions vs scholar set)

Substrate hypothesis proposes phoneme value at an AB sign covered by a scholar-proposed reading at the same span; the first character of the substrate proposal differs from the scholar's. This is **negative evidence** at the sign level — the substrate proposal disagrees with the published scholarly proposal.

| pool | surface | inscription | scholar entry | AB sign | substrate proposed | scholar first phoneme | scholarly CV |
|:--|:--|:--|:--|:--|:--|:--|:--|
| eteocretan | `arka` | ARKH 5 | tana_ARKH5 | AB59 | `k` | `t` | `ta` |
| eteocretan | `arka` | HT 108 | tana_HT108 | AB59 | `k` | `t` | `ta` |
| eteocretan | `des` | ARKH 5 | tana_ARKH5 | AB59 | `e` | `t` | `ta` |
| eteocretan | `des` | HT 108 | tana_HT108 | AB59 | `e` | `t` | `ta` |
| eteocretan | `dioi` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| eteocretan | `dioi` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |
| eteocretan | `iar` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| eteocretan | `iar` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| eteocretan | `iarei` | ARKH 5 | tana_ARKH5 | AB59 | `e` | `t` | `ta` |
| eteocretan | `ier` | ARKH 5 | tana_ARKH5 | AB59 | `e` | `t` | `ta` |
| eteocretan | `ier` | HT 108 | tana_HT108 | AB59 | `e` | `t` | `ta` |
| eteocretan | `ine` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| eteocretan | `ine` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| eteocretan | `isala` | ARKH 5 | tana_ARKH5 | AB59 | `l` | `t` | `ta` |
| eteocretan | `mi` | ARKH 2 | kura_ARKH2 | AB81 | `m` | `k` | `ku` |
| eteocretan | `mi` | ARKH 5 | tana_ARKH5 | AB59 | `m` | `t` | `ta` |
| eteocretan | `noi` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| eteocretan | `noi` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |
| eteocretan | `ona` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| eteocretan | `ona` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| eteocretan | `os` | ARKH 2 | kura_ARKH2 | AB81 | `o` | `k` | `ku` |
| eteocretan | `os` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| eteocretan | `sam` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| eteocretan | `sam` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| eteocretan | `si` | ARKH 2 | kura_ARKH2 | AB81 | `s` | `k` | `ku` |
| eteocretan | `si` | ARKH 5 | tana_ARKH5 | AB59 | `s` | `t` | `ta` |
| eteocretan | `wai` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| eteocretan | `wai` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| eteocretan | `wow` | ARKH 5 | tana_ARKH5 | AB59 | `o` | `t` | `ta` |
| eteocretan | `wow` | HT 108 | tana_HT108 | AB59 | `o` | `t` | `ta` |

## First-match enumeration (up to 3 inscriptions per surface)

| surface | inscription | n_a | n_b | n_c |
|:--|:--|---:|---:|---:|
| `iar` | ARKH 1a | 4 | 4 | 0 |
| `iar` | ARKH 1a | 2 | 0 | 0 |
| `iar` | ARKH 1a | 4 | 1 | 0 |
| `iarei` | ARKH 2 | 16 | 1 | 0 |
| `iarei` | ARKH 2 | 12 | 0 | 0 |
| `iarei` | ARKH 5 | 3 | 2 | 0 |
| `ine` | ARKH 1a | 2 | 1 | 0 |
| `ine` | ARKH 1a | 2 | 1 | 0 |
| `ine` | ARKH 1a | 2 | 1 | 0 |
| `isala` | ARKH 2 | 12 | 0 | 0 |
| `isala` | ARKH 2 | 12 | 5 | 0 |
| `isala` | ARKH 5 | 1 | 7 | 0 |
| `mi` | ARKH 1a | 2 | 2 | 0 |
| `mi` | ARKH 1a | 0 | 1 | 0 |
| `mi` | ARKH 1a | 2 | 1 | 0 |
| `noi` | ARKH 1a | 2 | 1 | 0 |
| `noi` | ARKH 1a | 2 | 2 | 0 |
| `noi` | ARKH 1a | 4 | 7 | 0 |
| `os` | ARKH 1a | 0 | 1 | 0 |
| `os` | ARKH 1a | 2 | 4 | 0 |
| `os` | ARKH 1a | 2 | 1 | 0 |
| `sam` | ARKH 1a | 0 | 2 | 0 |
| `sam` | ARKH 1a | 2 | 2 | 0 |
| `sam` | ARKH 1a | 2 | 2 | 0 |
| `si` | ARKH 1a | 0 | 2 | 0 |
| `si` | ARKH 1a | 2 | 1 | 0 |
| `si` | ARKH 1a | 2 | 2 | 0 |
| `wai` | ARKH 1a | 2 | 2 | 0 |
| `wai` | ARKH 1a | 0 | 1 | 0 |
| `wai` | ARKH 1a | 2 | 1 | 0 |
| `des` | ARKH 1a | 1 | 0 | 0 |
| `des` | ARKH 1a | 2 | 1 | 0 |
| `des` | ARKH 1a | 2 | 1 | 0 |
| `ona` | ARKH 1a | 2 | 1 | 0 |
| `ona` | ARKH 1a | 2 | 1 | 0 |
| `ona` | ARKH 1a | 2 | 2 | 0 |
| `wantai` | GO Wc 1a | 0 | 1 | 0 |
| `wantai` | HT 122b | 25 | 1 | 0 |
| `wantai` | HT 95a | 2 | 1 | 0 |
| `arka` | ARKH 1a | 4 | 1 | 1 |
| `arka` | ARKH 1a | 4 | 1 | 1 |
| `arka` | ARKH 2 | 14 | 0 | 1 |
| `dioi` | ARKH 1a | 1 | 0 | 0 |
| `dioi` | ARKH 1a | 2 | 1 | 0 |
| `dioi` | ARKH 2 | 12 | 0 | 0 |
| `iareion` | KN Zc 6 | 4 | 3 | 0 |
| `iareion` | KN Zc 6 | 2 | 1 | 0 |
| `iareion` | KN Zc 7 | 2 | 1 | 0 |
| `netamoi` | KN Zc 6 | 0 | 3 | 0 |
| `netamoi` | KN Zc 6 | 2 | 2 | 0 |
| `netamoi` | KN Zc 7 | 0 | 2 | 0 |
| `ier` | ARKH 1a | 2 | 2 | 0 |
| `ier` | ARKH 1a | 0 | 1 | 0 |
| `ier` | ARKH 1a | 2 | 2 | 0 |
| `wow` | ARKH 1a | 2 | 1 | 0 |
| `wow` | ARKH 1a | 2 | 1 | 0 |
| `wow` | ARKH 1a | 2 | 1 | 0 |
| `epimere` | KN Zc 6 | 0 | 2 | 0 |
| `epimere` | KN Zc 6 | 0 | 3 | 0 |
| `epimere` | KN Zc 7 | 0 | 2 | 0 |

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
