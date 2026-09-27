# Architecture-first governed execution — ADR, 2026-09-26

## Owner direction

Owner: “the principle here is to ensure that we implement principles that are known, tested and have evidence of best performance posture. Research and implement requirements as per best posture, we are testing the architecture not the elements. elements should work in principle and if they dont we will fix them once we have all piecec together.”

Owner confirmed: research established patterns/trade-offs; assemble source, skill,
training/evaluation paths against real interfaces; use labelled test doubles for
unavailable elements; keep mandatory authority/custody gates and E1-not-data-path;
GPU parked. Element availability no longer blocks architectural assembly/testing.

## Research and selected posture

1. Temporal, *What is idempotency? And why it matters for durable systems*:
   https://temporal.io/blog/idempotency-and-durable-execution — fetched2026-09-26.
   Separates deterministic durable workflow history from external activities;
   activities can be delivered more than once; stable business-operation keys and
   sink-side deduplication are required. A preflight existence check alone races.
2. Amazon Builders Library, *Timeouts, retries, and backoff with jitter*:
   https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
   — fetched2026-09-26. Timeouts do not prove absence of side effects; limit retries
   at one layer; retry amplification/load makes aggressive replay unsafe. Timeout
   tuning requires measured downstream latency, not invented optimal constants.
3. MongoDB, unique indexes and transactions:
   https://www.mongodb.com/docs/manual/core/index-unique/
   https://www.mongodb.com/docs/manual/core/transactions/
   — existing canonical writer already uses tenant+command and tenant+sequence
   unique indexes. Reuse that durable commit boundary rather than introduce an
   independently mutable operations store and dual-write window.
4. Existing integration guidance: remote submit/status/cancel metadata protocols;
   per-engine authority and sealed SSH checks remain at Akki; independently
   checked artifact manifests; actual usage; current rights before release.

These are established reliability mechanisms and their documented trade-offs,
NOT a benchmark proving universally best latency/throughput on Akki hardware.
No vendor sample's demo auth, mutable operation store, defaults or new UI is copied.

## Decision

Build an additive Northena execution spine with strict immutable metadata contracts,
durable Ledger-backed intent/observation/terminal records and injected typed
authority/executor/registry ports. Northena coordinates; governing engines retain
decisions and Akki workers retain all source/model/artifact payloads.

- Four explicit kinds: source, skill, training, evaluation. Governing-engine mapping
  remains explicit; a skill query is Solva-governed, while skill development/training
  remains Targeta-governed. Existing DAP operation mappings are not rewritten.
- A single durable dispatch-claim key chooses the initial submitter. Others resume
  through status with the SAME worker operation key. No “exactly once” network claim.
- Any submit ambiguity is recorded unknown and reconciled; never blindly redispatch
  or switch host/model. Adapter status and sink idempotency are required contracts.
- Register/check artifacts and meter actual consumption before terminal publication.
  Missing usage is unavailable, not zero. Event-time terms stay bound to the approved
  dispatch snapshot; current rights are independently rechecked before release.
- Cancellation is an intent and worker-acknowledged outcome, not rollback. A single
  terminal command prevents incompatible terminal histories; reread the winner.
- No timers, scheduler, detached background tasks or local workload executors. Each
  coordinator advance is bounded metadata RPC composition; durable scheduling remains
  a separate admitted worker concern. No source/SSH/model operation is exercised here.
- Production bindings are server-side composition, never caller-selected callbacks
  or policy booleans. Unbound authority/elements remain truthful holds. Tests supply
  labelled adapters; no test double is registered as a production default.
- Architectural completion and operational element validation are separate evidence
  axes. An architectural completed trace marked MOCKED does not unlock real serving,
  approve a request, become a real invoice or replace held portal states.

## Integration boundary

Existing DAP request APIs and literal UI stay intact. Add an authenticated request
execution-control seam over a reconstructed frozen request; it reads the same
Ledger and keeps absent admissions held. No public approval/adapter-registration
endpoint. Callable-skill, source and training/evaluation integrations share the same
coordinator contracts through server-owned adapters, not a new model/client bypass.

Sealed principal carriers, canonical writer/verifier/row, DAP state machine, existing
SSH boundary, training/MOAC and prototype files remain unchanged. Execution `phase`
is orchestration evidence, not an invented DAP lifecycle edge or new policy authority.

## Six-field execution contract

1. **Denominator:** four architectural kinds `[source, skill, training, evaluation]`,
   plus the production held-request boundary; pin IDs/tests before implementation.
2. **Procedure:** for each kind assemble frozen request→authority→durable dispatch
   intent→executor observation→artifact checks/registration→actual metering→terminal
   publication→current-rights retrieval. Exercise restart, conflict, concurrent submit,
   ambiguous result, cancellation, withdrawal, invalid artifacts and ledger failure.
3. **Artifact:** one verification row per kind with outcome, component-double labels,
   trace/evidence refs, and separate `architecture_verified` / `live_element_verified`.
   Record production-boundary checks separately; no denominator inflation.
4. **Acceptance script:** write RED before runtime edits, then run integration and
   existing portal regressions. Protected EX4/R37 independence is not asserted merely
   because another process wrote tests in the shared workspace.
5. **Shortcuts/detectors:** (a) bool-only authority → exact request/scope/expiry binding
   tests; (b) fake exactly-once → concurrency and lost-response restart tests; (c) mock
   success as production → evidence-mode propagation and default-hold tests; (d) ready
   before receipts → artifact/meter/commit fault tests; (e) element isolation only →
   complete four-kind composed traces; (f) inferred performance → no claimed SLOs.
6. **Evidence:** research citations/ADR, pinned RED/GREEN scripts/output, four-kind
   trace artifacts, current protected-file hashes and actual held API smoke. Local
   architecture timing, if measured, must not be called Akki workload performance.

## Deferred operational checks, not architectural blockers

Actual source population/GPU execution, serving quality, real training/evaluation,
independent artifact checking/registry admission and metering producers, protected
benchmark placement, notification/witness facilities and owner-held policy choices.
Adapters cannot silently manufacture these authorities or claim their measured
performance. Existing decision register remains effective.