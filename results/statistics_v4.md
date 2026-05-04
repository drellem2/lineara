# mg-7c8c statistics: curated v4 (n=20 per bucket)

Mann-Whitney U + Cliff's δ + power-calculation report on the 100-row curated set defined by `hypotheses/curated/CONSTRUCTION.manifest.jsonl` (100 entries) under three v3 metrics. Power-calc constants: α=0.05, β=0.20. Scramble bucket RNG seed=4242 (curated v4); mg-fb23 scrambles used seed=42.

## Headline acceptance gate

**Plausible Aquitanian (B; n=20) vs deliberately-wrong Aquitanian (C; n=20)** under the v3 metrics. The mg-fb23 / mg-7dd1 / mg-23cc n=4 buckets all missed this gate (identical medians, +0.14 v1-units, and -20 bits respectively); this is the same test re-run at n=20.

### plausible Aquitanian (bucket=B_aquit_plausible) vs deliberately-wrong Aquitanian (bucket=C_aquit_wrong)

| metric | n_a | n_b | median_a | median_b | Δ_medians | Mann-Whitney U_a | z | p | Cliff's δ | detectable Δ (n=20, α=.05, β=.2) | underpowered? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `local_fit_v1` | 20 | 20 | -2.7410 | -2.7168 | -0.0242 | 208.0 | +0.203 | 0.8392 | +0.040 | 0.2622 | yes |
| `partial_mapping_compression_delta_v0` | 20 | 20 | -56.0000 | -104.0000 | +48.0000 | 224.0 | +0.637 | 0.5244 | +0.120 | 75.4108 | yes |
| `geographic_genre_fit_v1` | 20 | 20 | +0.5500 | +0.2500 | +0.3000 | 392.0 | +5.445 | 0.0000 | +0.960 | 0.0748 | no |

## Anchor vs scramble (sanity check)

**Linear-B anchor (A; n=20) vs random scramble (E; n=20)**. mg-fb23's gate (anchor median > scramble median) cleared at n=4; verifying it holds at n=20 is reassurance that the metrics still separate something well-grounded from random.

### Linear-B carryover anchor (bucket=A_linear_b_anchor) vs random scramble (bucket=E_scramble)

| metric | n_a | n_b | median_a | median_b | Δ_medians | Mann-Whitney U_a | z | p | Cliff's δ | detectable Δ (n=20, α=.05, β=.2) | underpowered? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `local_fit_v1` | 20 | 20 | -4.4867 | -4.1696 | -0.3170 | 115.0 | -2.286 | 0.0223 | -0.425 | 0.2139 | yes |
| `partial_mapping_compression_delta_v0` | 20 | 20 | -80.0000 | -128.0000 | +48.0000 | 266.0 | +1.774 | 0.0761 | +0.330 | 73.0392 | yes |
| `geographic_genre_fit_v1` | 20 | 20 | +0.5000 | +0.5000 | +0.0000 | 200.0 | +0.000 | 1.0000 | +0.000 | 0.0000 | no |

## Toponym (third pool) vs scramble

**Pre-Greek toponym (D; n=20) vs random scramble (E; n=20)**. Tests whether the toponym pool's third-pool axis carries any discriminative signal at all (independent of any plausible-vs-wrong claim).

### pre-Greek toponym (bucket=D_toponym_plausible) vs random scramble (bucket=E_scramble)

| metric | n_a | n_b | median_a | median_b | Δ_medians | Mann-Whitney U_a | z | p | Cliff's δ | detectable Δ (n=20, α=.05, β=.2) | underpowered? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `local_fit_v1` | 20 | 20 | -3.1559 | -4.1696 | +1.0137 | 356.0 | +4.206 | 0.0000 | +0.780 | 0.4035 | no |
| `partial_mapping_compression_delta_v0` | 20 | 20 | -32.0000 | -128.0000 | +96.0000 | 310.5 | +2.979 | 0.0029 | +0.552 | 75.4108 | no |
| `geographic_genre_fit_v1` | 20 | 20 | +0.5000 | +0.5000 | +0.0000 | 200.0 | +0.000 | 1.0000 | +0.000 | 0.0000 | no |

## Plausible Aquitanian vs anchor (control sanity)

**Plausible Aquitanian (B; n=20) vs Linear-B anchor (A; n=20)**. Both buckets are 'plausible'; metrics should NOT separate them strongly. A large effect here would suggest a confound.

### plausible Aquitanian (bucket=B_aquit_plausible) vs Linear-B anchor (bucket=A_linear_b_anchor)

