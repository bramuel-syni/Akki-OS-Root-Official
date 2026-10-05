"""WP-A3 — pre-redaction objective capture, frozen and consumed downstream (Doc 1 B5.1–B5.5 [B82–B87], B6 [B89–B93]).

Offline (reader FAKED at the control-plane seam, SYNTHETIC questions, scratch tenant cleaned up): capture → frozen artefact; idempotent for
the same question; a changed question on the same request is refused as frozen (B84); `revise` is the explicit non-path; a tampered record
fails `verify` (B92); incoherent → `ask` for a human, `refuse` for a system caller; reader unavailable → refuse (never a fallback); an
objective that repeats an enforced register value is refused (B90); the chat journey captures BEFORE the scope check and BEFORE the answer
crossing (B82/B89) and both consume the SAME artefact id (B91); observations are append-only and divergence is reported (B85).
Live (skips when the reader is not serving): one real contained read of a SYNTHETIC question → coherent, privileged-free bounded objective."""
import asyncio
import json
import os
import sys
import uuid

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.chat import answer as answering, decision as deciding, journey, sessions, spine, window as windowing  # noqa: E402
from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.synisense.shield import objective_capture as oc  # noqa: E402
from services.synisense.shield import semantic_register as reg  # noqa: E402
from services.training_lab import store as lab  # noqa: E402

TENANT = 'tenant-SYNTHETIC-a3-' + uuid.uuid4().hex[:6]
SCOPE = {'tenant_id': TENANT, 'principal_id': 'principal-SYNTHETIC-a3', 'roles': ['operator']}
QUESTION = 'Which training questions from Zinnia Grove Test Cooperative were about minerals, and what did farmers ask most?'
READING = {'objective': {'intent': 'summarise', 'bounded_objective': 'Summarise which training questions from a named cooperative concerned minerals and what farmers asked most', 'coherent': True},
           'meaning': 'A request to summarise the themes of farmer training questions for one client.', 'privileged': [{'category': 'client_identity', 'span': 'Zinnia Grove Test Cooperative', 'reason': 'names the client'}],
           'indirect_disclosures': [], 'safe_rewrite': 'Which training questions from [PARTY] were about minerals, and what did farmers ask most?'}
_LOOP = asyncio.new_event_loop()


def run(coro):
    asyncio.set_event_loop(_LOOP); return _LOOP.run_until_complete(coro)


@pytest.fixture(autouse=True)
def _motor_on_this_loop(monkeypatch):
    """`core.db` is a module-level Motor client bound to whichever loop first used it; in a multi-module session another module's loop may
    own it. Bind a fresh client to this module's loop for the chat journey (sessions/spine read `db` at import)."""
    import core
    from motor.motor_asyncio import AsyncIOMotorClient
    from services.chat import sessions as _sessions, spine as _spine
    asyncio.set_event_loop(_LOOP)
    client = AsyncIOMotorClient(os.environ['MONGO_URL'], io_loop=_LOOP)
    fresh = client[os.environ['DB_NAME']]
    for mod in (core, _sessions, _spine): monkeypatch.setattr(mod, 'db', fresh)
    yield
    client.close()


def fake_read(reading=READING, log=None, label='capture'):
    def _read(text, categories, purpose, **_):
        if log is not None: log.append(label)
        assert text and isinstance(categories, list) and 'objective_capture' in purpose and 'Zinnia' not in purpose
        return {'reading': json.loads(json.dumps(reading)), 'seconds': 0.1, 'lineage': {'model_id': 'contained-reader-SYNTHETIC', 'weight_sha256': 'f' * 64, 'host': 'synthetic-host'}, 'receipt_id': 'gpurcp-synthetic', 'chars': len(text)}
    return _read


@pytest.fixture(autouse=True, scope='module')
def _cleanup():
    yield
    d = lab.db()
    d.shield_objectives.delete_many({'tenant_id': TENANT}); d.shield_objective_observations.delete_many({'tenant_id': TENANT}); d.shield_register.delete_many({'tenant_id': TENANT})
    d[sessions.COLLECTION].delete_many({'tenant_id': TENANT})  # sync client: the per-test Motor binding is gone by module teardown


