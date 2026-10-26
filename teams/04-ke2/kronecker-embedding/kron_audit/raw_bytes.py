"""True bytes of every token ID, via per-family strategies.

Shared rules run first, in this order, for every family:
  unassigned     ID with no token                       -> b""
  special        tokenizer special token                -> literal piece (same as the repo)
  byte_fallback  piece "<0xNN>"                         -> the single byte NN
  added_literal  added token outside the model vocab    -> its literal UTF-8 text
Everything else goes to RAW_STRATEGIES[family](piece, token_id, ctx). A
strategy returns None when the piece is not in its encoding (e.g. a
literal-only token stored in a byte-level vocab); that piece then falls
back to its literal UTF-8 text with kind "added_literal".

To support a new tokenizer family: register a strategy here and a detector
in sources.FAMILY_DETECTORS.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from .bytes_util import unicode_to_byte
from .sources import LoadedTokenizer

BYTE_FALLBACK_RE = re.compile(r"^<0x([0-9A-Fa-f]{2})>$")


@dataclass
class VocabView:
    id_to_piece: dict[int, str]
    special_ids: set[int]
    added: dict[int, str]       # id -> content of added tokens
    model_ids: set[int]         # ids that the model (BPE/Unigram/WordPiece) itself knows
    V: int


def vocab_view(lt: LoadedTokenizer) -> VocabView:
    tok = lt.tok
    vocab = tok.get_vocab()
    id_to_piece = {i: p for p, i in vocab.items()}
    special = set(getattr(tok, "all_special_ids", []) or [])
    if lt.backend is not None:
        model_vocab = (lt.backend.get("model") or {}).get("vocab")
        if isinstance(model_vocab, dict):
            model_ids = set(model_vocab.values())
        elif isinstance(model_vocab, list):           # Unigram: [[piece, score], ...]
            model_ids = set(range(len(model_vocab)))
        else:
            model_ids = set(id_to_piece)
        added = {a["id"]: a["content"] for a in lt.backend.get("added_tokens", [])}
    else:                                              # slow tokenizer, no tokenizer.json
        added = {i: t.content for i, t in getattr(tok, "added_tokens_decoder", {}).items()}
        model_ids = set(id_to_piece) - set(added)
    return VocabView(id_to_piece, special, added, model_ids, max(vocab.values()) + 1)


# ---- strategies --------------------------------------------------------------

Strategy = Callable[[str, int, "StrategyContext"], "bytes | None"]


@dataclass
class StrategyContext:
    lt: LoadedTokenizer
    sp_marker: str = "▁"


def _bbpe(piece: str, tid: int, ctx: StrategyContext) -> bytes | None:
    table = unicode_to_byte()
    if all(c in table for c in piece):
        return bytes(table[c] for c in piece)
    return None  # not byte-level encoded: only literal matching can produce it


def _sentencepiece(piece: str, tid: int, ctx: StrategyContext) -> bytes | None:
    return piece.replace(ctx.sp_marker, " ").encode("utf-8")


def _wordpiece(piece: str, tid: int, ctx: StrategyContext) -> bytes | None:
    # WordPiece drops whitespace; "##" marks a word continuation.
    return (piece[2:] if piece.startswith("##") else piece).encode("utf-8")


def _decode(piece: str, tid: int, ctx: StrategyContext) -> bytes | None:
    # Unknown family: the best available surface form is the decoder's output.
    from kronecker_embeddings import token_id_to_bytes
    return token_id_to_bytes(ctx.lt.tok, tid)


RAW_STRATEGIES: dict[str, Strategy] = {
    "bbpe": _bbpe,
    "sentencepiece": _sentencepiece,
    "wordpiece": _wordpiece,
    "decode": _decode,
}


def register_strategy(family: str, fn: Strategy) -> None:
    RAW_STRATEGIES[family] = fn


def _sp_marker(lt: LoadedTokenizer) -> str:
    """The SentencePiece space marker, read from a Metaspace component if present."""
    from .sources import _walk
    for part in ("decoder", "pre_tokenizer"):
        for d in _walk((lt.backend or {}).get(part)):
            if d.get("type") == "Metaspace" and d.get("replacement"):
                return d["replacement"]
    return "▁"


def raw_bytes(lt: LoadedTokenizer) -> tuple[list[bytes], list[str]]:
    """True (untruncated) bytes and the rule used, for every ID 0..V-1."""
    vv = vocab_view(lt)
    strategy = RAW_STRATEGIES[lt.family]
    ctx = StrategyContext(lt, _sp_marker(lt) if lt.family == "sentencepiece" else "▁")
    rows: list[bytes] = []
    kinds: list[str] = []
    for i in range(vv.V):
        piece = vv.id_to_piece.get(i)
        if piece is None:
            rows.append(b""); kinds.append("unassigned"); continue
        if i in vv.special_ids:
            rows.append(piece.encode("utf-8")); kinds.append("special"); continue
        m = BYTE_FALLBACK_RE.match(piece)
        if m:
            rows.append(bytes([int(m.group(1), 16)])); kinds.append("byte_fallback"); continue
        if i in vv.added and i not in vv.model_ids:
            rows.append(vv.added[i].encode("utf-8")); kinds.append("added_literal"); continue
        b = strategy(piece, i, ctx)
        if b is None:
            rows.append(piece.encode("utf-8")); kinds.append("added_literal")
        else:
            rows.append(b); kinds.append(f"model_{lt.family}")
    return rows, kinds
