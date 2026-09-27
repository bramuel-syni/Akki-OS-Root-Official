"""RED-first contracts for mtafiti execution inspection + canonical registry adapter."""

from __future__ import annotations

import asyncio
import importlib

import pytest

from contracts.principal_v1 import PrincipalKind, PrincipalV1
from services.entitlement_service_v1.allowance import LicenceAllowanceState
from services.entitlement_service_v1.licence import Licence
from services.northena.execution_models import Artifact, Request, Usage, WorkerResult
from services.portal_operational.entitlements import LicencePortalView


def _models_module():
    try:
        return importlib.import_module("services.mtafiti.execution_record_models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.mtafiti.execution_record_models: {exc}")


def _registry_module():
    try:
        return importlib.import_module("services.mtafiti.execution_registry")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.mtafiti.execution_registry: {exc}")


def _request() -> Request:
    return Request(
        request_id="req-registry",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind="source",
        engine="mtafiti",
        objective_sha256="a" * 64,
        input_refs=("akki://source/rms",),
        scope_refs=("scope://allowed",),
        deadline_epoch=9_999_999_999,
    )


def _result(request: Request, *, operation_key: str = "op-1", evidence_mode: str = "measured") -> WorkerResult:
    artifact = Artifact(
        ref="akki://artifact/1",
        sha256="b" * 64,
        size_bytes=10,
        tenant_id="DIGICOW",
        class_label="non_factual",
    )
    return WorkerResult(
        operation_key=operation_key,
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(artifact,),
        usage=(Usage(unit="tokens", quantity="1"),),
        evidence_mode=evidence_mode,
    )


class _Journal:
    def __init__(self):
        self.rows = {}
        self.fail_registry_once = False

    async def append(self, request, slot, data):
        from services.ledger_writer.principal_control import CommandConflict

        rows = self.rows.setdefault(request.request_id, [])
        for row in rows:
            if row["slot"] == slot and row["data"] == data:
                return row
            if row["slot"] == slot and row["data"] != data:
                raise CommandConflict("slot conflict")
        if self.fail_registry_once and slot == "registry":
            self.fail_registry_once = False
            raise RuntimeError("registry commit failure")
        row = {"slot": slot, "data": data, "seq": len(rows) + 1, "hash": f"h-{len(rows)+1}"}
        rows.append(row)
        return row

    async def read(self, request):
        return list(self.rows.get(request.request_id, []))


def _synthetic_typed_context(*, principal_id: str = "principal-1"):
    principal = PrincipalV1(
        principal_id=principal_id,
        kind=PrincipalKind.INDIVIDUAL,
        legal_identity=principal_id,
        trust_domain_identifier="td-1",
        admission_time_mandate="mandate",
        behavioural_signature_state="watch:baseline@admission",
        parent_organisation_id="org-1",
        autonomy_scope=None,
        admit_authority=False,
        suspended=False,
    )
    licence = Licence(
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
    view = LicencePortalView(
        principal_id=principal_id,
        status="resolved",
        reason_code="",
        licence=licence,
        allowance_state=LicenceAllowanceState(
            licence_terms_id=licence.terms_identifier,
            period_iso="2026-09",
            credits_debited=0,
            credits_allowance=1000,
            credits_remaining=1000,
        ),
        rows=[],
        badges=[],
        count=0,
    )
    return principal, view


class _Authority:
    async def context(self, request):
        return _synthetic_typed_context(principal_id=request.principal_id)

    async def authorize(self, request, _phase):
        from services.northena.execution_models import Authority

        return Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=9_999_999_999,
            terms_ref="terms://dispatch/v1",
            policy_epoch=1,
        )


class _Inspector:
    def __init__(self, mode="measured"):
        self.mode = mode

    async def inspect(self, request, result, operation_key):
        models = _models_module()
        from contracts.asset_registry import AssetClass, AssetRegistryRecord, CustodyClass, NamedOwner
        from contracts.mtafiti_registry import FreshnessStamp

        assert result.request_sha256 == request.digest()
        assert operation_key == result.operation_key

        record = AssetRegistryRecord(
            asset_ref=result.artifacts[0].ref,
            asset_class=AssetClass.ARTIFACT,
            named_owner=NamedOwner(owner_id="org-1", owner_class="organisation", mandate_source="test"),
            custody_class=CustodyClass.OPEN,
            freshness_stamp=FreshnessStamp(logged_date="2026-01-01T00:00:00+00:00", structural_signature=None),
        )
        entry = models.InspectionEntry(artifact=result.artifacts[0], record=record)
        return models.InspectorReceipt(
            request_sha256=request.digest(),
            operation_key=operation_key,
            worker_receipt_ref=result.receipt_ref,
            inspection_ref="inspect://1",
            evidence_mode=self.mode,
            entries=(entry,),
        )


# Module/feature: Fake journal replay is idempotent; changed payload for same slot conflicts.
def test_fake_journal_replay_is_idempotent_and_conflicting_slot_is_refused():
    from services.ledger_writer.principal_control import CommandConflict

    journal = _Journal()
    request = _request()
    first = asyncio.run(journal.append(request, "registry", {"request_sha256": request.digest(), "operation_key": "op-1"}))
    replay = asyncio.run(journal.append(request, "registry", {"request_sha256": request.digest(), "operation_key": "op-1"}))
    assert replay["seq"] == first["seq"] == 1

    with pytest.raises(CommandConflict):
        asyncio.run(journal.append(request, "registry", {"request_sha256": request.digest(), "operation_key": "op-2"}))


# Module/feature: record model contracts expose measured/MOCKED evidence and typed entries.
def test_execution_record_models_contract_shapes_are_present_and_strict():
    mod = _models_module()
    assert hasattr(mod, "InspectionEntry")
    assert hasattr(mod, "InspectorReceipt")


# Module/feature: CanonicalRegistry refuses MOCKED evidence as production registration input.
def test_canonical_registry_rejects_mocked_inspection_for_real_registration():
    mod = _registry_module()
    journal = _Journal()
    registry = mod.CanonicalRegistry(journal=journal, authority=_Authority(), inspector=_Inspector(mode="MOCKED"))
    with pytest.raises(Exception):
        request = _request()
        asyncio.run(registry.verify(request, _result(request, operation_key="op-1", evidence_mode="MOCKED"), "op-1"))


# Module/feature: registry envelope commit occurs before canonical writer side-effect.
def test_registry_commit_failure_blocks_asset_writer_side_effect(monkeypatch):
    mod = _registry_module()
    journal = _Journal()
    journal.fail_registry_once = True
    calls = {"writer": 0}

    def _writer(_record):
        calls["writer"] += 1
        return object()

    monkeypatch.setattr(mod, "write_asset_record", _writer)
    registry = mod.CanonicalRegistry(journal=journal, authority=_Authority(), inspector=_Inspector(mode="measured"))
    request = _request()

    with pytest.raises(Exception, match="registry commit failure"):
        asyncio.run(registry.verify(request, _result(request, operation_key="op-1", evidence_mode="measured"), "op-1"))

    rows = asyncio.run(journal.read(request))
    assert not any(row["slot"] == "registry" for row in rows)
    assert calls["writer"] == 0
