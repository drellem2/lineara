# Curated bucket construction (mg-7c8c, v4)

This document specifies the **rules** by which the 100 hypotheses in
`hypotheses/curated/` were assembled, so the set is reproducible and so
future expansions (n=50, n=100) can extend the same structure without
re-deriving the methodology.

The 20 mg-fb23 entries (4 anchors, 4 plausible Aquitanian, 4 deliberately-
wrong Aquitanian, 4 pre-Greek toponym fragments, 4 random scrambles) were
hand-authored by pm-lineara and committed before this ticket. The 80 v4
entries (16 per bucket) were generated mechanically by
`scripts/build_curated_v4.py`. Re-running that script with the same
corpus snapshot, same pools, and same input lists produces byte-identical
YAMLs and manifest.

## Why expand?

mg-fb23 / mg-7dd1 / mg-23cc each ran a candidate-equation metric against
the n=4 plausible-vs-deliberately-wrong-Aquitanian buckets. **All three
metrics missed the gate.** Per mg-23cc's findings entry:

> Either (a) the metrics collectively miss the plausibility signal, or
> (b) n=4 is too small to detect what's actually there. Future v4 work
> needs to expand the curated bucket before chasing more metric variants.

This ticket settles (a) vs (b) by growing each bucket to n=20 and
re-running all three v3 metrics with a Mann-Whitney U test +
power-calculation sanity check. The result is a *methodology* finding,
not a metric finding.

## Bucket A — Linear-B carryover anchors (n=20)

**Goal.** Maximally-defensible "this Linear-A span has reading X" claims:
each anchor is a Linear-A sequence whose Linear-B carryover phonetic
values are accepted in Younger's online edition of *Linear A texts in
phonetic transcription*. Includes recurring lexemes
(`ku-ro` "total", `ki-ro` "deficit", `ku-mi-na` "cumin",
`pi-ta-ja` name-form, libation-formula prefixes, etc).

**Construction rules:**

1. Each anchor is a 2- or 3-sign Linear-A sequence.
2. Each constituent sign occurs **≥10 times** in the SigLA corpus
   (acceptance bar from the brief; mechanically asserted by the build
   script before placement).
3. Each constituent sign is pairwise distinct (the
   `sign_to_phoneme` dict cannot carry duplicate keys).
4. Placement: the anchor is pinned to the **first matching window in
   the first matching inscription**, with placement preference for
   Knossos clean accountancy inscriptions (region_compat=1.0 for
   `linear_b × Knossos`); falling back to any clean accountancy
   inscription. Records are sorted lexicographically by id, so the
   selection is deterministic.
5. Per-anchor citation: Younger's online edition + (where applicable)
   a secondary literature pointer (Schoep 2002 for libation tables;
   Hooker 1979 for Phaistos carryover; Watkins 1995 for substrate
   etymology paths). Retrieval date 2026-05-04.

**The 16 v4 anchors** (the 4 mg-fb23 anchors are listed separately):

| surface  | signs              | gloss                                       |
|----------|--------------------|---------------------------------------------|
| `kupa`   | AB81 AB03          | ku-pa name family                            |
| `kapa`   | AB77 AB03          | ka-pa transaction term                       |
| `karu`   | AB77 AB26          | ka-ru recurring lexeme                       |
| `mate`   | AB80 AB04          | ma-te (cf. Linear-B mater)                   |
| `tana`   | AB59 AB06          | ta-na suffix                                  |
| `dina`   | AB07 AB06          | di-na recurring lexeme                       |
| `kupa3`  | AB81 AB56          | ku-pa3 name (kupa variant)                  |
| `mina`   | AB73 AB06          | mi-na (cumin termination; cf. ku-mi-na)      |
| `kira`   | AB67 AB60          | ki-ra suffix variant                         |
| `dare`   | AB01 AB27          | da-re libation continuation                  |
| `data`   | AB01 AB59          | da-ta libation prefix                        |
| `tare`   | AB59 AB27          | ta-re libation continuation                  |
| `paja`   | AB03 AB57          | pa-ja name-family                            |
| `kuse`   | AB81 AB09          | ku-se recurring lexeme                       |
| `kumina` | AB81 AB73 AB06     | ku-mi-na (cumin commodity)                   |
| `pitaja` | AB39 AB59 AB57     | pi-ta-ja standard 3-sign name                |

