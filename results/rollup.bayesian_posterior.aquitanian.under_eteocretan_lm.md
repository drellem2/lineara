# v23 cross-LM gate — aquitanian substrate under Eteocretan LM (mg-b599) — under Eteocretan LM (reverse cross-LM check)

**Headline: the aquitanian substrate pool PASSes the v10 right-tail bayesian gate against control_aquitanian when both sides are scored under the Eteocretan LM at p=1.791e-03** (median substrate posterior 0.9808 vs median control posterior 0.9401; gap +0.0407).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| aquitanian | control_aquitanian | Eteocretan | 20 | 20 | 0.9808 | 0.9401 | 307.0 | 1.791e-03 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9700. Mean of top-20 control posterior_mean: 0.9403. Gap (median, gate-relevant): +0.0407; gap (mean): +0.0296. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `idiar` | 54 | 54 | 0.9821 | `eass` | 69 | 69 | 0.9859 |
| 2 | `nahi` | 51 | 51 | 0.9811 | `anao` | 62 | 62 | 0.9844 |
| 3 | `behi` | 50 | 50 | 0.9808 | `onia` | 57 | 57 | 0.9831 |
| 4 | `bide` | 50 | 50 | 0.9808 | `in` | 100 | 99 | 0.9804 |
| 5 | `eki` | 50 | 50 | 0.9808 | `ntsilai` | 38 | 38 | 0.9750 |
| 6 | `erori` | 50 | 50 | 0.9808 | `ia` | 19 | 19 | 0.9524 |
| 7 | `esne` | 50 | 50 | 0.9808 | `aaer` | 17 | 17 | 0.9474 |
| 8 | `gari` | 50 | 50 | 0.9808 | `anii` | 17 | 17 | 0.9474 |
| 9 | `hesi` | 50 | 50 | 0.9808 | `itx` | 90 | 86 | 0.9457 |
| 10 | `itsaso` | 50 | 50 | 0.9808 | `aarig` | 166 | 157 | 0.9405 |
| 11 | `oin` | 50 | 50 | 0.9808 | `raiia` | 81 | 77 | 0.9398 |
| 12 | `ona` | 50 | 50 | 0.9808 | `iiemn` | 157 | 148 | 0.9371 |
| 13 | `zortzi` | 50 | 50 | 0.9808 | `arzaeai` | 26 | 25 | 0.9286 |
| 14 | `sei` | 65 | 64 | 0.9701 | `itre` | 110 | 103 | 0.9286 |
| 15 | `ezti` | 50 | 49 | 0.9615 | `riieen` | 53 | 50 | 0.9273 |
| 16 | `etxe` | 54 | 52 | 0.9464 | `ionm` | 9 | 9 | 0.9091 |
| 17 | `bihotz` | 50 | 48 | 0.9423 | `urie` | 156 | 142 | 0.9051 |
| 18 | `bizi` | 50 | 48 | 0.9423 | `auhis` | 8 | 8 | 0.9000 |
| 19 | `ere` | 50 | 48 | 0.9423 | `enaa` | 18 | 17 | 0.9000 |
| 20 | `non` | 50 | 48 | 0.9423 | `hina` | 88 | 79 | 0.8889 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `eass` | 69 | 69 | 0.9859 | 1.000 | 0.9859 |
| 2 | control | `anao` | 62 | 62 | 0.9844 | 1.000 | 0.9844 |
| 3 | control | `onia` | 57 | 57 | 0.9831 | 1.000 | 0.9831 |
| 4 | substrate | `idiar` | 54 | 54 | 0.9821 | 1.000 | 0.9821 |
| 5 | substrate | `nahi` | 51 | 51 | 0.9811 | 1.000 | 0.9811 |
| 6 | substrate | `behi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `bide` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `eki` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `erori` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `esne` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `gari` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `hesi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `itsaso` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 14 | substrate | `oin` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 15 | substrate | `ona` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 16 | substrate | `zortzi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 17 | control | `in` | 100 | 99 | 0.9804 | 1.000 | 0.9804 |
| 18 | control | `ntsilai` | 38 | 38 | 0.9750 | 1.000 | 0.9750 |
| 19 | substrate | `sei` | 65 | 64 | 0.9701 | 1.000 | 0.9701 |
| 20 | substrate | `ezti` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 21 | control | `ia` | 19 | 19 | 0.9524 | 1.000 | 0.9524 |
| 22 | control | `aaer` | 17 | 17 | 0.9474 | 1.000 | 0.9474 |
| 23 | control | `anii` | 17 | 17 | 0.9474 | 1.000 | 0.9474 |
| 24 | substrate | `etxe` | 54 | 52 | 0.9464 | 1.000 | 0.9464 |
| 25 | control | `itx` | 90 | 86 | 0.9457 | 1.000 | 0.9457 |
| 26 | substrate | `bihotz` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 27 | substrate | `bizi` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 28 | substrate | `ere` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 29 | substrate | `non` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 30 | control | `aarig` | 166 | 157 | 0.9405 | 1.000 | 0.9405 |
| 31 | control | `raiia` | 81 | 77 | 0.9398 | 1.000 | 0.9398 |
| 32 | control | `iiemn` | 157 | 148 | 0.9371 | 1.000 | 0.9371 |
| 33 | control | `arzaeai` | 26 | 25 | 0.9286 | 1.000 | 0.9286 |
| 34 | control | `itre` | 110 | 103 | 0.9286 | 1.000 | 0.9286 |
| 35 | control | `riieen` | 53 | 50 | 0.9273 | 1.000 | 0.9273 |
| 36 | substrate | `mahats` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 37 | substrate | `txiki` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 38 | control | `urie` | 156 | 142 | 0.9051 | 1.000 | 0.9051 |
| 39 | substrate | `egun` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 40 | substrate | `gaitz` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 41 | substrate | `hau` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 42 | control | `enaa` | 18 | 17 | 0.9000 | 1.000 | 0.9000 |
| 43 | substrate | `iri` | 92 | 83 | 0.8936 | 1.000 | 0.8936 |
| 44 | substrate | `aitz` | 53 | 48 | 0.8909 | 1.000 | 0.8909 |
| 45 | substrate | `seni` | 367 | 327 | 0.8889 | 1.000 | 0.8889 |
| 46 | control | `hina` | 88 | 79 | 0.8889 | 1.000 | 0.8889 |
| 47 | control | `iaem` | 16 | 15 | 0.8889 | 1.000 | 0.8889 |
| 48 | control | `an` | 1620 | 1429 | 0.8816 | 1.000 | 0.8816 |
| 49 | control | `ionm` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 50 | substrate | `gatz` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (label: Eteocretan). Substrate pool: `aquitanian` (20 top surfaces). Control pool: `control_aquitanian` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

