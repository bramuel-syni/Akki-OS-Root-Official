# Wave G Close Report — V8 Adoption

**Session close: 2026-08-28T~04:52Z · autonomous under all standing disciplines · stop-and-report for external verification.**

---

## §1. Scope executed

Wave G was re-scoped this session to **V8 Adoption** by owner ruling 2026-08-28T~04:15Z (in-chat) — superseding the earlier v4-shell-to-pod scope (v4 rescinded) and the v7-v2 farmaIQ upload (declassified as design source).

Steps executed:
- **Step 0** — v8 identity verification (file-bytes only, no README/filename/prior claim).
- **Step 0.5** — v8 inventory built from verified bytes with mandatory citations.
- **Step 2** — v8 shell code landed at `pod_shell/frontend/src/design/` and byte-identically mirrored to `/app/frontend/src/design/`.
- **Step 3** — every declared pod route wired into the shell as click-target (no URL-only surface remains).
- **Step 4** — real data unchanged (pod routes still serve their existing components; the shell is chrome).
- **Step 5** — double-green permanent close at ratcheted floor.

---

## §2. Step 0 — v8 identity verdict (PASS)

**Files verified (raw bytes only):**

| file | sha256 | bytes |
|---|---|---:|
| `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` | `e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2` | 1,264,425 |
| `fixtures/Akki_Platform_v8_Design_Spec.docx` | `d7cfd3aed244da1b53b7b86ed9572852b8e6e928f2294d6f94083ff775491304` | 108,191 |

**Bundler manifest inside the HTML** — 4 base64+gzip payloads + 1 inline JSON-encoded template:

| uid | mime | bytes | payload sha256 | vs v7-v1 |
|---|---|---:|---|---|
| `8d5cc57e…` | application/javascript | 6,289 | `ba61852925c4327a…` | byte-identical (dc-runtime county-map) |
| `0f495aa5…` | text/javascript | 69,150 | `8fe7df74405f3c55…` | byte-identical (dc-runtime main bundle) |
| `a27c8ca4…` | text/javascript | 131,835 | `35f4f974f4b2bcd4…` | identical (react-dom@18.3.1 UMD) |
| `373c1b27…` | text/javascript | 10,751 | `d949f1c3687aedad…` | identical (react@18.3.1 UMD) |
| inline template | text/html (decoded) | 1,111,498 | `9177c2b910b9caf5…` | **NEW · differs from v7-v1/v7-v2 `59200739b34dd23d` · ~8.25× larger · genuine new content** |

**Identity grammar scan** on the decoded template:
- Akki OS grammar: 21 distinct terms × 836 hits — includes every canon-characteristic term (Registry · Shield · Grey Mirror · Manage Estate · Approvals · Rules Updates · Model Admission · Board 360 · Exco 360 · WorkStudio · ThinkLab · Compliance Owner · Watch Officer · Trust Center · The Watch · custody · Checker).
- FarmaIQ grammar: 8 terms × 97 hits — appears as a **hosted "deployed agent"** application inside the OS shell (via `openDeployedAgent(a){ if(a.name==='Farma IQ'){…} }`), NOT as the shell wordmark. The v8 default `agentsList` seeds `Vendor Risk Monitor` (Deployed) + `Payroll Variance Checker` (Ready to deploy); FarmaIQ has been REMOVED from the default seed.

**Structural evidence** (verbatim citations):
- Wordmark literal at top-of-shell (52px header on `--blue2:#0f1b33`): `RMS AI` [v8-HTML:pos≈1655].
- 10-group NAV literal at pos≈511700: `workstudio · thinklab · collab · monitor · estate · approvals · build · buildlib · thirdparty · watch`.
- TABS literal at pos≈514470: `work · build · apps · admin(right:true)`.
- ROLES literal at pos≈514800: `Compliance Owner (M.Chen·MC) · Watch Officer (A.Njeri·AN) · Operator (J.Otieno·JO)`.
- v8 self-cites canon docs inline (verbatim comment at pos=513138): Manage Rules → Doc 3 Part V · Doc 5 §23; Data Shield → Doc 3 §13–§20; Reasoning Shield → Doc 4 Part IV; Access Shield → Doc 3 §22.1 · Doc 5 §41; State/Record/Under Watch/Decisions → Doc 8 §13 · Doc 5 Part VII-A; People & Declarations → Doc 3 §6.1; Ceremonies → Doc 3 §24.

