"""M4/M5 offline proofs on SYNTHETIC units: window determinism, heavy shrink with disclosed loss, oversized
load-bearing unit excluded whole, compaction → durable Mongo artefact → hash-verified reload, tamper refusal and
cross-tenant refusal. No model call, no estate bytes, no SSH. The chain append is stubbed so no synthetic row
enters the one Northena ledger; the ordering guarantee (ledger row before bytes) is exercised inside storage.
"""
import asyncio
import hashlib
import json
import os
import sys
import uuid
from types import SimpleNamespace

import pytest

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.chat import sessions, window as windowing  # noqa: E402
from services.memory.compaction_v1.carriers import Claim, RetentionRuleSetVersion, RunScopedContext  # noqa: E402
from services.memory.compaction_v1.mongo_storage import MongoCompactionStorage  # noqa: E402
from services.memory.compaction_v1.operations import compact, reload  # noqa: E402
from services.memory.compaction_v1.refusals import MemoryLedgerRowMissingRefusalError, MemoryReloadRefusalError  # noqa: E402
from services.memory.compaction_v1.retention import DraftingComponent, RetentionEngine  # noqa: E402
from services.memory.compaction_v1.verifier import ReloadVerifier  # noqa: E402

TENANT = 'tenant-SYNTHETIC-m4m5'
OTHER = 'tenant-SYNTHETIC-other'
REQUEST = 'req-synthetic-m4m5'


_LOOP = asyncio.new_event_loop()


def run(coro):
    asyncio.set_event_loop(_LOOP)
    return _LOOP.run_until_complete(coro)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def candidate(i, *, overlap, kind='matched', words=12, class_label='utterance'):
    body = ' '.join(f'w{i}_{k}' for k in range(words))
    unit = {'unit_id': f'unit-{i:04d}', 'record': {'id': i, 'note': body},
            'provenance': {'locator': {'database': 'db', 'table': 'tbl', 'primary_key': 'id', 'key_value': str(i)}},
            'defensibility': {'defensibility_class': class_label}}
    line = json.dumps(unit, sort_keys=True)
    return {'ref': f'akki://unit/{TENANT}/{REQUEST}/unit-{i:04d}', 'unit_id': unit['unit_id'], 'unit': unit, 'position': i,
            'overlap': overlap, 'kind': kind, 'rel_keys': [], 'content_sha256': sha(line), 'region': 'db.tbl',
            'artifact_ref': 'akki://artifact/synthetic', 'request_id': REQUEST, 'class_label': class_label,
            'reextraction_ref': f'akki://reextract/{TENANT}/{REQUEST}/unit-{i:04d}'}


def population(n=200, oversized_at=None):
    rows = []
    for i in range(n):
        words = 4000 if i == oversized_at else 12 + (i % 7) * 3
        rows.append(candidate(i, overlap=3 if i % 5 == 0 else (1 if i % 2 else 0), kind='matched' if i % 2 or i % 5 == 0 else 'neighbour', words=words))
    return rows


def build(cands, reserved=1200):
    return windowing.build(objective_text='synthetic objective', frame_ref='akki://chat/session/cs-synthetic', model='gpt-5-mini',
                           qualified_set_receipt_ref=sha('qualified'), candidates=cands, reserved_tokens=reserved)


class TestWindow:
    def test_same_population_same_window(self):
        first, sel1, exc1 = build(population())
        second, sel2, exc2 = build(population())
        assert first.selected_refs == second.selected_refs
        assert first.excluded_counts == second.excluded_counts
        assert first.top_excluded_handles == second.top_excluded_handles
        assert [c['ref'] for c in sel1] == [c['ref'] for c in sel2]

    def test_load_bearing_first_and_whole_units_only(self):
        window, selected, excluded = build(population())
        lead = list(window.selected_refs[:len(window.load_bearing_refs)])
        assert set(lead) <= set(window.load_bearing_refs)
        budget = window.window_tokens - window.reserved_tokens
        assert sum(c['tokens'] for c in selected) <= budget
        assert all(c['tokens'] == windowing.count_tokens(c['text']) for c in selected)

    def test_heavy_shrink_discloses_loss(self):
        cands = population(400)
        window, selected, excluded = build(cands)
        total = sum(c['tokens'] for c in cands)
        kept = sum(c['tokens'] for c in selected)
        assert kept / total < 0.30, (kept, total)
        assert window.loss_disclosed and sum(window.excluded_counts.values()) == len(excluded) > 0
        statement = windowing.loss_statement(window, {'matched_total': 1000, 'failures': []})
        assert 'excluded by budget' in statement and 'further matching units not retrieved' in statement

    def test_oversized_load_bearing_unit_is_excluded_whole(self):
        cands = population(60, oversized_at=0)
        big = cands[0]
        big['overlap'] = 99
        window, selected, excluded = build(cands)
        assert big['ref'] in window.load_bearing_refs
        assert big['ref'] not in window.selected_refs
        assert big['reextraction_ref'] in window.top_excluded_handles
        assert big['tokens'] > window.window_tokens - window.reserved_tokens

    def test_nothing_fits_refuses_instead_of_splitting(self):
        cands = [candidate(0, overlap=5, words=4000)]
        with pytest.raises(ValueError):
            build(cands)


