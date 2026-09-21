"""services.platform_control_plane.tenant_entity — CP-P1-CP2 · M9 · pure carrier.

Freezes the control-plane `tenant` record shape per Akki OS Pilot
Platform Reference v0.2 (17 September 2026) §10 verbatim:

    tenant(id, legal_name, short_name, jurisdiction, status, mou_ref,
           created_at)

§3.1 anchor: "A tenant maps one-to-one to a legal entity."

Pure carrier · no refusal wrapper · no I/O · no data-plane imports.

Composition-only surface:
- `id`, `legal_name`, `short_name`, `jurisdiction`, `mou_ref`,
  `created_at` are caller-supplied opaque strings.
- `status` is an OPEN str whose canonical vocabulary is
  {provisioning, sandbox_active, production_active, suspended,
  offboarded} per §4.7 but is validated by CP-P1-CP6 (lifecycle FSM),
  not by this carrier · case-agnostic per 2026-09-13 owner correction.

Standing-line proof:
- No `bytes` fields · all-str · 7 exact-order fields.
- No enforcement hard-gate · pure data · caller composes validation.
"""
from __future__ import annotations

import dataclasses


TENANT_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim control-plane data model: "
    "tenant(id, legal_name, short_name, jurisdiction, status, mou_ref, "
    "created_at). §3.1 anchor: 'A tenant maps one-to-one to a legal "
    "entity. All resources are owned by exactly one tenant and carry "
    "its tenant_id.'"
)


@dataclasses.dataclass(frozen=True)
class TenantEntity:
    """Frozen carrier for the control-plane `tenant` record.

    All 7 fields are OPEN str per case-agnostic doctrine (2026-09-13
    owner correction). Downstream CPs compose validation:
    - CP-P1-CP1 · assert_tenant_context_valid checks cross-tenant
      access on refs whose tenant_id must match `id`.
    - CP-P1-CP6 · lifecycle-FSM validates `status` transitions against
      the §4.7 vocabulary.
    """
    id: str
    legal_name: str
    short_name: str
    jurisdiction: str
    status: str
    mou_ref: str
    created_at: str


TENANT_ENTITY_FIELDS = tuple(f.name for f in dataclasses.fields(TenantEntity))


__all__ = [
    "TENANT_ENTITY_ANCHOR",
    "TENANT_ENTITY_FIELDS",
    "TenantEntity",
]
