"""Numerical checks for Lemma 1, Lemma 2 and Theorem 1 (see proof.md).

Every check runs on every row of a byte table, through the repo's own
`kronecker_codec` (the function both KroneckerEmbedding modes call).
"""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict

import numpy as np
import torch

from common import CHAR_DIM, D, EPS, P, row_key

CHUNK = 4096


def _codec(bb: np.ndarray, lb: np.ndarray, z: bool) -> torch.Tensor:
    from kronecker_embeddings import kronecker_codec
    return kronecker_codec(torch.from_numpy(bb), torch.from_numpy(lb.astype(np.int64)),
                           char_dim=CHAR_DIM, pos_dim=P, z_normalize=z)


def closed_form(L: int) -> tuple[float, float]:
    """Lemma 2: z-normalized value on the support and off it, for length L >= 1."""
    mu = math.sqrt(L) / D
    sigma = math.sqrt((1.0 - L / D) / (D - 1))
    return (1.0 / math.sqrt(L) - mu) / (sigma + EPS), -mu / (sigma + EPS)


def run_checks(bb: np.ndarray, lb: np.ndarray, groups) -> dict:
    V = bb.shape[0]
    pos = torch.arange(P)

    # Lemma 1 counters
    l1_rows_ok = 0
    l1_max_norm_err = 0.0
    l1_empty_rows_zero = 0
    # Lemma 2 counters
    l2_support_ok = 0
    l2_by_L = defaultdict(lambda: {"tokens": 0, "max_abs_err": 0.0, "max_rel_err": 0.0})
    l2_empty_zero = 0
    # Theorem 1
    row_hash: list[bytes] = []
    digest = hashlib.sha256()

    for s in range(0, V, CHUNK):
        b = bb[s : s + CHUNK]
        l = lb[s : s + CHUNK]
        n = b.shape[0]
        L = torch.from_numpy(l.astype(np.int64))
        bt = torch.from_numpy(b.astype(np.int64))
        valid = pos.unsqueeze(0) < L.unsqueeze(1)                     # (n, P)

        # ---- Lemma 1: pre-norm codec is invertible and has unit norm ----
        X = _codec(b, l, z=False)                                     # (n, D)
        Xr = X.view(n, CHAR_DIM, P)                                   # [byte, pos]
        nz = Xr != 0
        count_ok = (nz.sum(1) == valid.long()).all(1)                 # one byte per used slot
        byte_ok = ((Xr.argmax(1) == bt) | ~valid).all(1)              # recovered bytes match
        scale = torch.rsqrt(L.clamp_min(1).float())
        val_ok = ((Xr.amax(1) == scale.unsqueeze(1)) | ~valid).all(1)  # each value = 1/sqrt(L)
        l1_rows_ok += int((count_ok & byte_ok & val_ok).sum())
        norms = X.double().pow(2).sum(1).sqrt()
        has = L > 0
        if has.any():
            l1_max_norm_err = max(l1_max_norm_err, float((norms[has] - 1).abs().max()))
        l1_empty_rows_zero += int(((~has) & (X.abs().sum(1) == 0)).sum())

        # ---- Lemma 2: z-norm matches the closed form; support = {z > 0} ----
        Z = _codec(b, l, z=True)
        support = nz.view(n, D)
        l2_support_ok += int(((Z > 0) == support).all(1)[has].sum())
        l2_empty_zero += int(((~has) & (Z.abs().sum(1) == 0)).sum())
        for Lv in torch.unique(L[has]).tolist():
            m = L == Lv
            on, off = closed_form(Lv)
            pred = torch.where(support[m], torch.tensor(on, dtype=torch.float64),
                               torch.tensor(off, dtype=torch.float64))
            diff = (Z[m].double() - pred).abs()
            rec = l2_by_L[Lv]
            rec["tokens"] += int(m.sum())
            rec["max_abs_err"] = max(rec["max_abs_err"], float(diff.max()))
            rec["max_rel_err"] = max(rec["max_rel_err"], float((diff / pred.abs()).max()))

        # ---- Theorem 1: hash every codec row ----
        Zn = Z.numpy()
        digest.update(Zn.tobytes())
        for i in range(n):
            row_hash.append(hashlib.sha256(Zn[i].tobytes()).digest())

    # Theorem 1: byte row <-> codec row must be a bijection.
    key_to_hash = defaultdict(set)
    hash_to_key = defaultdict(set)
    for i in range(V):
        k = row_key(bb, lb, i)
        key_to_hash[k].add(row_hash[i])
        hash_to_key[row_hash[i]].add(k)
    n_empty = int((lb == 0).sum())

    l2_table = []
    for Lv in sorted(l2_by_L):
        on, off = closed_form(Lv)
        l2_table.append({"L": Lv, "tokens": l2_by_L[Lv]["tokens"], "z_on": on, "z_off": off,
                         "max_abs_err": l2_by_L[Lv]["max_abs_err"],
                         "max_rel_err": l2_by_L[Lv]["max_rel_err"]})

    res = {
        "rows": V,
        "empty_rows": n_empty,
        "lemma1": {
            "rows_roundtrip_ok": l1_rows_ok,
            "max_abs_norm_minus_1": l1_max_norm_err,
            "empty_rows_map_to_zero": l1_empty_rows_zero,
            "pass": l1_rows_ok == V and l1_empty_rows_zero == n_empty and l1_max_norm_err < 1e-6,
        },
        "lemma2": {
            "rows_support_recovered": l2_support_ok,
            "nonempty_rows": V - n_empty,
            "empty_rows_map_to_zero": l2_empty_zero,
            "max_abs_err_vs_closed_form": max((r["max_abs_err"] for r in l2_table), default=0.0),
            "max_rel_err_vs_closed_form": max((r["max_rel_err"] for r in l2_table), default=0.0),
            "by_length": l2_table,
        },
        "theorem1": {
            "distinct_byte_rows": len(key_to_hash),
            "distinct_codec_rows": len(hash_to_key),
            "byte_rows_with_more_than_one_codec_row": sum(len(v) > 1 for v in key_to_hash.values()),
            "codec_rows_shared_by_distinct_byte_rows": sum(len(v) > 1 for v in hash_to_key.values()),
            "collision_groups_with_single_codec_row": sum(
                len({row_hash[i] for i in ids}) == 1 for _, ids in groups),
            "collision_groups": len(groups),
            "codec_table_sha256": digest.hexdigest(),
        },
    }
    l2 = res["lemma2"]
    l2["pass"] = (l2["rows_support_recovered"] == V - n_empty and l2["empty_rows_map_to_zero"] == n_empty
                  and l2["max_rel_err_vs_closed_form"] < 1e-5)
    t1 = res["theorem1"]
    t1["pass"] = (t1["distinct_byte_rows"] == t1["distinct_codec_rows"]
                  and t1["byte_rows_with_more_than_one_codec_row"] == 0
                  and t1["codec_rows_shared_by_distinct_byte_rows"] == 0
                  and t1["collision_groups_with_single_codec_row"] == len(groups))
    res["_row_hash"] = row_hash
    return res


