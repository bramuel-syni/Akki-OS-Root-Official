# Iteration 2 — R-91 CP-APP-JS-UNIFY Option A

## What was implemented
- **V8 substitution engine** restored into the React tree (Option A per spec §3.2)
- New module: `/app/frontend/src/lib/v8SubstitutionEngine.js` (861 lines)
  - 37 named substitution rules ported verbatim from pod_shell App.js
  - `window.V8_SUBSTITUTIONS_DUMMIES` exposed at module load time (37 entries)
  - `applySubstitutions(doc, vals)` function exported
  - Helper functions: `_sourcesPhrase`, `_tablesPhrase`, `_findAncestorContainingText`, `_findAncestorWithSlot`
- Rewritten: `/app/frontend/src/pages/os/OSPrototype.jsx` (175 lines)
  - Full PortalIframe behavior: debounced applyAll, 3 API fetches, MutationObserver
  - `data-testid="v8-portal-iframe-host"` on outer div (harness sentinel)
  - `data-testid="v8-prototype-iframe"` on iframe

## Architecture decision
- Option A selected: engine restored into `/app/frontend/src/lib/v8SubstitutionEngine.js`
- Separate module (not inline in OSPrototype.jsx) for clean separation of concerns
- Import chain: App.js → OSPrototype → v8SubstitutionEngine → window.V8_SUBSTITUTIONS_DUMMIES set at startup
- App.js stays as 71-line router (unchanged SHA 282650cb...)

## Verification results
- `window.V8_SUBSTITUTIONS_DUMMIES.length === 37` ✅
- `data-testid="v8-portal-iframe-host"` present in DOM ✅
- `data-testid="v8-prototype-iframe"` present in DOM ✅
- Frontend compiles cleanly ✅
- ESLint passes (both files) ✅
- Hard omissions preserved (zero partial-release UI, zero "Waited" copy in rendered UI) ✅

## Dependencies installed
None (no new packages needed)

## Known issues / deferred items
- Pod_shell mirroring (byte-identity copy to `pod_shell/frontend/src/`) is NOT this agent's responsibility — requires separate agent working on `/app/assessment_workspace/repos/Extraction-Akki/`
- `data-substitution-applied=0` at screenshot time — substitutions fire only after iframe loads and dc-runtime renders; the count increments asynchronously
- Baseline retirement (`baseline_failures.json` edits) is outside `/app/frontend/` write scope
