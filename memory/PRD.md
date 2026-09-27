# Akki — product requirements and current continuity

## Original problem statement

The user requires the AI to deeply understand, audit and operate the Akki Extraction
platform under strict architectural and governance rules; wire DAP requests, work
history and entitlement lifecycles to actual backend engines; and execute a
dependency-ordered fix plan based on a648-row gap analysis, bridging isolated
components into a continuous governed end-to-end chain with durable evidence.

Product requirements:
- **E1 is NEVER the source-data execution path.** It wires admitted descriptors.
- Evidence-based accounts of what is built, mocked, unbound or actually verified.
- Strict100% UI fidelity to the user's literal HTML prototypes; data wiring only.
- Preserve frozen Canon contracts and single authoritative append-only ledger.
- Architecture testing is distinct from real-element/operational qualification.
- Owner permissions and live results cannot be manufactured from fixtures or chat.

## Current owner instruction and operating boundary

"Proceed, only blocked issue is GPU/SSH. Rest you are cleared to go".
Continue autonomously with all independent implementation/integration/testing and
properly admitted non-GPU activity. Do not impose blanket source/model/credential
work bans. Required authority is a workflow to implement/use, not a reason to stop
all work. No blind GPU retries, key replacement or disturbance of original runtime.
Use English in all communication.

Live Activation v1.3 document review closed. Owner v1.1 certificate schema/crossing
table accepted as final desk-authored inputs; E1 owns versioned hardening, semantic
verification, policy integration and record recovery. No further generic specification
round. Actual unknown policy decisions must be precise, resolved before protected
evaluation; never infer measurements or thresholds after observing results.

Owner rulings to recover/validate in native records (not automatically applied):
scope/expenditure/purpose-specific approval categories, independent required groups,
any-one within each unless ceremony quorum; per-run authority through gate; existing
allocation20 GPU-hours/run and USD0 external; controlled pilot custody, masked
uncontrolled-only frontier crossing, controlled exception unavailable, no disclosure
counterparties; any loosening receipted. File/chat claims do not establish live records.

## Architecture and source of truth

- React frontend + FastAPI + MongoDB. Environment-configured URLs, databases and
  credentials only. Canonical backend imports vendored Akki services.
- Runtime: `/app/backend/vendored/extraction_akki/backend/`.
- Bootstrap: `/app/backend/server.py`.
- Canonical ledger: `services/ledger_writer/{principal_control,mongo_control}.py`.
- Coordinator/ports/native adapters: `services/northena/execution_*.py`.
- Handoff sidecars: `services/mkondo/execution_*.py`, native registry/contract intact.
- Registry/inspection consumer: `services/mtafiti/execution_registry.py`.
- Portal: `routers/portal_requests.py`, `services/portal_operational/`,
  `services/northena/portal_work.py`.
- New activation controls: `services/activation/`, `routers/activation_controls.py`.
- Frontend owner markup: `frontend/src/.../OwnerMarkup.js` and original public
  `prototype/dap_latest.html`, `prototype/v2_os.html`; neither changed this batch.
- Every Mongo response excludes BSON IDs; immutable request identity and canonical
  evidence are preserved. Do not introduce a parallel job/admission/receipt authority.

## Previous implementation checkpoint — 2026-09-27

First autonomous control-plane implementation batch verified. Detailed result:
`assessment_workspace/notes/activation_controls_20260927/IMPLEMENTATION_RESULT.md`.

Implemented: hash-preserved owner policy bundle, versioned/fingerprinted validation
profile, bounded certificate consistency/chronology/reconciliation checks,
server-owned evidence-verification interface, fail-closed table-driven crossing
resolver, authenticated profile/validation APIs with native audit, portal history
and stop/retry/result-reference joins to the same execution coordinator. Immutable
deadline/scope/objective replay enforced; unsafe fabricated training descriptors removed.

New endpoints:
- `GET /api/portal/activation/profile`
- `POST /api/portal/activation/certificates/validate`

No certificate or admission issued by these endpoints. `execution_authorized=false`,
`certificate_issued=false`; output handles do not prove byte delivery
(`delivery_verified=false`). No default fake-positive provider installed.

**Final full backend tests:451 passed,0 failures/errors,2 explicitly gated custody/
identity/refusal drills skipped.** JUnit:
`/app/test_reports/pytest/pytest_activation_portal_final_full.xml`.
Positive signature/worker/inspector/authority verdicts are **MOCKED/SYNTHETIC** and
positive storage FAKE. Real API tests cover auth/scope/refusal and validation-audit
writes, not live source/model operations.9 protected and owner JSON hashes unchanged.

At that checkpoint, not complete: native signature/provenance/ref adapters, durable approval-group and
estate activation joins, runtime dimensional limits/reservations, genuine DQ/worker/
inspection/usage producers, native model descriptor/callable wiring, real training/
evaluation, actual custody delivery, certificate issuance and independent live proof.
See ROADMAP.md. Do not call the typed EvidenceVerdict interface real cryptographic
verification or infer that the14 readiness packages are complete.

## Current checkpoint — 2026-09-27 combined activation continuation

User explicitly reconfirmed the combined scope (controls + real A/B/C proofs), not
separate approval per package. Engineering continued; GPU/SSH remained untouched.
**Control-plane batch verified; the complete live-path scope is NOT complete.**

