# extraction_request_approval_journey · citation extract

**Source manifest**: `phase0/credential_drop_manifests/20260920T1140Z_owner_drops_manifest.json` (drop_id `20260920T1140Z`)
**Custody**: `custody/owner_drops/20260920T1140Z/extraction_request_approval_journey.md` (sha256 `a7485f060882ce4c2a4750a148b3eac34b4643d2b88f46f1e09ddbff8a139361` · 73,017 bytes · 468 lines)
**Role**: binding journey specification (extraction request approval flow · atomic-extraction subject)
**Citation form**: `extraction_request_approval_journey.md · §<section-num> · L<line>`

This extract is a citation index. Bodies are the authoritative document; this file exists so tests can cite exact line anchors without re-reading the whole doc.

## Section map

| § | Title | Line | Notes |
|---|---|---|---|
| 1 | (implicit intro · purpose) | 1 | "Governed extraction exists so that a requesting party can get the data, model, or skill it actually needs from the data owner — without ever gaining unmediated access to the estate…" |
| 2 | Ground rules / states set | 25–30 | State-machine terminals, DAP-15 refusal vs Expired, Blocked 3 kinds |
| 3 | Post-submission compose reset + toast + inline note | 47–50 | Submission toast copy verbatim; failure = no toast |
| 4 | State card grammar (page rail) | 55–60 | Approved→Executing immediately (no waiting-to-start bucket); Retrieved re-openable per mode |
| 5 | State diagram (Mermaid) | 70–91 | E{Decision made before 14-day window closes?} + Refused/Approved/Expired branches |
| 6 | Page rail vs. module landing page | 110 | (Design-side · not lifecycle) |
| 7 | Progress rendering (percentage vs step indicator) | 149–150 | Retrieval action verbs per mode |
| 9 | Rail visual grammar | 200–226 | Declined→Refused rename; timestamp discipline; stat card set final = 8 |
| 10 | Open Questions | 235–255 | 8 questions banked; L247 Q7 verbatim; L252 Q8 verbatim |
| 11 | Drawer specifications per status | 256–end | Sign-off drawer block; Refused/In Approval/Executing/Blocked/Ready/Retrieved drawer contents |

## Buildable-now spine · line-anchored citations

### State machine (Phase 2 test 1)

- **L27**: "A request that receives no decision within 14 calendar days of submission expires unexecuted — silence is never treated as approval (DAP-15). If the 14th day falls on a day the data owner doesn't work, the deadline rolls forward to their next working day (never earlier). The deadline is computed and returned by the backend as `window_ends_at`; the front end never does the date arithmetic itself."
- **L25**: "The instant a request is approved, it moves directly into `Executing` — there is no separate 'waiting to start' bucket. The approval event is still stamped with who approved it and when in the platform's record, but it isn't a stat card on its own — and the approver's name is never shown to the party (see §11, Sign-off)."
- **L26**: "A decision (approved or declined) is permanent and recorded against the request. It cannot be reopened, appealed, or edited from this view."
- **L55**: "**Approved** — moves immediately into **Executing**. […] The approval is stamped in the record with who approved it and when; the party sees the date and the approver's role, never the name."
- **L56**: "**Refused** — stops permanently. The reason is recorded and visible. A new request needs a fresh submission."
- **L57**: "**Expired** — no decision before the 14-day review window closes. Distinct from Refused: nobody said no."
- **L58**: "**Blocked** (only if a gate stops the request) — a gate refuses it, either because of something about the request or a check that couldn't complete (§2). The party sees where it stopped, which kind, a plain-language reason (except for an estate-level budget block, where nothing is disclosed — DAP-35), a reference to quote when following up, and the unchanged sign-off record. A new request needs a fresh submission."
- **L60**: "**Retrieved** — the party retrieves it: opens the report, or downloads the model, skill, or data package. The request is now closed out on this rail; it still counts toward `Total`. Retrieval is not one-shot for every mode: a report stays openable indefinitely with no new receipt, and a model, skill, or data package can be downloaded again — each repeat is its own metered event with its own receipt (DAP-21), never a silent re-pull."
- **L91**: "*(A suspension-triggered block, DAP-27, is terminal wherever it lands — In Approval, Executing, or Ready — and doesn't resume when the suspension lifts; the party submits fresh. Simplified above as three edges into the same `Blocked` node rather than three separate outcomes.)*" → informs DAP-LIFECYCLE-Q5 HARD HOLD placement
- **L219**: "**The 14-day review window is fixed, not still open.** Calendar days from submission, not working days […] If the 14th day lands on a day the owner doesn't work, the deadline rolls forward (never earlier) to their next working day. The window is computed and returned by the backend as `window_ends_at`; nothing about the roll-forward is explained to the party — they see only the resulting date."

### DAP-15 timer discipline (Phase 2 test 2 · corrected per owner)

- Timer runs **from submission to decision**, not to retrieval.
- Correct transition: **In Approval → Expired** when no decision landed within 14 calendar days of submission.
- Silence ≠ approval.
- No separate Ready→Expired rule in this document. (If found in another spec, cite separately.)

### Identity discipline (Phase 2 test 3 · owner-added invariant)

