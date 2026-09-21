"""services.entitlement_service_v1.cascade_selector · ENT-19/26/34 · Cascade selection.

ENT-19 (§6 verbatim): "Where a model is reachable under more than one access
class for the same licence — reseller-frontier and customer-key — the
customer-key row is selected. The buyer's own key is preferred over platform
capacity whenever both exist."

ENT-26 (§8 verbatim): "When allowance is exhausted, the cascade (D-16) stops
escalating to reseller-frontier rows and serves the job on a local-served row.
The response carries the fixed string 'Frontier allowance used · served
locally'. It MUST NOT serve locally without the string, and it MUST NOT
refuse the job when a local-served row can serve it." [A5.5; D-16]

ENT-34 (§10 verbatim): "A reseller channel that is unreachable or refuses is
a closed gate for that row. The cascade serves the job on a local-served row
with the fixed string 'Frontier unavailable · served locally', or refuses if
no local-served row can serve it. It never retries silently on a different
provider." [FP-2; A5.5]

Fixed strings (BINDING · byte-verbatim from custody docx sha256 `46c3670e…`
§7 ENT-23 · §8 ENT-26 · §10 ENT-34 · cross-check byte-match against specialist
`/app/frontend/src/strings/entitlementStrings.js` verified at extraction receipt
`phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log`).
Middle-dot character is U+00B7 (UTF-8 `c2 b7`), same code point as the JS
`\\u00b7` escape.

Reseller-frontier CHANNEL HARD HOLD at this wave: this module SELECTS the
cascade path (customer-key vs local-served vs refuse) but does NOT invoke a
reseller channel — that lives at the unbuilt `reseller_channel.py` module
gated behind R-24 counsel-reviewed reseller agreement per ENT-32 verbatim
'A reseller-frontier row MUST NOT be set to listed before the agreement
covering its provider is on record.'
"""
from __future__ import annotations

from typing import List, Optional, Tuple

from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.licence import Licence


# ENT-26 fixed string · BINDING · byte-verbatim from spec docx §8
# Written with the literal U+00B7 middle-dot character (UTF-8 c2 b7) so the
# raw source bytes match the docx paragraph body and the ENT_26_FRONTIER_EXHAUSTION
# JS register constant byte-for-byte.
ENT_26_FRONTIER_EXHAUSTION_FIXED_STRING: str = "Frontier allowance used · served locally"

# ENT-34 fixed string · BINDING · byte-verbatim from spec docx §10
# Written with the literal U+00B7 middle-dot character (UTF-8 c2 b7).
ENT_34_FRONTIER_UNAVAILABLE_FIXED_STRING: str = "Frontier unavailable · served locally"


class CascadeRefusal(RuntimeError):
    """ENT-34 verbatim second clause: 'or refuses if no local-served row
    can serve it. It never retries silently on a different provider.'
    """


def select_cascade(
    *,
    licence: Licence,
    candidate_rows: List[CatalogRow],
    allowance_exhausted: bool,
    reseller_unreachable: bool = False,
) -> Tuple[CatalogRow, Optional[str]]:
    """ENT-19/26/34 · Cascade selection at chokepoint.

    Arguments:
      · licence  — the resolved Licence attached to the calling org
      · candidate_rows — the (>=1) CatalogRow(s) that the caller has
                          identified as reachable for the requested model
                          (may include customer-key + reseller-frontier +
                          local-served + customer-model access classes)
      · allowance_exhausted — the chokepoint_resolver returned an
                          ENT-16-step-6 refusal on reseller-frontier due
                          to `credits_remaining <= 0` (ENT-22 derived)
      · reseller_unreachable — the reseller channel probe returned
                          unreachable/refused (ENT-34 · at this build wave
                          the reseller channel is HARD HOLD unbuilt · this
                          flag is caller-supplied for FUTURE reseller build)

    Returns (selected_row, fixed_string_if_any):
      · fixed_string is None when a customer-key OR customer-model row is
        selected, OR when a first-choice reseller-frontier row is selected
        without exhaustion.
      · fixed_string is ENT_26_FRONTIER_EXHAUSTION_FIXED_STRING when the
        selection falls back to a local-served row due to allowance
        exhaustion (ENT-26 verbatim).
      · fixed_string is ENT_34_FRONTIER_UNAVAILABLE_FIXED_STRING when the
        selection falls back to a local-served row due to reseller
        unreachable/refused (ENT-34 verbatim).

    Raises CascadeRefusal when no local-served row is available to serve
    (ENT-34 second clause verbatim).

    Selection rules (§6 ENT-19 + §8 ENT-26 + §10 ENT-34):

      1. If a customer-key row EXISTS for this licence (Frontier dial =
         your_keys) and the licence's dials admit it → SELECT that row.
         The buyer's own key is preferred over platform capacity (ENT-19
         verbatim).
      2. Else if the request is for a reseller-frontier row AND
         allowance_exhausted → fall back to a local-served row with
         ENT-26 fixed string. Refuse via CascadeRefusal if no local-served
         row is available (ENT-26 verbatim second clause 'MUST NOT refuse
         the job when a local-served row can serve it').
      3. Else if the request is for a reseller-frontier row AND
         reseller_unreachable → fall back to a local-served row with
         ENT-34 fixed string. Refuse if no local-served row is available.
      4. Else default: SELECT the highest-preference admitted row (first
         customer-model, then local-served, then reseller-frontier).
    """
    # Rule 1 · ENT-19 customer-key preference
    customer_key_rows = [r for r in candidate_rows if r.access_class == "customer_key"]
    if customer_key_rows and licence.frontier_dial == "your_keys":
        return customer_key_rows[0], None

    # Rule 2 · ENT-26 exhaustion cascade to local-served
    reseller_rows = [r for r in candidate_rows if r.access_class == "reseller_frontier"]
    local_rows = [r for r in candidate_rows if r.access_class == "local_served"]
    if reseller_rows and allowance_exhausted:
        if not local_rows:
            raise CascadeRefusal(
                "ENT-26 second clause · allowance exhausted AND no local-served row available · refuse per FP-2."
            )
        return local_rows[0], ENT_26_FRONTIER_EXHAUSTION_FIXED_STRING

    # Rule 3 · ENT-34 reseller unreachable cascade to local-served
    if reseller_rows and reseller_unreachable:
        if not local_rows:
            raise CascadeRefusal(
                "ENT-34 second clause · reseller unreachable AND no local-served row available · refuse per FP-2 · never retries silently on a different provider."
            )
        return local_rows[0], ENT_34_FRONTIER_UNAVAILABLE_FIXED_STRING

    # Rule 4 · default admitted-set preference (customer-model → local → reseller)
    customer_model_rows = [r for r in candidate_rows if r.access_class == "customer_model"]
    if customer_model_rows:
        return customer_model_rows[0], None
    if local_rows:
        return local_rows[0], None
    if reseller_rows and licence.frontier_dial == "managed":
        return reseller_rows[0], None

    # Nothing admitted · cascade refuses (never silently)
    raise CascadeRefusal(
        f"cascade_selector · no admitted candidate row available "
        f"(licence dials compute={licence.compute_dial!r} frontier={licence.frontier_dial!r} · "
        f"candidates access_class={[r.access_class for r in candidate_rows]!r}) · refuse per FP-2."
    )