# ----------------------------------------------------------------------------- the artefact
def test_capture_freezes_one_artifact_idempotent_and_refuses_a_changed_question(monkeypatch):
    monkeypatch.setattr(oc.reader, 'read', fake_read())
    rid = 'req-' + uuid.uuid4().hex[:8]
    art = oc.capture(QUESTION, TENANT, rid, caller='human')
    assert art['artifact_id'].startswith('obj-') and art['request_id'] == rid and art['coherent'] is True and art['declared_intent'] == art['intent'] == 'summarise'
    assert art['sequence_position'] == 'before_deidentify' and 'Zinnia' not in art['bounded_objective'] and art['privileged_spans'] == 1 and len(art['sha256']) == 64
    assert art['categories_declared'] >= 1 and art['reader']['model_id'] == 'contained-reader-SYNTHETIC' and art['reader']['receipt_id'] == 'gpurcp-synthetic'
    again = oc.capture(QUESTION, TENANT, rid, caller='human')
    assert again['artifact_id'] == art['artifact_id'] and again['sha256'] == art['sha256']
    with pytest.raises(oc.ObjectiveFrozen, match='new request'):
        oc.capture(QUESTION + ' And the fees?', TENANT, rid, caller='human')
    with pytest.raises(oc.ObjectiveFrozen):
        oc.revise(art['artifact_id'], bounded_objective='something else')
    assert oc.verify(art['artifact_id'])['sha256'] == art['sha256']


def test_tampered_record_fails_verification_and_cannot_be_consumed(monkeypatch):
    monkeypatch.setattr(oc.reader, 'read', fake_read())
    art = oc.capture(QUESTION, TENANT, 'req-' + uuid.uuid4().hex[:8], caller='system')
    lab.db().shield_objectives.update_one({'artifact_id': art['artifact_id']}, {'$set': {'bounded_objective': 'rewritten to match whatever came back'}})
    with pytest.raises(oc.ObjectiveTampered):
        oc.verify(art['artifact_id'])
    with pytest.raises(oc.ObjectiveTampered):
        oc.observe(art['artifact_id'], 'turn', {'decision': 'warm'})


def test_failure_outcomes_are_defined_never_a_guess(monkeypatch):
    incoherent = {**READING, 'objective': {'intent': 'unclear', 'bounded_objective': 'The request asks to both delete and preserve the same records', 'coherent': False}}
    monkeypatch.setattr(oc.reader, 'read', fake_read(incoherent))
    with pytest.raises(oc.ObjectiveNotCaptured) as human:
        oc.capture('Delete everything but keep it all, then neither.', TENANT, 'req-' + uuid.uuid4().hex[:8], caller='human')
    assert human.value.outcome == 'ask' and human.value.kind == 'incoherent' and 'delete and preserve' in human.value.reason
    with pytest.raises(oc.ObjectiveNotCaptured) as system:
        oc.capture('Delete everything but keep it all, then neither.', TENANT, 'req-' + uuid.uuid4().hex[:8], caller='system')
    assert system.value.outcome == 'refuse'
    assert oc.for_request(system.value.__class__.__name__) is None  # nothing fabricated was stored

    def unavailable(*a, **k): raise cr.ReaderUnavailable('contained-reader is not serving (job failed)')
    monkeypatch.setattr(oc.reader, 'read', unavailable)
    with pytest.raises(oc.ObjectiveNotCaptured) as down:
        oc.capture(QUESTION, TENANT, 'req-' + uuid.uuid4().hex[:8], caller='human')
    assert down.value.outcome == 'refuse' and down.value.kind == 'reader_unavailable' and 'no external model' in down.value.reason

    leaky = {**READING, 'objective': {**READING['objective'], 'bounded_objective': 'Summarise the Zinnia Grove Test Cooperative questions'}}
    monkeypatch.setattr(oc.reader, 'read', fake_read(leaky))
    with pytest.raises(oc.ObjectiveNotCaptured) as unsafe:
        oc.capture(QUESTION, TENANT, 'req-' + uuid.uuid4().hex[:8], caller='human')
    assert unsafe.value.kind == 'unsafe_reading' and unsafe.value.outcome == 'refuse'
    with pytest.raises(oc.ObjectiveNotCaptured) as empty:
        oc.capture('   ', TENANT, 'req-' + uuid.uuid4().hex[:8], caller='system')
    assert empty.value.kind == 'empty' and empty.value.outcome == 'refuse'


