# Generated tables

Rendered by `src/report.py` from `results/`. Do not edit by hand.

## Overview (P = 32)

`lost` = V − distinct rows = IDs that do not get their own codec row.

| tokenizer | V | decode groups | decode colliding IDs | decode lost | raw groups | raw colliding IDs | raw lost | L1/L2/T1/modes |
|---|---|---|---|---|---|---|---|---|
| gpt2 | 50,257 | 14 | 357 | 343 | 7 | 17 | 10 | pass |
| llama-3.2 | 128,256 | 41 | 1,452 | 1,411 | 28 | 223 | 195 | pass |
| qwen3 | 151,669 | 36 | 1,556 | 1,520 | 25 | 209 | 184 | pass |
| gemma-3 | 262,145 | 159 | 336 | 177 | 159 | 336 | 177 | pass |
| deepseek-v3 | 128,815 | 50 | 1,174 | 1,124 | 14 | 68 | 54 | pass |
| gpt-oss | 200,019 | 47 | 1,405 | 1,358 | 29 | 184 | 155 | pass |

## Collisions by cause

| tokenizer | table | cause | groups | tokens |
|---|---|---|---|---|
| gpt2 | decode | utf8_replacement | 7 | 340 |
| gpt2 | decode | truncation_p32 | 7 | 17 |
| gpt2 | raw | truncation_p32 | 7 | 17 |
| llama-3.2 | decode | utf8_replacement | 13 | 1229 |
| llama-3.2 | decode | truncation_p32 | 28 | 223 |
| llama-3.2 | raw | truncation_p32 | 28 | 223 |
| qwen3 | decode | utf8_replacement | 11 | 1347 |
| qwen3 | decode | truncation_p32 | 25 | 209 |
| qwen3 | raw | truncation_p32 | 25 | 209 |
| gemma-3 | decode | truncation_p32 | 49 | 116 |
| gemma-3 | decode | byte_fallback_alias | 110 | 220 |
| gemma-3 | raw | truncation_p32 | 49 | 116 |
| gemma-3 | raw | byte_fallback_alias | 110 | 220 |
| deepseek-v3 | decode | utf8_replacement | 37 | 1108 |
| deepseek-v3 | decode | truncation_p32 | 13 | 66 |
| deepseek-v3 | raw | truncation_p32 | 14 | 68 |
| gpt-oss | decode | utf8_replacement | 18 | 1221 |
| gpt-oss | decode | truncation_p32 | 29 | 184 |
| gpt-oss | raw | truncation_p32 | 29 | 184 |

## Colliding token IDs per script class — decode table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| CJK Han | 108 | 571 | 570 | 0 | 338 | 531 | 2118 |
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

## Colliding token IDs per script class — raw table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

| script class | gpt2 | llama-3.2 | qwen3 | gemma-3 | deepseek-v3 | gpt-oss | total |
|---|---|---|---|---|---|---|---|
| ASCII | 14 | 145 | 145 | 212 | 35 | 101 | 652 |
| Whitespace | 0 | 76 | 60 | 8 | 27 | 57 | 228 |
| Bengali | 0 | 0 | 0 | 63 | 0 | 0 | 63 |
| Devanagari | 0 | 0 | 0 | 25 | 0 | 0 | 25 |
| Tamil | 0 | 0 | 0 | 22 | 0 | 0 | 22 |
| Thai | 0 | 0 | 4 | 2 | 0 | 14 | 20 |
| Other scripts | 0 | 0 | 0 | 0 | 2 | 6 | 8 |
| Malayalam | 0 | 0 | 0 | 2 | 0 | 4 | 6 |
| Punctuation/symbols | 0 | 0 | 0 | 2 | 2 | 0 | 4 |
| Latin-ext | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| CJK Han | 0 | 0 | 0 | 0 | 2 | 0 | 2 |
| Cyrillic | 0 | 2 | 0 | 0 | 0 | 0 | 2 |
| Gujarati | 0 | 0 | 0 | 0 | 0 | 2 | 2 |

## gpt2

Tokenizer `openai-community/gpt2` snapshot `607a30d783dfa663caf39e06633721c8d4cfcd7e`.