def mode_check(bb: np.ndarray, lb: np.ndarray, groups, row_hash, n_random: int = 4096) -> dict:
    """dynamic vs cached KroneckerEmbedding, on every collision member plus random IDs.

    Also checks that a single full-batch codec call gives the same rows as the
    chunked calls used for hashing (batch invariance).
    """
    from kronecker_embeddings import KroneckerEmbedding
    rng = np.random.default_rng(0)
    members = sorted({i for _, ids in groups for i in ids})
    if len(members) > 8192:
        members = sorted(rng.choice(members, 8192, replace=False).tolist())
    rand = rng.choice(bb.shape[0], min(n_random, bb.shape[0]), replace=False).tolist()
    ids = sorted(set(members) | set(rand))
    sb = torch.from_numpy(bb[ids])
    sl = torch.from_numpy(lb[ids])
    torch.manual_seed(0)
    dyn = KroneckerEmbedding(len(ids), 16, byte_buffer=sb, length_buffer=sl, mode="dynamic")
    cac = KroneckerEmbedding(len(ids), 16, byte_buffer=sb, length_buffer=sl, mode="cached")
    cac.load_state_dict(dyn.state_dict())
    x = torch.arange(len(ids)).view(1, -1)
    with torch.no_grad():
        cd, cc = dyn._codec_lookup(x), cac._codec_lookup(x)
        ed, ec = dyn(x), cac(x)
    codec = cd.view(len(ids), -1).numpy()
    batch_inv = all(hashlib.sha256(codec[k].tobytes()).digest() == row_hash[i] for k, i in enumerate(ids))
    return {
        "ids_tested": len(ids),
        "collision_members_tested": len(members),
        "codec_dynamic_equals_cached_bitwise": bool(torch.equal(cd, cc)),
        "embedding_dynamic_equals_cached_bitwise": bool(torch.equal(ed, ec)),
        "full_batch_equals_chunked_rows": bool(batch_inv),
        "pass": bool(torch.equal(cd, cc) and torch.equal(ed, ec) and batch_inv),
    }
