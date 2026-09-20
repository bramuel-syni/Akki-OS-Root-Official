# DAP REQUEST LIFECYCLE · Pending Rulings Register

**Opened**: 2026-09-20T~12:00Z at CP-DAP-LIFECYCLE-BACKEND-WAVE opening (WAVE R-70 · Step 1)
**Manifest**: `phase0/credential_drop_manifests/20260920T1140Z_owner_drops_manifest.json`
**Owner directive verbatim (this-session)**: "Eight owner-policy/spec-clarification decision questions issued (DAP-LIFECYCLE-Q1..Q8) — 6 owner-policy (Q1..Q6) + 2 spec clarifications (Q7..Q8); each is HARD-HOLD fail-closed until ruled per owner directive verbatim."

**Owner corrections banked at wave-open (this-session, verbatim)**:
1. DAP-15 timer discipline correction: "DAP-15's 14-day expiry runs from SUBMISSION to DECISION: the transition is `In Approval → Expired` when no decision lands within 14 calendar days of submission ('a request that receives no decision within 14 calendar days of submission expires unexecuted — silence is never treated as approval'). Ready → Expired is NOT the DAP-15 rule — a finished, unretrieved output does not expire under DAP-15."
2. Q7/Q8 disposition correction: "Q8 is NOT a hard hold: the banked DEFAULT-class ruling is BUILD TO THE YES-READING (destination removal blocks future use only; historical receipts untouched, DAP-26 analogy), tagged pending ratification. Only Q1-Q6 are hard-hold placeholders. Q7's disposition is also already set: Blocked stays 3-kind, non-gate fault surfaces as banked TODO marker fail-closed (check first whether the unshared remainder of spec §6 exists on disk)."
3. Scope-addition: "Add the notification event-emission surface to Phase 2/3 scope (toast events at submission + retrieval per the journey spec; email as stub/queue behind flag OFF — DEFAULT-class, already banked)."
4. Approval-service test additions: "The decision-service tests should assert the identity discipline from the journey spec — submitter identity recorded and surfaceable, approver identity NEVER surfaced to the party (role + data-owner name only), decisions permanent (no reopen path). Those three are testable now and are the spine of the approval surface."
5. Ratchet discipline: "Ratchet: NEVER a preset target — measure the delta empirically post-GREEN, reconcile line-by-line, then bump. 5546 is the floor; write the measured number."

## Q7 spec §6 check-first outcome

**Hunt receipt**: `phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json`

The unshared remainder of DAP-Spec §6 EXISTS on disk at `canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx`. Section title is "Failure Posture" containing DAP-28/29/30. It defines fail-closed for gates only — **it does NOT define a non-gate execution fault state and does NOT define a fourth kind of `Blocked`**. Q7 disposition therefore STANDS at HARD HOLD with the banked TODO marker fail-closed pattern until owner rules.

## Register

| ID | Class | Question verbatim | Disposition | Code-site pattern |
|---|---|---|---|---|
| DAP-LIFECYCLE-Q1 | owner-policy | Can an unchanged request be retried after a check block without fresh approval? | **HARD HOLD** — Retry action NOT shipped; placeholder fail-closed at code sites | `raise NotYetSpecified("DAP-LIFECYCLE-Q1 retry semantics undecided — see STATE/dap_lifecycle_pending_rulings.md")` |
| DAP-LIFECYCLE-Q2 | owner-policy | Can a standing approval cover Train a Model or Build a Skill? | **HARD HOLD** — Standing-approval branch exists structurally, unreachable at runtime until ruled | Standing-approval routing branch present but gated `if False:  # HARD HOLD DAP-LIFECYCLE-Q2`; else path routes to normal `In Approval` |
| DAP-LIFECYCLE-Q3 | owner-policy | Does a partial release exist as an outcome? | **HARD HOLD** — All-or-nothing default; TC-RET-16 stays held | Decision service accepts only `accept` / `refuse`; `partial_release` disposition raises `NotYetSpecified("DAP-LIFECYCLE-Q3")` |
| DAP-LIFECYCLE-Q4 | owner-policy | Who receives a spend-ceiling breach (owner-side/party-side) + 14-day applicability + party-visible state? | **HARD HOLD** — Route to refusal-with-banked-marker until ruled; no party-side waiting state | Spend-ceiling breach → `Refused` with `banked_marker="DAP-LIFECYCLE-Q4"`; NO new state added |
| DAP-LIFECYCLE-Q5 | owner-policy | Does finished output survive a suspension from Ready? | **HARD HOLD** — Blocked drawer renders visible "not yet specified" placeholder; journey L91 confirms terminal `Blocked` from anywhere including Ready | Suspension-from-Ready path lands in `Blocked` with `kind=<gate-kind>` and marker `DAP-LIFECYCLE-Q5`; artefact retention question raises `NotYetSpecified` at retrieval-attempt site |
| DAP-LIFECYCLE-Q6 | owner-policy | Should the party see the owner's turnaround time ("Waited N days" line)? | **HARD HOLD** — OMIT the line entirely until owner consents (showing without consent is harm; omission reversible) | Backend does NOT emit any "days-waited-by-owner" or turnaround field until ruled |
| DAP-LIFECYCLE-Q7 | spec-clarification | Does a non-gate execution fault exist as its own state? | **HARD HOLD (banked TODO marker fail-closed)** — spec §6 remainder read (see hunt receipt); no fourth kind of Blocked authorised. Non-gate fault surfaces as banked TODO marker fail-closed until owner rules | Non-gate fault raises `NonGateExecutionFaultNotYetSpecified("DAP-LIFECYCLE-Q7")`; NO fourth Blocked kind added |
| DAP-LIFECYCLE-Q8 | spec-clarification | Does removing a registered destination leave historical receipts untouched? | **DEFAULT-CLASS · BUILD TO YES-READING · PENDING RATIFICATION** — destination removal blocks future use only; historical receipts untouched (DAP-26 no-retroactive-change by analogy; `party_admission_journey.md, §6` analogy) | Destination removal → future-use block; historical `Retrieved` drawer's "Delivered to X" line and receipt records remain untouched; module-scope constant `DESTINATION_REMOVAL_HISTORICAL_UNTOUCHED = True  # DAP-LIFECYCLE-Q8 · DEFAULT-class · pending ratification` |

