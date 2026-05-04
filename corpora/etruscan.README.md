# Etruscan word-forms corpus (mg-ee18)

External substrate-language word-form corpus used to train the
Etruscan char-bigram phoneme prior consumed by
`external_phoneme_perplexity_v0`.

## Provenance

* `pools/etruscan.yaml` — the existing Etruscan substrate-root pool
  (mg-23cc), itself authored from Bonfante & Bonfante 2002 and
  Pallottino's TLE. Each entry contributes its `surface` plus its
  `attestations` list.
* `scripts/build_etruscan_corpus.py` `SUPPLEMENTARY` table — a curated
  list of well-attested Etruscan word forms organized by category
  (numerals, magistracies, kinship, religious vocabulary, verbal
  forms, calendar, personal names, toponyms, civic vocabulary, Liber
  Linteus phrases, function words). Per-category source citations are
  inlined in the script.

Primary cited sources for both layers:

* Bonfante, G., & Bonfante, L. (2002). *The Etruscan Language: An
  Introduction* (revised ed.). Manchester University Press. — alphabet
  + phonology (ch. 4), morphology + glossary (ch. 5–6).
* Pallottino, M. (1968). *Testimonia Linguae Etruscae* (TLE), 2nd ed.
  Florence: La Nuova Italia. — inscription corpus standard.
* CIE — *Corpus Inscriptionum Etruscarum* (cinerary urn inscriptions).
* Liber Linteus (Zagreb mummy wrappings) and Tabula Cortonensis (the
  two longest extant Etruscan texts).

## License

Cited fair-use of the secondary sources for compilation of word
forms. The underlying inscriptions are in the public domain. The
derived `corpora/etruscan/words.txt` is gitignored (mirroring the
Basque pattern — both external corpora are reproducible from the
committed build script). The downstream char-bigram model
(`harness/external_phoneme_models/etruscan.json`) is committed as a
statistical derivative.

## Reproducibility

```bash
python3 scripts/build_etruscan_corpus.py
```

Idempotent: the script normalizes, dedupes, and emits forms in sorted
order. Re-runs produce a byte-identical file. Build authored against
`pools/etruscan.yaml` 2026-05-04.

## Format

* Single UTF-8 file at `corpora/etruscan/words.txt`.
* One word form per line. Sorted alphabetically.
* Lowercase ASCII (a–z only).
* `ś` folded to `s` to align with the Linear-A candidate phoneme
  inventory (which has only `s`); other diacritics stripped.
* Hyphenated compounds split on the hyphen — each component becomes
  its own line. Single-character forms dropped.
* Aspirate digraphs `th`, `ph`, `ch` are *kept* as 2-char sequences:
  the bigram model treats them as 2 chars, which is the right level
  for char-bigram statistics over the standard Latin transliteration
  of Etruscan (Bonfante & Bonfante 2002 ch. 4).

## Phoneme conventions (Bonfante & Bonfante 2002 ch. 4)

* 4 vowels: `a`, `e`, `i`, `u`. **No /o/.** Loanwords sometimes show
  `o` in transliteration; the corpus carries this as-is.
* `c k q` for /k/.
* `b d g` only in early loans.
* `f v` for /f w/.
* `s ś` for /s ʃ/ (folded to `s` here per format note).
* `z` for /ts/.
* Aspirates `th ph ch` as single phonemes /tʰ pʰ kʰ/.

## Acceptance bar

mg-ee18 sets ≥500 word forms. Current build emits 666 unique forms.
The bar is met, but Etruscan is corpus-limited by reality (only a few
thousand attested words exist), and the bigram log-likelihoods will
remain noisy at the small-corpus end. The Etruscan model uses a
larger smoothing α (1.0) than Basque (0.1) to compensate; this is
documented in `scripts/build_external_phoneme_models.py` and in
the model JSON's metadata.
