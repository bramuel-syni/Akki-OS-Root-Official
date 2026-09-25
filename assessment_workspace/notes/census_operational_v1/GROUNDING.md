# Census operational V1 — grounding and execution record

## A. Owner scope
"Great, aligned - Recommendation approved. Maintain guard rails especialy post compaction as per disk specification. Enhance UI where necessary."

Approved recommendation: Akki-owned census execution and consistent OS/DAP registry views, including read controls and truthful completion/results. Parent directive, verbatim, is banked in STATE/DECISIONS.md current entry. Objective: STATE/OBJECTIVES/CP_CENSUS_OPERATIONAL_V1.md.

## B. Tests-first criteria (published before code)
|ID|Pass criterion; otherwise fail|
|--|--|
|T01|Current scope, prototypes, conflicts, next action recoverable from disk.|
|T02|Anonymous census/registry reads denied on current and legacy routes.|
|T03|Authenticated identity controls tenant, run-state and source scope; forged tenant cannot widen it.|
|T04|List/detail include every authorized retained census including 4 where owned; future valid records require no hardcoded list change.|
|T05|Estimated vs measured vs absent values remain distinct; fixture percentages/usage never become fact.|
|T06|Missing/invalid admission, foreign source and expired budget prevent a source read.|
|T07|Only Akki executor reads sources; pod never connects to estates or receives source rows.|
|T08|Validated outputs and governing receipts required for COMPLETE; placeholders/malformed outputs refused.|
|T09|Blocked lanes are explicit; permitted lanes may continue; partial is not complete.|
|T10|Repeat requests/interruption preserve outcome and do not silently duplicate work.|
|T11|OS and DAP use the same scoped facts and actual run state.|
|T12|Owner prototype browse/detail/history/run journey preserved; departures logged.|
|T13|Desktop 1920x800 and mobile 390x844 controls usable with zero page overflow.|
|T14|Actual authorized bounded Akki execution produces owned output and receipt. Fixtures/heartbeat/connection alone cannot pass.|

## C. Prototype conflicts and explicit dispositions
- PC01: OS labels Nexus Bank/persona M. Chen; DAP filename says RMS but rendered content names Digicow/Meridian. These illustrate tenants/personas, not authority to remap actual identities. Preserve authenticated tenant context; no fake person or cross-tenant data.
- PC02: prototype census count/volume/access/quality figures and dates are illustrative. Preserve hierarchy and flow; substitute record-derived measures/estimates or explicit missing measurement. Never calculate access permission from prototype percentages.
- PC03: OS prototype run uses a duration constant and synthesized time remaining. Preserve run/history controls but replace timed success/ETA with actual service state. A queued job isn't complete.
- PC04: prototype fixed multi-column framing breaks narrow screens. Owner authorized enhancement; collapse navigation into accessible mobile disclosure and stack notes/details without changing journey.
- PC05: generated design_guidelines.json proposes a dark dashboard, non-prototype fonts and decorative assets. Rejected as inconsistent with owner HTML. Existing light paper/serif/nav treatment and supplied flow govern; no unsolicited redesign.

## D. Implementation change log
### 2026-09-25 implementation and owner correction
- Added additive tenant-scoped census route composition, dynamic manifest projection, operational queue/executor/receipt validation, strict existing-host SSH dispatch, remote aggregate-only worker and source isolation. No sealed engine function bodies changed. Existing scheduler consumer points at the new executor.
- Applied owner-approved RMS membership to four existing accounts; receipt `phase0/drill_receipts/census_operational_v1/membership_binding.json`; passwords/roles unchanged.
- RED-first contract tests banked. Initial expanded slice and live read/role tests: 52 passing, report `test_reports/iteration_2.json`. Injected executor tests are MOCKED test doubles only.
- Actual bounded run `cr-a29e3b7b16ae` tried both configured host identities via Akki and was BLOCKED by AuthenticationException on both. No estate read. T14 is BLOCKED, not passed. This does not establish GPU hardware failure.
- The first UI implementation (`CensusWorkspace`/`CensusOSPage`) was a simplified redesign. Owner rejected its fidelity. **T12 is reopened/FAILED**, notwithstanding the prior testing report's functional-only PASS. Do not claim those screenshots match the supplied designs.
- Owner correction: "Aligned. this serve as baseline experience architecture nothing less only better if to be changed. Proceed autonomous - let me know if ready to." Confirmation: "this covers it foe now". Approved corrective scope: preserve original supplied OS/DAP structure, navigation, hierarchy, drawers and flow; remove replacement dashboard; keep backend/tenant controls; limit deviations to real data/state, accessibility and responsive fixes; explicitly surface Canon conflicts.

