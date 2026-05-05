# Linear A side leave-one-out validation of the chic-v5 framework on LB-carryover anchors (v28; mg-4a7b)

## Method

For each of the 21 Linear A LB-carryover anchors S (parsed from `pools/linear_b_carryover.yaml`'s 21 well-attested AB-sign → phoneme citations; AB123 excluded as conjectural per Younger), S is removed from the LB-carryover pool (yielding a reduced 20-anchor pool), then S is treated as unknown by the chic-v5 framework and the three non-circular lines of evidence are recomputed against the reduced pool. The framework's proposed phoneme class is then compared to V's known class.

- **L1 distributional plurality** — top-3 nearest anchors by mean Bhattacharyya similarity over four per-AB-sign fingerprint dimensions (`left_neighbor`, `right_neighbor`, `position`, `support`); plurality vote on phoneme class. Fingerprints are computed over the full 772-inscription Linear A corpus.
- **L2 strict-top-1 anchor distance** — single nearest anchor's phoneme class.
- **L3 substrate-consistency under the v21 Eteocretan LM** — for each candidate value V in the rebuilt candidate-value pool, score (LB-carryover anchors ∪ {S → V}) under the v21 Eteocretan LM via `external_phoneme_perplexity_v0`; per-class mean paired_diff picks the winning class. Same machinery as chic-v5/chic-v9; the LM choice is symmetric with chic-v9.
- **L4 cross-script paleographic** is **deliberately excluded**: the LB-carryover anchor pool's known values are themselves derived via paleographic similarity to deciphered Linear B signs (Ventris-Chadwick 1956), so for any anchor S the L4 line trivially recovers V by construction. Including L4 would make the LOO test circular and inflate accuracy. With L4 excluded the framework's tier classification reduces from the chic-v5 4-line scheme to a 3-line scheme:

- **tier-2** — 3-of-3 unanimity on the top class.
- **tier-3** — 2-of-3 agreement.
- **tier-4** — 1-of-3 (single line of evidence).
- **untiered** — 0 voting lines (no fingerprint signal).

### LM choice for L3

The v21 Eteocretan LM is used, in **direct symmetry with chic-v9** (mg-18cb). The methodologically-symmetric alternative would be to pick a per-anchor LM keyed on the candidate's substrate pool, but LB-carryover anchors are not naturally partitioned across the v10/v18/v21 substrate pools — they are paleographic carryovers from deciphered Linear B signs, not predictions from any single substrate. Eteocretan was the strongest pool on Linear A (v21 PASSed at +0.20 gap) and the strongest pool on CHIC, so the LM-bias profile is symmetric across scripts. Using it here keeps the LA-side comparison apples-to-apples with chic-v9.

### Inclusion criterion for the anchor pool

The anchor pool is the set of AB signs whose Linear-B carryover phonetic value is embedded as an `AB##=phon` pair in the `pools/linear_b_carryover.yaml` source citations. This is the **well-attested-citation** subset: the citation strings on every entry follow Younger 2020 (online edition) plus Ventris-Chadwick 1956 carryover values. AB123 (proposed `na` in the v4_anchor_taina_HT39 hypothesis) is **excluded** because Younger's own citation flags AB123 as conjectural and the pool yaml's citation does not embed it as a stable `AB123=na` entry. v28 inherits that inclusion criterion verbatim, yielding 21 well-attested anchors. (For comparison: chic-v9 ran 20 anchors from chic-v2's paleographic-candidate pool; the LA-side anchor pool size of 21 is comparable.)

The candidate-value pool for L3 is rebuilt from the reduced 20-anchor pool's distinct LB-carryover values plus bare vowels a/e/i/o/u, filtered to values whose first character is in the Eteocretan phoneme inventory (chic-v5 convention). Where the rebuild removes the held-out value entirely (typical when the held-out value has no other anchor sharing it), L3 can still recover the *class* if another candidate in the pool shares it. Where the held-out class itself has no other representative in the rebuilt pool, L3 cannot recover the class by construction; this is flagged with ⚠ in the per-anchor table.

## Aggregate accuracy

Of the 21 LB-carryover anchors run blind under L1+L2+L3, the framework's proposed class agrees with the known class on **7/21 (33.3%)**. This is the headline LA-side LOO validation number.

| metric | value |
|---|---:|
| n anchors run blind | 21 |
| n with framework_class == known_class | 7 |
| **aggregate LA-side LOO accuracy** | **33.3%** |
| chance baseline (6-class taxonomy) | ~16.7% |
| chic-v9 (CHIC-side) aggregate LOO accuracy | 20.0% |
| **delta (LA − CHIC)** | **+13.3%** |
| n LOO tier-2 (3-of-3 unanimity) | 3 |
| n LOO tier-3 (2-of-3) | 11 |
| n LOO tier-4 (1-of-3) | 7 |
| n LOO untiered (0 votes) | 0 |

Validation regime: **not validated** — at the chic-v9 brief's thresholds (>70% high; 40-70% moderate; <40% low), the framework's L1+L2+L3 recovery accuracy of 33.3% on the LA side places this LOO test in the **low-agreement** band.

## Per-anchor LOO results

Each row below is one LOO run: the named anchor was removed from the LB-carryover pool and treated as unknown; the three lines voted on its class against the reduced 20-anchor pool. Tier here is the L1+L2+L3-only tier (3-of-3 = tier-2, 2-of-3 = tier-3, etc.). The agreement column is whether the framework's proposed class matches the known class.

| anchor | freq | known phoneme | known class | framework class | tier | agreement | L1 | L2 | L3 |
|---|---:|---|---|---|:---:|:---:|:---:|:---:|:---:|
| `AB01` | 99 | `da` | stop | fricative | tier-4 | ✗ | liquid | nasal | fricative |
| `AB02` | 89 | `ro` | liquid | liquid | tier-3 | ✓ | liquid | liquid | nasal |
| `AB03` | 82 | `pa` | stop | stop | tier-3 | ✓ | stop | vowel | stop |
| `AB04` | 75 | `te` | stop | fricative | tier-4 | ✗ | nasal | stop | fricative |
| `AB06` | 97 | `na` | nasal | stop | tier-2 | ✗ | stop | stop | stop |
| `AB07` | 79 | `di` | stop | stop | tier-3 | ✓ | stop | stop | nasal |
| `AB08` | 136 | `a` | vowel | stop | tier-2 | ✗ | stop | stop | stop |
| `AB09` | 47 | `se` | fricative | stop | tier-3 | ✗ | stop | stop | nasal ⚠ |
| `AB26` | 69 | `ru` | liquid | liquid | tier-4 | ✓ | liquid | stop | nasal |
| `AB27` | 91 | `re` | liquid | nasal | tier-2 | ✗ | nasal | nasal | nasal |
| `AB28` | 95 | `i` | vowel | fricative | tier-4 | ✗ | nasal | stop | fricative |
| `AB39` | 37 | `pi` | stop | glide | tier-4 | ✗ | glide | liquid | nasal |
| `AB56` | 40 | `pa3` | stop | liquid | tier-3 | ✗ | liquid | liquid | nasal |
| `AB57` | 87 | `ja` | glide | nasal | tier-3 | ✗ | nasal | nasal | stop ⚠ |
| `AB59` | 106 | `ta` | stop | stop | tier-3 | ✓ | stop | stop | fricative |
| `AB60` | 85 | `ra` | liquid | nasal | tier-3 | ✗ | nasal | nasal | stop |
| `AB67` | 93 | `ki` | stop | stop | tier-3 | ✓ | stop | stop | nasal |
| `AB73` | 68 | `mi` | nasal | stop | tier-3 | ✗ | stop | stop | nasal |
| `AB77` | 92 | `ka` | stop | fricative | tier-4 | ✗ | nasal | stop | fricative |
| `AB80` | 84 | `ma` | nasal | fricative | tier-4 | ✗ | glide | stop | fricative |
| `AB81` | 138 | `ku` | stop | stop | tier-3 | ✓ | stop | stop | nasal |

⚠ marker on L3 indicates that the held-out anchor's class had no other representative in the rebuilt candidate-value pool, so L3 was structurally unable to recover that class. Total such cases: 2/21.

## Per-line accuracy decomposition

How accurately does each line, run in isolation, recover the known class on the LOO test? This decomposition diagnoses which lines carry the signal and which are noise — and lets us compare per-line behaviour to chic-v9's CHIC-side LOO.

| line | LA-side n_correct/n_total | LA-side accuracy | chic-v9 (CHIC-side) accuracy | delta (LA − CHIC) |
|---|:---:|---:|---:|---:|
| L1 (distributional plurality, top-3 nearest anchors) | 7/21 | 33.3% | 20.0% | +13.3% |
| L2 (strict-top-1 anchor distance) | 7/21 | 33.3% | 20.0% | +13.3% |
| L3 (substrate-consistency under Eteocretan LM) | 2/21 | 9.5% | 5.0% | +4.5% |
| **L1+L2+L3 consensus (framework class)** | **7/21** | **33.3%** | **20.0%** | **+13.3%** |

Per-line cross-script comparison reads directly: positive deltas mean the line recovers more accurately on LA than on CHIC (i.e. LA's larger and more distributionally-rich corpus lets the line carry more signal); negative deltas mean the line does worse on LA. The bottom row's delta is the headline LA-vs-CHIC framework-validation comparison; if it is positive and large, the chic-v5 framework is structurally portable but CHIC-corpus-limited; if it is small or negative, the at-chance behaviour observed on chic-v9 is structural to the framework rather than CHIC-specific.

## Tier-classification accuracy

The chic-v5 framework's tier-2 criterion requires 3-of-3 unanimity on the top class (with L4 silent for all chic-v5 unknowns by construction). The LOO equivalent — 3-of-3 unanimity on L1+L2+L3 — is the same operational criterion. How accurately does the framework correctly tier-2-classify anchors as their known class, on the LA side?

| metric | value |
|---|---:|
| n LOO tier-2 (3-of-3 unanimous) | 3 |
| n LOO tier-2 with framework_class == known_class | 0 |
| **tier-2 classification accuracy (n_correct / n_tier_2)** | **0.0%** |
| chic-v9 tier-2 classification accuracy | 0/3 = 0.0% |
| **tier-2-or-3 with framework_class == known_class (≥2 of 3 voting lines agreeing on the known class)** | **6/21 = 28.6%** |

The tier-2 row tells us whether the chic-v5 tier-2 criterion (3-of-3 unanimity) is reliable when applied to known cases on the LA side. The tier-2-or-3 row is the looser test (at least 2 of 3 lines agreeing on the *known* class), which captures cases where L1+L2+L3 detect a partial signal but one line dissents.

## Implication for the chic-v5 / v22 / v26 framework's per-sign credibility

The LA-side aggregate LOO accuracy of 33.3% is **below 40%**, placing the framework's L1+L2+L3 recovery in the **low-agreement / not-validated** band on the Linear A side. The chance baseline for a 6-class taxonomy is ~16.7%, so this is modestly above chance, far below what would be expected if the framework reliably recovered known phoneme values when run blind.

Combined with chic-v9's 20.0% on the CHIC side, the methodology paper's reading becomes: **the at-chance behaviour is structural to the chic-v5 framework, not CHIC-specific**. The framework detects substrate-LM-phonotactic kinship at the **population level** (the v10/v18/v21 PASSes on Linear A; the chic-v3 right-tail bayesian gate PASS for Eteocretan against CHIC at p=7.33e-04) but **per-sign value extraction is below the noise floor on both scripts** under our held-out validation. The implication for the broader chic-v5 / v22 / v26 / leader-board top-K framework is a **substantial downgrade across both scripts**:

- **The chic-v5 tier-2 candidates' credibility downgrade (per chic-v9 / chic-v10) extends to the v22 + v26 leaderboard top-K mechanical-verification results' per-sign-value claims.** The leaderboard top-K substrates were detected by the same population-level kinship machinery whose per-sign extraction is at chance; v26's tier-1 → tier-2 mechanical lift on Linear A and chic-v6's analogous +3-inscription / +20-hit lift on CHIC are **mechanical findings about the framework's sign-coverage ladder**, not independent evidence for the per-sign phoneme-class assignments.
- **The population-level cross-script claim survives intact.** chic-v3 / chic-v4's right-tail bayesian gate PASS and Spearman ρ=+1.000 cross-script ranking are population-level signals that do not depend on the per-sign machinery; the v28 LA-side null does not move those numbers.
- **v28 closes the methodology paper's CHIC/LA asymmetry on held-out validation.** v26 (mg-c202) closed the asymmetry on mechanical-verification (LA top-K vs chic-v6 tier-2 lift) by adding a §4.6 paragraph parallel to §4.7's chic-v6 paragraph; v28 closes the analogous asymmetry on per-sign-recovery validation by adding a §4.6 paragraph parallel to §4.7's chic-v9 paragraph.

## Caveats

- **L4 exclusion is non-negotiable methodologically.** The LB-carryover anchor pool's known values are themselves derived via paleographic similarity to deciphered Linear B signs; including L4 would inflate accuracy by construction. The L1+L2+L3-only LOO is the honest test.
- **Class-level resolution.** The agreement predicate is exact phoneme-class identity (vowel / stop / nasal / liquid / fricative / glide). The framework's per-sign resolution is class-level, so this is the correct evaluation granularity. The LOO test does not adjudicate whether the framework could correctly recover the **specific phoneme value** within the class.
- **L3 candidate-pool reduction.** Where the held-out value is the only representative of its class in the rebuilt pool, L3 cannot recover the class by construction. The 2 cases where the held-out class has no other representative in the candidate pool are flagged with ⚠ in the per-anchor table; for these anchors L3 cannot recover the class by construction.
- **N = 21 anchors.** The sample is comparable in size to chic-v9's 20 CHIC anchors; ±5% differences fall within the binomial noise floor. The headline accuracy should be read as a point estimate with substantial uncertainty.
- **Anchor-pool composition bias.** The LB-carryover anchors are paleographically-derived AB signs, not a random sample of Linear A syllabograms; the LOO test measures recovery accuracy on this specific population, which may differ systematically from the broader 56 non-anchored AB signs the framework would be applied to in a hypothetical chic-v5-on-LA per-sign extraction run.
- **LM symmetry.** The v21 Eteocretan LM is used in direct symmetry with chic-v9. The alternative — per-pool LM swap — would couple the L3 score to candidate-substrate identity, which is methodologically odd for an LB-carryover anchor pool that is not naturally partitioned across the v10/v18/v21 substrate pools.

## Determinism

- No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-keyed permutation construction (deterministic, no `random.Random(seed)` draw).
- Same inputs → byte-identical output. Re-running this script overwrites the result file with identical content.

## Citations

- Younger, J. G. (2020). *Linear A texts in phonetic transcription* (online edition).
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
- Schoep, I. (2002). *The Administration of Neopalatial Crete.* Liège.

## Build provenance

- Generated by `scripts/build_linear_a_v28.py` (mg-4a7b).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs: `corpus/all.jsonl` (LA corpus, 772 inscriptions); `pools/linear_b_carryover.yaml` (21 LB-carryover anchors via citation-string extraction); `pools/eteocretan.yaml` (Eteocretan phoneme inventory for the L3 candidate-pool filter); `harness/external_phoneme_models/eteocretan.json` (v21 LM artifact).
- Cross-script comparison numbers (chic-v9 / mg-18cb): aggregate 20.0%; per-line L1=20.0% L2=20.0% L3=5.0%; tier-2 unanimity 0/3 = 0.0%.
