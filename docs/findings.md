# Lineara research findings

*Append-mostly. Each merge that produces a substantive observation appends a
"## Findings from mg-XXXX" subsection. Curated edits happen only when a prior
finding is explicitly superseded.*

This file is the durable, scientific counterpart to `docs/roadmap.md` (which
is plan-oriented and rewritten each pm-lineara sweep). The roadmap tracks
**what we're doing**; this file tracks **what we've learned** — observations,
metric limitations, hypothesis distributions, and known gaps. Findings should
be readable in under 5 minutes; raw rows live in `results/experiments.jsonl`,
and curated leaderboards live in `results/rollup.*.md`.

## Mission summary

Linear A is undeciphered, and the realistic posture is that no single
hypothesis will crack it. The lineara repo runs a long tail of cheap,
falsifiable, mechanically-scored experiments whose mostly-null results
gradually constrain the space — decipherment-by-compression-improvement,
many small bets, no narrative leaps. The working candidate substrate is the
old-European root layer: toponyms, Basque / Aquitanian, Etruscan, and adjacent
pre-IE material. None of these is assumed to be "the" answer; they are scored.

A "cheap-test multiplier" is in the design from the start: candidate roots
carry geographic and semantic provenance, so a second-stage filter can
re-rank a leaderboard by whether the candidate's region / semantic field
match the inscription's findspot and genre hint. This filter is queued behind
the bulk-distribution baseline.

The mission brief explicitly accepts mostly-null results as the common case.
The harness, the result schema, and this findings log are all designed
around that — null findings ship the same as positive ones, and the
discipline of mechanical scoring (no human in the scoring loop) is the
protection against motivated-reasoning failure modes that have plagued past
Linear A decipherment attempts.

## Corpus state

