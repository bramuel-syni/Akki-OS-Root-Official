"""Native integration tests for execution composition with isolated FAKE ledger DB.

Synthetic upstream signals only; real native reader/writer/resolver paths are exercised.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from contracts.asset_registry import AssetClass, AssetRegistryRecord, CustodyClass, NamedOwner
from contracts.mtafiti_registry import FreshnessStamp
from contracts.principal_v1 import PrincipalKind, PrincipalV1
from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events
from services.mtafiti import execution_registry as execution_registry_module
from services.mtafiti.asset_registry_writer import _REGISTRY as CANONICAL_REGISTRY_MEMORY, _compute_receipt_id
from services.mtafiti.execution_record_models import InspectionEntry, InspectorReceipt
from services.northena.execution_authority import ComponentAuthority
from services.northena.execution_bindings import ExecutionBindings, build_coordinator
from services.northena.execution_component_models import Decision
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Authority, Held, Request, Usage, WorkerResult
from services.northena.execution_ports import EngineAdapter
from services.northena.execution_usage import LedgerUsagePublisher
from services.portal_operational.entitlements import read_view
from services.principal_store.store import Principal

try:
    from execution_spine.test_execution_fault_recovery_and_contract_supplemental import (
        _FakeCollection,
        _FakeDb as _DB,
    )
except ModuleNotFoundError:
    _HELPER_PATH = Path(__file__).resolve().parents[1] / "execution_spine" / "test_execution_fault_recovery_and_contract_supplemental.py"
    _SPEC = importlib.util.spec_from_file_location("_spine_fake_db", _HELPER_PATH)
    if _SPEC is None or _SPEC.loader is None:
        raise RuntimeError(f"Failed to load fake DB helper from {_HELPER_PATH}")
    _MOD = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(_MOD)
    _FakeCollection = _MOD._FakeCollection
    _DB = _MOD._FakeDb


def _run_in_scope(principal_id: str, tenant_id: str, coro):
    async def _runner():
        with principal_context(principal_id):
            with bind_control_scope({"principal_id": principal_id, "tenant_id": tenant_id}):
                return await coro

    return asyncio.run(_runner())


def _request(request_id: str, *, kind: str = "source", engine: str = "mtafiti") -> Request:
    return Request(
        request_id=request_id,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind=kind,
        engine=engine,
        objective_sha256=hashlib.sha256(request_id.encode("utf-8")).hexdigest(),
        input_refs=("akki://source/rms_mysql",),
        scope_refs=("rms_mysql",),
        deadline_epoch=4_102_444_800,  # 2100-01-01
    )


def _principal_lookup():
    principal = Principal(
        PrincipalV1(
            principal_id="principal-1",
            kind=PrincipalKind.INDIVIDUAL,
            legal_identity="principal-1",
            trust_domain_identifier="td-1",
            admission_time_mandate="synthetic-admission",
            behavioural_signature_state="watch:baseline@admission",
            parent_organisation_id="org-1",
            autonomy_scope=None,
            admit_authority=False,
            suspended=False,
        )
    )
    org = Principal(
        PrincipalV1(
            principal_id="org-1",
            kind=PrincipalKind.ORGANISATION,
            legal_identity="org-1",
            trust_domain_identifier="td-1",
            admission_time_mandate="synthetic-org-admission",
            behavioural_signature_state="watch:baseline@admission",
            parent_organisation_id=None,
            autonomy_scope=None,
            admit_authority=True,
            suspended=False,
        )
    )
    return lambda pid: principal if pid == "principal-1" else org


def _seed_entitlements(
    db,
    *,
    tenant_id: str,
    principal_id: str,
    org_id: str,
    model_identifier: str,
    access_class: str,
    credit_rate: float | None,
    period_iso: str,
):
    now = datetime.now(timezone.utc)
    period_start = (now - timedelta(days=1)).isoformat()
    period_end = (now + timedelta(days=1)).isoformat()

    membership_payload = {
        "principal_id": principal_id,
        "status": "active",
        "organisation_principal_id": org_id,
        "admission_receipt_ref": "synthetic://owner-admission/membership",
        "ceremony_receipt_ref": "synthetic://ceremony/membership",
    }
    licence_payload = {
        "licence": {
            "plan_identifier": "plan-v1",
            "organisation_principal_id": org_id,
            "seat_count": 10,
            "compute_dial": "managed",
            "frontier_dial": "managed",
            "credits_per_seat_per_period": 100,
            "pooled_credits_flag": True,
            "seat_soft_limit": 8,
            "organisation_ceiling": 10_000,
            "period": "month",
            "renewal_date": (now + timedelta(days=30)).isoformat(),
            "status": "active",
            "terms_identifier": "terms://dispatch/v1",
            "agent_count": None,
        },
        "period_start": period_start,
        "period_end": period_end,
        "period_iso": period_iso,
        "admission_receipt_ref": "synthetic://owner-admission/licence",
        "ceremony_receipt_ref": "synthetic://ceremony/licence",
    }
    catalog_payload = {
        "organisation_principal_id": org_id,
        "catalog_row": {
            "model_identifier": model_identifier,
            "access_class": access_class,
            "status": "listed",
            "residency": "za",
            "credit_rate": credit_rate,
        },
        "ceremony_receipt_ref": "synthetic://ceremony/catalog",
    }

    for idx, (resource_type, payload) in enumerate(
        (
            ("principal_membership", membership_payload),
            ("entitlement_licence", licence_payload),
            ("entitlement_catalog", catalog_payload),
        ),
        start=1,
    ):
        command_id = digest(
            {
                "seed": resource_type,
                "idx": idx,
                "principal": principal_id,
                "period": period_iso,
                "payload": payload,
            }
        )
        _run_in_scope(
            principal_id,
            tenant_id,
            append_event(
                db,
                tenant_id=tenant_id,
                run_id=f"seed-{resource_type}",
                command_id=command_id,
                event_type=f"entitlement.{resource_type}.recorded",
                resource_type=resource_type,
                decision="recorded",
                reason_code="SYNTHETIC_TEST_SEED",
                payload=payload,
            ),
        )


class _SyntheticDecisions:
    def __init__(self, *, model_identifier: str | None, access_class: str | None):
        self.model_identifier = model_identifier
        self.access_class = access_class

    async def resolve(self, request, _phase, principal, _view):
        grant = Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=principal.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=4_102_444_800,
            terms_ref="terms://dispatch/v1",
            policy_epoch=1,
        )
        return Decision(
            authority=grant,
            catalog_model_identifier=self.model_identifier,
            catalog_access_class=self.access_class,
        )


class _SyntheticInspector:
    def __init__(self):
        self.calls = 0
        self.mode = "normal"
        self.logged_date = "2026-02-01T00:00:00+00:00"

    async def inspect(self, request, result, operation_key):
        self.calls += 1
        artifact = result.artifacts[0]
        owner_id = "org-1"
        custody = CustodyClass.OPEN
        artifact_ref = artifact.ref

        if self.mode == "owner_changed":
            owner_id = "org-2"
        elif self.mode == "custody_forbidden":
            custody = CustodyClass.FORBIDDEN
        elif self.mode == "artifact_changed":
            artifact_ref = "akki://artifact/changed"

        record = AssetRegistryRecord(
            asset_ref=artifact_ref,
            asset_class=AssetClass.ARTIFACT,
            named_owner=NamedOwner(owner_id=owner_id, owner_class="organisation", mandate_source="SYNTHETIC"),
            custody_class=custody,
            freshness_stamp=FreshnessStamp(logged_date=self.logged_date, structural_signature=None),
        )
        entry = InspectionEntry(artifact=artifact, record=record)
        return InspectorReceipt(
            request_sha256=request.digest(),
            operation_key=operation_key,
            worker_receipt_ref=result.receipt_ref,
            inspection_ref=f"inspect://{self.calls}",
            evidence_mode="measured",
            entries=(entry,),
        )


class _SyntheticSourceRpc:
    async def submit(self, request, operation_key, fence, _authority):
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-source-mtafiti",
            fence=fence,
            state="accepted",
            receipt_ref="akki://receipt/submit/native",
            artifacts=(),
            usage=None,
            evidence_mode="measured",
        )

    async def status(self, request, operation_key, fence):
        artifact = Artifact(
            ref="akki://artifact/native-1",
            sha256="b" * 64,
            size_bytes=32,
            tenant_id=request.tenant_id,
            class_label="non_factual",
        )
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-source-mtafiti",
            fence=fence,
            state="complete",
            receipt_ref="akki://receipt/status/native",
            artifacts=(artifact,),
            usage=(Usage(unit="tokens", quantity="111"),),
            evidence_mode="measured",
        )

    async def cancel(self, request, operation_key, fence):
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-source-mtafiti",
            fence=fence,
            state="cancelled",
            receipt_ref="akki://receipt/cancel/native",
            artifacts=(),
            usage=(Usage(unit="tokens", quantity="0"),),
            evidence_mode="measured",
        )


class _FailOnceSlotJournal:
    def __init__(self, inner: LedgerJournal, slot: str):
        self.inner = inner
        self.slot = slot
        self.hit = False

    async def read(self, request):
        return await self.inner.read(request)

    async def append(self, request, slot, data):
        if slot == self.slot and not self.hit:
            self.hit = True
            raise RuntimeError(f"injected boundary: {slot}")
        return await self.inner.append(request, slot, data)


# Module/feature: FULL native source pipeline (Coordinator+Journal+Authority+Registry+UsagePublisher+EngineAdapter).
def test_native_full_source_pipeline_non_model_handoff_and_registry_sequence(monkeypatch):
    CANONICAL_REGISTRY_MEMORY.clear()
    db = _DB({"ledger_v1_control_events": _FakeCollection()})
    request = _request("req-native-a")
    _seed_entitlements(
        db,
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        org_id="org-1",
        model_identifier="model://northena/customer-model",
        access_class="customer_model",
        credit_rate=None,
        period_iso="2026-02",
    )

    inspector = _SyntheticInspector()
    rpc = _SyntheticSourceRpc()
    adapter = EngineAdapter("source", "mtafiti", rpc.submit, rpc.status, rpc.cancel, timeout_seconds=1.0)
    bindings = ExecutionBindings(
        decisions=_SyntheticDecisions(model_identifier=None, access_class=None),
        inspector=inspector,
        executors={("source", "mtafiti"): adapter},
    )
    coordinator = build_coordinator(db, bindings)
    coordinator.authority.principal_lookup = _principal_lookup()
    default_unbound = build_coordinator(db, None)
    assert default_unbound.executors == {}

    writer_observations = []
    real_writer = execution_registry_module.write_asset_record

    def _spy_writer(record):
        docs = db["ledger_v1_control_events"].docs
        registry_count = len([d for d in docs if d["row"]["resource_type"] == "execution_flow" and d["payload"]["slot"] == "registry"])
        writer_observations.append(registry_count)
        return real_writer(record)

    monkeypatch.setattr(execution_registry_module, "write_asset_record", _spy_writer)

    view = _run_in_scope(request.principal_id, request.tenant_id, coordinator.advance(request))
    assert view.phase == "ready"
    assert view.execution_verified is True
    assert view.evidence_mode == "measured"

    rows = _run_in_scope(request.principal_id, request.tenant_id, coordinator.journal.read(request))
    slots = [row["slot"] for row in rows]
    assert slots.count("registry") == 1
    assert writer_observations and all(value == 1 for value in writer_observations)
    assert "metered" in slots and "usage_handoff" in slots and "terminal" in slots
    assert slots.index("metered") < slots.index("usage_handoff") < slots.index("terminal")

    registry_row = next(row for row in rows if row["slot"] == "registry")
    assert len(registry_row["data"]["records"]) == 1
    rec = registry_row["data"]["records"][0]
    assert rec["receipt_id"] == _compute_receipt_id(AssetRegistryRecord.model_validate(rec["record"]))
    assert rec["record"]["asset_ref"] in CANONICAL_REGISTRY_MEMORY

    metered_events = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        read_events(db, {"row.tenant_id": request.tenant_id, "row.resource_type": {"$in": ["metered_event"]}}),
    )
    assert metered_events == []

    before = inspector.calls
    retrieved = _run_in_scope(request.principal_id, request.tenant_id, coordinator.retrieve(request))
    assert retrieved.phase == "ready"
    assert inspector.calls > before


# Module/feature: REGISTRY recovery boundaries + immutable slot replay + revalidation refusal on changed owner/custody/artifact.
def test_native_registry_recovery_and_revalidation_refusal_paths(monkeypatch):
    CANONICAL_REGISTRY_MEMORY.clear()
    db = _DB({"ledger_v1_control_events": _FakeCollection()})
    request = _request("req-native-b")
    _seed_entitlements(
        db,
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        org_id="org-1",
        model_identifier="model://northena/customer-model",
        access_class="customer_model",
        credit_rate=None,
        period_iso="2026-02",
    )

    authority = ComponentAuthority(db=db, decisions=_SyntheticDecisions(model_identifier=None, access_class=None), principal_lookup=_principal_lookup())
    inspector = _SyntheticInspector()
    journal = LedgerJournal(db)

    result = WorkerResult(
        operation_key="op-native-b",
        request_sha256=request.digest(),
        executor_id="exec-source-mtafiti",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/status/native-b",
        artifacts=(Artifact(ref="akki://artifact/native-b", sha256="c" * 64, size_bytes=12, tenant_id=request.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="tokens", quantity="5"),),
        evidence_mode="measured",
    )

    _run_in_scope(
        request.principal_id,
        request.tenant_id,
        journal.append(
            request,
            "dispatch",
            {
                "operation_key": "op-native-b",
                "request_sha256": request.digest(),
                "action": "submit",
                "authority": Authority(
                    authority_ref="auth://req-native-b",
                    request_sha256=request.digest(),
                    tenant_id=request.tenant_id,
                    principal_id=request.principal_id,
                    scope_refs=request.scope_refs,
                    engine=request.engine,
                    expires_epoch=4_102_444_800,
                    terms_ref="terms://dispatch/v1",
                    policy_epoch=1,
                ).model_dump(mode="json"),
                "commercial_snapshot": {
                    "licence": {
                        "plan_identifier": "plan-v1",
                        "organisation_principal_id": "org-1",
                        "seat_count": 10,
                        "compute_dial": "managed",
                        "frontier_dial": "managed",
                        "credits_per_seat_per_period": 100,
                        "pooled_credits_flag": True,
                        "seat_soft_limit": 8,
                        "organisation_ceiling": 10_000,
                        "period": "month",
                        "renewal_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
                        "status": "active",
                        "terms_identifier": "terms://dispatch/v1",
                        "agent_count": None,
                    },
                    "catalog_row": None,
                    "period_iso": "2026-02",
                    "principal_id": request.principal_id,
                },
            },
        ),
    )
    _run_in_scope(
        request.principal_id,
        request.tenant_id,
        journal.append(request, "observation:" + digest(result.model_dump(mode="json")), {"result": result.model_dump(mode="json")}),
    )

    failing_registry = execution_registry_module.CanonicalRegistry(_FailOnceSlotJournal(journal, "registry"), authority, inspector)
    with pytest.raises(RuntimeError, match="injected boundary: registry"):
        _run_in_scope(request.principal_id, request.tenant_id, failing_registry.verify(request, result, "op-native-b"))

    rows_after_fail = _run_in_scope(request.principal_id, request.tenant_id, journal.read(request))
    assert not any(row["slot"] == "registry" for row in rows_after_fail)

    boundary = {"projection_failure_reached": False}
    real_writer = execution_registry_module.write_asset_record

    def _fail_after_commit(record):
        boundary["projection_failure_reached"] = True
        raise RuntimeError("injected projection failure")

    monkeypatch.setattr(execution_registry_module, "write_asset_record", _fail_after_commit)
    registry = execution_registry_module.CanonicalRegistry(journal, authority, inspector)
    with pytest.raises(RuntimeError, match="injected projection failure"):
        _run_in_scope(request.principal_id, request.tenant_id, registry.verify(request, result, "op-native-b"))
    assert boundary["projection_failure_reached"] is True

    rows_after_projection_fail = _run_in_scope(request.principal_id, request.tenant_id, journal.read(request))
    registry_rows = [row for row in rows_after_projection_fail if row["slot"] == "registry"]
    assert len(registry_rows) == 1
    saved_records = list(registry_rows[0]["data"]["records"])

    monkeypatch.setattr(execution_registry_module, "write_asset_record", real_writer)
    recovered_registry = execution_registry_module.CanonicalRegistry(journal, authority, inspector)
    _run_in_scope(request.principal_id, request.tenant_id, recovered_registry.verify(request, result, "op-native-b"))
    rows_after_recovery = _run_in_scope(request.principal_id, request.tenant_id, journal.read(request))
    recovered_rows = [row for row in rows_after_recovery if row["slot"] == "registry"]
    assert len(recovered_rows) == 1
    assert recovered_rows[0]["data"]["records"] == saved_records

    for mode in ("owner_changed", "custody_forbidden", "artifact_changed"):
        inspector.mode = mode
        with pytest.raises(Held):
            _run_in_scope(request.principal_id, request.tenant_id, recovered_registry.revalidate(request, ("akki://artifact/native-b",)))


# Module/feature: Historical model usage publisher -> real entitlement projection with event-time pricing and idempotent recovery.
def test_native_usage_publisher_event_time_projection_and_recoverable_handoff_failure():
    CANONICAL_REGISTRY_MEMORY.clear()
    db = _DB({"ledger_v1_control_events": _FakeCollection()})
    request = _request("req-native-c", kind="source", engine="mtafiti")

    _seed_entitlements(
        db,
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        org_id="org-1",
        model_identifier="model://northena/frontier-r1",
        access_class="reseller_frontier",
        credit_rate=0.002,
        period_iso="2026-02",
    )

    journal = LedgerJournal(db)
    publisher = LedgerUsagePublisher(db, journal)
    authority = Authority(
        authority_ref="auth://req-native-c",
        request_sha256=request.digest(),
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        scope_refs=request.scope_refs,
        engine=request.engine,
        expires_epoch=4_102_444_800,
        terms_ref="terms://dispatch/v1",
        policy_epoch=1,
    )
    dispatch = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        journal.append(
            request,
            "dispatch",
            {
                "operation_key": "op-native-c",
                "request_sha256": request.digest(),
                "action": "submit",
                "authority": authority.model_dump(mode="json"),
                "commercial_snapshot": {
                    "licence": {
                        "plan_identifier": "plan-v1",
                        "organisation_principal_id": "org-1",
                        "seat_count": 10,
                        "compute_dial": "managed",
                        "frontier_dial": "managed",
                        "credits_per_seat_per_period": 100,
                        "pooled_credits_flag": True,
                        "seat_soft_limit": 8,
                        "organisation_ceiling": 10_000,
                        "period": "month",
                        "renewal_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
                        "status": "active",
                        "terms_identifier": "terms://dispatch/v1",
                        "agent_count": None,
                    },
                    "catalog_row": {
                        "model_identifier": "model://northena/frontier-r1",
                        "access_class": "reseller_frontier",
                        "status": "listed",
                        "residency": "za",
                            "credit_rate": 0.002,
                    },
                    "period_iso": "2026-02",
                    "principal_id": request.principal_id,
                },
            },
        ),
    )
    result = WorkerResult(
        operation_key="op-native-c",
        request_sha256=request.digest(),
        executor_id="exec-source-mtafiti",
        fence=dispatch["seq"],
        state="complete",
        receipt_ref="akki://receipt/status/native-c",
        artifacts=(Artifact(ref="akki://artifact/native-c", sha256="d" * 64, size_bytes=18, tenant_id=request.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="tokens", quantity="1000"),),
        evidence_mode="measured",
    )
    raw_meter = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        journal.append(
            request,
            "metered",
            {
                "terms_ref": "terms://dispatch/v1",
                "worker_receipt_ref": result.receipt_ref,
                "usage": [item.model_dump(mode="json") for item in result.usage],
                "evidence_mode": "measured",
            },
        ),
    )

    _run_in_scope(request.principal_id, request.tenant_id, publisher.publish(request, result, dispatch, raw_meter))
    _run_in_scope(request.principal_id, request.tenant_id, publisher.publish(request, result, dispatch, raw_meter))

    metered_events = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        read_events(db, {"row.tenant_id": request.tenant_id, "row.resource_type": {"$in": ["metered_event"]}}),
    )
    assert len(metered_events) == 1

    _seed_entitlements(
        db,
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        org_id="org-1",
        model_identifier="model://northena/frontier-r1",
        access_class="reseller_frontier",
        credit_rate=0.02,
        period_iso="2026-02",
    )
    view = _run_in_scope(request.principal_id, request.tenant_id, read_view(db, {"tenant_id": request.tenant_id, "principal_id": request.principal_id}))
    assert view.status == "resolved"
    assert view.allowance_state is not None
    assert view.allowance_state.credits_debited == 2

    mocked_result = result.model_copy(update={"evidence_mode": "MOCKED"})
    with pytest.raises(Held, match="MOCKED_USAGE_NOT_CHARGEABLE"):
        _run_in_scope(request.principal_id, request.tenant_id, publisher.publish(request, mocked_result, dispatch, raw_meter))
    metered_events_after_mocked = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        read_events(db, {"row.tenant_id": request.tenant_id, "row.resource_type": {"$in": ["metered_event"]}}),
    )
    assert len(metered_events_after_mocked) == 1

    class _FailUsageHandoffOnce:
        def __init__(self, inner):
            self.inner = inner
            self.hit = False

        async def read(self, req):
            return await self.inner.read(req)

        async def append(self, req, slot, data):
            if slot == "usage_handoff" and not self.hit:
                self.hit = True
                raise RuntimeError("injected consumer usage_handoff failure")
            return await self.inner.append(req, slot, data)

    recovering_publisher = LedgerUsagePublisher(db, _FailUsageHandoffOnce(journal))
    with pytest.raises(RuntimeError, match="injected consumer usage_handoff failure"):
        _run_in_scope(request.principal_id, request.tenant_id, recovering_publisher.publish(request, result, dispatch, raw_meter))
    _run_in_scope(request.principal_id, request.tenant_id, recovering_publisher.publish(request, result, dispatch, raw_meter))
    metered_events_after_recovery = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        read_events(db, {"row.tenant_id": request.tenant_id, "row.resource_type": {"$in": ["metered_event"]}}),
    )
    assert len(metered_events_after_recovery) == 1

    reseller_authority = ComponentAuthority(
        db=db,
        decisions=_SyntheticDecisions(model_identifier="model://northena/frontier-r1", access_class="reseller_frontier"),
        principal_lookup=_principal_lookup(),
    )
    with pytest.raises(Held, match="RESELLER_AUTHORITY_UNRESOLVED"):
        _run_in_scope(request.principal_id, request.tenant_id, reseller_authority.prepare(request))