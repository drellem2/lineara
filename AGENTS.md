# Agents

This repo is operated under the pogo multi-agent conventions. In short:

- **pm-lineara** owns triage. New ideas, candidate hypotheses, corpus-source
  decisions, and prioritization land in pm-lineara's queue first. pm-lineara
  decomposes them into mg work items.
- **polecats** execute. Each polecat takes one mg ticket, runs in an
  isolated worktree, and submits its branch to the refinery. Polecats are
  ephemeral: one ticket, one merge, done.
- **mayor** dispatches. The mayor pulls available work items, spawns
  polecats against them, and stops them when their work is verified merged.

For the full pogo conventions (mg work items, refinery merge queue, mail
between agents, pogod schedules), see the pogo project. This repo follows
those conventions without modification — if something here disagrees with
pogo's docs, pogo's docs win.

## Scope-of-work norms specific to this repo

- Hypotheses are committed as artifacts before any scoring run that
  references them. No retroactive "we also tried this" entries.
- `results/` is append-only. Polecats do not edit or delete prior rows;
  they add new rows with a fresh run id.
- Corpus data is not committed. `corpus/` holds metadata sidecars and
  loaders only; the actual glyph sequences live outside the repo and are
  pointed to by sidecar config.
- Null results are reported with the same rigor as positive ones. A
  polecat whose hypothesis scored null still ships the JSONL row.
