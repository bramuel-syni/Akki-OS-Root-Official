# Live Activation v1.3 — implementation and operational readiness register

Assessment recorded: 2026-09-27 UTC. Governing document reviewed: owner's
Live_Activation_v1_3.docx, internally dated 28 September 2026.
SHA256: `76e83dc251ac5b1e9c005f6afe04358868f919c8e1c779626bcf019f895edc4e`.

## Scope and verdict

User requested outstanding operational readiness and implementation aspects, then
approved a read-only assessment: **"Except GPU, procceed"**. GPU work is excluded.
No runtime/source/model/worker calls, credentials, database queries, workload
execution, configuration changes or application edits were made. Only assessment
documents and continuity notes were written. No GPU diagnostic or retry performed.

**Document-review gaps are closed; implementation and live-proof gaps are not.**
For the three DAP→execution-spine activation paths, the supported status is
**IMPLEMENTED architecture / NOT LIVE-VERIFIED**, not PARTIALLY LIVE. Production
bindings default to unbound/held; successful architecture tests use SYNTHETIC /
MOCKED upstream receipts and FAKE storage. There is no basis to substitute test
success for a v1.3 activation certificate. This does not assert that every unrelated
legacy operation across the entire platform has never performed real work.

The most important distinction: this is **not just a credential/configuration
problem**. There are missing joins, live producers, new policy consumers and
operational acceptance proofs. Working access alone would not close them.

## Evidence method and limits

- Read current Python routes, services and contracts; searched runtime/frontend
  source for binding registration and v1.3 certificate/state identifiers.
- Re-read prior component/handoff results and original v1.3 document custody copy.
- Rechecked both existing final JUnit reports: **227 tests, zero errors, failures
  or skips in each**. These are earlier runs, **not tests rerun in this assessment**.
- Rehashed all nine files pinned by the model-handoff suite: all unchanged,
  including the two literal owner prototypes.
- No dynamic inspection of current users, licences, estate records, storage mounts
  or worker availability. Those must be recovered and validated by the activation
  dossier, not assumed present or absent from this static review.
- Negative search findings below are scoped to the traced activation integration;
  they are not claims that no reusable policy/kernel exists anywhere in the repo.

All abbreviated runtime paths below are relative to
`/app/backend/vendored/extraction_akki/backend/`.

## What is already real and reusable

1. Durable coordinator/journal, frozen request identity, ledger ordering,
   dispatch reservation, send/cancel arbitration, conservative post-send recovery.
2. Native principal/licence/catalogue adapters, historical commercial snapshots,
   native metered-event consumer, registry writer and rebuildable projections.
3. Purpose-bound eligibility consumer, receiver/ACK sidecars, native Mkondo
   registration/attestation and metadata-only delivery validation.
4. Source/skill/training/evaluation descriptor builders; refusal, expiry,
   tampering, withdrawal, restart and interleaving architecture tests.
5. Tenant/principal-scoped portal request/history surfaces with honest held states.

These are implemented mechanisms. The live facts they consume are not thereby
established; `evidence_mode="measured"` is a typed declaration, not independent
verification that a remote measurement or mandate actually exists.

## Prioritized register

**P0** means required for the applicable first live certificate, not that every
row must finish before independent work can begin. **E** = engineering; **O** =
owner gate decision if no valid recorded authority exists; **X** = external estate
operator/custodian evidence. Existing records must be recovered before any O/X ask.

### R01 — Activation envelope, estate dials and effective policy [P0, E; O conditionally]

**Status:** v1.3 is specified, not integrated as an activation contract.
`execution_models.py:28–38` contains a deadline, input/scope refs and optional skill
floor, not the four dial versions, effective per-dimension limits or separate
execution/release decisions. Scoped search found no v1.3 activation-certificate
implementation. Existing custody contracts are not absent; their new composition is.

**Work:** Add versioned sidecar/envelope and canonical event bindings for the
activation dossier, estate policy/dials, immutable objective and limit resolution.
Reuse existing admission/custody authorities; do not edit frozen Canon schemas or
create a competing registry. Map LA-1–20/S-36/R-47 to implementation and tests.

**Closure:** An assembled request cites each recovered record, resolved default,
binding ceiling and policy version; missing authority/dial or forbidden widening
holds. No caller flag or licence-only classification can grant access.

### R02 — Real controlled-request approval → operation authority [P0, E; O conditionally]

