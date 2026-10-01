"""M1 closure on the pinned accessible scope: declared-coverage frontier + common durable identity across readers."""
import os
import sys

import pytest
import requests

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from services.census_autonomy import frontier  # noqa: E402

BASE = (os.environ.get('REACT_APP_BACKEND_URL') or '').rstrip('/')
OPERATOR = ('demo.operator@demo.rms.example.com', 'demo-operator-pw')


def _records():
    obs = {'source_ids': ['rms_obs'], 'record_id': 'cr-obs-2', 'status': 'PARTIAL', 'finished_at': '20260929T042148Z', 'source_details': [
        {'source_ref': 's1', 'label': 'bucket-a', 'status': 'complete', 'volume_bytes': 10},
        {'source_ref': 's2', 'label': 'bucket-b', 'status': 'blocked', 'reason_code': 'NoSuchBucket', 'volume_bytes': 0},
        {'source_ref': 's3', 'label': 'bucket-c', 'status': 'partial', 'volume_bytes': 5}]}
    older = {'source_ids': ['rms_obs'], 'record_id': 'cr-obs-1', 'status': 'COMPLETE', 'finished_at': '20260901T000000Z',
             'source_details': [{'source_ref': 's1', 'label': 'bucket-a', 'status': 'complete', 'volume_bytes': 1}]}
    mysql = {'source_ids': ['rms_mysql'], 'record_id': 'cr-sql-1', 'status': 'PARTIAL', 'finished_at': '20260928T000000Z', 'source_details': [
        {'source_ref': 'm1', 'label': 'rms_core', 'status': 'complete', 'volume_bytes': 100, 'table_count': 10},
        {'source_ref': 'm2', 'label': 'artists_app', 'status': 'blocked', 'reason_code': 'AUTHENTICATION_FAILED'}]}
    nas = {'source_ids': ['rms_nas'], 'record_id': 'cr-nas-1', 'status': 'BLOCKED', 'finished_at': '20260927T000000Z',
           'source_details': [{'source_ref': 'n1', 'label': 'synology', 'status': 'blocked', 'reason_code': 'FileNotFoundError'}]}
    pending = {'source_ids': ['rms_nas'], 'record_id': 'cr-nas-9', 'status': 'PENDING', 'finished_at': None, 'source_details': []}
    return [obs, older, mysql, nas, pending]


def test_frontier_keeps_latest_terminal_per_family_and_exclusions_in_denominator():
    view = frontier.frontier(_records())
    by_family = {r['family']: r for r in view['rows']}
    assert set(by_family) == {'rms_obs', 'rms_mysql', 'rms_nas'}
    assert by_family['rms_obs']['record_id'] == 'cr-obs-2'  # latest terminal, not the older complete one, not PENDING
    assert (by_family['rms_obs']['declared'], by_family['rms_obs']['completed'], by_family['rms_obs']['excluded']) == (3, 1, 2)
    assert by_family['rms_obs']['state'] == 'partial' and by_family['rms_obs']['measured_bytes'] == 10
    assert by_family['rms_nas']['state'] == 'blocked'
    assert view['declared_scopes'] == 6 and view['completed_scopes'] == 2 and view['excluded_scopes'] == 4
    assert view['pinned_accessible_scope'] == '2 of 6 declared scopes across 3 source families'
    assert view['exclusion_classes_total'] == {'declared_but_absent': 1, 'unclassified': 1, 'access_not_granted': 1, 'mount_absent': 1}


def test_exclusions_carry_plain_english_cause_and_ruling():
    view = frontier.frontier(_records())
    mysql = next(r for r in view['rows'] if r['family'] == 'rms_mysql')
    artists = mysql['exclusions'][0]
    assert artists['label'] == 'artists_app' and artists['class'] == 'access_not_granted'
    assert 'grant read access' in artists['plain'] and 'denominator' in artists['ruling']
    nas = next(r for r in view['rows'] if r['family'] == 'rms_nas')['exclusions'][0]
    assert nas['class'] == 'mount_absent' and 'SMB' in nas['plain']
    assert frontier.exclusion_for('ClientError')['class'] == 'unclassified'
    assert frontier.exclusion_for('botocore NoSuchBucket')['class'] == 'declared_but_absent'


