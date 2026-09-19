# RB_KMS_ROTATION_ON_DEMAND_operator_triggered

**Runbook code:** `KMS_ROTATION_ON_DEMAND` — operator-triggered tenant master-key rotation (compromise-suspected).
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W3 (destroy-does-not-exist · rotation appends lineage) · Canon 8 §W1 (eyes-never-act · rotation is operator-issued, never mechanistic).
**Sealed anchor:** `services.kms.rotation_scheduler.execute_rotation` (M13-W2 · Commit-A `f2d0a792` sealed 2026-09-19T04:47Z · same primitive as scheduled rotation, different `reason` field).

## TRIGGER

An operator invokes `services.kms.rotation_scheduler.execute_rotation(tenant_id, reason="on_demand_operator_triggered")` in response to a suspected key compromise or a compensating control after a related incident. Unlike the scheduled cadence, the on-demand trigger is a deliberate operator action following owner-desk direction or a live incident's containment step. It is never triggered as a mechanism.

## EVIDENCE

- **Incident anchor:** the on-demand rotation is always tied to an open incident id (SEC-<YYYY-MM-DD-NN>) or an owner-desk directive; the `reason` field on the resulting `KeyLineageRecord` cites the incident id.
- **On-record lineage:** the `KeyLineageRecord` appended by `execute_rotation`, binding `prev_key_id → new_key_id` for the tenant, carrying `reason="on_demand_operator_triggered"` plus the incident anchor.
- **Prior key history:** `tenant_key_registry.list_key_history(tenant_id)` shows the outgoing key at the head immediately before this rotation; the incoming key becomes the new head.
- **Related evidence:** any Watch sever-certainty signals recorded within the 24-hour window prior to the on-demand rotation are cross-referenced by signal_id on the incident's evidence ledger.

## VERIFY

1. Confirm the incident anchor cited on the `reason` field is on-record in the SEC incident ledger with a state of `open` at the rotation time.
2. Confirm the `KeyLineageRecord` binds the correct `prev_key_id → new_key_id` pair per `tenant_key_registry.list_key_history` immediately before and after the rotation.
3. Confirm `tenant_key_registry.get_active_key(tenant_id)` returns the incoming key after the rotation.
4. Confirm no envelope wrap operation between rotation issue time and rotation land time succeeded under the outgoing key (a wrap under a superseded key is a Watch signal candidate under attestation_failure).

## DECIDE

The incident lead reviews the pre-rotation state and decides:
- **Option A** · proceed with the on-demand rotation as scoped to the affected tenant only.
- **Option B** · extend the rotation to related tenants if the incident's blast radius crosses tenant boundaries; each additional tenant requires its own `execute_rotation` invocation and its own `KeyLineageRecord`.
- **Option C** · route to owner-desk if the incident's evidence set does not clearly identify the affected key set; an on-demand rotation on an unclear scope is a fork banked with two options, not resolved by the runbook.

## ACT

The incident lead is the authority for every action here. Each step is operator-issued.

1. The incident lead opens the KMS operator console under the incident's operator handle.
2. The incident lead invokes `services.kms.rotation_scheduler.execute_rotation(tenant_id, reason="on_demand_operator_triggered · SEC-<YYYY-MM-DD-NN>")` per the DECIDE scope; the invocation is operator-issued, never scheduled by a mechanism.
3. If DECIDE chose Option B, the incident lead issues one additional `execute_rotation` per related tenant, each with its own operator-issued invocation.
4. The incident lead files each returned `KeyLineageRecord` id in the incident's evidence ledger.
5. The incident lead pauses new envelope wrap operations against the affected tenant(s) for a 30-minute observation window, using the write-authority console. The pause is human-issued.

## RECORD

- The incident id + each `KeyLineageRecord` id + tenant list + operator handle + rotation reason string are recorded in the SEC incident ledger.
- The observation window (start · end · verdict) is recorded on the same entry.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3 at the next §3.3 seal boundary.
- The pilot-tenant contact ledger is updated for every affected tenant so the tenant owner learns of the rotation from the platform, not from a third-party observation.

## POSTMORTEM

Within 5 working days of incident close:
- The on-demand rotation is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md`.
- The elapsed time from suspected-compromise-detection to rotation-land is measured and reported on the KMS operational dashboard.
- If the elapsed time exceeded 30 minutes, a fork is banked at STATE/DECISIONS.md offering options to reduce the detection-to-rotation latency; the fork routes to owner-desk per §6.3.
- The runbook is reviewed against the incident's evidence set; gaps that would have shortened the response time are extended in a follow-on additive seal.
