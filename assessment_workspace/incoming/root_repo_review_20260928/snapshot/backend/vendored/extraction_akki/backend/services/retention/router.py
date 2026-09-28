"""services.retention.router — CA1-N1 endpoints.

GET  /api/retention/classes       · declared retention letter per class
POST /api/retention/enforce       · run enforcement (default dry_run=true)
GET  /api/retention/attestations  · attestation records
GET  /api/retention/expired       · expired records list (audit)
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, ConfigDict, Field

from services.retention import classes as _classes
from services.retention import enforce as _enforce


router = APIRouter()


class EnforceRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    dry_run: bool = Field(default=True, description="Default True. Set False to write .expired sidecars + attestation record.")


@router.get("/api/retention/classes")
async def get_classes() -> Dict[str, Any]:
    """CA1-N1 · governed per-record-class retention letter."""
    return {
        "classes": _classes.RETENTION_CLASSES,
        "note": (
            "Append-only classes take mark-expired posture · NEVER delete. "
            "Governed-delete classes soft-delete to retired/ after retention, "
            "then hard-delete after grace_period_days. Canon 1 §4.3."
        ),
    }


@router.post("/api/retention/enforce")
async def post_enforce(body: EnforceRequest) -> Dict[str, Any]:
    """CA1-N1 · run enforcement · dry_run default true."""
    run = _enforce.run_enforcement(dry_run=body.dry_run)
    return asdict(run)


@router.get("/api/retention/attestations")
async def get_attestations(limit: int = Query(50, ge=1, le=500)) -> Dict[str, Any]:
    """List attestation records · newest first."""
    return {
        "attestations": _enforce.list_attestations(limit=limit),
    }


@router.get("/api/retention/expired")
async def get_expired(
    class_name: Optional[str] = Query(None, description="filter to one record class · e.g. 'crossing_receipts'"),
    limit: int = Query(100, ge=1, le=1000),
) -> Dict[str, Any]:
    """List records that currently carry a .expired sidecar (audit view)."""
    return {
        "expired": _enforce.list_expired(class_name=class_name, limit=limit),
    }
