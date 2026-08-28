# v8 Prototype Inventory — `Akki Platform (RMS AI) — v8`

**Source files (verified bytes only):**

| file | sha256 | bytes |
|---|---|---:|
| `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` | `e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2` | 1,264,425 |
| `fixtures/Akki_Platform_v8_Design_Spec.docx` | `d7cfd3aed244da1b53b7b86ed9572852b8e6e928f2294d6f94083ff775491304` | 108,191 |

**Derived (this session):**

| file | sha256 | bytes | provenance |
|---|---|---:|---|
| `notes/wave_g_step0_v8/v8_template_decoded.html` | `9177c2b910b9caf5b07d6887317b37404443da83f548166da6f6e08f858e3a9a` | 1,111,498 | JSON-decoded inline template extracted from bundler manifest inside the HTML |
| `notes/wave_g_step0_v8/v8_design_spec.txt` | (docx-extracted plain text) | 39,635 | via `python-docx` paragraph+table walk, 312 lines |

Citation format used throughout:
- `[v8-HTML:pos=N]` = byte position inside the **decoded** template (`v8_template_decoded.html`). All byte positions in this file refer to that decoded artifact.
- `[v8-Docx:§X.Y line N]` = section+line reference inside `v8_design_spec.txt` (docx paragraph-preserving extraction).

Absence-is-a-finding rule: fields the spec is silent on are explicitly marked "NOT IN v8" rather than left blank.

---

## §0. Verdict (Step 0)

**Identity = Akki OS.** File-of-record `Akki Prototype v8.dc.html` is the branded instance **RMS AI** [v8-Docx:§1 line 4 · "Build: v8 · Branded instance: RMS AI · Source file: Akki Prototype v8.dc.html"]. Wordmark literal in the top bar is `RMS AI` [v8-HTML:pos≈1655 · verbatim `<div style="font-family:var(--head);…">RMS AI</div>` inside the 52-px header on `var(--blue2)`]. The docx confirms this is the only literal brand token; the same product has previously shipped as BDO AI, DigiCow AI, TrinityAI by swapping that one string [v8-Docx:§1 line 13].

Farma IQ has been **removed** from the default `agentsList` in v8; the two seeded deployed agents in v8 are `Vendor Risk Monitor` (Deployed) and `Payroll Variance Checker` (Ready to deploy) [v8-HTML:pos=453684 · agentsList seed literal]. Residual `Farma IQ` string references (14 hits total) are legacy state-machine plumbing (`fqAppOpen`, `openDeployedAgent(a){ if(a.name==='Farma IQ'){…}}` etc.) that fire only if a `Farma IQ`-named agent is re-added; **they never render by default**.

Full identity verification receipt banked at `phase0/drill_receipts/20260828T041500Z_wave_g_step0_v8_identity_verification.log`.

---

## §1. Product overview (verbatim quotable claims)

- **"Akki is a unified AI governance and intelligence platform for an operating company. It combines a grounded chat assistant, document and task workflows, performance monitoring (Exco 360 / Board 360), an AI agent and model registry, a security-monitoring service ('The Watch' / 'Grey Mirror'), and a full rules-and-entitlements governance layer ('Shield') — all backed by one append-only audit record."** [v8-Docx:§1 line 12]
- **"This build is branded RMS AI. The wordmark in the top bar is the only literal brand token in the file; the identical underlying product has previously shipped under other brand names (BDO AI, DigiCow AI, TrinityAI) by swapping that one string."** [v8-Docx:§1 line 13]
- Design law (verbatim): **"Four-questions surfaces. Rule zero: every block leads with a sentence; measures live behind 'see the working'."** [v8-Docx:§1 line 15]

Voice principles catalogued [v8-Docx:§1 lines 16–21] — five bullets, exact:
1. Refusals framed as proof, not failure ("A refusal is the system keeping its promise.")
2. Every quantitative claim carries its honesty caveat; "Not yet measured" drawn as its own category, never blank.
3. Numbers carry lineage: receipt ID, audit ID, or census date accompany nearly every figure.
4. Plain sentences lead even the densest governance data.
5. Third-person register ("Held for review. Nothing is lost."), rarely user-addressed.

---

## §2. Design system (v8-Docx §2)

### 2.1 Color tokens [v8-Docx:§2.1 lines 23–43]

| token | value | usage |
|---|---|---|
| `--paper` | `#f5f2ea` | Page / app background (warm off-white) |
| `--surface` | `#f0ece1` | Panel background, one step deeper than paper |
| `--surface2` | `#ede8da` | Pills, hover states, chart track background |
| `--line` | `#e4dfd3` | All hairline borders |
| `--ink` | `#1b1f27` | Primary text |
| `--ink2` | `#3d4350` | Secondary text / body copy in cards |
| `--ink3` | `#5b6270` | Tertiary text, meta lines, timestamps |
| `--blue` | `#16274a` | Primary brand navy — buttons, links, active tab, icon marks |
| `--blue2` | `#0f1b33` | Deep navy — top bar background, dark app bars |
| `--oxblood` | `#b8395b` | Danger border (refusal cards, cancel buttons) |
| `--oxblood2` | `#c64e6e` | Danger fill (refused-message backgrounds, "Rejected" pill) |
| `--brass` | `#b08d2e` | Warning / held / pending amber |
| `--sage` | `#1d7a6e` | Success / verified / in-service green |
| `--accent` | `#4c5fd5` | Secondary interactive accent (ThinkLab throughout) |
| `--accent-soft` | `rgba(76,95,213,.10)` | Accent tint background |
| `--scrim` | `rgba(15,27,51,.42)` | Modal / drawer backdrop |
| `--shadow-drawer` | `-14px 0 48px rgba(15,27,51,.18)` | Right-drawer elevation |

Additional tokens present in HTML but not enumerated in docx: `--surface2:#ede8da` (already above); `--shadow-pop:0 22px 64px rgba(15,27,51,.26)`; `--drawer-w:min(460px,94vw)`; `--drawer-wide:max(480px,50vw)` [v8-HTML:pos≈1330–1610 · style variable block on the root div].

### 2.2 Status-pill colors [v8-Docx:§2.1 lines 45–54 · `statusColors()` function]

| status | bg | fg |
|---|---|---|
| Uploaded | `rgba(91,98,112,.10)` | `#5b6270` |
| In Progress | `rgba(22,39,74,.10)` | `#16274a` |
| Committed / Live / On track / Deployed / Accepted / Ready to deploy | `rgba(29,122,110,.12)` | `var(--sage)` |
| Draft / In Review / At risk / In progress / Pending approval | `rgba(176,141,46,.12)` | `var(--brass)` |
| Rejected / Not started | `rgba(184,57,91,.12)` | `var(--oxblood2)` |
| (any other value) | `var(--surface2)` | `var(--ink2)` |

### 2.3 Typography [v8-Docx:§2.2 lines 57–62]

| role | stack | usage | sizes |
|---|---|---|---|
| Head | `Iowan Old Style, Georgia, serif` | Headlines, card/modal titles, big stat numbers | 16.5–31px |
| Body | `Söhne, Helvetica Neue, Arial, sans-serif` | All UI text, buttons, body copy | 11–15px |
| Mono | `ui-monospace, Menlo, Consolas, monospace` | Eyebrows, meta lines, receipt/audit IDs, governance-surface tab labels | 9–11px, uppercase, letterspaced `.06–.12em` |

Confirmed in HTML root style declaration: `--head:Iowan Old Style,Georgia,serif;--body:Söhne,Helvetica Neue,Arial,sans-serif;--mono:ui-monospace,Menlo,Consolas,monospace` [v8-HTML:pos≈1520–1600].