- Source: SigLA (Salgarella & Castellan, https://sigla.phis.me), built on
  GORILA (Godart & Olivier 1976–85). License: CC BY-NC-SA 4.0.
- Coverage: **772** documents listed in SigLA, **772 (100%)** ingested as
  records, **761 (98.6%)** carry at least one transcribed sign, **4,935**
  total transcribed sign occurrences across **356** distinct sign IDs.
- Site distribution skews hard: Haghia Triada 372, Khania 213, Phaistos 63;
  the remaining 14 sites contribute < 125 records combined.
- Token vocabulary: `AB##` and `A###` syllabograms (sure), `[?:AB54]`
  (unsure reading), `[?]` (unreadable / erasure), `LOG:<id>` (logogram),
  `FRAC:<id>` (fraction), `DIV` (word divider). Bare-id transaction signs
  intentionally collapse with syllabograms (orthographically identical).
- Token role frequencies (top 4): bare `AB##` 2,906 · `DIV` 2,212 ·
  `LOG:<id>` 1,119 · `[?]` 388.
- Determinism: `corpus/all.jsonl` is sorted by inscription id and rebuilt
  byte-identically from the per-inscription JSONs.
- Round-trip cross-check: all 761 transcribed inscriptions reproduce SigLA's
  word-view seq-patterns under the v1 inverse mapping (verified by
  `scripts/check_corpus.py`).
- Known gaps: 11 drawing-only inscriptions (`n_signs=0`, transcribed in
  `corpus_status.md`), no numerals (SigLA does not encode them as signs),
  no line-break tokens (SigLA preserves layout via SVG coordinates only).
- Full corpus details: `corpus_status.md`.

## Harness state

- Hypothesis shapes:
  - `hypothesis.v0` (mapping) — global sign → phoneme mapping. Default
    metric: `compression_delta_v0`. Schema:
    `harness/schemas/hypothesis.v0.schema.json`.
  - `candidate_equation.v1` (local) — "this Linear A sign sequence in this
    inscription = this candidate substrate root." Default metric:
    `local_fit_v0`. Schema:
    `harness/schemas/hypothesis.candidate_equation.v1.schema.json`.
- Metrics:
  - `compression_delta_v0` — zlib L9 compression delta over a deterministic
    2-byte symbol-id encoding of the corpus token stream. Reflects
    structural compressibility, not phoneme name length.
  - `local_fit_v0` — position-fit term (Bhattacharyya coefficient between
    each sign's corpus position fingerprint and the proposed phoneme's
    expected position profile) plus a phoneme-class bigram log-likelihood
    under a hardcoded Basque-style CV phonotactic prior. Each row records
    `score_control_z` standardized against 200 random
    phoneme-permutations (seed=42, frozen for v0).
  - `local_fit_v1` (mg-7dd1) — absolute-units variant. Mean per-pair
    `log(BC + floor)` position term + mean per-bigram log-prob under an
    *empirical* bigram model trained on the active pool's surfaces +
    a `1/n` length penalty + a rare-sign correction (signs with corpus
    count < 5). No per-hypothesis z, so cross-hypothesis ranks are
    directly comparable. Diagnostic terms `position_term`, `bigram_term`,
    `length_penalty`, `rare_sign_correction` persisted on each row.
  - `geographic_genre_fit_v1` (mg-7dd1) — categorical compat score in
    [0, 1] from `α * region_compat + (1 - α) * semantic_compat`,
    α=0.4 default. Region compat reads (pool-region × inscription-site)
    from a small sourced lookup table; semantic compat reads
    (pool-semantic_field × inscription-genre_hint). Missing or unmapped
    pairs fall back to neutral 0.5. Diagnostic terms `region_compat`
    and `semantic_compat` persisted on each row.
- Result stream: append-only `results/experiments.jsonl`, validated against
  `harness/schemas/result.v0.schema.json`. Every row carries
  `hypothesis_hash`, `harness_version`, `corpus_snapshot`, and `metric` so
  rows whose hypothesis YAML has since been edited are detectable
  (hash mismatch) and ignorable.
- Determinism contract: same hypothesis + same corpus snapshot ⇒
  byte-identical scores. Re-runs add new rows with a fresh `run_id`; rows
  are never edited or deleted.
- Bulk pipeline: `scripts/generate_candidates.py` turns a substrate-root
  pool YAML into thousands of candidate-equation hypotheses;
  `scripts/run_sweep.py --metrics m1,m2 [--pool ...]` is resumable
  (resume key is `(hash, snapshot, metric)`, so each metric can be
  re-run independently) and prints a per-metric histogram + summary at
  the end; `scripts/rollup.py --pool <name>` renders a per-pool
  leaderboard, or with `--metrics m1,m2 --weights w1,w2 --normalize zscore`
  produces a composite leaderboard joining rows across metrics by
  hypothesis.

## Findings by ticket (chronological, append-only)

### Findings from mg-1c8c (corpus ingest, 2026-05-04)

- SigLA's actual public corpus is **smaller** than the original ingest
  ticket estimated (~1,400). True size: 772 documents. We ingested all of
  them — 772/772 records, 761/761 transcribed inscriptions round-trip. The
  acceptance criterion (≥ 80% of SigLA coverage) is satisfied at ~98.6%.
- **Two-stage scrape design (fetch + parse) survives a re-pull cleanly.**
  `scripts/fetch_sigla.py` caches HTML under `.cache/sigla/` and is
  idempotent; `scripts/parse_sigla.py` re-runs in under 5 s without
  touching the network. SigLA's `database.js` is an OCaml `js_of_ocaml`
  bytecode bundle — we did not attempt to decode it; the public per-document
  HTML pages are sufficient.
- **SigLA does not encode numerals as signs** — only the AB-numbered
  syllabograms / logograms / fractions / dividers we already tokenize. The
  v1 spec's `NUM:<value>` token is reserved for a future GORILA / Younger
  pull. Many tablets that look like commodity records will read sparser
  than they actually are.
- **No line-break tokens.** SigLA preserves layout via absolute SVG
  coordinates, not discrete line markers. Reconstruction would need a
  y-coordinate clustering pass on the rect data; not done in v1.
- **Word-boundary semantics: in-word non-syllabograms inherit the surrounding
  word group.** A fraction or logogram sandwiched between two same-word
  signs is treated as part of the word, mirroring SigLA's visual word
  preservation. Standalone non-word signs are emitted as their own
  `DIV`-delimited groups.
- **Genre hint is heuristic, not authoritative.** "Accountancy" sweeps up
  742/772 records purely because tablets / roundels / nodules dominate the
  Linear A corpus; the label is for coarse filtering only.
- See `corpus_status.md` for the full per-rule tokenization mapping, the
  11 drawing-only inscription IDs, and seven additional caveats
  (HT 22 metadata mismatch, `&amp;` HTML entities in `corpus_link`, etc.).

### Findings from mg-d5ef (harness v0, 2026-05-04)

- **Identity hypothesis (empty mapping) scored exactly 0.0** on
  `compression_delta_v0`, as the metric design predicts. Confirms the
  baseline encoding and the metric's "no mapping = no score" property.
- **Younger AB54 → /ti/ scored +72.0 bits compression delta** on the real
  761-record corpus (`bits_per_sign_baseline=6.6017` →
  `bits_per_sign_mapped=6.5926`). A single high-frequency-sign mapping
  produces a measurable, reproducible compression improvement; the metric
  responds non-trivially to a single sign substitution if the sign is
  frequent enough.
- **Determinism verified end-to-end.** Reruns of either hypothesis produced
  bit-identical scores; the smoke test asserts byte-equality across
  consecutive runs.
- The `compression_delta_v0` metric design — encoding by sorted symbol id,
  not by phoneme name length — was a deliberate choice to keep scores
  reflecting structural compressibility rather than the cosmetic length
  of phoneme labels. Future global mappings will inherit this.

### Findings from mg-fb23 (harness v1, 2026-05-04)

- **Acceptance gate cleared.** Linear-B carryover anchor bucket median
  `score_control_z` = **+1.140** vs random-scramble bucket median = **0.000**.
  The metric distinguishes plausible substrate readings from random
  nonsense at n=4 per bucket.
- **One anchor outlier:** `anchor_taina_HT39` reached z = **+1.964**, the
  highest in the curated set. The other three anchors clustered tightly at
  z = +1.140.
- **Metric-discrimination gap (n=4):** Plausible Aquitanian and
  *deliberately-wrong* Aquitanian buckets were **statistically identical**
  on n=4 — both medians at +1.140, both with the same 3-of-4 above zero,
  1-of-4 below distribution. On this sample the metric does **not**
  distinguish "real-substrate-root in plausible context" from "the same
  root in deliberately-wrong context." This is the methodological gap the
  bulk Aquitanian sweep (mg-f832) was scoped to characterize, and that the
  next metric refinement ticket is scoped to address.
- **`control_std=0` pathology.** Two of four scramble cases
  (`scramble_HT100_E1`, `scramble_HT1_E4`) tripped a degeneracy where the
  equation has fewer than two distinct phoneme classes, all 200 random
  permutations score identically, the control std collapses to 0, and z
  is forced to 0. Generators must filter these before scoring; mg-f832's
  bulk generator implements the filter as a hard rule.
- **Scramble outlier:** `scramble_HT25a_E2` reached z = **+1.363**, above
  some plausible-Aquitanian readings. With n=4 scrambles this is one
  uncomfortable data point, not a distribution. Bulk scramble baselines
  remain to be done.
- **v0 metric limitations documented in `harness.metrics.local_fit_v0`'s
  docstring:** 2-phoneme cases yield essentially binary z values, and the
  V/S/C class collapse means /a/ and /i/ are partly conflated through the
  position-fit fingerprint.

### Findings from mg-f832 (bulk Aquitanian sweep, 2026-05-04)

- **First end-to-end bulk run.** A 153-entry Aquitanian / Proto-Basque pool
  (Trask 1997 + Gorrochategui 1984) generated **7,190** candidate equations
  against the 761-record corpus; the sweep completed in **26 seconds**
  (well inside the 15-minute budget).
- **Bulk distribution on `local_fit_v0`:** mean z = **+1.153**, median =
  **+1.308**, sd = **0.669**. **5,348 / 7,190 (74.4%)** of candidate
  equations beat z = +1.0; **11 (0.2%)** beat z = +2.0; **179 (2.5%)**
  fell below z = -1.0. The acceptance criterion (≥ 5% beat z = +1.0)
  cleared by a wide margin.
- **The metric distinguishes Aquitanian-style phoneme orderings from random
  scrambles in bulk far more decisively than the n=4 hand-curated buckets
  in mg-fb23 could measure.** The mg-fb23 metric-discrimination concern
  (plausible vs deliberately-wrong indistinguishable) needs to be re-asked
  against the bulk distribution rather than the n=4 sample — that
  re-evaluation is the post-mg-f832 metric refinement ticket.
- **Top-10 by `score_control_z`:** `sukalde` (z=+2.118 on KN Zc 7
  span [15..21], plus four other KN Zc/Zf placements above z=+2.0),
  `hil` (z=+2.033 on ARKH 5 span [6..8], plus a second ARKH 4b
  placement), and `haran` (z=+2.030 on HT Wc 3010 span [0..4]) lead the
  leaderboard. Full top-50 in `results/rollup.aquitanian.md`.
- **Skip rules baked into the bulk generator** (informed by mg-fb23 and
  the ticket spec): pool entries with < 2 distinct phoneme classes
  (`control_std=0` pathology), fragmentary inscriptions, DIV-crossing
  windows, and duplicate-sign windows are all filtered before scoring.
- **Sweep runner is resumable.** Re-running against the same corpus
  snapshot skips already-scored hypotheses (matched by hypothesis hash);
  determinism plus skip-on-resume is exercised by
  `harness/tests/test_sweep_runner.py` on a 5-record toy corpus and a
  3-entry toy pool.
- 7,190 + 20 (mg-fb23) + 4 (mg-d5ef) = **7,214 result rows total** in
  `results/experiments.jsonl` after this sweep.

### Findings from mg-7dd1 (harness v2: local_fit_v1 + geographic_genre_fit_v1, 2026-05-04)

This ticket replaced the per-hypothesis-z-normalized `local_fit_v0` with
an absolute-units `local_fit_v1` metric, added a categorical
`geographic_genre_fit_v1` cheap-test multiplier, and produced a
composite leaderboard. **The headline finding is a null:** v1 missed
three of the four discrimination acceptance bars set by the ticket.
Per the brief's "ship-the-null-rather-than-tweak-the-constants" rule,
the metric is shipped as written; v2 directions are listed below.

**v0 → v1 distribution shift (7,190 Aquitanian candidates).**

| stat                        | v0 (`score_control_z`) | v1 (`score`)        |
|-----------------------------|-----------------------:|--------------------:|
| mean                        | +1.1534                | -2.6633             |
| median                      | +1.3078                | -2.6632             |
| std                         | 0.6694                 | 0.2995              |
| range                       | [-1.97, +2.12] (4.09)  | [-3.78, -1.86] (1.92) |
| top-1% mean                 | +1.9661                | -1.9586             |
| top-1% mean − median        | +0.658                 | +0.705              |
| max 0.5-wide window count   | 3,298 / 7,190 (45.9%)  | 4,224 / 7,190 (58.7%) |
| max bucket (10-bucket histogram) | n/a               | 1,695 / 7,190 (23.6%) |
| n at top of mass            | 5,348 (74.4%) z>+1     | 57 (0.8%) score>-2.05 |

The v1 distribution is **narrower in absolute units than v0's z**, so the
"top-1% beats the median by ≥ 2.0 v1-units" bar can't be hit (the entire
range is only 1.92 v1-units wide). The "≤ 25% in any 0.5-wide band" bar
is also missed; v1 is more concentrated in absolute units because
length-normalization removed the longest-equation tail and rare-sign
correction trimmed the bottom. This is a structural property of the
formulation, not tweakable noise.

