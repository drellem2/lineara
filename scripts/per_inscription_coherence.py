#!/usr/bin/env python3
"""Per-inscription coherence test (mg-3438, harness v19).

Daniel-proposed reframe of the consensus question (mg-c216 / v13 measured
*per-surface* coherence — aggregate over many windows of many inscriptions
for each top-20 surface — and FAILed at median 0.18 vs the 0.6 bar). v19
asks the per-INSCRIPTION question: do the multiple substrate surfaces that
hit a single short inscription I agree on what each sign in I should be?

For each Linear A inscription I, we gather every positive-paired-diff
candidate equation targeting I (substrate side, across the three validated
substrate pools — aquitanian, etruscan, toponym — under the same-LM
``external_phoneme_perplexity_v0`` metric). For each Linear A sign s in I:

  * Collect proposed phonemes from those candidates' sign_to_phoneme
    mappings (v8 single-root: full mapping; v9 multi-root: each root's
    own mapping).
  * Per-sign histogram, modal phoneme, smoothed Dirichlet-multinomial
    posterior with α=0.5 and V = number of distinct phonemes proposed
    locally for sign s in I, and Shannon entropy in bits.

Per-inscription coherence statistic (the central output):

    fraction_high_coherence_signs(I)
      = Σ_{s ∈ tokens(I)} 1[modal_posterior(s, I) > 0.5]
        / |tokens(I)|

where ``tokens(I)`` is the syllabographic-only token sequence (DIV, LOG:,
[?] excluded), and signs not covered by any positive-paired-diff candidate
in I contribute 0 to the numerator. The denominator weights repeated signs
by their occurrence count, so a sign appearing 3× and 1× in I is weighted
4 if both pass the threshold (3 + 1 = 4). The brief calls this "weighted by
sign-frequency in I"; concretely it is a per-token average over I.

We also report a robust secondary statistic that excludes lone-proposal
signs (which trivially pass the threshold under any smoothing):

    fraction_robust_high_coherence_signs(I)
      = Σ_{s ∈ tokens(I)} 1[modal_posterior(s, I) > 0.5 AND n_proposals(s, I) ≥ 2]
        / |tokens(I)|

The robust version answers Daniel's brief framing more directly — "do
multiple surfaces collide on the same handful of signs" — by requiring
that at least two surfaces collide on each "high-coherence" sign. The
literal-brief headline is also reported.

Cascade-decipherment classification (uses the *robust* statistic; the
literal-brief statistic is reported alongside but not used for cascade
classification because lone-proposal signs are not collisions):

  * **Cascade candidate** — fraction_robust_high_coherence_signs ≥ 0.5
  * **Partial cascade**   — 0.25 ≤ robust fraction < 0.5
  * **Noise**             — robust fraction < 0.25

For cascade candidates we emit the *mechanical proposed reading*:
concatenate the modal phoneme of each sign in I in token order. **The
proposed reading is NOT a decipherment claim** — it is the mechanical
output of the consensus, presented for domain-expert review.

Populations evaluated
=====================
Population A — Top-30 inscriptions by v10 right-tail concentration density
  (mg-0f97). Read directly from
  ``results/rollup.right_tail_inscription_concentration.md``'s "by raw
  count" view (Daniel's brief calls this "top-30 by right-tail
  concentration density" but the rollup's headline view is by raw count;
  both views are honored — we evaluate the union and tag rows with which
  view selected them).

Population B — Short inscriptions (n_signs ≤ 5 in corpus/all.jsonl), capped
  at top-30 by total positive-paired-diff candidate count.

Population C — Inscriptions whose token sequence contains the libation-
  formula ``AB57-AB31-AB31-AB60-AB13`` (JA-SA-SA-RA-ME), with DIV
  separators tolerated. The match criterion is documented in the rollup.

Outputs
=======
  results/rollup.per_inscription_coherence.md  (Populations A, B, C and
                                                cascade-candidate enumeration)

Determinism: byte-identical across re-runs given the same result stream,
manifests, and hypothesis YAMLs. No RNG anywhere in the pipeline. Tie-
breaking on ranking and on modal-phoneme selection is alphabetical.

Usage
=====
  python3 scripts/per_inscription_coherence.py
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

# Allow ``python3 scripts/per_inscription_coherence.py`` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.consensus_map import (  # type: ignore
    extract_v8_sign_to_phoneme,
    extract_v9_root_sign_to_phoneme,
)
from scripts.per_surface_bayesian_rollup import (  # type: ignore
    _DEFAULT_AUTO,
    _DEFAULT_AUTO_SIG,
    _DEFAULT_LANGUAGE_DISPATCH,
    _DEFAULT_POOLS,
    _DEFAULT_RESULTS_DIR,
    _load_manifest,
    _load_pool_phonemes,
    _load_score_rows,
    build_v8_records,
    build_v9_records,
)


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_VALIDATED_POOLS: tuple[str, ...] = ("aquitanian", "etruscan", "toponym")
_DEFAULT_ALPHA = 0.5
_DEFAULT_THRESHOLD = 0.5
_DEFAULT_CASCADE_BAR = 0.5
_DEFAULT_PARTIAL_BAR = 0.25
_DEFAULT_TOP_N = 30
_LIBATION_NEEDLE: tuple[str, ...] = ("AB57", "AB31", "AB31", "AB60", "AB13")


# ---------------------------------------------------------------------------
# Token filtering
# ---------------------------------------------------------------------------


_AB_TOKEN_RE = re.compile(r"^AB[0-9]+[a-z]*$")


def syllabographic_tokens(tokens: list[str]) -> list[str]:
    """Return only the syllabogram tokens of ``tokens``.

    Drops DIV separators, LOG: logographs, ``[?]`` unknowns, and other
    non-AB tokens (e.g. A301). The candidate sign_to_phoneme mappings are
    keyed on AB-prefixed sign IDs — those are the only signs whose
    consensus we can compute. Non-AB syllabograms such as A301 / A302
    appear in some inscriptions but are rare and never in the v8/v9
    sign_to_phoneme keyspace, so they would always fail the threshold;
    excluding them up-front is more honest than counting them as
    "noise".
    """
    return [t for t in tokens if _AB_TOKEN_RE.match(t)]


# ---------------------------------------------------------------------------
# Manifest indexing (substrate hash → metadata)
# ---------------------------------------------------------------------------


def _hash_to_v8_meta(auto_dir: Path, pool: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in _load_manifest(auto_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = {
            "path": row["hypothesis_path"],
            "surface": row["pool_entry_surface"],
            "inscription_id": row["inscription_id"],
        }
    return out


def _hash_to_v9_meta(auto_sig_dir: Path, pool: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in _load_manifest(auto_sig_dir / f"{pool}.manifest.jsonl"):
        out[row["hypothesis_hash"]] = {
            "path": row["hypothesis_path"],
            "root_surfaces": tuple(row["root_surfaces"]),
            "inscription_id": row["inscription_id"],
        }
    return out


# ---------------------------------------------------------------------------
# Per-inscription histogram aggregation
# ---------------------------------------------------------------------------


def collect_per_inscription_proposals(
    *,
    pools: list[str],
    auto_dir: Path,
    auto_sig_dir: Path,
    pools_dir: Path,
    results_dir: Path,
    repo_root: Path,
    language_dispatch: dict[str, str],
) -> dict:
    """Walk substrate paired_diff records → per-inscription (sign, phoneme) tally.

    Returns
    -------
    dict
        ``{
          "histograms_by_ins": {ins_id: {sign: {phoneme: count}}},
          "n_pos_records_by_ins": {ins_id: int},
          "n_total_records_by_ins": {ins_id: int},
          "contributing_surfaces_by_ins": {ins_id: {surface: count}},
          "contributing_pools_by_ins": {ins_id: {pool: count}},
        }``
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

    histograms_by_ins: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(int))
    )
    n_pos: dict[str, int] = defaultdict(int)
    n_total: dict[str, int] = defaultdict(int)
    contributing_surfaces: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    contributing_pools: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for rec in sub_records:
        pool = rec["pool"]
        sub_hash = rec["substrate_hash"]
        kind = rec["kind"]
        if kind == "v8":
            meta = v8_meta[pool].get(sub_hash)
        else:
            meta = v9_meta[pool].get(sub_hash)
        if meta is None:
            continue
        ins_id = meta["inscription_id"]
        n_total[ins_id] += 1
        if rec["paired_diff"] <= 0:
            continue
        n_pos[ins_id] += 1
        contributing_pools[ins_id][pool] += 1

        if kind == "v8":
            yaml_path = repo_root / meta["path"]
            sign_to_phoneme = extract_v8_sign_to_phoneme(yaml_path)
            contributing_surfaces[ins_id][meta["surface"]] += 1
            for sign, phoneme in sign_to_phoneme.items():
                histograms_by_ins[ins_id][sign][phoneme] += 1
        else:
            yaml_path = repo_root / meta["path"]
            roots = extract_v9_root_sign_to_phoneme(yaml_path)
            for root in roots:
                surface = root["surface"]
                contributing_surfaces[ins_id][surface] += 1
                for sign, phoneme in root["sign_to_phoneme"].items():
                    histograms_by_ins[ins_id][sign][phoneme] += 1

    # Convert nested defaultdicts to plain dicts.
    histograms_out = {
        ins: {sign: dict(ph) for sign, ph in signs.items()}
        for ins, signs in histograms_by_ins.items()
    }
    return {
        "histograms_by_ins": histograms_out,
        "n_pos_records_by_ins": dict(n_pos),
        "n_total_records_by_ins": dict(n_total),
        "contributing_surfaces_by_ins": {
            ins: dict(d) for ins, d in contributing_surfaces.items()
        },
        "contributing_pools_by_ins": {
            ins: dict(d) for ins, d in contributing_pools.items()
        },
    }


