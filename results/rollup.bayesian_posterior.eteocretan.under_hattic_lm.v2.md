# v23 cross-LM gate — eteocretan substrate under Hattic LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the eteocretan substrate pool FAILs the v10 right-tail bayesian gate against control_eteocretan_bigram when both sides are scored under the Hattic LM at p=9.911e-01** (median substrate posterior 0.9000 vs median control posterior 0.9608; gap -0.0608). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | Hattic | 20 | 20 | 0.9000 | 0.9608 | 113.0 | 9.911e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8840. Mean of top-20 control posterior_mean: 0.9456. Gap (median, gate-relevant): -0.0608; gap (mean): -0.0616. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `isala` | 50 | 50 | 0.9808 | `phai` | 110 | 110 | 0.9911 |
| 2 | `rima` | 50 | 50 | 0.9808 | `isai` | 97 | 97 | 0.9899 |
| 3 | `wai` | 50 | 50 | 0.9808 | `sal` | 50 | 50 | 0.9808 |
| 4 | `omali` | 50 | 49 | 0.9615 | `disa` | 49 | 49 | 0.9804 |
| 5 | `siatas` | 24 | 24 | 0.9615 | `etaltat` | 48 | 48 | 0.9800 |
| 6 | `wantai` | 24 | 24 | 0.9615 | `ial` | 34 | 34 | 0.9722 |
| 7 | `arka` | 50 | 48 | 0.9423 | `ana` | 33 | 33 | 0.9714 |
| 8 | `sante` | 50 | 48 | 0.9423 | `tem` | 56 | 55 | 0.9655 |
| 9 | `si` | 50 | 46 | 0.9038 | `ete` | 131 | 127 | 0.9624 |
| 10 | `sametion` | 8 | 8 | 0.9000 | `nadina` | 24 | 24 | 0.9615 |
| 11 | `zethante` | 8 | 8 | 0.9000 | `dnta` | 23 | 23 | 0.9600 |
| 12 | `natoniate` | 6 | 6 | 0.8750 | `iphai` | 15 | 15 | 0.9412 |
| 13 | `parsiphai` | 6 | 6 | 0.8750 | `ieti` | 163 | 154 | 0.9394 |
| 14 | `inaiperima` | 5 | 5 | 0.8571 | `ima` | 44 | 42 | 0.9348 |
| 15 | `iareion` | 13 | 11 | 0.8000 | `pepim` | 12 | 12 | 0.9286 |
| 16 | `omalioi` | 13 | 11 | 0.8000 | `mari` | 74 | 68 | 0.9079 |
| 17 | `noi` | 50 | 40 | 0.7885 | `iamet` | 190 | 173 | 0.9062 |
| 18 | `niate` | 50 | 39 | 0.7692 | `alan` | 7 | 7 | 0.8889 |
| 19 | `etion` | 50 | 38 | 0.7500 | `ipisa` | 6 | 6 | 0.8750 |
| 20 | `ieroi` | 50 | 38 | 0.7500 | `isar` | 6 | 6 | 0.8750 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `phai` | 110 | 110 | 0.9911 | 1.000 | 0.9911 |
| 2 | control | `isai` | 97 | 97 | 0.9899 | 1.000 | 0.9899 |
| 3 | substrate | `isala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `rima` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | control | `sal` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | control | `disa` | 49 | 49 | 0.9804 | 1.000 | 0.9804 |
| 8 | control | `etaltat` | 48 | 48 | 0.9800 | 1.000 | 0.9800 |
| 9 | control | `ial` | 34 | 34 | 0.9722 | 1.000 | 0.9722 |
| 10 | control | `ana` | 33 | 33 | 0.9714 | 1.000 | 0.9714 |
| 11 | control | `tem` | 56 | 55 | 0.9655 | 1.000 | 0.9655 |
| 12 | control | `ete` | 131 | 127 | 0.9624 | 1.000 | 0.9624 |
| 13 | substrate | `omali` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 14 | substrate | `siatas` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `wantai` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | control | `nadina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 17 | control | `dnta` | 23 | 23 | 0.9600 | 1.000 | 0.9600 |
| 18 | substrate | `arka` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 19 | substrate | `sante` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 20 | control | `iphai` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 21 | control | `ieti` | 163 | 154 | 0.9394 | 1.000 | 0.9394 |
| 22 | control | `ima` | 44 | 42 | 0.9348 | 1.000 | 0.9348 |
| 23 | control | `pepim` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 24 | control | `mari` | 74 | 68 | 0.9079 | 1.000 | 0.9079 |
| 25 | control | `iamet` | 190 | 173 | 0.9062 | 1.000 | 0.9062 |
| 26 | substrate | `si` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 27 | control | `iaiete` | 42 | 37 | 0.8636 | 1.000 | 0.8636 |
| 28 | control | `owaiais` | 21 | 18 | 0.8261 | 1.000 | 0.8261 |
| 29 | substrate | `sametion` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 30 | substrate | `zethante` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 31 | control | `iowup` | 31 | 26 | 0.8182 | 1.000 | 0.8182 |
| 32 | substrate | `iareion` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 33 | substrate | `omalioi` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 34 | substrate | `noi` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 35 | control | `ka` | 100 | 79 | 0.7843 | 1.000 | 0.7843 |
| 36 | control | `alan` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 37 | substrate | `niate` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 38 | substrate | `etion` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 39 | substrate | `ieroi` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 40 | control | `phanw` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 41 | substrate | `epimere` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 42 | substrate | `komnai` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 43 | substrate | `natoniate` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 44 | substrate | `parsiphai` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 45 | control | `ipisa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 46 | control | `isar` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 47 | substrate | `omosai` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 48 | substrate | `inaiperima` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 49 | substrate | `sameti` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 50 | substrate | `epioi` | 50 | 32 | 0.6346 | 1.000 | 0.6346 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `eteocretan` (20 top surfaces). Control pool: `control_eteocretan_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

