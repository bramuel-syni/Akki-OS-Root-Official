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
generated_at_utc: 2026-09-19T23:10:00Z
generator: main-agent Autopilot (CP-CCS3-DAP-RECEIPT-FREEZE Commit-C fixup · state master · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim + owner PROCEED ratification this-session verbatim (banked at CCS1 Commit-A banking section) · advances heads_last_sealed.state_repo.head `0520469dbf5d836d253244ae820681ac4bc980cd` (CCS2 Commit-B) → new Commit-B `d48f6e1e049b35dd334d284be9bbfb2f67eed97f` (CCS3 Commit-B · banks Commit-A `379e45508bbfbc362f2b28d93065f527bc3864bd`) · advances heads_last_sealed.code_repo.head `3fde289560830d5dffafe25c52080664625caaf8` (CCS2 Commit-A) → this-wave Commit-A `379e45508bbfbc362f2b28d93065f527bc3864bd` (CCS3 Commit-A · 12 DAP receipt freeze invariants + baseline ratchet 5515 → 5527) · ratchet 5527 unchanged at Commit-C · CCS3 R-67 marker flips ⏳→✅ SEALED · frozen contract pin #3 of 3 achieved · CCS trio complete · absence findings #3/#6/#9/#10 CLOSED at CCS3 · MEM-R-053 CROWN BAN NOT triggered · owner FRONTENDS-GATE-IS-HALT-POINT + owner PROCEED verbatim · Contract Closure Wave 3 FULLY SEALED · HALT at frontends gate opens next · staleness clock T-~12.4h remains armed)
regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-ccs3-dap-receipt-freeze-advancing-state-head-and-code-head

ratchet:
  passed_floor: 5527
  counts_at_baseline_passed: 5527
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: 8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: d48f6e1e049b35dd334d284be9bbfb2f67eed97f
    sealed_at_utc: 2026-09-19T23:10:00Z
    seal_kind: "CP-CCS3-DAP-RECEIPT-FREEZE · state Commit-B `d48f6e1e049b35dd334d284be9bbfb2f67eed97f` · banks Commit-A `379e45508bbfbc362f2b28d93065f527bc3864bd` · Contract Closure Wave 3 · DAP receipt contract freeze (FINAL contract closure wave before frontends gate HALT) · frozen contract pin #3 of 3 achieved · CCS trio complete (bundle sha `81d3c0a5e8e54137d96873784dc3714c99f574c40f430996a66b0b17ada68a62` name-sorted concat canonical JSON bytes of 3 receipt-bundle shapes MeteredEvent + TrustReceiptV1 + OuterGateReceiptV1 · Canon 3 §9.3 canonicalization discipline · mirrors CCS1 + CCS2 bundle-sha patterns · closes B-frontends-Q1 frontends-gate contract-pin triple) · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim + owner PROCEED ratification this-session verbatim (both banked at CCS1 Commit-A banking section) · state-side landing includes STATE/DECISIONS.md CCS3 Commit-A banking section (12 invariants across 5 sub-wave clusters: W1 DAP-21 MeteredEvent freeze 3 tests + W2 reliable_time_source wiring 2 tests + W3 related receipts pinned + non-α gaps banked 4 tests + W4 integration seal 2 tests + W5 absence findings closure attestation 1 test · absence findings FINAL closure status post-CCS3: CLOSED across CCS1-3 #2/#3/#4/#5/#6/#9/#10 (7 findings) · BANKED to frontends-card wave #1/#8 (2 findings) · BANKED to future integration wave #7 · additional banked at CCS3 TrustReceiptV1_alpha_gap + OuterGateReceiptV1_alpha_gap owner ratification ceremony · three frozen contract pins table (#1 C.17 seam `a6107d46…` · #2 DAP entitlement `051f25df…` · #3 DAP receipt `81d3c0a5…`) · RED-first cycle receipts + pre-Commit-A double-green byte-identical stripped-sha `5eed33e9384288952e20202b9850fbf3851db239bd9aea4c476b9ec19c26347d` IDENTICAL across drill_receipts/20260919T225820Z_run1 + 20260919T230129Z_run2 · 5527 passed/1 skipped/438 warnings · against FINAL baseline_failures.json sha256 `8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1` · both counts_at_baseline.passed AND invariants_enforced_when_baseline_guard_1.passed_floor bumped per CCS2 lesson · sealed contracts NOT edited · canon anchors Canon 5/3 §9.3/8 §W11 + SO §3.8/3.10-α/6.4/6.7 + M17-W1 milestone precedent + CCS1-C17 + CCS2 DAP entitlement bundle-sha precedents + B-frontends-Q1 + Doc-3 DAP-Spec dap_backend_spec_v1 verbatim + FRONTENDS-GATE-IS-HALT-POINT + PROCEED + owner ruling 2026-09-19T~17:54Z item (e) verbatim · Stop-conditions NOT triggered) + STATE/NEXT.md R-67 marker ⏳ IN-FLIGHT (flipped to ✅ SEALED at this Commit-C fixup) + notes/ORCH_BOOT.md R-6 boundary regen advancing state_head from prior CCS2 Commit-B `0520469dbf5d836d253244ae820681ac4bc980cd` to this CCS3 Commit-B + code_head from prior CCS2 Commit-A `3fde289560830d5dffafe25c52080664625caaf8` to this CCS3 Commit-A + audit copy re-sync byte-identical + STATE/PINS.md commissioning_record pointer refresh (state-side sensor drift · R-29-BOOT housekeeping-pickup) · additive-only per SO §3.8 · ratchet 5527 unchanged at Commit-C state files only Commit-A carried the +12"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 379e45508bbfbc362f2b28d93065f527bc3864bd
    sealed_at_utc: 2026-09-19T23:00:00Z
    seal_kind: "CP-CCS3-DAP-RECEIPT-FREEZE · Commit-A `379e45508bbfbc362f2b28d93065f527bc3864bd` · Contract Closure Wave 3 · DAP receipt contract freeze (FINAL contract closure wave before frontends gate HALT) · owner FRONTENDS-GATE-IS-HALT-POINT ratification 2026-09-19T~21:30Z verbatim + owner PROCEED ratification this-session verbatim + owner ruling 2026-09-19T~17:54Z item (e) verbatim · new backend/tests/invariants/test_ccs3_dap_receipt_freeze.py (~465 lines · 12 invariants organised in 4 sub-wave clusters + banking cluster: W1.1 MeteredEvent schema pin `b354818c…` (DAP-21 metering rail · sealed contracts.dap.MeteredEvent · absence finding #3 CLOSED via naming resolution: class exists as MeteredEvent not DAP21MeteredEvent_v0) + W1.2 MeteredEvent carries all 7 DAP-Spec-verbatim fields (operation_type + accessed_scope + quantity + quantity_unit + terms_id + party_id + timestamp_iso + R-C2 au_3b_defensible) + W1.3 MeteredEvent SO §3.10-α (frozen=True + extra=forbid) + W2.1 reliable_time_source module importable from sealed path (services.reliable_time_source.clock surface presence · ReliableClock + TimeAnchor + au_3b_defensible_now · absence finding #6 CLOSED) + W2.2 au_3b_defensible_now callable returns dict with wall_time_iso + au_3b_defensible keys (sealed surface adherence) + W3.1 TrustReceiptV1 schema pin `d4645512…` (LLM-provenance rail · sibling · absence finding #9 CLOSED via relationship documentation + pin) + W3.2 OuterGateReceiptV1 schema pin `196e56f0…` (outer-gate transform-receipt rail · sibling · absence finding #10 CLOSED via relationship documentation + pin) + W3.3 TrustReceiptV1 SO §3.10-α NON-COMPLIANCE finding (frozen=False · BANKED for owner ratification · SO §3.8 forbids editing at this wave) + W3.4 OuterGateReceiptV1 SO §3.10-α NON-COMPLIANCE finding (frozen=None · BANKED for owner ratification) + W4.1 DAP receipt bundle sha `81d3c0a5e8e54137d96873784dc3714c99f574c40f430996a66b0b17ada68a62` FROZEN CONTRACT PIN #3 OF 3 · name-sorted concat canonical JSON bytes · Canon 3 §9.3 canonicalization discipline · mirrors CCS1 + CCS2 bundle-sha patterns · closes B-frontends-Q1 frontends-gate contract-pin triple + W4.2 bundle binds all 3 named shapes (vocabulary containment · exactly 3 receipt shapes: MeteredEvent + OuterGateReceiptV1 + TrustReceiptV1) + W5 Banking test attests CCS3 closure disposition #3 CLOSED at W1 · #6 CLOSED at W2 · #7 BANKED to future integration wave · #9 CLOSED at W3 · #10 CLOSED at W3 · TrustReceiptV1_alpha_gap BANKED · OuterGateReceiptV1_alpha_gap BANKED) · zero new implementation module (all 3 DAP receipt shapes already sealed at prior CP · consumed via identity import from contracts.dap + contracts.trust_receipt_v1 + contracts.outer_gate_receipt_v1 · reliable_time_source consumed via identity import from services.reliable_time_source.clock) · baseline_failures.json ratchet 5515 → 5527 (+12 exactly · zero wizard trigger · not a contracts/*.py file · zero flip zero regression zero refactor additive-only · both counts_at_baseline.passed AND invariants_enforced_when_baseline_guard_1.passed_floor bumped per CCS2 lesson) · AUTHENTIC RED-first: RED at drill_receipts/20260919T225647Z (2 fail right-reason: (1) bundle sha computed `81d3c0a5…` != corrupted-all-zeros frozen constant · (2) au_3b_defensible_now stamp key assertion too narrow · fixed to match sealed surface (wall_time_iso + au_3b_defensible) · 10/12 pass immediately on clean codebase state) → GREEN at drill_receipts/20260919T225712Z (12/12 pass · 0.83s) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `5eed33e9384288952e20202b9850fbf3851db239bd9aea4c476b9ec19c26347d` IDENTICAL across drill_receipts/20260919T225820Z_run1 + 20260919T230129Z_run2 (both 11124 bytes raw · 11103 bytes stripped · 5527 passed/1 skipped/438 warnings · ~180s each) against final baseline_failures.json sha256 `8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1` · additive-only per SO §3.8 · sealed contracts/dap.py + contracts/trust_receipt_v1.py + contracts/outer_gate_receipt_v1.py + services/reliable_time_source/clock.py all NOT edited (all consumed via identity import) · sealed M17-W1..W6 + M14 + M11 + M16 + W-M2-SW7 + W-7bB + c13_scope + memory-compaction-v1 (4 sub-waves) + CCS1-C17-seam-bundle + CCS2-DAP-entitlement modules all NOT edited · Canon anchors: Canon 5 · seam-boundary discipline + Canon 3 §9.3 · append-only writer + Canon 8 §W11 · one-task-one-identity + SO §3.8 + SO §3.10-α · closed-schema discipline (only MeteredEvent fully compliant · TrustReceiptV1 + OuterGateReceiptV1 non-α gaps banked) + SO §6.4 NOTHING-BEYOND + SO §6.7 sequence CCS1 → CCS2 → CCS3 → HALT before frontends (FINAL contract closure wave completed · frontends gate HALT point next) + M17-W1 milestone precedent + CCS1-C17 bundle-sha `a6107d46…` precedent + CCS2 DAP entitlement bundle-sha `051f25df…` precedent + B-frontends-Q1 + Doc-3 DAP-Spec dap_backend_spec_v1 verbatim (DAP-21 metered event 7-field surface + reliable time source requirement + R-C2 au_3b_defensible) + owner FRONTENDS-GATE-IS-HALT-POINT + owner PROCEED + owner ruling 2026-09-19T~17:54Z item (e) verbatim · Stop-conditions NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next HALT at frontends gate for owner dispatch to specialists"
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
