# chic-v3 — pool=toponym right-tail bayesian gate on CHIC (mg-9700)

**Headline: the toponym substrate pool FAILs the v10 right-tail bayesian gate against control_toponym_bigram on the CHIC syllabographic corpus at p=4.350e-01** (median substrate posterior 0.7941 vs median control posterior 0.7874). Cross-script transfer of the Linear A toponym signal to CHIC is not detected at the gate threshold; CHIC's smaller corpus reduces the framework's discriminating power and a borderline p-value should be read with that caveat in mind.

## Acceptance gate

| substrate pool | control pool | LM | n paired windows | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| toponym | control_toponym_bigram | basque | 2599 | 20 | 20 | 0.7941 | 0.7874 | 206.5 | 4.350e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8059. Mean of top-20 control posterior_mean: 0.7928. Gap: +0.0131. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side (gate input)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `lasaia` | 11 | 11 | 0.9231 | `ena` | 75 | 74 | 0.9740 |
| 2 | `lebena` | 11 | 11 | 0.9231 | `ale` | 25 | 24 | 0.9259 |
| 3 | `aios` | 49 | 44 | 0.8824 | `kaiksals` | 9 | 9 | 0.9091 |
| 4 | `mukenai` | 6 | 6 | 0.8750 | `ain` | 100 | 91 | 0.9020 |
| 5 | `minoa` | 20 | 18 | 0.8636 | `lel` | 50 | 45 | 0.8846 |
| 6 | `ina` | 50 | 43 | 0.8462 | `lutinolua` | 6 | 6 | 0.8750 |
| 7 | `nax` | 49 | 42 | 0.8431 | `arin` | 13 | 12 | 0.8667 |
| 8 | `ala` | 50 | 42 | 0.8269 | `alpaia` | 19 | 17 | 0.8571 |
| 9 | `aksos` | 20 | 17 | 0.8182 | `iebza` | 36 | 31 | 0.8421 |
| 10 | `keos` | 49 | 40 | 0.8039 | `ape` | 125 | 99 | 0.7874 |
| 11 | `muke` | 49 | 39 | 0.7843 | `zin` | 125 | 99 | 0.7874 |
| 12 | `hierapytna` | 2 | 2 | 0.7500 | `taia` | 39 | 31 | 0.7805 |
| 13 | `kudonia` | 6 | 5 | 0.7500 | `akuthe` | 18 | 14 | 0.7500 |
| 14 | `kuzikos` | 6 | 5 | 0.7500 | `kerurtoia` | 6 | 5 | 0.7500 |
| 15 | `lykabettos` | 2 | 2 | 0.7500 | `osar` | 26 | 19 | 0.7143 |
| 16 | `melitos` | 6 | 5 | 0.7500 | `pales` | 36 | 25 | 0.6842 |
| 17 | `orchomenos` | 2 | 2 | 0.7500 | `alnisso` | 13 | 9 | 0.6667 |
| 18 | `phalasarna` | 2 | 2 | 0.7500 | `iso` | 50 | 32 | 0.6346 |
| 19 | `tirintha` | 6 | 5 | 0.7500 | `asbe` | 39 | 25 | 0.6341 |
| 20 | `andos` | 20 | 15 | 0.7273 | `kto` | 25 | 16 | 0.6296 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `ena` | 75 | 74 | 0.9740 | 1.000 | 0.9740 |
| 2 | control | `ale` | 25 | 24 | 0.9259 | 1.000 | 0.9259 |
| 3 | substrate | `lasaia` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 4 | substrate | `lebena` | 11 | 11 | 0.9231 | 1.000 | 0.9231 |
| 5 | control | `ain` | 100 | 91 | 0.9020 | 1.000 | 0.9020 |
| 6 | control | `lel` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 7 | substrate | `aios` | 49 | 44 | 0.8824 | 1.000 | 0.8824 |
| 8 | control | `kaiksals` | 9 | 9 | 0.9091 | 0.900 | 0.8682 |
| 9 | control | `arin` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 10 | substrate | `minoa` | 20 | 18 | 0.8636 | 1.000 | 0.8636 |
| 11 | control | `alpaia` | 19 | 17 | 0.8571 | 1.000 | 0.8571 |
| 12 | substrate | `ina` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 13 | substrate | `nax` | 49 | 42 | 0.8431 | 1.000 | 0.8431 |
| 14 | control | `iebza` | 36 | 31 | 0.8421 | 1.000 | 0.8421 |
| 15 | substrate | `ala` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 16 | substrate | `aksos` | 20 | 17 | 0.8182 | 1.000 | 0.8182 |
| 17 | substrate | `keos` | 49 | 40 | 0.8039 | 1.000 | 0.8039 |
| 18 | control | `ape` | 125 | 99 | 0.7874 | 1.000 | 0.7874 |
| 19 | control | `zin` | 125 | 99 | 0.7874 | 1.000 | 0.7874 |
| 20 | substrate | `muke` | 49 | 39 | 0.7843 | 1.000 | 0.7843 |
| 21 | control | `taia` | 39 | 31 | 0.7805 | 1.000 | 0.7805 |
| 22 | control | `akuthe` | 18 | 14 | 0.7500 | 1.000 | 0.7500 |
| 23 | substrate | `andos` | 20 | 15 | 0.7273 | 1.000 | 0.7273 |
| 24 | substrate | `lukia` | 20 | 15 | 0.7273 | 1.000 | 0.7273 |
| 25 | substrate | `mukenai` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 26 | control | `lutinolua` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 27 | control | `osar` | 26 | 19 | 0.7143 | 1.000 | 0.7143 |
| 28 | substrate | `kno` | 50 | 36 | 0.7115 | 1.000 | 0.7115 |
| 29 | substrate | `mnos` | 49 | 35 | 0.7059 | 1.000 | 0.7059 |
| 30 | substrate | `athenai` | 11 | 8 | 0.6923 | 1.000 | 0.6923 |
| 31 | substrate | `ikaria` | 11 | 8 | 0.6923 | 1.000 | 0.6923 |
| 32 | substrate | `mna` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 33 | control | `pales` | 36 | 25 | 0.6842 | 1.000 | 0.6842 |
| 34 | control | `alnisso` | 13 | 9 | 0.6667 | 1.000 | 0.6667 |
| 35 | substrate | `kudonia` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 36 | substrate | `kuzikos` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 37 | substrate | `melitos` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 38 | substrate | `tirintha` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 39 | control | `kerurtoia` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 40 | control | `iso` | 50 | 32 | 0.6346 | 1.000 | 0.6346 |
| 41 | control | `asbe` | 39 | 25 | 0.6341 | 1.000 | 0.6341 |
| 42 | control | `kto` | 25 | 16 | 0.6296 | 1.000 | 0.6296 |
| 43 | control | `abe` | 100 | 63 | 0.6275 | 1.000 | 0.6275 |
| 44 | control | `emndak` | 19 | 12 | 0.6190 | 1.000 | 0.6190 |
| 45 | substrate | `iassos` | 11 | 7 | 0.6154 | 1.000 | 0.6154 |
| 46 | substrate | `naxos` | 11 | 7 | 0.6154 | 1.000 | 0.6154 |
| 47 | control | `inaletos` | 18 | 11 | 0.6000 | 1.000 | 0.6000 |
| 48 | substrate | `aso` | 50 | 30 | 0.5962 | 1.000 | 0.5962 |
| 49 | control | `ospa` | 52 | 31 | 0.5926 | 1.000 | 0.5926 |
| 50 | substrate | `assos` | 20 | 12 | 0.5909 | 1.000 | 0.5909 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `basque`.
- Target corpus: CHIC syllabographic-only stream (`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 / mg-9700).
- Substrate pool: `toponym`. Control pool: `control_toponym_bigram` — Linear-A-shape control reused verbatim per the chic-v3 brief; matched controls are about substrate phoneme shape, not target-corpus shape, so reusing the existing controls keeps the chic-v3 result directly comparable to the Linear A v10 / v18 / v21 numbers.
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same CHIC corpus, pool YAMLs, and LM. No RNG anywhere in the pipeline.
- Corpus-size caveat: CHIC's syllabographic-only stream is roughly an order of magnitude smaller than Linear A's (see `corpora/cretan_hieroglyphic/syllabographic_stats.md`); the framework's discriminating power is corpus-size-dependent. Borderline p-values (0.04 < p < 0.10) should be read as informative-but-underpowered rather than definitive.

