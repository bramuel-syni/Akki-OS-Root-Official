"""Iteration 82: RMS whole-estate Monte Carlo forecast report + release artifacts regression.

Scope (per review_request):
  1. /api/portal/census/estate-intelligence/report must expose stores.content_forecast with
     all keys and internal consistency (bounds, measured/forecast split, basis sums, sort order).
  2. /api/studio/commissions/com-1f3a3606e140 must reflect v7 released frontier build (read-only).
  3. Static downloads: 6 files (3 dated + 3 unversioned) match bytes/sha256 from manifest,
     each opens with python-docx / python-pptx / openpyxl.
  4. Document content: DOCX forecast total, heading order, no unresolved {Fxxx} tokens, thousands
     separators; PPTX exec summary on slide 2 with total; XLSX sheets + decision D0 + 2024offairrecs row.

Runs serially (-n 0) via pytest.ini default; no POST to /studio/producers or /revise or /build.
"""
import hashlib
import io
import json
import os
import re
import pytest
import requests


def _load_base_url():
    url = os.environ.get("REACT_APP_BACKEND_URL")
    if not url:
        # Read from frontend/.env since backend pytest env doesn't inherit it
        try:
            with open("/app/frontend/.env") as f:
                for line in f:
                    if line.startswith("REACT_APP_BACKEND_URL="):
                        url = line.split("=", 1)[1].strip()
                        break
        except FileNotFoundError:
            pass
    assert url, "REACT_APP_BACKEND_URL not configured"
    return url.rstrip("/")


BASE_URL = _load_base_url()
MANIFEST_PATH = "/app/assessment_workspace/deliverables/estate_forecast_20261003/finalized_release_manifest.json"
COMMISSION_ID = "com-1f3a3606e140"
BUILD_ID = "bld-e51ed4034736"

RMS_EMAIL = "demo.operator@demo.rms.example.com"
RMS_PW = "demo-operator-pw"


# ----- Shared fixtures -----
@pytest.fixture(scope="session")
def manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def auth_token():
    r = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": RMS_EMAIL, "password": RMS_PW},
        timeout=30,
    )
    if r.status_code != 200:
        pytest.skip(f"RMS login failed {r.status_code}: {r.text[:200]}")
    tok = r.json().get("access_token")
    assert tok, f"access_token missing from login response: {r.json()}"
    return tok


@pytest.fixture(scope="session")
def report(auth_token):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/estate-intelligence/report",
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=120,
    )
    assert r.status_code == 200, f"report fetch {r.status_code}: {r.text[:300]}"
    body = r.json()
    assert "tenant_id" in body and "report" in body and "running" in body, f"shape: {list(body)}"
    return body["report"]


