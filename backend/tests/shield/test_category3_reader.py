"""WP-A4 — Category-3 contained recogniser; reconstruction; cue-regex demoted (Doc 2 A3 B21, A5.2 B35, A5.3 B36 · Doc 1 A5.4 B42, A6 B56).

Offline (reader FAKED at the control-plane seam `contained_reader.read`, SYNTHETIC texts, scratch tenant cleaned up): a DPO description is
bound to the reader, never to cue words; cue hits are the draft proposer and advisory receipts only — never a rewrite or refusal cause;
reader-marked meanings (English + Kiswahili, paraphrase, case-insensitive) are located and reconstructed; indirect disclosures are withheld;
seeded privileged meanings leave zero survivors in the outbound; the harmless corpus (the 4–5 Oct false positives) yields zero refusals and an
unchanged payload; an ambiguous read of an ENFORCED category refuses, of an advisory one is receipted; reader unavailability refuses before any
external client is constructed and synthetic custody never consults the reader; task separation refuses on the reader's intent verdict, not on
cues; long texts are read in chunks with global offsets; receipts carry counts and digests, never values.
Live (skips when the reader is not serving): the indirect-disclosure audit excerpt reads without a leak after the carrier scrub; the harmless
system prompt marks nothing privileged."""
import asyncio
import json
import os
import sys
import uuid

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import category3 as c3  # noqa: E402
from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.synisense.shield import register_gate as g  # noqa: E402
from services.synisense.shield import semantic_register as reg  # noqa: E402
from services.synisense.shield import task_separation as ts  # noqa: E402
from services.training_lab import store as lab  # noqa: E402

TENANT = 'tenant-SYNTHETIC-a4-' + uuid.uuid4().hex[:6]
ACTOR = 'dpo-SYNTHETIC-a4'
CONTRACT_EN = ('SYNTHETIC CONTRACT. Our counterparty for this engagement is Nuru Orchard Test Cooperative, trading under the internal label Papaya Comet. '
               'The reserve fee is KES 147300 and the bid is computed as 0.73 times the rival floor. Prepare a one-page summary for the board.')
CONTRACT_SW = ('MKATABA WA HUDUMA (SYNTHETIC). Mteja: Ushirika wa Majaribio wa Nuru Orchard. Ada ya kuhifadhi ni KES 147,300 kwa mwezi. '
               'Jina la mradi wa ndani: Papaya Comet. Tafadhali andaa muhtasari wa kurasa moja.')
AUDIT_INDIRECT = ('Audit note (SYNTHETIC): the counterparty is the only cooperative in Nyeri exporting macadamia to one Dutch buyer, so naming the county and the crop '
                  'identifies it. Their margin is thinner than disclosed to lenders; the board has not been told. Prepare a neutral summary for the external reviewer.')
HARMLESS = {
    'system': ('You are Akki, a governed answerer. You may use ONLY the qualified units supplied in the window. Reply with one JSON object and nothing else. '
               'The project is internal; token accounting applies to every reply; schema keys: answer, cited_units, sufficient, unsupported.'),
    'window': 'OBJECTIVE: Identify the topics of interest in farmer training questions\n\nQUESTION: Which of those were about minerals?\n\nWINDOW:\n{"unit_id": "u1", "text": "Farmer asked which mineral lick suits dairy cows in the dry season"}',
    'forecast': 'Summarise the estate forecast of 500,290 hours and the 986 USD/mo saving; the internal review calls the token budget a project constraint.',
}
EN_SPANS = [{'category': 'client_identity', 'span': 'Nuru Orchard Test Cooperative', 'reason': 'names the counterparty'}, {'category': 'private_project_name', 'span': 'papaya comet', 'reason': 'internal label'},
            {'category': 'commercial_terms', 'span': 'KES 147300', 'reason': 'negotiated fee'}, {'category': 'unpublished_pricing_method', 'span': '0.73 times the rival floor', 'reason': 'how the bid is computed'}]
