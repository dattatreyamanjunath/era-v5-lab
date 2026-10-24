"""Shared settings and helpers for the P=32 byte-table audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")  # CPU only
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np

P = 32            # pos_dim: bytes kept per token
CHAR_DIM = 256    # byte alphabet
D = CHAR_DIM * P  # codec width = 8192
EPS = 1e-6        # z-norm stabilizer used by kronecker_codec

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ARTIFACTS = ROOT / "artifacts"  # gitignored: binary tables

# The six tokenizers of paper Table 3. Llama and Gemma use ungated mirrors
# of the official repos (same tokenizer files).
TOKENIZERS = {
    "gpt2":        ("openai-community/gpt2",         "bbpe"),
    "llama-3.2":   ("unsloth/Llama-3.2-1B",          "bbpe"),
    "qwen3":       ("Qwen/Qwen3-32B",                "bbpe"),
    "gemma-3":     ("unsloth/gemma-3-1b-pt",         "sentencepiece"),
    "deepseek-v3": ("deepseek-ai/DeepSeek-V3-Base",  "bbpe"),
    "gpt-oss":     ("openai/gpt-oss-120b",           "bbpe"),
}


def load_tokenizer(name: str):
    from transformers import AutoTokenizer
    repo, _ = TOKENIZERS[name]
    return AutoTokenizer.from_pretrained(repo)


def tokenizer_revision(name: str) -> dict:
    """HF snapshot commit and tokenizer.json SHA-256 from the local cache."""
    from huggingface_hub import try_to_load_from_cache
    repo, _ = TOKENIZERS[name]
    path = try_to_load_from_cache(repo, "tokenizer.json")
    if not isinstance(path, str):
        return {"repo": repo, "snapshot": None, "tokenizer_json_sha256": None}
    snapshot = Path(path).parent.name
    return {"repo": repo, "snapshot": snapshot,
            "tokenizer_json_sha256": sha256_file(path)}


def bytes_to_unicode() -> dict[int, str]:
    """GPT-2 byte -> printable char map used by every byte-level BPE vocab."""
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


UNICODE_TO_BYTE = {c: b for b, c in bytes_to_unicode().items()}


def boundary_truncate(raw: bytes, max_bytes: int = P) -> bytes:
    """Cut to max_bytes, backing off while the cut would split a UTF-8 sequence.

    A cut at position k splits a sequence iff raw[k] is a continuation byte
    (0b10xxxxxx). Unlike utf8_safe_truncate this works on any byte string,
    including partial UTF-8 tokens; on valid UTF-8 the two agree.
    """
    if len(raw) <= max_bytes:
        return raw
    end = max_bytes
    while end > max_bytes - 3 and end > 0 and (raw[end] & 0xC0) == 0x80:
        end -= 1
    return raw[:end]


def pack(rows: list[bytes], pos_dim: int = P) -> tuple[np.ndarray, np.ndarray]:
    """List of already-truncated byte strings -> (uint8 [V,P], int16 [V])."""
    V = len(rows)
    bb = np.zeros((V, pos_dim), dtype=np.uint8)
    lb = np.zeros((V,), dtype=np.int16)
    for i, r in enumerate(rows):
        assert len(r) <= pos_dim
        if r:
            bb[i, : len(r)] = np.frombuffer(r, dtype=np.uint8)
        lb[i] = len(r)
    return bb, lb


def table_sha256(bb: np.ndarray, lb: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(f"{bb.shape[0]}x{bb.shape[1]}".encode())
    h.update(np.ascontiguousarray(bb, dtype=np.uint8).tobytes())
    h.update(np.ascontiguousarray(lb, dtype="<i2").tobytes())
    return h.hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def row_key(bb: np.ndarray, lb: np.ndarray, i: int) -> bytes:
    return bb[i, : int(lb[i])].tobytes()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")
