# v23 cross-LM gate — eteocretan substrate under Hattic LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the eteocretan substrate pool FAILs the v10 right-tail bayesian gate against control_eteocretan_bigram when both sides are scored under the Hattic LM at p=9.653e-01** (median substrate posterior 0.8875 vs median control posterior 0.9583; gap -0.0708). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | Hattic | 20 | 20 | 0.8875 | 0.9583 | 133.5 | 9.653e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8905. Mean of top-20 control posterior_mean: 0.9338. Gap (median, gate-relevant): -0.0708; gap (mean): -0.0432. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `iarei` | 50 | 50 | 0.9808 | `phai` | 110 | 110 | 0.9911 |
| 2 | `inai` | 50 | 50 | 0.9808 | `ka` | 100 | 100 | 0.9902 |
| 3 | `rima` | 50 | 50 | 0.9808 | `sal` | 50 | 50 | 0.9808 |
| 4 | `wai` | 50 | 50 | 0.9808 | `disa` | 49 | 49 | 0.9804 |
| 5 | `wantai` | 24 | 24 | 0.9615 | `ieti` | 163 | 160 | 0.9758 |
| 6 | `arka` | 50 | 48 | 0.9423 | `ial` | 34 | 34 | 0.9722 |
| 7 | `isala` | 50 | 48 | 0.9423 | `ana` | 33 | 33 | 0.9714 |
| 8 | `iareion` | 13 | 13 | 0.9333 | `nadina` | 24 | 24 | 0.9615 |
| 9 | `ieroi` | 50 | 46 | 0.9038 | `dnta` | 23 | 23 | 0.9600 |
| 10 | `zethante` | 8 | 8 | 0.9000 | `etaltat` | 48 | 47 | 0.9600 |
| 11 | `natoniate` | 6 | 6 | 0.8750 | `owaiais` | 21 | 21 | 0.9565 |
| 12 | `parsiphai` | 6 | 6 | 0.8750 | `iphai` | 15 | 15 | 0.9412 |
| 13 | `epimere` | 13 | 12 | 0.8667 | `mari` | 74 | 69 | 0.9211 |
| 14 | `inaiperima` | 5 | 5 | 0.8571 | `ke` | 100 | 90 | 0.8922 |
| 15 | `kanet` | 50 | 43 | 0.8462 | `alan` | 7 | 7 | 0.8889 |
| 16 | `siatas` | 24 | 21 | 0.8462 | `iaiete` | 42 | 38 | 0.8864 |
| 17 | `arkadioi` | 8 | 7 | 0.8000 | `ipisa` | 6 | 6 | 0.8750 |
| 18 | `kilenti` | 13 | 11 | 0.8000 | `isar` | 6 | 6 | 0.8750 |
| 19 | `niate` | 50 | 40 | 0.7885 | `ete` | 131 | 112 | 0.8496 |
| 20 | `arkaginoi` | 6 | 5 | 0.7500 | `waieth` | 11 | 10 | 0.8462 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `phai` | 110 | 110 | 0.9911 | 1.000 | 0.9911 |
| 2 | control | `ka` | 100 | 100 | 0.9902 | 1.000 | 0.9902 |
| 3 | substrate | `iarei` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `inai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `rima` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | control | `sal` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | control | `disa` | 49 | 49 | 0.9804 | 1.000 | 0.9804 |
| 9 | control | `ieti` | 163 | 160 | 0.9758 | 1.000 | 0.9758 |
| 10 | control | `ial` | 34 | 34 | 0.9722 | 1.000 | 0.9722 |
| 11 | control | `ana` | 33 | 33 | 0.9714 | 1.000 | 0.9714 |
| 12 | substrate | `wantai` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 13 | control | `nadina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 14 | control | `dnta` | 23 | 23 | 0.9600 | 1.000 | 0.9600 |
| 15 | control | `etaltat` | 48 | 47 | 0.9600 | 1.000 | 0.9600 |
| 16 | control | `owaiais` | 21 | 21 | 0.9565 | 1.000 | 0.9565 |
| 17 | substrate | `arka` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 18 | substrate | `isala` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 19 | control | `iphai` | 15 | 15 | 0.9412 | 1.000 | 0.9412 |
| 20 | substrate | `iareion` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 21 | control | `mari` | 74 | 69 | 0.9211 | 1.000 | 0.9211 |
| 22 | substrate | `ieroi` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 23 | control | `ke` | 100 | 90 | 0.8922 | 1.000 | 0.8922 |
| 24 | control | `iaiete` | 42 | 38 | 0.8864 | 1.000 | 0.8864 |
| 25 | substrate | `epimere` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 26 | control | `ete` | 131 | 112 | 0.8496 | 1.000 | 0.8496 |
| 27 | substrate | `kanet` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 28 | substrate | `siatas` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 29 | control | `waieth` | 11 | 10 | 0.8462 | 1.000 | 0.8462 |
| 30 | control | `tem` | 56 | 48 | 0.8448 | 1.000 | 0.8448 |
| 31 | control | `ima` | 44 | 37 | 0.8261 | 1.000 | 0.8261 |
| 32 | substrate | `zethante` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 33 | substrate | `kilenti` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 34 | substrate | `niate` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 35 | control | `alan` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 36 | substrate | `arkadioi` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 37 | control | `phanw` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 38 | control | `tow` | 73 | 54 | 0.7333 | 1.000 | 0.7333 |
| 39 | substrate | `inaipe` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 40 | substrate | `omosai` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 41 | substrate | `natoniate` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 42 | substrate | `parsiphai` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 43 | control | `ipisa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 44 | control | `isar` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 45 | substrate | `epioi` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 46 | substrate | `inaiperima` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 47 | substrate | `komnai` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 48 | control | `etabz` | 18 | 12 | 0.6500 | 1.000 | 0.6500 |
| 49 | substrate | `arkaginoi` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 50 | control | `ianteiarkal` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `eteocretan` (20 top surfaces). Control pool: `control_eteocretan_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

