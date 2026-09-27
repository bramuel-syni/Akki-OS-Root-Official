from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from core import db
from routers.activation_controls import bounded_payload
from routers.custody_delivery import service, response, unavailable, PRIVATE
from services.portal_operational.access import portal_scope
from services.portal_operational import query_intents, query_execution, query_plans
from services.portal_operational.hold_reasons import disclosure
from services.transform_forms.callable_skill_gate import require_governed_skill_query
from services.northena.execution_models import Held
from services.custody_delivery.models import DeliveryRequest

router = APIRouter(prefix='/api/callable_skill', tags=['governed-skill-queries'])


def fail(exc):
    return JSONResponse({'outcome': 'held', **disclosure(exc.reason_code), 'execution_verified': False,
                         'delivery_verified': False}, status_code=404 if exc.reason_code == 'SKILL_QUERY_NOT_FOUND' else 409,
                        headers=PRIVATE)


@router.post('/{skill_id}/query-intents')
async def submit_intent(skill_id: str, request: Request):
    provisioning = await require_governed_skill_query(request, skill_id, db)
    if isinstance(provisioning, JSONResponse):
        return provisioning
    async with portal_scope(request) as scope:
        body = await bounded_payload(request, query_intents.QueryIntentBody)
        try:
            intent = await query_intents.submit(db, scope, skill_id, provisioning, body)
            current = await query_execution.current_status(db, scope, skill_id, intent['row']['run_id'], provisioning,
                getattr(request.app.state, 'native_runtime', None))
            return JSONResponse(current, status_code=201, headers=PRIVATE)
        except Held as exc:
            return fail(exc)


@router.get('/{skill_id}/queries/{query_id}')
async def query_status(skill_id: str, query_id: str, request: Request):
    gate = await require_governed_skill_query(request, skill_id, db)
    if isinstance(gate, JSONResponse):
        return gate
    async with portal_scope(request) as scope:
        try:
            current = await query_execution.current_status(db, scope, skill_id, query_id, gate,
                getattr(request.app.state, 'native_runtime', None))
            return JSONResponse(current, headers=PRIVATE)
        except Held as exc:
            return fail(exc)


@router.post('/{skill_id}/queries/{query_id}/advance')
async def advance_query(skill_id: str, query_id: str, request: Request):
    provisioning = await require_governed_skill_query(request, skill_id, db)
    if isinstance(provisioning, JSONResponse):
        return provisioning
    async with portal_scope(request) as scope:
        try:
            result = await query_execution.advance(db, scope, skill_id, query_id, provisioning,
                getattr(request.app.state, 'native_runtime', None))
            checked = await require_governed_skill_query(request, skill_id, db)
            if isinstance(checked, JSONResponse):
                return checked
            rows = await query_intents.events(db, scope, skill_id, query_id)
            query_intents.require_current_provisioning(rows[0], checked)
            return JSONResponse(result, headers=PRIVATE, status_code=409 if result['outcome'] == 'held' else 200)
        except Held as exc:
            return fail(exc)


@router.post('/{skill_id}/queries/{query_id}/delivery')
async def query_delivery(skill_id: str, query_id: str, request: Request):
    provisioning = await require_governed_skill_query(request, skill_id, db)
    if isinstance(provisioning, JSONResponse):
        return provisioning
    async with portal_scope(request) as scope:
        body = await bounded_payload(request, DeliveryRequest)
        try:
            rows = await query_intents.events(db, scope, skill_id, query_id)
            # Re-run proof checks; old UI status is not a release authority.
            runtime = getattr(request.app.state, 'native_runtime', None)
            verified = await query_execution.advance(db, scope, skill_id, query_id, provisioning, runtime)
            if not verified.get('execution_verified') or body.artifact_ref not in verified.get('artifact_refs', []):
                raise Held('SKILL_GROUNDING_RECEIPT_REQUIRED')
            frozen = await query_plans.resolve(runtime, scope, rows[0], provisioning)
            offered = await service(request).prepare(frozen, body)
            current = await require_governed_skill_query(request, skill_id, db)
            if isinstance(current, JSONResponse):
                return current
            query_intents.require_current_provisioning(rows[0], current)
            return response(offered)
        except Held as exc:
            return unavailable(exc)
        except (ValueError, KeyError, TypeError):
            raise HTTPException(409, 'Skill custody metadata could not be verified.', headers=PRIVATE) from None


@router.get('/{skill_id}/queries/{query_id}/deliveries/{delivery_id}')
async def query_delivery_status(skill_id: str, query_id: str, delivery_id: str, request: Request):
    provisioning = await require_governed_skill_query(request, skill_id, db)
    if isinstance(provisioning, JSONResponse):
        return provisioning
    async with portal_scope(request) as scope:
        try:
            runtime = getattr(request.app.state, 'native_runtime', None)
            checked = await query_execution.current_status(db, scope, skill_id, query_id, provisioning, runtime)
            if not checked.get('execution_verified'):
                raise Held('SKILL_GROUNDING_RECEIPT_REQUIRED')
            rows = await query_intents.events(db, scope, skill_id, query_id)
            frozen = await query_plans.resolve(runtime, scope, rows[0], provisioning)
            status = await service(request).status(frozen, delivery_id)
            current = await require_governed_skill_query(request, skill_id, db)
            if isinstance(current, JSONResponse):
                return current
            query_intents.require_current_provisioning(rows[0],current)
            return response(status)
        except Held as exc:
            return unavailable(exc)
        except (ValueError, KeyError, TypeError):
            raise HTTPException(409, 'Skill custody metadata could not be verified.', headers=PRIVATE) from None