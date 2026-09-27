"""Supplemental architecture/fault coverage with real Coordinator+LedgerJournal and isolated fake DB."""

from __future__ import annotations

import asyncio
import copy
import hashlib

import pytest
from pymongo.errors import DuplicateKeyError

from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.northena.execution_coordinator import Coordinator
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Authority, Held, Request, Usage, WorkerResult
from services.northena.execution_validation import authority_for, checked_artifacts, result_for


def _nested_get(doc: dict, key: str):
    value = doc
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return object()
        value = value[part]
    return value


def _matches(doc: dict, query: dict) -> bool:
    for key, expected in query.items():
        actual = _nested_get(doc, key)
        if isinstance(expected, dict) and "$in" in expected:
            if actual not in expected["$in"]:
                return False
        elif actual != expected:
            return False
    return True


class _FakeCursor:
    def __init__(self, docs: list[dict]):
        self.docs = docs

    def sort(self, key: str, direction: int):
        reverse = direction < 0
        self.docs = sorted(self.docs, key=lambda row: _nested_get(row, key), reverse=reverse)
        return self

    async def to_list(self, _limit):
        return [copy.deepcopy(row) for row in self.docs]


class _FakeCollection:
    def __init__(self):
        self.docs: list[dict] = []

    async def create_index(self, *_args, **_kwargs):
        return None

    async def find_one(self, query: dict, projection: dict | None = None, sort=None):
        rows = [row for row in self.docs if _matches(row, query)]
        if not rows:
            return None
        if sort:
            for key, direction in reversed(sort):
                rows = sorted(rows, key=lambda row: _nested_get(row, key), reverse=direction < 0)
        return copy.deepcopy(rows[0])

    def find(self, query: dict, projection: dict | None = None):
        rows = [row for row in self.docs if _matches(row, query)]
        return _FakeCursor(rows)

    async def insert_one(self, doc: dict):
        tenant_id = doc["row"]["tenant_id"]
        seq = doc["row"]["seq"]
        command_id = doc["command_id"]
        for row in self.docs:
            if row["row"]["tenant_id"] == tenant_id and row["row"]["seq"] == seq:
                raise DuplicateKeyError("duplicate tenant sequence")
            if row["row"]["tenant_id"] == tenant_id and row["command_id"] == command_id:
                raise DuplicateKeyError("duplicate command id")
        self.docs.append(copy.deepcopy(doc))
        return type("InsertResult", (), {"inserted_id": "fake-id"})()


class _FakeDb(dict):
    pass


class _AuthorityPort:
    def __init__(self):
        self.withdraw_on_publish = False
        self.withdraw_on_retrieve = False
        self.current_terms_ref = "terms://dispatch/v1"

    async def authorize(self, request, phase):
        if self.withdraw_on_publish and phase == "publish":
            raise Held("RIGHTS_WITHDRAWN")
        if self.withdraw_on_retrieve and phase == "retrieve":
            raise Held("RIGHTS_WITHDRAWN")
        terms_ref = self.current_terms_ref if phase == "dispatch" else "terms://publish/changed"
        return Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=9_999_999,
            terms_ref=terms_ref,
            policy_epoch=1,
        )


class _ExecutorPort:
    def __init__(self, *, evidence_mode="MOCKED"):
        self.submit_calls = 0
        self.status_state = "complete"
        self.evidence_mode = evidence_mode
        self.executor_id = "exec-1"
        self.usage = (Usage(unit="tokens", quantity="10"),)

    async def submit(self, request, operation_key, fence, _authority):
        self.submit_calls += 1
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id=self.executor_id,
            fence=fence,
            state="accepted",
            receipt_ref="akki://receipt/submit",
            artifacts=(),
            usage=None,
            evidence_mode=self.evidence_mode,
        )

    async def status(self, request, operation_key, fence):
        artifact = Artifact(
            ref="akki://artifact/ok",
            sha256="b" * 64,
            size_bytes=5,
            tenant_id=request.tenant_id,
            class_label=request.result_floor or "non_factual",
        )
        usage = self.usage if self.status_state == "complete" else None
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id=self.executor_id,
            fence=fence,
            state=self.status_state,
            receipt_ref="akki://receipt/status",
            artifacts=(artifact,),
            usage=usage,
            evidence_mode=self.evidence_mode,
        )

    async def cancel(self, request, operation_key, fence):
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id=self.executor_id,
            fence=fence,
            state="cancelled",
            receipt_ref="akki://receipt/cancel",
            artifacts=(),
            usage=(Usage(unit="tokens", quantity="1"),),
            evidence_mode=self.evidence_mode,
        )


