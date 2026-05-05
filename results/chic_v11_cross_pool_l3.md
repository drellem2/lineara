# CHIC chic-v5 tier-2 candidates: cross-pool L3 robustness check (chic-v11; mg-d69c)

## Method

For each of the 3 chic-v5 tier-2 candidates (`#001 -> wa`/glide, `#012 -> wa`/glide, `#032 -> ki`/stop), the chic-v5 L3 substrate-consistency line is recomputed under EACH of the 4 substrate pools' LMs. The L3 machinery is byte-identical to chic-v5's: candidate-value pool rebuilt from chic-v2 anchor LB-carryover values + bare vowels (filtered to values whose first character is in the substrate pool's phoneme inventory, chic-v5 convention), each candidate scored via paired_diff against a deterministic class-disjoint control under the substrate pool's LM, per-class mean paired_diff picks the winning class. The only thing changing across the 12 cells is the (pool, LM) dispatch.

## Pool-LM dispatch table

| substrate pool | LM file | candidate-pool size | candidate-pool classes |
|---|---|---:|---|
| aquitanian | `harness/external_phoneme_models/basque.json` | 21 | glide, liquid, nasal, stop, vowel |
| etruscan | `harness/external_phoneme_models/etruscan.json` | 18 | liquid, nasal, stop, vowel |
| toponym | `harness/external_phoneme_models/basque.json` | 19 | liquid, nasal, stop, vowel |
| eteocretan | `harness/external_phoneme_models/eteocretan.json` | 20 | glide, liquid, nasal, stop, vowel |

Per-pool candidate-value pool composition (each pool's filter differs because the substrate-pool phoneme inventories differ):

- **aquitanian** (21 values): `a` `de` `e` `i` `ja` `je` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **etruscan** (18 values): `a` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **toponym** (19 values): `a` `de` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u`
- **eteocretan** (20 values): `a` `de` `e` `i` `ke` `ki` `ma` `me` `mu` `ni` `o` `pa` `ra` `ro` `ta` `te` `ti` `to` `u` `wa`

## Acceptance bands (per chic-v11 brief)

- 4 of 4 LMs agree on the same phoneme class for a candidate -> L3 vote is **LM-robust**.
- 3 of 4 agree -> **mostly robust**; flag the dissenting LM.
- 2 of 4 -> **weak agreement**; the L3 vote is partly LM-specific.
- <=1 of 4 -> L3 vote is an **LM artifact**.

## Per-candidate cross-pool L3 verdict

Each row is one (candidate, pool) cell. The `winning class` column is the L3 vote under that pool's LM (per-class mean paired_diff argmax over the rebuilt candidate-value pool). Mean paired_diff columns show the per-class aggregate; — for a class indicates the class is empty in the rebuilt candidate pool for that substrate.

### Candidate `#001` (chic-v5 proposed class: glide; chic-v5 best value: `wa`)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | stop | `ta` | +0.000279 | +0.000190 | +0.000279 | -0.000132 | -0.001015 | — | -0.000435 |
| etruscan | `etruscan.json` | stop | `ta` | +0.001077 | -0.001599 | +0.001077 | +0.000420 | -0.001862 | — | — |
| toponym | `basque.json` | stop | `ta` | +0.000402 | +0.000190 | +0.000402 | +0.000322 | -0.001015 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.002212 | -0.000429 | +0.000218 | +0.000626 | -0.002077 | — | +0.002212 |

**Cross-pool verdict for `#001`**: top class = `stop` (3/4 pools); votes = stop:3, glide:1; mostly LM-robust (3 of 4 agree); **disagrees with chic-v5 proposed class** (`glide`).

Dissenting pool(s): eteocretan.

### Candidate `#012` (chic-v5 proposed class: glide; chic-v5 best value: `wa`)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | nasal | `me` | +0.001893 | -0.003243 | +0.001502 | +0.001893 | -0.003349 | — | -0.000898 |
| etruscan | `etruscan.json` | stop | `te` | +0.007672 | -0.011432 | +0.007672 | +0.003537 | -0.007999 | — | — |
| toponym | `basque.json` | stop | `de` | +0.002285 | -0.003562 | +0.002285 | +0.001893 | -0.003349 | — | — |
| eteocretan | `eteocretan.json` | glide | `wa` | +0.005331 | -0.005831 | +0.000995 | +0.003529 | -0.004316 | — | +0.005331 |

**Cross-pool verdict for `#012`**: top class = `stop` (2/4 pools); votes = stop:2, glide:1, nasal:1; weak agreement (2 of 4); **disagrees with chic-v5 proposed class** (`glide`).

Dissenting pool(s): aquitanian, eteocretan.

### Candidate `#032` (chic-v5 proposed class: stop; chic-v5 best value: `ki`)

| pool | LM | winning class | winning value | winning paired_diff | mean(vowel) | mean(stop) | mean(nasal) | mean(liquid) | mean(fricative) | mean(glide) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aquitanian | `basque.json` | glide | `ja` | +0.004302 | -0.006965 | +0.001846 | +0.001178 | -0.009504 | — | +0.004302 |
| etruscan | `etruscan.json` | stop | `ti` | +0.010569 | -0.014481 | +0.010569 | +0.004253 | -0.000644 | — | — |
| toponym | `basque.json` | nasal | `me` | +0.003171 | -0.006965 | +0.001936 | +0.003171 | -0.009504 | — | — |
| eteocretan | `eteocretan.json` | stop | `ki` | +0.004579 | -0.005642 | +0.004579 | +0.002986 | -0.012112 | — | -0.001315 |

**Cross-pool verdict for `#032`**: top class = `stop` (2/4 pools); votes = stop:2, glide:1, nasal:1; weak agreement (2 of 4); **agrees with chic-v5 proposed class** (`stop`).

Dissenting pool(s): aquitanian, toponym.

## Cross-candidate cross-pool summary

| candidate | chic-v5 class | top cross-pool class | vote split | verdict | agrees with chic-v5 |
|---|---|---|---|---|:---:|
| `#001` | glide | stop (3/4) | stop=3 / glide=1 | mostly LM-robust (3 of 4 agree) | ✗ |
| `#012` | glide | stop (2/4) | stop=2 / glide=1 / nasal=1 | weak agreement (2 of 4) | ✗ |
| `#032` | stop | stop (2/4) | stop=2 / glide=1 / nasal=1 | weak agreement (2 of 4) | ✓ |

## Discipline notes

- **L3 robustness is a partial defence, not a positive validation.** If all 4 LMs agree, the L3 vote is robust to LM choice — but L3 itself recovers known anchor classes at 5% under chic-v9's leave-one-out test (below the ~16.7% chance baseline for the 6-class taxonomy), and the chic-v9 verdict that chic-v5's framework operates in the low-agreement / not-validated band stands. Cross-pool L3 robustness adds confidence that the L3 axis itself is not an LM-specific artifact for that candidate; it does not raise the framework's validation accuracy.
- **Per-pool candidate-value pools differ.** When a substrate pool's phoneme inventory excludes a candidate value's onset char, that value drops from the per-pool pool, and the class loses its representative if no other candidate of the same class survives. Per-class mean paired_diff is computed only over surviving candidates; columns with `—` mean the class is empty under that pool's filter and L3 cannot vote for it by construction.
- **The chic-v9 framework-level negative is unaffected.** chic-v11 is an axis-restricted re-test of L3 only; L1+L2 (distributional fingerprint) are not re-run. Even an all-4-pools-agree L3 verdict here does not lift the framework's chic-v9 LOO accuracy from 20.0% / 0/3 tier-2 correct.

## Determinism

- No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-keyed permutation construction.
- Same (CHIC syllabographic stream, chic-v2 anchor mapping, substrate-pool yamls, LM artifacts) -> byte-identical output.

## Build provenance

- Generated by `scripts/build_chic_v11.py` (mg-d69c).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs: `corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); `pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; `harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* Amsterdam: J. C. Gieben.
- Trask, R. L. (1997). *The History of Basque.* London: Routledge.
- Bonfante, G. & Bonfante, L. (2002). *The Etruscan Language: An Introduction* (revised ed.). Manchester / New York.
- Beekes, R. S. P. (2010). *Etymological Dictionary of Greek*, vol. 2 appendix on Pre-Greek substrate. Leiden: Brill.
