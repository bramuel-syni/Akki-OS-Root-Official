"""Adapter snapshots; existing Canon principal/licence/catalogue schemas unchanged."""
from typing import Literal
from pydantic import model_validator
from services.entitlement_service_v1.licence import Licence
from services.entitlement_service_v1.catalog import CatalogRow
from services.northena.execution_models import Authority, Frozen, Name


class Decision(Frozen):
    authority: Authority
    catalog_model_identifier: Name | None = None
    catalog_access_class: Literal["local_served", "customer_model", "customer_key", "reseller_frontier"] | None = None

    @model_validator(mode="after")
    def paired_selection(self):
        if (self.catalog_model_identifier is None) != (self.catalog_access_class is None):
            raise ValueError("Catalogue identifier and access class must be selected together.")
        return self


class CommercialSnapshot(Frozen):
    licence: Licence
    catalog_row: CatalogRow | None
    period_iso: Name
    principal_id: Name


class Prepared(Frozen):
    authority: Authority
    commercial_snapshot: CommercialSnapshot

    @model_validator(mode="after")
    def same_binding(self):
        if (self.authority.principal_id != self.commercial_snapshot.principal_id
                or self.authority.terms_ref != self.commercial_snapshot.licence.terms_identifier):
            raise ValueError("Commercial snapshot must match the operation authority.")
        return self