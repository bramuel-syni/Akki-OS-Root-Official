"""services.documents_registry.collections.skill_files · SkillFileProvenanceV0 collection.

Doc 18 A18.7 · sealed W2 shape (`SkillFileProvenanceV0` buyer-facing
provenance chain · closed 7-field tuple + closed 4-tuple Literal
`PROVENANCE_STEP_KINDS`) · consumed as-is from
`contracts.skill_file_provenance_v0`.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`
(sole Motor importer for the data plane).

Append-only writer discipline (Canon 3 §9.3 · M11 single-writer +
TF-E4 (b) α write-once): only `insert_skill_file_provenance` is
exposed. No `update_*`, `delete_*`, `upsert_*`, `replace_*`,
`modify_*`, `drop_*` surface (AST-enforced by M15-W3 test 5).

Note: TF-E4 (b) α write-once discipline for the JSONL persistence
surface is implemented at `services.skill_files.persistence.append`
(sealed pre-M15). This Mongo collection wrapper composes on top of
Repository (M11-W1) for per-tenant DB scope; TF-E4 (b) α is the
concern of the sealed JSONL layer, not of this thin-adapter module.

SO §3.8 thin-kernel additive-only: consumes sealed pre-M15 Repository
primitive + sealed W2 model without editing either. SO §3.10-α closed
schema discipline: sealed `SkillFileProvenanceV0` (extra=forbid +
frozen) is re-exposed by import identity (never redefined here).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# Sealed W2 surface · consumed as-is via import identity (SO §3.8).
from contracts.skill_file_provenance_v0 import SkillFileProvenanceV0


# Collection name constant · used as the Mongo collection name under
# `t_<tenant_id>` database.
COLLECTION_NAME: str = "skill_file_provenances"


def _tenant_db_name(tenant_id: str) -> str:
    """Return the per-tenant DB name for the skill-files collection.

    Canon 3 §B.7 · M11 discipline: `t_<tenant_id>`.
    """
    return f"t_{tenant_id}"


def insert_skill_file_provenance(
    provenance: SkillFileProvenanceV0,
    *,
    repository: Any,  # services.data.repository.Repository instance
) -> SkillFileProvenanceV0:
    """Append-only insert of a skill-file-provenance row.

    Callers supply a Repository bound to the correct tenant context;
    cross-tenant refusal is enforced at the primitive (AKKI-DATA-001).
    """
    doc: Dict[str, Any] = provenance.model_dump()
    repository.insert_one(doc)
    return provenance


def get_skill_file_provenance(
    skill_id: str,
    *,
    repository: Any,
) -> Optional[SkillFileProvenanceV0]:
    """Read-surface lookup by `skill_id` under the current tenant
    context, or None if absent."""
    doc = repository.find_one({"skill_id": skill_id})
    if doc is None:
        return None
    doc = {k: v for k, v in doc.items() if k != "_id"}
    return SkillFileProvenanceV0(**doc)


def list_skill_file_provenances_for_adapter(
    adapter_id: str,
    *,
    repository: Any,
) -> List[SkillFileProvenanceV0]:
    """Read-surface: all skill-file-provenances under the current
    tenant context for a given `adapter_id`."""
    cursor = repository.find({"adapter_id": adapter_id})
    out: List[SkillFileProvenanceV0] = []
    for doc in cursor:
        doc = {k: v for k, v in doc.items() if k != "_id"}
        out.append(SkillFileProvenanceV0(**doc))
    return out