SW_SPANS = [{'category': 'client_identity', 'span': 'Ushirika wa Majaribio wa Nuru Orchard', 'reason': 'mteja'}, {'category': 'commercial_terms', 'span': 'KES 147,300', 'reason': 'ada'}, {'category': 'private_project_name', 'span': 'Papaya Comet', 'reason': 'jina la mradi'}]
INDIRECT = ['the only cooperative in Nyeri exporting macadamia to one Dutch buyer', 'Their margin is thinner than disclosed to lenders']
SEEDED = ['Nuru Orchard', 'Papaya Comet', '147300', '147,300', '0.73 times', 'Nyeri', 'macadamia', 'Dutch buyer', 'thinner than disclosed']
_LOOP = asyncio.new_event_loop()


def run(coro):
    asyncio.set_event_loop(_LOOP); return _LOOP.run_until_complete(coro)


def reading(privileged=(), indirect=(), requests_privileged=False, coherent=True, bounded='Prepare a short summary of the material for its stated audience'):
    return {'objective': {'intent': 'summarise', 'bounded_objective': bounded, 'coherent': coherent, 'requests_privileged': requests_privileged}, 'meaning': 'A request to prepare a summary over commercially sensitive material.',
            'privileged': [dict(p) for p in privileged], 'indirect_disclosures': list(indirect), 'safe_rewrite': 'Prepare a one-page summary for [PARTY] under [PROJECT].'}


def fake_reader(rules, log=None):
    """`rules`: list of (substring_present_in_text → reading). The first matching rule answers; otherwise an empty reading. Records what it was asked."""
    def _read(text, categories, purpose, **_):
        assert isinstance(categories, list) and all(set(c) >= {'name', 'description'} for c in categories), 'the reader is asked with the declared categories (name + description)'
        assert not any(s in purpose for s in SEEDED), 'purposes carry no values'
        if log is not None: log.append({'chars': len(text), 'purpose': purpose, 'categories': [c['name'] for c in categories]})
        doc = next((json.loads(json.dumps(r)) for needle, r in rules if needle in text), reading())
        return {'reading': doc, 'seconds': 0.05, 'lineage': {'model_id': 'contained-reader-SYNTHETIC', 'weight_sha256': 'f' * 64, 'host': 'synthetic-host'}, 'receipt_id': 'gpurcp-synthetic-' + uuid.uuid4().hex[:6], 'chars': len(text)}
    return _read


def _no_values(obj):
    blob = json.dumps(obj, ensure_ascii=False, default=str).lower()
    return [s for s in SEEDED if s.lower() in blob]


@pytest.fixture(autouse=True, scope='module')
def _tenant():
    reg.ensure_defaults(TENANT)
    yield
    d = lab.db()
    d.shield_register.delete_many({'tenant_id': TENANT}); d.shield_separations.delete_many({'tenant_id': TENANT})


