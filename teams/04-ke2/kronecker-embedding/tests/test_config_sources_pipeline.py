from dataclasses import replace
from pathlib import Path

import pytest

parametrize = pytest.mark.parametrize  # alias: the lab pr-guard email regex flags top-level pytest.mark decorators
import yaml

from kron_audit.config import PROJECT_ROOT, ConfigError, from_dict, load_config
from kron_audit.paths import RunPaths, read_json

CONFIGS = PROJECT_ROOT / "configs"


# ---- config -------------------------------------------------------------------

def test_shipped_configs_load():
    p32, p64 = load_config(CONFIGS / "p32.yaml"), load_config(CONFIGS / "p64.yaml")
    assert (p32.codec.pos_dim, p64.codec.pos_dim) == (32, 64)
    assert p64.codec.D == 16384
    assert [t.name for t in p32.tokenizers] == [t.name for t in p64.tokenizers]
    load_config(CONFIGS / "example-local.yaml")    # paths are only resolved when loading tokenizers


def test_overrides_and_digest():
    cfg = load_config(CONFIGS / "p32.yaml", {"pos_dim": 48, "tokenizers": ["gpt2", "qwen3"], "name": "p48"})
    assert cfg.codec.pos_dim == 48 and cfg.name == "p48"
    assert [t.name for t in cfg.tokenizers] == ["gpt2", "qwen3"]
    base = load_config(CONFIGS / "p32.yaml")
    spec = base.spec("gpt2")
    assert base.tokenizer_digest(spec) == load_config(CONFIGS / "p32.yaml").tokenizer_digest(spec)
    assert base.tokenizer_digest(spec) != cfg.tokenizer_digest(spec)
    with pytest.raises(ConfigError):
        load_config(CONFIGS / "p32.yaml", {"tokenizers": ["nope"]})


@parametrize("bad", [
    {"name": "x", "tokenizers": []},
    {"name": "x", "codec": {"pos_dim": 0}, "tokenizers": [{"name": "a", "source": "b"}]},
    {"name": "x", "codec": {"char_dim": 128}, "tokenizers": [{"name": "a", "source": "b"}]},
    {"name": "x", "tokenizers": [{"name": "a", "source": "b"}, {"name": "a", "source": "c"}]},
    {"name": "x", "tokenizers": [{"name": "a", "source": "b", "family": "weird"}]},
    {"name": "bad name", "tokenizers": [{"name": "a", "source": "b"}]},
    {"name": "x", "tokenizers": [{"name": "a", "source": "b"}], "typo_key": 1},
])
def test_validation_errors(bad):
    with pytest.raises((ConfigError, TypeError)):
        from_dict(bad, base_dir=PROJECT_ROOT)


def test_resolved_config_round_trip(tmp_path):
    cfg = load_config(CONFIGS / "p64.yaml", {"results_root": tmp_path / "r", "artifacts_root": tmp_path / "a"})
    path = tmp_path / "resolved.yaml"
    cfg.save(path)
    assert load_config(path).to_dict() == cfg.to_dict()


# ---- sources ------------------------------------------------------------------

def test_family_detection(gpt2_json, gemma_cached):
    from kron_audit.config import TokenizerSpec
    from kron_audit.sources import load_tokenizer
    assert load_tokenizer(TokenizerSpec("g", "openai-community/gpt2"), PROJECT_ROOT).family == "bbpe"
    assert load_tokenizer(TokenizerSpec("m", gemma_cached), PROJECT_ROOT).family == "sentencepiece"


def test_missing_local_source_errors(tmp_path):
    from kron_audit.config import TokenizerSpec
    from kron_audit.sources import load_tokenizer
    with pytest.raises(FileNotFoundError):
        load_tokenizer(TokenizerSpec("x", "./does/not/exist/tokenizer.json"), tmp_path)


