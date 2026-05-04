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
    and `semantic_compat` persisted on each row. mg-23cc extended
    the region-compat table to recognize `etruria` as the geographic
    tag for the Etruscan pool (parallel with `aquitania`).
  - `partial_mapping_compression_delta_v0` (mg-23cc) — corpus-side
    third axis. Wraps `compression_delta_v0`: takes a candidate
    equation's `sign_to_phoneme` dict, treats it as a partial global
    mapping, and computes `baseline_bits − mapped_bits` over the
    full corpus stream. Within a single Aquitanian surface (~47
    candidates that share a root), local_fit_v1's bigram term is
    identical, so this axis is the only within-surface
    discriminator. Distribution sd ≈ 110 bits, range ~900 bits;
    within-surface SDs of 50-100 bits across all surfaces with
    ≥30 candidates. Diagnostic terms `bits_per_sign_baseline` and
    `bits_per_sign_mapped` persisted on each row.
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

### Findings from mg-23cc (harness v3: partial_mapping_compression_delta_v0 + Etruscan pool + triple-axis composite, 2026-05-04)

This ticket added a **third, structurally orthogonal scoring axis** —
`partial_mapping_compression_delta_v0`, a corpus-side metric — and a
**second substrate pool** (Etruscan, 143 entries from Bonfante &
Bonfante 2002 / Pallottino TLE / ETP), then ran every Aquitanian +
Etruscan candidate under all three v1 metrics for a triple-axis
composite leaderboard. The headline finding is **mixed**: the metric
*massively* passes the within-surface discrimination test (the central
question for this ticket — see below), but **fails** the n=4 plausible-
vs-deliberately-wrong Aquitanian curated gate, the same gate v0 and v1
of the local-fit metric also missed.

**`partial_mapping_compression_delta_v0` distribution (12,210
candidates: 7,190 Aquitanian + 5,966 Etruscan + 20 curated).**

| stat | aquitanian (n=7,190) | etruscan (n=5,966) | combined bulk (n=13,156) |
|---|---:|---:|---:|
| mean         | -90.85   | -106.10   | -97.77   |
| median       | -96.00   | -112.00   | -104.00  |
| sd           | 109.85   | 111.16    | 110.71   |
| min          | -424.00  | -472.00   | -472.00  |
| max          | +448.00  | +336.00   | +448.00  |
| top-1% mean  | +258.33  | +235.07   | +248.49  |
| top-1% mean − median | +354.33 | +347.07 | +352.49 |

The score is in raw bits (`baseline_bits − mapped_bits`). The
distribution is **wide** (sd ~110 bits, range ~900 bits) and the top-1%
mean clears the median by ~352 bits — a genuinely heavy-tailed signal
that responds non-trivially to the partial mapping. Most candidates
score negative (the partial mapping makes things slightly worse —
expected, since most candidate equations cover signs that occur few
times); the discriminating signal is the small fraction whose mapping
covers high-frequency signs in the corpus.

**Within-surface discrimination test (the central question for this
ticket).** Within a single Aquitanian surface (~47 candidates that
share the same root), local_fit_v1's bigram term is identical, so
within-surface discrimination must come from corpus-side. The mg-7dd1
diagnosis predicted this would be the bottleneck. We tested it:

| surface (Aquitanian) | n | sd of pmcd | range | min..max |
|---|---:|---:|---:|---:|
| ur                | 50 | 55.47  | 256  | -168..+88 |
| sukalde           | 13 | 50.07  | 168  | -360..-192 |
| hil               | 50 | 69.13  | 232  | -176..+56 |
| haran             | 50 | 81.52  | 408  | -240..+168 |
| etxe              | 50 | 82.74  | 376  | -64..+312 |
| sembe             | 50 | 94.75  | 464  | (table) |
| seni              | 50 | 76.04  | 376  | (table) |
| atta              | 50 | 97.45  | 360  | (table) |
| larre             | 50 | 70.49  | 320  | (table) |
| hanna             | 50 | 94.68  | 480  | (table) |

**Acceptance gate: SD > 5 bits ⇒ metric is doing within-surface work.**
**All 20 Aquitanian surfaces with ≥30 candidates clear it; SDs run
50–100 bits, ~10–20× the threshold. Within-surface discrimination is
the strongest behavior of this metric. The corpus-side signal mg-7dd1
predicted is real and large.**

**Discrimination gate on n=4 plausible vs n=4 wrong Aquitanian
(mg-fb23).** The acceptance criterion required plausible median −
wrong median ≥ +5 bits. **FAIL.**

| bucket | scores | median |
|---|---|---:|
| plausible | -96, -56, -24, +72 | -40 |
| wrong (deliberate) | -32, -24, -16, +40 | -20 |

Plausible − wrong = **−20 bits** (wrong scores HIGHER than plausible on
the median). The corpus-side metric **also** does not separate
plausible-context Aquitanian readings from deliberately-wrong-context
on the n=4 hand-curated buckets, even though it produces a strong
within-surface spread on the bulk distribution. Per the ticket's
"ship-the-null" rule, the metric is shipped as written; the
implication is that *neither* the local-fit signals (v0/v1) *nor* the
corpus-side compression signal carry the within-surface
plausibility-vs-misplacement information the curated bucket targets.
The discrimination signal these metrics carry is real (within-surface
SDs of 50-100 bits are not noise) but the *direction* of variation
isn't aligned with "plausible context yes/no" on n=4. Whether n=4 is
just too small to detect a small true effect is an open question;
n=20+ curated buckets would be needed to address it.

**Cross-pool distribution shapes.**

| metric | aquitanian | etruscan |
|---|---:|---:|
| local_fit_v1 mean / sd          | -2.663 / 0.299 | -2.744 / 0.213 |
| local_fit_v1 range              | [-3.78, -1.86] | [-3.73, -2.24] |
| pmcd mean / sd                  | -90.85 / 109.85 | -106.10 / 111.16 |
| geographic_genre_fit_v1 mean    | +0.452          | +0.574          |
| geographic_genre_fit_v1 sd      | 0.108           | 0.107           |
| geographic_genre_fit_v1 range   | [0.25, 0.70]    | [0.35, 0.80]    |

The geographic compat score *is* doing what the polecat-recommended v2
direction predicted: **Etruscan candidates score systematically higher
on geographic_genre_fit_v1 (+0.574 mean vs +0.452 for Aquitanian),
because etruria × Cretan-site = 0.5 vs aquitania × Cretan-site = 0.25
in the lookup table. The filter is no longer pinned at a single value
on every Aquitanian-only candidate — it now exercises both rows of
the table.**

The pmcd distribution is similarly-shaped across both pools (sd ~110,
heavy negative tail with a positive top-1%) — pleasing, because it
suggests the corpus-side metric is *not* pool-dependent. local_fit_v1
is narrower on Etruscan (sd 0.213 vs 0.299), which is consistent with
the empirical bigram model being trained on Etruscan's smaller pool
(143 entries vs 153) and tighter phoneme inventory (no /o/, more
aspirate digraphs).

**Top-10 composite_v3 review (0.4 local_fit_v1 + 0.3 pmcd + 0.3
geographic_genre_fit, all z-normalized over the joined 13,156-row
result set).**

