"""Scoring metrics. v0 ships exactly one: compression_delta_v0."""

from __future__ import annotations

import zlib
from dataclasses import dataclass

from .corpus import apply_mapping


# Frozen for v0. Changing any of these is a harness_version bump.
_ZLIB_LEVEL = 9
_ZLIB_WBITS = 15  # default deflate window; explicit so we don't drift
_SYMBOL_BYTES = 2  # big-endian 16-bit token IDs
_MAX_UNIQUE = 1 << (8 * _SYMBOL_BYTES)


@dataclass(frozen=True)
class CompressionResult:
    score: float
    bits_per_sign_baseline: float
    bits_per_sign_mapped: float
    baseline_bits: int
    mapped_bits: int
    stream_length: int


def _encode_to_bytes(stream: list[str]) -> bytes:
    """Map each unique token to a fixed 16-bit ID (sorted-lex order) and emit
    big-endian. Distinct token, distinct symbol; identical per-token cost across
    streams so zlib measures structural redundancy, not name-length."""
    unique = sorted(set(stream))
    if len(unique) > _MAX_UNIQUE:
        raise ValueError(
            f"compression_delta_v0 supports up to {_MAX_UNIQUE} unique tokens; "
            f"stream has {len(unique)}"
        )
    sym = {tok: i for i, tok in enumerate(unique)}
    buf = bytearray(len(stream) * _SYMBOL_BYTES)
    for i, tok in enumerate(stream):
        v = sym[tok]
        buf[i * 2] = (v >> 8) & 0xFF
        buf[i * 2 + 1] = v & 0xFF
    return bytes(buf)


def _zlib_bits(payload: bytes) -> int:
    compressor = zlib.compressobj(_ZLIB_LEVEL, zlib.DEFLATED, _ZLIB_WBITS)
    out = compressor.compress(payload) + compressor.flush(zlib.Z_FINISH)
    return len(out) * 8


def compression_delta_v0(stream: list[str], mapping: dict[str, str]) -> CompressionResult:
    """Score `mapping` against `stream` via zlib compression delta.

    Pipeline (frozen for harness v0):
      1. Encode the raw stream with a 2-byte symbol-id coder + zlib L9.
      2. Apply `mapping` to the stream; encode the mapped stream the same way.
      3. score = baseline_bits - mapped_bits.
    """
    if not stream:
        raise ValueError("compression_delta_v0 requires a non-empty stream")

    baseline_payload = _encode_to_bytes(stream)
    mapped_stream = apply_mapping(stream, mapping)
    mapped_payload = _encode_to_bytes(mapped_stream)

    baseline_bits = _zlib_bits(baseline_payload)
    mapped_bits = _zlib_bits(mapped_payload)

    n = len(stream)
    return CompressionResult(
        score=float(baseline_bits - mapped_bits),
        bits_per_sign_baseline=baseline_bits / n,
        bits_per_sign_mapped=mapped_bits / n,
        baseline_bits=baseline_bits,
        mapped_bits=mapped_bits,
        stream_length=n,
    )


METRICS = {
    "compression_delta_v0": compression_delta_v0,
}
