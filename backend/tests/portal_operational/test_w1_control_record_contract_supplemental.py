"""Supplemental W1 control-record contract tests for uncovered C01-C12 gaps.

MOCKED DB only. These tests extend (not replace) the RED-first contract suite.
"""

from __future__ import annotations

import asyncio
import copy
from dataclasses import asdict

import pytest

from services.enforce.control_scope import bind_control_scope, require_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_emitter.emit_intent import emit_control_intent
from services.ledger_writer.control_commands import COMMAND_KEY, CommandConflict
from services.ledger_writer.control_integrity import checked_event, load_verified_prefix
from services.ledger_writer.main import append_intent
from services.ledger_writer.mongo_control import COLLECTION, digest
from services.ledger_writer import principal_control


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
    def __init__(self, docs: list[dict] | None = None, *, return_foreign_on_find=False):
        self.docs = list(docs or [])
        self.insert_called = 0
        self.find_one_called = 0
        self.return_foreign_on_find = return_foreign_on_find

    async def create_index(self, *_args, **_kwargs):
        return None

    async def find_one(self, query: dict, projection: dict | None = None, sort=None):
        self.find_one_called += 1
        rows = [row for row in self.docs if _matches(row, query)]
        if not rows:
            return None
        if sort:
            for key, direction in reversed(sort):
                rows = sorted(rows, key=lambda row: _nested_get(row, key), reverse=direction < 0)
        return copy.deepcopy(rows[0])

    def find(self, query: dict, projection: dict | None = None):
        rows = list(self.docs) if self.return_foreign_on_find else [row for row in self.docs if _matches(row, query)]
        return _FakeCursor(rows)

    async def insert_one(self, doc: dict):
        self.insert_called += 1
        self.docs.append(copy.deepcopy(doc))
        return type("InsertResult", (), {"inserted_id": "fake-id"})()


class _FakeDb(dict):
    pass


def _seed_valid_docs(tenant_id: str = "DIGICOW") -> list[dict]:
    payloads = [
        {"principal_id": "principal-1", "tenant_id": tenant_id, "step": 1, "kind": "a"},
        {"principal_id": "principal-1", "tenant_id": tenant_id, "step": 2, "kind": "b"},
    ]
    rows = []
    prev = None
    for idx, payload in enumerate(payloads, start=1):
        intent = emit_control_intent(
            tenant_id=tenant_id,
            run_id="run-1",
            actor_id="principal-1",
            event_type=f"event-{idx}",
            resource_type="dap_request" if idx == 1 else "skill_query",
            resource_id="run-1",
            decision="held",
            reason_code="ADMISSION_UNRESOLVED",
            payload_ref=digest(payload),
            epoch_s=idx,
        )
        row = append_intent(intent=intent, prev_row=prev, tenant_seq_next=idx)
        rows.append({"command_id": f"cmd-{idx}", "row": asdict(row), "payload": payload})
        prev = row
    return rows


# Module/feature: C01 absent scope must refuse before DB access.
def test_append_refuses_without_scope_before_any_db_access():
    coll = _FakeCollection(_seed_valid_docs())
    db = _FakeDb({COLLECTION: coll})
    with pytest.raises(Exception):
        asyncio.run(principal_control.append_event(
            db,
            tenant_id="DIGICOW",
            run_id="run-new",
            command_id="cmd-new",
            event_type="dap.request.commissioned",
            resource_type="dap_request",
            decision="held",
            reason_code="ADMISSION_UNRESOLVED",
            payload={"principal_id": "principal-1", "tenant_id": "DIGICOW"},
        ))
    assert coll.find_one_called == 0
    assert coll.insert_called == 0


# Module/feature: C02 caller actor keyword and payload mismatch refusal.
def test_append_refuses_caller_actor_keyword_and_payload_tenant_mismatch():
    coll = _FakeCollection(_seed_valid_docs())
    db = _FakeDb({COLLECTION: coll})
    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            with pytest.raises(TypeError):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-new",
                    command_id="cmd-new",
                    actor_id="forged",  # forbidden legacy actor argument
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-1", "tenant_id": "DIGICOW"},
                ))
            with pytest.raises(Exception):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-new",
                    command_id="cmd-new-2",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-1", "tenant_id": "OTHER"},
                ))
    assert coll.insert_called == 0


# Module/feature: C03/C04 malformed scope, substitution refusal, cleanup on exception/cancel.
@pytest.mark.parametrize("bad_scope", [None, "not-a-dict", 1, [], {"principal_id": "p1"}, {"tenant_id": "DIGICOW"}])
def test_bind_control_scope_refuses_malformed_scope_inputs(bad_scope):
    with principal_context("principal-1"):
        with pytest.raises(Exception):
            with bind_control_scope(bad_scope):
                pass


def test_scope_refuses_current_principal_substitution_and_restores_after_exception_and_cancel():
    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            with principal_context("principal-2"):
                with pytest.raises(Exception):
                    require_control_scope()

    with principal_context("principal-1"):
        with pytest.raises(RuntimeError):
            with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
                raise RuntimeError("boom")
        with pytest.raises(Exception):
            require_control_scope()

    copied = {}

    async def _worker():
        with principal_context("principal-1"):
            with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
                from contextvars import copy_context
                copied["ctx"] = copy_context()
                await asyncio.sleep(10)

    async def _run_cancel():
        task = asyncio.create_task(_worker())
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(_run_cancel())
    with pytest.raises(Exception):
        copied["ctx"].run(require_control_scope)


