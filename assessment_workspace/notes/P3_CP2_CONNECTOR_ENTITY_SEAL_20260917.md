READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P3-CP2 · M9 · Platform-layer connector_entity · seal note · 2026-09-17T~05:30Z

**Track-a HEAD:** `df6d3cf6dada703d28af5c92717a977a2bf2df9f`. **Ratchet:** 4525 → **4534** (+9).

## Anchor
§10 verbatim: `connector (id, tenant_id, estate_id, type, location, credential_ref, scope, mode, mou_task_ref, status)`. §5.2 M-C-1 verbatim: *"Every connector carries: type, location, credential_ref, scope, mode, mou_task_ref, status. Empty scope is invalid."*

## Mechanism
`services/platform_control_plane/connector_entity.py` · `ConnectorEntity` frozen 10-carrier all str OPEN · `CONNECTOR_ENTITY_FIELDS` tuple · preventive-charter `assert_connector_carrier_valid` fail-fast:
1. `scope == ""` → `EmptyScopeRefused`.
2. `mou_task_ref == ""` → `MissingMouTaskRefRefused`.

3 refusal classes · COUNTS-only messages.

## Invariants (9)
Module fabric · frozen 10-carrier · fields constant · refusal hierarchy · empty-scope refusal · missing-mou-task-ref refusal · admits when both non-empty · refusal-order (scope before mou_task_ref) · anchor + grep-negative + import-negative.

## Double-green
GREEN1 4534/1/0 · GREEN2 4534/1/0.

## §3.3
- A `df6d3cf6dada703d28af5c92717a977a2bf2df9f` ✅.
- B `f974aa6177db3e8246cf93a9ecaac725578fd759` ✅.
- C this-turn.

## GPU util
Elapsed **25.63 h** · remaining **46.37 h**.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