### 2.4 Shape, spacing, elevation [v8-Docx:§2.3 lines 64–70]

- Corner radius: 6–9px on controls/small cards; 10–14px on panels/cards; 50% on avatars/status dots.
- Card default: 1px solid `var(--line)`, white or `var(--surface)` fill, 14–18px padding, no shadow at rest.
- Left-accent cards (chat answers, collab items, rule cards): 2–3px solid left border in a semantic color — sage=answered/positive, oxblood=refused/danger, blue=neutral fact — with that corner squared off.
- Drawers slide from the right at `var(--drawer-w) = min(460px, 94vw)`; shadow=`var(--shadow-drawer)`; backdrop=`var(--scrim)`.
- Modals centered, white, 12–14px radius, max-width 380–620px.
- Buttons: primary=solid `var(--blue)` fill/white text; ghost/secondary=white fill/`var(--line)` border/`var(--ink2)` text; destructive=`var(--oxblood)` or `var(--oxblood2)` outline/fill.

### 2.5 Recurring components [v8-Docx:§2.4 lines 71–81]

1. **Stat-card grid** (§2.4/Stat-card grid) — 3-column grid, 1px hairline seams (`var(--line)` showing through 1px gaps); each cell white; uppercase mono eyebrow label; 25px serif value; 11.5px ink3 note. Opens every Governance Surface block.
2. **Horizontal bar chart** — row = 110px label + flexible track (14px tall, `var(--surface2)` bg, 3px radius) + 104px right-aligned size label. Dropdown above the chart switches the cut (e.g. by language, by type, by rights class).
3. **Table row (governance list)** — NOT literal HTML `<table>`; each row is a padded block: bold 12.5px sentence, small meta line (class · count), fuller meta sentence, right-aligned blue link ("Walk this →", "Open the rule →"). Colored state pill sits top-right.
4. **Tabs — two styles**:
   - (a) Underline tabs: 13px semibold, 2px colored bottom border on active — simple in-page switches.
   - (b) Governance-surface tabs: 11.5px bold uppercase letterspaced, same underline treatment — used on Shield, Registry, Grey Mirror.
5. **Pills / chips**:
   - Filter chips: 11.5px bold, 14px pill radius, colored border+bg+text when active, white/`var(--line)`/`ink2` inactive.
   - Status pills: 10–10.5px bold uppercase, 10–11px radius, colored per `statusColors()`.

---

## §3. Global application shell (v8-Docx §3)

### 3.1 Top bar [v8-Docx:§3.1 lines 83–86]

- Fixed 52px height, background `var(--blue2)` (`#0f1b33`).
- Left: **19×22 shield-outline SVG mark** + **wordmark `RMS AI`** in `var(--head)` 16px, letterspacing `.02em`, color `var(--paper)`.
- Right: **role/department text** (12px, `#c9c2ae`), then a **27px circular avatar** (bg `#28345c`, 2-letter initials, 11px, `#efe9da`).

Confirmed literal in template — the SVG path is a shield-plus-checkmark composite: `d="M12 1.5 22 5.2v8.1c0 6.2-4.2 10.9-10 13.2C6.2 24.2 2 19.5 2 13.3V5.2L12 1.5Z"` (shield outline) and `d="m7.7 13.6 3 3 5.6-6"` (inner checkmark) [v8-HTML:pos≈1785–1965].

### 3.2 Portal mode (no app open) [v8-Docx:§3.2 lines 87–90]

Below the top bar the body splits into two panes:
- **Left pane** — 45% width, `var(--surface)` bg, right border, 24/34px padding: the Tab pill-groups, then the grouped nav list (§4), then — only on the Build tab — a row of deployed-agent tiles ("Deployed — open directly").
- **Right pane** — 55% width: a "landing" card for the selected nav item — white, max-width 600px, 16px radius, holding an icon, group/app label, a generated greeting line, an optional "last activity" glimpse, tip bullets, and Continue/Start-new buttons with a usage stat.

Confirmed in template: `<sc-if value="{{ portalMode }}" hint-placeholder-val="{{ true }}"> <div style="flex:0 0 45%;…background:var(--surface);border-right:1px solid var(--line);padding:24px 34px 50px;overflow-y:auto;">` [v8-HTML:pos≈2740–2830].

### 3.3 App mode (an app is open) [v8-Docx:§3.3 lines 91–95]

- **Single column.** Slim header row: app-group mono breadcrumb on the left; app-specific controls on the right (Documents shows an "Exposure site map" pill; Chat shows the editable conversation title).
- **Optional session banner** appears on Watch and Shield/Trust apps: colored dot + "Watch session · recorded." or "Governance session · recorded." in brass or sage.
- Below sits the app's body — specified per app in §6–§15 of the docx.
- **Exit** always returns to portal mode.

Session banner literal in template: `sessionBanner: appGroup==='watch'? 'Watch session · recorded.' : 'Governance session · recorded.', sessionBannerColor: appGroup==='watch'? 'var(--brass)' : 'var(--sage)'` [v8-HTML:pos≈1008040].

### 3.4 Navigation rendering rules [v8-Docx:§3.4 lines 96–100]

- **Tabs** (Work / Build / 3rd Party Apps left-aligned, **Admin right-aligned**) are pills in an `rgba(22,39,74,.1)` track; active tab gets a solid/tinted fill.
- Each nav group renders as **label + vertical item list**, except a group flagged `tabs:true` (`buildlib` = "Your Resources"), which renders items as an **inline horizontal tab row**.
- A group flagged `divider:true` gets a **hairline rule above it**.
- **Deployed-agent tiles** (Build tab only) list every agent whose `status==='Deployed'`; each opens that agent's dedicated full-screen app.

Confirmed literal: `showDeployedTiles: s.navTab==='build'` and `deployedAgentsView: this.allAgents().filter(a=>a.name==='Farma IQ').map(…)` — the Farma-IQ filter is a legacy carryover, but the default `agentsList` (see §0 verdict) drives what actually shows [v8-HTML:pos≈908000–908450].

---

## §4. Navigation taxonomy (verbatim from `const NAV / TABS / ROLES`)

**TABS literal** [v8-HTML:pos≈514470]:

```js
const TABS = [
  { key:'work',  label:'Work',            groups:['workstudio','thinklab','collab','monitor'] },
  { key:'build', label:'Build',           groups:['build','buildlib'] },
  { key:'apps',  label:'3rd Party Apps',  groups:[] },
  { key:'admin', label:'Admin',           groups:['estate','approvals','watch'], right:true }
];
```

**NAV literal** [v8-HTML:pos≈511700 opening `const NAV = [` … pos≈513125 closing `];` + `NAV.push({...watch group...})` at pos≈513850]:

| # | key | label | flags | items (key → label) |
|---|---|---|---|---|
| 1 | `workstudio` | WorkStudio | — | `chat`→Chat · `analyze`→Data Suite · `documents`→Documents · `tasks`→Task Manager |
| 2 | `thinklab` | ThinkLab | — | `clarity`→Seek Clarity · `strategy`→Develop Strategy · `hypothesis`→Test Hypothesis · `perspective`→Get Perspective |
| 3 | `collab` | Collab | — | `mentions`→Mentions · `emails`→Emails · `projects`→Projects/Tasks · `hrstuff`→HR Stuff |
| 4 | `monitor` | Performance Management | — | `performance`→Exco 360 · `board`→Board 360 |
| 5 | `estate` | Manage Estate | — | `estate`→Registry · `govern`→Shield · `greymirror`→Grey Mirror |
| 6 | `approvals` | Approvals | — | `spendreq`→Spend Requests · `rulesupd`→Rules Updates · `modeladmission`→Model Admission |
| 7 | `build` | Build Your Resources | — | `train`→Train Models · `agentbuild`→Build Agents · `extract`→Extract Data |
| 8 | `buildlib` | Your Resources | `divider:true`, `tabs:true` | `youragents`→Agents · `yourmodels`→Models |
| 9 | `thirdparty` | 3rd Party Apps | — | `appsnew`→New · `appsfrequent`→Frequent · `appsconnected`→Connected · `appsrequests`→Requests |
| 10 | `watch` | The Watch | appended via `NAV.push(...)`; shown only when `Watch Officer` role is active | `wstate`→State · `wrecord`→Record · `wunder`→Under Watch · `wdecisions`→Decisions |

