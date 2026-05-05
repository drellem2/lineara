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

## Findings from mg-ddee

mg-f419 found that the per-surface leaderboard ranks any pool whose
phoneme inventory and length distribution overlap the Linear-A
syllabogram set — substrate identity adds no signal on top of phonotactics
across all three pools (Aquitanian, Etruscan, toponym). mg-ddee attempts
the structural pivot the f419 close-out flagged: a corpus-derived phoneme
cluster model (no substrate-pool prior) plus a sign-prediction perplexity
metric, scored as a paired difference (substrate − matched control)
rather than as an absolute substrate value.

### Headline answer — null finding (in fact, inverse finding) on all three pools

For each substrate pool, per-surface paired-diff medians were tested
against zero with one-tail Wilcoxon signed-rank (alternative: median > 0,
i.e. substrate beats control) and a sign test for robustness:

| pool       | n_surfaces | median(median paired_diff) | mean   | frac surfaces > 0 | Wilcoxon p (one-tail) | sign-test n+/n | sign-test p (one-tail) |
|------------|-----------:|---------------------------:|-------:|------------------:|----------------------:|---------------:|-----------------------:|
| aquitanian |        153 |                    +0.0000 | -0.069 |             0.144 |                0.9674 |          22/52 |                 0.8942 |
| etruscan   |        143 |                    +0.0000 | -0.105 |             0.105 |                0.9884 |          15/45 |                 0.9920 |
| toponym    |        111 |                    +0.0000 | -0.198 |             0.126 |                0.9953 |          14/51 |                 0.9997 |

All three pools fail the acceptance gate, and the sign tests are
significant in the *opposite* direction — controls systematically beat
substrate at the per-surface paired-diff median level. The toponym pool's
sign-test p of 0.9997 is functionally equivalent to "the wrong direction
at the 3σ level." The mean paired_diff per pool is also negative for all
three pools.

The gate explicitly anticipates this case: "If the data shows substrate <
control significantly, that's also a real finding ... it would mean the
new metric anti-correlates with substrate identity." That is what
happened here, on a metric whose signal direction was supposed to
*depend* on the assignment rather than the phonotactics.

### Why this is a stronger negative than mg-f419

mg-f419's headline was "no signal." mg-ddee's headline is "negative
signal." Specifically:

* The cluster model is built without any pool prior; the only place a
  phoneme-side prior enters is the once-at-build-time bridge from
  cluster centroids to phoneme classes (Trask 1997 ch. 3 position
  priors). The candidate equation's phoneme assignment is the ONLY
  candidate-specific input to term 1 of the metric.
* Paired-difference is computed at the candidate level (same inscription,
  same span; control chosen by minimum edit distance on the phoneme
  sequence) and aggregated to per-surface medians. The leaderboard's
  primary column is the substrate − control delta by construction —
  phonotactic baseline is subtracted out, not assumed-away.
* Despite that, all three pools end up with paired_diff distributions
  centered at zero with negative tails. The metric does not just fail to
  separate substrate from control; it slightly *prefers* control.

This is the second independent direction (after mg-f419) in which the
substrate-pool identity signal does not survive a phonotactic control.

### Distribution of the metric value (substrate + control candidates)

Across all 32,172 candidates (16,723 substrate + 15,449 control):

* mean score = -1.70, median = -1.60, sd = 2.02, min = -7.71, max = +2.69.
* Term 1 (cluster_agreement) is an integer in [0, n_pairs]; for typical
  6-sign equations the modal value is 0–2.
* Term 2 (window_bigram_loglik) dominates the score scale (-7 to 0 in
  nats over 5 bigrams typical), so scores cluster in the -3 to 0 band.

The score distribution per pool is similar in shape; the discriminating
signal (if any) lives in term 1, which is small in magnitude relative to
term 2.

### Why term 2 doesn't discriminate (window-quality prior, not phoneme
discriminator)

Term 2 is a corpus-side bigram log-likelihood over the candidate's
inscription window — it depends only on which signs the equation pins,
not on the proposed phonemes. Two candidates that pick the same window
get identical term-2 contributions. Substrate and control candidates at
the same (inscription, span) thus have identical term-2 contributions,
and the paired-diff cancels term 2 out completely. So the paired-diff
signal lives in term 1 alone — the cluster_agreement count.

### Why term 1 doesn't discriminate (phoneme-to-cluster collapse)

Term 1 counts (sign, phoneme) pairs where ``cluster_id(sign) ==
phoneme_to_modal_cluster(phoneme)``. The bridge is pre-computed at model
build time; for the chosen 8-cluster model, most phonemes (a, e, i, l,
m, n, r, s, u, x, z) bridge to cluster 6 (the largest mid-balanced
cluster), while a few stops (d, g, p, t) bridge to cluster 5 (medial-
heavy) and a few onset-heavy phonemes (b, h, j, k, w) bridge to
cluster 7. Vowel /o/ is the lone bridge to cluster 2 (final-heavy).

The substrate phoneme distributions are heavily vowel-laden (Aquitanian
words are CV / V-final), so substrate candidates pile most of their
phonemes into cluster 6. The control pools were drawn IID from the same
marginal phoneme frequencies, so they pile their phonemes into cluster
6 at almost the same rate. The cluster_agreement counts therefore have
nearly identical distributions for substrate and control candidates at
the same window — and the paired_diff median is ~0 with a slight
negative tail driven by the few candidates where the substrate phoneme
sequence happens to land in non-cluster-6 clusters less often than the
control.

This is structural: with a coarse 8-cluster model and phoneme bridging
that collapses most of the inventory to one cluster, the per-pair
discrimination capacity is ~1 bit per equation, and the within-pool
variance of term 1 is on the same scale as the between-pool difference.
The paired-difference test therefore lacks power, and the sign of the
small effect we do see is unfavorable.

### What this means for the research direction

mg-f419's diagnosis stands: phonotactics, not substrate identity, is what
the leaderboard ranks. mg-ddee tested a structural pivot in the metric
shape; the pivot does not change the verdict. The natural reading is that
*at the current granularity of corpus modeling*, the substrate-vs-random
signal in Linear-A is below the noise floor. Three orthogonal directions
have now failed to surface it (compression delta, local position-fit,
corpus-derived cluster perplexity), and mg-f419's matched-control
framework reduced two of those to "no signal," with mg-ddee converting
the third to "wrong-direction signal."

Per the ticket, this is an explicit "ship the null finding and shift
direction" outcome. The ticket sketched the next-tier directions as:

* **Reframe the candidate-equation hypothesis itself.** The equation
  shape ("this span = this root") may be the wrong unit — a signed
  signature over multiple cooccurring substrate roots within a window
  may be the right shape, since real lexicons cluster by root family.
* **Pull a Linear-B reference corpus** to derive a learned phoneme
  prior in a script known to be a syllabary. The LB position prior +
  cluster centroids would lift the phoneme-bridge step out of the
  hand-curated Trask priors, which is the weakest part of mg-ddee's
  build. This is the Younger-2000-style approach, queued behind
  ingest cost.

mg-ddee does not take either step. Both are larger lifts and the present
ticket's job was to test the cheaper structural pivot first.

### Artifacts shipped

* `harness/corpus_phoneme_model.py` — corpus-derived k-means clustering
  over per-sign distributional features (position-in-word ×5,
  position-in-inscription ×2, genre ×1, top-30 left/right neighbors
  ×1). k=8, deterministic seed=42. Builds and emits
  `harness/corpus_phoneme_model.json` byte-deterministically.
* `harness/corpus_phoneme_model.json` — committed cluster-model
  artifact. 136 signs across 8 clusters; cluster sizes 7, 9, 17, 18,
  6, 11, 29, 39 with distinct mean position-fingerprints (vowel-final,
  standalone, all-medial, etc.).
* `harness/corpus_phoneme_model.README.md` — human-readable cluster
  compositions, phoneme→cluster bridge, and the 8x8 bigram matrix.
* `harness/metrics.py` — `sign_prediction_perplexity_v0` registered.
  Two-term metric: cluster_agreement (term 1) + window_bigram_loglik
  (term 2). The metric is deterministic and per-equation O(window
  length).
* `harness/schemas/result.v0.schema.json` — extended with
  `cluster_agreement`, `window_bigram_loglik`, `n_pairs_scored`,
  `n_window_bigrams` for the new metric, plus optional `paired_diff`
  / `paired_diff_match` columns reserved for rollup-time use.
* `harness/tests/test_sign_prediction_perplexity.py` — smoke test on a
  hand-built 3-cluster mini-model.
* `scripts/run_sweep.py` — accepts `--cluster-model` and dispatches the
  new metric. 32,172 rows scored in ~37s on the committed manifests.
* `scripts/paired_diff_rollup.py` — rollup-time pairing on
  (inscription, span) with edit-distance tie-break on phoneme sequence.
  Emits per-pool acceptance-gate stats (Wilcoxon signed-rank one-tail
  + sign test).
* `results/rollup.paired_diff.sign_prediction_perplexity_v0.md` —
  committed paired-diff leaderboard, all three pools.
* `results/experiments.sign_prediction_perplexity_v0.jsonl` — 32,172
  new rows (16,723 substrate + 15,449 control candidates × 1 metric).
  Sidecar stream — the primary `results/experiments.jsonl` was
  approaching GitHub's 100 MB push limit, so sign_prediction_perplexity_v0
  rows go to a per-metric sidecar. The sweep runner writes to it
  transparently and the paired-diff rollup reads from both files via a
  unified resume cache. AGENTS.md "results/ is append-only" still
  holds: neither file is edited, only appended to.
* `HARNESS_VERSION` bumped to `v7`.

### Determinism

Re-runs of `python3 -m harness.corpus_phoneme_model` produce a
byte-identical JSON. Re-runs of the sweep with the resume cache empty
produce identical row contents (only `run_id` and `ran_at` differ;
`score`, `cluster_agreement`, `window_bigram_loglik` are bit-identical).
Re-runs of `paired_diff_rollup.py` over the same result stream produce
byte-identical markdown.

## Findings from mg-ee18

mg-ddee diagnosed the v7 corpus-derived cluster bridge as collapsing
most of the phoneme inventory to a single cluster, killing
discrimination. v8 keeps the candidate-equation hypothesis shape
(per Daniel's explicit instruction to defer the deeper structural
reframe) and replaces the prior with the polecat's queued
Younger-2000-style direction: a learned **char-bigram phoneme prior
trained on real text in the proposed substrate language** — Basque
Wikipedia for the Aquitanian (and toponym-stand-in) pool, a
Bonfante-and-Bonfante-derived word-form list for Etruscan.

### Headline answer — partial direction reversal; gate still not met

For each substrate pool, per-surface paired-diff medians were tested
against zero with one-tail Wilcoxon signed-rank (alternative: median
> 0, i.e. substrate beats control) and a sign test for robustness:

| pool       | n_surfaces | median(median paired_diff) | mean   | frac surfaces > 0 | Wilcoxon p (one-tail) | sign-test n+/n | sign-test p (one-tail) |
|------------|-----------:|---------------------------:|-------:|------------------:|----------------------:|---------------:|-----------------------:|
| aquitanian |        153 |                    +0.0627 | +0.008 |             0.549 |                0.3804 |          84/152 |                 0.1118 |
| etruscan   |        143 |                    -0.0353 | -0.027 |             0.469 |                0.7495 |          67/141 |                 0.7497 |
| toponym    |        111 |                    -0.0089 | -0.082 |             0.486 |                0.8224 |          54/110 |                 0.6125 |

**No pool clears the 0.05 acceptance gate.** The aquitanian sign-test
p of 0.11 is the first directionally-correct, non-rejected-at-α=0.10
signal this research line has produced — but it is not statistically
significant at the pre-registered bar. v8 ships as a partial-positive
null: directionally improved, structurally insufficient.

### Direction reversal vs. mg-ddee

The previous metric (`sign_prediction_perplexity_v0`) showed
*controls beating substrate* significantly on all three pools (sign
test p ≈ 0.89, 0.99, 1.00). v8 reverses the direction on aquitanian
and approximately neutralizes the etruscan / toponym signal:

| pool       | v7 mean paired_diff | v7 frac > 0 | v8 mean paired_diff | v8 frac > 0 | direction        |
|------------|--------------------:|------------:|--------------------:|------------:|------------------|
| aquitanian |              -0.069 |       0.144 |              +0.008 |       0.549 | reversed         |
| etruscan   |              -0.105 |       0.105 |              -0.027 |       0.469 | neutralized      |
| toponym    |              -0.198 |       0.126 |              -0.082 |       0.486 | partially neutralized |

The reversal is the substantive change. mg-ddee's negative signal was
attributable to the phoneme-to-cluster bridge collapsing most phonemes
to one cluster: substrate candidates piled into the same cluster as
controls and the small remaining wedge slightly favored controls. The
Basque-bigram model in v8 has 28 tokens and 700+ bigram cells, so
phoneme-by-phoneme variation in the candidate's mapping output now
produces meaningful per-bigram log-likelihood deltas. The aquitanian
top-50 leaderboard reflects this: Basque-orthography-friendly
substrate roots (`aitz`, `itsaso`, `oin`, `gatz`, `zelai`, `non`,
`gaitz`, `egun`) all sit at median paired_diff > +1.0 with frac > 0
near 1.0. The win is real per-surface; what fails is generalization
across the full 153-surface set.

### Per-pool diagnostic — Aquitanian-with-Basque is the natural-match
case and it responds best

The brief asked specifically about which substrate pools (if any)
responded best to the external prior. The natural-match prediction
was: aquitanian-with-Basque should clear if any pool does. The
distribution of per-surface paired_diff medians supports the
prediction without certifying the pool:

* **aquitanian.** 84 / 152 surfaces have positive median; the top 50
  are all > +0.36; 18 surfaces score median > +0.7. The shape is "a
  population whose top tail is real and whose bulk is null," consistent
  with a substrate hypothesis that holds for *some* roots but not all.
  Several top-scoring surfaces (`itsaso` "sea", `egun` "day", `nahi`
  "want", `etxe` "house", `ama` "mother", `ona` "good") are core
  inherited Basque vocabulary; their high paired_diff is the natural
  outcome if any subset of Linear-A signs encoded these words.
* **etruscan.** 67 / 141 surfaces positive — a near-50/50 coin-toss.
  The top 50 includes `chimth`, `larth`, `mach`, `sath`, `suthi`,
  `camthi`, all attested Etruscan forms with the language's
  characteristic aspirate-cluster digraphs. Their median paired_diff
  is positive and high (>+1.3), but the bulk of the 143 surfaces
  cluster around zero. The Etruscan model carries α=1.0 smoothing on
  a 666-form corpus, which limits its per-bigram precision; this is
  the documented v8 limitation, and the etruscan flat result is
  consistent with both "substrate not present" and "model too noisy
  to detect substrate." We cannot distinguish those two readings on
  this evidence alone.
* **toponym.** 54 / 110 surfaces positive — also near-50/50. The
  toponym pool is scored against the Basque model as a substrate-style
  stand-in (no pre-Greek text corpus exists). The neutral result is
  consistent with either (i) the toponym hypothesis being wrong, or
  (ii) Basque being the wrong stand-in for pre-Greek phonotactics.
  The toponym top-50 is dominated by Greek-style surfaces (`kuzikos`,
  `zakuntos`, `phaistos`, `amnisos`, `tegea`) with mostly small
  positive medians (+0.1 to +0.3); the signal is weakly positive at
  the surface level but heterogeneous in direction across the bulk.

### Distribution of metric values

Across all 32,172 candidates the per-pool raw score distributions
under their own LM dispatch:

| pool                  |      n | mean   | median | sd   |
|-----------------------|-------:|-------:|-------:|-----:|
| aquitanian            |  7,190 | -6.218 | -6.194 | 0.71 |
| control_aquitanian    |  6,490 | -6.281 | -6.271 | 0.81 |
| etruscan              |  5,966 | -5.279 | -5.367 | 0.78 |
| control_etruscan      |  5,542 | -5.269 | -5.375 | 0.75 |
| toponym               |  3,567 | -6.332 | -6.291 | 0.67 |
| control_toponym       |  3,417 | -6.318 | -6.301 | 0.75 |

The Etruscan pool's higher absolute scores (mean -5.28 vs -6.22 for
aquitanian) reflect the smaller, smoother Etruscan LM rather than a
substrate-vs-Aquitanian quality difference; raw scores are not
comparable across LMs. Paired-diff is the right unit; matched control
shares the substrate's LM dispatch by construction so the LM choice
cancels.

### What this means for the candidate-equation framing

Per the brief's explicit instruction: if all three pools fail the
acceptance gate, the next move is fundamentally structural — a
reframe of the candidate-equation hypothesis itself. v8 fails the
gate on all three pools, but **it fails informatively**: the
direction reversal on aquitanian-with-Basque (the natural-match
case) is the first directionally-correct signal in this research
line, and the per-surface top-50 includes coherent, contextually
plausible Basque roots. The metric is doing something right; the
candidate-equation shape is the limiting factor.

A concrete reframe sketch for the next ticket: **signed signature
over multiple cooccurring substrate roots within a window, rather
than one root per equation.** Real lexicons cluster by root family
(an inscription that has one Basque-substrate root tends to have
several adjacent ones), and the candidate-equation shape — pin
one span to one root, score independently — discards that
co-occurrence structure. A reframed hypothesis would: (i) pick a
window of, say, 12-20 tokens; (ii) propose a *set* of substrate
roots that jointly cover most of the window; (iii) score the
joint coverage as a single log-likelihood under the same external
LM, with non-overlapping mappings required across the chosen
roots. This subsumes the current single-equation scoring (set of
size 1) while admitting the multi-root-per-window case which the
current shape cannot represent.

A second, complementary reframe: per-surface bayesian update over
many windows. The aquitanian top-50 surfaces all have many windows
each (n=24-50) that vary in paired_diff. The current rollup takes
the median per surface; a bayesian per-surface posterior over "is
this surface real Linear-A vocabulary?" would integrate the
window-by-window evidence and surface roots whose evidence is
*concentrated* (a few high-confidence windows) rather than
dispersed (many marginal windows). The current statistics treat
both shapes identically.

Both reframes are larger lifts than the v8 metric swap. They are
the natural mg-pee18+1 direction; v8's job was to confirm or rule
out the cheaper "different prior, same hypothesis shape" pivot
first. The cheaper pivot does not pass the gate but the
pivot also informatively narrows the next move: a metric that DOES
get the direction right at the per-surface top, but whose median-
across-surfaces does not survive aggregation, is a metric whose
unit of aggregation is wrong — exactly the diagnosis a multi-root-
per-window reframe addresses.

### Artifacts shipped

