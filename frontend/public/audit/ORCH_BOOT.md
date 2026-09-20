READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ORCH_BOOT.md — Anti-forget boot manifest

**Owner ruling (verbatim, 2026-09-17T~20:45Z, banked in STATE/DECISIONS.md):**

> "Add a machine-checkable boot manifest whose ratchet field can never
>  silently drift, and whose HEAD fields cannot race with the §3.3 commit
>  protocol.  This file MUST be regenerated at every seal boundary (R-6)."

This file is the CANONICAL boot state for the orchestrator.  A byte-identical
downloadable copy is served at `/app/frontend/public/audit/ORCH_BOOT.md`.

The invariant test at
`repos/Extraction-Akki/backend/tests/invariants/test_orch_boot.py` enforces:

1. Both copies exist and are byte-identical.
2. `ratchet.passed_floor` equals live `baseline_failures.json.passed_floor`
   (drift-and-burn priority guard · always-on hard assertion).
3. `ratchet.baseline_failures_sha256` equals live sha256 of that file
   (paired byte-fingerprint · always-on hard assertion).
4. `heads_last_sealed.*.head` are well-formed 40-hex AND banked in
   STATE/DECISIONS.md or STATE/NEXT.md (last-sealed HEADs, NOT live
   `git rev-parse HEAD` — freshness is enforced by R-6 boundary
   regeneration, not by an always-on equality-to-live-HEAD test, per
   owner ruling refinement to avoid racing §3.3 Commit-A/B/C ordering).

Regenerate this file (both copies, byte-identically) at every §3.3
Commit-C fixup, at every owner ruling that mutates ratchet / HEADs /
STATE files, and on any boot ritual that detects drift.

---

