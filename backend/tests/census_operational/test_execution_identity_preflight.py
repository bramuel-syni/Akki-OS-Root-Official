"""Local identity preflight + refusal-path live contract checks (no SSH transport execution)."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values

from services.census_autonomy.execution_identity import IdentityVerificationError, verify_identity
from services.training_runner import ssh_seam


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"

pytestmark = pytest.mark.skipif(
    os.environ.get("AKKI_RUN_IDENTITY_REFUSAL_DRILL") != "1",
    reason="Explicit authorization required for custody access and a production refusal drill",
)

RECEIPT_DIR = Path(
    "/app/assessment_workspace/phase0/drill_receipts/census_operational_v1/execution_recovery/local_preflight_identity_refusal.json"
).parent


def _load_env_file(path: Path, monkeypatch) -> None:
    # Match dotenv parsing used by the app and restore process env after tests.
    for key, value in dotenv_values(path).items():
        if key not in os.environ and value is not None:
            monkeypatch.setenv(key, value)


def _login_operator_token() -> str:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL not set")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": OPERATOR_EMAIL, "password": OPERATOR_PASSWORD},
        timeout=20,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("access_token"), str) and data["access_token"]
    return data["access_token"]


@pytest.fixture
def fresh_local_preflight(monkeypatch):
    # Load backend .env into process for local-only identity verification.
    _load_env_file(Path("/app/backend/.env"), monkeypatch)

    hosts = ssh_seam.list_hosts()
    assert len(hosts) == 2

    checks = []
    all_pin_mismatch = True

    for i, host in enumerate(hosts):
        config = ssh_seam.get_host_config(host)
        receipt_ref = os.environ.get(f"{config.slug}_SSH_IDENTITY_RECEIPT_PATH", "")
        try:
            verify_identity(config)
            all_pin_mismatch = False
            checks.append({"slot": i, "status": "unexpected_match", "reason_code": "IDENTITY_MATCHED"})
        except IdentityVerificationError as exc:
            checks.append(
                {
                    "slot": i,
                    "status": "refused",
                    "reason_code": exc.reason_code,
                    "identity_receipt_ref": Path(receipt_ref).name if receipt_ref else "missing",
                }
            )
            if exc.reason_code != "IDENTITY_PIN_MISMATCH":
                all_pin_mismatch = False

    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all_pin_mismatch else "FAIL",
        "safe_code": "LOCAL_IDENTITY_PREFLIGHT",
        "host_count": len(hosts),
        "checks": checks,
    }
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    with (RECEIPT_DIR / f"local_preflight_{stamp}.json").open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    assert all_pin_mismatch
    return payload


def test_local_preflight_identity_refusal_for_existing_hosts_only(fresh_local_preflight):
    assert fresh_local_preflight["status"] == "PASS"


def test_live_refusal_path_idempotency_after_preflight_pin_mismatch(fresh_local_preflight):
    # This cannot consume a receipt from an earlier run or test invocation.
    assert fresh_local_preflight["status"] == "PASS"

    token = _login_operator_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    idempotency_key = "test-identity-refusal-idempotent-v1"
    payload = {
        "source_ids": ["rms_mysql"],
        "idempotency_key": idempotency_key,
    }
    assert payload.keys() == {"source_ids", "idempotency_key"}

    run_response = requests.post(f"{BASE_URL}/api/portal/census/run", headers=headers, json=payload, timeout=30)
    assert run_response.status_code == 202
    run_body = run_response.json()
    run_id = run_body.get("census_run_id")
    assert isinstance(run_id, str) and run_id

    state = None
    for _ in range(30):
        poll = requests.get(f"{BASE_URL}/api/portal/census/runs/{run_id}/state", headers=headers, timeout=20)
        assert poll.status_code == 200
        state = poll.json()
        if state.get("status") == "REFUSED":
            break
        time.sleep(1)

    assert state and state.get("status") == "REFUSED"
    top_reason = str(state.get("reason_code", ""))
    nested_reason = ""
    outcomes = state.get("outcomes") or []
    if outcomes and isinstance(outcomes, list):
        nested_reason = str((outcomes[0] or {}).get("reason_code", ""))
    assert "IDENTITY_NOT_VERIFIED" in f"{top_reason} {nested_reason}"

    transport_path = Path(
        f"/app/assessment_workspace/phase0/census_autonomy_state/dispatch/transport-{run_id}-rms_mysql.json"
    )
    assert transport_path.exists()
    transport_doc = json.loads(transport_path.read_text(encoding="utf-8"))
    attempts = transport_doc.get("attempts", [])
    assert len(attempts) == 2
    assert all(a.get("reason_code") == "IDENTITY_PIN_MISMATCH" for a in attempts)

    repeat = requests.post(f"{BASE_URL}/api/portal/census/run", headers=headers, json=payload, timeout=30)
    assert repeat.status_code == 202
    repeat_body = repeat.json()
    assert repeat_body.get("census_run_id") == run_id
