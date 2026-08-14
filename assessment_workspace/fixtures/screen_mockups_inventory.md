# screen_mockups_inventory.md - Akki Prototype v7 Registry brief inventory

## Fixture reception

- **File:** `fixtures/screen_mockups_v7.pdf`
- **Received:** 2026-08-14 (owner fixture drop, this cycle)
- **Source URL:** https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/zx1ezrxr_Screen%20mockups.PDF
- **sha256:** `418ad0e3c087c613be7d7d885a18a3c895b7d51ed253119aff9ba042ee81da8a`
- **Size:** 195,644 bytes
- **PDF metadata:** Creator = mobile Chrome (Android 10), Producer = Skia/PDF m151, Title = "Screen mockups", CreationDate = 2026-08-14T17:38:44Z, ModDate identical.

## Discrepancy against owner claim (recorded, not silently reconciled)

- Owner said "19 pages" — actual page count is **5**.
- Owner said "plus 4 inline screenshots of the Registry surface and Connect wizard" — those screenshots are NOT embedded in the PDF (PDF contains ZERO images, pure text) and were NOT attached as separate job assets accessible to this session.
- Content matches the Akki Estate group's Registry feature-and-component brief — a written specification of the surface pattern, tabs, components, Connect wizard grammar, content rules, states, and open questions. It is NOT a visual mockup deck.
- Owner's inline textual description of the 4 screenshots stands as the visual reference for Registry surface header/tabs/tiles and the Connect wizard's opening screen; the PDF stands as the written spec/rules.

## Page-by-page inventory

### Page 1 - Registry (Purpose + The page pattern)

**Eyebrow:** `AKKI · ESTATE · FEATURE & COMPONENT BRIEF`
**Title:** `Registry`
**Deck:** "The surface that answers three questions about the instance: what data you hold, what compute is connected to it, and which models are answering on it. Read-only by design, with one write path - Connect."
**Version note:** "Version 7 · prototype reference: Akki Prototype v7.dc.html · Estate group"

#### 1. Purpose and scope

- Registry is the instance's inventory. Every figure is a measurement taken at the seam, never an estimate; every figure traces to a census.
- Answers "what do we actually have?" for three classes: data, compute, models.
- Only page in the Estate group that admits new assets.
- **In scope:** holdings, composition, condition, rights class, extraction progress, cluster capacity and utilisation, GPU workflow status, connected LLMs and locally trained models, acceptance state, spend and call volumes, and the connection journey for anything new.
- **Out of scope:** rule-making and enforcement (Govern), watch and security posture (Grey Mirror, The Watch), model training runs and agent construction (Build), anything that changes a rule.

#### 2. The page pattern

Two-column: LEFT (fluid) | RIGHT (300px).
- **Topline row:** section title, one-liner, 3x3 stat grid | Headliner panel (editorial deck).
- Full-width divider.
- **Visual row:** section title, dataset dropdown, one-liner, bar chart | Context panel.
- Full-width divider.
- **Table row:** section title, filter chips, one-liner, table, "view the full record" link | Context panel.

**Rules across every instance of the pattern:**
1. Right column always speaks to the block beside it; vertically centred so the relationship reads without a label.
2. Headliner sits on the same plane as the topline, same shape and type on every page.
3. Every section title carries a one-line intro to the thing below it.
4. Dividers cut full width across both columns.
5. Unmeasured shares are drawn with the same weight as measured ones - hatched, labelled "not yet measured", never omitted.

### Page 2 - Tabs (Data Connected, Compute Connected, LLMs & Trained Models)

#### 3.1 Data Connected
- Intro: "The estate as last read by the census."
- **Topline (9):** held in total, sources connected, share measured, data types present, languages observed, share already verified, share carrying PII, licensed for external use, not yet measured.
- **Headliner:** holdings sentence with measured figures ruled; one editorial phrase in crimson; census provenance line with run time + link to how the estate is measured.
- **Visual:** composition by language / data type / rights class / condition.
- **Table:** source, size, rights pill, extracted %, meta line (type, languages, condition, measurement date).
- **Right panels:** "Reading the mix" beside chart; "What your data can do" (opportunity list) beside table.

