"""Load a tokenizer from a Hugging Face repo, a local folder or one tokenizer.json.

Also detects the tokenizer family (how vocab pieces map to bytes) and
records provenance (snapshot / file hashes) so results can be traced.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .bytes_util import sha256_file
from .config import TokenizerSpec


@dataclass
class LoadedTokenizer:
    spec: TokenizerSpec
    tok: Any                      # transformers tokenizer
    family: str                   # bbpe | sentencepiece | wordpiece | decode
    backend: dict | None          # parsed tokenizer.json, if the tokenizer has one
    provenance: dict = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def V(self) -> int:
        return max(self.tok.get_vocab().values()) + 1


# ---- source resolution -------------------------------------------------------

def resolve_source(source: str, base_dir: Path) -> tuple[str, str]:
    """-> ("file", path) | ("dir", path) | ("hf", repo_id)."""
    looks_local = source.startswith((".", "/", "~")) or source.endswith(".json")
    p = Path(source).expanduser()
    if not p.is_absolute():
        p = (base_dir / p)
    if p.exists():
        return ("file", str(p.resolve())) if p.is_file() else ("dir", str(p.resolve()))
    if looks_local:
        raise FileNotFoundError(f"tokenizer source {source!r} not found (resolved to {p})")
    return "hf", source


def _load(spec: TokenizerSpec, base_dir: Path):
    kind, where = resolve_source(spec.source, base_dir)
    if kind == "file":
        from transformers import PreTrainedTokenizerFast
        return kind, where, PreTrainedTokenizerFast(tokenizer_file=where)
    from transformers import AutoTokenizer
    kw = {"trust_remote_code": spec.trust_remote_code}
    if spec.revision:
        kw["revision"] = spec.revision
    return kind, where, AutoTokenizer.from_pretrained(where, **kw)


def _backend_json(tok) -> dict | None:
    bt = getattr(tok, "backend_tokenizer", None)
    if bt is None:
        return None
    try:
        return json.loads(bt.to_str())
    except Exception:
        return None


# ---- family detection --------------------------------------------------------

def _walk(node: Any):
    """Yield every dict inside a nested tokenizer.json component."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _has_type(node: Any, type_name: str) -> bool:
    return any(d.get("type") == type_name for d in _walk(node))


def _is_bbpe(j: dict) -> bool:
    return _has_type(j.get("decoder"), "ByteLevel") or _has_type(j.get("pre_tokenizer"), "ByteLevel")


def _is_sentencepiece(j: dict) -> bool:
    model = j.get("model") or {}
    if model.get("byte_fallback"):
        return True
    if _has_type(j.get("decoder"), "Metaspace") or _has_type(j.get("pre_tokenizer"), "Metaspace"):
        return True
    return any(d.get("type") == "Replace" and (d.get("pattern") or {}).get("String") == "▁"
               for d in _walk(j.get("decoder")))


def _is_wordpiece(j: dict) -> bool:
    return (j.get("model") or {}).get("type") == "WordPiece"


# Ordered; the first match wins. Add a detector here to support a new family.
FAMILY_DETECTORS: list[tuple[str, Callable[[dict], bool]]] = [
    ("bbpe", _is_bbpe),
    ("sentencepiece", _is_sentencepiece),
    ("wordpiece", _is_wordpiece),
]


def detect_family(backend: dict | None) -> str:
    if backend is None:
        return "decode"
    for name, test in FAMILY_DETECTORS:
        if test(backend):
            return name
    return "decode"


# ---- entry point -------------------------------------------------------------

def load_tokenizer(spec: TokenizerSpec, base_dir: Path) -> LoadedTokenizer:
    kind, where, tok = _load(spec, base_dir)
    backend = _backend_json(tok)
    family = detect_family(backend) if spec.family == "auto" else spec.family
    prov: dict[str, Any] = {"source": spec.source, "source_kind": kind, "revision": spec.revision,
                            "family": family, "family_detected": spec.family == "auto",
                            "tokenizer_class": type(tok).__name__}
    tj = None
    if kind == "hf":
        from huggingface_hub import try_to_load_from_cache
        path = try_to_load_from_cache(where, "tokenizer.json", revision=spec.revision)
        if isinstance(path, str):
            prov["snapshot"] = Path(path).parent.name
            tj = path
    elif kind == "dir":
        cand = Path(where) / "tokenizer.json"
        tj = str(cand) if cand.exists() else None
    else:
        tj = where
    prov["tokenizer_json_sha256"] = sha256_file(tj) if tj else None
    return LoadedTokenizer(spec, tok, family, backend, prov)
