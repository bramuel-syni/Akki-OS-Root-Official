"""services.tenant_separation.oversight_screens · per-tenant Content Registry.

Owner card §5 verbatim (STATE/OBJECTIVES/TENANT_SEPARATION.md):

    "Owner oversight — the data owner sees what the customer is doing.
    One screen family on the tenant console, per tenant, for the estate
    owner's principals only:
    - Every party admitted under the tenant, with mandate and posture
      (DAP-1).
    - The approvals queue — pending, decided, expired — with decision,
      reason and deciding identity (DAP-15; the approver is visible
      here and only here).
    - Cumulative extraction history per party, queryable (DAP-24).
    - Every receipt: operation, units or scope, quantity, terms
      identifier (DAP-21).
    - Release-budget consumption against the ceiling (DAP-35) — shown
      to the owner, never to the party.
    - Standing approvals in force (DAP-17).
    - Suspend-in-one-act (DAP-27).
    Nothing in this view crosses tenants. An RMS owner sees RMS parties
    and nothing of DigiCow, and the reverse."

Owner card §7 verbatim: "Every new string is a Content Registry entry
(CON-1); the oversight screens' headline slots are ranked per CON-15."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Final, Tuple

from services.tenant_separation.tenant_registry import CANONICAL_TENANT_IDS


# ═══════════════════════════════════════════════════════════════════════════
# Seven required oversight surfaces per owner card §5 verbatim
# ═══════════════════════════════════════════════════════════════════════════

OVERSIGHT_SURFACE_IDS: Final[Tuple[str, ...]] = (
    "dap_1_parties",
    "dap_15_approvals_queue",
    "dap_24_cumulative_extraction",
    "dap_21_receipts",
    "dap_35_release_budget_consumption",
    "dap_17_standing_approvals",
    "dap_27_suspend_in_one_act",
)


def _default_surface(tenant_id: str, surface_id: str) -> Dict[str, Any]:
    base = {
        "surface_id": surface_id,
        "scope_tenant_id": tenant_id,
        "cross_tenant_visible": False,
        "tenant_selectable_ui_control": False,  # owner §7 verbatim
        "visible_to_owner": True,
    }
    # Release-budget consumption is shown to owner, never to party (§5 verbatim).
    if surface_id == "dap_35_release_budget_consumption":
        base["visible_to_party"] = False
    else:
        base["visible_to_party"] = True
    return base


_OVERSIGHT_BUNDLES: Final[Dict[str, Dict[str, Dict[str, Any]]]] = {
    tenant_id: {
        surface_id: _default_surface(tenant_id, surface_id)
        for surface_id in OVERSIGHT_SURFACE_IDS
    }
    for tenant_id in CANONICAL_TENANT_IDS
}


# ═══════════════════════════════════════════════════════════════════════════
# Content Registry per-tenant headline entries (CON-1 · CON-15)
# ═══════════════════════════════════════════════════════════════════════════

_CONTENT_REGISTRY_HEADLINES: Final[Dict[str, Dict[str, Dict[str, Any]]]] = {
    tenant_id: {
        surface_id: {
            "con_1_registered": True,
            "con_15_rank": idx + 1,
            "headline_slot": f"{tenant_id}/{surface_id}/HEADLINE",
        }
        for idx, surface_id in enumerate(OVERSIGHT_SURFACE_IDS)
    }
    for tenant_id in CANONICAL_TENANT_IDS
}


def get_oversight_bundle(tenant_id: str) -> Dict[str, Dict[str, Any]]:
    """Return the per-tenant oversight surface bundle.

    Owner card §5 verbatim: "Nothing in this view crosses tenants."
    """
    if tenant_id not in _OVERSIGHT_BUNDLES:
        raise KeyError(
            f"unknown tenant_id: {tenant_id!r} · canonical set is "
            f"{tuple(_OVERSIGHT_BUNDLES.keys())}"
        )
    return _OVERSIGHT_BUNDLES[tenant_id]


def get_content_registry_entries(tenant_id: str) -> Dict[str, Dict[str, Any]]:
    """Return per-tenant Content Registry entries per CON-1 + CON-15."""
    if tenant_id not in _CONTENT_REGISTRY_HEADLINES:
        raise KeyError(
            f"unknown tenant_id: {tenant_id!r} · canonical set is "
            f"{tuple(_CONTENT_REGISTRY_HEADLINES.keys())}"
        )
    return _CONTENT_REGISTRY_HEADLINES[tenant_id]


__all__ = (
    "OVERSIGHT_SURFACE_IDS",
    "get_content_registry_entries",
    "get_oversight_bundle",
)
