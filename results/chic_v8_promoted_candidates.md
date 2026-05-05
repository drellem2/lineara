# CHIC dual-script bilingual promoted candidates (chic-v8; mg-dfcc)

Per the chic-v8 brief: enumeration of any chic-v5 tier-3 or tier-4 candidate that promotes to tier-2 under the 4-of-5 rule with the L5 (LA-constraint) line of evidence added. Built by `scripts/build_chic_v8.py`.

## Headline

**0 new tier-2 candidates** derivable via the chic-v8 bilingual extension on the v0 corpora.

L5 is silent for all 76 unknown CHIC syllabographic signs because the chic-v0 + LA-v0 corpora do not contain any genuinely-dual-script artifact (an artifact bearing parallel inscriptions in both Cretan Hieroglyphic and Linear A on the same physical object). With L4 silent by chic-v5 construction and L5 silent by chic-v8 corpus state, the 4-of-5 promotion rule reduces to chic-v5's 3-of-3 (L1+L2+L3 unanimity) — byte-identical to the chic-v5 tier-2 criterion. No new tier-2 candidates are produced.

## Promoted candidates (none)

| sign | freq | from | to | L1 | L2 | L3 | L4 | L5 |
|---|---:|---|---|---|---|---|---|---|
| _(no rows; null result)_ |  |  |  |  |  |  |  |  |

## Tier-3 → tier-2 single-step promotions: none

29 chic-v5 tier-3 signs inspected (`#002, #005, #006, #007, #008, #009, #011, #017, #020, #021, #027, #033, #037, #039, #040, #043, #045, #050, #055, #056, #058, #059, #060, #063, #065, #066, #069, #072, #078`). For each, L5 is silent because no genuine dual- script artifact in the v0 corpora carries the sign at a position parallel to a confidently-read LA sign.

## Tier-4 → tier-2 single-step promotions: none

17 chic-v5 tier-4 signs inspected (`#003, #004, #014, #018, #023, #029, #034, #036, #046, #047, #051, #052, #062, #068, #076, #094, #095`). Tier-4 → tier-2 in a single step would require **three** confirming votes from L4+L5 alone (since tier-4 has only 1 of 4 chic-v5 lines yielding a class) — methodologically weak even if corpus state were to provide L5 votes; flagged for investigation rather than silent promotion per the chic-v8 brief. The v0 corpus state makes the question moot for now.

## Reproducibility

Built by `scripts/build_chic_v8.py` from the same inputs as `results/chic_dual_script_bilingual_leaderboard.md`. Re-run with `python3 scripts/build_chic_v8.py`.