```yaml
schema_version: 1
generated_at_utc: 2026-09-20T11:30:00Z
generator: main-agent Autopilot (CP-PRINCIPAL-MODEL-WAVE Commit-C fixup · WAVE R-69 Step 9 · state master · R-6 boundary regen advancing heads_last_sealed.state_repo.head `b8225536ca976ce5bea92fd673b90217094a58e8` (CP-ALPHA-GAP-HARDENING Commit-B) → new Commit-B `947591831da09601a6880a3e42084b78657e9d01` (this-CP Commit-B · banks Commit-A `4b3b5e09a71254c3ccb9d4b6abcd19dbdfe13e34` on programme/track-a) · advances heads_last_sealed.code_repo.head narratively-current first-block `8c944ee7d06e6655c73eb12ad1453267f92a3d91` (CP-ALPHA-GAP-HARDENING Commit-A) → this-CP Commit-A `4b3b5e09a71254c3ccb9d4b6abcd19dbdfe13e34` (Principal Model Spec v1 landed · 13 PRIN requirements PRIN-1..PRIN-13 RED-first with verbatim spec docstrings per SO §2.5 · new frozen contract contracts.principal_v1 + 4 new service modules services.principal_store + services.credential_plane + services.trust_domain + services.request_context including ledger_actor_binding adapter wrapper · ratchet 5532 → 5546 · +14 measured delta reconciled per owner directive verbatim "expect +13 but write the measured number") · ratchet already advanced pre-Commit-A at 5532→5546 with baseline_failures_sha256 7cb320ef3fc7…→5abc315125f3… per M16-W3 corrected order — unchanged at this Commit-C fixup · R-76 marker flips ⏳ IN-FLIGHT → ✅ SEALED at this fixup · owner ratification chain 2026-09-20T~09:48Z (Step 9 opening authorization verbatim — 13 PRIN requirements + R-22 90-day rotation DEFAULT-class as ruling + R-23 team endpoints as read-views as ruling + interlude marker discipline) + this-session GO ratification verbatim (plan confirmed · ContextVar async-safe · fail-closed on absence · key-material-absence-scan discipline · Ledger actor-string upgrade as adapter/wrapper not in-place edit · Commit-A programme/track-a Commits-B/C master · prominent seal report — DAP portal frontend work UNBLOCKED at this seal) · Commit-B state landing this-wave (DECISIONS.md append R-76 banking + NEXT.md R-76 marker + STATE/PINS.md commissioning_record pointer refresh per R-29-BOOT housekeeping-pickup + notes/wave_principal_model_grounding_brief.md 173 lines NEW + notes/ORCH_BOOT.md ratchet-only regen already prepared + POD audit sync + 6 drill receipts pre-Commit-A double-green byte-identical stripped-sha256 11adcbe6030e42f9e20702f42f91a9312e44f20d1d7a02b2912dd1c91f41efc1 IDENTICAL run1+run2 both 5546 passed/1 skipped/438 warnings against post-bump baseline sha256 5abc315125f3…) · Commit-C fixup this-commit files (DECISIONS.md Commit-C fixup banking section + NEXT.md R-76 marker flip + notes/ORCH_BOOT.md this-file regen + /app/frontend/public/audit/ORCH_BOOT.md byte-identical sync — POD repo commit tracking deferred to next POD-sync boundary per prior seal precedent) · sealed contracts NOT edited · sealed writers NOT edited (Ledger actor-string upgrade landed as adapter/wrapper module per owner reminder verbatim) · zero production mutation-site FINDINGS banked · Canon anchors Principal Model Spec v1 sha256 056caa00b5eb… + SO §2.5 + §3 + §3.3 + §3.8 + §3.10-α + §6.4 + §6.7 + Northena Promise #32 + DAP-1/2/3/5/13 + DAP R-4 + Attribute 12 + dap_backend_spec_v1 LIM-3 + tcb_enumeration_v1 IN PRIN-2/5/6/11 + failure_posture_v1 + R-22 + R-23 + CP-ALPHA-GAP-HARDENING α-gap precedent + M16-W3 corrected order · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · principal-wave seal = last gate on DAP portal frontend work per owner directives · Standing bounds unchanged)
regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-dap-lifecycle-backend-wave-advancing-state-head-and-code-head-narrative

ratchet:
  passed_floor: 5580
  counts_at_baseline_passed: 5580
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: e57cfd4c632f88b3e8e0d5a16be21bd76ce69a67d22bacb5cbfd3e5472a17eca

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: b4850fd8f062e785877a74ddd09718be72a5df2c
    sealed_at_utc: 2026-09-20T12:38:00Z
    seal_kind: "CP-DAP-LIFECYCLE-BACKEND-WAVE · state Commit-B `b4850fd8f062e785877a74ddd09718be72a5df2c` · banks Commit-A `86348320a74816542f6fa3da1e42ce044448625e` on programme/track-a · WAVE R-70 Step 1 · DAP Request Lifecycle backend wave state-side banking · 2026-09-20T~12:38Z · owner directive verbatim (this-session · post-CP-PRINCIPAL-MODEL-WAVE seal `4b3b5e09` / `94759183` / `afe46cf8`) `OPEN DAP REQUEST LIFECYCLE BACKEND WAVE with three formally-ingested artifacts — RMS DAP LATEST.html (NOW BINDING design source · SUPERSEDES prior banked portal prototype RMS AI Prototype v2 sha 9952692ce058... referenced in Step 8 OS-prototype frontends card) + DAP List of Changes 20.09 + extraction_request_approval_journey.md. Eight owner-policy/spec-clarification decision questions issued (DAP-LIFECYCLE-Q1..Q8) — 6 owner-policy (Q1..Q6) + 2 spec clarifications (Q7..Q8); each is HARD-HOLD fail-closed until ruled per owner directive verbatim.` · owner corrections banked verbatim: (1) DAP-15 timer discipline (In Approval → Expired · silence never = approval · Ready → Expired NOT the DAP-15 rule); (2) Q8 DEFAULT-class BUILD-TO-YES-READING pending ratification · Q7 disposition-set (Blocked stays 3-kind · non-gate fault = banked TODO marker fail-closed · spec §6 CHECK-FIRST executed with hunt receipt phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json banking authoritative DAP-Spec §6 Failure Posture DAP-28/29/30 does NOT authorise a fourth kind of Blocked); (3) notification event-emission surface added (toast at submission + retrieval · email stub OFF DEFAULT-class); (+) identity-discipline test-addition (submitter surfaceable · approver never surfaced · decisions permanent no-reopen); (+) ratchet discipline `measure empirically post-GREEN reconcile line-by-line write the measured number` · DELTA +34 measured (34 new invariants at tests/invariants/test_dap_lifecycle_wave.py W1..W8 clusters · scope frozen at 6 buildable-now items + Q1-Q8 placeholders per SO §6.4 NOTHING-BEYOND) · Files added Commit-B (11 tracked): STATE/DECISIONS.md R-77 append + STATE/NEXT.md R-77 append + STATE/PINS.md commissioning_record pointer refresh housekeeping-pickup + STATE/dap_lifecycle_pending_rulings.md NEW register + notes/ORCH_BOOT.md ratchet-only regen (pre-Commit-A) advanced to full R-6 boundary regen (this-Commit-C fixup) + 3 extract notes (extraction_request_approval_journey_extract + rms_dap_latest_extract + dap_list_of_changes_20_09_extract) + phase0/credential_drop_manifests/20260920T1140Z_owner_drops_manifest.json + phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json + tools/dap_lifecycle_wave_bump_baseline.py · Ratchet 5546 → 5580 (+34 exactly · both counts_at_baseline.passed AND invariants_enforced_when_baseline_guard_1.passed_floor bumped per CCS2 lesson) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `447c341523db803307d2c4404eb6b915164a8512996aa9c9b5c8777ce8d612de` IDENTICAL across drill_receipts/20260920T1230Z_run1 (163.07s) + 20260920T1235Z_run2 (161.49s) both 5580 passed/1 skipped/438 warnings against post-bump baseline_failures.json sha256 `e57cfd4c632f88b3e8e0d5a16be21bd76ce69a67d22bacb5cbfd3e5472a17eca` · Additive-only per SO §3.8 · sealed contracts NOT edited · sealed writers NOT edited · sealed test files NOT edited (dap_lifecycle_wave.lifecycle_shape_snapshot.json is NEW · deliberately outside frozen-Pydantic-parity domain per parity test docstring lines 118-122) · Commit-C fixup this-commit files DECISIONS.md Commit-C banking + NEXT.md R-77 marker flip ⏳ OPEN → ✅ SEALED + notes/ORCH_BOOT.md this-file R-6 boundary regen advancing state_head `947591831da09601a6880a3e42084b78657e9d01` → this-Commit-B `b4850fd8` + code_head narratively-current first-block `4b3b5e09a71254c3ccb9d4b6abcd19dbdfe13e34` → this-CP Commit-A `8634832` + /app/frontend/public/audit/ORCH_BOOT.md byte-identical sync · Canon anchors verbatim extraction_request_approval_journey.md (sha256 `a7485f06…` · 468 lines · custody/owner_drops/20260920T1140Z/) + RMS_DAP_LATEST.html (sha256 `1b5f59d4…` · 221620 bytes · NOW BINDING · SUPERSEDES RMS AI Prototype v2 for DAP portal surfaces only) + DAP_List_of_Changes_20260920.docx (sha256 `4eabe4d5…`) + DAP-Spec §6 Failure Posture DAP-28/29/30 + DAP-15 refusal-vs-expiry + DAP-21 metered event per retrieval + DAP-26 no-retroactive-change (Q8 analogy) + DAP-27 suspension terminal Blocked + DAP-28 gates fail closed + DAP-29 ledger write required + DAP-35 release-budget non-disclosure + Canon 5 Interface Architecture seam-boundary discipline + Canon 3 §9.3 canonicalization discipline + Canon 8 §W11 one-task-one-identity + SO §2.5 verbatim-docstring-discipline + SO §3 tests-first + SO §3.3 3-Commit Seal on dual branches + SO §3.8 thin-kernel additive-only + SO §3.10-α closed-schema (RequestState + BlockedKind + TERMINAL_STATES + ALLOWED_EDGES all frozen tuples/enums) + SO §4.1 §E custody discipline + SO §4.1 §F sha-pinning discipline + SO §6.4 NOTHING-BEYOND + SO §6.7 sequence WAVE R-70 Step 1 OPEN post-WAVE-R-69-Step-9-SEAL + M16-W3 corrected order (pre-Commit-A ratchet-only ORCH_BOOT regen · heads advance at Commit-C fixup) + CCS2 lesson (bump BOTH passed_floor AND counts_at_baseline_passed) + CCS3 seal-of-frontends-gate context + CP-PRINCIPAL-MODEL-WAVE seal `4b3b5e09` / `94759183` / `afe46cf8` precedent + CP-OS-PROTOTYPE-FRONTENDS-CARD `e3ea95df` Step 8 context · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next HALT for owner Q1-Q6 rulings + specialist dispatch for DAP portal frontend build per owner directive item 6 at wave-open"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 86348320a74816542f6fa3da1e42ce044448625e
    sealed_at_utc: 2026-09-20T12:35:00Z
    seal_kind: "CP-DAP-LIFECYCLE-BACKEND-WAVE · Commit-A `86348320a74816542f6fa3da1e42ce044448625e` · code programme/track-a · WAVE R-70 Step 1 · DAP Request Lifecycle backend wave landed · 34 new invariants at tests/invariants/test_dap_lifecycle_wave.py (W1-W8 clusters) · 2026-09-20T~12:35Z · owner directive verbatim (this-session · post-CP-PRINCIPAL-MODEL-WAVE seal) `OPEN DAP REQUEST LIFECYCLE BACKEND WAVE with three formally-ingested artifacts — RMS DAP LATEST.html + DAP List of Changes 20.09 + extraction_request_approval_journey.md. Eight owner-policy/spec-clarification decision questions issued (DAP-LIFECYCLE-Q1..Q8) — 6 owner-policy (Q1..Q6) + 2 spec clarifications (Q7..Q8); each is HARD-HOLD fail-closed until ruled per owner directive verbatim.` · Owner corrections banked at wave-open verbatim: (1) DAP-15's 14-day expiry runs from SUBMISSION to DECISION · In Approval → Expired · silence never = approval; (2) Q8 DEFAULT-class BUILD-TO-YES-READING pending ratification · Q7 disposition-set Blocked stays 3-kind · non-gate fault = banked TODO marker fail-closed · spec §6 CHECK-FIRST executed; (3) notification event-emission surface added · toast at submission + retrieval · email stub OFF DEFAULT-class; (+) identity-discipline test-addition verbatim `the decision-service tests should assert the identity discipline from the journey spec — submitter identity recorded and surfaceable, approver identity NEVER surfaced to the party (role + data-owner name only), decisions permanent (no reopen path)` · DELTA +34 · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (6 buildable-now items + 8 HARD HOLDs) · Files added (20 NEW · additive-only per SO §3.8): backend/services/dap_lifecycle/{__init__,state_machine,timer,approval_service,blocked_kinds,metering_wiring,notification_surface,fail_closed}.py (8 new modules) + backend/tests/invariants/test_dap_lifecycle_wave.py (34 invariants) + backend/tests/invariants/dap_lifecycle_wave.lifecycle_shape_snapshot.json (contract_sha256 `253c69c6d75e29f7e48a69c0b8cb8e20d25e09267ccb7f6e7089992905a77e06` · deliberately NOT .contract_snapshot.json to stay outside frozen-Pydantic-parity domain) + 9 drill receipts · Files edited (additive-only): backend/tests/invariants/baseline_failures.json (passed_floor + counts_at_baseline.passed 5546 → 5580 + ratchet_history append) · AUTHENTIC RED-first at 20260920T1210Z (fail right-reason ModuleNotFoundError No module named 'services.dap_lifecycle') → GREEN at 20260920T1215Z (33/34 pass · 1 right-reason contract-sha placeholder fail · authentic-RED-pin pattern from CCS2/CCS3) → GREEN_post_snapshot at 20260920T1216Z (34/34 pass 0.70s) → full_sweep_post_snapshot at 20260920T1220Z (5580 passed + 1 skipped + 438 warnings clean zero regressions elsewhere) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `447c341523db803307d2c4404eb6b915164a8512996aa9c9b5c8777ce8d612de` IDENTICAL across drill_receipts/20260920T1230Z_run1 + 20260920T1235Z_run2 both 5580 passed/1 skipped/438 warnings against post-bump baseline_failures.json sha256 `e57cfd4c632f88b3e8e0d5a16be21bd76ce69a67d22bacb5cbfd3e5472a17eca` · sweep-adjacent housekeeping-pickup (transparency banking): 1 prior GUARD1 attempt at 20260920T1225Z_run1.log failed 1 test test_orch_boot_anti_forget_manifest_matches_live_ratchet_and_sealed_heads because I initially bumped baseline but hadn't yet regenned notes/ORCH_BOOT.md ratchet fields · reconciled by regenning ORCH_BOOT.md pre-Commit-A per M16-W3 corrected order · not a scope creep · precedent CCS1/CCS2/CCS3/Principal-wave · Additive-only per SO §3.8 · sealed contracts NOT edited (contracts.dap.MeteredEvent consumed via composition only) · sealed writers NOT edited · sealed test files NOT edited · Q7 spec §6 hunt receipt phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json reads authoritative DAP-Spec §6 body from canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx (§6 title `Failure Posture` containing DAP-28/29/30 · speaks ONLY of gates failing closed · does NOT authorise a fourth kind of Blocked · Q7 disposition STANDS at HARD HOLD with banked TODO marker) · Canon anchors verbatim extraction_request_approval_journey.md L25/L26/L27/L30/L47/L48/L55-58/L60/L91/L149-150/L201/L212/L219/L225/L397/L408/L411 + DAP-15 + DAP-21 + DAP-26 + DAP-28 + DAP-29 + DAP-35 spec bindings + SO §2.5 + §3 + §3.3 + §3.8 + §3.10-α + §4.1 §E + §4.1 §F + §6.4 + §6.7 + M16-W3 corrected order + CCS2 lesson + CP-PRINCIPAL-MODEL-WAVE seal precedent · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B → Commit-C fixup → HALT for owner Q1-Q6 rulings + specialist dispatch"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 4b3b5e09a71254c3ccb9d4b6abcd19dbdfe13e34
    sealed_at_utc: 2026-09-20T11:28:00Z
    seal_kind: "CP-PRINCIPAL-MODEL-WAVE · Commit-A `4b3b5e09a71254c3ccb9d4b6abcd19dbdfe13e34` · code programme/track-a · WAVE R-69 Step 9 · Principal Model Spec v1 landed · 13 PRIN requirements PRIN-1..PRIN-13 RED-first with verbatim spec docstrings per SO §2.5 · owner ruling 2026-09-20T~09:48Z verbatim (Step 9 opening authorization — 13 PRIN each in verbatim docstring per SO §2.5 + RED-FIRST-WITH-TESTS always + R-22 90-day rotation DEFAULT-class ratified as ruling + R-23 keep team endpoints /api/team/access_register + /api/team/constitutional_seats as read-views over new principal store ratified as ruling + interlude marker discipline authorized) + owner this-session GO ratification verbatim (scope frozen at 13 PRIN no additions + ContextVar async-safe is the only correct choice under FastAPI/asyncio thread-locals leak across await boundaries + fail-closed on principal-context absence never default to anonymous actor + key-material-absence-scan discipline test proves absence via scan/AST or storage-inspection not just happy-path check + Ledger actor-string upgrade and trust-domain identifier on every record are PRIN requirements with cross-cutting touch points keep them additive wrappers/adapters if any sealed writer needs its actor semantics upgraded in place that's a fork not an edit + Commit-A on programme/track-a Commits-B/C on master · prominent seal report on landing DAP portal frontend work UNBLOCKS at this seal) · DELTA +14 measured (13 new PRIN invariants at tests/invariants/test_principal_model_v1.py + 1 natural collection increment observed on full sweep · not scope creep · owner directive verbatim `expect +13 but write the measured number`) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · Files added (10 NEW · additive-only per SO §3.8): backend/contracts/principal_v1.py + backend/services/principal_store/*.py + backend/services/credential_plane/*.py + backend/services/trust_domain/*.py + backend/services/request_context/*.py + backend/tests/invariants/test_principal_model_v1.py + backend/tests/invariants/principal_v1.contract_snapshot.json · Files edited (additive-only): backend/tests/invariants/test_frozen_contract_snapshot_parity.py (1 new CONTRACT_TO_SNAPSHOT entry · docstring-sanctioned two-side extension) + backend/tests/invariants/baseline_failures.json (passed_floor + counts_at_baseline.passed 5532 → 5546 + ratchet_history append) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `11adcbe6030e42f9e20702f42f91a9312e44f20d1d7a02b2912dd1c91f41efc1` IDENTICAL both runs · Additive-only per SO §3.8 · sealed contracts NOT edited · sealed writers NOT edited (Ledger upgrade landed as adapter/wrapper) · Acceptance frame spec §6 verbatim 8 DAP requirements unblocked (DAP-13 + DAP-14 + DAP-21 + DAP-22 + DAP-23 + DAP-24 + DAP-25 + DAP-27) · Canon anchors verbatim Principal Model Spec v1 sha256 `056caa00b5eb…` + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.4/§6.7 + Northena Promise #32 + DAP-1/2/3/5/13 + DAP R-4 + Attribute 12 + dap_backend_spec_v1 (LIM-3) + tcb_enumeration_v1 IN PRIN-2/5/6/11 + failure_posture_v1 fail-closed on absence + R-22/R-23 + CP-ALPHA-GAP-HARDENING α-gap precedent + M16-W3 corrected order · Stop-conditions #1/#2/#3 NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: ebebc46f75494dbaa16efacd7b077c47afcb69f1
    sealed_at_utc: 2026-09-19T20:50:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION · Commit-A `ebebc46f75494dbaa16efacd7b077c47afcb69f1` · memory-layer follow-on wave W3 · owner OPTION 1 ratification + owner CLARIFICATION verbatim · new backend/tests/invariants/test_memory_compaction_v1_w3_tcb_registration.py (3 tests MEM-3 IN + MEM-7 IN + MEM-2 OUT) · additive edit backend/services/doc0_attributes/tcb.py::_TCB_ENTRIES appending 3 TCBEntry tuple entries per module docstring line 24 amendment method · sealed W-M2-SW7 logic NOT edited (TCBEntry model + get_tcb_current + is_in_tcb + TCB_VERSION + docstring all unchanged · only tuple additive-appended) · baseline_failures.json ratchet 5482 → 5485 (+3 exactly) · pre-Commit-A double-green byte-identical stripped-sha256 `5b4ec526cd517afd1bacf829edbc5f81a88c485839a0b3896e0179bcf333dc52` · Canon anchors MEM-2 + MEM-3 + MEM-7 + Spec §4 Table 3 + tcb.py docstring line 24 + Doc-0 Attribute 1 + Canon 8 §W11 + SO §3.8 + SO §6.4 + M16 R-3 2026-09-09 precedent (Mkono/Grey Mirror pure-tuple-append)"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 67b5e070e017ecbbd8645df87d42966721fa082d
    sealed_at_utc: 2026-09-19T20:22:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W2-HARD-BANS-GREP-NEGATIVE · Commit-A `67b5e070e017ecbbd8645df87d42966721fa082d` · memory-layer follow-on wave W2 · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim (W2 grep-negative hard bans as invariants via AST/grep-negative over backend/**/*.py per ingest directive · summarise-with-model-delete-original convergence ban is crown one · STOP not test tweak if triggered) · new backend/tests/invariants/test_memory_compaction_v1_hard_bans_grep_negative.py (6 grep-negative tests MEM-R-048..MEM-R-053 · scanner + regex helper · scope backend/**/*.py excluding tests + compaction_v1 + phase0 + __pycache__) · baseline_failures.json ratchet 5476 → 5482 (+6 exactly · zero wizard trigger) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `edb0d556398107f1683a000b92552f9f09361adb1d01be31fd79fdb8cd75af55` IDENTICAL across drill_receipts/20260919T201614Z_run1 + 20260919T201953Z_run2 · additive-only per SO §3.8 · Canon anchors MEM-R-047..MEM-R-053 + Canon 8 §W11 + SO §3.8 + SO §6.4 NOTHING-BEYOND · MEM-R-053 CROWN BAN NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: b1d1183674856c99e85d64b4fbd22a1508ffc4c9
    sealed_at_utc: 2026-09-19T19:57:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-BUILD-WAVE · Commit-A `b1d1183674856c99e85d64b4fbd22a1508ffc4c9` · MEMORY LAYER FIRST BUILD WAVE · owner MEMORY GO ruling banked verbatim · new backend/services/memory/compaction_v1/ sub-package (7 files) matches c13_scope precedent · new test_memory_compaction_v1_property_tests.py (7 property tests) · baseline_failures.json ratchet 5469→5476 · pre-Commit-A double-green byte-identical stripped-sha256 03aace2f · additive-only per SO §3.8 · Canon anchors MEM-1..MEM-11 + Spec §2/§4/§5/§7 + Canon 3 §9.3 + Canon 8 §W11 + Canon 4 §22 + SO §3.10-α + SO §3.8 + SO §6.4 · Stop-conditions NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: f57f6c68e765096bd8bc69f8fbfdf96679e5280a
    sealed_at_utc: 2026-09-19T19:05:00Z
    seal_kind: "CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG · Commit-A `f57f6c68e765096bd8bc69f8fbfdf96679e5280a` · M17-W5 STRUCTURAL FORK CLOSED · owner ruling 2026-09-19T~17:54Z Owner Desk Batch item (f) verbatim ratifying scope (`Handoff-ID adapter + ID-domain type-tagging (ho_ slot rejects non-ho_ prefixes, tests first)`) · Option (i) additive-adapter extension per M17_W5_HANDOFF_ID_MISMATCH_FORK doc verbatim · new backend/services/personal_client/handoff_binding.py (5-surface: HandoffId str-subclass type-tag with ho_ slot regex-enforcing __new__ + HandoffIdRefused + HandoffBindingRefused fail-closed sentinels + derive_handoff_id deterministic pure-data-in adapter mapping pcs_<suffix>→ho_<suffix> + emit_ask_with_handoff seam-routing wrapper delegating to sealed M14-W3 insert_ask under caller-supplied M11 t_<tenant_id> repository) · new backend/tests/invariants/test_m17_w6_handoff_binding_adapter_and_type_tag.py (7 tests: module_surface + derive_handoff_id_deterministic + derive_handoff_id_rejects_non_pcs + handoffid_class_rejects_non_ho + emit_ask_with_handoff_routes_where_sealed_fails + AST_bans_decision_write_surface + AST_zero_import_m17_w3_and_learned_surfaces) · baseline_failures.json ratchet 5462→5469 (+7 exactly · zero wizard trigger since not a contracts/*.py file) · AUTHENTIC RED-first at drill_receipts/20260919T184633Z (7/7 fail right-reason ModuleNotFoundError) → GREEN at drill_receipts/20260919T184858Z (7/7 pass · 0.77s) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `00a516263feb56c9495080b671efe06a9693c4eda4684191fc2bdf7cbebe9843` IDENTICAL across drill_receipts/20260919T185617Z_run1 + 20260919T185924Z_run2 (both 58129 bytes · 5469 passed/1 skipped/438 warnings · ~168s each) against final baseline_failures.json sha256 `cb15b9803afb33e738e87ba7de9531bd1ef49e3828215adf551ba00905ea2360` · additive-only per SO §3.8 · sealed M17-W3 session.py NOT edited (thin-adapter discipline · adapter is new authoritative runtime path per fork Option (i) verbatim) · sealed M14-W3 asks.py NOT edited (consumed via identity import) · sealed M17-W1/W2/W4/W5/M14/M11/M16/W-M2-SW7/W-7bB modules all NOT edited · Canon 8 §W11 structural role separation AST-enforced · Canon 5 interface architecture · Canon 4 §22 rung-1 discipline · Canon 3 §9.3 append-only · AC-18 · R-21 · HR-2 · SO §3.10-α · SO §6.4 NOTHING-BEYOND · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · M17 milestone_status CLOSED-WITH-FORK-BANKED → CLOSED at Commit-B via M17.md update (fork closed on seal per owner ratification) · notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md status flips OPEN-OPTION-(ii)-APPLIED → CLOSED-BY-M17-W6-OPTION-(i)-LANDED at Commit-B"

boot_sequence:
  - Read STATE/STANDING_ORDERS.md end-to-end.
  - Read last 300 lines of STATE/DECISIONS.md and all of STATE/NEXT.md.
  - Verify HEADs against `git rev-parse` for informational purposes only — this file's HEADs are LAST-SEALED, not live.
  - Verify ratchet floor + baseline sha256 against baseline_failures.json (hard-asserted by test_orch_boot.py).
  - Resume the in-flight work order at the top of STATE/NEXT.md.

regeneration_triggers_r6:
  - After Commit-C fixup of every §3.3 3-commit seal (CP boundary).
  - After any owner ruling that mutates ratchet, HEADs, or STATE files.
  - On every boot ritual when STANDING_ORDERS §1 boot verification detects drift.

authoritative_downloadable_copy_path: /app/frontend/public/audit/ORCH_BOOT.md
```

