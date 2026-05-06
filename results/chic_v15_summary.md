# chic-v15 within-window context inspection summary (mg-2904)

## Headline counts

| metric | value |
|:--|---:|
| `n_input` (chic-v12 tier-3-uncorroborated candidates) | 17 |
| `n_consistent` | **12** |
| `n_inconsistent` | **0** |
| `n_inconclusive` (within-window) | **3** |
| `n_inconclusive_on_corpus_quality` (non-viable) | **2** |
| **pass rate** (consistent / n_input) | **12/17 = 70.6%** |
| chic-v13 reference pass rate | 6/8 = 75.0% |

## Triage breakdown

| viability band | candidates | n |
|:--|:--|---:|
| viable (n_clean ≥ 3 + clean anchor adjacency) | `#007`, `#008`, `#009`, `#011`, `#020`, `#040`, `#059`, `#069` | 8 |
| marginal (n_clean ∈ {1, 2}) | `#027`, `#037`, `#043`, `#045`, `#058`, `#060`, `#066` | 7 |
| non-viable (n_clean = 0) | `#002`, `#078` | 2 |

## Per-candidate one-line verdict

| sign | freq | proposed class | viability | verdict | strongest cited inscription |
|:--|---:|:--|:--|:--|:--|
| `#002` | 7 | liquid | non-viable | **inconclusive on corpus quality** | 0 clean inscriptions (3 partial + 3 fragmentary) |
| `#007` | 8 | vowel | viable | **inconclusive** | CHIC #296 / #308 / #090 — V-V hiatus at #090 (`a-i-V-?`) phonotactically awkward; no formula-grade positive evidence |
| `#008` | 7 | glide | viable | **consistent** | CHIC #297 (clean Crete-unprov. seal: `i-[G:#008]` opening parallel to `i-ja-ro`; co-attested `ki-de` + `ki-stop:#005`) |
| `#009` | 10 | stop | viable | **consistent** | CHIC #003 (clean Knossos nodulus: `[stop:#009]-ma-pa-[V]` 4-sign with strong anchor bracketing) + CHIC #018 (clean crescent with `ki-stop:#005`) |
| `#011` | 24 | liquid | viable | **consistent** | CHIC #297 + #042 (clean Knossos medallion: `[L:#011]` co-attested with `ki-de NUM:634` accountancy formula) |
| `#020` | 9 | vowel | viable | **inconclusive** | CHIC #003 / #018 / #082 — V-V hiatus at #082 (`[V]-a-ni`) phonotactically awkward; no formula-grade positive evidence |
| `#027` | 3 | glide | marginal | **inconclusive** | only 1 clean (CHIC #073, 3-sign `[G]-[?]-ra`); accountancy fragment at fragmentary #049 suggestive but not formula-grade |
| `#037` | 3 | liquid | marginal | **consistent** | recurring `037-011-029 NUM` accountancy formula across CHIC #042 (clean) + #057 (partial, permuted) + #061 (fragmentary) |
| `#040` | 17 | stop | viable | **consistent** | CHIC #129 (clean Mallia nodulus: `wa-[stop:#040]-de NUM:0` accountancy formula) + CHIC #298 (clean: all 3 canonical sealstone formulas) + CHIC #309 (clean Pyrgos seal) |
| `#043` | 6 | liquid | marginal | **consistent** | CHIC #256 (clean Crete-unprov. seal: `i-[L:#043]-de NUM:0` accountancy formula) + CHIC #042 (clean medallion with `ki-de NUM:634`) |
| `#045` | 4 | stop | marginal | **consistent** | CHIC #298 (clean: 5-sign `ra-te-ke-[stop:#045]-ra` with 4-of-5 anchor bracketing within all-3-canonical-formula sealstone) |
| `#058` | 5 | stop | marginal | **consistent** | CHIC #283 (clean Crete-unprov. seal: `[stop:#056]-pa-[stop:#058]` co-attested with `ki-stop:#005` + `ki-de`) + CHIC #123 (clean `ke-[stop:#058]`) |
| `#059` | 5 | glide | viable | **consistent** | CHIC #242 (clean Crete-unprov. seal: `[stop:#056]-[G:#059]` opening + canonical `i-ja-ro` formula on line 2) + CHIC #004 + CHIC #017 |
| `#060` | 8 | stop | marginal | **consistent** | CHIC #074 (clean Mallia medallion: `wa-ra-[stop:#060]-ki` 4-sign with 3-of-4 anchor bracketing) |
| `#066` | 3 | stop | marginal | **consistent** | CHIC #305 (clean Lastros seal: `wa-[stop:#066]-a-?` opening within multi-formula sealstone with `ki-de` + `ki-stop:#005`) |
| `#069` | 3 | stop | viable | **consistent** | CHIC #038 (clean Knossos medallion: `je-[stop:#069]-ra NUM:110` accountancy formula) + CHIC #287 (clean: both `ki-de` + `ki-stop:#005`) + CHIC #041 (clean accountancy) |
| `#078` | 3 | stop | non-viable | **inconclusive on corpus quality** | 0 clean inscriptions (1 partial + 1 fragmentary) |

## Direct comparison to chic-v13

| metric | chic-v13 (tier-2-equivalent) | chic-v15 (tier-3-uncorroborated) |
|:--|---:|---:|
| n_input | 8 | 17 |
| n_consistent | 6 | 12 |
| n_inconsistent | 0 | 0 |
| n_inconclusive (any reason) | 2 | 5 |
| **pass rate** | **6/8 = 75.0%** | **12/17 = 70.6%** |

The pass rates are within 4.4pp of each other. chic-v15's pass rate clears the ≥70% threshold the chic-v15 brief pre-registered for the **"Cross-pool L3 has no independent discriminative value"** verdict.

## Plain-English verdict on the discriminative test

**Cross-pool L3 has no independent discriminative value.** Within-window context inspection passes at statistically and methodologically comparable rates regardless of whether cross-pool L3 corroborates the chic-v5 proposed class: 75.0% on the chic-v12 tier-2-equivalent set (chic-v13) vs 70.6% on the chic-v12 tier-3-uncorroborated set (chic-v15). The 4.4pp gap is well within the noise of a small-sample inspection on a corpus of 302 inscriptions, and the qualitative structure of the consistent verdicts is indistinguishable across the two sets — both are dominated by `[CV]-[stop]-[CV] NUM` accountancy formulas (chic-v13: `#072 → stop`, `#017 → nasal`, `#039 → stop`, `#056 → stop`; chic-v15: `#040 → stop`, `#069 → stop`, `#037 → liquid`, `#043 → liquid`) and multi-formula sealstone co-occurrence (chic-v13: `#005 → stop`, `#021 → nasal`; chic-v15: `#040 → stop`, `#011 → liquid`, `#069 → stop`, `#066 → stop`, `#058 → stop`). The 7 paired-evidence candidates count from v30 is methodologically *narrowed* but not arithmetically lifted — chic-v15's 12 `consistent` candidates lack cross-pool L3 corroboration by definition, so they count as candidates with **context-inspection-only evidence**, distinct from the 7 paired-evidence candidates. The total context-inspection-consistent count across the chic sub-program is **12 (chic-v15) + 6 (chic-v13) + 1 (chic-v11 `#032`) = 19** candidates: 7 with paired cross-pool L3 + within-window context evidence; 12 with within-window context evidence only. This finding **reinforces chic-v14's anti-evidentiary verdict on cross-pool L3** with an orthogonal observation: the discriminative *failure* of cross-pool L3 within the tier-3 set is also confirmed at the per-candidate within-window-context level. The chic-v9 framework-level negative (LOO accuracy 20.0% / 0/3 tier-2 unanimity correct) remains load-bearing across all 19 context-inspection-consistent candidates; chic-v15 contributes no lift to the framework's external validation accuracy. Specialist review remains the load-bearing next step for any candidate; promotion of `consistent` candidates to "candidate proposal pending domain-expert review" prose status remains a PM call, separate from chic-v15's deliverable.

## Bail rule status

The chic-v15 brief pre-registered a bail rule: if the polecat hits ≥80% of the 1.2M token budget while having processed fewer than 17 candidates, bail with the first k completed and surface the budget-pressure signal. **All 17 candidates were processed within budget (15 inspected + 2 reported as `inconclusive on corpus quality` after triage); no bail invoked.**

## Build provenance

- Generated by manual inspection following the chic-v13 `results/chic_v13_context_inspection.md` template (mg-2904).
- fetched_at: 2026-05-06T00:00:00Z
- Inputs:
  - `corpora/cretan_hieroglyphic/all.jsonl` (chic-v0)
  - `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2)
  - `results/chic_v12_cross_pool_l3.md` (chic-v12; the 17 tier-3-uncorroborated candidate list)
  - `results/chic_v13_context_inspection.md` (chic-v13; methodological template + reference 6/8 pass rate)
- Companion document: `results/chic_v15_context_inspection.md` (full per-candidate inspection report).

## Citations

- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum Inscriptionum Cretae* (Études Crétoises 31). Paris.
- Younger, J. G. (online). *The Cretan Hieroglyphic Texts: a web edition of CHIC with commentary.* Wayback Machine snapshot 20220703170656.
- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.
- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean Greek.* Cambridge.
