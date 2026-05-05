# Mechanical Falsifiable Testing of Substrate-Language Hypotheses for Linear A

**Methodology paper draft (v16, mg-d5ed; lineage citations corrected
in v17, mg-2bfd; v19 cascade-candidate / external-validation
integration in v20, mg-711c)** — a publication-readable consolidation
of what the Lineara project has mechanically established about
Linear A across 20 work items, anchored on the SigLA corpus ingest
(`mg-1c8c`) and spanning the harness pipeline `mg-d5ef` (v0) through
`mg-3438` (v19). The repo scaffold (`mg-9e00`) predates the corpus
ingest. The companion log `docs/findings.md` carries the per-ticket
history; this document carries the consolidated methodology, results,
and supportable / unsupportable claim split, audited end-to-end
against the committed result files in `results/` and the merge notes
in `docs/findings.md`.

The intended reader is a research scientist or Aegean-syllabary
specialist who has not followed the merge notes. Section ordering
follows the standard methodology-paper shape (Abstract, Introduction,
Methods, Results, Discussion, Limitations, Conclusion) so the document
can be read cold.

---

## Abstract

Past attempts to decipher Linear A — the undeciphered Bronze Age
Aegean syllabary (~761 transcribed inscriptions in the SigLA corpus,
4,935 sign occurrences) — have repeatedly suffered from
motivated-reasoning failure modes: a candidate substrate language is
asserted, plausible-looking matches are advanced as evidence, and
unfavourable cases are explained away. We ask whether **mechanical,
falsifiable testing** of substrate-language hypotheses is tractable,
and what it can and cannot establish.

The framework scores candidate equations (substrate-root → Linear A
sign window) under an external character-bigram phoneme **language
model (LM)** trained on real substrate text, paired against
phonotactically-matched scramble controls drawn from each substrate
pool's own marginal phoneme distribution. Per-surface paired-difference
evidence is aggregated as a Beta-binomial posterior over θ_S = P(this
surface beats its matched control on a given Linear A window). The
**right-tail Bayesian gate** is a one-tail Mann-Whitney U test on the
top-K substrate posteriors versus the top-K matched-control posteriors,
with K=20 the production setting.

We evaluate three substrate hypotheses (Aquitanian, Etruscan, pre-Greek
Aegean toponyms) plus a Linear-B-carryover positive control under
seven falsifiable acceptance gates: own-LM right-tail (mg-d26d),
cross-LM and third-LM negative controls (mg-0f97 / mg-4664), per-sign
cross-window coherence (mg-c216), and same-distribution and
cross-language pollution tests (mg-6b73 / mg-7ecb). The framework
**detects substrate-LM-phonotactic kinship at the population level**
(Aquitanian PASS p = 3.22e-05, Etruscan PASS p = 5.21e-04 under their
own LMs) and **partially discriminates substrate-shape from
non-substrate-shape within the right tail** (real-vs-Greek-shape
within-tail Mann-Whitney p = 8.29e-05). It does **not** support
per-sign decipherment: the consensus sign-to-phoneme map fails the
0.6 cross-window-coherence bar decisively (median 0.18 on both
Aquitanian and Etruscan v10 top-20 sets), and a same-distribution
pollution test cannot distinguish real Aquitanian roots from
phonotactically-matched conjecturals (real-vs-conjectural within-tail
p = 0.98).

A per-inscription cascade-candidate test (mg-3438) further refines
the picture: three inscriptions (`KH 10`, `KH 5`, `PS Za 2`) reach
internal consensus across multiple substrate candidates on ≥ 50% of
their signs under a robust statistic (modal posterior > 0.5 with
n_proposals ≥ 2). The first **external validation** of the framework
— against the long-attested scholarly transliteration `ja-sa-sa-ra-me`
of the Linear A libation formula AB57-AB31-AB31-AB60-AB13 on
`PS Za 2` — finds the framework's mechanical consensus reads
`th-u-u-n-i`, divergent from the scholarly proposal on every
formula-span sign (0/5 consonantal-segment match). A targeted
follow-up search (mg-711c) for additional comparable sequences in
the cascade-candidate inscriptions — the well-attested accountancy
totals `ku-ro` (AB81-AB02) and `ki-ro` (AB67-AB02) — finds neither
sequence in `KH 10` or `KH 5`, leaving the libation formula on
`PS Za 2` as the project's sole external comparand to date.
**Internal consensus across surviving candidates does not imply
external correctness:** mechanical scoring + phonotactically-matched
controls catches a failure mode that internal-consensus-only
methodology would miss.

The supportable claim is therefore strictly narrower than "Linear A
is X": the framework identifies which substrate phonotactic profiles
produce population-level signal in the SigLA corpus, and on which
inscriptions that signal concentrates, but does not validate specific
sign readings — and where external validation against an independent
scholarly proposal is available, the mechanical reading diverges.

---

## 1. Introduction

Linear A, the Bronze Age Aegean syllabary in use ~1800–1450 BCE, has
resisted decipherment despite a century of scholarly attention. Its
sister script Linear B was deciphered (as Mycenaean Greek) by Ventris
and Chadwick in 1956, but Linear A's underlying language remains
unidentified, and proposed substrate identifications — pre-Greek
Aegean, Anatolian Indo-European, Etruscan-related Tyrrhenian, Semitic,
isolate-Vasconic, etc. — have not converged.

Past decipherment attempts have shared two failure modes:

1. **Confirmatory presentation.** A candidate substrate is named, a
   small set of inscriptions is offered as glossable under that
   substrate, and contrary evidence is rationalized rather than
   weighed mechanically. Without an explicit null model, "this looks
   plausible" is the typical evidentiary standard.
2. **Per-sign over-specification.** A specific syllabogram-to-phoneme
   correspondence is proposed and defended on a small number of cases,
   without testing whether the same correspondence remains stable
   across the rest of the corpus.

This project asks a narrower, more tractable question: **given a
substrate-language hypothesis with attested vocabulary and a phoneme
language model trained on real substrate text, can we mechanically
test whether the hypothesis exhibits population-level phonotactic
signal in the Linear A corpus, with appropriate phonotactically-
matched negative controls?** The bet was that many cheap mechanical
experiments, each with a pre-registered acceptance gate, would
accumulate signal that loose qualitative methods would not.

The scope is deliberately narrow:

- Three substrate-language pools (Aquitanian/Vasconic, Etruscan,
  pre-Greek Aegean toponyms) plus a Linear-B-carryover positive
  control.
- The SigLA corpus (Salgarella & Castellan; CC BY-NC-SA 4.0;
  761 transcribed inscriptions, 4,935 sign occurrences, 356 distinct
  sign IDs; `corpus_status.md`).
- Char-bigram external phoneme language models trained on real
  substrate text (Basque text for Aquitanian, the TLE Etruscan corpus
  for Etruscan, the LiBER Mycenaean-Greek transliteration for
  Linear-B-carryover).

Out of scope by construction: morphological structure, decipherment
of specific tablets, semantic gloss generation, syntactic claims, and
expansion to less-attested substrate families (Phoenician, Sumerian,
Hattic, etc.).

The remainder of this document specifies the pipeline (§2), reports
the eleven pre-registered falsifiable acceptance-gate / external-
validation outcomes (§3), discusses what the framework does and
does not detect (§4), and explicitly enumerates unsupported claims
(§5).

---

## 2. Methods

The pipeline is built up across the harness sequence `mg-d5ef` (v0)
through `mg-7ecb` (v15), atop the SigLA corpus ingest (`mg-1c8c`) and
the initial repo scaffold (`mg-9e00`). It is deterministic end-to-end:
re-running any rollup against the same
`experiments.external_phoneme_perplexity_v0.jsonl` and the same
pool / hypothesis manifests produces byte-identical output. No RNG
sits in the scoring or aggregation path.

### 2.1 Corpus

The Linear A corpus is `corpus/`: 761 inscriptions with at least one
transcribed sign, 4,935 sign occurrences across 356 distinct sign IDs,
ingested from SigLA (`https://sigla.phis.me`) under
CC BY-NC-SA 4.0. The underlying print authority is GORILA
(Godart & Olivier 1976–85). Each inscription is normalized to a
per-record JSON schema (`schema/inscription.schema.json`) with sign
tokens, position, site, support type, and provenance metadata.
Site distribution: Haghia Triada 372, Khania 213, Phaistos 63, Zakros
44, Knossos 31, Mallia 20, Arkhanes 10, plus minor sites. See
`corpus_status.md` for the full ingestion record.

### 2.2 Substrate pools

Each substrate hypothesis is encoded as a YAML pool of candidate root
surfaces with phoneme decompositions, attestations, and citations:

| pool | n_entries | source | LM dispatch |
|:--|---:|:--|:--|
| `aquitanian` | 153 | Trask 1997 + Gorrochategui 1984 (Vasconic / pre-IE roots) | basque |
| `etruscan` | 143 | Bonfante & Bonfante 2002 + TLE | etruscan |
| `toponym` | 112 | Beekes 2010 (pre-Greek Aegean toponyms) | basque (substrate-style stand-in) |
| `linear_b_carryover` | 20 | Ventris & Chadwick 1956 carryover values + Younger 2000 conjecturals (positive control) | mycenaean_greek |

The three pollution variants used for the curation-tolerance and
cross-language-pollution tests are:

| pool | n_entries | construction |
|:--|---:|:--|
| `polluted_aquitanian` | 306 | 153 real Aquitanian roots + 153 same-distribution conjecturals (mg-6b73) |
| `greek_polluted_aquitanian` | 306 | 153 real Aquitanian roots + 153 Mycenaean-Greek-shape conjecturals (mg-7ecb) |

