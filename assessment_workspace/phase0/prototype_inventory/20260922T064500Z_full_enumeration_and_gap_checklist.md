# Prototype full 46-view enumeration + ε-apply gap checklist · 2026-09-22T06:45:00Z

**Turn 4 · sub-slice 4a: state-side prep only. NO frontend commits yet.** Extends the starter at `phase0/prototype_inventory/20260922T062000Z_prototype_inventory_starter.md`. Owner directive verbatim (2026-09-22T~06:35Z): *"the ε-apply wave ships EVERY prototype view, including the entitlements/org-admin screens — live-wired where a real backend exists, honest-gap pattern where it does not."*

## 1 · v2 OS prototype · complete NAV enumeration (from `RMS_AI_Prototype_v2.html` byte-verbatim)

### 1.1 · Top-level TABS constant (byte-verbatim)

```js
const TABS = [
  { key:'work',  label:'Work',           groups:['workstudio','thinklab','collab','monitor'] },
  { key:'build', label:'Build',          groups:['build','buildlib'] },
  { key:'apps',  label:'3rd Party Apps', groups:[] },
  { key:'admin', label:'Admin',          groups:['estate','approvals','watch'], right:true }
];
```

### 1.2 · NAV constant · ALL 10 groups · **37 leaf views** (byte-verbatim extracted)

| # | Group key | Group label | Leaves (verbatim key:label pairs) |
|---:|---|---|---|
| 1 | `workstudio` | WorkStudio | `chat`→Chat · `analyze`→Data Suite · `documents`→Documents · `tasks`→My Work · `team`→My Team · `performance`→Company Goals · `board`→Board **(7)** |
| 2 | `thinklab` | ThinkLab | `clarity`→Seek Clarity · `strategy`→Develop Strategy · `hypothesis`→Test Hypothesis · `perspective`→Get Perspective **(4)** |
| 3 | `collab` | Collab | `mentions`→Mentions · `emails`→Emails · `projects`→Projects/Tasks · `hrstuff`→HR Stuff **(4)** |
| 4 | `monitor` | Monitor (Work tab · sub-tabs via `monitorTabsView`) | `performance`→Performance (already in workstudio) · **`signals`→Signals** · **`ideas`→Ideas** **(2 net-new leaves + performance overlap)** |
| 5 | `estate` | Manage Estate | `estate`→Registry · `govern`→Shield · `greymirror`→Grey Mirror **(3)** |
| 6 | `approvals` | Approvals | `spendreq`→Spend Requests · `rulesupd`→Rules Updates · `modeladmission`→Model Approval **(3)** |
| 7 | `watch` | The Watch (Admin tab) | `wstate`→State · `wrecord`→Record · `wunder`→Under Watch · `wdecisions`→Decisions **(4)** |
| 8 | `build` | Build Your Resources | `train`→Train Models · `agentbuild`→Build Agents · `buildskill`→Build Skill · `extract`→Extract Data **(4)** |
| 9 | `buildlib` | Your Resources (divider · tabs) | `youragents`→Agents · `yourmodels`→Models **(2)** |
| 10 | `thirdparty` | 3rd Party Apps | `appsnew`→New · `appsfrequent`→Frequent · `appsconnected`→Connected · `appsrequests`→Requests **(4)** |

**Total distinct leaf views: 37** (33 in NAV + 2 in monitor overrides + 2 in monitor tabs excluding overlap with workstudio.performance).

### 1.3 · Personas (`ROLES` constant · byte-verbatim)

```js
const ROLES = [
  { key:'compliance', label:'Compliance Owner', person:'M. Chen',   dept:'Compliance', initials:'MC', groups:['estate','approvals'] },
  { key:'watch',      label:'Watch Officer',    person:'A. Njeri',  dept:'The Watch',  initials:'AN', groups:['watch'] },
  { key:'operator',   label:'Operator',         person:'J. Otieno', dept:'Operations', initials:'JO', groups:['estate'] }
];
```

- The runtime App.js must implement role-based nav filtering: a persona sees only their `groups` in Admin tab; the Watch officer sees only `watch`; the operator sees only `estate`; the compliance owner sees `estate + approvals`. Non-admin tabs (work, build, apps) are unconditional.

### 1.4 · TONE palette (byte-verbatim)