| rank | composite | pool | surface | inscription | site | genre |
|---:|---:|---|---|---|---|---|
| 1  | +1.74 | aquitanian | hamar  | HT Wc 3017a | Haghia Triada  | accountancy |
| 2  | +1.61 | aquitanian | hanna  | KN Zc 6     | Knossos        | votive_or_inscription |
| 3  | +1.61 | etruscan   | ana    | ARKH 2      | Arkhanes       | accountancy |
| 4  | +1.56 | aquitanian | bere   | HT 128a     | Haghia Triada  | accountancy |
| 5  | +1.54 | aquitanian | bi     | ARKH 5      | Arkhanes       | accountancy |
| 6  | +1.52 | aquitanian | bi     | ARKH 3b     | Arkhanes       | accountancy |
| 7  | +1.52 | aquitanian | ere    | ARKH 2      | Arkhanes       | accountancy |
| 8  | +1.51 | aquitanian | hamar  | HT 110a     | Haghia Triada  | accountancy |
| 9  | +1.47 | aquitanian | senben | KN Zc 6     | Knossos        | votive_or_inscription |
| 10 | +1.45 | aquitanian | bere   | HT 12       | Haghia Triada  | accountancy |

- **7 distinct surfaces** in the top 10 (hamar×2, hanna, ana, bere×2,
  bi×2, ere, senben). The composite is **noticeably more diverse than
  mg-7dd1's local_fit_v1 top-50 (49/50 = 98% one surface "harri")** —
  the addition of pmcd as a third axis breaks single-surface
  domination by rewarding partial mappings whose signs happen to be
  high-frequency, regardless of the surface they came from.
- **4 distinct sites** (Haghia Triada × 4, Arkhanes × 4, Knossos × 2).
  Less site-skew than the v2 composite (which was 7×HT, 2×KN, 2×ARKH,
  1×GO).
- **2 genres** (accountancy × 8, votive_or_inscription × 2). The two
  votive entries land on KN Zc 6, the same Knossos votive inscription
  that drove much of mg-f832/mg-7dd1's leader-board action — the
  signal is durable across metric rotations.
- **Pool diversity: 9/10 Aquitanian, 1/10 Etruscan.** Etruscan only
  reaches the top with `ana` (ritual/votive name suffix; +1.61). In
  the top-50, Aquitanian is 34/50, Etruscan 16/50 — Etruscan competes
  but does not dominate. The deficit is on local_fit_v1: Etruscan's
  narrower distribution (sd 0.213) means even its best candidates
  score lower in z-units than Aquitanian's best.
- **Length artifact reset.** The mg-7dd1 v1 leaderboard was 49/50
  five-sign equations (the length penalty's sweet spot). The v3
  composite top-50 is more length-mixed because the pmcd term rewards
  high-frequency sign coverage, which often comes from 2–3 sign
  equations on common signs. Bi (2 phonemes) gets 11/50 entries;
  hamar (5 phonemes) gets 7/50.

**Etruscan pool-quality observation.** Per the policy of surfacing
real-world biases as findings: the Etruscan pool is **strongly
biased toward religious / funerary / kin vocabulary** (143 entries:
36 religion, 39 function, 26 kin, 14 number, 12 time, 8 place, 4
commodity, 2 animal, 1 dwelling, 1 descriptor). This is not a pool
defect — it reflects what's preserved in the Etruscan corpus
(funerary urns, sarcophagi, Liber Linteus, Tabula Capuana). The
consequence for scoring: most Etruscan candidates score
geographic_genre_fit_v1 = 0.5 (religion × accountancy = 0.25 plus
α=0.4 region weight) or 0.65 (kin × accountancy = 0.5), versus
Aquitanian's 0.4 (kin × accountancy = 0.5 with aquitania × Crete =
0.25). The bias means **Etruscan systematically outperforms
Aquitanian on the geographic axis but underperforms on local_fit_v1
under the same composite weights** — which the leaderboard reflects.

**What worked.**
- The corpus-side metric **does** discriminate within-surface, with
  SDs 50-100 bits across all 20 surfaces with ≥30 candidates. The
  central diagnosis from mg-7dd1 — that within-surface
  discrimination must come from corpus-side — was directionally
  correct. The metric is doing the work.
- Multi-pool data exercises geographic_genre_fit_v1 properly. The
  filter now produces meaningful pool-level differences (+0.452 vs
  +0.574) where mg-7dd1's single-pool run had it pinned at one row.
- The triple-axis composite leaderboard breaks the
  single-surface-dominance pathology mg-7dd1 reported (49/50 same
  surface → 11/50 maximum in v3, 7 surfaces represented in top-10).
- 5,966 Etruscan candidates emitted from 143 pool entries (within
  the 1,000-10,000 acceptance window). Generator filter rejected 0
  single-class entries; capped 106 entries at 50 candidates each.
- Determinism preserved end-to-end: re-running the sweep is a no-op
  via the resume key.

**What did not work / null findings.**
- **The plausible-vs-deliberately-wrong gate failed for the third
  metric in a row.** v0 (mg-fb23): identical medians. v1 (mg-7dd1):
  +0.14. v3 pmcd (this ticket): -20 bits (plausible *lower* than
  wrong). The n=4 hand-curated bucket is repeatedly indistinguishable
  under three structurally different metrics; either (a) the metrics
  collectively miss the plausibility signal, or (b) n=4 is too small
  to detect what's actually there. Future v4 work needs to expand
  the curated bucket before chasing more metric variants.
- **Etruscan does not dominate the leaderboard despite the geographic
  filter favoring it.** The local_fit_v1 narrowness on Etruscan
  cancels the geographic advantage when the composite weights are
  even (0.4/0.3/0.3); a heavier pmcd weight or geographic weight
  would change this — but tuning weights to make Etruscan win is
  exactly the motivated-reasoning failure mode the harness was built
  to avoid.

**Operational artifacts.**
- 7,190 Aquitanian × 1 new metric = **7,190 new pmcd rows**.
- 5,966 Etruscan candidates × 3 metrics = **17,898 new Etruscan rows**
  (local_fit_v1 + pmcd + geographic_genre_fit_v1).
- 20 curated × 1 new metric = **20 new pmcd rows** on the curated
  hypotheses (rescore for completeness).
- Total stream after merge: **46,742 rows**, up from 21,634 at
  mg-7dd1 merge.
- Three new committed leaderboards: `results/rollup.composite_v3.md`
  (top-50 across both pools), `results/rollup.aquitanian.composite_v3.md`
  (top-50 Aquitanian only), `results/rollup.etruscan.composite_v3.md`
  (top-50 Etruscan only).
- `pools/etruscan.yaml` (143 entries) + `pools/etruscan.README.md`
  (phonology + bias caveats) committed.
- `harness/tests/test_partial_mapping_compression_delta.py` (7 tests)
  committed and passing alongside the existing 30 tests.
- `harness/metrics._GG1_REGION_COMPAT` extended with `etruria` rows
  (parallel with `aquitania` for the Aquitanian pool — the
  geographic-tag convention).
- `scripts/rollup.py` extended with `--by source-pool` for the
  composite path; `_render_composite` factored through a per-table
  helper so the same function renders both global and per-pool views.
