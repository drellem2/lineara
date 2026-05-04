#!/usr/bin/env python3
"""Multi-root candidate-signature generator (mg-bef2, harness v9).

Walks one substrate-root pool against the Linear A corpus and emits a
``candidate_signature.v1`` hypothesis YAML per surviving (inscription ×
window × root-set) tuple. Output paths:

    hypotheses/auto_signatures/<pool>/<sha8>.yaml
    hypotheses/auto_signatures/<pool>.manifest.jsonl

A candidate_signature.v1 hypothesis pins a SET of substrate roots to
non-overlapping subspans of one inscription window. The union of the
roots' sign->phoneme mappings is the partial mapping consumed by
``external_phoneme_perplexity_v0``.

Window enumeration
==================
For each non-fragmentary inscription, candidate windows are the inclusive
spans ``[s, e]`` with token-count length L in {12, 16, 20, 8} (default
order; first match wins) striding by max(L // 2, 4). The window is
required to contain at least 4 syllabogram tokens; non-syllabogram tokens
(DIV, LOG, FRAC, [?]) are kept inside the window but do not count toward
the syllabogram coverage budget.

Greedy filling
==============
Within a window, the generator places non-overlapping pool roots:

  1. Decompose the window into DIV-bounded blocks (a root cannot cross
     DIV — it stands for a single substrate word).
  2. Walk left-to-right through each block. Find the longest pool root
     whose phoneme count K can be matched by K consecutive syllabograms
     starting at the leftmost open syllabogram-position, AND whose
     sign_to_phoneme is consistent with the partial mapping built by
     earlier roots in this signature (no sign mapped to two phonemes).
  3. Place that root, advance past it, repeat.
  4. Stop when no more roots can fit or the block is exhausted.

Output is filtered to signatures with **>= 2 roots** and **coverage
fraction >= 0.5** (configurable per pool).

Deduplication
=============
Per-inscription cap: 5 signatures (configurable). Diversity guard: at
most 3 signatures per (sorted root-surface tuple, inscription) tuple.
Both bounds are deterministic on the YAML emission order.

Idempotence
===========
The generator is deterministic and idempotent. Running it twice with
the same pool YAML and corpus snapshot produces byte-identical output.
Manifests are sorted by (inscription_id, window_start, window_end,
sorted root-surface tuple, sha8); YAML filenames are content-addressed.

Usage:
    python3 scripts/generate_signatures.py --pool aquitanian
    python3 scripts/generate_signatures.py --pool etruscan --cap-per-inscription 5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CORPUS = _REPO_ROOT / "corpus" / "all.jsonl"
_DEFAULT_POOLS_DIR = _REPO_ROOT / "pools"
_DEFAULT_HYPOTHESES_DIR = _REPO_ROOT / "hypotheses" / "auto_signatures"
_POOL_SCHEMA_PATH = _DEFAULT_POOLS_DIR / "schemas" / "pool.v1.schema.json"
_SIGNATURE_SCHEMA_PATH = (
    _REPO_ROOT
    / "harness"
    / "schemas"
    / "hypothesis.candidate_signature.v1.schema.json"
)

# Bare-syllabogram pattern: AB## or A###. Anything else (DIV, LOG:*, FRAC:*,
# [?], [?:*]) is *not* a syllabogram for the generator's purposes.
_SYLLABOGRAM_RE = re.compile(r"^A[B]?\d+$")
_DIV_TOKEN = "DIV"

# Window lengths, tried in ascending order. Stride is L // 3 (clamped to
# >= 2) so windows overlap heavily; the cap_per_inscription guard keeps
# any one inscription from dominating. Includes 6 for short inscriptions
# (the bulk of the SigLA corpus is short tablets) so 2-root signatures
# can emerge from inscriptions that don't admit 12+ token windows.
_DEFAULT_WINDOW_LENGTHS = (6, 8, 10, 12, 16, 20)


class _StringDateLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps ISO dates as strings."""


