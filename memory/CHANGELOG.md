# Akki implementation history

## 2026-09-27 17:33 UTC — owner-requested GPU connection diagnostic

User requested a new GPU connection check and clarification of overall completion.
One real pinned SSH handshake per configured host: BOTH network-reachable and
server identities match; BOTH local client identities fail IDENTITY_PIN_MISMATCH.
Zero key authentication attempts; auth_none only advertised publickey. No login,
channels, commands, workload, key/config/env/identity changes or automatic retries.
Protected-file before/after hashes match. Report46 and timestamped diagnostic
receipts record the result; no connectivity restoration or GPU health asserted.

Offline RCA interpreted without adopting unsupported claims about authorized_keys:
current remote authorisation and original-runtime health are unknown. Do not repin
the mismatched key as remediation. Earlier Sept26 actual auth rejection is not
today's auth result. Safe next step is original admitted key/runtime custody
recovery, not another generated key. All engineering tests remain last verified
565backend/7frontend; no full suite rerun for this read-only connectivity check.

## 2026-09-27 — Native startup, model descriptors, recovery and safe hold reasons

User said to proceed with next actions/backlog/suggestion together. Added explicit
opt-in native startup, bounded async PrincipalV1 lookup and Mkondo revalidation,
same-ledger provider validation and safe runtime configuration endpoint. Model
portal requests recover exact signed descriptors; missing bindings bank a durable
hold, not fake model inputs. Current provider configuration remains absent.

DAP/OS reason/action/history text uses existing owner elements; unknown native
errors sanitised. No source prototype/CSS change. Actual long-objective drawer
verified at1920×800 and390×844 without overflow. All7 frontend tests pass.

Added immutable worker_outcome checkpoint (old marker readable), contradictory
terminal guard, stale reply/view convergence and interrupted-before-view recovery.
Four actual Mongo/new-process crash drills preserve one SYNTHETIC effect/submit/
meter/terminal and stable fence. These are same-host tests, not genuine cross-host.

Testing reports44/45: fixed6 initial regressions without weakening baseline tests;
added full signed B/C LAB positives, then hardened verifier with actual dispatch/
runtime ACKs, full child-evaluation approvals/limits/reservations/terms/settlement,
transitive proof-prefix checks and sum-preserving usage. A/B/C LAB positives use
NativeEvidence/NativeReceipts, not fabricated verifier flags. No live proof issued.

Final: **565 backend pass,2 gated skips,0 failures/errors;7 frontend pass**.
`test_reports/pytest/native_continuation_verified.{xml,log}` (131.853s). Scoped lint
and original frozen hash/shape invariants pass. No GPU/SSH, actual source/model data,
new keys/identities, auth-policy/credential/env changes. Unsolicited auth policy
recommendations in44 were not treated as adopted policy or silently implemented.
Remaining indispensable input is the existing admitted native provider/connection
descriptor and actual signed activation records. Details in native_continuation
RESULT and updated BINDING_SPEC; combined scope does not need reconfirmation.

## 2026-09-27 — Combined activation/control continuation

User reconfirmed autonomous combined controls + real-path scope, GPU/SSH parked.
Implemented signed canonical-Ledger control intake/projections, approval groups,
atomic allocation reservations/settlement, native decision bridge, bounded worker
admission envelope/ACK and worker-side limit helper. Existing EngineAdapter remained
unchanged after regression exposed field drift; explicit subtype owns the extension.

Added concrete certificate signature/native-journal joins, signed certificate
recording only after proof, current revocation/supersession and predeclared script/
snapshot/policy checks. Model consumers enforce grounded anchors/context/refusal,
native protected evaluation of the recorded training artifact, explicit adopted
MOAC mapping, threshold direction and separate release. Legacy training reporting
and close reuse one persisted result; unknown outcomes cannot re-run. Removed
fabricated scores and dummy admission ceremony; unmeasured values remain null.

