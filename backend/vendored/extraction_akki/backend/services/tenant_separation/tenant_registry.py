"""services.tenant_separation.tenant_registry · canonical 4-tenant roster.

Owner card §2 verbatim (STATE/OBJECTIVES/TENANT_SEPARATION.md):

    "RMS — organisation principal, own trust-domain identifier, own
    Ledger, own context key, own licence. DIGICOW — same, independently.
    AKKI-TEST — a dedicated test tenant for systems testing. Synthetic
    data only. Never holds RMS or DigiCow content.
    AUDIT-FIXTURE-20260921 — as already exists; unchanged."

Owner card §3 verbatim (data assignment):

    "Each connector record, each census artefact (census_0001/0002 →
    DIGICOW; Item-3 receipts → RMS), each source_inventory row, each
    stratified sample, each cost receipt carries its tenant_id via the
    akki.data primitive — auto-injected, never caller-supplied (M11,
    AKKI-DATA-001). A source with no tenant does not exist to the
    platform."

Owner card §7 verbatim (UI/UX unchanged):

    "Tenant context is set at sign-in from the principal and never
    selectable in the UI."

Closed-vocab per SO §3.10-α; authoritative source is
`contracts/canonical_tenant_ids.schema.json`; the Python tuple is a
mirror of the schema enum · paired equality asserted by the CP invariant
test.
"""

from __future__ import annotations

from typing import Any, Dict, Final, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# Canonical tenant vocabulary — SO §3.10-α closed set
# ═══════════════════════════════════════════════════════════════════════════

CANONICAL_TENANT_IDS: Final[Tuple[str, ...]] = (
    "RMS",
    "DIGICOW",
    "AKKI-TEST",
    "AUDIT-FIXTURE-20260921",
)

CANONICAL_TENANT_COUNT: Final[int] = 4

TENANT_ROLES: Final[Dict[str, str]] = {
    "RMS": "legal_entity_customer",
    "DIGICOW": "legal_entity_customer",
    "AKKI-TEST": "systems_test_synthetic",
    "AUDIT-FIXTURE-20260921": "audit_fixture",
}

# Owner card §7 verbatim: tenant context is set at sign-in from the
# principal and never selectable in the UI. This constant pins the
# derivation source name so invariants can assert against it.
TENANT_CONTEXT_DERIVATION: Final[str] = "sign_in_principal"


# ═══════════════════════════════════════════════════════════════════════════
# Source roster — owner card §3 verbatim
# ═══════════════════════════════════════════════════════════════════════════

# Each row is the additive declaration of which tenant a named source
# belongs to. Runtime auto-injection of `tenant_id` happens via the
# sealed `services.data.repository` M11 primitive (AKKI-DATA-001); this
# roster is the platform-facing manifest of tenant/source binding.
SOURCE_ROSTER: Final[Tuple[Dict[str, Any], ...]] = (
    # RMS — owner card §3 verbatim.
    {"source_name": "weego_mysql", "tenant_id": "RMS", "kind": "mysql"},
    {"source_name": "ussd_mysql", "tenant_id": "RMS", "kind": "mysql"},
    {"source_name": "citizen_digital_mysql", "tenant_id": "RMS", "kind": "mysql"},
    {"source_name": "visitors_mysql", "tenant_id": "RMS", "kind": "mysql"},
    {"source_name": "nas_16_channels_smb", "tenant_id": "RMS", "kind": "smb"},
    {
        "source_name": "obs_google_transcripts",
        "tenant_id": "RMS",
        "kind": "obs_object_read_only",
    },
    {"source_name": "razuna_newsvault", "tenant_id": "RMS", "kind": "razuna"},
    # DigiCow — owner card §3 verbatim.
    {
        "source_name": "digicow_live",
        "tenant_id": "DIGICOW",
        "kind": "digicow_operational",
    },
    {"source_name": "ndume", "tenant_id": "DIGICOW", "kind": "digicow_call_audio"},
    # AKKI-TEST — synthetic only (owner card §2 verbatim).
    {
        "source_name": "akki_test_synthetic_pack",
        "tenant_id": "AKKI-TEST",
        "kind": "synthetic",
        "data_class": "synthetic",
    },
    # AUDIT-FIXTURE-20260921 — unchanged per owner card §2 verbatim.
    {
        "source_name": "audit_fixture_20260921_bundle",
        "tenant_id": "AUDIT-FIXTURE-20260921",
        "kind": "audit_fixture_bundle",
    },
)


__all__ = (
    "CANONICAL_TENANT_IDS",
    "CANONICAL_TENANT_COUNT",
    "SOURCE_ROSTER",
    "TENANT_CONTEXT_DERIVATION",
    "TENANT_ROLES",
)
