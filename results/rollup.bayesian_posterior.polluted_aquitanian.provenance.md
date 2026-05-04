# v14 polluted Aquitanian — provenance breakdown (mg-6b73)

Headline first: **the polluted Aquitanian pool clears the v10 right-tail bayesian gate**. The framework's PASS signal is *tolerant* of 50% conjectural pollution; reading #1 (substrate-LM-phonotactic kinship at the surface aggregate) is supported, and reading #2 (curation-sensitivity) is undermined as a wholesale account. v10's clean-Aquitanian PASS does not depend on every entry being valid.

## Acceptance gate

| pool | n_substrate_top | n_control_top | median(top substrate posterior) | median(top control posterior) | MW U | MW p (one-tail, substrate>control) | gate |
|:--|---:|---:|---:|---:|---:|---:|:--:|
| polluted_aquitanian | 20 | 20 | 0.9808 | 0.9572 | 340.0 | 2.740e-05 | PASS |
| aquitanian (v10) | 20 | 20 | 0.9808 | 0.9512 | 345.0 | 3.222e-05 | PASS |

## Provenance breakdown of the polluted-pool top-20

Of the **20** surfaces with the highest substrate posteriors in the polluted pool:

- **`provenance: real`:**       **9** (45.0%)
- **`provenance: conjectural`:** **11** (55.0%)
- *unknown* (sanity check, should be 0): **0**

**Interpretation.** The framework cannot distinguish real from conjectural surfaces in the right-tail; both provenances populate the top-K at roughly the rate expected if the gate were responding only to phonotactic shape, not to actual substrate-vocabulary identity.


## Polluted-pool top-20 substrate surfaces, with provenance tag

| rank | surface | provenance | n | k | posterior mean | CI low | CI high |
|---:|---|:--|---:|---:|---:|---:|---:|
| 1 | `aanah` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 2 | `aari` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 3 | `abek` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 4 | `ahe` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 5 | `ahuntz` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 6 | `air` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 7 | `aleoa` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 8 | `anoka` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 9 | `bai` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 10 | `bizi` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 11 | `bost` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 12 | `eil` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 13 | `eki` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 14 | `ekr` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 15 | `entzun` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 16 | `eoezd` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 17 | `etxe` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 18 | `gatz` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 19 | `iul` | conjectural | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |
| 20 | `izotz` | real | 50 | 50 | 0.9808 | 0.9302 | 0.9995 |

## Real-only vs conjectural-only top-20 (sanity check)

Splitting the polluted pool's substrate posteriors by provenance and ranking each side independently lets us check whether real surfaces dominate over conjecturals when both have a level playing field.

| | n | median posterior | mean posterior | min | max |
|:--|---:|---:|---:|---:|---:|
| real (top-20)        | 20 | 0.9808 | 0.9760 | 0.9423 | 0.9808 |
| conjectural (top-20) | 20 | 0.9808 | 0.9808 | 0.9808 | 0.9808 |

Mann-Whitney U one-tail (real > conjectural) on the two top-20 sets: U = 160.0, p = 9.824e-01. 
Real and conjectural surfaces are statistically indistinguishable in the right tail at the chosen top-K — the polluted pool's gate PASS is driven by phonotactic shape, not by underlying provenance.

## Distribution shift on real surfaces (clean Aquitanian → polluted Aquitanian)

Surfaces present in both rollups (real-provenance only): **153**.

| | mean posterior | median posterior | min | max |
|:--|---:|---:|---:|---:|
| clean Aquitanian   | 0.5033 | 0.5192 | 0.0125 | 0.9818 |
| polluted Aquitanian | 0.5086 | 0.5000 | 0.0192 | 0.9808 |

- **Mean Δ (polluted − clean):**   +0.0053
- **Median Δ:** +0.0192
- **Pos / neg counts:** +80 / −69 / =0: 4

Top-10 surfaces by absolute posterior shift:

| surface | clean posterior | polluted posterior | Δ |
|---|---:|---:|---:|
| `egun` | 0.9808 | 0.0192 | -0.9615 |
| `oin` | 0.9808 | 0.0192 | -0.9615 |
| `ikusi` | 0.0189 | 0.9615 | +0.9427 |
| `anai` | 0.0175 | 0.9423 | +0.9248 |
| `hara` | 0.9231 | 0.0192 | -0.9038 |
| `bost` | 0.1132 | 0.9808 | +0.8676 |
| `begi` | 0.8462 | 0.0385 | -0.8077 |
| `haragi` | 0.0385 | 0.8462 | +0.8077 |
| `erori` | 0.7885 | 0.0192 | -0.7692 |
| `gau` | 0.7885 | 0.0192 | -0.7692 |

## Notes

- This file is a v14-specific summary on top of `results/rollup.bayesian_posterior.polluted_aquitanian.md`. Re-run with `python3 scripts/v14_polluted_provenance_analysis.py` after any change that affects the bayesian rollup.
- The provenance map is read from `pools/polluted_aquitanian.yaml` directly — every entry has a `provenance` field (`real` or `conjectural`).
- Metric: `external_phoneme_perplexity_v0`. Top-K: 20. n_min: 10. No randomness in this script.

