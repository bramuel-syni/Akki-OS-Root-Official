"""PersonalClientSession_v0 · M17-W3 · C.23 scope · MILESTONE 8.

Canon anchors (per M17.md MUST-DO 3):

- NEXT_MILESTONES_PLAN §11 verbatim ("personal client for
  tenant-of-one"). W3 seals the session-composition surface of the
  personal client.
- Canon 6 (User Journeys · session composition anchor) — the
  session record binds a tenant-of-one journey to its issued
  application key.
- Canon 5 (Interface Architecture · client surface constraint) —
  the session shape carries only the fields the personal-client
  surface consumes; anything beyond that is a fork.
- Canon 8 §W11 one-task-one-identity · structural role separation
  preserved: the contract carries NO decision surface, NO
  persistence surface, NO signing surface at the shape level.
- AC-18 (proposes-never-ratifies · contract carries no
  ratification-adjacent field · verified at shape level test 2).
- R-21 (STATE/DECISIONS.md:12333 + 12366 verbatim
  owner-outstanding: "user-memory class, consent model: owner
  input outstanding — implement the class behind a tenant-wide
  flag, off by default, no consent model assumed, no principal
  data written until ruled") — the session record carries NO
  principal-data / user-memory-adjacent field. Verified at shape
  level test 2.
- M11 discipline — `tenant_id` regex `^t_[a-z0-9_-]+$` mirrors
  sealed W-M11-W1 per-tenant DB naming convention. Consumed by
  emit_ask at W3 for per-tenant DB scope.
- M17-W1 sealed ApplicationContract_v0 — the session's
  `application_id` field mirrors the M17-W1 contract's
  application_id regex to preserve structural coupling across the
  wave.
- SO §3.8 thin-kernel additive-only.
- SO §3.10-α closed-schema discipline · frozen pydantic +
  extra=forbid + regex on session_id · closed tuples for ask_ids
  and pending_receipts.

Shape (canon-anchored · 6 required fields):

- `session_id`           · `^pcs_[a-z0-9_-]+$` (namespace-isolated
                           from app_/cif_/hnd_/wp_/sk_/console_
                           prefixes at the identifier level).
- `application_id`       · `^app_[a-z0-9_-]+$` (mirrors M17-W1
                           ApplicationContract_v0 regex · structural
                           coupling preserved across wave).
- `tenant_id`            · `^t_[a-z0-9_-]+$` (M11 per-tenant DB
                           naming discipline · Motor writer role
                           scope · consumed by emit_ask for DB
                           routing).
- `started_at`           · ISO-8601 UTC min_length=1.
- `ask_ids`              · Tuple[str, ...] (append-only running
                           list of ask ids emitted through this
                           session; ordering-preserving; empty
                           tuple by default).
- `pending_receipts`     · Tuple[str, ...] (append-only running
                           list of ask ids awaiting receipt from
                           the answering service; ordering-preserving;
                           empty tuple by default).

Non-goals (SO §6.4 NOTHING-BEYOND applied to M17 per owner steer
2026-09-19T~12:45Z verbatim):

- NO principal-data / user-memory / memory-compaction field (R-21).
- NO decision surface field (no approved, no ratified, no
  decided_by, no admit_at). AC-18 + B-frontends-Q1.
- NO signing / signature / seal field. Signing stays under sealed
  M12b-W1 primitive at any authoring point that requires it.
- NO receipt payload storage — pending_receipts is a list of
  ask_ids only, not the receipt payloads themselves; receipt
  payloads live under M14-W3 answering-service seam.
"""
from __future__ import annotations

from typing import Tuple

from pydantic import BaseModel, ConfigDict, Field


class PersonalClientSession_v0(BaseModel):
    """C.23 canon-anchored personal-client-session shape · closed 6-field tuple.

    Represents an in-flight tenant-of-one session consuming an
    application key issued at M17-W2. The session composes asks
    through the sealed M14 answering-service seam under
    `t_<tenant_id>` per M11 discipline (enforced at emit_ask
    boundary at the W3 module level).

    AC-18 preserved: the session record itself does not decide;
    the acceptance point for asks lives under the sealed M14
    Mkondo registry admit + the sealed M14-W3 asks collection
    append. B-frontends-Q1 preserved at the shape level: no
    approve-adjacent field. R-21 preserved at the shape level: no
    principal-data field.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str = Field(
        ...,
        pattern=r"^pcs_[a-z0-9_-]+$",
        description=(
            "Namespace-isolated personal-client-session identifier · "
            "`^pcs_[a-z0-9_-]+$` (isolated from app_ / cif_ / hnd_ / "
            "wp_ / sk_ / console_ prefixes at the identifier level)."
        ),
    )
    application_id: str = Field(
        ...,
        pattern=r"^app_[a-z0-9_-]+$",
        description=(
            "Application identifier mirroring the M17-W1 sealed "
            "ApplicationContract_v0 regex · structural coupling "
            "preserved across the wave."
        ),
    )
    tenant_id: str = Field(
        ...,
        pattern=r"^t_[a-z0-9_-]+$",
        description=(
            "Per-tenant identifier · `^t_[a-z0-9_-]+$` mirroring "
            "sealed W-M11-W1 per-tenant DB naming discipline · "
            "consumed by emit_ask at W3 for `t_<tenant_id>` DB "
            "scope routing."
        ),
    )
    started_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of session start.",
    )
    ask_ids: Tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Closed tuple of ask ids emitted through this session · "
            "append-only running list · ordering-preserving · empty "
            "tuple by default."
        ),
    )
    pending_receipts: Tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Closed tuple of ask ids awaiting receipt from the "
            "answering service · append-only running list · "
            "ordering-preserving · empty tuple by default. Receipt "
            "payloads themselves live under M14-W3 answering-service "
            "seam; this field carries only the ask_ids awaiting "
            "receipt."
        ),
    )


__all__ = ["PersonalClientSession_v0"]
