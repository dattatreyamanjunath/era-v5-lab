"""Numerical checks for Lemma 1, Lemma 2 and Theorem 1 (proof.md), for any codec config.

Rows are streamed in chunks sized from D (ComputeConfig.rows_per_chunk), so
memory stays flat as V or P grows. Each lemma has its own accumulator.
"""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np
import torch

from .config import CodecConfig, ComputeConfig
from .grouping import Groups
from .tables import ByteTable

KRON_DEFAULT_EPS = 1e-6  # KroneckerEmbedding always calls kronecker_codec with its default eps


def codec_rows(data: np.ndarray, lengths: np.ndarray, codec: CodecConfig, z: bool) -> torch.Tensor:
    from kronecker_embeddings import kronecker_codec
    return kronecker_codec(torch.from_numpy(np.ascontiguousarray(data)),
                           torch.from_numpy(lengths.astype(np.int64)),
                           char_dim=codec.char_dim, pos_dim=codec.pos_dim,
                           length_normalize=codec.length_normalize,
                           z_normalize=z and codec.z_normalize, eps=codec.eps)


def support_value(L: int, codec: CodecConfig) -> float:
    """Value of every nonzero pre-norm coordinate (Lemma 1)."""
    return 1.0 / math.sqrt(L) if codec.length_normalize else 1.0


def closed_form(L: int, codec: CodecConfig) -> tuple[float, float]:
    """Lemma 2: z-normalized value on the support and off it, for length L >= 1."""
    D, v = codec.D, support_value(L, codec)
    mu = L * v / D
    sigma = math.sqrt(L * v * v * (1.0 - L / D) / (D - 1))
    return (v - mu) / (sigma + codec.eps), -mu / (sigma + codec.eps)


# ---- accumulators --------------------------------------------------------------

@dataclass
class Lemma1:
    """Pre-norm codec: one nonzero per used position, right byte, right value, known norm."""
    codec: CodecConfig
    rows_ok: int = 0
    empty_zero: int = 0
    max_norm_err: float = 0.0

    def update(self, X: torch.Tensor, bt: torch.Tensor, L: torch.Tensor, valid: torch.Tensor) -> torch.Tensor:
        n, C, P = X.shape[0], self.codec.char_dim, self.codec.pos_dim
        Xr = X.view(n, C, P)
        nz = Xr != 0
        count_ok = (nz.sum(1) == valid.long()).all(1)
        byte_ok = ((Xr.argmax(1) == bt) | ~valid).all(1)
        if self.codec.length_normalize:
            val = torch.rsqrt(L.clamp_min(1).float())
        else:
            val = torch.ones(n)
        val_ok = ((Xr.amax(1) == val.unsqueeze(1)) | ~valid).all(1)
        self.rows_ok += int((count_ok & byte_ok & val_ok).sum())
        has = L > 0
        if has.any():
            want = torch.ones(n, dtype=torch.float64) if self.codec.length_normalize else L.double().sqrt()
            norms = torch.linalg.vector_norm(X, dim=1).double()   # no [n, D] temporary
            err = (norms - want)[has].abs().max()
            self.max_norm_err = max(self.max_norm_err, float(err))
        self.empty_zero += int(((~has) & (X.abs().sum(1) == 0)).sum())
        return nz.view(n, -1)

    def result(self, V: int, n_empty: int) -> dict:
        return {"rows_roundtrip_ok": self.rows_ok, "max_abs_norm_minus_expected": self.max_norm_err,
                "expected_norm": "1" if self.codec.length_normalize else "sqrt(L)",
                "empty_rows_map_to_zero": self.empty_zero,
                "pass": self.rows_ok == V and self.empty_zero == n_empty and self.max_norm_err < 1e-5}


@dataclass
class Lemma2:
    """z-norm: values match the closed form; the support is exactly {z > 0}."""
    codec: CodecConfig
    support_ok: int = 0
    empty_zero: int = 0
    by_L: dict = field(default_factory=lambda: defaultdict(lambda: {"tokens": 0, "max_abs_err": 0.0, "max_rel_err": 0.0}))

    def update(self, Z: torch.Tensor, support: torch.Tensor, L: torch.Tensor) -> None:
        has = L > 0
        self.support_ok += int(((Z > 0) == support).all(1)[has].sum())
        self.empty_zero += int(((~has) & (Z.abs().sum(1) == 0)).sum())
        for Lv in torch.unique(L[has]).tolist():
            m = L == Lv
            on, off = closed_form(Lv, self.codec)
            pred = torch.where(support[m], torch.tensor(on, dtype=torch.float64),
                               torch.tensor(off, dtype=torch.float64))
            diff = (Z[m].double() - pred).abs()
            r = self.by_L[Lv]
            r["tokens"] += int(m.sum())
            r["max_abs_err"] = max(r["max_abs_err"], float(diff.max()))
            r["max_rel_err"] = max(r["max_rel_err"], float((diff / pred.abs()).max()))

    def result(self, V: int, n_empty: int) -> dict:
        table = []
        for Lv in sorted(self.by_L):
            on, off = closed_form(Lv, self.codec)
            table.append({"L": Lv, "z_on": on, "z_off": off, **self.by_L[Lv]})
        max_rel = max((r["max_rel_err"] for r in table), default=0.0)
        return {"rows_support_recovered": self.support_ok, "nonempty_rows": V - n_empty,
                "empty_rows_map_to_zero": self.empty_zero,
                "max_abs_err_vs_closed_form": max((r["max_abs_err"] for r in table), default=0.0),
                "max_rel_err_vs_closed_form": max_rel, "by_length": table,
                "pass": self.support_ok == V - n_empty and self.empty_zero == n_empty and max_rel < 1e-5}