- `scripts/generate_candidates.py` slugs the surface for the
  hypothesis name (Etruscan śuthina contains a non-ASCII character;
  the schema's name pattern is ASCII-only). Aquitanian regenerates
  byte-identically (no surface-character changes there).

**Proposed v4 directions** (deferred; filing intentionally not done
in this ticket per scope-of-work norm).
- Expand the plausible-vs-wrong curated bucket from n=4 to n=20+
  before re-attempting the discrimination gate; three different
  metrics have now missed it on n=4.
- **Pre-Greek toponym pool** as a third pool — the polecat's
  remaining v2 multi-pool direction. region_compat = 1.0 for
  pre_greek × Crete; the geographic axis would carry an even
  stronger pool-level signal.
- **Held-out empirical bigram** (leave-one-out over pool entries)
  remains queued; this ticket added a corpus-side axis instead, but
  the held-out bigram is independently worth running.
- **Cross-corpus position prior**: the position fingerprints are
  still computed on the same Linear-A corpus the metric scores
  against, which is partly circular. A Linear-B reference corpus
  for fingerprinting would break the circularity.
- **Publication-trigger thresholding**: the v3 composite distribution
  is the first one that's heavy-tailed enough to consider thresholding
  against (top-1% mean − median ~ 352 bits on pmcd). Defer to a
  separate ticket.

### Findings from mg-7c8c (curated v4: n=20 buckets + n=4-or-bad-metric resolution, 2026-05-04)

This ticket grew each of the five curated buckets from n=4 to n=20
(80 new hand-systematic hypotheses + a 35-entry pre-Greek toponym
pool) and re-ran all three v3 metrics, with a Mann-Whitney U test +
power-calculation sanity check. **The headline finding is the
methodology answer to the question that motivated v4: the n=4 buckets
were not the bottleneck — the metrics genuinely do not discriminate
within-surface plausibility-of-context, and at the observed effect
sizes even n=50–100 would not rescue them.**

The full statistics report is in `results/statistics_v4.md`. The key
rows:

**Plausible-vs-wrong-Aquitanian (B vs C; n=20 each).** Mann-Whitney U,
two-sided, with mid-rank ties:

| metric | Δ_medians | Cliff's δ | U_a | z | p | detectable Δ at n=20 | underpowered? |
|---|---:|---:|---:|---:|---:|---:|:---:|
| `local_fit_v1`                          | -0.0242 | +0.040 | 208 | +0.20 | **0.84** | 0.262 | yes |
| `partial_mapping_compression_delta_v0`  | +48 bits | +0.120 | 224 | +0.64 | **0.52** | 75.4 bits | yes |
| `geographic_genre_fit_v1`               | +0.30 | +0.960 | 392 | +5.45 | **<0.0001** | 0.075 | no |

`local_fit_v1` and `partial_mapping_compression_delta_v0` again **fail
the gate** (p > 0.05, Cliff's δ ≈ 0). The observed effect sizes are
*tiny in absolute units* (-0.024 v1-units; +48 bits) — at the observed
within-bucket SDs (0.295 and 85 respectively) the comparison is
underpowered for the observed effect even at n=20. To detect those
specific effect sizes at α=0.05, β=0.20 would need:
- `local_fit_v1`: **n* ≈ 2,400 per bucket** (effect is dominated by
  noise; nothing realistic will rescue it).
- `partial_mapping_compression_delta_v0`: **n* ≈ 50 per bucket**
  (n=50 might surface it, n=20 is on the wrong side of the threshold).

`geographic_genre_fit_v1` separates the buckets with massive effect —
**but tautologically.** Bucket C was *defined* by genre-incompat
(semantic_compat ≤ 0.25 by construction). The metric is reading the
construction rule, not an emergent signal. This is a methodological
caveat and is documented in `hypotheses/curated/CONSTRUCTION.md`.

**Bottom-line answer to the n=4-or-bad-metric question.** Per the
ticket brief's three options: **option (b)** — *"all three have p>0.05
even at n=20, and the metric collectively does not capture
within-surface plausibility-of-context"* — is the closest match, with
the qualifier that the comparisons are also underpowered at n=20 for
the observed effect sizes. The two non-tautological metrics
(`local_fit_v1` and `partial_mapping_compression_delta_v0`) carry **no
detectable plausible-vs-wrong-Aquitanian signal at n=20.** The
geographic axis separates the buckets but does so by reading the
construction rule.

So **n=4 was *not* the bottleneck**: even at n=20, neither metric's
effect size is large enough that further bucket expansion (n=50,
n=100) would produce a clean discrimination — the
`local_fit_v1` effect is well below the noise floor at any realistic
n, and `partial_mapping_compression_delta_v0`'s effect is on the
wrong side of the n=50 threshold. The next move is fundamentally
different from "another bucket expansion": the metrics need a
structural change. Candidate directions are listed below.

**Anchor-vs-scramble sanity check (A vs E; n=20 each).** Verifies
mg-fb23's n=4 gate (anchor median > scramble median) survives at
larger n.

| metric | Δ_medians | Cliff's δ | p | detectable Δ |
|---|---:|---:|---:|---:|
| `local_fit_v1`                          | -0.317 | -0.425 | **0.022** | 0.214 |
| `partial_mapping_compression_delta_v0`  | +48 bits | +0.330 | 0.076    | 73.0 bits |
| `geographic_genre_fit_v1`               | 0.000  | 0.000  | 1.000    | 0.000 |

`local_fit_v1` actually shows anchors **lower than scrambles**
(direction-flipped from the mg-fb23 z-score-based result). Why: the
empirical bigram model in `local_fit_v1` is built from the active
pool's surfaces — for these curated entries the runner falls back to
`pools/aquitanian.yaml` (per the runner's source-pool inference
rule). Linear-B carryover surfaces (`kupa`, `mate`, `kira`) and random
IPA scrambles (`q`, `ʁ`, ...) are *both* off-distribution under the
Aquitanian bigram, but anchors hit additional rare-sign correction
penalties on their sign sets (some anchors pin to AB04, AB05, etc.
which appear < 5 times in the bigram model's vocabulary; the v1 metric
penalizes that). Random scramble surfaces are off-distribution but
shorter and don't trigger the rare-sign correction as often. The
direction flip is a **metric artifact** of the off-pool scoring path,
not a substrate finding.

`partial_mapping_compression_delta_v0` is the relevant axis here, and
it shows a marginal positive effect (Cliff δ=+0.33, p=0.076) —
suggestive but not significant. The more meaningful question (does
the corpus-side metric distinguish anchors from random IPA?) is mostly
clarified by the +48 bit median difference, but the within-bucket SD
on this metric is high enough (~57-101 bits depending on bucket) that
the test is underpowered even at n=20.

`geographic_genre_fit_v1` is uniformly 0.5 for both buckets because
neither anchor surfaces (`kupa`/`mate`/etc.) nor scramble surfaces
(random IPA) appear in any pool's `by_surface` lookup, so the metric
falls back to the neutral 0.5/0.5 default for both inputs. This is
the documented "Missing or empty fields → neutral 0.5" behavior of
the metric (`harness.metrics._lookup_compat`).

**Toponym-vs-scramble (D vs E; n=20 each).** Tests whether the
new third pool carries any independent discriminative signal.

| metric | Δ_medians | Cliff's δ | p | detectable Δ |
|---|---:|---:|---:|---:|
| `local_fit_v1`                          | +1.014 | +0.780 | **<0.0001** | 0.404 |
| `partial_mapping_compression_delta_v0`  | +96 bits | +0.552 | **0.003** | 75.4 bits |
| `geographic_genre_fit_v1`               | 0.000 | 0.000 | 1.000 | 0.000 |

Toponym candidates **strongly separate from scrambles** on both
non-tautological metrics — both effects are large (Cliff δ > 0.5,
"large effect" in Cliff 1993) and detectable at n=20. So the
metrics ARE capable of separating real-substrate-style readings
from random IPA at this sample size; the failure mode is
specifically "plausible-vs-wrong on the SAME pool's surfaces."

The geographic axis is again 0.5/0.5 for both buckets because the
toponym candidates' surfaces are *fragments* of full toponyms (e.g.
`kno` from `knossos`), not pool entries, so the surface lookup
misses. To exercise `geographic_genre_fit_v1` properly on the
toponym bucket, future work should either (a) add the fragments as
their own pool entries with `region: pre_greek`, or (b) extend the
runner's pool-context lookup to read region/semantic_field from the
candidate's `source_pool` rather than the surface.

**Plausible-Aquitanian-vs-anchor (B vs A; n=20 each).** A control
sanity check — both buckets are "plausible" in their own pool's
sense; metrics should not separate them strongly.

| metric | Δ_medians | Cliff's δ | p |
|---|---:|---:|---:|
| `local_fit_v1`                          | +1.746 | **+1.000** | <0.0001 |
| `partial_mapping_compression_delta_v0`  | +24 bits | +0.085 | 0.66 |
| `geographic_genre_fit_v1`               | +0.05 | +0.750 | <0.0001 |

`local_fit_v1` separates them with **perfect Cliff δ = +1.0** —
every Aquitanian-plausible candidate scores above every anchor.
This is the off-pool-bigram artifact noted above: anchor surfaces
under the Aquitanian bigram model are uniformly worse than
Aquitanian-pool surfaces. **This is a confound for any
cross-pool analysis under `local_fit_v1`.** Cross-pool
comparisons need either pool-specific bigram models or a
pool-agnostic phoneme prior (the held-out bigram or cross-corpus
prior already queued under "Proposed v2 directions" in the mg-7dd1
section).

**Distribution shapes (n=20 each, by bucket).**

| metric | A_anchor | B_aquit_plausible | C_aquit_wrong | D_toponym | E_scramble |
|---|---|---|---|---|---|
| `local_fit_v1` median (sd)              | -4.49 (0.13) | -2.74 (0.29) | -2.72 (0.30) | -3.16 (0.56) | -4.17 (0.32) |
| `pmcd` median (sd)                      | -80 (57) | -56 (92) | -104 (77) | -32 (65) | -128 (102) |
| `geographic_genre_fit_v1` median (sd)   | 0.50 (0.00) | 0.55 (0.08) | 0.25 (0.09) | 0.50 (0.00) | 0.50 (0.00) |

The `pmcd` distribution is consistent with mg-23cc's bulk
characterization (sd ≈ 90-110 bits within-pool); the curated buckets
show similar within-bucket spread. The geographic-axis bucket SDs are
0 except for B and C (the only buckets whose surfaces hit the pool
lookup) — D, A, E all fall back to 0.5.

**What worked.**
- Bucket construction is reproducible: the build script
  (`scripts/build_curated_v4.py`) runs in <1s and emits 80 YAMLs
  byte-identically across re-runs. RNG seed=4242 frozen for the
  scramble bucket. CONSTRUCTION.md documents the rules.
- Pool ingest: `pools/toponym.yaml` (35 entries, Beekes 2010 /
  Furnée 1972) clears the ≥30 acceptance bar.
- Sweep is resumable end-to-end. 240 new rows appended to
  `results/experiments.jsonl` (80 new × 3 metrics); existing 60
  rows for the 20 original curated entries are preserved (per the
  append-only rule).
- Statistics implementation is self-contained — no scipy
  dependency. `scripts/curated_v4_stats.py` produces a markdown
  report with U statistics, p-values, Cliff's δ, and per-comparison
  power calculations.
- The toponym-vs-scramble test confirms the metrics CAN separate
  real-substrate-style readings from random IPA at n=20 — the
  problem really is specifically the within-surface
  plausibility-of-context signal, not "the metrics work at all."

**What did not work / null findings.**
- **Plausible-vs-wrong-Aquitanian remains the open methodological
  question.** Three metrics × two sample sizes (n=4 and n=20) all
  miss the gate on the non-tautological metrics. The
  `local_fit_v1` effect is below the noise floor at any realistic
  n (≈2,400/bucket needed); `pmcd` would need ≈ n=50/bucket. The
  geographic axis "separates" them with massive effect, but
  tautologically (the bucket-construction rule is embedded in the
  metric's lookup table).
- The `geographic_genre_fit_v1` axis on D and A buckets is uniformly
  0.5 because the curated surfaces don't hit any pool's
  `by_surface` lookup. The metric fall-back is documented but
  surfaces a real limitation: candidate-fragment surfaces, anchor
  surfaces, and scramble surfaces all bypass the geographic table.
  A v2 of the metric (or runner) should look up region/semantic_field
  from the candidate's `source_pool` rather than the surface.
- The local_fit_v1 anchor < scramble direction flip is real and
  driven by the off-pool bigram artifact. Cross-pool
  `local_fit_v1` comparisons need pool-specific bigram models.

**Bottom-line operator takeaways.**
- The next ticket should NOT be "n=50 expansion." The power
  calculation says that wouldn't fix it.
- The next ticket should be a *structural* metric change. Candidates,
  in priority order:
  1. **Held-out empirical bigram** (mg-7dd1's queued v2 direction):
     leave-one-out over pool entries when scoring. The current
     bigram model is built from the same pool's surfaces, so the
     bigram term is identical for all candidates of the same
     surface.
  2. **Cross-corpus position prior** (mg-7dd1's queued v2
     direction): build the per-phoneme position fingerprint from
     a Linear-B / GORILA reference corpus rather than the same
     Linear-A corpus the metric scores against. Breaks the
     position-fit term's circularity.
  3. **Pool-specific bigram models in the runner**: the
     anchor-vs-scramble direction flip indicates that
     cross-pool `local_fit_v1` numbers are not comparable.
     `scripts/run_sweep.py` and `harness.run.score_hypothesis`
     should pick the right pool's bigram model based on the
     hypothesis's `source_pool`, not fall back to aquitanian.
  4. **Corpus-derived phoneme model** (the polecat's "harder
     direction" from mg-7dd1 / mg-23cc): drop the substrate-pool
     prior altogether and learn the phoneme prior from the
     Linear-A corpus's structural patterns (e.g. via
     position-conditional MLE under a candidate sign-to-phoneme
     mapping). This is structurally different from the candidate-
     equation framing and is a separate research direction.

**Operational artifacts.**
- 80 new curated YAMLs under `hypotheses/curated/v4_*.yaml`.
- `hypotheses/curated/CONSTRUCTION.manifest.jsonl` with 100 rows
  (existing 20 + new 80), bucket-tagged.
- `hypotheses/curated/CONSTRUCTION.md` documenting the rules.
- `pools/toponym.yaml` (35 entries) + `pools/toponym.README.md`
  (citation + bias caveats).
- `scripts/build_curated_v4.py` (deterministic builder; idempotent).
- `scripts/score_curated_v4.py` (per-hypothesis pool dispatch
  sweep wrapper; resumable).
- `scripts/curated_v4_stats.py` (self-contained Mann-Whitney U /
  Cliff's δ / power-calc report generator).
- `results/statistics_v4.md` (committed report).
- `harness/tests/test_curated_v4_smoke.py` (loads the manifest,
  validates a sampled subset of YAMLs against the schema, exercises
  one sweep call end-to-end).
- 240 new result rows appended to `results/experiments.jsonl`
  (80 new × 3 metrics). Total stream after merge:
  46,742 + 240 = **46,982 rows**.
- No metrics or harness internals modified — this is a
  methodology ticket per the brief.

## Findings from mg-c2af

Three coupled changes shipped: (a) pool-specific bigram dispatch in
`harness.run` and `scripts/run_sweep.py`, (b) toponym pool expansion
from 35 → 112 entries with derived fragment surfaces, (c) per-surface
aggregation as a new `scripts/rollup.py --by surface` mode and
committed leaderboards. mg-7c8c diagnosed two separate problems —
the runner was falling back to the Aquitanian bigram model for
non-Aquitanian candidates, and the metrics genuinely cannot grade
within-surface plausibility-of-context at any feasible n. mg-c2af
fixes the first and pivots research strategy in light of the second.

### Pool-bigram dispatch fix — pre/post score deltas (n=100 curated)

The 100 mg-7c8c curated hypotheses were re-scored under the fixed
runner. The fix's largest effect lands on the curated buckets whose
`source_pool` did not match a `pools/<name>.yaml` (anchors with
`source_pool: linear_b_carryover`, scrambles with
`source_pool: random_scramble`, and `pre_greek_toponym` curated
fragments). Previously these hypotheses were silently routed through
the Aquitanian bigram model — every bigram of their phonemes hit the
smoothing floor, dragging their `local_fit_v1` scores far below
the level pool-matched candidates were graded at. With pool dispatch
in place these hypotheses now use a `null` bigram model and the
metric rescales the position weight to compensate (see
`harness/metrics.py local_fit_v1` for the renormalization formula).

Median `local_fit_v1` change by curated bucket (n=20 each post-fix):

| bucket           | pre median | post median | Δmedian |
|------------------|-----------:|------------:|--------:|
| anchor           |    -4.4781 |     -0.6709 | +3.8072 |
| scramble         |    -4.0600 |     -0.6422 | +3.4179 |
| plausible (Aqu.) |    -2.8573 |     -2.7863 | +0.0710 |
| wrong (Aqu.)     |    -2.6871 |     -2.7168 | -0.0297 |

Anchors and scrambles jumped by ~+3.5 because they're now scored
under the null-bigram path; plausible/wrong Aquitanian buckets are
nearly unchanged because they were already getting the right pool's
bigram and the per-letter position overrides do most of the work.
Per-hypothesis Δscore: n=80, mean=+1.49, range [-0.11, +3.88].

### Anchor-vs-scramble direction flip — partly resolved

mg-7c8c flagged that `anchor < scramble` under `local_fit_v1` was
the wrong direction (real Linear-B carryover readings should beat
random IPA at the same span). Pre-fix Cliff δ(anchor, scramble) =
**-0.69** (large effect, wrong direction). Post-fix Cliff δ =
**-0.03** (essentially zero — no separation). The wrong-direction
*magnitude* collapsed almost entirely, but the metric still does
not pick anchors out from scrambles in this curated set.

Why the residual: anchors and scrambles share signs by construction
(they pin the same span; only the proposed phonemes differ). With
the bigram term excluded for both, the score is
`(A+B)*pos - C*length_penalty - D*rare_sign`. The position term's
discrimination depends on whether the anchor's phonemes (real
Linear-A carryovers like `ku-ro`) have per-letter position-profile
overrides in `harness/metrics._PHON_POSITION_OVERRIDES` and whether
the scramble's phonemes (random IPA like `q-ʁ`) fall back to the
class-default profile. For most curated pairs the override and
default differ only by ~0.13 log-units per sign — well within
within-bucket dispersion at n=20. The fix corrected the magnitude
confound (anchors are no longer punished by wrong-pool vocabulary);
the discrimination ceiling is the position-term resolution itself,
which is already known to be a v1 limit (mg-7c8c power calc).

### Toponym bulk distribution shape (3,567 candidates, post-fix)

The toponym pool expanded to 112 entries (35 full toponyms + 33
derived fragment surfaces + 44 additional Beekes/Furnée/Kretschmer
toponyms). The `scripts/generate_candidates.py --pool toponym` run
emitted 3,567 candidates (cap_per_entry=50). Distribution:

| metric                                       |    mean |  median |     sd | top 1% |
|----------------------------------------------|--------:|--------:|-------:|-------:|
| local_fit_v1                                 |  -2.473 |  -2.467 |  0.399 | -1.740 |
| partial_mapping_compression_delta_v0 (pmcd)  | -93.253 | -104.00 | 129.09 | +296.0 |
| geographic_genre_fit_v1                      |  +0.650 |  +0.700 |  0.111 | +0.850 |

Comparison to Aquitanian (mg-23cc + mg-c2af re-score, 7,190 cand.):
local_fit_v1 mean **-2.66** (sd 0.30), pmcd median **-96** (sd 110,
top-1% +208), geo mean **+0.45**. Comparison to Etruscan (mg-23cc +
mg-c2af re-score, 5,966 cand.): local_fit_v1 mean **-2.74** (sd
0.21), pmcd median **-112** (sd 111, top-1% +192), geo mean **+0.57**.

Toponym leads on every axis: highest local_fit_v1 mean, highest pmcd
top-1%, highest geographic mean (the `pre_greek × Crete = 1.0`
region-compat row pays off as designed). The toponym local_fit_v1
sd is wider (0.40 vs Aqu. 0.30 vs Etr. 0.21) because the pool now
has its own bigram model and the metric is finally discriminating
between fragment families with different consonant-cluster structure.

### Per-surface top-20 leaderboard (across all pools)

Top 20 (pool, surface) pairs by per-surface median pmcd over
≥10-candidate groups (`results/rollup.surface_aggregated.md`):

| rank | pool        | surface  |   n | median_pmcd | best_pmcd | best_inscription |
|-----:|-------------|----------|----:|------------:|----------:|------------------|
|    1 | toponym     | ssos     |  50 |     +240.00 |   +520.00 | HT 110a          |
|    2 | toponym     | knossos  |  13 |     +184.00 |   +536.00 | KN Zc 6          |
|    3 | toponym     | assos    |  50 |     +180.00 |   +480.00 | KN Zc 6          |
|    4 | aquitanian  | alaba    |  50 |     +172.00 |   +448.00 | ARKH 2           |
|    5 | etruscan    | nene     |  50 |     +172.00 |   +288.00 | HT 117a          |
|    6 | etruscan    | papa     |  50 |     +172.00 |   +288.00 | HT 117a          |
|    7 | aquitanian  | atta     |  50 |     +160.00 |   +328.00 | HT 108           |
|    8 | toponym     | lasaia   |  24 |     +124.00 |   +264.00 | KN Zc 6          |
|    9 | aquitanian  | ama      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   10 | aquitanian  | ere      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   11 | aquitanian  | etxe     |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   12 | aquitanian  | iri      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   13 | aquitanian  | non      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   14 | etruscan    | ana      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   15 | etruscan    | apa      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   16 | toponym     | ala      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   17 | toponym     | sos      |  50 |      +84.00 |   +312.00 | ARKH 2           |
|   18 | toponym     | aptara   |  24 |      +80.00 |   +368.00 | KN Zc 6          |
|   19 | etruscan    | matam    |  50 |      +76.00 |   +288.00 | GO Wc 1a         |
|   20 | aquitanian  | hanna    |  50 |      +72.00 |   +400.00 | KN Zc 6          |

Pool composition of the top-20: **toponym 7**, aquitanian 8,
etruscan 5. Toponym does dominate the high-median band (3 of top 4),
driven entirely by the substrate-suffix family `-ssos/-sos/-assos`
(ranks 1, 3, 17 are pure suffix fragments; rank 2 is the full
Knossos surface; rank 8 is Lasaia which contains the same -saia
diagnostic; rank 16 is the substrate-cluster /ala-/). This is the
expected pattern under Beekes 2010 vol. 2 §3-5: the diagnostic
substrate suffixes are exactly the pieces that recur frequently
in any Aegean-substrate signal.

`results/rollup.surface_aggregated.md` (top-50 across all pools)
plus per-pool views (`.aquitanian.md`, `.etruscan.md`,
`.toponym.md`) committed.

### Per-surface vs per-candidate ranking — the central methodological question

Top-20 *individual* candidates by pmcd are dominated by toponym
(17 of 20 are toponym surfaces; 11 of the top-50 are `ssos`
fragment candidates). The top-20 *per-surface* leaderboard is
similarly dominated (7 of 20 are toponym). At first glance the
two views look like the same projection.

The differences worth noting:

* **`alaba`/`atta` (Aquitanian) and `nene`/`papa` (Etruscan)** climb
  the per-surface ranking even though only ~4 of their candidates
  appear in the top-50 individual list. They get there because they
  have many mid-range candidates: per-surface n=50, per-surface
  median +160-+172. This is the "many positive landings, no single
  outlier" pattern the brief flagged as the kind of evidence a
  per-surface ranking should privilege. (In the per-candidate top-10
  composite from mg-23cc — `hamar`, `hanna`, `ana`, `bere`, `bi`,
  `ere`, `senben` — these are different surfaces from the per-surface
  leaders entirely, except `ana`.)
* **`hanna`** is the converse pattern: per-surface rank 20 (median
  +72) but only 1 of its candidates appears in the top-50 individual.
  Single high-z outlier on KN Zc 6 driving its mg-23cc composite
  rank, no broad-corpus signal.
* **The /-ssos/ fragment family** dominates by per-surface AND
  per-candidate. This is consistent with the substrate hypothesis
  in a stronger way than any single Aquitanian or Etruscan surface:
  the signal is broad-corpus, not concentrated on one inscription.
* **Many Aquitanian/Etruscan/toponym surfaces tie at median +84**
  (ranks 9-17 all): these are 3-phoneme surfaces whose candidate
  windows happen to share a small number of frequent sign triples.
  The metric is not discriminating between them at the per-surface
  level. 9 surfaces with identical median+best across three pools
  is a generator-side artifact — they all pin to the same handful
  of frequent inscription windows.

**The methodologically important finding.** The per-surface
leaderboard re-projects much of the per-candidate composite top-K
(toponym dominance, /-ssos/ family, high-median Aquitanian roots),
but it surfaces a different sub-leader (`alaba`, `atta`, `nene`,
`papa`) that the per-candidate composite misses. These four are
moderately substrate-plausible roots in their respective pools and
their per-surface signal is "many candidates compressing the corpus,
none anomalously high" rather than "one inscription that fits this
root unusually well". This is a real distinction.

### What this strategy does NOT tell us

The per-surface ranking is silent on **which inscription each
surface fits**. The very thing we cannot grade — within-surface
plausibility-of-context — remains ungraded under per-surface
aggregation. A surface that dominates the per-surface leaderboard
because it landed productively on 30 different inscriptions is
indistinguishable, in this view, from a surface that landed on the
same inscription 30 times. The aggregate compresses across exactly
the axis we care about most. Use this leaderboard to **rank pools
and surface families**, not to claim "this inscription says that".

For the same reason, the per-surface ranking does not validate
the substrate hypothesis as such. Toponym dominates because the
diagnostic substrate suffixes recur frequently in the Linear-A
corpus — but a frequent recurrence pattern is what we'd see for
*any* substrate whose phoneme inventory happens to overlap the
syllabogram set at the right structural points. The next move is
either (a) cross-corpus position prior (Linear-B / GORILA reference
per the mg-7c8c "out of scope" list, deferred) or (b) per-surface
controls — score the same surface aggregation against a
phonotactically-matched scramble pool and see whether the substrate
pool's median pmcd actually clears the scramble baseline.

### Artifacts shipped

- `harness/run.py`, `scripts/run_sweep.py`: pool-specific bigram
  dispatch (per-hypothesis lookup against a registry built from
  `pools/`); falls back to `null` bigram for hypotheses with no
  pool match. Backward-compatible `--pool` flag preserved as a
  diagnostic override.
- `harness/metrics.py local_fit_v1`: accepts `bigram_model=None`
  and rescales position weight by `(A + B)/A` so pool-matched and
  pool-unmatched scores remain on the same scale.
- `harness/schemas/result.v0.schema.json`: `bigram_term` may be
  null (with a documentation note pointing to the renormalization).
- `harness/tests/test_pool_dispatch.py`: covers (a) Aquitanian →
  Aquitanian bigram, (b) Etruscan → Etruscan, (c) toponym → toponym,
  (d) anchor / scramble → null/excluded; plus a sweep-runner
  end-to-end check and a determinism assertion (re-runs are
  byte-identical).
- `pools/toponym.yaml`: 112 entries (was 35), full toponyms and
  derived fragment surfaces; `pools/toponym.README.md` documents
  the fragmentation rule.
- `harness/metrics._GG1_REGION_COMPAT`: `pre_greek` × Cretan-site
  coverage extended to all 18 Cretan corpus sites (Tylissos,
  Gournia, Pyrgos, etc.) so toponym candidates landing on minor
  sites hit the substrate-favoring 1.0 row instead of the unmapped
  neutral 0.5.
- `scripts/rollup.py --by surface`: per-surface aggregation mode;
  outputs `results/rollup.surface_aggregated*.md`.
- `scripts/score_curated_v4.py`, `scripts/run_sweep.py`:
  `--force-rescore` flag bypasses the resume cache, used to
  generate post-fix rows on the unchanged corpus snapshot.
- 50,469 new result rows appended to `results/experiments.jsonl`
  (300 curated re-scores + 21,570 Aquitanian re-scores +
  17,898 Etruscan re-scores + 10,701 toponym new). Total stream
  size: 46,982 → **97,451 rows**.
- `results/rollup.surface_aggregated.md` (top-50 across all pools),
  `.aquitanian.md`, `.etruscan.md`, `.toponym.md` (per-pool views).

### Determinism

Pool dispatch is fully deterministic. Re-running the same hypothesis
under the same corpus snapshot produces byte-identical scores: the
pool registry is loaded in sorted basename order, bigram models are
built from pool entries in document order, and the null-bigram path
has no source of randomness. `harness/tests/test_pool_dispatch.py`
asserts byte-identical scores across two consecutive sweep runs.

## Findings from mg-f419

mg-c2af pivoted to per-surface ranking and then closed with the explicit
caveat: *“Toponym dominates because the diagnostic substrate suffixes
recur frequently in the Linear-A corpus — but a frequent recurrence
pattern is what we'd see for any substrate whose phoneme inventory
happens to overlap the syllabogram set at the right structural points.”*
mg-f419 builds the matched controls that test that caveat.

Three phonotactically-matched scramble pools were generated
(`pools/control_aquitanian.yaml`, `.control_etruscan.yaml`,
`.control_toponym.yaml`), each sharing its substrate's phoneme inventory
and length distribution but with surfaces drawn IID from the substrate's
marginal phoneme frequencies (`scripts/build_control_pools.py`,
deterministic seed = sha256(`"control_pool:<pool>"`)[:16]). The control
pools were run end-to-end through the same generator + sweep pipeline,
adding **30,898** rows to `results/experiments.jsonl` (128,349 total).
Per-surface aggregation was then computed for each substrate-control pair
(`scripts/compare_substrate_vs_control.py`,
`results/rollup.surface_aggregated.with_controls.md`).

### Headline answer — none of the three substrate pools clear their controls

For each pool, Mann-Whitney U on per-surface medians (substrate vs
control), Cliff's δ, and the rank of the highest-ranked control surface
in the interleaved leaderboard:

| comparison                              | n_sub | n_ctrl | Δmedian | U      | z      | p (2-tail) | Cliff δ | top-control rank |
|-----------------------------------------|------:|-------:|--------:|-------:|-------:|-----------:|--------:|-----------------:|
| aquitanian vs control_aquitanian        |   153 |    139 |   -60.0 | 9381.5 | -1.740 |     0.0818 | -0.118  |              #1  |
| etruscan   vs control_etruscan          |   138 |    129 |   -76.0 | 6740.0 | -3.431 |     0.0006 | -0.243  |              #1  |
| toponym    vs control_toponym           |    88 |     85 |   -50.0 | 3123.5 | -1.875 |     0.0608 | -0.165  |              #1  |

All three Cliff's δ values are **negative**: the substrate pools'
per-surface medians are *lower* than the matched-phonotactics controls.
For Etruscan the difference is significant in the *wrong* direction
(p = 0.0006). For Aquitanian and toponym the effect is marginal but the
sign is the same. In every case the highest-ranked surface in the
interleaved (substrate ⊕ control) leaderboard is a *control* surface, not
a substrate one — i.e. there is no “separation” between the substrate
top of leaderboard and the control top of leaderboard.

The reading is blunt: at the per-surface aggregation level, the substrate
hypothesis as currently tested is not distinguishable from a same-
phonotactics random scramble. Or in plainer English: the per-surface
leaderboard ranks any pool whose phoneme inventory and length distribution
overlap the Linear-A syllabogram set — the substrate identity of the pool
adds no signal on top of the phonotactics.

### The /-ssos/ family under control

The /-ssos/ substrate-suffix family was the most striking signal in
mg-c2af's leaderboard (toponym `ssos` rank 1 at median +240, `assos`
rank 3 at +180, `knossos` rank 2 at +184). Under the matched control:

- The toponym pool's top control surface is `amrrrrh` (control_toponym,
  median +320). It outranks every substrate toponym surface — so the
  /-ssos/ family no longer leads even the interleaved toponym ranking.
- The control pool also produced a `osossa` surface (median +240,
  best +520 on KN Zc 6) that ties the substrate `ssos` exactly. `osossa`
  is a synthetic random draw from the toponym phoneme inventory; it
  happens to contain the same /sso/ cluster.
- Other -sso-bearing controls in the toponym leaderboard top-15:
  `ssoo` (#6 at +152), `aas` (#8 at +96), `ssn` (#9 at +96), `msssrap`
  (#10 at +88), `sstsnhm` (#17 at +80). These are random
  concatenations.

**Interpretation.** The /-ssos/ family signal is real in the sense that
it's a true compression-improving structural pattern in the Linear-A
syllabogram stream — but the signal lives in the /sso/ phoneme cluster,
not in the substrate-toponym claim. Any source of the same /sso/ pattern
gets the same boost. mg-c2af's flagged-as-suspect signal turns out to be
suspect.

### Per-pool detail

`results/rollup.surface_aggregated.with_controls.md` carries the full
interleaved top-30 plus the top-20 control surfaces for each pool. Salient
control surfaces that beat substrate at the top of each pool:

- **Aquitanian:** control `ehaahee` (#1, median +264, best +728 on
  KN Zc 6) outranks every substrate Aquitanian surface; substrate
  `alaba` (the prior #1 Aquitanian surface from mg-c2af) drops to
  interleaved-rank #2.
- **Etruscan:** control `tllumtrh` (#1) and several other long control
  strings outrank the substrate top (`nene`, `papa`); substrate's
  per-surface median distribution is shifted left of the control's by
  ~76 pmcd points.
- **Toponym:** control `amrrrrh` (#1, median +320) leads. The /-ssos/
  family and full toponym surfaces (Knossos, Phaistos, etc.) are
  interleaved among long control surfaces.

### Rank 9–17 tie diagnosis

mg-c2af's per-surface leaderboard had nine surfaces (`ama`, `ere`, `etxe`,
`iri`, `non`, `ana`, `apa`, `ala`, `sos`) from three pools all tied at
identical median pmcd +84.00 / best pmcd +312.00, all best inscription
ARKH 2. Diagnosis:

1. **All nine surfaces share the same 50 candidate windows.** The bulk
   generator picks the first 50 length-3 syllabogram windows from the
   sorted-by-id corpus where the syllabograms are pairwise distinct
   (`scripts/generate_candidates.py --cap-per-entry 50`). For
   3-phoneme surfaces the first 50 such windows are identical regardless
   of phoneme content, since the cap fires before the corpus is fully
   walked.
2. **PMCD is byte-aligned compression delta and is insensitive to single-
   character phoneme substitutions on short candidates.** When we compare
   the per-window pmcd score for `ama` vs `ere` vs `etxe` vs `ana` vs
   `apa` vs `ala` etc. on the same window, the scores agree to the byte
   on **48 of 50 windows** (the only divergences are toponym `sos`,
   which differs by 8 bits on 2 windows because /s/ has different
   surrounding-context bigram interactions in the DEFLATE window). zlib
   L9's output is byte-aligned, so substituting one 1-character phoneme
   for another rarely crosses a byte boundary on a 4,935-token corpus.
3. **The control pools confirm this.** `control_aquitanian` produces the
   same pattern: `hah` and `tit` (length-3 controls) tie at median +84 /
   best +312 on ARKH 2, identical to the substrate ties.
   `control_toponym` produces a similar ARKH 2 +312 tie cluster
   (`ala`, `ana`, `thnth`).

So the rank 9-17 tie is a **combined generator-side and metric-side
artifact**: the generator emits structurally identical 3-phoneme
candidates across pools, and the metric is too coarse to distinguish
their phoneme content. This is not a metric error — pmcd is correctly
reporting that those 50 windows have a fixed compression-delta when
mapped under any one-character phoneme triple — but it is a *reportable*
artifact when reading the per-surface leaderboard. Recommendation: a
separate small ticket should add per-window deduplication at generation
time so the result stream stops paying compute for structurally identical
candidates that differ only in surface phoneme strings. Filed as
follow-up; not addressed in this ticket per its scope note.

### Implications — fork in the research road

The mg-f419 ticket's brief asked: *if substrate clears, the next research
move is cross-corpus position prior; if substrate does not clear, the
candidate-equation framing or the metric needs a fundamentally different
signal axis.*

The data clearly land on the second fork. None of the three substrate
pools clear their phonotactic-control baselines on per-surface medians.
Concrete consequences:

- The per-surface ranking has no remaining decipherment-relevant signal
  under the current metrics. mg-c2af's top-K surfaces (toponym `ssos`/
  `knossos`/`assos`, Aquitanian `alaba`/`atta`, Etruscan `nene`/`papa`)
  should be downgraded — they are not “the most substrate-plausible
  surfaces in the data,” they are “the surfaces whose phonotactics best
  exploit DEFLATE's byte-aligned compressibility on the syllabogram
  stream.” The substrate identity of the pool is not contributing.
- Cross-corpus position prior (Linear-B / GORILA reference) was queued
  as the natural next step *if* substrate cleared. Since it didn't, this
  is no longer the highest-priority direction. It would still be useful
  for sharpening the position-fit term in `local_fit_v1`, but it does not
  address the diagnosis above.
- The candidate-equation framing needs reframing. Two structural changes
  would respond directly to the mg-f419 finding:
  1. **Pair-up against control during scoring.** Score every candidate
     pair (substrate, matched-control) and report the substrate-minus-
     control delta as the headline metric, instead of substrate score
     in isolation. The aggregator becomes substrate-vs-control by
     construction.
  2. **A signal axis that DOES distinguish substrate from random.**
     The current pmcd + local_fit_v1 + gg1 axes all miss it. Candidates:
     held-out per-pool bigram likelihood (mg-7c8c #1 — pool-LOO over
     entries — would also matter for substrate selection), corpus-side
     phoneme-prediction perplexity under a learned phoneme model
     (Younger 2000 used a similar approach to argue against random
     substrates), or a sign-prediction perplexity under the candidate
     mapping. None are quick to build, but each is a structural pivot
     that would address the mg-f419 finding.
- The methodological humility from mg-c2af was warranted. The
  per-surface leaderboard re-projection produced an interpretable ranking
  but the ranking did not survive its own most-natural control. mg-f419
  is the kind of negative result the mission brief said to take
  seriously — it changes the priority of the upcoming work.

### Artifacts shipped

- `pools/control_aquitanian.yaml`, `pools/control_etruscan.yaml`,
  `pools/control_toponym.yaml` — three phonotactic-control pools.
  Same entry counts (153 / 143 / 112), same length distribution, same
  phoneme inventory subset. Deterministic.
- `pools/control_aquitanian.README.md`, `.control_etruscan.README.md`,
  `.control_toponym.README.md` — per-pool README documenting the
  matching algorithm with a side-by-side phoneme histogram and a length
  distribution match table.
- `scripts/build_control_pools.py` — idempotent control-pool builder.
- `scripts/compare_substrate_vs_control.py` — Mann-Whitney U + Cliff's
  δ on per-surface medians, plus the interleaved leaderboard renderer.
- `harness/tests/test_control_pools.py` — phonotactic-equivalence smoke
  test on a synthetic 8-entry pool plus a sanity check on the committed
  control YAMLs.
- `hypotheses/auto/control_<pool>/`, `.manifest.jsonl` — bulk-generated
  control candidates (6,490 + 5,542 + 3,417 = 15,449 candidates).
- `results/experiments.jsonl` — 30,898 new rows (15,449 candidates × 2
  metrics: `partial_mapping_compression_delta_v0`, `geographic_genre_fit_v1`).
  Stream size 97,451 → **128,349** rows.
- `results/rollup.surface_aggregated.with_controls.md` — interleaved
  substrate-vs-control leaderboard with stats per pool.
- `results/rollup.surface_aggregated.control_aquitanian.md`,
  `.control_etruscan.md`, `.control_toponym.md` — per-control-pool
  per-surface leaderboards.

### Determinism

Control pool generation is fully deterministic — the seed is derived
from a hash of the substrate pool name (`sha256("control_pool:<pool>")
[:16]`) and `random.choices` is the only RNG. Re-running
`scripts/build_control_pools.py` produces byte-identical YAMLs;
asserted by `harness/tests/test_control_pools.py::test_determinism_byte_identical`.
Sweep results inherit the existing `--force-rescore` resume protocol
from mg-c2af.

## Known metric limitations

- **Three metrics in a row missed the n=4 plausible-vs-wrong gate;
  mg-7c8c expanded to n=20 and they still miss it.** Plausible-vs-
  wrong-Aquitanian Mann-Whitney U at n=20 each: `local_fit_v1`
  p=0.84, Cliff δ=+0.04; `partial_mapping_compression_delta_v0`
  p=0.52, δ=+0.12; `geographic_genre_fit_v1` p<0.0001, δ=+0.96
  (tautological — bucket C is defined by genre-incompat). The
  power calculation rules out "n=4 was too small" — at the observed
  effect sizes even n=50 only barely surfaces `pmcd`, and
  `local_fit_v1` is below the noise floor at any realistic n. The
  next move is a *structural* metric change, not a third bucket
  expansion. See the mg-7c8c findings entry for the priority-ordered
  candidate directions (held-out empirical bigram, cross-corpus
  position prior, pool-specific bigram models in the runner,
  corpus-derived phoneme model).
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
geographic-vs-genre filter and metric refinement are scoped follow-ups.
**Per mg-f419, the per-surface ranking does not survive a phonotactic-
control comparison; the leaderboard entries below should be downgraded
in confidence accordingly.***

- **Linear-B carryover anchors** (`hypotheses/curated/anchor_*.yaml`): all
  four scored z ≥ +1.140 on `local_fit_v0` (mg-fb23). `anchor_taina_HT39`
  reached z = +1.964. These are the strongest in-corpus reading anchors
  drawn from a known-related script. (Anchors come from a known-related
  script; mg-f419's negative result on substrate pools does not directly
  affect anchor confidence, since the anchor surfaces are derived from
  a known mapping rather than a substrate hypothesis.)
- **Bulk Aquitanian leaders** (mg-f832, top-10 by `score_control_z`): the
  surfaces `sukalde` (Trask 1997, "kitchen / hearth"), `hil` ("dead, kill"),
  and `haran` lead at z > +2.0. `sukalde` placements concentrate on
  Knossos Zc/Zf inscriptions; `hil` on ARKH 4b/5; `haran` on HT Wc 3010.
  Full leaderboard in `results/rollup.aquitanian.md`. (mg-f419 controls
  were not run on `local_fit_v0`, only on pmcd + gg1; the v0 leaderboard
  has not been directly tested against phonotactic controls but the
  same artifact pattern is plausible at v0.)

## What we have NOT yet tried

- **A signal axis that distinguishes substrate from same-phonotactics
  random.** mg-f419's headline finding: pmcd, local_fit_v1, and gg1 all
  miss this distinction. Until at least one metric clears the matched-
  control baseline, the ranking outputs are not load-bearing. Priority-
  ordered candidates: substrate-vs-control delta as the primary score
  (paired difference per surface), per-pool LOO held-out bigram
  likelihood (mg-7c8c #1, also a substrate-discriminator), corpus-side
  sign-prediction perplexity under the candidate mapping, learned
  phoneme-model perplexity (Younger 2000 style).
- **`local_fit_v2`.** A v2 of the local-fit metric is needed; v1
  (mg-7dd1) shipped as a null finding on three of four discrimination
  bars and mg-7c8c confirmed at n=20 that the within-surface
  plausibility signal it misses is below noise floor at any
  realistic n. Priority-ordered v2 directions (mg-7c8c):
  held-out empirical bigram, cross-corpus position prior,
  pool-specific bigram models in the sweep runner. The corpus-
  derived phoneme model (drop the substrate-pool prior altogether)
  is the "harder direction" alternative. mg-f419 makes the
  *control-paired* version of any of these the natural shape:
  score (substrate – matched-control) rather than substrate alone.
- **Cross-corpus position prior (Linear-B / GORILA reference).** Was
  queued as the natural follow-up *if* substrate cleared mg-f419's
  control test. Since it didn't, this is no longer the highest-priority
  direction — it sharpens local_fit_v1's position term but does not
  address the substrate-vs-control collapse mg-f419 surfaced.
- **Per-window / per-(sign-set, inscription) deduplication at generation
  time.** mg-f419 surfaced the rank 9-17 tie as a generator-side
  artifact (50-window cap fires identically across all 3-phoneme
  surfaces of any pool). Filed as a small follow-up ticket.
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
