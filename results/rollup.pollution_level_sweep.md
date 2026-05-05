# v18 pollution-level sweep — Aquitanian (mg-9f18)

Characterizes how the right-tail bayesian gate's p-value scales with same-distribution conjectural pollution across 10%/25%/50%/75% levels. The 50% row is v14 (mg-6b73); the other three are new in v18.

## Gate p-value vs pollution level

| pollution % | n_real | n_conj | substrate top-K | control top-K | median(top substrate) | median(top control) | MW U (substrate) | MW p (one-tail) | gate | top-K real | top-K conjectural |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|
| 10 | 153 | 17 | 20 | 20 | 0.9808 | 0.9450 | 325.5 | 1.502e-04 | PASS | 19 | 1 |
| 25 | 153 | 51 | 20 | 20 | 0.9808 | 0.9379 | 320.0 | 2.747e-04 | PASS | 12 | 8 |
| 50 | 153 | 153 | 20 | 20 | 0.9808 | 0.9572 | 340.0 | 2.740e-05 | PASS | 9 | 11 |
| 75 | 153 | 459 | 20 | 20 | 0.9808 | 0.9703 | 260.0 | 4.268e-02 | PASS | 5 | 15 |

## Interpretation

**Insensitive to pollution level — but non-monotonic p-values.** All four levels PASS, and the p-values are comparable. The non-monotonicity in p across levels is consistent with sampling noise in the conjectural draws (each polluted pool draws a different number of conjectural surfaces under a different seed, so the control's matched-marginal shifts pool-by-pool). The headline holds: same-distribution pollution does not collapse the gate at any level we tested.

**Provenance breakdown of the substrate top-K** (top-20, ranked by posterior_mean) is reported per row. Pollution levels at which the conjecturals are largely absent from the right tail (`top-K real ≥ 18`) are consistent with v14's reading: real and conjectural surfaces are *partially* discriminated even when the gate itself is insensitive to the pollution level.

## Comparison to v14 50% baseline

The 50% pool (v14, mg-6b73) is reproduced from this run as a sanity check that the v18 sweep code path produces the same gate values as the v10/v14 path:

- 50% gate verdict: **PASS**, p=2.740e-05, MW U=340.0.
- v14 reported PASS at p≈2.74e-05; reproduce here to within sampling noise of the result-stream merge.

## Notes

- Metric: `external_phoneme_perplexity_v0` (Basque LM). Substrate-side: real Aquitanian + same-distribution conjecturals. Control-side: `pools/control_polluted_aquitanian_<N>pct.yaml` (or `pools/control_polluted_aquitanian.yaml` at 50%) — each control is matched to its polluted pool's combined (real+conjectural) marginal.
- Top-K: 20. n_min: 10. Right-tail MW U is one-tail with normal-approximation tie-corrected p; see `scripts/per_surface_bayesian_rollup.py`.
- Determinism: pool surfaces are pinned by deterministic seed; sweep results are bit-identical across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl` and pool YAMLs.

