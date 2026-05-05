# Lineara — findings summary (mg-7ecb, harness v15)

A publication-shape consolidation of what the Lineara project has
mechanically established about Linear-A so far. This is the v0
"manuscript narrative" Daniel asked for in mg-4664, with a major v13
update from mg-c216 sharpening what the v10 PASSes do and do not
support, a v14 update from mg-6b73 establishing curation-tolerance
under same-distribution pollution, and a **v15 update from mg-7ecb
sharpening the manuscript-shape claim against cross-language pollution.**
A reader who has not followed the merge notes should be able to pick
up from here.

The companion log `docs/findings.md` carries the per-ticket history;
this document carries the consolidated picture and the supportable /
unsupportable claim split.

## v15 update — what changed (mg-7ecb, 2026-05-05)

The v15 ticket built the **cross-language pollution test** that v14's
result motivated: a Greek-shape polluted Aquitanian pool (153 real
Aquitanian roots + 153 synthetic conjecturals drawn from the Mycenaean-
Greek char-bigram distribution at
`harness/external_phoneme_models/mycenaean_greek.json`, with lengths
matched to the real pool) plus matched phonotactic controls, all run
through the v10 right-tail bayesian gate under the Basque LM (the
substrate's own LM, same as v10/v14). The pre-registered binary
question was: **does the framework PASS for ANY phonotactic match,
or only when the polluting distribution matches the substrate's own?**

**Verdict: partial-discrimination — gate PASSes at p = 2.01e-03, but
within the right tail real Aquitanian dominates Greek-shape
conjecturals at p = 8.29e-05.** This is the "neutral-ish" outcome the
v15 brief flagged as the most interesting case for the manuscript.

The headline gate clears for any pool with non-trivial char-bigram
overlap with the LM, but the cross-language gate is ~70× weaker than
v14's same-distribution gate (p = 2.74e-05) and ~16× weaker than v10's
clean gate (p = 3.22e-05). The framework therefore has measurable
shape selectivity, but not enough to flip the headline gate to FAIL.
The provenance breakdown of the polluted-pool top-20 is **13 of 20 real
(65%) / 7 of 20 conjectural-greek (35%)**, vs v14's near-50/50 split,
and the within-tail real-vs-conjectural-greek MW U is **p = 8.29e-05**
(vs v14's p = 0.98). Real Aquitanian surfaces' posteriors actually
**shifted UP** by +5.8% median when Greek-shape conjecturals were
mixed in, because Greek-shape conjecturals don't compete as well as
same-Aquitanian-shape conjecturals do for the same Linear-A windows.

**What this means for v14's manuscript-shape claim.** v14's claim was:

> The framework detects substrate-LM-phonotactic kinship at the
> population level for any pool whose phoneme + length distribution
> is drawn from the substrate's own marginal distribution. It does
> NOT detect "real substrate vocabulary," and does NOT support
> per-sign reading claims.

v15 **refines** this claim. Both halves survive, but the boundary is
sharper than v14 alone could reveal:

* The headline-PASS condition is *broader* than v14's clause says —
  the gate clears for pools whose phoneme distribution does not match
  the substrate's own, as long as char-bigram overlap with the LM is
  non-trivial. Greek-shape conjecturals carry enough Mediterranean-
  style CV phonotactics to out-score scramble controls under the
  Basque LM.
* But within-tail discrimination is real and large: real Aquitanian
  dominates Greek-shape conjecturals at p < 0.001 within the right
  tail, even when both are mixed in the same pool. The framework is
  *partially* selective to substrate-distribution shape — enough to
  push Greek-shape conjecturals down the substrate-side leaderboard,
  but not enough to break the population gate.

The v14 within-tail real-vs-conjectural MW p of 0.98 (no
discrimination) → v15 within-tail real-vs-conjectural-greek MW p of
8.3e-05 (strong discrimination) is the cleanest diagnostic. The
distinguishing axis is whether the polluting distribution matches
the substrate's own: when it does (v14), conjecturals are
indistinguishable from real; when it doesn't (v15), they are
distinguishable.

**Implications for the rest of this document.** The supportable-
claims section gains: "the framework's substrate-side leaderboard
within-tail-discriminates substrate-shape from non-substrate-shape
when both are mixed in the same pool; this discrimination is below
the population gate's resolution, but above the leaderboard's." The
unsupportable-claims section is unchanged in spirit but tightens its
language: the right-tail leaderboard does not distinguish real from
*same-distribution* conjectural surfaces (v14), but does distinguish
real from *cross-language* conjectural surfaces (v15) — so the
"Aquitanian-shaped surfaces the LM rewards consistently" framing
remains right, but it's specifically Aquitanian-shaped, not just
phonotactically-plausible-under-Basque. The remaining-work section
gains v16 (methodology paper draft) as the natural next ticket and
removes "cross-language pollution" (now done).

## v14 update — what changed (mg-6b73, 2026-05-05)

The v14 ticket built the **held-out pool-curation test** that the
v13 coherence verdict pre-registered: a polluted Aquitanian pool
(153 real Aquitanian roots + 153 phonotactically-matched but
synthetic conjecturals, with provenance tags) plus matched
phonotactic controls, all run through the v10 right-tail bayesian
gate. The pre-registered binary question was: **does the framework
PASS on a 50%-polluted pool?**

**Verdict: PASS at p = 2.74e-05.** That is essentially identical
to the clean Aquitanian PASS at p = 3.22e-05 (within ~1.2× of
each other). The framework's gate is **tolerant** of heavy
conjectural pollution — it does not depend on every pool entry
being a real substrate root.

The provenance breakdown of the polluted-pool top-20 surfaces is
**9 of 20 real (45%) / 11 of 20 conjectural (55%)** — almost
exactly the 50/50 split of the underlying pool. A real-vs-
conjectural one-tail Mann-Whitney U gave p = 0.98: the framework
**cannot distinguish real from conjectural surfaces** in the
right tail of a mixed pool. Its discriminator is *phonotactic
shape*, not substrate-vocabulary identity.

**What this means for the v12+v13 readings.** Reading #1
(substrate-LM-phonotactic kinship at the surface aggregate) is
*supported*. Reading #2 (curation-sensitivity — the framework
PASSes only when the substrate pool is uniformly clean) is
*undermined as a wholesale account*. The v10 PASSes do not depend
on every entry being valid; they reflect the framework's response
to phonotactic-shape match between the substrate and the LM.

The Linear-B positive-control failure (mg-4664) therefore needs
a different explanation than curation-sensitivity. The remaining
candidates: small N (12 anchors), short anchor surfaces, or a
Linear-B-specific structural issue. Not pursued in v14.

**Implications for the rest of this document.** The supportable-
claims section gains: "the framework's PASS is curation-tolerant
within the same phoneme + length distribution; the gate signal is
not contingent on uniformly-clean substrate pools." The
unsupportable-claims section gains: "the right-tail leaderboard
does not distinguish real from conjectural surfaces — even within
a mixed pool — so the surfaces in the v10 top-K are not validated
as substrate vocabulary by the gate, only as phonotactically-
plausible Aquitanian-shaped surfaces." The remaining-work section
removes "held-out pool-curation test" (now done) and notes that
v15 follow-ups (varied pollution levels, cross-language
pollution) are optional rather than load-bearing.

## v13 update — what changed (mg-c216, 2026-05-05)

The v13 ticket built the **consensus sign-to-phoneme map** + a
**cross-window coherence test** to distinguish two coupled readings of
the v12 result: (1) the v10 PASSes are real substrate signal and the
gate is just over-conservative on mixed-cleanness pools, vs (2) the
v10 PASSes hold *only because* the substrate pools happened to be
uniformly clean and the framework cannot tolerate heterogeneous
curation. The verdict is unambiguous: median per-surface coherence is
**0.1818 for Aquitanian and 0.1808 for Etruscan** against a 0.6
acceptance bar. **Both pools fail decisively. Reading #2 is
supported.** The v10 PASSes are coherent at the surface-aggregate
level but the underlying sign-to-phoneme mappings are not stable
across windows — high-frequency Linear A signs receive proposals
scattered across the entire phoneme alphabet (max-likelihood entropy
3.6–4.0 bits out of log2(23) ≈ 4.5 bits maximum). The framework
recovers a real signal at the substrate-phonotactic-kinship level,
but **does not establish per-sign readings**.

A bundled refined-gate sensitivity check on the Linear-B positive
control sweeps K ∈ {5, 10, 20}: K=5 cleanly clears p<0.05 (p=0.011),
K=10 is borderline (p=0.060), K=20 (production) fails (p=0.155). So
the K=20 gate is somewhat over-conservative on mixed-cleanness pools,
but adopting a smaller K does not change the v13 verdict — the
deeper coherence failure is the load-bearing finding.

**Implications for the rest of this document.** The supportable claims
section below is unchanged at the surface-aggregate level; the
unsupportable claims section gains "no per-sign sign-to-phoneme map
is validated" as a now-empirically-confirmed (rather than
conservatively-stated) finding. The downstream-work section drops
per-inscription gloss generation (originally v14) and replaces it
with the held-out pool-curation test that addresses reading #2
structurally.

