# Aquitanian / Proto-Basque substrate pool

`pools/aquitanian.yaml` is the v1 substrate-root pool used by the bulk
candidate generator (`scripts/generate_candidates.py`). Every entry is a
candidate root drawn from one of three traceable sources:

1. **Aquitanian onomastica** — personal names and theonyms attested on
   Roman-era votive altars and funerary inscriptions in the southwestern
   Gallic provinces (Aquitania Tertia / Novempopulania), catalogued in:
   - Gorrochategui, J. (1984). *Estudio sobre la onomástica indígena de
     Aquitania.* Vitoria-Gasteiz: UPV/EHU.
2. **Modern Basque substrate vocabulary** — root vocabulary that Trask
   identifies as plausibly continuous with the substrate language, drawn
   from his etymological discussion in:
   - Trask, R. L. (1997). *The History of Basque.* London: Routledge.
     (Chapters 3, 4, and the lexical-history sections.)
3. **Public-domain inscription catalogues** — the underlying primary
   inscriptions catalogued by Gorrochategui are out of copyright (their
   discovery dates from the 19th and early 20th centuries; the Roman-era
   originals themselves are public domain).

## Why these three together

The point of the pool is not "the canonical Aquitanian dictionary" —
no such thing exists, since the language is attested only in onomastic
fragments. The point is to expose the local-fit metric to a *broad*
inventory of plausibly-substrate roots and characterize its bulk
behaviour. Trask's modern-Basque material lets us cover semantic fields
(numerals, body parts, basic vocabulary) that the onomastic record alone
cannot. Gorrochategui's catalogue grounds the pool in actually-attested
ancient forms.

Per-entry citations identify which source each root is anchored in.

## Schema

`pools/schemas/pool.v1.schema.json`. Required fields per entry:
`surface`, `phonemes`. Recommended: `gloss`, `semantic_field`, `region`,
`attestations`, `citation`. The `region` and `semantic_field` fields are
forward-compat for the geographic-vs-genre second-stage filter (separate
ticket); they are emitted into the candidate hypotheses but not yet
consumed by the metric.

## Phoneme conventions

Phonemes are written in lowercase modern-Basque-style orthography. The
multi-character digraphs `tx` (=/tʃ/), `tz` (=/ts̻/), and `ts` (=/ts̺/)
are kept as single phoneme units; the `local_fit_v0` metric classifies
them by their first character (so all three count as class C).

The metric requires every entry to span at least two distinct phoneme
classes (V/S/C) to avoid the `control_std=0` pathology documented in
mg-fb23. The pool was filtered to satisfy that constraint at compile
time.

## Refresh / regeneration

This pool is hand-compiled, not scraped. To revise:

1. Add or remove entries in `aquitanian.yaml`. Keep entries sorted by
   stable order (currently grouped: numerals, body parts, kin terms,
   nature, attested onomastica).
2. Update the per-entry `citation` and the top-level `source_citation`
   if a new source is introduced.
3. Re-run `scripts/generate_candidates.py --pool aquitanian` (it is
   idempotent — same pool + same corpus regenerate the same candidate
   YAMLs deterministically).
4. Re-run `scripts/run_sweep.py --manifest hypotheses/auto/aquitanian.manifest.jsonl`
   to extend the result stream. The sweep runner is resumable; only
   newly-emitted candidates will be scored.

## Verification

`python3 -c "import json,yaml,jsonschema; \
  d=yaml.safe_load(open('pools/aquitanian.yaml')); \
  s=json.load(open('pools/schemas/pool.v1.schema.json')); \
  jsonschema.Draft202012Validator(s).validate(d); \
  print(len(d['entries']),'entries')"`

## Substitution policy

If digitizing Aquitanian secondary-source data turns out to be blocked,
the ticket (mg-f832) permits substitution to Etruscan or pre-Greek
toponyms under the same schema. As of this commit no substitution was
needed; the pool ships with Aquitanian/Proto-Basque material.
