"""
Backend tests for Train Models (training_lab/board) endpoints.
Scope limited per review request. At most ONE real LLM message call, ONE action call.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")

OPERATOR = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}
ANALYST = {"email": "demo.analyst@demo.rms.example.com", "password": "demo-analyst-pw"}

def _login(creds):
    r = requests.post(f"{BASE_URL}/api/auth/login", json=creds, timeout=20)
    if r.status_code != 200:
        pytest.skip(f"Login failed for {creds['email']}: {r.status_code} {r.text[:200]}")
    token = r.json().get("access_token")
    assert token, f"No access_token in response: {r.text[:200]}"
    return token


@pytest.fixture(scope="module")
def op_headers():
    return {"Authorization": f"Bearer {_login(OPERATOR)}"}


@pytest.fixture(scope="module")
def an_headers():
    return {"Authorization": f"Bearer {_login(ANALYST)}"}


@pytest.fixture(scope="module")
def created_runs():
    """Track shape-* runs we create so we can delete them at end."""
    runs = []
    yield runs
    # cleanup
    try:
        headers = {"Authorization": f"Bearer {_login(OPERATOR)}"}
    except Exception:
        return
    for rid in runs:
        try:
            requests.delete(f"{BASE_URL}/api/training/lab/board/{rid}", headers=headers, timeout=15)
        except Exception:
            pass


# ---------- Board GET ----------

class TestBoardGet:
    def test_anon_board_401(self):
        r = requests.get(f"{BASE_URL}/api/training/lab/board", timeout=15)
        assert r.status_code == 401, f"Expected 401, got {r.status_code}: {r.text[:200]}"

    def test_operator_board_200(self, op_headers):
        r = requests.get(f"{BASE_URL}/api/training/lab/board", headers=op_headers, timeout=20)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert "runs" in data and isinstance(data["runs"], list)
        assert "counts" in data
        assert data.get("training_authorized") is False
        runs = data["runs"]
        assert len(runs) >= 10, f"Expected many runs, got {len(runs)}"
        statuses = {r["status"] for r in runs}
        # Must have varied statuses
        for required in ["Shaping", "In Approval", "In service", "Refused", "Retired"]:
            assert required in statuses, f"Missing status {required}; got {statuses}"
        # Fields present on each run
        required_fields = {"run_id", "family", "name", "status", "objective", "messages",
                           "checks", "record_rows", "reflect_rows", "sources",
                           "eta", "meta", "deletable", "ready"}
        for run in runs:
            missing = required_fields - set(run.keys())
            assert not missing, f"Run {run.get('run_id')} missing: {missing}"
        # Check specific expected runs exist
        rids = {r["run_id"] for r in runs}
        assert "music-identification" in rids
        assert "reinforcement-lwg" in rids
        assert "m9j-74af7cef0a85" in rids
        # No raw run_id visible in display name/meta of recorded runs (m9j- / lcj- prefixes)
        for run in runs:
            rid = run["run_id"]
            if rid.startswith(("m9j-", "lcj-")):
                # name/meta shouldn't display the raw id
                nm = run.get("name") or ""
                meta = run.get("meta") or ""
                assert rid not in nm, f"Raw id {rid} appears in name '{nm}'"
                assert rid not in meta, f"Raw id {rid} appears in meta '{meta}'"

    def test_analyst_board_200(self, an_headers):
        r = requests.get(f"{BASE_URL}/api/training/lab/board", headers=an_headers, timeout=20)
        assert r.status_code == 200, r.text[:300]


# ---------- Analyst forbidden on writes ----------

class TestAnalystReadOnly:
    def test_analyst_cannot_create(self, an_headers):
        r = requests.post(f"{BASE_URL}/api/training/lab/board/new", json={}, headers=an_headers, timeout=15)
        assert r.status_code == 403, f"Expected 403, got {r.status_code}: {r.text[:200]}"

    def test_analyst_cannot_message(self, an_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/m9j-74af7cef0a85/messages",
            json={"text": "hi"}, headers=an_headers, timeout=15,
        )
        assert r.status_code == 403, f"Expected 403, got {r.status_code}: {r.text[:200]}"


# ---------- New / Delete ----------

class TestNewDelete:
    def test_create_blank_and_delete(self, op_headers, created_runs):
        r = requests.post(f"{BASE_URL}/api/training/lab/board/new", json={}, headers=op_headers, timeout=20)
        assert r.status_code == 201, r.text[:300]
        data = r.json()
        rid = data.get("run_id")
        assert rid and rid.startswith("shape-"), f"Bad run_id: {rid}"
        created_runs.append(rid)
        assert data.get("status") == "Shaping"
        assert data.get("name") == "New model"
        # confirm board shows it with opening message
        board = requests.get(f"{BASE_URL}/api/training/lab/board", headers=op_headers, timeout=20).json()
        match = [r for r in board["runs"] if r["run_id"] == rid]
        assert match, "New run not visible on board"
        run = match[0]
        assert run["deletable"] is True
        msgs = run.get("messages") or []
        assert any(m.get("origin") == "conversation" for m in msgs), f"No conversation opener: {msgs}"
        # delete
        d = requests.delete(f"{BASE_URL}/api/training/lab/board/{rid}", headers=op_headers, timeout=15)
        assert d.status_code == 204, f"Expected 204, got {d.status_code}: {d.text[:200]}"
        created_runs.remove(rid)
        # confirm gone
        board2 = requests.get(f"{BASE_URL}/api/training/lab/board", headers=op_headers, timeout=20).json()
        assert not any(r["run_id"] == rid for r in board2["runs"])

    def test_delete_recorded_run_409(self, op_headers):
        r = requests.delete(f"{BASE_URL}/api/training/lab/board/m9j-74af7cef0a85", headers=op_headers, timeout=15)
        assert r.status_code == 409, f"Expected 409, got {r.status_code}: {r.text[:200]}"

    def test_next_version_from_served(self, op_headers, created_runs):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/new",
            json={"from_run": "m9j-74af7cef0a85", "mode": "next_version"},
            headers=op_headers, timeout=20,
        )
        assert r.status_code == 201, r.text[:300]
        data = r.json()
        rid = data["run_id"]
        created_runs.append(rid)
        assert data["status"] == "Shaping"
        name = data.get("name", "")
        assert "v2" in name.lower() or "v2" in name, f"Expected version-2 name, got: {name}"
        assert "Language identification" in name, f"Name mismatch: {name}"
        # lineage/opening message mentions parent untouched
        board = requests.get(f"{BASE_URL}/api/training/lab/board", headers=op_headers, timeout=20).json()
        run = next(r for r in board["runs"] if r["run_id"] == rid)
        msg_text = " ".join([(m.get("text") or "") for m in (run.get("messages") or [])]).lower()
        assert "untouched" in msg_text or "parent" in msg_text or "still" in msg_text or "unchanged" in msg_text, \
            f"Opener did not mention parent untouched: {msg_text[:300]}"

    def test_mode_new_from_run_422(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/new",
            json={"from_run": "m9j-74af7cef0a85", "mode": "new"},
            headers=op_headers, timeout=15,
        )
        assert r.status_code == 422, f"Expected 422, got {r.status_code}: {r.text[:200]}"

    def test_from_run_unknown_404(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/new",
            json={"from_run": "nope-does-not-exist", "mode": "next_version"},
            headers=op_headers, timeout=15,
        )
        assert r.status_code == 404, f"Expected 404, got {r.status_code}: {r.text[:200]}"


# ---------- Actions (bounded, SAFE ones only) ----------

class TestBoardActions:
    def test_use_baseline_music(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/music-identification/actions",
            json={"action": "use_baseline", "value": "learned"},
            headers=op_headers, timeout=25,
        )
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        msgs = data.get("messages") or []
        assert len(msgs) >= 2, f"Expected 2 messages, got {msgs}"
        # First: user decision
        dec = msgs[0]
        assert dec.get("role") == "user"
        # second: akki note
        akki = msgs[1]
        assert "starting point" in (akki.get("text") or "").lower() or "recorded" in (akki.get("text") or "").lower()

    def test_record_training_request_lwg(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/reinforcement-lwg/actions",
            json={"action": "record_training_request"},
            headers=op_headers, timeout=25,
        )
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert data.get("training_started") is False
        msgs = data.get("messages") or []
        txt = " ".join([(m.get("text") or "") for m in msgs]).lower()
        assert "held" in txt or "nothing has started" in txt or "stays" in txt, f"Unexpected text: {txt[:300]}"

    def test_retire_served_refused(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/m9j-74af7cef0a85/actions",
            json={"action": "retire"},
            headers=op_headers, timeout=25,
        )
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        msgs = data.get("messages") or []
        # Expect an akki note that starts with 'Not done'
        texts = [(m.get("text") or "") for m in msgs]
        assert any(t.strip().lower().startswith("not done") for t in texts), f"Expected 'Not done' refusal: {texts}"

    def test_unknown_run_404(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/nope-xxxx/actions",
            json={"action": "use_baseline", "value": "learned"},
            headers=op_headers, timeout=15,
        )
        assert r.status_code == 404, f"Expected 404, got {r.status_code}: {r.text[:200]}"

    def test_invalid_action_422(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/music-identification/actions",
            json={"action": "does_not_exist"},
            headers=op_headers, timeout=15,
        )
        assert r.status_code == 422, f"Expected 422, got {r.status_code}: {r.text[:200]}"


# ---------- Real LLM message (ONE call) ----------

class TestConversation:
    def test_message_grounded(self, op_headers):
        r = requests.post(
            f"{BASE_URL}/api/training/lab/board/m9j-74af7cef0a85/messages",
            json={"text": "Which language carried the smallest margin on this run?"},
            headers=op_headers, timeout=90,
        )
        assert r.status_code == 200, r.text[:400]
        data = r.json()
        msgs = data.get("messages") or []
        assert len(msgs) >= 2, f"Expected [user, akki], got {msgs}"
        akki = msgs[-1]
        assert akki.get("status") != "unavailable", f"Model unavailable: {akki}"
        assert akki.get("action") in (None, "", {}), f"Action should be null: {akki.get('action')}"
        text = (akki.get("text") or "").lower()
        # grounded reference - Kikamba is the expected answer
        assert "kikamba" in text or "91.3" in text, f"Not grounded; akki said: {text[:400]}"
        # think steps present
        think = akki.get("think") or []
        assert isinstance(think, list) and len(think) > 0, f"No think steps: {akki}"
