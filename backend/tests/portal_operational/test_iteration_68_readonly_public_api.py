"""Read-only public API checks for auth + portal entitlement/census surfaces (no writes)."""

import os
from datetime import datetime, timezone

import pytest
import requests
from dotenv import load_dotenv


load_dotenv("/app/frontend/.env")
BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    raise RuntimeError("REACT_APP_BACKEND_URL is required for public endpoint tests")
BASE_URL = BASE_URL.rstrip("/")

RMS = {
    "email": os.environ.get("M7_READINESS_RMS_EMAIL"),
    "password": os.environ.get("M7_READINESS_RMS_PASSWORD"),
}
DIGICOW = {
    "email": os.environ.get("M7_READINESS_DIGICOW_EMAIL"),
    "password": os.environ.get("M7_READINESS_DIGICOW_PASSWORD"),
}


def _login(session: requests.Session, creds: dict) -> str:
    if not all(creds.values()):
        pytest.skip("Set the M7_READINESS_RMS/DIGICOW_EMAIL/PASSWORD test environment variables")
    response = session.post(f"{BASE_URL}/api/auth/login", json=creds, timeout=30)
    assert response.status_code == 200
    data = response.json()
    token = data.get("access_token")
    assert isinstance(token, str) and len(token) > 20
    return token


@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# Module/feature: login + /api/auth/me contract for both retained operator identities.
@pytest.mark.parametrize("creds", [RMS, DIGICOW])
def test_operator_login_and_me_readonly_contract(session, creds):
    token = _login(session, creds)
    session.headers.update({"Authorization": f"Bearer {token}"})
    me = session.get(f"{BASE_URL}/api/auth/me", timeout=30)
    assert me.status_code == 200
    data = me.json()
    assert data.get("email") == creds["email"]


# Module/feature: protected endpoints refuse missing auth.
@pytest.mark.parametrize(
    "path",
    [
        "/api/auth/me",
        "/api/portal/census/overview",
        "/api/portal/entitlement/licence",
        "/api/portal/entitlement/allowance",
        "/api/portal/entitlement/catalog/listed",
        "/api/portal/entitlement/badges",
    ],
)
def test_missing_auth_refused(path):
    response = requests.get(f"{BASE_URL}{path}", timeout=30)
    assert response.status_code in (401, 403)


def _read_surface(session: requests.Session, token: str, path: str):
    session.headers.update({"Authorization": f"Bearer {token}"})
    response = session.get(f"{BASE_URL}{path}", timeout=30)
    assert response.status_code == 200
    return response.json()


# Module/feature: entitlement/census portal reads resolve and stay non-mutating across tenants.
def test_readonly_portal_surfaces_rms_vs_digicow(session):
    rms_token = _login(session, RMS)
    rms_overview = _read_surface(session, rms_token, "/api/portal/census/overview")
    rms_licence = _read_surface(session, rms_token, "/api/portal/entitlement/licence")
    rms_allowance = _read_surface(session, rms_token, "/api/portal/entitlement/allowance")
    rms_catalog = _read_surface(session, rms_token, "/api/portal/entitlement/catalog/listed")
    rms_badges = _read_surface(session, rms_token, "/api/portal/entitlement/badges")

    digicow_token = _login(session, DIGICOW)
    digicow_overview = _read_surface(session, digicow_token, "/api/portal/census/overview")
    digicow_licence = _read_surface(session, digicow_token, "/api/portal/entitlement/licence")
    digicow_allowance = _read_surface(session, digicow_token, "/api/portal/entitlement/allowance")
    digicow_catalog = _read_surface(session, digicow_token, "/api/portal/entitlement/catalog/listed")
    digicow_badges = _read_surface(session, digicow_token, "/api/portal/entitlement/badges")

    for payload in (rms_licence, rms_allowance, digicow_licence, digicow_allowance):
        assert payload.get("status") in ("resolved", "unresolved", "expired", "suspended")
        assert "reason_code" in payload

    assert rms_licence.get("status") == "resolved"
    assert digicow_licence.get("status") == "resolved"

    assert isinstance(rms_catalog.get("rows", []), list)
    assert isinstance(digicow_catalog.get("rows", []), list)
    assert isinstance(rms_badges.get("badges", []), list)
    assert isinstance(digicow_badges.get("badges", []), list)
    # Zero visible rows was an observation, not an invariant: future admitted
    # rows must not fail this read-contract test merely by existing.
    assert rms_catalog.get("count") == len(rms_catalog["rows"])
    assert digicow_catalog.get("count") == len(digicow_catalog["rows"])

    assert rms_overview["tenant_id"] == "RMS"
    assert digicow_overview["tenant_id"] == "DIGICOW"


# Module/feature: retained census identifiers must not leak cross-tenant details.
@pytest.mark.parametrize("owner,other,tenant", [(RMS, DIGICOW, "RMS"), (DIGICOW, RMS, "DIGICOW")])
def test_cross_tenant_read_refusal_with_retained_census_id(session, owner, other, tenant):
    owner_token = _login(session, owner)
    session.headers.update({"Authorization": f"Bearer {owner_token}"})
    records = session.get(f"{BASE_URL}/api/portal/census/records", timeout=30)
    assert records.status_code == 200
    records_json = records.json()
    assert records_json["tenant_id"] == tenant
    rows = records_json["records"]
    if not rows:
        pytest.skip("No retained census rows exposed to validate cross-tenant record-id isolation")

    record_id = rows[0]["record_id"]
    own_detail = session.get(f"{BASE_URL}/api/portal/census/records/{record_id}", timeout=30)
    assert own_detail.status_code == 200

    other_token = _login(session, other)
    session.headers.update({"Authorization": f"Bearer {other_token}"})
    foreign_detail = session.get(f"{BASE_URL}/api/portal/census/records/{record_id}", timeout=30)
    assert foreign_detail.status_code in (401, 403, 404)


# Module/feature: billing endpoint mount/read check (if mounted should be GET-200, else explicit 404).
def test_billing_endpoint_mount_read(session):
    token = _login(session, RMS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    period = datetime.now(timezone.utc).strftime("%Y-%m")
    response = session.get(f"{BASE_URL}/api/portal/entitlement/billing", params={"period": period}, timeout=30)

    assert response.status_code == 200
    data = response.json()
    assert data.get("scope") == "principal"
    assert "financial_invoice_issued" in data