## Bucket B — Plausible Aquitanian (n=20)

**Goal.** Aquitanian-substrate readings placed in inscriptions whose
genre is *plausibly compatible* with the surface's semantic field, so
that the v1 geographic-genre filter assigns
`semantic_compat ≥ 0.5`.

**Construction rules:**

1. Surface drawn from `pools/aquitanian.yaml` (already cited from
   Trask 1997 / Gorrochategui 1984).
2. Phoneme length 2-5 (matches the v1 metric's tested range).
3. Surface's `semantic_field ∈ {food, animal, number}`. These three
   semantic fields *flip* against `accountancy` vs
   `votive_or_inscription` in
   `harness.metrics._GG1_SEMANTIC_COMPAT`:
   - food / animal × accountancy = 0.75 ; × votive_or_inscription = 0.25
   - number × accountancy = 1.00 ; × votive_or_inscription = 0.25
4. Inscription `transcription_confidence == 'clean'` (no partial /
   fragmentary).
5. Inscription `genre_hint == 'accountancy'` (the dominant Linear-A
   genre; ensures plausible-bucket compat ≥ 0.75).
6. Placement: first window where the syllabograms are pairwise
   distinct, with the first matching record in id-sorted order. The
   build script tracks placement keys and avoids reusing the same
   `(record, span_start, span_end)` triple within a bucket.

The 16 v4 plausible surfaces (from the Aquitanian pool):
`gari`, `arto`, `ogi`, `esne`, `ardo`, `olio`, `ezti`, `sagar`,
`ardi`, `behi`, `katu`, `zaldi`, `bat`, `hiru`, `lau`, `hamar`.

## Bucket C — Deliberately-wrong Aquitanian (n=20)

**Goal.** Same surfaces as bucket B, but placed in inscriptions whose
genre is *incompatible* with the surface's semantic field — so the
ONLY thing distinguishing C from B is the inscription's genre context,
not the phoneme order, not the sign set, not the phonotactic
plausibility of the candidate equation.

**Construction rules:**

1. Same 16 surfaces as bucket B (so the comparison isolates the
   placement-context signal).
2. Inscription `transcription_confidence == 'clean'`.
3. Inscription `genre_hint == 'votive_or_inscription'`. The Linear-A
   corpus has 5 such clean records with ≥4 syllabograms:
   `HT Zb 158b`, `HT Zb 159`, `HT Zb 160`, `KN Zb 35`, `SY Za 4`.
   Multiple wrong-bucket placements may land on the same inscription
   (different surfaces / different windows); the build script tracks
   placement keys and avoids reusing the same `(record, span_start,
   span_end)` triple.
4. **The wrong placement is NOT phonotactically wrong.** This is a
   deliberate departure from the mg-fb23 wrong-bucket rule (which
   chose signs whose position fingerprints fail V/S/C class
   expectations). The mg-7c8c rule is: keep the equation
   phonotactically valid; differ ONLY in placement context. We want
   to test whether the metrics detect the *plausibility-of-context*
   signal, not the obvious *signs-are-the-wrong-class* failure mode.
5. The 4 mg-fb23 wrong entries (kept as-is per the append-only rule)
   *do* embed the older phonotactic-wrong rule. When mixed with the
   16 new genre-wrong v4 entries, the combined n=20 wrong bucket
   contains both flavors. This is fine for rank-based statistics
   (Mann-Whitney U is rank-invariant under the difference); the
   construction note here is that the bucket is intentionally
   heterogeneous in the *kind* of "wrongness" it embeds.

## Bucket D — Plausible pre-Greek toponym (n=20)

**Goal.** Substrate readings drawn from a third pool —
`pools/toponym.yaml` (35 entries from Beekes 2010 / Furnée 1972, added
in this ticket) — to exercise the
`pre_greek × Crete = 1.0` row of the v1 region-compat lookup table.

**Construction rules:**

1. Each candidate's surface is a 2-5 phoneme **fragment** (prefix or
   substring) of a full toponym in `pools/toponym.yaml`.