**Docx spec §4 lists 10 groups matching the above** [v8-Docx:§4 lines 111–123].

Additional group mounted dynamically but not in `NAV` array literal:
- `instance` — Instance / People & Declarations / Ceremonies group. Used in `appGroup==='instance'` mount branch [v8-HTML:pos≈1009238 · `isInstanceGroup: appGroup==='instance' && appMode`]. Docx spec §15 describes it as "Instance — People & Declarations / Ceremonies" [v8-Docx:§15 lines 262–265]. **NOT in NAV taxonomy** — access path is via ceremony surfaces or role-restricted deep links.

**SUB_TO_GROUP inversion** [v8-HTML:pos≈514355]:
```js
const SUB_TO_GROUP = {};
NAV.forEach(g => g.items.forEach(it => { SUB_TO_GROUP[it.key] = g.key; }));
SUB_TO_GROUP.signals='monitor'; SUB_TO_GROUP.ideas='monitor';
const P360_SUBS=['performance','signals','ideas'];
```

The `signals` and `ideas` keys are sub-tabs inside `Exco 360` (per docx §9.1); they route to the `monitor` group visually.

**ROLES literal** [v8-HTML:pos≈514800]:

| role key | label | person | dept | initials | groups visible |
|---|---|---|---|---|---|
| `compliance` | Compliance Owner | M. Chen | Compliance | MC | `estate`, `approvals` |
| `watch` | Watch Officer | A. Njeri | The Watch | AN | `watch` |
| `operator` | Operator | J. Otieno | Operations | JO | `estate` |

Docx §4 confirms exactly this table [v8-Docx:§4 lines 125–130].

**Role gating rule**: on the Admin tab, only the groups in the active role's `groups` array render.

**Restricted sub-set** (per HTML `RESTRICTED = new Set(['wstate','wrecord','wunder','wdecisions'])`) [v8-HTML:pos≈899950] — Watch sub-surfaces render with sage tinting when the current role doesn't own them (a locked-preview affordance).

**Canon citation comment** inline before `NAV.push(watch)` at [v8-HTML:pos=513138]:

```
/* v7 — label ↔ canon identity mapping (§4 of the v7 brief), recorded here as required:
   Manage Rules            → The Rulebook + change ceremony (Doc 3 Part V, Doc 5 §23)
   Data Shield             → Boundary custody: chain, receipts, disclosure (Doc 3 §13–§20)
   Reasoning Shield        → Reasoning assurance: depth, evidence bars, traces (Doc 4 Part IV)
   Access Shield           → Entitlement + Access surface (Doc 3 §22.1, Doc 5 §41)
   Data Estate             → Estate Map / census & registry reading (Doc 5 control band)
   Models / Compute / Connect → Model registry & ladder · economics/metering · integration wizard (Docs 4, 7)
   State / Record / Under Watch / Decisions → The Watch Console's four panels (Doc 8 §13, Doc 5 Part VII-A)
   People & Declarations   → Admission declarations (Doc 3 §6.1)
   Ceremonies              → The change ceremony pipeline (Doc 3 §24)
*/
```

This is the file's own self-declared canon-doc mapping — binding for the assessment.

---

## §5. Governance Surface template (v8-Docx §5)

**One layout is reused, unmodified, across:**
- **Shield** (Data / Reasoning / Access sub-tabs)
- **Grey Mirror** (all four tabs)
- **Registry** (Data / Compute / LLM sub-tabs)
- **Rule Book** (via View more)
- **Trust Center** (Registry-side mirror)

### 5.1 Structure [v8-Docx:§5.1 lines 134–139]

- **Tab row**: underline, mono-style tabs for the sub-surfaces (e.g. Data / Reasoning / Access).
- **Grid**: `max-width:1180px`, two columns — `minmax(0,1fr)` content + `minmax(240px,300px)` sticky aside, 44px gap, separated every block by a full-width hairline.
- **Block 1 — Stats**: eyebrow + one-liner, then the 3-column stat-card grid; aside shows headline eyebrow, a large serif sentence with 2–3 inline underlined callout phrases, a sub-line, and a "View more →" link to the Brief modal (§16.2).
- **Block 2 — Visual**: eyebrow + chart-cut dropdown, one-liner, horizontal-bar chart card, footer note; aside repeats eyebrow+body+View-more.
- **Block 3 — Table**: eyebrow + filter-chip row, one-liner, card with 2-column header ("What happened / Result") then row list and "View/Walk the full record →" link; closing narrative sentence below card; aside repeats.

### 5.2 Field shape [v8-Docx:§5.2 lines 141–153]

Per-instance field shape (for regenerating or extending):

| field | purpose |
|---|---|
| `tab` / `topEyebrow` / `topOneliner` | Tab label and the one-line framing sentence |
| `headEyebrow` / `headDeck` / `headSub` | Big-sentence stats-aside block (`headDeck` holds inline `<span>` underline/color callouts) |
| `stats[]` | 9 objects `{label, value, note}` for the 3×3 stat grid |
| `visualEyebrow` / `visualOneliner` / `visualFoot` | Copy around chart |
| `charts{}` | Keyed by cut name → `{label, title, caption, rows:[{label, pct, size, fill}]}` |
| `tableEyebrow` / `tableOneliner` / `tableTitle` | Copy around table |
| `filters[]` | Chip labels — first entry always "All" |
| `rows[]` | `{text, cls, state, count, lane, meta, link, go}` |
| `narrative` | Closing sentence under table |
| `tableAsideTitle` / `tableAsideBody` | Right-hand explanation |

**Worked example — Shield › Data** [v8-Docx:§5.2 lines 155–160]:
- `tab: "Data"` · `topEyebrow: "What leaves, and how"`
- `headDeck: "4,182 crossings this week — every one masked, and nothing left without a receipt."`
- Sample stat: `{label:"Crossings this week", value:"4,182", note:"each with its receipt"}`
- Sample row: `{text:"A pricing question needed customer records, and they crossed masked", cls:"Mask tier 2", state:"Crossed", count:"Tue 14:02", lane:"Crossed", meta:"118 fields swapped · receipt R-4390, replayed successfully Aug 13", link:"Walk the crossing →"}`
- `narrative: "Four of 4,194 asks shown. Every crossing here can be replayed from its receipt, and a refusal reads as plainly as a success."`

**Full literal dataset lives in source constants:** `GOV`, `GM`, `TRUST`, `RB_CATS`, `EST_GROUPS` — see §17 appendix.

---

## §6. WorkStudio (v8-Docx §6) — 4 apps

### 6.1 Chat (Akki) [v8-Docx:§6.1 lines 162–172]

