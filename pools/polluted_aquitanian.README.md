# polluted_aquitanian — DELIBERATELY POLLUTED TEST POOL

> ⚠️ **This pool is a test artifact, not a research claim.** Half of its 306 entries are real aquitanian substrate roots; the other half are deliberately-conjectural surfaces tagged as if they were real. Do **NOT** use this pool to make substrate claims, build derived dictionaries, or train downstream models. It exists solely for the harness v14 / mg-6b73 held-out pool-curation test: does the v10 right-tail bayesian PASS on the clean `aquitanian` pool survive 50% conjectural pollution?

## Why this pool exists

v10 (mg-d26d) found that the per-surface bayesian posterior on the clean `aquitanian` pool clears the right-tail Mann-Whitney U gate against its phonotactic control. v12+v13 narrowed the interpretation of that PASS to two readings:

1. **Substrate-LM-phonotactic kinship.** The framework genuinely detects that real Aquitanian surfaces are more Basque-LM-likely than random Aquitanian-shaped surfaces — tolerant of mixed-cleanness pools.
2. **Curation-sensitivity.** The framework's PASS depends on the substrate pool being uniformly real; pollution by conjectural-but-phonotactically-matched surfaces would collapse the PASS.

This polluted pool is the binary discriminator for the two readings. See mg-6b73 for the full pre-registered analysis plan.

## Construction algorithm

1. **Real half.** All 153 entries from `pools/aquitanian.yaml` are carried over verbatim (surface, phonemes, gloss, semantic_field, region, attestations, citation) and tagged `provenance: real`.
2. **Conjectural half.** 153 synthetic entries are drawn under the same algorithm as `scripts/build_control_pools.py`:
   - Length: same length as the i-th real entry (so the length distribution doubles exactly).
   - Phonemes: sampled with replacement from the real pool's marginal phoneme-frequency histogram.
   - Surface: concatenation of sampled phonemes.
   - **Region tag:** `region: aquitania` (so the conjectural entries are indistinguishable from real ones to the candidate generator's source_pool routing — the test asks whether the framework can detect the conjecturals despite that camouflage).
   - **Provenance tag:** `provenance: conjectural` (so the rollup post-processing can compute the provenance breakdown of the top-20).
   - **No semantic_field.** Conjecturals have no real-world semantics; the field is omitted entirely (treated as null by the geographic_genre_fit_v1 metric, which falls back to neutral 0.5 — irrelevant for the v8 metric this pool is actually scored under).
3. **Uniqueness.** Conjectural surfaces are forced unique against (a) the real pool's surfaces and (b) prior conjecturals. Collisions trigger redraws up to 50 times, then a deterministic seed bump — the output stays reproducible.
4. **Phoneme-class filter.** Every conjectural entry must span at least two distinct phoneme classes (V/S/C); single-class draws are redrawn so the candidate generator does not skip any conjectural entry.
5. **Determinism.** Seed = `0xb4b7c1f037ead5f1` (sha256("polluted_aquitanian:conjectural")[:16]). Re-running the builder produces a byte-identical YAML. Asserted by `harness/tests/test_polluted_pool.py`.

## Pool counts

- Real entries:         **153**
- Conjectural entries:  **153**
- Total entries:        **306**

## Length distribution

Real and conjectural entries share length pairwise (i-th conjectural matches i-th real). The polluted pool's length distribution is exactly 2× the real pool's.

| length | real pool | polluted pool |
|---:|---:|---:|
| 2 | 5 | 10 |
| 3 | 32 | 64 |
| 4 | 60 | 120 |
| 5 | 40 | 80 |
| 6 | 12 | 24 |
| 7 | 4 | 8 |

## Phoneme inventory and frequency

The conjectural draw uses the real pool's marginal phoneme frequency, so the polluted pool's overall histogram should track ~2× the real pool's in expectation. Realized counts are approximate due to finite sample size.

| phoneme | real pool count | real pool % | polluted pool count | polluted pool % |
|---|---:|---:|---:|---:|
| `a` | 88 | 13.6% | 167 | 12.9% |
| `b` | 25 | 3.9% | 48 | 3.7% |
| `c` | 4 | 0.6% | 12 | 0.9% |
| `d` | 13 | 2.0% | 28 | 2.2% |
| `e` | 69 | 10.7% | 141 | 10.9% |
| `g` | 19 | 2.9% | 39 | 3.0% |
| `h` | 37 | 5.7% | 69 | 5.3% |
| `i` | 81 | 12.5% | 146 | 11.3% |
| `j` | 1 | 0.2% | 4 | 0.3% |
| `k` | 9 | 1.4% | 20 | 1.5% |
| `l` | 26 | 4.0% | 57 | 4.4% |
| `m` | 11 | 1.7% | 22 | 1.7% |
| `n` | 38 | 5.9% | 75 | 5.8% |
| `o` | 38 | 5.9% | 71 | 5.5% |
| `p` | 1 | 0.2% | 2 | 0.2% |
| `r` | 68 | 10.5% | 154 | 11.9% |
| `s` | 24 | 3.7% | 55 | 4.3% |
| `t` | 16 | 2.5% | 32 | 2.5% |
| `ts` | 2 | 0.3% | 4 | 0.3% |
| `tx` | 4 | 0.6% | 7 | 0.5% |
| `tz` | 11 | 1.7% | 17 | 1.3% |
| `u` | 37 | 5.7% | 70 | 5.4% |
| `x` | 1 | 0.2% | 1 | 0.1% |
| `z` | 23 | 3.6% | 51 | 3.9% |

## What this pool is and is not

- **IS:** A test fixture for the framework's curation-sensitivity. Half-conjectural by design.
- **IS NOT:** A research claim. Conjectural surfaces are synthetic. Do not cite, do not gloss, do not derive secondary artifacts.
- **IS NOT:** A replacement for `pools/aquitanian.yaml`. The clean Aquitanian pool remains the substrate-claim pool; this polluted pool is parallel scaffolding.
- **Matched control:** `pools/control_polluted_aquitanian.yaml`, built by `scripts/build_control_pools.py`. Length and phoneme-inventory matched to the polluted pool, drawn under a distinct seed.