## Question

Linear-A is undeciphered, and no single hypothesis is realistic on
its own. What's tractable is mechanical, falsifiable testing of
substrate-language hypotheses against the Linear-A corpus, scored
under a fixed metric and gated against phonotactically-matched
controls. The project asks: which substrate hypotheses survive
mechanical right-tail testing, and which inscriptions concentrate
that signal?

## Method

The pipeline (built up across mg-1c8c through mg-4664) is:

1. **Corpus.** `corpus/` holds 761 Linear-A inscription records
   ingested from SigLA (CC BY-NC-SA 4.0), normalized to a
   per-inscription JSON schema with sign tokens, position, and
   metadata. `corpus_status.md` documents what's in and what's out.
2. **Substrate pools.** `pools/<name>.yaml` lists candidate root
   surfaces with phoneme decompositions, attestations, and citations.
   Three substrate pools: `aquitanian` (Vasconic / pre-IE roots from
   Trask 1997, Gorrochategui 1984), `etruscan` (Bonfante &
   Bonfante 2002 + TLE), `toponym` (pre-Greek Aegean toponyms from
   Beekes 2010). A fourth pool, `linear_b_carryover` (mg-4664), holds
   20 Ventris-Chadwick 1956 carryover values as a positive control.
3. **Matched controls.** For each substrate pool, a `control_<name>`
   pool is generated by sampling random surfaces of matching length
   distribution from the substrate's marginal phoneme histogram.
   Deterministic seed; mg-f419 + mg-c2af.
4. **Hypothesis generation.** `scripts/generate_candidates.py` walks
   each pool entry against every Linear-A inscription window of
   matching length, emitting one `candidate_equation.v1` hypothesis
   per (pool entry × inscription × window) triple. mg-bef2 added a
   `candidate_signature.v1` shape that pins multiple roots to
   non-overlapping sub-windows of one inscription window.
5. **Scoring.** `scripts/run_sweep.py` scores each hypothesis under
   the `external_phoneme_perplexity_v0` metric (mg-ee18), which
   feeds the candidate's phoneme stream through a held-out
   char-bigram language model trained on actual substrate text and
   reads off the per-record log-likelihood. Substrate pools dispatch
   to their own LM (`aquitanian → basque`, `etruscan → etruscan`,
   `linear_b_carryover → mycenaean_greek`); each control pool
   shares its substrate's LM so the paired-diff cancels the LM
   choice out of the comparison.
