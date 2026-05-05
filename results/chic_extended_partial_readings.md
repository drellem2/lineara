# CHIC extended partial readings under chic-v6 tier extensions (mg-a557)

Extended partial readings of every CHIC inscription in `corpora/cretan_hieroglyphic/all.jsonl`, rendered at four tier levels of sign-value extension. Built by `scripts/build_chic_v6.py`.

## Tier levels

- **tier-1** — chic-v2 paleographic-anchor pool only (20 anchors; same as `results/chic_partial_readings.md`).
- **tier-2** — tier-1 ∪ chic-v5 tier-2 candidates with chic-v6 specific-phoneme overrides (`#001 → wa`, `#012 → wa`, `#032 → ki`).
- **tier-3** — tier-2 ∪ chic-v5 tier-3 candidates as class-level placeholders (`[STOP:#NNN]`, `[GLIDE:#NNN]`, …); 29 added signs.
- **tier-4** — tier-3 ∪ chic-v5 tier-4 candidates as class-level placeholders; 17 more added signs.

## Rendering convention

- Anchored clean: emit phonetic value (e.g. `ra`).
- Anchored uncertain: emit `[?:value]`.
- Class-placeholder clean: emit `[CLASS:#NNN]` (e.g. `[STOP:#005]`).
- Class-placeholder uncertain: emit `[?:CLASS:#NNN]`.
- Unanchored clean: emit `#NNN`.
- Unanchored uncertain: emit `[?:#NNN]`.
- DIV: emit `/`.
- Illegible: emit `[?]`.
- Ideogram: emit `IDEO:#NNN`.

## Per-tier coverage rollup

Coverage = (anchored literal positions + class-placeholder positions) / total syllabographic positions, per chic-v1 sign classification. Per-inscription numerator-denominator detail is in `results/experiments.chic_verification_v0.jsonl`.

| tier | n anchored signs (literal) | n class-placeholder signs | n inscriptions w/ ≥1 syllabographic | mean extended coverage |
|---|---:|---:|---:|---:|
| tier-1 | 20 | 0 | 288 | 0.6298 |
| tier-2 | 23 | 0 | 288 | 0.6385 |
| tier-3 | 23 | 29 | 288 | 0.8475 |
| tier-4 | 23 | 46 | 288 | 0.9735 |

## Per-inscription extended readings

Per-inscription readings are tabulated below. For each inscription, the four tier-level readings are listed in successive rows.

