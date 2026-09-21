"""services.rules_service.ceremony — W-M2-SW2.

Rules-Service ceremony (change-control ceremony · Doc-0 Attr-9 rolled
in per BUILD_STATUS §2 row 4i).

Rules-Service R-1 (DEFAULT · Ratification_Record_v1 Table 2):
    countdown = 48h system-ordinary / 7d system-TCB.

Rules-Service R-2 (OPEN · Ratification_Record_v1 Table 2):
    second-signatory named role.  Landed here as
    DEFAULT-PENDING-OVERRIDE marker.

Rules-Service R-3 (RATIFIED · Ratification_Record_v1 Table 2):
    witness = the same witness the Watch uses.  WITNESS_IDENTITY_SOURCE
    == 'the_watch'.

Rules-Service R-4 (RATIFIED · Ratification_Record_v1 Table 2):
    v1 business-type taxonomy is the finite named set.

Canon-1 §4.10: verdicts are never curated; only an Amendment (via this
ceremony) retires a verdict.

Ceremony flow:
    1. RuleFlipRequest submitted (rule_id, business_type,
       target_enforcement_class, requester_id, submitted_at)
    2. start_rule_flip() -> RuleFlipCeremony (countdown starts)
    3. attempt_apply_rule_flip(ceremony, witness_id, second_signatory_id,
       now) -> {applied: bool, basis: 'rules_service', ...}

Fail-closed on any missing gate (countdown / witness / signatory /
business-type).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from services.rulings import default_class_constants as _dcc
from services.rules_service.rule_registry import (
    RuleRecord,
    RuleIdCollision,
    get_rule_registry,
)


# Bound to the ledger constant — silent divergence forbidden by test.
SYSTEM_ORDINARY_COUNTDOWN_HOURS: Final[int] = (
    _dcc.RULES_SERVICE_COUNTDOWN_SYSTEM_ORDINARY_HOURS
)
SYSTEM_TCB_COUNTDOWN_DAYS: Final[int] = (
    _dcc.RULES_SERVICE_COUNTDOWN_SYSTEM_TCB_DAYS
)


# R-3 witness identity source (RATIFIED).
WITNESS_IDENTITY_SOURCE: Final[str] = "the_watch"


# R-2 second-signatory pending marker (OPEN owner-input).
SECOND_SIGNATORY_ROLE_PENDING_OVERRIDE: Final[str] = "PENDING-OVERRIDE"


# R-4 v1 business-type taxonomy.
BUSINESS_TYPE_TAXONOMY: Final[Tuple[str, ...]] = (
    "system_ordinary",
    "system_tcb",
    "amendment",
)


class CountdownNotElapsed(RuntimeError):
    """R-1: the ceremony countdown has not elapsed yet."""


class WitnessMismatch(RuntimeError):
    """R-3: witness identity source is not `the_watch`."""


class SecondSignatoryMissing(RuntimeError):
    """R-2: second-signatory identity was not supplied."""


class BusinessTypeUnknown(ValueError):
    """R-4: business type is not in v1 taxonomy."""


class RuleFlipRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    rule_id: str = Field(min_length=3)
    business_type: str
    target_enforcement_class: str = Field(min_length=1)
    requester_id: str = Field(min_length=1)
    submitted_at: datetime

    @field_validator("business_type")
    @classmethod
    def _bt(cls, v: str) -> str:
        if v not in BUSINESS_TYPE_TAXONOMY:
            raise BusinessTypeUnknown(
                f"business_type must be one of "
                f"{BUSINESS_TYPE_TAXONOMY}; got {v!r}"
            )
        return v


class RuleFlipCeremony(BaseModel):
    """A single in-flight ceremony.  Immutable; ceremony state
    transitions are represented by new records, not mutation."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    request: RuleFlipRequest
    started_at: datetime


def start_rule_flip(request: RuleFlipRequest) -> RuleFlipCeremony:
    """Begin the ceremony.  The countdown starts at `submitted_at`."""
    return RuleFlipCeremony(
        request=request,
        started_at=request.submitted_at,
    )


def _countdown_delta_for(business_type: str) -> timedelta:
    if business_type == "system_tcb":
        return timedelta(days=SYSTEM_TCB_COUNTDOWN_DAYS)
    if business_type == "amendment":
        # Amendments piggy-back the system-TCB countdown (conservative).
        return timedelta(days=SYSTEM_TCB_COUNTDOWN_DAYS)
    # system_ordinary
    return timedelta(hours=SYSTEM_ORDINARY_COUNTDOWN_HOURS)


def attempt_apply_rule_flip(
    ceremony: RuleFlipCeremony,
    *,
    witness_id: str,
    second_signatory_id: str,
    now: datetime | None = None,
) -> dict:
    """Attempt to close the ceremony and apply the rule flip.

    Fail-closed on any missing gate.  On success, appends a new
    RuleRecord to the singleton registry (Canon-3 §22 additive) and
    returns {applied: True, basis: 'rules_service'}.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    # R-1 · countdown
    required = _countdown_delta_for(ceremony.request.business_type)
    elapsed = now - ceremony.started_at
    if elapsed < required:
        raise CountdownNotElapsed(
            f"countdown {required} required; only {elapsed} elapsed"
        )

    # R-3 · witness identity source
    if witness_id != WITNESS_IDENTITY_SOURCE:
        raise WitnessMismatch(
            f"witness_id must equal WITNESS_IDENTITY_SOURCE "
            f"({WITNESS_IDENTITY_SOURCE!r}); got {witness_id!r}"
        )

    # R-2 · second-signatory identity supplied
    if not second_signatory_id or not second_signatory_id.strip():
        raise SecondSignatoryMissing(
            "second_signatory_id must be supplied; R-2 role is "
            f"{SECOND_SIGNATORY_ROLE_PENDING_OVERRIDE!r} awaiting owner"
        )

    # Apply: append new rule (or supersession) to the registry.
    registry = get_rule_registry()
    new_rec = RuleRecord(
        rule_id=ceremony.request.rule_id,
        source_citation=(
            f"Rules-Service ceremony · requester={ceremony.request.requester_id} · "
            f"witness={witness_id} · signatory={second_signatory_id} · "
            f"business_type={ceremony.request.business_type}"
        ),
        scope="rules_service.ceremony_applied",
        enforcement_class=ceremony.request.target_enforcement_class,
    )
    try:
        registry.append(new_rec)
    except RuleIdCollision:
        # Ceremony would attempt supersession — Canon-3 §22 requires a
        # NEW id.  Refuse this application; the requester must resubmit
        # under a new (supersession) id.
        raise RuleIdCollision(
            f"ceremony application refused: rule_id {new_rec.rule_id!r} "
            f"already registered.  Canon-3 §22 supersession requires a "
            f"NEW id citing the prior."
        )

    return {
        "applied": True,
        "basis": "rules_service",
        "rule_id": new_rec.rule_id,
        "witness_id": witness_id,
        "second_signatory_id": second_signatory_id,
        "business_type": ceremony.request.business_type,
    }


__all__ = [
    "SYSTEM_ORDINARY_COUNTDOWN_HOURS",
    "SYSTEM_TCB_COUNTDOWN_DAYS",
    "WITNESS_IDENTITY_SOURCE",
    "SECOND_SIGNATORY_ROLE_PENDING_OVERRIDE",
    "BUSINESS_TYPE_TAXONOMY",
    "CountdownNotElapsed",
    "WitnessMismatch",
    "SecondSignatoryMissing",
    "BusinessTypeUnknown",
    "RuleFlipRequest",
    "RuleFlipCeremony",
    "start_rule_flip",
    "attempt_apply_rule_flip",
]
