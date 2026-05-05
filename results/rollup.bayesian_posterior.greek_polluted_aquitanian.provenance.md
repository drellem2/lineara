# v15 cross-language pollution — provenance breakdown (mg-7ecb)

**The cross-language polluted Aquitanian pool clears the v10 right-tail bayesian gate at p = 2.006e-03 (top-20 split: 13 real / 7 conjectural-greek), AND within the right tail real Aquitanian surfaces dominate Greek-shape conjecturals at p = 8.292e-05.** This is the *partial-discrimination* outcome: the gate has measurable shape selectivity (Greek-shape conjecturals score lower than real Aquitanian within the substrate-side right tail) but not enough to flip the headline gate to FAIL — the LM still rewards Greek-shape phonotactic strings well enough relative to scramble controls. The v14 manuscript-shape claim ('any pool whose phoneme + length distribution is drawn from the substrate's own marginal distribution') is **refined**: the framework discriminates substrate-shape from non-substrate-shape *within* the right tail, but the population gate clears for any pool with non-trivial char-bigram overlap with the LM.

## Acceptance gate (cross-language vs same-distribution vs clean)

| pool | n_substrate_top | n_control_top | median(top substrate posterior) | median(top control posterior) | MW U | MW p (one-tail, substrate>control) | gate |
|:--|---:|---:|---:|---:|---:|---:|:--:|
| greek_polluted_aquitanian (v15, cross-language) | 20 | 20 | 0.9808 | 0.9735 | 300.0 | 2.006e-03 | PASS |
| polluted_aquitanian (v14, same-distribution) | 20 | 20 | 0.9808 | 0.9572 | 340.0 | 2.740e-05 | PASS |
| aquitanian (v10, clean) | 20 | 20 | 0.9808 | 0.9512 | 345.0 | 3.222e-05 | PASS |

## Provenance breakdown of the polluted-pool top-20

Of the **20** surfaces with the highest substrate posteriors in the cross-language polluted pool:

- **`provenance: real`:**             **13** (65.0%)
- **`provenance: conjectural_greek`:** **7** (35.0%)
- *unknown* (sanity check, should be 0): **0**

v14's same-distribution polluted pool top-20 was 9 real / 11 conjectural (~50/50); v15's split is 13/7 = 13:7.

## Polluted-pool top-20 substrate surfaces, with provenance tag

| rank | surface | provenance | n | k | posterior mean | CI low | CI high |
|---:|---|:--|---:|---:|---:|---:|---:|
| 1 | `aitz` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 2 | `aki` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 3 | `ame` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 4 | `anai` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 5 | `ate` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 6 | `awa` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 7 | `bai` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 8 | `begi` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 9 | `behi` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 10 | `bi` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 11 | `eki` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 12 | `entzun` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 13 | `esku` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 14 | `eta` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 15 | `fren` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 16 | `gau` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 17 | `haize` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 18 | `ini` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 19 | `joten` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 20 | `kare` | conjectural_greek | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |

## Real-only vs conjectural-greek-only top-20 (within-tail discrimination)

Splitting the cross-language polluted pool's substrate posteriors by provenance and ranking each side independently lets us check whether real Aquitanian surfaces dominate over Greek-shape conjecturals when both have a level playing field. If real dominates, the framework discriminates within the right tail even when it can't break the headline gate.

| | n | median posterior | mean posterior | min | max |
|:--|---:|---:|---:|---:|---:|
| real (top-20)              | 20 | 0.9808 | 0.9808 | 0.9808 | 0.9808 |
| conjectural_greek (top-20) | 20 | 0.9519 | 0.9404 | 0.8462 | 0.9808 |

Mann-Whitney U one-tail (real > conjectural_greek) on the two top-20 sets: U = 310.0, p = 8.292e-05.

Real surfaces dominate the right tail relative to Greek-shape conjecturals at p<0.05. **Within-tail discrimination is detectable** even though the headline gate may PASS or FAIL depending on aggregation. Combined with v14 (which found NO within-tail discrimination on same-distribution pollution, real-vs-conjectural MW p = 0.98), v15 shows the framework can distinguish substrate-shape from non-substrate-shape — but only when the polluting distribution is *different enough*. v14's same-Aquitanian-shape conjecturals are indistinguishable from real Aquitanian; v15's Greek-shape conjecturals are distinguishable.

## Distribution shift on real surfaces (clean Aquitanian → cross-language polluted)

Surfaces present in both rollups (real-provenance only): **153**.

| | mean posterior | median posterior | min | max |
|:--|---:|---:|---:|---:|
| clean Aquitanian        | 0.5033 | 0.5192 | 0.0125 | 0.9818 |
| cross-language polluted | 0.5484 | 0.5192 | 0.0192 | 0.9808 |

- **Mean Δ (cross-language − clean):** +0.0451
- **Median Δ:**                       +0.0577
- **Pos / neg counts:** +85 / −65 / =0: 3

Top-10 surfaces by absolute posterior shift:

| surface | clean posterior | cross-language posterior | Δ |
|---|---:|---:|---:|
| `anai` | 0.0175 | 0.9808 | +0.9632 |
| `argi` | 0.9630 | 0.0192 | -0.9437 |
| `bihotz` | 0.9808 | 0.0385 | -0.9423 |
| `bi` | 0.0893 | 0.9808 | +0.8915 |
| `harri` | 0.0577 | 0.9423 | +0.8846 |
| `buru` | 0.0962 | 0.9423 | +0.8462 |
| `erori` | 0.7885 | 0.0192 | -0.7692 |
| `ilur` | 0.0154 | 0.7692 | +0.7538 |
| `ibai` | 0.0192 | 0.7692 | +0.7500 |
| `ilun` | 0.0952 | 0.8077 | +0.7125 |

## Notes

- This file is a v15-specific summary on top of `results/rollup.bayesian_posterior.greek_polluted_aquitanian.md`. Re-run with `python3 scripts/v15_cross_language_pollution_analysis.py` after any change that affects the bayesian rollup.
- The provenance map is read from `pools/greek_polluted_aquitanian.yaml` directly — every entry has a `provenance` field (`real` or `conjectural_greek`).
- Metric: `external_phoneme_perplexity_v0`. Top-K: 20. n_min: 10. No randomness in this script.

