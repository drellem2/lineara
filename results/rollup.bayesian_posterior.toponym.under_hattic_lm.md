# v23 cross-LM gate — toponym substrate under Hattic LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the toponym substrate pool FAILs the v10 right-tail bayesian gate against control_toponym_bigram when both sides are scored under the Hattic LM at p=5.228e-02** (median substrate posterior 0.9712 vs median control posterior 0.9149; gap +0.0563). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| toponym | control_toponym_bigram | Hattic | 20 | 20 | 0.9712 | 0.9149 | 260.0 | 5.228e-02 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9439. Mean of top-20 control posterior_mean: 0.9180. Gap (median, gate-relevant): +0.0563; gap (mean): +0.0259. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `aksos` | 50 | 50 | 0.9808 | `pales` | 130 | 130 | 0.9924 |
| 2 | `ala` | 50 | 50 | 0.9808 | `tenthe` | 76 | 76 | 0.9872 |
| 3 | `aso` | 50 | 50 | 0.9808 | `kto` | 58 | 58 | 0.9833 |
| 4 | `assos` | 50 | 50 | 0.9808 | `taia` | 35 | 34 | 0.9459 |
| 5 | `ina` | 50 | 50 | 0.9808 | `akaintha` | 16 | 16 | 0.9444 |
| 6 | `lukia` | 50 | 50 | 0.9808 | `luarasa` | 15 | 15 | 0.9412 |
| 7 | `ntha` | 50 | 50 | 0.9808 | `thelak` | 60 | 57 | 0.9355 |
| 8 | `phai` | 50 | 50 | 0.9808 | `arin` | 60 | 56 | 0.9194 |
| 9 | `smu` | 50 | 50 | 0.9808 | `lel` | 118 | 109 | 0.9167 |
| 10 | `tarra` | 50 | 50 | 0.9808 | `tak` | 10 | 10 | 0.9167 |
| 11 | `gortyn` | 24 | 24 | 0.9615 | `inaletos` | 44 | 41 | 0.9130 |
| 12 | `naxos` | 24 | 24 | 0.9615 | `lzkukai` | 9 | 9 | 0.9091 |
| 13 | `hua` | 50 | 47 | 0.9231 | `tar` | 111 | 101 | 0.9027 |
| 14 | `iassos` | 24 | 23 | 0.9231 | `krs` | 8 | 8 | 0.9000 |
| 15 | `kuthera` | 24 | 23 | 0.9231 | `alpaia` | 67 | 61 | 0.8986 |
| 16 | `chios` | 50 | 46 | 0.9038 | `nthoi` | 170 | 151 | 0.8837 |
| 17 | `smurna` | 24 | 22 | 0.8846 | `ain` | 6 | 6 | 0.8750 |
| 18 | `parnassos` | 6 | 6 | 0.8750 | `kaiksals` | 6 | 6 | 0.8750 |
| 19 | `hierapytna` | 5 | 5 | 0.8571 | `alnisso` | 20 | 18 | 0.8636 |
| 20 | `phalasarna` | 5 | 5 | 0.8571 | `aphutasalos` | 5 | 5 | 0.8571 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `pales` | 130 | 130 | 0.9924 | 1.000 | 0.9924 |
| 2 | control | `tenthe` | 76 | 76 | 0.9872 | 1.000 | 0.9872 |
| 3 | control | `kto` | 58 | 58 | 0.9833 | 1.000 | 0.9833 |
| 4 | substrate | `aksos` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `ala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `aso` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `assos` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `ina` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `lukia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `ntha` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `phai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `smu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `tarra` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 14 | substrate | `gortyn` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `naxos` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | control | `taia` | 35 | 34 | 0.9459 | 1.000 | 0.9459 |
| 17 | control | `akaintha` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 18 | control | `luarasa` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 19 | control | `thelak` | 60 | 57 | 0.9355 | 1.000 | 0.9355 |
| 20 | substrate | `hua` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 21 | substrate | `iassos` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 22 | substrate | `kuthera` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 23 | control | `arin` | 60 | 56 | 0.9194 | 1.000 | 0.9194 |
| 24 | control | `lel` | 118 | 109 | 0.9167 | 1.000 | 0.9167 |
| 25 | control | `tak` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 26 | control | `inaletos` | 44 | 41 | 0.9130 | 1.000 | 0.9130 |
| 27 | substrate | `chios` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 28 | control | `tar` | 111 | 101 | 0.9027 | 1.000 | 0.9027 |
| 29 | control | `alpaia` | 67 | 61 | 0.8986 | 1.000 | 0.8986 |
| 30 | substrate | `smurna` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 31 | control | `nthoi` | 170 | 151 | 0.8837 | 1.000 | 0.8837 |
| 32 | control | `lzkukai` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 33 | control | `alnisso` | 20 | 18 | 0.8636 | 1.000 | 0.8636 |
| 34 | control | `ham` | 73 | 63 | 0.8533 | 1.000 | 0.8533 |
| 35 | substrate | `lyktos` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 36 | control | `tte` | 17 | 15 | 0.8421 | 1.000 | 0.8421 |
| 37 | control | `krs` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 38 | control | `abeti` | 36 | 30 | 0.8158 | 1.000 | 0.8158 |
| 39 | substrate | `lebena` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 40 | substrate | `thera` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 41 | substrate | `tulisos` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 42 | substrate | `tos` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 43 | substrate | `melitos` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 44 | substrate | `parnassos` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 45 | control | `ain` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 46 | control | `kaiksals` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 47 | control | `airso` | 26 | 19 | 0.7143 | 1.000 | 0.7143 |
| 48 | control | `ttr` | 78 | 56 | 0.7125 | 1.000 | 0.7125 |
| 49 | substrate | `ida` | 50 | 36 | 0.7115 | 1.000 | 0.7115 |
| 50 | substrate | `ther` | 50 | 36 | 0.7115 | 1.000 | 0.7115 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `toponym` (20 top surfaces). Control pool: `control_toponym_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

