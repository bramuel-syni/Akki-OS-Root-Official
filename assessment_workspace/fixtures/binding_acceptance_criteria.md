# binding_acceptance_criteria.md

**Sources (both delivered 2026-08-14):**
- `Akki_Prototype_v7_Design_Brief.md` — sha256 `063f2b470d74dcd30ad43b4645c4e656edaa7fb1185198a4116ad5328a9717b4` · 150 lines · owner-authored governing document (interface fixture).
- `reference_screenshot_transcription.md` — sha256 `d3ae9a6cf598a38333b5c11d6d73dc9069dc3671fb31598f2e594dfb002fc949` · owner-inline transcription of the Admin-surface reference screenshot · grade AUTHORITATIVE-UNTIL-FILE-ARRIVES (owner Q1(c) ruling · 2026-08-14).

**Purpose.** These are the binding acceptance criteria every interface item across BUILD_STRATEGY.md now inherits (Build Order 01 §3: *"The interface fixture is binding, not illustrative"*). Every criterion below appears in an item's Definition of Done as a specific must-hold statement, plus in its NEW-INVARIANTS-TO-WRITE-FIRST list where it's mechanically checkable.

---

## BAC-1 · Rule zero — the four-question topline (Brief §2 rule zero, screenshot E-2)

**Statement (verbatim from Brief §2):** *"Every surface leads with plain sentences answering, in order: What's happening? How do we know? What are we doing about it? Is what we agreed being done?"*

