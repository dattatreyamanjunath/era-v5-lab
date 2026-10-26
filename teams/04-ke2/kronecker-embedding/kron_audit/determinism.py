"""Decode every token ID on CPU in N fresh processes; all hashes must match.

Each worker is a new Python process with its own PYTHONHASHSEED and torch
thread count (from the config). For every tokenizer it hashes:
  decode table  (the repo's build_byte_buffer: one decode per ID)
  raw table     (true bytes from the vocab)
  codec table   (kronecker_codec on every decode-table row, fp32)
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from .config import PROJECT_ROOT, ExperimentConfig, load_config
from .paths import RunPaths, write_json

log = logging.getLogger("kron_audit")
FIELDS = ("decode_table_sha256", "raw_table_sha256", "codec_table_sha256")


def worker(config_path: str, k: int, out_path: str) -> None:
    import numpy as np
    import torch
    cfg = load_config(config_path)
    run = cfg.determinism.runs[k]
    torch.set_num_threads(run.threads)
    from kronecker_embeddings import build_byte_buffer
    from .bytes_util import table_sha256
    from .codec_checks import codec_rows
    from .sources import load_tokenizer
    from .tables import build_raw_table

    P = cfg.codec.pos_dim
    chunk = cfg.compute.rows_per_chunk(cfg.codec.D)
    res = {"run": k + 1, "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
           "torch_threads": torch.get_num_threads(),
           "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"), "device": "cpu",
           "tokenizers": {}}
    for spec in cfg.tokenizers:
        t0 = time.time()
        lt = load_tokenizer(spec, cfg.base_dir)
        bb, lb = build_byte_buffer(lt.tok, pos_dim=P)          # decodes every ID
        bb, lb = bb.numpy(), lb.numpy()
        raw, _ = build_raw_table(lt, P)
        h = hashlib.sha256()
        for s in range(0, bb.shape[0], chunk):
            h.update(codec_rows(bb[s:s + chunk], lb[s:s + chunk], cfg.codec, z=True).numpy().tobytes())
        res["tokenizers"][spec.name] = {
            "ids_decoded": int(bb.shape[0]),
            "decode_table_sha256": table_sha256(bb, lb),
            "raw_table_sha256": raw.sha256(),
            "codec_table_sha256": h.hexdigest(),
            "seconds": round(time.time() - t0, 2),
        }
    Path(out_path).write_text(json.dumps(res, indent=2))


def run_workers(cfg: ExperimentConfig) -> bool:
    """Launch the configured workers, compare their hashes, write determinism.json."""
    paths = RunPaths.of(cfg)
    cfg.save(paths.resolved_config)   # workers read exactly this config
    runs = []
    for k, r in enumerate(cfg.determinism.runs):
        out = paths.determinism_worker(k + 1)
        out.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PYTHONHASHSEED=str(r.seed), CUDA_VISIBLE_DEVICES="",
                   HF_HUB_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
        log.info("determinism run %d/%d (seed %d, threads %d) ...", k + 1, len(cfg.determinism.runs), r.seed, r.threads)
        t0 = time.time()
        subprocess.run([sys.executable, "-m", "kron_audit", "determinism-worker",
                        "--config", str(paths.resolved_config), "--run", str(k), "--out", str(out)],
                       env=env, check=True, cwd=PROJECT_ROOT)
        d = json.loads(out.read_text())
        d["wall_seconds"] = round(time.time() - t0, 1)
        runs.append(d)

    per_tok, all_ok = {}, True
    for spec in cfg.tokenizers:
        rec = {"ids_decoded_per_run": runs[0]["tokenizers"][spec.name]["ids_decoded"]}
        for f in FIELDS:
            hs = [r["tokenizers"][spec.name][f] for r in runs]
            rec[f] = {f"run{i + 1}": h for i, h in enumerate(hs)} | {"match": len(set(hs)) == 1}
            all_ok &= rec[f]["match"]
        per_tok[spec.name] = rec

    import torch, transformers, tokenizers
    write_json(paths.determinism, {
        "run": cfg.name, "P": cfg.codec.pos_dim, "all_hashes_match": all_ok,
        "runs": [{k: r[k] for k in ("run", "pythonhashseed", "torch_threads", "cuda_visible_devices",
                                    "device", "wall_seconds")} for r in runs],
        "tokenizers": per_tok,
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "machine": platform.machine(), "torch": torch.__version__,
                        "transformers": transformers.__version__, "tokenizers": tokenizers.__version__},
    })
    log.info("determinism: %s", "PASS" if all_ok else "FAIL")
    return all_ok
