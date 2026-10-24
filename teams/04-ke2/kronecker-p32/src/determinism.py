"""Decode every token ID on CPU three times; the three hashes must match.

Each run is a fresh Python process with a different PYTHONHASHSEED and a
different torch thread count. In each run, for every tokenizer, we
  1. decode every token ID (the repo's build_byte_buffer) -> decode table hash,
  2. rebuild the raw byte table -> raw table hash,
  3. run the codec on every decode-table row -> codec table hash.

Usage:  python src/determinism.py            (runs the three workers)
        python src/determinism.py --worker K out.json
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time

RUNS = [  # (PYTHONHASHSEED, torch threads)
    ("0", 1),
    ("1", 4),
    ("2", 8),
]


def worker(k: int, out_path: str) -> None:
    import torch
    torch.set_num_threads(RUNS[k][1])
    from common import TOKENIZERS, load_tokenizer, table_sha256, pack, boundary_truncate
    from tables import decode_table, raw_full
    from checks import _codec, CHUNK

    res = {"run": k + 1, "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
           "torch_threads": torch.get_num_threads(),
           "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
           "device": "cpu", "tokenizers": {}}
    for name in TOKENIZERS:
        t0 = time.time()
        tok = load_tokenizer(name)
        bb, lb = decode_table(tok)                       # decodes every ID
        rfull, _ = raw_full(tok, TOKENIZERS[name][1])
        rbb, rlb = pack([boundary_truncate(r) for r in rfull])
        h = hashlib.sha256()
        for s in range(0, bb.shape[0], CHUNK):
            h.update(_codec(bb[s:s + CHUNK], lb[s:s + CHUNK], z=True).numpy().tobytes())
        res["tokenizers"][name] = {
            "ids_decoded": int(bb.shape[0]),
            "decode_table_sha256": table_sha256(bb, lb),
            "raw_table_sha256": table_sha256(rbb, rlb),
            "codec_table_sha256": h.hexdigest(),
            "seconds": round(time.time() - t0, 2),
        }
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2)


def main() -> int:
    from common import RESULTS, ARTIFACTS, write_json
    here = os.path.dirname(os.path.abspath(__file__))
    runs = []
    for k, (seed, _) in enumerate(RUNS):
        out = ARTIFACTS / f"determinism_run{k + 1}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PYTHONHASHSEED=seed, CUDA_VISIBLE_DEVICES="",
                   HF_HUB_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
        t0 = time.time()
        subprocess.run([sys.executable, os.path.join(here, "determinism.py"), "--worker", str(k), str(out)],
                       env=env, check=True, cwd=here)
        r = json.loads(out.read_text())
        r["wall_seconds"] = round(time.time() - t0, 1)
        runs.append(r)

    names = list(runs[0]["tokenizers"])
    per_tok = {}
    all_ok = True
    for n in names:
        rec = {}
        for field in ("decode_table_sha256", "raw_table_sha256", "codec_table_sha256"):
            hs = [r["tokenizers"][n][field] for r in runs]
            rec[field] = {"run1": hs[0], "run2": hs[1], "run3": hs[2], "match": len(set(hs)) == 1}
            all_ok &= rec[field]["match"]
        rec["ids_decoded_per_run"] = runs[0]["tokenizers"][n]["ids_decoded"]
        per_tok[n] = rec
    import torch, transformers, tokenizers
    summary = {
        "all_hashes_match": all_ok,
        "runs": [{k: r[k] for k in ("run", "pythonhashseed", "torch_threads", "cuda_visible_devices",
                                    "device", "wall_seconds")} for r in runs],
        "tokenizers": per_tok,
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "machine": platform.machine(), "torch": torch.__version__,
                        "transformers": transformers.__version__, "tokenizers": tokenizers.__version__},
    }
    write_json(RESULTS / "determinism.json", summary)
    print("determinism:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--worker":
        worker(int(sys.argv[2]), sys.argv[3])
    else:
        sys.exit(main())
