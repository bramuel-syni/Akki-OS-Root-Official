# Review of owner position and machine-readable activation artifacts

## Verdict

Engineering ownership, refusal to relabel synthetic measurements, per-run approval
and the broad dependency sequence are correct. The assertions that the two
artifacts make semantic proof structural, that a synthetic value has nowhere to
hide, and that every non-infrastructure dependency is therefore closed are **not
supported**. These files are useful policy/contract inputs, not operative grants,
runtime registry updates or evidence verifiers.

The work remains E1's: shape hardening, semantic verification, policy resolution,
admission/registry integration, real producers and independent operational proof.
The owner need not implement them or repeatedly supply general specifications.
The14 packages are delivery work, including real verification—not only code edits.

## Authoritative bytes and scope

Originals retained unchanged in `originals/`:
- `activation_certificate.schema.json`: SHA256
  `6bebe79c4d5db17db3bcf047c0512c749193bd7cc081e83bdaf7e5f6bbe8f0fa`.
- `crossing_decision_table.v1.json`: SHA256
  `f90cf6d7c36f3d4b89bc8bf099c990c223b5836c5cbdf282f70d781b69ba74f3`.

Review is against the downloaded original bytes. An intermediate extracted policy
representation added fields not present in the original; those additions were
discarded. The original has5 rows and no row IDs, priority fields, conditions DSL
or scope/all metadata. No conclusions depend on those invented fields.

Offline review only. No application code, configuration, admissions, registry
entries, database, credentials, source/model/worker/provider or GPU operations
changed or invoked. Only custody copies, review fixtures/tests/results and notes
were written. A fixture below is not an issued certificate and was never ingested
into Akki. GPU remains excluded by the prior user instruction.

## Tested certificate findings

The document is a valid Draft2020-12 schema under `check_schema`. That checks schema
construction, not whether its instances represent legitimate operations.
`Draft202012Validator` validation exercised24 constructed cases against the
UNCHANGED schema. Date-time checking was enabled by a local timezone-aware checker
(native optional date-time checker was unavailable); this was not a full RFC3339
format-conformance test. jsonschema version4.26.0.

**17 semantically inconsistent candidates passed the schema. Six explicit guard
controls rejected as expected. One honest absence representation was rejected.**
These are observed structural-validation results, not observed application bypasses.

| Case | Observed schema result |
|---|---|
| LIVE-VERIFIED with peripheral mocks | Accepted |
| LIVE-VERIFIED with blocked=true and authority_revocation | Accepted |
| LIVE-VERIFIED with unverified issuer and empty signature | Accepted |
| LIVE-VERIFIED with failed activation acceptance script | Accepted |
| Path C marked admitted with empty criteria, no standard, no heldout/base/recipe, census-only purpose | Accepted |
| Path B with null required refusal demonstration | Accepted |
| Criterion met with hardcoded scalar and empty measurement_ref | Accepted |
| Criterion met with made-up nonempty measurement_ref | Accepted |
| Negative reconciliation counters and inconsistent denominator/manifest counts, unaccounted=0 | Accepted |
| Negative usage; negative limit; observed above limit (three cases) | Accepted |
| No spend dimension, reservation null, reconciliation=false | Accepted |
| All approval decisions refused, empty group/principal, quorum without threshold reference | Accepted |
| Well-formatted but impossible chronology | Accepted |
| Negative/mismatched re-performance counters | Accepted |
| Revocation/change trigger listed while blocked=false | Accepted |
| not_measured with measured_value=null | Rejected: null excluded by value type |
| Evidence-chain mock=true; unaccounted!=0; workspace_touched=true | Rejected by const controls |
| Required root field missing; unknown root property | Rejected |
| Invalid date-time text with checker enabled | Rejected |

### What this disproves

- `description` text such as "derived, never asserted" is annotation, not an
  executable invariant. The instance still contains a caller-supplied enum.
- Requiring `measurement_ref` as an unconstrained string does not establish that
  the reference is nonempty, real, authentic, measured, current or bound to this
  run/material/evaluator. Even a perfectly formed invented reference passes shape
  validation; provenance must be resolved from authoritative records.
- `unaccounted:0` constrains a supplied declaration. It does not reconcile actual
  manifest identities, denominator and totals. Arithmetic and real member
  reconciliation are separate verifier work.
- `implementation_workspace_touched_data:false` cannot establish where a workload
  actually ran. Runtime/custody attestations and independent proof remain needed.
- Authority and acceptance as separate objects is a sound structural distinction,
  but chronology, scope, group membership, quorum and release eligibility are not
  thereby enforced. A failed real model can still evidence live execution; a failed
  activation acceptance script is a different matter.

### Engineering correction, not another owner questionnaire

1. Versioned schema hardening: conditional states and path requirements, meaningful
   nonempty refs, nonnegative counters/quantities, cardinality/uniqueness where
   applicable, and an honest not-measured branch. Preserve original upload bytes.
2. Represent absence explicitly (e.g. null measured_value plus reason/failure event
   provenance); do not force zero, false or arbitrary text into an absent measurement.
   Actual measured zero/false remains legitimate when genuine evidence establishes it.
3. Mandatory semantic verifier: native receipt/registry resolution, issuer authority
   and signature validation, frozen request/snapshot/policy matching, required group
   decisions, chronology, arithmetic/manifest reconciliation, actual limit/reservation
   enforcement, criteria and protected evaluator evidence. Fail closed on unavailable
   proof. Standard JSON Schema does not establish remote truth or general cross-field
   arithmetic/chronology.
