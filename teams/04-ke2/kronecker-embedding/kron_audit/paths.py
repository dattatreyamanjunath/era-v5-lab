"""Where a run reads and writes. Each run has its own folders, so runs never overwrite each other."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import ExperimentConfig


@dataclass(frozen=True)
class RunPaths:
    results: Path    # committed text results:   results/<run>/
    artifacts: Path  # binary tables, gitignored: artifacts/<run>/

    @classmethod
    def of(cls, cfg: ExperimentConfig) -> "RunPaths":
        return cls(cfg.results_root / cfg.name, cfg.artifacts_root / cfg.name)

    # run level
    @property
    def overview(self) -> Path: return self.results / "overview.json"
    @property
    def log(self) -> Path: return self.results / "run.log"
    @property
    def resolved_config(self) -> Path: return self.results / "config.resolved.yaml"
    @property
    def determinism(self) -> Path: return self.results / "determinism.json"
    @property
    def tables_md(self) -> Path: return self.results / "tables.md"

    # tokenizer level
    def tok(self, name: str) -> Path: return self.results / name
    def summary(self, name: str) -> Path: return self.tok(name) / "summary.json"
    def checks(self, name: str) -> Path: return self.tok(name) / "checks.json"
    def groups(self, name: str, kind: str) -> Path: return self.tok(name) / f"groups_{kind}.jsonl"
    def script_csv(self, name: str, kind: str) -> Path: return self.tok(name) / f"collisions_by_script_{kind}.csv"
    def table_npz(self, name: str, kind: str) -> Path: return self.artifacts / name / f"{kind}.npz"
    def determinism_worker(self, k: int) -> Path: return self.artifacts / f"determinism_run{k}.json"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
