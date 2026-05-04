# Basque text corpus (mg-ee18)

External substrate-language text corpus used to train the Basque
char-bigram phoneme prior consumed by
`external_phoneme_perplexity_v0`.

## Provenance

* **Source.** Plain-text extracts of articles from the Basque-language
  Wikipedia (eu.wikipedia.org), pulled via the MediaWiki action API
  (`prop=extracts&explaintext=1`).
* **Pinning.** `corpora/basque.fetch_manifest.txt` lists one
  `<oldid>\t<title>` per line. Wikipedia article revisions are
  immutable, so a re-fetch of the same `oldid` returns byte-identical
  source text. The manifest is committed; `text.txt` is gitignored
  because it is derived.
* **Volume.** 122 pinned revisions; ~3.5 M chars after normalization.
  Acceptance bar is ≥100 k chars.
* **Authoring snapshot.** Manifest authored 2026-05-04 against
  eu.wikipedia.org current revisions on that date.

## License

Wikipedia text is licensed under **CC BY-SA 4.0**
(https://creativecommons.org/licenses/by-sa/4.0/). This repository
ships only the manifest of `(oldid, title)` pairs and the fetch script
— the derived `text.txt` is not committed. Anyone who runs the fetch
locally produces a CC BY-SA 4.0 corpus that they must continue to
attribute as such if they redistribute it.

The downstream char-bigram model (`harness/external_phoneme_models/basque.json`)
is a statistical artifact derived from the corpus. Per the CC BY-SA
"adapted material" provisions, the bigram model carries the same
license; it is committed under that license with attribution to
"Basque Wikipedia contributors (eu.wikipedia.org)" recorded here.

## Reproducibility

```bash
# One-time: refresh the manifest with current revids. Authors only.
python3 scripts/fetch_basque_corpus.py --resolve-revids

# Re-fetch text.txt from the pinned revisions in the manifest.
# Idempotent given the manifest.
python3 scripts/fetch_basque_corpus.py
```

## Format

* Single UTF-8 file at `corpora/basque/text.txt`.
* Lowercase plain text. The 26-letter Latin alphabet is preserved;
  `ñ`, `ü`, `ç` are folded to `n`, `u`, `s` respectively (the brief
  specifies a 26-char vocabulary, and these letters are rare in the
  general corpus). Digits, punctuation, markup, and IPA diacritics are
  stripped.
* Whitespace is collapsed to a single ASCII space; no newlines beyond
  the trailing one. Each pinned article's extract is separated from
  the next by a single space.

## Phonemic justification

Modern standard Basque orthography (Trask 1997, _The History of
Basque_, ch. 1 §1.4) is largely phonemic: `<a>` `<e>` `<i>` `<o>`
`<u>` are the five vowels; `<x>` is /ʃ/; `<tx>` /tʃ/; `<tz>` /ts̻/;
`<ts>` /ts̺/; `<j>` /j/ in most dialects; `<h>` is silent in most
dialects. The cleaned `text.txt` therefore doubles as a phoneme
stream for char-bigram modeling at acceptable approximation, with the
known caveat that digraph allophony (`<tx>`, `<tz>`, `<ts>`) is
collapsed to bigrams of the underlying letters. This is consistent
with the way Aquitanian phonemes are already represented in
`pools/aquitanian.yaml`.
