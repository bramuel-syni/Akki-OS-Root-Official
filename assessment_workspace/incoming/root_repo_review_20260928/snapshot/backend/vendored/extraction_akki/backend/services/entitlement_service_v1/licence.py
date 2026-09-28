"""services.entitlement_service_v1.licence · Licence object surface (§3 ENT-5..8).

ENT-5 (§3 verbatim): "A licence is a terms object on exactly one organisation
principal. It is created by the estate owner's admission act (PRIN-2) and
resolves at DAP-22's first level, per-party agreement, ahead of custody-class
and estate defaults." [PRIN-1, PRIN-2, DAP-22]

ENT-6 (§3 verbatim): "A licence carries, as required fields: plan identifier;
seat count; Compute dial; Frontier dial; credits per seat per period;
pooled-credits flag; seat soft limit; organisation ceiling; period; renewal
date; status ∈ {active, suspended, expired}. A licence missing any required
field does not resolve, and a call under it refuses." [FP-2]

ENT-7 (§3 verbatim): "A change to any licence field takes effect through the
Rules Service ceremony at the ordinary tier and applies prospectively only.
It MUST NOT alter the terms identifier cited on any receipt already issued."
[DAP-26, RBM-8]

ENT-8 (§3 verbatim): "Suspension is a status on the licence, set by the
estate owner in one act, refusing every subsequent call under it immediately.
Suspension does not touch receipts, credits already recorded, or the catalog."
[DAP-27]

R-31 (owner sprint order verbatim): "seats-as-default with separate agent
count at organisation size" — Licence.agent_count is Optional; None at
small orgs, integer at organisation-size upgrades.

SO §3.10-α · Licence is a frozen pydantic BaseModel with extra=forbid.
Model name starts with "Licence" per ENT-49 four-allowed-shapes discipline.
"""
from __future__ import annotations

from typing import Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field


# ENT-6 closed status enum · 3-tuple exactly per spec verbatim
LICENCE_STATUS_ACTIVE: Literal["active"] = "active"
LICENCE_STATUS_SUSPENDED: Literal["suspended"] = "suspended"
LICENCE_STATUS_EXPIRED: Literal["expired"] = "expired"
_LICENCE_STATUSES: Tuple[str, str, str] = ("active", "suspended", "expired")


# R-26..R-30 DEFAULT-class values tagged pending owner ratification per
# confirmed sprint order verbatim. Constant names carry
# `_DEFAULT_PENDING_OWNER_RATIFICATION` suffix to make grep-visible that
# the numeric is not-yet-a-rule.
R_26_ROLLOVER_PERIODS_DEFAULT_PENDING_OWNER_RATIFICATION: int = 1
R_27_SEAT_SOFT_LIMIT_FRACTION_DEFAULT_PENDING_OWNER_RATIFICATION: float = 0.80
R_29_KEY_SCOPE_DEFAULT_PENDING_OWNER_RATIFICATION: Literal["organisation"] = "organisation"


class LicenceRefusal(RuntimeError):
    """FP-2 fail-closed refusal on a licence that does not resolve.

    Raised by chokepoint_resolver.resolve() when the licence is missing a
    required field, suspended, expired, or otherwise fails to satisfy the
    resolution chain (ENT-16 verbatim: 'Any link that does not resolve
    refuses the call.').
    """


class Licence(BaseModel):
    """ENT-5/6 · Licence object on exactly one organisation principal.

    Attached to a single `PrincipalV1` of `PrincipalKind.organisation`
    (sealed principal_v1 contract). All ENT-6 required fields present or
    the licence does not resolve.

    R-31 note (agent_count): Optional. None means agents occupy seats
    (ENT-42 default). Integer means separate agent count field at
    organisation size (R-31 owner sprint order verbatim).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # ENT-6 required fields · verbatim order from spec
    plan_identifier: str = Field(..., min_length=1, description="ENT-6 plan identifier · required.")
    organisation_principal_id: str = Field(..., min_length=1, description="ENT-5 organisation PRIN-1 identifier · required.")
    seat_count: int = Field(..., ge=1, description="ENT-6 seat count · required · at least 1.")
    compute_dial: Literal["managed", "yours"] = Field(..., description="ENT-6 Compute dial · closed 2-tuple.")
    frontier_dial: Literal["managed", "your_keys"] = Field(..., description="ENT-6 Frontier dial · closed 2-tuple.")
    credits_per_seat_per_period: int = Field(..., ge=0, description="ENT-6 credits allowance · required.")
    pooled_credits_flag: bool = Field(..., description="ENT-6 pooled-credits flag · required.")
    seat_soft_limit: int = Field(..., ge=0, description="ENT-6 seat soft limit · required · warns at R-27 threshold does not refuse.")
    organisation_ceiling: int = Field(..., ge=0, description="ENT-6 organisation ceiling · required · refuses on hit.")
    period: str = Field(..., min_length=1, description="ENT-6 period · required · e.g., 'month'.")
    renewal_date: str = Field(..., min_length=1, description="ENT-6 renewal date · ISO-8601 UTC string.")
    status: Literal["active", "suspended", "expired"] = Field(..., description="ENT-6 status · closed 3-tuple.")

    # ENT-7 terms identifier · cited on receipts · MUST NOT change on receipt-already-issued
    terms_identifier: str = Field(..., min_length=1, description="ENT-7 terms identifier · immutable on receipts already issued.")

    # R-31 optional agent count (Optional per sprint order verbatim)
    agent_count: Optional[int] = Field(default=None, ge=0, description="R-31 · separate agent count at organisation size (None means agents occupy seats per ENT-42).")