| metric | n_a | n_b | median_a | median_b | Δ_medians | Mann-Whitney U_a | z | p | Cliff's δ | detectable Δ (n=20, α=.05, β=.2) | underpowered? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `local_fit_v1` | 20 | 20 | -2.7410 | -4.4867 | +1.7457 | 400.0 | +5.396 | 0.0000 | +1.000 | 0.2000 | no |
| `partial_mapping_compression_delta_v0` | 20 | 20 | -56.0000 | -80.0000 | +24.0000 | 217.0 | +0.447 | 0.6551 | +0.085 | 68.0433 | yes |
| `geographic_genre_fit_v1` | 20 | 20 | +0.5500 | +0.5000 | +0.0500 | 350.0 | +4.572 | 0.0000 | +0.750 | 0.0476 | no |

### Bucket distributions (raw)

#### `local_fit_v1`

| bucket | n | median | mean | sd | min | max |
|---|---:|---:|---:|---:|---:|---:|
| `A_linear_b_anchor` | 20 | -4.4867 | -4.4471 | 0.1300 | -4.5781 | -4.1100 |
| `B_aquit_plausible` | 20 | -2.7410 | -2.7075 | 0.2916 | -3.4100 | -2.2073 |
| `C_aquit_wrong` | 20 | -2.7168 | -2.7247 | 0.3004 | -3.2428 | -2.1526 |
| `D_toponym_plausible` | 20 | -3.1559 | -3.2793 | 0.5614 | -4.9790 | -2.6311 |
| `E_scramble` | 20 | -4.1696 | -4.2504 | 0.3157 | -4.9274 | -3.8744 |

#### `partial_mapping_compression_delta_v0`

| bucket | n | median | mean | sd | min | max |
|---|---:|---:|---:|---:|---:|---:|
| `A_linear_b_anchor` | 20 | -80.0000 | -77.6000 | 57.1930 | -184.0000 | +40.0000 |
| `B_aquit_plausible` | 20 | -56.0000 | -74.8000 | 92.3394 | -280.0000 | +72.0000 |
| `C_aquit_wrong` | 20 | -104.0000 | -88.8000 | 77.2280 | -272.0000 | +40.0000 |
| `D_toponym_plausible` | 20 | -32.0000 | -42.8000 | 64.5613 | -176.0000 | +64.0000 |
| `E_scramble` | 20 | -128.0000 | -135.2000 | 101.6000 | -416.0000 | +48.0000 |

#### `geographic_genre_fit_v1`

| bucket | n | median | mean | sd | min | max |
|---|---:|---:|---:|---:|---:|---:|
| `A_linear_b_anchor` | 20 | +0.5000 | +0.5000 | 0.0000 | +0.5000 | +0.5000 |
| `B_aquit_plausible` | 20 | +0.5500 | +0.5650 | 0.0760 | +0.4000 | +0.7000 |
| `C_aquit_wrong` | 20 | +0.2500 | +0.2950 | 0.0921 | +0.2500 | +0.5000 |
| `D_toponym_plausible` | 20 | +0.5000 | +0.5000 | 0.0000 | +0.5000 | +0.5000 |
| `E_scramble` | 20 | +0.5000 | +0.5000 | 0.0000 | +0.5000 | +0.5000 |

## Methodology notes

- **Mann-Whitney U.** Two-sided, with mid-rank tie correction. p-value via normal approximation with continuity correction (Hollander, Wolfe & Chicken §4.2). Self-contained implementation in `scripts/curated_v4_stats.py`; no scipy.
- **Cliff's δ.** `(#(a>b) − #(a<b)) / (n_a × n_b)`. Range [-1, +1]; +1 = every value in *a* exceeds every value in *b*; -1 = the reverse; 0 = stochastic equivalence. |δ| ≥ 0.474 is 'large' (Cliff 1993).
- **Power calculation.** Two-sample two-sided z-test approximation: detectable Δ at α=0.05, 1-β=0.80 is `(z_{1-α/2} + z_{1-β}) × pooled_sd × √(1/n_a + 1/n_b)`. If observed |Δ_means| < detectable Δ, the comparison is underpowered for the observed effect even at n=20.
- **Bucket C heterogeneity.** The 4 mg-fb23 wrong-Aquitanian entries embed a phonotactic-position-mismatch rule; the 16 v4 entries embed a genre-context-mismatch rule. Mann-Whitney U is rank-based, so this mixed bucket is fine for testing the central question (does the metric rank plausible above wrong, period?).
- **Score sources.** Most-recent row per `(hypothesis_hash, metric)` from `results/experiments.jsonl` (in case of duplicate rows from re-runs). Curation is deterministic and corpus-stable, so under normal conditions there is exactly one row per (hash, metric) on the current snapshot.

