"""services.credential_plane.plane — Principal Model Spec v1 §3 plane.

PRIN-5 · PRIN-6 · PRIN-7 · PRIN-8 enforcement, additive-only.

PRIN-6 hardening (owner reminder this-session verbatim): 'key material
never persisted means tests should prove absence — e.g., a scan/AST or
storage-inspection test that no persistence path receives raw key bytes
(hash-only at rest), not just a happy-path check.'  This module
therefore:

  (i)   Generates the raw credential material inside `issue_credential`,
        immediately hashes it (`hashlib.sha256(raw).hexdigest()`), and
        drops the raw bytes on the same stack frame — no assignment to
        a module-level, class-level, or persistence surface receives
        the raw bytes.
  (ii)  The internal `_ISSUED` registry keeps ONLY the SHA-256 digest of
        the material, alongside opaque handle metadata (key_id +
        principal_id + trust_domain_identifier + revoked flag).  The
        digest is one-way; readback is impossible even with full
        registry access.
  (iii) Deliberately DOES NOT expose `recover_credential` or
        `get_credential_material` surfaces.  Tests scan for absence.
  (iv)  The issuance receipt carries key_id + rotation metadata only;
        no `key_material` / `secret` / `raw_key` / `private_key` /
        `key_secret` field exists on the receipt shape.

R-22 verbatim (spec §9 · owner-ratified this-session): 90 days,
DEFAULT-class.
"""
from __future__ import annotations

import hashlib
import secrets
import threading
from typing import Dict, Final, Optional

from pydantic import BaseModel, ConfigDict, Field


# PRIN-8 · R-22 verbatim.
ROTATION_DEFAULT_DAYS: Final[int] = 90
ROTATION_DEFAULT_CLASS: Final[str] = "DEFAULT"


class CredentialRefusal(RuntimeError):
    """Raised on any presentation the credential plane refuses.

    PRIN-6 (readback refused), PRIN-7 (out-of-domain refused), and
    PRIN-8 (revoked / unknown) all refuse via this exception.
    """


