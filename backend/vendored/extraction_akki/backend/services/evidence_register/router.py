"""services.evidence_register.router · Doc 19B §19B.5-6 HTTP surface.

W11 B · CP6 · EP-1 (evidence register) + EP-3 (A-4 claims validation).

Endpoints:
  GET  /api/evidence-register                        · list (empty at ship)
  GET  /api/evidence-register/{figure_id:path}       · 404 refusal for unknown
  POST /api/evidence-register                        · 201/409/422
  GET  /api/claims-validation                        · list (empty at ship)
  POST /api/claims-validation                        · 201/409/422

§19B.6 verbatim absolute: 'No figure reaches an external document
without a resolvable register row.' The GET-by-id 404 IS the refusal
mechanism — a figure without a register row cannot be quoted.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from contracts.claims_validation_row_v0 import ClaimsValidationRowV0
from contracts.evidence_register_row_v0 import EvidenceRegisterRowV0
from services.evidence_register import claims_validation, register


router = APIRouter()


@router.get("/api/evidence-register")
def list_evidence_register() -> Dict[str, Any]:
    """EP-1 · list every evidence-register row. Empty at ship."""
    rows = register.read_all()
    return {
        "ship_state": "empty" if not rows else "populated",
        "count": len(rows),
        "rows": [r.model_dump() for r in rows],
        "status_class_note": (
            "Doc 19B is PROPOSED · Owner-ratified 2026-08-26T04:20Z as "
            "not-yet-canon. Every row carries status_class='PROPOSED' "
            "until an Owner ratification flips it."
        ),
    }


@router.get("/api/evidence-register/{figure_id:path}")
def get_by_figure_id(figure_id: str) -> Dict[str, Any]:
    """§19B.6 absolute: 'No figure reaches an external document without
    a resolvable register row.' Unknown figure -> 404 refusal envelope."""
    row = register.get_by_figure_id(figure_id)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "reason": "figure_not_resolvable",
                "figure_id": figure_id,
                "spec_ref": "Doc 19B §19B.6",
                "spec_verbatim": (
                    "No figure reaches an external document without a "
                    "resolvable register row."
                ),
            },
        )
    return row.model_dump()


@router.post("/api/evidence-register", status_code=201)
def post_evidence_register(payload: Dict[str, Any]) -> Dict[str, Any]:
    """EP-2 · dual-judge scoring; contract enforces min 2 judges +
    judge_versions count parity. Write-once on figure_id."""
    try:
        row = EvidenceRegisterRowV0.model_validate(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": (
                    "The evidence-register row could not be validated "
                    "against Doc 19B §19B.5 shape."
                ),
                "field": "body",
                "remedy": (
                    "Provide figure_id, figure, method, named_site "
                    "(from the 5 §19B.4 sites), at least 2 judges + "
                    "matching judge_versions, rubric_version, kappa in "
                    "[-1,1], date, and at least one source_row."
                ),
                "detail": str(exc),
            },
        )
    try:
        register.append(row)
    except register.WriteOnceViolation as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "plain": str(exc),
                "field": "figure_id",
                "remedy": "Mint a fresh figure_id for the new score and retry.",
            },
        )
    return row.model_dump()


@router.get("/api/claims-validation")
def list_claims_validation() -> Dict[str, Any]:
    """EP-3 A-4 · list claims-validation rows. Empty at ship."""
    rows = claims_validation.read_all()
    return {
        "ship_state": "empty" if not rows else "populated",
        "count": len(rows),
        "rows": [r.model_dump() for r in rows],
        "never_a_gate_note": (
            "Doc 19B §19B.6: 'A-4 never becomes a gate by drift — its "
            "scope is validation and re-entry, and staying there is a "
            "condition of adoption, not a detail.' This surface is "
            "read-only lineage; nothing here blocks a build."
        ),
    }


@router.post("/api/claims-validation", status_code=201)
def post_claims_validation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """EP-3 · a parked idea returns with a three-arm result behind it."""
    try:
        row = ClaimsValidationRowV0.model_validate(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": "The claims-validation row could not be validated.",
                "field": "body",
                "remedy": (
                    "Provide claim_id, claim_kind ('reentry' or 'bakeoff'), "
                    "subject, exactly three arm names, opened_at."
                ),
                "detail": str(exc),
            },
        )
    try:
        claims_validation.append(row)
    except claims_validation.WriteOnceViolation as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "plain": str(exc),
                "field": "claim_id",
                "remedy": "Mint a fresh claim_id for the new attempt.",
            },
        )
    return row.model_dump()


# =====================================================================
# W11 D · CP-D0 · EP-4 mechanical ordering guard for terminal_test
# =====================================================================
# Owner directive verbatim (2026-08-26T~12:40Z · Batch 1 · reclass. 1):
#   'the evidence register and dual-judge protocol must exist before
#    the terminal test runs, or that test's verdict is single-judge
#    permanently — no retroactive fix once it's run.'
# ---------------------------------------------------------------------


@router.post("/api/evidence-register/precheck/terminal-test")
def post_precheck_terminal_test() -> Dict[str, Any]:
    """§EP-4 structural precondition check. 200 with receipt when the
    register carries a dual-judge terminal_test row; 422 with EP-4
    verbatim citation otherwise. The guard is a MEASUREMENT — reads
    disk each call, never cached."""
    from services.evidence_register.terminal_test_guard import (
        precheck_terminal_test_ready, TerminalTestGuardRefusal,
        EP4_VERBATIM, EP2_VERBATIM,
    )

    try:
        return precheck_terminal_test_ready()
    except TerminalTestGuardRefusal as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "terminal_test_precondition_unmet",
                "spec_ref": "Doc 19B §EP-4",
                "spec_verbatim": EP4_VERBATIM,
                "spec_verbatim_ep2": EP2_VERBATIM,
                "measurement": str(exc),
                "remedy": (
                    "Land a dual-judge EvidenceRegisterRowV0 for "
                    "named_site='terminal_test' via POST "
                    "/api/evidence-register before the terminal test "
                    "fires. The verdict cannot be retroactively fixed."
                ),
            },
        )

