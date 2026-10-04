"""Context-as-a-Service routes. Licensor side (estate operator): admit clients, grant/revoke licences, issue/revoke keys, read deliveries, memory and
metering. Client side (external application): authenticate with its own key (`X-CaaS-Key`), see its licence, obtain governed deliveries."""
import asyncio
from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from services.enforce.census_identity import census_identity
from services.training_lab import contracts as c

router = APIRouter(prefix='/api/caas', tags=['caas'])


def _operator(actor):
    if not {'operator', 'master_admin'}.intersection(actor['roles']): raise HTTPException(403, 'An admitted operator is required')


class AdmitClient(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    application: str = Field(min_length=1, max_length=400)
    contact: str | None = Field(default=None, max_length=200)
    note: str | None = Field(default=None, max_length=600)


class ClientTransition(BaseModel):
    action: Literal['suspend', 'reinstate', 'revoke']
    note: str | None = Field(default=None, max_length=600)


class GrantLicence(BaseModel):
    purpose: str = Field(min_length=3, max_length=600)
    products: list[str] = Field(min_length=1, max_length=20)
    deliveries_per_period: int = Field(default=100, ge=1, le=100000)
    period: Literal['month', 'day'] = 'month'
    supersedes: str | None = None


class Reason(BaseModel):
    reason: str = Field(min_length=1, max_length=600)


class Deliver(BaseModel):
    product: str = Field(min_length=1, max_length=80)
    brief: dict | None = None


def _svc():
    from services.caas import service
    return service


def _wrap(fn, *args):
    svc = _svc()
    try: return fn(*args)
    except LookupError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    except svc.Refused as exc: raise HTTPException(exc.code, exc.text) from exc


# ----------------------------------------------------------------------------- licensor
@router.get('/overview', response_model=c.Envelope)
async def overview(actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(_svc().overview, actor['tenant_id'])}


@router.get('/products', response_model=c.Envelope)
async def products(actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'products': _svc().PRODUCTS}


@router.get('/clients', response_model=c.Envelope)
async def clients(actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'clients': await asyncio.to_thread(_svc().list_clients, actor['tenant_id'])}


@router.post('/clients', status_code=201, response_model=c.Envelope)
async def admit(body: AdmitClient, actor=Depends(census_identity)):
    _operator(actor)
    return {'tenant_id': actor['tenant_id'], 'client': await asyncio.to_thread(_svc().admit_client, actor['tenant_id'], actor['principal_id'], body.model_dump())}


@router.get('/clients/{client_id}', response_model=c.Envelope)
async def client(client_id: str, actor=Depends(census_identity)):
    doc = await asyncio.to_thread(_svc().client, actor['tenant_id'], client_id)
    if not doc: raise HTTPException(404, 'No client with that identity in this estate')
    return {'tenant_id': actor['tenant_id'], 'client': doc}


@router.post('/clients/{client_id}/transition', response_model=c.Envelope)
async def transition(client_id: str, body: ClientTransition, actor=Depends(census_identity)):
    _operator(actor)
    doc = await asyncio.to_thread(_wrap, _svc().transition_client, actor['tenant_id'], actor['principal_id'], client_id, body.action, body.note)
    return {'tenant_id': actor['tenant_id'], 'client': doc}


@router.post('/clients/{client_id}/licences', status_code=201, response_model=c.Envelope)
async def grant(client_id: str, body: GrantLicence, actor=Depends(census_identity)):
    _operator(actor)
    doc = await asyncio.to_thread(_wrap, _svc().grant_licence, actor['tenant_id'], actor['principal_id'], client_id, body.model_dump())
    return {'tenant_id': actor['tenant_id'], 'licence': doc}


@router.post('/licences/{licence_id}/revoke', response_model=c.Envelope)
async def revoke_licence(licence_id: str, body: Reason, actor=Depends(census_identity)):
    _operator(actor)
    doc = await asyncio.to_thread(_wrap, _svc().revoke_licence, actor['tenant_id'], actor['principal_id'], licence_id, body.reason)
    return {'tenant_id': actor['tenant_id'], 'licence': doc}


@router.post('/licences/{licence_id}/keys', status_code=201, response_model=c.Envelope)
async def issue_key(licence_id: str, actor=Depends(census_identity)):
    """The secret is returned once and never stored in clear."""
    _operator(actor)
    key, secret = await asyncio.to_thread(_wrap, _svc().issue_key, actor['tenant_id'], actor['principal_id'], licence_id)
    return {'tenant_id': actor['tenant_id'], 'key': key, 'secret': secret, 'shown_once': True}


@router.post('/keys/{key_id}/revoke', response_model=c.Envelope)
async def revoke_key(key_id: str, body: Reason, actor=Depends(census_identity)):
    _operator(actor)
    doc = await asyncio.to_thread(_wrap, _svc().revoke_key, actor['tenant_id'], actor['principal_id'], key_id, body.reason)
    return {'tenant_id': actor['tenant_id'], 'key': doc}


@router.get('/licences/{licence_id}/memory', response_model=c.Envelope)
async def licence_memory(licence_id: str, actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'licence_id': licence_id, 'memory': await asyncio.to_thread(_svc().memory, actor['tenant_id'], licence_id)}


@router.get('/deliveries', response_model=c.Envelope)
async def deliveries(client_id: str | None = None, actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], 'deliveries': await asyncio.to_thread(_svc().deliveries, actor['tenant_id'], client_id)}


@router.get('/deliveries/{delivery_id}', response_model=c.Envelope)
async def delivery(delivery_id: str, actor=Depends(census_identity)):
    doc = await asyncio.to_thread(_svc().delivery, actor['tenant_id'], delivery_id)
    if not doc: raise HTTPException(404, 'No delivery with that reference in this estate')
    return {'tenant_id': actor['tenant_id'], 'delivery': doc}


@router.get('/metering', response_model=c.Envelope)
async def metering(period: str | None = None, actor=Depends(census_identity)):
    return {'tenant_id': actor['tenant_id'], **await asyncio.to_thread(_svc().metering, actor['tenant_id'], period)}


# ----------------------------------------------------------------------------- client application (key-authenticated; no estate login)
def _key(x_caas_key: str | None = Header(default=None)):
    return x_caas_key


@router.get('/client/licence')
async def client_licence(secret: str | None = Depends(_key)):
    key, lic, cl = await asyncio.to_thread(_wrap, _svc().resolve, secret)
    return {'client': {'client_id': cl['client_id'], 'name': cl['name'], 'application': cl['application']}, 'licence': {k: lic[k] for k in ('licence_id', 'status', 'terms', 'terms_identifier', 'issued_at')},
            'key': {'key_id': key['key_id'], 'issued_at': key['issued_at'], 'uses': key.get('uses', 0)}, 'products': {p: _svc().PRODUCTS[p] for p in lic['terms']['products']}}


@router.post('/client/deliver', status_code=201)
async def client_deliver(body: Deliver, secret: str | None = Depends(_key)):
    svc = _svc()
    try: return await svc.deliver(secret, body.product, body.brief)
    except svc.Refused as exc: raise HTTPException(exc.code, exc.text) from exc


@router.get('/client/deliveries')
async def client_deliveries(secret: str | None = Depends(_key)):
    return {'deliveries': await asyncio.to_thread(_wrap, _svc().client_deliveries, secret)}
