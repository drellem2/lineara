# v23 cross-LM gate — eteocretan substrate under Etruscan LM (mg-b599) — under Etruscan LM (cross-LM check)

**Headline: the eteocretan substrate pool PASSes the v10 right-tail bayesian gate against control_eteocretan_bigram when both sides are scored under the Etruscan LM at p=6.698e-03** (median substrate posterior 0.9378 vs median control posterior 0.8992; gap +0.0387).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | Etruscan | 20 | 20 | 0.9378 | 0.8992 | 291.5 | 6.698e-03 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9424. Mean of top-20 control posterior_mean: 0.8927. Gap (median, gate-relevant): +0.0387; gap (mean): +0.0497. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `ieme` | 50 | 50 | 0.9808 | `sal` | 50 | 50 | 0.9808 |
| 2 | `isala` | 50 | 50 | 0.9808 | `isai` | 97 | 96 | 0.9798 |
| 3 | `mete` | 50 | 50 | 0.9808 | `ima` | 44 | 44 | 0.9783 |
| 4 | `noi` | 50 | 50 | 0.9808 | `ial` | 34 | 34 | 0.9722 |
| 5 | `rima` | 50 | 50 | 0.9808 | `ana` | 33 | 33 | 0.9714 |
| 6 | `samet` | 50 | 50 | 0.9808 | `disa` | 49 | 48 | 0.9608 |
| 7 | `wai` | 50 | 50 | 0.9808 | `iphai` | 15 | 15 | 0.9412 |
| 8 | `ieroi` | 50 | 49 | 0.9615 | `pepim` | 12 | 12 | 0.9286 |
| 9 | `nato` | 50 | 49 | 0.9615 | `etaltat` | 48 | 45 | 0.9200 |
| 10 | `omali` | 50 | 48 | 0.9423 | `phai` | 110 | 100 | 0.9018 |
| 11 | `epimere` | 13 | 13 | 0.9333 | `tem` | 56 | 51 | 0.8966 |
| 12 | `sameti` | 24 | 23 | 0.9231 | `alan` | 7 | 7 | 0.8889 |
| 13 | `sante` | 50 | 47 | 0.9231 | `dnta` | 23 | 21 | 0.8800 |
| 14 | `si` | 50 | 47 | 0.9231 | `ipisa` | 6 | 6 | 0.8750 |
| 15 | `siatas` | 24 | 23 | 0.9231 | `isar` | 6 | 6 | 0.8750 |
| 16 | `arka` | 50 | 46 | 0.9038 | `ianteiarkal` | 4 | 4 | 0.8333 |
| 17 | `mi` | 50 | 46 | 0.9038 | `imaima` | 17 | 14 | 0.7895 |
| 18 | `sametion` | 8 | 8 | 0.9000 | `ete` | 131 | 103 | 0.7820 |
| 19 | `zethante` | 8 | 8 | 0.9000 | `inipina` | 2 | 2 | 0.7500 |
| 20 | `barkse` | 24 | 22 | 0.8846 | `ralu` | 2 | 2 | 0.7500 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `ieme` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `isala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `mete` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `noi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `rima` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `samet` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | control | `sal` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | control | `isai` | 97 | 96 | 0.9798 | 1.000 | 0.9798 |
| 10 | control | `ima` | 44 | 44 | 0.9783 | 1.000 | 0.9783 |
| 11 | control | `ial` | 34 | 34 | 0.9722 | 1.000 | 0.9722 |
| 12 | control | `ana` | 33 | 33 | 0.9714 | 1.000 | 0.9714 |
| 13 | substrate | `ieroi` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 14 | substrate | `nato` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 15 | control | `disa` | 49 | 48 | 0.9608 | 1.000 | 0.9608 |
| 16 | substrate | `omali` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 17 | control | `iphai` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 18 | substrate | `epimere` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 19 | control | `pepim` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 20 | substrate | `sameti` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 21 | substrate | `sante` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 22 | substrate | `si` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 23 | substrate | `siatas` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 24 | control | `etaltat` | 48 | 45 | 0.9200 | 1.000 | 0.9200 |
| 25 | substrate | `arka` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 26 | substrate | `mi` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 27 | control | `phai` | 110 | 100 | 0.9018 | 1.000 | 0.9018 |
| 28 | control | `tem` | 56 | 51 | 0.8966 | 1.000 | 0.8966 |
| 29 | substrate | `barkse` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 30 | control | `dnta` | 23 | 21 | 0.8800 | 1.000 | 0.8800 |
| 31 | substrate | `wantai` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 32 | substrate | `sametion` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 33 | substrate | `zethante` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 34 | substrate | `omalioi` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 35 | control | `imaima` | 17 | 14 | 0.7895 | 1.000 | 0.7895 |
| 36 | control | `ete` | 131 | 103 | 0.7820 | 1.000 | 0.7820 |
| 37 | control | `alan` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 38 | substrate | `omosai` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 39 | substrate | `isalabre` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 40 | substrate | `arkaginoi` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 41 | substrate | `naiperima` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 42 | substrate | `natoniate` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 43 | substrate | `omokrates` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 44 | substrate | `parsiphai` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 45 | control | `ipisa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 46 | control | `isar` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 47 | substrate | `magini` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 48 | substrate | `inaiperima` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 49 | control | `owaiais` | 21 | 14 | 0.6522 | 1.000 | 0.6522 |
| 50 | substrate | `phraisona` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `etruscan` (label: Etruscan). Substrate pool: `eteocretan` (20 top surfaces). Control pool: `control_eteocretan_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

