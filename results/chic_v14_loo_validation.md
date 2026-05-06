# CHIC chic-v12 cross-pool L3 reclassification leave-one-out validation against chic-v2 anchors (chic-v14; mg-7f57)

## Method

For each of the 20 chic-v2 paleographic anchors S with known LB-carryover value V (and known phoneme class C), S is held out in-memory (the chic-v2 anchor pool yaml is read-only) and treated as the single unknown sign by the chic-v12 cross-pool L3 reclassification machinery, run against the reduced 19-anchor pool. For each of the 4 substrate pools (aquitanian / etruscan / toponym / eteocretan) a fresh candidate-value pool is built from the reduced anchor pool's distinct LB-carryover values + bare vowels, filtered by the substrate pool's phoneme inventory (chic-v5 convention). The class-disjoint sha256-keyed control mapping inside ``compute_substrate_consistency`` is regenerated per (LOO iteration, pool) cell because the candidate-value pool is rebuilt per iteration; controls are not cached across iterations (chic-v14 brief).

Per-pool L3 winning class is the per-class argmax of the mean paired_diff over surviving candidate values. The chic-v12 reclassification rule is then applied with the held-out anchor's **known** class as the reference class (in chic-v12 the reference was the chic-v5 proposed class):

- ``corroborated_by`` = list of non-Eteocretan substrate LMs whose winning class matches the held-out anchor's known class.
- ``eteocretan_corroborates`` = (Eteocretan-L3 winning class == known class).
- ``reclassification`` = ``tier-2-equivalent`` if ``corroborated_by`` is non-empty; ``tier-3-corroborated`` if only Eteocretan-L3 corroborates; ``tier-3-uncorroborated`` otherwise.

L1 (distributional plurality, top-3 nearest anchors) and L2 (strict-top-1 anchor distance) are recomputed per LOO iteration for audit context (same machinery as chic-v9), but the chic-v14 verdict is purely a function of the cross-pool L3 reclassification — L1 + L2 are surfaced in the per-anchor table only. L4 (cross-script paleographic) is excluded by construction (chic-v9 precedent): the chic-v1 PALEOGRAPHIC_CANDIDATES list is the source of the chic-v2 anchor pool, so for any anchor S the L4 line trivially recovers V — including L4 would inflate accuracy by construction.

## Headline aggregate metrics

| metric | value |
|---|---:|
| n anchors run blind | 20 |
| **cross_pool_l3_recovery_rate** (fraction reclassifying to tier-2-equivalent under LOO) | **12/20 = 60.0%** |
| eteocretan_only_recovery_rate (fraction reclassifying to tier-3-corroborated) | 0/20 = 0.0% |
| no_corroboration_rate (fraction reclassifying to tier-3-uncorroborated) | 8/20 = 40.0% |
| chic-v12 reclassification rate (8 of 29 tier-3 candidates) | 8/29 = 27.6% |
| **chic-v12 minus LOO baseline** | **-32.4pp (below-baseline)** |

The chic-v12 reclassification rate (27.6%) is **below** the chic-v14 LOO baseline (27.6% chic-v12 vs 60.0% chic-v14 LOO; chic-v12 minus LOO = -32.4pp; |delta| ≤ 5pp = at-baseline). See the verdict subsection below for the implication.

## Per-anchor LOO results

Each row is one LOO iteration: the named anchor was removed from the chic-v2 pool and treated as the single unknown sign; the 4 substrate-pool LMs each computed an L3 winning class for the held-out anchor against the reduced 19-anchor mapping. ``corroborated_by`` lists non-Eteocretan substrate LMs whose winning class matches the held-out anchor's known class. ``reclassification`` is the chic-v12 verdict with the known class as reference. L1 + L2 columns are chic-v9 audit context.

