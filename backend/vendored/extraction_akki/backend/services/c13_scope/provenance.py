"""Provenance / content separation re-export for C.13 closure.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "provenance separated
from content and immutable".

Provenance shape lives at contracts/c13_provenance_v0.py (frozen pydantic
with closed 4-field tuple: content_sha256 · produced_at · produced_by ·
scoped_key). Content shape lives at contracts/c13_content_v0.py (frozen
pydantic with closed 2-field tuple: content_sha256 · payload_bytes).

Immutability enforced structurally via pydantic model_config
frozen=True + extra=forbid + closed field set. Separation enforced
structurally at contract level (the provenance shape has NO
payload_bytes field · the content shape has NO produced_by /
produced_at / scoped_key fields).

Canon 3 §9.3 append-only writer discipline: provenance records are
immutable at construction. Canon 8 §W11 structural role separation:
provenance and content are distinct shapes with disjoint field sets.

This module is a pure re-export surface (identity imports from the
sealed contracts modules · no logic).
"""
from __future__ import annotations

from contracts.c13_provenance_v0 import C13Provenance_v0
from contracts.c13_content_v0 import C13Content_v0

__all__ = ("C13Provenance_v0", "C13Content_v0")
