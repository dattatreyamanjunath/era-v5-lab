# Architecture of `kron_audit`

`kron_audit` checks, for any Kronecker codec setting and any tokenizer, which token IDs end up with the same embedding, and why. This page covers how the package is split, where to extend it, and how its cost grows with vocabulary size `V` and bytes-per-token `P`.

## Data flow

```
configs/*.yaml ──► config.load_config ──► ExperimentConfig (one typed object, no globals)
                                              │
            ┌─────────────────────────────────┘  pipeline.run_experiment: for each TokenizerSpec
            ▼
 sources.load_tokenizer ──► LoadedTokenizer (tok, family, provenance)
            │
            ▼
 tables.build_tables ──► TablePair
            │               ├─ decode: ByteTable  (repo's build_byte_buffer, P from config)
            │               └─ raw:    ByteTable  (raw_bytes strategies + boundary_truncate)
            ▼
 grouping.find_groups ──► Groups (np.unique over fixed-width row records)
            │
            ├─► causes.assign_cause   (ordered CauseRule list)
            ├─► script_class.token_class
            ▼
 analysis.analyse ──► TableReport ──► results/<run>/<tok>/{summary.json, groups_*.jsonl, collisions_by_script_*.csv}
            │
            ▼
 codec_checks.run_checks / mode_check ──► results/<run>/<tok>/checks.json
            │
            ▼
 determinism.run_workers (N fresh processes) ──► results/<run>/determinism.json
            │
            ▼
 report.render_run ──► results/<run>/tables.md        compare.compare_runs ──► results/compare_<a>_<b>.md
```

Each stage takes plain data from the stage before it and writes plain files. `report` and `compare` read only those files, so any past run can be re-rendered or compared without recomputing.

## Modules

| module | does one thing | key types / functions |
|---|---|---|
| `config.py` | load, override and validate the experiment | `ExperimentConfig`, `CodecConfig`, `TokenizerSpec`, `load_config`, `tokenizer_digest` |
| `paths.py` | every file location for a run | `RunPaths` |
| `sources.py` | get a tokenizer from an HF repo, a folder or a `tokenizer.json`; detect its family | `load_tokenizer`, `FAMILY_DETECTORS` |
| `raw_bytes.py` | the true bytes of every ID | `RAW_STRATEGIES`, `register_strategy`, `raw_bytes` |
| `bytes_util.py` | pure byte helpers (truncation, packing, hashing) | `boundary_truncate`, `pack`, `table_sha256` |
| `tables.py` | the two `[V, P]` byte tables | `ByteTable`, `TablePair`, `build_tables` |
| `grouping.py` | IDs that share a row | `find_groups` |
| `causes.py` | why a group exists | `CauseRule`, `DEFAULT_RULES`, `assign_cause` |
| `script_class.py` | which script a token belongs to | `token_class` |
| `analysis.py` | per-group and per-script report for one table | `analyse`, `TableReport`, `truncation_claim` |
| `codec_checks.py` | Lemma 1, Lemma 2, Theorem 1, dynamic vs cached | `run_checks`, `mode_check`, `closed_form` |
| `determinism.py` | N fresh decode processes, hashes compared | `run_workers`, `worker` |
| `pipeline.py` | run everything, resume, isolate failures | `run_experiment`, `run_tokenizer` |
| `report.py`, `compare.py` | markdown from saved results | `render_run`, `compare_runs` |
| `__main__.py` | CLI | `run`, `report`, `compare`, `determinism` |

## Extension points

**A new experiment** (different P, codec flags or tokenizer set) is a new YAML file. There is no code change. CLI overrides (`--pos-dim`, `--tokenizers`, `--name`) cover one-off variations; the exact config used is saved as `results/<run>/config.resolved.yaml`.

**A new tokenizer**, in one of these forms:
- **HF repo:** `{name: x, source: org/repo, revision: <commit>}`.
- **Local tokenizer:** `{name: x, source: ./path/tokenizer.json}`, or a folder holding `tokenizer.json` (plus `tokenizer_config.json` for special tokens).

Its family is detected from the backend JSON:
- **`bbpe`:** a ByteLevel decoder or pre-tokenizer.
- **`sentencepiece`:** byte fallback, a Metaspace component, or a `▁` Replace decoder.
- **`wordpiece`:** a WordPiece model.
- **`decode`:** anything else. Its raw table then equals its decode table, so check the summary's `family` field.

`family:` in the config overrides detection.

**A new tokenizer family:** add a detector to `sources.FAMILY_DETECTORS` and a strategy with `raw_bytes.register_strategy(name, fn)`. The function maps `(piece, token_id, ctx)` to bytes, or to `None` for "use the literal text". The shared rules (unassigned, special, `<0xNN>`, literal-only added tokens) run before any strategy.

**A new collision cause:** append a `CauseRule(name, description, applies, tables)` to `causes.DEFAULT_RULES`, or pass your own list to `analysis.analyse`. The first rule that matches wins. Groups no rule explains are labelled `unexplained` and still reported.

**A new script class:** add a `(lo, hi, class)` range to `script_class.RANGES`.

## How cost grows

`V` = vocabulary size, `P` = bytes per token, `D = 256·P` (codec width), `C` = rows per codec chunk.

| stage | time | memory | notes |
|---|---|---|---|
| decode table | O(V) `tokenizer.decode` calls | O(V·P) | the slowest step for large V (single-threaded Rust decode) |
| raw table | O(V·token length) | O(V·P) | |
| grouping | O(V log V) in C (`np.unique`) | O(V·(P+2)) | replaced a Python dict over V |
| causes + script classes | O(colliding IDs + V) | O(V) | |
| codec checks | O(V·D) | O(C·D) | streamed; `chunk_rows: auto` picks `C ≈ chunk_bytes / (4·D)`: 4,096 rows at P=32, 2,048 at P=64 with the default 128 MB |
| row hashing | O(V·D) bytes through SHA-256 | O(V) digests | |
| determinism | N × (decode + codec) | per process | runs sequentially, one fresh process each |

Doubling P doubles the codec-check time and halves the rows per chunk, so peak memory stays the same. The byte tables (`V × P` bytes) are the only part that grows with both V and P; at V = 262K and P = 64 they are about 17 MB each.

**Parallelism.** `compute.max_workers: N` runs N tokenizers at once in separate processes, each needing roughly 1–2 GB at P ≤ 64. The default is 1, which suits an 8 GB laptop.

**Resume.** A tokenizer is skipped when its saved `summary.json` has the same digest (codec + tokenizer spec + schema + library version); `--force` redoes it. `summary.json` is written last, so an interrupted tokenizer is simply redone.

**Failure isolation.** An exception in one tokenizer is recorded in `overview.json` with its traceback. The other tokenizers still run, and the exit code is non-zero.

## Tests

`pytest` (offline; uses the local Hugging Face cache) covers:
- truncation against the repo's `utf8_safe_truncate`, for P ∈ {4, 8, 32, 64};
- grouping against a dict reference, including rows that differ only in length;
- every cause rule, and script classes of fragments;
- Lemma 2's closed form against `kronecker_codec` for P ∈ {8, 32, 64}, and the checks with z-norm or length-norm turned off;
- chunk-size invariance;
- config validation, overrides, digest and round-trip;
- family detection, and a local `tokenizer.json` giving the same tables as the HF repo;
- an end-to-end run: GPT-2 at P=8 with determinism, resume, `--force`, a P=4 run and the comparison;
- failure isolation.
