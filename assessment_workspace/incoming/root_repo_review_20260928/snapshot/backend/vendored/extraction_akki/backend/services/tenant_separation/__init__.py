"""services.tenant_separation · CP-TENANT-SEPARATION additive package.

Landed at Turn 4 sub-slice 4j (2026-02-XX) opening PHASE 2 per SO §6.8:

    "PHASE 2 CP-TENANT-SEPARATION · two legal entities, two tenants,
    zero mixing." (owner card TENANT_SEPARATION.md · card_sha256
    3aefe137ebf33ac86e4a7a21603a7d5fee9f276009eab69416a097375d5e24dc)

Additive-only per SO §3.8. Sealed siblings preserved:

- services.platform_control_plane.pilot_tenant_register
  (interim 4-tenant pilot register keys ("RMS","DigiCow","BDO","Trinity")
  · superseded by canonical roster here but LEFT UNCHANGED · retirement
  is a future slice · SO §3.8 additive-only forbids in-place sealed edit).
- services.data.repository (M11 auto-injection · AKKI-DATA-001).
- services.dap_lifecycle.* (DAP-1..38 lifecycle · R-95..R-97).
"""

from __future__ import annotations

__all__ = (
    "dap_activation",
    "isolation_sweep",
    "oversight_screens",
    "platform_operator",
    "tenant_registry",
)
