# Akki implementation history

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