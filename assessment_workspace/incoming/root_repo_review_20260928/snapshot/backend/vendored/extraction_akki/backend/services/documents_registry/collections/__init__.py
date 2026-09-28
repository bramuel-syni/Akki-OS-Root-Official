"""services.documents_registry.collections · two-collection sub-package.

M15-W3 · binds sealed W1/W2 document contracts to per-tenant Mongo
databases via the sealed M11-W1 Repository primitive.

- `whitepapers` · wraps `contracts.whitepaper_draft.WhitepaperDraft_v0`.
- `skill_files` · wraps `contracts.skill_file_provenance_v0.SkillFileProvenanceV0`.

Each module exposes:
- the sealed pydantic model (re-imported by identity · SO §3.8),
- a `COLLECTION_NAME` string constant,
- a `_tenant_db_name(tenant_id: str) -> str` helper (Canon 3 §B.7),
- append-only `insert_*` writer + read `get_*` / `list_*_for_*` surfaces.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`
(sole Motor importer). SO §3.8 thin-kernel additive-only: new
sub-package; sealed pre-M15 surfaces consumed as-is.
"""
