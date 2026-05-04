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

- `corpus/` — Linear A corpus + metadata sidecars (no corpus data committed)
- `hypotheses/` — declarative hypothesis artifacts
- `results/` — append-only JSONL of mechanical scores
- `harness/` — scoring harness, pluggable metrics

See `AGENTS.md` for who does what.