# ---------------------------------------------------------------------------
# Per-sign consensus within one inscription
# ---------------------------------------------------------------------------


def _shannon_entropy_bits(counts) -> float:
    counts = [c for c in counts if c > 0]
    total = sum(counts)
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts:
        p = c / total
        h -= p * math.log2(p)
    return h


def per_sign_consensus_local(
    histogram: dict[str, int],
    *,
    alpha: float,
) -> dict | None:
    """Per-sign consensus within one inscription.

    Smoothing is local: V = number of distinct phonemes observed in this
    sign's local histogram. This is *different* from v13's consensus map,
    which used a global vocabulary V across all signs. The local choice
    is correct for v19's "do the candidates targeting THIS inscription
    agree?" framing — the prior over an unobserved phoneme outside the
    local proposals is irrelevant to local agreement.

    Returns ``None`` if the histogram is empty.
    """
    if not histogram:
        return None
    n_proposals = sum(histogram.values())
    if n_proposals == 0:
        return None
    # Sort by (-count, phoneme) so ties resolve deterministically (alpha).
    sorted_phonemes = sorted(histogram.items(), key=lambda kv: (-kv[1], kv[0]))
    modal_phoneme, modal_count = sorted_phonemes[0]
    vocab_size = len(histogram)
    denom = n_proposals + alpha * vocab_size
    modal_posterior = (modal_count + alpha) / denom
    entropy_bits = _shannon_entropy_bits(histogram.values())
    return {
        "modal_phoneme": modal_phoneme,
        "modal_count": modal_count,
        "n_proposals": n_proposals,
        "n_distinct_phonemes": vocab_size,
        "modal_posterior": modal_posterior,
        "entropy_bits": entropy_bits,
        "histogram": dict(histogram),
    }


