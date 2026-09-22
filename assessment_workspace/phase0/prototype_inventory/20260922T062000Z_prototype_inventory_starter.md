# RMS AI Prototype Ver 2.0 Sep 2026 · page/state inventory · 2026-09-22T06:20:00Z

## Trigger
Owner directive at CENSUS-3-F.2 seal boundary (2026-09-22T~06:10Z): *"the prototype is the design authority; our banked specs are subordinate to it where they differ ... Locate the bound HTML prototype on disk (the cp10 realchrome harness binds rules to rendered DOM, so the prototype and a chrome runtime exist — find both; also check /app/frontend/public/, notes/, phase0/ for the prototype bundle 'RMS AI Prototype Ver 2.0 Sep 2026', 20 pages)."*

## Provenance chain (from owner Front_End_Integration_Brief.md at custody/owner_drops/20260920T0824Z/)

> **The prototype is the design of record. The repository's React app is derived from it.**
> ... Every wired component in `frontend/src/components/` carries a header recording that it was extracted from our prototype: `DataShield.jsx` — "v7 oracle fabric — extracted verbatim from `fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html`"; palette tokens "extracted verbatim from prototype.html :root vars."
>
> - **Trust the repo components for endpoint behaviour, not for UI.**
> - **Where the repo's React app and the prototype differ in layout, navigation, naming, or interaction, the prototype wins.**
> - Exception: §2.2 refusal copy (binding canon text · not repo preference).

## The two authoritative files (banked design of record)

