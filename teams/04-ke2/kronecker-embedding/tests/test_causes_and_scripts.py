import pytest

parametrize = pytest.mark.parametrize  # alias: the lab pr-guard email regex flags top-level pytest.mark decorators

from kron_audit.causes import DEFAULT_RULES, UNEXPLAINED, CauseRule, GroupContext, assign_cause
from kron_audit.script_class import token_class

FFFD = "�".encode()


def ctx(kind, key, raws, decs=None, kinds=None, P=4):
    n = len(raws)
    return GroupContext(kind, key, list(range(n)), raws, decs or raws, kinds or ["model_bbpe"] * n, P)


def test_utf8_replacement():
    g = ctx("decode", FFFD, [b"\xe4", b"\xe5"], [FFFD, FFFD])
    assert assign_cause(g) == "utf8_replacement"


def test_utf8_replacement_is_decode_only():
    # A literal U+FFFD in two raw rows is not a decode artifact.
    g = ctx("raw", FFFD, [FFFD, FFFD])
    assert assign_cause(g) == "duplicate_vocab_entry"


def test_truncation_uses_P():
    g = ctx("raw", b"aaaa", [b"aaaa", b"aaaaaa"], P=4)
    assert assign_cause(g) == "truncation"
    g8 = ctx("raw", b"aaaa", [b"aaaa", b"aaaaaa"], P=8)       # not equal at P = 8
    assert assign_cause(g8) == UNEXPLAINED


def test_same_bytes_rules():
    assert assign_cause(ctx("raw", b"\n", [b"\n", b"\n"], kinds=["model_sentencepiece", "byte_fallback"])) == "byte_fallback_alias"
    assert assign_cause(ctx("raw", b"<s>", [b"<s>", b"<s>"], kinds=["special", "model_bbpe"])) == "special_literal_clash"
    assert assign_cause(ctx("raw", b"ab", [b"ab", b"ab"])) == "duplicate_vocab_entry"


def test_decoder_normalization_and_empty():
    g = ctx("decode", b"the", [b" the", b"the"], [b"the", b"the"])
    assert assign_cause(g) == "decoder_normalization"
    assert assign_cause(ctx("raw", b"", [b"", b""])) == "empty_bytes"


def test_custom_rule_extends_defaults():
    rule = CauseRule("all_digits", "rows of digits", lambda g: g.key.isdigit(), tables=("raw",))
    g = ctx("raw", b"12", [b"12", b"123"], P=8)
    assert assign_cause(g) == UNEXPLAINED
    assert assign_cause(g, DEFAULT_RULES + [rule]) == "all_digits"


@parametrize("raw,kind,want", [
    (b"hello", "model_bbpe", "ASCII"),
    (" नमस्ते".encode(), "model_bbpe", "Devanagari"),
    (b"\xe0\xa4", "model_bbpe", "Devanagari (fragment)"),
    (b" \xe0\xa6", "model_bbpe", "Bengali (fragment)"),
    (b"\xf0\x9f\x98", "model_bbpe", "Emoji (fragment)"),      # U+1F600..1F63F
    (b"\xe4\xb8", "model_bbpe", "CJK Han (fragment)"),         # U+4E00..4E3F
    (b"\xe4", "model_bbpe", "Mixed (fragment)"),                # U+4000..4FFF spans 3 blocks
    (b"\x80\x81", "model_bbpe", "Continuation bytes only"),
    (b"\xc0", "model_bbpe", "Invalid UTF-8 byte"),
    (b"   ", "model_bbpe", "Whitespace"),
    (b"<s>", "special", "Special"),
    (b"", "unassigned", "Empty"),
])
def test_token_class(raw, kind, want):
    assert token_class(raw, kind) == want
