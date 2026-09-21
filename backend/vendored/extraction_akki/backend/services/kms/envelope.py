"""Envelope encryption primitive · M13-W2 · §6.4 pre-ruling 4 verbatim.

**Structural role (Canon 8 §W11 one-task-one-identity):** this module
wraps a fresh data-encryption-key (DEK) under a per-tenant master key,
encrypts plaintext with the DEK, and roundtrips both back on unwrap.
It does NOT mint master keys — that responsibility belongs to
`services.kms.tenant_key_registry`. AST ban enforces the boundary at
`tests/invariants/test_m13_w2_kms_envelope_and_rotation.py::
test_ast_envelope_does_not_mint_master_key`.

**Cross-tenant refusal (Canon 8 §W11):** unwrap raises
`CrossTenantEnvelopeRefused` when the caller's tenant_id does not
match the envelope's own tenant_id.

Cipher: AES-256-GCM (authenticated encryption · standard tier-2).
"""
from __future__ import annotations

import secrets
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from services.kms.tenant_key_registry import (
    _get_key_material,
    get_active_key,
)


class CrossTenantEnvelopeRefused(Exception):
    """Raised when a caller attempts to unwrap an envelope minted for
    a different tenant. Canon 8 §W11 one-task-one-identity."""


@dataclass(frozen=True)
class Envelope:
    """A wrapped-DEK + AEAD-ciphertext envelope. Tenant-scoped by
    construction: `unwrap_and_decrypt` refuses cross-tenant access."""
    tenant_id: str
    tenant_key_id: str
    wrapped_dek_nonce: bytes
    wrapped_dek_ct: bytes
    payload_nonce: bytes
    payload_ct: bytes


def wrap_dek(tenant_id: str, plaintext: bytes) -> Envelope:
    """Wrap a fresh DEK under the tenant's active master key and
    encrypt `plaintext` under the DEK. Returns a tenant-scoped
    `Envelope`. Does NOT mint the tenant master key — expects the
    tenant to have one already (via
    services.kms.tenant_key_registry.mint_tenant_master_key)."""
    active = get_active_key(tenant_id)
    master_key = _get_key_material(active.key_id)

    # Fresh DEK per wrap (256-bit AES key).
    dek = secrets.token_bytes(32)

    # Wrap the DEK under the master key using AES-256-GCM.
    master_aead = AESGCM(master_key)
    dek_nonce = secrets.token_bytes(12)
    wrapped_dek_ct = master_aead.encrypt(
        dek_nonce, dek, associated_data=tenant_id.encode("utf-8")
    )

    # Encrypt plaintext under the DEK.
    dek_aead = AESGCM(dek)
    payload_nonce = secrets.token_bytes(12)
    payload_ct = dek_aead.encrypt(
        payload_nonce, plaintext, associated_data=tenant_id.encode("utf-8")
    )

    return Envelope(
        tenant_id=tenant_id,
        tenant_key_id=active.key_id,
        wrapped_dek_nonce=dek_nonce,
        wrapped_dek_ct=wrapped_dek_ct,
        payload_nonce=payload_nonce,
        payload_ct=payload_ct,
    )


def unwrap_and_decrypt(caller_tenant_id: str, envelope: Envelope) -> bytes:
    """Refuse if `caller_tenant_id != envelope.tenant_id`; otherwise
    unwrap the DEK under the tenant master key and decrypt the payload
    under the DEK. Returns the recovered plaintext bytes."""
    if caller_tenant_id != envelope.tenant_id:
        raise CrossTenantEnvelopeRefused(
            f"caller tenant {caller_tenant_id!r} may not unwrap envelope "
            f"minted for tenant {envelope.tenant_id!r} "
            f"(Canon 8 §W11 one-task-one-identity)"
        )

    master_key = _get_key_material(envelope.tenant_key_id)
    master_aead = AESGCM(master_key)
    dek = master_aead.decrypt(
        envelope.wrapped_dek_nonce,
        envelope.wrapped_dek_ct,
        associated_data=envelope.tenant_id.encode("utf-8"),
    )

    dek_aead = AESGCM(dek)
    plaintext = dek_aead.decrypt(
        envelope.payload_nonce,
        envelope.payload_ct,
        associated_data=envelope.tenant_id.encode("utf-8"),
    )
    return plaintext