Testing42/43 exposed/corrected adapter shape drift; additional hardening addressed
late worker admission, wall-clock rollback, final pre-send freshness, native scan
reconciliation, exact approval provenance and re-signed semantic mutations.
Canonical final run: **520 passed,2 gated skips,0 failures/errors**. JUnit/log:
`test_reports/pytest/activation_combined_canonical.{xml,log}`. Native suite includes
actual two-client Mongo CAS under unique TEST-SYNTHETIC tenants, append-only retained.
Full signed Path-A positive test is SYNTHETIC on FAKE ledger; no real source data,
retrieval, model training/evaluation, live issuance, native trust root or worker
installation. Complete native positive B/C chain still unverified.

Recovered local ledger had no activation approvals/allocations/worker admissions.
Four legacy local training records were mock-mode, including one historical
closed_adopted status; preserved unchanged and not promoted to evidence. No auth
credentials/env changes, GPU/SSH action or UI edit. Scoped runtime Python lint and
external desktop UI smoke pass. Existing third-party multipart deprecation only.
Details: `assessment_workspace/notes/activation_combined_20260927/RESULT.md`.

## Historical continuity
The prior699-line PRD is preserved unchanged at
`/app/memory/ARCHIVE_PRD_BEFORE_ACTIVATION_CONTROLS.md`.
It contains the original W1, execution spine, native components, model-handoff,
document review and workspace-provenance history. Detailed evidence remains in
`/app/assessment_workspace/notes/` and `/app/test_reports/`.

## 2026-09-27 — First autonomous activation-control implementation batch

Owner: "Proceed, only blocked issue is GPU/SSH. Rest you are cleared to go".
No further broad questionnaire or blanket ban on non-GPU execution is authorised.
Real activity must still follow admitted authority/custody/budget routes.

Implemented:
- Hash-preserved owner v1.1 artifact bundle and hardened, fingerprinted validation
  profile; real semantic consistency/chronology/purpose/reconciliation checks.
- Server-owned bounded typed evidence-verification boundary. All claims/refs/hash/
  scope/proof categories must verify. Default is unbound and held, never mock-positive.
- Table-driven split crossing controls with CC-1 condition, ceremony/per-call
  binding, masking obligations, unassessed treatment, disclosure/spend refusal and
  canonical normalization of the stale scalar deny row.
- Authenticated `/api/portal/activation/profile` and
  `/api/portal/activation/certificates/validate`; bounded JSON, role/tenant isolation,
  no value leakage and native canonical audit. No certificate/admission issuance.
- Portal work/detail/history joins to canonical execution stream; real coordinator
  stop/retry/result actions, frozen descriptor replay and closed-request guards.
  Result returns rights-admitted handles, with delivery_verified=false.
- Removed fabricated training descriptors from source IDs; model paths require a
  real native descriptor rather than a caller/adapter guess.

Tested and corrected:
- Positive evidence/B/C/API tests exposed field-name and enum inconsistencies with
  owner raw JSON; fixed all reported runtime defects, not the source artifacts.
- Baseline validation assertions added to negatives. Corrected invalid state-test
  expectation and time-dependent replay fixture, preserving runtime safety guards.
- Final all-backend serial run: **451 passed,2 explicitly gated custody/refusal
  drills skipped,0 failures/errors**. Previous transient500s fixed; no failing
  API tests in final run. Source/model/GPU calls were not made.
-9 protected hashes and owner JSON hashes unchanged; UI untouched; shell smoke,
  compile and whitespace checks passed. Existing multipart deprecation warning only.
- Installed jsonschema[format-nongpl]4.26.0 and froze requirements, restarted backend.
  No auth credentials, accounts, environment values or source/GPU settings changed.

Limits: this is tested software, not live activation. Positive proof/worker inputs
are **MOCKED/SYNTHETIC**; positive ledger storage is FAKE. Native signature/receipt/
engine providers, actual limit enforcement, approval integrations, blob delivery,
issuance and real experiments remain to be implemented/proved. Validation audit
records are real control-plane observations, not certificates or grants.

Result: `/app/assessment_workspace/notes/activation_controls_20260927/IMPLEMENTATION_RESULT.md`.
Final JUnit: `/app/test_reports/pytest/pytest_activation_portal_final_full.xml`.
Reports38–41 retained as historical intermediate findings; final evidence supersedes
their current defect status. See ROADMAP.md for next work and honest package status.