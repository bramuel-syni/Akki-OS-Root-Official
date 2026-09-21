"""services.model_admission.router — W7 CP7 · HTTP surface.

Endpoints:
  GET  /api/model_admission/records                 — admission history
  GET  /api/model_admission/records/{filename}      — one record
  POST /api/model_admission/dry_run                 — validate a MOAC card
                                                     WITHOUT firing register/write.

Notes:
  * The "fire" endpoint (POST /api/model_admission/admit) is NOT
    exposed at W7 — admission is triggered from the owner-side operator
    surface via a governed action that we haven't built yet. Emitting
    it as a public POST here would allow fabricated admissions. W7
    ships the READ surface + a dry-run validator; the governed firing
    endpoint is named as a W8 deferral.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from contracts.model_acceptance_card import ModelAcceptanceCard_v0


router = APIRouter()


def _admits_dir() -> Path:
    return Path(os.environ.get(
        "MODEL_ADMISSION_RECORDS_DIR",
        "/app/assessment_workspace/phase0/model_admission_records",
    ))


@router.get("/api/model_admission/records")
async def list_records() -> Dict[str, Any]:
    d = _admits_dir()
    if not d.is_dir():
        return {"count": 0, "records": [], "honest_note": (
            f"no admission ceremony has fired yet on this estate — "
            f"{d} is empty or absent."
        )}
    records: List[Dict[str, Any]] = []
    for p in sorted(d.glob("admit_*.json")):
        try:
            r = json.loads(p.read_text())
            r["_filename"] = p.name
            records.append(r)
        except Exception:
            continue
    return {"count": len(records), "records": records}


@router.get("/api/model_admission/records/{filename}")
async def get_record(filename: str) -> Dict[str, Any]:
    d = _admits_dir()
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="invalid filename")
    p = d / filename
    if not p.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"{filename!r} not on record. Honest gap.",
        )
    return json.loads(p.read_text())


@router.post("/api/model_admission/dry_run")
async def dry_run(card_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a MOAC card without firing register/write. Returns the
    contract validation outcome only — no admission decision. The
    governed firing endpoint is a W8 deferral (see module docstring)."""
    try:
        card = ModelAcceptanceCard_v0(**card_payload)
    except Exception as e:
        return {"valid": False, "error": str(e)}
    return {
        "valid": True,
        "candidate_model_id": card.candidate_model_id,
        "evidence_source_kind": card.evidence_source_kind,
        "six_criteria_present": True,
        "training_lineage_resolved": card.training_lineage_resolved,
    }
