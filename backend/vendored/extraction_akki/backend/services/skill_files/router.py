"""services.skill_files.router — Doc 18 A18.7 provenance HTTP surface.

W11 B · CP4 · Skill-file provenance chain (Ship-Manifest DoD closure).

Doc 18 §A18.7 verbatim (grounding brief · line 14 anchor):
    'every skill's provenance chain traces back to the training run that
     produced its adapter (extends Doc14-016 rights-lineage +
     Doc14-017 version-history).'

Doc 18 §A18.4 verbatim (grounding brief · line 12 anchor):
    'A18.4  [CANON] Below the floor is a refusal, never a degraded answer.'

Endpoints (thin HTTP wrapper over persistence + state):
    GET  /api/skill-files/state
         Rollup of every provisioned skill; ship_state=empty|populated,
         chain-length summary per row, honest-empty at CP4 landing.
    GET  /api/skill-files/{skill_id}/provenance
         Full chain for a single skill, 404 when unknown.
    POST /api/skill-files/{skill_id}/provenance
         Append a provenance record (write-once per Doc 18 TF-E4 (b) α).
         Body carries the SkillFileProvenanceV0 shape; 409 on repeat.

Every response body is REFERENCE-NOT-COPY: fields come from the on-disk
JSONL sidecar via services.skill_files.persistence, no secrets, no raw
signing material.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from contracts.skill_file_provenance_v0 import SkillFileProvenanceV0
from services.skill_files import persistence
from services.skill_files import state as _state


router = APIRouter()


@router.get("/api/skill-files/state")
def get_skill_files_state() -> Dict[str, Any]:
    """Rollup for the /skill-files React surface.

    Doc 18 A18.7 · REFERENCE-NOT-COPY: each row cites its on-disk record
    identifiers (skill_id, adapter_id, training_run_id, moac_card_id,
    recipe_version) so the surface renders without needing to embed the
    raw JSONL.
    """
    return _state.rollup()


@router.get("/api/skill-files/{skill_id:path}/provenance")
def get_skill_file_provenance(skill_id: str) -> Dict[str, Any]:
    """Full provenance chain for a single skill.

    Doc 18 A18.4 verbatim: 'Below the floor is a refusal, never a
    degraded answer.' → 404 with structured envelope when the skill
    is unknown, not a partial rollup.
    """
    record = persistence.get_by_skill_id(skill_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={
                "reason": "skill_file_provenance_not_found",
                "skill_id": skill_id,
            },
        )
    return record.model_dump()


@router.post("/api/skill-files/{skill_id:path}/provenance", status_code=201)
def post_skill_file_provenance(skill_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Append a provenance record. Write-once per Doc 18 TF-E4 (b) α:
    a second POST for the same skill_id returns 409 with a
    human-speak remedy (per Wave A R2 human-speak error discipline).
    """
    body_skill = payload.get("skill_id")
    if body_skill and body_skill != skill_id:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": (
                    "The path skill_id and the body skill_id disagree. "
                    "They must match."
                ),
                "field": "skill_id",
                "remedy": (
                    f"Set body.skill_id to {skill_id!r} or change the URL "
                    "to match the body."
                ),
            },
        )
    payload = {**payload, "skill_id": skill_id}
    try:
        record = SkillFileProvenanceV0.model_validate(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": (
                    "The provenance record could not be validated against "
                    "the SkillFileProvenanceV0 contract."
                ),
                "field": "body",
                "remedy": (
                    "Fill every required field (adapter_id, training_run_id, "
                    "moac_card_id, recipe_version, provisioned_at) and ensure "
                    "the provenance_chain begins with a base_model step."
                ),
                "detail": str(exc),
            },
        )
    try:
        persistence.append(record)
    except persistence.WriteOnceViolation as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "plain": (
                    "This skill has already been provisioned. Doc 18 "
                    "TF-E4 (b) α: a new slice needs a new skill_id."
                ),
                "field": "skill_id",
                "remedy": (
                    "Mint a fresh skill_id for the new provisioning and retry."
                ),
                "detail": str(exc),
            },
        )
    return record.model_dump()
