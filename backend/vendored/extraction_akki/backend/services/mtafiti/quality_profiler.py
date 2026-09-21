"""Data-Quality Profiler — CP5 kernel.

Owner authorisation this session:
    "CP4..CPn: full deep census over both connections — composition-by-
    strata, semantic column classification, PII detection+tagging,
    data-quality profiling, embeddings/relationship signals,
    deterministic stratified sampling."

CP5 delivers: null-density per column · cardinality (distinct-count on
bounded sample) · format-conformance for role-tagged columns (fraction
of sampled values that match the role's canonical regex).

Every SQL routed through CP1 read-only guard. Table + column selection
uses CP1 deterministic adaptive walker so C4-013 repeatability holds.
Every sampled column values-list is discarded after aggregation — only
the aggregate (null_ratio, distinct_count, format_conformance_ratio)
lands in the receipt.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.mtafiti.detectors.pii_detector import _PII_PATTERNS, _luhn_ok
from services.mtafiti.detectors.pii_redaction_guard import assert_no_raw_pii
from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
from services.mtafiti.probes.live_readonly_probe import (
    ExecutorResult,
    SqlExecutor,
    data_view,
)
from services.mtafiti.sampling.deterministic_adaptive_walker import deterministic_walk


# ────────────────────────────────────────────────────────────────────────
# Role → canonical-regex map (from pii_detector), extended with column-
# name-only roles (role.email → pii.email regex; role.phone → pii.phone).
# ────────────────────────────────────────────────────────────────────────
_ROLE_TO_REGEX: Dict[str, "re.Pattern[str]"] = {}
for _kind, _rx, _ in _PII_PATTERNS:
    # pii.email → role.email etc.
    _role_name = _kind.replace("pii.", "role.")
    _ROLE_TO_REGEX[_role_name] = _rx


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


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


def _profile_column_values(values: List[Any], role_names: List[str]) -> Dict[str, Any]:
    """Compute aggregate quality signals from a sampled column values list.

    Returns {null_ratio, distinct_count, sample_n, format_conformance:{role_name: ratio}}.
    Values themselves are NOT retained.
    """
    n = len(values)
    if n == 0:
        return {"null_ratio": None, "distinct_count": 0, "sample_n": 0, "format_conformance": {}}
    null_n = sum(1 for v in values if v is None)
    non_null = [v for v in values if v is not None]
    distinct = len({str(v) for v in non_null})
    conformance: Dict[str, float] = {}
    for role in role_names:
        rx = _ROLE_TO_REGEX.get(role)
        if rx is None:
            continue
        if not non_null:
            conformance[role] = 0.0
            continue
        hits = 0
        for v in non_null:
            s = v if isinstance(v, str) else str(v)
            m = rx.search(s)
            if m is None:
                continue
            if role == "role.credit_card" and not _luhn_ok(m.group(0)):
                continue
            hits += 1
        conformance[role] = hits / len(non_null)
    return {
        "null_ratio": null_n / n,
        "distinct_count": distinct,
        "sample_n": n,
        "format_conformance": conformance,
    }


def run_quality_profile(
    *,
    host: str,
    port: int,
    user: str,
    label: str,
    sql_executor: SqlExecutor,
    per_table: Dict[str, Dict[str, Any]],  # from composition census
    tables_per_schema: int = 3,
    columns_per_table: int = 10,
    sample_size: int = 200,
) -> Dict[str, Any]:
    """Run the CP5 data-quality profile.

    `per_table` is a dict keyed by "schema.table" carrying at least
    {row_count, column_count, columns: [{column_name, data_type, ...}],
    role_signals: [{role, column, confidence}, ...]} — i.e. the CP4
    composition census output.
    """
    receipt: Dict[str, Any] = {
        "at_utc": _iso(),
        "label": label,
        "host": host,
        "port": port,
        "user": user,
        "connected": False,
        "sql_trace": [],
        # per_column: {"schema.table.col": {null_ratio, distinct_count, sample_n,
        #                                    format_conformance:{role:ratio}, roles:[role...]}}
        "per_column": {},
        "totals": {
            "tables_profiled": 0,
            "columns_profiled": 0,
            "sample_rows_pulled": 0,
        },
        "errors": [],
    }
    # Group per_table by schema so we can walker-pick a subset per schema.
    by_schema: Dict[str, List[str]] = {}
    for key in per_table.keys():
        sch = key.split(".", 1)[0]
        by_schema.setdefault(sch, []).append(key)

    receipt["connected"] = True
    for sch, keys in by_schema.items():
        # Sort deterministic + pick top-N by row_count for stability.
        keys_sorted = sorted(
            keys,
            key=lambda k: (-(per_table[k].get("row_count") or 0), k),
        )
        # CP1 walker: bounded, deterministic. Feed the sorted list.
        walk_manifest = deterministic_walk(keys_sorted, sample_size=min(tables_per_schema, len(keys_sorted)))
        picked_tables = walk_manifest["sample"]
        for tk in picked_tables:
            tbl_info = per_table[tk]
            all_cols = tbl_info.get("columns", [])
            roles_by_col: Dict[str, List[str]] = {}
            for rs in tbl_info.get("role_signals", []):
                roles_by_col.setdefault(rs["column"], []).append(rs["role"])
            # Column selection: prioritise role-tagged columns, then walker-pick rest.
            role_tagged = [c["column_name"] for c in all_cols if c["column_name"] in roles_by_col]
            untagged = [c["column_name"] for c in all_cols if c["column_name"] not in roles_by_col]
            picked_cols = list(role_tagged[:columns_per_table])
            if len(picked_cols) < columns_per_table and untagged:
                walk2 = deterministic_walk(sorted(untagged), sample_size=columns_per_table - len(picked_cols))
                picked_cols.extend(walk2["sample"])
            if not picked_cols:
                continue
            # One SELECT per table pulling the picked columns bounded.
            col_list_sql = ", ".join(f"`{c}`" for c in picked_cols)
            _sch, _tbl = tk.split(".", 1)
            sql = f"SELECT {col_list_sql} FROM `{_sch}`.`{_tbl}` LIMIT {int(sample_size)}"
            res = _guarded_execute(sql, sql_executor, receipt)
            if res.error:
                receipt["errors"].append({"stage": f"sample {tk}", "err": res.error})
                continue
            receipt["totals"]["tables_profiled"] += 1
            receipt["totals"]["sample_rows_pulled"] += len(res.rows)
            for idx, col in enumerate(picked_cols):
                col_values = [row[idx] for row in res.rows]
                stats = _profile_column_values(col_values, roles_by_col.get(col, []))
                receipt["per_column"][f"{tk}.{col}"] = {
                    "roles": roles_by_col.get(col, []),
                    **stats,
                }
                receipt["totals"]["columns_profiled"] += 1

    _finalize_profile(receipt)
    return receipt


def _finalize_profile(receipt: Dict[str, Any]) -> None:
    receipt.pop("password", None)
    assert_no_raw_pii(data_view(receipt))
    receipt["profile_sha256"] = _canonical_sha256(
        {k: v for k, v in receipt.items() if k != "profile_sha256"}
    )
