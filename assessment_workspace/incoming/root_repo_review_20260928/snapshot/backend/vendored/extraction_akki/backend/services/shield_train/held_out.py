"""shield_train.held_out — deterministic held-out slice + sha256 banking.

Owner ruling verbatim (2026-09-06T~13:XXZ):
    "HELD-OUT SLICE FIRST (STEP 2 order unchanged): bank the deterministic
     split + sha256 BEFORE any training byte moves."

The split is fully deterministic on row order:
  - The row_executor emits rows in primary-key order (ORDER BY id).
  - The LAST floor(N * 0.20) rows form the held-out slice.
  - Both slices are sha256'd via canonical JSONL serialization
    (json.dumps(row, sort_keys=True) + "\n", utf-8).

`bank_held_out_slice_hash` writes the receipt to
`SHIELD_TRAIN_HELD_OUT_RECEIPT_DIR` (default
`phase0/shield_train_receipts/held_out_slices/`) BEFORE any staging or
training call. The receipt carries `banked_before_first_run_starts=True`
and NEVER row content — only hashes, counts, and seed.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _canonical_jsonl_bytes(rows: List[Dict[str, Any]]) -> bytes:
    """Deterministic JSONL serialization: one row per line, sort_keys=True,
    utf-8, LF-terminated. Matches shield_train.pipeline.build_masked_corpus_file
    on-disk shape so sha256 comparison is meaningful."""
    parts = []
    for r in rows:
        parts.append(json.dumps(r, sort_keys=True) + "\n")
    return "".join(parts).encode("utf-8")


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def deterministic_20pct_tail_split(
    rows: List[Dict[str, Any]],
    seed: int = 31337,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    """Split `rows` into (train, held_out, meta).

    Held-out = last floor(N * 0.20) rows (minimum 1 for non-empty input).
    Train = first N - held_out rows.
    Seed is banked in meta but does NOT shuffle — tail selection is
    deterministic on the row_executor's already-deterministic order.
    """
    if not rows:
        raise ValueError(
            "rows must be non-empty for deterministic held-out split; "
            "row_executor returned zero rows"
        )
    n = len(rows)
    held_size = n // 5  # floor(N * 0.20)
    if held_size == 0:
        held_size = 1  # minimum 1 held-out row for tiny corpora
    split = n - held_size
    train = list(rows[:split])
    held = list(rows[split:])
    meta: Dict[str, Any] = {
        "seed": int(seed),
        "total_row_count": n,
        "train_row_count": len(train),
        "held_out_row_count": len(held),
        "train_sha256": _sha256_hex(_canonical_jsonl_bytes(train)),
        "held_out_sha256": _sha256_hex(_canonical_jsonl_bytes(held)),
        "split_method": "deterministic_20pct_tail",
    }
    return train, held, meta


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_receipt_dir() -> Path:
    return Path(os.environ.get(
        "SHIELD_TRAIN_HELD_OUT_RECEIPT_DIR",
        "/app/assessment_workspace/phase0/shield_train_receipts/held_out_slices",
    ))


def bank_held_out_slice_hash(
    run_id: str,
    table_context: str,
    split_meta: Dict[str, Any],
    out_dir: str = None,
) -> str:
    """Write held-out slice hash receipt BEFORE any training byte moves.

    Receipt shape (JSON):
      {
        "kind": "held_out_slice_hash_receipt",
        "at_utc": "...",
        "run_id": "...",
        "table_context": "...",
        "seed": int,
        "total_row_count": int,
        "train_row_count": int,
        "held_out_row_count": int,
        "train_sha256": "hex",
        "held_out_sha256": "hex",
        "split_method": "deterministic_20pct_tail",
        "banked_before_first_run_starts": true
      }

    Returns the absolute path of the written receipt file.
    NEVER writes row content — only hashes + counts.
    """
    d = Path(out_dir) if out_dir else _default_receipt_dir()
    d.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_run = str(run_id).replace("/", "_").replace(":", "_")
    p = d / f"held_out_{safe_run}_{ts}.json"
    body: Dict[str, Any] = {
        "kind": "held_out_slice_hash_receipt",
        "at_utc": _iso_utc(),
        "run_id": str(run_id),
        "table_context": str(table_context),
        "seed": split_meta.get("seed"),
        "total_row_count": split_meta.get("total_row_count"),
        "train_row_count": split_meta.get("train_row_count"),
        "held_out_row_count": split_meta.get("held_out_row_count"),
        "train_sha256": split_meta.get("train_sha256"),
        "held_out_sha256": split_meta.get("held_out_sha256"),
        "split_method": split_meta.get("split_method"),
        "banked_before_first_run_starts": True,
    }
    p.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    return str(p)
