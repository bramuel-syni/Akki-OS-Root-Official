"""CP-ENT-16-PILOT-LICENCE-SEEDS · pilot_licence_seeds_v1 · additive §1.2 modality-extension.

Pilot licence seed objects created at tenant creation for RMS + DigiCow + AKKI-TEST
with Compute dial `Managed` + Frontier dial `Your Keys` — so every model call resolves
from day 1 per SO §6.9 amendment §6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim.

Spec anchors (verbatim on single un-wrapped lines):
- SO §6.9 amendment §6 verbatim (STATE/OWNER_DROPS/so_6_9_amendment_20260223/DROP.md line 20): "ENT-16 keeps its rule and gains its seed: a pilot licence object created at tenant creation for RMS, DigiCow, and AKKI-TEST — Compute dial Managed, Frontier dial Your Keys — so every model call resolves from the first day."
- Entitlement Service Spec v1 §6 ENT-16..19 verbatim (chokepoint resolves before dispatch; 6-step ordered chain; any link that does not resolve refuses the call).
- Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: ENT-16 Managed compute + Frontier Your Keys; training compute + model weights + labelled corpus never leave Akki's boundary.
- §1.2 modality-extension composes sealed CP-ENTITLEMENT-BUILD-WAVE `services/entitlement_service_v1/chokepoint_resolver.py` (R-82); no redeclaration.

Additive-only per SO §3.8.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Optional


class TenantCreationRefusedWithoutPilotLicenceSeedError(Exception):
    """ENT-16 gate: tenant creation refused without a pilot licence seed present.

    Enforces the SO §6.9 amendment §6 rule that every tenant must have a pilot
    licence seed at creation so ENT-16 chokepoint resolution never fails on day 1.
    """


@dataclass(frozen=True)
class PilotLicenceSeed_v1:
    """Pilot licence seed per SO §6.9 amendment §6 verbatim.

    4-field shape (order-verbatim):
    - tenant_name: canonical tenant identifier.
    - compute_dial: Literal["Managed"] — Managed compute per ENT-16 + Ruling (b).
    - frontier_dial: Literal["Your Keys"] — Your Keys frontier per ENT-16 + Ruling (b).
    - created_at_utc: ISO-8601 tz-aware creation timestamp.
    """
    tenant_name: str
    compute_dial: Literal["Managed"]
    frontier_dial: Literal["Your Keys"]
    created_at_utc: str


@dataclass(frozen=True)
class TenantCreationRecord_v1:
    """Tenant creation record carrying the pilot licence seed evidence."""
    tenant_name: str
    pilot_licence_seed: PilotLicenceSeed_v1
    created_at_utc: str


# --- The three pilot licence seeds (SO §6.9 amendment §6 verbatim) ------------

RMS_PILOT_LICENCE_SEED: Final[PilotLicenceSeed_v1] = PilotLicenceSeed_v1(
    tenant_name="RMS",
    compute_dial="Managed",
    frontier_dial="Your Keys",
    created_at_utc="2026-02-23T13:00:00Z",
)

DIGICOW_PILOT_LICENCE_SEED: Final[PilotLicenceSeed_v1] = PilotLicenceSeed_v1(
    tenant_name="DigiCow",
    compute_dial="Managed",
    frontier_dial="Your Keys",
    created_at_utc="2026-02-23T13:00:00Z",
)

AKKI_TEST_PILOT_LICENCE_SEED: Final[PilotLicenceSeed_v1] = PilotLicenceSeed_v1(
    tenant_name="AKKI-TEST",
    compute_dial="Managed",
    frontier_dial="Your Keys",
    created_at_utc="2026-02-23T13:00:00Z",
)


THREE_TENANT_PILOT_LICENCE_SEEDS: Final[tuple[PilotLicenceSeed_v1, ...]] = (
    RMS_PILOT_LICENCE_SEED,
    DIGICOW_PILOT_LICENCE_SEED,
    AKKI_TEST_PILOT_LICENCE_SEED,
)


# --- Tenant creation boundary (ENT-16 gate) -----------------------------------

def create_tenant_with_pilot_licence_seed(
    *,
    tenant_name: str,
    pilot_licence_seed: Optional[PilotLicenceSeed_v1],
) -> TenantCreationRecord_v1:
    """Create a tenant with its pilot licence seed per SO §6.9 amendment §6.

    Refuses:
    - `pilot_licence_seed is None` (ENT-16: any link that does not resolve refuses the call).
    - `tenant_name` empty (chokepoint resolves before dispatch).
    - `pilot_licence_seed.compute_dial != "Managed"` (structural — Literal type would catch,
      but frozen dataclass could be bypassed via reflection; defensive check retained).
    - `pilot_licence_seed.frontier_dial != "Your Keys"` (same reasoning).
    """
    if pilot_licence_seed is None:
        raise TenantCreationRefusedWithoutPilotLicenceSeedError(
            f"Tenant creation refused for tenant_name={tenant_name!r}: pilot licence seed absent "
            "(ENT-16 chokepoint resolution requires a resolvable licence at day 1 per SO §6.9 "
            "amendment §6 verbatim)."
        )
    if not tenant_name:
        raise TenantCreationRefusedWithoutPilotLicenceSeedError(
            "Tenant creation refused: tenant_name is empty (ENT-16 chokepoint resolves before "
            "dispatch; any link that does not resolve refuses the call)."
        )
    if pilot_licence_seed.compute_dial != "Managed":
        raise TenantCreationRefusedWithoutPilotLicenceSeedError(
            f"Tenant creation refused: compute_dial={pilot_licence_seed.compute_dial!r} != "
            "'Managed' (Ruling (b) AKKI-RUNS-IT verbatim: ENT-16 Managed compute)."
        )
    if pilot_licence_seed.frontier_dial != "Your Keys":
        raise TenantCreationRefusedWithoutPilotLicenceSeedError(
            f"Tenant creation refused: frontier_dial={pilot_licence_seed.frontier_dial!r} != "
            "'Your Keys' (Ruling (b) AKKI-RUNS-IT verbatim: ENT-16 Frontier Your Keys)."
        )
    return TenantCreationRecord_v1(
        tenant_name=tenant_name,
        pilot_licence_seed=pilot_licence_seed,
        created_at_utc=pilot_licence_seed.created_at_utc,
    )


# --- Final posture marker (SO §6.9 amendment §6 verbatim) ---------------------

EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE: Final[str] = (
    "SO §6.9 amendment §6 verbatim: 'ENT-16 keeps its rule and gains its seed: a pilot licence "
    "object created at tenant creation for RMS, DigiCow, and AKKI-TEST — Compute dial Managed, "
    "Frontier dial Your Keys — so every model call resolves from the first day.'"
)


__all__ = [
    "TenantCreationRefusedWithoutPilotLicenceSeedError",
    "PilotLicenceSeed_v1",
    "TenantCreationRecord_v1",
    "RMS_PILOT_LICENCE_SEED",
    "DIGICOW_PILOT_LICENCE_SEED",
    "AKKI_TEST_PILOT_LICENCE_SEED",
    "THREE_TENANT_PILOT_LICENCE_SEEDS",
    "create_tenant_with_pilot_licence_seed",
    "EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE",
]
