"""services.whitepapers.router — Doc 14-024 CA1-005 Whitepaper HTTP surface.

W11 R4.6 · owner directive 2026-08-26 verbatim:
    "whitepaper HTTP surface"

Wraps services.whitepapers.draft.{draft_whitepaper, load_whitepapers}
in a thin HTTP layer:

    POST /api/whitepapers        draft a new whitepaper
    GET  /api/whitepapers        list existing whitepapers

The draft function enforces Doc 14 §33 (citation invariant · admission +
baseline must be on record) and §43 (idempotent whitepaper_id).
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from services.whitepapers import draft as _draft
# W11 R4.8 · Doc19A-005 verbatim: 'every worker output passes through the
# Critic Seam; shipped-without-seam is a defect'.
from services.critic_pass import producer_seam as _critic_seam


router = APIRouter()


@router.post("/api/whitepapers")
def post_whitepaper(payload: Dict[str, Any]):
    """Draft a whitepaper. 422 on validation failure (unknown admission
    or baseline citation); 409 if whitepaper_id already on record.

    Every drafted whitepaper is routed through the Critic Seam
    (Doc19A-005) before returning to the caller; the verdict is
    embedded in the response body (QA-1 · findings are DATA)."""
    try:
        w = _draft.draft_whitepaper(payload)
    except ValueError as e:
        msg = str(e)
        if "already on record" in msg:
            raise HTTPException(status_code=409, detail={"plain": msg,
                                                          "field": "whitepaper_id",
                                                          "remedy": "generate a new whitepaper_id and retry."})
        raise HTTPException(status_code=422, detail={"plain": msg,
                                                      "field": "cites_*",
                                                      "remedy": "cite an admission and a baseline that are on record."})
    # W11 R4.8 · producer-side seam attestation on the drafted artifact.
    # The whitepaper's textual payload lives in `summary_note` per
    # WhitepaperDraft_v0 (Doc 14 §33 · summary + citations).
    verdict = _critic_seam.route_through_seam(
        artifact_ref=f"whitepaper:{w.whitepaper_id}",
        artifact_content=w.summary_note,
        producing_instance_id="whitepapers.draft",
    )
    return {**w.model_dump(),
            "critic_verdict": _critic_seam.verdict_summary(verdict)}


@router.get("/api/whitepapers")
def list_whitepapers() -> Dict[str, Any]:
    """List all whitepapers on record (sorted by drafted_at then id)."""
    rows: List[Dict[str, Any]] = [w.model_dump() for w in _draft.load_whitepapers()]
    return {"whitepapers": rows, "count": len(rows)}
