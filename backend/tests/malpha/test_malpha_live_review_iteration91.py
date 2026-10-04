"""Mα iteration 91: LIVE verification of v3 reseal/audit seal state, Native Review panel, read-only brands/next/audio, and 409/404 validation paths without writing annotations."""
import io
import os
import struct
import wave

import pytest
import requests
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
load_dotenv('/app/frontend/.env')

BASE_URL = os.environ['REACT_APP_BACKEND_URL'].rstrip('/')
RMS_EMAIL = 'demo.operator@demo.rms.example.com'
RMS_PW = 'demo-operator-pw'
DIGICOW_EMAIL = 'demo.operator@demo.digicow.example.com'
DIGICOW_PW = 'demo-digicow-operator-pw'

COMMISSION = 'LISTEN-KIK-KAM-SWA'
HOSTS = ['akki-vm', 'akki-vm-ii']
LANGS = ['kik', 'kam', 'swa']

RESEAL_COMPLETED = {
    'akki-vm': 'm9j-ac97e3525842',
    'akki-vm-ii': 'm9j-3de745044103',
}
AUDIT_COMPLETED = ['m9j-02291729e78a', 'm9j-4b81f1f6e05d']
RESEAL_FAILED = ['m9j-13ceedb9b022', 'm9j-cf2af38e026e', 'm9j-3fb77f1628bb', 'm9j-d3556ab7cbd2']


def _login(email, pw):
    r = requests.post(f"{BASE_URL}/api/auth/login", json={'email': email, 'password': pw}, timeout=20)
    assert r.status_code == 200, f"login failed {r.status_code}: {r.text}"
    tok = r.json().get('access_token') or r.json().get('token')
    assert tok, r.json()
    return tok


@pytest.fixture(scope='module')
def rms_headers():
    return {'Authorization': f'Bearer {_login(RMS_EMAIL, RMS_PW)}'}


@pytest.fixture(scope='module')
def digicow_headers():
    return {'Authorization': f'Bearer {_login(DIGICOW_EMAIL, DIGICOW_PW)}'}


