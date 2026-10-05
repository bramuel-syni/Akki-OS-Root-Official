"""WP-A5 — Shield as a discrete sealed stage; dual-file seam; the chokepoint verifies the seal (Doc 1 A5.2 B36–B39, A5.3 B40–B41, A5.6 B46 ·
Doc 2 B5.1–B5.6 B65–B85).

Offline (reader FAKED at the control-plane seam, external client FAKED, SYNTHETIC texts, scratch tenant cleaned up): two files assessed in
separate passes with no shared context (B66/B76) — altering File 2 cannot change File 1's assessment; one value → one token across the pair
and a colliding token is renumbered, never guessed; the seam refuses a dropped marker (B67/B77) and a pair that jointly re-identifies what
each withheld (B73/B74); the chokepoint refuses an unsealed estate payload, a tampered seal, a purpose mismatch and a spent artifact (B72),
sends exactly one query with the two-item context, re-checks the outbound at consumption, rebinds locally and destroys the mapping (B40);
both files are retained in full under their own custody class and masked at every later read (B71); every live caller crosses through the
stage (static scan) and the sole-invocation scan stays green. Live (skips when the reader is not serving): one real staged pair."""
import asyncio
import json
import os
import re
import sys
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.chokepoint import llm  # noqa: E402
from services.synisense.shield import category3 as c3  # noqa: E402
from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.synisense.shield import semantic_register as reg  # noqa: E402
from services.synisense.shield import stage as st  # noqa: E402
from services.training_lab import store as lab  # noqa: E402

TENANT = 'tenant-SYNTHETIC-a5-' + uuid.uuid4().hex[:6]
ACTOR = 'operator-SYNTHETIC-a5'
PURPOSE = 'chat.governed_answer'
CLIENT, CLIENT_2, PROJECT = 'Nuru Orchard Test Cooperative', 'Zinnia Grove Test Cooperative', 'Papaya Comet'
DOC = (f'SYNTHETIC CONTRACT. Our counterparty for this engagement is {CLIENT}, trading under the internal label {PROJECT}. '
       'The reserve fee is KES 147300 and the bid is computed as 0.73 times the rival floor. Deliveries happen on Mondays.')
QUESTION = 'Which deliverables does the counterparty owe in the first quarter, and on which weekday are deliveries made?'
SYSTEM = 'You are a governed answerer. Use only the data item. Reply with one JSON object.'
SEEDED = [CLIENT, CLIENT_2, PROJECT]  # enforced by default; commercial figures are advisory until the DPO enforces them
_LOOP = asyncio.new_event_loop()


def run(coro):
    asyncio.set_event_loop(_LOOP); return _LOOP.run_until_complete(coro)


def _reading(privileged=(), bounded='Answer a question about deliverables from the supplied contract data'):
    return {'objective': {'intent': 'answer', 'bounded_objective': bounded, 'coherent': True, 'requests_privileged': False}, 'meaning': 'A grounded question over a commercial agreement.', 'privileged': [dict(p) for p in privileged], 'indirect_disclosures': [], 'safe_rewrite': 'Answer the question from [PARTY]\'s agreement.'}


def mark(*values):
    """A reader that marks exactly the given (category, value) pairs present in whatever text it is asked to read; records every read."""
    log = []

    def _read(text, categories, purpose, **_):
        log.append({'text': text, 'purpose': purpose, 'categories': [c['name'] for c in categories]})
        found = [{'category': cat, 'span': value, 'reason': 'declared meaning'} for cat, value in values if value.lower() in text.lower()]
        return {'reading': _reading(found), 'seconds': 0.05, 'lineage': {'model_id': 'contained-reader-SYNTHETIC', 'weight_sha256': 'f' * 64, 'host': 'synthetic-host'}, 'receipt_id': 'gpurcp-synthetic-' + uuid.uuid4().hex[:6], 'chars': len(text)}
    _read.log = log
    return _read


def _no_values(obj):
    blob = json.dumps(obj, ensure_ascii=False, default=str).lower()
    return [s for s in SEEDED if s.lower() in blob]


class _FakeClient:
    sent = []

    def __init__(self, **kw): self.system_message = kw.get('system_message')

    def with_model(self, *a, **k): return self

    def with_params(self, **k): return self

    async def send_message(self, msg):
        _FakeClient.sent.append((self.system_message, msg.text))
        tokens = sorted(set(re.findall(r'\[[A-Z]+_\d+\]|\[\[ENT_[A-Z]+_\d+\]\]', msg.text)))
        return json.dumps({'answer': f"Deliveries for {' / '.join(tokens) or 'the party'} are on Mondays.", 'cited_units': [], 'sufficient': True, 'unsupported': ''})


