"""services.n_series.router — Doc 15 N-series (breach + erasure) HTTP surface.

W11 R4.7 · owner directive 2026-08-26 verbatim:
    "N-series breach/erasure routers"

Wraps services.n_series.{breach.fire_breach_notification,
erasure.fire_erasure_request} and their loaders in HTTP endpoints:

    POST /api/n_series/breach          fire a breach notification
    GET  /api/n_series/breach          list breach notifications
    POST /api/n_series/erasure         fire an erasure request
    GET  /api/n_series/erasure         list erasure requests

N-series discipline:
  * Breach fires from a governance detection (N2 · notification within
    the ceremony countdown).
  * Erasure is an operator-initiated request (N3 · right-to-be-forgotten).
Both write append-only records under `phase0/n_series/{breach,erasure}/`.
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from services.n_series import breach as _breach
from services.n_series import erasure as _erasure
from services.response_sanitizer import sanitize  # Wave E CP-E7 · response boundary


router = APIRouter()


@router.post("/api/n_series/breach")
def post_breach(payload: Dict[str, Any]):
    """Fire a breach notification. 422 on payload validation failure."""
    try:
        row = _breach.fire_breach_notification(payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"plain": str(e),
                                                      "field": "",
                                                      "remedy": "check the breach payload shape."})
    return sanitize(row.model_dump())


@router.get("/api/n_series/breach")
def list_breach() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = [sanitize(r.model_dump()) for r in _breach.load_breach_notifications()]
    return {"breach_notifications": rows, "count": len(rows)}


@router.post("/api/n_series/erasure")
def post_erasure(payload: Dict[str, Any]):
    """Fire an erasure request. 422 on payload validation failure."""
    try:
        row = _erasure.fire_erasure_request(payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"plain": str(e),
                                                      "field": "",
                                                      "remedy": "check the erasure payload shape."})
    return sanitize(row.model_dump())


@router.get("/api/n_series/erasure")
def list_erasure() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = [sanitize(r.model_dump()) for r in _erasure.load_erasure_requests()]
    return {"erasure_requests": rows, "count": len(rows)}


# ---------- Wave E CP-E3 · CA1-N3 · rights-lapse flags surface ----------

@router.get("/api/n_series/rights_lapse_flags")
def list_rights_lapse_flags() -> Dict[str, Any]:
    """CA1-N3 · Wave E CP-E3 · list rights-lapse flags emitted for
    trained models whose corpus included an erased subject's data.
    Owner ruling: 'already-trained models get FLAGGED via the A17.15
    rights-lapse provenance mechanism and scheduled for retraining OR
    documented as residual exposure.'"""
    rows: List[Dict[str, Any]] = [
        sanitize(f.model_dump()) for f in _erasure.load_rights_lapse_flags()
    ]
    return {
        "rights_lapse_flags": rows,
        "count": len(rows),
        "policy_ref": "services/n_series/erasure_policy.v0.json",
    }
