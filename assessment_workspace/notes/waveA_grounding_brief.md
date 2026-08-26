# Wave A Grounding Brief · Verbatim Requirements Only · 2026-08-26

Owner Condition 1 (2026-08-26): "Every requirement you implement must be built from the VERBATIM spec text, and the verbatim quote (doc + § + exact words) must appear in the gating test's docstring and the drill receipt. If the quote isn't in the test, the test doesn't gate the row."

Owner Condition 2 (2026-08-26): after any compaction, re-read this brief before touching Wave A code.

This brief carries VERBATIM quotes only. No paraphrase. No summary. Where I break structure with `[…]`, that's whitespace elision inside a paragraph; every word between `«»` marks is verbatim from disk. Citations point to the file, section header, and quoted line-count for reproducibility.

---

## R1 · Ship-Manifest & Callers-Cover-the-Rule DoDs (already GREEN, awaiting commit)

Owner ruling text (2026-08-26 owner message · verbatim):

> «Ship-Manifest DoD: a row is DONE only if runtime-assembler wiring (`pod_shell/backend/server.py` AND its /app mirror), frontend route/component in `pod_shell/frontend/`, and a green user-path test land in ONE commit. Write a meta-invariant test that enumerates every `services/*/router.py` + `routers/*.py` and asserts each is either (a) included in the runtime assembler or (b) explicitly listed in a `KNOWN_UNWIRED` manifest with a register row citing why. Also assert /app runtime files match pod_shell (no more out-of-band drift).»
>
> «Callers-Cover-the-Rule DoD: for every "every X does Y" register row, DONE requires a producer-side test proving Y fires. Record both DoDs in STATE/DECISIONS.md as owner rulings.»

Enforcement code: `backend/tests/invariants/test_ship_manifest_dod.py` (8 tests, GREEN).

---

## R2 · Fix ConnectDrawerChat: stale-closure bug + human-speak error translation

Owner directive verbatim (2026-08-26 message):

> «R2: fix ConnectDrawerChat — (a) the stale-closure runSubmit bug (confirm must reference server-side draft state, not a captured null), (b) errDetailToString replaced with a human-speak translation layer (raw Pydantic 422 shapes never reach the user; each failure names the field and the remedy in plain words). Tests-first: pytest parse→confirm→submit roundtrip + node --test for the error rendering. This must pass the owner's exact repro: paste akki-vm notes → confirm → clean submit path (or the honest publickey narration), never "String should have at least 1 character."»

Spec anchor for the human-speak grammar (Canon 5 §9.2 verbatim, `Akki_Canon_5_Interface_Architecture.txt` lines 130–140):

> «Not to the standard you asked for.
>
> Accept as recorded statement · Narrow the objective · Lower the standard
>
> A refusal is the system keeping its promise.»
>
> «The title, the three actions, and the footer are binding copy, reproduced verbatim wherever this card renders. They are never paraphrased, shortened, or restyled for a particular surface.»

Spec anchor for "failure is a first-class outcome" (STATE/DECISIONS.md 2026-08-14 fixture ruling verbatim):

> «FL-P2-12 CLOSED "Wizard-not-form" rendering decision. Connect is a right-hand drawer holding a conversation, not a form. Four suggestion chips; free-text input; branch-by-what; failure is a first-class outcome; success ends the conversation with a single Close and a toast.»

---

## R3 · Wizard rebase on Canon 5 §14 + §15 + Canon 6 §6 + SOLVA.md §5.2/§5.6 + edit-in-place

### R3.a · Canon 5 §14 verbatim ("Commission — The Shaping Wizard")

Source: `canon/text/Akki_Canon_5_Interface_Architecture.txt` lines 191–197.

