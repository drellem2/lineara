# Mechanical Falsifiable Testing of Substrate-Language Hypotheses for Linear A and Cretan Hieroglyphic

**Methodology paper draft (v16, mg-d5ed initial polish; lineage
citations corrected in v17, mg-2bfd; v19 cascade-candidate /
external-validation integration in v20, mg-711c; Eteocretan 4th-pool
integration in v21, mg-6ccd; population-level scholar-proposed-reading
external-validation integration in v22, mg-46d5; full Eteocretan
cross-LM matrix integration in v23, mg-b599; per-inscription
cascade-candidate analysis under Eteocretan LM in v24, mg-c103;
single-script consolidation pass in v25, mg-36bd; cross-script
extension to Cretan Hieroglyphic via the chic-v0..chic-v5 sub-program
(corpus ingest mg-99df, sign classification mg-c7e3 + mg-0ea1
backfill, paleographic anchor inheritance mg-362d, substrate
framework on CHIC mg-9700, cross-script correlation mg-c769, per-sign
syllable-value extraction framework mg-7c6d) integrated into the
extended methodology paper in chic-v7, mg-9508; CHIC-side mechanical-
verification pass against three external-scholarship sources in
chic-v6, mg-a557; Linear A-side companion mechanical-verification
pass at the leaderboard top-K granularity in v26, mg-c202; dual-
script bilingual analysis (Malia altar stone CHIC #328 verified
unilingual; 0 new tier-2 candidates derivable on v0 corpora) in
chic-v8, mg-dfcc; final cross-script polish pass integrating v26 +
chic-v8 for journal-submission handoff in v27, mg-b731;
**leave-one-out held-out validation of the chic-v5 framework on the
chic-v2 anchor pool yielding 20.0% aggregate recovery accuracy and
0/3 tier-2 unanimity correctly classified, downgrading the
credibility of chic-v5's three tier-2 candidate proposals** in
chic-v9, mg-18cb; methodology paper polish pass integrating
chic-v9 in chic-v10, mg-1178; **Linear A side analogous LOO
validation of the chic-v5 framework on LB-carryover anchors
yielding 33.3% aggregate accuracy (7/21) and 0/3 tier-2 unanimity
correctly classified, establishing that the framework's at-chance
per-sign behaviour is structural across both scripts rather than
CHIC-specific** in v28, mg-4a7b; **additional within-scope
evidence on the 3 chic-v5 tier-2 candidates (cross-pool L3
robustness check + #032 ku-pa context inspection) yielding an
asymmetric per-candidate refinement** in chic-v11, mg-d69c;
**unified v28 + chic-v11 polish pass integrating Linear A + CHIC
LOO verdicts into a symmetric §4.6/§4.7 narrative and framing
leave-one-out held-out validation as the fifth discipline-
protecting pillar** in v29, mg-a1e2; **cross-pool L3 robustness
extended to the 29 chic-v5 tier-3 candidates (8 reclassify to
tier-2-equivalent, 4 tier-3-corroborated, 17 tier-3-uncorroborated)**
in chic-v12, mg-2035; **within-window context inspection on the
8 chic-v12 tier-2-equivalent candidates** yielding **6 consistent
/ 2 inconclusive / 0 inconsistent** in chic-v13, mg-5261;
**leave-one-out held-out validation of the chic-v12 cross-pool L3
reclassification methodology on the 20 chic-v2 anchors** yielding
**60.0% LOO recovery vs chic-v12's 27.6% on the tier-3 set
(-32.4pp below baseline → cross-pool L3 reclassification is
anti-evidentiary on the tier-3 set; cross-pool L3 demoted to
permissive corroboration; chic-v13 within-window context
inspection becomes the load-bearing fourth discipline pillar)**
in chic-v14, mg-7f57; **methodology paper polish pass integrating
chic-v12 + chic-v13 + chic-v14 — cross-pool L3 demoted to
permissive corroboration; n=32 evidence-graded candidates with 7
carrying paired cross-pool L3 + within-window context-inspection
evidence; within-window context inspection promoted to the
load-bearing fourth discipline pillar** in v30, mg-ee1f)** — a publication-readable
consolidation of what
the Lineara project has mechanically established **across two
undeciphered Cretan scripts (Linear A and Cretan Hieroglyphic)**
across 28 Linear A work items + 14 chic sub-program work items,
anchored on the SigLA corpus ingest (`mg-1c8c`, Linear A) and the
Younger CHIC web edition ingest (`mg-99df`, CHIC), spanning the
Linear A harness pipeline `mg-d5ef` (v0) through `mg-4a7b` (v28)
and the chic sub-program `mg-99df` (chic-v0) through `mg-7f57`
(chic-v14); v25, chic-v7, v27, chic-v10, v29, and v30 are
editorial-only (no harness commits).
The repo scaffold (`mg-9e00`) predates the corpus ingest. The
companion log `docs/findings.md` carries the per-ticket history;
this document carries the consolidated methodology, results, and
supportable / unsupportable claim split, audited end-to-end against
the committed result files in `results/` and the merge notes in
`docs/findings.md`.

The intended reader is a research scientist or Aegean-syllabary
specialist who has not followed the merge notes. Section ordering
follows the standard methodology-paper shape (Abstract, Introduction,
Methods, Results, Discussion, Limitations, Conclusion) so the document
can be read cold. Linear A is the primary demonstration corpus
(§3.1–§3.14); the cross-script extension to Cretan Hieroglyphic
(§4.7) is the methodological-novel deliverable of the chic
sub-program — the Linear A substrate framework, ported verbatim to
CHIC, reproduces the Linear A monotonic-with-relatedness ordering
across the 4 substrate pools at cross-script Spearman ρ=+1.000 on
the per-pool right-tail gate gap.

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

We evaluate four substrate hypotheses — Aquitanian, Etruscan,
pre-Greek Aegean toponyms, and Eteocretan (presumed Linear-A
linguistic descendant) — plus a Linear-B-carryover positive control,
under thirteen pre-registered falsifiable acceptance gates: own-LM
right-tail (mg-d26d), cross-LM and third-LM negative controls
(mg-0f97 / mg-4664), per-sign cross-window coherence (mg-c216),
same-distribution and cross-language pollution tests
(mg-6b73 / mg-7ecb), bigram-preserving control sampler (mg-9f18),
per-inscription cascade-candidate test (mg-3438), targeted
KU-RO / KI-RO scholarly-anchor search (mg-711c), Eteocretan own-LM
gate (mg-6ccd), full Eteocretan cross-LM matrix (mg-b599),
population-level scholar-proposed-reading comparison (mg-46d5), and
per-inscription cascade analysis under the Eteocretan LM (mg-c103).
The framework **detects substrate-LM-phonotactic kinship at the
population level**, with all four substrate pools clearing their
own-LM gates (Aquitanian under Basque LM p = 3.22e-05; Etruscan under
Etruscan LM p = 5.21e-04; toponym under Basque LM with bigram-
preserving control p = 9.99e-05; Eteocretan under Eteocretan LM
p = 4.10e-06). The **gap-magnitude ordering** across pools is
consistent with a-priori genealogical relatedness: Eteocretan +0.20
(closest-relative) > toponym +0.11 (Cretan pre-Greek substrate) >
Etruscan +0.06 > Aquitanian +0.03 (furthest-out Mediterranean).
The **full cross-LM matrix** (v23) shows own-LM dominance HOLDS
for 3 of 4 pools; Aquitanian is the small-dynamic-range exception.
The framework **partially discriminates substrate-shape from
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
sequence in `KH 10` or `KH 5`. v22 (mg-46d5) broadens the
external-validation footprint to a 35-entry, 76-AB-sign-comparison-
point set drawn from Younger's contextual scholarly readings
across 6 sites and 21+ scholar-attested CV combinations
(ku-ro, ki-ro, ja-sa-sa-ra-me, ku-mi-na, ta-na, pi-ta-ja, ma-te,
ku-pa, ki-ra, ka-pa, da-re, da-ta, di-na, pa-ja, a-ra, ta-i,
ku-ra, ku-pa3, ku-se, mi-na, ka-ru). The aggregate match rate is
**3.95% (3/76)** on the consonantal first segment of the
scholarly CV — strong-null-band (the pre-registered < 5% threshold
for "reinforces v13 / v19 verdicts"), with 32 of 35 entries scoring
zero and the 3 non-zero entries owing their match to vowel-initial
syllables or chance overlap on common phonemes.
**Internal consensus across surviving candidates does not imply
external correctness:** mechanical scoring + phonotactically-matched
controls catches a failure mode that internal-consensus-only
methodology would miss, and the v22 35-entry result moves that
claim from "one inscription, decisively divergent" to
"population-level decisively divergent". v24 (mg-c103) closes the
external-validation narrative: re-running the per-inscription
cascade analysis with v21's Eteocretan pool included produces zero
cascade candidates under eteocretan-only aggregation (and a 0/76
match rate against the scholar set), while the four-pool aggregation
reproduces v19's three cascade candidates with byte-identical
high-coherence mechanical readings on PS Za 2 and matches v22's
3.95% aggregate rate to the digit. The closest-genealogical-
relative substrate's strongest-own-LM PASS therefore reflects
population-level phonotactic selectivity but does **not** propagate
to a per-inscription decipherment signal under any candidate
substrate the framework has tested.

The supportable claim is therefore strictly narrower than "Linear A
is X": the framework identifies which substrate phonotactic profiles
produce population-level signal in the SigLA corpus, and on which
inscriptions that signal concentrates, but does not validate specific
sign readings — and where external validation against an independent
scholarly proposal is available, the mechanical reading diverges.

A second external-validation channel at the leaderboard-top-K
granularity (**v26, mg-c202**) extends the v22 per-inscription
consensus comparison to the four pools' top-20 substrate surfaces.
Each Linear A pool's top-20 produces a positive **inscription-count
match-rate lift over the LB-carryover-only baseline (177/772 =
22.93%)** on its extended-inscription subset (aquitanian +5,
etruscan +6, toponym +7, eteocretan +5 — all clearing chic-v6's
tier-1 → tier-2 lift threshold of +3 inscriptions on the CHIC side),
demonstrating that the verification methodology is portable cross-
script. The load-bearing **negative-evidence companion** is the per-
pool sign-level inverse-verification table: 29 / 22 / 19 / 30
sign-level contradictions of scholarly proposals across aquitanian /
etruscan / toponym / eteocretan respectively, where a substrate
hypothesis's first-phoneme proposal at an AB sign disagrees with the
scholarly first-phoneme proposal at the same sign in the same
inscription. Both signals are real and publishable; neither alone
supports a decipherment claim, which remains conditional on Aegean-
syllabary specialist review.

**Cross-script extension to Cretan Hieroglyphic (chic-v0..v14).** A
parallel chic sub-program ports the same substrate-LM-phonotactic-
kinship framework to **CHIC**, the older sister-script to Linear A
(302 of 331 catalog inscriptions ingested from the Younger web
edition; 96 syllabographic + 35 ideogram signs identified; 20
paleographic anchor candidates inherited from Linear A — 3 consensus,
10 proposed, 7 debated; 60.85% (864/1420) corpus-wide syllabographic-
position anchor coverage). Applied to the CHIC syllabographic-only
stream (276 inscriptions, 1,258 tokens, 551 maximal syllabographic
blocks — roughly one-quarter the size of Linear A's corpus), the
4 Linear A substrate pools produce a **CHIC right-tail bayesian
gate ordering identical to Linear A's**: Eteocretan PASSes at
p=7.33e-04 (the only pool to clear α=0.05 on CHIC's smaller corpus);
toponym FAILs at p=0.435; Etruscan FAILs at p=0.720; Aquitanian
FAILs at p=0.937. Cross-script Spearman rank correlation on the
per-pool right-tail gap is **ρ=+1.000** across the 4 pools, with
mean top-20 substrate-surface overlap 0.47 (38/80 substrate-side
slots shared) and per-substrate-surface continuity strongest for
Eteocretan (Pearson +0.45). The extended methodology paper's
headline cross-script claim is therefore: **the substrate-LM-
phonotactic-kinship signal the framework detects is cross-script;
the per-pool PASS/FAIL distinction tracks candidate-substrate
genealogical relatedness to the target script's underlying
language, and that tracking survives transfer between Linear A and
CHIC under the same scoring infrastructure.** A per-sign syllable-
value extraction framework on the chic-v3-validated Eteocretan
substrate (chic-v5, four-line-of-evidence discipline) classifies
**3 of 76 unknown CHIC syllabographic signs as tier-2 candidates**
(≥ 3 of 4 lines agree on a coarse phoneme class — `vowel`, `stop`,
`nasal`, `liquid`, `fricative`, `glide`); these are **candidate
proposals pending domain-expert review**, not decipherments, and
the framework's per-sign resolution is class-level, not phoneme-
specific. The discipline (mechanical agreement predicate +
explicit silent-line bookkeeping + the L3-systematic-class-bias
disclosure) is the chic-v5 contribution; the count is a small-
corpus-noise-floor artifact rather than the deliverable.

A CHIC-side mechanical-verification pass against three external-
scholarship sources (**chic-v6, mg-a557**) — scholar-proposed Linear-A
readings, Cretan/Aegean toponym substrings, and item-location
consistency — produces a small-but-non-zero **+3 inscriptions / +20
hits** tier-1 → tier-2 verification lift on the CHIC corpus, with
the larger tier-3 / tier-4 lifts (+91 / +46 inscriptions) caveated
for class-level-matching permissiveness in the absence of a
phonotactically-matched permutation control. A dual-script
bilingual analysis (**chic-v8, mg-dfcc**) verifies that Daniel's
named candidate (the Malia altar stone) is **CHIC #328**, ingested
in chic-v0 as **unilingual CHIC**, not dual-script per the Olivier-
Godart 1996 catalog, and a systematic survey of the v0 corpora
finds no genuinely-dual-script artifact bearing parallel
inscriptions in both scripts on the same physical object. The
fifth line of evidence (L5, LA-constraint) is therefore silent for
all 76 unknown CHIC syllabographic signs by corpus state, mirroring
chic-v5's L4 (cross-script paleographic) silent-by-construction;
**0 new tier-2 candidates** are derived via the bilingual
extension on v0 corpora, and the chic-v5 tier-2 candidate count
remains 3 (`#001 → wa`, `#012 → wa`, `#032 → ki`) unchanged. This
is a publishable null result preserving the bilingual extension as
a falsifiable fifth axis contingent on future corpus expansion
(full GORILA Za-series + CMS sealstone-catalog dual-script
entries), while explicitly refusing to invoke conjectural
genre-parallels (CHIC #328 vs LA libation tables PS Za 2 / SY Za 4)
as load-bearing evidence.

A held-out validation of the chic-v5 framework (**chic-v9, mg-18cb**)
applies the L1+L2+L3 machinery to the chic-v2 anchor pool of 20
known scholarly values under leave-one-out: each anchor S is
removed, treated as unknown, and re-classified against the reduced
19-anchor pool. L4 is excluded for circularity (it is the source of
the anchor pool). **The framework recovers known phoneme classes at
20.0% (4/20) aggregate accuracy — at the 16.7% chance baseline for
a 6-class taxonomy** — with per-line accuracy L1=20%, L2=20%, L3=5%
and **0 of 3 LOO tier-2 (3-of-3 unanimous) calls correctly
classified**. The Linear A analog (**v28, mg-4a7b**) applies the
same LOO machinery to the 21 LB-carryover anchors with paleographic
L4 again excluded for circularity; the framework recovers known
phoneme classes at **33.3% (7/21) aggregate accuracy — modestly
above the 16.7% chance baseline but below the 40% moderate-
agreement threshold** — with per-line accuracy L1=33.3%, L2=33.3%,
L3=9.5% and **0 of 3 LOO tier-2 calls correctly classified, byte-
identical to chic-v9 on the unanimity criterion**. The cross-script
deltas are small (+13.3% / +13.3% / +4.5% percentage points on the
L1/L2/L3 lines respectively); both scripts land in the **low-
agreement / not-validated band**, and the per-script delta is
within the regime that **the at-chance per-sign behaviour is
structural to the chic-v5 framework rather than CHIC-corpus-
specific**, closing the v28-pre-registered "structural vs corpus-
specific" question in favour of the structural-limitation arm.
A within-polecat-scope candidate-evidence pass (**chic-v11,
mg-d69c**) checks two additional axes for the 3 chic-v5 tier-2
candidates: cross-pool L3 robustness under all 4 substrate-pool
LMs (12 cells = 3 candidates × 4 LMs) and inscription-level
metadata for the chic-v6 ku-pa-family lift attributable to
`#032 → ki`. Cross-pool L3 produces an **asymmetric per-candidate
refinement**: `#001 → wa`/glide is rejected by 3 of 4 LMs (the
chic-v5 glide vote is an Eteocretan-LM-specific artifact);
`#012 → wa`/glide is rejected by 3 of 4 LMs (only Eteocretan
votes glide); `#032 → ki`/stop is supported by 2 of 4 LMs
including the chic-v5 default Eteocretan plus Etruscan, and the
ku-pa context inspection corroborates the chic-v6 lift on both
sides (4 source Linear A tablets HT 1, HT 16, HT 102, HT 110a are
all LM IB Hagia Triada accountancy tablets; the matched CHIC #057
context is `#079 ki pa / NUM:20`, the canonical sign-run-followed-
by-numeral accountancy-formula structure). **chic-v12 (mg-2035)**
extends the cross-pool L3 robustness check methodologically
symmetrically to the **29 chic-v5 tier-3 candidates**: **8
reclassify to ``tier-2-equivalent``** (≥1 non-Eteocretan substrate
LM corroborates the chic-v5 proposed class — same band-level
evidence structure as `#032`: `#005`, `#017`, `#021`, `#039`,
`#055`, `#056`, `#065`, `#072`, all stop or nasal class), 4 to
``tier-3-corroborated`` (Eteocretan-only, the chic-v5 baseline
state for the L1+L2-disagree subset), 17 to
``tier-3-uncorroborated``. **chic-v13 (mg-5261)** runs within-
window context inspection on the 8 tier-2-equivalent candidates
following the chic-v11 `#032`/CHIC #057 ku-pa template: **6
consistent / 0 inconsistent / 2 inconclusive on corpus state**;
the strongest evidence falls on `#072` (two `[stop:#072]-de NUM`
accountancy entries at Knossos bar CHIC #065, mirroring the
chic-v11 ku-pa NUM-following structure directly), `#056`
(multiple `[?] [stop:#056] NUM` entries at Knossos bar CHIC #061,
including one preceding `ke-de NUM:1`), and `#021` (3-fold cross-
site recurrence of `031-021-061` plus direct adjacency with
`ki-de` at #059). **chic-v14 (mg-7f57)** then leave-one-out tests
the chic-v12 cross-pool L3 reclassification rule on the 20
chic-v2 anchors with **known** class as reference: **12/20 = 60.0%
LOO recovery rate**, so chic-v12's 27.6% on the tier-3 set is
**-32.4pp BELOW the LOO baseline → the chic-v12 reclassification
on the tier-3 set is anti-evidentiary** (cross-pool L3 corroborates
ground-truth class on known anchors *more often* than chic-v12
corroborates the chic-v5 proposed class on the tier-3 set).
**Cross-pool L3 is therefore demoted from a discipline-protecting
pillar to a permissive corroboration test**, useful only in
combination with at least one other independent line of evidence;
**within-window context inspection (chic-v13) becomes the load-
bearing fourth discipline pillar**, with the framework-level
chic-v9 + v28 LOO negatives unchanged as the fifth pillar. The
post-chic-v14 per-candidate framing extends the chic-v11 register
into a 32-candidate evidence-graded set: **n = 32 evidence-graded
candidates** (3 chic-v5 tier-2 + 29 chic-v5 tier-3) with **7
carrying paired cross-pool L3 + within-window context-inspection
evidence** (`#032` chic-v11 + 6 chic-v13 consistent: `#005`,
`#017`, `#021`, `#039`, `#056`, `#072`), 2 inconclusive on
context inspection (`#055`, `#065` chic-v13), 2 chic-v5 tier-2
demoted by chic-v11 cross-pool L3 (`#001`, `#012`), 4 chic-v5
tier-3 / Eteocretan-only L3 corroborated (`#006`, `#033`, `#050`,
`#063`), and 17 chic-v5 tier-3 / cross-pool L3 not corroborated.
**The v28 + chic-v9 framework-level negative remains the dominant
constraint**, and none of the 7 paired-evidence candidates clears
specialist-review elevation; the chic-v5 / chic-v6 / chic-v8
framing of the three tier-2 candidates remains "candidate
proposals contingent on the framework's currently-low validation
accuracy on both scripts"; the §4.6 / §4.7 narrative leads
symmetrically with the LOO accuracy numbers rather than the
candidate counts; the methodology paper's three-sentence reading
test (§7) is restructured for the post-chic-v14 register
accordingly. The 7 paired-evidence candidates remain "candidate
proposals pending domain-expert review" at the same tier as
`#032` was post-chic-v11; promotion to higher tiers requires
specialist review out of polecat scope.

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

A parallel chic sub-program (chic-v0 through chic-v14) extends the
same mechanical-falsifiability discipline to a second undeciphered
Cretan script — **Cretan Hieroglyphic (CHIC)**, the older
sister-script to Linear A (~1900–1600 BCE; sealstone-dominated,
shorter inscriptions, 302 of 331 catalog entries machine-recoverable
from Younger's web edition of CHIC's Olivier & Godart 1996 catalog).
The chic sub-program is **a cross-script methodology test, not a
CHIC decipherment claim**: the same Linear A substrate framework,
the same external phoneme LMs, the same matched-control protocol,
the same right-tail bayesian gate, applied to a different undeciphered
Cretan script. The cross-script extension's purpose is to test
whether the substrate-LM-phonotactic-kinship signal the Linear A
framework detects (§3.14, §4.1) is **specific to Linear A** or
**transferable across scripts under the same a-priori
genealogical-relatedness ordering of substrate candidates**.

The methodology paper's central methodological claim is best
read as a union of **five pre-registered falsifiable discipline-
protecting pillars**, each catching a different motivated-
reasoning failure mode that internal-consensus-only methodology
cannot catch:

1. **Per-surface coherence** (v13, mg-c216) — cross-window-
   consensus median 0.18 against a 0.6 bar (catches the
   "framework converges on a stable mapping" failure).
2. **Per-inscription cascade-candidate external validation**
   (v19 / v24, mg-3438 + mg-c103) — combined with v22 / v26
   sign-level inverse-verification companions yielding 19–30
   sign-level contradictions of scholarly proposals per pool
   on Linear A (catches the "internal-consensus inscription is
   correctly read" failure).
3. **Population-level scholar comparison** (v22, mg-46d5;
   chic-v6, mg-a557) — aggregate match rate 3.95% (3/76) on the
   Younger 35-entry scholar set on Linear A; small-but-non-zero
   +3-inscription / +20-hit chic-v6 tier-1 → tier-2 lift on CHIC
   (catches the "population-level matching averages out
   individual divergence" failure).
4. **Within-window context inspection** (chic-v11, mg-d69c;
   chic-v13, mg-5261) — the chic-v11 `#032`/CHIC #057 ku-pa
   accountancy-formula corroboration and the chic-v13 6-of-8
   consistent verdict on the chic-v12 tier-2-equivalent
   candidates (catches the "cross-pool L3 corroboration alone
   confirms a class-level value" failure mode that chic-v14's
   LOO baseline finding made acute). **This pillar is load-
   bearing as the fourth discipline-protecting axis post-
   chic-v14**: chic-v14's leave-one-out test of the chic-v12
   cross-pool L3 reclassification rule recovers known anchor
   classes at 60.0% baseline, demoting cross-pool L3 from a
   discipline-protecting axis in its own right to a permissive
   corroboration test that requires within-window context
   evidence to be load-bearing.
5. **Leave-one-out held-out validation** (chic-v9 / v28 /
   chic-v14, mg-18cb + mg-4a7b + mg-7f57) — chic-v5 framework
   per-sign recovery 20.0% on CHIC and 33.3% on Linear A
   (low-agreement / not-validated band, both scripts; 0/3 on
   the tier-2 unanimity criterion); chic-v12 cross-pool L3
   reclassification rule 27.6% on the tier-3 set vs 60.0% LOO
   baseline on known anchors → -32.4pp below baseline → cross-
   pool L3 reclassification is anti-evidentiary on the tier-3
   set (catches the "framework that produces candidates fails
   to recover known values when run blind" and "permissive
   corroboration mistaken for discriminative gate" failure
   modes).

The pillar-4 demotion of cross-pool L3 robustness from a
discipline-protecting axis to a permissive corroboration test
is itself a discipline-protecting outcome: the held-out
validation pillar (chic-v14) caught a permissive corroboration
axis (chic-v11 + chic-v12 cross-pool L3) before it could
load-bear in the methodology paper, demonstrating that the
discipline pillars work. The chic-v11 / chic-v12 cross-pool L3
results stand as documented (per-candidate evidence structure
information), but their interpretive weight is bounded above by
chic-v14's LOO baseline.

The remainder of this document specifies the pipeline (§2), reports
the thirteen pre-registered falsifiable acceptance-gate / external-
validation outcomes plus the v23 cross-LM matrix follow-up on Linear
A (§3), the chic-v0..v14 cross-script extension to CHIC (§4.7;
positioned within the Discussion as the methodology paper's
cross-script Part-B because §4.7 simultaneously delivers chic
results and the cross-script methodological synthesis), the
mechanical-verification follow-ups on each side (chic-v6 and v26 in
§4.7 / §4.6 respectively; closing the previous LA-side / CHIC-side
asymmetry on leaderboard-top-K external-scholarship match-rate
testing) and the chic-v8 dual-script bilingual analysis null result
(§4.7), discusses what the framework does and does not detect
across both scripts (§4), and explicitly enumerates unsupported
claims (§5).

---

## 2. Methods

The pipeline is built up across the harness sequence `mg-d5ef` (v0)
through `mg-c103` (v24), atop the SigLA corpus ingest (`mg-1c8c`) and
the initial repo scaffold (`mg-9e00`); the v8–v15 harness lineage
established the production scoring path (paired-difference under
external phoneme LMs, Beta-binomial per-surface posteriors,
right-tail Mann-Whitney gate), and v18–v24 added the bigram-
preserving control sampler, Eteocretan substrate pool, full cross-LM
matrix, and per-inscription cascade-candidate analysis. It is
deterministic end-to-end:
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
| `eteocretan` | 84 | Duhoux 1982 + Whittaker 2017 + Younger online catalog (Praisos 1–7, Dreros 1–2 + minor short attestations; mg-6ccd) | eteocretan |
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
substrate's phoneme distribution. Two samplers are committed: a
**unigram-marginal sampler** (v6) draws each phoneme independently
from the substrate's marginal histogram; a **bigram-preserving
sampler** (v18, `--sampler bigram`, alpha = 0.1) draws each phoneme
conditional on the previous phoneme using the substrate's bigram
counts, so adjacent-phoneme structure (CV transitions, vowel hiatus
rates) is matched. The bigram sampler is the production default for
new pools after v18 (mg-9f18); v6 unigram is retained for backwards-
compatible reruns. Determinism is preserved by seeding from
`sha256(pool_name)`. The LM dispatch routes each control pool
through its substrate's LM so the paired-difference cancels the LM
choice out of the comparison
(`scripts/build_control_pools.py`, `mg-f419` + `mg-c2af` + `mg-9f18`).

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
`harness/external_phoneme_models/{basque,etruscan,mycenaean_greek,eteocretan}.json`,
each fit with add-α smoothing on real text (α=0.1 for the v8 LMs;
α=1.0 for the v21 Eteocretan LM, set higher because the corpus is
small):

- **basque.json** — Basque text (Aquitanian's modern descendant) used
  as the LM for the Aquitanian substrate pool.
- **etruscan.json** — TLE Etruscan corpus.
- **mycenaean_greek.json** — LiBER (`https://liber.cnr.it`) corpus,
  5,638 Linear-B inscriptions yielding 21,634 word tokens and
  5,113 unique forms (mg-4664).
- **eteocretan.json** — manual transcription of the canonical
  Eteocretan corpus (Duhoux 1982 + Whittaker 2017 + Younger online
  catalog), 100 inscriptions / 87 unique word forms; the LM is
  genuinely small-corpus by reality (the Eteocretan epigraphic
  record is finite at ~9 substantive multi-line texts) and uses
  α=1.0 to compensate (mg-6ccd).

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

### 2.10 Post-v15 additional gates (v18–v26)

Five additional pre-registered gates / verification passes were
added in the v18–v26 sequence within the same scoring discipline:

- **Bigram-preserving control sampler** (mg-9f18, v18). Re-evaluate
  the toponym pool against the v18 bigram-preserving control;
  re-run the v10 gate at four pollution levels (10/25/50/75%) to
  characterize the gate's curation-sensitivity gradient.
- **Per-inscription cascade-candidate test** (mg-3438, v19). For
  each Linear A inscription I drawn from a top-30 right-tail,
  short, or libation-formula population, aggregate all positive-
  paired-diff candidate equations targeting I; report the per-token
  *robust* fraction (modal_posterior > 0.5 AND n_proposals ≥ 2);
  classify as cascade candidate (≥ 0.5), partial (0.25–0.5), or
  noise. mg-711c (v20) extended this with a targeted KU-RO / KI-RO
  scholarly-anchor search on the v19 cascade-candidate accountancy
  tablets `KH 10` / `KH 5`.
- **Eteocretan substrate pool** (mg-6ccd, v21; mg-b599, v23). Add
  Eteocretan as a 4th substrate pool with its own bigram-preserving
  control; re-run the v10 gate; fill out the full substrate × LM
  cross-LM matrix (Eteocretan candidates re-scored under Mycenaean
  Greek and Etruscan LMs; existing pools re-scored under the
  Eteocretan LM).
- **Population-level scholar-proposed-reading comparison**
  (mg-46d5, v22; mg-c103, v24). Score the per-inscription
  mechanical modal phonemes against a 35-entry curated set of
  scholar-proposed contextual readings drawn from Younger's
  online catalog; report the aggregate match rate on the
  consonantal first segment of the scholarly CV. v24 (mg-c103)
  re-runs the per-inscription cascade analysis under the
  Eteocretan-only and four-pool aggregations.
- **Linear A-side leaderboard-top-K mechanical verification**
  (mg-c202, v26). Apply the chic-v6 verification methodology
  verbatim — same three pre-registered match sources (Source A:
  scholar-proposed Linear-A reading match; Source B: toponym
  substring match length 3–5; Source C: item-location consistency)
  and identical match criteria (no relaxation) — to each Linear A
  pool's top-20 leaderboard substrate surfaces. Report per-pool
  inscription-count / a+b+c hit-count lift over the LB-carryover-
  only baseline (177/772 = 22.93% across the full Linear A corpus)
  on each pool's extended-inscription subset. Compute the per-pool
  sign-level inverse-verification table: cases where a substrate
  hypothesis's per-sign first-phoneme proposal contradicts a
  scholar entry's first-phoneme proposal at the same AB sign in
  the same inscription. v26 closes the previously asymmetric
  CHIC-side (chic-v6) / Linear A-side mechanical-verification
  reporting at the leaderboard-top-K granularity.

### 2.11 Cross-script extension pipeline (chic-v0–chic-v14)

The chic sub-program reuses the same scoring infrastructure
verbatim — same external phoneme LMs, same matched-control pools
(`control_aquitanian`, `control_etruscan`, `control_toponym_bigram`,
`control_eteocretan_bigram`), same `external_phoneme_perplexity_v0`
metric, same per-surface Beta-binomial posterior, same right-tail
Mann-Whitney U gate at K=20. The only chic-specific code paths are
the corpus ingest + sign-classification + paleographic-anchor +
syllabographic-stream filter pipeline (chic-v0..v3) and the per-sign
value-extraction framework (chic-v5). Full per-stage detail in §4.7.

- **chic-v0 corpus** (mg-99df). 302 of 331 CHIC catalog entries
  ingested from Younger's web edition (Wayback Machine snapshot,
  2022-07-03; live URL retired); 29 missing entries deferred to a
  manual-transcription pass. 131 distinct CHIC sign IDs observed;
  1,489 sign-token occurrences. Site distribution Knossos- and
  Mallia-skewed (62% combined); support distribution sealstone-
  dominated (126 sealstones + 49 crescents + 34 medallions +
  44 long admin documents).
- **chic-v1 sign classification** (mg-c7e3 + mg-0ea1 backfill). 131
  CHIC sign IDs partitioned under the Olivier & Godart 1996
  numeric-range rule into **96 syllabographic + 35 ideogram + 0
  ambiguous**. 20 paleographic anchor candidates enumerated as
  CHIC ↔ Linear A correspondences (3 consensus, 10 proposed, 7
  debated; sources Younger online + Salgarella 2020 + Decorte
  2017/2018 + Civitillo 2016).
- **chic-v2 paleographic anchor inheritance** (mg-362d). 20 anchors
  promoted into a tier-1 (3 consensus) / tier-2 (17
  proposed-or-debated) anchor pool. **864 of 1,420** syllabographic
  CHIC sign positions across the corpus are anchored — **60.85%**
  corpus-wide coverage; **263 of 302** inscriptions carry ≥1
  anchored position.
- **chic-v3 substrate framework on CHIC** (mg-9700). The 4 Linear A
  substrate pools (Aquitanian, Etruscan, toponym, Eteocretan) are
  scored against the CHIC syllabographic-only stream (276
  inscriptions, 1,258 syllabographic tokens, 551 maximal
  syllabographic blocks — roughly one-quarter the size of Linear
  A's corpus) under the Linear A v10 / v18 / v21 right-tail
  bayesian gate. Matched controls are reused verbatim from the
  Linear A pools (controls are about substrate phonotactic shape,
  not target-corpus shape; reuse keeps the chic-v3 result directly
  comparable to Linear A's v10 / v18 / v21 numbers).
- **chic-v4 cross-script correlation** (mg-c769). Compute Spearman
  rank correlation across the 4 substrate pools' Linear A vs CHIC
  per-pool gate gaps; compute mean top-20 substrate-surface
  overlap; compute per-substrate-surface Pearson continuity
  on overlapping surfaces. Pure descriptive markdown-table-parser
  + closed-form arithmetic; no rescore.
- **chic-v5 per-sign syllable-value extraction**
  (mg-7c6d). Four lines of evidence per unknown CHIC syllabographic
  sign: (1) distributional plurality via top-3 nearest chic-v2
  anchors by Bhattacharyya similarity across four fingerprint
  dimensions (`left_neighbor`, `right_neighbor`, `position`,
  `support`); (2) anchor-distance strict top-1; (3) substrate-
  consistency under v21 Eteocretan LM scored against a class-
  disjoint deterministic-permutation control mapping; (4) cross-
  script paleographic — silent for all 76 unknowns by construction
  (the chic-v1 paleographic-candidate list is precisely the seed
  for the chic-v2 anchor pool, so by construction no unknown
  carries a paleographic note; documented as a limitation).
  Tier classification mechanical: ≥3 of 4 lines agreeing →
  tier-2 candidate proposal (post-chic-v9: contingent on the
  framework's currently-low validation accuracy); 2 of 4 →
  tier-3 (suggestive); 1 of 4 → tier-4; 0 → untiered. Coarse
  phoneme classes (`vowel`, `stop`, `nasal`, `liquid`, `fricative`,
  `glide`).
- **chic-v6 mechanical verification pass** (mg-a557). Apply three
  pre-registered external-scholarship match sources (Source A:
  scholar-proposed Linear-A reading match against the v22 35-entry
  curated set; Source B: toponym substring match length 3–5 against
  `pools/toponym.yaml`; Source C: item-location consistency, i.e.
  per-inscription `site` field substrings length 3–5 matched against
  the inscription's own phoneme stream) to four extended-partial-
  reading tier levels (tier-1 chic-v2 anchors only; tier-2 ∪ chic-v5
  tier-2 specific-phoneme overrides; tier-3 ∪ chic-v5 tier-3 class-
  level placeholders; tier-4 ∪ chic-v5 tier-4 class-level
  placeholders). Match criteria fixed before computing match counts;
  no post-hoc relaxation. The tier-1 → tier-2 lift is the load-
  bearing chic-v6 result; tier-3 / tier-4 lifts are caveated for
  class-level-matching permissiveness.
- **chic-v8 dual-script bilingual analysis** (mg-dfcc). Cross-
  reference chic-v0 + LA-v0 corpora for genuinely-dual-script
  artifacts (an artifact bearing parallel inscriptions in both
  CHIC and Linear A on the same physical object); apply the LA-side
  reading at parallel positions as a fifth line of evidence (L5,
  LA-constraint) constraining CHIC-side phoneme values; promotion
  rule: ≥4 of 5 lines (L1+L2+L3+L4+L5) agreeing on coarse phoneme
  class promotes a chic-v5 tier-3 / tier-4 candidate to tier-2.
  Refuse to invoke genre-parallels (CHIC #328 offering table vs LA
  libation tables PS Za 2 / SY Za 4) as load-bearing evidence —
  reported informationally only.
- **chic-v9 leave-one-out held-out validation** (mg-18cb). For each
  of the 20 chic-v2 anchors S with known scholarly value V: remove
  S from the chic-v2 anchor pool, treat S as unknown, recompute
  L1+L2+L3 against the reduced 19-anchor pool (rebuilding the L3
  candidate-value pool from the reduced 19-anchor pool plus bare
  vowels under the chic-v5 Eteocretan-phoneme-inventory filter),
  apply the chic-v5 tier classification with L4 silent (3-of-3
  unanimity → LOO tier-2; 2-of-3 → tier-3; 1-of-3 → tier-4; 0 →
  untiered), and compare framework class to V's known class. **L4
  is deliberately excluded for circularity** (the chic-v1
  PALEOGRAPHIC_CANDIDATES list is the source of the chic-v2 anchor
  pool, so for any anchor S the L4 line trivially recovers V by
  construction; including L4 would inflate accuracy by circularity).
  Pre-registered acceptance bands: >70% high; 40-70% moderate; <40%
  low / not validated.
- **chic-v11 cross-pool L3 robustness on the 3 chic-v5 tier-2
  candidates + #032 ku-pa context inspection** (mg-d69c). Re-runs
  the chic-v5 L3 substrate-consistency line under all 4 substrate-
  pool LMs (12 cells = 3 candidates × 4 LMs) plus a metadata
  cross-check on the chic-v6 ku-pa-family lift attributable to
  `#032 → ki`. Pre-registered output: per-candidate cross-pool L3
  reading + asymmetric per-candidate refinement.
- **chic-v12 cross-pool L3 robustness on the 29 chic-v5 tier-3
  candidates** (mg-2035). Methodologically symmetric extension of
  chic-v11 to the tier-3 set (29 × 4 = 116 cells). Pre-registered
  reclassification bands: ``tier-2-equivalent`` (≥1 non-Eteocretan
  substrate LM corroborates the chic-v5 proposed class — same
  band-level evidence structure as `#032`); ``tier-3-corroborated``
  (only Eteocretan-L3 corroborates); ``tier-3-uncorroborated`` (no
  LM's L3 corroborates). Pre-registered bail rule on within-window
  context inspection at > 5 reclassifications: defer the
  inspection to a chic-v13 follow-up because the count itself is
  the scale signal.
- **chic-v13 within-window context inspection on the chic-v12
  tier-2-equivalent candidates** (mg-5261). For each candidate ×
  1–3 high-density host inscriptions: render with chic-v2 anchors
  substituted and the candidate as a class-level placeholder
  (`[stop:#NNN]`, `[N:#NNN]`); check whether the rendered reading
  is consistent with surrounding accountancy / sealing / sealstone-
  formula structure on the chosen inscriptions and whether it
  contradicts canonical CHIC sealstone formulas (`i-ja-ro`,
  `ki-de`, `wa-ke`) or any chic-v2 anchor's known value. Output:
  per-candidate verdict in {`consistent`, `inconsistent`,
  `inconclusive`}.
- **chic-v14 leave-one-out held-out validation of the chic-v12
  cross-pool L3 reclassification methodology** (mg-7f57). For each
  of the 20 chic-v2 anchors S with known phoneme class V: hold S
  out, treat as unknown, rebuild candidate-value pool per (LOO
  iteration, substrate pool), regenerate the sha256-keyed control
  mapping per cell, apply the chic-v12 reclassification rule with
  S's **known** class as reference (in chic-v12 the reference was
  the chic-v5 proposed class). Pre-registered LOO output:
  cross_pool_l3_recovery_rate; eteocretan_only_recovery_rate;
  no_corroboration_rate. Pre-registered comparison band: chic-v12
  rate vs chic-v14 LOO baseline; if the chic-v12 rate is below
  baseline, cross-pool L3 reclassification is anti-evidentiary on
  the tier-3 set.

---

## 3. Results

### 3.1 Acceptance-gate outcomes — summary table

The thirteen pre-registered gates / pre-specified tests and their
outcomes are (gates 1–7 form the original v15-shape pre-registration;
gates 8–13 were added by v18–v22 follow-on tickets within the same
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
| 12 | Eteocretan substrate pool, own-LM bigram-preserving control | mg-6ccd (v21) | gate p = 4.10e-06 (PASS); cross-LM under Basque p = 2.58e-03 (PASS, ~600× weaker) | **strongest pool PASS in the validation series** (closest-genealogical-relative substrate; see §3.14) |
| 12b | full cross-LM matrix for Eteocretan (Eteocretan under MG + Etruscan; existing pools under Eteocretan LM) | mg-b599 (v23) | own-LM-dominance pattern HOLDS for 3/4 substrate pools; Eteocretan-LM has Eteocretan-specific selectivity (Etruscan-substrate-under-Eteocretan-LM FAILs at p=0.92, gap −0.017); Eteocretan-substrate PASSes under all 4 LMs tested with own-LM strongest | cross-LM matrix shape consistent with substrate-LM-phonotactic-kinship detection; Aquitanian deviation is small-dynamic-range artifact (see §3.14 "Cross-LM matrix (v23)") |
| 13 | population-level external validation against scholar-proposed Linear A readings (35-entry curated set drawn from Younger; 76 AB-sign comparison points across 6 sites; categories include accountancy totals, libation formulae, theonyms, commodity terms, names) | mg-46d5 (v22) | aggregate match rate **3.95%** (3/76) on consonantal first segment of scholarly CV; robust 1.32% (1/76); 32/35 entries score zero | **decisive negative external validation at population scale** (strong-null band, < 5%; reinforces v13 / v19 / v20 — internal consensus does not imply external correctness; see §3.13.4 / §4.6) |
| 14 (chic-v12) | cross-pool L3 robustness reclassification on the 29 chic-v5 tier-3 candidates (4 substrate-pool LMs × 29 candidates = 116-cell matrix; reclassification rule: ≥1 non-Eteocretan substrate LM corroborates the chic-v5 proposed class → ``tier-2-equivalent``; same band-level evidence structure as the chic-v11 surviving tier-2 `#032`) | mg-2035 (chic-v12) | **8 of 29 reclassify to ``tier-2-equivalent``** (`#005`, `#017`, `#021`, `#039`, `#055`, `#056`, `#065`, `#072`; all stop or nasal class), 4 to ``tier-3-corroborated`` (Eteocretan-only), 17 to ``tier-3-uncorroborated``; bail on within-window context inspection at 8 > 5 (chic-v12 brief pre-registered scale signal) | **n=32 evidence-graded candidates** (3 chic-v5 tier-2 + 29 chic-v5 tier-3); per-candidate evidence grading within the chic-v9 framework-level negative; subsequently re-interpreted by chic-v14 LOO (gate 16) — see §4.7 |
| 15 (chic-v13) | within-window context inspection on the 8 chic-v12 ``tier-2-equivalent`` candidates following the chic-v11 `#032 → ki` ku-pa context inspection methodology (each candidate × 1–3 high-density host inscriptions × rendered reading + structural commentary + per-candidate verdict) | mg-5261 (chic-v13) | **6 consistent / 0 inconsistent / 2 inconclusive** out of 8; consistent: `#021`, `#005`, `#072`, `#017`, `#039`, `#056`; inconclusive: `#055`, `#065` (predominantly fragmentary host inscriptions); strongest cases at `#072` (Knossos bar #065 `[stop:#072]-de NUM:1` accountancy entries — direct mirror of chic-v11 ku-pa structure), `#056` (Knossos bar #061 `[?] [stop:#056] NUM` adjacent to `ke-de NUM:1`), `#021` (3-fold cross-site `031-021-061` recurrence + `ki-de` adjacency) | **load-bearing fourth discipline pillar post-chic-v14** (cross-pool L3 corroboration alone is not sufficient for class-level value confirmation; see §4.7) |
| 16 (chic-v14) | leave-one-out held-out validation of the chic-v12 cross-pool L3 reclassification rule on the 20 chic-v2 paleographic anchors (per LOO iteration: hold one anchor out, treat as unknown, rebuild candidate-value pool per pool, regenerate sha256-keyed control mapping per cell, apply chic-v12 reclassification rule with the held-out anchor's **known** class as reference; in chic-v12 the reference was the chic-v5 proposed class) | mg-7f57 (chic-v14) | **12/20 = 60.0% LOO cross_pool_l3_recovery_rate** to ``tier-2-equivalent``; 0/20 ``tier-3-corroborated``; 8/20 ``tier-3-uncorroborated``; chic-v12's 27.6% (8/29) on the tier-3 set is **-32.4pp BELOW the LOO baseline** | **decisive demotion of cross-pool L3 from a discipline-protecting pillar to a permissive corroboration test**; chic-v12 reclassification on the tier-3 set is **anti-evidentiary** (cross-pool L3 corroborates ground-truth class on known anchors *more often* than chic-v12 corroborates the chic-v5 proposed class on the tier-3 set); chic-v13 within-window context inspection becomes the load-bearing fourth pillar (see §4.7) |

All thirteen outcomes (and the v23 12b matrix follow-up, plus
the chic-v12 / chic-v13 / chic-v14 cross-script extension rows
14–16) are
reproducible from `results/rollup.bayesian_posterior.*.md`, the
supporting provenance breakdowns in
`results/rollup.bayesian_posterior.*.provenance.md`,
`results/consensus_sign_phoneme_map.md`,
`results/rollup.per_inscription_coherence.md`, (v21)
`results/rollup.bayesian_posterior.eteocretan.md` plus
`results/rollup.bayesian_posterior.eteocretan_under_basque.md`,
and (v23) `results/rollup.cross_lm_matrix.md` plus the per-cell
files
`results/rollup.bayesian_posterior.eteocretan.under_{mg,etruscan}_lm.md`
and
`results/rollup.bayesian_posterior.{aquitanian,etruscan,toponym}.under_eteocretan_lm.md`.
The detailed per-pool breakdowns follow.

### 3.2 Validation status by pool

The validation matrix as of v21 (v19 / v20 operate at the
per-inscription level documented in §3.12 / §3.13 rather than
altering pool-level gate outcomes; v21 adds the Eteocretan
substrate pool — the closest-genealogical-relative candidate;
see §3.14):

| pool | own-LM (v10/mg-d26d) | cross-LM (v11/mg-0f97) | third-LM (v12/mg-4664, MycGreek) | curation gate (v14/v15) | bigram control (v18/v21) | status |
|:--|:--:|:--:|:--:|:--:|:--:|:--|
| `aquitanian` | PASS p = 3.22e-05 (basque) | partial p = 0.0205 (etruscan, 5× weaker) | FAIL p = 0.0953 | (see polluted variants) | n/a (v6 unigram control already PASSes) | substrate-LM-specific against unrelated LMs; partial Mediterranean-phonotactic kinship under etruscan LM |
| `polluted_aquitanian` | n/a (v14 build) | n/a | n/a | **PASS p = 2.74e-05** (basque, 50% same-distribution pollution) | n/a | gate is curation-tolerant; top-20 split 9 real / 11 conjectural; within-tail real-vs-conjectural Mann-Whitney p = 0.98 |
| `polluted_aquitanian_{10,25,75}pct` | n/a (v18 build) | n/a | n/a | **PASS** at all three levels (1.5e-04 / 2.7e-04 / 4.3e-02) | n/a | v18 sweep characterizes the gate's curation-sensitivity gradient; see §3.11 |
| `greek_polluted_aquitanian` | n/a (v15 build) | n/a | n/a | **PASS p = 2.01e-03** (basque, 50% Mycenaean-Greek-shape pollution) | n/a | partial within-tail discrimination; top-20 split 13 real / 7 conjectural-greek; real-vs-conjectural-greek MW p = 8.29e-05 |
| `etruscan` | PASS p = 5.21e-04 (etruscan) | FAIL p = 0.591 (basque) | FAIL p = 0.185 (mycenaean_greek) | n/a | n/a (v6 unigram control already PASSes) | substrate-LM-specific; both unrelated LMs collapse the separation |
| `toponym` | FAIL p = 0.92 (v6 unigram control) | (skipped at v10) | (skipped at v10) | n/a | **PASS p = 9.99e-05** (v18 bigram control) | v10 failure was a control-sampler artifact; v18 validates against the stricter bigram null. See §3.10 |
| `linear_b_carryover` | n/a | n/a | **FAIL p = 0.155** at K=20 (mycenaean_greek own-LM positive control) | n/a | n/a | positive control fails production gate; K=5 sensitivity passes at p = 0.0106 |
| `eteocretan` | **PASS p = 4.10e-06** (eteocretan, v21) | partial p = 2.58e-03 (basque, ~600× weaker) | **PASS** p = 1.73e-05 (mycenaean_greek, v23) | n/a | **PASS p = 4.10e-06** (v21 bigram control — built as v18 production default) | strongest gate PASS in the validation series; PASSes under all 4 LMs tested (own > MG ≈ basque > etruscan); closest-genealogical-relative candidate; see §3.14 |

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

#### 3.13.4 Population-level external validation against the Younger scholar-reading set (v22)

v22 (mg-46d5) broadens the §3.13.1 / §3.13.2 footprint to a
**35-entry curated scholar-proposed-reading set** drawn from
Younger's online catalog (canonical scholarly Linear A reference;
*Linear A texts in phonetic transcription*, retrieved 2026-05-04)
and the upstream Schoep 2002 / Salgarella 2020 / Palmer 1995 /
Davis 2014 sources Younger references. Each entry is a
*contextual* claim — "this AB-sequence in this inscription means
this thing in this language" — not a sign-value-only
transliteration; sign-value-only entries (`AB67 = ki`) are
excluded by construction since they are not contextual readings.

The set spans 6 sites (Haghia Triada, Khania, Phaistos, Zakros,
Arkhanes, Psykhro) and 21+ scholar-attested CV combinations
(ku-ro, ki-ro, ja-sa-sa-ra-me, ku-mi-na, mi-na, pi-ta-ja, ma-te,
ku-pa, ku-pa3, ku-ra, ki-ra, ka-pa, ka-ru, da-re, da-ta, di-na,
pa-ja, ta-na, ta-i, a-ra, ku-se), distributed across 15
categories: accountancy_total (5), accountancy_deficit (3),
libation_formula (1), libation_or_onomastic (3), commodity (2),
commodity_or_name (2), name_family (5), name_or_kinship (2),
name_or_suffix (2), name_or_votive (2), personal_name (1),
onomastic_prefix (2), transaction_term (1), lexeme (2),
onomastic (2). Total: 76 AB-sign comparison points.

The comparison strategy follows §3.13.1's PS Za 2 convention
exactly: for each AB sign in each entry's span, take the
per-inscription mechanical modal phoneme (the same v19 per-sign
local-Dirichlet-smoothed consensus over all positive-paired-diff
candidate equations targeting that inscription across the 3
validated substrate pools — aquitanian, etruscan, toponym —
under the same-LM `external_phoneme_perplexity_v0` metric);
compare to the *first phoneme* of the scholarly CV (consonant for
CV syllables, vowel itself for vowel-initial syllables a/e/i/o/u).

| metric | value |
|:--|:--:|
| n entries | 35 |
| n AB-sign comparison points | 76 |
| n with at least one substrate proposal | 45 |
| **aggregate match rate (consonantal first segment)** | **3.95%** (3/76) |
| aggregate match rate (robust: + modal posterior > 0.5 + n_proposals ≥ 2) | 1.32% (1/76) |
| aggregate match rate (full CV — strict) | 2.63% (2/76) |
| per-entry mean | 4.29% |
| per-entry median | 0.00% |
| per-entry max | 50.00% (3 entries) |

Per-entry distribution:

| bucket | n entries |
|:--|---:|
| 0%             | 32 |
| (0%, 20%)      |  0 |
| [20%, 40%)     |  0 |
| [40%, 60%)     |  3 |
| [60%, 80%)     |  0 |
| [80%, 100%]    |  0 |

The 3 entries that score the per-entry max (50% match):

- `ara_ARKH1a` (a-ra → mechanical `a-z`) — the vowel-initial AB08 has consensus modal `a` (matches scholarly `a`); AB60 mechanical `z` does not match scholarly `r`.
- `ara_HT1` (a-ra → mechanical `a-a`) — AB08 again matches `a`; AB60 mechanical `a` does not match `r`.
- `karu_HT2` (ka-ru → mechanical `u-r`) — AB77 mechanical `u` does not match scholarly `k`; AB26 mechanical `r` matches scholarly `r` (the single robust match in the 35-entry set).

The headline 3.95% rate sits squarely in the pre-registered
**strong-null band** (< 5%; the threshold for "reinforces v13 /
v19 verdicts"). Two interpretive points are load-bearing:

1. *The non-zero matches do not constitute partial recovery.* The
   2 `ara_*` matches both fire on the same AB-sign (AB08), whose
   consensus modal phoneme `a` is dominated by Aquitanian-pool
   priors (the substrate alphabet has high `a` mass). This is
   the random-coincidence-on-common-phonemes shape — a vowel-
   initial scholarly syllable hitting a vowel-modal mechanical
   consensus. The single robust match (`karu_HT2` AB26 → `r`) is
   the only entry where the comparison *and* the modal-posterior
   threshold *and* the n_proposals ≥ 2 condition all hold; one
   of 76 is consistent with random chance.
2. *Population-level v.s. single-inscription claim shape.* Before
   v22, §3.13's verdict rested on PS Za 2 alone (one inscription,
   five comparison points, 0/5). v22 extends to 76 comparison
   points across 35 entries; the rate stays in the same band.
   The "internal consensus does not imply external correctness"
   claim is now backed by a population-level external-validation
   set, not a single inscription.

| acceptance band | meaning | observed |
|:--|:--|:--:|
| < 5%   | strong reinforcement of v13 / v19's "internal consensus does not imply external correctness" | **3.95% — observed band** |
| 5–20%  | ambiguous middle case; document with hedging | not observed |
| > 20%  | partial recovery of scholar-meaningful readings; warrants follow-up | not observed |

The result is reproducible from
`results/rollup.scholar_proposed_readings_comparison.md`; the
underlying entry set lives in
`corpora/scholar_proposed_readings/all.jsonl`.

### 3.14 Eteocretan: 4th external-validation pool (v21)

v21 (mg-6ccd) adds a 4th external-validation pool to the framework:
**Eteocretan**, the Greek-alphabet language of post-Linear-A
inscriptions from eastern Crete (~7th–3rd c. BCE; Praisos 1–7,
Dreros 1–2, plus minor short attestations). Eteocretan carries
unique interpretive weight in the validation series: scholarly
consensus treats it as the linguistic descendant of whatever
underlies Linear A — i.e., the **closest-genealogical-relative**
candidate substrate. If substrate-LM-phonotactic kinship between
a candidate substrate and Linear A is meaningful at the
methodological level, Eteocretan should produce the cleanest
signal of any candidate.

The pool was built from a manual transcription of the canonical
Eteocretan corpus (`scripts/build_eteocretan_corpus.py` from
Duhoux 1982 *L'Étéocrétois*, Whittaker 2017, Younger online
catalog): 100 inscriptions; 87 unique word forms; 84 valid pool
entries after filtering V-only tokens. The own-LM
(`harness/external_phoneme_models/eteocretan.json`) is built with
α = 1.0 smoothing — the same setting as the Etruscan LM, chosen
deliberately because the Eteocretan corpus is corpus-limited by
reality (~6× smaller than Etruscan, ~80× smaller than Basque).
The matched control is bigram-preserving (`control_eteocretan_bigram`,
the v18 production default for new pools); no v6 unigram baseline
exists for Eteocretan.

**Acceptance gate result.** Under the own-LM and against the
bigram-preserving matched control:

| substrate pool | control pool | substrate top-K median | control top-K median | MW U | MW p (one-tail) | gate |
|:--|:--|:--:|:--:|---:|:--:|:--:|
| `eteocretan` | `control_eteocretan_bigram` | 0.9712 | 0.7697 | 364.0 | **4.10e-06** | **PASS** |

The Eteocretan pool **PASSes the v10 right-tail bayesian gate at
p = 4.10e-06**, with a substrate-vs-control posterior-median gap
of +0.20 — by both metrics, the *strongest* PASS in the
validation series:

| pool | own-LM gate p | substrate-vs-control posterior-median gap |
|:--|:--:|:--:|
| `aquitanian` (v10) | 3.22e-05 | +0.0296 |
| `etruscan` (v10) | 5.21e-04 | +0.0591 |
| `toponym` (v18, bigram control) | 9.99e-05 | +0.1090 |
| **`eteocretan` (v21, bigram control)** | **4.10e-06** | **+0.2014** |

Top-20 substrate surfaces (Eteocretan word forms, no per-surface
gloss because Eteocretan is undeciphered) include
`iar`, `iarei`, `ine`, `isala`, `mi`, `noi`, `os`, `sam`, `si`,
`wai`, `des`, `ona`, `wantai`, `arka`, `dioi`, `iareion`,
`netamoi`, `ier`, `wow`, `epimere` — every entry attested in the
Eteocretan corpus, most appearing in Praisos 2 (the longest
inscription) or Dreros 1 (the bilingual). The full breakdown is
at `results/rollup.bayesian_posterior.eteocretan.md`.

**Cross-LM negative-control sketch.** Re-scoring the same
substrate + control candidates under the Basque LM (a natural-
language LM unrelated to Eteocretan) produces:

| LM under test | substrate top-K median | control top-K median | MW p (one-tail) | gate |
|:--|:--:|:--:|:--:|:--:|
| `eteocretan` (own LM) | 0.9712 | 0.7697 | 4.10e-06 | PASS |
| `basque` (cross LM) | 0.9615 | 0.8661 | 2.58e-03 | PASS |

The cross-LM gate still passes but the gap shrinks substantially
(median gap +0.20 → +0.10; gate p weakens from 4.10e-06 to
2.58e-03 — ~600× weaker). The own-LM advantage is real and
quantitatively dominant, but a residual natural-language-LM
preference for Eteocretan-shaped surfaces persists. This mirrors
the v11 Aquitanian-under-Etruscan-LM result (substrate-LM-specific
signal but partial Mediterranean phonotactic-kinship overlap).
Output: `results/rollup.bayesian_posterior.eteocretan_under_basque.md`.

**Interpretation.** Eteocretan PASSes the framework's own
gate, and PASSes more strongly than any prior pool — including
the v18 bigram-controlled toponym pool, Aquitanian, and Etruscan.
Under the closest-relative hypothesis (the consensus framing),
this is the expected outcome: *the candidate substrate scholars
already treat as Linear A's linguistic descendant produces the
cleanest right-tail substrate-vs-control gap of any candidate
the framework has tested.* The own-LM-vs-cross-LM separation
ratio (own gap +0.20 vs cross gap +0.10, factor of 2) further
suggests a meaningful Eteocretan-specific component to the
signal beyond a generic natural-language-LM bias.

The result is consistent with — but does not by itself
**establish** — the consensus framing. The framework continues
not to support per-sign decipherment claims (§3.7 / §4.2 / §5),
including not validating any specific Eteocretan-Linear-A
correspondence at the per-sign level. What v21 adds to the
methodology paper is the data point that the framework's
substrate-LM-phonotactic-kinship signal scales with a-priori
genealogical relatedness — Eteocretan (closest-relative) >
toponym (Cretan substrate via Beekes) ≈ Aquitanian / Etruscan
(unrelated Mediterranean substrates). That ordering is the kind
of pattern an independent scholarly review would expect a
working substrate-detection methodology to produce.

**Limitations specific to v21.**

- *Corpus size.* The Eteocretan LM is built from ~87 unique word
  forms (vs Basque ~125,000+ chars; Etruscan ~700 forms;
  Mycenaean Greek 5,638 inscriptions). The α=1.0 smoothing
  partially compensates, but the LM is genuinely noisier than
  the v8–v18 LMs. The strong PASS magnitude despite the noise
  floor is itself a finding: the substrate-vs-control gap is
  large enough to clear the gate even with an LM trained on a
  small fragmentary corpus.
- *No per-sign external-validation comparand.* Unlike Linear-A
  vs `ja-sa-sa-ra-me` (v19), no comparable scholarly
  Eteocretan-Linear-A sequence-mapping comparand exists; the
  Praisos and Dreros bilinguals do not give word-by-word
  translations. v21 is a population-level pool gate, not an
  inscription-level external-validation point.
- *Cross-LM matrix not exhaustive in v21; filled out by v23.* v21
  shipped only the Eteocretan → Basque cross-LM check. v23 (mg-b599)
  fills out the full matrix; see "Cross-LM matrix (v23)" below for the
  combined verdict.
- *Genuinely undeciphered substrate side.* The pool's `gloss`
  field is `unknown` for almost every entry. Surface-level
  semantic-stratum analysis (§3.4 for Aquitanian / Etruscan)
  is not performable for Eteocretan because the substrate side
  itself is undeciphered.

#### Cross-LM matrix (v23)

v23 (mg-b599) fills out the cross-LM matrix that v21 left partial.
Five additional cells join the existing diagonal (own-LM) and
v11 / v12 / v21 cross-LM points: Eteocretan candidates re-scored
under Mycenaean Greek and Etruscan LMs, plus Aquitanian / Etruscan /
toponym candidates re-scored under the Eteocretan LM. The full 4×4
matrix (substrate × LM, sparse on toponym × {Etruscan, Mycenaean
Greek} which v23 did not commission) lives at
`results/rollup.cross_lm_matrix.md`; the headline structure follows.

| substrate ↓ \ LM → | Basque                | Etruscan              | Mycenaean Greek       | Eteocretan            |
|:--                  |:--                    |:--                    |:--                    |:--                    |
| `aquitanian`        | **PASS (own)** p=3.22e-05 / gap +0.030 | PASS p=0.020 / gap +0.039 | FAIL p=0.095 / gap +0.018 | PASS p=0.002 / gap +0.041 |
| `etruscan`          | FAIL p=0.591 / gap +0.008 | **PASS (own)** p=5.21e-04 / gap +0.059 | FAIL p=0.185 / gap +0.012 | FAIL p=0.924 / gap −0.017 |
| `toponym` (bigram ctrl) | **PASS (own)** p=9.99e-05 / gap +0.109 | — | — | PASS p=0.025 / gap +0.043 |
| `eteocretan` (bigram ctrl) | PASS p=2.58e-03 / gap +0.095 | PASS p=6.70e-03 / gap +0.039 | PASS p=1.73e-05 / gap +0.104 | **PASS (own)** p=4.10e-06 / gap +0.201 |

**Headline: own-LM dominance HOLDS for 3 of 4 substrate pools**
(`etruscan`, `toponym`, `eteocretan`). For these pools the own-LM
median posterior gap exceeds every cross-LM gap; foreign LMs
weaken the substrate-vs-control separation in a manner consistent
with the LM's distance from the substrate's phonotactic profile.
Eteocretan under its own LM produces gap +0.20 — the strongest in
the validation series — and the gap shrinks monotonically to +0.10
under the natural-language LMs (Mycenaean Greek, Basque) and
to +0.04 under Etruscan. Etruscan under its own LM produces
gap +0.06 and collapses to ≈0 (or negative under Eteocretan)
under all foreign LMs. Toponym under its own LM (Basque, with
v18 bigram-preserving control) produces gap +0.11 and weakens to
+0.04 under the Eteocretan LM. The pattern matches the prediction
that the framework's right-tail gate is detecting substrate-LM-
phonotactic kinship rather than a generic natural-language-LM bias.

**Aquitanian is the exception: own-LM dominance does NOT hold.**
Aquitanian's own-LM gap is small in absolute terms (+0.030,
roughly an order of magnitude below Eteocretan's), and the
cross-LM cells produce numerically larger gaps (Etruscan +0.039,
Eteocretan +0.041) — though the cross-LM Mycenaean-Greek cell
FAILs at p=0.095. The most plausible reading: Aquitanian's
own-LM gap is below the dynamic range needed for the cross-LM
ordering to be cleanly readable. The matched bigram-preserving
control under Basque is itself extremely Basque-shape because the
Basque LM is large (~125,000+ chars; v8 build manifest); the
substrate-vs-control separation is consequently small, and
foreign LMs that happen to score the matched control more
harshly produce numerically larger gaps without the gate
becoming "more right" about Aquitanian. This is consistent with
Aquitanian's well-known intermediate position in the gap-magnitude
ordering (§3.14, summary table: Eteocretan +0.20 > toponym +0.11
> Etruscan +0.06 > Aquitanian +0.03).

**Two interesting cross-LM observations on the Eteocretan substrate
side.** First, Eteocretan PASSes the right-tail gate under *every*
LM tested (own + 3 foreign), with the smallest gap (+0.039) under
Etruscan. The Mediterranean-substrate-LM-bias hypothesis (cells
1+2 of v23: would Eteocretan under Etruscan PASS strongly because
both are Mediterranean substrate-style LMs?) is **not** supported:
the Eteocretan-under-Etruscan-LM cell produces the *weakest* gap
of the four Eteocretan cells. Etruscan-LM and Eteocretan-LM are
not interchangeable; the Eteocretan LM has Eteocretan-specific
selectivity. Second, the Eteocretan-under-Mycenaean-Greek cell
(gap +0.10) is approximately as strong as the v21
Eteocretan-under-Basque cell (gap +0.095) — both natural-language
LMs unrelated to Eteocretan produce similar mid-strength signal,
suggesting the residual cross-LM gap reflects Eteocretan surfaces'
"natural-language-like-ness" generically rather than a specific
Basque or Greek phonotactic preference.

**Reverse direction (cells 3-5 of v23).** When existing substrate
pools are re-scored under the Eteocretan LM (the closest-
genealogical-relative LM to whatever underlies Linear A), the
Etruscan substrate FAILs the gate with a *negative* median gap
(−0.017, p=0.92) — the Eteocretan LM does not reward Etruscan
phonotactics. Toponym under the Eteocretan LM PASSes (p=0.025,
gap +0.043) but materially weaker than under Basque (gap +0.109);
the Eteocretan LM does reward Cretan-substrate-shape toponyms,
which is consistent with Beekes' framing of Aegean toponyms as
pre-Greek substrate residue but the gap shrinkage indicates
substantial LM-specificity. Aquitanian under Eteocretan PASSes
(p=0.002, gap +0.041) but inside the small-dynamic-range zone
described above. The Eteocretan LM is therefore not a generic
"any substrate-style phonotactics" detector — it has measurable
selectivity, but the selectivity is not as sharp as the v21
own-LM analysis alone suggested.

**Implication for the methodology paper's interpretive framing.**
The cross-LM matrix is consistent with the v21 reading: the
framework's right-tail gate detects substrate-LM-phonotactic
kinship that is genealogical-distance-modulated. The 3-of-4
own-LM-dominance pattern is the load-bearing observation. The
Aquitanian deviation is a small-dynamic-range artifact rather
than a counterexample (no foreign LM produces a *gate-grade*
PASS that the own-LM gate would not also produce, and Aquitanian
under Mycenaean Greek FAILs as expected). Per-cell rollup files:
`results/rollup.bayesian_posterior.eteocretan.under_{mg,etruscan}_lm.md`;
`results/rollup.bayesian_posterior.{aquitanian,etruscan,toponym}.under_eteocretan_lm.md`.

#### Per-inscription cascade-candidate analysis under Eteocretan LM (v24)

v24 (mg-c103) extends v19's per-inscription cascade analysis
(§3.12, originally on aquitanian + etruscan + toponym) to include
v21's Eteocretan pool — the closest-genealogical-relative
substrate, and the strongest own-LM PASS in the project. Two
analyses ship: an **eteocretan-only** aggregation (substrate-LM-
specific test of whether Eteocretan candidates concentrate per-
inscription), and a **four-pool** aggregation
(`aquitanian + etruscan + toponym + eteocretan`, the natural
extension of v19's three-pool). Both populations evaluated:
top-30 right-tail, short ≤5 sign tokens, libation-formula
carriers (PS Za 2). Outputs:
`results/rollup.per_inscription_coherence.eteocretan_only.md` and
`.four_pools.md`; sub-piece v21-equivalent right-tail rollups at
`results/rollup.right_tail_inscription_concentration.eteocretan_only.md`
and `.four_pools.md`. The same `--control-pools` machinery is
threaded through `right_tail_inscription_concentration.py`,
`per_inscription_coherence.py`, and `compare_scholar_proposed.py`
so eteocretan→`control_eteocretan_bigram` substrate pairing
applies automatically when eteocretan is in the pool list.

| view | n cascade candidates | n partial cascades | inscriptions |
|:--|---:|---:|:--|
| **eteocretan-only** | **0** | **0** | — |
| four-pool (aquitanian + etruscan + toponym + eteocretan) | 3 | 1 | KH 10, KH 5, PS Za 2 (cascade); HT 95a (partial) |
| v19 three-pool (baseline) | 3 | 2 | KH 10, KH 5, PS Za 2 (cascade); HT 95a, HT 31 (partial) |

**Eteocretan-only result.** Zero cascade candidates and zero
partial cascades across all three populations. Population A
(top-30 right-tail eteocretan-concentration inscriptions) is
filled to n=30, but every inscription classifies as Noise
(robust fraction < 0.25); the highest robust fraction in the
population is **0.1667** (`HT Zb 158b` and `HT Zb 159`), with
the rest of the population in the 0.00–0.17 band. Population B
is degenerate at n=4 (only 4 short inscriptions have positive
eteocretan paired_diff records). Population C is **n=0**:
PS Za 2 has *zero* positive eteocretan paired_diff records;
under the v21 bigram-preserving control, no eteocretan substrate
surface beats the matched control on any PS Za 2 span. The
Eteocretan candidate count (~2,985 substrate + ~2,635 control
records) is too sparse for per-inscription consensus to form at
the 50% robust bar under eteocretan-LM-only aggregation. This is
the "no cascade candidates emerge at all" outcome the v24 brief
flagged as the unexpected possibility — it is the actual
eteocretan-only result.

**Four-pool result.** Three cascade candidates emerge:
**KH 10, KH 5, PS Za 2** — *the same set as v19's three-pool
result*. Robust fractions are unchanged from v19 to one part in
ten thousand (KH 10 0.5455, KH 5 0.5000, PS Za 2 0.7143).
Mechanical readings on high-coherence positions are identical
to v19; only the low-coherence (`(parens)`) positions show minor
phoneme shifts as eteocretan candidates contribute additional
mass at signs that did not have v19 robust consensus to begin
with. **PS Za 2's mechanical reading on the libation-formula span
is byte-identical between v19 and v24**:
`c-e-a-(ch)-th-(ch)-th-u-u-n-i-(l)-a-(l)`. The eteocretan-LM-
conditioned aggregation does *not* yield a different mechanical
reading on the libation-formula carrier — the substrate-LM
conditioning is invariant on this inscription. HT 31 falls out
of the partial-cascade list because the four-pool right-tail
ranking (with eteocretan top-20 surfaces added to the universe)
reorders the top-30; HT 95a remains as the sole partial cascade.

**External-validation comparison (v22 machinery on v24 outputs).**
Both v24 aggregations were scored against the 35-entry Younger
scholar-proposed-reading set. Output:
`results/rollup.scholar_proposed_readings_comparison.eteocretan_only.md`
and `.four_pools.md`; cascade-candidate-filtered run at
`.four_pools_cascades.md`. Aggregate match-rate comparison:

| view | matches first | n signs | aggregate match rate | n with ≥1 substrate proposal | band |
|:--|---:|---:|---:|---:|:--|
| **v22 three-pool (baseline)** | 3 | 76 | **3.95%** | 45 | STRONG NULL |
| **v24 eteocretan-only** | 0 | 76 | **0.00%** | 19 | STRONG NULL |
| **v24 four-pool** | 3 | 76 | **3.95%** | 45 | STRONG NULL |
| v24 four-pool, filtered to cascade candidates (PS Za 2 only — KH 10 / KH 5 absent from scholar set) | 0 | 5 | 0.00% | 5 | STRONG NULL |

The eteocretan-only aggregation produces 0/76 matches — strict
strong-null, the most negative possible result. Of the 76
AB-sign comparison points, only 19 receive any positive
eteocretan paired_diff record (vs 45 under three-pool); the
other 57 have *no* eteocretan substrate proposal at all because
no eteocretan surface beats the bigram-preserving control on
those inscriptions. The four-pool aggregation lands at *exactly
the same 3/76* the v22 three-pool did, with *exactly the same*
45/76 coverage — adding eteocretan to the substrate pool union
does not change the match count or the coverage. Cascade-
filtered: only PS Za 2 has any scholar-proposed entry among the
three four-pool cascade candidates (KH 10 and KH 5 carry no
contextual scholarly readings); the cascade-filtered headline is
0/5 on PS Za 2's libation-formula span — identical to v19's
single-entry verdict.

**Interpretation.** v24 closes the §3.13/§4.6 narrative
unambiguously. The two informative possibilities the v24 brief
flagged were (a) *eteocretan-LM aggregation surfaces different
cascade candidates with better external-validation match rates
than three-pool* — would have reopened the per-sign decipherment
question — and (b) *eteocretan-LM aggregation produces near-zero
match rates similar to v19/v22* — strongest evidence that the
substrate-LM-phonotactic-kinship signal is structural-only and
not recoverable as readings under any pool, regardless of
genealogical relatedness. The actual outcome combines the
predicted strong-null with an additional sparseness observation:
eteocretan-only aggregation produces *no* cascade candidates at
all (and 0% external match rate), while the four-pool
aggregation reproduces the v19 cascade candidates and the v22
3.95% population-level rate to the digit. Eteocretan, the
closest-relative substrate with the strongest own-LM PASS
(p=4.10e-06, gap +0.20), does not improve external-validation
match rates and does not produce per-inscription consensus that
differs from the existing three-pool view. This is the strongest
evidence yet that the v10/v18/v21 PASSes detect substrate-LM-
phonotactic-kinship at the population level *only*, and that
this kinship signal does not concentrate at any specific Linear A
sign or inscription as a phoneme-recoverable reading — under any
candidate substrate the framework has tested, including the
closest-relative one.

The result also clarifies the v21 narrative: Eteocretan's
strongest-own-LM PASS reflects population-level phonotactic
selectivity (right-tail substrate-vs-control gap +0.20) but does
*not* propagate to a stronger per-inscription cascade signal.
Right-tail population statistics and per-inscription cascade
geometry are different observables; v21's PASS magnitude is
about how Eteocretan-shape phonotactic patterns concentrate in
the substrate side's right tail relative to bigram-preserving
controls, not about how Eteocretan-LM-conditioned candidate
equations agree on specific Linear A signs at specific tablets.
v24 is the first analysis to make that distinction load-bearing
in the manuscript narrative.

---

## 4. Discussion

### 4.1 What the framework detects

After v15 the supportable claim is sharper than at any earlier
point; v21 (mg-6ccd) adds a 4th external-validation data point — and
specifically the *closest-genealogical-relative* candidate substrate —
that produces the strongest pool gate PASS in the validation series.
The framework reliably detects three things:

- **Substrate-LM-phonotactic kinship at the population level, and
  the magnitude scales with a-priori genealogical relatedness.** The
  v10 right-tail gate clears for both Aquitanian (under the Basque
  LM) and Etruscan (under the Etruscan LM) at p < 0.001, and the
  separation collapses cleanly under genuinely unrelated LMs
  (Etruscan p = 0.591 under Basque, p = 0.185 under Mycenaean Greek;
  Aquitanian p = 0.0953 under Mycenaean Greek). The pattern is what
  one expects of substrate-specific signal: a real substrate's
  phonotactic profile is rewarded by the LM trained on that
  substrate's text and not by LMs trained on unrelated languages.
  v21 sharpens this: Eteocretan — the candidate substrate scholarly
  consensus already treats as Linear A's linguistic descendant —
  produces the *strongest* pool PASS yet (p = 4.10e-06; substrate-vs-
  control posterior-median gap +0.20). The cross-LM check (Eteocretan
  candidates under Basque) still passes but ~600× weaker (p = 2.58e-03;
  gap +0.10), so the own-LM advantage is real and quantitatively
  dominant. Concretely, the gap-magnitude ordering across pools is
  Eteocretan (+0.20, closest-relative) > toponym (+0.11, Cretan
  pre-Greek substrate) > Etruscan (+0.06) > Aquitanian (+0.03,
  furthest-out Mediterranean) — the kind of ordering an independent
  scholarly review would expect a working substrate-detection
  methodology to produce. v23 (mg-b599) extends this to a full
  substrate × LM matrix: own-LM dominance (own-LM gap > every cross-LM
  gap) HOLDS for 3 of 4 substrate pools (Eteocretan, Etruscan,
  toponym), with the cross-LM gaps weakening monotonically as the LM
  drifts further from the substrate's phonotactic profile. Aquitanian
  is the exception — its own-LM gap (+0.03) is small enough that
  foreign-LM rank noise produces numerically larger but
  not-gate-grade-cleaner separations. The matrix shape is what
  substrate-LM-phonotactic-kinship detection predicts, and the
  Aquitanian deviation is a dynamic-range observation rather than a
  counterexample (no foreign LM produces a gate PASS that own-LM does
  not; Aquitanian under Mycenaean Greek FAILs as expected). Full
  matrix: `results/rollup.cross_lm_matrix.md`.
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

**Post-v28 framing (the load-bearing register for this section).**
v28's leave-one-out held-out validation (mg-4a7b, full subsection
below) places the chic-v5 framework's mechanical recovery on the
21 LB-carryover anchors at **33.3% aggregate accuracy** (7 of 21),
with **0/3 = 0.0%** on the tier-2 unanimity criterion. Per the
chic-v9 brief's pre-registered thresholds (>70% high; 40-70%
moderate; <40% low), this places the framework in the **low-
agreement / not-validated band** on the Linear A side, parallel
to chic-v9's CHIC-side verdict. The cross-script delta is +13.3
percentage points (LA above CHIC on aggregate accuracy), within
the same band; **the at-chance per-sign behaviour is structural
to the chic-v5 framework rather than CHIC-corpus-specific**,
closing the v28-pre-registered "structural vs corpus-specific"
question in favour of the structural-limitation arm. The
implication for the v22 / v26 leaderboard top-K mechanical-
verification results' per-sign-value claims is a **substantial
credibility downgrade**: the leaderboard top-K substrates were
detected by the same population-level kinship machinery whose
per-sign extraction is at chance; v26's tier-1 → tier-2
mechanical lift on Linear A is a **mechanical finding about the
framework's sign-coverage ladder**, not independent evidence for
the per-sign phoneme-class assignments. The population-level
cross-script claim survives intact (chic-v3 / chic-v4's right-
tail bayesian gate PASS and Spearman ρ=+1.000 cross-script
ranking are population-level signals that do not depend on the
per-sign machinery; v28's LA-side null does not move those
numbers). The §4.6 narrative across the layered v19 / v20 / v22
/ v24 / v26 evidence base — the cascade-candidate framing, the
population-level scholar-set comparison, the leaderboard top-K
verification with its sign-level inverse-verification companion —
is read in the post-v28 register: **leave-one-out held-out
validation against known anchors is the fifth discipline-
protecting pillar, and the chic-v5 framework's per-sign value
extraction proposals on either script are bounded above by that
pillar's verdict**. The per-subsection content that follows is
read in this register.

The methodology paper's headline external-validation result is the
v19 + v20 + v22 cascade-candidate / population-level finding
(§3.12 / §3.13). It is the project's first mechanical comparison
of a framework reading to scholarly proposals *independent* of
the framework's own pipeline. The evidence base has three
layered components:

1. **One cascade-candidate inscription, decisively divergent (v19).**
   On `PS Za 2`, the libation-formula span AB57-AB31-AB31-AB60-
   AB13 yields the framework's confidently-cascading mechanical
   reading `th-u-u-n-i`, divergent from the scholarly
   transliteration `ja-sa-sa-ra-me` on every formula-span sign
   (0/5 consonantal-segment match).
2. **Targeted accountancy follow-up, null comparand (v20).** A
   search for the canonical KU-RO = AB81-AB02 and KI-RO =
   AB67-AB02 sequences in the other two cascade candidates
   (`KH 10`, `KH 5`) finds neither sequence present.
3. **Population-level scholar-set comparison (v22).** A 35-entry
   curated scholar-proposed-reading set drawn from Younger's
   online catalog (76 AB-sign comparison points across 6 sites
   and 21+ scholar-attested CV combinations) yields **aggregate
   match rate 3.95%** (3/76) on the consonantal first segment of
   the scholarly CV, with 32 of 35 entries scoring zero and the
   3 non-zero entries owing their match to vowel-initial
   syllables or chance overlap on common phonemes. The single
   robust match (1/76; modal posterior > 0.5 AND n_proposals ≥
   2) is consistent with random chance. The result sits squarely
   in the pre-registered strong-null band (< 5%).

v24 (mg-c103) extends the layered evidence base by re-running
the per-inscription cascade analysis with v21's Eteocretan pool
included. The eteocretan-only aggregation produces **zero
cascade candidates and a 0/76 (0.00%) aggregate match rate** on
the 35-entry scholar set; the four-pool
(`aquitanian + etruscan + toponym + eteocretan`) aggregation
reproduces v19's three cascade candidates **with byte-identical
high-coherence mechanical readings on PS Za 2** and matches v22's
3/76 (3.95%) aggregate rate to the digit. The eteocretan-LM-
conditioned aggregation does *not* produce a different mechanical
reading on the libation-formula span and does *not* improve the
match rate against scholarly proposals. v24 is therefore a fourth
layer of external-validation evidence: a substrate-LM swap to the
closest-genealogical-relative pool (the strongest a-priori case
in the validation series) leaves the external-validation match
rate unchanged.

That four-layer evidence base — one inscription decisively
divergent (v19), two follow-up cascade candidates with no
comparand (v20), a 35-entry / 76-comparison-point population-
level set with 3.95% aggregate match (v22), and an eteocretan-
LM-conditioned re-run that does not move the match rate (v24) —
is enough to ground the load-bearing methodological claim:

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
enough about its own structure to surface that. The v22
population-level scholar-set comparison (3.95% aggregate over 76
comparison points across 35 entries) extends that
discipline-protection from "one inscription, decisively
divergent" to "population-level decisively divergent" — the
framework does not partially recover scholar-meaningful readings
even when measured across the broader, multi-category Younger
catalog.

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

#### v26 — Linear A side leaderboard top-K mechanical verification (mg-c202)

The §4.6 framing was previously **asymmetric**. The CHIC side
acquired a mechanical-verification companion (chic-v6, §4.7
mg-a557) that pre-registers three external-scholarship sources
and reports per-tier match counts at the leaderboard top-K
extension. The Linear A side never ran the analogous pass at
the leaderboard top-K granularity — v22 (mg-46d5) covered the
*per-inscription consensus* layer (3.95% aggregate) but not the
top-K leaderboard layer. v26 closes that asymmetry.

For each substrate pool with a right-tail bayesian gate PASS
(Aquitanian v10, Etruscan v10, toponym v18, Eteocretan v21),
v26 sources the top-20 substrate surfaces, identifies positive-
paired-diff records targeting Linear A inscriptions where any
top-20 surface participates, applies that surface's full
sign_to_phoneme map (extending the LB-carryover-only
baseline), and runs the chic-v6 three-source check verbatim:
scholar-proposed Linear-A reading match (Source A), Cretan/
Aegean toponym substring match (Source B, length 3–5), and
item-location consistency (Source C). Match criteria are
pre-registered chic-v6-verbatim — no relaxation.

Headline numbers (full output in
`results/rollup.linear_a_top_k_verification.aggregate.md` and
the four per-pool rollups
`rollup.linear_a_top_k_verification.<pool>.md`):

| pool | n top-20 w/ +records | n insc. extended | n insc. w/ match | match rate (extended) | tier-2 lift (insc.) | tier-2 lift (a+b+c hits) | inverse-verifications |
|:--|---:|---:|---:|---:|--:|--:|--:|
| aquitanian | 20 | 40 | 38 | 0.9500 | +5 | +9216 | 29 |
| etruscan | 20 | 42 | 40 | 0.9524 | +6 | +9925 | 22 |
| toponym | 20 | 39 | 39 | 1.0000 | +7 | +14106 | 19 |
| eteocretan | 20 | 42 | 37 | 0.8810 | +5 | +7172 | 30 |

The LB-carryover-only baseline match rate over the full 772-
inscription Linear A corpus is **177/772 = 22.93%**, near-
identical to chic-v6's tier-1 (chic-v2 anchors only) baseline of
22.19% on the 302-inscription CHIC corpus — a structural-
similarity sanity check.

**Each Linear A pool's top-20 extension produces a positive
inscription-count lift (+5 to +7) over the LB-carryover baseline
on its extended-inscription subset, exceeding chic-v6's tier-1
→ tier-2 lift of +3 inscriptions on the CHIC side.** In that
sense the verification methodology is **portable cross-script**:
the leaderboard top-K passes the same external-scholarship test
on the Linear A side that chic-v6's tier-2 passed on the CHIC
side.

**Two structural caveats determine how to read the lift
magnitudes.** First, chic-v6's tier-2 extension added only 3
specific-phoneme overrides corpus-wide (`#001 → wa`, `#012 →
wa`, `#032 → ki`); each Linear A v26 hypothesis adds 5–10
newly-anchored AB signs (the substrate surface is pinned to a
multi-sign Linear A span). The *absolute* hit-count lifts (e.g.
+9216 hits on aquitanian) are therefore much larger than
chic-v6's +20 hits, but this reflects extension density, not
stronger evidence per anchor. The *directional* verdict (lift
positive / negative) is the comparable cross-script signal.
Second, every top-20 surface of every pool is classified
**verified** under the per-surface verification status
(verified = ≥1 source-A/B/C hit across any extended
inscription); none falls into the **unverified** band. This
high verification rate is itself partly structural: the
substrate hypotheses pin many AB signs at once, so per-pool
phoneme-stream slot density rises sharply, and source-B's
3–5-character toponym substrings have many search positions.

The **load-bearing negative-evidence companion** is the per-
pool sign-level inverse-verification table. v26 records all
`(pool, surface, inscription, AB sign)` tuples where the
substrate hypothesis's proposed first-phoneme at an AB sign
disagrees with a scholar entry's proposed first-phoneme at the
same sign in the same inscription, restricted to AB-sign
positions where both hypotheses overlap. Aquitanian produces 29
such cases (concentrated on `AB59`: every top-20 surface that
pinned `AB59` proposed something other than the scholarly `t-`
of `ta`); etruscan 22, toponym 19, eteocretan 30. These are
sign-level *contradictions* of scholarly proposals from the
v22/Younger 35-entry set — a stricter form of negative evidence
than the per-inscription consensus-vs-scholar-set comparison
used by v22, since each line in the v26 inverse table identifies
a specific AB sign position where the substrate's per-sign
proposal conflicts with the published scholarly value.

The combined v22 + v26 picture: the Linear A leaderboard
detects substrate-LM-phonotactic kinship faithfully (the v10/
v18/v21 PASSes), and applying its top-K substrates corpus-wide
produces **mechanical** lift in three external-scholarship
match sources. It also produces sign-level proposals that
**systematically contradict** the published scholarly proposals
where the two overlap. Both signals are real; both are
publishable. Neither one alone supports a decipherment claim,
which remains conditional on Aegean-syllabary specialist review
of the per-pool verified surfaces and the inverse-verification
table.

This v26 paragraph is the §4.6 Linear-A-side analog of the
chic-v6 paragraph in §4.7 (mg-a557). The two together close the
methodology paper's previous asymmetry: the cross-script
verification methodology is now reported at the leaderboard
top-K granularity on both sides.

#### v28 — Linear A side leave-one-out validation of the chic-v5 framework on LB-carryover anchors (mg-4a7b)

The §4.6 framing was previously **asymmetric on held-out
validation**. The CHIC side acquired a held-out validation
companion (chic-v9, §4.7 mg-18cb) that holds each chic-v2
paleographic anchor out of the pool, runs the chic-v5 framework
blind under L1+L2+L3 (L4 excluded as circular), and reports
recovery accuracy. The Linear A side never ran the analogous
LOO pass on its LB-carryover anchor pool. v28 closes that
asymmetry, parallel to how v26 closed the asymmetry on
mechanical-verification.

For each of 21 LB-carryover anchors S (parsed from
`pools/linear_b_carryover.yaml`'s well-attested AB-sign →
phoneme citations; AB123 excluded as conjectural per Younger),
v28 holds S out of the LB-carryover pool, treats S as unknown,
and recomputes L1 (distributional plurality on top-3 nearest
anchors over the four-dimensional Bhattacharyya fingerprint),
L2 (strict-top-1 anchor distance), and L3 (substrate-consistency
under the v21 Eteocretan LM) for S against the reduced 20-anchor
pool. Per-AB-sign distributional fingerprints (`left_neighbor`,
`right_neighbor`, `position`, `support`) are computed over the
full 772-inscription Linear A corpus. L4 is **deliberately
excluded**: the LB-carryover anchor pool's known values are
themselves derived via paleographic similarity to deciphered
Linear B signs (Ventris-Chadwick 1956), so for any anchor S the
L4 line trivially recovers V by construction, exactly mirroring
chic-v9's L4-exclusion rationale. The LM choice for L3 is the
v21 Eteocretan LM in **direct symmetry with chic-v9** (the
strongest pool on both LA and CHIC; LB-carryover anchors are not
naturally partitioned across the v10/v18/v21 substrate pools).

**Headline LA-side LOO accuracy: 7 of 21 anchors recover
correctly = 33.3%.** Above chic-v9's 20% (delta +13.3%) but
**still below the 40% moderate-agreement threshold** the chic-v9
brief pre-registered. The chance baseline for a 6-class taxonomy
is ~16.7%, so 33.3% is **modestly above chance** — comparable
to chic-v9's 20% in being in the low-agreement / not-validated
band, not at the validation threshold. Per-line accuracies
(L1=33.3%, L2=33.3%, L3=9.5%) are each higher on LA than on CHIC
(chic-v9: L1=20.0%, L2=20.0%, L3=5.0%) but the deltas are small:
+13.3 / +13.3 / +4.5 percentage points. L3 is **below chance on
both scripts**, identical in direction across scripts — strong
evidence that L3's near-zero recovery is a property of the
Eteocretan-LM machinery itself (the LM's onset distribution
rewards `na`/`ni`/`no`/`ma`/`me` and `fa`/`fe`/`fi` over the
held-out values' actual classes), not a property of either
corpus.

| metric | LA-side (v28) | CHIC-side (chic-v9) | delta (LA − CHIC) |
|:--|:--:|:--:|---:|
| n anchors run blind | 21 | 20 | +1 |
| n with framework_class == known_class | 7 | 4 | +3 |
| **aggregate LOO accuracy** | **33.3%** | **20.0%** | **+13.3%** |
| chance baseline (6-class taxonomy) | ~16.7% | ~16.7% | 0% |
| L1 (distributional plurality) | 33.3% | 20.0% | +13.3% |
| L2 (strict top-1) | 33.3% | 20.0% | +13.3% |
| L3 (substrate-consistency, Eteocretan LM) | 9.5% | 5.0% | +4.5% |
| n LOO tier-2 (3-of-3 unanimous) | 3 | 3 | 0 |
| **n LOO tier-2 correctly classified** | **0/3 = 0.0%** | **0/3 = 0.0%** | **0%** |

**Tier-2 unanimity classification accuracy is 0/3 on both
scripts.** Each LA-side tier-2 case mirrors a chic-v9 tier-2
case structurally: unanimous-but-wrong, with all three lines
voting the framework's most-typed class (stop or nasal) over
the held-out anchor's actual class. The unanimity criterion does
not require the unanimously-voted class to be correct — under
both scripts, unanimity is achievable on systematic distributional
biases (frequent neighbors and positions cluster anchors of the
same broad class together), and the systematic biases do not
align with held-out anchor values. The three LA-side LOO tier-2
anchors are `AB06 = na` (nasal → stop), `AB08 = a` (vowel →
stop), and `AB27 = re` (liquid → nasal); none of the three
unanimous votes lands on the held-out anchor's actual class.

**Implication for the broader chic-v5 / v22 / v26 framework's
per-sign credibility.** The pre-registered three-way hypothesis
resolves to the **structural-limitation arm**:

1. **The at-chance behaviour is structural to the chic-v5
   framework, not CHIC-specific.** The framework detects
   substrate-LM-phonotactic kinship at the **population level**
   (the v10/v18/v21 PASSes on Linear A; the chic-v3 right-tail
   bayesian gate PASS for Eteocretan against CHIC at p=7.33e-04)
   but per-sign value extraction is below the noise floor on
   both scripts under our held-out validation.
2. **The chic-v5 tier-2 candidates' credibility downgrade (per
   chic-v9 / chic-v10) extends to the v22 + v26 leaderboard
   top-K mechanical-verification results' per-sign-value
   claims.** The leaderboard top-K substrates were detected by
   the same population-level kinship machinery whose per-sign
   extraction is at chance; v26's tier-1 → tier-2 mechanical
   lift on Linear A and chic-v6's analogous +3-inscription /
   +20-hit lift on CHIC are **mechanical findings about the
   framework's sign-coverage ladder**, not independent evidence
   for the per-sign phoneme-class assignments.
3. **The population-level cross-script claim survives intact.**
   chic-v3 / chic-v4's right-tail bayesian gate PASS and
   Spearman ρ=+1.000 cross-script ranking are population-level
   signals that do not depend on the per-sign machinery; v28's
   LA-side null does not move those numbers.

This v28 paragraph is the §4.6 Linear-A-side analog of the
chic-v9 paragraph in §4.7 (mg-18cb). The two together close the
methodology paper's previous asymmetry: held-out validation of
the chic-v5 per-sign value-extraction framework is now reported
on both sides, with **symmetrically negative verdicts** —
low-agreement / not-validated band on both LA and CHIC; 0/3
tier-2 unanimity correct on both. The methodology paper's
post-v28 framing reads: **the chic-v5 framework is a discipline-
protecting protocol that catches per-sign motivated-reasoning
failure modes through pre-registered held-out validation, and
the discipline — not the per-sign output — is the deliverable**.

### 4.7 Cross-script extension: Cretan Hieroglyphic (chic-v0 through chic-v14)

A parallel sub-program (the **chic-v\*** ticket series) extends
the same mechanical-falsifiability discipline to **Cretan
Hieroglyphic** (CHIC), the older sister-script to Linear A
(~1900–1600 BCE; sealstone-dominated, shorter inscriptions, more
fragmentary by support type). The goal is *not* a CHIC decipherment
but a **cross-script methodology test**: re-application of the
infrastructure built for Linear A under a different and more
constrained input distribution (302 mostly-short CHIC inscriptions
on sealstones and clay administrative documents, against a sign
inventory of 131 distinct IDs whose syllabographic / ideogram
partition is itself a research question), to test whether the
substrate-LM-phonotactic-kinship signal the Linear A framework
detects (§3.14, §4.1) is *Linear-A-specific* or *transferable
across scripts under the same a-priori genealogical-relatedness
ordering of substrate candidates*.

This subsection is positioned within the Discussion as the
methodology paper's **cross-script Part B**: it simultaneously
delivers the chic-v0..v14 results and the cross-script
methodological synthesis, parallel in narrative role to the
single-script Discussion §4.1–§4.6. The chic-v5 per-sign
syllable-value extraction framework (chic-v5 below) is the chic
sub-program's per-sign discipline-protecting deliverable —
parallel in role to v13's per-sign coherence verdict on Linear A
(§3.7) — and is reported with the same anti-motivated-reasoning
framing.

The chic sub-program is positioned as a **methodology test**, not
a CHIC decipherment claim. Each ticket is treated the same way as
the Linear A pipeline: outputs are committed, artefacts are
byte-identical on rebuild, and findings are filed in
`docs/findings.md`. The chic-v7 polish pass (mg-9508), the v27
polish pass (mg-b731), and the chic-v10 polish pass (mg-1178, this
document's post-chic-v9 polish pass for journal-submission handoff
of the cross-script paper) are editorial-only and add no new
harness commits.

**Post-chic-v14 framing (the load-bearing register for this
section).** Three layered LOO + per-candidate evidence-grading
results jointly load the §4.7 register:

- *chic-v9 (mg-18cb)*: leave-one-out held-out validation of the
  chic-v5 four-line framework on the chic-v2 anchor pool of 20
  known scholarly values places the framework's mechanical
  recovery at **20.0% aggregate accuracy** (4 of 20), essentially
  at the **~16.7% chance baseline** for a 6-class phoneme
  taxonomy, and at **0/3 = 0.0%** on the tier-2 unanimity
  criterion. Per the chic-v9 brief's pre-registered thresholds
  (>70% high; 40-70% moderate; <40% low), the framework is in
  the **low-agreement / not-validated band**. This is the
  framework-level negative bound on per-sign decipherment.
- *chic-v12 + chic-v13 + chic-v14 (mg-2035 + mg-5261 + mg-7f57)*:
  the cross-pool L3 robustness check chic-v11 introduced for the
  3 chic-v5 tier-2 candidates is extended methodologically
  symmetrically to the **29 chic-v5 tier-3 candidates** (chic-v12)
  and **leave-one-out tested on the 20 chic-v2 anchors** with
  known class as reference (chic-v14). chic-v12 reclassifies 8 of
  29 tier-3 candidates to ``tier-2-equivalent`` (≥1 non-Eteocretan
  substrate LM corroborates the chic-v5 proposed class — same
  band-level evidence structure as chic-v11's surviving tier-2
  `#032`); chic-v14 recovers 12 of 20 known anchors to
  ``tier-2-equivalent`` (60.0% LOO baseline) when the reference
  is ground-truth class. **chic-v12's 27.6% on the tier-3 set is
  -32.4pp BELOW the LOO baseline → cross-pool L3 reclassification
  is anti-evidentiary on the tier-3 set** — cross-pool L3
  corroborates known anchor class *more often* than chic-v12
  corroborates the chic-v5 proposed class on the tier-3 set, so
  cross-pool L3 corroboration alone does not discriminate "true
  class" candidates from "L3-favoured class" candidates.
  **Cross-pool L3 is therefore demoted from a discipline-
  protecting pillar to a permissive corroboration test**, useful
  only in combination with at least one other independent line
  of evidence. chic-v13 supplies that line: within-window context
  inspection on the 8 chic-v12 tier-2-equivalent candidates
  yields **6 consistent / 0 inconsistent / 2 inconclusive on
  corpus state**; **within-window context inspection becomes the
  load-bearing fourth discipline pillar** post-chic-v14, replacing
  cross-pool L3 robustness in that role.

The chic-v14 demotion of cross-pool L3 is itself a discipline-
protecting outcome: the held-out validation pillar (chic-v14)
caught a permissive corroboration axis (chic-v11 + chic-v12
cross-pool L3) before it could load-bear in the methodology
paper, demonstrating that the discipline pillars work. Note
explicitly that the **LA-side cross-pool L3 axis was already
exercised** in v15–v18 (4-pool × 4-LM gates in §3.3 / §3.10 and
the v23 cross-LM matrix in §3.14); the CHIC-side analog now
produces the **same anti-evidentiary verdict** on the tier-3 set
under held-out validation, mirroring v15–v23's cross-LM-matrix
shape findings on Linear A.

The implication for the chic-v5 tier-2 candidate proposals
(`#001 → wa`/glide, `#012 → wa`/glide, `#032 → ki`/stop) is
unchanged from the post-chic-v9 framing: they remain
**"candidate proposals contingent on the framework's currently-
low validation accuracy"**. The new contribution post-chic-v14
is a **per-candidate evidence-graded set across both axes
(cross-pool L3 corroboration + within-window context
inspection)**:

| paired-evidence status | n | identity |
|---|---:|---|
| cross-pool L3 + context-inspection consistent | 7 | `#032` (chic-v11), `#021`, `#005`, `#072`, `#017`, `#039`, `#056` (chic-v13) |
| cross-pool L3 only (context inspection inconclusive on corpus state) | 2 | `#055`, `#065` (chic-v13 inconclusive on fragmentary inscriptions) |
| cross-pool L3 only (context inspection failed) | 0 | (none — chic-v13 found 0 inconsistent) |
| chic-v5 tier-2 / cross-pool L3 fail | 2 | `#001`, `#012` (chic-v11 demoted) |
| chic-v5 tier-3 / cross-pool L3 not corroborated | 17 | tier-3-uncorroborated set |
| chic-v5 tier-3 / Eteocretan-only L3 corroborated | 4 | `#006`, `#033`, `#050`, `#063` (tier-3-corroborated) |

**The framework-level negative is unchanged**. chic-v9's 20.0%
aggregate / 0/3 tier-2 unanimity correct on the chic-v5 four-line
framework remains the headline negative-finding result, and the
v28 + chic-v9 framework-level negative (with chic-v14 now adding
the cross-pool L3 anti-evidentiary verdict on the tier-3 set as a
third LOO data point) is the dominant constraint. v30's
contribution is per-candidate evidence-graded granularity within
the chic-v9-validated low-accuracy band: 7 of 32 evidence-graded
candidates carry paired cross-pool L3 + within-window context-
inspection evidence; 2 inconclusive; 2 demoted; 21 do not clear
both axes. **None of the 7 paired-evidence candidates is
promoted to chic-v2 anchor status or to "domain-expert-confirmed"**;
they remain "candidate proposals pending domain-expert review"
at the same tier as `#032` was post-chic-v11. Promotion to
higher tiers requires specialist review, out of polecat scope.

The candidates do not disappear — chic-v6's small-but-non-zero
+3-inscription / +20-hit tier-1 → tier-2 mechanical-verification
lift is independent of chic-v9's framework-validation result; L4
(cross-script paleographic agreement) was deliberately excluded
from the LOO test as circular by construction but remains a
falsifiable evidence axis contingent on hand-curated extension
from O&G 1996, Salgarella 2020, Decorte 2017, and adjacent
paleography scholarship; chic-v13's within-window context
inspection contributes a fourth axis distinct from L1/L2/L3 — but
the framing across this entire section reads in the post-chic-v14
register: **the chic-v0..v14 sub-program demonstrates that
mechanical scoring + pre-registered falsifiable acceptance gates
+ cross-script transfer + leave-one-out held-out validation +
within-window context inspection is a 5-pillar discipline-
protecting protocol that catches per-sign motivated-reasoning
failure modes (including, via chic-v14, the failure mode of
treating a permissive corroboration axis as a discriminative
gate), and the discipline is the deliverable**. The per-ticket
subsections that follow are read in this register, with chic-v5's
tier-2 candidates and the 7 chic-v13-consistent candidates flagged
as candidate proposals contingent on the chic-v9 + v28 framework-
level verdict rather than as elevated-priority specialist-review
targets.

#### chic-v0 — corpus ingest (mg-99df)

302 of 331 CHIC catalog entries ingested from John Younger's web
edition of CHIC (Olivier & Godart 1996), via the Wayback Machine
snapshot (the live URL has retired). Site distribution skews to
Knossos and Mallia (62% combined). Support-type distribution is
sealstone-dominated. Tokenization: hyphen-joined digit groups →
sign IDs (`#NNN`); standalone digits → `NUM:N`; uncertain
readings → `[?:#NNN]`; illegible → `[?]`. The 29 missing
catalog entries are deferred to a manual-transcription pass.

#### chic-v1 — sign classification (mg-c7e3)

The 131 distinct CHIC sign IDs partition (under the numeric-range
rule of Olivier & Godart 1996, retained in Younger's web edition)
into **96 syllabographic + 35 ideogram + 0 ambiguous**. The
syllabographic frequency distribution is comparable in shape to
Linear A's (heavy-tailed but tractable; CHIC top-10 covers 49% of
sign tokens vs Linear A top-10 at 36%). chic-v1 also enumerates
**20 paleographic anchor candidates** — CHIC syllabographic signs
visually similar to Linear A signs with established Linear B
carryover values. **3 are consensus matches, 10 proposed, 7
debated** (counts cross-checked against
`pools/cretan_hieroglyphic_signs.README.md` and the
`results/chic_sign_inventory.md` paleographic-candidate table by
the chic-v7 audit pass, mg-9508).

#### chic-v2 — anchor inheritance + partial-reading map (mg-362d)

Mechanically applies the chic-v1 candidates as a tier-1 (consensus,
3 anchors) / tier-2 (proposed-or-debated, 17 anchors) anchor pool.
Outputs `pools/cretan_hieroglyphic_anchors.yaml`,
`results/chic_partial_readings.md`, and
`results/chic_anchor_density_leaderboard.md`.

Headline numbers:

- **864 of 1420** syllabographic CHIC sign positions across the
  corpus are anchored — **60.85%** corpus-wide coverage.
- **263 of 302** inscriptions carry ≥1 anchored position; the
  top-30 most-anchored inscriptions are all at coverage = 1.0
  (saturated; tiebreakers go to anchored count, then
  syllabographic count).
- Recurrent anchored short forms: `i-ja-ro` (5 distinct fully-
  anchored sealstones plus many embeddings); `ki-de` (23
  sealstones); `wa-ke` (6 sealstones, including a Samothrace
  cluster). These are known-formulaic seal sequences in CHIC
  scholarship; chic-v2 contributes a **mechanical, reproducible**
  rendering rather than a new claim about them.

A Mycenaean-Greek char-bigram-LM perplexity sanity check
(`results/chic_mg_perplexity_sanity_check.md`) confirms the
anchor-portion phoneme strings are not phonotactically arbitrary
(per-char log-likelihood −2.58 nats; uniform-smoothed baseline is
−3.33), but the absolute value is well above MG-typical (−1.4 to
−1.8 for real Mycenaean Greek under the same LM), consistent with
the substrate-language hypothesis for CHIC. The cross-check is
**informational, not evidential** — the substrate language for
CHIC remains pre-Greek (toponym / Eteocretan / similar), and
chic-v3 will swap in the substrate LMs the lineara harness
already supports.

#### chic-v3 — substrate framework on CHIC, 4 pools, right-tail bayesian gate per pool (mg-9700)

The chic-v3 ticket exercises the full Linear A substrate framework
(Aquitanian, Etruscan, toponym, Eteocretan — the 4 validated pools
from v10 / v18 / v21) against the CHIC syllabographic-only corpus.
The CHIC syllabographic-only token stream is built by filtering the
chic-v0 corpus through the chic-v1 sign classification (drop
ideograms / fractions / numerals / uncertain-ID / wholly-unknown
markers; treat them as structural breaks); the result has 276
inscriptions, 1,258 syllabographic tokens, and 551 maximal
syllabographic blocks (one-quarter the size of Linear A's
~5,000-token corpus). Candidate equations are generated against
CHIC inscription windows under the same generator rules as Linear
A's bulk pipeline; matched controls are reused verbatim from the
Linear A pools (per the chic-v3 brief's option (b) — matched
controls are about substrate phoneme shape, not target-corpus
shape, so reuse keeps the chic-v3 result directly comparable to the
Linear A v10 / v18 / v21 numbers). Score rows are isolated to a
dedicated sidecar
`results/experiments.external_phoneme_perplexity_v0.chic.jsonl`.

Per-pool right-tail bayesian gate verdicts on CHIC:

| pool | LM | n paired windows | median sub posterior | median ctrl posterior | MW p (one-tail) | gate |
|:--|:--|---:|---:|---:|---:|:--:|
| eteocretan | eteocretan | 2,286 | 0.8038 | 0.6927 | 7.33e-04 | **PASS** |
| toponym | basque | 2,599 | 0.7941 | 0.7874 | 4.35e-01 | FAIL |
| etruscan | etruscan | 4,490 | 0.8534 | 0.8758 | 7.20e-01 | FAIL |
| aquitanian | basque | 5,746 | 0.8739 | 0.9106 | 9.37e-01 | FAIL |

**Eteocretan PASSes; the 3 farther-out pools FAIL.** The
realised per-pool ordering on CHIC, ranked by p-value
(stronger-substrate-signal first), is **Eteocretan > toponym >
Etruscan > Aquitanian** — the Linear A monotonic-with-relatedness
ordering reproducing exactly on a different script.

This is the cross-script methodological-novel finding the chic-v3
brief targeted: the framework's PASS/FAIL distinction tracks
candidate-substrate genealogical relatedness to the target
script's underlying language, and that tracking *survives*
cross-script transfer. The Linear A v21 reading — the framework
detects substrate-LM-phonotactic kinship between candidate
substrate and target script — generalises to CHIC. The Eteocretan
PASS magnitude is comparable to the Linear A v21 magnitude
(p≈1e-3 in both cases, on similar-sized paired window sets);
chic-v4 will quantify the cross-script correlation directly.

**Caveats.** CHIC's syllabographic stream is one-quarter the size
of Linear A's; statistical power for the right-tail gate is
correspondingly lower. The Eteocretan PASS clears the threshold by
~2 orders of magnitude in p, so the corpus-size caveat does not
affect that verdict; but the borderline-FAIL pools (especially
toponym at p=0.435) should be read as informative-but-underpowered
rather than definitive — distinguishing "no real signal at the
chic-v3 threshold" from "real signal, insufficient corpus to
detect at α=0.05" requires CHIC corpus expansion or a more
sensitive cross-script test (chic-v4).

**No infrastructure changes.** chic-v3 reuses the v8 metric, the
v18 / v21 control pools, and the v10 right-tail bayesian gate
verbatim. The only new code is the CHIC syllabographic-stream
filter (`scripts/build_chic_syllabographic_corpus.py`) and the
chic-v3 driver (`scripts/chic_substrate_run.py`); a smoke test
(`harness/tests/test_chic_substrate_run.py`) runs the full
pipeline on a 5-record toy and asserts re-runs are byte-identical
+ resume-no-op. This is exactly the "methodologically
straightforward port" the ticket described.

#### chic-v4 — cross-script correlation analysis: Linear A vs CHIC right-tail bayesian gate signals across the 4 substrate pools (mg-c769)

The chic-v4 ticket takes the methodologically novel cross-script step
the chic sub-program was built for: directly compare Linear A's
per-pool right-tail bayesian gate magnitudes (v10 / v18 / v21) to
CHIC's per-pool magnitudes (chic-v3) to test whether the substrate-LM-
phonotactic-kinship signal carries across the two undeciphered Cretan
scripts. The brief pre-registered three competing hypotheses as
descriptive predictions: **H1 substrate-continuity** (the Linear A
monotonic-with-relatedness ordering reproduces on CHIC), **H2 script-
specific contact** (CHIC reflects a different substrate stratum, so
the per-pool ordering differs), and **H0 corpus-characteristic null**
(both scripts produce similar PASS magnitudes regardless of substrate;
magnitude is corpus-driven). None is an acceptance gate; the
contribution is the cross-script comparison itself.

Per-pool gate-magnitude comparison
(`results/rollup.linear_a_vs_chic_substrate_comparison.md`):

| pool | LA gap | LA p | LA gate | CHIC gap | CHIC p | CHIC gate |
|:--|---:|---:|:--:|---:|---:|:--:|
| eteocretan | +0.2015 | 4.10e-06 | PASS | +0.1111 | 7.33e-04 | **PASS** |
| toponym | +0.1090 | 9.99e-05 | PASS | +0.0067 | 4.35e-01 | FAIL |
| etruscan | +0.0591 | 5.00e-04 | PASS | -0.0224 | 7.20e-01 | FAIL |
| aquitanian | +0.0296 | <1e-04 | PASS | -0.0367 | 9.37e-01 | FAIL |

Cross-script Spearman rank correlation on the per-pool gap = **ρ =
+1.000** (perfect rank-preservation). The Linear A pool ranking
(Eteocretan > toponym > Etruscan > Aquitanian) reproduces exactly
on CHIC. Mean overlap of the top-20 substrate surfaces between the
two scripts' right-tail leaderboards across the 4 pools = **0.47**
(38 surfaces appear in both top-20s out of 80 substrate-side slots
across the 4 pools combined). Per-substrate-surface continuity
(Pearson on overlapping surfaces, ceiling-clustering caveat noted in
the rollup): Eteocretan +0.45 / toponym +0.14 / Etruscan +0.03 /
Aquitanian −0.28 — strongest for Eteocretan, the closest-
genealogical-relative substrate, and weakest for the more distant
external substrates.

**Headline verdict: H1 (substrate-continuity) is the data's most
consistent reading.** The cross-script Spearman ρ=+1.0 on per-pool
gap rules out H2 (which predicts a different ordering); the magnitude
spread of ~2 orders of magnitude in p across the 4 pools on each
script, combined with the identical rank ordering between scripts,
rules out H0 (which predicts corpus-characteristic-only patterning).
Eteocretan PASSes the gate on **both** scripts, the only pool to do
so on CHIC; the other three pools' rank ordering is preserved on
CHIC even though their absolute signal-to-noise drops below the
α=0.05 threshold under CHIC's smaller corpus (~1,258 syllabographic
tokens vs Linear A's ~5,000). The supportable claim for the extended
methodology paper is therefore: **the substrate-LM-phonotactic-
kinship signal the framework detects is cross-script — the per-pool
PASS/FAIL distinction tracks candidate-substrate genealogical
relatedness to the target script's underlying language, and that
tracking survives transfer between Linear A and CHIC.** Only the
strongest pool (Eteocretan, closest-genealogical-relative candidate)
clears the formal gate threshold on CHIC's smaller corpus, but the
**rank** signal — preserved exactly across scripts — is the
strongest H1-vs-H0 discriminator the cross-script comparison
produces.

This is the chic sub-program's central methodological deliverable.
The framing the chic-v4 verdict supports for the extended
methodology paper is: **mechanical substrate-LM-phonotactic-kinship
detection methodology demonstrated cross-script on Linear A and CHIC;
substrate continuity signal correlates between the two undeciphered
Cretan scripts at Spearman ρ=+1.0 on per-pool gate gap, with mean
top-20 substrate-surface overlap of 0.47.** The chic-v4 cross-script
deliverable is descriptive — no decipherment claim is added or
strengthened by it; what *is* strengthened is the case that the
framework's PASS signal on Linear A is not Linear-A-corpus-specific
but a substrate-LM-phonotactic-kinship signature that generalises to
the older sister-script under the same scoring infrastructure.

#### chic-v5 — per-sign syllable-value extraction framework for unknown CHIC syllabographic signs (Eteocretan-LM-anchored, four-line-of-evidence discipline) (mg-7c6d)

The chic-v5 ticket builds the methodologically delicate per-sign
counterpart to chic-v3's population-level gate. The chic-v3 PASS on
Eteocretan (p = 7.33e-04) and the chic-v4 cross-script Spearman
ρ = +1.0 jointly established Eteocretan as the substrate whose
phonotactic shape carries a detectable signal on the CHIC
syllabographic stream; chic-v5 mechanically asks, for every CHIC
syllabographic sign that is not a chic-v2 paleographic anchor (76 such
unknowns out of 96 syllabographic signs total), whether four
independent lines of evidence converge on a single proposed phoneme
class. **The discipline is the deliverable, not the count of tier-2
candidates.** The framework is built to fail loudly when the lines
diverge — that's the anti-motivated-reasoning property the
methodology paper has insisted on since v13's per-sign coherence
failure.

The four lines (`scripts/build_chic_v5.py`, with full per-sign tables
in `results/chic_value_extraction_leaderboard.md`,
`results/chic_anchor_distance_map.md`,
`results/chic_substrate_consistency.md`,
`harness/chic_sign_fingerprints.json`,
`pools/cretan_hieroglyphic_signs.distributional.yaml`):

1. **Distributional plurality.** Per-sign Bhattacharyya similarity to
   each chic-v2 anchor across four fingerprint dimensions
   (`left_neighbor`, `right_neighbor`, `position`, `support`); the
   top-3 nearest anchors vote on phoneme class by plurality.
2. **Anchor-distance (strict top-1).** The single-closest anchor's
   phoneme class. Same fingerprint machinery as line 1, different
   aggregation; lines diverge when the top-1 differs from the
   top-3 plurality.
3. **Substrate-consistency under Eteocretan LM.** For every candidate
   phoneme value V drawn from the union of the anchor pool's
   Linear-B carryover values plus bare vowels — filtered to only
   values whose first character is in the Eteocretan phoneme
   inventory, which excludes the glide values `ja` and `je`
   (Eteocretan vocabulary has no `j` phoneme; the LM would fold it
   to OOV) and leaves a 20-value pool — the chic-v2 anchor mapping
   extended with `(unknown_sign → V)` is scored against a
   class-disjoint deterministic-permutation control (sha256-keyed;
   no RNG) under the v21 Eteocretan LM. The per-class mean
   paired_diff picks the line-3 winning class. The 20-value pool
   breaks down as 5 vowel / 8 stop / 4 nasal / 2 liquid / 1 glide
   (`wa` only), with no fricatives — an inevitable consequence of
   the chic-v2 anchor pool's contents (no fricative-onset Linear-B
   carryover values are paleographically anchored on CHIC).
4. **Cross-script paleographic.** Where the chic-v1
   PALEOGRAPHIC_CANDIDATES list flags a Linear A counterpart for the
   unknown sign with a known/proposed value. **Silent for all 76
   unknowns** in chic-v5: the chic-v1 paleographic-candidate list is
   precisely the seed for the chic-v2 anchor pool, so by construction
   no unknown carries a paleographic note. This is documented as a
   methodological limitation rather than papered over; line 4
   contributes 0 votes for every unknown, and tier-2 in chic-v5
   therefore requires unanimous agreement of the three remaining
   non-silent lines (1, 2, 3). Domain-curated extension of line 4 is
   the natural chic-v6 target.

Tier classification is mechanical (≥3 of 4 agreeing → tier-2; 2 of 4
→ tier-3; 1 of 4 → tier-4; 0 → untiered) with exact phoneme-class
identity as the agreement predicate (`vowel`, `stop`, `nasal`,
`liquid`, `fricative`, `glide` — coarser than phonemes, since the
framework's per-sign resolution is unlikely to be more granular).
Unknown signs with corpus frequency below n=3 are marked **untiered**
on the discipline-protecting grounds that their distributional
fingerprints are too thin (≤2 occurrences) to support meaningful
Bhattacharyya similarity.

Headline counts (76 unknowns, n=3 frequency floor):

| tier | meaning | n |
|:--|:--|---:|
| tier-1 | chic-v2 anchor (already established; carried over) | 20 |
| **tier-2** | ≥3 of 4 lines agree on a phoneme class — **candidate proposal contingent on the framework's currently-low validation accuracy (chic-v9, below)** | **3** |
| tier-3 | 2 of 4 lines agree — suggestive but insufficient for a candidate proposal | 29 |
| tier-4 | 1 of 4 lines yields a class — single line of evidence; not a proposal | 17 |
| untiered | no line of evidence yields a class (frequency < 3 floor) | 27 |

The three tier-2 candidates:

| sign | freq | proposed class | L1 nearest-anchor | L2 nearest-anchor (sim) | L3 best-value (paired_diff) |
|:--|---:|:--|:--|:--|:--|
| `#001` | 4 | glide | `#057` | `#057` (`je`, BC=0.5533) | `wa` (+0.002212) |
| `#012` | 5 | glide | `#042` | `#042` (`wa`, BC=0.6611) | `wa` (+0.005331) |
| `#032` | 9 | stop | `#061` | `#061` (`te`, BC=0.6021) | `ki` (+0.004579) |

**The chic-v5 methodology paper framing must lead with the
discipline, not the count.** The supportable claim is: a four-line-
of-evidence framework, mechanically derived from chic-v2 + chic-v3
machinery + per-sign distributional fingerprints under a
Bhattacharyya similarity metric and Eteocretan LM substrate-
consistency scoring, surfaces **3 candidate proposals at tier-2** out
of 76 unknown CHIC syllabographic signs, where tier-2 requires three
independent lines (one of the four canonical lines being silent for
chic-v5 by construction) to converge on a single coarse phoneme
class. **Post-chic-v9, these are candidate proposals contingent on
the framework's currently-low validation accuracy** (the same
machinery that produced them recovers known anchor classes at
20.0% aggregate / 0/3 on the tier-2 unanimity criterion under
leave-one-out; see chic-v9 below). They remain candidate proposals
pending domain-expert review by an Aegean-syllabary specialist —
they are not decipherment claims — but the credibility weight the
methodology paper attaches to them is bounded above by the chic-v9
framework-validation accuracy. The framework's per-sign resolution
is class-level, not phoneme-specific, and the line 1 / line 2
distributional machinery is built on the chic-v2 anchor pool's
fingerprints rather than a fully-independent paleographic ground
truth. The 29 tier-3 signs
are the next-stratum candidates (29 of 76 unknowns showing 2-of-3
non-silent line agreement); these are the ones where chic-v6's
hand-curated paleographic-line extension would most plausibly raise
to tier-2 by adding a fourth confirming vote.

**Per-sign substrate-consistency paired_diffs are uniformly small
(top values in the +0.002 to +0.005 nat-per-char range).** This is
qualitatively consistent with the chic-v3 corpus-size caveat (~1,420
syllabographic positions across 288 partly-fragmentary inscriptions
is small for per-sign value extraction even when the substrate-
pool-level signal is strong) and with the chic-v4 cross-script gap-
magnitude observation (CHIC's Eteocretan gap +0.111 is roughly half
of Linear A's +0.201). The line-3 paired_diff magnitudes shouldn't
be over-read as decipherment-grade per-sign signal; they are *a
ranking of candidate phoneme values by substrate-consistency*, not
absolute confidence. The tier classification, not the magnitude,
carries the chic-v5 discipline.

**Disagreement bookkeeping + L3 systematic class bias.** Per the
brief's anti-motivated-reasoning instruction, the script reports
per-sign votes from each line even where they disagree (full
per-sign breakdown in the leaderboard `## Per-sign tier verdict`
table). Above the n=3 frequency floor (49 of 76 unknowns): lines
1 and 2 (distributional plurality vs strict top-1) agree on 26
of 49 (53%) and diverge on 23 of 49 (47%) — the natural
consequence of the top-3-plurality vs strict-top-1 distinction;
the lines share the same fingerprint machinery but differ in
aggregation. The line-3 class distribution is heavily skewed:
26/49 votes for `nasal`, 20/49 for `glide`, 2/49 for `liquid`,
1/49 for `stop`, and 0/49 for `vowel` or `fricative` — qualitatively
consistent with the Eteocretan LM's bigram distribution rewarding
common Eteocretan-vocabulary onset patterns (`na`/`ni`/`no`/
`ma`/`me`; pool unigram counts m=32, n=32) and with the
candidate-value pool composition (smaller class pools producing
higher mean paired_diffs by construction). The L3 bias is a
**property of the framework, not random noise** — the methodology
paper should disclose it explicitly. It also means line 3 is
under-discriminating in isolation; the tier-2 / tier-3 discipline
is precisely what filters out the L3 systematic bias by requiring
independent confirmation from at least one distributional line.

**`docs/findings.md` (mg-7c6d entry)** records the per-line vote
counts, the tier-2 / tier-3 candidate lists, the
phoneme-class-taxonomy choice, and the 3 tier-2 candidates' per-line
evidence breakdown. Per AGENTS.md (cited explicitly per the
chic-v5 brief, recalling chic-v1's mg-c7e3 missed-update incident
that mg-0ea1 had to backfill retroactively): the findings update is
a non-negotiable acceptance blocker for the chic sub-program, not
an optional accompaniment to the experiment ticket.

#### chic-v6 — mechanical verification pass on chic candidate proposals (mg-a557)

Daniel's reframing reminder (2026-05-05) repositioned chic-v6 from
"domain-expert review" (out of polecat scope) to **mechanical
verification before specialist review** (in scope). The cryptography
framing: verification of "is this doing something?" is much easier
than hypothesis generation. chic-v5 *generated* candidate proposals
from internal evidence (4 lines of evidence converging on phoneme
classes); chic-v6 *verifies* whether applying those proposals to the
corpus produces hits against three external-scholarship sources we
already have ingested. Match rate becomes a verification signal that
can promote candidate proposals toward "verified-by-scholarship"
status without invoking an Aegean-syllabary specialist's judgment.

**The chic-v6 deliverable is NOT a decipherment claim.** It is a
verification-rate report against three pre-registered match sources;
specialist judgment is still required to advance any matched
candidate from "matched" to "decipherment". The match criteria
(`scripts/build_chic_v6.py` module-level docstring;
`results/chic_verification_match_rates.md` "Pre-registered match
criteria" section) are fixed BEFORE any match counts are computed,
to prevent post-hoc relaxation.

The three external-scholarship match sources:

- **Source A — scholar-proposed Linear-A readings.**
  `corpora/scholar_proposed_readings/all.jsonl` (35 entries from
  v22, e.g. `ku-ro`, `ki-ro`, `ja-sa-sa-ra-me`). A scholar entry
  with `ab_sequence` of length k matches a CHIC inscription iff
  there exists a contiguous run of k syllabographic-class tokens
  within a single DIV-bounded segment such that for each position
  i: (a) the token is anchored at the active tier and the token's
  literal first-phoneme equals the scholar's
  `scholarly_first_phoneme[i]`, OR (b) the token is a class
  placeholder whose class equals
  `classify_value(scholarly_first_phoneme[i])`. All k positions
  must match.
- **Source B — toponym substring.** `pools/toponym.yaml` (112
  toponym surfaces from v18). For every surface, generate
  substrings of length 3–5 (substring length 1–2 excluded as a
  noise-floor convention). Match in a single DIV-bounded phoneme
  stream char-by-char: literal char by string equality;
  class-onset slot by class-membership; vowel slot by
  vowel-membership.
- **Source C — item-location consistency.** Per-inscription
  `site` field. Generate substrings of length 3–5 from the
  lowercased site surface; apply the source-B procedure but
  only against the inscription's own phoneme stream and only
  against substrings of its own site name.

Four extended-partial-reading tier levels (full per-inscription
table in `results/chic_extended_partial_readings.md`):

- **tier-1** — chic-v2 paleographic-anchor pool only (20 anchors).
- **tier-2** — tier-1 ∪ chic-v5 tier-2 candidates with chic-v6
  L3-substrate-consistency-best specific phoneme overrides
  (`#001 → wa`, `#012 → wa`, `#032 → ki`).
- **tier-3** — tier-2 ∪ chic-v5 tier-3 candidates as class-level
  placeholders (`[STOP:#NNN]`, `[GLIDE:#NNN]`, …); 29 added signs.
- **tier-4** — tier-3 ∪ chic-v5 tier-4 candidates as class-level
  placeholders; 17 more added signs.

Per-tier match-rate table (full output in
`results/chic_verification_match_rates.md`):

| tier | n_inscriptions | n_with_any_match | match_rate_any | n_with_a | n_with_b | n_with_c | total_a | total_b | total_c |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| tier-1 | 302 | 67 | 0.2219 | 30 | 48 | 0 | 216 | 74 | 0 |
| tier-2 | 302 | 70 | 0.2318 | 31 | 51 | 0 | 233 | 77 | 0 |
| tier-3 | 302 | 161 | 0.5331 | 96 | 154 | 12 | 828 | 1803 | 18 |
| tier-4 | 302 | 207 | 0.6854 | 111 | 202 | 23 | 1019 | 3957 | 40 |

Tier-over-tier verification lift in `n_inscriptions_with_any_match`
(positive lift = tier-N extension produces matches not attainable
under tier-(N-1)):

| from | to | lift (n_inscriptions) | lift (total a+b+c hits) |
|:--|:--|--:|--:|
| tier-1 | tier-2 | +3 | +20 |
| tier-2 | tier-3 | +91 | +2339 |
| tier-3 | tier-4 | +46 | +2367 |

**The headline interpretation must lead with the discipline.** The
tier-2 to tier-1 lift is the cleanest signal: tier-2 adds three
*specific-phoneme* overrides (`#001 → wa`, `#012 → wa`,
`#032 → ki`), and the lift is **+3 inscriptions** with any match
(67 → 70) and **+20 total hits** across the three sources. This is
a small but non-zero verification-grade signal: the three chic-v5
tier-2 candidate proposals do produce mechanical hits against
external scholarship that were not attainable under chic-v2 anchors
alone. The match enumerations include source-A hits where the
chic-v5 tier-2 candidate participates in the matched run (e.g.
CHIC inscriptions where `[#012:wa]` followed by an anchored stop
matches the scholar `wa-...` family), and source-B hits where the
specific phoneme `ki` inside `#032`'s extended reading hits a
toponym substring containing `ki` (e.g. `kid`, `kin`, `nik`,
`liki`).

**The tier-3 and tier-4 lifts (+91 and +46 inscriptions
respectively, with hit counts in the thousands) are dominated by
class-level matching's structural permissiveness, not by
verification-grade evidence.** Class-level matching expands the
match space substantially: a `STOP` placeholder matches any of
`{p, b, t, d, k, g, q}`, a `GLIDE` placeholder matches any of
`{j, w, y}`, and so on (full class → consonant set table in
`results/chic_verification_match_rates.md`). The hit counts
therefore confound (a) the tier-3/4 candidates being
correctly-classed, (b) the class-level criterion being permissive
enough to produce many incidental alignments. Without a
phonotactically-matched permutation control of the tier-3/4 class
assignments, the tier-3/4 lift is not interpretable as
verification-grade signal — only as a *ceiling* on what verification
the class-level proposals could possibly produce. The tier-1 →
tier-2 lift is the load-bearing chic-v6 result; the tier-3 / tier-4
numbers are reported for completeness and to explicitly disclose
the class-level-matching ceiling, not as evidence in their own
right.

**Per-match enumeration (tier-4) is committed** at
`results/chic_verification_match_rates.md` "Per-match enumeration"
section. Every matched scholar reading, every matched toponym
substring, and every matched site-substring is listed with the
inscription id, the matched signs/substring, and the match modes
(exact-phoneme vs class-level). This gives a concrete list of
"candidate proposals with mechanical external verification" — but
specialist judgment is still required to elevate any of these from
matched to decipherment.

**Source-C item-location consistency emerges only at tier-3+** (12
inscriptions match a substring of their own site name at tier-3,
23 at tier-4). This is consistent with the source-B and source-A
ceiling effects: source-C is structurally a constrained subset of
source-B (only own-site substrings count), so its lift is bounded
above by the source-B lift, and the source-C lift inherits the same
class-level-matching permissiveness caveat. The discipline-protecting
reading: source-C produces zero matches at tier-1 / tier-2, so even
the verification-grade tier-2 lift does not extend to per-inscription
geographic consistency on this corpus.

**Post-chic-v9, the methodology paper's chic-v5 / §4.7 framing is
"candidate proposals contingent on the framework's currently-low
validation accuracy"** (downgraded from the pre-chic-v9 framing
"candidate proposals pending domain-expert review by an Aegean-
syllabary specialist"). The chic-v6 mechanical-verification result
narrows the framing slightly: chic-v5's three tier-2 candidates
*do* clear a low-bar mechanical verification check (small but
non-zero lift), while the larger tier-3 / tier-4 strata's apparent
verification lift is dominated by class-level-matching
permissiveness and does not constitute verification-grade evidence
in the absence of a permutation control. A specialist review
remains the load-bearing next step for advancing any of these from
"matched" to "decipherment". **The chic-v9 LOO test (mg-18cb,
below) is what loads the post-chic-v9 framing onto the candidates**:
the same framework that proposed the three tier-2 candidates
recovers known chic-v2 anchor classes at only 20.0% aggregate
accuracy under leave-one-out (and 0/3 on the tier-2 unanimity
criterion), so the chic-v6 +3-inscription / +20-hit verification
lift cannot be read as independent corroboration of the
candidates' specific phoneme values — it remains a small
mechanical signal whose load-bearing weight is bounded above by
the chic-v9 framework validation accuracy. chic-v6's lift stays
on the page as independent evidence that the three candidates do
produce mechanical hits against external scholarship; it is just
no longer carrying the weight of "specialist-review priority".

**Inputs / outputs.** Inputs:
`corpora/cretan_hieroglyphic/all.jsonl` (chic-v0; 302 inscriptions),
`pools/cretan_hieroglyphic_anchors.yaml` (chic-v2),
`results/chic_value_extraction_leaderboard.md` (chic-v5),
`corpora/scholar_proposed_readings/all.jsonl` (v22),
`pools/toponym.yaml` (v18). Outputs:
`results/chic_extended_partial_readings.md`,
`results/chic_verification_match_rates.md`,
`results/experiments.chic_verification_v0.jsonl`. Determinism: no
RNG; same inputs → byte-identical outputs (re-run hash-stable, see
`scripts/build_chic_v6.py`).

**Linear A side companion (v26, mg-c202).** The §4.6 paragraph
under "v26 — Linear A side leaderboard top-K mechanical
verification" reports the analogous Linear A pass: pre-registered
chic-v6-verbatim match criteria, applied to the v10/v18/v21
leaderboard top-20 substrate surfaces. Each Linear A pool produces
a positive inscription-count lift exceeding chic-v6's +3 tier-2
lift (+5/+6/+7/+5 across aquitanian/etruscan/toponym/eteocretan)
plus a sign-level inverse-verification table that contradicts the
scholarly proposals at 19–30 AB-sign positions per pool. The two
together close the methodology paper's previous CHIC/Linear A
asymmetry on mechanical verification at the leaderboard top-K
granularity.

#### chic-v8 — Malia altar stone (and other CHIC + Linear A dual-script artifacts) bilingual analysis (mg-dfcc)

Daniel's reminder (2026-05-05): the Malia altar stone is referenced in
scholarship as bearing both Linear A and CHIC inscriptions; can the
LA-side reading constrain CHIC-side phoneme values at parallel
positions, providing a fifth line of evidence (L5, LA-constraint)
beyond the four chic-v5 lines, and potentially promoting some chic-v5
tier-3 (29 signs) or tier-4 (17 signs) candidates to tier-2?

The chic-v8 polecat (mg-dfcc) verified the artifact identification,
surveyed both v0 corpora for genuinely-dual-script artifacts, and ran
the per-sign promotion analysis. The build script is
`scripts/build_chic_v8.py`; outputs are
`results/chic_dual_script_bilingual_leaderboard.md` and
`results/chic_v8_promoted_candidates.md`.

**Headline: 0 new tier-2 candidates derived via the bilingual
extension on the v0 corpora.** The Malia altar stone is **CHIC #328**
(Mallia, offering_table, 16 signs; partial transcription confidence)
per the Olivier-Godart 1996 catalog; per Younger's web edition and
Olivier-Godart this artifact is **unilingual CHIC**, not dual-script.
The Linear A v0 corpus has no Mallia stone-vessel inscription (its 20
Mallia entries are 17 administrative tablets + 3 roundels), and a
systematic survey of the sites carrying inscriptions in both corpora
(Arkhanes, Haghia Triada, Knossos, Mallia, Phaistos, Zakros) finds no
genuinely-dual-script artifact (i.e. no artifact bearing parallel
inscriptions in both CHIC and Linear A on the same physical object).

**The fifth line of evidence (L5) is therefore silent for all 76
unknown CHIC syllabographic signs by corpus state**, mirroring chic-
v5's L4 (cross-script paleographic) which is silent by chic-v1
construction. With two of the five lines silent, the 4-of-5 promotion
rule reduces to chic-v5's 3-of-3 (L1+L2+L3 unanimity) — byte-identical
to the chic-v5 tier-2 criterion. **No new tier-2 candidates are
produced. The chic-v5 tier-2 candidate count remains 3** (`#001 → wa`,
`#012 → wa`, `#032 → ki/stop`), unchanged.

This is a legitimate publishable null result (chic-v8 brief, Goal
section: `N = 0 new tier-2 candidates: bilingual constraint either
doesn't apply (no truly parallel positions) or produces conflicting
constraints. Either is informative.`). The methodology paper's
framing should:

1. **Disclose the corpus state**: the v0 ingest does not include
   any genuinely-dual-script artifact, even where scholarship
   discusses candidates (e.g. debated dual-script seals from
   Phaistos / Knossos discussed in Salgarella 2020 §5.3 and
   Decorte 2017 are not in the v0 corpora because sealstone CMS
   catalog ingest is itself a separate sub-program).
2. **Position L5 as a falsifiable additional line of evidence**,
   contingent on the underlying corpus including genuinely-dual-
   script artifacts. The line is structured so that a future
   corpus-expansion ingest pass (full GORILA Za-series; manual
   O&G 1996 cross-check on near-#312 / near-#328 entries; CMS
   sealstone-catalog dual-script entries) could reactivate it
   without modifying the discipline.
3. **Refuse to invoke genre-parallels** (CHIC #328 vs LA libation
   tables PS Za 2 / SY Za 4) as load-bearing evidence. The
   Duhoux-style hypothesis that the stereotyped Linear A libation
   formula (`a-ta-i-*301-wa-ja ja-sa-sa-ra-me ja-ti i-da-ma-te
   ...`) may have a CHIC counterpart on stone-vessel inscriptions
   is a scholarly conjecture, not consensus; and position
   alignment between CHIC #328's 16 signs and the LA libation
   tables' 16 / 13 signs is conjectural in the absence of
   confirmed parallel content. The genre-parallel section is
   reported in the leaderboard for completeness but contributes
   zero L5 votes — relying on it would re-introduce the motivated-
   reasoning failure mode the methodology paper has insisted on
   protecting against since v13's per-sign coherence verdict and
   v22/v24's external-validation null.
4. **Flag the corpus-expansion path**: a future ingest pass adding
   the full GORILA Za-series and any genuinely-dual-script CMS
   sealstone-catalog entries would reactivate the bilingual
   extension and could in principle produce non-zero L5 votes.
   Filed under `corpus-expansion` for chic-v9+ / pm-lineara
   triage.

The chic-v8 result extends the chic sub-program's anti-motivated-
reasoning discipline cleanly: the framework is structured to *fail
loudly when the lines diverge or the evidence axis is silent*. With
L4 silent for all 76 unknowns by chic-v5 construction and L5 silent
for all 76 unknowns by chic-v8 corpus state, the chic-v5 tier-2
candidate count (3) and chic-v6 mechanical-verification result
(small but non-zero +3-inscription / +20-hit tier-1 → tier-2 lift,
with the larger tier-3/4 lifts caveated for class-level-matching
permissiveness) carry forward as the chic sub-program's per-sign
deliverables — though the chic-v9 LOO validation (mg-18cb, below)
subsequently downgrades the credibility of the 3 tier-2 candidates
to "contingent on the framework's currently-low validation
accuracy" by placing the framework's mechanical recovery on known
anchors at 20.0% aggregate / 0/3 on the tier-2 unanimity criterion.
chic-v8 adds a methodologically-coherent zero contribution
documented as a corpus-state observation.

**Determinism.** No RNG, no network, no system-clock dependency;
same inputs produce byte-identical outputs across re-runs (verified
at chic-v8 build time, 2026-05-05; md5 hash stability across two
consecutive runs). `docs/findings.md` (mg-dfcc entry) is committed
in the same merge as the harness artifacts, per AGENTS.md NON-
NEGOTIABLE acceptance-blocker rule and the chic-v1 (mg-c7e3) missed-
update precedent that mg-0ea1 had to backfill retroactively.

#### chic-v9 — leave-one-out held-out validation of the chic-v5 framework on chic-v2 anchors (mg-18cb)

Daniel's observation (2026-05-05): the strong result of the chic
sub-program would be proposing 3 new values for Cretan Hieroglyphs
(chic-v5 tier-2: `#001 → wa`/glide, `#012 → wa`/glide,
`#032 → ki`/stop) **especially if we independently hypothesised known
values**. The italicised clause is the methodological move
chic-v0..v8 never made: held-out validation of the chic-v5 framework
against the chic-v2 anchor pool (20 signs with scholarly-known
phoneme values), where ground truth lets us measure recovery
accuracy when the framework is run blind.

**Method (`scripts/build_chic_v9.py`, full per-anchor table in
`results/chic_v9_loo_validation.md`).** For each chic-v2 anchor S
with known scholarly value V: remove S from the chic-v2 anchor pool
(reduced 19-anchor pool); treat S as unknown; rebuild the
candidate-value pool from the reduced 19-anchor pool plus bare
vowels (filtered by the Eteocretan phoneme inventory, chic-v5
convention); compute L1 (distributional plurality on top-3 nearest
anchors), L2 (strict-top-1 anchor distance), L3 (substrate-
consistency under the v21 Eteocretan LM) for S against the reduced
pool; classify into a 3-line tier (3-of-3 unanimous = LOO tier-2;
2-of-3 = tier-3; 1-of-3 = tier-4; 0 = untiered); compare the
framework's proposed class to V's known class. **L4 (cross-script
paleographic) is deliberately excluded**: chic-v1's
PALEOGRAPHIC_CANDIDATES list is the source of the chic-v2 anchor
pool, so for any anchor S the L4 line trivially recovers V by
construction. Including L4 would inflate accuracy by circularity;
the L1+L2+L3-only LOO is the honest test the chic-v9 brief
specifies.

**Headline LOO accuracy: 4 of 20 anchors recover correctly = 20.0%
aggregate accuracy.** The chance baseline for a 6-class taxonomy is
~16.7%, so the framework's L1+L2+L3 mechanical recovery on known
cases is essentially **at chance**. Per the chic-v9 brief's
pre-registered thresholds (>70% high; 40-70% moderate; <40% low),
this places the chic-v5 framework's recovery accuracy in the
**low-agreement / not-validated band**.

| metric | value |
|:--|---:|
| n anchors run blind | 20 |
| n with framework_class == known_class | 4 |
| **aggregate LOO accuracy** | **20.0%** |
| chance baseline (6-class taxonomy) | ~16.7% |
| n LOO tier-2 (3-of-3 unanimity) | 3 |
| **n LOO tier-2 correctly classified** | **0/3 = 0.0%** |
| n LOO tier-3 (2-of-3) | 14 |
| n LOO tier-4 (1-of-3) | 3 |
| n LOO untiered | 0 |

**Per-line accuracy decomposition:**

| line | n_correct/n_total | accuracy |
|:--|:--:|---:|
| L1 (distributional plurality, top-3) | 4/20 | 20.0% |
| L2 (strict-top-1 anchor distance) | 4/20 | 20.0% |
| L3 (substrate-consistency under Eteocretan LM) | 1/20 | 5.0% |
| **L1+L2+L3 consensus (framework class)** | **4/20** | **20.0%** |

L1 and L2 are tied at 20% (both reading the same Bhattacharyya
fingerprint distance machinery, differing only in aggregation); L3
at 5% is **below chance**, consistent with chic-v5's own diagnosis
of a systematic class bias in the Eteocretan LM (the LM's onset
distribution rewards `na`/`ni`/`no`/`ma`/`me` over the actual
held-out values' classes, regardless of whether the held-out value
is in fact a nasal). The voted L1+L2+L3 consensus inherits the
distributional lines' 20% — L3's near-zero recovery cannot pull
the consensus below the L1+L2 floor because L3 disagrees noisily,
not systematically wrongly in the same direction.

**Tier-2 classification accuracy is 0/3 = 0.0%.** Three anchors
unanimously classified at LOO tier-2 (3-of-3 agreement on a top
class): `#031 = ro` (liquid; framework called stop), `#042 = wa`
(glide; framework called stop, with L3 structurally unable to
recover glide because removing #042 strips the only glide value
from the candidate pool), `#053 = me` (nasal; framework called
glide). **Every LOO tier-2 call disagrees with the known class.**
The tier-2-or-3 looser test (≥2 of 3 lines voting for the *known*
class) recovers 4/20 = 20.0%, byte-identical to the consensus
accuracy.

**Implication for the chic-v5 tier-2 candidates (`#001 → wa`/glide,
`#012 → wa`/glide, `#032 → ki`/stop).** The same framework that
proposed these three new values recovers known anchor classes at
**20% aggregate** and **0% on the tier-2 unanimity criterion** when
run blind. The chic-v5 / chic-v6 / chic-v8 framing must downgrade
the three candidates accordingly. The methodology-paper framing for
§4.7 should now read: **"The chic-v5 framework's three tier-2
candidate proposals are mechanically derived from a four-line-of-
evidence machine that, when run blind on the chic-v2 anchor pool of
20 known cases, recovers known phoneme classes at 20% aggregate
(near the 16.7% chance baseline for a 6-class taxonomy) and
correctly classifies zero of the three anchors that emerge as
tier-2 unanimous under the held-out reduced pool. The three new
candidates are therefore **candidate proposals contingent on the
framework's currently-low validation accuracy**, not mechanical
proposals deserving elevated specialist-review priority."** This is
substantially weaker framing than the chic-v5 / chic-v6 commits
implied; the chic-v9 LOO test is what would have caught a
mis-specified framework before journal submission. Honest reporting
on the negative result is the discipline-protecting outcome the
chic sub-program has emphasised since chic-v1's missed-update
incident (mg-c7e3, backfilled by mg-0ea1).

**Additional caveats.** Small N (20-anchor LOO) limits statistical
resolution; ±5% differences fall within the binomial noise floor
for this sample size. The headline 20% should be read as a point
estimate with substantial uncertainty, not a precise calibration
figure — but the qualitative reading (recovery near the chance
baseline; 0/3 tier-2 correct) is robust to that uncertainty. The
anchor-pool composition is itself a curated set (the chic-v1
paleographic-candidate list); the LOO test measures recovery on
**anchor-shaped** signs, which is the relevant target population
for the methodology, but the 76 unknown signs the framework
proposes against may differ systematically (e.g. lower frequency,
different distributional shape) — the 20% chic-v9 number bounds
above what the framework should be expected to achieve on the
unknown pool. L4 exclusion is non-negotiable: including L4 would
make the test circular; the L1+L2+L3-only setup is the honest one.

**Determinism.** No RNG. Same inputs → byte-identical
`results/chic_v9_loo_validation.md` across re-runs (md5 stability
verified at chic-v9 build time, 2026-05-05). The L3 control-phoneme
selection inherits chic-v5's sha256-keyed permutation construction.

**`docs/findings.md` (mg-18cb entry)** records the 20-anchor LOO
table, the per-line decomposition, and the tier-2 classification
accuracy, plus the explicit downgrade of chic-v5 tier-2-candidate
credibility. Per AGENTS.md (cited explicitly per the chic-v9 brief,
recalling chic-v1's mg-c7e3 missed-update incident that mg-0ea1 had
to backfill retroactively): the findings update is a
non-negotiable acceptance blocker.

#### chic-v11 — additional within-scope evidence on the 3 chic-v5 tier-2 candidates: cross-pool L3 robustness + #032 ku-pa context inspection (mg-d69c)

chic-v9 (above) gave a framework-level negative on the chic-v5
machinery; chic-v11 asks the two remaining additional-evidence
questions in scope for a polecat against the 3 individual
candidates. The pre-registered tests are mechanical (no specialist
judgment beyond cross-referencing committed metadata).

**Test 1: Cross-pool L3 robustness.** chic-v5's L3 substrate-
consistency line was scored under the v21 Eteocretan LM only. If
the L3 votes for the 3 candidates are an Eteocretan-LM artifact, we
expect them to disagree under the other 3 substrate pools' LMs.
chic-v11 reruns the chic-v5 L3 machinery byte-identically except
for the (substrate-pool, LM) dispatch — 12 cells = 3 candidates ×
4 pool-LM dispatches (aquitanian → basque, etruscan → etruscan,
toponym → basque, eteocretan → eteocretan; chic-v3/chic-v5
convention). The candidate-value pool is rebuilt per pool because
the chic-v5 phoneme-inventory filter is per-substrate. Output:
`results/chic_v11_cross_pool_l3.md`.

| candidate | chic-v5 class | top cross-pool class | vote split | verdict | agrees with chic-v5 |
|:--|:--|:--|:--|:--|:--:|
| `#001` | glide | stop (3/4) | stop=3 / glide=1 | mostly LM-robust (3 of 4 agree, on stop) | ✗ |
| `#012` | glide | stop (2/4) | stop=2 / glide=1 / nasal=1 | weak agreement (2 of 4) | ✗ |
| `#032` | stop | stop (2/4) | stop=2 / glide=1 / nasal=1 | weak agreement (2 of 4) | ✓ |

**Per-candidate cross-pool L3 reading:**

- `#001 → wa`/glide: under aquitanian, etruscan, toponym pools, L3
  votes **stop** (winning value `ta` in all 3); under eteocretan
  alone, L3 votes glide (winning value `wa`). The chic-v5 glide
  vote for `#001` is **an Eteocretan-LM-specific artifact**: 3 of
  4 substrate-pool LMs reject the glide reading and converge on
  stop. This is a cross-pool L3 negative.
- `#012 → wa`/glide: 2 stop (etruscan, toponym), 1 nasal (aquitanian),
  1 glide (eteocretan). The chic-v5 glide vote for `#012` is
  supported by **only 1 of 4 LMs** (eteocretan, the chic-v5
  default); the cross-pool L3 winning class is stop with weak
  agreement (2/4). This is a cross-pool L3 negative — `#012`'s
  glide vote is also LM-specific to Eteocretan.
- `#032 → ki`/stop: 2 stop (etruscan, eteocretan), 1 glide
  (aquitanian), 1 nasal (toponym). The chic-v5 stop vote for `#032`
  is **supported by 2 of 4 LMs**, including the chic-v5 default
  Eteocretan (winning value `ki` matches chic-v5 exactly) plus
  Etruscan (winning value `ti` — same class, different value).
  Cross-pool L3 weakly corroborates the stop reading; the verdict
  is `weak agreement (2 of 4)` but **agrees with chic-v5**, unlike
  `#001` and `#012`.

**Test 2: #032 ku-pa context inspection.** chic-v6 produced a
+3-inscription / +20-hit tier-1 → tier-2 verification lift on the
source-A scholar-proposed-Linear-A-readings test. The portion
attributable to `#032 → ki + #013 → pa` literal/literal lands on
**1 CHIC inscription (CHIC #057) with 4 scholar-entry hits** from
the ku-pa name-family / ka-pa transaction-term family attested in
the four Linear A tablets HT 1, HT 16, HT 102, HT 110a. Output:
`results/chic_v11_032_ku_pa_context.md`.

The mechanical metadata cross-check:

- **Source Linear A tablets** (HT 1, HT 16, HT 102, HT 110a): all
  four are `genre_hint = accountancy`, `support = tablet`,
  `period = LM IB`, `site = Haghia Triada`. The scholarly readings
  `ku-pa` (name family / commodity prefix), `ku-pa3` (variant),
  and `ka-pa` (recurring transaction term) are extracted by
  Younger's online edition from Hagia Triada accountancy tablets
  in their native-corpus genre.
- **Matched CHIC inscription** (CHIC #057, Knossos, support `bar`,
  partial transcription): the partial reading under chic-v2 anchors
  + `#032 → ki` is `wa #029 ki #011 / NUM:10 / #079 ki pa / NUM:20
  / i [?:mu] #034 / NUM:20 / #011 #029 #037 / NUM:50`. The matched
  `(#032, #013)` literal pair sits in the second DIV-bounded
  segment as `#079 ki pa`, **immediately followed (after the next
  DIV) by `NUM:20`** — the canonical CHIC accountancy formula
  structure (sign-run = entry, followed by a quantity numeral).
  The inscription's overall structure is four DIV-bounded
  numerical entries (NUM:10 / NUM:20 / NUM:20 / NUM:50), confirming
  the accountancy reading on the CHIC side as well.

**Combined #032 verdict.** The chic-v6 ku-pa-family lift
attributable to `#032 → ki` is **corroborated by inscription-level
context on both sides of the match**: scholarly readings in their
native LM IB Hagia Triada accountancy context on the Linear A
source side; the matched CHIC bar inscription with the canonical
sign-run-followed-by-numeral accountancy-formula structure on the
CHIC target side. This is contextual corroboration of the chic-v6
mechanical lift specifically for `#032 → ki`, **not validation of
the chic-v5 framework as a whole** — chic-v9's framework-level
LOO accuracy (20.0% / 0/3 tier-2 unanimity correct) is unaffected.

**Per-candidate post-chic-v11 status (combined chic-v5 + chic-v6 + chic-v9 + chic-v11):**

- **`#001 → wa`/glide.** chic-v9 LOO-framework negative; chic-v11
  cross-pool L3 actively undermines (3 of 4 substrate-pool LMs
  vote stop, not glide; the chic-v5 glide vote is an Eteocretan-LM
  artifact); chic-v6 produced **no `#001 → wa`-attributable lift**
  (the chic-v6 enumeration shows `#001 → wa` did not enter any
  source-A literal-match pair). Net: `#001` retains the weakest
  evidentiary basis of the three candidates. **Status: weakened
  beyond the chic-v9 generic downgrade.**
- **`#012 → wa`/glide.** chic-v9 LOO-framework negative; chic-v11
  cross-pool L3 weakly undermines (only 1 of 4 LMs supports glide;
  cross-pool top is stop at 2/4 weak agreement); chic-v6 produced
  **no `#012 → wa`-attributable lift**. Net: same shape as `#001`.
  **Status: weakened beyond the chic-v9 generic downgrade.**
- **`#032 → ki`/stop.** chic-v9 LOO-framework negative; chic-v11
  cross-pool L3 weakly corroborates (2 of 4 LMs vote stop, including
  the chic-v5 default Eteocretan with byte-identical `ki` winning
  value, plus Etruscan with `ti` winning value); chic-v6 lift
  contextually corroborated on both sides of the `(#032, #013)`
  match (accountancy-tablet source + accountancy-formula CHIC
  context). Net: `#032` retains the strongest evidentiary basis of
  the three candidates by every chic-v11 axis, while still
  inheriting the chic-v9 framework-level negative. **Status:
  partially corroborated within polecat scope — but the
  framework-level chic-v9 negative remains the dominant constraint.**

**Implication for the methodology paper's per-candidate framing.**
The chic-v10 generic downgrade (chic-v5 tier-2 candidates →
"candidate proposals contingent on the framework's currently-low
validation accuracy") was applied uniformly to all three candidates.
chic-v11 produces an **asymmetric refinement** of that framing:

- For `#001` and `#012`, chic-v11 adds an additional negative axis
  (cross-pool L3 disagrees with chic-v5's class) on top of the
  chic-v9 generic downgrade. The methodology paper's per-candidate
  framing for these two should explicitly note the cross-pool L3
  result as an additional Eteocretan-LM-artifact concern.
- For `#032`, chic-v11 adds a partial positive axis (cross-pool L3
  weakly corroborates the stop class; chic-v6 lift contextually
  corroborated). The methodology paper's per-candidate framing for
  `#032` can note this asymmetry — `#032` is the strongest of the
  three under polecat-scope mechanical evidence — without lifting
  the chic-v9 framework-level constraint that would let the
  candidate clear the journal-submission bar.

The combined post-chic-v11 framing remains: **none of the three
candidates clears specialist-review elevation under the
chic-v9-validated framework's currently-low accuracy band**, but
within that band the relative evidentiary basis is now ranked
`#032 > #001 ≈ #012` rather than uniform.

**`docs/findings.md` (mg-d69c entry)** records the 12-cell cross-
pool L3 table, the ku-pa context-inspection metadata, the
per-candidate post-chic-v11 status, and the asymmetric methodology-
paper-framing implication. Per AGENTS.md: the findings update is a
non-negotiable acceptance blocker.

**Determinism.** chic-v11 inherits chic-v5's L3 sha256-keyed
permutation construction and operates on committed input artifacts;
re-running `scripts/build_chic_v11.py` produces byte-identical
result files (md5 stability verified at chic-v11 build time,
2026-05-06).

#### chic-v12 — cross-pool L3 robustness on the 29 chic-v5 tier-3 candidates (mg-2035)

chic-v11 (above) ran the chic-v5 L3 substrate-consistency line
under each of the 4 substrate-pool LMs on the 3 chic-v5 **tier-2**
candidate proposals and produced sharp per-candidate
differentiation: `#032` weakly corroborated cross-pool (2 of 4
LMs vote stop); `#001` and `#012` actively undermined as
Eteocretan-LM glide artifacts. chic-v12 scales the same robustness
check to the **29 chic-v5 tier-3 candidates** — the L1+L2-but-not-
L3-Eteocretan agreement subset (23 candidates), plus the 6 L1+L2-
disagree subset where the chic-v5 consensus class is via L1-or-L2
+ Eteocretan-L3 agreement.

The methodological question chic-v12 asks: does any tier-3
candidate have the same evidence structure as the surviving
tier-2 (`#032`) — three independent lines plus ≥ 1 non-Eteocretan
substrate-LM corroboration — under the same chic-v11 cross-pool
L3 axis? The 29 × 4 = 116-cell matrix is byte-identical to
chic-v11 except for the candidate list. Outputs:
`results/chic_v12_cross_pool_l3.md` (per-candidate × per-LM table
+ per-candidate per-class mean paired_diff details + bail-or-
context-inspection block), `results/chic_v12_tier3_summary.md`
(top-of-file count table + per-candidate one-line summary +
verdict).

Reclassification bands per the chic-v12 brief:

- **`tier-2-equivalent`** — ≥1 non-Eteocretan substrate LM
  corroborates the chic-v5 proposed class. Same evidence
  structure as `#032`.
- **`tier-3-corroborated`** — only Eteocretan-L3 corroborates
  the chic-v5 proposed class. For the 23 L1+L2-agree tier-3
  candidates this is structurally impossible (Eteocretan-L3
  disagrees by chic-v5 construction). For the 6 L1+L2-disagree
  tier-3 candidates this is the chic-v5 baseline state by
  construction.
- **`tier-3-uncorroborated`** — no LM's L3 corroborates the
  chic-v5 proposed class.

Headline reclassification counts:

| reclassification | n |
|:--|--:|
| **tier-2-equivalent** | **8** |
| tier-3-corroborated | 4 |
| tier-3-uncorroborated | 17 |
| **total tier-3** | **29** |

The 8 `tier-2-equivalent` candidates are `#005`, `#017`, `#021`,
`#039`, `#055`, `#056`, `#065`, `#072`. Their `corroborated_by`
sets vary from 1 of 3 non-Eteocretan LMs (`#017` etruscan only;
`#039` toponym only; `#056` etruscan only) up to 3 of 3 (`#021`
aquitanian + etruscan + toponym, the strongest case). The 4
`tier-3-corroborated` candidates are `#006`, `#033`, `#050`,
`#063` — the L1+L2-disagree subset where Eteocretan-L3
corroborates the chic-v5 proposed glide class by construction
and no non-Eteocretan LM additionally agrees. The 17
`tier-3-uncorroborated` candidates exhaust the L1+L2-agree
subset where the cross-pool L3 axis adds nothing beyond chic-v5's
L1+L2 distributional agreement.

**Verdict.** The chic-v12 reclassification rate is large enough
(8 of 29 tier-3 candidates → tier-2-equivalent) that the chic-v12
brief's pre-registered bail rule applies on the within-window
context inspection: the brief expected ≤ 5 candidates and
pre-registered a bail at > 5 because that count is a scale signal
worth surfacing rather than a mechanical N candidates to inspect.
The scale signal itself is the chic-v12 finding: **the cross-pool
L3 axis is meaningfully more permissive than the Eteocretan-only
L3 axis chic-v5 used.** For tier-3 candidates whose chic-v5
proposed class lies in a non-Eteocretan substrate-LM's high-
probability bigram region (typically `stop` for the basque LM
under aquitanian / toponym; typically `nasal` for either basque
or etruscan), at least one non-Eteocretan LM is structurally
likely to vote the proposed class regardless of the underlying
truth. This is the same methodological caveat the chic-v9 LOO
test surfaced for the Eteocretan LM in isolation (L3 recovery
1/20 = 5%, below the ~16.7% chance baseline for a 6-class
taxonomy), now extended: the cross-pool L3 axis as a whole shares
the systematic class bias.

**Differential evidentiary strength among the 8 tier-2-equivalent
reclassifications is non-trivial.** `#021 → nasal` is the
strongest case (3 of 3 non-Eteocretan LMs corroborate, plus
Eteocretan-L3 by L1+L2-disagree-via-Eteo construction = 4 of 4
LMs vote nasal); `#005`, `#055`, `#065`, `#072` carry 2-of-3
non-Eteocretan corroborations on stop; `#017`, `#039`, `#056`
are 1-of-3. By contrast the chic-v11 surviving tier-2 (`#032`)
carries 1-of-3 non-Eteocretan corroboration (etruscan) **plus**
Eteocretan-L3 itself, for 4 of 5 mechanical lines (chic-v5 L1
+ L2 + Eteo-L3 + Etruscan-L3) all voting stop — no chic-v12
tier-2-equivalent matches `#032`'s overall mechanical-lines
tally; the evidentiary structure is bandwise-equivalent (≥ 1
non-Eteocretan LM corroborates) but per-line vote counts differ.

**Implication for the methodology paper's per-candidate framing.**
The chic-v11 asymmetric refinement (`#032 > #001 ≈ #012`) is now
extended with a tier-3 evidence-grading layer:

- `#032` retains its position as the chic sub-program's strongest
  per-candidate mechanical evidence basis (cross-pool L3
  corroborated by Eteocretan + Etruscan; chic-v6 ku-pa context
  corroborated on both sides; chic-v11).
- 8 chic-v5 tier-3 candidates reclassify to `tier-2-equivalent`,
  meaning they have the same band-level evidence structure as
  `#032` (≥ 1 non-Eteocretan substrate-LM corroborates) but
  differ in per-line vote tallies and lack the chic-v6 ku-pa
  context corroboration `#032` carries.
- 17 chic-v5 tier-3 candidates reclassify to
  `tier-3-uncorroborated`, meaning the cross-pool L3 axis adds
  no support beyond chic-v5's L1+L2 distributional agreement.
- 4 chic-v5 tier-3 candidates reclassify to
  `tier-3-corroborated`, retaining only the chic-v5 baseline
  state.

The framework's discrimination claim now spans **n = 32**
evidence-graded candidates (3 chic-v5 tier-2 + 29 chic-v5
tier-3) with **9 cross-pool L3 corroborated by ≥ 1 non-
Eteocretan substrate LM** (`#032` chic-v11 + 8 chic-v12
tier-2-equivalents), **4 chic-v5-baseline tier-3-corroborated**,
and **17 cross-pool L3 uncorroborated**. The chic-v9 framework-
level negative (LOO accuracy 20.0% / 0/3 tier-2 unanimity
correct) is unchanged; chic-v12's contribution is per-candidate
evidence-grading granularity within the chic-v9-validated low-
accuracy band. **(Post-chic-v14 caveat: chic-v14's LOO test of
the cross-pool L3 reclassification rule on the 20 chic-v2
anchors recovers known-class to ``tier-2-equivalent`` at 60.0%,
so the 9-candidate count above represents per-candidate
*permissive corroboration* evidence rather than a discriminative
gate verdict; the load-bearing per-candidate axis is now the
within-window context inspection chic-v13 supplies on top of the
chic-v12 cross-pool L3 corroboration. See chic-v14 below.)**

**Pre-registered chic-v13 candidate.** The bail on within-window
context inspection at 8 > 5 tier-2-equivalents is itself a
pre-registration for a chic-v13 follow-up: run the within-window
context inspection on a stratified sample of the 8 tier-2-
equivalent candidates (stratified on `corroborated_by` size:
1-of-3 vs 2-of-3 vs 3-of-3 non-Eteocretan corroboration) and
re-evaluate the per-candidate evidence weighting under the
cross-pool L3 axis. Out of chic-v12's polecat budget; pm-lineara
triage call.

**`docs/findings.md` (mg-2035 entry)** records the 116-cell
cross-pool L3 reclassification table, the per-candidate
`corroborated_by` + `reclassification` columns, the bail-on-
context-inspection rationale, the differential-evidentiary-
strength reading, and the implication for the methodology paper's
per-candidate framing. Per AGENTS.md: the findings update is a
non-negotiable acceptance blocker.

**Determinism.** chic-v12 inherits chic-v5's L3 sha256-keyed
permutation construction. Re-running `scripts/build_chic_v12.py`
produces byte-identical output (md5 stability verified at
chic-v12 build time, 2026-05-06):
`results/chic_v12_cross_pool_l3.md` md5
`0e6444da401d69fd7f8af7fcec0a403c`;
`results/chic_v12_tier3_summary.md` md5
`4fa90790d73f3348bad4a5376ff2aaa5`.

#### chic-v13 — within-window context inspection on the 8 chic-v12 tier-2-equivalent candidates (mg-5261)

chic-v12 (above) bailed on the within-window context inspection
when the tier-2-equivalent count exceeded the brief's pre-
registered threshold (8 > 5) and pre-registered the deferral as
a chic-v13 follow-up ticket. chic-v13 (mg-5261) executes the
deferred inspection, applying the chic-v11 `#032 → ki` ku-pa
context inspection methodology
(`results/chic_v11_032_ku_pa_context.md`) to all 8 chic-v12
tier-2-equivalent candidates. For each candidate: pick 1–3
high-density host inscriptions, render with chic-v2 anchors
substituted and the candidate as a class-level placeholder
(`[stop:#NNN]`, `[N:#NNN]`), and check whether the rendered
reading produces a result consistent with the surrounding
accountancy / sealing / sealstone-formula structure on the
chosen inscriptions and whether it contradicts canonical CHIC
sealstone formulas (`i-ja-ro`, `ki-de`, `wa-ke`) or any chic-v2
anchor's known value.

Headline counts (out of 8 input candidates):

| metric | value |
|:--|--:|
| `n_consistent` | **6** |
| `n_inconsistent` | **0** |
| `n_inconclusive` | **2** |

Per-candidate verdict:

| sign | freq | proposed | corroborated_by (non-Eteo) | verdict |
|:--|--:|:--|:--|:--|
| `#021` | 3 | nasal | aquitanian, etruscan, toponym (3 of 3) | **consistent** |
| `#005` | 48 | stop | aquitanian, toponym (2 of 3) | **consistent** |
| `#055` | 5 | stop | aquitanian, toponym (2 of 3) | **inconclusive** |
| `#065` | 3 | stop | aquitanian, toponym (2 of 3) | **inconclusive** |
| `#072` | 7 | stop | etruscan, toponym (2 of 3) | **consistent** |
| `#017` | 6 | nasal | etruscan (1 of 3) | **consistent** |
| `#039` | 7 | stop | toponym (1 of 3) | **consistent** |
| `#056` | 52 | stop | etruscan (1 of 3) | **consistent** |

Of the 8 chic-v12 tier-2-equivalent candidates from the
post-chic-v12 narrative above, **6 (`#021`, `#005`, `#072`,
`#017`, `#039`, `#056`) pass within-window context inspection,
2 (`#055`, `#065`) are inconclusive on corpus state, and 0 are
disconfirmed**. The strongest within-window context evidence
falls on `#072 → stop` (two `[stop:#072]-de NUM` accountancy
formula entries at Knossos bar CHIC #065, mirroring the chic-v11
`#032`-`#013 = ki-pa` ku-pa NUM-following structure on CHIC #057
directly), `#056 → stop` (multiple `[?] [stop:#056] NUM` entries
at Knossos bar CHIC #061, including one fragment where
`[?:#034] [stop:#056]` directly precedes the canonical
`019-049 = ke-de` formula plus NUM:1), and `#021 → nasal`
(three-fold cross-site recurrence of the formula
`031-021-061 = ro-[N]-te` at Mallia sealing CHIC #149, Mallia
seal CHIC #197, and Knossos accountancy bar CHIC #059, the
latter with the formula in direct adjacency with the canonical
`044-049 = ki-de` sealstone formula). The 2 inconclusive
verdicts (`#055`, `#065`) reflect honest under-determination on
corpus state — both signs occur predominantly in
`fragmentary`-confidence inscriptions, and `#065`'s only
`clean`-confidence occurrence is itself in a variant-bracketed
transcription `{065}` (CHIC #174).

**Cross-pool L3 corroboration alone, in the absence of
supporting within-window context evidence, is not sufficient for
class-level value confirmation**: chic-v13 demonstrates that 2
of 8 tier-2-equivalents fail to clear the within-window context
bar despite passing the chic-v12 cross-pool L3 axis. This is the
publishable methodology finding the chic-v13 brief explicitly
flagged: cross-pool L3 alone does not load-bear, and the
chic-v13 axis discriminates *within* the cross-pool L3
tier-2-equivalent set, not just at its boundary. The chic-v9
framework-level negative (LOO accuracy 20.0% / 0/3 tier-2
unanimity correct) is unaffected; chic-v13 contributes the
**fourth within-polecat-scope discipline-protecting axis** on top
of the three pillars chic-v6 / chic-v9 / chic-v11+v12 already
established (mechanical verification, LOO held-out validation,
cross-pool L3 robustness). The discipline-pillar structure is
the deliverable; the per-candidate verdicts are the side-effect.

The post-chic-v13 per-candidate framing for the chic
sub-program's candidate proposals: `#032 → ki/stop` retains 5/5
within-polecat-scope axes positive (chic-v5 tier-2 + chic-v6
ku-pa lift + chic-v11 cross-pool L3 + chic-v11 ku-pa context +
chic-v13 not applicable since `#032` is chic-v5 tier-2 not
chic-v12 tier-2-equivalent); `#021 → nasal` retains 4/4 (chic-v5
tier-3 + chic-v12 tier-2-equivalent with 3 of 3 non-Eteocretan
corroboration + chic-v13 consistent); `#005 → stop`,
`#072 → stop`, `#056 → stop`, `#017 → nasal`, `#039 → stop`
retain 3/4 (chic-v5 tier-3 + chic-v12 tier-2-equivalent +
chic-v13 consistent); `#055 → stop`, `#065 → stop` retain 2/4
(chic-v5 tier-3 + chic-v12 tier-2-equivalent + chic-v13
inconclusive); `#001 → wa/glide`, `#012 → wa/glide` remain
chic-v11-actively-undermined as Eteocretan-LM glide artifacts.
Specialist review remains the load-bearing next step for any
candidate; promotion of `consistent` candidates to "candidate
proposal pending domain-expert review" prose is a PM call after
seeing both chic-v13 and the sibling chic-v14
LOO-on-cross-pool-L3-methodology results.

Outputs: `results/chic_v13_context_inspection.md` (per-candidate
context inspection report following the chic-v11 template;
all 8 candidates × 1–3 inscriptions × rendered readings +
structural commentary + per-candidate verdict);
`results/chic_v13_summary.md` (top-of-file count table +
1-paragraph plain-English verdict). **Done in mg-5261.** No
anchor pool modification; the ticket is read-only on
`pools/cretan_hieroglyphic_anchors.yaml`.

**Determinism.** No RNG; the candidate list is fixed by chic-v12;
inscription selection is a deterministic frequency-density
argmax over `corpora/cretan_hieroglyphic/all.jsonl`; rendered
readings use the chic-v2 anchor mapping byte-identically.


#### chic-v14 — leave-one-out held-out validation of the chic-v12 cross-pool L3 reclassification methodology (mg-7f57)

chic-v12 (above) introduced the cross-pool L3 reclassification rule
and reclassified 8 of 29 chic-v5 tier-3 candidates to
``tier-2-equivalent`` (27.6%). chic-v12 did not answer the held-out
validation question: when run blind on **known** chic-v2 anchors,
what fraction reclassify to ``tier-2-equivalent`` if the reference
class is the anchor's *known* phoneme class? That rate is the
cross-pool L3 LOO baseline against which chic-v12's 27.6% reads as
above-baseline / at-baseline / below-baseline.

chic-v14 closes that gap. **Methodologically symmetric to chic-v9**
(which closed the analogous LOO gap for the chic-v5 four-line
framework: aggregate accuracy 20.0%, tier-2 unanimity 0/3 correct,
``not validated`` band), chic-v14 runs a leave-one-out test of the
chic-v12 cross-pool L3 reclassification rule on the 20 chic-v2
paleographic anchors. Per LOO iteration the held-out anchor is
treated as the single unknown sign, the candidate-value pool is
rebuilt per (LOO iteration, substrate pool), the class-disjoint
sha256-keyed control mapping is regenerated per cell (no caching
across iterations — chic-v14 brief discipline reminder), and the
chic-v12 reclassification rule is applied with the held-out anchor's
**known** class as reference (in chic-v12 the reference was the
chic-v5 proposed class).

Outputs: `results/chic_v14_loo_validation.md` (per-anchor LOO table
+ per-pool per-class mean paired_diff details + headline aggregate
metrics + verdict + caveats); `results/chic_v14_summary.md`
(headline-count table + 1-paragraph plain-English verdict + specific
anchors that did and did not reclassify).

Headline metrics:

| metric | value |
|:--|--:|
| n anchors run blind | 20 |
| **cross_pool_l3_recovery_rate** (tier-2-equivalent) | **12/20 = 60.0%** |
| eteocretan_only_recovery_rate (tier-3-corroborated) | 0/20 = 0.0% |
| no_corroboration_rate (tier-3-uncorroborated) | 8/20 = 40.0% |
| chic-v12 reclassification rate (8 of 29 tier-3) | 8/29 = 27.6% |
| **chic-v12 minus chic-v14 LOO** | **-32.4pp (below-baseline)** |

The 12 anchors that reclassified to ``tier-2-equivalent`` (cross-
pool L3 corroborates the known class via at least one non-Eteocretan
LM): `#019`, `#031`, `#041`, `#042`, `#044`, `#049`, `#053`, `#057`,
`#061`, `#073`, `#077`, `#092`. The 8 anchors that reclassified to
``tier-3-uncorroborated``: `#010`, `#013`, `#016`, `#025`, `#028`,
`#038`, `#054`, `#070`. **Zero** anchors landed in
``tier-3-corroborated`` — Eteocretan-L3 alone-corroboration without
any non-Eteocretan LM agreement did not occur on any LOO iteration.

**Verdict (honest read; not soft-pedalled per the chic-v14 brief).**
The chic-v14 LOO cross-pool L3 recovery rate on known anchors is
60.0%, so chic-v12's 27.6% reclassification rate on the 29 tier-3
candidates is **-32.4pp BELOW the LOO baseline**. Cross-pool L3
corroborates ground-truth class on known anchors **more often** than
chic-v12 corroborates the chic-v5 proposed class on the tier-3 set.
Read against the chic-v14 brief's interpretation framework ("if LOO
shows 80%, the 27.6% is below baseline and the reclassification is
anti-evidentiary"): the chic-v12 reclassification on the tier-3 set
is **anti-evidentiary on the tier-3 set**. The chic-v12
``tier-2-equivalent`` band fires at 60.0% on known anchors vs 27.6%
on the chic-v5 tier-3 set; the band is therefore a **permissive
corroboration test, not a discriminative one** — it fires at high
rate regardless of whether the reference class is the correct
phoneme class. **chic-v13's context inspection (sibling ticket,
mg-5261) becomes the load-bearing evidence pillar** for any
tier-3 candidate's elevated credibility; cross-pool L3 alone is no
longer the dominant evidence axis on the tier-3 set.

**Why the LOO baseline is high (60%).** With 4 LMs voting and the
corroboration rule "≥ 1 non-Eteocretan LM votes the reference class"
(a permissive OR over 3 LMs), it is structurally likely that at
least one of the 3 non-Eteocretan LMs picks the reference class for
*any* reference class — including ground-truth class on known
anchors. The 60.0% LOO baseline is therefore not a sign that cross-
pool L3 reliably tracks phoneme class; it is a sign that the
corroboration rule is permissive. This reading explains why
chic-v12's 27.6% on tier-3 candidates is *below* the LOO 60.0%
baseline: when chic-v5's L1+L2 distributional consensus is the
reference (tier-3 candidates), the cross-pool L3 axis fires less
often than when the reference is ground-truth class on known
anchors. One natural interpretation is that chic-v5's L1+L2
proposed classes are biased away from the classes the cross-pool L3
axis natively favours (basque LM under aquitanian / toponym
favours `stop`; etruscan LM favours `nasal`; chic-v9's documented L3
class bias). The chic-v12 ``tier-2-equivalent`` verdict therefore
**does not separate** "true class" candidates from "L3-favoured
class" candidates — chic-v14 LOO shows ground-truth class also gets
corroborated at high rate, so corroboration alone does not
discriminate.

**Per-class breakdown of the 20 LOO iterations.** 6 stop-class
anchors reclassified to tier-2-equivalent (out of 9 stop anchors:
67%); 1 liquid-class out of 2 (50%); 3 nasal-class out of 4 (75%);
2 glide-class out of 3 (67%); 0 vowel-class out of 2 (0%). The
vowel class underperforms relative to other classes; this is
consistent with the chic-v12 cross-pool L3 axis's permissiveness
toward stop / nasal / glide / liquid and against vowel (the
candidate-value pool's vowel sub-pool is small — only the bare
vowels and the chic-v2 anchor values `a` and `i` — which makes
vowel-class corroboration mechanically rare).

**Implication for the methodology paper.** The chic-v9 framework-
level negative (LOO accuracy 20.0% on the chic-v5 four-line
framework, 0/3 tier-2 unanimity correct) and chic-v14's permissive-
corroboration finding (60.0% LOO baseline; chic-v12 below baseline)
together imply that **the chic-v12 cross-pool L3 reclassification is
not a discriminative gate**. The chic-v12 finding stands as
documented (8 of 29 tier-3 candidates have the same band-level
evidence structure as `#032`), but the **interpretation of that
evidence structure is downgraded**: cross-pool L3 corroboration is
not a per-candidate signal that lifts a candidate above the chic-v9
framework-level negative. chic-v13's context inspection (sibling
ticket) is the load-bearing evidence pillar for any candidate's
elevated credibility.

**`docs/findings.md` (mg-7f57 entry)** records the 20-anchor LOO
table, the per-pool per-class mean paired_diff details, the
headline aggregate metrics, the chic-v12-vs-LOO comparison verdict
(below-baseline), the per-class breakdown, and the implication for
the methodology paper. Per AGENTS.md: the findings update is a
hard merge-time blocker.

**Determinism.** chic-v14 inherits chic-v5's L3 sha256-keyed
permutation construction. Re-running `scripts/build_chic_v14.py`
produces byte-identical output (md5 stability verified at
chic-v14 build time, 2026-05-06):
`results/chic_v14_loo_validation.md` md5
`b64ba241ef6a3ca65f88e5571d37ce62`;
`results/chic_v14_summary.md` md5
`dce77a6ec28548e9edf275bdfe6aab86`.

#### Pre-registered chic-v10+ (chic-v9 done in mg-18cb)

- **chic-v13 done.** Within-window context inspection on the 8
  chic-v12 tier-2-equivalent candidates, applying the chic-v11
  `#032 → ki` ku-pa context inspection methodology
  (`results/chic_v11_032_ku_pa_context.md`). **6 of 8 candidates
  pass context inspection (`consistent`); 2 are `inconclusive` on
  corpus state; 0 are `inconsistent`.** Strongest cases: `#072`
  (two `[stop:#072]-de NUM` accountancy entries at Knossos bar
  #065, mirroring chic-v11 ku-pa structure directly), `#056`
  (multiple `[?] [stop:#056] NUM` entries at Knossos bar #061,
  including one preceding `ke-de NUM:1`), and `#021` (3-fold
  cross-site recurrence of `031-021-061 = ro-[N]-te` formula plus
  direct adjacency with `ki-de` at #059). Inconclusive: `#055`,
  `#065` (predominantly fragmentary host inscriptions; `#065`'s
  only clean occurrence is variant-bracketed). Outputs:
  `results/chic_v13_context_inspection.md`,
  `results/chic_v13_summary.md`. **Done in mg-5261.** Net: the
  chic-v9 framework-level negative is unaffected; chic-v13
  contributes the fourth within-polecat-scope discipline-
  protecting axis (mechanical verification + LOO validation +
  cross-pool L3 robustness + within-window context inspection)
  and demonstrates that cross-pool L3 corroboration alone is not
  sufficient for class-level value confirmation (2/8
  tier-2-equivalents fail the within-window context bar). No
  anchor pool modification; promotion of `consistent` candidates
  to "candidate proposal pending domain-expert review" prose is a
  PM call after seeing both chic-v13 and the sibling chic-v14
  LOO-on-cross-pool-L3-methodology results.
- **chic-v14 done.** Leave-one-out held-out validation of the
  chic-v12 cross-pool L3 reclassification methodology on the 20
  chic-v2 paleographic anchors with **known** class as reference
  (in chic-v12 the reference was the chic-v5 proposed class).
  **12 of 20 LOO iterations reclassify the held-out anchor to
  ``tier-2-equivalent`` = 60.0% LOO recovery rate** (cross_pool_
  l3_recovery_rate); 0 to ``tier-3-corroborated``; 8 to
  ``tier-3-uncorroborated``. **chic-v12's 27.6% (8/29) on the
  tier-3 set is -32.4pp BELOW the chic-v14 LOO baseline → the
  chic-v12 reclassification on the tier-3 set is anti-evidentiary**
  (cross-pool L3 corroborates ground-truth class on known anchors
  *more often* than chic-v12 corroborates the chic-v5 proposed
  class on the tier-3 set). **Cross-pool L3 is therefore a
  permissive corroboration test, not a discriminative gate**;
  chic-v13's within-window context inspection (sibling ticket)
  becomes the load-bearing fourth discipline pillar. Outputs:
  `results/chic_v14_loo_validation.md`,
  `results/chic_v14_summary.md`. **Done in mg-7f57.** Net: the
  chic-v9 framework-level negative is unaffected; the chic-v12
  reclassification stands as documented per-candidate evidence-
  grading (8 of 29 tier-3 candidates have the same band-level
  evidence structure as `#032`), but its interpretive weight is
  bounded above by the chic-v14 60.0% LOO baseline — cross-pool
  L3 corroboration is a *permissive corroboration* signal, not a
  per-candidate signal that lifts a candidate above the
  chic-v9 / v28 framework-level negative. The held-out validation
  pillar (chic-v14) catching a permissive corroboration axis
  before it could load-bear in the methodology paper is itself a
  discipline-protecting outcome.
- **chic-v13 done (re-stated for chronology).** Within-window
  context inspection on the 8 chic-v12 tier-2-equivalent
  candidates following the chic-v11 `#032 → ki` ku-pa context
  inspection methodology. **6 consistent / 0 inconsistent / 2
  inconclusive on corpus state.** Strongest cases at `#072`
  (Knossos bar #065 `[stop:#072]-de NUM` accountancy entries),
  `#056` (Knossos bar #061 `[?] [stop:#056] NUM` adjacent to
  `ke-de NUM:1`), `#021` (3-fold cross-site `031-021-061` plus
  `ki-de` adjacency at #059). Inconclusive: `#055`, `#065`
  (predominantly fragmentary host inscriptions). Outputs:
  `results/chic_v13_context_inspection.md`,
  `results/chic_v13_summary.md`. **Done in mg-5261.** Per the
  post-chic-v14 framing, chic-v13 is the load-bearing fourth
  discipline pillar (replacing cross-pool L3 robustness in that
  role); the 6 chic-v13-consistent candidates plus chic-v11's
  `#032` constitute the **7 paired-evidence candidates** the
  post-v30 §4.7 reframe centres on. Specialist review remains
  the load-bearing next step for any candidate; promotion to
  "candidate proposal pending domain-expert review" prose is
  per-candidate within the v30 register.
- **chic-v12 done.** Cross-pool L3 robustness check on the 29
  chic-v5 tier-3 candidates, methodologically symmetric extension
  of chic-v11. **8 of 29 tier-3 candidates reclassify to
  `tier-2-equivalent`** (≥ 1 non-Eteocretan substrate LM
  corroborates the chic-v5 proposed class — same band-level
  evidence structure as `#032`); 4 to `tier-3-corroborated` (the
  L1+L2-disagree subset's chic-v5 baseline state); 17 to
  `tier-3-uncorroborated`. The reclassification rate (8 > 5)
  triggers the chic-v12 brief's pre-registered bail on
  within-window context inspection; the scale signal — the
  cross-pool L3 axis is meaningfully more permissive than the
  Eteocretan-only L3 chic-v5 used — is the chic-v12 finding.
  No chic-v12 tier-2-equivalent matches `#032`'s overall
  mechanical-lines tally; the evidentiary structure is
  bandwise-equivalent but per-line vote counts differ. Outputs:
  `results/chic_v12_cross_pool_l3.md`,
  `results/chic_v12_tier3_summary.md`. **Done in mg-2035.**
  Net: the chic-v9 framework-level negative is unaffected; the
  framework's per-sign discrimination claim now spans n = 32
  evidence-graded candidates (3 chic-v5 tier-2 + 29 chic-v5
  tier-3, of which 9 are cross-pool L3 corroborated by ≥ 1
  non-Eteocretan substrate LM). **(Post-chic-v14: cross-pool L3
  alone is permissive corroboration, not a discriminative gate;
  the per-candidate evidence-grading provided by this 9-count
  is interpretively load-bearing only when paired with chic-v13's
  within-window context inspection — see chic-v14 entry above
  and the post-chic-v14 framing block at the top of §4.7.)**
- **chic-v11 done.** Cross-pool L3 robustness check + #032 ku-pa
  context inspection on the 3 chic-v5 tier-2 candidates. Cross-
  pool L3: of 12 cells (3 candidates × 4 substrate-pool LMs),
  `#001 → wa`/glide is rejected by 3 of 4 LMs (only Eteocretan
  votes glide), `#012 → wa`/glide is rejected by 3 of 4 LMs (only
  Eteocretan votes glide), `#032 → ki`/stop is supported by 2 of
  4 LMs including the chic-v5 default Eteocretan. The chic-v5
  glide votes for `#001`/`#012` are Eteocretan-LM-specific
  artifacts; `#032`'s stop vote is partially LM-robust. #032 ku-pa
  context: chic-v6 lift attribution lands on CHIC #057 (Knossos
  bar) via 4 ku-pa-family scholar entries from accountancy-tablet
  Hagia Triada inscriptions HT 1, HT 16, HT 102, HT 110a. The
  matched `(#032, #013)` token run sits in an accountancy-formula
  position (`#079 ki pa / NUM:20`) on the CHIC side; the chic-v6
  ku-pa lift for `#032 → ki` is corroborated by inscription-level
  context on both sides. Per-candidate post-chic-v11 status:
  `#032` retains the strongest evidentiary basis (partial
  corroboration); `#001` and `#012` are weakened beyond the
  chic-v9 generic downgrade (cross-pool L3 actively undermines).
  Outputs: `results/chic_v11_cross_pool_l3.md`,
  `results/chic_v11_032_ku_pa_context.md`. **Done in mg-d69c.**
  Net: the chic-v9 framework-level negative is unaffected, but the
  per-candidate framing for the methodology paper is now
  asymmetric — `#032 > #001 ≈ #012` on within-polecat-scope
  mechanical evidence.
- **chic-v9 done.** Leave-one-out held-out validation of the
  chic-v5 framework on the chic-v2 anchor pool. **Aggregate
  accuracy 20.0% (4/20)**, near the 16.7% chance baseline for a
  6-class taxonomy; per-line L1=20%, L2=20%, L3=5% (L3 at chance
  / below chance, consistent with the known systematic Eteocretan-
  LM class bias); **tier-2 classification accuracy 0/3 = 0.0%**.
  This is the held-out validation that should have been run as
  part of chic-v5; the negative result downgrades the credibility
  of chic-v5's three tier-2 candidates from "mechanical proposals
  deserving specialist review" to "candidate proposals contingent
  on the framework's currently-low validation accuracy". Output:
  `results/chic_v9_loo_validation.md`. **The methodology paper's
  three-sentence reading test (§7) must be restructured to lead
  with the LOO accuracy number, not the candidate count.**
- **chic-v8 done.** Bilingual analysis on the Malia altar stone
  (CHIC #328, verified unilingual CHIC) and a systematic survey
  of the v0 corpora for any other genuinely-dual-script artifact
  yielded a null result: 0 promoted candidates. The L5 (LA-
  constraint) line of evidence is silent for all 76 unknown
  CHIC syllabographic signs by corpus state. Outputs:
  `results/chic_dual_script_bilingual_leaderboard.md`,
  `results/chic_v8_promoted_candidates.md`. The bilingual
  extension is preserved in the methodology paper as a
  falsifiable fifth line of evidence contingent on future
  corpus expansion; the genre-parallel CHIC #328 vs LA libation-
  table comparison is reported informationally only and is NOT
  load-bearing.
- **chic-v6 done.** The original "domain-expert review" framing
  for chic-v6 was reframed by Daniel (2026-05-05) to a
  mechanical-verification pass before specialist review (the
  domain-expert review remains out of polecat scope and is
  unchanged as a follow-up). chic-v6's verification-rate report
  is in `results/chic_verification_match_rates.md`; the load-bearing
  finding is the small-but-non-zero +3-inscription / +20-hit
  tier-1 → tier-2 lift, with the larger tier-3 / tier-4 lifts
  caveated for class-level-matching permissiveness.
- **Specialist review of chic-v5's tier-2 candidates and chic-v6's
  matched enumerations.** Hand-curated review by an Aegean-
  syllabary specialist remains the next step; mechanical
  verification (chic-v6) does not substitute for specialist
  judgment. Hand-curated extension of line 4 (cross-script
  paleographic) from O&G 1996, Salgarella 2020, Decorte 2017,
  and adjacent paleography scholarship would also raise additional
  tier-3 candidates to tier-2 by adding a fourth confirming vote
  where the distributional + substrate lines already converge.
- **chic-v7** — methodology-paper extension integrating chic-v0..v5
  cleanly into the v25 manuscript shape; the final consolidation
  pass before journal-submission handoff for the cross-script
  paper. **Done in mg-9508** (this document); editorial-only, no
  new harness commits. The chic-v7 audit pass cross-checked every
  quantitative claim in §4.7 against the committed result files
  (`results/chic_sign_inventory.md`,
  `results/chic_anchor_density_leaderboard.md`,
  `results/chic_partial_readings.md`,
  `results/rollup.bayesian_posterior.{aquitanian,etruscan,toponym,eteocretan}.chic.md`,
  `results/rollup.bayesian_posterior.chic.md`,
  `results/rollup.linear_a_vs_chic_substrate_comparison.md`,
  `results/chic_value_extraction_leaderboard.md`); one
  inconsistency was found and fixed (chic-v1 paleographic-anchor
  candidate confidence-tier counts had been written as "9 proposed,
  8 debated" in an earlier draft; the committed source-of-truth in
  `pools/cretan_hieroglyphic_signs.README.md` and
  `results/chic_sign_inventory.md` is **3 consensus / 10 proposed
  / 7 debated**, and the audit pass corrected the manuscript text
  accordingly).
- **chic-v10** — methodology-paper polish pass integrating chic-v9's
  leave-one-out held-out validation (mg-18cb) result and
  downgrading the chic-v5 tier-2 candidates' credibility per the
  20% LOO accuracy / 0/3 tier-2 unanimity verdict. **Done in
  mg-1178** (this document); editorial-only, no new harness commits.
  The chic-v10 polish pass restructured §4.7's narrative to lead
  with the post-chic-v9 framing in the section's intro, hedged the
  chic-v5 tier-2 framing from "candidate proposal pending domain-
  expert review" to "candidate proposal contingent on the
  framework's currently-low validation accuracy", added a chic-v9
  entry to §5.4 (Cross-script CHIC limitations), integrated chic-v9
  into §6 (Conclusion) alongside the existing v13 / v22 / v24 /
  chic-v6 negative-validation lineage, and restructured §7's three-
  sentence reading test to lead with the LOO accuracy number rather
  than the tier-2 candidate count. The chic-v10 audit-of-the-audit
  on chic-v9's incremental edits confirmed all numbers in the §4.7
  chic-v9 subsection verify against `results/chic_v9_loo_validation.md`
  (4/20 = 20.0% aggregate; chance baseline ~16.7%; per-line L1=20%,
  L2=20%, L3=5%; 0/3 LOO tier-2 correct; the 3 LOO tier-2 anchors
  `#031 = ro` / `#042 = wa` ⚠ / `#053 = me`).

#### Cross-script methodological synthesis (chic-v0..v14 + Linear A v0..v28)

The two parallel result blocks of this manuscript — Linear A
§3.1–§3.14 and CHIC §4.7 above — converge on a single
methodology-paper claim: **the framework's right-tail bayesian
gate detects substrate-LM-phonotactic kinship at the population
level, with the magnitude scaling monotonically with a-priori
genealogical relatedness, that signal is cross-script, and the
per-sign machinery layered on top of the population-level gate
does not recover known phoneme classes when run blind under
leave-one-out held-out validation.** The load-bearing observations
across the 42-ticket sequence:

- *Population-level kinship detection across two scripts.* All
  four substrate pools' own-LM right-tail gate behaviours on
  Linear A and CHIC produce **identical rank orderings of the
  per-pool gap** (Eteocretan > toponym > Etruscan > Aquitanian),
  cross-script Spearman ρ = +1.000 on the per-pool gate gap.
  Eteocretan, the closest-genealogical-relative candidate
  substrate, PASSes the gate on **both** scripts (LA p=4.10e-06,
  gap +0.20; CHIC p=7.33e-04, gap +0.11). On Linear A all four
  pools clear α=0.05; on CHIC's smaller (~1,258-token vs Linear
  A's ~5,000-token) syllabographic stream only Eteocretan
  formally clears α=0.05, but the ordering of the FAILing pools
  is preserved.
- *Per-sign decipherment remains unsupported on either script.*
  On Linear A: v13's cross-window coherence median 0.18 (vs 0.6
  bar) decisively fails; v19/v22 internal consensus across
  surviving substrate candidates yields 3.95% aggregate match
  rate (3/76) against the 35-entry Younger scholar-reading set,
  squarely in the pre-registered strong-null band. On CHIC:
  chic-v5's four-line-of-evidence framework, applied to 76
  unknown CHIC syllabographic signs under Eteocretan-LM
  substrate-consistency scoring, surfaces 3 tier-2 candidate
  proposals (≥3 of 4 lines agreeing on a coarse phoneme class,
  with line 4 silent for all unknowns by construction) — and
  chic-v9's leave-one-out held-out validation places the same
  framework's mechanical recovery on 20 known anchor classes at
  **20.0% aggregate / 0/3 on the tier-2 unanimity criterion**
  when run blind, near the ~16.7% chance baseline for the 6-class
  taxonomy. The 3 chic-v5 tier-2 candidates are therefore
  **candidate proposals contingent on the framework's currently-
  low validation accuracy** (chic-v9 verdict: low-agreement / not
  validated band) rather than mechanical proposals deserving
  elevated specialist-review priority. The framework's per-sign
  resolution is class-level on either script.
- *The discipline is the deliverable on both scripts.* On Linear
  A, the methodology paper's central methodological warning
  (§4.5) — that qualitative-impression evidence is structurally
  equivalent to the framework's surface-aggregate PASS, and the
  surface-aggregate PASS by mg-6b73 cannot distinguish real
  substrate roots from phonotactically-matched conjecturals —
  carries forward to CHIC unchanged. The chic-v5 framework's
  anti-motivated-reasoning structural choices (mechanical
  agreement predicate, explicit silent-line bookkeeping,
  L3-systematic-class-bias disclosure, frequency-floor
  thresholding) are the cross-script port of the v13 / v19 /
  v22 discipline.
- *Internal consensus does not imply external correctness, and
  this generalises across scripts, substrate pools, and across
  the population / per-sign axis.* On Linear A, v22 / v24's 3.95%
  aggregate match rate against the Younger scholar set holds
  across substrate-pool unions (eteocretan-only 0.00%; three-pool
  3.95%; four-pool 3.95% byte-identical to three-pool). On CHIC,
  chic-v9's LOO test puts a quantitative number on the analogous
  internal-vs-external gap at the per-sign machinery level: the
  chic-v5 framework's L1+L2+L3 mechanical recovery on the 20
  known chic-v2 anchors is 20.0% / 0/3 tier-2 unanimous correct
  when run blind, and the 3 chic-v5 tier-2 candidates inherit
  that internal-consensus-vs-validation gap. The cross-script
  lesson: mechanical scoring against phonotactically-matched
  controls, paired with explicit external-comparand bookkeeping
  AND held-out validation, catches failure modes that internal-
  consensus-only methodology produces uniformly across scripts.
- *Held-out validation as the falsification check internal-
  consensus-only methodology cannot supply.* chic-v9's leave-one-
  out test is the chic sub-program's analogue to v22 / v24 on
  the Linear A side: it places a quantitative number on the
  per-sign machinery's reliability under known ground truth. The
  chic-v9 verdict — 20.0% aggregate / 0/3 tier-2 correct — is the
  fifth piece of evidence in the methodology paper's negative-
  validation lineage (v13 cross-window coherence median 0.18 vs
  0.6 bar; v22 35-entry scholar-set 3.95% aggregate; v24
  eteocretan-only 0/76 = 0.00%; chic-v6 +3-inscription / +20-hit
  tier-1 → tier-2 lift caveated by chic-v9; chic-v9 LOO 20.0% /
  0/3). **chic-v14 (mg-7f57) extends the held-out-validation
  pillar a second time** by leave-one-out testing the chic-v12
  cross-pool L3 reclassification rule on the 20 chic-v2 anchors
  with known class as reference: 60.0% LOO recovery on known
  anchors vs 27.6% on the chic-v5 tier-3 set →
  **-32.4pp anti-evidentiary verdict on cross-pool L3
  reclassification on the tier-3 set**, demoting cross-pool L3
  robustness from a discipline-protecting axis in its own right
  to a permissive corroboration test that requires within-window
  context evidence (chic-v13) to be load-bearing. All six
  validation channels point in the same methodological
  direction: the framework detects substrate-LM-phonotactic
  kinship at the population level, but per-sign decipherment is
  unsupported by any of the validation channels the framework
  has been tested against, and held-out validation continues to
  catch new permissive-corroboration failure modes (most
  recently chic-v14's verdict on cross-pool L3) before they can
  load-bear. The discipline of pre-registered falsifiable
  acceptance gates + cross-script transfer + leave-one-out held-
  out validation + within-window context inspection is what
  catches motivated-reasoning failure modes that internal-
  consensus-only analyses cannot.
- *Cross-script transferability of the methodology is the
  novel methodology-paper deliverable of the chic sub-program.*
  The Linear A v0..v25 result is "the framework detects
  substrate-LM-phonotactic kinship between candidate substrate
  and target script's underlying language at the population
  level". The chic-v3..v4 result extends that to "and that
  detection is *script-transferable* under the same scoring
  infrastructure: the per-pool PASS/FAIL ordering survives
  cross-script transfer at ρ=+1.0 between two independent
  undeciphered Cretan scripts". This is the cross-script
  methodology-paper claim that single-script v25 could not
  make.

What the cross-script extension does **not** establish: it
does not adjudicate the question of whether Linear A and CHIC
share a common underlying language (the cross-script signal is
consistent with shared underlying language *or* with shared
substrate phonotactic stratum — both produce ρ=+1.0 rank
correlation under genealogical-relatedness-modulated
substrate-LM kinship). It does not validate per-sign Linear
A or CHIC syllabic value assignments. It does not propose a
decipherment of either script. It does extend the methodology
paper's central discipline-protecting claim — that mechanical
scoring + matched controls + external-comparand bookkeeping
catches failure modes internal-only methodology cannot — from
one undeciphered Cretan script to two.

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
  no instance of either sequence in `KH 10` or `KH 5`. v22
  (mg-46d5) extended the external-validation footprint to a
  35-entry / 76-AB-sign-comparison-point Younger-catalog
  scholar-proposed-reading set spanning 6 sites and 21+ CV
  combinations; the aggregate match rate is **3.95%** (3/76) on
  the consonantal first segment of the scholarly CV, with 32 of
  35 entries scoring zero — squarely in the pre-registered
  strong-null band (< 5%). The external-validation evidence base
  is therefore three layered components: one cascade-candidate
  inscription decisively divergent (v19), one targeted accountancy
  follow-up returning null comparand (v20), and one population-
  level 35-entry scholar-set comparison with 3.95% aggregate
  match (v22). All three lines of evidence — global aggregate v13,
  local cascade-candidate external-comparison v19 + v20, and
  population-level scholar-set comparison v22 — support the same
  supportable-claim shape: per-sign decipherment is not
  established by this framework, and where independent scholarly
  ground truth is available at population scale the mechanical
  consensus does not partially recover it. *This does not
  constitute a decipherment.* The cascade candidates are
  hypotheses for
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
- **Eteocretan LM is small-corpus by reality.** v21's own-LM is
  built from ~87 unique word forms across ~9 substantive
  multi-line texts (Praisos 1–7, Dreros 1–2). The α=1.0 smoothing
  partially compensates, and the strong PASS magnitude despite the
  noise floor is itself a finding (§3.14), but the LM is genuinely
  noisier than the v8–v18 LMs and per-surface posteriors carry more
  variance than under Basque / Etruscan / Mycenaean-Greek. The
  Eteocretan epigraphic record is finite at ~9 substantive texts;
  expanding the corpus is not a v22+ engineering action item but a
  fact about the surviving inscriptional record. v24 (mg-c103)
  surfaces a related sparseness observation: the eteocretan-only
  candidate count (~2,985 substrate + ~2,635 control) is large
  enough for the population-level right-tail PASS but too sparse
  for per-inscription consensus to form at the 50% robust bar —
  zero cascade candidates emerge across all three populations
  (top-30 right-tail, short ≤5 sign tokens, libation-formula
  carriers) under eteocretan-LM-only aggregation. PS Za 2 in
  particular has *zero* positive eteocretan paired_diff records
  under the bigram-preserving control. This is not a
  framework-blocking limitation but a fact about Eteocretan-pool
  granularity; the v22 / v24 four-pool aggregations remain the
  load-bearing per-inscription view.

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

### 5.4 Cross-script (CHIC) limitations

Limitations specific to the chic-v0..v14 sub-program (§4.7),
parallel in role to §5.1–§5.3 above for the Linear A pipeline:

- **CHIC corpus is incomplete.** 302 of 331 catalog entries
  (~91%) ingested from Younger's web edition (chic-v0, mg-99df);
  29 missing entries are deferred to a manual-transcription pass
  from print Olivier & Godart 1996. The chic-v3 / chic-v4 / chic-v5
  results are computed against the 302-inscription subset; CHIC
  corpus expansion is the natural intervention for raising
  borderline-FAIL pool signals (toponym at p=0.435 on CHIC) above
  α=0.05.
- **CHIC syllabographic stream is one-quarter the size of Linear
  A's.** 1,258 syllabographic tokens / 551 maximal blocks across
  276 inscriptions (chic-v3 build), vs Linear A's ~5,000 tokens
  across ~760 inscriptions. Statistical power for the CHIC
  right-tail bayesian gate is correspondingly lower; only
  Eteocretan formally clears α=0.05 on CHIC, vs all four pools on
  Linear A. The cross-script Spearman ρ=+1.0 result (chic-v4)
  remains robust because rank ordering is preserved even where
  threshold signal fails on the borderline pools.
- **chic-v5 line 4 is silent for all 76 unknowns by construction.**
  The chic-v1 paleographic-candidate list (the cross-script
  paleographic line 4 input) is precisely the seed for the chic-v2
  anchor pool; every candidate became an anchor, so no unknown
  carries a paleographic note. tier-2 in chic-v5 therefore
  requires unanimous agreement of the three remaining non-silent
  lines (1, 2, 3). Hand-curated extension of line 4 from O&G 1996,
  Salgarella 2020, Decorte 2017, and adjacent paleography
  scholarship is the natural chic-v6 target — an Aegean-syllabary
  specialist task, not a polecat task.
- **chic-v5 line 3 carries a systematic class bias.** Above the
  n=3 frequency floor (49 of 76 unknowns), the line-3 class
  distribution is 26/49 votes for `nasal`, 20/49 for `glide`,
  2/49 for `liquid`, 1/49 for `stop`, 0/49 for `vowel` or
  `fricative` — a property of the framework (Eteocretan-LM
  bigram preference for common Eteocretan-vocabulary onset
  patterns + chic-v2 anchor pool's class-imbalanced candidate-
  value pool: 5 vowel / 8 stop / 4 nasal / 2 liquid / 1 glide;
  no fricatives because no fricative-onset Linear-B carryover
  values are paleographically anchored on CHIC). The tier-2 /
  tier-3 discipline is what filters out the L3 bias by requiring
  independent confirmation from at least one distributional line;
  the discipline is the deliverable, not the count of tier-2
  candidates.
- **chic-v5 tier-2 candidates are candidate proposals, not
  decipherments.** The 3 tier-2 candidates (#001 → glide;
  #012 → glide; #032 → stop) are pending domain-expert review
  by an Aegean-syllabary specialist. The framework's per-sign
  resolution is class-level (`vowel`, `stop`, `nasal`, `liquid`,
  `fricative`, `glide`) rather than phoneme-specific. The line 1 /
  line 2 distributional machinery is built on the chic-v2 anchor
  pool's fingerprints rather than a fully-independent paleographic
  ground truth; tier-2 promotion to "decipherment claim" requires
  external domain-expert validation that polecats cannot supply.
  The chic-v11 (mg-d69c) within-polecat-scope refinement adds a
  **per-candidate asymmetric framing**: cross-pool L3 robustness
  under all 4 substrate-pool LMs rejects #001 / #012's glide vote
  at 3 of 4 LMs (Eteocretan-LM-specific artifact) and weakly
  corroborates #032's stop vote at 2 of 4 LMs including the
  chic-v5 default Eteocretan plus Etruscan, while the
  inscription-level metadata cross-check on the chic-v6 ku-pa-
  family lift (the `(#032, #013)` literal pair) corroborates the
  match on both sides (4 source Linear A tablets HT 1, HT 16, HT
  102, HT 110a are all LM IB Hagia Triada accountancy tablets;
  matched CHIC #057 context is `#079 ki pa / NUM:20`, the
  canonical sign-run-followed-by-numeral accountancy-formula
  structure). The per-candidate post-chic-v11 ranking is
  `#032 > #001 ≈ #012` on within-polecat-scope mechanical
  evidence — `#032` retains the strongest evidentiary basis of
  the three under axis-restricted polecat-scope checks while
  `#001` and `#012` are weakened beyond the chic-v9 generic
  downgrade — but the v28 + chic-v9 framework-level negative
  remains the dominant constraint and none of the three clears
  specialist-review elevation.
- **CHIC has no per-sign external-validation comparand in
  scholarly literature.** Unlike Linear A (Younger 35-entry
  scholar-set, v22), CHIC has no comparable contextual-reading
  set; chic-v5's tier-2 candidates have no analogue to the v22
  population-level external-validation comparison. This is a fact
  about CHIC's scholarly state of the art, not a methodology
  limitation.
- **No within-CHIC per-inscription cascade-candidate analysis.**
  The v19 / v24 per-inscription robust-fraction analysis was
  not run on CHIC; chic-v3 / chic-v4 / chic-v5 stayed at the
  population-level. CHIC's smaller corpus would likely produce
  even sparser per-inscription consensus than Eteocretan-only
  on Linear A (where the v24 result was zero cascade candidates;
  see §3.14 / Per-inscription cascade-candidate analysis under
  Eteocretan LM (v24)). Tracked as a chic follow-up.
- **chic-v6 tier-3 / tier-4 verification lifts are not directly
  interpretable as verification-grade evidence.** The +91 / +46
  inscription-count lifts from tier-2 to tier-3 / tier-3 to tier-4
  are dominated by class-level-matching's structural
  permissiveness: a `STOP` placeholder matches any of
  `{p, b, t, d, k, g, q}`, a `GLIDE` placeholder matches any of
  `{j, w, y}`, etc. Without a phonotactically-matched permutation
  control of the tier-3 / tier-4 class assignments, those lifts
  are interpretable only as a *ceiling* on what verification the
  class-level proposals could possibly produce. The tier-1 →
  tier-2 specific-phoneme-override lift (+3 inscriptions / +20
  hits) is the load-bearing chic-v6 result.
- **chic-v8 L5 (LA-constraint) is silent for all 76 unknowns by
  v0 corpus state.** No genuinely-dual-script artifact is
  ingested in either v0 corpus; the canonical candidate (Malia
  altar stone CHIC #328) is unilingual-CHIC per Olivier-Godart
  1996. Genre-parallel comparisons (CHIC #328 vs LA libation
  tables PS Za 2 / SY Za 4) are conjectural and reported
  informationally only. A future corpus-expansion ingest pass
  (full GORILA Za-series + CMS sealstone-catalog dual-script
  entries) could reactivate L5; the chic-v8 build script
  (`scripts/build_chic_v8.py`) would surface any L5 votes
  automatically against the new corpus state.
- **chic-v5 framework's mechanical recovery on known cases (LOO
  validation, chic-v9) is at chance baseline.** chic-v9's leave-
  one-out held-out validation against the 20-anchor chic-v2 pool
  places the chic-v5 framework's L1+L2+L3 mechanical recovery at
  **20.0% aggregate** (4/20), near the **~16.7% chance baseline**
  for a 6-class phoneme taxonomy (vowel / stop / nasal / liquid /
  fricative / glide), with **tier-2 classification accuracy at
  0/3 = 0.0%** (every LOO tier-2 anchor's framework-proposed
  class disagrees with the known scholarly class). Per-line
  decomposition: L1 = 4/20 = 20.0%, L2 = 4/20 = 20.0%, L3 =
  1/20 = 5.0% (below chance, consistent with the known L3
  systematic class bias under the Eteocretan LM disclosed in
  chic-v5). Per the chic-v9 brief's pre-registered thresholds
  (>70% high; 40-70% moderate; <40% low), the framework is in the
  **low-agreement / not-validated band**. Per-sign value-extraction
  proposals derived via the chic-v5 framework should be read as
  **"phonotactically-coherent candidates contingent on the
  framework's currently-low validation accuracy"** rather than
  "validated phoneme-class assignments deserving elevated
  specialist-review priority", pending domain-expert review and
  an independent line of evidence (paleographic, dual-script, or
  otherwise) per candidate. The L4 (cross-script paleographic)
  line was deliberately excluded from the LOO test as circular by
  construction (chic-v1's PALEOGRAPHIC_CANDIDATES list is the
  source of the chic-v2 anchor pool); the L1+L2+L3-only setup is
  the honest test, and L4 remains a falsifiable evidence axis
  contingent on hand-curated extension from O&G 1996, Salgarella
  2020, Decorte 2017, and adjacent paleography scholarship. The
  N=20 LOO test is small (±5% differences fall within the
  binomial noise floor for this sample size); the headline 20%
  is a point estimate with substantial uncertainty, but the
  qualitative reading (recovery near chance; 0/3 tier-2 correct)
  is robust to that uncertainty. The chic-v9 verdict is what the
  methodology-paper framing of the chic-v5 candidates loads on:
  in the post-chic-v9 register, the 3 tier-2 candidates are
  **candidate proposals contingent on the framework's currently-
  low validation accuracy**, not "candidate proposals pending
  domain-expert review by an Aegean-syllabary specialist".
- **chic-v5 framework's mechanical recovery is at chance
  baseline on the Linear A side too (v28 LOO).** v28's symmetric
  Linear A-side leave-one-out validation against the 21-anchor
  LB-carryover pool places the chic-v5 framework's L1+L2+L3
  mechanical recovery at **33.3% aggregate** (7/21), modestly
  above the **~16.7% chance baseline** for the 6-class phoneme
  taxonomy but **below the 40% moderate-agreement threshold** the
  chic-v9 brief pre-registered, with **tier-2 classification
  accuracy at 0/3 = 0.0%** (LA-side LOO tier-2 anchors `AB06=na`,
  `AB08=a`, `AB27=re`, all unanimous-but-wrong). Per-line
  decomposition: L1 = 7/21 = 33.3%, L2 = 7/21 = 33.3%, L3 =
  2/21 = 9.5% (still below chance, consistent with the L3
  Eteocretan-LM systematic class bias documented in chic-v5).
  Each LA-side per-line accuracy is ~13 percentage points above
  the corresponding CHIC-side number (chic-v9: L1=20%, L2=20%,
  L3=5%); the L1+L2+L3 consensus delta is +13.3 percentage
  points. Both scripts land in the **low-agreement / not-
  validated band** per the chic-v9 brief's pre-registered
  thresholds, and the per-script delta is within the regime
  that establishes **the at-chance per-sign behaviour as
  structural to the chic-v5 framework rather than CHIC-corpus-
  specific**, closing the v28-pre-registered "structural vs
  corpus-specific" question in favour of the structural-
  limitation arm. L4 (cross-script paleographic) is again
  excluded as circular by construction (the LB-carryover
  anchors' known values are themselves derived from Linear B
  paleographic similarity, mirroring chic-v9's L4-exclusion
  rationale on the CHIC side); the L1+L2+L3-only setup is the
  honest LA-side test. The N=21 LOO test is small (±5%
  differences fall within the binomial noise floor for this
  sample size; comparable to chic-v9's N=20); the headline 33.3%
  is a point estimate with substantial uncertainty, but the
  qualitative reading (recovery near the chance baseline; 0/3
  tier-2 correct) is robust to that uncertainty. The L3 LM
  choice for the LA-side LOO is the v21 Eteocretan LM in
  **direct symmetry with chic-v9** (LB-carryover anchors are not
  naturally partitioned across the v10/v18/v21 substrate pools,
  so a per-pool LM swap would be methodologically odd; using
  the v21 Eteocretan LM keeps the LA-side comparison apples-to-
  apples with chic-v9). The v28 verdict, with chic-v9, jointly
  loads the post-v28 + post-chic-v9 register on the methodology
  paper's chic-v5 framing across both scripts: in this register,
  the 3 chic-v5 tier-2 candidates on CHIC are **candidate
  proposals contingent on the framework's currently-low
  validation accuracy on both scripts**, with the chic-v11
  per-candidate refinement (above) noting `#032` corroborated
  weakly while `#001` / `#012` are weakened beyond the chic-v9
  generic downgrade.
- **chic-v11's cross-pool L3 robustness check is axis-restricted
  and does not lift the framework-level negative.** chic-v11
  reruns the chic-v5 L3 substrate-consistency line under all 4
  substrate-pool LMs (12 cells = 3 candidates × 4 LMs) but does
  not re-run L1+L2 (distributional fingerprint axes); the chic-v9
  framework-level LOO accuracy of 20.0% / 0/3 tier-2 correct does
  not improve from axis-restricted L3 cross-pool corroboration on
  individual candidates. Even an all-4-pools-agree L3 verdict
  (which `#032` does not produce — only 2 of 4 LMs vote stop)
  would be a per-candidate axis-restricted finding, not a lift on
  the framework's full-machinery validation accuracy. Similarly
  the inscription-level metadata cross-check on the chic-v6 ku-pa
  lift attributable to `#032 → ki` is contextual corroboration of
  one chic-v6 verification-line hit, not framework-level
  validation. The chic-v11 deliverable is a per-candidate
  refinement of the chic-v9 generic downgrade, not a lift on
  chic-v9's verdict.
- **Cross-pool L3 robustness is a permissive corroboration test,
  not a discriminative gate (chic-v14 LOO).** chic-v14's leave-
  one-out test of the chic-v12 cross-pool L3 reclassification
  rule on the 20 chic-v2 paleographic anchors with **known**
  class as reference recovers 12 of 20 anchors to
  ``tier-2-equivalent`` (60.0%); chic-v12's 27.6% (8/29) on the
  chic-v5 tier-3 candidates is **-32.4pp BELOW the LOO baseline**.
  Cross-pool L3 corroborates ground-truth class on known anchors
  *more often* than chic-v12 corroborates the chic-v5 proposed
  class on the tier-3 set, so the chic-v12 reclassification on
  the tier-3 set is **anti-evidentiary**. Cross-pool L3 is
  therefore demoted from a discipline-protecting axis in its own
  right to a permissive corroboration test, useful only in
  combination with at least one other independent line of
  evidence (chic-v13 within-window context inspection supplies
  that line). The chic-v11 / chic-v12 cross-pool L3 results stand
  as documented per-candidate evidence-grading information; their
  interpretive weight as standalone evidence for a candidate's
  class is bounded above by chic-v14's 60.0% LOO baseline. The
  LA-side cross-pool L3 axis was already exercised in v15–v18
  (4-pool × 4-LM gates in §3.3 / §3.10 and the v23 cross-LM
  matrix in §3.14); the CHIC-side analog now produces the same
  anti-evidentiary verdict on the chic-v5 tier-3 set under held-
  out validation, mirroring v15–v23's cross-LM-matrix shape
  findings on Linear A. **chic-v13's within-window context
  inspection is the load-bearing fourth discipline pillar
  post-chic-v14**, replacing cross-pool L3 robustness in that
  role.
- **2 of 8 chic-v12 tier-2-equivalent candidates fail the
  chic-v13 within-window context inspection on corpus-quality
  grounds, not framework grounds.** chic-v13's verdict on the 8
  chic-v12 tier-2-equivalent candidates is 6 consistent / 0
  inconsistent / 2 inconclusive; the 2 inconclusive cases
  (`#055`, `#065`) reflect honest under-determination on corpus
  state — `#055` occurs predominantly in `fragmentary`-confidence
  inscriptions, and `#065`'s only `clean`-confidence occurrence
  is itself in a variant-bracketed transcription `{065}` (CHIC
  #174). Neither candidate is rejected; both await cleaner
  inscription evidence to elevate or reject. The 2 inconclusive
  verdicts are a corpus-quality limitation, not a chic-v13
  framework limitation. A future corpus-expansion pass that adds
  cleaner host inscriptions for these two signs (manual
  transcription of the 29 missing CHIC catalog entries; CMS
  sealstone-catalog entries containing `#055` / `#065` in
  cleaner contexts) would reactivate chic-v13's within-window
  context inspection on these candidates without modifying the
  discipline.
- **The chic-v9 / v28 framework-level LOO negative on per-sign
  decipherment continues to hold, regardless of v30's per-
  candidate evidence-graded refinement.** v30's contribution is
  **granularity within the chic-v9 + v28 framework-level negative
  band** (low-agreement / not-validated; 20.0% on CHIC, 33.3% on
  Linear A; 0/3 on tier-2 unanimity correct on both scripts), not
  a lift on the framework-level negative. The 7 paired-evidence
  candidates (`#032` chic-v11 + 6 chic-v13 consistent: `#005`,
  `#017`, `#021`, `#039`, `#056`, `#072`) carry per-candidate
  evidence at two distinct axes (cross-pool L3 corroboration +
  within-window context inspection) but inherit the framework-
  level negative on per-sign decipherment claims. They remain
  **"candidate proposals pending domain-expert review"** at the
  same tier as `#032` was post-chic-v11; the chic-v9 + v28
  framework-level negative continues to apply, and promotion to
  higher tiers requires specialist review out of polecat scope.
- **v26 per-surface verification status is structurally
  permissive.** Every top-20 surface across all four pools is
  classified "verified" under v26's per-surface verification
  status (verified = ≥1 source-A/B/C hit across any extended
  inscription where the surface has a positive paired-diff
  record). None falls into the "unverified" band. This high
  verification rate is partly structural: dense AB-sign pinning
  per hypothesis raises slot density per inscription, and source-
  B's 3..5-character toponym substrings have many search
  positions. The load-bearing negative-evidence companion is the
  per-pool sign-level inverse-verification table (19–30
  sign-level contradictions per pool), not the per-surface
  verified count.
- **AGENTS.md scope-of-work norms not yet updated for the chic
  sub-program.** The current AGENTS.md describes the Linear A
  workflow; the chic sub-program inherits it with minor
  variations (chic-v0 corpus ingest pattern, chic-vN ticket
  numbering, the documented chic-v1 → mg-0ea1 findings.md
  backfill incident). Codifying the chic-specific norms is a
  small follow-up; not load-bearing for the manuscript shape.

---

## 6. Conclusion

A mechanical, falsifiable framework for testing substrate-language
hypotheses against Linear A — paired-difference scoring under
external phoneme language models with phonotactically-matched
controls, aggregated as per-surface Beta-binomial posteriors and
gated against a right-tail Mann-Whitney U test — detects
substrate-LM-phonotactic kinship at the population level for **all
four** substrate hypotheses tested under their own LMs (Aquitanian
under Basque LM p = 3.22e-05; Etruscan under Etruscan LM
p = 5.21e-04; toponym under Basque LM with bigram-preserving control
p = 9.99e-05; Eteocretan under Eteocretan LM p = 4.10e-06), under
negative controls that confirm substrate-LM specificity. The
**gap-magnitude ordering** across the four pools is consistent with
a-priori genealogical relatedness: Eteocretan +0.20 (presumed
Linear-A linguistic descendant) > toponym +0.11 (Cretan pre-Greek
substrate) > Etruscan +0.06 > Aquitanian +0.03 (furthest-out
Mediterranean substrate). The **full cross-LM matrix** (v23,
mg-b599) shows own-LM dominance HOLDS for 3 of 4 pools (Eteocretan,
Etruscan, toponym); the Aquitanian deviation is a small-dynamic-
range artifact rather than a counterexample (no foreign LM produces
a gate PASS that own-LM does not, and Aquitanian under Mycenaean
Greek FAILs as expected). The framework also exhibits partial
within-tail shape selectivity: under cross-language pollution it
discriminates real Aquitanian surfaces from Greek-shape conjecturals
at p = 8.29e-05.

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
(AB67-AB02) — finds neither sequence in either tablet. v22 (mg-46d5)
broadens the external-validation footprint to a 35-entry curated
Younger-catalog scholar-proposed-reading set (76 AB-sign comparison
points across 6 sites and 21+ CV combinations); the aggregate
mechanical-vs-scholarly match rate is **3.95%** on the consonantal
first segment of the scholarly CV, with 32 of 35 entries scoring
zero — squarely in the pre-registered strong-null band (< 5%) for
"reinforces v13 / v19 / v20 verdicts". v24 (mg-c103) closes the
external-validation narrative: re-running the per-inscription
cascade analysis with v21's Eteocretan pool — the closest-
genealogical-relative substrate, and the strongest own-LM PASS in
the project — included produces **zero** cascade candidates under
eteocretan-only aggregation and a 0/76 (0.00%) match rate against
the scholar set, while the four-pool aggregation reproduces v19's
three cascade candidates with byte-identical high-coherence
mechanical readings on PS Za 2 and matches v22's 3.95% aggregate
rate to the digit. A substrate-LM swap to the closest-relative
pool — the strongest a-priori case in the validation series —
leaves the external-validation match rate unchanged.

The supportable claim is therefore strictly narrower than past
decipherment-shape claims for Linear A: the framework identifies
which substrate phonotactic profiles produce population-level signal
in the SigLA corpus, with the magnitude of that signal scaling with
a-priori genealogical relatedness, and identifies the specific
inscriptions on which that signal concentrates; but it does not
validate per-sign readings or per-tablet glosses — and where the
cascade candidates *do* admit external comparison to scholarly
ground truth, the mechanical reading diverges. **Internal consensus
among surviving substrate candidates does not imply external
correctness;** mechanical scoring against phonotactically-matched
controls, paired with external comparison to independent scholarly
proposals, is what distinguishes the framework's claim from the
qualitative-impression claims that have plagued past Linear A work.
The framework's null findings — no per-sign coherence at the global
aggregate level (v13), no real-vs-conjectural surface discrimination
at the same-distribution pollution level (v14), decisive divergence
on the one performable single-inscription external comparison
(v19 / v20), the 3.95% aggregate match rate (3/76) on a 35-entry,
6-site, 21+ CV-combination Younger-catalog scholar-proposed-reading
set (v22, mg-46d5; squarely in the pre-registered strong-null band),
the v24 confirmation that the closest-genealogical-relative
substrate's strongest-own-LM PASS does **not** propagate to a
per-inscription decipherment signal under any candidate substrate
the framework has tested, chic-v9's leave-one-out held-out
validation placing the chic-v5 per-sign extraction framework's
mechanical recovery on 20 known CHIC anchor classes at **20.0%
aggregate / 0/3 tier-2 unanimous correct** (near the ~16.7%
chance baseline for a 6-class phoneme taxonomy; in the low-
agreement / not-validated band per the chic-v9 brief's pre-
registered thresholds), and v28's symmetric Linear A-side leave-
one-out held-out validation placing the chic-v5 framework's
mechanical recovery on 21 LB-carryover anchors at **33.3%
aggregate / 0/3 tier-2 unanimous correct** (modestly above the
~16.7% chance baseline but below the 40% moderate-agreement
threshold; in the same low-agreement / not-validated band, with
the cross-script delta of +13.3 percentage points within the
regime that establishes **the at-chance per-sign behaviour is
structural to the chic-v5 framework rather than CHIC-corpus-
specific**)
— are themselves contributions to the methodological literature on
undeciphered-script analysis: each is a falsification result that
internal-only methodology, by construction, cannot produce. v26 (mg-c202) extends the external-
validation surface to the leaderboard-top-K granularity: each Linear
A pool's top-20 substrate surfaces produce a positive inscription-
count match-rate lift over the LB-carryover-only baseline
(177/772 = 22.93%) on the inscriptions where any top-20 surface has
a positive paired-diff record (aquitanian +5, etruscan +6, toponym
+7, eteocretan +5 — each clearing chic-v6's +3-inscription tier-1 →
tier-2 lift threshold on the CHIC side), with a load-bearing
sign-level inverse-verification companion table that contradicts
scholarly proposals at 19–30 AB-sign positions per pool. The
**cascade-candidate framing** (v19 + v24) and the **leaderboard-
top-K verification framing with sign-level inverse-verification
companion** (v26 / chic-v6) are jointly transferable: any research
group testing a substrate-language hypothesis on an undeciphered
script can adopt the protocol of finding inscriptions with high
local internal consensus and the protocol of mechanical verification
against external-scholarship sources at the leaderboard-top-K
granularity, then validating against external scholarly ground
truth, as discipline-protecting checks against motivated-reasoning
failure modes that internal-only analyses cannot catch.

**Cross-script extension (chic-v0..v14) and the symmetric Linear A
LOO companion (v28).** The chic sub-program
ports the framework verbatim to a second undeciphered Cretan
script — Cretan Hieroglyphic — and demonstrates that the Linear A
substrate-LM-phonotactic-kinship signal **transfers across
scripts under the same scoring infrastructure**, and that the
per-sign machinery layered on top of the population-level gate
**fails a held-out leave-one-out validation against known anchor
classes on both scripts** (CHIC 20.0% via chic-v9; Linear A 33.3%
via v28; both in the low-agreement / not-validated band; +13.3
percentage point cross-script delta within the regime that
establishes the at-chance per-sign behaviour as structural to the
chic-v5 framework rather than CHIC-corpus-specific). The Linear A
monotonic-with-relatedness ordering across the 4 substrate pools
(Eteocretan > toponym > Etruscan > Aquitanian) reproduces exactly
on CHIC: Eteocretan PASSes the right-tail bayesian gate on **both**
scripts (LA p=4.10e-06, gap +0.20; CHIC p=7.33e-04, gap +0.11);
the three more-distant pools' rank ordering is preserved on CHIC
even where their absolute signal-to-noise drops below α=0.05
under CHIC's smaller (~1,258-token vs Linear A's ~5,000-token)
syllabographic stream. Cross-script Spearman rank correlation on
the per-pool right-tail gap is **ρ=+1.000** across the 4 pools;
mean top-20 substrate-surface overlap is 0.47 (38/80 substrate-side
slots shared across the two scripts); per-substrate-surface
continuity is strongest for Eteocretan (Pearson +0.45) and degrades
monotonically with pool genealogical distance. The chic-v5
four-line-of-evidence per-sign value-extraction framework, applied
to 76 unknown CHIC syllabographic signs under the Eteocretan-LM
substrate-consistency line, classifies 3 as tier-2 candidate
proposals (≥3 of 4 lines agreeing on a coarse phoneme class —
`vowel`, `stop`, `nasal`, `liquid`, `fricative`, `glide`); the
chic-v9 leave-one-out held-out validation (mg-18cb) subsequently
places the same framework's mechanical recovery on the 20 known
chic-v2 anchors at **20.0% aggregate accuracy / 0/3 on the
tier-2 unanimity criterion** (near the ~16.7% chance baseline
for a 6-class taxonomy; in the low-agreement / not-validated band
per the chic-v9 brief's pre-registered thresholds), so the 3
tier-2 candidates are **candidate proposals contingent on the
framework's currently-low validation accuracy**, not
decipherments — and the discipline (mechanical agreement
predicate, explicit silent-line bookkeeping for the construction-
silent line 4, the L3-systematic-class-bias disclosure, plus
chic-v9's leave-one-out held-out validation as the falsification
check internal-consensus-only methodology cannot supply) is the
chic-v0..v14 sub-program's contribution rather than the count. A CHIC-side mechanical-verification pass
against the same three external-scholarship sources used by v26
(chic-v6, mg-a557) produces a small-but-non-zero +3-inscriptions /
+20-hits tier-1 → tier-2 lift; the larger tier-3 / tier-4 lifts
(+91 / +46 inscriptions) are caveated for class-level-matching
permissiveness in the absence of a phonotactically-matched
permutation control. A dual-script bilingual analysis (chic-v8,
mg-dfcc) verifies the Malia altar stone as **CHIC #328**,
unilingual-CHIC per the Olivier-Godart 1996 catalog, and finds
**no genuinely-dual-script artifact** in the v0 corpora; the fifth
line of evidence (L5, LA-constraint) is silent for all 76 unknown
CHIC syllabographic signs by corpus state, **0 new tier-2
candidates** are derivable on v0 corpora, and the chic-v5 tier-2
candidate count remains 3 — a publishable null result preserving
the bilingual extension as a falsifiable fifth axis contingent on
future corpus expansion. **chic-v9's leave-one-out held-out
validation (mg-18cb)** subsequently runs the chic-v5 framework
blind on the 20-anchor chic-v2 pool and places the per-sign
mechanical recovery at **20.0% aggregate accuracy / 0/3 on the
tier-2 unanimity criterion**, near the ~16.7% chance baseline for
a 6-class taxonomy and in the **low-agreement / not-validated
band** per the chic-v9 brief's pre-registered thresholds (>70%
high; 40-70% moderate; <40% low); per-line decomposition L1 =
20%, L2 = 20%, L3 = 5% (below chance, consistent with chic-v5's
disclosed Eteocretan-LM systematic class bias); the 3 chic-v5
tier-2 candidates are accordingly downgraded from "candidate
proposals pending domain-expert review by an Aegean-syllabary
specialist" to **"candidate proposals contingent on the
framework's currently-low validation accuracy"**, with chic-v6's
small-but-non-zero +3-inscription / +20-hit tier-1 → tier-2
mechanical-verification lift retained as independent evidence
that the candidates produce mechanical hits against external
scholarship and L4 (cross-script paleographic) preserved as a
falsifiable evidence axis pending hand-curated extension from
adjacent paleography scholarship. **v28's symmetric Linear A-side
leave-one-out validation (mg-4a7b)** then runs the chic-v5
framework blind on the 21-anchor LB-carryover pool with the L4
paleographic line again excluded for circularity (the LB-
carryover anchors' known values are themselves derived from
Linear B paleographic similarity, mirroring chic-v9's L4 rationale
on the CHIC side); the framework recovers known phoneme classes
at **33.3% aggregate accuracy** (7/21) and **0/3 on the tier-2
unanimity criterion** (anchors `AB06=na`, `AB08=a`, `AB27=re`,
all unanimous-but-wrong). Per-line decomposition L1=33.3%,
L2=33.3%, L3=9.5% — each ~13 percentage points above chic-v9's
CHIC-side numbers but still in the **low-agreement / not-
validated band**, closing the v28-pre-registered "structural vs
corpus-specific" question in favour of the structural-limitation
arm. **chic-v11 (mg-d69c)** then refines the per-candidate
framing within the chic-v9 generic downgrade with two within-
polecat-scope axes: **cross-pool L3 robustness** under all 4
substrate-pool LMs (12 cells) shows `#001 → wa`/glide is rejected
by 3 of 4 LMs (Eteocretan-LM-specific artifact), `#012 →
wa`/glide is rejected by 3 of 4 LMs (only Eteocretan supports
glide), and `#032 → ki`/stop is supported by 2 of 4 LMs
including the chic-v5 default Eteocretan plus Etruscan; and
**inscription-level metadata for the chic-v6 ku-pa-family lift**
attributable to `#032 → ki` corroborates on both sides (4
source Linear A tablets HT 1, HT 16, HT 102, HT 110a all LM IB
Hagia Triada accountancy tablets; matched CHIC #057 context
`#079 ki pa / NUM:20` is the canonical sign-run-followed-by-
numeral accountancy-formula structure). The post-chic-v11
per-candidate framing is **`#032 > #001 ≈ #012`** on within-
polecat-scope mechanical evidence — but the v28 + chic-v9
framework-level negative remains the dominant constraint, and
none of the three candidates clears specialist-review elevation
under the chic-v5 framework's currently-low accuracy band on
**either script**. **chic-v12 (mg-2035)** extends the
cross-pool L3 robustness check to the 29 chic-v5 tier-3
candidates and reclassifies 8 to ``tier-2-equivalent`` (≥1 non-
Eteocretan substrate LM corroborates the chic-v5 proposed class:
`#005`, `#017`, `#021`, `#039`, `#055`, `#056`, `#065`, `#072`),
4 to ``tier-3-corroborated`` (Eteocretan-only), 17 to
``tier-3-uncorroborated``. **chic-v13 (mg-5261)** runs within-
window context inspection on the 8 tier-2-equivalent candidates
following the chic-v11 ku-pa template: **6 consistent / 0
inconsistent / 2 inconclusive on corpus state**, with the
strongest evidence at `#072` (Knossos bar #065 `[stop:#072]-de
NUM` accountancy entries — direct mirror of chic-v11 ku-pa
structure), `#056` (Knossos bar #061 `[?] [stop:#056] NUM`
adjacent to `ke-de NUM:1`), and `#021` (3-fold cross-site
`031-021-061` recurrence + `ki-de` adjacency at #059).
**chic-v14 (mg-7f57)** then leave-one-out tests the chic-v12
cross-pool L3 reclassification rule on the 20 chic-v2 anchors
with **known** class as reference: 12 of 20 LOO iterations
reclassify to ``tier-2-equivalent`` (60.0%), so chic-v12's 27.6%
on the tier-3 set is **-32.4pp BELOW the LOO baseline → cross-
pool L3 reclassification on the tier-3 set is anti-evidentiary**.
**Cross-pool L3 is therefore demoted from a discipline-
protecting pillar to a permissive corroboration test**, useful
only in combination with at least one other independent line of
evidence; **within-window context inspection (chic-v13) becomes
the load-bearing fourth discipline pillar** post-chic-v14. The
post-chic-v14 per-candidate evidence-graded set: **n = 32
evidence-graded candidates** with **7 carrying paired cross-pool
L3 + within-window context-inspection evidence** (`#032` chic-v11
+ 6 chic-v13 consistent), 2 inconclusive on context state
(`#055`, `#065`), 2 chic-v11-demoted (`#001`, `#012`), 4
Eteocretan-only L3 corroborated (`#006`, `#033`, `#050`, `#063`),
17 cross-pool L3 not corroborated. **The v28 + chic-v9 +
chic-v14 framework-level negative remains the dominant
constraint**; none of the 7 paired-evidence candidates clears
specialist-review elevation; all remain "candidate proposals
pending domain-expert review" at the same tier as `#032` was
post-chic-v11. The cross-script claim the
chic sub-program adds to the methodology paper, beyond what the
single-script v25 manuscript could support, is therefore: **the
substrate-LM-phonotactic-kinship signal the framework detects is
not Linear-A-corpus-specific; it is a cross-script substrate-
detection signature whose per-pool ordering tracks candidate-
substrate genealogical relatedness to the target script's
underlying language identically across two independent
undeciphered Cretan scripts**, and the **mechanical-verification
methodology against pre-registered external-scholarship sources
runs symmetrically on both sides** (v26 on Linear A, chic-v6 on
CHIC) at the leaderboard-top-K granularity, while the **leave-
one-out held-out validation runs symmetrically on both sides**
(v28 on Linear A, chic-v9 + chic-v14 on CHIC) at both the
per-sign value-extraction granularity (chic-v9 / v28; 20.0% /
33.3% LOO accuracy on the chic-v5 four-line framework) and the
per-candidate evidence-graded granularity (chic-v14; 60.0% LOO
baseline on cross-pool L3 reclassification, demoting cross-pool
L3 to permissive corroboration), with the **bilingual fifth-axis
extension reported as a null result** on the v0 corpus state
under the same anti-motivated-reasoning discipline. Per-sign
decipherment remains unsupported on either script.

**Five discipline-protecting pillars (post-v30 register).** The
chic-v0..v14 + Linear A v0..v28 evidence base is most usefully
read as the union of five pre-registered falsifiable pillars,
each catching a different motivated-reasoning failure mode that
internal-consensus-only methodology, by construction, cannot
catch:

1. **Per-surface coherence** (v13, mg-c216). Cross-window-
   consensus median 0.18 against a 0.6 bar; the framework cannot
   produce a stable per-sign sign-to-phoneme map across the v10
   top-20 substrate surfaces' candidate equations. Catches the
   "framework converges on a stable mapping" failure mode.
2. **Per-inscription cascade-candidate external validation**
   (v19 / v20 / v24, mg-3438 + mg-711c + mg-c103). On the
   cascade candidate that admits scholarly comparison
   (`PS Za 2` libation formula), the mechanical reading diverges
   from the scholarly proposal at 0/5 consonantal-segment match;
   targeted accountancy follow-up on `KH 10` / `KH 5` returns
   null comparand; v22 / v24 sign-level inverse-verification
   companion produces 19–30 sign-level contradictions per pool
   on Linear A. Catches the "internal-consensus inscription is
   correctly read" / "population-level matching averages out
   individual divergence" failure modes.
3. **Population-level scholar comparison + leaderboard-top-K
   mechanical verification** (v22 / v26 / chic-v6, mg-46d5 +
   mg-c202 + mg-a557). Aggregate match rate 3.95% (3/76) on the
   35-entry Younger scholar set; substrate-LM swap to the
   closest-genealogical-relative pool (Eteocretan) leaves the
   rate unchanged at four-pool (3.95%) and produces 0.00% under
   eteocretan-only. Leaderboard top-K verification produces
   small-but-non-zero inscription-count lift on both scripts
   (+5/+6/+7/+5 across LA pools, +3 inscriptions on the chic-v6
   tier-1 → tier-2 lift); the larger tier-3 / tier-4 lifts on
   CHIC are caveated for class-level-matching permissiveness.
   Catches the "population-level signal propagates to per-sign
   correctness" failure mode.
4. **Within-window context inspection** (chic-v11 / chic-v13,
   mg-d69c + mg-5261). The chic-v11 `#032 → ki` ku-pa
   accountancy-formula corroboration (CHIC #057 `#079 ki pa /
   NUM:20` + 4 source LM IB Hagia Triada accountancy tablets HT
   1, HT 16, HT 102, HT 110a) and the chic-v13 6-of-8 consistent
   verdict on the chic-v12 tier-2-equivalent candidates jointly
   constitute the **fourth discipline-protecting pillar**, load-
   bearing as of chic-v14. Catches the "cross-pool L3
   corroboration alone confirms a class-level value" failure
   mode that chic-v14's LOO baseline finding (60.0% on known
   anchors) made acute. The chic-v11 + chic-v12 cross-pool L3
   robustness check is **demoted from a discipline-protecting
   pillar in its own right to a permissive corroboration test
   that requires within-window context evidence to be load-
   bearing**: chic-v14's leave-one-out test recovered known
   class to ``tier-2-equivalent`` at 60.0%, vs chic-v12's 27.6%
   on the chic-v5 tier-3 set → -32.4pp anti-evidentiary verdict
   on cross-pool L3 reclassification on the tier-3 set, and the
   per-candidate evidence-grading work cross-pool L3 supports is
   itself bounded above by within-window context inspection
   pairing.
5. **Leave-one-out held-out validation against known anchors**
   (chic-v9 / v28 / chic-v14, mg-18cb + mg-4a7b + mg-7f57). The
   chic-v5 framework's L1+L2+L3 mechanical recovery on known
   anchor classes is **20.0% on CHIC and 33.3% on Linear A**
   when run blind under leave-one-out, both in the low-agreement
   / not-validated band per the chic-v9 brief's pre-registered
   thresholds, with **0/3 on the tier-2 unanimity criterion on
   both scripts**. **chic-v14 (mg-7f57)** extends the LOO pillar
   a second time by running held-out validation on the chic-v12
   cross-pool L3 reclassification rule itself, recovering known
   anchor class to ``tier-2-equivalent`` at 60.0% LOO baseline →
   chic-v12's 27.6% on the chic-v5 tier-3 set is -32.4pp below
   the LOO baseline → cross-pool L3 reclassification is anti-
   evidentiary on the tier-3 set; this is the demotion that
   relegates pillar 4 to within-window context inspection.
   Catches the **"framework that produces candidates fails to
   recover known values when run blind"** and the **"permissive
   corroboration mistaken for discriminative gate"** failure
   modes — the framework-level falsification check that
   internal-consensus-only methodology cannot supply.

The five pillars point in the same methodological direction
across the project's full ticket sequence: the framework detects
substrate-LM-phonotactic kinship at the population level
faithfully, and it produces no per-sign decipherment-grade
output that survives any of the five held-out / external /
cross-pool / cross-script validation channels. Each pillar
catches a *different* failure mode; their conjunction is the
methodology paper's central contribution. The pillar-4 demotion
of cross-pool L3 robustness from a discipline-protecting axis
to a permissive corroboration test is itself a discipline-
protecting outcome: the held-out validation pillar (chic-v14)
caught a permissive corroboration axis (chic-v11 + chic-v12
cross-pool L3) before it could load-bear in the methodology
paper, demonstrating that the discipline pillars work.

The chic-v5 + chic-v6 + chic-v8 framing of the three chic-v5
tier-2 CHIC candidates (`#001 → wa`, `#012 → wa`, `#032 → ki`)
remains "candidate proposals contingent on the framework's
currently-low validation accuracy on both scripts", with the
chic-v11 per-candidate refinement noting that `#032` retains the
strongest evidentiary basis of the three (cross-pool L3 weakly
corroborates + chic-v6 ku-pa lift contextually corroborated on
both sides) while `#001` and `#012` are weakened beyond the
chic-v9 generic downgrade (cross-pool L3 actively undermines).
**Post-v30 the per-candidate evidence-graded set extends to n =
32 candidates** (3 chic-v5 tier-2 + 29 chic-v5 tier-3) across
two coarse evidence axes:

| paired-evidence status | n | identity |
|---|---:|---|
| **cross-pool L3 + context-inspection consistent** | **7** | `#032` (chic-v11), `#021`, `#005`, `#072`, `#017`, `#039`, `#056` (chic-v13) |
| cross-pool L3 only (context inspection inconclusive on corpus state) | 2 | `#055`, `#065` |
| chic-v5 tier-2 / cross-pool L3 fail | 2 | `#001`, `#012` |
| chic-v5 tier-3 / cross-pool L3 not corroborated | 17 | (tier-3-uncorroborated set) |
| chic-v5 tier-3 / Eteocretan-only L3 corroborated | 4 | `#006`, `#033`, `#050`, `#063` |

The 7 paired-evidence candidates remain "candidate proposals
pending domain-expert review" at the same tier as `#032` was
post-chic-v11. Promotion to higher tiers (chic-v2 anchor;
"domain-expert-confirmed") requires specialist review out of
polecat scope. The framework-level negative bound on per-sign
decipherment is unchanged; v30's contribution is granularity
within the chic-v9 + v28-validated low-accuracy band, not
displacement of the chic-v9 / v28 verdict.

---

## 7. Three-sentence reading test

The methodology paper canonical reading test, established at v16
(mg-d5ed) for Linear A, extended to cross-script by chic-v7
(mg-9508), updated for the now-fully-cross-script + symmetric-
mechanical-verification document by v27 (mg-b731), updated again
for the post-chic-v9 register by chic-v10 (mg-1178), updated for
the post-v28 + chic-v11 register by v29 (mg-a1e2), and updated
again here for the post-chic-v12 + chic-v13 + chic-v14 register
by v30 (mg-ee1f), asks: what would a hypothetical Linear-A
scholar (or broader Aegean-syllabary specialist) reading this
document cold learn from it? Three sentences, in the narrower-
but-defensible register the v16 reading test established and the
v28 + chic-v9 + chic-v11 + chic-v14 verdicts have tightened:

1. **What the framework detects (population level, both scripts).**
   A mechanical, falsifiable substrate-LM-phonotactic-kinship test
   — paired-difference scoring under external phoneme language
   models with phonotactically-matched controls, aggregated as
   per-surface Beta-binomial posteriors and gated by a right-tail
   Mann-Whitney U test on top-K=20 substrate vs top-K=20 matched-
   control surfaces — detects population-level kinship between four
   candidate substrate pools (Aquitanian/Vasconic, Etruscan, pre-
   Greek Aegean toponyms, Eteocretan) and two undeciphered Cretan
   scripts (Linear A SigLA, Cretan Hieroglyphic Younger web edition),
   with the per-pool gate-magnitude ordering tracking a-priori
   genealogical relatedness identically across both scripts
   (Eteocretan > toponym > Etruscan > Aquitanian; cross-script
   Spearman ρ=+1.000 on per-pool right-tail gap; mean top-20
   substrate-surface overlap 0.47 across the two scripts).

2. **Per-sign decipherment is unsupported on either script, and
   the framework's per-sign mechanical recovery on known anchors
   via L1+L2+L3 is at chance baseline on both scripts (CHIC 20%,
   Linear A 33%); per-sign value-extraction proposals from
   chic-v5 / its LA analog are downgraded accordingly, and the
   chic-v11 + chic-v12 cross-pool L3 robustness check is itself
   demoted by chic-v14 LOO from a discipline-protecting axis to
   a permissive corroboration test (60.0% LOO baseline on known
   anchors vs chic-v12's 27.6% on the tier-3 set = -32.4pp anti-
   evidentiary).** On Linear A the v13 cross-window coherence
   median is 0.18 against a 0.6 bar, v22/v24 internal-consensus
   mechanical readings match the Younger 35-entry scholar-
   proposed-reading set at an aggregate 3.95% rate (3/76) —
   squarely in the strong-null band — and v26's per-pool sign-
   level inverse-verification companion table reports 19–30 sign-
   level contradictions of scholarly proposals per pool; **chic-
   v9's CHIC-side leave-one-out held-out validation places the
   chic-v5 framework's mechanical recovery on the 20 known
   chic-v2 anchors at 20.0% aggregate accuracy / 0/3 on the
   tier-2 unanimity criterion**, and **v28's symmetric Linear
   A-side leave-one-out validation places the same framework's
   mechanical recovery on the 21 LB-carryover anchors at 33.3%
   aggregate / 0/3 tier-2 unanimous correct** — both in the
   low-agreement / not-validated band per the chic-v9 brief's
   pre-registered thresholds (>70% high; 40-70% moderate; <40%
   low; chance baseline ~16.7% for the 6-class taxonomy), with
   the +13.3 percentage-point cross-script delta within the
   regime that establishes **the at-chance per-sign behaviour as
   structural to the chic-v5 framework rather than CHIC-corpus-
   specific**, so the 3 chic-v5 tier-2 candidate class-level
   proposals on CHIC (`#001` glide, `#012` glide, `#032` stop)
   are **candidate proposals contingent on the framework's
   currently-low validation accuracy on both scripts**, not
   decipherments. **chic-v12 / chic-v13 / chic-v14 (mg-2035 +
   mg-5261 + mg-7f57)** then build a **per-candidate evidence-
   graded set spanning n = 32 candidates** (3 chic-v5 tier-2 +
   29 chic-v5 tier-3) across two coarse axes — cross-pool L3
   corroboration and within-window context inspection — and
   surface **7 paired-evidence candidates** carrying both axes
   (`#032` chic-v11 + 6 chic-v13 consistent: `#005`, `#017`,
   `#021`, `#039`, `#056`, `#072`); 2 inconclusive on context
   state (`#055`, `#065` — corpus-quality limitation); 2
   chic-v11-demoted (`#001`, `#012`); 4 Eteocretan-only L3
   corroborated; 17 cross-pool L3 not corroborated. chic-v14's
   LOO baseline of 60.0% on known anchors against chic-v12's
   27.6% on the tier-3 set produces a **-32.4pp anti-evidentiary
   verdict on cross-pool L3 reclassification on the tier-3 set**,
   demoting cross-pool L3 robustness from a discipline-protecting
   axis to a permissive corroboration test and elevating
   **within-window context inspection (chic-v13) to the load-
   bearing fourth discipline pillar**. The 7 paired-evidence
   candidates remain "candidate proposals pending domain-expert
   review" at the same tier as `#032` was post-chic-v11;
   chic-v6's small-but-non-zero +3-inscription / +20-hit tier-1
   → tier-2 mechanical-verification lift is retained as
   independent evidence; L4 (cross-script paleographic) is
   preserved as a falsifiable evidence axis pending hand-curated
   extension from O&G 1996 / Salgarella 2020 / Decorte 2017
   paleography scholarship; the chic-v8 dual-script bilingual
   fifth-axis extension produces 0 new tier-2 candidates on v0
   corpora because no genuinely-dual-script artifact (the
   candidate Malia altar stone CHIC #328 is unilingual-CHIC per
   Olivier-Godart 1996) is ingested in either v0 corpus; and the
   chic-v9 + v28 + chic-v14 framework-level negative remains the
   dominant constraint, with v30's per-candidate evidence-graded
   refinement strictly inside the chic-v9-validated low-accuracy
   band rather than displacing chic-v9's verdict.

3. **The cross-script methodological contribution: five
   discipline-protecting pillars (post-v30 register).** The
   methodology paper's accumulated contribution across its 28
   Linear A + 14 chic sub-program tickets is best read as **five
   pre-registered falsifiable pillars**, each catching a
   different motivated-reasoning failure mode that internal-
   consensus-only analyses cannot catch — (i) **per-surface
   coherence** (v13, mg-c216), (ii) **per-inscription cascade-
   candidate external validation** (v19 / v20 / v24, mg-3438 +
   mg-711c + mg-c103, with v22 / v26 sign-level inverse-
   verification companion at 19–30 contradictions per pool),
   (iii) **population-level scholar comparison + leaderboard-
   top-K mechanical verification** (v22 / v26 / chic-v6, mg-46d5
   + mg-c202 + mg-a557; 3.95% LA aggregate match rate; small-
   but-non-zero +3-inscription / +20-hit chic-v6 tier-1 → tier-2
   lift), (iv) **within-window context inspection** (chic-v11 /
   chic-v13, mg-d69c + mg-5261; chic-v11 `#032`/CHIC #057 ku-pa
   accountancy-formula corroboration + chic-v13 6-of-8 consistent
   verdict on the chic-v12 tier-2-equivalent candidates;
   load-bearing as the fourth discipline pillar post-chic-v14,
   replacing cross-pool L3 robustness in that role), and
   (v) **leave-one-out held-out validation** (chic-v9 / v28 /
   chic-v14, mg-18cb + mg-4a7b + mg-7f57; LOO accuracy 20.0% on
   CHIC and 33.3% on Linear A on the chic-v5 four-line
   framework; 0/3 on the tier-2 unanimity criterion on both
   scripts; chic-v14's 60.0% LOO baseline on the chic-v12
   cross-pool L3 reclassification rule produces the -32.4pp
   anti-evidentiary verdict that demoted cross-pool L3 in
   pillar 4) — together with the cross-script transfer
   demonstration (chic-v3 / chic-v4 Spearman ρ=+1.0 on per-pool
   gate gap; mean top-20 substrate-surface overlap 0.47 across
   the two scripts), the falsifiable bilingual fifth-axis
   extension (chic-v8, silent on v0 corpus state, reactivable
   under future corpus expansion), the chic-v11 per-candidate
   within-polecat-scope refinement (mg-d69c, asymmetric
   `#032 > #001 ≈ #012` framing within the chic-v9 generic
   downgrade), and the post-chic-v14 per-candidate evidence-
   graded set (n = 32 candidates with 7 carrying paired cross-
   pool L3 + within-window context-inspection evidence remaining
   as "candidate proposals pending domain-expert review"
   contingent on the chic-v9 + v28 + chic-v14 framework-level
   negative), constitute a **transferable cross-script
   methodology** that any research group testing a substrate-
   language hypothesis on an undeciphered script can adopt; the
   framework's negative findings on Linear A (v13 / v14 / v19 /
   v20 / v22 / v24 / v26 / v28) together with its cross-script
   transfer on CHIC (chic-v3 / chic-v4 / chic-v5 / chic-v6 /
   chic-v8 / chic-v9 / chic-v11 / chic-v12 / chic-v13 / chic-v14)
   are themselves the methodological deliverable — a discipline-
   protecting protocol that catches motivated-reasoning failure
   modes which internal-only analyses produce uniformly across
   scripts, substrate pools, external-validation channels, and
   the population / per-sign axis, including (via chic-v14) the
   failure mode of treating a permissive corroboration axis as
   a discriminative gate.

---

## Appendix A: result-file index

Every quantitative claim in this document maps to one or more
committed artefacts under `results/`:

| claim source | committed file |
|:--|:--|
| v10 own-LM gate (Aquitanian, Etruscan, Toponym) | `rollup.bayesian_posterior.{aquitanian,etruscan,toponym}.md` |
| v21 Eteocretan own-LM gate (mg-6ccd) | `rollup.bayesian_posterior.eteocretan.md` |
| v21 Eteocretan cross-LM under Basque (mg-6ccd) | `rollup.bayesian_posterior.eteocretan_under_basque.md` |
| v11 cross-LM gate | `rollup.bayesian_posterior.{aquitanian_under_etruscan_lm,etruscan_under_basque_lm}.md` |
| v12 third-LM (Mycenaean Greek) gate | `rollup.bayesian_posterior.{aquitanian,etruscan}.under_mycenaean_greek_lm.md` |
| v23 full cross-LM matrix for Eteocretan (mg-b599) | `rollup.cross_lm_matrix.md` plus `rollup.bayesian_posterior.eteocretan.under_{mg,etruscan}_lm.md` plus `rollup.bayesian_posterior.{aquitanian,etruscan,toponym}.under_eteocretan_lm.md` |
| v12 Linear-B positive control | `rollup.bayesian_posterior.linear_b_carryover.md` |
| v13 consensus sign-to-phoneme map + per-pool coherence + K-sweep | `consensus_sign_phoneme_map.md` |
| v14 same-distribution pollution gate + provenance | `rollup.bayesian_posterior.polluted_aquitanian.md` + `…provenance.md` |
| v15 cross-language pollution gate + provenance | `rollup.bayesian_posterior.greek_polluted_aquitanian.md` + `…provenance.md` |
| per-inscription concentration | `rollup.right_tail_inscription_concentration.md` |
| v19 per-inscription coherence + cascade candidates | `rollup.per_inscription_coherence.md` |
| v20 KU-RO / KI-RO scholarly-anchor search on `KH 10` / `KH 5` | `corpus/Khania/KH%2010.json`, `corpus/Khania/KH%205.json` (token streams) + `pools/linear_b_carryover.yaml` (canonical AB-sequence anchors) |
| v22 population-level external validation against Younger scholar-set (mg-46d5) | `rollup.scholar_proposed_readings_comparison.md` + `../corpora/scholar_proposed_readings/all.jsonl` (35-entry curated set) |
| v24 per-inscription cascade-candidate analysis under Eteocretan LM (mg-c103) | `rollup.per_inscription_coherence.eteocretan_only.md`, `rollup.per_inscription_coherence.four_pools.md`, `rollup.right_tail_inscription_concentration.eteocretan_only.md`, `rollup.right_tail_inscription_concentration.four_pools.md`, `rollup.scholar_proposed_readings_comparison.eteocretan_only.md`, `rollup.scholar_proposed_readings_comparison.four_pools.md`, `rollup.scholar_proposed_readings_comparison.four_pools_cascades.md` |
| chic-v0 CHIC corpus ingest (mg-99df) | `../corpora/cretan_hieroglyphic/all.jsonl` + `../corpus_status.chic.md` |
| chic-v1 CHIC sign classification + paleographic candidates (mg-c7e3) | `../pools/cretan_hieroglyphic_signs.yaml`, `chic_sign_inventory.md`, `chic_vs_linear_a_sign_inventory_comparison.md` |
| chic-v2 CHIC paleographic anchor inheritance + partial-reading map (mg-362d) | `../pools/cretan_hieroglyphic_anchors.yaml`, `chic_partial_readings.md`, `chic_anchor_density_leaderboard.md`, `chic_mg_perplexity_sanity_check.md` |
| chic-v3 substrate framework on CHIC, 4 pools, right-tail bayesian gate per pool (mg-9700) | `../corpora/cretan_hieroglyphic/syllabographic.jsonl`, `../corpora/cretan_hieroglyphic/syllabographic_stats.md`, `experiments.external_phoneme_perplexity_v0.chic.jsonl`, `rollup.bayesian_posterior.{aquitanian,etruscan,toponym,eteocretan}.chic.md`, `rollup.bayesian_posterior.chic.md` (combined) |
| chic-v4 cross-script correlation analysis Linear A vs CHIC (mg-c769) | `rollup.linear_a_vs_chic_substrate_comparison.md` |
| chic-v5 per-sign syllable-value extraction framework (mg-7c6d) | `chic_value_extraction_leaderboard.md`, `chic_anchor_distance_map.md`, `chic_substrate_consistency.md`, `../harness/chic_sign_fingerprints.json`, `../pools/cretan_hieroglyphic_signs.distributional.yaml` |
| chic-v6 mechanical verification pass on chic-v5 candidate proposals (mg-a557) | `chic_extended_partial_readings.md`, `chic_verification_match_rates.md`, `experiments.chic_verification_v0.jsonl` |
| v26 Linear A-side leaderboard top-K mechanical verification (mg-c202) | `rollup.linear_a_top_k_verification.aggregate.md`, `rollup.linear_a_top_k_verification.{aquitanian,etruscan,toponym,eteocretan}.md`, `experiments.linear_a_top_k_verification_v0.jsonl` |
| chic-v8 dual-script bilingual analysis (mg-dfcc) | `chic_dual_script_bilingual_leaderboard.md`, `chic_v8_promoted_candidates.md` |
| chic-v9 leave-one-out held-out validation of the chic-v5 framework on the chic-v2 anchor pool (mg-18cb) | `chic_v9_loo_validation.md` |
| v28 Linear A-side analogous LOO validation of the chic-v5 framework on LB-carryover anchors (mg-4a7b) | `v28_la_loo_validation.md` |
| chic-v11 cross-pool L3 robustness check + #032 ku-pa context inspection on the 3 chic-v5 tier-2 candidates (mg-d69c) | `chic_v11_cross_pool_l3.md`, `chic_v11_032_ku_pa_context.md` |
| chic-v12 cross-pool L3 robustness check on the 29 chic-v5 tier-3 candidates (mg-2035) | `chic_v12_cross_pool_l3.md`, `chic_v12_tier3_summary.md` |
| chic-v13 within-window context inspection on the 8 chic-v12 tier-2-equivalent candidates (mg-5261) | `chic_v13_context_inspection.md`, `chic_v13_summary.md` |
| chic-v14 leave-one-out held-out validation of the chic-v12 cross-pool L3 reclassification methodology on the 20 chic-v2 anchors (mg-7f57) | `chic_v14_loo_validation.md`, `chic_v14_summary.md` |
| corpus ingestion record | `../corpus_status.md` |

Per-ticket merge notes are in `docs/findings.md` under
`## Findings from mg-XXXX` headers, in chronological order from
`mg-1c8c` (SigLA corpus ingest, 2026-05-04) through `mg-7f57`
(chic-v14, 2026-05-06); the Linear A harness pipeline itself spans
`mg-d5ef` (v0, 2026-05-04 first harness commit) through `mg-4a7b`
(v28, 2026-05-06), with mg-711c (v20) a documentation-and-
investigation ticket that adds no harness code path and mg-36bd
(v25), mg-9508 (chic-v7), mg-b731 (v27), mg-1178 (chic-v10),
mg-a1e2 (v29), and mg-ee1f (v30) editorial-only methodology-paper
polish passes. The
chic sub-program spans `mg-99df` (chic-v0 corpus ingest) through
`mg-7f57` (chic-v14 leave-one-out held-out validation of the
chic-v12 cross-pool L3 reclassification methodology).
The repo scaffold (`mg-9e00`) predates `findings.md`'s
introduction in `mg-13a2` and so does not have a per-ticket entry
there.
