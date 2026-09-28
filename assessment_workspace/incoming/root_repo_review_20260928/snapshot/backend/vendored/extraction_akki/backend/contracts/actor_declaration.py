"""Actor Declaration — Canon 3 §6 seat contract, Build Order 01 §4.A1.

Frozen contract for the actor-declaration record class.

Canonical anchor: Canon 3 §6 (Admit — declarations captured before operations)
and Canon 6 §3 (setup declarations morning forward). Every actor entering
the platform (human, agent, or connector service) must carry an in-force
declaration; admit refuses on missing/expired/scope-mismatched declaration.

Contract version: v0. Parity-seat entry in
`tests/invariants/actor_declaration_v0.contract_snapshot.json`.

This is a THIN-KERNEL record class per Build Order 01 §4.A0 — one of the
six classes the live path touches: Ledger.Row, Receipt, Census.Snapshot,
Actor.Declaration, Ingestion.Artifact, Training.Artifact.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


DECLARATION_COLLECTION = "actor_declarations"


ActorKind = Literal["human", "agent", "connector", "infrastructure"]


class ActorDeclaration(BaseModel):
    """Actor declaration record — Canon 3 §6 shape.

    Fields:
      actor_id           — stable id of the declarant.
      actor_kind         — human · agent · connector · infrastructure (Build
                           Order 01 §6 adds infrastructure for the VM).
      objective          — declared purpose in one sentence (org language).
      capabilities       — declared capability list (Build Order 01 §6.1).
      risks              — declared risk list (Build Order 01 §6.1).
      scope              — bounded scope tuple; admit checks against this.
      declared_at        — first-declaration timestamp (UTC).
      expires_at         — hard expiry; supersession required after.
      superseded_by      — id of a later declaration that replaces this
                           one (Canon 3 §6 append-only chain).
      lawful_basis       — reference to the lawful basis this declaration
                           relies on (crosses to admit's completeness check).
    """

    model_config = ConfigDict(extra="forbid")

    actor_id: str
    actor_kind: ActorKind
    objective: str = Field(min_length=1)
    capabilities: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    scope: List[str] = Field(default_factory=list)
    declared_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    expires_at: Optional[datetime] = None
    superseded_by: Optional[str] = None
    lawful_basis: str = Field(min_length=1)


DeclarationVerdict = Literal[
    "in_force",
    "missing",
    "expired",
    "scope_mismatch",
    "superseded",
]
