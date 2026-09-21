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
