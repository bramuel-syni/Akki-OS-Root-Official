"""RED-first acceptance contract for W1 control-record scope/guarded writer slice.

This suite intentionally encodes expected behavior before production implementation.
Absence of new modules/services is expected in RED.
"""

from __future__ import annotations

import asyncio
import copy
import hashlib
import inspect
from contextvars import copy_context
from dataclasses import asdict
from importlib import import_module
from pathlib import Path

import pytest

from contracts.ledger_v1 import LedgerRow, LedgerRowAt, GENESIS_PREV_HASH
from services.enforce.principal_context_adapter import principal_context
from services.ledger_emitter.emit_intent import emit_control_intent
from services.ledger_verifier.verify import verify_chain
from services.ledger_writer.main import append_intent, compute_row_hash
from services.ledger_writer.mongo_control import COLLECTION, digest, read_events as raw_read_events
from services.northena import portal_work
from services.portal_operational import entitlements, skill_query


RUNTIME_ROOT = Path("/app/backend/vendored/extraction_akki/backend")

# Module/feature: freeze the four denominator members before autonomous changes.
EXPECTED_MEMBER_SOURCE_SHA256 = {
    "services.northena.portal_work.submit": "de13c14d37717e1f6d7a402977faacda9c5fc6d1776b655bfe26207592fd63b2",
    "services.portal_operational.skill_query.refuse_unadmitted": "b6cde6fa2c284760fedd18d5197d2f43a78a0682ea021346744a7bc96775120c",
    "services.northena.portal_work.events_for": "15b85145940961c4db5bb422c026059938c9bd3a765a95db4838dfdf26b7ce94",
    "services.portal_operational.entitlements.read_view": "f20199e3f4b4afbb88775f4348cdf295d2fbe98013c3eefcb3229192e437880d",
}

# Module/feature: sealed modules + prototype assets remain byte-identical.
EXPECTED_FILE_SHA256 = {
    "/app/backend/vendored/extraction_akki/backend/services/request_context/context.py": "ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb",
    "/app/backend/vendored/extraction_akki/backend/services/enforce/principal_context_adapter.py": "16e2f2069cff5ec2c2d686766b3b6bf6fe502c7c2240678b1cf8ec198a5b20ed",
    "/app/backend/vendored/extraction_akki/backend/services/ledger_emitter/emit_intent.py": "5855d3758508e6a1f90324e41a574d55044dcb4351e2f139918dd1e2a27d98cb",
    "/app/backend/vendored/extraction_akki/backend/services/ledger_writer/main.py": "9110d16e3a6a6dc53eb9825c6d3397455932f7f0f65ae724735bd25022bb6b9f",
    "/app/backend/vendored/extraction_akki/backend/services/ledger_writer/mongo_control.py": "f653905cc76a2ba8ed78e3dc5277040db1e325a8eb0e47ed622c2f633b9bd9bd",
    "/app/backend/vendored/extraction_akki/backend/services/ledger_verifier/verify.py": "18d894ada77903435dd9cd50153b89a7d9514fc9a93ca2e2e1ae68b1bc97c0bc",
    "/app/backend/vendored/extraction_akki/backend/contracts/ledger_v1.py": "d2a8f5495ca4b963b6deddb892f13803225b4ba565e62c0197608818f0d6aa9e",
    "/app/assessment_workspace/canon/prototypes/20260925_owner_updated/os.html": "a0a6df580d034cd9eef8efa7ddd130a131b1f97600c181b50002bd30846911b2",
    "/app/assessment_workspace/canon/prototypes/20260925_owner_updated/dap.html": "0d9a9ee2cf39179c04d77545f5fd3f5c46c41e4a24c44dabade0c6f175b1c188",
    "/app/assessment_workspace/canon/prototypes/20260925_owner_updated/intake.json": "cc2f7ad2e2ba967ba41540ab1f46e40f165c149a11cf14682f41a0e1ecfe426e",
}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_path(path: str) -> str:
    return _sha256_bytes(Path(path).read_bytes())


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
    def __init__(self, docs: list[dict] | None = None):
        self.docs = list(docs or [])
        self.insert_called = 0

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
        self.insert_called += 1
        self.docs.append(copy.deepcopy(doc))
        return type("InsertResult", (), {"inserted_id": "fake-id"})()