```js
const TONE = {
  plain:  { bg:'#fff',                       border:'var(--line)',    color:'var(--ink)'  },
  held:   { bg:'rgba(176,141,46,.07)',       border:'var(--brass)',   color:'var(--ink)'  },
  refused:{ bg:'rgba(184,57,91,.06)',        border:'var(--oxblood)', color:'var(--ink)'  },
  failed: { bg:'var(--surface2)',            border:'var(--line)',    color:'var(--ink3)' },
  drill:  { bg:'var(--surface)',             border:'var(--line)',    color:'var(--ink2)' }
};
```

- `:root` CSS variables (verified in `phase0/prototype_inventory/20260922T062000Z_prototype_inventory_starter.md`): paper `#f5f2ea` · ink `#1b1f27` · blue `#16274a` · brass `#b08d2e` · sage `#1d7a6e` · plus `--line`, `--surface`, `--surface2`, `--ink2`, `--ink3`, `--oxblood`.

### 1.5 · FOURQ pattern (byte-verbatim comment)

Every four-questions surface starts with a sentence + "see the working" (measures behind the sentence):

```js
/* Four-questions surfaces. Rule zero: every block leads with a sentence;
   measures live behind "see the working". */
```

### 1.6 · Canon label ↔ identity mapping (byte-verbatim from v7 brief section preserved in v2)

```
Manage Rules              → The Rulebook + change sign-off process (Doc 3 Part V, Doc 5 §23)
Data Shield               → Boundary handling: chain, receipts, disclosure (Doc 3 §13–§20)
Reasoning Shield          → Reasoning assurance: depth, evidence bars, traces (Doc 4 Part IV)
Access Shield             → Permission + Access surface (Doc 3 §22.1, Doc 5 §41)
Data Estate               → Estate Map / census & registry reading (Doc 5 control band)
Models / Compute / Connect → Model registry & ladder · economics/metering · integration wizard (Docs 4, 7)
State / Record / Under Watch / Decisions → The Watch Console's four panels (Doc 8 §13, Doc 5 Part VII-A)
People & Declarations     → Approval declarations (Doc 3 §6.1)
Rule Changes              → The change sign-off process pipeline (Doc 3 §24)
```

## 2 · DAP LATEST prototype · state machine enumeration (from `RMS_DAP_LATEST.html`)

### 2.1 · Ownership status strings (top-level filter chips)

- `Available` — open resource · anyone with entitlement can request.
- `Yours` — owned by you (assignable).
- `In use` — currently held by another party.
- `Not available` — gate refused (entitlement or admit).

### 2.2 · Request lifecycle states (extracted verbatim)

| Stage | Meaning | Prototype view |
|---|---|---|
| **`Open to you`** | Viewable · you can request | Browse list · request-detail card open |
| **`In Approval`** | Awaiting sign-off | Sign-off queue row · sign-off review card |
| **`Needs sign-off`** | Someone needs to approve | Row with badge (approver-side) |
| **`Ready`** | Approved · queued to execute | Request-detail with "Start" primary button |
| **`Executing` / `running`** | Extraction in progress | Progress card with live rows + stop button |
| **`stopped`** | Explicitly stopped mid-run | Refusal-adjacent card · "Stopped" copy verbatim per R-100 seal |
| **`Refused` / `refused`** | Gate refused (pre- or post-Admit) | Refusal card §2.2 canon copy verbatim |
| **`Blocked`** | Awaiting external condition | Blocked-state card · reason surfaced |
| **`transferring`** | Delivery in progress | Progress card with delivery percentage |
| **`Retrieved` / `done`** | Extraction complete · retrieved | Done-state card with delivery pointers |
| **`failed`** | Error state | Failure card with reason · retry option per R-78 bounded-3 |
| **`Expired`** | Approval or admit expired | Timeout card |
| **`closed`** | Terminal (post-done or post-refused) | Read-only history entry |
| **`pending`** | Awaiting classification | Interim state during Admit filing |

**Total distinct DAP states: 14.** Plus 4 ownership statuses = **18 discriminators**. Screens: browse list + request detail + running progress + transferring progress + done delivery + refused card + sign-off queue + sign-off review + blocked state + failed state + retry surface = **11 canonical DAP screens** (each with per-state variants).

## 3 · Owner's "20 pages" ambiguity — resolved reading

