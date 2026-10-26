"""Why a collision group exists: an ordered list of rules, first match wins.

Add a cause by appending a CauseRule (or passing your own list to
analysis.analyse). A group that no rule explains is labelled "unexplained"
and reported, never dropped.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Callable

from .bytes_util import boundary_truncate, utf8_valid

FFFD = "�".encode("utf-8")
UNEXPLAINED = "unexplained"


@dataclass
class GroupContext:
    table_kind: str            # "decode" | "raw"
    key: bytes                 # the shared row
    ids: list[int]
    raw_full: list[bytes]      # true bytes of the members (untruncated)
    dec_full: list[bytes]      # decode bytes of the members (untruncated)
    kinds: list[str]           # raw-byte rule of the members
    P: int

    @cached_property
    def same_true_bytes(self) -> bool:
        return len(set(self.raw_full)) == 1

    @cached_property
    def any_invalid_utf8(self) -> bool:
        return any(not utf8_valid(r) for r in self.raw_full)


@dataclass(frozen=True)
class CauseRule:
    name: str
    description: str
    applies: Callable[[GroupContext], bool]
    tables: tuple[str, ...] = ("decode", "raw")


DEFAULT_RULES: list[CauseRule] = [
    CauseRule("empty_bytes", "the shared row is empty",
              lambda g: len(g.key) == 0),
    CauseRule("utf8_replacement",
              "decode wrote U+FFFD for bytes that are not valid UTF-8 (a piece of a character)",
              lambda g: FFFD in g.key and g.any_invalid_utf8, tables=("decode",)),
    CauseRule("byte_fallback_alias", "a <0xNN> byte-fallback token and a normal token with the same byte",
              lambda g: g.same_true_bytes and "byte_fallback" in g.kinds),
    CauseRule("special_literal_clash", "a special/added literal equals another token's bytes",
              lambda g: g.same_true_bytes and ("special" in g.kinds or "added_literal" in g.kinds)),
    CauseRule("duplicate_vocab_entry", "two IDs with identical true bytes",
              lambda g: g.same_true_bytes),
    CauseRule("truncation", "true bytes differ, but their first <= P bytes (cut on a character boundary) match",
              lambda g: len({boundary_truncate(r, g.P) for r in g.raw_full}) == 1),
    CauseRule("decoder_normalization", "decode changed valid bytes (e.g. dropped a space)",
              lambda g: any(d != r for d, r in zip(g.dec_full, g.raw_full)), tables=("decode",)),
]


def assign_cause(ctx: GroupContext, rules: list[CauseRule] = DEFAULT_RULES) -> str:
    for rule in rules:
        if ctx.table_kind in rule.tables and rule.applies(ctx):
            return rule.name
    return UNEXPLAINED


def cause_names(rules: list[CauseRule] = DEFAULT_RULES) -> list[str]:
    return [r.name for r in rules] + [UNEXPLAINED]