---

## HARD BANS / ANTI-DRIFT · plain-language narrative (Q1 · owner ruling 2026-09-18 · additive to R-6 boundary regen)

**Purpose.** A fresh or compacted session reads STANDING_ORDERS.md end-to-end per boot step 1, but this section carries the single-line high-frequency reminders so no critical ban is ever silently forgotten between reads. Sources always win if the summary diverges — every line here cites its authoritative source. If a line here contradicts its source, the source is right; correct this file at the next R-6 boundary.

### 1 · Commit / push discipline

- **Never push. Ever.** Local commits are the record. — *SO §4 · Owner Clarification 1 2026-08-14 · reaffirmed R-18 owner ruling 2026-09-18 Item 4.*
- **§3.3 3-commit seal or it is not sealed.** Commit-A code (`programme/track-a`) · Commit-B state (`master`) · Commit-C fixup (`master`) banks Commit-B SHA into DECISIONS + NEXT + `ORCH_BOOT.md` `heads_last_sealed.state_repo.head`. — *SO §3.3 + SO §7 R-1..R-6.*
- **A CP claimed "sealed" without both SHAs banked is a discipline mislabel.** Reconciliation before forward progress. — *SO §3.3 · Owner ruling 2026-09-15 Discovery-1 ratification.*
- **`pending-C-fixup` count in seal files must be 0.** — *SO §7 R-2.*
- **Every boot ritual runs the master-parity check** (R-1) and the ratchet-history/git-log cross-check (R-3). — *SO §7 R-1, R-3.*

