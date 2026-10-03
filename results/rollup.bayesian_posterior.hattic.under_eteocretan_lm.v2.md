# v23 cross-LM gate — hattic substrate under Eteocretan LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the hattic substrate pool PASSes the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Eteocretan LM at p=9.204e-06** (median substrate posterior 0.9808 vs median control posterior 0.8750; gap +0.1058).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Eteocretan | 20 | 20 | 0.9808 | 0.8750 | 356.5 | 9.204e-06 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9577. Mean of top-20 control posterior_mean: 0.8767. Gap (median, gate-relevant): +0.1058; gap (mean): +0.0810. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `her` | 50 | 50 | 0.9808 | `tar` | 50 | 50 | 0.9808 |
| 2 | `iah` | 50 | 50 | 0.9808 | `wina` | 72 | 71 | 0.9730 |
| 3 | `mis` | 50 | 50 | 0.9808 | `pikipin` | 13 | 13 | 0.9333 |
| 4 | `pin` | 50 | 50 | 0.9808 | `wepa` | 26 | 25 | 0.9286 |
| 5 | `pu` | 50 | 50 | 0.9808 | `watte` | 56 | 52 | 0.9138 |
| 6 | `sa` | 50 | 50 | 0.9808 | `hini` | 8 | 8 | 0.9000 |
| 7 | `teh` | 50 | 50 | 0.9808 | `we` | 7 | 7 | 0.8889 |
| 8 | `tu` | 50 | 50 | 0.9808 | `zzi` | 7 | 7 | 0.8889 |
| 9 | `wae` | 50 | 50 | 0.9808 | `inelanasi` | 6 | 6 | 0.8750 |
| 10 | `wunan` | 50 | 50 | 0.9808 | `ppi` | 6 | 6 | 0.8750 |
| 11 | `zihar` | 50 | 50 | 0.9808 | `siawe` | 30 | 27 | 0.8750 |
| 12 | `hapras` | 24 | 24 | 0.9615 | `suwaste` | 13 | 12 | 0.8667 |
| 13 | `sepsep` | 24 | 24 | 0.9615 | `san` | 5 | 5 | 0.8571 |
| 14 | `tiuz` | 50 | 49 | 0.9615 | `ttau` | 5 | 5 | 0.8571 |
| 15 | `wel` | 50 | 49 | 0.9615 | `zakinsiazi` | 5 | 5 | 0.8571 |
| 16 | `sahis` | 50 | 48 | 0.9423 | `wuw` | 22 | 19 | 0.8333 |
| 17 | `parsiel` | 13 | 13 | 0.9333 | `akurstaste` | 9 | 8 | 0.8182 |
| 18 | `ippi` | 50 | 45 | 0.8846 | `nnarunas` | 14 | 12 | 0.8125 |
| 19 | `nes` | 50 | 45 | 0.8846 | `patapitetit` | 8 | 7 | 0.8000 |
| 20 | `iskinawar` | 6 | 6 | 0.8750 | `zanarutanirk` | 3 | 3 | 0.8000 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `her` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `iah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `mis` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `pin` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `pu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `sa` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `teh` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `tu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `wae` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `wunan` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `zihar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | control | `tar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | control | `wina` | 72 | 71 | 0.9730 | 1.000 | 0.9730 |
| 14 | substrate | `hapras` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `sepsep` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | substrate | `tiuz` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 17 | substrate | `wel` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 18 | substrate | `sahis` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 19 | substrate | `parsiel` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 20 | control | `pikipin` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 21 | control | `wepa` | 26 | 25 | 0.9286 | 1.000 | 0.9286 |
| 22 | control | `watte` | 56 | 52 | 0.9138 | 1.000 | 0.9138 |
| 23 | substrate | `ippi` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 24 | substrate | `nes` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 25 | control | `siawe` | 30 | 27 | 0.8750 | 1.000 | 0.8750 |
| 26 | control | `suwaste` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 27 | substrate | `estan` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 28 | substrate | `sakil` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 29 | control | `wuw` | 22 | 19 | 0.8333 | 1.000 | 0.8333 |
| 30 | substrate | `sinit` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 31 | control | `hini` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 32 | control | `nnarunas` | 14 | 12 | 0.8125 | 1.000 | 0.8125 |
| 33 | substrate | `arinna` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 34 | substrate | `niwas` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 35 | substrate | `taparna` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 36 | substrate | `zari` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 37 | control | `tars` | 106 | 84 | 0.7870 | 1.000 | 0.7870 |
| 38 | control | `akurstaste` | 9 | 8 | 0.8182 | 0.900 | 0.7864 |
| 39 | control | `we` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 40 | control | `zzi` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 41 | control | `mun` | 109 | 83 | 0.7568 | 1.000 | 0.7568 |
| 42 | control | `kakas` | 88 | 67 | 0.7556 | 1.000 | 0.7556 |
| 43 | control | `pipa` | 51 | 39 | 0.7547 | 1.000 | 0.7547 |
| 44 | control | `tassantu` | 18 | 14 | 0.7500 | 1.000 | 0.7500 |
| 45 | control | `zirarais` | 10 | 8 | 0.7500 | 1.000 | 0.7500 |
| 46 | control | `kasku` | 122 | 91 | 0.7419 | 1.000 | 0.7419 |
| 47 | substrate | `telipinu` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 48 | control | `patapitetit` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 49 | control | `wuli` | 21 | 16 | 0.7391 | 1.000 | 0.7391 |
| 50 | substrate | `haippin` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (label: Eteocretan). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

