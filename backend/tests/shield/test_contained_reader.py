"""WP-A2 — contained reasoning rung on the estate serving seam (Doc 1 A5.5 B43–B45, A5.6 B46; Doc 11 A5.1 B35).

Unit (no host): the in-process egress guard refuses non-loopback connections and the probe reports blocked; JSON extraction, schema and
leak checks on SYNTHETIC readings; dispatch validation requires the attested weight hash; the control plane REFUSES (ReaderUnavailable)
when the reader is not serving — never a fallback. Live (skips with the reason when the reader is not serving): health carries lineage and
offline env, the egress probe is blocked on the host, a SYNTHETIC contract reads to a schema-valid reading with the declared categories,
no original text appears in the SSH receipt purpose, latency is recorded."""
import json
import os
import socket
import sys

import pytest
import requests
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.training_runner import m9_dispatch as m9  # noqa: E402
from services.training_runner import reader_worker as rw  # noqa: E402

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
SYNTHETIC = ('SYNTHETIC BRD. Prepare a launch brief for our client Zinnia Grove Test Cooperative under the internal codename Mango Halo. '
             'The agreed retainer is KES 88,500 per month with a 12% exclusivity premium; the bid is computed as 0.81 times the rival floor. Contact: amina.test@example.com.')
CATEGORIES = [{'name': 'client_identity', 'description': 'who the counterparty, client or partner is'}, {'name': 'private_project_name', 'description': 'internal code names'},
              {'name': 'commercial_terms', 'description': 'fees, prices, premiums and negotiated figures'}, {'name': 'unpublished_pricing_method', 'description': 'how a price or bid is computed'}, {'name': 'personal_data', 'description': 'direct identifiers'}]