**Status:** Approval kernels exist but the traced portal chain is not joined.
`northena/portal_work.py:46–74` always banks `ADMISSION_UNRESOLVED` at routing.
`dap/approval.py:65–67` stores routing/decision/standing grants in process memory;
its single-authority kernel is not a durable multi-group activation workflow.
`execution_authority.py:54–62` requires an unbound `decisions.resolve` producer.
The existing team approval surface serves checker/source/key-grant queues
(`routers/team.py:104–175,292+`), not this complete v1.3 path.

**Work:** Join the existing DAP approval mechanism to the same frozen activation
request and canonical ledger. Resolve required scope/expenditure/purpose groups,
any-one/quorum within groups, expiry, standing-scope checks and revocation. Rehydrate
admitted sender/receiver/org contexts from authoritative records after restart.
Principal store `principal_store/store.py:5–28` is an in-process consumer, not by
itself proof of that durable admission bridge.

**Closure:** A controlled portal request reaches all correct groups; decisions
survive restart and produce a request-bound authority receipt consumed before send.
Pending, expired, wrong-group and widened-scope requests cannot execute. Owner
permission is a gate receipt, not a message or synthetic principal seed.

### R03 — Complete portal ↔ execution-spine lifecycle [P0, E]

**Status:** Public integration remains incomplete despite direct-core tests.
`portal_operational/execution.py:17–30` maps only four operation labels; training
is built from source handles rather than the full recipe/model/corpus/MOAC builders.
Other operations return409. There is no skill/evaluation builder join in that adapter.
`portal_work.project:26–43` reads DAP events, not completed execution-flow events.
`portal_operational/actions.py:7–27` refuses stop/retry/result rather than calling
the newly implemented coordinator cancellation/retrieval path.

**Work:** Resolve proper operation-specific descriptors and join job progress,
history, cancellation, approved retries and rights-gated retrieval to the existing
spine. Use the existing orchestrator's progress consumption; no E1 polling loop.
Preserve the original UI markup and information-disclosure rules.

**Closure:** One actual approved request stays the same request across routing,
execution, usage, result, retrieval, stop/retry and history. A direct `RunView.ready`
does not leave the portal stuck at routing or fabricate a retrieved result.

### R04 — R-47 limit enforcement and spend reservation [P0, E; O conditionally]

**Status:** Existing deadline checks and RPC timeouts are useful, but insufficient.
`portal_operational/execution.py:12–14` accepts only `deadline_epoch`.
`execution_models.py:28–38` does not carry the dimensional enforcement envelope.
`execution_send.py:19–42` checks authority/commercial freshness and pre-send expiry;
it is not scan/byte/media/spend enforcement during actual execution.
`execution_ports.py:24–36,46–58` bounds worker RPC waits, not remote job duration.

**Work:** Resolve and bank per-dimension limits at assembly; separate replaceable
estate defaults from binding ceilings. Reserve spend atomically across concurrent
runs. Enforce source scans/records/bytes, applicable compute/media dimensions and
inclusive termination deadline inside the admitted runtime. Bound operation
decision/inspection calls too: `execution_authority.py:58` and
`mtafiti/execution_registry.py:34` currently await those providers directly.

**Closure:** Worker receipts demonstrate actual boundaries were obeyed, including
termination within the ceiling. Concurrent requests cannot oversubscribe the
reservation. Missing spend authority or unenforceable ceiling holds before effect.
Cancelling an RPC alone never counts as stopping the remote operation.

### R05 — Genuine material eligibility and classification [P0, E; O if genuinely unruled]

**Status:** `execution_eligibility.py:14–26,34–72` validates and pins receipts; it
does not perform DQ checks. Missing provider holds. Source kind bypasses this
model-input gate (`44–45`), which does NOT establish that source extraction is safe
or Clean. Training's legacy admit uses caller-supplied qualification bits
(`training_runner/runner.py:52–98`), not a substitute for current measured evidence.

**Work:** Bind effective approved packs/policies to actual admitted snapshots and
emit purpose-specific eligibility from real checks. Apply source exclusion and
unknown/stale classification treatment separately. Trace any unresolved DQ/closed
MOAC mappings against existing rulings; do not invent pack thresholds or new classes.

**Closure:** Same exact inputs/purpose/policy produce independently traceable
decisions; unsupported inputs are unassessed/held. Withdrawal blocks send/release
without erasing real consumed usage. Licence/rights and custody stay separate.

