"""Typed experiment configuration, loaded from YAML with CLI overrides.

Every other module receives one `ExperimentConfig` (or a part of it); no
module reads globals for P, D or the tokenizer list.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

import yaml

from . import SCHEMA_VERSION

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAMILIES = ("auto", "bbpe", "sentencepiece", "wordpiece", "decode")
_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class CodecConfig:
    """Parameters of the Kronecker codec (kronecker_codec / KroneckerEmbedding)."""
    pos_dim: int = 32            # P: bytes kept per token
    char_dim: int = 256          # byte alphabet; must cover byte values 0..255
    length_normalize: bool = True
    z_normalize: bool = True
    eps: float = 1e-6

    @property
    def D(self) -> int:
        return self.char_dim * self.pos_dim


@dataclass(frozen=True)
class TokenizerSpec:
    """Where a tokenizer comes from.

    source: a Hugging Face repo id ("Qwen/Qwen3-32B"), a local folder with
    tokenizer files, or a path to a single tokenizer.json. Relative paths
    are resolved against the config file's folder.
    """
    name: str
    source: str
    revision: str | None = None
    family: str = "auto"
    trust_remote_code: bool = False


@dataclass(frozen=True)
class DeterminismRun:
    seed: int
    threads: int


@dataclass(frozen=True)
class DeterminismConfig:
    enabled: bool = True
    runs: tuple[DeterminismRun, ...] = (
        DeterminismRun(0, 1), DeterminismRun(1, 4), DeterminismRun(2, 8))


@dataclass(frozen=True)
class ComputeConfig:
    chunk_rows: int | str = "auto"        # rows per codec chunk, or "auto"
    chunk_bytes: int = 128 * 1024 * 1024  # target fp32 bytes per codec chunk for "auto"
    mode_check_random_ids: int = 4096     # random IDs in the dynamic-vs-cached check
    mode_check_max_members: int = 8192    # cap on collision members in that check
    max_workers: int = 1                  # tokenizers processed in parallel
    seed: int = 0

    def rows_per_chunk(self, D: int) -> int:
        if isinstance(self.chunk_rows, int):
            return self.chunk_rows
        return max(64, self.chunk_bytes // (D * 4))


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    codec: CodecConfig
    tokenizers: tuple[TokenizerSpec, ...]
    determinism: DeterminismConfig = DeterminismConfig()
    compute: ComputeConfig = ComputeConfig()
    results_root: Path = PROJECT_ROOT / "results"
    artifacts_root: Path = PROJECT_ROOT / "artifacts"
    base_dir: Path = PROJECT_ROOT  # where relative tokenizer paths resolve

    # ---- identity -------------------------------------------------------
    def tokenizer_digest(self, spec: TokenizerSpec) -> str:
        """Changes iff a result for this tokenizer would change."""
        from importlib.metadata import version
        payload = {
            "schema": SCHEMA_VERSION,
            "codec": asdict(self.codec),
            "tokenizer": asdict(spec),
            "kronecker_embeddings": version("kronecker-embeddings"),
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def spec(self, name: str) -> TokenizerSpec:
        for s in self.tokenizers:
            if s.name == name:
                return s
        raise KeyError(name)

    # ---- serialization -----------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "codec": asdict(self.codec),
            "tokenizers": [asdict(t) for t in self.tokenizers],
            "determinism": {"enabled": self.determinism.enabled,
                            "runs": [asdict(r) for r in self.determinism.runs]},
            "compute": asdict(self.compute),
            # Paths are stored relative (base_dir to the project, the roots to base_dir)
            # so a saved config is portable across machines.
            "base_dir": _rel(self.base_dir, PROJECT_ROOT),
            "results_root": _rel(self.results_root, self.base_dir),
            "artifacts_root": _rel(self.artifacts_root, self.base_dir),
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(self.to_dict(), sort_keys=False, allow_unicode=True))


def _rel(path: Path, start: Path) -> str:
    """path relative to start when both sit under the project, else absolute."""
    import os
    path, start = Path(path).resolve(), Path(start).resolve()
    if path.is_relative_to(PROJECT_ROOT) and start.is_relative_to(PROJECT_ROOT):
        return os.path.relpath(path, start)
    return str(path)


# ---- loading ---------------------------------------------------------------

def load_config(path: str | Path, overrides: dict[str, Any] | None = None) -> ExperimentConfig:
    """Load a YAML config and apply overrides.

    overrides keys: name, pos_dim, tokenizers (list of names to keep),
    determinism_enabled, max_workers, results_root, artifacts_root.
    """
    path = Path(path).resolve()
    raw = yaml.safe_load(path.read_text()) or {}
    cfg = from_dict(raw, base_dir=path.parent)
    return apply_overrides(cfg, overrides or {})


def from_dict(raw: dict[str, Any], base_dir: Path) -> ExperimentConfig:
    known = {"name", "codec", "tokenizers", "determinism", "compute",
             "results_root", "artifacts_root", "base_dir"}
    extra = set(raw) - known
    if extra:
        raise ConfigError(f"unknown config keys: {sorted(extra)}")
    if "name" not in raw:
        raise ConfigError("config needs a 'name'")
    base = Path(raw["base_dir"]) if "base_dir" in raw else Path(base_dir)
    if not base.is_absolute():
        base = (PROJECT_ROOT / base).resolve()

    codec = CodecConfig(**(raw.get("codec") or {}))
    toks = tuple(TokenizerSpec(**t) for t in (raw.get("tokenizers") or []))
    det_raw = raw.get("determinism") or {}
    det = DeterminismConfig(
        enabled=det_raw.get("enabled", True),
        runs=tuple(DeterminismRun(**r) for r in det_raw["runs"]) if "runs" in det_raw
        else DeterminismConfig().runs,
    )
    compute = ComputeConfig(**(raw.get("compute") or {}))

    def _dir(key: str, default: Path) -> Path:
        v = raw.get(key)
        if v is None:
            return default
        p = Path(v)
        return p if p.is_absolute() else (base / p).resolve()

    cfg = ExperimentConfig(
        name=str(raw["name"]), codec=codec, tokenizers=toks, determinism=det, compute=compute,
        results_root=_dir("results_root", PROJECT_ROOT / "results"),
        artifacts_root=_dir("artifacts_root", PROJECT_ROOT / "artifacts"),
        base_dir=base,
    )
    validate(cfg)
    return cfg


def apply_overrides(cfg: ExperimentConfig, ov: dict[str, Any]) -> ExperimentConfig:
    if not ov:
        return cfg
    if ov.get("pos_dim") is not None:
        cfg = replace(cfg, codec=replace(cfg.codec, pos_dim=int(ov["pos_dim"])))
    if ov.get("name"):
        cfg = replace(cfg, name=str(ov["name"]))
    if ov.get("tokenizers"):
        keep = list(ov["tokenizers"])
        missing = [n for n in keep if n not in {t.name for t in cfg.tokenizers}]
        if missing:
            raise ConfigError(f"tokenizers not in config: {missing}")
        cfg = replace(cfg, tokenizers=tuple(cfg.spec(n) for n in keep))
    if ov.get("determinism_enabled") is not None:
        cfg = replace(cfg, determinism=replace(cfg.determinism, enabled=bool(ov["determinism_enabled"])))
    if ov.get("max_workers") is not None:
        cfg = replace(cfg, compute=replace(cfg.compute, max_workers=int(ov["max_workers"])))
    for key in ("results_root", "artifacts_root"):
        if ov.get(key):
            cfg = replace(cfg, **{key: Path(ov[key]).resolve()})
    validate(cfg)
    return cfg


def validate(cfg: ExperimentConfig) -> None:
    c = cfg.codec
    if not _NAME_RE.match(cfg.name):
        raise ConfigError(f"name {cfg.name!r}: use letters, digits, '.', '_' or '-'")
    if c.pos_dim < 1:
        raise ConfigError("codec.pos_dim must be >= 1")
    if c.pos_dim > 32767:
        raise ConfigError("codec.pos_dim must fit the int16 length buffer (<= 32767)")
    if c.char_dim < 256:
        raise ConfigError("codec.char_dim must be >= 256 so every byte value has a slot")
    if c.eps <= 0:
        raise ConfigError("codec.eps must be > 0")
    if not cfg.tokenizers:
        raise ConfigError("config lists no tokenizers")
    names = [t.name for t in cfg.tokenizers]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        raise ConfigError(f"duplicate tokenizer names: {sorted(dup)}")
    for t in cfg.tokenizers:
        if not _NAME_RE.match(t.name):
            raise ConfigError(f"tokenizer name {t.name!r}: use letters, digits, '.', '_' or '-'")
        if t.family not in FAMILIES:
            raise ConfigError(f"tokenizer {t.name}: family must be one of {FAMILIES}")
    if cfg.determinism.enabled and not cfg.determinism.runs:
        raise ConfigError("determinism is enabled but lists no runs")
    for r in cfg.determinism.runs:
        if r.threads < 1:
            raise ConfigError("determinism run threads must be >= 1")
    cr = cfg.compute.chunk_rows
    if not (cr == "auto" or (isinstance(cr, int) and cr >= 1)):
        raise ConfigError("compute.chunk_rows must be 'auto' or a positive integer")
    if cfg.compute.max_workers < 1:
        raise ConfigError("compute.max_workers must be >= 1")
