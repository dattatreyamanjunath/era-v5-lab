"""Run the whole P=32 audit: tables, collisions, proof checks, determinism.

    cd teams/04-ke2/kronecker-p32
    .venv/bin/python src/run_all.py            # all six tokenizers
    .venv/bin/python src/run_all.py gpt2       # a subset
"""

from __future__ import annotations

import logging
import subprocess
import sys
import time

import common  # noqa: F401  (sets CPU-only env first)
from common import RESULTS, TOKENIZERS, load_tokenizer, tokenizer_revision, write_json
import tables
import collisions
import checks


def main(names: list[str], with_determinism: bool) -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(RESULTS / "run.log", mode="w"),
                                  logging.StreamHandler()])
    log = logging.getLogger()
    import torch, transformers, tokenizers, kronecker_embeddings
    log.info("torch %s | transformers %s | tokenizers %s | kronecker_embeddings %s | threads %d",
             torch.__version__, transformers.__version__, tokenizers.__version__,
             kronecker_embeddings.__version__, torch.get_num_threads())

    overall = {}
    for name in names:
        t0 = time.time()
        tok = load_tokenizer(name)
        t = tables.build(name, tok)
        classes = collisions.classify_all(t)
        log.info("[%s] V=%d tables built (%.1fs); decode!=raw rows: %d",
                 name, t.V, time.time() - t0, t.info["rows_where_decode_differs_from_raw"])

        summary = {"tokenizer": tokenizer_revision(name), "tables": t.info, "decode": None, "raw": None}
        chk = {}
        for table in ("decode", "raw"):
            res = collisions.analyse(t, classes, table)
            groups = res.pop("_groups")
            summary[table] = res
            bb, lb = (t.dec_bb, t.dec_lb) if table == "decode" else (t.raw_bb, t.raw_lb)
            c = checks.run_checks(bb, lb, groups)
            row_hash = c.pop("_row_hash")
            c["modes"] = checks.mode_check(bb, lb, groups, row_hash)
            chk[table] = c
            log.info("[%s/%s] distinct=%d groups=%d colliding=%d | L1 %s L2 %s T1 %s modes %s",
                     name, table, res["distinct_rows"], res["collision_groups"], res["colliding_tokens"],
                     c["lemma1"]["pass"], c["lemma2"]["pass"], c["theorem1"]["pass"], c["modes"]["pass"])

        # Paper claim (§4.2): truncated tokens still get distinct embeddings.
        over = [i for i in range(t.V) if len(t.raw_full[i]) > common.P]
        shared = set()
        for line in open(RESULTS / name / "groups_raw.jsonl", encoding="utf-8"):
            import json
            g = json.loads(line)
            if g["cause"] == "truncation_p32":
                shared.update(i for i in g["ids"] if len(t.raw_full[i]) > common.P)
        summary["paper_truncation_claim"] = {
            "tokens_longer_than_P": len(over),
            "of_which_share_row_with_another_token": len(shared),
            "claim_holds": len(shared) == 0,
        }
        write_json(RESULTS / name / "summary.json", summary)
        write_json(RESULTS / name / "checks.json", chk)
        overall[name] = {
            "V": t.V,
            "decode": {k: summary["decode"][k] for k in ("distinct_rows", "collision_groups", "colliding_tokens", "ids_without_unique_row")},
            "raw": {k: summary["raw"][k] for k in ("distinct_rows", "collision_groups", "colliding_tokens", "ids_without_unique_row")},
            "all_checks_pass": all(chk[tb][k]["pass"] for tb in chk for k in ("lemma1", "lemma2", "theorem1", "modes"))
                               and t.info["decode_repacked_equals_repo_buffer"]
                               and t.info["truncation_rule_check"]["valid_utf8_tokens_over_P"]
                               == t.info["truncation_rule_check"]["boundary_equals_utf8_safe"],
            "seconds": round(time.time() - t0, 1),
        }
        log.info("[%s] done in %.1fs, all checks pass: %s", name, overall[name]["seconds"], overall[name]["all_checks_pass"])

    write_json(RESULTS / "overview.json", overall)
    ok = all(v["all_checks_pass"] for v in overall.values())
    if with_determinism:
        log.info("determinism: three fresh CPU runs ...")
        rc = subprocess.run([sys.executable, str(common.ROOT / "src" / "determinism.py")]).returncode
        ok &= rc == 0
    log.info("ALL PASS" if ok else "SOME CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    names = args or list(TOKENIZERS)
    sys.exit(main(names, with_determinism=not args and "--no-determinism" not in sys.argv))
