#!/usr/bin/env python3
"""Per-surface bayesian posterior aggregation over v8 + v9 paired-diff data (mg-d26d).

Pivots the *aggregation* (not the metric or hypothesis shape). v8
single-root candidates and v9 multi-root signatures both emit
``paired_diff = substrate_score − control_score`` under the held-out
external phoneme LM ``external_phoneme_perplexity_v0``. The
population-level Wilcoxon gate (mg-bef2) collapses concentrated and
dispersed evidence identically; this rollup instead computes a per-
surface Beta-binomial posterior over

    θ_S = P(this surface is real Linear-A substrate vocabulary)

using the *sign* of paired_diff as binary evidence.

For each pool P ∈ {aquitanian, etruscan, toponym}:

  * Substrate side, for each surface S that appears in either a v8
    single-root candidate (``pool_entry_surface == S``) or any v9
    multi-root signature (``S in root_surfaces``): collect every
    paired_diff record where S appears. paired_diff > 0 → success,
    ≤ 0 → failure. Posterior = Beta(1+k, 1+n−k) under a Beta(1,1)
    prior; posterior mean = (1+k)/(2+n); 95% credible interval from
    the inverse-CDF.

  * Control side, same procedure on the matched control pool's
    signatures + control candidates. The binary observation is
    flipped (paired_diff < 0 → control wins → success), so the
    posterior reads "P(this control surface beats its substrate)".
    Apples-to-apples with the substrate posterior.

Credibility cap: ``credibility = min(1, n/n_min)`` with ``n_min=10``
(configurable). Surfaces with n < n_min are downweighted but not
excluded; ranking is by the credibility-shrunk effective score

    effective = credibility * posterior_mean + (1 − credibility) * 0.5

so a surface with 1 record at paired_diff > 0 (raw posterior 2/3) is
shrunk toward the prior mean 0.5 rather than leading the leaderboard.

Acceptance gate (mg-d26d, right-tail by construction)
=====================================================
For at least one substrate pool: a one-tail Mann-Whitney U on the
top-20 substrate surfaces' posterior means vs the top-20 control
surfaces' posterior means must satisfy p < 0.05 with substrate >
control. The full-distribution Wilcoxon (which mg-bef2 failed for the
right reasons) is not the right test for this data shape; the right-
tail comparison asks whether the *best* substrate surfaces beat the
*best* control surfaces.

Output
======
  results/rollup.bayesian_posterior.<pool>.md    (per pool, controls interleaved)
  results/rollup.bayesian_posterior.md           (combined view across pools)

Re-runs are deterministic given the result stream and the manifests.

Usage
=====
  python3 scripts/per_surface_bayesian_rollup.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RESULTS_DIR = _REPO_ROOT / "results"
_DEFAULT_AUTO = _REPO_ROOT / "hypotheses" / "auto"
_DEFAULT_AUTO_SIG = _REPO_ROOT / "hypotheses" / "auto_signatures"
_DEFAULT_POOLS = _REPO_ROOT / "pools"

_METRIC = "external_phoneme_perplexity_v0"
_SUBSTRATE_POOLS: tuple[str, ...] = (
    "aquitanian",
    "etruscan",
    "toponym",
    "linear_b_carryover",
    "polluted_aquitanian",
    "greek_polluted_aquitanian",
    # mg-9f18 (harness v18): pollution-level sweep variants and
    # toponym bigram-control re-evaluation pool. The toponym pool
    # itself stays in the substrate list and gets paired against
    # `control_toponym_bigram` in the v18 dedicated analysis script;
    # we don't add it here a second time.
    "polluted_aquitanian_10pct",
    "polluted_aquitanian_25pct",
    "polluted_aquitanian_75pct",
)
_DEFAULT_NMIN = 10
_DEFAULT_TOP_PER_POOL = 50
_DEFAULT_TOP_K_GATE = 20

# Default same-LM dispatch: substrate-pool name → external phoneme LM.
# Mirrors ``scripts/run_sweep._EXT_POOL_LANGUAGE``. Used to *filter* the
# row stream so cross-LM rows added by mg-0f97's negative control do
# not contaminate the same-LM rollup. Override via --language-dispatch.
_DEFAULT_LANGUAGE_DISPATCH: dict[str, str] = {
    "aquitanian": "basque",
    "control_aquitanian": "basque",
    "etruscan": "etruscan",
    "control_etruscan": "etruscan",
    "toponym": "basque",
    "control_toponym": "basque",
    "linear_b_carryover": "mycenaean_greek",
    "control_linear_b_carryover": "mycenaean_greek",
    "polluted_aquitanian": "basque",
    "control_polluted_aquitanian": "basque",
    "greek_polluted_aquitanian": "basque",
    "control_greek_polluted_aquitanian": "basque",
    # mg-9f18 (harness v18): pollution-level sweep variants and
    # toponym bigram-preserving control. Same Basque LM as the
    # underlying substrates.
    "polluted_aquitanian_10pct": "basque",
    "control_polluted_aquitanian_10pct": "basque",
    "polluted_aquitanian_25pct": "basque",
    "control_polluted_aquitanian_25pct": "basque",
    "polluted_aquitanian_75pct": "basque",
    "control_polluted_aquitanian_75pct": "basque",
    "control_toponym_bigram": "basque",
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def _load_manifest(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _load_score_rows(results_dir: Path) -> dict[tuple[str, str], dict]:
    """(hash, language) → most-recent-by-ran_at result row for the bayesian
    metric.

    Keying on (hypothesis_hash, language) lets multiple LM rescores of
    the same hypothesis coexist in the result stream — important for
    mg-0f97's cross-LM negative control, which appends rows with the
    *swapped* substrate LM under the same hypothesis_hash. Callers select
    the row for a given (hash, expected_language) pair via
    :func:`pick_score_row`.
    """
    out: dict[tuple[str, str], dict] = {}
    # Primary stream + per-metric sidecar + per-pool sidecars
    # (e.g. ``experiments.external_phoneme_perplexity_v0.polluted.jsonl``,
    # added in mg-6b73 to keep individual files under GitHub's 100 MB
    # push-size limit).
    paths = [
        results_dir / "experiments.jsonl",
        results_dir / f"experiments.{_METRIC}.jsonl",
    ]
    paths.extend(sorted(results_dir.glob(f"experiments.{_METRIC}.*.jsonl")))
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row.get("metric") != _METRIC:
                    continue
                h = row.get("hypothesis_hash")
                if not h:
                    continue
                lang = row.get("language", "")
                key = (h, lang)
                cur = out.get(key)
                if cur is None or row.get("ran_at", "") > cur.get("ran_at", ""):
                    out[key] = row
    return out


def pick_score_row(
    score_rows: dict[tuple[str, str], dict],
    h_hash: str,
    language: str,
) -> dict | None:
    """Look up the most-recent score row for a given (hash, language)."""
    return score_rows.get((h_hash, language))


def _load_pool_phonemes(pools_dir: Path) -> dict[str, list[list[str]]]:
    """pool_name → list[phoneme_sequence] indexed by pool_entry_index.

    Used only to break ties when matching a v8 substrate candidate to a
    v8 control candidate at the same (inscription, span). Hand-rolled
    YAML reader (no extra dep) — the entries we need are small + flat.
    """
    import yaml  # pyyaml is already a runtime dependency

    class _StringDateLoader(yaml.SafeLoader):
        pass

    _StringDateLoader.yaml_implicit_resolvers = {
        k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    out: dict[str, list[list[str]]] = {}
    for path in sorted(pools_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=_StringDateLoader)
        if not doc:
            continue
        pool = doc["pool"]
        out[pool] = [list(e["phonemes"]) for e in doc.get("entries", [])]
    return out


# ---------------------------------------------------------------------------
# v8 single-root pairing (mirrors paired_diff_rollup logic)
# ---------------------------------------------------------------------------


def _edit_distance(a: list[str], b: list[str]) -> int:
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[m]


def build_v8_records(
    *,
    pool: str,
    auto_dir: Path,
    score_rows: dict[tuple[str, str], dict],
    pool_phonemes: dict[str, list[list[str]]],
    language_dispatch: dict[str, str],
    control_pool: str | None = None,
) -> list[dict]:
    """Return one paired_diff record per substrate v8 candidate that has
    an exact-window control match in ``control_<pool>``. Each record
    carries the *substrate* and *control* surfaces so per-surface
    aggregation can read both sides off a single record.

    ``control_pool`` defaults to ``f"control_{pool}"`` — the standard
    matched-control naming. Override it (mg-9f18 / v18 toponym bigram
    re-evaluation) to pair the substrate against a non-default control,
    e.g. ``pool='toponym', control_pool='control_toponym_bigram'``.
    """
    if control_pool is None:
        control_pool = f"control_{pool}"
    sub_path = auto_dir / f"{pool}.manifest.jsonl"
    ctrl_path = auto_dir / f"{control_pool}.manifest.jsonl"
    sub_rows = _load_manifest(sub_path)
    ctrl_rows = _load_manifest(ctrl_path)
    if not sub_rows or not ctrl_rows:
        return []

    by_window: dict[tuple[str, int, int], list[dict]] = defaultdict(list)
    for row in ctrl_rows:
        key = (row["inscription_id"], int(row["span_start"]), int(row["span_end"]))
        by_window[key].append(row)

    sub_phon = pool_phonemes.get(pool, [])
    ctrl_phon = pool_phonemes.get(control_pool, [])
    sub_lang = language_dispatch.get(pool, "")
    ctrl_lang = language_dispatch.get(control_pool, sub_lang)

    records: list[dict] = []
    for sub in sub_rows:
        sub_hash = sub["hypothesis_hash"]
        sub_score_row = pick_score_row(score_rows, sub_hash, sub_lang)
        if sub_score_row is None:
            continue
        key = (sub["inscription_id"], int(sub["span_start"]), int(sub["span_end"]))
        candidates = by_window.get(key, [])
        if not candidates:
            continue
        sub_seq = sub_phon[sub["pool_entry_index"]] if sub_phon else []

        best: dict | None = None
        best_d = math.inf
        for c in sorted(candidates, key=lambda r: r["hypothesis_hash"]):
            c_hash = c["hypothesis_hash"]
            if pick_score_row(score_rows, c_hash, ctrl_lang) is None:
                continue
            c_seq = ctrl_phon[c["pool_entry_index"]] if ctrl_phon else []
            d = _edit_distance(sub_seq, c_seq)
            if d < best_d:
                best_d = d
                best = c
        if best is None:
            continue
        ctrl_score_row = pick_score_row(score_rows, best["hypothesis_hash"], ctrl_lang)
        if ctrl_score_row is None:
            continue
        sub_score = float(sub_score_row.get("score", 0.0))
        ctrl_score = float(ctrl_score_row.get("score", 0.0))
        records.append(
            {
                "kind": "v8",
                "pool": pool,
                "control_pool": control_pool,
                "substrate_surfaces": (sub["pool_entry_surface"],),
                "control_surfaces": (best["pool_entry_surface"],),
                "substrate_score": sub_score,
                "control_score": ctrl_score,
                "paired_diff": sub_score - ctrl_score,
                "substrate_hash": sub_hash,
                "control_hash": best["hypothesis_hash"],
            }
        )
    return records


# ---------------------------------------------------------------------------
# v9 multi-root pairing (mirrors paired_diff_signature_rollup logic)
# ---------------------------------------------------------------------------


def build_v9_records(
    *,
    pool: str,
    auto_dir: Path,
    score_rows: dict[tuple[str, str], dict],
    language_dispatch: dict[str, str],
    control_pool: str | None = None,
) -> list[dict]:
    """Return one paired_diff record per substrate v9 signature that has
    a matched control (paired_substrate_hash). Carries both substrate
    and control root_surfaces.

    ``control_pool`` defaults to ``f"control_{pool}"``; the same override
    semantics apply as :func:`build_v8_records`.
    """
    if control_pool is None:
        control_pool = f"control_{pool}"
    sub_path = auto_dir / f"{pool}.manifest.jsonl"
    ctrl_path = auto_dir / f"{control_pool}.manifest.jsonl"
    sub_rows = _load_manifest(sub_path)
    ctrl_rows = _load_manifest(ctrl_path)
    if not sub_rows or not ctrl_rows:
        return []

    ctrl_by_paired: dict[str, dict] = {}
    for row in ctrl_rows:
        ctrl_by_paired[row["paired_substrate_hash"]] = row

    sub_lang = language_dispatch.get(pool, "")
    ctrl_lang = language_dispatch.get(control_pool, sub_lang)

    records: list[dict] = []
    for sub in sub_rows:
        sub_hash = sub["hypothesis_hash"]
        ctrl = ctrl_by_paired.get(sub_hash)
        if ctrl is None:
            continue
        sub_score_row = pick_score_row(score_rows, sub_hash, sub_lang)
        ctrl_score_row = pick_score_row(score_rows, ctrl["hypothesis_hash"], ctrl_lang)
        if sub_score_row is None or ctrl_score_row is None:
            continue
        sub_score = float(sub_score_row.get("score", 0.0))
        ctrl_score = float(ctrl_score_row.get("score", 0.0))
        records.append(
            {
                "kind": "v9",
                "pool": pool,
                "control_pool": control_pool,
                "substrate_surfaces": tuple(sub["root_surfaces"]),
                "control_surfaces": tuple(ctrl["root_surfaces"]),
                "substrate_score": sub_score,
                "control_score": ctrl_score,
                "paired_diff": sub_score - ctrl_score,
                "substrate_hash": sub_hash,
                "control_hash": ctrl["hypothesis_hash"],
            }
        )
    return records


# ---------------------------------------------------------------------------
# Per-surface aggregation
# ---------------------------------------------------------------------------


def aggregate_per_surface(records: list[dict]) -> dict[tuple[str, str], dict]:
    """(pool_kind, surface) → {n, k, n_v8, n_v9, k_v8, k_v9, paired_diffs}.

    A signature with surfaces ["ur", "ur"] contributes one observation
    under "ur" — surfaces are deduplicated per-record so the same window
    cannot double-vote for the same surface.

    pool_kind is the substrate pool name on the substrate side (e.g.
    "aquitanian") or the control pool name on the control side
    (e.g. "control_aquitanian"). The substrate side counts a paired_diff
    > 0 as a success; the control side flips and counts paired_diff < 0
    as a success (control beat substrate).
    """
    out: dict[tuple[str, str], dict] = defaultdict(
        lambda: {
            "n": 0,
            "k": 0,
            "n_v8": 0,
            "k_v8": 0,
            "n_v9": 0,
            "k_v9": 0,
            "paired_diffs": [],
        }
    )

    for rec in records:
        pd = rec["paired_diff"]
        kind = rec["kind"]
        for s in set(rec["substrate_surfaces"]):
            cell = out[(rec["pool"], s)]
            cell["n"] += 1
            cell["paired_diffs"].append(pd)
            if pd > 0:
                cell["k"] += 1
            if kind == "v8":
                cell["n_v8"] += 1
                if pd > 0:
                    cell["k_v8"] += 1
            else:
                cell["n_v9"] += 1
                if pd > 0:
                    cell["k_v9"] += 1
        for s in set(rec["control_surfaces"]):
            cell = out[(rec["control_pool"], s)]
            cell["n"] += 1
            # control's view: -paired_diff. Sign-only, so we just flip
            # the test and store -pd in paired_diffs for diagnostics.
            cell["paired_diffs"].append(-pd)
            if pd < 0:
                cell["k"] += 1
            if kind == "v8":
                cell["n_v8"] += 1
                if pd < 0:
                    cell["k_v8"] += 1
            else:
                cell["n_v9"] += 1
                if pd < 0:
                    cell["k_v9"] += 1
    return out


# ---------------------------------------------------------------------------
# Beta posterior + Mann-Whitney U
# ---------------------------------------------------------------------------


def _betacf(a: float, b: float, x: float) -> float:
    """Lentz's algorithm for the continued fraction in the regularized
    incomplete beta function. Standard Numerical Recipes."""
    MAXIT = 200
    EPS = 3.0e-14
    FPMIN = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        if abs(d * c - 1.0) < EPS:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b). 0 ≤ x ≤ 1, a > 0, b > 0."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    log_pref = a * math.log(x) + b * math.log(1.0 - x) - lbeta
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(log_pref) * _betacf(a, b, x) / a
    return 1.0 - math.exp(log_pref) * _betacf(b, a, 1.0 - x) / b


def beta_ppf(p: float, a: float, b: float) -> float:
    """Inverse Beta CDF via bisection on betainc (deterministic, no scipy)."""
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if betainc(a, b, mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def beta_posterior(n: int, k: int) -> tuple[float, float, float]:
    """Beta(1+k, 1+n−k) → (mean, ci_low, ci_high) at 95%."""
    a = 1.0 + k
    b = 1.0 + (n - k)
    mean = a / (a + b)
    lo = beta_ppf(0.025, a, b)
    hi = beta_ppf(0.975, a, b)
    return mean, lo, hi


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def mann_whitney_u_one_tail(
    a: list[float], b: list[float]
) -> tuple[float, float, int, int]:
    """One-tail MW-U with normal-approximation p-value (alternative: A > B).

    Returns ``(U_a, p_one_tail, n_a, n_b)``. ``U_a`` is the count of
    pairs where a_i > b_j (with ties contributing 0.5). The
    normal-approximation p includes a tie correction; for the small
    n_a = n_b = 20 cells used by the gate, the asymptotic test is
    slightly conservative but the directionality is unambiguous.
    """
    n_a, n_b = len(a), len(b)
    if n_a == 0 or n_b == 0:
        return 0.0, float("nan"), n_a, n_b
    # Rank-sum implementation (handles ties via mid-rank).
    pooled = sorted(((v, 0) for v in a), key=lambda t: t[0]) + sorted(
        ((v, 1) for v in b), key=lambda t: t[0]
    )
    pooled.sort(key=lambda t: t[0])
    ranks = [0.0] * len(pooled)
    i = 0
    n = len(pooled)
    tie_correction_sum = 0.0
    while i < n:
        j = i
        while j + 1 < n and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for r in range(i, j + 1):
            ranks[r] = avg
        t = j - i + 1
        if t > 1:
            tie_correction_sum += t ** 3 - t
        i = j + 1
    rank_sum_a = sum(rk for rk, (_v, src) in zip(ranks, pooled) if src == 0)
    u_a = rank_sum_a - n_a * (n_a + 1) / 2.0
    mu = n_a * n_b / 2.0
    var = n_a * n_b * (n_a + n_b + 1) / 12.0
    if tie_correction_sum > 0:
        var -= n_a * n_b * tie_correction_sum / (12.0 * (n_a + n_b) * (n_a + n_b - 1))
    if var <= 0:
        return u_a, float("nan"), n_a, n_b
    z = (u_a - mu - 0.5) / math.sqrt(var)
    p_one = 1.0 - _normal_cdf(z)
    return u_a, p_one, n_a, n_b


# ---------------------------------------------------------------------------
# Posterior table assembly
# ---------------------------------------------------------------------------


def build_posterior_rows(
    aggregates: dict[tuple[str, str], dict],
    *,
    n_min: int,
) -> list[dict]:
    """One posterior row per (pool_kind, surface)."""
    out: list[dict] = []
    for (pool_kind, surface), cell in sorted(aggregates.items()):
        n = cell["n"]
        k = cell["k"]
        mean, lo, hi = beta_posterior(n, k)
        cred = min(1.0, n / n_min) if n_min > 0 else 1.0
        eff = cred * mean + (1.0 - cred) * 0.5
        side = "control" if pool_kind.startswith("control_") else "substrate"
        substrate_pool = pool_kind[len("control_") :] if side == "control" else pool_kind
        out.append(
            {
                "pool_kind": pool_kind,
                "substrate_pool": substrate_pool,
                "side": side,
                "surface": surface,
                "n": n,
                "k": k,
                "n_v8": cell["n_v8"],
                "k_v8": cell["k_v8"],
                "n_v9": cell["n_v9"],
                "k_v9": cell["k_v9"],
                "posterior_mean": mean,
                "posterior_ci_low": lo,
                "posterior_ci_high": hi,
                "credibility": cred,
                "effective_score": eff,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt(x: float, w: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "  nan"
    return f"{x:.{w}f}"


def _surface_table_row(rank: int, row: dict) -> str:
    return (
        "| {rank} | {side} | `{surface}` | {n} | {k} | {n_v8} | {n_v9} | "
        "{mean} | {lo} | {hi} | {cred} | {eff} |".format(
            rank=rank,
            side=row["side"],
            surface=row["surface"],
            n=row["n"],
            k=row["k"],
            n_v8=row["n_v8"],
            n_v9=row["n_v9"],
            mean=_fmt(row["posterior_mean"]),
            lo=_fmt(row["posterior_ci_low"]),
            hi=_fmt(row["posterior_ci_high"]),
            cred=_fmt(row["credibility"], 3),
            eff=_fmt(row["effective_score"]),
        )
    )


_SURFACE_TABLE_HEADER = (
    "| rank | side | surface | n | k | n_v8 | n_v9 | "
    "posterior mean | CI low | CI high | credibility | effective |"
)
_SURFACE_TABLE_SEP = "|---:|:--|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"


def _gate_block(
    pool: str,
    sub_top: list[dict],
    ctrl_top: list[dict],
    *,
    top_k_gate: int,
) -> dict:
    sub_means = [r["posterior_mean"] for r in sub_top]
    ctrl_means = [r["posterior_mean"] for r in ctrl_top]
    u, p, na, nb = mann_whitney_u_one_tail(sub_means, ctrl_means)
    median_sub = _median(sub_means)
    median_ctrl = _median(ctrl_means)
    gate = (not math.isnan(p)) and p < 0.05 and median_sub > median_ctrl
    return {
        "pool": pool,
        "top_k_gate": top_k_gate,
        "n_substrate_top": na,
        "n_control_top": nb,
        "median_substrate_top": median_sub,
        "median_control_top": median_ctrl,
        "mw_u_substrate": u,
        "mw_p_one_tail": p,
        "gate": "PASS" if gate else "FAIL",
    }


def _median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def render_pool_md(
    *,
    pool: str,
    rows: list[dict],
    top_per_pool: int,
    top_k_gate: int,
    n_min: int,
    title_suffix: str = "",
) -> tuple[str, dict]:
    pool_rows = [r for r in rows if r["substrate_pool"] == pool]
    sub_rows = [r for r in pool_rows if r["side"] == "substrate"]
    ctrl_rows = [r for r in pool_rows if r["side"] == "control"]

    # Top-K for the gate: ranked purely by posterior_mean (right-tail
    # comparison; the credibility shrinkage is for the leaderboard,
    # not for the gate).
    sub_top = sorted(sub_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    ctrl_top = sorted(ctrl_rows, key=lambda r: -r["posterior_mean"])[:top_k_gate]
    summary = _gate_block(pool, sub_top, ctrl_top, top_k_gate=top_k_gate)

    # Interleaved top-K for the leaderboard: ranked by the credibility-
    # shrunk effective score, both sides combined.
    interleaved = sorted(pool_rows, key=lambda r: -r["effective_score"])[:top_per_pool]

    out: list[str] = []
    suffix = f" {title_suffix}" if title_suffix else ""
    out.append(
        f"# Per-surface bayesian posterior — pool={pool}{suffix} (mg-d26d)\n"
    )
    out.append(
        f"Generated by `scripts/per_surface_bayesian_rollup.py`. Metric: "
        f"`{_METRIC}`. Posterior over θ_S = P(this surface beats its "
        f"matched alternative under the held-out external phoneme LM), "
        f"Beta(1+k, 1+n−k) under a Beta(1, 1) prior. n is the number of "
        f"paired_diff records the surface appears in (v8 single-root + v9 "
        f"multi-root, deduplicated per record); k is the number of those "
        f"records where this side won. `effective` shrinks the posterior "
        f"toward the prior mean 0.5 by `credibility = min(1, n/{n_min})`.\n"
    )
    out.append(
        f"**Acceptance gate (mg-d26d, right-tail):** one-tail Mann-Whitney "
        f"U on the top-{top_k_gate} substrate posterior means vs the "
        f"top-{top_k_gate} control posterior means; p < 0.05 with "
        f"substrate > control passes. Top-K is by posterior_mean only "
        f"(no credibility shrinkage) so the gate sees the right-tail of "
        f"each side's distribution directly.\n"
    )
    out.append("## Pool acceptance gate\n")
    out.append(
        "| pool | n_substrate_top | n_control_top | "
        "median(top substrate posterior) | median(top control posterior) | "
        "MW U (substrate) | MW p (one-tail, substrate>control) | gate |"
    )
    out.append("|:--|---:|---:|---:|---:|---:|---:|:--:|")
    out.append(
        "| {pool} | {ns} | {nc} | {mss:.4f} | {msc:.4f} | {u:.1f} | {p:.4f} | {gate} |".format(
            pool=summary["pool"],
            ns=summary["n_substrate_top"],
            nc=summary["n_control_top"],
            mss=summary["median_substrate_top"],
            msc=summary["median_control_top"],
            u=summary["mw_u_substrate"],
            p=summary["mw_p_one_tail"],
            gate=summary["gate"],
        )
    )
    out.append("")

    out.append(
        f"## {pool} — top {len(interleaved)} surfaces by effective score "
        f"(substrate + control interleaved)\n"
    )
    out.append(_SURFACE_TABLE_HEADER)
    out.append(_SURFACE_TABLE_SEP)
    for i, r in enumerate(interleaved, 1):
        out.append(_surface_table_row(i, r))
    out.append("")

    # Right-tail side-by-side at top-K.
    out.append(
        f"## {pool} — top-{top_k_gate} substrate vs top-{top_k_gate} control "
        f"side-by-side (gate input)\n"
    )
    out.append(
        "| rank | substrate surface | n_s | k_s | posterior_s | "
        "control surface | n_c | k_c | posterior_c |"
    )
    out.append("|---:|:--|---:|---:|---:|:--|---:|---:|---:|")
    pad = max(len(sub_top), len(ctrl_top))
    for i in range(pad):
        s = sub_top[i] if i < len(sub_top) else None
        c = ctrl_top[i] if i < len(ctrl_top) else None
        out.append(
            "| {r} | {ss} | {sn} | {sk} | {sm} | {cs} | {cn} | {ck} | {cm} |".format(
                r=i + 1,
                ss=f"`{s['surface']}`" if s else "—",
                sn=s["n"] if s else "—",
                sk=s["k"] if s else "—",
                sm=_fmt(s["posterior_mean"]) if s else "—",
                cs=f"`{c['surface']}`" if c else "—",
                cn=c["n"] if c else "—",
                ck=c["k"] if c else "—",
                cm=_fmt(c["posterior_mean"]) if c else "—",
            )
        )
    out.append("")

    return "\n".join(out) + "\n", summary


def render_combined_md(
    *,
    rows: list[dict],
    summaries: list[dict],
    top_per_pool: int,
    top_k_gate: int,
    n_min: int,
    title_suffix: str = "",
) -> str:
    out: list[str] = []
    suffix = f" {title_suffix}" if title_suffix else ""
    out.append(
        f"# Per-surface bayesian posterior — combined view{suffix} (mg-d26d)\n"
    )
    out.append(
        f"Generated by `scripts/per_surface_bayesian_rollup.py`. Metric: "
        f"`{_METRIC}`. Reframes the v8 + v9 paired-diff aggregation as a "
        f"per-surface Beta-binomial posterior: each paired_diff record "
        f"contributes a binary observation (substrate side: paired_diff > "
        f"0 → success; control side: paired_diff < 0 → success). The bulk "
        f"distribution failure mg-bef2 documented (root-projection bias "
        f"in greedy-fill v9 generation) is by-design tolerated here — the "
        f"right-tail comparison asks whether the *best* substrate "
        f"surfaces beat the *best* control surfaces, regardless of bulk "
        f"behavior.\n"
    )
    out.append("## Per-pool acceptance gate\n")
    out.append(
        f"| pool | n_substrate_top | n_control_top | "
        f"median(top-{top_k_gate} substrate posterior) | "
        f"median(top-{top_k_gate} control posterior) | "
        f"MW U (substrate) | MW p (one-tail) | gate |"
    )
    out.append("|:--|---:|---:|---:|---:|---:|---:|:--:|")
    for s in summaries:
        out.append(
            "| {pool} | {ns} | {nc} | {mss:.4f} | {msc:.4f} | {u:.1f} | {p:.4f} | {gate} |".format(
                pool=s["pool"],
                ns=s["n_substrate_top"],
                nc=s["n_control_top"],
                mss=s["median_substrate_top"],
                msc=s["median_control_top"],
                u=s["mw_u_substrate"],
                p=s["mw_p_one_tail"],
                gate=s["gate"],
            )
        )
    out.append("")

    for pool in _SUBSTRATE_POOLS:
        pool_rows = [r for r in rows if r["substrate_pool"] == pool]
        if not pool_rows:
            continue
        interleaved = sorted(pool_rows, key=lambda r: -r["effective_score"])[:top_per_pool]
        out.append(
            f"## {pool} — top {len(interleaved)} surfaces by effective score "
            f"(substrate + control interleaved)\n"
        )
        out.append(_SURFACE_TABLE_HEADER)
        out.append(_SURFACE_TABLE_SEP)
        for i, r in enumerate(interleaved, 1):
            out.append(_surface_table_row(i, r))
        out.append("")

    out.append("## Notes\n")
    out.append(
        f"- Prior: Beta(α=1, β=1) (uninformative). Posterior mean = "
        f"(1+k)/(2+n); 95% credible interval from the Beta inverse-CDF "
        f"(stdlib bisection on the regularized incomplete beta).\n"
        f"- Credibility cap n_min = {n_min}. Surfaces with n < n_min are "
        f"shrunk toward the prior mean 0.5 in the leaderboard ranking but "
        f"not excluded; the gate uses posterior_mean directly so small-n "
        f"outliers can still appear in the top-{top_k_gate} if their raw "
        f"posterior is high.\n"
        f"- v8 single-root substrate: surface = `pool_entry_surface`; v9 "
        f"multi-root substrate: surface = each unique entry in "
        f"`root_surfaces`. A signature like `lur+lur+ur` contributes one "
        f"observation under `lur` and one under `ur` per window. The "
        f"control side mirrors this on the matched control pool's "
        f"surfaces.\n"
        f"- Determinism: identical n + k + posterior + p-values across "
        f"re-runs given the same `experiments.{_METRIC}.jsonl`, "
        f"`hypotheses/auto/*`, `hypotheses/auto_signatures/*`, and "
        f"`pools/*`. No RNG anywhere in the pipeline.\n"
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
        "--pools",
        type=str,
        default=",".join(_SUBSTRATE_POOLS),
        help="Comma-separated substrate pools to roll up.",
    )
    parser.add_argument("--n-min", type=int, default=_DEFAULT_NMIN)
    parser.add_argument("--top-per-pool", type=int, default=_DEFAULT_TOP_PER_POOL)
    parser.add_argument("--top-k-gate", type=int, default=_DEFAULT_TOP_K_GATE)
    parser.add_argument(
        "--language-dispatch",
        type=str,
        default=None,
        help=(
            "JSON object mapping pool name → external phoneme LM name "
            "(used to filter rows in the result stream by language). "
            "Defaults to the same-LM dispatch (aquitanian→basque, "
            "etruscan→etruscan, toponym→basque, control_*→same as "
            "their substrate). Pass a swapped dispatch to compute the "
            "cross-LM negative-control posteriors (mg-0f97)."
        ),
    )
    parser.add_argument(
        "--out-suffix",
        type=str,
        default="",
        help=(
            "Optional filename suffix appended to the per-pool / combined "
            "output paths (e.g. '.aquitanian_under_etruscan_lm'). Empty "
            "string preserves the legacy filenames."
        ),
    )
    parser.add_argument(
        "--title-suffix",
        type=str,
        default="",
        help=(
            "Optional title suffix appended to the rendered Markdown "
            "headers. Default empty (legacy)."
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path for the per-pool gate summary JSON sidecar.",
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]

    if args.language_dispatch:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)
        language_dispatch.update(json.loads(args.language_dispatch))
    else:
        language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    score_rows = _load_score_rows(args.results_dir)
    pool_phonemes = _load_pool_phonemes(args.pools_dir)

    all_records: list[dict] = []
    for pool in pools:
        all_records.extend(
            build_v8_records(
                pool=pool,
                auto_dir=args.auto_dir,
                score_rows=score_rows,
                pool_phonemes=pool_phonemes,
                language_dispatch=language_dispatch,
            )
        )
        all_records.extend(
            build_v9_records(
                pool=pool,
                auto_dir=args.auto_sig_dir,
                score_rows=score_rows,
                language_dispatch=language_dispatch,
            )
        )

    aggregates = aggregate_per_surface(all_records)
    rows = build_posterior_rows(aggregates, n_min=args.n_min)

    summaries: list[dict] = []
    for pool in pools:
        text, summary = render_pool_md(
            pool=pool,
            rows=rows,
            top_per_pool=args.top_per_pool,
            top_k_gate=args.top_k_gate,
            n_min=args.n_min,
            title_suffix=args.title_suffix,
        )
        out_name = f"rollup.bayesian_posterior.{pool}{args.out_suffix}.md"
        out_path = args.results_dir / out_name
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path}", file=sys.stderr)
        summaries.append(summary)

    combined = render_combined_md(
        rows=rows,
        summaries=summaries,
        top_per_pool=args.top_per_pool,
        top_k_gate=args.top_k_gate,
        n_min=args.n_min,
        title_suffix=args.title_suffix,
    )
    combined_name = f"rollup.bayesian_posterior{args.out_suffix}.md"
    combined_path = args.results_dir / combined_name
    combined_path.write_text(combined, encoding="utf-8")
    print(f"wrote {combined_path}", file=sys.stderr)

    if args.summary_json:
        args.summary_json.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summaries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