# ----------------------------------------------------------------------------- B21/B35: the declaration is bound to the reader; cues are the proposer
def test_contextual_declarations_bind_to_the_reader_and_cues_never_rewrite_or_refuse():
    declared = c3.declared(TENANT)
    assert {'client_identity', 'private_project_name', 'commercial_terms', 'unpublished_pricing_method'} <= set(declared) and all(c['recogniser'] == c3.RECOGNISER for c in declared.values())
    with pytest.raises(ValueError, match='describes the privileged meaning'):
        reg.author(TENANT, ACTOR, {'name': 'vague', 'kind': 'contextual', 'action': 'abstract', 'description': 'x'})
    spans = reg.classify(CONTRACT_EN, TENANT)  # no reader spans: Category 3 can only come from the reader
    contextual = [s for s in spans if s['kind'] == 'contextual']
    assert contextual and all(s.get('proposer') and s['enforcement'] == 'advisory' and s.get('source') == 'cue' for s in contextual), 'cue hits are advisory proposer receipts'
    assert not reg.classify(CONTRACT_EN, TENANT, cues='off')
    recon = reg.reconstruct(CONTRACT_EN, TENANT)
    assert not recon['bindings'] and not recon['categories_applied'] and recon['advisory_cues'].get('client_identity'), 'cues alone rewrite nothing; they are counted'
    assert recon['joint_disclosure']['residual_quasi_identifier_groups'], 'what did change came from the deterministic joint-disclosure generalisation (B5.6), not from a cue'
    out = reg.propose(TENANT, ACTOR, CONTRACT_EN, reader_findings=[{'category': 'other_privileged', 'value': 'Dutch buyer route', 'reason': 'export dependency', 'located': True}])
    drafts = {d['name']: d for d in out['drafts']}
    assert 'client_identity_values' in drafts and 'Nuru Orchard Test Cooperative' in drafts['client_identity_values']['values'] and drafts['client_identity_values']['status'] == 'draft'
    assert 'Dutch buyer route' in drafts['reader_privileged_values']['values'] and drafts['reader_privileged_values']['status'] == 'draft'
    assert not any(s['category'] == 'reader_privileged_values' for s in reg.classify('Dutch buyer route', TENANT)), 'a draft protects nothing until adopted and approved'
    for n in drafts: reg.discard(TENANT, ACTOR, n)


def test_harmless_corpus_zero_refusals_and_unchanged_payload(monkeypatch):
    log = []
    monkeypatch.setattr(c3.reader, 'read', fake_reader([], log))
    for name, text in HARMLESS.items():
        r = g.gate(HARMLESS['system'], text, TENANT, f'harmless:{name}')
        assert not r.refused and r.prompt == text and r.system_message == HARMLESS['system'] and not r.enforced and not r.token_map and r.inspection['clean'] and r.hostility['verdict'] == 'pass', name
        assert r.reader['applied'] is True and r.reader['spans'] == 0
    assert log and all(e['categories'] for e in log), 'every read carried the declared Category-3 set'


# ----------------------------------------------------------------------------- A5.2/A5.3: reader-marked meaning located, reconstructed, zero survivors
def test_reader_marked_meanings_are_located_and_reconstructed_in_english_and_kiswahili(monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('Our counterparty', reading(EN_SPANS, ['the bid is computed as 0.73 times the rival floor'])), ('MKATABA', reading(SW_SPANS))]))
    out = c3.recognise(CONTRACT_EN, TENANT, 'test.recognise')
    by_cat = {s['category']: s for s in out['spans']}
    assert {'client_identity', 'private_project_name', 'commercial_terms', 'unpublished_pricing_method', 'indirect_disclosure'} == set(by_cat) and out['blocking_ambiguities'] == 0 and out['chunks'] == 1
    assert all(CONTRACT_EN[s['start']:s['end']] == s['text'] for s in out['spans']) and by_cat['private_project_name']['text'] == 'Papaya Comet', 'case-insensitive location returns the text as written'
    assert by_cat['client_identity']['enforcement'] == 'enforced' and by_cat['commercial_terms']['enforcement'] == 'advisory' and by_cat['indirect_disclosure']['action'] == 'remove'
    recon = reg.reconstruct(CONTRACT_EN, TENANT, reader_spans=out['spans'])
    assert not _no_values(recon['safe_text']) and recon['joint_disclosure']['passes'] and {b['category'] for b in recon['bindings'].values()} >= {'client_identity', 'private_project_name', 'commercial_terms'}
    assert '[METHOD_WITHHELD]' in recon['safe_text'] or '[DISCLOSURE_WITHHELD]' in recon['safe_text']
    sw = c3.recognise(CONTRACT_SW, TENANT, 'test.recognise.sw')
    assert len(sw['spans']) == 3 and all(CONTRACT_SW[s['start']:s['end']] == s['text'] for s in sw['spans'])
    safe_sw = reg.reconstruct(CONTRACT_SW, TENANT, reader_spans=sw['spans'])['safe_text']
    assert not _no_values(safe_sw) and 'Tafadhali andaa muhtasari' in safe_sw, 'the task survives, the privileged meaning does not'