**Length artifact reversal.** mg-f832's v0 top-50 was dominated by
3-sign equations (34/50 = 68%) — the predicted "longest sums of
log-probs are most negative" artifact. v1 top-50 is dominated by
5-sign equations (49/50 = 98%); the length penalty did its job, but
the swap from "shortest dominates" to "exactly 5 dominates" suggests
the per-unit-length tradeoff between the position term and the length
penalty is too sharp at C=1.0. A future v2 might explore length-aware
**per-pair** position discounting rather than a flat 1/n term.

**Discrimination acceptance bars (4 total, 1 PASS / 3 FAIL).**

| Bar | Description | Required | Observed | Status |
|---|---|---:|---:|:---:|
| 1 | Linear-B-anchor median > random-scramble median (n=4 each) | strictly > | -4.5433 vs -4.6693, diff +0.13 | ✅ PASS |
| 2a | top-1% mean − median ≥ 2.0 v1-units (bulk n=7,190) | ≥ 2.0 | +0.7046 | ❌ FAIL |
| 2b | ≤ 25% of bulk candidates in any 0.5-wide score band | ≤ 25% | 58.7% | ❌ FAIL |
| 3 | plausible-Aquitanian median − wrong-Aquitanian median (n=4 each) | ≥ 1.0 v1-unit | +0.1408 | ❌ FAIL |

