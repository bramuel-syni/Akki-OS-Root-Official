"""services.documents_registry.frame_precedence · D-12 admission gate.

M15-W4 · Frame precedence via HandoffContract binding. Closes D-12
structurally: no document class (whitepaper or skill_file provenance
record) may claim precedence over the `HandoffContract_v0` that
authored it. The gate admits a document only when the hand-off
contract's ``what`` field cites the document's governed-artefact
identifier.

Canon anchors:
- **D-12** frame precedence: hand-off authors documents, never the
  other way around.
- **CA1-009**: every cross-app crossing is expressed as a
  `HandoffContract_v0` before it ships.
- **Canon 15 §33** (M14-W1 sealed): four required fields on
  `HandoffContract_v0` · `what` field carries the governed-artefact
  cite.
- **Canon 8 §W11** one-task-one-identity: this module is a pure
  admission predicate — it does NOT sign, does NOT persist, does NOT
  emit ledger intents.

Discipline:
- No `services.documents_registry.collections.*` imports
  (persist path).
- No `services.watch.*` imports (signing path).
- No direct Motor imports (M11-W1 sole Motor importer).
- No mutation function surface (only `admit_document`).

Shape drift is a pydantic `ValidationError` at construction (handled
by sealed W1/W2 + M14-W1 models); this module accepts already-
constructed instances and raises `FramePrecedenceRefused` on a
missing hand-off cite or an unknown document type.
"""
from __future__ import annotations

from typing import Any

# Sealed W1/W2 surfaces consumed by identity import (SO §3.8).
from contracts.skill_file_provenance_v0 import SkillFileProvenanceV0
from contracts.whitepaper_draft import WhitepaperDraft_v0

# Sealed M14-W1 surface (HandoffContract_v0) consumed for type-hint
# purposes only. We use `Any` at the parameter level to keep this
# module a pure predicate — no coupling to construction concerns.
from contracts.handoff_contract import HandoffContract_v0


class FramePrecedenceRefused(RuntimeError):
    """D-12 refusal: the hand-off contract does not cite the
    document's governed-artefact id (or the document is not a known
    sealed type)."""


def _document_governed_artefact_ref(document: Any) -> str:
    """Return the governed-artefact id that the hand-off contract's
    ``what`` field MUST cite.

    - `WhitepaperDraft_v0` · `whitepaper_id`.
    - `SkillFileProvenanceV0` · `skill_id`.

    Raises `FramePrecedenceRefused` for any other type (SO §3.10-α
    closed-schema discipline: the gate is closed to the two sealed
    document types).
    """
    if isinstance(document, WhitepaperDraft_v0):
        return document.whitepaper_id
    if isinstance(document, SkillFileProvenanceV0):
        return document.skill_id
    raise FramePrecedenceRefused(
        "D-12 · frame_precedence.admit_document refuses unknown "
        f"document type {type(document).__name__!r} · admissible types "
        "are WhitepaperDraft_v0 (sealed W1) and SkillFileProvenanceV0 "
        "(sealed W2)."
    )


def admit_document(
    document: Any,
    *,
    handoff_contract: HandoffContract_v0,
) -> Any:
    """D-12 admission gate.

    Admits `document` if and only if `handoff_contract.what` contains
    the document's governed-artefact id. Returns the same document
    instance on admission (identity, not a copy).

    Raises `FramePrecedenceRefused` on:
    - unknown document type,
    - missing hand-off cite.
    """
    doc_ref = _document_governed_artefact_ref(document)
    if doc_ref not in handoff_contract.what:
        raise FramePrecedenceRefused(
            "D-12 · frame_precedence.admit_document refuses admission: "
            "hand-off contract's `what` field does not cite the "
            f"document's governed-artefact id (expected substring: "
            f"{doc_ref!r}) · CA1-009 requires every cross-app crossing "
            "to be authored by a HandoffContract_v0 that names the "
            "artefact being handed off."
        )
    return document
