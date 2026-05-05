# CHIC value-extraction leaderboard (chic-v5; mg-7c6d)

Per-sign tier classification combining four independent lines of evidence into a single proposal-or-no-proposal verdict for every unknown CHIC syllabographic sign. Built by `scripts/build_chic_v5.py`.

## Headline counts

| tier | meaning | n |
|---|---|---:|
| tier-1 | chic-v2 anchor (already established) | 20 |
| tier-2 | ≥3 of 4 lines agree on a phoneme class — **candidate proposal pending domain-expert review** | **3** |
| tier-3 | 2 of 4 lines agree — suggestive but insufficient for a candidate proposal | 29 |
| tier-4 | 1 of 4 lines yields a class — single line of evidence; not a proposal | 17 |
| untiered | no line of evidence yields a class (e.g. very low-frequency signs below the n≥3 threshold) | 27 |
| **total unknowns** | (chic-v1 syllabographic minus chic-v2 anchors) | **76** |

## Lines of evidence

Four independent lines, mechanically derived per the chic-v5 brief (mg-7c6d). Phoneme classes are coarse: `vowel`, `stop`, `nasal`, `liquid`, `fricative`, `glide`. The tier-2 / tier-3 / tier-4 thresholds are exact phoneme-class identity across the lines that yield a vote; lines that are silent (no signal) do not vote.

- **Line 1: distributional plurality.** Per-sign Bhattacharyya similarity to every chic-v2 anchor across four fingerprint dimensions; the top-3 nearest anchors vote on phoneme class by plurality. See `results/chic_anchor_distance_map.md`.
- **Line 2: anchor-distance (strict top-1).** The single closest anchor's phoneme class. Same fingerprint machinery as line 1; differs in the aggregation. Lines 1 and 2 *can* diverge when the top-1 anchor's class differs from the plurality of the top-3.
- **Line 3: substrate-consistency under Eteocretan LM.** For every candidate phoneme value V, mapping = (chic-v2 anchors ∪ {sign → V}) is scored against a class-disjoint deterministic-permutation control mapping. Per-class mean paired_diff picks the winning class. See `results/chic_substrate_consistency.md`.
- **Line 4: cross-script paleographic.** Where the chic-v1 PALEOGRAPHIC_CANDIDATES list flags a Linear A counterpart for the unknown sign with a known/proposed value. **Silent for all 76 unknowns in chic-v5**, because the curated paleographic-candidate list is precisely the seed for the chic-v2 anchor pool — every candidate became an anchor, so by construction no unknown carries a paleographic note. This is a documented methodological limitation: extending line 4 requires hand-curated additional paleographic associations from O&G 1996, Salgarella 2020, etc., which is out of scope for chic-v5 (and would land in chic-v6 if it were prioritised). For the leaderboard, line 4 contributes 0 votes for every unknown sign.

## Eligibility threshold

Unknown signs with corpus frequency below n=3 are marked **untiered** and excluded from line 1 / 2 / 3 voting; their distributional fingerprints are too thin (≤2 occurrences) to support meaningful Bhattacharyya similarity, and their substrate-consistency paired_diffs are below the noise floor. We report the count for transparency rather than dropping the rows.

## Per-sign tier verdict

Sorted by tier (2, 3, 4, untiered), then by sign id. Each row shows the per-line vote and the consensus proposal (where one exists).

