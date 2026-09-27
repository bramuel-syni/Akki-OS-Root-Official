"""Portal execution lifecycle join tests over native coordinator + canonical fake ledger DB."""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import json
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi import HTTPException

from contracts.asset_registry import AssetClass, AssetRegistryRecord, CustodyClass, NamedOwner
from contracts.mtafiti_registry import FreshnessStamp
from contracts.principal_v1 import PrincipalKind, PrincipalV1
from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event
from services.northena import portal_work
from services.northena.execution_bindings import ExecutionBindings
from services.northena.execution_component_models import Decision
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Authority, Held, Request, Usage, WorkerResult
from services.northena.execution_ports import EngineAdapter
from services.portal_operational import actions, execution
from services.portal_operational.models import SubmitRequest
from services.principal_store.store import Principal
import services.northena.execution_authority as execution_authority

try:
    from execution_spine.test_execution_fault_recovery_and_contract_supplemental import (
        _FakeCollection,
        _FakeDb,
    )
except ModuleNotFoundError:
    _HELPER_PATH = (
        Path(__file__).resolve().parents[1]
        / "execution_spine"
        / "test_execution_fault_recovery_and_contract_supplemental.py"
    )
    _SPEC = importlib.util.spec_from_file_location("_spine_fake_db", _HELPER_PATH)
    if _SPEC is None or _SPEC.loader is None:
        raise RuntimeError(f"Failed to load fake DB helper from {_HELPER_PATH}")
    _MOD = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(_MOD)
    _FakeCollection = _MOD._FakeCollection
    _FakeDb = _MOD._FakeDb


def _run(scope: dict, coro):
    async def _runner():
        with principal_context(scope["principal_id"]):
            with bind_control_scope(scope):
                return await coro

    return asyncio.run(_runner())


def _scope(principal_id: str = "principal-1", tenant_id: str = "DIGICOW") -> dict:
    return {"principal_id": principal_id, "tenant_id": tenant_id, "roles": ["operator"]}


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
    def lookup(pid):
        if pid == "principal-1":
            return principal
        if pid == "org-1":
            return org
        raise KeyError(pid)
    return lookup


@pytest.fixture(autouse=True)
def _patch_component_authority_principal_lookup(monkeypatch):
    original_init = execution_authority.ComponentAuthority.__init__

    def _patched_init(self, db, decisions=None, principal_lookup=execution_authority.get_principal, clock=time.time):
        return original_init(self, db, decisions=decisions, principal_lookup=_principal_lookup(), clock=clock)

    monkeypatch.setattr(execution_authority.ComponentAuthority, "__init__", _patched_init)