| anchor | freq | known phoneme | known class | L1 | L2 | Eteocretan-L3 | Aquitanian-L3 | Etruscan-L3 | toponym-L3 | corroborated_by | reclassification |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| `#010` | 50 | `ja` | glide | liquid | liquid | nasal | stop | nasal ⚠ | stop ⚠ | — | tier-3-uncorroborated |
| `#013` | 26 | `pa` | stop | stop | stop | glide | liquid | nasal | liquid | — | tier-3-uncorroborated |
| `#016` | 20 | `a` | vowel | stop | glide | glide | stop | nasal | stop | — | tier-3-uncorroborated |
| `#019` | 50 | `ke` | stop | liquid | liquid | nasal | stop | stop | stop | aquitanian, etruscan, toponym | tier-2-equivalent |
| `#025` | 11 | `ta` | stop | stop | vowel | nasal | liquid | nasal | liquid | — | tier-3-uncorroborated |
| `#028` | 22 | `ti` | stop | glide | stop | nasal | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#031` | 65 | `ro` | liquid | stop | stop | stop | liquid | liquid | liquid | aquitanian, etruscan, toponym | tier-2-equivalent |
| `#038` | 75 | `i` | vowel | stop | stop | glide | nasal | nasal | nasal | — | tier-3-uncorroborated |
| `#041` | 20 | `ni` | nasal | stop | liquid | stop | stop | nasal | stop | etruscan | tier-2-equivalent |
| `#042` | 57 | `wa` | glide | stop | stop | stop ⚠ | glide | stop ⚠ | stop ⚠ | aquitanian | tier-2-equivalent |
| `#044` | 128 | `ki` | stop | stop | stop | glide | nasal | stop | nasal | etruscan | tier-2-equivalent |
| `#049` | 119 | `de` | stop | stop | stop | glide | liquid | stop | liquid | etruscan | tier-2-equivalent |
| `#053` | 14 | `me` | nasal | glide | glide | glide | nasal | stop | stop | aquitanian | tier-2-equivalent |
| `#054` | 22 | `mu` | nasal | glide | stop | glide | stop | stop | stop | — | tier-3-uncorroborated |
| `#057` | 35 | `je` | glide | nasal | stop | glide | glide | stop ⚠ | stop ⚠ | aquitanian | tier-2-equivalent |
| `#061` | 39 | `te` | stop | liquid | liquid | glide | liquid | stop | liquid | etruscan | tier-2-equivalent |
| `#070` | 56 | `ra` | liquid | stop | stop | nasal | nasal | stop | nasal | — | tier-3-uncorroborated |
| `#073` | 5 | `to` | stop | liquid | liquid | nasal | stop | nasal | stop | aquitanian, toponym | tier-2-equivalent |
| `#077` | 13 | `ma` | nasal | glide | stop | glide | stop | nasal | stop | etruscan | tier-2-equivalent |
| `#092` | 37 | `ke` | stop | glide | liquid | glide | glide | nasal | stop | toponym | tier-2-equivalent |

⚠ on a pool's L3 column indicates that the held-out anchor's class had no representative in that pool's rebuilt 19-anchor candidate-value pool, so the L3 vote for that pool was structurally unable to recover the class. Total LOO iterations with at least one such pool: 3/20.

## Per-anchor per-pool per-class mean paired_diff

Detail-table view of the 20 × 4 = 80 cells. Each row is one (LOO iteration, pool) cell; columns are per-class mean paired_diff over the surviving candidate values for that pool's filter. ``winning class`` is the per-class argmax. ``—`` for a class indicates the class is empty in the rebuilt candidate-value pool for that substrate (e.g. ``glide`` for aquitanian / etruscan / toponym, since their candidate pools exclude `wa` / `ja` / `je` by inventory filter; this is a structural property of those pools, not an L3 finding).