**Docx spec confirms** [§1 line 13]: *"This build is branded RMS AI. The wordmark in the top bar is the only literal brand token in the file; the identical underlying product has previously shipped under other brand names (BDO AI, DigiCow AI, TrinityAI) by swapping that one string."*

**Verdict: PASS.** v8 identity = Akki OS (RMS AI branded instance). Receipt banked at `phase0/drill_receipts/20260828T041500Z_wave_g_step0_v8_identity_verification.log`.

---

## §3. Step 0.5 — v8 inventory built

`notes/prototype_inventory_v8.md` (656 lines · 62 `[v8-HTML:pos=…]` and `[v8-Docx:§X line N]` citations) — inventory sourced exclusively from the two verified files (v8 HTML template DOM + v8 docx). Structure:

- §1 Product overview (verbatim voice-principles + design-law)
- §2 Design system (color tokens · status-pill colors · typography · shape/spacing · recurring components)
- §3 Global application shell (top bar · portal mode · app mode · nav rendering rules)
- §4 Navigation taxonomy (NAV × TABS × ROLES verbatim literals + `SUB_TO_GROUP` mapping + canon citations)
- §5 Governance Surface template (structure + field shape + worked example)
- §6–§15 Per-app specifications (WorkStudio · ThinkLab · Collab · Performance Management · Build · 3rd Party · Manage Estate · Approvals · The Watch · Instance)
- §16 Cross-cutting overlays (FourQ · Brief · Shield Intelligence · Walk-this · Exposure Site Map · Toasts · Streaming)
- §17 Content-data constant reference (appendix)
- §18 Reachability inventory — 15 pod surfaces mapped into v8 lattice
- §19 Conflicts and agreements with the v7 four-fixture set (v8 wins; v4 rescinded)
- §20 Provenance and repro

**Extracted artifacts** at `notes/wave_g_step0_v8/`:
- `_hashes.json` — structured hash summary
- `v8_template.html` — raw JSON-encoded template
- `v8_template_decoded.html` — decoded 1,111,498 B application HTML (canonical citation index)
- `v8_design_spec.txt` — docx paragraph+table extract (39,635 B · 312 lines · canonical citation index)
- 4 bundler payloads decoded and persisted to disk

---

## §4. Step 2/3 — v8 shell code landed

**New files** (byte-identical mirror between pod_shell and /app):

| file | sha256 | bytes |
|---|---|---:|
| `pod_shell/frontend/src/design/akkiv8_design_system.js` | `ff4510b90958f1159b4cbfff8b8e6197fd923b340c7b3c2903784a71bb4f6c59` | ~6,600 |
| `/app/frontend/src/design/akkiv8_design_system.js` | `ff4510b90958f1159b4cbfff8b8e6197fd923b340c7b3c2903784a71bb4f6c59` | ~6,600 |
| `pod_shell/frontend/src/design/AkkiV8Shell.jsx` | `28d705ae45ddc289e78f482b3b20552c29ac8fdfbda16560c38c4911ce2d3768` | ~11,000 |
| `/app/frontend/src/design/AkkiV8Shell.jsx` | `28d705ae45ddc289e78f482b3b20552c29ac8fdfbda16560c38c4911ce2d3768` | ~11,000 |

**Modified files** (byte-identical mirror between pod_shell and /app):

| file | sha256 |
|---|---|
| `pod_shell/frontend/src/App.js` | `c41404d924d5ee779112ed7a4a117cd3bb485fbbbce43de4d341402cb2e7b31a` |
| `/app/frontend/src/App.js` | `c41404d924d5ee779112ed7a4a117cd3bb485fbbbce43de4d341402cb2e7b31a` |

`design_system.js` exports:
- `TOKENS` — all v8 color+font tokens verbatim [v8-Docx:§2.1/§2.2]
- `NAV` — the 10-group array verbatim [v8-HTML const NAV literal at pos≈511700 + `NAV.push({key:'watch',…})` at pos≈513850]
- `TABS` — the 4-tab array verbatim [v8-HTML const TABS literal at pos≈514470]
- `ROLES` — the 3-role array verbatim [v8-HTML const ROLES literal at pos≈514800]
- `V8_TO_POD_ROUTE` — 33 NAV item keys → pod routes (null where not yet mounted; rendered as greyed "not yet mounted" tiles per honest-empty rule)
- `POD_ONLY_TILES` — 5 pod-only surfaces (audit-trail · skill-files · evidence-register · commission · cost-ledger) so every declared pod route is click-reachable from `/`

