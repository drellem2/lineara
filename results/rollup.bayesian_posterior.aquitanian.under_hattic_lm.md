# v23 cross-LM gate — aquitanian substrate under Hattic LM (mg-b599) — Hattic cross-LM cell (mg-7b882)

**Headline: the aquitanian substrate pool FAILs the v10 right-tail bayesian gate against control_aquitanian when both sides are scored under the Hattic LM at p=1.546e-01** (median substrate posterior 0.9619 vs median control posterior 0.9500; gap +0.0119). The substrate-vs-control posterior median ordering does not clear the gate under this LM.

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| aquitanian | control_aquitanian | Hattic | 20 | 20 | 0.9619 | 0.9500 | 238.0 | 1.546e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9577. Mean of top-20 control posterior_mean: 0.9511. Gap (median, gate-relevant): +0.0119; gap (mean): +0.0067. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `nahi` | 51 | 51 | 0.9811 | `ilae` | 187 | 187 | 0.9947 |
| 2 | `aita` | 50 | 50 | 0.9808 | `itx` | 90 | 90 | 0.9891 |
| 3 | `ezti` | 50 | 50 | 0.9808 | `anao` | 62 | 62 | 0.9844 |
| 4 | `hara` | 50 | 50 | 0.9808 | `in` | 100 | 99 | 0.9804 |
| 5 | `haran` | 50 | 50 | 0.9808 | `aatzasl` | 71 | 70 | 0.9726 |
| 6 | `hesi` | 50 | 50 | 0.9808 | `aai` | 26 | 26 | 0.9643 |
| 7 | `itsaso` | 50 | 50 | 0.9808 | `iiemn` | 157 | 152 | 0.9623 |
| 8 | `aitz` | 53 | 52 | 0.9636 | `tztzan` | 23 | 23 | 0.9600 |
| 9 | `argi` | 52 | 51 | 0.9630 | `aninze` | 44 | 43 | 0.9565 |
| 10 | `ate` | 51 | 50 | 0.9623 | `enaa` | 18 | 18 | 0.9500 |
| 11 | `hauten` | 24 | 24 | 0.9615 | `ntsilai` | 38 | 37 | 0.9500 |
| 12 | `hori` | 50 | 49 | 0.9615 | `anii` | 17 | 17 | 0.9474 |
| 13 | `zaldi` | 50 | 49 | 0.9615 | `hah` | 192 | 181 | 0.9381 |
| 14 | `ile` | 60 | 58 | 0.9516 | `ueih` | 13 | 13 | 0.9333 |
| 15 | `atta` | 78 | 75 | 0.9500 | `iihe` | 55 | 52 | 0.9298 |
| 16 | `handi` | 50 | 48 | 0.9423 | `arzaeai` | 26 | 25 | 0.9286 |
| 17 | `ahuntz` | 58 | 55 | 0.9333 | `lalt` | 11 | 11 | 0.9231 |
| 18 | `zelai` | 50 | 47 | 0.9231 | `txiah` | 50 | 47 | 0.9231 |
| 19 | `hartu` | 54 | 50 | 0.9107 | `aoel` | 10 | 10 | 0.9167 |
| 20 | `begi` | 50 | 46 | 0.9038 | `llatz` | 10 | 10 | 0.9167 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `ilae` | 187 | 187 | 0.9947 | 1.000 | 0.9947 |
| 2 | control | `itx` | 90 | 90 | 0.9891 | 1.000 | 0.9891 |
| 3 | control | `anao` | 62 | 62 | 0.9844 | 1.000 | 0.9844 |
| 4 | substrate | `nahi` | 51 | 51 | 0.9811 | 1.000 | 0.9811 |
| 5 | substrate | `aita` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `ezti` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `hara` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `haran` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `hesi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `itsaso` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | control | `in` | 100 | 99 | 0.9804 | 1.000 | 0.9804 |
| 12 | control | `aatzasl` | 71 | 70 | 0.9726 | 1.000 | 0.9726 |
| 13 | control | `aai` | 26 | 26 | 0.9643 | 1.000 | 0.9643 |
| 14 | substrate | `aitz` | 53 | 52 | 0.9636 | 1.000 | 0.9636 |
| 15 | substrate | `argi` | 52 | 51 | 0.9630 | 1.000 | 0.9630 |
| 16 | substrate | `ate` | 51 | 50 | 0.9623 | 1.000 | 0.9623 |
| 17 | control | `iiemn` | 157 | 152 | 0.9623 | 1.000 | 0.9623 |
| 18 | substrate | `hauten` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 19 | substrate | `hori` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 20 | substrate | `zaldi` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 21 | control | `tztzan` | 23 | 23 | 0.9600 | 1.000 | 0.9600 |
| 22 | control | `aninze` | 44 | 43 | 0.9565 | 1.000 | 0.9565 |
| 23 | substrate | `ile` | 60 | 58 | 0.9516 | 1.000 | 0.9516 |
| 24 | substrate | `atta` | 78 | 75 | 0.9500 | 1.000 | 0.9500 |
| 25 | control | `enaa` | 18 | 18 | 0.9500 | 1.000 | 0.9500 |
| 26 | control | `ntsilai` | 38 | 37 | 0.9500 | 1.000 | 0.9500 |
| 27 | control | `anii` | 17 | 17 | 0.9474 | 1.000 | 0.9474 |
| 28 | substrate | `handi` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 29 | control | `hah` | 192 | 181 | 0.9381 | 1.000 | 0.9381 |
| 30 | substrate | `ahuntz` | 58 | 55 | 0.9333 | 1.000 | 0.9333 |
| 31 | control | `ueih` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 32 | control | `iihe` | 55 | 52 | 0.9298 | 1.000 | 0.9298 |
| 33 | control | `arzaeai` | 26 | 25 | 0.9286 | 1.000 | 0.9286 |
| 34 | substrate | `zelai` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 35 | control | `lalt` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 36 | control | `txiah` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 37 | control | `aoel` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 38 | control | `llatz` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 39 | substrate | `hartu` | 54 | 50 | 0.9107 | 1.000 | 0.9107 |
| 40 | substrate | `begi` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 41 | substrate | `hartz` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 42 | control | `aahzl` | 49 | 45 | 0.9020 | 1.000 | 0.9020 |
| 43 | control | `ehaahee` | 25 | 23 | 0.8889 | 1.000 | 0.8889 |
| 44 | control | `uoh` | 70 | 63 | 0.8889 | 1.000 | 0.8889 |
| 45 | control | `onia` | 57 | 51 | 0.8814 | 1.000 | 0.8814 |
| 46 | control | `lna` | 85 | 75 | 0.8736 | 1.000 | 0.8736 |
| 47 | substrate | `sori` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 48 | control | `zaa` | 86 | 75 | 0.8636 | 1.000 | 0.8636 |
| 49 | substrate | `hezur` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 50 | substrate | `katu` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `aquitanian` (20 top surfaces). Control pool: `control_aquitanian` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

