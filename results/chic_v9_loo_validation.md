# CHIC chic-v5 framework leave-one-out validation against chic-v2 anchors (chic-v9; mg-18cb)

## Method

For each of the 20 chic-v2 paleographic anchors S with a known scholarly Linear-B carryover value V, S is removed from the chic-v2 anchor pool (yielding a reduced 19-anchor pool), then S is treated as unknown by the chic-v5 framework and the three non-circular lines of evidence (L1 distributional plurality, L2 strict-top-1 anchor distance, L3 substrate-consistency under the v21 Eteocretan LM) are recomputed against the reduced pool. The framework's proposed phoneme class is then compared to V's known class.

L4 (cross-script paleographic) is **deliberately excluded** from this LOO test: chic-v1's PALEOGRAPHIC_CANDIDATES list is the source of the chic-v2 anchor pool, so for any anchor S the L4 line trivially recovers V by construction. Including L4 would make the test circular and inflate accuracy. With L4 excluded the framework's tier classification reduces from the chic-v5 4-line scheme to a 3-line scheme:

- **tier-2** — 3-of-3 unanimity on the top class.
- **tier-3** — 2-of-3 agreement.
- **tier-4** — 1-of-3 (single line of evidence).
- **untiered** — 0 voting lines (no fingerprint signal).

The candidate-value pool for L3 is rebuilt from the reduced 19-anchor pool's distinct Linear-B carryover values plus bare vowels a/e/i/o/u, filtered to values whose first character is in the Eteocretan phoneme inventory (chic-v5 convention). For 18 of 20 LOO runs this strict-LOO rebuild removes the held-out value entirely; L3 can therefore still recover the *class* (if another candidate in the pool shares it) but cannot recover the *value*. The class is the framework's per-sign resolution unit, so this is the relevant LOO target. Where the held-out class has no other representative in the candidate pool, L3 cannot recover the class either; this is a structural property of the LOO setup and is flagged in the per-anchor table.

## Aggregate accuracy

Of the 20 chic-v2 anchors run blind under L1+L2+L3, the framework's proposed class agrees with the known class on **4/20 (20.0%)**. This is the headline LOO validation number.

| metric | value |
|---|---:|
| n anchors run blind | 20 |
| n with framework_class == known_class | 4 |
| **aggregate LOO accuracy** | **20.0%** |
| n LOO tier-2 (3-of-3 unanimity) | 3 |
| n LOO tier-3 (2-of-3) | 14 |
| n LOO tier-4 (1-of-3) | 3 |
| n LOO untiered (0 votes) | 0 |

Validation regime: **not validated** — at the chic-v9 brief's thresholds (>70% high; 40-70% moderate; <40% low), the framework's L1+L2+L3 recovery accuracy of 20.0% places this LOO test in the **low-agreement** band.

## Per-anchor LOO results

Each row below is one LOO run: the named anchor was removed from the chic-v2 pool and treated as unknown; the three lines voted on its class against the reduced 19-anchor pool. Tier here is the L1+L2+L3-only tier (3-of-3 = tier-2, 2-of-3 = tier-3, etc.). The agreement column is whether the framework's proposed class matches the known class.

| anchor | freq | known phoneme | known class | framework class | tier | agreement | L1 | L2 | L3 |
|---|---:|---|---|---|:---:|:---:|:---:|:---:|:---:|
| `#010` | 50 | `ja` | glide | liquid | tier-3 | ✗ | liquid | liquid | nasal |
| `#013` | 26 | `pa` | stop | stop | tier-3 | ✓ | stop | stop | glide |
| `#016` | 20 | `a` | vowel | glide | tier-3 | ✗ | stop | glide | glide |
| `#019` | 50 | `ke` | stop | liquid | tier-3 | ✗ | liquid | liquid | nasal |
| `#025` | 11 | `ta` | stop | nasal | tier-4 | ✗ | stop | vowel | nasal |
| `#028` | 22 | `ti` | stop | glide | tier-4 | ✗ | glide | stop | nasal |
| `#031` | 65 | `ro` | liquid | stop | tier-2 | ✗ | stop | stop | stop |
| `#038` | 75 | `i` | vowel | stop | tier-3 | ✗ | stop | stop | glide |
| `#041` | 20 | `ni` | nasal | stop | tier-3 | ✗ | stop | liquid | stop |
| `#042` | 57 | `wa` | glide | stop | tier-2 | ✗ | stop | stop | stop ⚠ |
| `#044` | 128 | `ki` | stop | stop | tier-3 | ✓ | stop | stop | glide |
| `#049` | 119 | `de` | stop | stop | tier-3 | ✓ | stop | stop | glide |
| `#053` | 14 | `me` | nasal | glide | tier-2 | ✗ | glide | glide | glide |
| `#054` | 22 | `mu` | nasal | glide | tier-3 | ✗ | glide | stop | glide |
| `#057` | 35 | `je` | glide | glide | tier-4 | ✓ | nasal | stop | glide |
| `#061` | 39 | `te` | stop | liquid | tier-3 | ✗ | liquid | liquid | glide |
| `#070` | 56 | `ra` | liquid | stop | tier-3 | ✗ | stop | stop | nasal |
| `#073` | 5 | `to` | stop | liquid | tier-3 | ✗ | liquid | liquid | nasal |
| `#077` | 13 | `ma` | nasal | glide | tier-3 | ✗ | glide | stop | glide |
| `#092` | 37 | `ke` | stop | glide | tier-3 | ✗ | glide | liquid | glide |

⚠ marker on L3 indicates that the held-out anchor's class had no other representative in the rebuilt 19-anchor candidate-value pool, so L3 was structurally unable to recover that class. Total such cases: 1/20.

## Per-line accuracy decomposition

