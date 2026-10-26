# Determinism: every token ID decoded on CPU three times

**Result: all three runs give identical hashes for every tokenizer and every table (18 of 18 match).**

`src/determinism.py` starts three fresh Python processes, one after another. Each one:

1. loads each of the six tokenizers from the local Hugging Face cache (`HF_HUB_OFFLINE=1`);
2. **decodes every token ID** with the repo's `build_byte_buffer` (one `tokenizer.decode([id])` per ID) and hashes the resulting decode table;
3. rebuilds the raw byte table from the vocab and hashes it;
4. runs `kronecker_codec` on every decode-table row and hashes the full fp32 codec table.

The three runs change everything that could plausibly leak into the result:

| run | PYTHONHASHSEED | torch threads | device | CUDA_VISIBLE_DEVICES | wall time |
|---|---|---|---|---|---|
| 1 | 0 | 1 | cpu | (empty) | 94.2 s |
| 2 | 1 | 4 | cpu | (empty) | 56.2 s |
| 3 | 2 | 8 | cpu | (empty) | 52.1 s |

Each run decodes all 921,161 token IDs (50,257 + 128,256 + 151,669 + 262,145 + 128,815 + 200,019).

## Hashes

The table hash is SHA-256 over the shape header `"{V}x{P}"`, the `uint8 [V, 32]` byte buffer and the little-endian `int16 [V]` length buffer (`common.table_sha256`). The codec hash is SHA-256 over the `float32 [V, 8192]` codec table in ID order. The run 1, 2 and 3 values are identical, so one column is shown. Per-run values are in [`results/determinism.json`](results/determinism.json).

| tokenizer | table | SHA-256 (runs 1 = 2 = 3) | match |
|---|---|---|---|
| gpt2 | decode | `fea58ad63a97f0ac9568a74d6d564b148f4ebaf84f289acf32e1e6571f1c1a5b` | yes |
| gpt2 | raw | `e8db9b5152c0828b5e69e5092d6b2f4eb002cc51df0d1930ff8c6f4f100ec86a` | yes |
| gpt2 | codec | `1d0ad8bdd5295a310268fec3ea9694d32a1358be830468ba2a9af69aa40a7724` | yes |
| llama-3.2 | decode | `b051c5ca594b9feec36dd95b04177dbeb9bdea3ec70b5eb33409756e2421e4a6` | yes |
| llama-3.2 | raw | `70d6e7b67a030cccce09fae1fc7893b5fbe6d418d621a16e9881645ce7d1fc3b` | yes |
| llama-3.2 | codec | `b5e3d654a94a3eec378a3639bcccec87bdcdad9fcedbd1b425c134207786eb14` | yes |
| qwen3 | decode | `a3f1f90b85c7fb39dd7e3a2b89d0881bd82248287d09a17eecf5355505701af8` | yes |
| qwen3 | raw | `70c9fd1f77ce95a3bac9d4ccddb86b041d10cf98f4379bdb2aa5243165e0d95d` | yes |
| qwen3 | codec | `a960fde45a72a5f6ebc7ca45687125bcd2c867a5fef272b5bcaa417a222c8e12` | yes |
| gemma-3 | decode | `a76c712edf3ed29c8c1cf0f243d6fa3a03e01782f942e660cf5884118e92dd80` | yes |
| gemma-3 | raw | `a76c712edf3ed29c8c1cf0f243d6fa3a03e01782f942e660cf5884118e92dd80` | yes |
| gemma-3 | codec | `fdbce93b64335d389c3eacb36ddf3f165ed42eb6e5ae4c3812dbe8a063f7f0d8` | yes |
| deepseek-v3 | decode | `9b094069b7eadd8518d4f95ec845afcbb9fc7be4aafa9d5308f373415a212a61` | yes |
| deepseek-v3 | raw | `748d9ff20baf3c4ee96c2b9b01b0becda5655136d413e50b32dd9b846d8ba73a` | yes |
| deepseek-v3 | codec | `91c4dd63b76fc134a2f32c75f260ae1d3e97378855f9f4e29a03330db4fda257` | yes |
| gpt-oss | decode | `b895f2b9a7d5f65ae3973ce6171892e2bd2fd34ce2744705dd9fbc16da9a0aea` | yes |
| gpt-oss | raw | `b7e1f90a0852b5f115fa32b3a4a26703976045b9bcfa78c314097dcccfe4d295` | yes |
| gpt-oss | codec | `f1228acd8c46f657bfb0194f14a9c0925a471d2d0f426364ff541627ce6ff8ba` | yes |

Gemma's decode and raw hashes are equal because the two tables are byte-for-byte the same ([collisions.md](collisions.md)).

**A fourth, independent computation agrees.** The main analysis (`src/run_all.py`, a separate process with torch's default 4 threads) wrote the same decode-table, raw-table and codec-table hashes into `results/<tokenizer>/summary.json` and `checks.json`, for all six tokenizers.

## Why the result is deterministic

- **Decoding is a pure function of the tokenizer files.** `tokenizer.decode` in the Rust `tokenizers` backend has no randomness. Python's string hashing (`PYTHONHASHSEED`) never decides any order: IDs are visited `0 … V−1`.
- **The codec is exact.** Every output cell receives at most one `scatter_add` term (Lemma 1: the indices in a row are distinct), so the order of additions can't matter. The z-norm then reduces over each row on its own. The torch thread count did not change a single bit (runs 1–3).

## Environment

| item | value |
|---|---|
| machine | Apple Silicon (arm64), macOS 26.6.2 |
| Python | 3.10.12 |
| torch | 2.14.1 (CPU wheel) |
| transformers | 5.20.2 |
| tokenizers | 0.23.3 |
| kronecker-embeddings | 0.1.1, git `d07cb543f03d7a72a7c35bc68cfb795bcb02e1ec` |

Tokenizer files (Hugging Face snapshot and SHA-256 of `tokenizer.json`):

| tokenizer | repo | snapshot | tokenizer.json SHA-256 |
|---|---|---|---|
| gpt2 | openai-community/gpt2 | `607a30d783dfa663caf39e06633721c8d4cfcd7e` | `8414cab924d8b9b33013f0d221c5862f365ee9be39c5c2bfae8a5a9e970478a6` |
| llama-3.2 | unsloth/Llama-3.2-1B | `9535bd9b1d1dea6acafbdc4813b728796aeb28da` | `6b9e4e7fb171f92fd137b777cc2714bf87d11576700a1dcd7a399e7bbe39537b` |
| qwen3 | Qwen/Qwen3-32B | `9216db5781bf21249d130ec9da846c4624c16137` | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` |
| gemma-3 | unsloth/gemma-3-1b-pt | `34a98bf3eaecc08c699516f625eb5e56e4c5d99d` | `4667f2089529e8e7657cfb6d1c19910ae71ff5f28aa7ab2ff2763330affad795` |
| deepseek-v3 | deepseek-ai/DeepSeek-V3-Base | `afb92e1fa402c2be2a9eb085312bb02e0384d6c7` | `621ac2e32d0dba658404412318818aaa8ce8cda492e59830109d8da6b517fb41` |
| gpt-oss | openai/gpt-oss-120b | `b5c939de8f754692c1647ca79fbf85e8c1e70f8a` | `0614fe83cadab421296e664e1f48f4261fa8fef6e03e63bb75c20f38e37d07d3` |

The binary tables (`artifacts/<tokenizer>/{decode,raw}_P32.npz`) are not committed: the lab's pr-guard rejects files over 5 MB, and Gemma's raw table alone is 8.9 MB. Rerunning `src/run_all.py` recreates them, and their hashes must equal the table above.
