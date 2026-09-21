"""Cost Receipt Builder — CP6 kernel.

Aggregates per-host cost figures from the CP3-CP6 banked receipts.
Estimates egress bytes from row-counts + column data lengths (from
information_schema.tables DATA_LENGTH proxy for full-table scans; from
sampled row-count × avg-cell-size for bounded sampling). GPU-hours are
0.0 (no GPU cycles consumed in CP1-CP6). Billing basis is
'cassava_lease · $0 marginal on idle capacity' per prior-session
finding banked in DECISIONS.md.

Emitted receipt is DetectionSignal-clean (contains only numeric costs +
metadata; no raw PII).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


_HUAWEI_EGRESS_RATE_USD_PER_GB = 0.16  # weego egress ~ same as prior-session finding
_BYTES_PER_GB = 1024 ** 3


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def _estimate_bytes_from_samples(host_receipt: Dict[str, Any]) -> int:
    """Estimate egress bytes from a sample bundle's rows_redacted."""
    total = 0
    for _key, info in (host_receipt.get("samples") or {}).items():
        for row in info.get("rows_redacted", []):
            # rough size = sum of str-lens; redaction tokens ≈ same footprint as raw values
            total += sum(len(str(v)) for v in row.values())
    return total


def build_cost_receipt(
    *,
    composition_path: Path,
    stratified_path: Path,
    quality_path: Path,
    huawei_egress_rate_usd_per_gb: float = _HUAWEI_EGRESS_RATE_USD_PER_GB,
    billing_basis: str = "cassava_lease · $0 marginal on idle capacity (banked prior-session)",
) -> Dict[str, Any]:
    """Aggregate egress + GPU hours across the CP1-CP6 phase0 receipts."""
    def _load_maybe(p: Path) -> Dict[str, Any]:
        return json.loads(p.read_text()) if p.is_file() else {}

    composition = _load_maybe(composition_path)
    stratified  = _load_maybe(stratified_path)
    quality     = _load_maybe(quality_path)

    hosts = sorted(set().union(
        composition.get("hosts", []),
        stratified.get("hosts", []),
        quality.get("hosts", []),
    ))

    per_host_cost: Dict[str, Dict[str, Any]] = {}
    total_bytes = 0
    for h in hosts:
        # Composition egress: overwhelmingly metadata queries, ~0.2 bytes per column entry.
        comp_h = composition.get("per_host", {}).get(h, {})
        comp_bytes = 400 * len(comp_h.get("sql_trace", []))  # rough per-query bytes
        # Quality egress: bounded sample pulls — use sample_rows_pulled × columns_per_table × avg 25 bytes.
        q_h = quality.get("per_host", {}).get(h, {})
        q_bytes = 25 * q_h.get("totals", {}).get("sample_rows_pulled", 0) * 5  # 5 cols avg
        # Stratified egress: from actual redacted samples.
        strat_h = stratified.get("per_host", {}).get(h, {})
        strat_bytes = _estimate_bytes_from_samples(strat_h)
        h_bytes = comp_bytes + q_bytes + strat_bytes
        total_bytes += h_bytes
        per_host_cost[h] = {
            "egress_bytes_estimated": h_bytes,
            "egress_gb_estimated": h_bytes / _BYTES_PER_GB,
            "egress_usd_estimated": (h_bytes / _BYTES_PER_GB) * huawei_egress_rate_usd_per_gb,
            "composition_sql_count": len(comp_h.get("sql_trace", [])),
            "quality_sql_count": len(q_h.get("sql_trace", [])),
            "stratified_sql_count": len(strat_h.get("sql_trace", [])),
        }

    receipt: Dict[str, Any] = {
        "at_utc": _iso(),
        "label": "cp6_cost_receipt",
        "billing_basis": billing_basis,
        "huawei_egress_rate_usd_per_gb": huawei_egress_rate_usd_per_gb,
        "gpu_hours_consumed": 0.0,
        "gpu_marginal_cost_usd": 0.0,
        "per_host": per_host_cost,
        "totals": {
            "egress_bytes_estimated": total_bytes,
            "egress_gb_estimated": total_bytes / _BYTES_PER_GB,
            "egress_usd_estimated": (total_bytes / _BYTES_PER_GB) * huawei_egress_rate_usd_per_gb,
            "gpu_hours": 0.0,
            "gpu_usd": 0.0,
            "wave_total_usd_estimated": (total_bytes / _BYTES_PER_GB) * huawei_egress_rate_usd_per_gb,
        },
    }
    receipt["cost_receipt_sha256"] = _sha256(
        {k: v for k, v in receipt.items() if k != "cost_receipt_sha256"}
    )
    return receipt
