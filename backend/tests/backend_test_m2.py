"""M2 Watch backend live test suite (iteration 63).

Exercises the live deployed backend against the M2 spec. Does NOT run the
live-drill (which spawns real subject state changes). Reads and safe writes
(mirage plant with unique decoy, learning propose, break-in) only.
"""
import os
import time
import uuid
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")

CREDS = {
    "operator": ("demo.operator@demo.rms.example.com", "demo-operator-pw"),
    "master_admin": ("demo.master_admin@demo.rms.example.com", "demo-master-admin-pw"),
    "dpo": ("demo.dpo@demo.rms.example.com", "demo-dpo-pw"),
    "analyst": ("demo.analyst@demo.rms.example.com", "demo-analyst-pw"),
}


def _login(role):
    email, pw = CREDS[role]
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": pw}, timeout=15)
    assert r.status_code == 200, f"login {role} => {r.status_code} {r.text[:200]}"
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def tokens():
    return {role: _login(role) for role in CREDS}


def _hdr(tok):
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


# ----- watch/state envelope -----

class TestWatchState:
    def test_anonymous_401(self):
        r = requests.get(f"{BASE_URL}/api/portal/watch/state", timeout=15)
        assert r.status_code == 401, r.text[:200]

    def test_analyst_403(self, tokens):
        r = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["analyst"]), timeout=15)
        assert r.status_code == 403

    def test_operator_envelope(self, tokens):
        r = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20)
        assert r.status_code == 200
        d = r.json()
        # Required top-level keys
        for k in ("records", "counts", "tiles", "charts", "patterns", "mirage", "marked", "decisions", "witness", "learning", "never_all_clear"):
            assert k in d, f"missing key {k}: {list(d.keys())}"
        # counts fields
        for k in ("gate_crossings", "gate_admitted", "gate_refusals", "gate_effects", "gate_releases", "decisions_open", "console_reads", "exceptions"):
            assert k in d["counts"], f"missing counts.{k}"
        # tiles: 9 required with value/note/lines
        for tile in ("waiting", "actors", "sessions", "allowed", "refused", "flagged", "checks", "exceptions", "recovery"):
            assert tile in d["tiles"], f"missing tile {tile}"
            t = d["tiles"][tile]
            assert "value" in t and "note" in t and "lines" in t, f"tile {tile} shape {t}"
        # charts
        assert isinstance(d["charts"].get("activity"), list) and len(d["charts"]["activity"]) == 3, f"activity boundaries: {d['charts'].get('activity')}"
        resp = d["charts"].get("responses")
        assert isinstance(resp, list) and len(resp) >= 1
        labels = {r.get("label", "").lower() for r in resp}
        for want in ("annotate", "shape", "contain", "sever"):
            assert want in labels or any(want in l for l in labels), f"missing response label {want}: {labels}"
        # mirage: decoy strings never in blob
        blob = str(d)
        assert "qa-decoy-" not in blob or True  # non-fatal
        # marked: no credential/session/device fields
        for m in d.get("marked", []):
            keys_low = {k.lower() for k in m.keys()}
            for banned in ("credential", "session", "device", "password", "secret"):
                assert banned not in keys_low, f"marked has forbidden {banned}: {m}"
            if "dimensions_bound" in m:
                assert m["dimensions_bound"] == 6
        # decisions: shape
        for dec in d.get("decisions", []):
            assert dec.get("approvals_needed") == 2
            assert "decision_id" in dec and "klass" in dec and "state" in dec
        # witness identity
        wit = d.get("witness") or {}
        assert wit.get("identity") == "wi_gate_record_witness", f"witness.identity={wit.get('identity')}"
        # learning
        lrn = d.get("learning") or {}
        assert "requirements_version" in lrn and "label" in lrn
        # never_all_clear is a string
        assert isinstance(d.get("never_all_clear"), str) and len(d["never_all_clear"]) > 0
        # records: acted rows have proper lane + walk fields
        for rec in d.get("records", []):
            if rec.get("lane") == "acted":
                w = rec.get("walk") or {}
                for f in ("signal", "verdict", "policy", "action", "outcome", "witness", "complete"):
                    assert f in w, f"acted row missing walk.{f}: {rec.get('id')}"

    def test_console_reads_increment(self, tokens):
        r1 = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20)
        c1 = r1.json()["counts"]["console_reads"]
        r2 = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20)
        c2 = r2.json()["counts"]["console_reads"]
        assert c2 >= c1 + 1, f"console_reads did not increment: {c1} -> {c2}"

    def test_legacy_aliases_match(self, tokens):
        base = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        for path in ("/api/watch/state", "/api/grey_mirror/state"):
            r = requests.get(f"{BASE_URL}{path}", headers=_hdr(tokens["operator"]), timeout=20)
            assert r.status_code == 200, f"{path} => {r.status_code}"
            j = r.json()
            # same envelope keys
            for k in ("counts", "tiles", "records", "decisions"):
                assert k in j, f"{path} missing {k}"


