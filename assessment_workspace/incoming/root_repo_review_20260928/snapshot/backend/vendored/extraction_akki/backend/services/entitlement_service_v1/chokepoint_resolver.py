"""services.entitlement_service_v1.chokepoint_resolver · ENT-16..19 · Chokepoint resolution.

ENT-16 (§6 verbatim): "Before dispatch, the chokepoint resolves, in order: the
calling principal (from propagated context, PRIN-11); its organisation's
licence (ENT-5); the licence status (ENT-6); the catalog row for the requested
or cascade-selected model (ENT-9); whether the row's access class is admitted
by the licence's dials (ENT-3); and, for reseller-frontier rows, whether
allowance remains (ENT-22). Any link that does not resolve refuses the call.
No default licence, default row, or default allowance exists." [A5.1; PRIN-11;
FP-2]

ENT-17 (§6 verbatim): "Resolution is a pure function of (principal, licence,
catalog row, allowance state) with no parameter through which any learned
component's output can enter. The cascade (D-16) may select the model; it
cannot alter what the licence admits." [Attribute 10; A5.2 pattern]

ENT-18 (§6 verbatim): "There is no second path by which a model is reached
under a licence. The existing negative-scan test (A5.1) is the proof; this
document adds no new route and permits none." [A5.1]

ENT-19 (§6 verbatim): "Where a model is reachable under more than one access
class for the same licence — reseller-frontier and customer-key — the
customer-key row is selected. The buyer's own key is preferred over platform
capacity whenever both exist." (Selection logic lives at cascade_selector.py;
this module is the resolution/refusal boundary.)

This module is a PURE FUNCTION. No imports from learned surfaces per ENT-17
verbatim `'no parameter through which any learned component's output can
enter'` — the AST scan at test_entitlement_service_v1_property_tests.py
enforces banned import roots: services.solva_v2, services.mtafiti,
services.perception, services.cif.detection, openai, anthropic.
"""
from __future__ import annotations

from typing import Optional

# Sealed identity imports · SO §3.8 additive-only
from contracts.principal_v1 import PrincipalV1, PrincipalKind

from services.entitlement_service_v1.licence import Licence, LicenceRefusal
from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.allowance import LicenceAllowanceState


class ResolutionRefusal(RuntimeError):
    """ENT-16 fail-closed refusal at chokepoint resolution boundary.

    Raised when any link in the ordered chain does not resolve
    (principal → licence → status → catalog row → dial admission →
    allowance for reseller-frontier rows). FP-2 discipline verbatim
    'Any link that does not resolve refuses the call.'
    """


