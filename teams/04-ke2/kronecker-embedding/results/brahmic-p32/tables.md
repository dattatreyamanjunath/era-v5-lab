# Generated tables — run `brahmic-p32` (P = 32, D = 8,192)

Rendered by `python -m kron_audit report` from this folder. Do not edit by hand.

## Overview

`lost` = V − distinct rows = IDs that do not get their own codec row.

| tokenizer | V | family | decode groups | decode colliding IDs | decode lost | raw groups | raw colliding IDs | raw lost | L1/L2/T1/modes |
|---|---|---|---|---|---|---|---|---|---|
| brahmic-131k | 131,072 | bbpe | 10 | 1,151 | 1,141 | 0 | 0 | 0 | pass |

## Collisions by cause

| tokenizer | table | cause | groups | tokens |
|---|---|---|---|---|
| brahmic-131k | decode | utf8_replacement | 10 | 1151 |

## Tokens longer than P = 32

| tokenizer | tokens > 32 bytes | of these, sharing a row |
|---|---|---|
| brahmic-131k | 0 | 0 |

## Colliding token IDs per script class — decode table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

| script class | brahmic-131k | total |
|---|---|---|
| CJK Han | 513 | 513 |
| Hangul | 230 | 230 |
| Continuation bytes only | 139 | 139 |
| Mixed | 39 | 39 |
| Emoji | 35 | 35 |
| Other scripts | 35 | 35 |
| Punctuation/symbols | 31 | 31 |
| Latin-ext | 21 | 21 |
| Private use | 12 | 12 |
| Arabic | 11 | 11 |
| Telugu | 10 | 10 |
| Cyrillic | 7 | 7 |
| Greek | 6 | 6 |
| Bengali | 6 | 6 |
| Gujarati | 6 | 6 |
| Malayalam | 6 | 6 |
| Tamil | 6 | 6 |
| CJK symbols | 5 | 5 |
| Kana | 5 | 5 |
| Thai | 5 | 5 |
| Replacement char | 4 | 4 |
| Devanagari | 4 | 4 |
| Gurmukhi | 4 | 4 |
| Kannada | 4 | 4 |
| Oriya | 4 | 4 |
| Hebrew | 2 | 2 |
| Combining marks | 1 | 1 |

## Colliding token IDs per script class — raw table

Fragments (partial UTF-8 tokens) are counted under the script their lead byte points to.

No collisions.

## brahmic-131k

Source `theschoolofai/BrahmicTokenizer-131K` (hf), snapshot `93df154cbc9dbf038a222c010d9b43906a8a72c3`, family `bbpe`.

- V = 131,072; raw rows by rule: model_bbpe 131,068, special 4
- rows where decode bytes ≠ raw bytes: 1,306; raw rows that are not valid UTF-8: 1,306
- tokens longer than 32 bytes: 0; of these, sharing a row with another token: 0
- decode table SHA-256 `783f26265de9b12a6dc7366c17effab6b7354170bfc0c9635f708e688f5af35f`
- raw table SHA-256 `d36cdf74777982365555894c95267db4f2b0b518f25b8db20a4cb0cb64f8fe38`

**decode table, by script class** (cause columns: tokens / groups)

