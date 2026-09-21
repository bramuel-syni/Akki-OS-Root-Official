"""ApplicationContract_v0 · M17-W1 · C.23 scope · MILESTONE 8.

Owner Standing Order §6.2 verbatim (banked in STATE/STANDING_ORDERS.md
· batch-ratification-at-preceding-seal authority for M13–M17 draft
cards):

    "e1_dev drafts cards for M13–M17, memory layer, and frontends
     from canon and the SER, for batch ratification at the next seal
     boundary."

Owner steer verbatim (this-session · 2026-09-19T~12:45Z · banked in
notes/M17_OBJECTIVE_CARD_DRAFT_20260919.md preamble):

    "5-10 MUST-DO lines stands. Anchor priority: span BOTH surfaces
     of M17 — (a) the tenant-facing/journey surface (Canon 6
     journeys, Canon 5 interface) AND (b) the governance constraints
     that must hold in any client surface: approval blocks rather
     than warns, silence never approves, the chat proposes and never
     decides ... If the personal client's canon anchor requires any
     principal/user-memory data handling, remember R-21 is still
     owner-outstanding: tenant-wide flag off, no consent model
     assumed, no principal data written until ruled — put that in
     MUST-NOT with the ruling cite."

Structural placement:
- C.23 (Tenant Apps · Application-contract enforcement + personal
  client for tenant-of-one) at L3-shape-freeze level in the
  Extraction-Akki backend per NEXT_MILESTONES_PLAN_20260917.md §11
  verbatim.
- Reference application on the Integration-Console-issued-key model
  per STATE/AUTONOMOUS_RUN_PLAN.md §11 (Canon 7 §28).

Shape (canon-anchored · 7 required fields · closed 2-tuple Literal
on `receipt_policy` binding the two receipt dispositions):

- `application_id`      · `^app_[a-z0-9_-]+$` (namespace-isolated
                          from CIF `cif_` and handoff `hnd_` and
                          whitepaper `wp_` and skill `sk_` prefixes).
- `tenant_id`           · `^t_[a-z0-9_-]+$` mirroring sealed W-M11-W1
                          per-tenant DB naming discipline
                          (t_<tenant_id> Motor writer role scope · a
                          structural coupling that prevents
                          downstream ask persistence at W3 landing
                          under a non-matching database name).
- `issued_at`           · ISO-8601 UTC timestamp of application
                          registration authoring.
- `issuer_console_id`   · `^console_[a-z0-9_-]+$` identifying the
                          Integration Console instance that issued
                          the application registration (Canon 7 §28
                          Integration-Console-issued-key model).
- `capability_manifest` · Tuple[str, ...] of L-5 capability register
                          category names the application declares
                          (binds to sealed W1b·CP4 capability
                          register · A20.16).
- `receipt_policy`      · Literal["required","forbidden"]:
                          closed 2-tuple binding the two valid
                          receipt dispositions at contract shape
                          level (SO §3.10-α closed-schema).
- `citations`           · closed tuple of str evidence-cite strings
                          backing the application registration
                          (canon anchors, ruling refs, etc.).

Same-commit DoD:
  * `ConfigDict(extra="forbid", frozen=True)` — shape drift
    protection + immutability post-construction (AC-18 preserved:
    every application registration is intent-in-record only; the
    decision surface for key issuance lives at W2, and even that is
    a mechanical consequence of a valid contract, not an independent
    decision).
  * The shape-snapshot sha256 is pinned in
    `tests/invariants/test_m17_w1_application_contract_shape_freeze.py`
    and breaks on any refactor until a ceremony re-pins it.

Non-goals (SO §6.4 "NOTHING beyond" clause applied to M17 · owner
steer 2026-09-19T~12:45Z verbatim: "if the card needs something
canon doesn't anchor, that is a fork · bank it · don't improvise
it"):

  * NO ratification-adjacent field (no `ratified_at`, no
    `decided_by`, no `accepted`, no `admitted`, no `approved`,
    no `approval_status`). AC-18 + B-frontends-Q1 preserved at
    shape level.
  * NO principal-data / user-memory field. R-21 is owner-outstanding
    per STATE/DECISIONS.md:12333 + 12366 verbatim ("R-21
    (user-memory class, consent model): owner input outstanding —
    implement the class behind a tenant-wide flag, off by default,
    no consent model assumed, no principal data written until
    ruled"); no principal-data-adjacent field is allowed at M17
    shape level.
  * NO write / signing / persistence surface in this module. Those
    concerns live at W2 (issuance) + W3 (personal-client session
    composition) + M14 seam (ask emission).
  * NO reference to CIF / Targeta / DET-1 / Memory / Frontends
    surfaces. Those are separate milestones.

Canon anchors:
- NEXT_MILESTONES_PLAN §11 verbatim (C.23 goal) + AUTONOMOUS_RUN_PLAN
  §11 (Canon 7 §28 issuance model) + Canon 5 (Interface Architecture
  · client-consumable contract shape) + Canon 6 (User Journeys ·
  application_id + tenant_id binding a journey) + AC-18
  (proposes-never-ratifies · contract carries no ratification field)
  + STATE/DECISIONS.md:12333 + 12366 (R-21 verbatim · no
  principal-data field) + STATE/DECISIONS.md:12115 (B-frontends-Q1
  verbatim · no approve-adjacent field) + M11 seal (`t_<tenant_id>`
  regex discipline) + services/capability_registry.py sealed W1b·CP4
  (L-5 A20.16 category-name anchor for `capability_manifest`) + SO
  §3.8 (thin-kernel additive-only) + SO §3.10-α (closed-schema
  discipline) + SO §6.7 batch-ratification-at-preceding-seal.
"""
from __future__ import annotations

