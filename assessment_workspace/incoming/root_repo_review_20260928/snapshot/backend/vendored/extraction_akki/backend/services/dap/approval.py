"""W-DAP-STACK 2C · approval routing + controlled-operations kernel.

Canon anchors: DAP-Spec DAP-11, DAP-14, DAP-15, DAP-16, DAP-17.

C4 owner ruling 2026-09-13: DAP-R-2 approving-authority named person is
OPEN; land as ``DEFAULT-PENDING-OVERRIDE``. Production-grade close awaits
owner input.
"""

from __future__ import annotations

import datetime
import secrets
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# C4 marker · DAP-R-2 open per owner 2026-09-13
DAP_R2_APPROVING_AUTHORITY: str = "DEFAULT-PENDING-OVERRIDE"

# Operations that ALWAYS require approval regardless of `controlled` status
_ALWAYS_REQUIRE_APPROVAL = frozenset({"fine_tune_model", "develop_skills"})


class ApprovalRouting(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    request_id: str
    requesting_principal_id: str
    objective: str
    units_or_scope: List[str]
    why_each_controlled: Dict[str, str]
    terms_that_would_apply: str
    approving_authority_id: str  # may be DEFAULT-PENDING-OVERRIDE
    status: str  # pending | approved | refused | expired
    executes: bool = False
    stated_reason: Optional[str] = None
    routed_at_iso: str


class ApprovalDecisionRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    request_id: str
    decision: str  # approved | refused
    stated_reason: str
    deciding_authority_id: str
    decided_at_iso: str


class StandingApprovalGrant(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    grant_id: str
    party_principal_id: str
    scope: str
    window_from_iso: str
    window_to_iso: str
    includes_controlled_units_named: List[str]
    approving_authority_id: str
    active: bool = True


_ROUTES: Dict[str, ApprovalRouting] = {}
_DECISIONS: Dict[str, ApprovalDecisionRecord] = {}
_STANDINGS: Dict[str, StandingApprovalGrant] = {}


def requires_approval(*, operation: str, controlled: bool) -> bool:
    """DAP-16: fine-tune / develop-skills ALWAYS require approval;
    controlled raw-download ALWAYS requires approval; uncontrolled
    raw-download is estate-owner-configurable (DAP-22 · not decided here)."""
    if operation in _ALWAYS_REQUIRE_APPROVAL:
        return True
    if operation == "download_raw_data" and controlled:
        return True
    if controlled:
        return True
    return False


def route_for_approval(
    *,
    requesting_principal_id: str,
    objective: str,
    units_or_scope: List[str],
    why_each_controlled: Dict[str, str],
    terms_that_would_apply: str,
    approving_authority_id: str,
) -> ApprovalRouting:
    """DAP-14: route a controlled request to the named approving authority.
    The request does not execute while pending."""
    routing = ApprovalRouting(
        request_id=f"apr_{secrets.token_hex(6)}",
        requesting_principal_id=requesting_principal_id,
        objective=objective,
        units_or_scope=list(units_or_scope),
        why_each_controlled=dict(why_each_controlled),
        terms_that_would_apply=terms_that_would_apply,
        approving_authority_id=approving_authority_id,
        status="pending",
        executes=False,
        routed_at_iso=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    _ROUTES[routing.request_id] = routing
    return routing


def record_decision(
    *,
    request_id: str,
    decision: str,
    stated_reason: str,
    deciding_authority_id: str,
) -> ApprovalDecisionRecord:
    """DAP-15: decisions recorded with deciding authority identity, decision,
    and stated reason."""
    if decision not in {"approved", "refused"}:
        raise ValueError("DAP-15: decision must be 'approved' or 'refused'")
    if not stated_reason.strip():
        raise ValueError("DAP-15: a refusal / approval MUST state a reason")
    record = ApprovalDecisionRecord(
        request_id=request_id,
        decision=decision,
        stated_reason=stated_reason,
        deciding_authority_id=deciding_authority_id,
        decided_at_iso=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    _DECISIONS[request_id] = record
    # Flip the routing (immutable, so we replace):
    r = _ROUTES[request_id]
    _ROUTES[request_id] = r.model_copy(update={
        "status": decision,
        "stated_reason": stated_reason,
        "executes": decision == "approved",
    })
    return record


def expire_if_unanswered(request_id: str) -> ApprovalRouting:
    """DAP-15 tail: unanswered request expires unexecuted."""
    r = _ROUTES[request_id]
    expired = r.model_copy(update={"status": "expired", "executes": False})
    _ROUTES[request_id] = expired
    return expired


def grant_standing_approval(
    *,
    party_principal_id: str,
    scope: str,
    window_from_iso: str,
    window_to_iso: str,
    includes_controlled_units_named: List[str],
    approving_authority_id: str,
) -> StandingApprovalGrant:
    """DAP-17: standing approval — named party, named scope, stated window.
    Revocable single-act.  MUST NOT cover controlled units unless named."""
    grant = StandingApprovalGrant(
        grant_id=f"stg_{secrets.token_hex(6)}",
        party_principal_id=party_principal_id,
        scope=scope,
        window_from_iso=window_from_iso,
        window_to_iso=window_to_iso,
        includes_controlled_units_named=list(includes_controlled_units_named),
        approving_authority_id=approving_authority_id,
        active=True,
    )
    _STANDINGS[grant.grant_id] = grant
    return grant


def revoke_standing_approval(grant_id: str) -> None:
    """DAP-17 tail: revocable in one act, immediate effect."""
    if grant_id in _STANDINGS:
        _STANDINGS[grant_id] = _STANDINGS[grant_id].model_copy(update={"active": False})


def is_standing_approval_valid(
    *,
    party_principal_id: str,
    operation: str,
    controlled_units_in_request: List[str],
    at_iso: str,
) -> bool:
    for g in _STANDINGS.values():
        if not g.active:
            continue
        if g.party_principal_id != party_principal_id:
            continue
        if operation != g.scope:
            continue
        if not (g.window_from_iso <= at_iso <= g.window_to_iso):
            continue
        # DAP-17: MUST NOT cover controlled unless named
        for u in controlled_units_in_request:
            if u not in g.includes_controlled_units_named:
                return False
        return True
    return False


def reset_state() -> None:
    """Test-only helper."""
    _ROUTES.clear()
    _DECISIONS.clear()
    _STANDINGS.clear()
