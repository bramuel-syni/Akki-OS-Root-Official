"""A18.5 · Server-side scope resolver · client-scope-widening refusal gate.

Doc 18 §A18.5 verbatim (Wave B grounding brief · Canon-of-Record):
    'A18.5  [CANON] Scope is enforced server-side, not by client
     discipline. Access rides the engineer key-grant records. A
     consuming application's own good behaviour is never the control —
     scope is checked at the gate on every call, so a compromised or
     careless client can narrow what it asks for but cannot widen what
     it's able to get.'

Doc 18 §18.6 paired canon:
    'Revocation is enforced at the gate, not at the client — a revoked
     key produces a refusal even if a consumer never checks its own
     state.' (Revocation-at-gate is a follow-on lifecycle; this slice
     lands the shape of server-side scope resolution.)

Secondary carrier anchors (disk-verifiable · pinned OVER · not modified):
  * `backend/services/auth/engineer_key_grant.py` — Phase 8 Stage B-3
    E4 engineer key-grant registration record. A18.5 verbatim:
    "Access rides the engineer key-grant records." The resolver reads
    the `key_grant_id` field from the provisioning record (A18.1) and
    resolves scope entirely server-side.
  * `backend/services/skill_provisioning_persistence.py` — Sealed A18.2
    write-once persistence (Slice 2). The resolver uses
    `get_by_skill_id` as its only lookup path.
  * `backend/contracts/skill_provisioning_record_v0.py` — Sealed A18.1
    frozen tuple (Slice 1). The `scope` field of that record is the
    ONLY source of truth for a call's effective scope.

Refusal envelope semantics (this slice):
  * `ClientSuppliedScopeRefused` — raised BEFORE any lookup when the
    caller passes a non-None `client_supplied_scope` kwarg. The refusal
    is structural, not value-based: the presence of the kwarg means
    the client tried to influence scope, and that is forbidden by
    A18.5 verbatim ("the client is never the control"). Even a
    client_supplied_scope that matches the record byte-for-byte is
    refused — the pattern is prevented, not just the outcome.
  * `SkillNotProvisioned` — raised when the skill_id is not present
    in the sealed A18.2 write-once persistence. No default scope, no
    empty-string fallback: an unknown skill is a refusal.

Runtime wiring into the sealed inner-gate per-call carrier is
DEFERRED to a later slice per SO §6.4 NOTHING-BEYOND. At this slice
the resolver is a structural drift-detector pin: any future runtime
that resolves scope for a skill call MUST consume the sealed A18.1
record verbatim, never a client-supplied value.
"""
from __future__ import annotations

from typing import Optional

from services import skill_provisioning_persistence


class ClientSuppliedScopeRefused(RuntimeError):
    """Attempted call with a client-supplied scope override.

    A18.5 verbatim: "A consuming application's own good behaviour is
    never the control." Any non-None `client_supplied_scope` kwarg is
    a structural refusal at the gate — the value is never inspected,
    the presence alone is the refusal.
    """


class SkillNotProvisioned(RuntimeError):
    """Attempted scope resolution for a skill_id not in the sealed
    A18.2 write-once persistence.

    A18.2 read alongside A18.5: no scope is derivable without a
    frozen provisioning record. There is no default scope.
    """


def resolve_scope_for_call(
    skill_id: str,
    *,
    client_supplied_scope: Optional[str] = None,
) -> str:
    """Return the server-side scope for a per-call gate check.

    A18.5-conformant behaviour:
      1. If `client_supplied_scope is not None`: raise
         `ClientSuppliedScopeRefused` immediately, BEFORE any lookup.
         The kwarg's presence is the refusal — its value is never
         inspected.
      2. Look up the sealed A18.1 provisioning record via the sealed
         A18.2 `get_by_skill_id` public callable.
      3. If no record: raise `SkillNotProvisioned` — no default, no
         fallback.
      4. Return the record's `scope` field byte-verbatim (no transform,
         no widening, no narrowing).

    The client narrows what it asks for at the application layer
    (upstream of this call). It cannot widen what it is able to get:
    that is guaranteed by (1) refusing any client_supplied_scope, and
    (4) returning the record's scope field verbatim.
    """
    if client_supplied_scope is not None:
        raise ClientSuppliedScopeRefused(
            f"client_supplied_scope was passed for skill_id "
            f"{skill_id!r} · Doc 18 §A18.5 verbatim: 'A consuming "
            f"application's own good behaviour is never the control' "
            f"· client_supplied_scope kwarg presence is a structural "
            f"refusal, value is never inspected"
        )
    record = skill_provisioning_persistence.get_by_skill_id(skill_id)
    if record is None:
        raise SkillNotProvisioned(
            f"skill_id {skill_id!r} has no A18.2 write-once provisioning "
            f"record · Doc 18 §A18.5 read alongside §A18.2: no scope is "
            f"derivable without a frozen provisioning record"
        )
    return record.scope
