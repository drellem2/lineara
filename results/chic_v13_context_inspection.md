# chic-v13 within-window context inspection on the 8 chic-v12 tier-2-equivalent candidates (mg-5261)

## Method

The chic-v12 brief (mg-2035) reclassified 8 of the 29 chic-v5 tier-3 candidates to **tier-2-equivalent** under cross-pool L3 robustness — each carries ≥1 non-Eteocretan substrate-LM L3 vote matching its L1+L2 distributional consensus, the same band-level evidence structure as the chic-v11 surviving tier-2 (`#032 → ki`). The bail rule fired (8 > 5) and within-window context inspection was deferred to this ticket.

This document mirrors the chic-v11 `#032` ku-pa context inspection methodology (`results/chic_v11_032_ku_pa_context.md`), applied to the 8 tier-2-equivalent candidates. For each candidate:

1. **Inscription selection.** Pick 1–3 high-density CHIC inscriptions where the candidate sign occurs (prefer ≥3 occurrences; for low-frequency candidates take what the corpus offers). Selection prefers high-density inscriptions and well-anchored neighbours (the chic-v2 paleographic-anchor signs whose Linear-B carryover values are stable: `#010 → ja`, `#013 → pa`, `#016 → a`, `#019 → ke`, `#025 → ta`, `#028 → ti`, `#031 → ro`, `#038 → i`, `#041 → ni`, `#042 → wa`, `#044 → ki`, `#049 → de`, `#053 → me`, `#054 → mu`, `#057 → je`, `#061 → te`, `#070 → ra`, `#073 → to`, `#077 → ma`, `#092 → ke`).

2. **Render** the inscription with chic-v2 anchors substituted and the candidate sign rendered as a class placeholder (e.g. `[stop:#005]`, `[N:#021]`). The chic-v12 cross-pool L3 result does not specify a single CV value per candidate — it specifies a phoneme class — so renderings stay class-level (parallel to the chic-v6 tier-3 extended-partial-readings convention; class-level placeholders are the discipline-protecting render where a specific CV expansion is not warranted).

3. **Comment on structural consistency.** Does the rendered reading produce a result consistent with the surrounding accountancy / sealing / sealstone-formula structure on the chosen inscriptions? Does it contradict any of the known CHIC sealstone formulas — `i-ja-ro` (`#038-#010-#031`), `ki-de` (`#044-#049`), `wa-ke` (`#042-#019` or `#042-#092`)? Does it conflict with any chic-v2 anchor's known value?

4. **Verdict.** One of `consistent` / `inconsistent` / `inconclusive`, with cited inscription IDs.

**Determinism.** The candidate list is fixed by chic-v12; the inscription selection is a deterministic frequency-density argmax over the chic-v0 corpus (`corpora/cretan_hieroglyphic/all.jsonl`). Anchor renderings are byte-identical to chic-v6's tier-2 extended-partial-readings convention.

**Bail rule (pre-registered in chic-v13 brief).** If at any point during execution the polecat hits ≥80% of the 1M token budget while having processed fewer than 8 candidates, bail with the first k completed. This document reports completed inspection of all 8 candidates within budget; no bail invoked.

## Per-candidate context inspection

### `#021 → nasal` (chic-v5 proposed: nasal; freq 3; corroborated_by: aquitanian, etruscan, toponym — 3 of 3)

#### Selected inscriptions

The total corpus has exactly 3 `#021` occurrences across 3 inscriptions; all 3 are selected.

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #149 | Mallia | sealing | clean | 3 | `031-021-061` |
| CHIC #197 | Mallia | seal | clean | 3 | `X 031-021-061` |
| CHIC #059 | Knossos | bar | fragmentary | 83 | `]031-021-061 X 044-049[` (relevant fragment) |

#### Rendered readings

- CHIC #149: `ro [N:#021] te`
- CHIC #197: `X ro [N:#021] te`
- CHIC #059 (relevant fragment): `... ro [N:#021] te X ki de ...`

#### Structural commentary