### 2 · Testing discipline

- **Terminal pytest only. `testing_agent` is BANNED.** Curl / `python3 -c` are allowed for spot checks. — *SO §3.*
- **Tests-first mechanical RED before any code lands.** RED receipt banked under `phase0/drill_receipts/`. — *SO §3.*
- **Double-green byte-match to close every CP.** Both `BASELINE_GUARD=1` receipts identical, banked. — *SO §3 + SO §7 R-5 (per-CP raw logs mandatory).*
- **Full `BASELINE_GUARD=1` sweep BEFORE any §3.3 seal that banks rulings.** Targeted invariants supplement, never substitute. — *Owner ruling 2026-09-18 transparency item 1 · pre-seal standard added at ORCH_BOOT R-6 regen for owner-ruling seals + all subsequent seals.*
- **Ratchet floor monotonic-up.** `baseline_failures.json` `passed_floor` + `ratchet_history` append at every close. Silent rebaselining is banned. — *SO §3.*

### 3 · Code / build discipline

- **No refactor. Thin-kernel additive-only.** Sealed modules are not edited; new work extends via thin adapter layer. — *SO §3.8 · Owner ruling 2026-09-17 Tension (a) = Option C.*
- **Zero closed enum type — schema authoritative, Python tuple mirrors.** — *SO §3.10 · Owner ruling 2026-09-17 Tension (b) = Option α.*
- **Order of authority (top→bottom):** canon → Standing Orders → SER → contract schemas → code. — *SO §2.1 · R-18 owner ruling 2026-09-18 effect 1.*
- **T-c sequencing (α):** schema + AST + P-15 land BEFORE M11-W1; caller-flip at M12b-W1; new M11 callers target the new Watch schema from day one. — *Owner ruling 2026-09-18 Item 4.*

