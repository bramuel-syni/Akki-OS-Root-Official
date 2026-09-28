"""services.documents_registry.collections.whitepapers · WhitepaperDraft_v0 collection.

Doc 14 §33 · sealed W1 shape (`WhitepaperDraft_v0` CITATION invariant ·
closed 8-field tuple) · consumed as-is from `contracts.whitepaper_draft`.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`
(sole Motor importer for the data plane).

Append-only writer discipline (Canon 3 §9.3 · M11 single-writer):
only `insert_whitepaper_draft` is exposed. No `update_*`, `delete_*`,
`upsert_*`, `replace_*`, `modify_*`, `drop_*` surface (AST-enforced by
M15-W3 test 5).

SO §3.8 thin-kernel additive-only: consumes sealed pre-M15 Repository
primitive + sealed W1 model without editing either. SO §3.10-α closed
schema discipline: sealed `WhitepaperDraft_v0` (extra=forbid + frozen)
is re-exposed by import identity (never redefined here).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# Sealed W1 surface · consumed as-is via import identity (SO §3.8).
from contracts.whitepaper_draft import WhitepaperDraft_v0


# Collection name constant · used as the Mongo collection name under
# `t_<tenant_id>` database.
COLLECTION_NAME: str = "whitepaper_drafts"


def _tenant_db_name(tenant_id: str) -> str:
    """Return the per-tenant DB name for the whitepapers collection.

    Canon 3 §B.7 · M11 discipline: `t_<tenant_id>`.
    """
    return f"t_{tenant_id}"


def insert_whitepaper_draft(
    draft: WhitepaperDraft_v0,
    *,
    repository: Any,  # services.data.repository.Repository instance
) -> WhitepaperDraft_v0:
    """Append-only insert of a whitepaper-draft row.

    Callers supply a Repository bound to the correct tenant context;
    cross-tenant refusal is enforced at the primitive (AKKI-DATA-001).
    """
    doc: Dict[str, Any] = draft.model_dump()
    repository.insert_one(doc)
    return draft


def get_whitepaper_draft(
    whitepaper_id: str,
    *,
    repository: Any,
) -> Optional[WhitepaperDraft_v0]:
    """Read-surface lookup by `whitepaper_id` under the current tenant
    context, or None if absent."""
    doc = repository.find_one({"whitepaper_id": whitepaper_id})
    if doc is None:
        return None
    doc = {k: v for k, v in doc.items() if k != "_id"}
    return WhitepaperDraft_v0(**doc)


def list_whitepaper_drafts_for_run(
    run_ref: str,
    *,
    repository: Any,
) -> List[WhitepaperDraft_v0]:
    """Read-surface: all whitepaper-drafts under the current tenant
    context for a given `run_ref`."""
    cursor = repository.find({"run_ref": run_ref})
    out: List[WhitepaperDraft_v0] = []
    for doc in cursor:
        doc = {k: v for k, v in doc.items() if k != "_id"}
        out.append(WhitepaperDraft_v0(**doc))
    return out
