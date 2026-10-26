# Collisions in the P = 32 byte tables, per script class

Two token IDs **collide** when their byte rows are identical. By Theorem 1 ([proof.md](proof.md)), they then get the same Kronecker codec row, and so the same input embedding, for every projection and at every training step. This file counts those collisions for the six tokenizers of paper Table 3, in two byte tables:

- **decode table:** what the repo builds today, `build_byte_buffer` → `tokenizer.decode([id])`.
- **raw byte table:** each token's true bytes, read from its vocab piece ([README.md](README.md#the-two-tables)).

Terms:
- A **group** is a set of two or more IDs that share one row.
- **Colliding IDs** is the number of IDs in all groups.
- **Lost IDs** is `V − distinct rows`: how many IDs do not get an embedding of their own. Each group of size `n` loses `n − 1`.

For the same analysis at P = 64, see [p64.md](p64.md).

Every number here comes from `results/p32/` (rendered in [`results/p32/tables.md`](results/p32/tables.md)). The cause of every single group is listed in `results/p32/tables.md` and in `results/p32/<tokenizer>/groups_{decode,raw}.jsonl`.

## Overview

| tokenizer | V | decode: groups | decode: colliding IDs | decode: lost IDs | raw: groups | raw: colliding IDs | raw: lost IDs |
|---|---|---|---|---|---|---|---|
| gpt2 | 50,257 | 14 | 357 | 343 | 7 | 17 | 10 |
| llama-3.2 | 128,256 | 41 | 1,452 | 1,411 | 28 | 223 | 195 |
| qwen3 | 151,669 | 36 | 1,556 | 1,520 | 25 | 209 | 184 |
| gemma-3 | 262,145 | 159 | 336 | 177 | 159 | 336 | 177 |
| deepseek-v3 | 128,815 | 50 | 1,174 | 1,124 | 14 | 68 | 54 |
| gpt-oss | 200,019 | 47 | 1,405 | 1,358 | 29 | 184 | 155 |

- **The byte-level BPE tokenizers lose far fewer IDs with the raw table:** 86–97% fewer, e.g. Qwen3 goes from 1,520 to 184.
- **Gemma's two tables are byte-for-byte identical** (same SHA-256). Its decoder maps `▁` to a space and `<0xNN>` to a byte, and none of its normal tokens is a partial character.
- **No table has an empty row**, so `empty_bytes` never occurs.

## Causes

Each group gets one cause. The rules are applied in this order (`kron_audit/causes.py`, `DEFAULT_RULES`):

| cause | rule | example |
|---|---|---|
| `utf8_replacement` | the shared row contains U+FFFD (`EF BF BD`) and at least one member's true bytes are not valid UTF-8 | GPT-2 IDs 94, 95, 96 … (bytes `A1`, `A2`, `A3` …) all decode to `�` |
| `truncation` | members' true bytes differ, but their first ≤ 32 bytes (cut on a character boundary) are equal | GPT-2 IDs 3880, 10097, 43801, 47232 = 32, 64, 56 and 48 dashes |
| `byte_fallback_alias` | members have identical true bytes, and one of them is a SentencePiece `<0xNN>` token | Gemma ID 248 `<0x0A>` and ID 107 `\n` |
| `decoder_normalization`, `special_literal_clash`, `duplicate_vocab_entry`, `empty_bytes` | (see code) | **never occurred** |

Groups and IDs per cause:

| tokenizer | decode: utf8_replacement | decode: truncation | decode: byte_fallback_alias | raw: truncation | raw: byte_fallback_alias |
|---|---|---|---|---|---|
| gpt2 | 7 groups / 340 IDs | 7 / 17 | – | 7 / 17 | – |
| llama-3.2 | 13 / 1,229 | 28 / 223 | – | 28 / 223 | – |
| qwen3 | 11 / 1,347 | 25 / 209 | – | 25 / 209 | – |
| gemma-3 | – | 49 / 116 | 110 / 220 | 49 / 116 | 110 / 220 |
| deepseek-v3 | 37 / 1,108 | 13 / 66 | – | 14 / 68 | – |
| gpt-oss | 18 / 1,221 | 29 / 184 | – | 29 / 184 | – |

**DeepSeek has one more truncation group in the raw table (14 vs 13).** IDs 70766 and 71586 are long Myanmar tokens whose true bytes begin with a stray continuation byte (`80`).
- In the decode table, that byte becomes the 3-byte U+FFFD, so the two rows end at different places and do not collide by truncation.
- In the raw table, they share a 32-byte prefix.

### Why each cause happens

1. **`utf8_replacement` (decode table only).** Byte-level BPE vocabularies contain tokens that are *pieces* of a multi-byte character. Examples: the lone byte `E4`, the bytes `E2 80`, or `の` followed by `E5`.
   - `tokenizer.decode([id])` cannot print a piece of a character, so the decoder writes U+FFFD in its place.
   - Every token with the same valid context and the same number of broken spots then decodes to the same string: `�`, ` �`, `��`, `の�`, `�다` …
   - The true bytes were all different. The decoder threw the difference away.
   - This is the largest cause by far, at 340–1,347 IDs per byte-level tokenizer.