# ----------------------------------------------------------------------------- unit: egress guard
def test_egress_guard_refuses_non_loopback_and_probe_reports_blocked():
    saved = (socket.socket.connect, socket.socket.connect_ex, socket.create_connection)
    guard = rw.EgressGuard().install()
    try:
        with pytest.raises(PermissionError, match='EGRESS_DENIED'):
            socket.create_connection(('1.1.1.1', 443), timeout=1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with pytest.raises(PermissionError):
            s.connect(('93.184.216.34', 80))
        s.close()
        probe = guard.probe()
        assert probe['blocked'] is True and len(guard.blocked) >= 3
        assert os.environ['HF_HUB_OFFLINE'] == '1' and os.environ['TRANSFORMERS_OFFLINE'] == '1'
        # loopback stays allowed (the server itself is loopback)
        srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(1)
        cli = socket.create_connection(srv.getsockname(), timeout=2); cli.close(); srv.close()
        assert guard.allowed_loopback >= 1
    finally:
        socket.socket.connect, socket.socket.connect_ex, socket.create_connection = saved


# ----------------------------------------------------------------------------- unit: reading shape
def test_json_extraction_schema_and_leak_check_on_synthetic_readings():
    good = json.loads(rw.EXAMPLE_OUT)
    assert rw.extract_json('Sure! ' + rw.EXAMPLE_OUT + ' trailing') == good
    assert rw.validate_reading(good) == [] and rw.leak_check(good) == []
    assert rw.extract_json('no json here') is None and rw.extract_json('{"a": [1, 2') is None
    bad = {**good, 'objective': {'intent': 'plan'}}
    assert any('objective' in p for p in rw.validate_reading(bad))
    leaky = {**good, 'safe_rewrite': 'Draft a plan for Nuru Orchard Test Cooperative'}
    assert rw.leak_check(leaky) == ['Nuru Orchard Test Cooperative']
    msgs = rw.build_messages('Text under review', CATEGORIES)
    assert msgs[0]['role'] == 'system' and 'client_identity' in msgs[-1]['content'] and 'Text under review' in msgs[-1]['content'] and len(msgs) == 6


def test_dispatch_validation_requires_attested_hash_and_residency_entry():
    good = {'base_registry_id': 'qwen3-8b-base', 'expected_weight_sha256': 'a' * 64, 'port': 8641, 'gpu_index': 1, 'residency_entry_id': 'res-x', 'authority': {'model_id': cr.MODEL_ID}}
    m9.validate('serve_reader', good, 'akki-vm-ii')
    for missing in ('expected_weight_sha256', 'residency_entry_id', 'authority', 'base_registry_id'):
        with pytest.raises(ValueError, match='M9_SERVE_READER_REQUIRES'):
            m9.validate('serve_reader', {k: v for k, v in good.items() if k != missing}, 'akki-vm-ii')
    with pytest.raises(ValueError, match='M9_SERVE_READER_REQUIRES'):
        m9.validate('serve_reader', {**good, 'expected_weight_sha256': 'not-a-hash'}, 'akki-vm-ii')
    with pytest.raises(ValueError, match='M9_GPU_INDEX_REQUIRED'):
        m9.validate('serve_reader', {**good, 'gpu_index': '1'}, 'akki-vm-ii')
    assert 'services/training_runner/reader_worker.py' in __import__('zipfile').ZipFile(__import__('io').BytesIO(__import__('base64').b64decode(m9.build_bundle()[0]))).namelist()


def test_control_plane_refuses_when_the_reader_is_not_serving(monkeypatch):
    monkeypatch.setattr(cr, 'load_registry', lambda: {})
    with pytest.raises(cr.ReaderUnavailable, match='not registered'):
        cr.read(SYNTHETIC, CATEGORIES, 'test')
    monkeypatch.setattr(cr, 'load_registry', lambda: {cr.MODEL_ID: {'model_id': cr.MODEL_ID, 'role': cr.ROLE, 'serving': {'job_id': 'm9j-000000000000', 'port': 8641}}})
    monkeypatch.setattr(cr.m9, 'refresh', lambda job_id: {'job_id': job_id, 'status': 'failed', 'reason': 'synthetic'})
    with pytest.raises(cr.ReaderUnavailable, match='not serving'):
        cr.read(SYNTHETIC, CATEGORIES, 'test')
    with pytest.raises(cr.ReaderUnavailable):
        cr.health()


# ----------------------------------------------------------------------------- live (host): skips honestly when the reader is not serving
def _serving():
    st = cr.status()
    if st.get('status') != 'running':
        pytest.skip(f"contained reader not serving: {st.get('status')} {json.dumps(st.get('job') or st.get('reason') or '')[:160]}")
    return st


def test_live_health_lineage_offline_env_and_egress_probe_blocked():
    _serving()
    h = cr.health()
    assert h['status'] in ('serving', 'revoked') and h['role'] == 'contained_reader' and h['licence_verified'].startswith('apache') and len(h['weight_sha256']) == 64
    assert h['offline_env'] == {'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1', 'DO_NOT_TRACK': '1'} and h['egress_guard']['installed'] is True and h['resident_mib'] > 10000
    probe = cr.egress_probe()
    assert probe['probe']['blocked'] is True, probe


def test_live_synthetic_read_is_schema_valid_and_bounded():
    st = _serving()
    if (st.get('entry') or {}).get('serving', {}).get('status') == 'revoked':
        pytest.skip('reader authority revoked')
    out = cr.read(SYNTHETIC, CATEGORIES, 'test_contained_reader')
    reading = out['reading']
    assert rw.validate_reading(reading) == [] and rw.leak_check(reading) == []
    spans = ' '.join(p['span'] for p in reading['privileged']).lower()
    assert any(k in spans for k in ('zinnia', 'mango halo', '88,500', '88500', '0.81')), reading['privileged']
    assert reading['objective']['coherent'] is True and out['seconds'] is not None and out['lineage']['host'] and out['receipt_id']
    assert 'zinnia' not in reading['safe_rewrite'].lower() and 'mango halo' not in reading['safe_rewrite'].lower()
    # the receipt purpose names the caller, never the text
    from services.training_runner.ssh_seam import _env_get  # noqa: F401
    assert 'Zinnia' not in out['receipt_id']


def test_live_api_status_and_role_gates():
    r = requests.post(f'{BASE_URL}/api/auth/login', json={'email': 'demo.operator@demo.rms.example.com', 'password': 'demo-operator-pw'}, timeout=20)
    if r.status_code != 200: pytest.skip('operator login failed')
    op = {'Authorization': f"Bearer {r.json()['access_token']}"}
    s = requests.get(f'{BASE_URL}/api/shield/reader', headers=op, timeout=120); assert s.status_code == 200 and s.json()['status'] in ('running', 'not_serving', 'not_registered')
    assert requests.post(f'{BASE_URL}/api/shield/reader/start', headers=op, json={}, timeout=30).status_code == 403, 'start is a master-admin act'
    assert requests.post(f'{BASE_URL}/api/shield/reader/revoke', headers=op, json={'reason': 'nope'}, timeout=30).status_code == 403
    res = requests.get(f'{BASE_URL}/api/training/residency/terms', headers=op, timeout=60); assert res.status_code == 200 and set(res.json()['terms']) == {'active_run_data', 'checkpoint', 'admitted_model', 'serving_resident', 'derived_register', 'raw_material'}