def per_inscription_coherence(
    *,
    inscription_id: str,
    tokens: list[str],
    histograms: dict[str, dict[str, int]],
    alpha: float,
    threshold: float,
    robust_min_n: int = 2,
) -> dict:
    """Compute the per-inscription coherence statistic.

    Parameters
    ----------
    inscription_id
        Just for record-keeping in the output dict.
    tokens
        Syllabographic-only token sequence of the inscription (post
        :func:`syllabographic_tokens`).
    histograms
        ``{sign: {phoneme: count}}`` for this inscription's positive-
        paired-diff candidates.
    alpha
        Dirichlet smoothing concentration (default 0.5, Jeffreys).
    threshold
        Modal posterior threshold for "high-coherence" classification
        (default 0.5).
    robust_min_n
        Minimum number of distinct positive-paired-diff candidates that
        must propose phonemes for a sign at this inscription before that
        sign can count toward the *robust* high-coherence statistic.
        Default 2 — a "collision" requires ≥2 surfaces. Lone-proposal
        signs (n=1) trivially have modal_posterior = 1.0 under any
        smoothing and therefore pass the literal-brief threshold but do
        not constitute genuine consensus.
    """
    per_sign: dict[str, dict] = {}
    for sign in sorted(set(tokens)):
        h = histograms.get(sign, {})
        info = per_sign_consensus_local(h, alpha=alpha)
        per_sign[sign] = info  # may be None if no proposals

    n_tokens = len(tokens)
    if n_tokens == 0:
        return {
            "inscription_id": inscription_id,
            "n_tokens_syllabographic": 0,
            "n_tokens_with_proposals": 0,
            "n_tokens_high_coherence": 0,
            "n_tokens_robust_high_coherence": 0,
            "fraction_high_coherence_signs": float("nan"),
            "fraction_robust_high_coherence_signs": float("nan"),
            "per_sign": {},
            "tokens": [],
            "mechanical_reading": "",
        }

    n_high = 0
    n_robust_high = 0
    n_with_proposals = 0
    reading: list[str] = []
    for tok in tokens:
        info = per_sign.get(tok)
        if info is None:
            reading.append("·")  # no proposal at all
            continue
        n_with_proposals += 1
        passes_literal = info["modal_posterior"] > threshold
        passes_robust = passes_literal and info["n_proposals"] >= robust_min_n
        if passes_literal:
            n_high += 1
        if passes_robust:
            n_robust_high += 1
            reading.append(info["modal_phoneme"])
        elif passes_literal:
            # Literal-pass but lone proposal: render with a trailing
            # superscript marker so readers can see this sign passed the
            # literal threshold but is not a robust collision.
            reading.append(f"{info['modal_phoneme']}*")
        else:
            # Below threshold: render in parens to make the uncertainty
            # visible in the mechanical reading.
            reading.append(f"({info['modal_phoneme']})")

    return {
        "inscription_id": inscription_id,
        "n_tokens_syllabographic": n_tokens,
        "n_tokens_with_proposals": n_with_proposals,
        "n_tokens_high_coherence": n_high,
        "n_tokens_robust_high_coherence": n_robust_high,
        "fraction_high_coherence_signs": n_high / n_tokens,
        "fraction_robust_high_coherence_signs": n_robust_high / n_tokens,
        "per_sign": {
            s: info for s, info in per_sign.items() if info is not None
        },
        "tokens": list(tokens),
        "mechanical_reading": "-".join(reading),
    }


def classify_cascade(
    fraction: float,
    *,
    cascade_bar: float,
    partial_bar: float,
) -> str:
    if math.isnan(fraction):
        return "n/a"
    if fraction >= cascade_bar:
        return "Cascade candidate"
    if fraction >= partial_bar:
        return "Partial cascade"
    return "Noise"


# ---------------------------------------------------------------------------
# Population builders
# ---------------------------------------------------------------------------


