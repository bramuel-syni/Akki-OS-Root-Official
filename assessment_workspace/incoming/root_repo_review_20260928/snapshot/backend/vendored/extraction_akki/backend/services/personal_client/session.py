"""services.personal_client.session · Canon 6 · Canon 5 · session composition + ask emission.

Canon anchors (per M17.md MUST-DO 3):

- **NEXT_MILESTONES_PLAN §11 verbatim** ("personal client for
  tenant-of-one"). This module authors the session composition
  surface + the ask emission routing surface.
- **Canon 6** (User Journeys · session composition anchor) — the
  session record binds a tenant-of-one journey to its issued
  application key. `compose_session` is the identity-import
  producer of `PersonalClientSession_v0` instances.
- **Canon 5** (Interface Architecture · client surface constraint)
  — the ask emission surface `emit_ask` is the interface between
  the personal client and the sealed M14 answering-service seam.
- **Canon 8 §W11** one-task-one-identity · structural role
  separation. The module has NO decision surface (banned prefixes
  enforced by AST-scan); does NOT import any principal-data /
  user-memory surface (R-21 hard ban until owner ruling · AST-scan
  enforced); does NOT import any learned / model-client / CIF
  detection surface at execution scope (Canon 4 §22 rung-1
  discipline · AST-scan enforced).
- **R-21 (STATE/DECISIONS.md:12333 + 12366 verbatim)** hard ban:
  banned import roots across `ast.Import` + `ast.ImportFrom` walk:
  `services.memory.*` · `services.principal_data.*` ·
  `services.user_memory.*` · `services.memory_compaction.*`.
- **AC-18** (proposes-never-ratifies · session surface has no
  decision-surface function; banned function-name prefixes
  enforced at test-file level: `decide_`, `ratify_`, `admit_`,
  `accept_`, `reject_`, `approve_`, `sign_`).
- **M14-W2 sealed** — `services.mkondo.registry.admit_handoff`
  consumed at ask emission boundary by identity import (M14 seam
  role separation preserved).
- **M14-W3 sealed** — `services.answering_service.collections.asks`
  consumed at ask emission boundary for `t_<tenant_id>` per-tenant
  DB scope per M11 (M11 seam role separation preserved).
- **M11** (per-tenant DB sealed) — consumed via `t_<tenant_id>`
  discipline (`_tenant_db_name` helper mirrors sealed asks
  collection convention).
- **M17-W1 sealed** `ApplicationContract_v0` — consumed by identity
  import for `compose_session` typing (SO §3.10-α closed-schema
  discipline · `type() is` identity check at boundary).
- **M17-W2 sealed** — bearer_key_prefix parameter type-checked as
  32-char lowercase-hex string (structural coupling to M17-W2
  output shape).
- **SO §3.8** thin-kernel additive-only: this file lands NEW; no
  sealed module edited.
- **SO §3.10-α** (closed-schema discipline): type identity check
  at boundary refuses masquerade classes.

Public surface:

    compose_session(*, application_contract: ApplicationContract_v0,
                       bearer_key_prefix: str,
                       session_id: str,
                       started_at: str) -> PersonalClientSession_v0

    emit_ask(*, session: PersonalClientSession_v0,
                payload: str,
                ask_id: str,
                created_at: str) -> str

`compose_session` deterministically constructs a
`PersonalClientSession_v0` from the sealed M17-W1
`ApplicationContract_v0` (structural coupling: application_id and
tenant_id fields mirror). The bearer_key_prefix (from M17-W2
issuance) is validated for shape (32-char lowercase-hex) but not
stored on the session record — the session is scoped by the
tenant-of-one journey, not by the bearer prefix.

`emit_ask` routes through the sealed M14 seam:
1. Constructs a payload_ref (deterministic sha256 over the
   ask_id + payload tuple).
2. Instantiates the sealed M14-W3 Ask_v0 model.
3. Delegates persistence to the sealed
   `services.answering_service.collections.asks.insert_ask`
   surface under `t_<tenant_id>` DB scope per M11
   (repository passed by the caller · role-separated).
4. Returns the ask_id.

At the shape-freeze wave, `emit_ask` is bound structurally to the
M14/M11 seams via identity import + reference. Runtime wiring
requires the caller to supply the `t_<tenant_id>`-scoped
repository per M11 discipline.
"""
from __future__ import annotations

import hashlib
from typing import Any

from contracts.application_contract_v0 import ApplicationContract_v0
from contracts.personal_client_session_v0 import PersonalClientSession_v0
from services.answering_service.collections.asks import (
    Ask_v0,
    _tenant_db_name,
    insert_ask,
)
from services.mkondo.registry import admit_handoff  # noqa: F401 — identity binding


__all__ = ("compose_session", "emit_ask", "SessionCompositionRefused", "AskEmissionRefused")


class SessionCompositionRefused(Exception):
    """Fail-closed sentinel raised at `compose_session` boundary when
    the input is not an identity instance of the sealed
    `ApplicationContract_v0` model OR when the bearer_key_prefix is
    not a 32-char lowercase-hex string (SO §3.10-α)."""


