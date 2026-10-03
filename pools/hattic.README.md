# Hattic substrate pool (mg-7e7d6; rebuilt from published editions, mg-7f4db)

A pool built from Hattic, the Bronze Age central-Anatolian isolate known
only through the Hittite archives. **This is a specificity probe, not a
candidate Linear A substrate.** Hattic has no relationship to Linear A
or to the Aegean / old-European pools. If the right-tail gate PASSes on
Hattic as readily as on the Aegean pools, that is evidence the signal is
generic structure, not substrate affinity (handoff 2026-05-06 §D.3).

## What changed in mg-7f4db

v32 (mg-7e7d6) keyed 72 forms from memory and did not collate them
against any edition. mg-7f4db discarded all 72 and rebuilt the pool
under one rule: **a form enters only if its published source was opened
and read during the task, and the entry records where (scan URL + page)**.
A form known from memory but not found on a viewed page is not in the
pool, even where it is standard (that is why, for example, v32's
`windu` „Wein“ and `Kait` are absent).

## Sources

### Opened and used

| source | where viewed | pages used | rows |
|---|---|---|---:|
| Kammenhuber, A. (1969). 'Hattisch.' In *Altkleinasiatische Sprachen*, HdO I/2.1-2/2: 428-546 | Internet Archive scan `friedrich-reiner-kammenhuber-neumann-heubeck-altkleinasiatische-sprachen-1969` (page images + OCR) | 432-437, 446-447, 460-462, 466, 479-480, 495-497, 526-530, 535 | 121 |
| Schuster, H.-S. (1974). *Die hattisch-hethitischen Bilinguen* I/1 | Internet Archive scan `die-hattisch-hethitischen-bilinguen` | 89, 92-93, 96-97, 101, 103, 105, 107, 116, 126, 146 | 13 |

Kammenhuber's backbone sections are the alphabetical list of all Hattic
words collected in RHA 70 (§ 9, pp. 446-447), the verb list with glosses
(§ 26a, pp. 526-530), and the Hattic loanwords, titles and theonyms of
§ 4 (pp. 432-437). The 13 Schuster rows are the `cited` rows of mg-78856
(`~/research/hattic-semitic/data/hattic.tsv`, commit 46557d35), reused
as that ticket's README says they may be. Its other `cited` rows either
duplicate a Kammenhuber entry here (they are added to it as a second
citation) or were left out: `a-ša-a` (no stem), `li-e-bi-nu` (stem `in`
too uncertain), the prefix `ḫa-`, and `u̯aₐ-aḫ-zi-i-ḫé-ir-ta`, whose verb
is entered from Kammenhuber as `ziḫer`.

The OCR misreads ḫ, š, u̯ and subscripts, so every Kammenhuber form was
**read off the page image** in this task. Pages with dense bound
transcription were re-rendered at 220-250 dpi. The Schuster forms were
read off the page images by mg-78856. Here they were spot-checked
against the images of pp. 93, 97 and 126 (`tiuz`, `tu`, `bu`/`i̯a`,
`vae-`, `tittaḫ`), and all 13 are machine-checked against the OCR of
the cited leaf (below).

### Not reachable (as reported by mg-78856; not re-searched)

* **Soysal 2004**, *Hattischer Wortschatz* (the standard lexicon):
  Internet Archive copy lending-restricted, Brill paywalled.
* **Klinger 1996**, StBoT 37: no open copy.
* **Schuster 2002**, *Bilinguen* Teil 2: no open copy.

Daniel was asked for Soysal 2004 / Klinger 1996 PDFs. None had arrived
when this ticket was dispatched, so neither is used.

## Size: 124 entries (≥ 80 bar met)

`corpora/hattic/sources/lexicon.tsv` has **134 rows** (one per form per
source) for **125 lexemes**. One lexeme, `ai̯a` „geben“ → `aia`, has
only vowels and fails the builder's two-phoneme-class filter (as in the
Eteocretan builder), which leaves **124 pool entries**. Nothing was
padded, and every entry has `provenance: real`.

