"""M3 live bindings — Northena Coordinator bound to M1 census transport.

Tests the DIGICOW operator-visible /api/portal/commission and /api/portal/requests
endpoints against the LIVE control plane. Follows review_request features_or_bugs_to_test.
"""
import os
import time
import uuid
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")

DIGICOW_EMAIL = "demo.operator@demo.digicow.example.com"
DIGICOW_PW = "demo-digicow-operator-pw"
RMS_ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
RMS_ANALYST_PW = "demo-analyst-pw"

REQ_READY = "req-97999a0b46d2f51564b85dcd05d871a2"
REQ_STOPPED = "req-393db89ef35ac94ccae17770f52b1c1f"
REQ_INTERRUPTED = "req-c1f2738b3449081569aebfbfd537e2a6"

LONG_TIMEOUT = 150


def _login(email, password):
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": password}, timeout=30)
    assert r.status_code == 200, f"login {email} -> {r.status_code} {r.text}"
    body = r.json()
    token = body.get("token") or body.get("access_token")
    assert token, f"no token in response: {body}"
    return token


@pytest.fixture(scope="module")
def digicow_headers():
    tok = _login(DIGICOW_EMAIL, DIGICOW_PW)
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


@pytest.fixture(scope="module")
def rms_analyst_headers():
    tok = _login(RMS_ANALYST_EMAIL, RMS_ANALYST_PW)
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


