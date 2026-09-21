"""C13Provenance_v0 · frozen pydantic contract for C.13 closure wave
provenance shape.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "provenance separated
from content and immutable".

Closed 4-field tuple (alphabetical):
  - content_sha256: str · sha256 hex over the content's payload_bytes
    (64 lowercase-hex characters · SO §3.10-α closed-schema discipline)
  - produced_at: str · ISO-8601 timestamp of provenance record creation
    (min_length=1)
  - produced_by: str · component_id of the writer (identity source · e.g.
    component_alpha_v1 · min_length=1)
  - scoped_key: str · 32-char lowercase-hex from
    services.c13_scope.key_derivation.derive_scoped_key (SO §3.10-α +
    OWNER-DROP-02 forward rule)

model_config: extra="forbid" · frozen=True (immutability structural)

Canon 3 §9.3 append-only writer discipline: provenance records constructed
once, never mutated (frozen=True enforces).

Canon 8 §W11 structural role separation: provenance shape has NO
payload_bytes / content-bearing field. Content lives at
contracts.c13_content_v0.C13Content_v0.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class C13Provenance_v0(BaseModel):
    """Immutable provenance record for a C.13 scoped-key write boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    content_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$",
        description="sha256 hex over payload_bytes (64 lowercase-hex)",
    )
    produced_at: str = Field(
        min_length=1,
        description="ISO-8601 timestamp of provenance record creation",
    )
    produced_by: str = Field(
        min_length=1,
        description="component_id of the writer (identity source)",
    )
    scoped_key: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="32-char lowercase-hex from derive_scoped_key",
    )
