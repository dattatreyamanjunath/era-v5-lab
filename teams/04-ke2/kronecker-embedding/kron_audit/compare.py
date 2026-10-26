"""Compare two runs (e.g. P=32 vs P=64) from their saved results."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .causes import cause_names
from .report import RunView, esc, md_table

D_MODELS = (768, 4096)  # example widths for the projection-size row


def _split_status(groups_a: list[dict], groups_b: list[dict]) -> tuple[dict, list[dict]]:
    """For each group in A: unchanged / partly split / fully split in B."""
    where_b = {i: g["group"] for g in groups_b for i in g["ids"]}
    counts = {"unchanged": 0, "partly split": 0, "fully split": 0}
    kept = []
    for g in groups_a:
        labels = [where_b.get(i, ("solo", i)) for i in g["ids"]]
        n_rows = len(set(labels))
        if n_rows == 1:
            counts["unchanged"] += 1
            kept.append(g)
        elif n_rows == len(g["ids"]):
            counts["fully split"] += 1
        else:
            counts["partly split"] += 1
            kept.append(g)
    return counts, kept


def compare_runs(dir_a: Path, dir_b: Path, out_path: Path | None = None) -> Path:
    a, b = RunView(dir_a), RunView(dir_b)
    common = [n for n in a.tokenizers if n in b.tokenizers]
    A, B = f"P={a.P}", f"P={b.P}"
    out = [f"# Run comparison: `{a.name}` ({A}) vs `{b.name}` ({B})", "",
           "Rendered by `python -m kron_audit compare` from the two run folders. Do not edit by hand.", ""]

    # Lost IDs
    rows = []
    for n in common:
        sa, sb = a.summary(n), b.summary(n)
        rows.append([n, f"{sa['tables']['V']:,}",
                     f"{sa['decode']['ids_without_unique_row']:,}", f"{sb['decode']['ids_without_unique_row']:,}",
                     f"{sa['raw']['ids_without_unique_row']:,}", f"{sb['raw']['ids_without_unique_row']:,}",
                     f"{sa['raw']['collision_groups']} → {sb['raw']['collision_groups']}"])
    out += ["## Lost IDs (V − distinct rows)", "",
            md_table(["tokenizer", "V", f"decode {A}", f"decode {B}", f"raw {A}", f"raw {B}", "raw groups"], rows), ""]

    # By cause
    rows = []
    for n in common:
        sa, sb = a.summary(n), b.summary(n)
        for kind in ("decode", "raw"):
            for cause in cause_names():
                ca, cb = sa[kind]["by_cause"].get(cause), sb[kind]["by_cause"].get(cause)
                if ca or cb:
                    fmt = lambda c: f"{c['groups']} / {c['tokens']}" if c else "0 / 0"
                    rows.append([n, kind, cause, fmt(ca), fmt(cb)])
    out += ["## Collisions by cause (groups / tokens)", "",
            md_table(["tokenizer", "table", "cause", A, B], rows), ""]

    # Paper truncation claim
    rows = []
    for n in common:
        ca, cb = a.summary(n)["paper_truncation_claim"], b.summary(n)["paper_truncation_claim"]
        rows.append([n, ca["tokens_longer_than_P"], ca["of_which_share_row_with_another_token"],
                     cb["tokens_longer_than_P"], cb["of_which_share_row_with_another_token"]])
    out += ["## Paper §4.2: do tokens longer than P get distinct embeddings?", "",
            md_table(["tokenizer", f"tokens > {a.P} B", f"sharing a row ({A})",
                      f"tokens > {b.P} B", f"sharing a row ({B})"], rows), ""]

    # What happens to A's raw truncation groups in B
    rows, remaining = [], []
    for n in common:
        ga = [g for g in a.groups(n, "raw") if g["cause"] == "truncation"]
        counts, kept = _split_status(ga, b.groups(n, "raw"))
        rows.append([n, len(ga), counts["fully split"], counts["partly split"], counts["unchanged"]])
        remaining += [(n, g) for g in kept]
    out += [f"## Raw-table truncation groups at {A}: what happens at {B}", "",
            md_table(["tokenizer", f"truncation groups at {A}", "fully split", "partly split", "unchanged"], rows), ""]
    if remaining:
        rrows = [[n, g["size"], "`" + esc(g["row_preview"]) + "`"] for n, g in remaining[:40]]
        out += [f"Groups from {A} that still share a row at {B} (first 40):", "",
                md_table(["tokenizer", f"size at {A}", f"shared row at {A}"], rrows), ""]

    # Script classes (raw table)
    for kind in ("raw", "decode"):
        ma, mb = a.script_matrix(kind), b.script_matrix(kind)
        scripts = sorted(set(ma) | set(mb), key=lambda s: -(sum(ma[s].values()) + sum(mb[s].values())))
        rows = [[s, sum(ma[s][n] for n in common), sum(mb[s][n] for n in common)]
                for s in scripts if sum(ma[s].values()) or sum(mb[s].values())]
        out += [f"## Colliding IDs per script class, {kind} table (all tokenizers)", "",
                md_table(["script class", A, B], rows), ""]

    # Cost
    rows = [["P (bytes kept)", a.P, b.P],
            ["D = 256·P (codec width)", f"{a.D:,}", f"{b.D:,}"],
            ["codec row, fp32", f"{a.D * 4 / 1024:.0f} KiB", f"{b.D * 4 / 1024:.0f} KiB"]]
    for dm in D_MODELS:
        rows.append([f"projection params, d_model = {dm}", f"{a.D * dm / 1e6:.1f} M", f"{b.D * dm / 1e6:.1f} M"])
    for n in common:
        V = a.summary(n)["tables"]["V"]
        rows.append([f"byte buffer, {n} (V·P + 2V bytes)", f"{(V * a.P + 2 * V) / 1e6:.1f} MB",
                     f"{(V * b.P + 2 * V) / 1e6:.1f} MB"])
    out += ["## Cost", "", md_table(["", A, B], rows), ""]

    # Checks + determinism
    def _status(rv: RunView) -> str:
        ok = all(e.get("all_checks_pass") for e in rv.overview.values())
        d = rv.determinism()
        det = "not run" if d is None else ("all hashes match" if d["all_hashes_match"] else "MISMATCH")
        return f"checks {'pass' if ok else 'FAIL'}; determinism: {det}"
    out += ["## Status", "", f"- `{a.name}`: {_status(a)}", f"- `{b.name}`: {_status(b)}", ""]

    out_path = out_path or (a.dir.parent / f"compare_{a.name}_{b.name}.md")
    out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return out_path