# ===== 1. Estate forecast report =====
class TestEstateForecastReport:
    def test_content_forecast_present(self, report):
        stores = report.get("stores", {})
        assert "content_total" in stores, "regression: content_total missing"
        assert "content_forecast" in stores, "content_forecast missing"
        cf = stores["content_forecast"]
        required = {"simulations", "strata", "donors", "estate", "by_store", "by_basis",
                    "measured_share_of_hours", "forecast_share_of_hours", "sources", "folders", "method"}
        missing = required - set(cf.keys())
        assert not missing, f"missing keys: {missing}"

    def test_estate_hours_bounds_and_subassets(self, report):
        est = report["stores"]["content_forecast"]["estate"]
        h = est["hours"]
        assert h["lo"] <= h["est"] <= h["hi"], f"hours bounds violated: {h}"
        assert "speech" in est and "music" in est, f"missing speech/music: {list(est)}"

    def test_by_basis_sums_and_shares(self, report):
        cf = report["stores"]["content_forecast"]
        est = cf["estate"]
        by_basis = cf["by_basis"]
        # by_basis is a dict keyed by basis name
        if isinstance(by_basis, list):
            bases = {row["basis"]: row for row in by_basis}
            rows = by_basis
        else:
            bases = by_basis
            rows = list(by_basis.values())
        assert "measured" in bases, f"basis 'measured' missing from {list(bases)}"
        assert "forecast_denied" in bases, f"basis 'forecast_denied' missing from {list(bases)}"
        total_hours = sum(r["hours"]["est"] for r in rows)
        assert abs(total_hours - est["hours"]["est"]) / max(est["hours"]["est"], 1) <= 0.05, \
            f"by_basis hours sum {total_hours} not within 5% of estate.hours.est {est['hours']['est']}"
        total_files = sum(r["files"] for r in rows)
        assert total_files == est["files"], f"files sum {total_files} != estate.files {est['files']}"
        ms = cf["measured_share_of_hours"]
        fs = cf["forecast_share_of_hours"]
        assert 0 < ms < 1, f"measured_share_of_hours out of range: {ms}"
        assert 0 < fs < 1, f"forecast_share_of_hours out of range: {fs}"

    def test_sources_basis_and_bounds(self, report):
        sources = report["stores"]["content_forecast"]["sources"]
        valid_bases = {"measured", "forecast", "mixed"}
        for row in sources:
            assert row["basis"] in valid_bases, f"bad basis {row.get('basis')} in {row}"
            h = row["hours"]
            assert h["lo"] <= h["est"] <= h["hi"], f"bounds violated for source {row.get('name')}: {h}"
        # denied-access forecast sources
        forecast_rows = [r for r in sources if r["basis"] == "forecast"]
        assert forecast_rows, "no forecast-basis sources found (expected denied buckets)"
        for r in forecast_rows:
            assert r["hours"]["est"] > 0, f"forecast source with zero hours: {r.get('name')}"

    def test_folders_sorted_descending(self, report):
        folders = report["stores"]["content_forecast"]["folders"]
        est_hours = [f["hours"]["est"] for f in folders]
        assert est_hours == sorted(est_hours, reverse=True), "folders not sorted by hours.est desc"


# ===== 2. Commission state (read-only) =====
class TestCommissionState:
    def test_commission_v7_released(self, auth_token):
        r = requests.get(
            f"{BASE_URL}/api/studio/commissions/{COMMISSION_ID}",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=60,
        )
        assert r.status_code == 200, f"{r.status_code}: {r.text[:300]}"
        body = r.json()
        assert "tenant_id" in body and "commission" in body, f"shape: {list(body)}"
        c = body["commission"]
        assert c["current_content_version"] == 7, f"version {c.get('current_content_version')}"
        assert c["release"]["state"] == "clear", f"release state {c['release'].get('state')}"
        builds = c.get("builds", [])
        assert builds, "no builds in commission"
        last = builds[-1]
        assert last["build_id"] == BUILD_ID, f"last build {last.get('build_id')} != {BUILD_ID}"
        assert last["status"] == "released", f"last build status {last.get('status')}"
        assert last["qa"]["status"] == "PASS"
        assert last["validate"]["status"] == "PASS"
        assert last["prove"]["byte_identical"] is True
        authoring = c["authoring"]
        assert authoring["pipeline"] == "frontier", authoring.get("pipeline")
        assert authoring["gate"]["passed"] is True
        review = authoring["review"]
        assert review["model"] == "claude-fable-5-1", review.get("model")
        assert isinstance(review.get("resolution"), str) and review["resolution"], "resolution missing"


# ===== 3. Static downloads =====
DOWNLOAD_PARAMS = []  # populated in module scope below


def _collect_download_params():
    with open(MANIFEST_PATH) as f:
        m = json.load(f)
    params = []
    for section in ("published_dated", "published_unversioned"):
        for ext, entry in m[section].items():
            params.append(pytest.param(entry["file"], entry["bytes"], entry["sha256"], ext,
                                       id=f"{section}:{entry['file']}"))
    return params