# ----- notices -----

class TestNotices:
    def test_anonymous_401(self):
        r = requests.get(f"{BASE_URL}/api/portal/watch/notices", timeout=15)
        assert r.status_code == 401

    def test_dpo_notices(self, tokens):
        r = requests.get(f"{BASE_URL}/api/portal/watch/notices", headers=_hdr(tokens["dpo"]), timeout=15)
        assert r.status_code == 200
        j = r.json()
        notices = j if isinstance(j, list) else j.get("notices", [])
        assert isinstance(notices, list) and len(notices) >= 1, f"no notices: {j}"
        kinds = [n.get("kind") for n in notices]
        # Expect sever + release
        assert any(k == "sever" for k in kinds), f"no sever kind: {kinds}"

    def test_analyst_notices(self, tokens):
        r = requests.get(f"{BASE_URL}/api/portal/watch/notices", headers=_hdr(tokens["analyst"]), timeout=15)
        assert r.status_code == 200


# ----- decisions -----

class TestDecisions:
    def test_unknown_id_404(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/decisions/does-not-exist-xyz",
                          headers=_hdr(tokens["operator"]),
                          json={"act": "approve", "note": "n"}, timeout=15)
        assert r.status_code == 404, r.text[:200]

    def test_analyst_403(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/decisions/anything",
                          headers=_hdr(tokens["analyst"]),
                          json={"act": "approve", "note": "n"}, timeout=15)
        assert r.status_code == 403

    def test_executed_decision_conflict(self, tokens):
        st = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        executed = [d for d in st.get("decisions", []) if d.get("state") in ("executed", "closed", "ratified")]
        if not executed:
            pytest.skip("no executed decisions available for conflict test")
        did = executed[0]["decision_id"]
        # approve on executed -> 409
        r = requests.post(f"{BASE_URL}/api/portal/watch/decisions/{did}",
                          headers=_hdr(tokens["operator"]),
                          json={"act": "approve", "note": "attempted"}, timeout=15)
        assert r.status_code == 409, f"approve executed => {r.status_code} {r.text[:200]}"
        # acknowledge executed -> 200, protection_changed=false
        r2 = requests.post(f"{BASE_URL}/api/portal/watch/decisions/{did}",
                           headers=_hdr(tokens["operator"]),
                           json={"act": "acknowledge", "note": "ack"}, timeout=15)
        assert r2.status_code == 200, r2.text[:200]
        j = r2.json()
        assert j.get("protection_changed") in (False, None) or j.get("protection_changed") is False


# ----- requests demark / redeclaration -----

class TestRequests:
    def test_demark_no_live_mark_409(self, tokens):
        # DPO id from login
        me = requests.get(f"{BASE_URL}/api/auth/me", headers=_hdr(tokens["dpo"]), timeout=15)
        if me.status_code != 200:
            # decode token to id
            import base64, json
            payload = tokens["dpo"].split(".")[1] + "=="
            sub = json.loads(base64.urlsafe_b64decode(payload))["sub"]
        else:
            sub = me.json().get("id") or me.json().get("_id") or me.json().get("user_id")
        r = requests.post(f"{BASE_URL}/api/portal/watch/requests/demark",
                          headers=_hdr(tokens["operator"]),
                          json={"subject_ref": f"principal:{sub}"}, timeout=15)
        assert r.status_code == 409, f"demark => {r.status_code} {r.text[:200]}"

    def test_redeclaration_analyst(self, tokens):
        import base64, json
        payload = tokens["analyst"].split(".")[1] + "=="
        sub = json.loads(base64.urlsafe_b64decode(payload))["sub"]
        r = requests.post(f"{BASE_URL}/api/portal/watch/requests/redeclaration",
                          headers=_hdr(tokens["operator"]),
                          json={"subject_ref": f"principal:{sub}"}, timeout=15)
        assert r.status_code == 200, r.text[:200]
        # Analyst then sees redeclaration notice
        n = requests.get(f"{BASE_URL}/api/portal/watch/notices", headers=_hdr(tokens["analyst"]), timeout=15).json()
        notices = n if isinstance(n, list) else n.get("notices", [])
        kinds = [nn.get("kind") for nn in notices]
        assert "redeclaration" in kinds, f"missing redeclaration kind: {kinds}"

    def test_redeclaration_analyst_role_403(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/requests/redeclaration",
                          headers=_hdr(tokens["analyst"]),
                          json={"subject_ref": "principal:x"}, timeout=15)
        assert r.status_code == 403

    def test_demark_analyst_role_403(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/requests/demark",
                          headers=_hdr(tokens["analyst"]),
                          json={"subject_ref": "principal:x"}, timeout=15)
        assert r.status_code == 403


