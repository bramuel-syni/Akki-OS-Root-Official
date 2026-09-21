"""services/gateway/x_akki_context_middleware.py · M11-W2 · FastAPI middleware factory.

Canon anchor:
  v1.0 B.1 δ-1 · every service dependency verifies X-Akki-Context on
  every request.  This middleware factory binds the verifier from
  `context_signer.verify_header` to a Starlette/FastAPI ASGI app.

Fail-closed on missing / expired / wrong-key headers via
XAkkiContextRefusalError -> HTTP 401 with `AKKI-AUTH-003` in body.
"""
from __future__ import annotations

import os
from typing import Any, Callable, Optional

from services.gateway.context_signer import (
    AKKI_AUTH_003,
    SignedContext,
    XAkkiContextRefusalError,
    verify_header,
)


HEADER_NAME = "X-Akki-Context"
ENV_KEY_VAR = "AKKI_CONTEXT_HMAC_KEY"


def load_key_from_env(env: Optional[dict] = None) -> bytes:
    """Load the HMAC key from environment.  Fail-closed on missing."""
    src = env if env is not None else os.environ
    raw = src.get(ENV_KEY_VAR)
    if not raw:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: {ENV_KEY_VAR} not configured "
            f"(counts mismatch: 1)"
        )
    if isinstance(raw, str):
        raw = raw.encode()
    if len(raw) < 16:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: {ENV_KEY_VAR} length insufficient "
            f"(counts mismatch: 1)"
        )
    return raw


def make_middleware(
    key_loader: Callable[[], bytes] = load_key_from_env,
) -> Callable[..., Any]:
    """Return an ASGI middleware factory that verifies X-Akki-Context.

    Usage:
        app.add_middleware(BaseHTTPMiddleware, dispatch=make_middleware())
    """

    async def dispatch(request, call_next):
        try:
            key = key_loader()
            header = request.headers.get(HEADER_NAME)
            ctx = verify_header(header, key)
            # Bind verified context onto request.state for downstream deps
            request.state.akki_signed_context = ctx
        except XAkkiContextRefusalError as e:
            # Import locally so this module has zero FastAPI/Starlette
            # import cost at unit-test time.
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={"refusal_code": AKKI_AUTH_003, "message": str(e)},
            )
        return await call_next(request)

    return dispatch
