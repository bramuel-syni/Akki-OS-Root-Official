"""services.credential_plane — CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9.

Credential plane implementing PRIN-5..PRIN-8 (spec §3):
    PRIN-5  Credentials per principal, never per organisation; each
            independently revocable in one act.
    PRIN-6  Credential material never persisted in a form any component
            can read back; the plane issues and can revoke, cannot
            recover or display.
    PRIN-7  A credential is bound to exactly one trust-domain identifier
            at issuance and cannot resolve identity outside that domain.
    PRIN-8  Rotation default 90 days DEFAULT-class (R-22 · owner-ratified
            2026-09-20 verbatim); revocation unconditional and immediate.

R-22 verbatim (spec §9 · owner-ratified this-session): 'Credential
rotation default (PRIN-8): 90 days, DEFAULT-class · consistent with the
existing API-key convention.'

Additive-only per SO §3.8. Sealed contracts.dap.ApiKeyIssueReceipt is
consumed via identity import (not edited); the DAP-13 opaque-handle
discipline is honoured verbatim.
"""
from __future__ import annotations

from services.credential_plane.plane import (
    ROTATION_DEFAULT_CLASS,
    ROTATION_DEFAULT_DAYS,
    CredentialIssueReceipt,
    CredentialRefusal,
    is_revoked,
    issue_credential,
    resolve_identity,
    revoke_credential,
)

__all__ = (
    "ROTATION_DEFAULT_CLASS",
    "ROTATION_DEFAULT_DAYS",
    "CredentialIssueReceipt",
    "CredentialRefusal",
    "is_revoked",
    "issue_credential",
    "resolve_identity",
    "revoke_credential",
)
