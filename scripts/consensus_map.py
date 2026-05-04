#!/usr/bin/env python3
"""Consensus sign-to-phoneme map + cross-window coherence test (mg-c216, harness v13).

For each Linear A sign s appearing in at least N candidate equations
drawn from the v10 Aquitanian / Etruscan top-20 substrate surfaces:

  * Build a histogram of the phonemes proposed for s by those candidates'
    sign_to_phoneme mappings.
  * Compute the modal phoneme, its smoothed Dirichlet-multinomial
    posterior probability (symmetric prior with concentration α and
    vocabulary size V = number of distinct phonemes observed across the
    consensus dataset), and the Shannon entropy of the maximum-likelihood
    histogram (in bits).
  * Record the top-3 alternative phonemes with their posteriors and the
    set of v10 top-20 substrate surfaces whose equations contributed.

Only **positive paired-diff** records are aggregated — a candidate
equation is included only if its substrate side beat its matched control
under the same-LM `external_phoneme_perplexity_v0` metric. This keeps
"wrong" mappings out of the consensus.

Cross-window coherence test
===========================
For each v10 top-20 substrate surface S:

  * Per-surface coherence = Σ_s [freq(S, s) * P_modal(s)]  /  Σ_s freq(S, s)
    weighted by sign-frequency in S's positive-paired-diff equations.

Per-pool coherence = median of per-surface coherences (only surfaces
with at least one targeted sign in the consensus map are included).

Acceptance gate (the central question for mg-c216):
  For at least one substrate pool (Aquitanian or Etruscan), the median
  per-surface coherence must exceed 0.6. ≥0.6 in both pools → reading
  #1 (gate-too-conservative) is supported. <0.6 in both → reading #2
  (curation-sensitivity) is supported. Mixed verdict possible.

Refined-gate sensitivity check
==============================
Recompute the right-tail one-tail Mann-Whitney U gate on the
linear_b_carryover positive-control pool with K ∈ {5, 10, 20}. Reported
purely as a diagnostic for the merge note — the production rollup
(`scripts/per_surface_bayesian_rollup.py`) is unchanged.

Output
======
  results/consensus_sign_phoneme_map.md   (committed; one row per sign)

A summary JSON is printed to stdout containing the per-pool coherence
verdicts and the K-sensitivity p-values for the merge note.

Determinism
===========
The aggregation is byte-identical across re-runs given the same result
stream (`results/experiments.external_phoneme_perplexity_v0.jsonl`) and
the same manifests + hypothesis YAMLs. No RNG anywhere.

Usage
=====
  python3 scripts/consensus_map.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

# Allow `python3 scripts/consensus_map.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.per_surface_bayesian_rollup import (  # type: ignore
    _DEFAULT_AUTO,
    _DEFAULT_AUTO_SIG,
    _DEFAULT_LANGUAGE_DISPATCH,
    _DEFAULT_POOLS,
    _DEFAULT_RESULTS_DIR,
    _load_manifest,
    _load_pool_phonemes,
    _load_score_rows,
    aggregate_per_surface,
    beta_posterior,
    build_posterior_rows,
    build_v8_records,
    build_v9_records,
    mann_whitney_u_one_tail,
)


# v10 (mg-d26d) top-20 substrate surfaces, by passing pool. Hardcoded
# from the committed `results/rollup.bayesian_posterior.{aquitanian,
# etruscan}.md` so that downstream analyses are reproducible against the
# v10 published right-tail leaderboard, not against whatever the current
# rollup happens to produce after future tie-breaking changes. Identical
# to `_V10_TOP20_BY_POOL` in scripts/right_tail_inscription_concentration.py;
# kept as its own copy so the two analyses can independently drift if
# v10's top-20 ever needs revisiting.
_V10_TOP20_BY_POOL: dict[str, tuple[str, ...]] = {
    "aquitanian": (
        "aitz", "hanna", "nahi", "ako", "beltz", "bihotz", "egun", "eki",
        "ezti", "gaitz", "hau", "hesi", "itsaso", "oin", "ona", "zelai",
        "zortzi", "argi", "ate", "entzun",
    ),
    "etruscan": (
        "larth", "aiser", "matam", "avils", "camthi", "chimth", "hanthe",
        "laris", "nac", "sech", "thana", "zelar", "caitim", "thesan",
        "spureri", "thanchvil", "suthi", "mach", "arnth", "sath",
    ),
}


# ---------------------------------------------------------------------------
# Hypothesis YAML loaders (cached by path; deterministic).
# ---------------------------------------------------------------------------


def _yaml_loader():
    import yaml

    class _StringDateLoader(yaml.SafeLoader):
        pass

    _StringDateLoader.yaml_implicit_resolvers = {
        k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    return _StringDateLoader


def _hash_to_v8_meta(auto_dir: Path, pool: str) -> dict[str, dict]:
    """v8 substrate hypothesis_hash → {path, surface, inscription_id}."""
    out: dict[str, dict] = {}
    for row in _load_manifest(auto_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = {
            "path": row["hypothesis_path"],
            "surface": row["pool_entry_surface"],
            "inscription_id": row["inscription_id"],
        }
    return out


def _hash_to_v9_meta(auto_sig_dir: Path, pool: str) -> dict[str, dict]:
    """v9 substrate hypothesis_hash → {path, root_surfaces, inscription_id}."""
    out: dict[str, dict] = {}
    for row in _load_manifest(auto_sig_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = {
            "path": row["hypothesis_path"],
            "root_surfaces": tuple(row["root_surfaces"]),
            "inscription_id": row["inscription_id"],
        }
    return out


def extract_v8_sign_to_phoneme(yaml_path: Path) -> dict[str, str]:
    """Read a candidate_equation.v1 YAML and return its sign_to_phoneme."""
    import yaml

    with yaml_path.open("r", encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=_yaml_loader())
    eq = doc.get("equation", {}) if doc else {}
    raw = eq.get("sign_to_phoneme", {}) or {}
    return {str(s): str(p) for s, p in raw.items()}


def extract_v9_root_sign_to_phoneme(yaml_path: Path) -> list[dict]:
    """Read a candidate_signature.v1 YAML and return per-root sign_to_phoneme.

    Returns a list of ``{"surface": str, "sign_to_phoneme": dict}`` ordered
    as in the YAML. Callers filter to the roots whose surface is in the
    v10 top-20 set.
    """
    import yaml

    with yaml_path.open("r", encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=_yaml_loader())
    out: list[dict] = []
    if not doc:
        return out
    for root in doc.get("roots", []) or []:
        raw = root.get("sign_to_phoneme", {}) or {}
        out.append(
            {
                "surface": str(root.get("surface", "")),
                "sign_to_phoneme": {str(s): str(p) for s, p in raw.items()},
            }
        )
    return out


# ---------------------------------------------------------------------------
# Consensus aggregation
# ---------------------------------------------------------------------------


def collect_sign_phoneme_proposals(
    *,
    pools: list[str],
    top20_by_pool: dict[str, tuple[str, ...]],
    auto_dir: Path,
    auto_sig_dir: Path,
    pools_dir: Path,
    results_dir: Path,
    repo_root: Path,
    language_dispatch: dict[str, str],
) -> dict:
    """Walk positive-paired-diff substrate records → (sign, phoneme) tally.

    Returns
    -------
    dict
        ``{
          "histograms": {sign: {phoneme: count}},
          "contributing_surfaces": {sign: {surface: {pool: count}}},
          "per_surface_targets": {(pool, surface): {sign: {phoneme: count}}},
          "n_records_seen": int,
          "n_positive_records": int,
        }``

    A "proposal" is one (sign, phoneme) pair pulled from one positive-
    paired-diff candidate's sign_to_phoneme mapping, restricted to v10
    top-20 contributions. v8 candidates contribute their full mapping
    (the whole equation maps to one v10 surface). v9 signatures
    contribute only the sign_to_phoneme of roots whose surface is in
    the v10 top-20 set; other roots in the same signature are
    irrelevant to the consensus.
    """
    score_rows = _load_score_rows(results_dir)
    pool_phonemes = _load_pool_phonemes(pools_dir)

    sub_records: list[dict] = []
    for pool in pools:
        sub_records.extend(
            build_v8_records(
                pool=pool,
                auto_dir=auto_dir,
                score_rows=score_rows,
                pool_phonemes=pool_phonemes,
                language_dispatch=language_dispatch,
            )
        )
        sub_records.extend(
            build_v9_records(
                pool=pool,
                auto_dir=auto_sig_dir,
                score_rows=score_rows,
                language_dispatch=language_dispatch,
            )
        )

    v8_meta: dict[str, dict[str, dict]] = {p: _hash_to_v8_meta(auto_dir, p) for p in pools}
    v9_meta: dict[str, dict[str, dict]] = {p: _hash_to_v9_meta(auto_sig_dir, p) for p in pools}

    flat_top20: dict[str, set[str]] = {p: set(top20_by_pool[p]) for p in pools}
    union_top20: set[str] = set()
    for s in flat_top20.values():
        union_top20.update(s)

    histograms: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    contributing: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(int))
    )
    per_surface_targets: dict[tuple[str, str], dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(int))
    )

    n_records_seen = 0
    n_positive_records = 0

    for rec in sub_records:
        n_records_seen += 1
        if rec["paired_diff"] <= 0:
            continue
        n_positive_records += 1
        pool = rec["pool"]
        sub_hash = rec["substrate_hash"]
        kind = rec["kind"]
        substrate_surfaces = set(rec["substrate_surfaces"])
        # Skip records whose substrate surfaces don't intersect the
        # v10 top-20 set for this pool — they don't contribute to the
        # consensus.
        relevant = substrate_surfaces & flat_top20[pool]
        if not relevant:
            continue
        if kind == "v8":
            meta = v8_meta[pool].get(sub_hash)
            if meta is None:
                continue
            yaml_path = repo_root / meta["path"]
            sign_to_phoneme = extract_v8_sign_to_phoneme(yaml_path)
            surface = meta["surface"]
            if surface not in flat_top20[pool]:
                continue
            for sign, phoneme in sign_to_phoneme.items():
                histograms[sign][phoneme] += 1
                contributing[sign][surface][pool] += 1
                per_surface_targets[(pool, surface)][sign][phoneme] += 1
        else:
            meta = v9_meta[pool].get(sub_hash)
            if meta is None:
                continue
            yaml_path = repo_root / meta["path"]
            roots = extract_v9_root_sign_to_phoneme(yaml_path)
            for root in roots:
                surface = root["surface"]
                if surface not in flat_top20[pool]:
                    continue
                for sign, phoneme in root["sign_to_phoneme"].items():
                    histograms[sign][phoneme] += 1
                    contributing[sign][surface][pool] += 1
                    per_surface_targets[(pool, surface)][sign][phoneme] += 1

    # Convert nested defaultdicts to plain dicts for stable serialization.
    histograms_out = {s: dict(h) for s, h in histograms.items()}
    contributing_out = {
        s: {surf: dict(slots) for surf, slots in surfs.items()}
        for s, surfs in contributing.items()
    }
    per_surface_targets_out = {
        ks: {sign: dict(ph) for sign, ph in signs.items()}
        for ks, signs in per_surface_targets.items()
    }

    return {
        "histograms": histograms_out,
        "contributing_surfaces": contributing_out,
        "per_surface_targets": per_surface_targets_out,
        "n_records_seen": n_records_seen,
        "n_positive_records": n_positive_records,
        "union_top20": sorted(union_top20),
    }


# ---------------------------------------------------------------------------
# Per-sign consensus statistics
# ---------------------------------------------------------------------------


def _shannon_entropy_bits(counts: Iterable[int]) -> float:
    counts = [c for c in counts if c > 0]
    total = sum(counts)
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts:
        p = c / total
        h -= p * math.log2(p)
    return h


def per_sign_consensus(
    histograms: dict[str, dict[str, int]],
    *,
    n_min: int,
    alpha: float,
    vocab_size: int,
    top_alternatives: int = 3,
) -> list[dict]:
    """One row per sign with n_proposals ≥ n_min."""
    rows: list[dict] = []
    for sign in sorted(histograms.keys()):
        hist = histograms[sign]
        n_proposals = sum(hist.values())
        if n_proposals < n_min:
            continue
        # Sort by (-count, phoneme) so ties resolve deterministically.
        sorted_phonemes = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))
        modal_phoneme, modal_count = sorted_phonemes[0]
        # Smoothed Dirichlet-multinomial posterior with symmetric prior
        # α over a vocabulary of size V. Posterior mean for phoneme i:
        # (n_i + α) / (N + α * V).
        denom = n_proposals + alpha * vocab_size
        modal_posterior = (modal_count + alpha) / denom
        entropy_bits = _shannon_entropy_bits(hist.values())
        alternatives: list[dict] = []
        for ph, cnt in sorted_phonemes[1 : 1 + top_alternatives]:
            alternatives.append(
                {
                    "phoneme": ph,
                    "count": cnt,
                    "posterior": (cnt + alpha) / denom,
                }
            )
        rows.append(
            {
                "sign": sign,
                "n_proposals": n_proposals,
                "n_distinct_phonemes": len(hist),
                "modal_phoneme": modal_phoneme,
                "modal_count": modal_count,
                "modal_posterior": modal_posterior,
                "entropy_bits": entropy_bits,
                "alternatives": alternatives,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Cross-window coherence test
# ---------------------------------------------------------------------------


def per_surface_coherence(
    *,
    per_surface_targets: dict[tuple[str, str], dict[str, dict[str, int]]],
    modal_posterior_by_sign: dict[str, float],
) -> dict[tuple[str, str], dict]:
    """(pool, surface) → {coherence, n_signs_targeted, n_proposals_total}.

    Coherence(S) = Σ_s [freq(S, s) * P_modal(s)] / Σ_s freq(S, s)
    where freq(S, s) is the number of times S's positive-paired-diff
    equations targeted sign s, and P_modal(s) is the modal-phoneme
    posterior for sign s in the global consensus map.

    Signs not in the consensus map (filtered out by n_min) are skipped,
    so a surface whose signs all fall below the consensus threshold
    yields a NaN coherence (reported but excluded from per-pool median).
    """
    out: dict[tuple[str, str], dict] = {}
    for (pool, surface), signs in per_surface_targets.items():
        weighted_sum = 0.0
        total_weight = 0
        n_signs_in_consensus = 0
        n_proposals_total = 0
        for sign, ph_counts in signs.items():
            freq = sum(ph_counts.values())
            n_proposals_total += freq
            modal = modal_posterior_by_sign.get(sign)
            if modal is None:
                continue
            n_signs_in_consensus += 1
            weighted_sum += freq * modal
            total_weight += freq
        coherence = (weighted_sum / total_weight) if total_weight > 0 else float("nan")
        out[(pool, surface)] = {
            "pool": pool,
            "surface": surface,
            "coherence": coherence,
            "n_signs_targeted": len(signs),
            "n_signs_in_consensus": n_signs_in_consensus,
            "n_proposals_total": n_proposals_total,
        }
    return out


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def per_pool_coherence(
    surface_stats: dict[tuple[str, str], dict],
    top20_by_pool: dict[str, tuple[str, ...]],
    *,
    coherence_floor: float,
) -> dict[str, dict]:
    """Per-pool median over per-surface coherence (NaN-skipping)."""
    out: dict[str, dict] = {}
    for pool, surfaces in top20_by_pool.items():
        values: list[float] = []
        per_surface: list[dict] = []
        for s in surfaces:
            stat = surface_stats.get((pool, s))
            if stat is None:
                per_surface.append(
                    {
                        "surface": s,
                        "coherence": float("nan"),
                        "n_signs_targeted": 0,
                        "n_signs_in_consensus": 0,
                        "n_proposals_total": 0,
                    }
                )
                continue
            per_surface.append(
                {
                    "surface": s,
                    "coherence": stat["coherence"],
                    "n_signs_targeted": stat["n_signs_targeted"],
                    "n_signs_in_consensus": stat["n_signs_in_consensus"],
                    "n_proposals_total": stat["n_proposals_total"],
                }
            )
            if not math.isnan(stat["coherence"]):
                values.append(stat["coherence"])
        median = _median(values)
        out[pool] = {
            "pool": pool,
            "n_surfaces": len(surfaces),
            "n_surfaces_with_coherence": len(values),
            "median_coherence": median,
            "max_coherence": max(values) if values else float("nan"),
            "min_coherence": min(values) if values else float("nan"),
            "gate": (
                "PASS"
                if not math.isnan(median) and median >= coherence_floor
                else "FAIL"
            ),
            "per_surface": per_surface,
        }
    return out


# ---------------------------------------------------------------------------
# Refined-gate sensitivity (Linear-B carryover, K ∈ {5, 10, 20})
# ---------------------------------------------------------------------------


def refined_gate_sensitivity(
    *,
    pool: str,
    auto_dir: Path,
    auto_sig_dir: Path,
    pools_dir: Path,
    results_dir: Path,
    language_dispatch: dict[str, str],
    n_min: int,
    k_values: list[int],
) -> list[dict]:
    """Re-run the v10 right-tail one-tail MW U gate at each K.

    No code change to the production rollup. This is a pure diagnostic:
    rebuild the same per-surface posterior table the production rollup
    uses, then call the same MW U at the swept K values.
    """
    score_rows = _load_score_rows(results_dir)
    pool_phonemes = _load_pool_phonemes(pools_dir)
    records: list[dict] = []
    records.extend(
        build_v8_records(
            pool=pool,
            auto_dir=auto_dir,
            score_rows=score_rows,
            pool_phonemes=pool_phonemes,
            language_dispatch=language_dispatch,
        )
    )
    records.extend(
        build_v9_records(
            pool=pool,
            auto_dir=auto_sig_dir,
            score_rows=score_rows,
            language_dispatch=language_dispatch,
        )
    )
    aggregates = aggregate_per_surface(records)
    rows = build_posterior_rows(aggregates, n_min=n_min)
    sub_rows = [r for r in rows if r["substrate_pool"] == pool and r["side"] == "substrate"]
    ctrl_rows = [r for r in rows if r["substrate_pool"] == pool and r["side"] == "control"]

    out: list[dict] = []
    for k in k_values:
        sub_top = sorted(sub_rows, key=lambda r: -r["posterior_mean"])[:k]
        ctrl_top = sorted(ctrl_rows, key=lambda r: -r["posterior_mean"])[:k]
        sub_means = [r["posterior_mean"] for r in sub_top]
        ctrl_means = [r["posterior_mean"] for r in ctrl_top]
        u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
        sub_top_max = max(sub_means) if sub_means else float("nan")
        ctrl_top_max = max(ctrl_means) if ctrl_means else float("nan")
        # "fraction-of-top-K-substrate-surfaces-with-posterior > control-top-K-max"
        if sub_means and not math.isnan(ctrl_top_max):
            frac_above = sum(1 for v in sub_means if v > ctrl_top_max) / len(sub_means)
        else:
            frac_above = float("nan")
        out.append(
            {
                "K": k,
                "n_substrate_top": na,
                "n_control_top": nb,
                "median_substrate_top": _median(sub_means),
                "median_control_top": _median(ctrl_means),
                "max_substrate_top": sub_top_max,
                "max_control_top": ctrl_top_max,
                "mw_u_substrate": u,
                "mw_p_one_tail": p,
                "frac_substrate_above_control_top_max": frac_above,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt(x: float, w: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "nan"
    return f"{x:.{w}f}"


def render_consensus_md(
    *,
    consensus_rows: list[dict],
    contributing_surfaces: dict[str, dict[str, dict[str, int]]],
    surface_coherence: dict[str, dict],
    sensitivity: list[dict],
    n_min: int,
    alpha: float,
    vocab_size: int,
    coherence_floor: float,
    summary: dict,
) -> str:
    out: list[str] = []
    out.append("# Consensus sign-to-phoneme map (mg-c216, harness v13)\n")
    out.append(
        "Generated by `scripts/consensus_map.py`. For each Linear A sign s "
        "appearing in at least "
        f"{n_min} positive-paired-diff candidate equations whose substrate "
        "surface is in the v10 (mg-d26d) Aquitanian or Etruscan top-20, "
        "we report the histogram of phonemes proposed for s by those "
        "candidates. Modal posterior is computed under a symmetric "
        f"Dirichlet-multinomial prior with α={alpha:g} and "
        f"vocabulary size V={vocab_size} (the number of distinct phonemes "
        "observed across the consensus dataset). Entropy is computed on "
        "the maximum-likelihood histogram (no smoothing) in bits.\n"
    )
    out.append(
        "**Inputs.** Built from "
        f"`results/experiments.external_phoneme_perplexity_v0.jsonl` + the "
        "v8 (`hypotheses/auto/{aquitanian,etruscan}.manifest.jsonl`) and "
        "v9 (`hypotheses/auto_signatures/{aquitanian,etruscan}.manifest."
        "jsonl`) substrate manifests. Only candidates with positive "
        "`paired_diff = substrate_score − control_score` against the "
        "matched control are aggregated; \"wrong\" mappings (negative "
        "paired_diff) are not in the consensus.\n"
    )
    out.append(
        "**Determinism.** Identical output across re-runs given the same "
        "result stream and manifests + hypothesis YAMLs. No RNG.\n"
    )

    # Coherence verdict — central headline.
    out.append("## Cross-window coherence test\n")
    out.append(
        f"For each v10 top-20 substrate surface S, the **coherence** "
        "statistic is Σ_s [freq(S, s) · P_modal(s)] / Σ_s freq(S, s) where "
        "freq(S, s) is the number of times S's positive-paired-diff "
        "equations targeted sign s and P_modal(s) is the modal-phoneme "
        "posterior for s in the global consensus map. Per-pool coherence "
        f"is the median of per-surface coherences. Acceptance gate: at "
        f"least one pool's median ≥ {coherence_floor:g}.\n"
    )
    out.append(
        "| pool | n_surfaces | n_surfaces_with_coherence | "
        "median coherence | min | max | gate (≥{:g}) |".format(coherence_floor)
    )
    out.append("|:--|---:|---:|---:|---:|---:|:--:|")
    for pool in ("aquitanian", "etruscan"):
        cs = surface_coherence.get(pool)
        if cs is None:
            continue
        out.append(
            "| {pool} | {n} | {nc} | {med} | {mn} | {mx} | {gate} |".format(
                pool=pool,
                n=cs["n_surfaces"],
                nc=cs["n_surfaces_with_coherence"],
                med=_fmt(cs["median_coherence"]),
                mn=_fmt(cs["min_coherence"]),
                mx=_fmt(cs["max_coherence"]),
                gate=cs["gate"],
            )
        )
    out.append("")

    out.append(
        "### Per-surface coherence (full table)\n"
    )
    out.append(
        "| pool | surface | coherence | n_signs_targeted | "
        "n_signs_in_consensus | n_proposals_total |"
    )
    out.append("|:--|:--|---:|---:|---:|---:|")
    for pool in ("aquitanian", "etruscan"):
        cs = surface_coherence.get(pool)
        if cs is None:
            continue
        for row in cs["per_surface"]:
            out.append(
                "| {pool} | `{surf}` | {coh} | {nt} | {nc} | {np} |".format(
                    pool=pool,
                    surf=row["surface"],
                    coh=_fmt(row["coherence"]),
                    nt=row["n_signs_targeted"],
                    nc=row["n_signs_in_consensus"],
                    np=row["n_proposals_total"],
                )
            )
    out.append("")

    # Refined-gate sensitivity (Linear-B carryover positive control).
    out.append("## Refined-gate sensitivity for Linear-B positive control\n")
    out.append(
        "Recomputes the right-tail one-tail Mann-Whitney U gate on "
        "`linear_b_carryover` with K ∈ {5, 10, 20}. The production rollup "
        "(`scripts/per_surface_bayesian_rollup.py`) is unchanged; this is "
        "a diagnostic for the merge note. K=20 is the production gate "
        "(matches mg-4664's reported p=0.155).\n"
    )
    out.append(
        "| K | n_substrate_top | n_control_top | median substrate | "
        "median control | max substrate | max control | MW U | "
        "p (one-tail, sub>ctrl) | frac substrate > max(control) |"
    )
    out.append(
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    )
    for row in sensitivity:
        out.append(
            "| {k} | {ns} | {nc} | {ms} | {mc} | {xs} | {xc} | "
            "{u:.1f} | {p} | {f} |".format(
                k=row["K"],
                ns=row["n_substrate_top"],
                nc=row["n_control_top"],
                ms=_fmt(row["median_substrate_top"]),
                mc=_fmt(row["median_control_top"]),
                xs=_fmt(row["max_substrate_top"]),
                xc=_fmt(row["max_control_top"]),
                u=row["mw_u_substrate"],
                p=_fmt(row["mw_p_one_tail"]),
                f=_fmt(row["frac_substrate_above_control_top_max"], 3),
            )
        )
    out.append("")

    # Consensus map — the publishable-shape output.
    out.append(
        "## Consensus sign-to-phoneme map "
        f"(n_proposals ≥ {n_min}, sorted by entropy ascending)\n"
    )
    out.append(
        "Each row: one Linear A sign with at least "
        f"{n_min} positive-paired-diff proposals from v10-top-20 "
        "substrate surfaces. Lower entropy = more concentrated "
        "consensus. `modal_posterior` is the smoothed Dirichlet-"
        "multinomial posterior for the modal phoneme. `alternatives` "
        "lists the next 3 phonemes by raw count.\n"
    )
    out.append(
        f"**Total:** {len(consensus_rows)} signs above the threshold "
        f"(of {summary['n_signs_with_any_proposal']} signs with ≥1 "
        f"proposal). Aggregated from {summary['n_positive_records']} "
        f"positive-paired-diff records (out of "
        f"{summary['n_records_seen']} total substrate records).\n"
    )
    out.append(
        "| sign | n_proposals | modal | modal_posterior | entropy_bits | "
        "alternatives | contributing v10 surfaces |"
    )
    out.append("|:--|---:|:--|---:|---:|:--|:--|")
    rows_sorted = sorted(
        consensus_rows,
        key=lambda r: (r["entropy_bits"], -r["n_proposals"], r["sign"]),
    )
    for row in rows_sorted:
        sign = row["sign"]
        alts = ", ".join(
            f"{a['phoneme']}={a['count']} ({a['posterior']:.3f})"
            for a in row["alternatives"]
        ) or "—"
        surfs = sorted(contributing_surfaces.get(sign, {}).keys())
        surfs_fmt = ", ".join(f"`{s}`" for s in surfs) or "—"
        out.append(
            "| `{sign}` | {n} | `{modal}` | {mp} | {ent} | {alts} | "
            "{surfs} |".format(
                sign=sign,
                n=row["n_proposals"],
                modal=row["modal_phoneme"],
                mp=f"{row['modal_posterior']:.4f}",
                ent=f"{row['entropy_bits']:.3f}",
                alts=alts,
                surfs=surfs_fmt,
            )
        )
    out.append("")

    out.append("## Notes\n")
    out.append(
        "- *Why positive-paired-diff only?* Negative-paired-diff records "
        "represent equations where the substrate side LOST against its "
        "matched control under the same-LM phoneme LM. Including them "
        "would inject \"wrong\" sign-to-phoneme mappings into the "
        "histogram and bias the consensus toward the noise floor.\n"
    )
    out.append(
        "- *Why restrict to v10 top-20?* The v10 PASSes are the only "
        "substrate surfaces that beat their matched controls under the "
        "same-LM gate. Restricting the consensus to those surfaces' "
        "equations asks: *given the surfaces we believe most likely to "
        "be correct readings, do their proposed sign mappings agree?*\n"
    )
    out.append(
        "- *Symmetric Dirichlet prior.* α applies uniformly across V "
        "= number of distinct phonemes observed in the consensus "
        "dataset. The modal posterior is therefore (n_modal + α) / "
        "(N + α·V). For typical sign-counts n in the 30–500 range and "
        "V ≈ 25, the smoothing is small but non-zero.\n"
    )
    out.append(
        "- *Why entropy in bits?* Bits make the scale interpretable: "
        "a sign with two equally-proposed phonemes has entropy = 1.0 "
        "bit; a sign with four equally-proposed phonemes has 2.0 "
        "bits; a sign with one dominant phoneme has entropy → 0.\n"
    )
    out.append(
        "- *Coherence statistic interpretation.* For a v10 top-20 "
        "substrate surface S, coherence(S) is the freq-weighted "
        "average modal-phoneme posterior over the signs S targets. "
        "If S's equations consistently target signs whose modal "
        "phoneme is nearly unanimous, coherence(S) is high. If S "
        "targets signs whose proposals scatter across phonemes, "
        "coherence(S) is low. Per-pool median sweeps S over the v10 "
        "top-20.\n"
    )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    parser.add_argument("--auto-dir", type=Path, default=_DEFAULT_AUTO)
    parser.add_argument("--auto-sig-dir", type=Path, default=_DEFAULT_AUTO_SIG)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repo root (used to resolve hypothesis_path entries).",
    )
    parser.add_argument(
        "--pools",
        type=str,
        default="aquitanian,etruscan",
        help="Comma-separated substrate pools to draw v10 top-20 from.",
    )
    parser.add_argument(
        "--n-min",
        type=int,
        default=10,
        help="Minimum number of positive-paired-diff proposals required "
             "for a sign to appear in the consensus map.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="Symmetric Dirichlet prior concentration. Default 0.5 "
             "(Jeffreys).",
    )
    parser.add_argument(
        "--coherence-floor",
        type=float,
        default=0.6,
        help="Per-pool median per-surface coherence acceptance bar. "
             "Default 0.6 per the mg-c216 brief.",
    )
    parser.add_argument(
        "--linear-b-pool",
        type=str,
        default="linear_b_carryover",
        help="Pool name for the refined-gate sensitivity check.",
    )
    parser.add_argument(
        "--ks",
        type=str,
        default="5,10,20",
        help="Comma-separated K values for the refined-gate sweep.",
    )
    parser.add_argument(
        "--n-min-rollup",
        type=int,
        default=10,
        help="n_min credibility cap passed to build_posterior_rows for "
             "the refined-gate sensitivity (matches the production rollup).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output Markdown path. Default results/consensus_sign_phoneme_map.md.",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path for a summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    top20 = {p: _V10_TOP20_BY_POOL[p] for p in pools if p in _V10_TOP20_BY_POOL}
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    proposals = collect_sign_phoneme_proposals(
        pools=pools,
        top20_by_pool=top20,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        pools_dir=args.pools_dir,
        results_dir=args.results_dir,
        repo_root=args.repo_root,
        language_dispatch=language_dispatch,
    )

    histograms = proposals["histograms"]
    contributing = proposals["contributing_surfaces"]
    per_surface_targets = proposals["per_surface_targets"]

    # Vocabulary size = distinct phonemes observed across all signs.
    # Deterministic given the input. Used as V in the smoothed posterior.
    distinct_phonemes: set[str] = set()
    for hist in histograms.values():
        distinct_phonemes.update(hist.keys())
    vocab_size = max(1, len(distinct_phonemes))

    consensus_rows = per_sign_consensus(
        histograms,
        n_min=args.n_min,
        alpha=args.alpha,
        vocab_size=vocab_size,
    )

    # Coherence test.
    modal_by_sign = {row["sign"]: row["modal_posterior"] for row in consensus_rows}
    surface_stats = per_surface_coherence(
        per_surface_targets=per_surface_targets,
        modal_posterior_by_sign=modal_by_sign,
    )
    pool_coherence = per_pool_coherence(
        surface_stats, top20, coherence_floor=args.coherence_floor
    )

    # Refined-gate sensitivity.
    k_values = sorted({int(k.strip()) for k in args.ks.split(",") if k.strip()})
    sensitivity = refined_gate_sensitivity(
        pool=args.linear_b_pool,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        pools_dir=args.pools_dir,
        results_dir=args.results_dir,
        language_dispatch=language_dispatch,
        n_min=args.n_min_rollup,
        k_values=k_values,
    )

    summary = {
        "n_records_seen": proposals["n_records_seen"],
        "n_positive_records": proposals["n_positive_records"],
        "n_signs_with_any_proposal": len(histograms),
        "n_signs_above_threshold": len(consensus_rows),
        "vocab_size": vocab_size,
        "alpha": args.alpha,
        "n_min": args.n_min,
        "coherence_floor": args.coherence_floor,
        "pool_coherence": pool_coherence,
        "refined_gate_sensitivity": sensitivity,
    }

    text = render_consensus_md(
        consensus_rows=consensus_rows,
        contributing_surfaces=contributing,
        surface_coherence=pool_coherence,
        sensitivity=sensitivity,
        n_min=args.n_min,
        alpha=args.alpha,
        vocab_size=vocab_size,
        coherence_floor=args.coherence_floor,
        summary=summary,
    )

    out_path = args.out or (args.results_dir / "consensus_sign_phoneme_map.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
