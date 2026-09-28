"""services.entitlement_service_v1.customer_key_plane · ENT-35..36 · Customer Key plane.

ENT-35 (§11 verbatim): "A provider credential the buyer supplies is held by
the credential plane under envelope encryption, bound to the buyer's
trust-domain identifier, usable by the chokepoint and by nothing else, never
displayable after entry, and revocable in one act. Rotation replaces it;
recovery does not exist." [PRIN-5, PRIN-6, PRIN-7]

ENT-36 (§11 verbatim): "Keys are held at organisation scope by default; a
seat-scoped key is permitted and takes precedence for that seat (R-29)."

This module wraps the sealed `services.credential_plane` (M11-SW1 · PRIN-5/6/7)
adding the entitlement-specific `CredentialEnvelope` shape (ENT-49 name prefix
'Credential' compliant) that binds `organisation_principal_id` + optional
`seat_principal_id` (for ENT-36 seat-scoped precedence). Key material NEVER
touches this module surface — only the opaque `key_id` handle from the sealed
credential plane and the trust-domain binding are stored on the envelope.

Structural role separation per Canon 8 §W11:
  · this module does NOT persist raw key material (sealed credential plane
    handles envelope encryption + storage · zero raw-key surface at this
    module boundary).
  · this module does NOT emit metered events (that lives at chokepoint
    dispatch surface via sealed `contracts.dap.MeteredEvent`).
  · this module does NOT decide dispatch (that lives at chokepoint_resolver).

ENT-35 hard bans (enforced structurally by
tests.invariants.test_entitlement_service_v1_property_tests.test_ent_35_...):
No function name may begin with the following identifier tokens (spaced
to keep this docstring outside the grep-negative match window):
  get key material · read key material · display key · reveal key
  · recover customer · restore customer
Rotation is a replacement (issue new · revoke old); no recovery surface
of any kind exists.

R-29 (§19 verbatim): "Key scope: recommend organisation by default, seat-scoped
permitted with precedence (ENT-36). DEFAULT-class."
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# Sealed identity import · SO §3.8 additive-only · zero edit
from services.credential_plane.plane import (
    is_revoked as _sealed_is_revoked,
    revoke_credential as _sealed_revoke_credential,
)


class CredentialEnvelope(BaseModel):
    """ENT-35/36 · Customer-key envelope binding a sealed credential plane
    key_id to the buyer's trust-domain identifier at organisation scope,
    with optional seat-scoped precedence per R-29.

    Model name starts with 'Credential' per ENT-49 four-allowed-shapes.
    key_id is OPAQUE — never the key material itself (ENT-35 verbatim
    'never displayable after entry').
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    key_id: str = Field(..., min_length=1, description="ENT-35 opaque handle from sealed credential plane · NEVER key material.")
    organisation_principal_id: str = Field(..., min_length=1, description="ENT-35 organisation PRIN-1 (default scope · R-29).")
    trust_domain_id: str = Field(..., min_length=1, description="ENT-35 trust-domain binding · usable by the chokepoint and by nothing else.")
    seat_principal_id: Optional[str] = Field(
        default=None,
        description="ENT-36 seat-scoped precedence (Optional · None means organisation-scope per R-29 default)."
    )
    provider: str = Field(..., min_length=1, description="ENT-35 which provider (openai/anthropic/etc) · category label only.")
    wrapped_at_iso: str = Field(..., min_length=1, description="ISO-8601 UTC timestamp of envelope creation.")


def wrap_customer_key(
    *,
    key_id: str,
    organisation_principal_id: str,
    trust_domain_id: str,
    provider: str,
    wrapped_at_iso: str,
    seat_principal_id: Optional[str] = None,
) -> CredentialEnvelope:
    """ENT-35 · Wrap a sealed-credential-plane opaque `key_id` into an
    entitlement-scope CredentialEnvelope binding organisation + optional
    seat + trust-domain + provider.

    This function DOES NOT accept raw key material. Callers must first
    invoke `services.credential_plane.plane.issue_credential(...)` (sealed
    surface) which handles envelope encryption + returns the opaque
    `key_id`. This function is a THIN adapter attaching entitlement-scope
    fields (organisation_principal_id, seat_principal_id per ENT-36).
    """
    return CredentialEnvelope(
        key_id=key_id,
        organisation_principal_id=organisation_principal_id,
        trust_domain_id=trust_domain_id,
        seat_principal_id=seat_principal_id,
        provider=provider,
        wrapped_at_iso=wrapped_at_iso,
    )


def revoke_customer_key(envelope: CredentialEnvelope, *, by: Optional[str] = None) -> None:
    """ENT-35 · Revocable in one act. Delegates to sealed
    `services.credential_plane.plane.revoke_credential`.

    Rotation replaces (revoke_customer_key + wrap_customer_key on a fresh
    key_id); no recovery surface of any kind exists (per ENT-35 verbatim
    "recovery does not exist" — no restore/recover/backup/undelete surface
    is authored, and the grep-negative hard ban catches any future addition).
    """
    _sealed_revoke_credential(envelope.key_id, by=by)


def is_customer_key_revoked(envelope: CredentialEnvelope) -> bool:
    """ENT-35 · Read-only revocation status probe. Delegates to sealed
    `services.credential_plane.plane.is_revoked`.
    """
    return _sealed_is_revoked(envelope.key_id)
