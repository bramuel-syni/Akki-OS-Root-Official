# System-Wide Spec↔Build Audit · 2026-08-26

Owner directive: expand from the wizard spec-hunt to a system-wide audit. Verdict grammar:
FAITHFUL · DIVERGED · PARTIAL · MISSING · UNSPECED-ADDITION · STATUS-INFLATED. Every claim
below is sourced from files opened this session under `/app/assessment_workspace/repos/Extraction-Akki`
(`programme/track-a` HEAD `d763721`), the pod runtime at `/app/backend` + `/app/frontend`, and
`STATE/DECISIONS.md`.

This is a mirror of the chat-side audit delivered 2026-08-26. See the chat transcript for
the full narrative version. This note preserves the audit for the record and for
cross-referencing during remediation.

## §0 · Framing correction the owner is right about

Two structural facts came out first because everything below depends on them:

1. **The repo has TWO backends and TWO frontends.** `backend/` + `frontend/` (legacy V4 shell)
   and `pod_shell/backend/` + `pod_shell/frontend/` (new v7-oracle shell). The pod runtime
   `/app/backend` is a nearly-verbatim mirror of `pod_shell/backend/server.py`, with the sole
   difference being **two extra lines wiring `services/training/router`** (CP3). The pod runtime
   `/app/frontend` mirrors `pod_shell/frontend/`, plus an extra `Training.jsx` component and
   `/training` route. **`git show a85774a` (CP3) never committed the `pod_shell/backend/server.py`
   include, the `pod_shell/frontend/src/App.js` route, or the `Training.jsx` component. The commit
   is functionally incomplete against the repo — CP3 works only because the pod runtime was edited
   out-of-band.**
2. **`server.py` (the assembler) is the ground truth of what is reachable**, not the presence
   of a `router.py` file under `services/`. Multiple services on disk (`training`, `critic_pass`,
   `whitepapers`, `skill_files`, `n_series`, `opportunity_briefs` generator/selector,
   `outer_gate`) are never imported by ANY wired assembler.

## §1..§16 · By-canon findings