### Fidelity acceptance gates — defined before corrective implementation
- F01: Original artifact hashes unchanged; operational markup mechanically derived from those originals with source-line provenance. No reinterpretation/replacement dashboard.
- F02: DAP original navy identity header, collapsible grouped left navigation, central two-line estate headline/figure cards/composition and rights bars, right notes and usage rail retained in the original order and proportions.
- F03: OS original portal tile launcher/preview, Registry back/header/tabs, four estate topline cards, four disclosure sections, census-intelligence rail and in-place history/detail hierarchy retained.
- F04: Each visible datum is from scoped records or explicitly unavailable/estimated. No Nexus/Digicow persona, made-up usage, inferred rights, random deltas or timer completion leaks.
- F05: Original browse/disclosure/history/detail/run actions are keyboard-accessible, use actual service state, and support browser back. A missing binding is an explicit refusal, never silent/no-op.
- F06: Compare desktop at 1920x800 with the supplied original reference, preserving structure; at mobile390x844 preserve order/actions without original clipping. Also verify widths320/768/1024/1440 for overflow via non-screenshot layout checks. Fidelity PASS requires original comparison, not merely attractive output.
- F07: Re-run scoped API/role/refusal tests; no backend regressions. T14 remains separate and blocked until actual live output exists.

### Further explicit prototype conflicts
- PC06: Registry prototype says every figure is measured, never estimated, and names J. Mwangi with fixed TB/PII/rights/opportunities. Actual census4 contains estimates and no identity/coverage/rights attestation. Keep exact containers and interactions, substitute truthful record text/unknowns; do not remove the sections.
- PC07: Original DAP declares partner MER-1, open record entitlements, free browsing and 214GB received. Those grants, price and usage are not backed for the admitted RMS account. Preserve identity/badge/usage positions but show admitted actor and unestablished values rather than inventing licence or billing facts.

### Pre-implementation authorization finding

**RESOLVED BY OWNER:** The owner replied "Approved." to explicit RMS binding of the existing four demo users, preserving roles/passwords, operator-only launch and analyst read-only access. This is the authorization, not an inference from email. Binding changes will be banked without credentials.
Local application database inspection (metadata only; no estate connection) found no principal/tenant/org admission collection and no tenant/org membership field on the four existing demo users. `services/auth/dependencies.py` yields an Identity with user_id/email/roles/key_grants, not tenant_id. `services/principal_store/store.py` is an in-process admission store with no demonstrated bridge to those Mongo users. `services/tenant_separation/tenant_registry.py:20-23` requires identity-derived, non-selectable tenant context. Inferring RMS authority from the `demo.rms.example.com` email suffix would violate that requirement; no such mapping was created. Owner confirmation is needed before binding the existing accounts to RMS. Other identities must remain refused if unbound; roles alone must not imply cross-tenant access.

Existing census-3 lawful-basis receipt DOES exist at `phase0/lawful_basis_admits/20260922T014000Z_LAWFUL_BASIS_ADMIT_CENSUS3.json`, permitting scoped RMS/Digicow census under recorded read-only/aggregate/budget constraints. This is source-work authority, not a user-to-tenant admission record. The two must not be conflated.

Corrections to prior audit assumptions found during this trace: `data_source_adapter.py` implements refusal-queue and single-writer routing, not a live read closure; `RealRmsDataSource` raises on construction. Alternative live source services must be traced and composed rather than calling this placeholder. Mtafiti asset writer is an in-process envelope and explicitly not persistence; durable outcomes cannot be proved by its returned receipt alone. Existing scheduler is supervisor-managed (R-106 owner requirement); no new pod extraction loop or scheduler was created. Prototype source explicitly uses random deltas and timer-based completion; never port that behaviour to operational runs.

## E. Honest limits
The canonical code directory is empty; separate code/state .git and historical baseline suite are absent. No rebaseline or fictitious five-commit seal. Local tests will be reported as this slice only. No new remote connection failure has been established. Existing backend has registered real paths and placeholders; trace full consumer before selecting bindings. Preserve old receipts even when their completion claim is unproven; classify them without rewriting history.

## F. Verification and continuity
Record RED and two repeatable GREEN logs under phase0/drill_receipts/census_operational_v1. Original prototype artifacts are read-only evidence at canon/prototypes/20260925_owner_updated with intake hashes. Application source changes are recorded by the environment; no fabricated separate branch commits/seals. Update RESUME/NEXT/PRD at boundaries. Live activation T14 is separate from injected-executor tests.

## G. Final fidelity correction checkpoint
`VERIFICATION_REPORT.md` is the per-case T01–T14/F01–F08 record and change ledger. UI ready for owner review; overall census activation remains NOT COMPLETE. Original markup compiled (not redesigned), mock scripts never run. Three reported defects fixed: 320px header overflow, React-node keys and abbreviated run IDs; additional compact timestamp issue fixed. Final 42/42 layout checks pass at six widths across seven routes; 58/58 backend/source/API tests pass twice; 4/4 rendering units pass. Historical full-suite baseline/seal not claimed. T14 remains BLOCKED for cr-a29e3b7b16ae, both configured host identities refused authentication. No fresh remote operation was attempted during the fidelity correction. Existing source receipts and failed test observations are retained, not rewritten.