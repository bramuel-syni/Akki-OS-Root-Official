"""Live API contracts for activation native receipt/readiness/settlement/issuance endpoints."""

from __future__ import annotations

import time
import uuid

import pytest
import requests

from test_activation_controls_api_live import (
    BASE_URL,
    _base_document,
    _operator_scope,
    _read_existing_demo_credentials,
    _require_base_url,
    _login,
)


@pytest.fixture(scope="session")
def operator_headers() -> dict:
    _require_base_url()
    (operator_email, operator_password), _ = _read_existing_demo_credentials()
    return _login(operator_email, operator_password)


@pytest.fixture(scope="session")
def analyst_headers() -> dict:
    _require_base_url()
    _, (analyst_email, analyst_password) = _read_existing_demo_credentials()
    return _login(analyst_email, analyst_password)


def _receipt_payload(tenant_id: str, *, signer: str = "owner") -> dict:
    now = int(time.time())
    return {
        "version": "akki.activation.receipt/1",
        "tenant_id": tenant_id,
        "signer_id": signer,
        "key_id": "SYNTHETIC-key",
        "kind": "allocation",
        "request_sha256": None,
        "scope_refs": ["source-scope"],
        "issued_epoch": now - 1,
        "expires_epoch": now + 600,
        "claims": {"terms_ref": "terms-1", "limits": [{"dimension": "spend", "unit": "USD", "quantity": "0"}]},
        "signature_hex": "0" * 128,
    }


def _request_payload(tenant_id: str, principal_id: str) -> dict:
    return {
        "request_id": f"req_{uuid.uuid4().hex}",
        "tenant_id": tenant_id,
        "principal_id": principal_id,
        "kind": "source",
        "engine": "mtafiti",
        "objective_sha256": "a" * 64,
        "input_refs": ["akki://source/descriptor"],
        "scope_refs": ["source-scope"],
        "deadline_epoch": int(time.time()) + 900,
    }


# Module/feature: write endpoints enforce anonymous/operator/analyst gates.
@pytest.mark.parametrize(
    "path,body,analyst_expected,operator_expected",
    [
        ("/api/portal/activation/receipts", {"invalid": True}, 403, 422),
        ("/api/portal/activation/readiness", {"invalid": True}, 422, 422),
        ("/api/portal/activation/reservations/settle", {"invalid": True}, 403, 422),
        ("/api/portal/activation/certificates/issue", {"invalid": True}, 403, 422),
    ],
)
def test_activation_records_authz_matrix(
    operator_headers,
    analyst_headers,
    path,
    body,
    analyst_expected,
    operator_expected,
):
    _require_base_url()
    anon = requests.post(f"{BASE_URL}{path}", json=body, timeout=20)
    assert anon.status_code == 401

    analyst = requests.post(f"{BASE_URL}{path}", headers=analyst_headers, json=body, timeout=20)
    assert analyst.status_code == analyst_expected

    operator = requests.post(f"{BASE_URL}{path}", headers=operator_headers, json=body, timeout=20)
    assert operator.status_code == operator_expected


# Module/feature: bounded payload parser rejects duplicate keys and non-finite constants.
def test_activation_receipts_rejects_duplicate_and_non_finite_json(operator_headers):
    _require_base_url()
    endpoint = f"{BASE_URL}/api/portal/activation/receipts"
    duplicate = '{"version":"akki.activation.receipt/1","version":"akki.activation.receipt/1"}'
    dup = requests.post(endpoint, headers=operator_headers, data=duplicate, timeout=20)
    assert dup.status_code == 422

    non_finite = '{"version":"akki.activation.receipt/1","claims":{"x":NaN}}'
    nan = requests.post(endpoint, headers=operator_headers, data=non_finite, timeout=20)
    assert nan.status_code == 422


# Module/feature: native receipt verification enforces tenant isolation before record.
def test_activation_receipts_cross_tenant_is_held(operator_headers):
    _require_base_url()
    tenant_id, _ = _operator_scope(operator_headers)
    forged = _receipt_payload("foreign-tenant" if tenant_id != "foreign-tenant" else "rms")
    response = requests.post(
        f"{BASE_URL}/api/portal/activation/receipts",
        headers=operator_headers,
        json=forged,
        timeout=20,
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "held"
    assert body.get("reason_code") == "RECEIPT_TENANT_MISMATCH"


# Module/feature: readiness request must be inside authenticated tenant/principal scope.
def test_activation_readiness_cross_scope_forbidden(operator_headers):
    _require_base_url()
    tenant_id, principal_id = _operator_scope(operator_headers)
    body = _request_payload(tenant_id, "another-principal" if principal_id != "another-principal" else "operator")
    response = requests.post(
        f"{BASE_URL}/api/portal/activation/readiness",
        headers=operator_headers,
        json=body,
        timeout=20,
    )
    assert response.status_code == 403


# Module/feature: issuance fails closed when admitted signer resolver is unbound.
def test_activation_issue_unbound_signer_resolver_returns_held(operator_headers):
    _require_base_url()
    tenant_id, principal_id = _operator_scope(operator_headers)
    cert = _base_document()
    cert["certificate_id"] = f"cert_{uuid.uuid4().hex}"
    cert["identity"]["estate_id"] = tenant_id
    cert["identity"]["tenant_id"] = tenant_id
    cert["identity"].pop("proposing_principal_id", None)

    response = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/issue",
        headers=operator_headers,
        json={"certificate": cert},
        timeout=20,
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "held"
    assert body.get("reason_code") == "ADMITTED_SIGNER_RESOLVER_UNBOUND"
    assert body.get("certificate_issued") is False
    assert body.get("execution_authorized") is False


# Module/feature: settle endpoint fails closed for unresolved references.
def test_activation_settle_unknown_refs_are_held(operator_headers):
    _require_base_url()
    response = requests.post(
        f"{BASE_URL}/api/portal/activation/reservations/settle",
        headers=operator_headers,
        json={"reservation_ref": "nope", "observation_ref": "nope"},
        timeout=20,
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "held"
    assert body.get("reason_code") in {
        "AUTHORITATIVE_RECEIPT_UNRESOLVED",
        "RECEIPT_KIND_MISMATCH",
        "RECEIPT_REQUEST_MISMATCH",
        "RESERVATION_NOT_OWNED",
    }
