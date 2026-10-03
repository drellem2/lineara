# v23 cross-LM gate — hattic substrate under Eteocretan LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the hattic substrate pool FAILs the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Eteocretan LM at p=7.334e-01** (median substrate posterior 0.7500 vs median control posterior 0.7868; gap -0.0368). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Eteocretan | 20 | 20 | 0.7500 | 0.7868 | 177.5 | 7.334e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.7816. Mean of top-20 control posterior_mean: 0.7966. Gap (median, gate-relevant): -0.0368; gap (mean): -0.0150. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `an` | 50 | 50 | 0.9808 | `wari` | 78 | 78 | 0.9875 |
| 2 | `arinna` | 24 | 24 | 0.9615 | `kapanas` | 64 | 61 | 0.9394 |
| 3 | `ankuwa` | 24 | 22 | 0.8846 | `tuinina` | 33 | 31 | 0.9143 |
| 4 | `tastenuwa` | 6 | 6 | 0.8750 | `esturka` | 9 | 9 | 0.9091 |
| 5 | `tawananna` | 6 | 6 | 0.8750 | `wuina` | 8 | 8 | 0.9000 |
| 6 | `teteshapi` | 6 | 6 | 0.8750 | `esttal` | 28 | 24 | 0.8333 |
| 7 | `il` | 50 | 43 | 0.8462 | `pinun` | 28 | 24 | 0.8333 |
| 8 | `estan` | 50 | 42 | 0.8269 | `tantusurili` | 4 | 4 | 0.8333 |
| 9 | `hasammili` | 6 | 5 | 0.7500 | `tapas` | 139 | 116 | 0.8298 |
| 10 | `istustaya` | 6 | 5 | 0.7500 | `katunami` | 15 | 13 | 0.8235 |
| 11 | `nuwa` | 50 | 38 | 0.7500 | `ayami` | 6 | 5 | 0.7500 |
| 12 | `wasezzili` | 6 | 5 | 0.7500 | `zasun` | 68 | 51 | 0.7429 |
| 13 | `tete` | 50 | 37 | 0.7308 | `wamarule` | 9 | 7 | 0.7273 |
| 14 | `telipinu` | 8 | 6 | 0.7000 | `ntepas` | 16 | 12 | 0.7222 |
| 15 | `kait` | 50 | 35 | 0.6923 | `ztitepi` | 5 | 4 | 0.7143 |
| 16 | `washap` | 24 | 17 | 0.6923 | `zinte` | 63 | 45 | 0.7077 |
| 17 | `wel` | 50 | 35 | 0.6923 | `kamana` | 102 | 72 | 0.7019 |
| 18 | `inar` | 50 | 34 | 0.6731 | `zuintas` | 8 | 6 | 0.7000 |
| 19 | `nerik` | 50 | 34 | 0.6731 | `pil` | 67 | 47 | 0.6957 |
| 20 | `wazari` | 24 | 16 | 0.6538 | `ammataz` | 4 | 3 | 0.6667 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `wari` | 78 | 78 | 0.9875 | 1.000 | 0.9875 |
| 2 | substrate | `an` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `arinna` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 4 | control | `kapanas` | 64 | 61 | 0.9394 | 1.000 | 0.9394 |
| 5 | control | `tuinina` | 33 | 31 | 0.9143 | 1.000 | 0.9143 |
| 6 | substrate | `ankuwa` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 7 | control | `esturka` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 8 | substrate | `il` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 9 | control | `esttal` | 28 | 24 | 0.8333 | 1.000 | 0.8333 |
| 10 | control | `pinun` | 28 | 24 | 0.8333 | 1.000 | 0.8333 |
| 11 | control | `tapas` | 139 | 116 | 0.8298 | 1.000 | 0.8298 |
| 12 | substrate | `estan` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 13 | control | `katunami` | 15 | 13 | 0.8235 | 1.000 | 0.8235 |
| 14 | control | `wuina` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 15 | substrate | `nuwa` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 16 | control | `zasun` | 68 | 51 | 0.7429 | 1.000 | 0.7429 |
| 17 | substrate | `tete` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 18 | substrate | `tastenuwa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 19 | substrate | `tawananna` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 20 | substrate | `teteshapi` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 21 | control | `ntepas` | 16 | 12 | 0.7222 | 1.000 | 0.7222 |
| 22 | control | `zinte` | 63 | 45 | 0.7077 | 1.000 | 0.7077 |
| 23 | control | `wamarule` | 9 | 7 | 0.7273 | 0.900 | 0.7045 |
| 24 | control | `kamana` | 102 | 72 | 0.7019 | 1.000 | 0.7019 |
| 25 | control | `pil` | 67 | 47 | 0.6957 | 1.000 | 0.6957 |
| 26 | substrate | `kait` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 27 | substrate | `washap` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 28 | substrate | `wel` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 29 | substrate | `inar` | 50 | 34 | 0.6731 | 1.000 | 0.6731 |
| 30 | substrate | `nerik` | 50 | 34 | 0.6731 | 1.000 | 0.6731 |
| 31 | control | `kinanaat` | 10 | 7 | 0.6667 | 1.000 | 0.6667 |
| 32 | substrate | `telipinu` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |
| 33 | control | `zuintas` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |
| 34 | substrate | `wazari` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 35 | substrate | `hasammili` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 36 | substrate | `istustaya` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 37 | substrate | `wasezzili` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 38 | control | `ayami` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 39 | control | `hipannuili` | 15 | 10 | 0.6471 | 1.000 | 0.6471 |
| 40 | control | `tantusurili` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |
| 41 | control | `zhawisuhi` | 9 | 6 | 0.6364 | 0.900 | 0.6227 |
| 42 | control | `estt` | 27 | 17 | 0.6207 | 1.000 | 0.6207 |
| 43 | control | `elist` | 32 | 20 | 0.6176 | 1.000 | 0.6176 |
| 44 | control | `kalesten` | 7 | 5 | 0.6667 | 0.700 | 0.6167 |
| 45 | substrate | `katte` | 50 | 31 | 0.6154 | 1.000 | 0.6154 |
| 46 | substrate | `pinu` | 50 | 31 | 0.6154 | 1.000 | 0.6154 |
| 47 | control | `linam` | 67 | 41 | 0.6087 | 1.000 | 0.6087 |
| 48 | control | `ztitepi` | 5 | 4 | 0.7143 | 0.500 | 0.6071 |
| 49 | substrate | `kastama` | 13 | 8 | 0.6000 | 1.000 | 0.6000 |
| 50 | substrate | `sul` | 50 | 30 | 0.5962 | 1.000 | 0.5962 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (label: Eteocretan). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

