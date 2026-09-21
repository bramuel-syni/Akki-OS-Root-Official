"""Live Read-Only Probe — CP3 kernel.

Owner authorisation this session:

    "CP3: first LIVE read-only dry-run against Weego (159.138.162.146)
    and USSD (110.238.76.159) — SELECT/SHOW only, zero writes. Prove
    the executor + detectors work on real data before scaling."

Design (thin-kernel, injection-friendly):
  - `run_live_probe(host, port, user, password, database, ...,
                    sql_executor=None, redact_fn=None, detect_fn=None)`
    returns a receipt dict. Every SQL is routed through
    `services.mtafiti.executor.readonly_sql_guard.refuse_if_write` BEFORE
    the executor sees it. Every sampled row is passed through
    `services.mtafiti.detectors.pii_redaction_guard.redact_row` BEFORE
    it enters the receipt. The final receipt is passed through
    `assert_no_raw_pii` BEFORE it is returned.
  - `sql_executor(sql: str) -> ExecutorResult` is injectable so the
    invariant tests can prove the guard is invoked without touching
    a real MySQL server. Real callers pass in a pymysql-backed executor.
  - The receipt schema is stable and content-addressed by receipt sha256.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

from services.mtafiti.detectors.pii_detector import detect_pii
from services.mtafiti.detectors.pii_redaction_guard import (
    assert_no_raw_pii,
    redact_row,
)
from services.mtafiti.executor.readonly_sql_guard import refuse_if_write


@dataclass
class ExecutorResult:
    """Structured result of a single SQL execution."""

    columns: List[str] = field(default_factory=list)
    rows: List[Sequence[Any]] = field(default_factory=list)
    row_count: Optional[int] = None
    error: Optional[str] = None


SqlExecutor = Callable[[str], ExecutorResult]


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _guarded_execute(
    sql: str, executor: SqlExecutor, receipt: Dict[str, Any]
) -> ExecutorResult:
    """Run `sql` after passing it through the read-only guard. Bank the
    SQL + lead verb into the receipt regardless of executor outcome."""
    normalised = refuse_if_write(sql)  # raises WriteVerbRefused on any write
    lead = normalised.split(None, 1)[0].upper()
    entry: Dict[str, Any] = {"sql": normalised, "lead_verb": lead}
    try:
        result = executor(normalised)
        entry["row_count"] = result.row_count
        entry["columns"] = list(result.columns)
        if result.error:
            entry["error"] = result.error
        entry["ok"] = result.error is None
    except Exception as exc:
        entry["ok"] = False
        entry["error"] = f"{type(exc).__name__}: {str(exc)[:250]}"
        result = ExecutorResult(error=entry["error"])
    receipt["sql_trace"].append(entry)
    return result


def run_live_probe(
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    database: Optional[str] = None,
    label: str = "run",
    sql_executor: SqlExecutor,
    schema_probe_limit: int = 3,
    table_probe_limit: int = 3,
    sample_rows: int = 5,
) -> Dict[str, Any]:
    """Run a read-only dry-run probe against a live MySQL host and return
    a receipt dict.

    The probe enumerates schemas (SHOW DATABASES), then tables
    (SHOW TABLES) for a bounded number of schemas, then row-counts and a
    tiny redacted sample per table. Every SQL is guarded; every sampled
    row is redacted before landing in the receipt.
    """
    receipt: Dict[str, Any] = {
        "at_utc": _iso_utc_now(),
        "label": label,
        "host": host,
        "port": port,
        "user": user,
        # password is DELIBERATELY never in the receipt
        "database": database,
        "probe_limits": {
            "schema_probe_limit": schema_probe_limit,
            "table_probe_limit": table_probe_limit,
            "sample_rows": sample_rows,
        },
        "sql_trace": [],
        "schemas": [],
        "tables": {},  # schema -> [table_names]
        "row_counts": {},  # "schema.table" -> int
        "samples": {},  # "schema.table" -> {columns, rows_redacted, pii_signals}
        "detector_signals_summary": {"total": 0, "by_kind": {}},
        "connected": False,
        "errors": [],
    }

    # ── SHOW DATABASES ───────────────────────────────────────────────
    res = _guarded_execute("SHOW DATABASES", sql_executor, receipt)
    if res.error:
        receipt["errors"].append({"stage": "SHOW DATABASES", "err": res.error})
        _finalize_receipt(receipt)
        return receipt

    receipt["connected"] = True
    all_schemas = [
        r[0] if isinstance(r, (list, tuple)) else r for r in res.rows
    ]
    # Skip MySQL system schemas
    _SYSTEM = {"information_schema", "mysql", "performance_schema", "sys"}
    user_schemas = [s for s in all_schemas if s not in _SYSTEM]
    receipt["schemas"] = list(all_schemas)
    receipt["schemas_user"] = user_schemas

    # ── SHOW TABLES per bounded schema ──────────────────────────────
    probed_schemas = user_schemas[:schema_probe_limit]
    for sch in probed_schemas:
        res = _guarded_execute(f"USE `{sch}`", sql_executor, receipt)
        if res.error:
            receipt["errors"].append({"stage": f"USE {sch}", "err": res.error})
            continue
        res = _guarded_execute("SHOW TABLES", sql_executor, receipt)
        if res.error:
            receipt["errors"].append({"stage": f"SHOW TABLES ({sch})", "err": res.error})
            continue
        tables = [r[0] if isinstance(r, (list, tuple)) else r for r in res.rows]
        receipt["tables"][sch] = list(tables)

        # ── SELECT COUNT + SELECT sample per bounded table ──────────
        for tb in tables[:table_probe_limit]:
            key = f"{sch}.{tb}"
            res_cnt = _guarded_execute(
                f"SELECT COUNT(*) FROM `{sch}`.`{tb}`",
                sql_executor,
                receipt,
            )
            if res_cnt.error:
                receipt["errors"].append({"stage": f"COUNT {key}", "err": res_cnt.error})
                continue
            n = None
            if res_cnt.rows and isinstance(res_cnt.rows[0], (list, tuple)):
                n = res_cnt.rows[0][0]
            receipt["row_counts"][key] = int(n) if n is not None else None

            res_smp = _guarded_execute(
                f"SELECT * FROM `{sch}`.`{tb}` LIMIT {int(sample_rows)}",
                sql_executor,
                receipt,
            )
            if res_smp.error:
                receipt["errors"].append({"stage": f"SAMPLE {key}", "err": res_smp.error})
                continue
            cols = list(res_smp.columns)
            rows_redacted: List[Dict[str, Any]] = []
            pii_signals_for_table: List[Dict[str, Any]] = []
            for row in res_smp.rows:
                row_dict = {cols[i]: row[i] for i in range(len(cols))} if cols else {}
                # PII detection BEFORE redaction so we bank signal summary
                for sig in detect_pii(row_dict):
                    kind = sig.signal_name
                    receipt["detector_signals_summary"]["total"] += 1
                    receipt["detector_signals_summary"]["by_kind"][kind] = (
                        receipt["detector_signals_summary"]["by_kind"].get(kind, 0) + 1
                    )
                    pii_signals_for_table.append(
                        {"kind": kind, "field": sig.source_ref, "confidence": sig.confidence}
                    )
                rows_redacted.append(redact_row(row_dict))
            receipt["samples"][key] = {
                "columns": cols,
                "rows_redacted": rows_redacted,
                "pii_signals": pii_signals_for_table,
            }

    _finalize_receipt(receipt)
    return receipt


def _finalize_receipt(receipt: Dict[str, Any]) -> None:
    """Seal a receipt with a canonical sha256 + defence-in-depth PII scan.

    The PII scan runs over a DATA-VIEW of the receipt — infrastructure
    metadata (host, port, user, database, hosts, label, at_utc,
    receipt_sha256, probe_limits, connected, errors) is stripped from the
    view before scanning, because these fields legitimately carry host
    IPs / user names / config strings that would otherwise false-fire the
    IPv4 / URL patterns. Data-bearing fields (samples, sql_trace, schemas,
    tables, row_counts, detector_signals_summary, etc.) are ALL scanned.
    """
    # Strip the password field before hashing / scanning (defence in depth —
    # the probe never puts it there, but future edits shouldn't be able to leak).
    receipt.pop("password", None)
    # Defence in depth: scan the DATA-VIEW of the receipt for any raw PII
    # that slipped past the redactor. Raises RawPiiLeakForbidden.
    assert_no_raw_pii(data_view(receipt))
    # Bank a canonical sha256 (excluding itself).
    receipt["receipt_sha256"] = _canonical_sha256(
        {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    )


# ────────────────────────────────────────────────────────────────────────
# Metadata keys — recursively stripped from receipt before PII scan.
# Public so the invariant tests can scan the same view the writer did.
# ────────────────────────────────────────────────────────────────────────
METADATA_KEYS: frozenset = frozenset({
    "host",
    "port",
    "hosts",
    "user",
    "database",
    "label",
    "at_utc",
    "receipt_sha256",
    "census_sha256",
    "profile_sha256",
    "manifest_sha256",
    "inputs_sha256",
    "sample_bundle_sha256",
    "cost_receipt_sha256",
    "wave_close_sha256",
    "receipt_chain_sha256",
    "probe_limits",
    "connected",
    "errors",
    "credential_reuse_note",
})


def data_view(receipt: Any) -> Any:
    """Return a recursive copy of `receipt` with METADATA_KEYS stripped.

    Preserves list ordering and nested dict shapes. Non-dict / non-list
    scalars pass through unchanged.
    """
    if isinstance(receipt, dict):
        return {k: data_view(v) for k, v in receipt.items() if k not in METADATA_KEYS}
    if isinstance(receipt, list):
        return [data_view(v) for v in receipt]
    return receipt
