"""Expanded live contracts for portal operational durability/concurrency/refusal semantics."""

import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import requests
from pymongo import MongoClient

from services.ledger_writer.mongo_control import digest
from services.ledger_writer.main import compute_row_hash
from contracts.ledger_v1 import LedgerRow, LedgerRowAt


def _env_value(path: str, key: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _resolve_base_url() -> str:
    return (os.environ.get("REACT_APP_BACKEND_URL") or _env_value("/app/frontend/.env", "REACT_APP_BACKEND_URL")).strip().rstrip("/")


def _resolve_mongo() -> tuple[str, str]:
    mongo_url = (os.environ.get("MONGO_URL") or _env_value("/app/backend/.env", "MONGO_URL")).strip().strip('"')
    db_name = (os.environ.get("DB_NAME") or _env_value("/app/backend/.env", "DB_NAME")).strip().strip('"')
    return mongo_url, db_name


BASE_URL = _resolve_base_url()
OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PASSWORD = "demo-analyst-pw"


def _require_base_url() -> None:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")


def _login(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert isinstance(token, str) and token
    return token


@pytest.fixture(scope="session")
def operator_headers() -> dict:
    _require_base_url()
    token = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def analyst_headers() -> dict:
    _require_base_url()
    token = _login(ANALYST_EMAIL, ANALYST_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def mongo_collection():
    mongo_url, db_name = _resolve_mongo()
    if not mongo_url or not db_name:
        pytest.skip("MONGO_URL/DB_NAME unavailable for ledger verification")
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
    coll = client[db_name]["ledger_v1_control_events"]
    yield coll
    client.close()


def _submit_payload(idem: str, *, objective="Expanded contract verification", operation="processed_intelligence", units=None) -> dict:
    return {
        "objective_text": objective,
        "operation": operation,
        "units": units or ["rms_mysql"],
        "idempotency_key": idem,
    }


def _submit(headers: dict, payload: dict):
    return requests.post(f"{BASE_URL}/api/portal/requests", headers=headers, json=payload, timeout=20)


def _scope(headers: dict) -> str:
    listing = requests.get(f"{BASE_URL}/api/portal/requests", headers=headers, timeout=20)
    assert listing.status_code == 200
    principal_id = listing.json().get("principal_id")
    assert isinstance(principal_id, str) and principal_id
    return principal_id


# Module/feature: concurrent same-key replay must converge to one request/event identity
def test_concurrent_same_key_replay_returns_single_request_and_command_record(operator_headers, mongo_collection):
    _require_base_url()
    idem = f"exp-same-key-{uuid.uuid4().hex}"
    payload = _submit_payload(idem, objective="Concurrent same-key replay")

    with ThreadPoolExecutor(max_workers=2) as pool:
        first, second = list(pool.map(lambda _: _submit(operator_headers, payload), [1, 2]))

    assert first.status_code == 202
    assert second.status_code == 202
    request_ids = {first.json().get("request_id"), second.json().get("request_id")}
    assert len(request_ids) == 1
    request_id = next(iter(request_ids))
    assert isinstance(request_id, str) and request_id

    principal_id = _scope(operator_headers)
    row_doc = mongo_collection.find_one({"row.run_id": request_id}, {"_id": 0, "row.tenant_id": 1})
    assert isinstance(row_doc, dict)
    tenant_id = row_doc["row"]["tenant_id"]
    command_id = digest([tenant_id, principal_id, idem])
    docs = list(mongo_collection.find({"row.tenant_id": tenant_id, "row.run_id": request_id, "command_id": command_id}, {"_id": 0}))
    assert len(docs) == 1


# Module/feature: same idempotency key with changed body/operation/units must conflict
def test_same_key_changed_operation_or_units_conflicts(operator_headers):
    _require_base_url()
    idem = f"exp-collision-{uuid.uuid4().hex}"
    base = _submit_payload(idem, objective="Collision base")
    created = _submit(operator_headers, base)
    assert created.status_code == 202

    changed_operation = _submit(operator_headers, _submit_payload(idem, objective="Collision base", operation="download_raw_data"))
    assert changed_operation.status_code == 409

    changed_units = _submit(operator_headers, _submit_payload(idem, objective="Collision base", units=["rms_postgres"]))
    assert changed_units.status_code in (403, 409)


# Module/feature: different-key concurrent submissions should not fork tenant sequence
def test_different_key_concurrent_submits_keep_single_sequence_without_fork(operator_headers, mongo_collection):
    _require_base_url()
    payloads = [_submit_payload(f"exp-seq-{uuid.uuid4().hex}", objective=f"Tenant sequence {i}") for i in range(5)]

    with ThreadPoolExecutor(max_workers=5) as pool:
        responses = list(pool.map(lambda body: _submit(operator_headers, body), payloads))

    assert all(r.status_code == 202 for r in responses)
    request_ids = [r.json().get("request_id") for r in responses]
    assert len([r for r in request_ids if isinstance(r, str) and r]) == 5
    assert len(set(request_ids)) == 5

    docs = list(mongo_collection.find({"row.run_id": {"$in": request_ids}, "row.resource_type": "dap_request"}, {"_id": 0}))
    assert len(docs) == 5
    seqs = [doc["row"]["seq"] for doc in docs]
    assert len(seqs) == len(set(seqs))


# Module/feature: immutable 17-field row hashes + payload digest integrity
def test_ledger_row_hash_and_payload_digest_are_valid_for_request(operator_headers, mongo_collection):
    _require_base_url()
    idem = f"exp-integrity-{uuid.uuid4().hex}"
    payload = _submit_payload(idem, objective="Ledger integrity check")
    created = _submit(operator_headers, payload)
    assert created.status_code == 202
    request_id = created.json()["request_id"]

    doc = mongo_collection.find_one({"row.run_id": request_id, "row.resource_type": "dap_request"}, {"_id": 0})
    assert isinstance(doc, dict)

    row = doc["row"]
    assert len(row.keys()) == 17
    assert tuple(row.keys()) == (
        "seq", "prev_hash", "hash", "schema_version", "tenant_id", "run_id", "task_id", "actor_id", "actor_type",
        "event_type", "resource_type", "resource_id", "decision", "reason_code", "payload_ref", "at", "break_glass_session_id",
    )
    assert row["payload_ref"] == digest(doc["payload"])

    row_struct = LedgerRow(
        seq=row["seq"], prev_hash=row["prev_hash"], hash=row["hash"], schema_version=row["schema_version"],
        tenant_id=row["tenant_id"], run_id=row["run_id"], task_id=row["task_id"], actor_id=row["actor_id"],
        actor_type=row["actor_type"], event_type=row["event_type"], resource_type=row["resource_type"],
        resource_id=row["resource_id"], decision=row["decision"], reason_code=row["reason_code"], payload_ref=row["payload_ref"],
        at=LedgerRowAt(**row["at"]), break_glass_session_id=row.get("break_glass_session_id"),
    )
    assert compute_row_hash(row_struct.prev_hash, row_struct) == row_struct.hash


# Module/feature: persistence visible after fresh client; list/detail parity across DAP and OS
def test_fresh_client_sees_same_persisted_record_in_portal_and_os(operator_headers):
    _require_base_url()
    idem = f"exp-refresh-{uuid.uuid4().hex}"
    created = _submit(operator_headers, _submit_payload(idem, objective="Fresh client persistence"))
    assert created.status_code == 202
    data = created.json()
    request_id = data["request_id"]

    fresh = requests.Session()
    fresh.headers.update(operator_headers)
    dap_list = fresh.get(f"{BASE_URL}/api/portal/requests", timeout=20)
    assert dap_list.status_code == 200
    dap_row = next((r for r in dap_list.json()["rows"] if r["request_id"] == request_id), None)
    assert dap_row is not None

    dap_detail = fresh.get(f"{BASE_URL}/api/portal/requests/{request_id}", timeout=20)
    assert dap_detail.status_code == 200
    os_list = fresh.get(f"{BASE_URL}/api/os/work", timeout=20)
    assert os_list.status_code == 200
    os_row = next((r for r in os_list.json()["rows"] if r["work_id"] == request_id), None)
    assert os_row is not None

    os_detail = fresh.get(f"{BASE_URL}/api/os/work/{request_id}", timeout=20)
    assert os_detail.status_code == 200
    assert dap_detail.json()["objective_hash"] == os_detail.json()["objective_hash"]


# Module/feature: role and principal isolation for submit/list/detail/actions
def test_analyst_submit_forbidden_and_cross_principal_not_exposed(operator_headers, analyst_headers):
    _require_base_url()
    created = _submit(operator_headers, _submit_payload(f"exp-principal-{uuid.uuid4().hex}", objective="Principal isolation"))
    assert created.status_code == 202
    request_id = created.json()["request_id"]

    analyst_submit = _submit(analyst_headers, _submit_payload(f"exp-analyst-{uuid.uuid4().hex}", objective="Analyst write deny"))
    assert analyst_submit.status_code == 403

    analyst_list = requests.get(f"{BASE_URL}/api/portal/requests", headers=analyst_headers, timeout=20)
    assert analyst_list.status_code == 200
    assert all(row.get("request_id") != request_id for row in analyst_list.json().get("rows", []))

    analyst_detail = requests.get(f"{BASE_URL}/api/portal/requests/{request_id}", headers=analyst_headers, timeout=20)
    assert analyst_detail.status_code in (403, 404)


# Module/feature: forged fields and bounds/whitespace validation
def test_forged_fields_and_whitespace_bounds_are_rejected(operator_headers):
    _require_base_url()
    forged = _submit_payload(f"exp-forged-{uuid.uuid4().hex}")
    forged.update({"principal_id": "forged", "tenant_id": "forged", "approver_id": "forged", "answer_stub": "x", "class_label": "x"})
    assert _submit(operator_headers, forged).status_code == 422

    blank_obj = _submit_payload(f"exp-blank-{uuid.uuid4().hex}", objective="   ")
    assert _submit(operator_headers, blank_obj).status_code == 422

    short_key = _submit_payload("short", objective="Too short idempotency key")
    assert _submit(operator_headers, short_key).status_code == 422

    too_many_units = _submit_payload(f"exp-many-{uuid.uuid4().hex}", units=[f"u{i}" for i in range(51)])
    assert _submit(operator_headers, too_many_units).status_code == 422


# Module/feature: unknown and routing-state actions must fail closed
def test_unknown_request_actions_404_and_routing_actions_409(operator_headers):
    _require_base_url()
    unknown = f"req-missing-{uuid.uuid4().hex}"
    for path in [f"/api/portal/requests/{unknown}/stop", f"/api/portal/requests/{unknown}/retry", f"/api/portal/requests/{unknown}/result"]:
        response = requests.post(f"{BASE_URL}{path}", headers=operator_headers, json={}, timeout=20) if path.endswith(("stop", "retry")) else requests.get(f"{BASE_URL}{path}", headers=operator_headers, timeout=20)
        assert response.status_code == 404

    created = _submit(operator_headers, _submit_payload(f"exp-routing-{uuid.uuid4().hex}", objective="Routing refusal checks"))
    assert created.status_code == 202
    request_id = created.json()["request_id"]
    stop = requests.post(f"{BASE_URL}/api/portal/requests/{request_id}/stop", headers=operator_headers, json={}, timeout=20)
    retry = requests.post(f"{BASE_URL}/api/portal/requests/{request_id}/retry", headers=operator_headers, json={}, timeout=20)
    result = requests.get(f"{BASE_URL}/api/portal/requests/{request_id}/result", headers=operator_headers, timeout=20)
    assert stop.status_code == 409
    assert retry.status_code == 409
    assert result.status_code == 409
