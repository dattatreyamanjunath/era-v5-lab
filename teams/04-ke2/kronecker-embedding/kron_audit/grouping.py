"""Find token IDs that share a byte row (bytes and length).

Vectorized: each row plus its 2-byte length is one fixed-width record, and
np.unique sorts the records in C. O(V log V) time, O(V * P) memory.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .tables import ByteTable


@dataclass
class Groups:
    inverse: np.ndarray         # [V] class id of each token's row
    n_distinct: int             # number of distinct rows
    members: list[np.ndarray]   # ID arrays of classes with >= 2 IDs, largest first, IDs ascending

    @property
    def colliding_tokens(self) -> int:
        return int(sum(len(m) for m in self.members))


def row_records(table: ByteTable) -> np.ndarray:
    """[V] array of opaque fixed-width records: P row bytes + 2 length bytes."""
    lens = table.lengths.astype("<u2").view(np.uint8).reshape(-1, 2)
    rec = np.ascontiguousarray(np.concatenate([table.data, lens], axis=1))
    return rec.view(np.dtype((np.void, rec.shape[1]))).ravel()


def find_groups(table: ByteTable) -> Groups:
    _, inverse, counts = np.unique(row_records(table), return_inverse=True, return_counts=True)
    inverse = inverse.ravel()
    order = np.argsort(inverse, kind="stable")          # IDs grouped by class, ascending within
    starts = np.concatenate([[0], np.cumsum(counts)[:-1]])
    members = [order[starts[c]: starts[c] + counts[c]] for c in np.nonzero(counts >= 2)[0]]
    members.sort(key=lambda m: (-len(m), int(m[0])))
    return Groups(inverse, int(len(counts)), members)