@pytest.fixture(autouse=True, scope='module')
def _tenant():
    reg.ensure_defaults(TENANT)
    yield
    d = lab.db(); d.shield_register.delete_many({'tenant_id': TENANT}); d.shield_dual_files.delete_many({'tenant_id': TENANT})


def _tokens(art, value):
    return sorted(t for m in (art.binding_map, art.entity_map) for t, v in m.items() if str(v).lower() == value.lower())


@pytest.fixture
def no_ner(monkeypatch):
    """Isolate the stage/seam logic from the NER layer (which has its own suite): the de-identifier passes text through unchanged."""
    from services.synisense.shield import deidentifier as de

    async def passthrough(content, *, tenant_id, purpose=None): return de.DeIdResult(content, {}, {}, 0.0, 0.0, 0)
    monkeypatch.setattr(st, 'deidentify', passthrough)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(llm, '_client_factory', lambda **kw: _FakeClient(**kw)); monkeypatch.setattr(llm, '_emergent_api_key', lambda: 'test-key'); _FakeClient.sent.clear()
    return _FakeClient


# ----------------------------------------------------------------------------- B65/B66/B76: two files, two separate passes, no shared context
def test_two_files_are_assessed_in_separate_passes_and_sealed_with_full_retention(monkeypatch, no_ner):
    reader = mark(('client_identity', CLIENT), ('private_project_name', PROJECT)); monkeypatch.setattr(c3.reader, 'read', reader)
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, objective_ref='obj-synthetic', session_id='cs-synthetic'))
    assert len(reader.log) == 2, 'one read per file, no joined read'
    assert QUESTION not in reader.log[1]['text'] and DOC not in reader.log[0]['text'] and SYSTEM in reader.log[0]['text'], 'File 2 is read without File 1 as an input and vice versa (B66)'
    assert st.verify(art, tenant_id=TENANT, purpose=PURPOSE, custody_class='tenant_estate') is None and len(art.seal) == 64
    assert len(art.safe_items) == 2 and not _no_values(art.safe_items) and not _no_values(art.safe_system or '') and '[PARTY_1]' in art.safe_items[1] and '[PROJECT_1]' in art.safe_items[1]
    assert art.binding_map['[PARTY_1]'] == CLIENT and art.binding_map['[PROJECT_1]'] == PROJECT and set(art.protected_values) >= {CLIENT, PROJECT}
    assert '[ITEM 1 — QUESTION AS ASKED]' in art.render() and '[ITEM 2 — DATA]' in art.render() and art.objective_ref == 'obj-synthetic'
    files = art.receipt['files']
    assert [f['file'] for f in files] == [st.FILE_1, st.FILE_2] and files[1]['enforced'] == {'client_identity': 1, 'private_project_name': 1} and files[1]['clean'] and files[0]['clean']
    assert art.receipt['seam']['joint']['passes'] and all(r['clean_at_seam'] for r in art.receipt['seam']['rechecks']) and not _no_values(art.receipt) and not _no_values(art.summary())
    retained = lab.db().shield_dual_files.find_one({'artifact_id': art.artifact_id}, {'_id': 0})
    assert retained['custody_class'] == st.CUSTODY_RETAINED and [f['text'] for f in retained['files']] == [QUESTION, DOC], 'both files retained in full (B71)'
    assert 'binding_map' not in json.dumps(retained) and '[PARTY_1]' not in json.dumps(retained['receipt']), 'the mapping envelope is never persisted (B40/B68)'


def test_altering_file_2_cannot_change_file_1_assessment(monkeypatch, no_ner):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT), ('client_identity', CLIENT_2)))
    a = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, retain=False))
    b = run(st.stage(question=QUESTION, data=DOC.replace(CLIENT, CLIENT_2) + ' Penalty clause 14 applies.', tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, retain=False))
    assert a.safe_items[0] == b.safe_items[0] and a.safe_system == b.safe_system
    assert {k: v for k, v in a.receipt['files'][0].items() if k != 'reader'} == {k: v for k, v in b.receipt['files'][0].items() if k != 'reader'}
    assert a.safe_items[1] != b.safe_items[1] and a.binding_map['[PARTY_1]'] == CLIENT and b.binding_map['[PARTY_1]'] == CLIENT_2


