# Prototype Inventory — Chunk 1

Source: `/app/assessment_workspace/prototype/prototype.html`
(the "Akki Prototype v6 Standalone" file). This is a single-page bundle that
loads an inline React-like application (all JS inline; no external routes).

The prototype does NOT expose classical URL routes; navigation is via internal
`s.navSub` state (a "screen key") plus `s.navGroup` (a "pillar/group key"),
selected from the constants `NAV`, `TABS`, `SUB_TO_GROUP`, and `GROUP_TO_TAB`.
All facts below come from inspecting the file directly (not from a README or
description).

## 1. Navigation constants — the ground truth

Extracted verbatim from the `const NAV = [...]` declaration inside the bundle
(byte offset ~388,780 of `prototype.html`):

### 1.1 Top tabs (`const TABS`)

| tab key | label | groups | right-aligned |
|---|---|---|---|
| `work` | Work | workstudio, thinklab, collab, monitor | no |
| `build` | Build | build | no |
| `apps` | 3rd Party Apps | (empty in TABS) | no |
| `admin` | Admin | trust, registry | **yes** |

### 1.2 Nav groups (`const NAV`) and their items

Eight groups. All 38 nav-item keys listed inline.

| group `key` | group `label` | item `key` → `label` |
|---|---|---|
| `workstudio` | WorkStudio | `chat` → Chat · `analyze` → Analyze · `documents` → Documents · `tasks` → Task Manager |
| `thinklab` | ThinkLab | `clarity` → Seek Clarity · `strategy` → Develop Strategy · `hypothesis` → Simulate a Hypothesis · `perspective` → Get Perspective |
| `collab` | Collab | `mentions` → Mentions · `emails` → Emails · `projects` → Projects/Tasks · `hrstuff` → HR Stuff |
| `monitor` | Monitor | `performance` → Performance · `signals` → Signals · `ideas` → Ideas by Akki |
| `trust` | Trust Center | `rules` → Manage Rules · `datashield` → Data Shield · `reasoningshield` → Reasoning Shield · `accessshield` → Access Shield |
| `registry` | Registry | `estate` → Data Estate · `models` → Models · `compute` → Compute · `connect` → Connect |
| `build` | Build | `train` → Train Models · `agentbuild` → Build Agents · `extract` → Extract Data · `youragents` → Your Agents |
| `thirdparty` | 3rd Party Apps | `appsnew` → New · `appsfrequent` → Frequent · `appsconnected` → Connected · `appsrequests` → Requests |

Totals: **8 groups**, **32 nav items** (the 4×8 grid above). Plus:

- `SESSION_TOOLS` (a per-tool "open session" set): `chat, analyze, documents, tasks, clarity, strategy, hypothesis, perspective` — 8 keys.
- `RESTRICTED` set (rendered under the sage/green colour token per the bundle logic): `hrstuff, datashield, reasoningshield, accessshield` — 4 keys.
- `GROUP_TO_TAB` maps every group into one of the four top tabs above.

### 1.3 Screen inventory (one row per screen key encountered)

