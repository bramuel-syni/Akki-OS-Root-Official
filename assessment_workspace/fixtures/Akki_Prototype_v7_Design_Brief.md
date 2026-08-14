# Akki Prototype v7 — Design Brief
### Updating the standalone HTML with actual features and material
**Base:** `Akki_Prototype_v6_Standalone.html` · **Governing documents:** Canon 5 (interface law), Canon 8 (the Watch), Canon 9 (identities), Canon 3 (rules & ceremony), Canon 6 (journeys) · **Reference:** the Admin-surface screenshot (tile grid + detail card)

---

## 1 · What v7 is for

v6 proved the shell. v7 proves the **content**: the governance and security surfaces carrying real canon material — real rule sentences, real lane rows, real ceremony states, real refusal copy — laid out in the grammar the screenshot fixed: **app tiles on the left, one detail card on the right, open into the app.** The single test v7 must pass: a compliance owner and a watch officer can each walk their day on it and nothing they read is filler.

**In scope:** the Admin surface rebuilt to the tile/card grammar; the four app groups (Trust Center, Registry, **The Watch**, Instance); the repurposed governance apps with actual material; the Watch's four apps built new with one coherent scenario threaded through them; the admission declaration step; the global fabric rules below.
**Out of scope (do not touch):** Work / Build / 3rd Party surfaces beyond nav labels; any backend claim; anything marked FUTURE below.

---

## 2 · Binding fabric rules (apply everywhere, before any screen)

**Rule zero — the four questions.** Every surface leads with plain sentences answering, in order: *What's happening? How do we know? What are we doing about it? Is what we agreed being done?* A number appears only as evidence inside a sentence a person would say aloud ("stopped in under four seconds," "effective in 22 hours"). Engineering measures — p95 latencies, budget percentages, parameter codes, signal-class names — never render on an officer's surface; they live one tap behind the sentence ("see the working") and in the builder-facing drill view only. The test: if a screen cannot be read aloud to a colleague and understood first pass, it fails this rule. The Extraction frontend's simplified language is the register to match.

1. **Palette and type come from the existing tokens.** Reuse v6's CSS variables and the screenshot's rendering: warm paper canvas, white cards, ink text, navy for primary action and headers. **Oxblood is reserved** — it appears only on refusal, hold, and severance states, never decoratively. Serif display faces for app titles (as "Manage Rules" renders), sans for body and data.
2. **No build state on any surface.** No internal engine names anywhere a user reads: no Mtafiti, Northena, Solva, SyniSense, Macho, Mkono, Sarabi, Doa, Sahihi, Mnara, Moshi on screen. Org language only (mapping table in §4).
3. **Four response classes only.** Every action resolves visibly as: **done** (quiet confirmation), **held** (amber, with why and what happens next), **refused** (oxblood card, exact copy in §8), or **failed** (grey, "this is ours, not yours" tone). No fifth state, no silent outcomes.
4. **Nothing renders all-green.** Every status surface carries at least one live imperfection: an aging item, a spent fraction of a budget, a stale calibration, an open decision. All-clear is a rendering defect.
5. **Unmeasured renders honestly.** Anything not yet measured shows "not yet measured" — never a dash, never zero, never omitted.
6. **Every consequential act shows its ceremony.** Rule changes and de-marks render the counter-signature and countdown states inline (§5.1).
7. **Traceability affordance everywhere.** Any figure, verdict, or rule row offers "walk this" — even where the walk is a stub, the affordance exists and opens the walk pattern (§6.3).

---

## 3 · Navigation and identity

Top nav: `Work · Build · 3rd Party Apps · —— · Admin` (as screenshot). Admin opens the tile surface.

**Groups on the Admin surface, in order:**

| Group | Tiles | Visible to |
|---|---|---|
| TRUST CENTER | Manage Rules · Data Shield · Reasoning Shield · Access Shield | Compliance owner, operator |
| REGISTRY | Data Estate · Models · Compute · Connect | Operator, compliance read-only |
| **THE WATCH** | State · Record · Under Watch · Decisions | **Watch officer only** |
| INSTANCE | People & Declarations · Ceremonies | Instance owner, compliance |

