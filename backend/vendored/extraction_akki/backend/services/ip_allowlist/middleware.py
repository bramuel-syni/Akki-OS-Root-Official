"""services/ip_allowlist/middleware.py — source-IP allowlist gate.

Owner stop-order 2026-08-14: token-gate retired. The spine-served surface is
reachable ONLY from IPs in SPINE_ALLOWED_IPS. Refusal is a single plain
sentence, HTTP 403, text/plain.

W10 interleave (2026-08-26): owner-access path added without weakening
governance:
  - OWNER_ALLOWLIST_IPS · comma-separated additional IPs layered on
    SPINE_ALLOWED_IPS. Admits are attributed by layer in the log.
  - ALLOWLIST_MODE=strict|permissive · 'permissive' admits all inbound
    (preview demo access) · default 'strict' preserves fail-closed.
  - Every decision logged via `ip_allowlist_decision` INFO-level log
    line naming (decision, mode, layer, client_ip). Nothing silent.

Trust boundary (empirically discovered 2026-08-14 · phase0/drill_receipts/
20260814T145200Z_header_topology_probe.md):
  Preview topology is Cloudflare Worker + Cloudflare edge + Google Cloud LB.
  X-Forwarded-For header shape received by the app:
      [client-spoofable..., true-client-IP, CF-edge-IP, GCP-LB-IP]
  Cloudflare Worker deterministically injects the true client IP; the two
  entries to its right are our own infra. SPINE_TRUSTED_PROXY_HOPS defaults
  to 2 → trusted position = xff.split(',')[-3].

Fail-closed everywhere in strict mode:
  - Missing / empty SPINE_ALLOWED_IPS + OWNER_ALLOWLIST_IPS → refuse.
  - XFF absent → refuse.
  - XFF chain shorter than SPINE_TRUSTED_PROXY_HOPS + 1 → refuse.
  - Trusted-position IP not in composed allowlist → refuse.

Permissive mode (owner demo access) admits everything and logs the mode
explicitly for audit; the strict-mode behaviour is preserved verbatim
when ALLOWLIST_MODE is unset or any value other than 'permissive'.
"""
from __future__ import annotations

import logging
import os
from typing import Set

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp


REFUSAL_SENTENCE = "This surface answers allowlisted addresses only."

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def read_allowlist_from_env() -> Set[str]:
    """Parse SPINE_ALLOWED_IPS into a set of bare-IP strings.

    Whitespace-tolerant; empty entries dropped.
    """
    raw = os.environ.get("SPINE_ALLOWED_IPS", "")
    return {p.strip() for p in raw.split(",") if p.strip()}


def read_owner_allowlist_from_env() -> Set[str]:
    """Parse OWNER_ALLOWLIST_IPS (W10 interleave) into a set of bare-IP
    strings. Layered on top of SPINE_ALLOWED_IPS; admits attributed to
    'owner' layer in the log."""
    raw = os.environ.get("OWNER_ALLOWLIST_IPS", "")
    return {p.strip() for p in raw.split(",") if p.strip()}


def read_mode_from_env() -> str:
    """Parse ALLOWLIST_MODE (W10 interleave) · normalizes case+whitespace.
    Returns 'strict' (default · fail-closed) or 'permissive' (admits all).
    Any unknown value defaults to strict (fail-closed on config typo)."""
    raw = os.environ.get("ALLOWLIST_MODE", "").strip().lower()
    if raw == "permissive":
        return "permissive"
    return "strict"


def _trusted_proxy_hops() -> int:
    try:
        return int(os.environ.get("SPINE_TRUSTED_PROXY_HOPS", "2"))
    except (TypeError, ValueError):
        return 2


def _extract_trusted_client_ip(xff: str, hops: int) -> str | None:
    """Return the trusted true-client-IP or None if topology invariant fails."""
    if not xff:
        return None
    parts = [p.strip() for p in xff.split(",") if p.strip()]
    # Need at least hops+1 entries: hops trusted proxies + 1 client entry.
    if len(parts) < hops + 1:
        return None
    return parts[-(hops + 1)]


def _log_decision(*, decision: str, mode: str, layer: str,
                  client_ip: str | None, path: str) -> None:
    """Emit a single structured INFO-level log line naming the decision.
    Nothing silent — every request produces exactly one decision log."""
    _LOGGER.info(
        "ip_allowlist_decision decision=%s mode=%s layer=%s "
        "client_ip=%s path=%s",
        decision, mode, layer, client_ip or "<none>", path,
    )


class IPAllowlistMiddleware(BaseHTTPMiddleware):
    """Refuse any request whose true-client-IP is not in the composed
    allowlist (SPINE_ALLOWED_IPS ∪ OWNER_ALLOWLIST_IPS) when
    ALLOWLIST_MODE=strict (default).

    ALLOWLIST_MODE=permissive admits every inbound (owner demo access).
    Runs BEFORE route matching, covers every path family."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        spine = read_allowlist_from_env()
        owner = read_owner_allowlist_from_env()
        mode = read_mode_from_env()
        hops = _trusted_proxy_hops()
        client_ip = _extract_trusted_client_ip(
            request.headers.get("x-forwarded-for", ""), hops
        )
        path = request.url.path

        # Permissive mode: admit everything · log the mode so audits
        # can distinguish permissive admits from strict admits.
        if mode == "permissive":
            _log_decision(
                decision="admit", mode="permissive", layer="permissive",
                client_ip=client_ip, path=path,
            )
            return await call_next(request)

        # Strict mode: fail-closed against composed allowlist.
        composed = spine | owner
        if not composed or client_ip is None:
            _log_decision(
                decision="refuse", mode="strict", layer="none",
                client_ip=client_ip, path=path,
            )
            return PlainTextResponse(REFUSAL_SENTENCE, status_code=403)

        # Attribute admit to the layer that permitted it (owner layer
        # first because owner rulings dominate spine config in audit).
        if client_ip in owner:
            _log_decision(
                decision="admit", mode="strict", layer="owner",
                client_ip=client_ip, path=path,
            )
            return await call_next(request)
        if client_ip in spine:
            _log_decision(
                decision="admit", mode="strict", layer="spine",
                client_ip=client_ip, path=path,
            )
            return await call_next(request)

        _log_decision(
            decision="refuse", mode="strict", layer="none",
            client_ip=client_ip, path=path,
        )
        return PlainTextResponse(REFUSAL_SENTENCE, status_code=403)
