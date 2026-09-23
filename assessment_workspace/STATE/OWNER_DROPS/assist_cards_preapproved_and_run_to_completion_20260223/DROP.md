# OWNER DROP — CP-AIP-ASSIST CARDS PRE-APPROVED · TRACK-5 CHECKPOINT REMOVED · RUN TO COMPLETION — 2026-02-23

**Received:** 2026-02-23 (mid-CP-AIP-9 pre-Commit-B) · **Class:** §6.8 standing-authority ratification + run-to-completion mandate · **Banking:** verbatim + application notes · **Additive:** no sealed code touched; supersedes the prior Track-5 pre-build checkpoint · **Owner status from receipt:** STEPPING AWAY — E1 runs to completion autonomously and delivers OWNER_RETURN_REPORT.md + BUILD_JOURNAL.md as final artefact.

---

## §1 — Verbatim owner text (BINDING; bank in `STATE/OBJECTIVES` for both cards + `DECISIONS.md`)

> "CP-AIP-ASSIST-CENSUS and CP-AIP-ASSIST-TRAINING · pre-approved; build under standing authority. §6.8 applies. No spec review, no GO. The six conditions below are the cards' MUST-DO and MUST-NOT lines and their exit evidence; a draft that meets them is approved by construction.
>
> Objective. An assistant inside Akki that runs the shape-and-evolve dialogue with a tenant owner — propose an objective, test it against the estate's own account, record the confirmed decision, re-shape as new facts land — for census reads and for training runs. It proposes; the owner confirms; the platform's existing gates decide.
>
> Conditions — tests first, RED, then build:
> 1. No path to any decision. Negative-scan: assistant modules import nothing from approval, commission, gate, or measure modules, and nothing there imports them. A proposal reaches a decide-point only through a human confirm action carrying that human's principal.
> 2. Confirmed turns only are banked. A confirmed turn writes a receipted decision with provenance (A5.16). An unconfirmed turn is a draft and never enters the decision record.
> 3. Census assistant is read-only against the Registry. No write path. A census run with and without the assistant produces byte-identical figures (B5.1).
> 4. Training assistant's proposals freeze at commission. Objective and criteria set cannot change after Northena's freeze; MOAC criteria are set by the owner's confirm, never by the assistant.
> 5. Content: Generated, chat surface, anchored, gated. R-32, A5.15, CON-6 — a sentence without an anchor is refused; a number not in the Registry is refused; honest markers over refusals wherever canon provides one.
> 6. No learning from dialogue. No per-tenant adaptation, no cross-tenant memory. Improvements enter only through the research queue and capability admission (L-4, L-5).
>
> Placement. Outside the TCB. The decide-points it feeds — confirm, commission, criteria-set — already exist and stay where they are. Every string is a Content Registry entry.
>
> Forks. A condition that cannot be met as written is banked to DESK_QUEUE.md with options and a recommendation; the other track continues.
>
> Exit. Six test IDs green in the ratchet; both cards pinned; seal per §3.3."

---

## §2 — Verbatim EXECUTION block

> "- RED-first: author the six invariants (one test ID per condition) FAILING first, cite the exact clause on each (negative-scan import isolation = condition 1; A5.16 receipted-confirmed-turn = 2; B5.1 byte-identical census with/without assistant = 3; post-freeze immutability + owner-set MOAC = 4; R-32/A5.15/CON-6 anchored-gated content = 5; L-4/L-5 no-dialogue-learning = 6), then build additively to GREEN. Both cards pinned; 5-commit seal per §3.3.
> - Placement OUTSIDE the TCB; assistant only proposes into existing confirm/commission/criteria-set decide-points via a human confirm carrying that human's principal. Every user-facing string is a Content Registry entry.
> - FORK RULE: any condition not meetable as written → bank to DESK_QUEUE.md with options + your recommendation, and continue the other track. Surface DESK_QUEUE forks to me at the next milestone report."

---

## §3 — Verbatim OWNER-STEPPING-AWAY / RUN-TO-COMPLETION mandate

> "The owner is stepping away. Run the entire remaining ledger to completion autonomously (CP-AIP-9 seal → CP-AIP-10 → §6.9 LID wave on the labelled corpus → ENT-16 seeds → census three waves → tenant separation → Track-4 autonomy wiring → Track-5 ASSIST cards). Then, as the FINAL deliverable, compile OWNER_RETURN_REPORT.md + BUILD_JOURNAL.md so the owner has one consolidated report on return: everything sealed, ratchet history, all owner-drop receipts (Q1/Q2/Q3, corpus census, LID gate agreement numbers), GAPS_FIXED ledger, bundle-publish confirmations, DESK_QUEUE forks with recommendations, and the two pending human items (Akki-OS-Root privacy flip if you lacked repo-admin; any credential/ratification items per §6.9 clause 9).
>
> HALT to me only on: a SPEC-CONFLICT-<n>, a hard custody/gate violation, or when the full ledger + OWNER_RETURN_REPORT is complete. Otherwise report-and-continue at each milestone seal (bundle status + GAPS_FIXED each time). All 17 guards + SO §6.9 binding. Execute."

---

## §4 — Application

**Pre-approval by construction.** Prior Track-5 pre-build checkpoint (where E1 was to report card drafts before building) is REMOVED. Both cards are approved-by-construction if the six conditions land as RED-first invariants → GREEN implementations at the specified test IDs. E1 opens the ASSIST cards as ordinary sequential seals after Track-4 (Census Autonomy Service wiring) completes.

**Six conditions as MUST-DO/MUST-NOT test IDs (each becomes exactly one RED-first invariant per card, or one shared invariant covering both cards depending on scope):**

