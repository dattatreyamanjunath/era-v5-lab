"""kron_audit: byte-table and collision audit for Kronecker Embeddings.

Pipeline: config -> tokenizer source -> byte tables -> grouping ->
causes / script classes -> codec checks -> reports. See ARCHITECTURE.md.
"""

import os

# CPU only, and quiet tokenizer threads. Set before torch / tokenizers import.
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

SCHEMA_VERSION = 2  # bump when result files change shape or meaning

__all__ = ["SCHEMA_VERSION"]