6. **Aggregation.** `scripts/per_surface_bayesian_rollup.py`
   (mg-d26d) computes a per-surface Beta-binomial posterior over the
   sign of `paired_diff = substrate_score − control_score`. Each
   paired_diff record contributes one binary observation; the
   posterior is Beta(1+k, 1+n−k) under a Beta(1, 1) prior.
7. **Acceptance gate.** Right-tail comparison: one-tail Mann-Whitney
   U on the top-20 substrate posterior means vs the top-20 control
   posterior means. p < 0.05 with substrate > control passes.
   Cross-LM negative controls (mg-0f97) and a third-LM check
   (mg-4664) test substrate-LM specificity by re-routing the same
   data through other natural-language LMs.

The pipeline is deterministic end-to-end. Re-running the gate against
the same `experiments.external_phoneme_perplexity_v0.jsonl` and the
same pool / manifest files produces byte-identical posterior
leaderboards.

## Validation status by pool

The framework was designed to be falsifiable. Three substrate pools
plus one positive-control pool have been evaluated under same-LM,
cross-LM, and third-LM gates. Outcomes:

| pool                       | own-LM gate (v10/mg-d26d) | cross-LM gate (v11/mg-0f97)        | third-LM gate (v12/mg-4664, Mycenaean-Greek) | pool-curation gate (v14/mg-6b73 + v15/mg-7ecb)                              | status                                                                                  |
|----------------------------|:--------------------------:|:----------------------------------:|:--------------------------------------------:|:----------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------|
| aquitanian                 | PASS p=3.22e-05 (basque)   | PASS p=0.0205 (etruscan, 5× weaker) | FAIL p=0.0953                                | (clean — see polluted_aquitanian / greek_polluted_aquitanian)                | substrate-LM-specific: Mediterranean LMs reward Aquitanian, Mycenaean-Greek does not    |
| polluted_aquitanian        | (n/a — built for v14)      | (n/a)                              | (n/a)                                        | **PASS p=2.74e-05 (basque, 50/50 same-dist polluted)**                       | gate is curation-tolerant; top-20 is 9 real / 11 conjectural (~50/50, within-tail MW p=0.98) |
| greek_polluted_aquitanian  | (n/a — built for v15)      | (n/a)                              | (n/a)                                        | **PASS p=2.01e-03 (basque, 50/50 cross-language polluted)**                  | partial-discrimination; top-20 is 13 real / 7 conj-greek, within-tail real>conj p=8.3e-05 |
| etruscan                   | PASS p=5.21e-04 (etruscan) | FAIL p=0.591 (basque)              | FAIL p=0.185                                 | (not run; out of scope for v14/v15)                                          | cleanly substrate-LM-specific; both unrelated LMs collapse the separation              |
| toponym                    | FAIL p=0.92                | (skipped; v10 already FAIL)        | (skipped)                                    | (n/a)                                                                        | not validated — see "Toponym failure" below                                            |
| linear_b_carryover         | (positive-control pool)    | (positive-control pool)            | **FAIL p=0.155** (Mycenaean-Greek own-LM)    | (n/a)                                                                        | **POSITIVE CONTROL FAILED** at the population gate — see "What this means" below       |

### Etruscan: cleanly validated

The Etruscan substrate top-20 separates from its matched control
top-20 at p=5.21e-04 under the Etruscan LM, and the separation
collapses (p=0.591) under the Basque LM and weakens substantially
(p=0.185) under the Mycenaean-Greek LM. This is the clean signature
of substrate-LM specificity: the metric only rewards Etruscan
substrate when paired with a phonotactic prior trained on real
Etruscan text. The top-20 surfaces are a coherent semantic stratum:
religious vocabulary (`aiser` "gods", `thesan` dawn-goddess, `hanthe`
ritual position, `spureri` sacrifice-for-the-city), praenomina
(`larth`, `laris`, `thana`, `sech`), function words (`camthi`
magistrate, `nac` as/when, `matam` above/before, `chimth` at/near),
time references (`avils` of-years, `zelar` ritual-time, `caitim`
month-name).

### Aquitanian: validated, but with caveats

Under the Basque LM, Aquitanian substrate top-20 (median posterior
0.9808) decisively beats its matched control top-20 (median 0.9512;
p=3.22e-05). Under the Etruscan LM, the separation persists at
p=0.0205 — 5× weaker than same-LM, but still present. Under the
Mycenaean-Greek LM, the separation drops below the gate (p=0.0953;
substrate median 0.9808 vs control median 0.9630; MW U 248.5 vs the
null expectation of 200).

The pattern across three LMs is informative:

* The Aquitanian PASS is **not** "natural-language LM bias" in the
  general sense — if it were, all three natural-language LMs
  would reward Aquitanian roots equally and the separation would
  persist under the Mycenaean-Greek LM. It does not.
* The v11 partial cross-LM separation under the Etruscan LM is
  most likely a **Basque-Etruscan kinship artifact**: both
  languages share Mediterranean phonotactic features (CV
  syllables, similar consonant inventories, no consonant clusters
  in core vocabulary) that the Aquitanian roots match. Mycenaean
  Greek is also a natural language but has very different
  phonotactic statistics — heavy CV CVC syllables, different vowel
  distribution, labiovelars (`q`-class) — and Aquitanian roots
  no longer dominate the right tail.
* The v10 Aquitanian PASS is therefore more genuinely
  substrate-specific than v11's mixed result suggested. The PASS
  is contingent on the LM having Mediterranean phonotactic
  statistics close enough to Aquitanian's that the right tail
  separates from the matched control's random-phonotactic surfaces.

### Toponym: not validated

The toponym pool failed the right-tail gate at p=0.92 under its own
LM (Basque, used as a substrate-style stand-in since no pre-Greek
text corpus is available). The substrate side recovers recognizable
Aegean toponyms (`dikte`, `keos`, `kno`, `minoa`, `tenos`, `iassos`,
etc., posterior 0.82–0.98), but the matched control surfaces
(`eoao`, `aathei`, `eta`, `ioonaol`) sit at *higher* posteriors
(0.89–0.99) — the control sampler's character distribution drifted
into a region the LM treats as low-perplexity for the wrong reason.
This is a real failure of the matched-control sampler for the
toponym pool, not a substrate-side issue. Tightening the sampler is
out-of-scope for v12 and a candidate next ticket.