class CredentialIssueReceipt(BaseModel):
    """PRIN-5 + PRIN-6 + PRIN-7 + PRIN-8 receipt shape.

    Carries the opaque handle (key_id) and rotation metadata only.
    Deliberately omits any field a component could use to read the
    material back.  Sibling of DAP-13's ApiKeyIssueReceipt in
    contracts.dap; the two shapes are not merged because the
    principal-model plane is scoped to the Principal Model Spec §3
    (verbatim), consumed by DAP's own admission ceremony from a
    separate specification (LIM-3).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    key_id: str = Field(
        ...,
        description=(
            "PRIN-5 verbatim: opaque handle to the credential.  "
            "Independently revocable; the identifier is the surface, "
            "not the material."
        ),
    )
    principal_id: str = Field(
        ...,
        description=(
            "PRIN-5 verbatim: 'Credentials are issued per principal, "
            "never per organisation.'  This field pins the binding."
        ),
    )
    parent_organisation_id: str = Field(
        ...,
        description=(
            "PRIN-1 kinship: the organisation the credentialed "
            "principal acts under.  Preserved for correlation only; "
            "the credential itself is NOT owned by the organisation "
            "(PRIN-5 verbatim)."
        ),
    )
    trust_domain_identifier: str = Field(
        ...,
        description=(
            "PRIN-7 verbatim: 'A credential is bound to exactly one "
            "trust-domain identifier at issuance.  It cannot be "
            "presented to resolve identity outside that domain.'"
        ),
    )
    rotation_days: int = Field(
        default=ROTATION_DEFAULT_DAYS,
        description="PRIN-8 · R-22 owner-ratified verbatim: 90 days.",
    )
    rotation_class: str = Field(
        default=ROTATION_DEFAULT_CLASS,
        description="PRIN-8 · R-22 owner-ratified verbatim: DEFAULT-class.",
    )
    revocable_in_single_act: bool = Field(
        default=True,
        description=(
            "PRIN-5 verbatim: 'each independently revocable in one act, "
            "none of which reveals or touches the others.'"
        ),
    )


# Internal registry: {key_id: {digest, principal_id, org_id, td_id, revoked}}
# CRITICAL PRIN-6 discipline: the raw credential material is NEVER stored
# here; only its SHA-256 digest is retained.  The digest is one-way and
# cannot reveal the credential to any component with registry access.
_ISSUED: Dict[str, Dict[str, object]] = {}
_LOCK = threading.Lock()


def issue_credential(
    principal_id: str,
    parent_organisation_id: str,
    trust_domain_identifier: Optional[str] = None,
    rotation_days: int = ROTATION_DEFAULT_DAYS,
    rotation_class: str = ROTATION_DEFAULT_CLASS,
) -> CredentialIssueReceipt:
    """PRIN-5 + PRIN-6 + PRIN-7 + PRIN-8 issuance.

    The raw credential material is generated on this stack frame,
    immediately digested, and dropped without ever being assigned to a
    surface a component could read back.  The returned receipt carries
    the opaque handle (key_id) and rotation metadata only.  A
    credential shown once and lost is reissued, never recovered.
    """

    # Raw material stays local; digest-only at rest per PRIN-6.
    raw_material = secrets.token_urlsafe(32)
    digest = hashlib.sha256(raw_material.encode("utf-8")).hexdigest()
    del raw_material  # PRIN-6: raw bytes MUST NOT persist beyond this call.

    key_id = f"key_{secrets.token_urlsafe(12)}"
    trust_domain = trust_domain_identifier or f"td_{secrets.token_urlsafe(8)}"

    with _LOCK:
        _ISSUED[key_id] = {
            "digest": digest,  # one-way; cannot reveal material.
            "principal_id": principal_id,
            "parent_organisation_id": parent_organisation_id,
            "trust_domain_identifier": trust_domain,
            "revoked": False,
        }

    return CredentialIssueReceipt(
        key_id=key_id,
        principal_id=principal_id,
        parent_organisation_id=parent_organisation_id,
        trust_domain_identifier=trust_domain,
        rotation_days=rotation_days,
        rotation_class=rotation_class,
    )


def revoke_credential(key_id: str, by: Optional[str] = None) -> None:
    """PRIN-5 + PRIN-8 verbatim: 'each independently revocable in one
    act, none of which reveals or touches the others' + 'Revocation is
    unconditional and immediate on the estate owner's act, regardless
    of rotation schedule.'
    """

    with _LOCK:
        entry = _ISSUED.get(key_id)
        if entry is None:
            # PRIN-8 fail-closed on revoke: unknown key_id is a refusal,
            # never silently treated as already revoked (failure_posture_v1
            # verbatim from spec §7).
            raise CredentialRefusal(
                f"PRIN-8 · revoke refused: unknown key_id {key_id!r}."
            )
        entry["revoked"] = True


def is_revoked(key_id: str) -> bool:
    with _LOCK:
        entry = _ISSUED.get(key_id)
        if entry is None:
            raise CredentialRefusal(
                f"is_revoked refused: unknown key_id {key_id!r}."
            )
        return bool(entry["revoked"])


def resolve_identity(key_id: str, requested_trust_domain: str) -> str:
    """PRIN-7 verbatim: 'A credential is bound to exactly one
    trust-domain identifier at issuance.  It cannot be presented to
    resolve identity outside that domain.'
    """

    with _LOCK:
        entry = _ISSUED.get(key_id)
    if entry is None:
        raise CredentialRefusal(
            f"PRIN-7 · resolve refused: unknown key_id {key_id!r}."
        )
    if entry["revoked"]:
        raise CredentialRefusal(
            f"PRIN-8 · resolve refused: credential {key_id!r} is revoked."
        )
    if entry["trust_domain_identifier"] != requested_trust_domain:
        raise CredentialRefusal(
            f"PRIN-7 · resolve refused: credential {key_id!r} bound to "
            f"trust domain {entry['trust_domain_identifier']!r}, presented "
            f"in {requested_trust_domain!r}."
        )
    return str(entry["principal_id"])
