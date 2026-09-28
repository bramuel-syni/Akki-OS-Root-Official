"""shield_train.multi_table — sequential per-table extract + composed corpus.

Owner ruling verbatim (2026-09-06T~14:XXZ, via user proxy):
    "multi-table extraction in row_executor (UNION or sequential per-table
     extract + composed corpus — pick the design that keeps the
     refuse-unclassified-by-construction property per table)."

Design chosen: sequential per-table extract. Each table's extraction
goes through `row_executor.execute_row_bearing_query` unchanged — so
every existing HARD GATE (admission, ledger completeness, PII regex
belt-and-braces) fires PER TABLE. The multi-table composition layer
lives at the pipeline level; it never bypasses the per-table gates.

Per-table training_text formatters:
  - `ussd_question_response`: matches the single-table pipeline path
    verbatim ([value_chain]\\nQ:\\nA:).
  - `sms_log`: [sms_topic: title]\\nbody.

Deduplication (when enabled): first-occurrence-wins by sha256 of
`training_text`, preserving overall order (USSD rows first, then SMS
rows in ORDER-BY-id order per table). This keeps the deterministic
20 % tail split reproducible.
"""
from __future__ import annotations

import hashlib
from typing import Any, Callable, Dict, List, Tuple


def _compose_training_text_ussd(row: Dict[str, Any]) -> str:
    """USSD training_text (matches single-table pipeline format verbatim)."""
    vc = str(row.get("value_chain", "") or "").strip()
    qs = str(row.get("question_string", "") or "").strip()
    opt = str(row.get("option_string", "") or "").strip()
    return f"[value_chain: {vc}]\nQ: {qs}\nA: {opt}"


def _compose_training_text_sms(row: Dict[str, Any]) -> str:
    """SMS training_text.

    Ruling #5(a) (2026-09-06T~15:XXZ, owner via user proxy) resolves
    the drawer entry for `sms_log.sms_sent`: INCLUDE message bodies
    with `mask_regex_scrub`. Post-resolution `sms_sent` is the
    required emit field (body carries the DigiCow→farmer directive
    content); `sms_title` is an opportunistic topic prefix.

    Row survival:
      - body present, title present → `[sms_topic: TITLE]\\nBODY`
      - body present, title empty   → `[sms_topic: ]\\nBODY`  (body-only)
      - body empty                  → row dropped upstream by
        required_fields=(sms_sent,) in _TABLE_FORMATTERS.
    """
    title = str(row.get("sms_title", "") or "").strip()
    body = str(row.get("sms_sent", "") or "").strip()
    return f"[sms_topic: {title}]\n{body}"


# Table -> (composer, required-non-empty-fields for row survival).
_TABLE_FORMATTERS: Dict[str, Tuple[Callable, Tuple[str, ...]]] = {
    "ussd_question_response": (
        _compose_training_text_ussd,
        ("question_string", "option_string"),
    ),
    "sms_log": (
        _compose_training_text_sms,
        # Post-Ruling-#5(a) (W-SMS-Body-Emit): sms_sent is the required
        # emit field for row survival. Rows with empty body drop upstream.
        # sms_title remains an opportunistic topic prefix (not required).
        ("sms_sent",),
    ),
}


def _emit_columns_for_table(table: str) -> List[str]:
    """Which columns to SELECT for `table` from masking policy ledger
    (action ∈ {include, mask_regex_scrub}). Row_executor further
    enforces refuse-unclassified — this list feeds SELECT construction."""
    from services.shield_train.row_executor import _ledger_for_table
    ledger = _ledger_for_table(table)
    if not ledger:
        return []  # row_executor will UnclassifiedRefusal downstream
    return sorted([
        c for c, e in ledger.items()
        if e.get("action") in ("include", "mask_regex_scrub")
    ])


def compose_multi_table_corpus(
    tables: List[str],
    database: str,
    principal: str,
    purpose: str,
    backend_execute: Callable[[str, Dict[str, Any]], List[Dict[str, Any]]],
    slice_size_per_table: int,
    dedup: bool = True,
) -> Dict[str, Any]:
    """Extract rows from each table in `tables` via the governed
    row_executor, compose training_text per table shape, concatenate
    in table order, optionally deduplicate by training_text sha256.

    Returns:
      {
        "tables": [...],
        "dedup": bool,
        "total_row_count": int,
        "per_table_row_counts": {table: n, ...},
        "per_table_extraction_receipts": [receipt_path, ...],
        "composed_rows": [{"training_text": ..., "source_table": ...}, ...],
      }

    Refuses per-table (via row_executor) if ANY table is unclassified,
    has no emit columns, or has an unclassified column in the emit set.
    """
    from services.shield_train import row_executor as _rx

    per_table_receipts: List[str] = []
    per_table_counts: Dict[str, int] = {}
    composed: List[Dict[str, Any]] = []

    for table in tables:
        if table not in _TABLE_FORMATTERS:
            raise _rx.UnclassifiedRefusal(
                f"table {table!r} has no pipeline training_text formatter — "
                f"multi_table composition supports "
                f"{sorted(_TABLE_FORMATTERS)!r} for now. Adding new tables "
                f"requires an authored formatter + policy classification."
            )
        formatter, required_fields = _TABLE_FORMATTERS[table]
        emit_cols = _emit_columns_for_table(table)
        if not emit_cols:
            raise _rx.UnclassifiedRefusal(
                f"table {table!r} has no include/mask_regex_scrub ledger "
                f"entries — nothing to emit. Classify columns in "
                f"masking_policy.v0.json before this table can extract."
            )
        # ORDER BY id when the table has an id column (deterministic tail split).
        order_by = " ORDER BY id" if "id" in _rx._ledger_for_table(table) else ""
        limit_clause = f" LIMIT {int(slice_size_per_table)}" \
                       if int(slice_size_per_table) > 0 else ""
        sql = (
            f"SELECT {', '.join(emit_cols)} FROM {table}"
            f"{order_by}{limit_clause}"
        )
        # Governed extraction per-table — row_executor emits its own receipt
        # + fires refuse-unclassified-by-construction on this exact SELECT.
        extract = _rx.execute_row_bearing_query(
            sql=sql, params={}, database=database, table_context=table,
            principal=principal, purpose=f"{purpose}::table={table}",
            backend_execute=backend_execute,
        )
        per_table_receipts.append(extract.receipt_path)

        # Compose training_text for surviving rows.
        survived = 0
        for row in extract.rows:
            missing_required = any(
                not str(row.get(f, "") or "").strip() for f in required_fields
            )
            if missing_required:
                continue
            training_text = formatter(row)
            composed.append({
                "training_text": training_text,
                "source_table": table,
            })
            survived += 1
        per_table_counts[table] = survived

    # Deduplicate by training_text sha256 (first-occurrence-wins).
    if dedup:
        seen: set = set()
        deduped: List[Dict[str, Any]] = []
        for row in composed:
            h = hashlib.sha256(row["training_text"].encode("utf-8")).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            deduped.append(row)
        composed = deduped

    return {
        "tables": list(tables),
        "dedup": bool(dedup),
        "total_row_count": len(composed),
        "per_table_row_counts": per_table_counts,
        "per_table_extraction_receipts": per_table_receipts,
        "composed_rows": composed,
    }
