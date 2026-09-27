# Activation controls and portal execution joins — first implementation batch

Date: 2026-09-27. Owner authorised autonomous work: **"Proceed, only blocked issue
is GPU/SSH. Rest you are cleared to go"**. Only GPU/SSH work is explicitly parked.
Other implementation and admitted non-GPU activity are authorised to progress;
ordinary permission/custody/evidence gates are requirements, not blanket task bans.

## Result and scope

**Implemented and verified the first control-plane batch. Not full live activation.**

1. Owner v1.1 schema/policy custody copies bundled unchanged with hash checks.
   Hardened versioned validation profile; profile and implementation fingerprints
   accompany every validation result/audit. No schema/proof fetched from user URLs.
2. Executable certificate consistency checks: bounded closed metadata; correct
   owner fields/enums; stage/state guards; exact counts and re-performance
   reconciliation; chronology; purpose/scope; six distinct criteria; approval
   group/voter separation; admission prerequisites; limit and reservation assertions.
3. A bounded server-owned evidence verification port: certificate/scope digest
   binding; typed immutable verdict revalidation; all proof categories; complete
   reference coverage; expiry (including elapsed RPC time); explicit finite timeout;
   measured-mode requirement; no caller-injected verifier or trusted booleans.
4. Table-driven crossing resolver: split subdials; immutable policy version; pilot
   controlled exception remains unavailable; explicit estate/class ceremony and
   request-bound per-call authority; CC-1 entity-knowledge objective; masking
   obligations; preserved unassessed status; disclosure/spend checks; exact Decimal
   cost comparison; deny by default. Old scalar catch-all is normalized to canonical
   all-class refusal, not used to widen either independent permission.
5. Authenticated APIs:
   - `GET /api/portal/activation/profile`
   - `POST /api/portal/activation/certificates/validate`
   Existing portal scope/roles are reused; source metadata only. A native canonical
   ledger observation records the assessment and fingerprints, not a certificate,
   admission or signature. `execution_authorized=false` and
   `certificate_issued=false`. Production without an evidence provider honestly holds.
6. Canonical execution stream joined to scoped DAP detail/list/history. Source
   dispatch/running/uncertain/terminal/held observations become user-facing states;
   outputs/commercial snapshots/worker details are not leaked in history.
7. Stop invokes actual coordinator cancellation and reports Stopped only when
   confirmed. Retry resumes the recorded non-terminal Interrupted request under
   the same immutable identity; post-send uncertainty stays status-only. Result
   invokes fresh rights/registry gates and returns only admitted artifact references.
   `delivery_verified=false`: this is NOT downstream byte-delivery or Retrieved proof.
8. Portal advance reuses the durable request snapshot; deadline/objective/scope
   mutation refuses. Closed requests cannot silently recommission. Removed the
   unsafe shortcut constructing training requests from source IDs. Model/skill/eval
   descriptors still need their proper admitted native builder join; already recorded
   matching descriptors can be resumed, never reconstructed by guessing.

## Important qualification: what the evidence layer does and does not do

The consistency checker and fail-closed evidence interface are real executable code.
The **native signature/provenance/reference adapters are not yet implemented/bound**.
An async trusted provider must actually resolve immutable native records, validate
signatures, current rights, measurements, independent evaluation and all claims.
No provider is installed by default; no fake-positive provider was added to production.

Thus this batch does NOT implement real cryptographic/evidence verification merely
by defining `EvidenceVerdict`, and does NOT issue live activation certificates.
Positive verdict/worker/inspector/authority fixtures are **SYNTHETIC/MOCKED** with
FAKE ledger storage in positive/fault tests. Real authenticated API tests exercised
metadata validation, scope refusal and actual canonical validation-audit writes.
Those audit writes are not live workload or certificate evidence.

CrossingContext is server-owned metadata only; no endpoint accepts a browser's
CrossingContext as authority. Resolver `allowed=true` means policy obligations are
resolved for those verified-shaped facts, not execution permission. It always
returns `execution_authorized=false`; actual grants and masking/receipts must be
enforced when the production crossing is integrated.

## Files and implementation boundaries

Runtime base: `/app/backend/vendored/extraction_akki/backend/`.
- `services/activation/{models,schema,chronology,semantics,evidence,validation,crossing}.py`
- `services/activation/policies/owner_certificate_v1_1.json`
- `services/activation/policies/owner_crossing_v1_1.json`
- `routers/activation_controls.py`; registered in `/app/backend/server.py`
- `services/portal_operational/{execution_records,execution,actions}.py`
- `services/northena/portal_work.py`; `routers/portal_requests.py`

