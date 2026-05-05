# Linear A top-K verification — pool=etruscan (mg-c202)

v26 mechanical verification of the v10/v18/v21 leaderboard top-20 substrate surfaces for the **etruscan** pool. Built by `scripts/build_linear_a_v26.py`. Methodology mirrors chic-v6 (mg-a557) verbatim — three pre-registered match sources, no post-hoc relaxation. The candidate-value source is the per-pool leaderboard top-20 (substrate side) rather than the chic-v5 tier-2 specific-phoneme override set; the corpus is Linear A (`corpus/all.jsonl`) rather than CHIC.

## Pre-registered match criteria (chic-v6 verbatim)

- **Source A.** Scholar-proposed Linear-A reading match. A scholar entry's `ab_sequence` (length k) matches a Linear A inscription iff there exists a contiguous run of k literal-anchored syllabographic events within a single DIV-bounded segment such that for each position i, the literal phoneme value's first character equals the scholar's `scholarly_first_phoneme[i]`.
- **Source B.** Toponym substring match (`pools/toponym.yaml`, length L ∈ [3, 5]).
- **Source C.** Item-location consistency. Per-inscription `site` field (lowercased; alphabetical chars only); substrings length 3..5; matched against the inscription's own phoneme stream.

## Candidate-value source — pool top-20 substrate surfaces

| rank | surface |
|---:|:--|
| 1 | `larth` |
| 2 | `aiser` |
| 3 | `matam` |
| 4 | `avils` |
| 5 | `camthi` |
| 6 | `chimth` |
| 7 | `hanthe` |
| 8 | `laris` |
| 9 | `nac` |
| 10 | `sech` |
| 11 | `thana` |
| 12 | `zelar` |
| 13 | `caitim` |
| 14 | `thesan` |
| 15 | `spureri` |
| 16 | `thanchvil` |
| 17 | `suthi` |
| 18 | `mach` |
| 19 | `arnth` |
| 20 | `sath` |

## Per-pool aggregate

Inputs: 772 Linear A inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| metric | value |
|:--|--:|
| n top-20 surfaces with ≥1 positive paired-diff record | 20 |
| n positive paired-diff records (post-filter) | 900 |
| n distinct inscriptions extended | 42 |
| n distinct inscriptions with ≥1 source-A/B/C match | 40 |
| match rate (over extended inscriptions) | 0.9524 |
| total source-A hits | 6575 |
| total source-B hits | 3735 |
| total source-C hits | 58 |
| total a+b+c hits | 10368 |

## Per-surface verification status

| rank | surface | n records | n inscriptions extended | n inscriptions w/ match | a hits | b hits | c hits | status |
|---:|:--|---:|---:|---:|---:|---:|---:|:--|
| 1 | `larth` | 55 | 24 | 24 | 660 | 217 | 5 | verified |
| 2 | `aiser` | 52 | 24 | 23 | 181 | 199 | 1 | verified |
| 3 | `matam` | 52 | 25 | 15 | 196 | 55 | 1 | verified |
| 4 | `avils` | 50 | 24 | 13 | 174 | 57 | 1 | verified |
| 5 | `camthi` | 50 | 24 | 24 | 366 | 64 | 1 | verified |
| 6 | `chimth` | 50 | 21 | 21 | 623 | 174 | 5 | verified |
| 7 | `hanthe` | 50 | 24 | 24 | 176 | 876 | 6 | verified |
| 8 | `laris` | 50 | 24 | 24 | 278 | 154 | 1 | verified |
| 9 | `nac` | 50 | 12 | 10 | 400 | 42 | 3 | verified |
| 10 | `sech` | 50 | 12 | 9 | 387 | 38 | 3 | verified |
| 11 | `thana` | 50 | 21 | 20 | 528 | 244 | 13 | verified |
| 12 | `zelar` | 50 | 24 | 23 | 269 | 72 | 1 | verified |
| 13 | `caitim` | 24 | 9 | 8 | 103 | 23 | 0 | verified |
| 14 | `thesan` | 49 | 24 | 24 | 181 | 438 | 1 | verified |
| 15 | `spureri` | 13 | 3 | 3 | 22 | 29 | 0 | verified |
| 16 | `thanchvil` | 13 | 3 | 3 | 22 | 66 | 0 | verified |
| 17 | `suthi` | 47 | 21 | 21 | 583 | 167 | 5 | verified |
| 18 | `mach` | 53 | 13 | 10 | 431 | 56 | 3 | verified |
| 19 | `arnth` | 46 | 21 | 21 | 622 | 667 | 5 | verified |
| 20 | `sath` | 46 | 11 | 11 | 373 | 97 | 3 | verified |

## Inverse-verification (sign-level contradictions vs scholar set)

Substrate hypothesis proposes phoneme value at an AB sign covered by a scholar-proposed reading at the same span; the first character of the substrate proposal differs from the scholar's. This is **negative evidence** at the sign level — the substrate proposal disagrees with the published scholarly proposal.

