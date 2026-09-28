"""services.tenant_separation.dap_activation · per-tenant DAP records.

Owner card §4 verbatim (STATE/OBJECTIVES/TENANT_SEPARATION.md):

    "DAP activated on both tenants, separately. Per tenant: The six
    crossing profiles enabled per DAP-25 — every custody-class/operation
    combination defaults unavailable until the owner grants it. A licence
    object (ENT-5). A catalog view. A release budget (DAP-35) at the
    DEFAULT value, tagged pending R-7. An approving authority (DAP-14).
    The named approving authority is a tier-4 fork per tenant — bank
    both to STATE/DESK_QUEUE.md; until named, no controlled request
    executes (DAP-14 holds by construction; nothing is defaulted)."

Owner refinement verbatim (this-session · 2026-02-XX in response to 4j
plan confirmation):

    "No override on the PRIN-1 authorities — admit as named-but-unseated
    records (names + roles only; identity details arrive only via the
    custody path per R-104; controlled-request routing testable on
    AKKI-TEST synthetics meanwhile)."

Closed-vocab per SO §3.10-α. Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Final, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# DAP-25 · six crossing profiles per tenant
# ═══════════════════════════════════════════════════════════════════════════

DAP_25_CROSSING_PROFILE_IDS: Final[Tuple[str, ...]] = (
    "READ_INTERNAL",
    "WRITE_INTERNAL",
    "READ_CONTROLLED",
    "WRITE_CONTROLLED",
    "READ_EXTERNAL",
    "WRITE_EXTERNAL",
)


# ═══════════════════════════════════════════════════════════════════════════
# DAP-35 · DEFAULT-class release budget (tagged pending R-7)
# ═══════════════════════════════════════════════════════════════════════════

DAP_35_DEFAULT_BUDGET: Final[Dict[str, Any]] = {
    "units_per_calendar_month": 1000,
    "unit_kind": "controlled_release_events",
    "ceiling_visible_to_party": False,
}


# ═══════════════════════════════════════════════════════════════════════════
# Per-tenant activation records — sealed at 4j; identity material for
# RMS + DIGICOW enters via custody path per R-104 at future slice.
# ═══════════════════════════════════════════════════════════════════════════

def _crossing_profiles_default_unavailable() -> Dict[str, str]:
    return {pid: "unavailable_until_owner_grant" for pid in DAP_25_CROSSING_PROFILE_IDS}


_ACTIVATIONS: Final[Dict[str, Dict[str, Any]]] = {
    "RMS": {
        "dap_25_crossing_profiles": _crossing_profiles_default_unavailable(),
        "ent_5_licence_id": "ENT5-RMS-4J-INITIAL",
        "catalog_view_id": "CATALOG-RMS-4J",
        "dap_35_release_budget": {
            "value": DAP_35_DEFAULT_BUDGET,
            "ratification_status": "pending_R-7",
        },
        # DAP-14 · named-but-unseated per owner refinement 2026-02-XX.
        # Names + roles only; NO identity material at this stage.
        "dap_14_named_authority": {
            "name": "RMS Data-Owner Authority (name-of-record pending custody)",
            "role": "principal_of_record_dap_14_approver",
            "seat_state": "named_but_unseated",
            "custody_source_expected": "rms_connection_creds_vNEXT",
        },
    },
    "DIGICOW": {
        "dap_25_crossing_profiles": _crossing_profiles_default_unavailable(),
        "ent_5_licence_id": "ENT5-DIGICOW-4J-INITIAL",
        "catalog_view_id": "CATALOG-DIGICOW-4J",
        "dap_35_release_budget": {
            "value": DAP_35_DEFAULT_BUDGET,
            "ratification_status": "pending_R-7",
        },
        # DAP-14 · named-but-unseated per owner refinement 2026-02-XX.
        "dap_14_named_authority": {
            "name": "DigiCow Data-Owner Authority (name-of-record pending custody)",
            "role": "principal_of_record_dap_14_approver",
            "seat_state": "named_but_unseated",
            "custody_source_expected": "digicow_aws_creds_vNEXT",
        },
    },
    "AKKI-TEST": {
        "dap_25_crossing_profiles": _crossing_profiles_default_unavailable(),
        "ent_5_licence_id": "ENT5-AKKI-TEST-4J-INITIAL",
        "catalog_view_id": "CATALOG-AKKI-TEST-4J",
        "dap_35_release_budget": {
            "value": DAP_35_DEFAULT_BUDGET,
            "ratification_status": "pending_R-7",
        },
        "dap_14_named_authority": {
            "name": "AKKI-TEST Synthetic Authority (test fixture)",
            "role": "principal_of_record_dap_14_approver",
            "seat_state": "seated_synthetic",
        },
    },
    "AUDIT-FIXTURE-20260921": {
        "dap_25_crossing_profiles": _crossing_profiles_default_unavailable(),
        "ent_5_licence_id": "ENT5-AUDIT-FIXTURE-20260921",
        "catalog_view_id": "CATALOG-AUDIT-FIXTURE-20260921",
        "dap_35_release_budget": {
            "value": DAP_35_DEFAULT_BUDGET,
            "ratification_status": "pending_R-7",
        },
        "dap_14_named_authority": {
            "name": "Audit-Fixture Approving Authority (fixed)",
            "role": "principal_of_record_dap_14_approver",
            "seat_state": "seated_fixture",
        },
    },
}


def get_activation(tenant_id: str) -> Dict[str, Any]:
    """Return the activation record for a canonical tenant.

    Raises KeyError with a diagnostic message if the tenant is unknown.
    """
    if tenant_id not in _ACTIVATIONS:
        raise KeyError(
            f"unknown tenant_id: {tenant_id!r} · canonical set is "
            f"{tuple(_ACTIVATIONS.keys())}"
        )
    return _ACTIVATIONS[tenant_id]


__all__ = (
    "DAP_25_CROSSING_PROFILE_IDS",
    "DAP_35_DEFAULT_BUDGET",
    "get_activation",
)