See chat transcript 2026-08-26 for the section-by-section breakdown across:
- Canon 1–2 (Docs 01–02, custody / chokepoint)
- Canon 3 + Canon 8 (Doc 03, Watch / Grey Mirror)
- Canon 4 §1–§9 (Doc 04, Solver / grounding)
- Canon 4 §10–§14 (Doc 05, Northena)
- Canon 4 §15 (Doc 06, progressive disclosure)
- Canon 2 §4 + Canon 4 §16 (Doc 07, five-ring / shrinkage)
- Canon 2 §5 + Canon 4 §17 (Doc 08, memory & retrieval)
- Docs 09–10 (Registry + Connect)
- Docs 11–12 (Cost & Compute)
- Docs 13–14 (Targeta + Model Ecosystem)
- Doc 15 (governance ceremony + N-series)
- Doc 16 (cross-cutting)
- Docs 17–19 (CP2/CP3/CP4/CP7)
- The Objective / Shaping / Connect Wizard (owner's original probe)
- Root-cause honesty (10 concrete instances of the same failure class)

## §16 · Root-cause honesty · specific occasions where paraphrase-not-spec cost time

The ten concrete instances (numbered as delivered in chat):

1. **The wizard / Connect Chat**: Canon 5 §14–16 verbatim + Canon 6 §6 five-step + STATE/DECISIONS
   2026-08-14 fixture + Simplification + T12 exist ON DISK, but the W1 close ran only against the
   T12 sentence ("conversational paste-assist drawer chat"), not the full Canon 5 §14 grammar
   (amber chips, agent-assumed rows, ask-not-propose, edit-in-place). Four LIFTed contracts
   (`contracts/wizard_commit_state.py`, `operator_turn.py`, `agent_assumption.py`,
   `committed_value.py`) sit unused.
2. **CP3 Training plane**: commit `a85774a` did not touch `pod_shell/backend/server.py` or
   `pod_shell/frontend/src/App.js` or commit `Training.jsx`. Runtime works via out-of-band edits.
3. **CP2 Critic Seam LIFT**: 950 LOC + 27/27 tests green, but no worker output calls
   `run_critic_pass()` anywhere in the codebase outside its own tests. Doc19A-005 vacuous.
4. **Doc18 Callable Skill Files**: register marks DONE — but wiring is in legacy
   `backend/server.py:155`, not runtime `pod_shell/backend/server.py`. On the pod,
   `/api/callable_skill/*` returns 404.
5. **Doc10-006 Opportunity Briefs**: mechanism exists as sophisticated code; the actual
   `/api/registry/opportunity_briefs` endpoint queries Mongo without calling the mechanism.
6. **Doc15-086 Handoff contract**: wired in legacy backend only; unreachable on pod.
7. **Doc16-014 Refusal card DONE**: refers to `RefusalCard.js` in RMS/OS-V1 — never lifted into
   Extraction-Akki's `pod_shell/frontend/src/components/`.
8. **Doc04-014 (structured refusal Evidence/Coverage/Contradiction)**: same as #7.
9. **Watch/GreyMirror surface routers wired at CP8**: routers read from `phase0/` JSON dirs that
   are mostly empty; mechanism modules exist but no producer fires them.
10. **Memory router (Doc 08 REUSABLE)**: `routers/memory.py` wired in legacy assembler only; on
    the running pod, `/api/memory/*` is unreachable.

**Common thread**: verdicts entered against partial artifact evidence (LIFT source ratified,
tests green, receipts banked) without verifying the artifact was reachable through the runtime
user path. The register is not lying about what was built; it is lying about what is shipped.

## §17 · Counts per verdict (approximate)

- FAITHFUL: ~12
- PARTIAL: ~14
- DIVERGED: 4
- MISSING: ~40
- UNSPECED-ADDITION: ~6
- STATUS-INFLATED: 10 specifically named

## §18 · Top 10 divergences by owner impact

1. CP3 Training plane repo/runtime drift.
2. Doc18 Callable Skill Files unreachable on pod.
3. CP2 Critic Seam orphaned.
4. Connect Chat P0 stale-closure bug + Pydantic passthrough.
5. Canon 5 §14 wizard grammar not honored by W1 delivery.
6. `RefusalCard.jsx` not lifted.
7. Watch/GreyMirror = readers over near-empty dirs.
8. Doc15-086 Handoff contract unreachable on pod.
9. Memory router unreachable on pod.
10. `services/opportunity_briefs/` mechanism unused by the endpoint that lists briefs.

## §19 · Corrected seasoned state-of-the-build

**What genuinely works, end-to-end, from the browser through the runtime pod today**: Registry
three-tab landing + real facts; Connect drawer chat paste→submit for Compute/Data-source/Non-
compute; RDS Data API live to DigiCow; Compute reflection-before-commit; Chat surface via
chokepoint; Cost Ledger surface; Model Ecosystem MOAC six-criterion; Governance state + write
path; ThinkLab admit/gate/converge + Solva; Data Shield; Retention dry-run/apply; IP allowlist
gate; Training plane (pod only, not repo).

**What does not work / is not shipped, despite disk presence**: Watch mechanism; Grey Mirror
mechanism; Critic Seam gating; Callable Skill Files on pod; Handoff contract on pod; Memory
router on pod; Whitepaper draft surface; Skill Files provenance chain; N-series breach + erasure;
Opportunity brief generation pipeline; Refusal card component; Walk-this; Wizard amber chip +
agent-assumed rows + five-step + edit-in-place + coach voice + human-speak error translation;
Solva five-layer reasoning journey.

## §20 · Recommended remediation order (owner rules)

1. Ratify a Ship-Manifest DoD: no row moves to DONE unless the router is wired in the runtime
   assembler AND the frontend route/component exists in `pod_shell/frontend/` AND a green test
   asserts the user-visible path — all in ONE commit.
2. Ratify a "Callers Cover the Rule" DoD: for any row naming a rule "every X does Y", no DONE
   until at least one producer's tests assert Y fires for X.
3. Wizard rebase on Canon 5 §14 + Canon 6 §6 + SOLVA.md §5.2/5.6; fix P0 closure bug + Pydantic
   translation.
4. RefusalCard lift + wire every refusal surface through it.
5. Register cleanup: land the missing wiring for the ten inflated rows OR downgrade with a receipt.
   Recompute composite under lock.
6. Watch/GreyMirror mechanism decision: build the producers OR retire the `/watch` + `/grey-mirror`
   routes.
7. P1 frontend brief compliance table only after 1–5.

---

STOP-AND-REPORT · awaiting owner ruling on the audit before P0/P1 code writes resume.