def _seed_entitlements(db, *, tenant_id: str, principal_id: str, org_id: str, period_iso: str = "2026-02"):
    now = datetime.now(timezone.utc)
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
        "period_start": (now - timedelta(days=1)).isoformat(),
        "period_end": (now + timedelta(days=1)).isoformat(),
        "period_iso": period_iso,
        "admission_receipt_ref": "synthetic://owner-admission/licence",
        "ceremony_receipt_ref": "synthetic://ceremony/licence",
    }
    catalog_payload = {
        "organisation_principal_id": org_id,
        "catalog_row": {
            "model_identifier": "model://northena/customer-model",
            "access_class": "customer_model",
            "status": "listed",
            "residency": "za",
            "credit_rate": None,
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
        _run(
            _scope(principal_id=principal_id, tenant_id=tenant_id),
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


class _Decisions:
    def __init__(self, *, revoke_phases: set[str] | None = None):
        self.revoke_phases = set(revoke_phases or set())

    async def resolve(self, request, phase, principal, _view):
        if phase in self.revoke_phases:
            raise Held("RIGHTS_WITHDRAWN")
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
        return Decision(authority=grant, catalog_model_identifier=None, catalog_access_class=None)


class _Inspector:
    async def inspect(self, request, result, operation_key):
        from services.mtafiti.execution_record_models import InspectionEntry, InspectorReceipt

        artifact = result.artifacts[0]
        record = AssetRegistryRecord(
            asset_ref=artifact.ref,
            asset_class=AssetClass.ARTIFACT,
            named_owner=NamedOwner(owner_id="org-1", owner_class="organisation", mandate_source="SYNTHETIC"),
            custody_class=CustodyClass.OPEN,
            freshness_stamp=FreshnessStamp(logged_date="2026-02-01T00:00:00+00:00", structural_signature=None),
        )
        entry = InspectionEntry(artifact=artifact, record=record)
        return InspectorReceipt(
            request_sha256=request.digest(),
            operation_key=operation_key,
            worker_receipt_ref=result.receipt_ref,
            inspection_ref=f"inspect://{request.request_id}",
            evidence_mode="measured",
            entries=(entry,),
        )


class _SourceRpc:
    def __init__(self, *, status_states: list[str] | None = None, cancel_state: str = "cancelled", cancel_timeout=False):
        self.status_states = status_states or ["complete"]
        self.cancel_state = cancel_state
        self.cancel_timeout = cancel_timeout
        self.submit_calls = 0
        self.status_calls = 0
        self.cancel_calls = 0

    async def submit(self, request, operation_key, fence, _authority):
        self.submit_calls += 1
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
        self.status_calls += 1
        state = self.status_states[0] if len(self.status_states) == 1 else self.status_states.pop(0)
        artifact = Artifact(
            ref=f"akki://artifact/{request.request_id}",
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
            state=state,
            receipt_ref="akki://receipt/status/native",
            artifacts=(artifact,),
            usage=(Usage(unit="tokens", quantity="9"),) if state in {"complete", "cancelled", "failed"} else None,
            evidence_mode="measured",
        )

    async def cancel(self, request, operation_key, fence):
        self.cancel_calls += 1
        if self.cancel_timeout:
            raise TimeoutError("synthetic timeout")
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-source-mtafiti",
            fence=fence,
            state=self.cancel_state,
            receipt_ref="akki://receipt/cancel/native",
            artifacts=(),
            usage=(Usage(unit="tokens", quantity="1"),),
            evidence_mode="measured",
        )


def _bindings(rpc: _SourceRpc, decisions: _Decisions | None = None) -> ExecutionBindings:
    adapter = EngineAdapter("source", "mtafiti", rpc.submit, rpc.status, rpc.cancel, timeout_seconds=1.0)
    return ExecutionBindings(decisions=decisions or _Decisions(), inspector=_Inspector(), executors={("source", "mtafiti"): adapter})


def _new_db():
    return _FakeDb({"ledger_v1_control_events": _FakeCollection()})


def _submit_request(db, scope, *, operation="browse_estate", objective="lifecycle join objective", units=None):
    payload = SubmitRequest(
        objective_text=objective,
        operation=operation,
        units=units or ["digicow_rds"],
        idempotency_key=f"idem-{uuid.uuid4().hex}",
    )
    return _run(scope, portal_work.submit(db, scope, payload)).request_id


def _advance(db, scope, request_id, *, deadline_epoch, bindings):
    budget = execution.ExecutionBudget(deadline_epoch=deadline_epoch)
    return _run(scope, execution.advance(db, scope, request_id, budget, bindings=bindings))


# Module/feature: successful source execution join updates portal views and keeps output allowlisted.
def test_source_execution_ready_join_updates_detail_listing_history_and_result_allowlist():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["complete"])
    bindings = _bindings(rpc)
    request_id = _submit_request(db, scope)

    run_view = _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    assert run_view.phase == "ready"
    detail = _run(scope, portal_work.detail(db, scope, request_id))
    assert detail.lifecycle_state == "Ready"
    assert detail.state == "ready"
    assert detail.permitted_actions == ["result"]
    assert detail.result is None
    assert any(entry.event == "execution_reserved" for entry in detail.history)
    assert any(entry.event == "execution_ready" for entry in detail.history)

    listing = _run(scope, portal_work.listing(db, scope))
    listed = next(row for row in listing if row.request_id == request_id)
    assert listed.lifecycle_state == "Ready"
    history_json = json.dumps([entry.model_dump(mode="json") for entry in listed.history])
    assert "commercial_snapshot" not in history_json
    assert "worker_receipt_ref" not in history_json
    assert "executor_id" not in history_json

    released = _run(scope, actions.result(db, scope, request_id, bindings=bindings))
    assert set(released.keys()) == {"request_id", "artifact_refs", "execution_verified", "delivery_verified"}
    assert released["request_id"] == request_id
    assert released["execution_verified"] is True
    assert released["delivery_verified"] is False
    assert all(ref.startswith("akki://artifact/") for ref in released["artifact_refs"])


# Module/feature: rights revoked after ready fail-closes result release while metered usage remains recorded.
def test_rights_revoked_after_ready_result_returns_409_without_artifact_release_and_metered_persists():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["complete"])
    decisions = _Decisions()
    bindings = _bindings(rpc, decisions=decisions)
    request_id = _submit_request(db, scope)

    deadline = int(time.time()) + 3600
    ready = _advance(db, scope, request_id, deadline_epoch=deadline, bindings=bindings)
    assert ready.phase == "ready"
    decisions.revoke_phases.add("retrieve")
    with pytest.raises(HTTPException) as exc:
        _run(scope, actions.result(db, scope, request_id, bindings=bindings))
    assert exc.value.status_code == 409

    descriptor = _run(
        scope,
        execution.frozen_request(
            db,
            scope,
            request_id,
            execution.ExecutionBudget(deadline_epoch=deadline),
        ),
    )
    rows = _run(scope, LedgerJournal(db).read(descriptor))
    assert any(row["slot"] == "metered" for row in rows)


