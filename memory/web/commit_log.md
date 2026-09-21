## Iteration 1 — DAP Portal Full Build + OS Prototype v2

- **Commit**: dc48d53131be2a36b36aabab83048cbbb779cfa2
- **Date**: 2026-09-20T14:21Z
- **Changes**:
  - Built DAP Portal (Track 1) with all specified screens
  - Built OS Prototype v2 iframe wrapper (Track 2)
  - Wired JWT login/refresh flow via sidebar
  - Created binding verbatim ENT strings module
  - Verified hard omissions (no partial-release, no "Waited" copy)
- **Files modified**:
  - frontend/src/App.js (routes)
  - frontend/src/App.css (design tokens)
  - frontend/src/lib/apiClient.js (centralized API client)
  - frontend/src/strings/entitlementStrings.js (ENT-23, ENT-26, ENT-34)
  - frontend/src/pages/dap/DAPLayout.jsx (sidebar + auth context)
  - frontend/src/pages/dap/DAPLanding.jsx
  - frontend/src/pages/dap/AvailableResources.jsx
  - frontend/src/pages/dap/DataGovernance.jsx
  - frontend/src/pages/dap/RequestLifecycle.jsx
  - frontend/src/pages/dap/DataEstates.jsx
  - frontend/src/pages/dap/ExtractModes.jsx
  - frontend/src/pages/dap/ConnectResources.jsx
  - frontend/src/pages/os/OSPrototype.jsx
  - frontend/src/components/dap/StatusBadge.jsx
  - frontend/src/components/shared/BackendPending.jsx
  - frontend/src/components/shared/TransportError.jsx
  - frontend/src/components/shared/AllowlistBlock.jsx
  - frontend/src/components/shared/LoadingState.jsx
  - frontend/src/components/shared/HonestEmpty.jsx
  - frontend/src/components/shared/RefusalCard.jsx
- **Mobile files referenced**: mobile/app/index.tsx, mobile/app/_layout.tsx (minimal placeholder app)

## Iteration 2 — R-91 CP-APP-JS-UNIFY Option A · V8 substitution engine restored

- **Commit**: d5ad077c6efd8e5d04105d05b2a4779a727616c7
- **Date**: 2026-09-21T00:17Z
- **Changes**:
  - Created lib/v8SubstitutionEngine.js (37 named rules verbatim from pod_shell)
  - window.V8_SUBSTITUTIONS_DUMMIES exposed at module load (37 entries verified)
  - Rewrote pages/os/OSPrototype.jsx as full PortalIframe with MutationObserver
  - data-testid="v8-portal-iframe-host" sentinel on outer div
  - App.js unchanged (71-line router)
- **Files modified**:
  - frontend/src/lib/v8SubstitutionEngine.js (NEW — 861 lines)
  - frontend/src/pages/os/OSPrototype.jsx (REWRITTEN — 175 lines)
- **Reference files used**:
  - assessment_workspace/repos/Extraction-Akki/pod_shell/frontend/src/App.js (V8-shell-port source)
  - assessment_workspace/phase0/specs/r91_cp_app_js_unify_spec.md
  - assessment_workspace/phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md

## Iteration 3 — R-91 follow-up · inline V8 engine into App.js

- **Commit**: 8ff2f67376f56dee661a816160fc11219807accc
- **Date**: 2026-09-21T00:34Z
- **Changes**:
  - Merged pod_shell App.js (V8 engine, 37 rules, PortalIframe) into /app/frontend/src/App.js (1108 lines)
  - Added DAP Portal routes alongside V8 engine in same file
  - Deleted lib/v8SubstitutionEngine.js (content now inline in App.js)
  - Reduced OSPrototype.jsx to thin re-export of PortalIframe from App.js
  - All 18 static grep pinned substrings confirmed HIT
  - 37 rules at runtime, v8-portal-iframe-host sentinel present
- **Files modified**:
  - frontend/src/App.js (REWRITTEN — 1108 lines, merged V8 engine + DAP routes)
  - frontend/src/pages/os/OSPrototype.jsx (REDUCED — thin re-export)
  - frontend/src/lib/v8SubstitutionEngine.js (DELETED)
- **Reason**: 63 sealed backend invariants are STATIC TEXT-SUBSTRING assertions against App.js file bytes; the prior module-boundary factoring put pinned substrings in files the tests never read

## Iteration 4 — Portal write-path wiring (R-100 surfaces)

- **Commit**: 5705617f4b9e06ff5f09f2310e59f84277ba15b2
- **Date**: 2026-09-21T09:05Z
- **Changes**:
  - RequestLifecycle.jsx: wired to GET/POST /api/portal/requests, stop, retry. Full state machine with submit form, Stop confirm dialog (STOP_CONFIRM), retry counter, Stopped terminal state
  - Entitlement.jsx (NEW): licence card, catalog picker with ENT-43 badges, allowance display (derived only, DAP-35 enforced), binding strings reference
  - CanonCountdown.jsx (NEW): R-91 ceremony surface wired to GET /api/canon/rules/rbm-8-ceremony-mechanic BYTE-VERBATIM
  - DataGovernance.jsx: added CanonRulesView wired to /api/canon/rules/{dap,rbm,roc}
  - apiClient.js: added tryGet/tryPost (never-throw API helpers)
  - App.js: added Entitlement + CanonCountdown imports and routes (additive only)
  - DAPLayout.jsx: added nav items for Entitlement, R-91 Countdown, Canon Rules
  - All 14 endpoints return 404 — honest "backend pending" states rendered throughout
- **Files modified**: App.js, apiClient.js, CanonCountdown.jsx (NEW), DAPLayout.jsx, DataGovernance.jsx, Entitlement.jsx (NEW), RequestLifecycle.jsx
- **Binding omissions grep-verified**: DAP-15 (no approver identity), DAP-35 (no remaining budget), ENT-3/ENT-43 (excluded rows absent), no party-halt on stop, no X-Akki-App-ID, no partial-release, no "Waited N days" in Sign-off
