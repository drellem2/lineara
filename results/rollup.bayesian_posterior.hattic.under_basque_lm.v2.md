# v23 cross-LM gate — hattic substrate under Basque LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the hattic substrate pool PASSes the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Basque LM at p=4.240e-02** (median substrate posterior 0.9808 vs median control posterior 0.8983; gap +0.0825).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Basque | 20 | 20 | 0.9808 | 0.8983 | 263.5 | 4.240e-02 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9435. Mean of top-20 control posterior_mean: 0.9126. Gap (median, gate-relevant): +0.0825; gap (mean): +0.0310. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `iah` | 50 | 50 | 0.9808 | `ku` | 115 | 115 | 0.9915 |
| 2 | `katte` | 50 | 50 | 0.9808 | `kakas` | 88 | 88 | 0.9889 |
| 3 | `kun` | 50 | 50 | 0.9808 | `lin` | 51 | 51 | 0.9811 |
| 4 | `narak` | 50 | 50 | 0.9808 | `ka` | 44 | 44 | 0.9783 |
| 5 | `taru` | 50 | 50 | 0.9808 | `za` | 34 | 34 | 0.9722 |
| 6 | `wae` | 50 | 50 | 0.9808 | `kasku` | 122 | 118 | 0.9597 |
| 7 | `wau` | 50 | 50 | 0.9808 | `zehah` | 60 | 58 | 0.9516 |
| 8 | `zar` | 50 | 50 | 0.9808 | `kazui` | 16 | 16 | 0.9444 |
| 9 | `zaras` | 50 | 50 | 0.9808 | `tanana` | 76 | 72 | 0.9359 |
| 10 | `zari` | 50 | 50 | 0.9808 | `hini` | 8 | 8 | 0.9000 |
| 11 | `zia` | 50 | 50 | 0.9808 | `tetu` | 27 | 25 | 0.8966 |
| 12 | `anna` | 50 | 48 | 0.9423 | `zzi` | 7 | 7 | 0.8889 |
| 13 | `tiuz` | 50 | 48 | 0.9423 | `tehaam` | 32 | 29 | 0.8824 |
| 14 | `hanniku` | 13 | 13 | 0.9333 | `inelanasi` | 6 | 6 | 0.8750 |
| 15 | `hasammil` | 8 | 8 | 0.9000 | `happak` | 28 | 25 | 0.8667 |
| 16 | `kaksazet` | 8 | 8 | 0.9000 | `san` | 5 | 5 | 0.8571 |
| 17 | `tawananna` | 6 | 6 | 0.8750 | `zakinsiazi` | 5 | 5 | 0.8571 |
| 18 | `wulasne` | 13 | 12 | 0.8667 | `zinilarit` | 5 | 5 | 0.8571 |
| 19 | `kut` | 50 | 44 | 0.8654 | `ikahiuna` | 4 | 4 | 0.8333 |
| 20 | `tetekuzzan` | 5 | 5 | 0.8571 | `zurilzakk` | 4 | 4 | 0.8333 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `ku` | 115 | 115 | 0.9915 | 1.000 | 0.9915 |
| 2 | control | `kakas` | 88 | 88 | 0.9889 | 1.000 | 0.9889 |
| 3 | control | `lin` | 51 | 51 | 0.9811 | 1.000 | 0.9811 |
| 4 | substrate | `iah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `katte` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `kun` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `narak` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `taru` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `wae` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `wau` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `zar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `zaras` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `zari` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 14 | substrate | `zia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 15 | control | `ka` | 44 | 44 | 0.9783 | 1.000 | 0.9783 |
| 16 | control | `za` | 34 | 34 | 0.9722 | 1.000 | 0.9722 |
| 17 | control | `kasku` | 122 | 118 | 0.9597 | 1.000 | 0.9597 |
| 18 | control | `zehah` | 60 | 58 | 0.9516 | 1.000 | 0.9516 |
| 19 | control | `kazui` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 20 | substrate | `anna` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 21 | substrate | `tiuz` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 22 | control | `tanana` | 76 | 72 | 0.9359 | 1.000 | 0.9359 |
| 23 | substrate | `hanniku` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 24 | control | `tetu` | 27 | 25 | 0.8966 | 1.000 | 0.8966 |
| 25 | control | `tehaam` | 32 | 29 | 0.8824 | 1.000 | 0.8824 |
| 26 | substrate | `wulasne` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 27 | control | `happak` | 28 | 25 | 0.8667 | 1.000 | 0.8667 |
| 28 | substrate | `kut` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 29 | substrate | `ziapa` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 30 | substrate | `alep` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 31 | control | `kapian` | 66 | 55 | 0.8235 | 1.000 | 0.8235 |
| 32 | substrate | `hasammil` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 33 | substrate | `kaksazet` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 34 | control | `hini` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 35 | control | `kunah` | 58 | 48 | 0.8167 | 1.000 | 0.8167 |
| 36 | substrate | `nes` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 37 | substrate | `hapalki` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 38 | substrate | `asah` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 39 | substrate | `pala` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 40 | substrate | `sakil` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 41 | control | `zzi` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 42 | substrate | `sahis` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 43 | substrate | `sepsep` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 44 | substrate | `takkehal` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 45 | substrate | `halawes` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 46 | substrate | `zintuhi` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 47 | substrate | `antiu` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 48 | substrate | `huzzia` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 49 | substrate | `ures` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 50 | substrate | `tawananna` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `basque` (label: Basque). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