2. **`truncation` (both tables).** `P = 32` keeps only the first 32 bytes, so tokens that agree on those bytes become one row. Two kinds of token do this:
   - **Long runs**, the large majority: whitespace, `----`, `////`, `/****`, `====`, `____`, `....`. They exist in 32-, 48- and 64-byte versions, and all of them map to the same 32-byte row.
   - **Long words in scripts with 3-byte characters:** Bengali, Devanagari, Tamil and Malayalam (Gemma); Thai, Georgian, Malayalam and Gujarati (gpt-oss). Eleven characters already fill 32 bytes. For example, `▁বিশ্ববিদ্যাল`, `▁বিশ্ববিদ্যালয়` and `▁বিশ্ববিদ্যালয়ের` are 37, 40 and 46 bytes, and all share the row ` বিশ্ববিদ্য`.
3. **`byte_fallback_alias` (Gemma only).** Gemma's SentencePiece vocabulary has 256 byte-fallback tokens `<0x00>`–`<0xFF>`. For 110 of those bytes it also has an ordinary token for the same single character: all 95 printable ASCII characters plus 15 control characters (e.g. `\n`, `\t`). The pair has the same true bytes, so any byte table collides them. The other 146 byte-fallback tokens (mostly `80`–`FF`) have no ordinary twin and stay unique.

## Colliding IDs per script class

Each token's class comes from its true bytes (`kron_audit/script_class.py`).
- A token that holds no complete character (a partial UTF-8 piece) is classed by the code-point range its lead byte allows. For example, `E0 A4` can only begin U+0900–U+093F, so it is Devanagari.
- Below, such fragments are folded into their script.
- **Continuation bytes only** means the token has no lead byte at all, e.g. `A3 8F`.
- **Invalid UTF-8 byte** means bytes that can never start a character (`C0`, `C1`, `F5`–`FF`).
- **Mixed** means a lead byte whose range spans several scripts, e.g. `E2`.

### Decode table

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| CJK Han | 108 | 571 | 570 | 0 | 338 | 531 | 2,118 |
| Hangul | 7 | 249 | 258 | 0 | 205 | 240 | 959 |
| Continuation bytes only | 91 | 193 | 132 | 0 | 119 | 147 | 682 |
| ASCII | 14 | 145 | 145 | 212 | 35 | 101 | 652 |
| Other scripts | 7 | 17 | 131 | 0 | 75 | 53 | 283 |
| Whitespace | 0 | 76 | 60 | 8 | 27 | 57 | 228 |
| Mixed | 23 | 39 | 39 | 0 | 37 | 46 | 184 |
| Punctuation/symbols | 17 | 30 | 50 | 2 | 42 | 34 | 175 |
| Hebrew | 2 | 2 | 4 | 0 | 145 | 2 | 155 |
| Emoji | 12 | 16 | 47 | 0 | 37 | 39 | 151 |
| Latin-ext | 19 | 19 | 18 | 0 | 20 | 21 | 97 |
| Bengali | 1 | 3 | 3 | 63 | 4 | 6 | 80 |
| Invalid UTF-8 byte | 13 | 13 | 13 | 0 | 13 | 13 | 65 |
| Arabic | 6 | 12 | 16 | 0 | 11 | 11 | 56 |
| Devanagari | 3 | 4 | 3 | 25 | 3 | 4 | 42 |
| Greek | 5 | 10 | 8 | 0 | 10 | 6 | 39 |
| Tamil | 0 | 3 | 3 | 22 | 5 | 5 | 38 |
| Kana | 11 | 7 | 11 | 0 | 3 | 5 | 37 |
| Cyrillic | 5 | 9 | 6 | 0 | 8 | 7 | 35 |
| Thai | 2 | 3 | 6 | 2 | 2 | 19 | 34 |
| Private use | 2 | 8 | 3 | 0 | 3 | 12 | 28 |
| CJK symbols | 1 | 5 | 11 | 0 | 4 | 5 | 26 |
| Malayalam | 0 | 2 | 2 | 2 | 6 | 10 | 22 |
| Telugu | 0 | 3 | 3 | 0 | 4 | 9 | 19 |
| Replacement char | 4 | 3 | 3 | 0 | 4 | 4 | 18 |
| Gurmukhi | 3 | 3 | 3 | 0 | 3 | 4 | 16 |
| Gujarati | 0 | 3 | 3 | 0 | 3 | 7 | 16 |
| Kannada | 0 | 3 | 3 | 0 | 3 | 3 | 12 |
| Oriya | 0 | 0 | 1 | 0 | 3 | 3 | 7 |
| Combining marks | 1 | 1 | 1 | 0 | 2 | 1 | 6 |