The v1 metric IS more discriminative than v0 in spirit (cross-hypothesis
absolute scores instead of per-hypothesis z-collapse, empirical bigram
prior trained on the active pool's own surfaces, length-normalized,
rare-sign-corrected), but **does not separate plausible from
deliberately-wrong Aquitanian readings on the n=4 hand-curated
buckets** — the same gap mg-fb23 found in v0. v1 *also* failed to
spread the bulk distribution wide enough to satisfy bars 2a and 2b. The
"absolute-units score" design target was met; the "discriminative
absolute-units score" target was not.

**Why the bigram_term contributes near-zero discrimination.** The
empirical bigram model is trained on the same pool surfaces that the
hypotheses are drawn from, so within one pool entry's ~47 bulk
candidates the bigram_term is identical (same phoneme sequence). The
bigram term distinguishes between *pool entries* (different surfaces),
not between candidates of the same surface. The position term carries
all the within-surface signal, and the position term's range at the
mean-per-pair scale is ~[-0.5, 0]. v2 should consider a held-out
phoneme model (leave-one-out over pool entries) or a corpus-side
phoneme prior built from a non-substrate source.

**`geographic_genre_fit_v1` distribution (7,190 bulk candidates).**

mean=+0.4518, median=+0.4000, std=0.108, range=[0.250, 0.700].
The score is a structural categorical compat in [0, 1]; the histogram
is multi-modal (delta-spikes at 0.25, 0.40, 0.55, 0.70) reflecting the
small lookup tables. Aquitanian/basque_substrate × any Linear-A site is
fixed at 0.25 (region_compat); semantic_field × accountancy carries the
discriminating signal at 0.25 / 0.50 / 0.75 / 1.00. With α=0.4 default,
the four observed score points are 0.4*0.25 + 0.6*{0.25, 0.50, 0.75,
1.0} = {0.25, 0.40, 0.55, 0.70}. As designed, this is a coarse
multiplier, not a fine-grained metric.