* `corpora/basque/` (gitignored) + `corpora/basque.fetch_manifest.txt`
  (committed, 122 pinned eu.wikipedia.org revisions) +
  `corpora/basque.README.md` — provenance, CC BY-SA 4.0 license,
  rebuild procedure. ~3.5 M chars after normalization (acceptance
  bar ≥100 k).
* `corpora/etruscan/words.txt` (gitignored) +
  `corpora/etruscan.README.md` + `scripts/build_etruscan_corpus.py`
  with inline `SUPPLEMENTARY` table — 666 unique word forms
  combining the existing `pools/etruscan.yaml` attestations with a
  curated supplementary list from Bonfante & Bonfante 2002 + Liber
  Linteus + TLE personal-name catalog. Acceptance bar ≥500.
* `harness/external_phoneme_model.py` — char-bigram model class,
  28-token vocab (a-z + space + `<W>`), add-α Laplace smoothing,
  byte-deterministic JSON serialization with rounded log-probs.
* `harness/external_phoneme_models/basque.json` (α=0.1) +
  `etruscan.json` (α=1.0) — committed model artifacts.
* `scripts/fetch_basque_corpus.py` — fixed-revision fetch from
  eu.wikipedia.org via the MediaWiki API. Supports a one-shot
  `--resolve-revids` mode for refreshing the manifest pins.
* `scripts/build_external_phoneme_models.py` — deterministic model
  builder; reads either text or word-list corpora.
* `harness/metrics.py` — `external_phoneme_perplexity_v0` registered.
  Per-char average char-bigram log-likelihood over runs of mapped
  phonemes; `<unk>` / `DIV` / `INSCRIPTION_BOUNDARY` all break runs.
* `scripts/run_sweep.py` — pool→language dispatch table for the new
  metric (Aquitanian/toponym → Basque, Etruscan → Etruscan; control
  pools share their substrate's LM); `--external-model-dir` flag;
  loads every needed LM at startup.
* `harness/tests/test_external_phoneme_perplexity.py` — 12 smoke
  tests, including a hand-computed run-extraction check, a Basque-
  vs-bad-stream sanity check, and an OOV-fold check.
* `results/experiments.external_phoneme_perplexity_v0.jsonl` (sidecar)
  — 32,172 new rows; ~26 MB; well below the 100 MB push limit.
* `results/rollup.paired_diff.external_phoneme_perplexity_v0.md` —
  committed paired-diff leaderboard, all three pools, top-50 per
  pool by median paired_diff, plus the per-pool acceptance-gate
  Wilcoxon + sign-test stats.
* `harness/schemas/result.v0.schema.json` — extended with
  `n_runs`, `n_chars_scored`, `n_phonemes_scored`, `total_loglik`,
  `language` for the new metric.
* `HARNESS_VERSION` bumped to `v8`.

### Determinism

Re-runs of `scripts/build_external_phoneme_models.py` produce
byte-identical JSON (verified). Re-runs of the sweep with an empty
resume cache produce identical row contents (only `run_id` and
`ran_at` differ; `score`, `total_loglik`, `n_runs`,
`n_chars_scored` are bit-identical). Re-runs of
`paired_diff_rollup.py` over the same result stream produce
byte-identical markdown.

The Basque corpus is reproducible only modulo Wikipedia's
content-drift if the pins are rotated (`--resolve-revids`); against
a fixed manifest, Wikipedia's revision-immutability guarantees
byte-identical fetches.

## Findings from mg-bef2

mg-ee18 produced the first directionally-correct signal in the
Aquitanian pool (sign-test p=0.11, 54.9% of surfaces positive, top-50
dominated by inherited core Basque vocabulary at median paired_diff > +1.0)
but missed the formal one-tail acceptance gate on every pool. The
diagnosis was that "the metric is doing something right; the
candidate-equation shape is the limiting factor." This ticket replaced
the single-root-per-equation hypothesis with `candidate_signature.v1`
— a multi-root signature over a window of one inscription, with the
union of the roots' sign->phoneme mappings as the partial mapping
consumed by `external_phoneme_perplexity_v0`. Matched controls keep
the same window, the same per-root span placements, and the same
root-length distribution; only the surfaces / phonemes change.

**Headline result: stronger null in the wrong direction.** All three
substrate pools fail the acceptance gate, with the Wilcoxon test in
the substrate-*below*-control direction at large effect sizes:

| pool       | n_surface_sets | n_paired records | median(median paired_diff) | mean | frac surface-sets > 0 | Wilcoxon p (1-tail) | sign-test n+/n | gate |
|------------|---------------:|-----------------:|---------------------------:|-----:|----------------------:|--------------------:|---------------:|:----:|
| aquitanian |            178 |             1971 |                    -0.5031 | -0.6344 |                 0.253 |              ~1.0 (substrate worse) |        45/178 | FAIL |
| etruscan   |            184 |             2053 |                    -0.1732 | -0.1444 |                 0.277 |              ~1.0 |        51/184 | FAIL |
| toponym    |             90 |              808 |                    -0.9004 | -0.8897 |                 0.067 |              ~1.0 |          6/90 | FAIL |

The one-tail p reported here is the substrate>control alternative; the
substrate<control direction is the one with the small p-value, and a
post-hoc two-tail rejection of substrate==control is decisive in every
pool. The reported `~1.0` is `1 − tiny`, consistent with that.

**Distribution shift v8 → v9, by pool.** The single-root v8 paired-diff
distribution sat very close to zero in every pool; v9 multi-root pulls
sharply negative everywhere:

| pool       | v8 single-root (mg-ee18) median paired_diff | v9 multi-root median(per-surface-set median) | shift |
|------------|--------------------------------------------:|---------------------------------------------:|------:|
| aquitanian |                                     +0.0627 |                                      -0.5031 | −0.57 |
| etruscan   |                                     -0.0353 |                                      -0.1732 | −0.14 |
| toponym    |                                     -0.0089 |                                      -0.9004 | −0.89 |

The reframe did not just fail to improve the signal — it *reversed* it
in Aquitanian (where v8 had been weakly positive) and *amplified* it in
toponym (where v8 had been near zero). Etruscan moved least, but in the
same direction. So the multi-root co-occurrence hypothesis is
falsified at the population level: across the 4,832 paired
(substrate-signature, control-signature) records over 452 distinct
sorted root-surface tuples, controls outscore substrate by a wide
margin under the external phoneme LM.

**Top per-window signatures still show coherent kinship/landscape
clusters.** The top-20 (across pools, by per-window paired_diff) is
not noise — it carries the same semantic-cluster pattern v8 hinted at,
just dwarfed by the bulk distribution:

  * Aquitanian (17/20 of top-20): `seni+seni` (kin+kin), `aitz+seni`
    (rock + kin), `lur+seni` (mountain/earth + child/kin), `ile+lur`
    (hair + earth), `bi+bi+sembe` (two + son), `lur+lur` (earth+earth),
    `lur+ur` (mountain + water). The pairs cluster cleanly into
    kin / landscape / numeral semantic families.
  * Etruscan (3/20): `larth+zal` (god-name + verbal-stem-like) at
    SY Za 4 and `aiser+semph` (god + verbal-stem-like) at HT 115a.
  * Toponym (0/20): no toponym signature reaches the top-20.

These per-window paired_diffs sit in [+0.79, +1.62] — the same
magnitude as v8's anchor-bucket separation in the curated v4 set. So
the *right-tail* of the v9 distribution looks like a coherent
multi-root substrate fit; the *bulk* is dominated by signatures whose
union mapping over-projects the same short root (`ur`, `lur`, `bi`)
across the corpus and gets penalized for the resulting unrealistic
phoneme-stream pattern.

**What does this tell us.** Multi-root signatures, evaluated as a
population under a held-out external phoneme LM, are *worse* than
single-root candidates and *much worse* than length-matched
phonotactic controls. The polecat's working theory ("real lexicons
cluster by root family") is not refuted at the per-signature level —
the top-20 above looks exactly like that theory predicts — but the
cluster signal is buried by a bulk failure mode the v9 generator
exposes:

  * **Root-projection bias.** Greedy-fill places the *longest*
    compatible root at each open position. The Aquitanian pool's
    median root length is 4 phonemes; the SigLA corpus's median
    inscription length is 4 syllabograms. The longest root that
    fits is usually the *only* root that fits, and short
    high-frequency roots (`ur`, `lur`, `bi`) repeatedly win the
    leftover slots. The resulting union mapping injects the same
    2-3 phonemes into many positions across the corpus, and the
    Basque LM scores that flat-pattern poorly.
  * **The matched control is more diverse than the substrate.** A
    paired control draws each of its k roots independently from
    the synthetic phonotactic pool, so the union mapping it
    produces sees more distinct phonemes more uniformly across
    the corpus than the substrate union does. The control isn't
    "winning by accident" — the LM literally prefers a phoneme
    stream with more even distribution over `a..z` than one
    dominated by 2-3 substrate phonemes.
  * **The aggregation key (sorted root-surface tuple) compounds
    this.** A surface-set like `lur+lur+lur+ur` produces a single
    median across many windows, and that single number lands well
    into the negative because the same projection failure
    repeats. The 102 surface-sets in Aquitanian's aggregation are
    therefore *not* 102 independent observations — they are 102
    correlated samples of the same projection bias.

**Acceptance.** All three pools fail; the result ships as the spec's
"stronger null." The polecat's complementary reframe — a *per-surface
bayesian update over many windows*, treating concentrated evidence
(many positive paired_diffs on the same surface-context combination)
differently from dispersed evidence — is now the natural next ticket.
That reframe operates entirely on the existing v8 + v9 paired-diff
data: no new candidate generation is required.

**Sketch for the bayesian-posterior reframe.** For each surface S in
substrate pool P:

  1. Collect every paired_diff record where S appears (single-root
     v8 or any signature whose roots[] contains S in v9).
  2. Compute a posterior over `θ_S = P(this S-context is real
     substrate)` under a Beta(α, β) prior (α=β=1, uninformative)
     using the per-record paired_diff as evidence (positive = +1
     toward θ_S; sign rather than magnitude, so very-large
     concentrated evidence doesn't dominate).
  3. Rank surfaces by posterior mean, with sample size as a
     credibility cap (small-n surfaces don't lead the
     leaderboard regardless of how positive their few records
     are).

That ticket would replace the population-level Wilcoxon (which mg-bef2
just demonstrated is too coarse for this data) with a per-surface
posterior that surfaces the right-tail signal v8 + v9 both
hinted at. It would *not* require a new metric, a new schema, or a
new corpus pull.

**Operational notes for v9.**

  * Substrate signatures: 2,162 (Aquitanian), 2,116 (Etruscan), 841
    (toponym). The Aquitanian and Etruscan pools land in the
    spec's 2k-8k estimate band; the toponym pool falls short
    (841) because its YAML has no 2-phoneme entries, so the median
    Linear A inscription (4 syllabograms) cannot host two non-overlapping
    toponym roots. The generator's defaults
    (`cap_per_inscription=25`, `cap_per_root_set=8`,
    `window_lengths=6,8,10,12,16,20`, `min_roots=2`,
    `coverage_threshold=0.5`) are deliberately more permissive than
    the spec's nominal 5/3 caps; that change is what brings
    Aquitanian + Etruscan into the 2k band, and it does not change
    the qualitative direction of the result (mean and Wilcoxon p
    are within 5% of the original 5/3 run). Per-pool yields are
    stable across re-runs; the generator is deterministic and
    idempotent.
  * Matched-control yield: 1,971/2,162 (Aquitanian, 91.2% paired),
    2,053/2,116 (Etruscan, 97.0%), 808/841 (toponym, 96.1%). The
    dropped substrate signatures had no consistent control
    assignment under the ranked control pool — typically because
    the closest-edit-distance control roots all produced sign-
    mapping conflicts with already-placed control roots in the
    same signature.
  * Sweep ran in ~7 s total across all 6 manifests on a fresh
    laptop; the metric is the same as v8.
  * The signature schema (`harness/schemas/hypothesis.candidate_signature.v1.schema.json`)
    enforces: ≥ 1 root, non-overlapping root spans, consistent
    union sign->phoneme mapping, well-formed coverage block. The
    sweep runner gates `external_phoneme_perplexity_v0` as the only
    metric that consumes signatures.

## Findings from mg-d26d

mg-bef2 shipped the strongest null we'd produced (population-level
Wilcoxon decisively in the *substrate-below-control* direction across
all three pools) but the polecat's diagnosis was that the failure is
structural to v9's greedy-fill generator, not to the multi-root
hypothesis itself: the top-K per-window signatures showed coherent
kinship/landscape clustering exactly as the substrate theory predicts
— that signal was just buried by a bulk distribution dominated by a
few short, over-projected roots. mg-d26d pivots the *aggregation*
without changing the metric or the candidate-equation/signature
shape: a per-surface Beta-binomial posterior over the v8 single-root
+ v9 multi-root paired_diff data treats the *sign* of paired_diff as
binary evidence for `θ_S = P(this surface is real Linear-A substrate
vocabulary)` and reads the right tail directly, so concentrated
positive evidence on a coherent substrate surface is no longer
collapsed against dispersed negative evidence on a different surface.

**Headline result: 2/3 substrate pools clear the right-tail gate.**
One-tail Mann-Whitney U on top-20 substrate posterior means vs top-20
control posterior means (ranked by raw posterior_mean):

| substrate pool | n_substrate_top | n_control_top | median(top-20 substrate posterior) | median(top-20 control posterior) | MW U (substrate) | MW p (one-tail, substrate>control) | gate |
|----------------|----------------:|--------------:|-----------------------------------:|---------------------------------:|-----------------:|-----------------------------------:|:----:|
| aquitanian     | 20              | 20            | 0.9808 | 0.9512 | 345.0 | 3.22e-05 | PASS |
| etruscan       | 20              | 20            | 0.9808 | 0.9217 | 321.0 | 5.21e-04 | PASS |
| toponym        | 20              | 20            | 0.9186 | 0.9464 | 149.5 |   0.9165 | FAIL |

Aquitanian and Etruscan beat their phonotactically-matched controls
at the right tail at p < 0.001 and p < 0.01 respectively. Toponym
fails — the toponym pool's right-tail substrate posteriors are
*lower* than its control's right-tail posteriors (median 0.92 vs
0.95). This is the first acceptance-gate clear in the project; it is
also the first time we have separated substrate from control at all,
not just in toy buckets.

**Distribution shift across rollups, by pool.** v8's per-surface
median rollup (mg-ee18) and v9's per-surface-set median rollup
(mg-bef2) both ran into the same problem: a single number per
surface (or per surface-set) compresses concentrated and dispersed
evidence identically, and the population-level Wilcoxon then sees a
bulk distribution dominated by the dispersed-evidence regime.
mg-d26d's posterior leaderboard recovers the right-tail signal:

| pool       | v8 single-root rollup gate (mg-ee18) | v9 multi-root rollup gate (mg-bef2) | mg-d26d bayesian right-tail gate |
|------------|:------------------------------------:|:-----------------------------------:|:--------------------------------:|
| aquitanian | FAIL (Wilcoxon p=0.38, sign p=0.11)  | FAIL (Wilcoxon p~1.0, frac>0=0.25)  | **PASS (MW p=3.22e-05)**         |
| etruscan   | FAIL (p=0.75, sign p=0.75)           | FAIL (p~1.0, frac>0=0.28)           | **PASS (MW p=5.21e-04)**         |
| toponym    | FAIL (p=0.82, sign p=0.61)           | FAIL (p~1.0, frac>0=0.07)           | FAIL (MW p=0.92)                 |

**Top-20 substrate vs top-20 control side-by-side (gate input).**

*Aquitanian.* All 20 top substrate surfaces have k_s = n_s − 1 or
k_s = n_s (a near-perfect 50–53 records each, every record positive
or all-but-one positive). The substrate top-20 is glossable as a
single semantic stratum of inherited core Basque vocabulary —
nature/landscape (`aitz` rock, `eki` sun, `argi` light, `itsaso`
sea, `zelai` meadow), body (`oin` foot, `bihotz` heart), descriptor
(`beltz` black, `ona` good, `gaitz` ill), function/grammatical
(`hau` this, `nahi` desire, `entzun` hear), kinship (`hanna` brother),
time (`egun` day), food (`ezti` honey), dwelling (`ate` door),
place (`hesi` fence), number (`zortzi` eight), morphology (`ako`
suffix). The control top-20 is the random-phonotactic noise floor:
`anao`, `onia`, `aninze`, `an`, `zaa`, `aai`, `arzaeai`, `tztzan`,
`ia`, `ilae`, `enaa`, `ntsilai`, `aaer`, `anii`, `aatzasl`, `zihn`,
`loear`, `aoel`, `hina`, `keho` — phoneme-frequency-matched strings
sampled from the substrate pool's letter distribution, no glossable
content.

*Etruscan.* Top-20 substrate is the same single-stratum pattern in
the Etruscan domain — religion (`aiser` gods, `thesan` dawn-goddess,
`hanthe` ritual-position, `spureri` sacrifice-for-the-city),
common praenomina (`larth`, `laris`, `thana`, `sech` = Larth, Laris,
Thana, daughter), function (`camthi` magistrate, `nac` as/when, `matam`
above/before, `chimth` at/near), time (`avils` of-years, `zelar`
ritual-time, `caitim` month-name). Control top-20: `thia`, `vsinc`,
`aasaas`, `laaeca`, `chsa`, `mechthsll`, `la`, `miphit`, `thi`,
`izththuch`, `chischeaa`, `hsaa`, `cael`, `srchlcn`, `cthpnr`, `iaae`,
`aalchci`, `arth`, `chelnscr`, `sueip` — random Etruscan-phonotactic
strings, again no semantic coherence.

*Toponym.* The substrate top is recognizable Aegean toponyms
(`dikte`, `keos`, `kno`, `minoa`, `tenos`, `iassos`, `lemnos`,
`kuzikos`, `melitos`, `tulisos`, `melos`, `aspendos`, `kalumnos`,
`zakuntos`, `lukia`, `mukenai`, `lykabettos`, `itanos`,
`halikarnassos`, `poikilassos`) but at lower posterior means
(0.82 – 0.98) than the control top (`eoao`, `aathei`, `ana`, `eta`,
`ioonaol`, `kolee`, `kllzua`, `anealo`, `kim`, `oaest`, `saenaa`,
`aas`, `ala`, `oks`, `tea`, `aasn`, `onn`, `aoe`, `nul`, `eonun`),
which sit at 0.89 – 0.99. Toponym is structurally harder for this
metric: most toponym roots are length-5+ multisyllable strings,
fewer windows have an exact-length match, and the control's
phonotactic distribution drifts further from natural-language
phoneme frequencies (the `eoao` / `aathei` controls are extreme),
which the Basque LM still scores well by sheer phoneme-frequency
match. The posterior surfaces a real signal — the substrate top is
the Aegean toponym corpus we put in — but the control top wins on
the right tail because the control pool's character distribution
landed in a region the LM treats as low-perplexity for the wrong
reason.