**Identity is real in the prototype:** a role switcher (top right, demo affordance) toggles Compliance Owner / Watch Officer / Operator. The Watch group is **absent — not greyed** — for non-watch roles. Opening any Watch tile shows a one-line session banner: *"Watch session · recorded."* Trust Center tiles show *"Governance session · recorded."* This renders the Canon 9 task-identity law without explaining it.

---

## 4 · Label ↔ canon identity mapping (record this table in the code as comments)

| On-screen label | Canon identity |
|---|---|
| Manage Rules | The Rulebook + change ceremony (Doc 3 Part V, Doc 5 §23) |
| Data Shield | Boundary custody: chain, receipts, disclosure (Doc 3 §13–§20) |
| Reasoning Shield | Reasoning assurance: depth, evidence bars, traces (Doc 4 Part IV) |
| Access Shield | Entitlement + Access surface (Doc 3 §22.1, Doc 5 §41) |
| Data Estate | Estate Map / census & registry reading (Doc 5 control band) |
| Models / Compute / Connect | Model registry & ladder · economics/metering · integration wizard (Docs 4, 7) |
| State / Record / Under Watch / Decisions | The Watch Console's four panels (Doc 8 §13, Doc 5 Part VII‑A) |
| People & Declarations | Admission declarations (Doc 3 §6.1) |
| Ceremonies | The change ceremony pipeline (Doc 3 §24) |

---

## 5 · Trust Center apps — repurposed, with actual material

Each tile's **detail card** follows the screenshot pattern exactly: group kicker · app title · one-sentence description with a live number · LAST ACTIVITY (one real item, attributed, dated) · TIPS (one doctrine stated as help) · primary open button.

### 5.1 Manage Rules
**Card:** "Four rules in force. Changing one takes a counter-signature." · Last activity: *Business Development Officers may not see payroll-category content — Maria Chen, Compliance Owner · May 2, 2026* · Tip: *Rails are read-only status — no control exists to flip one, here or anywhere.*
**Open state — three tabs:**
- **Rules in force.** Plain-sentence rows, each with who set it, when, class chip (`Rule` / `Entitlement` / `Registry`), and "walk this." Seed exactly these four: (1) the BDO/payroll rule above; (2) *"Customer-identifying fields never leave the estate below masking tier 2"* — set at founding; (3) *"Model training excludes anything marked legal-hold"* — Maria Chen, Mar 14, 2026; (4) *"Third-party applications receive derived signals only, never source rows"* — set at founding.
- **Change a rule.** The ceremony as a visible pipeline: Propose → Counter-sign → **Wait (countdown)** → Applied → Re-verified. Seed one live item: a proposal to widen analyst access to supplier records, counter-signed, showing *"Effective in 22 hours — you can still cancel."* Cancel is a real button (demo-functional).
- **Rails.** Read-only list, lock glyphs, no controls — three rows: one record; deletion is an authority act; nothing leaves unmasked. Footer: *"These have no off switch. That is the product."*

### 5.2 Data Shield
**Card:** "Nothing left the estate unmasked this week — 4,182 crossings, each with its receipt." · Last activity: *The pricing study was cleared to see a little more — approved by J. Otieno · Aug 11, 2026* · Tip: *If a crossing has no receipt, the answer is refused — not the other way round.*
**Open state — the four questions:** *What's happening:* "Everything that reached a model this week crossed masked — names and identifying details swapped out before leaving, restored after." *How do we know:* the crossings list, each row a sentence — *"A pricing question crossed at the standard mask · Tue 14:02"* — with its receipt one tap behind. *What we're doing about it:* one **held** item — *"The supplier study is asking to see more than its clearance allows. Held until someone approves."* *Is what we agreed being done:* "Four data promises in force. All held this week." The masking-tier ladder and receipt ids live behind "see the working."

### 5.3 Reasoning Shield
**Card:** "Answers only claim what their evidence carries. Twelve were refused this month for saying more than we could back." · Last activity: *An answer about supplier risk was refused — it rested on a single source · Aug 9, 2026* · Tip: *A refused answer is the shield working, not the product failing.*
**Open state — the four questions:** *What's happening:* "Every answer this month was checked against its sources before it went out. Most cleared; twelve didn't, and each was refused with its reason." *How do we know:* the recent-answers list, each a sentence — *"The supplier-risk answer was refused: one source, big claim"* — tap to see the claim and its sources side by side. *What we're doing about it:* "One session was gently reframed — the questions showed someone testing a conclusion rather than exploring one, and the screen said so in the moment." *Is what we agreed being done:* "The evidence bar hasn't moved this quarter. Moving it takes the same ceremony as any rule."

