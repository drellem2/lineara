# Eteocretan substrate pool (mg-6ccd, harness v21)

The 4th external-validation candidate substrate pool — the
Greek-alphabet, post-Linear-A language of inscriptions from eastern
Crete (~7th-3rd c. BCE). Eteocretan is the most a-priori-likely
candidate substrate by genealogy: scholarly consensus treats it as
the linguistic descendant of whatever underlies Linear A.

## Provenance

Built deterministically from `corpora/eteocretan/all.jsonl` via
`scripts/build_eteocretan_pool.py`. Each entry is a unique attested
word form from the Eteocretan inscriptional record; `attestations`
list the inscription IDs the form appears in, and the per-entry
citation tags whether the form appears in a partial bilingual
(Praisos 2 / Dreros 1).

Source catalogs:
* Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.*
  Amsterdam: J. C. Gieben.
* Whittaker, H. (2017). 'Of linguistic alterity in Crete: the
  Eteocretan inscriptions.' *SCI* 36: 7-31.
* Younger, J. G. 'Linear A: text and inscriptions.' Online catalog,
  https://people.ku.edu/~jyounger/LinearA/  (Eteocretan annex).

## Pool size and small-pool caveat

84 entries (after filtering 3 V-only word forms that
`scripts/generate_candidates.py` would skip wholesale because they
have only 1 phoneme class). The ≥80 acceptance bar is met.

The Eteocretan pool is small **by reality**, not by methodology
choice. The substantive textual material lives in just 9 multi-line
inscriptions (Praisos 1-7, Dreros 1-2); the remaining 91 corpus
entries are short attestations contributing single-word phonotactic
samples. The downstream `external_phoneme_perplexity_v0` LM
(`harness/external_phoneme_models/eteocretan.json`) is built with
α=1.0 to compensate for the small-corpus noise floor; this matches
the Etruscan smoothing setting and is documented in
`scripts/build_external_phoneme_models.py`.

## Glosses

Almost every entry carries `gloss: unknown`. Eteocretan is
undeciphered; even the partial bilinguals (Praisos 2, Dreros 1) do
not give word-by-word translations. We do not assert glosses we
cannot defend — the pool's purpose here is phonotactic-shape
modeling, not semantic decoding.

## Region

`region: crete`. Geographically, every attestation is from eastern
Crete (Praisos area + Dreros + the contested Psychro cave).

## Phoneme conventions

Per-character lowercase ASCII split of the surface. Multi-character
phonemes from the Greek-alphabet → ASCII transliteration (`th`,
`ph`, `kh`, `ks`, `ps`) are kept as bigrams of their constituent
letters — same convention as `pools/etruscan.yaml` and the Basque /
Mycenaean-Greek LM word lists. The `_phoneme_class` filter in the
build script uses the standard V/S/C decomposition (vowels: a e i o
u; sonorants: l r n m; consonants: everything else).

## Reproducibility

```bash
python3 scripts/build_eteocretan_corpus.py
python3 scripts/build_eteocretan_pool.py
```

Idempotent. Deterministic — entries sorted by surface, YAML keys in
stable order. Validates against `pools/schemas/pool.v1.schema.json`.