def test_enforced_register_value_in_the_objective_is_refused(monkeypatch):
    reg.ensure_defaults(TENANT)
    reg.author(TENANT, 'dpo-SYNTHETIC', {'name': 'synthetic_codenames', 'kind': 'exact', 'action': 'abstract', 'enforcement': 'enforced', 'values': ['Mango Halo'], 'description': 'SYNTHETIC code names'})
    reg.approve(TENANT, 'dpo-SYNTHETIC-2', 'synthetic_codenames')
    leaky = {**READING, 'privileged': [], 'objective': {**READING['objective'], 'bounded_objective': 'Plan the launch of Mango Halo for the committee'}}
    monkeypatch.setattr(oc.reader, 'read', fake_read(leaky))
    with pytest.raises(oc.ObjectiveNotCaptured) as unsafe:
        oc.capture('Plan the launch of Mango Halo for the committee', TENANT, 'req-' + uuid.uuid4().hex[:8], caller='human')
    assert unsafe.value.kind == 'unsafe_reading'


def test_observations_append_only_and_divergence_reported(monkeypatch):
    monkeypatch.setattr(oc.reader, 'read', fake_read())
    art = oc.capture(QUESTION, TENANT, 'req-' + uuid.uuid4().hex[:8])
    first = oc.observe(art['artifact_id'], 'turn', {'turn_id': 't1', 'decision': 'warm', 'grounding': 'cited_in_window', 'citations_dropped': 0})
    assert first['observation']['divergence'] == [] and first['intent_audit']['declared_situation_class'] == 'summarise' and len(first['intent_audit']['demonstrated_observations']) == 1
    assert oc.divergence(art['artifact_id'])['diverged'] is False
    second = oc.observe(art['artifact_id'], 'turn', {'turn_id': 't2', 'decision': 'warm', 'grounding': 'partially_cited', 'citations_dropped': 2})
    assert second['observation']['divergence'] == ['grounding_outside_window'] and len(second['intent_audit']['demonstrated_observations']) == 2
    third = oc.observe(art['artifact_id'], 'turn', {'turn_id': 't3', 'decision': 'refused', 'reason': 'out_of_scope', 'follow_up': True})
    assert 'scope_drift' in third['observation']['divergence']
    div = oc.divergence(art['artifact_id'])
    assert div['diverged'] is True and div['observations'] == 3 and {d['flag'] for d in div['divergent']} == {'grounding_outside_window', 'scope_drift'} and div['declared_intent'] == 'summarise'
    assert oc.verify(art['artifact_id'])['sha256'] == art['sha256']  # the artefact itself never moved


