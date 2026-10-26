# Run comparison: `p32` (P=32) vs `p64` (P=64)

Rendered by `python -m kron_audit compare` from the two run folders. Do not edit by hand.

## Lost IDs (V − distinct rows)

| tokenizer | V | decode P=32 | decode P=64 | raw P=32 | raw P=64 | raw groups |
|---|---|---|---|---|---|---|
| gpt2 | 50,257 | 343 | 334 | 10 | 1 | 7 → 1 |
| llama-3.2 | 128,256 | 1,411 | 1,316 | 195 | 100 | 28 → 18 |
| qwen3 | 151,669 | 1,520 | 1,436 | 184 | 100 | 25 → 18 |
| gemma-3 | 262,145 | 177 | 110 | 177 | 110 | 159 → 110 |
| deepseek-v3 | 128,815 | 1,124 | 1,079 | 54 | 9 | 14 → 5 |
| gpt-oss | 200,019 | 1,358 | 1,275 | 155 | 72 | 29 → 11 |

## Collisions by cause (groups / tokens)

| tokenizer | table | cause | P=32 | P=64 |
|---|---|---|---|---|
| gpt2 | decode | utf8_replacement | 7 / 340 | 7 / 340 |
| gpt2 | decode | truncation | 7 / 17 | 1 / 2 |
| gpt2 | raw | truncation | 7 / 17 | 1 / 2 |
| llama-3.2 | decode | utf8_replacement | 13 / 1229 | 13 / 1229 |
| llama-3.2 | decode | truncation | 28 / 223 | 18 / 118 |
| llama-3.2 | raw | truncation | 28 / 223 | 18 / 118 |
| qwen3 | decode | utf8_replacement | 11 / 1347 | 11 / 1347 |
| qwen3 | decode | truncation | 25 / 209 | 18 / 118 |
| qwen3 | raw | truncation | 25 / 209 | 18 / 118 |
| gemma-3 | decode | byte_fallback_alias | 110 / 220 | 110 / 220 |
| gemma-3 | decode | truncation | 49 / 116 | 0 / 0 |
| gemma-3 | raw | byte_fallback_alias | 110 / 220 | 110 / 220 |
| gemma-3 | raw | truncation | 49 / 116 | 0 / 0 |
| deepseek-v3 | decode | utf8_replacement | 37 / 1108 | 36 / 1106 |
| deepseek-v3 | decode | truncation | 13 / 66 | 5 / 14 |
| deepseek-v3 | raw | truncation | 14 / 68 | 5 / 14 |
| gpt-oss | decode | utf8_replacement | 18 / 1221 | 18 / 1221 |
| gpt-oss | decode | truncation | 29 / 184 | 11 / 83 |
| gpt-oss | raw | truncation | 29 / 184 | 11 / 83 |

## Paper §4.2: do tokens longer than P get distinct embeddings?

| tokenizer | tokens > 32 B | sharing a row (P=32) | tokens > 64 B | sharing a row (P=64) |
|---|---|---|---|---|
| gpt2 | 14 | 12 | 3 | 1 |
| llama-3.2 | 231 | 210 | 123 | 112 |
| qwen3 | 240 | 198 | 121 | 112 |
| gemma-3 | 379 | 86 | 0 | 0 |
| deepseek-v3 | 771 | 59 | 13 | 10 |
| gpt-oss | 266 | 171 | 85 | 77 |

## Raw-table truncation groups at P=32: what happens at P=64

| tokenizer | truncation groups at P=32 | fully split | partly split | unchanged |
|---|---|---|---|---|
| gpt2 | 7 | 6 | 1 | 0 |
| llama-3.2 | 28 | 10 | 15 | 3 |
| qwen3 | 25 | 7 | 15 | 3 |
| gemma-3 | 49 | 49 | 0 | 0 |
| deepseek-v3 | 14 | 9 | 4 | 1 |
| gpt-oss | 29 | 18 | 10 | 1 |

Groups from P=32 that still share a row at P=64 (first 40):

