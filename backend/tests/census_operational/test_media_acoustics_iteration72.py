"""Backend tests for media acoustics (iteration 72).

Covers:
  - /api/media/acoustics/register (auth required, structure)
  - /api/media/acoustics (list, tenant isolation)
  - /api/media/files/{id}/acoustics GET (profile + privacy fields)
  - POST /api/media/files/{id}/acoustics (queue + replay + worker)
  - POST /api/media/acoustics/batch (mixed types + validation)
  - /api/media/acoustics/patterns (aggregation)
  - Regression: GET /api/media/config, /api/media/files, download, assessments.
"""
import os
import time
import uuid
import pytest
import requests

def _read_env_url():
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v
    try:
        with open("/app/frontend/.env") as f:
            for ln in f:
                if ln.startswith("REACT_APP_BACKEND_URL="):
                    return ln.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


BASE_URL = _read_env_url().rstrip("/")
API = BASE_URL + "/api"

RMS_OP = ("demo.operator@demo.rms.example.com", "demo-operator-pw")
RMS_AN = ("demo.analyst@demo.rms.example.com", "demo-analyst-pw")
DIGICOW_OP = ("demo.operator@demo.digicow.example.com", "demo-digicow-operator-pw")

MEASURED_RMS_FILE = "22d381189c76471ea0ad91c034858300"


def _login(email, pw):
    r = requests.post(f"{API}/auth/login", json={"email": email, "password": pw}, timeout=30)
    assert r.status_code == 200, f"login failed {email}: {r.status_code} {r.text[:200]}"
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def rms_op_token():
    return _login(*RMS_OP)


@pytest.fixture(scope="module")
def rms_an_token():
    return _login(*RMS_AN)


@pytest.fixture(scope="module")
def digicow_op_token():
    return _login(*DIGICOW_OP)


def H(tok):
    return {"Authorization": f"Bearer {tok}"}