### 5.4 Access Shield
**Card:** "Forty-one people and agents hold seats across six roles. Two changes this quarter — both counter-signed." · Last activity: *Watch Officer seat granted to A. Njeri — counter-signed · Aug 3, 2026* · Tip: *Access is a rule like any other — same ceremony, same record.*
**Open state — the four questions:** *What's happening:* "Who can see and do what, written as sentences, not a grid — *'Business Development Officers may not see payroll-category content.'*" *How do we know:* every seat shows who granted it, who counter-signed, and when. *What we're doing about it:* "One seat is waiting on its second signature." *Is what we agreed being done:* "No one holds access outside a written rule. Both changes this quarter went through the waiting period." The full role-by-capability grid lives behind "see the working"; declaration chips link to §7.

*(Registry group: keep v6 content, restyled into the tile/card grammar. Cards get one live number and one last-activity each; do not invent new depth. FUTURE: Compute metering detail.)*

---

## 6 · The Watch — four apps, built new, one scenario threading all four

**The scenario (seed data tells one story):** Actor **ACT-1189** ("Procurement agent · autonomous," declared objective: *supplier qualification*) accumulated 11 noted events over 9 days (rising retrieval breadth, off-declaration data classes) → promoted to misdirection Aug 12, 14:02 → touched a planted supplier-credential record 14:31 → **held** (severed, marked) → aftermath item sits in Decisions. In parallel: one innocent, **ACT-0733** (human analyst), was contained 40 min on drift Aug 10, released clean on expiry, reconciliation notice sent. Every panel below shows its face of this same story.

### 6.1 State
The four questions answered in sentences, verbatim (headline: **"Quiet, with one thing needing you"**):
- **What's happening:** *"Work is flowing normally. One automated procurement agent reached for something planted as bait — it's been stopped and marked. Nobody's legitimate work was interrupted this week."*
- **How do we know:** *"The watch tested itself this morning: a planted fault was caught and stopped in under four seconds. Every line here can be traced — tap it to see the working."*
- **What we're doing about it:** *"The stopped agent is held and waiting for your decision. Nothing else needed action."*
- **Is what we agreed being done:** *"All four rules held this week. One rule change is in its waiting period — effective in 22 hours. You can still cancel it."*

Buttons: **Decide now (1 waiting)** · **Open the record.** The measurement layer (latency figures, budget gauges, population counts, calibration status, drill history) lives behind "see the working" — one tap, same card grammar, and the amber calibration-aging item lives there (rule 4 still holds: the working view is never all-green).

### 6.2 Record
Three lanes. Every row is a sentence first — *"A procurement agent reached for something planted as bait — stopped and marked"* — with time, actor, and certainty as the quiet second line. Never a data tuple. The lanes answer the four questions across time: noted-only is *what's happening*, the walk is *how we know*, acted/held is *what we did about it*:
- **Noted — no action** (default lane, deliberately first): seed ~10 rows incl. ACT-1189's early drift events and ACT-0733's first flag. Copy at top: *"Seen and let pass. This lane is the restraint record."*
- **Acted:** ACT-0733's row as a sentence — *"An analyst was held 40 minutes by mistake — released on the timer, work restored."* Kept visible on purpose: this is the honesty record. Two lighter rows: *"Asked to verify again before continuing."*
- **Held:** the bait-touch row, oxblood: *"Reached for something planted as bait — stopped and marked. Your decision is waiting."* (Which rule fired lives in the walk, not on the row.)
- **Drills** appear as filter chips, not a lane: toggling shows 3 drill rows woven into the lanes, marked ◇.

### 6.3 The walk (row expansion — build once, reuse everywhere)
Expanding the held row shows the chain as connected cards, each named as a plain question and answered in a sentence: **What was seen** — *"It touched a record planted as bait. No honest path reaches that record."* → **What we concluded** — *"This is certain, not suspicion,"* with a **"check it again"** button (demo-functional: re-runs and matches) → **The rule that fired** — the rule as its sentence: *"Anything touching planted bait is stopped at once."* → **What we did** — *"Stopped at 14:31 — within four seconds of the touch."* → **How it ended** — *"Marked. It will be recognised at every door it tries next."* → **Who saw us do it** — *"Two independent witnesses signed this record as it happened."* Every card offers "see the working" for the ids, versions, and timestamps beneath. Include one broken-walk example elsewhere rendering in failed-grammar grey: *"This trail is incomplete — so it doesn't count as proof."*

