# First assembled execution architecture — verified 2026-09-27

## Delivered architectural milestone

One shared Northena control-plane path now composes:

**Frozen descriptor → exact authority binding → durable dispatch claim → worker
observation → artifact check → recorded actual usage under dispatch-time terms →
single terminal publication → current-rights retrieval.**

Four descriptor bridges cover source/Census, provisioned skill query, training and
evaluation. They consume existing component contracts/metadata; they do not admit
principals, resolve sources, invoke models or manufacture MOAC decisions.

### Runtime files

Under `backend/vendored/extraction_akki/backend/`:
- `services/northena/execution_models.py`: frozen strict metadata shapes; opaque
  Akki refs, finite measured quantities, explicit evidence mode and no raw payloads.
- `execution_validation.py`: exact identity/scope/engine/expiry and result
  key/fence/tenant binding; manifest/floor checks and revalidation of model instances.
- `execution_journal.py`: intent/observation slots in the existing canonical Ledger;
  no parallel workflow database or mutable effectiveness store.
- `execution_coordinator.py`, `execution_completion.py`: atomic submit-versus-cancel
  claim, stable-key status recovery, commit ordering, actual usage and result release.
- `execution_ports.py`: server-owned bounded async metadata RPC adapter; rejects
  sync workload callbacks, mismatched engine and MOCKED results as live receipts.
- `execution_builders.py`: read-only bridges for four kinds; training identity binds
  corpus and MOAC refs while excluding mutable progress/status.
- `execution_composition.py`: explicit production holds while authority, executors
  and independent artifact checkers remain unbound. No successful doubles registered.
- `services/portal_operational/execution.py` and additive route in
  `routers/portal_requests.py`: authenticated frozen-request advance control seam.

The advance route is `POST /api/portal/requests/{request_id}/execution/advance` with
an explicit integer `deadline_epoch`. A changed deadline for the same execution
identity conflicts; the requester cannot supply authority/adapter/actor fields.
Current production response is honestly held, never a simulated ready result.
Existing OS/DAP request history, skill-refusal routes and UI remain unchanged.

## Research applied, with trade-offs

See `ARCHITECTURE_EXECUTION_ADR.md` for fetched Temporal and Amazon Builders Library
sources and Mongo constraints. Applied stable operation IDs, sink idempotency,
durable intent-before-effect, timeout ambiguity reconciliation, single retry owner,
bounded calls and exact evidence binding. No new Temporal service/vendor added; no
sample demo-auth/second mutable authority/UI copied.

No automatic redispatch after an uncertain result. A fresh coordinator reconstructs
the previous claim and asks for its status. Exactly-once network execution is not
claimed. Model/host substitution is not used for availability. A cancellation needs
an acknowledgement; consumed work remains measurable even if release is withheld.

Full-prefix integrity verification remains deliberately uncached and can amplify
control-plane reads with large histories. Trusted checkpoints, full-Mongo contention
tests and target-hardware performance measurement remain follow-ups, not a reason to
weaken integrity or claim an unmeasured best-performance posture.

## Tests and evidence

- RED-first contract: corrected before implementation to require actual four-kind
  composed readiness, not merely accepting a submit; test doubles remain MOCKED.
- **126 passed / 0 failed / 0 skipped** across execution_spine and portal_operational.
  JUnit: `test_reports/pytest/pytest_architecture_portal_final_20260927.xml`.
- Four-kind integration uses REAL Coordinator, LedgerJournal and canonical
  emitter/writer/verifier; authority, worker, artifact checker and isolated DB are
  explicitly MOCKED/FAKE. Tests include concurrency, timeout recovery, reconstructed
  coordinator after four commit-failure boundaries, cancel interleavings, exact
  bindings, missing usage, manifest/floor refusal, terms freeze and withdrawal.
- Actual API tests validate held control intents, immutable replay/conflict,
  role/scope refusals, unsupported operations and malformed inputs through existing
  Mongo. No approvals/grants/users created; no history deleted.
- Protected canonical/principal/prototype hashes checked unchanged. Desktop/mobile
  unchanged-shell smoke passed; there is no new UI to validate or redesign.
- Final independent-of-test-run re-performance reused the checker fixture and banked
  four seven-step traces, request hashes and minted row hashes in
  `architecture_verification/FINAL_ARCHITECTURE_EVIDENCE_20260927.json`. This is not
  EX4/R37 technical independence or a self-contained full archived-chain proof.

### Findings resolved, not hidden

Iteration26's403/404 report was a contradictory test expectation: the same analyst
role was expected to receive403 for one operator-owned request and404 for another.
The live test now proves uniform analyst403 for known/random IDs, authorized
operator404 for unknown IDs; an isolated write-authorized foreign-principal test
proves404. Runtime authentication was NOT reordered/weakened.

Iteration27 found training's objective-specific hash omitted corpus/MOAC refs.
The complete Request digest already bound those input refs; the objective digest
now binds them too so downstream descriptor consumers see consistent identity.
Original failing reports remain retained; final regression is all green.

## Explicit limits / next work

Architecture evidence is verified for this four-kind control spine. Live element
validation is **not** verified. Production authority/worker/artifact integrations
remain unbound; callable query still refuses without admitted execution. Older
MOCKED training/evaluation implementations were not relabelled or replaced with
purported real experiments. Consumption events here are not real invoices/grants.

Next: bind existing admitted engine/authority/registry producers to these tested
ports, finish their custody/queued-handoff and commercial consumers, and expand
whole-programme architectural compositions. Keep unavailable elements isolated
without blocking independent assembly. Actual worker acceptance, source population,
full Mongo replica/failover/concurrency and hardware performance stay separately
tracked. GPU remains parked; no new decision or credentials requested.

Useful later enhancement: show the same receipt-linked execution prerequisites in
the existing request drawer, preserving the owner prototype and measured/unknown
distinction.