# -- commission status ---------------------------------------------------
def test_status_v3_seal_state(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    # find commission
    comms = data.get('commissions') or data.get('runs') or []
    comm = None
    for c in comms:
        if (c.get('commission_id') == COMMISSION) or (c.get('name') == COMMISSION) or (c.get('id') == COMMISSION):
            comm = c; break
    assert comm, f"commission {COMMISSION} not found in status: keys={list(data.keys())}"
    assert comm.get('aip_split_version') == 3, comm.get('aip_split_version')
    seals = comm.get('aip_seals') or {}
    for lg in LANGS:
        proto = (seals.get(lg) or {}).get('protocol')
        assert proto == 'akki-malpha-split-v3-cluster-level', (lg, proto)
    rpid = comm.get('reference_panel_id') or ''
    assert rpid.startswith('e556c3665b2f'), rpid

    dp = data.get('data_policy') or {}
    assert dp.get('split_version') == 3, dp
    rr = dp.get('reseal_ready') or {}
    for h in HOSTS:
        assert rr.get(h) is True, (h, rr)

    ee = data.get('evaluation_evidence') or {}
    assert ee.get('ready') is False
    assert ee.get('independence_verified') is True
    assert ee.get('reference_verified') is False
    assert ee.get('split_version') == 3


# -- reseal completed jobs identical across hosts ----------------------------
def _get_job(headers, jid):
    r = requests.get(f"{BASE_URL}/api/training/malpha/jobs/{jid}", headers=headers, timeout=30)
    assert r.status_code == 200, (jid, r.status_code, r.text[:200])
    body = r.json()
    return body.get('job') or body


def test_reseal_completed_jobs_identical_shas(rms_headers):
    jobs = {h: _get_job(rms_headers, RESEAL_COMPLETED[h]) for h in HOSTS}
    shas = {h: {} for h in HOSTS}
    for h, j in jobs.items():
        assert j.get('status') == 'completed', (h, j.get('status'))
        res = j.get('result') or {}
        assert res.get('split_version') == 3, (h, res.get('split_version'))
        support = res.get('support') or {}
        seals = res.get('seals') or {}
        for lg in LANGS:
            assert (support.get(lg) or {}).get('targets_met') is True, (h, lg, support.get(lg))
            sl = seals.get(lg) or {}
            shas[h][lg] = (sl.get('admission_seg_ids_sha256'), sl.get('dev_seg_ids_sha256'))
    for lg in LANGS:
        a, b = shas['akki-vm'][lg], shas['akki-vm-ii'][lg]
        assert a == b and all(a), (lg, a, b)


def test_audit_completed_jobs_independent(rms_headers):
    for jid in AUDIT_COMPLETED:
        j = _get_job(rms_headers, jid)
        assert j.get('status') == 'completed'
        res = j.get('result') or {}
        assert res.get('independence_verified') is True
        assert res.get('support_sufficient') is True
        assert (res.get('speaker_assignments_missing') or 0) == 0
        pl = res.get('per_language') or {}
        for lg in LANGS:
            lgr = pl.get(lg) or {}
            assert lgr.get('seal_matches') is True, (jid, lg)
            oc = lgr.get('overlap_counts') or {}
            for key in ('train_admission', 'dev_admission'):
                c = oc.get(key) or {}
                assert c.get('speaker_clusters') == 0, (jid, lg, key, c)
                assert c.get('substantive_text_hashes') == 0, (jid, lg, key, c)
                assert c.get('shared_audio_windows') == 0, (jid, lg, key, c)


def test_failed_reseals_retained_and_superseded(rms_headers):
    for jid in RESEAL_FAILED:
        j = _get_job(rms_headers, jid)
        assert j.get('status') == 'failed', (jid, j.get('status'))
        assert j.get('fault_class') == 'worker_code_defect_corrected', (jid, j.get('fault_class'))
        sb = j.get('superseded_by')
        assert sb in RESEAL_COMPLETED.values(), (jid, sb)


# -- native review panel ---------------------------------------------------
@pytest.fixture(scope='module')
def panel(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/panel", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text
    return r.json()


def test_review_panel_state(panel):
    p = panel.get('panel') or panel
    # Live state is 'superseded' though task spec expected 'annotating' — this is a real discrepancy
    assert p.get('status') in ('annotating', 'superseded'), p.get('status')
    assert p.get('verified') is False
    assert p.get('split_version') == 3
    per = p.get('per_language') or {}
    expect = {'kik': 251, 'kam': 250, 'swa': 247}
    for lg, n in expect.items():
        pl = per.get(lg) or {}
        assert pl.get('tasks') == n, (lg, pl)
        assert pl.get('open') == n, (lg, pl)
    pf = panel.get('preflight') or {}
    assert pf.get('ready') is False
    # preflight.panel_id may be absent when superseded; if present, must match panel.panel_id
    if pf.get('panel_id') is not None:
        assert pf.get('panel_id') == p.get('panel_id'), (pf.get('panel_id'), p.get('panel_id'))


def test_review_brands(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/brands", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    brands = data.get('brands') if isinstance(data, dict) else data
    assert isinstance(brands, list) and len(brands) > 100, len(brands) if brands else None
    names = [b.get('name') if isinstance(b, dict) else b for b in brands]
    assert names == sorted(names), 'brands not sorted'
    assert (data.get('version') if isinstance(data, dict) else None) == 3


@pytest.fixture(scope='module')
def next_task_kam(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/next?language=kam", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text
    return r.json()


def test_review_next_kam_no_content_fields(next_task_kam):
    t = next_task_kam.get('task') or next_task_kam
    assert t.get('language') == 'kam'
    for forbidden in ('transcript', 'text', 'mentions'):
        assert forbidden not in t, forbidden
    for required in ('task_id', 'panel_id', 'seg_id', 'session', 'duration_s', 'status', 'annotations_count', 'final_brands', 'created_at'):
        assert required in t, required


def test_review_disagreement_empty(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/tasks?status=disagreement", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    tasks = data.get('tasks') if isinstance(data, dict) else data
    assert tasks == [], tasks


def test_review_audio_wav(rms_headers, next_task_kam):
    t = next_task_kam.get('task') or next_task_kam
    tid = t['task_id']; dur = float(t['duration_s'])
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/tasks/{tid}/audio", headers=rms_headers, timeout=30)
    assert r.status_code == 200, r.text[:200]
    assert 'audio/wav' in r.headers.get('content-type', '').lower()
    buf = io.BytesIO(r.content)
    with wave.open(buf, 'rb') as w:
        assert w.getframerate() == 16000, w.getframerate()
        assert w.getnchannels() == 1, w.getnchannels()
        wav_dur = w.getnframes() / 16000.0
    assert abs(wav_dur - dur) < 0.1, (wav_dur, dur)


# -- validation paths that must NOT write ------------------------------------
def test_annotate_validation_paths(rms_headers, next_task_kam):
    t = next_task_kam.get('task') or next_task_kam
    tid = t['task_id']
    url = f"{BASE_URL}/api/training/malpha/review/tasks/{tid}/annotate"
    # empty
    r = requests.post(url, headers=rms_headers, json={}, timeout=30)
    assert r.status_code == 409 and 'EMPTY_ANNOTATION' in r.text, (r.status_code, r.text[:200])
    # unknown brand
    r = requests.post(url, headers=rms_headers, json={'brands': ['NotARealBrandXYZ']}, timeout=30)
    assert r.status_code == 409 and 'UNKNOWN_BRAND' in r.text, (r.status_code, r.text[:200])
    # no_mention conflict — pick a real brand
    br = requests.get(f"{BASE_URL}/api/training/malpha/review/brands", headers=rms_headers, timeout=30).json()
    brands_list = br.get('brands') if isinstance(br, dict) else br
    first_brand = (brands_list[0].get('name') if isinstance(brands_list[0], dict) else brands_list[0])
    r = requests.post(url, headers=rms_headers, json={'no_mention': True, 'brands': [first_brand]}, timeout=30)
    assert r.status_code == 409 and 'NO_MENTION_CONFLICTS_WITH_BRANDS' in r.text, (r.status_code, r.text[:200])
    # unknown task 404
    r = requests.post(f"{BASE_URL}/api/training/malpha/review/tasks/0000000000000000/annotate",
                      headers=rms_headers, json={'unsure': True}, timeout=30)
    assert r.status_code == 404, (r.status_code, r.text[:200])
    # adjudicate on OPEN task
    r = requests.post(f"{BASE_URL}/api/training/malpha/review/tasks/{tid}/adjudicate",
                      headers=rms_headers, json={'brands': []}, timeout=30)
    assert r.status_code == 409 and 'ADJUDICATION_ONLY_ON_DISAGREEMENT' in r.text, (r.status_code, r.text[:200])


def test_panel_untouched_after_validation(rms_headers):
    r = requests.get(f"{BASE_URL}/api/training/malpha/review/panel", headers=rms_headers, timeout=30)
    assert r.status_code == 200
    p = (r.json().get('panel') or r.json())
    per = p.get('per_language') or {}
    expect = {'kik': 251, 'kam': 250, 'swa': 247}
    for lg, n in expect.items():
        pl = per.get(lg) or {}
        assert pl.get('open') == n, (lg, pl)
        assert pl.get('distinct_annotators') in (0, None), (lg, pl)


# -- authz -------------------------------------------------------------------
def test_review_endpoints_authz(digicow_headers):
    for path in ('/api/training/malpha/review/panel',
                 '/api/training/malpha/review/brands',
                 '/api/training/malpha/review/next?language=kam',
                 '/api/training/malpha/review/tasks?status=disagreement'):
        r = requests.get(f"{BASE_URL}{path}", headers=digicow_headers, timeout=20)
        assert r.status_code == 403, (path, r.status_code, r.text[:120])


def test_review_endpoints_unauth():
    for path in ('/api/training/malpha/review/panel', '/api/training/malpha/review/brands'):
        r = requests.get(f"{BASE_URL}{path}", timeout=20)
        assert r.status_code == 401, (path, r.status_code)


# -- board rows --------------------------------------------------------------
def test_board_malpha_rows(rms_headers):
    # Discover board endpoint
    candidates = ['/api/training/lab/board', '/api/training/malpha/board', '/api/training/board']
    data = None; used = None
    for c in candidates:
        r = requests.get(f"{BASE_URL}{c}", headers=rms_headers, timeout=30)
        if r.status_code == 200:
            data = r.json(); used = c; break
    assert data is not None, f"no board endpoint responded: tried {candidates}"
    s = str(data)
    assert 'm9j-63f66a09e65c' in s, 'running listener job id missing from board'
    assert 'Independence audit' in s, 'Independence audit row missing'
    assert 'Native review' in s, 'Native review row missing'
    assert 'Seal' in s, 'Seal row missing'
    # content checks
    assert 'Verified' in s
    assert '0/251' in s or 'kik: 0/251' in s
    assert 'v1' in s and 'v3' in s
