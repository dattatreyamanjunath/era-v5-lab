# When do two token IDs get the same Kronecker embedding? (any P; checked at P = 32 and P = 64)

This note proves that the Kronecker codec of
[theschoolofai/kronecker-embeddings](https://github.com/theschoolofai/kronecker-embeddings)
(commit `d07cb54`, package 0.1.1) loses no information about a token's byte row, **for every
`P = pos_dim`**. So two token IDs share a codec row **if and only if** they share a byte row.
Every collision is therefore a property of the byte table (how token IDs are turned into bytes),
never of the codec.

Each statement is followed by a numerical check at **P = 32** and **P = 64**. The checks run on every row of the decode table and of the raw byte table, for all six tokenizers of paper Table 3: 921,161 rows per table, per P. They run through the repo's own `kronecker_codec` (`kron_audit/codec_checks.py`).

Every number below comes from `results/<run>/<tokenizer>/checks.json`, with `<run>` = `p32` or `p64`. The same values appear, rendered, in [`results/p32/tables.md`](results/p32/tables.md) and [`results/p64/tables.md`](results/p64/tables.md).

## Setup and notation

| symbol | meaning | values checked |
|---|---|---|
| `P` | `pos_dim`, bytes kept per token | 32, 64 |
| `C` | `char_dim`, byte alphabet | 256 |
| `D` | codec width `C·P` | 8,192 and 16,384 |
| `ε` | z-norm stabilizer in `kronecker_codec` | 1e-6 |

- `B≤P` is the set of byte strings `b = (b_0, …, b_{L−1})` with `0 ≤ L ≤ P` and each `b_p ∈ {0, …, 255}`. The empty string is `∅`.
- **Index map.** `ι(v, p) = v·P + p`. This is the storage rule in `kronecker_codec` (`lin_idx = byte * pos_dim + pos`). It is the coordinate of `c_v ⊗ p_p` in the paper's Eq. 1.
- **Pre-norm codec.** `κ̃(b) = L^{−1/2} · Σ_{p<L} e_{ι(b_p, p)}` for `L ≥ 1`, and `κ̃(∅) = 0`. Here `e_k` is the k-th unit vector of `R^D`. This is `kronecker_codec(..., z_normalize=False)`.
- **z-norm.** `z(x) = (x − μ(x)·1) / (σ(x) + ε)`, with `μ` the mean over the `D` coordinates and `σ` the sample standard deviation: `torch.std`'s default, dividing by `D − 1`.
- **Codec.** `κ = z ∘ κ̃`. This is what `kronecker_codec` returns with its defaults, and what `KroneckerEmbedding` feeds to its projection.
- **Byte table.** `T(i) = bb[i, :lb[i]]` for token ID `i`, where `bb` is the `uint8 [V, P]` byte buffer and `lb` the `int16 [V]` length buffer.
  - The **decode table** is the repo's `build_byte_buffer(tok, pos_dim=P)`, i.e. `tokenizer.decode([i])`.
  - The **raw byte table** holds the token's true bytes, read from its vocab piece; see [README.md](README.md#the-two-tables).
  - Both are cut to at most `P` bytes on a character boundary.

**One fact about D and P is used throughout:** `D = 256·P`, so every length satisfies `L ≤ P < D`, for every P ≥ 1.

## Lemma 1 — the pre-norm codec is injective and has unit norm

**Statement.** For every `P ≥ 1` and every `b ∈ B≤P` with length `L`:

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

**Without length normalization** (`length_normalize=False`), the same proof gives nonzero entries equal to 1 and `‖κ̃(b)‖₂ = √L`. The inverse is unchanged. `kron_audit` checks whichever setting the config uses.

**Numerical check.** For every row, `kronecker_codec(z_normalize=False)` is reshaped to `[256, P]`, i.e. `[byte, position]`. Three things are checked:
- every used position `p < L` has exactly one nonzero entry, and unused positions have none;
- the `argmax` over bytes equals `bb[i, p]`;
- the nonzero value equals `rsqrt(L)`.

| tokenizer | rows | P=32: rows inverted exactly (decode / raw) | P=64: rows inverted exactly (decode / raw) |
|---|---|---|---|
| gpt2 | 50,257 | 50,257 / 50,257 | 50,257 / 50,257 |
| llama-3.2 | 128,256 | 128,256 / 128,256 | 128,256 / 128,256 |
| qwen3 | 151,669 | 151,669 / 151,669 | 151,669 / 151,669 |
| gemma-3 | 262,145 | 262,145 / 262,145 | 262,145 / 262,145 |
| deepseek-v3 | 128,815 | 128,815 / 128,815 | 128,815 / 128,815 |
| gpt-oss | 200,019 | 200,019 / 200,019 | 200,019 / 200,019 |

The largest deviation of `‖κ̃‖₂` from 1 over all rows is 6.7e-08 at P=32 and 1.2e-07 at P=64. That is fp32 rounding of `rsqrt(L)`; one float32 ulp at 1 is 1.2e-07. No table has an empty row: the minimum `L` is 1 everywhere.

## Lemma 2 — z-normalization keeps the information

**Statement.** Let `b ∈ B≤P` with `L ≥ 1`, and let `x = κ̃(b)`. Then:

- `μ(x) = √L / D`
- `Σ_k (x_k − μ)² = 1 − L/D`
- `σ(x) = √((1 − L/D) / (D − 1)) > 0`

and `κ(b) = z(x)` takes exactly two values:

- `a_L = (L^{−1/2} − √L/D) / (σ + ε)` on `S(b)`;
- `c_L = −(√L/D) / (σ + ε)` off `S(b)`;

with `a_L > 0 > c_L`. Hence `S(b) = {k : κ(b)_k > 0}`. Also `κ(∅) = 0`, which differs from every `κ(b)` with `L ≥ 1`. Therefore **`κ` is injective on `B≤P`, for every P**.

**Proof.**
- **Mean.** `x` has `L` entries equal to `L^{−1/2}` and `D − L` zeros. So `μ = L · L^{−1/2} / D = √L / D`.
- **Spread.** `Σ (x_k − μ)² = Σ x_k² − D μ² = 1 − L/D`, using Lemma 1(2). Since `L ≤ P < D = 256·P`, this is positive, so `σ > 0`.
- **Two values.** `z` is the affine map `t ↦ (t − μ)/(σ + ε)` with a positive slope. It sends `L^{−1/2}` to `a_L` and `0` to `c_L`.
- **Signs.** `a_L > 0` because `L^{−1/2} > √L/D ⟺ D > L`. And `c_L < 0` is immediate.
- **Support.** So `S(b)` is exactly the set of positive coordinates of `κ(b)`. Then `L = |S(b)|`, and Lemma 1(3) recovers `b` from `S(b)`.
- **Empty string.** For `b = ∅`, `x = 0`, so `μ = σ = 0` and `z(x) = 0/ε = 0`. Every non-empty `κ(b)` has a positive coordinate, so it is not 0. ∎

(With `length_normalize=False` the entries are 1 instead of `L^{−1/2}`, giving `μ = L/D` and `σ = √(L(1 − L/D)/(D − 1))`. The same sign argument applies; `kron_audit.codec_checks.closed_form` handles both.)

**It also holds in float32.** The computed on-support value is `(fl(L^{−1/2}) − fl(μ)) / (fl(σ) + ε)`.
- `fl(L^{−1/2}) ≥ P^{−1/2}`: at least 0.177 at P=32 and 0.125 at P=64.
- `0 < fl(μ) ≤ √P/D = 1/(256·√P)`: at most 6.9e-4 at P=32 and 4.9e-4 at P=64.
- So the numerator is positive whatever the rounding, and the off-support value `−fl(μ)/(fl(σ) + ε)` is negative.
- So the sign pattern, and with it `S(b)`, survives rounding. Two different byte rows give two different fp32 vectors, bit for bit.

**Numerical check.**
- **Closed form vs torch.** For every row, torch's output is compared with the closed form `a_L` / `c_L`, computed in float64.
- **Sign recovers the support.** `{z > 0}` is checked to equal the support found in Lemma 1.

| tokenizer | P=32: support = {z>0} (decode / raw) | P=32: max rel err | P=64: support = {z>0} (decode / raw) | P=64: max rel err |
|---|---|---|---|---|
| gpt2 | 50,257 / 50,257 | 1.2e-07 | 50,257 / 50,257 | 1.3e-07 |
| llama-3.2 | 128,256 / 128,256 | 1.9e-07 | 128,256 / 128,256 | 1.7e-07 |
| qwen3 | 151,669 / 151,669 | 1.9e-07 | 151,669 / 151,669 | 1.7e-07 |
| gemma-3 | 262,145 / 262,145 | 1.9e-07 | 262,145 / 262,145 | 1.7e-07 |
| deepseek-v3 | 128,815 / 128,815 | 1.9e-07 | 128,815 / 128,815 | 1.7e-07 |
| gpt-oss | 200,019 / 200,019 | 1.9e-07 | 200,019 / 200,019 | 1.7e-07 |

Closed-form values for a few lengths ("rows" counts both tables of all six tokenizers). Every length is in the `tables.md` of each run.

| L | P=32: a_L | P=32: c_L | P=32: rows | P=64: a_L | P=64: c_L | P=64: rows |
|---|---|---|---|---|---|---|
| 1 | 90.490429 | −0.01104754 | 2,652 | 127.975807 | −0.00781150 | 2,652 |
| 2 | 63.982490 | −0.01562454 | 45,097 | 90.489798 | −0.01104747 | 45,097 |
| 4 | 45.236927 | −0.02209913 | 225,888 | 63.982044 | −0.01562443 | 225,888 |
| 8 | 31.979523 | −0.03126053 | 136,949 | 45.236612 | −0.02209898 | 136,949 |
| 16 | 22.601882 | −0.04423069 | 13,639 | 31.979300 | −0.03126031 | 13,639 |
| 32 | 15.966297 | −0.06261293 | 3,012 | 22.601723 | −0.04423038 | 312 |
| 64 | – | – | – | 15.966184 | −0.06261249 | 772 |

**How the values scale.** `a_L` falls as `L` grows: a one-byte token is one spike, while a P-byte token spreads over P smaller spikes. Doubling P (and so D) multiplies every value by about √2, because `σ ≈ 1/√D`. So `a_L` at P=64 is close to `a_{L/2}` at P=32. The gap `a_L − c_L` never closes, since `D − L ≥ 255·P`.

At P=32, the L=32 row counts every token of 32 bytes or more; at P=64 most of those are no longer cut. That is why L=32 drops from 3,012 rows to 312.

## Theorem 1 — codec collisions are exactly byte-table collisions

**Statement.** Fix any P. Let `T` be any byte table with rows in `B≤P` (the decode table, the raw table, or any other). Let `K(i)` be the codec row that `KroneckerEmbedding` computes for token ID `i`, in either `mode="dynamic"` or `mode="cached"`. Then for all IDs `i, j`:

    K(i) = K(j)   ⟺   T(i) = T(j).

**Consequences.**

- **(a)** The number of distinct codec rows equals the number of distinct byte rows. The codec's collision groups are exactly the byte table's collision groups.
- **(b)** The embedding is `E(i) = W·K(i)`. So `T(i) = T(j)` forces `E(i) = E(j)` for every projection `W`, at every training step. Byte-table collisions are permanent: no amount of training separates them. A collision can only be removed by changing the byte table, or P.
- **(c) Truncation (raw table).** Let `trunc_P` be the boundary-safe cut to P bytes. Two tokens collide iff `trunc_P(bytes(i)) = trunc_P(bytes(j))`. So the paper's sentence (§4.2, §7) *"truncated tokens still receive distinct embeddings based on their first 32 bytes"* holds at a given P iff no two tokens share a P-byte prefix (cut on a character boundary):

  | tokenizer | P=32: tokens > 32 B | sharing a row | P=64: tokens > 64 B | sharing a row |
  |---|---|---|---|---|
  | gpt2 | 14 | 12 | 3 | 1 |
  | llama-3.2 | 231 | 210 | 123 | 112 |
  | qwen3 | 240 | 198 | 121 | 112 |
  | gemma-3 | 379 | 86 | 0 | 0 |
  | deepseek-v3 | 771 | 59 | 13 | 10 |
  | gpt-oss | 266 | 171 | 85 | 77 |

  It fails for all six tokenizers at P=32. At P=64 it holds only for Gemma-3, which has no token longer than 64 bytes.
- **(d) Decoding (decode table).** Two tokens collide whenever `tokenizer.decode` returns the same string for both. In byte-level BPE, a token that is a piece of a multi-byte character decodes to U+FFFD (`EF BF BD`). So all such tokens with the same valid context collapse into one row, at any P. The largest group is 1,067 IDs for Qwen3, which all decode to `�`. See [collisions.md](collisions.md) and [p64.md](p64.md).

**Proof.**
- **Every row is computed on its own.** In `kronecker_codec`, row `r` of the output depends only on `bb[r, :lb[r]]`:
  - `scatter_add_` writes only into row `r`;
  - positions `≥ lb[r]` are masked out;
  - the z-norm `mean`/`std` reduce over the last dimension only.

  So row `r` is `κ(T(r))`.
- **Both modes give that row.** The cached mode computes `kronecker_codec(bb, lb)` once and returns row `i` with `index_select`. The dynamic mode computes `kronecker_codec(bb[ids], lb[ids])` and returns the row for `i`. Either way `K(i) = κ(T(i))`.
- **(⇐)** is immediate.
- **(⇒)** If `κ(T(i)) = κ(T(j))`, then Lemma 2 (injectivity) gives `T(i) = T(j)`. ∎

**Numerical check.** For both tables of every tokenizer, at each P:
- **Hashing.** Every z-normalized codec row (fp32: 32 KiB at P=32, 64 KiB at P=64) is hashed with SHA-256. Two counts are compared: distinct codec-row hashes, and distinct byte rows.
- **Group check.** For every collision group, all members are checked to have one codec hash. No hash may be shared by two different byte rows.
- **Modes.** `KroneckerEmbedding` is built in both modes, with the same projection weights, over every collision member plus 4,096 random IDs. The codec rows and the projected embeddings are compared bit for bit.
- **Batching.** One full-batch call is compared with the chunked calls used for hashing.

| tokenizer | table | P=32: byte rows = codec rows | P=32: groups → 1 codec row | P=64: byte rows = codec rows | P=64: groups → 1 codec row |
|---|---|---|---|---|---|
| gpt2 | decode | 49,914 = 49,914 | 14 / 14 | 49,923 = 49,923 | 8 / 8 |
| gpt2 | raw | 50,247 = 50,247 | 7 / 7 | 50,256 = 50,256 | 1 / 1 |
| llama-3.2 | decode | 126,845 = 126,845 | 41 / 41 | 126,940 = 126,940 | 31 / 31 |
| llama-3.2 | raw | 128,061 = 128,061 | 28 / 28 | 128,156 = 128,156 | 18 / 18 |
| qwen3 | decode | 150,149 = 150,149 | 36 / 36 | 150,233 = 150,233 | 29 / 29 |
| qwen3 | raw | 151,485 = 151,485 | 25 / 25 | 151,569 = 151,569 | 18 / 18 |
| gemma-3 | decode | 261,968 = 261,968 | 159 / 159 | 262,035 = 262,035 | 110 / 110 |
| gemma-3 | raw | 261,968 = 261,968 | 159 / 159 | 262,035 = 262,035 | 110 / 110 |
| deepseek-v3 | decode | 127,691 = 127,691 | 50 / 50 | 127,736 = 127,736 | 41 / 41 |
| deepseek-v3 | raw | 128,761 = 128,761 | 14 / 14 | 128,806 = 128,806 | 5 / 5 |
| gpt-oss | decode | 198,661 = 198,661 | 47 / 47 | 198,744 = 198,744 | 29 / 29 |
| gpt-oss | raw | 199,864 = 199,864 | 29 / 29 | 199,947 = 199,947 | 11 / 11 |

In every case, at both P:
- no byte row had two codec hashes, and no codec hash was shared by two byte rows;
- `dynamic` and `cached` agreed bit for bit (4,097–5,619 IDs tested per table);
- full-batch and chunked codec rows matched.

## Two checks on the byte tables themselves

These are not part of the lemmas, but the counts above depend on them (`results/<run>/<tokenizer>/summary.json`, field `tables`):

- **Our decode table is the repo's.** Repacking `token_id_to_bytes` output with the repo's `utf8_safe_truncate` reproduces `build_byte_buffer(tok, pos_dim=P)` exactly, for all six tokenizers at both P.
- **Our truncation agrees with the repo's on valid text.** The raw table uses a boundary cut that also works on partial UTF-8. On every valid-UTF-8 token longer than P bytes, it gives the same bytes as the repo's `utf8_safe_truncate`:
  - **P=32:** 14 / 231 / 240 / 379 / 769 / 266 tokens, all equal.
  - **P=64:** 3 / 123 / 121 / 0 / 13 / 85 tokens, all equal.

  At P=32, DeepSeek also has 2 long tokens that are not valid UTF-8 (Myanmar text starting with a stray continuation byte). On those, the repo's `utf8_safe_truncate` would return `b""`. The test suite also checks the two cuts against each other on random text for P ∈ {4, 8, 32, 64}.

## Summary

- **Lemma 1:** for any P, the byte row can be read back from `κ̃`, whose norm is exactly 1.
- **Lemma 2:** for any P, the byte row can still be read back after z-norm, from the sign pattern; this also holds in fp32.
- **Theorem 1:** the Kronecker embedding identifies two tokens exactly when their byte rows match.

So every collision counted in [collisions.md](collisions.md) (P=32) and [p64.md](p64.md) (P=64) is a real, permanent embedding collision. Every one of them comes from the byte table: decoding to U+FFFD, truncation at P bytes, or byte-fallback aliases. None comes from the codec.
