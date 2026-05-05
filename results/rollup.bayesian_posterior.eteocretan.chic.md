# chic-v3 — pool=eteocretan right-tail bayesian gate on CHIC (mg-9700)

**Headline: the eteocretan substrate pool PASSes the v10 right-tail bayesian gate against control_eteocretan_bigram on the CHIC syllabographic corpus at p=7.329e-04** (median substrate posterior 0.8038 vs median control posterior 0.6927). Linear A v10 / v18 / v21 framework PASS reproduces on CHIC.

## Acceptance gate

| substrate pool | control pool | LM | n paired windows | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | eteocretan | 2286 | 20 | 20 | 0.8038 | 0.6927 | 318.0 | 7.329e-04 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8413. Mean of top-20 control posterior_mean: 0.7068. Gap: +0.1344. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side (gate input)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `mi` | 50 | 50 | 0.9808 | `isai` | 51 | 50 | 0.9623 |
| 2 | `os` | 50 | 50 | 0.9808 | `enonin` | 12 | 11 | 0.8571 |
| 3 | `si` | 50 | 50 | 0.9808 | `iaiete` | 12 | 11 | 0.8571 |
| 4 | `ine` | 50 | 49 | 0.9615 | `owaipbi` | 9 | 8 | 0.8182 |
| 5 | `noi` | 50 | 45 | 0.8846 | `disa` | 51 | 42 | 0.8113 |
| 6 | `iareion` | 6 | 6 | 0.8750 | `ionoi` | 56 | 46 | 0.8103 |
| 7 | `wai` | 50 | 44 | 0.8654 | `ieti` | 34 | 27 | 0.7778 |
| 8 | `siatas` | 11 | 10 | 0.8462 | `ial` | 30 | 23 | 0.7500 |
| 9 | `inai` | 49 | 42 | 0.8431 | `iamet` | 14 | 11 | 0.7500 |
| 10 | `ier` | 50 | 41 | 0.8077 | `ete` | 90 | 63 | 0.6957 |
| 11 | `arkaginoi` | 3 | 3 | 0.8000 | `isar` | 85 | 59 | 0.6897 |
| 12 | `parsiphai` | 3 | 3 | 0.8000 | `ianteiarkal` | 1 | 1 | 0.6667 |
| 13 | `des` | 50 | 40 | 0.7885 | `senkpioe` | 4 | 3 | 0.6667 |
| 14 | `kse` | 50 | 40 | 0.7885 | `inipina` | 9 | 6 | 0.6364 |
| 15 | `iarei` | 20 | 16 | 0.7727 | `isal` | 85 | 54 | 0.6322 |
| 16 | `ieroi` | 20 | 16 | 0.7727 | `egiei` | 56 | 32 | 0.5690 |
| 17 | `iemete` | 11 | 9 | 0.7692 | `kaisi` | 28 | 16 | 0.5667 |
| 18 | `inaipe` | 11 | 9 | 0.7692 | `ima` | 30 | 17 | 0.5625 |
| 19 | `komnai` | 11 | 9 | 0.7692 | `into` | 68 | 38 | 0.5571 |
| 20 | `magini` | 11 | 9 | 0.7692 | `bomadome` | 8 | 4 | 0.5000 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | substrate | `mi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 2 | substrate | `os` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `si` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | control | `isai` | 51 | 50 | 0.9623 | 1.000 | 0.9623 |
| 5 | substrate | `ine` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 6 | substrate | `noi` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 7 | substrate | `wai` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 8 | control | `enonin` | 12 | 11 | 0.8571 | 1.000 | 0.8571 |
| 9 | control | `iaiete` | 12 | 11 | 0.8571 | 1.000 | 0.8571 |
| 10 | substrate | `siatas` | 11 | 10 | 0.8462 | 1.000 | 0.8462 |
| 11 | substrate | `inai` | 49 | 42 | 0.8431 | 1.000 | 0.8431 |
| 12 | control | `disa` | 51 | 42 | 0.8113 | 1.000 | 0.8113 |
| 13 | control | `ionoi` | 56 | 46 | 0.8103 | 1.000 | 0.8103 |
| 14 | substrate | `ier` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 15 | substrate | `des` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 16 | substrate | `kse` | 50 | 40 | 0.7885 | 1.000 | 0.7885 |
| 17 | control | `owaipbi` | 9 | 8 | 0.8182 | 0.900 | 0.7864 |
| 18 | control | `ieti` | 34 | 27 | 0.7778 | 1.000 | 0.7778 |
| 19 | substrate | `iarei` | 20 | 16 | 0.7727 | 1.000 | 0.7727 |
| 20 | substrate | `ieroi` | 20 | 16 | 0.7727 | 1.000 | 0.7727 |
| 21 | substrate | `iemete` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 22 | substrate | `inaipe` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 23 | substrate | `komnai` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 24 | substrate | `magini` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 25 | substrate | `sameti` | 11 | 9 | 0.7692 | 1.000 | 0.7692 |
| 26 | substrate | `dioi` | 49 | 38 | 0.7647 | 1.000 | 0.7647 |
| 27 | substrate | `onoi` | 49 | 38 | 0.7647 | 1.000 | 0.7647 |
| 28 | substrate | `ona` | 50 | 38 | 0.7500 | 1.000 | 0.7500 |
| 29 | control | `ial` | 30 | 23 | 0.7500 | 1.000 | 0.7500 |
| 30 | control | `iamet` | 14 | 11 | 0.7500 | 1.000 | 0.7500 |
| 31 | substrate | `onai` | 49 | 37 | 0.7451 | 1.000 | 0.7451 |
| 32 | substrate | `iar` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 33 | substrate | `iareion` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 34 | substrate | `ieme` | 49 | 35 | 0.7059 | 1.000 | 0.7059 |
| 35 | control | `ete` | 90 | 63 | 0.6957 | 1.000 | 0.6957 |
| 36 | substrate | `omoion` | 11 | 8 | 0.6923 | 1.000 | 0.6923 |
| 37 | substrate | `omosai` | 11 | 8 | 0.6923 | 1.000 | 0.6923 |
| 38 | control | `isar` | 85 | 59 | 0.6897 | 1.000 | 0.6897 |
| 39 | substrate | `wow` | 50 | 34 | 0.6731 | 1.000 | 0.6731 |
| 40 | substrate | `sam` | 50 | 33 | 0.6538 | 1.000 | 0.6538 |
| 41 | substrate | `netamoi` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 42 | substrate | `epioi` | 20 | 13 | 0.6364 | 1.000 | 0.6364 |
| 43 | control | `isal` | 85 | 54 | 0.6322 | 1.000 | 0.6322 |
| 44 | control | `inipina` | 9 | 6 | 0.6364 | 0.900 | 0.6227 |
| 45 | substrate | `mo` | 50 | 31 | 0.6154 | 1.000 | 0.6154 |
| 46 | substrate | `wantai` | 11 | 7 | 0.6154 | 1.000 | 0.6154 |
| 47 | substrate | `omai` | 49 | 30 | 0.6078 | 1.000 | 0.6078 |
| 48 | substrate | `arkaginoi` | 3 | 3 | 0.8000 | 0.300 | 0.5900 |
| 49 | substrate | `parsiphai` | 3 | 3 | 0.8000 | 0.300 | 0.5900 |
| 50 | substrate | `epimere` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan`.
- Target corpus: CHIC syllabographic-only stream (`corpora/cretan_hieroglyphic/syllabographic.jsonl`, chic-v3 / mg-9700).
- Substrate pool: `eteocretan`. Control pool: `control_eteocretan_bigram` — Linear-A-shape control reused verbatim per the chic-v3 brief; matched controls are about substrate phoneme shape, not target-corpus shape, so reusing the existing controls keeps the chic-v3 result directly comparable to the Linear A v10 / v18 / v21 numbers.
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same CHIC corpus, pool YAMLs, and LM. No RNG anywhere in the pipeline.
- Corpus-size caveat: CHIC's syllabographic-only stream is roughly an order of magnitude smaller than Linear A's (see `corpora/cretan_hieroglyphic/syllabographic_stats.md`); the framework's discriminating power is corpus-size-dependent. Borderline p-values (0.04 < p < 0.10) should be read as informative-but-underpowered rather than definitive.