def test_frontier_empty_records():
    view = frontier.frontier([])
    assert view['rows'] == [] and view['declared_scopes'] == 0 and view['pinned_accessible_scope'].startswith('0 of 0')


@pytest.fixture(scope='module')
def headers():
    if not BASE:
        pytest.skip('REACT_APP_BACKEND_URL is not set')
    r = requests.post(f'{BASE}/api/auth/login', json={'email': OPERATOR[0], 'password': OPERATOR[1]}, timeout=60)
    assert r.status_code == 200
    return {'Authorization': f"Bearer {r.json()['access_token']}"}


def test_live_overview_carries_frontier_and_annotated_exclusions(headers):
    r = requests.get(f'{BASE}/api/portal/census/overview', headers=headers, timeout=120)
    assert r.status_code == 200
    body = r.json()
    view = body['frontier']
    assert view['declared_scopes'] >= view['completed_scopes'] > 0
    assert view['excluded_scopes'] == view['declared_scopes'] - view['completed_scopes']
    assert sum(view['exclusion_classes_total'].values()) == view['excluded_scopes']
    for row in view['rows']:
        assert row['declared'] == row['completed'] + row['excluded'] and row['state'] in {'complete', 'partial', 'blocked'}
        for exclusion in row['exclusions']:
            assert exclusion['plain'] and exclusion['ruling'] and exclusion['class']
    incomplete = [s for r in body['records'] for s in r.get('source_details', []) if s.get('status') != 'complete']
    assert incomplete and all(s.get('exclusion', {}).get('plain') for s in incomplete)
    assert all('exclusion' not in s for r in body['records'] for s in r.get('source_details', []) if s.get('status') == 'complete')
    standalone = requests.get(f'{BASE}/api/portal/census/frontier', headers=headers, timeout=120)
    assert standalone.status_code == 200 and standalone.json()['tenant_id'] == 'RMS'
    assert standalone.json()['frontier']['pinned_accessible_scope'] == view['pinned_accessible_scope']


def test_live_common_durable_identity_across_registry_readers(headers):
    """The same census identity must restate identically through every reader: overview, registry facts, record, run state."""
    overview = requests.get(f'{BASE}/api/portal/census/overview', headers=headers, timeout=120).json()
    facts = requests.get(f'{BASE}/api/registry/facts', headers=headers, timeout=120).json()
    assert [r['record_id'] for r in overview['records']] == [r['record_id'] for r in facts['records']]
    assert overview['frontier'] == facts['frontier']
    latest = overview['latest']
    record = requests.get(f"{BASE}/api/portal/census/records/{latest['record_id']}", headers=headers, timeout=120).json()['record']
    for key in ('record_id', 'status', 'finished_at', 'table_count', 'database_count', 'volume_bytes', 'proof_sha256', 'coverage'):
        assert record.get(key) == latest.get(key), key
    runs = {r['census_run_id']: r for r in overview['runs']}
    checked = 0
    for run_id, run in list(runs.items())[:5]:
        state = requests.get(f'{BASE}/api/portal/census/runs/{run_id}/state', headers=headers, timeout=120)
        assert state.status_code == 200
        assert state.json()['census_run_id'] == run_id and state.json()['status'] == run['status']
        checked += 1
    assert checked > 0
    history = requests.get(f'{BASE}/api/census/history', headers=headers, timeout=120).json()
    census_ids = {r['record_id'] for r in overview['records'] if not r['record_id'].startswith('eij-')}
    assert {r['record_id'] for r in history['records']} == census_ids
