# v7 prototype inventory — RMS AI · Akki Prototype v7 (Standalone) · 2026-08-19

Source: `fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html` (sha256 `07df1d6846841da57ac0405536555262586362ac8d02a7bd682d9f3bebd6be55`, 1,307,752 bytes, 396 lines). Extract at `/tmp/v7_ingest/v7_extract.txt`. This is a **single-file standalone HTML** with an inline compiled React app (React.createElement in 10 places; 16 `React` refs; 107 onClick handlers; 119 top-level UPPER_SNAKE constants; no external routes, no fetch, no server).

Companion doc for v6: `notes/prototype_inventory.md` (Chunk-1, 2026-08-14) — read as the baseline against which this delta reads.

## 1 · Navigation lattice (v7)

### 1.1 Top tabs (`const TABS`)

| tab key | label | groups | right-aligned |
|---|---|---|---|
| `work` | Work | workstudio, thinklab, collab, monitor | no |
| `build` | Build | build, buildlib | no |
| `apps` | 3rd Party Apps | (empty) | no |
| `admin` | Admin | estate, approvals, watch | **yes** |

### 1.2 Nav groups (`const NAV`) — nine groups, forty-one item keys

| group `key` | group `label` | item `key` → `label` | count |
|---|---|---|---|
| `workstudio` | WorkStudio | `chat` → Chat · `analyze` → Data Suite · `documents` → Documents · `tasks` → Task Manager | 4 |
| `thinklab` | ThinkLab | `clarity` → Seek Clarity · `strategy` → Develop Strategy · `hypothesis` → Test Hypothesis · `perspective` → Get Perspective | 4 |
| `collab` | Collab | `mentions` → Mentions · `emails` → Emails · `projects` → Projects/Tasks · `hrstuff` → HR Stuff | 4 |
| `monitor` | Performance Management | `performance` → Exco 360 · `board` → Board 360 | 2 |
| `estate` | Manage Estate | `estate` → Registry · `govern` → Shield · `greymirror` → Grey Mirror | 3 |
| `approvals` | Approvals | `spendreq` → Spend Requests · `rulesupd` → Rules Updates · `modeladmission` → Model Admission | 3 |
| `build` | Build Your Resources | `train` → Train Models · `agentbuild` → Build Agents · `extract` → Extract Data | 3 |
| `buildlib` | Your Resources (tabbed sidebar) | `youragents` → Agents · `yourmodels` → Models | 2 |
| `thirdparty` | 3rd Party Apps | `appsnew` → New · `appsfrequent` → Frequent · `appsconnected` → Connected · `appsrequests` → Requests | 4 |

Total: **9 groups**, **29 direct nav items**, plus **P360_SUBS** = `['performance','signals','ideas']` (sub-nav under `monitor.performance` for Exco 360). The `watch` group referenced by `TABS.admin.groups` is NOT declared in NAV — it is a **standalone destination hook** (probably injected elsewhere in the module for the Watch Officer role).

### 1.3 Roles (`const ROLES`)

| role key | label | person | dept | initials | scoped groups |
|---|---|---|---|---|---|
| `compliance` | Compliance Owner | M. Chen | Compliance | MC | estate, approvals |
| `watch` | Watch Officer | A. Njeri | The Watch | AN | watch |
| `operator` | Operator | J. Otieno | Operations | JO | estate |

Three roles; each is a **static, illustrative persona** (no auth flow, no seat matrix, no permission enforcement in the standalone HTML).

## 2 · Registry surface (v7) — matches what we built

The v7 Registry lives at `estate.estate` (`Manage Estate → Registry`). Its interior tab keys map exactly to what we built to under the Registry brief PDF (`fixtures/screen_mockups_v7.pdf`):

- **DATA CONNECTED** — tab key `measure` (per `CONNECT_KINDS[data].tab`)
- **COMPUTE CONNECTED** — tab key `compute`
- **LLMS & TRAINED MODELS** — tab key `llms`

