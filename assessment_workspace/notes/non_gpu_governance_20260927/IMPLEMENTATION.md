# Non-GPU autonomous continuation — 2026-09-27

Owner instruction: **Complete all non-GPU work in one autonomous go. Dont stop.**
This is a continuation, not a declaration that all 648 requirements are complete.
GPU connections, workbook, keys, accounts and original runtime are untouched.

## Implemented boundaries

- `services/non_gpu_governance/quality.py`: versioned metadata verifier for seven
  family coverage, confirmed rule identities, complete per-record outcomes,
  deterministic conservative strata, unknown provenance, applicable media checks,
  exact population/count reconciliation and accuracy-not-measured disclosure.
  **Not an actual seven-family source-side check executor.** No estate values enter E1.
- `context.py`: deterministic whole-unit ranking/packing from signed native token
  observations; frozen objective/frame/model/tokenizer/budget, unique unit identities,
  counts by class and top-ten re-extraction handles. No model call or token estimate.
- `rights.py` / `lineage.py`: signed native lineage and current-rights joins,
  transitive withdrawal and cycle/conflicting-identity rejection. Immutable withdrawn
  refs cannot be revived. No deletion, recall notification, retraining or budget refund.
- `memory.py` / `gate.py`: publication-before-reload proof, source version lineage,
  principal/closed-run linkage, retained class/loss metadata. User memory stays disabled.
  Actual memory bytes and re-extraction remain native-provider obligations.
- Native coordinator composition now invokes these checks at reserve/send and
  verification/publication/retrieval; the existing custody path inherits retrieval
  checks. Missing genuine records hold. Generic test-only bindings are not installed.
- Signed sidecars extend Observation only; sealed Canon contracts/owner schemas,
  original engine protocol, ledger shape and UI prototypes are unchanged.
- `GET /api/portal/entitlement/billing?period=<existing-period-id>`: principal-only,
  read-only ledger-derived usage lines with source meter/dispatch/terms/time joins,
  half-open periods, no other-seat detail, duplicate rejection, no silent fractional
  credit rounding or current-rate repricing. This is not a fiscal invoice issuer,
  payment processor, seat-capacity producer or an invented allowance/rollover policy.
- Current query GET rechecks release gates after awaited grounding verification.
- Canonical insert retry now yields through `contention_control.py`, an additive
  sidecar around the sealed writer. The initial direct edit was caught by invariant
  tests and removed byte-for-byte; hash baselines were NOT changed. All pre/post-write
  integrity checks remain. Fixed diagnostic codes omit payloads.

## Native metadata contract

Use the existing signed `/api/portal/activation/receipts` ingress and original
server-owned admitted signer resolver. New exact observation permissions are
`activation:observation:<category>`, not caller roles or newly minted roots.
Categories: quality_policy, quality_population, quality_register, context_policy,
context_window, lineage, rights, memory_policy, memory_publication, memory.
Typed claims commit `digest(claim.model_dump(mode='json'))`; all signatures are
verified through existing NativeReceipts. See the code models for exact schemas.

Quality policy must precede population and assessment receipts. Policy-pack version
and snapshot match the signed plan. `quality_population` commits snapshot_sha256 and
population_refs. Context policy commits frame_ref, model_sha256, tokenizer_sha256,
load_bearing_refs, window_tokens, reserved_tokens. Quality evidence precedes window.
Memory publication commits all MemoryEvidence fields except its own backlink.
Memory policy and original terminal record precede publication, which precedes reload.
Source→unit→derivative lineage is mandatory for source-version memory checks.

## What cannot be marked complete

The configured environment has **no AKKI_NATIVE_RUNTIME_FACTORY or matching native
runtime timeout**, no actual admitted worker/query ingress/inspection/custody transport
bound to this composition. No substitute provider is installed. Credential presence
for Tigris is not source admission and is not used as a workaround. GPU is parked.

Consequently no genuine source read, warm answer, measured delivery, source-side DQ
assessment, memory re-extraction, independently witnessed physical-host recovery,
notification delivery, original-estate health observation or live certificate has
been produced. Positive signed tests use **SYNTHETIC/MOCKED** authority and observations.
Algorithm correctness and real Mongo mechanics must not be relabelled live proofs.

The wider plan still includes source/ruling reconciliation (24 source-bounded rows,
509 supplemental mappings), broader DQ/repair/exception producers, commercial
membership/seats/period producers, Watch operations, audio/transforms and release
measurement. This tranche does not close them by adding metadata types. Mandatory
gates stay held wherever the actual authority, ruling or infrastructure is absent.

## Final verification

Final full non-GPU run: **684 passed,2 pre-existing gated skips,0 failures/errors**,
42.070s; all7 frontend tests and scoped Ruff F checks passed. GPU suites excluded.
New82 tests cover metadata, signed joins, billing, memory/certificate refusal and
bounded contention. Desktop1920×800/mobile390×844 overflow checks empty, mobile
account menu opens. Protected writer/control/prototype hashes match their original
baseline. No auth credential changes. `test_reports/iteration_49_resolution.json`
and `test_reports/pytest/non_gpu_governance_final.{xml,log}` are final references.

The original v1 `NativeEvidence` historical/LAB verifier is NOT alone sufficient for
the live application path: startup and certificate issuance now use
`GovernedNativeEvidence`, adding the same current native governance gate. No real
certificate was issued. Tests explicitly prove legacy signed LAB evidence cannot
bypass the stricter live composition.

An existing mobile header badge CSS precedence error was fixed without altering
owner prototypes. Admin-password overwrite suggestion in agent boilerplate was
not applicable to this scope and was not adopted. Earlier API503/TCP errors did
not recur in the final full or33-case targeted diagnostics; contention remains a
hypothesis for some earlier errors, not a proven universal RCA. Structured safe
diagnostics retained. No expectation loosened and no localhost substitution.

### Intermediate results retained for audit

72 new focused metadata/native-join/billing tests passed before independent testing.
Full initial regression: 668 passed, 6 external API failures, 2 pre-existing gated
skips; GPU suites explicitly excluded. See `test_reports/pytest/non_gpu_governance_first.*`.
Failures include app 503s and external TCP timeouts. No assertion, API URL or
integrity check was weakened to hide them. Final independent report supersedes this
intermediate result. Frontend markup/styles and auth credentials remain unchanged.