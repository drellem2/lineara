# v23 cross-LM gate — etruscan substrate under Hattic LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the etruscan substrate pool FAILs the v10 right-tail bayesian gate against control_etruscan when both sides are scored under the Hattic LM at p=4.195e-01** (median substrate posterior 0.9245 vs median control posterior 0.9179; gap +0.0066). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| etruscan | control_etruscan | Hattic | 20 | 20 | 0.9245 | 0.9179 | 208.0 | 4.195e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9211. Mean of top-20 control posterior_mean: 0.9169. Gap (median, gate-relevant): +0.0066; gap (mean): +0.0042. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `laris` | 50 | 50 | 0.9808 | `la` | 54 | 53 | 0.9643 |
| 2 | `maru` | 50 | 50 | 0.9808 | `pheei` | 24 | 24 | 0.9615 |
| 3 | `hanthe` | 50 | 49 | 0.9615 | `ae` | 42 | 41 | 0.9545 |
| 4 | `śuthina` | 24 | 24 | 0.9615 | `atti` | 16 | 16 | 0.9444 |
| 5 | `suthi` | 50 | 48 | 0.9423 | `hsaa` | 16 | 16 | 0.9444 |
| 6 | `hinthial` | 13 | 13 | 0.9333 | `mialn` | 16 | 16 | 0.9444 |
| 7 | `penthuna` | 13 | 13 | 0.9333 | `eahss` | 15 | 15 | 0.9412 |
| 8 | `thunchulth` | 13 | 13 | 0.9333 | `ula` | 32 | 31 | 0.9412 |
| 9 | `larth` | 54 | 51 | 0.9286 | `zltha` | 41 | 39 | 0.9302 |
| 10 | `spural` | 25 | 24 | 0.9259 | `luua` | 100 | 93 | 0.9216 |
| 11 | `lauchum` | 24 | 23 | 0.9231 | `thia` | 138 | 127 | 0.9143 |
| 12 | `lautnitha` | 9 | 9 | 0.9091 | `aiph` | 114 | 104 | 0.9052 |
| 13 | `sath` | 50 | 46 | 0.9038 | `neeui` | 88 | 80 | 0.9000 |
| 14 | `thapna` | 50 | 46 | 0.9038 | `aasaas` | 57 | 52 | 0.8983 |
| 15 | `zelar` | 50 | 46 | 0.9038 | `sata` | 88 | 79 | 0.8889 |
| 16 | `lautni` | 25 | 23 | 0.8889 | `uaeapa` | 7 | 7 | 0.8889 |
| 17 | `caitim` | 24 | 22 | 0.8846 | `iat` | 80 | 71 | 0.8780 |
| 18 | `tinia` | 50 | 45 | 0.8846 | `iazs` | 6 | 6 | 0.8750 |
| 19 | `hilarthune` | 6 | 6 | 0.8750 | `ithalam` | 22 | 20 | 0.8750 |
| 20 | `huth` | 64 | 56 | 0.8636 | `tthlain` | 13 | 12 | 0.8667 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `laris` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `maru` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | control | `la` | 54 | 53 | 0.9643 | 1.000 | 0.9643 |
| 4 | substrate | `hanthe` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 5 | substrate | `śuthina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 6 | control | `pheei` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 7 | control | `ae` | 42 | 41 | 0.9545 | 1.000 | 0.9545 |
| 8 | control | `atti` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 9 | control | `hsaa` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 10 | control | `mialn` | 16 | 16 | 0.9444 | 1.000 | 0.9444 |
| 11 | substrate | `suthi` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 12 | control | `eahss` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 13 | control | `ula` | 32 | 31 | 0.9412 | 1.000 | 0.9412 |
| 14 | substrate | `hinthial` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 15 | substrate | `penthuna` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 16 | substrate | `thunchulth` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 17 | control | `zltha` | 41 | 39 | 0.9302 | 1.000 | 0.9302 |
| 18 | substrate | `larth` | 54 | 51 | 0.9286 | 1.000 | 0.9286 |
| 19 | substrate | `spural` | 25 | 24 | 0.9259 | 1.000 | 0.9259 |
| 20 | substrate | `lauchum` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 21 | control | `luua` | 100 | 93 | 0.9216 | 1.000 | 0.9216 |
| 22 | control | `thia` | 138 | 127 | 0.9143 | 1.000 | 0.9143 |
| 23 | control | `aiph` | 114 | 104 | 0.9052 | 1.000 | 0.9052 |
| 24 | substrate | `sath` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 25 | substrate | `thapna` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 26 | substrate | `zelar` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 27 | control | `neeui` | 88 | 80 | 0.9000 | 1.000 | 0.9000 |
| 28 | control | `aasaas` | 57 | 52 | 0.8983 | 1.000 | 0.8983 |
| 29 | substrate | `lautni` | 25 | 23 | 0.8889 | 1.000 | 0.8889 |
| 30 | control | `sata` | 88 | 79 | 0.8889 | 1.000 | 0.8889 |
| 31 | substrate | `caitim` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 32 | substrate | `tinia` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 33 | control | `iat` | 80 | 71 | 0.8780 | 1.000 | 0.8780 |
| 34 | control | `ithalam` | 22 | 20 | 0.8750 | 1.000 | 0.8750 |
| 35 | substrate | `lautnitha` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 36 | control | `tthlain` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 37 | substrate | `huth` | 64 | 56 | 0.8636 | 1.000 | 0.8636 |
| 38 | control | `izththuch` | 39 | 34 | 0.8537 | 1.000 | 0.8537 |
| 39 | substrate | `matam` | 52 | 45 | 0.8519 | 1.000 | 0.8519 |
| 40 | substrate | `capi` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 41 | substrate | `chimth` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 42 | substrate | `trutnu` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 43 | control | `aan` | 1243 | 1048 | 0.8426 | 1.000 | 0.8426 |
| 44 | control | `ithalr` | 17 | 15 | 0.8421 | 1.000 | 0.8421 |
| 45 | control | `senu` | 114 | 94 | 0.8190 | 1.000 | 0.8190 |
| 46 | substrate | `lautn` | 58 | 48 | 0.8167 | 1.000 | 0.8167 |
| 47 | substrate | `ipei` | 60 | 49 | 0.8065 | 1.000 | 0.8065 |
| 48 | control | `neie` | 174 | 138 | 0.7898 | 1.000 | 0.7898 |
| 49 | substrate | `tul` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 50 | control | `iilie` | 139 | 110 | 0.7872 | 1.000 | 0.7872 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `etruscan` (20 top surfaces). Control pool: `control_etruscan` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