| key | label | pillar/group | tab | notes |
|---|---|---|---|---|
| chat | Chat | workstudio | work | reference-app-style Ask surface; conversations, model menu, Data-Shield report per conversation |
| analyze | Analyze | workstudio | work | multi-source analysis; "Rapid vs Deep Dive"; source history log |
| documents | Documents | workstudio | work | wizard-driven document/deck generation; commit/superseded/uploaded states; a proposal-editor overlay |
| tasks | Task Manager | workstudio | work | tasks manage/drawer; distinct from a commissioned objective |
| clarity | Seek Clarity | thinklab | work | TL_FLOW step chain (probes, frame, candidates, tension, weigh, conclusion, load-bearing, reflection) |
| strategy | Develop Strategy | thinklab | work | same TL_FLOW pattern |
| hypothesis | Simulate a Hypothesis | thinklab | work | same TL_FLOW pattern |
| perspective | Get Perspective | thinklab | work | same TL_FLOW pattern |
| mentions | Mentions | collab | work | thread-carrying notifications |
| emails | Emails | collab | work | governed threads read inside the shield |
| projects | Projects/Tasks | collab | work | tasks grouped by other people on them |
| hrstuff | HR Stuff | collab | work | **restricted**; aggregate-only |
| performance | Performance | monitor | work | performance drawer / drilldown |
| signals | Signals | monitor | work | signal feed |
| ideas | Ideas by Akki | monitor | work | idea drawer / proposals |
| rules | Manage Rules | trust | admin | rulesView; rule-change flow |
| datashield | Data Shield | trust | admin | **restricted** |
| reasoningshield | Reasoning Shield | trust | admin | **restricted** |
| accessshield | Access Shield | trust | admin | **restricted** |
| estate | Data Estate | registry | admin | registry / estate |
| models | Models | registry | admin | modelDetail drawer |
| compute | Compute | registry | admin | (present; content not enumerated further) |
| connect | Connect | registry | admin | connector registration |
| train | Train Models | build | build | training surface |
| agentbuild | Build Agents | build | build | agent wizard |
| extract | Extract Data | build | build | extract wizard (portfolio drawer, sig note, deploy screens) |
| youragents | Your Agents | build | build | agent inventory |
| appsnew | New | thirdparty | apps | filter of APPS by `isNew` |
| appsfrequent | Frequent | thirdparty | apps | filter of APPS by `isFrequent` |
| appsconnected | Connected | thirdparty | apps | filter of APPS by `isConnected` |
| appsrequests | Requests | thirdparty | apps | (no filter key; renders requests) |

The APP inventory the bundle ships:
Slack Connector · Salesforce Sync · Tableau Feed · Jira Bridge · DocuSign Bridge.

## 2. Component fabric

Detected via regex over `this.<name>` method definitions and `open<Name>` handlers:

- **View-generator methods**: `akkiConversationsView`, `akkiMessagesView`, `akkiArchivedView`, `rulesView` (all found once each in the bundle — the app is largely rendered from a monolithic `render()` that assembles view fragments from state).
- **Open/drawer handlers**: `openDocWiz` (×8), `openDocDrawer` (×4), `openPerfDrawer` (×3), `openQuestionDrawer` (×2), `openShareAs` (×2), `openModelDetail` (×2), `openExtractWizard`, `openAgentWizard`, `openExistingDoc`, `openRuleChange`, `openTaskWorkspace`, `openPortfolioDrawer`, `openSigNote`, `openDeploy`.
- **State constants pulled out of the bundle**:
    - `EVIDENCE_KINDS = ['A committed document','A compiled pack','Sign-off from a named person','A metric threshold']` — plus an `EVIDENCE_RESOLVES` map to resolution phrasing.
    - `DOC_GEN_LABELS` (referenced from the state seed `docGenLabels`).
    - `LANDING_TIPS` — per-screen-key tips shown on the landing panel for `chat, analyze, documents, tasks, mentions, emails, projects, hrstuff, …` (partial — full map in the file).
    - `TL_FLOW` — ThinkLab step content for `clarity` (probes, frame, candidates, tension, weigh, conclusion, loadBearing, reflection); parallel entries expected for `strategy, hypothesis, perspective`.
    - `NAV`, `TABS`, `SUB_TO_GROUP`, `GROUP_TO_TAB`, `SESSION_TOOLS`, `RESTRICTED`, `APPS` — the navigation lattice.
- **Chat feature surface** (found in state): `akkiConversations, akkiModel, akkiComposerText, shieldReportOpen, shieldBandRows [Public/Internal/Confidential/Restricted], shieldedItems [PII/BII], shieldItemsView` — the Data-Shield report is rendered per conversation, itemising redacted tokens.
- **Document wizard state (`docWiz`)**: `open, path, stageIdx, messages, answers, input, sourceMode ('upload'|other), sourceQuery, selected, editingKey, editValue`.
- **Document editor state**: `docEditorText, docUndoStack, docRedoStack, docAttachedFile, docAskOpen, docAskText, docAskImage, docProposalOpen, docProposalAfter`.
- **Deck state**: `deckSlides, deckActiveSlide, deckProposedSlide, deckProposedTitle, deckProposedBody`.
- **Task state**: `taskTab ('manage'|...), taskDrawerId, taskOpenId`.
- **Work-Studio objective state**: `wsObjEditing, wsObjDraft, wsNewItem, wsNewItemEvidence (∈EVIDENCE_KINDS), wsNewQuestion`.

