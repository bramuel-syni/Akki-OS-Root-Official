"""contracts/dap.py — W-DAP-STACK contracts (shared across sub-waves 2A..2H).

DAP-Spec `dap_backend_spec_v1` (opened first-hand this session).  DAP owns
no invariant of its own (DAP-Spec §7): every guarantee it makes is a
guarantee of a component it composes.

R-C1 marker (this module):
  R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE = True — mirrors the
  W-REGISTRY-EXTENSION-G3 marker.  DAP-14 controlled-unit
  determination falls back to custody class alone (DAP-Spec §8
  dependency table).  Silent flip forbidden.

R-C2 marker: metered records carry `au_3b_defensible=False` on their
receipt until Doc-0 G-8 (`Security_Promise_Set_Amendments.docx`
Amendment 3) closes.  Silent flip forbidden.

DPO-1 linkage note (per owner directive this session):
  The `controlled` custody-class value is a DEFAULT-class WORKING
  value.  Its authoritative resolution is DAP R-1 (§10, pending owner
  ratification) — NOT Document 4's enum.  When DAP R-1 ratifies,
  `controlled` aligns to it and any change is a CEREMONY change per
  Rules Service, not a silent edit.  See DAP-14 mechanism for the
  binding site of this linkage.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field


# --- R-C1 marker mirror for DAP surface -----------------------------
R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE: bool = True


# --- 2A · External-Party Principal (DAP-1..4) -----------------------
class GovernancePosture(str, Enum):
    """DAP-1: the party's declared governance posture at admission."""
    RESEARCH = "research"
    COMMERCIAL = "commercial"
    REGULATORY = "regulatory"
    AI_LAB = "ai_lab"


class PartyPrincipalKind(str, Enum):
    """DAP-2/DAP-3: party principal is a named individual OR a registered agent."""
    INDIVIDUAL = "individual"
    AGENT = "agent"


class ExternalPartyPrincipal(BaseModel):
    """DAP-1 verbatim: 'organisation-level principal carrying: legal
    identity; declared governance posture; the terms it is admitted
    under; its trust domain identifier; and an admission-time mandate.'"""

    model_config = ConfigDict(extra="forbid", frozen=True)

    legal_identity: str = Field(..., description="Registered legal name.")
    governance_posture: GovernancePosture
    terms_id: str = Field(..., description="Terms under which admitted.")
    trust_domain_id: str = Field(..., description="DAP-5 trust-domain identifier.")
    admission_mandate: str = Field(..., description="What it came to do.")


class PartyPrincipal(BaseModel):
    """DAP-2 verbatim: 'Every request carries a party principal — a
    named individual or a registered agent — with its own mandate,
    mark state, and behavioural signature under the Watch.'"""

    model_config = ConfigDict(extra="forbid", frozen=True)

    principal_id: str
    kind: PartyPrincipalKind
    mandate: str = Field(..., description="Own mandate, separate from operator.")
    parent_org_id: str = Field(..., description="Under-organisation reference (DAP-1).")
    autonomy_scope: Optional[str] = Field(
        default=None,
        description=(
            "DAP-3: for AGENT principals, MUST carry stated scope of "
            "autonomy.  For INDIVIDUAL principals, None."
        ),
    )


# --- Cumulative history (DAP-4 anchor) ------------------------------
class CumulativeHistoryEntry(BaseModel):
    """DAP-24: cumulative extraction history is a first-class,
    queryable record.  DAP-4 slow-play detection reads it as
    aggregate, not per-request."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    operation: str
    scope_signature: str = Field(
        ...,
        description="Deterministic signature of what was accessed for aggregate reconstruction check.",
    )
    quantity: int
    terms_id: str
    timestamp_iso: str = Field(
        ...,
        description=(
            "R-C2: timestamp not defensible under AU-3(b) until "
            "Doc-0 G-8 closes."
        ),
    )


# --- 2B · Trust domain + API keys (DAP-5, DAP-13) -------------------
class ApiKeyIssueReceipt(BaseModel):
    """DAP-13: keys issued per party principal, revocable single-act,
    stated lifetime.  Key material is NEVER written to any record."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    principal_id: str
    key_id: str = Field(..., description="Opaque handle to the key.  Key material is NOT stored here.")
    lifetime_seconds: int = Field(..., ge=1, description="§10 R-4 parked; lifetime STATED.")
    revocable_in_single_act: bool = Field(default=True)


