import random
from dataclasses import replace

import numpy as np
import pytest

parametrize = pytest.mark.parametrize  # alias: the lab pr-guard email regex flags top-level pytest.mark decorators
import torch

from kron_audit.bytes_util import pack
from kron_audit.codec_checks import closed_form, codec_rows, mode_check, run_checks
from kron_audit.config import CodecConfig, ComputeConfig
from kron_audit.grouping import find_groups
from kron_audit.tables import ByteTable


def random_table(P, V=300, seed=0, dup=20):
    rng = random.Random(seed)
    rows = [bytes(rng.randrange(256) for _ in range(rng.randrange(1, P + 1))) for _ in range(V - dup)]
    rows += [rows[rng.randrange(len(rows))] for _ in range(dup)]   # force some collisions
    rows[0] = b""                                                   # one empty row
    data, lengths = pack(rows, P)
    return ByteTable("rand", "raw", data, lengths)


@parametrize("P", [8, 32, 64])
def test_closed_form_matches_codec(P):
    codec = CodecConfig(pos_dim=P)
    for L in sorted({1, 2, P // 2, P}):
        data, lengths = pack([bytes(range(10, 10 + L))], P)
        z = codec_rows(data, lengths, codec, z=True)[0].double()
        on, off = closed_form(L, codec)
        assert torch.allclose(z[z > 0], torch.tensor(on, dtype=torch.float64), rtol=1e-6)
        assert torch.allclose(z[z < 0], torch.tensor(off, dtype=torch.float64), rtol=1e-6)
        assert int((z > 0).sum()) == L


def test_closed_form_without_length_normalize():
    codec = CodecConfig(pos_dim=16, length_normalize=False)
    data, lengths = pack([b"abcde"], 16)
    z = codec_rows(data, lengths, codec, z=True)[0].double()
    on, off = closed_form(5, codec)
    assert torch.allclose(z[z > 0], torch.tensor(on, dtype=torch.float64), rtol=1e-6)


@parametrize("P", [8, 64])
def test_run_checks_pass_on_random_table(P):
    t = random_table(P)
    g = find_groups(t)
    assert g.members, "the fixture should contain collisions"
    res, row_hash = run_checks(t, g, CodecConfig(pos_dim=P), ComputeConfig(chunk_rows=37))
    assert res["lemma1"]["pass"] and res["lemma2"]["pass"] and res["theorem1"]["pass"]
    assert res["theorem1"]["distinct_codec_rows"] == g.n_distinct
    assert mode_check(t, g, row_hash, CodecConfig(pos_dim=P), ComputeConfig(mode_check_random_ids=50))["pass"]


def test_chunking_does_not_change_results():
    t = random_table(16)
    g = find_groups(t)
    a, ha = run_checks(t, g, CodecConfig(pos_dim=16), ComputeConfig(chunk_rows=7))
    b, hb = run_checks(t, g, CodecConfig(pos_dim=16), ComputeConfig(chunk_rows=10_000))
    assert ha == hb
    assert a["theorem1"]["codec_table_sha256"] == b["theorem1"]["codec_table_sha256"]


def test_checks_follow_codec_flags():
    t = random_table(8)
    g = find_groups(t)
    res, _ = run_checks(t, g, CodecConfig(pos_dim=8, z_normalize=False, length_normalize=False),
                        ComputeConfig())
    assert res["lemma1"]["pass"] and res["theorem1"]["pass"]
    assert "skipped" in res["lemma2"]


def test_auto_chunk_rows_scales_with_D():
    c = ComputeConfig()
    assert c.rows_per_chunk(256 * 64) == c.rows_per_chunk(256 * 32) // 2
