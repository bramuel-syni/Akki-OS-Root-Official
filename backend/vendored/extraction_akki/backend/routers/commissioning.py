"""Commissioning, approvals, run view and authorised retrieval — control-plane metadata only."""
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from core import db
from routers.activation_controls import bounded_payload
from services.commissioning import shaping, commission as freeze, approvals, run_view
from services.commissioning.census_profile import tables_for
from services.commissioning.shaping import DraftBody
from services.custody_delivery.service import CustodyDelivery
from services.estate_admission.records import latest
from services.estate_admission.runtimes import admitted_runtimes
from services.extraction_runtime.custody_provider import record_retrieval
from services.northena.execution_bindings import build_coordinator
from services.northena.execution_models import Held
from services.portal_operational import execution
from services.portal_operational.access import portal_scope
from services.portal_operational.execution_records import existing_request
from services.portal_operational.hold_reasons import disclosure
from services.watch import commission_gate
from services.work_orders.kind_profiles import routable

router = APIRouter(prefix='/api/portal', tags=['commissioning'])
PRIVATE = {'Cache-Control': 'private, no-store', 'Pragma': 'no-cache'}


class FreezeBody(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    idempotency_key: str = Field(min_length=8, max_length=128)


class DecideBody(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    group: str = Field(min_length=1, max_length=128)
    decision: Literal['approved', 'refused']
    reason: str = Field(min_length=1, max_length=200)


def _held(exc):
    return JSONResponse({'outcome': 'held', **disclosure(exc.reason_code)}, status_code=409, headers=PRIVATE)


@router.get('/commission/kinds')
async def commission_kinds(request: Request):
    async with portal_scope(request):
        return {'kinds': routable()}


@router.get('/commission/runtimes')
async def commission_runtimes(request: Request):
    """Admitted runtime descriptors of this estate: roles, classes, capacity, reach — never an address."""
    async with portal_scope(request) as scope:
        rows = []
        for rid, d in (await admitted_runtimes(db, scope['tenant_id'])).items():
            rows.append({k: d.get(k) for k in ('runtime_id', 'roles', 'kinds', 'compute_classes', 'capacity', 'enforced_dimensions',
                                                 'reach', 'status', 'executor_version', 'compute_accounting')}
                        | {'transport_kind': d['transport']['kind'], 'attested_at': (d.get('attestation') or {}).get('attested_at')})
        return {'rows': rows, 'count': len(rows)}


@router.get('/commission/profile/{source_id}')
async def source_profile(source_id: str, request: Request):
    async with portal_scope(request) as scope:
        rows = await tables_for(scope['tenant_id'], source_id)
        if rows is None:
            raise HTTPException(403, 'That source is not admitted to this estate.')
        return {'source_id': source_id, 'count': len(rows), 'tables': [
            {k: r[k] for k in ('source_ref', 'label', 'database', 'table', 'row_count', 'column_count', 'primary_key',
                               'personal_columns', 'census_run_id', 'observed_at')} for r in rows]}


@router.get('/commission/destinations')
async def commission_destinations(request: Request):
    """The delivery destinations verified at the estate's admission ceremony — provider, origin and custodian only;
    bucket, prefix and every secret stay server-side. No origin means retrieval is held, not that nothing exists."""
    async with portal_scope(request) as scope:
        record = await latest(db, scope['tenant_id'], 'custody_descriptor', 'default')
        if record is None:
            return {'rows': [], 'count': 0, 'reason_code': 'CUSTODY_DESCRIPTOR_UNRESOLVED'}
        custody = record['payload']['record']
        origin = custody.get('endpoint_origin')
        rows = [{'destination_id': 'default', 'provider': custody['provider'], 'region': custody.get('region'),
                 'custodian_runtime_id': custody['custodian_runtime_id'], 'retrieval_origin': origin,
                 'retrievable_over_https': bool(origin), 'state': 'offered' if origin else 'held',
                 'reason_code': None if origin else 'CUSTODY_ORIGIN_UNAVAILABLE',
                 'basis': custody.get('basis'), 'ledger_ref': record['row']['hash']}]
        return {'rows': rows, 'count': len(rows)}


@router.get('/commission/drafts')
async def list_drafts(request: Request):
    async with portal_scope(request) as scope:
        rows = await shaping.listing(db, scope)
        return {'rows': rows, 'count': len(rows)}


@router.post('/commission/drafts', status_code=201)
async def save_draft(request: Request):
    async with portal_scope(request, write=True) as scope:
        body = await bounded_payload(request, DraftBody)
        return await shaping.save(db, scope, body)


@router.get('/commission/drafts/{draft_id}')
async def get_draft(draft_id: str, request: Request):
    async with portal_scope(request) as scope:
        return await shaping.view(db, scope, draft_id)


@router.post('/commission/drafts/{draft_id}/withdraw')
async def withdraw_draft(draft_id: str, request: Request):
    async with portal_scope(request, write=True) as scope:
        state = await shaping.load(db, scope, draft_id)
        if state['state'] != 'draft':
            raise HTTPException(409, f"Draft is already {state['state']}.")
        await shaping.mark(db, scope, draft_id, 'withdrawn', {'withdrawn_at': datetime.now(timezone.utc).isoformat()})
        return await shaping.view(db, scope, draft_id)


@router.post('/commission/drafts/{draft_id}/freeze', status_code=202)
async def freeze_draft(draft_id: str, request: Request):
    async with portal_scope(request, write=True) as scope:
        body = await bounded_payload(request, FreezeBody)
        with commission_gate.crossing(scope, 'dap.commission', {'draft_id': draft_id, 'idempotency_key': body.idempotency_key}):
            try:
                return await freeze.commission(db, scope, draft_id, body.idempotency_key)
            except Held as exc:
                return _held(exc)


@router.post('/commission/{request_id}/advance')
async def advance_commissioned(request_id: str, request: Request):
    """One bounded advance of a commissioned request under its frozen deadline (the same slot the
    generic /execution/advance uses; the deadline is read from the work order, never re-supplied)."""
    async with portal_scope(request, write=True) as scope:
        for row in await shaping.listing(db, scope):
            if row.get('request_id') == request_id:
                state = await shaping.load(db, scope, row['draft_id'])
                budget = execution.ExecutionBudget(deadline_epoch=int(state['deadline_epoch']))
                try:
                    view = await execution.advance(db, scope, request_id, budget,
                                                   bindings=getattr(request.app.state, 'execution_bindings', None),
                                                   receipts=getattr(request.app.state, 'activation_receipts', None))
                except Held as exc:
                    return _held(exc)
                return JSONResponse({**view.model_dump(mode='json'), **disclosure(view.reason_code)}, headers=PRIVATE)
        raise HTTPException(404, 'No commission record for this request.')


@router.get('/approvals/queue')
async def approvals_queue(request: Request):
    async with portal_scope(request) as scope:
        rows = await approvals.queue(db, scope)
        return {'rows': rows, 'count': len(rows)}


@router.get('/approvals/{request_id}')
async def approvals_routing(request_id: str, request: Request):
    async with portal_scope(request) as scope:
        return await approvals.routing(db, scope, request_id)


@router.post('/approvals/{request_id}/decide')
async def approvals_decide(request_id: str, request: Request):
    async with portal_scope(request, write=True) as scope:
        body = await bounded_payload(request, DecideBody)
        with commission_gate.crossing(scope, 'dap.approval', {'request_id': request_id, 'group': body.group, 'decision': body.decision}):
            return await approvals.decide(db, scope, request_id, body.group, body.decision, body.reason)


@router.get('/requests/{request_id}/run')
async def request_run(request_id: str, request: Request):
    async with portal_scope(request) as scope:
        frozen, _ = await existing_request(db, scope, request_id)
        return await run_view.run_view(db, frozen)


@router.get('/requests/{request_id}/commission')
async def request_commission(request_id: str, request: Request):
    """The frozen work order and its deadline even before the first advance (no execution snapshot yet)."""
    async with portal_scope(request) as scope:
        for row in await shaping.listing(db, scope):
            if row.get('request_id') == request_id:
                return await shaping.view(db, scope, row['draft_id'])
        raise HTTPException(404, 'No commission record for this request.')


@router.post('/requests/{request_id}/deliveries/{delivery_id}/retrieve')
async def authorise_retrieval(request_id: str, delivery_id: str, request: Request):
    """The requester declares authorised retrieval; the custodian then proves completion from the store."""
    async with portal_scope(request, write=True) as scope:
        frozen, _ = await existing_request(db, scope, request_id)
        runtime = getattr(request.app.state, 'native_runtime', None)
        if runtime is None or runtime.custody is None:
            return _held(Held('CUSTODY_PROVIDER_UNBOUND'))
        with commission_gate.crossing(scope, 'dap.delivery', {'request_id': request_id, 'delivery_id': delivery_id}):
            redeemed, ref = await record_retrieval(db, delivery_id, request_id)
            try:
                view = await CustodyDelivery(runtime.custody, build_coordinator(db, runtime.bindings)).status(frozen, delivery_id)
            except Held as exc:
                return _held(exc)
            value = view.model_dump(mode='json', exclude={'url'})
            return JSONResponse({**value, 'retrieval_receipt_ref': ref, 'redeemed_epoch': redeemed}, headers=PRIVATE)
