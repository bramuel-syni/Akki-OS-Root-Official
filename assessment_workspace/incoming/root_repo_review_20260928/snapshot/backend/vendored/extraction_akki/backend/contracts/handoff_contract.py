"""HandoffContract_v0 · CA1-009 · Doc 15 Promise #32.

Every cross-app crossing of governed work MUST be expressed in this
contract BEFORE it ships. Same discipline as Doc 1 single-chokepoint
rule: any new hand-off must go through this contract; any handoff
attempted without a HandoffContract_v0 on record is a defect.

Four required fields per Doc 15 §33 verbatim:
  * what      · the governed artefact being handed off
  * shape     · the shape/schema the receiver commits to accept
  * identity  · the actors on each side (source + destination)
  * receipt   · how the hand-off is confirmed on record

Freeze contract: 40th frozen contract post-W8 CP2. Snapshot bijection
enforced (count 39 → 40 per W6-ratified DoD).

Historical anchor: today's built estate has ONE handoff instance
(ThinkLab → Task Manager · lifted implicit at W5). CA1-009 GENERALIZES
that contract shape. This is a forward-looking rule — no cross-app
crossings exist yet at W8 open.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HandoffActor(BaseModel):
    """Named actor on one side of a handoff · source or destination."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    app: str = Field(
        ..., min_length=1,
        description="App / service name (e.g., 'thinklab', 'task_manager')."
    )
    role: str = Field(
        ..., min_length=1,
        description="Role in the crossing (e.g., 'author', 'receiver')."
    )
    actor_id: str = Field(
        ..., min_length=1,
        description="Actor id on record (user / system). Facts-not-claims."
    )


class HandoffContract_v0(BaseModel):
    """CA1-009 generalized handoff contract."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    handoff_id: str = Field(
        ..., min_length=1,
        pattern=r"^ho_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ho_<source>_to_<dest>_<yyyy_mm>'."
    )
    what: str = Field(
        ..., min_length=1,
        description="What governed artefact is crossing. Cite the artefact "
                    "id + kind (e.g., 'thinklab_objective:obj_2026_08_042 · "
                    "carries locked-in load-bearing set')."
    )
    shape: str = Field(
        ..., min_length=1,
        description="Shape / schema the receiver commits to accept. Cite "
                    "the contract type + version if governed by a frozen "
                    "contract (e.g., 'ObjectiveRequest_v2') or the "
                    "structural sentence if plain."
    )
    identity_source: HandoffActor = Field(
        ...,
        description="Actor on the source side (authoring the handoff)."
    )
    identity_destination: HandoffActor = Field(
        ...,
        description="Actor on the destination side (receiving the handoff)."
    )
    receipt_kind: str = Field(
        ..., min_length=1,
        description="How the hand-off is confirmed on record. Free-text "
                    "sentence citing where the confirming ledger row / "
                    "receipt file lives (e.g., 'northena ledger row "
                    "ledger_row_id + task_manager acknowledge event')."
    )
    receipt_ref: Optional[str] = Field(
        default=None,
        description="Optional stable id of the confirming receipt on "
                    "record (if already on file). None until the receiving "
                    "side writes its ack."
    )
    authored_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when this handoff contract was recorded."
    )
    authored_by: str = Field(
        ..., min_length=1,
        description="Actor id that authored this contract."
    )
