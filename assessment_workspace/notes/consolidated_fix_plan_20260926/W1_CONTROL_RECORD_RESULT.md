# First autonomous W1 slice — bounded result, 2026-09-26

**Verified scope:** two prospective control-record producers and two read families,
not full principal admission, all of W1, or real workload execution.

## What changed

- Added immutable request attribution with a request-lifetime lease; derive the
  Ledger actor through the sealed propagated-principal binding. Absent, mismatched,
  substituted and expired copied context cannot authorize these writes.
- Reused the existing canonical Mongo writer behind a before-insert scope guard;
  no edits to sealed principal, Ledger schema, emitter/writer/verifier or raw writer.
- Added full tenant-prefix validation before the two read families and prospective
  appends. Individual valid row hashes no longer suffice when links/sequence fail.
- Bound new command identity into the hash-covered payload; duplicate commands
  cannot silently change actor/run/type/intent. Historical records remain untouched.
- Wired existing DAP submit, skill refusal, shared work history and entitlement
  projections. Existing account membership still allows only the pre-existing held
  commissioning slice; no admission, approval, price or licence was fabricated.

## Evidence

Contract/source boundaries are in `W1_CONTROL_RECORD_CONTRACT.md`. Tests were written
and run RED before code: 4pass/10fail. A mistaken always-current source pin was
corrected before implementation to pin immutable pre-change evidence, not forbid
the authorized producer edits; protected kernel/prototype pins never changed.

Final scoped suite: **77 passed / 0 failed / 0 skipped**, including real API held
commission/replay/concurrency/denials and MOCKED fault/positive entitlement/skill
fixtures. JUnit: `test_reports/pytest/pytest_portal_operational_with_supplemental_iteration23.xml`.
This is not a full backend baseline or real executor success test.

Original UI unchanged. Checker desktop/mobile flows passed. Its mobile overlay
finding was reconciled against the literal modal backdrop in the prototype:
the explicit close restores navigation as intended. Main recheck used keyboard
Enter on the existing close, opened mobile nav and recorded `OVERFLOW=[]` at390px.
No automatic-dismiss redesign was introduced. One extra browser attempt received
a transient bundle503; follow-up HTTP200 and complete browser recheck passed
without code/config/cache intervention. That incident is retained, not called a
root-cause fix or an availability demonstration.

`w1_verification/FINAL_BOUNDED_RESULT.json` reconciles exactly four code members,
records actual pre/post hashes and separates code processing from runtime refusal.
The prior checker artifact's baseline-labelled-as-member hashes are retained and
explicitly corrected by this additive final receipt, not overwritten.

## Next autonomous work

1. W0: continue exact document-qualified source/closure links; do not conflate the
   Ledger comment BR namespace with Governance Architecture BR rows.
2. W1: inventory and extend coverage beyond these producers/readers; finish actual
   owner/organisation admission, credential and queued-handoff authority, custody
   exception cleanup and effective-rule commit boundaries under existing rulings.
3. Bring W5a/W6a/W7a prerequisites forward; keep W9a measurement/holdout protection
   early. No live execution until the applicable gates and admitted infrastructure
   genuinely exist. The old DAP4verified/7partial/1open accounting is not upgraded
   into a whole-operation claim by this hardening.

AISCA remains parked. Callable execution, real operation metering/results and
source CensusT14 remain unclosed; training/evaluation MOCKED paths remain outside
this slice. EX4/R37 protected independence, independent-head witnessing, full
source audit and CC performance are not claimed. No further owner decision is
needed to continue independent, already-authoritative work.