# ---------- register ----------
class TestAcousticRegister:
    def test_anonymous_401(self):
        r = requests.get(f"{API}/media/acoustics/register", timeout=15)
        assert r.status_code == 401

    def test_register_structure(self, rms_op_token):
        r = requests.get(f"{API}/media/acoustics/register", headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        assert d.get("profile_version") == "measured_dsp_v1"
        obs = d.get("observables")
        assert isinstance(obs, list) and len(obs) >= 55, f"observables count={len(obs) if obs else 0}"
        chains_seen = set()
        for o in obs:
            for k in ("chain", "key", "label", "unit", "method"):
                assert k in o, f"missing {k} in {o}"
            chains_seen.add(o["chain"])
        assert chains_seen == {"wave", "frequency", "tone", "energy", "timbre", "channel"}, chains_seen
        assert set(d.get("classes", [])) == {"speech", "music", "mixed", "noise", "silence"}
        assert set(d.get("channel_conditions", [])) == {"field", "studio", "telephone_band"}
        backends = d.get("backends")
        assert isinstance(backends, list) and len(backends) == 3
        for b in backends:
            assert b.get("state") == "ratified", b


# ---------- list ----------
class TestAcousticList:
    def test_list_rms(self, rms_op_token):
        r = requests.get(f"{API}/media/acoustics", headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200
        meas = r.json().get("measurements", [])
        measured = [m for m in meas if m.get("status") == "measured"]
        assert len(measured) >= 5, f"expected >=5 measured, got {len(measured)}"
        music = [m for m in measured if m.get("reads_as") == "music"]
        assert len(music) >= 5, f"expected music reads_as, got {[m.get('reads_as') for m in measured]}"
        for m in measured:
            for k in ("file_id", "status", "reads_as", "confidence", "channel_condition",
                      "profile_version", "measured_at"):
                assert k in m, f"missing {k} in summary"
            assert isinstance(m["channel_condition"], str) and m["channel_condition"], \
                f"channel_condition not string: {m}"

    def test_tenant_isolation_list(self, digicow_op_token):
        r = requests.get(f"{API}/media/acoustics", headers=H(digicow_op_token), timeout=30)
        assert r.status_code == 200
        meas = r.json().get("measurements", [])
        ids = [m.get("file_id") for m in meas]
        assert MEASURED_RMS_FILE not in ids


# ---------- profile ----------
class TestAcousticProfile:
    def test_measured_profile(self, rms_op_token):
        r = requests.get(f"{API}/media/files/{MEASURED_RMS_FILE}/acoustics",
                         headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        f = d.get("file")
        assert f and (f.get("file_id") == MEASURED_RMS_FILE or f.get("id") == MEASURED_RMS_FILE)
        # Privacy fields must not be exposed
        for forbidden in ("storage_path", "upload_key", "lease_token", "requested_by"):
            assert forbidden not in f, f"leaked {forbidden}"
        m = d.get("measurement")
        assert m and m.get("status") == "measured"
        prof = m.get("profile")
        assert prof, "no profile"
        obs = prof.get("observables", {})
        for chain in ("wave", "frequency", "tone", "energy", "timbre", "channel"):
            assert chain in obs, f"missing chain {chain}"
        sig = prof.get("signature") or m.get("signature")
        if sig is None:
            # signature may live at top level of measurement
            sig = m.get("signature")
        assert sig, "no signature"
        for k in ("reads_as", "confidence", "window_shares", "timeline"):
            assert k in sig, f"missing signature.{k}"
        tl = sig["timeline"]
        assert isinstance(tl, list) and len(tl) > 0
        for w in tl:
            for k in ("start_s", "end_s", "reads_as", "confidence", "scores", "cues"):
                assert k in w, f"timeline window missing {k}"
        assert "compute_seconds" in m or "compute_seconds" in prof
        assert "frames" in m or "frames" in prof

    def test_unknown_file_404(self, rms_op_token):
        r = requests.get(f"{API}/media/files/{uuid.uuid4().hex}/acoustics",
                         headers=H(rms_op_token), timeout=30)
        assert r.status_code == 404

    def test_tenant_isolation_profile(self, digicow_op_token):
        r = requests.get(f"{API}/media/files/{MEASURED_RMS_FILE}/acoustics",
                         headers=H(digicow_op_token), timeout=30)
        assert r.status_code == 404


# ---------- helpers ----------
def _find_unmeasured_audio(token):
    r = requests.get(f"{API}/media/files", params={"kind": "audio"},
                     headers=H(token), timeout=30)
    assert r.status_code == 200, r.text[:300]
    files = r.json().get("files", [])
    files = [f for f in files if f.get("kind") == "audio"
             and f.get("status") == "available"
             and not f.get("is_deleted")]
    r2 = requests.get(f"{API}/media/acoustics", headers=H(token), timeout=30)
    measured_ids = {m["file_id"] for m in r2.json().get("measurements", [])}
    for f in files:
        fid = f.get("file_id") or f.get("id")
        if fid and fid not in measured_ids:
            f["id"] = fid
            return f
    return None


def _find_non_audio_file(token):
    r = requests.get(f"{API}/media/files", headers=H(token), timeout=30)
    files = r.json().get("files", [])
    for f in files:
        if f.get("kind") != "audio" and f.get("status") == "available" and not f.get("is_deleted"):
            f["id"] = f.get("file_id") or f.get("id")
            return f
    return None


# ---------- unmeasured + request ----------
class TestAcousticRequest:
    def test_get_unmeasured_404(self, rms_op_token):
        f = _find_unmeasured_audio(rms_op_token)
        if not f:
            pytest.skip("no unmeasured audio file available")
        r = requests.get(f"{API}/media/files/{f['id']}/acoustics",
                         headers=H(rms_op_token), timeout=30)
        assert r.status_code == 404
        assert "not been measured" in r.text.lower()

    def test_analyst_forbidden(self, rms_an_token, rms_op_token):
        f = _find_unmeasured_audio(rms_op_token)
        if not f:
            # analyst 403 can be checked on any audio file (POST should still be forbidden)
            r0 = requests.get(f"{API}/media/files", params={"kind": "audio"},
                              headers=H(rms_an_token), timeout=30)
            files = r0.json().get("files", [])
            if not files:
                pytest.skip("no audio file available")
            fid = files[0].get("file_id") or files[0].get("id")
        else:
            fid = f["id"]
        r = requests.post(f"{API}/media/files/{fid}/acoustics",
                          headers=H(rms_an_token), timeout=30)
        assert r.status_code == 403, f"got {r.status_code}: {r.text[:200]}"

    def test_anonymous_forbidden(self, rms_op_token):
        f = _find_unmeasured_audio(rms_op_token) or {"id": MEASURED_RMS_FILE}
        r = requests.post(f"{API}/media/files/{f['id']}/acoustics", timeout=15)
        assert r.status_code == 401

    def test_non_audio_422(self, rms_op_token):
        nf = _find_non_audio_file(rms_op_token)
        if not nf:
            pytest.skip("no non-audio file available")
        r = requests.post(f"{API}/media/files/{nf['id']}/acoustics",
                          headers=H(rms_op_token), timeout=30)
        assert r.status_code == 422, f"got {r.status_code}: {r.text[:200]}"
        assert "audio" in r.text.lower()

    def test_queue_replay_and_measurement(self, rms_op_token):
        f = _find_unmeasured_audio(rms_op_token)
        if not f:
            pytest.skip("no unmeasured audio file available to request")
        fid = f["id"]
        r1 = requests.post(f"{API}/media/files/{fid}/acoustics",
                           headers=H(rms_op_token), timeout=30)
        assert r1.status_code == 202, r1.text[:300]
        d1 = r1.json()
        assert d1.get("created") is True
        assert d1["measurement"]["status"] in ("queued", "measuring", "measured")

        # replay
        r2 = requests.post(f"{API}/media/files/{fid}/acoustics",
                           headers=H(rms_op_token), timeout=30)
        assert r2.status_code == 202
        assert r2.json().get("created") is False

        # poll
        deadline = time.time() + 150
        status = None
        while time.time() < deadline:
            r = requests.get(f"{API}/media/files/{fid}/acoustics",
                             headers=H(rms_op_token), timeout=30)
            if r.status_code == 200:
                status = r.json().get("measurement", {}).get("status")
                if status == "measured":
                    break
                if status == "failed":
                    pytest.fail(f"measurement failed: {r.json().get('measurement')}")
            time.sleep(5)
        assert status == "measured", f"status={status} after 150s"
        prof_r = requests.get(f"{API}/media/files/{fid}/acoustics",
                              headers=H(rms_op_token), timeout=30).json()
        meas = prof_r["measurement"]
        assert meas.get("profile")

        # repost → created=false, still measured, no re-queue
        r3 = requests.post(f"{API}/media/files/{fid}/acoustics",
                           headers=H(rms_op_token), timeout=30)
        assert r3.status_code == 202
        d3 = r3.json()
        assert d3.get("created") is False
        assert d3["measurement"]["status"] == "measured"


# ---------- batch ----------
class TestAcousticBatch:
    def test_empty_422(self, rms_op_token):
        r = requests.post(f"{API}/media/acoustics/batch",
                          headers=H(rms_op_token), json={"file_ids": []}, timeout=30)
        assert r.status_code == 422

    def test_mixed_batch(self, rms_op_token):
        # pick one audio (any) + one non-audio
        r0 = requests.get(f"{API}/media/files", headers=H(rms_op_token), timeout=30)
        files = r0.json().get("files", [])
        audio = next((f for f in files if f.get("kind") == "audio"
                      and f.get("status") == "available" and not f.get("is_deleted")), None)
        nonaud = next((f for f in files if f.get("kind") != "audio"
                       and f.get("status") == "available" and not f.get("is_deleted")), None)
        if not (audio and nonaud):
            pytest.skip("need both audio and non-audio file")
        aid = audio.get("file_id") or audio.get("id")
        nid = nonaud.get("file_id") or nonaud.get("id")
        r = requests.post(f"{API}/media/acoustics/batch",
                          headers=H(rms_op_token),
                          json={"file_ids": [aid, nid]}, timeout=30)
        assert r.status_code == 202, r.text[:300]
        d = r.json()
        meas = d.get("measurements", [])
        skipped = d.get("skipped", [])
        assert any(m.get("file_id") == aid for m in meas), f"audio missing: {meas}"
        assert any(s.get("file_id") == nid and s.get("reason") for s in skipped), \
            f"non-audio not skipped: {skipped}"


# ---------- patterns ----------
class TestAcousticPatterns:
    def test_patterns(self, rms_op_token):
        r = requests.get(f"{API}/media/acoustics/patterns",
                         headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        assert d.get("measured_files", 0) >= 5
        classes = d.get("classes", [])
        assert isinstance(classes, list) and len(classes) >= 1
        for cl in classes:
            assert "reads_as" in cl and "file_count" in cl
            assert isinstance(cl.get("files"), list)
            if cl["files"]:
                for fe in cl["files"]:
                    for k in ("file_id", "title", "confidence"):
                        assert k in fe
                    assert "human_label" in fe
            for ob in cl.get("observables", []):
                for k in ("key", "label", "unit", "n", "median", "p10", "p90"):
                    assert k in ob
        hr = d.get("human_review", {})
        for k in ("reviewed_files", "agreements", "disagreements"):
            assert k in hr
        assert "most_separating" in d and isinstance(d["most_separating"], list)
        assert isinstance(d.get("method"), str) and d["method"]


# ---------- regression ----------
class TestRegression:
    def test_config(self, rms_op_token):
        r = requests.get(f"{API}/media/config", headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200

    def test_files(self, rms_op_token):
        r = requests.get(f"{API}/media/files", headers=H(rms_op_token), timeout=30)
        assert r.status_code == 200
        assert "files" in r.json()

    def test_download(self, rms_op_token):
        r = requests.get(f"{API}/media/files/{MEASURED_RMS_FILE}/download",
                         headers=H(rms_op_token), timeout=60, allow_redirects=True)
        assert r.status_code == 200
        assert len(r.content) > 0

    def test_assessment(self, rms_op_token):
        idem = f"test-iter72-{uuid.uuid4().hex}"
        # Use an available audio for assessment
        r0 = requests.get(f"{API}/media/files", params={"kind": "audio"},
                          headers=H(rms_op_token), timeout=30)
        files = [f for f in r0.json().get("files", [])
                 if f.get("kind") == "audio" and f.get("status") == "available"
                 and not f.get("is_deleted")]
        if not files:
            pytest.skip("no audio file for assessment")
        fid = files[0].get("file_id") or files[0].get("id")
        r = requests.post(f"{API}/media/assessments",
                          headers={**H(rms_op_token), "Idempotency-Key": idem},
                          json={"title": "iter72 test", "file_ids": [fid]}, timeout=60)
        assert r.status_code == 201, f"{r.status_code}: {r.text[:300]}"
