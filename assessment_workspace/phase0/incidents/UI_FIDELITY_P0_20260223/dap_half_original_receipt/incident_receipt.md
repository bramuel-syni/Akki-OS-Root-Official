# DAP-FIDELITY-P0 · Incident Receipt · 2026-02-23T~19:20Z

**Class:** P0 · owner-escalated fidelity defect on a user-visible surface.

**Owner verbatim (2026-02-23T~19:15Z):** *"This is nothing close to DAP i gave you to build - I'm getting seriously worried."*

**Surface at fault:** `/dap` landing route rendered by `DAPLayout` + `DAPLanding`.

**Status:** DIAGNOSTIC ONLY. NO REBUILD executed. Awaiting owner GO on the corrective plan below.

**Adjacent work status (as owner explicitly directed to STOP if conflicting):** the CP-SINGLE-SURFACE-RULING seal (owner ruling 2026-02-23T~19:00Z) reached DOUBLE-GREEN at 6421 passed / 13 skipped / 0 failed (sweeps A `ffe2728c…` + B `4b4dd74d…` byte-consistent to within 5 lines of expected non-carrier diff), code changes STAGED in the working tree of BOTH pod_shell/frontend/src/App.js + /app/frontend/src/App.js + 4 scaffolding tests updated + the RED-first `test_cp_single_surface_ruling.py` GREEN at 10/10, but **UNCOMMITTED — no Code Commit-A, no /app-A, no State-B**. That work does not conflict with this diagnostic (route-wiring only, not DAP content); paused pending owner clearance on the joint scope. If cleared, the corrective plan below folds the DAP fidelity rebuild AND the single-surface ruling into a single seal chain OR sequences them as two separate seals — owner picks.

---

## Investigation 1 · DESIGN AUTHORITY — the owner's DAP source of truth

### 1.1 · Owner-provided DAP artefacts located (all opened this session)

| # | Path (abs) | Timestamp | sha-context | Type |
|---|---|---|---|---|
| 1 | `/app/assessment_workspace/canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html` | 2026-09-09 08:55 · 230,577 B | design_id `dap_frontend_standalone` sha256 `d0fc1b498e07…` (banked in `notes/spec_id_index.md`) | HTML prototype (v1 owner-labelled) |
| 2 | `/app/assessment_workspace/canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` | 2026-09-09 · 21,346 B | sha256 `e675990aa68e75141f41b418fd19c0a2c05b70441c6217ebdde44e5362c55263` | Backend spec (DAP-1..30 canon) |
| 3 | `/app/assessment_workspace/canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | 2026-09-09 extraction | — | Extracted text of #2 |
| 4 | `/app/assessment_workspace/custody/owner_drops/20260920T0824Z/RMS_Data_Access_Portal.html` | 2026-09-20 08:25 · 327,266 B | — | HTML prototype (mid-day rev) |
| 5 | `/app/assessment_workspace/custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` | 2026-09-20 08:24 | sha256 `3c9be71541534942d3c3038c24cc8981aea38667a3a2e521043810a23c5085fe` | Backend engineering brief |
| 6 | `/app/assessment_workspace/custody/owner_drops/20260920T0824Z/Front_End_Integration_Brief.md` | 2026-09-20 08:24 | — | Front-end integration brief |
| 7 | `/app/assessment_workspace/custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` | 2026-09-20 11:48 · 221,620 B | — | **HTML prototype (LATEST — owner-labelled operative reference)** |
| 8 | `/app/assessment_workspace/custody/owner_drops/20260920T1140Z/DAP_List_of_Changes_20260920.docx` | 2026-09-20 11:48 · 16,645 B | 290-word delta doc | List of Data-Estate + Extract module changes at 2026-09-20 |
| 9 | `/app/assessment_workspace/custody/owner_drops/20260920T1140Z/extraction_request_approval_journey.md` | 2026-09-20 11:48 | — | Extraction request submission-to-approval journey spec |
| 10 | `/app/assessment_workspace/notes/DAP_SPEC_REVISION_RECONCILIATION_20260920.md` | 2026-09-20 08:35 | — | Session reconciliation report (revision inventory) |
| 11 | `/app/assessment_workspace/notes/canon_dap_backend_spec_v1_requirements.md` | 2026-09-09 ingest | — | DAP-1..30 canon requirement enumeration |
| 12 | `/app/assessment_workspace/notes/W_DAP_STACK_2A_close.md` | 2026-09-13 wave-close | ratchet 3560→3570 | Wave close for DAP admission sub-wave |

**Operative authority:** artefact **#7 `RMS_DAP_LATEST.html`** (2026-09-20 11:48 owner-labelled "LATEST") is the front-end design of record. Artefacts #5 + #6 are the backend + integration briefs the front-end binds to. Artefacts #2/#3 + #11 define the DAP-1..30 canon requirement set the backend serves.

### 1.2 · What the owner's DAP design actually specifies

**Header/chrome (from `RMS_DAP_LATEST.html` bytes 3800–4600 opened verbatim):**

- Blue2 (`--blue2:#0f1b33`) top bar, height 52px.
- Wordmark: **`Digicow Data Access Portal`** in `var(--head)` (Iowan Old Style, Georgia, serif) at 16px, letter-spacing .02em, with tagline **`Powered by Akki OS`** in mono 9.5px uppercase — the header brands FROM `Akki OS` (the platform) TO `{{ dataOwner }}` (the data-owner tenant); **it does NOT brand as "RMS · DATA ACCESS PORTAL".**
- Trust-domain pill: `"Partner access · {{ trustDomain }}"` (parametric).
- Identity block: `"{{ party }} · {{ principal }}"` + circular `{{ initials }}` badge — these are the REQUESTING PARTY's identity (external party principal per DAP-1), NOT the data owner's employee.

