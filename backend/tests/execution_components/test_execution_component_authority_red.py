"""RED-first contracts for services.northena.execution_authority.ComponentAuthority."""

from __future__ import annotations

import asyncio
import importlib

import pytest

from contracts.principal_v1 import PrincipalKind, PrincipalV1
from services.enforce.control_scope import bind_control_scope, require_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.entitlement_service_v1.allowance import LicenceAllowanceState
from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.licence import Licence
from services.northena.execution_models import Held, Request
from services.portal_operational.entitlements import LicencePortalView
from services.principal_store.store import Principal


def _module():
    try:
        return importlib.import_module("services.northena.execution_authority")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_authority: {exc}")


def _component_models_module():
    try:
        return importlib.import_module("services.northena.execution_component_models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_component_models: {exc}")


def _request(*, kind="source", engine="mtafiti") -> Request:
    return Request(
        request_id=f"req-{kind}",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind=kind,
        engine=engine,
        objective_sha256="a" * 64,
        input_refs=("akki://source/rms",),
        scope_refs=("scope://allowed",),
        deadline_epoch=9_999_999_999,
        result_floor="non_factual" if kind == "skill" else None,
    )


def _licence(*, status="active", org_id="org-1", terms="terms://dispatch/v1") -> Licence:
    return Licence(
        plan_identifier="plan-v1",
        organisation_principal_id=org_id,
        seat_count=10,
        compute_dial="managed",
        frontier_dial="managed",
        credits_per_seat_per_period=100,
        pooled_credits_flag=True,
        seat_soft_limit=8,
        organisation_ceiling=1000,
        period="month",
        renewal_date="2099-01-01T00:00:00+00:00",
        status=status,
        terms_identifier=terms,
    )


def _principal(principal_id: str, *, kind: PrincipalKind, parent_org: str | None, suspended: bool = False) -> Principal:
    return Principal(
        PrincipalV1(
            principal_id=principal_id,
            kind=kind,
            legal_identity=principal_id,
            trust_domain_identifier="td-1",
            admission_time_mandate="mandate",
            behavioural_signature_state="watch:baseline@admission",
            parent_organisation_id=parent_org,
            autonomy_scope=None,
            admit_authority=False,
            suspended=suspended,
        )
    )


def _resolved_view(*, principal_id: str = "principal-1", include_catalog: bool = True) -> LicencePortalView:
    rows = []
    if include_catalog:
        rows = [
            CatalogRow(
                model_identifier="model://northena/m1",
                access_class="customer_model",
                status="listed",
                residency="eu",
                credit_rate=None,
            )
        ]
    return LicencePortalView(
        principal_id=principal_id,
        status="resolved",
        reason_code="",
        licence=_licence(),
        allowance_state=LicenceAllowanceState(
            licence_terms_id="terms://dispatch/v1",
            period_iso="2026-09",
            credits_debited=10,
            credits_allowance=1000,
            credits_remaining=990,
        ),
        rows=rows,
        badges=list(rows),
        count=len(rows),
    )


class _Decisions:
    def __init__(self, mod_models, terms="terms://dispatch/v1", catalog_model_identifier=None, catalog_access_class=None):
        self.mod_models = mod_models
        self.terms = terms
        self.catalog_model_identifier = catalog_model_identifier
        self.catalog_access_class = catalog_access_class

    async def resolve(self, request, phase, principal, licence_view):
        from services.northena.execution_models import Authority

        authority = Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=principal.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=9_999_999_999,
            terms_ref=self.terms,
            policy_epoch=1,
        )
        return self.mod_models.Decision(
            authority=authority,
            catalog_model_identifier=self.catalog_model_identifier,
            catalog_access_class=self.catalog_access_class,
        )


# Module/feature: prepare binds typed principal/licence decision into Prepared snapshot.
def test_component_authority_prepare_binds_typed_principal_licence_and_terms(monkeypatch):
    mod = _module()
    cm = _component_models_module()

    principal = _principal("principal-1", kind=PrincipalKind.INDIVIDUAL, parent_org="org-1")
    org = _principal("org-1", kind=PrincipalKind.ORGANISATION, parent_org=None)

    async def _read_view(_db, _scope):
        scope = require_control_scope()
        assert scope.principal_id == "principal-1"
        assert scope.tenant_id == "DIGICOW"
        return _resolved_view(principal_id="principal-1", include_catalog=True)

    monkeypatch.setattr(mod, "read_view", _read_view)
    lookup = lambda pid: principal if pid == "principal-1" else org
    decisions = _Decisions(cm, catalog_model_identifier="model://northena/m1", catalog_access_class="customer_model")
    authority = mod.ComponentAuthority(db=object(), decisions=decisions, principal_lookup=lookup, clock=lambda: 100)

    request = _request(kind="source", engine="mtafiti")
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            prepared = asyncio.run(authority.prepare(request))
    assert prepared.authority.terms_ref == prepared.commercial_snapshot.licence.terms_identifier
    assert prepared.commercial_snapshot.principal_id == "principal-1"
    assert prepared.commercial_snapshot.period_iso == "2026-09"


