"""RED contract tests for portal operational request lifecycle and OS work parity.

These tests intentionally assert the target public contract. Current STUBBED
endpoints are expected to fail until durable request/work persistence exists.
"""

import hashlib
import os
import uuid
from pathlib import Path
from typing import Dict, Tuple

import pytest
import requests



def _resolve_base_url() -> str:
    env_url = (os.environ.get("REACT_APP_BACKEND_URL") or "").strip()
    if env_url:
        return env_url.rstrip("/")

    frontend_env = Path("/app/frontend/.env")
    if frontend_env.is_file():
        for line in frontend_env.read_text(encoding="utf-8").splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip().rstrip("/")
    return ""


BASE_URL = _resolve_base_url()

# Existing demo credentials (from /app/memory/test_credentials.md)
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
    payload = response.json()
    token = payload.get("access_token")
    assert isinstance(token, str) and token
    return token


@pytest.fixture(scope="session")
def operator_headers() -> Dict[str, str]:
    _require_base_url()
    token = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def analyst_headers() -> Dict[str, str]:
    _require_base_url()
    token = _login(ANALYST_EMAIL, ANALYST_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _base_submit_payload(*, idem: str, objective_text: str = "Review retained RMS source scope") -> dict:
    return {
        "objective_text": objective_text,
        "operation": "processed_intelligence",
        "units": ["rms_mysql"],
        "idempotency_key": idem,
    }


def _assert_submit_shape(data: dict, request_payload: dict) -> Tuple[str, str, str]:
    assert isinstance(data.get("request_id"), str) and data["request_id"]
    assert isinstance(data.get("work_id"), str) and data["work_id"]
    assert data["request_id"] == data["work_id"]
    assert isinstance(data.get("objective_hash"), str) and data["objective_hash"]
    expected_hash = hashlib.sha256(request_payload["objective_text"].encode("utf-8")).hexdigest()
    assert data["objective_hash"] == expected_hash
    assert isinstance(data.get("state"), str) and data["state"]
    return data["request_id"], data["work_id"], data["objective_hash"]


# Module/feature: auth gate and anonymous denial rules
def test_requests_and_os_work_deny_anonymous_access():
    _require_base_url()
    endpoints = [
        ("GET", "/api/portal/requests"),
        ("POST", "/api/portal/requests"),
        ("GET", "/api/os/work"),
        ("GET", "/api/os/work/nonexistent"),
        ("POST", "/api/portal/requests/nonexistent/stop"),
        ("POST", "/api/portal/requests/nonexistent/retry"),
    ]
    for method, path in endpoints:
        if method == "POST":
            body = _base_submit_payload(idem=f"anon-{uuid.uuid4().hex}") if path.endswith("/requests") else {}
            response = requests.post(f"{BASE_URL}{path}", json=body, timeout=20)
        else:
            response = requests.get(f"{BASE_URL}{path}", timeout=20)
        assert response.status_code in (401, 403), f"{method} {path} returned {response.status_code}"


# Module/feature: request submission persistence + same request/work ID contract
def test_submit_returns_durable_ids_hash_state_and_persists_in_list_and_detail(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-submit-{uuid.uuid4().hex}")

    submit = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert submit.status_code == 202
    body = submit.json()
    request_id, work_id, objective_hash = _assert_submit_shape(body, payload)

    listing = requests.get(f"{BASE_URL}/api/portal/requests", headers=operator_headers, timeout=20)
    assert listing.status_code == 200
    listing_data = listing.json()
    assert isinstance(listing_data.get("rows"), list)
    row = next((r for r in listing_data["rows"] if r.get("request_id") == request_id), None)
    assert row is not None
    assert row.get("work_id") == work_id
    assert row.get("objective_hash") == objective_hash

    detail = requests.get(f"{BASE_URL}/api/portal/requests/{request_id}", headers=operator_headers, timeout=20)
    assert detail.status_code == 200
    detail_data = detail.json()
    assert detail_data.get("request_id") == request_id
    assert detail_data.get("work_id") == work_id
    assert detail_data.get("objective_hash") == objective_hash


# Module/feature: idempotency semantics (same key/body stable id, changed body conflict)
def test_idempotency_same_key_same_body_same_id_and_changed_body_conflicts(operator_headers):
    _require_base_url()
    idem = f"red-idem-{uuid.uuid4().hex}"
    payload1 = _base_submit_payload(idem=idem, objective_text="Review retained RMS source scope")
    payload2 = _base_submit_payload(idem=idem, objective_text="Changed objective text for collision")

    first = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload1, timeout=20)
    assert first.status_code == 202
    first_id = first.json().get("request_id")
    assert isinstance(first_id, str) and first_id

    second = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload1, timeout=20)
    assert second.status_code == 202
    assert second.json().get("request_id") == first_id

    changed = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload2, timeout=20)
    assert changed.status_code == 409


