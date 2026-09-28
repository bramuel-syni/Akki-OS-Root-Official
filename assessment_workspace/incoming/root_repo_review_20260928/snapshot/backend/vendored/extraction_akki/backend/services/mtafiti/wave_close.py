"""Wave-Close Bundle Builder — CP7 kernel.

Consolidates the CP1-CP6 phase0 receipts into a single wave-close bundle
with a canonical sha256 chain that ratchets the entire wave.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def build_wave_close_bundle(*, phase0_dir: Path) -> Dict[str, Any]:
    """Aggregate CP1-CP6 phase0 receipts and derive wave-total figures."""

    def _load(p: Path) -> Dict[str, Any]:
        return json.loads(p.read_text()) if p.is_file() else {}

    live_probe = _load(phase0_dir / "live_readonly_probe_latest.json")
    composition = _load(phase0_dir / "composition_census_latest.json")
    quality = _load(phase0_dir / "quality_profile_latest.json")
    stratified = _load(phase0_dir / "stratified_samples_latest.json")
    cost = _load(phase0_dir / "cost_receipt_latest.json")

    hosts = sorted(set().union(
        live_probe.get("hosts", []),
        composition.get("hosts", []),
        quality.get("hosts", []),
        stratified.get("hosts", []),
    ))

    per_host_summary: Dict[str, Dict[str, Any]] = {}
    for h in hosts:
        comp_h = composition.get("per_host", {}).get(h, {})
        strat_h = stratified.get("per_host", {}).get(h, {})
        qual_h = quality.get("per_host", {}).get(h, {})
        live_h = live_probe.get("per_host", {}).get(h, {})
        fk_h = stratified.get("fk_candidate_signals_by_host", {}).get(h, {})
        per_host_summary[h] = {
            "connected": bool(live_h.get("connected") or comp_h.get("connected")),
            "composition_totals": comp_h.get("totals", {}),
            "column_role_signals_summary": comp_h.get("column_role_signals_summary", {}),
            "pii_signals_summary_live_probe": live_h.get("detector_signals_summary", {}),
            "pii_signals_summary_stratified": strat_h.get("pii_signals_summary", {}),
            "quality_totals": qual_h.get("totals", {}),
            "stratified_totals": strat_h.get("totals", {}),
            "fk_candidate_signals": fk_h,
        }

    totals = {
        "schemas": sum(
            per_host_summary[h]["composition_totals"].get("schemas", 0) for h in hosts
        ),
        "tables": sum(
            per_host_summary[h]["composition_totals"].get("tables", 0) for h in hosts
        ),
        "columns": sum(
            per_host_summary[h]["composition_totals"].get("columns", 0) for h in hosts
        ),
        "rows_estimated": sum(
            per_host_summary[h]["composition_totals"].get("rows", 0) for h in hosts
        ),
        "column_role_signals": sum(
            per_host_summary[h]["column_role_signals_summary"].get("total", 0) for h in hosts
        ),
        "pii_signals_live": sum(
            per_host_summary[h]["pii_signals_summary_live_probe"].get("total", 0) or 0 for h in hosts
        ),
        "pii_signals_stratified": sum(
            per_host_summary[h]["pii_signals_summary_stratified"].get("total", 0) or 0 for h in hosts
        ),
        "fk_candidate_signals": sum(
            per_host_summary[h]["fk_candidate_signals"].get("total", 0) or 0 for h in hosts
        ),
        "tables_profiled_quality": sum(
            per_host_summary[h]["quality_totals"].get("tables_profiled", 0) or 0 for h in hosts
        ),
        "columns_profiled_quality": sum(
            per_host_summary[h]["quality_totals"].get("columns_profiled", 0) or 0 for h in hosts
        ),
        "tables_sampled_stratified": sum(
            per_host_summary[h]["stratified_totals"].get("tables_sampled", 0) or 0 for h in hosts
        ),
        "rows_redacted_stratified": sum(
            per_host_summary[h]["stratified_totals"].get("rows_redacted", 0) or 0 for h in hosts
        ),
    }

    receipt_chain = {
        "live_probe": live_probe.get("per_host", {}) and {
            h: live_probe["per_host"][h].get("receipt_sha256") for h in hosts
        },
        "composition": {
            h: composition.get("per_host", {}).get(h, {}).get("census_sha256") for h in hosts
        },
        "quality": {
            h: quality.get("per_host", {}).get(h, {}).get("profile_sha256") for h in hosts
        },
        "stratified": {
            h: stratified.get("per_host", {}).get(h, {}).get("sample_bundle_sha256") for h in hosts
        },
        "cost_receipt": cost.get("cost_receipt_sha256"),
    }

    bundle = {
        "at_utc": _iso(),
        "label": "cp7_wave_close_bundle",
        "wave": "W-MTAFITI-GPU-DISCOVERY",
        "hosts": hosts,
        "per_host_summary": per_host_summary,
        "totals": totals,
        "cost_summary": {
            "gpu_hours_consumed": cost.get("gpu_hours_consumed", 0.0),
            "gpu_marginal_cost_usd": cost.get("gpu_marginal_cost_usd", 0.0),
            "egress_gb_estimated": cost.get("totals", {}).get("egress_gb_estimated"),
            "egress_usd_estimated": cost.get("totals", {}).get("egress_usd_estimated"),
            "wave_total_usd_estimated": cost.get("totals", {}).get("wave_total_usd_estimated"),
            "billing_basis": cost.get("billing_basis"),
        },
        "receipt_chain_sha256": receipt_chain,
    }
    bundle["wave_close_sha256"] = _sha256(
        {k: v for k, v in bundle.items() if k != "wave_close_sha256"}
    )
    return bundle