| script class | tokens in class | colliding | groups | utf8_replacement |
|---|---|---|---|---|
| CJK Han (fragment) | 513 | 513 | 2 | 513 / 2 |
| Hangul (fragment) | 230 | 230 | 2 | 230 / 2 |
| Continuation bytes only | 140 | 139 | 3 | 139 / 3 |
| Mixed (fragment) | 39 | 39 | 3 | 39 / 3 |
| Emoji (fragment) | 35 | 35 | 2 | 35 / 2 |
| Other scripts (fragment) | 35 | 35 | 3 | 35 / 3 |
| Punctuation/symbols (fragment) | 31 | 31 | 2 | 31 / 2 |
| Latin-ext (fragment) | 22 | 21 | 2 | 21 / 2 |
| Private use (fragment) | 12 | 12 | 2 | 12 / 2 |
| Arabic (fragment) | 11 | 11 | 2 | 11 / 2 |
| Cyrillic (fragment) | 7 | 7 | 2 | 7 / 2 |
| Greek (fragment) | 6 | 6 | 2 | 6 / 2 |
| Telugu | 1497 | 5 | 2 | 5 / 2 |
| CJK symbols (fragment) | 5 | 5 | 2 | 5 / 2 |
| Kana (fragment) | 5 | 5 | 2 | 5 / 2 |
| Telugu (fragment) | 5 | 5 | 3 | 5 / 3 |
| Thai (fragment) | 5 | 5 | 3 | 5 / 3 |
| Replacement char | 19 | 4 | 4 | 4 / 4 |
| Bengali (fragment) | 4 | 4 | 2 | 4 / 2 |
| Devanagari (fragment) | 4 | 4 | 2 | 4 / 2 |
| Gujarati (fragment) | 4 | 4 | 2 | 4 / 2 |
| Gurmukhi (fragment) | 4 | 4 | 2 | 4 / 2 |
| Kannada (fragment) | 4 | 4 | 2 | 4 / 2 |
| Malayalam (fragment) | 4 | 4 | 2 | 4 / 2 |
| Oriya (fragment) | 4 | 4 | 2 | 4 / 2 |
| Tamil (fragment) | 4 | 4 | 2 | 4 / 2 |
| Bengali | 2285 | 2 | 1 | 2 / 1 |
| Malayalam | 1891 | 2 | 1 | 2 / 1 |
| Gujarati | 1832 | 2 | 1 | 2 / 1 |
| Tamil | 1130 | 2 | 1 | 2 / 1 |
| Hebrew (fragment) | 2 | 2 | 2 | 2 / 2 |
| Combining marks (fragment) | 1 | 1 | 1 | 1 / 1 |

**decode table, groups**

| # | size | cause | shared row | row bytes | IDs |
|---|---|---|---|---|---|
| 0 | 658 | utf8_replacement | `�` | 3 | 77, 173, 402, 413, 436, 475 … |
| 1 | 396 | utf8_replacement | ` �` | 4 | 490, 1594, 2995, 4368, 4784, 5040 … |
| 2 | 82 | utf8_replacement | `��` | 6 | 4351, 8467, 14687, 16428, 19609, 27230 … |
| 3 | 3 | utf8_replacement | `�ి` | 6 | 46661, 56242, 68514 |
| 4 | 2 | utf8_replacement | `�়` | 6 | 26588, 54680 |
| 5 | 2 | utf8_replacement | `�்` | 6 | 39329, 74642 |
| 6 | 2 | utf8_replacement | `�ે` | 6 | 65364, 75092 |
| 7 | 2 | utf8_replacement | `�്ച` | 9 | 70992, 74921 |
| 8 | 2 | utf8_replacement | `�్` | 6 | 79229, 81345 |
| 9 | 2 | utf8_replacement | `�\n\n` | 5 | 115875, 129421 |

All 10 groups. Member pieces and hex bytes: `brahmic-131k/groups_decode.jsonl`.

**raw table:** no collisions.

## Proof checks

| tokenizer | table | L1 round-trip | L1 max norm err | L2 support = {z>0} | L2 max rel err | T1 distinct byte rows | T1 distinct codec rows | T1 groups → 1 codec row | dynamic = cached |
|---|---|---|---|---|---|---|---|---|---|
| brahmic-131k | decode | 131,072/131,072 | 1.2e-07 | 131,072/131,072 | 1.9e-07 | 129,931 | 129,931 | 10/10 | yes |
| brahmic-131k | raw | 131,072/131,072 | 1.2e-07 | 131,072/131,072 | 1.9e-07 | 131,072 | 131,072 | 0/0 | yes |

## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)

| L | z on support | z off support | rows checked | max rel err |
|---|---|---|---|---|
| 1 | 90.490429 | -0.01104754 | 371 | 4.5e-08 |
| 2 | 63.982490 | -0.01562454 | 7,283 | 4.0e-08 |
| 3 | 52.238294 | -0.01913724 | 25,994 | 3.2e-08 |
| 4 | 45.236927 | -0.02209913 | 39,608 | 9.3e-08 |
| 5 | 40.458667 | -0.02470909 | 40,270 | 2.7e-08 |
| 6 | 36.931285 | -0.02706911 | 38,437 | 2.5e-08 |
| 7 | 34.189637 | -0.02923976 | 30,251 | 2.9e-08 |
| 8 | 31.979523 | -0.03126053 | 20,882 | 1.7e-08 |
| 9 | 30.148741 | -0.03315883 | 19,461 | 4.9e-08 |
| 10 | 28.599860 | -0.03495461 | 13,921 | 1.2e-07 |
| 11 | 27.267230 | -0.03666294 | 6,348 | 4.6e-08 |
| 12 | 26.104789 | -0.03829553 | 6,162 | 2.8e-08 |
| 13 | 25.079137 | -0.03986169 | 4,903 | 4.2e-08 |
| 14 | 24.165383 | -0.04136896 | 1,125 | 4.0e-08 |
| 15 | 23.344551 | -0.04282356 | 1,507 | 6.7e-08 |
| 16 | 22.601882 | -0.04423069 | 2,556 | 8.6e-08 |
| 17 | 21.925705 | -0.04559474 | 72 | 2.8e-08 |
| 18 | 21.306652 | -0.04691947 | 439 | 7.6e-08 |
| 19 | 20.737103 | -0.04820812 | 1,122 | 3.8e-08 |
| 20 | 20.210791 | -0.04946351 | 12 | 4.0e-08 |
| 21 | 19.722506 | -0.05068812 | 168 | 1.1e-07 |
| 22 | 19.267875 | -0.05188412 | 568 | 8.2e-08 |
| 23 | 18.843200 | -0.05305345 | 4 | 7.5e-08 |
| 24 | 18.445328 | -0.05419783 | 104 | 1.2e-07 |
| 25 | 18.071550 | -0.05531881 | 306 | 7.9e-08 |
| 26 | 17.719528 | -0.05641780 | 8 | 1.1e-07 |
| 27 | 17.387227 | -0.05749604 | 40 | 1.9e-07 |
| 28 | 17.072873 | -0.05855468 | 130 | 3.2e-08 |
| 29 | 16.774903 | -0.05959478 | 4 | 1.2e-07 |
| 30 | 16.491941 | -0.06061728 | 14 | 1.8e-08 |
| 31 | 16.222768 | -0.06162306 | 52 | 9.8e-08 |
| 32 | 15.966297 | -0.06261293 | 22 | 4.4e-08 |

## Determinism (3 fresh CPU processes)

| run | PYTHONHASHSEED | torch threads | device | wall s |
|---|---|---|---|---|
| 1 | 0 | 1 | cpu | 19.6 |
| 2 | 1 | 4 | cpu | 12.0 |
| 3 | 2 | 8 | cpu | 11.9 |

| tokenizer | hash of | IDs decoded per run | SHA-256 (run 1) | all runs |
|---|---|---|---|---|
| brahmic-131k | decode_table | 131,072 | `783f26265de9b12a6dc7366c17effab6b7354170bfc0c9635f708e688f5af35f` | match |
| brahmic-131k | raw_table | 131,072 | `d36cdf74777982365555894c95267db4f2b0b518f25b8db20a4cb0cb64f8fe38` | match |
| brahmic-131k | codec_table | 131,072 | `fe40c8ad363bd259daad03dca3d012ebd1ec86a285832d8fb9e3a848f83feeba` | match |

All hashes match: **True**.

