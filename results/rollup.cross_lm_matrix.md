# Cross-LM matrix — substrate × LM (mg-b599 / harness v23)

**Headline: own-LM dominance pattern HOLDS for 3/5 substrate pools across the v23 cross-LM matrix.** Substrate pools whose own-LM gap exceeds every cross-LM gap: `etruscan`, `toponym`, `eteocretan`. Substrate pools where the own-LM gap is NOT the largest: `aquitanian`, `hattic`. Strongest own-LM gap: `eteocretan` (median posterior gap +0.201). Methodology paper §3.14 narrative: the framework's right-tail gate selectivity is genealogical-distance-modulated for substrate pools with substantial own-LM gaps; pools with small own-LM gaps (Aquitanian) lack the dynamic range for the cross-LM ordering to be cleanly readable.

## Matrix (gate verdict / p-value / median posterior gap)

| substrate ↓ \ LM → | `basque`<br/>Basque | `etruscan`<br/>Etruscan | `mycenaean_greek`<br/>Mycenaean Greek | `eteocretan`<br/>Eteocretan | `hattic`<br/>Hattic |
|:--|---:|---:|---:|---:|---:|
| `aquitanian`<br/>Aquitanian (proto-Basque, ~1st c. BCE / 1st c. CE) | PASS (own)<br/>p=3.22e-05<br/>gap=+0.030 | PASS<br/>p=0.020<br/>gap=+0.039 | FAIL<br/>p=0.095<br/>gap=+0.018 | PASS<br/>p=0.002<br/>gap=+0.041 | PASS<br/>p=0.038<br/>gap=+0.012 |
| `etruscan`<br/>Etruscan (Italic, ~7th c. BCE - 1st c. CE) | FAIL<br/>p=0.591<br/>gap=+0.008 | PASS (own)<br/>p=5.21e-04<br/>gap=+0.059 | FAIL<br/>p=0.185<br/>gap=+0.012 | FAIL<br/>p=0.924<br/>gap=-0.017 | FAIL<br/>p=0.420<br/>gap=+0.007 |
| `toponym`<br/>Mediterranean toponyms (modern surface forms; Greek-style) | PASS (own)<br/>p=9.99e-05<br/>gap=+0.109 | — | — | PASS<br/>p=0.025<br/>gap=+0.043 | PASS<br/>p=0.031<br/>gap=+0.074 |
| `eteocretan`<br/>Eteocretan (presumed Linear-A continuation, ~7th-3rd c. BCE) | PASS<br/>p=0.003<br/>gap=+0.095 | PASS<br/>p=0.007<br/>gap=+0.039 | PASS<br/>p=1.73e-05<br/>gap=+0.104 | PASS (own)<br/>p=4.10e-06<br/>gap=+0.201 | FAIL<br/>p=0.991<br/>gap=-0.061 |
| `hattic`<br/>Hattic (Anatolian isolate, specificity probe, ~2nd mill. BCE) | PASS<br/>p=0.042<br/>gap=+0.082 | PASS<br/>p=4.74e-05<br/>gap=+0.072 | PASS<br/>p=0.002<br/>gap=+0.038 | PASS<br/>p=9.20e-06<br/>gap=+0.106 | PASS (own)<br/>p=4.22e-04<br/>gap=+0.072 |

## Per-cell details

| substrate | LM | n_substrate_top | n_control_top | median(top substrate posterior) | median(top control posterior) | median gap (substrate − control) | MW U | MW p (one-tail) | gate |
|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--:|
| `aquitanian` | `basque` (own) | 20 | 20 | 0.9808 | 0.9512 | +0.030 | 345.0 | 3.22e-05 | PASS |
| `aquitanian` | `etruscan` | 20 | 20 | 0.9808 | 0.9422 | +0.039 | 275.5 | 0.020 | PASS |
| `aquitanian` | `mycenaean_greek` | 20 | 20 | 0.9808 | 0.9630 | +0.018 | 248.5 | 0.095 | FAIL |
| `aquitanian` | `eteocretan` | 20 | 20 | 0.9808 | 0.9401 | +0.041 | 307.0 | 0.002 | PASS |
| `aquitanian` | `hattic` | 20 | 20 | 0.9624 | 0.9500 | +0.012 | 266.0 | 0.038 | PASS |
| `etruscan` | `basque` | 20 | 20 | 0.9615 | 0.9535 | +0.008 | 192.0 | 0.591 | FAIL |
| `etruscan` | `etruscan` (own) | 20 | 20 | 0.9808 | 0.9217 | +0.059 | 321.0 | 5.21e-04 | PASS |
| `etruscan` | `mycenaean_greek` | 20 | 20 | 0.9615 | 0.9498 | +0.012 | 233.5 | 0.185 | FAIL |
| `etruscan` | `eteocretan` | 20 | 20 | 0.9341 | 0.9509 | -0.017 | 147.5 | 0.924 | FAIL |
| `etruscan` | `hattic` | 20 | 20 | 0.9245 | 0.9179 | +0.007 | 208.0 | 0.420 | FAIL |
| `toponym` | `basque` (own) | 20 | 20 | 0.9615 | 0.8525 | +0.109 | 337.5 | 9.99e-05 | PASS |
| `toponym` | `etruscan` | — | — | — | — | — | — | — | — |
| `toponym` | `mycenaean_greek` | — | — | — | — | — | — | — | — |
| `toponym` | `eteocretan` | 20 | 20 | 0.9615 | 0.9189 | +0.043 | 272.5 | 0.025 | PASS |
| `toponym` | `hattic` | 20 | 20 | 0.9712 | 0.8974 | +0.074 | 269.0 | 0.031 | PASS |
| `eteocretan` | `basque` | 20 | 20 | 0.9615 | 0.8661 | +0.095 | 303.0 | 0.003 | PASS |
| `eteocretan` | `etruscan` | 20 | 20 | 0.9378 | 0.8992 | +0.039 | 291.5 | 0.007 | PASS |
| `eteocretan` | `mycenaean_greek` | 20 | 20 | 0.9423 | 0.8382 | +0.104 | 353.0 | 1.73e-05 | PASS |
| `eteocretan` | `eteocretan` (own) | 20 | 20 | 0.9712 | 0.7697 | +0.201 | 364.0 | 4.10e-06 | PASS |
| `eteocretan` | `hattic` | 20 | 20 | 0.9000 | 0.9608 | -0.061 | 113.0 | 0.991 | FAIL |
| `hattic` | `basque` | 20 | 20 | 0.9808 | 0.8983 | +0.082 | 263.5 | 0.042 | PASS |
| `hattic` | `etruscan` | 20 | 20 | 0.9712 | 0.8991 | +0.072 | 343.5 | 4.74e-05 | PASS |
| `hattic` | `mycenaean_greek` | 20 | 20 | 0.9712 | 0.9333 | +0.038 | 304.0 | 0.002 | PASS |
| `hattic` | `eteocretan` | 20 | 20 | 0.9808 | 0.8750 | +0.106 | 356.5 | 9.20e-06 | PASS |
| `hattic` | `hattic` (own) | 20 | 20 | 0.9808 | 0.9083 | +0.072 | 321.0 | 4.22e-04 | PASS |