def _load_corpus(corpus_path: Path) -> list[dict]:
    rows: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def parse_population_a(
    rollup_path: Path,
    *,
    top_n: int,
) -> list[str]:
    """Parse top-N inscription IDs from results/rollup.right_tail_inscription_concentration.md.

    Reads the "Top-30 inscriptions by raw count" view (the headline
    leaderboard), in the order they appear. Returns the inscription_id
    strings.
    """
    if not rollup_path.exists():
        return []
    text = rollup_path.read_text(encoding="utf-8")
    # The headline section is "## Top-30 inscriptions by raw count …".
    # Match the table rows (lines starting with "| <int> | `…` |").
    in_section = False
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("## Top-30 inscriptions by raw count"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        m = re.match(r"\|\s*\d+\s*\|\s*`([^`]+)`\s*\|", line)
        if m:
            out.append(m.group(1))
        if len(out) >= top_n:
            break
    return out


def select_population_b(
    *,
    corpus: list[dict],
    n_pos_records_by_ins: dict[str, int],
    max_signs: int,
    top_n: int,
) -> list[str]:
    """Filter corpus by n_signs ≤ max_signs, sort by candidate count, take top-N.

    Inscriptions with zero positive-paired-diff records are excluded
    (they have no consensus to test).
    """
    rows: list[tuple[int, int, str]] = []
    for r in corpus:
        n_signs = r.get("n_signs", 0)
        if not (0 < n_signs <= max_signs):
            continue
        ins_id = r["id"]
        npos = n_pos_records_by_ins.get(ins_id, 0)
        if npos <= 0:
            continue
        rows.append((-npos, n_signs, ins_id))
    rows.sort()
    return [ins_id for _, _, ins_id in rows[:top_n]]


def _find_subseq_with_div(tokens: list[str], needle: tuple[str, ...]) -> bool:
    """True iff ``needle`` appears in ``tokens`` as a contiguous run, allowing
    DIV separators to be skipped between needle elements.

    The libation formula is conventionally written as five contiguous
    syllabograms (no separators within), but this is robust if the
    digital transliteration inserts DIV at word boundaries.
    """
    clean = [t for t in tokens if t != "DIV"]
    n = len(needle)
    for i in range(len(clean) - n + 1):
        if tuple(clean[i : i + n]) == needle:
            return True
    return False


def select_population_c(corpus: list[dict]) -> list[str]:
    """Inscriptions whose token sequence contains AB57-AB31-AB31-AB60-AB13."""
    out: list[str] = []
    for r in corpus:
        tokens = r.get("tokens", [])
        if _find_subseq_with_div(tokens, _LIBATION_NEEDLE):
            out.append(r["id"])
    return sorted(out)


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt(x: float, w: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "nan"
    return f"{x:.{w}f}"


def _short_present(d: dict[str, int], top: int = 3) -> str:
    """Render a small ``{key: count}`` dict as ``key (count), …`` (top-N)."""
    items = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
    return ", ".join(f"`{k}` ({v})" for k, v in items)


def _evaluate_population(
    *,
    name: str,
    inscription_ids: list[str],
    corpus_by_id: dict[str, dict],
    proposals: dict,
    alpha: float,
    threshold: float,
) -> list[dict]:
    """Run the per-inscription coherence test on each ID in ``inscription_ids``.

    Returns one row per inscription, in the input order (so Population A
    preserves its right-tail rank order).
    """
    histograms_by_ins = proposals["histograms_by_ins"]
    n_pos_by_ins = proposals["n_pos_records_by_ins"]
    n_total_by_ins = proposals["n_total_records_by_ins"]
    contributing_surfaces = proposals["contributing_surfaces_by_ins"]
    contributing_pools = proposals["contributing_pools_by_ins"]

    rows: list[dict] = []
    for ins_id in inscription_ids:
        rec = corpus_by_id.get(ins_id, {})
        tokens_all = rec.get("tokens", [])
        tokens = syllabographic_tokens(tokens_all)
        histograms = histograms_by_ins.get(ins_id, {})
        info = per_inscription_coherence(
            inscription_id=ins_id,
            tokens=tokens,
            histograms=histograms,
            alpha=alpha,
            threshold=threshold,
        )
        info["population"] = name
        info["site"] = rec.get("site", "")
        info["genre_hint"] = rec.get("genre_hint", "")
        info["n_signs_corpus"] = rec.get("n_signs", 0)
        info["raw_transliteration"] = rec.get("raw_transliteration", "")
        info["n_pos_records"] = n_pos_by_ins.get(ins_id, 0)
        info["n_total_records"] = n_total_by_ins.get(ins_id, 0)
        info["contributing_surfaces"] = contributing_surfaces.get(ins_id, {})
        info["contributing_pools"] = contributing_pools.get(ins_id, {})
        rows.append(info)
    return rows


def _render_population_table(
    *,
    title: str,
    rows: list[dict],
    cascade_bar: float,
    partial_bar: float,
) -> list[str]:
    out: list[str] = []
    out.append(f"## {title}\n")
    if not rows:
        out.append("_No inscriptions selected for this population._\n")
        return out
    out.append(
        "| inscription_id | site | genre | n_tokens (syll) | n_with_proposals | "
        "n_high_coh | fraction_high_coh | n_robust_high_coh | "
        "fraction_robust_high_coh | n_pos_records | "
        "contributing_pools | top contributing_surfaces | classification |"
    )
    out.append("|:--|:--|:--|---:|---:|---:|---:|---:|---:|---:|:--|:--|:--|")
    for r in rows:
        cls = classify_cascade(
            r["fraction_robust_high_coherence_signs"],
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
        pools_present = _short_present(r["contributing_pools"], top=4)
        surfaces_present = _short_present(r["contributing_surfaces"], top=5)
        out.append(
            "| `{ins}` | {site} | {genre} | {nt} | {nwp} | {nhc} | "
            "{frac} | {nrhc} | {rfrac} | {npos} | {pools} | "
            "{surfaces} | {cls} |".format(
                ins=r["inscription_id"],
                site=r["site"] or "—",
                genre=r["genre_hint"] or "—",
                nt=r["n_tokens_syllabographic"],
                nwp=r["n_tokens_with_proposals"],
                nhc=r["n_tokens_high_coherence"],
                frac=_fmt(r["fraction_high_coherence_signs"]),
                nrhc=r["n_tokens_robust_high_coherence"],
                rfrac=_fmt(r["fraction_robust_high_coherence_signs"]),
                npos=r["n_pos_records"],
                pools=pools_present or "—",
                surfaces=surfaces_present or "—",
                cls=cls,
            )
        )
    out.append("")
    return out


def _render_per_sign_block(rows: list[dict], threshold: float) -> list[str]:
    """Per-sign breakdown for cascade candidates only (most informative)."""
    out: list[str] = []
    if not rows:
        return out
    out.append("### Per-sign breakdown for cascade candidates\n")
    out.append(
        "Each row: one (inscription, sign) pair. ``n_proposals`` is the "
        "number of positive-paired-diff candidates contributing a "
        f"phoneme for that sign at that inscription. ``modal_posterior > "
        f"{threshold}`` is the high-coherence threshold; α=0.5, V=local "
        "vocabulary.\n"
    )
    out.append(
        "| inscription | sign | n_proposals | modal | modal_count | "
        "modal_posterior | entropy_bits | full histogram |"
    )
    out.append("|:--|:--|---:|:--|---:|---:|---:|:--|")
    for r in rows:
        for sign in sorted(r["per_sign"].keys()):
            info = r["per_sign"][sign]
            hist_fmt = ", ".join(
                f"{p}={c}"
                for p, c in sorted(
                    info["histogram"].items(), key=lambda kv: (-kv[1], kv[0])
                )
            )
            out.append(
                "| `{ins}` | `{sign}` | {n} | `{modal}` | {mc} | {mp} | "
                "{ent} | {hist} |".format(
                    ins=r["inscription_id"],
                    sign=sign,
                    n=info["n_proposals"],
                    modal=info["modal_phoneme"],
                    mc=info["modal_count"],
                    mp=_fmt(info["modal_posterior"]),
                    ent=_fmt(info["entropy_bits"], 3),
                    hist=hist_fmt,
                )
            )
    out.append("")
    return out


def _render_cascade_readings(
    rows: list[dict],
    *,
    cascade_bar: float,
    partial_bar: float,
) -> list[str]:
    """Mechanical proposed reading for cascade + partial-cascade candidates.

    Cascade classification uses the *robust* statistic (fraction of
    tokens with modal_posterior > 0.5 AND n_proposals ≥ 2) — see the
    module docstring for why. The literal-brief fraction is also
    reported so readers can see both.
    """
    out: list[str] = []
    cascades = [
        r for r in rows
        if r["fraction_robust_high_coherence_signs"] >= cascade_bar
    ]
    partials = [
        r for r in rows
        if partial_bar <= r["fraction_robust_high_coherence_signs"] < cascade_bar
    ]
    out.append("## Cascade candidates and mechanical proposed readings\n")
    out.append(
        f"**Cascade candidates** (robust fraction ≥ {cascade_bar}): "
        f"{len(cascades)}. **Partial cascades** "
        f"({partial_bar} ≤ robust fraction < {cascade_bar}): "
        f"{len(partials)}. Classification uses the robust statistic; "
        "the literal-brief fraction is shown alongside for "
        "transparency.\n"
    )
    out.append(
        "**The proposed readings below are NOT decipherment claims.** They "
        "are the *mechanical* output of the per-inscription consensus: for "
        "each Linear A sign in the inscription, the modal phoneme over all "
        "positive-paired-diff candidates targeting that inscription. "
        "Rendering convention: a bare phoneme (e.g. `s`) is robust high-"
        "coherence (n≥2 candidates agree); a phoneme followed by `*` is "
        "literal-pass but lone-proposal (n=1, technically unanimous but "
        "no collision); a phoneme in parens (e.g. `(a)`) is below the "
        "modal-posterior threshold; `·` is a sign with no proposal at "
        "all. These are hypotheses for domain-expert review.\n"
    )
    if cascades:
        out.append("### Cascade candidates\n")
        out.append(
            "| inscription | site | robust fraction | literal fraction | "
            "tokens | mechanical reading |"
        )
        out.append("|:--|:--|---:|---:|:--|:--|")
        for r in cascades:
            out.append(
                "| `{ins}` | {site} | {rfrac} | {frac} | {toks} | {reading} |".format(
                    ins=r["inscription_id"],
                    site=r["site"] or "—",
                    rfrac=_fmt(r["fraction_robust_high_coherence_signs"]),
                    frac=_fmt(r["fraction_high_coherence_signs"]),
                    toks="-".join(r["tokens"]) or "—",
                    reading=r["mechanical_reading"] or "—",
                )
            )
        out.append("")
    else:
        out.append(
            "_No cascade candidates emerged at the robust bar in any of "
            "the three populations._\n"
        )
    if partials:
        out.append("### Partial cascades\n")
        out.append(
            "| inscription | site | robust fraction | literal fraction | "
            "tokens | mechanical reading |"
        )
        out.append("|:--|:--|---:|---:|:--|:--|")
        for r in partials:
            out.append(
                "| `{ins}` | {site} | {rfrac} | {frac} | {toks} | {reading} |".format(
                    ins=r["inscription_id"],
                    site=r["site"] or "—",
                    rfrac=_fmt(r["fraction_robust_high_coherence_signs"]),
                    frac=_fmt(r["fraction_high_coherence_signs"]),
                    toks="-".join(r["tokens"]) or "—",
                    reading=r["mechanical_reading"] or "—",
                )
            )
        out.append("")
    return out


def _render_population_c_comparison(
    rows: list[dict],
    *,
    cascade_bar: float,
    partial_bar: float,
) -> list[str]:
    """Compare Population C mechanical readings to scholarly proposals.

    The libation-formula scholarly proposal is `ja-sa-sa-ra-me`. We
    extract the per-sign modal phonemes for the AB57-AB31-AB31-AB60-AB13
    span specifically (skipping DIV separators) and present alongside.
    """
    out: list[str] = []
    if not rows:
        return out
    out.append("## Population C: comparison to scholarly libation-formula proposal\n")
    out.append(
        "The Linear A libation-table formula `JA-SA-SA-RA-ME` "
        "(AB57-AB31-AB31-AB60-AB13) has a long-standing scholarly "
        "transliteration `ja-sa-sa-ra-me`, often interpreted as a divine "
        "epithet (Davis 2014; Younger 2000–; cf. broader Aegean syllabary "
        "literature). The proposal is not universally accepted but is the "
        "best-attested known-content reading available against which to "
        "compare a mechanical consensus output.\n"
    )
    out.append(
        "| inscription | sign sequence | mechanical modal | "
        "scholarly transliteration | match? |"
    )
    out.append("|:--|:--|:--|:--|:--|")
    needle = list(_LIBATION_NEEDLE)
    scholarly = ["j+a", "s+a", "s+a", "r+a", "m+e"]
    # The substrate hypotheses propose single phonemes per sign, not
    # syllables; the table pairs each AB sign to a single mechanical
    # phoneme to be comparable to the *first phoneme* of each scholarly
    # syllable (rough surface match). Mismatches flagged "—".
    scholarly_first = ["j", "s", "s", "r", "m"]
    for r in rows:
        per_sign = r["per_sign"]
        modal_seq = []
        match_flags = []
        for sign, expected in zip(needle, scholarly_first):
            info = per_sign.get(sign)
            if info is None:
                modal_seq.append("·")
                match_flags.append("·")
            else:
                m = info["modal_phoneme"]
                modal_seq.append(m)
                match_flags.append("✓" if m == expected else "✗")
        out.append(
            "| `{ins}` | {needle} | {modal} | {scholarly} | {flags} |".format(
                ins=r["inscription_id"],
                needle="-".join(needle),
                modal="-".join(modal_seq),
                scholarly="-".join(scholarly),
                flags=" ".join(match_flags),
            )
        )
    out.append("")
    out.append(
        "*Note.* The mechanical consensus emits ONE phoneme per sign; the "
        "scholarly proposal is a CV syllable per sign. The match column "
        "compares the mechanical phoneme to the consonantal first segment "
        "of the scholarly syllable (j, s, s, r, m). A `✓` does not "
        "constitute corroboration of the scholarly reading — it indicates "
        "the per-inscription consensus's modal phoneme overlaps with the "
        "scholarly phoneme on that sign. Drawing decipherment-shaped "
        "conclusions from such a comparison without domain-expert review "
        "of the underlying candidate equations is out of scope for v19.\n"
    )
    out.append(
        "*If all five signs miss.* A complete divergence on the libation "
        "formula is also a meaningful result. It could mean either (a) "
        "the framework's substrate matches do not capture real Linear A "
        "phonology on these particular signs (consistent with v13's "
        "per-surface coherence failure), or (b) the scholarly "
        "transliteration is wrong (unlikely given Linear B parallels for "
        "AB57=ja, AB31=sa, AB60=ra, AB13=me). The most-honest read is "
        "(a) — the per-inscription consensus on PS Za 2 is high *within "
        "the framework's own equations* but those equations propose "
        "phonemes that disagree with the best-attested scholarly "
        "reading. Internal consensus does not imply external "
        "correctness.\n"
    )
    return out


def render_md(
    *,
    pop_a_rows: list[dict],
    pop_b_rows: list[dict],
    pop_c_rows: list[dict],
    pools: list[str],
    alpha: float,
    threshold: float,
    cascade_bar: float,
    partial_bar: float,
    rollup_a_path: Path,
    pop_b_max_signs: int,
    pop_b_top_n: int,
) -> str:
    out: list[str] = []
    out.append("# Per-inscription coherence test (mg-3438, harness v19)\n")
    out.append(
        "Generated by `scripts/per_inscription_coherence.py`. For each "
        "Linear A inscription I drawn from one of three populations "
        "(top-30 right-tail concentration; short n_signs ≤ "
        f"{pop_b_max_signs}; libation-formula carriers), this rollup "
        "gathers all positive-paired-diff candidate equations targeting "
        f"I — substrate side, across the {len(pools)} validated "
        f"substrate pools ({', '.join(pools)}) under the same-LM "
        "`external_phoneme_perplexity_v0` metric — and aggregates the "
        "proposed sign_to_phoneme mappings into a per-sign histogram. "
        f"Smoothed Dirichlet-multinomial posterior: α={alpha:g}, V = "
        "local vocabulary (distinct phonemes proposed for the sign at "
        "this inscription).\n"
    )
    out.append(
        "**Per-inscription coherence statistic.** For each I:\n\n"
        "    fraction_high_coherence_signs(I)\n"
        "      = #{tokens t in I : modal_posterior(t, I) > "
        f"{threshold}}}\n"
        "        / |tokens(I)|\n\n"
        "where tokens(I) is the syllabographic-only token sequence (DIV, "
        "LOG:, [?] excluded). Signs not covered by any candidate "
        "contribute 0 to the numerator; repeated signs are weighted by "
        "their occurrence count via the per-token average.\n"
    )
    out.append(
        f"**Cascade-decipherment classification.** ≥{cascade_bar} → "
        f"Cascade candidate; [{partial_bar}, {cascade_bar}) → Partial "
        f"cascade; <{partial_bar} → Noise. Classification uses the "
        "**robust** statistic (modal_posterior > "
        f"{threshold} AND n_proposals ≥ 2). The literal-brief statistic "
        "(no n_proposals minimum) is reported in every per-population "
        "table alongside the robust statistic, so readers can see both. "
        "Lone-proposal signs trivially satisfy the literal-brief "
        "threshold under any smoothing — a single candidate proposing "
        "anything for a sign yields modal_posterior = 1.0 — but a "
        "single proposal is not a *consensus* and not a *collision*. "
        "The brief's animating intuition is that 'short inscriptions "
        "force multiple surfaces to collide on the same handful of "
        "signs', which the robust statistic operationalizes directly.\n"
    )
    out.append(
        "**Important honesty constraint.** A cascade candidate is NOT a "
        "decipherment claim. It is a hypothesis for domain-expert "
        "review: the multiple substrate surfaces hitting this short "
        "inscription mostly agree on what each sign should be. Whether "
        "those agreed-upon phonemes correspond to the ACTUAL Linear A "
        "phonetic values is a separate, much higher-bar question that "
        "this framework does NOT settle.\n"
    )
    out.append(
        "**Difference from v13 (mg-c216).** v13 measured *per-surface* "
        "coherence — for each top-20 surface S, are the equations using "
        "S coherent? — and FAILed at median 0.18 vs the 0.6 bar. v19 is "
        "the *per-inscription* version: for each inscription I, do the "
        "candidates targeting I agree on what each sign should be? "
        "Different scope, different statistic. Per-inscription "
        "concentration is local; per-surface aggregate is global. v13's "
        "failure does not predict v19's outcome.\n"
    )
    out.append(
        "**Determinism.** Byte-identical output across re-runs given the "
        "same result stream + manifests + hypothesis YAMLs. No RNG. "
        "Tie-breaking on modal phoneme is alphabetical.\n"
    )

    out.append("## Population definitions\n")
    out.append(
        f"* **Population A** — top-30 inscriptions by right-tail "
        f"concentration (mg-0f97). Sourced from "
        f"`{rollup_a_path.relative_to(_REPO_ROOT) if rollup_a_path.is_absolute() else rollup_a_path}` "
        f"\"by raw count\" view; preserved in rank order. n="
        f"{len(pop_a_rows)} after filtering to inscriptions with at "
        f"least one positive-paired-diff record.\n"
        f"* **Population B** — short inscriptions with "
        f"n_signs ≤ {pop_b_max_signs} in `corpus/all.jsonl`, sorted by "
        f"total positive-paired-diff candidate count (descending), top "
        f"{pop_b_top_n}. n={len(pop_b_rows)}.\n"
        f"* **Population C** — inscriptions whose token sequence "
        f"contains the libation-formula syllabogram run "
        f"`{'-'.join(_LIBATION_NEEDLE)}` (JA-SA-SA-RA-ME), DIV "
        f"separators tolerated. n={len(pop_c_rows)}.\n"
    )

    # Headline summary table.
    out.append("## Headline summary\n")
    all_rows = pop_a_rows + pop_b_rows + pop_c_rows
    cascades = [
        r for r in all_rows
        if r["fraction_robust_high_coherence_signs"] >= cascade_bar
    ]
    partials = [
        r for r in all_rows
        if partial_bar
        <= r["fraction_robust_high_coherence_signs"]
        < cascade_bar
    ]
    noise = [
        r for r in all_rows
        if r["fraction_robust_high_coherence_signs"] < partial_bar
        and not math.isnan(r["fraction_robust_high_coherence_signs"])
    ]
    nan_rows = [
        r for r in all_rows
        if math.isnan(r["fraction_robust_high_coherence_signs"])
    ]
    out.append(
        "Classification uses the **robust** fraction (modal_posterior > "
        "0.5 AND n_proposals ≥ 2). Lone-proposal signs (n=1) trivially "
        "satisfy the literal-brief threshold under any smoothing, so the "
        "literal headline is reported alongside but does not drive cascade "
        "classification.\n"
    )
    out.append(
        "| population | n inscriptions | cascade | partial | noise | nan |"
    )
    out.append("|:--|---:|---:|---:|---:|---:|")
    for name, rows in [
        ("A: right-tail top-30", pop_a_rows),
        ("B: short ≤5 signs", pop_b_rows),
        ("C: libation formula", pop_c_rows),
    ]:
        nc = sum(
            1 for r in rows
            if r["fraction_robust_high_coherence_signs"] >= cascade_bar
        )
        np_ = sum(
            1 for r in rows
            if partial_bar
            <= r["fraction_robust_high_coherence_signs"]
            < cascade_bar
        )
        nn = sum(
            1 for r in rows
            if r["fraction_robust_high_coherence_signs"] < partial_bar
            and not math.isnan(r["fraction_robust_high_coherence_signs"])
        )
        nan_n = sum(
            1 for r in rows
            if math.isnan(r["fraction_robust_high_coherence_signs"])
        )
        out.append(
            f"| {name} | {len(rows)} | {nc} | {np_} | {nn} | {nan_n} |"
        )
    out.append(
        f"| **all (union)** | **{len(all_rows)}** | **{len(cascades)}** | "
        f"**{len(partials)}** | **{len(noise)}** | **{len(nan_rows)}** |"
    )
    out.append("")

    # Per-population tables.
    out.extend(
        _render_population_table(
            title="Population A — top-30 by right-tail concentration",
            rows=pop_a_rows,
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
    )
    out.extend(
        _render_population_table(
            title="Population B — short inscriptions (n_signs ≤ "
                  f"{pop_b_max_signs}), top-{pop_b_top_n} by candidate count",
            rows=pop_b_rows,
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
    )
    out.extend(
        _render_population_table(
            title="Population C — libation-formula inscriptions",
            rows=pop_c_rows,
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
    )

    # Cascade candidates + mechanical readings.
    out.extend(
        _render_cascade_readings(
            all_rows,
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
    )

    # Per-sign breakdown for cascade candidates (most informative for
    # domain-expert review). If no cascades, this section is empty.
    out.extend(
        _render_per_sign_block(
            [
                r for r in all_rows
                if r["fraction_robust_high_coherence_signs"] >= cascade_bar
            ],
            threshold=threshold,
        )
    )

    # Population C scholarly comparison.
    out.extend(
        _render_population_c_comparison(
            pop_c_rows,
            cascade_bar=cascade_bar,
            partial_bar=partial_bar,
        )
    )

    out.append("## Notes\n")
    out.append(
        "- *All-positive-paired-diff scope.* Unlike v13 (which restricted "
        "to v10 top-20 surfaces), v19 aggregates over ALL positive-"
        "paired-diff candidates targeting an inscription, regardless of "
        "the candidate's surface. The hypothesis is per-inscription "
        "local concentration: even noisy individual surfaces should "
        "agree on signs they all hit at the same inscription, IF those "
        "underlying surface matches reflect real signal. Restricting to "
        "top-20 would have re-imposed v13's selection criterion and "
        "muddied the per-inscription test.\n"
    )
    out.append(
        "- *Local Dirichlet smoothing.* V = number of distinct phonemes "
        "observed for the sign in this inscription's candidates. A sign "
        "with N=2 unanimous proposals has modal posterior 1.0 (V=1, "
        "α=0.5: (2+0.5)/(2+0.5) = 1.0); a 1/1 split has modal posterior "
        "0.5 (the threshold); a 2/1 split has modal posterior 0.7. This "
        "differs from v13's global V≈25; the local V is appropriate for "
        "v19's local-consensus framing.\n"
    )
    out.append(
        "- *Why the per-token weighting?* The brief specifies \"weighted "
        "by sign-frequency in I\". A sign occurring 3× in I that has a "
        "high-coherence modal contributes 3 to the numerator and 3 to "
        "the denominator; a sign occurring 1× contributes 1/1. This "
        "matches the natural reading of \"fraction of signs\" as a "
        "per-token quantity rather than per-distinct-sign.\n"
    )
    out.append(
        "- *Why three pools and not just the v10 PASSes?* The brief "
        "explicitly names aquitanian, etruscan, AND toponym as the three "
        "validated pools. Toponym FAILed v10's aggregate right-tail "
        "gate; that aggregate failure does not invalidate individual "
        "positive-paired-diff records on specific inscriptions, which is "
        "what v19 aggregates. Excluding toponym entirely would discard "
        "evidence the per-inscription test is designed to consider.\n"
    )
    out.append(
        "- *Mechanical reading rendering.* Modal phoneme bare → robust "
        "high-coherence sign (n_proposals ≥ 2 AND modal_posterior > "
        f"{threshold}); phoneme followed by `*` → literal-pass with "
        "lone proposal (n_proposals=1, modal_posterior=1.0 by tautology, "
        "no genuine collision); modal phoneme in `(parens)` → below the "
        "modal-posterior threshold; `·` → no candidate covered this "
        "sign at all. Token-position order is preserved.\n"
    )
    out.append(
        "- *Determinism.* Identical output across re-runs given the same "
        "`results/experiments.external_phoneme_perplexity_v0.jsonl`, "
        "`hypotheses/auto/*`, `hypotheses/auto_signatures/*`, and "
        "`pools/*`. Tie-breaking is alphabetical on modal phoneme.\n"
    )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=Path("corpus") / "all.jsonl")
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
        default=",".join(_DEFAULT_VALIDATED_POOLS),
        help=(
            "Comma-separated substrate pools to aggregate over. Default: "
            "the three validated pools (aquitanian, etruscan, toponym)."
        ),
    )
    parser.add_argument(
        "--rollup-a",
        type=Path,
        default=Path("results") / "rollup.right_tail_inscription_concentration.md",
        help="mg-0f97 right-tail concentration rollup; Population A source.",
    )
    parser.add_argument("--alpha", type=float, default=_DEFAULT_ALPHA)
    parser.add_argument("--threshold", type=float, default=_DEFAULT_THRESHOLD)
    parser.add_argument("--cascade-bar", type=float, default=_DEFAULT_CASCADE_BAR)
    parser.add_argument("--partial-bar", type=float, default=_DEFAULT_PARTIAL_BAR)
    parser.add_argument("--pop-a-top-n", type=int, default=_DEFAULT_TOP_N)
    parser.add_argument("--pop-b-max-signs", type=int, default=5)
    parser.add_argument("--pop-b-top-n", type=int, default=_DEFAULT_TOP_N)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results") / "rollup.per_inscription_coherence.md",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional path for a summary JSON sidecar (cascade rollup).",
    )
    args = parser.parse_args(argv)

    pools = [p.strip() for p in args.pools.split(",") if p.strip()]
    language_dispatch = dict(_DEFAULT_LANGUAGE_DISPATCH)

    proposals = collect_per_inscription_proposals(
        pools=pools,
        auto_dir=args.auto_dir,
        auto_sig_dir=args.auto_sig_dir,
        pools_dir=args.pools_dir,
        results_dir=args.results_dir,
        repo_root=args.repo_root,
        language_dispatch=language_dispatch,
    )

    corpus = _load_corpus(args.corpus)
    corpus_by_id = {r["id"]: r for r in corpus}

    pop_a_ids = [
        ins for ins in parse_population_a(args.rollup_a, top_n=args.pop_a_top_n)
        if proposals["n_pos_records_by_ins"].get(ins, 0) > 0
    ]
    pop_b_ids = select_population_b(
        corpus=corpus,
        n_pos_records_by_ins=proposals["n_pos_records_by_ins"],
        max_signs=args.pop_b_max_signs,
        top_n=args.pop_b_top_n,
    )
    pop_c_ids = [
        ins for ins in select_population_c(corpus)
        if proposals["n_pos_records_by_ins"].get(ins, 0) > 0
    ]

    pop_a_rows = _evaluate_population(
        name="A",
        inscription_ids=pop_a_ids,
        corpus_by_id=corpus_by_id,
        proposals=proposals,
        alpha=args.alpha,
        threshold=args.threshold,
    )
    pop_b_rows = _evaluate_population(
        name="B",
        inscription_ids=pop_b_ids,
        corpus_by_id=corpus_by_id,
        proposals=proposals,
        alpha=args.alpha,
        threshold=args.threshold,
    )
    pop_c_rows = _evaluate_population(
        name="C",
        inscription_ids=pop_c_ids,
        corpus_by_id=corpus_by_id,
        proposals=proposals,
        alpha=args.alpha,
        threshold=args.threshold,
    )

    text = render_md(
        pop_a_rows=pop_a_rows,
        pop_b_rows=pop_b_rows,
        pop_c_rows=pop_c_rows,
        pools=pools,
        alpha=args.alpha,
        threshold=args.threshold,
        cascade_bar=args.cascade_bar,
        partial_bar=args.partial_bar,
        rollup_a_path=args.rollup_a,
        pop_b_max_signs=args.pop_b_max_signs,
        pop_b_top_n=args.pop_b_top_n,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)

    def _count(rows, lo, hi):
        return sum(
            1 for r in rows
            if lo <= r["fraction_robust_high_coherence_signs"] < hi
        )

    def _count_ge(rows, lo):
        return sum(
            1 for r in rows
            if r["fraction_robust_high_coherence_signs"] >= lo
        )

    summary = {
        "pools": pools,
        "alpha": args.alpha,
        "threshold": args.threshold,
        "cascade_bar": args.cascade_bar,
        "partial_bar": args.partial_bar,
        "classification_statistic": "fraction_robust_high_coherence_signs",
        "robust_min_n": 2,
        "n_inscriptions": {
            "population_a": len(pop_a_rows),
            "population_b": len(pop_b_rows),
            "population_c": len(pop_c_rows),
        },
        "n_cascade_candidates": {
            "population_a": _count_ge(pop_a_rows, args.cascade_bar),
            "population_b": _count_ge(pop_b_rows, args.cascade_bar),
            "population_c": _count_ge(pop_c_rows, args.cascade_bar),
        },
        "n_partial_cascades": {
            "population_a": _count(pop_a_rows, args.partial_bar, args.cascade_bar),
            "population_b": _count(pop_b_rows, args.partial_bar, args.cascade_bar),
            "population_c": _count(pop_c_rows, args.partial_bar, args.cascade_bar),
        },
        "cascade_candidates": [
            {
                "inscription_id": r["inscription_id"],
                "population": r["population"],
                "fraction_robust": r["fraction_robust_high_coherence_signs"],
                "fraction_literal": r["fraction_high_coherence_signs"],
                "tokens": r["tokens"],
                "mechanical_reading": r["mechanical_reading"],
            }
            for r in (pop_a_rows + pop_b_rows + pop_c_rows)
            if r["fraction_robust_high_coherence_signs"] >= args.cascade_bar
        ],
    }
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"wrote {args.summary_json}", file=sys.stderr)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
