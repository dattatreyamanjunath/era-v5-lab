"""Decode table and raw byte table for P=32.

decode table: exactly what the kronecker-embeddings repo builds
              (`build_byte_buffer`, which calls `tokenizer.decode([id])`).
raw table:    each token's true bytes, read from the vocab piece.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

import numpy as np

from common import (ARTIFACTS, P, TOKENIZERS, UNICODE_TO_BYTE, boundary_truncate,
                    pack, table_sha256)

BYTE_FALLBACK_RE = re.compile(r"^<0x([0-9A-Fa-f]{2})>$")


@dataclass
class Tables:
    name: str
    V: int
    kinds: list[str]            # how each raw row was derived
    pieces: list[str]           # convert_ids_to_tokens
    dec_full: list[bytes]       # decode bytes before truncation
    raw_full: list[bytes]       # true bytes before truncation
    dec_bb: np.ndarray
    dec_lb: np.ndarray
    raw_bb: np.ndarray
    raw_lb: np.ndarray
    info: dict = field(default_factory=dict)


def decode_table(tok, pos_dim: int = P):
    """The repo's own byte buffer: decode every token ID once."""
    from kronecker_embeddings import build_byte_buffer
    bb, lb = build_byte_buffer(tok, pos_dim=pos_dim)
    return bb.numpy(), lb.numpy()


def decode_full(tok) -> list[bytes]:
    """Untruncated decode bytes per ID, via the repo's token_id_to_bytes."""
    from kronecker_embeddings import token_id_to_bytes
    V = max(tok.get_vocab().values()) + 1
    special = set(getattr(tok, "all_special_ids", []) or [])
    out = []
    for i in range(V):
        try:
            out.append(token_id_to_bytes(tok, i, special))
        except Exception:
            out.append(b"")
    return out


def raw_full(tok, family: str) -> tuple[list[bytes], list[str]]:
    """True bytes per ID, and the rule used for each.

    special       -> literal piece (same as the repo)
    byte_fallback -> <0xNN> is the single byte NN
    added_literal -> added token outside the model vocab: literal content
    model_bbpe    -> invert the GPT-2 bytes_to_unicode map
    model_sp      -> SentencePiece: U+2581 -> space
    unassigned    -> ID with no token
    """
    j = json.loads(tok.backend_tokenizer.to_str())
    model_vocab = j["model"]["vocab"]
    model_ids = set(model_vocab.values())
    added = {a["id"]: a["content"] for a in j["added_tokens"]}
    V = max(tok.get_vocab().values()) + 1
    special = set(getattr(tok, "all_special_ids", []) or [])
    id_to_piece = {i: p for p, i in tok.get_vocab().items()}

    rows, kinds = [], []
    for i in range(V):
        piece = id_to_piece.get(i)
        if piece is None:
            rows.append(b""); kinds.append("unassigned"); continue
        if i in special:
            rows.append(piece.encode("utf-8")); kinds.append("special"); continue
        m = BYTE_FALLBACK_RE.match(piece)
        if m:
            rows.append(bytes([int(m.group(1), 16)])); kinds.append("byte_fallback"); continue
        if i in added and i not in model_ids:
            rows.append(added[i].encode("utf-8")); kinds.append("added_literal"); continue
        if family == "bbpe":
            if all(c in UNICODE_TO_BYTE for c in piece):
                rows.append(bytes(UNICODE_TO_BYTE[c] for c in piece)); kinds.append("model_bbpe")
            else:
                # Not byte-level encoded (e.g. DeepSeek '<｜begin▁of▁sentence｜>' in the
                # model vocab): BPE can never emit it, only literal matching can.
                rows.append(piece.encode("utf-8")); kinds.append("added_literal")
        else:
            rows.append(piece.replace("▁", " ").encode("utf-8")); kinds.append("model_sp")
    return rows, kinds


def build(name: str, tok=None, save: bool = True) -> Tables:
    from kronecker_embeddings import utf8_safe_truncate
    if tok is None:
        from common import load_tokenizer
        tok = load_tokenizer(name)
    family = TOKENIZERS[name][1]
    V = max(tok.get_vocab().values()) + 1

    dec_bb, dec_lb = decode_table(tok)
    dfull = decode_full(tok)
    rfull, kinds = raw_full(tok, family)
    raw_bb, raw_lb = pack([boundary_truncate(r) for r in rfull])
    pieces = tok.convert_ids_to_tokens(list(range(V)))

    # Our packing of the decode bytes must reproduce the repo's buffer exactly.
    my_bb, my_lb = pack([utf8_safe_truncate(r, P) for r in dfull])
    repo_match = bool(np.array_equal(my_bb, dec_bb) and np.array_equal(my_lb, dec_lb))

    # boundary_truncate == utf8_safe_truncate on every valid-UTF-8 raw token.
    n_valid_long, n_agree = 0, 0
    for r in rfull:
        if len(r) > P:
            try:
                r.decode("utf-8")
            except UnicodeDecodeError:
                continue
            n_valid_long += 1
            n_agree += boundary_truncate(r) == utf8_safe_truncate(r, P)

    t = Tables(name, V, kinds, [p if p is not None else "" for p in pieces],
               dfull, rfull, dec_bb, dec_lb, raw_bb, raw_lb)
    t.info = {
        "V": V,
        "family": family,
        "decode_table_sha256": table_sha256(dec_bb, dec_lb),
        "raw_table_sha256": table_sha256(raw_bb, raw_lb),
        "decode_repacked_equals_repo_buffer": repo_match,
        "truncation_rule_check": {"valid_utf8_tokens_over_P": n_valid_long,
                                  "boundary_equals_utf8_safe": n_agree},
        "raw_kind_counts": {k: kinds.count(k) for k in sorted(set(kinds))},
        "rows_where_decode_differs_from_raw": int(sum(a != b for a, b in zip(dfull, rfull))),
        "raw_len_over_P": int(sum(len(r) > P for r in rfull)),
        "decode_len_over_P": int(sum(len(r) > P for r in dfull)),
        "raw_invalid_utf8": int(sum(not _valid(r) for r in rfull)),
    }
    if save:
        out = ARTIFACTS / name
        out.mkdir(parents=True, exist_ok=True)
        np.savez(out / "decode_P32.npz", bytes=dec_bb, lengths=dec_lb)
        np.savez(out / "raw_P32.npz", bytes=raw_bb, lengths=raw_lb)
    return t


def _valid(b: bytes) -> bool:
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
