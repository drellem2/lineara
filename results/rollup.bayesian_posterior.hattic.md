# Hattic specificity probe — pre-registered right-tail bayesian gate (mg-7b882)

**Verdict against the pre-registered criterion: FAIL** — `hattic` (n=72 pool entries, below the v21 bar of 80) vs `control_hattic_bigram`, one-tailed MW p=3.931e-01; median top-20 posterior 0.8750 vs 0.8697 (gap +0.0053). Per the pre-registered interpretation rules this FAIL is **inconclusive on data quality** (hand-keyed, uncollated lexical forms; 72 < 80 entries), not evidence that the gate's signal is substrate-specific.

## Pre-registered criterion

Top-20 `hattic` posteriors vs top-20 `control_hattic_bigram` posteriors, both under the `hattic` LM; one-tailed Mann-Whitney U (substrate > control); PASS iff p < 0.05 and median(substrate) > median(control). Fixed in this script's docstring in the branch's first commit, before any run output.

## Acceptance gate

| substrate pool | pool entries | control pool | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | median gap | MW U | MW p (one-tail) | gate |
|:--|---:|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| hattic | 72 | control_hattic_bigram | 20 | 20 | 0.8750 | 0.8697 | +0.0053 | 210.5 | 3.931e-01 | FAIL |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.8695. Mean of top-20 control posterior_mean: 0.8423. Gap: +0.0271. Not part of the gate.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `katah` | 50 | 50 | 0.9808 | `pil` | 67 | 67 | 0.9855 |
| 2 | `katapa` | 24 | 24 | 0.9615 | `taha` | 67 | 67 | 0.9855 |
| 3 | `halentu` | 13 | 13 | 0.9333 | `hal` | 59 | 59 | 0.9836 |
| 4 | `hapalki` | 13 | 13 | 0.9333 | `hhanka` | 56 | 56 | 0.9828 |
| 5 | `katahha` | 13 | 13 | 0.9333 | `zap` | 24 | 24 | 0.9615 |
| 6 | `tahurpa` | 13 | 13 | 0.9333 | `kinanaat` | 10 | 10 | 0.9167 |
| 7 | `tawiniya` | 8 | 8 | 0.9000 | `haka` | 19 | 18 | 0.9048 |
| 8 | `tuhtasul` | 8 | 8 | 0.9000 | `lina` | 80 | 73 | 0.9024 |
| 9 | `hapantali` | 6 | 6 | 0.8750 | `wuina` | 8 | 8 | 0.9000 |
| 10 | `tastenuwa` | 6 | 6 | 0.8750 | `elist` | 32 | 29 | 0.8824 |
| 11 | `teteshapi` | 6 | 6 | 0.8750 | `ztitepi` | 5 | 5 | 0.8571 |
| 12 | `lihzina` | 13 | 12 | 0.8667 | `hipannuili` | 15 | 13 | 0.8235 |
| 13 | `il` | 50 | 44 | 0.8654 | `kanewahal` | 3 | 3 | 0.8000 |
| 14 | `katte` | 50 | 43 | 0.8462 | `wari` | 78 | 63 | 0.8000 |
| 15 | `ashap` | 50 | 42 | 0.8269 | `watarusuw` | 3 | 3 | 0.8000 |
| 16 | `hanhana` | 13 | 11 | 0.8000 | `watulal` | 2 | 2 | 0.7500 |
| 17 | `hatepinu` | 8 | 7 | 0.8000 | `ikatarpal` | 1 | 1 | 0.6667 |
| 18 | `tuhkanti` | 8 | 7 | 0.8000 | `linast` | 1 | 1 | 0.6667 |
| 19 | `tawananna` | 6 | 5 | 0.7500 | `tapas` | 139 | 90 | 0.6454 |
| 20 | `kastama` | 13 | 10 | 0.7333 | `hkast` | 36 | 23 | 0.6316 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `pil` | 67 | 67 | 0.9855 | 1.000 | 0.9855 |
| 2 | control | `taha` | 67 | 67 | 0.9855 | 1.000 | 0.9855 |
| 3 | control | `hal` | 59 | 59 | 0.9836 | 1.000 | 0.9836 |
| 4 | control | `hhanka` | 56 | 56 | 0.9828 | 1.000 | 0.9828 |
| 5 | substrate | `katah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `katapa` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 7 | control | `zap` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 8 | substrate | `halentu` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 9 | substrate | `hapalki` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 10 | substrate | `katahha` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 11 | substrate | `tahurpa` | 13 | 13 | 0.9333 | 1.000 | 0.9333 |
| 12 | control | `kinanaat` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 13 | control | `haka` | 19 | 18 | 0.9048 | 1.000 | 0.9048 |
| 14 | control | `lina` | 80 | 73 | 0.9024 | 1.000 | 0.9024 |
| 15 | control | `elist` | 32 | 29 | 0.8824 | 1.000 | 0.8824 |
| 16 | substrate | `lihzina` | 13 | 12 | 0.8667 | 1.000 | 0.8667 |
| 17 | substrate | `il` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 18 | substrate | `katte` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 19 | substrate | `ashap` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 20 | control | `hipannuili` | 15 | 13 | 0.8235 | 1.000 | 0.8235 |
| 21 | substrate | `tawiniya` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 22 | substrate | `tuhtasul` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 23 | control | `wuina` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 24 | substrate | `hanhana` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 25 | control | `wari` | 78 | 63 | 0.8000 | 1.000 | 0.8000 |
| 26 | substrate | `hatepinu` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 27 | substrate | `tuhkanti` | 8 | 7 | 0.8000 | 0.800 | 0.7400 |
| 28 | substrate | `kastama` | 13 | 10 | 0.7333 | 1.000 | 0.7333 |
| 29 | substrate | `hapantali` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 30 | substrate | `tastenuwa` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 31 | substrate | `teteshapi` | 6 | 6 | 0.8750 | 0.600 | 0.7250 |
| 32 | substrate | `kait` | 50 | 35 | 0.6923 | 1.000 | 0.6923 |
| 33 | control | `ztitepi` | 5 | 5 | 0.8571 | 0.500 | 0.6786 |
| 34 | substrate | `wintu` | 50 | 34 | 0.6731 | 1.000 | 0.6731 |
| 35 | substrate | `hilamar` | 13 | 9 | 0.6667 | 1.000 | 0.6667 |
| 36 | substrate | `hattus` | 24 | 16 | 0.6538 | 1.000 | 0.6538 |
| 37 | substrate | `zalpa` | 50 | 33 | 0.6538 | 1.000 | 0.6538 |
| 38 | substrate | `tawananna` | 6 | 5 | 0.7500 | 0.600 | 0.6500 |
| 39 | control | `tapas` | 139 | 90 | 0.6454 | 1.000 | 0.6454 |
| 40 | substrate | `lewae` | 50 | 32 | 0.6346 | 1.000 | 0.6346 |
| 41 | control | `hkast` | 36 | 23 | 0.6316 | 1.000 | 0.6316 |
| 42 | substrate | `an` | 50 | 31 | 0.6154 | 1.000 | 0.6154 |
| 43 | control | `pinun` | 28 | 17 | 0.6000 | 1.000 | 0.6000 |
| 44 | control | `kanewahal` | 3 | 3 | 0.8000 | 0.300 | 0.5900 |
| 45 | control | `watarusuw` | 3 | 3 | 0.8000 | 0.300 | 0.5900 |
| 46 | substrate | `telipinu` | 8 | 5 | 0.6000 | 0.800 | 0.5800 |
| 47 | substrate | `alep` | 50 | 29 | 0.5769 | 1.000 | 0.5769 |
| 48 | substrate | `washap` | 24 | 14 | 0.5769 | 1.000 | 0.5769 |
| 49 | substrate | `halmasuit` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |
| 50 | substrate | `hanwasuit` | 6 | 4 | 0.6250 | 0.600 | 0.5750 |

## Interpretation rules (fixed before the run)

- **Pool size.** 72 entries, below the v21 bar of 80; not padded.
- **Circularity.** The `hattic` LM is trained on the same 72 lexical citation forms that make up the pool. The own-LM readout in the cross-LM matrix is inflated by construction and is not evidence. This gate is less exposed, because `control_hattic_bigram` is sampled from the same bigram statistics and is scored under the same LM; that is a mitigation, not immunity.
- **Collation.** Forms are hand-keyed and not collated against Soysal 2004 / the printed editions (`corpora/hattic.README.md`). A PASS supports generic structure regardless; a FAIL is inconclusive on data quality.

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (α=1.0, 72 lexical forms; `harness/external_phoneme_models/hattic.json`).
- Gate: top-20 by posterior_mean only (credibility n_min=10 shown in the leaderboard, not used by the gate).
- Determinism: no RNG; re-runs are byte-identical given the same result-stream sidecars, manifests and pool YAMLs.

