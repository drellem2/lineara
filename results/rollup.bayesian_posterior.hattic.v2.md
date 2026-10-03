# Hattic specificity probe — pre-registered right-tail bayesian gate (mg-7b882; v2 re-run mg-a38bf)

**Verdict against the pre-registered criterion: PASS** — `hattic` (n=124 pool entries, above the v21 bar of 80) vs `control_hattic_bigram`, one-tailed MW p=4.220e-04; median top-20 posterior 0.9808 vs 0.9083 (gap +0.0724). Hattic is an unrelated Anatolian isolate run as a specificity probe: a PASS is evidence that the gate rewards generic natural-language structure (the v15 reading), not substrate affinity with Linear A.

## Pre-registered criterion

Top-20 `hattic` posteriors vs top-20 `control_hattic_bigram` posteriors, both under the `hattic` LM; one-tailed Mann-Whitney U (substrate > control); PASS iff p < 0.05 and median(substrate) > median(control). Fixed in this script's docstring in the branch's first commit, before any run output.

## Acceptance gate

| substrate pool | pool entries | control pool | substrate top-K | control top-K | median(top substrate posterior) | median(top control posterior) | median gap | MW U | MW p (one-tail) | gate |
|:--|---:|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| hattic | 124 | control_hattic_bigram | 20 | 20 | 0.9808 | 0.9083 | +0.0724 | 321.0 | 4.220e-04 | PASS |

## Mean-of-means (informational)

Mean of top-20 substrate posterior_mean: 0.9700. Mean of top-20 control posterior_mean: 0.9156. Gap: +0.0544. Not part of the gate.

## Top-20 substrate vs top-20 control side-by-side

| rank | substrate surface | n_s | k_s | posterior_s | control surface | n_c | k_c | posterior_c |
|---:|:--|---:|---:|---:|:--|---:|---:|---:|
| 1 | `asah` | 50 | 50 | 0.9808 | `tah` | 139 | 138 | 0.9858 |
| 2 | `estan` | 50 | 50 | 0.9808 | `halipil` | 52 | 52 | 0.9815 |
| 3 | `katah` | 50 | 50 | 0.9808 | `tar` | 50 | 50 | 0.9808 |
| 4 | `kun` | 50 | 50 | 0.9808 | `laras` | 120 | 118 | 0.9754 |
| 5 | `pala` | 50 | 50 | 0.9808 | `lin` | 51 | 50 | 0.9623 |
| 6 | `pu` | 50 | 50 | 0.9808 | `lepstt` | 24 | 24 | 0.9615 |
| 7 | `put` | 50 | 50 | 0.9808 | `tuti` | 49 | 48 | 0.9608 |
| 8 | `sa` | 50 | 50 | 0.9808 | `tassantu` | 18 | 18 | 0.9500 |
| 9 | `sahis` | 50 | 50 | 0.9808 | `hapi` | 107 | 99 | 0.9174 |
| 10 | `sul` | 50 | 50 | 0.9808 | `stul` | 10 | 10 | 0.9167 |
| 11 | `tahil` | 50 | 50 | 0.9808 | `hini` | 8 | 8 | 0.9000 |
| 12 | `tu` | 50 | 50 | 0.9808 | `tanttuha` | 8 | 8 | 0.9000 |
| 13 | `zia` | 50 | 50 | 0.9808 | `eshahi` | 7 | 7 | 0.8889 |
| 14 | `kasuh` | 50 | 49 | 0.9615 | `hileh` | 23 | 21 | 0.8800 |
| 15 | `katte` | 50 | 49 | 0.9615 | `inelanasi` | 6 | 6 | 0.8750 |
| 16 | `kut` | 50 | 49 | 0.9615 | `pipsakasu` | 6 | 6 | 0.8750 |
| 17 | `tahaia` | 24 | 24 | 0.9615 | `zehah` | 60 | 53 | 0.8710 |
| 18 | `taru` | 50 | 49 | 0.9615 | `ttau` | 5 | 5 | 0.8571 |
| 19 | `tuntu` | 50 | 48 | 0.9423 | `hiuu` | 161 | 136 | 0.8405 |
| 20 | `hasammil` | 8 | 8 | 0.9000 | `ikahiuna` | 4 | 4 | 0.8333 |

## Top-50 surfaces by effective score (substrate + control interleaved)