### Linear-B carryover: positive control FAILED at the population gate

mg-4664 promoted the 20 curated Linear-B carryover anchors
(`hypotheses/curated/{anchor,v4_anchor}_*.yaml`) into a first-class
substrate pool and scored them against `pools/control_linear_b_carryover.yaml`
under a Mycenaean-Greek LM trained on 5,113 unique Mycenaean-Greek
word forms from the LiBER corpus (5,638 inscriptions). Linear-B
carryover values are KNOWN-correct readings under the
Ventris-Chadwick 1956 syllabogram identification, so the framework
must recover signal here or it is broken on a known case.

Headline: **the gate fails at p=0.155** (n=12 substrate top vs n=11
control top). The substrate top-20 median posterior is 0.7500 and
the control top-20 median is 0.3103, so the directionality is
correct and the magnitude separation is large. But the population
MW U does not cross p<0.05.

The right-tail leaderboard explains why:

| rank | side | surface  |   n |   k | posterior | reading                                        |
|----:|:------|---------|----:|----:|:---------:|:-----------------------------------------------|
|   1 | sub  | `mate`   |  50 |  50 | 0.9808    | "ma-te" Linear-B carryover                     |
|   2 | sub  | `tare`   |  50 |  50 | 0.9808    | "ta-re" Linear-B carryover                     |
|   3 | sub  | `kiro`   |  50 |  45 | 0.8846    | "ki-ro" deficit/owed (Linear-A accountancy)    |
|   4 | sub  | `kuro`   |  50 |  43 | 0.8462    | "ku-ro" total/sum (Linear-A accountancy)       |
|   5 | ctrl | `reka`   |  21 |  18 | 0.8261    | random Linear-B-phonotactic control            |
|   6 | sub  | `kira`   |  50 |  39 | 0.7692    |                                                |
|   7 | sub  | `tana`   |  50 |  39 | 0.7692    |                                                |
|   8 | ctrl | `narase` | 100 |  77 | 0.7647    |                                                |
|  ... | ...  |  ...     | ... | ... |   ...     |                                                |
|  18 | sub  | `ara`    |  50 |   9 | 0.1923    | "a-ra" conjectural onomastic                  |
|  19 | sub  | `taina`  |  50 |   9 | 0.1923    | "ta-i-na" conjectural onomastic               |
|  20 | sub  | `dina`   |  50 |   5 | 0.1154    | "di-na" recurring lexeme                      |
|  23 | sub  | `dare`   |  50 |   0 | 0.0192    | "da-re" libation-formula continuation         |

The gate failure has a specific shape: the **canonical Linear-A
administrative terms** (`kuro`, `kiro`, `mate`, `tare`) decisively
clear their controls (substrate posterior 0.85–0.98), but the
**conjectural anchors** (`dare`, `dina`, `ara`, `taina`,
`kumina`) drag the substrate distribution down because they don't
separate from random Mycenaean-Greek phonotactic strings. The
population MW U on top-K substrate vs top-K control therefore
straddles p<0.05 because top-K of each side includes both the
clean wins (`mate`, `kuro`, `kiro`) and the bad anchors (`dare` at
0.02 — substrate loses 50/50 paired records).

### What this means for v10 / v11

The Linear-B positive control fails the population gate but
*succeeds* on the well-attested subset. Two interpretations are
compatible with the data:

1. **The gate is too conservative for mixed-cleanness pools.** The
   v10 / v11 PASSes for Aquitanian and Etruscan are genuine
   substrate signal that survives the gate by virtue of having
   uniformly clean substrate surfaces. The positive-control failure
   is then specifically a function of the carryover anchor pool
   containing both well-attested and conjectural readings, not a
   defect of the framework. If true, this would mean the v10
   Aquitanian / Etruscan PASSes can be trusted, but a stricter
   gate (e.g. require top-K substrate to *uniformly* beat top-K
   control by some margin, rather than only beat them in
   median-of-rank-pairs) would be more honest about heterogeneous
   substrate cleanness.
2. **The framework recovers signal only on substrate sets where the
   majority of entries are correct.** Under this reading, the v10
   PASSes for Aquitanian and Etruscan reflect that those pool
   designs (Trask 1997 core vocabulary; Bonfante & Bonfante's well-
   attested forms) happen to be uniformly clean. The framework
   would not recover signal on a pool where, say, half the entries
   are wrong — and we can't independently certify that the
   Aquitanian / Etruscan pools meet that bar without a domain
   expert. The Linear-B positive control's failure is then a
   warning that the gate is sensitive to substrate-pool curation,
   not a free certification.

We cannot disambiguate these two readings from this ticket's data.
Both are consistent with what we observe. **The conservative
interpretation is reading #2**: ship the v10 Aquitanian and Etruscan
PASSes as "promising-but-validated-only-conditionally-on-pool-curation"
rather than as cleanly-publishable claims. Domain expert review of
the top-K substrate surfaces is the missing ingredient.

A refined gate that handles heterogeneous substrate cleanness is a
candidate next ticket. It would not require a new metric — only a
new aggregation rule.

### v13 cross-window coherence test (mg-c216) — adjudicates the v12 fork

The v13 ticket addressed the v12 fork directly with a coherence test:
for the v10 Aquitanian + Etruscan top-20 substrate surfaces, do the
sign-to-phoneme mappings *agree* across the many positive-paired-diff
candidate equations, or are they incoherent across windows? The
falsifiable cases were:

* Coherence ≥ 0.6 on both pools → reading #1 (gate-too-conservative);
  v10 PASSes reflect coherent underlying mappings; gloss-shape work
  becomes a clean follow-up.
