# v23 cross-LM gate — hattic substrate under Mycenaean Greek LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the hattic substrate pool PASSes the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Mycenaean Greek LM at p=2.214e-03** (median substrate posterior 0.9712 vs median control posterior 0.9333; gap +0.0378).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Mycenaean Greek | 20 | 20 | 0.9712 | 0.9333 | 304.0 | 2.214e-03 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9598. Mean of top-20 control posterior_mean: 0.9373. Gap (median, gate-relevant): +0.0378; gap (mean): +0.0225. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `her` | 50 | 50 | 0.9808 | `tar` | 50 | 50 | 0.9808 |
| 2 | `kun` | 50 | 50 | 0.9808 | `tah` | 139 | 137 | 0.9787 |
| 3 | `mis` | 50 | 50 | 0.9808 | `ka` | 44 | 44 | 0.9783 |
| 4 | `narak` | 50 | 50 | 0.9808 | `sek` | 39 | 39 | 0.9756 |
| 5 | `pin` | 50 | 50 | 0.9808 | `siawe` | 30 | 30 | 0.9688 |
| 6 | `wae` | 50 | 50 | 0.9808 | `tetu` | 27 | 27 | 0.9655 |
| 7 | `wunan` | 50 | 50 | 0.9808 | `tanana` | 76 | 74 | 0.9615 |
| 8 | `zaras` | 50 | 50 | 0.9808 | `kakas` | 88 | 84 | 0.9444 |
| 9 | `zia` | 50 | 50 | 0.9808 | `pikipin` | 13 | 13 | 0.9333 |
| 10 | `zik` | 50 | 50 | 0.9808 | `puttta` | 43 | 41 | 0.9333 |
| 11 | `pirpir` | 24 | 24 | 0.9615 | `suwaste` | 13 | 13 | 0.9333 |
| 12 | `sepsep` | 24 | 24 | 0.9615 | `wepa` | 26 | 25 | 0.9286 |
| 13 | `katte` | 50 | 48 | 0.9423 | `pipa` | 51 | 48 | 0.9245 |
| 14 | `haippin` | 13 | 13 | 0.9333 | `zirarais` | 10 | 10 | 0.9167 |
| 15 | `halawes` | 13 | 13 | 0.9333 | `sappa` | 21 | 20 | 0.9130 |
| 16 | `hanniku` | 13 | 13 | 0.9333 | `kasku` | 122 | 112 | 0.9113 |
| 17 | `parsiel` | 13 | 13 | 0.9333 | `akurstaste` | 9 | 9 | 0.9091 |
| 18 | `taparna` | 13 | 13 | 0.9333 | `patapitetit` | 8 | 8 | 0.9000 |
| 19 | `zaparwa` | 13 | 13 | 0.9333 | `pahik` | 84 | 76 | 0.8953 |
| 20 | `taru` | 50 | 47 | 0.9231 | `tines` | 83 | 75 | 0.8941 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `her` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `kun` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `mis` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `narak` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `pin` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `wae` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `wunan` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `zaras` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `zia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `zik` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | control | `tar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | control | `tah` | 139 | 137 | 0.9787 | 1.000 | 0.9787 |
| 13 | control | `ka` | 44 | 44 | 0.9783 | 1.000 | 0.9783 |
| 14 | control | `sek` | 39 | 39 | 0.9756 | 1.000 | 0.9756 |
| 15 | control | `siawe` | 30 | 30 | 0.9688 | 1.000 | 0.9688 |
| 16 | control | `tetu` | 27 | 27 | 0.9655 | 1.000 | 0.9655 |
| 17 | substrate | `pirpir` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 18 | substrate | `sepsep` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 19 | control | `tanana` | 76 | 74 | 0.9615 | 1.000 | 0.9615 |
| 20 | control | `kakas` | 88 | 84 | 0.9444 | 1.000 | 0.9444 |
| 21 | substrate | `katte` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 22 | substrate | `haippin` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 23 | substrate | `halawes` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 24 | substrate | `hanniku` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 25 | substrate | `parsiel` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 26 | substrate | `taparna` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 27 | substrate | `zaparwa` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 28 | control | `pikipin` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 29 | control | `puttta` | 43 | 41 | 0.9333 | 1.000 | 0.9333 |
| 30 | control | `suwaste` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 31 | control | `wepa` | 26 | 25 | 0.9286 | 1.000 | 0.9286 |
| 32 | control | `pipa` | 51 | 48 | 0.9245 | 1.000 | 0.9245 |
| 33 | substrate | `taru` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 34 | control | `zirarais` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 35 | control | `sappa` | 21 | 20 | 0.9130 | 1.000 | 0.9130 |
| 36 | control | `kasku` | 122 | 112 | 0.9113 | 1.000 | 0.9113 |
| 37 | substrate | `ippi` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 38 | control | `pahik` | 84 | 76 | 0.8953 | 1.000 | 0.8953 |
| 39 | control | `tines` | 83 | 75 | 0.8941 | 1.000 | 0.8941 |
| 40 | substrate | `tiuz` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 41 | substrate | `zihar` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 42 | control | `psak` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 43 | control | `akurstaste` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 44 | control | `kapian` | 66 | 56 | 0.8382 | 1.000 | 0.8382 |
| 45 | control | `wana` | 59 | 50 | 0.8361 | 1.000 | 0.8361 |
| 46 | substrate | `estan` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 47 | substrate | `kut` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 48 | control | `patapitetit` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 49 | substrate | `huru` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 50 | substrate | `put` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `mycenaean_greek` (label: Mycenaean Greek). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

