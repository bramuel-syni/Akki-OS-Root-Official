"""shield_train.row_executor — governed row-bearing SQL executor.

Refuses unclassified columns by construction. Applies per-column
masking per `masking_policy.v0.json`. Emits shape-only receipts.
Backend is INJECTED so this executor is testable against fixtures
with no live estate connection.
"""
from __future__ import annotations

import dataclasses
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# Exceptions
# ============================================================================

class UnclassifiedRefusal(ValueError):
    """Raised when the query touches a table or column that the masking
    policy does not classify. Cautious-default — the executor doesn't
    guess."""


class PolicyRefusal(ValueError):
    """Raised when the query touches a column that the masking policy
    classifies as `pii` + `exclude` (or any `exclude`-action column).
    The executor never emits excluded columns."""


class SqlShapeRefusal(ValueError):
    """Raised when the SQL isn't a single-table SELECT the executor can
    reason about. This wave supports single-table SELECT only; joins
    are r2."""


# ============================================================================
# Result shape
# ============================================================================

@dataclasses.dataclass
class RowBearingResult:
    rows: List[Dict[str, Any]]
    columns_included: List[str]
    columns_excluded: List[str]
    masking_steps_applied: List[Dict[str, str]]
    row_count: int
    receipt_utc: str
    principal: str
    purpose: str
    table_context: str
    database: str
    receipt_path: Optional[str] = None


# ============================================================================
# Policy loading (cached)
# ============================================================================

_POLICY_PATH = Path(__file__).resolve().parent / "masking_policy.v0.json"


def _load_policy() -> Dict[str, Any]:
    return json.loads(_POLICY_PATH.read_text(encoding="utf-8"))


def _ledger_for_table(table: str) -> Dict[str, Dict[str, Any]]:
    policy = _load_policy()
    out: Dict[str, Dict[str, Any]] = {}
    for e in policy.get("ledger", []):
        if e.get("table") == table:
            out[e["column"]] = e
    return out


# ============================================================================
# SQL column extraction
# ============================================================================

_SELECT_COLS_RE = re.compile(
    r"^\s*SELECT\s+(?P<cols>.+?)\s+FROM\s+", re.IGNORECASE | re.DOTALL
)
_STAR_RE = re.compile(r"\*")


def _extract_selected_columns(sql: str) -> List[str]:
    """Extract the SELECT column list from a single-table SELECT.

    Handles: `SELECT c1, c2, c3 FROM tbl ...`. Rejects `SELECT *`
    (cautious-default: `*` would include unclassified columns) and
    aliased-expression forms (`SELECT c1 AS x FROM tbl`) — this wave
    only supports bare column names.
    """
    m = _SELECT_COLS_RE.search(sql)
    if m is None:
        raise SqlShapeRefusal(
            "SQL is not a SELECT ... FROM ... shape the executor can parse"
        )
    cols_expr = m.group("cols").strip()
    if _STAR_RE.search(cols_expr):
        raise SqlShapeRefusal(
            "SELECT * is refused — the executor cannot classification-check "
            "an unbounded column list. Enumerate the columns explicitly."
        )
    parts = [c.strip() for c in cols_expr.split(",")]
    out: List[str] = []
    for p in parts:
        if " " in p or "(" in p:
            raise SqlShapeRefusal(
                f"aliased or expression columns are refused this wave: {p!r}"
            )
        out.append(p)
    return out


# ============================================================================
# Regex scrub (lifted from tools/text_train_pipeline/mask.py)
# ============================================================================

_PHONE_PATTERNS = [
    re.compile(r"\+?254[\s\-]*[17](?:[\s\-]*\d){8,9}"),
    re.compile(r"(?<!\d)0[\s\-]*[17](?:[\s\-]*\d){8,9}"),
]
_ID_PATTERN = re.compile(r"(?<![\d\w])\d{7,10}(?![\d\w])")


def _mask_free_text(s: Any) -> str:
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    out = s
    for p in _PHONE_PATTERNS:
        out = p.sub("[PHONE]", out)
    out = _ID_PATTERN.sub("[ID]", out)
    return out


# ============================================================================
# Receipt writer (shape-only)
# ============================================================================

def _receipt_dir() -> Path:
    p = Path(os.environ.get(
        "SHIELD_TRAIN_RECEIPTS_DIR",
        "/app/assessment_workspace/phase0/shield_train_receipts",
    ))
    p.mkdir(parents=True, exist_ok=True)
    return p


def _emit_receipt(receipt: Dict[str, Any]) -> Path:
    d = _receipt_dir()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = d / f"shield_train_row_receipt_{ts}_{uuid.uuid4().hex[:8]}.json"
    p.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    return p