## Reading the matrix

Each cell reports the right-tail bayesian gate's verdict when the named substrate pool is paired against its matched control and both sides are scored under the named LM. ``own`` marks the substrate's home LM (the same LM family run_sweep dispatches the same-LM gate on); cross-LM cells score the same hypotheses under a non-home LM. PASS at the v10 right-tail bar requires MW p < 0.05 with the substrate-side posterior median strictly above the control's. The median posterior gap (substrate − control) is *informational*: the gate is rank-based, not gap-based, so a positive gap can co-exist with a FAIL when the rank distributions overlap.

If the framework's right-tail gate detects substrate-LM phonotactic kinship, the own-LM cell should produce the largest gap and cross-LM cells should produce progressively smaller gaps as the LM drifts further from the substrate's phonotactic profile. The headline above reports whether this pattern HOLDS pool-by-pool, which is the test of substrate-specific (vs. natural-language-LM-bias) signal.

**Hattic row / column (mg-7b882; v2 re-run mg-a38bf) — specificity probe, not a candidate substrate.** Hattic is an Anatolian isolate unrelated to Linear A. Since mg-7f4db its pool has 124 entries read off viewed scans of Kammenhuber 1969 / Schuster 1974 (above the v21 bar of 80), and the `hattic` LM is trained on TLHdig running text (1,940 word types). 56 of the 124 pool surfaces occur as LM word types (9.1% of LM tokens), so the `hattic` × `hattic` (own) cell is partly circular and is reported, not leaned on; the other cells of the `hattic` column are not circular. Under the v2 rules pre-registered in `scripts/hattic_gate.py`, a FAIL of the Hattic own-LM gate is weak evidence for specificity and a PASS supports the v15 generic-structure reading. The v32 matrix (72 hand-keyed forms, LM = pool) is in git history at 91bd0f13e.

## Provenance

- Generated by `scripts/v23_cross_lm_matrix.py`. Metric: `external_phoneme_perplexity_v0`. Top-K (gate): 20. n_min: 10.
- Result stream: union of all `results/experiments.external_phoneme_perplexity_v0*.jsonl` sidecars. The v23 cross-LM rows are split into the existing `.eteocretan.jsonl` (Eteocretan-substrate cross-LM rows) and a new `.under_eteocretan_lm.jsonl` (Aquitanian / Etruscan / Toponym substrate rows under the Eteocretan LM); the primary sidecar `experiments.external_phoneme_perplexity_v0.jsonl` (~88 MB) is left unchanged to keep individual files under GitHub's 100 MB push cap. mg-7b882 Hattic rows: own-LM and Hattic-substrate cross-LM rows in `.hattic.jsonl`; other substrate pools under the Hattic LM in `.under_hattic_lm.jsonl`. mg-a38bf v2 rows are appended to the same two sidecars and carry `notes` starting `mg-a38bf hattic-v2`; the loader takes the newest row per (hash, LM), so v2 rows supersede v32 rows.
- Per-cell rollup files: `results/rollup.bayesian_posterior.<substrate>.under_<lm>_lm.md` (v23 cross-LM cells); `results/rollup.bayesian_posterior.<substrate>.md` (own-LM cells, written by per-pool gate scripts in earlier harness versions).
- Determinism: re-running the rescore + this script produces byte-identical output given the same manifests + result-stream sidecars. No RNG anywhere in the pipeline.