### `#010` (known: `ja`, class: glide; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.043713 | -0.048040 | +0.043713 | -0.002632 | +0.017704 | — | -0.086171 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.090413 | -0.038831 | +0.006695 | +0.090413 | -0.029589 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.043713 | -0.079653 | +0.043713 | -0.002632 | +0.017704 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.055555 | -0.011452 | -0.009002 | +0.055555 | -0.031650 | — | +0.017979 |

### `#013` (known: `pa`, class: stop; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.024000 | -0.025396 | +0.010362 | +0.015762 | +0.024000 | — | -0.003028 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.018424 | -0.049557 | +0.000439 | +0.018424 | +0.015496 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.024000 | -0.025396 | +0.006692 | +0.005392 | +0.024000 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.018481 | -0.025525 | +0.004081 | +0.017474 | +0.011790 | — | +0.018481 |

### `#016` (known: `a`, class: vowel; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.009906 | -0.020026 | +0.009906 | -0.001118 | -0.009578 | — | -0.004447 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.022889 | -0.020875 | +0.008957 | +0.022889 | -0.018316 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.007882 | -0.020026 | +0.007882 | -0.001118 | -0.009578 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.024791 | -0.011384 | -0.003944 | +0.011357 | -0.004576 | — | +0.024791 |

### `#019` (known: `ke`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian, etruscan, toponym)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.066934 | -0.077770 | +0.066934 | +0.030319 | +0.052163 | — | -0.049974 |
| etruscan | `etruscan.json` | stop | `ta` | +0.105378 | -0.099240 | +0.105378 | +0.075747 | +0.083410 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.066572 | -0.091032 | +0.066572 | +0.030319 | +0.052163 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.041072 | -0.059886 | +0.036564 | +0.041072 | +0.016521 | — | -0.030214 |

### `#025` (known: `ta`, class: stop; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.013447 | -0.010932 | +0.003111 | +0.005521 | +0.013447 | — | -0.007504 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.011052 | -0.025244 | -0.002953 | +0.011052 | +0.006220 | — | — |
| toponym | `basque.json` | liquid | `ro` | +0.005587 | -0.014687 | +0.003111 | +0.005521 | +0.005587 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.008346 | -0.013238 | +0.000545 | +0.008346 | +0.001274 | — | +0.002722 |

### `#028` (known: `ti`, class: stop; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.020208 | -0.012535 | +0.004950 | +0.020208 | -0.009707 | — | -0.000398 |
| etruscan | `etruscan.json` | nasal | `me` | +0.028161 | -0.023222 | +0.020783 | +0.028161 | -0.005156 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.020208 | -0.011143 | +0.007592 | +0.020208 | -0.012544 | — | — |
| eteocretan | `eteocretan.json` | nasal | `ma` | +0.027069 | -0.013497 | +0.002285 | +0.027069 | -0.024803 | — | +0.015538 |

### `#031` (known: `ro`, class: liquid; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian, etruscan, toponym)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.158985 | -0.089843 | +0.068348 | +0.023568 | +0.158985 | — | -0.151436 |
| etruscan | `etruscan.json` | liquid | `ra` | +0.133984 | -0.143253 | -0.017953 | +0.021136 | +0.133984 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.158985 | -0.142355 | +0.049406 | +0.000848 | +0.158985 | — | — |
| eteocretan | `eteocretan.json` | stop | `de` | +0.010256 | -0.106704 | +0.010256 | -0.009479 | -0.010176 | — | -0.048654 |

### `#038` (known: `i`, class: vowel; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.080628 | -0.045198 | +0.025543 | +0.080628 | -0.000261 | — | -0.044524 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.102854 | -0.095924 | +0.015052 | +0.102854 | +0.015573 | — | — |
| toponym | `basque.json` | nasal | `ni` | +0.050364 | -0.039478 | +0.025543 | +0.050364 | -0.000261 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.096229 | -0.029937 | +0.004949 | +0.075833 | -0.038853 | — | +0.096229 |