No frozen Principal/Licence/Catalogue/Handoff/Mtafiti/ledger-control contract changes.
No frontend files or owner prototypes changed. No credentials/accounts changed.
`jsonschema[format-nongpl]==4.26.0` installed using pip, requirements frozen; backend
restarted for dependency installation. Native date-time format validation is present.
No GPU/SSH, source-data or real model/training/evaluation calls during this batch.

## Verification and corrective history

- Iteration38:75 RED cases created for new modules.
- Initial75 control tests and227 prior scoped regressions passed, but positive
  verification later exposed inadequate owner-shape fixture coverage. These earlier
  totals are historical runs, not sufficient final semantic acceptance.
- Iteration39: real owner-shaped positives found erroneous principal-field access.
  Fixed scope to actual `identity.tenant_id`; actor comes from authenticated scope
  and the server proof result, not an invented caller-supplied principal field.
- Added valid-baseline assertions before negative mutation tests to prevent a
  malformed fixture from falsely proving all later guards.
- Iteration40:14 native portal lifecycle cases passed. RCA identified incorrect
  input/heldout/prerequisite field assumptions; corrected to actual raw owner JSON
  (`custody_classes_in_scope`, `fixed_before_training_at`, prerequisite `outcome`).
  Prerequisite timestamps are resolved from receipts, not invented envelope fields.
- Iteration41: populated positive B/C shapes exercised heldout and prerequisites.
  C passed; B exposed an incompatible hardening literal. Fixed to the owner enum
  `out_of_scope_question` and added a startup compatibility check.
- A test requiring a later state check was itself invalid under the owner's earlier
  shape guard. Corrected the assertion, not the guard. Test replay also recomputed a
  deadline across a second boundary; fixed the fixture to reuse the frozen deadline.
  Unknown fixture principals now refuse instead of mapping every ID to its org.
- Transient earlier503 responses coincided with WatchFiles reloads while code/tests
  were written. Final stable serial run had no500/503 failures; no service policy was
  weakened to hide them.

**Final full backend run:**453 collected, **451 passed,0 failed,0 errors,2 skipped**.
The two skips are explicit custody/identity/preflight/production-refusal drills,
left unauthorised in keeping with the parked GPU/SSH boundary. All15 census HTTP
tests previously skipped for missing test-process URL were enabled by exporting the
existing frontend environment, not by modifying it.

Evidence:
- `/app/test_reports/pytest/pytest_activation_portal_final_full.xml`
  SHA256 `c28b5e1807c38b7324d8382363975a5ec1435ac379f777338804e65505b9f309`.
- `/app/test_reports/activation_portal_final_full.log`
- `/app/test_reports/iteration_38.json` through `iteration_41.json` retain original
  findings; final run supersedes their open runtime defect status for this batch.
- Existing DAP desktop shell smoke passed. No new visual-acceptance claim or UI change.
- Python compilation and diff whitespace checks pass; existing multipart dependency
  deprecation warning is not a new functional failure.
- Nine protected hashes unchanged, including both literal owner prototypes.
- Owner schema runtime copy unchanged:
  `ad848bd95e76dcf4ef71cd0e0688914632de33e68ceb4168e7ede4209ad256d2`.
- Owner crossing runtime copy unchanged:
  `472b6369ef7059f9b451504e329605f02a8918081dbf3d5438239853ba6c8830`.

## What remains and next engineering order

- **R01/R02:** recover effective estate/group/dial records; native durable multi-group
  approval and activation-envelope assembly. No automatic pilot admission/registry
  updates were performed based on messages or file `pilot_setting` values.
- **R04:** enforce R-47 in the actual runtime and reserve/reconcile allocation across
  concurrent requests. Declaration checks do not enforce a worker's budget/deadline.
- **R05/R06/R11/R12/R13:** genuine DQ, mandate/ACK, worker, inspector, measurement and
  signature/native-receipt adapters; certificate issuer and revalidation projections.
- **R03/R07/R08/R09/R10:** complete native model/skill/eval descriptor and callable
  endpoint joins, actual admitted source/skill/training/evaluation proof, protected
  real evaluation and actual blob custody/delivery. Legacy duplicate-training and
  synthetic MOAC paths remain identified fixes; do not enable them as live switches.
- **R14:** real-store/worker restart and independent re-performance evidence. Archive
  test success is not a substitute for live effects, measured outcomes or separation.

Only GPU/SSH is categorically parked. Other engineering and properly admitted
non-GPU operations proceed; surface actual dependencies precisely instead of imposing
another blanket ban. Continue from the current workspace; latest remote Git push
was not accessible in the preceding read-only comparison. Preserve original live
Akki instance and its identity; this workspace is not automatically that runtime.