* Coherence < 0.6 on both pools → reading #2 (curation-sensitivity);
  v10 PASSes reflect noise on different sign bases; the next ticket
  reframes toward held-out pool-curation tests.
* Mixed verdict → cleaner pool advances; noisier pool needs more
  validation.

**Result:**

| pool       | n_surfaces | n_with_coherence | median coherence | min     | max     | gate (≥0.60) |
|:-----------|:----------:|:----------------:|:----------------:|:-------:|:-------:|:------------:|
| aquitanian |     20     |        20        |     0.1818       | 0.1805  | 0.1864  |    **FAIL**  |
| etruscan   |     20     |        20        |     0.1808       | 0.1739  | 0.1867  |    **FAIL**  |

Both pools fail decisively. The values cluster tightly in [0.17, 0.19]
— nowhere near the 0.6 acceptance bar, nowhere near even the
"close-but-no-cigar" 0.5–0.55 region. **Reading #2 is supported.**
v10 PASSes do not reflect stable per-sign readings; they reflect
substrate-phonotactic kinship that the metric rewards broadly.

The companion **refined-gate sensitivity check** on the Linear-B
positive control:

| K  | n_substrate_top | n_control_top | median substrate | median control | MW U  | p (one-tail) |
|---:|:---------------:|:-------------:|:----------------:|:--------------:|:-----:|:------------:|
|  5 |       5         |      5        |     0.8846       |    0.5772      | 24.0  |  **0.0106**  |
| 10 |      10         |     10        |     0.7692       |    0.3552      | 71.0  |   0.0603     |
| 20 |      12         |     11        |     0.7500       |    0.3103      | 83.0  |   0.1547     |

K=5 cleanly clears p<0.05 (the K=20 production gate is somewhat
over-conservative on mixed-cleanness pools), but this is a
surface-aggregate fact and does not rescue the deeper coherence
failure. Full breakdown in `docs/findings.md` mg-c216 entry and
`results/consensus_sign_phoneme_map.md`.

## Top-K substrate surfaces by pool (publication-readable)

The leaderboards below are the v10 (mg-d26d) bayesian posterior
top-K, ranked by raw posterior_mean. They reflect the substrate
beating its phonotactically-matched control in the right tail, as
of v10. Under v11 / v12 cross-LM tests, these orderings are
substantially preserved (the substrate top-20 mostly stays in the
top-20 across LMs even when the gate stops clearing) — so reading
this as "the surfaces most consistently rewarded by the metric on
the substrate side" remains valid.

### Aquitanian top-20 (under Basque LM; see `results/rollup.bayesian_posterior.aquitanian.md`)

| rank | surface  | n | k | posterior_mean | semantic field           |
|----:|:----------|--:|--:|:--------------:|:-------------------------|
|   1 | `aitz`    | 50 | 50 | 0.9808 | nature: rock              |
|   2 | `eki`     | 50 | 50 | 0.9808 | nature: sun               |
|   3 | `argi`    | 50 | 50 | 0.9808 | nature: light             |
|   4 | `itsaso`  | 50 | 50 | 0.9808 | nature: sea               |
|   5 | `zelai`   | 50 | 50 | 0.9808 | nature: meadow            |
|   6 | `oin`     | 50 | 50 | 0.9808 | body: foot                |
|   7 | `bihotz`  | 50 | 50 | 0.9808 | body: heart               |
|   8 | `beltz`   | 50 | 50 | 0.9808 | descriptor: black         |
|   9 | `ona`     | 50 | 50 | 0.9808 | descriptor: good          |
|  10 | `gaitz`   | 50 | 50 | 0.9808 | descriptor: ill           |
|  11 | `hau`     | 50 | 50 | 0.9808 | function: this            |
|  12 | `nahi`    | 50 | 50 | 0.9808 | function: desire          |
|  13 | `entzun`  | 50 | 50 | 0.9808 | function: hear            |
|  14 | `hanna`   | 50 | 50 | 0.9808 | kinship: brother          |
|  15 | `egun`    | 50 | 50 | 0.9808 | time: day                 |
|  16 | `ezti`    | 50 | 50 | 0.9808 | food: honey               |
|  17 | `ate`     | 50 | 50 | 0.9808 | dwelling: door            |
|  18 | `hesi`    | 50 | 50 | 0.9808 | place: fence              |
|  19 | `zortzi`  | 50 | 50 | 0.9808 | number: eight             |
|  20 | `ako`     | 50 | 50 | 0.9808 | morphology: suffix        |

This reads like a Swadesh-list cross-section of inherited core
Basque vocabulary across the standard semantic families. No semantic
family dominates.

### Etruscan top-20 (under Etruscan LM; see `results/rollup.bayesian_posterior.etruscan.md`)

| rank | surface       | n | k | posterior_mean | gloss                                |
|----:|:---------------|--:|--:|:--------------:|:-------------------------------------|
|   1 | `larth`        | 50 | 50 | 0.9808 | praenomen "Larth"                       |
|   2 | `aiser`        | 50 | 50 | 0.9808 | "gods"                                  |
|   3 | `matam`        | 50 | 50 | 0.9808 | "above / before"                        |
|   4 | `avils`        | 50 | 50 | 0.9808 | "of years"                              |
|   5 | `camthi`       | 50 | 50 | 0.9808 | magistracy                              |
|   6 | `chimth`       | 50 | 50 | 0.9808 | "at / near"                             |
|   7 | `hanthe`       | 50 | 50 | 0.9808 | ritual position                         |
|   8 | `laris`        | 50 | 50 | 0.9808 | praenomen "Laris"                       |
|   9 | `nac`          | 50 | 50 | 0.9808 | "as / when"                             |
|  10 | `sech`         | 50 | 50 | 0.9808 | "daughter"                              |
|  11 | `thana`        | 50 | 50 | 0.9808 | praenomen "Thana"                       |
|  12 | `zelar`        | 50 | 50 | 0.9808 | ritual time-reference                   |
|  13 | `caitim`       | 50 | 50 | 0.9808 | month-name                              |
|  14 | `thesan`       | 50 | 50 | 0.9808 | dawn-goddess                            |
|  15 | `spureri`      | 50 | 50 | 0.9808 | "sacrifice for the city"                |
|  16 | `thanchvil`    | 50 | 50 | 0.9808 | praenomen "Thanchvil"                   |
|  17 | `suthi`        | 50 | 50 | 0.9808 | "tomb / burial"                         |
|  18 | `mach`         | 50 | 50 | 0.9808 | numeral "five"                          |
|  19 | `arnth`        | 50 | 50 | 0.9808 | praenomen "Arnth"                       |
|  20 | `sath`         | 50 | 50 | 0.9808 | (unattested gloss; recurring stem)      |

