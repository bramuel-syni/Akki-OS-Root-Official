# Census operational slice — prototype fidelity and acceptance results

Date: 2026-09-25. **UI correction ready for owner review. Overall census activation NOT COMPLETE.**

## Owner baseline and correction

The owner rejected the first simplified UI and reaffirmed the supplied OS/DAP HTML as the baseline experience architecture. The corrected implementation uses markup mechanically extracted from those original artifacts, not another interpretation of their appearance. Their original bytes/hashes remain unchanged. The original simulated scripts, timers, random deltas and fixture entitlements are not executed.

Native routes:
- `/os`: owner-style portal launcher, tile selection and preview.
- `/os/admin/estate`: owner-style Registry, disclosure sections, census-intelligence rail and in-place history/detail.
- `/dap`: owner-style header, grouped navigation, four figures, composition/rights panel and notes/usage rail.
- `/dap/census` and `/dap/census?record=census-4`: scoped record browsing/detail.

CensusWorkspace/CensusOSPage (the rejected replacement dashboards) are no longer routed. Existing pages outside this census slice retain their implementations within the DAP shell; they have NOT all been brought to operational readiness.

## Verification runs

- `GREEN_fidelity_backend_live_1.log`: **58 passed**, 0 skipped, with the configured external preview API.
- `GREEN_fidelity_backend_live_2.log`: **58 passed**, 0 skipped, repeated.
- `frontend_markup_unit_FINAL.log`: **4 passed**: CSS shorthand preservation, CSS functions/quoted declarations, safe expression resolution, keyed React-node bindings.
- `fidelity_layout_FINAL.json`: **42/42 route-width checks passed**, widths 320, 390, 768, 1024, 1440, 1920 across seven routes. Full canonical run ID visible; no unexpected console errors. Initial anonymous 401 responses are expected, separately retained—not suppressed as application errors.
- `frontend_fidelity_lint_scoped_FINAL.log`: **0 errors / 0 warnings** for the changed fidelity modules. Existing project has no standalone ESLint config; a scoped ESLint API invocation uses installed parser/plugins, without changing global project lint rules.
- Final desktop OS/DAP screenshots and mobile390 canonical-record screenshot confirm no horizontal overflow. The first final mobile capture had an ambiguous text selector (same ID in list and heading); it was retaken against the unique record-heading element. This was a capture-selector error, not erased or counted as a product pass.
- `test_reports/iteration_3.json`: independent functional/visual comparison and interaction tests. Its reported 320px overflow, shortened run ID and React key warnings were subsequently fixed and rechecked by the main verification above. The original report is not overwritten to erase failures.
- Earlier local runs without the required URL environment skipped 15 API tests. Those runs are NOT the final runtime pass evidence. The final two logs above set `REACT_APP_BACKEND_URL` correctly.
- The historical whole-platform ratchet suite is still unavailable in this snapshot. None of these counts replaces its floor or claims a multi-repository seal.

## Original acceptance cases T01–T14

| Case | Result | Evidence / limit |
|---|---|---|
| T01 Continuity | PASS | Objective, current scope, owner rulings, original hashes, tests and next action banked; historical baseline limitations retained. |
| T02 Read protection | PASS | Anonymous current/legacy census and registry reads return 401. |
| T03 Tenant separation | PASS (scoped tests) | Server-owned RMS membership, no client tenant widening; RMS excludes Digicow records; foreign-state tests use isolated fixtures. Not a universal platform tenancy audit. |
| T04 Record coverage | PASS | Retained census 4 list/detail/latest agree; future tagged records are dynamically discovered in fixtures. Mixed/unassigned records deliberately withheld. |
| T05 Measurement honesty | PASS | 41 databases, 2,642 tables, 428,786,937 ESTIMATED rows; quality/volume/rights unknown. No raw SQL/host credentials emitted. |
| T06 Admission/bounds | PASS (API + isolated execution tests) | Analyst run denied; malformed/foreign/credential-bearing input rejected; missing admission and expired bound cause no executor call in tests. |
| T07 Execution boundary | PASS for implemented boundary; live read NOT VERIFIED | No pod estate reader in the dispatch path. Existing host identities and strict host-key verification used. Actual attempt was refused before any source read. |
| T08 Completion evidence | PASS (contract/failure tests) | Placeholder/malformed output cannot COMPLETE; canonical write/result failure cannot report success; old unverified completions not promoted. Live successful-output path remains unproven until T14. |
| T09 Failure isolation | PASS in MOCKED-executor tests | Blocked lane does not suppress another admitted lane; partial != complete. Not a claim of live multi-source coverage. |
| T10 Retry/recovery | PASS for tested cases | Duplicate key/changed selection/repeated completed run, registry rehydration and result-write failure tests. Not a full remote host power-loss assurance test. |
| T11 Shared views | PASS | OS/DAP read same tenant projection; live comparison confirms. |
| T12 Prototype journey/fidelity | PASS within census slice | Original markup, shell/disclosures/history/tabs, keyboard/pointer and actual state binding. Out-of-scope compute/model/connect controls explicitly disclose unavailable binding instead of simulating success. |
| T13 Responsive access | PASS for tested layouts | 42 route-width checks, desktop/mobile visual comparison; narrow header controls fixed. |
| T14 Actual activation | **BLOCKED / NOT PASSED** | Run `cr-a29e3b7b16ae`: both configured Akki identities returned AuthenticationException. No source data read, no verified live census result. |

