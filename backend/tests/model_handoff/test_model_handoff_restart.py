"""Crash/restart acceptance tests for model-handoff durable recovery paths.

Focus: NEW restart/fault races omitted in iteration34 supplemental suite.
All providers/storage in this file remain SYNTHETIC/FAKE.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.northena.execution_bindings import ExecutionBindings, build_coordinator
from services.northena.execution_models import Held, Request
from services.northena.execution_ports import EngineAdapter
from services.principal_store.store import PrincipalRefusal, get_principal

from test_model_handoff_red_contract import (
    _FakeCollection,
    _FakeDb,
    _principal_lookup,
    _run_in_scope,
    _seed_entitlements,
    _skill_request,
)
from test_model_handoff_supplemental_iteration34 import (
    EligibilityProvider,
    HandoffProvider,
    RecordingRpc,
    _build_stack,
    _cancel,
    _must_import,
    _rows,
    _training_request,
)


def _source_request() -> Request:
    return Request(
        request_id="req-native-source-restart",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind="source",
        engine="mtafiti",
        objective_sha256="a" * 64,
        input_refs=("akki://source/rms",),
        scope_refs=("rms",),
        deadline_epoch=4_102_444_800,
    )


class DeliveryAwareRpc(RecordingRpc):
    """Status reflects actual delivery receipt, not fabricated completion."""

    def __init__(self, receiver_by_kind: dict[str, str], *, lose_delivery_once: bool = False, mark_delivered_on_loss: bool = False):
        super().__init__(receiver_by_kind)
        self.lose_delivery_once = lose_delivery_once
        self.mark_delivered_on_loss = mark_delivered_on_loss
        self._lost_once = False
        self.delivered_keys: set[str] = set()

    async def delivery(self, packet):
        if self.lose_delivery_once and not self._lost_once:
            self.delivery_calls += 1
            self._lost_once = True
            if self.mark_delivered_on_loss:
                self.delivered_keys.add(packet.operation_key)
            raise TimeoutError("synthetic lost response after committed send")
        self.delivered_keys.add(packet.operation_key)
        # The base RecordingRpc counts successful calls; do not count twice.
        return await super().delivery(packet)

    async def status(self, request, operation_key: str, fence: int):
        self.status_calls += 1
        if operation_key not in self.delivered_keys:
            return self._worker(request, operation_key, fence, "unknown", executor_id=self._receiver(request))
        return self._worker(request, operation_key, fence, "complete", executor_id=self._receiver(request))


def _build_stack_on_existing_db(
    tmp_path,
    monkeypatch,
    request,
    *,
    db,
    rpc,
    eligibility_provider,
    handoff_provider,
    principal_lookup,
    gate_timeout=0.05,
):
    """Build a NEW coordinator over SAME fake ledger and SAME provider objects."""

    monkeypatch.setenv("HANDOFF_CONTRACTS_DIR", str(tmp_path / "handoff_contracts"))
    eligibility_mod = _must_import("services.northena.execution_eligibility")
    handoff_mod = _must_import("services.mkondo.execution_handoff")
    adapter = EngineAdapter(
        request.kind,
        request.engine,
        rpc.submit,
        rpc.status,
        rpc.cancel,
        timeout_seconds=gate_timeout,
        delivery_rpc=rpc.delivery if request.kind != "source" else None,
    )
    bindings = ExecutionBindings(
        decisions=_must_import("test_model_handoff_red_contract")._SyntheticDecisions(),
        inspector=_must_import("test_model_handoff_red_contract")._SyntheticInspector(),
        executors={(request.kind, request.engine): adapter},
        eligibility=eligibility_mod.InputEligibility(journal=None, provider=eligibility_provider, timeout_seconds=gate_timeout),
        handoffs=handoff_mod.MkondoHandoff(journal=None, authority=None, provider=handoff_provider, timeout_seconds=gate_timeout),
        gate_timeout_seconds=gate_timeout,
    )
    coordinator = build_coordinator(db, bindings)
    coordinator.authority.principal_lookup = principal_lookup
    return SimpleNamespace(request=request, db=db, coordinator=coordinator, rpc=rpc)


def _install_append_fault(stack, *, slot_matcher, timing: str, marker: dict):
    """Fault-once journal append hook wired to bound gate consumers via journal."""

    original_append = stack.coordinator.journal.append

    async def wrapped(request, slot, data):
        if not marker["fired"] and slot_matcher(slot, data):
            marker["fired"] = True
            if timing == "before":
                raise OSError(f"synthetic crash before append slot={slot}")
            value = await original_append(request, slot, data)
            raise OSError(f"synthetic crash after committed append slot={slot}")
        return await original_append(request, slot, data)

    stack.coordinator.journal.append = wrapped


@pytest.mark.parametrize(
    "case,matcher,timing,expect_unknown,expect_crash",
    [
        ("before_eligibility", lambda slot, _data: slot == "eligibility", "before", False, True),
        ("before_handoff", lambda slot, _data: slot == "handoff", "before", False, True),
        ("before_handoff_ack", lambda slot, _data: slot == "handoff_ack", "before", False, True),
        ("before_send", lambda slot, data: slot == "send" and data.get("action") == "submit", "before", False, True),
        ("after_send_commit", lambda slot, data: slot == "send" and data.get("action") == "submit", "after", True, True),
        (
            "after_send_response_lost",
            lambda slot, _data: slot == "uncertain:dispatch",
            "after",
            True,
            True,
        ),
        ("after_observation", lambda slot, _data: slot.startswith("observation:"), "after", False, False),
        ("after_terminal", lambda slot, _data: slot == "terminal", "after", False, True),
    ],
)
def test_restart_fail_once_durable_recovery_paths(monkeypatch, tmp_path, case, matcher, timing, expect_unknown, expect_crash):
    """Fail-once before gate appends and after committed rows with restart on same ledger."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"}, lose_delivery_once=(case == "after_send_response_lost"))
    eligibility_provider = EligibilityProvider()
    handoff_provider = HandoffProvider(receiver_id="rx-skill")
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
    )
    marker = {"fired": False}
    _install_append_fault(stack, slot_matcher=matcher, timing=timing, marker=marker)

    first_view = None
    crashed = False
    try:
        first_view = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    except OSError:
        crashed = True

    assert crashed is expect_crash
    assert marker["fired"] is True
    if case == "after_observation":
        assert first_view is not None
        assert first_view.phase == "unknown"

    first_rows = _rows(stack)
    first_dispatch = next((row for row in first_rows if row["slot"] == "dispatch"), None)
    if case.startswith("before_"):
        assert all(row["slot"] != "send" for row in first_rows)
        assert rpc.delivery_calls == 0

    restarted = _build_stack_on_existing_db(
        tmp_path,
        monkeypatch,
        request,
        db=stack.db,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
        principal_lookup=_principal_lookup(),
    )
    second = _run_in_scope(request.principal_id, request.tenant_id, restarted.coordinator.advance(request))

    if expect_unknown:
        assert second.phase == "unknown"
        assert second.reason_code in {"EXECUTOR_OUTCOME_UNCERTAIN", "EXECUTOR_UNKNOWN"}
        # Status-only reconciliation (no blind delivery replay).
        third = _run_in_scope(request.principal_id, request.tenant_id, restarted.coordinator.advance(request))
        assert third.phase == "unknown"
        assert rpc.delivery_calls == (0 if case == "after_send_commit" else 1)
        assert rpc.status_calls >= 1
    else:
        assert second.phase in {"ready", "running", "unknown", "held"}
        if second.phase != "ready":
            second = _run_in_scope(request.principal_id, request.tenant_id, restarted.coordinator.advance(request))
        assert second.phase == "ready"

    rows = _rows(restarted)
    dispatch = next(row for row in rows if row["slot"] == "dispatch")
    if first_dispatch is not None:
        assert dispatch["data"]["operation_key"] == first_dispatch["data"]["operation_key"]
        assert dispatch["seq"] == first_dispatch["seq"]

    if not expect_unknown:
        assert rpc.delivery_calls == 1
        assert len([r for r in rows if r["slot"] == "send" and r["data"].get("action") == "submit"]) == 1
        assert len([r for r in rows if r["slot"] == "metered"]) == 1
        assert len([r for r in rows if r["slot"] == "terminal"]) == 1


