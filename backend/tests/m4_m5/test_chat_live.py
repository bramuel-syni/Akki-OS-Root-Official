"""M4/M5 live proof against the deployed control plane: a DIGICOW operator asks, follows up, is refused honestly,
then compacts, reloads (hash-verified) and archives the session. Every warm answer must show ZERO source
dispatches; the qualified store is the only thing read. Model calls are real (one per warm turn), so this suite is
small by design. RMS analyst and anonymous callers prove scope and identity gates.
"""
import os

import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
DIGICOW = ('demo.operator@demo.digicow.example.com', 'demo-digicow-operator-pw')
RMS_ANALYST = ('demo.analyst@demo.rms.example.com', 'demo-analyst-pw')
TURN_TIMEOUT = 170


def _login(email, password):
    r = requests.post(f'{BASE_URL}/api/auth/login', json={'email': email, 'password': password}, timeout=30)
    assert r.status_code == 200, r.text
    body = r.json()
    return {'Authorization': f"Bearer {body.get('access_token') or body.get('token')}", 'Content-Type': 'application/json'}


@pytest.fixture(scope='module')
def digicow():
    return _login(*DIGICOW)


@pytest.fixture(scope='module')
def rms_analyst():
    return _login(*RMS_ANALYST)


@pytest.fixture(scope='module')
def state():
    return {}


def ask(headers, question, session_id=None):
    r = requests.post(f'{BASE_URL}/api/chat/ask', headers=headers, json={'question': question, 'session_id': session_id}, timeout=TURN_TIMEOUT)
    assert r.status_code == 200, r.text
    return r.json()


class TestGovernedJourney:
    def test_01_first_question_opens_session_and_answers_warm_with_zero_source_reads(self, digicow, state):
        body = ask(digicow, 'What do farmers ask about feeding and minerals in the training questions?')
        turn, reads = body['turn'], body['turn']['evidence']['reads']
        state['session_id'] = body['session_id']
        assert body['objective']['text'] == turn['question'] and body['turns'] == 1
        assert turn['decision'] == 'warm' and not turn['refused'], turn.get('refusal_reason')
        assert reads['source_dispatches'] == 0 and reads['source_rows_read'] == 0 and reads['qualified_store_calls'] >= 1
        window = turn['evidence']['window']
        assert window['tokens_in_window'] <= window['window_tokens'] - window['reserved_tokens']
        assert window['loss_statement'] in turn['answer']
        assert turn['evidence']['grounding']['grounding'] in ('cited_in_window', 'partially_cited')
        assert all(ref in window['selected_refs'] for ref in turn['evidence']['cited_refs'])
        assert turn['decision_detail']['ledger_row_id'].startswith('led-') and turn['receipt_id'].startswith('rcp-')
        assert turn['critic_verdict']['seam_attested'] is True
        state['hot_after'] = turn['evidence']['memory']['hot_refs_after']

    def test_02_follow_up_stays_in_session_reuses_warm_memory(self, digicow, state):
        body = ask(digicow, 'Which of those were about minerals specifically?', state['session_id'])
        turn = body['turn']
        assert body['session_id'] == state['session_id'] and body['turns'] == 2
        assert turn['decision'] == 'warm' and turn['evidence']['reads']['source_dispatches'] == 0, (turn['decision'], turn.get('refusal_reason'))
        if not turn['refused']:
            assert turn['evidence']['memory']['hits'] + turn['evidence']['memory']['misses'] == len(turn['evidence']['window']['selected_refs'])

    def test_03_out_of_scope_is_refused_without_any_read(self, digicow, state):
        body = ask(digicow, 'What is the weather forecast for Paris tomorrow?', state['session_id'])
        turn = body['turn']
        assert turn['decision'] == 'refused' and turn['refused'] and 'Out of scope' in turn['refusal_reason']
        assert turn['evidence']['reads']['source_dispatches'] == 0 and turn['evidence']['reads']['candidates_returned'] == 0
        assert turn['decision_detail']['reason'] == 'out_of_scope'

    def test_04_session_is_durable_and_listed(self, digicow, state):
        r = requests.get(f"{BASE_URL}/api/chat/sessions/{state['session_id']}", headers=digicow, timeout=60)
        assert r.status_code == 200
        session = r.json()
        assert len(session['turns']) == 3 and [t['decision'] for t in session['turns']] == ['warm', 'warm', 'refused']
        rows = requests.get(f'{BASE_URL}/api/chat/sessions', headers=digicow, timeout=60).json()['rows']
        assert any(row['session_id'] == state['session_id'] and 'turns' not in row for row in rows)

    def test_05_compact_then_hash_verified_reload(self, digicow, state):
        r = requests.post(f"{BASE_URL}/api/chat/sessions/{state['session_id']}/compact", headers=digicow, timeout=60)
        assert r.status_code == 200 and r.json()['status'] == 'compacted', r.text
        compaction = r.json()['compaction']
        assert compaction['chain_row_id'] == f"memory-compaction-v1-{compaction['artefact_hash']}" and compaction['compacted_turns'] == 3
        reload = requests.get(f"{BASE_URL}/api/chat/sessions/{state['session_id']}/reload", headers=digicow, timeout=60).json()
        assert reload['status'] == 'verified' and reload['verified_sha256'] == compaction['artefact_hash']
        facts = [e for e in reload['entries'] if e['class'] in ('fact', 'receipt_ref')]
        assert facts and all('text' not in e for e in facts)
        assert any(e['class'] == 'refusal' for e in reload['entries'])
        again = requests.post(f"{BASE_URL}/api/chat/sessions/{state['session_id']}/compact", headers=digicow, timeout=60).json()
        assert again['status'] == 'nothing_to_compact'

    def test_06_archive_hides_from_default_listing(self, digicow, state):
        r = requests.post(f"{BASE_URL}/api/chat/sessions/{state['session_id']}/archive", headers=digicow, timeout=60)
        assert r.status_code == 200
        rows = requests.get(f'{BASE_URL}/api/chat/sessions', headers=digicow, timeout=60).json()['rows']
        assert all(row['session_id'] != state['session_id'] for row in rows)
        archived = requests.get(f'{BASE_URL}/api/chat/sessions?archived=true', headers=digicow, timeout=60).json()['rows']
        assert any(row['session_id'] == state['session_id'] for row in archived)


class TestScopeAndIdentity:
    def test_anonymous_is_refused(self):
        assert requests.post(f'{BASE_URL}/api/chat/ask', json={'question': 'anything'}, timeout=30).status_code == 401
        assert requests.get(f'{BASE_URL}/api/chat/sessions', timeout=30).status_code == 401

    def test_other_tenant_cannot_open_the_session(self, rms_analyst, state):
        r = requests.get(f"{BASE_URL}/api/chat/sessions/{state['session_id']}", headers=rms_analyst, timeout=60)
        assert r.status_code == 404
        r = requests.post(f'{BASE_URL}/api/chat/ask', headers=rms_analyst, json={'question': 'follow up', 'session_id': state['session_id']}, timeout=TURN_TIMEOUT)
        assert r.status_code == 404

    def test_analyst_without_qualified_units_gets_fresh_or_refused_and_never_a_draft(self, rms_analyst):
        body = ask(rms_analyst, 'How many songs are in the catalogue?')
        turn = body['turn']
        assert turn['decision'] in ('fresh', 'refused')
        assert turn['evidence']['reads']['source_dispatches'] == 0
        assert not turn['decision_detail'].get('draft')
        requests.post(f"{BASE_URL}/api/chat/sessions/{body['session_id']}/archive", headers=rms_analyst, timeout=60)