Owner earlier said the prototype is "20 pages". This mismatches the leaf count (37 OS + 11 DAP = 48 canonical views + state variants). **Best reading given the ratified pro-tem "newest owner drop wins":** the 20-count likely counts **top-level surfaces** (Work / Build / Admin tabs of OS + DAP entry views), not leaves. Ratified pro-tem to enumerate exhaustively (all 37 OS leaves + all 11 DAP canonical screens + state variants) — this satisfies either reading of "20 pages" and matches owner Q1 ruling that no prototype view is deferred out of the ε-apply wave.

## 4 · Runtime target · CURRENT `/app/frontend/src/App.js` structural inventory

| Metric | Value |
|---|---|
| Runtime App.js lines | 1112 |
| pod_shell App.js lines | 1084 (28-line drift · the R-91 mirror-drift baseline) |
| Runtime pages/ dirs | `pages/dap/`, `pages/os/` (both present) |
| pod_shell pages/ dirs | **absent** (pod_shell/frontend/src/pages/ does NOT exist per `diff -rq` at 06:30Z) |
| Sealed shell components in runtime | Chat, ConnectWizard, ModelEcosystem, CommissionWizard, EvidenceRegister, RefusalCard, CostLedger, Training, ThinkLab, DataShield, Registry, Governance, SkillFiles, GreyMirror, Watch, ClassBadge, ConnectDrawerChat, AuditTrail (18 components) — many pre-existing, byte-identity between runtime and pod_shell needs re-verification |
| Runtime-only helpers | `strings/entitlementStrings.js`, `strings/lifecycleStrings.js`, `lib/apiClient.js`, `plugins/health-check/*` |

**Mirror-drift closure operation (per R-91 §22243 verbatim + owner note verbatim "at apply, the mirror lands the CURRENT tree"):** runtime is source-of-truth; pod_shell is target. But this precedes the frontend rebuild — after ε-apply, runtime App.js will be REBUILT to match v2 OS + LATEST DAP prototypes (which is a NEW state that pod_shell must then also match). Direction operation: **rebuild runtime App.js → then bulk-copy /app/frontend/{App.js, pages/, components/} to pod_shell/frontend/{...}** as the closing sync.

## 5 · ε-APPLY GAP CHECKLIST · 46 canonical views (owner-visible feature slots)

For each: `[STATUS]` on backend availability, decision on wiring, and RED-first invariant test to author.

### 5.1 · OS surface (work tab · 15 leaves)

| # | Leaf | Group | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 1 | `chat` (Chat) | workstudio | **PARTIAL** — `Chat.jsx` exists (BUILT · sealed) | Live-wire to existing `Chat.jsx` per prototype layout · **prototype wins** for layout only |
| 2 | `analyze` (Data Suite) | workstudio | **MISSING** — no data-suite backend | **HONEST-GAP** string: "Data Suite arrives with the census productization objective." |
| 3 | `documents` (Documents) | workstudio | **PARTIAL** — Documents+Deck tab in prototype; Doc 18 Skills A18.1-3,5,8 NOT BUILT; deck engine DR-R1..R14 PARTIAL | **HONEST-GAP** for skills · Documents-only read live from doc read endpoints if any |
| 4 | `tasks` (My Work) | workstudio | **MISSING** — no task backend | **HONEST-GAP** string per prototype |
| 5 | `team` (My Team) | workstudio | **MISSING** | **HONEST-GAP** |
| 6 | `performance` (Company Goals) | workstudio (+ monitor overlap) | **MISSING** | **HONEST-GAP** |
| 7 | `board` (Board) | workstudio | **MISSING** | **HONEST-GAP** |
| 8 | `clarity` (Seek Clarity) | thinklab | **PARTIAL** — `ThinkLab.jsx` exists (BUILT · sealed) | Live-wire to `ThinkLab.jsx` |
| 9 | `strategy` (Develop Strategy) | thinklab | **PARTIAL** — same as clarity | Live-wire to `ThinkLab.jsx` variant |
| 10 | `hypothesis` (Test Hypothesis) | thinklab | **PARTIAL** — same | Live-wire |
| 11 | `perspective` (Get Perspective) | thinklab | **PARTIAL** — same | Live-wire |
| 12 | `mentions` (Mentions) | collab | **MISSING** | **HONEST-GAP** |
| 13 | `emails` (Emails) | collab | **MISSING** | **HONEST-GAP** |
| 14 | `projects` (Projects/Tasks) | collab | **MISSING** | **HONEST-GAP** |
| 15 | `hrstuff` (HR Stuff) | collab | **MISSING** | **HONEST-GAP** |

### 5.2 · Monitor sub-view (Work tab · 2 net-new leaves via monitorTabsView)

