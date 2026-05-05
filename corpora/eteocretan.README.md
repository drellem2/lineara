# Eteocretan inscription corpus (mg-6ccd, harness v21)

External substrate-language inscription corpus used to train the
Eteocretan char-bigram phoneme prior consumed by
`external_phoneme_perplexity_v0`. Eteocretan is the
Greek-alphabet, post-Linear-A language of inscriptions from eastern
Crete (~7th-3rd c. BCE), broadly held by the consensus to be the
linguistic descendant of whatever underlies Linear A — making it the
single most a-priori-likely candidate substrate by genealogy.

## Provenance

* **Sources.** Three published catalogs:
  * Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.*
    Amsterdam: J. C. Gieben. — the canonical scholarly edition of the
    Eteocretan inscriptional record. Provides the Praisos 1-7 and
    Dreros 1-2 transcriptions and the (debated) Psychro stone.
  * Whittaker, H. (2017). 'Of linguistic alterity in Crete: the
    Eteocretan inscriptions.' *Scripta Classica Israelica* 36: 7-31. —
    the most recent scholarly catalog; supplements Duhoux with
    additional short attestations from the Praisos area whose
    language is non-Greek and conventionally treated as Eteocretan.
  * Younger, J. G. (2000-present). 'Linear A: text and inscriptions.'
    https://people.ku.edu/~jyounger/LinearA/ — primarily a Linear A
    catalog, with an Eteocretan annex covering iron-age Cretan
    short inscriptions.
* The transcriptions are hand-keyed from the cited published editions.
  This is a manual-transcription corpus, not a scraper-built one — the
  Eteocretan epigraphic record is too small (~9 substantive multi-line
  inscriptions) and too fragmentary for an OCR or scraping approach to
  pay off.
* **Volume.** 100 inscriptions; 87 unique word forms; 215 word tokens.
  Of those 100, 9 are canonical multi-line Praisos / Dreros texts (IC
  III.vi.1-7, Dreros 1-2); 1 is the Psychro stone (debated authenticity);
  the remaining 90 are short attestations (single-word graffiti, pottery
  sherd inscriptions, dedicatory tags, personal names) drawn from the
  three catalogs.

## License

The underlying inscriptions are public domain (Bronze Age / Iron Age
stone-cut texts, ~7th-3rd c. BCE). Cited fair-use of Duhoux 1982 and
Whittaker 2017 for the transcribed forms and editorial conventions.

This repository commits:
* `corpora/eteocretan/inscriptions/<id>.json` — per-inscription metadata
  (Greek-alphabet text, ASCII transliteration, word list, citation).
* `corpora/eteocretan/all.jsonl` — aggregate, sorted by id.
* `corpora/eteocretan/words.txt` — flat sorted-unique word list,
  gitignored (mirrors the Basque / Etruscan / Linear-B pattern;
  reproducible from the build script).
* `harness/external_phoneme_models/eteocretan.json` — the downstream
  char-bigram model (statistical derivative).

## Reproducibility

```bash
python3 scripts/build_eteocretan_corpus.py
python3 scripts/build_external_phoneme_models.py --only eteocretan
```

Idempotent. The build script normalizes Greek → ASCII, sorts inscription
records by id, and emits stable JSON keys; re-runs produce byte-identical
output.

## Format

Per-inscription JSON object:
```json
{
  "id": 2,
  "name": "Praisos 2",
  "site": "praisos",
  "ic_ref": "IC III.vi.2",
  "completeness": "multi-line",
  "text": "<Greek-alphabet text, lowercased, lacuna markers as ...>",
  "transliteration": "<ASCII a-z + spaces, lacunae dropped>",
  "words": ["<word forms from the transliteration>"],
  "provenance": "<short note>",
  "source_citation": "<publication>",
  "is_bilingual": true
}
```

## Phoneme conventions

Eteocretan is written in the East Cretan Doric Greek alphabet. The
ASCII transliteration uses standard scholarly conventions:
* Vowels: α a, ε e, η e, ι i, ο o, υ u, ω o
* Stops: π p, β b, τ t, δ d, κ k, γ g
* Aspirates: θ th, φ ph, χ kh, ψ ps
* Sonorants: λ l, μ m, ν n, ρ r
* Sibilants: σ/ς s, ζ z
* Cluster: ξ ks
* Digamma: ϝ w (preserved in eastern Cretan dialects through the
  archaic period; appears in Praisos 2, Dreros 1-2)
* Diacritics (psili, oxia, perispomeni, etc.) are stripped before
  transliteration — they are editorial additions not present in the
  stone-cut originals.

## Acceptance bar

mg-6ccd sets ≥80 inscriptions. Current build emits 100. Note the
qualitative caveat: the substantive textual material lives in just 9
multi-line texts (Praisos 1-7, Dreros 1-2) — the additional 90+
short attestations contribute mostly word-boundary structure and
single-word phonotactic shape, not connected text. The downstream
char-bigram model is correspondingly noisier than Aquitanian (≥1,000
forms) or Etruscan (~700 forms); the α=1.0 smoothing constant
documented in `scripts/build_external_phoneme_models.py` matches the
Etruscan setting and is the natural choice for this corpus size.

## What this corpus is *not*

* **Not deciphered.** Praisos 2 and Dreros 1 are partial bilinguals
  but the surviving Greek counterparts give vocabulary anchors, not
  a word-by-word translation. The corpus carries the Eteocretan side
  for phonotactic-shape modeling; it does not claim semantic
  decipherment.
* **Not normalized for dialect period.** The texts span ~400 years;
  Praisos 1 is c. 7th c. BCE and Dreros 1 is c. 5th c. BCE.
  Phonological drift across that span is not adjusted for — the
  bigram model treats every word form as an independent sample.
* **Not free of editorial uncertainty.** Where Duhoux 1982 reads
  letters that other editions question, we follow Duhoux's reading
  silently. The provenance field on each inscription documents the
  primary publication.