4. Compute state server-side from verified evidence and dependency modes; reject
   contradictory submitted labels. Discovered evidence-chain mocks cannot be hidden
   by simply omitting them from a submitted mocked_components list.
5. Define append-only certificate versus current-status projection explicitly.
   `superseded_by` and changing revalidation/state must come from later events or a
   derived view, not an in-place edit of a signed original certificate. Pin the
   existing canonical receipt/signature mechanism rather than create a second authority.

## Crossing table: useful input, not an executable complete resolver

Correct provisions: single crossing; no-match REFUSE; rights do not downgrade
custody; one-call exception not persistent. These should be preserved.

Important policy binding gap: both uncontrolled/frontier and controlled/frontier
exception rows require the same `external_crossing="masked_permitted"` dial.
The pilot ruling only permits masked crossing for **uncontrolled classes**.
The exception row's ceremony requirement is currently prose, not a structured
class/estate-specific adoption/exception receipt binding in this file.

**Required behavior:** row4 remains unavailable for the pilots unless a distinct
valid class-scoped dial change/ceremony AND the applicable call-specific authority
are evidenced. An owner per-call approval must not silently substitute for a
prohibited dial/class change. If current adopted vocabulary cannot express those
records, preserve refusal rather than invent a permissive interpretation.

No resolver is contained in the upload, so this is a specification/integration
gap—not a demonstrated live leakage or policy bypass.

E1 must implement the typed policy loader/resolver and prove:
- immutable adopted policy hash/version; closed inputs; missing/unknown values deny;
- explicit allow/refuse outcomes and masking obligations; denial and mandatory
  ceilings cannot be overridden by a less restrictive matching row;
- interaction with per-purpose authority, actual source custody, recipients,
  expenditure and scope—not treating crossing permission as permission to execute;
- conservative unassessed→controlled ROUTING while retaining unassessed status;
  neither quality eligibility nor unmasked disclosure can be inferred from coercion;
- call-specific exception expiry/replay, effective class/tenant/receiver/model scope,
  and required ceremony evidence through the existing crossing, not another route.

## New owner rulings — policy intent received; record application not verified

1. Approval groups described as already seated for two tenants; three categories
   scope, expenditure, purpose-specific; any-one per group absent ceremony quorum.
   **Interpret as categories, not one interchangeable purpose-specific pool:** all
   required ethics/security/etc. groups still independently participate under LA-5.
2. Purpose/scope obtained through the gate per run; no standing permission from chat.
   This is correct and remains a pre-effect condition.
3. Existing allocation,20 GPU-hours/run and USD0 external; absent recorded ceiling
   holds. No GPU action authorised by this review. Runtime bindings must resolve
   aggregate resource-hours, actual allocation/reservations and charge boundaries.
   USD0 external does not permit paid frontier calls because a crossing is allowed.
4. Pilot dials stated: controlled custody floor; seated authority groups; masked
   uncontrolled-only crossing; no disclosure counterparties; v1 registry records;
   loosening receipted. These are owner statements, not evidence that this review
   wrote/verified those entries. Recover actual IDs, effective versions and receipts.
5. Missing applicable threshold to be presented as an exact missing value and ruled
   same day. This establishes response process, not a presently missing threshold.
   Freeze the adopted threshold before protected evaluation; never fill an observed
   measurement by owner ruling or tune acceptance after unblinding results.

No new generic questionnaire is needed. E1 recovers/seats the policy through the
existing governed mechanisms as authorised, validates the records, and escalates
only genuine missing decisions or infrastructure/custodian actions it cannot perform.
Reading a message does not itself mutate the estate registry or seat a principal.

## Sequence interpretation and closure language

The ratified order is workable: activation/control/portal → evidence producers →
A → B → C → certificates, with approvals and bounds preceding effects.
**Certificates last must mean issuance last, not validator/design/acceptance-script
work last.** Freeze those interfaces and acceptance tests before commissioning runs;
otherwise later proof design cannot certify that it preceded the run.

The two concrete C findings remain code/provenance fixes: reuse the recorded
training result rather than retrain during evaluation; actual criterion observations
or honest not-measured, never relabelled placeholders.

Preferred position:
"Owner policy direction and initial machine-readable artifacts are supplied. E1
owns contract hardening, semantic/evidence validation, policy integration, actual
record recovery, implementation and operational proof. Engineering proceeds without
another broad owner questionnaire; real admission/custody/evaluator dependencies
are verified, not presumed. Certificates are issued only after the frozen proof
requirements are met. Infrastructure is not used to defer independent engineering."

It is not accurate to claim only infrastructure remains operationally outstanding;
all the readiness register's joins/producers/proofs still require delivery. This
does not shift them back to the owner.

## Reproducible evidence

- `validation/test_artifact_validation_offline.py`: one pytest harness,24 payload
  cases plus schema/hash/policy assertions (not24 separate pytest test functions).
- `validation/results_matrix.json`: exact accepted/rejected results and error paths.
- `validation/counterexamples/`: all24 synthetic payloads, never issued/ingested.
- `validation/verification.xml`: main-agent confirmation run,1 test passed.
- `/app/test_reports/iteration_36.json`: independent testing report; subsequent
  checker correction preserves nullable format semantics and timezone shape, with
  the same24 observed outcomes. No runtime/schema-original fixes were applied.