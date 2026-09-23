# UI-FIDELITY-P0 · Combined Incident Receipt · 2026-02-23T~19:40Z

**Owner verbatim escalation ladder:**
- 2026-02-23T~19:15Z: *"This is nothing close to DAP i gave you to build - I'm getting seriously worried."*
- 2026-02-23T~19:30Z: *"This is a problem with OS too. do both reports together."*

**Class:** P0 · owner-escalated fidelity defect · **widened** to cover BOTH the DAP surface AND the v2 OS shell surface.

**Surfaces at fault:** `/dap` (native React DAP portal) + `/` (v8 prototype iframe `<PortalIframe/>`) + 37 `/os/*` native React leaves.

**Status:** DIAGNOSTIC ONLY. **NO REBUILD executed.** Awaiting owner GO on the combined corrective plan (§7 below).

**Adjacent work status (STILL paused at double-green, uncommitted):** CP-SINGLE-SURFACE-RULING seal from the 2026-02-23T~19:00Z ruling remains at DOUBLE-GREEN 6421 passed / 13 skipped / 0 failed with code changes STAGED in both trees + 4 scaffolding tests updated + new test file GREEN, but UNCOMMITTED. That seal is DOWNSTREAM of this P0 — the single-surface `/` = OS-shell target depends on this diagnostic's OS half.

---

# PART I — DAP SURFACE FINDINGS

## Investigation 1 (DAP) · Design Authority

### 1.1 · Owner-provided DAP artefacts located (all opened this session)