@pytest.mark.parametrize("fname,size,sha,ext", _collect_download_params())
def test_download_bytes_and_hash(fname, size, sha, ext):
    url = f"{BASE_URL}/downloads/{fname}"
    r = requests.get(url, timeout=120)
    assert r.status_code == 200, f"{url} -> {r.status_code}"
    content = r.content
    assert len(content) == size, f"{fname} size {len(content)} != {size}"
    got_sha = hashlib.sha256(content).hexdigest()
    assert got_sha == sha, f"{fname} sha mismatch\n got {got_sha}\n exp {sha}"


@pytest.mark.parametrize("fname,ext", [
    ("RMS_Whole_Estate_Forecast_2026-10-03.docx", "docx"),
    ("RMS_Whole_Estate_Forecast_2026-10-03.pptx", "pptx"),
    ("RMS_Whole_Estate_Forecast_2026-10-03.xlsx", "xlsx"),
    ("RMS_Estate_and_Language_Review.docx", "docx"),
    ("RMS_Estate_and_Language_Review.pptx", "pptx"),
    ("RMS_Estate_and_Language_Review.xlsx", "xlsx"),
])
def test_download_opens_as_office_doc(fname, ext):
    r = requests.get(f"{BASE_URL}/downloads/{fname}", timeout=120)
    assert r.status_code == 200
    buf = io.BytesIO(r.content)
    if ext == "docx":
        from docx import Document
        doc = Document(buf)
        assert len(doc.paragraphs) > 10, f"{fname}: too few paragraphs"
    elif ext == "pptx":
        from pptx import Presentation
        p = Presentation(buf)
        assert len(p.slides) > 10, f"{fname}: too few slides"
    elif ext == "xlsx":
        from openpyxl import load_workbook
        wb = load_workbook(buf, read_only=True, data_only=True)
        assert len(wb.sheetnames) > 2, f"{fname}: too few sheets"


# ===== 4. Document content =====
@pytest.fixture(scope="session")
def forecast_docx_text():
    r = requests.get(f"{BASE_URL}/downloads/RMS_Whole_Estate_Forecast_2026-10-03.docx", timeout=120)
    assert r.status_code == 200
    from docx import Document
    doc = Document(io.BytesIO(r.content))
    paragraphs = [p.text for p in doc.paragraphs]
    # also pick up heading texts in order with styles
    heading_seq = [(p.text, p.style.name if p.style else "") for p in doc.paragraphs
                   if p.style and "Heading" in (p.style.name or "")]
    return paragraphs, heading_seq, doc


@pytest.fixture(scope="session")
def forecast_pptx():
    r = requests.get(f"{BASE_URL}/downloads/RMS_Whole_Estate_Forecast_2026-10-03.pptx", timeout=120)
    assert r.status_code == 200
    from pptx import Presentation
    return Presentation(io.BytesIO(r.content))


@pytest.fixture(scope="session")
def forecast_xlsx():
    r = requests.get(f"{BASE_URL}/downloads/RMS_Whole_Estate_Forecast_2026-10-03.xlsx", timeout=120)
    assert r.status_code == 200
    from openpyxl import load_workbook
    return load_workbook(io.BytesIO(r.content), data_only=True)


class TestDocxContent:
    def test_total_hours_present(self, forecast_docx_text):
        paragraphs, _, _ = forecast_docx_text
        joined = "\n".join(paragraphs)
        assert "500,290.3" in joined, "forecast total '500,290.3' not found in DOCX"

    def test_heading_order(self, forecast_docx_text):
        paragraphs, headings, _ = forecast_docx_text
        texts = [t for t, _ in headings]
        joined = "\n".join(paragraphs)
        # 'Summary' must appear before plain-english / coverage / appendix
        def idx(needle):
            for i, p in enumerate(paragraphs):
                if needle.lower() in p.lower():
                    return i
            return -1
        i_summary = idx("Summary")
        i_plain = idx("Plain English")
        i_cov = idx("Coverage and limits")
        i_app = idx("Appendix: receipts")
        assert i_summary >= 0, "'Summary' heading not found"
        assert i_plain > i_summary, f"Plain English not after Summary (summary={i_summary}, plain={i_plain})"
        assert i_cov > i_summary, f"Coverage not after Summary (cov={i_cov})"
        assert i_app > max(i_plain, i_cov), f"Appendix: receipts not last (app={i_app})"

    def test_no_unresolved_tokens(self, forecast_docx_text):
        paragraphs, _, _ = forecast_docx_text
        joined = "\n".join(paragraphs)
        unresolved = re.findall(r"\{[A-Z]\w+\}", joined)
        assert not unresolved, f"unresolved tokens in DOCX: {set(unresolved)}"

    def test_thousands_separators(self, forecast_docx_text):
        paragraphs, _, _ = forecast_docx_text
        joined = "\n".join(paragraphs)
        assert "248,841" in joined, "'248,841' not present (thousands sep check)"
        assert "248841" not in joined, "bare '248841' present without separator"


