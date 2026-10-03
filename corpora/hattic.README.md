# Hattic lexical-attestation corpus (mg-7e7d6, specificity probe)

External corpus used to train the Hattic char-bigram phoneme prior
(`harness/external_phoneme_models/hattic.json`) consumed by
`external_phoneme_perplexity_v0`, and the source of `pools/hattic.yaml`.

## Why Hattic, and what it can and cannot show

Hattic is the non-Indo-European isolate of Bronze Age central Anatolia
(the pre-Hittite language of Ḫatti), known only through the Hittite
state archives at Ḫattuša. It has **no relationship** to Linear A or to
any of the Aegean / old-European pools already in this repo
(Aquitanian, Etruscan, Eteocretan, Mycenaean Greek).

It is run through the lineara program as a **specificity probe**
(handoff 2026-05-06 §D.3). v15 (mg-7ecb) showed that the right-tail gate
passes for any pool that shares character pairs with its LM. If the
framework PASSes on Hattic as readily as on Eteocretan / Aquitanian /
Etruscan, that is evidence the signal is generic structure, not
substrate affinity. A Hattic PASS is **not** a decipherment claim and
not evidence that Linear A is Hattic or related to it.

## Provenance

Hand-keyed by the mg-7e7d6 polecat via `scripts/build_hattic_corpus.py`.
Works cited per record:

* Soysal, O. (2004). *Hattischer Wortschatz in hethitischer
  Textüberlieferung.* HdO I/74. Leiden: Brill. — the standard Hattic
  lexicon; main reference for the lexemes.
* Klinger, J. (1996). *Untersuchungen zur Rekonstruktion der
  hattischen Kultschicht.* StBoT 37. Wiesbaden: Harrassowitz.
* Kammenhuber, A. (1969). 'Hattisch.' In *Altkleinasiatische Sprachen*,
  HdO I/2.1-2/2: 428-546. Leiden: Brill. — Hittite titles and words of
  probable Hattic origin.
* Taracha, P. (2009). *Religions of Second Millennium Anatolia.* DBH 27.
  Wiesbaden: Harrassowitz. — the Hattic pantheon.
* del Monte, G. F. & Tischler, J. (1978). *Die Orts- und Gewässernamen
  der hethitischen Texte.* RGTC 6. — toponyms.
* Bischoff, A. M. (2023). 'Some new Hattian-Hittite correspondences from
  the quasi-bilingual text of CTH 733.' *Hungarian Assyriological
  Review* 4: 95-109. — `an` 'sea', `il` 'prosper'.
* de.wikipedia 'Hattische Sprache' (accessed 2026-10-03) — the analysed
  `le-` / verbal word forms (`le-binu`, `taš-te-nuwa`, `tu-ḫ-ta-šul`, …).

### Choice of source, and how it departs from the ticket

The ticket suggested keying Hattic **running text** from the CTH 725-745
cult texts and bilinguals. That was not done. Keying connected passages
needs the printed editions (Schuster's bilingual editions, Klinger 1996,
Soysal 2004) collated line by line, and the polecat could not consult
them; keying them from memory would have fabricated text. The
reachable online material (Wikipedia en/de, Bischoff 2023) holds only
about 20 forms. So the corpus is **lexical**: one record per attested
lexeme, theonym, or Hattic-area name, each pointing to the work that
standardly treats it.

**The forms have not been collated against the printed editions.** They
are standard citation forms from the Hattic literature, keyed from the
compiler's knowledge of it. Collating them against Soysal 2004 is the
recommended follow-up if the probe result is ever given evidential
weight.

## Volume and tiers

72 records, 72 unique normalised word forms (one per record; no
connected text, so tokens = types).

| category | tier A | tier B |
|---|---:|---:|
| theonym | 19 | 6 |
| lexeme (incl. titles, analysed word forms) | 23 | 8 |
| toponym | — | 14 |
| personal name | — | 2 |
| **total** | **42** | **30** |

* **Tier A**: core, widely cited Hattic lexemes and theonyms whose
  Hattic status is uncontroversial.
* **Tier B**: the Hattic attribution is conventional but argued. This
  covers Hittite titles and words of probable Hattic origin
  (`tawananna`, `tabarna`, `tuḫkanti`, `ḫalentu`, `ḫapalki`), Hattic-area
  toponyms and personal names (the language layer is inferred from
  geography and cult context), and Bischoff's 2023 proposals.

23 records carry `is_bilingual: true`, meaning their gloss rests on a
Hattic-Hittite bilingual correspondence.

## Normalisation (applied identically to corpus, LM, and pool)

Hattic "phonemes" are a **transliteration convention** over Hittite
scribal cuneiform, not a phonetic transcription. The real phonology,
including the debated labial fricative written "f" by some authors,
is not recoverable at this resolution. `normalise()` maps the cited
form to lowercase ASCII:

* diacritics stripped: **š → s** (s/š merged), **ḫ → h**, ē → e;
* morpheme hyphens removed (`le-binu` → `lepinu`);
* stop voicing merged to the voiceless series: **b → p, d → t, g → k**
  (cuneiform does not reliably write Hattic stop voicing);
* "f" (Wikipedia's `fur`, `findu`) → **w**, because cuneiform writes it
  with the WA series (`wur`, `wintu`);
* plene vowel runs collapsed (`ka-a-at-te` → `katte`);
* consonant gemination kept as conventionally cited.

The resulting inventory is 16 letters: `a e h i k l m n p r s t u w y z`
(no `o`, `b`, `d`, `g`, `f`).

## License

The underlying tablets are Bronze Age and public domain. The lexical
forms and glosses are cited from the scholarly literature as fair-use
scholarly data, following the `corpora/etruscan.README.md` /
`corpora/eteocretan.README.md` convention. Bischoff 2023 is CC BY-NC
4.0. Only a handful of individual word forms are taken from it, with
attribution and for non-commercial research use, so that is compatible.

This repository commits:
* `corpora/hattic/inscriptions/<id>.json`: one lexical record each,
  with cited form, normalised form, gloss, tier, and citation (the
  directory name mirrors the other corpora; these are not inscriptions);
* `corpora/hattic/all.jsonl`: aggregate, sorted by id;
* `harness/external_phoneme_models/hattic.json`: the char-bigram LM
  (α = 1.0), a statistical derivative.

`corpora/hattic/words.txt` is gitignored, as for the other corpora, and
is rebuilt by the script.

## Reproducibility

```bash
python3 scripts/build_hattic_corpus.py
python3 scripts/build_external_phoneme_models.py --only hattic
python3 scripts/build_hattic_pool.py
python3 scripts/build_control_pools.py --pool hattic --sampler bigram --suffix _bigram
```

All four are deterministic. Byte-identical rebuilds are asserted by
`harness/tests/test_build_hattic.py` and `harness/tests/test_control_pools.py`.

## What this corpus is *not*

* **Not running text.** There is no Hattic word order or phrase context
  in it, and the LM's word-boundary statistics come from isolated
  citation forms.
* **Not unbiased.** Names (25 theonyms, 14 toponyms, 2 personal names:
  41 of 72) are over-represented
  compared with real Hattic text, and they are long compounds
  (`wurunkatte`, `katahzipuri`), so they skew the bigram statistics
  toward onomastic shapes.
* **Not collated** (see above).