### R06 — Production bindings and authentic receiver crossing [P0, E; X conditionally]

**Status:** `execution_bindings.py:45–65` defaults to no decision producer, no worker
mapping, no inspector, unbound eligibility and `UnboundHandoff`.
`routers/portal_requests.py:61` reads optional `app.state.execution_bindings`;
scoped production search found no assignment registering a live bundle.
`mkondo/execution_handoff.py:34–51,69–93` verifies typed bindings/ACKs from an
injected producer, not remote identity/custody by itself.

**Work:** Supply server-owned concrete providers from admitted engines, not public
callback registration. Verify receiver mandate, custody, authentication and receipt
provenance; make the actual receiver resolve canonical envelope/ACK/send references.
Implement receiver-side stable-key/fence/replay, status and cancellation behavior.

**Closure:** Genuine distinct receiver acknowledges the real contract; delivery
occurs after committed send. Invalid identities, forged ACKs and wrong executor
results refuse. Restart ambiguity reconciles status without blind resubmission.
No production fixture factories, mock-mode switches or self-asserted grants.

### R07 — Path A: bounded source execution and unit registration [P0 for A, E; O/X conditionally]

**Status:** A real-shaped census runner exists, separately from the new spine.
`census_autonomy/operational_runner.py:25–84` checks descriptor/scope/admission,
dispatches through its existing seam and persists validated result receipts.
`execution_builders.py:11–23` constructs a source descriptor but is not execution.
No v1.3 composed live source→registry→retrieval proof was identified in the reviewed
activation evidence. Census completion must not be widened into extraction rights.

**Work:** Compose the admitted existing source runner with the canonical coordinator,
R-47 enforcement, exact source snapshot/units, real usage, inspector and retrieval.
Resolve source credentials only by custody reference inside the admitted runtime.
Validate source exclusions and unit re-extraction handles; no E1 source reads.

**Closure:** Actual bounded approved read; reconciliation manifest identifies read,
excluded and failed units; registered artifacts and measured usage precede a real
authorised portal retrieval. A connection/heartbeat/census estimate is insufficient.

### R08 — Path B: actual grounded callable skill [P0 for B, E; O/X conditionally]

**Status:** Public query still deliberately refuses.
`routers/transform_forms.py:88–92` calls `refuse_unadmitted`;
`portal_operational/skill_query.py:20–32` returns `SKILL_EXECUTOR_UNADMITTED`.
`execution_builders.py:26–40` freezes provisioning/query identity, not retrieval
or model execution. No actual answer is produced by this endpoint today.

**Work:** Join admitted provisioning/key scope, frozen corpus and admitted model to
the real retrieval/invocation path. Implement anchor verification, floor/refusal,
context-loss disclosure and genuine query-reference custody. Preserve sole governed
crossing and recorded model/receiver identity; no mock answer fallback.

**Closure:** In-scope query yields a real anchored answer and measured usage;
out-of-scope query yields a durable genuine refusal. Revoked provisioning/corpus
rights prevent use. Smoke proof is not full skill qualification.

### R09 — Path C: training effect and artifact lineage [P0 for C, E; O/X conditionally]

**Status:** Training descriptors/orchestrators and adoption gates exist, but the
new production composition has no concrete training adapter.
Important legacy issue: `training_runner/runner.py:212–225` invokes the training
seam, and `emit_moac_for_run:229–239` invokes it again to obtain measurement inputs.
These are two call sites, not verified reuse of a committed result. No execution
was attempted in this assessment, and duplicate remote effects are not asserted.

**Work:** Commission the adopted base/recipe and exact eligible corpus once; persist
the actual immutable worker result and inspectable adapter. Evaluation and reporting
must consume that result rather than re-launching training. Bind the existing
trainer through the stable operation-key/fence protocol and accurate metering.

**Closure:** One bounded authorised training effect yields a real hashed adapter
with resolved lineage. Retry/reporting/evaluation cannot repeat training implicitly.
Release remains governed by separate acceptance, not successful process exit.

### R10 — Path C: real evaluation, protected split and acceptance mapping [P0 for C, E; O/X conditionally]

