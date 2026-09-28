"""Existing JWT/account gate composition; no new authentication authority."""
from contextlib import asynccontextmanager
import logging
import traceback
from pathlib import Path
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from services.enforce.census_identity import census_identity
from services.enforce.principal_context_adapter import principal_context
from services.enforce.control_scope import bind_authenticated_request_scope
from services.ledger_writer.principal_control import CommandConflict
from services.census_autonomy.operational_scope import SOURCE_TENANTS


@asynccontextmanager
async def portal_scope(request, *, write=False):
    phase = 'identity'
    try:
        scope = await census_identity(request)
        if write and not {"operator", "master_admin"}.intersection(scope["roles"]):
            raise HTTPException(403, "An admitted operator is required to commission or change work.")
        with principal_context(scope["principal_id"]):
            phase = 'binding'
            with bind_authenticated_request_scope(scope):
                phase = 'operation'
                yield scope
    except CommandConflict as exc:
        raise HTTPException(409, "This request key already belongs to a different frozen command.") from exc
    except (PyMongoError, ValueError, RuntimeError) as exc:
        frames = traceback.extract_tb(exc.__traceback__)
        locations = ';'.join(f'{Path(f.filename).name}:{f.name}:{f.lineno}' for f in frames)
        logging.getLogger(__name__).error('PORTAL_RECORD_UNAVAILABLE phase=%s type=%s code_path=%s',
            phase, type(exc).__name__, locations)
        raise HTTPException(503, "The authoritative record could not be verified. Retry with the same request key.") from exc


def validate_units(body, scope):
    if any(SOURCE_TENANTS.get(unit) != scope["tenant_id"] for unit in body.units):
        raise HTTPException(403, "One or more source references are not admitted to this tenant.")