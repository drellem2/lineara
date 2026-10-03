# v23 cross-LM gate — hattic substrate under Basque LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the hattic substrate pool FAILs the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Basque LM at p=9.975e-01** (median substrate posterior 0.7321 vs median control posterior 0.8545; gap -0.1224). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Basque | 20 | 20 | 0.7321 | 0.8545 | 97.0 | 9.975e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.7661. Mean of top-20 control posterior_mean: 0.8633. Gap (median, gate-relevant): -0.1224; gap (mean): -0.0971. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `zari` | 50 | 50 | 0.9808 | `kamana` | 102 | 101 | 0.9808 |
| 2 | `katah` | 50 | 49 | 0.9615 | `zap` | 24 | 24 | 0.9615 |
| 3 | `hapantali` | 6 | 6 | 0.8750 | `katunami` | 15 | 15 | 0.9412 |
| 4 | `hasammili` | 6 | 6 | 0.8750 | `zinte` | 63 | 60 | 0.9385 |
| 5 | `mezulla` | 13 | 12 | 0.8667 | `hal` | 59 | 56 | 0.9344 |
| 6 | `an` | 50 | 44 | 0.8654 | `wuina` | 8 | 8 | 0.9000 |
| 7 | `estan` | 50 | 42 | 0.8269 | `kalesten` | 7 | 7 | 0.8889 |
| 8 | `kasku` | 50 | 41 | 0.8077 | `narunete` | 6 | 6 | 0.8750 |
| 9 | `nerik` | 50 | 39 | 0.7692 | `lina` | 80 | 70 | 0.8659 |
| 10 | `halentu` | 13 | 10 | 0.7333 | `tuinina` | 33 | 29 | 0.8571 |
| 11 | `kait` | 50 | 37 | 0.7308 | `kunu` | 52 | 45 | 0.8519 |
| 12 | `istarazzil` | 5 | 4 | 0.7143 | `ammataz` | 4 | 4 | 0.8333 |
| 13 | `sulinkatte` | 5 | 4 | 0.7143 | `esttal` | 28 | 24 | 0.8333 |
| 14 | `zippalanta` | 5 | 4 | 0.7143 | `kinanaat` | 10 | 9 | 0.8333 |
| 15 | `katte` | 50 | 35 | 0.6923 | `haka` | 19 | 16 | 0.8095 |
| 16 | `katahzipuri` | 4 | 3 | 0.6667 | `kanewahal` | 3 | 3 | 0.8000 |
| 17 | `ankuwa` | 24 | 16 | 0.6538 | `zuintas` | 8 | 7 | 0.8000 |
| 18 | `halmasuit` | 6 | 4 | 0.6250 | `taha` | 67 | 54 | 0.7971 |
| 19 | `hanwasuit` | 6 | 4 | 0.6250 | `zasun` | 68 | 54 | 0.7857 |
| 20 | `tawananna` | 6 | 4 | 0.6250 | `kaninastu` | 7 | 6 | 0.7778 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `zari` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | control | `kamana` | 102 | 101 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `katah` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 4 | control | `zap` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 5 | control | `katunami` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 6 | control | `zinte` | 63 | 60 | 0.9385 | 1.000 | 0.9385 |
| 7 | control | `hal` | 59 | 56 | 0.9344 | 1.000 | 0.9344 |
| 8 | substrate | `mezulla` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 9 | control | `lina` | 80 | 70 | 0.8659 | 1.000 | 0.8659 |
| 10 | substrate | `an` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 11 | control | `tuinina` | 33 | 29 | 0.8571 | 1.000 | 0.8571 |
| 12 | control | `kunu` | 52 | 45 | 0.8519 | 1.000 | 0.8519 |
| 13 | control | `esttal` | 28 | 24 | 0.8333 | 1.000 | 0.8333 |
| 14 | control | `kinanaat` | 10 | 9 | 0.8333 | 1.000 | 0.8333 |
| 15 | substrate | `estan` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 16 | control | `wuina` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 17 | control | `haka` | 19 | 16 | 0.8095 | 1.000 | 0.8095 |
| 18 | substrate | `kasku` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 19 | control | `taha` | 67 | 54 | 0.7971 | 1.000 | 0.7971 |
| 20 | control | `zasun` | 68 | 54 | 0.7857 | 1.000 | 0.7857 |
| 21 | control | `kalesten` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 22 | substrate | `nerik` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 23 | control | `kapanas` | 64 | 48 | 0.7424 | 1.000 | 0.7424 |
| 24 | control | `zuintas` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 25 | substrate | `halentu` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 26 | substrate | `kait` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 27 | substrate | `hapantali` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 28 | substrate | `hasammili` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 29 | control | `narunete` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 30 | control | `kaninastu` | 7 | 6 | 0.7778 | 0.700 | 0.6944 |
| 31 | control | `zurpal` | 7 | 6 | 0.7778 | 0.700 | 0.6944 |
| 32 | substrate | `katte` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 33 | control | `linam` | 67 | 46 | 0.6812 | 1.000 | 0.6812 |
| 34 | substrate | `ankuwa` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 35 | control | `ayami` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 36 | control | `ammataz` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |
| 37 | control | `kammazi` | 22 | 14 | 0.6250 | 1.000 | 0.6250 |
| 38 | control | `wamarule` | 9 | 6 | 0.6364 | 0.900 | 0.6227 |
| 39 | substrate | `istarazzil` | 5 | 4 | 0.7143 | 0.500 | 0.6071 |
| 40 | substrate | `sulinkatte` | 5 | 4 | 0.7143 | 0.500 | 0.6071 |
| 41 | substrate | `zippalanta` | 5 | 4 | 0.7143 | 0.500 | 0.6071 |
| 42 | control | `za` | 58 | 35 | 0.6000 | 1.000 | 0.6000 |
| 43 | substrate | `zalpa` | 50 | 30 | 0.5962 | 1.000 | 0.5962 |
| 44 | control | `kanewahal` | 3 | 3 | 0.8000 | 0.300 | 0.5900 |
| 45 | control | `letenurul` | 10 | 6 | 0.5833 | 1.000 | 0.5833 |
| 46 | substrate | `halmasuit` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |
| 47 | substrate | `hanwasuit` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |
| 48 | substrate | `tawananna` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |
| 49 | substrate | `zashapuna` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |
| 50 | substrate | `katahzipuri` | 4 | 3 | 0.6667 | 0.400 | 0.5667 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `basque` (label: Basque). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

