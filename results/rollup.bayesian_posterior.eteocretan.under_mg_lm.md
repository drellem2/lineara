# v23 cross-LM gate — eteocretan substrate under Mycenaean Greek LM (mg-b599) — under Mycenaean Greek LM (cross-LM negative control)

**Headline: the eteocretan substrate pool PASSes the v10 right-tail bayesian gate against control_eteocretan_bigram when both sides are scored under the Mycenaean Greek LM at p=1.725e-05** (median substrate posterior 0.9423 vs median control posterior 0.8382; gap +0.1042).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | Mycenaean Greek | 20 | 20 | 0.9423 | 0.8382 | 353.0 | 1.725e-05 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9433. Mean of top-20 control posterior_mean: 0.8256. Gap (median, gate-relevant): +0.1042; gap (mean): +0.1177. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `arka` | 50 | 50 | 0.9808 | `nadina` | 24 | 24 | 0.9615 |
| 2 | `dowa` | 50 | 50 | 0.9808 | `iaiete` | 42 | 41 | 0.9545 |
| 3 | `epioi` | 50 | 50 | 0.9808 | `ana` | 33 | 32 | 0.9429 |
| 4 | `oma` | 50 | 50 | 0.9808 | `owaiais` | 21 | 20 | 0.9130 |
| 5 | `rima` | 50 | 50 | 0.9808 | `ete` | 131 | 117 | 0.8872 |
| 6 | `sam` | 50 | 50 | 0.9808 | `tow` | 73 | 65 | 0.8800 |
| 7 | `wai` | 50 | 50 | 0.9808 | `okadkaiom` | 14 | 13 | 0.8750 |
| 8 | `ieroi` | 50 | 49 | 0.9615 | `ka` | 100 | 88 | 0.8725 |
| 9 | `nato` | 50 | 48 | 0.9423 | `onaipetosa` | 5 | 5 | 0.8571 |
| 10 | `omai` | 50 | 48 | 0.9423 | `owala` | 119 | 101 | 0.8430 |
| 11 | `omal` | 50 | 48 | 0.9423 | `iaruorta` | 4 | 4 | 0.8333 |
| 12 | `onai` | 50 | 48 | 0.9423 | `ke` | 100 | 82 | 0.8137 |
| 13 | `porta` | 50 | 48 | 0.9423 | `intokame` | 8 | 7 | 0.8000 |
| 14 | `iareion` | 13 | 13 | 0.9333 | `rar` | 92 | 74 | 0.7979 |
| 15 | `etion` | 50 | 47 | 0.9231 | `tem` | 56 | 45 | 0.7931 |
| 16 | `mere` | 50 | 47 | 0.9231 | `inipina` | 2 | 2 | 0.7500 |
| 17 | `dowai` | 50 | 46 | 0.9038 | `imaima` | 17 | 13 | 0.7368 |
| 18 | `ieme` | 50 | 46 | 0.9038 | `alatetdos` | 1 | 1 | 0.6667 |
| 19 | `natoniate` | 6 | 6 | 0.8750 | `ddiomadou` | 1 | 1 | 0.6667 |
| 20 | `mete` | 50 | 44 | 0.8654 | `konamemer` | 1 | 1 | 0.6667 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `arka` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `dowa` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `epioi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `oma` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `rima` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `sam` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `ieroi` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 9 | control | `nadina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 10 | control | `iaiete` | 42 | 41 | 0.9545 | 1.000 | 0.9545 |
| 11 | control | `ana` | 33 | 32 | 0.9429 | 1.000 | 0.9429 |
| 12 | substrate | `nato` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 13 | substrate | `omai` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 14 | substrate | `omal` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 15 | substrate | `onai` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 16 | substrate | `porta` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 17 | substrate | `iareion` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 18 | substrate | `etion` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 19 | substrate | `mere` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 20 | control | `owaiais` | 21 | 20 | 0.9130 | 1.000 | 0.9130 |
| 21 | substrate | `dowai` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 22 | substrate | `ieme` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 23 | control | `ete` | 131 | 117 | 0.8872 | 1.000 | 0.8872 |
| 24 | control | `tow` | 73 | 65 | 0.8800 | 1.000 | 0.8800 |
| 25 | control | `okadkaiom` | 14 | 13 | 0.8750 | 1.000 | 0.8750 |
| 26 | control | `ka` | 100 | 88 | 0.8725 | 1.000 | 0.8725 |
| 27 | substrate | `mete` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 28 | substrate | `omos` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 29 | substrate | `onoi` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 30 | control | `owala` | 119 | 101 | 0.8430 | 1.000 | 0.8430 |
| 31 | control | `ke` | 100 | 82 | 0.8137 | 1.000 | 0.8137 |
| 32 | substrate | `eko` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 33 | substrate | `enete` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 34 | substrate | `siatas` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 35 | control | `rar` | 92 | 74 | 0.7979 | 1.000 | 0.7979 |
| 36 | control | `tem` | 56 | 45 | 0.7931 | 1.000 | 0.7931 |
| 37 | substrate | `iarei` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 38 | substrate | `arkadioi` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 39 | control | `intokame` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 40 | control | `imaima` | 17 | 13 | 0.7368 | 1.000 | 0.7368 |
| 41 | substrate | `arkadi` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 42 | substrate | `omosai` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 43 | substrate | `natoniate` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 44 | control | `onaipetosa` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 45 | substrate | `iar` | 50 | 34 | 0.6731 | 1.000 | 0.6731 |
| 46 | substrate | `netamoi` | 13 | 9 | 0.6667 | 1.000 | 0.6667 |
| 47 | control | `etaltat` | 48 | 32 | 0.6600 | 1.000 | 0.6600 |
| 48 | substrate | `sameti` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 49 | substrate | `wantai` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 50 | substrate | `ier` | 50 | 32 | 0.6346 | 1.000 | 0.6346 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `mycenaean_greek` (label: Mycenaean Greek). Substrate pool: `eteocretan` (20 top surfaces). Control pool: `control_eteocretan_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

