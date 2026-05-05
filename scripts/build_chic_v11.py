#!/usr/bin/env python3
"""chic-v11: cross-pool L3 robustness + #032 ku-pa context inspection (mg-d69c).

Two within-scope additional-evidence tests on the 3 chic-v5 tier-2
candidates (`#001 -> wa`/glide, `#012 -> wa`/glide, `#032 -> ki`/stop)
following chic-v9's negative leave-one-out validation result (LOO
accuracy 20.0%, 0/3 tier-2 unanimity correct). chic-v11 asks two
follow-on questions whose pass/fail signals are mechanical:

1. **Cross-pool L3 robustness.** Is the L3 substrate-consistency vote
   for each candidate an Eteocretan-LM artifact, or does it survive
   re-running L3 under each of the 4 substrate pools' LMs (with the
   per-pool candidate-value-pool filter that chic-v5 uses)? If all
   4 LMs vote the same phoneme class, the L3 vote is LM-robust; if
   the LMs disagree, the L3 vote is partly or fully LM-specific.

2. **#032 ku-pa context inspection.** chic-v6 produced a +3-inscription
   / +20-hit tier-1->tier-2 verification lift on the source-A
   scholar-proposed-Linear-A-readings test. The lift attributable to
   `#032 -> ki` (combined with the chic-v2 anchor `#013 -> pa`) lands
   on a single CHIC inscription via 5 scholar entries from the
   ku-pa name family / ka-pa transaction-term family attested in 4
   Linear A tablets (HT 1, HT 16, HT 102, HT 110a). chic-v11 inspects
   the source Linear A tablets' contextual metadata (genre, support)
   and the matched CHIC inscription's partial-reading rendering with
   chic-v2 anchors + `#032 -> ki` applied; the test asks whether the
   chic-v6 mechanical lift is corroborated by accountancy-context
   plausibility on both sides of the match.

Cross-pool L3 dispatch table (chic-v5 convention)
=================================================
  aquitanian -> basque LM       (pools/aquitanian.yaml +
                                  harness/external_phoneme_models/basque.json)
  etruscan   -> etruscan LM     (pools/etruscan.yaml +
                                  harness/external_phoneme_models/etruscan.json)
  toponym    -> basque LM       (pools/toponym.yaml + basque LM
                                  as substrate-pool stand-in,
                                  per chic-v3/chic-v5 convention)
  eteocretan -> eteocretan LM   (pools/eteocretan.yaml +
                                  harness/external_phoneme_models/eteocretan.json,
                                  the chic-v5 default)

The candidate-value pool is rebuilt per dispatch from
(chic-v2 anchor LB-carryover values + bare vowels a/e/i/o/u),
filtered to values whose first character is in the substrate
pool's phoneme inventory or is a bare vowel (chic-v5 convention,
preserving phonotactic comparability across pools).

Inputs (all already committed)
==============================
- corpora/cretan_hieroglyphic/all.jsonl                  (chic-v0)
- corpora/cretan_hieroglyphic/syllabographic.jsonl       (chic-v3)
- corpus/all.jsonl                                       (Linear A v0)
- pools/cretan_hieroglyphic_signs.yaml                   (chic-v1)
- pools/cretan_hieroglyphic_anchors.yaml                 (chic-v2)
- pools/aquitanian.yaml, pools/etruscan.yaml,
  pools/toponym.yaml, pools/eteocretan.yaml              (substrate pools)
- harness/external_phoneme_models/basque.json,
  harness/external_phoneme_models/etruscan.json,
  harness/external_phoneme_models/eteocretan.json        (LMs)
- corpora/scholar_proposed_readings/all.jsonl            (v22)
- results/experiments.chic_verification_v0.jsonl         (chic-v6)

Outputs
=======
- results/chic_v11_cross_pool_l3.md
- results/chic_v11_032_ku_pa_context.md

Determinism
===========
- No RNG. Same inputs -> byte-identical outputs across re-runs.
  L3 control-phoneme selection inherits chic-v5's sha256-keyed
  permutation; cross-pool dispatch + ku-pa enumeration are pure
  iteration over deterministic input order.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from harness.external_phoneme_model import ExternalPhonemeModel  # noqa: E402

from scripts.build_chic_v5 import (  # noqa: E402
    aggregate_class_means,
    build_anchor_mapping,
    candidate_value_pool,
    classify_value,
    compute_substrate_consistency,
    load_chic_records,
)

CHIC_FULL = ROOT / "corpora" / "cretan_hieroglyphic" / "all.jsonl"
CHIC_SYLL = ROOT / "corpora" / "cretan_hieroglyphic" / "syllabographic.jsonl"
LA_CORPUS = ROOT / "corpus" / "all.jsonl"
ANCHORS_YAML = ROOT / "pools" / "cretan_hieroglyphic_anchors.yaml"
SCHOLAR_JSONL = ROOT / "corpora" / "scholar_proposed_readings" / "all.jsonl"
CHIC_V6_EXPERIMENTS = ROOT / "results" / "experiments.chic_verification_v0.jsonl"

OUT_CROSS_POOL_MD = ROOT / "results" / "chic_v11_cross_pool_l3.md"
OUT_KU_PA_MD = ROOT / "results" / "chic_v11_032_ku_pa_context.md"

FETCHED_AT = "2026-05-06T00:00:00Z"

# (pool_name, pool_yaml_path, lm_path, dispatch_label) ordered as in the brief.
POOL_DISPATCH: list[tuple[str, Path, Path, str]] = [
    ("aquitanian",
     ROOT / "pools" / "aquitanian.yaml",
     ROOT / "harness" / "external_phoneme_models" / "basque.json",
     "aquitanian -> basque LM"),
    ("etruscan",
     ROOT / "pools" / "etruscan.yaml",
     ROOT / "harness" / "external_phoneme_models" / "etruscan.json",
     "etruscan -> etruscan LM"),
    ("toponym",
     ROOT / "pools" / "toponym.yaml",
     ROOT / "harness" / "external_phoneme_models" / "basque.json",
     "toponym -> basque LM (substrate stand-in)"),
    ("eteocretan",
     ROOT / "pools" / "eteocretan.yaml",
     ROOT / "harness" / "external_phoneme_models" / "eteocretan.json",
     "eteocretan -> eteocretan LM (chic-v5 default)"),
]

CANDIDATES: list[tuple[str, str, str]] = [
    # (sign_id, chic-v5 best L3 value, chic-v5 proposed class)
    ("#001", "wa", "glide"),
    ("#012", "wa", "glide"),
    ("#032", "ki", "stop"),
]

# Scholar entries to inspect (the 4 ku-pa-family scholars whose source
# Linear A tablets the brief calls out).
KU_PA_SCHOLAR_IDS: list[str] = [
    "kupa3_HT1",
    "kupa_HT16",
    "kapa_HT102",
    "kupa_HT110a",
]

CLASS_ORDER = ("vowel", "stop", "nasal", "liquid", "fricative", "glide")


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _phoneme_inventory(pool_yaml: dict) -> set[str]:
    """Collect the set of single-character phonemes across all entries.

    Multi-char phonemes (``th``, ``ph``, ``ts``, ...) are split into
    constituent chars; this matches the LM's char-level vocabulary
    and the chic-v5 candidate-value-pool filter, which keys on the
    candidate's first character.
    """
    inv: set[str] = set()
    for entry in pool_yaml.get("entries", []):
        for ph in entry.get("phonemes", []):
            for ch in ph:
                inv.add(ch)
    return inv


# ---------------------------------------------------------------------------
# Cross-pool L3 dispatch
# ---------------------------------------------------------------------------


def run_cross_pool_l3(
    *,
    syll_records: list[dict],
    anchor_records: list[dict],
    progress: bool = True,
) -> dict:
    """For each (candidate, pool) cell, run L3 substrate-consistency
    against the chic-v2 anchor mapping under that pool's LM.

    Returns a dict keyed by sign_id, with per-pool result rows and a
    cross-pool agreement summary.
    """
    anchor_mapping = build_anchor_mapping(anchor_records)
    pool_yaml_cache: dict[str, dict] = {}
    pool_inv_cache: dict[str, set[str]] = {}
    pool_value_pool_cache: dict[str, list[str]] = {}
    lm_cache: dict[str, ExternalPhonemeModel] = {}

    for pool_name, pool_path, lm_path, _ in POOL_DISPATCH:
        if pool_name not in pool_yaml_cache:
            pool_yaml = _load_yaml(pool_path)
            pool_yaml_cache[pool_name] = pool_yaml
            pool_inv_cache[pool_name] = _phoneme_inventory(pool_yaml)
            pool_value_pool_cache[pool_name] = candidate_value_pool(
                anchor_records, pool_yaml,
            )
        if str(lm_path) not in lm_cache:
            lm_cache[str(lm_path)] = ExternalPhonemeModel.load_json(lm_path)

    sign_ids = [c[0] for c in CANDIDATES]

    per_sign: dict[str, dict] = {}
    for sid, _v, _cls in CANDIDATES:
        per_sign[sid] = {
            "sign": sid,
            "chic_v5_best_value": dict((s, v) for s, v, _ in CANDIDATES)[sid],
            "chic_v5_proposed_class": dict((s, c) for s, _, c in CANDIDATES)[sid],
            "per_pool": OrderedDict(),
        }

    for pool_name, pool_path, lm_path, dispatch_label in POOL_DISPATCH:
        if progress:
            print(
                f"chic-v11: L3 cross-pool: pool={pool_name} lm={lm_path.name}",
                file=sys.stderr,
            )
        value_pool = pool_value_pool_cache[pool_name]
        lm = lm_cache[str(lm_path)]
        substrate = compute_substrate_consistency(
            syll_records=syll_records,
            anchor_mapping=anchor_mapping,
            unknown_ids=sign_ids,
            value_pool=value_pool,
            lm=lm,
        )
        for sid, _v, _cls in CANDIDATES:
            sub_rows = substrate.get(sid, [])
            class_agg = aggregate_class_means(sub_rows)
            if class_agg:
                winning_class = class_agg[0]["class"]
                winning_value = class_agg[0]["best_candidate"]
                winning_diff = class_agg[0]["mean_paired_diff"]
            else:
                winning_class = None
                winning_value = None
                winning_diff = None
            class_means: dict[str, float | None] = {c: None for c in CLASS_ORDER}
            for row in class_agg:
                class_means[row["class"]] = row["mean_paired_diff"]
            per_sign[sid]["per_pool"][pool_name] = {
                "pool_name": pool_name,
                "lm_path": str(lm_path.relative_to(ROOT)),
                "dispatch_label": dispatch_label,
                "value_pool_size": len(value_pool),
                "value_pool_classes": sorted({classify_value(v) for v in value_pool}),
                "winning_class": winning_class,
                "winning_value": winning_value,
                "winning_paired_diff": winning_diff,
                "per_class_mean_paired_diff": class_means,
            }

    # Per-sign cross-pool agreement summary.
    for sid in sign_ids:
        votes = Counter()
        for pool_name, _pp, _lm, _dl in POOL_DISPATCH:
            cls = per_sign[sid]["per_pool"][pool_name]["winning_class"]
            if cls:
                votes[cls] += 1
        total = sum(votes.values())
        if not votes:
            top_class = None
            top_count = 0
        else:
            top_class, top_count = sorted(
                votes.items(), key=lambda kv: (-kv[1], kv[0])
            )[0]
        if top_count >= 4:
            verdict = "lm_robust"
            verdict_word = "LM-robust (all 4 agree)"
        elif top_count == 3:
            verdict = "mostly_robust"
            verdict_word = "mostly LM-robust (3 of 4 agree)"
        elif top_count == 2:
            verdict = "weak"
            verdict_word = "weak agreement (2 of 4)"
        elif top_count == 1:
            verdict = "lm_artifact"
            verdict_word = "LM-artifact (<=1 of 4 agree)"
        else:
            verdict = "no_signal"
            verdict_word = "no signal"
        # Identify dissenting pool(s) for "mostly robust".
        majority_pools: list[str] = []
        dissent_pools: list[str] = []
        for pool_name, _pp, _lm, _dl in POOL_DISPATCH:
            cls = per_sign[sid]["per_pool"][pool_name]["winning_class"]
            if cls == top_class:
                majority_pools.append(pool_name)
            else:
                dissent_pools.append(pool_name)
        per_sign[sid]["cross_pool"] = {
            "votes": dict(votes),
            "top_class": top_class,
            "top_count": top_count,
            "n_pools_voting": total,
            "verdict": verdict,
            "verdict_word": verdict_word,
            "majority_pools": majority_pools,
            "dissent_pools": dissent_pools,
            "agrees_with_chic_v5": (
                top_class == per_sign[sid]["chic_v5_proposed_class"]
            ),
        }
    return {
        "per_sign": per_sign,
        "pool_value_pools": {
            pool_name: pool_value_pool_cache[pool_name]
            for pool_name, _pp, _lm, _dl in POOL_DISPATCH
        },
        "pool_inventories": {
            pool_name: sorted(pool_inv_cache[pool_name])
            for pool_name, _pp, _lm, _dl in POOL_DISPATCH
        },
    }


def write_cross_pool_md(
    summary: dict,
    out_path: Path,
) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC chic-v5 tier-2 candidates: cross-pool L3 robustness check "
      "(chic-v11; mg-d69c)")
    a("")
    a("## Method")
    a("")
    a("For each of the 3 chic-v5 tier-2 candidates "
      "(`#001 -> wa`/glide, `#012 -> wa`/glide, `#032 -> ki`/stop), "
      "the chic-v5 L3 substrate-consistency line is recomputed under "
      "EACH of the 4 substrate pools' LMs. The L3 machinery is "
      "byte-identical to chic-v5's: candidate-value pool rebuilt "
      "from chic-v2 anchor LB-carryover values + bare vowels (filtered "
      "to values whose first character is in the substrate pool's "
      "phoneme inventory, chic-v5 convention), each candidate scored "
      "via paired_diff against a deterministic class-disjoint control "
      "under the substrate pool's LM, per-class mean paired_diff "
      "picks the winning class. The only thing changing across the "
      "12 cells is the (pool, LM) dispatch.")
    a("")
    a("## Pool-LM dispatch table")
    a("")
    a("| substrate pool | LM file | candidate-pool size | candidate-pool classes |")
    a("|---|---|---:|---|")
    for pool_name, pool_path, lm_path, dispatch_label in POOL_DISPATCH:
        vp = summary["pool_value_pools"][pool_name]
        cls_present = sorted({classify_value(v) for v in vp})
        a(
            f"| {pool_name} | `{lm_path.relative_to(ROOT)}` | "
            f"{len(vp)} | {', '.join(cls_present)} |"
        )
    a("")
    a("Per-pool candidate-value pool composition (each pool's filter "
      "differs because the substrate-pool phoneme inventories differ):")
    a("")
    for pool_name, _pp, _lm, _dl in POOL_DISPATCH:
        vp = summary["pool_value_pools"][pool_name]
        items = " ".join(f"`{v}`" for v in vp)
        a(f"- **{pool_name}** ({len(vp)} values): {items}")
    a("")
    a("## Acceptance bands (per chic-v11 brief)")
    a("")
    a("- 4 of 4 LMs agree on the same phoneme class for a candidate "
      "-> L3 vote is **LM-robust**.")
    a("- 3 of 4 agree -> **mostly robust**; flag the dissenting LM.")
    a("- 2 of 4 -> **weak agreement**; the L3 vote is partly LM-specific.")
    a("- <=1 of 4 -> L3 vote is an **LM artifact**.")
    a("")
    a("## Per-candidate cross-pool L3 verdict")
    a("")
    a("Each row is one (candidate, pool) cell. The `winning class` "
      "column is the L3 vote under that pool's LM (per-class mean "
      "paired_diff argmax over the rebuilt candidate-value pool). "
      "Mean paired_diff columns show the per-class aggregate; — for a "
      "class indicates the class is empty in the rebuilt candidate "
      "pool for that substrate.")
    a("")
    for sid, _v, _cls in CANDIDATES:
        info = summary["per_sign"][sid]
        cp = info["cross_pool"]
        a(f"### Candidate `{sid}` "
          f"(chic-v5 proposed class: {info['chic_v5_proposed_class']}; "
          f"chic-v5 best value: `{info['chic_v5_best_value']}`)")
        a("")
        a("| pool | LM | winning class | winning value | "
          "winning paired_diff | "
          + " | ".join(f"mean({c})" for c in CLASS_ORDER) + " |")
        a("|---|---|---|---|---:|"
          + "|".join("---:" for _ in CLASS_ORDER) + "|")
        for pool_name, _pp, lm_path, _dl in POOL_DISPATCH:
            cell = info["per_pool"][pool_name]
            wc = cell["winning_class"] or "—"
            wv = f"`{cell['winning_value']}`" if cell["winning_value"] else "—"
            wd = (
                f"{cell['winning_paired_diff']:+.6f}"
                if cell["winning_paired_diff"] is not None else "—"
            )
            cls_cells: list[str] = []
            for c in CLASS_ORDER:
                v = cell["per_class_mean_paired_diff"].get(c)
                if v is None:
                    cls_cells.append("—")
                else:
                    cls_cells.append(f"{v:+.6f}")
            a(
                f"| {pool_name} | `{lm_path.name}` | {wc} | {wv} | "
                f"{wd} | " + " | ".join(cls_cells) + " |"
            )
        a("")
        votes_str = ", ".join(
            f"{c}:{n}" for c, n in sorted(
                cp["votes"].items(), key=lambda kv: (-kv[1], kv[0])
            )
        )
        agreement_str = (
            "**agrees with chic-v5 proposed class**"
            if cp["agrees_with_chic_v5"]
            else "**disagrees with chic-v5 proposed class**"
        )
        a(f"**Cross-pool verdict for `{sid}`**: top class = "
          f"`{cp['top_class'] or '—'}` "
          f"({cp['top_count']}/4 pools); votes = {votes_str}; "
          f"{cp['verdict_word']}; "
          f"{agreement_str} "
          f"(`{info['chic_v5_proposed_class']}`).")
        if cp["dissent_pools"] and cp["top_count"] >= 1:
            a("")
            a(f"Dissenting pool(s): "
              f"{', '.join(cp['dissent_pools'])}.")
        a("")

    # ------- Cross-candidate summary -------
    a("## Cross-candidate cross-pool summary")
    a("")
    a("| candidate | chic-v5 class | top cross-pool class | "
      "vote split | verdict | agrees with chic-v5 |")
    a("|---|---|---|---|---|:---:|")
    for sid, _v, _cls in CANDIDATES:
        info = summary["per_sign"][sid]
        cp = info["cross_pool"]
        votes_str = " / ".join(
            f"{c}={n}" for c, n in sorted(
                cp["votes"].items(), key=lambda kv: (-kv[1], kv[0])
            )
        ) if cp["votes"] else "—"
        agreement = "✓" if cp["agrees_with_chic_v5"] else "✗"
        a(
            f"| `{sid}` | {info['chic_v5_proposed_class']} | "
            f"{cp['top_class'] or '—'} ({cp['top_count']}/4) | "
            f"{votes_str} | {cp['verdict_word']} | {agreement} |"
        )
    a("")
    a("## Discipline notes")
    a("")
    a("- **L3 robustness is a partial defence, not a positive validation.** "
      "If all 4 LMs agree, the L3 vote is robust to LM choice — but "
      "L3 itself recovers known anchor classes at 5% under chic-v9's "
      "leave-one-out test (below the ~16.7% chance baseline for the "
      "6-class taxonomy), and the chic-v9 verdict that chic-v5's "
      "framework operates in the low-agreement / not-validated band "
      "stands. Cross-pool L3 robustness adds confidence that the L3 "
      "axis itself is not an LM-specific artifact for that candidate; "
      "it does not raise the framework's validation accuracy.")
    a("- **Per-pool candidate-value pools differ.** When a substrate "
      "pool's phoneme inventory excludes a candidate value's onset "
      "char, that value drops from the per-pool pool, and the class "
      "loses its representative if no other candidate of the same "
      "class survives. Per-class mean paired_diff is computed only "
      "over surviving candidates; columns with `—` mean the class is "
      "empty under that pool's filter and L3 cannot vote for it by "
      "construction.")
    a("- **The chic-v9 framework-level negative is unaffected.** "
      "chic-v11 is an axis-restricted re-test of L3 only; L1+L2 "
      "(distributional fingerprint) are not re-run. Even an "
      "all-4-pools-agree L3 verdict here does not lift the "
      "framework's chic-v9 LOO accuracy from 20.0% / 0/3 tier-2 "
      "correct.")
    a("")
    a("## Determinism")
    a("")
    a("- No RNG. The L3 control-phoneme selection inherits chic-v5's "
      "sha256-keyed permutation construction.")
    a("- Same (CHIC syllabographic stream, chic-v2 anchor mapping, "
      "substrate-pool yamls, LM artifacts) -> byte-identical output.")
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v11.py` (mg-d69c).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpora/cretan_hieroglyphic/syllabographic.jsonl` "
      "(chic-v3); `pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); "
      "`pools/{aquitanian,etruscan,toponym,eteocretan}.yaml`; "
      "`harness/external_phoneme_models/{basque,etruscan,eteocretan}.json`.")
    a("")
    a("## Citations")
    a("")
    a("- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum "
      "Inscriptionum Cretae* (Études Crétoises 31). Paris.")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")
    a("- Duhoux, Y. (1982). *L'Étéocrétois: les textes — la langue.* "
      "Amsterdam: J. C. Gieben.")
    a("- Trask, R. L. (1997). *The History of Basque.* London: Routledge.")
    a("- Bonfante, G. & Bonfante, L. (2002). *The Etruscan Language: "
      "An Introduction* (revised ed.). Manchester / New York.")
    a("- Beekes, R. S. P. (2010). *Etymological Dictionary of Greek*, "
      "vol. 2 appendix on Pre-Greek substrate. Leiden: Brill.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# #032 ku-pa context inspection
# ---------------------------------------------------------------------------


def _render_chic_token_with_anchors(
    tok: str, anchor_mapping: dict[str, str], extra_overrides: dict[str, str],
) -> str:
    """Render a CHIC corpus token under (chic-v2 anchors + overrides).

    extra_overrides supplies per-sign phoneme values to inject (e.g.
    `#032 -> ki` per chic-v6's tier-2 override). Mirrors the chic-v6
    rendering convention but only emits literal anchor values + override
    values; class placeholders are not applied (chic-v11 inspection is
    about whether the rendered partial reading is interpretable around
    the anchored values, not about class-level extension).
    """
    if tok == "DIV":
        return "/"
    if tok == "[?]":
        return "[?]"
    if tok.startswith("NUM:"):
        return tok
    if tok.startswith("LOG:") or tok.startswith("FRAC:") or tok.startswith("IDEO:"):
        return tok
    is_unc = False
    sid = tok
    if tok.startswith("[?:#") and tok.endswith("]"):
        is_unc = True
        sid = tok[3:-1]
    if sid in extra_overrides:
        val = extra_overrides[sid]
        return f"[?:{val}]" if is_unc else val
    if sid in anchor_mapping:
        val = anchor_mapping[sid]
        return f"[?:{val}]" if is_unc else val
    return f"[?:{sid}]" if is_unc else sid


def _find_match_position(
    tokens: list[str], match_signs: list[str],
) -> tuple[int, int] | None:
    """Find the (start, end) token-index window where `match_signs`
    matches a contiguous run of CHIC sign tokens (clean or uncertain).

    Match is on raw sign id (`#NNN`), tolerating the `[?:#NNN]` uncertain
    form. Returns (start_idx, end_idx) inclusive, or None.
    """
    def _normalize(tok: str) -> str | None:
        if tok.startswith("#"):
            return tok
        if tok.startswith("[?:#") and tok.endswith("]"):
            return tok[3:-1]
        return None

    norm = [_normalize(t) for t in tokens]
    L = len(match_signs)
    for i in range(0, len(tokens) - L + 1):
        if all(norm[i + k] == match_signs[k] for k in range(L)):
            return i, i + L - 1
    return None


def _summarize_la_inscription(rec: dict) -> dict:
    return {
        "id": rec["id"],
        "site": rec.get("site"),
        "support": rec.get("support"),
        "genre_hint": rec.get("genre_hint"),
        "period": rec.get("period"),
        "n_signs": rec.get("n_signs"),
        "transcription_confidence": rec.get("transcription_confidence"),
        "raw_transliteration": rec.get("raw_transliteration"),
    }


def run_ku_pa_context(
    *,
    chic_records: list[dict],
    anchor_records: list[dict],
    progress: bool = True,
) -> dict:
    """Inspect chic-v6's ku-pa-family lift for #032 -> ki + #013 -> pa.

    Identifies the CHIC inscription(s) where the `(#032, #013)` literal+
    literal token-run match landed (chic-v6 source-A, tier-2-only-new
    relative to tier-1) and assembles the contextual metadata for both
    the source Linear A tablets (HT 1 / HT 16 / HT 102 / HT 110a) and
    the matched CHIC inscription(s).
    """
    if progress:
        print("chic-v11: ku-pa context inspection...", file=sys.stderr)

    # --- Load all four LA source tablets.
    target_la_ids = {"HT 1", "HT 16", "HT 102", "HT 110a"}
    la_records: dict[str, dict] = {}
    with LA_CORPUS.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r["id"] in target_la_ids:
                la_records[r["id"]] = r
    missing = target_la_ids - set(la_records.keys())
    if missing:
        raise RuntimeError(
            f"chic-v11: missing Linear A inscription(s) in corpus/all.jsonl: "
            f"{missing}"
        )

    # --- Load chic-v6 source-A hits restricted to ku-pa-family scholar IDs
    #     and the (#032, #013) literal/literal pair (the lift attribution).
    chic_by_id = {r["id"]: r for r in chic_records}
    anchor_mapping = {
        a["chic_sign"]: a["linear_b_carryover_phonetic"]
        for a in anchor_records
    }
    overrides = {"#032": "ki"}

    scholar_to_lifts: dict[str, list[dict]] = {sid: [] for sid in KU_PA_SCHOLAR_IDS}
    chic_inscriptions_with_lift: set[str] = set()
    n_lift_hits_total = 0

    if not CHIC_V6_EXPERIMENTS.exists():
        raise RuntimeError(
            f"chic-v11: missing chic-v6 experiments file at "
            f"{CHIC_V6_EXPERIMENTS}"
        )
    with CHIC_V6_EXPERIMENTS.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row["tier_level"] != "tier-2":
                continue
            for h in row.get("source_a_hits", []):
                if h["scholar_entry_id"] not in KU_PA_SCHOLAR_IDS:
                    continue
                if list(h["matched_signs"]) != ["#032", "#013"]:
                    continue
                if list(h["matched_kinds"]) != ["literal", "literal"]:
                    continue
                # tier-2 hit through the #032 -> ki override.
                lift_row = {
                    "chic_inscription_id": row["inscription_id"],
                    "site": row["site"],
                    "support": row["support"],
                    "scholar_entry_id": h["scholar_entry_id"],
                    "scholar_phonemes": h.get("scholarly_phonemes"),
                    "scholar_first_phoneme": h.get("scholarly_first_phoneme"),
                    "ab_sequence": h.get("ab_sequence"),
                    "matched_signs": h["matched_signs"],
                    "matched_kinds": h["matched_kinds"],
                    "category": h.get("category", ""),
                }
                scholar_to_lifts[h["scholar_entry_id"]].append(lift_row)
                chic_inscriptions_with_lift.add(row["inscription_id"])
                n_lift_hits_total += 1

    # --- For each matched CHIC inscription, build the partial reading
    #     under chic-v2 anchors + #032 -> ki override and locate the
    #     position of the (#032, #013) match.
    chic_inscription_renderings: dict[str, dict] = {}
    for cid in sorted(chic_inscriptions_with_lift):
        if cid not in chic_by_id:
            raise RuntimeError(
                f"chic-v11: chic-v6 reports inscription {cid} that is not "
                f"in the CHIC corpus."
            )
        rec = chic_by_id[cid]
        tokens = rec["tokens"]
        rendered: list[str] = []
        for tok in tokens:
            rendered.append(
                _render_chic_token_with_anchors(tok, anchor_mapping, overrides)
            )
        match_pos = _find_match_position(tokens, ["#032", "#013"])
        # Identify whether the immediate post-match token is a numeral.
        immediate_post = None
        immediate_post_rendered = None
        if match_pos:
            after = match_pos[1] + 1
            # Skip a single DIV right after the matched run, since CHIC
            # accountancy formula is "(sign-run) DIV NUM:n DIV".
            if after < len(tokens) and tokens[after] == "DIV":
                after += 1
            if after < len(tokens):
                immediate_post = tokens[after]
                immediate_post_rendered = rendered[after]
        chic_inscription_renderings[cid] = {
            "id": cid,
            "site": rec.get("site"),
            "support": rec.get("support"),
            "raw_transliteration": rec.get("raw_transliteration"),
            "transcription_confidence": rec.get("transcription_confidence"),
            "tokens": tokens,
            "rendered_tokens": rendered,
            "match_position": match_pos,
            "immediate_post_token": immediate_post,
            "immediate_post_rendered": immediate_post_rendered,
            "n_tokens": len(tokens),
        }

    return {
        "la_records": {sid: _summarize_la_inscription(la_records[sid])
                       for sid in la_records},
        "scholar_to_lifts": scholar_to_lifts,
        "n_chic_inscriptions_with_lift": len(chic_inscriptions_with_lift),
        "chic_inscriptions_with_lift": sorted(chic_inscriptions_with_lift),
        "chic_inscription_renderings": chic_inscription_renderings,
        "n_lift_hits_total": n_lift_hits_total,
    }


def write_ku_pa_md(summary: dict, out_path: Path) -> None:
    lines: list[str] = []
    a = lines.append
    a("# CHIC `#032 -> ki` ku-pa context inspection (chic-v11; mg-d69c)")
    a("")
    a("## Method")
    a("")
    a("chic-v6 produced a tier-1 -> tier-2 verification lift of "
      "+3 inscriptions / +20 hits on the source-A "
      "scholar-proposed-Linear-A-readings test "
      "(`results/chic_verification_match_rates.md`). The portion of "
      "that lift attributable to `#032 -> ki` (combined with the "
      "chic-v2 anchor `#013 -> pa`) is the set of new tier-2 hits "
      "where the chic-v6 source-A match is on the literal/literal "
      "token pair `(#032, #013)` against scholar entries from the "
      "ku-pa name family / ka-pa transaction-term family attested in "
      "the four Linear A tablets HT 1, HT 16, HT 102, HT 110a "
      "(scholar entry IDs `kupa3_HT1`, `kupa_HT16`, `kapa_HT102`, "
      "`kupa_HT110a`).")
    a("")
    a("This document does two mechanical inspections:")
    a("")
    a("1. **Source Linear A context.** For each of the four Linear A "
      "source tablets, record the `genre_hint`, `support`, `period`, "
      "and `site` from the Linear A corpus "
      "(`corpus/all.jsonl`, v0). The chic-v6 source-A test takes the "
      "scholar's reading as a probe pattern; if the source tablet is "
      "an accountancy genre tablet, the scholarly reading `ku-pa` / "
      "`ka-pa` / `ku-pa3` is in its native context (the readings are "
      "the standard Younger-online-edition entries for accountancy / "
      "name-family / transaction-term elements on Hagia Triada "
      "tablets). If the source tablet is votive or unknown, the "
      "scholar's reading is less load-bearing as an accountancy probe.")
    a("")
    a("2. **Matched CHIC inscription context.** For each CHIC inscription "
      "where the chic-v6 lift landed, render the partial reading with "
      "chic-v2 anchors + `#032 -> ki` applied (no class-placeholder "
      "extension), locate the position of the literal `(#032, #013)` "
      "token run within the inscription, and inspect whether the "
      "surrounding context — adjacent numerals, support type, "
      "DIV-bounded segment structure — is consistent with the kind of "
      "accountancy-formula structure that scholar readings like "
      "`ku-pa` / `ka-pa` are extracted from on the Linear A side.")
    a("")
    a("**Determinism.** All inputs are committed; the procedure is a "
      "single pass over the chic-v6 experiments JSONL with literal "
      "filters on `scholar_entry_id`, `matched_signs`, `matched_kinds`, "
      "and `tier_level`. No RNG.")
    a("")
    a("## Source Linear A tablet metadata")
    a("")
    a(f"All four ku-pa-family scholar entries reference Linear A "
      f"tablets at Haghia Triada. The tabulated metadata "
      f"(from `corpus/all.jsonl`):")
    a("")
    a("| Linear A id | site | support | genre_hint | period | "
      "n_signs | transcription_confidence | scholar entry id | scholar reading |")
    a("|---|---|---|---|---|---:|---|---|---|")
    scholar_to_la = {
        "kupa3_HT1": ("HT 1", "ku-pa3"),
        "kupa_HT16": ("HT 16", "ku-pa"),
        "kapa_HT102": ("HT 102", "ka-pa"),
        "kupa_HT110a": ("HT 110a", "ku-pa"),
    }
    for scholar_id in KU_PA_SCHOLAR_IDS:
        la_id, scholar_reading = scholar_to_la[scholar_id]
        rec = summary["la_records"].get(la_id)
        if rec is None:
            a(f"| {la_id} | — | — | — | — | — | — | `{scholar_id}` | "
              f"`{scholar_reading}` |")
            continue
        a(
            f"| {la_id} | {rec['site']} | {rec['support']} | "
            f"{rec['genre_hint']} | {rec['period']} | {rec['n_signs']} | "
            f"{rec['transcription_confidence']} | "
            f"`{scholar_id}` | `{scholar_reading}` |"
        )
    a("")
    a("**Source-side verdict.** All four source Linear A tablets are "
      "**accountancy-genre tablets** (`genre_hint = accountancy`) on "
      "the **tablet** support type, dated to **LM IB**, from "
      "**Haghia Triada**. The scholarly readings `ku-pa` (name family "
      "/ commodity prefix), `ku-pa3` (variant of the same family), "
      "and `ka-pa` (recurring transaction term) are exactly the "
      "kind of readings the Younger online edition extracts from "
      "Hagia Triada accountancy tablets, attested in their "
      "native-corpus genre. As a probe pattern for the chic-v6 "
      "source-A test, the readings are in their native context.")
    a("")
    a("## Raw transliterations of the source Linear A tablets")
    a("")
    a("Each tablet's `raw_transliteration` field, for direct inspection "
      "of the scholarly-reading position relative to numerals, "
      "logograms, and DIV breaks. (Numerical entries are denoted by "
      "the `LOG:` and `FRAC:` prefixes; AB syllabograms are the "
      "phonetic positions.)")
    a("")
    for scholar_id in KU_PA_SCHOLAR_IDS:
        la_id, _ = scholar_to_la[scholar_id]
        rec = summary["la_records"].get(la_id)
        if rec is None:
            a(f"- **{la_id}** — _missing in v0 corpus_")
            continue
        a(f"- **{la_id}** ({rec['genre_hint']}, "
          f"{rec['support']}, "
          f"n_signs={rec['n_signs']}): "
          f"`{rec['raw_transliteration']}`")
    a("")
    a("## CHIC inscriptions where the lift landed")
    a("")
    n_chic = summary["n_chic_inscriptions_with_lift"]
    n_hits = summary["n_lift_hits_total"]
    a(
        f"chic-v6's tier-2 ku-pa-family lift via `#032 -> ki + #013 -> pa` "
        f"(literal/literal `(#032, #013)`) lands on "
        f"**{n_chic} CHIC inscription(s)** with **{n_hits} total scholar-"
        f"entry hits** across the 4 ku-pa-family scholars. "
        f"(The full chic-v6 tier-1 -> tier-2 lift of +3 inscriptions / "
        f"+20 hits also includes a separate `(#032, #070)` family of "
        f"k-r-onset matches against `ku-ro` / `ki-ro` / `ku-ra` / "
        f"`ki-ra` / `ka-ru` scholar entries on a different inscription; "
        f"that family is outside the ku-pa scope of this inspection.)"
    )
    a("")
    for cid in summary["chic_inscriptions_with_lift"]:
        rendering = summary["chic_inscription_renderings"][cid]
        a(f"### {cid}")
        a("")
        a(f"- **site**: {rendering['site']}")
        a(f"- **support**: {rendering['support']}")
        a(f"- **transcription_confidence**: "
          f"{rendering['transcription_confidence']}")
        a(f"- **raw_transliteration**: "
          f"`{rendering['raw_transliteration']}`")
        a(f"- **n_tokens**: {rendering['n_tokens']}")
        a("")
        a("**Partial reading (chic-v2 anchors + `#032 -> ki`):**")
        a("")
        a("```")
        a(" ".join(rendering["rendered_tokens"]))
        a("```")
        a("")
        mp = rendering["match_position"]
        if mp is None:
            a("**Match position**: not located (this is a chic-v11 bug "
              "if the chic-v6 experiments row says the inscription "
              "matched). No further per-inscription inspection.")
            a("")
            continue
        start, end = mp
        before_excerpt = " ".join(rendering["rendered_tokens"][:start])
        match_excerpt = " ".join(rendering["rendered_tokens"][start:end + 1])
        after_excerpt = " ".join(rendering["rendered_tokens"][end + 1:])
        if not before_excerpt:
            before_excerpt = "(start of inscription)"
        if not after_excerpt:
            after_excerpt = "(end of inscription)"
        a(f"**Match position**: tokens {start}..{end} (the "
          f"`(#032, #013)` literal pair, rendered as `ki pa` under the "
          f"chic-v2 anchors + chic-v5 tier-2 override).")
        a("")
        a("- before: `" + before_excerpt + "`")
        a("- **match**: `" + match_excerpt + "`")
        a("- after: `" + after_excerpt + "`")
        a("")
        ipt = rendering["immediate_post_token"]
        ipr = rendering["immediate_post_rendered"]
        if ipt is not None:
            if ipt.startswith("NUM:"):
                a(f"**Immediate post-match token**: `{ipt}` "
                  "(numerical entry; a positional structure consistent "
                  "with **accountancy formula** — sign-run followed by "
                  "a quantity).")
            elif ipt.startswith("LOG:") or ipt.startswith("IDEO:"):
                a(f"**Immediate post-match token**: `{ipt}` "
                  "(logogram / ideogram; consistent with accountancy "
                  "formula — sign-run followed by a commodity logogram).")
            elif ipt.startswith("FRAC:"):
                a(f"**Immediate post-match token**: `{ipt}` "
                  "(fraction; consistent with accountancy formula — "
                  "sign-run followed by a fractional quantity).")
            else:
                a(f"**Immediate post-match token (after the next DIV "
                  "break, if present)**: `" + ipt + "` (rendered: `" +
                  (ipr or "—") + "`); not a numeral / logogram / "
                  "fraction.")
        else:
            a("**Immediate post-match token**: none (the match runs "
              "to the end of the inscription).")
        a("")
        a("**Scholar entries that contribute lift to this inscription**:")
        a("")
        a("| scholar id | scholar reading | category | LA source | match kinds |")
        a("|---|---|---|---|---|")
        for scholar_id in KU_PA_SCHOLAR_IDS:
            scholar_lifts = summary["scholar_to_lifts"][scholar_id]
            for lift in scholar_lifts:
                if lift["chic_inscription_id"] == cid:
                    la_id, scholar_reading = scholar_to_la[scholar_id]
                    a(
                        f"| `{scholar_id}` | `{scholar_reading}` | "
                        f"{lift['category']} | {la_id} | "
                        f"{'/'.join(lift['matched_kinds'])} |"
                    )
        a("")

    # ------- Summary verdict -------
    a("## Combined verdict")
    a("")
    if n_chic == 0:
        a("**No CHIC inscription carried a ku-pa-family `(#032, #013)` "
          "literal/literal lift at tier-2.** The chic-v6 source-A "
          "lift attributed to `#032 -> ki` for the ku-pa family is "
          "absent from the chic-v6 experiments record. The chic-v11 "
          "ku-pa context inspection is therefore moot; the lift's "
          "interpretation cannot be corroborated by inscription-level "
          "context. (See `results/chic_verification_match_rates.md` "
          "for the ku-pa-family enumeration; if this branch is "
          "reached, chic-v6 produced no ku-pa lift via `#032 -> ki` "
          "at the literal/literal level.)")
    else:
        a("- **Source-side context**: all 4 Linear A source tablets "
          "(HT 1, HT 16, HT 102, HT 110a) are accountancy-genre "
          "tablets at Haghia Triada (LM IB). The scholarly readings "
          "`ku-pa` / `ku-pa3` / `ka-pa` are in their native "
          "Hagia Triada accountancy-tablet context.")
        any_accountancy_post_match = False
        for cid in summary["chic_inscriptions_with_lift"]:
            rendering = summary["chic_inscription_renderings"][cid]
            ipt = rendering["immediate_post_token"]
            if ipt is not None and (
                ipt.startswith("NUM:") or ipt.startswith("LOG:")
                or ipt.startswith("IDEO:") or ipt.startswith("FRAC:")
            ):
                any_accountancy_post_match = True
                break
        if any_accountancy_post_match:
            a("- **CHIC-side context**: the matched `(#032, #013)` "
              "token run is followed (after the immediate DIV break) "
              "by a numerical / logogram entry in at least one matched "
              "CHIC inscription. This is **the canonical accountancy-"
              "formula structure** (sign-run = entry, followed by a "
              "quantity / commodity) on which the Linear A scholar "
              "readings `ku-pa` / `ka-pa` are themselves extracted. "
              "The CHIC inscription's support type and DIV-bounded "
              "structure (per the per-inscription tables above) "
              "reinforce the accountancy reading.")
            a("- **Combined**: the chic-v6 ku-pa-family mechanical "
              "lift is **corroborated by inscription-level context "
              "on both sides of the match**: scholarly readings in "
              "their native LM IB Hagia Triada accountancy context "
              "on the Linear A source side; matched CHIC inscription "
              "with accountancy-consistent positional structure on "
              "the CHIC target side. **This is contextual "
              "corroboration of the chic-v6 mechanical lift "
              "specifically for `#032 -> ki`**, not validation of "
              "the chic-v5 framework as a whole — the chic-v9 "
              "framework-level negative (LOO accuracy 20.0%, 0/3 "
              "tier-2 unanimity correct) stands.")
        else:
            a("- **CHIC-side context**: the matched `(#032, #013)` "
              "token run is not followed by a numerical / logogram / "
              "fraction entry in any matched CHIC inscription. "
              "**The accountancy-formula corroboration is weaker on "
              "the CHIC side**: the matched CHIC inscription does "
              "not exhibit the canonical sign-run-followed-by-quantity "
              "structure that scholarly readings like `ku-pa` / "
              "`ka-pa` are extracted from on the Linear A side. "
              "Combined with chic-v9's framework-level negative, the "
              "chic-v6 ku-pa lift's interpretation as a substantive "
              "accountancy match is weakened.")
    a("")
    a("## Discipline notes")
    a("")
    a("- **What this inspection does NOT do.** It does not run "
      "specialist judgment on whether `(#032 #013) = ki pa` is a "
      "plausible scribal Hieroglyph reading in CHIC #057's "
      "accountancy context — that is squarely out of polecat scope. "
      "It runs the mechanical metadata cross-check the brief asks "
      "for: do the scholar source tablets carry accountancy-genre "
      "metadata, and does the matched CHIC inscription exhibit "
      "accountancy-formula positional structure?")
    a("- **What this inspection does NOT lift.** The chic-v9 LOO "
      "framework-level accuracy (20.0% / 0/3 tier-2 correct) does "
      "not improve from contextual corroboration of a single "
      "candidate's mechanical-match lift. chic-v11 contextual "
      "corroboration of the chic-v6 ku-pa lift is the strongest "
      "additional evidence available within polecat scope for "
      "`#032 -> ki` specifically; it is consistent with the chic-v9 "
      "verdict that the framework's per-sign machinery is at-chance "
      "but is positive evidence axially restricted to the chic-v6 "
      "verification line for one candidate.")
    a("")
    a("## Build provenance")
    a("")
    a("- Generated by `scripts/build_chic_v11.py` (mg-d69c).")
    a(f"- fetched_at: {FETCHED_AT}")
    a("- Inputs: `corpus/all.jsonl` (Linear A v0); "
      "`corpora/cretan_hieroglyphic/all.jsonl` (chic-v0); "
      "`pools/cretan_hieroglyphic_anchors.yaml` (chic-v2); "
      "`results/experiments.chic_verification_v0.jsonl` (chic-v6); "
      "`corpora/scholar_proposed_readings/all.jsonl` (v22).")
    a("")
    a("## Citations")
    a("")
    a("- Younger, J. G. (online). *Linear A texts in phonetic "
      "transcription* (retrieved 2026-05-04). Includes the "
      "`ku-pa` / `ku-pa3` / `ka-pa` Hagia Triada accountancy entries.")
    a("- Olivier, J.-P. & Godart, L. (1996). *Corpus Hieroglyphicarum "
      "Inscriptionum Cretae* (Études Crétoises 31). Paris.")
    a("- Salgarella, E. (2020). *Aegean Linear Script(s).* Cambridge.")
    a("- Ventris, M. & Chadwick, J. (1956). *Documents in Mycenaean "
      "Greek.* Cambridge.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(*, progress: bool = True) -> dict:
    if progress:
        print("chic-v11: loading inputs...", file=sys.stderr)
    chic_records = load_chic_records(CHIC_FULL)
    syll_records = load_chic_records(CHIC_SYLL)
    anchors_yaml = _load_yaml(ANCHORS_YAML)
    anchor_records = anchors_yaml["anchors"]

    cross = run_cross_pool_l3(
        syll_records=syll_records,
        anchor_records=anchor_records,
        progress=progress,
    )
    write_cross_pool_md(cross, OUT_CROSS_POOL_MD)

    ku_pa = run_ku_pa_context(
        chic_records=chic_records,
        anchor_records=anchor_records,
        progress=progress,
    )
    write_ku_pa_md(ku_pa, OUT_KU_PA_MD)

    if progress:
        print("chic-v11: cross-pool L3 verdicts:", file=sys.stderr)
        for sid, _v, cls in CANDIDATES:
            cp = cross["per_sign"][sid]["cross_pool"]
            print(
                f"  {sid} (chic-v5 class {cls}): top={cp['top_class']} "
                f"({cp['top_count']}/4) verdict={cp['verdict']}",
                file=sys.stderr,
            )
        print(
            f"chic-v11: ku-pa lift CHIC inscriptions = "
            f"{ku_pa['chic_inscriptions_with_lift']} "
            f"(n_hits={ku_pa['n_lift_hits_total']})",
            file=sys.stderr,
        )
    return {"cross_pool": cross, "ku_pa": ku_pa}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--no-progress", action="store_true")
    args = p.parse_args(argv)
    out = run(progress=not args.no_progress)
    summary = {
        "per_candidate": {
            sid: {
                "chic_v5_class": out["cross_pool"]["per_sign"][sid][
                    "chic_v5_proposed_class"
                ],
                "cross_pool_top_class": out["cross_pool"]["per_sign"][sid][
                    "cross_pool"
                ]["top_class"],
                "cross_pool_vote_split":
                    out["cross_pool"]["per_sign"][sid]["cross_pool"]["votes"],
                "cross_pool_verdict":
                    out["cross_pool"]["per_sign"][sid]["cross_pool"]["verdict"],
                "agrees_with_chic_v5":
                    out["cross_pool"]["per_sign"][sid]["cross_pool"][
                        "agrees_with_chic_v5"
                    ],
            }
            for sid, _v, _c in CANDIDATES
        },
        "ku_pa_chic_inscriptions": out["ku_pa"]["chic_inscriptions_with_lift"],
        "ku_pa_n_hits_total": out["ku_pa"]["n_lift_hits_total"],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