Copy-grammar honoured: "Where the row-mass sits", "drawn, never left blank", "Twelve connected sources make up the estate…", `≈` glyph for approximate figures, hatched bars for "not yet measured".

## 3 · Component fabric — top-level constants extracted

Complete list of the 40 constants harvested (byte-ranges vary; each is a JS literal — object, array or paren-expression):

| Constant | Bytes | Purpose |
|---|---:|---|
| `NAV` | 1,574 | Nine nav groups (§1.2 above) |
| `SUB_TO_GROUP` | 2 | Empty (`{}`) — reserved |
| `P360_SUBS` | 33 | Exco 360 sub-nav |
| `TABS` | 293 | Top tabs (§1.1) |
| `ROLES` | 364 | Personas (§1.3) |
| `TONE` | 393 | Style tokens: plain / held / refused / failed / drill |
| `FOURQ` | **602,224** | The four-questions content for every framed screen (Data / Reasoning / Access / Watch / Registry). Very large — the copy-of-record for the surface. |
| `CONNECT_KINDS` | 1,893 | Four kinds: data / llm / model / compute + methods per kind |
| `CONNECT_CREDS` | 288 | Two credential postures: issue / receive |
| `CONNECT_CHIPS` | 321 | Wizard chip labels per stage |
| `WIZ` | 5,277 | Two wizards: `rulebook` (rule update ceremony) + `actor` (admit user/model). |
| `CONNECT_STAGES` | 172 | Five-stage Connect wizard: What / How / Credentials / Name / Ready |
| `GOV` | 33,634 | Shield surface (overview / rulebook / enforcement / updates) with charts, rows, filters |
| `RB_CATS` | 8,516 | Rule-book categories (System Gates, LLM Interaction Rules, Confidential Data Management, …) |
| `GM` | 40,583 | Grey Mirror surface (overview / monitor / response / people) — the Watch/Mkondo surface |
| `LLM_STATS` | 746 | 9 stat tiles for LLMs tab (128,400 calls, KES 1.9M, etc.) |
| `LLMS` | 1,012 | 5 model rows: Claude Sonnet 5, Swahili TRN-007, Embedding EMB-002, Long-context (eval), Legacy SUM-001 (retired) |
| `LLM_NARRATIVE` | 557 | Per-filter narrative sentences |
| `LLM_CHARTS` | 1,190 | 3 charts: calls / spend / refusals |
| `COMPUTE_CHARTS` | 1,181 | 3 charts: door / week / state |
| `FLOWS` | 1,141 | 7 workflow rows spanning ongoing/complete/failed |
| `FLOW_NARRATIVE` | 542 | Per-filter narrative sentences |
| `CHARTS` | 2,026 | 4 estate charts: language / type / rights / condition (composition of 86.4 TB) |
| `PAGE_TOPLINE` | 1,555 | Eyebrow/headline/sub per page (rules/wrecord/wunder/wdecisions/people/ceremonies) |
| `FQ_TOPLINE` | 1,948 | FQ eyebrow/headline/sub per surface (wstate/datashield/reasoningshield/accessshield/govern/greymirror) |
| `WALKS` | 3,316 | Four walk stories: bait / crossing / rule / broken (the "Walk this →" affordance content) |
| `BRIEF_SUB` | 4,603 | 6 sub-briefs for visual+table drill-in (estate-visual, estate-table, gov-visual, gov-table, gm-visual, gm-table) |
| `EST_GROUPS` | 4,656 | Per-surface tile groups (gov: overview/rulebook/enforcement/updates; gm: overview/monitor/response/people; and others) |
| `TRUST` | 15,608 | Trust Center content (datashield / reasoningshield / accessshield subsurfaces, each with rows/charts/tables) |
| `BRIEF` | 5,200 | Highlight briefs (gm / gov / estate / datashield / reasoningshield / accessshield) — two-page reads |
| `APPROVALS` | (not extracted, cost) | Approvals surface content |
| `RULES_IN_FORCE` | " | Rules-in-force ledger |
| `RAILS` | " | Rails (governance rails visualisation) |
| `CEREMONY_STAGES` | " | Ceremony wizard stages |
| `CEREMONIES` | " | Ceremony ledger |
| `RECORD_ROWS` | " | Record-table rows |
| `LANE_COPY` | " | Copy for the "lane" mechanism |
| `PATTERNS` | " | Watch patterns |
| `DECISIONS` | " | Decisions ledger |
| `ACTORS` | " | Actor register (people/agents/models) |

