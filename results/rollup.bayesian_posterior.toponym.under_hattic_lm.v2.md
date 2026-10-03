# v23 cross-LM gate — toponym substrate under Hattic LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the toponym substrate pool PASSes the v10 right-tail bayesian gate against control_toponym_bigram when both sides are scored under the Hattic LM at p=3.082e-02** (median substrate posterior 0.9712 vs median control posterior 0.8974; gap +0.0738).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| toponym | control_toponym_bigram | Hattic | 20 | 20 | 0.9712 | 0.8974 | 269.0 | 3.082e-02 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9458. Mean of top-20 control posterior_mean: 0.9106. Gap (median, gate-relevant): +0.0738; gap (mean): +0.0352. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `ala` | 50 | 50 | 0.9808 | `pales` | 130 | 130 | 0.9924 |
| 2 | `aso` | 50 | 50 | 0.9808 | `tenthe` | 76 | 76 | 0.9872 |
| 3 | `assos` | 50 | 50 | 0.9808 | `kto` | 58 | 58 | 0.9833 |
| 4 | `ina` | 50 | 50 | 0.9808 | `taia` | 35 | 35 | 0.9730 |
| 5 | `lukia` | 50 | 50 | 0.9808 | `humu` | 17 | 17 | 0.9474 |
| 6 | `ntha` | 50 | 50 | 0.9808 | `luarasa` | 15 | 15 | 0.9412 |
| 7 | `phai` | 50 | 50 | 0.9808 | `iss` | 14 | 14 | 0.9375 |
| 8 | `smu` | 50 | 50 | 0.9808 | `thelak` | 60 | 57 | 0.9355 |
| 9 | `tarra` | 50 | 50 | 0.9808 | `phumnak` | 11 | 11 | 0.9231 |
| 10 | `tul` | 50 | 50 | 0.9808 | `krs` | 8 | 8 | 0.9000 |
| 11 | `gortyn` | 24 | 24 | 0.9615 | `abeti` | 36 | 33 | 0.8947 |
| 12 | `iassos` | 24 | 24 | 0.9615 | `akuthe` | 7 | 7 | 0.8889 |
| 13 | `naxos` | 24 | 24 | 0.9615 | `lel` | 118 | 105 | 0.8833 |
| 14 | `tiruns` | 24 | 24 | 0.9615 | `tar` | 111 | 98 | 0.8761 |
| 15 | `tulisos` | 13 | 13 | 0.9333 | `ain` | 6 | 6 | 0.8750 |
| 16 | `lyktos` | 24 | 22 | 0.8846 | `kaiksals` | 6 | 6 | 0.8750 |
| 17 | `smurna` | 24 | 22 | 0.8846 | `arin` | 60 | 53 | 0.8710 |
| 18 | `hierapytna` | 5 | 5 | 0.8571 | `aphutasalos` | 5 | 5 | 0.8571 |
| 19 | `phalasarna` | 5 | 5 | 0.8571 | `nthoi` | 170 | 143 | 0.8372 |
| 20 | `hua` | 50 | 43 | 0.8462 | `akaintha` | 16 | 14 | 0.8333 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `pales` | 130 | 130 | 0.9924 | 1.000 | 0.9924 |
| 2 | control | `tenthe` | 76 | 76 | 0.9872 | 1.000 | 0.9872 |
| 3 | control | `kto` | 58 | 58 | 0.9833 | 1.000 | 0.9833 |
| 4 | substrate | `ala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `aso` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `assos` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `ina` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `lukia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `ntha` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `phai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `smu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `tarra` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `tul` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 14 | control | `taia` | 35 | 35 | 0.9730 | 1.000 | 0.9730 |
| 15 | substrate | `gortyn` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | substrate | `iassos` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 17 | substrate | `naxos` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 18 | substrate | `tiruns` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 19 | control | `humu` | 17 | 17 | 0.9474 | 1.000 | 0.9474 |
| 20 | control | `luarasa` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 21 | control | `iss` | 14 | 14 | 0.9375 | 1.000 | 0.9375 |
| 22 | control | `thelak` | 60 | 57 | 0.9355 | 1.000 | 0.9355 |
| 23 | substrate | `tulisos` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 24 | control | `phumnak` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 25 | control | `abeti` | 36 | 33 | 0.8947 | 1.000 | 0.8947 |
| 26 | substrate | `lyktos` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 27 | substrate | `smurna` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 28 | control | `lel` | 118 | 105 | 0.8833 | 1.000 | 0.8833 |
| 29 | control | `tar` | 111 | 98 | 0.8761 | 1.000 | 0.8761 |
| 30 | control | `arin` | 60 | 53 | 0.8710 | 1.000 | 0.8710 |
| 31 | substrate | `hua` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 32 | control | `nthoi` | 170 | 143 | 0.8372 | 1.000 | 0.8372 |
| 33 | control | `akaintha` | 16 | 14 | 0.8333 | 1.000 | 0.8333 |
| 34 | control | `krs` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 35 | control | `ham` | 73 | 60 | 0.8133 | 1.000 | 0.8133 |
| 36 | substrate | `lebena` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 37 | control | `akuthe` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 38 | control | `lioss` | 55 | 43 | 0.7719 | 1.000 | 0.7719 |
| 39 | substrate | `lasaia` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 40 | substrate | `lemnos` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 41 | control | `huiksos` | 60 | 46 | 0.7581 | 1.000 | 0.7581 |
| 42 | control | `thos` | 39 | 30 | 0.7561 | 1.000 | 0.7561 |
| 43 | substrate | `phaistos` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 44 | substrate | `melitos` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 45 | control | `ain` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 46 | control | `kaiksals` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 47 | control | `inaletos` | 44 | 32 | 0.7174 | 1.000 | 0.7174 |
| 48 | control | `hudrmn` | 7 | 6 | 0.7778 | 0.700 | 0.6944 |
| 49 | control | `thosp` | 60 | 42 | 0.6935 | 1.000 | 0.6935 |
| 50 | control | `alnisso` | 20 | 14 | 0.6818 | 1.000 | 0.6818 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `toponym` (20 top surfaces). Control pool: `control_toponym_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

