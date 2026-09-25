"""Approved identity-to-tenant composition; no email inference or role escalation."""
from bson import ObjectId
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from core import db
from services.auth.dependencies import require_identity_or_deny
from services.census_autonomy.operational_scope import tenant_from_account


async def census_identity(request: Request):
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        raise HTTPException(401, "Sign in to view your estate's census.")
    if not ObjectId.is_valid(result.user_id):
        raise HTTPException(403, "Admitted account membership is required.")
    account = await db.users.find_one({"_id": ObjectId(result.user_id)},
                                      {"_id": 0, "tenant_id": 1, "roles": 1})
    try:
        tenant = tenant_from_account(account or {})
    except ValueError as exc:
        raise HTTPException(403, str(exc)) from exc
    return {"principal_id": result.user_id, "tenant_id": tenant, "roles": (account or {}).get("roles", [])}