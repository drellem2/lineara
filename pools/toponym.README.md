# Pre-Greek toponym pool (mg-7c8c, expanded mg-c2af)

Pre-Greek substrate toponyms with the diagnostic suffixes -ssos, -nthos,
-ttos, -ndos, -mnos, and the broader Aegean-substrate place-name layer
discussed by Beekes 2010 (vol. 2 appendix on the Pre-Greek substrate),
Furnée 1972 (Die wichtigsten konsonantischen Erscheinungen des
Vorgriechischen), and Kretschmer 1896 (Einleitung in die Geschichte der
griechischen Sprache).

The pool was added during the harness v4 curated-bucket expansion
(mg-7c8c) so that the third-pool axis of `geographic_genre_fit_v1` can
exercise the maximum-region-compat row of its lookup table:
**`pre_greek` × Crete = 1.0** vs **`aquitania` × Crete = 0.25** and
**`etruria` × Crete = 0.5**. Every Cretan inscription where a toponym
candidate lands gets the strongest geographic-axis score the metric
emits.

mg-c2af expands the pool from 35 to 112 entries so that toponym
surfaces compete in the per-surface leaderboard with Aquitanian and
Etruscan, and adds derived fragment surfaces so the Linear-A bulk
generator can pin them to short syllabogram windows (the full
toponyms are typically 5-10 phonemes, longer than most Linear-A
windows in the SigLA corpus).

## Construction rules

- ≥ 100 entries (mg-c2af acceptance bar).
- Each `place`-tagged entry is a real attested place name from the
  cited sources.
- `morphology`-tagged entries are derived fragment surfaces (see
  fragmentation rule below) and document the substrate cluster they
  decompose into.
- Phoneme arrays use the Greek-via-Latinate transliteration practice
  in Beekes (e.g. /y/ rendered as /u/).
- Multi-character phonemes (`th`, `ts`, etc.) are permitted; the
  metric classes them by first character (matching the rest of the
  harness conventions).

## Fragmentation rule (mg-c2af)

Linear-A windows in the SigLA corpus skew short — most accountancy
tablet entries are 2-4 syllabograms — but the canonical Pre-Greek
toponyms are 5-10 phonemes (Knossos = 7, Halikarnassos = 13,
Probalinthos = 11). A bulk generator that only emits full-toponym
candidates pins almost nothing on the corpus. The fix: emit fragment
surfaces alongside each full toponym so the diagnostic substrate
clusters can land on short windows.

Fragment kinds added in mg-c2af:

1. **Suffix fragments** — the substrate suffixes that diagnose a
   Pre-Greek toponym. The /-ssos/, /-sos/, /-nthos/, /-ntha/, /-ttos/,
   /-tos/, /-ndos/, /-mnos/, /-mna/, /-aios/, /-aia/ family. Tagged
   `semantic_field: morphology`.
2. **Initial-onset fragments** — the high-frequency CV / CCV / CVC
   onsets of the toponym list (kno-, kor-, par-, tul-, hum-, hua-,
   olu-, muke-, ami-, gor-, phai-, ter-, lab-, per-, ephe-, smu-,
   prie-, les-, lem-, ther-, nax-, ina-, ala-).
3. **Substrate-cluster fragments** — short bigrams / trigrams that
   appear as recurrent components but are not full names on their
   own (e.g. `aso`, `ina`, `ala`).

Fragments inherit `region: pre_greek`, attest the toponym(s) they
were extracted from in their `attestations` list, and cite the
source the fragmentation rule itself rests on (Beekes vol. 2 §§3-5
on the -ssos/-sos/-ttos splits, Furnée §§120-128 on the broader
suffix typology).

The fragment-vs-full split is encoded in `semantic_field`:

- `place` → full attested toponym (49 entries).
- `morphology` → derived fragment (33 entries).
- (legacy mg-7c8c entries kept their `place` tagging for stability;
  mg-c2af preserved the existing 35 entries verbatim and added 77 new
  entries on top.)

## Bias caveats

- **Skewed toward classical-period attestations.** Most place entries
  are documented from Greek sources; a handful (Knossos, Tylissos,
  Phaistos, Amnisos, Pylos, Lyktos, Aptara) are independently attested
  in Linear A or Linear B, but most are reconstructed from later Greek
  transcriptions. The substrate hypothesis is itself contested for
  some of these names (Olympos, Mukenai, Athenai); we follow Beekes'
  inclusive practice.
- **Cretan-heavy and Anatolian-heavy.** Crete is overrepresented
  because the Linear A corpus is overwhelmingly Cretan, and we want
  to exercise the `pre_greek × Crete = 1.0` region-compat cell.
  Anatolian toponyms are overrepresented because the substrate
  continuum extends into Asia Minor and Beekes vol. 2 documents many
  of them; their geographic compat falls back to neutral 0.5
  (unmapped) on Cretan inscriptions where most candidates land.
- **Some toponyms have transparent later etymology** (e.g. Olympos
  is sometimes reconstructed from PIE root \*olu-). Beekes treats
  these as substrate; the field is not unanimous. We record what
  Beekes records.
- **Fragment surfaces are not standalone words.** Treating /-ssos/
  or /kno-/ as a surface is a convenience for the bulk generator;
  the substrate fragments only carry meaning as components of the
  full names they were extracted from. Per-surface leaderboard
  results that lift `ssos` or `kno` to the top should be read as
  "this fragment family appears with discriminating frequency in
  the corpus", not as "this fragment denotes anything by itself".

## Re-deriving / refreshing

The list is hand-curated from Beekes 2010, Furnée 1972, and Kretschmer
1896; no programmatic fetch or scrape is involved. To extend, add
entries at the bottom of the YAML and bump `fetched_at`. Mechanical
hash determinism follows trivially because the pool YAML is
content-stable; the bigram model the harness builds from this pool is
a function of the entries present.

## Score expectations under v3 metrics + pool dispatch

The mg-c2af pool-bigram dispatch fix means the toponym pool's
empirical bigram model is now applied to toponym hypotheses (and only
toponym hypotheses); previously the runner was falling back to the
Aquitanian bigram for toponym candidates, which under-rewarded the
substrate-typical /-ssos/ and /-nthos/ clusters because those bigrams
are not in the Aquitanian vocabulary. Expected effect: toponym
local_fit_v1 scores should improve on average, and the dispersion
across surfaces should widen as the pool's own statistics start
discriminating between fragment families.

`geographic_genre_fit_v1` continues to ride at `α=0.4 * 1.0 + 0.6 *
semantic_compat`; with `place × accountancy = 0.75` (most common
pairing) toponym candidates should land near +0.85 on this axis,
unchanged from mg-7c8c.

The per-surface leaderboard (mg-c2af) is the central new view: each
fragment family aggregates dozens to hundreds of corpus candidates,
and the median pmcd is the pool-vs-pool indicator that survives the
within-surface plausibility-of-context gap (mg-7c8c power calculation
showed individual-candidate metrics need n ≈ 2,400 to grade
plausibility; aggregate-per-surface across the corpus gets us a
statistic the metrics CAN grade).