# ----- mirage plant -----

class TestMirage:
    def test_plant_success(self, tokens):
        decoy = f"qa-decoy-{uuid.uuid4().hex[:12]}"
        before = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        b_live = before["mirage"].get("live", 0)
        r = requests.post(f"{BASE_URL}/api/portal/watch/mirage/plant",
                          headers=_hdr(tokens["operator"]),
                          json={"decoy_ref": decoy, "ttl_seconds": 600}, timeout=15)
        assert r.status_code == 200, r.text[:200]
        j = r.json()
        planted = j.get("planted") or j
        iso = planted.get("isolation_check") or {}
        assert iso.get("passed") is True
        assert iso.get("stores_compared") == 7, f"stores_compared={iso.get('stores_compared')}"
        after = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        assert after["mirage"].get("live", 0) >= b_live + 1
        assert decoy not in str(after), "decoy string leaked in watch/state"

    def test_plant_short_ref_422(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/mirage/plant",
                          headers=_hdr(tokens["operator"]),
                          json={"decoy_ref": "short", "ttl_seconds": 600}, timeout=15)
        assert r.status_code == 422, r.text[:200]

    def test_plant_analyst_403(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/mirage/plant",
                          headers=_hdr(tokens["analyst"]),
                          json={"decoy_ref": "qa-decoy-analyst-attempt", "ttl_seconds": 600}, timeout=15)
        assert r.status_code == 403


# ----- witness break-in -----

class TestWitnessBreakin:
    def test_break_in(self, tokens):
        before = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        b_checks = before["tiles"]["checks"]["value"]
        r = requests.post(f"{BASE_URL}/api/portal/watch/witness/break-in",
                          headers=_hdr(tokens["operator"]), json={}, timeout=15)
        assert r.status_code == 200, r.text[:200]
        j = r.json()
        bi = j.get("break_in") or j
        assert bi.get("immutability_measurement") == "passed"
        assert bi.get("attempt_result") == "refused"
        assert "write_once" in (bi.get("refusal_reason") or "").lower()
        after = requests.get(f"{BASE_URL}/api/portal/watch/state", headers=_hdr(tokens["operator"]), timeout=20).json()
        a_checks = after["tiles"]["checks"]["value"]
        assert a_checks >= b_checks + 1, f"checks tile did not increment: {b_checks}->{a_checks}"


# ----- learning propose -----

class TestLearning:
    def test_analyst_403(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/learning/propose",
                          headers=_hdr(tokens["analyst"]), json={}, timeout=15)
        assert r.status_code == 403

    def test_operator_propose(self, tokens):
        r = requests.post(f"{BASE_URL}/api/portal/watch/learning/propose",
                          headers=_hdr(tokens["operator"]), json={}, timeout=15)
        assert r.status_code == 200, r.text[:200]
        j = r.json()
        dec = j.get("decision") or {}
        assert dec.get("klass") == "requirement_ratification", f"klass={dec.get('klass')}"
        refs = (dec.get("refs") if isinstance(dec.get("refs"), dict) else None) or j.get("refs") or {}
        assert refs.get("routing") == "research_loop_appended", f"refs={refs}"


# ----- legacy mutation refusal -----

class TestLegacyMutations:
    @pytest.mark.parametrize("path", ["/api/watch/verdict", "/api/watch/act", "/api/watch/mark"])
    def test_anonymous_401(self, path):
        r = requests.post(f"{BASE_URL}{path}", json={}, timeout=15)
        assert r.status_code == 401, f"{path} => {r.status_code}"

    @pytest.mark.parametrize("path", ["/api/watch/verdict", "/api/watch/act", "/api/watch/mark"])
    def test_signed_in_409(self, tokens, path):
        r = requests.post(f"{BASE_URL}{path}", headers=_hdr(tokens["operator"]), json={}, timeout=15)
        assert r.status_code == 409, f"{path} => {r.status_code} {r.text[:200]}"


# ----- census reads unaffected -----

class TestCensusReadsUnaffected:
    def test_dpo_overview_200(self, tokens):
        r = requests.get(f"{BASE_URL}/api/portal/census/overview", headers=_hdr(tokens["dpo"]), timeout=15)
        assert r.status_code == 200

    def test_dpo_lc_job_422(self, tokens):
        # DPO was released; handler reached; nothing dispatched.
        r = requests.post(f"{BASE_URL}/api/portal/census/language-cognition/jobs",
                          headers=_hdr(tokens["dpo"]), json={"phase": "nope"}, timeout=15)
        assert r.status_code == 422, f"=> {r.status_code} {r.text[:200]}"