### `#041` (known: `ni`, class: nasal; reclassification: **tier-2-equivalent**; corroborated_by: etruscan)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.024074 | -0.022912 | +0.024074 | +0.001499 | +0.003000 | — | -0.012530 |
| etruscan | `etruscan.json` | nasal | `me` | +0.032253 | -0.055926 | +0.028972 | +0.032253 | -0.030225 | — | — |
| toponym | `basque.json` | stop | `de` | +0.022384 | -0.022912 | +0.022384 | +0.001499 | +0.000066 | — | — |
| eteocretan | `eteocretan.json` | stop | `ki` | +0.019743 | -0.026692 | +0.019743 | +0.017688 | -0.035171 | — | +0.015175 |

### `#042` (known: `wa`, class: glide; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | glide | `je` | +0.038545 | -0.041186 | +0.038344 | +0.020981 | -0.020476 | — | +0.038545 |
| etruscan | `etruscan.json` | stop | `ti` | +0.087066 | -0.080875 | +0.087066 | +0.045864 | -0.023787 | — | — |
| toponym | `basque.json` | stop | `pa` | +0.045416 | -0.041186 | +0.045416 | +0.020981 | -0.035148 | — | — |
| eteocretan | `eteocretan.json` | stop | `pa` | +0.037220 | -0.040266 | +0.037220 | +0.029848 | -0.009139 | — | — |

### `#044` (known: `ki`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: etruscan)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.037702 | -0.100815 | -0.020731 | +0.037702 | -0.126362 | — | +0.028110 |
| etruscan | `etruscan.json` | stop | `te` | +0.081086 | -0.227521 | +0.081086 | +0.069635 | -0.085670 | — | — |
| toponym | `basque.json` | nasal | `ma` | +0.057980 | -0.099466 | -0.003409 | +0.057980 | -0.126362 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.346987 | -0.076955 | +0.018722 | +0.078420 | -0.132660 | — | +0.346987 |

### `#049` (known: `de`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: etruscan)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.114762 | -0.178813 | +0.087521 | -0.047042 | +0.114762 | — | -0.154639 |
| etruscan | `etruscan.json` | stop | `ke` | +0.184740 | -0.181245 | +0.184740 | +0.094462 | -0.046650 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.114762 | -0.232560 | +0.087521 | -0.082705 | +0.114762 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.102319 | -0.083596 | +0.068068 | +0.086503 | -0.139356 | — | +0.102319 |

### `#053` (known: `me`, class: nasal; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `ma` | +0.010031 | -0.011481 | +0.008224 | +0.010031 | +0.003288 | — | +0.007343 |
| etruscan | `etruscan.json` | stop | `ke` | +0.018467 | -0.026627 | +0.018467 | +0.012517 | -0.015165 | — | — |
| toponym | `basque.json` | stop | `de` | +0.010288 | -0.011481 | +0.010288 | +0.007790 | -0.007819 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.011177 | -0.007700 | +0.004151 | +0.004174 | -0.006139 | — | +0.011177 |

### `#054` (known: `mu`, class: nasal; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.022063 | -0.024834 | +0.022063 | -0.007876 | +0.016059 | — | +0.008829 |
| etruscan | `etruscan.json` | stop | `ti` | +0.020043 | -0.031236 | +0.020043 | +0.002027 | -0.014211 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.025511 | -0.024834 | +0.025511 | -0.007876 | -0.001047 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.018168 | -0.011066 | +0.008764 | +0.012975 | -0.019839 | — | +0.018168 |

### `#057` (known: `je`, class: glide; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | glide | `ja` | +0.052681 | -0.027631 | +0.022193 | +0.010713 | -0.040925 | — | +0.052681 |
| etruscan | `etruscan.json` | stop | `te` | +0.040202 | -0.039267 | +0.040202 | +0.024803 | -0.062779 | — | — |
| toponym | `basque.json` | stop | `de` | +0.022193 | -0.027631 | +0.022193 | +0.010713 | -0.040925 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.051856 | -0.014241 | +0.019433 | +0.021953 | -0.030907 | — | +0.051856 |

