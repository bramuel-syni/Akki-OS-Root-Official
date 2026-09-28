"""services.principal_store — CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9.

Principal store implementing PRIN-1..PRIN-4 (spec §2):
    PRIN-1  Three principal kinds (organisation · individual · agent);
            individual/agent MUST reference an organisation.
    PRIN-2  Admission is a governed act; no principal self-admits.
    PRIN-3  Behavioural-signature state present from admission (not
            deferred).
    PRIN-4  Mandate immutable once frozen at admission (Northena
            Promise #32 objective-freeze mechanism).

Additive-only per SO §3.8. New module; no sealed contract or writer edited.
"""
from __future__ import annotations

from services.principal_store.store import (
    PRINCIPAL_KINDS,
    Principal,
    PrincipalRefusal,
    admit_agent,
    admit_individual,
    admit_organisation,
    admit_organisation_for_test_fixture,
    get_principal,
)

__all__ = (
    "PRINCIPAL_KINDS",
    "Principal",
    "PrincipalRefusal",
    "admit_agent",
    "admit_individual",
    "admit_organisation",
    "admit_organisation_for_test_fixture",
    "get_principal",
)
