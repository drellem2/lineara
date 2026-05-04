# lineara

Mechanical info-theoretic chipping-away at Linear A.

## Mission

Linear A is undeciphered, and the realistic posture is that no single
hypothesis will crack it. What's tractable is a long tail of cheap,
falsifiable experiments whose mostly-null results gradually constrain the
space — decipherment-by-compression-improvement, many small bets, no
narrative leaps. The working candidate substrate is the old-European root
layer: toponyms, Basque, Etruscan, and adjacent pre-IE material. None of
these is assumed to be "the" answer; they are scored.

## What counts as a hypothesis

A declarative artifact under `hypotheses/` that names a candidate mapping,
segmentation, alignment, or substrate prior; is concrete enough that the
scoring harness can consume it without further human interpretation; and
predicts a measurable change in a compression / entropy / alignment score
against the corpus, relative to a stated baseline. If the harness can't
score it, it doesn't belong here.

## How results are reported

Each harness run appends one JSON object per hypothesis × metric × corpus
slice to `results/` as JSONL. Append-only. Null results are first-class —
they're the point. Re-runs add new rows with a fresh run id; aggregation
lives downstream of the log, never inside it.

## Layout

- `corpus/` — Linear A corpus + metadata sidecars
- `hypotheses/` — declarative hypothesis artifacts
- `results/` — append-only JSONL of mechanical scores
- `harness/` — scoring harness, pluggable metrics
- `schema/inscription.schema.json` — JSON Schema for one inscription record
- `scripts/` — corpus fetch / parse / build / cross-check tooling
- `corpus_status.md` — what's in the corpus, what was dropped, and how the v1 tokenization rules map to source data

See `AGENTS.md` for who does what.

## Corpus ingestion (v1, SigLA)

Per-inscription JSON records under `corpus/<site>/<id>.json` plus a
`corpus/all.jsonl` aggregate, ingested from SigLA (CC BY-NC-SA 4.0). The
per-inscription files are the source of truth; `all.jsonl` is rebuilt
deterministically from them. Tokenization, coverage, and known gaps are
documented in `corpus_status.md`.

Rebuild from scratch:

```bash
python3 scripts/fetch_sigla.py            # cache SigLA HTML under .cache/sigla/
python3 scripts/parse_sigla.py            # write corpus/<site>/<id>.json + all.jsonl
python3 scripts/build_corpus.py --strict  # round-trip + schema-validate
python3 scripts/check_corpus.py           # SigLA word-pattern cross-check
```

## Scoring harness

The harness scores a declarative hypothesis against the corpus and appends one row to `results/experiments.jsonl`. Two hypothesis shapes are supported, each paired with a default metric:

| Shape | Discriminator | Default metric | Use for |
|---|---|---|---|
| `hypothesis.v0` (mapping) | (no `schema_version`) | `compression_delta_v0` | corpus-global sign→phoneme mappings |
| `candidate_equation.v1` | `schema_version: candidate_equation.v1` | `local_fit_v0` | local "this span = this candidate root" hypotheses |

```bash
# Score a hypothesis and append the result row (auto-dispatches metric on shape).
python3 -m harness.run hypotheses/identity.yaml
python3 -m harness.run hypotheses/younger_ab54_ti.yaml --note "baseline rerun"
python3 -m harness.run hypotheses/curated/anchor_kuro_HT100.yaml

# View per-metric leaderboards (regenerated on demand; not committed).
python3 scripts/rollup.py
python3 scripts/rollup.py --metric local_fit_v0
```

Hypothesis YAMLs live under `hypotheses/`; the curated test suite for the v1 candidate-equation shape is in `hypotheses/curated/`, and bulk-generated hypotheses from the Aquitanian pool live under `hypotheses/auto/aquitanian/`. Schemas: `harness/schemas/hypothesis.v0.schema.json`, `harness/schemas/hypothesis.candidate_equation.v1.schema.json`. Each result row is validated against `harness/schemas/result.v0.schema.json` (which carries `local_fit_v0`-specific optional fields `score_control_z` and `metric_notes`). The result stream is **append-only** — re-runs add new rows; rows are never edited or deleted. Every row carries `hypothesis_hash`, `harness_version`, and `corpus_snapshot` so a stale row whose hypothesis YAML has since been edited is detectable (hash mismatch) and ignorable.

## Bulk pipeline (substrate root pools)

The bulk path turns a substrate-root pool into thousands of candidate-equation hypotheses, scores them all, and renders a leaderboard:

```bash
# 1. Generate candidate hypotheses from a pool. Idempotent + content-addressed
#    filenames; manifest is sorted by (pool_entry_index, inscription_id, span_start).
python3 scripts/generate_candidates.py --pool aquitanian

# 2. Run the sweep. Resumable: skips hypotheses already scored under the
#    current corpus snapshot. Prints progress every 100 rows and a summary
#    block + ASCII histogram at the end.
python3 scripts/run_sweep.py --manifest hypotheses/auto/aquitanian.manifest.jsonl

# 3. Render the per-pool leaderboard snapshot.
python3 scripts/rollup.py --metric local_fit_v0 --pool aquitanian --top 50 \
    --write results/rollup.aquitanian.md
```

Pool YAMLs live under `pools/<name>.yaml`, validated against `pools/schemas/pool.v1.schema.json`. The Aquitanian pool's source provenance and refresh procedure are documented in `pools/aquitanian.README.md`.

The `local_fit_v0` metric scores a `candidate_equation.v1` hypothesis by combining a position-fit term (how well do the equation's signs' corpus position fingerprints match the proposed phonemes' expected position profiles?) with a phoneme-class bigram log-likelihood under a hardcoded Basque-style CV phonotactic prior. The result row carries a control-z computed against 200 random phoneme-permutations of the same alignment (seed=42); see the docstring on `harness.metrics.local_fit_v0` for the formula, what it does/does-not measure, and known v0 limitations.

The harness depends on `pyyaml` and `jsonschema`; install with `pip install pyyaml jsonschema`.
