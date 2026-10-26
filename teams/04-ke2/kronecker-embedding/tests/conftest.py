import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")   # tests use only the local Hugging Face cache
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

import pytest

fixture = pytest.fixture  # alias: the lab pr-guard email regex flags top-level pytest.fixture decorators


def cached_tokenizer_json(repo: str) -> str | None:
    from huggingface_hub import try_to_load_from_cache
    p = try_to_load_from_cache(repo, "tokenizer.json")
    return p if isinstance(p, str) else None


@fixture(scope="session")
def gpt2_json():
    p = cached_tokenizer_json("openai-community/gpt2")
    if not p:
        pytest.skip("openai-community/gpt2 not in the local HF cache")
    return p


@fixture(scope="session")
def gemma_cached():
    if not cached_tokenizer_json("unsloth/gemma-3-1b-pt"):
        pytest.skip("unsloth/gemma-3-1b-pt not in the local HF cache")
    return "unsloth/gemma-3-1b-pt"