**Composite leaderboard top-10 diversity** (0.7 *
`local_fit_v1`(z) + 0.3 * `geographic_genre_fit_v1`(z)):

- 10 / 10 distinct (root, inscription) pairings
- 4 distinct sites: Haghia Triada × 5, Knossos × 2, Arkhanes × 2, Gournia × 1
- 2 semantic fields: number × 4, nature × 6
- 3 genre hints: accountancy × 7, unknown × 2, votive_or_inscription × 1

Surface forms in the top-10: `harri` (rock; nature) and `hamar`
(ten; number) — the latter benefits heavily from the
semantic_field=number × genre_hint=accountancy lookup table entry
(1.0). The composite IS structurally orthogonal to the pure-`local_fit_v1`
top-50 (which is 49/50 5-sign equations all sharing surface
`harri`-or-similar): the geographic compat lifts shorter
number-field roots back into contention.

Full top-50 in `results/rollup.aquitanian.composite.md`.

**Null-finding section: what v1 did not improve.**

- The plausible-vs-deliberately-wrong-Aquitanian gap (mg-fb23's open
  question). v0 had identical medians; v1 has +0.14 v1-units of
  separation, far short of the +1.0 target. The metric still cannot
  distinguish "real-substrate-root in plausible context" from "the same
  root in deliberately-wrong context" on n=4 curated buckets.