> «14  Commission — The Shaping Wizard
>
> Layout: a chat pane on one side, an objective draft rail on the other.
>
> Chat. The operator states intent; the agent asks for mandatory fields and never proposes on them. An estate-check chip renders inline before any feasibility-dependent question is asked.
>
> Draft rail. Three dimensions — entry, reach, output — plus the envelope, each field in one of three visual states: filled with a check, open and muted, or agent-assumed with the amber chip. The envelope line lists done-condition, budget, and lawful basis until each is supplied.
>
> Sample action. Run a sample becomes available once reach is drafted.
>
> Mandatory fields — reach, the four output fields, done-condition, budget, lawful basis — are asked, never pre-filled. Preference fields may carry agent recommendations, but the mandatory set never does. Every turn is grounded in a real estate read; no fabricated availability, ever, under any circumstance.»

### R3.b · Canon 5 §15 verbatim ("Freeze — Commit Review")

Source: `canon/text/Akki_Canon_5_Interface_Architecture.txt` lines 198–206.

> «15  Freeze — Commit Review
>
> You supplied. Rows of operator-stated values.
>
> Agent assumed. Rows headed "Agent assumed — confirm or change," each carrying the amber chip and a change link.
>
> Feasibility verdict. A success-treatment card. Binding pattern: "Floor feasible — {n}% of in-scope estate meets your standard."
>
> Grounding marker. States whether the objective was sample-grounded or estimate-grounded.
> Grounded by sample {sample_ref}   ·   No sample run — estimates only.
>
> Envelope line. Lawful-basis reference, budget, commissioner, and the scope ceiling respected.
>
> Action. Freeze objective.
>
> Frozen is immutable — a changed intent is a new objective.»

### R3.c · Canon 5 §9.3 verbatim ("The agent-assumed chip")

Source: `canon/text/Akki_Canon_5_Interface_Architecture.txt` lines 141–144.

> «9.3  The agent-assumed chip
>
> Agent assumed — confirm or change
>
> Amber, 11px label weight, attached to any field an agent filled rather than the person. It survives to the commit review unchanged — a value that was agent-assumed at draft time is never quietly reclassified as user-supplied by the act of confirming the screen it appears on.»

### R3.d · Canon 6 §6 verbatim (five-step commissioning)

Source: `canon/text/Akki_Canon_6_User_Journeys.txt` line 61.

> «The objective wizard — the Extraction Console's Commission screen, Document 5 §14 — turns a need into governed work in five steps: the need stated in plain words; scope selected from what the registry says actually exists; standards and rights confirmed against explained defaults; a plan preview — extraction volume as a range, reusable stock already identified, expected coverage of the goal, and what cannot be covered, all shown before any commitment; and commissioning itself, with a confirmation stating precisely what becomes permanent at that moment.»

### R3.e · SOLVA.md §5.1 verbatim (six states, one-question-at-a-time)

Source: `repos/Akki-Executive-Core/memory/briefs/SOLVA.md` lines 359–365.

> «Every Solva session moves through six states:
>
> - Entry. The user lands on the Solva menu item or is auto-activated into Simulate Hypothesis. Sub-module is selected.
> - Framing. The system explains what the sub-module does in two sentences. The user enters initial framing.
> - Layer 0 (silent). The frame audit runs. 1–3 second pause. No user-facing screen. Transitions directly to Layer 1 with the tuned opening question.
> - Layers 1 and 2. Up to four questions per layer. One question at a time with progress indication. Material attachment available at any question.
> - Layer 3. Synthesis prepared ("Let me put this together") and rendered. User reviews; can request clarification of any element via citation; can return to earlier layers if framing was off.
> - Layer 4. Three reflection questions, one at a time. Session marked complete on submission and saved to history.»

### R3.f · SOLVA.md §5.2 verbatim (the coach voice)

Source: `repos/Akki-Executive-Core/memory/briefs/SOLVA.md` lines 366–371.

