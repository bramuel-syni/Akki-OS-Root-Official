"""services.chokepoint.router — Data Shield HTTP surface (W3).

Endpoints:
  POST /api/shield/dry-run    — CA1-007 · dry-run preview (Doc 02 §A5.2/§A5.3)
  GET  /api/shield/receipts   — crossing-receipt log (Doc 01 §A5.7)
  GET  /api/shield/allowlists — governed masking-tier + residency configs
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from services.chokepoint import list_receipts
from services.chokepoint.dry_run import DeclarationInvalid, preview
from services.chokepoint.masking_tier import _entries_by_tier
from services.chokepoint.residency import allowlisted_regions


router = APIRouter()


class DryRunRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    candidate_declaration: Dict[str, Any] = Field(..., description="{kind: 'exact_value'|'pattern'|'category', ...}")
    sample_scope: str = Field(default="crossing_receipts_recent", min_length=1, max_length=64)


@router.post("/api/shield/dry-run")
async def post_shield_dry_run(body: DryRunRequest) -> Dict[str, Any]:
    """CA1-007 · dry-run preview. REFERENCE-NOT-COPY: preview refs by
    receipt identity, never copies receipt content into the response."""
    try:
        return preview(
            candidate_declaration=body.candidate_declaration,
            sample_scope=body.sample_scope,
        )
    except DeclarationInvalid as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/api/shield/receipts")
async def get_shield_receipts(
    limit: int = Query(50, ge=1, le=500),
    kind: Optional[str] = Query(None, description="Filter: solva | chat | llm | data | ssh (matches by prefix); None = all"),
    include_expired: bool = Query(False, description="W6 CP3 · CA1-N1 · include receipts marked expired (audit view). Default False."),
) -> Dict[str, Any]:
    """Doc 01 §A5.7 · the crossing-receipt log.

    Returns the receipt identities + custody markers (kind, region, verb,
    masking_tier, actor, at_iso). The credential is NEVER on the receipt
    (statically enforced by services.chokepoint's dataclass shape) — so
    this endpoint cannot leak one.

    W5 CP4 · kind filter (Reasoning Shield uses this):
      - 'solva'  → all solva_* kinds (frame_audit / candidate_generation / synthesis)
      - 'chat'   → chat_governed_answer
      - 'llm'    → any llm_* / solva_* / chat_* / thinklab_direct_answer
      - 'data'   → rds_data_api
      - 'ssh'    → ssh_seam

    W6 CP3 · CA1-N1 retention:
      Receipts marked expired (via a `.expired` sidecar) are EXCLUDED
      from render by default. `include_expired=true` surfaces them
      for audit view.
    """
    import os as _os
    import pathlib as _pl

    receipts = list_receipts()
    # Most recent first.
    receipts.sort(key=lambda r: r.at_iso, reverse=True)

    # W6 CP3 · exclude expired by default.
    if not include_expired:
        receipts_dir = _pl.Path(_os.environ.get(
            "CROSSING_RECEIPT_DIR",
            "/app/assessment_workspace/phase0/crossing_receipts",
        ))
        expired_ids = {
            sidecar.stem.replace(".json", "")
            for sidecar in receipts_dir.glob("*.expired")
        }
        receipts = [r for r in receipts if r.receipt_id not in expired_ids]

    if kind:
        k = kind.lower()
        if k == "solva":
            receipts = [r for r in receipts if r.kind.startswith("solva_")]
        elif k == "chat":
            receipts = [r for r in receipts if r.kind.startswith("chat_")]
        elif k == "llm":
            llm_prefixes = ("solva_", "chat_", "thinklab_", "llm_")
            receipts = [r for r in receipts if any(r.kind.startswith(p) for p in llm_prefixes)]
        elif k == "data":
            receipts = [r for r in receipts if r.kind == "rds_data_api"]
        elif k == "ssh":
            receipts = [r for r in receipts if r.kind == "ssh_seam"]
        # unknown kind → no filter (return all)

    return {
        "count": len(receipts),
        "receipts": [r.to_json() for r in receipts[:limit]],
        "kind_filter": kind,
        "include_expired": include_expired,
    }


@router.get("/api/shield/allowlists")
async def get_shield_allowlists() -> Dict[str, Any]:
    """Read-only view of the governed positive allowlists in force today.

    Data Shield surface consumes this to render "rules in force" — the
    v7 oracle's "rails" pattern, honestly bound to what's actually on
    disk (not to fabricated status lines).
    """
    entries = _entries_by_tier()
    tiers = [
        {
            "tier": entry["tier"],
            "description": entry.get("description", ""),
            "admissible_under_env": entry.get("admissible_under_env", []),
            "applicable_kinds": entry.get("applicable_kinds", []),
            "row_content_permitted": entry.get("row_content_permitted", False),
            "not_admissible_because": entry.get("not_admissible_because"),
            "canon_anchor": entry.get("canon_anchor", ""),
        }
        for entry in entries.values()
    ]
    return {
        "masking_tiers": sorted(tiers, key=lambda t: t["tier"]),
        "residency": {
            "allowlisted_regions": allowlisted_regions(),
            "note": (
                "Region field on record is required for every crossing. "
                "A crossing whose region is missing is refused honestly "
                "(Doc 01 §A5.6 + CA1-N4)."
            ),
        },
    }
