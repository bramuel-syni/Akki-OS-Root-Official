"""Existing JWT/account gate composition; no new authentication authority."""
from contextlib import asynccontextmanager
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from services.enforce.census_identity import census_identity
from services.enforce.principal_context_adapter import principal_context
from services.census_autonomy.operational_scope import SOURCE_TENANTS


@asynccontextmanager
async def portal_scope(request, *, write=False):
    try:
        scope = await census_identity(request)
        if write and not {"operator", "master_admin"}.intersection(scope["roles"]):
            raise HTTPException(403, "An admitted operator is required to commission or change work.")
        with principal_context(scope["principal_id"]):
            yield scope
    except (PyMongoError, ValueError, RuntimeError) as exc:
        raise HTTPException(503, "The authoritative record could not be verified. Retry with the same request key.") from exc


def validate_units(body, scope):
    if any(SOURCE_TENANTS.get(unit) != scope["tenant_id"] for unit in body.units):
        raise HTTPException(403, "One or more source references are not admitted to this tenant.")