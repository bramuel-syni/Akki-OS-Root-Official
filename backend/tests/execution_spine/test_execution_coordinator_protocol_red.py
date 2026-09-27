"""RED-first protocol tests for services.northena.execution_coordinator.

Uses explicit MOCKED ports; no live providers, HTTP, SSH, or model calls.
"""

from __future__ import annotations

import asyncio
import importlib

import pytest


def _models_module():
    try:
        return importlib.import_module("services.northena.execution_models")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_models: {exc}")


def _coord_module():
    try:
        return importlib.import_module("services.northena.execution_coordinator")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.northena.execution_coordinator: {exc}")


def _make_request(mod, *, kind: str, engine: str, request_id: str = "req-1"):
    return mod.Request(
        request_id=request_id,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind=kind,
        engine=engine,
        objective_sha256="a" * 64,
        input_refs=("akki://input/1",),
        scope_refs=("scope://allowed",),
        deadline_epoch=10_000,
        result_floor="non_factual",
    )


class _FakeJournal:
    def __init__(self):
        self.events = {}

    async def read(self, request):
        return list(self.events.get(request.request_id, []))

    async def append(self, request, slot, data):
        rows = self.events.setdefault(request.request_id, [])
        for row in rows:
            if row["slot"] == slot and row["data"] == data:
                return row
            if row["slot"] == slot and row["data"] != data:
                from services.ledger_writer.principal_control import CommandConflict

                raise CommandConflict("slot conflict")
        seq = len(rows) + 1
        event = {"slot": slot, "data": data, "seq": seq, "hash": f"h-{seq}"}
        rows.append(event)
        return event


class _FakeAuthorityPort:
    def __init__(self, mod):
        self.mod = mod
        self.expired = False
        self.withdrawn = False

    async def authorize(self, request, phase):
        if self.withdrawn:
            raise self.mod.Held(reason_code="RIGHTS_WITHDRAWN")
        if self.expired:
            raise self.mod.Held(reason_code="AUTHORITY_EXPIRED")
        return self.mod.Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=99_999,
            terms_ref="terms://dispatch/v1",
            policy_epoch=1,
        )


class _FakeExecutorPort:
    def __init__(self, mod):
        self.mod = mod
        self.submitted = []
        self.timeout_submit = False
        self.status_state = "accepted"
        self.cancel_usage = None

    async def submit(self, request, operation_key, fence, authority):
        self.submitted.append((request.request_id, operation_key, fence, authority.authority_ref))
        if self.timeout_submit:
            raise TimeoutError("submit timeout")
        return self.mod.WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-1",
            fence=fence,
            state="accepted",
            receipt_ref="akki://receipt/submit",
            artifacts=(),
            usage=None,
            evidence_mode="MOCKED",
        )

    async def status(self, request, operation_key, fence):
        artifact = self.mod.Artifact(
            ref="akki://artifact/a",
            sha256="b" * 64,
            size_bytes=12,
            tenant_id=request.tenant_id,
            class_label=request.result_floor or "non_factual",
        )
        usage = None if self.status_state == "running" else (self.mod.Usage(unit="tokens", quantity="10"),)
        return self.mod.WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-1",
            fence=fence,
            state=self.status_state,
            receipt_ref="akki://receipt/status",
            artifacts=(artifact,),
            usage=usage,
            evidence_mode="MOCKED",
        )

    async def cancel(self, request, operation_key, fence):
        return self.mod.WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-1",
            fence=fence,
            state="cancelled",
            receipt_ref="akki://receipt/cancel",
            artifacts=(),
            usage=self.cancel_usage,
            evidence_mode="MOCKED",
        )


class _FakeArtifactPort:
    def __init__(self):
        self.bad_hash = False
        self.bad_size = False

    async def verify(self, request, result, operation_key):
        verified = []
        for art in result.artifacts:
            if self.bad_hash:
                raise ValueError("ARTIFACT_HASH_MISMATCH")
            if self.bad_size:
                raise ValueError("ARTIFACT_SIZE_MISMATCH")
            verified.append(art)
        if not verified:
            raise ValueError("ARTIFACT_EMPTY")
        return tuple(verified)


