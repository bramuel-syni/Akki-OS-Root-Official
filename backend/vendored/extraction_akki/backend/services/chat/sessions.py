"""Chat sessions: frozen objective, durable turns, and M5 compaction → hash-verified reload.

A session is one closed run (Doc 05: one run has one Ledger). The objective is frozen at the first question;
every turn banks its decision, window, memory and receipt references. Compaction (MEM-1..11) turns the closed
working context into a new artefact — facts and receipts by pointer, other text verbatim — with its ledger row on
the ONE chain before the bytes are readable; reload verifies the hash or refuses.
"""
import asyncio
import hashlib
import json
import uuid
from datetime import datetime, timezone

from core import db
from services.memory.compaction_v1.carriers import Claim, CompactionArtefactRef, RetentionRuleSetVersion, RunScopedContext
from services.memory.compaction_v1.chain_integration import append_compaction_row_to_chain
from services.memory.compaction_v1.mongo_storage import MongoCompactionStorage
from services.memory.compaction_v1.operations import compact as _compact, reload as _reload
from services.memory.compaction_v1.refusals import MemoryLedgerRowMissingRefusalError, MemoryReloadRefusalError
from services.memory.compaction_v1.retention import DraftingComponent, RetentionEngine
from services.memory.compaction_v1.verifier import ReloadVerifier

COLLECTION = 'chat_sessions'
RULE_SET = RetentionRuleSetVersion(version='v1')


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _public(doc):
    doc = dict(doc)
    doc.pop('_id', None)
    return doc


async def create(scope, question, title=None):
    session = {'session_id': 'cs-' + uuid.uuid4().hex[:12], 'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id'],
               'objective': {'text': question, 'sha256': sha(question), 'frozen_at': now()},
               'title': (title or question)[:80], 'created_at': now(), 'updated_at': now(), 'archived': False,
               'turns': [], 'compaction': None}
    await db[COLLECTION].insert_one(dict(session))
    return session


async def get(scope, session_id):
    doc = await db[COLLECTION].find_one({'session_id': session_id, 'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id']})
    return _public(doc) if doc else None


async def listing(scope, archived=False):
    cursor = db[COLLECTION].find({'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id'], 'archived': archived},
                                 {'_id': 0, 'turns': 0}).sort('updated_at', -1)
    out = []
    async for doc in cursor:
        out.append(doc)
    return out


async def append_turn(scope, session_id, turn):
    await db[COLLECTION].update_one({'session_id': session_id, 'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id']},
                                    {'$push': {'turns': turn}, '$set': {'updated_at': now()}})


async def update(scope, session_id, fields):
    result = await db[COLLECTION].update_one({'session_id': session_id, 'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id']},
                                             {'$set': {**fields, 'updated_at': now()}})
    return result.matched_count == 1


async def tenant_sessions(tenant_id):
    """Every session of the estate (all principals) — used only by estate-level acts such as a rights withdrawal."""
    return [_public(doc) async for doc in db[COLLECTION].find({'tenant_id': tenant_id})]


async def mark_turn_stale(tenant_id, session_id, turn_id, stale):
    await db[COLLECTION].update_one({'session_id': session_id, 'tenant_id': tenant_id, 'turns.turn_id': turn_id},
                                    {'$set': {'turns.$.stale_rights': stale, 'updated_at': now()}})


def recent_context(session, limit=3):
    """The conversation ring that enters the prompt: compacted pointers, then the last turns verbatim (bounded)."""
    lines = []
    compaction = session.get('compaction')
    if compaction:
        lines.append(f"Earlier turns are compacted into artefact {compaction['artefact_hash'][:16]}… "
                     f"({compaction['claims']} claims, facts and receipts by pointer).")
    live = [t for t in session.get('turns', []) if not t.get('compacted')]
    withheld = sum(1 for t in live if t.get('stale_rights'))
    if withheld:
        lines.append(f"{withheld} earlier answer(s) withheld: the source right behind them was withdrawn.")
    for turn in [t for t in live if not t.get('stale_rights')][-limit:]:
        lines.append(f"Q: {turn['question'][:300]}")
        lines.append(f"A ({turn['decision']}): {(turn.get('answer') or turn.get('refusal_reason') or '')[:400]}")
    return lines