# Module/feature: mocked/unverified terminal projection never exposes releasable public result.
def test_mocked_ready_projection_becomes_blocked_and_result_is_refused():
    db = _new_db()
    scope = _scope()
    request_id = _submit_request(db, scope)
    work = _run(scope, portal_work.detail(db, scope, request_id))
    fake_event = {
        "row": {"at": {"epoch_s": int(time.time())}, "hash": "h" * 64},
        "payload": {
            "slot": "terminal",
            "data": {
                "phase": "ready",
                "reason_code": "VERIFIED_RESULT_RECORDED",
                "evidence_mode": "MOCKED",
                "artifact_refs": ["akki://artifact/synthetic"],
                "usage": [{"unit": "tokens", "quantity": "1"}],
                "terms_ref": "terms://dispatch/v1",
            },
        },
    }
    projected = execution.execution_records.project(work, [fake_event])
    assert projected.lifecycle_state == "Blocked"
    assert projected.reason_code == "MOCKED_RESULT_NOT_RELEASABLE"
    assert projected.permitted_actions == []


# Module/feature: foreign principal/tenant concealment for stop/retry/result actions.
def test_foreign_scope_actions_are_concealed_with_404_on_stop_retry_and_result():
    db = _new_db()
    owner_scope = _scope(principal_id="principal-1", tenant_id="DIGICOW")
    foreign_scope = _scope(principal_id="principal-2", tenant_id="FOREIGN")
    request_id = _submit_request(db, owner_scope)

    for call in (
        actions.stop(db, foreign_scope, request_id, bindings=None),
        actions.retry(db, foreign_scope, request_id, bindings=None),
        actions.result(db, foreign_scope, request_id, bindings=None),
    ):
        with pytest.raises(HTTPException) as exc:
            _run(foreign_scope, call)
        assert exc.value.status_code == 404


# Module/feature: stop confirms cancellation only on executor-confirmed cancelled result.
def test_stop_from_executing_transitions_to_stopped_only_on_confirmed_cancel():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["running"], cancel_state="cancelled")
    bindings = _bindings(rpc)
    request_id = _submit_request(db, scope)

    running = _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    assert running.phase == "running"
    stopped = _run(scope, actions.stop(db, scope, request_id, bindings=bindings))
    assert stopped.lifecycle_state == "Stopped"
    assert rpc.cancel_calls == 1


# Module/feature: stop refuses unknown/timeout/held cancellation outcomes and never claims stopped.
@pytest.mark.parametrize(
    "cancel_state,cancel_timeout,bindings_present",
    [("unknown", False, True), ("cancelled", True, True), ("cancelled", False, False)],
)
def test_stop_refuses_non_confirmed_cancel_paths(cancel_state, cancel_timeout, bindings_present):
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["running"], cancel_state=cancel_state, cancel_timeout=cancel_timeout)
    active_bindings = _bindings(rpc)
    request_id = _submit_request(db, scope)

    _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=active_bindings)
    with pytest.raises(HTTPException) as exc:
        _run(scope, actions.stop(db, scope, request_id, bindings=active_bindings if bindings_present else None))
    assert exc.value.status_code == 409
    state = _run(scope, portal_work.detail(db, scope, request_id)).lifecycle_state
    assert state != "Stopped"


# Module/feature: stop refuses routing/no-execution and already-ready completed requests.
def test_stop_refuses_routing_and_ready_states():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")

    routing_id = _submit_request(db, scope)
    with pytest.raises(HTTPException) as routing_exc:
        _run(scope, actions.stop(db, scope, routing_id, bindings=None))
    assert routing_exc.value.status_code == 409

    rpc = _SourceRpc(status_states=["complete"])
    bindings = _bindings(rpc)
    ready_id = _submit_request(db, scope)
    _advance(db, scope, ready_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    with pytest.raises(HTTPException) as ready_exc:
        _run(scope, actions.stop(db, scope, ready_id, bindings=bindings))
    assert ready_exc.value.status_code == 409


# Module/feature: interrupted retry reuses existing dispatch/send and performs bounded status without resubmit.
def test_interrupted_retry_uses_status_without_resubmit_and_can_reach_ready():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["unknown", "complete"])
    bindings = _bindings(rpc)
    request_id = _submit_request(db, scope)

    first = _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    assert first.phase == "unknown"
    interrupted = _run(scope, portal_work.detail(db, scope, request_id))
    assert interrupted.lifecycle_state == "Interrupted"
    assert rpc.submit_calls == 1
    assert rpc.status_calls == 1

    retried = _run(scope, actions.retry(db, scope, request_id, bindings=bindings))
    assert retried.lifecycle_state == "Ready"
    assert rpc.submit_calls == 1
    assert rpc.status_calls == 2


