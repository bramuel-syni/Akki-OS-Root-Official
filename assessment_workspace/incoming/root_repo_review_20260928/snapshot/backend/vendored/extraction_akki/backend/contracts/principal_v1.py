"""contracts.principal_v1 — Principal Model Spec v1 · closed-schema contract.

CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9 · SO §3.10-α closed-schema discipline.

Owner ruling 2026-09-20T~09:48Z verbatim: 'PRINCIPAL MODEL WAVE (Step 9):
13 PRIN requirements PRIN-1..PRIN-13 each in verbatim docstring per SO §2.5.'

Spec source (hash-pinned):
    custody/owner_drops/20260920T0856Z/Principal_Model_Spec_v1.docx
    sha256 056caa00b5eb8c4d75abe1e2d2653cee590682e946c87a1bbf43693cb7c8787c

Canon anchors:
    - SO §3.10-α · frozen=True + extra='forbid' from day one (α-gap discipline
      landed at CP-ALPHA-GAP-HARDENING seal 8c944ee7/b8225536/32fe6df2).
    - Northena Promise #32 · objective-freeze mechanism (PRIN-4 anchor).
    - DAP-1, DAP-2, DAP-3, DAP-5 · spec bindings on the three principal kinds
      and the trust-domain boundary.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PrincipalKind(str, Enum):
    """PRIN-1 verbatim: 'three principal kinds ... organisation ... individual
    ... agent'. Ordering preserved from spec §2 paragraph 1.
    """

    ORGANISATION = "organisation"
    INDIVIDUAL = "individual"
    AGENT = "agent"


class PrincipalV1(BaseModel):
    """PRIN-1 + PRIN-3 + PRIN-4 · immutable principal contract.

    Fields carry:
    - PRIN-1 (organisation): legal identity + trust-domain identifier +
      admission-time mandate.
    - PRIN-1 (individual/agent): parent organisation reference (MUST
      reference the organisation it acts under; MUST NOT exist without one).
    - PRIN-3: behavioural_signature_state present from admission
      (not deferred).
    - PRIN-4: admission_time_mandate frozen at admission per Northena
      Promise #32 objective-freeze mechanism.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    principal_id: str = Field(..., description="Opaque platform-issued handle.")
    kind: PrincipalKind
    legal_identity: str = Field(
        ...,
        description=(
            "For ORGANISATION: DAP-1's legal identity (registered legal "
            "name). For INDIVIDUAL/AGENT: display name of the principal."
        ),
    )
    trust_domain_identifier: str = Field(
        ...,
        description=(
            "PRIN-7 + PRIN-9 anchor. The trust-domain boundary a credential "
            "is bound to at issuance; the domain no estate identifier "
            "resolves into by default."
        ),
    )
    admission_time_mandate: str = Field(
        ...,
        description=(
            "PRIN-4 verbatim: 'Mandate is immutable once frozen at "
            "admission ... Changing what a principal is admitted to do "
            "is a new admission event, not an edit to the old one.'"
        ),
    )
    behavioural_signature_state: str = Field(
        ...,
        description=(
            "PRIN-3 verbatim: 'Every principal carries a "
            "behavioural-signature state under the Watch, present from "
            "its first request.'"
        ),
    )
    parent_organisation_id: Optional[str] = Field(
        default=None,
        description=(
            "PRIN-1 verbatim: 'An individual or agent MUST reference the "
            "organisation it acts under; it MUST NOT exist without one.' "
            "None only for kind=ORGANISATION."
        ),
    )
    autonomy_scope: Optional[str] = Field(
        default=None,
        description=(
            "PRIN-1 (agent) verbatim: 'an autonomous non-human principal "
            "... carrying its own stated scope of autonomy'. None for "
            "ORGANISATION and INDIVIDUAL kinds."
        ),
    )
    admit_authority: bool = Field(
        default=False,
        description=(
            "PRIN-2 verbatim: 'An individual or agent is admitted only "
            "by a principal already holding authority to admit under its "
            "own organisation's terms.' True only for organisation-level "
            "principals admitted by the estate owner's named authority."
        ),
    )
    suspended: bool = Field(
        default=False,
        description=(
            "DAP-27 acceptance unblock: 'suspend a party' is a state on "
            "the principal store (spec §6 verbatim)."
        ),
    )