> «5.2 The coach voice
>
> Solva has one user-facing voice — the coach. Empathetic, restrained, conversational. Informed by every reasoning model but surfaces none of them as content. Four rules govern it:
>
> - Explain before asking. Each layer opens with a one-sentence explanation of what is about to happen and why.
> - Acknowledge before pushing. If the user has provided a framing, the system reflects what it has heard before asking the next question. One sentence.
> - Restrain in synthesis. Layer 3 output uses editorial cadence — short sentences, one idea per line, white space.
> - Speak in one voice — the coach's. The audit is preparation, not content. No reasoning model output renders to the user as audit language.»

### R3.g · SOLVA.md §5.6 verbatim (answer surfaces)

Source: `repos/Akki-Executive-Core/memory/briefs/SOLVA.md` lines 396–400.

> «5.6 Answer surfaces
>
> - Open text — generous textarea, no character limit, file attachment and Akki document reference inline
> - Single-select with text fallback — when the question benefits from a constrained answer, 4–6 options plus an "Other — describe" text field
> - Multi-select with weighting — when asking the user to weight several factors, 4–6 options with simple weighting. Used sparingly.
>
> One question at a time. One answer surface at a time. Clear progression indication.»

### R3.h · Owner directive verbatim (2026-08-26)

> «R3: wizard rebase on the spec verbatim — Canon 5 §14 (amber chip, "Agent assumed — confirm or change" rows, mandatory fields [reach, four output fields, done-condition, budget, lawful basis] ASKED never pre-filled/proposed, every turn grounded in a real estate read), Canon 5 §15 freeze grammar (frozen is immutable, changed intent = new objective), Canon 6 §6 five steps, SOLVA.md §5.2/§5.6 coach-voice (explain before asking, acknowledge before pushing, one question at a time, progress indication), edit-in-place. USE the four lifted contracts (wizard_commit_state, operator_turn, agent_assumption, committed_value) — diff them field-by-field against Akki-OS-V1 canonical shapes first (the audit gap you flagged). Where the 2026-08-14 Simplification Ruling conflicts with Canon 5 §14, Canon 5 wins — the owner's current directive supersedes; note that supersession in DECISIONS.md.»

Note: the Canon-5-supersedes-Simplification-Ruling note was recorded in DECISIONS.md as part of the R1 ruling section (uncommitted at freeze; will land with R1 commit).

---

## R4 · Reachability repair (Ship-Manifest DoD, one commit per item)

Owner directive verbatim (2026-08-26):