| category | entries |
|---|---:|
| noun | 53 |
| verb (stems, § 26a) | 30 |
| theonym | 18 |
| title / functionary | 10 |
| toponym | 6 |
| adjective | 4 |
| particle | 2 |
| personal name | 1 |

Gloss confidence (from the source's own marking): 99 secure, 14 doubtful
(the source writes "?", „vielleicht“ etc., or the gloss comes only from
a compound), 11 of unknown meaning (the source lists a Hattic word as
„Nomen“ or „u.B.“ without a gloss). 112 entries cite Kammenhuber only,
8 cite both works, and 4 cite Schuster only. Compared with v32, names
are a smaller share: 25 of 124 (theonyms, toponyms, one personal name),
against 41 of 72.

## Fields

* `surface` / `phonemes`: `normalise(keyed)`, split one character per
  phoneme. The normalisation is the corpus's (see
  `corpora/hattic.README.md`): v32's rules plus u̯ → w, i̯ → i, v → w for
  the editions' bound transcription. Inventory:
  `a e h i k l m n p r s t u w z`.
* `gloss`: an English rendering of the source's gloss.
* `attestations`: the form as printed in each source (e.g.
  `kaḫḫir/kāḫer`, `p/u̯eₑl`).
* `citation`: for every source row, `<work>, p. <page>,
  https://archive.org/details/<IA id>/page/n<leaf>`.
* `notes`: lexicon id; per source, the gloss as given (German),
  confidence, a verbatim **OCR quote** from that leaf, and remarks.
* `semantic_field`: `hattic_<category>`. `region`: `central_anatolia`.

### Keying conventions

Where a source gives alternants, the first is keyed, or the one the
source prefers (`kašuḫ`, „oder eher“). Optional letters in parentheses
are dropped (`kun(nu)` → `kun`, `kat(t)aḫ` → `kataḫ`). Kammenhuber's
p/u̯ alternation, which marks an [f] (her „mit [f]“), is keyed with u̯
and so normalises to `w` (`p/u̯eₑl` → `wel`), as v32 mapped "f" → w.
Starred stems (`*dundu`, `*ziḫer`, `*zii̯a`) are stems Kammenhuber
abstracts from prefixed verb forms. They are kept and flagged in
`notes`. Where Kammenhuber and Schuster gloss the same form differently
(`u̯aₐe` „Werkzeug“ vs `vae-` „Haus“; `alep` „Wort“ vs `aleb` „Zunge“),
both glosses are recorded and the entry's `gloss` takes the first row.

## Verification

* `scripts/verify_hattic_sources.py` downloads the IA OCR and checks
  every row: (1) the scan leaf carries the printed page number given,
  and (2) the quote is a verbatim substring of that leaf's OCR. Result
  on 2026-10-03: **134 rows, 0 problems**. A negative control, with one
  quote altered and one page number off by one, was reported as 2
  problems.
* `harness/tests/test_build_hattic.py` asserts a byte-identical rebuild,
  the citation format, and `provenance: real` on every entry.

## LM-corpus overlap

The `hattic` LM is trained on TLHdig running text, not on this pool. 56
of the 124 surfaces also occur as a word type in the LM corpus (2.9% of
its 1,940 types; 9.1% of its tokens). v32 had 72 of 72. Details are in
`corpora/hattic.README.md`.

## Control

`pools/control_hattic_bigram.yaml` (124 entries) is the
bigram-preserving phonotactic control, rebuilt with
`scripts/build_control_pools.py --pool hattic --sampler bigram --suffix _bigram`.

## Gate

`scripts/hattic_gate.py` is the v32 pre-registration. Its
`_N_POOL_ENTRIES = 72` describes the v32 pool and was left unchanged.
Running the gate on this pool is the next ticket, and it needs its own
pre-registration.

## Reproducibility

```bash
python3 scripts/build_hattic_pool.py      # reads corpora/hattic/sources/lexicon.tsv
python3 scripts/verify_hattic_sources.py  # network: re-checks every citation
```