## 3. Cross-check against Canon 5 — obvious gaps

Purely inventory + naming comparison. Full Canon-5 conformance scoring is Chunk-3 work.

### 3.1 Canon 5 surfaces the prototype **exposes** (by name / by function)

- Canon 5 §12.1 "Registry Dashboard" ↔ prototype `estate` (Registry > Data Estate).
- Canon 5 §29 "Register an Application" / §26 "Administer" ↔ prototype `appsnew / appsfrequent / appsconnected / appsrequests` (third-party surface) — though the prototype exposes it as a browsable app catalogue rather than as an admin console with key-issuance.
- Canon 5 §14 "Commission — Shaping Wizard" ↔ prototype `extract` (Build > Extract Data), via `openExtractWizard`.
- Canon 5 §36 "The Reference Application (Ask)" ↔ prototype `chat` (WorkStudio > Chat).
- Canon 5 §23 "Compliance Rulebook" ↔ prototype `rules` (Trust Center > Manage Rules).
- Canon 5 §17 "Registry Administration" and Doc 6 §3 source connectors ↔ prototype `connect` (Registry > Connect).
- Canon 5 §34-A "The Watch Console" — the prototype has NO surface labelled "Watch"; the Trust-Center `datashield / reasoningshield / accessshield` marked *restricted* are the closest analogues, but Canon 5 §34-A specifies four panels (State / Record / Under-Watch / Decisions) that are not present under those labels.
- Canon 5 §41 "Control band" (Connect, Estate Map, Rulebook, Access, Watch) — the prototype's admin tab groups these under `trust` + `registry`, but does not present them as a horizontal control band.

### 3.2 Prototype-exposed surfaces that Canon 5 **does not name**

- `WorkStudio` as a top-level pillar name (Canon 5 §40 uses "Work" as a pillar containing Chat, Analyze, Documents — and NEVER uses the name "WorkStudio").
- `Analyze`, `Documents`, `Task Manager` under WorkStudio — the labels for the first two appear in Canon 5 §40 as the "Work" pillar, but Task Manager does not.
- `ThinkLab` — Canon 5 §40 lists ThinkLab under the "Lead" pillar. The prototype omits the "Lead" pillar label entirely and elevates ThinkLab to a top-level group.
- `ThinkLab > Seek Clarity / Develop Strategy / Simulate a Hypothesis / Get Perspective` — none of these four sub-tools appear as named surfaces in Canon 5.
- `Collab` — Canon 5 §40 does not list a Collab pillar or its four children (Mentions, Emails, Projects/Tasks, HR Stuff).
- `Monitor > Performance / Signals / Ideas by Akki` — Canon 5 §40 lists Monitor under Lead but does not enumerate these three children (Ideas is designated as Canon 5 §19 "Opportunity Briefs" — labelling is different).
- `Trust Center > Data Shield / Reasoning Shield / Access Shield` — Canon 5's Compliance Console (Doc 5 Part V) has different sub-organisation (Home, Prove-one-run, Retention & Rights, Compliance Rulebook). No "Shield" nomenclature appears in Canon 5 for these compliance sub-surfaces.
- `Registry > Models / Compute` — Canon 5's Extraction Console has Registry Administration (§17), Quality Observation (§18), Opportunity Briefs (§19). It does not enumerate Models or Compute as separate sub-screens on any console.
- `Build > Train Models / Build Agents / Extract Data / Your Agents` — Canon 5 §40 lists Train, Studio, Extract as the Build pillar. `Build Agents` and `Your Agents` roughly correspond to Canon 5's "Studio" (§40, §42 designated as *Designed*, not sourced). The prototype uses different labels.
- `3rd Party Apps > New / Frequent / Connected / Requests` — Canon 5 §24–27 (Integration Console) is different in shape (Register / First call / Administer / Dual-Actor Scoping).

