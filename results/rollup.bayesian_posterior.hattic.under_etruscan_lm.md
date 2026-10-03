# v23 cross-LM gate — hattic substrate under Etruscan LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the hattic substrate pool FAILs the v10 right-tail bayesian gate against control_hattic_bigram when both sides are scored under the Etruscan LM at p=9.993e-01** (median substrate posterior 0.8000 vs median control posterior 0.9000; gap -0.1000). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| hattic | control_hattic_bigram | Etruscan | 20 | 20 | 0.8000 | 0.9000 | 82.0 | 9.993e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8205. Mean of top-20 control posterior_mean: 0.8963. Gap (median, gate-relevant): -0.1000; gap (mean): -0.0758. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `zari` | 50 | 50 | 0.9808 | `taha` | 67 | 67 | 0.9855 |
| 2 | `kammama` | 13 | 13 | 0.9333 | `esttal` | 28 | 28 | 0.9667 |
| 3 | `mezulla` | 13 | 13 | 0.9333 | `zap` | 24 | 24 | 0.9615 |
| 4 | `hapantali` | 6 | 6 | 0.8750 | `zinte` | 63 | 61 | 0.9538 |
| 5 | `hasammili` | 6 | 6 | 0.8750 | `haka` | 19 | 19 | 0.9524 |
| 6 | `halentu` | 13 | 12 | 0.8667 | `kamana` | 102 | 96 | 0.9327 |
| 7 | `lihzina` | 13 | 12 | 0.8667 | `lina` | 80 | 75 | 0.9268 |
| 8 | `istarazzil` | 5 | 5 | 0.8571 | `elist` | 32 | 30 | 0.9118 |
| 9 | `an` | 50 | 42 | 0.8269 | `pamz` | 9 | 9 | 0.9091 |
| 10 | `kastama` | 13 | 11 | 0.8000 | `wuina` | 8 | 8 | 0.9000 |
| 11 | `tuhtasul` | 8 | 7 | 0.8000 | `zuintas` | 8 | 8 | 0.9000 |
| 12 | `alep` | 50 | 40 | 0.7885 | `kalesten` | 7 | 7 | 0.8889 |
| 13 | `ashap` | 50 | 39 | 0.7692 | `linam` | 67 | 60 | 0.8841 |
| 14 | `estan` | 50 | 39 | 0.7692 | `katunami` | 15 | 14 | 0.8824 |
| 15 | `il` | 50 | 39 | 0.7692 | `narunete` | 6 | 6 | 0.8750 |
| 16 | `hanwasuit` | 6 | 5 | 0.7500 | `hasez` | 27 | 24 | 0.8621 |
| 17 | `sul` | 50 | 38 | 0.7500 | `tantusurili` | 4 | 4 | 0.8333 |
| 18 | `hanhana` | 13 | 10 | 0.7333 | `estt` | 27 | 23 | 0.8276 |
| 19 | `hilamar` | 13 | 10 | 0.7333 | `hal` | 59 | 47 | 0.7869 |
| 20 | `leipinu` | 13 | 10 | 0.7333 | `zapasusha` | 12 | 10 | 0.7857 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `taha` | 67 | 67 | 0.9855 | 1.000 | 0.9855 |
| 2 | substrate | `zari` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | control | `esttal` | 28 | 28 | 0.9667 | 1.000 | 0.9667 |
| 4 | control | `zap` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 5 | control | `zinte` | 63 | 61 | 0.9538 | 1.000 | 0.9538 |
| 6 | control | `haka` | 19 | 19 | 0.9524 | 1.000 | 0.9524 |
| 7 | substrate | `kammama` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 8 | substrate | `mezulla` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 9 | control | `kamana` | 102 | 96 | 0.9327 | 1.000 | 0.9327 |
| 10 | control | `lina` | 80 | 75 | 0.9268 | 1.000 | 0.9268 |
| 11 | control | `elist` | 32 | 30 | 0.9118 | 1.000 | 0.9118 |
| 12 | control | `linam` | 67 | 60 | 0.8841 | 1.000 | 0.8841 |
| 13 | control | `katunami` | 15 | 14 | 0.8824 | 1.000 | 0.8824 |
| 14 | control | `pamz` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 15 | substrate | `halentu` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 16 | substrate | `lihzina` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 17 | control | `hasez` | 27 | 24 | 0.8621 | 1.000 | 0.8621 |
| 18 | control | `estt` | 27 | 23 | 0.8276 | 1.000 | 0.8276 |
| 19 | substrate | `an` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 20 | control | `wuina` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 21 | control | `zuintas` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 22 | substrate | `kastama` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 23 | substrate | `alep` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 24 | control | `hal` | 59 | 47 | 0.7869 | 1.000 | 0.7869 |
| 25 | control | `zapasusha` | 12 | 10 | 0.7857 | 1.000 | 0.7857 |
| 26 | control | `kalesten` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 27 | substrate | `ashap` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 28 | substrate | `estan` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 29 | substrate | `il` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 30 | substrate | `sul` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 31 | control | `kinanaat` | 10 | 8 | 0.7500 | 1.000 | 0.7500 |
| 32 | control | `letenurul` | 10 | 8 | 0.7500 | 1.000 | 0.7500 |
| 33 | substrate | `tuhtasul` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 34 | substrate | `hanhana` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 35 | substrate | `hilamar` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 36 | substrate | `leipinu` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 37 | substrate | `tahurpa` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 38 | substrate | `lezuh` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 39 | substrate | `hapantali` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 40 | substrate | `hasammili` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 41 | control | `narunete` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 42 | substrate | `arinna` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 43 | substrate | `istarazzil` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 44 | control | `zasun` | 68 | 46 | 0.6714 | 1.000 | 0.6714 |
| 45 | control | `hkast` | 36 | 24 | 0.6579 | 1.000 | 0.6579 |
| 46 | substrate | `hanwasuit` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 47 | control | `tantusurili` | 4 | 4 | 0.8333 | 0.400 | 0.6333 |
| 48 | control | `tapas` | 139 | 88 | 0.6312 | 1.000 | 0.6312 |
| 49 | control | `kapanas` | 64 | 40 | 0.6212 | 1.000 | 0.6212 |
| 50 | substrate | `sulinkatte` | 5 | 4 | 0.7143 | 0.500 | 0.6071 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `etruscan` (label: Etruscan). Substrate pool: `hattic` (20 top surfaces). Control pool: `control_hattic_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