- **Purpose**: default landing app — grounded chat assistant over the whole estate, with full audit provenance on every answer.
- **Layout**: three panes inside content column — **220px conversation rail**, center thread+composer, **220px collapsible Audit Trail panel** ("Shield & Provenance").
- **Conversation rail**: "+ New conversation", archive-drawer icon, conversation list (title, relative last-active time, kebab menu → Rename / Delete). Delete opens "Archive this chat?" confirmation — chats archive not hard-delete until permanently removed from Archive drawer.
- **Empty-thread state**: four suggestion buttons, each demonstrating one canonical response shape.
- **Message types** (6 shapes):
  1. User bubble — right-aligned, editable, "Save & branch" forks thread into branch pageable with ←/→
  2. Assistant "Working" — sequential thinking steps, sage dot
  3. Assistant "Answered" — **sage left border**, sentence with one bold-highlighted phrase, italic honesty-caveat block, memory tag, Copy/Retry/Regenerate/branch controls, click-to-expand shielding trigger
  4. Assistant "Refused — evidence floor" — **oxblood2 fill, white text**, headline + body + Accept-as-recorded / Narrow-the-objective / Lower-the-standard actions
  5. Assistant "Refused — entitlement" — same fill; single action Request an access review
  6. Assistant generic — sage border, plain text, optional "Open [doc] →" button
- **Composer**: multiline textarea; model-picker pill (grouped menu — Claude-family tiers grouped by vendor, each noting licence e.g. "Gateway-only — routed through Akki, never resold"); Auto-shield / Always-shield segmented toggle; "Think harder" toggle; "+ Create document from this chat"; Send.
- **Audit Trail panel**: collapses to 40px rail with sage dot; expanded has per-turn label, SHIELDED summary card, three lenses:
  - **Overview** — exposure-reduction % + dilution % as two large sage stats, Purpose/Audit ID/Receipt mono block, custody/context lines, italic closing note.
  - **Reasoning** — reasoning-unit list as individual cards.
  - **Raw trail** — dark mono pre-formatted trace block.
- **Shield Intelligence Report modal** (see §16.3 below): classification badge, stacked confidentiality-band bar, 3-column category-breakdown grid (PII / BII / Locations / Phone / Card / Other — each expandable to literal found values + substitution token), de-identification method line ("Regex + Presidio NER + selective LLM pipeline"), redacted-count / model-calls-shielded stat pair, models-used list, full append-only audit log; footer button "Export as JSON".
- **Content source constants** [v8-Docx:§6.1 line 172]: `seedConversations()` (11 sample conversations), `AKKI_SCRIPT` (regex-matched canned answers), factories `mkAnswered()` / `evidenceMsg()` / `entitlementMsg()` / `genericMsg()`.

### 6.2 Data Suite (Analyze) [v8-Docx:§6.2 lines 173–182]

- Left rail (collapsible to 38px icon strip): "+ New analysis" / "Pull data", working-files list.
- Tabs: **Rapid, Deep Dive, Sources, Export**.
- Rapid: feed of short finding cards (text + optional tag + timestamp) accumulating as user asks.
- Deep Dive: loading checklist + progress bar → synthesis viewer paging through slides built from flexible layout kit (stats row, numbered rows, horizontal bars, axis-labelled bar chart, 3-column cards, left/right "pairs"), plus citation chips and "Ask about any slide, figure or claim" mini-chat.
- Sources: uploaded-file list (removable), checklist of estate sources, refresh-history log.
- Export: receipt-style summary + DOCX/PPTX/PDF format chooser + "Finish & Export" (routes into the same conversational export wizard used by Documents).
- Right rail: "Ask your data anything" contextual chat.
- "New analysis" opens full-screen intake: attach from device / document journal / named work-file, name the scenario.

### 6.3 Documents [v8-Docx:§6.3 lines 183–192]

- Left rail (collapsible): + Create New / Enhance / Compile buttons, search box, category filter chips.
- Overview (no doc open): headline + subline, 3-stat row, two-column "Recent Drafts" + "Document Journal" (running click-to-jump activity log), mono footer.
- **Document detail drawer** (right ~24% pane), tabs:
  - **Details** — inline-editable title, meta line, objective-fit score + clarity sub-scores, recommendation checklist.
  - **Intelligence** — AI-generated summary, objective-fit/clarity panel, "Signals rising from this document" list with confidence % + quoted evidence, Open Questions list, Provenance mono block, Sources line.
  - **Questions** — threaded Q&A list (question + @mentions + nested answers + "Awaiting response" / "Respond →"), @mention-chip compose box.
  - **Related** — Same Metadata, Canonical Lineage, Explicit Attachment (search-and-attach with relationship-type picker), stubbed Content Similarity note: "Embedding-based similarity is deferred pending additional infrastructure."
- Drawer footer: Share, Download, Enhance, Use in Chat, and — if not yet committed — Commit.
- **Share flow** (3-step modal): Notice ("Send as is" vs. "Redact sensitive information") → Redact (category chips, checklist of flagged snippets each with Included toggle) → Send (recipient email list, confirm).
- **Rich-text Editor mode**: Bold/Italic/Underline/Delete toolbar, Undo/Redo, drag-and-drop "attach as reference" zone, inline AI-ask box returning a Proposed revision card (Apply / Discard) rather than silently editing.
- **Deck/slide mode**: slide viewer with Prev/Next and "+ Propose next slide (AI)", producing Accept/Reject proposal card.
- **Document classification vocabulary** (platform-wide for distribution rights): **Internal Only / Regulatory Only / Licensable** — seen as colored pills on Registry's source table and on Board 360's document "mark" tag. Apply this same 3-value vocabulary to any new document-metadata or licence field.

### 6.4 Task Manager [v8-Docx:§6.4 lines 193–199]

- **Manage Tasks**: 3 summary stat cards, task list (name, status pill, meta line, evidence-percent bar), persistent "Akki is on it" rail of autonomous follow-up log lines (tags color-coded: CHASING/NOTIFIED=brass, MILESTONE/EVIDENCE=sage, METRIC/BLOCKED=oxblood, default=blue).
- **Task workspace**: header with name/meta + large evidence-satisfied % over full-width bar; Objective (inline-editable); Work Items (each with evidence kind — A committed document / A compiled pack / Sign-off from a named person / A metric threshold — plus Mark-evidence-met or Notify-owner, blocked/stale callouts); Documents (attach/open); Open Questions (add/close); right column: Contributors (name, role, % bar — Akki always listed) + chronological Cycle Log with manual "Run a turn now".
- **Create New Task**: conversational 4-step wizard (objective → team → deadline → evidence kind) with chip quick-answers.
- **Question and Portfolio drawers** (60% width): shared side-drawers reused from Board/Exco 360 for individual open question or rolled-up entity's performance view.
- **Content constants**: `TASK_SEED` (3 fully populated examples), `makeTask()` factory, evidence kinds fixed in `EVIDENCE_KINDS` / `EVIDENCE_RESOLVES`.

---

## §7. ThinkLab (v8-Docx §7) — 4 modes

- **Purpose**: structured reasoning for hard questions, five-stage pipeline: **Frame → Name/Candidates → Challenge/Tension → Weigh → Lock-in**.
- **Four modes**:

| mode key | label | duration | shape |
|---|---|---|---|
| `clarity` | Seek Clarity | 15–20 min | Untangle a messy situation |
| `strategy` | Develop Strategy | 25–40 min | Build a defensible position |
| `hypothesis` | Test Hypothesis | 20–30 min | Stress-test a claim (**Challenge stage is scenario-based** rather than tension-based) |
| `perspective` | Get Perspectives | 15–25 min | View problem through named outside seats |

