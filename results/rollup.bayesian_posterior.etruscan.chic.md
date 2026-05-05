# chic-v3 — pool=etruscan right-tail bayesian gate on CHIC (mg-9700)

**Headline: the etruscan substrate pool FAILs the v10 right-tail bayesian gate against control_etruscan on the CHIC syllabographic corpus at p=7.197e-01** (median substrate posterior 0.8534 vs median control posterior 0.8758). Cross-script transfer of the Linear A etruscan signal to CHIC is not detected at the gate threshold; CHIC's smaller corpus reduces the framework's discriminating power and a borderline p-value should be read with that caveat in mind.

## Acceptance gate

| substrate pool | control pool | LM | n paired windows | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| etruscan | control_etruscan | etruscan | 4490 | 20 | 20 | 0.8534 | 0.8758 | 179.0 | 7.197e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8630. Mean of top-20 control posterior_mean: 0.8760. Gap: -0.0131. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side (gate input)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `catha` | 49 | 47 | 0.9412 | `ichcch` | 36 | 36 | 0.9737 |
| 2 | `sath` | 50 | 47 | 0.9231 | `ththavi` | 36 | 36 | 0.9737 |
| 3 | `chimth` | 49 | 46 | 0.9216 | `thia` | 25 | 25 | 0.9630 |
| 4 | `mlach` | 49 | 46 | 0.9216 | `ithalam` | 20 | 20 | 0.9545 |
| 5 | `thana` | 49 | 46 | 0.9216 | `phtlleth` | 20 | 20 | 0.9545 |
| 6 | `thapna` | 20 | 19 | 0.9091 | `thi` | 54 | 52 | 0.9464 |
| 7 | `thesan` | 20 | 19 | 0.9091 | `muuavthth` | 12 | 12 | 0.9286 |
| 8 | `sech` | 50 | 46 | 0.9038 | `aalchci` | 20 | 19 | 0.9091 |
| 9 | `cilth` | 49 | 44 | 0.8824 | `ithalr` | 36 | 33 | 0.8947 |
| 10 | `camthi` | 20 | 18 | 0.8636 | `nthi` | 25 | 23 | 0.8889 |
| 11 | `semph` | 49 | 42 | 0.8431 | `arth` | 100 | 87 | 0.8627 |
| 12 | `lautnitha` | 4 | 4 | 0.8333 | `chsa` | 125 | 108 | 0.8583 |
| 13 | `mach` | 50 | 42 | 0.8269 | `zltha` | 144 | 120 | 0.8288 |
| 14 | `suthi` | 49 | 41 | 0.8235 | `sa` | 117 | 97 | 0.8235 |
| 15 | `ziche` | 49 | 41 | 0.8235 | `izththuch` | 40 | 33 | 0.8095 |
| 16 | `cealch` | 20 | 17 | 0.8182 | `chnrlalth` | 24 | 20 | 0.8077 |
| 17 | `hanthe` | 20 | 17 | 0.8182 | `lnth` | 75 | 60 | 0.7922 |
| 18 | `ramtha` | 20 | 17 | 0.8182 | `hsaa` | 36 | 29 | 0.7895 |
| 19 | `larth` | 49 | 39 | 0.7843 | `ssri` | 72 | 57 | 0.7838 |
| 20 | `zilath` | 20 | 16 | 0.7727 | `laz` | 25 | 20 | 0.7778 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `ichcch` | 36 | 36 | 0.9737 | 1.000 | 0.9737 |
| 2 | control | `ththavi` | 36 | 36 | 0.9737 | 1.000 | 0.9737 |
| 3 | control | `thia` | 25 | 25 | 0.9630 | 1.000 | 0.9630 |
| 4 | control | `ithalam` | 20 | 20 | 0.9545 | 1.000 | 0.9545 |
| 5 | control | `phtlleth` | 20 | 20 | 0.9545 | 1.000 | 0.9545 |
| 6 | control | `thi` | 54 | 52 | 0.9464 | 1.000 | 0.9464 |
| 7 | substrate | `catha` | 49 | 47 | 0.9412 | 1.000 | 0.9412 |
| 8 | control | `muuavthth` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 9 | substrate | `sath` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 10 | substrate | `chimth` | 49 | 46 | 0.9216 | 1.000 | 0.9216 |
| 11 | substrate | `mlach` | 49 | 46 | 0.9216 | 1.000 | 0.9216 |
| 12 | substrate | `thana` | 49 | 46 | 0.9216 | 1.000 | 0.9216 |
| 13 | substrate | `thapna` | 20 | 19 | 0.9091 | 1.000 | 0.9091 |
| 14 | substrate | `thesan` | 20 | 19 | 0.9091 | 1.000 | 0.9091 |
| 15 | control | `aalchci` | 20 | 19 | 0.9091 | 1.000 | 0.9091 |
| 16 | substrate | `sech` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 17 | control | `ithalr` | 36 | 33 | 0.8947 | 1.000 | 0.8947 |
| 18 | control | `nthi` | 25 | 23 | 0.8889 | 1.000 | 0.8889 |
| 19 | substrate | `cilth` | 49 | 44 | 0.8824 | 1.000 | 0.8824 |
| 20 | substrate | `camthi` | 20 | 18 | 0.8636 | 1.000 | 0.8636 |
| 21 | control | `arth` | 100 | 87 | 0.8627 | 1.000 | 0.8627 |
| 22 | control | `chsa` | 125 | 108 | 0.8583 | 1.000 | 0.8583 |
| 23 | substrate | `semph` | 49 | 42 | 0.8431 | 1.000 | 0.8431 |
| 24 | control | `zltha` | 144 | 120 | 0.8288 | 1.000 | 0.8288 |
| 25 | substrate | `mach` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 26 | substrate | `suthi` | 49 | 41 | 0.8235 | 1.000 | 0.8235 |
| 27 | substrate | `ziche` | 49 | 41 | 0.8235 | 1.000 | 0.8235 |
| 28 | control | `sa` | 117 | 97 | 0.8235 | 1.000 | 0.8235 |
| 29 | substrate | `cealch` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 30 | substrate | `hanthe` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 31 | substrate | `ramtha` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 32 | control | `izththuch` | 40 | 33 | 0.8095 | 1.000 | 0.8095 |
| 33 | control | `chnrlalth` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 34 | control | `lnth` | 75 | 60 | 0.7922 | 1.000 | 0.7922 |
| 35 | control | `hsaa` | 36 | 29 | 0.7895 | 1.000 | 0.7895 |
| 36 | substrate | `larth` | 49 | 39 | 0.7843 | 1.000 | 0.7843 |
| 37 | control | `ssri` | 72 | 57 | 0.7838 | 1.000 | 0.7838 |
| 38 | control | `laz` | 25 | 20 | 0.7778 | 1.000 | 0.7778 |
| 39 | substrate | `zilath` | 20 | 16 | 0.7727 | 1.000 | 0.7727 |
| 40 | substrate | `arnth` | 49 | 38 | 0.7647 | 1.000 | 0.7647 |
| 41 | control | `saem` | 36 | 27 | 0.7368 | 1.000 | 0.7368 |
| 42 | substrate | `aiser` | 20 | 15 | 0.7273 | 1.000 | 0.7273 |
| 43 | substrate | `matam` | 20 | 15 | 0.7273 | 1.000 | 0.7273 |
| 44 | substrate | `zilac` | 20 | 15 | 0.7273 | 1.000 | 0.7273 |
| 45 | substrate | `amce` | 49 | 36 | 0.7255 | 1.000 | 0.7255 |
| 46 | substrate | `clan` | 49 | 36 | 0.7255 | 1.000 | 0.7255 |
| 47 | substrate | `cesu` | 49 | 35 | 0.7059 | 1.000 | 0.7059 |
| 48 | control | `uthm` | 100 | 70 | 0.6961 | 1.000 | 0.6961 |
| 49 | substrate | `chia` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 50 | substrate | `thu` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `etruscan`.
- Target corpus: CHIC syllabographic-only stream (`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 / mg-9700).
- Substrate pool: `etruscan`. Control pool: `control_etruscan` — Linear-A-shape control reused verbatim per the chic-v3 brief; matched controls are about substrate phoneme shape, not target-corpus shape, so reusing the existing controls keeps the chic-v3 result directly comparable to the Linear A v10 / v18 / v21 numbers.
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same CHIC corpus, pool YAMLs, and LM. No RNG anywhere in the pipeline.
- Corpus-size caveat: CHIC's syllabographic-only stream is roughly an order of magnitude smaller than Linear A's (see `corpora/cretan_hieroglyphic/syllabographic_stats.md`); the framework's discriminating power is corpus-size-dependent. Borderline p-values (0.04 < p < 0.10) should be read as informative-but-underpowered rather than definitive.

