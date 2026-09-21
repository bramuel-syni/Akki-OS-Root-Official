"""services.trust_domain — CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9.

Trust-domain boundary implementing PRIN-9..PRIN-10 (spec §4):
    PRIN-9   Principal's domain and estate's domain share no identifier
             resolution, no store, no credential (verbatim DAP-5).
    PRIN-10  Every record the platform writes on a principal's behalf
             carries that principal's trust-domain identifier; a write
             with no resolvable trust-domain identifier is refused,
             not defaulted to the estate's own domain.

Additive-only per SO §3.8.  Sibling of DAP-5's TrustDomainCrossingAttempt
in contracts.dap; that shape is consumed by DAP's own admission ceremony
from a separate specification.
"""
from __future__ import annotations

from services.trust_domain.boundary import (
    TrustDomainRefusal,
    resolve_estate_identifier_into_principal_domain,
    write_on_principal_behalf,
)

__all__ = (
    "TrustDomainRefusal",
    "resolve_estate_identifier_into_principal_domain",
    "write_on_principal_behalf",
)
