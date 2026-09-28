"""shield_train.pipeline — masked-file transport + cleanup + governed LoRA run.

Composes:
  * row_executor.execute_row_bearing_query — governed row extraction
  * build_masked_corpus_file              — write corpus JSONL + sha256
  * stage_corpus_to_host                  — transport with hash verification
  * cleanup_remote_corpus                 — post-run cleanup receipt
  * execute_governed_lora_run             — the end-to-end governed run;
    gates on masking-tier admission (raises MaskingTierNotAdmitted while
    admission remains parked).

Zero-influence: every operation returns a receipt-shaped dict. Failures
raise typed exceptions; the pipeline does NOT partially-succeed
silently. Cleanup is a distinct step from run — a caller can force
cleanup independently.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# Exceptions
# ============================================================================

class CorpusIntegrityRefusal(ValueError):
    """Belt-and-braces PII leak-check at the file boundary — refuses a
    corpus row whose value matches phone/ID regex after masking. Should
    NEVER fire if the row-executor did its job; this is defence-in-depth."""


class TransportIntegrityRefusal(RuntimeError):
    """sha256 mismatch between local and remote after `put_file`."""


class MaskingTierNotAdmitted(RuntimeError):
    """The masking tier is declared but not admissible in the current
    env — the admission gate that remains after the pre-r2 stub is
    removed. Owner ruling is what changes this."""


# ============================================================================
# Belt-and-braces leak regex (aligned with row_executor)
# ============================================================================

_PHONE_LEAK = [
    re.compile(r"\+?254[\s\-]*[17](?:[\s\-]*\d){8,9}"),
    re.compile(r"(?<!\d)0[\s\-]*[17](?:[\s\-]*\d){8,9}"),
]
_ID_LEAK = re.compile(r"(?<![\d\w])\d{7,10}(?![\d\w])")


def _has_pii_shaped_value(v: Any) -> bool:
    if v is None:
        return False
    if not isinstance(v, str):
        v = str(v)
    if _ID_LEAK.search(v):
        return True
    for p in _PHONE_LEAK:
        if p.search(v):
            return True
    return False


# ============================================================================
# Corpus file builder
# ============================================================================

def build_masked_corpus_file(rows: List[Dict[str, Any]],
                             out_path: Path,
                             sha256: bool = True) -> Dict[str, Any]:
    """Write `rows` as JSONL to `out_path`. Refuses any row that still
    carries PII-shaped values (post-mask leak-check). Returns a
    metadata dict `{path, sha256, row_count, bytes}`.
    """
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Leak-check pass — refuses BEFORE writing (belt-and-braces vs
    # row-executor which is the primary defence).
    for i, row in enumerate(rows):
        for col, v in row.items():
            if _has_pii_shaped_value(v):
                raise CorpusIntegrityRefusal(
                    f"row[{i}].{col} matches PII-shaped pattern after mask — "
                    f"row-executor scrub must have missed it. Refusing to "
                    f"write. Repro: {str(v)[:80]!r}"
                )
    # Deterministic write: sort keys in each row so sha256 is stable.
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    byte_count = p.stat().st_size
    hex_digest = ""
    if sha256:
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(64 * 1024), b""):
                h.update(chunk)
        hex_digest = h.hexdigest()
    return {
        "path": p,
        "sha256": hex_digest,
        "row_count": len(rows),
        "bytes": byte_count,
    }


# ============================================================================
# Transport + cleanup
# ============================================================================

def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def stage_corpus_to_host(corpus_meta: Dict[str, Any],
                         host_slug: str,
                         remote_dir: str,
                         ssh_seam: Any) -> Dict[str, Any]:
    """Copy the corpus file to `<host_slug>:<remote_dir>/<basename>`,
    then verify remote sha256 matches. Refuses on mismatch.

    `ssh_seam` is duck-typed: MUST expose `put_file(local_path, remote_path)`
    and `run(command) -> {"exit_code": int, "stdout": str}`. This shape
    lets tests inject a fake seam and lets production wire the real
    training_runner.ssh_seam behind an adapter without importing here.
    """
    local_path = Path(corpus_meta["path"])
    local_sha = corpus_meta["sha256"]
    remote_path = remote_dir.rstrip("/") + "/" + local_path.name
    # Ensure remote dir exists.
    ssh_seam.run(f"mkdir -p {remote_dir}")
    put_result = ssh_seam.put_file(str(local_path), remote_path)
    _ = put_result  # exit_code is on the seam's contract; not asserted here
    # Remote sha256 verification.
    r = ssh_seam.run(f"sha256sum {remote_path}")
    remote_stdout = r.get("stdout", "") if isinstance(r, dict) else ""
    remote_sha = remote_stdout.strip().split()[0] if remote_stdout.strip() else ""
    verified = (local_sha == remote_sha)
    receipt = {
        "at_utc": _iso_now(),
        "host_slug": host_slug,
        "remote_dir": remote_dir,
        "remote_path": remote_path,
        "local_sha256": local_sha,
        "remote_sha256": remote_sha,
        "bytes_transported": corpus_meta.get("bytes", 0),
        "row_count": corpus_meta.get("row_count", 0),
        "verified_match": verified,
    }
    if not verified:
        raise TransportIntegrityRefusal(
            f"sha256 mismatch after transport to {host_slug}:{remote_path}. "
            f"local={local_sha!r} remote={remote_sha!r}. "
            f"Receipt: {receipt}"
        )
    return receipt


def cleanup_remote_corpus(host_slug: str,
                           remote_dir: str,
                           ssh_seam: Any) -> Dict[str, Any]:
    """Remove the remote corpus dir. Returns a receipt with the exact
    cleanup_command and the exit_code from the remote."""
    # Optionally probe size before rm for the receipt.
    remote_bytes: Optional[int] = None
    try:
        du_r = ssh_seam.run(f"du -sb {remote_dir}")
        stdout = du_r.get("stdout", "") if isinstance(du_r, dict) else ""
        first_field = stdout.strip().split("\t", 1)[0] if stdout.strip() else ""
        if first_field.isdigit():
            remote_bytes = int(first_field)
    except Exception:
        remote_bytes = None
    cleanup_cmd = f"rm -rf {remote_dir}"
    r = ssh_seam.run(cleanup_cmd)
    exit_code = r.get("exit_code", -1) if isinstance(r, dict) else -1
    return {
        "at_utc": _iso_now(),
        "host_slug": host_slug,
        "remote_dir": remote_dir,
        "cleanup_command": cleanup_cmd,
        "exit_code": exit_code,
        "remote_bytes_removed_estimate": remote_bytes,
    }


# ============================================================================
# Governed LoRA run — the unstub target
# ============================================================================

def execute_governed_lora_run(
    tier: str,
    recipe_version: str,
    base_model_id: str,
    material_admit_ref: str,
    host_slug: str,
    table_context,   # str | list[str]  · list triggers multi-table path
    slice_size: int,
    backend_execute: Callable[[str, Dict[str, Any]], List[Dict[str, Any]]],
    ssh_seam: Any,
    corpus_variant: str = None,
) -> Dict[str, Any]:
    """End-to-end governed LoRA training run · UNSTUB + MULTI-TABLE (W-Multi-Table-Extract).

    Composition (see notes/wave_shield_train_run_grounding_brief.md §B
    and notes/wave_multi_table_extract_grounding_brief.md §C):
      1. Admission gate — chokepoint.masking_tier.validate_tier.
      2. Extract + compose training_text:
          - str table_context : single-table path via row_executor.
          - list table_context: multi-table path via multi_table.compose_multi_table_corpus.
      3. Deterministic 20% tail split (held_out.deterministic_20pct_tail_split).
      4. Bank held-out slice hash PREFLIGHT — before any staging.
      5. Build masked corpus files (train + held-out JSONL + sha256).
      6. Stage BOTH to host with sha256-verified transport.
      7. Return run handle dict (trainer invocation is a separate step
         handled by campaign_infra.production_trainer.default_trainer_fn).

    corpus_variant governs dedup for multi-table path:
      - 'raw' -> dedup=False (Campaign B2)
      - 'deduplicated' or None -> dedup=True (Campaign B-REF / B3 / B4 / B5 / B6)
      For single-table path, corpus_variant is metadata-only (dedup applied
      only in multi-table path since single-table composed_rows are already
      unique by masking-policy construction; dedup would only fire on the
      rare case of identical Q+A pairs, which is negligible for USSD).
    """
    # 1. Admission gate.
    from services.chokepoint import masking_tier as _mt
    env = os.environ.get("AKKI_ENV", "")
    try:
        _mt.validate_tier(tier, akki_env=env)
    except _mt.MaskingTierRefused as exc:
        raise MaskingTierNotAdmitted(
            f"masking tier {tier!r} not admissible under AKKI_ENV={env!r}. "
            f"Original refusal: {exc}. Admission is parked pending owner "
            f"ruling — see services/chokepoint/masking_tier_allowlist.v0.json "
            f"§tier {tier} prerequisites_status field."
        ) from exc

    from services.shield_train import row_executor as _rx
    from services.shield_train import held_out as _ho

    # 2. Extract + compose (dispatch on shape of table_context).
    principal = f"shield_train.execute_governed_lora_run::{host_slug}"
    purpose = f"lora_train.{recipe_version}.{material_admit_ref}"
    database = os.environ.get("AKKI_LORA_DATABASE", "digicow_live")

    is_multi = isinstance(table_context, (list, tuple))
    row_extraction_receipt_path = None
    per_table_extraction_receipts: List[str] = []
    dedup_flag = None

    if is_multi:
        # --- Multi-table path (W-Multi-Table-Extract) ---
        from services.shield_train import multi_table as _mtc
        dedup_flag = (corpus_variant != "raw")  # 'deduplicated' / None → True; 'raw' → False
        mt_result = _mtc.compose_multi_table_corpus(
            tables=list(table_context),
            database=database, principal=principal, purpose=purpose,
            backend_execute=backend_execute,
            slice_size_per_table=int(slice_size), dedup=dedup_flag,
        )
        composed = mt_result["composed_rows"]
        per_table_extraction_receipts = mt_result["per_table_extraction_receipts"]
    else:
        # --- Single-table path (existing behavior) ---
        ledger = _rx._ledger_for_table(table_context)
        if not ledger:
            raise _rx.UnclassifiedRefusal(
                f"table {table_context!r} has no ledger entries — "
                f"unclassified. Author classifications via "
                f"services.shield_train.authoring.add_entry(...)."
            )
        emit_cols = sorted([
            c for c, e in ledger.items()
            if e["action"] in ("include", "mask_regex_scrub")
        ])
        if not emit_cols:
            raise _rx.UnclassifiedRefusal(
                f"table {table_context!r} has no include/mask_regex_scrub "
                f"ledger entries — nothing to emit"
            )
        order_by = " ORDER BY id" if "id" in ledger else ""
        limit_clause = f" LIMIT {int(slice_size)}" if int(slice_size) > 0 else ""
        sql = f"SELECT {', '.join(emit_cols)} FROM {table_context}{order_by}{limit_clause}"
        extract = _rx.execute_row_bearing_query(
            sql=sql, params={}, database=database,
            table_context=table_context,
            principal=principal, purpose=purpose,
            backend_execute=backend_execute,
        )
        row_extraction_receipt_path = extract.receipt_path
        per_table_extraction_receipts = [extract.receipt_path]
        composed: List[Dict[str, Any]] = []
        for row in extract.rows:
            vc = str(row.get("value_chain", "") or "").strip()
            qs = str(row.get("question_string", "") or "").strip()
            opt = str(row.get("option_string", "") or "").strip()
            if not qs or not opt:
                continue
            composed.append({
                "training_text": f"[value_chain: {vc}]\nQ: {qs}\nA: {opt}",
                "value_chain": vc,
            })

    if not composed:
        raise CorpusIntegrityRefusal(
            f"no rows survived compose after governed extraction. "
            f"Table(s) {table_context!r} may lack the assumed schema."
        )

    # 3. Deterministic 20% tail split.
    train_rows, held_rows, split_meta = _ho.deterministic_20pct_tail_split(
        composed, seed=31337,
    )

    # 4. Compute run_id + bank held-out slice hash PREFLIGHT.
    run_id_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_ref = str(material_admit_ref).replace("/", "_").replace(":", "_")
    run_id = f"shield-train-{safe_ref}-{run_id_ts}"
    held_out_receipt_path = _ho.bank_held_out_slice_hash(
        run_id=run_id,
        table_context=(",".join(table_context) if is_multi else table_context),
        split_meta=split_meta,
    )

    # 5. Build masked corpus files (train + held-out JSONL + sha256).
    local_dir = Path(os.environ.get(
        "SHIELD_TRAIN_STAGE_LOCAL_DIR",
        "/app/assessment_workspace/phase0/shield_train_receipts/staged_corpora",
    )) / run_id
    local_dir.mkdir(parents=True, exist_ok=True)
    train_meta = build_masked_corpus_file(
        train_rows, local_dir / "train_corpus.jsonl", sha256=True,
    )
    held_meta = build_masked_corpus_file(
        held_rows, local_dir / "held_out_corpus.jsonl", sha256=True,
    )

    # 6. Stage both to host (sha256-verified transport).
    remote_dir = f"~/akki_journal/{run_id}"
    train_stage = stage_corpus_to_host(train_meta, host_slug, remote_dir, ssh_seam)
    held_stage = stage_corpus_to_host(held_meta, host_slug, remote_dir, ssh_seam)

    # 7. Return handle.
    return {
        "receipt_utc": _iso_now(),
        "run_id": run_id,
        "tier": tier,
        "env": env,
        "host_slug": host_slug,
        "table_context": table_context,   # str OR list preserved verbatim
        "corpus_variant": corpus_variant,
        "dedup": dedup_flag,
        "row_extraction_receipt_path": row_extraction_receipt_path,
        "per_table_extraction_receipts": per_table_extraction_receipts,
        "held_out_slice_receipt_path": held_out_receipt_path,
        "train_corpus": {
            "path": str(train_meta["path"]),
            "sha256": train_meta["sha256"],
            "row_count": train_meta["row_count"],
            "bytes": train_meta["bytes"],
        },
        "held_out_corpus": {
            "path": str(held_meta["path"]),
            "sha256": held_meta["sha256"],
            "row_count": held_meta["row_count"],
            "bytes": held_meta["bytes"],
        },
        "stage_receipts": [train_stage, held_stage],
        "remote_dir": remote_dir,
    }
