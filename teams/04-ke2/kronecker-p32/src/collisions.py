"""Collision groups per table, a cause for each group, counts per script class.

A collision group is a set of >= 2 token IDs whose byte rows (bytes and
length) are identical. By Theorem 1 (proof.md) these are exactly the IDs
whose Kronecker codec rows are identical.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict

from common import RESULTS, boundary_truncate, row_key
from script_class import token_class

FFFD = "�".encode("utf-8")

CAUSES = [
    "utf8_replacement",       # decode turned partial UTF-8 into U+FFFD
    "truncation_p32",         # different true bytes, same safe 32-byte prefix
    "decoder_normalization",  # decode changed valid bytes (e.g. dropped a space)
    "byte_fallback_alias",    # <0xNN> and a normal token with the same byte
    "special_literal_clash",  # special/added literal equals another token's bytes
    "duplicate_vocab_entry",  # two IDs with identical true bytes
    "empty_bytes",            # zero-length row
    "unexplained",
]


def _valid(b: bytes) -> bool:
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _same_bytes_cause(kinds: list[str]) -> str:
    if "byte_fallback" in kinds:
        return "byte_fallback_alias"
    if "special" in kinds or "added_literal" in kinds:
        return "special_literal_clash"
    return "duplicate_vocab_entry"


def group_cause(table: str, key: bytes, ids: list[int], t) -> str:
    raws = [t.raw_full[i] for i in ids]
    kinds = [t.kinds[i] for i in ids]
    if len(key) == 0:
        return "empty_bytes"
    if table == "decode":
        if FFFD in key and any(not _valid(r) for r in raws):
            return "utf8_replacement"
        if len(set(raws)) == 1:
            return _same_bytes_cause(kinds)
        if len({boundary_truncate(r) for r in raws}) == 1:
            return "truncation_p32"
        if any(t.dec_full[i] != t.raw_full[i] for i in ids):
            return "decoder_normalization"
        return "unexplained"
    # raw table
    if len(set(raws)) == 1:
        return _same_bytes_cause(kinds)
    if len({boundary_truncate(r) for r in raws}) == 1:
        return "truncation_p32"
    return "unexplained"


def preview(b: bytes, limit: int = 40) -> str:
    s = b.decode("utf-8", errors="backslashreplace")
    return s if len(s) <= limit else s[:limit] + "…"


def analyse(t, classes: list[str], table: str) -> dict:
    bb, lb = (t.dec_bb, t.dec_lb) if table == "decode" else (t.raw_bb, t.raw_lb)
    groups: dict[bytes, list[int]] = defaultdict(list)
    for i in range(t.V):
        groups[row_key(bb, lb, i)].append(i)
    distinct = len(groups)
    coll = [(k, ids) for k, ids in groups.items() if len(ids) >= 2]
    coll.sort(key=lambda kv: (-len(kv[1]), kv[1][0]))

    out_dir = RESULTS / t.name
    out_dir.mkdir(parents=True, exist_ok=True)

    per_class = defaultdict(lambda: Counter())
    class_total = Counter(classes)
    by_cause = {c: {"groups": 0, "tokens": 0} for c in CAUSES}
    group_records = []
    for gid, (key, ids) in enumerate(coll):
        cause = group_cause(table, key, ids, t)
        by_cause[cause]["groups"] += 1
        by_cause[cause]["tokens"] += len(ids)
        cc = Counter(classes[i] for i in ids)
        for c, n in cc.items():
            per_class[c]["colliding_tokens"] += n
            per_class[c]["groups_touching"] += 1
            per_class[c][f"tokens_{cause}"] += n
            per_class[c][f"groups_{cause}"] += 1
            if len(cc) == 1:
                per_class[c]["groups_pure"] += 1
        group_records.append({
            "table": table,
            "group": gid,
            "size": len(ids),
            "cause": cause,
            "row_hex": key.hex(),
            "row_preview": preview(key),
            "row_len": len(key),
            "class_counts": dict(cc.most_common()),
            "kinds": dict(Counter(t.kinds[i] for i in ids)),
            "members_invalid_utf8": sum(not _valid(t.raw_full[i]) for i in ids),
            "members_decode_ne_raw": sum(t.dec_full[i] != t.raw_full[i] for i in ids),
            "ids": ids,
            "members": [
                {"id": i, "piece": t.pieces[i], "raw_hex": t.raw_full[i].hex(),
                 "raw_len": len(t.raw_full[i]), "raw_preview": preview(t.raw_full[i]),
                 "class": classes[i]}
                for i in ids[:12]
            ],
        })

    with open(out_dir / f"groups_{table}.jsonl", "w", encoding="utf-8") as f:
        for r in group_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    cause_cols = [c for c in CAUSES if by_cause[c]["groups"]]
    rows = []
    for c in sorted(class_total, key=lambda c: (-per_class[c]["colliding_tokens"], -class_total[c], c)):
        pc = per_class[c]
        row = {
            "script_class": c,
            "tokens": class_total[c],
            "colliding_tokens": pc["colliding_tokens"],
            "colliding_pct": round(100.0 * pc["colliding_tokens"] / class_total[c], 3),
            "groups_touching": pc["groups_touching"],
            "groups_pure": pc["groups_pure"],
        }
        for cause in cause_cols:
            row[f"tokens_{cause}"] = pc[f"tokens_{cause}"]
            row[f"groups_{cause}"] = pc[f"groups_{cause}"]
        rows.append(row)
    with open(out_dir / f"collisions_by_script_{table}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    return {
        "V": t.V,
        "distinct_rows": distinct,
        "ids_without_unique_row": t.V - distinct,
        "collision_groups": len(coll),
        "colliding_tokens": sum(len(ids) for _, ids in coll),
        "largest_group": len(coll[0][1]) if coll else 0,
        "by_cause": {c: v for c, v in by_cause.items() if v["groups"]},
        "by_script": rows,
        "_groups": coll,  # used by checks.py, dropped before saving
    }


def classify_all(t) -> list[str]:
    return [token_class(t.raw_full[i], t.kinds[i]) for i in range(t.V)]