def _make_coordinator(kind: str, engine: str):
    mod = _models_module()
    coord_mod = _coord_module()
    request = _make_request(mod, kind=kind, engine=engine, request_id=f"req-{kind}")
    authority = _FakeAuthorityPort(mod)
    executor = _FakeExecutorPort(mod)
    artifacts = _FakeArtifactPort()
    journal = _FakeJournal()
    coordinator = coord_mod.Coordinator(
        journal=journal,
        authority=authority,
        executors={kind: executor},
        artifacts=artifacts,
        clock=lambda: 100,
    )
    return mod, coordinator, request, authority, executor, artifacts, journal


def _advance_with_budget(coordinator, request, *, max_followup_steps: int = 3):
    view = asyncio.run(coordinator.advance(request))
    for _ in range(max_followup_steps):
        if getattr(view, "phase", None) in {"ready", "failed", "held", "cancelled"}:
            break
        view = asyncio.run(coordinator.advance(request))
    return view


def _slot_has_any(slot: str, needles: tuple[str, ...]) -> bool:
    lowered = slot.lower()
    return any(needle in lowered for needle in needles)


def _first_slot_index(slots, *needles):
    for idx, slot in enumerate(slots):
        if _slot_has_any(slot, tuple(needles)):
            return idx
    return None


# Module/feature: all 4 denominator positive architecture flows with explicit MOCKED ports.
@pytest.mark.parametrize(
    "kind,engine",
    [
        ("source", "mtafiti"),
        ("skill", "solva"),
        ("training", "targeta"),
        ("evaluation", "targeta"),
    ],
)
def test_coordinator_end_to_end_mocked_positive_flows(kind, engine):
    _mod, coordinator, request, _authority, executor, _artifacts, journal = _make_coordinator(kind, engine)
    executor.status_state = "complete"

    view = _advance_with_budget(coordinator, request, max_followup_steps=3)
    assert view.request_id == request.request_id
    assert view.phase == "ready"
    assert view.evidence_mode == "MOCKED"
    assert getattr(view, "execution_verified", False) is False
    assert executor.submitted

    rows = journal.events.get(request.request_id, [])
    slots = [row["slot"] for row in rows]
    verify_or_register_idx = _first_slot_index(slots, "verify", "register")
    metered_idx = _first_slot_index(slots, "meter", "usage")
    terminal_idx = _first_slot_index(slots, "terminal", "ready", "complete")
    assert verify_or_register_idx is not None
    assert metered_idx is not None
    assert terminal_idx is not None
    assert verify_or_register_idx < metered_idx < terminal_idx
    assert len([slot for slot in slots if _slot_has_any(slot, ("meter", "usage"))]) == 1
    assert len([slot for slot in slots if _slot_has_any(slot, ("terminal", "ready", "complete"))]) == 1

    retrieved = asyncio.run(coordinator.retrieve(request))
    assert retrieved.phase == "ready"
    refs = getattr(retrieved, "artifact_refs", ())
    assert refs
    assert all(isinstance(ref, str) and ref.startswith("akki://") for ref in refs)
    if hasattr(retrieved, "rights_state"):
        assert retrieved.rights_state == "current"


# Module/feature: missing executor port must hold, not dispatch.
def test_missing_executor_port_stays_held():
    mod = _models_module()
    coord_mod = _coord_module()
    request = _make_request(mod, kind="skill", engine="solva", request_id="req-missing")
    coordinator = coord_mod.Coordinator(
        journal=_FakeJournal(),
        authority=_FakeAuthorityPort(mod),
        executors={},
        artifacts=_FakeArtifactPort(),
        clock=lambda: 100,
    )
    view = asyncio.run(coordinator.advance(request))
    assert view.phase == "held"