| Condition | MUST-DO / MUST-NOT (verbatim) | Test ID (proposed · will be finalised at card open) | Canon anchor |
|---|---|---|---|
| **1** | Assistant modules import nothing from approval/commission/gate/measure modules, and nothing there imports them. Proposal → decide-point only via human confirm carrying that human's principal. | `test_assist_no_path_to_any_decision_negative_scan_import_isolation` | A5.16 + §6.8 + §1.4 doctrine |
| **2** | Confirmed turns only are banked. Confirmed turn → receipted decision with provenance (A5.16). Unconfirmed turn = draft, never enters decision record. | `test_assist_confirmed_turn_only_banked_a5_16_receipted_provenance` | A5.16 |
| **3** | Census assistant is read-only against Registry (no write path). Census run WITH-assistant and WITHOUT-assistant produces byte-identical figures. | `test_assist_census_readonly_with_without_byte_identical_b5_1` | B5.1 |
| **4** | Training assistant's proposals freeze at commission. Objective + criteria set immutable post-Northena-freeze. MOAC criteria set by owner's confirm, never by assistant. | `test_assist_training_proposals_freeze_at_commission_moac_owner_set_only` | Northena freeze + MOAC |
| **5** | Content generated, chat surface, anchored, gated. R-32 (sentence without anchor refused) + A5.15 (number not in Registry refused) + CON-6 (honest markers over refusals wherever canon provides one). | `test_assist_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal` | R-32 + A5.15 + CON-6 |
| **6** | No learning from dialogue. No per-tenant adaptation, no cross-tenant memory. Improvements enter ONLY through research queue + capability admission. | `test_assist_no_learning_from_dialogue_l4_l5_only_admission_path` | L-4 + L-5 |

**Placement (verbatim owner directive):** OUTSIDE the TCB. Decide-points (confirm, commission, criteria-set) are pre-existing and stay where they are. Every user-facing string is a Content Registry entry (R-32/A5.15/CON-6 chain).

**Fork rule:** any condition not meetable as written → bank to `STATE/DESK_QUEUE.md` with options + recommendation; the OTHER track continues. Surface at next milestone report.

**Exit:** six test IDs green in the ratchet · both cards pinned · 5-commit seal per §3.3.

---

## §5 — Ledger position — the two ASSIST cards move ONTO the active ledger (from "drafts pending checkpoint" → "pre-approved sequential seals")

**Prior position (superseded):** two ASSIST card drafts sat at `STATE/OBJECTIVES/CP_AIP_ASSIST_CENSUS.md` + `STATE/OBJECTIVES/CP_AIP_ASSIST_TRAINING.md` awaiting Track-5 pre-build checkpoint report to owner.

**New position (this drop):** both cards are pre-approved by construction. They open in sequence AFTER Track-4 (Census Autonomy Service wiring) completes, per the run-to-completion order:

1. CP-AIP-9 seal (in flight; State Commit-B lands this drop as fold-in)
2. CP-AIP-10 seal (training-runs service registration seat)
3. SO §6.9 LID wave (Whisper-LID + VoxLingua107 admission gate on `google-transcripts/` labelled corpus)
4. ENT-16 pilot licence seeds (RMS + DigiCow + AKKI-TEST)
5. Census three waves + tenant separation (Fred Afune/Muthoni Kiarie/Samuel Kibacia + Vincent Kimani/Peninah Wanja + any-one rule + isolation-sweep exit evidence)
6. Track-4 autonomy wiring (LID + census + training as Census Autonomy Service jobs)
7. **CP-AIP-ASSIST-CENSUS** (six conditions RED-first → GREEN → 5-commit seal)
8. **CP-AIP-ASSIST-TRAINING** (six conditions RED-first → GREEN → 5-commit seal)
9. Compile OWNER_RETURN_REPORT.md + BUILD_JOURNAL.md as FINAL deliverable

---

## §6 — HALT conditions (verbatim owner directive)

HALT to owner ONLY on:
- Any `SPEC-CONFLICT-<n>` discovered mid-slice.
- A hard custody/gate violation.
- Completion of the full ledger + OWNER_RETURN_REPORT.md + BUILD_JOURNAL.md.

Otherwise: REPORT-AND-CONTINUE at each milestone seal (bundle status + GAPS_FIXED_LEDGER + measured receipts each time). All 17 standing guards + SO §6.9 remain binding.

---

## §7 — One-sentence protected objectives (per §6.9 desk discipline)

- **Pre-approval by construction:** removes a checkpoint that would gate on owner presence and unlocks autonomous build during owner's absence, while binding the build to six measurable exit-conditions so the deliverable is inspectable-not-negotiable.
- **Six conditions as MUST-DO/MUST-NOT test IDs:** ensures the assistant proposes-only and never decides — the platform's existing gates (confirm/commission/criteria-set) retain sole authority over decide-points.
- **RED-first invariants + GREEN implementation:** ensures the six MUST-DOs are structurally enforced, not assertion-of-good-behaviour.
- **Fork rule to DESK_QUEUE:** prevents any single-condition impasse from stalling both tracks; the other track continues while the fork awaits the batched desk answer.
- **Run-to-completion mandate:** delivers the full ledger without owner-round-trips; OWNER_RETURN_REPORT.md is the single consolidated report on owner return.
- **HALT only on SPEC-CONFLICT / custody / completion:** preserves owner authority over specification and custody edges without gating on routine execution.

---

## §8 — Ledger check

This drop banks the CP-AIP-ASSIST-CENSUS + CP-AIP-ASSIST-TRAINING pre-approval verbatim + the run-to-completion mandate verbatim + the placement + fork + exit rules, and nothing else. Additive-only. No sealed carrier edit. In-flight CP-AIP-9 5-commit seal continues on the same commit boundary; State Commit-B carries the fold-in.
