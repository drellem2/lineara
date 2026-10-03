# v23 cross-LM gate — etruscan substrate under Hattic LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the etruscan substrate pool FAILs the v10 right-tail bayesian gate against control_etruscan when both sides are scored under the Hattic LM at p=5.752e-01** (median substrate posterior 0.9142 vs median control posterior 0.9157; gap -0.0015). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| etruscan | control_etruscan | Hattic | 20 | 20 | 0.9142 | 0.9157 | 193.5 | 5.752e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9138. Mean of top-20 control posterior_mean: 0.9175. Gap (median, gate-relevant): -0.0015; gap (mean): -0.0037. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `capi` | 50 | 50 | 0.9808 | `thia` | 138 | 138 | 0.9929 |
| 2 | `chimth` | 50 | 50 | 0.9808 | `aiph` | 114 | 113 | 0.9828 |
| 3 | `laris` | 50 | 50 | 0.9808 | `pheei` | 24 | 24 | 0.9615 |
| 4 | `suthi` | 50 | 50 | 0.9808 | `zltha` | 41 | 40 | 0.9535 |
| 5 | `larth` | 54 | 53 | 0.9643 | `izththuch` | 39 | 38 | 0.9512 |
| 6 | `hanthe` | 50 | 49 | 0.9615 | `la` | 54 | 52 | 0.9464 |
| 7 | `hinthial` | 13 | 13 | 0.9333 | `atti` | 16 | 16 | 0.9444 |
| 8 | `thanchvil` | 13 | 13 | 0.9333 | `hsaa` | 16 | 16 | 0.9444 |
| 9 | `zelar` | 50 | 47 | 0.9231 | `tthlain` | 13 | 13 | 0.9333 |
| 10 | `ipei` | 60 | 56 | 0.9194 | `thi` | 1725 | 1592 | 0.9224 |
| 11 | `lautnitha` | 9 | 9 | 0.9091 | `ae` | 42 | 39 | 0.9091 |
| 12 | `aule` | 50 | 46 | 0.9038 | `iat` | 80 | 73 | 0.9024 |
| 13 | `sech` | 50 | 46 | 0.9038 | `ithalr` | 17 | 16 | 0.8947 |
| 14 | `thapna` | 50 | 46 | 0.9038 | `uaeapa` | 7 | 7 | 0.8889 |
| 15 | `hilarthune` | 6 | 6 | 0.8750 | `srchlcn` | 24 | 22 | 0.8846 |
| 16 | `velcitanus` | 5 | 5 | 0.8571 | `iaae` | 6 | 6 | 0.8750 |
| 17 | `avil` | 50 | 43 | 0.8462 | `iazs` | 6 | 6 | 0.8750 |
| 18 | `caitim` | 24 | 21 | 0.8462 | `thipti` | 38 | 34 | 0.8750 |
| 19 | `thana` | 50 | 43 | 0.8462 | `aan` | 1243 | 1066 | 0.8570 |
| 20 | `tinia` | 50 | 42 | 0.8269 | `neeui` | 88 | 76 | 0.8556 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `thia` | 138 | 138 | 0.9929 | 1.000 | 0.9929 |
| 2 | control | `aiph` | 114 | 113 | 0.9828 | 1.000 | 0.9828 |
| 3 | substrate | `capi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `chimth` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `laris` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `suthi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `larth` | 54 | 53 | 0.9643 | 1.000 | 0.9643 |
| 8 | substrate | `hanthe` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 9 | control | `pheei` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 10 | control | `zltha` | 41 | 40 | 0.9535 | 1.000 | 0.9535 |
| 11 | control | `izththuch` | 39 | 38 | 0.9512 | 1.000 | 0.9512 |
| 12 | control | `la` | 54 | 52 | 0.9464 | 1.000 | 0.9464 |
| 13 | control | `atti` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 14 | control | `hsaa` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 15 | substrate | `hinthial` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 16 | substrate | `thanchvil` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 17 | control | `tthlain` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 18 | substrate | `zelar` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 19 | control | `thi` | 1725 | 1592 | 0.9224 | 1.000 | 0.9224 |
| 20 | substrate | `ipei` | 60 | 56 | 0.9194 | 1.000 | 0.9194 |
| 21 | control | `ae` | 42 | 39 | 0.9091 | 1.000 | 0.9091 |
| 22 | substrate | `aule` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 23 | substrate | `sech` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 24 | substrate | `thapna` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 25 | control | `iat` | 80 | 73 | 0.9024 | 1.000 | 0.9024 |
| 26 | control | `ithalr` | 17 | 16 | 0.8947 | 1.000 | 0.8947 |
| 27 | control | `srchlcn` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 28 | control | `thipti` | 38 | 34 | 0.8750 | 1.000 | 0.8750 |
| 29 | substrate | `lautnitha` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 30 | control | `aan` | 1243 | 1066 | 0.8570 | 1.000 | 0.8570 |
| 31 | control | `neeui` | 88 | 76 | 0.8556 | 1.000 | 0.8556 |
| 32 | control | `laaeca` | 45 | 39 | 0.8511 | 1.000 | 0.8511 |
| 33 | substrate | `avil` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 34 | substrate | `caitim` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 35 | substrate | `thana` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 36 | control | `ithalam` | 22 | 19 | 0.8333 | 1.000 | 0.8333 |
| 37 | substrate | `tinia` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 38 | control | `aeana` | 316 | 259 | 0.8176 | 1.000 | 0.8176 |
| 39 | substrate | `lautni` | 25 | 21 | 0.8148 | 1.000 | 0.8148 |
| 40 | substrate | `arnth` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 41 | substrate | `cilth` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 42 | substrate | `maru` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 43 | substrate | `turce` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 44 | control | `iilie` | 139 | 110 | 0.7872 | 1.000 | 0.7872 |
| 45 | control | `aht` | 12 | 10 | 0.7857 | 1.000 | 0.7857 |
| 46 | substrate | `ziche` | 53 | 42 | 0.7818 | 1.000 | 0.7818 |
| 47 | substrate | `ati` | 57 | 45 | 0.7797 | 1.000 | 0.7797 |
| 48 | substrate | `ita` | 51 | 40 | 0.7736 | 1.000 | 0.7736 |
| 49 | control | `uaeapa` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 50 | substrate | `trutnu` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `etruscan` (20 top surfaces). Control pool: `control_etruscan` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