- **Session screen**: 5-dot animated stage strip → optional Material intake at Frame (upload / paste / attach-from-context) → running probe Q&A log → per-stage engine output (plain entries at Frame/Name; scenario cards with "second-order effects" line at Challenge for Hypothesis mode; confidence-tagged clusters at Weigh; at **Lock-in**: conclusion paragraph, highlighted **"Load-Bearing Set"** callout, brass-bordered **"Reflection"** list, Lock-in button, then **Export the Brief** / **Hand off to Task Manager**).
- **Right sidebar** (258px, persistent): duration + objective, fixed 2-point **"How This Reasons"** explainer (`"Challenge is not averaged"` / `"Refusal is a primitive"`), Recent Sessions list with colored state marks (`LOCKED IN`=sage ✓, `IN DEPTH`=accent, `DRAFT`=ink3, `REFUSED`=oxblood2) and Resume/Reopen control per session.
- **Content constants**: `TL_MODES` (mode metadata), `TL_FLOW` (full literal probe/frame/candidates/tension-or-scenarios/weigh/conclusion/loadBearing/reflection script per mode), `TL_SESSIONS` (recent-session seed), `TL_STAGE_LABELS`.

---

## §8. Collab (v8-Docx §8) — 1 sub-tab pattern × 4

- **Purpose**: single flat feed per sub-tab (Mentions / Emails / Projects·Tasks / HR Stuff). Simplest screen pattern.
- **Layout**: headline + subline, then vertical stack of **left-accent cards** — who + role, colored state word top-right, "where" line, ask/content line, timestamp. **Identical card shape across all four sub-tabs.**

---

## §9. Performance Management (v8-Docx §9)

### 9.1 Exco 360 [v8-Docx:§9.1 lines 210–215]

- **Purpose**: company performance tracking across Goals/Initiatives (Performance tab), emergent Signals, Akki-authored Ideas.
- **Performance tab**: status + owner dropdowns, sort dropdown, summary count chips, objective cards grouped by section — title + status pill, type chip + owner + initiative-count meta row, Target/By/Now value line. Opens 60%-width drawer: description, Target/Detail/By/Now/Reassessed field list, side-by-side Performance % + Probability % (scrub-able history slider when >1 reading), Recommended Action line, primary/secondary buttons.
- **Signals tab**: multi-dropdown filters (status/type/severity, then confidence/domain) + "Tracked only" checkbox; each card expands to Evidence bullet list, optional Cross-board context box, optional prior note, note composer, Bookmark/Resolve/Share/Note actions; paginated.
- **Ideas tab**: focus + sort dropdowns + "Bookmarked only"; each card shows "IDEA BY AKKI" tag, Storyline paragraph, Reasoning paragraph, expandable list of signals it links.
- **Right rail**: "Ask Akki about performance" contextual chat.
- Sub-tabs (`P360_SUBS`): `performance`, `signals`, `ideas`.

### 9.2 Board 360 [v8-Docx:§9.2 lines 216–222]

- **Purpose**: what has actually been submitted to the board — signals, performance, documents, questions.
- **Tabs**: Signals, Performance, Documents, Questions.
- Signals/Performance mirror Exco 360's card shape but every card cites its source submission ("Source: … →" / "Reported in: … →").
- Documents tab: filterable list of board submissions (mark/kind/status tags, note, by-line + page count + Q&A-open indicator) → detail view sharing Documents' threaded Q&A composer.
- Questions tab: standalone open questions asked of the board, each citing the submission it was asked on.
- Right rail: "Ask Akki about the board" contextual chat.

---

## §10. Build & Your Resources (v8-Docx §10)

- **Extract Data**: single CTA opening the **Extraction wizard** — conversational intake that assumes unset fields and shows its assumptions plainly before anything runs.
- **Train Models**: list of training runs, each with id, accepted/rejected status, **6-check score**, baseline note, and — if rejected — reason plus **Resubmit**; accepted runs offer **"Prepare white paper"** (auto-drafts a Documents entry from the run).
- **Build Agents**: name+purpose drawer form; **Scope field** starts as an amber "agent assumed — confirm or change" chip and becomes plain confirmed line once accepted.
- **Your Resources → Agents**: flat list (name, scope, status pill, Deploy button when eligible) driving a **4-step Deploy modal**: (1) 6 acceptance checks shown passed, (2) model-ladder rung picker, (3) scope/entitlement summary, (4) go-live confirmation.
- **Your Resources → Models**: flat list of trained + bought-in models with origin and status pill.
- **Content constants** [v8-Docx:§10 line 229]: `trainingRuns` (state), `agentsList` (state — **after Farma IQ removal in v8, contains Vendor Risk Monitor and Payroll Variance Checker**), `sixChecksView`, `rungOptions`.

---

## §11. 3rd Party Apps (v8-Docx §11)

- **New / Frequent / Connected** tabs list integrations as simple rows (name, description, connect-state label).
- **Requests** tab lists pending integration requests (name, requester, time, brass status) plus a **"+ Request a new integration"** form (name + reason textarea).

---

## §12. Manage Estate (v8-Docx §12) — 3 surfaces on Governance Surface template

### 12.1 Registry [v8-Docx:§12.1 lines 234–237]

- **Purpose**: what the estate holds and runs on — data, compute, models — read at the seam, never estimated.
- **Tabs**:
  - **Data** — Governance Surface template exactly: stats/visual/table blocks for 86.4 TB across 12 sources, chart-cut selector for language / type / rights class / condition.
  - **Compute** — same template for attached GPU cluster: capacity stats, hours-by-door/week/state chart, GPU-workflow table with door/allocation/status/progress columns.
  - **LLM** — same template for models: calls/spend/refusals-by-model chart, model table with origin/calls/status/share columns.
  - **Models** — flatter list + model-detail view showing its 6 acceptance checks.
  - **Connect** — flat connected-sources list with a rights pill.
- **"+ Connect"** opens 5-stage conversational wizard: What to connect (data source / LLM / trained model / compute) → How (method chips specific to the chosen kind) → Credentials (issue vs. receive) → Name it → Ready to connect (handshake-diagnostic block on failure, with retry/alternate options).

### 12.2 Shield (Govern) [v8-Docx:§12.2 lines 238–242]

- **Purpose**: rules in force, whether they're being followed, and how they change — **read-only everywhere except Rules Updates**.
- **Sub-tabs**: **Overview, Rule Book, Trust Center, Rules Updates, Rule Books Library** — the first four use the Governance Surface template.
- **Rule Book's "inner" full view** (via View more): category filter chips, then every rule grouped by its five categories (**System Gates / LLM Interaction / Confidential Data Management / Security / Regulatory Compliance**), each showing binding-level pill and expanding into **two-box profile** — "What it holds up" (the promise) + "What you feel" (day-to-day cost/experience) — plus facts line and gates/recommendations aside.
- **Rule Books Library**: shelf of **8 standard, ISO-27001-mapped** rulebooks with Adopted / Ready-to-adopt status; adopting one drafts its rules as ordinary rule-change proposals — same sign-off/countdown ceremony, never silent.

### 12.3 Grey Mirror [v8-Docx:§12.3 lines 243–248]

- **Purpose**: security monitoring framed as **two services on one surface** — the **Ledger** (records everything) and the **Responder** (flags, acts, asks) — meeting at one verdict.
- **Sub-tabs**: **Overview, Monitor & Detect, Response, People & Models** — Governance Surface template, with People & Models substituting a **people-shaped row list** (who / data accessed / models used / PII exposure / standing pill) and dedicated per-actor bar charts (PII exposure, data accessed, model use, downloads).
- **Deep-dive detail views** (opened via row links, not tab row): **"The copy in use"** (active decoy/quarantine session — findings list, action-by-action table) and **"Marks & baits"** (standing marks, bait-touch table).
- **"Add user / model"** opens same conversational-wizard pattern (kind → name → role/objective → declaration → bounds → rights → counter-signer → confirm) used to admit any actor; new actors default to cautious **"Forming"** standing until enough ordinary behaviour accumulates.
- **Content constants**: `GOV`, `RB_CATS` (Rule Book), `GM`, `EST_GROUPS` (tile-row summaries for both Shield + Grey Mirror), `TRUST` (Registry-side mirror of Shield content).

