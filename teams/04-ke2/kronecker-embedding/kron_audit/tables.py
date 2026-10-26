"""Decode table and raw byte table for any P.

decode: exactly the repo's buffer, kronecker_embeddings.build_byte_buffer(tok, pos_dim=P)
raw:    true bytes per ID (raw_bytes.py), cut on a character boundary at P
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .bytes_util import boundary_truncate, pack, table_sha256, utf8_valid
from .raw_bytes import raw_bytes
from .sources import LoadedTokenizer


@dataclass
class ByteTable:
    """A [V, P] byte buffer plus lengths: the exact input of the Kronecker codec."""
    name: str                 # tokenizer name
    kind: str                 # "decode" | "raw"
    data: np.ndarray          # uint8 [V, P], zero padded
    lengths: np.ndarray       # int16 [V]
    full: list[bytes] | None = None  # untruncated bytes, when known

    @property
    def V(self) -> int:
        return int(self.data.shape[0])

    @property
    def P(self) -> int:
        return int(self.data.shape[1])

    def row(self, i: int) -> bytes:
        return self.data[i, : int(self.lengths[i])].tobytes()

    def sha256(self) -> str:
        return table_sha256(self.data, self.lengths)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, bytes=self.data, lengths=self.lengths)

    @classmethod
    def load(cls, path: Path, name: str, kind: str) -> "ByteTable":
        z = np.load(path)
        return cls(name, kind, z["bytes"], z["lengths"])


@dataclass
class TablePair:
    """Both tables for one tokenizer, plus per-ID metadata shared by later stages."""
    decode: ByteTable
    raw: ByteTable
    kinds: list[str]          # raw-byte rule per ID
    pieces: list[str]         # convert_ids_to_tokens per ID
    info: dict = field(default_factory=dict)

    @property
    def V(self) -> int:
        return self.raw.V

    @property
    def P(self) -> int:
        return self.raw.P

    def table(self, kind: str) -> ByteTable:
        return self.decode if kind == "decode" else self.raw


def build_decode_table(lt: LoadedTokenizer, P: int) -> tuple[ByteTable, bool]:
    """The repo's buffer, plus a check that our repacking of decode bytes reproduces it."""
    from kronecker_embeddings import build_byte_buffer, token_id_to_bytes, utf8_safe_truncate
    bb, lb = build_byte_buffer(lt.tok, pos_dim=P)
    data, lengths = bb.numpy(), lb.numpy()
    special = set(getattr(lt.tok, "all_special_ids", []) or [])
    full = []
    for i in range(data.shape[0]):
        try:
            full.append(token_id_to_bytes(lt.tok, i, special))
        except Exception:
            full.append(b"")
    my_data, my_len = pack([utf8_safe_truncate(r, P) for r in full], P)
    same = bool(np.array_equal(my_data, data) and np.array_equal(my_len, lengths))
    return ByteTable(lt.name, "decode", data, lengths, full), same


def build_raw_table(lt: LoadedTokenizer, P: int) -> tuple[ByteTable, list[str]]:
    rows, kinds = raw_bytes(lt)
    data, lengths = pack([boundary_truncate(r, P) for r in rows], P)
    return ByteTable(lt.name, "raw", data, lengths, rows), kinds


def build_tables(lt: LoadedTokenizer, P: int) -> TablePair:
    from kronecker_embeddings import utf8_safe_truncate
    dec, repo_match = build_decode_table(lt, P)
    raw, kinds = build_raw_table(lt, P)
    if dec.V != raw.V:
        raise RuntimeError(f"{lt.name}: decode V={dec.V} != raw V={raw.V}")
    pieces = [p if p is not None else "" for p in lt.tok.convert_ids_to_tokens(list(range(raw.V)))]

    # Our boundary cut must equal the repo's utf8_safe_truncate on valid UTF-8.
    n_valid_long = n_agree = 0
    for r in raw.full:
        if len(r) > P and utf8_valid(r):
            n_valid_long += 1
            n_agree += boundary_truncate(r, P) == utf8_safe_truncate(r, P)

    info = {
        "V": raw.V,
        "P": P,
        "family": lt.family,
        "decode_table_sha256": dec.sha256(),
        "raw_table_sha256": raw.sha256(),
        "decode_repacked_equals_repo_buffer": repo_match,
        "truncation_rule_check": {"valid_utf8_tokens_over_P": n_valid_long,
                                  "boundary_equals_utf8_safe": n_agree},
        "raw_kind_counts": {k: kinds.count(k) for k in sorted(set(kinds))},
        "rows_where_decode_differs_from_raw": int(sum(a != b for a, b in zip(dec.full, raw.full))),
        "raw_len_over_P": int(sum(len(r) > P for r in raw.full)),
        "decode_len_over_P": int(sum(len(r) > P for r in dec.full)),
        "raw_invalid_utf8": int(sum(not utf8_valid(r) for r in raw.full)),
    }
    return TablePair(dec, raw, kinds, pieces, info)