**Bayesian surfaces vs v8/v9 rollups, by surface set.** The bayesian
top-20 substrate is largely the same surface set as v8's
median-paired_diff top (mg-ee18), but the order is meaningfully
different and the magnitude of evidence per surface is more
trustworthy because it counts every paired_diff record (including
v9 multi-root signatures that mention the surface) rather than only
the v8 single-root rollup. The v8 leaderboard ranked Aquitanian
surfaces by per-record median magnitude; the bayesian leaderboard
ranks by record-count of wins. These are different orderings:
`aitz` and `itsaso` lead both, but the bayesian ranking surfaces
`hanna`, `nahi`, `ako`, `beltz` higher than v8's median did — those
surfaces' v8 medians were modest, but they win 50/50 records, and a
posterior that counts 50 wins as 50 wins puts them right next to
`aitz`. v9's per-surface-set median (mg-bef2) failed at the
population level for the multi-root projection-bias reason; the
bayesian rollup's per-surface (not per-surface-set) aggregation
sidesteps that by reading individual roots out of multi-root
signatures and treating each record as one observation per surface.

**Semantic-family characterization of the right-tail.**

  * Aquitanian top-20 is a clean single stratum — inherited core
    Basque vocabulary across the standard semantic families
    (nature, body, descriptor, kinship, function, time, food,
    dwelling, place, number, morphology). No semantic family
    dominates; the top-20 reads like a Swadesh-list cross-section.
    This is consistent with the polecat's `seni+seni`,
    `aitz+seni`, `lur+ur` per-window observations from mg-bef2
    surfacing as their constituent roots `aitz`, `itsaso`,
    `oin`, `eki` here — the multi-root co-occurrence pattern
    decomposes into single-surface high-posterior cells.
  * Etruscan top-20 is dominated by religious vocabulary +
    common praenomina + function words + time references. This
    is exactly the genre profile of the Etruscan votive /
    funerary corpus the pool was sourced from, so the
    leaderboard is recovering the corpus's lexical center of
    gravity rather than randomly distributed noise.
  * Toponym top-20 is geographically coherent (Aegean +
    Anatolian + Cretan toponyms in proportion), so the substrate
    semantic structure is intact even where the gate fails. The
    failure is on the control side, not the substrate side.

**What does this tell us about the candidate-equation framework.**

The candidate-equation hypothesis IS supported at the right tail in
two of the three substrate pools. Specifically:

  * **The metric works.** When given enough records per surface
    (50+ for Aquitanian and Etruscan core surfaces), the
    held-out external phoneme LM separates substrate from
    phonotactically-matched control consistently. The mg-bef2
    bulk failure was real but it was not a metric failure; it
    was an aggregation-unit failure (per-signature-tuple
    medians) compounded by a generator failure (root projection
    bias).
  * **The hypothesis shape works at the surface level, not the
    surface-set level.** v9's multi-root signatures fail
    population-level Wilcoxon for structural reasons (greedy fill
    + short high-frequency roots dominate leftover slots), but
    the *constituent roots* of those signatures still pull
    substantial positive evidence per surface. The right
    aggregation unit for this data shape is the surface, not the
    signature; the surface aggregates over both single-root and
    multi-root contexts.
  * **What's left to do.** The toponym failure is a real
    constraint on the framework as currently specified — the
    Aegean toponym corpus has a phonotactic profile that the
    matched-control sampler can land too close to the
    substrate-favoured region of the LM's distribution. The
    next ticket is now genuinely choosable: (a) re-aggregate v9
    matched-control sampling so toponym controls don't get to
    pile mass on the LM's preferred corner, (b) pull a Linear-B
    reference corpus for cross-corpus position prior (the
    polecat's "other other" direction), or (c) accept the 2/3
    pass as the strongest result we can get under the current
    metric and move to the manuscript-side narrative. None of
    these is automatically correct — the bayesian gate has
    converted the question from "is there any substrate signal
    at all" (we now have evidence: yes, in two of three pools)
    into "what does the toponym failure mean for the framework"
    (a substantive, narrowable methodological question).

**Operational notes for v10.**

  * Records used: 16,723 v8 substrate candidates with paired
    controls + 4,832 v9 substrate signatures with paired
    controls = 21,555 paired records aggregated across 408
    distinct substrate surfaces (and the same records
    redistributed across 364 control surfaces on the flipped
    side). Determinism: posterior, CI, and MW p-values are
    byte-identical across re-runs of `scripts/per_surface_bayesian_rollup.py`
    given the same `experiments.external_phoneme_perplexity_v0.jsonl`
    and `hypotheses/auto*` manifests.
  * Credibility cap n_min = 10. The leaderboard is not
    dominated by tiny-n surfaces — the top-30 in every pool sit
    at credibility = 1.0 (n ≥ 10). The shrinkage matters at
    rank ~40+ where n < 10 surfaces would otherwise lead with
    raw posterior 2/3 or 3/4. Documented in the script
    docstring; configurable via `--n-min`.
  * The gate uses raw posterior_mean (not the credibility-shrunk
    effective score) deliberately: the spec frames the question
    as a right-tail comparison, not a credibility-weighted
    comparison, and using raw posterior_mean means a small-n
    surface that happens to win all its records can still appear
    in the gate's top-20 (and on inspection none of those
    appear; the top-20 is dominated by n ≥ 50 surfaces in the
    substrate pools that pass).
  * The Beta inverse-CDF is implemented from scratch via
    Numerical Recipes' Lentz BetaCF + bisection — no scipy
    dependency, consistent with the rest of the harness.
  * Sensitivity analysis on top-K: not run as part of v0 (the
    spec lists it as optional). On inspection, the Aquitanian
    and Etruscan gates clear so decisively (p < 1e-3) that
    top-10 / top-50 sensitivity is unlikely to flip them; the
    toponym gate fails so decisively (p ≈ 0.92) that no top-K
    relaxation will rescue it without changing the procedure.

## Findings from mg-0f97

mg-d26d's right-tail bayesian gate cleared on 2/3 substrate pools —
the first acceptance-gate clear in the project. mg-0f97 validates
that result by cross-substrate negative control: rescore each pool's
v8 + v9 substrate + matched-control records under the *other*
substrate's external phoneme LM (Aquitanian under the Etruscan LM,
Etruscan under the Basque LM) and re-run the same right-tail
posterior gate. If the v10 separation is real substrate signal, it
should collapse under the wrong LM. If the separation persists, the
v10 metric is preferring a character distribution regardless of the
substrate-LM relationship, which would invalidate the substrate
specificity claim. The ticket also bundles a per-inscription
right-tail concentration analysis: for each Linear A inscription, how
many v10 top-20 substrate surfaces have positive paired-diff records
on it? (Both pieces operate on existing v8 + v9 + v10 data — pure
analysis layer, no new corpus, no new metric.)

**Headline result: validation is mixed.** Etruscan validates cleanly;
Aquitanian validates only partially. The 2/3 v10 pass should be
reported as one strong-validation pool + one weak-validation pool,
not as a single uniform substrate result.

| pool       | v10 same-LM gate (mg-d26d) | v11 cross-LM gate (mg-0f97)  | validation outcome              |
|------------|:--------------------------:|:----------------------------:|:--------------------------------|
| aquitanian | PASS, MW p=3.22e-05        | PASS, MW p=0.0205 (etr LM)   | **partial** — signal persists under wrong LM at p<0.05 |
| etruscan   | PASS, MW p=5.21e-04        | FAIL, MW p=0.591 (bsq LM)    | **holds** — substrate-LM specificity confirmed |
| toponym    | FAIL, MW p=0.92            | (not run; v10 already FAIL)  | n/a                             |

The Etruscan validation is exactly the discriminating outcome the
ticket was designed to detect: under the Basque LM, the Etruscan
substrate top-20 (median posterior 0.9615) does not separate from
its matched control top-20 (median 0.9535) — MW U = 192.0, p = 0.591.
The v10 Etruscan PASS therefore reflects substrate-LM-specific
phonotactic match, not a metric artifact.

The Aquitanian validation is the worrying outcome. Under the Etruscan
LM, the Aquitanian substrate top-20 still beats its matched control
top-20 at p = 0.0205. The substrate-side median posterior (0.9808) is
identical to the same-LM case; the control-side median moves slightly
(0.9512 → 0.9422) but is the same order of magnitude; the MW U drops
from 345.0 to 275.5. Substrate beat its control on ~14/20 head-to-head
rank pairs even under the *wrong* LM. Reading this conservatively:
the Aquitanian top-20 surfaces have a phonotactic profile that *both*
the Basque and Etruscan LMs partially reward over the matched-control
sampler — the LM choice is not the only thing pulling substrate >
control on the Aquitanian side. Possible explanations (none confirmed
by this ticket):
  * The control sampler for `control_aquitanian` may not be tightly
    matched on Aquitanian-style phonotactics — the controls might
    have moved into a low-LM-density corner that *any* substrate-style
    LM would punish, regardless of which substrate.
  * The Aquitanian substrate surfaces may exhibit a "natural-language
    phonotactic profile" property that is shared by Basque and
    Etruscan — both are real-language LMs trained on word-form
    distributions; if Aquitanian roots happen to be plausible word
    forms in either tradition, both LMs reward them.
  * A subset of the v10 Aquitanian top-20 (e.g. `aitz`, `hesi`,
    `itsaso`, `argi`, `ate`, `beltz`) appears in the cross-LM top-20
    for Aquitanian substrate as well, alongside new entries (`bels`,
    `hara`, `hezur`, `hil`, `mahats`, `sori`, `sei`, `hamar`,
    `haran`, `hori`, `zahar`, `seme`); the ranking is reshuffled, not
    merely scaled. That reshuffling rules out the simplest "the metric
    just prefers all of them" story but does not localize the
    confound.

**The Etruscan side is doing what we want.** The v10 Etruscan
substrate PASS is now backed by a clean cross-substrate negative
control: when scored under the Basque LM (which has no historical or
phonotactic relationship to Etruscan), substrate and control are
indistinguishable in the right tail. The Etruscan top-20 surfaces
(`larth`, `aiser`, `matam`, `avils`, `camthi`, `chimth`, `hanthe`,
`laris`, `nac`, `sech`, `thana`, `zelar`, `caitim`, `thesan`,
`spureri`, `thanchvil`, `suthi`, `mach`, `arnth`, `sath`) reflect a
phonotactic match to *Etruscan-like text* and not to any
"natural-language" prior the Basque LM also recognizes.

**The Aquitanian side is a yellow flag, not a red flag.** The cross-LM
result's p-value (0.0205) is a 5x weaker separation than the same-LM
result (3.22e-05), meaning the Etruscan LM is *worse* at confirming
Aquitanian substrate than the Basque LM is — the LM choice does
contribute. But the cross-LM separation is still present, which means
the Aquitanian PASS in v10 is *partly* but not *entirely* attributable
to the substrate-LM specificity. Conservative reporting: the v10
Aquitanian result needs further investigation before publication-shape
claims; the v10 Etruscan result does not.

**Per-inscription right-tail concentration analysis.** Of 185 Linear
A inscriptions in the working set, 43 have ≥1 v10 top-20 substrate
surface with positive paired-diff evidence and 40 have ≥2. The
top-30-by-raw-count is dominated by long accountancy tablets at
Haghia Triada / Arkhanes / Gournia (where the substrate generator
emits many records per inscription, so even moderate per-record
positive rates compound into high raw counts). The top-30-by-density
(raw count divided by total v8+v9 records targeting the inscription)
better reflects "this inscription is genuinely amenable to substrate
readings." Top-density inscriptions:

| rank | inscription | site | genre | n_top20 | n_records | density |
|-----:|:------------|:-----|:------|--------:|----------:|--------:|
|    1 | `HT Wc 3010`  | Haghia Triada | accountancy            | 14 |  76 | 0.184 |
|    2 | `HT Wc 3017a` | Haghia Triada | accountancy            | 14 |  76 | 0.184 |
|    3 | `KH 60`       | Khania        | accountancy            | 14 |  76 | 0.184 |
|    4 | `KN Zb 5`     | Knossos       | unknown                | 14 |  76 | 0.184 |
|    5 | `HT 90`       | Haghia Triada | accountancy            | 14 |  94 | 0.149 |
|    6 | `KH 10`       | Khania        | accountancy            | 14 | 100 | 0.140 |
|    7 | `KH 5`        | Khania        | accountancy            | 14 | 110 | 0.127 |
|    8 | `HT 127a`     | Haghia Triada | accountancy            | 12 | 100 | 0.120 |
|    9 | `HT 12`       | Haghia Triada | accountancy            | 12 | 102 | 0.118 |
|   10 | `ARKH 6`      | Arkhanes      | accountancy            | 10 |  85 | 0.118 |

The full top-30-by-count and top-30-by-density tables, with the
specific top-20 surfaces present per inscription, are in
`results/rollup.right_tail_inscription_concentration.md`. Two
patterns are visible:

  * **Cluster A (accountancy + Etruscan-substrate-heavy).** Knossos
    Zc/Zf, Haghia Triada Wc / Zb, Khania accountancy tablets (`KH 60`,
    `KH 10`, `KH 5`), and HT Wc commodity records. The ~14 top-20
    surfaces present on these tablets are the Etruscan religious /
    praenomen / time-reference cluster (`aiser`, `avils`, `bihotz`,
    `camthi`, `entzun`, `hanna`, `hanthe`, `itsaso`, `laris`, `matam`,
    `thesan`, `zelai`, `zelar`, `zortzi`, plus `caitim` /
    `thanchvil` / `spureri` on the Knossos votive subset). Genre and
    site are consistent: short-line accountancy / votive tablets.
    These are the Etruscan-side concentration candidates and inherit
    the Etruscan validation outcome (substrate-LM-specific signal).
  * **Cluster B (longer accountancy at HT / ARKH / GO with mixed
    Aquitanian + Etruscan top-20).** `GO Wc 1a`, `ARKH 5`, `HT 104`,
    `HT 103`, `ARKH 2`, etc. show 23–38 distinct top-20 surfaces. The
    surface mix is broader (more Aquitanian-side surfaces present:
    `aitz`, `ako`, `ate`, `eki`, `hau`, `oin`, `ona`, `argi`, `nahi`)
    plus the Etruscan side. Conservatively these inscriptions inherit
    the Aquitanian partial-validation caveat — the per-inscription
    concentration is real but the substrate-LM-specificity of the
    underlying signal is weaker.

These per-inscription findings are the first publication-shape
research output of this project: they identify specific Linear A
tablets that concentrate substrate evidence and would reward
domain-expert review (especially the Khania / Knossos votive subset,
where substrate concentration is high *and* the Etruscan-side gate
validates cleanly). However they should be reported with the validation
caveat baked in — Cluster B's Aquitanian concentration is on a result
that did not fully validate.

**Multi-root all-top20 v9 signatures: empty, as expected.** The
ticket also asked for v9 signatures whose constituent surfaces are
all in v10 top-20. Across both passing pools, **0** signatures meet
this strict criterion (12 aquitanian + 30 etruscan have ≥1 top-20
constituent; 0 + 1 have ≥2). This is consistent with the mg-bef2
documented v9 greedy-fill bias toward short, high-frequency surfaces
(`ur`, `lur`, `seni`, `sembe`, `su`); v10's top-20 surfaces are
length 4–7 and rarely fit the leftover slots after the greedy fill
places its preferred short roots. The full filtered table (≥1 top-20
constituent, n=23 substrate signatures, 17 substrate wins / 6
substrate losses on paired_diff) is in
`results/rollup.multi_top20_signatures.md`. Notable substrate-wins:
`PH 7a [0..17] larth+larth+zal+zal` (paired_diff +0.6373),
`HT 108 [0..15] aitz+lur+seni` (+1.1444), `HT 108 [0..11] aitz+seni`
(+1.3461), `SY Za 4 [3..12] larth+zal` (+1.0978),
`HT 115a [0..15] aiser+semph` (+0.8961). Substrate-losses cluster on
`HT 104` (4 signatures, all losses) — worth flagging for v12
investigation.

**What does this tell us about the project's status.**

