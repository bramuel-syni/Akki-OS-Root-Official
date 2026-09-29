"""The board: one versioned pack per estate. Documents enter by exact version + content hash; questions and their
answers are recorded; a decision names exactly the versions it considered and is taken only by an authorised
principal; its follow-up actions become tasks. A later edit is a new decision that supersedes — the information
originally considered is never rewritten. 'Ask Akki about the board' is a chat session on the same spine."""
from fastapi import HTTPException

from services.chat import journey, sessions
from services.work import documents, records, tasks

RUN = 'board'


def current(rows):
    board = {'documents': [], 'questions': [], 'decisions': [], 'chat_sessions': {}, 'history': []}
    for e in rows:
        p = e['payload']
        kind = p['kind']
        if kind == 'document_added':
            board['documents'].append({'item_id': p['item_id'], 'doc_id': p['doc_id'], 'version': p['version'], 'content_sha256': p['content_sha256'],
                                       'title': p['title'], 'kind': p.get('doc_kind') or 'document', 'note': p.get('note'), 'by': p['principal_id'], 'at': p['at']})
        elif kind == 'question':
            board['questions'].append({'question_id': p['question_id'], 'item_id': p.get('item_id'), 'text': p['text'], 'by': p['principal_id'], 'at': p['at'], 'answers': []})
        elif kind == 'answer':
            for q in board['questions']:
                if q['question_id'] == p['question_id']:
                    q['answers'].append({'text': p['text'], 'by': p['principal_id'], 'at': p['at']})
        elif kind == 'decision':
            board['decisions'].append({'decision_id': p['decision_id'], 'text': p['text'], 'considered': p['considered'], 'actions': p['actions'],
                                       'task_ids': p.get('task_ids') or [], 'supersedes': p.get('supersedes'), 'by': p['principal_id'], 'at': p['at'],
                                       'receipt_hash': e['row']['hash'], 'superseded_by': None})
            if p.get('supersedes'):
                for d in board['decisions']:
                    if d['decision_id'] == p['supersedes']:
                        d['superseded_by'] = p['decision_id']
        elif kind == 'chat_session':
            board['chat_sessions'][p['principal_id']] = p['session_id']
        board['history'].append(records.history_entry(e))
    return board


async def load(db, scope):
    board = current(await records.events(db, scope, 'board', RUN))
    board['chat_session_id'] = board.pop('chat_sessions').get(scope['principal_id'])
    return board


async def add_document(db, scope, doc_id, *, doc_kind=None, note=None):
    if not records.is_operator(scope):
        raise HTTPException(403, 'Only an admitted operator can put a document before the board.')
    doc = await documents.load(db, scope, doc_id)
    item_id = 'bd-' + records.digest([doc_id, doc['version'], doc['content_sha256']])[:12]
    await records.append(db, scope, 'board', RUN, 'document_added', {'item_id': item_id, 'doc_id': doc_id, 'version': doc['version'], 'content_sha256': doc['content_sha256'],
                                                                     'title': doc['title'], 'doc_kind': doc_kind, 'note': note}, idempotent=True)
    return await load(db, scope)


async def ask_question(db, scope, text, item_id=None):
    board = await load(db, scope)
    if item_id and not any(d['item_id'] == item_id for d in board['documents']):
        raise HTTPException(404, 'That document is not before the board.')
    await records.append(db, scope, 'board', RUN, 'question', {'question_id': 'bq-' + records.digest([text, scope['principal_id'], records.now()])[:12], 'text': text[:2000], 'item_id': item_id})
    return await load(db, scope)


async def answer_question(db, scope, question_id, text):
    board = await load(db, scope)
    if not any(q['question_id'] == question_id for q in board['questions']):
        raise HTTPException(404, 'No such question before the board.')
    await records.append(db, scope, 'board', RUN, 'answer', {'question_id': question_id, 'text': text[:4000]})
    return await load(db, scope)


async def decide(db, scope, *, text, item_ids, actions, supersedes=None, owner=None):
    """An authorised decision: names the exact document versions considered; actions become tasks owned as assigned."""
    if not records.is_operator(scope):
        raise HTTPException(403, 'Only an authorised operator or master administrator can record a board decision.')
    board = await load(db, scope)
    items = {d['item_id']: d for d in board['documents']}
    missing = [i for i in item_ids if i not in items]
    if missing:
        raise HTTPException(404, f'Not before the board: {", ".join(missing)}.')
    if supersedes and not any(d['decision_id'] == supersedes for d in board['decisions']):
        raise HTTPException(404, 'The decision to supersede is not on record.')
    considered = [{k: items[i][k] for k in ('item_id', 'doc_id', 'version', 'content_sha256', 'title')} for i in item_ids]
    decision_id = 'bdec-' + records.digest([text, considered, records.now()])[:12]
    task_ids = []
    for label in actions:
        task = await tasks.create(db, scope, title=label[:200], objective_text=f'Board decision {decision_id}: {label}', owner=owner)
        await tasks.mutate(db, scope, task['task_id'], 'evidence_added', {'evidence_kind': 'board_decision', 'ref': decision_id, 'note': text[:400]})
        task_ids.append(task['task_id'])
    await records.append(db, scope, 'board', RUN, 'decision', {'decision_id': decision_id, 'text': text[:4000], 'considered': considered, 'actions': list(actions),
                                                               'task_ids': task_ids, 'supersedes': supersedes})
    return await load(db, scope)


async def ask_akki(db, scope, question):
    """The board's own conversation on the spine: one durable session whose objective is the board itself."""
    board = await load(db, scope)
    session_id = board['chat_session_id']
    if session_id and await sessions.get(scope, session_id) is None:
        session_id = None
    result = await journey.ask(db, scope, question=question, session_id=session_id)
    if result and result['session_id'] != session_id:
        await records.append(db, scope, 'board', RUN, 'chat_session', {'session_id': result['session_id']})
    return result
