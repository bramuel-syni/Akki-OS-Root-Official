"""Supplemental behavioral coverage for model-handoff contract (iteration34).

Focus: gate/fault/concurrency behaviors that were omitted from iteration33.
All providers/adapters here are SYNTHETIC/FAKE and isolated.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.mongo_control import digest
from services.northena.execution_bindings import ExecutionBindings, build_coordinator
from services.northena.execution_models import Artifact, Held, Request, Usage, WorkerResult
from services.northena.execution_ports import EngineAdapter
from services.principal_store.store import Principal, PrincipalRefusal
from contracts.principal_v1 import PrincipalKind, PrincipalV1

from test_model_handoff_red_contract import (
    _FakeCollection,
    _FakeDb,
    _SyntheticDecisions,
    _SyntheticInspector,
    _evaluation_request,
    _principal_lookup,
    _run_in_scope,
    _seed_entitlements,
    _skill_request,
    _training_request,
)


def _must_import(name: str):
    module = __import__(name, fromlist=["*"])
    return module


class RecordingRpc:
    def __init__(
        self,
        receiver_by_kind: dict[str, str],
        wrong_mode: str | None = None,
        timeout_on_submit=False,
        timeout_on_delivery=False,
    ):
        self.receiver_by_kind = receiver_by_kind
        self.wrong_mode = wrong_mode
        self.timeout_on_submit = timeout_on_submit
        self.timeout_on_delivery = timeout_on_delivery
        self.submit_calls = 0
        self.delivery_calls = 0
        self.status_calls = 0
        self.cancel_calls = 0

    def _receiver(self, request: Request) -> str:
        return self.receiver_by_kind.get(request.kind, f"rx-{request.kind}")

    def _worker(self, request: Request, operation_key: str, fence: int, state: str, executor_id: str | None = None):
        label = request.result_floor or "non_factual"
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id=executor_id or self._receiver(request),
            fence=fence,
            state=state,
            receipt_ref=f"akki://receipt/{state}",
            artifacts=(
                Artifact(
                    ref=f"akki://artifact/{request.request_id}",
                    sha256="b" * 64,
                    size_bytes=8,
                    tenant_id=request.tenant_id,
                    class_label=label,
                ),
            )
            if state == "complete"
            else (),
            usage=(Usage(unit="tokens", quantity="5"),) if state in {"complete", "cancelled", "failed"} else None,
            evidence_mode="measured",
        )

    async def submit(self, request: Request, operation_key: str, fence: int, _authority):
        self.submit_calls += 1
        if self.timeout_on_submit:
            raise TimeoutError("synthetic submit timeout")
        executor_id = "wrong-exec" if self.wrong_mode == "submit" else self._receiver(request)
        return self._worker(request, operation_key, fence, "accepted", executor_id=executor_id)

    async def delivery(self, packet):
        self.delivery_calls += 1
        if self.timeout_on_delivery:
            raise TimeoutError("synthetic delivery timeout")
        executor_id = "wrong-exec" if self.wrong_mode == "delivery" else packet.binding.receiver_principal_id
        return WorkerResult(
            operation_key=packet.operation_key,
            request_sha256=packet.request.digest(),
            executor_id=executor_id,
            fence=packet.fence,
            state="accepted",
            receipt_ref="akki://receipt/delivery",
            artifacts=(),
            usage=None,
            evidence_mode="measured",
        )

    async def status(self, request: Request, operation_key: str, fence: int):
        self.status_calls += 1
        executor_id = "wrong-exec" if self.wrong_mode == "status" else self._receiver(request)
        return self._worker(request, operation_key, fence, "complete", executor_id=executor_id)

    async def cancel(self, request: Request, operation_key: str, fence: int):
        self.cancel_calls += 1
        executor_id = "wrong-exec" if self.wrong_mode == "cancel" else self._receiver(request)
        return self._worker(request, operation_key, fence, "cancelled", executor_id=executor_id)


class EligibilityProvider:
    def __init__(self, mutate=None, sleep_seconds: float = 0):
        self.mutate = mutate
        self.sleep_seconds = sleep_seconds

    async def evaluate(self, request, purpose, phase):
        if self.sleep_seconds:
            await asyncio.sleep(self.sleep_seconds)
        mod = _must_import("services.northena.execution_eligibility")
        receipt = mod.EligibilityReceipt(
            request_sha256=request.digest(),
            input_refs=request.input_refs,
            scope_refs=request.scope_refs,
            purpose=purpose,
            policy_ref="akki://policy/input/1",
            rule_pack_refs=("akki://pack/input/1",),
            snapshot_refs=("akki://snapshot/input/1",),
            decision_ref="akki://decision/input/1",
            disposition="eligible",
            reason_code="ELIGIBLE",
            expires_epoch=4_102_444_800,
            evidence_mode="measured",
        )
        return self.mutate(receipt, request, purpose, phase) if self.mutate else receipt


class HandoffProvider:
    def __init__(self, receiver_id: str, mutate_binding=None, mutate_ack=None, receiver_sleep=0, ack_sleep=0):
        self.receiver_id = receiver_id
        self.mutate_binding = mutate_binding
        self.mutate_ack = mutate_ack
        self.receiver_sleep = receiver_sleep
        self.ack_sleep = ack_sleep

    async def receiver(self, request, grant, operation_key, _fence):
        if self.receiver_sleep:
            await asyncio.sleep(self.receiver_sleep)
        delivery = _must_import("services.mkondo.execution_delivery")
        binding = delivery.ReceiverBinding(
            request_sha256=request.digest(),
            authority_ref=grant.authority_ref,
            operation_key=operation_key,
            receiver_principal_id=self.receiver_id,
            receiver_app="mkondo",
            receiver_role="worker",
            receiver_task_id=delivery.receiver_task_id(request.request_id, operation_key, self.receiver_id),
            scope_refs=request.scope_refs,
            shape_sha256=delivery.shape_sha256(request),
            mandate_ref="akki://mandate/1",
            expires_epoch=4_102_444_800,
            evidence_mode="measured",
        )
        return self.mutate_binding(binding, request, grant, operation_key) if self.mutate_binding else binding

    async def acknowledge(self, request, contract, binding, operation_key, fence):
        if self.ack_sleep:
            await asyncio.sleep(self.ack_sleep)
        delivery = _must_import("services.mkondo.execution_delivery")
        ack = delivery.HandoffAck(
            handoff_id=contract.handoff_id,
            contract_sha256=digest(contract.model_dump(mode="json")),
            request_sha256=request.digest(),
            operation_key=operation_key,
            fence=fence,
            receiver_principal_id=binding.receiver_principal_id,
            receiver_task_id=binding.receiver_task_id,
            scope_refs=request.scope_refs,
            shape_sha256=binding.shape_sha256,
            receipt_ref="akki://ack/1",
            expires_epoch=4_102_444_800,
            evidence_mode="measured",
        )
        return self.mutate_ack(ack, request, contract, binding, operation_key, fence) if self.mutate_ack else ack


def _build_stack(
    tmp_path,
    monkeypatch,
    request: Request,
    *,
    gate_timeout=0.05,
    include_eligibility=True,
    include_handoff=True,
    include_delivery=True,
    eligibility_provider=None,
    handoff_provider=None,
    rpc=None,
    principal_lookup=None,
):
    monkeypatch.setenv("HANDOFF_CONTRACTS_DIR", str(tmp_path / "handoff_contracts"))
    db = _FakeDb({"ledger_v1_control_events": _FakeCollection()})
    _seed_entitlements(db, tenant_id=request.tenant_id, principal_id=request.principal_id)
    receiver_id = f"rx-{request.kind}"
    rpc = rpc or RecordingRpc({request.kind: receiver_id})
    eligibility_mod = _must_import("services.northena.execution_eligibility")
    handoff_mod = _must_import("services.mkondo.execution_handoff")

    adapter = EngineAdapter(
        request.kind,
        request.engine,
        rpc.submit,
        rpc.status,
        rpc.cancel,
        timeout_seconds=gate_timeout,
        delivery_rpc=rpc.delivery if include_delivery else None,
    )
    bindings = ExecutionBindings(
        decisions=_SyntheticDecisions(),
        inspector=_SyntheticInspector(),
        executors={(request.kind, request.engine): adapter},
        eligibility=(
            eligibility_mod.InputEligibility(
                journal=None,
                provider=eligibility_provider or EligibilityProvider(),
                timeout_seconds=gate_timeout,
            )
            if include_eligibility
            else None
        ),
        handoffs=(
            handoff_mod.MkondoHandoff(
                journal=None,
                authority=None,
                provider=handoff_provider or HandoffProvider(receiver_id),
                timeout_seconds=gate_timeout,
            )
            if include_handoff
            else None
        ),
        gate_timeout_seconds=gate_timeout,
    )
    coordinator = build_coordinator(db, bindings)
    coordinator.authority.principal_lookup = principal_lookup or _principal_lookup()
    return SimpleNamespace(request=request, db=db, coordinator=coordinator, rpc=rpc)


def _advance(stack):
    req = stack.request
    return _run_in_scope(req.principal_id, req.tenant_id, stack.coordinator.advance(req))


def _cancel(stack):
    req = stack.request
    return _run_in_scope(req.principal_id, req.tenant_id, stack.coordinator.cancel(req))


def _rows(stack):
    req = stack.request
    return _run_in_scope(req.principal_id, req.tenant_id, stack.coordinator.journal.read(req))


# Module/feature: finite timeout enforced for gate/adapter bindings.
@pytest.mark.parametrize("invalid", [None, 0, False, float("nan"), float("inf")])
def test_invalid_gate_timeouts_rejected(monkeypatch, tmp_path, invalid):
    request = _skill_request()
    with pytest.raises(ValueError):
        _build_stack(tmp_path, monkeypatch, request, gate_timeout=invalid)


# Module/feature: missing gate bindings produce holds, not implicit bypass.
@pytest.mark.parametrize(
    "include_eligibility,include_handoff,include_delivery,reason",
    [
        (False, True, True, "INPUT_ELIGIBILITY_NOT_BOUND"),
        (True, False, True, "HANDOFF_PRODUCER_NOT_BOUND"),
        (True, True, False, "DELIVERY_RPC_NOT_BOUND"),
    ],
)
def test_missing_gate_or_delivery_bindings_hold(monkeypatch, tmp_path, include_eligibility, include_handoff, include_delivery, reason):
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        _skill_request(),
        include_eligibility=include_eligibility,
        include_handoff=include_handoff,
        include_delivery=include_delivery,
    )
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == reason


# Module/feature: producer timeouts fail-closed across eligibility/receiver/ack.
@pytest.mark.parametrize("layer", ["eligibility", "receiver", "ack"])
def test_timeouts_hold_fail_closed(monkeypatch, tmp_path, layer):
    request = _skill_request()
    eligibility_provider = EligibilityProvider(sleep_seconds=0.1) if layer == "eligibility" else EligibilityProvider()
    handoff_provider = HandoffProvider(
        receiver_id="rx-skill",
        receiver_sleep=0.1 if layer == "receiver" else 0,
        ack_sleep=0.1 if layer == "ack" else 0,
    )
    stack = _build_stack(
        tmp_path,
        monkeypatch,
        request,
        gate_timeout=0.01,
        eligibility_provider=eligibility_provider,
        handoff_provider=handoff_provider,
    )
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == "EVIDENCE_PRODUCER_UNAVAILABLE"


# Module/feature: eligibility receipt/request binding and disposition controls are strict.
@pytest.mark.parametrize(
    "mutate,expected",
    [
        (lambda r, *_: r.model_copy(update={"request_sha256": "0" * 64}), "INPUT_ELIGIBILITY_BINDING_INVALID"),
        (lambda r, request, *_: r.model_copy(update={"input_refs": tuple(reversed(request.input_refs))}), "INPUT_ELIGIBILITY_BINDING_INVALID"),
        (lambda r, *_: r.model_copy(update={"scope_refs": ("scope://other",)}), "INPUT_ELIGIBILITY_BINDING_INVALID"),
        (lambda r, *_: r.model_copy(update={"purpose": "training_material"}), "INPUT_ELIGIBILITY_BINDING_INVALID"),
        (lambda r, *_: r.model_copy(update={"evidence_mode": "MOCKED"}), "INPUT_ELIGIBILITY_BINDING_INVALID"),
        (lambda r, *_: r.model_copy(update={"expires_epoch": 1}), "INPUT_ELIGIBILITY_EXPIRED"),
        (lambda r, *_: r.model_copy(update={"disposition": "unknown"}), "INPUT_NOT_ELIGIBLE"),
        (lambda r, *_: r.model_copy(update={"disposition": "ineligible"}), "INPUT_NOT_ELIGIBLE"),
        (lambda r, *_: r.model_copy(update={"disposition": "not_assessed"}), "INPUT_NOT_ELIGIBLE"),
    ],
)
def test_invalid_eligibility_receipts_hold(monkeypatch, tmp_path, mutate, expected):
    provider = EligibilityProvider(mutate=mutate)
    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), eligibility_provider=provider)
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == expected


# Module/feature: pinned policy/pack/snapshot basis cannot mutate between reserve and send.
def test_changed_eligibility_basis_after_reserve_holds(monkeypatch, tmp_path):
    def mutate(receipt, _request, _purpose, phase):
        if phase == "send":
            return receipt.model_copy(update={"policy_ref": "akki://policy/input/2"})
        return receipt

    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), eligibility_provider=EligibilityProvider(mutate=mutate))
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == "INPUT_ELIGIBILITY_BASIS_CHANGED"


# Module/feature: withdrawal in send/verify/publish/retrieve never reaches ready; post-effect usage remains metered.
@pytest.mark.parametrize("blocked_phase", ["send", "verify", "publish", "retrieve"])
def test_withdrawal_phase_blocks_readiness_and_preserves_usage_post_effect(monkeypatch, tmp_path, blocked_phase):
    def mutate(receipt, _request, _purpose, phase):
        if phase == blocked_phase:
            return receipt.model_copy(update={"disposition": "ineligible"})
        return receipt

    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), eligibility_provider=EligibilityProvider(mutate=mutate))
    view = _advance(stack)
    assert view.phase != "ready"
    rows = _rows(stack)
    slots = [row["slot"] for row in rows]
    if blocked_phase in {"verify", "publish", "retrieve"}:
        assert "metered" in slots


# Module/feature: receiver binding strict cross-field validation.
@pytest.mark.parametrize(
    "mutate,expected",
    [
        (lambda b, request, *_: b.model_copy(update={"receiver_principal_id": request.principal_id}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"request_sha256": "0" * 64}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"authority_ref": "auth://other"}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"operation_key": "op-other"}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"scope_refs": ("scope://other",)}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"shape_sha256": "a" * 64}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"evidence_mode": "MOCKED"}), "RECEIVER_BINDING_MISMATCH"),
        (lambda b, *_: b.model_copy(update={"expires_epoch": 1}), "RECEIVER_BINDING_EXPIRED"),
    ],
)
def test_receiver_binding_mismatches_hold(monkeypatch, tmp_path, mutate, expected):
    provider = HandoffProvider(receiver_id="rx-skill", mutate_binding=mutate)
    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), handoff_provider=provider)
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == expected


# Module/feature: unknown/suspended receiver principals are held (not server 500).
def test_unknown_receiver_lookup_refusal_is_held(monkeypatch, tmp_path):
    base_lookup = _principal_lookup()

    def lookup(pid):
        if pid.startswith("rx-"):
            raise PrincipalRefusal(f"principal {pid!r} not admitted")
        return base_lookup(pid)

    stack = _build_stack(
        tmp_path,
        monkeypatch,
        _skill_request(),
        handoff_provider=HandoffProvider(receiver_id="rx-skill"),
        principal_lookup=lookup,
    )
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == "PRINCIPAL_NOT_ADMITTED"


def test_suspended_receiver_is_held(monkeypatch, tmp_path):
    base_lookup = _principal_lookup()

    def lookup(pid):
        if pid == "rx-skill":
            return Principal(
                PrincipalV1(
                    principal_id="rx-skill",
                    kind=PrincipalKind.INDIVIDUAL,
                    legal_identity="rx-skill",
                    trust_domain_identifier="td-1",
                    admission_time_mandate="synthetic",
                    behavioural_signature_state="watch:baseline@admission",
                    parent_organisation_id="org-1",
                    autonomy_scope=None,
                    admit_authority=False,
                    suspended=True,
                )
            )
        return base_lookup(pid)

    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), principal_lookup=lookup)
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == "PRINCIPAL_UNAVAILABLE"


# Module/feature: malformed/mutated ACK refuses before send/delivery.
@pytest.mark.parametrize(
    "mutate,expected",
    [
        (lambda a, *_: a.model_copy(update={"handoff_id": "ho_other"}), "HANDOFF_ACK_BINDING_INVALID"),
        (lambda a, *_: a.model_copy(update={"contract_sha256": "0" * 64}), "HANDOFF_ACK_BINDING_INVALID"),
        (lambda a, *_: a.model_copy(update={"request_sha256": "0" * 64}), "HANDOFF_ACK_BINDING_INVALID"),
        (lambda a, *_: a.model_copy(update={"receiver_principal_id": "rx-other"}), "HANDOFF_ACK_BINDING_INVALID"),
        (lambda a, *_: a.model_copy(update={"shape_sha256": "0" * 64}), "HANDOFF_ACK_BINDING_INVALID"),
        (lambda a, *_: a.model_copy(update={"expires_epoch": 1}), "HANDOFF_ACK_EXPIRED"),
    ],
)
def test_ack_mismatch_blocks_send(monkeypatch, tmp_path, mutate, expected):
    provider = HandoffProvider(receiver_id="rx-skill", mutate_ack=mutate)
    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), handoff_provider=provider)
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == expected
    slots = [row["slot"] for row in _rows(stack)]
    assert "send" not in slots


# Module/feature: mutated authored_by/source/destination contract fails packet revalidation.
def test_mutated_contract_fails_packet_cross_validation(monkeypatch, tmp_path):
    handoff_mod = _must_import("services.mkondo.execution_handoff")
    stack = _build_stack(tmp_path, monkeypatch, _skill_request())
    request = stack.request
    _advance(stack)
    rows = {row["slot"]: row for row in _rows(stack)}
    dispatch = rows["dispatch"]
    from services.northena.execution_models import Authority

    grant = Authority.model_validate_json(json.dumps(dispatch["data"]["authority"]))
    handoffs = stack.coordinator.handoffs
    binding = _run_in_scope(request.principal_id, request.tenant_id, handoffs.receiver(request, grant, dispatch))
    contract = handoffs.contract(request, binding, dispatch)
    ack = _run_in_scope(
        request.principal_id,
        request.tenant_id,
        handoffs.provider.acknowledge(request, contract, binding, dispatch["data"]["operation_key"], dispatch["seq"]),
    )
    dispatch = rows["dispatch"]

    mutated = contract.model_copy(update={"authored_by": "other-principal"})
    with pytest.raises(Held):
        handoff_mod.MkondoHandoff.packet(
            request,
            grant,
            dispatch,
            mutated,
            binding,
            ack,
            "0" * 64,
            "1" * 64,
            "2" * 64,
            "3" * 64,
        )


# Module/feature: wrong executor identity is refused for delivery/status/cancel paths.
@pytest.mark.parametrize("wrong_mode,expected", [("delivery", "EXECUTOR_RECEIVER_MISMATCH"), ("status", "EXECUTOR_RECEIVER_MISMATCH"), ("cancel", "EXECUTOR_RECEIVER_MISMATCH")])
def test_wrong_executor_identity_refused(monkeypatch, tmp_path, wrong_mode, expected):
    request = _skill_request()
    if wrong_mode == "cancel":
        class CancelRpc(RecordingRpc):
            async def status(self, request: Request, operation_key: str, fence: int):
                self.status_calls += 1
                return self._worker(request, operation_key, fence, "running", executor_id=self._receiver(request))

        rpc = CancelRpc({request.kind: "rx-skill"}, wrong_mode=wrong_mode)
    else:
        rpc = RecordingRpc({request.kind: "rx-skill"}, wrong_mode=wrong_mode)
    stack = _build_stack(tmp_path, monkeypatch, request, rpc=rpc)
    if wrong_mode == "cancel":
        first = _advance(stack)
        assert first.phase in {"running", "unknown", "ready", "held"}
        view = _cancel(stack)
    else:
        view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == expected


# Module/feature: timeout after send commit recovers via status-only reconciliation (no resend).
def test_post_send_timeout_then_status_recovery_without_resubmit(monkeypatch, tmp_path):
    request = _skill_request()
    rpc = RecordingRpc({request.kind: "rx-skill"}, timeout_on_delivery=True)
    stack = _build_stack(tmp_path, monkeypatch, request, rpc=rpc)

    first = _advance(stack)
    assert first.phase == "unknown"
    assert first.reason_code == "EXECUTOR_OUTCOME_UNCERTAIN"
    assert rpc.delivery_calls == 1

    rpc.timeout_on_delivery = False
    second = _advance(stack)
    assert second.phase == "ready"
    assert rpc.delivery_calls == 1
    assert rpc.status_calls >= 1


# Module/feature: projection conflict holds and preserves canonical handoff record.
def test_native_projection_conflict_refuses(monkeypatch, tmp_path):
    stack = _build_stack(tmp_path, monkeypatch, _skill_request())
    first = _advance(stack)
    assert first.phase == "ready"
    rows = {row["slot"]: row for row in _rows(stack)}
    contract = rows["handoff"]["data"]["contract"]
    handoff_dir = Path(str(tmp_path / "handoff_contracts"))
    path = handoff_dir / f"{contract['handoff_id']}.json"
    payload = json.loads(path.read_text())
    payload["authored_by"] = "mutated-author"
    path.write_text(json.dumps(payload))

    view = _run_in_scope(stack.request.principal_id, stack.request.tenant_id, stack.coordinator.retrieve(stack.request))
    assert view.phase == "held"
    assert view.reason_code == "HANDOFF_PROJECTION_CONFLICT"
    rows_after = {row["slot"]: row for row in _rows(stack)}
    assert rows_after["handoff"]["data"]["contract"] == contract


# Module/feature: forced advance/advance interleaving still commits one send/one submit.
def test_concurrent_advance_interleaving_single_send(monkeypatch, tmp_path):
    gate = asyncio.Event()

    async def delayed_receiver(binding, request, grant, operation_key):
        await gate.wait()
        return binding

    provider = HandoffProvider(
        receiver_id="rx-skill",
        mutate_binding=lambda b, request, grant, operation_key: delayed_receiver(b, request, grant, operation_key),
    )

    # Adapt mutate to support coroutine return.
    original = provider.receiver

    async def patched_receiver(request, grant, operation_key, fence):
        base = await original(request, grant, operation_key, fence)
        if asyncio.iscoroutine(base):
            return await base
        return base

    provider.receiver = patched_receiver
    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), handoff_provider=provider)

    async def scoped(coro):
        with principal_context(stack.request.principal_id):
            with bind_control_scope({"principal_id": stack.request.principal_id, "tenant_id": stack.request.tenant_id}):
                return await coro

    async def run_pair():
        t1 = asyncio.create_task(scoped(stack.coordinator.advance(stack.request)))
        t2 = asyncio.create_task(scoped(stack.coordinator.advance(stack.request)))
        await asyncio.sleep(0.02)
        gate.set()
        return await asyncio.gather(t1, t2)

    pair = asyncio.run(run_pair())
    assert len(pair) == 2
    assert stack.rpc.submit_calls <= 1
    send_rows = [r for r in _rows(stack) if r["slot"] == "send"]
    assert len(send_rows) == 1


# Module/feature: cancel wins before send => no submit; loser advance does not fake send/status path.
def test_concurrent_advance_cancel_cancel_wins(monkeypatch, tmp_path):
    gate = asyncio.Event()

    async def delayed_receiver(request, grant, operation_key, _fence):
        await gate.wait()
        delivery = _must_import("services.mkondo.execution_delivery")
        return delivery.ReceiverBinding(
            request_sha256=request.digest(),
            authority_ref=grant.authority_ref,
            operation_key=operation_key,
            receiver_principal_id="rx-skill",
            receiver_app="mkondo",
            receiver_role="worker",
            receiver_task_id=delivery.receiver_task_id(request.request_id, operation_key, "rx-skill"),
            scope_refs=request.scope_refs,
            shape_sha256=delivery.shape_sha256(request),
            mandate_ref="akki://mandate/1",
            expires_epoch=4_102_444_800,
            evidence_mode="measured",
        )

    provider = HandoffProvider(receiver_id="rx-skill")
    provider.receiver = delayed_receiver
    stack = _build_stack(tmp_path, monkeypatch, _skill_request(), handoff_provider=provider)

    async def scoped(coro):
        with principal_context(stack.request.principal_id):
            with bind_control_scope({"principal_id": stack.request.principal_id, "tenant_id": stack.request.tenant_id}):
                return await coro

    async def run_race():
        t_adv = asyncio.create_task(scoped(stack.coordinator.advance(stack.request)))
        await asyncio.sleep(0.02)
        t_cancel = asyncio.create_task(scoped(stack.coordinator.cancel(stack.request)))
        await asyncio.sleep(0.02)
        gate.set()
        return await asyncio.gather(t_adv, t_cancel)

    advance_view, cancel_view = asyncio.run(run_race())
    assert cancel_view.phase == "cancelled"
    assert stack.rpc.submit_calls == 0
    assert stack.rpc.status_calls == 0
    assert advance_view.phase in {"held", "cancelled", "unknown"}


# Module/feature: legacy protocol-less dispatch remains status-only, never forced submit.
def test_legacy_dispatch_without_protocol_is_status_only(monkeypatch, tmp_path):
    request = Request(
        request_id="req-legacy-supp-1",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind="source",
        engine="mtafiti",
        objective_sha256="a" * 64,
        input_refs=("akki://source/rms",),
        scope_refs=("rms",),
        deadline_epoch=4_102_444_800,
    )
    stack = _build_stack(tmp_path, monkeypatch, request, include_eligibility=False, include_handoff=False)
    authority = _must_import("services.northena.execution_models").Authority(
        authority_ref="auth://legacy",
        request_sha256=request.digest(),
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        scope_refs=request.scope_refs,
        engine=request.engine,
        expires_epoch=4_102_444_800,
        terms_ref="terms://dispatch/v1",
        policy_epoch=1,
    )
    _run_in_scope(
        request.principal_id,
        request.tenant_id,
        stack.coordinator.journal.append(
            request,
            "dispatch",
            {"operation_key": "op-legacy-supp", "request_sha256": request.digest(), "action": "submit", "authority": authority.model_dump(mode="json")},
        ),
    )
    view = _advance(stack)
    assert view.phase in {"held", "unknown", "ready"}
    assert stack.rpc.submit_calls == 0


# Module/feature: no class lift on verification floor.
def test_defensibility_floor_not_silently_lifted(monkeypatch, tmp_path):
    request = _evaluation_request().model_copy(update={"result_floor": "fact"})

    class LowClassRpc(RecordingRpc):
        async def status(self, request: Request, operation_key: str, fence: int):
            self.status_calls += 1
            return WorkerResult(
                operation_key=operation_key,
                request_sha256=request.digest(),
                executor_id=self._receiver(request),
                fence=fence,
                state="complete",
                receipt_ref="akki://receipt/complete",
                artifacts=(
                    Artifact(
                        ref=f"akki://artifact/{request.request_id}",
                        sha256="b" * 64,
                        size_bytes=8,
                        tenant_id=request.tenant_id,
                        class_label="non_factual",
                    ),
                ),
                usage=(Usage(unit="tokens", quantity="3"),),
                evidence_mode="measured",
            )

    rpc = LowClassRpc({request.kind: "rx-evaluation"})
    stack = _build_stack(tmp_path, monkeypatch, request, rpc=rpc)
    view = _advance(stack)
    assert view.phase == "held"
    assert view.reason_code == "DEFENSIBILITY_BELOW_FLOOR"
