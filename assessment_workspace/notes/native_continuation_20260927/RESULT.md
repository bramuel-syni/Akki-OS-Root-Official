# Native continuation, recovery and hold reasons — 2026-09-27

User authorised the next action items, backlog and the hold-reason enhancement
together. GPU/SSH remained parked; no source/model data was processed through E1.

## Delivered engineering
- Explicit optional native runtime startup/shutdown composition. An existing
  admitted native provider must supply the signer directory, native PrincipalV1
  lookup, bounded worker clients, inspector and applicable eligibility/handoff
  ports. Missing configuration does nothing; partial/wrong-ledger/unbounded
  configurations fail closed. No credential, identity, key or approval is created.
- `GET /api/portal/activation/runtime` exposes safe configuration state only,
  never a grant/health certificate. Current application composition remains unbound.
- Portal answering/training requests can recover a matching signed native plan
  instead of inventing model inputs from source IDs. Principal, tenant, objective,
  operation, units and deadline must match. Missing descriptors return409 and
  append a durable `descriptor_held` event without creating an execution request.
  Skill provisioning is not relabelled answering/training; raw custody delivery
  is not relabelled a source scan.
- DAP and OS show the same safe reason code, explanation/action and receipted
  history inside existing prototype elements. Unknown native errors/identities
  are not echoed. No owner HTML, source styles, page layout or typography changed.
- A durable `worker_outcome` checkpoint prevents contradictory terminal facts.
  Older `worker_terminal` checkpoints remain readable. Delayed running/accepted
  replies reuse the definitive outcome rather than blocking a valid concurrent
  completion. Recovery finishes verification/accounting without re-running work.
- Requests interrupted before a portal-view update expose reconciliation/retry,
  not assumed execution. A late diagnostic view cannot reopen a canonical terminal
  or turn a MOCKED result into a releasable one.
- Native certificate verification now checks actual worker outcomes, canonical
  dispatch fences and pre-send signed runtime acknowledgements. Independent
  evaluation requires its OWN approved plan, allocation/reservation, distinct
  admitted worker/runtime, bounded ACK, metering/terms, registered report and
  terminal settlement. Child and supporting receipt dependencies must precede
  the certificate verifier head. Repeated usage units are summed, not overwritten.

## Verification and evidence class
- Final authoritative suite: **565 passed,2 explicitly gated custody drills
  skipped,0 failures/errors** in131.853s. Evidence:
  `test_reports/pytest/native_continuation_verified.xml` and matching `.log`.
  The earlier556-pass run preceded the last evaluation joins.
- All7 frontend tests pass. Scoped runtime Python lint passes.
- Desktop1920×800 and mobile390×844 verification used an existing request with a
  1071-character objective among hundreds of records; no horizontal overflow.
  Testing report44 independently verified the unchanged DAP/OS layout and reasons.
- Four real-Mongo, fresh-process crash drills pass: before send; after the
  synthetic effect/before response; after worker outcome/before observation; and
  before final control completion. Each preserves one operation/fence, simulated
  effect, submit, metering and terminal completion. These are separate processes
  on this SAME HOST, not independent physical-host/custody qualification.
- Complete signed A/B/C certificate verification and idempotent issuance fixtures
  pass with real Ed25519 math. All signers, admissions, worker/evaluator results,
  anchors, measurements and roots in those fixtures are SYNTHETIC/MOCKED. B/C
  fixtures use NativeReceipts/NativeEvidence, NOT a fabricated EvidenceVerdict.
  Report45 covers their introduction; main-agent hardening added complete child
  evaluation governance and negative cases for ACK, approval, metering and terms.
- Real public HTTP routes, demo logins and requester scope checks are tested.
  No production signing provider, keys, native actors or accounts were installed.
  Append-only TEST-SYNTHETIC storage evidence is retained; no evidence deleted.

## Findings resolved during the run
The terminal guard reproduced a real contradictory-outcome gap. Initial regression
then found a stale-response race plus5 tests whose `terminal` matching included the
new worker checkpoint. Fixed the race and distinguished `worker_outcome` from
final control acceptance WITHOUT weakening the original tests. Descriptor holds
exclude copied `_control_command` metadata; canonical writer validation is intact.
The crash harness initially attempted an identity switch and unsupported ledger
filter; those TEST fixtures were corrected, not the identity/ledger guards.

## Still held — not a claim that all non-GPU work depends on GPU
No existing native activation admission records or non-GPU runtime factory/worker
connection descriptor were recovered in this workspace. Available Tigris
credentials are not signer admission, worker admission, or permission to read data.
The new composition is wired into startup but has not been enabled with an actual
admitted native provider. Therefore genuine A/B/C effects, real retrieval, actual
hard-supervisor limit tests and independent-host recovery remain unverified. No
live certificate has been issued.

Indispensable next input: the EXISTING admitted non-GPU runtime/provider descriptor
(or the owning service's connection/credential REFERENCE) and recoverable signed
activation/approval records for this composition. Do not supply replacement GPU
SSH keys, invent another identity store, or install test roots. See the updated
activation_combined_20260927/BINDING_SPEC.md for the exact startup contract.

## Auth-policy scope
Report44 also listed unsolicited login-policy/CORS/seeding recommendations. These
are not introduced native-flow regressions or adopted owner policy: invalid login
attempts returned401, existing logins succeeded, and no five-attempt threshold was
specified for this application. Automatically rewriting existing credentials would
conflict with preserving accounts. No login policy, CORS, seed credentials or auth
store was modified. A separately authorised policy review would be a different task.