| rank | side | surface | n | k | posterior | credibility | effective |
|---:|:--|:--|---:|---:|---:|---:|---:|
| 1 | control | `tah` | 139 | 138 | 0.9858 | 1.000 | 0.9858 |
| 2 | control | `halipil` | 52 | 52 | 0.9815 | 1.000 | 0.9815 |
| 3 | substrate | `asah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 4 | substrate | `estan` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 5 | substrate | `katah` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 6 | substrate | `kun` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 7 | substrate | `pala` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 8 | substrate | `pu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 9 | substrate | `put` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 10 | substrate | `sa` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 11 | substrate | `sahis` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 12 | substrate | `sul` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 13 | substrate | `tahil` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 14 | substrate | `tu` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 15 | substrate | `zia` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 16 | control | `tar` | 50 | 50 | 0.9808 | 1.000 | 0.9808 |
| 17 | control | `laras` | 120 | 118 | 0.9754 | 1.000 | 0.9754 |
| 18 | control | `lin` | 51 | 50 | 0.9623 | 1.000 | 0.9623 |
| 19 | substrate | `kasuh` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 20 | substrate | `katte` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 21 | substrate | `kut` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 22 | substrate | `tahaia` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 23 | substrate | `taru` | 50 | 49 | 0.9615 | 1.000 | 0.9615 |
| 24 | control | `lepstt` | 24 | 24 | 0.9615 | 1.000 | 0.9615 |
| 25 | control | `tuti` | 49 | 48 | 0.9608 | 1.000 | 0.9608 |
| 26 | control | `tassantu` | 18 | 18 | 0.9500 | 1.000 | 0.9500 |
| 27 | substrate | `tuntu` | 50 | 48 | 0.9423 | 1.000 | 0.9423 |
| 28 | control | `hapi` | 107 | 99 | 0.9174 | 1.000 | 0.9174 |
| 29 | control | `stul` | 10 | 10 | 0.9167 | 1.000 | 0.9167 |
| 30 | substrate | `tittah` | 24 | 22 | 0.8846 | 1.000 | 0.8846 |
| 31 | control | `hileh` | 23 | 21 | 0.8800 | 1.000 | 0.8800 |
| 32 | control | `zehah` | 60 | 53 | 0.8710 | 1.000 | 0.8710 |
| 33 | substrate | `alep` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 34 | substrate | `antiu` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 35 | substrate | `sinit` | 50 | 44 | 0.8654 | 1.000 | 0.8654 |
| 36 | substrate | `anna` | 50 | 43 | 0.8462 | 1.000 | 0.8462 |
| 37 | control | `hiuu` | 161 | 136 | 0.8405 | 1.000 | 0.8405 |
| 38 | substrate | `sakil` | 50 | 42 | 0.8269 | 1.000 | 0.8269 |
| 39 | control | `kasku` | 122 | 101 | 0.8226 | 1.000 | 0.8226 |
| 40 | substrate | `hasammil` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 41 | substrate | `sahtaril` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 42 | control | `hini` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 43 | control | `tanttuha` | 8 | 8 | 0.9000 | 0.800 | 0.8200 |
| 44 | substrate | `hattus` | 24 | 20 | 0.8077 | 1.000 | 0.8077 |
| 45 | substrate | `hapalki` | 13 | 11 | 0.8000 | 1.000 | 0.8000 |
| 46 | control | `wal` | 123 | 99 | 0.8000 | 1.000 | 0.8000 |
| 47 | control | `wuli` | 21 | 17 | 0.7826 | 1.000 | 0.7826 |
| 48 | control | `heh` | 95 | 74 | 0.7732 | 1.000 | 0.7732 |
| 49 | control | `eshahi` | 7 | 7 | 0.8889 | 0.700 | 0.7722 |
| 50 | control | `heha` | 14 | 11 | 0.7500 | 1.000 | 0.7500 |

## Interpretation rules (v2, fixed before the run)

- **Pool size.** 124 entries, above the v21 bar of 80; not padded. Forms are read off viewed scans of Kammenhuber 1969 / Schuster 1974 with URL, page and quote (`pools/hattic.README.md`, `scripts/verify_hattic_sources.py`).
- **Reading.** A FAIL reads as a FAIL: weak evidence for specificity. A PASS supports the v15 generic-structure reading, not substrate affinity.
- **Circularity.** The `hattic` LM is trained on TLHdig running text (3,213 tokens / 1,940 types). 56 of the 124 pool surfaces also occur as LM word types (9.1% of LM tokens; v32 was 72 of 72). The own-LM readout is partly circular and is reported, not leaned on. `control_hattic_bigram` is scored under the same LM, which mitigates this for the gate itself.
- **v32 record.** The first run (72 hand-keyed forms, LM = pool) is kept in `results/hattic_gate_summary.json` and `results/rollup.bayesian_posterior.hattic.md`.

## Notes

- Metric: `external_phoneme_perplexity_v0`. LM: `hattic` (α=1.0, TLHdig running text, 1,940 word types; `harness/external_phoneme_models/hattic.json`).
- Gate: top-20 by posterior_mean only (credibility n_min=10 shown in the leaderboard, not used by the gate).
- Determinism: no RNG; re-runs are byte-identical given the same result-stream sidecars, manifests and pool YAMLs.