#### 3.2 Compute Connected
- Intro: "What hardware is attached and what it is carrying."
- **Topline (9):** clusters attached, GPUs, capacity this month, committed to work, free to allocate, jobs waiting, workflows this month, utilisation, runs receipted.
- **Visual:** hours by door / by week / by state.
- **Table:** GPU workflows - workflow, door, allocation, status pill, progress; filtered All / Ongoing / Complete / Failed; five rows; narrative changes per filter.
- **Right panels:** headliner beside topline; "Reading the load" beside chart; "The connection" (attachment date, location, interconnect, access, runtime, last measured) beside workflow table.

#### 3.3 LLMs & Trained Models
- Intro: "Bought-in models and models trained here, on one record."
- **Topline (9):** models connected, calls this month, refused at the shield, median answer time, spend, context masked, acceptance checks, models retired, drift testing (not yet measured).
- **Visual:** calls by model / spend by model / refusals by reason.

### Page 3 - LLM table + Components + Connect intro

#### 3.3 LLMs & Trained Models (continued)
- **Table:** model, origin (bought-in vs trained here), calls, status pill (in service / evaluating / retired), share; filters All / In service / Evaluating / Retired. **Retired models keep their row.**
- **Right panels:** headliner; "Reading the mix"; "How a model enters, and leaves" (six acceptance checks, re-run on cadence; failure removes it the same day).

#### 4. Components (behaviour and rules)

| Component | Behaviour and rules |
|---|---|
| **Tab bar** | Three uppercase tabs, 2px active underline, with the + Connect button pushed right on the same plane. Tab state resets its tab's chart and filter selections. |
| **Stat grid** | Always 3x3. Each cell: uppercase label, serif value, one-line note. Any unmeasurable cell reads "Not yet measured" rather than being dropped. |
| **Headliner panel** | 24px serif deck, vertically centred against the stat grid. Measured figures get a thin neutral rule; exactly one editorial phrase per deck is crimson. Sub-line carries provenance. |
| **Chart block** | Horizontal bars: label, track, value. Dataset switched by a native select. Hatched fill for unmeasured. Caption states the denominator. |
| **Filter chips** | One row, right-aligned to section title. Active chip is navy. Filtering also swaps the narrative line under the table. |
| **Record table** | Four or five columns max, plus a meta line per row so the table survives the narrowed column. Capped at five rows with a "view the full record" link. |
| **Context panel** | Uppercase title, 2-3 sentences of interpretation, optionally a short list. Never repeats the sentence already on screen; it says what the numbers mean. |
| **Announcement row** | A newly connected asset appears at the top of its tab's table with a sage "Just connected" pill and the meta "not yet measured". |

#### 5. Connect - the one write path (intro)

"A right-hand drawer holding a conversation, not a form. Akki asks; the operator answers in their own words or taps a suggestion chip. The drawer assumes no universal shape: the questions branch on what is being connected, and the outcome is not assumed to succeed."

- **Step 1. What:** a data source, an LLM, a trained model, or compute. Free text is interpreted; an unreadable answer is asked again rather than guessed.

### Page 4 - Connect steps 2-5 + Content rules + States and edges

#### 5. Connect (continued)

- **Step 2. How:** methods differ by kind - private link, on-premise mount, scheduled batch; in-seam hosted, on-premise weights, sandbox only; registry or imported weights; on-premise or co-located cluster.
- **Step 3. Credentials:** issued by the operator, or minted by Akki and recorded against whoever takes them.
- **Step 4. Name:** nothing connects unnamed.
- **Step 5. Attempt:** a summary, then a real attempt.

**Failure is a first-class outcome.** Failed attempt shows the handshake step by step - route, TLS, credentials, read - with the failing step in crimson and the untried step greyed, and states plainly that nothing crossed and nothing was written. The conversation continues: retry as-is, change the credentials arrangement, switch the method, or ask for the handshake log. Attempts are numbered.

**Success ends the conversation:** "Connection successful"; the asset is announced in its tab; the drawer offers a single Close; a toast names where it landed. The new asset is unmeasured until the next census and is drawn that way.