| # | Leaf | Group | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 16 | `signals` (Signals) | monitor | **MISSING** | **HONEST-GAP** |
| 17 | `ideas` (Ideas) | monitor | **MISSING** | **HONEST-GAP** |

### 5.3 · Build tab (6 leaves)

| # | Leaf | Group | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 18 | `train` (Train Models) | build | **PARTIAL** — `Training.jsx` sealed component exists; A17.12-14 no runner; A17.16 model form BUILT | **HONEST-GAP** for runner state · live-wire for form/admit |
| 19 | `agentbuild` (Build Agents) | build | **MISSING** — no agent-build backend | **HONEST-GAP** |
| 20 | `buildskill` (Build Skill) | build | **PARTIAL** — `SkillFiles.jsx` sealed; A18 mostly NOT BUILT | **HONEST-GAP** (per DQ-14 CP-SKILLS-LAYER draft-open) |
| 21 | `extract` (Extract Data) | build | **PARTIAL** — extraction backend live under DAP · censuses live | Live-wire to CENSUS-SURFACE-A endpoints (`/api/portal/census/*`) + DAP endpoints |
| 22 | `youragents` (Agents) | buildlib | **MISSING** — no agent registry read | **HONEST-GAP** |
| 23 | `yourmodels` (Models) | buildlib | **PARTIAL** — model registry contracts BUILT (A20.15-16); A20.1-14 PARTIAL | Live-wire model list to whatever registry endpoint exists · **HONEST-GAP** for missing metadata |

### 5.4 · 3rd Party Apps tab (4 leaves)

| # | Leaf | Group | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 24 | `appsnew` (New) | thirdparty | **MISSING** — no 3rd-party app store | **HONEST-GAP** |
| 25 | `appsfrequent` (Frequent) | thirdparty | **MISSING** | **HONEST-GAP** |
| 26 | `appsconnected` (Connected) | thirdparty | **MISSING** | **HONEST-GAP** |
| 27 | `appsrequests` (Requests) | thirdparty | **MISSING** | **HONEST-GAP** |

### 5.5 · Admin tab (10 leaves)

| # | Leaf | Group | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 28 | `estate` (Registry) | estate | **BUILT** — CENSUS-SURFACE-A Registry landing + census journey endpoints live | Live-wire to `/api/portal/census/{records,assets,surfaces,access,latest,duplication}` per `phase0/surface_connection/portal_registry_landing_ui_spec.md` + `portal_census_journey_ui_spec.md` |
| 29 | `govern` (Shield) | estate | **PARTIAL** — `Governance.jsx` sealed; C5.1-5.7 governance C-family PARTIAL | Live-wire to `Governance.jsx` for present surfaces · **HONEST-GAP** for governance rule-change ceremony UI (BR-12 PARTIAL) |
| 30 | `greymirror` (Grey Mirror) | estate | **PARTIAL** — `GreyMirror.jsx` sealed exists | Live-wire to `GreyMirror.jsx` |
| 31 | `spendreq` (Spend Requests) | approvals | **PARTIAL** — R-100 portal write-surface has spend request endpoints (submit / stop) live · `/api/portal/*` | Live-wire to R-100 portal endpoints per R-100 seal (JWT-gated) |
| 32 | `rulesupd` (Rules Updates) | approvals | **PARTIAL** — R-98 canon-rules HTTP surface at `/api/canon/rules/*` live (5 endpoints incl. RBM-8 anchor); customer rule-change ceremony BR-12 PARTIAL | Live-wire read side to R-99 canon-rules endpoints · **HONEST-GAP** for change-authoring ceremony UI |
| 33 | `modeladmission` (Model Approval) | approvals | **PARTIAL** — A17.13 "shows a capability with nothing running behind it" | **HONEST-GAP** live (echoes spec verbatim) |
| 34 | `wstate` (Watch · State) | watch | **PARTIAL** — Watch service scaffolded; state read endpoint not visible | **HONEST-GAP** |
| 35 | `wrecord` (Watch · Record) | watch | **PARTIAL** | **HONEST-GAP** |
| 36 | `wunder` (Watch · Under Watch) | watch | **PARTIAL** | **HONEST-GAP** |
| 37 | `wdecisions` (Watch · Decisions) | watch | **PARTIAL** | **HONEST-GAP** |

### 5.6 · DAP LATEST surface (canonical screens · 9 view classes + 2 stage-only helpers)