Implemented and tested:
- Signed native control-receipt consumer using existing Watch Ed25519 verification
  primitive and canonical Ledger. Admitted signer/key/permissions must resolve from
  a SERVER-OWNED native admission bridge. No keys, accounts or trust roots installed.
- Frozen activation plans with owner `inputs.dial_versions` / `inputs.policy_versions`
  mappings, script/input commitments, independent approval groups/quorum/current
  decisions/revocation, allocation and already-admitted worker attestations.
- Native ComponentAuthority decision join and SAME-ledger atomic reservations with
  compare-and-append; unknown usage remains reserved; signed terminal reconciliation
  preserves overruns. Real two-client Mongo CAS tested in isolated SYNTHETIC tenants.
- Explicit BoundedEngineAdapter, pre-send signed runtime-limit ACK, operation/fence
  binding, bounded metadata calls, worker-side counter/deadline helper including
  termination and late-admission/wall-clock-rollback checks. The helper is NOT an
  installed remote hard supervisor or proof that a real workload was terminated.
- Concrete certificate verification joins for signatures, request/objective,
  native approvals/policies/registry/usage/reservation/termination, independent
  evidence, predeclared acceptance, prefix chronology and supersession. Recording
  an already signed certificate is proof-gated; E1 never signs as the owner.
- Model-proof consumers require anchored skill/context/refusal evidence and a
  separate completed native evaluation consuming the trained artifact, predeclared
  six-criterion mapping/thresholds/protected split and distinct release decision.
- Legacy training now captures one write-once effect/result; emit and close reuse
  it, uncertain/historical outcomes cannot silently retrain. Missing MOAC evaluation
  values are null / `not_measured`; no fabricated zero scores or automatic dummy
  admission ceremony. Mocked close produces no chargeable metering receipt.

New metadata endpoints under `/api/portal/activation`: `/receipts`, `/readiness`,
`/reservations/settle`, `/certificates/issue`. Existing profile/validate remain
diagnostics; current issuance endpoint holds with no admitted signer bridge.

**Canonical regression: 520 passed, 2 explicitly gated custody drills skipped,
0 failures/errors** (`test_reports/pytest/activation_combined_canonical.xml`).
Testing reports42/43, protected-hash checks, unchanged UI desktop smoke and scoped
Python lint pass. Original EngineAdapter contract preserved; extension is a subtype.
No auth credentials, .env settings, original GPU/SSH runtime or frontend files changed.

Evidence limits: full signed Path-A verification/issuance positive is SYNTHETIC on
FAKE ledger, not real source/retrieval proof. Signature math is real but signer
admissions, worker/evaluator observations and trainer test effects are **MOCKED /
SYNTHETIC**. Mongo concurrency alone is real storage evidence. No live certificate
issued; no complete native positive B/C chain tested. No real worker installed.

Recovery: initial real control ledger had DAP/execution-request/portal-view and
validation-audit events, **no activation approvals, allocations or worker records**.
Legacy local runner metadata contained4 mock-mode records (3 closed_rejected,
1 historical closed_adopted); no historical row was rewritten or treated as live.
This finding is local to this composition, not proof the original estate is offline.

Current binding gap: `activation_receipts`/admitted-key resolver, real worker RPCs,
native inspector/eligibility and model query transports are not installed in app
startup. `services.activation.composition.native_activation_bindings` is an explicit
composition factory, NOT a running integration. Do not replace missing native
admissions with fixture roots. Preserve ordinary auth and PrincipalV1 architecture.
Detailed result and required interfaces:
`assessment_workspace/notes/activation_combined_20260927/{RESULT,BINDING_SPEC}.md`.

## Workspace versus original live Akki

Owner reports original runtime live on amazing-gates-8. Current configured workspace
is pensive-goodall-6 and uses local credentials/vendored code, not inherited sessions.
Read-only comparison: `notes/workspace_repo_connection_review/REVIEW.md` under
assessment_workspace. Git origin is Akki-OS-Root; remote read failed, so latest owner
push NOT verified. The apparent Extraction-Akki directory has no own backend/git.
Local key/receipt file presence is not proof of authorisation or connection.
Original real-training records are historical; current original health unobserved.
Current unbound findings concern this new activation composition, not a claim that
the entire original estate is mocked/disconnected. No new GPU/SSH action performed.

## Continuity and next work

- `CHANGELOG.md`: implemented changes/testing, with links to durable evidence.
- `ROADMAP.md`: R01–R14 progress, next slice, P1/P2 backlog.
- `ARCHIVE_PRD_BEFORE_ACTIVATION_CONTROLS.md`: complete previous699-line record.
- Original fix plan: `assessment_workspace/notes/consolidated_fix_plan_20260926/`.
- Owner artifacts/review: `notes/live_activation_v1_3_artifact_review/revision_v1_1/`.
- Readiness register: `notes/live_activation_v1_3_readiness/READINESS_REGISTER.md`.
- Existing auth credentials: `/app/memory/test_credentials.md`; unchanged this batch.

Next engineering: recover/bind actual estate admission/key provenance and non-GPU
worker/inspector/eligibility interfaces into the implemented composition. Complete
native callable/model descriptor and measured proof producers; obtain real bounded
A→B→C acceptance wherever an admitted route exists. GPU-dependent execution alone
stays parked. Freeze before effects; issue only after independently verified proof.