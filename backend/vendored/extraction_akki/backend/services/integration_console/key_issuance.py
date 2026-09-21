"""services.integration_console.key_issuance · Canon 7 §28 · deterministic pure-data-in.

Canon anchors verbatim (per M17.md MUST-DO 2):

- **Canon 7 §28** (Integration-Console-issued-key model · consumed
  by STATE/AUTONOMOUS_RUN_PLAN.md §11 verbatim: "Reference
  application on the Integration-Console-issued-key model (Canon 7
  §28)"). This module is the deterministic issuance surface.
- **Canon 8 §W11** one-task-one-identity · structural role
  separation. This module MUST NOT reach into persistence
  (persistence stays at M11 tenant DBs consumed by W3 for session
  composition), MUST NOT compose sessions (composition stays at
  W3), MUST NOT sign session tokens (signing stays under sealed
  M12b-W1 primitive at any authoring point that requires it, not
  at issuance).  All three role separations are AST-enforced at
  the M17-W2 invariant test level.
- **Canon 5** (Interface Architecture · issuance boundary
  constraint) — the returned `(application_id,
  opaque_bearer_key_prefix)` tuple IS the interface between the
  platform and the tenant application; it is deterministic
  pure-data-in per **M14-W4 owner tier-1 ruling** precedent 2026-09-19
  verbatim ("a code path is a code path · no live signing at
  issuance boundary").
- **M12b-W1** (Ed25519 primitive sealed) — referenced by identity
  only; NOT imported at any scope.  Signing / verification stays
  under the sealed primitive at any authoring point that requires
  it, which is not this module.
- **M14 answering service seam sealed** — NOT imported at issuance;
  consumed at W3 by identity import for session ask routing.
- **M11 per-tenant DB sealed** — NOT imported at issuance;
  consumed at W3 via `t_<tenant_id>` discipline.
- **M17-W1 sealed** `ApplicationContract_v0` (frozen pydantic ·
  closed 7-field tuple · sha256 baseline
  `ba1957dfbb38ba037ec6a57c52760f053e829451ccf6ee9c12b48ef4498b8d05`)
  consumed by identity import per SO §3.10-α closed-schema
  discipline.  Type identity check (`type(...) is
  ApplicationContract_v0`) at the boundary, not `isinstance`, not
  shadow, not subclass.
- **SO §3.8** thin-kernel additive-only: this file lands NEW; no
  sealed module edited.
- **SO §3.10-α** (closed-schema discipline): boundary refusal on
  non-`ApplicationContract_v0` inputs via `type() is` identity
  check.
- **SO §6.4** NOTHING-BEYOND clause applied to M17 (owner steer
  2026-09-19T~12:45Z verbatim: "if the card needs something canon
  doesn't anchor, that is a fork · bank it · don't improvise it"):
  ONLY the deterministic prefix derivation surface exists here.

Public surface:

    issue_application_key(*, application_contract: ApplicationContract_v0)
        -> Tuple[str, str]

Returns a tuple `(application_id, opaque_bearer_key_prefix)`
where:

- `application_id` echoes the contract field verbatim.
- `opaque_bearer_key_prefix` is a 32-char lowercase-hex sha256[:32]
  string derived from the canonical sorted-key JSON of the tuple
  `(application_id, tenant_id, issued_at, issuer_console_id)`.

The derivation is pure-data-in per **M14-W4** owner tier-1 ruling
precedent: no randomness source, no wall-clock read, no
environment read, no persistence, no signing.  Repeated calls
with the same `ApplicationContract_v0` return the same prefix
(deterministic).  Contracts differing in any of the four
canonical-tuple fields yield distinct prefixes.

Fail-closed: `application_contract` MUST be an identity instance
of the sealed `contracts.application_contract_v0.ApplicationContract_v0`
class (SO §3.10-α `type() is` discipline).  Any masquerade class /
dict / None / subclass instance raises `IssuanceRefused`.

Downstream wiring (W3 · W4 · W5):

- W3 personal-client session composition consumes the returned
  `opaque_bearer_key_prefix` at the session boundary to identify
  the issued application.
- W4 governance-in-client invariants are structural predicates
  over the personal-client surface authored at W3; the issuance
  module is not touched at W4.
- W5 milestone integration seal binds W1..W4 end-to-end and
  verifies R-21 no-principal-data write via dependency-closure
  walk.
"""
from __future__ import annotations

import hashlib
import json
from typing import Tuple

from contracts.application_contract_v0 import ApplicationContract_v0


__all__ = ("issue_application_key", "IssuanceRefused")


class IssuanceRefused(Exception):
    """Fail-closed sentinel raised at the issuance boundary when the
    input is not an identity instance of the sealed
    `ApplicationContract_v0` model (SO §3.10-α)."""


def issue_application_key(
    *,
    application_contract: ApplicationContract_v0,
) -> Tuple[str, str]:
    """Deterministic pure-data-in application-key issuance surface.

    Parameters
    ----------
    application_contract
        Identity instance of `contracts.application_contract_v0.ApplicationContract_v0`.
        Any non-identity input (masquerade class, dict, None,
        subclass instance) is refused via `IssuanceRefused` per SO
        §3.10-α closed-schema discipline.

    Returns
    -------
    Tuple[str, str]
        `(application_id, opaque_bearer_key_prefix)` where the
        prefix is a 32-char lowercase-hex sha256[:32] over the
        canonical sorted-key JSON of the tuple
        `(application_id, tenant_id, issued_at, issuer_console_id)`.

    Raises
    ------
    IssuanceRefused
        If `application_contract` is not an identity
        `ApplicationContract_v0` instance.
    """
    # SO §3.10-α: type identity check at boundary (not isinstance,
    # not subclass, not shadow).  M12b-W1 sealed primitive not
    # touched.  M14/M11 seams not touched.  Canon 8 §W11 role
    # separation preserved.
    if type(application_contract) is not ApplicationContract_v0:
        raise IssuanceRefused(
            "issue_application_key requires identity ApplicationContract_v0 "
            "instance per SO §3.10-α closed-schema discipline"
        )

    # Canonical tuple over the four fields that define the issuance
    # identity: application_id + tenant_id + issued_at +
    # issuer_console_id.  capability_manifest + receipt_policy +
    # citations are NOT part of the canonical prefix (they are
    # declaration payload; the prefix binds issuance identity).
    canonical_payload = {
        "application_id": application_contract.application_id,
        "issued_at": application_contract.issued_at,
        "issuer_console_id": application_contract.issuer_console_id,
        "tenant_id": application_contract.tenant_id,
    }
    encoded = json.dumps(canonical_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    opaque_bearer_key_prefix = digest[:32]

    return (application_contract.application_id, opaque_bearer_key_prefix)
