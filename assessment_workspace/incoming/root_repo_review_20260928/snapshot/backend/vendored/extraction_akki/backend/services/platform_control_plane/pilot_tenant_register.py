"""services.platform_control_plane.pilot_tenant_register — CP-P6-CP4 · M9.

Pilot-tenant register carrier + preventive-charter refusal wrapper
per Akki OS Pilot Platform Reference v0.2 §5 + Row 209:

    §5 (§11): pilot tenant register table lists RMS · DigiCow · BDO
    · Trinity with per-field capture-at-provisioning placeholders.
    Row 209: Refusal on missing capture-at-provisioning where
    marked.

Design note: per §5 canon table lines 127-130 the tenant descriptor
fields (estates / tier / compute / identity / initial_apps) hold
either concrete descriptions or the literal placeholder token
"*capture at provisioning*". The CP shape-freezes the 4 tenant
keys, the 5 descriptor field names, and the sentinel token; the
concrete descriptions are opaque ref strings CONTRACT-MODELED at
caller (loaded from §5 canon at run time · avoids per-tenant
description literals in the platform layer).

Vocabulary:
- PILOT_TENANT_KEYS = ("RMS", "DigiCow", "BDO", "Trinity").
- CAPTURE_AT_PROVISIONING_SENTINEL = "*capture at provisioning*".

Refusals:
1. record.tenant_key not in PILOT_TENANT_KEYS →
   UnknownPilotTenantKeyRefused (case-sensitive).
2. any of the 5 descriptor fields equals sentinel →
   MissingCaptureAtProvisioningRefused (Row 209).

Standing-line proof:
- 6 str · 6 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


PILOT_TENANT_REGISTER_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §5 "
    "+ Row 209: pilot tenant register — RMS · DigiCow · BDO · "
    "Trinity records; refusal on missing capture-at-provisioning "
    "where marked (sentinel '*capture at provisioning*')."
)


# §5 canon table verbatim tenant keys.
PILOT_TENANT_KEYS: Tuple[str, ...] = (
    "RMS",
    "DigiCow",
    "BDO",
    "Trinity",
)


# §5 canon verbatim placeholder token.
CAPTURE_AT_PROVISIONING_SENTINEL: str = "*capture at provisioning*"


# Descriptor field names that MUST be filled at provisioning.
PILOT_TENANT_DESCRIPTOR_FIELDS: Tuple[str, ...] = (
    "estates_ref",
    "tier_ref",
    "compute_ref",
    "identity_ref",
    "initial_apps_ref",
)


@dataclasses.dataclass(frozen=True)
class PilotTenantRecord:
    """Frozen carrier for a pilot-tenant register entry.

    Exact-order 6 str OPEN fields:
    - tenant_key · one of PILOT_TENANT_KEYS.
    - estates_ref · opaque ref (CAPTURE sentinel when unset).
    - tier_ref · opaque ref (CAPTURE sentinel when unset).
    - compute_ref · opaque ref (CAPTURE sentinel when unset).
    - identity_ref · opaque ref (CAPTURE sentinel when unset).
    - initial_apps_ref · opaque ref (CAPTURE sentinel when unset).
    """
    tenant_key: str
    estates_ref: str
    tier_ref: str
    compute_ref: str
    identity_ref: str
    initial_apps_ref: str


PILOT_TENANT_RECORD_FIELDS: Tuple[str, ...] = (
    "tenant_key",
    "estates_ref",
    "tier_ref",
    "compute_ref",
    "identity_ref",
    "initial_apps_ref",
)


class PilotTenantRegisterRefused(Exception):
    """Root refusal for pilot-tenant-register invariants."""


class UnknownPilotTenantKeyRefused(PilotTenantRegisterRefused):
    """Refused: tenant_key not in PILOT_TENANT_KEYS (case-sensitive)."""


class MissingCaptureAtProvisioningRefused(PilotTenantRegisterRefused):
    """Refused: at least one descriptor field still holds the
    CAPTURE_AT_PROVISIONING_SENTINEL (Row 209)."""


def assert_pilot_record_valid(
    *, record: PilotTenantRecord,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. tenant_key not in PILOT_TENANT_KEYS → UnknownPilotTenantKeyRefused.
    2. any descriptor field == CAPTURE_AT_PROVISIONING_SENTINEL →
       MissingCaptureAtProvisioningRefused.

    Returns None on admit."""
    if record.tenant_key not in frozenset(PILOT_TENANT_KEYS):
        raise UnknownPilotTenantKeyRefused(
            f"unknown-pilot-tenant-key refused: tenant_key not "
            f"among {len(PILOT_TENANT_KEYS)} §5 keys (case-sensitive)."
        )
    for fname in PILOT_TENANT_DESCRIPTOR_FIELDS:
        if getattr(record, fname) == CAPTURE_AT_PROVISIONING_SENTINEL:
            raise MissingCaptureAtProvisioningRefused(
                f"missing-capture-at-provisioning refused: "
                f"descriptor field at position "
                f"{PILOT_TENANT_DESCRIPTOR_FIELDS.index(fname)} "
                f"still holds the §5 sentinel · Row 209."
            )
    return None


__all__ = [
    "PILOT_TENANT_REGISTER_ANCHOR",
    "PILOT_TENANT_KEYS",
    "CAPTURE_AT_PROVISIONING_SENTINEL",
    "PILOT_TENANT_DESCRIPTOR_FIELDS",
    "PILOT_TENANT_RECORD_FIELDS",
    "PilotTenantRecord",
    "PilotTenantRegisterRefused",
    "UnknownPilotTenantKeyRefused",
    "MissingCaptureAtProvisioningRefused",
    "assert_pilot_record_valid",
]