### `#061` (known: `te`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: etruscan)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | liquid | `ra` | +0.066729 | -0.055777 | +0.038253 | -0.003724 | +0.066729 | — | -0.068504 |
| etruscan | `etruscan.json` | stop | `ta` | +0.071977 | -0.084503 | +0.071977 | +0.011790 | +0.032517 | — | — |
| toponym | `basque.json` | liquid | `ra` | +0.066729 | -0.055777 | +0.038253 | +0.003437 | +0.066729 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.036836 | -0.035775 | +0.025953 | +0.006912 | -0.014247 | — | +0.036836 |

### `#070` (known: `ra`, class: liquid; reclassification: **tier-3-uncorroborated**; corroborated_by: —)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `me` | +0.050134 | -0.037300 | +0.029210 | +0.050134 | +0.014235 | — | +0.007080 |
| etruscan | `etruscan.json` | stop | `ti` | +0.076019 | -0.101871 | +0.076019 | +0.060512 | +0.068646 | — | — |
| toponym | `basque.json` | nasal | `me` | +0.050134 | -0.058265 | +0.040777 | +0.050134 | +0.014235 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.076144 | -0.048278 | +0.036404 | +0.076144 | -0.027428 | — | +0.051601 |

### `#073` (known: `to`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: aquitanian, toponym)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.001457 | -0.005217 | +0.001457 | +0.000712 | -0.000238 | — | +0.001401 |
| etruscan | `etruscan.json` | nasal | `me` | +0.005332 | -0.005354 | +0.001763 | +0.005332 | -0.003819 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.001530 | -0.005724 | +0.001530 | +0.001221 | -0.000238 | — | — |
| eteocretan | `eteocretan.json` | nasal | `me` | +0.002567 | -0.003346 | +0.000523 | +0.002567 | -0.002100 | — | +0.000329 |

### `#077` (known: `ma`, class: nasal; reclassification: **tier-2-equivalent**; corroborated_by: etruscan)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `de` | +0.009061 | -0.006579 | +0.009061 | +0.003148 | -0.001196 | — | -0.001981 |
| etruscan | `etruscan.json` | nasal | `ni` | +0.014089 | -0.017564 | +0.012964 | +0.014089 | -0.002498 | — | — |
| toponym | `basque.json` | stop | `de` | +0.008158 | -0.008860 | +0.008158 | +0.003148 | -0.001196 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.011868 | -0.007198 | +0.007423 | +0.005475 | -0.001194 | — | +0.011868 |

### `#092` (known: `ke`, class: stop; reclassification: **tier-2-equivalent**; corroborated_by: toponym)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | glide | `ja` | +0.023710 | -0.042551 | +0.015673 | +0.006457 | -0.024851 | — | +0.023710 |
| etruscan | `etruscan.json` | nasal | `ma` | +0.018900 | -0.070942 | +0.017457 | +0.018900 | -0.031153 | — | — |
| toponym | `basque.json` | stop | `te` | +0.015628 | -0.042551 | +0.015628 | +0.006457 | -0.024851 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.019476 | -0.031175 | +0.015792 | +0.013992 | -0.018620 | — | +0.019476 |

## Verdict — chic-v12 vs chic-v14 LOO baseline

**The chic-v14 LOO cross-pool L3 recovery rate on known anchors is 60.0%, so chic-v12's 27.6% reclassification rate on the 29 tier-3 candidates is -32.4pp BELOW the LOO baseline.** Cross-pool L3 corroborates the held-out anchor's known class **more often** than chic-v12 corroborates the chic-v5 proposed class on the tier-3 set. Read against the chic-v14 brief's interpretation framework ("if LOO shows 80%, the 27.6% is below baseline and the reclassification is anti-evidentiary"): the cross-pool L3 axis recovers ground-truth class far more often than it corroborates the chic-v5 proposed class on the tier-3 set, so chic-v12's reclassification is below the rate we'd see if the proposed classes were correct — **anti-evidentiary on the tier-3 set**. chic-v13's context inspection (sibling ticket) becomes the load-bearing pillar; cross-pool L3 alone is no longer the dominant evidence axis on the tier-3 set.

