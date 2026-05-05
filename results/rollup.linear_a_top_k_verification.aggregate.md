# Linear A v26 top-K verification — aggregate (mg-c202)

Aggregate v26 verification report across all four substrate pools (aquitanian / etruscan / toponym / eteocretan), plus a side-by-side comparison with chic-v6 (mg-a557) — the CHIC-side analog. Built by `scripts/build_linear_a_v26.py`.

## Headline

Per the v26 brief: a Linear A pool top-20 verification rate ≥ chic-v6's tier-1 → tier-2 lift (+3 inscriptions / +20 hits) supports a "verification methodology is portable cross-script" claim. A Linear A pool top-20 verification rate uniformly below the chic-v6 tier-1 baseline (67/302 = 22.19%) supports the v22 / v24 / chic-v6-tier-3+ negative-validation pattern at the leaderboard-top-K granularity (a stricter test than v22's per-inscription consensus).

**All four Linear A pools produce a match-count lift ≥ chic-v6's tier-1 → tier-2 inscription lift (+3).** The verification methodology runs cross-script: the leaderboard top-K passes the same external-scholarship test on the Linear A side that chic-v6's tier-2 passed on the CHIC side, with each pool's extended subset clearing the +3-inscriptions threshold (aquitanian +5, etruscan +6, toponym +7, eteocretan +5).

**Structural asymmetry caveat.** chic-v6's tier-2 added only 3 specific-phoneme overrides corpus-wide (`#001 → wa`, `#012 → wa`, `#032 → ki`) — a tightly-constrained, low-density extension. Linear A v26's per-pool extension applies each top-20 substrate hypothesis's full sign_to_phoneme map (typically 5-10 newly-anchored AB signs per hypothesis), so the absolute lift magnitudes (`+9216 hits`, etc.) are not directly comparable to chic-v6's `+20 hits`. The directional verdict (lift exists / does not exist) IS comparable, and the per-surface verification status (verified / unverified) is comparable to chic-v6's enumeration of +/- entries at tier-2. Sign-level inverse-verifications (recorded below per-pool) are the load-bearing negative-evidence companion: every Aquitanian top-20 surface that pinned `AB59` proposed a value differing from the scholarly `ta`, for example.

## Per-pool aggregate vs LB-carryover-baseline lift

Lift is computed against the LB-carryover-only baseline rendered on the SAME inscription subset that each pool extended (the inscriptions where any top-20 substrate surface had a positive paired-diff record). This is the analog of chic-v6's tier-1 → tier-2 lift, except chic-v6 was over the full corpus and v26 is over the per-pool "extended-inscriptions" subset.

| pool | n top-20 surfaces with ≥1 positive record | n inscriptions extended | match rate (extended) | n inscriptions with match | total a+b+c hits | lift (inscriptions) | lift (hits) | inverse-verifications |
|:--|---:|---:|---:|---:|---:|--:|--:|--:|
| aquitanian | 20 | 40 | 0.9500 | 38 | 9667 | +5 | +9216 | 29 |
| etruscan | 20 | 42 | 0.9524 | 40 | 10368 | +6 | +9925 | 22 |
| toponym | 20 | 39 | 1.0000 | 39 | 14524 | +7 | +14106 | 19 |
| eteocretan | 20 | 42 | 0.8810 | 37 | 7590 | +5 | +7172 | 30 |

## Side-by-side with chic-v6 (mg-a557)

chic-v6's tier-1 baseline = chic-v2 paleographic-anchor pool (20 anchors). chic-v6's tier-2 = tier-1 ∪ specific-phoneme overrides for chic-v5 tier-2 candidates (`#001 → wa`, `#012 → wa`, `#032 → ki`). chic-v6's tier-1 → tier-2 lift was +3 inscriptions / +20 hits over a 302-inscription CHIC corpus.

| script side | tier-1 baseline | tier-2 (extension) | lift (inscriptions) | lift (a+b+c hits) |
|:--|:--|:--|--:|--:|
| CHIC chic-v6 | 67/302 = 0.2219 | 70/302 = 0.2318 | +3 | +20 |
| Linear A v26 — aquitanian | 33/40 = 0.8250 | 38/40 = 0.9500 | +5 | +9216 |
| Linear A v26 — etruscan | 34/42 = 0.8095 | 40/42 = 0.9524 | +6 | +9925 |
| Linear A v26 — toponym | 32/39 = 0.8205 | 39/39 = 1.0000 | +7 | +14106 |
| Linear A v26 — eteocretan | 32/42 = 0.7619 | 37/42 = 0.8810 | +5 | +7172 |

## LB-carryover-only baseline (Linear A corpus)

Inputs: 772 Linear A inscriptions; 35 scholar-proposed entries; 112 toponym surfaces.

| metric | value |
|:--|--:|
| n inscriptions | 772 |
| n inscriptions with ≥1 source-A/B/C match | 177 |
| match rate (any) | 0.2293 |
| total source-A hits | 1378 |
| total source-B hits | 316 |
| total source-C hits | 3 |

## Discipline framing

v26 is a verification-rate report, not a decipherment claim. Match criteria reuse chic-v6 verbatim (no relaxation). The outcome — high or low — is publishable. A low Linear A verification rate is consistent with v22's 3.95% Linear A per-inscription consensus baseline (mg-46d5) and with v24's cascade-candidate-under-Eteocretan-LM null result (mg-c103); a high rate at any pool would parallel chic-v6's positive #032 → ki tier-2 lift on the CHIC side.

## Determinism

- No RNG.
- All sortings deterministic.

## Citations

- Younger, J. G. (online). _Linear A texts in phonetic transcription._
- Olivier, J.-P. & Godart, L. (1996). _CHIC._
- Salgarella, E. (2020). _Aegean Linear Script(s)._
- Ventris, M. & Chadwick, J. (1956). _Documents in Mycenaean Greek._
- Beekes, R. S. P. (2010). _Etymological Dictionary of Greek._ (Pre-Greek substrate appendix.)
- Furnée, E. J. (1972). _Die wichtigsten konsonantischen Erscheinungen des Vorgriechischen._