| tokenizer | size at P=32 | shared row at P=32 |
|---|---|---|
| gpt2 | 3 | `ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ` |
| llama-3.2 | 60 | `                                ` |
| llama-3.2 | 16 | ` -------------------------------` |
| llama-3.2 | 15 | `////////////////////////////////` |
| llama-3.2 | 15 | `/*******************************` |
| llama-3.2 | 14 | `//------------------------------` |
| llama-3.2 | 12 | ` *******************************` |
| llama-3.2 | 11 | `################################` |
| llama-3.2 | 9 | `--------------------------------` |
| llama-3.2 | 9 | `********************************` |
| llama-3.2 | 8 | ` ===============================` |
| llama-3.2 | 5 | ` ###############################` |
| llama-3.2 | 4 | `================================` |
| llama-3.2 | 3 | `//==============================` |
| llama-3.2 | 3 | `/*------------------------------` |
| llama-3.2 | 3 | `//******************************` |
| llama-3.2 | 3 | ` ///////////////////////////////` |
| llama-3.2 | 2 | `#-------------------------------` |
| llama-3.2 | 2 | ` /******************************` |
| qwen3 | 60 | `                                ` |
| qwen3 | 16 | ` -------------------------------` |
| qwen3 | 15 | `////////////////////////////////` |
| qwen3 | 15 | `/*******************************` |
| qwen3 | 14 | `//------------------------------` |
| qwen3 | 12 | ` *******************************` |
| qwen3 | 11 | `################################` |
| qwen3 | 9 | `--------------------------------` |
| qwen3 | 9 | `********************************` |
| qwen3 | 8 | ` ===============================` |
| qwen3 | 5 | ` ###############################` |
| qwen3 | 4 | `================================` |
| qwen3 | 3 | `//==============================` |
| qwen3 | 3 | `/*------------------------------` |
| qwen3 | 3 | `//******************************` |
| qwen3 | 3 | ` ///////////////////////////////` |
| qwen3 | 2 | `#-------------------------------` |
| qwen3 | 2 | ` /******************************` |
| deepseek-v3 | 27 | `                                ` |
| deepseek-v3 | 11 | `................................` |
| deepseek-v3 | 5 | `--------------------------------` |

## Colliding IDs per script class, raw table (all tokenizers)

| script class | P=32 | P=64 |
|---|---|---|
| ASCII | 652 | 475 |
| Whitespace | 228 | 78 |
| Bengali | 63 | 0 |
| Devanagari | 25 | 0 |
| Tamil | 22 | 0 |
| Thai | 20 | 0 |
| Other scripts | 8 | 0 |
| Malayalam | 6 | 0 |
| Latin-ext | 3 | 2 |
| Punctuation/symbols | 4 | 0 |
| Gujarati | 2 | 0 |
| Cyrillic | 2 | 0 |
| CJK Han | 2 | 0 |

## Colliding IDs per script class, decode table (all tokenizers)

| script class | P=32 | P=64 |
|---|---|---|
| CJK Han | 2118 | 2116 |
| Hangul | 959 | 959 |
| Continuation bytes only | 682 | 682 |
| ASCII | 652 | 475 |
| Other scripts | 283 | 275 |
| Mixed | 184 | 184 |
| Punctuation/symbols | 175 | 171 |
| Hebrew | 155 | 155 |
| Whitespace | 228 | 78 |
| Emoji | 151 | 151 |
| Latin-ext | 97 | 96 |
| Invalid UTF-8 byte | 65 | 65 |
| Arabic | 56 | 56 |
| Bengali | 80 | 17 |
| Greek | 39 | 39 |
| Kana | 37 | 37 |
| Cyrillic | 35 | 33 |
| Devanagari | 42 | 17 |
| Private use | 28 | 28 |
| Tamil | 38 | 16 |
| CJK symbols | 26 | 26 |
| Thai | 34 | 14 |
| Malayalam | 22 | 16 |
| Telugu | 19 | 19 |
| Replacement char | 18 | 18 |
| Gurmukhi | 16 | 16 |
| Gujarati | 16 | 14 |
| Kannada | 12 | 12 |
| Oriya | 7 | 7 |
| Combining marks | 6 | 6 |

## Cost

|  | P=32 | P=64 |
|---|---|---|
| P (bytes kept) | 32 | 64 |
| D = 256·P (codec width) | 8,192 | 16,384 |
| codec row, fp32 | 32 KiB | 64 KiB |
| projection params, d_model = 768 | 6.3 M | 12.6 M |
| projection params, d_model = 4096 | 33.6 M | 67.1 M |
| byte buffer, gpt2 (V·P + 2V bytes) | 1.7 MB | 3.3 MB |
| byte buffer, llama-3.2 (V·P + 2V bytes) | 4.4 MB | 8.5 MB |
| byte buffer, qwen3 (V·P + 2V bytes) | 5.2 MB | 10.0 MB |
| byte buffer, gemma-3 (V·P + 2V bytes) | 8.9 MB | 17.3 MB |
| byte buffer, deepseek-v3 (V·P + 2V bytes) | 4.4 MB | 8.5 MB |
| byte buffer, gpt-oss (V·P + 2V bytes) | 6.8 MB | 13.2 MB |

## Status

- `p32`: checks pass; determinism: all hashes match
- `p64`: checks pass; determinism: all hashes match