### 4 · Silent-success + progress-signal bans

- **ALIVE IS NOT DONE.** Heartbeat / PID / directory / filename presence is NEVER completion evidence. Every seal read routes through `services.output_verified_seal.is_real_seal`. Every seal write emits `Kind:` as first-class body field. — *SO §3.1.*
- **NO RUN WITHOUT A PROGRESS SIGNAL.** Every commissioned run binds `run_id` to `runtime_supervisor` progress-ring. HALT verdicts are DATA, not process-kills. — *SO §3.2.*

### 5 · Verification-walk scope

- **Wave-window commit enumeration on every verification walk.** `git log --format=... <open>..<close_or_next>` — never the canonically-named wave-close commit alone. — *SO §4.2 · Owner ruling 2026-09-16.*
- **Cross-wave modifications** carrying their own CP citation + ratchet delta + owner directive + append-only-extension discipline are NOT drift for the origin wave's walk. — *SO §4.2 Clause 6.*

### 6 · Credential custody

- **PII / credentials: never committed, never returned, never logged, never in test docstrings.** Redacted everywhere. — *SO §4.*
- **§E · Custody-file reads only via shape-only helper OR env-injection.** Direct `cat`/`head`/`tail`/`csv.reader+print`/`openpyxl+print`/`set -x` on a custody path = SEC violation. — *SO §4.1 §E · Owner ruling 2026-09-15T~22:30Z.*
- **§F · Sha-pin every credential drop at intake or refuse.** Manifests at `phase0/credential_drop_manifests/YYYYMMDDTHHMMZ_drop_manifest.json`. Sha-less drops are quarantined at 0600 outside `estate_keys/`. — *SO §4.1 §F · R-18 Part 7(c) · Owner ruling 2026-09-18.*
- **HF token hash-delta gate.** SEC-2026-09-12-01: any HF-touching wave HOLDS until rotation is proven by sha delta ALONE (never by opening the value). Three-step owner action = revoke → generate → re-drop with §F sha-pin. — *SO §4.3 · Owner ruling 2026-09-18.*

