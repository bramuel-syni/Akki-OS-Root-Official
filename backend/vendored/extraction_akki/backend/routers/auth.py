"""Phase 8 Stage B-1 — auth router.

Endpoints (all under `/api/auth`):
  * `POST /api/auth/register` — open registration; new users default to
    `ask_console_user` role with no key_grants. Returns access + refresh
    tokens.
  * `POST /api/auth/login` — email + password; returns access + refresh.
  * `POST /api/auth/refresh` — refresh token → new access token.
  * `GET /api/auth/me` — authenticated introspection; returns Identity
    (without password_hash).

Owner E1 ratification: JWT single-source, standard-library-only (PyJWT +
bcrypt). Federation-forward: OAuth adapters later mint the same JWT
claim shape.

Owner E2 ratification: auth failures emit `{reason, detail}` with the
4-code bounded set. NO `outcome` key. NO `outcome=refused`. NO
AdmissionRefusal_v0 discriminator.
"""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

from services.auth import auth_refusal, user_store
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.auth.jwt_service import (
    TokenExpired,
    TokenInvalid,
    create_access_token,
    create_refresh_token,
    decode_token,
    extract_bearer_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    identity: Identity


def _issue_token_pair(identity: Identity) -> TokenPair:
    """Mint an access + refresh token pair for an identity."""
    access = create_access_token(
        user_id=identity.user_id,
        email=identity.email,
        roles=list(identity.roles),
        key_grants=[g.model_dump() for g in identity.key_grants],
    )
    refresh = create_refresh_token(user_id=identity.user_id)
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        identity=identity,
    )


@router.post("/register", response_model=TokenPair, status_code=201)
async def register(body: RegisterRequest):
    """Open registration. Default role: `ask_console_user`."""
    try:
        identity = await user_store.create_user(
            email=str(body.email),
            password_plaintext=body.password,
            name=body.name,
        )
    except ValueError as e:
        # Email already exists — 409 conflict with plain shape.
        if str(e).startswith("email_already_registered"):
            return JSONResponse(
                status_code=409,
                content={
                    "reason": "email_already_registered",
                    "detail": "An account with this email already exists.",
                },
            )
        raise
    return _issue_token_pair(identity)


@router.post("/login", response_model=TokenPair)
async def login(body: LoginRequest):
    """Verify credentials + issue tokens. Wrong-password → 401 auth_missing."""
    identity = await user_store.authenticate(str(body.email), body.password)
    if identity is None:
        await _observe_authentication(str(body.email), None)
        return auth_refusal.emit(
            "auth_missing",
            detail="Invalid credentials.",
        )
    await _observe_authentication(str(body.email), identity)
    return _issue_token_pair(identity)


async def _observe_authentication(email, identity):
    """M2 authentication boundary: a sign-in attempt against an admitted tenant account is a crossing the Watch sees
    under that account's own identity (refused on a wrong password, admitted on success). Observation only — the
    gate never blocks sign-in; detections act on the subject's commissioning, reads stay unaffected. Unknown
    e-mails have no admitted identity to observe and are not recorded."""
    import hashlib
    import time
    from services.census_autonomy.operational_scope import CANONICAL_TENANT_IDS
    from services.watch import commission_gate
    try:
        doc = await user_store.get_by_email(email)
        if not doc or doc.get("tenant_id") not in CANONICAL_TENANT_IDS:
            return
        actor = {"tenant_id": doc["tenant_id"], "principal_id": str(doc["_id"]), "roles": doc.get("roles", [])}
        # refusals share one digest (the detectors count them); each admitted sign-in is its own event, not a repeat.
        digest = hashlib.sha256((f"login:{doc['_id']}" + (f":{time.time_ns()}" if identity else "")).encode()).hexdigest()
        commission_gate.observe(actor, "auth.login", "admitted" if identity else "refused", 200 if identity else 401, digest)
    except Exception:  # the record, not the sign-in, is what fails here; it is logged, never fatal to authentication
        logging.getLogger(__name__).exception("auth boundary observation failed")


@router.post("/refresh", response_model=TokenPair)
async def refresh(request: Request):
    """Exchange a refresh token for a new access token pair.

    Refresh reads the token from `Authorization: Bearer <refresh_token>`.
    On success, returns a fresh (access, refresh) pair. On failure
    (expired / invalid / access-token-as-refresh) → 401.
    """
    token = extract_bearer_token(request.headers.get("Authorization"))
    if token is None:
        return auth_refusal.emit("auth_missing")
    try:
        claims = decode_token(token, expected_type="refresh")
    except TokenExpired:
        return auth_refusal.emit("auth_expired")
    except TokenInvalid:
        return auth_refusal.emit("auth_missing")
    user_doc = await user_store.get_by_id(claims["sub"])
    if user_doc is None:
        return auth_refusal.emit("auth_missing", detail="User not found.")
    # Single-source-of-truth (2026-07-31): derive active key_grants from
    # `engineer_key_grants` collection at refresh time so revoked grants
    # DO NOT survive a token refresh. EE-R4 no-parallel-mechanism.
    identity = await user_store.resolve_identity(user_doc)
    return _issue_token_pair(identity)


@router.get("/me", response_model=Identity)
async def me(request: Request):
    """Return the authenticated caller's Identity (verbatim from JWT claims).

    Never surfaces password_hash (JWT never carried it).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    # `result` is Identity.
    return result
