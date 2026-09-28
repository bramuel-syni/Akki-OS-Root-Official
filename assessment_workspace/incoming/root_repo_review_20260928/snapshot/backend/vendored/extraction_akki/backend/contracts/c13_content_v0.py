"""C13Content_v0 · frozen pydantic contract for C.13 closure wave
content shape.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "provenance separated
from content and immutable".

Closed 2-field tuple (alphabetical):
  - content_sha256: str · sha256 hex over payload_bytes (64 lowercase-
    hex characters · SO §3.10-α closed-schema discipline · matches
    the provenance shape's content_sha256 field for cross-shape
    correlation at read boundary)
  - payload_bytes: bytes · the actual content byte-string

model_config: extra="forbid" · frozen=True (immutability structural)

Canon 8 §W11 structural role separation: content shape has NO
provenance fields (produced_by / produced_at / scoped_key). Provenance
lives at contracts.c13_provenance_v0.C13Provenance_v0.

Immutability discipline: frozen=True + bytes semantics (Python bytes
are immutable · the field cannot be replaced after construction).
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class C13Content_v0(BaseModel):
    """Immutable content record for a C.13 scoped-key write boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    content_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$",
        description="sha256 hex over payload_bytes (64 lowercase-hex)",
    )
    payload_bytes: bytes = Field(
        description="the content byte-string",
    )