### 6.4 Under Watch
Header copy, verbatim: *"Nothing here is an accusation. These are patterns worth a look."*
- **Patterns:** rows as sentences — *"This procurement agent has been reading wider than its job for nine days. Small things, adding up."* — each with its little curve and two buttons: **Watch closer** · **Ask for an updated declaration** (the innocent exit, rendered as a first-class action).
- **The copy of the estate:** *"One suspect is working inside a copy of the estate right now — 29 minutes in. Everything it touches there is harmless, and everything it does is evidence."* Occupancy and findings only — never how the copy is built.
- **Marked:** *"One marked actor. Every door checks for it. Removing a mark takes two signatures"* — the request routes to Decisions.

### 6.5 Decisions
Exactly four seeded items, each a sentence with its trail attached: (1) *"The stopped procurement agent is waiting on you — keep it out, or release it with a reason."* (2) *"A hold expires in 3 hours — extend it, or let it release on its own."* (3) *"The rules say this run was allowed. The watch says it wasn't what was declared. Read both sides and decide."* — the two accounts side by side, resolution takes one written line. (4) *"A rule change is in its waiting period — effective in 22 hours. Cancel it here if it's wrong."* Footer, verbatim: *"If the same kind of item keeps arriving here, the fix is the rule — not faster clicking."*

**Watch negative space (hard):** no thresholds or bands anywhere; no placement info; no profile internals (trust standing chips only: `settled · forming · reduced`); no mirage construction detail.

---

## 7 · People & Declarations + onboarding step

- **People & Declarations app:** every actor row = name/id · type (human/agent · human-driven/autonomous) · declaration summary · status chip (`current · re-declaration requested · stale`). Agents show *objective / capabilities / risks* as three short lines. Seed ACT-1189's declaration so the scenario's divergence is legible against it.
- **Onboarding modal (reachable from "add person / commission agent"):** one screen, two variants. Human: role + working interests (chips). Agent: objective (one sentence) + capabilities (chips) + risk note. Closing copy, verbatim: *"You're declaring what this actor is here to do. Conduct is read against this — and updating it here is always legitimate."* Cannot skip; no undeclared entry path exists in the UI.

---

## 8 · Verbatim copy blocks (paste exactly)

**Refusal card (oxblood):** title *"This can't cross."* · body: reason in plain words, one sentence · line: *"What was refused, not who you are: [reason name]"* · actions: only ones the viewer can take (e.g., *request disclosure*, *see the rule*). Never "contact administrator" alone.
**Held card (amber):** *"Held for [reason]. Nothing is lost — it releases or resolves by [time]."*
**Failed card (grey):** *"Something on our side broke. Your request was valid. Retry, or leave it with us — it's recorded."*
**Watch session banner:** *"Watch session · recorded."*
**Reconciliation notice (ACT-0733's):** *"Between 09:12–09:52 on Aug 10 your work was held for review and did not land. It has been replayed successfully. Nothing further is needed."*

---

## 9 · Seed-data discipline

All data is fictional but **internally consistent**: every count on a card must equal the rows behind it; every figure's "walk this" must reach at least a stub; dates all within Mar–Aug 2026; names reused across apps (Maria Chen, J. Otieno, A. Njeri, ACT-1189, ACT-0733) so the estate reads as one place. No lorem ipsum anywhere — absence of content is rendered as the honest empty state: *"Nothing yet. That's real."*

## 10 · Build notes

Single-file constraint stands (one HTML, inline CSS/JS, same stack as v6). Reuse v6 components where the grammar matches; the tile+card and walk components are the two new primitives — build each once. Keep the §4 mapping table as a code comment block. Definition of done: every screen above exists with its seeded material; the three role views differ correctly; the four fabric-rule spot checks pass (find the amber item on State; find the not-yet-measured item; trigger one refusal; run one walk end-to-end); and nothing on any screen contradicts a canon clause cited in §4.
