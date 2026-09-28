# Iteration 1 — DAP Portal Full Build + OS Prototype v2

## What was implemented

### Pages (Track 1 — DAP Portal)
| Page | Route | File | Endpoints consumed |
|------|-------|------|-------------------|
| DAP Landing | /dap | DAPLanding.jsx | None (static estate map from DAP reference) |
| Available Resources: Compute | /dap/resources/compute | AvailableResources.jsx | GET /api/compute/estate |
| Available Resources: Base Models | /dap/resources/base-models | AvailableResources.jsx | GET /api/model_registry/models |
| Available Resources: Trained Models | /dap/resources/trained-models | AvailableResources.jsx | GET /api/model_registry/full_record |
| Available Resources: Skills | /dap/resources/skills | AvailableResources.jsx | GET /api/skill-files/state |
| Data Governance: Policies | /dap/governance/policies | DataGovernance.jsx | GET /api/governance/state, GET /api/govern/estate_rules_record (auth), GET /api/govern/trust_center_record (auth) |
| Data Governance: Contract | /dap/governance/contract | DataGovernance.jsx | GET /api/team/access_register (auth) |
| Data Governance: Collection | /dap/governance/collection | DataGovernance.jsx | None (static) |
| Request Lifecycle | /dap/requests | RequestLifecycle.jsx | None (backend pending — full state machine from spec) |
| Data Estates | /dap/estates/:estateId | DataEstates.jsx | None (static from DAP reference) |
| Extract Modes | /dap/extract/:mode | ExtractModes.jsx | None (backend pending) |
| Connect Resources | /dap/connect/:tab | ConnectResources.jsx | None (backend pending) |

### Pages (Track 2 — OS Prototype v2)
| Page | Route | File | Endpoints consumed |
|------|-------|------|-------------------|
| OS Prototype | / | OSPrototype.jsx | iframe wraps /v8_prototype.html |

### Components
- StatusBadge — state machine status rendering
- BackendPending — honest "no endpoint" state
- TransportError — API failure display
- LoadingState — async loading indicator
- HonestEmpty — empty collection state
- AllowlistBlock — 403 full-surface block
- RefusalCard — Canon 5 §9.2 refusal display

### Auth
- JWT login/refresh wired in DAPLayout sidebar
- Uses seeded demo accounts from test_credentials.md
- Auth-gated endpoints (estate_rules_record, access_register, trust_center_record) show data after login

## Binding copy (ENT fixed strings)
Located in `src/strings/entitlementStrings.js`:
- ENT-23: `"cost · not yet measured"`
- ENT-26: `"Frontier allowance used · served locally"`
- ENT-34: `"Frontier unavailable · served locally"`

## Known issues / deferred items
- Request lifecycle uses reference data from DAP spec (backend has no request submission/list endpoints)
- Extract modes and Connect Resources are backend pending (no submission endpoints in contract)
- Some governance endpoints require auth — sign-in panel enables this
- Compliance refusals endpoint requires month param (format: YYYY-MM) — needs further investigation
- Estate landing data is static from DAP reference HTML (matches Digicow's 81 TB estate profile)

## Dependencies installed
None — all needed packages were already in the template (react-router-dom, lucide-react, tailwindcss)
