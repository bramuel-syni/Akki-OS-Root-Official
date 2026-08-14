# reference_screenshot_transcription.md

**Grade:** AUTHORITATIVE-UNTIL-FILE-ARRIVES.
**Source:** Owner channel · 2026-08-14 · direct transcription of the Admin-surface reference screenshot (screenshot was sent inline to the owner's channel; original image file not yet in workspace — owner has asked to re-send as file; not yet arrived).
**Governance status:** Clears screenshot-dependent FIXTURE PENDING markers at **transcription grade** (not file grade). FL-P1-14 records the distinction: `transcription-cleared` (fixture-content available for extraction) vs `file-cleared` (image bytes on disk for pixel-level review). Re-open on file arrival if the pixels contradict this transcription.

---

## Verbatim owner transcription

=== SCREENSHOT TRANSCRIPTION (Admin surface, tile-grid-plus-detail-card) ===
Layout: two-pane. LEFT ~45%: top tab bar with pill tabs "Work · Build · 3rd Party Apps" grouped left, "Admin" right-aligned and active (darker pill). Below, tile GROUPS under small-caps letterspaced grey group labels. Group 1 label: "TRUST CENTER" — four tiles in a row: "Manage Rules" (SELECTED state: white card, dark border, icon in rounded lavender square), "Data Shield" (shield outline icon), "Reasoning Shield" (shield-check icon), "Access Shield" (shield-lock icon). Group 2 label: "REGISTRY" — four tiles: "Data Estate" (database icon), "Models" (layers icon), "Compute" (chip/gear icon), "Connect" (link icon). Unselected tiles: flat cream cards, subtle border, centered circular icon chip above centered label. RIGHT ~55%: one large white detail card, rounded corners, for the selected tile: eyebrow small-caps in blue "TRUST CENTER"; large SERIF display title "Manage Rules"; plain-sentence lede in grey sans: "Four rules in force. Changing one takes a counter-signature."; divider; section "LAST ACTIVITY" (small-caps grey) with bold plain sentence "Business Development Officers may not see payroll-category content" and attribution line "Maria Chen, Compliance Owner · May 2, 2026"; divider; section "TIPS" with bulleted plain sentence "Rails are read-only status — no control exists to flip one, here or anywhere."; footer row with primary dark-navy button "Open Manage Rules" and secondary outlined button "Open". Top-right of card: small square icon button (panel toggle). Palette: warm cream page background, white cards, dark navy primary, lavender icon accent, serif for card titles only, sans elsewhere. Grammar note: tiles never carry data; ALL state lives in the detail card as plain sentences (rule zero visible: what's happening = lede, how do we know = last activity with named actor + date, what are we doing = actions, is the agreement holding = tips/rails line).
=== END TRANSCRIPTION ===

---

## Binding extractions from the transcription (mechanical, no interpretation)

### E-1 · Global grammar (all Admin-surface consoles inherit)

- **Two-pane layout, LEFT ~45% / RIGHT ~55%.** Tile grid on the left; single detail card on the right.
- **Top tab bar** with pill tabs. Group order in this instance: `Work · Build · 3rd Party Apps` left-grouped, `Admin` right-aligned; active tab renders as darker pill.
- **Group labels** are small-caps letterspaced grey text sitting above each tile row.
- **Tiles never carry data.** Every runtime state lives in the detail card as plain sentences. Tiles present name + icon only.
- **Detail-card section grammar** (top to bottom): eyebrow (small-caps blue console-identity label) · SERIF display title · plain-sentence lede (grey sans) · divider · `LAST ACTIVITY` section (small-caps grey label + bold plain sentence + attribution line `Name, Role · Date`) · divider · `TIPS` section (bulleted plain sentence) · footer row (primary dark-navy button + secondary outlined button) · small square panel-toggle icon-button top-right.
- **Palette:** warm cream page background · white detail card + selected-tile card · dark navy primary (buttons, active pill, active tile border, primary text) · lavender icon accent (inside rounded square icon chip on the selected tile) · serif for detail-card display titles only · sans-serif elsewhere · unselected tiles render as flat cream cards with subtle border and a centered circular icon chip above the centered label.
- **Selected-tile state.** White card with dark border and icon in rounded lavender square chip; unselected tiles remain cream with circular chip.

### E-2 · Rule zero — four-question topline (per detail card)

Every detail card renders answers to Canon-5 rule zero in this exact reading order (grammar note, verbatim from transcription):

| Question | Rendering slot in the detail card |
|---|---|
| **What's happening?** | Plain-sentence LEDE under the display title. |
| **How do we know?** | `LAST ACTIVITY` block: bold plain sentence + `Name, Role · Date` attribution. |
| **What are we doing?** | Footer row action buttons (primary + secondary). |
| **Is the agreement holding?** | `TIPS` bulleted plain sentence naming the rail's read-only status. |

**Invariant that must be added to the new-invariants list for every console item** (Build Order 01 §3):
`test_four_questions_topline_present` — asserts that every detail-card render carries all four slots populated with plain sentences; engineering measures (latencies, percentages, parameter codes) are absent from these slots and remain one tap behind "see the working".

### E-3 · Verbatim seeded copy (Manage Rules card)

Copy shown MUST be used verbatim when the same surface renders (per Build Order 01 §3 "verbatim seeded copy — copy language from the brief rather than inventing it"):

- **Eyebrow:** `TRUST CENTER`
- **Display title:** `Manage Rules`
- **Lede:** `Four rules in force. Changing one takes a counter-signature.`
- **Last activity bold sentence:** `Business Development Officers may not see payroll-category content`
- **Last activity attribution:** `Maria Chen, Compliance Owner · May 2, 2026`
- **Tips sentence:** `Rails are read-only status — no control exists to flip one, here or anywhere.`
- **Primary button:** `Open Manage Rules`
- **Secondary button:** `Open`

### E-4 · Tile-group inventory (this screenshot instance)

| Group label | Tiles (in order) | Canon-5 identity mapping (per Build Order 01 §2.C rulings) |
|---|---|---|
| `TRUST CENTER` | `Manage Rules` · `Data Shield` · `Reasoning Shield` · `Access Shield` | Compliance Console family (Canon 5 §22-§26); Data/Reasoning/Access Shield label→identity mapping per FL-P1-16 (Build Order 01 §2.C). `Manage Rules` label→identity Canon 5 §32 Administration Console change-a-rule tile (FL-P1-13 dedupe closed). |
| `REGISTRY` | `Data Estate` · `Models` · `Compute` · `Connect` | Extraction Console family (Canon 5 §13-§17) — Data Estate = Estate Map; Models = Model Catalogue; Compute = new tile bound to A3 compute plan; Connect = Integration Console (Canon 5 §27-§29). |

**Not shown in this screenshot but named by Build Order 01 for the same grammar:** the Watch group (State · Record · Under Watch · Decisions per Canon 8 §13), renders as a fourth tile group on the Admin surface, never nested under Trust Center (Ruling 3 · Instruction 02).

### E-5 · Icon conventions (mechanical)

- Selected tile: icon in rounded-square lavender chip.
- Unselected tile: icon in centered circular chip above centered label.
- Trust Center tiles: shield-family icons (outline / check / lock variants) except `Manage Rules` (generic icon in lavender square when selected).
- Registry tiles: `Data Estate` = database icon; `Models` = layers icon; `Compute` = chip/gear icon; `Connect` = link icon.

### E-6 · What is NOT in the transcription (declared absences — do not invent)

- No search box visible.
- No breadcrumb visible.
- No numeric badges on any tile.
- No overlay / modal shown.
- Watch tile group is not shown on this screenshot (Watch is named in Build Order 01 §4 but the fixture in this transcription shows two groups only: Trust Center + Registry).
- No refusal card shown (Canon 5 §9.2 refusal surface is not exercised in this screenshot).
- No commissioning surface, no rulebook edit surface, no invariant list surface visible.
- Fifth pillar / Watch-officer session indicator: not visible in this transcription.
- Bottom-of-page footer / status bar: not visible.

Absences are recorded per Build Order 01 discipline (fixture-bound, do-not-invent).

---

## Item-level applicability (which strategy items now inherit this transcription as acceptance criteria)

Every interface item whose DoD carried `FIXTURE PENDING (reference screenshot)` inherits E-1 through E-6 as binding acceptance criteria at transcription grade. Names (from `notes/strategy_items_part1.md` and `strategy_items_part2.md`):

- WS-HARVEST-SHELL-GRAMMAR
- WS-HARVEST-TILE-GRID-COMPONENT
- WS-HARVEST-DETAIL-CARD-COMPONENT
- WS-HARVEST-REFUSAL-CARD-COMPONENT
- WS-HARVEST-CHIP-COMPONENT
- WS-MODIFY-USE-DATA-PLACEMENT (Ask reference application per FL-P1-10)
- WS-MODIFY-CONSOLE-COMPLIANCE
- WS-MODIFY-CONSOLE-EXTRACTION
- WS-MODIFY-CONSOLE-INTEGRATION
- WS-MODIFY-CONSOLE-ADMINISTRATION
- WS-MODIFY-CHANGE-A-RULE-TILE (dedupe per FL-P1-13)
- WS-MODIFY-TRUST-CENTER-GROUP (label kept per FL-P1-15)
- WS-MODIFY-SHIELD-TILES (labels kept per FL-P1-16)
- WS-MODIFY-WORKSTUDIO-RENAME (Work per FL-P1-17)
- WS-MODIFY-LEAD-REPARENT (ThinkLab, Monitor under Lead per FL-P1-18)
- WS-MODIFY-3RD-PARTY-APPS-TAB (label kept per FL-P1-19)
- WS-BUILD-FIVE-PILLARS
- WS-BUILD-CONSOLE-WATCH (Watch group placement per Ruling 3 · fourth group, never nested under Trust Center)
- WS-BUILD-REFUSAL-CARD-COPY
- WS-WIRE-REFUSAL-FAMILY
- WS-BUILD-COMMISSIONING-SURFACE
- WS-BUILD-INVARIANT-LIST-SURFACE
- Every Watch Console item consuming Canon 8 §13 four-panel grammar (State · Record · Under Watch · Decisions).

The `test_four_questions_topline_present` invariant is added to the must-write-first invariant list for **every** item in the list above (Build Order 01 §3).

## Re-open condition

If/when the original image file arrives in `fixtures/reference_screenshot.<ext>` and pixel-level review contradicts any extraction E-1..E-6, re-open FL-P1-14, correct the extraction, and re-audit affected item DoDs. Until then, this transcription IS the fixture.