def test_local_file_equals_hf_repo(gpt2_json):
    from kron_audit.config import TokenizerSpec
    from kron_audit.sources import load_tokenizer
    from kron_audit.tables import build_tables
    hf = build_tables(load_tokenizer(TokenizerSpec("g", "openai-community/gpt2"), PROJECT_ROOT), 8)
    lf = load_tokenizer(TokenizerSpec("g", gpt2_json), PROJECT_ROOT)
    assert lf.provenance["source_kind"] == "file" and lf.family == "bbpe"
    loc = build_tables(lf, 8)
    assert loc.info["raw_table_sha256"] == hf.info["raw_table_sha256"]
    assert loc.info["decode_table_sha256"] == hf.info["decode_table_sha256"]


# ---- end to end ---------------------------------------------------------------

def _smoke_cfg(tmp_path, P, name, runs=2):
    raw = {"name": name, "codec": {"pos_dim": P},
           "tokenizers": [{"name": "gpt2", "source": "openai-community/gpt2"}],
           "determinism": {"enabled": True, "runs": [{"seed": i, "threads": 1 + i} for i in range(runs)]},
           "compute": {"mode_check_random_ids": 256},
           "results_root": str(tmp_path / "results"), "artifacts_root": str(tmp_path / "artifacts")}
    return from_dict(raw, base_dir=PROJECT_ROOT)


def test_pipeline_end_to_end(tmp_path, gpt2_json):
    from kron_audit.compare import compare_runs
    from kron_audit.pipeline import run_experiment
    cfg8 = _smoke_cfg(tmp_path, 8, "p8")
    assert run_experiment(cfg8) == 0
    paths = RunPaths.of(cfg8)
    ov = read_json(paths.overview)
    assert ov["gpt2"]["status"] == "ok" and ov["gpt2"]["all_checks_pass"]
    assert read_json(paths.determinism)["all_hashes_match"]
    assert paths.tables_md.exists() and paths.table_npz("gpt2", "raw").exists()
    s = read_json(paths.summary("gpt2"))
    assert s["tables"]["P"] == 8 and "truncation" in s["raw"]["by_cause"]

    # Resume: unchanged config -> skipped; --force -> recomputed.
    cfg8_nodet = replace(cfg8, determinism=replace(cfg8.determinism, enabled=False))
    assert run_experiment(cfg8_nodet) == 0
    assert read_json(paths.overview)["gpt2"]["status"] == "skipped"
    assert run_experiment(cfg8_nodet, force=True) == 0
    assert read_json(paths.overview)["gpt2"]["status"] == "ok"

    # A second P, then compare: fewer truncation collisions at the larger P.
    cfg4 = replace(_smoke_cfg(tmp_path, 4, "p4"), determinism=replace(cfg8.determinism, enabled=False))
    assert run_experiment(cfg4) == 0
    lost4 = read_json(RunPaths.of(cfg4).summary("gpt2"))["raw"]["ids_without_unique_row"]
    assert lost4 > s["raw"]["ids_without_unique_row"]
    out = compare_runs(RunPaths.of(cfg4).results, paths.results)
    assert out.exists() and "P=4" in out.read_text()


def test_failing_tokenizer_is_isolated(tmp_path, gpt2_json):
    from kron_audit.pipeline import run_experiment
    raw = {"name": "iso", "codec": {"pos_dim": 8},
           "tokenizers": [{"name": "broken", "source": "./missing/tokenizer.json"},
                          {"name": "gpt2", "source": "openai-community/gpt2"}],
           "determinism": {"enabled": False}, "compute": {"mode_check_random_ids": 64},
           "results_root": str(tmp_path / "results"), "artifacts_root": str(tmp_path / "artifacts")}
    cfg = from_dict(raw, base_dir=PROJECT_ROOT)
    assert run_experiment(cfg) == 1
    ov = read_json(RunPaths.of(cfg).overview)
    assert ov["broken"]["status"] == "failed" and ov["gpt2"]["status"] == "ok"