- V = 50,257; raw rows by rule: model_bbpe 50,256, special 1
- rows where decode bytes ≠ raw bytes: 344; raw rows that are not valid UTF-8: 344
- tokens longer than 32 bytes: 14; of these, sharing a row with another token: 12
- decode table SHA-256 `fea58ad63a97f0ac9568a74d6d564b148f4ebaf84f289acf32e1e6571f1c1a5b`
- raw table SHA-256 `e8db9b5152c0828b5e69e5092d6b2f4eb002cc51df0d1930ff8c6f4f100ec86a`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation_p32 |
|---|---|---|---|---|---|
| CJK Han (fragment) | 104 | 104 | 4 | 104 / 4 | 0 / 0 |
| Continuation bytes only | 91 | 91 | 2 | 91 / 2 | 0 / 0 |
| Mixed (fragment) | 23 | 23 | 2 | 23 / 2 | 0 / 0 |
| Punctuation/symbols (fragment) | 17 | 17 | 2 | 17 / 2 | 0 / 0 |
| Latin-ext (fragment) | 16 | 16 | 2 | 16 / 2 | 0 / 0 |
| ASCII | 49372 | 14 | 6 | 0 / 0 | 14 / 6 |
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
| Latin-ext | 148 | 3 | 1 | 0 / 0 | 3 / 1 |
| Devanagari (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
| Gurmukhi (fragment) | 3 | 3 | 2 | 3 / 2 | 0 / 0 |
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
| 4 | 4 | truncation_p32 | `--------------------------------` | 32 | 3880, 10097, 43801, 47232 |
| 5 | 3 | truncation_p32 | `ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ` | 32 | 14827, 23090, 35496 |
| 6 | 2 | truncation_p32 | `................................` | 32 | 8864, 23193 |
| 7 | 2 | truncation_p32 | `================================` | 32 | 10052, 23926 |
| 8 | 2 | truncation_p32 | `________________________________` | 32 | 10221, 27193 |
| 9 | 2 | truncation_p32 | ` -------------------------------` | 32 | 16529, 20368 |
| 10 | 2 | utf8_replacement | `龍�` | 6 | 19049, 39820 |
| 11 | 2 | utf8_replacement | ` 裏�` | 7 | 20174, 34504 |
| 12 | 2 | truncation_p32 | ` ===============================` | 32 | 38093, 46111 |
| 13 | 2 | utf8_replacement | `���` | 9 | 47490, 48585 |

All 14 groups. Member pieces and hex bytes: `results/gpt2/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 |
|---|---|---|---|---|
| ASCII | 49372 | 14 | 6 | 14 / 6 |
| Latin-ext | 148 | 3 | 1 | 3 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 4 | truncation_p32 | `--------------------------------` | 32 | 3880, 10097, 43801, 47232 |
| 1 | 3 | truncation_p32 | `ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ` | 32 | 14827, 23090, 35496 |
| 2 | 2 | truncation_p32 | `................................` | 32 | 8864, 23193 |
| 3 | 2 | truncation_p32 | `================================` | 32 | 10052, 23926 |
| 4 | 2 | truncation_p32 | `________________________________` | 32 | 10221, 27193 |
| 5 | 2 | truncation_p32 | ` -------------------------------` | 32 | 16529, 20368 |
| 6 | 2 | truncation_p32 | ` ===============================` | 32 | 38093, 46111 |

All 7 groups. Member pieces and hex bytes: `results/gpt2/groups_raw.jsonl`.

## llama-3.2

Tokenizer `unsloth/Llama-3.2-1B` snapshot `9535bd9b1d1dea6acafbdc4813b728796aeb28da`.

- V = 128,256; raw rows by rule: added_literal 253, model_bbpe 128,000, special 3
- rows where decode bytes ≠ raw bytes: 1,352; raw rows that are not valid UTF-8: 1,352
- tokens longer than 32 bytes: 231; of these, sharing a row with another token: 210
- decode table SHA-256 `b051c5ca594b9feec36dd95b04177dbeb9bdea3ec70b5eb33409756e2421e4a6`
- raw table SHA-256 `70d6e7b67a030cccce09fae1fc7893b5fbe6d418d621a16e9881645ce7d1fc3b`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation_p32 |
|---|---|---|---|---|---|
| CJK Han (fragment) | 569 | 569 | 2 | 569 / 2 | 0 / 0 |
| Hangul (fragment) | 240 | 240 | 2 | 240 / 2 | 0 / 0 |
| Continuation bytes only | 198 | 193 | 6 | 193 / 6 | 0 / 0 |
| ASCII | 97461 | 145 | 22 | 0 / 0 | 145 / 22 |
| Whitespace | 530 | 76 | 5 | 0 / 0 | 76 / 5 |
| Mixed (fragment) | 39 | 39 | 3 | 39 / 3 | 0 / 0 |
| Punctuation/symbols (fragment) | 31 | 30 | 2 | 30 / 2 | 0 / 0 |
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
| Cyrillic | 6513 | 2 | 1 | 0 / 0 | 2 / 1 |
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
| 3 | 60 | truncation_p32 | `                                ` | 32 | 792, 1961, 2623, 3425, 4672, 5351 … |
| 4 | 16 | truncation_p32 | ` -------------------------------` | 32 | 8633, 18527, 20308, 24793, 40473, 52914 … |
| 5 | 15 | truncation_p32 | `////////////////////////////////` | 32 | 3985, 10023, 28282, 28505, 29326, 36209 … |
| 6 | 15 | truncation_p32 | `/*******************************` | 32 | 11624, 20766, 23381, 26342, 37813, 54296 … |
| 7 | 14 | truncation_p32 | `//------------------------------` | 32 | 10089, 18498, 31989, 45242, 46914, 49356 … |
| 8 | 12 | truncation_p32 | ` *******************************` | 32 | 10757, 17994, 23089, 23814, 29744, 62460 … |
| 9 | 11 | truncation_p32 | `################################` | 32 | 5134, 13367, 30954, 33141, 41586, 70161 … |
| 10 | 9 | truncation_p32 | `--------------------------------` | 32 | 1434, 3597, 9411, 23151, 26972, 44549 … |
| 11 | 9 | truncation_p32 | `********************************` | 32 | 1724, 4169, 5713, 34618, 41172, 47676 … |
| 12 | 8 | truncation_p32 | ` ===============================` | 32 | 16563, 29685, 36874, 39468, 67000, 71762 … |
| 13 | 8 | truncation_p32 | `　　　　　　　　　　` | 30 | 101265, 106339, 107261, 109230, 111210, 113591 … |
| 14 | 5 | utf8_replacement | `�다` | 6 | 20541, 104828, 112039, 117653, 123375 |
| 15 | 5 | truncation_p32 | ` ###############################` | 32 | 49597, 55401, 68261, 87300, 94958 |
| 16 | 5 | utf8_replacement | `�i` | 4 | 100309, 100646, 103180, 103965, 104789 |
| 17 | 5 | utf8_replacement | `�ng` | 5 | 105394, 107280, 107454, 112245, 117523 |
| 18 | 4 | truncation_p32 | `================================` | 32 | 3134, 8315, 19311, 64494 |
| 19 | 4 | utf8_replacement | `�n` | 4 | 100859, 100938, 101792, 111972 |
| 20 | 4 | truncation_p32 | ` 　　　　　　　　　　` | 31 | 106892, 119582, 121864, 126234 |
| 21 | 3 | truncation_p32 | `//==============================` | 32 | 24036, 77607, 95403 |
| 22 | 3 | truncation_p32 | `/*------------------------------` | 32 | 30965, 59006, 74162 |
| 23 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 36719, 67104, 74638 |
| 24 | 3 | truncation_p32 | `//******************************` | 32 | 56363, 65326, 66180 |
| 25 | 3 | truncation_p32 | ` ///////////////////////////////` | 32 | 61709, 72608, 96280 |
| 26 | 2 | truncation_p32 | `................................` | 32 | 16971, 43369 |
| 27 | 2 | truncation_p32 | `________________________________` | 32 | 17924, 48032 |
| 28 | 2 | utf8_replacement | `ー�` | 6 | 25005, 38248 |
| 29 | 2 | utf8_replacement | `�数` | 6 | 28359, 31041 |
| 30 | 2 | truncation_p32 | `%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%` | 32 | 34109, 80618 |
| 31 | 2 | utf8_replacement | `��이` | 9 | 47318, 70483 |
| 32 | 2 | truncation_p32 | `#-------------------------------` | 32 | 62015, 76610 |
| 33 | 2 | utf8_replacement | `�이` | 6 | 63718, 103618 |
| 34 | 2 | utf8_replacement | `ا�` | 5 | 69350, 100257 |
| 35 | 2 | truncation_p32 | ` ...............................` | 32 | 82472, 87172 |
| 36 | 2 | truncation_p32 | ` /******************************` | 32 | 98105, 100089 |
| 37 | 2 | truncation_p32 | `џџџџџџџџџџџџџџџџ` | 32 | 100509, 101056 |
| 38 | 2 | utf8_replacement | `�a` | 4 | 103497, 112865 |
| 39 | 2 | truncation_p32 | `                ` | 32 | 104462, 115922 |
| 40 | 2 | truncation_p32 | `                     ` | 31 | 104786, 119224 |

All 41 groups. Member pieces and hex bytes: `results/llama-3.2/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 |
|---|---|---|---|---|
| ASCII | 97461 | 145 | 22 | 145 / 22 |
| Whitespace | 530 | 76 | 5 | 76 / 5 |
| Cyrillic | 6513 | 2 | 1 | 2 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 60 | truncation_p32 | `                                ` | 32 | 792, 1961, 2623, 3425, 4672, 5351 … |
| 1 | 16 | truncation_p32 | ` -------------------------------` | 32 | 8633, 18527, 20308, 24793, 40473, 52914 … |
| 2 | 15 | truncation_p32 | `////////////////////////////////` | 32 | 3985, 10023, 28282, 28505, 29326, 36209 … |
| 3 | 15 | truncation_p32 | `/*******************************` | 32 | 11624, 20766, 23381, 26342, 37813, 54296 … |
| 4 | 14 | truncation_p32 | `//------------------------------` | 32 | 10089, 18498, 31989, 45242, 46914, 49356 … |
| 5 | 12 | truncation_p32 | ` *******************************` | 32 | 10757, 17994, 23089, 23814, 29744, 62460 … |
| 6 | 11 | truncation_p32 | `################################` | 32 | 5134, 13367, 30954, 33141, 41586, 70161 … |
| 7 | 9 | truncation_p32 | `--------------------------------` | 32 | 1434, 3597, 9411, 23151, 26972, 44549 … |
| 8 | 9 | truncation_p32 | `********************************` | 32 | 1724, 4169, 5713, 34618, 41172, 47676 … |
| 9 | 8 | truncation_p32 | ` ===============================` | 32 | 16563, 29685, 36874, 39468, 67000, 71762 … |
| 10 | 8 | truncation_p32 | `　　　　　　　　　　` | 30 | 101265, 106339, 107261, 109230, 111210, 113591 … |
| 11 | 5 | truncation_p32 | ` ###############################` | 32 | 49597, 55401, 68261, 87300, 94958 |
| 12 | 4 | truncation_p32 | `================================` | 32 | 3134, 8315, 19311, 64494 |
| 13 | 4 | truncation_p32 | ` 　　　　　　　　　　` | 31 | 106892, 119582, 121864, 126234 |
| 14 | 3 | truncation_p32 | `//==============================` | 32 | 24036, 77607, 95403 |
| 15 | 3 | truncation_p32 | `/*------------------------------` | 32 | 30965, 59006, 74162 |
| 16 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 36719, 67104, 74638 |
| 17 | 3 | truncation_p32 | `//******************************` | 32 | 56363, 65326, 66180 |
| 18 | 3 | truncation_p32 | ` ///////////////////////////////` | 32 | 61709, 72608, 96280 |
| 19 | 2 | truncation_p32 | `................................` | 32 | 16971, 43369 |
| 20 | 2 | truncation_p32 | `________________________________` | 32 | 17924, 48032 |
| 21 | 2 | truncation_p32 | `%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%` | 32 | 34109, 80618 |
| 22 | 2 | truncation_p32 | `#-------------------------------` | 32 | 62015, 76610 |
| 23 | 2 | truncation_p32 | ` ...............................` | 32 | 82472, 87172 |
| 24 | 2 | truncation_p32 | ` /******************************` | 32 | 98105, 100089 |
| 25 | 2 | truncation_p32 | `џџџџџџџџџџџџџџџџ` | 32 | 100509, 101056 |
| 26 | 2 | truncation_p32 | `                ` | 32 | 104462, 115922 |
| 27 | 2 | truncation_p32 | `                     ` | 31 | 104786, 119224 |

All 28 groups. Member pieces and hex bytes: `results/llama-3.2/groups_raw.jsonl`.

## qwen3

Tokenizer `Qwen/Qwen3-32B` snapshot `9216db5781bf21249d130ec9da846c4624c16137`.

- V = 151,669; raw rows by rule: added_literal 12, model_bbpe 151,643, special 14
- rows where decode bytes ≠ raw bytes: 1,448; raw rows that are not valid UTF-8: 1,448
- tokens longer than 32 bytes: 240; of these, sharing a row with another token: 198
- decode table SHA-256 `a3f1f90b85c7fb39dd7e3a2b89d0881bd82248287d09a17eecf5355505701af8`
- raw table SHA-256 `70c9fd1f77ce95a3bac9d4ccddb86b041d10cf98f4379bdb2aa5243165e0d95d`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation_p32 |
|---|---|---|---|---|---|
| CJK Han (fragment) | 565 | 565 | 2 | 565 / 2 | 0 / 0 |
| Hangul (fragment) | 254 | 254 | 2 | 254 / 2 | 0 / 0 |
| ASCII | 93929 | 145 | 22 | 0 / 0 | 145 / 22 |
| Continuation bytes only | 132 | 132 | 2 | 132 / 2 | 0 / 0 |
| Other scripts (fragment) | 131 | 131 | 3 | 131 / 3 | 0 / 0 |
| Whitespace | 441 | 60 | 1 | 0 / 0 | 60 / 1 |
| Punctuation/symbols (fragment) | 51 | 50 | 2 | 50 / 2 | 0 / 0 |
| Emoji (fragment) | 47 | 47 | 2 | 47 / 2 | 0 / 0 |
| Mixed (fragment) | 39 | 39 | 3 | 39 / 3 | 0 / 0 |
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
| Thai | 2571 | 4 | 2 | 0 / 0 | 4 / 2 |
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
| 3 | 60 | truncation_p32 | `                                ` | 32 | 786, 1920, 2559, 3344, 4569, 5238 … |
| 4 | 16 | truncation_p32 | ` -------------------------------` | 32 | 8466, 18036, 19728, 23852, 39373, 51814 … |
| 5 | 15 | truncation_p32 | `////////////////////////////////` | 32 | 3898, 9822, 27183, 27405, 28226, 35109 … |
| 6 | 15 | truncation_p32 | `/*******************************` | 32 | 11370, 20159, 22565, 25275, 36713, 53196 … |
| 7 | 14 | truncation_p32 | `//------------------------------` | 32 | 9888, 18012, 30889, 44142, 45814, 48256 … |
| 8 | 12 | truncation_p32 | ` *******************************` | 32 | 10534, 17535, 22292, 22958, 28644, 61360 … |
| 9 | 11 | truncation_p32 | `################################` | 32 | 5026, 13067, 29854, 32041, 40486, 69061 … |
| 10 | 9 | truncation_p32 | `--------------------------------` | 32 | 1408, 3513, 9229, 22349, 25885, 43449 … |
| 11 | 9 | truncation_p32 | `********************************` | 32 | 1689, 4077, 5596, 33518, 40072, 46576 … |
| 12 | 8 | truncation_p32 | ` ===============================` | 32 | 16168, 28585, 35774, 38368, 65900, 70662 … |
| 13 | 5 | truncation_p32 | ` ###############################` | 32 | 48497, 54301, 67161, 86200, 93858 |
| 14 | 4 | truncation_p32 | `================================` | 32 | 3058, 8152, 18782, 63394 |
| 15 | 3 | truncation_p32 | `//==============================` | 32 | 23161, 76507, 94303 |
| 16 | 3 | truncation_p32 | `/*------------------------------` | 32 | 29865, 57906, 73062 |
| 17 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 35619, 66004, 73538 |
| 18 | 3 | truncation_p32 | `//******************************` | 32 | 55263, 64226, 65080 |
| 19 | 3 | truncation_p32 | ` ///////////////////////////////` | 32 | 60609, 71508, 95180 |
| 20 | 3 | utf8_replacement | `珊�` | 6 | 119346, 119347, 119348 |
| 21 | 2 | truncation_p32 | `................................` | 32 | 16562, 42269 |
| 22 | 2 | truncation_p32 | `________________________________` | 32 | 17466, 46932 |
| 23 | 2 | utf8_replacement | `ー�` | 6 | 24041, 37148 |
| 24 | 2 | utf8_replacement | `�数` | 6 | 27260, 29941 |
| 25 | 2 | truncation_p32 | `%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%` | 32 | 33009, 79518 |
| 26 | 2 | utf8_replacement | `ו�` | 5 | 36669, 127572 |
| 27 | 2 | utf8_replacement | `��이` | 9 | 46218, 69383 |
| 28 | 2 | truncation_p32 | `#-------------------------------` | 32 | 60915, 75510 |
| 29 | 2 | truncation_p32 | ` ...............................` | 32 | 81372, 86072 |
| 30 | 2 | truncation_p32 | ` /******************************` | 32 | 97005, 98989 |
| 31 | 2 | utf8_replacement | `に�` | 6 | 127124, 137973 |
| 32 | 2 | utf8_replacement | `ご�` | 6 | 135078, 139816 |
| 33 | 2 | truncation_p32 | `เปลี่ยนแปล` | 30 | 135287, 135288 |
| 34 | 2 | truncation_p32 | `ที่เกี่ยวข` | 30 | 135313, 135314 |
| 35 | 2 | utf8_replacement | ` 오�` | 7 | 142209, 142210 |

All 36 groups. Member pieces and hex bytes: `results/qwen3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 |
|---|---|---|---|---|
| ASCII | 93929 | 145 | 22 | 145 / 22 |
| Whitespace | 441 | 60 | 1 | 60 / 1 |
| Thai | 2571 | 4 | 2 | 4 / 2 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 60 | truncation_p32 | `                                ` | 32 | 786, 1920, 2559, 3344, 4569, 5238 … |
| 1 | 16 | truncation_p32 | ` -------------------------------` | 32 | 8466, 18036, 19728, 23852, 39373, 51814 … |
| 2 | 15 | truncation_p32 | `////////////////////////////////` | 32 | 3898, 9822, 27183, 27405, 28226, 35109 … |
| 3 | 15 | truncation_p32 | `/*******************************` | 32 | 11370, 20159, 22565, 25275, 36713, 53196 … |
| 4 | 14 | truncation_p32 | `//------------------------------` | 32 | 9888, 18012, 30889, 44142, 45814, 48256 … |
| 5 | 12 | truncation_p32 | ` *******************************` | 32 | 10534, 17535, 22292, 22958, 28644, 61360 … |
| 6 | 11 | truncation_p32 | `################################` | 32 | 5026, 13067, 29854, 32041, 40486, 69061 … |
| 7 | 9 | truncation_p32 | `--------------------------------` | 32 | 1408, 3513, 9229, 22349, 25885, 43449 … |
| 8 | 9 | truncation_p32 | `********************************` | 32 | 1689, 4077, 5596, 33518, 40072, 46576 … |
| 9 | 8 | truncation_p32 | ` ===============================` | 32 | 16168, 28585, 35774, 38368, 65900, 70662 … |
| 10 | 5 | truncation_p32 | ` ###############################` | 32 | 48497, 54301, 67161, 86200, 93858 |
| 11 | 4 | truncation_p32 | `================================` | 32 | 3058, 8152, 18782, 63394 |
| 12 | 3 | truncation_p32 | `//==============================` | 32 | 23161, 76507, 94303 |
| 13 | 3 | truncation_p32 | `/*------------------------------` | 32 | 29865, 57906, 73062 |
| 14 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 35619, 66004, 73538 |
| 15 | 3 | truncation_p32 | `//******************************` | 32 | 55263, 64226, 65080 |
| 16 | 3 | truncation_p32 | ` ///////////////////////////////` | 32 | 60609, 71508, 95180 |
| 17 | 2 | truncation_p32 | `................................` | 32 | 16562, 42269 |
| 18 | 2 | truncation_p32 | `________________________________` | 32 | 17466, 46932 |
| 19 | 2 | truncation_p32 | `%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%` | 32 | 33009, 79518 |
| 20 | 2 | truncation_p32 | `#-------------------------------` | 32 | 60915, 75510 |
| 21 | 2 | truncation_p32 | ` ...............................` | 32 | 81372, 86072 |
| 22 | 2 | truncation_p32 | ` /******************************` | 32 | 97005, 98989 |
| 23 | 2 | truncation_p32 | `เปลี่ยนแปล` | 30 | 135287, 135288 |
| 24 | 2 | truncation_p32 | `ที่เกี่ยวข` | 30 | 135313, 135314 |

All 25 groups. Member pieces and hex bytes: `results/qwen3/groups_raw.jsonl`.

## gemma-3

Tokenizer `unsloth/gemma-3-1b-pt` snapshot `34a98bf3eaecc08c699516f625eb5e56e4c5d99d`.

- V = 262,145; raw rows by rule: byte_fallback 256, model_sp 261,881, special 8
- rows where decode bytes ≠ raw bytes: 0; raw rows that are not valid UTF-8: 128
- tokens longer than 32 bytes: 379; of these, sharing a row with another token: 86
- decode table SHA-256 `a76c712edf3ed29c8c1cf0f243d6fa3a03e01782f942e660cf5884118e92dd80`
- raw table SHA-256 `a76c712edf3ed29c8c1cf0f243d6fa3a03e01782f942e660cf5884118e92dd80`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 | byte_fallback_alias |
|---|---|---|---|---|---|
| ASCII | 150314 | 212 | 106 | 0 / 0 | 212 / 106 |
| Bengali | 9979 | 63 | 25 | 63 / 25 | 0 / 0 |
| Devanagari | 13750 | 25 | 12 | 25 / 12 | 0 / 0 |
| Tamil | 3850 | 22 | 9 | 22 / 9 | 0 / 0 |
| Whitespace | 104 | 8 | 4 | 0 / 0 | 8 / 4 |
| Thai | 2177 | 2 | 1 | 2 / 1 | 0 / 0 |
| Malayalam | 1955 | 2 | 1 | 2 / 1 | 0 / 0 |
| Punctuation/symbols | 1033 | 2 | 1 | 2 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 5 | truncation_p32 | ` বিশ্ববিদ্য` | 31 | 31827, 79140, 80645, 102142, 172141 |
| 1 | 4 | truncation_p32 | ` হোমিওপ্যাথ` | 31 | 47143, 95440, 110732, 127176 |
| 2 | 4 | truncation_p32 | ` মুক্তিযোদ্` | 31 | 68407, 118542, 168586, 233497 |
| 3 | 4 | truncation_p32 | ` শিক্ষার্থী` | 31 | 91831, 94921, 182879, 227203 |
| 4 | 3 | truncation_p32 | ` সেনাবাহিনী` | 31 | 41431, 48193, 157740 |
| 5 | 3 | truncation_p32 | ` পাকিস্তানী` | 31 | 45926, 134121, 201092 |
| 6 | 3 | truncation_p32 | `ப்பட்டுள்ள` | 30 | 47185, 60382, 122908 |
| 7 | 3 | truncation_p32 | ` பயன்படுத்த` | 31 | 47218, 112474, 144422 |
| 8 | 3 | truncation_p32 | ` পশ্চিমবঙ্গ` | 31 | 68215, 112883, 177774 |
| 9 | 3 | truncation_p32 | ` যুক্তরাষ্ট` | 31 | 70627, 122461, 187774 |
| 10 | 3 | truncation_p32 | ` विद्यार्थ्` | 31 | 85498, 186967, 231582 |
| 11 | 3 | truncation_p32 | ` செய்யப்பட்` | 31 | 133892, 164117, 199256 |
| 12 | 3 | truncation_p32 | ` ஏற்படுத்து` | 31 | 148446, 152558, 191917 |
| 13 | 2 | byte_fallback_alias | `\n` | 1 | 107, 248 |
| 14 | 2 | byte_fallback_alias | `` | 1 | 239, 249732 |
| 15 | 2 | byte_fallback_alias | `` | 1 | 240, 241247 |
| 16 | 2 | byte_fallback_alias | `` | 1 | 241, 247953 |
| 17 | 2 | byte_fallback_alias | `` | 1 | 243, 251303 |
| 18 | 2 | byte_fallback_alias | `` | 1 | 246, 243480 |
| 19 | 2 | byte_fallback_alias | `\t` | 1 | 247, 255968 |
| 20 | 2 | byte_fallback_alias | `` | 1 | 256, 248894 |
| 21 | 2 | byte_fallback_alias | `` | 1 | 257, 252295 |
| 22 | 2 | byte_fallback_alias | `` | 1 | 258, 255321 |
| 23 | 2 | byte_fallback_alias | `` | 1 | 261, 252786 |
| 24 | 2 | byte_fallback_alias | `` | 1 | 264, 255485 |
| 25 | 2 | byte_fallback_alias | `` | 1 | 265, 239473 |
| 26 | 2 | byte_fallback_alias | `` | 1 | 269, 253998 |
| 27 | 2 | byte_fallback_alias | ` ` | 1 | 270, 236743 |
| 28 | 2 | byte_fallback_alias | `!` | 1 | 271, 236888 |
| 29 | 2 | byte_fallback_alias | `"` | 1 | 272, 236775 |
| 30 | 2 | byte_fallback_alias | `#` | 1 | 273, 236865 |
| 31 | 2 | byte_fallback_alias | `$` | 1 | 274, 236795 |
| 32 | 2 | byte_fallback_alias | `%` | 1 | 275, 236908 |
| 33 | 2 | byte_fallback_alias | `&` | 1 | 276, 236880 |
| 34 | 2 | byte_fallback_alias | `'` | 1 | 277, 236789 |
| 35 | 2 | byte_fallback_alias | `(` | 1 | 278, 236769 |
| 36 | 2 | byte_fallback_alias | `)` | 1 | 279, 236768 |
| 37 | 2 | byte_fallback_alias | `*` | 1 | 280, 236829 |
| 38 | 2 | byte_fallback_alias | `+` | 1 | 281, 236862 |
| 39 | 2 | byte_fallback_alias | `,` | 1 | 282, 236764 |
| 40 | 2 | byte_fallback_alias | `-` | 1 | 283, 236772 |
| 41 | 2 | byte_fallback_alias | `.` | 1 | 284, 236761 |
| 42 | 2 | byte_fallback_alias | `/` | 1 | 285, 236786 |
| 43 | 2 | byte_fallback_alias | `0` | 1 | 286, 236771 |
| 44 | 2 | byte_fallback_alias | `1` | 1 | 287, 236770 |
| 45 | 2 | byte_fallback_alias | `2` | 1 | 288, 236778 |
| 46 | 2 | byte_fallback_alias | `3` | 1 | 289, 236800 |
| 47 | 2 | byte_fallback_alias | `4` | 1 | 290, 236812 |
| 48 | 2 | byte_fallback_alias | `5` | 1 | 291, 236810 |
| 49 | 2 | byte_fallback_alias | `6` | 1 | 292, 236825 |
| 50 | 2 | byte_fallback_alias | `7` | 1 | 293, 236832 |
| 51 | 2 | byte_fallback_alias | `8` | 1 | 294, 236828 |
| 52 | 2 | byte_fallback_alias | `9` | 1 | 295, 236819 |
| 53 | 2 | byte_fallback_alias | `:` | 1 | 296, 236787 |
| 54 | 2 | byte_fallback_alias | `;` | 1 | 297, 236793 |
| 55 | 2 | byte_fallback_alias | `<` | 1 | 298, 236820 |
| 56 | 2 | byte_fallback_alias | `=` | 1 | 299, 236784 |
| 57 | 2 | byte_fallback_alias | `>` | 1 | 300, 236813 |
| 58 | 2 | byte_fallback_alias | `?` | 1 | 301, 236881 |
| 59 | 2 | byte_fallback_alias | `@` | 1 | 302, 236940 |
| 60 | 2 | byte_fallback_alias | `A` | 1 | 303, 236776 |
| 61 | 2 | byte_fallback_alias | `B` | 1 | 304, 236799 |
| 62 | 2 | byte_fallback_alias | `C` | 1 | 305, 236780 |
| 63 | 2 | byte_fallback_alias | `D` | 1 | 306, 236796 |
| 64 | 2 | byte_fallback_alias | `E` | 1 | 307, 236788 |
| 65 | 2 | byte_fallback_alias | `F` | 1 | 308, 236811 |
| 66 | 2 | byte_fallback_alias | `G` | 1 | 309, 236823 |
| 67 | 2 | byte_fallback_alias | `H` | 1 | 310, 236814 |
| 68 | 2 | byte_fallback_alias | `I` | 1 | 311, 236777 |
| 69 | 2 | byte_fallback_alias | `J` | 1 | 312, 236863 |
| 70 | 2 | byte_fallback_alias | `K` | 1 | 313, 236855 |
| 71 | 2 | byte_fallback_alias | `L` | 1 | 314, 236798 |
| 72 | 2 | byte_fallback_alias | `M` | 1 | 315, 236792 |
| 73 | 2 | byte_fallback_alias | `N` | 1 | 316, 236797 |
| 74 | 2 | byte_fallback_alias | `O` | 1 | 317, 236806 |
| 75 | 2 | byte_fallback_alias | `P` | 1 | 318, 236791 |
| 76 | 2 | byte_fallback_alias | `Q` | 1 | 319, 236935 |
| 77 | 2 | byte_fallback_alias | `R` | 1 | 320, 236794 |
| 78 | 2 | byte_fallback_alias | `S` | 1 | 321, 236773 |
| 79 | 2 | byte_fallback_alias | `T` | 1 | 322, 236774 |
| 80 | 2 | byte_fallback_alias | `U` | 1 | 323, 236836 |
| 81 | 2 | byte_fallback_alias | `V` | 1 | 324, 236847 |
| 82 | 2 | byte_fallback_alias | `W` | 1 | 325, 236824 |
| 83 | 2 | byte_fallback_alias | `X` | 1 | 326, 236917 |
| 84 | 2 | byte_fallback_alias | `Y` | 1 | 327, 236874 |
| 85 | 2 | byte_fallback_alias | `Z` | 1 | 328, 236953 |
| 86 | 2 | byte_fallback_alias | `[` | 1 | 329, 236840 |
| 87 | 2 | byte_fallback_alias | `\` | 1 | 330, 236785 |
| 88 | 2 | byte_fallback_alias | `]` | 1 | 331, 236842 |
| 89 | 2 | byte_fallback_alias | `^` | 1 | 332, 236884 |
| 90 | 2 | byte_fallback_alias | `_` | 1 | 333, 236779 |
| 91 | 2 | byte_fallback_alias | `'` | 1 | 334, 236929 |
| 92 | 2 | byte_fallback_alias | `a` | 1 | 335, 236746 |
| 93 | 2 | byte_fallback_alias | `b` | 1 | 336, 236763 |
| 94 | 2 | byte_fallback_alias | `c` | 1 | 337, 236755 |
| 95 | 2 | byte_fallback_alias | `d` | 1 | 338, 236753 |
| 96 | 2 | byte_fallback_alias | `e` | 1 | 339, 236744 |
| 97 | 2 | byte_fallback_alias | `f` | 1 | 340, 236760 |
| 98 | 2 | byte_fallback_alias | `g` | 1 | 341, 236759 |
| 99 | 2 | byte_fallback_alias | `h` | 1 | 342, 236754 |
| 100 | 2 | byte_fallback_alias | `i` | 1 | 343, 236747 |
| 101 | 2 | byte_fallback_alias | `j` | 1 | 344, 236804 |
| 102 | 2 | byte_fallback_alias | `k` | 1 | 345, 236767 |
| 103 | 2 | byte_fallback_alias | `l` | 1 | 346, 236752 |
| 104 | 2 | byte_fallback_alias | `m` | 1 | 347, 236757 |
| 105 | 2 | byte_fallback_alias | `n` | 1 | 348, 236749 |
| 106 | 2 | byte_fallback_alias | `o` | 1 | 349, 236748 |
| 107 | 2 | byte_fallback_alias | `p` | 1 | 350, 236758 |
| 108 | 2 | byte_fallback_alias | `q` | 1 | 351, 236809 |
| 109 | 2 | byte_fallback_alias | `r` | 1 | 352, 236750 |
| 110 | 2 | byte_fallback_alias | `s` | 1 | 353, 236751 |
| 111 | 2 | byte_fallback_alias | `t` | 1 | 354, 236745 |
| 112 | 2 | byte_fallback_alias | `u` | 1 | 355, 236756 |
| 113 | 2 | byte_fallback_alias | `v` | 1 | 356, 236766 |
| 114 | 2 | byte_fallback_alias | `w` | 1 | 357, 236765 |
| 115 | 2 | byte_fallback_alias | `x` | 1 | 358, 236781 |
| 116 | 2 | byte_fallback_alias | `y` | 1 | 359, 236762 |
| 117 | 2 | byte_fallback_alias | `z` | 1 | 360, 236802 |
| 118 | 2 | byte_fallback_alias | `{` | 1 | 361, 236782 |
| 119 | 2 | byte_fallback_alias | `\|` | 1 | 362, 236909 |
| 120 | 2 | byte_fallback_alias | `}` | 1 | 363, 236783 |
| 121 | 2 | byte_fallback_alias | `~` | 1 | 364, 236995 |
| 122 | 2 | byte_fallback_alias | `` | 1 | 365, 251541 |
| 123 | 2 | truncation_p32 | ` পাকিস্তানে` | 31 | 14443, 30560 |
| 124 | 2 | truncation_p32 | ` পাকিস্তানি` | 31 | 32942, 149105 |
| 125 | 2 | truncation_p32 | ` প্রেসিডেন্` | 31 | 39010, 234815 |
| 126 | 2 | truncation_p32 | ` প্রধানমন্ত` | 31 | 43862, 141757 |
| 127 | 2 | truncation_p32 | ` विश्वविद्य` | 31 | 47661, 163304 |
| 128 | 2 | truncation_p32 | ` महाराष्ट्र` | 31 | 54835, 119317 |
| 129 | 2 | truncation_p32 | ` প্রতিষ্ঠান` | 31 | 64817, 137344 |
| 130 | 2 | truncation_p32 | ` ऑस्ट्रेलिय` | 31 | 67672, 204664 |
| 131 | 2 | truncation_p32 | ` कार्यकर्ता` | 31 | 79602, 84099 |
| 132 | 2 | truncation_p32 | ` इलेक्ट्रॉन` | 31 | 82771, 111957 |
| 133 | 2 | truncation_p32 | ` डॉक्यूमेंट` | 31 | 94375, 193089 |
| 134 | 2 | truncation_p32 | ` दुष्प्रभाव` | 31 | 100505, 184523 |
| 135 | 2 | truncation_p32 | `แมนเชสเตอร` | 30 | 101035, 149179 |
| 136 | 2 | truncation_p32 | ` মুক্তিযুদ্` | 31 | 101896, 158974 |
| 137 | 2 | truncation_p32 | ` নিয়ন্ত্রণ` | 31 | 103066, 208736 |
| 138 | 2 | truncation_p32 | ` சுற்றுச்சூ` | 31 | 107696, 139167 |
| 139 | 2 | truncation_p32 | ` কর্মকর্তার` | 31 | 108268, 227015 |
| 140 | 2 | truncation_p32 | `…………………………` | 30 | 118132, 207014 |
| 141 | 2 | truncation_p32 | ` মন্ত্রণালয়` | 31 | 122495, 142371 |
| 142 | 2 | truncation_p32 | ` क्रिप्टोकर` | 31 | 126064, 162859 |
| 143 | 2 | truncation_p32 | ` அமைந்துள்ள` | 31 | 128456, 162662 |
| 144 | 2 | truncation_p32 | ` प्रतिस्पर्` | 31 | 130631, 206672 |
| 145 | 2 | truncation_p32 | ` আর্জেন্টিন` | 31 | 138017, 167288 |
| 146 | 2 | truncation_p32 | ` মুক্তিবাহি` | 31 | 147706, 150776 |
| 147 | 2 | truncation_p32 | ` পূর্ববাংলা` | 31 | 150872, 169566 |
| 148 | 2 | truncation_p32 | ` চট্টগ্রামে` | 31 | 151265, 222217 |
| 149 | 2 | truncation_p32 | ` ইউনিভার্সি` | 31 | 151487, 193141 |
| 150 | 2 | truncation_p32 | ` நூற்றாண்டி` | 31 | 153887, 185456 |
| 151 | 2 | truncation_p32 | ` उपयोगकर्ता` | 31 | 156774, 181505 |
| 152 | 2 | truncation_p32 | ` क्रांतिकार` | 31 | 159923, 221109 |
| 153 | 2 | truncation_p32 | ` குறிப்பிட்` | 31 | 163284, 233971 |
| 154 | 2 | truncation_p32 | ` வால்பேப்பர` | 31 | 165413, 231638 |
| 155 | 2 | truncation_p32 | ` আনুষ্ঠানিক` | 31 | 178234, 178901 |
| 156 | 2 | truncation_p32 | ` പ്രവര്‍ത്ത` | 31 | 183688, 227415 |
| 157 | 2 | truncation_p32 | ` সিদ্ধান্তে` | 31 | 212837, 217147 |
| 158 | 2 | truncation_p32 | ` চলচ্চিত্রে` | 31 | 218376, 230506 |