## Caveats

- **Cross-pool L3 only — L1+L2 columns are audit context.** The chic-v14 verdict is computed from cross-pool L3 alone, matching the chic-v12 reclassification rule's structure. L1+L2 LOO accuracy is reported by chic-v9 (mg-18cb) and is not re-summarized here.
- **Class-level resolution.** The reclassification predicate is class-level (vowel / stop / nasal / liquid / fricative / glide), matching chic-v12's class-level resolution. The LOO test does not adjudicate specific phoneme value (`ja` vs `je` vs `wa` within glide; `pa` vs `ta` vs `ka` within stop).
- **Per-pool candidate-pool reduction.** Each pool's rebuilt-per-iteration candidate-value pool removes the held-out anchor's value (unless another anchor shares it; in this corpus only `ke` is shared, between `#019` and `#092`). When the held-out class has no other representative in a specific pool's rebuilt candidate pool, that pool's L3 vote cannot recover the class by construction — flagged with ⚠ in the per-anchor table.
- **Class-disjoint deterministic-permutation control.** The control phoneme for each (sign, candidate) pair is a sha256-keyed class-disjoint pick from the per-iteration candidate-value pool. The pool itself is rebuilt per LOO iteration, so controls are automatically per-iteration; no caching across iterations (chic-v14 brief).
- **Small N (20 anchors).** The LOO baseline is a 20-anchor rate; binomial noise on 20 trials is substantial. A ±5pp at-baseline band is a coarse approximation to that noise floor — finer comparisons should not be drawn from this test alone. The chic-v9 framework-level negative (LOO accuracy 20.0% on the L1+L2+L3 framework) sets the upper bound on what chic-v14's per-axis LOO can establish.
- **Anchor-pool composition bias.** The chic-v2 anchor pool is the chic-v1 paleographic-candidate list (curated). The LOO baseline measures cross-pool L3 corroboration on **anchor-shaped** signs, which may differ systematically from the 76 unknown signs the chic-v5 framework targets. The comparison to chic-v12's 27.6% on the tier-3 set is the intended axis of read.
- **Comparison band semantics.** The LOO recovery rate is the **baseline**; chic-v12's 27.6% is the test value. ``above-baseline`` = chic-v12 above LOO by > 5pp (meaningful: chic-v12 reclassifies *more* than ground-truth-LOO does, picking up a high-corroboration band). ``below-baseline`` = chic-v12 below LOO by > 5pp (anti-evidentiary: cross-pool L3 corroborates ground-truth more often than it corroborates chic-v12 proposals). ``at-baseline`` = |chic-v12 − LOO| ≤ 5pp.

## Determinism

- No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-keyed permutation construction; LOO iteration order is sorted by anchor numeric id; cross-pool dispatch is fixed in POOL_DISPATCH.
- Same inputs → byte-identical output. Re-running this script overwrites the result files with byte-identical content.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* Amsterdam: J. C. Gieben.
- Trask, R. L. (1997). *The History of Basque.* London: Routledge.
- Bonfante, G. & Bonfante, L. (2002). *The Etruscan Language: An Introduction* (revised ed.). Manchester / New York.
- Beekes, R. S. P. (2010). *Etymological Dictionary of Greek*, vol. 2 appendix on Pre-Greek substrate. Leiden: Brill.

## Build provenance

- Generated by `scripts/build_chic_v14.py` (mg-7f57).
- fetched_at: 2026-05-06T08:33:06Z
- Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); `corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); `pools/cretan_hieroglyphic_signs.yaml` (chic-v1); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); `pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; `harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.
