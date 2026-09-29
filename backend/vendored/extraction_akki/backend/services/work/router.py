"""Work surface (M5): tasks, documents, goals, board and rights withdrawal — identity-scoped, ledger-backed."""
from typing import List, Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from core import db
from services.northena.execution_models import Held
from services.portal_operational.access import portal_scope
from services.portal_operational.hold_reasons import disclosure
from services.work import board, documents, goals, records, tasks, withdrawal

router = APIRouter(prefix='/api/work', tags=['work'])
PRIVATE = {'Cache-Control': 'private, no-store', 'Pragma': 'no-cache'}


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')


class TaskCreate(Strict):
    title: Optional[str] = Field(default=None, max_length=200)
    objective_text: Optional[str] = Field(default=None, max_length=8000)
    session_id: Optional[str] = Field(default=None, max_length=64)
    turn_id: Optional[str] = Field(default=None, max_length=64)
    owner: Optional[str] = Field(default=None, max_length=64)
    due: Optional[str] = Field(default=None, max_length=40)


class Assign(Strict):
    owner: str = Field(max_length=64)


class Contributor(Strict):
    contributor: str = Field(max_length=64)
    role: str = Field(min_length=1, max_length=80)


class Item(Strict):
    label: str = Field(min_length=1, max_length=400)
    evidence_ref: Optional[str] = Field(default=None, max_length=512)


class ItemState(Strict):
    item_id: str = Field(max_length=32)
    state: str = Field(pattern=r'^(open|done|blocked)$')
    evidence_ref: Optional[str] = Field(default=None, max_length=512)


class Evidence(Strict):
    evidence_kind: str = Field(pattern=r'^(qualified_unit|receipt|document|measurement|board_decision|external)$')
    ref: str = Field(min_length=1, max_length=512)
    note: Optional[str] = Field(default=None, max_length=1000)


class Question(Strict):
    text: str = Field(min_length=1, max_length=2000)


class CloseQuestion(Strict):
    question_id: str = Field(max_length=32)
    answer: Optional[str] = Field(default=None, max_length=4000)


class Attach(Strict):
    doc_id: str = Field(max_length=64)


class LinkGoal(Strict):
    goal_id: str = Field(max_length=64)


class TaskRef(Strict):
    task_id: str = Field(max_length=64)


class State(Strict):
    state: str = Field(pattern=r'^(open|in_progress|done|withdrawn)$')


class DocumentSave(Strict):
    title: Optional[str] = Field(default=None, max_length=200)
    body: Optional[str] = Field(default=None, max_length=60000)
    session_id: Optional[str] = Field(default=None, max_length=64)
    turn_id: Optional[str] = Field(default=None, max_length=64)
    doc_id: Optional[str] = Field(default=None, max_length=64)


class Measure(Strict):
    name: str = Field(min_length=1, max_length=120)
    unit: Optional[str] = Field(default=None, max_length=40)
    target: float
    baseline: Optional[float] = None
    direction: str = Field(default='at_least', pattern=r'^(at_least|at_most)$')
    on_track_from: Optional[float] = Field(default=None, ge=0, le=1)


class GoalCreate(Strict):
    title: str = Field(min_length=1, max_length=200)
    type: str = Field(default='objective', max_length=40)
    measure: Measure
    owner: Optional[str] = Field(default=None, max_length=64)
    by_date: Optional[str] = Field(default=None, max_length=40)


class Measurement(Strict):
    value: float
    evidence_ref: str = Field(min_length=1, max_length=512)
    note: Optional[str] = Field(default=None, max_length=1000)


class BoardDocument(Strict):
    doc_id: str = Field(max_length=64)
    doc_kind: Optional[str] = Field(default=None, max_length=40)
    note: Optional[str] = Field(default=None, max_length=1000)


class BoardQuestion(Strict):
    text: str = Field(min_length=1, max_length=2000)
    item_id: Optional[str] = Field(default=None, max_length=32)


class BoardAnswer(Strict):
    question_id: str = Field(max_length=32)
    text: str = Field(min_length=1, max_length=4000)


class Decision(Strict):
    text: str = Field(min_length=1, max_length=4000)
    item_ids: List[str] = Field(min_length=1)
    actions: List[str] = Field(default_factory=list)
    supersedes: Optional[str] = Field(default=None, max_length=32)
    owner: Optional[str] = Field(default=None, max_length=64)


class Ask(Strict):
    question: str = Field(min_length=1, max_length=4000)


class Withdraw(Strict):
    artifact_ref: str = Field(min_length=1, max_length=512)
    reason_code: str = Field(default=withdrawal.REASON, pattern=r'^[A-Z][A-Z0-9_]{2,63}$')


def _ok(body):
    return JSONResponse(body, headers=PRIVATE)


def _held(exc):
    return JSONResponse({'outcome': 'held', **disclosure(exc.reason_code)}, status_code=409, headers=PRIVATE)


@router.get('/team')
async def get_team(request: Request):
    async with portal_scope(request) as scope:
        rows = await records.team(db, scope)
        return _ok({'rows': rows, 'count': len(rows), 'me': scope['principal_id']})