All 159 groups. Member pieces and hex bytes: `results/gemma-3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 | byte_fallback_alias |
|---|---|---|---|---|---|
| ASCII | 150314 | 212 | 106 | 0 / 0 | 212 / 106 |
| Bengali | 9979 | 63 | 25 | 63 / 25 | 0 / 0 |
| Devanagari | 13750 | 25 | 12 | 25 / 12 | 0 / 0 |
| Tamil | 3850 | 22 | 9 | 22 / 9 | 0 / 0 |
| Whitespace | 104 | 8 | 4 | 0 / 0 | 8 / 4 |
| Thai | 2177 | 2 | 1 | 2 / 1 | 0 / 0 |
| Malayalam | 1955 | 2 | 1 | 2 / 1 | 0 / 0 |
| Punctuation/symbols | 1033 | 2 | 1 | 2 / 1 | 0 / 0 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 5 | truncation_p32 | ` বিশ্ববিদ্য` | 31 | 31827, 79140, 80645, 102142, 172141 |
| 1 | 4 | truncation_p32 | ` হোমিওপ্যাথ` | 31 | 47143, 95440, 110732, 127176 |
| 2 | 4 | truncation_p32 | ` মুক্তিযোদ্` | 31 | 68407, 118542, 168586, 233497 |
| 3 | 4 | truncation_p32 | ` শিক্ষার্থী` | 31 | 91831, 94921, 182879, 227203 |
| 4 | 3 | truncation_p32 | ` সেনাবাহিনী` | 31 | 41431, 48193, 157740 |
| 5 | 3 | truncation_p32 | ` পাকিস্তানী` | 31 | 45926, 134121, 201092 |
| 6 | 3 | truncation_p32 | `ப்பட்டுள்ள` | 30 | 47185, 60382, 122908 |
| 7 | 3 | truncation_p32 | ` பயன்படுத்த` | 31 | 47218, 112474, 144422 |
| 8 | 3 | truncation_p32 | ` পশ্চিমবঙ্গ` | 31 | 68215, 112883, 177774 |
| 9 | 3 | truncation_p32 | ` যুক্তরাষ্ট` | 31 | 70627, 122461, 187774 |
| 10 | 3 | truncation_p32 | ` विद्यार्थ्` | 31 | 85498, 186967, 231582 |
| 11 | 3 | truncation_p32 | ` செய்யப்பட்` | 31 | 133892, 164117, 199256 |
| 12 | 3 | truncation_p32 | ` ஏற்படுத்து` | 31 | 148446, 152558, 191917 |
| 13 | 2 | byte_fallback_alias | `\n` | 1 | 107, 248 |
| 14 | 2 | byte_fallback_alias | `` | 1 | 239, 249732 |
| 15 | 2 | byte_fallback_alias | `` | 1 | 240, 241247 |
| 16 | 2 | byte_fallback_alias | `` | 1 | 241, 247953 |
| 17 | 2 | byte_fallback_alias | `` | 1 | 243, 251303 |
| 18 | 2 | byte_fallback_alias | `` | 1 | 246, 243480 |
| 19 | 2 | byte_fallback_alias | `\t` | 1 | 247, 255968 |
| 20 | 2 | byte_fallback_alias | `` | 1 | 256, 248894 |
| 21 | 2 | byte_fallback_alias | `` | 1 | 257, 252295 |
| 22 | 2 | byte_fallback_alias | `` | 1 | 258, 255321 |
| 23 | 2 | byte_fallback_alias | `` | 1 | 261, 252786 |
| 24 | 2 | byte_fallback_alias | `` | 1 | 264, 255485 |
| 25 | 2 | byte_fallback_alias | `` | 1 | 265, 239473 |
| 26 | 2 | byte_fallback_alias | `` | 1 | 269, 253998 |
| 27 | 2 | byte_fallback_alias | ` ` | 1 | 270, 236743 |
| 28 | 2 | byte_fallback_alias | `!` | 1 | 271, 236888 |
| 29 | 2 | byte_fallback_alias | `"` | 1 | 272, 236775 |
| 30 | 2 | byte_fallback_alias | `#` | 1 | 273, 236865 |
| 31 | 2 | byte_fallback_alias | `$` | 1 | 274, 236795 |
| 32 | 2 | byte_fallback_alias | `%` | 1 | 275, 236908 |
| 33 | 2 | byte_fallback_alias | `&` | 1 | 276, 236880 |
| 34 | 2 | byte_fallback_alias | `'` | 1 | 277, 236789 |
| 35 | 2 | byte_fallback_alias | `(` | 1 | 278, 236769 |
| 36 | 2 | byte_fallback_alias | `)` | 1 | 279, 236768 |
| 37 | 2 | byte_fallback_alias | `*` | 1 | 280, 236829 |
| 38 | 2 | byte_fallback_alias | `+` | 1 | 281, 236862 |
| 39 | 2 | byte_fallback_alias | `,` | 1 | 282, 236764 |
| 40 | 2 | byte_fallback_alias | `-` | 1 | 283, 236772 |
| 41 | 2 | byte_fallback_alias | `.` | 1 | 284, 236761 |
| 42 | 2 | byte_fallback_alias | `/` | 1 | 285, 236786 |
| 43 | 2 | byte_fallback_alias | `0` | 1 | 286, 236771 |
| 44 | 2 | byte_fallback_alias | `1` | 1 | 287, 236770 |
| 45 | 2 | byte_fallback_alias | `2` | 1 | 288, 236778 |
| 46 | 2 | byte_fallback_alias | `3` | 1 | 289, 236800 |
| 47 | 2 | byte_fallback_alias | `4` | 1 | 290, 236812 |
| 48 | 2 | byte_fallback_alias | `5` | 1 | 291, 236810 |
| 49 | 2 | byte_fallback_alias | `6` | 1 | 292, 236825 |
| 50 | 2 | byte_fallback_alias | `7` | 1 | 293, 236832 |
| 51 | 2 | byte_fallback_alias | `8` | 1 | 294, 236828 |
| 52 | 2 | byte_fallback_alias | `9` | 1 | 295, 236819 |
| 53 | 2 | byte_fallback_alias | `:` | 1 | 296, 236787 |
| 54 | 2 | byte_fallback_alias | `;` | 1 | 297, 236793 |
| 55 | 2 | byte_fallback_alias | `<` | 1 | 298, 236820 |
| 56 | 2 | byte_fallback_alias | `=` | 1 | 299, 236784 |
| 57 | 2 | byte_fallback_alias | `>` | 1 | 300, 236813 |
| 58 | 2 | byte_fallback_alias | `?` | 1 | 301, 236881 |
| 59 | 2 | byte_fallback_alias | `@` | 1 | 302, 236940 |
| 60 | 2 | byte_fallback_alias | `A` | 1 | 303, 236776 |
| 61 | 2 | byte_fallback_alias | `B` | 1 | 304, 236799 |
| 62 | 2 | byte_fallback_alias | `C` | 1 | 305, 236780 |
| 63 | 2 | byte_fallback_alias | `D` | 1 | 306, 236796 |
| 64 | 2 | byte_fallback_alias | `E` | 1 | 307, 236788 |
| 65 | 2 | byte_fallback_alias | `F` | 1 | 308, 236811 |
| 66 | 2 | byte_fallback_alias | `G` | 1 | 309, 236823 |
| 67 | 2 | byte_fallback_alias | `H` | 1 | 310, 236814 |
| 68 | 2 | byte_fallback_alias | `I` | 1 | 311, 236777 |
| 69 | 2 | byte_fallback_alias | `J` | 1 | 312, 236863 |
| 70 | 2 | byte_fallback_alias | `K` | 1 | 313, 236855 |
| 71 | 2 | byte_fallback_alias | `L` | 1 | 314, 236798 |
| 72 | 2 | byte_fallback_alias | `M` | 1 | 315, 236792 |
| 73 | 2 | byte_fallback_alias | `N` | 1 | 316, 236797 |
| 74 | 2 | byte_fallback_alias | `O` | 1 | 317, 236806 |
| 75 | 2 | byte_fallback_alias | `P` | 1 | 318, 236791 |
| 76 | 2 | byte_fallback_alias | `Q` | 1 | 319, 236935 |
| 77 | 2 | byte_fallback_alias | `R` | 1 | 320, 236794 |
| 78 | 2 | byte_fallback_alias | `S` | 1 | 321, 236773 |
| 79 | 2 | byte_fallback_alias | `T` | 1 | 322, 236774 |
| 80 | 2 | byte_fallback_alias | `U` | 1 | 323, 236836 |
| 81 | 2 | byte_fallback_alias | `V` | 1 | 324, 236847 |
| 82 | 2 | byte_fallback_alias | `W` | 1 | 325, 236824 |
| 83 | 2 | byte_fallback_alias | `X` | 1 | 326, 236917 |
| 84 | 2 | byte_fallback_alias | `Y` | 1 | 327, 236874 |
| 85 | 2 | byte_fallback_alias | `Z` | 1 | 328, 236953 |
| 86 | 2 | byte_fallback_alias | `[` | 1 | 329, 236840 |
| 87 | 2 | byte_fallback_alias | `\` | 1 | 330, 236785 |
| 88 | 2 | byte_fallback_alias | `]` | 1 | 331, 236842 |
| 89 | 2 | byte_fallback_alias | `^` | 1 | 332, 236884 |
| 90 | 2 | byte_fallback_alias | `_` | 1 | 333, 236779 |
| 91 | 2 | byte_fallback_alias | `'` | 1 | 334, 236929 |
| 92 | 2 | byte_fallback_alias | `a` | 1 | 335, 236746 |
| 93 | 2 | byte_fallback_alias | `b` | 1 | 336, 236763 |
| 94 | 2 | byte_fallback_alias | `c` | 1 | 337, 236755 |
| 95 | 2 | byte_fallback_alias | `d` | 1 | 338, 236753 |
| 96 | 2 | byte_fallback_alias | `e` | 1 | 339, 236744 |
| 97 | 2 | byte_fallback_alias | `f` | 1 | 340, 236760 |
| 98 | 2 | byte_fallback_alias | `g` | 1 | 341, 236759 |
| 99 | 2 | byte_fallback_alias | `h` | 1 | 342, 236754 |
| 100 | 2 | byte_fallback_alias | `i` | 1 | 343, 236747 |
| 101 | 2 | byte_fallback_alias | `j` | 1 | 344, 236804 |
| 102 | 2 | byte_fallback_alias | `k` | 1 | 345, 236767 |
| 103 | 2 | byte_fallback_alias | `l` | 1 | 346, 236752 |
| 104 | 2 | byte_fallback_alias | `m` | 1 | 347, 236757 |
| 105 | 2 | byte_fallback_alias | `n` | 1 | 348, 236749 |
| 106 | 2 | byte_fallback_alias | `o` | 1 | 349, 236748 |
| 107 | 2 | byte_fallback_alias | `p` | 1 | 350, 236758 |
| 108 | 2 | byte_fallback_alias | `q` | 1 | 351, 236809 |
| 109 | 2 | byte_fallback_alias | `r` | 1 | 352, 236750 |
| 110 | 2 | byte_fallback_alias | `s` | 1 | 353, 236751 |
| 111 | 2 | byte_fallback_alias | `t` | 1 | 354, 236745 |
| 112 | 2 | byte_fallback_alias | `u` | 1 | 355, 236756 |
| 113 | 2 | byte_fallback_alias | `v` | 1 | 356, 236766 |
| 114 | 2 | byte_fallback_alias | `w` | 1 | 357, 236765 |
| 115 | 2 | byte_fallback_alias | `x` | 1 | 358, 236781 |
| 116 | 2 | byte_fallback_alias | `y` | 1 | 359, 236762 |
| 117 | 2 | byte_fallback_alias | `z` | 1 | 360, 236802 |
| 118 | 2 | byte_fallback_alias | `{` | 1 | 361, 236782 |
| 119 | 2 | byte_fallback_alias | `\|` | 1 | 362, 236909 |
| 120 | 2 | byte_fallback_alias | `}` | 1 | 363, 236783 |
| 121 | 2 | byte_fallback_alias | `~` | 1 | 364, 236995 |
| 122 | 2 | byte_fallback_alias | `` | 1 | 365, 251541 |
| 123 | 2 | truncation_p32 | ` পাকিস্তানে` | 31 | 14443, 30560 |
| 124 | 2 | truncation_p32 | ` পাকিস্তানি` | 31 | 32942, 149105 |
| 125 | 2 | truncation_p32 | ` প্রেসিডেন্` | 31 | 39010, 234815 |
| 126 | 2 | truncation_p32 | ` প্রধানমন্ত` | 31 | 43862, 141757 |
| 127 | 2 | truncation_p32 | ` विश्वविद्य` | 31 | 47661, 163304 |
| 128 | 2 | truncation_p32 | ` महाराष्ट्र` | 31 | 54835, 119317 |
| 129 | 2 | truncation_p32 | ` প্রতিষ্ঠান` | 31 | 64817, 137344 |
| 130 | 2 | truncation_p32 | ` ऑस्ट्रेलिय` | 31 | 67672, 204664 |
| 131 | 2 | truncation_p32 | ` कार्यकर्ता` | 31 | 79602, 84099 |
| 132 | 2 | truncation_p32 | ` इलेक्ट्रॉन` | 31 | 82771, 111957 |
| 133 | 2 | truncation_p32 | ` डॉक्यूमेंट` | 31 | 94375, 193089 |
| 134 | 2 | truncation_p32 | ` दुष्प्रभाव` | 31 | 100505, 184523 |
| 135 | 2 | truncation_p32 | `แมนเชสเตอร` | 30 | 101035, 149179 |
| 136 | 2 | truncation_p32 | ` মুক্তিযুদ্` | 31 | 101896, 158974 |
| 137 | 2 | truncation_p32 | ` নিয়ন্ত্রণ` | 31 | 103066, 208736 |
| 138 | 2 | truncation_p32 | ` சுற்றுச்சூ` | 31 | 107696, 139167 |
| 139 | 2 | truncation_p32 | ` কর্মকর্তার` | 31 | 108268, 227015 |
| 140 | 2 | truncation_p32 | `…………………………` | 30 | 118132, 207014 |
| 141 | 2 | truncation_p32 | ` মন্ত্রণালয়` | 31 | 122495, 142371 |
| 142 | 2 | truncation_p32 | ` क्रिप्टोकर` | 31 | 126064, 162859 |
| 143 | 2 | truncation_p32 | ` அமைந்துள்ள` | 31 | 128456, 162662 |
| 144 | 2 | truncation_p32 | ` प्रतिस्पर्` | 31 | 130631, 206672 |
| 145 | 2 | truncation_p32 | ` আর্জেন্টিন` | 31 | 138017, 167288 |
| 146 | 2 | truncation_p32 | ` মুক্তিবাহি` | 31 | 147706, 150776 |
| 147 | 2 | truncation_p32 | ` পূর্ববাংলা` | 31 | 150872, 169566 |
| 148 | 2 | truncation_p32 | ` চট্টগ্রামে` | 31 | 151265, 222217 |
| 149 | 2 | truncation_p32 | ` ইউনিভার্সি` | 31 | 151487, 193141 |
| 150 | 2 | truncation_p32 | ` நூற்றாண்டி` | 31 | 153887, 185456 |
| 151 | 2 | truncation_p32 | ` उपयोगकर्ता` | 31 | 156774, 181505 |
| 152 | 2 | truncation_p32 | ` क्रांतिकार` | 31 | 159923, 221109 |
| 153 | 2 | truncation_p32 | ` குறிப்பிட்` | 31 | 163284, 233971 |
| 154 | 2 | truncation_p32 | ` வால்பேப்பர` | 31 | 165413, 231638 |
| 155 | 2 | truncation_p32 | ` আনুষ্ঠানিক` | 31 | 178234, 178901 |
| 156 | 2 | truncation_p32 | ` പ്രവര്‍ത്ത` | 31 | 183688, 227415 |
| 157 | 2 | truncation_p32 | ` সিদ্ধান্তে` | 31 | 212837, 217147 |
| 158 | 2 | truncation_p32 | ` চলচ্চিত্রে` | 31 | 218376, 230506 |

