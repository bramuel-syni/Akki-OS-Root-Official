"""services.platform_control_plane.tenant_lifecycle — CP-P1-CP6 · M9.

Preventive-charter tenant lifecycle FSM per Akki OS Pilot Platform
Reference v0.2 (17 September 2026) §4.7 verbatim:

    provisioning → sandbox_active → production_active → suspended
                                                     → offboarded
    suspended     → production_active (unsuspend) OR offboarded
    offboarded    → (terminal · irreversible)

§4.4: promotion sandbox_active → production_active requires
tenant_owner + platform_operator joint approval — recorded as tuple
of `approver_refs` on the Transition carrier · NOT enforced here
(caller composes via CP-P2-CP1 role-registry).

§4.7 effects on entry to suspended: sessions_revoked, jobs_halted,
allocations_released, data_retained.
§4.7 effects on entry to offboarded: metadata_deleted (30d),
artefacts_deleted (30d), certs_revoked, allocation_returned.

Effects tracked as OPEN str refs in `effects_refs: Tuple[str, ...]`
· enforcement composed by downstream CPs (P4 for allocation return,
P5 for artefact delete, P6 for cert revocation).

CONTRACT-MODELED items enabled (from PLATFORM_LAYER_REQUIREMENTS_v0_2 §8):
- Item 12 · 30-day irreversible offboarding delete — real wall-clock
  scheduler required. Contract shape: `assert_transition_valid`
  refuses on offboarded → anything (terminal invariant); the 30-day
  delete is a downstream P5 CP.

Analog of CP-M8-CSD-1 and CP-P1-CP1 preventive-charter pattern:
- 1 frozen carrier + 1 pure assess + 1 refusal wrapper + 3 refusal
  classes + verbatim anchor.
- Coarse rule by design (set-membership on the (source, target) pair).
- Caller-invoked · no runtime hard-gate.
- Upgrade path to hard-gate preserved by construction.

Standing-line proof:
- No `bytes` field · all str + tuple[str, ...] · 6 exact-order fields.
- No enforcement hard-gate · pure data · caller composes.
- Zero closed enums for state values (all OPEN str) · zero domain
  tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


TENANT_LIFECYCLE_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §4.7 "
    "verbatim tenant lifecycle: "
    "provisioning → sandbox_active → production_active → suspended → "
    "offboarded (terminal · irreversible). suspended may unsuspend to "
    "production_active. §4.4: sandbox → production promotion requires "
    "tenant_owner + platform_operator joint approval (recorded as "
    "approver_refs · NOT enforced here · caller composes via "
    "CP-P2-CP1 role-registry)."
)


# §4.7 canonical vocabulary (OPEN str per 2026-09-13 owner correction).
TENANT_LIFECYCLE_STATES: Tuple[str, ...] = (
    "provisioning",
    "sandbox_active",
    "production_active",
    "suspended",
    "offboarded",
)


TENANT_LIFECYCLE_TERMINAL_STATES: Tuple[str, ...] = (
    "offboarded",
)


# §4.7 verbatim allowed transitions (source, target) tuples.
TENANT_LIFECYCLE_TRANSITIONS: Tuple[Tuple[str, str], ...] = (
    ("provisioning", "sandbox_active"),
    ("sandbox_active", "production_active"),
    ("sandbox_active", "suspended"),
    ("sandbox_active", "offboarded"),
    ("production_active", "suspended"),
    ("production_active", "offboarded"),
    ("suspended", "production_active"),
    ("suspended", "offboarded"),
)


class TenantLifecycleTransitionRefused(Exception):
    """Root refusal for tenant lifecycle FSM invariants.

    Preventive-charter · caller-invoked only. Message reports COUNTS
    and positional indices only (never state values / tenant_id in the
    exception body)."""


class IllegalTransitionRefused(TenantLifecycleTransitionRefused):
    """Refused: the (source_state, target_state) pair is not in
    §4.7 verbatim allowed transitions."""


class TerminalStateOutboundRefused(TenantLifecycleTransitionRefused):
    """Refused: source_state is in TENANT_LIFECYCLE_TERMINAL_STATES.
    Fires FIRST (before matrix check) · offboarded is irreversible per
    §4.7."""


@dataclasses.dataclass(frozen=True)
class TenantLifecycleTransition:
    """Frozen carrier for a tenant lifecycle transition attempt.

    - `tenant_id` (str · OPEN opaque · owning tenant per CP-P1-CP1
      isolation invariant).
    - `source_state` / `target_state` (str · OPEN str · canonical
      vocabulary TENANT_LIFECYCLE_STATES per §4.7 but not enforced at
      carrier layer · caller composes).
    - `reason_ref` (str · OPEN opaque · reason record ref for audit).
    - `approver_refs` (tuple[str, ...] · OPEN opaque · approval record
      refs; §4.4 promotion requires 2 approvers with tenant_owner +
      platform_operator roles · NOT enforced here · caller composes).
    - `effects_refs` (tuple[str, ...] · OPEN opaque · §4.7 effect
      record refs for entry-side effects · NOT enforced here).
    """
    tenant_id: str
    source_state: str
    target_state: str
    reason_ref: str
    approver_refs: Tuple[str, ...]
    effects_refs: Tuple[str, ...]


def _pair_key(t: TenantLifecycleTransition) -> Tuple[str, str]:
    return (t.source_state, t.target_state)


def assess_transition_drift(
    *,
    transitions: Tuple[TenantLifecycleTransition, ...],
) -> Tuple[TenantLifecycleTransition, ...]:
    """Return sorted tuple of transitions whose (source, target) is not
    in TENANT_LIFECYCLE_TRANSITIONS OR whose source_state is terminal.

    Deterministic ordering by (tenant_id, source_state, target_state).
    Pure · no side effects."""
    legal = frozenset(TENANT_LIFECYCLE_TRANSITIONS)
    terminal = frozenset(TENANT_LIFECYCLE_TERMINAL_STATES)
    at_risk = [
        t for t in transitions
        if t.source_state in terminal or _pair_key(t) not in legal
    ]
    return tuple(sorted(
        at_risk,
        key=lambda t: (t.tenant_id, t.source_state, t.target_state),
    ))


def assert_transition_valid(
    *,
    transition: TenantLifecycleTransition,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast on the more fundamental violation):

    1. If `transition.source_state ∈ TENANT_LIFECYCLE_TERMINAL_STATES`
       → raise `TerminalStateOutboundRefused`.
    2. Else if `(source, target) ∉ TENANT_LIFECYCLE_TRANSITIONS`
       → raise `IllegalTransitionRefused`.

    Returns None on admit.

    Message reports COUNTS only (never state values or tenant_id)."""
    if transition.source_state in TENANT_LIFECYCLE_TERMINAL_STATES:
        raise TerminalStateOutboundRefused(
            f"terminal-state-outbound refused: source_state is one of "
            f"{len(TENANT_LIFECYCLE_TERMINAL_STATES)} terminal states "
            f"per §4.7 · offboarded is irreversible."
        )
    if _pair_key(transition) not in frozenset(TENANT_LIFECYCLE_TRANSITIONS):
        raise IllegalTransitionRefused(
            f"illegal-transition refused: (source, target) not in "
            f"{len(TENANT_LIFECYCLE_TRANSITIONS)} allowed §4.7 pairs."
        )
    return None


__all__ = [
    "TENANT_LIFECYCLE_ANCHOR",
    "TENANT_LIFECYCLE_STATES",
    "TENANT_LIFECYCLE_TRANSITIONS",
    "TENANT_LIFECYCLE_TERMINAL_STATES",
    "TenantLifecycleTransition",
    "assess_transition_drift",
    "assert_transition_valid",
    "TenantLifecycleTransitionRefused",
    "IllegalTransitionRefused",
    "TerminalStateOutboundRefused",
]
