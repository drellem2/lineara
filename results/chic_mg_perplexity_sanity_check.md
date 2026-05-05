# CHIC partial-reading × Mycenaean Greek LM cross-check (chic-v2; mg-362d)

**Sanity check, NOT a decipherment claim.** This document scores the anchored portion of the top-30 most-anchored CHIC inscriptions (from `results/chic_anchor_density_leaderboard.md`) under the v12 Mycenaean-Greek char-bigram LM (`harness/external_phoneme_models/mycenaean_greek.json`). The purpose is to confirm that the anchor inheritance machinery produces *well-formed phoneme strings* — not to assert that CHIC encodes Mycenaean Greek. The substrate hypothesis for CHIC remains pre-Greek; high or low MG perplexity here is informational, not evidential for any specific reading.

## Method

For each leaderboard inscription, walk the raw `tokens[]`. Extract maximal contiguous **runs** of anchored phoneme tokens (runs split by unanchored signs, DIV, and `[?]`). Char-decompose each run; bracket with `<W>` boundary sentinels. Score char-bigram log-probability under the MG LM. Normalize by total scored characters → per-char log-likelihood (nats). Per-char perplexity is `exp(-loglik)`.

This mirrors `external_phoneme_perplexity_v0` in `harness/metrics.py` (mg-ee18, harness v8); the only difference is run extraction comes from anchor application instead of candidate-equation scoring.

## LM artifact

- Source: `harness/external_phoneme_models/mycenaean_greek.json`
- α (smoothing): 0.1 — well-resourced corpus (≥5,000 inscriptions, ≥100k phoneme tokens); minimal smoothing keeps rare-bigram log-probs informative (matches the Basque setting).
- Trained on: corpora/linear_b/words.txt (LiBER, https://liber.cnr.it; syllabogram-derived Mycenaean-Greek transliterations from the per-inscription HTML, hyphens stripped). (n_words=5113, n_chars=31332, n_bigrams_observed=41557)

## Aggregate

- Inscriptions scored: **30** of 30
- Mean per-char log-likelihood (nats): **-2.5775**
- Mean per-char perplexity: **13.1645**

## Per-inscription scores

| Rank | CHIC id | n_anch | n_runs | n_chars | loglik/char (nats) | perplexity/char | anchored phonemes |
|--:|---|--:|--:|--:|--:|--:|---|
| 1 | CHIC #293 | 10 | 4 | 18 | -2.6955 | 14.8133 | `ma-i \| i-ja-ro \| wa-mu-te \| ki-de` |
| 2 | CHIC #270 | 8 | 3 | 14 | -2.7761 | 16.0563 | `ra-i \| ki-de \| i-ro-ja-te` |
| 3 | CHIC #284 | 5 | 2 | 9 | -2.4017 | 11.0417 | `ki-de \| i-ja-ro` |
| 4 | CHIC #207 | 4 | 2 | 8 | -2.4371 | 11.4394 | `ke-to \| ki-de` |
| 5 | CHIC #249 | 4 | 2 | 7 | -2.6663 | 14.3864 | `i-ja \| ki-de` |
| 6 | CHIC #011 | 3 | 2 | 6 | -3.0856 | 21.8811 | `de-de \| ti` |
| 7 | CHIC #069 | 3 | 2 | 6 | -2.5282 | 12.5305 | `to \| to-ra` |
| 8 | CHIC #133 | 3 | 1 | 6 | -2.5145 | 12.3610 | `ra-ti-ni` |
| 9 | CHIC #162 | 3 | 1 | 5 | -2.1863 | 8.9020 | `i-ja-ro` |
| 10 | CHIC #163 | 3 | 1 | 5 | -2.8824 | 17.8568 | `wa-ra-i` |
| 11 | CHIC #167 | 3 | 1 | 6 | -2.1773 | 8.8226 | `de-ra-ra` |
| 12 | CHIC #169 | 3 | 1 | 5 | -2.1863 | 8.9020 | `i-ja-ro` |
| 13 | CHIC #172 | 3 | 1 | 6 | -2.6854 | 14.6637 | `ja-ke-ti` |
| 14 | CHIC #179 | 3 | 2 | 6 | -2.6958 | 14.8176 | `wa-ke \| ke` |
| 15 | CHIC #184 | 3 | 1 | 6 | -2.4494 | 11.5812 | `ki-pa-ra` |
| 16 | CHIC #195 | 3 | 1 | 5 | -2.1863 | 8.9020 | `i-ja-ro` |
| 17 | CHIC #218 | 3 | 1 | 5 | -2.1863 | 8.9020 | `i-ja-ro` |
| 18 | CHIC #279 | 3 | 1 | 5 | -2.1863 | 8.9020 | `i-ja-ro` |
| 19 | CHIC #012 | 2 | 1 | 4 | -2.7851 | 16.2021 | `ti-de` |
| 20 | CHIC #035 | 2 | 1 | 4 | -2.5121 | 12.3308 | `wa-te` |
| 21 | CHIC #081 | 2 | 1 | 4 | -2.5240 | 12.4789 | `ti-ra` |
| 22 | CHIC #088 | 2 | 1 | 4 | -2.8030 | 16.4945 | `ro-ni` |
| 23 | CHIC #106 | 2 | 1 | 4 | -2.6852 | 14.6614 | `pa-de` |
| 24 | CHIC #134 | 2 | 1 | 4 | -2.6409 | 14.0264 | `wa-ke` |
| 25 | CHIC #135 | 2 | 1 | 4 | -2.6409 | 14.0264 | `wa-ke` |
| 26 | CHIC #136 | 2 | 1 | 4 | -2.6409 | 14.0264 | `wa-ke` |
| 27 | CHIC #137 | 2 | 1 | 4 | -2.6409 | 14.0264 | `wa-ke` |
| 28 | CHIC #150 | 2 | 1 | 4 | -2.6709 | 14.4536 | `ki-de` |
| 29 | CHIC #151 | 2 | 1 | 4 | -2.6776 | 14.5500 | `wa-me` |
| 30 | CHIC #152 | 2 | 1 | 4 | -3.1773 | 23.9826 | `mu-ki` |

## Interpretation notes

- Per-char log-likelihood is in nats; **higher = more language-like** under the MG LM. The MG LM is trained on Linear-B-derived Mycenaean Greek transliterations (LiBER corpus, ~5.1k words / ~31k chars / α=0.1), so it scores highest on phoneme strings that look like Mycenaean Greek.
- A value far from MG-typical (toward higher perplexity) could mean either (a) the underlying CHIC language is *not* Mycenaean Greek (the working substrate hypothesis), or (b) the anchor pool is too small to produce stable runs (most CHIC inscriptions have very few anchored positions). Both readings are consistent with chic-v3+ continuing on a substrate-language framework rather than an MG framework.
- A value near MG-typical does *not* establish that CHIC encodes Mycenaean Greek. The MG LM's smoothing floor is high enough that short, low-information runs can score near-baseline under any input — see `harness/metrics.py` discussion of the small-coverage failure mode.