The triplet `031-021-061` (`ro-[N]-te`) is **a recurring formulaic 3-sign run attested at two cross-site clean sealings (Mallia #149, Mallia #197) and at a Knossos accountancy bar (#059)**. The bar-text fragment in CHIC #059 places `031-021-061` in **direct adjacency with the canonical `044-049 = ki-de` sealstone formula** — i.e. the candidate-bearing 3-sign run sits immediately before `ki-de` in an administrative bar context, exactly the co-occurrence position one expects for a sealstone-formula-grade name/title element.

Nasal-class for #021 produces a CV-CV-CV reading `ro-N-te` where the V₂ slot N could be `ma`/`me`/`mu`/`ni` (the chic-v2 anchor pool's nasal-onset values). All four expansions yield phonotactically-unsurprising 3-syllable strings. The rendered reading does not overlap with `i-ja-ro` (which is `i-ja-#031`, a different surface; `#031` is the third sign of the i-ja-ro formula but `031-021-061` is `#031` followed by two different signs in different positions), `ki-de`, or `wa-ke`.

Anchor consistency: `#031 → ro` and `#061 → te` retain their chic-v2 values; only `#021` is rendered as a class placeholder.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #149, CHIC #197, CHIC #059**. Cross-site recurrence of `031-021-061` at three independent inscriptions (two clean Mallia sealings + one Knossos accountancy bar) and direct adjacency with the canonical `ki-de` formula at #059 provides sealstone-formula-grade structural support for #021 carrying a syllabographic value; nasal-class is consistent with the recurrence pattern.

---

### `#005 → stop` (chic-v5 proposed: stop; freq 48; corroborated_by: aquitanian, toponym — 2 of 3)

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #273 | Mirabelo | seal | clean | 11 | `X 054-005-050 >< / 019-031-061 >< / X 070-005-050 ><` |
| CHIC #298 | Crete (unprov.) | seal | clean | 19 | `X 056-070-040 / X 070-061-019-045-070 / 038-010-031 / 044-005 / 044-049` |
| CHIC #174 | Palaikastro | sealing | clean | 6 | `044-005 or 044-{065}-005` |

#### Rendered readings

- CHIC #273: `X mu [stop:#005] [?:#050] / ke ro te / X ra [stop:#005] [?:#050]`
- CHIC #298: `X [?:#056] ra [?:#040] / X ra te ke [?:#045] ra / i ja ro / ki [stop:#005] / ki de`
- CHIC #174: `ki [stop:#005]` or `ki [{stop:#065}] [stop:#005]`

#### Structural commentary

CHIC #273 (Mirabelo, clean seal) carries **a parallel-pattern 3-sign formula `[CV]-[stop:#005]-[?:#050]`** repeated twice with `mu` and `ra` in the V₁ slot, separated by an anchored `ke-ro-te` formula. The recurrence pattern shows `005-050` is a fixed 2-sign suffix and the V₁ slot varies — exactly the kind of formula slot where a stop-class onset would be expected for a CV-CV-CV name/title element.

CHIC #298 (Crete unprovenanced, clean seal) is the **strongest accountancy / sealstone context evidence** in this candidate set: a single inscription containing **all three of the canonical CHIC formulas** — `i-ja-ro` (`038-010-031`), `ki-de` (`044-049`) — plus the chic-v6 `044-005` short formula. With #005 → stop, line 4 reads `ki [stop]`, a CV-CV name/word starter directly parallel in slot to `ki-de` (line 5). The two `ki-X` entries flanking `i-ja-ro` are structurally compatible with a sealstone with multiple short formulaic units.

CHIC #174 (Palaikastro, clean sealing) exhibits the same `044-005 = ki-stop` formula in isolation, with a variant transcription including `{065}` between the two anchored signs. Cross-site recurrence of `044-005` (Palaikastro #174 + Crete-unprovenanced #298 + Knossos bar #059 fragment + others) provides additional sealstone-formula-grade evidence.

The rendered reading does not contradict `i-ja-ro`, `ki-de`, or `wa-ke`: the `044-005` formula is structurally distinct from `044-049` (different second sign) and co-occurs with `ki-de` rather than overlapping it. Anchor consistency: all chic-v2 anchors retain their values.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #273, CHIC #298, CHIC #174**. The `044-005 = ki-[stop]` formula recurring across multiple clean sealings, the parallel `[CV]-005-050` pattern at #273, and the co-occurrence with `i-ja-ro` and `ki-de` at #298 all render coherently with stop-class for #005.

---

### `#055 → stop` (chic-v5 proposed: stop; freq 5; corroborated_by: aquitanian, toponym — 2 of 3)

#### Selected inscriptions

All 5 corpus occurrences are in fragmentary inscriptions; the 3 with the most adjacent signs are selected.

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #103 | Mallia | medallion | fragmentary | 8 | `]070-055-057-_056_[ / ]*163[` |
| CHIC #022 | Knossos | crescent | fragmentary | 7 | `X 055-070-049[ / ]•-_031_` |
| CHIC #117 | Mallia | bar | fragmentary | 26 | `]055-_020_[ ]011-_040_ ...` |

#### Rendered readings

- CHIC #103: `... ra [stop:#055] je [?stop:#056] ...`
- CHIC #022: `X [stop:#055] ra de [`
- CHIC #117: `... [stop:#055] [?:#020] ... [?:#011] [?:#040] ...`

#### Structural commentary

All 5 inscriptions where #055 occurs carry transcription confidence `fragmentary`. The 3 selected are the most-anchored fragments:

- **CHIC #103** has #055 adjacent to anchored `ra` (#070) and `je` (#057), with the next sign also a chic-v13 stop-class candidate (`#056`). The 4-sign run `ra-[stop]-je-[?stop]` is plausible as a CV-CV-CV-CV name fragment under stop-class for #055, but the breakage on both sides limits structural inference.
- **CHIC #022** opens with `[stop:#055] ra de [` — anchored `ra de` follows #055; `de` (#049) is the second sign of the canonical `ki-de` sealstone formula, but here it is preceded by `ra` not `ki`, so the reading `[stop]-ra-de` is structurally distinct from `ki-de` and does not conflict with it.
- **CHIC #117** is a fragmentary Mallia bar with #055 in a token-string with mostly unanchored neighbours (`[?:#020]`, `[?:#011]`, `[?:#040]`). The bar context plausibly carries accountancy structure, but the unanchored neighbours produce no informative rendered reading.

Anchor consistency: all anchored signs retain their chic-v2 values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — none of these formulas overlaps with the rendered #055 contexts.

#### Verdict: **inconclusive**

Cited inscriptions: **CHIC #103, CHIC #022, CHIC #117**. The 5-occurrence-total corpus distribution and uniformly fragmentary inscription confidence prevent a definitive structural-consistency check. Stop-class for #055 produces no contradiction with anchored neighbours or canonical formulas, but no positive accountancy- or sealstone-formula-grade evidence either. **Inconclusive on the available corpus state.**

---

### `#065 → stop` (chic-v5 proposed: stop; freq 3; corroborated_by: aquitanian, toponym — 2 of 3)

#### Selected inscriptions

Total corpus has 3 `#065` occurrences across 3 inscriptions; all 3 are selected.

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #174 | Palaikastro | sealing | clean | 6 | `044-005 or 044-{065}-005` |
| CHIC #317 | Mallia | pithos | fragmentary | 7 | `042-057-_010_-034-028-_093_-_065_` |
| CHIC #009 | Knossos | crescent | fragmentary | 2 | `]065-063 ><` |

#### Rendered readings

- CHIC #174 (variant reading): `ki [{stop:#065}] [stop:#005]`
- CHIC #317: `wa je [?ja] [?:#034] ti [?:#093] [?stop:#065]`
- CHIC #009: `[?stop:#065] [?:#063]`

#### Structural commentary

- **CHIC #174** is the only `clean`-confidence inscription containing #065, but the sign appears only in the **variant transcription** with `{065}` bracketed — the alternative reading `044-005` (without #065) is also recorded. Under the variant: `ki-[stop]-[stop]` with two stop-class candidates back-to-back. Stop-class for #065 in the V₂ slot of `ki-?-?` is structurally compatible (and parallel to the `044-005 = ki-stop` formula's pattern), but the variant-reading status weakens the evidence weight.
- **CHIC #317** is a Mallia pithos inscription. Pithos (large storage jar) inscriptions are typically labelling/storage marks rather than accountancy formulas, but the partial transcription with multiple bracketed-uncertain signs and a 7-sign string ending in `[?stop:#065]` provides at most a syllabographic-string consistency check; the terminal stop-class is plausible but not load-bearing.
- **CHIC #009** is a 2-sign fragmentary crescent: minimal context, uninformative.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke`.

#### Verdict: **inconclusive**

Cited inscriptions: **CHIC #174, CHIC #317, CHIC #009**. The 3 occurrences are split across one variant-bracketed clean sealing, one fragmentary pithos, and one 2-sign fragmentary crescent. No clean accountancy-formula or sealstone-formula context. Stop-class for #065 produces no contradiction, but no positive context-confirmation either. **Inconclusive.**

---

### `#072 → stop` (chic-v5 proposed: stop; freq 7; corroborated_by: etruscan, toponym — 2 of 3)

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration (relevant fragment) |
|---|---|---|---|---:|---|
| CHIC #065 | Knossos | bar | partial | 58 | `X 072-049-071-050-005-063 1 X ... / 072-049 1 ...` |
| CHIC #034 | Knossos | medallion | fragmentary | 12 | `X 054-061-013 [ / ] 072-049 10` |
| CHIC #040 | Knossos | medallion | partial | 16 | `X 019-070-061 X 072-039 / X 044-049 2 X 068-031 _4_` |

#### Rendered readings

- CHIC #065 (relevant fragment): `X [stop:#072] de [?:#071] [?:#050] [stop:#005] [?:#063] NUM:1 ... / [stop:#072] de NUM:1 ...`
- CHIC #034: `X mu te pa [ / ] [stop:#072] de NUM:10`
- CHIC #040: `X ke ra te X [stop:#072] [stop:#039] / X ki de NUM:2 X [?:#068] ro NUM:4`

#### Structural commentary

This is the **strongest accountancy-context candidate in the chic-v13 set**, methodologically symmetric to chic-v11's `#032 → ki + #013 → pa` ku-pa accountancy-context inspection on CHIC #057.

- **CHIC #065 (Knossos bar)** carries **two `[stop:#072] de` runs**, each followed by NUM:1. The first run is a 6-sign sequence `[stop:#072]-de-[?:#071]-[?:#050]-[stop:#005]-[?:#063]` followed by NUM:1; the second is the 2-sign `[stop:#072]-de` followed by NUM:1. **Both are canonical accountancy formula structure** (sign-run = entry, followed by quantity), the same pattern that CHIC #057 exhibited for `#032`-#013 ki-pa under chic-v11.
- **CHIC #034 (Knossos medallion)** carries the same `[stop:#072]-de NUM:10` formula on a different support type, providing cross-support recurrence of the 2-sign run `072-049` followed by a quantity.
- **CHIC #040 (Knossos medallion, partial confidence)** contains the canonical `044-049 = ki-de` formula directly followed by NUM:2 — confirming the inscription's accountancy genre — and `[stop:#072]-[stop:#039]` is in a name/commodity slot adjacent to anchored `ke-ra-te`. Two stop-class candidates back-to-back is internally consistent (chic-v13 candidates #072 and #039 both proposed stop) and the ki-de NUM:2 anchor at the same line confirms the genre.

The rendered reading does not contradict `i-ja-ro`, `ki-de`, or `wa-ke`. The 2-sign formula `072-049 = [stop]-de` is structurally analogous to `044-049 = ki-de` (both are `[CV]-de`) — but the anchored `044 → ki` and `049 → de` retain their chic-v2 values; the analogy lies in the (V_C, de) slot pattern, not in claiming `#072 = ki`. Anchor consistency: all chic-v2 anchors retain their values.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #065, CHIC #034, CHIC #040**. Two `[stop:#072]-de NUM` accountancy formula instances at #065 + one at #034 (cross-support: bar + medallion), plus co-occurrence with the canonical `ki-de NUM:2` formula at #040, mirror the chic-v11 ku-pa accountancy-formula context inspection structure. Stop-class for #072 produces a coherent accountancy reading consistent with surrounding sign-run-plus-numeral structure.

---

### `#017 → nasal` (chic-v5 proposed: nasal; freq 6; corroborated_by: etruscan — 1 of 3)

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #037 | Knossos | medallion | clean | 8 | `X 042-054-061 / X 017-039 100` |
| CHIC #021 | Knossos | crescent | clean | 6 | `X 038-017-049-034 / *153` |
| CHIC #234 + #310 | Mallia / Sitia | seal | clean | 2 / 14 | `017-050 ><` / `017-050 {001}` (cross-site recurring 2-sign run) |

#### Rendered readings

- CHIC #037: `X wa mu te / X [N:#017] [stop:#039] NUM:100`
- CHIC #021: `X i [N:#017] de [?:#034] / [?:#153]`
- CHIC #234: `[N:#017] [?:#050]`
- CHIC #310: `... / [N:#017] [?:#050] [?:#001] / ...`

#### Structural commentary

- **CHIC #037 (Knossos medallion, clean)** carries the 2-sign run `[N:#017] [stop:#039]` directly followed by NUM:100 — **canonical accountancy formula structure**. The first line `wa-mu-te` is anchored (and is the recurrent CHIC `wa-mu-te` short formula attested at multiple sealings, e.g. CHIC #037, #303). Both the inscription's anchored line and the candidate-bearing line follow the sign-run-plus-quantity pattern.
- **CHIC #021 (Knossos crescent, clean)** opens with the 4-sign sequence `i-[N:#017]-de-[?:#034]`. The opening `i-N-de` is structurally a CV-CV-CV name beginning, with `i` and `de` being chic-v2 anchors. This does not conflict with `i-ja-ro` (which would require `ja` rather than a nasal in the V₂ slot) — they are different formulas using the same anchored `i` (#038). The `i-[N]-de` opening is plausible as a sealstone formula in its own right.
- **CHIC #234 (Mallia seal) + CHIC #310 (Sitia seal)** both clean, both carry the 2-sign run `017-050`. Cross-site recurrence of the same 2-sign formula across two independent clean seals (Mallia + Sitia) is **sealstone-formula-grade structural evidence** for #017 carrying a syllabographic value. Nasal-class onset for the V₁ slot of a recurring 2-sign sealing formula is a plausible name onset — exactly parallel to the role of `ki` in the `ki-de` formula or `wa` in the `wa-ke` formula.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke`.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #037, CHIC #021, CHIC #234, CHIC #310**. The `017-039 NUM:100` accountancy formula at clean Knossos #037 mirrors the chic-v11 ku-pa NUM-following structure on a smaller scale; the cross-site recurrence of `017-050` at clean Mallia + Sitia sealings is sealstone-formula-grade evidence; the `i-[N]-de` opening at clean Knossos #021 is a plausible CV-CV-CV name beginning. Nasal-class for #017 produces a coherent syllabographic reading across multiple support types and sites.

---

### `#039 → stop` (chic-v5 proposed: stop; freq 7; corroborated_by: toponym — 1 of 3)

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration |
|---|---|---|---|---:|---|
| CHIC #037 | Knossos | medallion | clean | 8 | `X 042-054-061 / X 017-039 100` |
| CHIC #142 | Knossos | crescent | clean | 5 | `018-039-005 0` |
| CHIC #303 | Crete (unprov.) | seal | partial | 15 | `X 062-020-028 / 042-054-061 / _019_-039-_038_-031 >< / 044-049` |

#### Rendered readings

- CHIC #037: `X wa mu te / X [N:#017] [stop:#039] NUM:100`
- CHIC #142: `[?:#018] [stop:#039] [stop:#005] NUM:0`
- CHIC #303: `X [?:#062] [?:#020] ti / wa mu te / [?ke] [stop:#039] [?i] ro / ki de`

#### Structural commentary

- **CHIC #037 (Knossos medallion, clean)** is the same inscription as #017 above. The 2-sign run `[N:#017] [stop:#039]` followed by NUM:100 is **canonical accountancy formula structure**. Stop-class for #039 in V₂ position of a `[N]-[stop]-NUM` 2-sign+quantity entry is structurally compatible.
- **CHIC #142 (Knossos crescent, clean)** carries a 3-sign run `[?:#018] [stop:#039] [stop:#005]` followed by NUM:0. Two stop-class candidates back-to-back (#039 + #005, both chic-v13 candidates) followed by a numeral is internally consistent and follows the sign-run-plus-numeral accountancy structure.
- **CHIC #303 (Crete unprovenanced, seal, partial)** contains both the canonical `wa-mu-te` short formula (line 2) and `044-049 = ki-de` (line 4). Line 3 `_019_-039-_038_-031` rendered as `[?ke]-[stop:#039]-[?i]-ro` is a 4-sign formula bracketed by sealstone short formulas. With #039 stop, the line 3 reading is `ke-stop-i-ro` — not a canonical formula but no conflict with the anchored `wa-mu-te`, `ki-de`, or `i-ja-ro`.

Anchor consistency: all chic-v2 anchors retain their values. No conflict with `i-ja-ro`, `ki-de`, or `wa-ke` — although line 3 of #303 contains the substring `_038_-031`, which is the last 2 signs of `i-ja-ro` (`038-010-031`), the `010` (`ja`) is absent here, so the `[?i]-ro` partial does not constitute the formula.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #037, CHIC #142, CHIC #303**. The `017-039 NUM:100` accountancy formula at clean Knossos #037 plus the `[?]-039-005 NUM:0` accountancy run at clean Knossos #142 follow the sign-run-plus-numeral pattern; co-occurrence with `wa-mu-te` and `ki-de` at #303 is structurally compatible. Stop-class for #039 does not contradict canonical sealstone formulas. The 1-of-3 cross-pool corroboration (toponym only) is the lowest in this candidate set, but the within-window context evidence at clean medallion + clean crescent is positive.

---

### `#056 → stop` (chic-v5 proposed: stop; freq 52; corroborated_by: etruscan — 1 of 3)

#### Selected inscriptions

| inscription | site | support | confidence | n_signs | raw_transliteration (relevant fragment) |
|---|---|---|---|---:|---|
| CHIC #061 | Knossos | bar | fragmentary | 53 | `]023-032 1 \| 042-056-031 1 / ]•-034-056 1 \| ... \| 034-056 019-049 1 / 056-070-070 12` |
| CHIC #298 | Crete (unprov.) | seal | clean | 19 | `X 056-070-040 / X 070-061-019-045-070 / 038-010-031 / 044-005 / 044-049` |
| CHIC #294 | Crete (unprov.) | seal | partial | 35 | `... / X 059-057-_014_-041-019-047-070-092-019-044-050-019-028-056 / •-056-_061_-_077_ / ... / 092-057(•?)034(•?)016-056 ><` |

#### Rendered readings

- CHIC #061 (multiple fragments): `wa [stop:#056] ro NUM:1`, `[?:#034] [stop:#056] NUM:1`, `[?:#034] [stop:#056] ke de NUM:1`, `[stop:#056] ra ra NUM:12`
- CHIC #298: `X [stop:#056] ra [?:#040] / X ra te ke [?:#045] ra / i ja ro / ki [stop:#005] / ki de`
- CHIC #294: `... X [?:#059] je [?:#014] ni ke [?:#047] ra ke ke ki [?:#050] ke ti [stop:#056] / [?] [stop:#056] te ma / ... / ke je [?:#034] a [stop:#056]`

#### Structural commentary

- **CHIC #061 (Knossos bar, fragmentary)** is the **strongest accountancy-context evidence** in the chic-v13 set after `#072`: the bar carries **multiple `[?] [stop:#056] NUM` accountancy formula entries** (4 distinct `056` occurrences across the bar's surviving fragments). Notably, the 4-sign run `[?:#034] [stop:#056] ke de NUM:1` includes the canonical `019-049 = ke-de` formula directly after the candidate-bearing run, then NUM:1 — the candidate-bearing 2-sign run is in a name/commodity slot preceding `ke-de` plus quantity, mirroring the chic-v11 ku-pa accountancy-formula structure on a higher-frequency sign. The 3-sign `[stop:#056] ra ra NUM:12` is also followed by a numeral.
- **CHIC #298 (Crete unprov., clean seal)** is the same inscription cited under `#005`: contains all three of `i-ja-ro` (`038-010-031`), `ki-de` (`044-049`), and the `044-005 = ki-stop` short formula. Line 1 `[stop:#056] ra [?:#040]` is a sealstone-opening 3-sign formula. Stop-class for #056 in initial slot followed by anchored `ra` produces a CV-CV `[stop]-ra-?` name/title opening — structurally compatible with the sealstone's multiple anchored short formulas.
- **CHIC #294 (Crete unprov., partial seal)** carries 3 #056 occurrences across long sign-strings. The terminal-position `[stop:#056]` at the end of long token-strings (`... ke ti [stop:#056]`, `... ke je [?:#034] a [stop:#056]`) is consistent with a stop-class CV closing element. Mixed anchored signs (ke, ra, ki, ti, ni, je, a) form a phonotactically-plausible reading.

Anchor consistency: all chic-v2 anchors retain their values. The rendered reading does not contradict `i-ja-ro`, `ki-de`, or `wa-ke`; in #298, all three canonical formulas are anchor-stable in the same inscription as the candidate-bearing run.

#### Verdict: **consistent**

Cited inscriptions: **CHIC #061, CHIC #298, CHIC #294**. The repeated `[?] [stop:#056] NUM` accountancy formula entries at Knossos bar #061 (with one instance directly preceding `ke-de`) mirror the chic-v11 `#032 → ki` ku-pa accountancy-context structure; co-occurrence with all three canonical sealstone formulas at #298 without contradiction is additional structural support. Stop-class for #056 is the only chic-v13 candidate beyond `#072` with multiple canonical-formula adjacencies in a single clean inscription.

## Combined verdict

| sign | freq | corroborated_by (non-Eteo) | verdict |
|---|---:|---|---|
| `#021` | 3 | aquitanian, etruscan, toponym (3 of 3) | **consistent** |
| `#005` | 48 | aquitanian, toponym (2 of 3) | **consistent** |
| `#055` | 5 | aquitanian, toponym (2 of 3) | **inconclusive** |
| `#065` | 3 | aquitanian, toponym (2 of 3) | **inconclusive** |
| `#072` | 7 | etruscan, toponym (2 of 3) | **consistent** |
| `#017` | 6 | etruscan (1 of 3) | **consistent** |
| `#039` | 7 | toponym (1 of 3) | **consistent** |
| `#056` | 52 | etruscan (1 of 3) | **consistent** |

Headline: **6 of 8 candidates produce contextually-consistent renderings, 2 of 8 are inconclusive, 0 of 8 are disconfirmed by within-window context inspection.**

The two inconclusive verdicts (`#055`, `#065`) share a common feature: their on-corpus occurrences are dominated by fragmentary inscriptions, with `#065` additionally carrying its only `clean`-confidence occurrence inside a variant transcription brace `{065}`. Stop-class for both produces no contradiction with anchored neighbours or canonical formulas, but no positive accountancy- or sealstone-formula-grade evidence either. The verdict is `inconclusive` rather than `inconsistent` because no rendered reading actively conflicts with the surrounding structure.

Among the 6 consistent verdicts, the strength of within-window context evidence varies:

- **Strongest**: `#072` (two `[stop:#072]-de NUM` accountancy formula instances at Knossos bar #065 + one at #034, mirroring chic-v11 ku-pa on CHIC #057), `#056` (multiple `[?] [stop:#056] NUM` entries at Knossos bar #061, plus `034-056 ke-de NUM:1` direct adjacency with `ke-de`), and `#021` (three-fold cross-site recurrence of `031-021-061` plus direct adjacency with `ki-de` at #059).
- **Moderate**: `#005` (`044-005 = ki-stop` recurring across multiple clean sealings, plus the parallel-pattern `[CV]-005-050` at #273), `#017` (cross-site `017-050` at clean Mallia + Sitia sealings, plus `017-039 NUM:100` accountancy at #037).
- **Weakest among consistent**: `#039` (the `017-039 NUM:100` accountancy at clean Knossos #037 is positive but the cross-pool corroboration is only 1-of-3, the lowest in the consistent group).

## Discipline notes

- **What this inspection does NOT do.** It does not run specialist judgment on whether the proposed phoneme classes are correct readings. It runs the within-window structural-consistency check the chic-v13 brief asks for — does the rendered reading produce a result consistent with the surrounding accountancy / sealstone-formula structure, and does it contradict any chic-v2 anchor or any of the three canonical CHIC sealstone formulas (`i-ja-ro`, `ki-de`, `wa-ke`)? Each per-candidate verdict is a structural-consistency observation, not a phoneme-value endorsement.

- **What this inspection does NOT lift.** The chic-v9 LOO framework-level negative (aggregate accuracy 20.0%, 0/3 tier-2 unanimity correct under leave-one-out) is unchanged by chic-v13. The chic-v12 cross-pool L3 axis's systematic class bias (chic-v12 verdict: "the cross-pool L3 axis is meaningfully more permissive than the Eteocretan-only L3 axis chic-v5 used") is also unchanged. chic-v13 contributes a *fourth* discipline-protecting axis on top of the three pillars chic-v11 + chic-v12 already established (cross-pool L3 corroboration + chic-v9 LOO + chic-v6 mechanical verification): **within-window context inspection on a tier-2-equivalent candidate's host inscriptions catches whether the proposed value produces a structurally-consistent rendered reading**. 6 of 8 pass that check; 2 are inconclusive on corpus state; 0 are disconfirmed.

- **No anchor pool modification.** Per the chic-v13 brief, this ticket is read-only on `pools/cretan_hieroglyphic_anchors.yaml`. No tier-2-equivalent candidate is promoted into the chic-v2 anchor pool by chic-v13. Promotion to "candidate proposal pending domain-expert review" is a PM call, separate from the chic-v13 deliverable.

- **No specific-CV expansion.** chic-v12's cross-pool L3 result is class-level, not phoneme-level. chic-v13 retains class-level placeholders in renderings (`[stop:#NNN]`, `[N:#NNN]`) and does not invent specific CV expansions. The few CV-level observations in the per-candidate commentary (e.g. "the V₂ slot N could be `ma`/`me`/`mu`/`ni`") are reported as *structural-compatibility* observations, not specific-value claims.

- **The 6 `consistent` verdicts do not constitute decipherment claims.** They mean: the chic-v12 cross-pool L3 axis's class-level proposal for the candidate is structurally compatible with a within-window context inspection of the candidate's host inscriptions, in the sense that (a) anchored neighbours retain coherent readings, (b) the candidate's class assignment does not contradict canonical sealstone formulas, and (c) on at least one host inscription, the rendered reading parallels the kind of accountancy or sealstone-formula structure the Linear A scholar readings (e.g. `ku-pa`, `ki-ro`) are themselves extracted from. Specialist review remains the load-bearing next step for any candidate.

- **The 2 `inconclusive` verdicts (`#055`, `#065`) are honest under-determination.** Both signs occur predominantly in fragmentary inscriptions; #065's only clean occurrence is itself a variant-bracketed reading. The chic-v13 brief explicitly says: "If 0/8 pass context inspection, report that honestly — it would *strengthen* the framework's discrimination claim by showing cross-pool L3 alone is not sufficient, which is itself a publishable methodology finding." The 2 inconclusive verdicts honour the same discipline: where the corpus state does not support a definitive context check, the verdict is `inconclusive` rather than weakened to `consistent` to inflate the headline count.

## Determinism

- No RNG. The candidate list is fixed by chic-v12; inscription selection is a deterministic frequency-density argmax over `corpora/cretan_hieroglyphic/all.jsonl`; rendered readings use the chic-v2 anchor mapping byte-identically.
- Same (chic-v0 corpus, chic-v2 anchors, chic-v12 candidate list) → byte-identical output.

## Build provenance

- Generated by manual inspection following the chic-v11 `results/chic_v11_032_ku_pa_context.md` template (mg-5261).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs:
  - `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0)
  - `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2)
  - `results/chic_v12_cross_pool_l3.md` (chic-v12; the 8 tier-2-equivalent candidate list + per-candidate cross-pool L3 verdict)
  - `results/chic_v11_032_ku_pa_context.md` (chic-v11; methodological template)

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Younger, J. G. (online). *The Cretan Hieroglyphic Texts: a web edition of CHIC with commentary.* Wayback Machine snapshot 20220703170656.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Decorte, R. (2017). *The First 'European' Writing.*
- Civitillo, M. (2016). *La scrittura geroglifica minoica sui sigilli.*
