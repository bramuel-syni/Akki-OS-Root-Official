# R-91 verbatim retrieval receipt · answering owner's direct question

**Retrieval instant:** 2026-09-22T06:15:23Z (verified via `date -u -Iseconds`).
**Retriever:** main-agent desk under Standing Order §6 autopilot.
**Purpose:** owner's directive verbatim: *"the owner asked directly: 'who set up the R-91 rule? what objective is it serving?' … quote VERBATIM from DECISIONS.md (and any linked note) the R-91 entry — its full text, timestamp, who authored/ratified it (owner directive vs agent proposal), why the horizon value 2026-09-23T03:23:15Z was chosen, and what the 5 mirror-drift annotations were."*
**Provenance:** every quote below traces to `STATE/DECISIONS.md` line-numbered anchor at retrieval instant. No summary, no paraphrase in the quote blocks — only the frame text is retrieval-agent.

Owner supersede ruling **relayed to this desk after this retrieval was drafted** (2026-09-22T~06:12Z, this session) has retired R-91's TIMER while preserving the WHAT. The record below documents WHAT the owner has just superseded; the paired supersede entry banks at `STATE/DECISIONS.md` next-append (R-101 · same turn as this retrieval).

---

## 1 · R-91 origin — Ruling 1 · R-86 schedule (2026-09-20T~19:00Z · owner directive)

R-91 was *scheduled* — not opened as a wave — by the owner at 2026-09-20T~19:00Z. The ceremony did not yet exist; the R-91 slot was fixed by owner as the closure wave for the App.js divergence.

**Anchor:** `STATE/DECISIONS.md:20571`, `20589`, `20668`, `20719`, `20721` (Ruling 1 · R-86 · v5 SRR sheets ratification banking).

> "Sequencing confirmed: R-86 (mid-flight) → R-87 vocabulary correction → R-88 Content Registry wave → G5-v5 (SFP-1..7 first slice) → CP-APP-JS-UNIFY at your proposed R-91 slot (owner accepted scheduling-not-open-ended; confirm the slot in the R-86 seal report). Standing bounds unchanged. Proceed."
> — Owner verbatim, banked at `STATE/DECISIONS.md:20589` (banking sha `1250c39a`)

> "Per Ruling 1(b): CP-APP-JS-UNIFY scheduled at **slot R-91**. Owner accepted scheduling-not-open-ended at prior banking (`1250c39a`) via verbatim: *"CP-APP-JS-UNIFY at your proposed R-91 slot (owner accepted scheduling-not-open-ended; confirm the slot in the R-86 seal report)."* This seal-report confirms it."
> — Banked at `STATE/DECISIONS.md:20721` (R-86 Commit-B state master seal report)

**Attribution:** slot proposed by agent, ratified by owner directive. Not agent unilateral.

---

## 2 · R-91 CEREMONY-OPEN — Path ε ratified (2026-09-21T03:23:15Z · owner directive verbatim)

The CEREMONY-OPEN (not a wave open — a rule-change ceremony per Canon 3 §24, ordinary tier, 48-hour countdown) was filed at `2026-09-21T03:23:15Z` in response to the owner's Path ε ratification. The horizon-value 2026-09-23T03:23:15Z is exactly proposal-filing timestamp + 48 hours per the ordinary tier of the rule-change ceremony.