def test_projection_failure_before_native_call_restarts_without_new_handoff(monkeypatch, tmp_path):
    """Envelope is banked before projection; failed projection should not append ACK/send."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})
    eligibility_provider = EligibilityProvider()
    handoff_provider = HandoffProvider(receiver_id="rx-skill")
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
    )
    projection_mod = _must_import("services.mkondo.execution_projection")
    original_admit = projection_mod.admit_handoff

    def fail_admit(_payload):
        raise OSError("synthetic native projection fail before admit")

    monkeypatch.setattr(projection_mod, "admit_handoff", fail_admit)
    first = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert first.phase == "held"
    assert first.reason_code == "HANDOFF_PROJECTION_UNAVAILABLE"

    rows = _rows(stack)
    slots = [row["slot"] for row in rows]
    assert "handoff" in slots
    assert "handoff_ack" not in slots
    assert "send" not in slots
    handoff_id = next(row for row in rows if row["slot"] == "handoff")["data"]["contract"]["handoff_id"]
    path = Path(str(tmp_path / "handoff_contracts")) / f"{handoff_id}.json"
    assert not path.exists()

    admit_calls = {"count": 0}

    def spy_admit(payload):
        assert any(
            doc["payload"].get("slot") == "handoff"
            for doc in stack.db["ledger_v1_control_events"].docs
            if doc["payload"].get("principal_id") == request.principal_id
        )
        admit_calls["count"] += 1
        return original_admit(payload)

    monkeypatch.setattr(projection_mod, "admit_handoff", spy_admit)
    restarted = _build_stack_on_existing_db(
        tmp_path,
        monkeypatch,
        request,
        db=stack.db,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
        principal_lookup=_principal_lookup(),
    )
    second = _run_in_scope(request.principal_id, request.tenant_id, restarted.coordinator.advance(request))
    assert second.phase == "ready"
    rows_after = _rows(restarted)
    assert len([row for row in rows_after if row["slot"] == "handoff"]) == 1
    assert len([row for row in rows_after if row["slot"] == "handoff_ack"]) == 1
    assert len([row for row in rows_after if row["slot"] == "send"]) == 1
    assert admit_calls["count"] == 1


def test_projection_file_saved_then_exception_restart_attests_without_second_admit(monkeypatch, tmp_path):
    """If process crashes after file projection, restart must attest exact file without overwrite."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})
    eligibility_provider = EligibilityProvider()
    handoff_provider = HandoffProvider(receiver_id="rx-skill")
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
    )
    handoff_mod = _must_import("services.mkondo.execution_handoff")
    original_project = handoff_mod.project

    def project_then_crash(contract, directory):
        original_project(contract, directory)
        raise OSError("synthetic crash after projection persisted")

    monkeypatch.setattr(handoff_mod, "project", project_then_crash)
    with pytest.raises(OSError):
        _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))

    rows = _rows(stack)
    handoff = next(row for row in rows if row["slot"] == "handoff")
    handoff_id = handoff["data"]["contract"]["handoff_id"]
    path = Path(str(tmp_path / "handoff_contracts")) / f"{handoff_id}.json"
    assert path.exists()
    persisted_before = json.loads(path.read_text())

    projection_mod = _must_import("services.mkondo.execution_projection")
    original_admit = projection_mod.admit_handoff
    admit_calls = {"count": 0}

    def spy_admit(payload):
        admit_calls["count"] += 1
        return original_admit(payload)

    monkeypatch.setattr(handoff_mod, "project", original_project)
    monkeypatch.setattr(projection_mod, "admit_handoff", spy_admit)
    restarted = _build_stack_on_existing_db(
        tmp_path,
        monkeypatch,
        request,
        db=stack.db,
        rpc=rpc,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
        principal_lookup=_principal_lookup(),
    )
    second = _run_in_scope(request.principal_id, request.tenant_id, restarted.coordinator.advance(request))
    assert second.phase == "ready"
    assert json.loads(path.read_text()) == persisted_before
    assert admit_calls["count"] == 0


