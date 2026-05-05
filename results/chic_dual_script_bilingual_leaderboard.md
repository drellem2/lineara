# CHIC dual-script bilingual leaderboard (chic-v8; mg-dfcc)

Per the chic-v8 brief: cross-reference the chic-v0 + Linear A v0 corpora for genuinely-dual-script artifacts (artifacts bearing inscriptions in BOTH Cretan Hieroglyphic AND Linear A on the same physical object), then apply the LA-side reading as a fifth line of evidence (L5) constraining CHIC-side phoneme values at parallel positions. Built by `scripts/build_chic_v8.py`.

## 1. The Malia altar stone (Daniel's primary case)

**CHIC #328** — Mallia, offering_table. 16 sign positions, partial transcription confidence. Per the Olivier-Godart 1996 catalog this is the Mallia _table d'offrandes_ (offering table / altar stone), ingested in chic-v0 from the Younger web-edition `misctexts.html` page. Source citation: `http://web.archive.org/web/20220703170656/http://www.people.ku.edu/~jyounger/Hiero/misctexts.html`.

Raw token stream (chic-v0):

```
_062_-034-002-056-070-025-019-051-070-094-034-056-077-049-038-029
```

Rendered under chic-v2 anchors (literal where anchored, `#NNN` where unanchored):

```
[?:#062] #034 #002 #056 ra ta ke #051 ra #094 #034 #056 ma de i #029
```

**The Malia altar stone is CHIC-only in our v0 corpus.** The chic-v0 ingest pulled the inscription from `misctexts.html` as a single-side CHIC entry. The Linear A v0 corpus contains 20 Mallia entries (17 clay tablets + 3 roundels: MA 1a/b/c, MA 2a/b/c, MA 4a/b, MA 6a/b/c/d, MA 9, MA 10a/b/c/d, MA Wc 7, MA Wc <5a>/<5b>); none is a stone vessel or offering table, and no MA-Za inscription has been ingested. Per Olivier & Godart 1996 and Younger's web edition, CHIC #328 is described as bearing CHIC text only — it is treated in scholarship as a **unilingual CHIC inscription**, not as a dual-script artifact.

**Corpus gap.** The most-cited Linear A altar/libation tables (e.g. IO Za 2, KO Za 1, PK Za 11, PK Za 12, TL Za 1) are not in our v0 Linear A corpus either; only PS Za 2 (Psykhro) and SY Za 4 (Syme) are present. None of those is the Malia altar stone or its companion. **A future ingest pass to broaden the v0 LA corpus to the full GORILA Za-series, plus a manual CHIC #312 / #328 audit against print Olivier-Godart 1996 for any commentary-flagged dual- script status, is filed for chic-v9 / corpus-expansion follow-up.**

## 2. Systematic survey for other dual-script artifacts in the v0 corpora

Sites carrying inscriptions in BOTH corpora (potential cross-script co-occurrence):

| site | n CHIC | n LA | CHIC support types | LA support types |
|---|---:|---:|---|---|
| Arkhanes | 4 | 10 | seal | tablet |
| Haghia Triada | 1 | 372 | sealing | graffiti, nodule, roundel, sherd, tablet, vase |
| Knossos | 95 | 31 | bar, crescent, medallion, nodulus, seal, sealing, tablet | architecture, clay_vase, jewellery, pithoid_jar, roundel, sealing, sherd, stone_weight, tablet, vase |
| Mallia | 92 | 20 | bar, chamaizi_vase, cone, crescent, lame, medallion, nodulus, offering_table, pithos, potsherd, seal, sealing, tablet, unknown, vase | roundel, tablet |
| Phaistos | 1 | 63 | sealing | label, nodule, roundel, sealing, tablet |
| Zakros | 4 | 44 | seal, sealing | roundel, tablet |

