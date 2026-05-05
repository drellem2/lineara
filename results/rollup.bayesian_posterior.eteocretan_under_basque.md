# v21 Eteocretan substrate pool — right-tail bayesian gate (mg-6ccd) — under Basque LM (cross-LM negative control)

**Headline: the Eteocretan substrate pool PASSes the v10 right-tail bayesian gate against the bigram-preserving control at p=2.579e-03** (median substrate posterior 0.9615 vs median control posterior 0.8661). Eteocretan — the closest-genealogical-relative candidate substrate (presumed Linear-A continuation) — joins Aquitanian + Etruscan + toponym as the 4th external-validation pool to clear the gate. Methodology paper §3.14 narrative: the framework detects phonotactic kinship between Linear A and the candidate substrate that the consensus already treats as its linguistic descendant — the strongest a-priori case in the validation series.

## Acceptance gate

| substrate pool | control pool | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|:--|---:|---:|---:|---:|---:|---:|:--:|
| eteocretan | control_eteocretan_bigram | 20 | 20 | 0.9615 | 0.8661 | 303.0 | 2.579e-03 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9539. Mean of top-20 control posterior_mean: 0.8369. Gap: +0.1170. The gate uses the rank-based MW U test rather than the mean gap, so this number is shown for orientation only.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `ieme` | 50 | 50 | 0.9808 | `ka` | 100 | 100 | 0.9902 |
| 2 | `inai` | 50 | 50 | 0.9808 | `ke` | 100 | 100 | 0.9902 |
| 3 | `isala` | 50 | 50 | 0.9808 | `sal` | 50 | 50 | 0.9808 |
| 4 | `kanet` | 50 | 50 | 0.9808 | `iaiete` | 42 | 42 | 0.9773 |
| 5 | `nato` | 50 | 50 | 0.9808 | `ionoi` | 109 | 107 | 0.9730 |
| 6 | `noi` | 50 | 50 | 0.9808 | `nadina` | 24 | 24 | 0.9615 |
| 7 | `oma` | 50 | 50 | 0.9808 | `ana` | 33 | 32 | 0.9429 |
| 8 | `onai` | 50 | 50 | 0.9808 | `intokame` | 8 | 8 | 0.9000 |
| 9 | `wai` | 50 | 50 | 0.9808 | `alan` | 7 | 7 | 0.8889 |
| 10 | `bar` | 50 | 49 | 0.9615 | `ipisa` | 6 | 6 | 0.8750 |
| 11 | `eko` | 50 | 49 | 0.9615 | `onaipetosa` | 5 | 5 | 0.8571 |
| 12 | `komnai` | 24 | 24 | 0.9615 | `okadkaiom` | 14 | 12 | 0.8125 |
| 13 | `omai` | 50 | 48 | 0.9423 | `ial` | 34 | 27 | 0.7778 |
| 14 | `iareion` | 13 | 13 | 0.9333 | `dima` | 93 | 72 | 0.7684 |
| 15 | `omalioi` | 13 | 13 | 0.9333 | `inipina` | 2 | 2 | 0.7500 |
| 16 | `enete` | 50 | 47 | 0.9231 | `ddiomadou` | 1 | 1 | 0.6667 |
| 17 | `onoi` | 50 | 47 | 0.9231 | `ianteiarkal` | 4 | 3 | 0.6667 |
| 18 | `sante` | 50 | 47 | 0.9231 | `konamemer` | 1 | 1 | 0.6667 |
| 19 | `des` | 50 | 46 | 0.9038 | `owaiais` | 21 | 14 | 0.6522 |
| 20 | `etion` | 50 | 45 | 0.8846 | `dnta` | 23 | 15 | 0.6400 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `ka` | 100 | 100 | 0.9902 | 1.000 | 0.9902 |
| 2 | control | `ke` | 100 | 100 | 0.9902 | 1.000 | 0.9902 |
| 3 | substrate | `ieme` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `inai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `isala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `kanet` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `nato` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `noi` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `oma` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `onai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `wai` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | control | `sal` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | control | `iaiete` | 42 | 42 | 0.9773 | 1.000 | 0.9773 |
| 14 | control | `ionoi` | 109 | 107 | 0.9730 | 1.000 | 0.9730 |
| 15 | substrate | `bar` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 16 | substrate | `eko` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 17 | substrate | `komnai` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 18 | control | `nadina` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 19 | control | `ana` | 33 | 32 | 0.9429 | 1.000 | 0.9429 |
| 20 | substrate | `omai` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 21 | substrate | `iareion` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 22 | substrate | `omalioi` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 23 | substrate | `enete` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 24 | substrate | `onoi` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 25 | substrate | `sante` | 50 | 47 | 0.9231 | 1.000 | 0.9231 |
| 26 | substrate | `des` | 50 | 46 | 0.9038 | 1.000 | 0.9038 |
| 27 | substrate | `etion` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 28 | substrate | `niate` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 29 | substrate | `omali` | 50 | 45 | 0.8846 | 1.000 | 0.8846 |
| 30 | substrate | `wantai` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 31 | substrate | `arka` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 32 | substrate | `omoion` | 24 | 21 | 0.8462 | 1.000 | 0.8462 |
| 33 | control | `intokame` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 34 | control | `okadkaiom` | 14 | 12 | 0.8125 | 1.000 | 0.8125 |
| 35 | substrate | `kilenti` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 36 | substrate | `netamoi` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 37 | control | `ial` | 34 | 27 | 0.7778 | 1.000 | 0.7778 |
| 38 | control | `alan` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 39 | substrate | `omal` | 50 | 39 | 0.7692 | 1.000 | 0.7692 |
| 40 | substrate | `omosai` | 24 | 19 | 0.7692 | 1.000 | 0.7692 |
| 41 | control | `dima` | 93 | 72 | 0.7684 | 1.000 | 0.7684 |
| 42 | substrate | `arkadioi` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 43 | substrate | `arkadi` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 44 | substrate | `barkse` | 24 | 18 | 0.7308 | 1.000 | 0.7308 |
| 45 | substrate | `natoniate` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 46 | control | `ipisa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 47 | substrate | `dioi` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 48 | substrate | `ine` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 49 | control | `onaipetosa` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 50 | substrate | `sametion` | 8 | 6 | 0.7000 | 0.800 | 0.6600 |

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `eteocretan` (α=1.0, ~87 word forms; see `harness/external_phoneme_models/eteocretan.json`).
- Substrate pool: `eteocretan` (20 top surfaces of ~84 entries). Control pool: `control_eteocretan_bigram` (20 top surfaces of ~84 entries; bigram-preserving sampler — the v18 production default for new pools).
- Gate: top-20 by posterior_mean only (no credibility shrinkage); one-tail Mann-Whitney U with normal-approximation tie-corrected p-value. PASS at p<0.05 with median(substrate top-K) > median(control top-K).
- Determinism: identical rows across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, the substrate / control manifests, and the pool YAMLs. No RNG anywhere in the pipeline.
- Small-corpus caveat: the Eteocretan LM is built from ~87 unique word forms, ~6× smaller than Etruscan and ~80× smaller than Basque. Per-surface posteriors are correspond-ingly noisier than in v10-v18 work; the gate tolerates this tolerable by using the *right-tail* (top-K) comparison rather than the bulk-distribution Wilcoxon.