| CHIC id | Site | Support | tier | n_syll | n_lit | n_cls | n_unanch | coverage | partial reading |
|---|---|---|---|--:|--:|--:|--:|--:|---|
| CHIC #001 | Knossos | crescent | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `[?:me] #034 ro ra` |
| CHIC #001 | Knossos | crescent | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `[?:me] #034 ro ra` |
| CHIC #001 | Knossos | crescent | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `[?:me] #034 ro ra` |
| CHIC #001 | Knossos | crescent | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `[?:me] [LIQUID:#034] ro ra` |
| CHIC #002 | Knossos | crescent | tier-1 | 5 | 2 | 0 | 3 | 0.4000 | `[?:pa] #056 #068 / [?:#050] a / [?]` |
| CHIC #002 | Knossos | crescent | tier-2 | 5 | 2 | 0 | 3 | 0.4000 | `[?:pa] #056 #068 / [?:#050] a / [?]` |
| CHIC #002 | Knossos | crescent | tier-3 | 5 | 2 | 2 | 1 | 0.8000 | `[?:pa] [STOP:#056] #068 / [?:GLIDE:#050] a / [?]` |
| CHIC #002 | Knossos | crescent | tier-4 | 5 | 2 | 3 | 0 | 1.0000 | `[?:pa] [STOP:#056] [LIQUID:#068] / [?:GLIDE:#050] a / [?]` |
| CHIC #003 | Knossos | nodulus | tier-1 | 11 | 8 | 0 | 3 | 0.7273 | `a mu / #009 ma pa #020 / je a / #050 a wa` |
| CHIC #003 | Knossos | nodulus | tier-2 | 11 | 8 | 0 | 3 | 0.7273 | `a mu / #009 ma pa #020 / je a / #050 a wa` |
| CHIC #003 | Knossos | nodulus | tier-3 | 11 | 8 | 3 | 0 | 1.0000 | `a mu / [STOP:#009] ma pa [VOWEL:#020] / je a / [GLIDE:#050] a wa` |
| CHIC #003 | Knossos | nodulus | tier-4 | 11 | 8 | 3 | 0 | 1.0000 | `a mu / [STOP:#009] ma pa [VOWEL:#020] / je a / [GLIDE:#050] a wa` |
| CHIC #004 | Knossos | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ke i #059` |
| CHIC #004 | Knossos | crescent | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `ke i #059` |
| CHIC #004 | Knossos | crescent | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `ke i [GLIDE:#059]` |
| CHIC #004 | Knossos | crescent | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `ke i [GLIDE:#059]` |
| CHIC #005 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?:#047] ke [?]` |
| CHIC #005 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?:#047] ke [?]` |
| CHIC #005 | Knossos | crescent | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `[?:#047] ke [?]` |
| CHIC #005 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?:LIQUID:#047] ke [?]` |
| CHIC #006 | Knossos | crescent | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#154` |
| CHIC #006 | Knossos | crescent | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#154` |
| CHIC #006 | Knossos | crescent | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#154` |
| CHIC #006 | Knossos | crescent | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#154` |
| CHIC #007 | Knossos | crescent | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #007 | Knossos | crescent | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #007 | Knossos | crescent | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #007 | Knossos | crescent | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #008 | Knossos | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ti i #032 [?]` |
| CHIC #008 | Knossos | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `ti i ki [?]` |
| CHIC #008 | Knossos | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `ti i ki [?]` |
| CHIC #008 | Knossos | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `ti i ki [?]` |
| CHIC #009 | Knossos | crescent | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#065] #063` |
| CHIC #009 | Knossos | crescent | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#065] #063` |
| CHIC #009 | Knossos | crescent | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[?:STOP:#065] [GLIDE:#063]` |
| CHIC #009 | Knossos | crescent | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[?:STOP:#065] [GLIDE:#063]` |
| CHIC #010 | Knossos | crescent | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `i` |
| CHIC #010 | Knossos | crescent | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `i` |
| CHIC #010 | Knossos | crescent | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `i` |
| CHIC #010 | Knossos | crescent | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `i` |
| CHIC #011 | Knossos | crescent | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `de de / [?:ti] / [?]` |
| CHIC #011 | Knossos | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `de de / [?:ti] / [?]` |
| CHIC #011 | Knossos | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `de de / [?:ti] / [?]` |
| CHIC #011 | Knossos | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `de de / [?:ti] / [?]` |
| CHIC #012 | Knossos | crescent | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?] / ti de [?]` |
| CHIC #012 | Knossos | crescent | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?] / ti de [?]` |
| CHIC #012 | Knossos | crescent | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?] / ti de [?]` |
| CHIC #012 | Knossos | crescent | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?] / ti de [?]` |
| CHIC #013 | Knossos | crescent | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `#062 #011 #056 / ki [?]` |
| CHIC #013 | Knossos | crescent | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `#062 #011 #056 / ki [?]` |
| CHIC #013 | Knossos | crescent | tier-3 | 4 | 1 | 2 | 1 | 0.7500 | `#062 [LIQUID:#011] [STOP:#056] / ki [?]` |
| CHIC #013 | Knossos | crescent | tier-4 | 4 | 1 | 3 | 0 | 1.0000 | `[GLIDE:#062] [LIQUID:#011] [STOP:#056] / ki [?]` |
| CHIC #014 | Knossos | crescent | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `[?] [?:i] [?]` |
| CHIC #014 | Knossos | crescent | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `[?] [?:i] [?]` |
| CHIC #014 | Knossos | crescent | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `[?] [?:i] [?]` |
| CHIC #014 | Knossos | crescent | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `[?] [?:i] [?]` |
| CHIC #015 | Knossos | crescent | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#011 #056 [?]` |
| CHIC #015 | Knossos | crescent | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#011 #056 [?]` |
| CHIC #015 | Knossos | crescent | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[LIQUID:#011] [STOP:#056] [?]` |
| CHIC #015 | Knossos | crescent | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[LIQUID:#011] [STOP:#056] [?]` |
| CHIC #016 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `de #056` |
| CHIC #016 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `de #056` |
| CHIC #016 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `de [STOP:#056]` |
| CHIC #016 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `de [STOP:#056]` |
| CHIC #017 | Knossos | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `IDEO:#153 / #059 mu ro` |
| CHIC #017 | Knossos | crescent | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `IDEO:#153 / #059 mu ro` |
| CHIC #017 | Knossos | crescent | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `IDEO:#153 / [GLIDE:#059] mu ro` |
| CHIC #017 | Knossos | crescent | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `IDEO:#153 / [GLIDE:#059] mu ro` |
| CHIC #018 | Knossos | crescent | tier-1 | 7 | 2 | 0 | 5 | 0.2857 | `#009 #056 te / #020 #047 / ki #005` |
| CHIC #018 | Knossos | crescent | tier-2 | 7 | 2 | 0 | 5 | 0.2857 | `#009 #056 te / #020 #047 / ki #005` |
| CHIC #018 | Knossos | crescent | tier-3 | 7 | 2 | 4 | 1 | 0.8571 | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] #047 / ki [STOP:#005]` |
| CHIC #018 | Knossos | crescent | tier-4 | 7 | 2 | 5 | 0 | 1.0000 | `[STOP:#009] [STOP:#056] te / [VOWEL:#020] [LIQUID:#047] / ki [STOP:#005]` |
| CHIC #019 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?] / [?:ta] [?:#046] / [?]` |
| CHIC #019 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?] / [?:ta] [?:#046] / [?]` |
| CHIC #019 | Knossos | crescent | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `[?] / [?:ta] [?:#046] / [?]` |
| CHIC #019 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?] / [?:ta] [?:GLIDE:#046] / [?]` |
| CHIC #020 | Knossos | crescent | tier-1 | 1 | 0 | 0 | 1 | 0.0000 | `[?] [?:#078] / [?]` |
| CHIC #020 | Knossos | crescent | tier-2 | 1 | 0 | 0 | 1 | 0.0000 | `[?] [?:#078] / [?]` |
| CHIC #020 | Knossos | crescent | tier-3 | 1 | 0 | 1 | 0 | 1.0000 | `[?] [?:STOP:#078] / [?]` |
| CHIC #020 | Knossos | crescent | tier-4 | 1 | 0 | 1 | 0 | 1.0000 | `[?] [?:STOP:#078] / [?]` |
| CHIC #021 | Knossos | crescent | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `i #017 de #034 / IDEO:#153` |
| CHIC #021 | Knossos | crescent | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `i #017 de #034 / IDEO:#153` |
| CHIC #021 | Knossos | crescent | tier-3 | 4 | 2 | 1 | 1 | 0.7500 | `i [NASAL:#017] de #034 / IDEO:#153` |
| CHIC #021 | Knossos | crescent | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `i [NASAL:#017] de [LIQUID:#034] / IDEO:#153` |
| CHIC #022 | Knossos | crescent | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `#055 ra de [?] / [?] [?:ro]` |
| CHIC #022 | Knossos | crescent | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `#055 ra de [?] / [?] [?:ro]` |
| CHIC #022 | Knossos | crescent | tier-3 | 4 | 3 | 1 | 0 | 1.0000 | `[STOP:#055] ra de [?] / [?] [?:ro]` |
| CHIC #022 | Knossos | crescent | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `[STOP:#055] ra de [?] / [?] [?:ro]` |
| CHIC #023 | Knossos | crescent | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `wa [?:#045] #029` |
| CHIC #023 | Knossos | crescent | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `wa [?:#045] #029` |
| CHIC #023 | Knossos | crescent | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `wa [?:STOP:#045] #029` |
| CHIC #023 | Knossos | crescent | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `wa [?:STOP:#045] [LIQUID:#029]` |
| CHIC #024 | Knossos | crescent | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#011 #056 / IDEO:#153` |
| CHIC #024 | Knossos | crescent | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#011 #056 / IDEO:#153` |
| CHIC #024 | Knossos | crescent | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[LIQUID:#011] [STOP:#056] / IDEO:#153` |
| CHIC #024 | Knossos | crescent | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[LIQUID:#011] [STOP:#056] / IDEO:#153` |
| CHIC #025 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?] i #011 / [?]` |
| CHIC #025 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?] i #011 / [?]` |
| CHIC #025 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[?] i [LIQUID:#011] / [?]` |
| CHIC #025 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?] i [LIQUID:#011] / [?]` |
| CHIC #026 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#011 ke / IDEO:#153` |
| CHIC #026 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#011 ke / IDEO:#153` |
| CHIC #026 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#011] ke / IDEO:#153` |
| CHIC #026 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#011] ke / IDEO:#153` |
| CHIC #027 | Knossos | crescent | tier-1 | 9 | 5 | 0 | 4 | 0.5556 | `wa ni #011 / ke #067 #032 / je ta #034 [?]` |
| CHIC #027 | Knossos | crescent | tier-2 | 9 | 6 | 0 | 3 | 0.6667 | `wa ni #011 / ke #067 ki / je ta #034 [?]` |
| CHIC #027 | Knossos | crescent | tier-3 | 9 | 6 | 1 | 2 | 0.7778 | `wa ni [LIQUID:#011] / ke #067 ki / je ta #034 [?]` |
| CHIC #027 | Knossos | crescent | tier-4 | 9 | 6 | 2 | 1 | 0.8889 | `wa ni [LIQUID:#011] / ke #067 ki / je ta [LIQUID:#034] [?]` |
| CHIC #028 | Knossos | crescent | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `#072 / [?] / [?] / [?:#062] ke te / [?:ni] / [?]` |
| CHIC #028 | Knossos | crescent | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `#072 / [?] / [?] / [?:#062] ke te / [?:ni] / [?]` |
| CHIC #028 | Knossos | crescent | tier-3 | 5 | 3 | 1 | 1 | 0.8000 | `[STOP:#072] / [?] / [?] / [?:#062] ke te / [?:ni] / [?]` |
| CHIC #028 | Knossos | crescent | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `[STOP:#072] / [?] / [?] / [?:GLIDE:#062] ke te / [?:ni] / [?]` |
| CHIC #029 | Knossos | crescent | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `[?:wa] / [?:#060] [?:ra] / [?:ke] #055` |
| CHIC #029 | Knossos | crescent | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `[?:wa] / [?:#060] [?:ra] / [?:ke] #055` |
| CHIC #029 | Knossos | crescent | tier-3 | 5 | 3 | 2 | 0 | 1.0000 | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` |
| CHIC #029 | Knossos | crescent | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `[?:wa] / [?:STOP:#060] [?:ra] / [?:ke] [STOP:#055]` |
| CHIC #030 | Knossos | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `[?:#068] [?:#046] [?:ke] / [?]` |
| CHIC #030 | Knossos | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `[?:#068] [?:#046] [?:ke] / [?]` |
| CHIC #030 | Knossos | medallion | tier-3 | 3 | 1 | 0 | 2 | 0.3333 | `[?:#068] [?:#046] [?:ke] / [?]` |
| CHIC #030 | Knossos | medallion | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[?:LIQUID:#068] [?:GLIDE:#046] [?:ke] / [?]` |
| CHIC #031 | Knossos | medallion | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `#034 de #056 #052` |
| CHIC #031 | Knossos | medallion | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `#034 de #056 #052` |
| CHIC #031 | Knossos | medallion | tier-3 | 4 | 1 | 1 | 2 | 0.5000 | `#034 de [STOP:#056] #052` |
| CHIC #031 | Knossos | medallion | tier-4 | 4 | 1 | 3 | 0 | 1.0000 | `[LIQUID:#034] de [STOP:#056] [LIQUID:#052]` |
| CHIC #032 | Knossos | medallion | tier-1 | 8 | 4 | 0 | 4 | 0.5000 | `#056 #047 ro / #050 a / je #047 te` |
| CHIC #032 | Knossos | medallion | tier-2 | 8 | 4 | 0 | 4 | 0.5000 | `#056 #047 ro / #050 a / je #047 te` |
| CHIC #032 | Knossos | medallion | tier-3 | 8 | 4 | 2 | 2 | 0.7500 | `[STOP:#056] #047 ro / [GLIDE:#050] a / je #047 te` |
| CHIC #032 | Knossos | medallion | tier-4 | 8 | 4 | 4 | 0 | 1.0000 | `[STOP:#056] [LIQUID:#047] ro / [GLIDE:#050] a / je [LIQUID:#047] te` |
| CHIC #033 | Knossos | medallion | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?:#050] ke i / [?] / [?] [?]` |
| CHIC #033 | Knossos | medallion | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?:#050] ke i / [?] / [?] [?]` |
| CHIC #033 | Knossos | medallion | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `[?:GLIDE:#050] ke i / [?] / [?] [?]` |
| CHIC #033 | Knossos | medallion | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[?:GLIDE:#050] ke i / [?] / [?] [?]` |
| CHIC #034 | Knossos | medallion | tier-1 | 5 | 4 | 0 | 1 | 0.8000 | `mu te pa / [?] / [?] / #072 de / NUM:10` |
| CHIC #034 | Knossos | medallion | tier-2 | 5 | 4 | 0 | 1 | 0.8000 | `mu te pa / [?] / [?] / #072 de / NUM:10` |
| CHIC #034 | Knossos | medallion | tier-3 | 5 | 4 | 1 | 0 | 1.0000 | `mu te pa / [?] / [?] / [STOP:#072] de / NUM:10` |
| CHIC #034 | Knossos | medallion | tier-4 | 5 | 4 | 1 | 0 | 1.0000 | `mu te pa / [?] / [?] / [STOP:#072] de / NUM:10` |
| CHIC #035 | Knossos | medallion | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| CHIC #035 | Knossos | medallion | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| CHIC #035 | Knossos | medallion | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| CHIC #035 | Knossos | medallion | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?] wa te / [?] / [?] / [?] / NUM:40` |
| CHIC #036 | Knossos | medallion | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `#023 [?:te] ke je / NUM:100` |
| CHIC #036 | Knossos | medallion | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `#023 [?:te] ke je / NUM:100` |
| CHIC #036 | Knossos | medallion | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `#023 [?:te] ke je / NUM:100` |
| CHIC #036 | Knossos | medallion | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `[LIQUID:#023] [?:te] ke je / NUM:100` |
| CHIC #037 | Knossos | medallion | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `wa mu te / #017 #039 / NUM:100` |
| CHIC #037 | Knossos | medallion | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `wa mu te / #017 #039 / NUM:100` |
| CHIC #037 | Knossos | medallion | tier-3 | 5 | 3 | 2 | 0 | 1.0000 | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` |
| CHIC #037 | Knossos | medallion | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `wa mu te / [NASAL:#017] [STOP:#039] / NUM:100` |
| CHIC #038 | Knossos | medallion | tier-1 | 9 | 7 | 0 | 2 | 0.7778 | `ke ma #029 / je pa de / je #069 ra / NUM:110` |
| CHIC #038 | Knossos | medallion | tier-2 | 9 | 7 | 0 | 2 | 0.7778 | `ke ma #029 / je pa de / je #069 ra / NUM:110` |
| CHIC #038 | Knossos | medallion | tier-3 | 9 | 7 | 1 | 1 | 0.8889 | `ke ma #029 / je pa de / je [STOP:#069] ra / NUM:110` |
| CHIC #038 | Knossos | medallion | tier-4 | 9 | 7 | 2 | 0 | 1.0000 | `ke ma [LIQUID:#029] / je pa de / je [STOP:#069] ra / NUM:110` |
| CHIC #039 | Knossos | medallion | tier-1 | 11 | 4 | 0 | 7 | 0.3636 | `#056 [?:#023] / #043 ra / #020 ma / wa #017 / je #023 [?:#051] / NUM:120` |
| CHIC #039 | Knossos | medallion | tier-2 | 11 | 4 | 0 | 7 | 0.3636 | `#056 [?:#023] / #043 ra / #020 ma / wa #017 / je #023 [?:#051] / NUM:120` |
| CHIC #039 | Knossos | medallion | tier-3 | 11 | 4 | 4 | 3 | 0.7273 | `[STOP:#056] [?:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:#017] / je #023 [?:#051] / NUM:120` |
| CHIC #039 | Knossos | medallion | tier-4 | 11 | 4 | 7 | 0 | 1.0000 | `[STOP:#056] [?:LIQUID:#023] / [LIQUID:#043] ra / [VOWEL:#020] ma / wa [NASAL:#017] / je [LIQUID:#023] [?:GLIDE:#051] / NUM:120` |
| CHIC #040 | Knossos | medallion | tier-1 | 10 | 6 | 0 | 4 | 0.6000 | `ke ra te / #072 #039 / ki de / NUM:2 / #068 ro / [?:#004]` |
| CHIC #040 | Knossos | medallion | tier-2 | 10 | 6 | 0 | 4 | 0.6000 | `ke ra te / #072 #039 / ki de / NUM:2 / #068 ro / [?:#004]` |
| CHIC #040 | Knossos | medallion | tier-3 | 10 | 6 | 2 | 2 | 0.8000 | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / #068 ro / [?:#004]` |
| CHIC #040 | Knossos | medallion | tier-4 | 10 | 6 | 4 | 0 | 1.0000 | `ke ra te / [STOP:#072] [STOP:#039] / ki de / NUM:2 / [LIQUID:#068] ro / [?:LIQUID:#004]` |
| CHIC #041 | Knossos | medallion | tier-1 | 6 | 1 | 0 | 5 | 0.1667 | `#069 #047 ni / NUM:1 / NUM:2 / #085 #011 #001 / NUM:32` |
| CHIC #041 | Knossos | medallion | tier-2 | 6 | 2 | 0 | 4 | 0.3333 | `#069 #047 ni / NUM:1 / NUM:2 / #085 #011 wa / NUM:32` |
| CHIC #041 | Knossos | medallion | tier-3 | 6 | 2 | 2 | 2 | 0.6667 | `[STOP:#069] #047 ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` |
| CHIC #041 | Knossos | medallion | tier-4 | 6 | 2 | 3 | 1 | 0.8333 | `[STOP:#069] [LIQUID:#047] ni / NUM:1 / NUM:2 / #085 [LIQUID:#011] wa / NUM:32` |
| CHIC #042 | Knossos | medallion | tier-1 | 7 | 3 | 0 | 4 | 0.4286 | `#037 #011 #029 / #043 ra / NUM:100 / ki de / NUM:634 / NUM:243` |
| CHIC #042 | Knossos | medallion | tier-2 | 7 | 3 | 0 | 4 | 0.4286 | `#037 #011 #029 / #043 ra / NUM:100 / ki de / NUM:634 / NUM:243` |
| CHIC #042 | Knossos | medallion | tier-3 | 7 | 3 | 3 | 1 | 0.8571 | `[LIQUID:#037] [LIQUID:#011] #029 / [LIQUID:#043] ra / NUM:100 / ki de / NUM:634 / NUM:243` |
| CHIC #042 | Knossos | medallion | tier-4 | 7 | 3 | 4 | 0 | 1.0000 | `[LIQUID:#037] [LIQUID:#011] [LIQUID:#029] / [LIQUID:#043] ra / NUM:100 / ki de / NUM:634 / NUM:243` |
| CHIC #043 | Knossos | medallion | tier-1 | 11 | 4 | 0 | 7 | 0.3636 | `#007 ja #006 #023 / [?] / ta ja / #024 #050 / ra #047 #047 / NUM:32` |
| CHIC #043 | Knossos | medallion | tier-2 | 11 | 4 | 0 | 7 | 0.3636 | `#007 ja #006 #023 / [?] / ta ja / #024 #050 / ra #047 #047 / NUM:32` |
| CHIC #043 | Knossos | medallion | tier-3 | 11 | 4 | 3 | 4 | 0.6364 | `[VOWEL:#007] ja [GLIDE:#006] #023 / [?] / ta ja / #024 [GLIDE:#050] / ra #047 #047 / NUM:32` |
| CHIC #043 | Knossos | medallion | tier-4 | 11 | 4 | 6 | 1 | 0.9091 | `[VOWEL:#007] ja [GLIDE:#006] [LIQUID:#023] / [?] / ta ja / #024 [GLIDE:#050] / ra [LIQUID:#047] [LIQUID:#047] / NUM:32` |
| CHIC #044 | Knossos | medallion | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?:i] ja #068 / IDEO:#153 / NUM:200` |
| CHIC #044 | Knossos | medallion | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?:i] ja #068 / IDEO:#153 / NUM:200` |
| CHIC #044 | Knossos | medallion | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `[?:i] ja #068 / IDEO:#153 / NUM:200` |
| CHIC #044 | Knossos | medallion | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[?:i] ja [LIQUID:#068] / IDEO:#153 / NUM:200` |
| CHIC #045 | Knossos | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#011 ma #034 / IDEO:#174 / NUM:1` |
| CHIC #045 | Knossos | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#011 ma #034 / IDEO:#174 / NUM:1` |
| CHIC #045 | Knossos | medallion | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `[LIQUID:#011] ma #034 / IDEO:#174 / NUM:1` |
| CHIC #045 | Knossos | medallion | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[LIQUID:#011] ma [LIQUID:#034] / IDEO:#174 / NUM:1` |
| CHIC #046 | Knossos | medallion | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `de [?:ke] #023 / IDEO:#166 / NUM:100` |
| CHIC #046 | Knossos | medallion | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `de [?:ke] #023 / IDEO:#166 / NUM:100` |
| CHIC #046 | Knossos | medallion | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `de [?:ke] #023 / IDEO:#166 / NUM:100` |
| CHIC #046 | Knossos | medallion | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `de [?:ke] [LIQUID:#023] / IDEO:#166 / NUM:100` |
| CHIC #047 | Knossos | medallion | tier-1 | 5 | 4 | 0 | 1 | 0.8000 | `me me ma / #089 ki / IDEO:#156 / NUM:441` |
| CHIC #047 | Knossos | medallion | tier-2 | 5 | 4 | 0 | 1 | 0.8000 | `me me ma / #089 ki / IDEO:#156 / NUM:441` |
| CHIC #047 | Knossos | medallion | tier-3 | 5 | 4 | 0 | 1 | 0.8000 | `me me ma / #089 ki / IDEO:#156 / NUM:441` |
| CHIC #047 | Knossos | medallion | tier-4 | 5 | 4 | 0 | 1 | 0.8000 | `me me ma / #089 ki / IDEO:#156 / NUM:441` |
| CHIC #048 | Knossos | bar | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#164 / NUM:2 / IDEO:#165 / NUM:2 / IDEO:#165 / NUM:2 / [?] / IDEO:#164 / NUM:2 / [?]` |
| CHIC #048 | Knossos | bar | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#164 / NUM:2 / IDEO:#165 / NUM:2 / IDEO:#165 / NUM:2 / [?] / IDEO:#164 / NUM:2 / [?]` |
| CHIC #048 | Knossos | bar | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#164 / NUM:2 / IDEO:#165 / NUM:2 / IDEO:#165 / NUM:2 / [?] / IDEO:#164 / NUM:2 / [?]` |
| CHIC #048 | Knossos | bar | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#164 / NUM:2 / IDEO:#165 / NUM:2 / IDEO:#165 / NUM:2 / [?] / IDEO:#164 / NUM:2 / [?]` |
| CHIC #049 | Knossos | bar | tier-1 | 23 | 10 | 0 | 13 | 0.4348 | `[?:#046] #063 / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [?] / ki de / NUM:40 / je #023 / NUM:20 / ki de / NUM:300 / #027 / [?:#005] NUM:50 / #034 #056 / NUM:6400 / ke #040 te / NUM:1300 [?] / ti #040 #004 / NUM:550 [?] / [?] / #088 #003 / [?] / [?] / NUM:1 [?:#006] NUM:0` |
| CHIC #049 | Knossos | bar | tier-2 | 23 | 10 | 0 | 13 | 0.4348 | `[?:#046] #063 / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [?] / ki de / NUM:40 / je #023 / NUM:20 / ki de / NUM:300 / #027 / [?:#005] NUM:50 / #034 #056 / NUM:6400 / ke #040 te / NUM:1300 [?] / ti #040 #004 / NUM:550 [?] / [?] / #088 #003 / [?] / [?] / NUM:1 [?:#006] NUM:0` |
| CHIC #049 | Knossos | bar | tier-3 | 23 | 10 | 7 | 6 | 0.7391 | `[?:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [?] / ki de / NUM:40 / je #023 / NUM:20 / ki de / NUM:300 / [GLIDE:#027] / [?:STOP:#005] NUM:50 / #034 [STOP:#056] / NUM:6400 / ke [STOP:#040] te / NUM:1300 [?] / ti [STOP:#040] #004 / NUM:550 [?] / [?] / #088 #003 / [?] / [?] / NUM:1 [?:GLIDE:#006] NUM:0` |
| CHIC #049 | Knossos | bar | tier-4 | 23 | 10 | 12 | 1 | 0.9565 | `[?:GLIDE:#046] [GLIDE:#063] / [?] / [?] / ti [?:de] / [?:IDEO:#200] / [?] / [?] / ki de / NUM:40 / je [LIQUID:#023] / NUM:20 / ki de / NUM:300 / [GLIDE:#027] / [?:STOP:#005] NUM:50 / [LIQUID:#034] [STOP:#056] / NUM:6400 / ke [STOP:#040] te / NUM:1300 [?] / ti [STOP:#040] [LIQUID:#004] / NUM:550 [?] / [?] / #088 [GLIDE:#003] / [?] / [?] / NUM:1 [?:GLIDE:#006] NUM:0` |
| CHIC #051 | Knossos | bar | tier-1 | 1 | 0 | 0 | 1 | 0.0000 | `[?] #051 / NUM:450 / [?] / NUM:20 [?] / [?] / NUM:6` |
| CHIC #051 | Knossos | bar | tier-2 | 1 | 0 | 0 | 1 | 0.0000 | `[?] #051 / NUM:450 / [?] / NUM:20 [?] / [?] / NUM:6` |
| CHIC #051 | Knossos | bar | tier-3 | 1 | 0 | 0 | 1 | 0.0000 | `[?] #051 / NUM:450 / [?] / NUM:20 [?] / [?] / NUM:6` |
| CHIC #051 | Knossos | bar | tier-4 | 1 | 0 | 1 | 0 | 1.0000 | `[?] [GLIDE:#051] / NUM:450 / [?] / NUM:20 [?] / [?] / NUM:6` |
| CHIC #052 | Knossos | bar | tier-1 | 10 | 7 | 0 | 3 | 0.7000 | `[?:te] / NUM:60 / #063 #047 te ro / NUM:40 / [?] / je ke te / NUM:290 / [?] / NUM:50 / NUM:50 / NUM:70 / [?:#029] ra / NUM:710` |
| CHIC #052 | Knossos | bar | tier-2 | 10 | 7 | 0 | 3 | 0.7000 | `[?:te] / NUM:60 / #063 #047 te ro / NUM:40 / [?] / je ke te / NUM:290 / [?] / NUM:50 / NUM:50 / NUM:70 / [?:#029] ra / NUM:710` |
| CHIC #052 | Knossos | bar | tier-3 | 10 | 7 | 1 | 2 | 0.8000 | `[?:te] / NUM:60 / [GLIDE:#063] #047 te ro / NUM:40 / [?] / je ke te / NUM:290 / [?] / NUM:50 / NUM:50 / NUM:70 / [?:#029] ra / NUM:710` |
| CHIC #052 | Knossos | bar | tier-4 | 10 | 7 | 3 | 0 | 1.0000 | `[?:te] / NUM:60 / [GLIDE:#063] [LIQUID:#047] te ro / NUM:40 / [?] / je ke te / NUM:290 / [?] / NUM:50 / NUM:50 / NUM:70 / [?:LIQUID:#029] ra / NUM:710` |
| CHIC #053 | Knossos | bar | tier-1 | 14 | 7 | 0 | 7 | 0.5000 | `[?] / ti de ni #003 / [?] #058 ro #056 / [?] / IDEO:#160 / NUM:170 / IDEO:#176 / NUM:160 / [?] / a je [?:pa] #074 #075 / [?] / [?:IDEO:#160] / [?:IDEO:#110] / [?] / [?] / IDEO:#176 / NUM:170 [?] / #058 [?:#002] / NUM:22` |
| CHIC #053 | Knossos | bar | tier-2 | 14 | 7 | 0 | 7 | 0.5000 | `[?] / ti de ni #003 / [?] #058 ro #056 / [?] / IDEO:#160 / NUM:170 / IDEO:#176 / NUM:160 / [?] / a je [?:pa] #074 #075 / [?] / [?:IDEO:#160] / [?:IDEO:#110] / [?] / [?] / IDEO:#176 / NUM:170 [?] / #058 [?:#002] / NUM:22` |
| CHIC #053 | Knossos | bar | tier-3 | 14 | 7 | 4 | 3 | 0.7857 | `[?] / ti de ni #003 / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#160 / NUM:170 / IDEO:#176 / NUM:160 / [?] / a je [?:pa] #074 #075 / [?] / [?:IDEO:#160] / [?:IDEO:#110] / [?] / [?] / IDEO:#176 / NUM:170 [?] / [STOP:#058] [?:LIQUID:#002] / NUM:22` |
| CHIC #053 | Knossos | bar | tier-4 | 14 | 7 | 5 | 2 | 0.8571 | `[?] / ti de ni [GLIDE:#003] / [?] [STOP:#058] ro [STOP:#056] / [?] / IDEO:#160 / NUM:170 / IDEO:#176 / NUM:160 / [?] / a je [?:pa] #074 #075 / [?] / [?:IDEO:#160] / [?:IDEO:#110] / [?] / [?] / IDEO:#176 / NUM:170 [?] / [STOP:#058] [?:LIQUID:#002] / NUM:22` |
| CHIC #054 | Knossos | bar | tier-1 | 10 | 9 | 0 | 1 | 0.9000 | `[?:wa] te / [?] / NUM:110 / je pa de / NUM:170 / [?] / NUM:160 / NUM:150 / NUM:50 / [?:#029] de / NUM:450 / ra ro ke / NUM:60` |
| CHIC #054 | Knossos | bar | tier-2 | 10 | 9 | 0 | 1 | 0.9000 | `[?:wa] te / [?] / NUM:110 / je pa de / NUM:170 / [?] / NUM:160 / NUM:150 / NUM:50 / [?:#029] de / NUM:450 / ra ro ke / NUM:60` |
| CHIC #054 | Knossos | bar | tier-3 | 10 | 9 | 0 | 1 | 0.9000 | `[?:wa] te / [?] / NUM:110 / je pa de / NUM:170 / [?] / NUM:160 / NUM:150 / NUM:50 / [?:#029] de / NUM:450 / ra ro ke / NUM:60` |
| CHIC #054 | Knossos | bar | tier-4 | 10 | 9 | 1 | 0 | 1.0000 | `[?:wa] te / [?] / NUM:110 / je pa de / NUM:170 / [?] / NUM:160 / NUM:150 / NUM:50 / [?:LIQUID:#029] de / NUM:450 / ra ro ke / NUM:60` |
| CHIC #055 | Knossos | bar | tier-1 | 5 | 2 | 0 | 3 | 0.4000 | `[?:#033] #018 ra [?] / [?:ra] #058 [?] / [?] / NUM:10` |
| CHIC #055 | Knossos | bar | tier-2 | 5 | 2 | 0 | 3 | 0.4000 | `[?:#033] #018 ra [?] / [?:ra] #058 [?] / [?] / NUM:10` |
| CHIC #055 | Knossos | bar | tier-3 | 5 | 2 | 2 | 1 | 0.8000 | `[?:GLIDE:#033] #018 ra [?] / [?:ra] [STOP:#058] [?] / [?] / NUM:10` |
| CHIC #055 | Knossos | bar | tier-4 | 5 | 2 | 3 | 0 | 1.0000 | `[?:GLIDE:#033] [GLIDE:#018] ra [?] / [?:ra] [STOP:#058] [?] / [?] / NUM:10` |
| CHIC #056 | Knossos | bar | tier-1 | 17 | 16 | 0 | 1 | 0.9412 | `ra ro ke / ki de / NUM:85 / NUM:800 / NUM:540 / NUM:44 / NUM:44 / wa je ra / NUM:800 / ki de / NUM:83 / #026 te / wa je i / NUM:483 / ki de / NUM:46` |
| CHIC #056 | Knossos | bar | tier-2 | 17 | 16 | 0 | 1 | 0.9412 | `ra ro ke / ki de / NUM:85 / NUM:800 / NUM:540 / NUM:44 / NUM:44 / wa je ra / NUM:800 / ki de / NUM:83 / #026 te / wa je i / NUM:483 / ki de / NUM:46` |
| CHIC #056 | Knossos | bar | tier-3 | 17 | 16 | 0 | 1 | 0.9412 | `ra ro ke / ki de / NUM:85 / NUM:800 / NUM:540 / NUM:44 / NUM:44 / wa je ra / NUM:800 / ki de / NUM:83 / #026 te / wa je i / NUM:483 / ki de / NUM:46` |
| CHIC #056 | Knossos | bar | tier-4 | 17 | 16 | 0 | 1 | 0.9412 | `ra ro ke / ki de / NUM:85 / NUM:800 / NUM:540 / NUM:44 / NUM:44 / wa je ra / NUM:800 / ki de / NUM:83 / #026 te / wa je i / NUM:483 / ki de / NUM:46` |
| CHIC #057 | Knossos | bar | tier-1 | 13 | 4 | 0 | 9 | 0.3077 | `wa #029 #032 #011 / NUM:10 / #079 #032 pa / NUM:20 / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50` |
| CHIC #057 | Knossos | bar | tier-2 | 13 | 6 | 0 | 7 | 0.4615 | `wa #029 ki #011 / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50` |
| CHIC #057 | Knossos | bar | tier-3 | 13 | 6 | 3 | 4 | 0.6923 | `wa #029 ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] #034 / NUM:20 / [LIQUID:#011] #029 [LIQUID:#037] / NUM:50` |
| CHIC #057 | Knossos | bar | tier-4 | 13 | 6 | 6 | 1 | 0.9231 | `wa [LIQUID:#029] ki [LIQUID:#011] / NUM:10 / #079 ki pa / NUM:20 / i [?:mu] [LIQUID:#034] / NUM:20 / [LIQUID:#011] [LIQUID:#029] [LIQUID:#037] / NUM:50` |
| CHIC #058 | Knossos | bar | tier-1 | 22 | 10 | 0 | 12 | 0.4545 | `wa mu te / NUM:640 / #047 ra ro / NUM:80 / #078 #032 #034 / NUM:50 / [?:ja] ra #005 / NUM:60 / #034 [?:#002] / NUM:20 / ti i #002 / NUM:90 / #078 #032 ra [?:#023] [?:#045] / NUM:30` |
| CHIC #058 | Knossos | bar | tier-2 | 22 | 12 | 0 | 10 | 0.5455 | `wa mu te / NUM:640 / #047 ra ro / NUM:80 / #078 ki #034 / NUM:50 / [?:ja] ra #005 / NUM:60 / #034 [?:#002] / NUM:20 / ti i #002 / NUM:90 / #078 ki ra [?:#023] [?:#045] / NUM:30` |
| CHIC #058 | Knossos | bar | tier-3 | 22 | 12 | 6 | 4 | 0.8182 | `wa mu te / NUM:640 / #047 ra ro / NUM:80 / [STOP:#078] ki #034 / NUM:50 / [?:ja] ra [STOP:#005] / NUM:60 / #034 [?:LIQUID:#002] / NUM:20 / ti i [LIQUID:#002] / NUM:90 / [STOP:#078] ki ra [?:#023] [?:STOP:#045] / NUM:30` |
| CHIC #058 | Knossos | bar | tier-4 | 22 | 12 | 10 | 0 | 1.0000 | `wa mu te / NUM:640 / [LIQUID:#047] ra ro / NUM:80 / [STOP:#078] ki [LIQUID:#034] / NUM:50 / [?:ja] ra [STOP:#005] / NUM:60 / [LIQUID:#034] [?:LIQUID:#002] / NUM:20 / ti i [LIQUID:#002] / NUM:90 / [STOP:#078] ki ra [?:LIQUID:#023] [?:STOP:#045] / NUM:30` |
| CHIC #059 | Knossos | bar | tier-1 | 35 | 22 | 0 | 13 | 0.6286 | `ti de de / ki #005 / NUM:40 [?] / i #071 #066 ra / NUM:400 [?] / #060 [?:pa] / ti #029 #002 / [?:pa] [?] / [?] / [?:#001] NUM:30 / [?] / NUM:2300 [?] / [?] / [?:IDEO:#300] / [?] / [?:ro] #021 te / ki de [?] / #072 de / NUM:11 / ki de / [?:#006] / ke #036 [?] / [?] / [?] / ti de #007 wa [?] / [?:#056] ra te / NUM:11 / [?]` |
| CHIC #059 | Knossos | bar | tier-2 | 35 | 23 | 0 | 12 | 0.6571 | `ti de de / ki #005 / NUM:40 [?] / i #071 #066 ra / NUM:400 [?] / #060 [?:pa] / ti #029 #002 / [?:pa] [?] / [?] / [?:wa] NUM:30 / [?] / NUM:2300 [?] / [?] / [?:IDEO:#300] / [?] / [?:ro] #021 te / ki de [?] / #072 de / NUM:11 / ki de / [?:#006] / ke #036 [?] / [?] / [?] / ti de #007 wa [?] / [?:#056] ra te / NUM:11 / [?]` |
| CHIC #059 | Knossos | bar | tier-3 | 35 | 23 | 9 | 3 | 0.9143 | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] / [STOP:#060] [?:pa] / ti #029 [LIQUID:#002] / [?:pa] [?] / [?] / [?:wa] NUM:30 / [?] / NUM:2300 [?] / [?] / [?:IDEO:#300] / [?] / [?:ro] [NASAL:#021] te / ki de [?] / [STOP:#072] de / NUM:11 / ki de / [?:GLIDE:#006] / ke #036 [?] / [?] / [?] / ti de [VOWEL:#007] wa [?] / [?:STOP:#056] ra te / NUM:11 / [?]` |
| CHIC #059 | Knossos | bar | tier-4 | 35 | 23 | 11 | 1 | 0.9714 | `ti de de / ki [STOP:#005] / NUM:40 [?] / i #071 [STOP:#066] ra / NUM:400 [?] / [STOP:#060] [?:pa] / ti [LIQUID:#029] [LIQUID:#002] / [?:pa] [?] / [?] / [?:wa] NUM:30 / [?] / NUM:2300 [?] / [?] / [?:IDEO:#300] / [?] / [?:ro] [NASAL:#021] te / ki de [?] / [STOP:#072] de / NUM:11 / ki de / [?:GLIDE:#006] / ke [GLIDE:#036] [?] / [?] / [?] / ti de [VOWEL:#007] wa [?] / [?:STOP:#056] ra te / NUM:11 / [?]` |
| CHIC #060 | Knossos | bar | tier-1 | 7 | 5 | 0 | 2 | 0.7143 | `ti de ni #003 [?] / [?:#009] mu te [?]` |
| CHIC #060 | Knossos | bar | tier-2 | 7 | 5 | 0 | 2 | 0.7143 | `ti de ni #003 [?] / [?:#009] mu te [?]` |
| CHIC #060 | Knossos | bar | tier-3 | 7 | 5 | 1 | 1 | 0.8571 | `ti de ni #003 [?] / [?:STOP:#009] mu te [?]` |
| CHIC #060 | Knossos | bar | tier-4 | 7 | 5 | 2 | 0 | 1.0000 | `ti de ni [GLIDE:#003] [?] / [?:STOP:#009] mu te [?]` |
| CHIC #061 | Knossos | bar | tier-1 | 23 | 10 | 0 | 13 | 0.4348 | `[?:#023] #032 / NUM:1 / wa #056 ro / NUM:1 / [?] #034 #056 / NUM:1 / #037 #011 #029 / NUM:1 / [?] / [?] / [?] / ra ke [?:#009] / NUM:1 / [?:ke] de / [?:#001] / #034 #056 / ke de / NUM:1 / #056 ra ra / NUM:12` |
| CHIC #061 | Knossos | bar | tier-2 | 23 | 12 | 0 | 11 | 0.5217 | `[?:#023] ki / NUM:1 / wa #056 ro / NUM:1 / [?] #034 #056 / NUM:1 / #037 #011 #029 / NUM:1 / [?] / [?] / [?] / ra ke [?:#009] / NUM:1 / [?:ke] de / [?:wa] / #034 #056 / ke de / NUM:1 / #056 ra ra / NUM:12` |
| CHIC #061 | Knossos | bar | tier-3 | 23 | 12 | 7 | 4 | 0.8261 | `[?:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] #034 [STOP:#056] / NUM:1 / [LIQUID:#037] [LIQUID:#011] #029 / NUM:1 / [?] / [?] / [?] / ra ke [?:STOP:#009] / NUM:1 / [?:ke] de / [?:wa] / #034 [STOP:#056] / ke de / NUM:1 / [STOP:#056] ra ra / NUM:12` |
| CHIC #061 | Knossos | bar | tier-4 | 23 | 12 | 11 | 0 | 1.0000 | `[?:LIQUID:#023] ki / NUM:1 / wa [STOP:#056] ro / NUM:1 / [?] [LIQUID:#034] [STOP:#056] / NUM:1 / [LIQUID:#037] [LIQUID:#011] [LIQUID:#029] / NUM:1 / [?] / [?] / [?] / ra ke [?:STOP:#009] / NUM:1 / [?:ke] de / [?:wa] / [LIQUID:#034] [STOP:#056] / ke de / NUM:1 / [STOP:#056] ra ra / NUM:12` |
| CHIC #062 | Knossos | bar | tier-1 | 14 | 12 | 0 | 2 | 0.8571 | `[?:mu] te / wa #034 de / [?] / [?:#001] NUM:40 / [?] mu te / [?] / NUM:30 / [?:wa] mu te / [?] / NUM:540 / [?:wa] mu te` |
| CHIC #062 | Knossos | bar | tier-2 | 14 | 13 | 0 | 1 | 0.9286 | `[?:mu] te / wa #034 de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM:30 / [?:wa] mu te / [?] / NUM:540 / [?:wa] mu te` |
| CHIC #062 | Knossos | bar | tier-3 | 14 | 13 | 0 | 1 | 0.9286 | `[?:mu] te / wa #034 de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM:30 / [?:wa] mu te / [?] / NUM:540 / [?:wa] mu te` |
| CHIC #062 | Knossos | bar | tier-4 | 14 | 13 | 1 | 0 | 1.0000 | `[?:mu] te / wa [LIQUID:#034] de / [?] / [?:wa] NUM:40 / [?] mu te / [?] / NUM:30 / [?:wa] mu te / [?] / NUM:540 / [?:wa] mu te` |
| CHIC #063 | Knossos | bar | tier-1 | 13 | 10 | 0 | 3 | 0.7692 | `[?:#006] je ke / NUM:105 [?] / [?:ni] #006 / NUM:3 / ki de [?] / [?:je] me / NUM:20 [?] / [?] / [?] / [?:de] te / NUM:20 [?] / [?:me] #006 [?]` |
| CHIC #063 | Knossos | bar | tier-2 | 13 | 10 | 0 | 3 | 0.7692 | `[?:#006] je ke / NUM:105 [?] / [?:ni] #006 / NUM:3 / ki de [?] / [?:je] me / NUM:20 [?] / [?] / [?] / [?:de] te / NUM:20 [?] / [?:me] #006 [?]` |
| CHIC #063 | Knossos | bar | tier-3 | 13 | 10 | 3 | 0 | 1.0000 | `[?:GLIDE:#006] je ke / NUM:105 [?] / [?:ni] [GLIDE:#006] / NUM:3 / ki de [?] / [?:je] me / NUM:20 [?] / [?] / [?] / [?:de] te / NUM:20 [?] / [?:me] [GLIDE:#006] [?]` |
| CHIC #063 | Knossos | bar | tier-4 | 13 | 10 | 3 | 0 | 1.0000 | `[?:GLIDE:#006] je ke / NUM:105 [?] / [?:ni] [GLIDE:#006] / NUM:3 / ki de [?] / [?:je] me / NUM:20 [?] / [?] / [?] / [?:de] te / NUM:20 [?] / [?:me] [GLIDE:#006] [?]` |
| CHIC #064 | Knossos | bar | tier-1 | 1 | 0 | 0 | 1 | 0.0000 | `NUM:2030 [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / NUM:110 [?:#002] / [?]` |
| CHIC #064 | Knossos | bar | tier-2 | 1 | 0 | 0 | 1 | 0.0000 | `NUM:2030 [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / NUM:110 [?:#002] / [?]` |
| CHIC #064 | Knossos | bar | tier-3 | 1 | 0 | 1 | 0 | 1.0000 | `NUM:2030 [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / NUM:110 [?:LIQUID:#002] / [?]` |
| CHIC #064 | Knossos | bar | tier-4 | 1 | 0 | 1 | 0 | 1.0000 | `NUM:2030 [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / NUM:110 [?:LIQUID:#002] / [?]` |
| CHIC #065 | Knossos | bar | tier-1 | 14 | 5 | 0 | 9 | 0.3571 | `#072 de #071 #050 #005 #063 / NUM:1 / #047 me / NUM:1 / ke ro / NUM:1 / NUM:42 / IDEO:#161 / IDEO:#161 / NUM:300 / [?:IDEO:#152] / NUM:1 / IDEO:#156 / NUM:2 / IDEO:#180 / NUM:32 / IDEO:#152 / NUM:1 / #033 #047 / IDEO:#178 / #072 de / NUM:1 / IDEO:#158 / IDEO:#167 / IDEO:#155` |
| CHIC #065 | Knossos | bar | tier-2 | 14 | 5 | 0 | 9 | 0.3571 | `#072 de #071 #050 #005 #063 / NUM:1 / #047 me / NUM:1 / ke ro / NUM:1 / NUM:42 / IDEO:#161 / IDEO:#161 / NUM:300 / [?:IDEO:#152] / NUM:1 / IDEO:#156 / NUM:2 / IDEO:#180 / NUM:32 / IDEO:#152 / NUM:1 / #033 #047 / IDEO:#178 / #072 de / NUM:1 / IDEO:#158 / IDEO:#167 / IDEO:#155` |
| CHIC #065 | Knossos | bar | tier-3 | 14 | 5 | 6 | 3 | 0.7857 | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / #047 me / NUM:1 / ke ro / NUM:1 / NUM:42 / IDEO:#161 / IDEO:#161 / NUM:300 / [?:IDEO:#152] / NUM:1 / IDEO:#156 / NUM:2 / IDEO:#180 / NUM:32 / IDEO:#152 / NUM:1 / [GLIDE:#033] #047 / IDEO:#178 / [STOP:#072] de / NUM:1 / IDEO:#158 / IDEO:#167 / IDEO:#155` |
| CHIC #065 | Knossos | bar | tier-4 | 14 | 5 | 8 | 1 | 0.9286 | `[STOP:#072] de #071 [GLIDE:#050] [STOP:#005] [GLIDE:#063] / NUM:1 / [LIQUID:#047] me / NUM:1 / ke ro / NUM:1 / NUM:42 / IDEO:#161 / IDEO:#161 / NUM:300 / [?:IDEO:#152] / NUM:1 / IDEO:#156 / NUM:2 / IDEO:#180 / NUM:32 / IDEO:#152 / NUM:1 / [GLIDE:#033] [LIQUID:#047] / IDEO:#178 / [STOP:#072] de / NUM:1 / IDEO:#158 / IDEO:#167 / IDEO:#155` |
| CHIC #066 | Knossos | bar | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:#005] #063 / NUM:1 / [?:IDEO:#182] / NUM:12 / IDEO:#161` |
| CHIC #066 | Knossos | bar | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:#005] #063 / NUM:1 / [?:IDEO:#182] / NUM:12 / IDEO:#161` |
| CHIC #066 | Knossos | bar | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:STOP:#005] [GLIDE:#063] / NUM:1 / [?:IDEO:#182] / NUM:12 / IDEO:#161` |
| CHIC #066 | Knossos | bar | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[?] / IDEO:#167 / IDEO:#155 / [?] / [?:STOP:#005] [GLIDE:#063] / NUM:1 / [?:IDEO:#182] / NUM:12 / IDEO:#161` |
| CHIC #067 | Knossos | bar | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 / NUM:1 / [?:IDEO:#152] / NUM:1 / ke ro / NUM:1 / [?]` |
| CHIC #067 | Knossos | bar | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 / NUM:1 / [?:IDEO:#152] / NUM:1 / ke ro / NUM:1 / [?]` |
| CHIC #067 | Knossos | bar | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 / NUM:1 / [?:IDEO:#152] / NUM:1 / ke ro / NUM:1 / [?]` |
| CHIC #067 | Knossos | bar | tier-4 | 3 | 2 | 0 | 1 | 0.6667 | `[?] / IDEO:#171 / [?:#100] / IDEO:#155 / IDEO:#156 / NUM:1 / [?] / IDEO:#180 / NUM:1 / [?:IDEO:#152] / NUM:1 / ke ro / NUM:1 / [?]` |
| CHIC #068 | Knossos | tablet | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156] / NUM:10 / [?:IDEO:#151] / NUM:5 / IDEO:#175 / [?:IDEO:#153] / NUM:15 / [?:IDEO:#154] / NUM:8` |
| CHIC #068 | Knossos | tablet | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156] / NUM:10 / [?:IDEO:#151] / NUM:5 / IDEO:#175 / [?:IDEO:#153] / NUM:15 / [?:IDEO:#154] / NUM:8` |
| CHIC #068 | Knossos | tablet | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156] / NUM:10 / [?:IDEO:#151] / NUM:5 / IDEO:#175 / [?:IDEO:#153] / NUM:15 / [?:IDEO:#154] / NUM:8` |
| CHIC #068 | Knossos | tablet | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156] / NUM:10 / [?:IDEO:#151] / NUM:5 / IDEO:#175 / [?:IDEO:#153] / NUM:15 / [?:IDEO:#154] / NUM:8` |
| CHIC #069 | Knossos | tablet | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| CHIC #069 | Knossos | tablet | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| CHIC #069 | Knossos | tablet | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| CHIC #069 | Knossos | tablet | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `[?] to [?] / [?:to] ra [?] / [?] [?]` |
| CHIC #070 | Mallia | cone | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `wa #034 [?:#007] #040` |
| CHIC #070 | Mallia | cone | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `wa #034 [?:#007] #040` |
| CHIC #070 | Mallia | cone | tier-3 | 4 | 1 | 2 | 1 | 0.7500 | `wa #034 [?:VOWEL:#007] [STOP:#040]` |
| CHIC #070 | Mallia | cone | tier-4 | 4 | 1 | 3 | 0 | 1.0000 | `wa [LIQUID:#034] [?:VOWEL:#007] [STOP:#040]` |
| CHIC #071 | Mallia | cone | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `#022 #056 ra te` |
| CHIC #071 | Mallia | cone | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `#022 #056 ra te` |
| CHIC #071 | Mallia | cone | tier-3 | 4 | 2 | 1 | 1 | 0.7500 | `#022 [STOP:#056] ra te` |
| CHIC #071 | Mallia | cone | tier-4 | 4 | 2 | 1 | 1 | 0.7500 | `#022 [STOP:#056] ra te` |
| CHIC #072 | Mallia | medallion | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#011 i / NUM:29` |
| CHIC #072 | Mallia | medallion | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#011 i / NUM:29` |
| CHIC #072 | Mallia | medallion | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#011] i / NUM:29` |
| CHIC #072 | Mallia | medallion | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#011] i / NUM:29` |
| CHIC #073 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#027 #034 ra` |
| CHIC #073 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#027 #034 ra` |
| CHIC #073 | Mallia | medallion | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `[GLIDE:#027] #034 ra` |
| CHIC #073 | Mallia | medallion | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[GLIDE:#027] [LIQUID:#034] ra` |
| CHIC #074 | Mallia | medallion | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `wa ra #060 ki` |
| CHIC #074 | Mallia | medallion | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `wa ra #060 ki` |
| CHIC #074 | Mallia | medallion | tier-3 | 4 | 3 | 1 | 0 | 1.0000 | `wa ra [STOP:#060] ki` |
| CHIC #074 | Mallia | medallion | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `wa ra [STOP:#060] ki` |
| CHIC #075 | Mallia | medallion | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#060 #009` |
| CHIC #075 | Mallia | medallion | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#060 #009` |
| CHIC #075 | Mallia | medallion | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[STOP:#060] [STOP:#009]` |
| CHIC #075 | Mallia | medallion | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[STOP:#060] [STOP:#009]` |
| CHIC #076 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#008 #056 pa` |
| CHIC #076 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#008 #056 pa` |
| CHIC #076 | Mallia | medallion | tier-3 | 3 | 1 | 2 | 0 | 1.0000 | `[GLIDE:#008] [STOP:#056] pa` |
| CHIC #076 | Mallia | medallion | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[GLIDE:#008] [STOP:#056] pa` |
| CHIC #077 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `[?:ro] #055 #081` |
| CHIC #077 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `[?:ro] #055 #081` |
| CHIC #077 | Mallia | medallion | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `[?:ro] [STOP:#055] #081` |
| CHIC #077 | Mallia | medallion | tier-4 | 3 | 1 | 1 | 1 | 0.6667 | `[?:ro] [STOP:#055] #081` |
| CHIC #078 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#083 [?:#047] ke [?]` |
| CHIC #078 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#083 [?:#047] ke [?]` |
| CHIC #078 | Mallia | medallion | tier-3 | 3 | 1 | 0 | 2 | 0.3333 | `#083 [?:#047] ke [?]` |
| CHIC #078 | Mallia | medallion | tier-4 | 3 | 1 | 1 | 1 | 0.6667 | `#083 [?:LIQUID:#047] ke [?]` |
| CHIC #079 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#068 [?:ma] #015` |
| CHIC #079 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#068 [?:ma] #015` |
| CHIC #079 | Mallia | medallion | tier-3 | 3 | 1 | 0 | 2 | 0.3333 | `#068 [?:ma] #015` |
| CHIC #079 | Mallia | medallion | tier-4 | 3 | 1 | 1 | 1 | 0.6667 | `[LIQUID:#068] [?:ma] #015` |
| CHIC #080 | Mallia | medallion | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#012 [?:ro] #082` |
| CHIC #080 | Mallia | medallion | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `wa [?:ro] #082` |
| CHIC #080 | Mallia | medallion | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `wa [?:ro] #082` |
| CHIC #080 | Mallia | medallion | tier-4 | 3 | 2 | 0 | 1 | 0.6667 | `wa [?:ro] #082` |
| CHIC #081 | Mallia | medallion | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ti ra` |
| CHIC #081 | Mallia | medallion | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ti ra` |
| CHIC #081 | Mallia | medallion | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ti ra` |
| CHIC #081 | Mallia | medallion | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ti ra` |
| CHIC #082 | Mallia | medallion | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `#020 a ni` |
| CHIC #082 | Mallia | medallion | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `#020 a ni` |
| CHIC #082 | Mallia | medallion | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `[VOWEL:#020] a ni` |
| CHIC #082 | Mallia | medallion | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[VOWEL:#020] a ni` |
| CHIC #083 | Mallia | medallion | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#030 #034` |
| CHIC #083 | Mallia | medallion | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#030 #034` |
| CHIC #083 | Mallia | medallion | tier-3 | 2 | 0 | 0 | 2 | 0.0000 | `#030 #034` |
| CHIC #083 | Mallia | medallion | tier-4 | 2 | 0 | 1 | 1 | 0.5000 | `#030 [LIQUID:#034]` |
| CHIC #084 | Mallia | medallion | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `[?] a [?]` |
| CHIC #084 | Mallia | medallion | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `[?] a [?]` |
| CHIC #084 | Mallia | medallion | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `[?] a [?]` |
| CHIC #084 | Mallia | medallion | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `[?] a [?]` |
| CHIC #085 | Mallia | lame | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#068 te` |
| CHIC #085 | Mallia | lame | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#068 te` |
| CHIC #085 | Mallia | lame | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `#068 te` |
| CHIC #085 | Mallia | lame | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#068] te` |
| CHIC #086 | Mallia | lame | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#068 [?:a] [?]` |
| CHIC #086 | Mallia | lame | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#068 [?:a] [?]` |
| CHIC #086 | Mallia | lame | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `#068 [?:a] [?]` |
| CHIC #086 | Mallia | lame | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[LIQUID:#068] [?:a] [?]` |
| CHIC #087 | Mallia | lame | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#064 #096 [?]` |
| CHIC #087 | Mallia | lame | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#064 #096 [?]` |
| CHIC #087 | Mallia | lame | tier-3 | 2 | 0 | 0 | 2 | 0.0000 | `#064 #096 [?]` |
| CHIC #087 | Mallia | lame | tier-4 | 2 | 0 | 0 | 2 | 0.0000 | `#064 #096 [?]` |
| CHIC #088 | Mallia | lame | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ro] ni` |
| CHIC #088 | Mallia | lame | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ro] ni` |
| CHIC #088 | Mallia | lame | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ro] ni` |
| CHIC #088 | Mallia | lame | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ro] ni` |
| CHIC #089 | Mallia | lame | tier-1 | 10 | 4 | 0 | 6 | 0.4000 | `ki de #023 / #034 ni #084 / #051 #051 #051 ni` |
| CHIC #089 | Mallia | lame | tier-2 | 10 | 4 | 0 | 6 | 0.4000 | `ki de #023 / #034 ni #084 / #051 #051 #051 ni` |
| CHIC #089 | Mallia | lame | tier-3 | 10 | 4 | 0 | 6 | 0.4000 | `ki de #023 / #034 ni #084 / #051 #051 #051 ni` |
| CHIC #089 | Mallia | lame | tier-4 | 10 | 4 | 5 | 1 | 0.9000 | `ki de [LIQUID:#023] / [LIQUID:#034] ni #084 / [GLIDE:#051] [GLIDE:#051] [GLIDE:#051] ni` |
| CHIC #090 | Mallia | lame | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `a i #007 #051 / NUM:0` |
| CHIC #090 | Mallia | lame | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `a i #007 #051 / NUM:0` |
| CHIC #090 | Mallia | lame | tier-3 | 4 | 2 | 1 | 1 | 0.7500 | `a i [VOWEL:#007] #051 / NUM:0` |
| CHIC #090 | Mallia | lame | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `a i [VOWEL:#007] [GLIDE:#051] / NUM:0` |
| CHIC #091 | Mallia | lame | tier-1 | 6 | 4 | 0 | 2 | 0.6667 | `wa pa #009 [?] / ra ro #034 [?]` |
| CHIC #091 | Mallia | lame | tier-2 | 6 | 4 | 0 | 2 | 0.6667 | `wa pa #009 [?] / ra ro #034 [?]` |
| CHIC #091 | Mallia | lame | tier-3 | 6 | 4 | 1 | 1 | 0.8333 | `wa pa [STOP:#009] [?] / ra ro #034 [?]` |
| CHIC #091 | Mallia | lame | tier-4 | 6 | 4 | 2 | 0 | 1.0000 | `wa pa [STOP:#009] [?] / ra ro [LIQUID:#034] [?]` |
| CHIC #092 | Mallia | lame | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `[?:te] #080 #032 [?] / [?] / [?:me] [?]` |
| CHIC #092 | Mallia | lame | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `[?:te] #080 ki [?] / [?] / [?:me] [?]` |
| CHIC #092 | Mallia | lame | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `[?:te] #080 ki [?] / [?] / [?:me] [?]` |
| CHIC #092 | Mallia | lame | tier-4 | 4 | 3 | 0 | 1 | 0.7500 | `[?:te] #080 ki [?] / [?] / [?:me] [?]` |
| CHIC #093 | Mallia | lame | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?]` |
| CHIC #093 | Mallia | lame | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?]` |
| CHIC #093 | Mallia | lame | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?]` |
| CHIC #093 | Mallia | lame | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?]` |
| CHIC #097 | Mallia | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `NUM:2 / #040 ra i` |
| CHIC #097 | Mallia | crescent | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `NUM:2 / #040 ra i` |
| CHIC #097 | Mallia | crescent | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `NUM:2 / [STOP:#040] ra i` |
| CHIC #097 | Mallia | crescent | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `NUM:2 / [STOP:#040] ra i` |
| CHIC #098 | Mallia | medallion | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `[?:#072] i #007 a` |
| CHIC #098 | Mallia | medallion | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `[?:#072] i #007 a` |
| CHIC #098 | Mallia | medallion | tier-3 | 4 | 2 | 2 | 0 | 1.0000 | `[?:STOP:#072] i [VOWEL:#007] a` |
| CHIC #098 | Mallia | medallion | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `[?:STOP:#072] i [VOWEL:#007] a` |
| CHIC #103 | Mallia | medallion | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `[?:ra] #055 je [?:#056] [?] / [?:IDEO:#163] [?]` |
| CHIC #103 | Mallia | medallion | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `[?:ra] #055 je [?:#056] [?] / [?:IDEO:#163] [?]` |
| CHIC #103 | Mallia | medallion | tier-3 | 4 | 2 | 2 | 0 | 1.0000 | `[?:ra] [STOP:#055] je [?:STOP:#056] [?] / [?:IDEO:#163] [?]` |
| CHIC #103 | Mallia | medallion | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `[?:ra] [STOP:#055] je [?:STOP:#056] [?] / [?:IDEO:#163] [?]` |
| CHIC #104 | Mallia | medallion | tier-1 | 3 | 0 | 0 | 3 | 0.0000 | `#032 #009 #056 / IDEO:#168 / NUM:100` |
| CHIC #104 | Mallia | medallion | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `ki #009 #056 / IDEO:#168 / NUM:100` |
| CHIC #104 | Mallia | medallion | tier-3 | 3 | 1 | 2 | 0 | 1.0000 | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` |
| CHIC #104 | Mallia | medallion | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `ki [STOP:#009] [STOP:#056] / IDEO:#168 / NUM:100` |
| CHIC #105 | Mallia | lame | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `[?] a i / [?] pa #035 / NUM:210` |
| CHIC #105 | Mallia | lame | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `[?] a i / [?] pa #035 / NUM:210` |
| CHIC #105 | Mallia | lame | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `[?] a i / [?] pa #035 / NUM:210` |
| CHIC #105 | Mallia | lame | tier-4 | 4 | 3 | 0 | 1 | 0.7500 | `[?] a i / [?] pa #035 / NUM:210` |
| CHIC #106 | Mallia | lame | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:pa] de` |
| CHIC #106 | Mallia | lame | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:pa] de` |
| CHIC #106 | Mallia | lame | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:pa] de` |
| CHIC #106 | Mallia | lame | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:pa] de` |
| CHIC #107 | Mallia | lame | tier-1 | 1 | 0 | 0 | 1 | 0.0000 | `[?] #020` |
| CHIC #107 | Mallia | lame | tier-2 | 1 | 0 | 0 | 1 | 0.0000 | `[?] #020` |
| CHIC #107 | Mallia | lame | tier-3 | 1 | 0 | 1 | 0 | 1.0000 | `[?] [VOWEL:#020]` |
| CHIC #107 | Mallia | lame | tier-4 | 1 | 0 | 1 | 0 | 1.0000 | `[?] [VOWEL:#020]` |
| CHIC #108 | Mallia | lame | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#169 / NUM:5 / [?] / [?] / NUM:6` |
| CHIC #108 | Mallia | lame | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#169 / NUM:5 / [?] / [?] / NUM:6` |
| CHIC #108 | Mallia | lame | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#169 / NUM:5 / [?] / [?] / NUM:6` |
| CHIC #108 | Mallia | lame | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#169 / NUM:5 / [?] / [?] / NUM:6` |
| CHIC #109 | Mallia | lame | tier-1 | 5 | 2 | 0 | 3 | 0.4000 | `ke #034 / #003 [?] / #036 ke [?]` |
| CHIC #109 | Mallia | lame | tier-2 | 5 | 2 | 0 | 3 | 0.4000 | `ke #034 / #003 [?] / #036 ke [?]` |
| CHIC #109 | Mallia | lame | tier-3 | 5 | 2 | 0 | 3 | 0.4000 | `ke #034 / #003 [?] / #036 ke [?]` |
| CHIC #109 | Mallia | lame | tier-4 | 5 | 2 | 3 | 0 | 1.0000 | `ke [LIQUID:#034] / [GLIDE:#003] [?] / [GLIDE:#036] ke [?]` |
| CHIC #110 | Mallia | lame | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `ki #040 [?] / [?:#085] / [?]` |
| CHIC #110 | Mallia | lame | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `ki #040 [?] / [?:#085] / [?]` |
| CHIC #110 | Mallia | lame | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `ki [STOP:#040] [?] / [?:#085] / [?]` |
| CHIC #110 | Mallia | lame | tier-4 | 3 | 1 | 1 | 1 | 0.6667 | `ki [STOP:#040] [?] / [?:#085] / [?]` |
| CHIC #111 | Mallia | bar | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `[?] / [?] / [?:#060] / [?] / [?] [?] / [?] / [?:#040] / [?]` |
| CHIC #111 | Mallia | bar | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `[?] / [?] / [?:#060] / [?] / [?] [?] / [?] / [?:#040] / [?]` |
| CHIC #111 | Mallia | bar | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[?] / [?] / [?:STOP:#060] / [?] / [?] [?] / [?] / [?:STOP:#040] / [?]` |
| CHIC #111 | Mallia | bar | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[?] / [?] / [?:STOP:#060] / [?] / [?] [?] / [?] / [?:STOP:#040] / [?]` |
| CHIC #113 | Mallia | bar | tier-1 | 27 | 15 | 0 | 12 | 0.5556 | `[?:#047] #002 te / de i [?] / #050 ra ke / NUM:10 / NUM:57 [?] / [?] #056 ma / NUM:20 / to #090 / #012 #050 / wa de a a [?] / [?:#040] pa / je #023 wa #063 #060 / #008 ra [?]` |
| CHIC #113 | Mallia | bar | tier-2 | 27 | 16 | 0 | 11 | 0.5926 | `[?:#047] #002 te / de i [?] / #050 ra ke / NUM:10 / NUM:57 [?] / [?] #056 ma / NUM:20 / to #090 / wa #050 / wa de a a [?] / [?:#040] pa / je #023 wa #063 #060 / #008 ra [?]` |
| CHIC #113 | Mallia | bar | tier-3 | 27 | 16 | 8 | 3 | 0.8889 | `[?:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / NUM:57 [?] / [?] [STOP:#056] ma / NUM:20 / to #090 / wa [GLIDE:#050] / wa de a a [?] / [?:STOP:#040] pa / je #023 wa [GLIDE:#063] [STOP:#060] / [GLIDE:#008] ra [?]` |
| CHIC #113 | Mallia | bar | tier-4 | 27 | 16 | 10 | 1 | 0.9630 | `[?:LIQUID:#047] [LIQUID:#002] te / de i [?] / [GLIDE:#050] ra ke / NUM:10 / NUM:57 [?] / [?] [STOP:#056] ma / NUM:20 / to #090 / wa [GLIDE:#050] / wa de a a [?] / [?:STOP:#040] pa / je [LIQUID:#023] wa [GLIDE:#063] [STOP:#060] / [GLIDE:#008] ra [?]` |
| CHIC #115 | Mallia | bar | tier-1 | 5 | 2 | 0 | 3 | 0.4000 | `[?:#035] me #034 / [?] pa #060 / [?] / [?]` |
| CHIC #115 | Mallia | bar | tier-2 | 5 | 2 | 0 | 3 | 0.4000 | `[?:#035] me #034 / [?] pa #060 / [?] / [?]` |
| CHIC #115 | Mallia | bar | tier-3 | 5 | 2 | 1 | 2 | 0.6000 | `[?:#035] me #034 / [?] pa [STOP:#060] / [?] / [?]` |
| CHIC #115 | Mallia | bar | tier-4 | 5 | 2 | 2 | 1 | 0.8000 | `[?:#035] me [LIQUID:#034] / [?] pa [STOP:#060] / [?] / [?]` |
| CHIC #116 | Mallia | bar | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?] / [?]` |
| CHIC #116 | Mallia | bar | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?] / [?]` |
| CHIC #116 | Mallia | bar | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?] / [?]` |
| CHIC #116 | Mallia | bar | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / [?] / [?]` |
| CHIC #117 | Mallia | bar | tier-1 | 4 | 0 | 0 | 4 | 0.0000 | `[?:#055] [?:#020] [?] / [?:#011] [?:#040] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?]` |
| CHIC #117 | Mallia | bar | tier-2 | 4 | 0 | 0 | 4 | 0.0000 | `[?:#055] [?:#020] [?] / [?:#011] [?:#040] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?]` |
| CHIC #117 | Mallia | bar | tier-3 | 4 | 0 | 4 | 0 | 1.0000 | `[?:STOP:#055] [?:VOWEL:#020] [?] / [?:LIQUID:#011] [?:STOP:#040] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?]` |
| CHIC #117 | Mallia | bar | tier-4 | 4 | 0 | 4 | 0 | 1.0000 | `[?:STOP:#055] [?:VOWEL:#020] [?] / [?:LIQUID:#011] [?:STOP:#040] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?] / [?]` |
| CHIC #118 | Mallia | bar | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `#056 ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM:1 / [?] / [?] / [?:IDEO:#153] / NUM:1 / #040 je / IDEO:#177 / NUM:1 / IDEO:#173 / NUM:2 / IDEO:#155 / NUM:4 / IDEO:#156 / NUM:20 / IDEO:#179 / NUM:240 / IDEO:#161 / NUM:1 / IDEO:#162 / NUM:1` |
| CHIC #118 | Mallia | bar | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `#056 ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM:1 / [?] / [?] / [?:IDEO:#153] / NUM:1 / #040 je / IDEO:#177 / NUM:1 / IDEO:#173 / NUM:2 / IDEO:#155 / NUM:4 / IDEO:#156 / NUM:20 / IDEO:#179 / NUM:240 / IDEO:#161 / NUM:1 / IDEO:#162 / NUM:1` |
| CHIC #118 | Mallia | bar | tier-3 | 4 | 2 | 2 | 0 | 1.0000 | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM:1 / [?] / [?] / [?:IDEO:#153] / NUM:1 / [STOP:#040] je / IDEO:#177 / NUM:1 / IDEO:#173 / NUM:2 / IDEO:#155 / NUM:4 / IDEO:#156 / NUM:20 / IDEO:#179 / NUM:240 / IDEO:#161 / NUM:1 / IDEO:#162 / NUM:1` |
| CHIC #118 | Mallia | bar | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `[STOP:#056] ra / IDEO:#159 / NUM:10 / [?:IDEO:#171] / NUM:1 / IDEO:#172 / NUM:1 / [?] / [?] / [?:IDEO:#153] / NUM:1 / [STOP:#040] je / IDEO:#177 / NUM:1 / IDEO:#173 / NUM:2 / IDEO:#155 / NUM:4 / IDEO:#156 / NUM:20 / IDEO:#179 / NUM:240 / IDEO:#161 / NUM:1 / IDEO:#162 / NUM:1` |
| CHIC #120 | Mallia | tablet | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / NUM:100 / [?] / [?] / NUM:300` |
| CHIC #120 | Mallia | tablet | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / NUM:100 / [?] / [?] / NUM:300` |
| CHIC #120 | Mallia | tablet | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / NUM:100 / [?] / [?] / NUM:300` |
| CHIC #120 | Mallia | tablet | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?] / NUM:100 / [?] / [?] / NUM:300` |
| CHIC #121 | Mallia | bar | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `NUM:41 [?] / [?:pa] [?]` |
| CHIC #121 | Mallia | bar | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `NUM:41 [?] / [?:pa] [?]` |
| CHIC #121 | Mallia | bar | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `NUM:41 [?] / [?:pa] [?]` |
| CHIC #121 | Mallia | bar | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `NUM:41 [?] / [?:pa] [?]` |
| CHIC #123 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `ke #058` |
| CHIC #123 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `ke #058` |
| CHIC #123 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `ke [STOP:#058]` |
| CHIC #123 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `ke [STOP:#058]` |
| CHIC #124 | Knossos | crescent | tier-1 | 3 | 0 | 0 | 3 | 0.0000 | `#040 #029 #029` |
| CHIC #124 | Knossos | crescent | tier-2 | 3 | 0 | 0 | 3 | 0.0000 | `#040 #029 #029` |
| CHIC #124 | Knossos | crescent | tier-3 | 3 | 0 | 1 | 2 | 0.3333 | `[STOP:#040] #029 #029` |
| CHIC #124 | Knossos | crescent | tier-4 | 3 | 0 | 3 | 0 | 1.0000 | `[STOP:#040] [LIQUID:#029] [LIQUID:#029]` |
| CHIC #125 | Knossos | sealing | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `wa #052 [?:#034] #045 / NUM:0` |
| CHIC #125 | Knossos | sealing | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `wa #052 [?:#034] #045 / NUM:0` |
| CHIC #125 | Knossos | sealing | tier-3 | 4 | 1 | 1 | 2 | 0.5000 | `wa #052 [?:#034] [STOP:#045] / NUM:0` |
| CHIC #125 | Knossos | sealing | tier-4 | 4 | 1 | 3 | 0 | 1.0000 | `wa [LIQUID:#052] [?:LIQUID:#034] [STOP:#045] / NUM:0` |
| CHIC #126 | Mallia | nodulus | tier-1 | 5 | 0 | 0 | 5 | 0.0000 | `#036 #047 #009 #056 #062` |
| CHIC #126 | Mallia | nodulus | tier-2 | 5 | 0 | 0 | 5 | 0.0000 | `#036 #047 #009 #056 #062` |
| CHIC #126 | Mallia | nodulus | tier-3 | 5 | 0 | 2 | 3 | 0.4000 | `#036 #047 [STOP:#009] [STOP:#056] #062` |
| CHIC #126 | Mallia | nodulus | tier-4 | 5 | 0 | 5 | 0 | 1.0000 | `[GLIDE:#036] [LIQUID:#047] [STOP:#009] [STOP:#056] [GLIDE:#062]` |
| CHIC #127 | Mallia | nodulus | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#062 #040` |
| CHIC #127 | Mallia | nodulus | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#062 #040` |
| CHIC #127 | Mallia | nodulus | tier-3 | 2 | 0 | 1 | 1 | 0.5000 | `#062 [STOP:#040]` |
| CHIC #127 | Mallia | nodulus | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[GLIDE:#062] [STOP:#040]` |
| CHIC #128 | Mallia | nodulus | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `[?:#008] me #017 / NUM:0` |
| CHIC #128 | Mallia | nodulus | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `[?:#008] me #017 / NUM:0` |
| CHIC #128 | Mallia | nodulus | tier-3 | 3 | 1 | 2 | 0 | 1.0000 | `[?:GLIDE:#008] me [NASAL:#017] / NUM:0` |
| CHIC #128 | Mallia | nodulus | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[?:GLIDE:#008] me [NASAL:#017] / NUM:0` |
| CHIC #129 | Mallia | nodulus | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `wa #040 de / NUM:0` |
| CHIC #129 | Mallia | nodulus | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `wa #040 de / NUM:0` |
| CHIC #129 | Mallia | nodulus | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `wa [STOP:#040] de / NUM:0` |
| CHIC #129 | Mallia | nodulus | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `wa [STOP:#040] de / NUM:0` |
| CHIC #130 | Mallia | nodulus | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `#052 mu [?:i] / NUM:0` |
| CHIC #130 | Mallia | nodulus | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `#052 mu [?:i] / NUM:0` |
| CHIC #130 | Mallia | nodulus | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `#052 mu [?:i] / NUM:0` |
| CHIC #130 | Mallia | nodulus | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[LIQUID:#052] mu [?:i] / NUM:0` |
| CHIC #131 | Mallia | nodulus | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #131 | Mallia | nodulus | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #131 | Mallia | nodulus | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #131 | Mallia | nodulus | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[GLIDE:#036] ke` |
| CHIC #133 | Pyrgos (Myrtos) | vase | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `ra ti ni / NUM:0` |
| CHIC #133 | Pyrgos (Myrtos) | vase | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `ra ti ni / NUM:0` |
| CHIC #133 | Pyrgos (Myrtos) | vase | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `ra ti ni / NUM:0` |
| CHIC #133 | Pyrgos (Myrtos) | vase | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `ra ti ni / NUM:0` |
| CHIC #134 | Knossos | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #134 | Knossos | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #134 | Knossos | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #134 | Knossos | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #135 | Samothrace | roundel | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #135 | Samothrace | roundel | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #135 | Samothrace | roundel | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #135 | Samothrace | roundel | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #136 | Samothrace | roundel | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #136 | Samothrace | roundel | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #136 | Samothrace | roundel | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #136 | Samothrace | roundel | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #137 | Samothrace | nodulus | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #137 | Samothrace | nodulus | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #137 | Samothrace | nodulus | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #137 | Samothrace | nodulus | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #138 | Zakros | sealing | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #138 | Zakros | sealing | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #138 | Zakros | sealing | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #138 | Zakros | sealing | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #140 | Knossos | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ki pa #005` |
| CHIC #140 | Knossos | crescent | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `ki pa #005` |
| CHIC #140 | Knossos | crescent | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `ki pa [STOP:#005]` |
| CHIC #140 | Knossos | crescent | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `ki pa [STOP:#005]` |
| CHIC #141 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#063 ro` |
| CHIC #141 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#063 ro` |
| CHIC #141 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[GLIDE:#063] ro` |
| CHIC #141 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[GLIDE:#063] ro` |
| CHIC #142 | Knossos | crescent | tier-1 | 3 | 0 | 0 | 3 | 0.0000 | `#018 #039 #005 / NUM:0` |
| CHIC #142 | Knossos | crescent | tier-2 | 3 | 0 | 0 | 3 | 0.0000 | `#018 #039 #005 / NUM:0` |
| CHIC #142 | Knossos | crescent | tier-3 | 3 | 0 | 2 | 1 | 0.6667 | `#018 [STOP:#039] [STOP:#005] / NUM:0` |
| CHIC #142 | Knossos | crescent | tier-4 | 3 | 0 | 3 | 0 | 1.0000 | `[GLIDE:#018] [STOP:#039] [STOP:#005] / NUM:0` |
| CHIC #143 | Knossos | crescent | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `wa` |
| CHIC #143 | Knossos | crescent | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `wa` |
| CHIC #143 | Knossos | crescent | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `wa` |
| CHIC #143 | Knossos | crescent | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `wa` |
| CHIC #144 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #144 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #144 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[?:ki] [STOP:#005]` |
| CHIC #144 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?:ki] [STOP:#005]` |
| CHIC #145 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #145 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #145 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #145 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #148 | Mallia | nodulus | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `#011 i a` |
| CHIC #148 | Mallia | nodulus | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `#011 i a` |
| CHIC #148 | Mallia | nodulus | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `[LIQUID:#011] i a` |
| CHIC #148 | Mallia | nodulus | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[LIQUID:#011] i a` |
| CHIC #149 | Mallia | sealing | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ro #021 te` |
| CHIC #149 | Mallia | sealing | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `ro #021 te` |
| CHIC #149 | Mallia | sealing | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `ro [NASAL:#021] te` |
| CHIC #149 | Mallia | sealing | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `ro [NASAL:#021] te` |
| CHIC #150 | Mallia | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #150 | Mallia | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #150 | Mallia | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #150 | Mallia | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #151 | Phaistos | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa me` |
| CHIC #151 | Phaistos | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa me` |
| CHIC #151 | Phaistos | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa me` |
| CHIC #151 | Phaistos | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa me` |
| CHIC #152 | Zakros | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `mu ki` |
| CHIC #152 | Zakros | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `mu ki` |
| CHIC #152 | Zakros | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `mu ki` |
| CHIC #152 | Zakros | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `mu ki` |
| CHIC #153 | Zakros | sealing | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `mu [?]` |
| CHIC #153 | Zakros | sealing | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `mu [?]` |
| CHIC #153 | Zakros | sealing | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `mu [?]` |
| CHIC #153 | Zakros | sealing | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `mu [?]` |
| CHIC #154 | Mallia | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa i` |
| CHIC #154 | Mallia | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa i` |
| CHIC #154 | Mallia | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa i` |
| CHIC #154 | Mallia | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa i` |
| CHIC #155 | Haghia Triada | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `mu ja` |
| CHIC #155 | Haghia Triada | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `mu ja` |
| CHIC #155 | Haghia Triada | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `mu ja` |
| CHIC #155 | Haghia Triada | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `mu ja` |
| CHIC #157 | Knossos | crescent | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #157 | Knossos | crescent | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #157 | Knossos | crescent | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #157 | Knossos | crescent | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #158 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #158 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #158 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #158 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #159 | Knossos | crescent | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #159 | Knossos | crescent | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #159 | Knossos | crescent | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #159 | Knossos | crescent | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #160 | Knossos | crescent | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?:ti] #020 ni` |
| CHIC #160 | Knossos | crescent | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?:ti] #020 ni` |
| CHIC #160 | Knossos | crescent | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `[?:ti] [VOWEL:#020] ni` |
| CHIC #160 | Knossos | crescent | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[?:ti] [VOWEL:#020] ni` |
| CHIC #161 | Knossos | crescent | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #161 | Knossos | crescent | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #161 | Knossos | crescent | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #161 | Knossos | crescent | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #162 | Knossos | crescent | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #162 | Knossos | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #162 | Knossos | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #162 | Knossos | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #163 | Knossos | crescent | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `wa ra i` |
| CHIC #163 | Knossos | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `wa ra i` |
| CHIC #163 | Knossos | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `wa ra i` |
| CHIC #163 | Knossos | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `wa ra i` |
| CHIC #165 | Knossos | crescent | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #165 | Knossos | crescent | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?:ki] #005` |
| CHIC #165 | Knossos | crescent | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[?:ki] [STOP:#005]` |
| CHIC #165 | Knossos | crescent | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?:ki] [STOP:#005]` |
| CHIC #166 | Knossos | crescent | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#056 #047 ro` |
| CHIC #166 | Knossos | crescent | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#056 #047 ro` |
| CHIC #166 | Knossos | crescent | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `[STOP:#056] #047 ro` |
| CHIC #166 | Knossos | crescent | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[STOP:#056] [LIQUID:#047] ro` |
| CHIC #167 | Knossos | crescent | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `de ra ra` |
| CHIC #167 | Knossos | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `de ra ra` |
| CHIC #167 | Knossos | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `de ra ra` |
| CHIC #167 | Knossos | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `de ra ra` |
| CHIC #168 | Knossos | crescent | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ra [?]` |
| CHIC #168 | Knossos | crescent | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ra [?]` |
| CHIC #168 | Knossos | crescent | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ra [?]` |
| CHIC #168 | Knossos | crescent | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ra [?]` |
| CHIC #169 | Knossos | sealing | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #169 | Knossos | sealing | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #169 | Knossos | sealing | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #169 | Knossos | sealing | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #170 | Knossos | sealing | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #170 | Knossos | sealing | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #170 | Knossos | sealing | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #170 | Knossos | sealing | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #171 | Mallia | nodulus | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#062 #040` |
| CHIC #171 | Mallia | nodulus | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#062 #040` |
| CHIC #171 | Mallia | nodulus | tier-3 | 2 | 0 | 1 | 1 | 0.5000 | `#062 [STOP:#040]` |
| CHIC #171 | Mallia | nodulus | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[GLIDE:#062] [STOP:#040]` |
| CHIC #172 | Mallia | crescent | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `ja ke ti` |
| CHIC #172 | Mallia | crescent | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `ja ke ti` |
| CHIC #172 | Mallia | crescent | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `ja ke ti` |
| CHIC #172 | Mallia | crescent | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `ja ke ti` |
| CHIC #173 | Mallia | sealing | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 #056` |
| CHIC #173 | Mallia | sealing | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 #056` |
| CHIC #173 | Mallia | sealing | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `je #034 [STOP:#056]` |
| CHIC #173 | Mallia | sealing | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `je [LIQUID:#034] [STOP:#056]` |
| CHIC #174 | Palaikastro | sealing | tier-1 | 5 | 2 | 0 | 3 | 0.4000 | `ki #005 / ki #065 #005` |
| CHIC #174 | Palaikastro | sealing | tier-2 | 5 | 2 | 0 | 3 | 0.4000 | `ki #005 / ki #065 #005` |
| CHIC #174 | Palaikastro | sealing | tier-3 | 5 | 2 | 3 | 0 | 1.0000 | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` |
| CHIC #174 | Palaikastro | sealing | tier-4 | 5 | 2 | 3 | 0 | 1.0000 | `ki [STOP:#005] / ki [STOP:#065] [STOP:#005]` |
| CHIC #175 | Pyrgos (Myrtos) | potsherd | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] ke [?] [?]` |
| CHIC #175 | Pyrgos (Myrtos) | potsherd | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] ke [?] [?]` |
| CHIC #175 | Pyrgos (Myrtos) | potsherd | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] ke [?] [?]` |
| CHIC #175 | Pyrgos (Myrtos) | potsherd | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] ke [?] [?]` |
| CHIC #177 | Knossos | nodulus | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #177 | Knossos | nodulus | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #177 | Knossos | nodulus | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #177 | Knossos | nodulus | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `[?:IDEO:#156]` |
| CHIC #178 | Knossos | sealing | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?:wa] [?:de] [?:#050] [?] / NUM:0` |
| CHIC #178 | Knossos | sealing | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?:wa] [?:de] [?:#050] [?] / NUM:0` |
| CHIC #178 | Knossos | sealing | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `[?:wa] [?:de] [?:GLIDE:#050] [?] / NUM:0` |
| CHIC #178 | Knossos | sealing | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[?:wa] [?:de] [?:GLIDE:#050] [?] / NUM:0` |
| CHIC #179 | Knossos | sealing | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `wa ke / ke [?]` |
| CHIC #179 | Knossos | sealing | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `wa ke / ke [?]` |
| CHIC #179 | Knossos | sealing | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `wa ke / ke [?]` |
| CHIC #179 | Knossos | sealing | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `wa ke / ke [?]` |
| CHIC #180 | Crete (unprovenanced) | seal | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `ki de #050 #056 / NUM:0` |
| CHIC #180 | Crete (unprovenanced) | seal | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `ki de #050 #056 / NUM:0` |
| CHIC #180 | Crete (unprovenanced) | seal | tier-3 | 4 | 2 | 2 | 0 | 1.0000 | `ki de [GLIDE:#050] [STOP:#056] / NUM:0` |
| CHIC #180 | Crete (unprovenanced) | seal | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `ki de [GLIDE:#050] [STOP:#056] / NUM:0` |
| CHIC #181 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #181 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #181 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #181 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #182 | Crete (unprovenanced) | seal | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `#056 ta #029 #011 / NUM:0` |
| CHIC #182 | Crete (unprovenanced) | seal | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `#056 ta #029 #011 / NUM:0` |
| CHIC #182 | Crete (unprovenanced) | seal | tier-3 | 4 | 1 | 2 | 1 | 0.7500 | `[STOP:#056] ta #029 [LIQUID:#011] / NUM:0` |
| CHIC #182 | Crete (unprovenanced) | seal | tier-4 | 4 | 1 | 3 | 0 | 1.0000 | `[STOP:#056] ta [LIQUID:#029] [LIQUID:#011] / NUM:0` |
| CHIC #183 | Crete (unprovenanced) | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `i ra #011` |
| CHIC #183 | Crete (unprovenanced) | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `i ra #011` |
| CHIC #183 | Crete (unprovenanced) | seal | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `i ra [LIQUID:#011]` |
| CHIC #183 | Crete (unprovenanced) | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `i ra [LIQUID:#011]` |
| CHIC #184 | Crete (unprovenanced) | seal | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `ki pa ra` |
| CHIC #184 | Crete (unprovenanced) | seal | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `ki pa ra` |
| CHIC #184 | Crete (unprovenanced) | seal | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `ki pa ra` |
| CHIC #184 | Crete (unprovenanced) | seal | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `ki pa ra` |
| CHIC #186 | Kalo Horio | seal | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `ti te de #047 / NUM:0` |
| CHIC #186 | Kalo Horio | seal | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `ti te de #047 / NUM:0` |
| CHIC #186 | Kalo Horio | seal | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `ti te de #047 / NUM:0` |
| CHIC #186 | Kalo Horio | seal | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `ti te de [LIQUID:#047] / NUM:0` |
| CHIC #187 | Mallia | seal | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `me #008` |
| CHIC #187 | Mallia | seal | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `me #008` |
| CHIC #187 | Mallia | seal | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `me [GLIDE:#008]` |
| CHIC #187 | Mallia | seal | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `me [GLIDE:#008]` |
| CHIC #188 | Mallia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki [?:de]` |
| CHIC #188 | Mallia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki [?:de]` |
| CHIC #188 | Mallia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki [?:de]` |
| CHIC #188 | Mallia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki [?:de]` |
| CHIC #189 | Mallia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] mu [?]` |
| CHIC #189 | Mallia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] mu [?]` |
| CHIC #189 | Mallia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] mu [?]` |
| CHIC #189 | Mallia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] mu [?]` |
| CHIC #191 | Mochlos | seal | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#036 #040 / NUM:49 [?]` |
| CHIC #191 | Mochlos | seal | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#036 #040 / NUM:49 [?]` |
| CHIC #191 | Mochlos | seal | tier-3 | 2 | 0 | 1 | 1 | 0.5000 | `#036 [STOP:#040] / NUM:49 [?]` |
| CHIC #191 | Mochlos | seal | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[GLIDE:#036] [STOP:#040] / NUM:49 [?]` |
| CHIC #193 | Ziros | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `a ke #056 / NUM:0` |
| CHIC #193 | Ziros | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `a ke #056 / NUM:0` |
| CHIC #193 | Ziros | seal | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `a ke [STOP:#056] / NUM:0` |
| CHIC #193 | Ziros | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `a ke [STOP:#056] / NUM:0` |
| CHIC #194 | Crete (unprovenanced) | seal | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #194 | Crete (unprovenanced) | seal | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `ki #005` |
| CHIC #194 | Crete (unprovenanced) | seal | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #194 | Crete (unprovenanced) | seal | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `ki [STOP:#005]` |
| CHIC #195 | Crete (unprovenanced) | seal | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #195 | Crete (unprovenanced) | seal | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #195 | Crete (unprovenanced) | seal | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #195 | Crete (unprovenanced) | seal | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #196 | Gortys | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ke te` |
| CHIC #196 | Gortys | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ke te` |
| CHIC #196 | Gortys | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ke te` |
| CHIC #196 | Gortys | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ke te` |
| CHIC #197 | Mallia | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ro #021 te` |
| CHIC #197 | Mallia | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `ro #021 te` |
| CHIC #197 | Mallia | seal | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `ro [NASAL:#021] te` |
| CHIC #197 | Mallia | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `ro [NASAL:#021] te` |
| CHIC #198 | Mirabelo | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ra to` |
| CHIC #198 | Mirabelo | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ra to` |
| CHIC #198 | Mirabelo | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ra to` |
| CHIC #198 | Mirabelo | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ra to` |
| CHIC #199 | Mallia | seal | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:70 [?]` |
| CHIC #199 | Mallia | seal | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:70 [?]` |
| CHIC #199 | Mallia | seal | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:70 [?]` |
| CHIC #199 | Mallia | seal | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:70 [?]` |
| CHIC #200 | Mallia | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `#029 ni #056 i [?:ma]` |
| CHIC #200 | Mallia | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `#029 ni #056 i [?:ma]` |
| CHIC #200 | Mallia | seal | tier-3 | 5 | 3 | 1 | 1 | 0.8000 | `#029 ni [STOP:#056] i [?:ma]` |
| CHIC #200 | Mallia | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `[LIQUID:#029] ni [STOP:#056] i [?:ma]` |
| CHIC #201 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #201 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #201 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #201 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `wa ke` |
| CHIC #202 | Arkhanes | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke [?:#095] #052` |
| CHIC #202 | Arkhanes | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke [?:#095] #052` |
| CHIC #202 | Arkhanes | seal | tier-3 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke [?:#095] #052` |
| CHIC #202 | Arkhanes | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `wa ke / ke [?:GLIDE:#095] [LIQUID:#052]` |
| CHIC #203 | Knossos | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #203 | Knossos | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #203 | Knossos | seal | tier-3 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #203 | Knossos | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `wa ke / ke [GLIDE:#095] [LIQUID:#052]` |
| CHIC #204 | Mallia | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `i #034 [?:#066]` |
| CHIC #204 | Mallia | seal | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `i #034 [?:#066]` |
| CHIC #204 | Mallia | seal | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `i #034 [?:STOP:#066]` |
| CHIC #204 | Mallia | seal | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `i [LIQUID:#034] [?:STOP:#066]` |
| CHIC #205 | Crete (unprovenanced) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #205 | Crete (unprovenanced) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #205 | Crete (unprovenanced) | seal | tier-3 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #205 | Crete (unprovenanced) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `wa ke / ke [GLIDE:#095] [LIQUID:#052]` |
| CHIC #207 | Mallia | seal | tier-1 | 4 | 4 | 0 | 0 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| CHIC #207 | Mallia | seal | tier-2 | 4 | 4 | 0 | 0 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| CHIC #207 | Mallia | seal | tier-3 | 4 | 4 | 0 | 0 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| CHIC #207 | Mallia | seal | tier-4 | 4 | 4 | 0 | 0 | 1.0000 | `[?:ke] [?:to] [?] / ki de` |
| CHIC #208 | Avdou | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #208 | Avdou | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #208 | Avdou | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #208 | Avdou | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #209 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #209 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #209 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #209 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:ki] de` |
| CHIC #210 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #210 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #210 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #210 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #211 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #211 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #211 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #211 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #212 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #212 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #212 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #212 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #213 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #213 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #213 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #213 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #214 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #214 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #214 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #214 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `i ja` |
| CHIC #215 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #215 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #215 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #215 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #216 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #216 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #216 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #216 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #217 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #217 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #217 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #217 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #218 | Crete (unprovenanced) | seal | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #218 | Crete (unprovenanced) | seal | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #218 | Crete (unprovenanced) | seal | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #218 | Crete (unprovenanced) | seal | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #219 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #219 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #219 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #219 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #220 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #220 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #220 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #220 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #221 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #221 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #221 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #221 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #223 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #223 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #223 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #223 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #224 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] i` |
| CHIC #224 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] i` |
| CHIC #224 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] i` |
| CHIC #224 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `[?:wa] i` |
| CHIC #225 | Crete (unprovenanced) | seal | tier-1 | 3 | 0 | 0 | 3 | 0.0000 | `#068 #009 #011` |
| CHIC #225 | Crete (unprovenanced) | seal | tier-2 | 3 | 0 | 0 | 3 | 0.0000 | `#068 #009 #011` |
| CHIC #225 | Crete (unprovenanced) | seal | tier-3 | 3 | 0 | 2 | 1 | 0.6667 | `#068 [STOP:#009] [LIQUID:#011]` |
| CHIC #225 | Crete (unprovenanced) | seal | tier-4 | 3 | 0 | 3 | 0 | 1.0000 | `[LIQUID:#068] [STOP:#009] [LIQUID:#011]` |
| CHIC #226 | Lasithi | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #226 | Lasithi | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #226 | Lasithi | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #226 | Lasithi | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #227 | Lithines | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #227 | Lithines | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #227 | Lithines | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #227 | Lithines | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #229 | Mallia | seal | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #229 | Mallia | seal | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #229 | Mallia | seal | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `#036 ke` |
| CHIC #229 | Mallia | seal | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[GLIDE:#036] ke` |
| CHIC #231 | Mallia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #231 | Mallia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #231 | Mallia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #231 | Mallia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #232 | Mallia | seal | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `[?:de]` |
| CHIC #232 | Mallia | seal | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `[?:de]` |
| CHIC #232 | Mallia | seal | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `[?:de]` |
| CHIC #232 | Mallia | seal | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `[?:de]` |
| CHIC #233 | Mallia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #233 | Mallia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #233 | Mallia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #233 | Mallia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #234 | Mallia | seal | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#017 #050` |
| CHIC #234 | Mallia | seal | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#017 #050` |
| CHIC #234 | Mallia | seal | tier-3 | 2 | 0 | 2 | 0 | 1.0000 | `[NASAL:#017] [GLIDE:#050]` |
| CHIC #234 | Mallia | seal | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[NASAL:#017] [GLIDE:#050]` |
| CHIC #235 | Mallia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #235 | Mallia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #235 | Mallia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #235 | Mallia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #236 | Mallia | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#012 ra #048` |
| CHIC #236 | Mallia | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `wa ra #048` |
| CHIC #236 | Mallia | seal | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `wa ra #048` |
| CHIC #236 | Mallia | seal | tier-4 | 3 | 2 | 0 | 1 | 0.6667 | `wa ra #048` |
| CHIC #237 | Mirabelo | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #237 | Mirabelo | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #237 | Mirabelo | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #237 | Mirabelo | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #238 | Mochlos | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 #056` |
| CHIC #238 | Mochlos | seal | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 #056` |
| CHIC #238 | Mochlos | seal | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `je #034 [STOP:#056]` |
| CHIC #238 | Mochlos | seal | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `je [LIQUID:#034] [STOP:#056]` |
| CHIC #239 | Praisos | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `i [?:ja] [?:#034]` |
| CHIC #239 | Praisos | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `i [?:ja] [?:#034]` |
| CHIC #239 | Praisos | seal | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `i [?:ja] [?:#034]` |
| CHIC #239 | Praisos | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `i [?:ja] [?:LIQUID:#034]` |
| CHIC #240 | Sitia | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `NUM:1 / ki de` |
| CHIC #240 | Sitia | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `NUM:1 / ki de` |
| CHIC #240 | Sitia | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `NUM:1 / ki de` |
| CHIC #240 | Sitia | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `NUM:1 / ki de` |
| CHIC #241 | Sitia | seal | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#094] [?:#036]` |
| CHIC #241 | Sitia | seal | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#094] [?:#036]` |
| CHIC #241 | Sitia | seal | tier-3 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#094] [?:#036]` |
| CHIC #241 | Sitia | seal | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[?:LIQUID:#094] [?:GLIDE:#036]` |
| CHIC #242 | Crete (unprovenanced) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `#056 #059 / i ja ro` |
| CHIC #242 | Crete (unprovenanced) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `#056 #059 / i ja ro` |
| CHIC #242 | Crete (unprovenanced) | seal | tier-3 | 5 | 3 | 2 | 0 | 1.0000 | `[STOP:#056] [GLIDE:#059] / i ja ro` |
| CHIC #242 | Crete (unprovenanced) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `[STOP:#056] [GLIDE:#059] / i ja ro` |
| CHIC #243 | Crete (unprovenanced) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `#006 je ke / NUM:0 / je #023` |
| CHIC #243 | Crete (unprovenanced) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `#006 je ke / NUM:0 / je #023` |
| CHIC #243 | Crete (unprovenanced) | seal | tier-3 | 5 | 3 | 1 | 1 | 0.8000 | `[GLIDE:#006] je ke / NUM:0 / je #023` |
| CHIC #243 | Crete (unprovenanced) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `[GLIDE:#006] je ke / NUM:0 / je [LIQUID:#023]` |
| CHIC #244 | Crete (unprovenanced) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `ki de / je #034 #056` |
| CHIC #244 | Crete (unprovenanced) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `ki de / je #034 #056` |
| CHIC #244 | Crete (unprovenanced) | seal | tier-3 | 5 | 3 | 1 | 1 | 0.8000 | `ki de / je #034 [STOP:#056]` |
| CHIC #244 | Crete (unprovenanced) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `ki de / je [LIQUID:#034] [STOP:#056]` |
| CHIC #245 | Crete (unprovenanced) | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `de [?] / #029 #014 [?]` |
| CHIC #245 | Crete (unprovenanced) | seal | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `de [?] / #029 #014 [?]` |
| CHIC #245 | Crete (unprovenanced) | seal | tier-3 | 3 | 1 | 0 | 2 | 0.3333 | `de [?] / #029 #014 [?]` |
| CHIC #245 | Crete (unprovenanced) | seal | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `de [?] / [LIQUID:#029] [GLIDE:#014] [?]` |
| CHIC #246 | Kritsa | seal | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `ki #005 / #006 ni` |
| CHIC #246 | Kritsa | seal | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `ki #005 / #006 ni` |
| CHIC #246 | Kritsa | seal | tier-3 | 4 | 2 | 2 | 0 | 1.0000 | `ki [STOP:#005] / [GLIDE:#006] ni` |
| CHIC #246 | Kritsa | seal | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `ki [STOP:#005] / [GLIDE:#006] ni` |
| CHIC #247 | Mallia | seal | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `ki de / ki #005` |
| CHIC #247 | Mallia | seal | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `ki de / ki #005` |
| CHIC #247 | Mallia | seal | tier-3 | 4 | 3 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005]` |
| CHIC #247 | Mallia | seal | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005]` |
| CHIC #248 | Palaikastro | seal | tier-1 | 6 | 4 | 0 | 2 | 0.6667 | `i ja ro / je #034 #056` |
| CHIC #248 | Palaikastro | seal | tier-2 | 6 | 4 | 0 | 2 | 0.6667 | `i ja ro / je #034 #056` |
| CHIC #248 | Palaikastro | seal | tier-3 | 6 | 4 | 1 | 1 | 0.8333 | `i ja ro / je #034 [STOP:#056]` |
| CHIC #248 | Palaikastro | seal | tier-4 | 6 | 4 | 2 | 0 | 1.0000 | `i ja ro / je [LIQUID:#034] [STOP:#056]` |
| CHIC #249 | Sitia | seal | tier-1 | 4 | 4 | 0 | 0 | 1.0000 | `i ja / ki de` |
| CHIC #249 | Sitia | seal | tier-2 | 4 | 4 | 0 | 0 | 1.0000 | `i ja / ki de` |
| CHIC #249 | Sitia | seal | tier-3 | 4 | 4 | 0 | 0 | 1.0000 | `i ja / ki de` |
| CHIC #249 | Sitia | seal | tier-4 | 4 | 4 | 0 | 0 | 1.0000 | `i ja / ki de` |
| CHIC #250 | Zakros | seal | tier-1 | 5 | 4 | 0 | 1 | 0.8000 | `ki #005 / i ja ro` |
| CHIC #250 | Zakros | seal | tier-2 | 5 | 4 | 0 | 1 | 0.8000 | `ki #005 / i ja ro` |
| CHIC #250 | Zakros | seal | tier-3 | 5 | 4 | 1 | 0 | 1.0000 | `ki [STOP:#005] / i ja ro` |
| CHIC #250 | Zakros | seal | tier-4 | 5 | 4 | 1 | 0 | 1.0000 | `ki [STOP:#005] / i ja ro` |
| CHIC #251 | Arkhanes | seal | tier-1 | 7 | 4 | 0 | 3 | 0.5714 | `ke [?:#095] [?:#052] / wa ke / [?:#094] [?:i]` |
| CHIC #251 | Arkhanes | seal | tier-2 | 7 | 4 | 0 | 3 | 0.5714 | `ke [?:#095] [?:#052] / wa ke / [?:#094] [?:i]` |
| CHIC #251 | Arkhanes | seal | tier-3 | 7 | 4 | 0 | 3 | 0.5714 | `ke [?:#095] [?:#052] / wa ke / [?:#094] [?:i]` |
| CHIC #251 | Arkhanes | seal | tier-4 | 7 | 4 | 3 | 0 | 1.0000 | `ke [?:GLIDE:#095] [?:LIQUID:#052] / wa ke / [?:LIQUID:#094] [?:i]` |
| CHIC #252 | Arkhanes | seal | tier-1 | 6 | 3 | 0 | 3 | 0.5000 | `ke #095 #052 / wa ke / [?:#062]` |
| CHIC #252 | Arkhanes | seal | tier-2 | 6 | 3 | 0 | 3 | 0.5000 | `ke #095 #052 / wa ke / [?:#062]` |
| CHIC #252 | Arkhanes | seal | tier-3 | 6 | 3 | 0 | 3 | 0.5000 | `ke #095 #052 / wa ke / [?:#062]` |
| CHIC #252 | Arkhanes | seal | tier-4 | 6 | 3 | 3 | 0 | 1.0000 | `ke [GLIDE:#095] [LIQUID:#052] / wa ke / [?:GLIDE:#062]` |
| CHIC #253 | Crete (unprovenanced) | seal | tier-1 | 6 | 5 | 0 | 1 | 0.8333 | `i ja / ki de / ki #005` |
| CHIC #253 | Crete (unprovenanced) | seal | tier-2 | 6 | 5 | 0 | 1 | 0.8333 | `i ja / ki de / ki #005` |
| CHIC #253 | Crete (unprovenanced) | seal | tier-3 | 6 | 5 | 1 | 0 | 1.0000 | `i ja / ki de / ki [STOP:#005]` |
| CHIC #253 | Crete (unprovenanced) | seal | tier-4 | 6 | 5 | 1 | 0 | 1.0000 | `i ja / ki de / ki [STOP:#005]` |
| CHIC #254 | Crete (unprovenanced) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `ki #005 / #036 ke ro / [?]` |
| CHIC #254 | Crete (unprovenanced) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `ki #005 / #036 ke ro / [?]` |
| CHIC #254 | Crete (unprovenanced) | seal | tier-3 | 5 | 3 | 1 | 1 | 0.8000 | `ki [STOP:#005] / #036 ke ro / [?]` |
| CHIC #254 | Crete (unprovenanced) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `ki [STOP:#005] / [GLIDE:#036] ke ro / [?]` |
| CHIC #255 | Crete (unprovenanced) | seal | tier-1 | 11 | 6 | 0 | 5 | 0.5455 | `ki #036 #018 / ti de wa ro #056 #036 / #046 ki` |
| CHIC #255 | Crete (unprovenanced) | seal | tier-2 | 11 | 6 | 0 | 5 | 0.5455 | `ki #036 #018 / ti de wa ro #056 #036 / #046 ki` |
| CHIC #255 | Crete (unprovenanced) | seal | tier-3 | 11 | 6 | 1 | 4 | 0.6364 | `ki #036 #018 / ti de wa ro [STOP:#056] #036 / #046 ki` |
| CHIC #255 | Crete (unprovenanced) | seal | tier-4 | 11 | 6 | 5 | 0 | 1.0000 | `ki [GLIDE:#036] [GLIDE:#018] / ti de wa ro [STOP:#056] [GLIDE:#036] / [GLIDE:#046] ki` |
| CHIC #256 | Crete (unprovenanced) | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `i #043 de / NUM:0` |
| CHIC #256 | Crete (unprovenanced) | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `i #043 de / NUM:0` |
| CHIC #256 | Crete (unprovenanced) | seal | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `i [LIQUID:#043] de / NUM:0` |
| CHIC #256 | Crete (unprovenanced) | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `i [LIQUID:#043] de / NUM:0` |
| CHIC #257 | Crete (unprovenanced) | seal | tier-1 | 8 | 6 | 0 | 2 | 0.7500 | `i ja ro / #036 ke ro / #046 ki` |
| CHIC #257 | Crete (unprovenanced) | seal | tier-2 | 8 | 6 | 0 | 2 | 0.7500 | `i ja ro / #036 ke ro / #046 ki` |
| CHIC #257 | Crete (unprovenanced) | seal | tier-3 | 8 | 6 | 0 | 2 | 0.7500 | `i ja ro / #036 ke ro / #046 ki` |
| CHIC #257 | Crete (unprovenanced) | seal | tier-4 | 8 | 6 | 2 | 0 | 1.0000 | `i ja ro / [GLIDE:#036] ke ro / [GLIDE:#046] ki` |
| CHIC #258 | Crete (unprovenanced) | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `i ja / #036 ke ro / ki de` |
| CHIC #258 | Crete (unprovenanced) | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `i ja / #036 ke ro / ki de` |
| CHIC #258 | Crete (unprovenanced) | seal | tier-3 | 7 | 6 | 0 | 1 | 0.8571 | `i ja / #036 ke ro / ki de` |
| CHIC #258 | Crete (unprovenanced) | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `i ja / [GLIDE:#036] ke ro / ki de` |
| CHIC #259 | Crete (unprovenanced) | seal | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `ki de / ki #005` |
| CHIC #259 | Crete (unprovenanced) | seal | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `ki de / ki #005` |
| CHIC #259 | Crete (unprovenanced) | seal | tier-3 | 4 | 3 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005]` |
| CHIC #259 | Crete (unprovenanced) | seal | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005]` |
| CHIC #260 | Crete (unprovenanced) | seal | tier-1 | 7 | 5 | 0 | 2 | 0.7143 | `ki de / i ja / je #034 #056` |
| CHIC #260 | Crete (unprovenanced) | seal | tier-2 | 7 | 5 | 0 | 2 | 0.7143 | `ki de / i ja / je #034 #056` |
| CHIC #260 | Crete (unprovenanced) | seal | tier-3 | 7 | 5 | 1 | 1 | 0.8571 | `ki de / i ja / je #034 [STOP:#056]` |
| CHIC #260 | Crete (unprovenanced) | seal | tier-4 | 7 | 5 | 2 | 0 | 1.0000 | `ki de / i ja / je [LIQUID:#034] [STOP:#056]` |
| CHIC #261 | Crete (unprovenanced) | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / i ja ro / ki de` |
| CHIC #261 | Crete (unprovenanced) | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / i ja ro / ki de` |
| CHIC #261 | Crete (unprovenanced) | seal | tier-3 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / i ja ro / ki de` |
| CHIC #261 | Crete (unprovenanced) | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / i ja ro / ki de` |
| CHIC #262 | Crete (unprovenanced) | seal | tier-1 | 9 | 7 | 0 | 2 | 0.7778 | `#036 ke ke ro / i ja ro / ki #005` |
| CHIC #262 | Crete (unprovenanced) | seal | tier-2 | 9 | 7 | 0 | 2 | 0.7778 | `#036 ke ke ro / i ja ro / ki #005` |
| CHIC #262 | Crete (unprovenanced) | seal | tier-3 | 9 | 7 | 1 | 1 | 0.8889 | `#036 ke ke ro / i ja ro / ki [STOP:#005]` |
| CHIC #262 | Crete (unprovenanced) | seal | tier-4 | 9 | 7 | 2 | 0 | 1.0000 | `[GLIDE:#036] ke ke ro / i ja ro / ki [STOP:#005]` |
| CHIC #263 | Crete (unprovenanced) | seal | tier-1 | 7 | 5 | 0 | 2 | 0.7143 | `#036 [?:ke] / i ja ro / ki #005` |
| CHIC #263 | Crete (unprovenanced) | seal | tier-2 | 7 | 5 | 0 | 2 | 0.7143 | `#036 [?:ke] / i ja ro / ki #005` |
| CHIC #263 | Crete (unprovenanced) | seal | tier-3 | 7 | 5 | 1 | 1 | 0.8571 | `#036 [?:ke] / i ja ro / ki [STOP:#005]` |
| CHIC #263 | Crete (unprovenanced) | seal | tier-4 | 7 | 5 | 2 | 0 | 1.0000 | `[GLIDE:#036] [?:ke] / i ja ro / ki [STOP:#005]` |
| CHIC #264 | Heraklion | seal | tier-1 | 7 | 4 | 0 | 3 | 0.5714 | `pa #050 / #004 / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki #005` |
| CHIC #264 | Heraklion | seal | tier-2 | 7 | 4 | 0 | 3 | 0.5714 | `pa #050 / #004 / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki #005` |
| CHIC #264 | Heraklion | seal | tier-3 | 7 | 4 | 2 | 1 | 0.8571 | `pa [GLIDE:#050] / #004 / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki [STOP:#005]` |
| CHIC #264 | Heraklion | seal | tier-4 | 7 | 4 | 3 | 0 | 1.0000 | `pa [GLIDE:#050] / [LIQUID:#004] / IDEO:#152 / ki de / NUM:49 / IDEO:#152 / ki [STOP:#005]` |
| CHIC #265 | Kasteli | seal | tier-1 | 6 | 3 | 0 | 3 | 0.5000 | `i ja / #043 #009 / [?] / #036 ke` |
| CHIC #265 | Kasteli | seal | tier-2 | 6 | 3 | 0 | 3 | 0.5000 | `i ja / #043 #009 / [?] / #036 ke` |
| CHIC #265 | Kasteli | seal | tier-3 | 6 | 3 | 2 | 1 | 0.8333 | `i ja / [LIQUID:#043] [STOP:#009] / [?] / #036 ke` |
| CHIC #265 | Kasteli | seal | tier-4 | 6 | 3 | 3 | 0 | 1.0000 | `i ja / [LIQUID:#043] [STOP:#009] / [?] / [GLIDE:#036] ke` |
| CHIC #266 | Kordakia | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / ki ta de / ki de` |
| CHIC #266 | Kordakia | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / ki ta de / ki de` |
| CHIC #266 | Kordakia | seal | tier-3 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / ki ta de / ki de` |
| CHIC #266 | Kordakia | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / ki ta de / ki de` |
| CHIC #267 | Kydonia | seal | tier-1 | 7 | 4 | 0 | 3 | 0.5714 | `mu ja mu / #036 ke / #050 #011` |
| CHIC #267 | Kydonia | seal | tier-2 | 7 | 4 | 0 | 3 | 0.5714 | `mu ja mu / #036 ke / #050 #011` |
| CHIC #267 | Kydonia | seal | tier-3 | 7 | 4 | 2 | 1 | 0.8571 | `mu ja mu / #036 ke / [GLIDE:#050] [LIQUID:#011]` |
| CHIC #267 | Kydonia | seal | tier-4 | 7 | 4 | 3 | 0 | 1.0000 | `mu ja mu / [GLIDE:#036] ke / [GLIDE:#050] [LIQUID:#011]` |
| CHIC #268 | Lakonia | seal | tier-1 | 6 | 4 | 0 | 2 | 0.6667 | `NUM:70 / ki #005 / i ja / NUM:70 / #006 ra` |
| CHIC #268 | Lakonia | seal | tier-2 | 6 | 4 | 0 | 2 | 0.6667 | `NUM:70 / ki #005 / i ja / NUM:70 / #006 ra` |
| CHIC #268 | Lakonia | seal | tier-3 | 6 | 4 | 2 | 0 | 1.0000 | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` |
| CHIC #268 | Lakonia | seal | tier-4 | 6 | 4 | 2 | 0 | 1.0000 | `NUM:70 / ki [STOP:#005] / i ja / NUM:70 / [GLIDE:#006] ra` |
| CHIC #269 | Lasithi | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `i ja ro [?] / de [?:de] [?] / [?:#046] ki` |
| CHIC #269 | Lasithi | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `i ja ro [?] / de [?:de] [?] / [?:#046] ki` |
| CHIC #269 | Lasithi | seal | tier-3 | 7 | 6 | 0 | 1 | 0.8571 | `i ja ro [?] / de [?:de] [?] / [?:#046] ki` |
| CHIC #269 | Lasithi | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `i ja ro [?] / de [?:de] [?] / [?:GLIDE:#046] ki` |
| CHIC #270 | Lasithi | seal | tier-1 | 8 | 8 | 0 | 0 | 1.0000 | `ra i / ki de / i ro ja te` |
| CHIC #270 | Lasithi | seal | tier-2 | 8 | 8 | 0 | 0 | 1.0000 | `ra i / ki de / i ro ja te` |
| CHIC #270 | Lasithi | seal | tier-3 | 8 | 8 | 0 | 0 | 1.0000 | `ra i / ki de / i ro ja te` |
| CHIC #270 | Lasithi | seal | tier-4 | 8 | 8 | 0 | 0 | 1.0000 | `ra i / ki de / i ro ja te` |
| CHIC #271 | Mallia | seal | tier-1 | 10 | 4 | 0 | 6 | 0.4000 | `#012 a [?:#062] #018 / ni [?:ro] #011 / #060 ki #056` |
| CHIC #271 | Mallia | seal | tier-2 | 10 | 5 | 0 | 5 | 0.5000 | `wa a [?:#062] #018 / ni [?:ro] #011 / #060 ki #056` |
| CHIC #271 | Mallia | seal | tier-3 | 10 | 5 | 3 | 2 | 0.8000 | `wa a [?:#062] #018 / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [STOP:#056]` |
| CHIC #271 | Mallia | seal | tier-4 | 10 | 5 | 5 | 0 | 1.0000 | `wa a [?:GLIDE:#062] [GLIDE:#018] / ni [?:ro] [LIQUID:#011] / [STOP:#060] ki [STOP:#056]` |
| CHIC #272 | Mirabelo | seal | tier-1 | 10 | 6 | 0 | 4 | 0.6000 | `i ja ro / #036 ke ro / [?] / [?:#068] ja #011 #020` |
| CHIC #272 | Mirabelo | seal | tier-2 | 10 | 6 | 0 | 4 | 0.6000 | `i ja ro / #036 ke ro / [?] / [?:#068] ja #011 #020` |
| CHIC #272 | Mirabelo | seal | tier-3 | 10 | 6 | 2 | 2 | 0.8000 | `i ja ro / #036 ke ro / [?] / [?:#068] ja [LIQUID:#011] [VOWEL:#020]` |
| CHIC #272 | Mirabelo | seal | tier-4 | 10 | 6 | 4 | 0 | 1.0000 | `i ja ro / [GLIDE:#036] ke ro / [?] / [?:LIQUID:#068] ja [LIQUID:#011] [VOWEL:#020]` |
| CHIC #273 | Mirabelo | seal | tier-1 | 9 | 5 | 0 | 4 | 0.5556 | `mu #005 #050 / ke ro te / ra #005 #050` |
| CHIC #273 | Mirabelo | seal | tier-2 | 9 | 5 | 0 | 4 | 0.5556 | `mu #005 #050 / ke ro te / ra #005 #050` |
| CHIC #273 | Mirabelo | seal | tier-3 | 9 | 5 | 4 | 0 | 1.0000 | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` |
| CHIC #273 | Mirabelo | seal | tier-4 | 9 | 5 | 4 | 0 | 1.0000 | `mu [STOP:#005] [GLIDE:#050] / ke ro te / ra [STOP:#005] [GLIDE:#050]` |
| CHIC #274 | Mirabelo | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `ki de / ki #005 / i ja ro` |
| CHIC #274 | Mirabelo | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `ki de / ki #005 / i ja ro` |
| CHIC #274 | Mirabelo | seal | tier-3 | 7 | 6 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005] / i ja ro` |
| CHIC #274 | Mirabelo | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `ki de / ki [STOP:#005] / i ja ro` |
| CHIC #276 | Pinakiano | seal | tier-1 | 8 | 5 | 0 | 3 | 0.6250 | `wa i / ro #006 #034 / #005 ki de` |
| CHIC #276 | Pinakiano | seal | tier-2 | 8 | 5 | 0 | 3 | 0.6250 | `wa i / ro #006 #034 / #005 ki de` |
| CHIC #276 | Pinakiano | seal | tier-3 | 8 | 5 | 2 | 1 | 0.8750 | `wa i / ro [GLIDE:#006] #034 / [STOP:#005] ki de` |
| CHIC #276 | Pinakiano | seal | tier-4 | 8 | 5 | 3 | 0 | 1.0000 | `wa i / ro [GLIDE:#006] [LIQUID:#034] / [STOP:#005] ki de` |
| CHIC #277 | Ziros | seal | tier-1 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / ke ke pa / ki de` |
| CHIC #277 | Ziros | seal | tier-2 | 7 | 6 | 0 | 1 | 0.8571 | `ki #005 / ke ke pa / ki de` |
| CHIC #277 | Ziros | seal | tier-3 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / ke ke pa / ki de` |
| CHIC #277 | Ziros | seal | tier-4 | 7 | 6 | 1 | 0 | 1.0000 | `ki [STOP:#005] / ke ke pa / ki de` |
| CHIC #278 | Crete (unprovenanced) | seal | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #278 | Crete (unprovenanced) | seal | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #278 | Crete (unprovenanced) | seal | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #278 | Crete (unprovenanced) | seal | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `ki de` |
| CHIC #279 | Crete (unprovenanced) | seal | tier-1 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #279 | Crete (unprovenanced) | seal | tier-2 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #279 | Crete (unprovenanced) | seal | tier-3 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #279 | Crete (unprovenanced) | seal | tier-4 | 3 | 3 | 0 | 0 | 1.0000 | `i ja ro` |
| CHIC #280 | Mallia | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `wa ti #005` |
| CHIC #280 | Mallia | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `wa ti #005` |
| CHIC #280 | Mallia | seal | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `wa ti [STOP:#005]` |
| CHIC #280 | Mallia | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `wa ti [STOP:#005]` |
| CHIC #281 | Mallia | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 [?:#056]` |
| CHIC #281 | Mallia | seal | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `je #034 [?:#056]` |
| CHIC #281 | Mallia | seal | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `je #034 [?:STOP:#056]` |
| CHIC #281 | Mallia | seal | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `je [LIQUID:#034] [?:STOP:#056]` |
| CHIC #282 | Pyrgos (Myrtos) | seal | tier-1 | 3 | 1 | 0 | 2 | 0.3333 | `#008 [?:ke] [?:#036]` |
| CHIC #282 | Pyrgos (Myrtos) | seal | tier-2 | 3 | 1 | 0 | 2 | 0.3333 | `#008 [?:ke] [?:#036]` |
| CHIC #282 | Pyrgos (Myrtos) | seal | tier-3 | 3 | 1 | 1 | 1 | 0.6667 | `[GLIDE:#008] [?:ke] [?:#036]` |
| CHIC #282 | Pyrgos (Myrtos) | seal | tier-4 | 3 | 1 | 2 | 0 | 1.0000 | `[GLIDE:#008] [?:ke] [?:GLIDE:#036]` |
| CHIC #283 | Crete (unprovenanced) | seal | tier-1 | 7 | 4 | 0 | 3 | 0.5714 | `ki #005 / ki de / #056 pa #058` |
| CHIC #283 | Crete (unprovenanced) | seal | tier-2 | 7 | 4 | 0 | 3 | 0.5714 | `ki #005 / ki de / #056 pa #058` |
| CHIC #283 | Crete (unprovenanced) | seal | tier-3 | 7 | 4 | 3 | 0 | 1.0000 | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` |
| CHIC #283 | Crete (unprovenanced) | seal | tier-4 | 7 | 4 | 3 | 0 | 1.0000 | `ki [STOP:#005] / ki de / [STOP:#056] pa [STOP:#058]` |
| CHIC #284 | Crete (unprovenanced) | seal | tier-1 | 5 | 5 | 0 | 0 | 1.0000 | `ki de / i ja ro` |
| CHIC #284 | Crete (unprovenanced) | seal | tier-2 | 5 | 5 | 0 | 0 | 1.0000 | `ki de / i ja ro` |
| CHIC #284 | Crete (unprovenanced) | seal | tier-3 | 5 | 5 | 0 | 0 | 1.0000 | `ki de / i ja ro` |
| CHIC #284 | Crete (unprovenanced) | seal | tier-4 | 5 | 5 | 0 | 0 | 1.0000 | `ki de / i ja ro` |
| CHIC #285 | Crete (unprovenanced) | seal | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `#029 / [?:ki] [?:de] [?]` |
| CHIC #285 | Crete (unprovenanced) | seal | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `#029 / [?:ki] [?:de] [?]` |
| CHIC #285 | Crete (unprovenanced) | seal | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `#029 / [?:ki] [?:de] [?]` |
| CHIC #285 | Crete (unprovenanced) | seal | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[LIQUID:#029] / [?:ki] [?:de] [?]` |
| CHIC #286 | Mallia | seal | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `i ja / #047 ra` |
| CHIC #286 | Mallia | seal | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `i ja / #047 ra` |
| CHIC #286 | Mallia | seal | tier-3 | 4 | 3 | 0 | 1 | 0.7500 | `i ja / #047 ra` |
| CHIC #286 | Mallia | seal | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `i ja / [LIQUID:#047] ra` |
| CHIC #287 | Crete (unprovenanced) | seal | tier-1 | 7 | 5 | 0 | 2 | 0.7143 | `ki de / ra te #069 / ki #005` |
| CHIC #287 | Crete (unprovenanced) | seal | tier-2 | 7 | 5 | 0 | 2 | 0.7143 | `ki de / ra te #069 / ki #005` |
| CHIC #287 | Crete (unprovenanced) | seal | tier-3 | 7 | 5 | 2 | 0 | 1.0000 | `ki de / ra te [STOP:#069] / ki [STOP:#005]` |
| CHIC #287 | Crete (unprovenanced) | seal | tier-4 | 7 | 5 | 2 | 0 | 1.0000 | `ki de / ra te [STOP:#069] / ki [STOP:#005]` |
| CHIC #288 | Mallia | seal | tier-1 | 6 | 4 | 0 | 2 | 0.6667 | `i ja / ki #005 / #036 ke` |
| CHIC #288 | Mallia | seal | tier-2 | 6 | 4 | 0 | 2 | 0.6667 | `i ja / ki #005 / #036 ke` |
| CHIC #288 | Mallia | seal | tier-3 | 6 | 4 | 1 | 1 | 0.8333 | `i ja / ki [STOP:#005] / #036 ke` |
| CHIC #288 | Mallia | seal | tier-4 | 6 | 4 | 2 | 0 | 1.0000 | `i ja / ki [STOP:#005] / [GLIDE:#036] ke` |
| CHIC #289 | Palaikastro | seal | tier-1 | 7 | 2 | 0 | 5 | 0.2857 | `[?] [?:#056] #011 / [?] ke #056 #034 [?] / [?] [?] / [?:#034] ja [?]` |
| CHIC #289 | Palaikastro | seal | tier-2 | 7 | 2 | 0 | 5 | 0.2857 | `[?] [?:#056] #011 / [?] ke #056 #034 [?] / [?] [?] / [?:#034] ja [?]` |
| CHIC #289 | Palaikastro | seal | tier-3 | 7 | 2 | 3 | 2 | 0.7143 | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] #034 [?] / [?] [?] / [?:#034] ja [?]` |
| CHIC #289 | Palaikastro | seal | tier-4 | 7 | 2 | 5 | 0 | 1.0000 | `[?] [?:STOP:#056] [LIQUID:#011] / [?] ke [STOP:#056] [LIQUID:#034] [?] / [?] [?] / [?:LIQUID:#034] ja [?]` |
| CHIC #290 | Sitia | seal | tier-1 | 8 | 5 | 0 | 3 | 0.6250 | `ki de / #051 ro #005 / ma a #033` |
| CHIC #290 | Sitia | seal | tier-2 | 8 | 5 | 0 | 3 | 0.6250 | `ki de / #051 ro #005 / ma a #033` |
| CHIC #290 | Sitia | seal | tier-3 | 8 | 5 | 2 | 1 | 0.8750 | `ki de / #051 ro [STOP:#005] / ma a [GLIDE:#033]` |
| CHIC #290 | Sitia | seal | tier-4 | 8 | 5 | 3 | 0 | 1.0000 | `ki de / [GLIDE:#051] ro [STOP:#005] / ma a [GLIDE:#033]` |
| CHIC #291 | Crete (unprovenanced) | seal | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#157` |
| CHIC #291 | Crete (unprovenanced) | seal | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#157` |
| CHIC #291 | Crete (unprovenanced) | seal | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#157` |
| CHIC #291 | Crete (unprovenanced) | seal | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#157` |
| CHIC #293 | Adromili | seal | tier-1 | 10 | 10 | 0 | 0 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| CHIC #293 | Adromili | seal | tier-2 | 10 | 10 | 0 | 0 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| CHIC #293 | Adromili | seal | tier-3 | 10 | 10 | 0 | 0 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| CHIC #293 | Adromili | seal | tier-4 | 10 | 10 | 0 | 0 | 1.0000 | `[?:ma] i / i ja ro / wa mu te / ki de` |
| CHIC #294 | Crete (unprovenanced) | seal | tier-1 | 27 | 18 | 0 | 9 | 0.6667 | `ta de [?] #040 [?] / #059 je [?:#014] ni ke #047 ra ke ke ki #050 ke ti #056 / #056 [?:te] [?:ma] / ta ta / ke je [?] #034 [?] a #056` |
| CHIC #294 | Crete (unprovenanced) | seal | tier-2 | 27 | 18 | 0 | 9 | 0.6667 | `ta de [?] #040 [?] / #059 je [?:#014] ni ke #047 ra ke ke ki #050 ke ti #056 / #056 [?:te] [?:ma] / ta ta / ke je [?] #034 [?] a #056` |
| CHIC #294 | Crete (unprovenanced) | seal | tier-3 | 27 | 18 | 6 | 3 | 0.8889 | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:#014] ni ke #047 ra ke ke ki [GLIDE:#050] ke ti [STOP:#056] / [STOP:#056] [?:te] [?:ma] / ta ta / ke je [?] #034 [?] a [STOP:#056]` |
| CHIC #294 | Crete (unprovenanced) | seal | tier-4 | 27 | 18 | 9 | 0 | 1.0000 | `ta de [?] [STOP:#040] [?] / [GLIDE:#059] je [?:GLIDE:#014] ni ke [LIQUID:#047] ra ke ke ki [GLIDE:#050] ke ti [STOP:#056] / [STOP:#056] [?:te] [?:ma] / ta ta / ke je [?] [LIQUID:#034] [?] a [STOP:#056]` |
| CHIC #295 | Crete (unprovenanced) | seal | tier-1 | 11 | 6 | 0 | 5 | 0.5455 | `ki de / #029 ma de / je #034 [?:#056] / ki #005 / #080` |
| CHIC #295 | Crete (unprovenanced) | seal | tier-2 | 11 | 6 | 0 | 5 | 0.5455 | `ki de / #029 ma de / je #034 [?:#056] / ki #005 / #080` |
| CHIC #295 | Crete (unprovenanced) | seal | tier-3 | 11 | 6 | 2 | 3 | 0.7273 | `ki de / #029 ma de / je #034 [?:STOP:#056] / ki [STOP:#005] / #080` |
| CHIC #295 | Crete (unprovenanced) | seal | tier-4 | 11 | 6 | 4 | 1 | 0.9091 | `ki de / [LIQUID:#029] ma de / je [LIQUID:#034] [?:STOP:#056] / ki [STOP:#005] / #080` |
| CHIC #296 | Crete (unprovenanced) | seal | tier-1 | 11 | 6 | 0 | 5 | 0.5455 | `ti #007 #018 / me i #039 / ki de / je #034 #056` |
| CHIC #296 | Crete (unprovenanced) | seal | tier-2 | 11 | 6 | 0 | 5 | 0.5455 | `ti #007 #018 / me i #039 / ki de / je #034 #056` |
| CHIC #296 | Crete (unprovenanced) | seal | tier-3 | 11 | 6 | 3 | 2 | 0.8182 | `ti [VOWEL:#007] #018 / me i [STOP:#039] / ki de / je #034 [STOP:#056]` |
| CHIC #296 | Crete (unprovenanced) | seal | tier-4 | 11 | 6 | 5 | 0 | 1.0000 | `ti [VOWEL:#007] [GLIDE:#018] / me i [STOP:#039] / ki de / je [LIQUID:#034] [STOP:#056]` |
| CHIC #297 | Crete (unprovenanced) | seal | tier-1 | 13 | 7 | 0 | 6 | 0.5385 | `#050 ke / i #008 / #036 ja / #011 #056 / ki de / ki #005 te` |
| CHIC #297 | Crete (unprovenanced) | seal | tier-2 | 13 | 7 | 0 | 6 | 0.5385 | `#050 ke / i #008 / #036 ja / #011 #056 / ki de / ki #005 te` |
| CHIC #297 | Crete (unprovenanced) | seal | tier-3 | 13 | 7 | 5 | 1 | 0.9231 | `[GLIDE:#050] ke / i [GLIDE:#008] / #036 ja / [LIQUID:#011] [STOP:#056] / ki de / ki [STOP:#005] te` |
| CHIC #297 | Crete (unprovenanced) | seal | tier-4 | 13 | 7 | 6 | 0 | 1.0000 | `[GLIDE:#050] ke / i [GLIDE:#008] / [GLIDE:#036] ja / [LIQUID:#011] [STOP:#056] / ki de / ki [STOP:#005] te` |
| CHIC #298 | Crete (unprovenanced) | seal | tier-1 | 15 | 11 | 0 | 4 | 0.7333 | `#056 ra #040 / ra te ke #045 ra / i ja ro / ki #005 / ki de` |
| CHIC #298 | Crete (unprovenanced) | seal | tier-2 | 15 | 11 | 0 | 4 | 0.7333 | `#056 ra #040 / ra te ke #045 ra / i ja ro / ki #005 / ki de` |
| CHIC #298 | Crete (unprovenanced) | seal | tier-3 | 15 | 11 | 4 | 0 | 1.0000 | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#005] / ki de` |
| CHIC #298 | Crete (unprovenanced) | seal | tier-4 | 15 | 11 | 4 | 0 | 1.0000 | `[STOP:#056] ra [STOP:#040] / ra te ke [STOP:#045] ra / i ja ro / ki [STOP:#005] / ki de` |
| CHIC #299 | Crete (unprovenanced) | seal | tier-1 | 9 | 7 | 0 | 2 | 0.7778 | `ki de / ki #005 / #036 ke / i ja ro` |
| CHIC #299 | Crete (unprovenanced) | seal | tier-2 | 9 | 7 | 0 | 2 | 0.7778 | `ki de / ki #005 / #036 ke / i ja ro` |
| CHIC #299 | Crete (unprovenanced) | seal | tier-3 | 9 | 7 | 1 | 1 | 0.8889 | `ki de / ki [STOP:#005] / #036 ke / i ja ro` |
| CHIC #299 | Crete (unprovenanced) | seal | tier-4 | 9 | 7 | 2 | 0 | 1.0000 | `ki de / ki [STOP:#005] / [GLIDE:#036] ke / i ja ro` |
| CHIC #300 | Crete (unprovenanced) | seal | tier-1 | 10 | 6 | 0 | 4 | 0.6000 | `ki de / i ja ro / ki #036 #018 / #014 #050` |
| CHIC #300 | Crete (unprovenanced) | seal | tier-2 | 10 | 6 | 0 | 4 | 0.6000 | `ki de / i ja ro / ki #036 #018 / #014 #050` |
| CHIC #300 | Crete (unprovenanced) | seal | tier-3 | 10 | 6 | 1 | 3 | 0.7000 | `ki de / i ja ro / ki #036 #018 / #014 [GLIDE:#050]` |
| CHIC #300 | Crete (unprovenanced) | seal | tier-4 | 10 | 6 | 4 | 0 | 1.0000 | `ki de / i ja ro / ki [GLIDE:#036] [GLIDE:#018] / [GLIDE:#014] [GLIDE:#050]` |
| CHIC #301 | Crete (unprovenanced) | seal | tier-1 | 9 | 6 | 0 | 3 | 0.6667 | `ki de / ki #005 / #018 #046 / wa ke ro` |
| CHIC #301 | Crete (unprovenanced) | seal | tier-2 | 9 | 6 | 0 | 3 | 0.6667 | `ki de / ki #005 / #018 #046 / wa ke ro` |
| CHIC #301 | Crete (unprovenanced) | seal | tier-3 | 9 | 6 | 1 | 2 | 0.7778 | `ki de / ki [STOP:#005] / #018 #046 / wa ke ro` |
| CHIC #301 | Crete (unprovenanced) | seal | tier-4 | 9 | 6 | 3 | 0 | 1.0000 | `ki de / ki [STOP:#005] / [GLIDE:#018] [GLIDE:#046] / wa ke ro` |
| CHIC #302 | Crete (unprovenanced) | seal | tier-1 | 12 | 7 | 0 | 5 | 0.5833 | `je #034 ki de / #046 ki / #006 #062 #012 / i ja ro` |
| CHIC #302 | Crete (unprovenanced) | seal | tier-2 | 12 | 8 | 0 | 4 | 0.6667 | `je #034 ki de / #046 ki / #006 #062 wa / i ja ro` |
| CHIC #302 | Crete (unprovenanced) | seal | tier-3 | 12 | 8 | 1 | 3 | 0.7500 | `je #034 ki de / #046 ki / [GLIDE:#006] #062 wa / i ja ro` |
| CHIC #302 | Crete (unprovenanced) | seal | tier-4 | 12 | 8 | 4 | 0 | 1.0000 | `je [LIQUID:#034] ki de / [GLIDE:#046] ki / [GLIDE:#006] [GLIDE:#062] wa / i ja ro` |
| CHIC #303 | Crete (unprovenanced) | seal | tier-1 | 12 | 9 | 0 | 3 | 0.7500 | `#062 #020 ti / wa mu te / [?:ke] #039 [?:i] ro / ki de` |
| CHIC #303 | Crete (unprovenanced) | seal | tier-2 | 12 | 9 | 0 | 3 | 0.7500 | `#062 #020 ti / wa mu te / [?:ke] #039 [?:i] ro / ki de` |
| CHIC #303 | Crete (unprovenanced) | seal | tier-3 | 12 | 9 | 2 | 1 | 0.9167 | `#062 [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` |
| CHIC #303 | Crete (unprovenanced) | seal | tier-4 | 12 | 9 | 3 | 0 | 1.0000 | `[GLIDE:#062] [VOWEL:#020] ti / wa mu te / [?:ke] [STOP:#039] [?:i] ro / ki de` |
| CHIC #304 | Crete (unprovenanced) | seal | tier-1 | 9 | 5 | 0 | 4 | 0.5556 | `#039 pa / #036 pa / #011 [?:ja] / #076 pa ro` |
| CHIC #304 | Crete (unprovenanced) | seal | tier-2 | 9 | 5 | 0 | 4 | 0.5556 | `#039 pa / #036 pa / #011 [?:ja] / #076 pa ro` |
| CHIC #304 | Crete (unprovenanced) | seal | tier-3 | 9 | 5 | 2 | 2 | 0.7778 | `[STOP:#039] pa / #036 pa / [LIQUID:#011] [?:ja] / #076 pa ro` |
| CHIC #304 | Crete (unprovenanced) | seal | tier-4 | 9 | 5 | 4 | 0 | 1.0000 | `[STOP:#039] pa / [GLIDE:#036] pa / [LIQUID:#011] [?:ja] / [GLIDE:#076] pa ro` |
| CHIC #305 | Lastros | seal | tier-1 | 8 | 5 | 0 | 3 | 0.6250 | `wa #066 a #062 / ki de / ki #005 / IDEO:#181 / IDEO:#180` |
| CHIC #305 | Lastros | seal | tier-2 | 8 | 5 | 0 | 3 | 0.6250 | `wa #066 a #062 / ki de / ki #005 / IDEO:#181 / IDEO:#180` |
| CHIC #305 | Lastros | seal | tier-3 | 8 | 5 | 2 | 1 | 0.8750 | `wa [STOP:#066] a #062 / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` |
| CHIC #305 | Lastros | seal | tier-4 | 8 | 5 | 3 | 0 | 1.0000 | `wa [STOP:#066] a [GLIDE:#062] / ki de / ki [STOP:#005] / IDEO:#181 / IDEO:#180` |
| CHIC #306 | Mallia | seal | tier-1 | 12 | 3 | 0 | 9 | 0.2500 | `#052 #050 mu / #036 i [?:#076] / #039 #056 [?:#014] / je #018 #050` |
| CHIC #306 | Mallia | seal | tier-2 | 12 | 3 | 0 | 9 | 0.2500 | `#052 #050 mu / #036 i [?:#076] / #039 #056 [?:#014] / je #018 #050` |
| CHIC #306 | Mallia | seal | tier-3 | 12 | 3 | 4 | 5 | 0.5833 | `#052 [GLIDE:#050] mu / #036 i [?:#076] / [STOP:#039] [STOP:#056] [?:#014] / je #018 [GLIDE:#050]` |
| CHIC #306 | Mallia | seal | tier-4 | 12 | 3 | 9 | 0 | 1.0000 | `[LIQUID:#052] [GLIDE:#050] mu / [GLIDE:#036] i [?:GLIDE:#076] / [STOP:#039] [STOP:#056] [?:GLIDE:#014] / je [GLIDE:#018] [GLIDE:#050]` |
| CHIC #308 | Palaikastro | seal | tier-1 | 9 | 5 | 0 | 4 | 0.5556 | `#036 ke ro / #034 #007 / ki de / IDEO:#174 / ki #005` |
| CHIC #308 | Palaikastro | seal | tier-2 | 9 | 5 | 0 | 4 | 0.5556 | `#036 ke ro / #034 #007 / ki de / IDEO:#174 / ki #005` |
| CHIC #308 | Palaikastro | seal | tier-3 | 9 | 5 | 2 | 2 | 0.7778 | `#036 ke ro / #034 [VOWEL:#007] / ki de / IDEO:#174 / ki [STOP:#005]` |
| CHIC #308 | Palaikastro | seal | tier-4 | 9 | 5 | 4 | 0 | 1.0000 | `[GLIDE:#036] ke ro / [LIQUID:#034] [VOWEL:#007] / ki de / IDEO:#174 / ki [STOP:#005]` |
| CHIC #309 | Pyrgos (Myrtos) | seal | tier-1 | 12 | 9 | 0 | 3 | 0.7500 | `ki #005 / wa #040 me ni / i ja ro / #036 ke ro` |
| CHIC #309 | Pyrgos (Myrtos) | seal | tier-2 | 12 | 9 | 0 | 3 | 0.7500 | `ki #005 / wa #040 me ni / i ja ro / #036 ke ro` |
| CHIC #309 | Pyrgos (Myrtos) | seal | tier-3 | 12 | 9 | 2 | 1 | 0.9167 | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / #036 ke ro` |
| CHIC #309 | Pyrgos (Myrtos) | seal | tier-4 | 12 | 9 | 3 | 0 | 1.0000 | `ki [STOP:#005] / wa [STOP:#040] me ni / i ja ro / [GLIDE:#036] ke ro` |
| CHIC #310 | Sitia | seal | tier-1 | 9 | 4 | 0 | 5 | 0.4444 | `je #034 #056 / #017 #050 / NUM:1 / #046 ki / wa i` |
| CHIC #310 | Sitia | seal | tier-2 | 9 | 4 | 0 | 5 | 0.4444 | `je #034 #056 / #017 #050 / NUM:1 / #046 ki / wa i` |
| CHIC #310 | Sitia | seal | tier-3 | 9 | 4 | 3 | 2 | 0.7778 | `je #034 [STOP:#056] / [NASAL:#017] [GLIDE:#050] / NUM:1 / #046 ki / wa i` |
| CHIC #310 | Sitia | seal | tier-4 | 9 | 4 | 5 | 0 | 1.0000 | `je [LIQUID:#034] [STOP:#056] / [NASAL:#017] [GLIDE:#050] / NUM:1 / [GLIDE:#046] ki / wa i` |
| CHIC #311 | Sitia | seal | tier-1 | 6 | 5 | 0 | 1 | 0.8333 | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:#005] / [?:ki] [?:de]` |
| CHIC #311 | Sitia | seal | tier-2 | 6 | 5 | 0 | 1 | 0.8333 | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:#005] / [?:ki] [?:de]` |
| CHIC #311 | Sitia | seal | tier-3 | 6 | 5 | 1 | 0 | 1.0000 | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` |
| CHIC #311 | Sitia | seal | tier-4 | 6 | 5 | 1 | 0 | 1.0000 | `[?:i] [?:ja] / [?] [?] [?] / [?:ki] [?:STOP:#005] / [?:ki] [?:de]` |
| CHIC #312 | Xida | seal | tier-1 | 11 | 8 | 0 | 3 | 0.7273 | `i ja ro / #036 ke ro / #047 de [?:pa] / #076 pa` |
| CHIC #312 | Xida | seal | tier-2 | 11 | 8 | 0 | 3 | 0.7273 | `i ja ro / #036 ke ro / #047 de [?:pa] / #076 pa` |
| CHIC #312 | Xida | seal | tier-3 | 11 | 8 | 0 | 3 | 0.7273 | `i ja ro / #036 ke ro / #047 de [?:pa] / #076 pa` |
| CHIC #312 | Xida | seal | tier-4 | 11 | 8 | 3 | 0 | 1.0000 | `i ja ro / [GLIDE:#036] ke ro / [LIQUID:#047] de [?:pa] / [GLIDE:#076] pa` |
| CHIC #313 | Crete (seal/sealing, mixed sites) | seal | tier-1 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #313 | Crete (seal/sealing, mixed sites) | seal | tier-2 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #313 | Crete (seal/sealing, mixed sites) | seal | tier-3 | 5 | 3 | 0 | 2 | 0.6000 | `wa ke / ke #095 #052` |
| CHIC #313 | Crete (seal/sealing, mixed sites) | seal | tier-4 | 5 | 3 | 2 | 0 | 1.0000 | `wa ke / ke [GLIDE:#095] [LIQUID:#052]` |
| CHIC #314 | Neapolis | seal | tier-1 | 24 | 12 | 0 | 12 | 0.5000 | `#050 ro #034 / ki de / #050 #007 #018 / #046 IDEO:#168 ki / i ja ro / #036 ke ro / ki de / [?:#018] #043 / #018 #043 / ki #005` |
| CHIC #314 | Neapolis | seal | tier-2 | 24 | 12 | 0 | 12 | 0.5000 | `#050 ro #034 / ki de / #050 #007 #018 / #046 IDEO:#168 ki / i ja ro / #036 ke ro / ki de / [?:#018] #043 / #018 #043 / ki #005` |
| CHIC #314 | Neapolis | seal | tier-3 | 24 | 12 | 6 | 6 | 0.7500 | `[GLIDE:#050] ro #034 / ki de / [GLIDE:#050] [VOWEL:#007] #018 / #046 IDEO:#168 ki / i ja ro / #036 ke ro / ki de / [?:#018] [LIQUID:#043] / #018 [LIQUID:#043] / ki [STOP:#005]` |
| CHIC #314 | Neapolis | seal | tier-4 | 24 | 12 | 12 | 0 | 1.0000 | `[GLIDE:#050] ro [LIQUID:#034] / ki de / [GLIDE:#050] [VOWEL:#007] [GLIDE:#018] / [GLIDE:#046] IDEO:#168 ki / i ja ro / [GLIDE:#036] ke ro / ki de / [?:GLIDE:#018] [LIQUID:#043] / [GLIDE:#018] [LIQUID:#043] / ki [STOP:#005]` |
| CHIC #315 | Arkhanes | seal | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#181 / IDEO:#134` |
| CHIC #315 | Arkhanes | seal | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#181 / IDEO:#134` |
| CHIC #315 | Arkhanes | seal | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#181 / IDEO:#134` |
| CHIC #315 | Arkhanes | seal | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `IDEO:#181 / IDEO:#134` |
| CHIC #316 | Mallia | chamaizi_vase | tier-1 | 4 | 3 | 0 | 1 | 0.7500 | `de ni #006 ta` |
| CHIC #316 | Mallia | chamaizi_vase | tier-2 | 4 | 3 | 0 | 1 | 0.7500 | `de ni #006 ta` |
| CHIC #316 | Mallia | chamaizi_vase | tier-3 | 4 | 3 | 1 | 0 | 1.0000 | `de ni [GLIDE:#006] ta` |
| CHIC #316 | Mallia | chamaizi_vase | tier-4 | 4 | 3 | 1 | 0 | 1.0000 | `de ni [GLIDE:#006] ta` |
| CHIC #317 | Mallia | pithos | tier-1 | 7 | 4 | 0 | 3 | 0.5714 | `wa je [?:ja] #034 ti [?:#093] [?:#065]` |
| CHIC #317 | Mallia | pithos | tier-2 | 7 | 4 | 0 | 3 | 0.5714 | `wa je [?:ja] #034 ti [?:#093] [?:#065]` |
| CHIC #317 | Mallia | pithos | tier-3 | 7 | 4 | 1 | 2 | 0.7143 | `wa je [?:ja] #034 ti [?:#093] [?:STOP:#065]` |
| CHIC #317 | Mallia | pithos | tier-4 | 7 | 4 | 2 | 1 | 0.8571 | `wa je [?:ja] [LIQUID:#034] ti [?:#093] [?:STOP:#065]` |
| CHIC #318 | Mallia | unknown | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `[?:#051] ke ke` |
| CHIC #318 | Mallia | unknown | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `[?:#051] ke ke` |
| CHIC #318 | Mallia | unknown | tier-3 | 3 | 2 | 0 | 1 | 0.6667 | `[?:#051] ke ke` |
| CHIC #318 | Mallia | unknown | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `[?:GLIDE:#051] ke ke` |
| CHIC #319 | Mallia | pithos | tier-1 | 4 | 1 | 0 | 3 | 0.2500 | `[?:#088] #087 ra #027` |
| CHIC #319 | Mallia | pithos | tier-2 | 4 | 1 | 0 | 3 | 0.2500 | `[?:#088] #087 ra #027` |
| CHIC #319 | Mallia | pithos | tier-3 | 4 | 1 | 1 | 2 | 0.5000 | `[?:#088] #087 ra [GLIDE:#027]` |
| CHIC #319 | Mallia | pithos | tier-4 | 4 | 1 | 1 | 2 | 0.5000 | `[?:#088] #087 ra [GLIDE:#027]` |
| CHIC #320 | Mallia | vase | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `ni #059 ta / [?]` |
| CHIC #320 | Mallia | vase | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `ni #059 ta / [?]` |
| CHIC #320 | Mallia | vase | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `ni [GLIDE:#059] ta / [?]` |
| CHIC #320 | Mallia | vase | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `ni [GLIDE:#059] ta / [?]` |
| CHIC #321 | Mallia | potsherd | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `[?:#056] ra` |
| CHIC #321 | Mallia | potsherd | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `[?:#056] ra` |
| CHIC #321 | Mallia | potsherd | tier-3 | 2 | 1 | 1 | 0 | 1.0000 | `[?:STOP:#056] ra` |
| CHIC #321 | Mallia | potsherd | tier-4 | 2 | 1 | 1 | 0 | 1.0000 | `[?:STOP:#056] ra` |
| CHIC #322 | Mallia | chamaizi_vase | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `#008 #068` |
| CHIC #322 | Mallia | chamaizi_vase | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `#008 #068` |
| CHIC #322 | Mallia | chamaizi_vase | tier-3 | 2 | 0 | 1 | 1 | 0.5000 | `[GLIDE:#008] #068` |
| CHIC #322 | Mallia | chamaizi_vase | tier-4 | 2 | 0 | 2 | 0 | 1.0000 | `[GLIDE:#008] [LIQUID:#068]` |
| CHIC #323 | Mallia | pithos | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:6 [?]` |
| CHIC #323 | Mallia | pithos | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:6 [?]` |
| CHIC #323 | Mallia | pithos | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:6 [?]` |
| CHIC #323 | Mallia | pithos | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:6 [?]` |
| CHIC #324 | Mallia | chamaizi_vase | tier-1 | 4 | 2 | 0 | 2 | 0.5000 | `je #023 ra #018` |
| CHIC #324 | Mallia | chamaizi_vase | tier-2 | 4 | 2 | 0 | 2 | 0.5000 | `je #023 ra #018` |
| CHIC #324 | Mallia | chamaizi_vase | tier-3 | 4 | 2 | 0 | 2 | 0.5000 | `je #023 ra #018` |
| CHIC #324 | Mallia | chamaizi_vase | tier-4 | 4 | 2 | 2 | 0 | 1.0000 | `je [LIQUID:#023] ra [GLIDE:#018]` |
| CHIC #325 | Mallia | chamaizi_vase | tier-1 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:28 [?]` |
| CHIC #325 | Mallia | chamaizi_vase | tier-2 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:28 [?]` |
| CHIC #325 | Mallia | chamaizi_vase | tier-3 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:28 [?]` |
| CHIC #325 | Mallia | chamaizi_vase | tier-4 | 0 | 0 | 0 | 0 | 0.0000 | `NUM:28 [?]` |
| CHIC #326 | Mallia | chamaizi_vase | tier-1 | 1 | 1 | 0 | 0 | 1.0000 | `[?] me` |
| CHIC #326 | Mallia | chamaizi_vase | tier-2 | 1 | 1 | 0 | 0 | 1.0000 | `[?] me` |
| CHIC #326 | Mallia | chamaizi_vase | tier-3 | 1 | 1 | 0 | 0 | 1.0000 | `[?] me` |
| CHIC #326 | Mallia | chamaizi_vase | tier-4 | 1 | 1 | 0 | 0 | 1.0000 | `[?] me` |
| CHIC #327 | Mallia | chamaizi_vase | tier-1 | 3 | 2 | 0 | 1 | 0.6667 | `de ni #006 / NUM:57` |
| CHIC #327 | Mallia | chamaizi_vase | tier-2 | 3 | 2 | 0 | 1 | 0.6667 | `de ni #006 / NUM:57` |
| CHIC #327 | Mallia | chamaizi_vase | tier-3 | 3 | 2 | 1 | 0 | 1.0000 | `de ni [GLIDE:#006] / NUM:57` |
| CHIC #327 | Mallia | chamaizi_vase | tier-4 | 3 | 2 | 1 | 0 | 1.0000 | `de ni [GLIDE:#006] / NUM:57` |
| CHIC #328 | Mallia | offering_table | tier-1 | 16 | 7 | 0 | 9 | 0.4375 | `[?:#062] #034 #002 #056 ra ta ke #051 ra #094 #034 #056 ma de i #029` |
| CHIC #328 | Mallia | offering_table | tier-2 | 16 | 7 | 0 | 9 | 0.4375 | `[?:#062] #034 #002 #056 ra ta ke #051 ra #094 #034 #056 ma de i #029` |
| CHIC #328 | Mallia | offering_table | tier-3 | 16 | 7 | 3 | 6 | 0.6250 | `[?:#062] #034 [LIQUID:#002] [STOP:#056] ra ta ke #051 ra #094 #034 [STOP:#056] ma de i #029` |
| CHIC #328 | Mallia | offering_table | tier-4 | 16 | 7 | 9 | 0 | 1.0000 | `[?:GLIDE:#062] [LIQUID:#034] [LIQUID:#002] [STOP:#056] ra ta ke [GLIDE:#051] ra [LIQUID:#094] [LIQUID:#034] [STOP:#056] ma de i [LIQUID:#029]` |
| CHIC #329 | Mallia | chamaizi_vase | tier-1 | 2 | 2 | 0 | 0 | 1.0000 | `de wa` |
| CHIC #329 | Mallia | chamaizi_vase | tier-2 | 2 | 2 | 0 | 0 | 1.0000 | `de wa` |
| CHIC #329 | Mallia | chamaizi_vase | tier-3 | 2 | 2 | 0 | 0 | 1.0000 | `de wa` |
| CHIC #329 | Mallia | chamaizi_vase | tier-4 | 2 | 2 | 0 | 0 | 1.0000 | `de wa` |
| CHIC #330 | Mallia | potsherd | tier-1 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#029] #064 [?]` |
| CHIC #330 | Mallia | potsherd | tier-2 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#029] #064 [?]` |
| CHIC #330 | Mallia | potsherd | tier-3 | 2 | 0 | 0 | 2 | 0.0000 | `[?:#029] #064 [?]` |
| CHIC #330 | Mallia | potsherd | tier-4 | 2 | 0 | 1 | 1 | 0.5000 | `[?:LIQUID:#029] #064 [?]` |
| CHIC #331 | Prodromos | chamaizi_vase | tier-1 | 2 | 1 | 0 | 1 | 0.5000 | `wa #091` |
| CHIC #331 | Prodromos | chamaizi_vase | tier-2 | 2 | 1 | 0 | 1 | 0.5000 | `wa #091` |
| CHIC #331 | Prodromos | chamaizi_vase | tier-3 | 2 | 1 | 0 | 1 | 0.5000 | `wa #091` |
| CHIC #331 | Prodromos | chamaizi_vase | tier-4 | 2 | 1 | 0 | 1 | 0.5000 | `wa #091` |

## Citations

- Olivier, J.-P. & Godart, L. (1996). _CHIC._
- Younger, J. G. (online). _The Cretan Hieroglyphic Texts._
- Salgarella, E. (2020). _Aegean Linear Script(s)._
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
