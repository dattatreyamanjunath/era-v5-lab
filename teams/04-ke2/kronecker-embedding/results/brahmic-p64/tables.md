# Generated tables — run `brahmic-p64` (P = 64, D = 16,384)

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

## Tokens longer than P = 64

| tokenizer | tokens > 64 bytes | of these, sharing a row |
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
- tokens longer than 64 bytes: 0; of these, sharing a row with another token: 0
- decode table SHA-256 `37bb952559640591c24921e23aad3bbfe05e76cabb2e77aea93ca64f1e242ae1`
- raw table SHA-256 `32ba57e59de4a20feaed1db4bbfbbbcc0902809fcce4d4854754b318ac7b984a`

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
| brahmic-131k | decode | 131,072/131,072 | 1.2e-07 | 131,072/131,072 | 1.7e-07 | 129,931 | 129,931 | 10/10 | yes |
| brahmic-131k | raw | 131,072/131,072 | 1.2e-07 | 131,072/131,072 | 1.7e-07 | 131,072 | 131,072 | 0/0 | yes |

## Lemma 2 closed form vs torch, by length (all tokenizers, both tables)

| L | z on support | z off support | rows checked | max rel err |
|---|---|---|---|---|
| 1 | 127.975807 | -0.00781150 | 371 | 5.5e-08 |
| 2 | 90.489798 | -0.01104747 | 7,283 | 7.4e-08 |
| 3 | 73.882356 | -0.01353074 | 25,994 | 3.8e-08 |
| 4 | 63.982044 | -0.01562443 | 39,608 | 5.1e-08 |
| 5 | 57.225532 | -0.01746918 | 40,270 | 4.2e-08 |
| 6 | 52.237930 | -0.01913711 | 38,437 | 7.8e-08 |
| 7 | 48.361449 | -0.02067107 | 30,251 | 2.6e-08 |
| 8 | 45.236612 | -0.02209898 | 20,882 | 4.3e-08 |
| 9 | 42.648184 | -0.02344022 | 19,461 | 7.0e-08 |
| 10 | 40.458385 | -0.02470892 | 13,921 | 2.4e-08 |
| 11 | 38.574378 | -0.02591572 | 6,348 | 4.7e-08 |
| 12 | 36.931027 | -0.02706892 | 6,162 | 8.6e-08 |
| 13 | 35.481099 | -0.02817508 | 4,903 | 3.3e-08 |
| 14 | 34.189398 | -0.02923956 | 1,125 | 3.7e-08 |
| 15 | 33.029088 | -0.03026674 | 1,507 | 6.2e-08 |
| 16 | 31.979300 | -0.03126031 | 2,556 | 3.4e-08 |
| 17 | 31.023530 | -0.03222338 | 72 | 1.3e-07 |
| 18 | 30.148531 | -0.03315859 | 439 | 7.2e-08 |
| 19 | 29.343528 | -0.03406826 | 1,122 | 7.5e-08 |
| 20 | 28.599660 | -0.03495436 | 12 | 7.2e-08 |
| 21 | 27.909557 | -0.03581866 | 168 | 7.7e-08 |
| 22 | 27.267039 | -0.03666269 | 568 | 6.4e-08 |
| 23 | 26.666875 | -0.03748781 | 4 | 5.1e-08 |
| 24 | 26.104606 | -0.03829527 | 104 | 2.2e-08 |
| 25 | 25.576404 | -0.03908614 | 306 | 5.4e-09 |
| 26 | 25.078961 | -0.03986141 | 8 | 5.4e-08 |
| 27 | 24.609402 | -0.04062199 | 40 | 1.7e-07 |
| 28 | 24.165214 | -0.04136867 | 130 | 9.3e-08 |
| 29 | 23.744192 | -0.04210220 | 4 | 4.2e-08 |
| 30 | 23.344387 | -0.04282326 | 14 | 1.1e-07 |
| 31 | 22.964076 | -0.04353246 | 52 | 4.3e-08 |
| 32 | 22.601723 | -0.04423038 | 22 | 5.1e-08 |

## Determinism (3 fresh CPU processes)

| run | PYTHONHASHSEED | torch threads | device | wall s |
|---|---|---|---|---|
| 1 | 0 | 1 | cpu | 29.4 |
| 2 | 1 | 4 | cpu | 17.6 |
| 3 | 2 | 8 | cpu | 17.0 |

| tokenizer | hash of | IDs decoded per run | SHA-256 (run 1) | all runs |
|---|---|---|---|---|
| brahmic-131k | decode_table | 131,072 | `37bb952559640591c24921e23aad3bbfe05e76cabb2e77aea93ca64f1e242ae1` | match |
| brahmic-131k | raw_table | 131,072 | `32ba57e59de4a20feaed1db4bbfbbbcc0902809fcce4d4854754b318ac7b984a` | match |
| brahmic-131k | codec_table | 131,072 | `c3b23d5d1d1b7d863a51b4e82c8fc33cd11ff1a7acd5df8b0b4510bbe4252267` | match |

All hashes match: **True**.