**Result: no dual-script artifact pair identified in the v0 corpora.** Both corpora are uniquely-keyed (CHIC by Olivier-Godart catalog #; Linear A by GORILA-style site+seq id), with no metadata field in either flagging an artifact as dual-script. The site-and-support-type intersection table above shows where cross-script co-occurrence could IN PRINCIPLE exist — Knossos / Mallia / Phaistos / Haghia Triada / Arkhanes / Zakros all have entries in both — but the support-type distributions barely overlap: Linear A's site-Mallia entries are administrative tablets and roundels, while CHIC Mallia is dominated by sealstones, medallions, and lames; the only LA stone-vessel inscriptions in the v0 corpus are PS Za 2 and SY Za 4, neither of which is at a site shared with CHIC. The CHIC corpus's only stone- vessel inscription is CHIC #328 (Mallia offering table), and it has no Linear A counterpart in the v0 corpus.

Documented dual-script artifacts in scholarship (e.g. some seal-and- sealing pairs from Phaistos and Knossos discussed in Salgarella 2020 §5.3 and Decorte 2017) are either (a) NOT in the v0 corpora because sealstone CMS catalog ingest is itself a separate sub-program, or (b) debated in the underlying scholarship and not unambiguously bilingual. None can be applied here as a load-bearing bilingual constraint without re-doing the underlying ingest.

## 3. Genre-parallel comparison: CHIC #328 vs LA libation tables (informational only)

Even without a true dual-script artifact, an attenuated form of cross- script comparison is possible: CHIC #328 (Mallia offering table) and the LA libation tables PS Za 2 (Psykhro) + SY Za 4 (Syme) are the same artifact CATEGORY (votive stone vessels likely bearing libation / altar formulae). Y. Duhoux and others have hypothesized that the stereotyped Linear A libation formula (`a-ta-i-*301-wa-ja ja-sa-sa-ra-me ja-ti i-da-ma-te ...`) may have a CHIC counterpart on stone- vessel inscriptions. **This is a SCHOLARLY CONJECTURE, not consensus**; we cannot use it as load-bearing first-principles bilingual constraint.

The conjectural genre-parallel comparison is reported here for completeness and for the methodology paper's discipline-protecting framing — readers can see that we considered the broader genre- parallel hypothesis, found it conjectural, and did not rely on it.

**CHIC #328 — Mallia offering table (16 positions):**

| pos | token | rendered (chic-v2) | chic-v5 tier (if unknown) |
|---:|---|---|---|
| 1 | `[?:#062]` | `[?:#062]` | tier-4 (proposed=glide; L1=glide, L2=vowel, L3=nasal) |
| 2 | `#034` | `#034` | tier-4 (proposed=liquid; L1=liquid, L2=stop, L3=nasal) |
| 3 | `#002` | `#002` | tier-3 (proposed=liquid; L1=liquid, L2=liquid, L3=nasal) |
| 4 | `#056` | `#056` | tier-3 (proposed=stop; L1=stop, L2=stop, L3=nasal) |
| 5 | `#070` | `ra` |  |
| 6 | `#025` | `ta` |  |
| 7 | `#019` | `ke` |  |
| 8 | `#051` | `#051` | tier-4 (proposed=glide; L1=liquid, L2=vowel, L3=glide) |
| 9 | `#070` | `ra` |  |
| 10 | `#094` | `#094` | tier-4 (proposed=liquid; L1=liquid, L2=stop, L3=nasal) |
| 11 | `#034` | `#034` | tier-4 (proposed=liquid; L1=liquid, L2=stop, L3=nasal) |
| 12 | `#056` | `#056` | tier-3 (proposed=stop; L1=stop, L2=stop, L3=nasal) |
| 13 | `#077` | `ma` |  |
| 14 | `#049` | `de` |  |
| 15 | `#038` | `i` |  |
| 16 | `#029` | `#029` | tier-4 (proposed=liquid; L1=liquid, L2=stop, L3=nasal) |

**PS Za 2 — Psykhro libation table (16 positions):**

Raw transliteration (LA v0):

```
AB59-AB06-AB28-A301-AB37 / [?] / AB57-AB37 / AB57-AB31-AB31-AB60-AB13 / AB27-AB28-AB44
```

Rendered under Linear-B carryover values (only AB ids in the v0 LA libation tables are mapped; unmapped AB ids and all A-prefixed signs left as-is):

```
ta na i A301 ti / [?] / ja ti / ja sa sa ra me / re i ke
```

**SY Za 4 — Syme libation table (13 positions):**

Raw transliteration (LA v0):

```
AB08-AB59-AB28-A301-AB54-AB57 / AB57-AB28-AB48-AB17 / AB56-AB30-AB40
```

Rendered under Linear-B carryover values (only AB ids in the v0 LA libation tables are mapped; unmapped AB ids and all A-prefixed signs left as-is):

```
a ta i A301 wa ja / ja i AB48 za / pa3 ni wi
```

**Position alignment is conjectural.** The two LA libation tables are 16 and 13 positions long respectively; CHIC #328 is 16. Aligning position-by-position would require either (a) confirmed parallel content (not established for CHIC stone vessels in scholarship), or (b) an alignment algorithm with an external phoneme-class similarity score. Either approach goes beyond the chic-v8 brief's scope, which requires _genuinely-dual-script artifacts with parallel positions_, not genre-parallels with conjectural alignment.

## 4. L5 (LA-constraint) voting outcome

**For each chic-v5 tier-3/4 candidate, an L5 vote is computed only where a parallel LA-side phoneme value at a confident position is available in the same artifact's bilingual reading.**

Because no genuinely-dual-script artifact exists in the v0 corpora, no parallel-position LA-side phoneme value is available for any of the 76 unknown CHIC syllabographic signs. **L5 is silent for all unknowns by corpus state**, mirroring chic-v5's L4 silent-by- construction (the chic-v1 paleographic-candidate list is precisely the seed for the chic-v2 anchor pool). Tier promotion under the 4-of-5 rule therefore reduces to the chic-v5 4-of-4 rule for every sign, which produces no new tier-2 candidates beyond the three already proposed by chic-v5 (#001 → wa, #012 → wa, #032 → ki/stop).

**Per-sign L5 vote summary (76 unknown CHIC syllabographic signs):**

| sign | freq | chic-v5 tier | L5 vote | reason |
|---|---:|---|---|---|
| `#001` | 4 | tier-2 | silent | no genuine dual-script artifact in v0 corpora |
| `#002` | 7 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#003` | 4 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#004` | 3 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#005` | 48 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#006` | 13 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#007` | 8 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#008` | 7 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#009` | 10 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#011` | 24 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#012` | 5 | tier-2 | silent | no genuine dual-script artifact in v0 corpora |
| `#014` | 4 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#015` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#017` | 6 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#018` | 12 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#020` | 9 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#021` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#022` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#023` | 12 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#024` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#026` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#027` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#029` | 18 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#030` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#032` | 9 | tier-2 | silent | no genuine dual-script artifact in v0 corpora |
| `#033` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#034` | 41 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#035` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#036` | 28 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#037` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#039` | 7 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#040` | 17 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#043` | 6 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#045` | 4 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#046` | 10 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#047` | 19 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#048` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#050` | 23 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#051` | 9 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#052` | 10 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#055` | 5 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#056` | 52 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#058` | 5 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#059` | 5 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#060` | 8 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#062` | 11 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#063` | 7 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#064` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#065` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#066` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#067` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#068` | 10 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#069` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#071` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#072` | 7 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#074` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#075` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#076` | 3 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#078` | 3 | tier-3 | silent | no genuine dual-script artifact in v0 corpora |
| `#079` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#080` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#081` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#082` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#083` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#084` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#085` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#087` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#088` | 2 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#089` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#090` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#091` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#093` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#094` | 3 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#095` | 6 | tier-4 | silent | no genuine dual-script artifact in v0 corpora |
| `#096` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |
| `#100` | 1 | — | silent | no genuine dual-script artifact in v0 corpora |

## 5. Per-sign tier-3/tier-4 → tier-2 promotion analysis

Promotion rule (chic-v8 brief): **any 4 of the 5 lines (L1, L2, L3, L4, L5) agreeing on the same coarse phoneme class promotes the sign to tier-2.** With L4 silent for all 76 unknowns by chic-v5 construction and L5 silent for all 76 unknowns by chic-v8 corpus state, the rule reduces to **all 3 of L1+L2+L3 agreeing** — byte-identical to the chic-v5 tier-2 criterion. The chic-v8 bilingual extension cannot promote any chic-v5 tier-3 or tier-4 candidate to tier-2 in the v0 corpus state.

Tier-3 candidates inspected (29; from `results/chic_value_extraction_leaderboard.md`):

`#002, #005, #006, #007, #008, #009, #011, #017, #020, #021, #027, #033, #037, #039, #040, #043, #045, #050, #055, #056, #058, #059, #060, #063, #065, #066, #069, #072, #078`

Tier-4 candidates inspected (17):

`#003, #004, #014, #018, #023, #029, #034, #036, #046, #047, #051, #052, #062, #068, #076, #094, #095`

**No promotion candidate emerges**: L5 is silent for every entry in either set. The 4-of-5 agreement count for every tier-3 sign stays at 2 (its chic-v5 line count); for every tier-4 sign it stays at 1.

## 6. Headline + discipline-protecting framing

**Headline: 0 new tier-2 candidates derived via dual-script bilingual constraint.** The bilingual extension does not produce any promotion under the v0 corpus state, because the chic-v0 + LA-v0 corpora do not contain a genuinely-dual-script artifact (an artifact bearing parallel inscriptions in both Cretan Hieroglyphic and Linear A on the same physical object). The Malia altar stone (CHIC #328), which the chic-v8 brief flagged as the canonical case, is unilingual CHIC in the v0 corpus and in the underlying Olivier-Godart 1996 catalog.

**This is a legitimate publishable null result** (chic-v8 brief, Goal section: `N = 0 new tier-2 candidates: bilingual constraint either doesn't apply (no truly parallel positions) or produces conflicting constraints. Either is informative.`). The methodology paper's framing should:

1. **Disclose the corpus state**: the v0 ingest does not include any genuinely-dual-script artifact, even where scholarship discusses candidates (debated dual-script seals from Phaistos / Knossos etc.).
2. **Position the bilingual extension as a falsifiable additional line of evidence**, contingent on the underlying corpus including genuinely-dual-script artifacts. This is exactly the chic-v5 L4 situation (silent by construction) restated as a corpus-state observation.
3. **Refuse to invoke genre-parallels** (CHIC #328 vs LA libation tables PS Za 2 / SY Za 4) as load-bearing evidence — those are conjectural alignments, not genuine bilingual constraint, and elevating them would re-introduce the motivated-reasoning failure mode the methodology paper has insisted on protecting against since v13's per-sign coherence verdict and v22's external-validation null.
4. **Flag the corpus-expansion path**: a future ingest pass adding the full GORILA Za-series and any genuinely-dual-script artifacts from CMS sealstone catalogs would reactivate the bilingual extension and could in principle produce non-zero L5 votes. Filed under `corpus-expansion` for chic-v9+ / pm-lineara triage.

## 7. Reproducibility

Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0), `corpus/all.jsonl` (LA v0), `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2), `results/chic_value_extraction_leaderboard.md` (chic-v5).

Outputs: this file plus `results/chic_v8_promoted_candidates.md`. Determinism: no RNG, no network, no system clock — same inputs produce byte-identical output across re-runs (verified at chic-v8 build time, 2026-05-05).

Driver: `scripts/build_chic_v8.py`. Re-run with `python3 scripts/build_chic_v8.py`.
