"""services.governance_plane.cross_service_binding — CP-M8-CSD-1 preventive charter.

Owner ruling §A verbatim (banked STATE/DECISIONS.md master `a04c65a8` 2026-09-16T~17:43Z):

    "§3.2 clause 5 = shape (b) PREVENTIVE-CHARTER RATIFIED: record + alert on
     dispatch-to-unregistered-resource, allow during pilot, upgrade path to
     hard-gate preserved as a future owner ruling. Build the preventive
     mechanism tests-first (small), then author the M8 wave-close report /
     M8 SEAL per the seal-readiness note."

Analog of `services.governance_plane.cross_table_consistency` (CP-M8-CTCC-1):
- Pure data-in / data-out primitives.
- No dispatch imports · no runtime hard-gate.
- Preventive-charter refusal wrapper: caller-invoked only; fires when the
  dispatch surface list references a resource_ref absent from the
  registered_resources set.
- Coarse rule by design (matches CP-M8-CTCC-1 wave-honest D.2): set-membership
  check on `resource_ref`; the primitive does not enumerate reasons.

Case-agnostic. Zero closed enums. Zero domain tokens. All identifier
discriminators are OPEN str (per 2026-09-13 owner correction).

Composition surface only:
- `surface_id` is a caller-supplied opaque str referencing a dispatch surface
  in the codebase; this module does NOT import any dispatch surface.
- `resource_ref` is opaque; caller-side composition binds it to a
  RegisteredResourceRef (e.g. an entry in `services.resource_registry`);
  this module does NOT import `services.resource_registry`.
- `registry_id` is opaque; caller-side composition binds it to a specific
  registry instance (e.g. a per-process registry id).

Standing-line proof:
- No `bytes` type-hint on any field.
- No enforcement hard-gate — preventive-charter · caller invokes.
- Upgrade path to hard-gate preserved by construction: a future CP can
  add a wrapper that binds this check to a global dispatch gate without
  refactoring this module.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


# Verbatim anchor · required for gating invariant.
CROSS_SERVICE_BINDING_SHAPE_B_ANCHOR = (
    "§3.2 clause 5 = shape (b) PREVENTIVE-CHARTER RATIFIED (owner ruling §A "
    "banked 2026-09-16T~17:43Z master a04c65a8): 'record + alert on "
    "dispatch-to-unregistered-resource, allow during pilot, upgrade path to "
    "hard-gate preserved as a future owner ruling'."
)


class CrossServiceBindingDriftRefused(Exception):
    """Caller-invoked refusal when any dispatch-surface's `resource_ref`
    is not present in the registered-resources set.

    Preventive-charter · runtime enforcement fires only when a caller
    explicitly invokes `assert_no_cross_service_binding_drift`. There is
    no global gate. Matches CP-M8-CTCC-1 pattern.

    Message reports COUNTS only (never surface_id/resource_ref values ·
    those are caller-supplied opaque strings potentially sensitive)."""


@dataclasses.dataclass(frozen=True)
class DispatchSurfaceRef:
    """Reference to a dispatch surface in the codebase · frozen · exact-order
    2 carriers.

    - `surface_id` (str) — opaque caller-supplied ref (e.g. a module path
      or a qualified function name).
    - `resource_ref` (str) — opaque caller-supplied ref to the resource
      the dispatch surface targets (e.g. a resource_registry entry id).
    """
    surface_id: str
    resource_ref: str


@dataclasses.dataclass(frozen=True)
class RegisteredResourceRef:
    """Reference to a registered resource in a resource registry · frozen ·
    exact-order 2 carriers.

    - `resource_ref` (str) — opaque caller-supplied ref matching the
      DispatchSurfaceRef.resource_ref shape.
    - `registry_id` (str) — opaque caller-supplied ref to the registry
      instance holding this registration.
    """
    resource_ref: str
    registry_id: str


def assess_binding_drift(
    *,
    dispatch_surfaces: Tuple[DispatchSurfaceRef, ...],
    registered_resources: Tuple[RegisteredResourceRef, ...],
) -> Tuple[DispatchSurfaceRef, ...]:
    """Return sorted tuple of `DispatchSurfaceRef`s whose `resource_ref` is
    NOT in the `registered_resources` set. Coarse rule (matches CP-M8-CTCC-1
    wave-honest D.2): set-membership check only.

    Deterministic ordering: sort by (`surface_id`, `resource_ref`).

    Pure function: no side effects, no I/O, no logging.
    """
    registered_set = frozenset(r.resource_ref for r in registered_resources)
    at_risk = [ds for ds in dispatch_surfaces if ds.resource_ref not in registered_set]
    return tuple(sorted(at_risk, key=lambda ds: (ds.surface_id, ds.resource_ref)))


def assert_no_cross_service_binding_drift(
    *,
    dispatch_surfaces: Tuple[DispatchSurfaceRef, ...],
    registered_resources: Tuple[RegisteredResourceRef, ...],
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Raises `CrossServiceBindingDriftRefused` when
    `assess_binding_drift(...)` returns a non-empty tuple.

    Returns None on admit.

    Message reports COUNTS only (never surface_id / resource_ref values)."""
    at_risk = assess_binding_drift(
        dispatch_surfaces=dispatch_surfaces,
        registered_resources=registered_resources,
    )
    if at_risk:
        raise CrossServiceBindingDriftRefused(
            f"cross-service binding drift detected: "
            f"{len(at_risk)} dispatch surface(s) reference unregistered "
            f"resource_ref(s) (n_registered={len(registered_resources)}, "
            f"n_dispatch={len(dispatch_surfaces)})."
        )
    return None


__all__ = [
    "CROSS_SERVICE_BINDING_SHAPE_B_ANCHOR",
    "DispatchSurfaceRef",
    "RegisteredResourceRef",
    "assess_binding_drift",
    "assert_no_cross_service_binding_drift",
    "CrossServiceBindingDriftRefused",
]
