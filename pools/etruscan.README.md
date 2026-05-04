# Etruscan substrate pool

`pools/etruscan.yaml` is the second substrate-root pool used by the bulk
candidate generator (`scripts/generate_candidates.py`). Filed under
mg-23cc as the second-pool ingest the polecats v2 directions called for.
Every entry is a candidate root drawn from one of three traceable sources:

1. **Bonfante & Bonfante 2002** — *The Etruscan Language: An
   Introduction* (revised ed., Manchester / New York: Manchester
   University Press). The canonical English-language reference grammar
   and the source for the bulk of the pool's vocabulary; chapters 4
   (alphabet and phonology), 5 (morphology, numerals, onomastics, and
   common particles), and the appendix glossary anchor every entry's
   gloss and phonemic transcription.
2. **Pallottino's Testimonia Linguae Etruscae (TLE), 2nd ed. 1968** —
   the standard inscription numbering. TLE numbers are referenced in
   the per-entry `citation` field where the entry's attestations come
   from a small, well-known inscription (e.g. TLE 1 = Cippus
   Perusinus).
3. **Etruscan Texts Project (ETP), University of Massachusetts Amherst
   (https://etp.classics.umass.edu)** — the searchable corpus of ~13,000
   Etruscan inscriptions; used for attestation cross-checks and
   frequency. Underlying inscriptions are public domain.

## Why these three together

The Etruscan corpus is unusual: ~13,000 inscriptions but only ~500
distinct words confidently glossed, and the preserved vocabulary is
heavily biased toward funerary and religious genres (cinerary urns,
sarcophagi, votive bronzes, the Liber Linteus, the Tabula Capuana). The
pool consequently over-represents `semantic_field: religion` and
`semantic_field: kin` (mostly funerary epitaph vocabulary), under-
represents agriculture / animal / commodity terms, and includes the
numeral system in full because numerals are one of the most
confidently-glossed sub-systems thanks to the dice of Tuscania and the
Tabula Cortonensis.

This is a real-world sampling bias to keep in mind when reading the
results: if Etruscan candidates concentrate on accountancy-tablet
windows, the `geographic_genre_fit_v1` semantic_compat score will pull
them down (most religious-field entries score 0.25 against accountancy);
if they concentrate on the small votive_or_inscription subset, the
filter favors them (1.0 for religion × votive_or_inscription).

## Phonology (constraints on the bigram model)

Etruscan phonology differs from Aquitanian / Basque in ways that matter
for the metric:

- **Four vowels: a, e, i, u — no /o/.** This alone gives the empirical
  bigram model trained on Etruscan a different shape from the Aquitanian
  model: bigrams ending or starting in /o/ have zero pool-side
  probability and rely on Laplace smoothing. The local_fit_v1 bigram
  term is therefore not bit-comparable across pools.
- **Aspirate stops: ch, ph, th alongside plain c (=/k/), p, t.** Pool
  entries keep the digraphs as single phoneme tokens (matching how the
  Aquitanian pool keeps `tx`, `tz`, `ts`); the local_fit_v0 V/S/C
  classifier handles them by their first character (so all three count
  as class C).
- **Fricatives s, z, f, h, sh (š).** s vs z is an attested phonemic
  contrast and both appear in the bigram model.
- **Liquids l, r; nasals m, n; glide v (=/w/).** Standard for the
  region.
- **Syllable structure CV / CVC predominantly.** Initial consonant
  clusters do appear (`clan`, `cletram`, `mlach`, `spura`) but are less
  common than CV; the empirical bigram model picks this up automatically
  from the pool surfaces.

Multi-character phonemes (`ch`, `ph`, `th`, `sh`) are kept as single
units exactly as in the Aquitanian pool's `tx`/`tz`/`ts` — the metric
classifies them by their first character.

The metric requires every entry to span at least two distinct phoneme
classes (V/S/C); the pool was constructed to satisfy that constraint.

## Schema

`pools/schemas/pool.v1.schema.json`. Required: `surface`, `phonemes`.
Recommended: `gloss`, `semantic_field`, `region`, `attestations`,
`citation`. Every entry in this pool sets `region: etruria` — the
geographic-origin tag, parallel with `aquitania` for the Aquitanian
pool (the convention is geographic region, not language family).

The mg-7dd1 region-compat lookup table keyed Etruscan rows under
`etruscan`; mg-23cc adds `etruria` rows alongside (so both keys
resolve to the same compat scores). The Etruscan × Cretan-site
compat is 0.5 (Mediterranean substrate ties; less direct than
pre-Greek toponyms, more direct than aquitania × Crete = 0.25).

## Refresh / regeneration

This pool is hand-compiled. To revise:

1. Add or remove entries in `etruscan.yaml`. Keep entries grouped by
   semantic field for human readability.
2. Update the per-entry `citation` and the top-level `source_citation`
   if a new source is introduced.
3. Re-run `scripts/generate_candidates.py --pool etruscan`.
4. Re-run `scripts/run_sweep.py --manifest hypotheses/auto/etruscan.manifest.jsonl --metrics ...`.

## Verification

```bash
python3 -c "import json,yaml,jsonschema; \
  d=yaml.safe_load(open('pools/etruscan.yaml')); \
  s=json.load(open('pools/schemas/pool.v1.schema.json')); \
  jsonschema.Draft202012Validator(s).validate(d); \
  print(len(d['entries']),'entries')"
```

## Pool-quality caveats

- **Religious / funerary bias.** ~25% of entries are `semantic_field:
  religion` and another ~18% are `kin` (largely funerary praenomina).
  The `geographic_genre_fit_v1` semantic_compat lookup table prices
  most of these poorly against accountancy tablets (0.25), which is the
  dominant Linear A genre — so Etruscan composite leaderboard scores
  will systematically run below Aquitanian on the third axis. This is
  a real-world property of the available Etruscan vocabulary, not a
  metric defect.
- **Latin loans included where attested.** A handful of entries
  (`capra`, `nepos`, `vinum`) are arguably late loans from or into
  Latin; they are included because they appear in Etruscan-context
  inscriptions, and excluding them would over-purify the pool relative
  to the actual epigraphic record.
- **Debated numeral values.** `huth` (4 or 6) and `sa` (4 or 6) have
  contested glosses in the literature; both are kept with the
  uncertainty noted in the gloss field.
- **No primary-source review.** Entries cite Bonfante & Bonfante 2002
  as the secondary source; primary inscription review (TLE re-reading,
  ETP attestation cross-check) is a future ticket.