### 2.3 Matched phonotactic controls

For each substrate pool, a corresponding `control_<name>` pool is
generated by sampling random surfaces of matching length from the
substrate's marginal phoneme histogram. Determinism is preserved by
seeding from `sha256(pool_name)`. The LM dispatch routes each control
pool through its substrate's LM so the paired-difference cancels the
LM choice out of the comparison
(`scripts/build_control_pools.py`, `mg-f419` + `mg-c2af`).

### 2.4 Hypothesis schemas

Two committed hypothesis shapes participate in the v8/v9/v10 paired-
difference data:

- **`candidate_equation.v1` (mg-d5ef, mg-fb23).** A single substrate
  root pinned to one Linear A inscription window; carries
  `sign_to_phoneme` mapping, window indices, root surface, and root
  phoneme decomposition.
- **`candidate_signature.v1` (mg-bef2).** Multiple substrate roots
  pinned to non-overlapping sub-windows of one Linear A window; each
  constituent root carries its own `sign_to_phoneme`.

Hypothesis manifests live under `hypotheses/auto/*.manifest.jsonl`
(equations) and `hypotheses/auto_signatures/*.manifest.jsonl`
(signatures). Generation is by exhaustive walk over each pool entry
× every Linear A inscription window of matching length, capped per
substrate entry to 50 candidate windows
(`scripts/generate_candidates.py`).

### 2.5 Metrics

The headline metric is **`external_phoneme_perplexity_v0`** (mg-ee18),
which feeds the candidate's phoneme stream through a held-out
char-bigram language model trained on real substrate text and reads
off the per-record log-likelihood. The bigram LMs are at
`harness/external_phoneme_models/{basque,etruscan,mycenaean_greek}.json`,
each fit with α=0.1 add-α smoothing on real text:

- **basque.json** — Basque text (Aquitanian's modern descendant) used
  as the LM for the Aquitanian substrate pool.
- **etruscan.json** — TLE Etruscan corpus.
- **mycenaean_greek.json** — LiBER (`https://liber.cnr.it`) corpus,
  5,638 Linear-B inscriptions yielding 21,634 word tokens and
  5,113 unique forms (mg-4664).

Earlier metric variants (`compression_delta_v0`,
`partial_mapping_compression_delta_v0`, `local_fit_v0`/`v1`,
`sign_prediction_perplexity_v0`, `geographic_genre_fit_v1`) are
retained in `results/experiments.jsonl` for reproducibility but did
not survive the matched-control discrimination test (mg-f419);
the current pipeline scores against `external_phoneme_perplexity_v0`
exclusively at the gating layer.

### 2.6 Paired-difference scoring

For each candidate equation/signature on the substrate side, the
matched control pool is queried for a length-equivalent random-
phonotactic surface; the same metric is computed for both sides; the
paired difference `paired_diff = substrate_score − control_score` is
recorded as one binary observation
(`paired_diff > 0` ⇒ substrate side won that record).

### 2.7 Per-surface Bayesian aggregation

For each substrate surface S, all paired-difference records targeting
S (across both single-root v8 candidates and multi-root v9
signatures, deduplicated per record) are collected. The posterior
over θ_S = P(this surface beats its matched control under the held-out
LM) is `Beta(1+k, 1+n−k)` under a `Beta(1, 1)` prior, where k is the
number of records the surface won. Credibility shrinks toward the
prior mean by `min(1, n / 10)`; the gate uses raw posterior_mean
(not the credibility-shrunk effective score) to inspect the right
tail directly. Implementation: `scripts/per_surface_bayesian_rollup.py`
(mg-d26d). Beta inverse-CDF is implemented from scratch via Numerical
Recipes Lentz βCF + bisection — no scipy dependency.

For mg-d26d, 16,723 v8 substrate paired records + 4,832 v9 substrate
signature records = 21,555 paired records were aggregated across 408
distinct substrate surfaces.

### 2.8 The right-tail Bayesian gate

The acceptance gate is a one-tail Mann-Whitney U test on the top-K
substrate posterior means versus the top-K matched-control posterior
means, ranked by raw posterior_mean. K=20 is the production value
(K=5/10/20 sweep run as a sensitivity diagnostic in mg-c216). The
PASS condition is **p < 0.05 with median(substrate top-K) >
median(control top-K)**. Pre-registered: a one-tail one-sided test
with substrate predicted to dominate. The gate is permissive in the
sense that it asks only that the *best* substrate surfaces beat the
*best* control surfaces, not that the bulk distributions separate;
this is by design, since the v9 generator's projection bias produces
a bulk distribution dominated by short over-projected roots
(mg-bef2).

### 2.9 Cross-LM, cross-window-coherence, and pollution checks

Five auxiliary checks were pre-registered against the v10 outcome:

- **Cross-substrate negative control** (mg-0f97). Re-route each pool's
  paired-difference records through the *other* substrate's LM
  (Aquitanian under Etruscan LM, Etruscan under Basque LM) and re-run
  the gate. If the v10 PASS reflects substrate-LM-specific signal, the
  cross-LM gate should collapse.
- **Third-LM check** (mg-4664). Re-route Aquitanian and Etruscan
  records through the Mycenaean-Greek LM (genuinely unrelated to both
  substrates) and re-run the gate. Cross-checks whether a partial
  cross-LM result reflects a Mediterranean-phonotactic kinship
  artefact versus a generic natural-language-LM bias.
- **Linear-B sister-syllabary positive control** (mg-4664). Promote
  20 Ventris-Chadwick carryover anchors plus Younger 2000
  conjecturals into a first-class substrate pool, score under the
  Mycenaean-Greek LM. If the framework can recover known-correct
  readings, the positive control passes; if not, it fails.
- **Cross-window coherence test** (mg-c216). For each v10 top-20
  substrate surface, build a per-sign histogram of the phoneme
  proposed by every positive-paired-difference candidate equation
  involving that surface; compute the modal-phoneme posterior and
  Shannon entropy per sign; compute per-surface coherence as
  `Σ_s [freq(S, s) · P_modal(s)] / Σ_s freq(S, s)`. Acceptance bar:
  median per-surface coherence ≥ 0.6 on at least one pool.
- **Pollution tests** (mg-6b73, mg-7ecb). Build a 50%-polluted
  Aquitanian pool (153 real + 153 same-distribution conjecturals,
  mg-6b73) and a cross-language polluted pool (153 real + 153
  Mycenaean-Greek-shape conjecturals, mg-7ecb); rerun the v10 gate
  on each. Tests whether the gate signal depends on uniformly-clean
  substrate pools or on a substrate-specific phonotactic shape.

---

## 3. Results

### 3.1 Acceptance-gate outcomes — summary table

The eleven pre-registered gates / pre-specified tests and their
outcomes are (gates 1–7 form the original v15-shape pre-registration;
gates 8–11 were added by v18–v20 follow-on tickets within the same
pre-registered scoring discipline):

| # | test | ticket | result | outcome |
|---:|:--|:--|:--|:--|
| 1 | own-LM right-tail bayesian gate, three substrate pools | mg-d26d (v10) | Aquitanian p = 3.22e-05; Etruscan p = 5.21e-04; Toponym p = 0.92 | **2/3 PASS** |
| 2 | cross-substrate negative control | mg-0f97 (v11) | Etruscan under Basque LM p = 0.591 (FAIL → validates); Aquitanian under Etruscan LM p = 0.0205 (partial PASS) | Etruscan validated; Aquitanian partial |
| 3 | third-LM (Mycenaean Greek) check | mg-4664 (v12) | Aquitanian p = 0.0953 (FAIL); Etruscan p = 0.185 (FAIL) | substrate-LM-specificity confirmed |
| 4 | Linear-B sister-syllabary positive control | mg-4664 (v12) | own-LM p = 0.155 at K=20 (FAIL); K=5 sensitivity p = 0.0106 (PASS) | positive control fails the production gate; passes a less-conservative gate |
| 5 | per-sign cross-window coherence | mg-c216 (v13) | median 0.1818 (Aquitanian), 0.1808 (Etruscan), bar 0.6 | **decisive FAIL** |
| 6 | same-distribution pollution test | mg-6b73 (v14) | polluted-pool gate p = 2.74e-05 (PASS); within-tail real-vs-conjectural Mann-Whitney p = 0.98 | gate PASS; framework cannot distinguish real from same-distribution conjectural |
| 7 | cross-language pollution test | mg-7ecb (v15) | polluted-pool gate p = 2.01e-03 (PASS); within-tail real-vs-conjectural-greek p = 8.29e-05 | partial within-tail discrimination |
| 8 | toponym pool, bigram-preserving control | mg-9f18 (v18) | gate p = 9.99e-05 (PASS) under bigram control vs p = 0.92 (FAIL) under v6 unigram control | toponym validated; v10 failure was a control-sampler artifact (see §3.10) |
| 9 | pollution-level sweep (10/25/50/75% same-distribution) | mg-9f18 (v18) | all four PASS; p = 1.5e-04 / 2.7e-04 / 2.7e-05 / 4.3e-02 | gate insensitive to pollution share within substrate distribution; threshold (if any) sits beyond 75% (see §3.11) |
| 10 | per-inscription cascade-candidate test on right-tail / short / known-content populations | mg-3438 (v19) | 3 cascade candidates emerged: `KH 10` (robust frac 0.55), `KH 5` (0.50), `PS Za 2` (0.71) | local-vs-global aggregate gap genuine; per-inscription internal consensus does not imply external correctness (see §3.12) |
| 11 | external validation against scholarly proposals (libation formula on `PS Za 2`; KU-RO / KI-RO on `KH 10` / `KH 5`) | mg-3438 (v19), mg-711c (v20) | `PS Za 2` AB57-AB31-AB31-AB60-AB13 mechanical `th-u-u-n-i` vs scholarly `ja-sa-sa-ra-me`: **0/5 consonantal-segment match**; `KH 10` and `KH 5` contain no AB81-AB02 (KU-RO) or AB67-AB02 (KI-RO) sequences (no comparable substring available) | **decisive negative external validation** where comparand exists; targeted search for additional comparands returns null (see §3.13) |

All eleven outcomes are reproducible from
`results/rollup.bayesian_posterior.*.md`, the supporting provenance
breakdowns in `results/rollup.bayesian_posterior.*.provenance.md`,
`results/consensus_sign_phoneme_map.md`, and
`results/rollup.per_inscription_coherence.md`. The detailed per-pool
breakdowns follow.

### 3.2 Validation status by pool

The validation matrix as of v20 (no pool-level changes since v18;
v19 / v20 operate at the per-inscription level documented in
§3.12 / §3.13 rather than altering pool-level gate outcomes):

| pool | own-LM (v10/mg-d26d) | cross-LM (v11/mg-0f97) | third-LM (v12/mg-4664, MycGreek) | curation gate (v14/v15) | bigram control (v18/mg-9f18) | status |
|:--|:--:|:--:|:--:|:--:|:--:|:--|
| `aquitanian` | PASS p = 3.22e-05 (basque) | partial p = 0.0205 (etruscan, 5× weaker) | FAIL p = 0.0953 | (see polluted variants) | n/a (v6 unigram control already PASSes) | substrate-LM-specific against unrelated LMs; partial Mediterranean-phonotactic kinship under etruscan LM |
| `polluted_aquitanian` | n/a (v14 build) | n/a | n/a | **PASS p = 2.74e-05** (basque, 50% same-distribution pollution) | n/a | gate is curation-tolerant; top-20 split 9 real / 11 conjectural; within-tail real-vs-conjectural Mann-Whitney p = 0.98 |
| `polluted_aquitanian_{10,25,75}pct` | n/a (v18 build) | n/a | n/a | **PASS** at all three levels (1.5e-04 / 2.7e-04 / 4.3e-02) | n/a | v18 sweep characterizes the gate's curation-sensitivity gradient; see §3.11 |
| `greek_polluted_aquitanian` | n/a (v15 build) | n/a | n/a | **PASS p = 2.01e-03** (basque, 50% Mycenaean-Greek-shape pollution) | n/a | partial within-tail discrimination; top-20 split 13 real / 7 conjectural-greek; real-vs-conjectural-greek MW p = 8.29e-05 |
| `etruscan` | PASS p = 5.21e-04 (etruscan) | FAIL p = 0.591 (basque) | FAIL p = 0.185 (mycenaean_greek) | n/a | n/a (v6 unigram control already PASSes) | substrate-LM-specific; both unrelated LMs collapse the separation |
| `toponym` | FAIL p = 0.92 (v6 unigram control) | (skipped at v10) | (skipped at v10) | n/a | **PASS p = 9.99e-05** (v18 bigram control) | v10 failure was a control-sampler artifact; v18 validates against the stricter bigram null. See §3.10 |
| `linear_b_carryover` | n/a | n/a | **FAIL p = 0.155** at K=20 (mycenaean_greek own-LM positive control) | n/a | n/a | positive control fails production gate; K=5 sensitivity passes at p = 0.0106 |

### 3.3 Aquitanian and Etruscan: validated against unrelated LMs

The clean Aquitanian PASS (mg-d26d) is reproduced at
`results/rollup.bayesian_posterior.aquitanian.md`: top-20 substrate
posterior median 0.9808 versus top-20 matched-control median 0.9512,
Mann-Whitney U = 345.0, p = 3.22e-05. The Etruscan PASS is at
`results/rollup.bayesian_posterior.etruscan.md`: substrate median
0.9808 versus control median 0.9217, U = 321.0, p = 5.21e-04.

The cross-LM negative controls (mg-0f97) behave as expected for
substrate-specific signal:

| pool | own-LM | cross-LM | third-LM (MycGreek) |
|:--|:--:|:--:|:--:|
| `aquitanian` (medians) | sub 0.9808 / ctrl 0.9512, p = 3.22e-05 (basque) | sub 0.9808 / ctrl 0.9422, p = 0.0205 (etruscan) | sub 0.9808 / ctrl 0.9630, p = 0.0953 (mycgreek) |
| `etruscan` (medians) | sub 0.9808 / ctrl 0.9217, p = 5.21e-04 (etruscan) | sub 0.9615 / ctrl 0.9535, p = 0.591 (basque) | sub 0.9615 / ctrl 0.9498, p = 0.185 (mycgreek) |

Etruscan validates cleanly: the separation collapses under both
unrelated LMs (Basque p = 0.591, Mycenaean-Greek p = 0.185). The
Etruscan top-20 substrate surfaces are a coherent semantic stratum
of religious vocabulary, common praenomina, function words, and
time references — exactly the genre profile of the votive / funerary
corpus the pool was sourced from.

Aquitanian is more nuanced: the separation persists under the
Etruscan LM at p = 0.0205 but collapses under the Mycenaean-Greek LM
at p = 0.0953. The cross-LM pattern is most parsimoniously explained
as a Basque-Etruscan **Mediterranean phonotactic-kinship artefact**:
both languages share CV-syllable-dominant phonotactics with simple
consonant inventories, so Aquitanian roots match either LM's
character-bigram statistics partially. Mycenaean Greek has more
complex syllable structures (CVC, labiovelars, geminate clusters)
and Aquitanian roots no longer dominate the right tail under it.
The v10 Aquitanian PASS is therefore substrate-specific against
genuinely unrelated LMs but partially overlaps with closely-related
LMs.

### 3.4 Top-K substrate surfaces by pool

The v10 (mg-d26d) Bayesian-posterior leaderboards are committed at
`results/rollup.bayesian_posterior.{aquitanian,etruscan,toponym,
linear_b_carryover}.md`. The top-20 substrate surfaces by raw
posterior_mean reproduce a coherent semantic stratum on each
substrate pool:

**Aquitanian top-20 under the Basque LM** — a cross-section of
inherited core Basque vocabulary across the standard semantic
families (no family dominates):

| rank | surface | n | k | posterior_mean | semantic field |
|---:|:--|---:|---:|:--:|:--|
| 1 | `aitz` | 53 | 53 | 0.9818 | nature: rock |
| 2 | `hanna` | 51 | 51 | 0.9811 | kinship: brother |
| 3 | `nahi` | 51 | 51 | 0.9811 | function: desire |
| 4 | `ako` | 50 | 50 | 0.9808 | morphology: suffix |
| 5 | `beltz` | 50 | 50 | 0.9808 | descriptor: black |
| 6 | `bihotz` | 50 | 50 | 0.9808 | body: heart |
| 7 | `egun` | 50 | 50 | 0.9808 | time: day |
| 8 | `eki` | 50 | 50 | 0.9808 | nature: sun |
| 9 | `ezti` | 50 | 50 | 0.9808 | food: honey |
| 10 | `gaitz` | 50 | 50 | 0.9808 | descriptor: ill |
| 11 | `hau` | 50 | 50 | 0.9808 | function: this |
| 12 | `hesi` | 50 | 50 | 0.9808 | place: fence |
| 13 | `itsaso` | 50 | 50 | 0.9808 | nature: sea |
| 14 | `oin` | 50 | 50 | 0.9808 | body: foot |
| 15 | `ona` | 50 | 50 | 0.9808 | descriptor: good |
| 16 | `zelai` | 50 | 50 | 0.9808 | nature: meadow |
| 17 | `zortzi` | 50 | 50 | 0.9808 | number: eight |
| 18 | `argi` | 52 | 51 | 0.9630 | nature: light |
| 19 | `ate` | 51 | 50 | 0.9623 | dwelling: door |
| 20 | `entzun` | 50 | 49 | 0.9615 | function: hear |

**Etruscan top-20 under the Etruscan LM** — religious vocabulary,
praenomina, function words, time references:

| rank | surface | n | k | posterior_mean | gloss |
|---:|:--|---:|---:|:--:|:--|
| 1 | `larth` | 54 | 54 | 0.9821 | praenomen "Larth" |
| 2 | `aiser` | 52 | 52 | 0.9815 | "gods" |
| 3 | `matam` | 52 | 52 | 0.9815 | "above / before" |
| 4 | `avils` | 50 | 50 | 0.9808 | "of years" |
| 5 | `camthi` | 50 | 50 | 0.9808 | magistracy |
| 6 | `chimth` | 50 | 50 | 0.9808 | "at / near" |
| 7 | `hanthe` | 50 | 50 | 0.9808 | ritual position |
| 8 | `laris` | 50 | 50 | 0.9808 | praenomen "Laris" |
| 9 | `nac` | 50 | 50 | 0.9808 | "as / when" |
| 10 | `sech` | 50 | 50 | 0.9808 | "daughter" |
| 11 | `thana` | 50 | 50 | 0.9808 | praenomen "Thana" |
| 12 | `zelar` | 50 | 50 | 0.9808 | ritual time-reference |
| 13–20 | `caitim`, `thesan`, `spureri`, `thanchvil`, `suthi`, `mach`, `arnth`, `sath` | … | … | 0.9714–0.9808 | month-name, dawn-goddess, "sacrifice for the city", praenomen, "tomb / burial", numeral "five", praenomen, recurring stem |

**Toponym top-20 under the Basque LM (v18 bigram-control gate)** —
recognizable Aegean / Mediterranean place-names plus a handful of
toponym-stem fragments (the bigram-control gate replaces the v6
unigram-control surfaces in the right tail; substrate surfaces
themselves are the v10 leaderboard):

| rank | surface | n | k | posterior_mean | identity / region |
|---:|:--|---:|---:|:--:|:--|
| 1 | `aksos` | 50 | 50 | 0.9808 | Crete (Axos) |
| 2 | `aso` | 50 | 50 | 0.9808 | toponym-stem |
| 3 | `assos` | 50 | 50 | 0.9808 | Aeolis (Assos) |
| 4 | `kno` | 50 | 50 | 0.9808 | Crete (Knossos stem) |
| 5 | `lukia` | 50 | 50 | 0.9808 | Anatolia (Lycia) |
| 6 | `tarra` | 50 | 50 | 0.9808 | Crete (Tarrha) |
| 7 | `ala` | 50 | 49 | 0.9615 | toponym-stem |
| 8 | `iassos` | 24 | 24 | 0.9615 | Caria (Iassos) |
| 9 | `itanos` | 24 | 24 | 0.9615 | Crete (Itanos) |
| 10 | `keos` | 50 | 49 | 0.9615 | Cyclades (Keos) |
| 11 | `lebena` | 24 | 24 | 0.9615 | Crete (Lebena) |
| 12 | `naxos` | 24 | 24 | 0.9615 | Cyclades (Naxos) |
| 13 | `andos` | 50 | 48 | 0.9423 | toponym-stem |
| 14 | `minoa` | 50 | 48 | 0.9423 | Crete (Minoa) |
| 15 | `kuzikos` | 13 | 13 | 0.9333 | Mysia (Kyzikos) |
| 16 | `mnos` | 50 | 46 | 0.9038 | toponym-stem |
| 17 | `aspendos` | 8 | 8 | 0.9000 | Pamphylia (Aspendos) |
| 18 | `tenos` | 50 | 45 | 0.8846 | Cyclades (Tenos) |
| 19 | `aios` | 50 | 44 | 0.8654 | toponym-stem |
| 20 | `lykabettos` | 5 | 5 | 0.8571 | Athens (Lykabettos) |

The control top-20 on all three pools is the random-phonotactic
noise floor (no semantic coherence). Full leaderboards in
`results/rollup.bayesian_posterior.aquitanian.md`,
`results/rollup.bayesian_posterior.etruscan.md`, and
`results/rollup.bayesian_posterior.toponym_bigram_control.md`.

### 3.5 Toponym: validated under bigram-preserving control (v18)

The toponym pool fails the v10 right-tail gate at p = 0.92 under
the v6 unigram-marginal matched control
(`results/rollup.bayesian_posterior.toponym.md`: substrate top-20
median 0.9186, control top-20 median 0.9464, U = 149.5). The
substrate top recovers recognizable Aegean toponyms (`dikte`, `keos`,
`kno`, `minoa`, `tenos`, `iassos`, `lemnos`, `kuzikos`, `melitos`,
`tulisos`, `melos`, `aspendos`, `kalumnos`, `zakuntos`, `lukia`,
`mukenai`, `lykabettos`, `itanos`, `halikarnassos`, `poikilassos`),
but the matched-control surfaces (`eoao`, `aathei`, `ana`, `eta`,
`ioonaol`, etc.) sit at higher posteriors. The v6 unigram sampler
draws each phoneme independently from the substrate's marginal
histogram, which can produce arbitrarily extreme phonotactic
violations as long as the inventory is matched; those violations
score well under the LM by raw phoneme-frequency overlap.

v18 (mg-9f18, §3.10) re-runs the gate against a bigram-preserving
matched control (`scripts/build_control_pools.py --sampler bigram`,
alpha = 0.1). Under the bigram null, the toponym pool **PASSes** at
p = 9.99e-05 (substrate top-20 median 0.9615, control top-20
median 0.8525, U = 337.5). The v10 failure is therefore a control-
sampler artifact: tightening the control to match adjacent-phoneme
structure (CV transitions, vowel hiatus rates) eliminates the
extreme-phonotactics-but-frequency-matched controls (`eoao` →
`akaintha`, `aathei` → `inaletos`, etc.), and the substrate signal
clears the right-tail comparison cleanly. The toponym pool joins
Aquitanian and Etruscan as a third validated cross-LM-checkable
pool. Full breakdown:
`results/rollup.bayesian_posterior.toponym_bigram_control.md`.

### 3.6 Linear-B carryover: positive control failed at the production gate

`results/rollup.bayesian_posterior.linear_b_carryover.md` reports
the K=20 own-LM gate at p = 0.155 (n_substrate_top = 12,
n_control_top = 11, MW U = 83). The substrate top-20 median is
0.7500 and the control median is 0.3103, so the directionality and
the magnitude of separation are correct, but the population MW U
does not cross p < 0.05. The leaderboard explains why: the
**well-attested anchors** (`mate`, `tare`, `kiro`, `kuro`) decisively
clear their controls (substrate posterior 0.85–0.98), but the
**conjectural anchors** (`dare`, `dina`, `ara`, `taina`, `kumina`)
do not separate from random Mycenaean-Greek-phonotactic strings.
`dare` (curator-flagged "libation-formula continuation") loses
50/50 paired records (k = 0).

The K-sweep diagnostic (mg-c216) shows the gate is partially over-
conservative on this mixed-cleanness pool:

| K | n_substrate_top | n_control_top | median sub | median ctrl | MW U | p (one-tail) | gate |
|---:|---:|---:|:--:|:--:|---:|:--:|:--:|
| 5 | 5 | 5 | 0.8846 | 0.5772 | 24.0 | **0.0106** | PASS |
| 10 | 10 | 10 | 0.7692 | 0.3552 | 71.0 | 0.0603 | borderline |
| 20 | 12 | 11 | 0.7500 | 0.3103 | 83.0 | 0.1547 | FAIL |

K=5 cleanly clears p<0.05. The production gate fails because the
K=20 substrate top is forced to include the conjectural drag.

### 3.7 Cross-window coherence: per-sign mappings are not stable

For each v10 top-20 substrate surface (Aquitanian + Etruscan, 40
surfaces total), the consensus map (mg-c216,
`results/consensus_sign_phoneme_map.md`) aggregates positive-
paired-difference candidate equations and reports the histogram of
phonemes proposed for each Linear A sign. Of 61 distinct Linear A
signs receiving at least one positive proposal, 60 cleared the
n_proposals ≥ 10 threshold. The headline coherence verdict:

| pool | n_surfaces | n_with_coherence | median | min | max | gate (≥0.6) |
|:--|---:|---:|:--:|:--:|:--:|:--:|
| `aquitanian` | 20 | 20 | 0.1818 | 0.1805 | 0.1864 | **FAIL** |
| `etruscan` | 20 | 20 | 0.1808 | 0.1739 | 0.1867 | **FAIL** |

Both pools fail decisively. The coherence values cluster tightly in
[0.17, 0.19] — far below the 0.6 acceptance bar, far below even the
"close-but-no-cigar" 0.5–0.55 region. Every consensus-map sign has
entropy ≥ 2.05 bits (out of log₂(23) ≈ 4.52 bits maximum), and
**no sign reaches modal posterior > 0.27**. The five most-coherent
signs (the lowest-entropy end of the distribution) are still very
diffuse:

| sign | n_proposals | modal | modal_posterior | entropy_bits |
|:--|---:|:--:|:--:|:--:|
| `A718` | 12 | `i` | 0.234 | 2.055 |
| `AB13` | 26 | `i` | 0.227 | 2.998 |
| `A306` | 14 | `i` | 0.137 | 3.039 |
| `AB66` | 15 | `i` | 0.132 | 3.057 |
| `A323` | 14 | `a` | 0.176 | 3.093 |

High-frequency signs (which receive proposals from essentially the
entire v10 top-20) are uniformly diffuse: AB08 (464 proposals,
modal `a` posterior 0.167, entropy 3.925 bits), AB37 (227 proposals,
modal `i` posterior 0.187, entropy 3.713 bits), AB28 (225 proposals,
modal `i` posterior 0.159, entropy 3.788 bits). The structural
reason: the metric rewards substrate-phonotactic match broadly
rather than specific sign-to-phoneme assignments, so different
substrate roots aligning with the same Linear A window propose
different sign mappings, and all of them score positive
paired-differences.

### 3.8 Pollution tests: gate is curation-tolerant; within-tail discrimination is partial

The v10 right-tail gate's response to deliberate pool pollution:

| pool | gate p | top sub median | top ctrl median | within-tail real-vs-conjectural Mann-Whitney p |
|:--|:--:|:--:|:--:|:--:|
| `aquitanian` (clean, v10) | 3.22e-05 | 0.9808 | 0.9512 | n/a (no conjecturals) |
| `polluted_aquitanian` (v14, 50% same-distribution conjectural) | 2.74e-05 | 0.9808 | 0.9572 | 0.98 (no within-tail discrimination) |
| `greek_polluted_aquitanian` (v15, 50% Mycenaean-Greek-shape conjectural) | 2.01e-03 | 0.9808 | 0.9735 | 8.29e-05 (strong within-tail discrimination) |

The same-distribution polluted gate (mg-6b73,
`results/rollup.bayesian_posterior.polluted_aquitanian.md`) is
within ~1.2× of the clean Aquitanian gate. The provenance breakdown
of the polluted-pool top-20 is **9 real / 11 conjectural** (~50/50,
matching the underlying pool); the within-tail Mann-Whitney
real-vs-conjectural test is essentially flat at p = 0.98 — the
framework **cannot distinguish real Aquitanian roots from
phonotactically-matched same-distribution conjecturals** within a
mixed pool.

The cross-language polluted gate (mg-7ecb,
`results/rollup.bayesian_posterior.greek_polluted_aquitanian.md`)
also PASSes, but ~70× weaker than the same-distribution gate and
~16× weaker than the clean gate. The provenance breakdown is
**13 real / 7 conjectural-greek** (a real-side bias of 65/35), and
the within-tail real-vs-conjectural-greek MW gives p = 8.29e-05 —
**strong within-tail discrimination**. The conjectural-greek
surfaces that did make the top-20 (`aki`, `ame`, `awa`, `fren`,
`ini`, `joten`, `kare`) share a Mediterranean-CV shape that the
Basque LM rewards heavily; the Greek-shape conjecturals that
fell out of the top-20 are heavier in distinctive features
(`j-` / `w-` glides, geminate clusters) that flag them as
out-of-distribution.

The control-side median rises monotonically from clean (0.9512)
through same-distribution polluted (0.9572) to cross-language
polluted (0.9735) — the matched-control sampler is sensitive to
the polluted pool's combined phoneme distribution. The substrate-
side median is the same 0.9808 in all three pools (cap-per-entry=50
ceiling). The shrinking substrate-vs-control gap is what produces
the weaker but still-PASSing gate under cross-language pollution.

### 3.9 Per-inscription concentration

Of 185 Linear A inscriptions in the working set, 43 have ≥ 1 v10
top-20 substrate surface with positive paired-difference evidence
on it, and 40 have ≥ 2 (mg-0f97,
`results/rollup.right_tail_inscription_concentration.md`). Top-by-
density inscriptions:

| rank | inscription | site | genre | n_top20 | n_records | density |
|---:|:--|:--|:--|---:|---:|---:|
| 1 | `HT Wc 3010` | Haghia Triada | accountancy | 14 | 76 | 0.184 |
| 2 | `HT Wc 3017a` | Haghia Triada | accountancy | 14 | 76 | 0.184 |
| 3 | `KH 60` | Khania | accountancy | 14 | 76 | 0.184 |
| 4 | `KN Zb 5` | Knossos | unknown | 14 | 76 | 0.184 |
| 5 | `HT 90` | Haghia Triada | accountancy | 14 | 94 | 0.149 |
| 6 | `KH 10` | Khania | accountancy | 14 | 100 | 0.140 |
| 7 | `KH 5` | Khania | accountancy | 14 | 110 | 0.127 |
| 8 | `HT 127a` | Haghia Triada | accountancy | 12 | 100 | 0.120 |
| 9 | `HT 12` | Haghia Triada | accountancy | 12 | 102 | 0.118 |
| 10 | `ARKH 6` | Arkhanes | accountancy | 10 | 85 | 0.118 |

The 14 v10-top-20 surfaces hitting these tablets are drawn from
**both** substrate pools' top-20 sets. The Etruscan-side
contribution is dominated by religious / praenomen / time-reference
vocabulary (`aiser`, `avils`, `camthi`, `hanthe`, `laris`, `matam`,
`thesan`, `zelar`, plus `caitim` / `thanchvil` / `spureri` on the
Knossos votive subset). The Aquitanian-side contribution is core
Basque vocabulary (`bihotz`, `entzun`, `hanna`, `itsaso`, `zelai`,
`zortzi`).

A second inscription cluster (`GO Wc 1a`, `ARKH 5`, `HT 104`,
`HT 103`, `ARKH 2`, etc.) shows 23–38 distinct top-20 surfaces, with
broader Aquitanian-side participation (`aitz`, `ako`, `ate`, `eki`,
`hau`, `oin`, `ona`, `argi`, `nahi`).

These per-inscription concentration patterns are reproducible and
indicate which Linear A tablets respond most strongly to the
substrate-aggregate signal. They do **not** indicate readability
under any specific substrate (see §3.7 and §4).

### 3.10 Toponym pool re-evaluation under bigram-preserving control sampler

v18 (mg-9f18) re-evaluates the toponym pool against a bigram-
preserving matched control. The v10 toponym failure (§3.5,
p = 0.92 under the v6 unigram-marginal control) was driven by
control surfaces like `eoao`, `aathei`, `kllzua` — phonotactically
extreme strings that the Basque LM scored well by raw phoneme-
frequency match. The v18 sampler
(`scripts/build_control_pools.py --sampler bigram`, alpha = 0.1)
draws each phoneme conditional on the previous phoneme using the
substrate's bigram counts, replacing those extremes with surfaces
like `akaintha`, `inaletos`, `metosord`.

Under the bigram-preserving control, the toponym pool **PASSes**
(p = 9.99e-05, MW U = 337.5; full results in
`results/rollup.bayesian_posterior.toponym_bigram_control.md`):

| variant            | substrate top-K | control top-K | median(top sub) | median(top ctrl) | MW U  | MW p (one-tail) | gate |
|:-------------------|---:|---:|---:|---:|---:|---:|:--:|
| bigram (v18)       | 20 | 20 | 0.9615 | 0.8525 | 337.5 | 9.988e-05 | PASS |
| unigram (v6/v10)   | 20 | 20 | 0.9186 | 0.9464 | 149.5 | 9.165e-01 | FAIL |

The control median drops 0.094 (0.946 → 0.852) under the bigram
sampler while the substrate median rises 0.043 (0.919 → 0.962);
every one of the v6 control's top-20 surfaces is absent from the
v18 control's top-20. The v10 toponym failure is therefore
attributable to control-sampler choice (an artifact of the
unigram-marginal sampler producing phonotactically improbable
surfaces with high LM-likelihood), not to a deficiency in the
substrate signal. The toponym pool joins Aquitanian and Etruscan
as a third validated pool.

What this does not mean: the bigram sampler is the strictest
control we test, but not the strictest defensible. Higher-order
controls (trigram, position-aware) would tighten further; matching
all of them would absorb the substrate signal entirely
(`pools/control_toponym_bigram.README.md` "What the control is
NOT"). The v18 result is a validation of the toponym pool against
a bigram-phonotactic null hypothesis — strictly stronger than the
v6 unigram-phonotactic null — and is consistent with the §3.4
substrate-LM-phonotactic-kinship reading.

### 3.11 Pollution-level sweep on Aquitanian (10%/25%/50%/75%)

v18 (mg-9f18) characterizes how the right-tail bayesian gate's
p-value scales with same-distribution conjectural pollution.
v14 (§3.8, mg-6b73) tested 50% pollution and PASSed at v10 magnitude;
the polecat's documented question — "is the gate essentially
insensitive to pollution within the same phoneme-distribution
shape, or is there a sharp threshold (e.g., 90% pollution)?" — is
the gradient v18 measures. Per
`results/rollup.pollution_level_sweep.md`:

| pollution % | n_real | n_conj | median(top sub) | median(top ctrl) | MW U  | MW p       | gate | top-K real | top-K conj |
|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|
| 10 | 153 | 17  | 0.9808 | 0.9450 | 325.5 | 1.502e-04 | PASS | 19 | 1  |
| 25 | 153 | 51  | 0.9808 | 0.9379 | 320.0 | 2.747e-04 | PASS | 12 | 8  |
| 50 | 153 | 153 | 0.9808 | 0.9572 | 340.0 | 2.740e-05 | PASS |  9 | 11 |
| 75 | 153 | 459 | 0.9808 | 0.9703 | 260.0 | 4.268e-02 | PASS |  5 | 15 |

The 50% row reproduces v14 (p = 2.740e-05) within sampling noise,
sanity-checking the v18 sweep code path against the v10/v14 path.

**Two readings.** At the gate level, every level PASSes; the
p-value at 75% (0.043) is close to but below the 0.05 threshold,
and the trend across 50% → 75% suggests the threshold (if any)
sits beyond 75% rather than at a sharp boundary inside the
gradient. v14's reading — that the framework's PASS at the
population level is driven by phonotactic-distribution-shape match
rather than by the fraction of surfaces that are real substrate
vocabulary — generalizes across the gradient.

At the top-K composition level, the substrate top-K shifts from
real-dominated at 10% (19/20 real) to conjectural-dominated at 75%
(5/20 real). Real surfaces remain near the maximum-posterior
ceiling regardless of pollution level (`median(top substrate)`
stays at 0.9808 across all four rows), but conjectural surfaces
with high-credibility wins crowd into the right tail as the
conjectural pool grows. Any reading of "the framework
discriminates real vs conjectural at the top-K level" needs to be
calibrated to the pollution level — at 10% pollution it does
(19/20 real); at 75% it does not (5/20 real).

**Threshold characterization (negative).** The sweep does not
locate a fail threshold within 10% – 75%. Locating one would need
finer sweep granularity (e.g. 85%, 90%, 95% rows); deferred. The
methodologically clean statement: *the v10 right-tail gate PASSes
at every same-distribution pollution level we tested, with
p-value at 75% close to but below the 0.05 threshold; same-
distribution pollution at higher conjectural shares may eventually
break the gate but the precise threshold is not located by this
sweep.*

### 3.12 Per-inscription coherence: cascade candidates

v19 (mg-3438,
`results/rollup.per_inscription_coherence.md`) asks the
*per-inscription* counterpart of v13's per-surface coherence
question: for a given Linear A inscription I, do the multiple
substrate candidates that target I agree on what each sign in I
should be?

The test aggregates all positive-paired-diff candidate equations
(across the three validated pools — Aquitanian, Etruscan,
toponym) targeting each inscription, computes a per-inscription
modal-phoneme posterior under local Dirichlet smoothing for every
sign in I, and reports the per-token *robust* fraction
(modal_posterior > 0.5 AND n_proposals ≥ 2) plus the *literal*
fraction (no n_proposals minimum) for transparency. Three
populations are evaluated: A — the top-30 v10 right-tail-
concentration inscriptions (mg-0f97); B — short inscriptions
(n_signs ≤ 5) capped at top-30 by candidate count; C — the
inscriptions whose token sequence contains the libation-formula
syllabogram run AB57-AB31-AB31-AB60-AB13 (`JA-SA-SA-RA-ME`).

**Cascade candidates** (robust fraction ≥ 0.5):

| inscription | site | population | robust fraction | mechanical reading |
|:--|:--|:--|---:|:--|
| `KH 10`   | Khania  | A | 0.5455 | `s-e-n-i-u-r-(a)-(e)-(l)-(a)-(a)` |
| `KH 5`    | Khania  | A | 0.5000 | `(s)-(a)-(l)-(a)-(a)-(s)-e-n-(a)-z-t-t-a-z-a-l-a-·-·-·` |
| `PS Za 2` | Psykhro | C | 0.7143 | `c-e-a-(ch)-th-(ch)-th-u-u-n-i-(l)-a-(l)` |

Two **partial cascades** (robust fraction in [0.25, 0.5)):
`HT 95a` (0.32) and `HT 31` (0.33). The literal-vs-robust gap on
the partial cascades arises because most signs that pass the
literal threshold are lone-proposal signs (n=1, modal_posterior =
1.0 trivially) — the robust filter catches that.

Population breakdown by classification (robust statistic):

| population | n inscriptions | cascade | partial | noise |
|:--|---:|---:|---:|---:|
| A: top-30 right-tail | 30 | 2 | 2 | 26 |
| B: short ≤5 signs    |  4 | 0 | 0 |  4 |
| C: libation formula  |  1 | 1 | 0 |  0 |

**Local-vs-global aggregate gap.** v13's per-surface coherence
median was 0.18 (against a 0.6 bar) — across all the windows where
each top-20 substrate surface was used, the proposed sign-to-
phoneme mappings disagreed heavily. v19 is local rather than
global: instead of asking "do the candidate equations using
surface S agree on what sign s should be?" it asks "do the
multiple substrate surfaces hitting inscription I agree on what
each sign in I should be?" The local-vs-global gap is genuine —
three of 35 evaluated inscriptions yield internal-consensus
cascade candidates — but, as §3.13 documents, internal consensus
does not by itself constitute decipherment evidence and on the
one cascade candidate that admits external comparison the
mechanical reading diverges from the scholarly proposal.

The cascade candidates are hypotheses for domain-expert review
(an Aegean-syllabary specialist), not decipherment claims. The
framework's surviving candidates agree on each cascade-candidate
inscription because the signs in those inscriptions have
phonotactic shapes consistent with the substrate-LM expectations
— not because the agreed-upon phoneme mappings correspond to the
historically-attested Linear A values.

### 3.13 External validation against scholarly proposals

v19's per-inscription cascade-candidate test (§3.12) is the first
result in the project that admits *external* validation: against
a scholarly proposal independent of the framework's own pipeline,
not against another mechanical artefact of that pipeline. v20
(mg-711c) consolidates the available external comparands —
`PS Za 2` from v19's population C, plus a targeted follow-up
search for additional comparable AB-sequences in `KH 10` and
`KH 5` — and reports the joint result.

#### 3.13.1 PS Za 2 vs the libation formula `ja-sa-sa-ra-me`

The Linear A libation formula, attested across multiple votive
contexts, has a long-standing scholarly transliteration
`ja-sa-sa-ra-me` (Younger 2000–; Davis 2014; cf. broader
Aegean-syllabary literature) on the syllabogram run
AB57-AB31-AB31-AB60-AB13. On `PS Za 2` (Psykhro, votive),
v19's per-inscription mechanical modal phonemes for that span
are `th-u-u-n-i`. Sign-by-sign:

| AB-sign | scholarly | mechanical (v19) | match (consonantal segment) |
|:--|:--:|:--:|:--:|
| AB57 | `ja` (j) | `th` | ✗ |
| AB31 | `sa` (s) | `u`  | ✗ |
| AB31 | `sa` (s) | `u`  | ✗ |
| AB60 | `ra` (r) | `n`  | ✗ |
| AB13 | `me` (m) | `i`  | ✗ |

The mechanical reading **diverges from the scholarly proposal on
every formula-span sign** (0/5 consonantal-segment match). All
five mechanical phonemes meet the robust threshold (modal posterior
> 0.5 with n_proposals ≥ 2) on this inscription, so the divergence
cannot be attributed to thin local data — the cascade candidate
*confidently* reads against the scholarly proposal.

#### 3.13.2 KH 10 / KH 5 vs accountancy totals `ku-ro` and `ki-ro` (v20 follow-up)

The other two cascade candidates — `KH 10` and `KH 5`, both
Khania accountancy tablets — admit a different external
comparand. Linear A accountancy is the most-attested genre with
scholarly translit-anchors: the totaling word `ku-ro` (Younger
2020; Schoep 2002 ch. 4; Palmer 1995) and the deficit word
`ki-ro` (Younger 2020; Palmer 1995) appear in dozens of tablets
at line-ends or section-ends. Under the Ventris-Chadwick 1956
carryover values incorporated as scholarly anchors in the
project's `linear_b_carryover` pool: `ku` = AB81, `ki` = AB67,
`ro` = AB02. So the canonical AB-sign sequences are:

- KU-RO = **AB81-AB02**
- KI-RO = **AB67-AB02**

v20 (mg-711c) inspects `KH 10` and `KH 5` for these subsequences
in their syllabogram-only token streams (logograms `LOG:*` and
divider tokens `DIV` excluded, matching v19's per-inscription
scoring path):

| inscription | syllabogram run |
|:--|:--|
| `KH 10` | AB28-AB03-AB31-AB57-AB16-AB118-AB08-AB67-AB39-AB38-AB04 |
| `KH 5`  | AB08-AB01-AB67-AB41-AB77-AB08-AB60-AB10-AB01-AB40-AB31-AB31-AB24-AB40-AB06-AB51-AB06-AB81-AB03-AB79 |

| sequence searched | KH 10 | KH 5 | result |
|:--|:--:|:--:|:--|
| AB81-AB02 (canonical KU-RO) | absent (AB81 not present) | absent (AB81 → AB03, not AB02) | **no match either tablet** |
| AB67-AB02 (canonical KI-RO) | absent (AB67 → AB39) | absent (AB67 → AB41) | **no match either tablet** |

AB02 itself is absent from both inscriptions. AB81 occurs once in
`KH 5` (followed by AB03); AB67 occurs once in each tablet
(followed by AB39 in `KH 10`, AB41 in `KH 5`). No KU-RO or
KI-RO instance is therefore available to compare to v19's
mechanical readings on these two cascade candidates.

*Tension flagged.* The mg-711c ticket text gave KU-RO and KI-RO
as AB81-AB60 and AB67-AB60 respectively — these are typos in the
ticket. AB60 is the canonical scholarly value for `ra` (visible
on the libation-formula span AB57-AB31-AB31-AB60-AB13 above),
not `ro`. The canonical value for `ro` is AB02, as cited by the
project's own `linear_b_carryover` pool entries for `ku-ro` and
`ki-ro` (Younger 2020; Ventris-Chadwick 1956 carryover values).
For completeness v20 also searched the literal ticket-text
sequences AB81-AB60 and AB67-AB60: neither occurs in either
inscription either (AB81 in `KH 5` is followed by AB03, not
AB60; AB67 in both tablets is followed by AB39 / AB41
respectively). So under either interpretation the §3.13.2
comparison set is **empty**.

#### 3.13.3 External-validation summary

The combined v19 + v20 external-validation evidence:

| comparand | inscription | scholarly span | mechanical span (v19) | match |
|:--|:--|:--|:--|:--:|
| libation formula `ja-sa-sa-ra-me` | `PS Za 2` | AB57-AB31-AB31-AB60-AB13 → j-s-s-r-m | `th-u-u-n-i` | **0/5** consonantal-segment |
| total `ku-ro` (AB81-AB02) | `KH 10`, `KH 5` | not present | not present | **n/a** (no comparand) |
| deficit `ki-ro` (AB67-AB02) | `KH 10`, `KH 5` | not present | not present | **n/a** (no comparand) |

The external-validation evidence to date is therefore one
mechanically-confident divergence (PS Za 2) and two attempted
follow-up comparisons that could not be performed for lack of a
comparable substring. Internal consensus across substrate
candidates does not imply external correctness on the one
inscription where the comparison is performable, and the
evidence base for that claim has not been broadened by the v20
follow-up — but neither has it been weakened. The supportable
local-level claim remains the v19 phrasing: *the framework's
mechanical consensus on the cascade candidates is a hypothesis,
not a reading; on the cascade candidate where independent
scholarly ground truth is available, the hypothesis is
mechanically confidently wrong.*

This refines rather than reverses the per-surface coherence
verdict (§3.7 / §5): per-sign decipherment remains unsupported
at the aggregate level (v13), and the only available local-level
comparison to a known-content scholarly proposal (v19 + v20)
shows divergence rather than corroboration. Both lines of
evidence — global aggregate (v13) AND local cascade-candidate
external check (v19 + v20) — point the same direction.

---

## 4. Discussion

### 4.1 What the framework detects

After v15, the supportable claim is sharper than at any earlier
point. The framework reliably detects three things:

- **Substrate-LM-phonotactic kinship at the population level.** The
  v10 right-tail gate clears for both Aquitanian (under the Basque
  LM) and Etruscan (under the Etruscan LM) at p < 0.001, and the
  separation collapses cleanly under genuinely unrelated LMs
  (Etruscan p = 0.591 under Basque, p = 0.185 under Mycenaean Greek;
  Aquitanian p = 0.0953 under Mycenaean Greek). The pattern is what
  one expects of substrate-specific signal: a real substrate's
  phonotactic profile is rewarded by the LM trained on that
  substrate's text and not by LMs trained on unrelated languages.
- **Curation tolerance within the same phoneme + length
  distribution.** The same-distribution polluted Aquitanian gate
  (50% conjectural, mg-6b73) PASSes at essentially the same magnitude
  as the clean gate (p = 2.74e-05 vs 3.22e-05). The signal does not
  depend on uniformly-clean substrate pools.
- **Partial within-tail shape selectivity.** Under cross-language
  pollution (50% Mycenaean-Greek-shape conjecturals, mg-7ecb), the
  population gate still PASSes (p = 2.01e-03) but ~70× weaker; and
  within the right tail, real Aquitanian dominates Greek-shape
  conjecturals at p = 8.29e-05. The framework therefore exhibits
  measurable shape selectivity below the population gate's
  resolution but above the leaderboard's.

The cleanest diagnostic for the boundary of the framework's
selectivity is the within-tail Mann-Whitney p-value across the two
pollution variants: 0.98 (no discrimination) under same-distribution
pollution → 8.29e-05 (strong discrimination) under cross-language
pollution. The distinguishing axis is whether the polluting
distribution matches the substrate's own marginal phoneme
distribution. When it does, conjecturals are statistically
indistinguishable from real surfaces; when it doesn't, they are
distinguishable.

### 4.2 What the framework does not detect

The framework fails at the per-sign decipherment level, and the
failure is empirical, not merely conservative:

- **No stable sign-to-phoneme map** (mg-c216). The cross-window
  coherence gate fails decisively on both v10-validated pools
  (median 0.18 versus a 0.6 bar). High-frequency Linear A signs
  receive proposals scattered across the entire phoneme alphabet
  (entropy 3.7–3.9 bits out of 4.5 bits maximum, no sign reaching
  modal posterior > 0.27). The proximate structural reason: the
  metric rewards substrate-phonotactic match broadly, so different
  substrate roots aligning with the same Linear A window propose
  different sign mappings and all of them score positive
  paired-differences.
- **No surface-level vocabulary identification within mixed pools**
  (mg-6b73). The same-distribution polluted gate cannot distinguish
  real Aquitanian roots from synthetic phonotactically-matched
  conjecturals (within-tail Mann-Whitney p = 0.98). Surfaces in the
  v10 top-K should be read as "Aquitanian-shaped surfaces the LM
  rewards consistently in the Linear A corpus" — not as "real
  Aquitanian roots the framework has identified in Linear A."

These two failures are coupled: without a stable per-sign
sign-to-phoneme map, "the framework identified surface X" cannot be
evidence about Linear A's specific lexical content; it can only be
evidence that surface X's phonotactic shape matches the Linear A
corpus's bigram statistics under the substrate's LM.

### 4.3 Why the gate PASSes under any same-distribution pollution

The clean Aquitanian gate's PASS is a population-level statement
about the right tail: top-K substrate surfaces beat top-K matched-
control surfaces. With the cap-per-entry = 50 generator setting,
many substrate surfaces saturate at posterior = 0.9808 (k = 50,
n = 50). When 153 conjecturals are added to the pool at the same
phoneme + length distribution, the conjecturals also generate
candidates that saturate at 0.9808; the new mass goes into the
substrate side of the gate without changing the substrate-side
median. The control side rises slightly because the matched-control
sampler's marginal distribution shifts modestly. Net: the
substrate-versus-control gap shrinks but stays positive, the gate
PASSes.

Under cross-language pollution (mg-7ecb), Greek-shape conjecturals
also saturate at 0.9808 *if* their bigrams happen to be Basque-LM-
favourable (the seven that landed in the top-20). The other Greek-
shape conjecturals carry distinctive features (`j-`, `w-`, geminate
clusters) that the Basque LM penalizes, so they don't saturate, and
the gate weakens — but not to FAIL.

### 4.4 Why per-sign coherence fails despite surface-aggregate PASS

The v10 PASS is a surface-aggregate statement about which substrate
roots the LM rewards consistently. That is mechanically distinct
from a *consistent* sign-to-phoneme assignment: the metric scores
the partial mapping perplexity of the substrate root's phoneme
stream against the sign window, and rewards configurations whose
character bigrams match the LM's bigram distribution. Many
substrate roots achieve that without agreeing on what any specific
Linear A sign should be. The high-frequency Linear A sign AB08, for
instance, is variously proposed as `a`, `e`, `h`, `z`, etc., by
different substrate surfaces' equations — and each of those
proposals contributes positive paired-difference evidence to its
own substrate surface. Surface-aggregate PASS and per-sign
incoherence are therefore both honest reports of what the metric
does at its respective resolution scales.

### 4.5 Implications for past Linear A decipherment claims

The methodology paper's central methodological warning is that
qualitative-impression ("this looks like Aquitanian") evidence
is **structurally equivalent** to the framework's surface-aggregate
PASS — and the surface-aggregate PASS, by mg-6b73, cannot
distinguish real substrate roots from phonotactically-matched
conjecturals. A past decipherment claim of the form "Linear A
inscription X reads Y in substrate language L" is no stronger than
the framework's surface-aggregate signal *unless* it presents
additional cross-window-coherence evidence at the per-sign level —
evidence that, on this corpus, this framework cannot recover.
Discipline of mechanical scoring against phonotactically-matched
controls is the protection against the motivated-reasoning failure
modes that have plagued Linear A studies historically.

### 4.6 Internal consensus does not imply external correctness

The methodology paper's headline external-validation result is the
v19 + v20 cascade-candidate finding (§3.12 / §3.13). It is the
project's first mechanical comparison of a framework reading to
a scholarly proposal *independent* of the framework's own
pipeline, and on the one inscription where the comparison is
performable (`PS Za 2`, libation-formula span AB57-AB31-AB31-
AB60-AB13) the framework's confidently-cascading mechanical
reading `th-u-u-n-i` diverges from the scholarly transliteration
`ja-sa-sa-ra-me` on every formula-span sign (0/5 consonantal-
segment match). v20's follow-up search for additional comparable
sequences (canonical KU-RO = AB81-AB02 and KI-RO = AB67-AB02)
in the other two cascade candidates `KH 10` and `KH 5` finds
neither sequence present, so the external-validation evidence
base remains a single comparable inscription. That is enough
to ground the load-bearing methodological claim:

> **Internal consensus among surviving substrate candidates does
> not imply external correctness.** A cascade candidate emerges
> when multiple independent substrate roots, having survived the
> right-tail and curation gates, agree on the same modal phoneme
> at most positions of an inscription. That agreement is
> evidence about the inscription's phonotactic shape under the
> substrate LMs; it is **not** evidence that the agreed-upon
> phonemes correspond to historically-attested Linear A values.
> Mechanical scoring against phonotactically-matched controls,
> followed by external comparison to scholarly ground truth, is
> what catches this distinction. Internal-consensus-only
> methodology — characteristic of past confirmatory-presentation
> Linear A work (§4.5, §1) — would not.

This is a discipline-protecting result. Without v19's external
comparison, the three cascade candidates `KH 10`, `KH 5`, and
`PS Za 2` would be the strongest "candidate readings" the
project has produced — exactly the motivated-reasoning failure
mode the paper's framing warned against. The mechanical
divergence on `PS Za 2`'s libation-formula span is therefore
not a setback but a verification that the methodology *catches
its own optimistic case*: the framework's surviving candidates
on a known-content inscription, when checked against scholarly
ground truth, are decisively wrong, and the framework is honest
enough about its own structure to surface that.

The result also tightens what the v10 / v18 PASSes mean.
Surface-aggregate PASS at the population level (Aquitanian,
Etruscan, toponym) detects substrate-LM-phonotactic kinship —
which the framework reports faithfully. Per-inscription
internal-consensus cascade candidates surface where that
phonotactic kinship concentrates within a single tablet —
which the framework also reports faithfully. *Neither* means
the framework has identified the correct phoneme assignment
for any specific Linear A sign, and the v19 + v20 external
validation makes that specific in a way that internal-only
metrics cannot.

---

## 5. Limitations

### 5.1 Out-of-scope by construction

- **Per-sign decipherment is not supported by the data.** The
  cross-window coherence gate fails decisively (§3.7); no specific
  sign-to-phoneme correspondence has been validated.
- **No specific Linear A inscription has a validated reading.** The
  per-inscription concentration patterns (§3.9) show which tablets
  respond strongly to the substrate-aggregate signal but do not
  adjudicate readability of any specific tablet under any specific
  substrate.
- **No claim of "Linear A is X" is supported.** The framework tests
  whether substrate roots beat matched controls in the right tail;
  it does not establish lexical identity between Linear A signs and
  substrate phonemes. The mechanical signal is consistent with
  multiple causal stories.
- **Per-inscription gloss generation was queued (originally v14) and
  failed at BOTH the aggregate AND the local cascade-candidate
  external-comparison level.** The mg-c216 cross-window coherence
  verdict (per-surface median 0.18 vs the 0.6 bar) ruled out
  per-surface reading-shape claims at the global aggregate level.
  v19 (mg-3438) re-opened the question at the LOCAL per-inscription
  level and found three cascade candidates (`KH 10`, `KH 5`,
  `PS Za 2`) where ≥ 50% of the signs in the inscription have ≥ 2
  substrate candidates agreeing on the same modal phoneme. v19's
  external comparison on `PS Za 2`'s libation-formula span
  AB57-AB31-AB31-AB60-AB13 (`ja-sa-sa-ra-me`) found the framework's
  mechanical consensus reads `th-u-u-n-i`, divergent on every
  formula-span sign (0/5 consonantal-segment match). v20 (mg-711c)
  searched the other two cascade candidates for additional
  comparable scholarly sequences — the well-attested accountancy
  totals `ku-ro` (AB81-AB02) and `ki-ro` (AB67-AB02) — and found
  no instance of either sequence in `KH 10` or `KH 5`. The
  external-validation evidence base is therefore a single
  comparable inscription with a confidently-divergent reading,
  with no successful corroborating comparand located by targeted
  follow-up. Both lines of evidence (global aggregate v13, local
  cascade-candidate external-comparison v19 + v20) support the
  same supportable-claim shape: per-sign decipherment is not
  established by this framework. *This does not constitute a
  decipherment.* The cascade candidates are hypotheses for
  domain-expert review, not decipherment claims; internal
  consensus among surviving candidates does not imply external
  correctness (§4.6).

### 5.2 Known unresolved issues

- **Linear-B positive control: K=20 production gate is over-
  conservative on mixed-cleanness pools.** The same pool clears at
  K=5 (p = 0.0106) but fails at K=20 (p = 0.155). Adopting a less-
  conservative gate would not change the v13 coherence verdict, so
  this is a methodology-paper observation rather than a load-bearing
  cleanup.
- **Per-window deduplication.** The 50-window cap-per-entry generator
  setting introduces minor per-(sign-set, inscription) duplication
  at rank 9–17 of some leaderboards (mg-f419 follow-up). Small
  effect; non-blocking.
- **Pollution-level threshold not localized.** v18's same-
  distribution sweep (§3.11) PASSes at every level 10%–75% with
  the 75% gate p sitting at 0.043 — close to but below the 0.05
  threshold. Locating the precise threshold (if any) at conjectural
  shares ≥ 75% would need finer sweep granularity; not load-bearing
  for the manuscript shape.
- **No second-corpus cross-validation.** All scoring is against the
  761-record SigLA snapshot. A GORILA / Younger 2000 ingest would
  add numerals and line-break information not in SigLA, expanding
  the corpus by ~10–15%; it has not been run.

### 5.3 Out-of-scope for this methodology characterization

Out of scope for the methodology paper but on the project's
follow-up surface:

- **Cross-language gates with other LMs** (Etruscan-shape pollution,
  Linear-B-shape pollution) — would localize which Mediterranean
  phonotactic features the gate is responding to.
- **Additional substrate pools** (Phoenician, Sumerian, Hattic) —
  the framework can in principle test any substrate hypothesis with
  attested vocabulary and a phoneme LM, but v15 made clear the
  framework does not produce decipherment-grade per-sign mappings on
  any substrate-language test it has run; expanding to more pools
  does not address the methodological limit.
- **Domain-expert review of top-K Aquitanian and Etruscan surfaces.**
  The only way to convert "the right tail is Aquitanian-shape-likely"
  into "the right tail is real Aquitanian vocabulary present in
  Linear A" is independent expert review by an Aegean-syllabary
  specialist.
- **Domain-expert review of v19 per-inscription cascade candidates.**
  The three cascade candidates `KH 10`, `KH 5`, and `PS Za 2`
  (§3.12) emerge with internal-consensus mechanical readings; on
  the one with a scholarly comparand (PS Za 2's libation formula),
  the mechanical reading diverges from the scholarly proposal
  (§3.13.1). v20 (mg-711c) searched `KH 10` and `KH 5` for the
  other two well-attested Linear A scholarly anchors (`ku-ro` =
  AB81-AB02, `ki-ro` = AB67-AB02) and found neither sequence
  present in either tablet (§3.13.2), so no further mechanical-
  vs-scholarly comparison was performable in v20's scope.
  Whether the framework's mechanical readings are correct on
  the cascade-candidate inscriptions where no scholarly comparand
  exists is a question only an Aegean-syllabary specialist can
  adjudicate. v19 + v20 surface the candidates honestly without
  drawing decipherment-shaped conclusions.
- **Deeper scholarly-source ingest.** v20 limited its scope to the
  two most-attested accountancy readings (KU-RO, KI-RO) plus the
  libation formula already in v19. A comprehensive scholarly-
  proposal database — Bonfante & Bonfante / Pallottino / Younger /
  Salgarella synthesised into a structured pool of well-attested
  Linear A AB-sequence-to-phoneme readings — would broaden the
  external-validation surface beyond the three sequences v19 + v20
  cover. Out of scope for this manuscript; tracked as follow-up.

---

## 6. Conclusion

A mechanical, falsifiable framework for testing substrate-language
hypotheses against Linear A — paired-difference scoring under
external phoneme language models with phonotactically-matched
controls, aggregated as per-surface Beta-binomial posteriors and
gated against a right-tail Mann-Whitney U test — detects substrate-
LM-phonotactic kinship at the population level for two of three
substrate hypotheses (Aquitanian under the Basque LM at p = 3.22e-05;
Etruscan under the Etruscan LM at p = 5.21e-04), under negative
controls that confirm substrate-LM specificity. The framework also
exhibits partial within-tail shape selectivity: under cross-language
pollution it discriminates real Aquitanian surfaces from Greek-shape
conjecturals at p = 8.29e-05.

The framework does **not** support per-sign decipherment claims.
A consensus sign-to-phoneme map built from the v10 top-20 substrate
surfaces fails a 0.6 cross-window-coherence bar decisively (median
0.18 on both validated pools). Same-distribution pollution tests
show the framework cannot distinguish real Aquitanian roots from
phonotactically-matched conjecturals within a mixed pool. And on
the project's first **external-validation** comparison — v19's
per-inscription cascade-candidate test, scoring the surviving
internal-consensus mechanical reading on `PS Za 2`'s libation-
formula span AB57-AB31-AB31-AB60-AB13 against the long-attested
scholarly transliteration `ja-sa-sa-ra-me` — the mechanical
consensus reads `th-u-u-n-i` (0/5 consonantal-segment match),
divergent from the scholarly proposal on every formula-span sign.
v20's targeted follow-up search for additional scholarly comparands
in the other two cascade candidates (`KH 10`, `KH 5`) — the
well-attested accountancy totals `ku-ro` (AB81-AB02) and `ki-ro`
(AB67-AB02) — finds neither sequence in either tablet, leaving the
libation formula as the project's sole external comparand to date.

The supportable claim is therefore strictly narrower than past
decipherment-shape claims for Linear A: the framework identifies
which substrate phonotactic profiles produce population-level signal
in the SigLA corpus, and on which specific inscriptions that signal
concentrates, but does not validate per-sign readings or per-tablet
glosses — and where the cascade candidates *do* admit external
comparison to scholarly ground truth, the mechanical reading
diverges. **Internal consensus among surviving substrate candidates
does not imply external correctness;** mechanical scoring against
phonotactically-matched controls, paired with external comparison
to independent scholarly proposals, is what distinguishes the
framework's claim from the qualitative-impression claims that have
plagued past Linear A work. The framework's null findings — no
per-sign coherence at the global aggregate level (v13), no
real-vs-conjectural surface discrimination at the same-distribution
pollution level (v14), and decisive divergence on the one
performable external comparison (v19 / v20) — are themselves
contributions to the methodological literature on undeciphered-
script analysis: each is a falsification result that internal-only
methodology, by construction, cannot produce.

---

## Appendix A: result-file index

Every quantitative claim in this document maps to one or more
committed artefacts under `results/`:

| claim source | committed file |
|:--|:--|
| v10 own-LM gate (Aquitanian, Etruscan, Toponym) | `rollup.bayesian_posterior.{aquitanian,etruscan,toponym}.md` |
| v11 cross-LM gate | `rollup.bayesian_posterior.{aquitanian_under_etruscan_lm,etruscan_under_basque_lm}.md` |
| v12 third-LM (Mycenaean Greek) gate | `rollup.bayesian_posterior.{aquitanian,etruscan}.under_mycenaean_greek_lm.md` |
| v12 Linear-B positive control | `rollup.bayesian_posterior.linear_b_carryover.md` |
| v13 consensus sign-to-phoneme map + per-pool coherence + K-sweep | `consensus_sign_phoneme_map.md` |
| v14 same-distribution pollution gate + provenance | `rollup.bayesian_posterior.polluted_aquitanian.md` + `…provenance.md` |
| v15 cross-language pollution gate + provenance | `rollup.bayesian_posterior.greek_polluted_aquitanian.md` + `…provenance.md` |
| per-inscription concentration | `rollup.right_tail_inscription_concentration.md` |
| v19 per-inscription coherence + cascade candidates | `rollup.per_inscription_coherence.md` |
| v20 KU-RO / KI-RO scholarly-anchor search on `KH 10` / `KH 5` | `corpus/Khania/KH%2010.json`, `corpus/Khania/KH%205.json` (token streams) + `pools/linear_b_carryover.yaml` (canonical AB-sequence anchors) |
| corpus ingestion record | `../corpus_status.md` |

Per-ticket merge notes are in `docs/findings.md` under
`## Findings from mg-XXXX` headers, in chronological order from
`mg-1c8c` (SigLA corpus ingest, 2026-05-04) through `mg-711c`
(v20, 2026-05-05); the harness pipeline itself spans `mg-d5ef`
(v0, 2026-05-04 first harness commit) through `mg-3438` (v19,
2026-05-05), with mg-711c (v20) a documentation-and-investigation
ticket that adds no harness code path. The repo scaffold
(`mg-9e00`) predates `findings.md`'s introduction in `mg-13a2`
and so does not have a per-ticket entry there.