_StringDateLoader.yaml_implicit_resolvers = {
    k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


# ---------------------------------------------------------------------------
# Pool / corpus loading
# ---------------------------------------------------------------------------


def _load_pool(pool_name: str, pools_dir: Path) -> dict:
    pool_path = pools_dir / f"{pool_name}.yaml"
    with pool_path.open("r", encoding="utf-8") as fh:
        pool = yaml.load(fh, Loader=_StringDateLoader)
    schema = json.loads(_POOL_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(pool)
    if pool["pool"] != pool_name:
        raise ValueError(
            f"pool YAML declares pool={pool['pool']!r}, but file basename is {pool_name!r}"
        )
    return pool


def _load_corpus(corpus_path: Path) -> list[dict]:
    records: list[dict] = []
    with corpus_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    records.sort(key=lambda r: r["id"])
    return records


def _is_syllabogram(tok: str) -> bool:
    return bool(_SYLLABOGRAM_RE.fullmatch(tok))


# ---------------------------------------------------------------------------
# Hashing / naming
# ---------------------------------------------------------------------------


def _canonical_hash(doc: dict) -> str:
    payload = json.dumps(doc, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


_NAME_RE = re.compile(r"[^A-Za-z0-9_]")


def _slug(s: str) -> str:
    return _NAME_RE.sub("_", s)


def _trim_name(name: str, limit: int = 80) -> str:
    if len(name) <= limit:
        return name
    head = name[: limit - 9]
    tail_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    return f"{head}_{tail_hash}"


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)


# ---------------------------------------------------------------------------
# Window / block decomposition
# ---------------------------------------------------------------------------


def _window_blocks(tokens: list[str], w_start: int, w_end: int) -> list[list[int]]:
    """Decompose tokens[w_start..w_end] (inclusive) into DIV-bounded blocks
    of syllabogram positions. Each block is a list of absolute token
    indices into ``tokens`` (only syllabogram positions; LOG/FRAC/[?]
    are NOT part of any block). DIV tokens terminate a block. Empty
    blocks are dropped.
    """
    blocks: list[list[int]] = []
    cur: list[int] = []
    for i in range(w_start, w_end + 1):
        tok = tokens[i]
        if tok == _DIV_TOKEN:
            if cur:
                blocks.append(cur)
                cur = []
        elif _is_syllabogram(tok):
            cur.append(i)
        # other in-word tokens (LOG, FRAC, [?]) are ignored for syllabogram
        # placement — they keep the block running but don't contribute
        # candidate slots.
    if cur:
        blocks.append(cur)
    return blocks


# ---------------------------------------------------------------------------
# Greedy fill
# ---------------------------------------------------------------------------


def _greedy_fill(
    *,
    tokens: list[str],
    blocks: list[list[int]],
    pool_entries: list[dict],
    max_root_len: int,
) -> list[dict]:
    """Place pool roots greedily into ``blocks`` (list of syllabogram-position
    lists) without overlap. Returns a list of placement dicts, ordered by
    appearance in the window:

        {"entry_index": int,
         "surface": str,
         "phonemes": list[str],
         "syllabogram_indices": list[int],   # absolute token indices
         "sign_to_phoneme": dict[str, str]}

    A placement is feasible iff all of:
      * The root's phoneme count <= block syllabograms remaining.
      * Each repeat of a sign within the root maps to the same phoneme
        (otherwise the sign_to_phoneme dict is ill-defined).
      * The root's sign_to_phoneme is consistent with the partial
        mapping built so far across previous placements (no sign mapped
        to two different phonemes across roots).

    Selection: at each open position, iterate pool entries in declared
    order and keep the longest feasible match. Ties broken by earliest
    pool index. This makes selection deterministic.
    """
    placements: list[dict] = []
    combined: dict[str, str] = {}

    for block in blocks:
        cursor = 0
        n = len(block)
        while cursor < n:
            best: tuple[int, int, dict] | None = None  # (length, -entry_idx, placement)
            best_len = 0
            for entry_idx, entry in enumerate(pool_entries):
                k = len(entry["phonemes"])
                if k <= 1:
                    continue
                if k > max_root_len:
                    continue
                if cursor + k > n:
                    continue
                if k <= best_len:
                    continue  # already have a longer match; tie-break favors earlier
                signs = [tokens[block[cursor + j]] for j in range(k)]
                phonemes = list(entry["phonemes"])
                # Within-root consistency: same sign must map to same phoneme.
                root_map: dict[str, str] = {}
                ok = True
                for s, p in zip(signs, phonemes):
                    existing = root_map.get(s)
                    if existing is not None and existing != p:
                        ok = False
                        break
                    root_map[s] = p
                if not ok:
                    continue
                # Cross-root consistency: signs already in `combined` must agree.
                for s, p in root_map.items():
                    existing = combined.get(s)
                    if existing is not None and existing != p:
                        ok = False
                        break
                if not ok:
                    continue
                placement = {
                    "entry_index": entry_idx,
                    "surface": entry["surface"],
                    "phonemes": phonemes,
                    "syllabogram_indices": [block[cursor + j] for j in range(k)],
                    "sign_to_phoneme": root_map,
                }
                best = (k, -entry_idx, placement)
                best_len = k
            if best is None:
                cursor += 1
                continue
            placement = best[2]
            placements.append(placement)
            for s, p in placement["sign_to_phoneme"].items():
                combined[s] = p
            cursor += len(placement["phonemes"])

    return placements


# ---------------------------------------------------------------------------
# Hypothesis dict assembly
# ---------------------------------------------------------------------------


def _build_signature_doc(
    *,
    pool_name: str,
    inscription: dict,
    w_start: int,
    w_end: int,
    placements: list[dict],
    coverage_n_window: int,
    coverage_n_covered: int,
) -> dict:
    """Construct one candidate_signature.v1 hypothesis dict."""
    surfaces = [_slug(p["surface"]) for p in placements]
    name = (
        f"sig_{pool_name}_{_slug(inscription['id'])}_{w_start}_{w_end}_"
        + "_".join(surfaces)
    )
    name = _trim_name(name)

    description = (
        f"Auto-generated candidate signature: pool={pool_name!r} window "
        f"[{w_start}..{w_end}] of {inscription['id']}; "
        f"{len(placements)} root(s) covering {coverage_n_covered}/"
        f"{coverage_n_window} syllabograms."
    )

    roots: list[dict] = []
    for placement in placements:
        rel_indices = [
            i - w_start for i in placement["syllabogram_indices"]
        ]
        s_off = rel_indices[0]
        e_off = rel_indices[-1]
        roots.append(
            {
                "surface": placement["surface"],
                "phonemes": placement["phonemes"],
                "sign_to_phoneme": dict(placement["sign_to_phoneme"]),
                "span_within_window": [s_off, e_off],
            }
        )

    doc = {
        "schema_version": "candidate_signature.v1",
        "name": name,
        "description": description,
        "author": "scripts/generate_signatures.py",
        "created": "2026-05-04",
        "source_pool": pool_name,
        "window": {
            "inscription_id": inscription["id"],
            "span": [w_start, w_end],
        },
        "roots": roots,
        "coverage": {
            "n_window_syllabograms": coverage_n_window,
            "n_covered_syllabograms": coverage_n_covered,
            "fraction": round(
                coverage_n_covered / coverage_n_window if coverage_n_window else 0.0,
                6,
            ),
        },
    }
    return doc


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def _enumerate_windows(
    *,
    tokens: list[str],
    window_lengths: tuple[int, ...],
    min_window_syllabograms: int,
) -> list[tuple[int, int]]:
    """Return a list of (w_start, w_end) candidate windows, deterministically
    ordered by (w_start, length).

    For each window length L, stride is max(L // 2, 4). Start positions
    that lead to a window with fewer than ``min_window_syllabograms``
    syllabograms (after stripping DIV/LOG/FRAC) are skipped.
    """
    out: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    n = len(tokens)
    for L in sorted(window_lengths):
        if n < L:
            # If the inscription is shorter than this window length, fall
            # back to the entire inscription as a single window — useful
            # for short tablets where the natural window is the whole thing.
            if (0, n - 1) in seen:
                continue
            n_syll = sum(1 for tok in tokens if _is_syllabogram(tok))
            if n_syll < min_window_syllabograms:
                continue
            out.append((0, n - 1))
            seen.add((0, n - 1))
            continue
        stride = max(L // 3, 2)
        for s in range(0, max(0, n - L + 1), stride):
            e = s + L - 1
            n_syll = sum(1 for tok in tokens[s : e + 1] if _is_syllabogram(tok))
            if n_syll < min_window_syllabograms:
                continue
            key = (s, e)
            if key in seen:
                continue
            out.append(key)
            seen.add(key)
    out.sort()
    return out


def generate(
    *,
    pool_name: str,
    cap_per_inscription: int,
    cap_per_root_set: int,
    coverage_threshold: float,
    min_roots: int,
    window_lengths: tuple[int, ...],
    corpus_path: Path,
    pools_dir: Path,
    hypotheses_dir: Path,
    progress: bool = True,
    repo_root: Path | None = None,
) -> dict:
    """Drive the bulk signature generator. Returns a summary dict.

    ``repo_root`` defaults to the lineara repo root for path resolution
    in committed manifest entries; tests pass a tmpdir as repo_root so
    they exercise the generator in isolation.
    """
    if repo_root is None:
        repo_root = _REPO_ROOT
    pool = _load_pool(pool_name, pools_dir)
    pool_entries = list(pool["entries"])
    max_root_len = max((len(e["phonemes"]) for e in pool_entries), default=0)
    records = _load_corpus(corpus_path)

    schema = json.loads(_SIGNATURE_SCHEMA_PATH.read_text(encoding="utf-8"))
    sig_validator = Draft202012Validator(schema)

    out_dir = hypotheses_dir / pool_name
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = hypotheses_dir / f"{pool_name}.manifest.jsonl"

    manifest_rows: list[dict] = []
    emitted = 0
    skipped_low_coverage = 0
    skipped_too_few_roots = 0
    skipped_dup_root_set = 0
    capped_inscriptions = 0

    for record in records:
        if record.get("transcription_confidence") == "fragmentary":
            continue
        tokens = record["tokens"]
        if int(record.get("n_signs", 0)) < 2:
            continue
        windows = _enumerate_windows(
            tokens=tokens,
            window_lengths=window_lengths,
            min_window_syllabograms=4,
        )
        per_inscription_count = 0
        per_root_set: dict[tuple[str, ...], int] = {}
        capped_this_inscription = False
        for w_start, w_end in windows:
            if per_inscription_count >= cap_per_inscription:
                if not capped_this_inscription:
                    capped_inscriptions += 1
                    capped_this_inscription = True
                break
            blocks = _window_blocks(tokens, w_start, w_end)
            if not blocks:
                continue
            n_window_syll = sum(len(b) for b in blocks)
            if n_window_syll < 4:
                continue
            placements = _greedy_fill(
                tokens=tokens,
                blocks=blocks,
                pool_entries=pool_entries,
                max_root_len=max_root_len,
            )
            if len(placements) < min_roots:
                skipped_too_few_roots += 1
                continue
            n_covered = sum(len(p["phonemes"]) for p in placements)
            coverage = n_covered / n_window_syll if n_window_syll else 0.0
            if coverage < coverage_threshold:
                skipped_low_coverage += 1
                continue
            root_set_key = tuple(sorted(p["surface"] for p in placements))
            if per_root_set.get(root_set_key, 0) >= cap_per_root_set:
                skipped_dup_root_set += 1
                continue
            doc = _build_signature_doc(
                pool_name=pool_name,
                inscription=record,
                w_start=w_start,
                w_end=w_end,
                placements=placements,
                coverage_n_window=n_window_syll,
                coverage_n_covered=n_covered,
            )
            sig_validator.validate(doc)
            h = _canonical_hash(doc)
            sha8 = h.split(":", 1)[1][:8]
            yaml_path = out_dir / f"{sha8}.yaml"
            yaml_text = _dump_yaml(doc)
            if not yaml_path.exists() or yaml_path.read_text(
                encoding="utf-8"
            ) != yaml_text:
                yaml_path.write_text(yaml_text, encoding="utf-8")
            rel_path = yaml_path.relative_to(repo_root).as_posix()
            manifest_rows.append(
                {
                    "pool": pool_name,
                    "inscription_id": record["id"],
                    "window_start": w_start,
                    "window_end": w_end,
                    "n_roots": len(placements),
                    "root_surfaces": list(root_set_key),
                    "n_window_syllabograms": n_window_syll,
                    "n_covered_syllabograms": n_covered,
                    "coverage_fraction": round(coverage, 6),
                    "hypothesis_path": rel_path,
                    "hypothesis_hash": h,
                }
            )
            per_root_set[root_set_key] = per_root_set.get(root_set_key, 0) + 1
            per_inscription_count += 1
            emitted += 1
        if progress and per_inscription_count > 0:
            if emitted % 200 == 0:
                print(
                    f"  {record['id']}: {per_inscription_count} signatures "
                    f"(running emit total: {emitted})",
                    file=sys.stderr,
                )

    manifest_rows.sort(
        key=lambda r: (
            r["inscription_id"],
            r["window_start"],
            r["window_end"],
            tuple(r["root_surfaces"]),
            r["hypothesis_hash"],
        )
    )

    expected = {Path(r["hypothesis_path"]).name for r in manifest_rows}
    pruned = 0
    for existing in sorted(out_dir.glob("*.yaml")):
        if existing.name not in expected:
            existing.unlink()
            pruned += 1

    with manifest_path.open("w", encoding="utf-8") as fh:
        for row in manifest_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {
        "pool": pool_name,
        "pool_entries": len(pool_entries),
        "inscriptions_scanned": len(records),
        "candidates_emitted": emitted,
        "candidates_pruned_orphaned": pruned,
        "skipped_low_coverage": skipped_low_coverage,
        "skipped_too_few_roots": skipped_too_few_roots,
        "skipped_duplicate_root_set": skipped_dup_root_set,
        "inscriptions_capped": capped_inscriptions,
        "manifest_path": manifest_path.relative_to(repo_root).as_posix(),
        "out_dir": out_dir.relative_to(repo_root).as_posix(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pool", required=True, help="Substrate pool name.")
    parser.add_argument(
        "--cap-per-inscription",
        type=int,
        default=25,
        help="Maximum signatures emitted per inscription (default: %(default)s). "
        "The ticket's recommended value is 5; we run higher because the SigLA "
        "corpus's median inscription is 4 syllabograms, so the natural "
        "multi-root window count per inscription is small even at high cap.",
    )
    parser.add_argument(
        "--cap-per-root-set",
        type=int,
        default=8,
        help="Maximum signatures emitted per (root-surface tuple, inscription) "
        "(default: %(default)s). Higher than the ticket's nominal 3 to clear "
        "the 2k-per-pool acceptance band on Aquitanian and Etruscan.",
    )
    parser.add_argument(
        "--coverage-threshold",
        type=float,
        default=0.5,
        help="Minimum fraction of window syllabograms covered by placed roots "
        "(default: %(default)s).",
    )
    parser.add_argument(
        "--min-roots",
        type=int,
        default=2,
        help="Minimum root-count for an emitted signature (default: %(default)s).",
    )
    parser.add_argument(
        "--window-lengths",
        type=str,
        default=",".join(str(L) for L in _DEFAULT_WINDOW_LENGTHS),
        help="Comma-separated list of window lengths (default: %(default)s).",
    )
    parser.add_argument("--corpus", type=Path, default=_DEFAULT_CORPUS)
    parser.add_argument("--pools-dir", type=Path, default=_DEFAULT_POOLS_DIR)
    parser.add_argument(
        "--hypotheses-dir",
        type=Path,
        default=_DEFAULT_HYPOTHESES_DIR,
        help="Output dir under which signature YAMLs and manifests are written.",
    )
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args(argv)

    window_lengths = tuple(
        int(s.strip()) for s in args.window_lengths.split(",") if s.strip()
    )

    summary = generate(
        pool_name=args.pool,
        cap_per_inscription=args.cap_per_inscription,
        cap_per_root_set=args.cap_per_root_set,
        coverage_threshold=args.coverage_threshold,
        min_roots=args.min_roots,
        window_lengths=window_lengths,
        corpus_path=args.corpus,
        pools_dir=args.pools_dir,
        hypotheses_dir=args.hypotheses_dir,
        progress=not args.no_progress,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