# ============================================================================
# Public entry point
# ============================================================================

def execute_row_bearing_query(
    sql: str,
    params: Dict[str, Any],
    database: str,
    table_context: str,
    principal: str,
    purpose: str,
    backend_execute: Callable[[str, Dict[str, Any]], List[Dict[str, Any]]],
) -> RowBearingResult:
    """Governed row-bearing query executor.

    Discipline (in order — refusals are cheap, execution is last):
      1. Table MUST be classified (has ledger entries) — else UnclassifiedRefusal.
      2. Every selected column MUST be in the ledger for this table —
         else UnclassifiedRefusal.
      3. NO selected column may have action='exclude' — else PolicyRefusal.
      4. Only then does `backend_execute(sql, params)` fire.
      5. Every returned row is filtered to include only ledger-included
         columns; `mask_regex_scrub` columns get free-text scrubbed.
      6. A shape-only receipt is written to $SHIELD_TRAIN_RECEIPTS_DIR
         even on failure (so backend outages are auditable).
    """
    at_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Step 1: table classified?
    ledger = _ledger_for_table(table_context)
    if not ledger:
        raise UnclassifiedRefusal(
            f"table {table_context!r} has no ledger entries — "
            f"unclassified. Author classifications for this table via "
            f"services.shield_train.authoring.add_entry(...) before "
            f"queries can run against it."
        )

    # Step 2: every selected column in the ledger?
    selected = _extract_selected_columns(sql)
    unknown = [c for c in selected if c not in ledger]
    if unknown:
        raise UnclassifiedRefusal(
            f"unclassified columns in SELECT: {unknown}. Every column MUST "
            f"be classified in masking_policy.v0.json before the executor "
            f"will emit its content."
        )

    # Step 3: no excluded columns selected?
    banned = [c for c in selected if ledger[c]["action"] == "exclude"]
    if banned:
        raise PolicyRefusal(
            f"selected columns are policy-excluded: {banned}. Their "
            f"classifications are: "
            f"{[(c, ledger[c]['class']) for c in banned]}. The executor "
            f"NEVER emits exclude-action columns even when the caller "
            f"explicitly asks for them."
        )

    # Compose masking_steps_applied for the whole table's ledger (not just
    # selected) — receipt needs full picture.
    masking_steps = [
        {"column": col, "action": ledger[col]["action"]}
        for col in sorted(ledger.keys())
    ]
    columns_included = [c for c in selected]
    columns_excluded = [
        col for col, e in ledger.items()
        if e["action"] == "exclude"
    ]

    # Step 4: backend call, with belt-and-braces failure receipt.
    try:
        raw_rows = backend_execute(sql, params)
    except Exception as exc:
        _emit_receipt({
            "at_utc": at_utc,
            "database": database,
            "table_context": table_context,
            "principal": principal,
            "purpose": purpose,
            "row_count": 0,
            "columns_included": columns_included,
            "columns_excluded": columns_excluded,
            "masking_steps_applied": masking_steps,
            "error_class": type(exc).__name__,
            "error_message": str(exc)[:500],
        })
        raise

    # Step 5: mask + filter rows.
    scrub_cols = {
        col for col in selected
        if ledger[col]["action"] == "mask_regex_scrub"
    }
    include_cols = {
        col for col in selected
        if ledger[col]["action"] == "include"
    }
    keep_cols = scrub_cols | include_cols
    filtered_rows: List[Dict[str, Any]] = []
    for row in raw_rows:
        new_row: Dict[str, Any] = {}
        for col in selected:
            if col not in keep_cols:
                continue
            v = row.get(col)
            if col in scrub_cols:
                new_row[col] = _mask_free_text(v)
            else:
                new_row[col] = v
        filtered_rows.append(new_row)

    # Step 6: receipt.
    receipt = {
        "at_utc": at_utc,
        "database": database,
        "table_context": table_context,
        "principal": principal,
        "purpose": purpose,
        "row_count": len(filtered_rows),
        "columns_included": columns_included,
        "columns_excluded": columns_excluded,
        "masking_steps_applied": masking_steps,
    }
    receipt_path = _emit_receipt(receipt)

    return RowBearingResult(
        rows=filtered_rows,
        columns_included=columns_included,
        columns_excluded=columns_excluded,
        masking_steps_applied=masking_steps,
        row_count=len(filtered_rows),
        receipt_utc=at_utc,
        principal=principal,
        purpose=purpose,
        table_context=table_context,
        database=database,
        receipt_path=str(receipt_path),
    )
