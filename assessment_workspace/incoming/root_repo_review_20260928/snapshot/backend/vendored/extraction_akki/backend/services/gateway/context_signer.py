"""services/gateway/context_signer.py · M11-W2 · HMAC-SHA256 X-Akki-Context signer.

Canon anchors (verbatim):
  v1.0 B.1 δ-1 · "Gateway-signed X-Akki-Context header (HMAC-SHA256)
  closes the M9 shape-only tenant_context.py primitive."
  v0.2 §3.1 + §4.3 · "The API gateway resolves tenant_id from the
  authenticated session and injects it into every request. Clients
  cannot supply it."

Header wire format:
  X-Akki-Context: v1.<b64url(payload_json)>.<b64url(hmac_sha256_sig)>

Payload:
  {"tenant_id": str, "principal_id": str, "request_id": str,
   "issued_at_epoch_s": int, "ttl_seconds": int}

Signature:
  hmac.new(key, message=canonical_bytes(payload), digestmod=sha256).digest()

where canonical_bytes(payload) = json.dumps(payload, sort_keys=True,
separators=(",",":")).encode() — deterministic UTF-8 JSON.

Refusal code: AKKI-AUTH-003 (COUNTS-only messages · no identifier leaks).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Optional


# --- Refusal code -----------------------------------------------------------

AKKI_AUTH_003 = "AKKI-AUTH-003"


# --- Refusal-class hierarchy (M9 preventive-charter shape) ---------------

class XAkkiContextRefusalError(Exception):
    """AKKI-AUTH-003 · X-Akki-Context header refused."""
    code: str = AKKI_AUTH_003


# --- Frozen carrier ---------------------------------------------------------

@dataclass(frozen=True)
class SignedContext:
    """Gateway-signed request context.

    Fields are OPEN str per SO §3.10 Option α · except epoch-int fields.
    """
    tenant_id: str
    principal_id: str
    request_id: str
    issued_at_epoch_s: int
    ttl_seconds: int


# --- Version marker · closed enum as tuple[str, ...] · SO §3.10 α --------

SUPPORTED_VERSIONS: tuple[str, ...] = ("v1",)


def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(s + pad)


def _canonical_payload_bytes(ctx: SignedContext) -> bytes:
    payload = {
        "tenant_id": ctx.tenant_id,
        "principal_id": ctx.principal_id,
        "request_id": ctx.request_id,
        "issued_at_epoch_s": ctx.issued_at_epoch_s,
        "ttl_seconds": ctx.ttl_seconds,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def sign_context(ctx: SignedContext, key: bytes) -> str:
    """Sign a SignedContext with the shared HMAC key and return the wire
    header value in `v1.<b64url(payload)>.<b64url(sig)>` format."""
    if not isinstance(key, (bytes, bytearray)) or len(key) < 16:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: signing-key length insufficient "
            f"(counts mismatch: 1)"
        )
    payload_bytes = _canonical_payload_bytes(ctx)
    sig = hmac.new(bytes(key), payload_bytes, hashlib.sha256).digest()
    return "v1." + _b64url_encode(payload_bytes) + "." + _b64url_encode(sig)


def verify_header(
    header_value: Optional[str], key: bytes, *, now_epoch_s: Optional[int] = None
) -> SignedContext:
    """Verify a wire header value and return the SignedContext.

    Raises XAkkiContextRefusalError (code AKKI-AUTH-003) on:
      * missing / empty header
      * malformed structure
      * unsupported version marker
      * signature mismatch (wrong key OR tampered payload)
      * expired (issued_at + ttl < now)
    """
    if not header_value:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context header missing "
            f"(counts mismatch: 1)"
        )
    if not isinstance(header_value, str):
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context header not a string "
            f"(counts mismatch: 1)"
        )
    parts = header_value.split(".")
    if len(parts) != 3:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context header malformed "
            f"(counts mismatch: 1)"
        )
    version, payload_b64, sig_b64 = parts
    if version not in SUPPORTED_VERSIONS:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context version unsupported "
            f"(counts mismatch: 1)"
        )
    # Decode payload
    try:
        payload_bytes = _b64url_decode(payload_b64)
        sig_bytes = _b64url_decode(sig_b64)
        payload = json.loads(payload_bytes)
    except Exception:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context header undecodable "
            f"(counts mismatch: 1)"
        )
    # Reconstruct SignedContext (fail-closed on missing keys)
    try:
        ctx = SignedContext(
            tenant_id=str(payload["tenant_id"]),
            principal_id=str(payload["principal_id"]),
            request_id=str(payload["request_id"]),
            issued_at_epoch_s=int(payload["issued_at_epoch_s"]),
            ttl_seconds=int(payload["ttl_seconds"]),
        )
    except (KeyError, TypeError, ValueError):
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context payload missing fields "
            f"(counts mismatch: 1)"
        )
    # Verify signature (constant-time)
    expected_sig = hmac.new(
        bytes(key), _canonical_payload_bytes(ctx), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(expected_sig, sig_bytes):
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context signature invalid "
            f"(counts mismatch: 1)"
        )
    # Verify TTL
    now = int(now_epoch_s if now_epoch_s is not None else time.time())
    if ctx.issued_at_epoch_s + ctx.ttl_seconds < now:
        raise XAkkiContextRefusalError(
            f"{AKKI_AUTH_003}: X-Akki-Context expired "
            f"(counts mismatch: 1)"
        )
    return ctx