class _FakeDb(dict):
    pass


def _load_control_scope_module():
    try:
        return import_module("services.enforce.control_scope")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.enforce.control_scope: {exc}")


def _load_principal_control_module():
    try:
        return import_module("services.ledger_writer.principal_control")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing expected RED target module services.ledger_writer.principal_control: {exc}")


def _read(path: str) -> str:
    return (RUNTIME_ROOT / path).read_text(encoding="utf-8")


def _seed_valid_docs(tenant_id: str = "DIGICOW") -> list[dict]:
    payload_1 = {"principal_id": "principal-1", "tenant_id": tenant_id, "step": 1}
    payload_2 = {"principal_id": "principal-1", "tenant_id": tenant_id, "step": 2}

    intent_1 = emit_control_intent(
        tenant_id=tenant_id,
        run_id="run-1",
        actor_id="principal-1",
        event_type="dap.request.commissioned",
        resource_type="dap_request",
        resource_id="run-1",
        decision="held",
        reason_code="ADMISSION_UNRESOLVED",
        payload_ref=digest(payload_1),
        epoch_s=1,
    )
    row_1 = append_intent(intent=intent_1, prev_row=None, tenant_seq_next=1)

    intent_2 = emit_control_intent(
        tenant_id=tenant_id,
        run_id="run-1",
        actor_id="principal-1",
        event_type="dap.request.held",
        resource_type="dap_request",
        resource_id="run-1",
        decision="held",
        reason_code="ADMISSION_UNRESOLVED",
        payload_ref=digest(payload_2),
        epoch_s=2,
    )
    row_2 = append_intent(intent=intent_2, prev_row=row_1, tenant_seq_next=2)

    return [
        {"command_id": "cmd-1", "row": asdict(row_1), "payload": payload_1},
        {"command_id": "cmd-2", "row": asdict(row_2), "payload": payload_2},
    ]


def test_w1_member_source_hashes_are_frozen_before_any_production_change():
    baseline_path = Path(
        "/app/assessment_workspace/notes/consolidated_fix_plan_20260926/"
        "w1_verification/w1_control_member_source_baseline_prechange_20260926.json"
    )
    assert baseline_path.exists(), "Missing immutable pre-change baseline snapshot JSON"

    baseline = __import__("json").loads(baseline_path.read_text(encoding="utf-8"))
    members = baseline.get("members", {})
    expected_members = set(EXPECTED_MEMBER_SOURCE_SHA256.keys())

    # Contract denominator is exactly four explicitly authorized migration targets.
    assert baseline.get("denominator_count") == 4
    assert set(members.keys()) == expected_members

    # Verify banked source bytes/hash evidence is internally consistent and pre-change pins are preserved.
    for member_name in expected_members:
        source = members[member_name]["source"]
        banked_sha = members[member_name]["sha256"]
        assert _sha256_bytes(source.encode("utf-8")) == banked_sha
        assert banked_sha == EXPECTED_MEMBER_SOURCE_SHA256[member_name]


def test_sealed_modules_and_prototype_assets_are_byte_unchanged():
    for path, expected in EXPECTED_FILE_SHA256.items():
        assert _sha256_path(path) == expected