# Module/feature: retry is refused after cancel intent/terminal and on closed stopped requests.
def test_retry_refused_after_cancelled_terminal_and_closed_state():
    db = _new_db()
    scope = _scope()
    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["running"], cancel_state="cancelled")
    bindings = _bindings(rpc)
    request_id = _submit_request(db, scope)

    _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    _run(scope, actions.stop(db, scope, request_id, bindings=bindings))
    with pytest.raises(HTTPException) as exc:
        _run(scope, actions.retry(db, scope, request_id, bindings=bindings))
    assert exc.value.status_code == 409


# Module/feature: unbound pre-send hold remains routing; post-dispatch unknown is interrupted, never fake-complete.
def test_unbound_hold_stays_routing_and_post_dispatch_unknown_is_interrupted():
    db = _new_db()
    scope = _scope()
    request_id = _submit_request(db, scope)
    held = _advance(db, scope, request_id, deadline_epoch=int(time.time()) + 3600, bindings=None)
    assert held.phase == "held"
    held_detail = _run(scope, portal_work.detail(db, scope, request_id))
    assert held_detail.lifecycle_state == "Routing"

    _seed_entitlements(db, tenant_id=scope["tenant_id"], principal_id=scope["principal_id"], org_id="org-1")
    rpc = _SourceRpc(status_states=["unknown"])
    bindings = _bindings(rpc)
    interrupted_id = _submit_request(db, scope)
    unknown = _advance(db, scope, interrupted_id, deadline_epoch=int(time.time()) + 3600, bindings=bindings)
    assert unknown.phase == "unknown"
    detail = _run(scope, portal_work.detail(db, scope, interrupted_id))
    assert detail.lifecycle_state == "Interrupted"
    assert detail.lifecycle_state != "Ready"


# Module/feature: persisted request snapshot prevents replay tampering (deadline/objective/scope) fail-closed.
def test_persisted_snapshot_replay_tamper_is_refused_with_409():
    db = _new_db()
    scope = _scope()
    request_id = _submit_request(db, scope, objective="frozen-objective", units=["digicow_rds"])
    deadline = int(time.time()) + 3600
    tampered = Request(
        request_id=request_id,
        tenant_id=scope["tenant_id"],
        principal_id=scope["principal_id"],
        kind="source",
        engine="mtafiti",
        objective_sha256=hashlib.sha256(b"different-objective").hexdigest(),
        input_refs=("akki://source/digicow_s3",),
        scope_refs=("digicow_s3",),
        deadline_epoch=deadline,
    )
    _run(scope, LedgerJournal(db).append(tampered, "request", {"request_sha256": tampered.digest(), "request": tampered.model_dump(mode="json")}))

    with pytest.raises(HTTPException) as exc:
        _run(scope, execution.advance(db, scope, request_id, execution.ExecutionBudget(deadline_epoch=deadline), bindings=None))
    assert exc.value.status_code == 409

    with pytest.raises(HTTPException) as deadline_exc:
        _run(scope, execution.advance(db, scope, request_id, execution.ExecutionBudget(deadline_epoch=deadline + 1), bindings=None))
    assert deadline_exc.value.status_code == 409



# Module/feature: execution event identity corruption is rejected; model ops without saved descriptor fail closed.
def test_snapshot_hash_corruption_refused_and_model_operation_without_descriptor_returns_409():
    db = _new_db()
    scope = _scope()
    browse_id = _submit_request(db, scope)
    budget = execution.ExecutionBudget(deadline_epoch=int(time.time()) + 3600)
    descriptor = _run(scope, execution.frozen_request(db, scope, browse_id, budget))
    _run(scope, LedgerJournal(db).append(descriptor, "request", {"request_sha256": descriptor.digest(), "request": descriptor.model_dump(mode="json")}))

    bad_payload = {
        "principal_id": scope["principal_id"],
        "request_sha256": "f" * 64,
        "slot": "portal_view:corrupt",
        "data": {"phase": "held", "reason_code": "CORRUPT", "evidence_mode": "unverified", "artifact_refs": [], "usage": None, "terms_ref": None},
    }
    _run(
        scope,
        append_event(
            db,
            tenant_id=scope["tenant_id"],
            run_id=browse_id,
            command_id=digest({"request": browse_id, "corrupt": True}),
            event_type="execution.portal_view",
            resource_type="execution_flow",
            decision="recorded",
            reason_code="EXECUTION_METADATA",
            payload=bad_payload,
        ),
    )
    with pytest.raises(ValueError):
        _run(scope, execution.frozen_request(db, scope, browse_id, budget))

    model_id = _submit_request(db, scope, operation="fine_tune_model")
    with pytest.raises(HTTPException) as model_exc:
        _run(scope, execution.advance(db, scope, model_id, budget, bindings=None))
    assert model_exc.value.status_code == 409