class TestPptxContent:
    def test_slide_count_range(self, forecast_pptx):
        n = len(forecast_pptx.slides)
        assert 60 <= n <= 90, f"slide count {n} outside 60..90"

    def test_slide2_is_exec_summary_with_total(self, forecast_pptx):
        slide = forecast_pptx.slides[1]  # slide 2
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    for run in p.runs:
                        texts.append(run.text)
                    texts.append(p.text)
        joined = " ".join(texts)
        assert "500,290.3" in joined, f"slide 2 missing '500,290.3'. Text sample: {joined[:400]}"

    def test_no_unresolved_tokens_pptx(self, forecast_pptx):
        all_text = []
        for s in forecast_pptx.slides:
            for shape in s.shapes:
                if shape.has_text_frame:
                    all_text.append(shape.text_frame.text)
        joined = "\n".join(all_text)
        unresolved = re.findall(r"\{F\w+\}", joined)
        assert not unresolved, f"PPTX unresolved {{F...}} tokens: {set(unresolved)}"


class TestXlsxContent:
    def test_required_sheets(self, forecast_xlsx):
        needed = {"Estate forecast by store", "Forecast by basis", "Forecast by folder",
                  "Forecast donors", "Decisions"}
        missing = needed - set(forecast_xlsx.sheetnames)
        assert not missing, f"missing sheets: {missing}. have: {forecast_xlsx.sheetnames}"

    def test_decisions_d0(self, forecast_xlsx):
        ws = forecast_xlsx["Decisions"]
        rows = list(ws.iter_rows(values_only=True))
        d0_row = None
        for row in rows:
            if row and row[0] and str(row[0]).strip().startswith("D0"):
                d0_row = row
                break
        assert d0_row is not None, f"no D0 row found. first cells: {[r[0] for r in rows[:10]]}"
        text = " ".join(str(c) for c in d0_row if c is not None).lower()
        assert "forecast" in text or "adopt" in text, f"D0 row doesn't mention adopt/forecast: {d0_row}"

    def test_estate_forecast_by_store_2024offairrecs(self, forecast_xlsx):
        ws = forecast_xlsx["Estate forecast by store"]
        rows = list(ws.iter_rows(values_only=True))
        # locate header row (contains both "Access" and "Basis")
        header = None
        header_idx = -1
        for idx, row in enumerate(rows):
            if not row:
                continue
            cells = [str(c).strip() if c is not None else "" for c in row]
            if "Access" in cells and "Basis" in cells:
                header = cells
                header_idx = idx
                break
        assert header is not None, f"header row with Access/Basis not found. first row cells: {rows[0]}"
        i_access = header.index("Access")
        i_basis = header.index("Basis")
        match = None
        for row in rows[header_idx + 1:]:
            if not row:
                continue
            if any("2024offairrecs" in str(c).lower() for c in row if c):
                match = row
                break
        assert match is not None, "no row for '2024offairrecs' bucket"
        access_val = str(match[i_access] or "")
        basis_val = str(match[i_basis] or "")
        assert "key refused (403)" in access_val.lower() or "403" in access_val, \
            f"Access value unexpected: {access_val}"
        assert basis_val.strip().lower() == "forecast", f"Basis value unexpected: {basis_val}"