**Templating discipline (verbatim from `extraction_request_approval_journey.md` §1):**

> *"`RMS` is the example data owner used in this document's reference screenshots and examples — it is a stand-in, not a fixed name. Anywhere the data owner appears in copy the party actually sees, use the real data owner's name for that tenant, following the reference portal's own convention of templated values (e.g. `{{ dataOwner }}`, the same pattern the portal already uses for `{{ party }}` and `{{ principal }}`) rather than hardcoding "RMS.""*

The prototype uses handlebars-style tokens throughout (~40+ occurrences): `{{ trustDomain }}`, `{{ party }}`, `{{ principal }}`, `{{ initials }}`, `{{ pageTitle }}`, `{{ ovTitle }}`, `{{ navGroups }}`, `{{ reportVM.title }}`, `{{ landFigures }}`, `{{ estStats }}`, `{{ estTopline }}`, `{{ estTabs }}`, `{{ estOps }}`, `{{ availBar }}`, `{{ availRows }}`, `{{ broughtRows }}`, `{{ composition }}`, `{{ computeRows }}`, `{{ confirmDests }}`, `{{ chatLog }}`, `{{ agentRows }}`, `{{ agentTerms }}`, `{{ govPolicyRows }}`, `{{ govCollectionRows }}`, `{{ govContractRows }}`, `{{ historyRows }}`, `{{ modeFields }}`. Everything the party sees flows from a view-model, never a string literal.

**Layout (verbatim from prototype bytes 6900–7300):**

- Three-column: `dap-nav` (left, clamp(186px,19%,254px) sidebar) · `dap-body` (center, scrollable content) · `dap-rail` (right, request-lifecycle status rail — from the 2026-09-20 List of Changes, §Extract §"Moved `[Start another request]` button to the rail and always visible" + "created `By` status section that changes per Extraction type").
- Nav uses `sc-for list="{{ navGroups }}" as="g"` iterating group items — the nav content is data-driven, not hardcoded groups.
- No estate-card grid ("Audio 41.2 TB · Text & Documents 9.6 TB · Records 20.2 TB · Logs 5.8 TB · Messages 4.2 TB") is present in the LATEST prototype's landing markup by that hardcoded shape; landing figures render via `{{ landFigures }}` view-model.

**Behaviour contract (verbatim from `Front_End_Integration_Brief.md` §"payload contract"):**

> *"Empty responses must carry `honest_gap` and `not_measured: true`. Fabrication is a right-reason failure."*

> *"Where the repo's React app and the prototype differ in layout, navigation, naming, or interaction, the prototype wins."*

**Design-ID binding (from `notes/MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md`, verbatim):**

> *"Binding design: `prototype_v3`."*

Plus: `notes/spec_id_index.md` banks `dap_frontend_standalone` = artefact #1 (sha256 `d0fc1b498e07…` · 230,577 B). Artefact #7 (`RMS_DAP_LATEST.html` · 2026-09-20 · 221,620 B) is a later revision from the same lineage per the §0.2 reconciliation note; whether it should be re-banked as `dap_frontend_latest_20260920` is a **PENDING-OWNER-DECISION**.

