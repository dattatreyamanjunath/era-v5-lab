"""Command line.

  python -m kron_audit run --config configs/p64.yaml [--pos-dim 48] [--tokenizers gpt2,qwen3]
                           [--name my-run] [--skip-determinism] [--force] [--max-workers 2]
  python -m kron_audit report results/p64
  python -m kron_audit compare results/p32 results/p64
  python -m kron_audit determinism --config results/p64/config.resolved.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import config as cfgmod


def _load(args) -> cfgmod.ExperimentConfig:
    ov = {
        "name": getattr(args, "name", None),
        "pos_dim": getattr(args, "pos_dim", None),
        "tokenizers": args.tokenizers.split(",") if getattr(args, "tokenizers", None) else None,
        "determinism_enabled": False if getattr(args, "skip_determinism", False) else None,
        "max_workers": getattr(args, "max_workers", None),
        "results_root": getattr(args, "results_root", None),
        "artifacts_root": getattr(args, "artifacts_root", None),
    }
    return cfgmod.load_config(args.config, ov)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="kron_audit", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="build tables, count collisions, run checks and determinism")
    r.add_argument("--config", required=True)
    r.add_argument("--name")
    r.add_argument("--pos-dim", type=int)
    r.add_argument("--tokenizers", help="comma-separated subset of the config's tokenizer names")
    r.add_argument("--skip-determinism", action="store_true")
    r.add_argument("--force", action="store_true", help="redo tokenizers even if results are up to date")
    r.add_argument("--max-workers", type=int)
    r.add_argument("--results-root")
    r.add_argument("--artifacts-root")

    rp = sub.add_parser("report", help="render results/<run>/tables.md")
    rp.add_argument("run_dir")

    c = sub.add_parser("compare", help="compare two run folders")
    c.add_argument("run_a")
    c.add_argument("run_b")
    c.add_argument("--out")

    d = sub.add_parser("determinism", help="only the N-process determinism check")
    d.add_argument("--config", required=True)

    w = sub.add_parser("determinism-worker", help=argparse.SUPPRESS)
    w.add_argument("--config", required=True)
    w.add_argument("--run", type=int, required=True)
    w.add_argument("--out", required=True)

    args = p.parse_args(argv)
    if args.cmd == "run":
        from .pipeline import run_experiment
        return run_experiment(_load(args), force=args.force)
    if args.cmd == "report":
        from .report import render_run
        print(render_run(Path(args.run_dir)))
        return 0
    if args.cmd == "compare":
        from .compare import compare_runs
        print(compare_runs(Path(args.run_a), Path(args.run_b), Path(args.out) if args.out else None))
        return 0
    if args.cmd == "determinism":
        from .determinism import run_workers
        from .paths import RunPaths
        from .pipeline import setup_logging
        cfg = cfgmod.load_config(args.config)
        setup_logging(RunPaths.of(cfg))
        return 0 if run_workers(cfg) else 1
    if args.cmd == "determinism-worker":
        from .determinism import worker
        worker(args.config, args.run, args.out)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