| sign | freq | tier | proposed | L1 distributional | L2 anchor-distance | L3 substrate | L4 cross-script |
|---|---:|:--:|:---:|:---:|:---:|:---:|:---:|
| `#001` | 4 | tier-2 | glide | glide | glide | glide | — |
| `#012` | 5 | tier-2 | glide | glide | glide | glide | — |
| `#032` | 9 | tier-2 | stop | stop | stop | stop | — |
| `#002` | 7 | tier-3 | liquid | liquid | liquid | nasal | — |
| `#005` | 48 | tier-3 | stop | stop | stop | nasal | — |
| `#006` | 13 | tier-3 | glide | glide | stop | glide | — |
| `#007` | 8 | tier-3 | vowel | vowel | vowel | nasal | — |
| `#008` | 7 | tier-3 | glide | glide | glide | nasal | — |
| `#009` | 10 | tier-3 | stop | stop | stop | nasal | — |
| `#011` | 24 | tier-3 | liquid | liquid | liquid | glide | — |
| `#017` | 6 | tier-3 | nasal | stop | nasal | nasal | — |
| `#020` | 9 | tier-3 | vowel | vowel | vowel | glide | — |
| `#021` | 3 | tier-3 | nasal | glide | nasal | nasal | — |
| `#027` | 3 | tier-3 | glide | glide | glide | nasal | — |
| `#033` | 3 | tier-3 | glide | stop | glide | glide | — |
| `#037` | 3 | tier-3 | liquid | liquid | liquid | glide | — |
| `#039` | 7 | tier-3 | stop | stop | stop | nasal | — |
| `#040` | 17 | tier-3 | stop | stop | stop | liquid | — |
| `#043` | 6 | tier-3 | liquid | liquid | liquid | glide | — |
| `#045` | 4 | tier-3 | stop | stop | stop | nasal | — |
| `#050` | 23 | tier-3 | glide | glide | stop | glide | — |
| `#055` | 5 | tier-3 | stop | stop | stop | glide | — |
| `#056` | 52 | tier-3 | stop | stop | stop | nasal | — |
| `#058` | 5 | tier-3 | stop | stop | stop | glide | — |
| `#059` | 5 | tier-3 | glide | glide | glide | nasal | — |
| `#060` | 8 | tier-3 | stop | stop | stop | nasal | — |
| `#063` | 7 | tier-3 | glide | glide | liquid | glide | — |
| `#065` | 3 | tier-3 | stop | stop | stop | nasal | — |
| `#066` | 3 | tier-3 | stop | stop | stop | nasal | — |
| `#069` | 3 | tier-3 | stop | stop | stop | glide | — |
| `#072` | 7 | tier-3 | stop | stop | stop | glide | — |
| `#078` | 3 | tier-3 | stop | stop | stop | glide | — |
| `#003` | 4 | tier-4 | glide | liquid | stop | glide | — |
| `#004` | 3 | tier-4 | liquid | liquid | stop | nasal | — |
| `#014` | 4 | tier-4 | glide | stop | liquid | glide | — |
| `#018` | 12 | tier-4 | glide | stop | vowel | glide | — |
| `#023` | 12 | tier-4 | liquid | stop | liquid | nasal | — |
| `#029` | 18 | tier-4 | liquid | liquid | stop | nasal | — |
| `#034` | 41 | tier-4 | liquid | liquid | stop | nasal | — |
| `#036` | 28 | tier-4 | glide | glide | vowel | nasal | — |
| `#046` | 10 | tier-4 | glide | stop | liquid | glide | — |
| `#047` | 19 | tier-4 | liquid | stop | liquid | nasal | — |
| `#051` | 9 | tier-4 | glide | liquid | vowel | glide | — |
| `#052` | 10 | tier-4 | liquid | liquid | vowel | nasal | — |
| `#062` | 11 | tier-4 | glide | glide | vowel | nasal | — |
| `#068` | 10 | tier-4 | liquid | liquid | vowel | nasal | — |
| `#076` | 3 | tier-4 | glide | glide | liquid | nasal | — |
| `#094` | 3 | tier-4 | liquid | liquid | stop | nasal | — |
| `#095` | 6 | tier-4 | glide | glide | stop | liquid | — |
| `#015` | 1 | — | — | — | — | — | — |
| `#022` | 1 | — | — | — | — | — | — |
| `#024` | 1 | — | — | — | — | — | — |
| `#026` | 1 | — | — | — | — | — | — |
| `#030` | 1 | — | — | — | — | — | — |
| `#035` | 2 | — | — | — | — | — | — |
| `#048` | 1 | — | — | — | — | — | — |
| `#064` | 2 | — | — | — | — | — | — |
| `#067` | 1 | — | — | — | — | — | — |
| `#071` | 2 | — | — | — | — | — | — |
| `#074` | 1 | — | — | — | — | — | — |
| `#075` | 1 | — | — | — | — | — | — |
| `#079` | 1 | — | — | — | — | — | — |
| `#080` | 2 | — | — | — | — | — | — |
| `#081` | 1 | — | — | — | — | — | — |
| `#082` | 1 | — | — | — | — | — | — |
| `#083` | 1 | — | — | — | — | — | — |
| `#084` | 1 | — | — | — | — | — | — |
| `#085` | 2 | — | — | — | — | — | — |
| `#087` | 1 | — | — | — | — | — | — |
| `#088` | 2 | — | — | — | — | — | — |
| `#089` | 1 | — | — | — | — | — | — |
| `#090` | 1 | — | — | — | — | — | — |
| `#091` | 1 | — | — | — | — | — | — |
| `#093` | 1 | — | — | — | — | — | — |
| `#096` | 1 | — | — | — | — | — | — |
| `#100` | 1 | — | — | — | — | — | — |

