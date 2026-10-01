"""M2 §6 'legitimate-work friction over representative traffic' — LIVE against the deployed control plane.

Representative ordinary traffic from the two admitted operators (sign-ins, portal reads, Watch state reads and one
independent-witness pass) must leave NO detection and NO effect on those principals, the new authentication and
egress boundaries must appear on the published inventory, and the watchdog's countersigned verdict must be
`consistent`. Nothing is commissioned, extracted, uploaded or spent.
"""
import os
import time

import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
OPERATORS = [('demo.operator@demo.digicow.example.com', 'demo-digicow-operator-pw'), ('demo.operator@demo.rms.example.com', 'demo-operator-pw')]


def login(email, password):
    r = requests.post(f'{BASE_URL}/api/auth/login', json={'email': email, 'password': password}, timeout=30)
    assert r.status_code == 200, r.text
    return {'Authorization': f"Bearer {r.json()['access_token']}"}


@pytest.fixture(scope='module')
def traffic():
    """Three sign-ins and a dozen reads per operator, spaced like a person working, before any assertion is read."""
    out = {}
    for email, password in OPERATORS:
        headers = None
        for _ in range(3):
            headers = login(email, password)
            time.sleep(0.4)
        reads = ['/api/auth/me', '/api/portal/requests', '/api/portal/commission/drafts', '/api/portal/entitlement/allowance',
                 '/api/portal/watch/state', '/api/portal/watch/notices', '/api/chat/sessions', '/api/portal/watch/witness',
                 '/api/portal/requests', '/api/portal/watch/state', '/api/chat/evaluations', '/api/portal/commission/destinations']
        statuses = [requests.get(f'{BASE_URL}{path}', headers=headers, timeout=60).status_code for path in reads]
        me = requests.get(f'{BASE_URL}/api/auth/me', headers=headers, timeout=30).json()
        out[email] = {'headers': headers, 'statuses': statuses, 'principal_id': me.get('user_id') or me.get('id') or me.get('principal_id')}
    return out


def test_reads_are_served_and_nothing_is_refused(traffic):
    for email, t in traffic.items():
        assert all(s == 200 for s in t['statuses']), (email, t['statuses'])


def test_no_detection_or_effect_lands_on_legitimate_operators(traffic):
    for email, t in traffic.items():
        state = requests.get(f'{BASE_URL}/api/portal/watch/state', headers=t['headers'], timeout=60).json()
        acted = [r for r in state['records'] if r['kind'] in ('action', 'verdict') and r.get('actor') == f"principal:{t['principal_id']}"
                 and (r.get('observed_at') or '') >= time.strftime('%Y-%m-%dT%H', time.gmtime())]
        assert acted == [], (email, acted)
        boundaries = {b['boundary'] for b in state['protected_boundaries']}
        assert {'auth.login', 'media.download', 'dap.commission', 'dap.approval', 'dap.delivery', 'skill.query', 'chat.evaluation'} <= boundaries
        assert state['witness']['independent']['placed'] is True and 'hysteresis' in state['detector_status']


def test_independent_watchdog_pass_is_consistent_and_countersigned(traffic):
    headers = traffic[OPERATORS[0][0]]['headers']
    r = requests.post(f'{BASE_URL}/api/portal/watch/witness/pass', headers=headers, timeout=120)
    assert r.status_code == 200, r.text
    result = r.json()['pass']
    assert result['outcome'] == 'witnessed' and result['verdict'] == 'consistent' and result['findings'] == [], result
    assert result['signature_verified'] is True and result['key_matches_registered_identity'] is True and result['host_script_matches'] is True
    assert result['record']['host'] == 'akki-vm' and result['record']['witness_seq'] >= 1
    status = requests.get(f'{BASE_URL}/api/portal/watch/witness', headers=headers, timeout=60).json()
    assert status['placed'] and status['silent'] is False and status['last_pass']['pass_id'] == result['pass_id']


def test_analyst_cannot_run_or_read_the_watchdog():
    headers = login('demo.analyst@demo.rms.example.com', 'demo-analyst-pw')
    assert requests.post(f'{BASE_URL}/api/portal/watch/witness/pass', headers=headers, timeout=60).status_code == 403
    assert requests.get(f'{BASE_URL}/api/portal/watch/witness', headers=headers, timeout=60).status_code == 403
    assert requests.post(f'{BASE_URL}/api/watch/witness/cron', json={'event': 'schedule.triggered', 'run_id': 'x', 'data': None}, timeout=30).status_code == 401
