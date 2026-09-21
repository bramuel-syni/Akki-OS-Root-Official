"""services.platform_control_plane.tenant_context — CP-P1-CP1 · M9 foundation.

Preventive-charter tenant-context enforcement, per Akki OS Pilot Platform
Reference v0.2 (17 September 2026) §3.1 + §4.3 verbatim mandates:

    §3.1: "A tenant maps one-to-one to a legal entity. All resources
    are owned by exactly one tenant and carry its tenant_id."

    §4.3: "The API gateway resolves tenant_id from the authenticated
    session and injects it into every request. Clients cannot supply
    it. Every data-plane service validates tenant_id on every call
    against its own provisioned identity and rejects mismatches."

Foundation isolation invariant for the entire M9 milestone: every
downstream CP composes on top of this module.

Analog of CP-M8-CSD-1 `services.governance_plane.cross_service_binding`:
- Pure data-in / data-out primitives.
- No I/O · no data-plane imports · no runtime hard-gate.
- Preventive-charter refusal wrappers: caller-invoked only.
- Coarse rule by design (set-membership on `tenant_id`); the primitive
  does not enumerate reasons beyond the two refusal classes.

Case-agnostic. Zero closed enums. Zero domain tokens. All identifier
discriminators are OPEN str (per 2026-09-13 owner correction).

Composition surface only:
- `tenant_id` is a caller-supplied opaque str (typically resolved by
  the API gateway from an authenticated session).
- `resource_type` / `resource_id` are opaque; caller-side composition
  binds them to concrete control-plane entities (workspace, task, job,
  connector, etc.) or data-plane surfaces.

Standing-line proof:
- No `bytes` type-hint on any field.
- No enforcement hard-gate — preventive-charter · caller invokes.
- Upgrade path to hard-gate preserved by construction: a future CP can
  add a wrapper that binds this check to a global request-time gate
  without refactoring this module.
"""
from __future__ import annotations

import dataclasses
from typing import Optional, Tuple


# Verbatim anchor · required for gating invariant.
TENANT_CONTEXT_ENFORCEMENT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) "
    "§3.1 + §4.3 verbatim: "
    "'A tenant maps one-to-one to a legal entity. All resources are "
    "owned by exactly one tenant and carry its tenant_id.' AND "
    "'The API gateway resolves tenant_id from the authenticated session "
    "and injects it into every request. Clients cannot supply it. "
    "Every data-plane service validates tenant_id on every call against "
    "its own provisioned identity and rejects mismatches.'"
)


class TenantContextRefused(Exception):
    """Root refusal for tenant-context invariants.

    Preventive-charter · runtime enforcement fires only when a caller
    explicitly invokes `assert_tenant_context_valid`. There is no global
    gate.

    Message reports COUNTS only (never tenant_id / resource_id values ·
    those are caller-supplied opaque strings potentially sensitive)."""


class ClientSuppliedTenantIdRefused(TenantContextRefused):
    """Refused: a client-side actor supplied a `tenant_id` explicitly.

    Per §4.3: 'The API gateway resolves tenant_id from the authenticated
    session and injects it into every request. Clients cannot supply it.'

    Any non-None `client_supplied_tenant_id` argument is a refusal event,
    even if its value happens to match the context. This preserves the
    server-side-resolves-only invariant."""


class CrossTenantAccessRefused(TenantContextRefused):
    """Refused: one or more requested resources carry a `tenant_id` that
    does not match the context's `tenant_id`, or carry an empty
    `tenant_id` (missing).

    Per §3.1: 'All resources are owned by exactly one tenant and carry
    its tenant_id.'"""


@dataclasses.dataclass(frozen=True)
class TenantContext:
    """Resolved tenant context · frozen · exact-order 1 carrier.

    - `tenant_id` (str) — opaque caller-supplied ref (typically resolved
      by the API gateway from the authenticated session per §4.3).
    """
    tenant_id: str


@dataclasses.dataclass(frozen=True)
class TenantOwnedResourceRef:
    """Reference to a control-plane or data-plane resource · frozen ·
    exact-order 3 carriers.

    - `tenant_id` (str) — opaque ref to the owning tenant. Empty string
      is treated as missing (refused).
    - `resource_type` (str) — opaque ref to the resource-type name
      (e.g. 'job', 'connector', 'estate'). Case-agnostic OPEN str.
    - `resource_id` (str) — opaque ref to the resource instance id.
    """
    tenant_id: str
    resource_type: str
    resource_id: str


def assess_tenant_context_drift(
    *,
    context: TenantContext,
    requested_resources: Tuple[TenantOwnedResourceRef, ...],
) -> Tuple[TenantOwnedResourceRef, ...]:
    """Return sorted tuple of `TenantOwnedResourceRef`s whose `tenant_id`
    is empty (missing) OR does not match `context.tenant_id`.

    Coarse rule: string equality on `tenant_id`.

    Deterministic ordering: sort by
    (`tenant_id`, `resource_type`, `resource_id`).

    Pure function: no side effects, no I/O, no logging.
    """
    at_risk = [
        r for r in requested_resources
        if r.tenant_id == "" or r.tenant_id != context.tenant_id
    ]
    return tuple(sorted(
        at_risk,
        key=lambda r: (r.tenant_id, r.resource_type, r.resource_id),
    ))


def assert_tenant_context_valid(
    *,
    context: TenantContext,
    requested_resources: Tuple[TenantOwnedResourceRef, ...],
    client_supplied_tenant_id: Optional[str],
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast on the more fundamental violation):

    1. If `client_supplied_tenant_id is not None` → raise
       `ClientSuppliedTenantIdRefused`.
    2. Else if `assess_tenant_context_drift(...)` returns a non-empty
       tuple → raise `CrossTenantAccessRefused`.

    Returns None on admit.

    Message reports COUNTS only (never tenant_id / resource_id values)."""
    if client_supplied_tenant_id is not None:
        raise ClientSuppliedTenantIdRefused(
            f"client-supplied tenant_id refused: server-side resolution "
            f"is mandatory per §4.3 (n_requested_resources="
            f"{len(requested_resources)})."
        )
    at_risk = assess_tenant_context_drift(
        context=context, requested_resources=requested_resources,
    )
    if at_risk:
        raise CrossTenantAccessRefused(
            f"cross-tenant access refused: "
            f"{len(at_risk)} of {len(requested_resources)} requested "
            f"resource(s) do not match the context's tenant_id or "
            f"carry an empty tenant_id."
        )
    return None


__all__ = [
    "TENANT_CONTEXT_ENFORCEMENT_ANCHOR",
    "TenantContext",
    "TenantOwnedResourceRef",
    "assess_tenant_context_drift",
    "assert_tenant_context_valid",
    "TenantContextRefused",
    "ClientSuppliedTenantIdRefused",
    "CrossTenantAccessRefused",
]
