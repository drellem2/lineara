# v23 cross-LM gate — aquitanian substrate under Hattic LM (mg-b599) — Hattic cross-LM cell, v2 edition-sourced pool/LM (mg-a38bf)

**Headline: the aquitanian substrate pool PASSes the v10 right-tail bayesian gate against control_aquitanian when both sides are scored under the Hattic LM at p=3.770e-02** (median substrate posterior 0.9624 vs median control posterior 0.9500; gap +0.0124).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| aquitanian | control_aquitanian | Hattic | 20 | 20 | 0.9624 | 0.9500 | 266.0 | 3.770e-02 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9643. Mean of top-20 control posterior_mean: 0.9493. Gap (median, gate-relevant): +0.0124; gap (mean): +0.0150. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `hartu` | 54 | 54 | 0.9821 | `iiemn` | 157 | 157 | 0.9937 |
| 2 | `nahi` | 51 | 51 | 0.9811 | `aatzasl` | 71 | 71 | 0.9863 |
| 3 | `aita` | 50 | 50 | 0.9808 | `anao` | 62 | 62 | 0.9844 |
| 4 | `ezti` | 50 | 50 | 0.9808 | `tit` | 47 | 47 | 0.9796 |
| 5 | `hara` | 50 | 50 | 0.9808 | `ilae` | 187 | 184 | 0.9788 |
| 6 | `haran` | 50 | 50 | 0.9808 | `aninze` | 44 | 44 | 0.9783 |
| 7 | `hesi` | 50 | 50 | 0.9808 | `luaha` | 55 | 54 | 0.9649 |
| 8 | `itsaso` | 50 | 50 | 0.9808 | `txiah` | 50 | 49 | 0.9615 |
| 9 | `argi` | 52 | 51 | 0.9630 | `nhhul` | 19 | 19 | 0.9524 |
| 10 | `atta` | 78 | 76 | 0.9625 | `enaa` | 18 | 18 | 0.9500 |
| 11 | `ate` | 51 | 50 | 0.9623 | `ntsilai` | 38 | 37 | 0.9500 |
| 12 | `hamar` | 50 | 49 | 0.9615 | `onia` | 57 | 55 | 0.9492 |
| 13 | `handi` | 50 | 49 | 0.9615 | `aeusi` | 192 | 181 | 0.9381 |
| 14 | `hauten` | 24 | 24 | 0.9615 | `ueih` | 13 | 13 | 0.9333 |
| 15 | `hori` | 50 | 49 | 0.9615 | `lalt` | 11 | 11 | 0.9231 |
| 16 | `sori` | 50 | 49 | 0.9615 | `ikez` | 10 | 10 | 0.9167 |
| 17 | `hau` | 50 | 48 | 0.9423 | `llatz` | 10 | 10 | 0.9167 |
| 18 | `hil` | 50 | 48 | 0.9423 | `eass` | 69 | 64 | 0.9155 |
| 19 | `ile` | 60 | 57 | 0.9355 | `iihe` | 55 | 51 | 0.9123 |
| 20 | `esne` | 50 | 47 | 0.9231 | `aahzl` | 49 | 45 | 0.9020 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `iiemn` | 157 | 157 | 0.9937 | 1.000 | 0.9937 |
| 2 | control | `aatzasl` | 71 | 71 | 0.9863 | 1.000 | 0.9863 |
| 3 | control | `anao` | 62 | 62 | 0.9844 | 1.000 | 0.9844 |
| 4 | substrate | `hartu` | 54 | 54 | 0.9821 | 1.000 | 0.9821 |
| 5 | substrate | `nahi` | 51 | 51 | 0.9811 | 1.000 | 0.9811 |
| 6 | substrate | `aita` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `ezti` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `hara` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `haran` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `hesi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `itsaso` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | control | `tit` | 47 | 47 | 0.9796 | 1.000 | 0.9796 |
| 13 | control | `ilae` | 187 | 184 | 0.9788 | 1.000 | 0.9788 |
| 14 | control | `aninze` | 44 | 44 | 0.9783 | 1.000 | 0.9783 |
| 15 | control | `luaha` | 55 | 54 | 0.9649 | 1.000 | 0.9649 |
| 16 | substrate | `argi` | 52 | 51 | 0.9630 | 1.000 | 0.9630 |
| 17 | substrate | `atta` | 78 | 76 | 0.9625 | 1.000 | 0.9625 |
| 18 | substrate | `ate` | 51 | 50 | 0.9623 | 1.000 | 0.9623 |
| 19 | substrate | `hamar` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 20 | substrate | `handi` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 21 | substrate | `hauten` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 22 | substrate | `hori` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 23 | substrate | `sori` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 24 | control | `txiah` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 25 | control | `nhhul` | 19 | 19 | 0.9524 | 1.000 | 0.9524 |
| 26 | control | `enaa` | 18 | 18 | 0.9500 | 1.000 | 0.9500 |
| 27 | control | `ntsilai` | 38 | 37 | 0.9500 | 1.000 | 0.9500 |
| 28 | control | `onia` | 57 | 55 | 0.9492 | 1.000 | 0.9492 |
| 29 | substrate | `hau` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 30 | substrate | `hil` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 31 | control | `aeusi` | 192 | 181 | 0.9381 | 1.000 | 0.9381 |
| 32 | substrate | `ile` | 60 | 57 | 0.9355 | 1.000 | 0.9355 |
| 33 | control | `ueih` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 34 | substrate | `esne` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 35 | substrate | `hezur` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 36 | control | `lalt` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 37 | control | `ikez` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 38 | control | `llatz` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 39 | control | `eass` | 69 | 64 | 0.9155 | 1.000 | 0.9155 |
| 40 | control | `iihe` | 55 | 51 | 0.9123 | 1.000 | 0.9123 |
| 41 | substrate | `lau` | 63 | 58 | 0.9077 | 1.000 | 0.9077 |
| 42 | substrate | `hanna` | 51 | 47 | 0.9057 | 1.000 | 0.9057 |
| 43 | substrate | `zaldi` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 44 | control | `aahzl` | 49 | 45 | 0.9020 | 1.000 | 0.9020 |
| 45 | substrate | `lur` | 1200 | 1082 | 0.9010 | 1.000 | 0.9010 |
| 46 | control | `ueinn` | 18 | 17 | 0.9000 | 1.000 | 0.9000 |
| 47 | control | `anii` | 17 | 16 | 0.8947 | 1.000 | 0.8947 |
| 48 | control | `aai` | 26 | 24 | 0.8929 | 1.000 | 0.8929 |
| 49 | control | `ehi` | 158 | 140 | 0.8812 | 1.000 | 0.8812 |
| 50 | control | `bile` | 265 | 233 | 0.8764 | 1.000 | 0.8764 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (label: Hattic). Substrate pool: `aquitanian` (20 top surfaces). Control pool: `control_aquitanian` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

