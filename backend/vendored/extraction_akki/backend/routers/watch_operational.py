"""Ordinary tenant-bound Watch reader and the reserved human set; no public authority-minting endpoints."""
import hmac
import os
import re
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Header, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from pymongo.errors import DuplicateKeyError

from core import db
from services.enforce.census_identity import census_identity
from services.watch import decisions, independent_witness, learning_loop, notices, tripwire, witness_binding
from services.watch.operational_reads import state_for
from services.watch import commission_gate

router = APIRouter(tags=['tenant-scoped-watch'])


class WatchEnvelope(BaseModel):
    model_config = ConfigDict(extra='allow')
    tenant_id: str


def _operator(actor):
    if not {'operator', 'master_admin'}.intersection(actor['roles']):
        raise HTTPException(403, 'Estate operator access is required for Watch records.')
    return actor


@router.get('/api/portal/watch/state', response_model=WatchEnvelope)
@router.get('/api/watch/state', response_model=WatchEnvelope)
@router.get('/api/grey_mirror/state', response_model=WatchEnvelope)
async def state(actor=Depends(census_identity)):
    return state_for(_operator(actor), independent=await independent_witness.status(db))


@router.get('/api/portal/watch/notices', response_model=WatchEnvelope)
def my_notices(actor=Depends(census_identity)):
    """What the Watch told THIS principal. Any admitted member reads their own notices only."""
    commission_gate.reconcile_expired(actor['tenant_id'])
    return {'tenant_id': actor['tenant_id'], 'principal_id': actor['principal_id'],
            'notices': notices.for_principal(actor['tenant_id'], actor['principal_id'])}


@router.post('/api/portal/watch/decisions/{decision_id}', response_model=WatchEnvelope)
def decide(decision_id: str, body: dict = Body(...), actor=Depends(census_identity)):
    """approve (dual control: two distinct operators) · decline · acknowledge (changes no protection)."""
    _operator(actor)
    try:
        item = decisions.act(actor['tenant_id'], decision_id, actor['principal_id'], body.get('act'), body.get('note', ''))
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'decision': item}


@router.post('/api/portal/watch/requests/demark', response_model=WatchEnvelope)
def request_demark(body: dict = Body(...), actor=Depends(census_identity)):
    """Under watch → Decisions: de-marking is a human, dual-control act, never autonomous."""
    _operator(actor)
    held = commission_gate.sever_state(actor['tenant_id'], str(body.get('subject_ref', '')).split(':', 1)[-1])
    if not held:
        raise HTTPException(409, 'That subject carries no live mark or severance in your tenant; nothing to request.')
    item = decisions.open_decision(actor['tenant_id'], 'demark_release', body['subject_ref'], {'action_ref': held['action_id'], 'mark_ref': held['mark_id']},
                                   actor['principal_id'], f"De-mark and release requested · {body['subject_ref']}")
    return {'tenant_id': actor['tenant_id'], 'decision': item}


@router.post('/api/portal/watch/requests/redeclaration', response_model=WatchEnvelope)
def request_redeclaration(body: dict = Body(...), actor=Depends(census_identity)):
    """Ask a watched subject for an updated declaration: a real notice, a real record, no penalty."""
    _operator(actor)
    principal = str(body.get('subject_ref', '')).split(':', 1)[-1]
    if not principal:
        raise HTTPException(422, 'subject_ref is required.')
    notice = notices.send(actor['tenant_id'], principal, 'redeclaration',
                          'The Watch has noted a widening pattern on your commissions. Please confirm or update the declared purpose of your census work with your estate operator. Nothing has been restricted by this request.',
                          {'requested_by': actor['principal_id']})
    commission_gate._append(actor['tenant_id'], {'kind': 'redeclaration_requested', 'at': notice['at'], 'tenant_id': actor['tenant_id'],
                                                 'principal_id': principal, 'requested_by': actor['principal_id'], 'notice_id': notice['notice_id']})
    return {'tenant_id': actor['tenant_id'], 'notice': notice}


@router.post('/api/portal/watch/learning/propose', response_model=WatchEnvelope)
def propose(actor=Depends(census_identity)):
    """Finding → CIF → acceptance → L-4 → grounding → Decisions. Ratification needs two operators."""
    _operator(actor)
    try:
        item = learning_loop.propose(actor['tenant_id'], actor['principal_id'])
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'decision': item}