# Module/feature: authority exposes typed context(request)->(PrincipalV1, LicencePortalView).
def test_component_authority_context_returns_typed_principal_and_resolved_view(monkeypatch):
    mod = _module()
    cm = _component_models_module()

    principal = _principal("principal-1", kind=PrincipalKind.INDIVIDUAL, parent_org="org-1")
    org = _principal("org-1", kind=PrincipalKind.ORGANISATION, parent_org=None)
    lookup = lambda pid: principal if pid == "principal-1" else org

    async def _read_view(_db, _scope):
        return _resolved_view(principal_id="principal-1", include_catalog=True)

    monkeypatch.setattr(mod, "read_view", _read_view)
    authority = mod.ComponentAuthority(db=object(), decisions=_Decisions(cm), principal_lookup=lookup, clock=lambda: 100)

    request = _request(kind="source", engine="mtafiti")
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            principal_ctx, view = asyncio.run(authority.context(request))

    assert isinstance(principal_ctx, PrincipalV1)
    assert isinstance(view, LicencePortalView)
    assert view.allowance_state is not None
    assert view.allowance_state.period_iso == "2026-09"


# Module/feature: prepare refuses when required principal/scope context is not bound.
def test_component_authority_prepare_refuses_without_bound_control_context(monkeypatch):
    mod = _module()
    cm = _component_models_module()
    principal = _principal("principal-1", kind=PrincipalKind.INDIVIDUAL, parent_org="org-1")
    org = _principal("org-1", kind=PrincipalKind.ORGANISATION, parent_org=None)
    lookup = lambda pid: principal if pid == "principal-1" else org

    async def _read_view(_db, _scope):
        _ = require_control_scope()
        return _resolved_view(principal_id="principal-1", include_catalog=True)

    monkeypatch.setattr(mod, "read_view", _read_view)
    authority = mod.ComponentAuthority(db=object(), decisions=_Decisions(cm), principal_lookup=lookup, clock=lambda: 100)

    with pytest.raises(Exception):
        asyncio.run(authority.prepare(_request(kind="source", engine="mtafiti")))


# Module/feature: unresolved/suspended/mismatched principal-licence paths are held, not admitted.
def test_component_authority_refuses_unresolved_or_mismatched_states(monkeypatch):
    mod = _module()
    cm = _component_models_module()

    suspended = _principal("principal-1", kind=PrincipalKind.INDIVIDUAL, parent_org="org-1", suspended=True)
    org = _principal("org-1", kind=PrincipalKind.ORGANISATION, parent_org=None)
    lookup = lambda pid: suspended if pid == "principal-1" else org

    async def _unresolved(_db, _scope):
        return LicencePortalView(principal_id="principal-1", status="unresolved", reason_code="LICENCE_UNRESOLVED")

    monkeypatch.setattr(mod, "read_view", _unresolved)
    authority = mod.ComponentAuthority(db=object(), decisions=_Decisions(cm), principal_lookup=lookup, clock=lambda: 100)
    request = _request()
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            with pytest.raises(Held):
                asyncio.run(authority.prepare(request))

    # This contract is refusal-first for unresolved and suspension paths.
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            with pytest.raises(Held):
                asyncio.run(authority.authorize(request, "dispatch"))


# Module/feature: model operations require exact decision catalog row binding, no default approval.
def test_component_authority_model_kind_requires_exact_catalog_decision(monkeypatch):
    mod = _module()
    cm = _component_models_module()

    principal = _principal("principal-1", kind=PrincipalKind.INDIVIDUAL, parent_org="org-1")
    org = _principal("org-1", kind=PrincipalKind.ORGANISATION, parent_org=None)

    async def _view(_db, _scope):
        return _resolved_view(principal_id="principal-1", include_catalog=False)

    monkeypatch.setattr(mod, "read_view", _view)
    lookup = lambda pid: principal if pid == "principal-1" else org
    authority = mod.ComponentAuthority(db=object(), decisions=_Decisions(cm), principal_lookup=lookup, clock=lambda: 100)

    request = _request(kind="skill", engine="solva")
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            with pytest.raises(Held):
                asyncio.run(authority.prepare(request))
