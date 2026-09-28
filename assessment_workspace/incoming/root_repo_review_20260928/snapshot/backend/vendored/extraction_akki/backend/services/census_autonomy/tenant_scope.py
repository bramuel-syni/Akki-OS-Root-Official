"""Adapter over the sealed CP-TENANT-SEPARATION carrier (4j Commit-A).

Owner R-106 §3 verbatim (banked in STATE/DECISIONS.md at 4k Commit-B
f775adf6):

> "The census engine productized: port the estate_census v3 logic into
> backend services (additive; adapters over the sealed data_source
> packages), tenant-scoped from birth, LawfulBasisAdmit + all-reads-
> receipted + no-second-store invariants enforced in the service path,
> bounded/budgeted per run."

This module is a THIN adapter over sealed
`services.tenant_separation.tenant_registry` (4j eed6c032a):
- Read-only exports of `CANONICAL_TENANT_IDS` + `TENANT_ROLES` +
  `TENANT_CONTEXT_DERIVATION`.
- Adds census-scoped helpers (`is_census_admitted_tenant`,
  `resolve_tenant_from_principal`) WITHOUT modifying the sealed carrier.

Zero writer verbs — this is read-only tenant identity resolution.
"""

from __future__ import annotations

from typing import Final, Mapping, Tuple

# READ-ONLY import of sealed 4j Commit-A eed6c032a carrier. Do NOT
# rebind these; they are Final constants in the sealed module.
from services.tenant_separation.tenant_registry import (  # noqa: E402
    CANONICAL_TENANT_IDS,
    TENANT_CONTEXT_DERIVATION,
    TENANT_ROLES,
)

# ---------------------------------------------------------------------------
# Census-admission set (adapter · additive · does NOT edit sealed carrier)
# ---------------------------------------------------------------------------
#
# Named-but-unseated approving authorities (DQ-19 RMS + DQ-20 DIGICOW)
# are excluded from census-admission until custody-material drop per
# R-104 §4.1 §F (see STATE/DECISIONS.md at 4j Commit-B 8998e173).
# Only 'seated_named' tenants and the AKKI-TEST fixture are census-
# admitted this-slice.
CENSUS_ADMITTED_TENANT_IDS: Final[Tuple[str, ...]] = tuple(
    t for t in CANONICAL_TENANT_IDS
    if TENANT_ROLES.get(t) not in ("named_but_unseated",)
)


def is_census_admitted_tenant(tenant_id: str) -> bool:
    """Return True iff tenant_id is admitted for census-autonomy runs.

    Named-but-unseated tenants (RMS + DIGICOW per DQ-19/DQ-20) return
    False until owner custody-material drop per R-104.
    """
    return tenant_id in CENSUS_ADMITTED_TENANT_IDS


def resolve_tenant_from_principal(principal: Mapping[str, str]) -> str:
    """Derive tenant_id from a signed-in principal payload.

    Uses TENANT_CONTEXT_DERIVATION='sign_in_principal' discipline from
    the sealed carrier — the principal payload's 'tenant_id' field IS
    the tenant identity source (Principal Model Spec v1 PRIN-11
    propagation).
    """
    if TENANT_CONTEXT_DERIVATION != "sign_in_principal":
        # Defensive: sealed constant should never mutate; fail-loud if
        # someone edits the sealed carrier (§3.8 violation detector).
        raise RuntimeError(
            f"Sealed TENANT_CONTEXT_DERIVATION mutated to "
            f"{TENANT_CONTEXT_DERIVATION!r} — SO §3.8 violated; "
            f"regen and reseal"
        )
    tenant_id = principal.get("tenant_id", "")
    if not tenant_id:
        raise ValueError("principal missing tenant_id — refusal required")
    return tenant_id