@router.post('/api/portal/watch/mirage/plant', response_model=WatchEnvelope)
def plant(body: dict = Body(...), actor=Depends(census_identity)):
    """Mkono plants a decoy descriptor one-way for this tenant's gates; the isolation check is measured first."""
    _operator(actor)
    decoy = str(body.get('decoy_ref', '')).strip()
    if len(decoy) < 8:
        raise HTTPException(422, 'decoy_ref must be a descriptor of at least 8 characters.')
    try:
        planted = tripwire.plant(actor['tenant_id'], decoy, int(body.get('ttl_seconds', 86400)), actor['principal_id'])
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {'tenant_id': actor['tenant_id'], 'planted': planted}


@router.post('/api/portal/watch/witness/break-in', response_model=WatchEnvelope)
def break_in(body: dict = Body(default={}), actor=Depends(census_identity)):
    """Standing break-in test against a tenant-owned gate action; the production writer must refuse."""
    _operator(actor)
    owned = commission_gate.owned_records(actor['tenant_id'])['action_ids']
    target = body.get('action_id') or (sorted(owned, key=lambda a: owned[a]['at'])[-1] if owned else None)
    if not target or target not in owned:
        raise HTTPException(409, 'No tenant-owned gate action is on record to test against.')
    result = witness_binding.break_in(target)
    commission_gate._append(actor['tenant_id'], {'kind': 'break_in', 'tenant_id': actor['tenant_id'], 'principal_id': actor['principal_id'], **result})
    return {'tenant_id': actor['tenant_id'], 'break_in': result}


@router.get('/api/portal/watch/witness', response_model=WatchEnvelope)
async def witness_status(actor=Depends(census_identity)):
    """The independent watchdog's state: host, last countersigned pass, findings, and whether it has gone silent."""
    _operator(actor)
    return {'tenant_id': actor['tenant_id'], **await independent_witness.status(db)}


@router.post('/api/portal/watch/witness/pass', response_model=WatchEnvelope)
async def witness_pass(actor=Depends(census_identity)):
    """Run one witness pass now (estate operator). The host judges and signs; this only verifies and banks."""
    _operator(actor)
    result = await independent_witness.run_pass(db, actor=actor['principal_id'])
    return {'tenant_id': actor['tenant_id'], 'pass': {k: v for k, v in result.items() if k != 'statement'}}


@router.post('/api/watch/witness/cron')
async def witness_cron(request: Request, background: BackgroundTasks, authorization: str | None = Header(default=None), x_webhook_id: str | None = Header(default=None)):
    # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.
    expected = os.environ['WEBHOOK_CRON_SECRET']
    supplied = authorization[7:] if authorization and authorization.startswith('Bearer ') else ''
    if not supplied or not hmac.compare_digest(supplied, expected):
        raise HTTPException(401, 'Invalid scheduler authorization')
    try:
        body = await request.json()
        if not isinstance(body, dict) or body.get('event') != 'schedule.triggered' or not isinstance(body.get('run_id'), str) or not body['run_id'] or body.get('data') is not None:
            raise ValueError()
        key = x_webhook_id or body['run_id']
        if not re.fullmatch(r'[a-zA-Z0-9_.:-]{1,150}', key):
            raise ValueError()
    except Exception as exc:
        raise HTTPException(400, 'Invalid schedule envelope') from exc
    try:
        await db.watch_witness_webhooks.insert_one({'_id': key, 'received_at': datetime.now(timezone.utc).isoformat()})
    except DuplicateKeyError:
        return {'accepted': True, 'duplicate': True}
    background.add_task(independent_witness.run_pass, db, 'scheduler')
    return {'accepted': True, 'duplicate': False}


def unbound_authority(actor=Depends(census_identity)):
    raise HTTPException(409, 'This legacy Watch surface has no admitted authority binding. No Watch record or protection was changed.')


def install(app):
    old = [route for route in app.routes if getattr(route, 'path', '').startswith(('/api/watch/', '/api/grey_mirror/'))]
    app.router.routes[:] = [route for route in app.routes if route not in old]
    app.include_router(router)
    covered = {(route.path, method) for route in router.routes for method in route.methods}
    for route in old:
        methods = [method for method in route.methods if (route.path, method) not in covered]
        if methods:
            app.add_api_route(route.path, unbound_authority, methods=methods, tags=['watch-legacy-boundary'])
