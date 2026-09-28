"""services.answering_service.collections · three-collection sub-package.

Canon 17 §4 · answering-service triangle: `asks` · `deliveries` ·
`webhook_endpoints`. Each module exposes a frozen pydantic model + an
append-only collection accessor + a `_tenant_db_name` helper.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`
(sole Motor importer for the data plane).

SO §3.8 thin-kernel additive-only: new sub-package; sealed pre-M14
Repository primitive consumed as-is.
"""