# ----------------------------------------------------------------------------- B67: the seam unifies, renumbers, re-checks and can refuse
def test_seam_unifies_one_value_one_token_and_renumbers_a_colliding_token(monkeypatch, no_ner):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT), ('client_identity', CLIENT_2), ('private_project_name', PROJECT)))
    same = run(st.stage(question=f'What does {CLIENT} owe this quarter?', data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert same.safe_items[0].count('[PARTY_1]') == 1 and same.safe_items[1].count('[PARTY_1]') == 1 and list(same.binding_map.values()).count(CLIENT) == 1
    both = run(st.stage(question=f'Does {CLIENT_2} owe more than {CLIENT} this quarter?', data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert both.binding_map['[PARTY_1]'] == CLIENT_2 and both.binding_map['[PARTY_2]'] == CLIENT and '[PARTY_2]' in both.safe_items[1] and '[PARTY_1]' not in both.safe_items[1] and both.receipt['seam']['unified'] == 1, 'File 2\'s [PARTY_1] names the value File 1 already bound as [PARTY_2]: one value, one token'
    other = run(st.stage(question=f'Compare this with what {CLIENT_2} owes.', data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert '[PARTY_1]' in other.safe_items[0] and '[PARTY_2]' in other.safe_items[1] and '[PARTY_1]' not in other.safe_items[1], 'the data file\'s colliding token is renumbered'
    assert other.binding_map['[PARTY_1]'] == CLIENT_2 and other.binding_map['[PARTY_2]'] == CLIENT and other.receipt['seam']['renumbered'] == 1
    assert st.rebind('[PARTY_1] vs [PARTY_2] under [PROJECT_1]', other) == f'{CLIENT_2} vs {CLIENT} under {PROJECT}'


def test_seam_rebinds_a_value_one_file_withheld_that_survives_in_the_other(monkeypatch, no_ner):
    """Independent reads diverge (seen live 5 Oct: the reader marked the role noun 'counterparty' in File 1 only): the seam re-associates the
    literal under File 1's token instead of refusing; a file's own leaked value (dropped marker) still refuses."""
    def divergent(text, categories, purpose, **_):
        found = [{'category': 'client_identity', 'span': 'counterparty', 'reason': 'role'}] if purpose.endswith(st.FILE_1) and 'counterparty' in text else []
        found += [{'category': 'client_identity', 'span': CLIENT, 'reason': 'declared'}] if CLIENT in text else []
        return {'reading': _reading(found), 'seconds': 0.05, 'lineage': {'model_id': 'contained-reader-SYNTHETIC', 'weight_sha256': 'f' * 64, 'host': 'synthetic-host'}, 'receipt_id': 'gpurcp-synthetic-x', 'chars': len(text)}
    monkeypatch.setattr(c3.reader, 'read', divergent)
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, retain=False))
    assert 'counterparty' not in art.render().lower() and CLIENT.lower() not in art.render().lower()
    assert art.receipt['seam']['cross_bound'] == {st.FILE_2: 1} and all(r['clean_at_seam'] for r in art.receipt['seam']['rechecks'])
    q_token = _tokens(art, 'counterparty')[0]; c_token = _tokens(art, CLIENT)[0]
    assert q_token != c_token and q_token in art.safe_items[0] and q_token in art.safe_items[1] and c_token in art.safe_items[1]
    assert st.rebind(f'{q_token} is {c_token}', art) == f'counterparty is {CLIENT}'


def test_seam_refuses_a_dropped_marker_and_a_joint_reidentification(monkeypatch, no_ner):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT)))
    with pytest.raises(st.StageRefused) as joint:
        run(st.stage(question='How much does the Nuru Orchard arrangement earn us per month?', data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert joint.value.kind == 'joint_reidentification' and joint.value.detail['groups'][0]['withheld_in'] == st.FILE_2 and not _no_values(joint.value.detail), 'File 1 kept two distinctive words of a value File 2 withheld (B74)'
    real_assess = st._assess

    async def leaky(label, system_message, text, tenant_id, purpose, custody_class):
        out = await real_assess(label, system_message, text, tenant_id, purpose, custody_class)
        if label == st.FILE_2: out['safe'] = out['safe'] + f' (ref: {CLIENT})'  # the marker says clean; the text no longer is — the seam must catch it, not trust the assessment
        return out
    monkeypatch.setattr(st, '_assess', leaky)
    with pytest.raises(st.StageRefused) as dropped:
        run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert dropped.value.kind == 'seam_marker_failed' and dropped.value.detail['rechecks'][-1]['clean_at_seam'] is False and dropped.value.detail['rechecks'][-1]['marker_clean_at_assessment'] is True


def test_reader_unavailable_or_ambiguous_refuses_the_stage_before_anything_external(monkeypatch, client):
    def down(*a, **k): raise cr.ReaderUnavailable('not serving')
    monkeypatch.setattr(c3.reader, 'read', down)
    with pytest.raises(st.StageRefused) as refused:
        run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert refused.value.kind == 'file_refused' and 'register_reader_unavailable' in refused.value.reason and not client.sent
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', 'Nuru Orchard Cooperative Ltd (paraphrased)')))
    monkeypatch.setattr(c3.reader, 'read', lambda text, categories, purpose, **_: {'reading': _reading([{'category': 'client_identity', 'span': 'Nuru Orchard Cooperative Limited', 'reason': 'paraphrased'}]), 'seconds': 0.0, 'lineage': {}, 'receipt_id': 'gpurcp-x', 'chars': len(text)})
    with pytest.raises(st.StageRefused) as ambiguous:
        run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    assert 'register_cat3_ambiguous' in ambiguous.value.reason
    synthetic = run(st.stage(question='SYNTHETIC connectivity text', tenant_id=TENANT, purpose='routing.candidate_trial', actor=ACTOR, custody_class='synthetic'))
    assert synthetic.receipt['files'][0]['reader']['applied'] is False and synthetic.receipt['retained'] is False


# ----------------------------------------------------------------------------- the chokepoint: verifies the seal, one query, local rebinding, mapping destroyed
def test_chokepoint_verifies_the_seal_sends_one_two_item_query_rebinds_and_destroys_the_mapping(monkeypatch, client):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT), ('private_project_name', PROJECT)))
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, session_id='cs-synthetic'))
    assert _tokens(art, CLIENT) and _tokens(art, PROJECT) and not _no_values(art.safe_items), 'NER first, register second: the value is bound under one of the two maps either way'
    resp = run(llm.invoke(purpose=PURPOSE, safe_artifact=art, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    assert len(client.sent) == 1, 'exactly one external query (B72)'
    sysm, outbound = client.sent[0]
    assert '[ITEM 1 — QUESTION AS ASKED]' in outbound and '[ITEM 2 — DATA]' in outbound and not _no_values(outbound) and not _no_values(sysm)
    assert CLIENT in resp.text and CLIENT not in (resp.text_as_returned or '') and re.search(r'\[[A-Z]+_\d+\]|\[\[ENT_[A-Z]+_\d+\]\]', resp.text_as_returned or ''), 'rebound locally; the placeholder form is what came back'
    assert resp.safe_artifact_id == art.artifact_id and art.consumed['receipt_id'] == resp.receipt_id and art.binding_map == {} and art.entity_map == {} and art.protected_values == [], 'the mapping died with the call (B40)'
    assert resp.shield['register']['reader']['attested_by_seal'] == art.artifact_id
    assert lab.db().shield_dual_files.find_one({'artifact_id': art.artifact_id})['crossed']['receipt_id'] == resp.receipt_id
    with pytest.raises(llm.ChokepointRefused, match='already consumed'):
        run(llm.invoke(purpose=PURPOSE, safe_artifact=art, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    assert len(client.sent) == 1


def test_chokepoint_refuses_unsealed_tampered_mismatched_and_recheck_failures(monkeypatch, client):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT)))
    with pytest.raises(llm.ChokepointRefused, match='unsealed_payload_refused'):
        run(llm.invoke(purpose=PURPOSE, prompt=DOC, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    with pytest.raises(llm.ChokepointRefused, match='purpose mismatch'):
        run(llm.invoke(purpose='doc_studio.plan', safe_artifact=art, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    assert art.binding_map == {}, 'a refused artifact loses its mapping too'
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    art.safe_items[1] = art.safe_items[1] + ' and ' + CLIENT  # altered after sealing
    with pytest.raises(llm.ChokepointRefused, match='seal mismatch'):
        run(llm.invoke(purpose=PURPOSE, safe_artifact=art, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    forged = st.SafeArtifact(artifact_id='sa-forged', tenant_id=TENANT, purpose=PURPOSE, custody_class='tenant_estate', safe_items=[DOC], safe_system=None, objective_ref=None, receipt={}, protected_digest='', created_at=lab.now(), seal='0' * 64)
    with pytest.raises(llm.ChokepointRefused, match='seal mismatch'):
        run(llm.invoke(purpose=PURPOSE, safe_artifact=forged, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    with pytest.raises(llm.ChokepointRefused, match='ambiguous_payload'):
        run(llm.invoke(purpose=PURPOSE, prompt='x', safe_artifact=forged, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR, retain=False))
    monkeypatch.setattr(st, 'recheck', lambda artifact, text: {'clean': False, 'protected_values_found': ['x'], 'checked': 1})
    with pytest.raises(llm.LLMShieldFailure, match='stage_seam_recheck_failed'):
        run(llm.invoke(purpose=PURPOSE, safe_artifact=art, masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    assert not client.sent, 'nothing crossed in any refusal'
    ok = run(llm.invoke(purpose='llm.connect_verify', prompt='Reply with a single word: ok.', masking_tier='llm_prompt_governed_text', actor=ACTOR, model='gpt-6-astra', provider='emergent', tenant_id='__connect_verify__', custody_class='synthetic'))
    assert ok.safe_artifact_id is None and len(client.sent) == 1, 'a synthetic connectivity check is the one unsealed path'


# ----------------------------------------------------------------------------- B71: retained files are masked at every read
def test_retained_files_are_masked_at_every_read_never_raw(monkeypatch, no_ner):
    monkeypatch.setattr(c3.reader, 'read', mark(('client_identity', CLIENT), ('private_project_name', PROJECT)))
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id=TENANT, purpose=PURPOSE, actor=ACTOR))
    view = run(st.read_retained(art.artifact_id, TENANT, 'auditor-SYNTHETIC'))
    assert view['custody_class'] == st.CUSTODY_RETAINED and [f['file'] for f in view['files']] == [st.FILE_1, st.FILE_2]
    assert not _no_values([f['masked_text'] for f in view['files']]) and 'Deliveries happen on Mondays' in view['files'][1]['masked_text'] and view['files'][1]['sha256'] == art.receipt['files'][1]['sha256_original']
    assert 'text' not in view['files'][1] and lab.db().shield_dual_files.find_one({'artifact_id': art.artifact_id})['reads'][0]['masked'] is True
    with pytest.raises(LookupError):
        run(st.read_retained(art.artifact_id, 'another-tenant', 'auditor-SYNTHETIC'))


def test_single_item_question_renders_as_itself(monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', mark())
    art = run(st.stage(question='{"task": "frame_audit_refinement", "direction_statement": "SYNTHETIC"}', tenant_id='principal-SYNTHETIC', purpose='solva.frame_audit', actor='principal-SYNTHETIC', retain=False))
    assert len(art.safe_items) == 1 and art.render() == art.safe_items[0] and art.receipt['files'][0]['file'] == st.FILE_1
    lab.db().shield_register.delete_many({'tenant_id': 'principal-SYNTHETIC'})


# ----------------------------------------------------------------------------- caller migration: every live caller crosses through the stage; the sole-invocation scan stays green
def test_every_live_caller_passes_a_sealed_artifact_and_the_sole_invocation_scan_is_green():
    root = Path('/app/backend/vendored/extraction_akki/backend')
    unsealed, sealed = [], []
    for path in list((root / 'services').rglob('*.py')) + list((root / 'routers').rglob('*.py')):
        if path.name == 'llm.py' and path.parent.name == 'chokepoint': continue
        src = path.read_text()
        for m in re.finditer(r'\binvoke\(', src):
            if src[max(0, m.start() - 4):m.start()].strip().endswith('def'): continue
            depth, i = 0, m.end() - 1
            while i < len(src):
                depth += src[i] == '('; depth -= src[i] == ')'
                if depth == 0: break
                i += 1
            call = src[m.start():i + 1]
            if 'purpose' not in call: continue  # not a chokepoint call (e.g. a local helper named invoke)
            (sealed if 'safe_artifact=' in call else unsealed).append((str(path.relative_to(root)), call[:60].replace('\n', ' ')))
    assert len(sealed) >= 14, sealed
    assert [u for u in unsealed if 'custody_class="synthetic"' not in u[1] and 'connect_llm_router' not in u[0]] == [], unsealed
    sys.path.insert(0, '/app/backend/tests/invariants')
    from test_llm_chokepoint_sole_importer import sdk_importers  # the restored AST sole-importer negative scan, run in-process
    assert sdk_importers() == []


# ----------------------------------------------------------------------------- live: one real staged pair through the contained reader
def test_live_stage_reads_both_files_inside_the_perimeter():
    s = cr.status()
    if s.get('status') != 'running': pytest.skip(f"contained reader not serving: {s.get('status')}")
    art = run(st.stage(question=QUESTION, data=DOC, tenant_id='RMS', purpose=PURPOSE, actor=ACTOR, system_message=SYSTEM, retain=False))
    assert st.verify(art, tenant_id='RMS', purpose=PURPOSE, custody_class='tenant_estate') is None and len(art.receipt['reader_receipts']) >= 2 and art.receipt['reader_spans'] >= 1
    assert CLIENT.lower() not in art.render().lower() and PROJECT.lower() not in art.render().lower() and os.environ.get('M9_REMOTE_ROOT')