### Raw table

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| ASCII | 14 | 145 | 145 | 212 | 35 | 101 | 652 |
| Whitespace | 0 | 76 | 60 | 8 | 27 | 57 | 228 |
| Bengali | 0 | 0 | 0 | 63 | 0 | 0 | 63 |
| Devanagari | 0 | 0 | 0 | 25 | 0 | 0 | 25 |
| Tamil | 0 | 0 | 0 | 22 | 0 | 0 | 22 |
| Thai | 0 | 0 | 4 | 2 | 0 | 14 | 20 |
| Other scripts (Georgian, Myanmar) | 0 | 0 | 0 | 0 | 2 | 6 | 8 |
| Malayalam | 0 | 0 | 0 | 2 | 0 | 4 | 6 |
| Punctuation/symbols | 0 | 0 | 0 | 2 | 2 | 0 | 4 |
| Latin-ext | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| CJK Han | 0 | 0 | 0 | 0 | 2 | 0 | 2 |
| Cyrillic | 0 | 2 | 0 | 0 | 0 | 0 | 2 |
| Gujarati | 0 | 0 | 0 | 0 | 0 | 2 | 2 |

### Reading the two tables

- **Decode-table collisions fall mostly on non-Latin scripts.**
  - CJK Han and Hangul alone account for 3,077 colliding IDs across the five byte-level tokenizers.
  - Indic fragments appear in all five byte-level tokenizers: the 3-byte characters `E0 A4 …` (Devanagari), `E0 A6 …` (Bengali), `E0 AE …` (Tamil) and so on each have a few fragment tokens in the vocab, and the decoder folds them all into `�` / ` �`. GPT-2's smaller vocab has only Devanagari, Bengali and Gurmukhi pieces.
  - These collisions come from the decoder, not from the scripts themselves. In the raw table, every CJK, Hangul, Hebrew, Arabic, emoji and fragment collision disappears.
- **Raw-table collisions are mostly ASCII and whitespace** (880 of 1,037 colliding IDs across all six). Apart from Gemma's 212 byte-fallback IDs, these are long runs (`----`, `////`, spaces). Those tokens are rare in text, and the shared 32-byte row is a fair summary of them.
- **The raw-table collisions that matter are real words truncated at 32 bytes:** Gemma's Bengali, Devanagari and Tamil words, and gpt-oss's Thai, Malayalam, Gujarati and Georgian words. They are the Indic case paper §4.2 mentions, and they are why its "distinct embeddings" claim fails (Theorem 1(c)).
- **Gemma's 110 byte-fallback aliases are true duplicates**, not a byte-table bug. Separating them would need a marker that the two IDs come from different paths, which the codec has no slot for.

## Notable groups (one line each)

| tokenizer | table | size | cause | shared row | what the members are |
|---|---|---|---|---|---|
| qwen3 | decode | 1,067 | utf8_replacement | `�` | every lone-byte or partial-character token with no valid context |
| deepseek-v3 | decode | 692 | utf8_replacement | `�` | same |
| gpt-oss | decode | 689 | utf8_replacement | `�` | same |
| llama-3.2 | decode | 434 | utf8_replacement | ` �` | space + a partial character, e.g. `Ġ` + `E2 80`, `Ġ` + `D0` |
| deepseek-v3 | decode | 10, 10, 10, 9 … (24 groups) | utf8_replacement | `�ר`, `�ה`, `�ת`, `�ל` … | Hebrew letter + the tail byte of the previous letter; the tail decodes to U+FFFD |
| llama-3.2 | decode | 5 | utf8_replacement | `�다` | Korean `다` preceded by different stray bytes |
| llama-3.2 / qwen3 | both | 60 | truncation | 32 spaces | space runs of 32 bytes and longer |
| gpt2 | both | 3 | truncation | `ÃÂÃÂ…` | mojibake (double-encoded UTF-8) runs of 32, 64 and 128 bytes |
| gemma-3 | both | 5 | truncation | ` বিশ্ববিদ্য` | Bengali "university" and its inflections, 37–46 bytes |
| gpt-oss | both | 3 | truncation | ` საქართველო` | Georgian "Georgia" and two longer forms |
| deepseek-v3 | both | 2 | truncation | `习近平新时代中国特色` | two Chinese political phrases, 42 and 48 bytes |
| gemma-3 | both | 2 | byte_fallback_alias | `\n` | IDs 107 (`\n`) and 248 (`<0x0A>`) |

## What this means

1. **Build the byte buffer from raw bytes, not from `decode`.** It removes every `utf8_replacement` collision, cutting lost IDs by 86–97% on the five byte-level tokenizers (343 → 10, 1,411 → 195, 1,520 → 184, 1,124 → 54, 1,358 → 155). It is a byte-table change only; the codec and the lemmas stay the same. For byte-level BPE, the raw bytes are one inverse lookup per piece character (`kron_audit/raw_bytes.py`).
2. **Truncation at P = 32 still merges 54–195 IDs per tokenizer**, mostly long punctuation and whitespace runs, plus long Indic, Thai and Georgian words. The paper's "distinct embeddings after truncation" sentence should be qualified (Theorem 1(c)). If those words matter, the options are a larger `P` or a tie-break for tokens over 32 bytes.
3. **Gemma's byte-fallback aliases (110 pairs) can't be removed** by changing the byte table. They are the only collisions where the two IDs truly mean the same bytes.
