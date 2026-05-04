# Linear-B reference corpus (mg-4664)

External Linear-B / Mycenaean-Greek inscription corpus used to:

1. Train the Mycenaean-Greek char-bigram phoneme prior consumed by
   `external_phoneme_perplexity_v0`
   (`harness/external_phoneme_models/mycenaean_greek.json`).
2. Provide a sister-syllabary positive-control test of the v8 / v9 /
   v10 / v11 framework: the 20 Linear-B carryover anchors
   (`pools/linear_b_carryover.yaml`) are KNOWN-correct readings under
   the Ventris-Chadwick 1956 syllabogram identification, so they MUST
   clear the right-tail bayesian gate when scored under a
   Mycenaean-Greek LM. If they don't, the gate is broken on a known
   case.

## Provenance

* **Source.** [LiBER (Linear B Electronic Resources)](https://liber.cnr.it),
  CNR / Sapienza Università di Roma. Maintainers: Maurizio Del Freo,
  Francesco Di Filippo. The site exposes one HTML page per Linear-B
  tablet under `/tablet/view/<id>` whose `<meta name="description"
  content="<NAME>, <TRANSLITERATION>" />` tag carries the full
  Mycenaean-Greek transliteration.
* **Volume.** LiBER's tablet index (`/database/api/tablet?query=*`)
  enumerates 5,638 inscriptions. Site distribution (LiBER prefixes):
  Knossos (KN, 4,228), Pylos (PY, 1,086), Mycenae (MY, 100), Thebes
  (TH, 75), Tiryns (TI, 72), Khania (KH, 53), and small counts at
  Midea (MI), Malthi (MA), Dimini (DI), Volimidia (VOL), Armenoi (ARM),
  Eleusis (EL), Gla (GLA), Iklaina (IK), Krisa (KR), Mamesz (MAM),
  Medeon (MED), Orchomenos (OR), Pyrasos (PR), Sikyon (SI). Acceptance
  bar of ≥1,000 inscriptions is met decisively.
* **Authoring snapshot.** Tablet index pulled 2026-05-04 against the
  live LiBER endpoint.

## License

LiBER content is © CNR / Sapienza Università di Roma and made
available for academic use under CC BY-NC-SA 4.0
(https://creativecommons.org/licenses/by-nc-sa/4.0/). The underlying
Linear-B inscriptions and their Mycenaean-Greek transliterations are
in the public domain (Bronze Age, ~1450–1180 BCE; Ventris-Chadwick
1956 transliteration values are out of copyright in the relevant
jurisdictions).

This repository commits:
* `corpora/linear_b/inscriptions/<id>.json` and
  `corpora/linear_b/all.jsonl` — per-inscription metadata + the
  parsed lowercase phoneme word list. These are statistical /
  structural derivatives of the LiBER HTML.
* `corpora/linear_b/all.jsonl` size: ~1 MB; well under GitHub's push
  budget.

The `corpora/linear_b/words.txt` flat sorted-unique word list is
gitignored (mirroring the Basque / Etruscan pattern), and the
downstream char-bigram model
(`harness/external_phoneme_models/mycenaean_greek.json`) is committed
as a statistical derivative under the same CC BY-NC-SA 4.0 terms with
attribution to LiBER recorded here.

## Reproducibility

```bash
# 1. Fetch the LiBER tablet index + every per-tablet HTML page.
#    Polite throttled scraper. Re-runs are free (cache-hit).
python3 scripts/fetch_liber.py

# 2. Parse the cached HTML into per-inscription JSON + words.txt.
python3 scripts/parse_liber.py

# 3. Build the char-bigram LM from words.txt.
python3 scripts/build_external_phoneme_models.py --only mycenaean_greek
```

The cache lives at `.cache/liber/tablet/<id>.html` (gitignored).
Re-running the parser on the same cache produces byte-identical
per-inscription JSON, `all.jsonl`, and `words.txt`.

## Per-inscription JSON format

Each `corpora/linear_b/inscriptions/<id>.json` is a single JSON object:

```json
{
  "id": 5713,
  "name": "ARM Z 1",
  "site": "ARM",
  "transliteration": "wi-na-jo",
  "words": ["winajo"]
}
```

* `id` — the LiBER tablet id (integer).
* `name` — the LiBER tablet name, e.g. `KN Da 1396`. Names contain a
  site prefix, a series tag, and a serial number.
* `site` — the site prefix from `name.split()[0]` (`KN`, `PY`, ...).
* `transliteration` — the raw Mycenaean-Greek transliteration as
  emitted by LiBER's meta description tag, including damage /
  editorial markers (`[`, `]`, `_`, `°`, `$vac.`, `$mut.`, etc.) and
  uppercase logograms (`OVIS`, `CROC`, `LANA`, `M`, `P`, `N`).
* `words` — the lowercase phoneme word list extracted from the
  transliteration: each contiguous run of lowercase ASCII letters
  separated by hyphens becomes one entry, with the hyphens stripped.
  Logograms, digits, damage markers, and `*`-numbered unidentified
  signs are dropped. Single-character entries are dropped (no bigram
  information). This is the form that flows into the LM builder.

## What this corpus is *not*

* **Not a Linear-A corpus.** It is the *sister* syllabary, used here
  as a known-correct positive-control reference. Linear-A inscription
  data lives under `corpus/`.
* **Not normalized for cluster differentiation.** Mycenaean-Greek's
  Ventris-Chadwick transliteration uses `q` for labiovelars, `j` for
  /j/, and a few digraphs (`pte`, `dwo`, `nwa`). These are kept
  verbatim in the lowercase word stream rather than being collapsed
  to monograph approximations — the char-bigram model treats them as
  bigrams of the constituent letters, which matches the
  Aquitanian-side convention (`tz`, `ts`, `tx` digraphs likewise
  collapse to bigrams).
* **Not deduplicated by lemma.** Word forms are unique within
  `words.txt` but not lemmatized — `to-ko-do-mo` and `to-ko-do-mo-i`
  count as two forms. The bigram model treats them as separate
  observations, which is correct for char-bigram statistics.

## Acceptance bar

mg-4664 sets ≥1,000 inscriptions. Current build emits the full LiBER
index (5,638 inscriptions); see `all.jsonl` line count for the exact
realized number.
