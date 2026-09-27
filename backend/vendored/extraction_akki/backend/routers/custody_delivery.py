"""Authenticated metadata-only handoff. Never fetch/stream a provider URL."""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from core import db
from routers.activation_controls import bounded_payload
from services.portal_operational.access import portal_scope
from services.portal_operational.execution_records import existing_request
from services.portal_operational.hold_reasons import disclosure
from services.northena.execution_models import Held
from services.northena.execution_bindings import build_coordinator
from services.custody_delivery.models import DeliveryRequest
from services.custody_delivery.service import CustodyDelivery
from services.activation.runtime_binding import NativeRuntime

router = APIRouter(prefix='/api/portal/requests', tags=['custody-delivery'])
PRIVATE = {'Cache-Control': 'private, no-store', 'Pragma': 'no-cache', 'Referrer-Policy': 'no-referrer'}


def service(request):
    runtime = getattr(request.app.state, 'native_runtime', None)
    if not isinstance(runtime, NativeRuntime) or runtime.custody is None:
        raise Held('CUSTODY_PROVIDER_UNBOUND')
    return CustodyDelivery(runtime.custody, build_coordinator(db, runtime.bindings))


def response(view):
    value = view.model_dump(mode='json', exclude={'url'})
    value['url'] = view.url.get_secret_value() if view.url is not None else None
    return JSONResponse(value, headers=PRIVATE)


def unavailable(exc):
    return JSONResponse({'outcome': 'held', **disclosure(exc.reason_code), 'delivery_verified': False},
                        status_code=404 if exc.reason_code == 'CUSTODY_DELIVERY_NOT_FOUND' else 409, headers=PRIVATE)


@router.post('/{request_id}/delivery')
async def prepare_delivery(request_id: str, request: Request):
    async with portal_scope(request) as scope:
        body = await bounded_payload(request, DeliveryRequest)
        frozen, _ = await existing_request(db, scope, request_id)
        try:
            return response(await service(request).prepare(frozen, body))
        except Held as exc:
            return unavailable(exc)
        except (ValueError, KeyError, TypeError):
            raise HTTPException(409, 'Custody metadata could not be verified.', headers=PRIVATE) from None


@router.get('/{request_id}/deliveries/{delivery_id}')
async def delivery_status(request_id: str, delivery_id: str, request: Request):
    async with portal_scope(request) as scope:
        frozen, _ = await existing_request(db, scope, request_id)
        try:
            return response(await service(request).status(frozen, delivery_id))
        except Held as exc:
            return unavailable(exc)
        except (ValueError, KeyError, TypeError):
            raise HTTPException(409, 'Custody metadata could not be verified.', headers=PRIVATE) from None