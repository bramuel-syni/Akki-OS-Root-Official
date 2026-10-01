"""services.chat.router — the governed, memory-backed chat surface (M4 answers · M5 durable sessions).

POST /api/chat/ask                       one question → one decision (warm | fresh | refused) inside a durable session
GET  /api/chat/sessions                  the requester's sessions (metadata; turns excluded)
GET  /api/chat/sessions/{id}             one session with every turn and its evidence
POST /api/chat/sessions/{id}/compact     compact the closed working context (ledger row → artefact → pointer)
GET  /api/chat/sessions/{id}/reload      scope-checked, hash-verified reload of the compacted context — or refusal
POST /api/chat/sessions/{id}/archive     close the session (turns stay; nothing is deleted)

Identity is the same portal gate every estate surface uses; tenant and principal come only from the signed-in
account. Held conditions surface as the existing 409 disclosure, never as an answer.
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from core import db
from services.chat import evaluation, journey, sessions
from services.northena.execution_models import Held
from services.portal_operational.access import portal_scope
from services.portal_operational.hold_reasons import disclosure
from services.watch import commission_gate

router = APIRouter(tags=['chat'])
PRIVATE = {'Cache-Control': 'private, no-store', 'Pragma': 'no-cache'}


class AskRequest(BaseModel):
    model_config = ConfigDict(extra='ignore')
    question: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = Field(default=None, max_length=64)
    model: str = Field(default=journey.DEFAULT_MODEL, max_length=64)
    provider: str = Field(default=journey.DEFAULT_PROVIDER, max_length=32)


def _held(exc):
    return JSONResponse({'outcome': 'held', **disclosure(exc.reason_code)}, status_code=409, headers=PRIVATE)


async def _session_or_404(scope, session_id):
    session = await sessions.get(scope, session_id)
    if session is None:
        raise HTTPException(404, 'No such conversation in your scope.')
    return session


@router.post('/api/chat/ask')
async def post_chat_ask(body: AskRequest, request: Request):
    async with portal_scope(request) as scope:
        try:
            result = await journey.ask(db, scope, question=body.question, session_id=body.session_id,
                                       model=body.model, provider=body.provider)
        except Held as exc:
            return _held(exc)
        if result is None:
            raise HTTPException(404, 'No such conversation in your scope.')
        return JSONResponse(result, headers=PRIVATE)


@router.get('/api/chat/sessions')
async def list_sessions(request: Request, archived: bool = False):
    async with portal_scope(request) as scope:
        rows = await sessions.listing(scope, archived=archived)
        return JSONResponse({'rows': rows, 'count': len(rows)}, headers=PRIVATE)


@router.get('/api/chat/sessions/{session_id}')
async def get_session(session_id: str, request: Request):
    async with portal_scope(request) as scope:
        return JSONResponse(await _session_or_404(scope, session_id), headers=PRIVATE)


@router.post('/api/chat/sessions/{session_id}/compact')
async def compact_session(session_id: str, request: Request):
    async with portal_scope(request) as scope:
        session = await _session_or_404(scope, session_id)
        compaction = await sessions.compact(scope, session, actor=scope['principal_id'])
        if compaction is None:
            return JSONResponse({'status': 'nothing_to_compact', 'reason': 'Every turn of this session is already compacted or the session has no turns.',
                                 'compaction': session.get('compaction')}, headers=PRIVATE)
        return JSONResponse({'status': 'compacted', 'compaction': compaction}, headers=PRIVATE)


@router.get('/api/chat/sessions/{session_id}/reload')
async def reload_session(session_id: str, request: Request):
    async with portal_scope(request) as scope:
        session = await _session_or_404(scope, session_id)
        return JSONResponse(await sessions.reload(scope, session), headers=PRIVATE)


@router.post('/api/chat/sessions/{session_id}/archive')
async def archive_session(session_id: str, request: Request):
    async with portal_scope(request) as scope:
        await _session_or_404(scope, session_id)
        await sessions.update(scope, session_id, {'archived': True})
        return JSONResponse({'status': 'archived', 'session_id': session_id}, headers=PRIVATE)


class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra='ignore')
    size: int = Field(default=200, ge=evaluation.MIN_SIZE, le=evaluation.MAX_SIZE)
    seed: int = Field(default=20261001, ge=0)


@router.get('/api/chat/evaluations')
async def list_evaluations(request: Request):
    async with portal_scope(request) as scope:
        rows = await evaluation.listing(scope)
        return JSONResponse({'rows': rows, 'count': len(rows), 'rule': evaluation.RULE}, headers=PRIVATE)


@router.get('/api/chat/evaluations/{evaluation_id}')
async def get_evaluation(evaluation_id: str, request: Request):
    async with portal_scope(request) as scope:
        doc = await evaluation.get(scope, evaluation_id)
        if doc is None:
            raise HTTPException(404, 'No such evaluation in your estate.')
        return JSONResponse(doc, headers=PRIVATE)


@router.post('/api/chat/evaluations', status_code=202)
async def start_evaluation(body: EvaluationRequest, request: Request):
    """Operator-only: runs a bounded benchmark through the live answering journey in the background; model spend is real."""
    async with portal_scope(request, write=True) as scope:
        with commission_gate.crossing(scope, 'chat.evaluation', body.model_dump()):
            try:
                doc = await evaluation.start(scope, size=body.size, seed=body.seed)
            except Held as exc:
                return _held(exc)
            return JSONResponse(doc, status_code=202, headers=PRIVATE)