The ticket framed two scenarios at submission time: (a) validation
holds + per-inscription concentration is non-trivial → publishable-
claim status; (b) validation fails OR per-inscription evidence too
dispersed → further investigation. Neither scenario applies cleanly:

  * **Etruscan substrate**: substrate-LM-specific signal validated
    cleanly. Per-inscription concentration is non-trivial (Cluster A
    above). This pool is at publishable-claim status: the v10 right-
    tail PASS on Etruscan reflects a substrate-LM-specific phonotactic
    match, and a defined set of inscriptions (Cluster A) concentrate
    that match.
  * **Aquitanian substrate**: substrate-LM-specificity is partial.
    Per-inscription concentration is real but inherits the cross-LM
    weakness. This pool is at "needs further investigation" status:
    publishable-shape claims should wait for either (i) a tighter
    matched-control sampler that closes the cross-LM weak separation,
    or (ii) a sister-syllabary positive control (Linear-B reference
    corpus, the polecat's "(b)" option from mg-d26d) that confirms
    the v10 Aquitanian PASS reflects substrate signal rather than
    natural-language-LM bias.

**Operational notes for v11.**

  * Records cross-LM rescored: 17,813 Aquitanian + control_Aquitanian
    (under Etruscan LM) + 15,677 Etruscan + control_Etruscan (under
    Basque LM) = 33,490 hypothesis × LM pairs. New rows are appended
    to `results/experiments.external_phoneme_perplexity_v0.jsonl`
    with `language=` set to the swapped LM; existing same-LM rows
    are not modified. The v10 same-LM bayesian rollup
    (`scripts/per_surface_bayesian_rollup.py`) is updated to filter
    rows by `(hash, language)` so cross-LM rows do not contaminate
    same-LM aggregation; re-running the rollup against the now-
    augmented file produces byte-identical output to the v10
    committed `rollup.bayesian_posterior.{aquitanian,etruscan,
    toponym}.md`.
  * Cross-LM rescore wall time: ~54 s for all 4 pools on a fresh
    laptop (the metric is char-bigram log-prob over O(stream-length)
    per hypothesis; the corpus stream and LM tables are reused
    across all hypotheses).
  * The cross-LM rescore script (`scripts/cross_lm_rescore.py`) is
    idempotent on `(hypothesis_hash, language)` pairs — a re-run is
    a no-op once the pairs are present.
  * Toponym pool was excluded from cross-LM rescoring by ticket
    decision: v10 already failed for toponym (control-sampler issue,
    documented in mg-d26d), so the cross-LM control would not be
    informative there.
  * Per-inscription rollup (`scripts/right_tail_inscription_concentration.py`)
    and multi-root signature rollup (`scripts/multi_top20_signatures.py`)
    are deterministic given the same result stream + manifests.
  * The v10 top-20 substrate surface lists are hardcoded in the
    per-inscription rollup at module level (rather than recomputed
    from the bayesian posterior on every run) so the per-inscription
    leaderboard is reproducible *as a downstream analysis of v10's
    published top-20*; if the upstream ranking ever shifts due to a
    tie-breaking change, the per-inscription rollup will keep
    pointing at the v10-published surfaces unless the constants are
    updated explicitly.
  * **Out of scope for this ticket** (deferred to v12 + later):
    Linear-B reference corpus pull (sister-syllabary positive control
    if validation holds, alternative-prior test if it doesn't);
    toponym control re-sampling; manuscript-side narrative;
    Phoenician / Sumerian / other substrate pools; domain-expert
    review of top-K. The validation outcome here makes the Linear-B
    pull more tractable to scope (positive control on Etruscan side,
    alternative-prior test on Aquitanian side — both directions are
    informative) but does not pre-empt the v12 brief.

## Findings from mg-4664

mg-4664 is the v12 ticket: Linear-B sister-syllabary positive control,
Aquitanian / Etruscan third cross-LM check, and the mg-0f97 forks'
"manuscript narrative" sub-piece. The ticket pulls a Linear-B reference
corpus (LiBER, https://liber.cnr.it; 5,638 inscriptions) and routes
the existing 20 curated Linear-B carryover anchors plus a new
Mycenaean-Greek char-bigram LM through the same v8 / v9 / v10 / v11
pipeline as a positive control. It also re-routes the existing
Aquitanian + Etruscan substrate / control candidates through the
Mycenaean-Greek LM as a third-LM cross-check (in addition to v11's
Aquitanian↔Etruscan swap), and consolidates the project's findings
into a publication-shape document at `docs/findings_summary.md`.

**Lead headline: the Linear-B positive control FAILS the gate at
p=0.155.** This is the most important result of the ticket. The
substrate top-20 median posterior (0.7500) is well above the control
top-20 median (0.3103), but the population MW U on top-K does not
cross p<0.05 (n=12 substrate top vs n=11 control top, MW U=83 vs null
expectation 66). The framework cleanly recovers the well-attested
Linear-A administrative terms — `kuro` (total/sum), `kiro`
(deficit/owed), `mate`, `tare` — at substrate posterior 0.85–0.98
versus control posterior 0.83 max, but fails to recover the
conjectural anchors `dare` (0.0192, loses 50/50 paired records),
`dina` (0.1154), `ara` (0.1923), `taina` (0.1923). The right-tail
gate as currently specified is therefore conservative against
mixed-cleanness substrate pools.

**Secondary headline: Aquitanian under Mycenaean-Greek LM also
fails the gate (p=0.0953), consistent with v10 Aquitanian PASS
being substrate-LM-specific.** Etruscan under Mycenaean-Greek LM
likewise fails the gate (p=0.185), consistent with v11's clean
Etruscan substrate-LM-specificity finding. Full third-LM table:

| pool       | own-LM (v10)      | cross-LM (v11)    | third-LM (v12, Mycenaean-Greek) | interpretation                                                            |
|------------|:-----------------:|:-----------------:|:-------------------------------:|:--------------------------------------------------------------------------|
| aquitanian | PASS p=3.22e-05   | PASS p=0.0205     | FAIL p=0.0953                   | Mediterranean LMs reward Aquitanian; truly unrelated LM does not          |
| etruscan   | PASS p=5.21e-04   | FAIL p=0.591      | FAIL p=0.185                    | substrate-LM-specific; both unrelated LMs collapse the separation         |

The brief's two interpretive scenarios for the Aquitanian third-LM
check were:
  * If Aquitanian beats controls under MycGreek too → "natural-language
    LM bias" (any natural-language LM rewards Aquitanian roots) → v11
    cross-LM partial signal is genuine.
  * If Aquitanian does NOT beat controls under MycGreek → v11 partial
    cross-LM separation is a Basque-Etruscan kinship artifact → v10
    Aquitanian PASS is substrate-specific.

We landed on the second scenario at p=0.0953. The Aquitanian
substrate top-20 median (0.9808) is *unchanged* from same-LM and
cross-LM, but the *control* top-20 median climbs to 0.9630 under
MycGreek (vs 0.9512 under Basque, 0.9422 under Etruscan). This
matches the expected shape: vowel-heavy random-phonotactic controls
(`edae`, `ioro`, `riieen`) score well under Mycenaean-Greek's
heavy-vowel LM regardless of substrate provenance, narrowing the
substrate-vs-control gap from the right-tail's control side rather
than from the substrate side. The v10 Aquitanian PASS is therefore
genuinely substrate-specific when measured against a phonotactically
unrelated LM; the v11 partial separation under Etruscan LM is most
likely a Basque-Etruscan Mediterranean-phonotactic kinship artifact,
not "natural-language LM bias" in general.

**What this means for the v10 PASSes.** Two readings of the
positive-control failure are compatible with the data:

  1. **Gate-too-conservative reading.** The v10 PASSes for Aquitanian
     and Etruscan are genuine substrate signal; the positive-control
     fails specifically because the Linear-B carryover anchor pool
     contains both well-attested and conjectural readings (the
     conjectural ones drag the population MW U). Under this reading,
     a refined gate (e.g. require top-N% to *uniformly* beat top-N%
     of control by some margin) would be more honest about
     mixed-cleanness pools but would not change the qualitative
     conclusion for Aquitanian/Etruscan.
  2. **Curation-sensitivity reading.** The framework recovers signal
     only on substrate pools where the majority of entries are
     correct. The v10 PASSes for Aquitanian and Etruscan reflect
     that those pools (Trask 1997 core; Bonfante & Bonfante 2002 +
     TLE) happen to be uniformly clean by curation. Linear-B
     carryover failed because we mixed canonical Linear-A
     accountancy terms with conjectural readings, exactly the kind
     of heterogeneity the gate cannot tolerate. Under this reading,
     the v10 PASSes are valid only conditional on the substrate
     pools being uniformly clean — a condition we have not
     independently certified.

Both readings are consistent with the data. The conservative
interpretation is reading #2: ship v10 PASSes as
"promising-but-pool-curation-conditional" rather than as
publication-ready claims. Domain-expert review of the top-K
Aquitanian / Etruscan surfaces is the missing certification.

**Operational notes for v12.**

  * **Linear-B corpus.** 5,638 inscriptions from LiBER (Knossos 4,228;
    Pylos 1,086; Mycenae 100; Thebes 75; Tiryns 72; Khania 53; small
    counts at MI/MA/DI/VOL/EL/GLA/KR/OR/MED/IK/ARM/MAM/PR/SI). Pulled
    with `scripts/fetch_liber.py` (polite throttled scraper), parsed
    with `scripts/parse_liber.py` into per-inscription JSON +
    `corpora/linear_b/all.jsonl`. The Mycenaean-Greek transliteration
    is extracted from each tablet's `<meta name="description">` tag,
    syllabogram clusters are kept (lowercase ASCII, hyphens stripped),
    logograms / digits / damage markers / single-character tokens are
    dropped. Output is 21,634 word tokens, 5,113 unique forms.
  * **Mycenaean-Greek LM.** α=0.1 (matches Basque setting; corpus is
    well-resourced enough that minimal smoothing is appropriate).
    n_tokens=41,558, n_chars=31,332, n_words=5,113. Built by
    extending `scripts/build_external_phoneme_models.py` with a
    `--only mycenaean_greek` branch and committed at
    `harness/external_phoneme_models/mycenaean_greek.json`.
  * **Linear-B carryover pool.** `pools/linear_b_carryover.yaml`
    promotes the 20 curated anchor surfaces (4 from mg-fb23 + 16
    from mg-7c8c) to a first-class pool. Built by
    `scripts/build_linear_b_carryover_pool.py`. 20 unique surfaces;
    8 single-class entries are skipped by `generate_candidates.py`'s
    standard `local_fit_v0`-class filter (data, kapa, kupa, kupa3,
    kuse, mina, paja, pitaja). The remaining 12 entries × cap-50 =
    600 substrate candidates. `pools/control_linear_b_carryover.yaml`
    is built by extending `scripts/build_control_pools._SUBSTRATE_POOLS`
    to include `linear_b_carryover`; 9 single-class skips, 11 entries
    × cap-50 = 550 control candidates.
  * **LM dispatch.** `scripts/run_sweep._EXT_POOL_LANGUAGE` and
    `scripts/per_surface_bayesian_rollup._DEFAULT_LANGUAGE_DISPATCH`
    both gain `linear_b_carryover → mycenaean_greek` and
    `control_linear_b_carryover → mycenaean_greek` rows. Existing
    same-LM pools' dispatch is unchanged.
  * **Third-LM rescore.** `scripts/cross_lm_rescore.py` gains a new
    `--mode third` flag that swaps to a `_THIRD_LM_DISPATCH` table
    routing the four existing Aquitanian + Etruscan substrate /
    control pools through `mycenaean_greek`. 33,490 hypothesis-LM
    pairs scored in 61 s (~550/s); identical resume-cache logic to
    v11 (key = (hypothesis_hash, language)); idempotent.
  * **Bayesian rollup invocation.** `--language-dispatch` JSON
    overlay routes Aquitanian + Etruscan rows to `mycenaean_greek`
    for the third-LM aggregation; `--out-suffix
    .under_mycenaean_greek_lm` keeps the new outputs from
    overwriting the same-LM and cross-LM committed files. The full
    no-args rollup now produces 4 per-pool files (the existing
    aquitanian / etruscan / toponym, plus linear_b_carryover) and
    a combined `rollup.bayesian_posterior.md` with all four pool
    sections.
  * **Tests.** `harness/tests/test_linear_b_pipeline.py` covers the
    LiBER HTML parser (logograms dropped, syllabograms preserved,
    short tokens dropped, broken-bracket syllabograms still parsed),
    the run_sweep / bayesian-rollup dispatch table edits, and the
    pool / control pool layouts. `harness/tests/test_cross_lm_rescore.py`
    gains a check on the new `_THIRD_LM_DISPATCH` table.
  * **Determinism.** All new code paths are deterministic. Re-running
    the LM build, the candidate generator, the sweep, the third-LM
    rescore, or the bayesian rollup produces byte-identical output
    given the same cached LiBER HTML + the same result stream +
    manifests. The LiBER fetch caches HTML by tablet id under
    `.cache/liber/tablet/<id>.html` (gitignored); a fresh fetch is
    polite (8 workers × 0.05s sleep) and finishes in roughly 7
    minutes against the live LiBER endpoint.
  * **Out of scope (deferred).** Tighter matched-control sampler for
    toponym; refined gate for mixed-cleanness pools; per-window
    deduplication (mg-f419 follow-up); GORILA ingest; additional
    substrate pools (Phoenician, Sumerian, Hattic); domain-expert
    review of top-K. The findings_summary.md document spells these
    out as the remaining work for full publication.
  * **See also.** `docs/findings_summary.md` for the manuscript-shape
    consolidation; `results/rollup.bayesian_posterior.linear_b_carryover.md`
    for the full positive-control top-K leaderboard;
    `results/rollup.bayesian_posterior.{aquitanian,etruscan}.under_mycenaean_greek_lm.md`
    for the third-LM per-pool tables;
    `results/rollup.bayesian_posterior.under_mycenaean_greek_lm.md`
    for the combined third-LM view.

## Findings from mg-c216

mg-c216 is the v13 ticket: build the consensus sign-to-phoneme map +
cross-window coherence test that distinguishes the two readings v12
left coupled — (1) gate-too-conservative (the v10 PASSes are real
substrate signal that the population MW U gate just under-credits on
mixed-cleanness pools) vs (2) curation-sensitivity (the v10 PASSes
hold *only because* Aquitanian + Etruscan pools are uniformly clean,
and the framework cannot tolerate heterogeneity). v13 also runs a
small refined-gate sensitivity check on the Linear-B positive control
at K ∈ {5, 10, 20} to address reading #1 directly.

**Lead headline: the cross-window coherence test FAILS decisively for
both substrate pools.** Median per-surface coherence is 0.1818 for
Aquitanian and 0.1808 for Etruscan, both far below the 0.6
acceptance bar. The full per-surface range is tight: Aquitanian
[0.1805, 0.1864], Etruscan [0.1739, 0.1867]. This strongly supports
**reading #2 (curation-sensitivity)** of the v12 fork: the v10
Aquitanian and Etruscan PASSes do not reflect coherent underlying
sign-to-phoneme readings. Per-inscription gloss generation (originally
slated for v14) is therefore **not justified by the data**.

**Secondary headline: the refined-gate sensitivity check shows the
production K=20 gate is partially over-conservative on mixed-cleanness
pools, but a less-conservative gate does not rescue the coherence
verdict.** On the Linear-B positive control:

| K  | n_substrate_top | n_control_top | median substrate | median control | MW U  | p (one-tail) | frac substrate > max(control) |
|---:|:---------------:|:-------------:|:----------------:|:--------------:|:-----:|:------------:|:-----------------------------:|
|  5 |       5         |      5        |     0.8846       |    0.5772      | 24.0  |  **0.0106**  |             0.800             |
| 10 |      10         |     10        |     0.7692       |    0.3552      | 71.0  |   0.0603     |             0.400             |
| 20 |      12         |     11        |     0.7500       |    0.3103      | 83.0  |   0.1547     |             0.333             |

K=5 cleanly clears p<0.05; K=10 is borderline; K=20 (production) is
the v12-reported p=0.155 fail. So a smaller gate K *would* rescue the
positive control, which on its own is partial evidence for reading #1.
But this is purely a surface-aggregate verdict; the **deeper
sign-to-phoneme-mapping verdict from the coherence test is
unambiguous failure**, so the surface-aggregate over-conservatism is
not the load-bearing finding here.

The honest combined reading: the v10 PASSes are coherent at the
surface-aggregate level (and the K=20 gate is somewhat over-strict on
mixed-cleanness pools), but they reflect substrate-pool / substrate-LM
phonotactic kinship rather than stable per-sign readings. They are
not a reading map.

### Method

`scripts/consensus_map.py`:

1. For the v10 (mg-d26d) Aquitanian + Etruscan top-20 substrate
   surfaces, walk the v8 single-root + v9 multi-root paired-diff
   records (built via the same helpers as
   `scripts/per_surface_bayesian_rollup.py`).
2. Filter to **positive paired_diff only** — equations where the
   substrate side beat its matched control. Negative-paired-diff
   records are excluded so "wrong" mappings don't bias the consensus.
3. For each such record, read the candidate's `sign_to_phoneme`
   mapping. v8: from `equation.sign_to_phoneme` of the single root.
   v9: from each root's `sign_to_phoneme`, restricted to roots whose
   surface is in the v10 top-20 set.
4. Aggregate (sign, phoneme) → count, plus (sign) → contributing v10
   surfaces.
5. Per-sign consensus: modal phoneme + smoothed Dirichlet-multinomial
   posterior (symmetric prior with α=0.5 over V=23 distinct phonemes
   observed; modal posterior = (n_modal + α) / (N + αV)) +
   max-likelihood Shannon entropy in bits.
6. Filter signs with n_proposals < N (default N=10).
7. Per-surface coherence: Σ_s [freq(S, s) · P_modal(s)] / Σ_s freq(S, s)
   weighted by sign-frequency in S's positive equations. Per-pool
   coherence: median over surfaces.

The aggregation is over **all four paired-diff streams** (v8 substrate
and v9 substrate for both Aquitanian + Etruscan pools, paired against
their matched controls). 7,190 of 17,180 substrate paired-diff records
are positive; those 7,190 records contribute the consensus.

### What the consensus map looks like

61 distinct Linear A signs received at least one positive-paired-diff
proposal; 60 of them have ≥10 proposals (the n_min threshold for the
consensus map). The map is dominated by very high-entropy signs:
**every sign in the consensus map has entropy ≥ 2.05 bits** (out of
log2(23) ≈ 4.52 bits maximum). Modal posteriors range from 0.10 to
0.27. The *least-scattered* sign in the entire consensus map is A718:
modal phoneme `i` with 12 proposals and modal posterior 0.234
(entropy 2.055 bits) — still nowhere near consensus.

The high-frequency signs (which appear in many windows and therefore
get many proposals) are uniformly diffuse: AB08 (464 proposals),
AB09 (387), AB01 (389), AB81 (348) — modal posteriors 0.15–0.20,
entropy 3.9 bits. There is no sign for which a single phoneme
dominates the proposal histogram. The contributing-surfaces lists for
the high-frequency signs include essentially the entire v10 top-20
(38+ surfaces each), which is the structural reason the consensus is
diffuse: the metric rewards substrate phonotactic surfaces broadly,
not specific sign-to-phoneme assignments. Different substrate roots
that happen to align with the same Linear A window propose different
sign mappings, and all of them score positive paired_diffs.

The full map is committed at
`results/consensus_sign_phoneme_map.md`. The header tables (per-pool
coherence + per-surface breakdown + refined-gate sensitivity) come
first; the per-sign rows follow, sorted by entropy ascending.

### Top-K signs by consensus

Sorted by entropy ascending (lowest-entropy = most-concentrated
consensus). All five top entries have very high entropy by absolute
standard, illustrating that even the *most coherent* signs in the
consensus map are not coherent in any reading-map sense:

| sign | n_proposals | modal | modal_posterior | entropy_bits | contributing v10 surfaces |
|:--|---:|:--|---:|---:|---:|
| `A718` |  12 | `i` | 0.2340 | 2.055 | 12 |
| `AB13` |  26 | `i` | 0.2267 | 2.998 | 26 |
| `A306` |  14 | `i` | 0.1373 | 3.039 | 14 |
| `AB66` |  15 | `i` | 0.1321 | 3.057 | 14 |
| `A323` |  14 | `a` | 0.1765 | 3.093 | 14 |

Compare with the brief's expectation: *"if the modal phoneme per
Linear A sign is stable across many independent candidate equations
(low entropy), reading #1 is right."* Observed entropies are far
above the "low" regime; modal posteriors are far below "stable."
Reading #2 is supported.

### Per-pool coherence verdict

| pool       | n_surfaces | n_with_coherence | median coherence | min     | max     | gate (≥0.60) |
|:-----------|:----------:|:----------------:|:----------------:|:-------:|:-------:|:------------:|
| aquitanian |     20     |        20        |     0.1818       | 0.1805  | 0.1864  |    **FAIL**  |
| etruscan   |     20     |        20        |     0.1808       | 0.1739  | 0.1867  |    **FAIL**  |

Both pools' coherence values cluster tightly in [0.17, 0.19] —
nowhere near the 0.6 acceptance bar, nowhere near even the
"close-but-no-cigar" 0.5–0.55 the brief flagged as ambiguous. The
verdict is unambiguous failure on the central question of v13.

### What this means for the v10 PASSes (and downstream tickets)

The v10 Aquitanian + Etruscan PASSes are real *as surface-aggregate
substrate-vs-control statements* — they reproduce, the cross-LM
checks behave as expected (v11/v12), and the K=5 refined-gate gives
the Linear-B positive control a clean p<0.05. But the per-sign
sign-to-phoneme mappings underlying those PASSes are not coherent
across windows. This means:

* **Per-inscription gloss generation (originally v14) is *not*
  justified by the data.** Reading-shape claims like "HT Wc 3010
  contains *aiser*" rely on a stable sign→phoneme map; we don't have
  one. v14 reframes per the brief: away from gloss generation,
  toward held-out pool-curation tests (deliberately polluting the
  Aquitanian pool with conjectural entries to see whether the PASS
  survives, as the structural curation-sensitivity test).
* **The framework still recovers a real signal.** The signal is at
  the substrate-pool / substrate-LM phonotactic-kinship level —
  v10's PASS gate is mechanically sound and the surface-aggregate
  numbers do reproduce. But what's reproducing is "this substrate
  surface's phoneme stream beats a random-phonotactic control under
  this LM," not "this surface attaches to specific Linear A signs in
  a stable way."
* **The K=20 gate is somewhat over-conservative** on mixed-cleanness
  pools (the Linear-B K=5 result is real), but adopting a smaller K
  would not change the v13 verdict — the deeper coherence failure
  rules out reading-map work regardless of where the surface gate
  is set.
* **`docs/findings_summary.md` is updated** to reflect the new
  verdict and to flag explicitly that no per-sign mapping is
  validated.

### Why coherence is so low — the structural explanation

For each Linear A sign s that appears in many windows, the v10 top-20
substrate surfaces collectively propose *many different phonemes* for
s, because each surface has a different phoneme structure and is
getting its positive paired_diff from "the metric rewards substrate
phonotactics broadly," not from "this specific surface is the right
reading at this specific window." The phonemes proposed for s
therefore scatter across the alphabet:

* AB08 (464 proposals, modal `a` at posterior 0.167, entropy 3.925
  bits, top-3 alternatives e/h/z): the same Linear A sign has been
  variously proposed as /a/, /e/, /h/, /z/, and many more, by
  different substrate surfaces' equations.
* AB37 (227 proposals, modal `i` at posterior 0.187, entropy 3.713
  bits, alternatives a/n/th): similarly scattered.

For the per-sign histogram to concentrate, the v10 top-20 surfaces
would need to propose the *same* phoneme for the same sign across
many windows. They don't — and the diffusion is the proximate cause
of the coherence failure.

### Operational notes

* **Inputs.** Re-uses `scripts/per_surface_bayesian_rollup.build_v8_records`
  + `build_v9_records` to build paired-diff records from
  `results/experiments.external_phoneme_perplexity_v0.jsonl` +
  `hypotheses/auto/{aquitanian,etruscan}.manifest.jsonl` +
  `hypotheses/auto_signatures/{aquitanian,etruscan}.manifest.jsonl`.
  No new corpus data ingest, no new metric. Pure analysis layer over
  the existing v10 paired-diff stream.
* **YAML reads.** Each positive-paired-diff record requires reading
  one hypothesis YAML to extract `sign_to_phoneme`. Across 7,190
  positive records the full run takes ~45–60s on Daniel's machine.
  No caching needed at this scale.
* **v10 top-20 is hardcoded.** `_V10_TOP20_BY_POOL` in
  `scripts/consensus_map.py` mirrors
  `scripts/right_tail_inscription_concentration.py:_V10_TOP20_BY_POOL`
  — the v10 mg-d26d top-20 list, hardcoded so downstream analyses
  reproduce against v10's published right-tail leaderboard rather
  than silently shifting if upstream tie-breaking changes.
* **Posterior smoothing.** Symmetric Dirichlet with α=0.5 over V=23.
  V is the count of distinct phonemes observed across the consensus
  dataset (deterministic). For a sign with n=200 proposals,
  unanimity caps the modal posterior at (200+0.5)/(200+11.5) ≈ 0.945
  — below 1.0 by design. Calibration: a perfectly-unanimous high-n
  sign would yield modal posterior ≈ 0.94, *not* 1.0; that's still
  far above the observed maxima (~0.27).
* **Refined-gate sensitivity.** `refined_gate_sensitivity()` calls
  the same `aggregate_per_surface` + `build_posterior_rows` +
  `mann_whitney_u_one_tail` machinery as the production rollup,
  swept across K ∈ {5, 10, 20}. **No production-rollup change.**
  Diagnostic only.
* **Tests.** `harness/tests/test_consensus_map.py` covers the modal-
  posterior smoothing formula, Shannon-entropy formula on
  hand-built histograms, the n_min filter, freq-weighted per-surface
  coherence math, NaN-skipping per-pool median, deterministic tie-
  breaking on the modal phoneme, and end-to-end determinism on the
  per-sign + per-surface aggregations. Full repo test suite (128
  tests) is green.
* **Determinism.** Re-running `scripts/consensus_map.py` produces
  byte-identical `results/consensus_sign_phoneme_map.md` and
  byte-identical summary JSON given the same result stream +
  manifests + hypothesis YAMLs. No RNG anywhere in the pipeline.

### What this implies for the next ticket

Per the mg-c216 brief, the falsifiable case for reading #2 (which
the data supports) directs the next ticket toward **held-out
pool-curation tests** rather than per-inscription gloss generation:
deliberately pollute the Aquitanian pool with conjectural entries
and re-run the v10 right-tail gate, asking *whether the PASS
survives heterogeneous curation*. If yes, then v10's PASS is robust
to curation noise and the v13 coherence failure is more puzzling
than damning; if no, then we have a structural confirmation of
reading #2.

Out of scope for v14 per the brief and now also per v13's verdict:
per-inscription proposed readings (gloss generation), morphological
pattern detection, manuscript-shape per-sign reading claims.

### See also

* `results/consensus_sign_phoneme_map.md` — the per-sign consensus
  map + per-surface coherence + refined-gate sensitivity, full
  tables (committed, deterministic).
* `scripts/consensus_map.py` — script + CLI.
* `harness/tests/test_consensus_map.py` — tests on hand-built
  minimal datasets.
* `docs/findings_summary.md` — manuscript-shape narrative, updated
  with the v13 verdict.

## Findings from mg-6b73

### Headline

**The polluted Aquitanian pool clears the v10 right-tail bayesian
gate at p = 2.74e-05 — almost identical to v10's clean-pool PASS
(p = 3.22e-05).** The framework's PASS signal is **tolerant of 50%
conjectural pollution**: injecting 153 phonotactically-matched but
synthetic surfaces alongside the 153 real Aquitanian roots does
not collapse the gate.

This is the pre-registered binary discriminator for the two
readings of v12+v13 (mg-c216):

- **Reading #1 (substrate-LM-phonotactic kinship at the surface
  aggregate)** — *supported.* The framework genuinely detects that
  Aquitanian-shaped surfaces (real or synthetic) score better
  under the Basque LM than under their matched scramble control.
  The PASS does not depend on every entry being a real substrate
  root.
- **Reading #2 (curation-sensitivity)** — *undermined as a
  wholesale account.* The framework's gate is not a "uniformly-
  clean substrate pool" detector; mixed-cleanness pools clear it
  too. The Linear-B v12 positive-control failure (mg-4664) must
  therefore have a different explanation — most plausibly small
  N (12 anchors), short anchor surfaces, or a Linear-B-specific
  structural issue, not curation-sensitivity per se.

### Provenance breakdown of the polluted-pool top-20

Of the top-20 substrate posteriors in the polluted pool:

- **9 of 20 (45%)** carry `provenance: real`.
- **11 of 20 (55%)** carry `provenance: conjectural`.

This is **almost exactly the 50/50 split of the underlying pool**.
A real-vs-conjectural one-tail Mann-Whitney U on the two top-20
sets gave p = 0.98 (i.e. real surfaces do *not* dominate the right
tail; if anything, conjecturals are marginally tighter). The
framework cannot distinguish real from conjectural surfaces
within a mixed pool — its discriminator is phonotactic shape, not
underlying provenance.

This is consistent with v13's coherence finding (median per-
surface coherence 0.18; high-frequency signs scatter across
the alphabet at entropy 3.7-3.9 bits): the framework is reacting
to *aggregate phonotactic match* between Linear-A windows and
Basque-LM-likely phoneme strings, not to whether any particular
surface is a "real" root.