| # | Path (abs) | Timestamp | Size | Kind |
|---|---|---|---|---|
| 1 | `canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html` | 2026-09-09 08:55 | 230,577 B | HTML prototype (owner-labelled) |
| 2 | `canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` (sha256 `e675990a…`) | 2026-09-09 | 21,346 B | Canon DAP-1..30 |
| 3 | `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | 2026-09-09 | — | Extracted text of #2 |
| 4 | `custody/owner_drops/20260920T0824Z/RMS_Data_Access_Portal.html` | 2026-09-20 08:25 | 327,266 B | Mid-day rev |
| 5 | `custody/owner_drops/20260920T0824Z/DAP_Backend_Engineering_Brief.md` (sha256 `3c9be715…`) | 2026-09-20 08:24 | — | Backend brief |
| 6 | `custody/owner_drops/20260920T0824Z/Front_End_Integration_Brief.md` (sha256 `4a5fd146…`) | 2026-09-20 08:24 | 53,284 B | FE brief |
| 7 | **`custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html`** | **2026-09-20 11:48** | **221,620 B** | **HTML prototype (LATEST · operative)** |
| 8 | `custody/owner_drops/20260920T1140Z/DAP_List_of_Changes_20260920.docx` | 2026-09-20 11:48 | 16,645 B | Delta doc (Data-Estate + Extract) |
| 9 | `custody/owner_drops/20260920T1140Z/extraction_request_approval_journey.md` | 2026-09-20 11:48 | — | Extraction journey spec |
| 10 | `notes/DAP_SPEC_REVISION_RECONCILIATION_20260920.md` | 2026-09-20 08:35 | — | Session reconciliation |
| 11 | `notes/canon_dap_backend_spec_v1_requirements.md` | 2026-09-09 ingest | — | DAP-1..30 enumeration |
| 12 | `notes/W_DAP_STACK_2A_close.md` | 2026-09-13 wave-close | — | DAP-STACK 2A close (ratchet 3560→3570) |

### 1.2 · What the owner's DAP design actually specifies (verbatim from #7 + #9 + #6)

- **Header wordmark:** `Digicow Data Access Portal · Powered by Akki OS` on `--blue2:#0f1b33` 52-px bar. Wordmark uses `{{ dataOwner }}` template, NOT hardcoded `RMS`.
- **Templating discipline** (verbatim from #9 §1): *"`RMS` is the example data owner used in this document's reference screenshots and examples — it is a stand-in, not a fixed name. Anywhere the data owner appears in copy the party actually sees, use the real data owner's name for that tenant, following the reference portal's own convention of templated values (e.g. `{{ dataOwner }}`, the same pattern the portal already uses for `{{ party }}` and `{{ principal }}`) rather than hardcoding "RMS.""*
- **View-model tokens (27 identified in #7):** `{{ trustDomain }} · {{ party }} · {{ principal }} · {{ initials }} · {{ pageTitle }} · {{ ovTitle }} · {{ navGroups }} · {{ reportVM.title }} · {{ landFigures }} · {{ estStats }} · {{ estTopline }} · {{ estTabs }} · {{ estOps }} · {{ availBar }} · {{ availRows }} · {{ broughtRows }} · {{ composition }} · {{ computeRows }} · {{ confirmDests }} · {{ chatLog }} · {{ agentRows }} · {{ agentTerms }} · {{ govPolicyRows }} · {{ govCollectionRows }} · {{ govContractRows }} · {{ historyRows }} · {{ modeFields }}` — every user-visible value flows from a view-model.
- **Layout:** 3-column (`dap-nav` left · `dap-body` center · `dap-rail` right for lifecycle status per 2026-09-20 List of Changes §Extract).
- **Behaviour contract** (verbatim from #6 payload contract): *"Empty responses must carry `honest_gap` and `not_measured: true`. Fabrication is a right-reason failure."*
- **Version-pin:** #7 (`RMS_DAP_LATEST.html`) is the operative design. Reconciliation note #10 §0.2 raises open question about the earlier `dap_frontend_standalone` (sha256 `d0fc1b498e07…` at #1) — likely superseded by #7 · PENDING-OWNER-DECISION.

### 1.3 · Divergence catalogue (12 findings · line-cited)

1. **Header hardcoded to `RMS`** at `DAPLayout.jsx:137` (`RMS · Data Access Portal`). Owner canon: `{{ dataOwner }} Data Access Portal · Powered by Akki OS`.
2. Missing `Powered by Akki OS` tagline.
3. Missing trust-domain pill `Partner access · {{ trustDomain }}`.
4. Missing `{{ party }} · {{ principal }}` identity block.
5. Sidebar NAV hardcoded (`DAPLayout.jsx::NAV_GROUPS`) instead of data-driven `sc-for list="{{ navGroups }}"`.
6. Landing body 100% HARDCODED in `DAPLanding.jsx` (`ESTATES` dict lines 11-15, `NOTES` array lines 19-23, `totalTB = 81.0` computed from hardcoded sum).
7. Right-side lifecycle rail ABSENT (2026-09-20 List of Changes explicitly moved `[Start another request]` + per-status counts there).
8. `DataEstates.jsx` lines 13-14, 17-18, 26-27, 32, 38-39, 43-44, 50, 62-63, 67 — every estate detail hardcoded.
9. `ExtractModes.jsx` lines 20, 23, 28+ — Digicow-referenced strings hardcoded.
10. `DataGovernance.jsx` lines 235, 243+ — same pattern.
11. Data-driven view-models NOT implemented — 27 `{{ ... }}` binding sites in the prototype have ZERO backend read paths.
12. DAP-1..30 canon requirements NOT surfaced beyond `/api/canon/rules/dap` + `/api/portal/entitlement/*` + `/api/dap/buildskill/provisioning-records` (3 wired routes vs ~15 needed).

## Investigation 2 (DAP) · Data Honesty · asserted-figure enumeration

**17 numerical figures + 4 narrative NOTES + ~30 hardcoded Digicow strings across sub-pages = ~50 §1.4 fabrication violations on the primary /dap landing + nested surfaces.**

Every figure is HARDCODED. Sample (full table in `dap_half_original_receipt/incident_receipt.md` §2.1):

| Figure | Source line | Value | Traceable to census? |
|---|---|---|---|
| Total estate TB | `DAPLanding.jsx:33` | `81.0` (computed) | NO |
| Audio TB/% | line 11 | `41.2 / 48` | NO |
| Text TB/% | line 12 | `9.6 / 11` | NO |
| Records TB/% | line 13 | `20.2 / 23` | NO |
| Logs TB/% | line 14 | `5.8 / 7` | NO |
| Messages TB/% | line 15 | `4.2 / 5` | NO |
| "Open to you" | line 78 | `11.7 TB` literal | NO |
| "Needs sign-off" | line 87 | `30.2 TB` literal | NO |
| "Not available" | line 96 | `39.1 TB` literal | NO |

**Live census-3 measured (from `/api/census/latest` 2026-02-23T~18:00Z):** 950,791 objects · **161.76 TB** across 106 buckets (RMS-tenant scope). The 81.0 TB DAP figure has NO relationship to any measured value on any tenant. Zero `honest_gap` / `not_measured` markers anywhere.

## Investigation 3 (DAP) · Tenant Scoping

- Header hardcoded `RMS · Data Access Portal` (`DAPLayout.jsx:137`) — not tenant-derived.
- Body strings hardcoded `Digicow` at 15+ sites — not tenant-derived.
- No fetch/API calls in `DAPLanding.jsx` — no data path, no cross-tenant leak.
- JWT identity carries `email + roles` but **no `tenant_id` claim** (verified via `/api/auth/login` curl 2026-02-23T~18:47Z).
- CP-TENANT-SEPARATION invariant is BACKEND-scoped (`test_every_source_has_tenant_id` enforces `tenant_id` on connector records / census artefacts / source_inventory / stratified samples / cost receipts via `akki.data` primitive). Frontend hardcoded literals live outside its scope — invariant could not have caught this and is not defective.
- **Verdict:** brand-confusion defect (`RMS`-header + `Digicow`-body = mixed-tenant state that no real tenant can actually be), NOT a data-separation defect.

---

# PART II — OS SHELL FINDINGS

## Investigation A (OS) · Design Authority

### A.1 · Investigation of the 4 candidate sources (owner priority order)

**(1) Akki-OS-V1 repo (owner's initialization reference):**

- **Path:** `/app/assessment_workspace/repos/Akki-OS-V1/`
- **README verbatim:** *"# RMS Intelligence System · A governed, multimodal intelligence system. Reads multimodal estate material via the Akki engine (Layers A→B→C→D), exposes a Normalized Tier of Five Rings units, and serves intelligence via Service 1 (Day Zero) and Service 2 (Day-to-Day) under three governors: SyniSense (boundary), Northena (direction), Solva (depth). Estate is mapped by Mtafiti and targeted by Targeta."*
- **Spec authority declared in README:** *"RMS Product & Engineering Spec v2.0 · RMS UX Architecture Briefing v2.0 · RMS Architecture Deck v2.0 · RMS Emergent Build Kickoff & Development Contract."*
- **App.js routes (83 lines, verbatim from `frontend/src/App.js`):**
  - `/` → `AskConsolePage` (ChatGPT-style ask/answer console)
  - `/auth/login`, `/auth/register` → auth pages
  - `/trace`, `/trace/:traceId` → trace receipt pages
  - `/operator/*` (operator role): `operator` home, `operator/commission`, `operator/commit-review/:sessionId`
  - `/engineer/*` (engineer role): `engineer/register`, `engineer/first-call`, `engineer/administer`, `engineer/onboarding`
  - `/master-admin/*` (master-admin role): home, `change-a-rule/:ruleId`, `audit-trail`
  - `/compliance/*` (compliance role): home, `prove`, `prove/:traceId`, `retention`, `rulebook`
  - `/extraction/*`: `console`, `registry-admin`
  - `/opportunity-briefs`
  - `*` → `Navigate to="/" replace` (single-surface rule from inception)
- **IA:** ROLE-based (operator / engineer / master-admin / compliance / extraction) with a single ask-console landing.
- **Docs (`docs/mandates/`):** `akki_operating_model_product_spec_v2.0.docx`, `akki_role_register.docx`, `akki_analyze_codebase_acquisition_v1.0.docx`, plus 7 `source/RMS_*_Specification.docx` files (Northena, Targeta, Solva, Mtafiti, UX Architecture, Interface, Product Engineering).

**(2) Akki-Executive-Core repo:**

- **Path:** `/app/assessment_workspace/repos/Akki-Executive-Core/`
- **App.js routes (sampled):** `/` → `WebsiteHome`, `/why-akki`, `/what-akki-does`, `/trust`, `/cohort`, `/waitlist`, `/pricing`, `/about`, `/contact`, `/privacy`, `/terms`, `/methodology`, `/help`, `/help/:slug`, `/help-legacy`, `/status`, `/welcome/:token`, `/exco360`, `/thinklab`, plus many `ProtectedRoute`-guarded operator surfaces.
- **IA:** Marketing website + protected operator surfaces. Distinct product from Akki-OS-V1.

**(3) RMS-IQ-Core-2 repo:**

- **App.js routes (sampled):** `/` → `CanonOSShellPage`, `/auth/*`, `/trace/*`, `/connect/*` (5 routes: home, new, rules, source-profile, setup), `/registry/*`, `/memory/*` (planes + observability), `/use-data/*` (landing, wizard, developer-surface, verdict-demo, verdict-panel), `/govern/*` (retention, change-rule, refusal-health, pending, rules, registries).
- **IA:** Different again — `/connect · /registry · /memory · /use-data · /govern` (data-plane oriented). Landing = `CanonOSShellPage`.

**(4) OWNER_DROPS + notes for OS shell spec:**

- **Owner drop `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html`** (2,286,992 B · sha256 `9952692ce058…`) — HTML prototype (working head of `prototype_v3` lineage per `OS_PROTOTYPE_FRONTENDS_CARD_20260920.md` §0.2 note).
- **Canon HTML `canon/drops/20260909/raw/RMS_AI_Prototype_standalone_v3.html`** — banked as `prototype_v3` (design_id).
- **v8 canon** at `notes/prototype_inventory_v8.md`: identifies `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` (sha256 `e56871d0…` · 1,264,425 B) + `fixtures/Akki_Platform_v8_Design_Spec.docx` (sha256 `d7cfd3ae…` · 108,191 B).
- **v8 docx quotes verbatim:**
  - *"Akki is a unified AI governance and intelligence platform for an operating company. It combines a grounded chat assistant, document and task workflows, performance monitoring (Exco 360 / Board 360), an AI agent and model registry, a security-monitoring service ('The Watch' / 'Grey Mirror'), and a full rules-and-entitlements governance layer ('Shield') — all backed by one append-only audit record."* (§1 line 12)
  - *"This build is branded RMS AI. The wordmark in the top bar is the only literal brand token in the file; the identical underlying product has previously shipped under other brand names (BDO AI, DigiCow AI, TrinityAI) by swapping that one string."* (§1 line 13)
  - *"Four-questions surfaces. Rule zero: every block leads with a sentence; measures live behind 'see the working'."* (§1 line 15 · design law)
- **`OS_PROTOTYPE_FRONTENDS_CARD_20260920.md`** (approved-draft) — specialist-dispatch card citing `RMS AI Prototype v2 ACTIVE.dc.html` as the design of record. §1 verbatim: *"DAP portal is OUT of card scope — held pending Step 9 (PRINCIPAL MODEL WAVE) seal per owner directive verbatim. Principal-wave seal is the last gate on DAP portal frontend work."*
- **Owner ruling 2026-09-20T~08:56Z verbatim** (from `OS_PROTOTYPE_FRONTENDS_CARD_20260920.md` §1): *"(i) draft the frontends card for the OS-prototype surfaces ONLY citing the Front End Integration Brief — DAP portal is OUT of card scope until the owner answers §2.1."*
- **DAP↔OS nesting confirmed by owner artefacts:** the OS prototype has a "Portal mode (no app open)" per v8 docx §3.2; the DAP is a SEPARATE portal for external parties (party principal per DAP-1). They are **PEER surfaces owned by the same platform**, NOT one nested inside the other. The OS shell is for the DATA-OWNER's internal roles; the DAP is for external requesting parties.

### A.2 · Divergence: what the OS prototype specifies vs what /os/* renders

**Owner's operative binding (per `OS_PROTOTYPE_FRONTENDS_CARD_20260920.md` §1):** `RMS_AI_Prototype_v2 ACTIVE.dc.html` (2,286,992 B · working head of `prototype_v3` lineage) — SUPERSEDES v8 (`e56871d0…` · 1,264,425 B) unless owner rules otherwise. Version pin is PENDING-OWNER-DECISION per Brief §0.2.

**Owner's OS surface inventory (per Brief §3 · cited in the frontends card §5):**

- **WorkStudio (7 destinations):** Chat (P — `POST /api/chat/ask` wired · single-turn only) · Data Suite (G) · Documents (G) · My Work (G · Perform 360 backend plane new) · My Team (G) · Company Goals (G · Perform 360) · Board (G · Perform 360)
- **ThinkLab (4 destinations · best-aligned group):** Seek Clarity (W) · Develop Strategy (W) · Test Hypothesis (W) · Get Perspective (W) — all bound to `/api/thinklab/*` · stage-count mismatch resolved 5-stages-not-4 per backend config
- **Collab (4 destinations · largest wholly-unbacked group):** [Mentions · Emails · Projects/Tasks · HR Stuff]
- **Internal operator surfaces:** Manage Estate · Approvals · Build Your Resources · Your Resources · 3rd Party Apps / Integration Console · The Watch · Grey Mirror

**Current v2 shell renders:**
- **`/` route:** `<PortalIframe/>` → iframes `/v8_prototype.html` (sha256 `e56871d0…` · v8 · superseded by v2 2026-09-20 per §A.1). Header wordmark `RMS AI`. Tabs Work/Build/3rd Party Apps/Admin. Tiles WORKSTUDIO/THINKLAB/COLLAB/PERFORMANCE MANAGEMENT. WaveG4 substituted ~10 tile values with real data; the rest remain dummy.
- **37 native `/os/*` leaves** (Turn-4 sub-slice 4d 9 + 4e 14 + 4f 14 = 37): each declares `HONEST GAP · SURFACE ONLY` sentinel + honest-gap sentence + "see the working" pointer. Verified this session by screenshot at `/os/work/documents` (screenshot §5.5 below).

**Divergence catalogue:**

D1. **Version-pin mismatch:** current `/v8_prototype.html` is the v8 (1,264,425 B) prototype, superseded by owner v2 (2,286,992 B) at 2026-09-20. PENDING-OWNER-DECISION on which to bind.
D2. **Portal-mode dummy data:** WaveG4 landed ~10 tile-value substitutions (per waveG4 close report); the remaining ~30+ tile values in the v8 portal still render dummy content — that is what the owner is seeing.
D3. **Missing surfaces in native React:** 24 of 37 nav destinations show `HONEST GAP · SURFACE ONLY` (not fabrication — the surfaces truthfully declare they aren't wired yet · Turn-4 sub-slice discipline). This is HONEST but visibly incomplete.
D4. **ThinkLab config not consumed:** Brief §5.3 mandates render 5 stages from `config.stage_labels` (never hardcoded). Current `ThinkLabClarity/Strategy/Hypothesis/Perspective` surfaces (per grep this session) show `honest_gap` markers = 5 each · api-refs = 0 — they don't consume `/api/thinklab/config` at all. Contradicts the surface-integration brief §3.2 "best-aligned group."
D5. **WorkChat not wired to `/api/chat/ask`:** honest_gap markers = 6 · api-refs = 1 (in file · but per Brief §5.1 the surface should be fully bound to `POST /api/chat/ask`). At best it's stub-wired.
D6. **Shared refusal card not present** (Brief §2.2 requires ONE Canon 5 §9.2 verbatim refusal card routed through every surface that emits a refusal). No component matches this discipline in `/app/frontend/src/components/`.
D7. **Outer 403 handler missing** (Brief §1.3 mandates that `IPAllowlistMiddleware` 403 with `text/plain "This surface answers allowlisted addresses only."` renders as a dedicated full-surface state on first paint · not a login prompt · not an error state).
D8. **Perform 360 backend plane** (Brief §7.6) — NOT built at all (My Work / Company Goals / Board all `HONEST GAP`).
D9. **Data Suite** (Brief §7.5) — NOT built (`analyze` honest-gap).
D10. **Collab surfaces** (Brief §3.3) — NOT built (`mentions/emails/projects/hrstuff` honest-gap).
D11. **DAP↔OS crossover:** current wiring has `/dap` as a top-level route peer to `/`. Per owner design, DAP is a peer surface for external parties, not nested inside OS. **However the pending single-surface ruling 2026-02-23T~19:00Z would move `/` → `/dap` — that ruling conflicts with the OS-shell binding above and needs owner clarification.**

**Verdict on whether the current v2 OS shell was built from an owner artefact:** partially. The `/v8_prototype.html` iframe is byte-verbatim from the owner's v8 prototype (WaveG2/G3/G4 discipline). The 37 native `/os/*` leaves are HONEST-GAP scaffolding authored by the E1 build agent per owner-authorised Turn-4 sub-slices (RED-first · honest-empty · not fabrication). **But the v2 OS shell has NOT been built from the owner's LATEST binding `RMS_AI_Prototype_v2 ACTIVE.dc.html` (2026-09-20 · 2,286,992 B), which supersedes v8.** That is the design-of-record gap.

## Investigation B (OS) · Data Honesty · asserted-figure enumeration

Two distinct sub-surfaces:

**B.1 · The v8 prototype iframe at `/`** (`/app/frontend/public/v8_prototype.html`, 1.26 MB HTML with embedded dc-runtime + `<sc-for>`/`<sc-if>` templating):
- WaveG4 landed **10 tile-value substitutions** in `App.js::PortalIframe` (from `waveG4_close_report_addendum.md` §Correction-2): topline tiles (Held in total · Sources connected · Share measured · Data types present · Languages observed · Share already verified · Share carrying PII · Licensed for external use · Not yet measured · Reduced to reusable memory) — each `{label, dummy, render}` rule matched by `TreeWalker` text-node mutation with `ancestor.textContent.includes(rule.label)` disambiguation.
- **The remaining 30+ tile values** (Registry counts, agent lists, run history, task boards, chart data, etc.) render whatever dummy values the v8 prototype's own `dc-runtime` seed put there — none of them substituted, none of them measured. The owner is seeing this dummy data on tiles beyond the 10 substituted.
- **Estimated fabrication count on `/`:** ~30–50 dummy figures/labels/counts still rendering unsubstituted from v8 dc-runtime seed.

**B.2 · The 37 native React `/os/*` leaves** (in-source scan this session):

| Surface | Lines | honest_gap markers | API refs | Hardcoded numeric stats |
|---|---:|---:|---:|---:|
| WorkChat | 130 | 6 | 1 | 0 |
| WorkAnalyze | 109 | 5 | 0 | 0 |
| WorkDocuments | 86 | 5 | 0 | 0 |
| WorkTasks | 93 | 5 | 0 | 0 |
| WorkTeam | 87 | 5 | 0 | 0 |
| WorkPerformance | 93 | 5 | 0 | 0 |
| WorkBoard | 88 | 5 | 0 | 0 |
| MonitorSignals | 88 | 5 | 0 | 0 |
| MonitorIdeas | 88 | 5 | 0 | 0 |
| WorkCommission | 80 | 2 | 1 | 0 |
| ThinkLab (×4) | ~90 each | 5 each | 0 | 0 |
| /os/admin/* (10) | — | — (all `HONEST GAP · SURFACE ONLY`) | 0 | 0 |
| /os/build/* (6) | — | same | 0 | 0 |
| /os/apps/* (4) | — | same | 0 | 0 |

**Verdict:** 34 of 37 `/os/*` native leaves declare `HONEST GAP · SURFACE ONLY` sentinels + honest-gap sentences + "see the working" pointers. **This half is HONEST, not fabricated** — zero hardcoded numeric stats surveyed. 3 surfaces wire minimal API: WorkChat (1 fetch), WorkCommission (1 · via `<CommissionWizard/>`), ThinkLab (zero — regression from Brief §5.3 which said `/api/thinklab/config` should be consumed).

**Combined OS fabrication surface = the v8 iframe at `/`. The `/os/*` native leaves are not fabricating.**

## Investigation C (OS) · Tenant Scoping

- The v8 iframe at `/` runs on the tenant "RMS AI" wordmark hardcoded in the v8 HTML file itself. Per v8 docx §1 line 13, `RMS AI` is the ONLY literal brand token; swapping it makes the file a different tenant instance. Current file has `RMS AI` at byte position ≈1655.
- v8 dc-runtime seed values (dummy content on tiles) are file-embedded — nothing crosses tenants because nothing reads from tenants.
- The 37 `/os/*` native leaves have no data flow (0 API refs surveyed for 34 of them) — no tenant plumbing possible.
- **CP-TENANT-SEPARATION verdict:** same as DAP — invariant is backend-scoped; frontend file-embedded literals live outside its scope; invariant could not have caught this and is not defective.
- **Verdict:** No cross-tenant leak (no data flow at all). Same brand-lock defect as DAP: the v8 file hardcodes `RMS AI`; swapping to a different tenant requires editing that one string per v8 docx.

---

# PART III — DAP ↔ OS RELATIONSHIP (owner-artefact-derived · not invented)

**Confirmed peer-surface relationship (from owner artefacts opened this session):**

1. Per `OS_PROTOTYPE_FRONTENDS_CARD_20260920.md` §1 owner ruling verbatim: *"DAP portal is OUT of card scope until owner answers §2.1."* → DAP is a distinct surface class with its own binding, not a leaf inside the OS shell.

2. Per v8 docx §3.2 heading verbatim (from `notes/prototype_inventory_v8.md` scan): *"3.2 Portal mode (no app open)"* + *"'Exit' always returns to portal mode."* → the OS has an internal "portal mode" (the tile grid the user lands on) but that is DIFFERENT from the DAP portal.

3. Per `Front_End_Integration_Brief.md` §0: OS prototype = `RMS AI Prototype v2 ACTIVE.dc.html`, DAP prototype = `RMS Data Access Portal LATEST.dc.html` — **two distinct design-of-record files**, both authoritative for their respective surfaces.

4. **Party principals (DAP-1)** vs **internal roles (OS master-admin/operator/compliance/engineer)** — DAP serves external requesting parties who need admission per DAP-1 admission-mandate; OS serves internal data-owner roles. Different identity classes.

**Owner-artefact-derived DAP-OS nesting model:**

- **OS shell** is the platform's home for the DATA OWNER's staff (internal roles). Landing = the tile grid + tabs (WorkStudio · ThinkLab · Collab · Admin · Build · Apps + The Watch/Grey Mirror rollups).
- **DAP** is a SEPARATE surface reached by external requesting parties (party principals) — likely via a different subdomain, different JWT scope, or a linked-from-OS "manage external access" admin subsurface (this is a design decision the owner has not yet ruled on).
- The pending single-surface ruling 2026-02-23T~19:00Z (`/` = one URL surface, redirect `*` → `/dap`) may conflict with this two-tenant-role model. **Needs owner reconciliation** before either surface's rebuild.

**I have not invented the DAP-OS relationship — the owner's artefacts describe them as PEERS, not parent-child. The owner needs to rule on how they nest / co-exist / redirect between each other.**

---

# CORRECTIVE PLAN (P0 · single combined plan for both surfaces)

## §7.1 · Scope

**Rebuild BOTH surfaces coherently:**
- (a) The OS shell at `/` (retire v8 iframe · adopt v2 prototype bound to view-model backend).
- (b) The DAP surface (retire hardcoded `/dap/*` React pages · adopt `RMS_DAP_LATEST.html` bound to `/api/portal/dap/*` view-model backend).
- (c) The OS↔DAP relationship (per owner ruling on peer-surface nesting).

**Preserve:** the 37 `/os/*` native honest-gap leaves stay in place (they are honest, not fabricated); each is UPGRADED as its backend plane lands.

## §7.2 · Design version-pin (PENDING-OWNER-DECISION P-A)

- **OS shell:** pin `os_prototype_v2_20260920` = `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` (2,286,992 B · sha256 `9952692ce058…`) · SUPERSEDES `prototype_v3` (2,032,024 B) and v8 (1,264,425 B) per Brief §0.2 open question. **Owner rules or picks a different revision.**
- **DAP:** pin `dap_frontend_latest_20260920` = `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` (221,620 B) · SUPERSEDES `dap_frontend_standalone` (2026-09-09). **Owner rules.**
- Re-bank sha256s in `notes/spec_id_index.md` at seal boundary.

## §7.3 · OS↔DAP nesting decision (PENDING-OWNER-DECISION P-B)

Owner picks one of:

- **Option 1 · TWO peer surfaces at DIFFERENT top-level paths:** `/` = OS shell (single-surface for OS) · `/dap` (or `/portal`) = DAP surface (single-surface for DAP). This preserves the peer-surface intent of the owner's two design-of-records. Retires the single-surface ruling 2026-02-23T~19:00Z at this boundary (owner ruling supersedes owner ruling per SO §6.9(1)).
- **Option 2 · ONE URL surface with tenant/role-scoped landing:** `/` = single entry point → route to OS shell if JWT identity is internal role / to DAP if JWT identity is external party principal. Honors the single-surface ruling AND the two design-of-records.
- **Option 3 · DAP as an OS shell admin sub-surface:** `/` = OS shell · `/os/admin/external-parties` reveals DAP as a nested surface for admin management (but external parties never enter the OS shell). Requires distinct auth flow — external parties can't authenticate into the OS at all.

**Recommendation (advisory, owner decides):** Option 2 — single entry point + role-scoped landing — honors both rulings. The 2026-02-23T~19:00Z single-surface ruling was authored before the DAP fidelity issue surfaced; Option 2 is the coherent generalization.

## §7.4 · Backend seam (additive · new services)

**DAP-side** (`services/dap_frontend/view_model_v1.py` + ~15 new routes under `/api/portal/dap/*`) — per DAP-half receipt §5.3. Every route auto-tenant-scoped via `akki.data` M11 primitive; `honest_gap` + `not_measured: true` defaults per Brief §"payload contract."

**OS-side** (`services/os_shell/view_model_v1.py` + ~10 new routes under `/api/portal/os/*`):
- `GET /api/portal/os/portal-mode/tiles` → `OsPortalTiles_v1` (topline tiles the v8 substituted + the un-substituted ones)
- `GET /api/portal/os/nav/tabs` → `OsNavTabs_v1` (Work/Build/3rd Party Apps/Admin from data)
- `GET /api/portal/os/nav/groups` → `OsNavGroups_v1` (WORKSTUDIO/THINKLAB/COLLAB/PERFORMANCE MANAGEMENT + per-group tile list)
- `GET /api/portal/os/agents/registry` → `OsAgentRegistry_v1` (retires the v8 hardcoded seed `Vendor Risk Monitor` + `Payroll Variance Checker`)
- `GET /api/portal/os/watch/status` → `OsWatchStatus_v1` (The Watch service state)
- `GET /api/portal/os/greymirror/rollup` → `OsGreyMirrorRollup_v1`
- `GET /api/portal/os/shield/gate-status` → `OsShieldGateStatus_v1` (rules-and-entitlements governance rollup per v8 docx §1 line 12)
- `GET /api/portal/os/thinklab/config` (already exists · verify + wire consumption from ThinkLab surfaces)
- `POST /api/portal/os/chat/ask` (already exists · verify + wire consumption from WorkChat)
- + shared refusal-card component reusable by every surface that returns `refused: true` (Brief §2.2 Canon 5 §9.2 verbatim).

## §7.5 · Frontend seam (additive · retire-supersede pattern)

**New components under `frontend/src/pages/os/v2/`:**
- `OSShellV2.jsx` — chrome (52-px `--blue2` header · `RMS AI` wordmark + Powered-by-Akki-OS tagline · tab-group with WorkStudio/Build/Apps/Admin) — bound to view-model backend.
- `OSPortalModeV2.jsx` — landing tile grid bound to `/api/portal/os/portal-mode/tiles` with `honest_gap` render.
- **Retire** `<PortalIframe/>` element from live routing (v8 iframe stays on disk as archive; `public/v8_prototype.html` preserved).
- 37 existing `/os/*` native leaves KEPT AS-IS (honest-gap discipline preserved · they are correct, just incomplete).

**DAP-side (from DAP-half §5.4):** `frontend/src/pages/dap/v2/DAPShell.jsx` + `DAPLandingV2.jsx` + `DAPExtractV2.jsx` + `DAPEstateV2.jsx` + `DAPGovernanceV2.jsx` + `DAPRequestsV2.jsx`.

## §7.6 · New invariant seats (RED-first)

Combined for both halves:

**DAP invariants** (~7 seats): no-hardcoded-tenant-literals · honest_gap-per-figure · view-model-only · tenant-scoped-reads · 27-token-coverage · not-measured-default · design-supersede-pin.

**OS invariants** (~7 seats): no-hardcoded-tile-values · honest_gap-per-tile · shared-refusal-card-imported-not-duplicated · outer-403-full-surface-handler-present · thinklab-config-consumed · chat-ask-wired · perform-360-honest-gap-until-plane-lands.

Approx ratchet delta: **+30 to +50 tests combined**.

## §7.7 · Honest scope estimate (marked UNMEASURED)

- **Backend seam:** ~1200–1800 lines python across 6 modules + ~25 new routes across DAP + OS.
- **Frontend seam:** ~1500–2200 lines JSX across 10–12 new components (retiring ~500 lines legacy).
- **Invariant seats:** ~30–50 new tests.
- **Byte-identity mirror to `pod_shell/frontend`:** maintained throughout every commit.
- **Seal size:** L class. Recommend splitting into 3 sub-seals (per SO §6.9 ladder):
  - **Sub-seal 1 · OS shell chrome + portal-mode tiles** (retires v8 iframe · lands OSShellV2 · view-model backend for tiles + nav). ~1.5-day seal.
  - **Sub-seal 2 · DAP shell + landing + estate detail** (retires hardcoded /dap · lands DAPShell + LandingV2 + EstateV2 + view-model backend). ~1.5-day seal.
  - **Sub-seal 3 · Extract lifecycle + Perform 360 + Data Suite + Collab** (progressively lands the remaining honest-gap surfaces). Multi-day seal · owner ratifies per-plane.

## §7.8 · Interaction with the pending single-surface ruling

The 2026-02-23T~19:00Z single-surface ruling (`/` = OS shell · retire V1 iframe) is IN-FLIGHT AT DOUBLE-GREEN. Three coherent chronologies:

- **Path A · Land single-surface first, then rebuild:** Land the 2-line App.js route swap now (Item 5.15 · already double-green at 6421 passed · zero new invariant risk). Owner's `/` = the v2 DAP shell via redirect. Then open UI-FIDELITY-P0 as multi-sub-seal Item 5.16.
- **Path B · Fold single-surface into UI-FIDELITY rebuild:** Land the single-surface ruling as PART OF sub-seal 1 (retiring v8 iframe + retiring `/dap` peer-route + landing OSShellV2 at `/` all in one commit).
- **Path C · Rescind single-surface ruling in favour of Option 2 above (peer-surface):** If owner picks Option 2 in §7.3, the single-surface ruling supersedes back to a role-scoped landing, and Path B becomes the executed path.

**Recommendation:** Path B or Path C, depending on §7.3 owner decision. Path A leaves an inconsistent /dap for the intermediate period.

## §7.9 · Owner ratification checkpoints (report-back before rebuild)

Owner GO needed on:
- **(a)** OS-shell version pin — bind `os_prototype_v2_20260920` (2,286,992 B) OR `prototype_v3` (2,032,024 B) OR keep `v8_prototype` (1,264,425 B)?
- **(b)** DAP-shell version pin — bind `dap_frontend_latest_20260920` (221,620 B, 2026-09-20)?
- **(c)** OS↔DAP nesting — Option 1 (peer), Option 2 (role-scoped landing · recommended), Option 3 (DAP-as-admin-subsurface)?
- **(d)** Chronology — Path A (sequenced), Path B (folded), Path C (§7.3-driven)?
- **(e)** Scope cut for sub-seal 1 — full OS shell chrome + portal-mode tiles, OR minimum viable OS shell chrome only + tiles deferred to sub-seal 1b?
- **(f)** JWT tenant-binding — add `tenant_id` claim (breaking change to auth) OR derive tenant from identity email domain OR seed a demo `RMS AI` tenant on the four seeded demo accounts?
- **(g)** DAP `role_switcher` (Employee → Manager → Exco → CEO) — Brief §4 flags this as a view-level construct only, needs identity plane + per-route authz + server-side role claim before it ships as anything other than a demo control (`[PENDING RATIFICATION on principal-wave seal]` per OS Frontends Card §4).

---

# CURRENT-STATE SCREENSHOTS BANKED

- `phase0/eyeball_proxies/20260923T190000Z_owner_diag_A_root_landing.png` — `/` (v8 iframe · dummy tiles beyond WaveG4-substituted ones)
- `phase0/eyeball_proxies/20260923T190500Z_owner_diag_B_os_work_commission.png` — `/os/work/commission` (native React WorkCommission · Canon 5 §14 Shaping Wizard · WIRED)
- `phase0/eyeball_proxies/20260923T190800Z_owner_diag_C_dap_landing.png` — `/dap` (seeded-demo DAP surface the owner rejected)
- `phase0/eyeball_proxies/20260923T193500Z_owner_diag_D_os_work_documents.png` — `/os/work/documents` (representative HONEST-GAP native leaf · non-fabricating)

**Owner-design reference files (side-by-side for review):**
- **OS binding v2:** `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` (2,286,992 B · sha256 `9952692ce058…`) · open in browser directly to compare against `/` iframe
- **DAP binding LATEST:** `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` (221,620 B) · open in browser directly to compare against `/dap`

---

**Ledger check:** this incident receipt implements UI-FIDELITY-P0 diagnostic (widening from DAP-only to DAP+OS · one combined report per owner directive 2026-02-23T~19:30Z) and nothing else. Additive-only per SO §3.8. **NO code delta. NO rebuild executed.** Awaiting owner GO on the ratification checkpoints above. All 6 Standing Bans + 17 Standing Guards + SO §6.9 + Ruling (b) AKKI-RUNS-IT verbatim remain binding meanwhile. **HALT to owner for review.**