# Module/feature: C09 guard recheck at insert boundary.
def test_insert_guard_rechecks_context_immediately_before_raw_insert():
    from services.ledger_writer.control_insert_guard import InsertGuard

    coll = _FakeCollection([])
    db = _FakeDb({COLLECTION: coll})
    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}) as scope:
            guarded = InsertGuard(db, scope)[COLLECTION]
            with principal_context("principal-2"):
                with pytest.raises(Exception):
                    asyncio.run(guarded.insert_one({"row": {}, "payload": {}, "command_id": "x"}))
    assert coll.insert_called == 0


# Module/feature: C07 interleaved resource filtering after full prefix verification.
def test_read_events_filters_interleaved_resource_types_after_prefix_verification():
    coll = _FakeCollection(_seed_valid_docs())
    db = _FakeDb({COLLECTION: coll})

    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            events = asyncio.run(principal_control.read_events(db, {
                "row.tenant_id": "DIGICOW",
                "row.resource_type": {"$in": ["skill_query"]},
                "payload.principal_id": "principal-1",
            }))
    assert len(events) == 1
    assert events[0]["row"]["resource_type"] == "skill_query"


# Module/feature: C08/C09 invalid prefix shapes/chain/tenant/dup commands fail closed.
@pytest.mark.parametrize(
    "mutator",
    [
        lambda docs: docs[0]["row"].update({"seq": 0}),
        lambda docs: docs[0]["row"].update({"schema_version": "v0"}),
        lambda docs: docs[1]["row"].update({"prev_hash": "0" * 64}),
        lambda docs: docs[0]["payload"].update({"tamper": True}),
        lambda docs: docs.append(copy.deepcopy({**docs[0], "command_id": docs[0]["command_id"]})),
    ],
)
def test_load_verified_prefix_rejects_invalid_prefix_variants(mutator):
    docs = _seed_valid_docs()
    mutator(docs)
    coll = _FakeCollection(docs)
    db = _FakeDb({COLLECTION: coll})
    with pytest.raises(Exception):
        asyncio.run(load_verified_prefix(db, "DIGICOW"))


def test_load_verified_prefix_refuses_foreign_tenant_rows_returned_by_db():
    docs = _seed_valid_docs("DIGICOW") + _seed_valid_docs("RMS")
    coll = _FakeCollection(docs, return_foreign_on_find=True)
    db = _FakeDb({COLLECTION: coll})
    with pytest.raises(Exception):
        asyncio.run(load_verified_prefix(db, "DIGICOW"))


# Module/feature: C10 marker tamper and changed-command conflicts.
def test_checked_event_refuses_marker_tamper_and_changed_command_conflicts(monkeypatch):
    coll = _FakeCollection([])
    db = _FakeDb({COLLECTION: coll})

    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            event = asyncio.run(principal_control.append_event(
                db,
                tenant_id="DIGICOW",
                run_id="run-x",
                command_id="cmd-same",
                event_type="dap.request.commissioned",
                resource_type="dap_request",
                decision="held",
                reason_code="ADMISSION_UNRESOLVED",
                payload={"principal_id": "principal-1", "tenant_id": "DIGICOW", "body_hash": "b1"},
            ))

            tampered_id = copy.deepcopy(event)
            tampered_id["payload"][COMMAND_KEY]["id"] = "other-cmd"
            with pytest.raises(Exception):
                checked_event(tampered_id)

            tampered_fp = copy.deepcopy(event)
            tampered_fp["payload"][COMMAND_KEY]["fingerprint"] = "0" * 64
            with pytest.raises(Exception):
                checked_event(tampered_fp)

            with pytest.raises(CommandConflict):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-changed",
                    command_id="cmd-same",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-1", "tenant_id": "DIGICOW", "body_hash": "b2"},
                ))


# Module/feature: C10 historical no-marker rows still replay unchanged.
def test_legacy_rows_without_marker_are_read_untouched():
    docs = _seed_valid_docs()
    docs[0]["payload"].pop(COMMAND_KEY, None)
    coll = _FakeCollection(docs)
    db = _FakeDb({COLLECTION: coll})
    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            events = asyncio.run(principal_control.read_events(db, {"row.tenant_id": "DIGICOW"}))
    assert len(events) == 2
    assert COMMAND_KEY not in events[0]["payload"]


# Module/feature: C11 no acknowledgement when durable prefix check misses inserted row.
def test_append_refuses_when_acknowledged_row_missing_from_verified_prefix(monkeypatch):
    coll = _FakeCollection([])
    db = _FakeDb({COLLECTION: coll})

    real_load = principal_control.load_verified_prefix
    calls = {"count": 0}

    async def _patched_load(db_obj, tenant_id):
        calls["count"] += 1
        if calls["count"] <= 1:
            return await real_load(db_obj, tenant_id)
        return []

    monkeypatch.setattr(principal_control, "load_verified_prefix", _patched_load)

    with principal_context("principal-1"):
        with bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            with pytest.raises(Exception):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-x",
                    command_id="cmd-x",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-1", "tenant_id": "DIGICOW"},
                ))