---

## §13. Approvals (v8-Docx §13) — 3 sub-tabs, lightest pattern

- **Purpose**: lightest screen pattern — stat row plus plain row list, **no chart or aside**.
- **Spend Requests**: 3 stats (waiting on you / over the ceiling / total this month) + row list (requester, amount, ceiling note, Waiting/Needs-2 pill).
- **Rules Updates**: 3 stats (counting down / waiting for signature / hours to effect) + row list mirroring Shield's own Rules Updates tab.
- **Model Admission**: 3 stats (in acceptance / checks passed / in service) + row list of models with acceptance state.
- **Content constant**: `APPROVALS`.

---

## §14. The Watch (v8-Docx §14) — Watch Officer role only

- **Purpose**: stricter, self-policing security console — the one app **held to a tighter rule than any other, proving itself from inside its own containment** and checked by an outside witness.
- **State tab** (`wstate`): uses the **Four-Questions template** directly (§16.1).
- **Record tab** (`wrecord`): three lanes:
  - **Noted** — "seen and let pass", the restraint record, intentionally the longest
  - **Acted** — "kept visible on purpose", the honesty record
  - **Held** — "stopped, and waiting on a person"
  - plus a **Drills toggle chip** to show/hide differently-tinted drill/test entries.
- **Under Watch tab** (`wunder`): Patterns list (each with inline sparkline of rising noted-event counts, Watch-closer / Ask-for-updated-declaration actions), "copy of the estate" (decoy/quarantine) summary block, Marked block with Request-removal action.
- **Decisions tab** (`wdecisions`): **two-sided-account cards** (What the rules say / What the watch says, side by side), required one-line decision note for ambiguous cases, per-item action buttons, closing footer sentence.
- **Content constants**: `RECORD_ROWS`, `LANE_COPY`, `PATTERNS`, `DECISIONS`, `FQ_TOPLINE.wstate` / `PAGE_TOPLINE` (aside copy).

---

## §15. Instance — People & Declarations / Ceremonies (v8-Docx §15)

**NOT in top-level NAV; mounted via `appGroup==='instance'` dynamic path** [v8-HTML:pos=1009238].

- **People & Declarations**: Add-a-person / Commission-an-agent buttons, then actor cards (name, id/type, status pill, declaration sentence or multi-line agent declaration, Walk-this link).
- **Ceremonies**: cards per rule-change in flight — title, meta (proposed/counter-signed by, dates), **5-stage pill row (Propose / Counter-sign / Wait / Applied / Re-verified)** with current stage highlighted, status line, and — while cancellable — a Cancel button.
- **Content constants**: `ACTORS`, `DECL_CHIPS`, `CEREMONIES`, `CEREMONY_STAGES`.

**Verified ACTORS seed** [v8-HTML:pos=671646]:
1. Maria Chen · Compliance Owner · Human · "Sets and counter-signs rules; reads every governance surface." · `current`
2. J. Otieno · Operator · Human · "Runs the estate day to day; may not change a rule alone." · `current`
3. A. Njeri · Watch Officer · Human · "Opens the watch record and decides what is waiting." · `current`
4. `ACT-1189` · Procurement agent · Agent · autonomous · `re-declaration requested` · has objective/capabilities/risks declaration lines.

**Verified CEREMONIES seed** [v8-HTML:pos=665703]:
1. `c1` "Widen analyst access to supplier records" · stage=2 waiting · "Effective in 22 hours — you can still cancel." · Proposed J. Otieno Aug 13 · counter-signed Maria Chen Aug 13 · `cancellable:true`
2. `c2` "Watch Officer seat for D. Okafor" · stage=1 awaiting-sign · "Waiting on a second signature before its clock starts." · Proposed Maria Chen Aug 12 · no counter-signature · `cancellable:true`
3. `c3` "Model training excludes anything marked legal-hold" · stage=4 done · "Applied Mar 14, re-verified Mar 15. Held every week since." · Proposed Maria Chen · counter-signed J. Otieno · `cancellable:false`

---

## §16. Cross-cutting overlays and shared patterns (v8-Docx §16)

### 16.1 Four-Questions block ("FourQ") [v8-Docx:§16.1 line 268]

Used for Shield's Data/Reasoning/Access underlying content **and** The Watch's State tab. Always **exactly four stacked cards, fixed order**:
1. **"What's happening"** — lead sentence.
2. **"How do we know"** — lead sentence + optional row list, each openable into a two-column claim-vs-sources panel.
3. **"What we're doing about it"** — lead sentence + (if something is waiting) a brass **"Held" box** with title/line/action buttons.
4. **"Is what we agreed being done"** — closing lead sentence with a Walk-this link.

A collapsible **"see the working"** toggle reveals raw supporting facts under any card — **including facts tagged `tone:'unmeasured'`, rendered without hiding or omitting them**.

Confirmed keys in template `isFourQ: appMode && ['datashield','reasoningshield','accessshield','wstate'].indexOf(s.appOpen)>=0` [v8-HTML:pos=1008296].

### 16.2 The Brief modal [v8-Docx:§16.2 line 270]

Reached via **"View more →"** links throughout Governance Surface template. Two-page-style read: title/sub, lead paragraph, lead2 paragraph, small facts key/value table. **One Brief exists per surface × per block** (visual vs. table) in `BRIEF_SUB`; top-level `BRIEF` object covers whole-surface highlight briefs (`gm` / `gov` / `estate` / `datashield` / `reasoningshield` / `accessshield`).

### 16.3 The Shield Intelligence Report [v8-Docx:§16.3 line 272]

Documented fully in §6.1; reusable via a **"Shield" pill** that recurs wherever a conversation, task, or performance drawer needs to show its own provenance — the Task workspace header, ThinkLab session sidebar, and Exco/Board 360 detail drawers all carry the same trigger.

### 16.4 The "Walk this" evidence drawer [v8-Docx:§16.4 line 274]

Fixed sequence of Q&A cards: What was seen / What we concluded / The rule that fired / What we did / How it ended / Who saw us do it (exact set varies slightly per walk type). Each has toggleable "working" detail line citing an ID (bait record, receipt, rule version, witness signature).

**Four walk types**: `bait` (stopped bad-actor event), `crossing` (masked data crossing + receipt), `rule` (rule + ceremony that set it), `broken` (intentionally incomplete trail — system admitting a gap rather than fabricating one).

**Content constant**: `WALKS`.

### 16.5 Exposure site map [v8-Docx:§16.5 line 277]