Total: **40 constants**. FOURQ (~590 kB) is the copy-of-record for every screen's four-question deck.

## 4 · Screen inventory — v7 pages

Cross-tabulating `NAV` × `TABS` gives the destination map. All screens are React function components inline in the same file; navigation is `s.navSub` state (screen key) + `s.navGroup` state (group key), same pattern as v6.

**Work tab:**
- WorkStudio: `chat` · `analyze` (Data Suite, was "Analyze" in v6) · `documents` · `tasks`
- ThinkLab: `clarity` · `strategy` · `hypothesis` (was "Simulate a Hypothesis" in v6, now "Test Hypothesis") · `perspective`
- Collab: `mentions` · `emails` · `projects` · `hrstuff`
- Performance Management: `performance` (Exco 360 — replaces v6 "Performance") · `board` (Board 360 — NEW)

**Build tab:**
- Build Your Resources: `train` · `agentbuild` · `extract` (v6 also had `youragents`)
- Your Resources: `youragents` · `yourmodels` — NEW as a sidebar-tabbed group

**3rd Party Apps tab:**
- `appsnew` · `appsfrequent` · `appsconnected` · `appsrequests`

**Admin tab:**
- Manage Estate: `estate` (Registry — the tab we built) · `govern` (Shield — the FQ triple: DataShield + ReasoningShield + AccessShield with `Rules Updates` linkage) · `greymirror` (Grey Mirror — the Watch surface)
- Approvals: `spendreq` (Spend Requests) · `rulesupd` (Rules Updates) · `modeladmission` (Model Admission) — the three ceremony surfaces
- Watch: (destination hook without a declared NAV entry — Watch Officer role sees it)

**Additional screens named in FQ_TOPLINE / BRIEF / GOV / GM / TRUST but reachable through `walk:` and `toast:` affordances rather than nav:**
- Walk-in-place cards: `walk:bait`, `walk:crossing`, `walk:rule`, `walk:broken` (4 stories)
- Sub-briefs: 6 (estate-visual/table, gov-visual/table, gm-visual/table)
- Wizards (`WIZ`): `rulebook` (rule-book update ceremony), `actor` (admit person/agent/model)
- Connect wizard (`CONNECT_STAGES` × `CONNECT_KINDS` × `CONNECT_CREDS`): five stages, four kinds, two credential postures = 40+ terminal states

Screen count (accessible destinations): **~28 primary nav items + ~30 ceremony/walk/wizard states = ~58 distinct rendered surfaces**.

## 5 · Seeded copy verbatim (a representative slice; full oracle sits in FOURQ + GOV + GM + TRUST)

**Registry (`estate`):**
- Topline: "Held: 86.4 TB across 12 sources · Measured: 78% at census #4 · Not yet measured: 22%, shown at full weight · Opportunities: 6 standing ready · Last census: Jul 21, 2026 · J. Mwangi"
- Composition by language: English 46% · Swahili 24% · Sheng 8% · French 6% · Not yet measured 12% (10.4 TB, hatched)
- Composition by type: Audio archive 48% · Database 23% · Documents 11% · Logs 9% · Email 3% · Not yet measured 6%
- Composition by rights: Internal only 74% · Regulatory 9% · Licensable 4% · Not yet measured 13%
- Condition: Clean 41% · Telephone-grade 27% · Scanned 12% · Sparse 8% · Not yet measured 12%

