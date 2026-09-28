"""W-DAP-STACK 2B · trust-domain boundary primitive.

Canon anchor · DAP-Spec DAP-5 (verbatim): 'DAP is a trust-domain boundary.
The external party's domain and the estate's domain share no identifier
resolution, no store, and no credential.  A unit identifier meaningful
inside the estate MUST NOT resolve to anything in the party's domain
except through an operation §4 permits.'

Thin kernel — records refused cross-domain resolutions.  §4 op set is the
formal admission channel (owner-adjustable in later sub-waves).
"""

from __future__ import annotations

import datetime
from typing import List, Optional

from contracts.dap import TrustDomainCrossingAttempt

# §4-permitted operation names (spine · verbatim from DAP-Spec §4 Table 2).
_PERMITTED_OPS = frozenset({
    "browse_estate",
    "connect_workspace",
    "processed_intelligence",
    "fine_tune_model",
    "develop_skills",
    "download_raw_data",
})

_ATTEMPTS: List[TrustDomainCrossingAttempt] = []


def resolve_estate_unit_from_party_domain(
    *,
    unit_id: str,
    party_principal_id: str,
    operation: Optional[str],
) -> str:
    """Attempt to resolve `unit_id` from the party's domain.

    Refuses when `operation` is not in the §4 permitted set (DAP-5).  Every
    attempt — refused or not — is recorded (DAP-5 tail).
    """
    permitted = operation in _PERMITTED_OPS if operation else False
    # Look up the party's trust domain via admission register.
    from services.dap.admission import _PARTY_REGISTER, _ORG_REGISTER  # type: ignore
    party = _PARTY_REGISTER.get(party_principal_id)
    party_td = "unknown"
    estate_td = "estate:default"
    if party is not None:
        org = _ORG_REGISTER.get(party.parent_org_id)
        if org is not None:
            party_td = org.trust_domain_id
    attempt = TrustDomainCrossingAttempt(
        party_trust_domain_id=party_td,
        estate_trust_domain_id=estate_td,
        attempted_unit_id=unit_id,
        permitted_operation=operation if permitted else None,
    )
    _ATTEMPTS.append(attempt)
    if not permitted:
        raise PermissionError(
            f"DAP-5 refusal: cross-domain resolution of {unit_id!r} outside "
            f"a §4-permitted operation. attempt recorded."
        )
    return unit_id  # would resolve; not exercised in 2B.


def recorded_attempts() -> List[TrustDomainCrossingAttempt]:
    return list(_ATTEMPTS)


def reset_state() -> None:
    """Test-only helper."""
    _ATTEMPTS.clear()
