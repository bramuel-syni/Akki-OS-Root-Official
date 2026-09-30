"""Iteration 67 - Estate Intelligence report + M9 read-only endpoint tests.

Read-only: never POST valid job bodies to /jobs or /cancel.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")

RMS_OP = ("demo.operator@demo.rms.example.com", "demo-operator-pw")
RMS_ANALYST = ("demo.analyst@demo.rms.example.com", "demo-analyst-pw")
DIGI_OP = ("demo.operator@demo.digicow.example.com", "demo-digicow-operator-pw")

TIMEOUT = 120


def _login(email, pw):
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": pw}, timeout=TIMEOUT)
    assert r.status_code == 200, f"login {email} -> {r.status_code} {r.text[:200]}"
    tok = r.json().get("access_token")
    assert tok
    return {"Authorization": f"Bearer {tok}"}


@pytest.fixture(scope="module")
def rms_op_h():
    return _login(*RMS_OP)


@pytest.fixture(scope="module")
def rms_an_h():
    return _login(*RMS_ANALYST)


@pytest.fixture(scope="module")
def digi_op_h():
    return _login(*DIGI_OP)


# ---------------- Estate Intelligence ----------------
class TestEstateIntelligence:
    def test_anon_report(self):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/report", timeout=TIMEOUT)
        assert r.status_code == 401

    def test_rms_report(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/report", headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        body = r.json()
        assert "running" in body
        report = body.get("report")
        assert report, "report missing"
        assert report.get("report_version") == 2, f"report_version={report.get('report_version')}"
        assert report.get("job_id") == "eij-1b359b3cbd2e", f"job_id={report.get('job_id')}"

        # degradation
        deg = report.get("degradation")
        assert isinstance(deg, dict), "degradation missing"
        assert set(["mojibake", "placeholder", "truncation", "invalid_format", "whitespace"]).issubset(
            set((deg.get("kinds") or {}).keys())
        )
        assert "kinds_note" in deg
        assert isinstance(deg.get("dead_columns"), int)
        assert isinstance(deg.get("columns_measured"), int)
        assert "dead_column_share" in deg
        dbs = deg.get("databases")
        assert isinstance(dbs, list) and len(dbs) == 20, f"databases len={len(dbs) if isinstance(dbs, list) else 'n/a'}"
        for d in dbs:
            for k in ["degraded_ratio", "dead_columns", "columns", "stale_tables",
                       "write_span_days", "days_since_last_write", "growth", "schema_drift_tables"]:
                assert k in d, f"db missing key {k}: {d.keys()}"
            for gk in ["rows_delta", "bytes_delta", "tables_delta"]:
                assert gk in d["growth"], f"growth missing {gk}"
        tr = deg.get("trend")
        assert isinstance(tr, dict)
        assert tr.get("previous_job_id") == "eij-91933223a5b1"
        for k in ["deltas", "coverage_changed", "databases_grown", "databases_shrunk"]:
            assert k in tr, f"trend missing {k}"
        assert "trend_note" in deg

        # within_table_duplicates
        wtd = report.get("within_table_duplicates")
        assert isinstance(wtd, list) and len(wtd) <= 25
        for row in wtd:
            assert row.get("exact_duplicate_ratio", 0) >= 0.01 - 1e-9

        # data_products grain / licensable_units
        dps = report.get("data_products")
        assert isinstance(dps, list) and len(dps) > 0
        for dp in dps:
            assert isinstance(dp.get("grain"), dict), f"grain not dict: {dp.get('grain')}"
            lu = dp.get("licensable_units")
            assert isinstance(lu, list)
            for item in lu:
                assert isinstance(item, str), f"licensable_units item not string: {item!r}"

        # dossier
        dossier = report.get("dossier")
        assert isinstance(dossier, dict), "dossier missing"
        assert dossier.get("model_id") == "gpt-5-mini"
        assert "receipt_id" in dossier
        assert dossier.get("text")

    def test_rms_job_specific_report(self, rms_op_h):
        r = requests.get(
            f"{BASE_URL}/api/portal/census/estate-intelligence/jobs/eij-1b359b3cbd2e/report",
            headers=rms_op_h, timeout=TIMEOUT
        )
        assert r.status_code == 200
        rep = r.json().get("report") or r.json()
        # allow either wrapping
        if "report" in r.json():
            rep = r.json()["report"]
        assert rep.get("job_id") == "eij-1b359b3cbd2e"
        assert rep.get("report_version") == 2

    def test_jobs_list(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/jobs",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        body = r.json()
        jobs = body.get("jobs") if isinstance(body, dict) else body
        assert isinstance(jobs, list)
        eij = [j for j in jobs if str(j.get("job_id", "")).startswith("eij-")]
        assert len(eij) >= 2, f"eij jobs found={len(eij)}"

    def test_previous_job(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/jobs/eij-91933223a5b1",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        j = r.json()
        job = j.get("job") if isinstance(j, dict) and "job" in j else j
        assert job.get("status") in ("completed", "partial")
        assert job.get("report_ready") is True

    def test_unknown_job_404(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/jobs/eij-doesnotexist",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 404

    def test_digicow_report_null(self, digi_op_h):
        r = requests.get(f"{BASE_URL}/api/portal/census/estate-intelligence/report",
                         headers=digi_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json().get("report") is None

    def test_analyst_compose_forbidden(self, rms_an_h):
        r = requests.post(
            f"{BASE_URL}/api/portal/census/estate-intelligence/jobs/eij-1b359b3cbd2e/dossier",
            headers=rms_an_h, json={}, timeout=TIMEOUT
        )
        assert r.status_code == 403, f"expected 403, got {r.status_code} {r.text[:200]}"


# ---------------- M9 Training (read-only) ----------------
class TestM9:
    def test_anon(self):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs", timeout=TIMEOUT)
        assert r.status_code == 401

    def test_rms_jobs_list(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs", headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        body = r.json()
        jobs = body.get("jobs") if isinstance(body, dict) else body
        assert isinstance(jobs, list) and len(jobs) > 0
        ids = [j.get("job_id") for j in jobs]
        assert "m9j-f064ba2a4ef9" in ids
        assert "m9j-1e1b97ce8e1c" in ids
        hosts = body.get("hosts") if isinstance(body, dict) else None
        if hosts is not None:
            assert set(hosts) == {"akki-vm-ii", "akki-vm"}, f"hosts={hosts}"

    def test_completed_train_job(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs/m9j-f064ba2a4ef9",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        j = r.json()
        job = j.get("job") if isinstance(j, dict) and "job" in j else j
        assert job.get("status") == "completed", f"status={job.get('status')}"
        cert = job.get("run_certificate")
        assert isinstance(cert, dict), "run_certificate missing"
        moac = cert.get("moac")
        assert isinstance(moac, dict)
        assert "m_a_improvement" in moac
        assert "per_stratum" in cert  # per_stratum lives at run_certificate level

    def test_certificate_endpoint(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/certificates/m9j-f064ba2a4ef9",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()

    def test_compare_optimizers_ineligible(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs/m9j-1e1b97ce8e1c",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        j = r.json()
        job = j.get("job") if isinstance(j, dict) and "job" in j else j
        opt = job.get("optimizer_comparison")
        assert isinstance(opt, dict)
        assert opt.get("verdict") == "ineligible", f"verdict={opt.get('verdict')}"

    def test_unknown_job_404(self, rms_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs/notarealid",
                         headers=rms_op_h, timeout=TIMEOUT)
        assert r.status_code == 404

    def test_digicow_jobs_empty(self, digi_op_h):
        r = requests.get(f"{BASE_URL}/api/training/m9/jobs", headers=digi_op_h, timeout=TIMEOUT)
        assert r.status_code == 200
        body = r.json()
        jobs = body.get("jobs") if isinstance(body, dict) else body
        assert jobs == [], f"digicow jobs={jobs}"

    def test_invalid_phase_422(self, rms_op_h):
        r = requests.post(
            f"{BASE_URL}/api/training/m9/jobs",
            headers=rms_op_h,
            json={"phase": "bogus", "host": "akki-vm-ii"},
            timeout=TIMEOUT,
        )
        assert r.status_code == 422, f"expected 422 got {r.status_code} {r.text[:200]}"
