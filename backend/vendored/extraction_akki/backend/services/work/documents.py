"""Documents: immutable versions of a saved answer (or a stated text) that keep their objective, citations, receipt,
sources (artefact + version + rights) and loss statement. A later save is a new version; nothing is rewritten."""
import hashlib

from fastapi import HTTPException

from services.chat import sessions
from services.work import records


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def current(rows):
    doc = None
    for e in rows:
        p = e['payload']
        if p['kind'] == 'version':
            if doc is None:
                doc = {'doc_id': e['row']['run_id'], 'created_by': p['principal_id'], 'created_at': p['at'], 'origin': p.get('origin'), 'versions': [], 'stale': None, 'history': []}
            doc['versions'].append({'version': len(doc['versions']) + 1, 'title': p['title'], 'body': p['body'], 'content_sha256': p['content_sha256'],
                                    'citations': p.get('citations') or [], 'sources': p.get('sources') or [], 'loss_statement': p.get('loss_statement'),
                                    'objective': p.get('objective'), 'receipt_id': p.get('receipt_id'), 'ledger_row_id': p.get('ledger_row_id'),
                                    'by': p['principal_id'], 'at': p['at'], 'receipt_hash': e['row']['hash']})
        elif doc is not None and p['kind'] == 'stale':
            doc['stale'] = {'reason_code': p['reason_code'], 'artifact_refs': p['artifact_refs'], 'revocation_ref': p.get('revocation_ref'), 'at': p['at']}
        if doc is not None:
            doc['history'].append(records.history_entry(e))
    if doc:
        latest = doc['versions'][-1]
        doc.update({'title': latest['title'], 'version': latest['version'], 'content_sha256': latest['content_sha256'], 'updated_at': latest['at']})
    return doc


async def load(db, scope, doc_id):
    doc = current(await records.events(db, scope, 'document', doc_id))
    if doc is None:
        raise HTTPException(404, 'No such document in your estate.')
    return doc


async def listing(db, scope):
    rows = [current(evs) for evs in records.grouped(await records.events(db, scope, 'document')).values()]
    return sorted((d for d in rows if d), key=lambda d: d['updated_at'], reverse=True)


def summary(doc):
    return {k: doc[k] for k in ('doc_id', 'title', 'version', 'content_sha256', 'created_by', 'created_at', 'updated_at', 'stale', 'origin')} | {
        'citations': len(doc['versions'][-1]['citations']), 'sources': doc['versions'][-1]['sources'], 'loss_statement': doc['versions'][-1]['loss_statement']}


async def save(db, scope, *, title=None, body=None, session_id=None, turn_id=None, doc_id=None):
    if session_id:
        session = await sessions.get(scope, session_id)
        turn = next((t for t in (session or {}).get('turns', []) if t['turn_id'] == turn_id), None)
        if turn is None:
            raise HTTPException(404, 'No such turn in your conversations.')
        if turn.get('refused'):
            raise HTTPException(409, 'A refusal is a record, not a document; nothing was answered to save.')
        handoff = records.evidence_from_turn(session, turn)
        doc_id = doc_id or 'doc-' + records.digest([scope['tenant_id'], session_id, turn_id])[:24]
        body = body or handoff['text']
        payload = {'title': (title or turn['question'])[:200], 'body': body, 'citations': handoff['cited_refs'], 'sources': handoff['sources'],
                   'loss_statement': handoff['loss_statement'], 'objective': session['objective'], 'receipt_id': handoff['receipt_id'],
                   'ledger_row_id': handoff['ledger_row_id'], 'origin': {k: handoff[k] for k in ('session_id', 'turn_id', 'decision', 'grounding')}}
    else:
        if not body:
            raise HTTPException(422, 'A document needs a body or a turn to save from.')
        doc_id = doc_id or 'doc-' + records.digest([scope['tenant_id'], scope['principal_id'], title or body, records.now()])[:24]
        payload = {'title': (title or body[:80])[:200], 'body': body, 'citations': [], 'sources': [], 'loss_statement': None, 'objective': None,
                   'receipt_id': None, 'ledger_row_id': None, 'origin': None}
    existing = current(await records.events(db, scope, 'document', doc_id))
    if existing and existing['created_by'] != scope['principal_id'] and not records.is_operator(scope):
        raise HTTPException(403, 'Only the author or an admitted operator can add a version.')
    await records.append(db, scope, 'document', doc_id, 'version', {**payload, 'content_sha256': _sha(payload['body'])}, idempotent=True)
    return await load(db, scope, doc_id)


async def mark_stale(db, scope, doc, *, reason_code, artifact_refs, revocation_ref):
    await records.append(db, scope, 'document', doc['doc_id'], 'stale', {'reason_code': reason_code, 'artifact_refs': artifact_refs, 'revocation_ref': revocation_ref})