### 7 · GPU obligations

- **Full-consumption guarantee.** All 4 GPUs run high-utilization while a campaign window is open. Idle lanes are interrupt-priority. — *SO §5.*
- **Never kill a training run mid-flight.** Ownership passes through the run's `ACTIVITY_SUMMARY.md` seal, never via SIGKILL. — *SO §5.*
- **Idle-lane restoration** uses banked machinery in `tools/queue_followon_launcher.py` + `tools/on_host_queue_dispatcher.py` — no improvisation. — *SO §5.*

### 8 · Canon-before-ruling doctrine

- **No decision proceeds from memory or summary where the governing document exists.** Read the document, don't recall it. Binding on both ruling authority and builder — no exception for either. — *Canon 1 §4.11 · Canon 7 §48 · SO §3.*

### 9 · Standing autonomous-run bounds (from owner ruling 2026-09-18)

- **Item 2 · The measure.** Every task in every chunk names which of R-18 effect-15's gate conditions (errata landed · Watch contract schema · AST + P-15 green · `canon_ref` check active · D-16..D-19 banked) it feeds or is deferred. That is the only test of movement vs circling.
- **Item 3 · Standing authority.** Autonomous from CHUNK 1 close through Q1 → Q2 → M11-W1 → M12b-W1, subject to Items 4–5. Checkpoints = reports, not holds.
- **Item 6 · SEC-2026-09-12-01** stays owner-only. HF-touching waves HOLD; everything else proceeds.
- **Item 7 · Reporting.** Chunk-close: six-item summary + gate conditions advanced + ratchet + open forks. Gate-release: R-18 effect-15's conditions each with evidence. No other reports.