@pytest.fixture
def storage():
    store = MongoCompactionStorage(TENANT)
    yield store
    for name in ('memory_compaction_ledger_rows', 'memory_compaction_artefacts', 'memory_compaction_refs'):
        store._db[name].delete_many({'tenant_id': {'$in': [TENANT, OTHER]}})
    store.close()


def context(key_suffix):
    claims = (Claim(class_='objective', text='what is in the units', text_hash=sha('what is in the units'), provenance_ref='objective:cs-x'),
              Claim(class_='fact', text='akki://unit/x/1', text_hash=sha('akki://unit/x/1'), provenance_ref='akki://unit/x/1'),
              Claim(class_='inference', text='answer text kept verbatim', text_hash=sha('answer text kept verbatim'), provenance_ref='turn:t1:answer'),
              Claim(class_='receipt_ref', text='rcp-abc', text_hash=sha('rcp-abc'), provenance_ref='receipt:rcp-abc'))
    return RunScopedContext(key=f't_{TENANT}/run_cs-{key_suffix}/obj_{sha("o")[:16]}', claims=claims)


class TestDurableCompaction:
    def test_compact_then_reload_verifies_from_a_fresh_client(self, storage):
        ref, row = compact(ctx=context(uuid.uuid4().hex[:8]), engine=RetentionEngine(rule_set_version=RetentionRuleSetVersion(version='v1')),
                           drafting=DraftingComponent(), storage=storage)
        fresh = MongoCompactionStorage(TENANT)
        try:
            payload = reload(artefact_ref=fresh.read_artefact_ref(artefact_hash=ref.artefact_hash), verifier=ReloadVerifier(), storage=fresh)
        finally:
            fresh.close()
        assert hashlib.sha256(payload).hexdigest() == ref.artefact_hash
        body = json.loads(payload)
        facts = [e for e in body['entries'] if e['class'] in ('fact', 'receipt_ref')]
        assert facts and all('text' not in e for e in facts)
        assert row.total_drops == 0

    def test_tampered_bytes_refuse(self, storage):
        ref, _ = compact(ctx=context(uuid.uuid4().hex[:8]), engine=RetentionEngine(rule_set_version=RetentionRuleSetVersion(version='v1')),
                         drafting=DraftingComponent(), storage=storage)
        storage.tamper_artefact_bytes(artefact_hash=ref.artefact_hash, new_bytes=b'{"entries":[],"key":"forged"}')
        with pytest.raises(MemoryReloadRefusalError):
            reload(artefact_ref=ref, verifier=ReloadVerifier(), storage=storage)

    def test_bytes_without_ledger_row_refuse(self, storage):
        with pytest.raises(MemoryLedgerRowMissingRefusalError):
            storage.write_artefact_bytes(artefact_hash=sha('orphan'), artefact_bytes=b'{}')

    def test_other_tenant_cannot_see_the_artefact(self, storage):
        ref, _ = compact(ctx=context(uuid.uuid4().hex[:8]), engine=RetentionEngine(rule_set_version=RetentionRuleSetVersion(version='v1')),
                         drafting=DraftingComponent(), storage=storage)
        other = MongoCompactionStorage(OTHER)
        try:
            assert other.read_artefact_ref(artefact_hash=ref.artefact_hash) is None
            with pytest.raises(MemoryLedgerRowMissingRefusalError):
                other.read_artefact_bytes(artefact_hash=ref.artefact_hash, verifier=ReloadVerifier())
        finally:
            other.close()


@pytest.fixture
def scope():
    return {'tenant_id': TENANT, 'principal_id': 'principal-synthetic', 'roles': ['operator']}