## Deliberately deferred (not questions · banked as product decisions at wave-open)

- **Org-admin status emails**: submitter-only remains the current rule per owner directive verbatim. Product decision. Nothing blocked.
- **Mass-suspension email granularity**: product decision. Nothing blocked.

## Buildable-now scope this wave

Notwithstanding the eight HARD HOLDs, the following are buildable and are the target scope for this wave:

1. **Request state machine** (structural · terminal set): `Compose → Submitted → Routing → In Approval → Executing → Ready → Retrieved`; terminals `Refused / Blocked / Expired`.
2. **DAP-15 14-day timer** on `In Approval → Expired` transition (silence never = approval).
3. **Approval decision service** (accept / refuse paths only): submitter identity recorded and surfaceable; approver identity NEVER surfaced to party (role + data-owner name only); decisions permanent (no reopen path).
4. **Gate → Blocked** surfacing (3 kinds: `request`, `check`, `estate`); non-gate execution fault Q7-TODO.
5. **Retrieval → MeteredEvent** wiring on the single chain (DAP-21 per-retrieval receipt; repeat downloads = new metered event; report re-open = no new event).
6. **Notification event-emission surface**: `RequestSubmittedNotification` + `RequestRetrievedNotification` toast events emitted on state transitions; **email = stub/queue behind flag OFF** (DEFAULT-class banked, no external side-effect).

## Standing bounds preserved at this register

zero push · terminal pytest only · no testing_agent · additive-only §3.8 · SO §4.1 §F sha-pinning discipline · three-repo discipline · ratchet monotonic (floor **5546** · never rebaselined silently).


---

## Update · 2026-09-20T~14:45Z · CP-Q-UNLOCK-SUB-WAVE dispositions

Owner ruling R-78 (2026-09-20T~13:00Z verbatim in STATE/DECISIONS.md R-78) resolved 6 of the 8 pending questions:

| ID | Prior | Now | Module |
|---|---|---|---|
| Q1 Retry after check block | HARD HOLD | **RULED** — retry-for-check-only, hash-identical objective + same units + unexpired approval, bounded DEFAULT 3, receipted attempts, re-runs every gate from failed stage forward. | `services.dap_lifecycle.retry_service` |
| Q2 Standing approval for Download | HARD HOLD | **RULED** — must name units AND operation, Connect approval never covers Download, redaction runs per release regardless. | `services.dap_lifecycle.approval_service.check_standing_approval_covers_operation` + `redaction_gate_runs_per_release` |
| Q3 Partial release | HARD HOLD | **STAYS HARD HOLD** — all-or-nothing default, TC-RET-16 stays held. | `services.dap_lifecycle.fail_closed.q3_partial_release` |
| Q4 Spend-ceiling breach | HARD HOLD | **RULED** — folds into `In Approval` reason line, one approval state not two. | `services.dap_lifecycle.fail_closed.q4_spend_ceiling_breach` |
| Q5 Suspension from Ready | HARD HOLD | **RULED** — output held in escrow on suspension, `Ready` on lift, termination = receipted Ledger event retaining artefact hash. | `services.dap_lifecycle.escrow` |
| Q6 Owner turnaround line | HARD HOLD | **STAYS HARD HOLD** — "Waited N days" line stays OMITTED. | `services.dap_lifecycle.fail_closed.Q6_OWNER_TURNAROUND_LINE_ENABLED=False` |
| Q7 Non-gate execution fault | HARD HOLD | **RULED** — `Interrupted (platform fault)` new non-terminal state, bounded auto-retry DEFAULT 3, exhaustion → `Blocked·check`, visible on surface throughout. | `services.dap_lifecycle.interrupted_service` |
| Q8 Destination removal | DEFAULT-class pending | **RATIFIED** (pending full ruling) — destination removal blocks future use only, historical receipts untouched (DAP-26 analogy). | `services.dap_lifecycle.fail_closed.apply_destination_removal` · `Q8_RATIFICATION_STATUS="ratified_pending_full_ruling"` |

**Additional new build items landed** (owner R-78):
- `Expired` state offers action `submit_again_as_new_request` (never a reopen) — `services.dap_lifecycle.expired_action`.
- Suspension notices to org admin + affected submitters only — `services.dap_lifecycle.suspension_notices`.
- DAP-15 14-day expiry with working-day roll-forward RATIFIED DEFAULT-class (closes "no duration stated" finding).

**Standing bounds unchanged**: zero push · terminal pytest only · no testing_agent · additive-only §3.8 · §4.1 §E · §4.1 §F sha-pinning discipline · three-repo discipline · ratchet monotonic (floor **5600** · never rebaselined silently).