| pool | surface | inscription | scholar entry | AB sign | substrate proposed | scholar first phoneme | scholarly CV |
|:--|:--|:--|:--|:--|:--|:--|:--|
| etruscan | `aiser` | ARKH 5 | tana_ARKH5 | AB59 | `e` | `t` | `ta` |
| etruscan | `arnth` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| etruscan | `arnth` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| etruscan | `avils` | ARKH 5 | tana_ARKH5 | AB59 | `l` | `t` | `ta` |
| etruscan | `chimth` | ARKH 5 | tana_ARKH5 | AB59 | `m` | `t` | `ta` |
| etruscan | `chimth` | HT 108 | tana_HT108 | AB59 | `m` | `t` | `ta` |
| etruscan | `laris` | ARKH 5 | tana_ARKH5 | AB59 | `i` | `t` | `ta` |
| etruscan | `larth` | ARKH 5 | tana_ARKH5 | AB59 | `r` | `t` | `ta` |
| etruscan | `larth` | HT 108 | tana_HT108 | AB59 | `r` | `t` | `ta` |
| etruscan | `mach` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| etruscan | `mach` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| etruscan | `matam` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| etruscan | `nac` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| etruscan | `nac` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| etruscan | `sath` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| etruscan | `sath` | HT 108 | tana_HT108 | AB59 | `a` | `t` | `ta` |
| etruscan | `sech` | ARKH 5 | tana_ARKH5 | AB59 | `e` | `t` | `ta` |
| etruscan | `sech` | HT 108 | tana_HT108 | AB59 | `e` | `t` | `ta` |
| etruscan | `thana` | ARKH 5 | tana_ARKH5 | AB59 | `n` | `t` | `ta` |
| etruscan | `thana` | HT 108 | tana_HT108 | AB59 | `n` | `t` | `ta` |
| etruscan | `thesan` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |
| etruscan | `zelar` | ARKH 5 | tana_ARKH5 | AB59 | `a` | `t` | `ta` |

## First-match enumeration (up to 3 inscriptions per surface)

| surface | inscription | n_a | n_b | n_c |
|:--|:--|---:|---:|---:|
| `larth` | ARKH 1a | 2 | 1 | 0 |
| `larth` | ARKH 1a | 4 | 2 | 0 |
| `larth` | ARKH 2 | 14 | 0 | 0 |
| `aiser` | ARKH 2 | 12 | 0 | 0 |
| `aiser` | ARKH 2 | 12 | 3 | 0 |
| `aiser` | ARKH 5 | 1 | 3 | 0 |
| `matam` | ARKH 2 | 12 | 0 | 0 |
| `matam` | ARKH 2 | 12 | 0 | 0 |
| `matam` | ARKH 5 | 1 | 1 | 0 |
| `avils` | ARKH 2 | 12 | 0 | 0 |
| `avils` | ARKH 2 | 12 | 0 | 0 |
| `avils` | ARKH 5 | 1 | 1 | 0 |
| `camthi` | ARKH 2 | 14 | 0 | 0 |
| `camthi` | ARKH 2 | 18 | 0 | 0 |
| `camthi` | ARKH 5 | 5 | 1 | 0 |
| `chimth` | ARKH 1a | 4 | 2 | 0 |
| `chimth` | ARKH 1a | 2 | 1 | 0 |
| `chimth` | ARKH 2 | 14 | 1 | 0 |
| `hanthe` | ARKH 2 | 12 | 18 | 1 |
| `hanthe` | ARKH 2 | 12 | 9 | 0 |
| `hanthe` | ARKH 5 | 1 | 19 | 1 |
| `laris` | ARKH 2 | 16 | 2 | 0 |
| `laris` | ARKH 2 | 12 | 0 | 0 |
| `laris` | ARKH 5 | 3 | 2 | 0 |
| `nac` | ARKH 1a | 2 | 1 | 0 |
| `nac` | ARKH 1a | 2 | 2 | 0 |
| `nac` | ARKH 1a | 4 | 4 | 0 |
| `sech` | ARKH 1a | 0 | 1 | 0 |
| `sech` | ARKH 1a | 2 | 1 | 0 |
| `sech` | ARKH 1a | 2 | 1 | 0 |
| `thana` | ARKH 1a | 0 | 2 | 1 |
| `thana` | ARKH 1a | 2 | 3 | 1 |
| `thana` | ARKH 2 | 12 | 0 | 0 |
| `zelar` | ARKH 2 | 14 | 0 | 0 |
| `zelar` | ARKH 2 | 12 | 0 | 0 |
| `zelar` | ARKH 5 | 3 | 1 | 0 |
| `caitim` | GO Wc 1a | 2 | 0 | 0 |
| `caitim` | HT 122b | 27 | 0 | 0 |
| `caitim` | HT 95a | 4 | 0 | 0 |
| `thesan` | ARKH 2 | 12 | 0 | 0 |
| `thesan` | ARKH 2 | 12 | 8 | 0 |
| `thesan` | ARKH 5 | 1 | 9 | 0 |
| `spureri` | KN Zc 6 | 0 | 2 | 0 |
| `spureri` | KN Zc 6 | 0 | 2 | 0 |
| `spureri` | KN Zc 7 | 0 | 1 | 0 |
| `thanchvil` | KN Zc 6 | 0 | 4 | 0 |
| `thanchvil` | KN Zc 6 | 0 | 15 | 0 |
| `thanchvil` | KN Zc 7 | 0 | 2 | 0 |
| `suthi` | ARKH 1a | 2 | 2 | 0 |
| `suthi` | ARKH 1a | 4 | 2 | 0 |
| `suthi` | ARKH 2 | 12 | 1 | 0 |
| `mach` | ARKH 1a | 2 | 1 | 0 |
| `mach` | ARKH 1a | 2 | 2 | 0 |
| `mach` | ARKH 1a | 2 | 1 | 0 |
| `arnth` | ARKH 1a | 4 | 13 | 0 |
| `arnth` | ARKH 2 | 12 | 9 | 0 |
| `arnth` | ARKH 2 | 16 | 13 | 0 |
| `sath` | ARKH 1a | 2 | 2 | 0 |
| `sath` | ARKH 1a | 2 | 5 | 0 |
| `sath` | ARKH 1a | 2 | 2 | 0 |

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