All 159 groups. Member pieces and hex bytes: `results/gemma-3/groups_raw.jsonl`.

## deepseek-v3

Tokenizer `deepseek-ai/DeepSeek-V3-Base` snapshot `afb92e1fa402c2be2a9eb085312bb02e0384d6c7`.

- V = 128,815; raw rows by rule: added_literal 816, model_bbpe 127,997, special 2
- rows where decode bytes ≠ raw bytes: 1,470; raw rows that are not valid UTF-8: 1,470
- tokens longer than 32 bytes: 771; of these, sharing a row with another token: 59
- decode table SHA-256 `9b094069b7eadd8518d4f95ec845afcbb9fc7be4aafa9d5308f373415a212a61`
- raw table SHA-256 `748d9ff20baf3c4ee96c2b9b01b0becda5655136d413e50b32dd9b846d8ba73a`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation_p32 |
|---|---|---|---|---|---|
| CJK Han (fragment) | 336 | 336 | 2 | 336 / 2 | 0 / 0 |
| Hangul (fragment) | 201 | 201 | 2 | 201 / 2 | 0 / 0 |
| Hebrew | 923 | 127 | 24 | 127 / 24 | 0 / 0 |
| Continuation bytes only | 121 | 119 | 3 | 119 / 3 | 0 / 0 |
| Other scripts (fragment) | 69 | 67 | 4 | 67 / 4 | 0 / 0 |
| Punctuation/symbols (fragment) | 40 | 40 | 2 | 40 / 2 | 0 / 0 |
| Emoji (fragment) | 37 | 37 | 2 | 37 / 2 | 0 / 0 |
| Mixed (fragment) | 37 | 37 | 2 | 37 / 2 | 0 / 0 |
| ASCII | 72143 | 35 | 10 | 0 / 0 | 35 / 10 |
| Whitespace | 157 | 27 | 1 | 0 / 0 | 27 / 1 |
| Latin-ext (fragment) | 23 | 20 | 2 | 20 / 2 | 0 / 0 |
| Hebrew (fragment) | 18 | 18 | 3 | 18 / 3 | 0 / 0 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| Arabic (fragment) | 11 | 11 | 2 | 11 / 2 | 0 / 0 |
| Greek (fragment) | 10 | 10 | 2 | 10 / 2 | 0 / 0 |
| Other scripts | 471 | 8 | 4 | 8 / 4 | 0 / 0 |
| Cyrillic (fragment) | 8 | 8 | 2 | 8 / 2 | 0 / 0 |
| Hangul | 1131 | 4 | 2 | 4 / 2 | 0 / 0 |
| Replacement char | 14 | 4 | 4 | 4 / 4 | 0 / 0 |
| Bengali (fragment) | 4 | 4 | 3 | 4 / 3 | 0 / 0 |
| CJK symbols (fragment) | 4 | 4 | 2 | 4 / 2 | 0 / 0 |
| Telugu (fragment) | 4 | 4 | 3 | 4 / 3 | 0 / 0 |
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
| CJK Han | 35289 | 2 | 1 | 0 / 0 | 2 / 1 |
| Punctuation/symbols | 481 | 2 | 1 | 0 / 0 | 2 / 1 |
| Tamil | 168 | 2 | 1 | 2 / 1 | 0 / 0 |
| Combining marks (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Thai (fragment) | 2 | 2 | 1 | 2 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 692 | utf8_replacement | `�` | 3 | 97, 98, 99, 100, 101, 102 … |
| 1 | 180 | utf8_replacement | ` �` | 4 | 332, 508, 544, 663, 669, 831 … |
| 2 | 86 | utf8_replacement | `��` | 6 | 518, 2002, 2100, 3042, 3308, 3457 … |
| 3 | 27 | truncation_p32 | `                                ` | 32 | 3788, 15970, 16932, 20989, 29996, 38932 … |
| 4 | 11 | truncation_p32 | `................................` | 32 | 5349, 13361, 39235, 48939, 63634, 65391 … |
| 5 | 10 | utf8_replacement | `�ר` | 5 | 19236, 20204, 23090, 32254, 102733, 107617 … |
| 6 | 10 | utf8_replacement | `�ה` | 5 | 20645, 27713, 32645, 56457, 62239, 73588 … |
| 7 | 10 | utf8_replacement | `�ת` | 5 | 30149, 37254, 37708, 38246, 38293, 40010 … |
| 8 | 9 | utf8_replacement | `�ל` | 5 | 19952, 34119, 56864, 97152, 101802, 104557 … |
| 9 | 9 | utf8_replacement | `�ים` | 7 | 26586, 38430, 48259, 62342, 79546, 93546 … |
| 10 | 8 | utf8_replacement | `�י` | 5 | 11529, 37818, 42079, 45346, 51989, 100301 … |
| 11 | 8 | utf8_replacement | `�ד` | 5 | 34073, 38210, 49390, 49920, 65057, 76057 … |
| 12 | 7 | utf8_replacement | `�ות` | 7 | 30952, 44901, 56156, 68296, 80064, 87464 … |
| 13 | 6 | utf8_replacement | `�ם` | 5 | 30146, 49213, 66174, 97480, 110003, 123182 |
| 14 | 6 | utf8_replacement | `�ן` | 5 | 37538, 87506, 90807, 92522, 99280, 123447 |
| 15 | 5 | truncation_p32 | `--------------------------------` | 32 | 9171, 24991, 48738, 79773, 111795 |
| 16 | 5 | utf8_replacement | `�ע` | 5 | 27758, 45277, 91039, 97052, 122271 |
| 17 | 4 | utf8_replacement | `�ט` | 5 | 29811, 46064, 60681, 62926 |
| 18 | 4 | utf8_replacement | `�ש` | 5 | 32556, 40497, 94263, 100290 |
| 19 | 4 | utf8_replacement | `�ס` | 5 | 46746, 53546, 80303, 116022 |
| 20 | 4 | utf8_replacement | `�ג` | 5 | 73227, 89919, 102743, 103361 |
| 21 | 3 | truncation_p32 | `********************************` | 32 | 17045, 42101, 123218 |
| 22 | 3 | utf8_replacement | `�ו` | 5 | 20837, 37640, 86274 |
| 23 | 3 | truncation_p32 | `================================` | 32 | 20971, 57816, 105553 |
| 24 | 3 | utf8_replacement | `subscript�` | 12 | 25433, 65046, 68426 |
| 25 | 3 | utf8_replacement | `�ב` | 5 | 40561, 48200, 119019 |
| 26 | 3 | utf8_replacement | `�്�` | 9 | 41011, 47476, 99098 |
| 27 | 3 | utf8_replacement | `�צ` | 5 | 41015, 52353, 60851 |
| 28 | 3 | utf8_replacement | `�ק` | 5 | 42835, 57332, 58118 |
| 29 | 3 | utf8_replacement | `�\n\n` | 5 | 57265, 107296, 126477 |
| 30 | 3 | truncation_p32 | ` -------------------------------` | 32 | 65304, 95394, 109465 |
| 31 | 3 | utf8_replacement | `�ך` | 5 | 67043, 82052, 86534 |
| 32 | 2 | utf8_replacement | `�다` | 6 | 6768, 107520 |
| 33 | 2 | utf8_replacement | `်�` | 6 | 14976, 106016 |
| 34 | 2 | utf8_replacement | `�்` | 6 | 15790, 87466 |
| 35 | 2 | truncation_p32 | `________________________________` | 32 | 21334, 62204 |
| 36 | 2 | truncation_p32 | `################################` | 32 | 32683, 92334 |
| 37 | 2 | utf8_replacement | `�်�` | 9 | 37058, 56561 |
| 38 | 2 | utf8_replacement | `�이` | 6 | 38331, 47896 |
| 39 | 2 | truncation_p32 | `////////////////////////////////` | 32 | 39217, 97278 |
| 40 | 2 | utf8_replacement | `�א` | 5 | 45279, 122046 |
| 41 | 2 | utf8_replacement | `�ית` | 7 | 51255, 110199 |
| 42 | 2 | utf8_replacement | `�ი` | 6 | 53177, 88400 |
| 43 | 2 | utf8_replacement | `�ז` | 5 | 56203, 74336 |
| 44 | 2 | truncation_p32 | `——————————` | 30 | 57077, 125146 |
| 45 | 2 | truncation_p32 | `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM` | 32 | 59785, 102872 |
| 46 | 2 | truncation_p32 | `习近平新时代中国特色` | 30 | 65995, 74252 |
| 47 | 2 | utf8_replacement | `�ျေးရွာအုပ` | 30 | 70766, 71586 |
| 48 | 2 | truncation_p32 | ` *******************************` | 32 | 74667, 118888 |
| 49 | 2 | utf8_replacement | `�ור` | 7 | 108027, 115719 |

All 50 groups. Member pieces and hex bytes: `results/deepseek-v3/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 |
|---|---|---|---|---|
| ASCII | 72143 | 35 | 10 | 35 / 10 |
| Whitespace | 157 | 27 | 1 | 27 / 1 |
| CJK Han | 35289 | 2 | 1 | 2 / 1 |
| Punctuation/symbols | 481 | 2 | 1 | 2 / 1 |
| Other scripts | 471 | 2 | 1 | 2 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 27 | truncation_p32 | `                                ` | 32 | 3788, 15970, 16932, 20989, 29996, 38932 … |
| 1 | 11 | truncation_p32 | `................................` | 32 | 5349, 13361, 39235, 48939, 63634, 65391 … |
| 2 | 5 | truncation_p32 | `--------------------------------` | 32 | 9171, 24991, 48738, 79773, 111795 |
| 3 | 3 | truncation_p32 | `********************************` | 32 | 17045, 42101, 123218 |
| 4 | 3 | truncation_p32 | `================================` | 32 | 20971, 57816, 105553 |
| 5 | 3 | truncation_p32 | ` -------------------------------` | 32 | 65304, 95394, 109465 |
| 6 | 2 | truncation_p32 | `________________________________` | 32 | 21334, 62204 |
| 7 | 2 | truncation_p32 | `################################` | 32 | 32683, 92334 |
| 8 | 2 | truncation_p32 | `////////////////////////////////` | 32 | 39217, 97278 |
| 9 | 2 | truncation_p32 | `——————————` | 30 | 57077, 125146 |
| 10 | 2 | truncation_p32 | `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM` | 32 | 59785, 102872 |
| 11 | 2 | truncation_p32 | `习近平新时代中国特色` | 30 | 65995, 74252 |
| 12 | 2 | truncation_p32 | `\x80ျေးရွာအုပ်` | 31 | 70766, 71586 |
| 13 | 2 | truncation_p32 | ` *******************************` | 32 | 74667, 118888 |

All 14 groups. Member pieces and hex bytes: `results/deepseek-v3/groups_raw.jsonl`.

## gpt-oss

Tokenizer `openai/gpt-oss-120b` snapshot `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`.

- V = 200,019; raw rows by rule: added_literal 18, model_bbpe 199,998, special 3
- rows where decode bytes ≠ raw bytes: 1,562; raw rows that are not valid UTF-8: 1,562
- tokens longer than 32 bytes: 266; of these, sharing a row with another token: 171
- decode table SHA-256 `b895f2b9a7d5f65ae3973ce6171892e2bd2fd34ce2744705dd9fbc16da9a0aea`
- raw table SHA-256 `b7e1f90a0852b5f115fa32b3a4a26703976045b9bcfa78c314097dcccfe4d295`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement | truncation_p32 |
|---|---|---|---|---|---|
| CJK Han (fragment) | 529 | 529 | 2 | 529 / 2 | 0 / 0 |
| Hangul (fragment) | 236 | 236 | 2 | 236 / 2 | 0 / 0 |
| Continuation bytes only | 148 | 147 | 4 | 147 / 4 | 0 / 0 |
| ASCII | 128445 | 101 | 16 | 0 / 0 | 101 / 16 |
| Whitespace | 434 | 57 | 1 | 0 / 0 | 57 / 1 |
| Mixed (fragment) | 46 | 46 | 3 | 46 / 3 | 0 / 0 |
| Emoji (fragment) | 39 | 39 | 2 | 39 / 2 | 0 / 0 |
| Other scripts (fragment) | 37 | 37 | 3 | 37 / 3 | 0 / 0 |
| Punctuation/symbols (fragment) | 34 | 34 | 2 | 34 / 2 | 0 / 0 |
| Latin-ext (fragment) | 22 | 21 | 2 | 21 / 2 | 0 / 0 |
| Other scripts | 4877 | 16 | 6 | 10 / 4 | 6 / 2 |
| Thai | 1561 | 14 | 7 | 0 / 0 | 14 / 7 |
| Invalid UTF-8 byte | 13 | 13 | 1 | 13 / 1 | 0 / 0 |
| Private use (fragment) | 12 | 12 | 2 | 12 / 2 | 0 / 0 |
| Arabic (fragment) | 11 | 11 | 2 | 11 / 2 | 0 / 0 |
| Cyrillic (fragment) | 7 | 7 | 2 | 7 / 2 | 0 / 0 |
| Malayalam | 1657 | 6 | 3 | 2 / 1 | 4 / 2 |
| Greek (fragment) | 6 | 6 | 2 | 6 / 2 | 0 / 0 |
| Telugu | 1326 | 5 | 2 | 5 / 2 | 0 / 0 |
| CJK symbols (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Kana (fragment) | 5 | 5 | 2 | 5 / 2 | 0 / 0 |
| Thai (fragment) | 5 | 5 | 3 | 5 / 3 | 0 / 0 |
| Hangul | 2369 | 4 | 2 | 4 / 2 | 0 / 0 |
| Gujarati | 1620 | 4 | 2 | 2 / 1 | 2 / 1 |
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
| Tamil | 975 | 2 | 1 | 2 / 1 | 0 / 0 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 | 0 / 0 |
| Combining marks (fragment) | 1 | 1 | 1 | 1 / 1 | 0 / 0 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 689 | utf8_replacement | `�` | 3 | 94, 95, 96, 97, 98, 99 … |
| 1 | 411 | utf8_replacement | ` �` | 4 | 300, 333, 367, 389, 463, 559 … |
| 2 | 88 | utf8_replacement | `��` | 6 | 1857, 1965, 2112, 2121, 2203, 4765 … |
| 3 | 57 | truncation_p32 | `                                ` | 32 | 1213, 3523, 4754, 6322, 8793, 9344 … |
| 4 | 17 | truncation_p32 | `--------------------------------` | 32 | 2737, 7535, 19076, 28943, 32635, 50529 … |
| 5 | 14 | truncation_p32 | `********************************` | 32 | 3368, 8599, 12217, 41547, 42538, 65371 … |
| 6 | 10 | truncation_p32 | ` *******************************` | 32 | 22567, 39967, 50885, 52918, 70007, 73838 … |
| 7 | 9 | truncation_p32 | `================================` | 32 | 6288, 17686, 38551, 63146, 111845, 154118 … |
| 8 | 7 | truncation_p32 | `////////////////////////////////` | 32 | 9731, 25493, 73297, 73681, 76050, 143581 … |
| 9 | 7 | truncation_p32 | ` -------------------------------` | 32 | 18882, 38771, 43717, 77304, 79593, 141084 … |
| 10 | 7 | truncation_p32 | ` ===============================` | 32 | 36014, 64084, 79343, 126247, 132548, 166044 … |
| 11 | 6 | truncation_p32 | `################################` | 32 | 10982, 29834, 71120, 81787, 103402, 185617 |
| 12 | 4 | truncation_p32 | ` ///////////////////////////////` | 32 | 93582, 149632, 151649, 176860 |
| 13 | 4 | truncation_p32 | `/*******************************` | 32 | 109438, 111383, 113341, 117837 |
| 14 | 3 | utf8_replacement | `�ი` | 6 | 4980, 6102, 142740 |
| 15 | 3 | utf8_replacement | `�ి` | 6 | 13981, 47426, 79041 |
| 16 | 3 | truncation_p32 | `________________________________` | 32 | 25182, 80553, 125094 |
| 17 | 3 | truncation_p32 | ` საქართველო` | 31 | 43652, 85815, 171158 |
| 18 | 3 | utf8_replacement | `�ვ` | 6 | 59325, 69450, 154624 |
| 19 | 3 | truncation_p32 | ` ###############################` | 32 | 125012, 138352, 180376 |
| 20 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 130774, 161620, 174223 |
| 21 | 3 | truncation_p32 | `//------------------------------` | 32 | 131495, 160888, 183481 |
| 22 | 3 | truncation_p32 | ` მნიშვნელოვ` | 31 | 135971, 141109, 186053 |
| 23 | 2 | utf8_replacement | `�்` | 6 | 4535, 70619 |
| 24 | 2 | utf8_replacement | `�়` | 6 | 6578, 44278 |
| 25 | 2 | utf8_replacement | `�്ച` | 9 | 7350, 165871 |
| 26 | 2 | utf8_replacement | `�美` | 6 | 9505, 82761 |
| 27 | 2 | utf8_replacement | `�ે` | 6 | 13601, 21340 |
| 28 | 2 | utf8_replacement | `�ლ` | 6 | 18038, 19922 |
| 29 | 2 | truncation_p32 | `................................` | 32 | 27838, 74358 |
| 30 | 2 | utf8_replacement | `�니다` | 9 | 34951, 162551 |
| 31 | 2 | utf8_replacement | `�ნ` | 6 | 55507, 61639 |
| 32 | 2 | utf8_replacement | `�다` | 6 | 56388, 75734 |
| 33 | 2 | truncation_p32 | ` วิเคราะห์บ` | 31 | 62394, 135127 |
| 34 | 2 | utf8_replacement | `�\n\n` | 5 | 68340, 115963 |
| 35 | 2 | utf8_replacement | `�్` | 6 | 73475, 76944 |
| 36 | 2 | utf8_replacement | `�pp` | 5 | 78747, 186978 |
| 37 | 2 | truncation_p32 | `ിരിക്കുന്ന` | 30 | 103491, 189470 |
| 38 | 2 | truncation_p32 | `อ่านข้อควา` | 30 | 110119, 110120 |
| 39 | 2 | truncation_p32 | ` กรุงเทพมหา` | 31 | 127607, 149851 |
| 40 | 2 | truncation_p32 | ` แขวงคลองเต` | 31 | 149494, 149708 |
| 41 | 2 | truncation_p32 | ` વિદ્યાર્થી` | 31 | 149901, 186895 |
| 42 | 2 | truncation_p32 | ` สำนักเลขาน` | 31 | 150140, 150141 |
| 43 | 2 | truncation_p32 | ` ...............................` | 32 | 152475, 164601 |
| 44 | 2 | truncation_p32 | `เปิดอภิปรา` | 30 | 173899, 173900 |
| 45 | 2 | truncation_p32 | ` ปมถวายสัตย` | 31 | 174023, 174024 |
| 46 | 2 | truncation_p32 | `പ്പെടുത്തി` | 30 | 192226, 198440 |

All 47 groups. Member pieces and hex bytes: `results/gpt-oss/groups_decode.jsonl`.

**raw table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | truncation_p32 |
|---|---|---|---|---|
| ASCII | 128445 | 101 | 16 | 101 / 16 |
| Whitespace | 434 | 57 | 1 | 57 / 1 |
| Thai | 1561 | 14 | 7 | 14 / 7 |
| Other scripts | 4877 | 6 | 2 | 6 / 2 |
| Malayalam | 1657 | 4 | 2 | 4 / 2 |
| Gujarati | 1620 | 2 | 1 | 2 / 1 |

**raw table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 57 | truncation_p32 | `                                ` | 32 | 1213, 3523, 4754, 6322, 8793, 9344 … |
| 1 | 17 | truncation_p32 | `--------------------------------` | 32 | 2737, 7535, 19076, 28943, 32635, 50529 … |
| 2 | 14 | truncation_p32 | `********************************` | 32 | 3368, 8599, 12217, 41547, 42538, 65371 … |
| 3 | 10 | truncation_p32 | ` *******************************` | 32 | 22567, 39967, 50885, 52918, 70007, 73838 … |
| 4 | 9 | truncation_p32 | `================================` | 32 | 6288, 17686, 38551, 63146, 111845, 154118 … |
| 5 | 7 | truncation_p32 | `////////////////////////////////` | 32 | 9731, 25493, 73297, 73681, 76050, 143581 … |
| 6 | 7 | truncation_p32 | ` -------------------------------` | 32 | 18882, 38771, 43717, 77304, 79593, 141084 … |
| 7 | 7 | truncation_p32 | ` ===============================` | 32 | 36014, 64084, 79343, 126247, 132548, 166044 … |
| 8 | 6 | truncation_p32 | `################################` | 32 | 10982, 29834, 71120, 81787, 103402, 185617 |
| 9 | 4 | truncation_p32 | ` ///////////////////////////////` | 32 | 93582, 149632, 151649, 176860 |
| 10 | 4 | truncation_p32 | `/*******************************` | 32 | 109438, 111383, 113341, 117837 |
| 11 | 3 | truncation_p32 | `________________________________` | 32 | 25182, 80553, 125094 |
| 12 | 3 | truncation_p32 | ` საქართველო` | 31 | 43652, 85815, 171158 |
| 13 | 3 | truncation_p32 | ` ###############################` | 32 | 125012, 138352, 180376 |
| 14 | 3 | truncation_p32 | ` //-----------------------------` | 32 | 130774, 161620, 174223 |
| 15 | 3 | truncation_p32 | `//------------------------------` | 32 | 131495, 160888, 183481 |
| 16 | 3 | truncation_p32 | ` მნიშვნელოვ` | 31 | 135971, 141109, 186053 |
| 17 | 2 | truncation_p32 | `................................` | 32 | 27838, 74358 |
| 18 | 2 | truncation_p32 | ` วิเคราะห์บ` | 31 | 62394, 135127 |
| 19 | 2 | truncation_p32 | `ിരിക്കുന്ന` | 30 | 103491, 189470 |
| 20 | 2 | truncation_p32 | `อ่านข้อควา` | 30 | 110119, 110120 |
| 21 | 2 | truncation_p32 | ` กรุงเทพมหา` | 31 | 127607, 149851 |
| 22 | 2 | truncation_p32 | ` แขวงคลองเต` | 31 | 149494, 149708 |
| 23 | 2 | truncation_p32 | ` વિદ્યાર્થી` | 31 | 149901, 186895 |
| 24 | 2 | truncation_p32 | ` สำนักเลขาน` | 31 | 150140, 150141 |
| 25 | 2 | truncation_p32 | ` ...............................` | 32 | 152475, 164601 |
| 26 | 2 | truncation_p32 | `เปิดอภิปรา` | 30 | 173899, 173900 |
| 27 | 2 | truncation_p32 | ` ปมถวายสัตย` | 31 | 174023, 174024 |
| 28 | 2 | truncation_p32 | `പ്പെടുത്തി` | 30 | 192226, 198440 |

All 29 groups. Member pieces and hex bytes: `results/gpt-oss/groups_raw.jsonl`.

## Proof checks

| tokenizer | table | L1 round-trip | L1 max ‖κ̃‖−1 | L2 support = {z>0} | L2 max rel err | T1 distinct byte rows | T1 distinct codec rows | T1 groups → 1 codec row | dynamic = cached |
|---|---|---|---|---|---|---|---|---|---|
| gpt2 | decode | 50,257/50,257 | 6.7e-08 | 50,257/50,257 | 1.2e-07 | 49,914 | 49,914 | 14/14 | yes |
| gpt2 | raw | 50,257/50,257 | 6.7e-08 | 50,257/50,257 | 1.2e-07 | 50,247 | 50,247 | 7/7 | yes |
| llama-3.2 | decode | 128,256/128,256 | 6.7e-08 | 128,256/128,256 | 1.9e-07 | 126,845 | 126,845 | 41/41 | yes |
| llama-3.2 | raw | 128,256/128,256 | 6.7e-08 | 128,256/128,256 | 1.9e-07 | 128,061 | 128,061 | 28/28 | yes |
| qwen3 | decode | 151,669/151,669 | 6.7e-08 | 151,669/151,669 | 1.9e-07 | 150,149 | 150,149 | 36/36 | yes |
| qwen3 | raw | 151,669/151,669 | 6.7e-08 | 151,669/151,669 | 1.9e-07 | 151,485 | 151,485 | 25/25 | yes |
| gemma-3 | decode | 262,145/262,145 | 6.7e-08 | 262,145/262,145 | 1.9e-07 | 261,968 | 261,968 | 159/159 | yes |
| gemma-3 | raw | 262,145/262,145 | 6.7e-08 | 262,145/262,145 | 1.9e-07 | 261,968 | 261,968 | 159/159 | yes |
| deepseek-v3 | decode | 128,815/128,815 | 6.7e-08 | 128,815/128,815 | 1.9e-07 | 127,691 | 127,691 | 50/50 | yes |
| deepseek-v3 | raw | 128,815/128,815 | 6.7e-08 | 128,815/128,815 | 1.9e-07 | 128,761 | 128,761 | 14/14 | yes |
| gpt-oss | decode | 200,019/200,019 | 6.7e-08 | 200,019/200,019 | 1.9e-07 | 198,661 | 198,661 | 47/47 | yes |
| gpt-oss | raw | 200,019/200,019 | 6.7e-08 | 200,019/200,019 | 1.9e-07 | 199,864 | 199,864 | 29/29 | yes |

## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)

| L | z on support | z off support | rows checked | max rel err |
|---|---|---|---|---|
| 1 | 90.490429 | -0.01104754 | 2,652 | 4.5e-08 |
| 2 | 63.982490 | -0.01562454 | 45,097 | 4.0e-08 |
| 3 | 52.238294 | -0.01913724 | 215,699 | 3.2e-08 |
| 4 | 45.236927 | -0.02209913 | 225,888 | 9.3e-08 |
| 5 | 40.458667 | -0.02470909 | 211,835 | 2.7e-08 |
| 6 | 36.931285 | -0.02706911 | 317,527 | 2.5e-08 |
| 7 | 34.189637 | -0.02923976 | 192,981 | 2.9e-08 |
| 8 | 31.979523 | -0.03126053 | 136,949 | 1.7e-08 |
| 9 | 30.148741 | -0.03315883 | 160,308 | 4.9e-08 |
| 10 | 28.599860 | -0.03495461 | 87,750 | 1.2e-07 |
| 11 | 27.267230 | -0.03666294 | 61,936 | 4.6e-08 |
| 12 | 26.104789 | -0.03829553 | 63,334 | 2.8e-08 |
| 13 | 25.079137 | -0.03986169 | 39,450 | 4.2e-08 |
| 14 | 24.165383 | -0.04136896 | 10,165 | 4.0e-08 |
| 15 | 23.344551 | -0.04282356 | 17,437 | 6.7e-08 |
| 16 | 22.601882 | -0.04423069 | 13,639 | 8.6e-08 |
| 17 | 21.925705 | -0.04559474 | 4,366 | 2.8e-08 |
| 18 | 21.306652 | -0.04691947 | 4,527 | 7.6e-08 |
| 19 | 20.737103 | -0.04820812 | 9,595 | 3.8e-08 |
| 20 | 20.210791 | -0.04946351 | 370 | 4.0e-08 |
| 21 | 19.722506 | -0.05068812 | 3,069 | 1.1e-07 |
| 22 | 19.267875 | -0.05188412 | 4,712 | 8.2e-08 |
| 23 | 18.843200 | -0.05305345 | 826 | 7.5e-08 |
| 24 | 18.445328 | -0.05419783 | 1,018 | 1.2e-07 |
| 25 | 18.071550 | -0.05531881 | 3,172 | 7.9e-08 |
| 26 | 17.719528 | -0.05641780 | 88 | 1.1e-07 |
| 27 | 17.387227 | -0.05749604 | 638 | 1.9e-07 |
| 28 | 17.072873 | -0.05855468 | 1,504 | 3.2e-08 |
| 29 | 16.774903 | -0.05959478 | 298 | 1.2e-07 |
| 30 | 16.491941 | -0.06061728 | 780 | 1.8e-08 |
| 31 | 16.222768 | -0.06162306 | 1,700 | 9.8e-08 |
| 32 | 15.966297 | -0.06261293 | 3,012 | 4.4e-08 |

## Determinism (three fresh CPU processes)

| run | PYTHONHASHSEED | torch threads | device | wall s |
|---|---|---|---|---|
| 1 | 0 | 1 | cpu | 94.2 |
| 2 | 1 | 4 | cpu | 56.2 |
| 3 | 2 | 8 | cpu | 52.1 |

| tokenizer | hash of | IDs decoded per run | run 1 | run 2 | run 3 | result |
|---|---|---|---|---|---|---|
| gpt2 | decode_table | 50,257 | `fea58ad63a97f0ac` | `fea58ad63a97f0ac` | `fea58ad63a97f0ac` | match |
| gpt2 | raw_table | 50,257 | `e8db9b5152c0828b` | `e8db9b5152c0828b` | `e8db9b5152c0828b` | match |
| gpt2 | codec_table | 50,257 | `1d0ad8bdd5295a31` | `1d0ad8bdd5295a31` | `1d0ad8bdd5295a31` | match |
| llama-3.2 | decode_table | 128,256 | `b051c5ca594b9fee` | `b051c5ca594b9fee` | `b051c5ca594b9fee` | match |
| llama-3.2 | raw_table | 128,256 | `70d6e7b67a030ccc` | `70d6e7b67a030ccc` | `70d6e7b67a030ccc` | match |
| llama-3.2 | codec_table | 128,256 | `b5e3d654a94a3eec` | `b5e3d654a94a3eec` | `b5e3d654a94a3eec` | match |
| qwen3 | decode_table | 151,669 | `a3f1f90b85c7fb39` | `a3f1f90b85c7fb39` | `a3f1f90b85c7fb39` | match |
| qwen3 | raw_table | 151,669 | `70c9fd1f77ce95a3` | `70c9fd1f77ce95a3` | `70c9fd1f77ce95a3` | match |
| qwen3 | codec_table | 151,669 | `a960fde45a72a5f6` | `a960fde45a72a5f6` | `a960fde45a72a5f6` | match |
| gemma-3 | decode_table | 262,145 | `a76c712edf3ed29c` | `a76c712edf3ed29c` | `a76c712edf3ed29c` | match |
| gemma-3 | raw_table | 262,145 | `a76c712edf3ed29c` | `a76c712edf3ed29c` | `a76c712edf3ed29c` | match |
| gemma-3 | codec_table | 262,145 | `fdbce93b64335d38` | `fdbce93b64335d38` | `fdbce93b64335d38` | match |
| deepseek-v3 | decode_table | 128,815 | `9b094069b7eadd85` | `9b094069b7eadd85` | `9b094069b7eadd85` | match |
| deepseek-v3 | raw_table | 128,815 | `748d9ff20baf3c4e` | `748d9ff20baf3c4e` | `748d9ff20baf3c4e` | match |
| deepseek-v3 | codec_table | 128,815 | `91c4dd63b76fc134` | `91c4dd63b76fc134` | `91c4dd63b76fc134` | match |
| gpt-oss | decode_table | 200,019 | `b895f2b9a7d5f65a` | `b895f2b9a7d5f65a` | `b895f2b9a7d5f65a` | match |
| gpt-oss | raw_table | 200,019 | `b7e1f90a0852b5f1` | `b7e1f90a0852b5f1` | `b7e1f90a0852b5f1` | match |
| gpt-oss | codec_table | 200,019 | `f1228acd8c46f657` | `f1228acd8c46f657` | `f1228acd8c46f657` | match |

All hashes match: **True**. Full 64-hex hashes are in `results/determinism.json`.

