"""W-DAP-STACK 2D · commissioning + assistance-chat boundary.

Canon anchors: DAP-Spec DAP-18, DAP-19, DAP-20.
"""

from __future__ import annotations

import datetime
import secrets
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict


# §7 composition table (verbatim) — DAP composes, does NOT execute.
_OPERATION_TO_ENGINE = {
    "browse_estate": "mtafiti",
    "connect_workspace": "synisense",
    "processed_intelligence": "solva",
    "fine_tune_model": "targeta",
    "develop_skills": "targeta",  # via callable-skill-files Doc 18
    "download_raw_data": "outer_gate",  # Promise #25 · not ordinary crossing
}


class CommissionedJob(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    job_id: str
    principal_id: str
    objective: str
    operation: str
    estate_id: str
    frozen: bool
    commissioned_at_iso: str


class JobRouting(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    job_id: str
    governing_engine: str


_JOBS: Dict[str, CommissionedJob] = {}


def commission_job(
    *,
    principal_id: str,
    objective: str,
    operation: str,
    estate_id: str,
) -> CommissionedJob:
    """DAP-18: commission a job with a frozen objective."""
    job = CommissionedJob(
        job_id=f"job_{secrets.token_hex(6)}",
        principal_id=principal_id,
        objective=objective,
        operation=operation,
        estate_id=estate_id,
        frozen=True,
        commissioned_at_iso=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    _JOBS[job.job_id] = job
    return job


def widen_scope_forbidden_after_commission(
    *,
    job_id: str,
    wider_objective: str,
    source: str,
) -> None:
    """DAP-18 tail: any path (including assistance chat) that attempts to
    widen a commissioned job's scope MUST refuse.  A wider scope is a new
    job."""
    _ = wider_objective  # captured for audit trail if needed
    raise PermissionError(
        f"DAP-18: attempt to widen scope of commissioned job {job_id!r} via "
        f"{source!r} refused.  A wider scope is a new job."
    )


def route_job_to_engine(job_id: str) -> JobRouting:
    """DAP-19: every job routes to the engine that governs its operation
    per §4 and MUST NOT execute through any other path."""
    job = _JOBS[job_id]
    engine = _OPERATION_TO_ENGINE.get(job.operation)
    if engine is None:
        raise ValueError(f"DAP-19: operation {job.operation!r} has no §4 governing engine")
    if engine == "dap":  # defensive — DAP holds no extraction logic of its own
        raise RuntimeError("DAP-19 violation: DAP composes; it does not execute")
    return JobRouting(job_id=job_id, governing_engine=engine)


class AssistanceChatBoundary:
    """DAP-20 (verbatim): 'It proposes; the gates decide.'

    Enumerates the pre-commission verbs the assistance chat MAY perform,
    and the post-commission verbs it MUST NOT.
    """

    _PRE_COMMISSION_PERMITTED = frozenset({
        "propose_objective", "propose_scope", "explain_terms",
    })
    _FORBIDDEN = frozenset({
        "approve", "widen_scope", "decide_gate",
    })

    def may(self, verb: str) -> bool:
        if verb in self._FORBIDDEN:
            return False
        return verb in self._PRE_COMMISSION_PERMITTED


def reset_state() -> None:
    """Test-only helper."""
    _JOBS.clear()
