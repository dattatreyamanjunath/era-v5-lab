"""Run an experiment: every tokenizer in the config, then determinism, then the report.

- Resume: a tokenizer whose summary.json carries the same digest is skipped
  (unless force=True). summary.json is written last, so its presence means
  the tokenizer finished.
- Isolation: a tokenizer that fails is recorded as failed; the others still run.
- Parallelism: compute.max_workers > 1 runs tokenizers in separate processes.
"""

from __future__ import annotations

import logging
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from multiprocessing import get_context

from . import SCHEMA_VERSION
from .analysis import analyse, classify_tokens, truncation_claim
from .codec_checks import mode_check, run_checks
from .config import ExperimentConfig, TokenizerSpec
from .paths import RunPaths, read_json, write_json
from .sources import load_tokenizer
from .tables import build_tables

log = logging.getLogger("kron_audit")
CHECK_KEYS = ("lemma1", "lemma2", "theorem1", "modes")


def _all_pass(summary: dict, checks: dict) -> bool:
    t = summary["tables"]
    trc = t["truncation_rule_check"]
    return (all(checks[k][c]["pass"] for k in checks for c in CHECK_KEYS)
            and t["decode_repacked_equals_repo_buffer"]
            and trc["valid_utf8_tokens_over_P"] == trc["boundary_equals_utf8_safe"])


def overview_entry(summary: dict, checks: dict, status: str, seconds: float) -> dict:
    pick = ("distinct_rows", "collision_groups", "colliding_tokens", "ids_without_unique_row")
    return {"status": status, "V": summary["tables"]["V"], "P": summary["tables"]["P"],
            "decode": {k: summary["decode"][k] for k in pick},
            "raw": {k: summary["raw"][k] for k in pick},
            "all_checks_pass": _all_pass(summary, checks), "seconds": round(seconds, 1)}


def run_tokenizer(cfg: ExperimentConfig, spec: TokenizerSpec, force: bool = False) -> dict:
    paths = RunPaths.of(cfg)
    digest = cfg.tokenizer_digest(spec)
    t0 = time.time()
    if not force and paths.summary(spec.name).exists() and paths.checks(spec.name).exists():
        s = read_json(paths.summary(spec.name))
        if s.get("digest") == digest:
            log.info("[%s] up to date, skipped (use --force to redo)", spec.name)
            return overview_entry(s, read_json(paths.checks(spec.name)), "skipped", 0.0)

    lt = load_tokenizer(spec, cfg.base_dir)
    P = cfg.codec.pos_dim
    pair = build_tables(lt, P)
    pair.decode.save(paths.table_npz(spec.name, "decode"))
    pair.raw.save(paths.table_npz(spec.name, "raw"))
    classes = classify_tokens(pair)
    log.info("[%s] V=%d P=%d family=%s tables built (%.1fs)", spec.name, pair.V, P, lt.family, time.time() - t0)

    summary = {"schema": SCHEMA_VERSION, "digest": digest, "run": cfg.name,
               "codec": asdict(cfg.codec), "tokenizer": {"name": spec.name, **lt.provenance},
               "tables": pair.info}
    checks = {}
    for kind in ("decode", "raw"):
        rep = analyse(pair, kind, classes)
        rep.write(paths.groups(spec.name, kind), paths.script_csv(spec.name, kind))
        summary[kind] = rep.summary()
        c, row_hash = run_checks(pair.table(kind), rep.grouping, cfg.codec, cfg.compute)
        c["modes"] = mode_check(pair.table(kind), rep.grouping, row_hash, cfg.codec, cfg.compute)
        checks[kind] = c
        if kind == "raw":
            summary["paper_truncation_claim"] = truncation_claim(pair, rep)
        log.info("[%s/%s] distinct=%d groups=%d colliding=%d | %s", spec.name, kind, rep.distinct_rows,
                 rep.collision_groups, rep.colliding_tokens,
                 " ".join(f"{k}={'ok' if c[k]['pass'] else 'FAIL'}" for k in CHECK_KEYS))
    write_json(paths.checks(spec.name), checks)
    write_json(paths.summary(spec.name), summary)   # last: marks the tokenizer complete
    entry = overview_entry(summary, checks, "ok", time.time() - t0)
    log.info("[%s] done in %.1fs, all checks pass: %s", spec.name, entry["seconds"], entry["all_checks_pass"])
    return entry


def _safe_run(cfg: ExperimentConfig, spec: TokenizerSpec, force: bool) -> tuple[str, dict]:
    if not logging.getLogger("kron_audit").handlers:   # fresh worker process (max_workers > 1)
        setup_logging(RunPaths.of(cfg))
    try:
        return spec.name, run_tokenizer(cfg, spec, force)
    except Exception as e:  # isolate: one tokenizer's failure doesn't stop the run
        log.error("[%s] FAILED: %s", spec.name, e)
        return spec.name, {"status": "failed", "error": f"{type(e).__name__}: {e}",
                           "traceback": traceback.format_exc(), "all_checks_pass": False}


def setup_logging(paths: RunPaths) -> None:
    paths.results.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger("kron_audit")
    root.setLevel(logging.INFO)
    root.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(message)s")
    for h in (logging.FileHandler(paths.log, mode="a"), logging.StreamHandler()):
        h.setFormatter(fmt)
        root.addHandler(h)


def run_experiment(cfg: ExperimentConfig, force: bool = False) -> int:
    from . import determinism, report
    paths = RunPaths.of(cfg)
    setup_logging(paths)
    cfg.save(paths.resolved_config)
    import torch, transformers, tokenizers, kronecker_embeddings
    log.info("run %s | P=%d D=%d | %d tokenizers | torch %s transformers %s tokenizers %s kronecker_embeddings %s",
             cfg.name, cfg.codec.pos_dim, cfg.codec.D, len(cfg.tokenizers), torch.__version__,
             transformers.__version__, tokenizers.__version__, kronecker_embeddings.__version__)

    results: dict[str, dict] = {}
    if cfg.compute.max_workers > 1:
        with ProcessPoolExecutor(cfg.compute.max_workers, mp_context=get_context("spawn")) as ex:
            futs = [ex.submit(_safe_run, cfg, s, force) for s in cfg.tokenizers]
            for f in as_completed(futs):
                name, entry = f.result()
                results[name] = entry
    else:
        for s in cfg.tokenizers:
            name, entry = _safe_run(cfg, s, force)
            results[name] = entry
    overview = {s.name: results[s.name] for s in cfg.tokenizers}   # config order
    write_json(paths.overview, overview)

    ok = all(e.get("all_checks_pass") for e in overview.values())
    if cfg.determinism.enabled:
        if ok:
            ok &= determinism.run_workers(cfg)
        else:
            log.warning("determinism skipped: a tokenizer failed or a check did not pass")
    report.render_run(paths.results)
    log.info("ALL PASS" if ok else "SOME CHECK FAILED")
    return 0 if ok else 1