class AskEmissionRefused(Exception):
    """Fail-closed sentinel raised at `emit_ask` boundary when the
    input session is not an identity instance of the sealed
    `PersonalClientSession_v0` model (SO §3.10-α)."""


def compose_session(
    *,
    application_contract: ApplicationContract_v0,
    bearer_key_prefix: str,
    session_id: str,
    started_at: str,
) -> PersonalClientSession_v0:
    """Deterministic pure-data-in session composition surface.

    Parameters
    ----------
    application_contract
        Identity instance of M17-W1 sealed
        `ApplicationContract_v0`. Type identity check at boundary
        refuses masquerade / dict / None / subclass instances.
    bearer_key_prefix
        32-char lowercase-hex string from M17-W2 sealed
        `issue_application_key`. Shape-validated (length + hex);
        NOT stored on the session record.
    session_id
        Personal-client-session identifier matching
        `^pcs_[a-z0-9_-]+$` (validated at pydantic construction).
    started_at
        ISO-8601 UTC timestamp of session start (min_length=1).

    Returns
    -------
    PersonalClientSession_v0
        Identity instance of the sealed M17-W3 contract.

    Raises
    ------
    SessionCompositionRefused
        If `application_contract` is not an identity
        `ApplicationContract_v0` instance OR if
        `bearer_key_prefix` is not a 32-char lowercase-hex
        string.
    """
    # SO §3.10-α: type identity check at boundary.
    if type(application_contract) is not ApplicationContract_v0:
        raise SessionCompositionRefused(
            "compose_session requires identity ApplicationContract_v0 "
            "instance per SO §3.10-α closed-schema discipline"
        )

    # M17-W2 output shape structural check: 32-char lowercase-hex.
    if (
        not isinstance(bearer_key_prefix, str)
        or len(bearer_key_prefix) != 32
        or not all(c in "0123456789abcdef" for c in bearer_key_prefix)
    ):
        raise SessionCompositionRefused(
            "compose_session requires bearer_key_prefix to be a "
            "32-char lowercase-hex string per M17-W2 output shape"
        )

    return PersonalClientSession_v0(
        session_id=session_id,
        application_id=application_contract.application_id,
        tenant_id=application_contract.tenant_id,
        started_at=started_at,
        ask_ids=(),
        pending_receipts=(),
    )


def emit_ask(
    *,
    session: PersonalClientSession_v0,
    payload: str,
    ask_id: str,
    created_at: str,
    repository: Any,
) -> str:
    """Ask emission surface routing through sealed M14/M11 seams.

    Parameters
    ----------
    session
        Identity instance of M17-W3 sealed
        `PersonalClientSession_v0`.
    payload
        Opaque string payload for the ask (min_length=1 at Ask_v0
        construction).
    ask_id
        Ask identifier (regex enforced at sealed Ask_v0
        construction).
    created_at
        ISO-8601 UTC timestamp of ask creation.
    repository
        `services.data.repository.Repository` instance bound to the
        `t_<tenant_id>` per-tenant DB per M11 discipline. The
        caller is responsible for constructing the repository with
        matching tenant context; the sealed M14-W3
        `_insert_via_repository` primitive refuses mismatched-tenant
        writes with AKKI-DATA-001.

    Returns
    -------
    str
        The ask_id string (echoed after successful append).

    Raises
    ------
    AskEmissionRefused
        If `session` is not an identity
        `PersonalClientSession_v0` instance.
    """
    # SO §3.10-α: type identity check at boundary.
    if type(session) is not PersonalClientSession_v0:
        raise AskEmissionRefused(
            "emit_ask requires identity PersonalClientSession_v0 "
            "instance per SO §3.10-α closed-schema discipline"
        )

    # Deterministic payload_ref derivation per B-M10-Q1 hash-binding
    # discipline (payload content not stored on ask row; only its
    # content-addressed reference).
    payload_bytes = payload.encode("utf-8")
    payload_ref = f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}"

    # M11 discipline: per-tenant DB scope check via sealed helper.
    # The sealed helper returns `t_<tenant_id>`; the tenant_id is
    # carried on the session per structural coupling to M17-W1.
    expected_db_name = _tenant_db_name(session.tenant_id.removeprefix("t_"))
    if not expected_db_name.startswith("t_"):
        # Defensive: sealed helper convention is `t_<tenant_id>`; this
        # branch structurally verifies the M11 discipline coupling
        # holds. Never reachable under sealed helper behaviour.
        raise AskEmissionRefused(
            f"emit_ask cannot route through sealed M14/M11 seam · "
            f"expected `t_<tenant_id>` DB name but got {expected_db_name!r}"
        )

    # Build sealed M14-W3 Ask_v0 instance.
    ask = Ask_v0(
        ask_id=ask_id,
        tenant_id=session.tenant_id,
        handoff_id=session.session_id,
        payload_ref=payload_ref,
        created_at=created_at,
    )

    # Delegate persistence to the sealed M14-W3 insert_ask surface.
    # Repository primitive enforces per-tenant DB scope per M11
    # (AKKI-DATA-001 · Canon 8 §W11 tenant isolation).
    insert_ask(ask, repository=repository)

    return ask_id
