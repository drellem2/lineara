# chic-v3 — pool=aquitanian right-tail bayesian gate on CHIC (mg-9700)

**Headline: the aquitanian substrate pool FAILs the v10 right-tail bayesian gate against control_aquitanian on the CHIC syllabographic corpus at p=9.369e-01** (median substrate posterior 0.8739 vs median control posterior 0.9106). Cross-script transfer of the Linear A aquitanian signal to CHIC is not detected at the gate threshold; CHIC's smaller corpus reduces the framework's discriminating power and a borderline p-value should be read with that caveat in mind.

## Acceptance gate

| substrate pool | control pool | LM | n paired windows | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| aquitanian | control_aquitanian | basque | 5746 | 20 | 20 | 0.8739 | 0.9106 | 144.0 | 9.369e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8720. Mean of top-20 control posterior_mean: 0.8981. Gap: -0.0260. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side (gate input)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `entzun` | 20 | 20 | 0.9545 | `an` | 70 | 70 | 0.9861 |
| 2 | `aitz` | 50 | 48 | 0.9423 | `enaa` | 60 | 60 | 0.9839 |
| 3 | `izotz` | 49 | 46 | 0.9216 | `eal` | 32 | 32 | 0.9706 |
| 4 | `ahuntz` | 20 | 19 | 0.9091 | `anai` | 60 | 59 | 0.9677 |
| 5 | `etxe` | 50 | 46 | 0.9038 | `onia` | 120 | 114 | 0.9426 |
| 6 | `gatz` | 50 | 46 | 0.9038 | `anao` | 60 | 57 | 0.9355 |
| 7 | `ona` | 50 | 46 | 0.9038 | `aatzasl` | 12 | 12 | 0.9286 |
| 8 | `non` | 50 | 45 | 0.8846 | `riieen` | 12 | 12 | 0.9286 |
| 9 | `oin` | 50 | 45 | 0.8846 | `zaa` | 96 | 89 | 0.9184 |
| 10 | `anai` | 49 | 44 | 0.8824 | `txiah` | 120 | 111 | 0.9180 |
| 11 | `ama` | 50 | 44 | 0.8654 | `aiab` | 60 | 55 | 0.9032 |
| 12 | `eta` | 50 | 44 | 0.8654 | `ehaahee` | 8 | 8 | 0.9000 |
| 13 | `zelai` | 20 | 18 | 0.8636 | `ikez` | 60 | 54 | 0.8871 |
| 14 | `ate` | 50 | 43 | 0.8462 | `in` | 95 | 83 | 0.8660 |
| 15 | `eki` | 50 | 43 | 0.8462 | `loear` | 40 | 35 | 0.8571 |
| 16 | `ile` | 50 | 42 | 0.8269 | `ezlal` | 80 | 67 | 0.8293 |
| 17 | `lan` | 50 | 42 | 0.8269 | `itx` | 85 | 71 | 0.8276 |
| 18 | `alaba` | 20 | 17 | 0.8182 | `iaem` | 240 | 196 | 0.8140 |
| 19 | `itsaso` | 20 | 17 | 0.8182 | `ngeo` | 60 | 49 | 0.8065 |
| 20 | `zortzi` | 20 | 16 | 0.7727 | `ronk` | 60 | 48 | 0.7903 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `an` | 70 | 70 | 0.9861 | 1.000 | 0.9861 |
| 2 | control | `enaa` | 60 | 60 | 0.9839 | 1.000 | 0.9839 |
| 3 | control | `eal` | 32 | 32 | 0.9706 | 1.000 | 0.9706 |
| 4 | control | `anai` | 60 | 59 | 0.9677 | 1.000 | 0.9677 |
| 5 | substrate | `entzun` | 20 | 20 | 0.9545 | 1.000 | 0.9545 |
| 6 | control | `onia` | 120 | 114 | 0.9426 | 1.000 | 0.9426 |
| 7 | substrate | `aitz` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 8 | control | `anao` | 60 | 57 | 0.9355 | 1.000 | 0.9355 |
| 9 | control | `aatzasl` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 10 | control | `riieen` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 11 | substrate | `izotz` | 49 | 46 | 0.9216 | 1.000 | 0.9216 |
| 12 | control | `zaa` | 96 | 89 | 0.9184 | 1.000 | 0.9184 |
| 13 | control | `txiah` | 120 | 111 | 0.9180 | 1.000 | 0.9180 |
| 14 | substrate | `ahuntz` | 20 | 19 | 0.9091 | 1.000 | 0.9091 |
| 15 | substrate | `etxe` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 16 | substrate | `gatz` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 17 | substrate | `ona` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 18 | control | `aiab` | 60 | 55 | 0.9032 | 1.000 | 0.9032 |
| 19 | control | `ikez` | 60 | 54 | 0.8871 | 1.000 | 0.8871 |
| 20 | substrate | `non` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 21 | substrate | `oin` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 22 | substrate | `anai` | 49 | 44 | 0.8824 | 1.000 | 0.8824 |
| 23 | control | `in` | 95 | 83 | 0.8660 | 1.000 | 0.8660 |
| 24 | substrate | `ama` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 25 | substrate | `eta` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 26 | substrate | `zelai` | 20 | 18 | 0.8636 | 1.000 | 0.8636 |
| 27 | control | `loear` | 40 | 35 | 0.8571 | 1.000 | 0.8571 |
| 28 | substrate | `ate` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 29 | substrate | `eki` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 30 | control | `ezlal` | 80 | 67 | 0.8293 | 1.000 | 0.8293 |
| 31 | control | `itx` | 85 | 71 | 0.8276 | 1.000 | 0.8276 |
| 32 | substrate | `ile` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 33 | substrate | `lan` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 34 | control | `ehaahee` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 35 | substrate | `alaba` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 36 | substrate | `itsaso` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 37 | control | `iaem` | 240 | 196 | 0.8140 | 1.000 | 0.8140 |
| 38 | control | `ngeo` | 60 | 49 | 0.8065 | 1.000 | 0.8065 |
| 39 | control | `ronk` | 60 | 48 | 0.7903 | 1.000 | 0.7903 |
| 40 | control | `aahzl` | 40 | 32 | 0.7857 | 1.000 | 0.7857 |
| 41 | control | `ntsilai` | 12 | 10 | 0.7857 | 1.000 | 0.7857 |
| 42 | substrate | `zortzi` | 20 | 16 | 0.7727 | 1.000 | 0.7727 |
| 43 | substrate | `aho` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 44 | substrate | `bai` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 45 | substrate | `zuhaitz` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 46 | control | `eass` | 60 | 46 | 0.7581 | 1.000 | 0.7581 |
| 47 | substrate | `sei` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 48 | substrate | `gaitz` | 49 | 37 | 0.7451 | 1.000 | 0.7451 |
| 49 | substrate | `ohe` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 50 | substrate | `ume` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `basque`.
- Target corpus: CHIC syllabographic-only stream (`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 / mg-9700).
- Substrate pool: `aquitanian`. Control pool: `control_aquitanian` — Linear-A-shape control reused verbatim per the chic-v3 brief; matched controls are about substrate phoneme shape, not target-corpus shape, so reusing the existing controls keeps the chic-v3 result directly comparable to the Linear A v10 / v18 / v21 numbers.
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same CHIC corpus, pool YAMLs, and LM. No RNG anywhere in the pipeline.
- Corpus-size caveat: CHIC's syllabographic-only stream is roughly an order of magnitude smaller than Linear A's (see `corpora/cretan_hieroglyphic/syllabographic_stats.md`); the framework's discriminating power is corpus-size-dependent. Borderline p-values (0.04 < p < 0.10) should be read as informative-but-underpowered rather than definitive.

