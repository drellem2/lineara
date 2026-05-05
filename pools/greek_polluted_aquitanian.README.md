# greek_polluted_aquitanian — DELIBERATELY POLLUTED TEST POOL

> ⚠️ **This pool is a test artifact, not a research claim.** Half of its 306 entries are real aquitanian substrate roots; the other half are synthetic conjectural surfaces drawn from a *different* language's char-bigram distribution (`harness/external_phoneme_models/mycenaean_greek.json`), with lengths matched to the real aquitanian pool. Do **NOT** use this pool to make substrate claims, build derived dictionaries, or train downstream models. It exists solely for the harness v15 / mg-7ecb cross-language pollution test: does the framework PASS for ANY phonotactic match, or only when the polluting distribution matches the substrate's own?

## Why this pool exists

v14 (mg-6b73) found that the right-tail bayesian gate on the clean `aquitanian` pool **PASSes** even when 50% of the pool is conjectural — *provided the conjecturals are drawn from the substrate's own phoneme + length distribution.* The polecat's manuscript-shape claim distilled from v14:

> The framework detects substrate-LM-phonotactic kinship at the population level for **any pool whose phoneme + length distribution is drawn from the substrate's own marginal distribution.** It does NOT detect 'real substrate vocabulary,' and does NOT support per-sign reading claims.

That claim's validity hinges on the *'drawn from the substrate's own marginal distribution'* clause. v15 tests it by **deliberately violating** that clause: conjecturals are drawn from a Mycenaean-Greek char-bigram model (`harness/external_phoneme_models/mycenaean_greek.json`) instead. The binary outcome:

- **Cross-language polluted pool PASSes** under the substrate's own LM → the framework's PASS signal is essentially trivial; any phonotactic-shape overlap with the LM produces a PASS, regardless of distribution-shape match.
- **Cross-language polluted pool FAILS** under the substrate's own LM → the framework's PASS has real selectivity to substrate-distribution shape; v14's PASS-on-same-distribution-pollution holds because the conjecturals shared aquitanian shape, and the v14 manuscript-shape claim stands as written.

## Construction algorithm

1. **Real half.** All 153 entries from `pools/aquitanian.yaml` are carried over verbatim (surface, phonemes, gloss, semantic_field, region, attestations, citation) and tagged `provenance: real`.
2. **Conjectural half.** 153 synthetic entries are drawn from the external char-bigram LM at `harness/external_phoneme_models/mycenaean_greek.json` under the following sampling procedure:
   - **Length:** same as the i-th real entry, so the polluted pool's length distribution is exactly 2× the real pool's. Length is **not** a confound between provenances.
   - **First character:** sampled from the LM's unigram-marginal restricted to the alphabet a..z (the `<W>` boundary token and the space character are filtered out so the word starts with a content character). Weights = `unigram_count + alpha`.
   - **Subsequent characters:** sampled conditional on the previous character via the bigram counts `count(prev, c) + alpha`, again restricted to a..z so the word never produces an early word-end. The relative frequencies of alphabet bigrams are preserved; the `<W>`/space boundary tokens are excluded at every step (this is the *'regenerate to match length'* interpretation of the brief).
   - **Phonemes:** each sampled character becomes a single-character phoneme. This matches how the v8 metric (`external_phoneme_perplexity_v0`) decomposes phonemes to chars at scoring time.
   - **Region tag:** `region: aquitania` (same as real entries — the conjecturals are deliberately indistinguishable from real ones to the candidate generator's source_pool routing).
   - **Provenance tag:** `provenance: conjectural_greek` (so the rollup post-processing can compute the per-provenance breakdown of the top-20).
   - **No semantic_field, no gloss.** Conjecturals have no real-world semantics.
3. **Uniqueness.** Conjectural surfaces are forced unique against (a) the real pool's surfaces and (b) prior conjecturals. Collisions trigger redraws up to 50 times, then a deterministic seed bump — the output stays reproducible.
4. **Phoneme-class filter.** Every conjectural entry must span at least two distinct phoneme classes (V/S/C); single-class draws are redrawn so the candidate generator does not skip any conjectural entry.
5. **Determinism.** Seed = `0xfa0fd94c61e71b23` (`sha256("greek_polluted_aquitanian:conjectural")[:16]`). Re-running the builder produces a byte-identical YAML. Asserted by `harness/tests/test_polluted_pool.py`.

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

The conjectural draw uses the **harness/external_phoneme_models/mycenaean_greek.json** char-bigram distribution, NOT the real pool's. The polluted pool's overall histogram is therefore the union of the real pool's marginal distribution and the source LM's alphabet-restricted bigram-derived marginal, which can differ substantially. Realized counts are exact for the realized 153 conjectural draws.

| phoneme | real pool count | real pool % | polluted pool count | polluted pool % |
|---|---:|---:|---:|---:|
| `a` | 88 | 13.6% | 172 | 13.3% |
| `b` | 25 | 3.9% | 25 | 1.9% |
| `c` | 4 | 0.6% | 4 | 0.3% |
| `d` | 13 | 2.0% | 27 | 2.1% |
| `e` | 69 | 10.7% | 151 | 11.7% |
| `f` | 0 | 0.0% | 1 | 0.1% |
| `g` | 19 | 2.9% | 19 | 1.5% |
| `h` | 37 | 5.7% | 37 | 2.9% |
| `i` | 81 | 12.5% | 143 | 11.1% |
| `j` | 1 | 0.2% | 36 | 2.8% |
| `k` | 9 | 1.4% | 37 | 2.9% |
| `l` | 26 | 4.0% | 26 | 2.0% |
| `m` | 11 | 1.7% | 27 | 2.1% |
| `n` | 38 | 5.9% | 71 | 5.5% |
| `o` | 38 | 5.9% | 122 | 9.4% |
| `p` | 1 | 0.2% | 24 | 1.9% |
| `q` | 0 | 0.0% | 14 | 1.1% |
| `r` | 68 | 10.5% | 124 | 9.6% |
| `s` | 24 | 3.7% | 36 | 2.8% |
| `t` | 16 | 2.5% | 57 | 4.4% |
| `ts` | 2 | 0.3% | 2 | 0.2% |
| `tx` | 4 | 0.6% | 4 | 0.3% |
| `tz` | 11 | 1.7% | 11 | 0.9% |
| `u` | 37 | 5.7% | 60 | 4.6% |
| `v` | 0 | 0.0% | 1 | 0.1% |
| `w` | 0 | 0.0% | 35 | 2.7% |
| `x` | 1 | 0.2% | 1 | 0.1% |
| `z` | 23 | 3.6% | 25 | 1.9% |

## What this pool is and is not

- **IS:** A test fixture for the framework's distribution-shape selectivity (mg-7ecb cross-language pollution test).
- **IS NOT:** A research claim. Conjectural surfaces are synthetic. Do not cite, do not gloss, do not derive secondary artifacts.
- **IS NOT:** A replacement for `pools/aquitanian.yaml`. The clean substrate pool remains the substrate-claim pool; this polluted pool is parallel scaffolding.
- **Matched control:** `pools/control_greek_polluted_aquitanian.yaml`, built by `scripts/build_control_pools.py`. Length and phoneme-inventory matched to the polluted pool's *combined* (real + cross-language-conjectural) distribution, drawn under a distinct seed.
