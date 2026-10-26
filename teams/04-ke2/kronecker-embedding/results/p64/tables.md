# Generated tables — run `p64` (P = 64, D = 16,384)

Rendered by `python -m kron_audit report` from this folder. Do not edit by hand.

## Overview

`lost` = V − distinct rows = IDs that do not get their own codec row.

| tokenizer | V | family | decode groups | decode colliding IDs | decode lost | raw groups | raw colliding IDs | raw lost | L1/L2/T1/modes |
|---|---|---|---|---|---|---|---|---|---|
| gpt2 | 50,257 | bbpe | 8 | 342 | 334 | 1 | 2 | 1 | pass |
| llama-3.2 | 128,256 | bbpe | 31 | 1,347 | 1,316 | 18 | 118 | 100 | pass |
| qwen3 | 151,669 | bbpe | 29 | 1,465 | 1,436 | 18 | 118 | 100 | pass |
| gemma-3 | 262,145 | sentencepiece | 110 | 220 | 110 | 110 | 220 | 110 | pass |
| deepseek-v3 | 128,815 | bbpe | 41 | 1,120 | 1,079 | 5 | 14 | 9 | pass |
| gpt-oss | 200,019 | bbpe | 29 | 1,304 | 1,275 | 11 | 83 | 72 | pass |

## Collisions by cause

| tokenizer | table | cause | groups | tokens |
|---|---|---|---|---|
| gpt2 | decode | utf8_replacement | 7 | 340 |
| gpt2 | decode | truncation | 1 | 2 |
| gpt2 | raw | truncation | 1 | 2 |
| llama-3.2 | decode | utf8_replacement | 13 | 1229 |
| llama-3.2 | decode | truncation | 18 | 118 |
| llama-3.2 | raw | truncation | 18 | 118 |
| qwen3 | decode | utf8_replacement | 11 | 1347 |
| qwen3 | decode | truncation | 18 | 118 |
| qwen3 | raw | truncation | 18 | 118 |
| gemma-3 | decode | byte_fallback_alias | 110 | 220 |
| gemma-3 | raw | byte_fallback_alias | 110 | 220 |
| deepseek-v3 | decode | utf8_replacement | 36 | 1106 |
| deepseek-v3 | decode | truncation | 5 | 14 |
| deepseek-v3 | raw | truncation | 5 | 14 |
| gpt-oss | decode | utf8_replacement | 18 | 1221 |
| gpt-oss | decode | truncation | 11 | 83 |
| gpt-oss | raw | truncation | 11 | 83 |

## Tokens longer than P = 64

| tokenizer | tokens > 64 bytes | of these, sharing a row |
|---|---|---|
| gpt2 | 3 | 1 |
| llama-3.2 | 123 | 112 |
| qwen3 | 121 | 112 |
| gemma-3 | 0 | 0 |
| deepseek-v3 | 13 | 10 |
| gpt-oss | 85 | 77 |

## Colliding token IDs per script class — decode table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| CJK Han | 108 | 571 | 570 | 0 | 336 | 531 | 2116 |
| Hangul | 7 | 249 | 258 | 0 | 205 | 240 | 959 |
| Continuation bytes only | 91 | 193 | 132 | 0 | 119 | 147 | 682 |
| ASCII | 0 | 95 | 95 | 212 | 11 | 62 | 475 |
| Other scripts | 7 | 17 | 131 | 0 | 73 | 47 | 275 |
| Mixed | 23 | 39 | 39 | 0 | 37 | 46 | 184 |
| Punctuation/symbols | 17 | 30 | 50 | 0 | 40 | 34 | 171 |
| Hebrew | 2 | 2 | 4 | 0 | 145 | 2 | 155 |
| Emoji | 12 | 16 | 47 | 0 | 37 | 39 | 151 |
| Latin-ext | 18 | 19 | 18 | 0 | 20 | 21 | 96 |
| Whitespace | 0 | 23 | 23 | 8 | 3 | 21 | 78 |
| Invalid UTF-8 byte | 13 | 13 | 13 | 0 | 13 | 13 | 65 |
| Arabic | 6 | 12 | 16 | 0 | 11 | 11 | 56 |
| Greek | 5 | 10 | 8 | 0 | 10 | 6 | 39 |
| Kana | 11 | 7 | 11 | 0 | 3 | 5 | 37 |
| Cyrillic | 5 | 7 | 6 | 0 | 8 | 7 | 33 |
| Private use | 2 | 8 | 3 | 0 | 3 | 12 | 28 |
| CJK symbols | 1 | 5 | 11 | 0 | 4 | 5 | 26 |
| Telugu | 0 | 3 | 3 | 0 | 4 | 9 | 19 |
| Replacement char | 4 | 3 | 3 | 0 | 4 | 4 | 18 |
| Devanagari | 3 | 4 | 3 | 0 | 3 | 4 | 17 |
| Bengali | 1 | 3 | 3 | 0 | 4 | 6 | 17 |
| Gurmukhi | 3 | 3 | 3 | 0 | 3 | 4 | 16 |
| Tamil | 0 | 3 | 3 | 0 | 5 | 5 | 16 |
| Malayalam | 0 | 2 | 2 | 0 | 6 | 6 | 16 |
| Thai | 2 | 3 | 2 | 0 | 2 | 5 | 14 |
| Gujarati | 0 | 3 | 3 | 0 | 3 | 5 | 14 |
| Kannada | 0 | 3 | 3 | 0 | 3 | 3 | 12 |
| Oriya | 0 | 0 | 1 | 0 | 3 | 3 | 7 |
| Combining marks | 1 | 1 | 1 | 0 | 2 | 1 | 6 |

## Colliding token IDs per script class — raw table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| ASCII | 0 | 95 | 95 | 212 | 11 | 62 | 475 |
| Whitespace | 0 | 23 | 23 | 8 | 3 | 21 | 78 |
| Latin-ext | 2 | 0 | 0 | 0 | 0 | 0 | 2 |

## gpt2

Source `openai-community/gpt2` (hf), snapshot `607a30d783dfa663caf39e06633721c8d4cfcd7e`, family `bbpe`.

