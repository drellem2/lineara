# polluted_aquitanian_25pct — DELIBERATELY POLLUTED TEST POOL

> ⚠️ **This pool is a test artifact, not a research claim.** Of its 204 entries, 153 are real aquitanian substrate roots and 51 are deliberately-conjectural surfaces tagged as if they were real (≈25% conjectural; target 25%). Do **NOT** use this pool to make substrate claims, build derived dictionaries, or train downstream models. It exists solely for the harness v18 / mg-9f18 pollution-level sweep, which characterizes how the right-tail bayesian gate's p-value scales with curation noise across 10%/25%/50%/75% conjectural pollution.

## Why this pool exists

v14 (mg-6b73) found that the right-tail bayesian gate on the clean `aquitanian` pool **PASSes** at the same v10-magnitude p-value even when 50% of the pool is conjectural-same-distribution. The polecat noted that this leaves an open question: is the gate essentially insensitive to pollution within the substrate's phonotactic distribution, or is there a sharp threshold (e.g. ≥90% conjectural) at which the gate finally fails? v18 (mg-9f18) characterizes the gate's sensitivity gradient by sweeping the conjectural ratio across 10%, 25%, and 75% same-distribution pollution. This pool is the **25% / target 25%** variant; the 50% pool is `pools/polluted_aquitanian.yaml`.

The full sweep table lands in `results/rollup.pollution_level_sweep.md`.

## Construction algorithm

1. **Real half.** All 153 entries from `pools/aquitanian.yaml` are carried over verbatim (surface, phonemes, gloss, semantic_field, region, attestations, citation) and tagged `provenance: real`.
2. **Conjectural half.** 51 synthetic entries are drawn under the same algorithm as `scripts/build_control_pools.py`:
   - Length: matches `real[i mod 153]` under cyclic indexing, so the realized length distribution preserves the real pool's distribution in expectation (and is exact when `n_conjectural` is a multiple of `n_real`).
   - Phonemes: sampled with replacement from the real pool's marginal phoneme-frequency histogram.
   - Surface: concatenation of sampled phonemes.
   - **Region tag:** `region: aquitania` (so the conjectural entries are indistinguishable from real ones to the candidate generator's source_pool routing — the test asks whether the framework can detect the conjecturals despite that camouflage).
   - **Provenance tag:** `provenance: conjectural` (so the rollup post-processing can compute the provenance breakdown of the top-20).
   - **No semantic_field.** Conjecturals have no real-world semantics; the field is omitted entirely (treated as null by the geographic_genre_fit_v1 metric, which falls back to neutral 0.5 — irrelevant for the v8 metric this pool is actually scored under).
3. **Uniqueness.** Conjectural surfaces are forced unique against (a) the real pool's surfaces and (b) prior conjecturals. Collisions trigger redraws up to 50 times, then a deterministic seed bump — the output stays reproducible.
4. **Phoneme-class filter.** Every conjectural entry must span at least two distinct phoneme classes (V/S/C); single-class draws are redrawn so the candidate generator does not skip any conjectural entry.
5. **Determinism.** Seed = `0x7b1a9f706d18b6c0` (sha256("polluted_aquitanian_25pct:conjectural")[:16]). Re-running the builder produces a byte-identical YAML. Asserted by `harness/tests/test_polluted_pool.py`.

## Pool counts

- Real entries:         **153**
- Conjectural entries:  **51**
- Total entries:        **204**

## Length distribution

Real and conjectural entries share length under cyclic indexing (`conjectural[i].length = real[i mod 153].length`). The polluted pool's length distribution preserves the real pool's distribution in expectation; it is exact when `n_conjectural` is a multiple of `n_real` (e.g. 75% pollution = 3× real_n). Length is **not** a confound between the real and conjectural halves.

| length | real pool | polluted pool |
|---:|---:|---:|
| 2 | 5 | 6 |
| 3 | 32 | 40 |
| 4 | 60 | 79 |
| 5 | 40 | 56 |
| 6 | 12 | 18 |
| 7 | 4 | 5 |

## Phoneme inventory and frequency

The conjectural draw uses the real pool's marginal phoneme frequency, so the polluted pool's overall histogram should track ~1.33× (real + 0.33×conjectural) the real pool's in expectation. Realized counts are approximate due to finite sample size.

| phoneme | real pool count | real pool % | polluted pool count | polluted pool % |
|---|---:|---:|---:|---:|
| `a` | 88 | 13.6% | 123 | 14.1% |
| `b` | 25 | 3.9% | 30 | 3.4% |
| `c` | 4 | 0.6% | 4 | 0.5% |
| `d` | 13 | 2.0% | 18 | 2.1% |
| `e` | 69 | 10.7% | 95 | 10.9% |
| `g` | 19 | 2.9% | 25 | 2.9% |
| `h` | 37 | 5.7% | 48 | 5.5% |
| `i` | 81 | 12.5% | 111 | 12.7% |
| `j` | 1 | 0.2% | 2 | 0.2% |
| `k` | 9 | 1.4% | 13 | 1.5% |
| `l` | 26 | 4.0% | 39 | 4.5% |
| `m` | 11 | 1.7% | 13 | 1.5% |
| `n` | 38 | 5.9% | 48 | 5.5% |
| `o` | 38 | 5.9% | 48 | 5.5% |
| `p` | 1 | 0.2% | 1 | 0.1% |
| `r` | 68 | 10.5% | 90 | 10.3% |
| `s` | 24 | 3.7% | 31 | 3.6% |
| `t` | 16 | 2.5% | 25 | 2.9% |
| `ts` | 2 | 0.3% | 2 | 0.2% |
| `tx` | 4 | 0.6% | 4 | 0.5% |
| `tz` | 11 | 1.7% | 15 | 1.7% |
| `u` | 37 | 5.7% | 50 | 5.7% |
| `x` | 1 | 0.2% | 2 | 0.2% |
| `z` | 23 | 3.6% | 34 | 3.9% |

## What this pool is and is not

- **IS:** A test fixture for the v18 pollution-level sweep (mg-9f18). Characterizes how the right-tail bayesian gate's p-value scales with curation noise; this is the 25%-conjectural variant.
- **IS NOT:** A research claim. Conjectural surfaces are synthetic. Do not cite, do not gloss, do not derive secondary artifacts.
- **IS NOT:** A replacement for `pools/aquitanian.yaml`. The clean substrate pool remains the substrate-claim pool; this polluted pool is parallel scaffolding.
- **Matched control:** `pools/control_polluted_aquitanian_25pct.yaml`, built by `scripts/build_control_pools.py`. Length and phoneme-inventory matched to the polluted pool, drawn under a distinct seed.