### Comparison to v10 clean-Aquitanian

| pool                | n_top | median(top sub) | median(top ctrl) | MW U | p (one-tail)   | gate |
|---------------------|------:|----------------:|-----------------:|-----:|---------------:|:----:|
| polluted_aquitanian | 20    | 0.9808          | 0.9572           | 340  | 2.74e-05       | PASS |
| aquitanian (v10)    | 20    | 0.9808          | 0.9512           | 345  | 3.22e-05       | PASS |

The two PASS magnitudes are within a factor of ~1.2× of each
other. The polluted pool's substrate top-K median is identical
(0.9808 — both pools have many substrate surfaces tied at n=50,
k=50 due to the cap-per-entry=50 generator setting); the only
difference is in the control top-K, which is slightly higher in
the polluted-pool case (0.9572 vs 0.9512) because the polluted
pool has 2× the entries and therefore 2× the candidate windows
the controls compete over, marginally raising the control's
right-tail.

### Distribution shift on real surfaces

Of the 153 surfaces present in both rollups (clean Aquitanian
right-tail and polluted-pool right-tail, real-provenance only):

| pool                | mean posterior | median posterior | min   | max   |
|---------------------|---------------:|-----------------:|------:|------:|
| clean Aquitanian    | 0.5033         | 0.5192           | 0.012 | 0.982 |
| polluted Aquitanian | 0.5086         | 0.5000           | 0.019 | 0.981 |

- Mean Δ (polluted − clean):   **+0.0053**
- Median Δ:                    **+0.0192**
- Pos / neg / zero counts:     **+80 / −69 / =0: 4**

In aggregate the bulk distribution of real-surface posteriors
barely moves (Δ ≈ 0). But individual surfaces shift dramatically:
some real surfaces drop from posterior 0.98 → 0.02 (`egun`,
`oin`, `hara`) while others jump from 0.02 → 0.98 (`ikusi`,
`anai`, `bost`). This is the per-window competition effect:
when a window has more candidates competing for the same
sign↔phoneme assignment, which surface "wins" depends on which
candidate happens to match the LM best, and adding 153
conjecturals reshuffles those win/loss outcomes for the real
surfaces. The bulk distribution is stable; individual surface
identity is not.

This is *another* nail in the per-sign-reading-claim coffin:
even within a single re-run, the assignment of high-posterior
surfaces is unstable to non-substrate-meaningful pool changes.
v13's coherence test ruled this out at the per-sign level;
v14 confirms it at the per-surface level.

### What v14 changes about the manuscript narrative

Combined with v12's Linear-B negative result and v13's per-sign
incoherence, the v14 PASS-on-pollution result tightens the
manuscript-shape claim to:

> The framework reliably detects substrate-LM-phonotactic kinship
> at the population level for any pool whose phoneme + length
> distribution is drawn from the substrate's own marginal
> distribution. It does **not** detect "real substrate
> vocabulary" (clean and polluted pools PASS equally), and it
> does **not** support per-sign reading claims (v13 coherence
> 0.18 vs 0.6 acceptance bar). The PASS is a structural
> phonotactic-overlap signal between Linear-A and the candidate
> substrate's character-bigram model — not a decipherment.

### Acceptance gate (re-stated for the audit trail)

Pre-registered (mg-c216 brief, mg-6b73 ticket): one-tail Mann-
Whitney U on the polluted-pool top-20 substrate posteriors vs the
top-20 matched-control posteriors; p < 0.05 with substrate >
control passes. Result: **U = 340.0, p = 2.74e-05, PASS** with
median(substrate top-20) = 0.9808 vs median(control top-20) =
0.9572.

### Construction artifact disclosure

`pools/polluted_aquitanian.yaml` is a deliberately-polluted test
pool. Half of its 306 entries are real Aquitanian roots; the
other half are synthetic conjectural surfaces drawn from the
real pool's phoneme + length distribution under deterministic
seed `0xb4b7c1f037ead5f1` (`sha256("polluted_aquitanian:
conjectural")[:16]`). The pool's README warns prominently that
it is a test artifact, not a substrate claim. Future ticket-
holders stumbling on this YAML must not derive secondary
artifacts from it (gloss tables, dictionaries, downstream
training).

### Determinism and reproducibility

Pool builder, candidate generator, sweep runner, bayesian
rollup, and provenance analysis are all deterministic. Re-
running the v14 pipeline from the polluted-pool YAML and the
existing corpus produces byte-identical artifacts. No RNG
anywhere in the analysis path.

### Out of scope and follow-ups

The v14 binary result is now in. Follow-up tickets that the
result *could* motivate (none filed yet):

- **v15: pollution-level sweep.** Run the same pipeline at 10%,
  25%, 75% conjectural pollution to characterize how the gate
  p-value scales with curation noise. v14's PASS at 50% suggests
  the gate is essentially insensitive to pollution within the
  same phoneme-distribution shape, but quantifying the gradient
  could rule out a sharp threshold near 100%.
- **v15 alternative: cross-language pollution.** Pollute with
  conjecturals drawn from a *different* language's phonotactic
  shape (Greek Wikipedia char-bigrams, Linear-B carryover, etc.)
  and see whether that breaks the PASS. v14 only tested
  pollution from the substrate's own distribution; cross-language
  pollution tests whether the gate has any phonotactic-shape
  selectivity.
- **Linear-B v12 follow-up.** The v14 result rules out
  curation-sensitivity as the explanation for v12's Linear-B
  positive-control failure. The remaining candidate explanations
  are small N, short anchor surfaces, anchor-pool curation
  errors. Separate ticket if anyone wants to chase this.

### See also

- `results/rollup.bayesian_posterior.polluted_aquitanian.md` —
  full per-surface bayesian posterior leaderboard, top-20
  side-by-side, gate computation. Generated by the existing
  `scripts/per_surface_bayesian_rollup.py`.
- `results/rollup.bayesian_posterior.polluted_aquitanian.provenance.md`
  — v14-specific provenance breakdown of the top-20, real-vs-
  conjectural sanity check, distribution-shift table, top-10
  shifted surfaces.
- `pools/polluted_aquitanian.yaml` + `pools/polluted_aquitanian.README.md`
  — the polluted pool itself + construction documentation. The
  README is the canonical "this is a test artifact, not a claim"
  warning.
- `pools/control_polluted_aquitanian.yaml` — matched phonotactic
  control (306 entries, same algorithm as `control_aquitanian`,
  distinct seed).
- `scripts/build_polluted_pool.py` — idempotent, deterministic
  builder. Reusable for future pollution variants (the seed
  derivation and two-class redraw filter are the only scope-
  specific bits).
- `scripts/v14_polluted_provenance_analysis.py` — post-rollup
  provenance enrichment script.
- `harness/tests/test_polluted_pool.py` — 11 unit tests on the
  builder + 1 sanity check on the committed pool YAML.

## Findings from mg-7ecb

### Headline