@pytest.mark.parametrize("builder", [_source_request, _skill_request])
def test_cancel_wins_between_rows_check_and_send_insert(monkeypatch, tmp_path, builder):
    """Cancellation beats submit between final gate check and send-slot insert."""

    request = builder()
    rpc = DeliveryAwareRpc({request.kind: f"rx-{request.kind}"})
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        handoff_provider=HandoffProvider(receiver_id=f"rx-{request.kind}"),
    )

    reached_submit = asyncio.Event()
    release_submit = asyncio.Event()
    original_append = stack.coordinator.journal.append

    async def delayed_send_append(req, slot, data):
        if slot == "send" and data.get("action") == "submit":
            reached_submit.set()
            await release_submit.wait()
        return await original_append(req, slot, data)

    stack.coordinator.journal.append = delayed_send_append

    async def scoped(coro):
        with principal_context(request.principal_id):
            with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
                return await coro

    async def run_race():
        t_advance = asyncio.create_task(scoped(stack.coordinator.advance(request)))
        await asyncio.wait_for(reached_submit.wait(), timeout=2)
        t_cancel = asyncio.create_task(scoped(stack.coordinator.cancel(request)))
        await asyncio.sleep(0.01)
        release_submit.set()
        return await asyncio.gather(t_advance, t_cancel)

    advance_view, cancel_view = asyncio.run(run_race())
    assert cancel_view.phase == "cancelled"
    assert advance_view.phase in {"held", "cancelled", "unknown"}
    assert rpc.submit_calls == 0
    assert rpc.delivery_calls == 0
    assert rpc.status_calls == 0
    rows = _rows(stack)
    assert any(row["slot"] == "send" and row["data"].get("action") == "cancel" for row in rows)
    assert all(row["slot"] != "metered" for row in rows)