Religious vocabulary + common praenomina + function words + time
references — exactly the genre profile of the Etruscan votive /
funerary corpus the pool was sourced from.

### Toponym top-20 (under Basque LM; see `results/rollup.bayesian_posterior.toponym.md`)

The substrate top-20 is geographically coherent (Aegean + Anatolian
+ Cretan toponyms in proportion: `dikte`, `keos`, `kno`, `minoa`,
`tenos`, `iassos`, `lemnos`, `kuzikos`, `melitos`, `tulisos`,
`melos`, `aspendos`, `kalumnos`, `zakuntos`, `lukia`, `mukenai`,
`lykabettos`, `itanos`, `halikarnassos`, `poikilassos`), but does
not clear the gate against its matched control because of the
control-sampler issue documented above.

### Linear-B carryover top-12 (under Mycenaean-Greek LM; see `results/rollup.bayesian_posterior.linear_b_carryover.md`)

| rank | surface    | n | k | posterior_mean | reading                                  |
|----:|:------------|--:|--:|:--------------:|:-----------------------------------------|
|   1 | `mate`      | 50 | 50 | 0.9808 | "ma-te"                                     |
|   2 | `tare`      | 50 | 50 | 0.9808 | "ta-re"                                     |
|   3 | `kiro`      | 50 | 45 | 0.8846 | "ki-ro" deficit/owed (Linear-A accountancy) |
|   4 | `kuro`      | 50 | 43 | 0.8462 | "ku-ro" total/sum (Linear-A accountancy)    |
|   5 | `kira`      | 50 | 39 | 0.7692 | "ki-ra"                                     |
|   6 | `tana`      | 50 | 39 | 0.7692 | "ta-na"                                     |
|   7 | `karu`      | 50 | 37 | 0.7308 | "ka-ru"                                     |
|   8 | `kumina`    | 50 | 14 | 0.2885 | "ku-mi-na"                                  |
|   9 | `ara`       | 50 |  9 | 0.1923 | "a-ra" conjectural onomastic               |
|  10 | `taina`     | 50 |  9 | 0.1923 | "ta-i-na" conjectural onomastic            |
|  11 | `dina`      | 50 |  5 | 0.1154 | "di-na" recurring lexeme                   |
|  12 | `dare`      | 50 |  0 | 0.0192 | "da-re" libation-formula continuation      |

The top-7 is a clean win for the framework: well-attested Linear-B
carryover values cleanly beat random Mycenaean-Greek-phonotactic
controls. The bottom-5 pulls the population gate below p<0.05 —
those anchors don't separate. Specifically, `dare` (which the
curator flagged as "libation-formula continuation, da-ta-re
paradigm") loses 50/50 paired records.

## Consensus sign-to-phoneme map (v13, mg-c216)

For each Linear A sign s with at least 10 positive-paired-diff
proposals from v10-top-20 substrate equations (across both Aquitanian
+ Etruscan pools), the consensus map reports the histogram of
proposed phonemes plus the modal phoneme + smoothed Dirichlet-
multinomial posterior + max-likelihood Shannon entropy. 60 of 61
candidate signs cleared the n_min threshold; **every consensus
entry has entropy ≥ 2.05 bits** out of log2(23) ≈ 4.52 maximum, and
**no sign reaches modal posterior > 0.27**. The five lowest-entropy
signs (the most-coherent end of the distribution):

| sign  | n_proposals | modal | modal_posterior | entropy_bits | n contributing v10 surfaces |
|:------|:-----------:|:-----:|:---------------:|:------------:|:---------------------------:|
| `A718`|     12      |  `i`  |     0.2340      |    2.055     |             12              |
| `AB13`|     26      |  `i`  |     0.2267      |    2.998     |             26              |
| `A306`|     14      |  `i`  |     0.1373      |    3.039     |             14              |
| `AB66`|     15      |  `i`  |     0.1321      |    3.057     |             14              |
| `A323`|     14      |  `a`  |     0.1765      |    3.093     |             14              |

For comparison, the *high-frequency* signs are uniformly diffuse:
AB08 (464 proposals, modal `a` at posterior 0.167, entropy 3.925
bits, top-3 alternatives e/h/z); AB37 (227 proposals, modal `i` at
posterior 0.187, entropy 3.713 bits, alternatives a/n/th); AB28 (225
proposals, modal `i` at posterior 0.159, entropy 3.788 bits,
alternatives a/n/th). The contributing-surfaces lists for those
high-frequency signs include essentially the entire v10 top-20 (38+
surfaces each) — the structural reason consensus is diffuse: the
metric rewards substrate phonotactic surfaces broadly rather than
specific sign-to-phoneme assignments. Different substrate roots
that align with the same Linear A window propose different sign
mappings, and all of them score positive paired_diffs.

Full table at `results/consensus_sign_phoneme_map.md`.

## Per-inscription concentration

mg-0f97 mapped, for each Linear-A inscription, how many of the v10
top-20 substrate surfaces have positive paired-diff records on it.
Two clusters surfaced:

* **Cluster A (Etruscan-validated, accountancy + votive).** Top-density
  inscriptions: `HT Wc 3010`, `HT Wc 3017a`, `KH 60`, `KN Zb 5`,
  `HT 90`, `KH 10`, `KH 5`, `HT 127a`, `HT 12`, `ARKH 6`. Each
  has ~14 v10 top-20 surfaces with positive evidence on it,
  dominated by the Etruscan religious / praenomen / time-reference
  cluster (`aiser`, `avils`, `bihotz`, `camthi`, `entzun`, `hanna`,
  `hanthe`, `itsaso`, `laris`, `matam`, `thesan`, `zelai`, `zelar`,
  `zortzi`, plus `caitim` / `thanchvil` / `spureri` on the Knossos
  votive subset). v12 framed these as the publishable per-inscription
  candidates under the conservative reading. **v13 downgrades this**:
  the consensus map shows the underlying sign-to-phoneme mappings on
  these inscriptions are not coherent across windows, so "this
  inscription contains *aiser*" is not a claim the data supports —
  only "this inscription is enriched in v10-top-20 substrate
  *surface-aggregate* signal" is.
* **Cluster B (Aquitanian-mixed, longer accountancy).** `GO Wc 1a`,
  `ARKH 5`, `HT 104`, `HT 103`, `ARKH 2`, etc. show 23–38 distinct
  top-20 surfaces concentrated, with the Aquitanian side
  (`aitz`, `ako`, `ate`, `eki`, `hau`, `oin`, `ona`, `argi`, `nahi`)
  mixing in alongside the Etruscan side. v12 flagged these as
  inheriting the Aquitanian validation caveat. **v13 makes them
  unsuitable for any reading-shape claim** for the same reason as
  cluster A — without coherent per-sign mappings, multi-surface
  density at an inscription is not evidence of a readable text.

Full per-inscription tables in `results/rollup.right_tail_inscription_concentration.md`.

## Supportable claims

After v14 + v15, "subject to the conservative reading of curation-
sensitivity" is no longer the binding caveat: v14's same-distribution
polluted-pool PASS shows the framework's PASS signal does not depend
on uniformly-clean substrate pools, and v15's cross-language polluted-
pool result narrows the boundary further. The supportable-claims list
below is therefore *less* hedged on curation than it was after
v13, but *more* hedged on the per-surface meaning of the right-
tail leaderboard.

* **The framework's headline gate is curation-tolerant within the
  same phoneme + length distribution AND is partially shape-
  selective across distributions.** v14: the same-distribution
  polluted Aquitanian pool (50% conjectural) PASSes at p = 2.74e-05,
  essentially matching the clean pool's p = 3.22e-05. (mg-6b73) v15:
  the *cross-language* polluted Aquitanian pool (50% Greek-shape
  conjecturals) also PASSes — but ~70× weaker, at p = 2.01e-03 — and
  within the right tail real Aquitanian dominates Greek-shape
  conjecturals at p = 8.29e-05. (mg-7ecb) The headline gate clears
  for any pool with non-trivial char-bigram overlap with the LM,
  but within the right tail the framework partially respects
  substrate-distribution shape.
* **The right-tail leaderboard within-tail-discriminates substrate-
  shape from non-substrate-shape when both are mixed in the same
  pool.** v14 showed no within-tail discrimination on same-Aquitanian-
  shape conjecturals (real-vs-conjectural MW p = 0.98). v15 showed
  strong within-tail discrimination on Greek-shape conjecturals
  (real-vs-conjectural-greek MW p = 8.29e-05). The distinguishing
  axis is whether the polluting distribution matches the substrate's
  own; when it doesn't, the leaderboard partially recovers signal
  even though the population gate doesn't break. (mg-7ecb)
* **The metric (`external_phoneme_perplexity_v0`) discriminates
  substrate from random-phonotactic controls when the substrate
  surfaces are well-attested.** The top of every substrate pool's
  bayesian posterior is dominated by surfaces drawn from canonical
  vocabulary lists; the bottom is dominated by less-attested
  conjectural readings. This is mechanically demonstrable.
* **Substrate-LM specificity holds for Etruscan.** The Etruscan
  top-20 separation collapses cleanly when re-routed through
  unrelated LMs (Basque p=0.591, Mycenaean-Greek p=0.185). This
  is what we expect of a real substrate signal: the LM that knows
  the substrate's phonotactics is the one that distinguishes it.
* **Substrate-LM specificity holds for Aquitanian when judged
  against truly unrelated LMs.** The v11 partial separation under
  Etruscan LM (p=0.0205) is best understood as a Mediterranean
  phonotactic-kinship artifact, not as evidence against
  substrate-specificity. Under Mycenaean-Greek (genuinely unrelated
  natural-language LM), Aquitanian no longer beats its control.
* **A defined set of Linear-A inscriptions concentrate substrate
  *surface-aggregate* evidence.** Cluster A in particular (Knossos
  Zc/Zf, HT Wc / Zb, Khania `KH 60` / `KH 10` / `KH 5`, HT Wc
  commodity records) is enriched in the Etruscan-validated top-20
  surfaces' positive paired_diff records. v13's coherence verdict
  rules out claiming these inscriptions are *readable* under the v10
  surface set, but the concentration of substrate-aggregate signal
  on these particular inscriptions is itself a reproducible
  observation. Domain-expert review of these tablets is still the
  natural follow-up; what it can establish is now narrower.
* **The corpus is well-curated and the pipeline is deterministic.**
  Re-running any rollup on the same result stream + manifests
  produces byte-identical output. No RNG anywhere in the scoring
  path.

## Unsupportable claims

