"""services.answering_service · answering-service package.

Canon 17 §4 · answering service triangle: `ask` · `delivery` ·
`webhook_endpoint`. Each entity carries a frozen pydantic model and an
append-only collection accessor.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`.

SO §3.8 thin-kernel additive-only: new package surface consuming
sealed pre-M14 surfaces (services.data.repository) without editing them.
"""