`AkkiV8Shell.jsx` exports `AkkiV8ShellLayout` — the react-router layout wrapper. Chrome:
- 52px `--blue2:#0f1b33` top bar with shield SVG + `RMS AI` wordmark (font `--head:Iowan Old Style`) + role/dept text + circular avatar (`#28345c` bg, `MC` initials) per [v8-Docx:§3.1].
- At `/` renders portal mode: 45% left pane (tab pills → role-scoped nav groups → pod-only tiles) + 55% right pane (landing card citing v8 sha256).
- At any other route renders app mode: slim white header with mono breadcrumb + "← Exit to portal" link + `<Outlet/>` serving the pod component.

`App.js` restructures routing:
- `/` → portal (was Registry)
- `/registry` → Registry (was `/`) — this ALSO closes the manifest divergence: `/registry` is now declared in the pod-shell App.js matching `MUST_BE_LIVE_SPA_ROUTES`.
- All 14 other in-app routes now wrap inside `<Route element={<AkkiV8ShellLayout/>}>` — they render inside app mode.

**Test file**: `backend/tests/invariants/test_wave_g_v8_shell_port.py` (26 tests):
1. Asset presence — `AkkiV8Shell.jsx` and `akkiv8_design_system.js` exist in pod_shell tree (2 tests).
2. Token verbatim — 17 parametrized tests × required tokens (color hexes + font stacks from v8-Docx §2.1/§2.2).
3. NAV/TABS/ROLES literals — 4 key-set coverage tests (10 group keys · 33 item keys · 4 tab keys · 3 role keys).
4. App.js wires shell — imports `AkkiV8ShellLayout` from `./design/AkkiV8Shell`.
5. Reachability — every route declared in pod_shell/frontend/src/App.js must appear as a string literal in shell/design_system source (either mapped via `V8_TO_POD_ROUTE` or listed in `POD_ONLY_TILES`).
6. Runtime mirror — `AkkiV8Shell.jsx` + `akkiv8_design_system.js` byte-identical between pod_shell and /app/frontend.

**Right-reason RED banked before implementation**: `phase0/drill_receipts/20260828T044500Z_wave_g_step2_v8_shell_right_reason_fail.log` — 3 fails with correct reasons (files not present), 23 dependent tests skipped.

---

## §5. Step 4 — data fidelity

Real data unchanged: the shell is chrome that wraps existing pod components. Every pod route continues to serve the same component with the same live data (DigiCow, GPU, audit-trail Overview, watch marks, evidence register, etc.).

Fabricated-content rule preserved:
- v8 NAV items without a pod destination render as **greyed "not yet mounted"** tiles in the portal (not clickable, marked with a mono caption). No fabricated data.
- `POD_ONLY_TILES` surfaces the pod-only routes without inventing content.
- No `data-fidelity="prototype-sample"` DOM tags applied yet (v8 hosts sample content in specific per-app data constants like GOV/GM/TRUST/RB_CATS — the pod's existing components already render at REFERENCE-NOT-COPY fidelity for the domains they cover; adding prototype-sample rendering for the not-yet-mounted domains is Step 4's extension work and is left to owner ruling per the "no fabricated data unless explicit supersession" rule).

---

## §6. Step 5 — permanent close

**Ratchet floor bumped**: `passed_floor` **2363 → 2389** (+26 = 26 new v8 shell port invariants). Manifest failures unchanged at 0. Quarantine unchanged at 0. Skipped unchanged at 1. `ratchet_history` entry appended at 20260828T045000Z.

**Full-suite double-green identical**:
- Run 1: `phase0/drill_receipts/20260828T045000Z_wave_g_v8_shell_close_run1.log` · `passed=2389 / baseline-failures-remaining=0 / quarantined=0` · 92.68s.
- Run 2: `phase0/drill_receipts/20260828T045200Z_wave_g_v8_shell_close_run2.log` · `passed=2389 / baseline-failures-remaining=0 / quarantined=0` · 92.41s.
- Identity check: both receipt lines byte-identical.

**Right-reason RED banked pre-implementation**: `phase0/drill_receipts/20260828T044500Z_wave_g_step2_v8_shell_right_reason_fail.log`.

---

## §7. Per-surface reachability table

Every one of the 15 pod-shell routes is click-reachable from `/` (portal mode). Access paths:

