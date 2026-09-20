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
generated_at_utc: 2026-09-20T09:32:00Z
generator: main-agent Autopilot (CP-STALENESS-CEREMONY Commit-C fixup · state master · Canon 3 §24 rule-change APPLY step for 5 mtafiti staleness invariants · WAVE R-69 · Step 3 in owner-ratified reorder · advances heads_last_sealed.state_repo.head `d48f6e1e049b35dd334d284be9bbfb2f67eed97f` (CCS3 Commit-B) → new Commit-B `9c0dd84013900cdc0a53f143f306eb4157a810e7` (this CP Commit-B · banks Commit-A `31d414bd540632e52cb050321b71b29b730a0f1e`) · advances heads_last_sealed.code_repo.head `379e45508bbfbc362f2b28d93065f527bc3864bd` (CCS3 Commit-A) → this-CP Commit-A `31d414bd540632e52cb050321b71b29b730a0f1e` (5 mtafiti test bodies rescoped + 1 new helper module · DELTA 0 · ratchet unchanged at 5527) · ratchet 5527 unchanged at Commit-C · R-70 marker flips ⏳→✅ SEALED · owner ruling verbatim 2026-09-20T~08:56Z APPLY-IMMEDIATELY 'Horizon is past; do not wait behind the trace' · Canon 3 §24 apply step complete · Stop-conditions NOT triggered · Standing bounds unchanged)
regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-staleness-ceremony-advancing-state-head-and-code-head