How accurately does each line, run in isolation, recover the known class on the LOO test? This decomposition diagnoses which lines carry the signal and which are noise.

| line | n_correct/n_total | accuracy |
|---|:---:|---:|
| L1 (distributional plurality, top-3 nearest anchors) | 4/20 | 20.0% |
| L2 (strict-top-1 anchor distance) | 4/20 | 20.0% |
| L3 (substrate-consistency under Eteocretan LM) | 1/20 | 5.0% |
| **L1+L2+L3 consensus (framework class)** | **4/20** | **20.0%** |

L3's known systematic class bias under the Eteocretan LM (chic-v5 finding: L3 favours nasal/glide due to the Eteocretan vocabulary's onset distribution) carries through to this LOO test. Per-line accuracies of L1=20.0%, L2=20.0%, L3=5.0% read directly: if L1 and L2 substantially exceed L3, then the distributional fingerprint machinery is the load-bearing part of the framework, and L3 functions as a noisy tiebreaker rather than as independent confirmatory evidence. The consensus accuracy (20.0%) reads against this backdrop.

## Tier-classification accuracy

The chic-v5 framework's tier-2 criterion requires 3-of-3 unanimity on the top class (with L4 silent for all chic-v5 unknowns by construction). The LOO equivalent — 3-of-3 unanimity on L1+L2+L3 — is the same operational criterion. How accurately does the framework correctly tier-2-classify anchors as their known class?

| metric | value |
|---|---:|
| n LOO tier-2 (3-of-3 unanimous) | 3 |
| n LOO tier-2 with framework_class == known_class | 0 |
| **tier-2 classification accuracy (n_correct / n_tier_2)** | **0.0%** |
| **tier-2-or-3 with framework_class == known_class (≥2 of 3 voting lines agreeing on the known class)** | **3/20 = 15.0%** |

The tier-2 row tells us whether the chic-v5 tier-2 criterion (3-of-3 unanimity) is reliable when applied to known cases: of the anchors that the framework would call tier-2 under L1+L2+L3, what fraction match the scholarly value's class? The tier-2-or-3 row is the looser test (at least 2 of 3 lines agreeing on the *known* class), which captures cases where L1+L2+L3 detect a signal but one line dissents.

## Implication for chic-v5 tier-2 candidates

The aggregate LOO accuracy is **below 40%**, placing the framework's L1+L2+L3 recovery in the **low-agreement band** the chic-v9 brief pre-registered. The framework recovers the known class on only 4 of 20 anchors (20.0%); for a 6-class taxonomy the chance baseline is ~16.7%, so this is close to chance, far below what would be expected if the framework reliably recovered known phoneme values when run blind.

**Implication for the chic-v5 tier-2 candidates (`#001 → wa`/glide, `#012 → wa`/glide, `#032 → ki`/stop):** these three new proposals **lose substantial credibility under this LOO test**. The same framework that proposed them recovers known anchor classes at only 20.0% accuracy when run blind; the methodology paper's framing must downgrade the three candidates from 'mechanical proposals deserving specialist review' to 'candidate proposals contingent on the framework's currently-low validation accuracy'. The chic-v9 LOO test is what would have caught a mis-specified framework before publication; honest reporting on the negative result is the discipline-protecting outcome the chic-v0..v8 sub-program has consistently emphasised (cf. chic-v1's missed-update incident mg-c7e3 backfilled by mg-0ea1).

## Caveats

- **L4 exclusion is non-negotiable methodologically.** Including L4 would inflate accuracy by construction; the L1+L2+L3-only LOO is the honest test.
- **Class-level resolution.** The agreement predicate is exact phoneme-class identity (vowel / stop / nasal / liquid / fricative / glide). The framework's per-sign resolution is class-level, so this is the correct evaluation granularity. The LOO test does not adjudicate whether the framework could correctly recover the **specific phoneme value** (`ja` vs `je` vs `wa` within glide; `pa` vs `ta` vs `ka` within stop) — at the LOO test level the framework's verdict is class-level only.
- **L3 candidate-pool reduction.** For 18 of 20 LOO runs the held-out anchor's value is removed from the rebuilt candidate-value pool, so L3 can no longer score the held-out value directly. The class is still recoverable if another candidate in the pool shares it. The 1 cases where the held-out class has no other representative in the candidate pool are flagged with ⚠ in the per-anchor table; for these anchors L3 cannot recover the class by construction.
- **Small N (20 anchors).** A 20-anchor LOO test produces limited statistical resolution. Differences of ±5% between lines or between this LOO test and a hypothetical larger LOO test on an expanded anchor pool fall within the binomial noise floor for this sample size. The headline accuracy should be read as a point estimate with substantial uncertainty, not as a precise calibration figure.
- **Anchor-pool composition bias.** The chic-v2 anchor pool is itself a curated set (the chic-v1 paleographic-candidate list); the LOO test measures recovery accuracy on this specific population, which may differ systematically from the 76 unknown signs the framework targets. The relevant comparison is the methodology's recovery on **anchor-shaped** signs, which is what this test reports.

## Determinism

- No RNG. The L3 control-phoneme selection inherits chic-v5's sha256-keyed permutation construction (deterministic, no `random.Random(seed)` draw).
- Same inputs → byte-identical output. Re-running this script overwrites the result file with identical content.

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.

## Build provenance

- Generated by `scripts/build_chic_v9.py` (mg-18cb).
- fetched_at: 2026-05-05T22:00:00Z
- Inputs: `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); `corpora/cretan_hieroglyphic/syllabographic.jsonl` (chic-v3); `pools/cretan_hieroglyphic_signs.yaml` (chic-v1); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); `pools/eteocretan.yaml`; `harness/external_phoneme_models/eteocretan.json` (v21).
