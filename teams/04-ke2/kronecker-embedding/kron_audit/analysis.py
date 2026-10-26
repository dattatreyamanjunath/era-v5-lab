"""Collision report for one byte table: a cause per group, counts per script class."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .bytes_util import preview, utf8_valid
from .causes import DEFAULT_RULES, CauseRule, GroupContext, assign_cause, cause_names
from .grouping import Groups, find_groups
from .script_class import token_class
from .tables import TablePair

MEMBERS_SHOWN = 12  # members listed in full per group in groups_*.jsonl


@dataclass
class TableReport:
    kind: str
    V: int
    P: int
    distinct_rows: int
    collision_groups: int
    colliding_tokens: int
    largest_group: int
    by_cause: dict[str, dict[str, int]]
    by_script: list[dict]
    groups: list[dict] = field(repr=False)
    grouping: Groups | None = field(default=None, repr=False)

    @property
    def lost_ids(self) -> int:
        return self.V - self.distinct_rows

    def summary(self) -> dict:
        return {
            "V": self.V, "P": self.P,
            "distinct_rows": self.distinct_rows,
            "ids_without_unique_row": self.lost_ids,
            "collision_groups": self.collision_groups,
            "colliding_tokens": self.colliding_tokens,
            "largest_group": self.largest_group,
            "by_cause": self.by_cause,
            "by_script": self.by_script,
        }

    def write(self, groups_path: Path, csv_path: Path) -> None:
        groups_path.parent.mkdir(parents=True, exist_ok=True)
        with open(groups_path, "w", encoding="utf-8") as f:
            for g in self.groups:
                f.write(json.dumps(g, ensure_ascii=False) + "\n")
        if self.by_script:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(self.by_script[0].keys()))
                w.writeheader()
                w.writerows(self.by_script)


def classify_tokens(pair: TablePair) -> list[str]:
    return [token_class(pair.raw.full[i], pair.kinds[i]) for i in range(pair.V)]


def analyse(pair: TablePair, kind: str, classes: list[str],
            rules: list[CauseRule] = DEFAULT_RULES) -> TableReport:
    table = pair.table(kind)
    groups = find_groups(table)
    class_total = Counter(classes)
    per_class: dict[str, Counter] = defaultdict(Counter)
    by_cause = {c: {"groups": 0, "tokens": 0} for c in cause_names(rules)}
    records = []

    for gid, ids_arr in enumerate(groups.members):
        ids = [int(i) for i in ids_arr]
        key = table.row(ids[0])
        ctx = GroupContext(kind, key, ids,
                           [pair.raw.full[i] for i in ids], [pair.decode.full[i] for i in ids],
                           [pair.kinds[i] for i in ids], pair.P)
        cause = assign_cause(ctx, rules)
        by_cause[cause]["groups"] += 1
        by_cause[cause]["tokens"] += len(ids)
        cc = Counter(classes[i] for i in ids)
        for c, n in cc.items():
            pc = per_class[c]
            pc["colliding_tokens"] += n
            pc["groups_touching"] += 1
            pc[f"tokens_{cause}"] += n
            pc[f"groups_{cause}"] += 1
            if len(cc) == 1:
                pc["groups_pure"] += 1
        records.append({
            "table": kind, "group": gid, "size": len(ids), "cause": cause,
            "row_hex": key.hex(), "row_preview": preview(key), "row_len": len(key),
            "class_counts": dict(cc.most_common()),
            "kinds": dict(Counter(ctx.kinds)),
            "members_invalid_utf8": sum(not utf8_valid(r) for r in ctx.raw_full),
            "members_decode_ne_raw": sum(d != r for d, r in zip(ctx.dec_full, ctx.raw_full)),
            "ids": ids,
            "members": [{"id": i, "piece": pair.pieces[i], "raw_hex": pair.raw.full[i].hex(),
                         "raw_len": len(pair.raw.full[i]), "raw_preview": preview(pair.raw.full[i]),
                         "class": classes[i]} for i in ids[:MEMBERS_SHOWN]],
        })

    used = [c for c in cause_names(rules) if by_cause[c]["groups"]]
    rows = []
    for c in sorted(class_total, key=lambda c: (-per_class[c]["colliding_tokens"], -class_total[c], c)):
        pc = per_class[c]
        row = {"script_class": c, "tokens": class_total[c],
               "colliding_tokens": pc["colliding_tokens"],
               "colliding_pct": round(100.0 * pc["colliding_tokens"] / class_total[c], 3),
               "groups_touching": pc["groups_touching"], "groups_pure": pc["groups_pure"]}
        for cause in used:
            row[f"tokens_{cause}"] = pc[f"tokens_{cause}"]
            row[f"groups_{cause}"] = pc[f"groups_{cause}"]
        rows.append(row)

    return TableReport(
        kind=kind, V=table.V, P=table.P, distinct_rows=groups.n_distinct,
        collision_groups=len(groups.members), colliding_tokens=groups.colliding_tokens,
        largest_group=len(groups.members[0]) if groups.members else 0,
        by_cause={c: v for c, v in by_cause.items() if v["groups"]},
        by_script=rows, groups=records, grouping=groups,
    )


def truncation_claim(pair: TablePair, raw_report: TableReport) -> dict:
    """Paper §4.2: tokens longer than P 'still receive distinct embeddings'."""
    P = pair.P
    over = [i for i in range(pair.V) if len(pair.raw.full[i]) > P]
    shared = {i for g in raw_report.groups if g["cause"] == "truncation"
              for i in g["ids"] if len(pair.raw.full[i]) > P}
    return {"P": P, "tokens_longer_than_P": len(over),
            "of_which_share_row_with_another_token": len(shared),
            "claim_holds": len(shared) == 0}