- **L25** + **L212**: "The approver's name is never shown to the party. In Approval already hides who is reviewing; approval and refusal show the date and the role ('the records authority at {{ dataOwner }}'), or the data owner alone when no role is named. The name stays in the platform's record. No initials or partial names."
- **L36**: "The individual user who submitted, and who retrieved, is shown — the opposite of the approver-name rule, and deliberately so."
- **L228**: "Individual user identity now appears on two things it didn't before: who submitted, and who retrieved. Deliberately asymmetric with the approver-name rule…"
- **L26** + **L272**: decisions permanent · no reopen · fixed permanence line: "This decision is final and can't be reopened here. A new request needs a fresh submission."
- Drawer identity rules cross-referenced at L264, L285, L307, L330, L357, L382 (each drawer states submitter name; none states approver name).

### Blocked 3-kind + DAP-28 gate discipline (Phase 2 test 4)

- **L30**: "Two kinds, and the drawer states which: `request` (the request itself won't pass this gate — resubmitting it unchanged is blocked again) and `check` (a gate couldn't complete for reasons unrelated to the request). The approval stamp survives either way. No Retry exists until retry semantics are decided (see Open Questions). A block caused by the estate's own release budget is a third kind, `estate` — see §11; its reason is deliberately uninformative, since DAP-35 prohibits disclosing anything about the estate's remaining budget."
- **L201**: "`Blocked` has three kinds, not one flat state: `request`, `check`, `estate`."
- **L103** (rail table): "Three kinds: `request`, `check`, `estate`."

### Retrieval → MeteredEvent wiring (Phase 2 test 5)

- **L60**: each retrieval → its own MeteredEvent + receipt (DAP-21). Never a silent re-pull.
- **L149**: retrieval verb mode-specific (Open report / Download model / Download skill / Download data). Flip to `Retrieved` **only on verified checksum match**.
- **L150**: `Retrieved` cards keep an action for 3 of 4 modes. Re-download = new metered event + new receipt.
- **L397**: toast on completion — "Downloaded — FTN-2026-0120" / "Report opened — FTN-2026-0111"; never on confirm, never on start, never on failure.
- **L408**: Get Intelligence — reading again is never a new event, never a new receipt.
- **L411**: repeat completion also toasts.

### Notification event-emission surface (Phase 2/3 test 6 · added per owner)

- **L47**: persistent inline note on submission: "Submitted as FTN-2026-0121 — waiting for sign-off. Expires 3 Oct 2026 if no decision is made." (or "— running now" for skips-approval).
- **L48**: toast on submission: "Submitted FTN-2026-0121 — waiting for sign-off" / "— running now" · 6 seconds · dismissible · pauses on hover · "View" action.
- **L50**: on failure — no toast, no reset, no rail insert, inline error.
- **L225**: toast fires on retrieval completion (specified in §11).
- **L49**: `Ready` and `Retrieved` transitions later in the journey also emit toasts.
- **Email**: not in scope on this journey · owner directive verbatim (this-session): "Org-admin status emails — submitter-only remains the current rule per owner directive verbatim (product decision · nothing blocked)". Backend email surface = stub/queue behind flag OFF (DEFAULT-class, already banked at Q register).

## §10 Open Questions verbatim anchors

- **L235**: cluster header — "Open Questions"
- **L243**: contextual line on Blocked-reason authorship (backend records plain-language text at time of block for kinds `request`/`check`; `estate` reason is fixed uninformative copy)
- **L247**: Q7 verbatim — "Does a non-gate execution fault exist as its own state?"
- **L249**: DAP-LIFECYCLE-Q4 context — "A spend check (DAP-23) that would exceed the party's own ceiling routes to a person, and this rail has no state for that wait. It isn't `In Approval` (no controlled-data question), and it isn't `Blocked` (nothing was refused). Provisionally the cheapest fit is folding it into `In Approval` with its own reason line, but this hasn't been designed — no drawer content, no distinct copy, no confirmation the 14-day window even applies to it the same way."
- **L252**: Q8 verbatim — "Whether removing a registered delivery destination (see `party_admission_journey.md`, §6) should cause the 'Delivered to X' line on a historical `Retrieved` drawer to change is answered there (no — future-only) by analogy to DAP-26, not by direct citation. If that answer changes, every `Retrieved` drawer showing a destination needs revisiting."

## §11 drawer specifications · state-scoped anchors

- **L256**: "The drawer opens per-request from any card's 'View more' link. Every status now has a specified drawer: `Refused`, `In Approval`, `Executing`, `Blocked`, `Expired`, `Ready`, `Retrieved`. Common to every status: the header pattern, a **Your request** block first, and a **Before you submitted** block last."
- **L214**: Sign-off drawer block persists across Executing/Blocked/Ready/Retrieved (approval stamp survives Blocked).
- **L220**: Expired/Refused/Blocked have no separate Sign-off block · the status block itself carries it.
- **L427–end**: Sign-off block · three branches (named authority · office · bypass).

## Standing bounds preserved

zero push · terminal pytest only · no testing_agent · additive-only §3.8 · SO §4.1 §F sha-pinning discipline (this note is not a spec · citations only).