- The bulk distribution flatness target. v1's range is bounded by
  the position-term's mean-per-pair scale, which is small. A wider
  spread would require either a more discriminative per-pair signal
  (e.g., per-phoneme position profile fitted to a held-out corpus
  rather than the same one we score against) or a complementary signal
  altogether.
- The "absolute scores cleanly compare across pool entries" target —
  partially met. Cross-entry comparisons are now meaningful, but the
  cross-entry variance is dominated by length effects (top-50 is 98%
  5-sign equations).

**Proposed v2 directions.**

- *Held-out empirical bigram*: leave-one-out over pool entries when
  scoring, so the bigram term is not zero-information for the surface
  being tested.
- *Per-pair length normalization*: replace flat 1/n length penalty
  with a per-pair correction that doesn't favor a single sweet-spot
  length. Worth exploring whether `score / sqrt(n)` produces a flatter
  length distribution at the top of the leaderboard.
- *Cross-corpus position prior*: build the expected-position
  distribution for each phoneme from an independent corpus
  (Linear-B / GORILA Younger), so the position-fit signal stops being
  partly circular (currently both fingerprint and prior come from the
  same Linear-A corpus).
- *Per-inscription scoring weight*: many top-10 entries land on
  Haghia Triada simply because HT dominates the corpus (372 / 761).
  An "inscription difficulty"-aware scoring would let small-corpus
  sites contribute proportionally.
