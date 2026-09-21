"""services.cost_ledger.ledger — the Cost Ledger (CA1-008).

Consumes W5 crossing receipts + W2 reflection records + SSH seam receipts.
Produces LedgerEntry records carrying:
    - quantities (from receipt payload_shape · never inferred)
    - money (only when a rate is on record; else None + honest_gap_note)
    - lever attribution (CA1-008 sequence: cache → route → narrow →
      cascade → waste_report; attributed only where evidence exists)
    - rate_provenance ('owner_supplied' / 'absent')
    - metering_source (carried forward from the receipt for W6 fidelity)

Canon 1 §4.4 · Measure, do not assert.
Canon 1 §4.1 · Cost optimisations fail transparent.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.cost_ledger.rates import (
    HONEST_GAP_SENTENCE,
    default_model_for_purpose,
    rate_for_gpu_hour,
    rate_for_model,
)

log = logging.getLogger(__name__)


# CA1-008 · lever sequence in exact canonical order.
LEVER_ORDER = ["cache", "route", "narrow", "cascade", "waste_report"]


_LLM_KINDS = ("chat_", "solva_", "thinklab_", "llm_")
_SEAM_KINDS = ("ssh_seam",)


def _receipts_dir() -> Path:
    return Path(os.environ.get(
        "CROSSING_RECEIPT_DIR",
        "/app/assessment_workspace/phase0/crossing_receipts",
    ))


def _reflection_dir() -> Path:
    return Path(os.environ.get(
        "REFLECTION_RECORD_DIR",
        "/app/assessment_workspace/phase0/reflection_records",
    ))


@dataclass
class LedgerEntry:
    """One ledger row · REFERENCE-NOT-COPY on the receipt (identity join).

    Quantities are FACTS drawn from the receipt. Money is a computed
    figure only when a rate is on record; else None + honest_gap_note.
    """
    receipt_id: str
    kind: str
    at_iso: str
    actor: str

    # Provenance from the receipt (identity + boundary).
    model_id: str = ""
    provider: str = ""
    endpoint_host: str = ""
    residency_region: str = ""
    masking_tier: str = ""
    purpose_declared: str = ""

    # Quantities (measured facts).
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    gpu_hours: float = 0.0
    calls: int = 1
    metering_source: str = ""

    # Money (only when rate on record).
    cost_in: Optional[float] = None
    cost_out: Optional[float] = None
    cost_gpu: Optional[float] = None
    cost_total: Optional[float] = None
    currency: str = ""

    # Honest absence markers.
    rate_provenance: str = "absent"  # 'owner_supplied' or 'absent'
    honest_gap_note: str = ""

    # CA1-008 lever attribution.
    levers: List[Dict[str, Any]] = field(default_factory=list)


def _new_levers_scaffold() -> List[Dict[str, Any]]:
    """Every entry names all five levers in exact order — attributed=False
    means honest-empty (no evidence yet), NOT invented saving."""
    return [
        {"name": name, "saving": 0.0, "evidence": "", "attributed": False}
        for name in LEVER_ORDER
    ]


def _attribute_route_lever(entry: LedgerEntry) -> None:
    """CA1-008 · 'route' lever: saving = (default_rate - actual_rate) *
    tokens, when the actual model is cheaper than the default for this
    purpose AND both rates are on record."""
    if not entry.purpose_declared or not entry.model_id:
        return
    default_id = default_model_for_purpose(entry.purpose_declared)
    if not default_id or default_id == entry.model_id:
        return
    default_rate = rate_for_model(default_id)
    actual_rate = rate_for_model(entry.model_id)
    if not default_rate or not actual_rate:
        return
    # Saving = tokens × (default_rate - actual_rate) / 1M.
    saving_in = (entry.tokens_in / 1_000_000.0) * (
        default_rate["rate_per_million_tokens_in"] -
        actual_rate["rate_per_million_tokens_in"]
    )
    saving_out = (entry.tokens_out / 1_000_000.0) * (
        default_rate["rate_per_million_tokens_out"] -
        actual_rate["rate_per_million_tokens_out"]
    )
    saving_total = round(max(0.0, saving_in + saving_out), 4)
    for l in entry.levers:
        if l["name"] == "route":
            l["saving"] = saving_total
            l["attributed"] = saving_total > 0
            l["evidence"] = (
                f"used {entry.model_id!r} for purpose "
                f"{entry.purpose_declared!r} instead of default "
                f"{default_id!r} · saving = ({default_rate['rate_per_million_tokens_in']}"
                f" - {actual_rate['rate_per_million_tokens_in']})/M × {entry.tokens_in}"
                f" tokens_in + ({default_rate['rate_per_million_tokens_out']}"
                f" - {actual_rate['rate_per_million_tokens_out']})/M × {entry.tokens_out}"
                f" tokens_out = ${saving_total:.4f}"
            )
            return


def _shape_entry_from_receipt(receipt: Dict[str, Any]) -> Optional[LedgerEntry]:
    """Project a crossing receipt onto a LedgerEntry — quantities always,
    money computed if rate on record."""
    kind = receipt.get("kind", "")
    payload = receipt.get("payload_shape") or {}

    entry = LedgerEntry(
        receipt_id=receipt.get("receipt_id", ""),
        kind=kind,
        at_iso=receipt.get("at_iso", ""),
        actor=receipt.get("actor", ""),
        endpoint_host=receipt.get("endpoint_host", ""),
        residency_region=receipt.get("residency_region", ""),
        masking_tier=receipt.get("masking_tier", ""),
        purpose_declared=payload.get("purpose_declared", ""),
        model_id=payload.get("model_id", ""),
        provider=payload.get("provider", ""),
        tokens_in=int(payload.get("tokens_in", 0) or 0),
        tokens_out=int(payload.get("tokens_out", 0) or 0),
        latency_ms=int(payload.get("latency_ms", 0) or 0),
        gpu_hours=float(payload.get("gpu_hours", 0) or 0),
        metering_source=payload.get("metering_source", ""),
        levers=_new_levers_scaffold(),
    )

    # Money · LLM kinds first.
    if any(kind.startswith(p) for p in _LLM_KINDS):
        rate = rate_for_model(entry.model_id) if entry.model_id else None
        if rate:
            entry.cost_in = round(
                (entry.tokens_in / 1_000_000.0)
                * float(rate.get("rate_per_million_tokens_in", 0)),
                6,
            )
            entry.cost_out = round(
                (entry.tokens_out / 1_000_000.0)
                * float(rate.get("rate_per_million_tokens_out", 0)),
                6,
            )
            entry.cost_total = round((entry.cost_in or 0) + (entry.cost_out or 0), 6)
            entry.currency = rate.get("currency", "USD")
            entry.rate_provenance = rate.get("source", "owner_supplied")
        else:
            entry.honest_gap_note = HONEST_GAP_SENTENCE
    # Money · GPU-hour kinds.
    elif kind in _SEAM_KINDS:
        node_id = payload.get("node_id", "")
        rate = rate_for_gpu_hour(node_id) if node_id else None
        if rate and entry.gpu_hours > 0:
            entry.cost_gpu = round(entry.gpu_hours * float(rate.get("rate_per_hour", 0)), 6)
            entry.cost_total = entry.cost_gpu
            entry.currency = rate.get("currency", "USD")
            entry.rate_provenance = rate.get("source", "owner_supplied")
        else:
            entry.honest_gap_note = HONEST_GAP_SENTENCE
    else:
        # Other kinds (rds_data_api, etc.) — no money, no gap.
        pass

    # CA1-008 lever attribution.
    _attribute_route_lever(entry)

    return entry


def _iter_receipts() -> List[Dict[str, Any]]:
    d = _receipts_dir()
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.glob("rcp-*.json")):
        try:
            out.append(json.loads(f.read_text()))
        except Exception:  # pragma: no cover
            continue
    return out


def build_entries(
    *,
    since_iso: Optional[str] = None,
    limit: Optional[int] = None,
    kind: Optional[str] = None,
) -> List[LedgerEntry]:
    """Build ledger entries from all receipts on record."""
    receipts = _iter_receipts()
    if since_iso:
        receipts = [r for r in receipts if r.get("at_iso", "") >= since_iso]
    if kind:
        if kind == "llm":
            receipts = [r for r in receipts if any(r.get("kind", "").startswith(p) for p in _LLM_KINDS)]
        elif kind == "seam":
            receipts = [r for r in receipts if r.get("kind") == "ssh_seam"]
        else:
            receipts = [r for r in receipts if r.get("kind", "").startswith(kind)]
    entries: List[LedgerEntry] = []
    for r in receipts:
        e = _shape_entry_from_receipt(r)
        if e is not None:
            entries.append(e)
    entries.sort(key=lambda e: e.at_iso, reverse=True)
    if limit:
        entries = entries[:limit]
    return entries


def summarise(entries: List[LedgerEntry]) -> Dict[str, Any]:
    """Aggregate totals + honest-gap flag."""
    total_calls = sum(e.calls for e in entries)
    total_tokens_in = sum(e.tokens_in for e in entries)
    total_tokens_out = sum(e.tokens_out for e in entries)
    total_gpu_hours = round(sum(e.gpu_hours for e in entries), 4)
    total_latency_ms = sum(e.latency_ms for e in entries)

    total_cost = 0.0
    total_cost_is_partial = False
    currency = ""
    for e in entries:
        if e.cost_total is not None:
            total_cost += e.cost_total
            if not currency and e.currency:
                currency = e.currency
        else:
            # This entry has no cost — surface partial-total flag.
            if e.tokens_in > 0 or e.tokens_out > 0 or e.gpu_hours > 0:
                total_cost_is_partial = True

    # Levers roll-up (sum of savings across attributed levers).
    lever_totals = {name: {"saving": 0.0, "attributed_calls": 0} for name in LEVER_ORDER}
    for e in entries:
        for l in e.levers:
            if l["attributed"]:
                lever_totals[l["name"]]["saving"] = round(
                    lever_totals[l["name"]]["saving"] + l["saving"], 4
                )
                lever_totals[l["name"]]["attributed_calls"] += 1

    gaps_present = total_cost_is_partial
    return {
        "total_calls": total_calls,
        "total_tokens_in": total_tokens_in,
        "total_tokens_out": total_tokens_out,
        "total_gpu_hours": total_gpu_hours,
        "total_latency_ms": total_latency_ms,
        "total_cost": round(total_cost, 6) if total_cost else 0.0,
        "total_cost_is_partial": total_cost_is_partial,
        "currency": currency,
        "gaps_present": gaps_present,
        "honest_gap_note": HONEST_GAP_SENTENCE if gaps_present else "",
        "levers": lever_totals,
    }


__all__ = [
    "LEVER_ORDER",
    "LedgerEntry",
    "build_entries",
    "summarise",
]
