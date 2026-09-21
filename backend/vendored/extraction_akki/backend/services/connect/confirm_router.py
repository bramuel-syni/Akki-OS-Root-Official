"""services.connect.confirm_router · POST /api/connect/confirm/{draft_id}
                                    · PATCH /api/connect/draft/{draft_id}

Owner directive 2026-08-26 (Wave A · R2 verbatim):
    "confirm must reference server-side draft state, not a captured null"
    "each failure names the field and the remedy in plain words"

Handler contract:
    * Confirm reads the draft server-side, dispatches to the pipeline by
      kind (compute → gpu_submit, data-source → rds_data_submit, else →
      intent record).
    * The client sends ONLY {} in the confirm body — no fields, no secrets.
    * The draft is CONSUMED by a successful confirm (delete on the way in).
    * Missing/expired drafts return 404 with a human-speak body.
    * All 4xx/5xx responses carry a structured detail: {field, remedy, plain}.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ValidationError

from services.connect import gpu_pipeline_stub
from services.connect.draft_store import get_store
from services.connect.human_speak import (
    missing_draft_error,
    not_editable_error,
    translate_pydantic_error,
)


router = APIRouter()


class ConfirmPayload(BaseModel):
    """The client sends {} on confirm — no fields. This shape is just a
    marker to keep FastAPI happy. Extra fields are ignored."""

    model_config = {"extra": "ignore"}


class DraftPatchPayload(BaseModel):
    """Single-field edit-in-place per SOLVA §5.6 (edit-in-place)."""

    field: str = Field(..., min_length=1, max_length=64)
    value: str = Field(..., min_length=0, max_length=512)


# Fields that cannot be patched via the URL — must come through the
# credentials paste seam.
_SECRET_FIELDS = {
    "password", "aws_secret_access_key", "api_key",
    "aws_access_key_id",  # treated as sensitive by policy even if not strictly a secret
}


@router.post("/api/connect/confirm/{draft_id}")
async def post_confirm(draft_id: str, _payload: ConfirmPayload) -> Dict[str, Any]:
    """Confirm and fire the pipeline. Reads server-side draft state, never
    client-provided fields."""
    store = get_store()
    d = store.consume(draft_id)
    if d is None:
        raise HTTPException(status_code=404, detail=missing_draft_error(draft_id))

    kind = d.kind
    if kind == "compute":
        payload = {
            "host_name": d.fields.get("host_name", ""),
            "username": d.fields.get("username", ""),
            "password": d.password or "",
            "public_ip": d.fields.get("public_ip", ""),
            "private_ip": d.fields.get("private_ip", ""),
            "os": d.fields.get("os", ""),
            "deploy_date": d.fields.get("deploy_date", ""),
        }
        try:
            result = gpu_pipeline_stub.run_gpu_pipeline(payload)
        except ValidationError as e:  # pragma: no cover · defensive
            raise HTTPException(status_code=422,
                                detail=translate_pydantic_error(e, kind=kind))
        return {"kind": "compute", **result}

    if kind == "data-source":
        payload = {
            "region": d.fields.get("region", ""),
            "cluster_arn": d.fields.get("cluster_arn", ""),
            "secret_arn": d.fields.get("secret_arn", ""),
            "database": d.fields.get("database"),
            "aws_access_key_id": d.fields.get("aws_access_key_id"),
            "aws_secret_access_key": d.aws_secret_access_key,
        }
        # Strip Nones so downstream sees only present fields
        payload = {k: v for k, v in payload.items() if v is not None}
        try:
            result = gpu_pipeline_stub.run_rds_pipeline(payload)
        except ValidationError as e:  # pragma: no cover
            raise HTTPException(status_code=422,
                                detail=translate_pydantic_error(e, kind=kind))
        for k in ("aws_secret_access_key", "aws_access_key_id"):
            if isinstance(result, dict):
                result.pop(k, None)
        return {"kind": "data-source", **(result or {})}

    # LLM / trained-model / other · honest intent recording
    payload = {
        "kind": kind or "unknown",
        "name": d.fields.get("name", f"unnamed-{kind or 'thing'}"),
        "description": d.fields.get("_paste_preview", "")[:200],
    }
    record = gpu_pipeline_stub.run_intent_record(payload)
    return {"kind": kind, "intent": record}


@router.patch("/api/connect/draft/{draft_id}")
async def patch_draft(draft_id: str, payload: DraftPatchPayload) -> Dict[str, Any]:
    """Edit a non-secret field on an existing draft, in place.

    Custody rule: credential-shaped fields (password, aws_secret_access_key,
    api_key, aws_access_key_id) cannot be patched via this route — the
    client must re-open the drawer and paste again.
    """
    if payload.field in _SECRET_FIELDS:
        raise HTTPException(status_code=400,
                            detail=not_editable_error(payload.field))
    store = get_store()
    ok = store.patch_field(draft_id, payload.field, payload.value)
    if not ok:
        raise HTTPException(status_code=404,
                            detail=missing_draft_error(draft_id))
    return {"draft_id": draft_id, "field": payload.field, "value": payload.value}
