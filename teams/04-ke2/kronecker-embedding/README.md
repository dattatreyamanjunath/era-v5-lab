# kronecker-embedding: byte-table and collision audit for Kronecker Embeddings

Team 04-ke2. `kron_audit` is a configurable tool that checks, for any `pos_dim` P and any tokenizer, which token IDs end up with the same embedding in [theschoolofai/kronecker-embeddings](https://github.com/theschoolofai/kronecker-embeddings) (commit `d07cb54`, package 0.1.1; paper arXiv 2605.29459), and why. This folder holds the tool and two finished runs on the six tokenizers of paper Table 3: P = 32 and P = 64.

## Results in one page

1. **The repo's byte table merges many token IDs, at any P.** It is built with `tokenizer.decode([id])`. Every byte-level BPE token that is a piece of a multi-byte character decodes to U+FFFD (`�`), so hundreds of such tokens share one byte row, and hence one embedding.
   - Lost IDs (IDs without an embedding of their own): 343–1,520 per byte-level tokenizer at P=32, and 334–1,436 at P=64.
   - The largest single group is 1,067 Qwen3 IDs, all mapped to `�`.
2. **A raw byte table fixes most of it.** It reads each token's true bytes from the vocab piece. On the five byte-level tokenizers it cuts lost IDs by 86–97% at P=32, and by 92–99.7% at P=64.
3. **What remains is truncation at P, plus Gemma's 110 byte-fallback twins** (e.g. `<0x0A>` and `\n`).
   - At P=32, truncation merges long runs (`----`, `////`, spaces) and long Bengali, Tamil, Devanagari, Thai and Georgian words.
   - At P=64, every word-like collision is gone; only long runs remain.
   - The paper's "truncated tokens still receive distinct embeddings" fails for all six tokenizers at P=32. At P=64 it fails for five; it holds only for Gemma-3, which has no token over 64 bytes.
4. **The codec is not the problem.** [proof.md](proof.md) proves, for every P, that two IDs share a codec row ⟺ they share a byte row. It is checked on all 921,161 rows of both tables, at both P.
5. **Everything is deterministic.** Every token ID was decoded on CPU in three fresh processes per P, and all hashes match. The rewrite also reproduces the first P=32 audit bit for bit. → [determinism.md](determinism.md)

| lost IDs | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss |
|---|---|---|---|---|---|---|
| decode table, P=32 | 343 | 1,411 | 1,520 | 177 | 1,124 | 1,358 |
| raw table, P=32 | 10 | 195 | 184 | 177 | 54 | 155 |
| decode table, P=64 | 334 | 1,316 | 1,436 | 110 | 1,079 | 1,275 |
| raw table, P=64 | 1 | 100 | 100 | 110 | 9 | 72 |

**What to do.** Build the byte buffer from raw bytes. It's free at training time and helps at any P. Going from P=32 to P=64 frees another 383 IDs across the six tokenizers, at the cost of doubling the projection (D = 8,192 → 16,384).

**Documents:**
- [collisions.md](collisions.md): the P=32 analysis.
- [p64.md](p64.md): what changes at P=64.
- [brahmic.md](brahmic.md): BrahmicTokenizer-131K at P=32 and P=64 (zero raw-table collisions).
- [proof.md](proof.md): Lemma 1, Lemma 2, Theorem 1.
- [determinism.md](determinism.md): the three decode runs per P.
- [ARCHITECTURE.md](ARCHITECTURE.md): how the tool is built and extended.

## Quick start

CPU only. The venv, the tables and the Hugging Face cache stay local.

```bash
cd teams/04-ke2/kronecker-embedding
python3.10 -m venv .venv
.venv/bin/pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements-dev.txt

.venv/bin/python -m kron_audit run --config configs/p64.yaml          # full run
.venv/bin/python -m kron_audit compare results/p32 results/p64      # side-by-side report
.venv/bin/python -m pytest                                          # 57 offline tests
```

`run` options:
- `--pos-dim 48` tries another P without a new file.
- `--tokenizers gpt2,qwen3` runs a subset.
- `--name my-run` writes to `results/my-run/`.
- `--skip-determinism`, `--force`, and `--max-workers N` (tokenizers in parallel).

The exit code is non-zero if any check fails.

On this laptop (Apple Silicon, 8 GB), the six tokenizers take about 10 minutes of analysis plus 4 minutes of determinism runs at P=32, and 16 + 8 minutes at P=64. Tokenizers that are already up to date are skipped.

## Configuration

One YAML file describes a run ([`configs/p32.yaml`](configs/p32.yaml), [`configs/p64.yaml`](configs/p64.yaml), [`configs/example-local.yaml`](configs/example-local.yaml)):

```yaml
name: p64                       # results go to results/p64/
codec:                          # passed to kronecker_codec / KroneckerEmbedding
  pos_dim: 64                   # P; D = char_dim * P
  char_dim: 256
  length_normalize: true
  z_normalize: true
  eps: 1.0e-6
tokenizers:
  - {name: gpt2, source: openai-community/gpt2}                 # Hugging Face repo
  - {name: mine, source: ../tok/tokenizer.json}                 # local file (relative to this YAML)
  - {name: pinned, source: Qwen/Qwen3-32B, revision: <commit>, family: auto}
determinism:
  enabled: true
  runs: [{seed: 0, threads: 1}, {seed: 1, threads: 4}, {seed: 2, threads: 8}]
compute:
  chunk_rows: auto              # codec rows per chunk; auto ≈ 128 MB per chunk
  mode_check_random_ids: 4096
  max_workers: 1
```

**Adding a tokenizer** means adding one line. `source` can be:
- a Hugging Face repo ID (optionally with `revision`);
- a local folder holding `tokenizer.json` (and `tokenizer_config.json` for special tokens);
- a path to one `tokenizer.json`.

The family (`bbpe`, `sentencepiece`, `wordpiece`, otherwise `decode`) is detected from the tokenizer and recorded in each summary. `family:` overrides it. To support a new family, or to add a collision cause, see [ARCHITECTURE.md](ARCHITECTURE.md#extension-points).

## The two tables

Both are `uint8 [V, P]` plus `int16 [V]` lengths, cut to at most P bytes on a UTF-8 character boundary.

| table | how each row is built |
|---|---|
| decode | the repo's own `kronecker_embeddings.build_byte_buffer(tok, pos_dim=P)` (`tokenizer.decode([id])`, `<0xNN>` → byte, special tokens → literal text) |
| raw | special token → literal text (same as the repo). `<0xNN>` → the byte. Added token the model can only match literally → its UTF-8 text. Otherwise a per-family strategy: byte-level BPE inverts GPT-2's `bytes_to_unicode`; SentencePiece maps `▁` → space; WordPiece strips `##`. |

**Why the raw table needs its own truncation rule.** The repo's `utf8_safe_truncate` returns `b""` for a byte string longer than P that is not valid UTF-8. So the raw table cuts at P and backs off while the cut lands on a continuation byte. On valid UTF-8 the two rules agree; this is checked on every token and in the tests.

## Tokenizers in the two runs

| name | Hugging Face repo | V | family |
|---|---|---|---|
| gpt2 | openai-community/gpt2 | 50,257 | bbpe |
| llama-3.2 | unsloth/Llama-3.2-1B (ungated mirror of meta-llama) | 128,256 | bbpe |
| qwen3 | Qwen/Qwen3-32B | 151,669 | bbpe |
| gemma-3 | unsloth/gemma-3-1b-pt (ungated mirror of google) | 262,145 | sentencepiece |
| deepseek-v3 | deepseek-ai/DeepSeek-V3-Base | 128,815 | bbpe |
| gpt-oss | openai/gpt-oss-120b (o200k_harmony) | 200,019 | bbpe |

## Layout

| path | what |
|---|---|
| `kron_audit/` | the package; one job per module (map in [ARCHITECTURE.md](ARCHITECTURE.md#modules)) |
| `configs/` | run configs: `p32.yaml`, `p64.yaml`, `example-local.yaml` |
| `tests/` | pytest suite, offline (uses the local HF cache) |
| `tools/pr_precheck.py` | runs the lab's pr-guard rules on staged files before a commit |
| `results/<run>/tables.md` | every table of a run, rendered, including **every collision group with its cause** |
| `results/<run>/<tok>/summary.json` | table hashes, provenance, counts by cause and script class, the paper-claim check |
| `results/<run>/<tok>/checks.json` | Lemma 1 / Lemma 2 / Theorem 1 / mode checks |
| `results/<run>/<tok>/collisions_by_script_{decode,raw}.csv` | per-script counts (fragments kept separate) |
| `results/<run>/<tok>/groups_{decode,raw}.jsonl` | every collision group: IDs, cause, shared row (hex), members' pieces and true bytes |
| `results/<run>/{overview,determinism}.json`, `config.resolved.yaml`, `run.log` | run-level outputs; the exact config used |
| `results/compare_p32_p64.md` | the generated P=32 vs P=64 comparison |
| `artifacts/` (gitignored) | binary tables `<run>/<tok>/{decode,raw}.npz`; their SHA-256 hashes are in `determinism.md` |

**Lab rules.** Files stay under `teams/04-ke2/<topic>/`, under 5 MB, with no data or archive extensions and no email addresses. Run `tools/pr_precheck.py` before committing. The lab's email regex also flags top-level `pytest.mark…` decorators, so the tests use `parametrize = pytest.mark.parametrize`.