MOCKED applies only to isolated test executors, not to the production census views or API. The blocked live run is displayed as blocked in both experiences.

## Corrective fidelity cases F01–F08

| Case | Result | Evidence |
|---|---|---|
| F01 Source provenance | PASS | Original SHA-256 checks; deterministic markup compilation receipt; no script/iframe nodes. |
| F02 DAP composition | PASS | Original header, grouped navigation, headline/figure cards, composition/rights panel and right rail compared with supplied artifact. |
| F03 OS architecture | PASS | Portal launcher/preview and Registry workspace/history retained; replacement dashboard unrouted. |
| F04 Real evidence only | PASS in visible census flows | Authenticated identity and scoped record values replace fixture persona, fake volume/usage/rights and random progress. |
| F05 Interactions | PASS in scoped journeys | Login, navigation, disclosures, history/detail/back/tabs, account/logout and run-dialog validation exercised without a new live source commission. |
| F06 Responsive layout | PASS after correction | 42 checks across six widths; original 320px failures preserved in before-fix receipt. |
| F07 Backend regression / IDs | PASS | 58 tests twice; full `cr-a29e3b7b16ae` displayed verbatim. |
| F08 Runtime stability | PASS after correction | React-node keys corrected, original CSS shorthand values preserved; no unexpected console errors on final matrix; 4 rendering units pass. |

## Every intentional deviation from the prototypes

1. **Tenant/persona:** Nexus Bank, Digicow/Meridian and example people are not adopted as authority. Existing authenticated RMS identity replaces them in the same header/avatar/badge positions.
2. **Numbers:** illustrative TB, quality, language, personal-data and rights shares become actual retained values or explicit unknowns. The original cards, disclosure boxes and bar positions remain; unmeasured bars are hatched/unfilled rather than falsely proportional.
3. **Meaning:** the Registry card says Source references rather than Sources connected, because configured/admitted references do not prove current reachability. Metadata row estimates are never labelled counted rows. The prototype's “every figure measured, never estimated” copy is replaced with actual provenance/limits.
4. **Entitlement/usage:** no Partner/MER-1 grant, free-pricing promise, included allowance or 214GB usage is fabricated. Existing badge/usage positions state scoped identity and unestablished measurements.
5. **Execution:** simulated time remaining, random deltas and click-to-complete are removed. The run action opens an identity-bound source confirmation and displays actual persisted state. A blocked run stays blocked.
6. **History:** only attributed records and real operational attempts are shown. Full run IDs are preserved. Missing GPU-spend or operator conversations are not replaced with synthetic transcripts/telemetry.
7. **Navigation gaps:** DAP gains a census-record entry and notes-rail links to run history/commissioning. The header acts as a home link. These close the original census-navigation gap without replacing the shell or introducing another dashboard.
8. **Accessibility:** original clickable elements receive keyboard operation, focus indication, semantic roles and unique test IDs. Existing modal close controls gain derived IDs. The prototype runtime's icons are supplied by React icon components in the original icon containers; original hover declarations are retained.
9. **Mobile:** three columns/Registry rail stack at narrow widths; a menu disclosure preserves navigation. At <=360px only the duplicated scoped-access badge hides, with tenant still shown in header and account menu. OS header actions wrap rather than overflow. All controls remain available.
10. **Long real values:** font size adapts in a numeric figure cell when the full estimate exceeds the prototype sample's width. Full value remains visible/in its title. Long evidence hashes wrap. Compact UTC dates are normalized for display.
11. **Unactivated adjacent surfaces:** Compute/LLM/Connect actions in this census view explicitly report the missing verified binding. Their availability is not fabricated, and this report does not claim those adjacent functions are complete.
12. **Prototype engine removal:** original declarative markup is rendered natively in React. No iframe, original mock script or eval is used. Safe binding lookup accepts identifiers/paths/negation only. Original raw artifacts remain immutable references.

## Remaining work / stop conditions

P0: validate the admitted Akki execution identity and authorized recovery options; inspect actual remote worker/connector custody configuration once access is established. Re-run T14 only through Akki. No competing keys, weakened host verification or fallback pod data pulls. Authentication refusal does not establish GPU hardware failure or prove remote authorized_keys contents.

P1: complete the remaining Canon-to-code/ruling reconciliation and operational journeys outside this slice. Existing request/entitlement/skill bindings identified as stubs in the audit are NOT fixed by this UI work.

Owner visual acceptance is still a human review step. Automated comparison and literal markup adoption establish a strong fidelity basis, not permission to silently change the design in future work.