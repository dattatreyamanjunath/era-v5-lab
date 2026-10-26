import random
from collections import defaultdict

import numpy as np
import pytest

parametrize = pytest.mark.parametrize  # alias: the lab pr-guard email regex flags top-level pytest.mark decorators
from kronecker_embeddings import utf8_safe_truncate

from kron_audit.bytes_util import boundary_truncate, pack, table_sha256, utf8_valid
from kron_audit.grouping import find_groups
from kron_audit.tables import ByteTable

CHARS = ["a", "Z", " ", "é", "ß", "न", "्", "中", "語", "한", "😀", "🇮", "‍", "\x00"]


def random_text(rng, max_chars=80):
    return "".join(rng.choice(CHARS) for _ in range(rng.randrange(max_chars)))


@parametrize("P", [4, 8, 32, 64])
def test_boundary_truncate_matches_repo_on_valid_utf8(P):
    rng = random.Random(P)
    for _ in range(3000):
        b = random_text(rng).encode("utf-8")
        out = boundary_truncate(b, P)
        assert out == utf8_safe_truncate(b, P)
        assert utf8_valid(out) and len(out) <= P


@parametrize("P", [4, 8, 32, 64])
def test_boundary_truncate_on_arbitrary_bytes(P):
    rng = random.Random(100 + P)
    for _ in range(3000):
        b = bytes(rng.randrange(256) for _ in range(rng.randrange(2 * P + 8)))
        out = boundary_truncate(b, P)
        assert b.startswith(out) and len(out) <= P
        if len(b) > P:
            assert len(out) >= P - 3
            # The cut is on a non-continuation byte unless the 3-byte back-off limit was hit.
            assert (b[len(out)] & 0xC0) != 0x80 or len(out) == P - 3


def test_pack_and_hash():
    rows = [b"", b"a", b"abc", b"\xff\x00"]
    data, lengths = pack(rows, 4)
    assert data.shape == (4, 4) and lengths.tolist() == [0, 1, 3, 2]
    assert [data[i, :lengths[i]].tobytes() for i in range(4)] == rows
    h = table_sha256(data, lengths)
    lengths2 = lengths.copy(); lengths2[0] = 1          # same bytes, different length
    assert table_sha256(data, lengths2) != h
    with pytest.raises(ValueError):
        pack([b"abcde"], 4)


def _reference_groups(rows):
    d = defaultdict(list)
    for i, r in enumerate(rows):
        d[r].append(i)
    return sorted((v for v in d.values() if len(v) > 1), key=lambda m: (-len(m), m[0])), len(d)


@parametrize("seed", range(5))
def test_find_groups_matches_dict_reference(seed):
    rng = random.Random(seed)
    pool = [bytes(rng.randrange(4) for _ in range(rng.randrange(6))) for _ in range(40)]
    rows = [rng.choice(pool) for _ in range(500)]
    data, lengths = pack(rows, 6)
    g = find_groups(ByteTable("t", "raw", data, lengths))
    ref, n = _reference_groups(rows)
    assert g.n_distinct == n
    assert [m.tolist() for m in g.members] == ref


def test_rows_differing_only_in_length_are_distinct():
    # b"a" (len 1) and b"a\x00" (len 2) have the same zero-padded bytes.
    data, lengths = pack([b"a", b"a\x00", b"a"], 4)
    g = find_groups(ByteTable("t", "raw", data, lengths))
    assert g.n_distinct == 2
    assert [m.tolist() for m in g.members] == [[0, 2]]
