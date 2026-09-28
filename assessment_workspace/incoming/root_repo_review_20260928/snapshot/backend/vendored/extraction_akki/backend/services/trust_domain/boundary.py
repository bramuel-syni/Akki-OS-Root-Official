"""services.trust_domain.boundary — Principal Model Spec v1 §4 boundary.

PRIN-9 · PRIN-10 enforcement, additive-only.

PRIN-9 verbatim: 'The principal's domain and the estate's domain share
no identifier resolution, no store, and no credential — verbatim DAP-5.
A unit identifier meaningful inside the estate MUST NOT resolve to
anything in the principal's domain except through an operation the
consuming component's own spec permits.'

PRIN-10 verbatim: 'Every record the platform writes on a principal's
behalf carries that principal's trust-domain identifier.  A write with
no resolvable trust-domain identifier is refused, not defaulted to the
estate's own domain.'

Design notes:
- The default resolution surface refuses.  Spec-permitted operations
  are consuming-component-specific and land in their own specs
  (LIM-3); this module is the base fail-closed floor.
- `write_on_principal_behalf` is an adapter, not an edit to any sealed
  writer.  Consumers of the old writer path continue to work (PRIN-12
  prospective correction discipline).
"""
from __future__ import annotations

from typing import Any, Dict, Optional


class TrustDomainRefusal(RuntimeError):
    """Raised on any trust-domain crossing the boundary refuses.

    PRIN-9 (cross-domain resolution refused) and PRIN-10 (write with no
    resolvable trust-domain identifier refused) both refuse via this
    exception.
    """


def resolve_estate_identifier_into_principal_domain(
    estate_unit_id: str,
    principal_trust_domain: str,
) -> None:
    """PRIN-9 verbatim: default resolution refuses.

    A unit identifier meaningful inside the estate MUST NOT resolve to
    anything in the principal's domain except through an operation the
    consuming component's own spec permits.  This module carries no
    such spec-permitted operation; it is the fail-closed floor.
    """

    raise TrustDomainRefusal(
        f"PRIN-9 · cross-domain resolution refused: estate unit "
        f"{estate_unit_id!r} does not resolve into principal trust "
        f"domain {principal_trust_domain!r} by default.  Any permitted "
        "crossing lives in the consuming component's own spec."
    )


def write_on_principal_behalf(
    principal_id: str,
    record_payload: Dict[str, Any],
    trust_domain_identifier: Optional[str] = None,
) -> Dict[str, Any]:
    """PRIN-10 verbatim: write with no resolvable trust-domain
    identifier is refused, not defaulted to the estate's own domain.

    Returns a `written_record` dict (record_payload + principal_id +
    trust_domain_identifier); no I/O is performed at this layer.
    Storage bindings are consumer-side.
    """

    if not trust_domain_identifier:
        raise TrustDomainRefusal(
            f"PRIN-10 · write refused for principal {principal_id!r}: "
            "no resolvable trust-domain identifier on record.  A write "
            "with no resolvable trust-domain identifier is refused, "
            "not defaulted to the estate's own domain."
        )
    return {
        "principal_id": principal_id,
        "trust_domain_identifier": trust_domain_identifier,
        "payload": record_payload,
    }