def test_duplicate_advance_barrier_exactly_one_delivery_no_legacy_submit(monkeypatch, tmp_path):
    """Concurrent advances at send claim: one delivery, one canonical send/terminal/metering."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        handoff_provider=HandoffProvider(receiver_id="rx-skill"),
    )

    waiters = {"count": 0}
    release = asyncio.Event()
    original_append = stack.coordinator.journal.append

    async def barrier_send(req, slot, data):
        if slot == "send" and data.get("action") == "submit":
            waiters["count"] += 1
            if waiters["count"] == 2:
                release.set()
            await release.wait()
        return await original_append(req, slot, data)

    stack.coordinator.journal.append = barrier_send

    async def scoped(coro):
        with principal_context(request.principal_id):
            with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
                return await coro

    async def run_pair():
        t1 = asyncio.create_task(scoped(stack.coordinator.advance(request)))
        t2 = asyncio.create_task(scoped(stack.coordinator.advance(request)))
        return await asyncio.gather(t1, t2)

    pair = asyncio.run(run_pair())
    assert len(pair) == 2
    final = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert final.phase == "ready"
    rows = _rows(stack)
    assert len([row for row in rows if row["slot"] == "send" and row["data"].get("action") == "submit"]) == 1
    assert len([row for row in rows if row["slot"] == "metered"]) == 1
    assert len([row for row in rows if row["slot"] == "terminal"]) == 1
    assert rpc.delivery_calls == 1
    assert rpc.submit_calls == 0


def test_missing_principal_uses_native_get_principal_and_holds_without_handoff_writes(monkeypatch, tmp_path):
    """Unknown receiver must invoke real native get_principal refusal mapping to Held."""

    request = _skill_request()
    unknown_receiver = f"rx-unknown-{uuid4().hex}"
    rpc = DeliveryAwareRpc({request.kind: unknown_receiver})
    base_lookup = _principal_lookup()

    def lookup(pid):
        if pid == unknown_receiver:
            return get_principal(pid)
        return base_lookup(pid)

    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        handoff_provider=HandoffProvider(receiver_id=unknown_receiver),
        principal_lookup=lookup,
    )
    view = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert view.phase == "held"
    assert view.reason_code == "PRINCIPAL_NOT_ADMITTED"
    slots = [row["slot"] for row in _rows(stack)]
    assert "handoff" not in slots
    assert "handoff_ack" not in slots
    assert "send" not in slots
    assert rpc.delivery_calls == 0


def test_component_authority_principal_refusal_maps_held_runtimeerror_propagates():
    """Exact PrincipalRefusal maps Held; unrelated RuntimeError must not be swallowed."""

    authority_mod = _must_import("services.northena.execution_authority")
    auth_refusal = authority_mod.ComponentAuthority(db={"ledger_v1_control_events": _FakeCollection()}, decisions=None)
    auth_refusal.principal_lookup = lambda _pid: get_principal(f"never-admitted-{uuid4().hex}")
    with pytest.raises(Held) as held_exc:
        auth_refusal.principal("rx-missing")
    assert held_exc.value.reason_code == "PRINCIPAL_NOT_ADMITTED"
    assert auth_refusal.db["ledger_v1_control_events"].docs == []

    auth_runtime = authority_mod.ComponentAuthority(
        db={"ledger_v1_control_events": _FakeCollection()},
        decisions=None,
        principal_lookup=lambda _pid: (_ for _ in ()).throw(RuntimeError("unrelated runtime")),
    )
    with pytest.raises(RuntimeError):
        auth_runtime.principal("rx-missing")


@pytest.mark.parametrize(
    "mutate",
    [
        lambda a, *_: a.model_copy(update={"operation_key": "op-tampered"}),
        lambda a, *_: a.model_copy(update={"fence": a.fence + 1}),
        lambda a, *_: a.model_copy(update={"receiver_task_id": "rx_task_tampered"}),
        lambda a, *_: a.model_copy(update={"scope_refs": ("scope://tampered",)}),
        lambda a, *_: a.model_copy(update={"evidence_mode": "mocked"}),
    ],
)
def test_ack_tamper_fields_block_send_no_delivery(monkeypatch, tmp_path, mutate):
    """Focused ACK tamper checks: key/fence/task/scope/evidence_mode refuse pre-send."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})
    provider = HandoffProvider(receiver_id="rx-skill", mutate_ack=mutate)
    stack = _build_stack(tmp_path, monkeypatch, request, rpc=rpc, handoff_provider=provider)
    view = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert view.phase == "held"
    assert view.reason_code in {"HANDOFF_ACK_BINDING_INVALID", "HANDOFF_ACK_INVALID"}
    assert rpc.delivery_calls == 0
    assert all(row["slot"] != "send" for row in _rows(stack))