### 10 · Stop-and-report conditions (from owner ruling 2026-09-18 Item 5)

Fail closed on the affected fork, present options with a recommendation, continue on everything else. Do not hold the whole build on one fork. Triggers:

1. **RED ratchet or failed invariant.**
2. **Canon vs lower-layer conflict discovered.**
3. **Any proposal to amend canon, add a TCB member outside `tcb_enumeration_v1`'s method, change a Fixed decision-register entry, or carve an exception to a hard invariant.**
4. **A new rule-vs-rule tension of the T-a/T-b kind.**

### 11 · Assessment / read-only chunk discipline (from client instruction doc · Chunk-1 scope)

- **No production/application code during ingest+ground-truth chunks.** Only markdown notes under the chunk's `notes/chunk*_YYYYMMDD/` folder + throwaway analysis scripts under `/app/assessment_workspace/tools/`.
- **Every factual claim must come from files opened this session.** Never from a README, a filename, or prior knowledge.
- **Never merge two repos' same-named services in-head.** They are different until diffed.
- **Absence is a finding.** Report it explicitly, never leave a blank.
- **BUILD_JOURNAL / close reports are claims to verify later, not findings.**
- **Do not propose sequencing, phases, or build order.** — *D7 (Canon 7 §47) · client's binding rule.*

