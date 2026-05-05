# v18 toponym pool — bigram-preserving control gate (mg-9f18)

**Headline: the toponym pool PASSes the v10 right-tail bayesian gate against the bigram-preserving control.** v10's toponym failure was a control-sampler artifact — the v6 unigram-marginal control produced phonotactically extreme surfaces (`eoao`, `aathei`, `kllzua`) that the Basque LM scored well by raw phoneme-frequency match. Replacing it with a bigram-preserving control tightens the gate enough that the substrate signal in real toponym roots clears the right-tail comparison. The toponym pool now joins Aquitanian + Etruscan as a third validated cross-LM-checkable substrate pool.

## Acceptance gate (v18 vs v10)

| variant | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|:--|---:|---:|---:|---:|---:|---:|:--:|
| bigram (v18) | 20 | 20 | 0.9615 | 0.8525 | 337.5 | 9.988e-05 | PASS |
| unigram (v6/v10) | 20 | 20 | 0.9186 | 0.9464 | 149.5 | 9.165e-01 | FAIL |

## Top-20 substrate vs top-20 control side-by-side (v18 bigram-preserving control)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `aksos` | 50 | 50 | 0.9808 | `lel` | 118 | 117 | 0.9833 |
| 2 | `aso` | 50 | 50 | 0.9808 | `ena` | 115 | 114 | 0.9829 |
| 3 | `assos` | 50 | 50 | 0.9808 | `ososoniena` | 12 | 12 | 0.9286 |
| 4 | `kno` | 50 | 50 | 0.9808 | `thelak` | 60 | 56 | 0.9194 |
| 5 | `lukia` | 50 | 50 | 0.9808 | `aiosontho` | 8 | 8 | 0.9000 |
| 6 | `tarra` | 50 | 50 | 0.9808 | `abeti` | 36 | 33 | 0.8947 |
| 7 | `ala` | 50 | 49 | 0.9615 | `akaintha` | 16 | 15 | 0.8889 |
| 8 | `iassos` | 24 | 24 | 0.9615 | `ain` | 6 | 6 | 0.8750 |
| 9 | `itanos` | 24 | 24 | 0.9615 | `ikialo` | 19 | 17 | 0.8571 |
| 10 | `keos` | 50 | 49 | 0.9615 | `terkks` | 33 | 29 | 0.8571 |
| 11 | `lebena` | 24 | 24 | 0.9615 | `inaletos` | 44 | 38 | 0.8478 |
| 12 | `naxos` | 24 | 24 | 0.9615 | `kukhun` | 24 | 21 | 0.8462 |
| 13 | `andos` | 50 | 48 | 0.9423 | `tar` | 111 | 94 | 0.8407 |
| 14 | `minoa` | 50 | 48 | 0.9423 | `arin` | 60 | 51 | 0.8387 |
| 15 | `kuzikos` | 13 | 13 | 0.9333 | `iebza` | 27 | 23 | 0.8276 |
| 16 | `mnos` | 50 | 46 | 0.9038 | `pales` | 130 | 106 | 0.8106 |
| 17 | `aspendos` | 8 | 8 | 0.9000 | `akuthe` | 7 | 6 | 0.7778 |
| 18 | `tenos` | 50 | 45 | 0.8846 | `ham` | 73 | 56 | 0.7600 |
| 19 | `aios` | 50 | 44 | 0.8654 | `likssssoumi` | 2 | 2 | 0.7500 |
| 20 | `lykabettos` | 5 | 5 | 0.8571 | `tak` | 10 | 8 | 0.7500 |

## Side-by-side: v6 unigram control top-20 (reproduced from mg-d26d for comparison)

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `dikte` | 50 | 50 | 0.9808 | `eoao` | 263 | 262 | 0.9925 |
| 2 | `keos` | 50 | 50 | 0.9808 | `aathei` | 78 | 78 | 0.9875 |
| 3 | `kno` | 50 | 50 | 0.9808 | `ana` | 117 | 116 | 0.9832 |
| 4 | `minoa` | 50 | 50 | 0.9808 | `eta` | 37 | 37 | 0.9744 |
| 5 | `tenos` | 50 | 50 | 0.9808 | `ioonaol` | 25 | 25 | 0.9630 |
| 6 | `iassos` | 24 | 24 | 0.9615 | `kolee` | 52 | 51 | 0.9630 |
| 7 | `lemnos` | 24 | 24 | 0.9615 | `kllzua` | 24 | 24 | 0.9615 |
| 8 | `kuzikos` | 13 | 13 | 0.9333 | `anealo` | 22 | 22 | 0.9583 |
| 9 | `melitos` | 13 | 13 | 0.9333 | `kim` | 42 | 41 | 0.9545 |
| 10 | `tulisos` | 13 | 13 | 0.9333 | `oaest` | 17 | 17 | 0.9474 |
| 11 | `melos` | 50 | 46 | 0.9038 | `saenaa` | 108 | 103 | 0.9455 |
| 12 | `aspendos` | 8 | 8 | 0.9000 | `aas` | 131 | 123 | 0.9323 |
| 13 | `kalumnos` | 8 | 8 | 0.9000 | `ala` | 831 | 769 | 0.9244 |
| 14 | `zakuntos` | 8 | 8 | 0.9000 | `oks` | 37 | 35 | 0.9231 |
| 15 | `lukia` | 50 | 45 | 0.8846 | `tea` | 155 | 143 | 0.9172 |
| 16 | `mukenai` | 13 | 12 | 0.8667 | `aasn` | 22 | 21 | 0.9167 |
| 17 | `lykabettos` | 5 | 5 | 0.8571 | `onn` | 9 | 9 | 0.9091 |
| 18 | `itanos` | 29 | 25 | 0.8387 | `aoe` | 8 | 8 | 0.9000 |
| 19 | `halikarnassos` | 4 | 4 | 0.8333 | `nul` | 101 | 91 | 0.8932 |
| 20 | `poikilassos` | 4 | 4 | 0.8333 | `eonun` | 7 | 7 | 0.8889 |

## Control top-K composition shift

Surfaces in the v6 unigram control top-K that are **absent** from the v18 bigram control top-K:

- `aas`
- `aasn`
- `aathei`
- `ala`
- `ana`
- `anealo`
- `aoe`
- `eoao`
- `eonun`
- `eta`
- `ioonaol`
- `kim`
- `kllzua`
- `kolee`
- `nul`
- `oaest`
- `oks`
- `onn`
- `saenaa`
- `tea`

Surfaces in the v18 bigram control top-K that are **new** (absent from the v6 unigram control top-K):

- `abeti`
- `ain`
- `aiosontho`
- `akaintha`
- `akuthe`
- `arin`
- `ena`
- `ham`
- `iebza`
- `ikialo`
- `inaletos`
- `kukhun`
- `lel`
- `likssssoumi`
- `ososoniena`
- `pales`
- `tak`
- `tar`
- `terkks`
- `thelak`

## Notes

- Metric: `external_phoneme_perplexity_v0` (Basque LM). Substrate pool: `toponym`. Bigram control: `control_toponym_bigram`. Unigram control: `control_toponym`.
- Top-K: 20. n_min: 10. Right-tail MW U is one-tail with normal-approximation tie-corrected p; see `scripts/per_surface_bayesian_rollup.py`.
- Determinism: identical rows + posterior + p across re-runs given the same `experiments.external_phoneme_perplexity_v0*.jsonl`, `hypotheses/auto/toponym.manifest.jsonl`, and `hypotheses/auto/{control_pool}.manifest.jsonl`. No RNG.