### 3.3 Canon 5 surfaces the prototype **omits**

- The five **consoles** as first-class surfaces named as such (Extraction, Compliance, Integration, Administration, Watch — Canon 5 §10). The prototype presents no surface labelled "Extraction Console", "Compliance Console", etc. Their capabilities are scattered across WorkStudio/Registry/Trust/Build.
- **Administration Console** in its Canon-5 shape (§29–34): Home with binding banner "Two rules are waiting…", Change-a-Rule flow, What-I've-Changed, Roles & Rights, Counter-Sign Duties. The prototype's `rules` screen partly overlaps but is not the full six-button Administration Home.
- **Watch Console** as specified in Canon 5 §34-A: four panels State / Record / Under-Watch / Decisions with the constitutional negative-space rules (no thresholds, no mark placement, no profile internals, no mirage construction). The prototype exposes no such console.
- **Reference Application "Ask" three lenses** (Canon 5 §37.1 Answer / Reasoning / Raw trail): the prototype's Chat surface renders conversations and a per-conversation Data-Shield report but does not present three progressive-disclosure lenses that read one object.
- **Refusal card** components per Canon 5 §9.2 (fixed copy "Not to the standard you asked for" · "Accept as recorded statement · Narrow the objective · Lower the standard" · "A refusal is the system keeping its promise") — no verbatim occurrence found in the bundle by string search.
- **Agent-assumed chip** (Canon 5 §9.3) — no matching amber-chip pattern found by string search.
- **The Five Pillars + Control Band** (Canon 5 §40 — Lead / Work / Build / 3rd Party / Learn over Connect · Estate Map · Rulebook · Access · Watch). The prototype has no "Lead" pillar and no "Learn" pillar; Control-band items are dispersed across Registry + Trust Center.
- **News, Pulse** (Canon 5 §40 Lead-pillar applications). Not present under any name.
- **Studio** (Canon 5 §40 Build-pillar) — the prototype has `Build > Build Agents` and `Your Agents` which cover part of the intent but do not use the Studio label.
- **Learn pillar** entirely (Canon 5 §40).
- **Grounding markers / class chips inline with claims** (Canon 5 §2.2 "Class with claim") — the DataShield conversation report shows PII/BII redaction bands and per-item locations, but there is no explicit rendering of a defensibility class chip adjacent to a claim.

### 3.4 Restricted / dormant capabilities

The prototype's four `RESTRICTED` keys (`hrstuff, datashield, reasoningshield, accessshield`) are rendered under the sage/green token per the bundle logic. Canon 5 §9.4 "Dormant capability" says such a state must be visible and named, with what would activate it — the prototype partially honours this by keeping them in nav rather than hiding them, but the "what would activate them" statement per screen is not observable from the bundle constants without running the app.

## 4. Compact summary

- **8 groups, 32 nav items, 4 top tabs.**
- **Reference App equivalent** = `chat` (WorkStudio > Chat).
- **Extraction wizard equivalent** = `extract` (Build > Extract Data) via `openExtractWizard`.
- **Trust Center equivalent** = `trust` (Manage Rules + 3 restricted shield sub-surfaces).
- **Registry Dashboard equivalent** = `estate` (Registry > Data Estate).
- **Watch Console equivalent** = **NONE observable**.
- The prototype uses a taxonomy (WorkStudio · ThinkLab · Collab · Monitor · Trust · Registry · Build · 3rd Party) that is **substantially different** from Canon 5 §40's taxonomy (Lead · Work · Build · 3rd Party · Learn + Control band). Chunk-3 will need to map both taxonomies onto Canon 5's service-sentences (Doc 1 §12) before assigning REUSE / MODIFY / RE-POINT / BUILD / RETIRE.
