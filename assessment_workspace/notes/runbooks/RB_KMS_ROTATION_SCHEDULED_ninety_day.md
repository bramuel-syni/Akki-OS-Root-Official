# RB_KMS_ROTATION_SCHEDULED_ninety_day

**Runbook code:** `KMS_ROTATION_SCHEDULED` — 90-day cadence tenant master-key rotation.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W3 (destroy-does-not-exist · rotation appends lineage) · §6.4 pre-ruling 4 R-4 verbatim ("KMS: envelope encryption, per-tenant keys, 90-day rotation").
**Sealed anchor:** `services.kms.rotation_scheduler.execute_rotation` (M13-W2 · Commit-A `f2d0a792` sealed 2026-09-19T04:47Z · `ROTATION_CADENCE_DAYS = 90`).

## TRIGGER

`services.kms.rotation_scheduler.rotation_due(tenant_id, last_rotated_at)` returns `True` when the elapsed time since a tenant's `last_rotated_at` reaches or exceeds the 90-day cadence. The scheduled trigger is a wall-clock check run per tenant; on `True`, an operator invokes `execute_rotation(tenant_id, reason="scheduled_90_day_cadence")` from the KMS operator console.

## EVIDENCE

- **On-record lineage:** the `KeyLineageRecord` appended by `execute_rotation`, binding `prev_key_id → new_key_id` for the tenant.
- **Ratchet + baseline_failures.json:** M13-W2 seal at Commit-A `f2d0a792` records the rotation module as landed; ratchet advanced 5279 → 5288.
- **Terraform manifest:** `notes/M13_W4_terraform_manifest.yaml` resource `kms_master_key_store` carries `rotation_cadence_days: 90` verbatim; drift between this cadence and the sealed module's `ROTATION_CADENCE_DAYS` fails `test_kms_master_key_store_carries_90_day_rotation_cadence` (M13-W4 · Commit-A `ffadd24b`).
- **Tenant key registry:** `services.kms.tenant_key_registry.list_key_history(tenant_id)` returns the tenant's full append-only key history; the new key from this rotation must appear as the head with `active_at_iso` set to the rotation time.

## VERIFY

1. Confirm the `KeyLineageRecord` is present under the tenant's lineage store and binds a `prev_key_id` (the outgoing key) to a fresh `new_key_id` (the incoming key).
2. Confirm `tenant_key_registry.get_active_key(tenant_id)` returns the incoming key (the head of the append-only history) and NOT the outgoing key.
3. Confirm the rotation `reason` field on the lineage record equals `"scheduled_90_day_cadence"`.
4. Confirm no envelope written before the rotation `active_at_iso` decrypts under the new key (envelope wrap/unwrap remains scoped to the key active at write time per Canon 8 §W11 one-task-one-identity).

## DECIDE

The KMS operator reviews the pre-rotation lineage head and decides:
- **Option A** · proceed with the scheduled rotation as-is (default when the cadence check is the only trigger and no incident is open).
- **Option B** · defer the scheduled rotation by up to 24 hours if a live incident is open against the affected tenant; log the defer decision on the tenant's operational ledger and page the on-call lead.
- **Option C** · route to owner-desk if the tenant's key history shows any signs of prior compromise (e.g., an on-demand rotation recorded within the past 30 days) — a scheduled rotation on top of a suspected compromise pattern is a fork banked with two options, not resolved by the runbook alone.

## ACT

The KMS operator is the authority for every action here. Each step is human-issued.

1. The KMS operator opens the KMS operator console.
2. The KMS operator invokes `services.kms.rotation_scheduler.execute_rotation(tenant_id, reason="scheduled_90_day_cadence")` — the invocation is operator-issued from the console; the module NEVER runs the invocation on a schedule of its own.
3. The KMS operator verifies the returned `KeyLineageRecord` and files the record id in the tenant's operational ledger.
4. The KMS operator opens a monitored 30-minute observation window; during this window the operator watches for any envelope wrap/unwrap errors flagged by the OTel `traced_call` wrapper.

## RECORD

- The `KeyLineageRecord` id + tenant_id + prev_key_id + new_key_id + rotation reason + operator handle are recorded on the tenant's operational ledger.
- The 30-minute observation window (start · end · verdict) is recorded on the same entry.
- If DECIDE chose Option B or Option C, the fork banking is recorded on STATE/DECISIONS.md (per §6.3) at the next §3.3 seal boundary.

## POSTMORTEM

Within 24 hours of the rotation (or 24 hours after the observation window closes if it stayed open):
- The rotation cadence adherence rate for the tenant is updated in the KMS operational dashboard.
- If any envelope wrap/unwrap errors surfaced during the observation window, a separate incident is opened for envelope integrity; the incident links back to this rotation's `KeyLineageRecord` id.
- The runbook is reviewed for gaps; if the tenant's rotation history reveals a pattern the runbook did not anticipate, a fork is banked at STATE/DECISIONS.md.