- *Multi-pool composite*: once Etruscan / Pre-Greek pools land, the
  geographic_genre_fit_v1 metric will become more discriminative
  (region_compat=1.0 for pre_greek × Crete vs 0.25 for aquitania ×
  Crete is a real signal that's currently not exercised).

**Operational artifacts.**

- 7,190 × 2 + 20 × 2 = **14,420 new result rows** appended to
  `results/experiments.jsonl` under the v1 metrics. Total stream:
  21,634 rows.
- `results/rollup.aquitanian.composite.md` committed with the top-50
  composite leaderboard (z-normalized 0.7/0.3 weighted).
- `harness/tests/test_local_fit_v1.py` and
  `harness/tests/test_geographic_genre_fit.py` exercise both metrics
  on toy corpora; existing 16 tests still pass.
- `HARNESS_VERSION` bumped from `v0` to `v1`. Sweep-runner resume key
  bumped from `(hash, snapshot)` to `(hash, snapshot, metric)` so the
  same hypothesis can hold one row per metric.
- `--metrics m1,m2 --weights w1,w2 --normalize zscore` flags added to
  `scripts/rollup.py` for the composite leaderboard.

## Known metric limitations

- **`local_fit_v1` did not solve the plausible-vs-wrong discrimination
  problem and produced a narrower bulk distribution than the
  acceptance bars require.** See mg-7dd1 for the v0 → v1 diagnostic and
  proposed v2 directions. The v0 limitations below remain on record
  because v0 rows are still in the result stream and v0's behavior is
  the baseline against which v2 will be measured.
- **`local_fit_v0` plausible-vs-wrong discrimination is the most important
  open methodological question.** The n=4 mg-fb23 buckets showed the metric
  separating real readings from random nonsense (anchor median +1.14 vs
  scramble median 0.00) but **not** separating plausible-context Aquitanian
  from deliberately-wrong-context Aquitanian (both +1.14). The mg-f832 bulk
  distribution (median +1.31, 74.4% above z=+1) suggests the metric is
  picking up on phoneme-class arrangement plausibility broadly, regardless
  of whether the inscription context is a sensible candidate for that root.
  Until the metric refinement ticket addresses this, a high `local_fit_v0`
  z is evidence of "this phoneme arrangement is bigram-plausible and
  position-consistent," not evidence of "this is what the inscription
  says." Treat the leaderboard accordingly.
- **`control_std=0` pathology on equations with < 2 distinct phoneme
  classes.** All 200 permutations of a single-class alignment score
  identically, the standardization collapses, and z is forced to 0. This
  is a generation-time requirement, not a metric fix: bulk generators must
  filter pre-scoring (mg-f832 does).
- **2-phoneme equations yield essentially binary z values.** The same
  control-permutation degeneracy means very short equations have only a
  handful of distinguishable permutation outcomes; their z values cluster
  on a small set of points rather than smoothly distributing.
- **V/S/C class collapse partly conflates /a/ and /i/.** The position-fit
  fingerprint and the phonotactic prior both operate at phoneme-class
  granularity in v0, so two vowels sharing a class are not separated by
  the metric. This is documented in the metric's docstring.
- **No second-corpus cross-validation yet.** All scores are against the
  761-record SigLA snapshot; no Younger / GORILA cross-check has been run.
  A leaderboard high z that does not survive a second corpus is a different
  failure mode than one that does.

## Current best hypotheses

*Preliminary — see "Known metric limitations" above for caveats. A high z
on `local_fit_v0` is necessary but probably not sufficient evidence; the
geographic-vs-genre filter and metric refinement are scoped follow-ups.*

- **Linear-B carryover anchors** (`hypotheses/curated/anchor_*.yaml`): all
  four scored z ≥ +1.140 on `local_fit_v0` (mg-fb23). `anchor_taina_HT39`
  reached z = +1.964. These are the strongest in-corpus reading anchors
  drawn from a known-related script.
- **Bulk Aquitanian leaders** (mg-f832, top-10 by `score_control_z`): the
  surfaces `sukalde` (Trask 1997, "kitchen / hearth"), `hil` ("dead, kill"),
  and `haran` lead at z > +2.0. `sukalde` placements concentrate on
  Knossos Zc/Zf inscriptions; `hil` on ARKH 4b/5; `haran` on HT Wc 3010.
  Full leaderboard in `results/rollup.aquitanian.md`.

## What we have NOT yet tried

- **`local_fit_v2`.** A v2 of the local-fit metric is needed; v1
  (mg-7dd1) shipped as a null finding on three of four discrimination
  bars. Proposed directions in mg-7dd1's findings entry: held-out
  empirical bigram, per-pair length normalization, cross-corpus
  position prior, multi-pool composite. Queued.
- **Etruscan pool ingest.** Same schema as Aquitanian, mechanical follow-on.
- **Pre-Greek toponym pool ingest.** Substrate-style data with natural fit
  to the geographic-vs-genre filter.
- **Younger / GORILA cross-validation pull.** Second corpus for
  cross-checking high-z candidates.
- **Additional metrics:** mutual information of (sign, position-in-word)
  under a proposed phoneme; perplexity under a learned Basque / Etruscan
  prior; MDL proxies. Second-iteration metric ensemble.
- **Numerals.** SigLA does not encode them; would require a GORILA
  ingest. Some commodity-record tablets will continue to read sparser
  than they actually are until this lands.
- **Line-break recovery.** SVG coordinates are in the cached HTML; a
  y-coordinate clustering pass would emit `BREAK` tokens. Schema already
  permits them.
