"""services.personal_client.handoff_binding · M17-W6 · handoff-ID adapter + ID-domain type-tagging.

Sub-wave: **CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG** ·
follow-on to M17-W5 fork banked at
`notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md`. Owner-ordered
at 2026-09-19T~17:54Z Owner Desk Batch item (f) verbatim: "Handoff-
ID adapter + ID-domain type-tagging (ho_ slot rejects non-ho_
prefixes, tests first)."

Canon anchors:

- **HR-2** (Doc-16 Handoff-Generalisation · ID-domain type-tagging
  binding · ho_ slot rejects non-ho_ prefixes).
- **`notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md`
  Option (i)** verbatim: "Additive-adapter extension — SO §3.8
  preserved. Author a new module handoff_binding.py (new file ·
  thin adapter · Canon 8 §W11 role separation preserved) that
  exposes derive_handoff_id(...) returning 'ho_' +
  session.session_id.removeprefix('pcs_'). Author a new
  emit_ask_with_handoff(...) surface that routes through the
  sealed M14/M11 seam correctly. Does NOT edit the sealed M17-W3
  session.py."
- **Canon 8 §W11** one-task-one-identity structural role
  separation: this module carries ONLY pure data-in adapter
  surfaces + refusal types; NO decision surface (AST-enforced by
  test 6).
- **Canon 5** (Interface Architecture · client surface constraint)
  — the adapter is the interface between the personal-client
  session shape (M17-W3 pcs_ regex) and the sealed M14 answering-
  service ask shape (ho_ regex).
- **Canon 4 §22** rung-1 deterministic discipline: no LLM /
  learned / randomness at any scope (AST-enforced by test 7).
- **AC-18** proposes-never-ratifies · adapter has no
  ratification-adjacent surface.
- **R-21** (STATE/DECISIONS.md:12333 + 12366 verbatim) hard ban:
  no import root matching services.memory.* /
  services.principal_data.* / services.user_memory.* /
  services.memory_compaction.* (AST-enforced by test 7).
- **M14-W3 sealed** `Ask_v0` — consumed at
  emit_ask_with_handoff boundary by identity import;
  `Ask_v0.handoff_id` field regex `^ho_[a-z0-9_-]+$` is the
  "ho_ slot" the owner directive names.
- **M14-W3 sealed** `insert_ask` — consumed at
  emit_ask_with_handoff persistence boundary (append-only writer
  discipline per Canon 3 §9.3).
- **M17-W3 sealed** `PersonalClientSession_v0` — consumed at
  derive_handoff_id boundary by identity import (SO §3.10-α
  closed-schema discipline · `type() is` identity check).
- **SO §3.8** thin-kernel additive-only: this file lands NEW.
  Sealed M17-W3 `services.personal_client.session` NOT imported
  (thin adapter discipline · avoids picking up the still-latent
  emit_ask bug through name resolution).
- **SO §3.10-α** closed-schema discipline preserved.
- **SO §6.4 NOTHING-BEYOND** applied to (f): scope frozen at
  three surfaces (`HandoffId` type-tagged class + `derive_handoff_id`
  + `emit_ask_with_handoff`).

Public surface (5 exports):

    class HandoffId(str)                    · ID-domain type-tag
    class HandoffIdRefused(Exception)       · fail-closed sentinel
    class HandoffBindingRefused(Exception)  · fail-closed sentinel
    derive_handoff_id(session) -> HandoffId
    emit_ask_with_handoff(*, session, payload, ask_id,
                          created_at, repository) -> str
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

from contracts.personal_client_session_v0 import PersonalClientSession_v0
from services.answering_service.collections.asks import (
    Ask_v0,
    _tenant_db_name,  # noqa: F401 — identity binding to sealed M11 helper
    insert_ask,
)


__all__ = (
    "HandoffId",
    "HandoffIdRefused",
    "HandoffBindingRefused",
    "derive_handoff_id",
    "emit_ask_with_handoff",
)


# ── Fail-closed sentinels ────────────────────────────────────


class HandoffIdRefused(Exception):
    """Fail-closed sentinel raised at `HandoffId` construction when
    the raw string does not match the sealed Ask_v0.handoff_id
    ho_ slot regex `^ho_[a-z0-9_-]+$` (HR-2 · Canon 15 §33 mirror).

    Owner directive verbatim (2026-09-19T~17:54Z item (f)):
    "ho_ slot rejects non-ho_ prefixes."
    """


class HandoffBindingRefused(Exception):
    """Fail-closed sentinel raised at `derive_handoff_id` boundary
    when the input session is not an identity instance of the
    sealed M17-W3 `PersonalClientSession_v0` model (SO §3.10-α
    closed-schema discipline)."""


# ── ID-domain type-tag ───────────────────────────────────────


class HandoffId(str):
    """ID-domain type-tag for handoff identifiers.

    A `HandoffId` is a `str` subclass that structurally guarantees
    at construction time (`isinstance(x, HandoffId)`) that the
    wrapped string matches the sealed `Ask_v0.handoff_id` regex
    `^ho_[a-z0-9_-]+$` — the "ho_ slot" per owner directive
    2026-09-19T~17:54Z item (f) verbatim.

    Rationale (owner directive verbatim + M17_W5_HANDOFF_ID_MISMATCH_FORK
    Option (i)):

        "Handoff-ID adapter + ID-domain type-tagging (ho_ slot
         rejects non-ho_ prefixes, tests first)."

    Runtime distinguishability: `HandoffId` inherits from `str`
    (NOT a `typing.NewType` alias which is erased at runtime),
    so `isinstance(x, HandoffId)` gates callers structurally.
    Any function that requires an already-validated handoff ID
    can type-annotate its parameter as `HandoffId` and refuse
    non-`HandoffId` inputs at boundary (Canon 8 §W11 one-task-
    one-identity: validation is the ONE task this class owns).

    Refusal grammar: `HandoffIdRefused` sentinel with sentence
    naming the failure kind (regex-mismatch / non-string / empty-
    suffix) — Doc-2 §A5.2 honest-refusal discipline.

    SO §3.10-α: closed regex boundary (no ambient-authority
    string coercion). SO §3.8: additive-only (new class · sealed
    Ask_v0.handoff_id pydantic regex NOT edited · still enforces
    at pydantic construction as before · this class strengthens
    the caller-side guarantee for API surfaces that consume
    handoff IDs).
    """

    __slots__ = ()
    _REGEX = re.compile(r"^ho_[a-z0-9_-]+$")

    def __new__(cls, raw: object) -> "HandoffId":
        if not isinstance(raw, str):
            raise HandoffIdRefused(
                f"HandoffId requires str input (HR-2 · ho_ slot); "
                f"got {type(raw).__name__!r}"
            )
        if cls._REGEX.match(raw) is None:
            raise HandoffIdRefused(
                f"HandoffId must match ^ho_[a-z0-9_-]+$ (ho_ slot per "
                f"owner directive 2026-09-19T~17:54Z item (f) verbatim); "
                f"got {raw!r}"
            )
        return str.__new__(cls, raw)


# ── Adapter surfaces ─────────────────────────────────────────


def derive_handoff_id(session: PersonalClientSession_v0) -> HandoffId:
    """Deterministic pure-data-in adapter mapping session ID → handoff ID.

    Mapping rule (owner directive + fork Option (i) verbatim):

        `ho_<suffix>`  ←  `pcs_<suffix>`

    where `<suffix>` is the portion of `session.session_id` after
    stripping the sealed `PersonalClientSession_v0.session_id`
    regex prefix `pcs_`.

    Parameters
    ----------
    session
        Identity instance of the sealed M17-W3
        `PersonalClientSession_v0` model. Type identity check at
        boundary refuses masquerade / dict / None / subclass
        instances (SO §3.10-α).

    Returns
    -------
    HandoffId
        Type-tagged string guaranteed to match the sealed
        `Ask_v0.handoff_id` regex. Callers can pass this directly
        to `Ask_v0(handoff_id=...)` without further validation.

    Raises
    ------
    HandoffBindingRefused
        If `session` is not an identity
        `PersonalClientSession_v0` instance.
    HandoffIdRefused
        If (impossible under sealed session shape) the derived
        string somehow fails the ho_ slot regex — defensive
        re-check inside HandoffId construction, propagates the
        HandoffIdRefused from the type-tag boundary.
    """
    if type(session) is not PersonalClientSession_v0:
        raise HandoffBindingRefused(
            "derive_handoff_id requires identity PersonalClientSession_v0 "
            "instance per SO §3.10-α closed-schema discipline; "
            f"got {type(session).__name__!r}"
        )
    suffix = session.session_id.removeprefix("pcs_")
    return HandoffId(f"ho_{suffix}")


def emit_ask_with_handoff(
    *,
    session: PersonalClientSession_v0,
    payload: str,
    ask_id: str,
    created_at: str,
    repository: Any,
) -> str:
    """Ask emission via handoff-ID adapter · fork-closure seam route.

    Follow-on to `services.personal_client.session.emit_ask` (sealed
    M17-W3 · latent bug per M17_W5_HANDOFF_ID_MISMATCH_FORK doc:
    the sealed emit_ask passes `session.session_id` [pcs_ regex]
    directly to `Ask_v0.handoff_id` [ho_ regex] triggering a
    ValidationError on every valid session). This surface routes
    the same emission path with the adapter interposed:

    1. `derive_handoff_id(session)` → validated `HandoffId`.
    2. Construct sealed `Ask_v0` with `handoff_id=str(HandoffId)`
       (ho_ slot regex now passes).
    3. Delegate persistence to sealed
       `services.answering_service.collections.asks.insert_ask`
       under caller-supplied per-tenant `Repository` (M11
       discipline · AKKI-DATA-001 tenant-isolation refusal
       remains sealed at the repository primitive).
    4. Return the ask_id string (echoed after successful append).

    Parameters
    ----------
    session
        Identity instance of M17-W3 sealed
        `PersonalClientSession_v0`. Type identity check enforced
        via `derive_handoff_id` (raises `HandoffBindingRefused` on
        masquerade).
    payload
        Opaque string payload for the ask (min_length=1 at Ask_v0
        construction).
    ask_id
        Ask identifier (regex `^ask_[a-z0-9_-]+$` enforced at
        sealed Ask_v0 construction).
    created_at
        ISO-8601 UTC timestamp of ask creation.
    repository
        `services.data.repository.Repository` instance bound to
        the `t_<tenant_id>` per-tenant DB per M11 discipline.
        Sealed M14-W3 `_insert_via_repository` primitive refuses
        mismatched-tenant writes with AKKI-DATA-001.

    Returns
    -------
    str
        The ask_id string (echoed after successful append).

    Raises
    ------
    HandoffBindingRefused
        If `session` is not identity `PersonalClientSession_v0`.
    HandoffIdRefused
        Defensive (unreachable under sealed session shape).
    pydantic.ValidationError
        If Ask_v0 construction fails for reasons other than
        handoff_id (e.g., malformed ask_id, empty payload_ref).
    """
    # Adapter step: derive validated handoff ID via type-tag boundary.
    handoff_id = derive_handoff_id(session)

    # Deterministic payload_ref derivation per B-M10-Q1 hash-binding
    # discipline (mirrors sealed session.emit_ask payload_ref
    # construction · payload content NOT stored on ask row; only
    # its content-addressed reference).
    payload_bytes = payload.encode("utf-8")
    payload_ref = f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}"

    # Build sealed M14-W3 Ask_v0 instance with adapter-validated
    # handoff_id (ho_ slot regex passes by HandoffId construction
    # guarantee).
    ask = Ask_v0(
        ask_id=ask_id,
        tenant_id=session.tenant_id,
        handoff_id=str(handoff_id),
        payload_ref=payload_ref,
        created_at=created_at,
    )

    # Delegate persistence to the sealed M14-W3 insert_ask surface.
    # Repository primitive enforces per-tenant DB scope per M11
    # (AKKI-DATA-001 · Canon 8 §W11 tenant isolation).
    insert_ask(ask, repository=repository)

    return ask_id