@pytest.fixture
def stub_chain(monkeypatch):
    calls = []

    async def fake(*, row, tenant_id, actor, trace_id):
        calls.append((row.artefact_hash, tenant_id, actor, trace_id))
        return SimpleNamespace(chain_row_id=f'memory-compaction-v1-{row.artefact_hash}', chain_appended_at_utc='stub', artefact_hash=row.artefact_hash)
    monkeypatch.setattr(sessions, 'append_compaction_row_to_chain', fake)
    return calls


@pytest.fixture
def cleanup_sessions():
    created = []
    yield created
    from core import db
    run(db[sessions.COLLECTION].delete_many({'session_id': {'$in': created}}))
    store = MongoCompactionStorage(TENANT)
    for name in ('memory_compaction_ledger_rows', 'memory_compaction_artefacts', 'memory_compaction_refs'):
        store._db[name].delete_many({'tenant_id': TENANT})
    store.close()


def turn(i, answer=True):
    t = {'turn_id': f'turn-{i:02d}', 'question': f'question {i}', 'asked_at': sessions.now(), 'decision': 'warm' if answer else 'refused',
         'evidence': {'cited_refs': [f'akki://unit/{TENANT}/{REQUEST}/unit-{i:04d}']}, 'refused': not answer}
    if answer:
        t.update({'answer': f'answer {i}', 'receipt_id': f'rcp-{i:012x}'})
    else:
        t['refusal_reason'] = 'out of scope'
    return t


class TestSessionContinuity:
    def test_session_compacts_reloads_and_refuses_other_scope(self, scope, stub_chain, cleanup_sessions):
        session = run(sessions.create(scope, 'what do the units say'))
        cleanup_sessions.append(session['session_id'])
        for i in range(4):
            run(sessions.append_turn(scope, session['session_id'], turn(i, answer=i != 2)))
        session = run(sessions.get(scope, session['session_id']))
        compaction = run(sessions.compact(scope, session, actor=scope['principal_id']))
        assert compaction['claims'] == 1 + 4 + 3 + 1 + 4 + 3  # objective, questions, answers, refusal, cited facts, receipts
        assert stub_chain and stub_chain[0][1] == TENANT
        session = run(sessions.get(scope, session['session_id']))
        assert all(t['compacted'] for t in session['turns'])
        assert sessions.recent_context(session)[0].startswith('Earlier turns are compacted into artefact')
        verified = run(sessions.reload(scope, session))
        assert verified['status'] == 'verified' and verified['verified_sha256'] == compaction['artefact_hash']
        assert any(e['class'] == 'refusal' for e in verified['entries'])
        other = dict(scope, tenant_id=OTHER)
        assert run(sessions.get(other, session['session_id'])) is None
        assert run(sessions.reload(other, session))['status'] == 'refused'
        assert run(sessions.compact(scope, session, actor=scope['principal_id'])) is None
        run(sessions.append_turn(scope, session['session_id'], turn(9)))
        session = run(sessions.get(scope, session['session_id']))
        second = run(sessions.compact(scope, session, actor=scope['principal_id']))
        assert second['artefact_hash'] != compaction['artefact_hash']
        session = run(sessions.get(scope, session['session_id']))
        assert [h['artefact_hash'] for h in session['compaction_history']] == [compaction['artefact_hash']]
        entries = run(sessions.reload(scope, session))['entries']
        assert any(e['provenance_ref'] == f"compaction:{compaction['artefact_hash']}" for e in entries)

    def test_reload_refuses_after_tamper(self, scope, stub_chain, cleanup_sessions):
        session = run(sessions.create(scope, 'tamper drill'))
        cleanup_sessions.append(session['session_id'])
        run(sessions.append_turn(scope, session['session_id'], turn(1)))
        session = run(sessions.get(scope, session['session_id']))
        compaction = run(sessions.compact(scope, session, actor=scope['principal_id']))
        store = MongoCompactionStorage(TENANT)
        store.tamper_artefact_bytes(artefact_hash=compaction['artefact_hash'], new_bytes=b'{"entries":[],"key":"forged"}')
        store.close()
        session = run(sessions.get(scope, session['session_id']))
        assert run(sessions.reload(scope, session))['status'] == 'refused'


if __name__ == '__main__':
    os.environ.setdefault('PYTHONPATH', '/app/backend/vendored/extraction_akki/backend')
    sys.exit(pytest.main([__file__, '-n', '0', '-q']))
