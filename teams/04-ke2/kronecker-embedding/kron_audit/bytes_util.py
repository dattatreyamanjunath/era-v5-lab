"""Pure byte helpers. P is always an argument."""

from __future__ import annotations

import hashlib
from functools import lru_cache

import numpy as np


def utf8_valid(b: bytes) -> bool:
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def boundary_truncate(raw: bytes, max_bytes: int) -> bytes:
    """Cut to max_bytes, backing off while the cut would split a UTF-8 sequence.

    A cut at position k splits a sequence iff raw[k] is a continuation byte
    (0b10xxxxxx); a sequence has at most 3 continuation bytes, so at most 3
    back-offs. Works on any byte string, including partial UTF-8 tokens. On
    valid UTF-8 it equals kronecker_embeddings.utf8_safe_truncate (tested).
    """
    if len(raw) <= max_bytes:
        return raw
    end = max_bytes
    while end > max_bytes - 3 and end > 0 and (raw[end] & 0xC0) == 0x80:
        end -= 1
    return raw[:end]


@lru_cache(maxsize=1)
def bytes_to_unicode() -> dict[int, str]:
    """GPT-2 byte -> printable char map used by byte-level BPE vocabularies."""
    bs = (list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1))
          + list(range(ord("®"), ord("ÿ") + 1)))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return {b: chr(c) for b, c in zip(bs, cs)}


@lru_cache(maxsize=1)
def unicode_to_byte() -> dict[str, int]:
    return {c: b for b, c in bytes_to_unicode().items()}


def pack(rows: list[bytes], pos_dim: int) -> tuple[np.ndarray, np.ndarray]:
    """Already-truncated byte strings -> (uint8 [V, P] zero-padded, int16 [V])."""
    V = len(rows)
    data = np.zeros((V, pos_dim), dtype=np.uint8)
    lengths = np.zeros((V,), dtype=np.int16)
    for i, r in enumerate(rows):
        n = len(r)
        if n > pos_dim:
            raise ValueError(f"row {i} has {n} bytes > pos_dim {pos_dim}")
        if n:
            data[i, :n] = np.frombuffer(r, dtype=np.uint8)
        lengths[i] = n
    return data, lengths


def table_sha256(data: np.ndarray, lengths: np.ndarray) -> str:
    """SHA-256 over "VxP", the uint8 rows and the little-endian int16 lengths."""
    h = hashlib.sha256()
    h.update(f"{data.shape[0]}x{data.shape[1]}".encode())
    h.update(np.ascontiguousarray(data, dtype=np.uint8).tobytes())
    h.update(np.ascontiguousarray(lengths, dtype="<i2").tobytes())
    return h.hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def preview(b: bytes, limit: int = 40) -> str:
    s = b.decode("utf-8", errors="backslashreplace")
    return s if len(s) <= limit else s[:limit] + "…"
