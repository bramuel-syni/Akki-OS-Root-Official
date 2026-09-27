"""RED-first contracts for new execution component model adapters."""

from __future__ import annotations

import importlib

import pytest

from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.licence import Licence
from services.northena.execution_models import Authority


def _module():
    try:
        return importlib.import_module("services.northena.execution_component_models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_component_models: {exc}")


def _authority() -> Authority:
    return Authority(
        authority_ref="auth://req-1",
        request_sha256="a" * 64,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        scope_refs=("scope://allowed",),
        engine="mtafiti",
        expires_epoch=9_999_999_999,
        terms_ref="terms://dispatch/v1",
        policy_epoch=1,
    )


def _licence() -> Licence:
    return Licence(
        plan_identifier="plan-v1",
        organisation_principal_id="org-1",
        seat_count=10,
        compute_dial="managed",
        frontier_dial="managed",
        credits_per_seat_per_period=100,
        pooled_credits_flag=True,
        seat_soft_limit=8,
        organisation_ceiling=1000,
        period="month",
        renewal_date="2099-01-01T00:00:00+00:00",
        status="active",
        terms_identifier="terms://dispatch/v1",
    )


def _catalog_row() -> CatalogRow:
    return CatalogRow(
        model_identifier="model://northena/m1",
        access_class="customer_model",
        status="listed",
        residency="eu",
        credit_rate=None,
    )


# Module/feature: Decision + CommercialSnapshot + Prepared typed/frozen contracts.
def test_component_models_expose_expected_typed_shapes_and_freeze_contract():
    mod = _module()

    decision = mod.Decision(authority=_authority(), catalog_model_identifier="model://northena/m1", catalog_access_class="customer_model")
    snapshot = mod.CommercialSnapshot(
        licence=_licence(),
        catalog_row=_catalog_row(),
        period_iso="2026-09",
        principal_id="principal-1",
    )
    prepared = mod.Prepared(authority=_authority(), commercial_snapshot=snapshot)

    assert decision.authority.principal_id == "principal-1"
    assert prepared.commercial_snapshot.licence.terms_identifier == prepared.authority.terms_ref

    with pytest.raises(Exception):
        mod.Decision(authority=_authority(), licence_admitted=True)  # forbidden legacy dict-style flag


# Module/feature: CommercialSnapshot allows explicit non-model source consumption handoff.
def test_snapshot_allows_catalog_row_none_without_fabricating_model_pricing():
    mod = _module()
    snapshot = mod.CommercialSnapshot(
        licence=_licence(),
        catalog_row=None,
        period_iso="2026-09",
        principal_id="principal-1",
    )
    assert snapshot.catalog_row is None