def test_indirect_disclosure_withheld_and_seeded_meanings_leave_zero_survivors_in_outbound(monkeypatch):
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('Audit note', reading([], INDIRECT)), ('Our counterparty', reading(EN_SPANS))]))
    r = g.gate('You are a neutral summariser for the external reviewer.', AUDIT_INDIRECT, TENANT, 'audit.summary')
    assert not r.refused and r.prompt.count('[DISCLOSURE_WITHHELD]') == 2 and 'Prepare a neutral summary' in r.prompt
    for s in ('Nyeri', 'macadamia', 'Dutch buyer', 'thinner than disclosed'): assert s not in r.prompt, s
    assert r.reader['indirect_disclosures'] == 2 and r.enforced == {'indirect_disclosure': 2}
    r = g.gate('Plan for the counterparty named in the brief.', CONTRACT_EN, TENANT, 'doc_studio.plan')
    assert not r.refused and r.inspection['clean'] and r.enforced.get('client_identity') == 1 and r.enforced.get('private_project_name') == 1 and 'commercial_terms' in r.advisory
    assert 'Nuru Orchard' not in r.prompt and 'Papaya Comet' not in r.prompt and '[PARTY_1]' in r.prompt and '[PROJECT_1]' in r.prompt
    assert reg.inspect_outbound(r.system_message + '\n' + r.prompt, ['Nuru Orchard Test Cooperative', 'Papaya Comet'])['clean']
    assert g.rebind('Deliver for [PARTY_1] under [PROJECT_1].', r.token_map) == 'Deliver for Nuru Orchard Test Cooperative under Papaya Comet.'


# ----------------------------------------------------------------------------- B42/B56: ambiguity and unavailability refuse safely; synthetic custody never consults the reader
def test_ambiguous_read_refuses_for_enforced_and_is_receipted_for_advisory(monkeypatch):
    paraphrased = reading([{'category': 'client_identity', 'span': 'Nuru Orchard Cooperative Limited', 'reason': 'paraphrased, not in the text'}])
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('Our counterparty', paraphrased)]))
    out = c3.recognise(CONTRACT_EN, TENANT, 'test.ambiguous')
    assert out['blocking_ambiguities'] == 1 and out['ambiguous'][0]['enforcement'] == 'enforced' and 'span_sha256' in out['ambiguous'][0] and not out['spans']
    r = g.gate('', CONTRACT_EN, TENANT, 'doc_studio.plan')
    assert r.refused and r.reason.startswith('register_cat3_ambiguous') and r.prompt == CONTRACT_EN, 'nothing was rewritten and nothing may cross'
    advisory_only = reading([{'category': 'commercial_terms', 'span': 'about one hundred and forty-seven thousand', 'reason': 'figure in words'}])
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('Our counterparty', advisory_only)]))
    r = g.gate('', CONTRACT_EN, TENANT, 'doc_studio.plan')
    assert not r.refused and r.reader['ambiguous'] == 1 and r.reader['blocking_ambiguities'] == 0
    undeclared = reading([{'category': 'other_privileged', 'span': 'rival floor', 'reason': 'undeclared meaning'}])
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('Our counterparty', undeclared)]))
    out = c3.recognise(CONTRACT_EN, TENANT, 'test.undeclared')
    assert out['undeclared'] == [{'category': 'other_privileged', 'value': 'rival floor', 'reason': 'undeclared meaning', 'located': True}] and not out['spans'], 'undeclared findings feed the proposer, never the rewrite'


