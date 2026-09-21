"""services.entitlement_service_v1.catalog · Catalog row surface (§4 ENT-9..13).

ENT-9 (§4 verbatim): "Every catalog row carries: model identifier (a registry
reference, hash-pinned per Doc 20); access class; status ∈ {listed, paused,
retired}; residency; and, for reseller-frontier rows only, one credit rate.
No other pricing field exists on a row." [Doc 20; ENT-1]

ENT-11 (§4 verbatim): "Retiring a model is a status change to retired. Calls
to a retired row refuse with a fixed reason. Receipts citing the row are
unaffected; the row is never deleted." [B.4; DAP-26]

ENT-12 (§4 verbatim): "Re-rating a reseller-frontier row changes one number
through the ordinary ceremony tier, prospectively. A credit rate is never
applied to usage metered before the change took effect." [DAP-26]

ENT-13 (§4 verbatim): "The catalog is read-only to every component except
the ceremony engine. No surface, wizard, or assistant writes a catalog row."
[RBM-5]

Access classes (§1 defined term):
  · local-served — registered open-weight base served on platform or
    connected-tier compute
  · reseller-frontier — frontier capacity supplied through provider reseller
    channel (HARD HOLD pending R-24 · not authored at this build wave)
  · customer-key — frontier model reached under buyer's own provider credential
  · customer-model — registered artefact the buyer brought or trained
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ENT-9 status enum · 3-tuple exactly per spec verbatim
CATALOG_STATUS_LISTED: Literal["listed"] = "listed"
CATALOG_STATUS_PAUSED: Literal["paused"] = "paused"
CATALOG_STATUS_RETIRED: Literal["retired"] = "retired"


# §1 defined term · access class · 4-tuple exactly per spec verbatim
ACCESS_CLASS_LOCAL_SERVED: Literal["local_served"] = "local_served"
ACCESS_CLASS_RESELLER_FRONTIER: Literal["reseller_frontier"] = "reseller_frontier"
ACCESS_CLASS_CUSTOMER_KEY: Literal["customer_key"] = "customer_key"
ACCESS_CLASS_CUSTOMER_MODEL: Literal["customer_model"] = "customer_model"


class CatalogRow(BaseModel):
    """ENT-9 · One catalog row per model.

    Fields verbatim from ENT-9:
      · model identifier (a registry reference, hash-pinned per Doc 20)
      · access class
      · status ∈ {listed, paused, retired}
      · residency
      · for reseller-frontier rows only: one credit rate

    No other pricing field exists on a row (ENT-9 verbatim last sentence).
    Model name starts with 'Catalog' per ENT-49 four-allowed-shapes discipline.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    model_identifier: str = Field(..., min_length=1, description="ENT-9 registry reference hash-pinned per Doc 20.")
    access_class: Literal["local_served", "reseller_frontier", "customer_key", "customer_model"] = Field(
        ..., description="ENT-9 access class · closed 4-tuple per §1 defined term."
    )
    status: Literal["listed", "paused", "retired"] = Field(..., description="ENT-9 status · closed 3-tuple.")
    residency: str = Field(..., min_length=1, description="ENT-9 residency.")

    # ENT-9: "for reseller-frontier rows ONLY, one credit rate"
    # Optional at contract level; enforced at row-level via model_validator.
    credit_rate: Optional[float] = Field(
        default=None,
        ge=0,
        description="ENT-9 credit rate · reseller-frontier rows ONLY · None on other access classes."
    )

    @model_validator(mode="after")
    def _enforce_credit_rate_only_on_reseller_frontier(self) -> "CatalogRow":
        """ENT-9 · credit_rate present iff access_class is reseller-frontier."""
        if self.access_class == "reseller_frontier":
            if self.credit_rate is None:
                raise ValueError(
                    "ENT-9 violation: reseller-frontier row missing credit_rate."
                )
        else:
            if self.credit_rate is not None:
                raise ValueError(
                    f"ENT-9 violation: credit_rate must be None on access_class={self.access_class!r}. "
                    "Reseller-frontier rows only carry credit_rate."
                )
        return self