**Anchor:** `STATE/DECISIONS.md:22213–22340` (R-91 CEREMONY-OPEN entry, single ## heading, full body). Quoted verbatim:

> "R-91 — PATH ε RATIFIED, via the RULE-CHANGE CEREMONY at the ordinary tier (48 hours), the same path as the GPU-staleness re-scope. Owner verbatim: 'the ceremony is the authorised way a sealed test file changes — a ceremonied amendment is not a §3.8 refactor.' Conditions, binding exactly:
> 1. Properties 2, 3, and 5 tolerate an empty annotation set ONLY when the CP_APP_JS_UNIFY card status is SEALED — accidental emptiness before closure stays RED.
> 2. The early return is a NAMED success, never a silent pass: the test output must state 'annotation set empty by ruled closure R-91' so the reason is on record every run.
> 3. Property 4 stays untouched.
> 4. The ceremony receipt cites this ruling.
> 5. On apply: retire 5/5 baselines, re-run the full sweep, seal at the new floor.
> Execute the ceremony per the GPU-staleness precedent shape exactly — including whatever notice/window mechanics the ordinary tier carries. If the ordinary tier imposes a 48-hour window before apply, do NOT idle: open the G5-v5 second slice (below) during the window and apply+seal R-91 at expiry. If the banked ceremony rules permit apply-on-owner-ruling-on-record, apply now. Follow the banked ceremony mechanics; do not invent."
> — Owner verbatim (2026-09-21T~01:00Z), banked at `STATE/DECISIONS.md:22215–22223`

**Countdown-window horizon rationale (banked verbatim at `DECISIONS.md:22233–22245`):**

> "**Ceremony type:** rule-change per Canon 3 §24 (propose → counter-sign → wait → apply). **Ordinary tier · 48-hour countdown** per R-18 effect 12.
>
> **Propose step:** filed this-turn at `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md`. Normative text §4 verbatim (see proposal §4.1-§4.6 for helper + 3 Property replacements + Property 4/1 untouched declarations).
>
> **Counter-sign step:** owner ruling this-session (2026-09-21T~01:00Z verbatim above) IS the batched counter-sign per STATE/STANDING_ORDERS.md:437 verbatim: *"ordinary-tier re-scopes that tighten (never loosen) may be proposed and countdown-started without waiting, countersign requested in the batch."* Character of amendment: TIGHTENING (accidental emptiness before closure stays RED · post-closure emptiness a named success). Not loosening. Precedent-fit at ordinary tier.
>
> **Countdown step:** starts at proposal filing timestamp `2026-09-21T03:23:15Z`. Horizon: `2026-09-23T03:23:15Z`. Apply schedule: at horizon (or later if a bridging reconcile is needed).
>
> **Apply step:** at horizon per proposal §6. Ten operations in order: (1) apply amendment verbatim, (2) re-run tests, (3) apply mirror `/app/frontend/{App.js,pages/}` → `pod_shell/frontend/{App.js,pages/}`, (4) update `baseline_failures.json` atomically (5 baselines → 0 · mirror-drift annotations 3 → 0 · v8-cascade annotations retire 2 keys retaining cp10-still-recent · counts+floor 5695 → 5700), (5) flip `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status`: SCHEDULED → SEALED, (6) regenerate `notes/ORCH_BOOT.md` ratchet block pre-Commit-A, (7) sync POD audit mirror, (8) regenerate CP10 harness if drifted, (9) BASELINE_GUARD=1 double-green byte-identical, (10) §3.3 3-Commit Seal.
>
> **Precedent shape:** CP-STALENESS-CEREMONY seal chain (2026-09-20T09:28Z Commit-A `31d414b` + Commit-B `9c0dd840` + Commit-C `23ff5808`) · rule-change apply per Canon 3 §24. Same class of change (rescoping a sealed test's floor guard to fire on live property, not ritual · owner verbatim GPU-staleness precedent line 15149: *"a test that measures ritual isn't a floor · a tightening, not a loosening"*)."

**Attribution of horizon value:** the exact value `2026-09-23T03:23:15Z` is arithmetic (proposal-filing 2026-09-21T03:23:15Z + 48 hours per R-18 effect 12 ordinary tier). Owner ratified the tier and the mechanic; the numeric horizon is a mechanical consequence of the tier + filing instant, not an owner-chosen number.

---

## 3 · NO-EXPEDITE reaffirmation — owner ruling (2026-09-21T~06:15Z)

The horizon was tested for expedite at 2026-09-21T~06:15Z. Owner denied the expedite request:

**Anchor:** `STATE/DECISIONS.md:23236` (banked in R-98 seal report verbatim).

> "Non-interrupting — owner ruling on the R-91 window, bank verbatim at next boundary: NO EXPEDITE. 'The countdown that cannot be shortened is the ceremony (RBM-8; SER C.5 I-4), and it's a Tier A check in the audit standard about to be applied to this repository — §6.6, "a countdown cut short" is what FAIL looks like. Waiving it because the sweep already proved green is exactly the argument every future shortcut would make; the mechanic's value is that it doesn't yield to a good result.' R-91 applies at 2026-09-23T03:23:15Z, at your next boundary after expiry — exactly as already planned. Completion sprint dispatch acknowledged by owner; proceed as sequenced. Note the RBM-8 / SER C.5 I-4 citations for the Family D (RBM/ROC) mapping — the owner just handed you a live cross-reference between the ceremony mechanic and the rows you'll be authoring."
> — Owner verbatim, banked at `STATE/DECISIONS.md:23236`

**Cross-reference:** the ceremony mechanic itself was subsequently authored as canonical Rules Service rows RBM-8 + SER C.5 I-4 at R-98 seal `38eeef6c` — the R-91 window became the live evidence receipt for RBM-8 in code (`RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC="2026-09-23T03:23:15Z"`).

---

## 4 · Objective the rule was serving — owner directive rationale

The R-91 CEREMONY served two nested objectives:

1. **Discipline objective (ceremony mechanic itself)** — owner verbatim (2026-09-21T~06:15Z, quoted above): the ceremony countdown is a **Tier A audit standard mechanic** (§6.6 · "a countdown cut short is what FAIL looks like"). Its value is that "the mechanic doesn't yield to a good result." Purpose: prove the desk cannot expedite ceremonies for its own convenience, even when the underlying sweep is already green.

2. **Closure objective (retire 5 baselines + 5 annotations)** — from the CEREMONY-OPEN apply schedule verbatim (`DECISIONS.md:22243`): the ε-apply at horizon executes ten operations to (a) mirror runtime `/app/frontend/{App.js,pages/}` byte-identically to `pod_shell/frontend/{App.js,pages/}`, (b) retire the 5 baseline entries carrying pod_shell mirror-drift + v8-cascade cascades, (c) retire 5 annotation keys (3 mirror-drift + 2 v8-cascade) retaining `test_cp10_harness_receipt_is_still_recent`, (d) flip `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status`: SCHEDULED → SEALED.

**Author of the rule (in the formal sense):** owner ruling at 2026-09-21T~01:00Z ("PATH ε RATIFIED") is the ceremony-open authority. Proposal drafted by main-agent desk at `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` per the ordinary-tier propose step; owner counter-signed with the ratification verbatim above per SO:437 batched-countersign clause. NOT an agent unilateral rule; NOT an owner unilateral rule either — it is a **ratified ceremony with an agent proposal + owner counter-sign**.

---

## 5 · The FIVE annotations · verbatim from `baseline_failures.json` at retrieval instant

**Source:** `/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` at commit `7170dfa` (CENSUS-3-F.2 Commit-A' · programme/track-a head).
**Total in-file annotations:** 6 (3 `known_runtime_drift_annotations` + 3 `known_r91_closure_scheduled_receipt_drift_annotations`).
**R-91 apply retires:** 5 of 6 (3 mirror-drift + 2 v8-cascade). **Retains 1** (`test_cp10_harness_receipt_is_still_recent`).

### Annotation set A · `known_runtime_drift_annotations` (3 · ALL retire at ε-apply)

1. **`tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell`**
   - drift_kind: `pod_shell_mirror_drift`
   - owner_ruling_ref: R-86 CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE (Ruling 1 · 2026-09-20T~19:00Z)
   - owner_ruling_verbatim_short: *"Coexistence with a closure date is discipline; without one it's drift with a ruling attached."*
   - closure_card_line: *"unify /app/frontend/** ↔ pod_shell/frontend/** byte-identity — this drift entry retires when the wave lands"*

2. **`tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js`**
   - drift_kind: `pod_shell_mirror_drift`
   - Same owner_ruling_ref / short / closure_card_line as (1).

3. **`tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir`**
   - drift_kind: `pod_shell_mirror_drift`
   - Same owner_ruling_ref / short / closure_card_line as (1).

### Annotation set B · `known_r91_closure_scheduled_receipt_drift_annotations` (3 · 2 retire + 1 retain)

4. **`tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom`** — RETIRES
   - drift_kind: `v8_substitution_rule_binding_fail_under_v8_engine_retirement`
   - owner_ruling_ref: R-88+ owner A-ruling (2026-09-20T~22:05Z)
   - owner_ruling_verbatim_short: *"Same root cause (dc48d5313), same closure (R-91), same reasoning that covered artifact 4 covers artifacts 5 and 6."*
   - closure_card_line: *"CP10 harness receipt returns non-vacuous (dummies_declared > 0, marked_slots > 0, per_rule non-empty) at the R-91 verification run"*

5. **`tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present`** — RETIRES
   - drift_kind: `v8_substitution_slot1_marker_missing_under_v8_engine_retirement`
   - Same owner_ruling_ref / short as (4).

6. **`tests/invariants/test_w_registry_full_build_cp10_wave_close.py::test_cp10_harness_receipt_is_still_recent`** — **RETAINS** per R-91 spec §22243 verbatim: *"v8-cascade annotations retire 2 keys retaining cp10-still-recent"*.
   - drift_kind: `cp10_harness_receipt_vacuous_pass_under_v8_engine_retirement`
   - owner_ruling_ref: R-88+ owner directive (2026-09-20T~21:55Z)
   - owner_ruling_verbatim_short: *"THE SUBJECT IS NOT RETIRED — IT IS DISPLACED BY AN ALREADY-RULED DIVERGENCE WITH A SCHEDULED CLOSURE. The CP10 harness vacuousness is a fourth artifact of the same divergence as the prior three."*
   - closure_card_line: *"CP10 harness receipt returns non-vacuous (dummies_declared > 0, marked_slots > 0, per_rule non-empty) at the R-91 verification run"*
   - **Retention reason:** cp10-still-recent is a time-drift guard (harness receipt must be < N hours old), not a v8-engine-retirement artifact per se; it stays as a live receipt-freshness guard past R-91.

### The FIVE RETIRING annotations (owner's phrasing "5 annotations exactly as R-91 specified")

1. `test_runtime_frontend_app_matches_repo_pod_shell`
2. `test_app_frontend_App_js_mirrors_pod_shell_App_js`
3. `test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir`
4. `test_every_v8_substitution_rule_binds_to_harness_rendered_dom`
5. `test_slot1_registry_aside_marker_present`

Plus the paired **5 baseline entries** (same 5 test nodeids) retiring atomically from `baseline_failures["baseline_failures"]` (currently length 5).

---

## 6 · Post-supersede status snapshot (owner ruling 2026-09-22T~06:12Z relayed to desk 2026-09-22T~06:15Z)

Owner ruling (relayed verbatim in the desk's inbound message, banked next-append at `DECISIONS.md` as R-101):

> "Unless you think otherwise i dont think the timer is useful or the rule - commence if xxx conditions are met. I dont think the rule serves much because there will always be something more to build or change. Should be a better way to manage the risk as we need to see what you are building and the only way now is the front end."

Effect on this retrieval:
- The R-91 TIMER (2026-09-23T03:23:15Z horizon) is superseded by condition-gating.
- The R-91 WHAT (byte-identical mirror + 5 baselines → 0 + 5 annotations retire + retain cp10-still-recent + milestone_status SEALED) is **unchanged**.
- The R-98 code-encoded RBM-8 constants (`RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC="2026-09-23T03:23:15Z"`) are **historical** — the horizon-value was the live evidence at authoring; owner has now superseded the mechanic on ε-apply timing only (canon-rule for future ceremonies stays).

**Retrieval closes clean.** All quotes above traced to file:line at retrieval instant. Zero paraphrase in quote blocks.

— main-agent desk, 2026-09-22T06:15:23Z