| # | route | shell access path | source |
|---|---|---|---|
| 1 | `/registry` | Admin › Manage Estate › Registry (or greyed sibling tile) | V8_TO_POD_ROUTE.estate |
| 2 | `/shield` | Admin › Manage Estate › Shield | V8_TO_POD_ROUTE.govern |
| 3 | `/grey-mirror` | Admin › Manage Estate › Grey Mirror | V8_TO_POD_ROUTE.greymirror |
| 4 | `/chat` | Work › WorkStudio › Chat | V8_TO_POD_ROUTE.chat |
| 5 | `/thinklab` (+ `/thinklab/:mode`) | Work › ThinkLab › (Clarity/Strategy/Hypothesis/Perspective) | V8_TO_POD_ROUTE.clarity/strategy/hypothesis/perspective |
| 6 | `/training` | Build › Build Your Resources › Train Models | V8_TO_POD_ROUTE.train |
| 7 | `/models` | Build › Your Resources (tabs) › Models | V8_TO_POD_ROUTE.yourmodels |
| 8 | `/governance` | Admin › Approvals › Spend Requests · Rules Updates · Model Admission (all 3 items map to same pod component) | V8_TO_POD_ROUTE.spendreq/rulesupd/modeladmission |
| 9 | `/watch` | Admin › The Watch › State/Record/Under Watch/Decisions (all 4 items map to same pod component) | V8_TO_POD_ROUTE.wstate/wrecord/wunder/wdecisions |
| 10 | `/audit-trail` | Portal › Extras (pod-only) › Audit Trail | POD_ONLY_TILES[0] |
| 11 | `/skill-files` | Portal › Extras (pod-only) › Skill Files | POD_ONLY_TILES[1] |
| 12 | `/evidence-register` | Portal › Extras (pod-only) › Evidence Register | POD_ONLY_TILES[2] |
| 13 | `/commission` | Portal › Extras (pod-only) › Commission | POD_ONLY_TILES[3] |
| 14 | `/cost-ledger` | Portal › Extras (pod-only) › Cost Ledger | POD_ONLY_TILES[4] |

Not-yet-mounted v8 items (rendered greyed, no click target — honest empty): `analyze` · `documents` · `tasks` · `mentions` · `emails` · `projects` · `hrstuff` · `performance` · `board` · `agentbuild` · `extract` · `youragents` · `appsnew` · `appsfrequent` · `appsconnected` · `appsrequests`. Total: **16 not-yet-mounted surfaces marked EXTENSION-PENDING-OWNER-EYEBALL per Wave G Step 3 discipline** — each labelled in the DOM as "not yet mounted" via a mono caption.

**Owner may re-home items** after seeing this — the mapping is a single JSON-ish object (`V8_TO_POD_ROUTE`) trivially reconfigurable.

---

## §8. Non-goals of this close

- No new backend routes were added (only frontend shell).
- No pod component bodies were changed (only where they mount inside the shell).
- No canon-doc content was renegotiated (v8 self-cites canon — inline comment at pos=513138 — that trace was recorded in the inventory).
- No changes to the composite lock at 52.82%.

---

## §9. Standing arrivals unchanged

- **SSH interrupt priority** unchanged (chmod 600 → env vars → hardware fact sheet → CUDA verify-only → EP-4 precondition → first governed run → real MOAC → whitepaper → stop-and-report).
- **Owner one-liners still open** (CA1-N5 RTO seconds · DigiCow occupation-boolean PII call · Doc 10 evidence-record backfill decision · base-model census activation A17.10).
- **Decks/Documents build** remains BUILD-SCHEDULED-POST-PLAN.

---

## §10. Stop-and-report

Position: **HOLD** at ready state · v8 shell landed · double-green banked · **standing by for owner external verification** on:
1. Shell present with v8 chrome (RMS AI wordmark on `#0f1b33`, Iowan Old Style / Söhne / ui-monospace fonts, `#f5f2ea` paper background).
2. All 15 pod surfaces click-reachable from `/`.
3. No FarmaIQ artifacts in the default portal experience (residual code paths only, hidden behind seed data that no longer includes FarmaIQ).
4. Real data still rendering in the pod components (registry facts, DigiCow, GPU, audit-trail, watch, evidence-register — all served by unchanged pod components inside the new shell).

Receipt line to verify: `passed=2389 / baseline-failures-remaining=0 / quarantined=0`.

**HEADs to ratify**:
- Extraction-Akki `programme/track-a`: (commit SHA — to be recorded at commit time)
- Master workspace: (commit SHA — to be recorded at commit time)

---

**End of Wave G close report.**
