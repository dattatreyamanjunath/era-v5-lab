# BrahmicTokenizer-131K at P = 32 and P = 64

This applies the same audit as [collisions.md](collisions.md) and [p64.md](p64.md) to [theschoolofai/BrahmicTokenizer-131K](https://huggingface.co/theschoolofai/BrahmicTokenizer-131K), pinned to Hub commit `93df154cbc9dbf038a222c010d9b43906a8a72c3` (`tokenizer.json` SHA-256 `01d968a7…`).

- **Config:** [`configs/brahmic.yaml`](configs/brahmic.yaml). The P=64 run uses `--pos-dim 64 --name brahmic-p64`.
- **Results:** [`results/brahmic-p32/`](results/brahmic-p32/) and [`results/brahmic-p64/`](results/brahmic-p64/); every group is listed in their `tables.md`.

## Result

**The raw byte table has zero collisions at both P: all 131,072 IDs get their own embedding.** It is the only tokenizer tested so far with none. The repo's decode table still loses 1,141 IDs to U+FFFD.

| | P=32 | P=64 |
|---|---|---|
| V | 131,072 | 131,072 |
| lost IDs, **raw** table | **0** | **0** |
| lost IDs, decode table | 1,141 | 1,141 |
| decode collision groups (all `utf8_replacement`) | 10, largest 658 | 10, largest 658 |
| tokens longer than P | 0 | 0 |
| paper §4.2 "distinct after truncation" | holds | holds |
| Lemma 1 / Lemma 2 / Theorem 1 / dynamic = cached | all pass | all pass |
| determinism (3 fresh CPU processes) | 9 / 9 hashes match | 9 / 9 hashes match |

The same two counts for the earlier tokenizers:

| lost IDs, raw table | P=32 | P=64 |
|---|---|---|
| BrahmicTokenizer-131K | 0 | 0 |
| best of the paper's six (GPT-2) | 10 | 1 |
| gpt-oss (o200k_harmony, which Brahmic is meant to replace) | 155 | 72 |

## Why the raw table is clean

- **No truncation.** The longest token is exactly 32 bytes (mean 6.6). Nothing is cut even at P=32, so P=64 changes nothing: every count is identical. The space and symbol runs that cause every truncation collision in the other byte-level tokenizers stop at 32 bytes here.
- **No byte-fallback twins.** It is byte-level BPE (detected as `bbpe`), not SentencePiece.
- **No duplicate entries** and no special-token clashes. 131,068 tokens are model pieces and 4 are special tokens.

**So P=32 is enough for this tokenizer.** P=64 doubles the projection (D 8,192 → 16,384) for no gain.

## What the decode table loses

1,306 tokens are pieces of multi-byte characters, and `decode` writes `�` in place of each piece. 1,151 of them land in 10 groups; the other 155 still decode to a unique string, thanks to their valid neighbours.

| group | size | what it holds |
|---|---|---|
| `�` | 658 | lone bytes / partial characters with no valid context |
| ` �` | 396 | space + a partial character |
| `��` | 82 | two partial characters |
| `�ి`, `�়`, `�்`, `�ે`, `�്ച`, `�్`, `�\n\n` | 3, 2, 2, 2, 2, 2, 2 | a stray byte, then a Telugu, Bengali, Tamil, Gujarati or Malayalam vowel sign or virama (or newlines) |

Colliding IDs per script class (fragments counted under the script their lead byte points to):
- CJK Han 513, Hangul 230, continuation bytes only 139, Mixed 39, Emoji 35, other scripts 35, punctuation/symbols 31, Latin-ext 21, Private use 12, Arabic 11.
- Indic: Telugu 10, Bengali 6, Gujarati 6, Malayalam 6, Tamil 6, Devanagari 4, Gurmukhi 4, Kannada 4, Oriya 4.

So 50 of its 15,708 Indic-script tokens are affected in the decode table, and none in the raw table.

**Token mix** (by script of the true bytes): ASCII 104,570; Latin-ext 8,488; Devanagari 4,166; Bengali 2,289; Malayalam 1,895; Gujarati 1,836; Telugu 1,502; Kannada 1,501; Tamil 1,134; Oriya 729; Gurmukhi 656 (Indic total 15,708).

## Proof checks and determinism

| check | P=32 | P=64 |
|---|---|---|
| Lemma 1 round-trip, decode / raw | 131,072 / 131,072 rows each | 131,072 / 131,072 rows each |
| Lemma 2: support = {z > 0}, every row; max rel err vs closed form | 1.9e-07 | 1.7e-07 |
| Theorem 1: distinct byte rows = distinct codec rows (decode / raw) | 129,931 / 131,072 | 129,931 / 131,072 |
| decode groups with one codec row | 10 / 10 | 10 / 10 |
| dynamic = cached, bit for bit (IDs tested, decode / raw) | 5,211 / 4,096 | 5,211 / 4,096 |

Determinism hashes (runs 1 = 2 = 3, seeds 0/1/2, threads 1/4/8):

| P | table | SHA-256 |
|---|---|---|
| 32 | decode | `783f26265de9b12a6dc7366c17effab6b7354170bfc0c9635f708e688f5af35f` |
| 32 | raw | `d36cdf74777982365555894c95267db4f2b0b518f25b8db20a4cb0cb64f8fe38` |
| 32 | codec | `fe40c8ad363bd259daad03dca3d012ebd1ec86a285832d8fb9e3a848f83feeba` |
| 64 | decode | `37bb952559640591c24921e23aad3bbfe05e76cabb2e77aea93ca64f1e242ae1` |
| 64 | raw | `32ba57e59de4a20feaed1db4bbfbbbcc0902809fcce4d4854754b318ac7b984a` |
| 64 | codec | `c3b23d5d1d1b7d863a51b4e82c8fc33cd11ff1a7acd5df8b0b4510bbe4252267` |

Run time on this laptop: 62 s (P=32) and 87 s (P=64) of analysis, plus about 45 s and 65 s for the three determinism runs.
