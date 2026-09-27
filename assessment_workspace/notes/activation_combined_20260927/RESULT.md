# Combined activation continuation — 2026-09-27

## Verdict
**Verified engineering batch, NOT completed live activation.** No real A/B/C
certificate was issued. No source/model data was processed through E1. GPU/SSH
and the original runtime were untouched. UI and protected owner/Canon hashes pass.

## Recovery, before implementation
Read-only aggregation of the existing Mongo `ledger_v1_control_events` found:
- 641 DAP request events;24 execution request events;16 execution portal-view events.
- 15 activation validation observations.
- No existing signed activation controls, approvals, allocations or worker records.

Local legacy runner metadata:4 mock-mode runs,3 closed_rejected and1 historical
closed_adopted. These records were NOT rewritten or considered activation proof.
This is not a claim that the original live Akki estate lacks its own records.

## Implemented
1. `receipts.py`: canonical Ledger references + existing Watch Ed25519 verification,
   admitted native signer/permission/scope/provenance/time checks, revocation and
   signed metadata intake. No credentials/key store/authentication changes.
2. `record_shapes.py`, `approvals.py`, `decisions.py`: signed immutable plans,
   exact owner inputs/dials/policies, snapshot/acceptance-script commitments,
   scope/expenditure/purpose groups, quorum/latest decisions, worker/allocation
   joins and the existing ComponentAuthority operation producer.
3. `conditional_control.py`, `reservations.py`: same-Ledger optimistic atomic
   reservations. Unique tenant/sequence arbitrates competing processes. A changed
   prefix forces recomputation, not a stale arithmetic retry. Unknown outcomes
   retain funds; signed terminal measurements settle, including truthful overrun.
4. `runtime_limits.py`, `worker_gate.py`, `bounded_adapter.py`: exact request/plan/
   reservation/operation/fence worker acknowledgement before send, safe replay,
   bounded provider waits, accounting before batches and inclusive termination
   window. Cooperative helper still needs the actual admitted hard supervisor.
5. `native_evidence.py`, `native_joins.py`, `model_proofs.py`, `issuance.py`: concrete
   signature/approval/native request/registry/usage/reservation/provenance and
   chronology checks; predeclared snapshots/script and semantic reference checks;
   independent skill/evaluation/release evidence; signed certificate recording
   only after proof and compare-and-append freshness.
6. Legacy `recorded_effect.py`, runner and MOAC emitter: one effect claim/result;
   emission and close never retrain; unresolved historical/uncertain effects hold.
   Missing independent scores are null/not_measured. No fabricated MOAC ceremony
   or chargeable MOCKED usage. Release is separate, not caller acceptance.

## Tests and evidence class
- `/app/test_reports/pytest/activation_combined_canonical.xml`: **520 pass,2 gated
  skips,0 failures/errors**,120.37 seconds. Original451-test behaviour preserved.
- Reports42/43: new live HTTP auth/scope/bounds/unbound refusal checks and signed
  semantic mutation coverage. Original EngineAdapter contract restored unchanged.
- Real Ed25519 math, but all positive signer admissions/observations are test-only
  SYNTHETIC. Full Path-A certificate chain/issuer positive uses FAKE storage and
  fabricated metadata, explicitly no real workload. Complete native B/C positive
  chain not established; numerical model-acceptance and refusal guards are tested.
- Real Mongo two-client reservation race under a unique TEST-SYNTHETIC tenant.
  These append-only test receipts remain isolated; no production account, root key
  or worker was installed and no workload ran. This proves storage arbitration,
  not real budget authority, measurements or execution.
- External desktop shell smoke passed. Frontend unchanged. Scoped Python lint
  passed. Third-party multipart deprecation remains non-blocking.

## Remaining scope, not concealed as GPU dependency
Actual admitted-key/provenance resolver, effective native authority imports and
owning-engine transports are not bound in this workspace. The explicit composition
factory is implementation, NOT activation. Source/skill/model producers, native
descriptor/query bindings, genuine DQ/inspection/usage, actual byte delivery and
live acceptance remain work. Independent non-GPU work is not parked as a policy;
live effects require an admitted route, and none was recovered for this composition.
See BINDING_SPEC.md. Do not substitute local fixtures or legacy mock records.