def _claims(session):
    claims = [Claim(class_='objective', text=session['objective']['text'], text_hash=session['objective']['sha256'],
                    provenance_ref=f"objective:{session['session_id']}")]
    previous = session.get('compaction')
    if previous:  # lineage by pointer: the new artefact names the one it succeeds
        claims.append(Claim(class_='fact', text=previous['artefact_hash'], text_hash=sha(previous['artefact_hash']),
                            provenance_ref=f"compaction:{previous['artefact_hash']}"))
    for turn in session['turns']:
        if turn.get('compacted'):
            continue
        claims.append(Claim(class_='utterance', text=turn['question'], text_hash=sha(turn['question']), provenance_ref=f"turn:{turn['turn_id']}:question"))
        if turn.get('stale_rights'):  # the answer and its facts are not carried forward; the withdrawal is
            note = f"withheld: {turn['stale_rights']['reason_code']} {turn['stale_rights']['revocation_ref']}"
            claims.append(Claim(class_='refusal', text=note, text_hash=sha(note), provenance_ref=f"turn:{turn['turn_id']}:withdrawn"))
            continue
        if turn.get('refused'):
            reason = turn.get('refusal_reason') or turn['decision']
            claims.append(Claim(class_='refusal', text=reason, text_hash=sha(reason), provenance_ref=f"turn:{turn['turn_id']}:refusal"))
        elif turn.get('answer'):
            claims.append(Claim(class_='inference', text=turn['answer'], text_hash=sha(turn['answer']), provenance_ref=f"turn:{turn['turn_id']}:answer"))
        for ref in (turn.get('evidence') or {}).get('cited_refs', []):
            claims.append(Claim(class_='fact', text=ref, text_hash=sha(ref), provenance_ref=ref))
        if turn.get('receipt_id'):
            claims.append(Claim(class_='receipt_ref', text=turn['receipt_id'], text_hash=sha(turn['receipt_id']), provenance_ref=f"receipt:{turn['receipt_id']}"))
    return tuple(claims)


async def compact(scope, session, actor):
    """Compact the session's working context (not its evidence/receipts) into a durable, ledgered artefact."""
    key = f"t_{scope['tenant_id']}/run_{session['session_id']}/obj_{session['objective']['sha256'][:16]}"
    if not any(not t.get('compacted') for t in session['turns']):
        return None
    ctx = RunScopedContext(key=key, claims=_claims(session))
    storage = MongoCompactionStorage(scope['tenant_id'])
    try:
        artefact_ref, row = await asyncio.to_thread(_compact, ctx=ctx, engine=RetentionEngine(rule_set_version=RULE_SET),
                                                    drafting=DraftingComponent(), storage=storage)
    finally:
        storage.close()
    receipt = await append_compaction_row_to_chain(row=row, tenant_id=scope['tenant_id'], actor=actor, trace_id=session['session_id'])
    compaction = {'artefact_hash': artefact_ref.artefact_hash, 'key': key, 'claims': len(ctx.claims), 'loss_statement': row.loss_statement,
                  'total_drops': row.total_drops, 'retention_rule_set_version': row.retention_rule_set_version,
                  'chain_row_id': receipt.chain_row_id, 'chain_appended_at_utc': receipt.chain_appended_at_utc,
                  'compacted_turns': sum(1 for t in session['turns'] if not t.get('compacted')), 'at': now(),
                  'source_version_hashes': list(artefact_ref.source_version_hashes)}
    update = {'$set': {'compaction': compaction, 'turns.$[].compacted': True, 'updated_at': now()}}
    if session.get('compaction'):
        update['$push'] = {'compaction_history': session['compaction']}
    await db[COLLECTION].update_one({'session_id': session['session_id'], 'tenant_id': scope['tenant_id']}, update)
    return compaction


async def reload(scope, session):
    """Scope-checked, hash-verified reload of the compacted context; refuses on missing row or tamper."""
    compaction = session.get('compaction')
    if not compaction:
        return {'status': 'none', 'reason': 'This session has not been compacted; its turns are read directly.'}
    storage = MongoCompactionStorage(scope['tenant_id'])
    try:
        ref = await asyncio.to_thread(storage.read_artefact_ref, artefact_hash=compaction['artefact_hash'])
        if ref is None or ref.key != compaction['key'] or not ref.key.startswith(f"t_{scope['tenant_id']}/"):
            return {'status': 'refused', 'reason': 'AKKI-MEM-COMPACT-003: artefact reference is not in this tenant scope.'}
        try:
            payload = await asyncio.to_thread(_reload, artefact_ref=ref, verifier=ReloadVerifier(), storage=storage)
        except (MemoryLedgerRowMissingRefusalError, MemoryReloadRefusalError) as exc:
            return {'status': 'refused', 'reason': str(exc)}
    finally:
        storage.close()
    body = json.loads(payload.decode('utf-8'))
    return {'status': 'verified', 'artefact_hash': compaction['artefact_hash'], 'verified_sha256': hashlib.sha256(payload).hexdigest(),
            'bytes': len(payload), 'entries': body['entries'], 'key': body['key'], 'chain_row_id': compaction['chain_row_id'],
            'loss_statement': compaction['loss_statement'], 'reloaded_at': now()}
