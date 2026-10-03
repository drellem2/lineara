# v23 cross-LM gate — hattic substrate under Mycenaean Greek LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the hattic substrate pool PASSes the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Mycenaean Greek LM at p=4.294e-03** (median substrate posterior 0.9038 vs median control posterior 0.8452; gap +0.0586).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Mycenaean Greek | 20 | 20 | 0.9038 | 0.8452 | 297.5 | 4.294e-03 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9040. Mean of top-20 control posterior_mean: 0.8365. Gap (median, gate-relevant): +0.0586; gap (mean): +0.0675. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `katte` | 50 | 50 | 0.9808 | `ntepas` | 16 | 16 | 0.9444 |
| 2 | `lewae` | 50 | 50 | 0.9808 | `tuinina` | 33 | 32 | 0.9429 |
| 3 | `ankuwa` | 24 | 24 | 0.9615 | `katunami` | 15 | 15 | 0.9412 |
| 4 | `inar` | 50 | 49 | 0.9615 | `kinanaat` | 10 | 10 | 0.9167 |
| 5 | `kasku` | 50 | 49 | 0.9615 | `esturka` | 9 | 9 | 0.9091 |
| 6 | `katapa` | 24 | 24 | 0.9615 | `wuina` | 8 | 8 | 0.9000 |
| 7 | `wel` | 50 | 49 | 0.9615 | `zuintas` | 8 | 8 | 0.9000 |
| 8 | `halentu` | 13 | 13 | 0.9333 | `narunete` | 6 | 6 | 0.8750 |
| 9 | `kammama` | 13 | 13 | 0.9333 | `tapas` | 139 | 122 | 0.8723 |
| 10 | `kait` | 50 | 46 | 0.9038 | `ztitepi` | 5 | 5 | 0.8571 |
| 11 | `tete` | 50 | 46 | 0.9038 | `ammataz` | 4 | 4 | 0.8333 |
| 12 | `nuwa` | 50 | 45 | 0.8846 | `wamarule` | 9 | 8 | 0.8182 |
| 13 | `hanwasuit` | 6 | 6 | 0.8750 | `kapanas` | 64 | 52 | 0.8030 |
| 14 | `tastenuwa` | 6 | 6 | 0.8750 | `kalesten` | 7 | 6 | 0.7778 |
| 15 | `taru` | 50 | 44 | 0.8654 | `wazurru` | 15 | 12 | 0.7647 |
| 16 | `sulinkatte` | 5 | 5 | 0.8571 | `apilesep` | 2 | 2 | 0.7500 |
| 17 | `wurunkatte` | 5 | 5 | 0.8571 | `itunur` | 6 | 5 | 0.7500 |
| 18 | `katahzipuri` | 4 | 4 | 0.8333 | `kamana` | 102 | 76 | 0.7404 |
| 19 | `kastama` | 13 | 11 | 0.8000 | `esttal` | 28 | 21 | 0.7333 |
| 20 | `wur` | 50 | 40 | 0.7885 | `wari` | 78 | 55 | 0.7000 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `katte` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `lewae` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `ankuwa` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 4 | substrate | `inar` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 5 | substrate | `kasku` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 6 | substrate | `katapa` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 7 | substrate | `wel` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 8 | control | `ntepas` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 9 | control | `tuinina` | 33 | 32 | 0.9429 | 1.000 | 0.9429 |
| 10 | control | `katunami` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 11 | substrate | `halentu` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 12 | substrate | `kammama` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 13 | control | `kinanaat` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 14 | substrate | `kait` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 15 | substrate | `tete` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 16 | substrate | `nuwa` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 17 | control | `tapas` | 139 | 122 | 0.8723 | 1.000 | 0.8723 |
| 18 | control | `esturka` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 19 | substrate | `taru` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 20 | control | `wuina` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 21 | control | `zuintas` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 22 | control | `kapanas` | 64 | 52 | 0.8030 | 1.000 | 0.8030 |
| 23 | substrate | `kastama` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 24 | substrate | `wur` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 25 | control | `wamarule` | 9 | 8 | 0.8182 | 0.900 | 0.7864 |
| 26 | control | `wazurru` | 15 | 12 | 0.7647 | 1.000 | 0.7647 |
| 27 | substrate | `an` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 28 | control | `kamana` | 102 | 76 | 0.7404 | 1.000 | 0.7404 |
| 29 | control | `esttal` | 28 | 21 | 0.7333 | 1.000 | 0.7333 |
| 30 | substrate | `pinu` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 31 | substrate | `hanwasuit` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 32 | substrate | `tastenuwa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 33 | control | `narunete` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 34 | control | `wari` | 78 | 55 | 0.7000 | 1.000 | 0.7000 |
| 35 | control | `kalesten` | 7 | 6 | 0.7778 | 0.700 | 0.6944 |
| 36 | substrate | `wintu` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 37 | control | `watuk` | 96 | 66 | 0.6837 | 1.000 | 0.6837 |
| 38 | substrate | `sulinkatte` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 39 | substrate | `wurunkatte` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 40 | control | `ztitepi` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 41 | substrate | `taparna` | 13 | 9 | 0.6667 | 1.000 | 0.6667 |
| 42 | substrate | `hapantali` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 43 | substrate | `tawananna` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 44 | control | `itunur` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 45 | control | `wa` | 42 | 27 | 0.6364 | 1.000 | 0.6364 |
| 46 | substrate | `estan` | 50 | 32 | 0.6346 | 1.000 | 0.6346 |
| 47 | substrate | `katahzipuri` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |
| 48 | control | `ammataz` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |
| 49 | control | `pinun` | 28 | 18 | 0.6333 | 1.000 | 0.6333 |
| 50 | substrate | `arinna` | 24 | 15 | 0.6154 | 1.000 | 0.6154 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `mycenaean_greek` (label: Mycenaean Greek). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