from typing import Literal, Tuple

from pydantic import BaseModel, ConfigDict, Field


APPLICATION_RECEIPT_POLICIES: Tuple[str, str] = ("required", "forbidden")


class ApplicationContract_v0(BaseModel):
    """C.23 canon-anchored application-contract shape · closed 7-field tuple.

    Every application registering under the M17 Integration Console
    issued-key model (Canon 7 §28) declares one of these records.
    The record itself does not act: it carries intent-in-record only
    at authoring time.  The deterministic key-issuance surface
    (authored at W2) is the single surface that acts on a valid
    contract; the personal-client session surface (authored at W3)
    composes a session that consumes the issued bearer-key prefix
    and routes asks through the sealed M14 answering-service seam
    under per-tenant DB scope per M11.  AC-18 + B-frontends-Q1 are
    preserved at the shape level: no ratification-adjacent field
    and no approve-adjacent field exists.  R-21 is preserved at the
    shape level: no principal-data / user-memory-adjacent field
    exists (owner input outstanding per STATE/DECISIONS.md:12333 +
    12366 verbatim).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    application_id: str = Field(
        ...,
        pattern=r"^app_[a-z0-9_-]+$",
        description=(
            "Namespace-isolated application identifier · "
            "`^app_[a-z0-9_-]+$` (isolated from CIF `cif_` and "
            "handoff `hnd_` and whitepaper `wp_` and skill `sk_` "
            "prefixes at the identifier level)."
        ),
    )
    tenant_id: str = Field(
        ...,
        pattern=r"^t_[a-z0-9_-]+$",
        description=(
            "Per-tenant identifier · `^t_[a-z0-9_-]+$` mirroring "
            "sealed W-M11-W1 per-tenant DB naming discipline "
            "(t_<tenant_id> Motor writer role scope · structural "
            "coupling to the M11 seal that prevents downstream ask "
            "persistence at W3 landing under a non-matching database "
            "name)."
        ),
    )
    issued_at: str = Field(
        ...,
        min_length=1,
        description=(
            "ISO-8601 UTC timestamp of application registration "
            "authoring."
        ),
    )
    issuer_console_id: str = Field(
        ...,
        pattern=r"^console_[a-z0-9_-]+$",
        description=(
            "Namespace-isolated Integration Console instance "
            "identifier that issued the application registration · "
            "`^console_[a-z0-9_-]+$` per Canon 7 §28 "
            "Integration-Console-issued-key model (per "
            "STATE/AUTONOMOUS_RUN_PLAN.md §11 verbatim)."
        ),
    )
    capability_manifest: Tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Closed tuple of L-5 capability register category names "
            "the application declares (binds to sealed W1b·CP4 "
            "services/capability_registry.py · A20.16 · consumed at "
            "W2 as the pre-issuance capability declaration; consumed "
            "at W3 as the session-composition capability scope; the "
            "tuple's shape is opaque data · type-checked but not "
            "categorically validated at contract level · downstream "
            "validation against the sealed L-5 register happens at "
            "W2 issuance boundary)."
        ),
    )
    receipt_policy: Literal["required", "forbidden"] = Field(
        ...,
        description=(
            "SO §3.10-α closed-schema binding · closed 2-tuple "
            "Literal · `required` mandates receipts on all session "
            "asks per C.17 answering-service seam · `forbidden` "
            "excludes receipts entirely (used in probe / test / "
            "synthetic-application contexts)."
        ),
    )
    citations: Tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Closed tuple of evidence-cite strings backing the "
            "application registration (canon anchors, ruling refs, "
            "etc.)."
        ),
    )


__all__ = ["ApplicationContract_v0", "APPLICATION_RECEIPT_POLICIES"]
