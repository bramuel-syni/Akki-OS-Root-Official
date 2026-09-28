"""services.platform_control_plane.service_account_entity — CP-P1-CP5.

Freezes the control-plane `service_account` record shape per Akki OS
Pilot Platform Reference v0.2 (17 September 2026) §10 verbatim:

    service_account(id, tenant_id, name, cert_fingerprint, expires_at)

§7.2 anchor: data-plane agents auth via short-lived certs bound to
tenant_id. `cert_fingerprint` OPEN str (algorithm-agnostic per
case-agnostic doctrine · admits sha-256, sha-1, ed25519-thumbprint,
etc. without a closed enum). `expires_at` OPEN str (ISO-8601 by
convention · not validated at carrier layer · empty admits · caller
composes).

Pure carrier · caller composes validation:
- CP-P1-CP1 · cross-tenant refusal on refs whose tenant_id ≠ owning
  ServiceAccountEntity.tenant_id.
- Downstream P4 CP · scheduler admission composes expires_at freshness
  refusal (CONTRACT-MODELED item 6 · real PKI required).
"""
from __future__ import annotations

import dataclasses


SERVICE_ACCOUNT_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim control-plane data model: "
    "service_account(id, tenant_id, name, cert_fingerprint, "
    "expires_at). §7.2 anchor: data-plane agents auth via short-lived "
    "certs bound to tenant_id. cert_fingerprint OPEN str "
    "(algorithm-agnostic · case-agnostic per 2026-09-13 owner "
    "correction)."
)


@dataclasses.dataclass(frozen=True)
class ServiceAccountEntity:
    """Frozen carrier for the control-plane `service_account` record.

    All 5 fields OPEN str · ownership isolation anchored at
    `tenant_id` (position 2 · index 1).
    """
    id: str
    tenant_id: str
    name: str
    cert_fingerprint: str
    expires_at: str


SERVICE_ACCOUNT_ENTITY_FIELDS = tuple(
    f.name for f in dataclasses.fields(ServiceAccountEntity)
)


__all__ = [
    "SERVICE_ACCOUNT_ENTITY_ANCHOR",
    "SERVICE_ACCOUNT_ENTITY_FIELDS",
    "ServiceAccountEntity",
]
