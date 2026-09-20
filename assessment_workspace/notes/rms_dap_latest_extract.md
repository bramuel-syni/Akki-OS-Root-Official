# RMS DAP LATEST · design-source extract (backend-relevant surfaces only)

**Source manifest**: `phase0/credential_drop_manifests/20260920T1140Z_owner_drops_manifest.json` (drop_id `20260920T1140Z`)
**Custody**: `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` (sha256 `1b5f59d4e7eb22cfea166ec5119dae8503c9755fa21af00a264c7596085738bc` · 221,620 bytes)
**Role**: binding design source (DAP portal) · SUPERSEDES RMS AI Prototype v2 (sha `9952692ce058…`) for DAP portal surfaces per owner ruling verbatim
**Non-supersession scope**: RMS AI Prototype v2 remains binding for non-DAP OS-prototype surfaces (WorkStudio, ThinkLab, Collab, Manage Estate, Approvals, Build Your Resources, Your Resources, 3rd Party Apps, The Watch, additional surfaces).
**Citation form**: `RMS DAP LATEST · <element-id-or-anchor>`

This extract catalogues ONLY the backend-relevant surfaces (state vocabulary, prop schema, script bindings). Full frontend audit is Chunk-3 territory.

## Prototype prop schema (deck-config JSON · data-dc-script data-props)

Four boolean/text switches drive the prototype's rendered state:

| Prop | Editor | Default | tsType | Section |
|---|---|---|---|---|
| `partyName` | text | `"Meridian AI Research"` | string | Party |
| `touchesControlled` | boolean | `true` | boolean | Governance |
| `standingApproval` | boolean | `false` | boolean | Governance |
| `censusStale` | boolean | `false` | boolean | Governance |

**Backend implications**:
- `touchesControlled`: whether the operation crosses controlled data (drives whether request enters `In Approval` or bypasses to `Executing`) — matches DAP-14 controlled request routing.
- `standingApproval`: whether the party holds a standing approval — surfaces DAP-LIFECYCLE-Q2 (hard hold: can standing approval cover Train a Model or Build a Skill?).
- `censusStale`: DAP-30 browse-degrades-not-refuses signal · already backend-side.
- `partyName`: template value substituted at render time · no backend contract impact.

## Structural anchors (backend-observable)

| Element id | Role |
|---|---|
| `dap-body` | page-level container |
| `dap-nav` | top navigation surface |
| `dap-rail` | left rail (stat card set · 8 states + Total) |
| `dap-progress-rail` | progress rail (per-request drawer detail) |

## Script bindings (test scaffolding · not runtime)

- `CURRENT_USER = '…'` — prototype-only mock user constant.
- `TODAY_ISO = '…'` — prototype-only mock date constant.
- `const nav = …` (2 occurrences) + `const navGroups = …` — navigation is inline JS-configured, not backend-fetched, in this design source.

## Stat card vocabulary (matches journey doc §9 verbatim · 8 cards + Total aggregate)

Confirmed in HTML source: `'Total' 'In Approval' 'Executing' 'Ready' 'Retrieved' 'Refused' 'Blocked' 'Expired'`.

Matches `extraction_request_approval_journey.md` L206 verbatim: "Page rail stat cards, final count: eight — `Total`, `In Approval`, `Executing`, `Ready`, `Retrieved`, `Refused`, `Blocked`, `Expired` — two rows of four."

## Absence findings for backend contract binding

- **No API endpoint declarations** in this HTML source (it's a standalone prototype using inline JS; the mock data is compile-time).
- **No JSON schema** for request records is embedded (drawer content is templated inline).
- **Blocked kind not decomposed** in top-level card set (three kinds surface at drawer level per §11, not at rail level).

## Supersession banking

Per drop manifest `supersedes_scope`: "DAP portal design source ONLY (RMS AI Prototype v2 remains binding for non-DAP OS-prototype surfaces — WorkStudio · ThinkLab · Collab · Manage Estate · Approvals · Build Your Resources · Your Resources · 3rd Party Apps · The Watch · additional surfaces not in nav per Step 8 card §§3.1-3.10)."

Owner ruling verbatim: "LATEST.html supersede the previously banked portal prototype as binding design source"

## Standing bounds preserved

Additive-only per SO §3.8 · frontend build HELD until this wave seals + specialists dispatched (per owner directive item 6 at wave-open ruling).