class _ArtifactPort:
    def __init__(self):
        self.raise_verify = False

    async def verify(self, _request, result, _operation_key):
        if self.raise_verify:
            raise ValueError("verification failed")
        return result.artifacts


class _FailOnceJournal:
    def __init__(self, inner: LedgerJournal, fail_slot: str):
        self.inner = inner
        self.fail_slot = fail_slot
        self.failed = False

    async def read(self, request):
        return await self.inner.read(request)

    async def append(self, request, slot, data):
        should_fail = (
            not self.failed
            and (
                slot == self.fail_slot
                or (self.fail_slot == "observation" and slot.startswith("observation:"))
            )
        )
        if should_fail:
            self.failed = True
            raise RuntimeError(f"injected once: {slot}")
        return await self.inner.append(request, slot, data)


def _make_request(request_id: str, *, kind="source", engine="mtafiti", floor=None):
    return Request(
        request_id=request_id,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind=kind,
        engine=engine,
        objective_sha256=hashlib.sha256(request_id.encode("utf-8")).hexdigest(),
        input_refs=("akki://source/rms_mysql",),
        scope_refs=("rms_mysql",),
        deadline_epoch=9_999_999,
        result_floor=floor,
    )


async def _with_scope(request: Request, coro):
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            return await coro


def _build_stack(request_id: str, *, kind="source", engine="mtafiti", floor=None, evidence_mode="MOCKED"):
    db = _FakeDb({"ledger_v1_control_events": _FakeCollection()})
    request = _make_request(request_id, kind=kind, engine=engine, floor=floor)
    authority = _AuthorityPort()
    executor = _ExecutorPort(evidence_mode=evidence_mode)
    artifacts = _ArtifactPort()
    journal = LedgerJournal(db)
    coordinator = Coordinator(journal=journal, authority=authority, executors={kind: executor}, artifacts=artifacts, clock=lambda: 100)
    return db, request, authority, executor, artifacts, coordinator


def _rows(coordinator: Coordinator, request: Request):
    return asyncio.run(_with_scope(request, coordinator.journal.read(request)))


def _slot_count(rows: list[dict], slot_prefix: str) -> int:
    return len([row for row in rows if row["slot"] == slot_prefix or row["slot"].startswith(slot_prefix + ":")])


# Module/feature: real LedgerJournal+canonical writer over all denominator kinds remains architecture-only (MOCKED evidence).
@pytest.mark.parametrize(
    "kind,engine,floor",
    [
        ("source", "mtafiti", None),
        ("skill", "solva", "non_factual"),
        ("training", "targeta", None),
        ("evaluation", "targeta", None),
    ],
)
def test_real_ledger_parameterized_four_kind_traces_are_architecture_only(kind, engine, floor):
    _db, request, _authority, _executor, _artifacts, coordinator = _build_stack(
        f"req-{kind}-real-ledger", kind=kind, engine=engine, floor=floor
    )
    view = asyncio.run(_with_scope(request, coordinator.advance(request)))
    assert view.phase == "ready"
    assert view.evidence_mode == "MOCKED"
    assert view.execution_verified is False
    rows = _rows(coordinator, request)
    assert any(row["slot"].startswith("verify_artifact") for row in rows)
    assert any(row["slot"] == "metered" for row in rows)
    assert any(row["slot"] == "terminal" for row in rows)


