# v23 cross-LM gate — toponym substrate under Eteocretan LM (mg-b599) — under Eteocretan LM (reverse cross-LM check)

**Headline: the toponym substrate pool PASSes the v10 right-tail bayesian gate against control_toponym_bigram when both sides are scored under the Eteocretan LM at p=2.503e-02** (median substrate posterior 0.9615 vs median control posterior 0.9189; gap +0.0427).

## Acceptance gate

| substrate pool | control pool | LM | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| toponym | control_toponym_bigram | Eteocretan | 20 | 20 | 0.9615 | 0.9189 | 272.5 | 2.503e-02 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9458. Mean of top-20 control posterior_mean: 0.9210. Gap (median, gate-relevant): +0.0427; gap (mean): +0.0248. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `ina` | 50 | 50 | 0.9808 | `issos` | 155 | 155 | 0.9936 |
| 2 | `kno` | 50 | 50 | 0.9808 | `iso` | 64 | 64 | 0.9848 |
| 3 | `lem` | 50 | 50 | 0.9808 | `goraro` | 24 | 24 | 0.9615 |
| 4 | `les` | 50 | 50 | 0.9808 | `thos` | 39 | 38 | 0.9512 |
| 5 | `nthe` | 50 | 50 | 0.9808 | `iss` | 14 | 14 | 0.9375 |
| 6 | `tarra` | 50 | 50 | 0.9808 | `ssosa` | 14 | 14 | 0.9375 |
| 7 | `ter` | 50 | 50 | 0.9808 | `oss` | 13 | 13 | 0.9333 |
| 8 | `thebai` | 50 | 50 | 0.9808 | `airso` | 26 | 25 | 0.9286 |
| 9 | `iassos` | 24 | 24 | 0.9615 | `ososoniena` | 12 | 12 | 0.9286 |
| 10 | `kuthera` | 24 | 24 | 0.9615 | `abeti` | 36 | 34 | 0.9211 |
| 11 | `tiruns` | 24 | 24 | 0.9615 | `tak` | 10 | 10 | 0.9167 |
| 12 | `amnisos` | 13 | 13 | 0.9333 | `tiososs` | 10 | 10 | 0.9167 |
| 13 | `mukenai` | 13 | 13 | 0.9333 | `inaletos` | 44 | 41 | 0.9130 |
| 14 | `praisos` | 13 | 13 | 0.9333 | `nthoi` | 170 | 156 | 0.9128 |
| 15 | `naxos` | 24 | 23 | 0.9231 | `lioss` | 55 | 50 | 0.8947 |
| 16 | `ssos` | 50 | 47 | 0.9231 | `omospa` | 24 | 22 | 0.8846 |
| 17 | `aios` | 50 | 46 | 0.9038 | `kospe` | 31 | 28 | 0.8788 |
| 18 | `phai` | 50 | 45 | 0.8846 | `ain` | 6 | 6 | 0.8750 |
| 19 | `erymanthos` | 6 | 6 | 0.8750 | `isososss` | 6 | 6 | 0.8750 |
| 20 | `salaminos` | 6 | 6 | 0.8750 | `therarossss` | 6 | 6 | 0.8750 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `issos` | 155 | 155 | 0.9936 | 1.000 | 0.9936 |
| 2 | control | `iso` | 64 | 64 | 0.9848 | 1.000 | 0.9848 |
| 3 | substrate | `ina` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `kno` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `lem` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `les` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `nthe` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `tarra` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `ter` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `thebai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `iassos` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 12 | substrate | `kuthera` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 13 | substrate | `tiruns` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 14 | control | `goraro` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 15 | control | `thos` | 39 | 38 | 0.9512 | 1.000 | 0.9512 |
| 16 | control | `iss` | 14 | 14 | 0.9375 | 1.000 | 0.9375 |
| 17 | control | `ssosa` | 14 | 14 | 0.9375 | 1.000 | 0.9375 |
| 18 | substrate | `amnisos` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 19 | substrate | `mukenai` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 20 | substrate | `praisos` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 21 | control | `oss` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 22 | control | `airso` | 26 | 25 | 0.9286 | 1.000 | 0.9286 |
| 23 | control | `ososoniena` | 12 | 12 | 0.9286 | 1.000 | 0.9286 |
| 24 | substrate | `naxos` | 24 | 23 | 0.9231 | 1.000 | 0.9231 |
| 25 | substrate | `ssos` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 26 | control | `abeti` | 36 | 34 | 0.9211 | 1.000 | 0.9211 |
| 27 | control | `tak` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 28 | control | `tiososs` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 29 | control | `inaletos` | 44 | 41 | 0.9130 | 1.000 | 0.9130 |
| 30 | control | `nthoi` | 170 | 156 | 0.9128 | 1.000 | 0.9128 |
| 31 | substrate | `aios` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 32 | control | `lioss` | 55 | 50 | 0.8947 | 1.000 | 0.8947 |
| 33 | substrate | `phai` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 34 | control | `omospa` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 35 | control | `kospe` | 31 | 28 | 0.8788 | 1.000 | 0.8788 |
| 36 | substrate | `athenai` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 37 | substrate | `itanos` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 38 | control | `tenthe` | 76 | 63 | 0.8205 | 1.000 | 0.8205 |
| 39 | control | `mni` | 30 | 25 | 0.8125 | 1.000 | 0.8125 |
| 40 | substrate | `ami` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 41 | substrate | `lasaia` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 42 | control | `ham` | 73 | 59 | 0.8000 | 1.000 | 0.8000 |
| 43 | control | `iebza` | 27 | 22 | 0.7931 | 1.000 | 0.7931 |
| 44 | control | `ale` | 87 | 68 | 0.7753 | 1.000 | 0.7753 |
| 45 | substrate | `ther` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 46 | control | `aiosontho` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 47 | substrate | `ikaria` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 48 | substrate | `muke` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |
| 49 | substrate | `priene` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 50 | substrate | `thera` | 50 | 37 | 0.7308 | 1.000 | 0.7308 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (label: Eteocretan). Substrate pool: `toponym` (20 top surfaces). Control pool: `control_toponym_bigram` (20 top surfaces).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG.