**Status:** Legacy evaluation cannot be made real merely by changing a mode flag.
`training_runner/moac_emitter.py:59–106` hardcodes robustness/refusal-honesty to
false/0.0 and uses mock-labelled thresholds. The admission translation in
`training_runner/runner.py:303–343` constructs synthetic0.0/999.0 measurements and
mock floors. This is safely rejecting scaffolding, not a real evaluation producer.
`training/test_set_seal.py:8–16` describes a seal over source/table/strata/count/
connection-record timestamp; that metadata hash alone does not demonstrate protected
held-out unit identities, split isolation or independent control.

**Work:** Implement all real probes under the adopted six-criterion mapping;
preserve exact versions, thresholds and measurement methods. Seal actual unit
membership/content snapshots using the adopted split protocol. Bind separate
evaluation/re-performance identities and custody. Add only adopted domain release
prerequisites, separately from frozen MOAC fields.

**Closure:** Independently reproducible per-unit measurements, protected holdout,
every criterion outcome and a real refused commission test. Failed/unknown stays
failed/unknown, not fabricated zero as measurement. Successful activation may
legitimately produce a rejected model; release decision remains separate.

### R11 — Actual artifact inspection, custody and retrieval [P0, E; X conditionally]

**Status:** Native registry validation/projection is implemented.
`mtafiti/execution_registry.py:21–79` requires an unbound inspector and checks the
returned metadata. `81–91` revalidates at retrieval. This does not itself read and
hash real artifacts in their admitted storage or demonstrate custody enforcement.

**Work:** Bind an admitted independent inspector and actual storage/custody resolver.
Verify bytes/hashes/manifests and re-extraction handles without bringing source data
into the implementation workspace. Join real authorised retrieval and its receipt
to the portal, with retention/residency/disclosure/rights rechecks.

**Closure:** Mutation, disappearance, ownership mismatch and revoked rights refuse;
genuine stored output is actually retrieved by an authorised principal. An `akki://`
handle returned from a synthetic fixture is not delivery evidence.

### R12 — Measured usage and budget reconciliation [P0, E; O/X conditionally]

**Status:** `execution_usage.py:17–98` validates and banks supplied worker quantities
under pinned commercial terms. `execution_completion.py:7–18,42–58` orders metering
before ready publication and retains consumed usage on an output hold. Those are
real consumers, not measurement producers. Source usage deliberately avoids
inventing a model price (`execution_usage.py:49–54`).

**Work:** Obtain genuine runtime/provider counters with recorded units and provenance;
reconcile them against reserved spend and terms. Include failed/cancelled/partial
work honestly. Keep actual zero distinct from unavailable measurement. Do not
interpret non-model-consumption-only as free execution.

**Closure:** Receipt quantities reconcile with actual work and allowed charges;
concurrent runs cannot overspend; replay does not duplicate usage; post-effect
revocation does not erase already-consumed work.

### R13 — Activation certificates and truthful operational state [P0, E]

**Status:** No v1.3 certificate issuer/verifier/revalidation composition was found
in the traced runtime. `execution_models.py:104–116` defines execution phases and
computes `execution_verified = ready && measured`; that is not an LA-11/15/13
certificate, independent re-performance or proof of actual user retrieval.

**Work:** Implement the versioned certificate contract, evidence-manifest bindings,
issuer/verifier checks, claim-register linkage and append-only supersession.
Record execution permission separately from release acceptance. Derive IMPLEMENTED,
LIVE-VERIFIED, LIVE-BLOCKED and PARTIALLY LIVE from actual certificate evidence and
dependency modes, not UI labels. Bind current input/model/receiver/policy/dial state.

**Closure:** Missing/mock/mismatched evidence prevents certification; changed binding
or revoked authority blocks current use without rewriting historical evidence. A
rejected artifact can still evidence a genuinely live evaluation path. Preserve UI
prototypes; do not relabel the old `ready` flag as live certification.

### R14 — Actual durability, independent re-performance and failure drills [P0 scoped proof, E/X]

**Status:** Archived227 architecture/regression tests pass, but positive fault and
concurrency suites use FAKE ledger storage and synthetic producers. Native ledger
kernels run in those tests; that does not establish real-store restart recovery,
independent control boundaries or downstream worker behavior.

**Work:** Run staged integration acceptance on admitted storage/control facilities,
including restart at envelope/ACK/send boundaries, actual projection restoration,
cancel races, uncertainty reconciliation, revocation, retrieval and independent
seeded re-performance. Keep real-runtime evidence separate from fixture tests.

