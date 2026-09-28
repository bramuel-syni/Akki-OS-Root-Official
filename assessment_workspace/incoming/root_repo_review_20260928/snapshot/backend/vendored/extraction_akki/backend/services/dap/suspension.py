"""W-DAP-STACK 2F · DAP-27 suspension + revocation.

Verbatim DAP-27 [Doc 3 A5.3 stop-never-delete]: 'An estate owner MUST
be able to suspend a party — halting every in-flight and future
operation for that party in one act — and to revoke its admission.
Suspension is immediate; in-flight jobs stop and are recorded as
stopped, not silently completed.'
"""

from __future__ import annotations

import datetime
from typing import Dict, List, Tuple

from pydantic import BaseModel, ConfigDict


class SuspensionAct(BaseModel):
    """DAP-27: single-act suspension.  Carries the list of in-flight
    jobs stopped by this act."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    reason: str
    at_iso: str
    in_flight_job_ids_stopped: Tuple[str, ...]


class AdmissionRevocation(BaseModel):
    """DAP-27: revoke admission (distinct from suspend)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    reason: str
    at_iso: str


_in_flight: Dict[str, List[str]] = {}          # party_id -> [job_id, ...]
_stopped: Dict[str, List[Dict]] = {}           # party_id -> [{job_id, status, at_iso}, ...]
_suspended: Dict[str, SuspensionAct] = {}
_revoked: Dict[str, AdmissionRevocation] = {}


def _now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


def start_in_flight_job(*, party_id: str, job_id: str) -> str:
    """Register an in-flight job; refuses if the party is suspended or
    revoked (DAP-27: 'halting every ... future operation ... in one
    act')."""
    if party_id in _suspended:
        raise PermissionError(
            f"DAP-27: party {party_id!r} is suspended; future operations refused."
        )
    if party_id in _revoked:
        raise PermissionError(
            f"DAP-27: party {party_id!r} admission revoked; future operations refused."
        )
    _in_flight.setdefault(party_id, []).append(job_id)
    return job_id


def suspend_party(*, party_id: str, reason: str) -> SuspensionAct:
    """DAP-27: one-act suspension.  Stops all in-flight jobs immediately
    and records each as `stopped` (not silently `completed`)."""
    stopped_ids = tuple(_in_flight.get(party_id, []))
    at = _now()
    for jid in stopped_ids:
        _stopped.setdefault(party_id, []).append({
            "job_id": jid, "status": "stopped", "at_iso": at,
        })
    _in_flight[party_id] = []
    act = SuspensionAct(
        party_id=party_id, reason=reason, at_iso=at,
        in_flight_job_ids_stopped=stopped_ids,
    )
    _suspended[party_id] = act
    return act


def revoke_admission(*, party_id: str, reason: str) -> AdmissionRevocation:
    """DAP-27: revoke admission (distinct act from suspend)."""
    rev = AdmissionRevocation(
        party_id=party_id, reason=reason, at_iso=_now(),
    )
    _revoked[party_id] = rev
    return rev


def is_suspended(*, party_id: str) -> bool:
    return party_id in _suspended


def list_stopped_in_flight_jobs(*, party_id: str) -> List[Dict]:
    return list(_stopped.get(party_id, []))


def reset_state() -> None:
    """Test-only helper."""
    _in_flight.clear()
    _stopped.clear()
    _suspended.clear()
    _revoked.clear()