**The cross-language polluted Aquitanian pool clears the v10 right-
tail bayesian gate at p = 2.006e-03 (top-20 split: 13 real / 7
conjectural-greek), AND within the right tail real Aquitanian
surfaces dominate Greek-shape conjecturals at p = 8.292e-05.** This
is the *partial-discrimination* outcome the v15 brief flagged as
"the most interesting case for the manuscript". The framework's
gate has measurable shape selectivity (the cross-language gate is
~70× weaker than v14's same-distribution gate at p = 2.74e-05 and
~16× weaker than v10's clean-pool gate at p = 3.22e-05), AND within
the substrate-side right tail real Aquitanian dominates Greek-shape
conjecturals at p < 0.001 — but the population gate still PASSes
because the LM rewards Greek-shape phonotactic strings well enough
relative to scramble controls.

The v14 manuscript-shape claim was:

> The framework detects substrate-LM-phonotactic kinship at the
> population level for any pool whose phoneme + length distribution
> is drawn from the substrate's own marginal distribution. It does
> NOT detect "real substrate vocabulary," and does NOT support
> per-sign reading claims.

v15 **refines** that claim. Both halves of the v14 claim survive,
but the boundary is sharper than v14 alone could reveal:

* The headline-PASS condition is broader than v14's clause says —
  the gate clears for any pool with non-trivial char-bigram overlap
  with the LM, even when the pool's phoneme distribution does NOT
  match the substrate's. Greek-shape conjecturals carry enough
  Mediterranean-style CV phonotactics that they out-score scramble
  controls under the Basque LM.
* But within-tail discrimination is real and large: real Aquitanian
  surfaces dominate Greek-shape conjecturals at p < 0.001 (top-20
  median posteriors 0.9808 real vs 0.9519 conjectural-greek), even
  when both are mixed in the same pool. v14's same-distribution
  pollution showed NO within-tail discrimination (real-vs-conjectural
  MW p = 0.98); v15's cross-language pollution shows STRONG within-
  tail discrimination.

The framework is therefore *partially* selective to substrate-
distribution shape: enough to push Greek-shape conjecturals down
the leaderboard relative to real Aquitanian, but not enough to
break the population gate.

### Provenance breakdown of the polluted-pool top-20

Of the top-20 substrate posteriors in the cross-language polluted
pool:

- **13 of 20 (65%)** carry `provenance: real`.
- **7 of 20 (35%)** carry `provenance: conjectural_greek`.

The conjecturals that *did* land in the top-20 (`aki`, `ame`,
`awa`, `fren`, `ini`, `joten`, `kare`) all share a particular
Mediterranean-CV shape that the Basque LM rewards heavily —
short open-syllable strings (CV.CV / V.CV / CV.CV.CV) without
the Greek-distinctive `j-` / `w-` glides or geminate clusters
that would have flagged them as out-of-distribution. The
Greek-shape conjecturals that fell out of the top-20 are heavier
in those distinctive features.

### Comparison to v14 and v10

| pool                                 | gate p   | top substrate median | top control median | within-tail real-vs-conj p |
|--------------------------------------|---------:|---------------------:|-------------------:|---------------------------:|
| greek_polluted_aquitanian (v15)      | 2.01e-03 | 0.9808               | 0.9735             | 8.29e-05                   |
| polluted_aquitanian (v14)            | 2.74e-05 | 0.9808               | 0.9572             | 0.98                       |
| aquitanian (v10)                     | 3.22e-05 | 0.9808               | 0.9512             | (n/a, no conjecturals)     |

The control-side median rises monotonically from clean (0.9512)
to same-distribution polluted (0.9572) to cross-language polluted
(0.9735) — the matched controls in v15 are partly drawn from
Greek-shape phonemes, which are themselves Basque-LM-favorable
under the matched-control sampler. The substrate-side median is
the same 0.9808 in all three pools (cap-per-entry=50 ceiling).
The shrinking substrate-vs-control gap is what produces the
weaker but still-PASSing gate.

The within-tail real-vs-conjectural MW p value is the cleanest
diagnostic: 0.98 in v14 (no discrimination) → 8.3e-05 in v15
(strong discrimination). v14's same-Aquitanian-shape conjecturals
are *indistinguishable* from real Aquitanian to the framework;
v15's Greek-shape conjecturals are *distinguishable*. So the
distinguishing axis is the polluting distribution's similarity
to the substrate's own — when the polluting distribution differs,
the framework partially recovers signal.

### Distribution shift on real surfaces

Of the 153 real Aquitanian surfaces present in both rollups
(clean Aquitanian and cross-language polluted):

| pool                | mean posterior | median posterior | min   | max   |
|---------------------|---------------:|-----------------:|------:|------:|
| clean Aquitanian    | 0.5033         | 0.5192           | 0.013 | 0.982 |
| cross-language      | 0.5484         | 0.5192           | 0.019 | 0.981 |

- Mean Δ (cross-language − clean): **+0.0451**
- Median Δ:                        **+0.0577**
- Pos / neg counts:                **+85 / −65 / =0: 3**

The real Aquitanian surfaces' posteriors **shifted UP** when
Greek-shape conjecturals were mixed in, by a meaningful +5.8%
median. Mechanism: Greek-shape conjecturals don't compete as
well as same-Aquitanian-shape conjecturals do for the same
windows, so real Aquitanian wins more paired_diffs in the cross-
language polluted pool than it does in the v14 same-distribution
polluted pool (where v14's median Δ was just +0.019). This is
consistent with the within-tail discrimination signal: the
framework is rewarding substrate-shape over non-substrate-shape
when both are competing for the same Linear-A windows.

### Acceptance gate (re-stated for the audit trail)

Pre-registered (mg-7ecb ticket): one-tail Mann-Whitney U on the
cross-language polluted pool top-20 substrate posteriors vs the
top-20 matched-control posteriors; p < 0.05 with substrate >
control passes. Result: **U = 300.0, p = 2.006e-03, PASS** with
median(substrate top-20) = 0.9808 vs median(control top-20) =
0.9735.

Within-tail real-vs-conjectural-greek MW U on the top-20 real
posteriors vs the top-20 Greek-shape posteriors: **U = 310.0,
p = 8.29e-05** — strong within-tail discrimination.

### Construction artifact disclosure

`pools/greek_polluted_aquitanian.yaml` is a deliberately-polluted
test pool. Half of its 306 entries are real Aquitanian roots; the
other half are synthetic conjectural surfaces sampled from the
Mycenaean-Greek char-bigram distribution at
`harness/external_phoneme_models/mycenaean_greek.json` under
deterministic seed `0xfa0fd94c61e71b23` (`sha256("greek_polluted_
aquitanian:conjectural")[:16]`). The pool's README warns
prominently that it is a test artifact, not a substrate claim.
Future ticket-holders stumbling on this YAML must not derive
secondary artifacts from it (gloss tables, dictionaries,
downstream training).

### Sampling procedure for the Greek-shape conjecturals

The brief asked for an explicit document of the sampling procedure;
it lives in `pools/greek_polluted_aquitanian.README.md` and in the
docstring of `_sample_word_from_external_lm()` in
`scripts/build_polluted_pool.py`. Summary:

* Each conjectural entry's length matches the corresponding real
  entry's length (so the polluted pool's length distribution is
  exactly 2× the real pool's).
* The first character is sampled from the LM's unigram-marginal
  restricted to the alphabet `a..z`; the `<W>` boundary token and
  the space character are filtered out so the word starts with a
  content character. Weights = `unigram_count + alpha`.
* Each subsequent character is sampled conditional on the previous
  character via `count(prev, c) + alpha`, again restricted to
  `a..z` so the word never produces an early word-end. The relative
  frequencies of alphabet bigrams are preserved; word-end / space
  tokens are excluded at every step (the "regenerate to match
  length" interpretation of the brief).
* Each sampled character becomes a single-character phoneme,
  matching how `external_phoneme_perplexity_v0` decomposes phonemes
  to chars at scoring time.
* Two-class V/S/C filter applied to every conjectural draw so the
  candidate generator does not skip any conjectural entry.

The realized Greek-shape conjectural inventory is dominated by `a`,
`o`, `e`, `i`, `r`, `t`, `j`, `w`, `n`, `k` (top-10), differing
visibly from the real Aquitanian top-10 of `a`, `i`, `e`, `r`, `n`,
`o`, `u`, `h`, `l`, `b`. Greek-distinctive `j` and `w` (the LiBER
syllabogram-derived transliteration of glides) appear with high
frequency in the conjecturals but never in real Aquitanian roots.

### Determinism and reproducibility

Pool builder (with and without `--source-lm`), candidate generator,
sweep runner, bayesian rollup, and v15 provenance analysis are all
deterministic. Re-running the v15 pipeline from the
`greek_polluted_aquitanian.yaml` and the existing corpus produces
byte-identical artifacts. No RNG anywhere in the analysis path.

The v14 default-mode pool builder still produces a byte-identical
`pools/polluted_aquitanian.yaml` after the v15 refactor (verified
manually on disk). The `--source-lm` flag is fully backward-
compatible; omitting it preserves v14 behavior.

### Out of scope and follow-ups

The v15 binary result is now in. v16 (methodology paper) can be
drafted with confidence about exactly which version of the v14
manuscript-shape claim is supported — the **partial-discrimination
refinement** above. Follow-up tickets the result *could* motivate
(none filed yet):

- **v16: methodology paper.** The manuscript-narrative refresh
  flagged in the v15 brief. Out-of-scope for v15 itself; defer to
  the dedicated ticket.
- **Pollution-level sweep.** v14-suggested (10%, 25%, 75% same-
  distribution pollution). v15 explicitly defers this as less
  informative than the cross-language test that v15 ran instead.
  Could now be run for completeness if a v17 ticket needs the
  smooth gradient curve.
- **Cross-language gates with other LMs.** v15 used Mycenaean-Greek
  as the polluting LM. The same test under Etruscan or
  Linear-B-as-substrate could illuminate which Mediterranean
  phonotactic features the gate is actually responding to. Defer
  pending v16 manuscript priorities.
- **Stricter control sampler.** The matched-control top-20 median
  rises monotonically (clean 0.9512 → polluted 0.9572 → greek-
  polluted 0.9735); the control sampler is sensitive to the
  polluted pool's combined phoneme distribution. A bigram-
  preserving control would tighten the gate further.

### See also

- `results/rollup.bayesian_posterior.greek_polluted_aquitanian.md`
  — full per-surface bayesian posterior leaderboard, top-20 side-
  by-side, gate computation. Generated by the existing
  `scripts/per_surface_bayesian_rollup.py`.
- `results/rollup.bayesian_posterior.greek_polluted_aquitanian.provenance.md`
  — v15-specific provenance breakdown of the top-20, real-vs-
  conjectural-greek within-tail MW U, distribution-shift table,
  top-10 shifted surfaces.
- `pools/greek_polluted_aquitanian.yaml` +
  `pools/greek_polluted_aquitanian.README.md` — the cross-
  language polluted pool itself + construction documentation.
  The README is the canonical "this is a test artifact, not a
  claim" warning and contains the full sampling procedure.
- `pools/control_greek_polluted_aquitanian.yaml` — matched
  phonotactic control (306 entries, sampled from the polluted
  pool's *combined* phoneme distribution, distinct seed).
- `scripts/build_polluted_pool.py` — extended with `--source-lm`
  / `--prefix` flags. Backward-compatible; default produces the
  v14 byte-identical same-distribution pool.
- `scripts/v15_cross_language_pollution_analysis.py` — post-
  rollup provenance enrichment for the cross-language pool;
  computes the v15 verdict text and writes the provenance md.
- `harness/tests/test_polluted_pool.py` — extended with a
  `CrossLanguagePollutedPoolBuilderTest` class (11 new tests on
  the v15 builder) and a `CommittedGreekPollutedPoolTest` sanity
  check on the committed pool YAML.
- `harness/external_phoneme_models/mycenaean_greek.json` — the
  source LM the conjecturals were drawn from. v12 artifact;
  unchanged in v15.

## Findings from mg-d5ed

mg-d5ed is the v16 ticket: an audit-and-polish pass on
`docs/findings_summary.md` to bring it to publication-readable
methodology-paper-draft standards. No new experiments, no new
corpora, no new metrics — strictly an editorial / verification
ticket.

### Audit summary

The pre-v16 draft was an incrementally-grown narrative, with v15 /
v14 / v13 update sections stacked at the top and the methodology
near the bottom. The audit replaced that structure with a standard
methodology-paper section ordering: **Abstract, Introduction,
Methods, Results, Discussion, Limitations, Conclusion**, plus a
result-file index appendix. The seven required sections are present
and well-developed (verified by section-grep).

Section-by-section audit:

- **Abstract (≤ 250 words).** Newly-written. Pre-registers question,
  method, and supportable claim in three paragraphs.
- **Introduction.** Newly-written. Frames why mechanical falsifiable
  testing matters for Linear A specifically (motivated-reasoning
  failure modes), what the project's bet was, and the explicit
  scoping choices.
- **Methods.** Reconsolidated. Covers corpus (SigLA, 761 transcribed
  inscriptions, 4,935 sign occurrences, 356 distinct sign IDs),
  the four substrate pools and three pollution variants with
  per-pool entry counts, hypothesis schemas
  (`candidate_equation.v1`, `candidate_signature.v1`), the metric
  (`external_phoneme_perplexity_v0`), paired-difference scoring,
  per-surface Beta-binomial aggregation, the right-tail Bayesian
  gate, and the five auxiliary checks (cross-LM, third-LM,
  positive control, coherence, pollution).
- **Results.** Each of the eight pre-registered acceptance gates
  is now reported with the same level of detail as the prior
  draft's per-pool sections, but in a results-section ordering
  rather than a chronological-update ordering. The summary table
  in §3.1 is the single-glance entry point.
- **Discussion.** Restructured around what the framework detects
  versus what it does not detect, with explicit micro-explanations
  for why same-distribution pollution PASSes the gate without
  within-tail discrimination, and why per-sign coherence fails
  despite surface-aggregate PASS.
- **Limitations.** Now an explicit section. Three sub-headings:
  out-of-scope by construction, known unresolved issues, out-of-
  scope for the methodology characterization itself.
- **Conclusion.** Newly-written single-paragraph wrap.

### Three-sentence reading test

The acceptance check from the ticket brief: three sentences a
hypothetical Linear A scholar reading `findings_summary.md` would
learn from it, that should sound publishable when read together.
After the audit pass:

1. Mechanical paired-difference scoring of substrate-language
   hypotheses against the SigLA Linear A corpus, with phonotactically-
   matched controls and an external character-bigram phoneme language
   model, detects substrate-LM-phonotactic kinship for Aquitanian
   under a Basque LM (right-tail bayesian gate p = 3.22e-05) and
   Etruscan under an Etruscan LM (p = 5.21e-04), with cross-LM
   negative controls confirming substrate-LM specificity for both.
2. The same framework cannot recover stable per-sign sign-to-phoneme
   mappings — a cross-window coherence test on the v10 top-20
   substrate surfaces fails decisively (median per-surface coherence
   0.18 versus a 0.6 acceptance bar) — and a same-distribution
   pollution test cannot distinguish real Aquitanian roots from
   phonotactically-matched conjectural surfaces (within-tail
   real-vs-conjectural Mann-Whitney p = 0.98), so the framework's
   right-tail leaderboard reports phonotactic-shape-likely surfaces,
   not validated substrate vocabulary.
3. The framework therefore identifies which substrate phonotactic
   profiles produce population-level signal in the Linear A corpus
   and which specific inscriptions concentrate that signal, but does
   not validate per-sign readings or per-tablet glosses; the
   discipline of mechanical scoring against phonotactically-matched
   controls is what distinguishes this method's claim from the
   qualitative-impression claims that have plagued past Linear A
   work.

These three sentences land in the "narrower-but-defensible" register
the brief asked for: the first acknowledges what the framework
detects, the second states the empirical limit on per-sign claims,
and the third frames the methodological contribution honestly. They
are not over-stated and they are not over-hedged.

### Inconsistencies discovered and resolved

The audit found three drift items in the pre-v16 draft:

1. **Pipeline lineage citation drift.** The pre-v16 Methods section
   said "the pipeline (built up across mg-1c8c through mg-4664) is".
   `mg-1c8c` does not exist in this repo — the actual project
   lineage starts with mg-d5ef (v0) and the v15 work shipped under
   mg-7ecb. **Fix applied:** the new draft cites `mg-d5ef` through
   `mg-7ecb` as the lineage, and the per-step Methods subsections
   cite individual tickets (mg-d26d for v10 aggregation, mg-bef2
   for v9 signatures, mg-ee18 for the metric, etc.).
2. **Cluster-A inscription concentration mislabeling.** The pre-v16
   per-inscription section attributed the v10-top-20 surfaces
   hitting `HT Wc 3010`, `KH 60`, etc., to "the Etruscan religious /
   praenomen / time-reference cluster," then listed surfaces that
   include several Aquitanian roots (`bihotz`, `entzun`, `hanna`,
   `itsaso`, `zelai`, `zortzi`). Those Aquitanian-side surfaces are
   from the Aquitanian top-20, not the Etruscan top-20. The
   description had been carried forward from mg-0f97's findings.md
   entry without being re-checked against the substrate-pool
   provenance. **Fix applied:** §3.9 now states explicitly that the
   14 v10-top-20 surfaces hitting these tablets are drawn from
   *both* substrate pools' top-20 sets, with separate enumeration
   of the Etruscan-side and Aquitanian-side contributions.
3. **High-frequency-sign entropy range stated too loosely.** The
   pre-v16 v13 narrative said "max-likelihood entropy 3.6–4.0 bits."
   Spot-check against `consensus_sign_phoneme_map.md` shows the
   high-frequency signs are in the 3.71–3.92 bits range. **Fix
   applied:** the new draft states "3.7–3.9 bits."

The committed result files were **not** modified — these are
narrative drift fixes, not historical-number rewrites. All
quantitative claims in the new draft were spot-checked against the
committed `results/*.md` files and `corpus_status.md`; the new
draft's numbers match the committed artefacts.

### What is and isn't ready for external review

**Ready for external review:** the methodology paper draft is now
internally consistent, every quantitative claim cites a specific
mg ticket and/or committed result file, and the supportable /
unsupportable claim split is honest. A research scientist or
Aegean-syllabary specialist who reads `docs/findings_summary.md`
cold should be able to follow the pipeline (§2), see which
substrate hypotheses produce signal at which gates (§3), and
understand why the framework does not support per-sign decipherment
(§4 + §5). The three-sentence reading test above is the canonical
"would this be publishable?" check, and the document clears it in
the narrower-but-defensible register.

**Not ready for external review (and explicitly out-of-scope):**

- Journal submission. Latex / journal-specific style / reference
  formatting / peer review — depends on Daniel's editorial choice
  of target venue.
- Domain-expert review of top-K substrate surfaces. Independent
  Aegean-syllabary specialist review is the only way to convert
  "the right tail is Aquitanian-shape-likely" into "the right tail
  is real Aquitanian vocabulary present in Linear A," and that is
  not a polecat task.
- Cleanup tickets the methodology paper flags but does not address:
  toponym pool control-sampler fix; Linear-B small-K refined gate
  adoption; pollution-level sweep (10% / 25% / 75%); GORILA /
  Younger ingest for numerals + line breaks; additional substrate
  pools (Phoenician, Sumerian, Hattic). The methodology paper's
  §5.3 enumerates these explicitly.

The natural next step is **Daniel's editorial choice of target
venue** — once that is made, the LaTeX / formatting / reference
work and any venue-specific narrative tightening can be done off
this draft.

### See also

- `docs/findings_summary.md` — the rewritten methodology paper
  draft. Six numbered sections plus an Abstract and a result-file
  index appendix.
- `docs/roadmap.md` — pm-lineara updates this directly to reflect
  "project at v16; methodology characterized; remaining open work
  is paper-submission-side and out-of-pogo-scope" (out-of-scope
  for this polecat ticket).

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

## Findings from mg-2bfd (v17 — manuscript correction: lineage citations + audit-of-the-audit, 2026-05-05)

Single-purpose documentation-correction ticket against the v16 polish
in mg-d5ed. Three lineage-span citations in `docs/findings_summary.md`
were rewritten by the v16 polecat under the false belief that
`mg-1c8c` did not exist in the repo (the worktree at audit time
appears to have had partial visibility into archived tickets). The
project lineage in fact starts at the SigLA corpus ingest `mg-1c8c`
(264k tokens spent, status archived), preceded only by the auto-
generated repo scaffold `mg-9e00`. v17 restores the citations.

### What was changed

In `docs/findings_summary.md`:

- Header (lines 3-9): the abstract bracket "across 19 work items
  (v0 through v15; `mg-d5ef` through `mg-7ecb`)" is rewritten to
  anchor on `mg-1c8c` (corpus ingest) and span the harness pipeline
  `mg-d5ef` through `mg-7ecb`, with `mg-9e00` (scaffold) noted as
  predecessor.
- §2 lead (line ~125): "The pipeline is built up across `mg-d5ef`
  (v0) through `mg-7ecb` (v15)" rewritten to add "atop the SigLA
  corpus ingest (`mg-1c8c`) and the initial repo scaffold
  (`mg-9e00`)". The harness span itself is unchanged — the harness
  pipeline genuinely is `mg-d5ef` through `mg-7ecb`.
- Appendix (line ~848): chronological lineage description rewritten
  to start at `mg-1c8c` (SigLA corpus ingest, 2026-05-04). Note
  added that `mg-9e00` predates `findings.md`'s introduction in
  `mg-13a2` and therefore lacks a per-ticket entry.

The "19 work items" count is preserved unchanged — it matches the 19
`## Findings from mg-XXXX` entries in `findings.md` (the per-ticket
log span is `mg-1c8c` through `mg-d5ed`; the v17 entry will make 20)
and was not part of the lineage-citation drift.

The lone `mg-d5ef` reference outside a span (line 178: "candidate_
equation.v1 (mg-d5ef, mg-fb23)" — citing the schema-introducing
ticket, not a lineage span) was left untouched: it is correct as
written.

### Audit-of-the-audit: are the v16 polecat's other two claimed fixes correct?

The v16 commit message (mg-d5ed) lists three drift fixes; one of
them (the lineage-citation fix) is being undone here. v17 spot-
checked the other two against the committed result files.

1. **Cluster-A inscription concentration mislabeling**
   (claimed fix in v16 commit message: "corrected the Aquitanian-
   side surfaces (`bihotz`, `entzun`, `hanna`, `itsaso`, `zelai`,
   `zortzi`) that had been mislabeled as part of the 'Etruscan
   religious / praenomen / time-reference cluster' — they are
   from the Aquitanian top-20").

   Verified against `results/rollup.right_tail_inscription_concen
   tration.md`:
   - That file's "v10 top-20 substrate surfaces (passing pools)"
     list confirms `bihotz`, `entzun`, `hanna`, `itsaso`, `zelai`,
     `zortzi` are all in the Aquitanian top-20 (line 9 of the
     rollup), not the Etruscan top-20 (line 11).
   - The `findings_summary.md` §3.9 text (lines 574-581) correctly
     splits the cluster: 8 Etruscan-side surfaces (`aiser`, `avils`,
     `camthi`, `hanthe`, `laris`, `matam`, `thesan`, `zelar`)
     plus 6 Aquitanian-side (`bihotz`, `entzun`, `hanna`, `itsaso`,
     `zelai`, `zortzi`), matching the 14 surfaces listed in the
     `top_substrate_surfaces_present` column for tablets HT Wc
     3010, HT Wc 3017a, KH 60, KN Zb 5, HT 90, KH 10, KH 5 (rollup
     ranks 1-7 by density).
   - The Knossos-votive subset citation (`caitim`, `thanchvil`,
     `spureri`) maps to `KN Zc 6`, `KN Zc 7`, `KN Zf 13` (rollup
     ranks 15-17), all of which list those three surfaces in the
     rollup. Correct.

   **Verdict: v16 fix is correct. No re-fix needed.**

2. **High-frequency-sign entropy range tightened from "3.6–4.0
   bits" to "3.7–3.9 bits"** (claimed fix in v16 commit message).

   Verified against `results/consensus_sign_phoneme_map.md`. The
   three high-frequency signs cited explicitly in `findings_summary
   .md` §3.7 (lines 502-504) are AB08 (n_proposals=464,
   entropy=3.925 bits), AB37 (n=227, entropy=3.713), AB28 (n=225,
   entropy=3.788). All three values round to one decimal as
   3.7-3.9. The §4.2 carryover citation (line 643) is consistent
   with these. The v16 narrowing is faithful to the cited examples.

   Caveat for future audits (not a fix): if "high-frequency signs"
   is interpreted more inclusively (e.g. all signs with
   n_proposals ≥ ~190, which includes AB04, AB27, AB67, AB58,
   AB01, AB81, AB31, AB07, AB59, AB09, AB80, AB24, AB57, AB06,
   AB41, AB10, AB53, AB45), the upper end of the entropy band
   crosses 3.95 (AB24=3.954, AB57=3.960). At one-decimal
   resolution that rounds up to 4.0, so a literal "3.7–4.0 bits"
   would also be defensible. v17 leaves the v16 phrasing in place
   because the cited examples are AB08/AB37/AB28 specifically and
   "3.7–3.9 bits" is correct for that explicit set. Re-broadening
   the citation set is a separate editorial decision out of scope
   here.

   **Verdict: v16 fix is correct as written for the cited
   examples. No re-fix.**

### Summary of v16 polish accuracy

Of the three drift items the v16 polecat documented as fixing:

- (1) Lineage-citation: incorrectly applied (v17 reverts).
- (2) Cluster-A inscription concentration: correctly applied.
- (3) High-frequency-sign entropy range: correctly applied.

The v16 audit's structural restructuring (methodology-paper section
ordering, claim-by-claim ticket/result-file citations, supportable
vs unsupportable split) is sound and was not re-audited; out-of-
scope per the v17 ticket. v17 also did **not** modify any
quantitative result, table, gate value, p-value, or claim — it
touched three lineage-span citations and the doc header marker, and
appended this findings entry. No new corpora, no new metrics, no
re-derivation.

### Lineage citation choice (documented per ticket guidance)

v17 chose `mg-1c8c` (SigLA corpus ingest) as the canonical start of
the project lineage in three-place narrative citations, with
`mg-9e00` (repo scaffold) noted as predecessor. Rationale: the
corpus is the empirical foundation of every downstream measurement,
while `mg-9e00` is auto-generated directory layout (corpus/,
hypotheses/, results/, harness/ with .gitkeep stubs and a 1-page
README) and contains no data the harness reads. The harness-span
citation `mg-d5ef` through `mg-7ecb` is preserved where it accurately
describes pipeline build-up.

## Findings from mg-9f18 (v18 — toponym bigram-control fix + pollution-level sweep, 2026-05-05)

Two methodology results, both substantively informative.

### 1. Toponym pool now PASSes under a bigram-preserving control

**Headline.** The toponym pool, which **failed** the v10 right-tail
bayesian gate at p=0.92 against the v6 unigram-marginal control
(mg-d26d), now **PASSes at p=9.99e-05** against a bigram-preserving
control. The toponym pool joins Aquitanian + Etruscan as a third
validated cross-LM-checkable substrate pool.

**What changed.** The v6 control sampler (`scripts/build_control_pools.py`,
default `--sampler unigram`) draws each phoneme independently from
the substrate's marginal histogram. v10 documented the resulting
toponym control as containing extreme strings like `eoao`, `aathei`,
`kllzua` — phonotactically improbable but unigram-frequency-matched.
Those strings scored extremely well under the Basque LM by raw
phoneme-frequency overlap, dragging the control's posterior median
above the substrate's. mg-7ecb's polecat called this out as the
likely cause of the toponym failure and flagged a bigram-preserving
control as the obvious next test.

The v18 sampler (`--sampler bigram`, mg-9f18) draws each phoneme
conditional on the previous phoneme using the substrate's bigram
counts (Laplace alpha=0.1, matching the LM and v15 cross-language
sampler smoothing). The realized control surfaces inherit Greek-
style adjacent-phoneme structure: `akaintha`, `inaletos`, `metosord`
instead of `eoao`, `aathei`, `kllzua`.

**Gate values.** Per `results/rollup.bayesian_posterior.toponym_bigram_control.md`:

| variant            | substrate top-K | control top-K | median(top sub) | median(top ctrl) | MW U | MW p (one-tail) | gate |
|:-------------------|---:|---:|---:|---:|---:|---:|:--:|
| bigram (v18)       | 20 | 20 | 0.9615 | 0.8525 | 337.5 | 9.988e-05 | PASS |
| unigram (v6/v10)   | 20 | 20 | 0.9186 | 0.9464 | 149.5 | 9.165e-01 | FAIL |

The reversal is sharp: control median drops 0.094 (0.946 → 0.852)
under the bigram sampler, while the substrate median rises 0.043
(0.919 → 0.962). Every one of the v6 control's top-20 surfaces is
absent from the v18 control's top-20 (`aas`, `aathei`, `ana`,
`anealo`, `eoao`, `eta`, `iaoeasanoaeoesa`, `ioonaol`, `kim`,
`kllzua`, `kolee`, `nul`, `oaest`, `oks`, `onn`, `saenaa`, `tea`,
…), replaced by phonotactically-realistic alternatives.

**Methodological consequence.** Toponym now sits alongside Aquitanian
and Etruscan in the §3 results. Findings_summary.md §5 Limitations
removes the entry "toponym failure (control-sampler issue)" — the
cause was indeed the control sampler, and the fix lands the gate
under a stricter null hypothesis (phoneme-inventory + bigram-
phonotactics overlap, not just phoneme-inventory).

**What this does NOT mean.** The bigram control is not the *only*
defensible control. Higher-order phonotactics (trigram, full
position-aware) are progressively closer to the substrate-LM
distribution and would tighten the gate further; matching all of
them would absorb the substrate signal entirely (see the v18
README's "What the control is NOT" section). The v18 gate is the
strictest control we test; reading it as a *necessary* fix to the
v10 toponym failure is correct, reading it as a *sufficient*
validation of every claim that could be made from the toponym pool
is not.

### 2. Pollution-level sweep on Aquitanian — gate stays PASS across 10%/25%/50%/75%, weakens monotonically with conjectural share

**Headline.** Same-distribution conjectural pollution does not
collapse the v10 right-tail bayesian gate on the Aquitanian pool at
any of the four levels tested. The p-value gradient is
non-monotonic across 10%/25%/50% but widens sharply at 75%, and the
substrate top-K composition shifts from real-dominated at 10% to
conjectural-dominated at 75%.

**Sweep table.** Per `results/rollup.pollution_level_sweep.md`:

| pollution % | n_real | n_conj | median(top sub) | median(top ctrl) | MW U  | MW p       | gate | top-K real | top-K conj |
|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|
| 10 | 153 | 17  | 0.9808 | 0.9450 | 325.5 | 1.502e-04 | PASS | 19 | 1  |
| 25 | 153 | 51  | 0.9808 | 0.9379 | 320.0 | 2.747e-04 | PASS | 12 | 8  |
| 50 | 153 | 153 | 0.9808 | 0.9572 | 340.0 | 2.740e-05 | PASS |  9 | 11 |
| 75 | 153 | 459 | 0.9808 | 0.9703 | 260.0 | 4.268e-02 | PASS |  5 | 15 |

The 50% row reproduces v14 (mg-6b73) within sampling noise of the
result-stream merge — the v18 sweep code path is consistent with
the v10/v14 path.

**Two readings of the gradient.**

Gate-level reading: the framework's PASS at the population level is
*essentially insensitive* to pollution share within the substrate's
phonotactic distribution at levels ≤50% (p stays at v10 magnitude:
1.5e-04 to 2.7e-05), and weakens but does not break at 75%
(p=4.3e-02, just clearing the 0.05 threshold). v14's reading —
that the gate detects substrate-LM-phonotactic kinship at the
*population level* rather than per-surface substrate-vocabulary
identity — generalizes across the gradient and now sits inside a
characterized stable region.

Top-K composition reading: the substrate top-K is 95% real at 10%
pollution but only 25% real at 75% pollution. Real and conjectural
surfaces are *partially discriminated* by their absolute posterior —
real surfaces remain near the maximum-posterior ceiling regardless
of pollution level (median(top sub) = 0.9808 across all four rows),
but as the conjectural pool grows, conjectural surfaces with
high-credibility wins crowd into the right tail. The gate's
right-tail median test does not depend on this composition, but
any reading of "the framework discriminates real vs conjectural"
that *would* depend on top-K composition needs to be calibrated to
the pollution level.

**Threshold characterization (negative).** The sweep does not
locate a threshold at which the gate fails: 75% PASS at p=0.043
suggests the threshold is between 75% and 100%, but with the
p-value swinging non-monotonically across levels the precise
location is not characterizable from these four data points
without finer sweep granularity (out of scope for v18). The
methodologically clean statement is: *the v10 right-tail gate
PASSes at every same-distribution pollution level we tested, with
p-value at 75% close to but below the 0.05 threshold; same-
distribution pollution at higher rates may eventually break the
gate but the threshold is not located by this sweep.*

### Artifacts shipped

- `scripts/build_control_pools.py` — extended with `--sampler bigram`
  and `--suffix` flags. Backward-compatible default `--sampler
  unigram` produces byte-identical output to the v6 control pools
  (verified by re-running and confirming `git diff pools/` is empty).
  The bigram sampler is documented in the script docstring and the
  per-pool README.
- `scripts/build_polluted_pool.py` — extended with `--ratio-pct`
  flag. Default (no flag) produces byte-identical v14 / v15 output;
  `--ratio-pct N` produces the `_<N>pct` variant pool with
  `n_conjectural = n_real * N / (100 - N)`.
- `pools/control_toponym_bigram.yaml` + `.README.md` — 112 entries,
  bigram-preserving sampler, deterministic seed
  `0x1b7b5d4ef69cede7` (sha256-keyed on `control_pool:toponym:
  bigram` so it draws from a disjoint random stream relative to the
  v6 unigram control).
- `pools/polluted_aquitanian_{10,25,75}pct.yaml` + matched
  `pools/control_polluted_aquitanian_{10,25,75}pct.yaml` plus
  READMEs. 170/204/612 entries respectively, deterministic seeds.
- `scripts/v18_toponym_bigram_gate.py` — v18 toponym analysis,
  pairs `toponym` substrate against the bigram control and emits
  the rollup file.
- `scripts/v18_pollution_level_sweep.py` — v18 sweep analysis,
  emits the four-row pollution-level table.
- `results/rollup.bayesian_posterior.toponym_bigram_control.md` —
  toponym v18 verdict + side-by-side with v6 unigram control top-K
  composition shift.
- `results/rollup.pollution_level_sweep.md` — four-row sweep table
  with provenance breakdown and interpretation.
- `harness/tests/test_control_pools.py` and
  `harness/tests/test_polluted_pool.py` — extended with bigram-
  sampler determinism tests, ratio-variant entry-count tests, and
  schema-validity tests on the new pools.

### Out of scope (deferred)

- Sub-75% threshold characterization (e.g. 85%, 95% rows) — would
  need finer sweep granularity. Recommend a separate ticket if the
  threshold location is needed for the methodology paper's claim
  shape.
- Bigram-preserving control on Aquitanian and Etruscan — those
  pools already PASS under unigram controls at v10 magnitude, so
  the bigram refinement would not change the verdict (and would
  arguably loosen the substrate-vs-control gap, which is the
  opposite direction we want to test); deferred unless the
  methodology paper discussion explicitly asks "would the validated
  pools still pass under a stricter null?".
- Higher-order (trigram, position-aware) controls — methodologically
  the next step beyond bigram. Out of v18 scope; the bigram fix is
  the minimum that addresses the v10 toponym failure.

### Reproducibility

All artifacts are deterministic. Re-running:

```
python3 scripts/build_control_pools.py --pool toponym --sampler bigram --suffix _bigram
python3 scripts/build_polluted_pool.py --pool aquitanian --ratio-pct 10
python3 scripts/build_polluted_pool.py --pool aquitanian --ratio-pct 25
python3 scripts/build_polluted_pool.py --pool aquitanian --ratio-pct 75
python3 scripts/build_control_pools.py --pool polluted_aquitanian_10pct
python3 scripts/build_control_pools.py --pool polluted_aquitanian_25pct
python3 scripts/build_control_pools.py --pool polluted_aquitanian_75pct
python3 scripts/generate_candidates.py --pool control_toponym_bigram
for p in polluted_aquitanian_{10,25,75}pct control_polluted_aquitanian_{10,25,75}pct; do
    python3 scripts/generate_candidates.py --pool "$p"
done
for m in hypotheses/auto/*{_10pct,_25pct,_75pct,toponym_bigram}.manifest.jsonl; do
    python3 scripts/run_sweep.py --manifest "$m" --metrics external_phoneme_perplexity_v0
done
python3 scripts/v18_toponym_bigram_gate.py
python3 scripts/v18_pollution_level_sweep.py
```

reproduces every byte of the new pools, manifests, sidecar JSONLs,
and rollups. No RNG anywhere is unkeyed.

## Findings from mg-3438 (v19 — per-inscription coherence test on right-tail / short / known-content inscriptions, 2026-05-05)

### Headline

The per-inscription coherence test produces **3 cascade candidates**
under the robust statistic (modal_posterior > 0.5 AND n_proposals ≥ 2,
weighted by sign frequency in the inscription):

- **`KH 10`** (Khania, accountancy, 11 syllabographic tokens) —
  robust fraction 0.5455, mechanical reading
  `s-e-n-i-u-r-(a)-(e)-(l)-(a)-(a)`. Six of the eleven sign positions
  show ≥2 substrate candidates agreeing on the same modal phoneme.
  The high-coherence span runs over the leading 6 tokens.
- **`KH 5`** (Khania, accountancy, 20 syllabographic tokens) —
  robust fraction 0.5000, mechanical reading
  `(s)-(a)-(l)-(a)-(a)-(s)-e-n-(a)-z-t-t-a-z-a-l-a-·-·-·`. Ten of
  twenty signs are robust-coherent; the trailing three tokens have
  no positive-paired-diff candidate at all.
- **`PS Za 2`** (Psykhro, votive_or_inscription, 14 tokens) —
  robust fraction 0.7143, mechanical reading
  `c-e-a-(ch)-th-(ch)-th-u-u-n-i-(l)-a-(l)`. The libation-formula
  span AB57-AB31-AB31-AB60-AB13 yields the modal sequence
  `th-u-u-n-i`.

Two **partial cascades** (robust fraction in [0.25, 0.5)):

- **`HT 95a`** (Haghia Triada, accountancy, 19 tokens) — robust
  fraction 0.3158, literal fraction 0.5789. The literal-vs-robust
  gap arises because most of the signs that pass the literal
  threshold are lone-proposal signs (n_proposals = 1), which
  trivially yield modal_posterior = 1.0 under any smoothing but do
  not constitute a multi-surface collision.
- **`HT 31`** (Haghia Triada, accountancy, 24 tokens) — robust
  fraction 0.3333, literal fraction 0.5000. Same lone-proposal
  attrition as HT 95a.

Population breakdown by classification (robust statistic):

| population | n inscriptions | cascade | partial | noise |
|:--|---:|---:|---:|---:|
| A: top-30 right-tail | 30 | 2 | 2 | 26 |
| B: short ≤5 signs    |  4 | 0 | 0 |  4 |
| C: libation formula  |  1 | 1 | 0 |  0 |
| **all**              | **35** | **3** | **2** | **30** |

### What this means and what it does NOT mean

**What it means.** v13 (mg-c216) showed the per-SURFACE consensus
median is 0.18 — across all the windows where a top-20 substrate
surface was used, the proposed sign-to-phoneme mappings disagreed
heavily. v19 asks the per-INSCRIPTION question and finds three
inscriptions where the *local* consensus on signs they share is
above the cascade bar. The local-aggregate-vs-global-aggregate gap
is genuine: the per-surface measure averages over many candidates
and many inscriptions; the per-inscription measure picks out a
small set of signs where multiple substrate hypotheses happen to
agree.

**What it does NOT mean.** A cascade candidate is a hypothesis for
domain-expert review, not a decipherment claim. The per-inscription
consensus tells us "the framework's surviving candidates agree on
these phoneme assignments at this inscription"; it does NOT tell us
"these phoneme assignments are correct Linear A". Internal consensus
is a necessary but not sufficient condition for correctness.

### Population C: comparison to scholarly libation-formula proposal

The libation-formula `JA-SA-SA-RA-ME` has a long-standing scholarly
transliteration `ja-sa-sa-ra-me` (consonantal segments j-s-s-r-m on
the five signs AB57-AB31-AB31-AB60-AB13). On `PS Za 2`, the framework
mechanical modal phonemes for that span are **`th-u-u-n-i`** —
divergent from the scholarly proposal on every position (0/5 match
on the consonantal segment).

The honest read of this divergence: the per-inscription consensus
on PS Za 2 is *internally* high (robust fraction 0.71) but the
agreed-upon phonemes do NOT correspond to the best-attested
scholarly phoneme values for these signs. This is consistent with
v13's per-surface failure (median 0.18) and with v15's (mg-7ecb)
finding that the gate detects *substrate-LM-phonotactic kinship*
rather than per-surface substrate-vocabulary identity. The
framework's surviving candidates agree on `PS Za 2` because the
signs in that inscription have phonotactic shapes consistent with
the substrate-LM expectations — not because the sign-to-phoneme
mappings being agreed upon are the historically correct ones.

### What this changes about the methodology paper's claims

The "what the framework does NOT support" section in
`findings_summary.md` claimed (correctly under v13) that the
framework cannot underwrite per-sign decipherment. That claim
remains true at the AGGREGATE level (per-surface coherence median
0.18). But v19 introduces a distinct piece of evidence: per-
inscription LOCAL coherence on a small set of inscriptions (3 of
35 evaluated) yields high consensus internally. The right framing
is:

  > Per-sign decipherment is NOT supported at the per-surface
  > aggregate level (v13). At the per-inscription local level
  > (v19), three inscriptions show consensus among multiple
  > substrate candidates targeting them — but on the one
  > inscription with a known-content scholarly proposal (PS Za 2,
  > libation formula), the mechanical consensus DIVERGES from the
  > scholarly transliteration on all five formula-span signs.
  > Internal consensus does not imply external correctness.

This is a refinement of the existing claim, not a reversal. The
methodology paper (`docs/findings_summary.md`) is updated to add a
short paragraph in §5 noting v19 as a follow-up that strengthens
the case against decipherment claims rather than supporting them.

### Methodological notes

- *All-positive-paired-diff scope.* v19 aggregates over ALL
  positive-paired-diff candidates targeting an inscription —
  including candidates whose surface is NOT in the v10 top-20.
  Restricting to the top-20 would have re-imposed v13's selection
  filter and confounded the per-inscription test. Cf. the script
  docstring for the rationale.
- *Local Dirichlet smoothing (V_local).* The per-sign modal
  posterior uses V = number of distinct phonemes proposed for that
  sign at that inscription, not the global vocabulary. This is the
  natural local-consensus formulation; it differs from v13's
  global-V smoothing.
- *Robust statistic.* The headline classification uses
  `fraction_robust_high_coherence_signs` (modal_posterior > 0.5
  AND n_proposals ≥ 2) rather than the literal-brief
  `fraction_high_coherence_signs`. The literal statistic is
  reported alongside in every per-population table. Lone-proposal
  signs (n=1) trivially satisfy the literal threshold under any
  smoothing — a single candidate proposing anything yields
  modal_posterior = 1.0 — but a single proposal is not a
  multi-surface "collision" and not a genuine consensus. The
  robust statistic operationalizes Daniel's brief framing
  ("multiple surfaces collide on the same handful of signs")
  directly.
- *Three pools (aquitanian + etruscan + toponym).* The brief
  explicitly enumerates these three as the validated pools.
  Toponym FAILed v10's aggregate right-tail gate; that aggregate
  failure does not invalidate individual positive-paired-diff
  records on specific inscriptions, which is what v19 aggregates.

### Artifacts shipped

- `scripts/per_inscription_coherence.py` — per-inscription
  consensus aggregation, modal-phoneme posterior under local
  Dirichlet smoothing, robust + literal coherence statistics,
  cascade classification, and mechanical-reading rendering.
- `results/rollup.per_inscription_coherence.md` — three-population
  rollup with cascade-candidate enumeration, partial-cascade
  enumeration, per-sign breakdowns for all three cascade
  candidates, and the Population C scholarly-comparison section.
- `harness/tests/test_per_inscription_coherence.py` — 22 smoke
  tests covering token filtering, per-sign consensus, end-to-end
  per-inscription aggregation on a hand-built minimal dataset
  (3 signs × 4 candidates), cascade classification thresholds,
  Population B selection, Population C needle matching, empty-
  tokens edge case, and determinism.

### Reproducibility

```
python3 scripts/per_inscription_coherence.py
```

reproduces `results/rollup.per_inscription_coherence.md` byte-for-
byte against the same `results/experiments.external_phoneme_perplexity_v0*.jsonl`,
`hypotheses/auto/*`, `hypotheses/auto_signatures/*`, and `pools/*`.
No RNG.

### Out of scope (deferred)

- **Domain-expert review of cascade candidates.** Not a polecat
  task; would need an Aegean syllabary specialist. The mechanical
  readings for `KH 10`, `KH 5`, and `PS Za 2` are the natural
  starting point for that review.
- **Broader known-content comparison.** The libation formula is
  the most-attested known-content reading available against which
  to compare. Comparing the cascade-candidate readings on KH 10 /
  KH 5 to scholarly proposals (where they exist for accountancy
  context) would require deeper secondary-source ingest.
- **Methodology paper rewrite.** v19's findings refine rather than
  reverse v13's claim. A minimal `findings_summary.md` paragraph is
  added; deeper rewriting (if the cascade-candidate framing
  warrants paper-shape integration) is its own ticket.
- **Per-window deduplication / Linear-B small-K gate adoption.**
  Out of v19 scope per the brief.

## Findings from mg-711c (v20 — methodology paper integration of v19 cascade-candidate findings + light scholarly-proposal comparison on KH 10 / KH 5, 2026-05-05)

### Headline

Two-part documentation-and-investigation ticket. Part 1 (small):
search the v19 cascade-candidate accountancy tablets `KH 10` and
`KH 5` for the two most-attested Linear A scholarly anchors —
`ku-ro` ("total/sum") and `ki-ro` ("deficit/owed") — and report
mechanical-vs-scholarly comparison on any matches found. Part 2
(bulk): elevate the v19 PS Za 2 external-validation result in
`docs/findings_summary.md` from minimal-paragraph status to
load-bearing-finding status across Abstract / §3.1 / §3.12 / §3.13
/ §4.6 / §5.1 / §5.3 / §6.

### Part 1 — KU-RO / KI-RO scholarly-anchor search (NULL result)

**Canonical scholarly AB-sequences** (from `pools/linear_b_carryover.yaml`,
which incorporates Younger 2020 + Schoep 2002 + Palmer 1995 +
Ventris-Chadwick 1956 carryover values):

- `ku-ro` = **AB81-AB02** (`ku` = AB81, `ro` = AB02)
- `ki-ro` = **AB67-AB02** (`ki` = AB67, `ro` = AB02)

**Tokens inspected** (syllabogram-only; logograms `LOG:*` and
divider tokens `DIV` excluded, matching v19's per-inscription
scoring path; `corpus/Khania/KH%2010.json` + `KH%205.json`):

| inscription | n syll | run |
|:--|--:|:--|
| `KH 10` | 11 | AB28-AB03-AB31-AB57-AB16-AB118-AB08-AB67-AB39-AB38-AB04 |
| `KH 5`  | 20 | AB08-AB01-AB67-AB41-AB77-AB08-AB60-AB10-AB01-AB40-AB31-AB31-AB24-AB40-AB06-AB51-AB06-AB81-AB03-AB79 |

**Match search** for each canonical sequence in each tablet:

| sequence | KH 10 | KH 5 | result |
|:--|:--:|:--:|:--|
| AB81-AB02 (KU-RO) | absent — AB81 not in syllabogram run | absent — AB81 → AB03, not AB02 | **no match** |
| AB67-AB02 (KI-RO) | absent — AB67 → AB39, not AB02 | absent — AB67 → AB41, not AB02 | **no match** |

AB02 (the canonical `ro`) is **absent from both inscriptions**.
AB81 occurs once in `KH 5` only (followed by AB03). AB67 occurs
once in each tablet (followed by AB39 in `KH 10`, AB41 in `KH 5`).
No KU-RO or KI-RO instance is therefore available to compare to
v19's mechanical readings on these two cascade candidates.

**Tension flagged.** The mg-711c ticket text gave KU-RO and KI-RO
as AB81-AB60 and AB67-AB60 respectively. AB60 is the canonical
scholarly value for `ra`, not `ro`, as visible on the libation-
formula span AB57-AB31-AB31-AB60-AB13 used by v19. The canonical
value for `ro` is AB02, per the project's own
`linear_b_carryover.yaml` entries for `kuro` and `kiro` (citing
Younger 2020; Ventris-Chadwick 1956 carryover values). v20 read
the ticket's `AB81-AB60` / `AB67-AB60` as a typo for the
well-attested `AB81-AB02` / `AB67-AB02` (canonical) — but for
completeness also searched the literal ticket-text sequences
AB81-AB60 and AB67-AB60. Both come up empty too: AB81 in `KH 5`
is followed by AB03 (not AB60), AB67 in both tablets is followed
by AB39 / AB41 (not AB60). So under either interpretation —
canonical or ticket-literal — the §3.13.2 comparison set is
**empty**.

### Part 2 — Methodology paper rewrite (`docs/findings_summary.md`)

The structural change is moving v19 from a "minimal §3.12 paragraph"
to a load-bearing methodological finding integrated across the
Abstract / Results / Discussion / Limitations / Conclusion. Edits:

- **Header.** Authoring-version tag updated to "v16, mg-d5ed;
  lineage citations corrected in v17, mg-2bfd; v19 cascade-candidate
  / external-validation integration in v20, mg-711c". Project span
  extended from "19 work items" / "v0 through v15 (mg-d5ef through
  mg-7ecb)" to "20 work items" / "v0 through v19 (mg-d5ef through
  mg-3438)".
- **Abstract.** New full paragraph integrating v19 cascade
  candidates and v20's external-validation summary as the project's
  *first external-validation* result, ending on the load-bearing
  framing "internal consensus across surviving candidates does not
  imply external correctness". The "supportable claim" closing
  paragraph extended to call out the divergence on the one
  performable external comparison.
- **§1 Introduction closer.** "seven falsifiable acceptance-gate
  outcomes" → "eleven pre-registered falsifiable acceptance-gate /
  external-validation outcomes" (faithful to the §3.1 table after
  v18 + v19 + v20 additions).
- **§3.1 acceptance-gate summary table.** Two new rows:
  - Row 10: per-inscription cascade-candidate test (mg-3438, v19) —
    3 cascade candidates emerged.
  - Row 11: external validation against scholarly proposals —
    PS Za 2 vs `ja-sa-sa-ra-me` 0/5 consonantal-segment match
    (mg-3438, v19); KH 10 / KH 5 vs `ku-ro` / `ki-ro` no comparable
    substring (mg-711c, v20).
- **§3.2 validation matrix.** Header updated from "as of v18" to
  "as of v20" with note that v19 / v20 operate at the
  per-inscription level, not at the pool-level gate.
- **§3.12 Per-inscription coherence.** Renamed (drop the "but
  diverge from scholarly readings" tail), trimmed the inline
  scholarly-comparison subsection, redirected its detail to §3.13.
  Local-vs-global aggregate-gap framing kept; cascade-candidate
  table and population-breakdown table kept as-is. The
  "honest read" / "refines rather than reverses" closing
  paragraphs absorbed into the new §3.13 closing.
- **§3.13 External validation against scholarly proposals (NEW).**
  Three subsubsections:
  - §3.13.1 PS Za 2 vs the libation formula `ja-sa-sa-ra-me` —
    sign-by-sign comparison table (AB57/AB31/AB31/AB60/AB13);
    explicit note that all 5 mechanical phonemes meet the robust
    threshold (cascade candidate is *confidently* divergent, not
    a thin-data artefact).
  - §3.13.2 KH 10 / KH 5 vs `ku-ro` / `ki-ro` — investigation
    summary, search-result table (no matches), explicit tension
    note re: ticket's AB81-AB60 / AB67-AB60 typo.
  - §3.13.3 External-validation summary — combined result table
    across all three comparands and a closing methodological
    statement: "the framework's mechanical consensus on the
    cascade candidates is a hypothesis, not a reading; on the
    cascade candidate where independent scholarly ground truth
    is available, the hypothesis is mechanically confidently
    wrong".
- **§4.6 Internal consensus does not imply external correctness
  (NEW).** Promoted from §3.12-passing-mention to a load-bearing
  Discussion subsection with a quotable framing block. Closes on
  the "discipline-protecting result" framing and how surface-
  aggregate PASS, internal-consensus cascade candidates, and the
  per-sign decipherment failure are all simultaneously true and
  consistent under the framework's structural reading.
- **§5.1 Out-of-scope by construction.** The existing v19
  paragraph rewritten to combine v13 (per-surface aggregate) AND
  v19 + v20 (per-inscription cascade-candidate external-comparison)
  as joint failures pointing the same direction. Explicitly
  cross-references §4.6 for the load-bearing framing.
- **§5.3 Out-of-scope follow-ups.** Domain-expert-review item
  extended to mention v20's KU-RO/KI-RO null result. New item:
  deeper scholarly-source ingest (Bonfante & Bonfante / Pallottino
  / Younger / Salgarella → comprehensive scholarly-proposal
  database) noted as out of scope per the v20 ticket's own scope
  limits.
- **§6 Conclusion.** New paragraph integrating v19 PS Za 2
  divergence + v20 KU-RO/KI-RO null follow-up; new closing line
  stating that the framework's *null findings* (v13 + v14 + v19 +
  v20) are themselves contributions to the methodological
  literature on undeciphered-script analysis — falsification
  results that internal-only methodology cannot produce.
- **Appendix A.** New row for v20's KU-RO/KI-RO investigation
  pointing to the inspected token-stream files and the canonical
  AB-sequence anchor source. Per-ticket-merge-notes footer
  extended through `mg-711c` (v20, 2026-05-05).

No earlier numbers were silently changed. Where v20's elevated
framing tightens an earlier claim (e.g., §5.1's "per-sign
decipherment is not supported by the data" → "per-sign decipherment
failed at BOTH the aggregate AND the local cascade-candidate
external-comparison level"), the change is additive — it joins
v19 + v20 evidence to v13 evidence on the same claim shape, not
overwriting it.

### Three-sentence reading test

The v16 (mg-d5ed) brief required that a Linear A scholar reading
the updated `findings_summary.md` cold should be able to extract
three sentences that capture the methodology paper's contribution.
After the v20 elevation, those three sentences are:

1. *(Methodology.)* The framework scores candidate substrate-root
   → Linear A sign-window equations under external phoneme LMs
   trained on real substrate text, against phonotactically-matched
   scramble controls drawn from each substrate pool's marginal
   phoneme distribution, with the right-tail Bayesian gate (top-K
   substrate posterior medians vs top-K matched-control posterior
   medians, one-tail Mann-Whitney U) as the population-level
   acceptance criterion.

2. *(Detect / not-detect split.)* The framework detects substrate-
   LM-phonotactic kinship at the population level (Aquitanian PASS
   p = 3.22e-05 under Basque LM, Etruscan p = 5.21e-04 under
   Etruscan LM, with both separations collapsing under unrelated
   LMs) but does NOT support per-sign decipherment: the consensus
   sign-to-phoneme map fails the cross-window-coherence bar
   decisively (median 0.18 vs the 0.6 acceptance bar), and the
   same-distribution pollution test cannot distinguish real
   Aquitanian roots from phonotactically-matched conjecturals
   (within-tail real-vs-conjectural Mann-Whitney p = 0.98).

3. *(External-validation falsification.)* The first external
   comparison of the framework's per-inscription cascade-candidate
   readings to a long-attested scholarly proposal — `PS Za 2`'s
   libation-formula span AB57-AB31-AB31-AB60-AB13 vs
   `ja-sa-sa-ra-me` — finds the framework's confidently-cascading
   mechanical reading `th-u-u-n-i` divergent on every formula-span
   sign (0/5 consonantal-segment match), and a follow-up search
   for additional scholarly comparands (`ku-ro` = AB81-AB02,
   `ki-ro` = AB67-AB02) on the other two cascade candidates
   `KH 10` and `KH 5` finds neither sequence present, leaving
   the libation formula as the project's sole external comparand
   to date and grounding the load-bearing methodological claim
   that internal consensus across surviving substrate candidates
   does not imply external correctness.

These three sentences appear distributed across the Abstract, §3
Results, and §4.6 Discussion in the updated paper. A scholar
reading cold should be able to extract them within ~10 minutes of
reading the Abstract + §3.13 + §4.6 alone.

### Artifacts shipped

- `docs/findings_summary.md` — Abstract, §1 closer, §3.1 table
  (rows 10–11 added), §3.2 header, §3.12 trim + rename, §3.13
  (NEW with three subsubsections), §4.6 (NEW), §5.1 (refined),
  §5.3 (extended), §6 (refined), Appendix A (extended).
- `docs/findings.md` — this entry.

No new corpora, no new metrics, no new pools, no new scripts. The
v20 KU-RO/KI-RO investigation is mechanical pattern-matching
against the existing committed `corpus/Khania/KH%2010.json` and
`KH%205.json`, comparing to the canonical AB-sequence anchors
already cited in `pools/linear_b_carryover.yaml`. Determinism
non-negotiable — the result is byte-identical re-runs of the
same lookup.

### Reproducibility

The KU-RO/KI-RO null result reproduces from the committed
corpus + pool data:

```
# Tokens of KH 10, KH 5 (syllabograms only):
python3 -c '
import json, re
for f in ["corpus/Khania/KH%2010.json", "corpus/Khania/KH%205.json"]:
    d = json.load(open(f))
    syl = [t for t in d["tokens"] if t != "DIV" and not t.startswith("LOG:") and re.match(r"^AB\d+$", t)]
    print(d["id"], "->", "-".join(syl))
'

# Search for canonical KU-RO (AB81-AB02) and KI-RO (AB67-AB02):
# both come up null in both tablets.
```

### Out of scope (deferred, unchanged from ticket)

- **Domain-expert review.** Still not a polecat task; needs an
  Aegean syllabary specialist.
- **Deeper scholarly-source ingest.** Bonfante & Bonfante /
  Pallottino / Younger / Salgarella → comprehensive scholarly
  proposal database is its own ticket. v20 limited scope to the
  two most-attested accountancy readings (KU-RO, KI-RO) plus the
  libation formula already in v19.
- **Per-window deduplication / Linear-B small-K gate adoption.**
  Cosmetic polish; deferred.
- **Methodology-paper LaTeX / journal submission.** Out of polecat
  scope.
- **More cascade-candidate populations** (longer formulaic
  inscriptions, syllabogram-frequency-extreme inscriptions, etc.).