Drawer (from Documents' header link) tracking every place a document has physically travelled — opened, downloaded, or sent outside the estate — **distinct from Shield, which only governs what reaches a model**. 3 summary stats, travel-history row list (name, lane pill, where, tracker/form/when meta, optional oxblood risk-signal line), Download-rule choice explaining that both download forms carry an invisible tracker.

### 16.6 Toast / inline confirmations [v8-Docx:§16.6 line 279]

Many row links resolve to a lightweight toast rather than a full drawer (encoded in data as `go:'toast:<message>'`) — used for detail that doesn't warrant a dedicated screen. Any row without a dedicated walk/drawer target is a toast candidate when extending the dataset.

### 16.7 Streaming / loading states [v8-Docx:§16.7 line 281]

Two matching patterns recur for anything taking visible time:
- **Step checklist with incrementing progress bar** (Deep Dive, page-level app loads, document generation).
- **Chat "Working" card** with sequential step lines and pulsing sage dot (Chat, per-panel contextual chat).

Both read step labels from small arrays (`GEN_STEPS`, `AKKI_DEFAULT_STEPS`, per-mode loading-line arrays) rather than a single spinner — user always sees what is actually happening.

---

## §17. Content-data constant reference (v8-Docx §17 appendix)

Extend a screen by adding to its matching constant in the **existing shape** — avoid parallel data sources for content that already has one.

| constant(s) | feeds |
|---|---|
| `NAV` / `TABS` / `ROLES` / `SUB_TO_GROUP` | Navigation taxonomy (§4) |
| `GOV` | Shield's Overview / Rule Book / Trust Center / Rules Updates / Library tabs |
| `RB_CATS` | Rule Book's full grouped-by-category rule list and profiles |
| `GM` | Grey Mirror's Overview / Monitor & Detect / Response / People & Models tabs |
| `TRUST` | Registry-side mirror of Shield's Data / Reasoning / Access content |
| `EST_GROUPS` | The 4-tile filter row atop Shield and Grey Mirror |
| `APPROVALS` | Spend Requests / Rules Updates / Model Admission |
| `RULES_IN_FORCE` / `RAILS` | The Watch's short rules-in-force + non-negotiable rails list |
| `CEREMONIES` / `CEREMONY_STAGES` | Instance → Ceremonies |
| `RECORD_ROWS` / `LANE_COPY` | The Watch → Record |
| `PATTERNS` / `DECISIONS` | The Watch → Under Watch / Decisions |
| `ACTORS` / `DECL_CHIPS` | Instance → People & Declarations |
| `WALKS` | The "Walk this" evidence drawer (§16.4) |
| `BRIEF` / `BRIEF_SUB` | The Brief modal (§16.2) |
| `PAGE_TOPLINE` / `FQ_TOPLINE` | Sticky-aside headline copy for FourQ and related surfaces |
| `CONNECT_KINDS` / `CONNECT_CREDS` / `CONNECT_STAGES` / `CONNECT_CHIPS` | Registry's Connect wizard |
| `LLM_STATS` / `LLMS` / `LLM_NARRATIVE` / `LLM_CHARTS` | Registry → LLM tab |
| `COMPUTE_CHARTS` / `FLOWS` / `FLOW_NARRATIVE` | Registry → Compute tab |
| `CHARTS` | Registry → Data tab's estate-composition charts |
| `TASK_SEED` / `EVIDENCE_KINDS` / `TASK_WIZ_STAGES` | Task Manager |
| `TL_MODES` / `TL_FLOW` / `TL_SESSIONS` / `THINKLAB_MODES` | ThinkLab |
| `AKKI_SCRIPT` / `seedConversations()` / `mkAnswered()` family | Chat's canned answers and seed history |
| `WIZ` | The two generic conversational wizards (rule-book change, actor admission) |

---

## §18. Reachability inventory — the 15+ existing pod surfaces mapped into the v8 lattice

The 15 pod surfaces currently mounted at `pod_shell/frontend/src/pages/` (per DECISIONS.md Wave G Step 1 mirror-hole close · ratchet floor 2363 · commit `b714957`):

Below is the **proposed home** for each in the v8 lattice. Marked `EXTENSION-PENDING-OWNER-EYEBALL` per Wave G Step 3 discipline — the owner may re-home items after seeing this. Mapping is trivially reconfigurable via the `NAV` literal.

| # | pod surface (route) | proposed v8 lattice home | click-path from `/` (Portal) | data-fidelity | citation |
|---|---|---|---|---|---|
| 1 | `/registry` (Registry Overview) | `admin` tab → `estate` group → `estate` item ("Registry") | Admin › Manage Estate › Registry | LIVE-DATA where present; SAMPLE elsewhere | v8-Docx:§12.1 line 234 |
| 2 | `/shield` (Data Shield) | `admin` tab → `estate` group → `govern` item ("Shield") | Admin › Manage Estate › Shield | LIVE + REFERENCE-NOT-COPY | v8-Docx:§12.2 line 238 |
| 3 | `/grey_mirror` (Grey Mirror) | `admin` tab → `estate` group → `greymirror` item ("Grey Mirror") | Admin › Manage Estate › Grey Mirror | LIVE + REFERENCE-NOT-COPY | v8-Docx:§12.3 line 243 |
| 4 | `/spend-requests` (Approvals: Spend) | `admin` tab → `approvals` group → `spendreq` item | Admin › Approvals › Spend Requests | SAMPLE (no live backend) | v8-Docx:§13 line 251 |
| 5 | `/rules-updates` (Approvals: Rules) | `admin` tab → `approvals` group → `rulesupd` item | Admin › Approvals › Rules Updates | SAMPLE | v8-Docx:§13 line 252 |
| 6 | `/model-admission` (Approvals: Model Admission) | `admin` tab → `approvals` group → `modeladmission` item | Admin › Approvals › Model Admission | SAMPLE | v8-Docx:§13 line 253 |
| 7 | `/train` (Train Models) | `build` tab → `build` group → `train` item | Build › Build Your Resources › Train Models | LIVE where GPU records exist | v8-Docx:§10 line 225 |
| 8 | `/extract` (Extract Data) | `build` tab → `build` group → `extract` item | Build › Build Your Resources › Extract Data | LIVE (DigiCow wired) | v8-Docx:§10 line 224 |
| 9 | `/build-agents` (Build Agents) | `build` tab → `build` group → `agentbuild` item | Build › Build Your Resources › Build Agents | SAMPLE | v8-Docx:§10 line 226 |
| 10 | `/your-agents` (Your Agents) | `build` tab → `buildlib` group → `youragents` item | Build › Your Resources › Agents | LIVE agentsList (Vendor Risk Monitor + Payroll Variance Checker) | v8-HTML:pos=453684 |
| 11 | `/your-models` (Your Models) | `build` tab → `buildlib` group → `yourmodels` item | Build › Your Resources › Models | LIVE where registry has models | v8-Docx:§10 line 228 |
| 12 | `/audit-trail` (Audit Trail Overview) | **NEW mapping** → `admin` tab → `estate` group → `govern` sub-tab (Governance Surface template's audit lens); alternate mapping: `admin` › new "Audit Trail" item slotted next to `greymirror` | Admin › Manage Estate › Shield › Overview (audit lens) | LIVE (CA1-001/002/003 with `partial_closure=true`; served units + `source_path` provenance) | v8-Docx:§17 (WALKS/GOV constants) — **EXTENSION-PENDING-OWNER-EYEBALL: v8 does not name a top-level "Audit Trail" item; it lives inside the Governance Surface Overview lens.** |
| 13 | `/prove` (Prove / Provenance) | `admin` tab → `estate` group → `govern` item → "Rule Book" or `wstate` (FourQ template) | Admin › Manage Estate › Shield › Rule Book (or Admin › The Watch › State for FourQ variant) | LIVE where evidence records exist | v8-Docx:§16.1 line 268; §12.2 line 239 |
| 14 | `/team` (Team / People) | Instance group (§15) → People & Declarations | Deep-linked via Instance mount (no top-level NAV slot); reachable through Ceremonies row-link "Add-a-person" | LIVE where `ACTORS` register has entries | v8-Docx:§15 line 263 |
| 15 | `/connect` (Connect Wizard) | `admin` tab → `estate` group → `estate` item → "+ Connect" launcher; alternate: `apps` tab | Admin › Manage Estate › Registry › + Connect | LIVE for DigiCow / GPU handshake | v8-Docx:§12.1 line 237 |

Additional surfaces present in repo tree (per `pod_shell/frontend/src/pages/*` listing in DECISIONS.md):
| pod surface | proposed v8 home | note |
|---|---|---|
| `/auth/*` (auth pages) | **NOT IN v8** — outside prototype scope | Retain as `pod_shell`-only chrome; not in shell nav. |
| `/master_admin/*` | Admin tab · dev-only visibility | Not surfaced in `NAV`; role-gated. |
| `/memory/*` | `work` tab → `workstudio` → `documents` (Journal) OR `apps` tab | **EXTENSION-PENDING-OWNER-EYEBALL** |
| `/trace/*` | Deep-linked from Walk-this drawer (§16.4) | Not top-level NAV. |
| `/commission_view/*` | Instance › Ceremonies deep-link | §15 mapping |

**Absence findings (v8 spec silent · pod surface exists)**:
- Auth flows — v8 says nothing about a login screen or auth chrome. Retained pod-side.
- Master-admin — v8 says nothing about master-admin surfaces. Retained pod-side (role-gated).
- `commission_view` — v8's Instance group covers this via Ceremonies; the standalone pod route may be redirected into Instance mount.
- `trace` — v8 mentions raw trace via Chat's Audit Trail panel → Raw trail lens (§6.1); no standalone `/trace` in v8.

**Absence findings (v8 spec has · pod does not yet)**:
- `workstudio`: `analyze` (Data Suite), `documents`, `tasks` — **pods do not yet mount these** (Step 3 to add stubs/redirects that at minimum reach a "coming from v8 spec" landing card).
- `thinklab`: all four modes — pods do not yet mount.
- `collab`: all four sub-tabs — pods do not yet mount.
- `monitor`: `performance` (Exco 360) + `board` (Board 360) — pods do not yet mount.
- `thirdparty`: all four sub-tabs — pods do not yet mount.
- `watch`: all four sub-tabs (`wstate` / `wrecord` / `wunder` / `wdecisions`) — pods do not yet mount as distinct routes; audit-trail Overview partially covers `wrecord` lane semantics.

Per owner ruling Wave G Step 3: **every one of the currently-mounted 15 pod surfaces must be click-reachable from `/`** via the shell. The above table plus the honest-empty landing pattern for missing groups satisfies that. Adding stub landings for missing groups is deferred to owner ruling — the "no fabricated data" rule holds unless owner explicitly supersedes.

---

## §19. Conflicts and agreements with v7 four-fixture set

**v7 four-fixture set** (per FL-P1-14 + FL-P2-11):
1. `fixtures/Akki_Prototype_v7_Design_Brief.md` — 18,791 B
2. `fixtures/reference_screenshot_transcription.md` — 10,281 B
3. `fixtures/binding_acceptance_criteria.md` — 23,018 B
4. `fixtures/screen_mockups_v7.pdf` — 195,644 B (via `screen_mockups_inventory.md`)

v7 status: `notes/prototype_inventory_v7.md` was **DECLASSIFIED as UNRELIABLE** in the ruling of 2026-08-28T~00:50Z (it described bytes that were not on disk under the `v7` fixture HTML). v8 **is** the file that inventory described.

**Conflict rule (owner ruling)**: v8 WINS all conflicts; v7 four-fixture set is companion oracle **only where v8 is silent**.

**Agreements between v8 and v7 four-fixture set** (advisory-strength):
- Nav grammar (WorkStudio · ThinkLab · Estate / Registry · Shield · Grey Mirror · Approvals · Compliance Owner · Watch Officer · Board 360 · Exco 360) — identical vocabulary in both. **v8 spec + v7 brief agree on the 9-group lattice.**
- Governance Surface template (Stats/Visual/Table + aside pattern) — described identically. Advisory-strength.
- Design tokens overlap — `--sage`, `--brass`, `--oxblood`, `--blue`, `--paper` color roles agree in semantic use. Exact hex values in v8 (§2.1) are BINDING; where v7 four-fixture set specifies different hexes, v8 wins.

**Conflicts (v8 wins)**:
- **Wordmark**: v7-v1/v7-v2 file bytes carry `"Farma IQ"` wordmark (see Wave G Step 1 halt-and-report findings 2 & 3, DECISIONS.md 2026-08-28T~00:15Z). v8 wordmark is **`RMS AI`** [v8-HTML:pos≈1655; v8-Docx:§3.1 line 85]. **v8 WINS.**
- **Fonts**: v7 four-fixture brief may reference `Instrument Sans / Newsreader / Spline Sans Mono` (v4 file-of-record header fonts). v8 stack is `Iowan Old Style / Söhne / ui-monospace` [v8-Docx:§2.2]. **v8 WINS.**
- **Paper background**: v4 token was `#F3F2E9`; v8 is `#f5f2ea` [v8-Docx:§2.1]. **v8 WINS.**
- **Deployed agents**: v7-v2 file bytes seeded `Farma IQ` as a deployed agent. v8 removes Farma IQ; seeds `Vendor Risk Monitor` (Deployed) + `Payroll Variance Checker` (Ready to deploy) [v8-HTML:pos=453684; v8-Docx:§10 line 229]. **v8 WINS.**
- **Farmer/enterprise/gov "four-doors" pattern**: v7-v1/v7-v2 file bytes render Farmer/Enterprise/Gov/HQ audience doors as the top-of-header pills (see Wave G Step 1 halt-and-report finding 3). v8 shows **Work / Build / 3rd Party Apps / Admin** as the top-of-portal tab groups [v8-Docx:§3.4 line 97; v8-HTML:TABS literal]. **v8 WINS.**

**v4 shell status**: **RESCINDED** per owner ruling. Code artifacts at `Extraction-Akki/frontend/src/design/AkkiV4Shell*` may be **REUSED as invisible implementation convenience** where v8 chrome happens to match, but v8 is the design authority and every cited element must trace to a v8 byte-range. The 6-item v4 sidebar (Connect · Registry · Use Data · Govern · Prove · Team) is **NOT the v8 lattice**; v8 uses a **4-tab × 10-group taxonomy** (see §4).

---

## §20. Provenance and repro

**All facts in this inventory trace to one of two files opened in this session:**
- `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` (sha256 `e56871d0…`)
- `fixtures/Akki_Platform_v8_Design_Spec.docx` (sha256 `d7cfd3ae…`)

**Extraction artifacts (all under `notes/wave_g_step0_v8/`)**:
- `_hashes.json` — structured hash summary for the four bundler payloads
- `v8_template.html` — raw JSON-encoded template (sha256 `47381de6…`, 1,152,815 B)
- `v8_template_decoded.html` — JSON-decoded template (sha256 `9177c2b9…`, 1,111,498 B) — **the file all `v8-HTML:pos=N` citations index into**
- `v8_design_spec.txt` — docx-extracted paragraph+table text (39,635 B, 312 lines) — **the file all `v8-Docx:§N line M` citations index into**
- `8d5cc57e-…application_javascript`, `0f495aa5-…text_javascript`, `a27c8ca4-…text_javascript`, `373c1b27-…text_javascript` — the four decoded bundler payloads (dc-runtime county-map · dc-runtime main bundle · react-dom · react)

**Repro command**: rerun the extraction with the identical logic captured in `phase0/drill_receipts/20260828T041500Z_wave_g_step0_v8_identity_verification.log` — the receipt file lists every hash and every extraction step.

---

**End of v8 inventory. Next step: Wave G Step 2 — port a v8-fidelity shell to `pod_shell/` (byte-identical spine mirror maintained), then Step 3 wire the 15 pod surfaces into the lattice per §18 above, Step 4 real data everywhere held, Step 5 double-green close.**