**Mechanical rendering slots (from screenshot E-2):**
- Q1 (What's happening) → detail-card LEDE (plain sentence in grey sans, under the serif display title).
- Q2 (How do we know) → detail-card `LAST ACTIVITY` block (bold plain sentence + `Name, Role · Date` attribution).
- Q3 (What are we doing) → detail-card FOOTER row (primary dark-navy button + secondary outlined button).
- Q4 (Is the agreement holding) → detail-card `TIPS` bulleted sentence stating the rail's read-only status.

**Engineering-measure exclusion (Brief §2, rule zero paragraph):** *"Engineering measures — p95 latencies, budget percentages, parameter codes, signal-class names — never render on an officer's surface; they live one tap behind the sentence ('see the working') and in the builder-facing drill view only."*

**New invariant added to every console item's must-write-first list:**
- `test_four_questions_topline_present` — asserts a detail-card render (any console) has all four slots populated with plain sentences and no engineering measure appears in Q1..Q4 rendering.
- `test_engineering_measures_behind_see_the_working` — asserts p95/latency/percentage/parameter/signal-class strings render only under a "see the working" (or equivalent one-tap-behind) affordance, never at Q1..Q4 slot level.

**Read-aloud test (Brief §2):** *"if a screen cannot be read aloud to a colleague and understood first pass, it fails this rule."* This becomes DoD language on every console item.

**Register:** Brief §2 fixes *"The Extraction frontend's simplified language is the register to match."* DoD copy pass compares against Extraction-Akki frontend register — no drift.

---

## BAC-2 · Palette + type (Brief §2.1, screenshot E-1)

- **Canvas:** warm cream page background.
- **Cards:** white for detail card + selected tile card; unselected tiles = flat cream cards with subtle border.
- **Primary text / actions / active pill:** dark navy.
- **Icon accent (selected tile only):** lavender rounded-square icon chip.
- **Serif faces:** display titles inside detail cards only ("Manage Rules" pattern).
- **Sans-serif:** body, group labels (small-caps letterspaced grey), attribution lines, buttons, tips.
- **Oxblood** (Brief §2.1): reserved — *"appears only on refusal, hold, and severance states, never decoratively."*
- **Amber** (Brief §2 held state, Brief §5.1 countdown, Brief §8 held card): held-state card + countdown states inline.
- **Grey** (Brief §8 failed card): failed-state card, "this is ours, not yours" tone.

**Reuse rule (Brief §2.1):** *"Palette and type come from the existing tokens. Reuse v6's CSS variables and the screenshot's rendering."*

**Applies-to items:** every WS-HARVEST-* interface component item; every WS-MODIFY-CONSOLE-* item; every WS-BUILD-* Watch console item.

---

## BAC-3 · No engine names in officer view (Brief §2.2)

Verbatim: *"No internal engine names anywhere a user reads: no Mtafiti, Northena, Solva, SyniSense, Macho, Mkono, Sarabi, Doa, Sahihi, Mnara, Moshi on screen. Org language only (mapping table in §4)."*

**New invariant added to every console item:**
- `test_no_engine_names_in_officer_render` — grep-style assertion over rendered strings; must be zero hits for the eleven engine names above.

**Mapping table** (from Brief §4, encoded as a code-comment block per Brief §4 requirement and Brief §10):

| On-screen label | Canon identity |
|---|---|
| Manage Rules | The Rulebook + change ceremony (Canon 3 Part V, Canon 5 §23 = Doc-5 §23) |
| Data Shield | Boundary custody: chain, receipts, disclosure (Canon 3 §13–§20) |
| Reasoning Shield | Reasoning assurance: depth, evidence bars, traces (Canon 4 Part IV) |
| Access Shield | Entitlement + Access surface (Canon 3 §22.1, Canon 5 §41 = Doc-5 §41) |
| Data Estate | Estate Map / census & registry reading (Canon 5 control band) |
| Models / Compute / Connect | Model registry & ladder · economics/metering · integration wizard (Canon 4, Canon 7) |
| State / Record / Under Watch / Decisions | Watch Console's four panels (Canon 8 §13, Canon 5 Part VII-A) |
| People & Declarations | Admission declarations (Canon 3 §6.1) |
| Ceremonies | Change ceremony pipeline (Canon 3 §24) |

**Applies-to items:** every interface item consuming a canon-named engine's output.

---

## BAC-4 · Four response classes, no fifth (Brief §2.3, Brief §8)

*"Every action resolves visibly as: done (quiet confirmation), held (amber, with why and what happens next), refused (oxblood card, exact copy in §8), or failed (grey, 'this is ours, not yours' tone). No fifth state, no silent outcomes."*

**Verbatim copy blocks (Brief §8) — must be pasted exactly:**

- **Refusal card (oxblood):**
  - title: *"This can't cross."*
  - body: reason in plain words, one sentence.
  - line: *"What was refused, not who you are: [reason name]"*
  - actions: only ones the viewer can take (e.g., *request disclosure*, *see the rule*). *"Never 'contact administrator' alone."*
- **Held card (amber):** *"Held for [reason]. Nothing is lost — it releases or resolves by [time]."*
- **Failed card (grey):** *"Something on our side broke. Your request was valid. Retry, or leave it with us — it's recorded."*
- **Watch session banner:** *"Watch session · recorded."*
- **Reconciliation notice (ACT-0733's):** *"Between 09:12–09:52 on Aug 10 your work was held for review and did not land. It has been replayed successfully. Nothing further is needed."*

**New invariants added to WS-BUILD-REFUSAL-CARD-COPY, WS-WIRE-REFUSAL-FAMILY, and every console item that surfaces held/failed states:**
- `test_response_classes_verbatim_copy` — asserts rendered refusal/held/failed/session-banner/reconciliation strings match the Brief §8 verbatim blocks byte-for-byte.
- `test_no_fifth_response_class` — asserts no state string outside {done, held, refused, failed} reaches a rendering path.

---

## BAC-5 · Nothing renders all-green (Brief §2.4)

*"Every status surface carries at least one live imperfection: an aging item, a spent fraction of a budget, a stale calibration, an open decision. All-clear is a rendering defect."*

**New invariant on every status surface:**
- `test_status_surface_carries_imperfection` — asserts every status page renders at least one non-quiet item (`held` OR `noted` OR `aging` OR `partial` OR `open decision`). Zero-live-imperfections is a rendering defect and MUST fail this test.

**Applies-to items:** WS-BUILD-WATCH-STATE, WS-BUILD-CONSOLE-COMPLIANCE-HOME, WS-BUILD-COMMISSIONING-SURFACE, WS-MODIFY-CONSOLE-EXTRACTION-DASHBOARD.

---

## BAC-6 · Unmeasured renders honestly (Brief §2.5)

*"Anything not yet measured shows 'not yet measured' — never a dash, never zero, never omitted."*

**New invariant:**
- `test_unmeasured_renders_verbatim` — asserts any not-yet-measured field renders the exact string `not yet measured` (case-insensitive on first word only). Zero, dash, empty, and null are rendering defects.

**Applies-to items:** every quality-matrix / metering / calibration surface (WS-BUILD-METERING-SURFACE, WS-MODIFY-CONSOLE-COMPUTE-TILE, WS-BUILD-COMMISSIONING-SURFACE).

---

## BAC-7 · Ceremony visibility (Brief §2.6, Brief §5.1)

*"Every consequential act shows its ceremony. Rule changes and de-marks render the counter-signature and countdown states inline (§5.1)."*

**Ceremony pipeline states (Brief §5.1 "Change a rule" tab):** `Propose → Counter-sign → Wait (countdown) → Applied → Re-verified.`

**Verbatim in-flight state (Brief §5.1):** *"Effective in 22 hours — you can still cancel."*

**Verbatim re-verify step:** on artifact write, state transitions to `Re-verified` (matches FL-OQ-03 ruling — both runtime state AND compliance-artifact write, transition on successful write).

**New invariants:**
- `test_ceremony_pipeline_renders_five_states` — asserts the five state names appear in reading order in the change-a-rule detail card render.
- `test_wait_state_shows_cancel_affordance` — asserts a live-cancel button renders in the Wait state.

**Applies-to items:** WS-BUILD-CEREMONY-PIPELINE, WS-MODIFY-CONSOLE-ADMINISTRATION, WS-MODIFY-CHANGE-A-RULE-TILE, WS-BUILD-CEREMONIES-APP.

---

## BAC-8 · "Walk this" everywhere (Brief §2.7, Brief §6.3)

*"Any figure, verdict, or rule row offers 'walk this' — even where the walk is a stub, the affordance exists and opens the walk pattern (§6.3)."*

**Walk pattern shape (Brief §6.3):** connected cards, each a plain question answered as a sentence, in this fixed order:
1. **What was seen** — one sentence, no ids.
2. **What we concluded** — one sentence, plus a *check it again* button (demo-functional: re-runs and matches).
3. **The rule that fired** — the rule as its sentence.
4. **What we did** — one sentence with time-to-action.
5. **How it ended** — one sentence.
6. **Who saw us do it** — one sentence naming the witness count.

Every card offers "see the working" for ids/versions/timestamps beneath. One broken-walk example must render in failed-grammar grey: *"This trail is incomplete — so it doesn't count as proof."*

**New invariant:**
- `test_walk_this_affordance_present` — asserts every rule row / verdict row / figure carries a walk-this control that opens the six-card walk pattern.
- `test_walk_pattern_six_cards_in_order` — asserts the six-card walk renders in the exact order above with the plain-question / sentence-answer grammar.

**Applies-to items:** WS-BUILD-WALK-PATTERN-COMPONENT, WS-BUILD-WATCH-RECORD, WS-BUILD-WATCH-STATE, WS-MODIFY-CONSOLE-COMPLIANCE (prove-one-run export), WS-BUILD-CEREMONY-PIPELINE.

---

## BAC-9 · Admin-surface tile groups + role visibility (Brief §3, screenshot E-4)

**Groups in order:**
| Group | Tiles | Visible to |
|---|---|---|
| TRUST CENTER | Manage Rules · Data Shield · Reasoning Shield · Access Shield | Compliance owner, operator |
| REGISTRY | Data Estate · Models · Compute · Connect | Operator, compliance read-only |
| **THE WATCH** | State · Record · Under Watch · Decisions | **Watch officer only** |
| INSTANCE | People & Declarations · Ceremonies | Instance owner, compliance |

**Identity rendering (Brief §3):**
- Role switcher top-right (demo affordance): Compliance Owner / Watch Officer / Operator.
- Watch group is *"absent — not greyed"* for non-watch roles.
- Watch tile open → banner *"Watch session · recorded."*
- Trust Center tile open → banner *"Governance session · recorded."*

**New invariants:**
- `test_watch_group_absent_not_greyed_for_non_watch_role` — asserts Watch tile group is not in the DOM at all for non-watch roles (not just hidden/disabled).
- `test_watch_session_banner_verbatim` — asserts the banner text is exactly `Watch session · recorded.`
- `test_governance_session_banner_verbatim` — asserts the banner text is exactly `Governance session · recorded.`

**Applies-to items:** WS-BUILD-CONSOLE-WATCH, WS-MODIFY-SHELL-GRAMMAR, WS-BUILD-FIVE-PILLARS, WS-BUILD-ROLE-SWITCHER, WS-BUILD-CONSOLE-COMPLIANCE-HOME, WS-WIRE-WATCH-IDENTITY.

**Placement constraint (Ruling 3 · Instruction 02 · Build Order 01 §4):** Watch tile group NEVER nested under Trust Center.

---

## BAC-10 · Watch console — verbatim §6 consumption (Brief §6, Build Order 01 §3)

*"Watch Console items consume the brief's §6 verbatim — four panels, plain-language walk card names, the seeded scenario."*

**Four panels:** State · Record · Under Watch · Decisions (Canon 8 §13).

**Seeded scenario (Brief §6, must render as one thread across all four panels):**
- Actor `ACT-1189` (procurement agent, autonomous, declared objective: supplier qualification) — 11 noted events over 9 days · rising retrieval breadth · off-declaration data classes · promoted to misdirection Aug 12 14:02 · touched planted supplier-credential record 14:31 · held (severed, marked) · aftermath in Decisions.
- Innocent actor `ACT-0733` (human analyst) — contained 40 min on drift Aug 10 · released clean on expiry · reconciliation notice sent.

**Panel 1 · State — verbatim headline + four sentences (Brief §6.1):**
- Headline: *"Quiet, with one thing needing you"*
- Q1: *"Work is flowing normally. One automated procurement agent reached for something planted as bait — it's been stopped and marked. Nobody's legitimate work was interrupted this week."*
- Q2: *"The watch tested itself this morning: a planted fault was caught and stopped in under four seconds. Every line here can be traced — tap it to see the working."*
- Q3: *"The stopped agent is held and waiting for your decision. Nothing else needed action."*
- Q4: *"All four rules held this week. One rule change is in its waiting period — effective in 22 hours. You can still cancel it."*
- Buttons: **Decide now (1 waiting)** · **Open the record.**
- Measurement layer (latency figures, budget gauges, population counts, calibration status, drill history) lives behind "see the working" · amber calibration-aging item lives there · rule 4 still holds.

**Panel 2 · Record — three lanes (Brief §6.2):**
- **Noted — no action** (default lane, first): ~10 rows including ACT-1189's early drift events and ACT-0733's first flag. Top copy: *"Seen and let pass. This lane is the restraint record."*
- **Acted:** ACT-0733's row as sentence — *"An analyst was held 40 minutes by mistake — released on the timer, work restored."* Plus two lighter rows *"Asked to verify again before continuing."*
- **Held:** bait-touch row, oxblood — *"Reached for something planted as bait — stopped and marked. Your decision is waiting."*
- **Drills** are filter chips (not a lane); toggle shows 3 drill rows woven into lanes, marked `◇`.

**Panel 3 · Under Watch — verbatim header + three sections (Brief §6.4):**
- Header: *"Nothing here is an accusation. These are patterns worth a look."*
- **Patterns:** rows as sentences (e.g., *"This procurement agent has been reading wider than its job for nine days. Small things, adding up."*); each with curve + two buttons: **Watch closer** · **Ask for an updated declaration**.
- **Copy of the estate:** *"One suspect is working inside a copy of the estate right now — 29 minutes in. Everything it touches there is harmless, and everything it does is evidence."* (Occupancy + findings only — never how the copy is built.)
- **Marked:** *"One marked actor. Every door checks for it. Removing a mark takes two signatures"* — request routes to Decisions.

**Panel 4 · Decisions — exactly four seeded items + footer (Brief §6.5):**
1. *"The stopped procurement agent is waiting on you — keep it out, or release it with a reason."*
2. *"A hold expires in 3 hours — extend it, or let it release on its own."*
3. *"The rules say this run was allowed. The watch says it wasn't what was declared. Read both sides and decide."* (two accounts side by side, resolution in one written line).
4. *"A rule change is in its waiting period — effective in 22 hours. Cancel it here if it's wrong."*
- Footer: *"If the same kind of item keeps arriving here, the fix is the rule — not faster clicking."*

**Watch negative space (hard) — Brief §6 closing paragraph:**
- No thresholds or bands anywhere.
- No placement info.
- No profile internals (trust standing chips only: `settled · forming · reduced`).
- No mirage construction detail.

**New invariants:**
- `test_watch_state_headline_verbatim`
- `test_watch_state_four_questions_verbatim`
- `test_watch_record_three_lanes_present_in_order`
- `test_watch_under_watch_verbatim_header`
- `test_watch_decisions_four_items_verbatim`
- `test_watch_no_thresholds_or_bands_rendered`
- `test_watch_no_placement_or_mirage_construction_rendered`
- `test_watch_trust_standing_chips_only_three_values`

**Applies-to items:** WS-BUILD-CONSOLE-WATCH, WS-BUILD-WATCH-STATE, WS-BUILD-WATCH-RECORD, WS-BUILD-WATCH-UNDER-WATCH, WS-BUILD-WATCH-DECISIONS, WS-BUILD-WATCH-FOUNDATION, WS-BUILD-WATCH-ACTORS.

---

## BAC-11 · People & Declarations + onboarding step (Brief §7)

- Actor rows: name/id · type (human/agent · human-driven/autonomous) · declaration summary · status chip (`current · re-declaration requested · stale`).
- Agents surface: objective / capabilities / risks as three short lines.
- Seed row `ACT-1189` with its declaration (matches Brief §6 scenario divergence).
- Onboarding modal (from "add person / commission agent"): one screen, two variants.
  - **Human:** role + working interests (chips).
  - **Agent:** objective (one sentence) + capabilities (chips) + risk note.
- Closing copy, verbatim: *"You're declaring what this actor is here to do. Conduct is read against this — and updating it here is always legitimate."*
- **Constraint:** *"Cannot skip; no undeclared entry path exists in the UI."*

**New invariants:**
- `test_declaration_modal_cannot_be_skipped` — asserts no keyboard/UI path escapes the modal without a completed declaration.
- `test_declaration_closing_copy_verbatim`
- `test_agent_declaration_carries_objective_capabilities_risks`

**Applies-to items:** WS-BUILD-DECL (already carrying Ruling-1 precondition (a) linkage), WS-BUILD-PEOPLE-DECLARATIONS-APP, WS-WIRE-CUSTODY-DECL.

---

## BAC-12 · Seed-data discipline (Brief §9)

*"All data is fictional but internally consistent: every count on a card must equal the rows behind it; every figure's 'walk this' must reach at least a stub; dates all within Mar–Aug 2026; names reused across apps (Maria Chen, J. Otieno, A. Njeri, ACT-1189, ACT-0733) so the estate reads as one place. No lorem ipsum anywhere — absence of content is rendered as the honest empty state: 'Nothing yet. That's real.'"*

**New invariants:**
- `test_seed_card_count_matches_rows_behind_it`
- `test_walk_this_reaches_at_least_stub`
- `test_seed_dates_within_march_august_2026`
- `test_no_lorem_ipsum_in_rendered_strings`
- `test_empty_state_verbatim_copy` — must render *"Nothing yet. That's real."*

**Applies-to items:** every interface item.

---

## BAC-13 · Single-file / build discipline (Brief §10)

Not directly a runtime invariant but binding on the interface donor discipline: v6 CSS variables + components reused where grammar matches; tile+card component and walk component are the two NEW primitives. §4 mapping table lives in the code as a comment block.

**Applies-to items:** WS-HARVEST-TILE-GRID-COMPONENT, WS-HARVEST-DETAIL-CARD-COMPONENT, WS-BUILD-WALK-PATTERN-COMPONENT, WS-MODIFY-SHELL-GRAMMAR.

**Definition-of-Done pass (Brief §10, verbatim):** *"every screen above exists with its seeded material; the three role views differ correctly; the four fabric-rule spot checks pass (find the amber item on State; find the not-yet-measured item; trigger one refusal; run one walk end-to-end); and nothing on any screen contradicts a canon clause cited in §4."*

**New invariants added to every interface item's DoD:**
- `test_three_role_views_differ_correctly` — asserts Compliance / Watch / Operator role switcher produces measurably different renders per Brief §3.
- `test_four_fabric_spot_checks_pass` — asserts (a) amber item findable on State surface; (b) not-yet-measured item findable somewhere; (c) at least one refusal path is trigger-able and renders the §8 refusal card; (d) at least one walk runs end-to-end without failing at a stub without stub-affordance.

---

## Applicability index — item DoD updates

For each interface item, the mapping BAC-N → DoD line is inserted with the wording *"BAC-N applied — see fixtures/binding_acceptance_criteria.md#bac-N"*. `FIXTURE PENDING` marker is REMOVED and replaced with a citation to the specific BAC-N applicable to that item.

Items receiving BAC-1..BAC-13 in their DoDs (from BUILD_STRATEGY.md item names):

- Shell + grammar: WS-HARVEST-SHELL-GRAMMAR (BAC-1,2,9,13) · WS-MODIFY-SHELL-GRAMMAR (BAC-1,2,3,9,13) · WS-HARVEST-TILE-GRID-COMPONENT (BAC-1,2,9,13) · WS-HARVEST-DETAIL-CARD-COMPONENT (BAC-1,2,7,13) · WS-BUILD-WALK-PATTERN-COMPONENT (BAC-8,13) · WS-HARVEST-CHIP-COMPONENT (BAC-2,9,13) · WS-HARVEST-REFUSAL-CARD-COMPONENT (BAC-2,4,13) · WS-BUILD-REFUSAL-CARD-COPY (BAC-4).
- Trust Center: WS-MODIFY-CONSOLE-COMPLIANCE (BAC-1,2,3,4,5,7,8,10:cross-link) · WS-MODIFY-CHANGE-A-RULE-TILE (BAC-7) · WS-MODIFY-TRUST-CENTER-GROUP (BAC-9) · WS-MODIFY-SHIELD-TILES (BAC-2,3).
- Registry: WS-MODIFY-CONSOLE-EXTRACTION (BAC-1,2,5,6,8) · WS-MODIFY-CONSOLE-COMPUTE-TILE (BAC-1,5,6,7) · WS-MODIFY-CONSOLE-INTEGRATION (BAC-1,7) · WS-MODIFY-USE-DATA-PLACEMENT (BAC-1,2,8; homes to Ask app per FL-P1-10).
- Watch: WS-BUILD-CONSOLE-WATCH (BAC-9,10) · WS-BUILD-WATCH-STATE (BAC-1,2,4,5,7,8,10) · WS-BUILD-WATCH-RECORD (BAC-1,4,8,10) · WS-BUILD-WATCH-UNDER-WATCH (BAC-10) · WS-BUILD-WATCH-DECISIONS (BAC-4,7,10) · WS-BUILD-WATCH-FOUNDATION (BAC-9,10) · WS-BUILD-WATCH-ACTORS (BAC-10,11).
- Instance: WS-BUILD-PEOPLE-DECLARATIONS-APP (BAC-11) · WS-BUILD-DECL (BAC-11) · WS-WIRE-CUSTODY-DECL (BAC-11) · WS-BUILD-CEREMONIES-APP (BAC-7) · WS-BUILD-CEREMONY-PIPELINE (BAC-7,8).
- Cross-cutting invariants: WS-WIRE-REFUSAL-FAMILY (BAC-4) · WS-BUILD-COMMISSIONING-SURFACE (BAC-1,5,6) · WS-BUILD-INVARIANT-LIST-SURFACE (BAC-13) · WS-BUILD-ROLE-SWITCHER (BAC-9) · WS-WIRE-WATCH-IDENTITY (BAC-9) · WS-BUILD-FIVE-PILLARS (BAC-9).

**Every item above gets `test_four_questions_topline_present` added to its NEW-INVARIANTS-TO-WRITE-FIRST list** (Build Order 01 §3 mandate).

---

## Re-open conditions

- If the original screenshot file arrives and pixel-level review contradicts any E-1..E-6 in the transcription: re-open FL-P1-14, correct the extraction here, re-audit affected item DoDs, refresh backend/deliverables snapshots.
- If a canon-side clarification refines any BAC-N above: append a "BAC-N-a supersession" row here and update every citation.