# ---------- 1. READ-ONLY /run on ready request ----------
class TestReadyRunView:
    def test_run_view_phases_and_terminal(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/run", headers=digicow_headers, timeout=60)
        assert r.status_code == 200, r.text
        body = r.json()
        phases_raw = body.get("phases", [])
        # phases is a list of {phase, reached}
        phases = {p["phase"]: p for p in phases_raw} if isinstance(phases_raw, list) else phases_raw
        required = ["commissioned", "reserved", "limits_admitted", "sent", "observed", "verified", "metered", "terminal"]
        for p in required:
            assert p in phases, f"missing phase {p}"
            assert phases[p].get("reached") is True, f"phase {p} not reached: {phases[p]}"

        terminal = body.get("terminal") or phases.get("terminal", {})
        assert terminal.get("phase") == "ready", terminal
        assert terminal.get("reason_code") == "VERIFIED_RESULT_RECORDED", terminal
        assert terminal.get("evidence_mode") == "measured", terminal

        artifact_refs = body.get("artifact_refs") or terminal.get("artifact_refs") or []
        expected = f"akki://artifact/DIGICOW/{REQ_READY}/qualified-units"
        assert artifact_refs == [expected], f"artifact_refs={artifact_refs}"

        budget = body.get("budget") or []
        def _get_budget(name):
            if isinstance(budget, list):
                for row in budget:
                    if row.get("dimension") == name or row.get("name") == name:
                        return row
            return None

        rr = _get_budget("returned_records")
        ac = _get_budget("active_compute")
        assert rr is not None, f"returned_records missing from budget: {budget}"
        assert ac is not None, f"active_compute missing from budget: {budget}"
        rr_consumed = rr.get("consumed") if isinstance(rr, dict) else None
        ac_consumed = ac.get("consumed") if isinstance(ac, dict) else None
        assert str(rr_consumed) == "200", f"returned_records consumed={rr_consumed}"
        assert ac_consumed is not None and str(ac_consumed) != "None", f"active_compute consumed={ac_consumed}"
        assert str(ac_consumed) == "0.38", f"active_compute consumed={ac_consumed}"

        registry = body.get("registry") or {}
        records = registry.get("records") or []
        assert len(records) >= 1, f"registry.records empty: {registry}"
        fs = records[0].get("freshness_stamp") or {}
        assert fs.get("logged_date") == "2026-09-29T15:38:40+00:00", f"freshness_stamp={fs}"

        sealed = body.get("sealed") or {}
        quality = sealed.get("quality") or {}
        assert quality.get("qualified_units") == 200, f"sealed.quality={quality}"


# ---------- 2. READ-ONLY /requests/{id} and /result and /commission ----------
class TestReadyRequestViews:
    def test_request_summary(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}", headers=digicow_headers, timeout=60)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body.get("lifecycle_state") == "Ready", body.get("lifecycle_state")
        assert body.get("execution_verified") is True
        pa = body.get("permitted_actions") or []
        assert pa == ["result"], f"permitted_actions={pa}"

    def test_result_view(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/result", headers=digicow_headers, timeout=60)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body.get("execution_verified") is True
        assert body.get("delivery_verified") is False

    def test_commission_view_matches_run(self, digicow_headers):
        r_c = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/commission", headers=digicow_headers, timeout=60)
        assert r_c.status_code == 200, r_c.text
        r_r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/run", headers=digicow_headers, timeout=60)
        assert r_r.status_code == 200
        c = r_c.json()
        rn = r_r.json()
        assert c.get("request_id") == REQ_READY
        wo_c = c.get("work_order_ref") or (c.get("commissioning") or {}).get("work_order_ref")
        wo_r = rn.get("work_order_ref") or (rn.get("commissioning") or {}).get("work_order_ref")
        # try nested search if not top-level
        def _find_wo(obj):
            if isinstance(obj, dict):
                if "work_order_ref" in obj:
                    return obj["work_order_ref"]
                for v in obj.values():
                    got = _find_wo(v)
                    if got:
                        return got
            elif isinstance(obj, list):
                for v in obj:
                    got = _find_wo(v)
                    if got:
                        return got
            return None
        if not wo_c:
            wo_c = _find_wo(c)
        if not wo_r:
            wo_r = _find_wo(rn)
        assert wo_c and wo_r and wo_c == wo_r, f"work_order_ref mismatch: {wo_c} vs {wo_r}"


# ---------- 3. Idempotent re-advance on ready request ----------
class TestIdempotentAdvance:
    def test_advance_three_times_stable(self, digicow_headers):
        first_freshness = None
        for i in range(3):
            r = requests.post(f"{BASE_URL}/api/portal/commission/{REQ_READY}/advance",
                              headers=digicow_headers, json={}, timeout=LONG_TIMEOUT)
            assert r.status_code == 200, f"call {i}: {r.status_code} {r.text[:400]}"
            body = r.json()
            terminal = body.get("terminal") or (body.get("phases") or {}).get("terminal") or {}
            phase = terminal.get("phase") or body.get("phase")
            reason = terminal.get("reason_code") or body.get("reason_code")
            assert phase == "ready", f"call {i} phase={phase} body keys={list(body)[:8]}"
            assert reason == "VERIFIED_RESULT_RECORDED", f"call {i} reason={reason}"

        # freshness_stamp unchanged
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/run", headers=digicow_headers, timeout=60)
        assert r.status_code == 200
        fs = (r.json().get("registry") or {}).get("records", [{}])[0].get("freshness_stamp", {})
        assert fs.get("logged_date") == "2026-09-29T15:38:40+00:00", f"freshness drifted: {fs}"


# ---------- 4. Stopped run view ----------
class TestStoppedRun:
    def test_stopped_run_view(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_STOPPED}/run", headers=digicow_headers, timeout=60)
        assert r.status_code == 200, r.text
        body = r.json()
        terminal = body.get("terminal") or (body.get("phases") or {}).get("terminal") or {}
        assert terminal.get("phase") == "cancelled", terminal
        assert terminal.get("reason_code") == "EXECUTOR_CANCELLED", terminal
        refs = body.get("artifact_refs") or terminal.get("artifact_refs") or []
        assert refs == [], f"artifact_refs should be empty: {refs}"

        budget = body.get("budget") or []
        def _get(name):
            if isinstance(budget, list):
                for row in budget:
                    if row.get("dimension") == name or row.get("name") == name:
                        return row
            return None
        sr = _get("scanned_records")
        ac = _get("active_compute")
        assert sr and str(sr.get("consumed")) == "2500", f"scanned={sr}"
        assert ac and str(ac.get("consumed")) == "1", f"active_compute={ac}"

    def test_stopped_summary(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_STOPPED}", headers=digicow_headers, timeout=60)
        assert r.status_code == 200
        body = r.json()
        assert body.get("lifecycle_state") == "Stopped", body.get("lifecycle_state")
        assert body.get("permitted_actions") == [], body.get("permitted_actions")

    def test_stop_on_stopped_conflict(self, digicow_headers):
        r = requests.post(f"{BASE_URL}/api/portal/requests/{REQ_STOPPED}/stop",
                          headers=digicow_headers, json={}, timeout=60)
        assert r.status_code == 409, f"expected 409 got {r.status_code}: {r.text[:300]}"


# ---------- 5. Interrupted legacy run ----------
class TestLegacyRegistrationBlocked:
    """The pre-fix run's registry carries a call-time stamp and is immutable: its last hold is
    ARTIFACT_REGISTRATION_CHANGED, which is a refusal (closed), not a retryable interruption."""

    def test_summary_blocked_with_honest_reason(self, digicow_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_INTERRUPTED}", headers=digicow_headers, timeout=60)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body.get("lifecycle_state") == "Blocked", body.get("lifecycle_state")
        assert body.get("reason_code") == "ARTIFACT_REGISTRATION_CHANGED", body.get("reason_code")
        assert body.get("permitted_actions") == [], body.get("permitted_actions")

    def test_advance_refused_as_closed(self, digicow_headers):
        r = requests.post(f"{BASE_URL}/api/portal/commission/{REQ_INTERRUPTED}/advance",
                          headers=digicow_headers, json={}, timeout=LONG_TIMEOUT)
        assert r.status_code == 409, f"expected 409 closed, got {r.status_code}: {r.text[:400]}"
        assert "closed" in r.text


# ---------- 6. Delivery held honestly ----------
class TestDeliveryHeld:
    def test_delivery_held_custody_origin_unavailable(self, digicow_headers):
        idem = f"qa-delivery-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        body = {
            "artifact_ref": f"akki://artifact/DIGICOW/{REQ_READY}/qualified-units",
            "idempotency_key": idem,
        }
        r = requests.post(f"{BASE_URL}/api/portal/requests/{REQ_READY}/delivery",
                          headers=digicow_headers, json=body, timeout=LONG_TIMEOUT)
        assert r.status_code == 409, f"expected 409 got {r.status_code}: {r.text[:400]}"
        try:
            data = r.json()
        except Exception:
            # FastAPI may wrap in {"detail": {...}}
            pytest.fail(f"not JSON: {r.text[:400]}")
        # normalise detail wrapper
        payload = data.get("detail") if isinstance(data, dict) and "detail" in data else data
        if isinstance(payload, str):
            payload = data
        assert payload.get("outcome") == "held", f"outcome={payload.get('outcome')} full={payload}"
        assert payload.get("reason_code") == "CUSTODY_ORIGIN_UNAVAILABLE", f"reason_code={payload.get('reason_code')}"
        assert payload.get("delivery_verified") is False, payload
        reason_text = (payload.get("reason") or "").lower()
        assert "estate" in reason_text or "store" in reason_text, f"reason text lacks estate/store mention: {reason_text}"


# ---------- 7. Draft shaping negative paths ----------
class TestDraftShaping:
    def test_draft_flow_no_dispatch(self, digicow_headers):
        # warm draft
        body = {
            "objective_text": "M3 shaping smoke test — do not freeze",
            "operation": "processed_intelligence",
            "units": ["digicow_rds"],
            "bounds": {"max_records": 50, "max_seconds": 300},
            "reach": {"database": "digicow_live", "table": "training_questions"},
        }
        r = requests.post(f"{BASE_URL}/api/portal/commission/drafts", headers=digicow_headers, json=body, timeout=60)
        assert r.status_code == 201, f"draft create: {r.status_code} {r.text[:400]}"
        d = r.json()
        draft_id = d.get("draft_id") or d.get("id")
        assert draft_id, d
        feas = d.get("feasibility") or {}
        assert feas.get("verdict") == "warm", f"verdict={feas.get('verdict')}"
        assert d.get("freeze_ready") is True, d
        quote = d.get("quote") or {}
        assert str(quote.get("total")) == "0", f"quote total={quote}"

        # revise same draft with larger bounds
        body2 = dict(body)
        body2["draft_id"] = draft_id
        body2["bounds"] = {"max_records": 5000, "max_seconds": 300}
        r2 = requests.post(f"{BASE_URL}/api/portal/commission/drafts", headers=digicow_headers, json=body2, timeout=60)
        assert r2.status_code == 201, f"revise: {r2.status_code} {r2.text[:400]}"
        d2 = r2.json()
        assert d2.get("version") == 2, f"version={d2.get('version')}"
        versions = d2.get("versions") or []
        assert versions and versions[0].get("envelope", {}).get("bounds", {}).get("max_records") == 50, f"versions[0]={versions[0] if versions else None}"

        # unknown table
        body_bad = dict(body)
        body_bad["reach"] = {"database": "digicow_live", "table": "not_a_table"}
        r3 = requests.post(f"{BASE_URL}/api/portal/commission/drafts", headers=digicow_headers, json=body_bad, timeout=60)
        assert r3.status_code == 201, r3.text
        d3 = r3.json()
        feas3 = d3.get("feasibility") or {}
        assert feas3.get("verdict") == "unknown", f"verdict={feas3.get('verdict')}"
        assert feas3.get("reason_code") == "TABLE_NOT_CENSUSED", feas3
        assert d3.get("freeze_ready") is False, d3
        # freeze unknown draft -> 409
        did3 = d3.get("draft_id") or d3.get("id")
        rf = requests.post(f"{BASE_URL}/api/portal/commission/drafts/{did3}/freeze",
                           headers=digicow_headers, json={"idempotency_key": f"qa-nofreeze-{uuid.uuid4().hex[:8]}"}, timeout=60)
        assert rf.status_code == 409, f"freeze unknown: {rf.status_code} {rf.text[:200]}"

        # users table -> floor columns include email/mobile_number
        body_pii = dict(body)
        body_pii["reach"] = {"database": "digicow_live", "table": "users"}
        r4 = requests.post(f"{BASE_URL}/api/portal/commission/drafts", headers=digicow_headers, json=body_pii, timeout=60)
        assert r4.status_code == 201, r4.text
        d4 = r4.json()
        floor_cols = (((d4.get("feasibility") or {}).get("floor") or {}).get("columns")) or []
        assert "email" in floor_cols, f"floor cols={floor_cols}"
        assert "mobile_number" in floor_cols, f"floor cols={floor_cols}"

        # withdraw v2 draft
        rw = requests.post(f"{BASE_URL}/api/portal/commission/drafts/{draft_id}/withdraw",
                          headers=digicow_headers, json={}, timeout=60)
        assert rw.status_code == 200, f"withdraw: {rw.status_code} {rw.text[:200]}"
        wbody = rw.json()
        assert wbody.get("state") == "withdrawn", wbody
        rwf = requests.post(f"{BASE_URL}/api/portal/commission/drafts/{draft_id}/freeze",
                            headers=digicow_headers, json={"idempotency_key": f"qa-nofreeze-{uuid.uuid4().hex[:8]}"}, timeout=60)
        assert rwf.status_code == 409, f"freeze withdrawn: {rwf.status_code}"


# ---------- 8. Tenant / role boundaries ----------
class TestBoundaries:
    def test_rms_analyst_run_view_404(self, rms_analyst_headers):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/run", headers=rms_analyst_headers, timeout=60)
        assert r.status_code == 404, f"expected 404 got {r.status_code}"

    def test_rms_analyst_draft_403(self, rms_analyst_headers):
        body = {
            "objective_text": "unauthorised",
            "operation": "processed_intelligence",
            "units": ["digicow_rds"],
            "bounds": {"max_records": 5, "max_seconds": 60},
            "reach": {"database": "digicow_live", "table": "training_questions"},
        }
        r = requests.post(f"{BASE_URL}/api/portal/commission/drafts", headers=rms_analyst_headers, json=body, timeout=60)
        assert r.status_code == 403, f"expected 403 got {r.status_code}: {r.text[:200]}"

    def test_anonymous_401(self):
        r = requests.get(f"{BASE_URL}/api/portal/requests/{REQ_READY}/run", timeout=30)
        assert r.status_code == 401, f"expected 401 got {r.status_code}"
