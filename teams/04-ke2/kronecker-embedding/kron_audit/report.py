"""Render one run's result files into results/<run>/tables.md.

Reads only the saved JSON/CSV/JSONL, so it can re-render any past run.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import yaml

from .causes import cause_names
from .paths import read_json

CHECK_KEYS = ("lemma1", "lemma2", "theorem1", "modes")


def md_table(header, rows) -> str:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def esc(s: str) -> str:
    return (s.replace("|", "\\|").replace("`", "'").replace("\n", "\\n")
            .replace("\r", "\\r").replace("\t", "\\t"))


def script_of(cls: str) -> str:
    return cls.replace(" (fragment)", "")


class RunView:
    """Read-only access to one run folder."""

    def __init__(self, run_dir: Path):
        self.dir = Path(run_dir)
        self.config = yaml.safe_load((self.dir / "config.resolved.yaml").read_text())
        self.overview = read_json(self.dir / "overview.json")
        self.name = self.config["name"]
        self.P = self.config["codec"]["pos_dim"]
        self.D = self.config["codec"]["char_dim"] * self.P
        self.tokenizers = [n for n, e in self.overview.items() if e.get("status") != "failed"]
        self.failed = [n for n, e in self.overview.items() if e.get("status") == "failed"]

    def summary(self, tok): return read_json(self.dir / tok / "summary.json")
    def checks(self, tok): return read_json(self.dir / tok / "checks.json")

    def script_rows(self, tok, kind):
        p = self.dir / tok / f"collisions_by_script_{kind}.csv"
        if not p.exists():
            return []
        with open(p, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def groups(self, tok, kind):
        with open(self.dir / tok / f"groups_{kind}.jsonl", encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def determinism(self):
        p = self.dir / "determinism.json"
        return read_json(p) if p.exists() else None

    def script_matrix(self, kind) -> dict[str, dict[str, int]]:
        mat: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for n in self.tokenizers:
            for row in self.script_rows(n, kind):
                mat[script_of(row["script_class"])][n] += int(row["colliding_tokens"])
        return mat


def render_run(run_dir: Path) -> Path:
    rv = RunView(run_dir)
    names = rv.tokenizers
    out = [f"# Generated tables — run `{rv.name}` (P = {rv.P}, D = {rv.D:,})", "",
           "Rendered by `python -m kron_audit report` from this folder. Do not edit by hand.", ""]
    if rv.failed:
        out += [f"**Failed tokenizers:** {', '.join(rv.failed)} (see overview.json).", ""]

    # Overview
    rows = []
    for n in names:
        s, c = rv.summary(n), rv.checks(n)
        d, r = s["decode"], s["raw"]
        ok = all(c[t][k]["pass"] for t in c for k in CHECK_KEYS)
        rows.append([n, f"{s['tables']['V']:,}", s["tables"]["family"], d["collision_groups"], f"{d['colliding_tokens']:,}",
                     f"{d['ids_without_unique_row']:,}", r["collision_groups"], f"{r['colliding_tokens']:,}",
                     f"{r['ids_without_unique_row']:,}", "pass" if ok else "FAIL"])
    out += ["## Overview", "", "`lost` = V − distinct rows = IDs that do not get their own codec row.", "",
            md_table(["tokenizer", "V", "family", "decode groups", "decode colliding IDs", "decode lost",
                      "raw groups", "raw colliding IDs", "raw lost", "L1/L2/T1/modes"], rows), ""]

    # Causes
    rows = []
    for n in names:
        s = rv.summary(n)
        for kind in ("decode", "raw"):
            for cause in cause_names():
                if cause in s[kind]["by_cause"]:
                    bc = s[kind]["by_cause"][cause]
                    rows.append([n, kind, cause, bc["groups"], bc["tokens"]])
    out += ["## Collisions by cause", "", md_table(["tokenizer", "table", "cause", "groups", "tokens"], rows), ""]

    # Paper claim
    rows = [[n, rv.summary(n)["paper_truncation_claim"]["tokens_longer_than_P"],
             rv.summary(n)["paper_truncation_claim"]["of_which_share_row_with_another_token"]] for n in names]
    out += [f"## Tokens longer than P = {rv.P}", "",
            md_table(["tokenizer", f"tokens > {rv.P} bytes", "of these, sharing a row"], rows), ""]

    # Script matrices
    for kind in ("decode", "raw"):
        mat = rv.script_matrix(kind)
        scripts = sorted([s for s in mat if any(mat[s].values())], key=lambda s: -sum(mat[s].values()))
        rows = [[s] + [mat[s][n] for n in names] + [sum(mat[s].values())] for s in scripts]
        out += [f"## Colliding token IDs per script class — {kind} table", "",
                "Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.", "",
                md_table(["script class"] + names + ["total"], rows) if rows else "No collisions.", ""]

    # Per tokenizer
    for n in names:
        s = rv.summary(n)
        ti, tk = s["tables"], s["tokenizer"]
        out += [f"## {n}", "",
                f"Source `{tk['source']}` ({tk['source_kind']}), snapshot `{tk.get('snapshot')}`, family `{tk['family']}`.", "",
                f"- V = {ti['V']:,}; raw rows by rule: " + ", ".join(f"{k} {v:,}" for k, v in ti["raw_kind_counts"].items()),
                f"- rows where decode bytes ≠ raw bytes: {ti['rows_where_decode_differs_from_raw']:,}; raw rows that are not valid UTF-8: {ti['raw_invalid_utf8']:,}",
                f"- tokens longer than {rv.P} bytes: {s['paper_truncation_claim']['tokens_longer_than_P']}; of these, sharing a row with another token: {s['paper_truncation_claim']['of_which_share_row_with_another_token']}",
                f"- decode table SHA-256 `{ti['decode_table_sha256']}`",
                f"- raw table SHA-256 `{ti['raw_table_sha256']}`", ""]
        for kind in ("decode", "raw"):
            csvrows = [r for r in rv.script_rows(n, kind) if int(r["colliding_tokens"])]
            if not csvrows:
                out += [f"**{kind} table:** no collisions.", ""]
                continue
            causes = [k[len("tokens_"):] for k in csvrows[0] if k.startswith("tokens_")]
            rows = [[r["script_class"], r["tokens"], r["colliding_tokens"], r["groups_touching"]]
                    + [f"{r['tokens_' + k]} / {r['groups_' + k]}" for k in causes] for r in csvrows]
            out += [f"**{kind} table, by script class** (cause columns: tokens / groups)", "",
                    md_table(["script class", "tokens in class", "colliding", "groups"] + causes, rows), ""]
            gs = rv.groups(n, kind)
            rows = [[g["group"], g["size"], g["cause"], "`" + esc(g["row_preview"]) + "`", g["row_len"],
                     ", ".join(str(i) for i in g["ids"][:6]) + (" …" if g["size"] > 6 else "")] for g in gs]
            out += [f"**{kind} table, groups**", "",
                    md_table(["#", "size", "cause", "shared row", "row bytes", "IDs"], rows)
                    + f"\n\nAll {len(gs)} groups. Member pieces and hex bytes: `{n}/groups_{kind}.jsonl`.", ""]

    # Proof checks
    rows = []
    for n in names:
        c = rv.checks(n)
        for kind in ("decode", "raw"):
            x = c[kind]
            l2 = x["lemma2"]
            rows.append([n, kind, f"{x['lemma1']['rows_roundtrip_ok']:,}/{x['rows']:,}",
                         f"{x['lemma1']['max_abs_norm_minus_expected']:.1e}",
                         f"{l2['rows_support_recovered']:,}/{l2['nonempty_rows']:,}" if "skipped" not in l2 else "skipped",
                         f"{l2['max_rel_err_vs_closed_form']:.1e}" if "skipped" not in l2 else "–",
                         f"{x['theorem1']['distinct_byte_rows']:,}", f"{x['theorem1']['distinct_codec_rows']:,}",
                         f"{x['theorem1']['collision_groups_with_single_codec_row']}/{x['theorem1']['collision_groups']}",
                         "yes" if x["modes"]["pass"] else "NO"])
    out += ["## Proof checks", "",
            md_table(["tokenizer", "table", "L1 round-trip", "L1 max norm err", "L2 support = {z>0}",
                      "L2 max rel err", "T1 distinct byte rows", "T1 distinct codec rows",
                      "T1 groups → 1 codec row", "dynamic = cached"], rows), ""]

    agg: dict[int, list] = {}
    for n in names:
        for kind in ("decode", "raw"):
            for r in rv.checks(n)[kind]["lemma2"].get("by_length", []):
                a = agg.setdefault(r["L"], [r["z_on"], r["z_off"], 0, 0.0])
                a[2] += r["tokens"]
                a[3] = max(a[3], r["max_rel_err"])
    if agg:
        rows = [[L, f"{a[0]:.6f}", f"{a[1]:.8f}", f"{a[2]:,}", f"{a[3]:.1e}"] for L, a in sorted(agg.items())]
        out += ["## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)", "",
                md_table(["L", "z on support", "z off support", "rows checked", "max rel err"], rows), ""]

    d = rv.determinism()
    if d:
        out += [f"## Determinism ({len(d['runs'])} fresh CPU processes)", "",
                md_table(["run", "PYTHONHASHSEED", "torch threads", "device", "wall s"],
                         [[r["run"], r["pythonhashseed"], r["torch_threads"], r["device"], r["wall_seconds"]] for r in d["runs"]]), ""]
        rows = []
        for n, rec in d["tokenizers"].items():
            for f in ("decode_table_sha256", "raw_table_sha256", "codec_table_sha256"):
                h = rec[f]
                runs = [h[k] for k in sorted(k for k in h if k.startswith("run"))]
                rows.append([n, f.replace("_sha256", ""), f"{rec['ids_decoded_per_run']:,}",
                             f"`{runs[0]}`", "match" if h["match"] else "MISMATCH"])
        out += [md_table(["tokenizer", "hash of", "IDs decoded per run", "SHA-256 (run 1)", "all runs"], rows),
                "", f"All hashes match: **{d['all_hashes_match']}**.", ""]

    path = rv.dir / "tables.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path
