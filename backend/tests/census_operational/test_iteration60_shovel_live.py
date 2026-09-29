"""Iteration 60 live API contract tests for census shovel origination.

Scope (review_request):
  - Operator login returns access_token.
  - POST /api/portal/census/plan {} reuses active plan (plan_80002c62711eb23e),
    returns commissioned_run_id cr-aa33fffba60e, and is idempotent.
  - Plan envelope carries engine evidence (Targeta MiningPlan, Northena run/trace,
    ledger rows admit + gate targeta_plan_built:<pid>, Solva critic, scoops list,
    cadence).
  - Scoop order matches Targeta ordered_targets; volume_bytes <= target_bytes
    for non-oversized scoops.
  - GET /api/portal/census/plan/{plan_id} for active + terminated + 404 unknown.
  - AuthZ: analyst 403, anonymous 401.
  - Mongo persistence (targeta_mining_plans + northena_ledger_rows) and disk
    ledger files under /app/assessment_workspace/phase0/northena_ledger.
  - Census run cursor state + on-disk dispatch cursor JSON contents.
  - Regressions: /api/portal/census/overview, /api/census/latest.

IMPORTANT constraints from main agent:
  - Do NOT send replan=true. Do NOT call POST /api/portal/census/run.
  - Read-only inspection of files under /app/assessment_workspace/phase0.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import requests
from pymongo import MongoClient

BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/")
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]

OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PW = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PW = "demo-analyst-pw"

EXPECTED_PLAN_ID = "plan_80002c62711eb23e"
EXPECTED_TERMINATED_PLAN_ID = "plan_53927bd32e60e591"
EXPECTED_COMMISSIONED_RUN = "cr-aa33fffba60e"
EXPECTED_CONTINUES_RUN = "cr-399d1b46e9f9"
TARGET_BYTES = 1099511627776


# ---------- fixtures ----------
@pytest.fixture(scope="module")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


def _login(session: requests.Session, email: str, password: str) -> str:
    r = session.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    assert r.status_code == 200, f"login {email} -> {r.status_code}: {r.text[:400]}"
    data = r.json()
    assert "access_token" in data and isinstance(data["access_token"], str) and data["access_token"]
    return data["access_token"]


@pytest.fixture(scope="module")
def operator_token(http):
    return _login(http, OPERATOR_EMAIL, OPERATOR_PW)


@pytest.fixture(scope="module")
def analyst_token(http):
    return _login(http, ANALYST_EMAIL, ANALYST_PW)


@pytest.fixture(scope="module")
def mongo_db():
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    yield client[DB_NAME]
    client.close()


# ---------- auth ----------
def test_operator_login_returns_access_token(operator_token):
    assert operator_token and isinstance(operator_token, str)


def test_analyst_login_returns_access_token(analyst_token):
    assert analyst_token and isinstance(analyst_token, str)


# ---------- POST /api/portal/census/plan ----------
@pytest.fixture(scope="module")
def plan_envelope(http, operator_token):
    r = http.post(
        f"{BASE_URL}/api/portal/census/plan",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={},
        timeout=60,
    )
    assert r.status_code == 200, f"POST plan -> {r.status_code}: {r.text[:600]}"
    return r.json()


def test_plan_envelope_structure(plan_envelope):
    env = plan_envelope
    assert env["tenant_id"] == "RMS"
    assert env["reused_active_plan"] is True
    assert env["commissioned_run_id"] == EXPECTED_COMMISSIONED_RUN
    plan = env["plan"]
    assert plan["plan_id"] == EXPECTED_PLAN_ID
    assert plan["state"] == "active"


def test_plan_is_idempotent(http, operator_token, plan_envelope):
    """Second call must return the SAME plan_id and commissioned run (no duplicates)."""
    r = http.post(
        f"{BASE_URL}/api/portal/census/plan",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={},
        timeout=60,
    )
    assert r.status_code == 200
    env2 = r.json()
    assert env2["plan"]["plan_id"] == plan_envelope["plan"]["plan_id"]
    assert env2["commissioned_run_id"] == plan_envelope["commissioned_run_id"]
    assert env2["reused_active_plan"] is True


def test_plan_carries_targeta_mining_plan(plan_envelope):
    mp = plan_envelope["plan"]["mining_plan"]
    assert mp["mode"] == "per_run"
    assert mp["yield_layer_version"] == "core-only"
    assert isinstance(mp["ordered_targets"], list) and mp["ordered_targets"]
    assert isinstance(mp["core_baseline_ranking"], list)
    gar = mp["governing_artifact_ref"]
    assert gar["artifact_type"] == "objective_request"
    assert gar["artifact_id"] == "census-shovel:RMS"
    assert "version" in gar
    assert "registry_snapshot_ref" in mp


def test_plan_carries_northena_evidence(plan_envelope):
    plan = plan_envelope["plan"]
    assert isinstance(plan.get("northena_run_id"), str) and plan["northena_run_id"].startswith("run-")
    assert plan.get("northena_trace_id")


def test_plan_ledger_rows(plan_envelope):
    rows = plan_envelope["plan"]["ledger_rows"]
    assert isinstance(rows, list) and len(rows) >= 2
    admit_row = next(
        (r for r in rows if r.get("kind") in ("admit", "admitted") or r.get("stage") in ("admit", "admitted")),
        None,
    )
    assert admit_row is not None, f"no admit row in {rows!r}"
    gate_row = next(
        (r for r in rows if (r.get("kind") in ("gate", "warm") or r.get("stage") in ("gate", "warm"))
         and str(r.get("reason", "")).startswith("targeta_plan_built:")),
        None,
    )
    assert gate_row is not None, "no gate/warm row with reason targeta_plan_built:*"
    assert gate_row["reason"] == f"targeta_plan_built:{EXPECTED_PLAN_ID}"


def test_plan_solva_critic(plan_envelope):
    critic = plan_envelope["plan"]["solva_critic"]
    assert "findings" in critic
    assert "citations" in critic


def test_plan_scoops_shape_and_cadence(plan_envelope):
    plan = plan_envelope["plan"]
    scoops = plan["scoops"]
    assert isinstance(scoops, list) and scoops
    for s in scoops:
        assert "sequence" in s
        assert s["kind"] in ("discovery", "region")
        assert "source_id" in s
        assert "source_refs" in s  # may be None for discovery
        if s["kind"] == "discovery":
            assert s["source_refs"] is None
        assert "volume_bytes" in s
        assert "oversized" in s
        assert "state" in s
        if not s["oversized"]:
            assert s["volume_bytes"] <= TARGET_BYTES, f"scoop {s.get('sequence')} exceeds target_bytes"
    assert plan["cadence"]["scoop_target"] == "1.00 TiB per scoop, one at a time"


def test_commissioned_scoop_matches_envelope(plan_envelope):
    """The commissioned_run_id must belong to the scoop whose state=='commissioned'."""
    commissioned = [
        s for s in plan_envelope["plan"]["scoops"] if s.get("state") == "commissioned"
    ]
    assert commissioned, "no commissioned scoop in plan"
    run_ids = {s.get("census_run_id") for s in commissioned}
    assert plan_envelope["commissioned_run_id"] in run_ids


def test_scoop_order_matches_targeta_ordering(plan_envelope):
    plan = plan_envelope["plan"]
    ordered = plan["mining_plan"]["ordered_targets"]
    ordered_refs = [t.get("source_ref") for t in ordered]

    flat_refs: list[str] = []
    for s in sorted(plan["scoops"], key=lambda x: x["sequence"]):
        if s["kind"] == "discovery":
            # discovery target source_ref is '<source_id>:inflight' or ':unmeasured'
            candidates = {f"{s['source_id']}:inflight", f"{s['source_id']}:unmeasured"}
            match = next((r for r in ordered_refs if r in candidates), None)
            assert match is not None, f"discovery scoop {s['source_id']} not in ordered_targets"
            flat_refs.append(match)
        else:
            refs = s.get("source_refs") or []
            flat_refs.extend(refs)

    # The flattened refs from scoops (in scoop-sequence order) must be a prefix-equal
    # subsequence of ordered_refs preserving order.
    # Strict requirement per spec: reproduce the ordered_targets source_ref sequence in order.
    assert flat_refs == ordered_refs[: len(flat_refs)], (
        f"scoop order deviates from Targeta order.\nflat_refs={flat_refs}\nordered_refs={ordered_refs}"
    )


# ---------- GET /api/portal/census/plan/{plan_id} ----------
def test_get_active_plan(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/portal/census/plan/{EXPECTED_PLAN_ID}",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 200, r.text[:400]
    plan = r.json()
    # response may be an envelope with 'plan' or the plan directly
    if "plan" in plan and isinstance(plan["plan"], dict):
        plan = plan["plan"]
    assert plan["plan_id"] == EXPECTED_PLAN_ID
    assert plan["state"] == "active"


def test_get_terminated_plan(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/portal/census/plan/{EXPECTED_TERMINATED_PLAN_ID}",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 200, r.text[:400]
    body = r.json()
    plan = body["plan"] if "plan" in body and isinstance(body["plan"], dict) else body
    assert plan["plan_id"] == EXPECTED_TERMINATED_PLAN_ID
    assert plan["state"] == "terminated"
    rows = plan["ledger_rows"]
    last_reasons = [r.get("reason", "") for r in rows[-4:]]
    assert any("no_progress_signal:owner_dependency_banked" in x for x in last_reasons), (
        f"expected converge/terminate_budget reason in tail, got {last_reasons}"
    )
    for s in plan["scoops"]:
        assert s["state"] == "banked"
        assert s.get("status") == "REFUSED"


def test_get_unknown_plan_404(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/portal/census/plan/plan_does_not_exist_xyz",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 404, f"{r.status_code}: {r.text[:200]}"


# ---------- Authorization ----------
def test_analyst_post_plan_forbidden(http, analyst_token):
    r = http.post(
        f"{BASE_URL}/api/portal/census/plan",
        headers={"Authorization": f"Bearer {analyst_token}"},
        json={},
        timeout=30,
    )
    assert r.status_code == 403, f"expected 403, got {r.status_code}: {r.text[:200]}"


def test_anonymous_post_plan_unauthorized(http):
    r = requests.post(f"{BASE_URL}/api/portal/census/plan", json={}, timeout=30)
    assert r.status_code == 401, f"expected 401, got {r.status_code}: {r.text[:200]}"


# ---------- Mongo persistence ----------
def test_mongo_targeta_mining_plans_persisted(mongo_db):
    coll = mongo_db["targeta_mining_plans"]
    ids = {d.get("plan_id") for d in coll.find({}, {"plan_id": 1})}
    assert EXPECTED_PLAN_ID in ids
    assert EXPECTED_TERMINATED_PLAN_ID in ids


def test_mongo_northena_ledger_rows_for_plan(mongo_db, plan_envelope):
    northena_run_id = plan_envelope["plan"]["northena_run_id"]
    coll = mongo_db["northena_ledger_rows"]
    rows = list(coll.find({"run_id": northena_run_id}))
    assert len(rows) >= 2, f"expected >=2 ledger rows for {northena_run_id}, got {len(rows)}"
    kinds = {(r.get("kind") or r.get("stage")) for r in rows}
    assert kinds & {"admit", "admitted"}
    assert kinds & {"gate", "warm"}


def test_northena_ledger_rows_on_disk(mongo_db, plan_envelope):
    northena_run_id = plan_envelope["plan"]["northena_run_id"]
    coll = mongo_db["northena_ledger_rows"]
    rows = list(coll.find({"run_id": northena_run_id}))
    ledger_dir = Path("/app/assessment_workspace/phase0/northena_ledger")
    assert ledger_dir.is_dir()
    missing = []
    for r in rows:
        row_id = r.get("row_id") or r.get("id")
        if not row_id:
            continue
        if not (ledger_dir / f"{row_id}.json").is_file():
            missing.append(row_id)
    assert not missing, f"missing ledger files on disk: {missing}"


# ---------- Census run cursor ----------
def test_census_run_state_endpoint(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/portal/census/runs/{EXPECTED_COMMISSIONED_RUN}/state",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 200, f"{r.status_code}: {r.text[:400]}"
    body = r.json()
    # If the view surfaces scoop_plan_id/scoop_index, verify. Otherwise skip that check
    # in favor of on-disk cursor verification (below).
    if "scoop_plan_id" in body:
        assert body["scoop_plan_id"] == EXPECTED_PLAN_ID
        assert body.get("scoop_index") == 0


def test_dispatch_cursor_file_contents():
    p = Path(
        f"/app/assessment_workspace/phase0/census_autonomy_state/dispatch/{EXPECTED_COMMISSIONED_RUN}.json"
    )
    assert p.is_file(), f"cursor file missing: {p}"
    data = json.loads(p.read_text())
    assert data.get("scoop_plan_id") == EXPECTED_PLAN_ID
    assert data.get("scoop_index") == 0
    assert isinstance(data.get("not_before"), (int, float))
    assert data.get("busy_retry_attempt") == 1
    assert data.get("continues_run_id") == EXPECTED_CONTINUES_RUN


# ---------- Regressions ----------
def test_regression_overview(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/portal/census/overview",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 200
    body = r.json()
    for key in ("records", "runs", "sources"):
        assert key in body, f"missing key {key} in overview"


def test_regression_census_latest(http, operator_token):
    r = http.get(
        f"{BASE_URL}/api/census/latest",
        headers={"Authorization": f"Bearer {operator_token}"},
        timeout=30,
    )
    assert r.status_code == 200, f"{r.status_code}: {r.text[:200]}"
