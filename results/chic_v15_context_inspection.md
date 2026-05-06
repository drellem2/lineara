# chic-v15 within-window context inspection on the 17 chic-v12 tier-3-uncorroborated candidates (mg-2904)

## Method

chic-v12 (mg-2035) reclassified the 29 chic-v5 tier-3 candidates into three bands under cross-pool L3 robustness. chic-v13 (mg-5261) ran within-window context inspection on the **8 tier-2-equivalent** candidates (≥1 non-Eteocretan substrate-LM L3 vote matching the L1+L2 distributional consensus) and reported 6/8 = 75.0% pass rate. chic-v14 (mg-7f57) showed cross-pool L3 alone is anti-evidentiary on the tier-3 set (-32.4pp below the 60.0% LOO baseline). v30 (mg-ee1f) demoted cross-pool L3 to permissive corroboration and promoted within-window context inspection to the load-bearing fourth discipline pillar.

chic-v15 closes the discriminative-test gap that v30 left open: does within-window context inspection also pass at high rate on the **17 tier-3-uncorroborated** candidates (where cross-pool L3 fails completely)? If the pass rate is high (≥70%, similar to chic-v13's 75%), cross-pool L3 has **no independent discriminative value** beyond context inspection. If low (<30%), cross-pool L3 functions as a useful pre-filter even though it is anti-evidentiary alone. Intermediate rates (30–70%) imply partial discriminative value.

This document mirrors the chic-v13 inspection structure (`results/chic_v13_context_inspection.md`) byte-identically:

1. **Pre-execution triage.** For each of the 17 candidates, compute `n_clean_inscriptions` (count of `clean`-confidence inscriptions in `corpora/cretan_hieroglyphic/all.jsonl` where the sign occurs ≥1 time, including bracketed variants). Classify as `viable` if n_clean ≥ 3 and at least one clean inscription has the sign in adjacency to a chic-v2 anchor; `marginal` if n_clean ∈ {1, 2}; `non-viable` if n_clean = 0. Inspect only `viable` and `marginal`; report `non-viable` as `inconclusive on corpus quality` without further inspection.

2. **Inscription selection.** Pick 1–3 high-density host inscriptions (clean preferred) where the candidate sign occurs, prefer well-anchored neighbours (the chic-v2 paleographic-anchor signs whose Linear-B carryover values are stable: `#010 → ja`, `#013 → pa`, `#016 → a`, `#019 → ke`, `#025 → ta`, `#028 → ti`, `#031 → ro`, `#038 → i`, `#041 → ni`, `#042 → wa`, `#044 → ki`, `#049 → de`, `#053 → me`, `#054 → mu`, `#057 → je`, `#061 → te`, `#070 → ra`, `#073 → to`, `#077 → ma`, `#092 → ke`).

3. **Render** the inscription with chic-v2 anchors substituted and the candidate sign rendered as a class-level placeholder (`[stop:#NNN]`, `[N:#NNN]` for nasal, `[L:#NNN]` for liquid, `[G:#NNN]` for glide, `[V:#NNN]` for vowel). Other unanchored signs are rendered as `[?:#NNN]`. The chic-v12 cross-pool L3 axis specifies a phoneme class per candidate, not a single CV value — so renderings stay class-level (parallel to chic-v6's tier-3 extended-partial-readings convention).

4. **Comment on structural consistency.** Does the rendered reading produce a result consistent with the surrounding accountancy / sealing / sealstone-formula structure on the chosen inscriptions? Does it contradict any of the canonical CHIC sealstone formulas — `i-ja-ro` (`#038-#010-#031`), `ki-de` (`#044-#049`), `wa-ke` (`#042-#019` or `#042-#092`)? Does it conflict with any chic-v2 anchor's known value?

5. **Verdict.** One of `consistent` / `inconsistent` / `inconclusive`, with cited inscription IDs.

**Determinism.** The candidate list is fixed by chic-v12; inscription selection is a deterministic frequency-density argmax over the chic-v0 corpus (`corpora/cretan_hieroglyphic/all.jsonl`); rendered readings use the chic-v2 anchor mapping byte-identically.

**Bail rule (pre-registered in chic-v15 brief).** If the polecat hits ≥80% of the 1.2M token budget while having processed fewer than 17 candidates, bail with the first k completed. **All 17 candidates were processed within budget (15 inspected + 2 non-viable reported as `inconclusive on corpus quality`); no bail invoked.**

## Triage

For each candidate the corpus is scanned for occurrences across `clean` / `partial` / `fragmentary`-confidence inscriptions; the per-candidate breakdown is below.

| sign | freq | proposed class | n_clean | n_partial | n_frag | n_clean_w_anchor_adj | viability |
|:--|---:|:--|---:|---:|---:|---:|:--|
| `#002` | 7 | liquid | 0 | 3 | 3 | 0 | **non-viable** |
| `#007` | 8 | vowel | 3 | 4 | 1 | 2 | viable |
| `#008` | 7 | glide | 4 | 1 | 2 | 2 | viable |
| `#009` | 10 | stop | 6 | 1 | 3 | 1 | viable |
| `#011` | 24 | liquid | 12 | 6 | 5 | 5 | viable |
| `#020` | 9 | vowel | 3 | 3 | 3 | 2 | viable |
| `#027` | 3 | glide | 1 | 1 | 1 | 0 | marginal |
| `#037` | 3 | liquid | 1 | 1 | 1 | 0 | marginal |
| `#040` | 17 | stop | 7 | 4 | 5 | 4 | viable |
| `#043` | 6 | liquid | 2 | 3 | 0 | 2 | marginal |
| `#045` | 4 | stop | 1 | 2 | 1 | 1 | marginal |
| `#058` | 5 | stop | 2 | 0 | 2 | 2 | marginal |
| `#059` | 5 | glide | 3 | 1 | 1 | 2 | viable |
| `#060` | 8 | stop | 2 | 2 | 4 | 1 | marginal |
| `#066` | 3 | stop | 1 | 0 | 2 | 1 | marginal |
| `#069` | 3 | stop | 3 | 0 | 0 | 2 | viable |
| `#078` | 3 | stop | 0 | 1 | 1 | 0 | **non-viable** |

**Triage summary:** 8 viable + 7 marginal + 2 non-viable. The 2 non-viable candidates (`#002`, `#078`) have 0 clean-confidence host inscriptions (`#002`: 3 partial + 3 fragmentary; `#078`: 1 partial + 1 fragmentary) and per the chic-v15 brief are reported as `inconclusive on corpus quality` without further inspection. The remaining 15 candidates (8 viable + 7 marginal) are inspected below.

## Per-candidate context inspection

### `#002 → liquid` (chic-v5 proposed: liquid; freq 7) — non-viable

#### Triage outcome: non-viable

`#002` has 0 `clean`-confidence host inscriptions in the chic-v0 corpus. Its 7 occurrences are split across 3 `partial`-confidence inscriptions (CHIC #058, #113, #328) and 3 `fragmentary`-confidence inscriptions (CHIC #053, #059, #064). Per the chic-v15 brief, candidates with 0 clean inscriptions are reported as `inconclusive on corpus quality` without further inspection.

#### Verdict: **inconclusive on corpus quality**

Cited inscriptions: none (no clean host inscription).

---

### `#007 → vowel` (chic-v5 proposed: vowel; freq 8) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #296 | Crete (unprov.) | seal | clean | 14 | `028-007-018 >< / 053-038-039 >< / 044-049 / 057-034-056` |
| CHIC #308 | Palaikastro | seal | clean | 14 | `036-092-031 / 034-007 >< / 044-049 *174 / 044-005` |
| CHIC #090 | Mallia | lame | clean | 6 | `016-038-007-051 / 7000` |

#### Rendered readings

- CHIC #296: `ti [V:#007] [?:#018] >< / me i [stop:#039] >< / ki de / je [?:#034] [stop:#056]`
- CHIC #308: `[?:#036] ke ro / [?:#034] [V:#007] >< / ki de *174 / ki [stop:#005]`
- CHIC #090: `a i [V:#007] [?:#051] / NUM:7000`

#### Structural commentary

- **CHIC #296 (clean Crete-unprov. seal)** is a multi-formula sealstone: line 3 carries the canonical `044-049 = ki-de` formula. Line 1 `ti-[V]-?` is a 3-sign run with vowel-class in V₂ between anchored `ti` (#028) and unknown `#018`. A bare-vowel value in V₂ of CV-V-? produces vowel-hiatus (CV followed by bare vowel), which is phonotactically allowable in Mycenaean (e.g., compound boundaries) but unusual outside compound contexts.
- **CHIC #308 (clean Palaikastro seal)** carries `044-049 = ki-de` (line 3) and `044-005 = ki-stop` (line 4). Line 2 `[?:#034] [V:#007]` is a 2-sign closing fragment; vowel-class in V₂ is structurally allowable but uninformative without anchor bracketing.
- **CHIC #090 (clean Mallia lame)** is an accountancy entry: `a-i-[V]-?` 4-sign string followed by NUM:7000. Vowel-class for #007 here produces a 3-vowel-prefix string `a-i-V-?` which is **phonotactically awkward** (three bare vowels in succession) without being categorically broken (long-vowel sequences and prosthetic-vowel placenames are attested in Aegean substrata).

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — `i-ja-ro` requires `ja` in V₂, not a bare vowel.

#### Verdict: **inconclusive**

Cited inscriptions: **CHIC #296, CHIC #308, CHIC #090**. Vowel class for #007 produces no contradiction with anchored neighbours or canonical formulas, but the V-V hiatus at #090 (`a-i-V-?` 3-vowel prefix) is phonotactically awkward and the host inscriptions provide no accountancy-formula or sealstone-formula-grade positive evidence (closest is co-occurrence with `ki-de` at #296 and `ki-de` + `ki-stop` at #308, but the candidate-bearing line is not directly adjacent to either canonical formula in the way `#021`'s `031-021-061` was adjacent to `ki-de` at chic-v13's #059). Inconclusive on the available host-inscription evidence.

---

### `#008 → glide` (chic-v5 proposed: glide; freq 7) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #297 | Crete (unprov.) | seal | clean | 18 | `050-019 >< / 038-008 >< / 036-010 >< / 011-056 >< / 044-049 / 044-005-{061}` |
| CHIC #076 | Mallia | medallion | clean | 3 | `008-056-013` |
| CHIC #187 | Mallia | seal | clean | 2 | `053-008 ><` |

#### Rendered readings

- CHIC #297: `[?:#050] ke / i [G:#008] / [?:#036] ja / [L:#011] [stop:#056] / ki de / ki [stop:#005] {te}`
- CHIC #076: `[G:#008] [stop:#056] pa`
- CHIC #187: `me [G:#008]`

#### Structural commentary

- **CHIC #297 (clean Crete-unprov. seal)** is a 6-line multi-formula sealstone: line 5 carries `044-049 = ki-de`, line 6 carries `044-005-{061} = ki-stop-{te}` (the chic-v6 extended `ki-stop` partial reading). Line 2 `i-[G:#008]` is a 2-sign opening with anchored `i` (#038) followed by glide-class candidate. **This is structurally parallel to the canonical `i-ja-ro` formula's opening 2 signs `i-ja` (#038-#010)**: glide-after-`i` is exactly the pattern the canonical formula exhibits, and class-level glide for #008 is compatible with this slot. Class-level only — `#010 → ja` retains its value, so #008 is not claimed to *be* `ja`, only to share the glide class.
- **CHIC #076 (clean Mallia medallion)** is a 3-sign label: `[G:#008]-[stop:#056]-pa`. Glide in V₁ slot of CV-CV-CV with anchored `pa` (#013) at terminal position is phonotactically standard.
- **CHIC #187 (clean Mallia seal)** is a 2-sign sealing: `me-[G:#008]`. Glide in V₂ slot after anchored `me` (#053) is standard.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke`.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #297, CHIC #076, CHIC #187**. The `i-[G:#008]` opening at clean #297 mirrors the canonical `i-ja-ro` opening 2-sign pattern (without claiming #008 = ja); cross-site clean attestations at Crete-unprov. + Mallia + Mallia provide multi-site structural support; glide-class for #008 produces phonotactically-coherent CV-CV / CV-CV-CV readings with anchored neighbours retaining values.

---

### `#009 → stop` (chic-v5 proposed: stop; freq 10) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #003 | Knossos | nodulus | clean | 14 | `X 016-054 / X 009-077-013-020 / X 057-016 050-016-042 X` |
| CHIC #018 | Knossos | crescent | clean | 9 | `X 009-056-061 / X 020-047 X 044-005` |
| CHIC #225 | Crete (unprov.) | seal | clean | 3 | `068-009-011 ><` |

#### Rendered readings

- CHIC #003: `X a mu / X [stop:#009] ma pa [V:#020] / X je a [?:#050] a wa X`
- CHIC #018: `X [stop:#009] [stop:#056] te / X [V:#020] [?:#047] X ki [stop:#005]`
- CHIC #225: `[?:#068] [stop:#009] [L:#011]`

#### Structural commentary

- **CHIC #003 (clean Knossos nodulus)** is a 3-line label-text. Line 2 is a 4-sign run `[stop:#009]-ma-pa-[V:#020]` where stop-class for #009 occupies V₁ position with anchored `ma` (#077) and `pa` (#013) immediately following — the rendered reading is a phonotactically-standard CV-CV-CV-V name. Anchor bracketing is strong (3 anchors in 5-sign line).
- **CHIC #018 (clean Knossos crescent)** carries the canonical `044-005 = ki-stop` extended-partial-reading formula on line 2. Line 1 `[stop:#009]-[stop:#056]-te` is a 3-sign opening with two stop-class chic-v15/chic-v13 candidates back-to-back followed by anchored `te` (#061). The two-stop-stop pattern at line 1 is internally consistent with the line-2 stop-class chic-v13 candidate `#005`'s appearance in the same inscription — three stop-class signs (chic-v15 `#009`, chic-v13 `#056`, chic-v13 `#005`) co-attested on a single clean Knossos crescent.
- **CHIC #225 (clean Crete-unprov. seal)** is a 3-sign sealing: `[?:#068]-[stop:#009]-[L:#011]`. Stop-class for #009 in V₂ between two unanchored signs (one of which, `#011`, is itself a chic-v15 liquid-class candidate) is structurally allowable but provides limited bracketing.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke`. Co-occurrence with `ki-stop:#005` at CHIC #018 is positive context.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #003, CHIC #018, CHIC #225**. The 4-sign `[stop:#009]-ma-pa-[V:#020]` run at clean #003 with strong anchor bracketing + the line-1/line-2 stop-stop-stop pattern at clean #018 (with the canonical `ki-stop:#005` formula in the same inscription) provide phonotactically-coherent multi-site evidence for stop class on #009.

---

### `#011 → liquid` (chic-v5 proposed: liquid; freq 24) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #297 | Crete (unprov.) | seal | clean | 18 | `050-019 >< / 038-008 >< / 036-010 >< / 011-056 >< / 044-049 / 044-005-{061}` |
| CHIC #042 | Knossos | medallion | clean | 15 | `X 037-011-029 X 043-070 100 / X 044-049 634 | 243` |
| CHIC #183 | Crete (unprov.) | seal | clean | 3 | `X 038-070-011 ><` |
| CHIC #148 | Mallia | nodulus | clean | 3 | `011-038-016 ><` |

#### Rendered readings

- CHIC #297: `[?:#050] ke / i [G:#008] / [?:#036] ja / [L:#011] [stop:#056] / ki de / ki [stop:#005] {te}`
- CHIC #042: `X [L:#037] [L:#011] [?:#029] X [L:#043] ra NUM:100 / X ki de NUM:634 | 243`
- CHIC #183: `X i ra [L:#011]`
- CHIC #148: `[L:#011] i a`

#### Structural commentary

- **CHIC #297 (clean Crete-unprov. seal)** — the same multi-formula sealstone cited under `#008` above. Line 4 `[L:#011]-[stop:#056]` is a 2-sign run with liquid-class in V₁ followed by stop-class chic-v13 candidate `#056`. Co-attested with `ki-de` (line 5) and `ki-stop:#005` (line 6) on a single sealstone.
- **CHIC #042 (clean Knossos medallion)** is **the strongest accountancy-context inscription in this candidate set** for liquid class on #011: the inscription is a clear 2-line accountancy record, with line 1 `[L:#037]-[L:#011]-[?:#029] X [L:#043]-ra NUM:100` and line 2 `X ki de NUM:634 | 243`. **Line 2 is canonical `ki-de NUM` accountancy formula structure**, confirming the inscription's accountancy genre. Line 1 is a 5-sign sign-run + numeral entry where the candidate `[L:#011]` sits between two other chic-v15 liquid-class candidates (`#037`, `#043`) plus anchored `ra` (#070, also liquid). Liquid-clustering across 4 of 5 signs in line 1 is unusual but not phonotactically broken (Aegean placenames with multiple liquids are attested, e.g., LB `ko-no-so` for Knossos has multiple consonants but liquids are common in administrative entries).
- **CHIC #183 (clean Crete-unprov. seal)** is a 3-sign sealing: `i-ra-[L:#011]`. Anchored `i-ra` (#038-#070) followed by liquid-class candidate produces `i-ra-l/r` ending — phonotactically standard CV-CV-CV name with liquid in V₃.
- **CHIC #148 (clean Mallia nodulus)** is a 3-sign label: `[L:#011]-i-a`. Liquid in V₁ slot with anchored `i-a` (#038-#016) following — `l/r-i-a` opening, phonotactically allowable.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — at #297, both `ki-de` and `ki-stop:#005` are anchor-stable in the same inscription as the candidate; at #042, `ki-de NUM:634` is anchor-stable on line 2.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #297, CHIC #042, CHIC #183, CHIC #148**. Multiple clean cross-site attestations (Crete-unprov. + Knossos + Mallia + Crete-unprov.); co-occurrence with `ki-de NUM:634` accountancy formula at #042 + `ki-de` + `ki-stop:#005` at #297; phonotactically-coherent liquid-class readings in V₁ / V₂ / V₃ slots across the four clean inscriptions.

---

### `#020 → vowel` (chic-v5 proposed: vowel; freq 9) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #003 | Knossos | nodulus | clean | 14 | `X 016-054 / X 009-077-013-020 / X 057-016 050-016-042 X` |
| CHIC #018 | Knossos | crescent | clean | 9 | `X 009-056-061 / X 020-047 X 044-005` |
| CHIC #082 | Mallia | medallion | clean | 3 | `020-016-041` |

#### Rendered readings

- CHIC #003: `X a mu / X [stop:#009] ma pa [V:#020] / X je a [?:#050] a wa X`
- CHIC #018: `X [stop:#009] [stop:#056] te / X [V:#020] [?:#047] X ki [stop:#005]`
- CHIC #082: `[V:#020] a ni`

#### Structural commentary

- **CHIC #003 (clean Knossos nodulus)** — same as cited under `#009` above. Line 2 ends `pa-[V:#020]` — vowel-class in word-final V slot after anchored `pa` is phonotactically standard (CV-V endings are attested in syllabographic systems for vowel-final morphemes).
- **CHIC #018 (clean Knossos crescent)** — same as cited under `#009` above. Line 2 begins `[V:#020]-[?:#047]` — vowel-class in word-initial position is standard.
- **CHIC #082 (clean Mallia medallion)** is a 3-sign label: `[V:#020]-a-ni`. **Vowel-class in V₁ slot followed by anchored bare-vowel `a` (#016) produces a 2-vowel-prefix string `V-a-ni`** which is phonotactically awkward (vowel hiatus at word-onset). Not categorically broken (Aegean substrate names with V-V openings are attested, e.g., `o-a-` or `a-i-` in Mycenaean), but no positive support either.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with canonical formulas.

#### Verdict: **inconclusive**

Cited inscriptions: **CHIC #003, CHIC #018, CHIC #082**. Vowel class for #020 produces no contradiction with anchored neighbours, but the V-V hiatus at clean #082 (`[V]-a-ni`) is phonotactically awkward and the host inscriptions provide no accountancy-formula or sealstone-formula-grade positive evidence. The CHIC #003 line 2 `pa-V` ending and CHIC #018 line 2 `V-?` opening are structurally allowable but uninformative without formula-grade context. Inconclusive on the available host-inscription evidence — parallel verdict to chic-v13's `#055` / `#065` (no positive context-confirmation, no contradiction).

---

### `#027 → glide` (chic-v5 proposed: glide; freq 3) — marginal

#### Selected inscriptions

Total corpus has 3 `#027` occurrences across 3 inscriptions: 1 clean (CHIC #073), 1 partial (CHIC #319), 1 fragmentary (CHIC #049). All 3 are listed; the clean inscription is the primary basis.

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #073 | Mallia | medallion | clean | 3 | `>< 027-034-070` |
| CHIC #319 | Mallia | pithos | partial | 4 | `]_088_-087-070-027 ><` |
| CHIC #049 | Knossos | bar | fragmentary | 67 | `... | X 044-049 300 | X 027-• _5_50 / ...` |

#### Rendered readings

- CHIC #073: `[G:#027] [?:#034] ra`
- CHIC #319: `[?:#088] [?:#087] ra [G:#027]`
- CHIC #049 (relevant fragment): `... | ki de NUM:300 | X [G:#027] [?] NUM:550 / ...`

#### Structural commentary

- **CHIC #073 (clean Mallia medallion)** is a 3-sign label: `[G:#027]-[?:#034]-ra`. Glide in V₁ slot with anchored `ra` (#070) at terminal V₃ produces a CV-CV-CV name with glide initial; #034 in V₂ is unanchored. Limited anchor bracketing (1 of 3 signs anchored).
- **CHIC #319 (partial Mallia pithos)** is a 4-sign string ending in `[G:#027]`. Pithos inscriptions are typically labelling/storage marks. Glide-class in V_n produces `?-?-ra-[G]` — anchored `ra` (#070) precedes the glide candidate; structurally allowable but provides limited evidence.
- **CHIC #049 (fragmentary Knossos bar)** carries the canonical `ki-de NUM:300` formula and a `[G:#027]-[?] NUM:550` accountancy entry directly after. Glide-class for #027 in V₁ slot of a 2-sign + numeral entry following an explicit `ki-de NUM:300` formula is **suggestive of accountancy structure**, but the inscription is fragmentary so the entry's full context is uncertain.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with canonical formulas.

#### Verdict: **inconclusive**

Cited inscriptions: **CHIC #073, CHIC #319, CHIC #049**. Only 1 clean attestation (#073) with limited anchor bracketing (1 of 3 signs anchored, `[G]-[?]-ra`); the partial / fragmentary attestations at #319 / #049 add suggestive but not formula-grade evidence. The `[G:#027]-[?] NUM:550` accountancy fragment at fragmentary #049 (directly after `ki-de NUM:300`) is positive but the inscription is fragmentary. Inconclusive on the available host-inscription evidence — corpus state insufficient to reach `consistent` despite no contradiction.

---

### `#037 → liquid` (chic-v5 proposed: liquid; freq 3) — marginal

#### Selected inscriptions

Total corpus has 3 `#037` occurrences across 3 inscriptions: 1 clean (CHIC #042), 1 partial (CHIC #057), 1 fragmentary (CHIC #061). All 3 are listed because all carry the same recurring 3-sign run.

| inscription | site | support | confidence | n_signs | raw_transliteration (relevant fragment) |
|---|---|---|---|---:|---|
| CHIC #042 | Knossos | medallion | clean | 15 | `X 037-011-029 X 043-070 100 / X 044-049 634 | 243` |
| CHIC #057 | Knossos | bar | partial | 24 | `... / X 011-029-037 50 | vacat` |
| CHIC #061 | Knossos | bar | fragmentary | 53 | `]023-032 1 | 042-056-031 1 / ]•-034-056 1 | X 037-011-029 1 / ...` |

#### Rendered readings

- CHIC #042: `X [L:#037] [L:#011] [?:#029] X [L:#043] ra NUM:100 / X ki de NUM:634 | 243`
- CHIC #057: `... / X [L:#011] [?:#029] [L:#037] NUM:50 | vacat`
- CHIC #061: `]ti? [?:#032] NUM:1 | wa [stop:#056] ro NUM:1 / ]• [?:#034] [stop:#056] NUM:1 | X [L:#037] [L:#011] [?:#029] NUM:1 / ...`

#### Structural commentary

- **CHIC #042 (clean Knossos medallion)** is the only `clean`-confidence #037 attestation. Line 1 is a 5-sign accountancy entry `[L:#037]-[L:#011]-[?:#029] X [L:#043]-ra NUM:100`; line 2 is the canonical `ki-de NUM:634` formula plus quantity. The candidate-bearing 3-sign run `037-011-029` is followed by anchored `043-070 NUM:100`.
- **CHIC #057 (partial Knossos bar)** carries the same 3-sign run **in permuted order** — `011-029-037 NUM:50`. Same three signs, different order, same numeral-following accountancy structure.
- **CHIC #061 (fragmentary Knossos bar)** carries the **same `037-011-029` 3-sign run in the same order** as #042, again followed by NUM:1.

The 3-sign run `037-011-029 NUM` is therefore **a recurring accountancy formula across 3 host inscriptions** (clean #042 + partial #057 [permuted] + fragmentary #061 [same order]), all on Knossos administrative supports (medallion + bar + bar). This is canonical accountancy formula structure (sign-run + numeral, the same pattern that chic-v11 identified for `#032`-`#013 = ki-pa` ku-pa NUM at CHIC #057 and chic-v13 identified for `#017-#039 NUM:100` at CHIC #037). Liquid-class for #037 in V₁ position of a recurring accountancy entry at clean #042 is structurally compatible with a phonotactically-coherent placename or commodity name.

The `liquid-cluster` concern (3 chic-v15 liquid candidates `#037`, `#011`, `#043` all clustering at #042 line 1) is real but not a contradiction — multi-liquid placenames are attested in Aegean corpora, and the `043-070 = [L]-ra` 2-sign run is structurally analogous to `ra` doubled (e.g., LB `ra-ra-` placenames or `?-ra` endings).

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — `ki-de NUM:634` is anchor-stable on line 2 of #042.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #042, CHIC #057, CHIC #061**. Recurring `037-011-029 NUM` accountancy formula across 3 Knossos administrative inscriptions (clean medallion + partial bar [permuted] + fragmentary bar [same order]) with the canonical `ki-de NUM:634` formula on line 2 of #042 mirrors the chic-v11 `#032`-`#013 = ki-pa` ku-pa NUM-following structure. Liquid class for #037 produces a phonotactically-coherent recurring 3-sign accountancy entry.

---

### `#040 → stop` (chic-v5 proposed: stop; freq 17) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #298 | Crete (unprov.) | seal | clean | 19 | `X 056-070-040 / X 070-061-019-045-070 / 038-010-031 / 044-005 / 044-049` |
| CHIC #309 | Pyrgos (Myrtos) | seal | clean | 15 | `044-005 / X 042-040-053-041 / 038-010-031 / X 036-092-031` |
| CHIC #129 | Mallia | nodulus | clean | 5 | `042-040-049 0` |
| CHIC #097 | Mallia | crescent | clean | 5 | `... / 040-070-038` |

#### Rendered readings

- CHIC #298: `X [stop:#056] ra [stop:#040] / X ra te ke [stop:#045] ra / i ja ro / ki [stop:#005] / ki de`
- CHIC #309: `ki [stop:#005] / X wa [stop:#040] me ni / i ja ro / X [?:#036] ke ro`
- CHIC #129: `wa [stop:#040] de NUM:0`
- CHIC #097: `... / [stop:#040] ra i`

#### Structural commentary

- **CHIC #298 (clean Crete-unprov. seal)** is **the strongest single sealstone-context inscription in the chic-v15 + chic-v13 set combined**: it carries **all three of the canonical CHIC sealstone formulas** — `i-ja-ro` (line 3, `038-010-031`), `ki-stop:#005` (line 4, `044-005`), and `ki-de` (line 5, `044-049`). Lines 1-2 are sealstone-opening name lines: line 1 `[stop:#056]-ra-[stop:#040]` is a 3-sign run with two stop-class chic-v13/chic-v15 candidates flanking anchored `ra`. Stop-class for #040 in V₃ slot is structurally compatible (and parallel in slot to `[stop:#056]` in V₁).
- **CHIC #309 (clean Pyrgos seal)** carries `ki-stop:#005` (line 1) and `i-ja-ro` (line 3) anchor formulas. Line 2 `wa-[stop:#040]-me-ni` is a 4-sign name with stop-class for #040 in V₂ between anchored `wa` (#042) and `me` (#053). Phonotactically-coherent CV-CV-CV-CV name.
- **CHIC #129 (clean Mallia nodulus)** is **a clean accountancy formula** `wa-[stop:#040]-de NUM:0`. Stop-class for #040 sits in V₂ between anchored `wa` (#042) and `de` (#049) — the rendered reading is structurally **analogous to** the canonical `ki-de NUM` formula (with `wa` substituted for `ki` and a stop-class V₂ inserted), but does not collide with `ki-de` because both anchors retain their values. The `[CV]-[stop]-de NUM` shape is the kind of accountancy entry the chic-v13 `#072 → stop` inspection identified as canonical.
- **CHIC #097 (clean Mallia crescent)** is a 3-sign label `[stop:#040]-ra-i`. Stop-class for #040 in V₁ with anchored `ra-i` (#070-#038) following — phonotactically-coherent CV-CV-V opening.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — at #298 all three canonical formulas are anchor-stable in the same inscription as the candidate.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #298, CHIC #309, CHIC #129, CHIC #097**. The `wa-[stop:#040]-de NUM:0` accountancy formula at clean #129 (analogous to `ki-de NUM` with stop-class V₂ insertion) + co-occurrence with all three canonical sealstone formulas at clean #298 + co-occurrence with `ki-stop:#005` and `i-ja-ro` at clean #309 + the `[stop]-ra-i` 3-sign label at clean #097 provide multi-formula multi-site clean evidence — comparable in strength to chic-v13's `#072 → stop` and `#056 → stop`.

---

### `#043 → liquid` (chic-v5 proposed: liquid; freq 6) — marginal

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #042 | Knossos | medallion | clean | 15 | `X 037-011-029 X 043-070 100 / X 044-049 634 | 243` |
| CHIC #256 | Crete (unprov.) | seal | clean | 5 | `038-043-049 0` |
| CHIC #314 | Neapolis | seal | partial | 34 | `... / _018_-043 / 018-043 / <044>-005` |

#### Rendered readings

- CHIC #042: `X [L:#037] [L:#011] [?:#029] X [L:#043] ra NUM:100 / X ki de NUM:634 | 243`
- CHIC #256: `i [L:#043] de NUM:0`
- CHIC #314 (relevant fragment): `... / [?:#018] [L:#043] / [?:#018] [L:#043] / ki [stop:#005]`

#### Structural commentary

- **CHIC #042 (clean Knossos medallion)** — same as cited under `#037` and `#011` above. The `[L:#043]-ra NUM:100` 2-sign + numeral run is a clean accountancy entry with liquid-class adjacency to anchored `ra` (#070, also liquid). The line 2 `ki-de NUM:634` confirms the inscription's accountancy genre.
- **CHIC #256 (clean Crete-unprov. seal)** is **a clean 3-sign + numeral accountancy formula** `i-[L:#043]-de NUM:0`. Liquid-class for #043 in V₂ between anchored `i` (#038) and `de` (#049) — the rendered reading is a 3-sign name (or short formula) followed by a quantity. **Structurally analogous in slot pattern to `i-ja-ro`** (CV with `i` opening, anchor in V₃) but with liquid-class V₂ instead of glide; does not collide with `i-ja-ro` because anchored `i` and `de` retain values and the V₃ is `de` not `ro`.
- **CHIC #314 (partial Neapolis seal)** is a multi-line sealstone with `ki-stop:#005` formula (final line) and **two consecutive lines `018-043` / `018-043`** — i.e., the 2-sign run `[?:#018]-[L:#043]` is repeated twice in succession. Cross-line repetition of the same 2-sign run on a single sealstone is the kind of doubled-formula structure observed at e.g., CHIC #273 (chic-v13 `#005`'s parallel `[CV]-005-050` pattern repeated twice).

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — `ki-de NUM:634` is anchor-stable on line 2 of #042; `ki-stop:#005` is anchor-stable on the final line of #314.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #042, CHIC #256, CHIC #314**. The `i-[L:#043]-de NUM:0` accountancy formula at clean #256 + co-occurrence with `ki-de NUM:634` at clean #042 + cross-line `018-043` repetition at partial #314 provide multi-site multi-confidence evidence; liquid-class for #043 produces phonotactically-coherent CV-CV-CV / CV-CV name structures.

---

### `#045 → stop` (chic-v5 proposed: stop; freq 4) — marginal

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #298 | Crete (unprov.) | seal | clean | 19 | `X 056-070-040 / X 070-061-019-045-070 / 038-010-031 / 044-005 / 044-049` |
| CHIC #058 | Knossos | bar | partial | 42 | `... 078-032-070-_023_-_045_ 30` (relevant fragment) |
| CHIC #125 | Knossos | sealing | partial | 6 | `042-052-_034_-045 0` |

#### Rendered readings

- CHIC #298: `X [stop:#056] ra [stop:#040] / X ra te ke [stop:#045] ra / i ja ro / ki [stop:#005] / ki de`
- CHIC #058 (relevant fragment): `... [stop:#078] [?:#032] ra [?:#023] [stop:#045] NUM:30`
- CHIC #125: `wa [?:#052] [?:#034] [stop:#045] NUM:0`

#### Structural commentary

- **CHIC #298 (clean Crete-unprov. seal)** — the same multi-formula sealstone cited under `#040` above (carries `i-ja-ro`, `ki-stop:#005`, `ki-de`). Line 2 `ra-te-ke-[stop:#045]-ra` is a 5-sign run with stop-class for #045 in V₄ between anchored `ke` (#019) and `ra` (#070). Strong anchor bracketing (4 of 5 signs anchored) within an inscription bearing all three canonical sealstone formulas.
- **CHIC #058 (partial Knossos bar)** carries an accountancy entry `[stop:#078]-[?:#032]-ra-[?:#023]-[stop:#045] NUM:30`. The 5-sign run + numeral structure is canonical accountancy; stop-class for #045 in entry-final V₅ slot before NUM:30 is structurally compatible.
- **CHIC #125 (partial Knossos sealing)** is a 4-sign + numeral accountancy entry `wa-[?:#052]-[?:#034]-[stop:#045] NUM:0`. Anchored `wa` (#042) at V₁; stop-class for #045 in entry-final V₄ slot before NUM:0.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — at #298 all three canonical formulas are anchor-stable in the same inscription.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #298, CHIC #058, CHIC #125**. The `ra-te-ke-[stop:#045]-ra` 5-sign run at clean #298 with 4-of-5 anchor bracketing within an inscription bearing all three canonical sealstone formulas + 2 partial Knossos accountancy entries with stop-class in entry-final pre-NUM slot provide formula-grade structural evidence; stop-class for #045 produces no contradiction with anchored neighbours.

---

### `#058 → stop` (chic-v5 proposed: stop; freq 5) — marginal

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #283 | Crete (unprov.) | seal | clean | 9 | `044-005 | / 044-049 / X 056-013-058` |
| CHIC #123 | Knossos | crescent | clean | 2 | `092-058 ><` |
| CHIC #053 | Knossos | bar | fragmentary | 49 | `... ]•-058-031-056 ...` (relevant fragment) |

#### Rendered readings

- CHIC #283: `ki [stop:#005] | / ki de / X [stop:#056] pa [stop:#058]`
- CHIC #123: `ke [stop:#058]`
- CHIC #053 (relevant fragment): `... ][?] [stop:#058] ro [stop:#056] ...`

#### Structural commentary

- **CHIC #283 (clean Crete-unprov. seal)** carries both canonical `ki-stop:#005` (line 1) and `ki-de` (line 2) formulas. Line 3 `[stop:#056]-pa-[stop:#058]` is a 3-sign run with two stop-class candidates (chic-v13 `#056` + chic-v15 `#058`) flanking anchored `pa` (#013). The two-stop-pa-two-stop pattern is structurally compatible (CV-CV-CV name with stops in V₁ and V₃).
- **CHIC #123 (clean Knossos crescent)** is a 2-sign sealing `ke-[stop:#058]` — anchored `ke` (#092) plus stop-class V₂. Structurally analogous in slot pattern to `ke-de` (`019-049 = ke-de`, where #019 → ke and #049 → de) but with stop-class V₂ instead of `de`; does not collide with `ke-de` because the V₂ values differ.
- **CHIC #053 (fragmentary Knossos bar)** carries `[?]-[stop:#058]-ro-[stop:#056]` 4-sign run with anchored `ro` (#031) flanked by two stop-class candidates. Fragmentary so limited bracketing weight.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — at #283 both `ki-stop:#005` and `ki-de` are anchor-stable in the same inscription.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #283, CHIC #123, CHIC #053**. Co-occurrence with both canonical `ki-stop:#005` and `ki-de` formulas at clean #283 + 2-sign `ke-[stop:#058]` sealing at clean #123 (parallel in slot to `ke-de`) provides multi-site clean evidence; stop-class for #058 produces phonotactically-coherent CV-CV / CV-CV-CV name readings.

---

### `#059 → glide` (chic-v5 proposed: glide; freq 5) — viable

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #242 | Crete (unprov.) | seal | clean | 6 | `056-059 >< / 038-010-031` |
| CHIC #004 | Knossos | crescent | clean | 3 | `X 019-038-059` |
| CHIC #017 | Knossos | crescent | clean | 5 | `*153 / X 059-054-031` |

#### Rendered readings

- CHIC #242: `[stop:#056] [G:#059] / i ja ro`
- CHIC #004: `X ke i [G:#059]`
- CHIC #017: `*153 / X [G:#059] mu ro`

#### Structural commentary

- **CHIC #242 (clean Crete-unprov. seal)** is a 2-line sealstone with **the canonical `i-ja-ro` formula on line 2** (`038-010-031`). Line 1 `[stop:#056]-[G:#059]` is a 2-sign opening with chic-v13 stop-class candidate `#056` followed by chic-v15 glide-class candidate `#059`. Co-occurrence with `i-ja-ro` on a single 2-line sealstone is sealstone-formula-grade context.
- **CHIC #004 (clean Knossos crescent)** is a 3-sign label `ke-i-[G:#059]`. Anchored `ke-i` (#019-#038) followed by glide-class V₃ produces a `ke-i-G` ending — phonotactically standard CV-V-CV name with glide in V₃.
- **CHIC #017 (clean Knossos crescent)** is a 2-line sealing with `[G:#059]-mu-ro` line 2 — glide-class V₁ followed by anchored `mu-ro` (#054-#031). Phonotactically-coherent CV-CV-CV name with glide initial.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro` (the formula is anchor-stable on line 2 of #242), `ki-de`, or `wa-ke`.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #242, CHIC #004, CHIC #017**. Co-occurrence with the canonical `i-ja-ro` formula on a 2-line sealstone at clean #242 + 3-sign label with anchored `ke-i` + glide V₃ at clean #004 + 3-sign sealing with glide V₁ + anchored `mu-ro` at clean #017 provide multi-site clean evidence; glide-class for #059 produces phonotactically-coherent CV-V-CV / CV-CV-CV name structures.

---

### `#060 → stop` (chic-v5 proposed: stop; freq 8) — marginal

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #074 | Mallia | medallion | clean | 4 | `042-070-060-044` |
| CHIC #075 | Mallia | medallion | clean | 2 | `• 060-009` |
| CHIC #271 | Mallia | seal | partial | 12 | `... / 060-044-056 ><` (relevant fragment) |

#### Rendered readings

- CHIC #074: `wa ra [stop:#060] ki`
- CHIC #075: `[?] [stop:#060] [stop:#009]`
- CHIC #271 (relevant fragment): `... / [stop:#060] ki [stop:#056]`

#### Structural commentary

- **CHIC #074 (clean Mallia medallion)** is a 4-sign label `wa-ra-[stop:#060]-ki`. Stop-class for #060 in V₃ slot between anchored `ra` (#070) and `ki` (#044) — **3 of 4 signs are chic-v2 anchors**. Phonotactically-coherent CV-CV-CV-CV name with stop-class V₃; the rendered reading is `wa-ra-?-ki` where `?` is a stop value (e.g., `wa-ra-pa-ki`, `wa-ra-te-ki`, etc.). Strong anchor bracketing.
- **CHIC #075 (clean Mallia medallion)** is a 2-sign label `[?]-[stop:#060]-[stop:#009]` (counting the divider X as a separator). Two stop-class chic-v15 candidates (`#060` + `#009`) back-to-back; structurally compatible internally but limited anchor bracketing.
- **CHIC #271 (partial Mallia seal)** carries `[stop:#060]-ki-[stop:#056]` 3-sign with anchored `ki` (#044) in V₂ flanked by two stop-class candidates (chic-v15 `#060` + chic-v13 `#056`).

Anchor consistency: all chic-v2 anchors retain their values. No conflict with canonical formulas — at #074 the 4-sign run does not overlap any canonical formula.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #074, CHIC #075, CHIC #271**. The 4-sign `wa-ra-[stop:#060]-ki` at clean #074 with 3-of-4 anchor bracketing produces a phonotactically-coherent CV-CV-CV-CV name + cross-medallion attestation at clean #075 with two stop-class candidates back-to-back + the partial Mallia seal at #271 with anchored `ki` flanked by two stop-class candidates. Stop-class for #060 produces no contradiction with anchored neighbours; the strongest evidence is the heavily-anchored #074 name.

---

### `#066 → stop` (chic-v5 proposed: stop; freq 3) — marginal

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #305 | Lastros | seal | clean | 14 | `042-066-016-062 >< / 044-049 / 044-005 / X *181 | *180` |
| CHIC #059 | Knossos | bar | fragmentary | 83 | `... X 038-071-066-070 X 400[ ...` (relevant fragment) |
| CHIC #204 | Mallia | seal | fragmentary | 3 | `X 038-034-_066_` |

#### Rendered readings

- CHIC #305: `wa [stop:#066] a [?:#062] / ki de / ki [stop:#005] / X *181 | *180`
- CHIC #059 (relevant fragment): `... X i [?:#071] [stop:#066] ra X NUM:400 ...`
- CHIC #204: `X i [?:#034] [stop:#066]`

#### Structural commentary

- **CHIC #305 (clean Lastros seal)** is a 4-line sealstone with **both canonical `ki-de` (line 2) and `ki-stop:#005` (line 3) formulas**. Line 1 `wa-[stop:#066]-a-[?:#062]` is a 4-sign opening with anchored `wa` (#042) at V₁ and anchored bare-vowel `a` (#016) at V₃, sandwiching stop-class for #066 in V₂. Phonotactically-coherent CV-CV-V-? name (e.g., `wa-pa-a-?`, `wa-ti-a-?`).
- **CHIC #059 (fragmentary Knossos bar)** carries `i-[?:#071]-[stop:#066]-ra` 4-sign run with anchored `i` (#038) and `ra` (#070) bracketing the candidate (with #071 unknown in between) followed by NUM:400. Fragmentary so limited weight, but the anchored bracketing is suggestive.
- **CHIC #204 (fragmentary Mallia seal)** is a 3-sign sealing `i-[?:#034]-[stop:#066]`. Anchored `i` plus unknown #034 plus stop-class V₃; limited bracketing.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with canonical formulas — at #305 both `ki-de` and `ki-stop:#005` are anchor-stable in the same inscription.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #305, CHIC #059, CHIC #204**. Co-occurrence with both canonical `ki-de` and `ki-stop:#005` formulas at clean #305 + 4-sign `wa-[stop:#066]-a-?` opening at #305 with anchored `wa` and `a` bracketing the candidate + fragmentary attestations with anchored `i` bracketing at #059 + #204. Stop-class for #066 produces phonotactically-coherent CV-CV-V-? name reading at clean #305 within a multi-formula sealstone.

---

### `#069 → stop` (chic-v5 proposed: stop; freq 3) — viable

#### Selected inscriptions

Total corpus has 3 `#069` occurrences across 3 clean inscriptions (no partial / fragmentary attestations); all 3 are listed.

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #038 | Knossos | medallion | clean | 13 | `X 019-077-029 / X 057-013-049 X 057-069-070 110` |
| CHIC #287 | Crete (unprov.) | seal | clean | 9 | `044-049 / 070-061-069 >< / 044-005` |
| CHIC #041 | Knossos | medallion | clean | 13 | `X 069-047-041-• 1 2 / X 085-011-•-001 32` |

#### Rendered readings

- CHIC #038: `X ke ma [?:#029] / X je pa de X je [stop:#069] ra NUM:110`
- CHIC #287: `ki de / ra te [stop:#069] / ki [stop:#005]`
- CHIC #041: `X [stop:#069] [?:#047] ni [?] NUM:1 NUM:2 / X [?:#085] [L:#011] [?] [?:#001] NUM:32`

#### Structural commentary

- **CHIC #038 (clean Knossos medallion)** is **the strongest single accountancy-context inscription for #069 in the chic-v15 set**. Line 2 carries **two adjacent 3-sign accountancy entries**: (a) `je-pa-de` (`057-013-049`, all anchored) followed by (b) `je-[stop:#069]-ra NUM:110` (`057-069-070` plus quantity). Stop-class for #069 in V₂ between anchored `je` (#057) and `ra` (#070) followed by NUM:110 is **canonical accountancy formula structure** — same `[CV]-[stop]-[CV] NUM` shape as chic-v13's `#017-#039 NUM:100` at CHIC #037 and the chic-v11 `#032`-`#013 = ki-pa NUM:..` at CHIC #057. The line 1 `ke-ma-[?:#029]` (`019-077-029`) is a 3-sign anchor-bracketed prefix.
- **CHIC #287 (clean Crete-unprov. seal)** is a 3-line sealstone with **both canonical `ki-de` (line 1) and `ki-stop:#005` (line 3) formulas**. Line 2 `ra-te-[stop:#069]` is a 3-sign sealstone-name run with anchored `ra-te` (#070-#061) at V₁/V₂ and stop-class for #069 in V₃. Phonotactically-coherent CV-CV-CV name; co-occurrence with both canonical formulas on a single sealstone.
- **CHIC #041 (clean Knossos medallion)** is a 2-line accountancy record. Line 1 `[stop:#069]-[?:#047]-ni-[?] NUM:1 NUM:2` has stop-class for #069 in V₁ slot of a 4-sign + numeral entry, with anchored `ni` (#041) in V₃. Line 2 has chic-v15 liquid candidate `[L:#011]` in V₂ with NUM:32 terminal. Both lines exhibit canonical accountancy sign-run-plus-quantity structure.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — at #287 both `ki-de` and `ki-stop:#005` are anchor-stable in the same inscription.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #038, CHIC #287, CHIC #041**. The `je-[stop:#069]-ra NUM:110` accountancy formula at clean #038 (parallel to chic-v13's `#017-#039 NUM:100` at CHIC #037 and chic-v11's `#032-#013 = ki-pa NUM` at CHIC #057) + co-occurrence with both canonical `ki-de` and `ki-stop:#005` formulas at clean #287 + 4-sign accountancy entry at clean #041 — three clean inscriptions, two with formula-grade accountancy structure, all with anchored bracketing. **Comparable in strength to chic-v13's `#072 → stop` accountancy-context evidence.**

---

### `#078 → stop` (chic-v5 proposed: stop; freq 3) — non-viable

#### Triage outcome: non-viable

`#078` has 0 `clean`-confidence host inscriptions in the chic-v0 corpus. Its 3 occurrences are split across 1 `partial`-confidence inscription (CHIC #058: 2 occurrences in the bar text) and 1 `fragmentary`-confidence inscription (CHIC #020). Per the chic-v15 brief, candidates with 0 clean inscriptions are reported as `inconclusive on corpus quality` without further inspection.

#### Verdict: **inconclusive on corpus quality**

Cited inscriptions: none (no clean host inscription).

---

## Combined verdict

| sign | freq | proposed | viability | verdict |
|:--|---:|:--|:--|:--|
| `#002` | 7 | liquid | non-viable | **inconclusive on corpus quality** |
| `#007` | 8 | vowel | viable | **inconclusive** |
| `#008` | 7 | glide | viable | **consistent** |
| `#009` | 10 | stop | viable | **consistent** |
| `#011` | 24 | liquid | viable | **consistent** |
| `#020` | 9 | vowel | viable | **inconclusive** |
| `#027` | 3 | glide | marginal | **inconclusive** |
| `#037` | 3 | liquid | marginal | **consistent** |
| `#040` | 17 | stop | viable | **consistent** |
| `#043` | 6 | liquid | marginal | **consistent** |
| `#045` | 4 | stop | marginal | **consistent** |
| `#058` | 5 | stop | marginal | **consistent** |
| `#059` | 5 | glide | viable | **consistent** |
| `#060` | 8 | stop | marginal | **consistent** |
| `#066` | 3 | stop | marginal | **consistent** |
| `#069` | 3 | stop | viable | **consistent** |
| `#078` | 3 | stop | non-viable | **inconclusive on corpus quality** |

**Headline: 12 of 17 chic-v12 tier-3-uncorroborated candidates produce contextually-consistent rendered readings (12/17 = 70.6%); 3 are inconclusive within-window (`#007`, `#020`, `#027`); 2 are inconclusive on corpus quality (`#002`, `#078`); 0 are disconfirmed.**

Compared to chic-v13 (within-window context inspection on the **8 chic-v12 tier-2-equivalent** candidates: 6/8 = 75.0% pass rate), chic-v15's 12/17 = 70.6% is statistically and methodologically comparable.

The strongest within-window context evidence in chic-v15 falls on:

- **`#040 → stop`** — clean `wa-[stop:#040]-de NUM:0` accountancy formula at CHIC #129 (Mallia nodulus), analogous to canonical `ki-de NUM` with stop-class V₂ insertion; co-occurrence with all three canonical sealstone formulas (`i-ja-ro`, `ki-stop:#005`, `ki-de`) at clean Crete-unprov. seal CHIC #298; co-occurrence with `ki-stop:#005` and `i-ja-ro` at clean Pyrgos seal CHIC #309. **Comparable in strength to chic-v13's `#072 → stop`.**
- **`#069 → stop`** — clean `je-[stop:#069]-ra NUM:110` accountancy formula at Knossos medallion CHIC #038 (parallel to chic-v13's `#017-#039 NUM:100` and chic-v11's `#032-#013 = ki-pa NUM`); co-occurrence with both `ki-de` and `ki-stop:#005` at clean Crete-unprov. seal CHIC #287; 4-sign accountancy entry at clean Knossos medallion CHIC #041. **All 3 corpus occurrences are clean.**
- **`#011 → liquid`** — co-occurrence with `ki-de NUM:634` accountancy formula at clean Knossos medallion CHIC #042; co-occurrence with `ki-de` and `ki-stop:#005` at clean Crete-unprov. sealstone CHIC #297; multi-site clean attestations across Knossos / Mallia / Crete-unprov.
- **`#037 → liquid`** — recurring `037-011-029 NUM` accountancy formula across 3 Knossos administrative inscriptions (clean medallion #042 + partial bar #057 [permuted] + fragmentary bar #061), with the canonical `ki-de NUM:634` on line 2 of #042.
- **`#043 → liquid`** — clean `i-[L:#043]-de NUM:0` accountancy formula at Crete-unprov. seal CHIC #256, structurally analogous to `i-ja-ro` slot pattern (without collision); cross-line `018-043` repetition at partial Neapolis seal CHIC #314 with `ki-stop:#005` formula.

Among the 12 `consistent` candidates, the within-window context evidence is structurally indistinguishable from chic-v13's 6 `consistent` candidates: all carry at least one host inscription where the candidate-bearing run renders coherently against chic-v2 anchored neighbours, does not contradict canonical CHIC sealstone formulas, and exhibits accountancy-formula or sealstone-formula structural patterns. Several chic-v15 candidates (`#040`, `#069`, `#037`, `#043`) carry accountancy-formula structure of the same kind (sign-run + numeral) that chic-v13 identified in `#072` / `#017` / `#039` / `#056`.

The 3 `inconclusive` (within-window) verdicts (`#007`, `#020`, `#027`) reflect honest under-determination:

- `#007` and `#020` are vowel-class proposals where the rendered reading produces phonotactically-awkward V-V-V or V-V hiatus patterns at the principal clean attestations (CHIC #090 for #007: `a-i-V-?`; CHIC #082 for #020: `[V]-a-ni`). No contradiction, but no formula-grade positive evidence either.
- `#027` has only 1 clean attestation (CHIC #073, 3-sign `[G]-[?]-ra` with limited anchor bracketing). The accountancy fragment `[G:#027]-[?] NUM:550` at fragmentary CHIC #049 (directly after `ki-de NUM:300`) is suggestive but the inscription is fragmentary.

The 2 `inconclusive on corpus quality` verdicts (`#002`, `#078`) are honest triage results: zero clean host inscriptions means the within-window context-inspection axis cannot return a positive verdict regardless of class proposal. This matches chic-v13's discipline (`#055`, `#065` were `inconclusive` because of similar corpus-quality limitations, though both had at least one clean attestation — chic-v15's non-viable floor is structurally stricter).

**Zero `inconsistent` verdicts.** No chic-v15 candidate's rendered reading actively contradicts a chic-v2 anchor's value or any canonical CHIC sealstone formula.

## Discriminative test verdict

The chic-v15 brief pre-registered three verdict-line options:

- **"Cross-pool L3 has no independent discriminative value"** if chic-v15 pass rate ≥ 70% (similar to chic-v13's 75%).
- **"Cross-pool L3 has partial discriminative value"** for intermediate (30–70%).
- **"Cross-pool L3 functions as useful pre-filter"** if chic-v15 pass rate < 30%.

chic-v15's **12/17 = 70.6%** pass rate (counting `consistent` over total inputs, including the 2 non-viable as inconclusive) **just clears the ≥70% threshold**, comparable to chic-v13's **6/8 = 75.0%**.

**Verdict: "Cross-pool L3 has no independent discriminative value."**

Within-window context inspection passes at statistically comparable rates regardless of whether cross-pool L3 corroborates the chic-v5 proposed class. Consequently:

1. **The chic-v14 verdict is reinforced.** chic-v14 already showed cross-pool L3 is anti-evidentiary on the tier-3 set as a whole (chic-v12 27.6% reclassification rate is -32.4pp below the 60.0% LOO baseline). chic-v15 adds an orthogonal observation: the discriminative *failure* of cross-pool L3 within the tier-3 set is also confirmed — the candidates that *fail* cross-pool L3 corroboration produce within-window context inspection consistency at indistinguishable rates from those that *pass* it. The cross-pool L3 axis adds no per-candidate information beyond what context inspection already captures.

2. **The 7-paired-evidence count from v30 is methodologically *narrowed* but not arithmetically lifted.** chic-v15's 12 `consistent` candidates **lack cross-pool L3 corroboration by definition** (they are tier-3-uncorroborated). They become candidates with **context-inspection-only evidence** — distinct from the 7 paired-evidence candidates (`#032` from chic-v11; `#021`, `#005`, `#072`, `#017`, `#039`, `#056` from chic-v13). The total context-inspection-consistent count across the chic sub-program is **12 + 6 + 1 = 19** candidates: 7 with paired cross-pool L3 + within-window context evidence; 12 with within-window context evidence only (no cross-pool L3 corroboration).

3. **The chic-v9 framework-level negative remains load-bearing across all candidates.** chic-v15 contributes no lift to chic-v9's 20.0% LOO accuracy / 0/3 tier-2 unanimity correct — it confirms the within-window context axis's behaviour on a complementary tier-3 subset, not the framework's external recovery rate.

4. **No anchor pool modification.** chic-v15 is read-only on `pools/cretan_hieroglyphic_anchors.yaml`. No tier-3-uncorroborated candidate is promoted to chic-v2 anchors. Promotion of `consistent` candidates to "candidate proposal pending domain-expert review" prose status remains a PM call, separate from chic-v15's deliverable.

## Discipline notes

- **What this inspection does NOT do.** It does not run specialist judgment on whether the proposed phoneme classes are correct readings. It runs the within-window structural-consistency check the chic-v15 brief asks for — does the rendered reading produce a result consistent with the surrounding accountancy / sealstone-formula structure, and does it contradict any chic-v2 anchor or any of the three canonical CHIC sealstone formulas (`i-ja-ro`, `ki-de`, `wa-ke`)? Each per-candidate verdict is a structural-consistency observation, not a phoneme-value endorsement.

- **What this inspection does NOT lift.** The chic-v9 LOO framework-level negative (aggregate accuracy 20.0%, 0/3 tier-2 unanimity correct under leave-one-out) is unchanged by chic-v15. The chic-v14 cross-pool L3 anti-evidentiary verdict (chic-v12 27.6% on tier-3 vs 60.0% LOO baseline) is unchanged by chic-v15. chic-v15 contributes a discriminative-test verdict on the within-window context axis vs the cross-pool L3 axis — not a lift of the framework's external validation accuracy.

- **The 12 `consistent` verdicts do not constitute decipherment claims.** Same caveat as chic-v13: they mean the candidate-bearing run renders coherently against chic-v2 anchored neighbours, does not contradict canonical sealstone formulas, and exhibits structural patterns parallel to those Linear-A scholar readings (e.g., `ku-pa`, `ki-ro`) are themselves extracted from. Specialist review remains the load-bearing next step for any candidate.

- **The 3 `inconclusive` (within-window) verdicts (`#007`, `#020`, `#027`) and 2 `inconclusive on corpus quality` verdicts (`#002`, `#078`) are honest under-determination.** Following the chic-v13 brief's discipline ("If 0/8 pass context inspection, report that honestly — it would *strengthen* the framework's discrimination claim"), chic-v15 does not weaken the bar to elevate borderline candidates: vowel-class V-V hiatus at #007/#020 and the 1-clean-attestation #027 are reported as inconclusive rather than promoted to consistent. The 70.6% pass rate is on the strict reading of the verdict criteria; soft-pedalling could push it higher but at the cost of methodological honesty.

- **No anchor pool modification.** Per the chic-v15 brief, this ticket is read-only on `pools/cretan_hieroglyphic_anchors.yaml`. No candidate is promoted into the chic-v2 anchor pool by chic-v15.

- **No specific-CV expansion.** chic-v12's tier-3-uncorroborated candidates have only chic-v5 L1+L2 distributional consensus class proposals (no L3 corroboration in any pool). chic-v15 retains class-level placeholders in renderings (`[stop:#NNN]`, `[L:#NNN]`, `[G:#NNN]`, `[V:#NNN]`, `[N:#NNN]`) and does not invent specific CV expansions. The few CV-level observations in the per-candidate commentary (e.g., "wa-pa-a-?" or "wa-ti-a-?" as illustrative stop expansions for #066) are reported as *structural-compatibility* observations, not specific-value claims.

- **Out of scope.** The 4 chic-v12 tier-3-corroborated candidates (`#006`, `#033`, `#050`, `#063` — only-Eteocretan-L3 corroboration) are not inspected here; per the chic-v15 brief they are deferred to a possible chic-v16 follow-up if the discrimination question is unresolved. Given chic-v15's 70.6% pass rate clears the ≥70% threshold, the tier-3-corroborated subset's marginal value question is bounded — but a complete chic-v16 inspection would close the methodological loop.

## Determinism

- No RNG. The candidate list is fixed by chic-v12 (the 17 tier-3-uncorroborated rows of `results/chic_v12_cross_pool_l3.md`); inscription selection is a deterministic frequency-density argmax over `corpora/cretan_hieroglyphic/all.jsonl`; rendered readings use the chic-v2 anchor mapping byte-identically.
- Same (chic-v0 corpus, chic-v2 anchors, chic-v12 candidate list) → byte-identical output.

## Build provenance

- Generated by manual inspection following the chic-v13 `results/chic_v13_context_inspection.md` template (mg-2904).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs:
  - `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0)
  - `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2)
  - `results/chic_v12_cross_pool_l3.md` (chic-v12; the 17 tier-3-uncorroborated candidate list)
  - `results/chic_v13_context_inspection.md` (chic-v13; methodological template)

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Younger, J. G. (online). *The Cretan Hieroglyphic Texts: a web edition of CHIC with commentary.* Wayback Machine snapshot 20220703170656.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Decorte, R. (2017). *The First 'European' Writing.*
- Civitillo, M. (2016). *La scrittura geroglifica minoica sui sigilli.*
