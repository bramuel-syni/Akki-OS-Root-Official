"""spine_auth.py — owner-token auth for the pod-served spine surface.

Owner ruling 2026-08-14 (WS-BUILD-CONNECT-GPU): the surface must be
reachable by the owner in a browser BEHIND an app-level auth gate. This
is an APP login, not a console/VM credential — standing policy on
external-console credentials is not touched.

Design:
  - On startup, if /app/backend/.owner_credentials does not exist, generate a
    32-hex-char owner access token, write it to that file (mode 0600), and
    log a one-time notice (only prefix, never the full token) so the pod
    operator can hand it to the owner.
  - Bearer-token auth: Authorization: Bearer <token>.
  - Rate limit: per-IP sliding window of 30 req / 60 s on /api/connect/*.
  - No cookies → no CSRF class.
  - Never log the token. Never return it in an API response. The file is the
    single artifact; the pod operator reads it and hands it over.
"""
from __future__ import annotations

import logging
import os
import secrets
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Optional

from fastapi import Header, HTTPException, Request

CRED_PATH = Path(__file__).parent / ".owner_credentials"
LOG = logging.getLogger(__name__)

_rl_events: dict[str, deque] = defaultdict(lambda: deque(maxlen=64))
_WINDOW_SEC = 60
_MAX_REQ = 30


def ensure_owner_token() -> str:
    """Read the owner token from disk; generate if not present. Never returned to callers."""
    if CRED_PATH.exists():
        return CRED_PATH.read_text().strip()
    token = secrets.token_hex(32)
    CRED_PATH.write_text(token + "\n")
    try:
        os.chmod(CRED_PATH, 0o600)
    except OSError:
        pass
    LOG.warning("owner-token: generated new .owner_credentials (mode 0600); prefix=%s...", token[:8])
    return token


def owner_token() -> str:
    """Return the owner token from disk. Callers must not log this value."""
    return ensure_owner_token()


async def require_owner(
    request: Request,
    authorization: Optional[str] = Header(None),
) -> str:
    """FastAPI dependency: verify bearer token + rate-limit per IP.

    Returns the actor identity string on success. Raises 401/403/429 otherwise.
    """
    client_ip = _client_ip(request)
    _rate_limit_or_raise(client_ip)

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="owner bearer token required")
    provided = authorization[len("Bearer ") :].strip()
    expected = owner_token()
    if not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=403, detail="owner bearer token rejected")

    request.state.actor = "owner"
    return "owner"


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limit_or_raise(ip: str) -> None:
    now = time.monotonic()
    events = _rl_events[ip]
    while events and (now - events[0]) > _WINDOW_SEC:
        events.popleft()
    if len(events) >= _MAX_REQ:
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    events.append(now)