# ----------------------------------------------------------------------------- the journey: capture precedes everything; one artefact consumed downstream
def test_chat_journey_captures_before_scope_check_and_crossing_and_consumes_one_artifact(monkeypatch):
    log, seen = [], {}
    monkeypatch.setattr(oc.reader, 'read', fake_read(log=log))

    async def no_artefacts(db_, scope): log.append('read_artefacts'); return []

    async def one_candidate(db_, scope, artefacts, terms, pinned=()):
        unit = {'unit_id': 'u1', 'provenance': {'locator': 'synthetic://u1'}, 'defensibility': {'defensibility_class': 'utterance'}}
        return {'candidates': [{'ref': 'akki://unit/t/r/u1', 'unit_id': 'u1', 'unit': unit, 'position': 0, 'overlap': 3, 'kind': 'matched', 'rel_keys': [], 'content_sha256': 'c' * 64, 'region': 'db.training_questions', 'artifact_ref': 'a1', 'request_id': 'r', 'class_label': 'utterance', 'reextraction_ref': 'x'}],
                'calls': 1, 'qualified_bytes_read': 10, 'matched_total': 1, 'units_total': 1, 'failures': []}

    async def fake_route(**kw):
        log.append('scope_check'); seen['route_artifact_ref'] = kw['artifact_ref']
        return {'decision': 'warm', 'reason': 'warm_units', 'ledger_row': {'row_id': 'led-synthetic'}}

    class Window:
        selected_refs = ('akki://unit/t/r/u1',); load_bearing_refs = ('akki://unit/t/r/u1',); excluded_counts = {}; top_excluded_handles = (); window_tokens = 1000; reserved_tokens = 100
        tokenizer_sha256 = 's' * 64; ranking_rule_ref = 'rule'; objective_sha256 = 'o' * 64; loss_disclosed = True

    def fake_build(**kw):
        return Window(), [{'ref': 'akki://unit/t/r/u1', 'region': 'db.training_questions', 'class_label': 'utterance', 'tokens': 20, 'proximity': 1.0, 'position': 0, 'content_sha256': 'c' * 64, 'unit': {'provenance': {'locator': 'synthetic://u1'}}, 'text': '{"q": "minerals"}'}], []

    class Accessor:
        plane_id = 'plane-synthetic'
        async def list_working_set(self): return []

    async def fake_plane(scope): return Accessor()
    async def fake_touch(accessor, refs): return {'plane_id': 'plane-synthetic', 'hits': 0, 'misses': len(refs), 'hot_refs_before': 0, 'hot_refs_after': len(refs), 'evicted': 0}

    async def fake_answer(*, scope, session, question, context_lines, selected, model, provider, actor):
        log.append('crossing'); seen['prompt'] = answering.prompt_for(objective=session['objective']['bounded_objective'], context_lines=context_lines, question=question, selected=selected, objective_ref=session['objective']['artifact_id'])
        seen['session_objective'] = session['objective']
        return {'refused': False, 'answer': 'Farmers asked about mineral licks.', 'cited_refs': ['akki://unit/t/r/u1'], 'sufficient': True, 'grounding': 'cited_in_window', 'unsupported': '', 'citations_dropped': 0,
                'objective_ref': session['objective']['artifact_id'], 'receipt_id': 'rcp-synthetic', 'model_id': model, 'provider': provider, 'tokens_in': 1, 'tokens_out': 1, 'latency_ms': 1, 'shield': None, 'prompt_chars': 10}

    async def no_converge(*a, **k): log.append('converge'); seen['converge_ref'] = k.get('objective_ref') or (a[3] if len(a) > 3 else None)

    monkeypatch.setattr(spine, 'verified_artefacts', no_artefacts); monkeypatch.setattr(spine, 'read_candidates', one_candidate)
    monkeypatch.setattr(spine, 'chat_plane', fake_plane); monkeypatch.setattr(spine, 'touch_working_set', fake_touch)
    monkeypatch.setattr(deciding.gate, 'route', fake_route); monkeypatch.setattr(windowing, 'build', fake_build); monkeypatch.setattr(windowing, 'loss_statement', lambda w, r: 'nothing lost (SYNTHETIC)')
    monkeypatch.setattr(answering, 'answer', fake_answer); monkeypatch.setattr(journey, '_converge', no_converge)
    monkeypatch.setattr(journey.critic_seam, 'route_through_seam', lambda **k: {'seam_attested': True}); monkeypatch.setattr(journey.critic_seam, 'verdict_summary', lambda v: v)

    out = run(journey.ask(sessions.db, SCOPE, question=QUESTION))
    assert log[0] == 'capture' and log.index('capture') < log.index('scope_check') < log.index('crossing'), log  # B82/B89: extraction first, before the scope check and the crossing
    art = out['objective']
    assert art['artifact_id'].startswith('obj-') and art['text'] == QUESTION and 'Zinnia' not in art['bounded_objective']
    assert seen['route_artifact_ref']['artifact_id'] == art['artifact_id'] == out['turn']['evidence']['objective_ref'] == out['turn']['decision_detail']['objective_ref'] == seen['converge_ref']  # B91: one artefact, by reference
    assert f"artefact {art['artifact_id']}" in seen['prompt'] and art['bounded_objective'] in seen['prompt'] and 'Zinnia Grove Test Cooperative' not in seen['prompt'].split('QUESTION:')[0]  # B83: the objective that crosses is the bounded one
    assert out['turn']['evidence']['intent']['declared_intent'] == 'summarise' and out['turn']['evidence']['intent']['observations'] == 1 and out['turn']['evidence']['intent']['diverged'] is False
    assert oc.verify(art['artifact_id'])['request_id'] == out['session_id']

    # a follow-up consumes the same frozen artefact; no second capture (log gains no 'capture')
    before = log.count('capture')
    follow = run(journey.ask(sessions.db, SCOPE, question='Which of those were about minerals specifically?', session_id=out['session_id']))
    assert log.count('capture') == before and follow['turn']['evidence']['objective_ref'] == art['artifact_id'] and follow['turns'] == 2
    assert follow['turn']['evidence']['intent']['observations'] == 2