def test_raw_read_events_repro_accepts_broken_prev_link_when_row_hashes_self_validate():
    payload_1 = {"a": 1}
    payload_2 = {"a": 2}

    at_1 = LedgerRowAt(epoch_s=1, source="wall_clock")
    row_1_seed = LedgerRow(
        seq=1,
        prev_hash=GENESIS_PREV_HASH,
        hash="",
        schema_version="v1",
        tenant_id="DIGICOW",
        run_id="run-x",
        task_id="run-x",
        actor_id="principal-1",
        actor_type="principal",
        event_type="one",
        resource_type="dap_request",
        resource_id="run-x",
        decision="held",
        reason_code="A",
        payload_ref=digest(payload_1),
        at=at_1,
        break_glass_session_id=None,
    )
    row_1 = LedgerRow(**{**asdict(row_1_seed), "at": at_1, "hash": compute_row_hash(row_1_seed.prev_hash, row_1_seed)})

    bad_prev = "f" * 64
    at_2 = LedgerRowAt(epoch_s=2, source="wall_clock")
    row_2_seed = LedgerRow(
        seq=2,
        prev_hash=bad_prev,
        hash="",
        schema_version="v1",
        tenant_id="DIGICOW",
        run_id="run-x",
        task_id="run-x",
        actor_id="principal-1",
        actor_type="principal",
        event_type="two",
        resource_type="dap_request",
        resource_id="run-x",
        decision="held",
        reason_code="B",
        payload_ref=digest(payload_2),
        at=at_2,
        break_glass_session_id=None,
    )
    row_2 = LedgerRow(**{**asdict(row_2_seed), "at": at_2, "hash": compute_row_hash(row_2_seed.prev_hash, row_2_seed)})

    receipt = verify_chain(rows_in_seq_order=[row_1, row_2])
    assert receipt.break_at_seq == 2

    coll = _FakeCollection([
        {"command_id": "cmd-1", "row": asdict(row_1), "payload": payload_1},
        {"command_id": "cmd-2", "row": asdict(row_2), "payload": payload_2},
    ])
    db = _FakeDb({COLLECTION: coll})
    rows = asyncio.run(raw_read_events(db, {"row.tenant_id": "DIGICOW"}))
    assert len(rows) == 2


def test_real_emitter_writer_verifier_functions_are_usable_for_contract_rows():
    docs = _seed_valid_docs()
    rows = [LedgerRow(**{**doc["row"], "at": LedgerRowAt(**doc["row"]["at"])}) for doc in docs]
    receipt = verify_chain(rows_in_seq_order=rows)
    assert receipt.break_at_seq is None
    assert receipt.head_seq == 2


def test_producer_and_consumer_imports_are_migrated_to_principal_control_module():
    portal_work_src = _read("services/northena/portal_work.py")
    skill_query_src = _read("services/portal_operational/skill_query.py")
    entitlements_src = _read("services/portal_operational/entitlements.py")

    assert "from services.ledger_writer.principal_control import append_event, read_events" in portal_work_src
    assert "from services.ledger_writer.principal_control import append_event" in skill_query_src
    assert "from services.ledger_writer.principal_control import read_events" in entitlements_src


def test_control_scope_contract_surface_exists_and_returns_frozen_scope_shape():
    mod = _load_control_scope_module()
    assert hasattr(mod, "bind_control_scope")
    assert hasattr(mod, "require_control_scope")

    with principal_context("principal-1"):
        with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            scope = mod.require_control_scope()
            assert scope.principal_id == "principal-1"
            assert scope.tenant_id == "DIGICOW"
            with pytest.raises(Exception):
                scope.principal_id = "principal-2"


def test_control_scope_refuses_absent_malformed_or_substituted_scope_before_writes():
    mod = _load_control_scope_module()
    with pytest.raises(Exception):
        mod.require_control_scope()

    with principal_context("principal-1"):
        with pytest.raises(Exception):
            with mod.bind_control_scope({"principal_id": "", "tenant_id": "DIGICOW"}):
                pass
        with pytest.raises(Exception):
            with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": ""}):
                pass
        with pytest.raises(Exception):
            with mod.bind_control_scope({"principal_id": "principal-2", "tenant_id": "DIGICOW"}):
                pass


def test_control_scope_nested_same_scope_restores_and_changed_actor_or_tenant_refuses():
    mod = _load_control_scope_module()
    with principal_context("principal-1"):
        with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            outer = mod.require_control_scope()
            with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
                inner = mod.require_control_scope()
                assert inner == outer
            restored = mod.require_control_scope()
            assert restored == outer
            with pytest.raises(Exception):
                with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": "RMS"}):
                    pass


def test_control_scope_copied_child_context_refuses_after_outer_exit():
    mod = _load_control_scope_module()

    with principal_context("principal-1"):
        with mod.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            copied = copy_context()

    with pytest.raises(Exception):
        copied.run(mod.require_control_scope)