#### 6. Content rules

1. **Sentences first, measures second.** Every block leads with a plain sentence; numbers sit behind it or beneath it.
2. **No figure without provenance.** Each tab states what it was measured against and when.
3. **Gaps are drawn.** "Not yet measured" is a value, never an omission or a zero.
4. **Refusals and failures** are reported as work done, not work lost.
5. **One emphasis per deck.** Everything cannot be important.
6. **Read-only means read-only:** no control on this page changes a rule, and the page says so where it matters.

#### 7. States and edges

- **Empty tab:** a tab with nothing connected still shows its topline with zeroes and an unmeasured note, plus the Connect prompt.
- **Stale census:** when the census is older than its cadence, the provenance line carries the age and the estate figures stay as last measured.
- **Failed workflow:** a run that hits its ceiling halts; nothing past the ceiling is billed and the halt keeps its row.
- **Retired model:** row retained, status greyed, share zero.
- **Role scope:** Registry is visible to the Compliance Owner and Operator. A Watch Officer sees the Watch group instead.
- **Narrow viewport:** nested grids collapse before the content column does; tables reflow to their meta line rather than shrinking type.

### Page 5 - Open questions

1. Should "view the full record" open a full-page record view, or a drawer with the same table unfiltered?
2. Does an opportunity in "What your data can do" link into Build, and does that carry the measurement with it?
3. Who may run a census, and should Registry expose a "run census" action or leave it to Ceremonies?
4. Drift testing is currently unmeasured on the models tab - what would make it measurable, and who owns the cadence?

## Owner's inline description of the 4 screenshots (verbatim record)

Owner's text: **"To resolve the back and forth - attached is screenshots of registry and connect wizard."**

Owner's own reading (owner's words, quoted for record):

> (a) Registry surface, title "Registry · ESTATE" with Back button, THREE TABS: "DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS", a "+ Connect" navy button top-right, stat-card grids with plain-sentence sublabels ("drawn, never left blank", "no path out skips the mask"), a right rail with small-caps eyebrow ("WHAT IS ANSWERING" / "WHAT YOU HOLD" / "WHAT IS CONNECTED") + large serif plain-sentence narrative with key figures underlined/red, horizontal bar charts with a "by ..." cut selector, and record tables (models with IN SERVICE/EVALUATING/RETIRED status chips; cluster workflows with doors Train/Extract/Export/Measure/Prove; estate sources with rights chips). Header: dark navy bar, org name left ("Acme Holdings AI" - DEMO org), right-side ROLE SWITCHER: "Compliance Owner · Watch Officer · Operator" + user chip.
>
> (b) The "+ Connect" opens "Connect something new - A conversation, not a form": a chat-style wizard with an opening prompt ("What would you like to connect? Tell me in your own words - a data source, a model, or compute...") + four quick chips (A data source · An LLM · A trained model · Compute) + free-text input + Send.

## Cross-reference: owner-claim → PDF-section

| Owner claim | PDF section |
|---|---|
| Three tabs "DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS" | §3, §3.1, §3.2, §3.3 |
| "+ Connect" navy button top-right pushed to right of tab bar | §4 Components -> "Tab bar" row |
| Right rail small-caps eyebrow + serif plain-sentence narrative | §2 The page pattern -> Headliner + Context panels |
| Horizontal bar charts with "by ..." cut selector | §4 Components -> "Chart block" |
| Record tables with status chips, meta lines | §4 Components -> "Record table" |
| Role switcher (Compliance Owner · Watch Officer · Operator) | §7 States and edges -> "Role scope" |
| Wizard "A conversation, not a form" with 4 quick chips | §5 Connect - Steps 1-5 |
| Failure grammar (handshake step by step, crimson failing step, greyed untried) | §5 Failure paragraph |
| Success grammar ("Connection successful" + single Close + toast) | §5 Success paragraph |
| "not yet measured" gap rule | §6 Content rule 3 |
| Read-only surface with one write path | §1 + §6 Content rule 6 |
| DEMO org "Acme Holdings AI" figures illustrative only | Not in PDF; per owner: rendered as honest current state instead. |
