# v23 cross-LM gate — etruscan substrate under Eteocretan LM (mg-b599) — under Eteocretan LM (reverse cross-LM check)

**Headline: the etruscan substrate pool FAILs the v10 right-tail bayesian gate against control_etruscan when both sides are scored under the Eteocretan LM at p=9.243e-01** (median substrate posterior 0.9341 vs median control posterior 0.9509; gap -0.0167). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| etruscan | control_etruscan | Eteocretan | 20 | 20 | 0.9341 | 0.9509 | 147.5 | 9.243e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9256. Mean of top-20 control posterior_mean: 0.9499. Gap (median, gate-relevant): -0.0167; gap (mean): -0.0243. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `aiser` | 52 | 52 | 0.9815 | `neie` | 174 | 174 | 0.9943 |
| 2 | `eis` | 50 | 50 | 0.9808 | `aasaas` | 57 | 57 | 0.9831 |
| 3 | `nesna` | 50 | 50 | 0.9808 | `iem` | 57 | 57 | 0.9831 |
| 4 | `thesan` | 50 | 50 | 0.9808 | `nai` | 180 | 177 | 0.9780 |
| 5 | `etera` | 50 | 49 | 0.9615 | `inathn` | 34 | 34 | 0.9722 |
| 6 | `tamera` | 24 | 24 | 0.9615 | `aan` | 1243 | 1199 | 0.9639 |
| 7 | `zinece` | 24 | 24 | 0.9615 | `nthi` | 25 | 25 | 0.9630 |
| 8 | `śuthina` | 24 | 24 | 0.9615 | `thi` | 1725 | 1659 | 0.9612 |
| 9 | `in` | 51 | 49 | 0.9434 | `ae` | 42 | 41 | 0.9545 |
| 10 | `cepen` | 50 | 48 | 0.9423 | `izththuch` | 39 | 38 | 0.9512 |
| 11 | `spural` | 25 | 24 | 0.9259 | `sann` | 99 | 95 | 0.9505 |
| 12 | `nethuns` | 24 | 23 | 0.9231 | `iilie` | 139 | 133 | 0.9504 |
| 13 | `puia` | 55 | 51 | 0.9123 | `thipti` | 38 | 37 | 0.9500 |
| 14 | `larth` | 54 | 50 | 0.9107 | `mialn` | 16 | 16 | 0.9444 |
| 15 | `semphalch` | 17 | 16 | 0.8947 | `nmlnv` | 11 | 11 | 0.9231 |
| 16 | `caitim` | 24 | 22 | 0.8846 | `aiph` | 114 | 106 | 0.9224 |
| 17 | `thanchvil` | 13 | 12 | 0.8667 | `emis` | 22 | 21 | 0.9167 |
| 18 | `maru` | 50 | 44 | 0.8654 | `ithalam` | 22 | 21 | 0.9167 |
| 19 | `zelar` | 50 | 43 | 0.8462 | `iauri` | 154 | 141 | 0.9103 |
| 20 | `tivr` | 50 | 42 | 0.8269 | `ssri` | 31 | 29 | 0.9091 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `neie` | 174 | 174 | 0.9943 | 1.000 | 0.9943 |
| 2 | control | `aasaas` | 57 | 57 | 0.9831 | 1.000 | 0.9831 |
| 3 | control | `iem` | 57 | 57 | 0.9831 | 1.000 | 0.9831 |
| 4 | substrate | `aiser` | 52 | 52 | 0.9815 | 1.000 | 0.9815 |
| 5 | substrate | `eis` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `nesna` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `thesan` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | control | `nai` | 180 | 177 | 0.9780 | 1.000 | 0.9780 |
| 9 | control | `inathn` | 34 | 34 | 0.9722 | 1.000 | 0.9722 |
| 10 | control | `aan` | 1243 | 1199 | 0.9639 | 1.000 | 0.9639 |
| 11 | control | `nthi` | 25 | 25 | 0.9630 | 1.000 | 0.9630 |
| 12 | substrate | `etera` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 13 | substrate | `tamera` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 14 | substrate | `zinece` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `śuthina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | control | `thi` | 1725 | 1659 | 0.9612 | 1.000 | 0.9612 |
| 17 | control | `ae` | 42 | 41 | 0.9545 | 1.000 | 0.9545 |
| 18 | control | `izththuch` | 39 | 38 | 0.9512 | 1.000 | 0.9512 |
| 19 | control | `sann` | 99 | 95 | 0.9505 | 1.000 | 0.9505 |
| 20 | control | `iilie` | 139 | 133 | 0.9504 | 1.000 | 0.9504 |
| 21 | control | `thipti` | 38 | 37 | 0.9500 | 1.000 | 0.9500 |
| 22 | control | `mialn` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 23 | substrate | `in` | 51 | 49 | 0.9434 | 1.000 | 0.9434 |
| 24 | substrate | `cepen` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 25 | substrate | `spural` | 25 | 24 | 0.9259 | 1.000 | 0.9259 |
| 26 | substrate | `nethuns` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 27 | control | `nmlnv` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 28 | control | `aiph` | 114 | 106 | 0.9224 | 1.000 | 0.9224 |
| 29 | control | `emis` | 22 | 21 | 0.9167 | 1.000 | 0.9167 |
| 30 | control | `ithalam` | 22 | 21 | 0.9167 | 1.000 | 0.9167 |
| 31 | substrate | `puia` | 55 | 51 | 0.9123 | 1.000 | 0.9123 |
| 32 | substrate | `larth` | 54 | 50 | 0.9107 | 1.000 | 0.9107 |
| 33 | control | `iauri` | 154 | 141 | 0.9103 | 1.000 | 0.9103 |
| 34 | control | `ssri` | 31 | 29 | 0.9091 | 1.000 | 0.9091 |
| 35 | control | `neeui` | 88 | 80 | 0.9000 | 1.000 | 0.9000 |
| 36 | control | `psach` | 58 | 53 | 0.9000 | 1.000 | 0.9000 |
| 37 | substrate | `semphalch` | 17 | 16 | 0.8947 | 1.000 | 0.8947 |
| 38 | control | `ithalr` | 17 | 16 | 0.8947 | 1.000 | 0.8947 |
| 39 | substrate | `caitim` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 40 | control | `suirc` | 40 | 36 | 0.8810 | 1.000 | 0.8810 |
| 41 | substrate | `thanchvil` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 42 | substrate | `maru` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 43 | control | `ninre` | 61 | 53 | 0.8571 | 1.000 | 0.8571 |
| 44 | control | `nil` | 149 | 127 | 0.8477 | 1.000 | 0.8477 |
| 45 | substrate | `zelar` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 46 | control | `nuhuse` | 57 | 48 | 0.8305 | 1.000 | 0.8305 |
| 47 | substrate | `tivr` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 48 | control | `eahss` | 15 | 13 | 0.8235 | 1.000 | 0.8235 |
| 49 | control | `thia` | 138 | 113 | 0.8143 | 1.000 | 0.8143 |
| 50 | substrate | `cilth` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (label: Eteocretan). Substrate pool: `etruscan` (20 top surfaces). Control pool: `control_etruscan` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

