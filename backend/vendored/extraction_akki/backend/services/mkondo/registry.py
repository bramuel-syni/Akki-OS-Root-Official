"""services.mkondo.registry · Mkondo hand-off registry runtime.

MILESTONE 5 · M14-W2 · new module authored at CP-M14-W2-MKONDO-REGISTRY.

Canon anchors:
- **Canon 15 §33** verbatim: HandoffContract carries four required fields:
  `what · shape · identity · receipt`. Every cross-app crossing of governed
  work MUST be expressed in a `HandoffContract_v0` before it ships. Mkondo
  registry is the admission gate: shape drift is refused at construction
  (via pydantic ValidationError propagation).
- **CA1-009** verbatim: every cross-app crossing is authored + persisted
  through `services.handoff.register_handoff` (sealed pre-M14). Mkondo
  registry composes on top of that persistence layer.
- **Canon 8 §W11** (one-task-one-identity): dual-hatted contracts where
  `identity_source.actor_id == identity_destination.actor_id` are refused
  with `MkondoRoleSeparationRefused`. This is a STRUCTURAL role
  separation: the actor who authors a hand-off cannot also be the
  receiver of the same hand-off. Signing is a separate role held by the
  Watch signature primitive at M14-W4; Mkondo does NOT sign.
- **Canon 1 §62** (single-writer ledger): every admitted hand-off emits
  exactly one ledger intent via `services.ledger_emitter.emit_intent`
  (the sole intent-writer surface). Registry does NOT touch mongo
  directly; it hands its intent to the emitter.
- **SO §3.8** (thin-kernel additive-only): this module is a new pure
  runtime surface. It consumes sealed pre-M14 surfaces without editing
  them.
- **SO §3.10-α** (closed-schema discipline): the registry admits only
  a valid `HandoffContract_v0` payload; extra fields are refused at
  construction; the shape is closed at M14-W1.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from contracts.handoff_contract import HandoffContract_v0
from contracts.ledger_v1 import LedgerRowAt
from services.handoff.contracts import register_handoff
from services.ledger_emitter.emit_intent import LedgerIntent, emit_intent


class MkondoRoleSeparationRefused(ValueError):
    """Refusal shape for dual-hatted hand-offs · Canon 8 §W11
    one-task-one-identity. The registry raises this class when
    identity_source.actor_id == identity_destination.actor_id."""


def admit_handoff(payload: Dict[str, Any]) -> HandoffContract_v0:
    """Admit a HandoffContract_v0 through the Mkondo registry.

    Order of operations:
    1. Construct the pydantic model (shape drift → pydantic ValidationError).
    2. Refuse dual-hatted contracts (Canon 8 §W11).
    3. Persist via the sealed `services.handoff.register_handoff` surface
       (CA1-009 · duplicate handoff_id → ValueError from that surface).
    4. Emit exactly one ledger intent via `services.ledger_emitter.emit_intent`
       (Canon 1 §62 single-writer).
    5. Return the frozen contract.
    """
    # Step 1 · shape validation at construction (pydantic ValidationError
    # propagates unwrapped per SO §3.8: no swallow / no wrap).
    contract = HandoffContract_v0(**payload)

    # Step 2 · structural role separation (Canon 8 §W11).
    if contract.identity_source.actor_id == contract.identity_destination.actor_id:
        raise MkondoRoleSeparationRefused(
            f"M14-W2 · dual-hatted handoff refused · "
            f"identity_source.actor_id == identity_destination.actor_id == "
            f"{contract.identity_source.actor_id!r} · Canon 8 §W11 "
            "one-task-one-identity · the actor authoring a hand-off cannot "
            "also be the receiver of the same hand-off."
        )

    # Step 3 · persist through the sealed pre-M14 surface (CA1-009).
    register_handoff(payload)

    # Step 4 · emit ledger intent (Canon 1 §62 single-writer).
    intent = LedgerIntent(
        tenant_id="mkondo",
        run_id=contract.handoff_id,
        task_id=contract.handoff_id,
        actor_id=contract.identity_source.actor_id,
        actor_type="mkondo_registry",
        event_type="mkondo.handoff.admitted",
        resource_type="handoff_contract_v0",
        resource_id=contract.handoff_id,
        decision="admitted",
        reason_code="mkondo_admit_ok",
        payload_ref=f"handoff_contract:{contract.handoff_id}",
        at=LedgerRowAt(
            epoch_s=int(datetime.now(timezone.utc).timestamp()),
            source="wall_clock",
        ),
    )
    emit_intent(intent=intent)

    return contract