2. The full toponym is cited per Beekes 2010 (s.v. each name) /
   Furnée 1972 (substrate suffix typology).
3. Inscription is **Cretan** (region_compat = 1.0 for `pre_greek ×
   Crete` in `harness.metrics._GG1_REGION_COMPAT`).
4. Inscription `transcription_confidence == 'clean'`.
5. Inscription `genre_hint == 'accountancy'` (semantic_compat for
   `place × accountancy` = 0.75 → plausible).
6. Placement: first window with pairwise-distinct syllabograms in
   id-sorted record order; the build script tracks placement keys.

Expected `geographic_genre_fit_v1` ≈ `0.4 * 1.0 + 0.6 * 0.75 = 0.85`,
which would be the highest geographic-axis score the metric emits on
this curated set.

## Bucket E — Random scramble (n=20)

**Goal.** Pure-random IPA strings as a null baseline. If the metrics
do not separate scrambles from real-substrate readings, the metrics
are not measuring anything useful at all.

**Construction rules:**

1. Random length in [2, 5], uniform.
2. Random phoneme labels sampled (without replacement) from a fixed
   inventory of "obviously not Linear-A-like" IPA glyphs — uvulars,
   pharyngeals, retroflexes — chosen to align with the mg-fb23
   scramble bucket's `q`, `ʁ`, `wj`, `ɣ`, `ɲ` pattern.
3. Random clean inscription with ≥5 syllabograms; selection is
   uniformly random over a re-shuffled copy of the id-sorted clean
   record pool.
4. Pairwise-distinct syllabograms within the chosen window.
5. **Frozen RNG seed: 4242** (`_RANDOM_SEED` in
   `scripts/build_curated_v4.py`). Re-running yields byte-identical
   scrambles.
6. The mg-fb23 scramble bucket used seed=42 (mirroring the
   `local_fit_v0` control-distribution seed). v4 uses 4242 to make
   the new and old scrambles independent; old entries are not
   regenerated.

## Manifest format

`hypotheses/curated/CONSTRUCTION.manifest.jsonl` follows the same shape
as `hypotheses/auto/<pool>.manifest.jsonl` (one JSON object per line)
plus three extra keys carried for downstream statistics:

- `bucket` — one of `A_linear_b_anchor`, `B_aquit_plausible`,
  `C_aquit_wrong`, `D_toponym_plausible`, `E_scramble`.
- `bucket_kind` — short tag (`anchor`, `plausible`, `wrong`,
  `scramble`).
- `is_v4_new` — boolean; `false` for the 20 mg-fb23 hypotheses,
  `true` for the 80 v4 ones.

The manifest is sorted by `(bucket, is_v4_new, hypothesis_name)` so
existing entries appear before new ones within each bucket and the
order is determinstic.

## Re-running / refreshing

```bash
python3 scripts/build_curated_v4.py            # writes 80 YAMLs + manifest
python3 scripts/build_curated_v4.py --no-write # dry run
```

If the corpus snapshot, Aquitanian pool, or toponym pool changes, the
script will re-pick placements and the manifest hashes will shift. The
sweep runner (`scripts/run_sweep.py`) detects hash drift via the
manifest's `hypothesis_hash` field and refuses to score a stale
manifest, which is the right behavior.

## Acceptance assertions baked into the build

The build script asserts at exit:

- 80 new entries written.
- 100 manifest rows total (20 existing + 80 new).
- 20 entries per bucket × 5 buckets.
- Every anchor sign occurs ≥10 times in the corpus.
- Every YAML validates against
  `harness/schemas/hypothesis.candidate_equation.v1.schema.json`.

These are not separate tests; they are inline `assert` / `raise` calls
in `main()`. A successful build implies all of them.
