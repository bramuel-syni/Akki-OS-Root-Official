"""Deterministic Stratified Sampler — CP6 kernel.

Owner authorisation this session:
    "CP4..CPn: full deep census over both connections — …
    deterministic stratified sampling. Persist measurement/detection
    OUTPUT (classifications, counts, strata, signatures, minimal
    redacted samples) — NOT raw PII dumps."

CP6 uses the CP1 `deterministic_adaptive_walker` to select a bounded
number of tables per schema (stratum = schema), pulls a small redacted
row sample from each, and lands the redacted samples + PII detector
signals to a receipt. Every SQL guarded; every sample redacted.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from services.mtafiti.detectors.pii_detector import detect_pii
from services.mtafiti.detectors.pii_redaction_guard import (
    assert_no_raw_pii,
    redact_row,
)
from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
from services.mtafiti.probes.live_readonly_probe import (
    ExecutorResult,
    SqlExecutor,
    data_view,
)
from services.mtafiti.sampling.deterministic_adaptive_walker import deterministic_walk


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def _guarded(sql: str, executor: SqlExecutor, receipt: Dict[str, Any]) -> ExecutorResult:
    normalised = refuse_if_write(sql)
    lead = normalised.split(None, 1)[0].upper()
    entry: Dict[str, Any] = {"sql": normalised, "lead_verb": lead}
    try:
        res = executor(normalised)
        entry["row_count"] = res.row_count
        entry["ok"] = res.error is None
        if res.error:
            entry["error"] = res.error
    except Exception as exc:
        entry["ok"] = False
        entry["error"] = f"{type(exc).__name__}: {str(exc)[:250]}"
        res = ExecutorResult(error=entry["error"])
    receipt["sql_trace"].append(entry)
    return res


def run_stratified_sampling(
    *,
    host: str,
    port: int,
    user: str,
    label: str,
    sql_executor: SqlExecutor,
    per_table: Dict[str, Dict[str, Any]],  # from composition census
    tables_per_stratum: int = 2,
    rows_per_table: int = 5,
) -> Dict[str, Any]:
    """Stratified sample: schema = stratum. CP1 walker picks tables per
    stratum; each table yields `rows_per_table` REDACTED rows into the
    receipt. All PII values replaced by deterministic salted tokens."""
    receipt: Dict[str, Any] = {
        "at_utc": _iso(),
        "label": label,
        "host": host,
        "port": port,
        "user": user,
        "connected": bool(per_table),
        "sql_trace": [],
        "strata": {},  # schema -> {tables_picked: [], sample_manifest_sha: str}
        "samples": {},  # "schema.table" -> {columns, rows_redacted, pii_signals}
        "pii_signals_summary": {"total": 0, "by_kind": {}},
        "totals": {"strata": 0, "tables_sampled": 0, "rows_redacted": 0},
        "errors": [],
    }

    # Group per_table by schema.
    by_schema: Dict[str, List[str]] = {}
    for key in per_table:
        sch = key.split(".", 1)[0]
        by_schema.setdefault(sch, []).append(key)

    for sch, keys in by_schema.items():
        # Sort deterministic + prefer non-empty tables.
        keys_sorted = sorted(
            keys,
            key=lambda k: (-(per_table[k].get("row_count") or 0), k),
        )
        walk = deterministic_walk(keys_sorted, sample_size=min(tables_per_stratum, len(keys_sorted)))
        picked = walk["sample"]
        receipt["strata"][sch] = {
            "tables_picked": picked,
            "manifest_sha256": walk["manifest_sha256"],
        }
        receipt["totals"]["strata"] += 1
        for tk in picked:
            _sch, _tbl = tk.split(".", 1)
            sql = f"SELECT * FROM `{_sch}`.`{_tbl}` LIMIT {int(rows_per_table)}"
            res = _guarded(sql, sql_executor, receipt)
            if res.error:
                receipt["errors"].append({"stage": f"sample {tk}", "err": res.error})
                continue
            cols = list(res.columns)
            rows_redacted: List[Dict[str, Any]] = []
            pii_for_table: List[Dict[str, Any]] = []
            for row in res.rows:
                d = {cols[i]: row[i] for i in range(len(cols))} if cols else {}
                for sig in detect_pii(d):
                    receipt["pii_signals_summary"]["total"] += 1
                    bk = receipt["pii_signals_summary"]["by_kind"]
                    bk[sig.signal_name] = bk.get(sig.signal_name, 0) + 1
                    pii_for_table.append(
                        {"kind": sig.signal_name, "field": sig.source_ref, "confidence": sig.confidence}
                    )
                rows_redacted.append(redact_row(d))
            receipt["samples"][tk] = {
                "columns": cols,
                "rows_redacted": rows_redacted,
                "pii_signals": pii_for_table,
            }
            receipt["totals"]["tables_sampled"] += 1
            receipt["totals"]["rows_redacted"] += len(rows_redacted)

    _finalize(receipt)
    return receipt


def _finalize(receipt: Dict[str, Any]) -> None:
    receipt.pop("password", None)
    assert_no_raw_pii(data_view(receipt))
    receipt["sample_bundle_sha256"] = _canonical_sha256(
        {k: v for k, v in receipt.items() if k != "sample_bundle_sha256"}
    )