@pytest.mark.parametrize("field,value", [("rule_pack_refs", ("akki://pack/input/changed",)), ("snapshot_refs", ("akki://snapshot/input/changed",))])
def test_changed_pinned_pack_snapshot_basis_blocks_send(monkeypatch, tmp_path, field, value):
    """Pinned eligibility basis changes at send are held and must not deliver."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})

    def mutate(receipt, _request, _purpose, phase):
        if phase == "send":
            return receipt.model_copy(update={field: value})
        return receipt

    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        eligibility_provider=EligibilityProvider(mutate=mutate),
        handoff_provider=HandoffProvider(receiver_id="rx-skill"),
    )
    view = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert view.phase == "held"
    assert view.reason_code == "INPUT_ELIGIBILITY_BASIS_CHANGED"
    assert rpc.delivery_calls == 0


def test_changed_receiver_mandate_between_prepare_and_send_blocks_delivery(monkeypatch, tmp_path):
    """Receiver mandate drift between prepare and send revalidation must hold pre-send."""

    request = _skill_request()
    rpc = DeliveryAwareRpc({request.kind: "rx-skill"})
    calls = {"n": 0}

    def mutate_binding(binding, *_args):
        calls["n"] += 1
        if calls["n"] >= 2:
            return binding.model_copy(update={"mandate_ref": "akki://mandate/2"})
        return binding

    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        rpc=rpc,
        handoff_provider=HandoffProvider(receiver_id="rx-skill", mutate_binding=mutate_binding),
    )
    view = _run_in_scope(request.principal_id, request.tenant_id, stack.coordinator.advance(request))
    assert view.phase == "held"
    assert view.reason_code == "HANDOFF_BASIS_CHANGED"
    assert rpc.delivery_calls == 0