def test_reader_unavailable_refuses_before_any_external_client_and_synthetic_custody_skips_the_reader(monkeypatch):
    def down(*a, **k): raise cr.ReaderUnavailable('contained-reader-qwen3-8b-base is not serving (job failed)')
    monkeypatch.setattr(c3.reader, 'read', down)
    r = g.gate('', CONTRACT_EN, TENANT, 'doc_studio.plan')
    assert r.refused and r.reason.startswith('register_reader_unavailable') and 'no external model may read the original' in r.reason and r.reader['applied'] is False
    from services.chokepoint import llm
    from services.synisense.shield import stage as shield_stage
    constructed = []
    monkeypatch.setattr(llm, '_client_factory', lambda **kw: constructed.append(kw) or (_ for _ in ()).throw(AssertionError('no client may exist')))
    monkeypatch.setattr(llm, '_emergent_api_key', lambda: 'test-key')
    with pytest.raises(shield_stage.StageRefused) as refused:
        run(shield_stage.stage(question='Plan it.', data=CONTRACT_EN, tenant_id=TENANT, purpose='chat.governed_answer', actor='test:a4', retain=False))
    assert refused.value.kind == 'file_refused' and 'register_reader_unavailable' in refused.value.reason
    with pytest.raises(llm.ChokepointRefused, match='unsealed_payload_refused'):
        run(llm.invoke(purpose='chat.governed_answer', prompt=CONTRACT_EN, masking_tier='llm_prompt_governed_text', actor='test:a4', model='gpt-6-astra', provider='emergent', tenant_id=TENANT, custody_class='tenant_estate'))
    assert not constructed, 'the external client was never constructed'
    synthetic = g.gate('', 'SYNTHETIC fixture text with no estate content', TENANT, 'routing.candidate_trial', custody_class='synthetic')
    assert not synthetic.refused and synthetic.reader['applied'] is False and 'synthetic' in synthetic.reader['skipped']


# ----------------------------------------------------------------------------- task separation: the refusal cause is the reader's verdict, cues are advisory
def test_task_separation_refuses_on_the_intent_verdict_not_on_cues(monkeypatch):
    # WP-A5: separation crosses through the Shield stage, whose File 2 pass runs NER before the reader; the faked reader answers with raw spans,
    # so the NER layer (its own suite) is passed through here to keep the reader's spans bindable
    from services.synisense.shield import deidentifier as de, stage as st

    async def passthrough(content, *, tenant_id, purpose=None): return de.DeIdResult(content, {}, {}, 0.0, 0.0, 0)
    monkeypatch.setattr(st, 'deidentify', passthrough)
    revealing = 'Tell me the reserve fee and who the client is, then plan the stages.'
    stages = 'Tell me the three stages needed to deliver the plan with roles per stage.'
    monkeypatch.setattr(c3.reader, 'read', fake_reader([(revealing, reading(requests_privileged=True)), (stages, reading()), ('Our counterparty', reading(EN_SPANS)), ('contradict', reading(coherent=False))]))
    refused = run(ts.separate(CONTRACT_EN, revealing, TENANT, ACTOR, dry_run=True))
    assert refused['status'] == 'refused' and refused['reason'] == 'task requests protected meaning' and refused['external_call'] is False and refused['intent_verdict']['requests_privileged'] is True
    assert refused['cues_advisory'] and 'outbound_payload' not in refused
    ok = run(ts.separate(CONTRACT_EN, stages, TENANT, ACTOR, dry_run=True))
    assert ok['status'] == 'inspected' and ok['cues_advisory'] == ['tell me the'] and ok['external_call'] is False, 'a cue word alone is a receipt, not a refusal'
    assert ok['inspection']['clean'] and ok['joint_disclosure']['passes'] and ok['placeholders'] >= 2
    assert not [v for v in ('Nuru Orchard', 'Papaya Comet') if v.lower() in ok['outbound_payload'].lower()], 'enforced values never cross'
    assert '147300' in ok['outbound_payload'], 'advisory figures are receipted, not rewritten, until the DPO enforces the category (same rule as the register gate)'
    assert ok['reader']['recogniser'] == c3.RECOGNISER and ok['reader']['spans'] == 4
    incoherent = run(ts.separate(CONTRACT_EN, 'Plan it and also do not plan it; contradict both.', TENANT, ACTOR, dry_run=True))
    assert incoherent['status'] == 'refused' and 'incoherent' in incoherent['reason']
    stored = list(lab.db().shield_separations.find({'tenant_id': TENANT}, {'_id': 0}))
    assert len(stored) == 3 and not _no_values(stored), 'separation receipts carry digests and counts, never values'