# Module/feature: fail-once at observation/verify/metered/terminal recovers via new Coordinator on same ledger without resubmit/duplicate usage.
@pytest.mark.parametrize("fail_slot", ["observation", "verify_artifact", "metered", "terminal"])
def test_fail_once_stages_recover_on_new_coordinator_without_duplicate_submit_or_usage(fail_slot):
    db, request, authority, executor, artifacts, coordinator = _build_stack("req-fail-once", evidence_mode="MOCKED")
    failing = Coordinator(
        journal=_FailOnceJournal(LedgerJournal(db), fail_slot),
        authority=authority,
        executors={request.kind: executor},
        artifacts=artifacts,
        clock=lambda: 100,
    )

    with pytest.raises(RuntimeError):
        asyncio.run(_with_scope(request, failing.advance(request)))

    rows_after_fail = _rows(coordinator, request)
    assert not any(row["slot"] == "terminal" and row["data"].get("phase") == "ready" for row in rows_after_fail)

    recovered = Coordinator(
        journal=LedgerJournal(db),
        authority=authority,
        executors={request.kind: executor},
        artifacts=artifacts,
        clock=lambda: 100,
    )
    view = asyncio.run(_with_scope(request, recovered.advance(request)))
    assert view.phase == "ready"
    assert executor.submit_calls == 1
    rows = _rows(recovered, request)
    assert _slot_count(rows, "metered") == 1
    assert _slot_count(rows, "terminal") == 1


# Module/feature: publish-time authority terms changes cannot reprice already metered usage.
def test_publish_terms_change_does_not_reprice_metered_terms_snapshot():
    _db, request, authority, _executor, _artifacts, coordinator = _build_stack("req-terms-frozen")
    authority.current_terms_ref = "terms://dispatch/frozen"
    view = asyncio.run(_with_scope(request, coordinator.advance(request)))
    assert view.phase == "ready"
    assert view.terms_ref == "terms://dispatch/frozen"


# Module/feature: consumed work is metered before hold when verify/publish fails.
def test_verify_or_publish_failure_still_records_actual_usage_then_holds():
    _db, request, authority, _executor, artifacts, coordinator = _build_stack("req-usage-hold")
    artifacts.raise_verify = True
    held = asyncio.run(_with_scope(request, coordinator.advance(request)))
    assert held.phase == "held"
    rows = _rows(coordinator, request)
    assert any(row["slot"] == "metered" for row in rows)

    _db2, request2, authority2, _executor2, _artifacts2, coordinator2 = _build_stack("req-publish-hold")
    authority2.withdraw_on_publish = True
    held_publish = asyncio.run(_with_scope(request2, coordinator2.advance(request2)))
    assert held_publish.phase == "held"
    rows2 = _rows(coordinator2, request2)
    assert any(row["slot"] == "metered" for row in rows2)


# Module/feature: immutable authority/worker/artifact binding mismatches are refused.
def test_authority_and_worker_binding_mismatch_refusals():
    request = _make_request("req-binding")
    good_authority = Authority(
        authority_ref="auth://req-binding",
        request_sha256=request.digest(),
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        scope_refs=request.scope_refs,
        engine=request.engine,
        expires_epoch=500,
        terms_ref="terms://dispatch/v1",
        policy_epoch=1,
    )

    with pytest.raises(Held):
        authority_for(request, good_authority.model_copy(update={"engine": "targeta"}), 100, "dispatch")
    with pytest.raises(Held):
        authority_for(request, good_authority.model_copy(update={"expires_epoch": 50}), 100, "dispatch")

    dispatch = {"data": {"operation_key": "op-1"}, "seq": 1}
    result = WorkerResult(
        operation_key="op-1",
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/ok",
        artifacts=(Artifact(ref="akki://artifact/a", sha256="c" * 64, size_bytes=1, tenant_id=request.tenant_id, class_label="non_factual"),),
        usage=(Usage(unit="tokens", quantity="1"),),
        evidence_mode="MOCKED",
    )
    with pytest.raises(Held):
        result_for(request, result.model_copy(update={"operation_key": "wrong"}), dispatch)
    with pytest.raises(Held):
        result_for(request, result.model_copy(update={"fence": 2}), dispatch)
    with pytest.raises(Held):
        result_for(request, result.model_copy(update={"request_sha256": "d" * 64}), dispatch)
    with pytest.raises(Held):
        bad_tenant_art = result.model_copy(
            update={"artifacts": (Artifact(ref="akki://artifact/a", sha256="c" * 64, size_bytes=1, tenant_id="FOREIGN", class_label="non_factual"),)}
        )
        result_for(request, bad_tenant_art, dispatch)


