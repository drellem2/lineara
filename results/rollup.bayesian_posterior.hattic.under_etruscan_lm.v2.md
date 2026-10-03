# v23 cross-LM gate — hattic substrate under Etruscan LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the hattic substrate pool PASSes the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Etruscan LM at p=4.741e-05** (median substrate posterior 0.9712 vs median control posterior 0.8991; gap +0.0721).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Etruscan | 20 | 20 | 0.9712 | 0.8991 | 343.5 | 4.741e-05 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9619. Mean of top-20 control posterior_mean: 0.9028. Gap (median, gate-relevant): +0.0721; gap (mean): +0.0591. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `asah` | 50 | 50 | 0.9808 | `laras` | 120 | 120 | 0.9918 |
| 2 | `katte` | 50 | 50 | 0.9808 | `zehah` | 60 | 60 | 0.9839 |
| 3 | `mis` | 50 | 50 | 0.9808 | `tassantu` | 18 | 18 | 0.9500 |
| 4 | `pala` | 50 | 50 | 0.9808 | `heha` | 14 | 14 | 0.9375 |
| 5 | `pu` | 50 | 50 | 0.9808 | `tetu` | 27 | 26 | 0.9310 |
| 6 | `sa` | 50 | 50 | 0.9808 | `hileh` | 23 | 22 | 0.9200 |
| 7 | `tahil` | 50 | 50 | 0.9808 | `stul` | 10 | 10 | 0.9167 |
| 8 | `tu` | 50 | 50 | 0.9808 | `akurstaste` | 9 | 9 | 0.9091 |
| 9 | `zar` | 50 | 50 | 0.9808 | `wal` | 123 | 112 | 0.9040 |
| 10 | `zia` | 50 | 50 | 0.9808 | `hini` | 8 | 8 | 0.9000 |
| 11 | `hapras` | 24 | 24 | 0.9615 | `tars` | 106 | 96 | 0.8981 |
| 12 | `iah` | 50 | 49 | 0.9615 | `hunah` | 37 | 34 | 0.8974 |
| 13 | `kasuh` | 50 | 49 | 0.9615 | `eshahi` | 7 | 7 | 0.8889 |
| 14 | `lahzan` | 24 | 24 | 0.9615 | `zzi` | 7 | 7 | 0.8889 |
| 15 | `sepsep` | 24 | 24 | 0.9615 | `inelanasi` | 6 | 6 | 0.8750 |
| 16 | `sahis` | 50 | 48 | 0.9423 | `tines` | 83 | 72 | 0.8588 |
| 17 | `pipizil` | 13 | 13 | 0.9333 | `san` | 5 | 5 | 0.8571 |
| 18 | `alep` | 50 | 47 | 0.9231 | `ttau` | 5 | 5 | 0.8571 |
| 19 | `anna` | 50 | 47 | 0.9231 | `zakinsiazi` | 5 | 5 | 0.8571 |
| 20 | `hasammil` | 8 | 8 | 0.9000 | `zirarais` | 10 | 9 | 0.8333 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `laras` | 120 | 120 | 0.9918 | 1.000 | 0.9918 |
| 2 | control | `zehah` | 60 | 60 | 0.9839 | 1.000 | 0.9839 |
| 3 | substrate | `asah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `katte` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `mis` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `pala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `pu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `sa` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `tahil` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `tu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `zar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `zia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `hapras` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 14 | substrate | `iah` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `kasuh` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 16 | substrate | `lahzan` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 17 | substrate | `sepsep` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 18 | control | `tassantu` | 18 | 18 | 0.9500 | 1.000 | 0.9500 |
| 19 | substrate | `sahis` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 20 | control | `heha` | 14 | 14 | 0.9375 | 1.000 | 0.9375 |
| 21 | substrate | `pipizil` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 22 | control | `tetu` | 27 | 26 | 0.9310 | 1.000 | 0.9310 |
| 23 | substrate | `alep` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 24 | substrate | `anna` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 25 | control | `hileh` | 23 | 22 | 0.9200 | 1.000 | 0.9200 |
| 26 | control | `stul` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 27 | control | `wal` | 123 | 112 | 0.9040 | 1.000 | 0.9040 |
| 28 | control | `tars` | 106 | 96 | 0.8981 | 1.000 | 0.8981 |
| 29 | control | `hunah` | 37 | 34 | 0.8974 | 1.000 | 0.8974 |
| 30 | substrate | `shap` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 31 | control | `akurstaste` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 32 | control | `tines` | 83 | 72 | 0.8588 | 1.000 | 0.8588 |
| 33 | substrate | `sul` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 34 | control | `zirarais` | 10 | 9 | 0.8333 | 1.000 | 0.8333 |
| 35 | substrate | `hasammil` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 36 | substrate | `sahtaril` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 37 | control | `hini` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 38 | substrate | `sakil` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 39 | control | `hiuu` | 161 | 130 | 0.8037 | 1.000 | 0.8037 |
| 40 | substrate | `taparna` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 41 | control | `tanana` | 76 | 60 | 0.7821 | 1.000 | 0.7821 |
| 42 | control | `eshahi` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 43 | control | `zzi` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 44 | substrate | `kamar` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 45 | control | `heh` | 95 | 73 | 0.7629 | 1.000 | 0.7629 |
| 46 | control | `hamis` | 107 | 82 | 0.7615 | 1.000 | 0.7615 |
| 47 | control | `kasku` | 122 | 93 | 0.7581 | 1.000 | 0.7581 |
| 48 | substrate | `nes` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 49 | control | `haskzilak` | 10 | 8 | 0.7500 | 1.000 | 0.7500 |
| 50 | substrate | `estan` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `etruscan` (label: Etruscan). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