# Module/feature: payload hardening forbids caller identity/approval/result injection
def test_submit_forbids_identity_and_approval_or_result_input_fields(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-forbid-{uuid.uuid4().hex}")
    payload.update(
        {
            "principal_id": "forged-principal",
            "tenant_id": "DIGICOW",
            "approver_id": "forged-approver",
            "answer_stub": "forged-answer",
            "class_label": "forged-class",
        }
    )
    response = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert response.status_code == 422


# Module/feature: unknown/cross-tenant units refusal
def test_submit_refuses_unknown_or_cross_tenant_units(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-units-{uuid.uuid4().hex}")
    payload["units"] = ["digicow_mysql"]

    response = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert response.status_code in (403, 422)


# Module/feature: requester stop/retry invalid records must 404 (no fake Stopped)
def test_stop_and_retry_nonexistent_request_return_404(operator_headers):
    _require_base_url()
    bogus = f"req-does-not-exist-{uuid.uuid4().hex}"

    stop = requests.post(f"{BASE_URL}/api/portal/requests/{bogus}/stop", headers=operator_headers, json={}, timeout=20)
    assert stop.status_code == 404

    retry = requests.post(f"{BASE_URL}/api/portal/requests/{bogus}/retry", headers=operator_headers, json={}, timeout=20)
    assert retry.status_code == 404


# Module/feature: role and principal isolation
def test_authenticated_other_principal_cannot_access_foreign_record(operator_headers, analyst_headers):
    _require_base_url()
    submit_payload = _base_submit_payload(idem=f"red-principal-{uuid.uuid4().hex}")
    created = requests.post(
        f"{BASE_URL}/api/portal/requests",
        headers=operator_headers,
        json=submit_payload,
        timeout=20,
    )
    assert created.status_code == 202
    request_id = created.json().get("request_id")
    assert isinstance(request_id, str) and request_id

    for path, method in [
        (f"/api/portal/requests/{request_id}", "GET"),
        (f"/api/portal/requests/{request_id}/stop", "POST"),
        (f"/api/portal/requests/{request_id}/retry", "POST"),
    ]:
        if method == "GET":
            resp = requests.get(f"{BASE_URL}{path}", headers=analyst_headers, timeout=20)
        else:
            resp = requests.post(f"{BASE_URL}{path}", headers=analyst_headers, json={}, timeout=20)
        assert resp.status_code in (401, 403, 404)


# Module/feature: OS work consumer reads same record as portal request
def test_os_work_list_and_detail_match_portal_request_record(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-os-work-{uuid.uuid4().hex}")
    created = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert created.status_code == 202
    request_id = created.json().get("request_id")
    assert isinstance(request_id, str) and request_id

    os_list = requests.get(f"{BASE_URL}/api/os/work", headers=operator_headers, timeout=20)
    assert os_list.status_code == 200
    os_rows = os_list.json().get("rows")
    assert isinstance(os_rows, list)
    os_row = next((r for r in os_rows if r.get("work_id") == request_id), None)
    assert os_row is not None
    assert os_row.get("request_id") == request_id

    os_detail = requests.get(f"{BASE_URL}/api/os/work/{request_id}", headers=operator_headers, timeout=20)
    assert os_detail.status_code == 200
    os_detail_data = os_detail.json()
    assert os_detail_data.get("work_id") == request_id
    assert os_detail_data.get("request_id") == request_id


# Module/feature: history disclosure must not leak approver identity/payload internals
def test_requester_history_redacts_approver_identity_and_internal_decision_payload(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-history-{uuid.uuid4().hex}")
    created = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert created.status_code == 202
    request_id = created.json().get("request_id")
    assert isinstance(request_id, str) and request_id

    detail = requests.get(f"{BASE_URL}/api/portal/requests/{request_id}", headers=operator_headers, timeout=20)
    assert detail.status_code == 200
    data = detail.json()
    history = data.get("history")
    assert isinstance(history, list) and history

    serialized = str(data).lower()
    forbidden = [
        "approver_id",
        "approver_name",
        "approver_initials",
        "approval_decision_payload",
        "internal_decision_payload",
    ]
    assert all(f not in serialized for f in forbidden)


# Module/feature: execution remains gated; accepted submission != accepted extraction
def test_accepted_request_does_not_claim_production_execution(operator_headers):
    _require_base_url()
    payload = _base_submit_payload(idem=f"red-gate-{uuid.uuid4().hex}")
    response = requests.post(f"{BASE_URL}/api/portal/requests", headers=operator_headers, json=payload, timeout=20)
    assert response.status_code == 202
    data = response.json()
    assert data.get("state") in {"submitted", "routing", "in_approval", "blocked", "unresolved"}
    assert data.get("state") not in {"executing", "ready", "retrieved", "completed"}


# Module/feature: entitlement allowance unresolved when licence record missing
def test_entitlement_allowance_without_licence_is_unresolved_and_null_state(operator_headers):
    _require_base_url()
    response = requests.get(f"{BASE_URL}/api/portal/entitlement/allowance", headers=operator_headers, timeout=20)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "unresolved"
    assert data.get("allowance_state") is None


# Module/feature: entitlement reads are scoped and auth-protected
def test_entitlement_licence_catalog_badges_are_scoped_reads(operator_headers):
    _require_base_url()
    for path in [
        "/api/portal/entitlement/licence",
        "/api/portal/entitlement/catalog/listed",
        "/api/portal/entitlement/badges",
    ]:
        response = requests.get(f"{BASE_URL}{path}", headers=operator_headers, timeout=20)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("principal_id"), str) and data["principal_id"]