def test_chat_journey_asks_instead_of_guessing_and_opens_no_session(monkeypatch):
    incoherent = {**READING, 'objective': {'intent': 'unclear', 'bounded_objective': 'The question contradicts itself about which period to cover', 'coherent': False}}
    monkeypatch.setattr(oc.reader, 'read', fake_read(incoherent))

    async def must_not_run(*a, **k): raise AssertionError('nothing may be read before an objective exists')
    monkeypatch.setattr(spine, 'verified_artefacts', must_not_run)
    out = run(journey.ask(sessions.db, SCOPE, question='Cover last year but only this year, and neither.'))
    assert out['session_id'] is None and out['outcome'] == 'ask' and out['turn']['decision'] == 'ask' and out['turn']['refused'] is True
    assert 'clarify' in out['turn']['refusal_reason'].lower() and out['turn']['evidence']['reads']['source_dispatches'] == 0 and out['turn']['objective_capture']['kind'] == 'incoherent'
    assert run(sessions.listing(SCOPE)) == [s for s in run(sessions.listing(SCOPE)) if s['objective'].get('artifact_id')]  # no session without an artefact was opened

    def unavailable(*a, **k): raise cr.ReaderUnavailable('not serving')
    monkeypatch.setattr(oc.reader, 'read', unavailable)
    out = run(journey.ask(sessions.db, SCOPE, question=QUESTION))
    assert out['session_id'] is None and out['outcome'] == 'refuse' and out['turn']['objective_capture']['kind'] == 'reader_unavailable'


# ----------------------------------------------------------------------------- live: one real contained read of a SYNTHETIC question
def test_live_capture_with_the_contained_reader_is_coherent_and_privileged_free():
    st = cr.status()
    if st.get('status') != 'running':
        pytest.skip(f"contained reader not serving: {st.get('status')}")
    rid = 'req-live-' + uuid.uuid4().hex[:8]
    art = oc.capture(QUESTION, TENANT, rid, caller='human')
    assert art['coherent'] is True and art['bounded_objective'] and 'zinnia' not in art['bounded_objective'].lower() and 'zinnia' not in art['meaning'].lower()
    assert art['reader']['host'] and art['reader']['receipt_id'] and art['reader']['seconds'] is not None and art['reader']['model_id'] == cr.MODEL_ID
    assert oc.verify(art['artifact_id'])['sha256'] == art['sha256']
    assert os.environ.get('M9_REMOTE_ROOT')  # the read crossed the sealed seam, not a local model
