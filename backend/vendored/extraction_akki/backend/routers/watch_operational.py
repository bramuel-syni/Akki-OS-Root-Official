"""Ordinary tenant-bound Watch reader; no public authority-minting endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from services.enforce.census_identity import census_identity
from services.watch.operational_reads import state_for

router = APIRouter(tags=['tenant-scoped-watch'])


class WatchEnvelope(BaseModel):
    model_config = ConfigDict(extra='allow')
    tenant_id: str


@router.get('/api/portal/watch/state', response_model=WatchEnvelope)
@router.get('/api/watch/state', response_model=WatchEnvelope)
@router.get('/api/grey_mirror/state', response_model=WatchEnvelope)
def state(actor=Depends(census_identity)):
    if not {'operator', 'master_admin'}.intersection(actor['roles']):
        raise HTTPException(403, 'Estate operator access is required for Watch records.')
    return state_for(actor)


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