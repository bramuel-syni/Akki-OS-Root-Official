# v1.1 artifact handoff review

## Decision

**Accepted as the owner-to-engineering handoff and versioned implementation inputs.**
The corrected position resolves the ownership/proof overclaims. The intended schema
repairs and the split crossing permissions were independently checked. No further
desk-authored artifact revision is requested. This is not a live-readiness finding,
operative approval, registry update or issued activation certificate.

Owner explicitly delegates further hardening, semantic verification, policy
integration and record recovery to E1. Remaining technical defects listed below
belong to that work. Genuine new policy decisions, if encountered, remain distinct
from engineering fixes; no further broad owner questionnaire is justified.

## Immutable source artifacts

Originals retained unchanged under `originals/`:
- Certificate schema v1.1, SHA256
  `ad848bd95e76dcf4ef71cd0e0688914632de33e68ceb4168e7ede4209ad256d2`.
- Crossing table v1.1, SHA256
  `472b6369ef7059f9b451504e329605f02a8918081dbf3d5438239853ba6c8830`.

Corrections must be versioned/traceable implementation derivatives or governed
adapters, not silent replacement of these owner-supplied custody copies. The
corrected policy intention is controlling; engineering must not widen permissions.

## Verification performed

Offline JSON review and one pytest harness exercising **60 constructed payload
cases**:6 positive shape fixtures,25 claimed repairs/controls,24 migrated prior
cases and5 focused residual edge cases. All cases matched their recorded expected
outcomes. This includes known residual ACCEPTANCES; it does not mean60 malformed
payloads were rejected or that operational verification passed.

Draft2020-12 schema metavalidation passed. A timezone-aware date-time checker was
enabled for the fixtures (not an exhaustive RFC3339 conformance suite). Both input
hashes were checked before/after and unchanged. Positive inputs/receipts/signatures
are explicitly SYNTHETIC, never issued certificates or app/registry data.

Artifacts:
- `validation/test_revision_v1_1_offline.py`
- `validation/results_matrix_v1_1.json` (case-by-case keyword/error paths)
- `validation/payloads/`
- `/app/test_reports/iteration_37.json`
- `/app/test_reports/pytest/pytest_artifact_validation_revision_v1_1_iteration37.xml`

No source, model, runtime, API, database, credential, configuration, frontend or GPU
operations were performed. Only assessment copies/tests/records/continuity notes.

## Intended changes confirmed

- LIVE-VERIFIED rejects blocked/revoked declarations, unverified issuer, empty
  signature, peripheral mocks and failed activation acceptance script.
- Scope/expenditure approval arrays containing only refusals reject.
- Path B requires a refusal object and a model reference.
- Path C requires a held-out object, recipe string, model reference and its refusal
  kind. Admitted output cannot have empty criteria or non-met outcomes.
- Path A cannot label model release as admitted; it requires not_applicable.
- Negative limits/usage/output-reconciliation counters reject.
- Refused Path C can honestly represent not_measured with BOTH value and
  measurement_ref null; substituting a fake value/ref rejects that branch.
- Crossing controls distinguish `external_crossing.uncontrolled` from
  `external_crossing.controlled_exception`. Pilot exception is unavailable; the
  controlled branch requires both class-scoped ceremony and per-call authority.
- Unassessed routing retains its original assessment state and grants no eligibility
  or disclosure permission. Default unmatched policy remains REFUSE.

## Residual engineering-owned corrections (not another owner revision cycle)

1. **PARTIALLY LIVE parity:** schema still accepts nonempty revalidation triggers
   with blocked=false, and a failed activation acceptance script. Enforce the real
   core-evidence requirement and consistent blocked-state derivation for this state.
2. **Small shape gaps:** re-performance agreement/disagreement counters still
   accept negative values; Path B permits a junk-stratum refusal instead of the
   specified out-of-scope query demonstration. Harden against applicable standards.
3. **Actual acceptance standard:** admitted C permits one met criterion. E1 must
   resolve the adopted six-criterion identities, completeness, uniqueness,
   thresholds and outcome evidence—not just require a nonempty list. Approval
   membership, distinct voters and actual quorum likewise require native records.
4. **Crossing migration:** the final deny row still tests scalar
   `external_crossing: refused`, although the new dial has two subfields. Normalize
   the deny logic into the canonical versioned representation; retain fail-closed
   handling for legacy/unknown forms. Do not conflate denying uncontrolled material
   with automatic permission for controlled material or silently broaden either
   branch. This is a static inconsistency, not an observed runtime disclosure.
5. **Mandatory semantic/evidence verification:** receipt authenticity and matching,
   signatures, membership/scope, chronology, actual manifest membership and sums,
   limits/reservations, held-out isolation, runtime provenance and current-state
   derivation. `semantic_verifier_note` is a minimum list; v1.3 and adopted Canon
   supply the full obligation set. A well-formed invented reference still proves
   nothing until authoritative resolution succeeds.
6. **Absence versus live proof:** a schema-valid refused C with not_measured is an
   honest result shape, not automatic evidence that the required producers really
   ran. If an evidence-bearing producer remains mocked/unimplemented, LA-13 still
   forbids live certification. Real failures/absence are recorded without inventing
   values and evaluated against the predeclared path-acceptance requirements.

## Next ownership and scope

Freeze versioned validator/semantic-verifier/policy-resolver interfaces and
acceptance tests BEFORE any run. Recover effective group/dial/limit records through
the existing authorities; a pilot_setting in a file is not an automatic estate
registry write. Retain distinct purpose-specific groups and actual recorded
allocation/reservation enforcement. Only then commission approved bounded work.

Certificate issuance follows real proof. Acceptance of these artifacts does not
close the14 readiness packages or permit relabelling existing architecture tests
as live evidence. GPU stays excluded; no new infrastructure action is implied.