class TrustDomainCrossingAttempt(BaseModel):
    """DAP-5: no identifier resolution across trust-domain boundary
    except through a permitted §4 operation.  Attempts are recorded."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_trust_domain_id: str
    estate_trust_domain_id: str
    attempted_unit_id: str
    permitted_operation: Optional[str] = Field(
        default=None,
        description="If None, the crossing is refused and recorded.",
    )


# --- 2C · Crossing profile (DAP-6..11) -----------------------------
class CrossingProfile(BaseModel):
    """DAP-Spec §4 spine: six operations, six governance profiles."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operation: str
    what_enters: str
    what_leaves: str
    governing_gate: str
    approval_rule: str
    receipted: str


# --- 2D · Approval + spend (DAP-14..17, DAP-23) ---------------------
class ControlledDeterminationBasis(str, Enum):
    """Owner directive (this session): every DAP-14 determination
    under R-C1 MUST carry its basis on its own record.  Once the
    Rules Service lands, RULES_SERVICE becomes the value; until then,
    CUSTODY_CLASS_FALLBACK — flip-forbidden invariant."""

    CUSTODY_CLASS_FALLBACK = "custody_class_fallback"
    RULES_SERVICE = "rules_service"


class ControlledDetermination(BaseModel):
    """DAP-14 record: carries the reason a request is controlled and
    the BASIS on which controlled-ness was determined.  Owner directive:
    'never silently downgraded and served' — a determination on custody
    class alone is a DOWNGRADED determination; its record says so.

    DPO-1 linkage: the `controlled` custody-class value is a DEFAULT-class
    WORKING value; its authoritative resolution is DAP R-1 (§10, pending
    ratification).  When DAP R-1 ratifies, this record's `controlled`
    aligns to it and any change is a CEREMONY change (Rules Service),
    not a silent edit.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    request_id: str
    is_controlled: bool
    reason: str = Field(..., description="Why each unit is controlled.")
    determination_basis: ControlledDeterminationBasis = Field(
        default=ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK,
        description=(
            "Owner-ruling this session: silent flip forbidden.  "
            "CUSTODY_CLASS_FALLBACK is the only permitted value until "
            "Rules Service ratification (DAP-Spec §8 dependency)."
        ),
    )


class ApprovalDecision(BaseModel):
    """DAP-15: identity, decision, reason.  Silence != approval."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    authority_id: str
    decision: str  # 'approved' | 'refused' | 'expired'
    reason: str


class StandingApproval(BaseModel):
    """DAP-17: named party, named scope, stated window.  MUST NOT
    cover controlled units unless it names them explicitly."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    scope_id: str
    window_end_iso: str
    explicit_controlled_unit_ids: Tuple[str, ...] = Field(default_factory=tuple)


class SpendCeilingCheck(BaseModel):
    """DAP-23: ceiling evaluated before execution."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    proposed_cost: float
    ceiling: float
    within_ceiling: bool


# --- 2E · Commission + assistance chat (DAP-18..20) ----------------
class CommissionedJob(BaseModel):
    """DAP-18: commissioned with a frozen objective; freeze at commission."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    job_id: str
    objective_frozen: str
    committed_at_iso: str
    engine_routing: str = Field(
        ...,
        description="DAP-19: MUST route to the engine that governs its operation per §4.",
    )


# --- 2F · Metering + receipts (DAP-21..24) --------------------------
class MeteredEvent(BaseModel):
    """DAP-21 verbatim: 'operation type; what was accessed; quantity;
    terms identifier in force; party principal; timestamp from the
    platform's reliable time source.'  R-C2: au_3b_defensible=False."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operation_type: str
    accessed_scope: str
    quantity: float
    quantity_unit: str
    terms_id: str
    party_id: str
    timestamp_iso: str
    au_3b_defensible: bool = Field(
        default=False,
        description=(
            "R-C2: timestamp not defensible under AU-3(b) until "
            "Doc-0 G-8 closes.  Silent flip forbidden by invariant."
        ),
    )


class TermsResolution(BaseModel):
    """DAP-22: three-level resolution, most-specific-first."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    resolved_terms_id: str
    resolution_level: str  # 'party' | 'custody_class' | 'estate_default'


# --- 2G · Owner configuration (DAP-25..27) --------------------------
class OperationAvailability(str, Enum):
    """DAP-25: default for every combination is unavailable."""
    UNAVAILABLE = "unavailable"
    ON_APPROVAL = "on_approval"
    UNDER_STANDING_TERMS = "under_standing_terms"


class SuspensionAct(BaseModel):
    """DAP-27: suspension halts all in-flight and future.  Immediate.
    In-flight jobs stop, recorded as stopped, never silently completed."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    suspension_reason: str
    in_flight_job_ids_stopped: Tuple[str, ...]


# --- 2H · Failure posture (DAP-28..30) — pure invariants, no schema --
# Enforced structurally in services/dap/gates.py + tests.
