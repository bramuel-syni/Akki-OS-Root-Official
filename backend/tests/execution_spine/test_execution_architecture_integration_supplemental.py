"""Supplemental architecture integration tests using real Coordinator+LedgerJournal.

Ports for authority/worker/artifact are explicitly MOCKED; canonical ledger kernels are real.
"""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
from pathlib import Path

import pytest
from pymongo.errors import DuplicateKeyError

from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_coordinator import Coordinator
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Artifact, Authority, Held, Request, Usage, WorkerResult


BASELINE_MANIFEST = Path(
    "/app/assessment_workspace/notes/consolidated_fix_plan_20260926/"
    "architecture_verification/execution_spine_baseline_hash_manifest.json"
)


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
        self.withdrawn = False

    async def authorize(self, request, _phase):
        if self.withdrawn:
            raise Held("RIGHTS_WITHDRAWN")
        return Authority(
            authority_ref=f"auth://{request.request_id}",
            request_sha256=request.digest(),
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            scope_refs=request.scope_refs,
            engine=request.engine,
            expires_epoch=9_999_999,
            terms_ref="terms://dispatch/v1",
            policy_epoch=1,
        )


class _ExecutorPort:
    def __init__(self):
        self.submit_calls = 0
        self.cancel_calls = 0
        self.timeout_first_submit = False
        self.cancel_timeout = False
        self.status_state = "complete"

    async def submit(self, request, operation_key, fence, _authority):
        self.submit_calls += 1
        if self.timeout_first_submit and self.submit_calls == 1:
            raise TimeoutError("submit timeout")
        await asyncio.sleep(0.01)
        return WorkerResult(
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
        artifact = Artifact(
            ref="akki://artifact/a",
            sha256="b" * 64,
            size_bytes=3,
            tenant_id=request.tenant_id,
            class_label=request.result_floor or "non_factual",
        )
        usage = (Usage(unit="tokens", quantity="10"),) if self.status_state == "complete" else None
        return WorkerResult(
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
        self.cancel_calls += 1
        if self.cancel_timeout:
            raise TimeoutError("cancel timeout")
        return WorkerResult(
            operation_key=operation_key,
            request_sha256=request.digest(),
            executor_id="exec-1",
            fence=fence,
            state="cancelled",
            receipt_ref="akki://receipt/cancel",
            artifacts=(),
            usage=(Usage(unit="tokens", quantity="1"),),
            evidence_mode="MOCKED",
        )


class _ArtifactPort:
    async def verify(self, _request, result, _operation_key):
        return result.artifacts


def _make_request(request_id: str, *, objective_seed: str = "a"):
    return Request(
        request_id=request_id,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind="source",
        engine="mtafiti",
        objective_sha256=hashlib.sha256(objective_seed.encode("utf-8")).hexdigest(),
        input_refs=("akki://source/rms_mysql",),
        scope_refs=("rms_mysql",),
        deadline_epoch=9_999_999,
    )


def _make_stack(request_id: str):
    db = _FakeDb({"ledger_v1_control_events": _FakeCollection()})
    authority = _AuthorityPort()
    executor = _ExecutorPort()
    coordinator = Coordinator(
        journal=LedgerJournal(db),
        authority=authority,
        executors={"source": executor},
        artifacts=_ArtifactPort(),
        clock=lambda: 100,
    )
    return db, coordinator, authority, executor


async def _with_scope(request: Request, coro):
    with principal_context(request.principal_id):
        with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
            return await coro


# Module/feature: baseline manifest must verify sealed/prototype bytes, not existence only.
def test_baseline_manifest_hashes_match_current_sealed_files_and_prototypes():
    manifest = json.loads(BASELINE_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["hash_algorithm"] == "sha256"
    for path, expected in manifest["sealed_hashes"].items():
        current = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        assert current == expected


# Module/feature: concurrent advances claim one dispatch slot and submit once.
def test_concurrent_advance_submits_once_with_real_ledger_journal():
    _db, coordinator, _authority, executor = _make_stack("req-concurrent")
    request = _make_request("req-concurrent")

    async def _run():
        return await asyncio.gather(
            _with_scope(request, coordinator.advance(request)),
            _with_scope(request, coordinator.advance(request)),
        )

    views = asyncio.run(_run())
    assert len(views) == 2
    assert executor.submit_calls == 1
    assert all(view.phase in {"running", "ready", "unknown"} for view in views)


# Module/feature: timeout replay reconciles stable worker key and avoids blind resubmit.
def test_submit_timeout_replay_reuses_worker_key_without_resubmit():
    _db, coordinator, _authority, executor = _make_stack("req-timeout")
    request = _make_request("req-timeout")
    executor.timeout_first_submit = True

    first = asyncio.run(_with_scope(request, coordinator.advance(request)))
    second = asyncio.run(_with_scope(request, coordinator.advance(request)))

    assert first.phase == "unknown"
    assert second.phase in {"running", "ready", "unknown"}
    assert executor.submit_calls == 1


# Module/feature: identical slot replay is idempotent; changed payload or frozen request hash conflicts.
def test_journal_slot_replay_idempotent_and_changed_payload_or_request_refused():
    db = _FakeDb({"ledger_v1_control_events": _FakeCollection()})
    journal = LedgerJournal(db)
    request = _make_request("req-slot")

    async def _run():
        with principal_context(request.principal_id):
            with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
                first = await journal.append(request, "dispatch", {"operation_key": "same", "action": "submit"})
                replay = await journal.append(request, "dispatch", {"operation_key": "same", "action": "submit"})
                with pytest.raises(CommandConflict):
                    await journal.append(request, "dispatch", {"operation_key": "different", "action": "submit"})
                return first, replay

    first, replay = asyncio.run(_run())
    assert first["seq"] == replay["seq"] == 1

    changed = _make_request("req-slot", objective_seed="changed")

    async def _read_changed():
        with principal_context(changed.principal_id):
            with bind_control_scope({"principal_id": changed.principal_id, "tenant_id": changed.tenant_id}):
                return await journal.read(changed)

    with pytest.raises(CommandConflict):
        asyncio.run(_read_changed())


# Module/feature: cancel winning dispatch slot writes tombstone action and prevents submit.
def test_cancel_before_dispatch_wins_atomic_slot_and_blocks_submit():
    _db, coordinator, _authority, executor = _make_stack("req-cancel-first")
    request = _make_request("req-cancel-first")

    cancelled = asyncio.run(_with_scope(request, coordinator.cancel(request)))
    replay = asyncio.run(_with_scope(request, coordinator.advance(request)))

    assert cancelled.phase == "cancelled"
    assert replay.phase == "cancelled"
    assert executor.submit_calls == 0


# Module/feature: ambiguous cancel acknowledgement remains unknown and does not mint terminal.
def test_cancel_timeout_returns_unknown_without_terminal_slot():
    db, coordinator, _authority, executor = _make_stack("req-cancel-unknown")
    request = _make_request("req-cancel-unknown")
    executor.status_state = "running"
    executor.cancel_timeout = True

    _ = asyncio.run(_with_scope(request, coordinator.advance(request)))
    cancelled = asyncio.run(_with_scope(request, coordinator.cancel(request)))

    assert cancelled.phase == "unknown"

    async def _read_rows():
        with principal_context(request.principal_id):
            with bind_control_scope({"principal_id": request.principal_id, "tenant_id": request.tenant_id}):
                return await coordinator.journal.read(request)

    rows = asyncio.run(_read_rows())
    assert not any(row["slot"] == "terminal" for row in rows)