- V = 50,257; raw rows by rule: model_bbpe 50,256, special 1
- rows where decode bytes ≠ raw bytes: 344; raw rows that are not valid UTF-8: 344
- tokens longer than 64 bytes: 3; of these, sharing a row with another token: 1
- decode table SHA-256 `0ec79d2ef48432eeced7b788544891df039ad8835df260b70180a8695d015384`
- raw table SHA-256 `33cc5f9de4daf911ca02e76cde1418777b4429737e99fae9f64c821760e1c1ce`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation |
|---|---|---|---|---|---|
| CJK Han (fragment) | 104 | 104 | 4 | 104 / 4 | 0 / 0 |
| Continuation bytes only | 91 | 91 | 2 | 91 / 2 | 0 / 0 |
| Mixed (fragment) | 23 | 23 | 2 | 23 / 2 | 0 / 0 |
| Punctuation/symbols (fragment) | 17 | 17 | 2 | 17 / 2 | 0 / 0 |
| Latin-ext (fragment) | 16 | 16 | 2 | 16 / 2 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| Emoji (fragment) | 12 | 12 | 2 | 12 / 2 | 0 / 0 |
| Hangul (fragment) | 7 | 7 | 2 | 7 / 2 | 0 / 0 |
| Other scripts (fragment) | 7 | 7 | 1 | 7 / 1 | 0 / 0 |
| Arabic (fragment) | 6 | 6 | 2 | 6 / 2 | 0 / 0 |
| Kana (fragment) | 6 | 6 | 2 | 6 / 2 | 0 / 0 |
| Kana | 133 | 5 | 1 | 5 / 1 | 0 / 0 |
| Cyrillic (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Greek (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| CJK Han | 50 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 8 | 4 | 4 | 4 / 4 | 0 / 0 |
| Devanagari (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Latin-ext | 148 | 2 | 1 | 0 / 0 | 2 / 1 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Private use (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |
| Thai (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |
| Bengali (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |
| CJK symbols (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |
| Combining marks (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 255 | utf8_replacement | `�` | 3 | 94, 95, 96, 97, 98, 99 … |
| 1 | 43 | utf8_replacement | ` �` | 4 | 564, 1587, 2343, 5525, 6184, 7377 … |
| 2 | 31 | utf8_replacement | `��` | 6 | 4204, 6353, 6408, 7134, 8008, 8955 … |
| 3 | 5 | utf8_replacement | `の�` | 6 | 15474, 17683, 27032, 33426, 49149 |
| 4 | 2 | utf8_replacement | `龍�` | 6 | 19049, 39820 |
| 5 | 2 | utf8_replacement | ` 裏�` | 7 | 20174, 34504 |
| 6 | 2 | truncation | `ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ` | 64 | 23090, 35496 |
| 7 | 2 | utf8_replacement | `���` | 9 | 47490, 48585 |

All 8 groups. Member pieces and hex bytes: `gpt2/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation |
|---|---|---|---|---|
| Latin-ext | 148 | 2 | 1 | 2 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 2 | truncation | `ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ` | 64 | 23090, 35496 |

All 1 groups. Member pieces and hex bytes: `gpt2/groups_raw.jsonl`.

## llama-3.2

Source `unsloth/Llama-3.2-1B` (hf), snapshot `9535bd9b1d1dea6acafbdc4813b728796aeb28da`, family `bbpe`.

- V = 128,256; raw rows by rule: added_literal 253, model_bbpe 128,000, special 3
- rows where decode bytes ≠ raw bytes: 1,352; raw rows that are not valid UTF-8: 1,352
- tokens longer than 64 bytes: 123; of these, sharing a row with another token: 112
- decode table SHA-256 `7d5372cd7d25dc4d813ca1bd998c7b595a39a7ce9d091fdc23a4fc6a153ec1ef`
- raw table SHA-256 `d8c70d202337b139f1194a123eee866ce867e9674199546414c59158e3b52fd7`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation |
|---|---|---|---|---|---|
| CJK Han (fragment) | 569 | 569 | 2 | 569 / 2 | 0 / 0 |
| Hangul (fragment) | 240 | 240 | 2 | 240 / 2 | 0 / 0 |
| Continuation bytes only | 198 | 193 | 6 | 193 / 6 | 0 / 0 |
| ASCII | 97461 | 95 | 17 | 0 / 0 | 95 / 17 |
| Mixed (fragment) | 39 | 39 | 3 | 39 / 3 | 0 / 0 |
| Punctuation/symbols (fragment) | 31 | 30 | 2 | 30 / 2 | 0 / 0 |
| Whitespace | 530 | 23 | 1 | 0 / 0 | 23 / 1 |
| Latin-ext (fragment) | 31 | 19 | 2 | 19 / 2 | 0 / 0 |
| Other scripts (fragment) | 17 | 17 | 3 | 17 / 3 | 0 / 0 |
| Emoji (fragment) | 16 | 16 | 2 | 16 / 2 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| Arabic (fragment) | 10 | 10 | 2 | 10 / 2 | 0 / 0 |
| Greek (fragment) | 10 | 10 | 2 | 10 / 2 | 0 / 0 |
| Hangul | 2293 | 9 | 3 | 9 / 3 | 0 / 0 |
| Private use (fragment) | 8 | 8 | 2 | 8 / 2 | 0 / 0 |
| Cyrillic (fragment) | 7 | 7 | 2 | 7 / 2 | 0 / 0 |
| CJK symbols (fragment) | 6 | 5 | 2 | 5 / 2 | 0 / 0 |
| Kana (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Devanagari (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 9 | 3 | 3 | 3 / 3 | 0 / 0 |
| Bengali (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gujarati (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Kannada (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Tamil (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Telugu (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Thai (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| CJK Han | 4284 | 2 | 1 | 2 / 1 | 0 / 0 |
| Arabic | 3788 | 2 | 1 | 2 / 1 | 0 / 0 |
| Kana | 1019 | 2 | 1 | 2 / 1 | 0 / 0 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Malayalam (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |
| Combining marks (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 647 | utf8_replacement | `�` | 3 | 94, 95, 96, 97, 98, 99 … |
| 1 | 434 | utf8_replacement | ` �` | 4 | 639, 1301, 1717, 2188, 2928, 3396 … |
| 2 | 117 | utf8_replacement | `��` | 6 | 3299, 7644, 10178, 16050, 16281, 19044 … |
| 3 | 23 | truncation | `                                        …` | 64 | 5351, 14984, 19829, 23136, 38244, 39271 … |
| 4 | 13 | truncation | ` ---------------------------------------…` | 64 | 8633, 24793, 40473, 52914, 60909, 64638 … |
| 5 | 12 | truncation | `//--------------------------------------…` | 64 | 10089, 18498, 45242, 46914, 51661, 57442 … |
| 6 | 11 | truncation | `/***************************************…` | 64 | 11624, 20766, 23381, 37813, 54296, 59107 … |
| 7 | 10 | truncation | `////////////////////////////////////////…` | 64 | 10023, 28282, 29326, 36209, 44300, 59969 … |
| 8 | 8 | truncation | ` ***************************************…` | 64 | 10757, 17994, 23089, 29744, 77650, 80471 … |
| 9 | 7 | truncation | `----------------------------------------…` | 64 | 3597, 23151, 26972, 44549, 54364, 63217 … |
| 10 | 6 | truncation | `########################################…` | 64 | 13367, 33141, 41586, 70161, 80548, 91830 |
| 11 | 5 | truncation | `****************************************…` | 64 | 4169, 5713, 34618, 62793, 80503 |
| 12 | 5 | truncation | ` =======================================…` | 64 | 16563, 39468, 67000, 83149, 90418 |
| 13 | 5 | utf8_replacement | `�다` | 6 | 20541, 104828, 112039, 117653, 123375 |
| 14 | 5 | utf8_replacement | `�i` | 4 | 100309, 100646, 103180, 103965, 104789 |
| 15 | 5 | utf8_replacement | `�ng` | 5 | 105394, 107280, 107454, 112245, 117523 |
| 16 | 4 | utf8_replacement | `�n` | 4 | 100859, 100938, 101792, 111972 |
| 17 | 3 | truncation | ` #######################################…` | 64 | 49597, 87300, 94958 |
| 18 | 3 | truncation | `//**************************************…` | 64 | 56363, 65326, 66180 |
| 19 | 2 | truncation | `========================================…` | 64 | 8315, 64494 |
| 20 | 2 | truncation | `//======================================…` | 64 | 24036, 95403 |
| 21 | 2 | utf8_replacement | `ー�` | 6 | 25005, 38248 |
| 22 | 2 | utf8_replacement | `�数` | 6 | 28359, 31041 |
| 23 | 2 | truncation | `/*--------------------------------------…` | 64 | 30965, 59006 |
| 24 | 2 | utf8_replacement | `��이` | 9 | 47318, 70483 |
| 25 | 2 | truncation | `#---------------------------------------…` | 64 | 62015, 76610 |
| 26 | 2 | utf8_replacement | `�이` | 6 | 63718, 103618 |
| 27 | 2 | utf8_replacement | `ا�` | 5 | 69350, 100257 |
| 28 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 72608, 96280 |
| 29 | 2 | truncation | ` /**************************************…` | 64 | 98105, 100089 |
| 30 | 2 | utf8_replacement | `�a` | 4 | 103497, 112865 |

All 31 groups. Member pieces and hex bytes: `llama-3.2/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation |
|---|---|---|---|---|
| ASCII | 97461 | 95 | 17 | 95 / 17 |
| Whitespace | 530 | 23 | 1 | 23 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 23 | truncation | `                                        …` | 64 | 5351, 14984, 19829, 23136, 38244, 39271 … |
| 1 | 13 | truncation | ` ---------------------------------------…` | 64 | 8633, 24793, 40473, 52914, 60909, 64638 … |
| 2 | 12 | truncation | `//--------------------------------------…` | 64 | 10089, 18498, 45242, 46914, 51661, 57442 … |
| 3 | 11 | truncation | `/***************************************…` | 64 | 11624, 20766, 23381, 37813, 54296, 59107 … |
| 4 | 10 | truncation | `////////////////////////////////////////…` | 64 | 10023, 28282, 29326, 36209, 44300, 59969 … |
| 5 | 8 | truncation | ` ***************************************…` | 64 | 10757, 17994, 23089, 29744, 77650, 80471 … |
| 6 | 7 | truncation | `----------------------------------------…` | 64 | 3597, 23151, 26972, 44549, 54364, 63217 … |
| 7 | 6 | truncation | `########################################…` | 64 | 13367, 33141, 41586, 70161, 80548, 91830 |
| 8 | 5 | truncation | `****************************************…` | 64 | 4169, 5713, 34618, 62793, 80503 |
| 9 | 5 | truncation | ` =======================================…` | 64 | 16563, 39468, 67000, 83149, 90418 |
| 10 | 3 | truncation | ` #######################################…` | 64 | 49597, 87300, 94958 |
| 11 | 3 | truncation | `//**************************************…` | 64 | 56363, 65326, 66180 |
| 12 | 2 | truncation | `========================================…` | 64 | 8315, 64494 |
| 13 | 2 | truncation | `//======================================…` | 64 | 24036, 95403 |
| 14 | 2 | truncation | `/*--------------------------------------…` | 64 | 30965, 59006 |
| 15 | 2 | truncation | `#---------------------------------------…` | 64 | 62015, 76610 |
| 16 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 72608, 96280 |
| 17 | 2 | truncation | ` /**************************************…` | 64 | 98105, 100089 |

All 18 groups. Member pieces and hex bytes: `llama-3.2/groups_raw.jsonl`.

## qwen3

Source `Qwen/Qwen3-32B` (hf), snapshot `9216db5781bf21249d130ec9da846c4624c16137`, family `bbpe`.

- V = 151,669; raw rows by rule: added_literal 12, model_bbpe 151,643, special 14
- rows where decode bytes ≠ raw bytes: 1,448; raw rows that are not valid UTF-8: 1,448
- tokens longer than 64 bytes: 121; of these, sharing a row with another token: 112
- decode table SHA-256 `6022214773e806ba281c5bfd094546f14173a100b8b9a9db40edb0bcabbddaed`
- raw table SHA-256 `927e0f0063c4443f9f016f8ebe328e7ab1105f1d5c6b6b7852711956dbfab1ce`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation |
|---|---|---|---|---|---|
| CJK Han (fragment) | 565 | 565 | 2 | 565 / 2 | 0 / 0 |
| Hangul (fragment) | 254 | 254 | 2 | 254 / 2 | 0 / 0 |
| Continuation bytes only | 132 | 132 | 2 | 132 / 2 | 0 / 0 |
| Other scripts (fragment) | 131 | 131 | 3 | 131 / 3 | 0 / 0 |
| ASCII | 93929 | 95 | 17 | 0 / 0 | 95 / 17 |
| Punctuation/symbols (fragment) | 51 | 50 | 2 | 50 / 2 | 0 / 0 |
| Emoji (fragment) | 47 | 47 | 2 | 47 / 2 | 0 / 0 |
| Mixed (fragment) | 39 | 39 | 3 | 39 / 3 | 0 / 0 |
| Whitespace | 441 | 23 | 1 | 0 / 0 | 23 / 1 |
| Latin-ext (fragment) | 19 | 18 | 2 | 18 / 2 | 0 / 0 |
| Arabic (fragment) | 16 | 16 | 2 | 16 / 2 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| CJK symbols (fragment) | 11 | 11 | 2 | 11 / 2 | 0 / 0 |
| Greek (fragment) | 8 | 8 | 2 | 8 / 2 | 0 / 0 |
| Kana | 1841 | 6 | 3 | 6 / 3 | 0 / 0 |
| Cyrillic (fragment) | 6 | 6 | 2 | 6 / 2 | 0 / 0 |
| CJK Han | 25882 | 5 | 2 | 5 / 2 | 0 / 0 |
| Kana (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Hangul | 3589 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 9 | 3 | 3 | 3 / 3 | 0 / 0 |
| Bengali (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Devanagari (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gujarati (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Kannada (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Private use (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Tamil (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Telugu (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Hebrew | 3164 | 2 | 1 | 2 / 1 | 0 / 0 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Malayalam (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |
| Thai (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |
| Combining marks (fragment) | 2 | 1 | 1 | 1 / 1 | 0 / 0 |
| Oriya (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 1067 | utf8_replacement | `�` | 3 | 94, 95, 96, 97, 98, 99 … |
| 1 | 191 | utf8_replacement | ` �` | 4 | 636, 1278, 1683, 2139, 2858, 3315 … |
| 2 | 72 | utf8_replacement | `��` | 6 | 3219, 7492, 9973, 15675, 15902, 18535 … |
| 3 | 23 | truncation | `                                        …` | 64 | 5238, 14642, 19273, 22335, 37144, 38171 … |
| 4 | 13 | truncation | ` ---------------------------------------…` | 64 | 8466, 23852, 39373, 51814, 59809, 63538 … |
| 5 | 12 | truncation | `//--------------------------------------…` | 64 | 9888, 18012, 44142, 45814, 50561, 56342 … |
| 6 | 11 | truncation | `/***************************************…` | 64 | 11370, 20159, 22565, 36713, 53196, 58007 … |
| 7 | 10 | truncation | `////////////////////////////////////////…` | 64 | 9822, 27183, 28226, 35109, 43200, 58869 … |
| 8 | 8 | truncation | ` ***************************************…` | 64 | 10534, 17535, 22292, 28644, 76550, 79371 … |
| 9 | 7 | truncation | `----------------------------------------…` | 64 | 3513, 22349, 25885, 43449, 53264, 62117 … |
| 10 | 6 | truncation | `########################################…` | 64 | 13067, 32041, 40486, 69061, 79448, 90730 |
| 11 | 5 | truncation | `****************************************…` | 64 | 4077, 5596, 33518, 61693, 79403 |
| 12 | 5 | truncation | ` =======================================…` | 64 | 16168, 38368, 65900, 82049, 89318 |
| 13 | 3 | truncation | ` #######################################…` | 64 | 48497, 86200, 93858 |
| 14 | 3 | truncation | `//**************************************…` | 64 | 55263, 64226, 65080 |
| 15 | 3 | utf8_replacement | `珊�` | 6 | 119346, 119347, 119348 |
| 16 | 2 | truncation | `========================================…` | 64 | 8152, 63394 |
| 17 | 2 | truncation | `//======================================…` | 64 | 23161, 94303 |
| 18 | 2 | utf8_replacement | `ー�` | 6 | 24041, 37148 |
| 19 | 2 | utf8_replacement | `�数` | 6 | 27260, 29941 |
| 20 | 2 | truncation | `/*--------------------------------------…` | 64 | 29865, 57906 |
| 21 | 2 | utf8_replacement | `ו�` | 5 | 36669, 127572 |
| 22 | 2 | utf8_replacement | `��이` | 9 | 46218, 69383 |
| 23 | 2 | truncation | `#---------------------------------------…` | 64 | 60915, 75510 |
| 24 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 71508, 95180 |
| 25 | 2 | truncation | ` /**************************************…` | 64 | 97005, 98989 |
| 26 | 2 | utf8_replacement | `に�` | 6 | 127124, 137973 |
| 27 | 2 | utf8_replacement | `ご�` | 6 | 135078, 139816 |
| 28 | 2 | utf8_replacement | ` 오�` | 7 | 142209, 142210 |

All 29 groups. Member pieces and hex bytes: `qwen3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation |
|---|---|---|---|---|
| ASCII | 93929 | 95 | 17 | 95 / 17 |
| Whitespace | 441 | 23 | 1 | 23 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 23 | truncation | `                                        …` | 64 | 5238, 14642, 19273, 22335, 37144, 38171 … |
| 1 | 13 | truncation | ` ---------------------------------------…` | 64 | 8466, 23852, 39373, 51814, 59809, 63538 … |
| 2 | 12 | truncation | `//--------------------------------------…` | 64 | 9888, 18012, 44142, 45814, 50561, 56342 … |
| 3 | 11 | truncation | `/***************************************…` | 64 | 11370, 20159, 22565, 36713, 53196, 58007 … |
| 4 | 10 | truncation | `////////////////////////////////////////…` | 64 | 9822, 27183, 28226, 35109, 43200, 58869 … |
| 5 | 8 | truncation | ` ***************************************…` | 64 | 10534, 17535, 22292, 28644, 76550, 79371 … |
| 6 | 7 | truncation | `----------------------------------------…` | 64 | 3513, 22349, 25885, 43449, 53264, 62117 … |
| 7 | 6 | truncation | `########################################…` | 64 | 13067, 32041, 40486, 69061, 79448, 90730 |
| 8 | 5 | truncation | `****************************************…` | 64 | 4077, 5596, 33518, 61693, 79403 |
| 9 | 5 | truncation | ` =======================================…` | 64 | 16168, 38368, 65900, 82049, 89318 |
| 10 | 3 | truncation | ` #######################################…` | 64 | 48497, 86200, 93858 |
| 11 | 3 | truncation | `//**************************************…` | 64 | 55263, 64226, 65080 |
| 12 | 2 | truncation | `========================================…` | 64 | 8152, 63394 |
| 13 | 2 | truncation | `//======================================…` | 64 | 23161, 94303 |
| 14 | 2 | truncation | `/*--------------------------------------…` | 64 | 29865, 57906 |
| 15 | 2 | truncation | `#---------------------------------------…` | 64 | 60915, 75510 |
| 16 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 71508, 95180 |
| 17 | 2 | truncation | ` /**************************************…` | 64 | 97005, 98989 |

All 18 groups. Member pieces and hex bytes: `qwen3/groups_raw.jsonl`.

## gemma-3

Source `unsloth/gemma-3-1b-pt` (hf), snapshot `34a98bf3eaecc08c699516f625eb5e56e4c5d99d`, family `sentencepiece`.

- V = 262,145; raw rows by rule: byte_fallback 256, model_sentencepiece 261,881, special 8
- rows where decode bytes ≠ raw bytes: 0; raw rows that are not valid UTF-8: 128
- tokens longer than 64 bytes: 0; of these, sharing a row with another token: 0
- decode table SHA-256 `a9183760fd6cf35e29eb6c9965917f5a0c7a5873a97860a0e7655d7e5c322960`
- raw table SHA-256 `a9183760fd6cf35e29eb6c9965917f5a0c7a5873a97860a0e7655d7e5c322960`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | byte_fallback_alias |
|---|---|---|---|---|
| ASCII | 150314 | 212 | 106 | 212 / 106 |
| Whitespace | 104 | 8 | 4 | 8 / 4 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 2 | byte_fallback_alias | `\n` | 1 | 107, 248 |
| 1 | 2 | byte_fallback_alias | `` | 1 | 239, 249732 |
| 2 | 2 | byte_fallback_alias | `` | 1 | 240, 241247 |
| 3 | 2 | byte_fallback_alias | `` | 1 | 241, 247953 |
| 4 | 2 | byte_fallback_alias | `` | 1 | 243, 251303 |
| 5 | 2 | byte_fallback_alias | `` | 1 | 246, 243480 |
| 6 | 2 | byte_fallback_alias | `\t` | 1 | 247, 255968 |
| 7 | 2 | byte_fallback_alias | `` | 1 | 256, 248894 |
| 8 | 2 | byte_fallback_alias | `` | 1 | 257, 252295 |
| 9 | 2 | byte_fallback_alias | `` | 1 | 258, 255321 |
| 10 | 2 | byte_fallback_alias | `` | 1 | 261, 252786 |
| 11 | 2 | byte_fallback_alias | `` | 1 | 264, 255485 |
| 12 | 2 | byte_fallback_alias | `` | 1 | 265, 239473 |
| 13 | 2 | byte_fallback_alias | `` | 1 | 269, 253998 |
| 14 | 2 | byte_fallback_alias | ` ` | 1 | 270, 236743 |
| 15 | 2 | byte_fallback_alias | `!` | 1 | 271, 236888 |
| 16 | 2 | byte_fallback_alias | `"` | 1 | 272, 236775 |
| 17 | 2 | byte_fallback_alias | `#` | 1 | 273, 236865 |
| 18 | 2 | byte_fallback_alias | `$` | 1 | 274, 236795 |
| 19 | 2 | byte_fallback_alias | `%` | 1 | 275, 236908 |
| 20 | 2 | byte_fallback_alias | `&` | 1 | 276, 236880 |
| 21 | 2 | byte_fallback_alias | `'` | 1 | 277, 236789 |
| 22 | 2 | byte_fallback_alias | `(` | 1 | 278, 236769 |
| 23 | 2 | byte_fallback_alias | `)` | 1 | 279, 236768 |
| 24 | 2 | byte_fallback_alias | `*` | 1 | 280, 236829 |
| 25 | 2 | byte_fallback_alias | `+` | 1 | 281, 236862 |
| 26 | 2 | byte_fallback_alias | `,` | 1 | 282, 236764 |
| 27 | 2 | byte_fallback_alias | `-` | 1 | 283, 236772 |
| 28 | 2 | byte_fallback_alias | `.` | 1 | 284, 236761 |
| 29 | 2 | byte_fallback_alias | `/` | 1 | 285, 236786 |
| 30 | 2 | byte_fallback_alias | `0` | 1 | 286, 236771 |
| 31 | 2 | byte_fallback_alias | `1` | 1 | 287, 236770 |
| 32 | 2 | byte_fallback_alias | `2` | 1 | 288, 236778 |
| 33 | 2 | byte_fallback_alias | `3` | 1 | 289, 236800 |
| 34 | 2 | byte_fallback_alias | `4` | 1 | 290, 236812 |
| 35 | 2 | byte_fallback_alias | `5` | 1 | 291, 236810 |
| 36 | 2 | byte_fallback_alias | `6` | 1 | 292, 236825 |
| 37 | 2 | byte_fallback_alias | `7` | 1 | 293, 236832 |
| 38 | 2 | byte_fallback_alias | `8` | 1 | 294, 236828 |
| 39 | 2 | byte_fallback_alias | `9` | 1 | 295, 236819 |
| 40 | 2 | byte_fallback_alias | `:` | 1 | 296, 236787 |
| 41 | 2 | byte_fallback_alias | `;` | 1 | 297, 236793 |
| 42 | 2 | byte_fallback_alias | `<` | 1 | 298, 236820 |
| 43 | 2 | byte_fallback_alias | `=` | 1 | 299, 236784 |
| 44 | 2 | byte_fallback_alias | `>` | 1 | 300, 236813 |
| 45 | 2 | byte_fallback_alias | `?` | 1 | 301, 236881 |
| 46 | 2 | byte_fallback_alias | `@` | 1 | 302, 236940 |
| 47 | 2 | byte_fallback_alias | `A` | 1 | 303, 236776 |
| 48 | 2 | byte_fallback_alias | `B` | 1 | 304, 236799 |
| 49 | 2 | byte_fallback_alias | `C` | 1 | 305, 236780 |
| 50 | 2 | byte_fallback_alias | `D` | 1 | 306, 236796 |
| 51 | 2 | byte_fallback_alias | `E` | 1 | 307, 236788 |
| 52 | 2 | byte_fallback_alias | `F` | 1 | 308, 236811 |
| 53 | 2 | byte_fallback_alias | `G` | 1 | 309, 236823 |
| 54 | 2 | byte_fallback_alias | `H` | 1 | 310, 236814 |
| 55 | 2 | byte_fallback_alias | `I` | 1 | 311, 236777 |
| 56 | 2 | byte_fallback_alias | `J` | 1 | 312, 236863 |
| 57 | 2 | byte_fallback_alias | `K` | 1 | 313, 236855 |
| 58 | 2 | byte_fallback_alias | `L` | 1 | 314, 236798 |
| 59 | 2 | byte_fallback_alias | `M` | 1 | 315, 236792 |
| 60 | 2 | byte_fallback_alias | `N` | 1 | 316, 236797 |
| 61 | 2 | byte_fallback_alias | `O` | 1 | 317, 236806 |
| 62 | 2 | byte_fallback_alias | `P` | 1 | 318, 236791 |
| 63 | 2 | byte_fallback_alias | `Q` | 1 | 319, 236935 |
| 64 | 2 | byte_fallback_alias | `R` | 1 | 320, 236794 |
| 65 | 2 | byte_fallback_alias | `S` | 1 | 321, 236773 |
| 66 | 2 | byte_fallback_alias | `T` | 1 | 322, 236774 |
| 67 | 2 | byte_fallback_alias | `U` | 1 | 323, 236836 |
| 68 | 2 | byte_fallback_alias | `V` | 1 | 324, 236847 |
| 69 | 2 | byte_fallback_alias | `W` | 1 | 325, 236824 |
| 70 | 2 | byte_fallback_alias | `X` | 1 | 326, 236917 |
| 71 | 2 | byte_fallback_alias | `Y` | 1 | 327, 236874 |
| 72 | 2 | byte_fallback_alias | `Z` | 1 | 328, 236953 |
| 73 | 2 | byte_fallback_alias | `[` | 1 | 329, 236840 |
| 74 | 2 | byte_fallback_alias | `\` | 1 | 330, 236785 |
| 75 | 2 | byte_fallback_alias | `]` | 1 | 331, 236842 |
| 76 | 2 | byte_fallback_alias | `^` | 1 | 332, 236884 |
| 77 | 2 | byte_fallback_alias | `_` | 1 | 333, 236779 |
| 78 | 2 | byte_fallback_alias | `'` | 1 | 334, 236929 |
| 79 | 2 | byte_fallback_alias | `a` | 1 | 335, 236746 |
| 80 | 2 | byte_fallback_alias | `b` | 1 | 336, 236763 |
| 81 | 2 | byte_fallback_alias | `c` | 1 | 337, 236755 |
| 82 | 2 | byte_fallback_alias | `d` | 1 | 338, 236753 |
| 83 | 2 | byte_fallback_alias | `e` | 1 | 339, 236744 |
| 84 | 2 | byte_fallback_alias | `f` | 1 | 340, 236760 |
| 85 | 2 | byte_fallback_alias | `g` | 1 | 341, 236759 |
| 86 | 2 | byte_fallback_alias | `h` | 1 | 342, 236754 |
| 87 | 2 | byte_fallback_alias | `i` | 1 | 343, 236747 |
| 88 | 2 | byte_fallback_alias | `j` | 1 | 344, 236804 |
| 89 | 2 | byte_fallback_alias | `k` | 1 | 345, 236767 |
| 90 | 2 | byte_fallback_alias | `l` | 1 | 346, 236752 |
| 91 | 2 | byte_fallback_alias | `m` | 1 | 347, 236757 |
| 92 | 2 | byte_fallback_alias | `n` | 1 | 348, 236749 |
| 93 | 2 | byte_fallback_alias | `o` | 1 | 349, 236748 |
| 94 | 2 | byte_fallback_alias | `p` | 1 | 350, 236758 |
| 95 | 2 | byte_fallback_alias | `q` | 1 | 351, 236809 |
| 96 | 2 | byte_fallback_alias | `r` | 1 | 352, 236750 |
| 97 | 2 | byte_fallback_alias | `s` | 1 | 353, 236751 |
| 98 | 2 | byte_fallback_alias | `t` | 1 | 354, 236745 |
| 99 | 2 | byte_fallback_alias | `u` | 1 | 355, 236756 |
| 100 | 2 | byte_fallback_alias | `v` | 1 | 356, 236766 |
| 101 | 2 | byte_fallback_alias | `w` | 1 | 357, 236765 |
| 102 | 2 | byte_fallback_alias | `x` | 1 | 358, 236781 |
| 103 | 2 | byte_fallback_alias | `y` | 1 | 359, 236762 |
| 104 | 2 | byte_fallback_alias | `z` | 1 | 360, 236802 |
| 105 | 2 | byte_fallback_alias | `{` | 1 | 361, 236782 |
| 106 | 2 | byte_fallback_alias | `\|` | 1 | 362, 236909 |
| 107 | 2 | byte_fallback_alias | `}` | 1 | 363, 236783 |
| 108 | 2 | byte_fallback_alias | `~` | 1 | 364, 236995 |
| 109 | 2 | byte_fallback_alias | `` | 1 | 365, 251541 |

All 110 groups. Member pieces and hex bytes: `gemma-3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | byte_fallback_alias |
|---|---|---|---|---|
| ASCII | 150314 | 212 | 106 | 212 / 106 |
| Whitespace | 104 | 8 | 4 | 8 / 4 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 2 | byte_fallback_alias | `\n` | 1 | 107, 248 |
| 1 | 2 | byte_fallback_alias | `` | 1 | 239, 249732 |
| 2 | 2 | byte_fallback_alias | `` | 1 | 240, 241247 |
| 3 | 2 | byte_fallback_alias | `` | 1 | 241, 247953 |
| 4 | 2 | byte_fallback_alias | `` | 1 | 243, 251303 |
| 5 | 2 | byte_fallback_alias | `` | 1 | 246, 243480 |
| 6 | 2 | byte_fallback_alias | `\t` | 1 | 247, 255968 |
| 7 | 2 | byte_fallback_alias | `` | 1 | 256, 248894 |
| 8 | 2 | byte_fallback_alias | `` | 1 | 257, 252295 |
| 9 | 2 | byte_fallback_alias | `` | 1 | 258, 255321 |
| 10 | 2 | byte_fallback_alias | `` | 1 | 261, 252786 |
| 11 | 2 | byte_fallback_alias | `` | 1 | 264, 255485 |
| 12 | 2 | byte_fallback_alias | `` | 1 | 265, 239473 |
| 13 | 2 | byte_fallback_alias | `` | 1 | 269, 253998 |
| 14 | 2 | byte_fallback_alias | ` ` | 1 | 270, 236743 |
| 15 | 2 | byte_fallback_alias | `!` | 1 | 271, 236888 |
| 16 | 2 | byte_fallback_alias | `"` | 1 | 272, 236775 |
| 17 | 2 | byte_fallback_alias | `#` | 1 | 273, 236865 |
| 18 | 2 | byte_fallback_alias | `$` | 1 | 274, 236795 |
| 19 | 2 | byte_fallback_alias | `%` | 1 | 275, 236908 |
| 20 | 2 | byte_fallback_alias | `&` | 1 | 276, 236880 |
| 21 | 2 | byte_fallback_alias | `'` | 1 | 277, 236789 |
| 22 | 2 | byte_fallback_alias | `(` | 1 | 278, 236769 |
| 23 | 2 | byte_fallback_alias | `)` | 1 | 279, 236768 |
| 24 | 2 | byte_fallback_alias | `*` | 1 | 280, 236829 |
| 25 | 2 | byte_fallback_alias | `+` | 1 | 281, 236862 |
| 26 | 2 | byte_fallback_alias | `,` | 1 | 282, 236764 |
| 27 | 2 | byte_fallback_alias | `-` | 1 | 283, 236772 |
| 28 | 2 | byte_fallback_alias | `.` | 1 | 284, 236761 |
| 29 | 2 | byte_fallback_alias | `/` | 1 | 285, 236786 |
| 30 | 2 | byte_fallback_alias | `0` | 1 | 286, 236771 |
| 31 | 2 | byte_fallback_alias | `1` | 1 | 287, 236770 |
| 32 | 2 | byte_fallback_alias | `2` | 1 | 288, 236778 |
| 33 | 2 | byte_fallback_alias | `3` | 1 | 289, 236800 |
| 34 | 2 | byte_fallback_alias | `4` | 1 | 290, 236812 |
| 35 | 2 | byte_fallback_alias | `5` | 1 | 291, 236810 |
| 36 | 2 | byte_fallback_alias | `6` | 1 | 292, 236825 |
| 37 | 2 | byte_fallback_alias | `7` | 1 | 293, 236832 |
| 38 | 2 | byte_fallback_alias | `8` | 1 | 294, 236828 |
| 39 | 2 | byte_fallback_alias | `9` | 1 | 295, 236819 |
| 40 | 2 | byte_fallback_alias | `:` | 1 | 296, 236787 |
| 41 | 2 | byte_fallback_alias | `;` | 1 | 297, 236793 |
| 42 | 2 | byte_fallback_alias | `<` | 1 | 298, 236820 |
| 43 | 2 | byte_fallback_alias | `=` | 1 | 299, 236784 |
| 44 | 2 | byte_fallback_alias | `>` | 1 | 300, 236813 |
| 45 | 2 | byte_fallback_alias | `?` | 1 | 301, 236881 |
| 46 | 2 | byte_fallback_alias | `@` | 1 | 302, 236940 |
| 47 | 2 | byte_fallback_alias | `A` | 1 | 303, 236776 |
| 48 | 2 | byte_fallback_alias | `B` | 1 | 304, 236799 |
| 49 | 2 | byte_fallback_alias | `C` | 1 | 305, 236780 |
| 50 | 2 | byte_fallback_alias | `D` | 1 | 306, 236796 |
| 51 | 2 | byte_fallback_alias | `E` | 1 | 307, 236788 |
| 52 | 2 | byte_fallback_alias | `F` | 1 | 308, 236811 |
| 53 | 2 | byte_fallback_alias | `G` | 1 | 309, 236823 |
| 54 | 2 | byte_fallback_alias | `H` | 1 | 310, 236814 |
| 55 | 2 | byte_fallback_alias | `I` | 1 | 311, 236777 |
| 56 | 2 | byte_fallback_alias | `J` | 1 | 312, 236863 |
| 57 | 2 | byte_fallback_alias | `K` | 1 | 313, 236855 |
| 58 | 2 | byte_fallback_alias | `L` | 1 | 314, 236798 |
| 59 | 2 | byte_fallback_alias | `M` | 1 | 315, 236792 |
| 60 | 2 | byte_fallback_alias | `N` | 1 | 316, 236797 |
| 61 | 2 | byte_fallback_alias | `O` | 1 | 317, 236806 |
| 62 | 2 | byte_fallback_alias | `P` | 1 | 318, 236791 |
| 63 | 2 | byte_fallback_alias | `Q` | 1 | 319, 236935 |
| 64 | 2 | byte_fallback_alias | `R` | 1 | 320, 236794 |
| 65 | 2 | byte_fallback_alias | `S` | 1 | 321, 236773 |
| 66 | 2 | byte_fallback_alias | `T` | 1 | 322, 236774 |
| 67 | 2 | byte_fallback_alias | `U` | 1 | 323, 236836 |
| 68 | 2 | byte_fallback_alias | `V` | 1 | 324, 236847 |
| 69 | 2 | byte_fallback_alias | `W` | 1 | 325, 236824 |
| 70 | 2 | byte_fallback_alias | `X` | 1 | 326, 236917 |
| 71 | 2 | byte_fallback_alias | `Y` | 1 | 327, 236874 |
| 72 | 2 | byte_fallback_alias | `Z` | 1 | 328, 236953 |
| 73 | 2 | byte_fallback_alias | `[` | 1 | 329, 236840 |
| 74 | 2 | byte_fallback_alias | `\` | 1 | 330, 236785 |
| 75 | 2 | byte_fallback_alias | `]` | 1 | 331, 236842 |
| 76 | 2 | byte_fallback_alias | `^` | 1 | 332, 236884 |
| 77 | 2 | byte_fallback_alias | `_` | 1 | 333, 236779 |
| 78 | 2 | byte_fallback_alias | `'` | 1 | 334, 236929 |
| 79 | 2 | byte_fallback_alias | `a` | 1 | 335, 236746 |
| 80 | 2 | byte_fallback_alias | `b` | 1 | 336, 236763 |
| 81 | 2 | byte_fallback_alias | `c` | 1 | 337, 236755 |
| 82 | 2 | byte_fallback_alias | `d` | 1 | 338, 236753 |
| 83 | 2 | byte_fallback_alias | `e` | 1 | 339, 236744 |
| 84 | 2 | byte_fallback_alias | `f` | 1 | 340, 236760 |
| 85 | 2 | byte_fallback_alias | `g` | 1 | 341, 236759 |
| 86 | 2 | byte_fallback_alias | `h` | 1 | 342, 236754 |
| 87 | 2 | byte_fallback_alias | `i` | 1 | 343, 236747 |
| 88 | 2 | byte_fallback_alias | `j` | 1 | 344, 236804 |
| 89 | 2 | byte_fallback_alias | `k` | 1 | 345, 236767 |
| 90 | 2 | byte_fallback_alias | `l` | 1 | 346, 236752 |
| 91 | 2 | byte_fallback_alias | `m` | 1 | 347, 236757 |
| 92 | 2 | byte_fallback_alias | `n` | 1 | 348, 236749 |
| 93 | 2 | byte_fallback_alias | `o` | 1 | 349, 236748 |
| 94 | 2 | byte_fallback_alias | `p` | 1 | 350, 236758 |
| 95 | 2 | byte_fallback_alias | `q` | 1 | 351, 236809 |
| 96 | 2 | byte_fallback_alias | `r` | 1 | 352, 236750 |
| 97 | 2 | byte_fallback_alias | `s` | 1 | 353, 236751 |
| 98 | 2 | byte_fallback_alias | `t` | 1 | 354, 236745 |
| 99 | 2 | byte_fallback_alias | `u` | 1 | 355, 236756 |
| 100 | 2 | byte_fallback_alias | `v` | 1 | 356, 236766 |
| 101 | 2 | byte_fallback_alias | `w` | 1 | 357, 236765 |
| 102 | 2 | byte_fallback_alias | `x` | 1 | 358, 236781 |
| 103 | 2 | byte_fallback_alias | `y` | 1 | 359, 236762 |
| 104 | 2 | byte_fallback_alias | `z` | 1 | 360, 236802 |
| 105 | 2 | byte_fallback_alias | `{` | 1 | 361, 236782 |
| 106 | 2 | byte_fallback_alias | `\|` | 1 | 362, 236909 |
| 107 | 2 | byte_fallback_alias | `}` | 1 | 363, 236783 |
| 108 | 2 | byte_fallback_alias | `~` | 1 | 364, 236995 |
| 109 | 2 | byte_fallback_alias | `` | 1 | 365, 251541 |

All 110 groups. Member pieces and hex bytes: `gemma-3/groups_raw.jsonl`.

## deepseek-v3

Source `deepseek-ai/DeepSeek-V3-Base` (hf), snapshot `afb92e1fa402c2be2a9eb085312bb02e0384d6c7`, family `bbpe`.

- V = 128,815; raw rows by rule: added_literal 816, model_bbpe 127,997, special 2
- rows where decode bytes ≠ raw bytes: 1,470; raw rows that are not valid UTF-8: 1,470
- tokens longer than 64 bytes: 13; of these, sharing a row with another token: 10
- decode table SHA-256 `150adce1f2c8fb895acb1d4b87f37ad16c867512829a3f1c9594a10c0262cce3`
- raw table SHA-256 `f06c29247c2f237eb96bccc8a3f5c92d276debf4521f0c1bb0d52b1563e52c4e`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation |
|---|---|---|---|---|---|
| CJK Han (fragment) | 336 | 336 | 2 | 336 / 2 | 0 / 0 |
| Hangul (fragment) | 201 | 201 | 2 | 201 / 2 | 0 / 0 |
| Hebrew | 923 | 127 | 24 | 127 / 24 | 0 / 0 |
| Continuation bytes only | 121 | 119 | 3 | 119 / 3 | 0 / 0 |
| Other scripts (fragment) | 69 | 67 | 4 | 67 / 4 | 0 / 0 |
| Punctuation/symbols (fragment) | 40 | 40 | 2 | 40 / 2 | 0 / 0 |
| Emoji (fragment) | 37 | 37 | 2 | 37 / 2 | 0 / 0 |
| Mixed (fragment) | 37 | 37 | 2 | 37 / 2 | 0 / 0 |
| Latin-ext (fragment) | 23 | 20 | 2 | 20 / 2 | 0 / 0 |
| Hebrew (fragment) | 18 | 18 | 3 | 18 / 3 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| ASCII | 72143 | 11 | 4 | 0 / 0 | 11 / 4 |
| Arabic (fragment) | 11 | 11 | 2 | 11 / 2 | 0 / 0 |
| Greek (fragment) | 10 | 10 | 2 | 10 / 2 | 0 / 0 |
| Cyrillic (fragment) | 8 | 8 | 2 | 8 / 2 | 0 / 0 |
| Other scripts | 471 | 6 | 3 | 6 / 3 | 0 / 0 |
| Hangul | 1131 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 14 | 4 | 4 | 4 / 4 | 0 / 0 |
| Bengali (fragment) | 4 | 4 | 3 | 4 / 3 | 0 / 0 |
| CJK symbols (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Telugu (fragment) | 4 | 4 | 3 | 4 / 3 | 0 / 0 |
| Whitespace | 157 | 3 | 1 | 0 / 0 | 3 / 1 |
| Malayalam | 67 | 3 | 1 | 3 / 1 | 0 / 0 |
| Devanagari (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gujarati (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Kana (fragment) | 3 | 3 | 1 | 3 / 1 | 0 / 0 |
| Kannada (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Malayalam (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Oriya (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Private use (fragment) | 3 | 3 | 1 | 3 / 1 | 0 / 0 |
| Tamil (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Tamil | 168 | 2 | 1 | 2 / 1 | 0 / 0 |
| Combining marks (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Thai (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 692 | utf8_replacement | `�` | 3 | 97, 98, 99, 100, 101, 102 … |
| 1 | 180 | utf8_replacement | ` �` | 4 | 332, 508, 544, 663, 669, 831 … |
| 2 | 86 | utf8_replacement | `��` | 6 | 518, 2002, 2100, 3042, 3308, 3457 … |
| 3 | 10 | utf8_replacement | `�ר` | 5 | 19236, 20204, 23090, 32254, 102733, 107617 … |
| 4 | 10 | utf8_replacement | `�ה` | 5 | 20645, 27713, 32645, 56457, 62239, 73588 … |
| 5 | 10 | utf8_replacement | `�ת` | 5 | 30149, 37254, 37708, 38246, 38293, 40010 … |
| 6 | 9 | utf8_replacement | `�ל` | 5 | 19952, 34119, 56864, 97152, 101802, 104557 … |
| 7 | 9 | utf8_replacement | `�ים` | 7 | 26586, 38430, 48259, 62342, 79546, 93546 … |
| 8 | 8 | utf8_replacement | `�י` | 5 | 11529, 37818, 42079, 45346, 51989, 100301 … |
| 9 | 8 | utf8_replacement | `�ד` | 5 | 34073, 38210, 49390, 49920, 65057, 76057 … |
| 10 | 7 | utf8_replacement | `�ות` | 7 | 30952, 44901, 56156, 68296, 80064, 87464 … |
| 11 | 6 | utf8_replacement | `�ם` | 5 | 30146, 49213, 66174, 97480, 110003, 123182 |
| 12 | 6 | utf8_replacement | `�ן` | 5 | 37538, 87506, 90807, 92522, 99280, 123447 |
| 13 | 5 | utf8_replacement | `�ע` | 5 | 27758, 45277, 91039, 97052, 122271 |
| 14 | 4 | truncation | `........................................…` | 64 | 13361, 70676, 77270, 111683 |
| 15 | 4 | utf8_replacement | `�ט` | 5 | 29811, 46064, 60681, 62926 |
| 16 | 4 | utf8_replacement | `�ש` | 5 | 32556, 40497, 94263, 100290 |
| 17 | 4 | utf8_replacement | `�ס` | 5 | 46746, 53546, 80303, 116022 |
| 18 | 4 | utf8_replacement | `�ג` | 5 | 73227, 89919, 102743, 103361 |
| 19 | 3 | truncation | `                                        …` | 64 | 16932, 69933, 124189 |
| 20 | 3 | utf8_replacement | `�ו` | 5 | 20837, 37640, 86274 |
| 21 | 3 | truncation | `----------------------------------------…` | 64 | 24991, 79773, 111795 |
| 22 | 3 | utf8_replacement | `subscript�` | 12 | 25433, 65046, 68426 |
| 23 | 3 | utf8_replacement | `�ב` | 5 | 40561, 48200, 119019 |
| 24 | 3 | utf8_replacement | `�്�` | 9 | 41011, 47476, 99098 |
| 25 | 3 | utf8_replacement | `�צ` | 5 | 41015, 52353, 60851 |
| 26 | 3 | utf8_replacement | `�ק` | 5 | 42835, 57332, 58118 |
| 27 | 3 | utf8_replacement | `�\n\n` | 5 | 57265, 107296, 126477 |
| 28 | 3 | utf8_replacement | `�ך` | 5 | 67043, 82052, 86534 |
| 29 | 2 | utf8_replacement | `�다` | 6 | 6768, 107520 |
| 30 | 2 | utf8_replacement | `်�` | 6 | 14976, 106016 |
| 31 | 2 | utf8_replacement | `�்` | 6 | 15790, 87466 |
| 32 | 2 | utf8_replacement | `�်�` | 9 | 37058, 56561 |
| 33 | 2 | utf8_replacement | `�이` | 6 | 38331, 47896 |
| 34 | 2 | utf8_replacement | `�א` | 5 | 45279, 122046 |
| 35 | 2 | utf8_replacement | `�ית` | 7 | 51255, 110199 |
| 36 | 2 | utf8_replacement | `�ი` | 6 | 53177, 88400 |
| 37 | 2 | utf8_replacement | `�ז` | 5 | 56203, 74336 |
| 38 | 2 | truncation | `========================================…` | 64 | 57816, 105553 |
| 39 | 2 | truncation | ` ***************************************…` | 64 | 74667, 118888 |
| 40 | 2 | utf8_replacement | `�ור` | 7 | 108027, 115719 |

All 41 groups. Member pieces and hex bytes: `deepseek-v3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation |
|---|---|---|---|---|
| ASCII | 72143 | 11 | 4 | 11 / 4 |
| Whitespace | 157 | 3 | 1 | 3 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 4 | truncation | `........................................…` | 64 | 13361, 70676, 77270, 111683 |
| 1 | 3 | truncation | `                                        …` | 64 | 16932, 69933, 124189 |
| 2 | 3 | truncation | `----------------------------------------…` | 64 | 24991, 79773, 111795 |
| 3 | 2 | truncation | `========================================…` | 64 | 57816, 105553 |
| 4 | 2 | truncation | ` ***************************************…` | 64 | 74667, 118888 |

All 5 groups. Member pieces and hex bytes: `deepseek-v3/groups_raw.jsonl`.

## gpt-oss

Source `openai/gpt-oss-120b` (hf), snapshot `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`, family `bbpe`.

- V = 200,019; raw rows by rule: added_literal 18, model_bbpe 199,998, special 3
- rows where decode bytes ≠ raw bytes: 1,562; raw rows that are not valid UTF-8: 1,562
- tokens longer than 64 bytes: 85; of these, sharing a row with another token: 77
- decode table SHA-256 `25aa217b0c832b61218c9c923dcaf9cc2da08aaca749453d9637a5f298457921`
- raw table SHA-256 `a6c11636348fd47fd36c8d61291ab1548dbd8401adebdc9a831a4137fe5102cb`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation |
|---|---|---|---|---|---|
| CJK Han (fragment) | 529 | 529 | 2 | 529 / 2 | 0 / 0 |
| Hangul (fragment) | 236 | 236 | 2 | 236 / 2 | 0 / 0 |
| Continuation bytes only | 148 | 147 | 4 | 147 / 4 | 0 / 0 |
| ASCII | 128445 | 62 | 10 | 0 / 0 | 62 / 10 |
| Mixed (fragment) | 46 | 46 | 3 | 46 / 3 | 0 / 0 |
| Emoji (fragment) | 39 | 39 | 2 | 39 / 2 | 0 / 0 |
| Other scripts (fragment) | 37 | 37 | 3 | 37 / 3 | 0 / 0 |
| Punctuation/symbols (fragment) | 34 | 34 | 2 | 34 / 2 | 0 / 0 |
| Whitespace | 434 | 21 | 1 | 0 / 0 | 21 / 1 |
| Latin-ext (fragment) | 22 | 21 | 2 | 21 / 2 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| Private use (fragment) | 12 | 12 | 2 | 12 / 2 | 0 / 0 |
| Arabic (fragment) | 11 | 11 | 2 | 11 / 2 | 0 / 0 |
| Other scripts | 4877 | 10 | 4 | 10 / 4 | 0 / 0 |
| Cyrillic (fragment) | 7 | 7 | 2 | 7 / 2 | 0 / 0 |
| Greek (fragment) | 6 | 6 | 2 | 6 / 2 | 0 / 0 |
| Telugu | 1326 | 5 | 2 | 5 / 2 | 0 / 0 |
| CJK symbols (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Kana (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Thai (fragment) | 5 | 5 | 3 | 5 / 3 | 0 / 0 |
| Hangul | 2369 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 21 | 4 | 4 | 4 / 4 | 0 / 0 |
| Bengali (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Devanagari (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Malayalam (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Telugu (fragment) | 4 | 4 | 3 | 4 / 3 | 0 / 0 |
| Gujarati (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Kannada (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Oriya (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Tamil (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| CJK Han | 7374 | 2 | 1 | 2 / 1 | 0 / 0 |
| Bengali | 2129 | 2 | 1 | 2 / 1 | 0 / 0 |
| Malayalam | 1657 | 2 | 1 | 2 / 1 | 0 / 0 |
| Gujarati | 1620 | 2 | 1 | 2 / 1 | 0 / 0 |
| Tamil | 975 | 2 | 1 | 2 / 1 | 0 / 0 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Combining marks (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 689 | utf8_replacement | `�` | 3 | 94, 95, 96, 97, 98, 99 … |
| 1 | 411 | utf8_replacement | ` �` | 4 | 300, 333, 367, 389, 463, 559 … |
| 2 | 88 | utf8_replacement | `��` | 6 | 1857, 1965, 2112, 2121, 2203, 4765 … |
| 3 | 21 | truncation | `                                        …` | 64 | 9344, 30723, 38959, 46371, 72056, 82724 … |
| 4 | 15 | truncation | `----------------------------------------…` | 64 | 7535, 28943, 32635, 50529, 61743, 78407 … |
| 5 | 10 | truncation | `****************************************…` | 64 | 8599, 12217, 41547, 42538, 76470, 82394 … |
| 6 | 7 | truncation | `========================================…` | 64 | 17686, 63146, 111845, 154118, 174517, 180864 … |
| 7 | 6 | truncation | ` ***************************************…` | 64 | 22567, 39967, 50885, 70007, 73838, 163690 |
| 8 | 5 | truncation | ` ---------------------------------------…` | 64 | 18882, 77304, 79593, 141084, 179041 |
| 9 | 5 | truncation | `////////////////////////////////////////…` | 64 | 25493, 73681, 76050, 143581, 174665 |
| 10 | 4 | truncation | `########################################…` | 64 | 29834, 81787, 103402, 185617 |
| 11 | 4 | truncation | ` =======================================…` | 64 | 36014, 126247, 132548, 166044 |
| 12 | 4 | truncation | `/***************************************…` | 64 | 109438, 111383, 113341, 117837 |
| 13 | 3 | utf8_replacement | `�ი` | 6 | 4980, 6102, 142740 |
| 14 | 3 | utf8_replacement | `�ి` | 6 | 13981, 47426, 79041 |
| 15 | 3 | utf8_replacement | `�ვ` | 6 | 59325, 69450, 154624 |
| 16 | 2 | utf8_replacement | `�்` | 6 | 4535, 70619 |
| 17 | 2 | utf8_replacement | `�়` | 6 | 6578, 44278 |
| 18 | 2 | utf8_replacement | `�്ച` | 9 | 7350, 165871 |
| 19 | 2 | utf8_replacement | `�美` | 6 | 9505, 82761 |
| 20 | 2 | utf8_replacement | `�ે` | 6 | 13601, 21340 |
| 21 | 2 | utf8_replacement | `�ლ` | 6 | 18038, 19922 |
| 22 | 2 | utf8_replacement | `�니다` | 9 | 34951, 162551 |
| 23 | 2 | utf8_replacement | `�ნ` | 6 | 55507, 61639 |
| 24 | 2 | utf8_replacement | `�다` | 6 | 56388, 75734 |
| 25 | 2 | utf8_replacement | `�\n\n` | 5 | 68340, 115963 |
| 26 | 2 | utf8_replacement | `�్` | 6 | 73475, 76944 |
| 27 | 2 | utf8_replacement | `�pp` | 5 | 78747, 186978 |
| 28 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 93582, 176860 |

All 29 groups. Member pieces and hex bytes: `gpt-oss/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation |
|---|---|---|---|---|
| ASCII | 128445 | 62 | 10 | 62 / 10 |
| Whitespace | 434 | 21 | 1 | 21 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 21 | truncation | `                                        …` | 64 | 9344, 30723, 38959, 46371, 72056, 82724 … |
| 1 | 15 | truncation | `----------------------------------------…` | 64 | 7535, 28943, 32635, 50529, 61743, 78407 … |
| 2 | 10 | truncation | `****************************************…` | 64 | 8599, 12217, 41547, 42538, 76470, 82394 … |
| 3 | 7 | truncation | `========================================…` | 64 | 17686, 63146, 111845, 154118, 174517, 180864 … |
| 4 | 6 | truncation | ` ***************************************…` | 64 | 22567, 39967, 50885, 70007, 73838, 163690 |
| 5 | 5 | truncation | ` ---------------------------------------…` | 64 | 18882, 77304, 79593, 141084, 179041 |
| 6 | 5 | truncation | `////////////////////////////////////////…` | 64 | 25493, 73681, 76050, 143581, 174665 |
| 7 | 4 | truncation | `########################################…` | 64 | 29834, 81787, 103402, 185617 |
| 8 | 4 | truncation | ` =======================================…` | 64 | 36014, 126247, 132548, 166044 |
| 9 | 4 | truncation | `/***************************************…` | 64 | 109438, 111383, 113341, 117837 |
| 10 | 2 | truncation | ` ///////////////////////////////////////…` | 64 | 93582, 176860 |

All 11 groups. Member pieces and hex bytes: `gpt-oss/groups_raw.jsonl`.

## Proof checks

| tokenizer | table | L1 round-trip | L1 max norm err | L2 support = {z>0} | L2 max rel err | T1 distinct byte rows | T1 distinct codec rows | T1 groups → 1 codec row | dynamic = cached |
|---|---|---|---|---|---|---|---|---|---|
| gpt2 | decode | 50,257/50,257 | 1.2e-07 | 50,257/50,257 | 1.3e-07 | 49,923 | 49,923 | 8/8 | yes |
| gpt2 | raw | 50,257/50,257 | 1.2e-07 | 50,257/50,257 | 1.3e-07 | 50,256 | 50,256 | 1/1 | yes |
| llama-3.2 | decode | 128,256/128,256 | 1.2e-07 | 128,256/128,256 | 1.7e-07 | 126,940 | 126,940 | 31/31 | yes |
| llama-3.2 | raw | 128,256/128,256 | 1.2e-07 | 128,256/128,256 | 1.7e-07 | 128,156 | 128,156 | 18/18 | yes |
| qwen3 | decode | 151,669/151,669 | 1.2e-07 | 151,669/151,669 | 1.7e-07 | 150,233 | 150,233 | 29/29 | yes |
| qwen3 | raw | 151,669/151,669 | 1.2e-07 | 151,669/151,669 | 1.7e-07 | 151,569 | 151,569 | 18/18 | yes |
| gemma-3 | decode | 262,145/262,145 | 1.2e-07 | 262,145/262,145 | 1.7e-07 | 262,035 | 262,035 | 110/110 | yes |
| gemma-3 | raw | 262,145/262,145 | 1.2e-07 | 262,145/262,145 | 1.7e-07 | 262,035 | 262,035 | 110/110 | yes |
| deepseek-v3 | decode | 128,815/128,815 | 1.2e-07 | 128,815/128,815 | 1.7e-07 | 127,736 | 127,736 | 41/41 | yes |
| deepseek-v3 | raw | 128,815/128,815 | 1.2e-07 | 128,815/128,815 | 1.7e-07 | 128,806 | 128,806 | 5/5 | yes |
| gpt-oss | decode | 200,019/200,019 | 1.2e-07 | 200,019/200,019 | 1.7e-07 | 198,744 | 198,744 | 29/29 | yes |
| gpt-oss | raw | 200,019/200,019 | 1.2e-07 | 200,019/200,019 | 1.7e-07 | 199,947 | 199,947 | 11/11 | yes |

## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)

| L | z on support | z off support | rows checked | max rel err |
|---|---|---|---|---|
| 1 | 127.975807 | -0.00781150 | 2,652 | 5.5e-08 |
| 2 | 90.489798 | -0.01104747 | 45,097 | 7.4e-08 |
| 3 | 73.882356 | -0.01353074 | 215,699 | 3.8e-08 |
| 4 | 63.982044 | -0.01562443 | 225,888 | 5.1e-08 |
| 5 | 57.225532 | -0.01746918 | 211,835 | 4.2e-08 |
| 6 | 52.237930 | -0.01913711 | 317,527 | 7.8e-08 |
| 7 | 48.361449 | -0.02067107 | 192,981 | 2.6e-08 |
| 8 | 45.236612 | -0.02209898 | 136,949 | 4.3e-08 |
| 9 | 42.648184 | -0.02344022 | 160,308 | 7.0e-08 |
| 10 | 40.458385 | -0.02470892 | 87,750 | 2.4e-08 |
| 11 | 38.574378 | -0.02591572 | 61,936 | 4.7e-08 |
| 12 | 36.931027 | -0.02706892 | 63,334 | 8.6e-08 |
| 13 | 35.481099 | -0.02817508 | 39,450 | 3.3e-08 |
| 14 | 34.189398 | -0.02923956 | 10,165 | 3.7e-08 |
| 15 | 33.029088 | -0.03026674 | 17,437 | 6.2e-08 |
| 16 | 31.979300 | -0.03126031 | 13,639 | 3.4e-08 |
| 17 | 31.023530 | -0.03222338 | 4,366 | 1.3e-07 |
| 18 | 30.148531 | -0.03315859 | 4,527 | 7.2e-08 |
| 19 | 29.343528 | -0.03406826 | 9,595 | 7.5e-08 |
| 20 | 28.599660 | -0.03495436 | 370 | 7.2e-08 |
| 21 | 27.909557 | -0.03581866 | 3,069 | 7.7e-08 |
| 22 | 27.267039 | -0.03666269 | 4,712 | 6.4e-08 |
| 23 | 26.666875 | -0.03748781 | 826 | 5.1e-08 |
| 24 | 26.104606 | -0.03829527 | 1,018 | 2.2e-08 |
| 25 | 25.576404 | -0.03908614 | 3,172 | 5.4e-09 |
| 26 | 25.078961 | -0.03986141 | 88 | 5.4e-08 |
| 27 | 24.609402 | -0.04062199 | 638 | 1.7e-07 |
| 28 | 24.165214 | -0.04136867 | 1,504 | 9.3e-08 |
| 29 | 23.744192 | -0.04210220 | 298 | 4.2e-08 |
| 30 | 23.344387 | -0.04282326 | 516 | 1.1e-07 |
| 31 | 22.964076 | -0.04353246 | 862 | 4.3e-08 |
| 32 | 22.601723 | -0.04423038 | 312 | 5.1e-08 |
| 33 | 22.255958 | -0.04491754 | 1,584 | 8.1e-08 |
| 34 | 21.925551 | -0.04559442 | 469 | 4.5e-08 |
| 35 | 21.609398 | -0.04626148 | 26 | 4.9e-08 |
| 36 | 21.306502 | -0.04691914 | 49 | 3.9e-08 |
| 37 | 21.015962 | -0.04756779 | 257 | 4.4e-08 |
| 38 | 20.736958 | -0.04820778 | 8 | 7.5e-08 |
| 39 | 20.468747 | -0.04883947 | 35 | 6.0e-08 |
| 40 | 20.210650 | -0.04946317 | 108 | 8.4e-08 |
| 41 | 19.962046 | -0.05007917 | 24 | 2.1e-08 |
| 42 | 19.722368 | -0.05068776 | 34 | 3.5e-08 |
| 43 | 19.491092 | -0.05128921 | 46 | 8.8e-08 |
| 44 | 19.267740 | -0.05188375 | 8 | 2.9e-08 |
| 45 | 19.051868 | -0.05247164 | 22 | 1.1e-07 |
| 46 | 18.843068 | -0.05305307 | 30 | 7.9e-08 |
| 47 | 18.640961 | -0.05362828 | 8 | 6.4e-08 |
| 48 | 18.445198 | -0.05419745 | 94 | 2.5e-08 |
| 49 | 18.255453 | -0.05476077 | 42 | 4.4e-08 |
| 50 | 18.071423 | -0.05531842 | 30 | 3.2e-08 |
| 51 | 17.892827 | -0.05587058 | 18 | 4.4e-08 |
| 52 | 17.719403 | -0.05641740 | 12 | 6.6e-08 |
| 53 | 17.550905 | -0.05695903 | 6 | 2.1e-08 |
| 54 | 17.387105 | -0.05749563 | 6 | 8.9e-08 |
| 55 | 17.227788 | -0.05802733 | 10 | 5.6e-08 |
| 56 | 17.072753 | -0.05855427 | 24 | 3.9e-08 |
| 57 | 16.921811 | -0.05907657 | 16 | 3.4e-08 |
| 58 | 16.774785 | -0.05959436 | 6 | 1.0e-07 |
| 59 | 16.631509 | -0.06010775 | 8 | 5.8e-08 |
| 60 | 16.491825 | -0.06061685 | 14 | 1.6e-08 |
| 61 | 16.355587 | -0.06112178 | 12 | 8.7e-08 |
| 62 | 16.222654 | -0.06162263 | 8 | 3.8e-08 |
| 63 | 16.092894 | -0.06211950 | 16 | 6.8e-08 |
| 64 | 15.966184 | -0.06261249 | 772 | 1.2e-08 |

## Determinism (3 fresh CPU processes)

| run | PYTHONHASHSEED | torch threads | device | wall s |
|---|---|---|---|---|
| 1 | 0 | 1 | cpu | 223.9 |
| 2 | 1 | 4 | cpu | 127.3 |
| 3 | 2 | 8 | cpu | 102.3 |

| tokenizer | hash of | IDs decoded per run | SHA-256 (run 1) | all runs |
|---|---|---|---|---|
| gpt2 | decode_table | 50,257 | `0ec79d2ef48432eeced7b788544891df039ad8835df260b70180a8695d015384` | match |
| gpt2 | raw_table | 50,257 | `33cc5f9de4daf911ca02e76cde1418777b4429737e99fae9f64c821760e1c1ce` | match |
| gpt2 | codec_table | 50,257 | `f8419cdb46a9e212e2e842d22956d9fea69ae5d92a81784fd47b1d2bae9cf365` | match |
| llama-3.2 | decode_table | 128,256 | `7d5372cd7d25dc4d813ca1bd998c7b595a39a7ce9d091fdc23a4fc6a153ec1ef` | match |
| llama-3.2 | raw_table | 128,256 | `d8c70d202337b139f1194a123eee866ce867e9674199546414c59158e3b52fd7` | match |
| llama-3.2 | codec_table | 128,256 | `063c51ed28f05a6ced045e053db93eaf98dd8b476b976d9d7c955e8dabbc0cd6` | match |
| qwen3 | decode_table | 151,669 | `6022214773e806ba281c5bfd094546f14173a100b8b9a9db40edb0bcabbddaed` | match |
| qwen3 | raw_table | 151,669 | `927e0f0063c4443f9f016f8ebe328e7ab1105f1d5c6b6b7852711956dbfab1ce` | match |
| qwen3 | codec_table | 151,669 | `d82d922edb8e9b51c80c711ba67a2b99bcc627628403b00d98162652318534bd` | match |
| gemma-3 | decode_table | 262,145 | `a9183760fd6cf35e29eb6c9965917f5a0c7a5873a97860a0e7655d7e5c322960` | match |
| gemma-3 | raw_table | 262,145 | `a9183760fd6cf35e29eb6c9965917f5a0c7a5873a97860a0e7655d7e5c322960` | match |
| gemma-3 | codec_table | 262,145 | `72ebe0048df77ee2bf1f0f644a335c1ecd632bcb67f5c09e7769fab3e059b938` | match |
| deepseek-v3 | decode_table | 128,815 | `150adce1f2c8fb895acb1d4b87f37ad16c867512829a3f1c9594a10c0262cce3` | match |
| deepseek-v3 | raw_table | 128,815 | `f06c29247c2f237eb96bccc8a3f5c92d276debf4521f0c1bb0d52b1563e52c4e` | match |
| deepseek-v3 | codec_table | 128,815 | `9864af201e2236cba59497c87feafd31579a0fad7a31f6db9d72059634ad9b62` | match |
| gpt-oss | decode_table | 200,019 | `25aa217b0c832b61218c9c923dcaf9cc2da08aaca749453d9637a5f298457921` | match |
| gpt-oss | raw_table | 200,019 | `a6c11636348fd47fd36c8d61291ab1548dbd8401adebdc9a831a4137fe5102cb` | match |
| gpt-oss | codec_table | 200,019 | `d203299a93597e2bd4979b65726cf399c155dc918b52389ac94e5af6476fb78a` | match |

All hashes match: **True**.