* **"The right-tail substrate surfaces are validated as substrate
  vocabulary."** The v14 polluted-pool test rules this out: the
  framework cannot distinguish real Aquitanian roots from
  *same-distribution* (Aquitanian-shape) phonotactically-matched
  conjectural surfaces in the same pool's right tail (top-20 split
  9 real / 11 conjectural; real-vs-conjectural one-tail MW p = 0.98,
  mg-6b73). The right tail is a *phonotactic-shape* response, not a
  substrate-vocabulary validation. Surfaces in the v10 top-K should
  be read as "Aquitanian-shaped surfaces the LM rewards consistently
  in the Linear-A corpus" — not as "real Aquitanian roots the
  framework has identified in Linear-A." v15 partially refines this:
  the framework *does* discriminate real from *cross-language*
  conjectural surfaces (real-vs-conjectural-greek p = 8.29e-05,
  mg-7ecb), so the response is specifically Aquitanian-shaped, not
  just any-shape-the-Basque-LM-likes. But the per-surface
  vocabulary-validation claim remains unsupported.
* **"Linear-A is Etruscan / Aquitanian / pre-Greek"** is *not*
  supported. The framework tests whether substrate roots beat
  matched controls in the right tail under a phoneme LM; it does
  not establish lexical identity between Linear-A signs and
  substrate phonemes. The mechanical signal is consistent with
  multiple causal stories.
* **A specific sign-to-phoneme mapping for Linear-A.** No such
  mapping has been validated, and v13's consensus map (mg-c216)
  established this *empirically* rather than only conservatively:
  the modal phoneme proposed for every consensus-eligible Linear A
  sign by the v10 top-20 substrate equations is far from
  unanimous (entropy ≥ 2.05 bits, modal posterior ≤ 0.27). The
  candidate-equation hypotheses pin a substrate root to a specific
  window in a specific inscription, but the metric scores the
  *partial mapping perplexity*, not the equation itself. The right
  tail tells us which substrate surfaces survive the test; it does
  not tell us the equation must be correct, and it does not — per
  v13 — induce stable per-sign readings. See
  `results/consensus_sign_phoneme_map.md`.
* **A reading of any specific Linear-A inscription.** Cluster A is
  enriched in Etruscan-validated top-20 surfaces, but the
  framework does not adjudicate whether `HT Wc 3010` actually
  contains `aiser` etc. — it adjudicates whether `aiser` is
  consistently rewarded over its matched controls when scored
  against the Linear-A corpus as a whole. v13's coherence map
  empirically confirms this: even on inscriptions where many
  v10-top-20 surfaces show positive paired_diff records, the
  underlying sign-to-phoneme mappings disagree, so the inscription
  is not "readable" under the v10 substrate set in any operational
  sense.
* **The toponym substrate hypothesis** — the gate failed and the
  control-sampler issue means we can't even report this null
  cleanly. No conclusion either way until the sampler is fixed.
* **Conjectural Linear-B carryover values** (`dare`, `dina`,
  `ara`, `taina`). The positive-control test rejects these — they
  do not separate from random Mycenaean-Greek-phonotactic
  controls. Whether this means the conjectural readings are wrong
  or that the framework only recognizes well-attested values is an
  open question.

## Remaining work for full publication

In rough priority order, *as updated by the v14 + v15 verdicts*:

1. **v16: methodology paper draft.** v14 + v15 together have
   solidified the manuscript-shape claim into the partial-
   discrimination refinement above; v16 polishes that narrative
   for external readers. Out of scope for v15 itself; the natural
   next ticket.
2. **Domain-expert review of top-K Etruscan and Aquitanian
   surfaces** — is the right-tail leaderboard a reasonable lexical
   subset, or are we surfacing morphological artifacts? After v14 +
   v15 this is the load-bearing missing piece: the framework
   *partially* distinguishes real surfaces from cross-language
   conjecturals but does not distinguish real from same-distribution
   conjecturals. The only way to convert "the right tail is
   phonotactically Aquitanian-shape-likely" into "the right tail is
   real Aquitanian vocabulary present in Linear-A" is independent
   expert review. Not a polecat ticket.
3. **Refined acceptance gate that is robust to mixed-cleanness
   pools.** The Linear-B positive control's failure-by-long-tail
   is a methodological signal that v13's K-sweep partially
   confirmed (K=5 cleanly clears, K=20 fails). A stricter rule
   (e.g. require top-N% of substrate to uniformly beat top-N% of
   control by some margin) would more honestly handle pools with
   heterogeneous curation. This is an analysis-layer ticket, no
   new metric. Lower priority now that v13 has shown the deeper
   coherence problem is the binding constraint.
3. **Tighter matched-control sampler for the toponym pool.** The
   v10 toponym FAIL is on the control side — the random
   phoneme-frequency sampler's drift into a low-LM-density corner
   that the LM accidentally rewards. The substrate side is
   internally coherent (recognizable Aegean toponyms). Fixing the
   sampler may turn this into a cleaner null or a fourth PASS.
4. **Per-window deduplication** (mg-f419 follow-up) — duplicate
   scoring of the same window under multiple roots inflates n
   without inflating evidence. Small effect; not blocking anything.
5. **GORILA ingest** — adds numerals and line-break information not
   in SigLA, would expand the corpus by ~10–15%.
6. **Phoenician / Sumerian / Hattic / other substrate pools** —
   the framework can in principle test any substrate hypothesis
   with attested vocabulary and a phoneme LM. None of these is on
   the critical path for the existing pools' validation.
7. **(Optional) Pollution-level sweep.** v15 ran the cross-language
   pollution test that v14 deferred; finer-grained same-distribution
   pollution sweeps (10% / 25% / 75%) would tell us whether the
   gate has a sharp threshold or smooth gradient under same-
   distribution noise. Not load-bearing for the manuscript shape
   after v15.
8. **(Optional) Cross-language gates with other LMs.** v15 used
   Mycenaean-Greek as the polluting LM. The same test under Etruscan
   or Linear-B-as-substrate could illuminate which Mediterranean
   phonotactic features the gate is responding to. Defer pending
   v16 manuscript priorities.
9. **Manuscript draft.** Subsumed by v16 above.
