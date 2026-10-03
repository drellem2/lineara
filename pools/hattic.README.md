# Hattic substrate pool (mg-7e7d6, specificity probe)

A pool built from Hattic, the Bronze Age central-Anatolian isolate known
only through the Hittite archives. **This is a specificity probe, not a
candidate Linear A substrate.** Hattic has no relationship to Linear A
or to the Aegean / old-European pools (Aquitanian, Etruscan, Eteocretan).
v15 (mg-7ecb) showed that the right-tail gate passes for any pool that
shares character pairs with its LM. If the gate PASSes on Hattic as
readily as on the Aegean pools, that is evidence the signal is generic
structure, not substrate affinity (handoff 2026-05-06 §D.3). A Hattic
PASS is not a decipherment claim.

## Provenance

Built deterministically from `corpora/hattic/all.jsonl` via
`scripts/build_hattic_pool.py`. Each entry is one normalised Hattic word
form. `attestations` holds the cited scholarly form(s), and `citation`
names the corpus record ids and the work the form is taken from. Main
sources: Soysal 2004 (*Hattischer Wortschatz*), Klinger 1996,
Kammenhuber 1969, Taracha 2009, RGTC 6, and Bischoff 2023. The full list
is in `corpora/hattic.README.md`.

The forms are hand-keyed standard citation forms. They have **not** been
collated against the printed editions (see the corpus README).

## Pool size: 72 entries, below the ≥80 v21 bar

The 72 entries are what the attested lexicon supports at reasonable
confidence. The pool was **not** padded to 80: no conjectural or
synthetic forms were added, and every entry has `provenance: real`. The
`notes` field carries the confidence tier (42 tier A, 30 tier B; tiers
are defined in the corpus README). Two consequences for the sweep ticket:

* The paired-diff / right-tail gate has somewhat less power than on the
  84-entry Eteocretan pool. Compare effect sizes, not just PASS/FAIL.
* Only 31 of the 72 entries are common lexemes (23 tier A + 8 tier B).
  The other 41 are names (25 theonyms, 14 toponyms, 2 personal names).
  A gate result driven by names says little about Hattic phonotactics
  in general.

## Fields

* `surface` / `phonemes`: normalised lowercase ASCII, split one
  character per phoneme. Normalisation: š→s, ḫ→h, b/d/g→p/t/k,
  f→w, plene collapsed, gemination kept. This is the same normalisation
  used for the LM corpus. Inventory: `a e h i k l m n p r s t u w y z`.
* `gloss`: the scholarly gloss (theonyms and toponyms are glossed by
  function).
* `semantic_field`: `hattic_theonym` / `hattic_lexeme` /
  `hattic_toponym` / `hattic_personal_name`.
* `region`: `central_anatolia`.

## Control

`pools/control_hattic_bigram.yaml` is the bigram-preserving phonotactic
control (production default since v18), built with
`scripts/build_control_pools.py --pool hattic --sampler bigram --suffix _bigram`.

## Dispatch

`hattic` and `control_hattic_bigram` route to the `hattic` LM in
`scripts/run_sweep.py` (`_EXT_POOL_LANGUAGE`, with sidecar tag `hattic`)
and in `scripts/per_surface_bayesian_rollup.py`. `scripts/v23_cross_lm_matrix.py`
gets a Hattic row and a `hattic` LM column. The sweep and gate run
belong to the next ticket.

## Reproducibility

```bash
python3 scripts/build_hattic_corpus.py
python3 scripts/build_hattic_pool.py
```

Idempotent and deterministic. The pool validates against
`pools/schemas/pool.v1.schema.json`, and `harness/tests/test_build_hattic.py`
asserts a byte-identical rebuild.