> «R4: reachability repair — wire into the RUNTIME assembler under the new DoD, one commit per item: callable skills (+ /api/callable_skill/*), handoff, memory, whitepaper HTTP surface, N-series breach/erasure routers, opportunity-briefs endpoint calls the generator/selector pipeline, Critic Seam producer wiring (pick the real worker outputs — at minimum chat/solva answer path and whitepaper drafts — and route them through run_critic_pass/manifest_gate with producer tests), and commit the CP3 training wiring (server include + App.js route + Training.jsx) properly to pod_shell in the repo.»

Canon anchors for the 10 items:

- **Callable Skills**: Doc 18 (see grounding docs at `canon/text/Akki_Doc_18_*` — verbatim quotes to be pulled at R4.item-1 open).
- **Handoff**: Doc 15-086 CA1-009 (spec text at `canon/text/Akki_Canon_5_Addendum.txt` / register row).
- **Memory**: Doc 08 memory plane (Canon 4 §17 + Canon 2 §5).
- **Whitepaper HTTP surface**: Doc 14-024 CA1-005.
- **N-series breach/erasure**: Doc 15 §N2/§N3.
- **Opportunity briefs pipeline**: Doc 10-006.
- **Critic Seam producer wiring**: Doc 19A-005 verbatim: «every worker output passes through the Critic Seam; shipped-without-seam is a defect». (Full quote to be pulled at R4.item-7 open.)
- **CP3 training wiring**: register rows Doc17-005/011; runtime code already present in /app runtime — R4 just commits it to pod_shell.

Each item lands under Ship-Manifest DoD (R1): runtime include + frontend + green user-path test in ONE commit.

---

## R5 · RefusalCard.js verbatim lift from RMS/OS-V1

Owner directive verbatim (2026-08-26):

> «R5: lift RefusalCard.js verbatim from RMS/OS-V1 into pod_shell/frontend/src/components/, wire every refusal surface (chat, connect, training seal refusal, solva) through it per Canon 5 §9.2 binding-copy card.»

Canon 5 §9.2 already quoted above (R2 anchor).

RefusalCard.js source will be located in either `repos/Akki-OS-V1/` or `repos/RMS-IQ-Core-2/` — will be located at R5 open via grep. Lift is VERBATIM copy of the component file + wire calls at every refusal surface.

---

## R6 · Register truth pass

Owner directive verbatim (2026-08-26):

> «R6: register truth pass — for each of the 10 STATUS-INFLATED rows: land wiring under DoD or downgrade with receipt. Then recompute the composite under the lock, authoritative, even if it drops. Also resolve your flagged residuals: CostLedger five-lever sequence text check + the wizard contracts field diff.»

The 10 STATUS-INFLATED rows are named in `notes/audit_2026-08-26/system_wide_spec_build_audit.md` §16 (already committed to workspace `master` HEAD `743046a`):

1. Wizard / Connect Chat (Canon 5 §14 grammar not honoured by W1 delivery) — resolved by R3.
2. CP3 Training plane repo/runtime drift — resolved by R4.
3. CP2 Critic Seam orphaned — resolved by R4 item 7.
4. Doc 18 Callable Skill Files unreachable-on-pod — resolved by R4 item 1.
5. Doc 10-006 Opportunity Briefs mechanism unused by endpoint — resolved by R4 item 6.
6. Doc 15-086 Handoff contract legacy-only wiring — resolved by R4 item 2.
7. Doc 16-014 Refusal card DONE conflates donor with pod — resolved by R5.
8. Doc 04-014 Structured refusal card same failure — resolved by R5.
9. Watch/GreyMirror CP8 surface routers wired without producers — resolved by R7 (Wave A) + Wave C.
10. Doc 08 Memory router legacy-only wiring — resolved by R4 item 3.

R6 verifies each resolution landed via DoD tests + recomputes composite %.

---

## R7 · Watch/Grey-Mirror honesty (Wave A first pass)

Owner directive verbatim (2026-08-26):

> «R7: Watch/Grey-Mirror honesty — wire existing producers (watch containment/fitness/mirage/witness/continuity) to fire from drills and real events so /watch and /grey-mirror read REAL records; any mechanism genuinely unbuilt renders an explicit "mechanism not yet built — register row Doc03-xxx BUILD" state in the UI instead of a silent empty panel.»

Canon 3 verbatim anchors for the Watch mechanism (source: `canon/text/Akki_Canon_3_Governance.txt` — quotes to be pulled at R7 open, one per producer):

- Doc03-014 (bait: touch = certainty, not suspicion) — verbatim quote to be pulled.
- Doc03-030 (containment ladder Noted/Friction/Contained/Held) — verbatim quote to be pulled.
- Doc03-055 (Suspect works inside quarantine copy) — verbatim quote to be pulled.
- Doc03-078 (Watch exempt · external witness signs) — verbatim quote to be pulled.

Wave A R7 scope: wire producers + explicit MISSING state UI. Wave C is the full mechanism build.

---

## Standing rules (from owner 2026-08-26)

- Both DoDs from R1 in force on every commit.
- Tests-first red/green receipts banked at `phase0/drill_receipts/`.
- Local commits only, NO push.
- No secrets echoed in stdout, tool logs, or commit messages.
- pydantic 2.13.4.
- Single chokepoint.
- REFERENCE-NOT-COPY.
- N-series / A17.12-17 / A18.8 / EP-4 / Doc14-020 remain open config slots, never blockers.
- External verification is the owner's at each wave close — make sure the pod stays runnable.