**Closure:** Durable chain and measured outcomes survive actual restart and agree
with receiver/storage observations. No second canonical writer, no duplicate
effect/usage claim and no shared-workspace independence claim. Broader disaster
recovery/hardware performance remains separately scoped, not a fabricated prerequisite
completion bundled into one small activation.

## Requirement coverage index (not a completion claim)

| Requirement | Work packages |
|---|---|
| LA-1, LA-2 | R01, R02, R14: evidence-source ownership, existing-record recovery |
| LA-3, LA-4, LA-5 | R01, R02, R03, R05: per-purpose multi-group authority |
| LA-6 | R07, R11, R12, R14: source proof and no implementation-workspace data path |
| LA-7 | R06, R08, R11, R12: skill retrieval/invocation/ACK/refusal |
| LA-8 | R09, R10, R11, R12: real training/evaluation, no automatic model admission |
| LA-9 | R01, R06, R07, R11: custody references and actual admitted runtime |
| LA-10, LA-16, R-47 | R01, R04, R12: bound dimensions/reservation/termination |
| LA-11, LA-12 | R03, R07–R14: manifests, receipts, actual retrieval/re-performance |
| LA-13, LA-15, S-36 | R13, R14: certificate and truthful operational claims |
| LA-14 | R01, R02, R05, R08, R11: estate dials/custody/crossing/disclosure |
| LA-17 | R10: real protected protocol-appropriate split |
| LA-18, LA-20 | R01, R02, R09, R10, R13: execution/release separation |
| LA-19 | R05, R07, R08, R11: unknown classification/rights not inferred |

## Engineering order — no new broad questionnaire

1. **Shared control-plane slice:** R01/R02/R03/R04; authority/admission recovery,
   versioned activation contract and limits, all required approval groups, correct
   operation descriptors, full portal lifecycle. Begin R13 certificate contract/tests
   in parallel; do not issue successful certificates before proof exists.
2. **Evidence producers and crossings:** R05/R06/R11/R12; real quality/mandate/ACK/
   inspector/measurement producer interfaces and integrations, inside admitted
   runtimes. No bypass for missing records; no substitution of fixtures.
3. **Path A:** R07 plus actual bounded source/registry/retrieval proof. Distinguish
   census from material extraction; dependent model uses need their own authority.
4. **Path B:** R08 over a suitable, permitted frozen corpus; real answer/refusal.
5. **Path C:** R09/R10; capture one training result, protected evaluation and separate
   release decision. Training and evaluation implementation can progress independently
   of when an actual run can be authorised and performed.
6. **Certification and operational acceptance:** R13/R14 for each bounded path,
   independently evidenced. No blanket whole-platform or all-sector readiness claim.

## Which missing inputs genuinely belong outside engineering?

Only after recovery of existing records:
- **Owner gate decisions:** actual named approval groups; permitted purpose/scope;
  spend/custody/dial change; applicable unresolved policy/threshold adoption. Route
  operation authority through the gate, not chat. Do not ask owner to supply results.
- **Estate operator/custodian evidence:** source snapshot/custody accessibility,
  admitted receiver/storage endpoints and protected evaluator/holdout arrangements.
  A statement of accessibility is not substituted for a verified runtime receipt.
- **Engineering responsibility:** every implementation/integration item above,
  dossier assembly, record recovery, proposed compatible descriptors, authentic
  producer wiring, tests, reconciliation and certificates.

The earlier decision register remains a source-reconciliation checklist, not a
blanket request to answer all old EX/DQ/CC questions again. v1.3 resolves several
policy distinctions; bring back only genuinely unresolved applicable decisions.

GPU readiness is deliberately excluded. It is neither investigated here nor used
to excuse the independent non-GPU engineering work listed above.

## Verification record

Archived JUnit reviewed (not rerun):
- `test_reports/pytest/pytest_model_handoff_final_20260927.xml`,227/0/0/0;
  SHA256 `32e17be8bd73001e5c4ee367303db36dd6d4e600963b5c32e73c52df100c9ce8`.
- `test_reports/pytest/pytest_model_handoff_final_serial_20260927.xml`,227/0/0/0;
  SHA256 `61c8d00f24818575e8a941d9e22d344899306931728650730283f4de1df066c2`.
Nine protected hashes rechecked unchanged during this assessment.
No live integration test, account change, provider call or operational success
claim was made. Readiness gaps are surfaced, **not fixed by this assessment**.