@router.get('/tasks')
async def list_tasks(request: Request):
    async with portal_scope(request) as scope:
        rows = await tasks.listing(db, scope)
        return _ok({'rows': rows, 'count': len(rows)})


@router.post('/tasks', status_code=201)
async def create_task(body: TaskCreate, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await tasks.create(db, scope, title=body.title, objective_text=body.objective_text, session_id=body.session_id,
                                      turn_id=body.turn_id, owner=body.owner, due=body.due))


@router.get('/tasks/{task_id}')
async def get_task(task_id: str, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await tasks.load(db, scope, task_id))


_TASK_MUTATIONS = {'assign': ('assigned', Assign), 'contributors': ('contributor_added', Contributor), 'items': ('item_added', Item),
                   'item-state': ('item_state', ItemState), 'evidence': ('evidence_added', Evidence), 'questions': ('question_added', Question),
                   'close-question': ('question_closed', CloseQuestion), 'documents': ('document_attached', Attach), 'goals': ('goal_linked', LinkGoal),
                   'state': ('state', State)}


def _task_route(path, kind, model):
    async def endpoint(task_id: str, body: model, request: Request):  # type: ignore[valid-type]
        async with portal_scope(request) as scope:
            return _ok(await tasks.mutate(db, scope, task_id, kind, body.model_dump()))
    endpoint.__name__ = f'task_{kind}'
    router.add_api_route(f'/tasks/{{task_id}}/{path}', endpoint, methods=['POST'])


for _path, (_kind, _model) in _TASK_MUTATIONS.items():
    _task_route(_path, _kind, _model)


@router.get('/documents')
async def list_documents(request: Request):
    async with portal_scope(request) as scope:
        rows = [documents.summary(d) for d in await documents.listing(db, scope)]
        return _ok({'rows': rows, 'count': len(rows)})


@router.post('/documents', status_code=201)
async def save_document(body: DocumentSave, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await documents.save(db, scope, title=body.title, body=body.body, session_id=body.session_id, turn_id=body.turn_id, doc_id=body.doc_id))


@router.get('/documents/{doc_id}')
async def get_document(doc_id: str, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await documents.load(db, scope, doc_id))


@router.get('/goals')
async def list_goals(request: Request):
    async with portal_scope(request) as scope:
        rows = await goals.listing(db, scope)
        return _ok({'rows': rows, 'count': len(rows)})


@router.post('/goals', status_code=201)
async def create_goal(body: GoalCreate, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await goals.create(db, scope, title=body.title, measure=body.measure.model_dump(), type_=body.type, owner=body.owner, by_date=body.by_date))


@router.get('/goals/{goal_id}')
async def get_goal(goal_id: str, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await goals.load(db, scope, goal_id))


@router.post('/goals/{goal_id}/measure')
async def measure_goal(goal_id: str, body: Measurement, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await goals.measure(db, scope, goal_id, value=body.value, evidence_ref=body.evidence_ref, note=body.note))


@router.post('/goals/{goal_id}/contributors')
async def goal_contributor(goal_id: str, body: Contributor, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await goals.mutate(db, scope, goal_id, 'contributor_added', body.model_dump()))


@router.post('/goals/{goal_id}/tasks')
async def goal_task(goal_id: str, body: TaskRef, request: Request):
    async with portal_scope(request) as scope:
        await tasks.mutate(db, scope, body.task_id, 'goal_linked', {'goal_id': goal_id})
        return _ok(await goals.mutate(db, scope, goal_id, 'task_linked', {'task_id': body.task_id}))


@router.get('/board')
async def get_board(request: Request):
    async with portal_scope(request) as scope:
        return _ok(await board.load(db, scope))


@router.post('/board/documents')
async def board_document(body: BoardDocument, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await board.add_document(db, scope, body.doc_id, doc_kind=body.doc_kind, note=body.note))


@router.post('/board/questions')
async def board_question(body: BoardQuestion, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await board.ask_question(db, scope, body.text, item_id=body.item_id))


@router.post('/board/answers')
async def board_answer(body: BoardAnswer, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await board.answer_question(db, scope, body.question_id, body.text))


@router.post('/board/decisions')
async def board_decision(body: Decision, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await board.decide(db, scope, text=body.text, item_ids=body.item_ids, actions=body.actions, supersedes=body.supersedes, owner=body.owner))


@router.post('/board/ask')
async def board_ask(body: Ask, request: Request):
    async with portal_scope(request) as scope:
        try:
            return _ok(await board.ask_akki(db, scope, body.question))
        except Held as exc:
            return _held(exc)


@router.get('/rights/dependents')
async def rights_dependents(artifact_ref: str, request: Request):
    async with portal_scope(request) as scope:
        return _ok(await withdrawal.dependents(db, scope, artifact_ref))


@router.post('/rights/withdraw')
async def rights_withdraw(body: Withdraw, request: Request):
    async with portal_scope(request, write=True) as scope:
        try:
            return _ok(await withdrawal.withdraw(db, scope, body.artifact_ref, body.reason_code))
        except Held as exc:
            return _held(exc)