**Compute:**
- Hours by door: Train 645 · Extract 298 · Export 174 · Measure 99 · Prove 24 (1,240 hrs committed)
- Hours by week: Aug 1–7: 274 · Aug 8–14: 339 · Aug 15–21: 65 · Not yet run 43 (hatched)
- Hours by state: Committed 1,240 · Free to allocate 1,640 (2,880 available)

**LLMs & Trained Models (5 rows verbatim):**
- Claude Sonnet 5 · bought-in · 71,200 calls · 55% share · in service · "General reasoning and drafting, answering in-seam · last acceptance Aug 8, all six checks held"
- Swahili call-center model TRN-007 · trained here · 38,900 calls · 30% · in service · "Trained on 4,120 hrs of verified calls, runs on the attached cluster · last acceptance Aug 11"
- Embedding model EMB-002 · trained here · 14,100 calls · 11% · in service · "Retrieval over the estate, weights never leave the cluster · last acceptance Jul 30"
- Long-context reasoning model · bought-in · 4,200 calls · 4% · evaluating · "Sandbox only · four of six checks passed · answers nothing real yet"
- Legacy summariser SUM-001 · trained here · 0 calls · retired · "Failed the citation check Jun 2 · out of service the same day"
- Stats: 4 models connected · 128,400 calls this month · 1,842 refused at the shield · 2.4s median · KES 1.9M spend · 100% context masked · 6 acceptance checks · 1 retired · drift testing "Not yet measured, drawn, never left blank"

**Connect wizard (`CONNECT_STAGES`):**
`['What would you like to connect?','How would you like to connect it?','Will you be issuing credentials, or receiving them?','What should it be called?','Ready to connect']`

## 6 · Demo-data inventory (what is fabricated vs what would be real)

**Every figure in v7 is demo data.** The prototype is a single-file HTML with no backend and no data pipeline. Numbers, people, receipts, timestamps, model names — all seeded. Concrete inventory of demo tokens (partial):
- Named people: Maria Chen, J. Otieno, A. Njeri, J. Whitfield, J. Mwangi, D. Okafor
- Named agents: ACT-1189, ACT-1043
- Named receipts: R-4390, R-4471, R-4472, R-4102, R-4388, R-4401, R-4388
- Named rules: R-014 v2, rule versions "v1", "v3"
- Named marks / witnesses: M-0219, W-8841, W-8842
- Named bait: BR-77
- Sizes: 86.4 TB across 12 sources; 41.2 TB customer service calls; KES 1.9M monthly spend
- Model names: Claude Sonnet 5 · TRN-007 · EMB-002 · SUM-001
- Rulebook categories seeded: sg1..sg4, lr1..lr3, cd1..cd?, etc.

None of these tokens correspond to anything in our built estate.

## 7 · v6 → v7 delta

Compared line-by-line with `notes/prototype_inventory.md`:

### 7.1 Nav groups added in v7
- `estate` (Manage Estate) — **replaces v6 `registry`** (Registry group). Adds `greymirror` (Grey Mirror surface) as a sibling of Registry and Shield.
- `approvals` (Approvals) — NEW three-item group: Spend Requests · Rules Updates · Model Admission. In v6, ceremonies were only reachable via wizards, not a dedicated nav.
- `buildlib` (Your Resources) — NEW two-item sidebar-tabbed group split out of `build`.

### 7.2 Nav groups removed in v7
- `trust` (Trust Center) — v6 had four items (Manage Rules, Data Shield, Reasoning Shield, Access Shield). In v7 these three shield surfaces have moved into `estate.govern` (Shield), and Manage Rules moves to `approvals.rulesupd`.

### 7.3 Nav items renamed
| v6 key + label | v7 key + label |
|---|---|
| `analyze` → "Analyze" | `analyze` → **"Data Suite"** |
| `hypothesis` → "Simulate a Hypothesis" | `hypothesis` → **"Test Hypothesis"** |
| `monitor.performance` → "Performance" | `monitor.performance` → **"Exco 360"** |
| — | `monitor.board` → **"Board 360"** (NEW; Promise Table A1) |