| Surface | Path | Bytes | Owner drop | Role |
|---|---|---|---|---|
| **OS** | `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` | 2,286,992 | 2026-09-20T08:24Z | *"RMS AI Prototype v2 ACTIVE"* — design of record for OS surface |
| **DAP** | `custody/owner_drops/20260920T1140Z/RMS_DAP_LATEST.html` | 221,620 | 2026-09-20T11:40Z (updated after 0824Z's `RMS_Data_Access_Portal.html`) | *"RMS Data Access Portal LATEST"* — design of record for DAP surface |

**cp10 realchrome harness binds** to `/app/frontend/public/v8_prototype.html` (1.26MB) — that is the RUNTIME iframe (pre-R-91 mirror per owner). Same bytes as `assessment_workspace/fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html`. The v8 runtime is **structurally different** from v2 design of record; the ε-apply seal must land the v2 design over the current v8 iframe path.

**Version note (owner-flagged complication)**: `notes/spec_id_index.md` banks `prototype_v3` (`ee6ebe77e1c5…`) as design_id; `MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md` states *"Binding design: prototype_v3."* But the owner's 2026-09-20 drops are named **v2** (`RMS_AI_Prototype_v2.html`). Working assumption per owner's most recent drop-of-record: **v2 (2026-09-20)** supersedes v3 (2026-09-09) — the owner's newest drop is the binding design. Confirmation ask filed with the desk.

## OS surface · nav enumeration (Vue.js `s.navTab` + `NAV[].items` mechanism)

**Top-level tabs (4)** — from `TABS = [...]` constant:

| key | label | groups | position |
|---|---|---|---|
| `work` | Work | workstudio, thinklab, collab, monitor | left |
| `build` | Build | build, buildlib | left |
| `apps` | 3rd Party Apps | — (uses thirdparty group directly) | left |
| `admin` | Admin | estate, approvals, watch | right-aligned |

**Groups → leaf items** — from `NAV = [...]` constant · **31 leaf views**:

- **workstudio (WorkStudio)** — 7 views: `chat` (Chat), `analyze` (Data Suite), `documents` (Documents), `tasks` (My Work), `team` (My Team), `performance` (Company Goals), `board` (Board).
- **thinklab (ThinkLab)** — 4 views: `clarity` (Seek Clarity), `strategy` (Develop Strategy), `hypothesis` (Test Hypothesis), `perspective` (Get Perspective).
- **collab (Collab)** — 4 views: `mentions` (Mentions), `emails` (Emails), `projects` (Projects/Tasks), `hrstuff` (HR Stuff).
- **estate (Manage Estate)** — 3 views: `estate` (Registry), `govern` (Shield), `greymirror` (Grey Mirror).
- **approvals (Approvals)** — 3 views: `spendreq` (Spend Requests), `rulesupd` (Rules Updates), `modeladmission` (Model Approval).
- **build (Build Your Resources)** — 4 views: `train` (Train Models), `agentbuild` (Build Agents), `buildskill` (Build Skill), `extract` (Extract Data).
- **buildlib (Your Resources · divider · tabs)** — 2 views: `youragents` (Agents), `yourmodels` (Models).
- **thirdparty (3rd Party Apps)** — 4 views: `appsnew` (New), `appsfrequent` (Frequent), `appsconnected` (Connected), `appsrequests` (Requests).

**Also-referenced groups not yet fully enumerated** (present in TABS but leaf items not surfaced in current extraction · to expand next turn):
- **monitor** (under Work tab)
- **watch** (under Admin tab)

**Owner's "20 pages" claim** — likely refers to primary/canonical views (perhaps a top-view-per-group + selected leaves), not all 31 leaves. **Confirmation ask filed**: does "20 pages" mean 20 canonical views for ε-apply landing, or 20 including states/modals? For ε-apply scoping.

## DAP surface · state/stage enumeration

**Architecture**: DAP is NOT nav-driven; it is a **state machine** for extraction-request lifecycle. No `TABS`/`NAV` constant. Discriminators are stage strings on request records + gate visibility.

**Stage strings found in `RMS_DAP_LATEST.html`** (partial · to expand next turn):

Request lifecycle:
- `Open to you` (viewable · you can request)
- `Needs sign-off` (someone needs to approve)
- `Not available` (gate refused)
- `running` (extraction in progress)
- `refused` (gate refused post-Admit)
- `done` (extraction complete)
- `transferring` (delivery in progress)
- `failed` (error state)

Ownership status:
- `In use` (currently held)
- `Yours` (owned by you)
- `Available` (open resource)

**Estimated distinct DAP screens/states**: 10-15 (browse list · request detail · running progress · transferring progress · done delivery · refused card · sign-off queue · sign-off review). Full enumeration next turn — needs deeper HTML walk (streaming/transition data owner mentioned).

## ε-apply work order (starter checklist — expand + verify against Chrome screenshots at next-turn)

**When**: R-91 horizon `2026-09-23T03:23:15Z` (~21.4h out at inventory time · NO EXPEDITE).

**Gates**:
1. `App.js` byte-identical mirror to `pod_shell/frontend/src/App.js` — R-91 landing.
2. Implement each of the 31 OS leaf views + the ~10-15 DAP stage-states as React components rendering byte-verbatim per prototype.
3. Every stage-state transition (idle → running → transferring → done, or → refused) must render the exact prototype cards/badges/copy.
4. Refusal card copy = §2.2 canon text VERBATIM (only exception to "prototype wins" per Front_End_Integration_Brief §0.2).
5. Palette tokens (`#f5f2ea` paper · `#1b1f27` ink · `#16274a` blue · `#b08d2e` brass · `#1d7a6e` sage) match prototype `:root` — verify at ε-apply.

**Gap-driven line items (starter — 8 anchors, expand next turn):**
- L1: Are all 31 OS leaf views implemented in current `/app/frontend/src/App.js`? — expected: NO, current runtime is v8 iframe pre-R-91 mirror.
- L2: Does DAP surface exist in current App.js at all? — expected: NO (banked as `phase0/surface_connection/portal_registry_landing_ui_spec.md` + `portal_census_journey_ui_spec.md` but not shipped).
- L3: Streaming/transition state components (running / transferring / done / refused) — none currently in App.js.
- L4: "N response required" badge — inventory of where it appears in the prototype pending.
- L5: Census RUNNING card — inventory pending.
- L6: Honest-gap strings — need to walk prototype for copy-verbatim inventory ("unverified volume is EXCLUDED from every verified figure until the next census reaches it" per CENSUS-SURFACE-A owner drop verbatim + others).
- L7: 4-tab nav structure (Work / Build / 3rd Party Apps / Admin) — need to reproduce.
- L8: Admin tab right-align, Watch sub-group in Admin — inventory pending.

## Next-turn expansion plan (state-side prep · no frontend commits)

1. Complete the leaf-item enumeration for `monitor` (Work) + `watch` (Admin) groups.
2. Fully enumerate DAP state machine + component names + screen count.
3. Boot Chrome runtime + serve each prototype at localhost:3000/prototype-v2 and prototype-dap-latest.
4. Take screenshots per canonical view (OS ~31 + DAP ~15 = ~46 screens · full page + notable modal/state variants).
5. Bank screenshots to `phase0/prototype_screenshots/20260922_v2_os/` and `20260922_v2_dap_latest/`.
6. Expand ε-apply work order into full 46-line gap checklist per prototype view.
7. Ask owner to confirm "20 pages" = which 20.

## Bounds

State-side prep only per owner directive: **"no frontend commits before horizon"**. Zero App.js touch this-turn. Zero sealed FE component edit. This receipt lives at `phase0/` state-repo; not code-repo. R-91 horizon `2026-09-23T03:23:15Z` UNCHANGED NO EXPEDITE.

## Canon anchors

- Owner directive verbatim 2026-09-22T~06:10Z (this-session at F.2 seal boundary): *"UI/UX architecture and experience flow needs to be exact as the HTML I shared."*
- Owner Front_End_Integration_Brief.md §0 verbatim (2026-09-20T~08:24Z): *"The prototype is the design of record ... prototype wins."*
- Owner Front_End_Integration_Brief.md §2.2 (refusal copy carve-out).
- CENSUS-SURFACE-A Commit-B autopilot line 2026-09-22T~03:45Z (R-91 ε-apply seal boundary).
- SO §3.3 R-6 boundary regen + §3.8 additive-only + §6.4 NOTHING-BEYOND.

<!-- 20260922T062000Z_prototype_inventory_starter.md END -->