| # | View class | DAP states rendered | Backend live? | Wiring decision |
|---:|---|---|---|---|
| 38 | Browse list (all requests) | Open to you · In Approval · Ready · Available · Yours · In use · Not available | **PARTIAL** — R-100 GET list endpoint live (JWT-gated) | Live-wire to `/api/portal/*` per R-100 |
| 39 | Request detail card | Open to you · Ready · Executing · Blocked · Refused · Retrieved · Failed · Stopped · Expired · Closed | **PARTIAL** — R-100 detail-shape stub live | Live-wire to R-100 detail endpoint |
| 40 | Running progress panel | Executing state · live rows | **PARTIAL** — R-100 request status live | Live-wire to R-100 status endpoint · progress rows honest-gap-per-source until CENSUS-3-F.2.1 live-bind lands |
| 41 | Stop confirm modal | Executing → Stopped transition | **BUILT** — R-100 CONDITION 2 stop endpoint live · confirm.confirm_copy byte-verbatim per R-100 seal | Live-wire to R-100 stop endpoint with byte-verbatim copy: *"Stop this request? What's run so far will still be billed; nothing further will execute."* |
| 42 | Refused card (§2.2 canon-copy) | Refused state | **BUILT** — `RefusalCard.jsx` sealed component | Live-wire to `RefusalCard.jsx` · §2.2 canon copy verbatim (only exception to "prototype wins" per FE brief §0.2) |
| 43 | Sign-off queue (approver-side) | In Approval · Needs sign-off | **PARTIAL** — R-100 portal has POST submit but not sign-off queue | **HONEST-GAP** for queue read · live-wire per available endpoints |
| 44 | Sign-off review card (approver) | In Approval detail | **PARTIAL** — same as (43) | **HONEST-GAP** |
| 45 | Retry surface (bounded-3 per R-78) | Failed → retry attempt | **BUILT** — R-100 CONDITION 4 retry endpoint live · `max_attempts=3` · `retry_service_reference=services.dap_lifecycle.retry_service.attempt_retry` | Live-wire to R-100 retry endpoint |
| 46 | Transferring / delivery panel | Transferring state | **PARTIAL** — no explicit delivery endpoint | **HONEST-GAP** |

**Total gap checklist rows: 46 canonical views.**

**Live-wired count: 8 slots** (1 chat + 4 thinklab + 1 registry + 1 refusal card + 1 stop modal + 1 retry surface + 1 mtafiti extract=CENSUS + 1 spend requests + 1 rules updates read + 1 grey mirror + 1 governance read = actually 13 slots have partial or full live wiring).

**HONEST-GAP count: 28 slots** (2 monitor + 8 workstudio HG + 4 collab + 4 thirdparty + 4 watch + more).

**Partial live + honest-gap hybrids: 5 slots** (train, buildskill, yourmodels, appsrequests when linkage available, deck when relevant).

## 6 · Palette + typography verbatim (from `:root` extraction)

```css
:root {
  --paper:    #f5f2ea;
  --ink:      #1b1f27;
  --ink2:     ...  (verify at rebuild)
  --ink3:     ...
  --blue:     #16274a;
  --brass:    #b08d2e;
  --sage:     #1d7a6e;
  --oxblood:  ...
  --line:     ...
  --surface:  ...
  --surface2: ...
}
```

Complete `:root` extraction pending Chrome-runtime screenshot pass — the abbreviated colour block found in v2 needs full `:root` walked at rebuild time.

## 7 · ε-apply implementation sequencing

Given DQ-12 CP-DOT-ENV-HYGIENE riding same wave (owner ruling R-101 condition iv), the sequence within Turn 4 is:

1. **Sub-slice 4a** *(this-commit · state-only)*: **Full 46-view enumeration + gap checklist** — this file.
2. **Sub-slice 4b** *(next boundary · Commit-A on programme/track-a)*: **DQ-12 CP-DOT-ENV-HYGIENE** — RED-first 3 invariants + `git rm --cached backend/.env` + `.env.local` untracked-from-birth + supervisor sourcing both.
3. **Sub-slice 4c** *(next boundary · Commit-A on programme/track-a)*: **Frontend rebuild slice 1 · shell + palette + 4 TABS + persona filter**. Rewrite `/app/frontend/src/App.js` opening block byte-verbatim per v2 OS TABS + NAV + ROLES + TONE + FOURQ pattern. RED-first mirror-invariant test guarantees pod_shell must sync afterward.
4. **Sub-slice 4d** *(next boundary · Commit-A)*: **Frontend rebuild slice 2 · OS surface views · Work tab** (chat live + analyze/documents/tasks/team/performance/board honest-gap) + Monitor sub-view (signals/ideas honest-gap).
5. **Sub-slice 4e** *(next boundary · Commit-A)*: **Frontend rebuild slice 3 · Work tab (thinklab live · collab honest-gap) + Admin tab (estate/govern/greymirror live · approvals live · watch honest-gap)**.
6. **Sub-slice 4f** *(next boundary · Commit-A)*: **Frontend rebuild slice 4 · Build tab + 3rd Party Apps tab** (mostly honest-gap; train/extract/yourmodels live-wired).
7. **Sub-slice 4g** *(next boundary · Commit-A)*: **Frontend rebuild slice 5 · DAP LATEST surface** — 9 view classes (browse list + detail + running progress + stop modal + refused card + sign-off queue + sign-off review + retry + transferring). Live-wire to R-100 portal write-surface + `RefusalCard.jsx`.
8. **Sub-slice 4h** *(next boundary · Commit-A)*: **Mirror sync + 5-baseline retirement + 5-annotation retirement + milestone_status SEALED**. Sync `/app/frontend/{App.js, pages/, components/}` → `pod_shell/frontend/{...}` byte-identically. Update `baseline_failures.json` atomically. Flip CP_APP_JS_UNIFY card SCHEDULED → SEALED.
9. **Sub-slice 4i** *(next boundary · Commit-B + Commit-C)*: **BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical sweep + §3.3 3-Commit Seal + 3-bundle Continuity regen + STATE/PINS.md sha-pin block**.
10. **Sub-slice 4j** *(post-seal boundary)*: **DQ-14/15/16 objective cards drafted** (CP-SKILLS-LAYER + CP-DECK-ENGINE + CP-STREAMING-EXTRACTION-FORK) + **CP-TENANT-SEPARATION opens** per owner Part-2 order.

Each sub-slice is a proper §3.3 3-Commit Seal boundary; the desk reports at each seal per SO §6.7.

## 8 · Chrome runtime screenshot plan (deferred to sub-slice 4c open · pre-first-commit)

At sub-slice 4c open (before `App.js` rewrite lands):
1. Serve `RMS_AI_Prototype_v2.html` at `localhost:3000/prototype-v2` via a temporary alias.
2. Serve `RMS_DAP_LATEST.html` at `localhost:3000/prototype-dap-latest`.
3. Boot Chrome via `screenshot_tool` at each of the 37 OS leaf views + 9 DAP view classes = 46 canonical screenshots.
4. Bank to `phase0/prototype_screenshots/20260922_v2_os/` and `phase0/prototype_screenshots/20260922_dap_latest/`.
5. Diff-per-view against sub-slice 4c-4g rebuild output for pixel-adjacent verification (structural, not pixel-exact — the prototype is Vue.js, the rebuild is React).

## 9 · Bounds

State-side prep only per this-commit. Zero App.js touch. Zero sealed FE component edit. Zero code branch commit this-boundary. R-101 supersede has removed the horizon; condition-gating replaces clock-gating; conditions (i)-(vi) apply per `DECISIONS.md:R-101 append`.

## 10 · Canon anchors verbatim

- Owner directive verbatim 2026-09-22T~06:10Z: *"UI/UX architecture and experience flow needs to be exact as the HTML I shared."*
- Owner Q1 ruling 2026-09-22T~06:35Z: *"ε-apply wave ships EVERY prototype view ... live-wired where a real backend exists, honest-gap pattern where it does not. No prototype view is deferred out of the UI wave; only the BACKEND build-out behind gapped views is a later objective."*
- Owner Front_End_Integration_Brief.md §0 verbatim (2026-09-20T~08:24Z): *"The prototype is the design of record ... prototype wins."*
- Owner FE brief §2.2 refusal-copy carve-out (only exception to prototype-wins).
- R-101 supersede banking at `STATE/DECISIONS.md:R-101 append` state master commit `fbcbf1f7`.
- R-91 CEREMONY-OPEN §22243 verbatim 10-operation apply schedule (WHAT preserved).
- SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + §6.8 owner-directive scope.

<!-- Turn 4 sub-slice 4a · Prototype full 46-view enumeration + ε-apply gap checklist · 2026-09-22T06:45:00Z END -->
