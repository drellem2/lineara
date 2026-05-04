# Pre-Greek toponym pool (mg-7c8c)

Pre-Greek substrate toponyms with the diagnostic suffixes -ssos, -nthos,
-ttos, -ndos, and the broader Aegean-substrate place-name layer
discussed by Beekes 2010 (vol. 2 appendix on the Pre-Greek substrate)
and Furnée 1972 (Die wichtigsten konsonantischen Erscheinungen des
Vorgriechischen).

The pool was added during the harness v4 curated-bucket expansion
(mg-7c8c) so that the third-pool axis of `geographic_genre_fit_v1` can
exercise the maximum-region-compat row of its lookup table:
**`pre_greek` × Crete = 1.0** vs **`aquitania` × Crete = 0.25** and
**`etruria` × Crete = 0.5**. Every Cretan inscription where a toponym
candidate lands gets the strongest geographic-axis score the metric
emits.

## Construction rules

- 35 entries (≥30 acceptance bar from the brief).
- Each entry is a real attested place name from the cited sources.
- Phoneme arrays use the Greek-via-Latinate transliteration practice
  in Beekes (e.g. /y/ rendered as /u/).
- Multi-character phonemes (`th`, `ts`, etc.) are permitted; the
  metric classes them by first character (matching the rest of the
  harness conventions).
- All entries carry `semantic_field: place` and `region: pre_greek`.

## Bias caveats

- **Skewed toward classical-period attestations.** Most entries are
  documented from Greek sources; a handful (Knossos, Tylissos, Phaistos,
  Amnisos) are independently attested in Linear A, but most are
  reconstructed from later Greek transcriptions. The substrate
  hypothesis is itself contested for some of these names (Olympos,
  Mukenai, Athenai); we follow Beekes' inclusive practice.
- **Cretan-heavy.** 10/35 entries are Cretan; this is intentional
  because the Linear A corpus is overwhelmingly Cretan, and the goal
  of this pool is to exercise the `pre_greek × Crete = 1.0`
  region-compat cell. The Aegean-island and Anatolian rows are
  included for breadth but their geographic compat will fall back
  to neutral 0.5 (unmapped) on the Cretan inscriptions where
  candidates land.
- **Some toponyms have transparent later etymology (e.g. Olympos
  is sometimes reconstructed from PIE root \*olu-);** Beekes treats
  these as substrate; the field is not unanimous. We record what
  Beekes records.

## Re-deriving / refreshing

The list is hand-curated from Beekes 2010's appendix; no programmatic
fetch or scrape is involved. To extend, add entries at the bottom of
the YAML and bump `fetched_at`. Mechanical hash determinism follows
trivially because the pool YAML is content-stable; the bigram model
the harness builds from this pool is a function of the entries
present.

## Score expectations under v3 metrics

Two-pool comparison row in mg-23cc's findings showed Etruscan candidates
clearing Aquitanian on `geographic_genre_fit_v1` (+0.574 vs +0.452
mean) because etruria × Cretan-site = 0.5 vs aquitania × Cretan-site =
0.25. Adding `pre_greek × Crete = 1.0` gives a third tier; expected
mean for toponym candidates against Cretan inscriptions:
`α=0.4 * 1.0 + 0.6 * semantic_compat`. With `place × accountancy = 0.75`
(the most common pairing), the toponym candidates should land near
**+0.85** on this axis, well above either prior pool's mean.

The local_fit_v1 distribution shape is harder to predict. Toponym
phoneme inventories are similar to Aquitanian/Etruscan in scale but
include heavier consonant clusters; the empirical bigram model will
fit those patterns. The pool is intentionally broader than the bulk
sweep needs (the bulk path is out of scope for this ticket — see
mg-7c8c's "out of scope" list).
