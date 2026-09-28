"""services.platform_control_plane.compute_integration — CP-P4-CP1 · M9.

Pure frozen carrier for control-plane compute_integration record per
Akki OS Pilot Platform Reference v0.2 §10 verbatim:

    compute_integration (id, tenant_id, kind, estate_id, class,
                         capacity, agent_id, status)

§6 anchor: `kind ∈ {central_allocation, tenant_provided}` (OPEN str
per case-agnostic doctrine). Every job (§6.4 M-Cp-1) names a
compute_integration_id.

Python keyword note: §10 field name `class` is a reserved keyword in
Python and cannot appear as a dataclass field. The verbatim §10 name
is preserved in the anchor and in COMPUTE_INTEGRATION_ENTITY_FIELDS
metadata; the dataclass attribute uses `class_ref` (str) which
carries the same semantics — the compute-class identifier the
integration exposes (OPEN str per §6 case-agnostic doctrine).

Refusals:
- kind not in COMPUTE_INTEGRATION_KINDS → UnknownComputeIntegrationKindRefused

Standing-line proof:
- 8 str · 8 fields exact-order (class → class_ref shim).
- No enforcement hard-gate · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


COMPUTE_INTEGRATION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: compute_integration (id, tenant_id, kind, estate_id, "
    "class, capacity, agent_id, status). §6 anchor: kind ∈ "
    "{central_allocation, tenant_provided}. §6.4 M-Cp-1: Every job "
    "names a compute_integration_id."
)


# §6 verbatim kind vocabulary · OPEN str · case-sensitive.
COMPUTE_INTEGRATION_KINDS: Tuple[str, ...] = (
    "central_allocation",
    "tenant_provided",
)


@dataclasses.dataclass(frozen=True)
class ComputeIntegrationEntity:
    """Frozen carrier for the control-plane compute_integration record.

    Exact-order 8 str OPEN fields (Python-safe · §10 `class` shim to
    `class_ref` documented in module docstring):
    - id · compute_integration record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - kind · §6 vocabulary (central_allocation | tenant_provided).
    - estate_id · which estate hosts the integration.
    - class_ref · compute-class identifier (§10 `class` verbatim
      · Python-keyword shim · OPEN str).
    - capacity · capacity descriptor ref (OPEN str; concrete
      structure is downstream P4-CP6 SCHEDULER-ADMISSION material).
    - agent_id · agent identifier ref.
    - status · lifecycle status (OPEN str).
    """
    id: str
    tenant_id: str
    kind: str
    estate_id: str
    class_ref: str
    capacity: str
    agent_id: str
    status: str


# §10 verbatim field-listing order preserved · exposes `class` in the
# name-tuple metadata (verbatim spec ordinal 5) with the dataclass
# attribute shim `class_ref`. Both tuples align by index.
COMPUTE_INTEGRATION_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "kind",
    "estate_id",
    "class_ref",
    "capacity",
    "agent_id",
    "status",
)

# §10 verbatim field names (Python-unsafe · reference only).
COMPUTE_INTEGRATION_ENTITY_FIELDS_SPEC_VERBATIM: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "kind",
    "estate_id",
    "class",
    "capacity",
    "agent_id",
    "status",
)


class ComputeIntegrationEntityRefused(Exception):
    """Root refusal for compute-integration-entity invariants."""


class UnknownComputeIntegrationKindRefused(ComputeIntegrationEntityRefused):
    """Refused: kind not in COMPUTE_INTEGRATION_KINDS (case-sensitive).
    §6 verbatim: kind ∈ {central_allocation, tenant_provided}."""


def assert_compute_integration_kind_valid(
    *, entity: ComputeIntegrationEntity,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses UnknownComputeIntegrationKindRefused when
    entity.kind not in COMPUTE_INTEGRATION_KINDS (case-sensitive).

    Returns None on admit."""
    if entity.kind not in frozenset(COMPUTE_INTEGRATION_KINDS):
        raise UnknownComputeIntegrationKindRefused(
            f"unknown-kind refused: kind not among "
            f"{len(COMPUTE_INTEGRATION_KINDS)} §6 kinds "
            f"(case-sensitive)."
        )
    return None


__all__ = [
    "COMPUTE_INTEGRATION_ANCHOR",
    "COMPUTE_INTEGRATION_KINDS",
    "COMPUTE_INTEGRATION_ENTITY_FIELDS",
    "COMPUTE_INTEGRATION_ENTITY_FIELDS_SPEC_VERBATIM",
    "ComputeIntegrationEntity",
    "ComputeIntegrationEntityRefused",
    "UnknownComputeIntegrationKindRefused",
    "assert_compute_integration_kind_valid",
]
