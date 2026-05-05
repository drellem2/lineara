# v21 Eteocretan substrate pool — right-tail bayesian gate (mg-6ccd)

**Headline: the Eteocretan substrate pool PASSes the v10 right-tail bayesian gate against the bigram-preserving control at p=4.096e-06** (median substrate posterior 0.9712 vs median control posterior 0.7697). Eteocretan — the closest-genealogical-relative candidate substrate (presumed Linear-A continuation) — joins Aquitanian + Etruscan + toponym as the 4th external-validation pool to clear the gate. Methodology paper §3.14 narrative: the framework detects phonotactic kinship between Linear A and the candidate substrate that the consensus already treats as its linguistic descendant — the strongest a-priori case in the validation series.

## Acceptance gate

| substrate pool | control pool | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | 20 | 20 | 0.9712 | 0.7697 | 364.0 | 4.096e-06 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9569. Mean of top-20 control posterior_mean: 0.7911. Gap: +0.1657. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `iar` | 50 | 50 | 0.9808 | `isai` | 97 | 97 | 0.9899 |
| 2 | `iarei` | 50 | 50 | 0.9808 | `ieti` | 163 | 158 | 0.9636 |
| 3 | `ine` | 50 | 50 | 0.9808 | `owaiais` | 21 | 20 | 0.9130 |
| 4 | `isala` | 50 | 50 | 0.9808 | `into` | 60 | 55 | 0.9032 |
| 5 | `mi` | 50 | 50 | 0.9808 | `ionoi` | 109 | 97 | 0.8829 |
| 6 | `noi` | 50 | 50 | 0.9808 | `ipisa` | 6 | 6 | 0.8750 |
| 7 | `os` | 50 | 50 | 0.9808 | `isar` | 6 | 6 | 0.8750 |
| 8 | `sam` | 50 | 50 | 0.9808 | `iaiete` | 42 | 37 | 0.8636 |
| 9 | `si` | 50 | 50 | 0.9808 | `pepim` | 12 | 11 | 0.8571 |
| 10 | `wai` | 50 | 50 | 0.9808 | `ete` | 131 | 104 | 0.7895 |
| 11 | `des` | 50 | 49 | 0.9615 | `inipina` | 2 | 2 | 0.7500 |
| 12 | `ona` | 50 | 49 | 0.9615 | `iomoso` | 74 | 56 | 0.7500 |
| 13 | `wantai` | 24 | 24 | 0.9615 | `omo` | 55 | 39 | 0.7018 |
| 14 | `arka` | 50 | 48 | 0.9423 | `inatetoip` | 8 | 6 | 0.7000 |
| 15 | `dioi` | 50 | 48 | 0.9423 | `intokame` | 8 | 6 | 0.7000 |
| 16 | `iareion` | 13 | 13 | 0.9333 | `iphonzeie` | 11 | 8 | 0.6923 |
| 17 | `netamoi` | 13 | 13 | 0.9333 | `konamemer` | 1 | 1 | 0.6667 |
| 18 | `ier` | 50 | 47 | 0.9231 | `senkpioe` | 16 | 11 | 0.6667 |
| 19 | `wow` | 50 | 46 | 0.9038 | `siag` | 4 | 3 | 0.6667 |
| 20 | `epimere` | 13 | 12 | 0.8667 | `nadina` | 24 | 15 | 0.6154 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `isai` | 97 | 97 | 0.9899 | 1.000 | 0.9899 |
| 2 | substrate | `iar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 3 | substrate | `iarei` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `ine` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `isala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `mi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `noi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `os` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `sam` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `si` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | control | `ieti` | 163 | 158 | 0.9636 | 1.000 | 0.9636 |
| 13 | substrate | `des` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 14 | substrate | `ona` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 15 | substrate | `wantai` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 16 | substrate | `arka` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 17 | substrate | `dioi` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 18 | substrate | `iareion` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 19 | substrate | `netamoi` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 20 | substrate | `ier` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 21 | control | `owaiais` | 21 | 20 | 0.9130 | 1.000 | 0.9130 |
| 22 | substrate | `wow` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 23 | control | `into` | 60 | 55 | 0.9032 | 1.000 | 0.9032 |
| 24 | control | `ionoi` | 109 | 97 | 0.8829 | 1.000 | 0.8829 |
| 25 | substrate | `epimere` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 26 | control | `iaiete` | 42 | 37 | 0.8636 | 1.000 | 0.8636 |
| 27 | control | `pepim` | 12 | 11 | 0.8571 | 1.000 | 0.8571 |
| 28 | substrate | `omali` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 29 | substrate | `mo` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 30 | substrate | `epioi` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 31 | substrate | `sante` | 50 | 41 | 0.8077 | 1.000 | 0.8077 |
| 32 | control | `ete` | 131 | 104 | 0.7895 | 1.000 | 0.7895 |
| 33 | substrate | `arkadi` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 34 | substrate | `enete` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 35 | substrate | `niate` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 36 | control | `iomoso` | 74 | 56 | 0.7500 | 1.000 | 0.7500 |
| 37 | control | `ipisa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 38 | control | `isar` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 39 | control | `omo` | 55 | 39 | 0.7018 | 1.000 | 0.7018 |
| 40 | substrate | `barkse` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 41 | substrate | `inaipe` | 24 | 17 | 0.6923 | 1.000 | 0.6923 |
| 42 | substrate | `omai` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 43 | control | `iphonzeie` | 11 | 8 | 0.6923 | 1.000 | 0.6923 |
| 44 | substrate | `inaiperima` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 45 | control | `senkpioe` | 16 | 11 | 0.6667 | 1.000 | 0.6667 |
| 46 | substrate | `isalabre` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |
| 47 | control | `inatetoip` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |
| 48 | control | `intokame` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |
| 49 | substrate | `rima` | 50 | 33 | 0.6538 | 1.000 | 0.6538 |
| 50 | substrate | `sameti` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (α=1.0, ~87 word forms; see `harness/external_phoneme_models/eteocretan.json`).
- Substrate pool: `eteocretan` (20 top surfaces of ~84 entries). Control pool: `control_eteocretan_bigram` (20 top surfaces of ~84 entries; bigram-preserving sampler — the v18 production default for new pools).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG anywhere in the pipeline.
- Small-corpus caveat: the Eteocretan LM is built from ~87 unique word forms, ~6× smaller than Etruscan and ~80× smaller than Basque. Per-surface posteriors are correspond-ingly noisier than in v10-v18 work; the gate tolerates this tolerable by using the *right-tail* (top-K) comparison rather than the bulk-distribution Wilcoxon.

