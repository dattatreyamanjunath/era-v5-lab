"""Render results/*.json and *.csv into markdown tables (results/tables.md).

The hand-written docs (collisions.md, proof.md, determinism.md) quote these
tables, so every number in them traces back to a result file.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict

from common import RESULTS, TOKENIZERS

CAUSE_ORDER = ["utf8_replacement", "truncation_p32", "decoder_normalization", "byte_fallback_alias",
               "special_literal_clash", "duplicate_vocab_entry", "empty_bytes", "unexplained"]


def load(name):
    s = json.loads((RESULTS / name / "summary.json").read_text())
    c = json.loads((RESULTS / name / "checks.json").read_text())
    return s, c


def script_of(cls: str) -> str:
    return cls.replace(" (fragment)", "")


def read_csv(name, table):
    with open(RESULTS / name / f"collisions_by_script_{table}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def groups(name, table):
    with open(RESULTS / name / f"groups_{table}.jsonl", encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def esc(s: str) -> str:
    return s.replace("|", "\\|").replace("`", "'").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")


def main():
    names = [n for n in TOKENIZERS if (RESULTS / n / "summary.json").exists()]
    out = ["# Generated tables", "", "Rendered by `src/report.py` from `results/`. Do not edit by hand.", ""]

    # 1. Overview
    rows = []
    for n in names:
        s, c = load(n)
        d, r = s["decode"], s["raw"]
        ok = all(c[t][k]["pass"] for t in c for k in ("lemma1", "lemma2", "theorem1", "modes"))
        rows.append([n, f"{s['tables']['V']:,}", d["collision_groups"], f"{d['colliding_tokens']:,}",
                     f"{d['ids_without_unique_row']:,}", r["collision_groups"], f"{r['colliding_tokens']:,}",
                     f"{r['ids_without_unique_row']:,}", "pass" if ok else "FAIL"])
    out += ["## Overview (P = 32)", "",
            "`lost` = V − distinct rows = IDs that do not get their own codec row.", "",
            md_table(["tokenizer", "V", "decode groups", "decode colliding IDs", "decode lost",
                      "raw groups", "raw colliding IDs", "raw lost", "L1/L2/T1/modes"], rows), ""]

    # 2. Causes
    out += ["## Collisions by cause", ""]
    rows = []
    for n in names:
        s, _ = load(n)
        for table in ("decode", "raw"):
            bc = s[table]["by_cause"]
            for cause in CAUSE_ORDER:
                if cause in bc:
                    rows.append([n, table, cause, bc[cause]["groups"], bc[cause]["tokens"]])
    out += [md_table(["tokenizer", "table", "cause", "groups", "tokens"], rows), ""]

    # 3. Script matrix (decode/raw colliding tokens per script, fragments merged)
    for table in ("decode", "raw"):
        mat = defaultdict(lambda: defaultdict(int))
        for n in names:
            for row in read_csv(n, table):
                mat[script_of(row["script_class"])][n] += int(row["colliding_tokens"])
        scripts = sorted([s for s in mat if any(mat[s].values())], key=lambda s: -sum(mat[s].values()))
        rows = [[s] + [mat[s][n] for n in names] + [sum(mat[s].values())] for s in scripts]
        out += [f"## Colliding token IDs per script class — {table} table", "",
                "Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.", "",
                md_table(["script class"] + names + ["total"], rows), ""]

    # 4. Per tokenizer detail
    for n in names:
        s, c = load(n)
        out += [f"## {n}", "", f"Tokenizer `{s['tokenizer']['repo']}` snapshot `{s['tokenizer']['snapshot']}`.", ""]
        ti = s["tables"]
        out += [f"- V = {ti['V']:,}; raw rows by rule: " + ", ".join(f"{k} {v:,}" for k, v in ti["raw_kind_counts"].items()),
                f"- rows where decode bytes ≠ raw bytes: {ti['rows_where_decode_differs_from_raw']:,}; raw rows that are not valid UTF-8: {ti['raw_invalid_utf8']:,}",
                f"- tokens longer than 32 bytes: {s['paper_truncation_claim']['tokens_longer_than_P']}; of these, sharing a row with another token: {s['paper_truncation_claim']['of_which_share_row_with_another_token']}",
                f"- decode table SHA-256 `{ti['decode_table_sha256']}`",
                f"- raw table SHA-256 `{ti['raw_table_sha256']}`", ""]
        for table in ("decode", "raw"):
            csvrows = [r for r in read_csv(n, table) if int(r["colliding_tokens"])]
            if not csvrows:
                out += [f"**{table} table:** no collisions.", ""]
                continue
            causes = [k[len("tokens_"):] for k in csvrows[0] if k.startswith("tokens_")]
            rows = [[r["script_class"], r["tokens"], r["colliding_tokens"], r["groups_touching"]]
                    + [f"{r['tokens_' + k]} / {r['groups_' + k]}" for k in causes] for r in csvrows]
            out += [f"**{table} table, by script class** (cause columns: tokens / groups)", "",
                    md_table(["script class", "tokens in class", "colliding", "groups"] + causes, rows), ""]
            gs = groups(n, table)
            show = gs
            rows = [[g["group"], g["size"], g["cause"], "`" + esc(g["row_preview"]) + "`", g["row_len"],
                     ", ".join(str(i) for i in g["ids"][:6]) + (" …" if g["size"] > 6 else "")] for g in show]
            more = f"\n\nAll {len(gs)} groups. Member pieces and hex bytes: `results/{n}/groups_{table}.jsonl`."
            out += [f"**{table} table, groups**", "",
                    md_table(["#", "size", "cause", "shared row", "row bytes", "IDs"], rows) + more, ""]

    # 5. Proof checks
    rows = []
    for n in names:
        _, c = load(n)
        for table in ("decode", "raw"):
            x = c[table]
            rows.append([n, table, f"{x['lemma1']['rows_roundtrip_ok']:,}/{x['rows']:,}",
                         f"{x['lemma1']['max_abs_norm_minus_1']:.1e}",
                         f"{x['lemma2']['rows_support_recovered']:,}/{x['lemma2']['nonempty_rows']:,}",
                         f"{x['lemma2']['max_rel_err_vs_closed_form']:.1e}",
                         f"{x['theorem1']['distinct_byte_rows']:,}", f"{x['theorem1']['distinct_codec_rows']:,}",
                         f"{x['theorem1']['collision_groups_with_single_codec_row']}/{x['theorem1']['collision_groups']}",
                         "yes" if x["modes"]["pass"] else "NO"])
    out += ["## Proof checks", "",
            md_table(["tokenizer", "table", "L1 round-trip", "L1 max ‖κ̃‖−1", "L2 support = {z>0}",
                      "L2 max rel err", "T1 distinct byte rows", "T1 distinct codec rows",
                      "T1 groups → 1 codec row", "dynamic = cached"], rows), ""]

    # Lemma 2 closed form table (same for every tokenizer)
    _, c = load(names[0])
    by_len = {r["L"]: r for n in names for t in ("decode", "raw") for r in load(n)[1][t]["lemma2"]["by_length"]}
    agg = defaultdict(lambda: [0, 0.0])
    for n in names:
        _, cc = load(n)
        for t in ("decode", "raw"):
            for r in cc[t]["lemma2"]["by_length"]:
                agg[r["L"]][0] += r["tokens"]
                agg[r["L"]][1] = max(agg[r["L"]][1], r["max_rel_err"])
    rows = [[L, f"{by_len[L]['z_on']:.6f}", f"{by_len[L]['z_off']:.8f}", f"{agg[L][0]:,}", f"{agg[L][1]:.1e}"]
            for L in sorted(agg)]
    out += ["## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)", "",
            md_table(["L", "z on support", "z off support", "rows checked", "max rel err"], rows), ""]

    # 6. Determinism
    dp = RESULTS / "determinism.json"
    if dp.exists():
        d = json.loads(dp.read_text())
        out += ["## Determinism (three fresh CPU processes)", "",
                md_table(["run", "PYTHONHASHSEED", "torch threads", "device", "wall s"],
                         [[r["run"], r["pythonhashseed"], r["torch_threads"], r["device"], r["wall_seconds"]] for r in d["runs"]]), ""]
        rows = []
        for n, rec in d["tokenizers"].items():
            for f in ("decode_table_sha256", "raw_table_sha256", "codec_table_sha256"):
                h = rec[f]
                rows.append([n, f.replace("_sha256", ""), f"{rec['ids_decoded_per_run']:,}",
                             f"`{h['run1'][:16]}`", f"`{h['run2'][:16]}`", f"`{h['run3'][:16]}`",
                             "match" if h["match"] else "MISMATCH"])
        out += [md_table(["tokenizer", "hash of", "IDs decoded per run", "run 1", "run 2", "run 3", "result"], rows),
                "", f"All hashes match: **{d['all_hashes_match']}**. Full 64-hex hashes are in `results/determinism.json`.", ""]

    (RESULTS / "tables.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote", RESULTS / "tables.md")


if __name__ == "__main__":
    main()
