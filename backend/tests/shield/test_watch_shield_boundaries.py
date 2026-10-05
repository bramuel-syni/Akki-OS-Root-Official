"""WP-A7 — Watch re-coverage of the Shield boundaries added by Wave A (roadmap: every operation added after M2 reruns the relevant Watch
coverage). Inventory: the register ceremony acts, vault intake, the sealed stage, task separation and the reader relay are protected
boundaries. Drills (isolated Watch record dirs, SYNTHETIC tenant, reader faked at the seam, NER passed through): a sealed stage is an
admitted crossing; a seam refusal is a refused crossing; three refusals inside the fast window mint a Watch verdict and a shape action on
the principal (M2 drill subset); an unobservable crossing refuses the stage and leaves nothing sealed. Live: a refused register act on the
real API lands as a refused crossing in the tenant feed."""
import asyncio
import os
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import requests
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, '/app/backend/tests/shield')

from services.synisense.shield import category3 as c3  # noqa: E402
from services.synisense.shield import semantic_register as reg  # noqa: E402
from services.synisense.shield import stage as st  # noqa: E402
from services.training_lab import store as lab  # noqa: E402
from services.watch import commission_gate as gate  # noqa: E402
import test_shield_stage as fixtures  # noqa: E402

NEW_BOUNDARIES = {'shield.register_author', 'shield.register_adopt', 'shield.register_approve', 'shield.register_withdraw', 'shield.register_enforcement', 'shield.register_removal',
                  'shield.register_removal_countersign', 'shield.register_removal_apply', 'shield.vault_intake', 'shield.stage', 'shield.separate', 'shield.reader_read', 'shield.reader_start',
                  'shield.reader_revoke', 'shield.reader_stop'}
TENANT = 'tenant-SYNTHETIC-a7-' + uuid.uuid4().hex[:6]
PRINCIPAL = 'operator-SYNTHETIC-a7'
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pensive-goodall-6.preview.emergentagent.com').rstrip('/')
_LOOP = asyncio.new_event_loop()


def run(coro):
    asyncio.set_event_loop(_LOOP); return _LOOP.run_until_complete(coro)


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    for key, sub in (('WATCH_OBSERVATIONS_DIR', 'obs'), ('WATCH_VERDICTS_DIR', 'verdicts'), ('WATCH_ACTIONS_DIR', 'actions'), ('WATCH_MARKS_DIR', 'marks'), ('WATCH_SEVER_SIGNALS_DIR', 'signals'),
                     ('MIRAGES_DIR', 'mirages'), ('MIRAGE_TOUCHES_DIR', 'touches'), ('WATCH_MIRAGE_ARTIFACTS_DIR', 'mirage_artifacts'), ('WITNESS_IDENTITIES_DIR', 'wi'), ('WITNESS_ATTESTATIONS_DIR', 'wa'),
                     ('WITNESS_TAMPER_ALARMS_DIR', 'ta'), ('WATCH_NOTICES_DIR', 'notices'), ('WATCH_DECISIONS_DIR', 'decisions'), ('WATCH_REQUIREMENTS_DIR', 'requirements')):
        monkeypatch.setenv(key, str(tmp_path / sub))
    monkeypatch.setenv('WATCH_CONTAIN_DEFAULT_TTL_SECONDS', '3600'); monkeypatch.setenv('WATCH_GATE_JITTER_PCT', '0')
    from services.synisense.shield import deidentifier as de

    async def passthrough(content, *, tenant_id, purpose=None): return de.DeIdResult(content, {}, {}, 0.0, 0.0, 0)
    monkeypatch.setattr(st, 'deidentify', passthrough)
    reg.ensure_defaults(TENANT)
    yield tmp_path
    d = lab.db(); d.shield_register.delete_many({'tenant_id': TENANT}); d.shield_dual_files.delete_many({'tenant_id': TENANT})


def test_shield_boundaries_are_in_the_watch_inventory():
    assert NEW_BOUNDARIES <= set(gate.PROTECTED_BOUNDARIES)
    register = {r['boundary']: r for r in gate.boundary_register()}
    assert all(register[b]['observed'] and register[b]['mark_check'] for b in NEW_BOUNDARIES)
    assert gate.PROTECTED_BOUNDARIES['shield.stage'].startswith('services.synisense.shield.stage.stage')


