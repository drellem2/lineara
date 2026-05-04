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

## Scoring harness (v0)

The v0 harness scores a declarative hypothesis against the corpus and appends one row to `results/experiments.jsonl`. One hypothesis shape (partial sign→phoneme mapping) and one metric (`compression_delta_v0`, zlib over a 2-byte symbol-id stream) for now; follow-up tickets add more.

```bash
# Score a hypothesis and append the result row.
python3 -m harness.run hypotheses/identity.yaml
python3 -m harness.run hypotheses/younger_ab54_ti.yaml --note "baseline rerun"

# View the leaderboard (regenerated on demand; not committed).
python3 scripts/rollup.py
```

Hypothesis YAMLs live under `hypotheses/`; their schema is `harness/schemas/hypothesis.v0.schema.json`. Each result row is validated against `harness/schemas/result.v0.schema.json`. The result stream is **append-only** — re-runs add new rows; rows are never edited or deleted. Every row carries `hypothesis_hash`, `harness_version`, and `corpus_snapshot` so a stale row whose hypothesis YAML has since been edited is detectable (hash mismatch) and ignorable.

The harness depends on `pyyaml` and `jsonschema`; install with `pip install pyyaml jsonschema`.