# Module/feature: artifact verification forbids empty/missing/extra and floor regressions.
def test_artifact_verify_strictness_for_empty_extra_and_floor_regression():
    request = _make_request("req-floor", kind="skill", engine="solva", floor="fact")
    good = Artifact(ref="akki://artifact/a", sha256="e" * 64, size_bytes=2, tenant_id=request.tenant_id, class_label="fact")
    lower = Artifact(ref="akki://artifact/b", sha256="f" * 64, size_bytes=2, tenant_id=request.tenant_id, class_label="non_factual")
    result = WorkerResult(
        operation_key="op",
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(good,),
        usage=(Usage(unit="tokens", quantity="1"),),
        evidence_mode="MOCKED",
    )
    with pytest.raises(Held):
        checked_artifacts(request, result, ())
    with pytest.raises(Held):
        checked_artifacts(request, result, (good, lower))
    with pytest.raises(Held):
        checked_artifacts(request, result.model_copy(update={"artifacts": (lower,)}), (lower,))


# Module/feature: instance revalidation blocks model_construct/model_copy bypass for Authority/WorkerResult/Artifact.
def test_instance_revalidation_blocks_model_construct_bypass():
    request = _make_request("req-revalidate")
    forged_authority = Authority.model_construct(
        authority_ref="auth://x",
        request_sha256=request.digest(),
        tenant_id=request.tenant_id,
        principal_id=request.principal_id,
        scope_refs=request.scope_refs,
        engine="invalid-engine",
        expires_epoch=999,
        terms_ref="terms://x",
        policy_epoch=1,
    )
    with pytest.raises(Held):
        authority_for(request, forged_authority, 1, "dispatch")

    forged_result = WorkerResult.model_construct(
        operation_key="op",
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(),
        usage=None,
        evidence_mode="FORGED",
    )
    with pytest.raises(Held):
        result_for(request, forged_result, {"data": {"operation_key": "op"}, "seq": 1})

    forged_artifact = Artifact.model_construct(
        ref="akki://artifact/x",
        sha256="short",
        size_bytes=1,
        tenant_id=request.tenant_id,
        class_label="fact",
    )
    valid_result = WorkerResult(
        operation_key="op",
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=1,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(forged_artifact,),
        usage=(Usage(unit="tokens", quantity="1"),),
        evidence_mode="MOCKED",
    )
    with pytest.raises(Held):
        checked_artifacts(request, valid_result, valid_result.artifacts)


# Module/feature: retrieval rights withdrawal returns held with no artifact refs.
def test_retrieve_rights_withdrawal_returns_held_without_refs():
    _db, request, authority, _executor, _artifacts, coordinator = _build_stack("req-retrieve-hold")
    ready = asyncio.run(_with_scope(request, coordinator.advance(request)))
    assert ready.phase == "ready"
    authority.withdraw_on_retrieve = True
    held = asyncio.run(_with_scope(request, coordinator.retrieve(request)))
    assert held.phase == "held"
    assert held.artifact_refs == ()


# Module/feature: cancel/dispatch and complete/cancel interleavings cannot mint multiple terminal states.
def test_cancel_dispatch_and_complete_cancel_interleavings_keep_single_terminal_state():
    _db, request, _authority, executor, _artifacts, coordinator = _build_stack("req-race")

    async def _run_race_one():
        return await asyncio.gather(
            _with_scope(request, coordinator.cancel(request)),
            _with_scope(request, coordinator.advance(request)),
        )

    asyncio.run(_run_race_one())
    rows = _rows(coordinator, request)
    assert _slot_count(rows, "terminal") <= 1

    _db2, request2, _authority2, executor2, _artifacts2, coordinator2 = _build_stack("req-race-2")
    _ = asyncio.run(_with_scope(request2, coordinator2.advance(request2)))

    async def _run_race_two():
        return await asyncio.gather(
            _with_scope(request2, coordinator2.cancel(request2)),
            _with_scope(request2, coordinator2.advance(request2)),
        )

    asyncio.run(_run_race_two())
    rows2 = _rows(coordinator2, request2)
    assert _slot_count(rows2, "terminal") == 1
    assert executor.submit_calls <= 1
    assert executor2.submit_calls <= 1