## Tier-2 candidate proposals (detailed)

Each tier-2 row below is a candidate decipherment proposal: ≥3 of 4 lines of evidence (line 4 always silent for chic-v5; agreement is across lines 1, 2, 3) point at the same phoneme class for this sign. **These are candidate proposals pending domain-expert review.**

| sign | freq | proposed class | L1 nearest-anchor | L2 nearest-anchor (sim) | L3 best-value (paired_diff) | L4 paleo |
|---|---:|---|---|---|---|---|
| `#001` | 4 | glide | #057 | `#057` (`je`, BC=0.5533) | `wa` (+0.002212) | — |
| `#012` | 5 | glide | #042 | `#042` (`wa`, BC=0.6611) | `wa` (+0.005331) | — |
| `#032` | 9 | stop | #061 | `#061` (`te`, BC=0.6021) | `ki` (+0.004579) | — |

## Tier-3 suggestive (2 of 4 agree)

Same per-line columns as the main verdict table; the consensus class here has only 2 of the 3 voting lines (line 4 is silent for all chic-v5 unknowns), so it does not clear the tier-2 bar.

| sign | freq | proposed class | L1 distributional | L2 anchor-distance | L3 substrate | L4 cross-script |
|---|---:|---|:---:|:---:|:---:|:---:|
| `#002` | 7 | liquid | liquid | liquid | nasal | — |
| `#005` | 48 | stop | stop | stop | nasal | — |
| `#006` | 13 | glide | glide | stop | glide | — |
| `#007` | 8 | vowel | vowel | vowel | nasal | — |
| `#008` | 7 | glide | glide | glide | nasal | — |
| `#009` | 10 | stop | stop | stop | nasal | — |
| `#011` | 24 | liquid | liquid | liquid | glide | — |
| `#017` | 6 | nasal | stop | nasal | nasal | — |
| `#020` | 9 | vowel | vowel | vowel | glide | — |
| `#021` | 3 | nasal | glide | nasal | nasal | — |
| `#027` | 3 | glide | glide | glide | nasal | — |
| `#033` | 3 | glide | stop | glide | glide | — |
| `#037` | 3 | liquid | liquid | liquid | glide | — |
| `#039` | 7 | stop | stop | stop | nasal | — |
| `#040` | 17 | stop | stop | stop | liquid | — |
| `#043` | 6 | liquid | liquid | liquid | glide | — |
| `#045` | 4 | stop | stop | stop | nasal | — |
| `#050` | 23 | glide | glide | stop | glide | — |
| `#055` | 5 | stop | stop | stop | glide | — |
| `#056` | 52 | stop | stop | stop | nasal | — |
| `#058` | 5 | stop | stop | stop | glide | — |
| `#059` | 5 | glide | glide | glide | nasal | — |
| `#060` | 8 | stop | stop | stop | nasal | — |
| `#063` | 7 | glide | glide | liquid | glide | — |
| `#065` | 3 | stop | stop | stop | nasal | — |
| `#066` | 3 | stop | stop | stop | nasal | — |
| `#069` | 3 | stop | stop | stop | glide | — |
| `#072` | 7 | stop | stop | stop | glide | — |
| `#078` | 3 | stop | stop | stop | glide | — |

## Disagreements with chic-v2 paleographic anchors

By construction, no unknown sign is also an anchor; disagreement here means a chic-v5 line points at a phoneme class that conflicts with a *paleographically-proposed* value for the same sign. Since line 4 is silent for all 76 unknowns in chic-v5, no such disagreement is possible at the per-sign level. The chic-v6 cross-script extension would surface disagreements as a dedicated reporting column.

## Determinism + reproducibility

- No RNG. The brief's 'deterministic seed' for the line-3 control is implemented as a pure sha256-keyed selection from the candidate-value pool.
- Same (CHIC corpus, anchor pool, signs yaml, Eteocretan LM) → byte-identical leaderboard. Re-running the script overwrites this file with the same content.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Decorte, R. (2017, 2018). The First 'European' Writing.
- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* Amsterdam: J. C. Gieben.
- Whittaker, H. (2017). 'Of linguistic alterity in Crete: the Eteocretan inscriptions.' *Scripta Classica Israelica* 36.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