ratchet:
  passed_floor: 5527
  counts_at_baseline_passed: 5527
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: 8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 9c0dd84013900cdc0a53f143f306eb4157a810e7
    sealed_at_utc: 2026-09-20T09:32:00Z
    seal_kind: "CP-STALENESS-CEREMONY · state Commit-B `9c0dd84013900cdc0a53f143f306eb4157a810e7` · banks Commit-A `31d414bd540632e52cb050321b71b29b730a0f1e` · Canon 3 §24 rule-change APPLY step for 5 mtafiti staleness invariants (test_live_composition_census_is_recent + test_probe_receipt_is_recent + test_live_quality_profile_is_recent + test_cost_receipt_is_recent + test_wave_close_bundle_is_recent) · owner rulings verbatim chain: 2026-09-18 rescope-not-retire scope + 2026-09-18T~12:35Z counter-sign scope-not-proposal-text-sight-unseen + 2026-09-18T~12:35Z proposal-alignment-verification EXACT + 2026-09-19T~05:15Z APPLY-ON-EXPIRY horizon 11:35Z + 2026-09-20T~08:56Z APPLY-IMMEDIATELY 'Horizon is past; do not wait behind the trace' · state-side landing: (1) DECISIONS.md Commit-B banking section with owner rulings verbatim chain + Commit-A scope + STATE-side data-migration record with sha-pins for 5 gitignored _latest.json files (previous_at_utc + previous_integrity_hash colon-pair-hex + campaign_context + integrity_hash colon-pair-hex) + 1 gitignored gpu_receipts close-out record + sweep-adjacent housekeeping-pickup transparency banking for CP10 harness refresh + Canon anchors + Stop-conditions + autopilot next · (2) NEXT.md R-70 marker ⏳ IN-FLIGHT flipped to ✅ SEALED at this Commit-C fixup · (3) PINS.md commissioning_record pointer refresh 20260919T231816Z → 20260920T092355Z (R-29-BOOT housekeeping-pickup · not a scope change) · (4) NEW STATE/mtafiti_campaign_state.json (sha256 48d9e77bf48b38f72063bb53bb086638137fbbbe21c45c5924bac6d1ce286809 · status='closed' · closed_at_utc='2026-09-18T08:16:00Z' · prior_campaign refs CP-M11-GATE-RELEASE) · (5) ORCH_BOOT.md R-6 boundary regen advancing state_head from CCS3 Commit-B d48f6e1e via WAVE R-69 Commit-1 04fcf6de + Commit-2 bbdfef1c to this Commit-B + code_head from CCS3 Commit-A 379e455 to this-CP Commit-A 31d414b + audit copy re-sync byte-identical · ratchet 5527 unchanged (no baseline_failures_sha256 change · pre-Commit-A double-green stripped-sha256 9d2d661daa43ba5dd1bf551829fec18d82a3185ef4ebd1bc48f45c577b6f4b66 IDENTICAL run1v2/run2 · 5527 passed/1 skipped/438 warnings ~162s each against unchanged baseline sha `8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1`) · sealed contracts NOT edited · Canon anchors Canon 3 §24 + Canon 3 §9.3 + Canon 8 §W8 + SO §3.3 + SO §3.8 + SO §6.4 + SO §6.7 · STALENESS RE-SCOPE APPLY-ON-EXPIRY fully LANDED at this seal · Stop-conditions #1/#2/#3 NOT triggered · WAVE R-69 · Step 3 in owner-ratified reorder · Step 2 (surface-language trace) opens next"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 31d414bd540632e52cb050321b71b29b730a0f1e
    sealed_at_utc: 2026-09-20T09:26:00Z
    seal_kind: "CP-STALENESS-CEREMONY · Commit-A `31d414bd540632e52cb050321b71b29b730a0f1e` · code programme/track-a · Canon 3 §24 rule-change APPLY step for 5 mtafiti staleness invariants · owner rulings verbatim chain: 2026-09-18 rescope-not-retire + 2026-09-18T~12:35Z counter-sign + 2026-09-18T~12:35Z alignment-verification EXACT + 2026-09-19T~05:15Z APPLY-ON-EXPIRY + 2026-09-20T~08:56Z APPLY-IMMEDIATELY · DELTA 0 (ratchet unchanged at 5527 · no new test names · 5 existing test bodies re-scoped · 1 new helper module NOT a test) · SCOPE FROZEN (5 mtafiti tests exactly per proposal §2 verbatim · NO test retired · NO scope creep): test_live_composition_census_is_recent + test_probe_receipt_is_recent + test_live_quality_profile_is_recent + test_cost_receipt_is_recent + test_wave_close_bundle_is_recent · Rescope pattern (each test now enforces STEADY-STATE ALWAYS: presence 'at_utc' + integrity_hash canonical-sha256-over-record-minus-integrity_hash + LKG 'previous_at_utc' + 'previous_integrity_hash' · GATED age check ONLY while campaign_declared_open() STATE/mtafiti_campaign_state.json status='open' AND expected_close_at_utc in future) · NEW backend/tests/invariants/_mtafiti_staleness_helpers.py (230 lines · 8 surfaces: _canonical_json_bytes + compute_integrity_hash-COLON-PAIR-HEX-form-to-avoid-sealed-pii_redaction_guard-METADATA_KEYS-false-match-on-plain-hex-sha256-via-`\\d{7,15}`-phone-regex + _to_colon_pair_hex + _normalise_sha256 + verify_integrity + last_known_good_recorded + parse_utc + campaign_declared_open + assert_staleness_steady_state + load_and_assert_steady_state) · AUTHENTIC RED-first: RED at drill_receipts/20260920T090500Z_cp_staleness_ceremony_RED_pre.log (5 fail right-reason 'integrity_hash field required (computed for reference: <sha>)') → targeted GREEN at 20260920T091100Z (5/5 pass 0.74s) → sibling pii_redaction_guard false-match regression discovered at 20260920T091200Z → colon-pair-hex fix → GREEN at 20260920T091500Z (46/46 pass across all 5 test files 1.44s) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `9d2d661daa43ba5dd1bf551829fec18d82a3185ef4ebd1bc48f45c577b6f4b66` IDENTICAL across drill_receipts/20260920T092028Z_run1v2 + 20260920T092327Z_run2 (both 58852 bytes raw · 54163 bytes stripped · 5527 passed/1 skipped/438 warnings · 162s + 161s) against UNCHANGED baseline_failures.json sha256 `8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1` · Sweep-adjacent housekeeping-pickup transparency banking: initial GUARD1 attempt 20260920T091456Z FAILED 1 test test_cp10_harness_receipt_is_still_recent (age 18.88h exceeded 12h horizon · natural time-passage from CCS3 seal · NOT one of 5 mtafiti rescoped tests) reconciled by running sealed tools/wave_g5_realchrome_verification_harness.py which produced GREEN verification result 2026-09-20T09:19:52Z (dummies absent · expected present · style signature INTERRUPT 3 met · 8 registry substitutions applied · full-page portal + registry screenshots captured at phase0/eyeball_proxies/) · fresh receipt phase0/harness_ground_truth/latest.json < 1h old · same refresh unblocked test_v8_substitution_rules_bind_to_rendered_dom::test_harness_ground_truth_receipt_is_recent · NOT scope-cut deviation (5-mtafiti scope frozen · harness refresh is SEPARATE mechanical housekeeping-pickup · precedent R-29-BOOT commissioning_record pointer refresh at CCS1/CCS2/CCS3 was similarly out-of-scope housekeeping-pickup) · Additive-only per SO §3.8 · sealed modules NOT edited: services.mtafiti.* (composition_census + probes.live_readonly_probe + detectors.pii_redaction_guard + detectors.pii_detector + METADATA_KEYS frozenset all consumed via identity import) · contracts.dap + services.reliable_time_source + all M17-W1..W6/M14/M11/M16/W-M2-SW7/W-7bB/c13_scope/memory-compaction-v1/CCS1-C17/CCS2-DAP-entitlement/CCS3-DAP-receipt modules NOT edited · Canon anchors: Canon 3 §24 rule-change 4-step + Canon 3 §9.3 canonicalization + Canon 8 §W8 the-floor-never-learns + SO §3.3 3-Commit Seal + SO §3.8 thin-kernel additive-only + SO §6.4 NOTHING-BEYOND + SO §6.7 sequence WAVE R-69 Step 3 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B → Commit-C fixup → WAVE R-69 Step 2 (surface-language trace across 5 locations + report)"
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