def test_control_scope_async_concurrency_isolates_distinct_requests():
    mod = _load_control_scope_module()

    async def _worker(principal_id: str, tenant_id: str):
        with principal_context(principal_id):
            with mod.bind_control_scope({"principal_id": principal_id, "tenant_id": tenant_id}):
                await asyncio.sleep(0)
                scope = mod.require_control_scope()
                return scope.principal_id, scope.tenant_id

    async def _run_pair():
        return await asyncio.gather(
            _worker("principal-a", "DIGICOW"),
            _worker("principal-b", "RMS"),
        )

    got = asyncio.run(_run_pair())
    assert set(got) == {("principal-a", "DIGICOW"), ("principal-b", "RMS")}


def test_principal_control_append_signature_reuses_existing_kwargs_except_actor_id():
    mod = _load_principal_control_module()
    sig = inspect.signature(mod.append_event)
    params = list(sig.parameters.keys())
    assert "actor_id" not in params
    assert params == [
        "db", "tenant_id", "run_id", "command_id", "event_type", "resource_type", "decision", "reason_code", "payload"
    ]


def test_principal_control_append_refuses_payload_actor_tenant_mismatch_before_db_access():
    control_scope = _load_control_scope_module()
    principal_control = _load_principal_control_module()
    coll = _FakeCollection(_seed_valid_docs())
    db = _FakeDb({COLLECTION: coll})

    with principal_context("principal-1"):
        with control_scope.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            with pytest.raises(Exception):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-2",
                    command_id="cmd-x",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-2", "tenant_id": "DIGICOW"},
                ))
    assert coll.insert_called == 0


def test_principal_control_append_deep_copies_payload_and_rejects_metadata_id_tamper_conflict():
    control_scope = _load_control_scope_module()
    principal_control = _load_principal_control_module()
    coll = _FakeCollection(_seed_valid_docs())
    db = _FakeDb({COLLECTION: coll})
    payload = {"tenant_id": "DIGICOW", "principal_id": "principal-1", "body_hash": "b1"}

    with principal_context("principal-1"):
        with control_scope.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            first = asyncio.run(principal_control.append_event(
                db,
                tenant_id="DIGICOW",
                run_id="run-9",
                command_id="cmd-same",
                event_type="dap.request.commissioned",
                resource_type="dap_request",
                decision="held",
                reason_code="ADMISSION_UNRESOLVED",
                payload=payload,
            ))
            payload["body_hash"] = "tampered-after-call"
            replay = asyncio.run(principal_control.append_event(
                db,
                tenant_id="DIGICOW",
                run_id="run-9",
                command_id="cmd-same",
                event_type="dap.request.commissioned",
                resource_type="dap_request",
                decision="held",
                reason_code="ADMISSION_UNRESOLVED",
                payload={"tenant_id": "DIGICOW", "principal_id": "principal-1", "body_hash": "b1"},
            ))
            assert replay["row"]["hash"] == first["row"]["hash"]
            with pytest.raises(principal_control.CommandConflict):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-9",
                    command_id="cmd-same",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="DIFFERENT",
                    payload={"tenant_id": "DIGICOW", "principal_id": "principal-1", "body_hash": "b2"},
                ))


def test_guarded_read_events_fail_closed_on_corrupt_prefix_but_supports_legacy_rows_without_command_metadata():
    control_scope = _load_control_scope_module()
    principal_control = _load_principal_control_module()

    docs = _seed_valid_docs()
    # Legacy replay row without _control_command metadata should still be readable.
    docs[0]["payload"].pop("_control_command", None)

    bad = copy.deepcopy(docs[1])
    bad["row"]["prev_hash"] = "0" * 64
    docs.append(bad)
    coll = _FakeCollection(docs)
    db = _FakeDb({COLLECTION: coll})

    with principal_context("principal-1"):
        with control_scope.bind_control_scope({"principal_id": "principal-1", "tenant_id": "DIGICOW"}):
            with pytest.raises(Exception):
                asyncio.run(principal_control.read_events(db, {"row.tenant_id": "DIGICOW"}))
            with pytest.raises(Exception):
                asyncio.run(principal_control.append_event(
                    db,
                    tenant_id="DIGICOW",
                    run_id="run-10",
                    command_id="cmd-new",
                    event_type="dap.request.commissioned",
                    resource_type="dap_request",
                    decision="held",
                    reason_code="ADMISSION_UNRESOLVED",
                    payload={"principal_id": "principal-1", "tenant_id": "DIGICOW"},
                ))