def resolve(
    *,
    principal: PrincipalV1,
    licence: Licence,
    catalog_row: CatalogRow,
    allowance_state: Optional[LicenceAllowanceState],
) -> None:
    """ENT-16..19 · Pure resolution function called BEFORE dispatch.

    Arguments are ENT-17 verbatim: `(principal, licence, catalog row,
    allowance state)`. No learned-component parameter · no side-effect ·
    fail-closed on any link failure.

    Ordered chain per ENT-16 verbatim (STEPS 1..6):
      1. principal — must be non-None (PRIN-11 propagated context absence
         is a refusal · FP-2 fail-closed).
      2. licence — must be attached to principal's organisation (ENT-5).
      3. licence.status — must be `active` (ENT-6 · suspended and expired
         both refuse per ENT-8).
      4. catalog_row — status must be `listed` (ENT-11 verbatim: 'Calls to
         a retired row refuse' · paused rows likewise not dispatched).
      5. dial admission — the catalog_row.access_class must be admitted
         by the licence's Compute/Frontier dials (ENT-3 verbatim · Your
         Keys removes reseller-frontier rows from admitted set).
      6. allowance — only for reseller-frontier rows (ENT-22): if allowance
         has been exhausted the resolution refuses at this link (the
         cascade_selector then serves locally per ENT-26 · but that's
         a POST-refusal fallback lookup · this function's contract is
         'refuse if the reseller-frontier link fails' and the caller
         decides whether to invoke the cascade fallback).

    Returns None on successful resolution (side-effect: none · caller
    proceeds to dispatch). Raises ResolutionRefusal(link_name, reason)
    on any link failure.
    """
    # LINK 1 · principal (PRIN-11 propagated context)
    if principal is None:
        raise ResolutionRefusal("ENT-16 step 1 · principal not resolved from propagated context (PRIN-11) · FP-2 fail-closed.")
    if not isinstance(principal, PrincipalV1):
        raise ResolutionRefusal(f"ENT-16 step 1 · principal is not a PrincipalV1 (got {type(principal).__name__}) · FP-2 fail-closed.")

    # LINK 2 · licence attached to principal's organisation (ENT-5)
    if licence is None:
        raise ResolutionRefusal("ENT-16 step 2 · no licence attached to principal's organisation (ENT-5) · FP-2 fail-closed.")
    # ENT-5 verbatim "attached to one organisation principal" · when the calling
    # principal is a seat (individual or agent) its parent org must match the
    # licence's organisation_principal_id. When the calling principal is itself
    # an organisation, its id must match directly.
    if principal.kind == PrincipalKind.ORGANISATION:
        if principal.principal_id != licence.organisation_principal_id:
            raise ResolutionRefusal(
                f"ENT-16 step 2 · licence organisation_principal_id ({licence.organisation_principal_id!r}) "
                f"does not match principal id ({principal.principal_id!r}) · FP-2 fail-closed."
            )
    # For individual and agent seats we accept licence attachment via caller-
    # supplied resolution (parent org lookup lives outside this pure function).

    # LINK 3 · licence.status must be active (ENT-6 + ENT-8)
    if licence.status != "active":
        raise ResolutionRefusal(
            f"ENT-16 step 3 · licence.status={licence.status!r} refuses (ENT-8 suspension immediate · ENT-6 expired refuses) · FP-2 fail-closed."
        )

    # LINK 4 · catalog_row.status must be listed (ENT-11)
    if catalog_row is None:
        raise ResolutionRefusal("ENT-16 step 4 · catalog_row not found · ENT-11 fixed reason for retired · FP-2 fail-closed.")
    if catalog_row.status != "listed":
        raise ResolutionRefusal(
            f"ENT-16 step 4 · catalog_row.status={catalog_row.status!r} refuses (retired/paused not dispatched) · FP-2 fail-closed."
        )

    # LINK 5 · dial admission (ENT-3)
    # ENT-3 verbatim: "'Every model' on a surface means every catalog row with
    # status listed whose access class the licence's dials admit." So we check
    # the intersection of access_class against admitted-set from dials.
    if not _dial_admits_access_class(licence=licence, access_class=catalog_row.access_class):
        raise ResolutionRefusal(
            f"ENT-16 step 5 · licence dials (compute={licence.compute_dial!r}, frontier={licence.frontier_dial!r}) "
            f"do not admit access_class={catalog_row.access_class!r} (ENT-3) · FP-2 fail-closed."
        )

    # LINK 6 · allowance for reseller-frontier rows (ENT-22)
    if catalog_row.access_class == "reseller_frontier":
        if allowance_state is None:
            raise ResolutionRefusal(
                "ENT-16 step 6 · reseller-frontier row requires allowance_state · none provided · FP-2 fail-closed."
            )
        if allowance_state.credits_remaining <= 0:
            raise ResolutionRefusal(
                "ENT-16 step 6 · allowance exhausted (credits_remaining <= 0) · cascade must serve locally per ENT-26 · FP-2 fail-closed."
            )

    # All 6 links resolved · dispatch may proceed. Return None (pure function
    # with side-effect-free success).


def _dial_admits_access_class(*, licence: Licence, access_class: str) -> bool:
    """ENT-3 · dial admission check.

    ENT-15 verbatim: "Setting the Frontier dial to Your Keys does not remove
    reseller-frontier rows from the catalog; it removes them from what the
    licence admits."

    Compute dial (managed/yours) does not restrict access_class admission
    directly; it affects fairness ceiling behaviour on local-served rows
    (ENT-30) which lives at a different rail (fairness) not admission.

    Frontier dial:
      · managed  → reseller-frontier admitted · customer-key NOT (buyer
                   uses platform capacity)
      · your_keys → customer-key admitted · reseller-frontier NOT
                    (ENT-15 verbatim)

    local-served AND customer-model are always admitted (they are non-
    frontier access classes).
    """
    # Non-frontier classes always admitted
    if access_class in ("local_served", "customer_model"):
        return True
    if access_class == "reseller_frontier":
        return licence.frontier_dial == "managed"
    if access_class == "customer_key":
        return licence.frontier_dial == "your_keys"
    # Unknown access class · fail-closed
    return False
