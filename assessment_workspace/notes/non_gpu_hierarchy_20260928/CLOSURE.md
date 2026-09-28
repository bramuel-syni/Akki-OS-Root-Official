# Akki — non-GPU hierarchy and reliability continuation

## Owner decisions

Owner requests completion without slower responses, reduced model capability or
degraded UI quality, then a holistic component-handoff acceptance test. Supporting
capabilities must not be surfaced as unrelated applications. Owner accepted our
recommendation: existing requirements/hierarchy first; five enhancements deferred.
Latest answer: “1 - as recommended. 2 - there is no repository, setting up the
repository now”. GPU/SSH remains parked. E1 is not a data path.

## Completed and verified in this continuation

| Area | Result | Evidence |
|---|---|---|
| My Work hierarchy | Work records, My Team, Company Goals, Board nested under one parent | hierarchy Jest + live browser51 |
| Grey Mirror hierarchy | The Watch feature with State/Record/Under Watch/Decisions | browser50/51, seven old redirect checks |
| Continuity | `?request` preserved across siblings, history and refresh | loaded1218-record operator UI51 |
| Truthful state | Unknown/loading/error is not zero/empty; unavailable feature data explicitly labelled | workmodel/hook tests + browser51 |
| UI fidelity | Original HTML/generated templates unchanged; scoped palette/spacing retained | protected hashes + desktop/mobile screenshots |
| Work performance | Same projection with1 fullyverifiedprefix instead of3; selecting a row fetches detail only | snapshot equality tests and6hook tests |
| Reliability | Closed inherited lease cannot poison a newly authenticated HTTP request |5scope recovery tests, fullsuite and3repeat flaky rounds |
| UX defects | Duplicate IDs, literal evidence binding, sign-in contrast and style warning removed |22frontendtests + browser/selftest |

### Scope503 root cause and safeguards

Safe diagnostics locate failure at `portal_scope` **binding** ->
`bind_control_scope` previous-scope check -> `require_control_scope`: previous
carrier exists but lease is closed. There is no lease TTL. The old assumptions
about a five-second deadline or universally caused ledger contention were wrong.

`bind_authenticated_request_scope` is used only after `census_identity` validates
the current request and its write-role gate. It discards a dead context carrier,
then composes the unchanged ordinary lease. `finally` closes/restores correctly.
Ordinary bind/require do not revive closed children; active nested scopes cannot
substitute identity; cancelled requests close inherited children. No JWT refresh,
new PrincipalV1, native admission, seed reset or secret rotation occurs.

## Explicitly not completed

- No native source/query/worker/inspector/custody provider was supplied or installed.
- Team/goals/board/Watch views have no native records connected. They are honest
  unavailable states, **not completed live data features** and not mock feeds.
- No native source-side seven-family check/repair, memory-byte publication/reload,
  recall/notification/re-derivation effect or physical-host recovery proof.
- No real grounded answer, byte delivery, measured end-to-end source/model latency,
  capability benchmark or live activation certificate.
- Broader commercial/period/seat producers, Watch/witness/governance, original24
  source-bounded and509supplemental semantic joins/648-row release audit remain.
- Two pre-existing gated custody drills skipped; all GPU-direct suites excluded.
- No security audit requested/performed. Explicit-origin CORS policy alignment and
  legacy App.js module decomposition remain maintenance observations.

Positive provider/authority test observations are **SYNTHETIC/MOCKED**. Persisted
demo held-work requests are useful for UI load/continuity checks, not proof of
native estate effects. Production API responses were not mocked in browser tests.

## Five recommendations — proposals only, deferred by owner choice

1. **Continue across applications:** carry objective, authorised context and cited
   evidence between Chat, Documents, Data Suite and My Work without silent loss.
2. **Resolve blockers in place:** name the exact missing approval/evidence and
   navigate to an authorised resolution from the existing work detail.
3. **Goal-linked delivery:** connect tasks, owners and milestones to Company Goals
   using actual organisational records rather than illustrative completion scores.
4. **Actionable Watch:** group related verified changes/risks and offer authorised
   responses inside Grey Mirror, instead of technical component tiles or noise.
5. **Fast, truthful feedback:** immediate acknowledgment, actual stage progress and
   supported streaming, without invented progress or model/context downgrades.

## Gate for the requested holistic component-handoff test

**Status: NOT READY / NOT RUN.** Repository availability alone is not completion.

Required entry evidence:
1. Original admitted native connection descriptors/implementations, signing-key
   resolver/mandates and bounds installed in the correct owning estate (not E1).
2. Genuine source/census/snapshot → frozen objective/plan → entitlement/rights/
   approvals → allocation → worker → DQ/context/class/memory → registry → query/
   delivery handoffs accepted with canonical evidence and measured usage.
3. Current denial, expiry, withdrawal, ambiguous-delivery, replay/no-double-spend,
   cancellation and host-recovery effects verified with real owning services.
4. Watch/notification/witness/commercial reports reconcile to those same effects,
   not generated substitute receipts or a second truth store.
5. Comparison baseline pins the SAME model/version, source set, class floors,
   context/token budget, permissions, load and environment. Measure latency
   distributions/first-useful-output and answer correctness/refusals. Never infer
   a speedup from fewer calls alone or improve speed by degrading capability.
6. Full owner experience: readable responsive layout, immediate honest pending
   states, keyboard/back/refresh continuity, no unscoped data or phantom actions.

The regression suites run here are NOT that final acceptance test. Once the owner
provides the repository/location, inspect actual bindings and finish the remaining
requirements before labelling the holistic exercise ready.

## Test record

Independent51:694backendpassed,2skipped,0failures/errors;22frontendpassed. Repeated
formerlyflaky API suites:8cases×3rounds plus12cases×3rounds, allpass. Dedicatedscope
recovery5/5. ScopedRuff F checks pass. Finalmargincleanup: no warning, supportpane
margins0px, zero mobile overflow. References: report50, report51, report51resolution,
pytest_iteration_51_non_gpu.xml and hierarchy_frontend_release.log.