# Hattic running-text corpus (mg-7f4db; specificity probe)

External corpus used to train the Hattic char-bigram phoneme prior
(`harness/external_phoneme_models/hattic.json`) consumed by
`external_phoneme_perplexity_v0`. Since mg-7f4db it is **running text
from a published digital edition**. It is no longer the pool's word list.

## Why Hattic, and what it can and cannot show

Hattic is the non-Indo-European isolate of Bronze Age central Anatolia
(the pre-Hittite language of Ḫatti), known only through the Hittite
state archives at Ḫattuša. It has **no relationship** to Linear A or to
any of the Aegean / old-European pools in this repo.

It is run through the lineara program as a **specificity probe**
(handoff 2026-05-06 §D.3). v15 (mg-7ecb) showed that the right-tail gate
passes for any pool that shares character pairs with its LM. A Hattic
PASS is **not** a decipherment claim and not evidence that Linear A is
Hattic or related to it.

## What changed in mg-7f4db, and why

v32 (mg-7e7d6) hand-keyed 72 lexical forms from memory, without
collating them against any edition, and trained the LM on exactly those
72 forms, so the LM corpus *was* the pool. The v32 write-up therefore
read the gate FAIL as "inconclusive on data quality". Daniel,
2026-10-03: "use published editions not memory please". mg-7f4db
replaced both data sets:

* **LM corpus (this directory).** Every intact Hattic word in the TLHdig
  transliterations, with tablet and line references.
* **Pool** (`pools/hattic.yaml`). Built separately from a page-cited
  lexicon of forms read off the scans of Kammenhuber 1969 and Schuster
  1974. See `pools/hattic.README.md`.

None of the v32 forms or records were carried over.

## Source

**Thesaurus Linguarum Hethaeorum digitalis (TLHdig), Beta Version 0.2**,
Hethitologie-Portal Mainz. The XML dataset is on Zenodo,
<https://doi.org/10.5281/zenodo.15459134> (file `TLHdig_0.2.0-beta.zip`, sha256
`02304950b3b33ac2e85f6020df57a91a3184aa994ac1eab6f58e796a7a0f282a`,
CC BY 4.0), and online at <https://www.hethport.uni-wuerzburg.de/TLHdig/>
(hethiter.net/: TLHdig). TLHdig holds the transliterations of the
published Boğazköy editions (KUB, KBo, …) and of some unpublished
fragments (e.g. the `Or. 90/…` numbers), tagged line by line and word
by word for language. The dataset was downloaded and read during
mg-7f4db. Hattic (`lg="Hattian"` / `"Hat"`) occurs in 647 manuscripts
under 73 CTH numbers.

`scripts/extract_tlhdig_hattic.py` reduces the XML to
`corpora/hattic/sources/tlhdig_hattic_lines.tsv`: one row per line
containing Hattic, with columns CTH, manuscript, line number, the line's
Hattic words as transliterated (breaks shown as `[`…`]`), and its
**intact** words. A word counts as intact only if no sign of it lies in
a break (`<del_in/>`…`<del_fin/>`, which can run across words and lines;
anything inside is lost or restored by the editor) and it is not a
fragment, an illegible sign (`x`), a Sumerogram or Akkadogram, an
editor's insertion or deletion (`〈…〉`, `〈〈…〉〉`), or an unread glyph.
Restored text is therefore never in the corpus. The zip itself (64 MB)
is not committed. The TSV is committed, and it is the only input of
`scripts/build_hattic_corpus.py`.

| | count |
|---|---:|
| lines with Hattic words (TSV rows) | 6,421 |
| Hattic word tokens on those lines | 17,043 |
| intact word tokens | 3,214 |
| manuscripts / CTH numbers | 647 / 73 |
| manuscripts with ≥1 intact word (corpus records) | 397 |
| corpus word tokens (normalised, length ≥ 2) | 3,213 |
| corpus word types (`words.txt`, the LM input) | 1,940 |

2,700 of the 3,213 tokens come from the Hattic and Hattic-Hittite texts
of CTH 725-746. The other 513 come from texts catalogued elsewhere:
the bilingual building ritual KUB 2.2+ (Bo 2030, the text Schuster 1974
edits; TLHdig files it under CTH 413), Hattic recitations embedded in
Hittite festival and cult texts (mainly CTH 627 and 670), and CTH 231
VBoT 68, a list of town names with the Hattic suffix *-il* that TLHdig
tags as Hattic. TLHdig's language tags
are taken as given.

