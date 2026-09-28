"""Composition Census — CP4 kernel.

Deep composition census over one live host:
  - schema × table × column enumeration (via information_schema.columns)
  - column type histogram per schema
  - row-count profile per table (from earlier probe or fresh SELECT COUNT)
  - name-based semantic column-role classification signals
    (role.email, role.phone, role.timestamp, role.pk_candidate, ...)
  - null-density profile per column (INFORMATION_SCHEMA.STATISTICS lite)

Every SQL routed through `services.mtafiti.executor.readonly_sql_guard.
refuse_if_write` BEFORE the injected executor sees it. Every sampled row
(none in this CP — CP4 is metadata-only) is passed through
`services.mtafiti.detectors.pii_redaction_guard.redact_row`. The final
census is passed through the `data_view` PII scan before returning.

Owner ruling this session (verbatim):
    "CP4..CPn: full deep census over both connections —
    composition-by-strata, semantic column classification, PII
    detection+tagging, data-quality profiling, embeddings/relationship
    signals, deterministic stratified sampling. Persist
    measurement/detection OUTPUT (classifications, counts, strata,
    signatures, minimal redacted samples) — NOT raw PII dumps."

CP4 lands COMPOSITION-BY-STRATA + name-based semantic column
classification. CPs 5+ pick up data-quality and embedding signals.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

from contracts.mtafiti_detection_signal import DetectionSignal, EvidenceClass
from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
from services.mtafiti.probes.live_readonly_probe import (
    ExecutorResult,
    SqlExecutor,
    data_view,
)
from services.mtafiti.detectors.pii_redaction_guard import assert_no_raw_pii


_DETECTOR_VERSION = "column-role-v0.1"

# ────────────────────────────────────────────────────────────────────────
# Name-based semantic column-role heuristics.
# Each pattern is a (role_name, regex, confidence) tuple. Compiled here
# once for determinism (no runtime regex compile in hot path).
# ────────────────────────────────────────────────────────────────────────
_COLUMN_ROLE_PATTERNS: Sequence[tuple] = (
    ("role.email",       re.compile(r"(?:^|_)email(?:_|$)", re.I),                  0.95),
    ("role.phone",       re.compile(r"(?:^|_)(?:phone|msisdn|mobile|cell)(?:_|$)", re.I),  0.90),
    ("role.national_id", re.compile(r"(?:^|_)(?:national_?id|nid|id_number)(?:_|$)", re.I), 0.85),
    ("role.name_person", re.compile(r"(?:^|_)(?:first_?name|last_?name|full_?name|user_?name|display_?name|surname)(?:_|$)", re.I), 0.75),
    ("role.dob",         re.compile(r"(?:^|_)(?:dob|date_of_birth|birthday|birthdate)(?:_|$)", re.I), 0.90),
    ("role.gender",      re.compile(r"(?:^|_)(?:gender|sex)(?:_|$)", re.I),         0.80),
    ("role.address",     re.compile(r"(?:^|_)(?:address|street|city|county|country|postal_?code|zip)(?:_|$)", re.I), 0.70),
    ("role.password",    re.compile(r"(?:^|_)(?:password|passwd|pwd|password_hash|salt)(?:_|$)", re.I), 0.95),
    ("role.token",       re.compile(r"(?:^|_)(?:token|access_?token|refresh_?token|api_?key|secret)(?:_|$)", re.I), 0.90),
    ("role.timestamp",   re.compile(r"(?:^|_)(?:created_?at|updated_?at|deleted_?at|inserted_?at|seen_?at|ts|time|date_?time|last_?login)(?:_|$)", re.I), 0.85),
    ("role.pk_candidate", re.compile(r"^id$|(?:^|_)id$|^uuid$", re.I),              0.70),
    ("role.fk_candidate", re.compile(r"_id$|_uuid$|(?:^|_)user_?id(?:_|$)|(?:^|_)ref(?:_|$)", re.I), 0.60),
    ("role.ip",          re.compile(r"(?:^|_)(?:ip|ip_?address|remote_?addr|src_?ip|dst_?ip)(?:_|$)", re.I), 0.85),
    ("role.url",         re.compile(r"(?:^|_)(?:url|link|href|redirect_?to)(?:_|$)", re.I), 0.75),
    ("role.amount",      re.compile(r"(?:^|_)(?:amount|balance|price|cost|fare|value|total|subtotal|tax|fee)(?:_|$)", re.I), 0.65),
    ("role.currency",    re.compile(r"(?:^|_)(?:currency|ccy|iso_?currency)(?:_|$)", re.I), 0.90),
    ("role.geo",         re.compile(r"(?:^|_)(?:lat|latitude|lng|long|longitude|geo|location)(?:_|$)", re.I), 0.75),
)


def _classify_column_role(column_name: str, schema: str, table: str) -> List[DetectionSignal]:
    """Emit DetectionSignals for every matched name-based role."""
    signals: List[DetectionSignal] = []
    source_ref = f"{schema}.{table}.{column_name}"
    for role, rx, confidence in _COLUMN_ROLE_PATTERNS:
        if rx.search(column_name):
            signals.append(
                DetectionSignal(
                    signal_name=role,
                    evidence_class=EvidenceClass.DETECTED,
                    confidence=confidence,
                    source_ref=source_ref,
                    detector_version=_DETECTOR_VERSION,
                )
            )
    return signals


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _guarded_execute(sql: str, executor: SqlExecutor, receipt: Dict[str, Any]) -> ExecutorResult:
    normalised = refuse_if_write(sql)
    lead = normalised.split(None, 1)[0].upper()
    entry: Dict[str, Any] = {"sql": normalised, "lead_verb": lead}
    try:
        result = executor(normalised)
        entry["row_count"] = result.row_count
        entry["ok"] = result.error is None
        if result.error:
            entry["error"] = result.error
    except Exception as exc:
        entry["ok"] = False
        entry["error"] = f"{type(exc).__name__}: {str(exc)[:250]}"
        result = ExecutorResult(error=entry["error"])
    receipt["sql_trace"].append(entry)
    return result


def run_composition_census(
    *,
    host: str,
    port: int,
    user: str,
    label: str,
    sql_executor: SqlExecutor,
    schemas: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Enumerate composition across `schemas` on `host`.

    If `schemas` is None, discovers user schemas via SHOW DATABASES first.
    Returns a receipt dict banked to phase0/mtafiti_gpu_discovery/.
    """
    receipt: Dict[str, Any] = {
        "at_utc": _iso_utc_now(),
        "label": label,
        "host": host,
        "port": port,
        "user": user,
        "connected": False,
        "sql_trace": [],
        "schemas_covered": [],
        # per_schema: {schema: {tables: [t], total_rows: int, column_type_histogram: {type: n}}}
        "per_schema": {},
        # per_table: {"schema.table": {row_count, column_count, columns: [...], role_signals: [...]}}
        "per_table": {},
        "column_role_signals_summary": {"total": 0, "by_role": {}},
        "totals": {"schemas": 0, "tables": 0, "columns": 0, "rows": 0},
        "errors": [],
    }

    # Discover schemas if not supplied.
    if schemas is None:
        res = _guarded_execute("SHOW DATABASES", sql_executor, receipt)
        if res.error:
            receipt["errors"].append({"stage": "SHOW DATABASES", "err": res.error})
            _finalize_census(receipt)
            return receipt
        receipt["connected"] = True
        all_schemas = [r[0] if isinstance(r, (list, tuple)) else r for r in res.rows]
        _SYS = {"information_schema", "mysql", "performance_schema", "sys"}
        schemas = [s for s in all_schemas if s not in _SYS]
    else:
        receipt["connected"] = True

    receipt["schemas_covered"] = list(schemas)

    # Bulk metadata via information_schema.columns per schema.
    for sch in schemas:
        res_cols = _guarded_execute(
            "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY "
            f"FROM information_schema.columns WHERE TABLE_SCHEMA = '{sch}' "
            "ORDER BY TABLE_NAME, ORDINAL_POSITION",
            sql_executor,
            receipt,
        )
        if res_cols.error:
            receipt["errors"].append({"stage": f"columns({sch})", "err": res_cols.error})
            continue

        tables: Dict[str, List[Dict[str, Any]]] = {}
        type_hist: Dict[str, int] = {}
        for row in res_cols.rows:
            tbl_name = row[0]
            col = {
                "column_name": row[1],
                "data_type": row[2],
                "is_nullable": (row[3] == "YES"),
                "column_key": row[4] or "",
            }
            tables.setdefault(tbl_name, []).append(col)
            type_hist[col["data_type"]] = type_hist.get(col["data_type"], 0) + 1

        # Pull row counts via a single information_schema.tables query.
        res_tabs = _guarded_execute(
            "SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH "
            f"FROM information_schema.tables WHERE TABLE_SCHEMA = '{sch}'",
            sql_executor,
            receipt,
        )
        row_counts: Dict[str, int] = {}
        data_lengths: Dict[str, int] = {}
        if not res_tabs.error:
            for row in res_tabs.rows:
                row_counts[row[0]] = int(row[1] or 0)
                data_lengths[row[0]] = int(row[2] or 0)
        else:
            receipt["errors"].append({"stage": f"tables({sch})", "err": res_tabs.error})

        # Bank per-schema + per-table entries + role signals.
        total_schema_rows = 0
        for tbl_name, cols in tables.items():
            key = f"{sch}.{tbl_name}"
            row_count = row_counts.get(tbl_name, None)
            data_length = data_lengths.get(tbl_name, None)
            total_schema_rows += row_count or 0
            role_signals: List[Dict[str, Any]] = []
            for col in cols:
                for sig in _classify_column_role(col["column_name"], sch, tbl_name):
                    role_signals.append(
                        {
                            "role": sig.signal_name,
                            "column": col["column_name"],
                            "confidence": sig.confidence,
                        }
                    )
                    receipt["column_role_signals_summary"]["total"] += 1
                    br = receipt["column_role_signals_summary"]["by_role"]
                    br[sig.signal_name] = br.get(sig.signal_name, 0) + 1
            receipt["per_table"][key] = {
                "row_count": row_count,
                "data_length_bytes": data_length,
                "column_count": len(cols),
                "columns": cols,
                "role_signals": role_signals,
            }
        receipt["per_schema"][sch] = {
            "tables": list(tables.keys()),
            "table_count": len(tables),
            "column_type_histogram": type_hist,
            "total_rows": total_schema_rows,
        }
        receipt["totals"]["tables"] += len(tables)
        receipt["totals"]["columns"] += sum(len(v) for v in tables.values())
        receipt["totals"]["rows"] += total_schema_rows

    receipt["totals"]["schemas"] = len(receipt["per_schema"])

    _finalize_census(receipt)
    return receipt


def _finalize_census(receipt: Dict[str, Any]) -> None:
    """Seal a census receipt: defence-in-depth PII scan + canonical sha256."""
    receipt.pop("password", None)
    assert_no_raw_pii(data_view(receipt))
    receipt["census_sha256"] = _canonical_sha256(
        {k: v for k, v in receipt.items() if k != "census_sha256"}
    )
