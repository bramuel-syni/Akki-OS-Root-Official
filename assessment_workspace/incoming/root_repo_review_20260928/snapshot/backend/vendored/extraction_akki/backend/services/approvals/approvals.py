"""services.approvals.approvals — governance ceremony records R/W.

Doc 15 §17 SoD enforced service-side: approver_actor_id MUST differ
from proposed_by. Records: phase0/approval_records/{requests,decisions}/.
Append-only; one decision per request_id; refused double-decision.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from contracts.approval_request import ApprovalDecision_v0, ApprovalRequest_v0


_DEFAULT_DIR = "/app/assessment_workspace/phase0/approval_records"


def _dir() -> Path:
    return Path(os.environ.get("APPROVAL_RECORDS_DIR", _DEFAULT_DIR))


def _requests_dir() -> Path:
    return _dir() / "requests"


def _decisions_dir() -> Path:
    return _dir() / "decisions"


def register_request(payload: Dict[str, Any]) -> ApprovalRequest_v0:
    """Author + persist an ApprovalRequest_v0."""
    req = ApprovalRequest_v0(**payload)
    d = _requests_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{req.request_id}.json"
    if path.exists():
        raise ValueError(
            f"approval request {req.request_id!r} already on record. "
            f"Overwrite is a load-bearing conflict."
        )
    path.write_text(json.dumps(req.model_dump(), indent=2, ensure_ascii=False))
    return req


def load_requests() -> List[ApprovalRequest_v0]:
    d = _requests_dir()
    if not d.is_dir():
        return []
    return sorted(
        (ApprovalRequest_v0(**json.loads(p.read_text())) for p in d.glob("ar_*.json")),
        key=lambda r: r.request_id,
    )


def load_decisions() -> List[ApprovalDecision_v0]:
    d = _decisions_dir()
    if not d.is_dir():
        return []
    return sorted(
        (ApprovalDecision_v0(**json.loads(p.read_text())) for p in d.glob("ad_*.json")),
        key=lambda d_: d_.decision_id,
    )


def _find_request(request_id: str) -> ApprovalRequest_v0 | None:
    for r in load_requests():
        if r.request_id == request_id:
            return r
    return None


def _find_decision_for(request_id: str) -> ApprovalDecision_v0 | None:
    for d in load_decisions():
        if d.request_id == request_id:
            return d
    return None


def decide_request(payload: Dict[str, Any]) -> ApprovalDecision_v0:
    """Record a decision. Enforces:
    - request_id exists on record.
    - not already decided (idempotency).
    - SoD: approver != proposer.
    """
    decision = ApprovalDecision_v0(**payload)
    req = _find_request(decision.request_id)
    if req is None:
        raise ValueError(
            f"approval request {decision.request_id!r} not on record. "
            f"Register the request before deciding."
        )
    if _find_decision_for(decision.request_id) is not None:
        raise ValueError(
            f"request {decision.request_id!r} already decided. "
            f"Doc 15 §17: one decision per request; second decisions "
            f"are load-bearing conflicts."
        )
    if decision.approver_actor_id == req.proposed_by:
        raise ValueError(
            f"separation-of-duties violation: approver "
            f"{decision.approver_actor_id!r} equals proposer "
            f"{req.proposed_by!r}. Doc 15 §17."
        )
    d = _decisions_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{decision.decision_id}.json").write_text(
        json.dumps(decision.model_dump(), indent=2, ensure_ascii=False)
    )
    return decision