Only one word in five survives intact (3,214 of 17,043). That is the
cost of excluding all restorations; the tablets are badly broken.

## Records

`corpora/hattic/inscriptions/<id>.json` (one per manuscript; the
directory name mirrors the other corpora) and the aggregate
`corpora/hattic/all.jsonl` hold `id`, `cth`, `manuscript`, `lines` (each
with `line` = TLHdig line reference, `raw`, `intact`, normalised
`words`), the flat `words`, `source_citation` and `url`.

## Normalisation (applied identically to corpus, LM, and pool)

Hattic "phonemes" are a **transliteration convention** over Hittite
scribal cuneiform, not a phonetic transcription. `normalise()` maps a
transliteration to lowercase ASCII. These rules are **unchanged from
v32**:

* diacritics stripped: **š → s**, **ḫ → h**, ú/í/é/á → u/i/e/a;
* hyphens removed (`ka-a-at-te` → `katte`);
* stop voicing merged: **b → p, d → t, g → k**;
* "f" → **w** (cuneiform writes it with the WA series);
* plene vowel runs collapsed;
* consonant gemination kept.

mg-7f4db **adds** three rules, which the sources force. Both printed
editions use a "bound transcription" that the v32 forms never used:

* **u̯ → w** (Kammenhuber's u̯ is the WA-series sign, which TLHdig writes
  `wa`: Kammenhuber `ḫanu̯aₐšuit` „Thron“ and TLHdig KUB 2.2+ III 16
  `ka-a-ḫa-a-an-wa-šu-it-tu-un` both give `…hanwasuit…`);
* **i̯ → i** (the IA-series sign, which TLHdig writes `ia`);
* **v → w** (Schuster's transcription of the same WA sign, `vae-`).

Subscript indices (`u̯aₐ`) and TLHdig sign-index numbers (`ša₄`) are
dropped. Both sides end up with the same 15-letter inventory:
`a e h i k l m n p r s t u w z`. (v32 also had `y`; no source here
writes it.)

## LM-corpus / pool overlap

The LM is trained on `words.txt`, the 1,940 corpus types. The pool is
not in it, but Hattic is one language, so forms recur:

| | count |
|---|---:|
| pool surfaces that are also a corpus word type | **56 of 124 (45%)** |
| corpus word types that are a pool surface | 56 of 1,940 (2.9%) |
| corpus word tokens equal to a pool surface | 291 of 3,213 (9.1%) |
| pool surfaces occurring inside some corpus word (substring) | 104 of 124 |
| pool character bigrams also seen in the corpus | 123 of 123 |

In v32 the corresponding figures were 72 of 72 and 100%: corpus = pool.
The 56 shared forms are ordinary attestations (`katte` „König“,
`taparna`, `pala` „und“, `wur` „Land“ …). Their whole-word
contribution to the LM is 56 types among 1,940. They are pinned in
`harness/tests/test_build_hattic.py`.

## License

TLHdig data: CC BY 4.0 (Zenodo record above). Attribution: Thesaurus
Linguarum Hethaeorum digitalis, hethiter.net/: TLHdig, Beta Version 0.2,
Hethitologie-Portal Mainz. The transliterations are those of the
published editions. The underlying tablets are Bronze Age and public
domain. `harness/external_phoneme_models/hattic.json` is a statistical
derivative. `corpora/hattic/words.txt` is gitignored and rebuilt by the
script.

## Reproducibility

```bash
# once, from the Zenodo zip (not committed):
python3 scripts/extract_tlhdig_hattic.py TLHdig_0.2.0-beta.zip
# from the committed TSVs:
python3 scripts/build_hattic_corpus.py
python3 scripts/build_external_phoneme_models.py --only hattic
python3 scripts/build_hattic_pool.py
python3 scripts/build_control_pools.py --pool hattic --sampler bigram --suffix _bigram
# check the pool's page citations against the scans (network):
python3 scripts/verify_hattic_sources.py
```

All builds are deterministic. `harness/tests/test_build_hattic.py`
asserts byte-identical corpus and pool rebuilds and tests the extractor
on hand-made TLHdig XML. `harness/tests/test_control_pools.py` covers
the control.

## What this corpus is *not*

* **Not a token-frequency model.** The LM sees word *types*
  (`words.txt` is sorted-unique, as for the other corpora). Duplicate
  manuscripts of one text add no weight.
* **Not complete.** Restored and damaged words are excluded (above), and
  TLHdig is a beta that is still growing.
* **Not glossed.** The corpus is untranslated Hattic text. Glosses live
  only in the pool's lexicon.
