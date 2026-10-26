# When do two token IDs get the same Kronecker embedding? (P = 32)

This note proves that the Kronecker codec of
[theschoolofai/kronecker-embeddings](https://github.com/theschoolofai/kronecker-embeddings)
(commit `d07cb54`, package 0.1.1) loses no information about a token's byte row. So two token
IDs share a codec row **if and only if** they share a byte row. Every collision is therefore a
property of the byte table (how token IDs are turned into bytes), never of the codec.

Each statement is followed by a numerical check. The checks run on every row of the decode table
and of the raw byte table, for all six tokenizers of paper Table 3: 921,161 rows per table. Every
number below comes from `results/<tokenizer>/checks.json`. The same values appear, rendered as
tables, in [`results/tables.md`](results/tables.md).

## Setup and notation

| symbol | meaning | value here |
|---|---|---|
| `P` | `pos_dim`, bytes kept per token | 32 |
| `C` | `char_dim`, byte alphabet | 256 |
| `D` | codec width `C·P` | 8192 |
| `ε` | z-norm stabilizer in `kronecker_codec` | 1e-6 |

- `B≤P` is the set of byte strings `b = (b_0, …, b_{L−1})` with `0 ≤ L ≤ P` and each `b_p ∈ {0, …, 255}`. The empty string is `∅`.
- **Index map.** `ι(v, p) = v·P + p`. This is the storage rule in `kronecker_codec` (`lin_idx = byte * pos_dim + pos`). It is the coordinate of `c_v ⊗ p_p` in the paper's Eq. 1.
- **Pre-norm codec.** `κ̃(b) = L^{−1/2} · Σ_{p<L} e_{ι(b_p, p)}` for `L ≥ 1`, and `κ̃(∅) = 0`. Here `e_k` is the k-th unit vector of `R^D`. This is `kronecker_codec(..., z_normalize=False)`.
- **z-norm.** `z(x) = (x − μ(x)·1) / (σ(x) + ε)`, with `μ` the mean over the `D` coordinates and `σ` the sample standard deviation: `torch.std`'s default, dividing by `D − 1`.
- **Codec.** `κ = z ∘ κ̃`. This is what `kronecker_codec` returns with its defaults, and what `KroneckerEmbedding` feeds to its projection.
- **Byte table.** `T(i) = bb[i, :lb[i]]` for token ID `i`, where `bb` is the `uint8 [V, P]` byte buffer and `lb` the `int16 [V]` length buffer.
  - The **decode table** is the repo's `build_byte_buffer`, i.e. `tokenizer.decode([i])`.
  - The **raw byte table** holds the token's true bytes, read from its vocab piece; see [README.md](README.md#the-two-tables).
  - Both are cut to at most 32 bytes on a character boundary.

## Lemma 1 — the pre-norm codec is injective and has unit norm

**Statement.** For every `b ∈ B≤P` with length `L`:

1. The support of `κ̃(b)` is `S(b) = {ι(b_p, p) : 0 ≤ p < L}`. It has exactly `L` elements, and every nonzero entry equals `L^{−1/2}`.
2. If `L ≥ 1`, then `‖κ̃(b)‖₂ = 1` exactly.
3. `κ̃` is injective on `B≤P`, with an explicit inverse:
   - `L = |supp κ̃(b)|`;
   - for each `p < L`, `b_p = (k − p)/P`, where `k` is the unique support index with `k ≡ p (mod P)`.

**Proof.**
- `ι(v, p) mod P = p`, because `0 ≤ p < P`. So the `L` indices `ι(b_p, p)`, `p = 0, …, L−1`, have pairwise different residues mod `P`, and are therefore pairwise different.
- So no two terms of the sum land on the same coordinate, and each of the `L` coordinates in `S(b)` receives exactly `L^{−1/2}`. This proves (1).
- (2) follows: `‖κ̃(b)‖₂² = L · (L^{−1/2})² = 1`.
- For (3), let `x = κ̃(b)`:
  - If `x = 0`, then `L = 0` and `b = ∅`.
  - Otherwise (1) gives `L = |supp x|`. For each `p < L`, exactly one `k ∈ supp x` has `k ≡ p (mod P)`, and `b_p = ⌊k/P⌋`.
- So `x` determines `b`. ∎

**Remark.** Paper §3.2 says `‖κ(b)‖²` is "approximately 1 … assuming distinct `(b_p, p)` pairs, which is the typical case". The pairs are always distinct, because their positions differ. So the pre-norm norm is exactly 1 for every non-empty token, not approximately.

**Numerical check.** For every row, `kronecker_codec(z_normalize=False)` is reshaped to `[256, P]`, i.e. `[byte, position]`. Three things are checked:
- every used position `p < L` has exactly one nonzero entry, and unused positions have none;
- the `argmax` over bytes equals `bb[i, p]`;
- the nonzero value equals `rsqrt(L)`.

| tokenizer | rows | decode table: rows inverted exactly | raw table: rows inverted exactly | max \|‖κ̃‖₂ − 1\| |
|---|---|---|---|---|
| gpt2 | 50,257 | 50,257 | 50,257 | 6.7e-08 |
| llama-3.2 | 128,256 | 128,256 | 128,256 | 6.7e-08 |
| qwen3 | 151,669 | 151,669 | 151,669 | 6.7e-08 |
| gemma-3 | 262,145 | 262,145 | 262,145 | 6.7e-08 |
| deepseek-v3 | 128,815 | 128,815 | 128,815 | 6.7e-08 |
| gpt-oss | 200,019 | 200,019 | 200,019 | 6.7e-08 |

The 6.7e-08 is fp32 rounding of `rsqrt(L)`; one float32 ulp at 1 is 1.2e-07. No table has an empty row: the minimum `L` is 1 everywhere.

## Lemma 2 — z-normalization keeps the information

**Statement.** Let `b ∈ B≤P` with `L ≥ 1`, and let `x = κ̃(b)`. Then:

- `μ(x) = √L / D`
- `Σ_k (x_k − μ)² = 1 − L/D`
- `σ(x) = √((1 − L/D) / (D − 1)) > 0`

and `κ(b) = z(x)` takes exactly two values:

- `a_L = (L^{−1/2} − √L/D) / (σ + ε)` on `S(b)`;
- `c_L = −(√L/D) / (σ + ε)` off `S(b)`;

with `a_L > 0 > c_L`. Hence `S(b) = {k : κ(b)_k > 0}`. Also `κ(∅) = 0`, which differs from every `κ(b)` with `L ≥ 1`. Therefore **`κ` is injective on `B≤P`**.

**Proof.**
- **Mean.** `x` has `L` entries equal to `L^{−1/2}` and `D − L` zeros. So `μ = L · L^{−1/2} / D = √L / D`.
- **Spread.** `Σ (x_k − μ)² = Σ x_k² − D μ² = 1 − L/D`, using Lemma 1(2). Since `L ≤ P = 32 < D = 8192`, this is positive, so `σ > 0`.
- **Two values.** `z` is the affine map `t ↦ (t − μ)/(σ + ε)` with a positive slope. It sends `L^{−1/2}` to `a_L` and `0` to `c_L`.
- **Signs.** `a_L > 0` because `L^{−1/2} > √L/D ⟺ D > L`. And `c_L < 0` is immediate.
- **Support.** So `S(b)` is exactly the set of positive coordinates of `κ(b)`. Then `L = |S(b)|`, and Lemma 1(3) recovers `b` from `S(b)`.
- **Empty string.** For `b = ∅`, `x = 0`, so `μ = σ = 0` and `z(x) = 0/ε = 0`. Every non-empty `κ(b)` has a positive coordinate, so it is not 0. ∎

**It also holds in float32.** The computed on-support value is `(fl(L^{−1/2}) − fl(μ)) / (fl(σ) + ε)`.
- `fl(L^{−1/2}) ≥ 0.176` and `0 < fl(μ) ≤ 7e-4`, so the numerator is positive whatever the rounding.
- The off-support value is `−fl(μ)/(fl(σ) + ε) < 0`.
- So the sign pattern, and with it `S(b)`, survives rounding. Two different byte rows give two different fp32 vectors, bit for bit.

**Numerical check.**
- **Closed form vs torch.** For every row, torch's output is compared with the closed form `a_L` / `c_L`, computed in float64.
- **Sign recovers the support.** `{z > 0}` is checked to equal the support found in Lemma 1.

| tokenizer | decode: support = {z>0} | raw: support = {z>0} | max relative error vs closed form |
|---|---|---|---|
| gpt2 | 50,257 / 50,257 | 50,257 / 50,257 | 1.2e-07 |
| llama-3.2 | 128,256 / 128,256 | 128,256 / 128,256 | 1.9e-07 |
| qwen3 | 151,669 / 151,669 | 151,669 / 151,669 | 1.9e-07 |
| gemma-3 | 262,145 / 262,145 | 262,145 / 262,145 | 1.9e-07 |
| deepseek-v3 | 128,815 / 128,815 | 128,815 / 128,815 | 1.9e-07 |
| gpt-oss | 200,019 / 200,019 | 200,019 / 200,019 | 1.9e-07 |

Closed-form values for a few lengths. All 32 lengths are in [`results/tables.md`](results/tables.md#lemma-2-closed-form-vs-torch-by-length-all-tokenizers-both-tables). "Rows checked" counts both tables of all six tokenizers.

| L | a_L (on support) | c_L (off support) | rows checked | max rel err |
|---|---|---|---|---|
| 1 | 90.490429 | −0.01104754 | 2,652 | 4.5e-08 |
| 2 | 63.982490 | −0.01562454 | 45,097 | 4.0e-08 |
| 4 | 45.236927 | −0.02209913 | 225,888 | 9.3e-08 |
| 8 | 31.979523 | −0.03126053 | 136,949 | 1.7e-08 |
| 16 | 22.601882 | −0.04423069 | 13,639 | 8.6e-08 |
| 32 | 15.966297 | −0.06261293 | 3,012 | 4.4e-08 |

`a_L` falls as `L` grows: a one-byte token's codec row is one spike of height ≈ 90, while a 32-byte token spreads over 32 spikes of ≈ 16. The gap `a_L − c_L` never closes, since `D − L ≥ 8160`.

## Theorem 1 — codec collisions are exactly byte-table collisions

**Statement.** Let `T` be any byte table with rows in `B≤P` (the decode table, the raw table, or any other). Let `K(i)` be the codec row that `KroneckerEmbedding` computes for token ID `i`, in either `mode="dynamic"` or `mode="cached"`. Then for all IDs `i, j`:

    K(i) = K(j)   ⟺   T(i) = T(j).

**Consequences.**

- **(a)** The number of distinct codec rows equals the number of distinct byte rows. The codec's collision groups are exactly the byte table's collision groups.
- **(b)** The embedding is `E(i) = W·K(i)`. So `T(i) = T(j)` forces `E(i) = E(j)` for every projection `W`, at every training step. Byte-table collisions are permanent: no amount of training separates them. A collision can only be removed by changing the byte table.
- **(c) Truncation (raw table).** Let `trunc` be the boundary-safe cut to 32 bytes. Two tokens collide iff `trunc(bytes(i)) = trunc(bytes(j))`. So the paper's sentence (§4.2, §7) *"truncated tokens still receive distinct embeddings based on their first 32 bytes"* holds iff no two tokens share a 32-byte prefix (cut on a character boundary). It does not hold for any of the six tokenizers:

  | tokenizer | tokens > 32 bytes | of these, sharing a row with another token |
  |---|---|---|
  | gpt2 | 14 | 12 |
  | llama-3.2 | 231 | 210 |
  | qwen3 | 240 | 198 |
  | gemma-3 | 379 | 86 |
  | deepseek-v3 | 771 | 59 |
  | gpt-oss | 266 | 171 |

- **(d) Decoding (decode table).** Two tokens collide whenever `tokenizer.decode` returns the same string for both. In byte-level BPE, a token that is a piece of a multi-byte character decodes to U+FFFD (`EF BF BD`). So all such tokens with the same valid context collapse into one row. The largest group is 1,067 IDs for Qwen3, which all decode to `�`. See [collisions.md](collisions.md).

**Proof.**
- **Every row is computed on its own.** In `kronecker_codec`, row `r` of the output depends only on `bb[r, :lb[r]]`:
  - `scatter_add_` writes only into row `r`;
  - positions `≥ lb[r]` are masked out;
  - the z-norm `mean`/`std` reduce over the last dimension only.

  So row `r` is `κ(T(r))`.
- **Both modes give that row.** The cached mode computes `kronecker_codec(bb, lb)` once and returns row `i` with `index_select`. The dynamic mode computes `kronecker_codec(bb[ids], lb[ids])` and returns the row for `i`. Either way `K(i) = κ(T(i))`.
- **(⇐)** is immediate.
- **(⇒)** If `κ(T(i)) = κ(T(j))`, then Lemma 2 (injectivity) gives `T(i) = T(j)`. ∎

**Numerical check.** For both tables of every tokenizer:
- **Hashing.** Every z-normalized codec row (fp32, 32 KiB) is hashed with SHA-256. Two counts are compared: distinct codec-row hashes, and distinct byte rows.
- **Group check.** For every collision group, all members are checked to have one codec hash. No hash may be shared by two different byte rows.
- **Modes.** `KroneckerEmbedding` is built in both modes, with the same projection weights, over every collision member plus 4,096 random IDs. The codec rows and the projected embeddings are compared bit for bit.
- **Batching.** One full-batch call is compared with the chunked calls used for hashing.

| tokenizer | table | distinct byte rows | distinct codec rows | groups with one codec row | dynamic = cached (IDs tested) |
|---|---|---|---|---|---|
| gpt2 | decode | 49,914 | 49,914 | 14 / 14 | yes (4,416) |
| gpt2 | raw | 50,247 | 50,247 | 7 / 7 | yes (4,110) |
| llama-3.2 | decode | 126,845 | 126,845 | 41 / 41 | yes (5,499) |
| llama-3.2 | raw | 128,061 | 128,061 | 28 / 28 | yes (4,316) |
| qwen3 | decode | 150,149 | 150,149 | 36 / 36 | yes (5,619) |
| qwen3 | raw | 151,485 | 151,485 | 25 / 25 | yes (4,301) |
| gemma-3 | decode | 261,968 | 261,968 | 159 / 159 | yes (4,425) |
| gemma-3 | raw | 261,968 | 261,968 | 159 / 159 | yes (4,425) |
| deepseek-v3 | decode | 127,691 | 127,691 | 50 / 50 | yes (5,233) |
| deepseek-v3 | raw | 128,761 | 128,761 | 14 / 14 | yes (4,162) |
| gpt-oss | decode | 198,661 | 198,661 | 47 / 47 | yes (5,475) |
| gpt-oss | raw | 199,864 | 199,864 | 29 / 29 | yes (4,274) |

In every case, no byte row had two codec hashes and no codec hash was shared by two byte rows. The full-batch and chunked codec rows matched bit for bit.

## Two checks on the byte tables themselves

These are not part of the lemmas, but the counts above depend on them (`results/<tokenizer>/summary.json`, field `tables`):

- **Our decode table is the repo's.** Repacking `token_id_to_bytes` output with the repo's `utf8_safe_truncate` reproduces `build_byte_buffer` exactly, for all six tokenizers.
- **Our truncation agrees with the repo's on valid text.** The raw table uses a boundary cut that also works on partial UTF-8. On every valid-UTF-8 token longer than 32 bytes, it gives the same bytes as the repo's `utf8_safe_truncate`. That is 14 / 231 / 240 / 379 / 769 / 266 tokens, all equal. DeepSeek also has 2 long tokens that are not valid UTF-8 (Myanmar text starting with a stray continuation byte). On those, the repo's `utf8_safe_truncate` would return `b""`.

## Summary

- **Lemma 1:** the byte row can be read back from `κ̃`, whose norm is exactly 1.
- **Lemma 2:** the byte row can still be read back after z-norm, from the sign pattern; this also holds in fp32.
- **Theorem 1:** the Kronecker embedding identifies two tokens exactly when their byte rows match.

So every collision counted in [collisions.md](collisions.md) is a real, permanent embedding collision. Every one of them comes from the byte table: decoding to U+FFFD, truncation at 32 bytes, or byte-fallback aliases. None comes from the codec.