### 7.4 Nav items removed
- `monitor.signals` (Signals) — removed as top-level; retained as a `P360_SUBS` sub-item under Exco 360.
- `monitor.ideas` (Ideas by Akki) — same; retained as a `P360_SUBS` sub-item.
- `registry.estate` (Data Estate), `registry.models` (Models), `registry.compute` (Compute), `registry.connect` (Connect) — collapsed into a single **Registry** node with the three sub-tabs (Data / Compute / LLMs & Trained Models).
- `build.youragents` — moved to `buildlib.youragents`.

### 7.5 Nav items added
- `monitor.board` — Board 360 (Promise Table A1).
- `estate.greymirror` — Grey Mirror surface (Watch, Promise Table #6/#7).
- `approvals.spendreq` — Spend Requests (Promise Table A6).
- `approvals.rulesupd` — Rules Updates (rule-book update ceremony surface, Promise Table #27).
- `approvals.modeladmission` — Model Admission (six-criterion acceptance surface, Promise Table #22).
- `buildlib.yourmodels` — trained-model library.

### 7.6 Tabs unchanged; Admin membership shifted
- Both v6 and v7 have `work · build · apps · admin`, admin right-aligned.
- v6 admin: `trust, registry`.
- v7 admin: `estate, approvals, watch`.

### 7.7 Component-fabric additions
- `PATTERNS`, `DECISIONS`, `ACTORS`, `RAILS`, `CEREMONY_STAGES`, `CEREMONIES`, `RULES_IN_FORCE`, `APPROVALS`, `LANE_COPY`, `RECORD_ROWS`, `LLM_STATS`, `LLM_NARRATIVE`, `LLM_CHARTS`, `COMPUTE_CHARTS`, `FLOW_NARRATIVE`, `PAGE_TOPLINE`, `FQ_TOPLINE`, `BRIEF_SUB`, `EST_GROUPS`, `TRUST`, `BRIEF`, `GM`, `RB_CATS`, `GOV`, `WALKS`, `WIZ` — most are new or greatly expanded in v7 vs v6.

### 7.8 Copy grammar
- v6's "Analyze" surface metaphor becomes v7's "Data Suite".
- v7 adopts systematic "≈" glyph for approximate figures (matches the Registry brief PDF's provenance rule).
- v7 introduces the "Walk this →" affordance canonicalised as a top-level pattern with four exemplar walks.
- v7 introduces "the four questions" as an explicit deck grammar across every framed surface (was implicit in v6).

## 8 · Cross-references

- **Canon 5 (Interface Architecture) mappings**: v7 preserves the five-pillar mapping via `estate` (Registry + Shield + Grey Mirror), `approvals` (ceremonies), and `workstudio+thinklab` (WorkStudio + ThinkLab). See `notes/canon_5_requirements.md` for the canonical pillar list.
- **Screen Mockups PDF (fixtures/screen_mockups_v7.pdf)**: the Registry brief we already built to. v7's Registry surface conforms to this PDF's page pattern (fluid left + 300px right context panel; Topline/Visual/Table bands; content rules §6). Our built Registry.jsx honours the same.
- **Tile-grid screenshot**: not yet seen in this cycle (owner's earlier tile-grid reference in message 244 predates the v7 drop).
- **Currently built**: Registry (3 tabs, real facts) · ConnectWizard (paste-and-connect panel + Provisioning-card aside) · IP-allowlist middleware · four-questions grammar in the compute detail card only. Every other v7 nav destination is not built.

## 9 · Immediate technical honesty

- **v7 is a single-file HTML.** It has no backend, no /api routes, no data pipeline, no auth. It is an oracle for grammar and copy, not for behaviour.
- **Our estate is a React SPA + FastAPI + Aurora Data API** under strict IP allowlist. Rendering v7's copy against real records is exactly what the Registry cycle just did — and the collision surface for the rest of v7 is enumerated in `notes/tension_table_2026-08-19.md`.