def test_sealed_stage_is_an_admitted_crossing_and_a_seam_refusal_a_refused_one(isolated, monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', fixtures.mark(('client_identity', fixtures.CLIENT)))
    art = run(st.stage(question=fixtures.QUESTION, data=fixtures.DOC, tenant_id=TENANT, purpose=fixtures.PURPOSE, actor=PRINCIPAL, retain=False))
    assert art.seal
    with pytest.raises(st.StageRefused) as refused:
        run(st.stage(question='How much does the Nuru Orchard arrangement earn us per month?', data=fixtures.DOC, tenant_id=TENANT, purpose=fixtures.PURPOSE, actor=PRINCIPAL, retain=False))
    assert refused.value.kind == 'joint_reidentification'
    rows = [r for r in gate.rows(TENANT) if r['kind'] == 'crossing']
    assert [(r['boundary'], r['outcome'], r['status'], r['principal_id']) for r in rows] == [('shield.stage', 'admitted', 202, PRINCIPAL), ('shield.stage', 'refused', 409, PRINCIPAL)]
    assert all(len(r['digest']) == 64 for r in rows) and fixtures.CLIENT.lower() not in str(rows).lower(), 'the feed carries digests, never values'


def test_fast_refusals_at_the_stage_mint_a_watch_verdict_and_shape_the_principal(isolated, monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', fixtures.mark(('client_identity', fixtures.CLIENT)))
    t0 = datetime(2026, 10, 5, 17, 0, tzinfo=timezone.utc); clock = [t0]
    monkeypatch.setattr(gate, '_now', lambda: clock[0])
    for n in range(3):
        clock[0] = t0 + timedelta(seconds=n)
        with pytest.raises(st.StageRefused):
            run(st.stage(question='How much does the Nuru Orchard arrangement earn us per month?', data=fixtures.DOC, tenant_id=TENANT, purpose=fixtures.PURPOSE, actor=PRINCIPAL, retain=False))
    detections = [r for r in gate.rows(TENANT) if r['kind'] == 'detection']
    assert [(d['detector'], d['action_class'], d['boundary']) for d in detections] == [('fast_violation', 'shape', 'shield.stage')]
    assert detections[0]['verdict_id'].startswith('mv_gate_') and 'detector=fast_violation' in detections[0]['evidence_ref']


def test_unobservable_crossing_refuses_the_stage_and_seals_nothing(isolated, monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', fixtures.mark(('client_identity', fixtures.CLIENT)))

    def broken(tenant_id, row): raise gate.GateUnobservable('observation_write_failed — OSError')
    monkeypatch.setattr(gate, '_append', broken)
    with pytest.raises(st.StageRefused) as refused:
        run(st.stage(question=fixtures.QUESTION, data=fixtures.DOC, tenant_id=TENANT, purpose=fixtures.PURPOSE, actor=PRINCIPAL, retain=False))
    assert refused.value.kind == 'unobservable'


def test_live_refused_register_act_lands_in_the_tenant_feed():
    r = requests.post(f'{BASE_URL}/api/auth/login', json={'email': 'demo.dpo@demo.rms.example.com', 'password': 'demo-dpo-pw'}, timeout=20)
    if r.status_code != 200: pytest.skip('DPO login unavailable')
    headers = {'Authorization': f"Bearer {r.json()['access_token']}"}
    name = 'synthetic_a7_absent_' + uuid.uuid4().hex[:6]
    before = len([x for x in gate.rows('RMS') if x['kind'] == 'crossing' and x['boundary'] == 'shield.register_withdraw'])
    r = requests.post(f'{BASE_URL}/api/shield/register/{name}/withdraw', headers=headers, json={'reason': 'WP-A7 drill: absent name'}, timeout=30)
    if r.status_code == 429 and 'Watch' in r.text:  # the demo DPO is under Watch friction from earlier negative probes: honoured, then one retry
        time.sleep(31); r = requests.post(f'{BASE_URL}/api/shield/register/{name}/withdraw', headers=headers, json={'reason': 'WP-A7 drill: absent name'}, timeout=30)
    if r.status_code == 409 and 'suspended by the Watch' in r.text: pytest.skip('drill principal contained by the Watch (M2 slow_play): ' + r.json().get('detail', '')[:160])
    assert r.status_code == 404, r.text
    after = [x for x in gate.rows('RMS') if x['kind'] == 'crossing' and x['boundary'] == 'shield.register_withdraw']
    assert len(after) == before + 1 and after[-1]['outcome'] == 'refused' and after[-1]['status'] == 404 and name not in str(after[-1])