### 12 · Defect classes (from Canon 7 §47) — reportable on sight by anyone

- **D1** · orphan gate (function with no honest promise or service trace).
- **D2** · NL-only enforcement (rule with no machine-checked twin).
- **D3** · curated verdict (validation material selected by favourability).
- **D4** · rung inflation (model-ladder placement above cheapest-sufficient with no written justification).
- **D5** · meta-spiral (second governance layer above one that exists; artefact stopped paying rent).
- **D6** · service conflation (function optimised for end-user persona rather than service sentence).
- **D7** · invented schedule/scope (sequencing without explicit instruction).
- **D8** · dual-identity execution (task or code path spanning >1 authority's identity/scope within a single execution).

### 13 · Watch doctrines (from Canon 8 §4) — 14 hard bans on the security authority

W1 eyes-never-act/hand-never-judges · W2 certainty-never-exceeds-evidence (signature-as-guard) · W3 every-autonomous-act-reversible-bounded-witnessed (destroy does not exist) · W4 deployed-in-force-never-in-shadow · W5 one-record-two-readings · W6 suspicion-refined-not-accumulated · W7 conformance-grants-trust/non-conformance-never-convicts · W8 the-floor-never-learns · W9 no-actor-enters-undeclared · W10 watcher-watched-from-outside · W11 one-task-one-identity · W12 peer-not-subordinate · W13 profile-is-armory-not-inventory · W14 self-proving-or-not-in-force.

### 14 · Structural-impossibility doctrine (from Canon 1 §4.2)

**Unrepresentable, not policed.** Where a state must never occur, the system is built so the state cannot be expressed (function signature, type, schema). Reviewed prohibitions are eventually violated; structural impossibility beats vigilance.

### Sources-win-if-drift note

If any line above disagrees with its cited source, the source is authoritative. This section is a distillation for boot-ritual convenience — never a replacement for reading `STANDING_ORDERS.md`, the referenced canon sections, or the DECISIONS entry for the specific owner ruling. Corrections land at the next R-6 boundary regen; this section is not edited in place — a superseded line is annotated with SUPERSEDED-BY at regen time, and the successor is added.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