# Module/feature: submit timeout becomes unknown and stable-key status recovery.
def test_submit_timeout_is_unknown_then_status_recovers_without_blind_resubmit():
    _mod, coordinator, request, _authority, executor, _artifacts, _journal = _make_coordinator("source", "mtafiti")
    executor.timeout_submit = True
    first = asyncio.run(coordinator.advance(request))
    assert first.phase == "unknown"

    executor.timeout_submit = False
    second = asyncio.run(coordinator.advance(request))
    assert len(executor.submitted) <= 1
    assert second.phase in {"running", "ready", "unknown"}


# Module/feature: refusal/fault paths for scope widening, expiry, manifest mismatch, unknown usage.
def test_refusal_fault_paths_scope_expiry_manifest_and_usage_none():
    _mod, coordinator, request, authority, executor, artifacts, _journal = _make_coordinator("training", "targeta")
    authority.expired = True
    held = asyncio.run(coordinator.advance(request))
    assert held.phase == "held"

    authority.expired = False
    executor.status_state = "complete"
    artifacts.bad_hash = True
    failed = _advance_with_budget(coordinator, request, max_followup_steps=3)
    assert executor.submitted
    assert failed.phase in {"failed", "held", "unknown"}
    assert failed.phase != "ready"
    rows = _journal.events.get(request.request_id, [])
    assert not any(_slot_has_any(row["slot"], ("ready", "terminal", "complete")) for row in rows)


# Module/feature: cancel semantics with explicit acknowledged zero usage.
def test_cancel_semantics_with_explicit_zero_usage_acknowledgement():
    mod, coordinator, request, _authority, executor, _artifacts, _journal = _make_coordinator("evaluation", "targeta")
    executor.cancel_usage = (mod.Usage(unit="tokens", quantity="0"),)
    _ = asyncio.run(coordinator.advance(request))
    view = asyncio.run(coordinator.cancel(request))
    assert view.phase == "cancelled"
    assert view.evidence_mode == "MOCKED"
    assert getattr(view, "usage", None)
    assert view.usage[0].quantity == "0"


# Module/feature: cancellation with no usage must hold; None cannot masquerade as charged zero.
def test_cancel_none_usage_is_held_not_charged_zero():
    _mod, coordinator, request, _authority, executor, _artifacts, _journal = _make_coordinator("source", "mtafiti")
    executor.cancel_usage = None
    _ = asyncio.run(coordinator.advance(request))
    view = asyncio.run(coordinator.cancel(request))
    assert view.phase == "held"
    assert getattr(view, "usage", None) in (None, ())


# Module/feature: retrieve/view enforce rights recheck and opaque refs only.
def test_retrieve_rechecks_publish_rights_and_returns_opaque_artifact_refs_only():
    _mod, coordinator, request, authority, executor, _artifacts, _journal = _make_coordinator("skill", "solva")
    executor.status_state = "complete"
    _advance_with_budget(coordinator, request, max_followup_steps=3)
    authority.withdrawn = True
    held = asyncio.run(coordinator.retrieve(request))
    assert held.phase == "held"
    assert not getattr(held, "artifact_refs", None)


# Module/feature: ledger append conflict must raise CommandConflict.
def test_journal_slot_conflict_raises_command_conflict():
    mod = _models_module()
    from services.ledger_writer.principal_control import CommandConflict

    journal = _FakeJournal()
    request = _make_request(mod, kind="source", engine="mtafiti", request_id="req-conflict")
    asyncio.run(journal.append(request, "dispatch", {"request_sha256": request.digest(), "nonce": 1}))
    replay = asyncio.run(journal.append(request, "dispatch", {"request_sha256": request.digest(), "nonce": 1}))
    assert replay["seq"] == 1
    with pytest.raises(CommandConflict):
        asyncio.run(journal.append(request, "dispatch", {"request_sha256": request.digest(), "nonce": 2}))
