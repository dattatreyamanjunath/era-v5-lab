# kronecker-p32: decode vs raw byte tables for Kronecker Embeddings at P = 32

Team 04-ke2. An audit of the byte tables that feed
[theschoolofai/kronecker-embeddings](https://github.com/theschoolofai/kronecker-embeddings)
(commit `d07cb54`, package 0.1.1; paper arXiv 2605.29459) at `pos_dim = P = 32`. It covers the six tokenizers of paper Table 3.

## Results in one page

1. **The repo's byte table merges many token IDs.** It is built with `tokenizer.decode([id])`. Every byte-level BPE token that is a piece of a multi-byte character decodes to U+FFFD (`�`), so hundreds of such tokens share one byte row, and hence one embedding.
   - Lost IDs (IDs without an embedding of their own): GPT-2 343, Llama-3.2 1,411, Qwen3 1,520, DeepSeek-V3 1,124, gpt-oss 1,358. Gemma-3 loses 177, for other reasons.
   - The largest single group is 1,067 Qwen3 IDs, all mapped to `�`.
   - Most of these are CJK, Hangul, Hebrew and Indic fragments. → [collisions.md](collisions.md)
2. **A raw byte table fixes most of it.** It reads each token's true bytes from its vocab piece.
   - Lost IDs drop by 86–97%: 10 / 195 / 184 / 54 / 155.
   - Gemma's tables are already identical (177 either way).
3. **What remains is truncation at 32 bytes, plus Gemma's byte-fallback twins.**
   - **Truncation:** long runs of spaces, `----` or `////`, and long words in 3-byte scripts (Bengali, Devanagari, Tamil, Thai, Malayalam, Georgian) share their first 32 bytes.
   - **This contradicts the paper.** It says truncated tokens "still receive distinct embeddings"; that is false for every tokenizer tested. For example, 210 of Llama-3.2's 231 tokens longer than 32 bytes share a row with another token.
   - **Gemma's byte-fallback twins:** 110 pairs like `<0x0A>` and `\n`, which have the same bytes.
4. **The codec is not the problem.** [proof.md](proof.md) proves:
   - Lemma 1: the pre-norm codec is injective, and its norm is exactly 1.
   - Lemma 2: z-norm keeps it injective, in exact arithmetic and in fp32.
   - Theorem 1: two IDs share a codec row ⟺ they share a byte row, in both `dynamic` and `cached` modes.

   Each is checked numerically on all 921,161 rows of both tables: every row is inverted exactly, and every collision group maps to exactly one codec hash.
5. **Everything is deterministic.** Every token ID was decoded on CPU in three fresh processes, with different hash seeds and thread counts, and all 18 table and codec hashes match. → [determinism.md](determinism.md)

## The two tables

Both are `uint8 [V, 32]` plus `int16 [V]` lengths. Both are cut to at most 32 bytes on a UTF-8 character boundary.

| table | how each row is built |
|---|---|
| decode | the repo's own `kronecker_embeddings.build_byte_buffer` (`tokenizer.decode([id])`, `<0xNN>` → byte, special tokens → literal text) |
| raw | special token → literal text (same as the repo). `<0xNN>` → the byte. Added token that the model can only match literally → its UTF-8 text. Byte-level BPE piece → invert GPT-2's `bytes_to_unicode` map. SentencePiece piece → `▁` becomes a space. |

**Why the raw table needs its own truncation rule.** The repo's `utf8_safe_truncate` returns `b""` for a byte string longer than 32 bytes that is not valid UTF-8. So the raw table instead cuts at 32 and backs off while the cut lands on a continuation byte. On valid UTF-8 the two rules agree on every token (checked).

## Tokenizers

| name | Hugging Face repo | V | family |
|---|---|---|---|
| gpt2 | openai-community/gpt2 | 50,257 | byte-level BPE |
| llama-3.2 | unsloth/Llama-3.2-1B (ungated mirror of meta-llama) | 128,256 | byte-level BPE |
| qwen3 | Qwen/Qwen3-32B | 151,669 | byte-level BPE |
| gemma-3 | unsloth/gemma-3-1b-pt (ungated mirror of google) | 262,145 | SentencePiece BPE + byte fallback |
| deepseek-v3 | deepseek-ai/DeepSeek-V3-Base | 128,815 | byte-level BPE |
| gpt-oss | openai/gpt-oss-120b (o200k_harmony) | 200,019 | byte-level BPE |

## Files

| path | what |
|---|---|
| [proof.md](proof.md) | Lemma 1, Lemma 2, Theorem 1, with numerical checks |
| [collisions.md](collisions.md) | collision counts per script class, causes, notable groups |
| [determinism.md](determinism.md) | the three CPU decode runs and their hashes |
| `results/tables.md` | every table rendered from the result files, including **every collision group with its cause** |
| `results/<tok>/summary.json` | table hashes, counts by cause and by script class, the paper-claim check |
| `results/<tok>/checks.json` | Lemma 1 / Lemma 2 / Theorem 1 / mode checks |
| `results/<tok>/collisions_by_script_{decode,raw}.csv` | per-script counts (fragments kept separate) |
| `results/<tok>/groups_{decode,raw}.jsonl` | every collision group: IDs, cause, shared row (hex), members' pieces and true bytes |
| `results/determinism.json`, `results/overview.json`, `results/run.log` | run outputs |
| `src/tables.py` | builds the decode and raw tables |
| `src/script_class.py` | script class from true bytes (fragments classed by lead byte) |
| `src/collisions.py` | grouping, cause rules, per-script counts |
| `src/checks.py` | numerical checks for the proofs |
| `src/determinism.py` | three fresh CPU decode runs |
| `src/run_all.py` | runs everything |
| `src/report.py` | renders `results/tables.md` |
| `src/pr_precheck.py` | runs the lab's pr-guard rules on staged files |

`artifacts/` (gitignored) holds the binary tables `{decode,raw}_P32.npz`. They are not committed, since Gemma's is over pr-guard's 5 MB limit; their SHA-256 hashes are in `determinism.md`.

## Reproduce

CPU only. About 6 minutes for the analysis plus about 3.5 minutes for the three determinism runs, on an Apple M-series laptop.

```bash
cd teams/04-ke2/kronecker-p32
python3.10 -m venv .venv
.venv/bin/pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt
.venv/bin/python src/run_all.py      # tables, collisions, proof checks, determinism
.venv/bin/python src/report.py       # results/tables.md
```

`run_all.py` exits non-zero if any check fails, and logs `ALL PASS` otherwise. Pass tokenizer names (e.g. `src/run_all.py gpt2`) for a quick partial run; that skips the determinism step.