### 1.3 · Where the current `/dap` render diverges

The current `/dap` surface is rendered by:
- `/app/frontend/src/pages/dap/DAPLayout.jsx` (chrome + sidebar)
- `/app/frontend/src/pages/dap/DAPLanding.jsx` (landing page body)
- `/app/frontend/src/pages/dap/DataEstates.jsx` (estate detail pages)

**Divergence catalogue (line-cited):**

1. **Header wordmark is HARDCODED to `RMS`** — `DAPLayout.jsx:137`: `RMS · Data Access Portal`. Owner canon requires `{{ dataOwner }} Data Access Portal · Powered by Akki OS` where `{{ dataOwner }}` = the data-owner tenant name (would be `Digicow` for a Digicow-tenant view, or generic if untenanted).
2. **Header MISSING the `Powered by Akki OS` tagline.**
3. **Header MISSING the trust-domain pill (`Partner access · {{ trustDomain }}`).**
4. **Header MISSING the `{{ party }} · {{ principal }}` identity block** — current identity in the top-right (`M. Chen · Compliance` per prior screenshot, but that's in the OLD v8_prototype iframe, not the /dap native surface).
5. **Sidebar NAV structure hardcoded (`DAPLayout.jsx::NAV_GROUPS`)**: sections `OVERVIEW / EXTRACT / AVAILABLE RESOURCES / DATA GOVERNANCE / CONNECT RESOURCES / REQUESTS / ENTITLEMENT / CEREMONY`. Owner canon requires `sc-for list="{{ navGroups }}"` — data-driven. The section labels themselves have precedent in the prototype but must render FROM a view-model.
6. **Landing body content is 100% HARDCODED** in `DAPLanding.jsx`: 
   - `ESTATES` object (lines 11–15) with 5 hard-coded estates + TB/pct/stratification.
   - `NOTES` array (lines 19–23) with 4 hard-coded copy strings.
   - `totalTB = Object.values(ESTATES).reduce(...) = 81.0` computed in-component.
7. **Right-side lifecycle rail is ABSENT** — the 2026-09-20 List of Changes explicitly moved `[Start another request]` and the per-status count section to the rail; the current /dap has no right rail at all.
8. **Estate-detail pages are HARDCODED** at `DataEstates.jsx` lines 13-14, 17-18, 26-27, 32, 38-39, 43-44, 50, 62-63, 67 — every stat + custody-narrative + note is a string literal referencing "Digicow" verbatim.
9. **Modes surface (`ExtractModes.jsx`)** — same pattern; string literals reference Digicow throughout (lines 20, 23, 28+).
10. **Governance surface (`DataGovernance.jsx`)** — same pattern (lines 235, 243+).
11. **Data-driven view-models not implemented.** The 27 `{{ ... }}` binding sites in the LATEST prototype have zero corresponding backend read paths in the frontend code.
12. **DAP-1..30 canon requirements not surfaced.** The `dap` API surface exposes `/api/canon/rules/dap` (canon rules) + `/api/portal/entitlement/*` (entitlement) + `/api/dap/buildskill/provisioning-records` (buildskill), but NO endpoint for landing figures, estate rollups, or request-lifecycle status.

---

## Investigation 2 · DATA HONESTY — where do the numbers come from

### 2.1 · Every asserted figure on the visible surface (§1.4 violation candidates)

Every figure is HARDCODED — none is measured. Full enumeration:

| Figure | File | Line | Value | Source |
|---|---|---|---|---|
| Total estate TB | `DAPLanding.jsx` | 33, 40 | `81.0` (computed from sum of ESTATES.tb) | HARDCODED (5 hardcoded estates summed) |
| Audio TB | `DAPLanding.jsx` | 11 | `41.2` | HARDCODED |
| Audio % | `DAPLanding.jsx` | 11 | `48` | HARDCODED |
| Audio standing / approval / closed | `DAPLanding.jsx` | 11 | `6.1 / 18.4 / 16.7` | HARDCODED |
| Text & Documents TB / % | `DAPLanding.jsx` | 12 | `9.6 / 11` | HARDCODED |
| Text & Documents stratification | `DAPLanding.jsx` | 12 | `3.4 / 4.1 / 2.1` | HARDCODED |
| Records TB / % | `DAPLanding.jsx` | 13 | `20.2 / 23` | HARDCODED |
| Records stratification | `DAPLanding.jsx` | 13 | `— / 4.6 / 15.6` | HARDCODED |
| Logs TB / % | `DAPLanding.jsx` | 14 | `5.8 / 7` | HARDCODED |
| Logs stratification | `DAPLanding.jsx` | 14 | `2.2 / 1.9 / 1.7` | HARDCODED |
| Messages TB / % | `DAPLanding.jsx` | 15 | `4.2 / 5` | HARDCODED |
| Messages stratification | `DAPLanding.jsx` | 15 | `— / 1.2 / 3.0` | HARDCODED |
| "Open to you" TB | `DAPLanding.jsx` | 78 | `11.7 TB` | HARDCODED (literal string) |
| "Needs sign-off" TB | `DAPLanding.jsx` | 87 | `30.2 TB` | HARDCODED (literal string) |
| "Not available" TB | `DAPLanding.jsx` | 96 | `39.1 TB` | HARDCODED (literal string) |
| NOTES "30.2 TB more…" | `DAPLanding.jsx` | 19 | full copy | HARDCODED |
| NOTES "Call recordings are 41.2 TB…" | `DAPLanding.jsx` | 20 | full copy | HARDCODED |
| NOTES "11.7 TB is open to you now…" | `DAPLanding.jsx` | 21 | full copy | HARDCODED |
| DataEstates.jsx Audio row | `DataEstates.jsx` | 13-14 | `41.2 TB · 48%` · `287,800 recorded calls · 61,400 hours` · custody + notes strings | HARDCODED |
| DataEstates.jsx Text row | `DataEstates.jsx` | 26-32 | `9.6 TB · 11%` · `9,140 complaint files · 2.1M pages` + strings | HARDCODED |
| DataEstates.jsx Records row | `DataEstates.jsx` | 38-44 | `20.2 TB · 23%` + strings | HARDCODED |
| DataEstates.jsx Logs row | `DataEstates.jsx` | 50 | `5.8 TB · 7%` + strings | HARDCODED |
| DataEstates.jsx Messages row | `DataEstates.jsx` | 62-67 | `4.2 TB · 5%` · `1.4M email threads` + strings | HARDCODED |
| ExtractModes.jsx dependents | `ExtractModes.jsx` | 20, 23, 28+ | Digicow-referenced copy | HARDCODED |
| DataGovernance.jsx dependents | `DataGovernance.jsx` | 235, 243+ | Digicow-referenced copy | HARDCODED |

**Total asserted-figures count on the primary /dap landing:** **17 numerical figures** + **4 narrative NOTES strings**, all hardcoded, none traceable to any census run.

### 2.2 · Comparison against the live measured census

Live census-3 measured (from `/api/census/latest` census_v3_extensions, verified 2026-02-23T~18:00Z probe):
- **Total OBS estate:** 950,791 objects · **161.76 TB** across 106 buckets (lower-bound; 33 buckets have >20k objects, capped list).
- Per-region: tr-west-1 130.38 TB · af-south-1 31.22 TB · ap-southeast-3 0.16 TB · ap-southeast-1 0.00 TB.
- Readable-bucket access: 32 readable / 74 blocked.

**Discrepancy:** the /dap landing asserts 81.0 TB (Digicow-branded). Live census measured 161.76 TB (RMS-tenant scope; blocked buckets on na7p4* pending DQ-05 owner IAM grant). **The 81.0 TB figure has NO relationship to any measured value on any tenant.**

### 2.3 · §1.4 violation classification

The DAP surface is a USER-FACING product surface bound by:
- **Canon-4 §1.4** (owner-drop directive stored in `Front_End_Integration_Brief.md` §"payload contract" verbatim): *"Empty responses must carry honest_gap and not_measured: true. Fabrication is a right-reason failure."*
- **Doc-15 §honest-empty** discipline (referenced throughout the wave-close notes).

**Verdict: 17 asserted figures + 4 narrative notes on the primary landing** each constitute a §1.4 fabrication violation. `DataEstates.jsx` + `ExtractModes.jsx` + `DataGovernance.jsx` add another ~30 hardcoded Digicow-referenced strings. Approximate total: **~50 §1.4 violations on the DAP surface** (P0-scale; the entire surface fabricates).

**No `honest_gap` marker, no `not_measured: true` marker, no INFERRED regime tag appears anywhere in `DAPLanding.jsx` / `DataEstates.jsx` / `ExtractModes.jsx` / `DataGovernance.jsx`** — this is the machine-readable signal the surface owes at every unmeasured figure per the frozen backend contract.

---

## Investigation 3 · TENANT SCOPING — why RMS header shows Digicow data

### 3.1 · The wiring

- **Header wordmark:** hardcoded string `RMS · Data Access Portal` at `DAPLayout.jsx:137`. Not read from any tenant identity.
- **Body copy:** hardcoded strings referencing `Digicow` at 15+ line sites across `DAPLanding.jsx`, `DataEstates.jsx`, `ExtractModes.jsx`, `DataGovernance.jsx`.
- **Identity block:** absent from the native `/dap` route (the top-right identity "M. Chen · Compliance" the owner saw is from the OLD v8_prototype iframe at `/`, not from `/dap`).
- **JWT identity ↔ tenant binding:** the auth response includes `identity.email` + `identity.roles` (verified in prior investigation 2026-02-23T~18:47Z curl) but **no `tenant_id` field**. The 4 seeded demo accounts live under `@demo.rms.example.com` — none carry an explicit tenant claim.
- **No tenant-read path from front-end:** `DAPLanding.jsx` performs zero fetch/API calls. Every value renders from module-scope constants.

### 3.2 · Is there any REAL cross-tenant read path?

**No.** The /dap frontend does not read from any tenant-scoped backend at all — there is no data path. The "RMS-brand + Digicow-body" mixing is a UI DEMO-COPY DEFECT, not a cross-tenant data leak.

### 3.3 · Should CP-TENANT-SEPARATION invariant have caught this?

**No.** CP-TENANT-SEPARATION (Item 5.11.d · sealed) invariants (`test_cp_tenant_separation.py`):

Verbatim owner-card scope from `test_four_tenants_declared_verbatim`: *"RMS — organisation principal, own trust-domain identifier, own Ledger, own context key, own licence. DIGICOW — same, independently. AKKI-TEST — a dedicated test tenant."*

And from `test_every_source_has_tenant_id`: *"Each connector record, each census artefact (`census_0001/0002` → DIGICOW; Item-3 receipts → RMS), each source_inventory row, each stratified sample, each cost receipt carries its `tenant_id` via the `akki.data` primitive — auto-injected, never caller-supplied (M11, AKKI-DATA-001)."*

CP-TENANT-SEPARATION invariant is **BACKEND data-flow scoped**: it enforces `tenant_id` propagation across connector records, census artefacts, source_inventory rows, stratified samples, and cost receipts through the `akki.data` primitive. A frontend page with hardcoded literal strings has no data flow and lives entirely outside the invariant's scope.

**However — an ADJACENT invariant SHOULD exist and does not.** A companion invariant like `test_dap_frontend_has_no_hardcoded_tenant_literals` would have caught this at the frontend layer. That would be a new invariant seat authored as part of the corrective plan (§5.3 below), not a retroactive defect of the existing sweep.

### 3.4 · Tenant confusion classification

Not a data-separation defect. **A brand-confusion defect** — the surface presents `RMS`-branded chrome overlaying `Digicow`-referenced body copy, which is neither the RMS view nor the Digicow view; it is a **mixed-tenant seeded-demo state that no real tenant can actually be** and violates the owner canon "hardcoding RMS is banned" clause verbatim.

---

## Investigation summary · verdict on WHY the owner saw V1 in the prior diagnostic

The prior diagnostic (2026-02-23T~19:08Z) reported /dap as "fully-native React DAP portal" and captured a screenshot of it. That characterisation was **partially correct at the render-technology level** (native React, no iframe) but **catastrophically incorrect at the design-fidelity level**. The correct verdict, evident now with the owner's LATEST prototype opened byte-verified:

**The `/dap` route renders a seeded demo COPY of the DAP surface, not the owner's DAP.** Every figure is hardcoded, tenant branding is confused (`RMS` header + `Digicow` body), the right lifecycle rail is missing, the 27 view-model tokens have zero data path, and there is no `honest_gap` marker on any of the ~50 §1.4-fabrication points.

The owner's "This is nothing close to DAP i gave you to build" is dead accurate. My prior diagnostic report understated it.

---

## CORRECTIVE PLAN (P0 · DO NOT EXECUTE until owner GO)

### §5.1 · Scope of the rebuild

**Retire:** the current `DAPLanding.jsx` + `DAPLayout.jsx` chrome + `DataEstates.jsx` + `ExtractModes.jsx` + `DataGovernance.jsx` seeded copy — retire-supersede in place (files stay on disk as prior implementations; no live route serves them once superseded).

**Author:** native-React port of `RMS_DAP_LATEST.html` chrome + landing + Extract mode surfaces bound to a NEW backend contract `services/dap_frontend/*` that serves the 27 view-model tokens from real reads (tenant-scoped, entitlement-scoped, census-scoped) with `honest_gap` + `not_measured: true` markers wherever a figure is not yet measured.

### §5.2 · Design authority + version pin (PENDING-OWNER-DECISION P-A)

Pin the **operative design** as `dap_frontend_latest_20260920` = `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` (221,620 B). Re-bank sha256 in `notes/spec_id_index.md` at commission time. Retire the prior `dap_frontend_standalone` = 2026-09-09 revision from binding-canon status (still on disk as archive).

**Alternative interpretation for owner clearance:** keep BOTH revisions live but treat the 2026-09-20 LATEST as strictly-newer supersede. Owner picks.

### §5.3 · Backend seam (additive)

New service module `services/dap_frontend/view_model_v1.py` with 27 view-model dataclasses matching the prototype's `{{ ... }}` binding sites. Each dataclass carries:
- `honest_gap: str | None` (verbatim sentence rendered when the value is not measured).
- `not_measured: bool = True` default; flipped to False only on a receipted measurement.
- `tenant_id: str` (auto-injected from JWT identity → tenant binding · never caller-supplied · via existing `akki.data` primitive per M11).
- `regime: Literal["MEASURED", "INFERRED", "UNMEASURED"]` per §6.9 markers.

New API routes (all under `/api/portal/dap/*`, tenant-scoped by middleware):
- `GET /api/portal/dap/landing/figures` → `LandFigures_v1` (topline TB + per-estate rollup)
- `GET /api/portal/dap/nav/groups` → `NavGroups_v1` (sidebar nav data-driven)
- `GET /api/portal/dap/estate/{estate_id}` → `EstStats_v1 + EstTopline_v1 + EstTabs_v1 + EstOps_v1`
- `GET /api/portal/dap/availability` → `AvailBar_v1 + AvailRows_v1`
- `GET /api/portal/dap/governance/policy` → `GovPolicyRows_v1`
- `GET /api/portal/dap/governance/collection` → `GovCollectionRows_v1`
- `GET /api/portal/dap/governance/contract` → `GovContractRows_v1`
- `GET /api/portal/dap/history` → `HistoryRows_v1`
- `GET /api/portal/dap/compute` → `ComputeRows_v1`
- (~15 additional routes matching the remaining view-model tokens)

Each route returns `{"honest_gap": "...", "not_measured": true, "value": null}` when unmeasured (per the frozen backend contract). Endpoints are auto-tenant-scoped via the `akki.data` M11 primitive; a request under a different tenant returns 404 or an empty scope, never cross-tenant data.

### §5.4 · Frontend seam (additive)

New components under `frontend/src/pages/dap/v2/` (parallel to the retired v1 tree · one-way switch at the route table):
- `DAPShell.jsx` — chrome (top bar + trust-pill + party identity + 3-column layout).
- `DAPLandingV2.jsx` — landing body bound to `/api/portal/dap/landing/figures`.
- `DAPExtractV2.jsx` — Extract module with lifecycle rail (per 2026-09-20 List of Changes §Extract).
- `DAPEstateV2.jsx` — Estate detail bound to `/api/portal/dap/estate/{estate_id}`.
- `DAPGovernanceV2.jsx` — Governance surfaces.
- `DAPRequestsV2.jsx` — Request lifecycle drawer (In Approval / Executing / Ready / Retrieved / Refused / Blocked / Expired · from `extraction_request_approval_journey.md`).

Copy discipline (SO §6.9(1) hardcode-ban):
- Zero hardcoded `RMS` / `Digicow` / TB figures in JSX.
- All text renders from view-model with `honest_gap` fallback verbatim.
- Header `wordmark` = `{data_owner_tenant.name} Data Access Portal · Powered by Akki OS` where `data_owner_tenant.name` is read from the tenant-scoped view-model.

### §5.5 · New invariant seats to author (RED-first)

- `test_dap_frontend_v2_has_no_hardcoded_tenant_literals` — grep-scan JSX for banned literals.
- `test_dap_frontend_v2_carries_honest_gap_marker_on_every_figure` — per-figure render honestly.
- `test_dap_frontend_v2_reads_view_model_only` — no numeric literal in JSX outside test-fixture files.
- `test_dap_frontend_v2_tenant_scoped_reads` — every `/api/portal/dap/*` call is behind the JWT-tenant middleware.
- `test_dap_backend_view_model_v1_carries_all_27_tokens` — every prototype `{{ ... }}` binding has a corresponding backend field.
- `test_dap_backend_view_model_v1_defaults_not_measured_true` — default honest-gap posture is `not_measured=True`.
- `test_prototype_v3_supersede_by_dap_frontend_latest_20260920` — banks the operative design binding.

Approx ratchet delta: **+35 to +50 tests** (RED-first per SO §3.8).

### §5.6 · Scope estimate (honest UNMEASURED)

- **Backend seam:** ~600–900 lines python across 3 modules + ~15 new routes.
- **Frontend seam:** ~800–1200 lines JSX across 6 new components (retiring ~500 lines of legacy hardcoded JSX).
- **Invariant seats:** ~35–50 new tests.
- **Byte-identity mirror to pod_shell/frontend maintained throughout** (both trees updated at every commit).
- **Estimated seal size:** M–L class; 2–4 code commits under Standing Order §3.8 additive-only. Full 6-commit chain per seal-discipline standard. Owner may authorise splitting into sub-seals (chrome first / view-model backend second / lifecycle rail third).

### §5.7 · Interaction with the pending CP-SINGLE-SURFACE-RULING

Two clean options for owner clearance:

**Option A · Land single-surface first, then DAP-fidelity.** The single-surface ruling is a 2-line App.js swap already double-green at 6421 passed. Land it as Item 5.15 (1-day seal), then open DAP-FIDELITY-P0 as Item 5.16 (multi-day seal). Sequences correctly because /dap becomes the single URL surface first, then the DAP surface itself gets rebuilt.

**Option B · Fold both into one seal.** Land the single-surface swap + DAP-fidelity rebuild as one combined Item 5.15 (larger seal). Slower to first-commit but avoids two ratchet events on adjacent surfaces.

Owner picks. Default recommendation: **Option A** — the single-surface ruling is already at double-green; landing it now closes the acknowledged wiring gap without waiting on the larger rebuild.

### §5.8 · Screenshots captured this diagnostic (banked)

- `/app/assessment_workspace/phase0/eyeball_proxies/20260923T190000Z_owner_diag_A_root_landing.png` — `/` (V8 iframe · the "RMS AI" shell the owner remembers)
- `/app/assessment_workspace/phase0/eyeball_proxies/20260923T190500Z_owner_diag_B_os_work_commission.png` — `/os/work/commission` (native React WorkCommission · Canon 5 §14 Shaping Wizard)
- `/app/assessment_workspace/phase0/eyeball_proxies/20260923T190800Z_owner_diag_C_dap_landing.png` — `/dap` (the seeded-demo DAP surface the owner rejected)

### §5.9 · Owner ratification required (report-back checkpoint)

Per owner directive verbatim: *"This is a report-back checkpoint — do not start the rebuild without my GO."*

Ratification needed on:
- (a) Version pin decision — bank `dap_frontend_latest_20260920` as new operative design_id? Y/N.
- (b) Chronology — Option A (single-surface first) or Option B (combined seal)?
- (c) Scope-cut authority — is the full 27-token view-model + lifecycle rail + Extract request drawer in scope for this seal, or do we cut to a sub-scope (e.g., chrome + landing figures only, rail + drawers deferred to a follow-on seal)?
- (d) Tenant-binding decision — should the JWT identity carry an explicit `tenant_id` claim (breaking change to auth), or should tenant be derived from the identity email domain / a separate seed table? Owner picks.

---

**Ledger check:** this incident receipt implements Item 5.14-adjacent P0 DAP-FIDELITY diagnostic and nothing else. Additive-only per SO §3.8. NO code delta. NO rebuild executed. Awaiting owner GO on the corrective plan above. All 6 Standing Bans + 17 Standing Guards + SO §6.9 + Ruling (b) AKKI-RUNS-IT verbatim remain binding meanwhile. **HALT** awaiting owner clearance.