# ----------------------------------------------------------------------------- bounded reads: chunking with global offsets; receipts never carry values
def test_long_text_is_read_in_chunks_with_global_offsets_and_receipts_carry_no_values(monkeypatch):
    log = []
    filler = 'The quarterly review covers logistics, staffing and the training calendar for the field teams. ' * 120
    text = filler + 'The internal label for the engagement is Papaya Comet. ' + filler[: c3.CHUNK_CHARS // 3]
    monkeypatch.setattr(c3.reader, 'read', fake_reader([('internal label', reading([{'category': 'private_project_name', 'span': 'Papaya Comet', 'reason': 'internal label'}]))], log))
    out = c3.recognise(text, TENANT, 'test.chunks')
    assert out['chunks'] >= 2 and len(log) == out['chunks'] and all(e['chars'] <= c3.CHUNK_CHARS for e in log) and len(out['receipts']) == out['chunks']
    assert len(out['spans']) == 1 and text[out['spans'][0]['start']:out['spans'][0]['end']] == 'Papaya Comet' and out['spans'][0]['start'] > c3.CHUNK_CHARS
    assert not _no_values(c3.summary(out)) and not _no_values(out['ambiguous']) and not _no_values(out['indirect_disclosures'])
    r = g.gate('', CONTRACT_EN, TENANT, 'doc_studio.plan', recognise=lambda texts, tenant, purpose: ([[], [{'start': CONTRACT_EN.find('Papaya Comet'), 'end': CONTRACT_EN.find('Papaya Comet') + 12, 'text': 'Papaya Comet', 'category': 'private_project_name', 'kind': 'contextual', 'action': 'abstract', 'enforcement': 'enforced', 'cue': 'test', 'source': c3.RECOGNISER}]], {'receipts': ['gpurcp-x'], 'seconds': 0.1, 'chunks': 1, 'categories_asked': 4, 'indirect_disclosures': [], 'undeclared': [], 'ambiguous': [], 'blocking_ambiguities': 0}))
    assert not _no_values(r.summary()) and r.token_map == {'[PROJECT_1]': 'Papaya Comet'}, 'the binding map stays in the process; the summary carries counts only'


# ----------------------------------------------------------------------------- live: the real reader on the shapes that drove the WP-A4 design
def _live():
    st = cr.status()
    if st.get('status') != 'running': pytest.skip(f"contained reader not serving: {st.get('status')}")


def test_live_indirect_audit_excerpt_reads_without_leak_and_harmless_system_prompt_marks_nothing():
    _live()
    out = c3.recognise(AUDIT_INDIRECT, 'RMS', 'wp_a4_live_audit')
    objective = out['objective'] or {}
    assert objective.get('coherent') is True and out['receipts'] and os.environ.get('M9_REMOTE_ROOT')
    marked = [s['text'].lower() for s in out['spans']]
    carriers = (str(objective.get('bounded_objective')) + ' ' + str(objective.get('meaning', ''))).lower()
    assert not any(m in carriers for m in marked if len(m) >= 3), 'a marked span never survives in the objective carriers (scrubbed on the host, re-checked here)'
    assert out['indirect_disclosures'] or out['spans'], 'the reader finds the indirect disclosure or the privileged meaning in this excerpt'
    harmless = cr.read(HARMLESS['system'], [{'name': n, 'description': c.get('description') or ''} for n, c in c3.declared('RMS').items()], 'wp_a4_live_harmless')
    assert harmless['reading']['privileged'] == [] and harmless['reading']['objective']['coherent'] is True and harmless['seconds'] < 120
