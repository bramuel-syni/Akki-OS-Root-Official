"""services.approvals.reserved_decisions — Canon 8 §19 reserved-decisions
panel (W10 CP4).

Canon 8 §19: reserved decisions are `promote_containment` ·
`extend_expiry` · `sign_de_mark` · `resolve_authority_disagreement` ·
`cancel_ceremony_in_countdown`. Each requires HUMAN AUTHORSHIP.

Canon 8 §32.6: NO reserved-decision is executed by machine. This
module RECORDS reserved requests + provides a read-side lister for
pending requests. It does NOT execute any side-effect on approval.
Operator authors the next call after ApprovalDecision.verdict ==
'approved' (extend_expiry becomes a start_containment with a new
containment_id; sign_de_mark becomes a Mkono action_class de_mark_signed;
etc.).

R3 (2026-08-26T04:20Z): reserved_decision_kind is a closed Literal
enum on ApprovalRequest_v0 · no free-text kinds.
"""
from __future__ import annotations

from typing import Any, Dict, List

from contracts.approval_request import ApprovalRequest_v0
from services.approvals.approvals import (
    load_decisions, load_requests, register_request,
)


def submit_reserved_request(payload: Dict[str, Any]) -> ApprovalRequest_v0:
    """Submit a reserved-decision request. Refuses if:
      - kind != 'generic' (reserved kinds are generic-only).
      - reserved_decision_kind is None (use approvals.register_request
        for non-reserved generic requests).

    Delegates to approvals.register_request; the reserved discipline
    is a wrapper that enforces the kind='generic' + non-None
    reserved_decision_kind pairing at submit time.
    """
    kind = payload.get("kind")
    reserved_decision_kind = payload.get("reserved_decision_kind")
    if kind != "generic":
        raise ValueError(
            f"reserved-decision kind must accompany kind='generic'; got "
            f"kind={kind!r}. Canon 8 §19: reserved kinds are the 5 named "
            f"decisions; they are 'generic' at the approval-fabric level."
        )
    if reserved_decision_kind is None:
        raise ValueError(
            f"reserved_decision_kind required for reserved requests. "
            f"Use approvals.register_request for non-reserved generic "
            f"requests."
        )
    return register_request(payload)


def list_pending_reserved() -> List[ApprovalRequest_v0]:
    """List reserved requests with no decision on record yet.
    Read-side lister · does not execute anything (§32.6)."""
    decided = {d.request_id for d in load_decisions()}
    return [
        r for r in load_requests()
        if r.reserved_decision_kind is not None
        and r.request_id not in decided
    ]


def list_all_reserved() -> List[ApprovalRequest_v0]:
    """List every reserved request on record (pending + decided).
    Read-side lister · panel view."""
    return [
        r for r in load_requests()
        if r.reserved_decision_kind is not None
    ]