@dataclass
class Theorem1:
    """Hash every final codec row; byte rows <-> codec rows must be a bijection."""
    row_hash: list[bytes] = field(default_factory=list)
    digest: "hashlib._Hash" = field(default_factory=hashlib.sha256)

    def update(self, K: torch.Tensor) -> None:
        Kn = K.numpy()
        self.digest.update(Kn.tobytes())
        self.row_hash.extend(hashlib.sha256(Kn[i].tobytes()).digest() for i in range(Kn.shape[0]))

    def hash_ids(self) -> tuple[np.ndarray, int]:
        arr = np.frombuffer(b"".join(self.row_hash), dtype="V32")
        _, inv = np.unique(arr, return_inverse=True)
        inv = inv.ravel()
        return inv, int(inv.max()) + 1 if inv.size else 0

    def result(self, groups: Groups) -> dict:
        h_inv, n_h = self.hash_ids()
        b_inv = groups.inverse.astype(np.int64)
        n_pairs = len(np.unique(b_inv * max(n_h, 1) + h_inv))
        single = sum(len(np.unique(h_inv[m])) == 1 for m in groups.members)
        return {
            "distinct_byte_rows": groups.n_distinct,
            "distinct_codec_rows": n_h,
            "byte_rows_with_more_than_one_codec_row": n_pairs - groups.n_distinct,
            "codec_rows_shared_by_distinct_byte_rows": n_pairs - n_h,
            "collision_groups_with_single_codec_row": int(single),
            "collision_groups": len(groups.members),
            "codec_table_sha256": self.digest.hexdigest(),
            "pass": groups.n_distinct == n_h == n_pairs and single == len(groups.members),
        }


# ---- drivers -------------------------------------------------------------------

def run_checks(table: ByteTable, groups: Groups, codec: CodecConfig, compute: ComputeConfig) -> tuple[dict, list[bytes]]:
    V, P = table.V, codec.pos_dim
    if table.P != P:
        raise ValueError(f"table P={table.P} != codec pos_dim={P}")
    chunk = compute.rows_per_chunk(codec.D)
    pos = torch.arange(P)
    l1, l2, t1 = Lemma1(codec), Lemma2(codec), Theorem1()
    for s in range(0, V, chunk):
        data, lens = table.data[s: s + chunk], table.lengths[s: s + chunk]
        L = torch.from_numpy(lens.astype(np.int64))
        bt = torch.from_numpy(data.astype(np.int64))
        valid = pos.unsqueeze(0) < L.unsqueeze(1)
        X = codec_rows(data, lens, codec, z=False)
        support = l1.update(X, bt, L, valid)
        if codec.z_normalize:
            Z = codec_rows(data, lens, codec, z=True)
            l2.update(Z, support, L)
            t1.update(Z)
        else:
            t1.update(X)
    n_empty = int((table.lengths == 0).sum())
    res = {"rows": V, "empty_rows": n_empty, "chunk_rows": chunk,
           "lemma1": l1.result(V, n_empty),
           "lemma2": l2.result(V, n_empty) if codec.z_normalize else {"skipped": "z_normalize is off", "pass": True},
           "theorem1": t1.result(groups)}
    return res, t1.row_hash


def mode_check(table: ByteTable, groups: Groups, row_hash: list[bytes],
               codec: CodecConfig, compute: ComputeConfig) -> dict:
    """KroneckerEmbedding dynamic vs cached, on collision members plus random IDs.

    Also checks that one full-batch call gives the chunked rows (batch invariance).
    """
    from kronecker_embeddings import KroneckerEmbedding
    rng = np.random.default_rng(compute.seed)
    members = sorted({int(i) for m in groups.members for i in m})
    if len(members) > compute.mode_check_max_members:
        members = sorted(rng.choice(members, compute.mode_check_max_members, replace=False).tolist())
    rand = rng.choice(table.V, min(compute.mode_check_random_ids, table.V), replace=False).tolist()
    ids = sorted(set(members) | set(rand))
    sb, sl = torch.from_numpy(table.data[ids]), torch.from_numpy(table.lengths[ids])
    kw = dict(byte_buffer=sb, length_buffer=sl, char_dim=codec.char_dim, pos_dim=codec.pos_dim,
              length_normalize=codec.length_normalize, z_normalize=codec.z_normalize)
    torch.manual_seed(compute.seed)
    dyn = KroneckerEmbedding(len(ids), 16, mode="dynamic", **kw)
    cac = KroneckerEmbedding(len(ids), 16, mode="cached", **kw)
    cac.load_state_dict(dyn.state_dict())
    x = torch.arange(len(ids)).view(1, -1)
    with torch.no_grad():
        cd, cc = dyn._codec_lookup(x), cac._codec_lookup(x)
        ed, ec = dyn(x), cac(x)
    out = {"ids_tested": len(ids), "collision_members_tested": len(members),
           "codec_dynamic_equals_cached_bitwise": bool(torch.equal(cd, cc)),
           "embedding_dynamic_equals_cached_bitwise": bool(torch.equal(ed, ec))}
    if codec.eps == KRON_DEFAULT_EPS:
        rows = cd.view(len(ids), -1).numpy()
        out["full_batch_equals_chunked_rows"] = all(
            hashlib.sha256(rows[k].tobytes()).digest() == row_hash[i] for k, i in enumerate(ids))
    else:
        out["full_batch_equals_chunked_rows"] = "skipped: eps differs from KroneckerEmbedding's default"
    out["pass"] = (out["codec_dynamic_equals_cached_bitwise"] and out["embedding_dynamic_equals_cached_bitwise"]
                   and out["full_batch_equals_chunked_rows"] is not False)
    return out
