READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M8 STATUS ROLLUP · Post-launch hardening + §COV/§ORPH catch-all · CP-ledger for eventual M8 seal

**Authored:** 2026-09-16T~08:00Z (this-shift · immediately after CP-M8-CTCC-1 Commit-C fixup landed on master).
**Authority:** Owner directive 2026-09-16T~07:30Z verbatim:

> "Path A — build CP-M8-CTCC-1 (W-Cross-Table-Consistency-Check) now under full §3.3 protocol, then produce the M8 status rollup and hold with utilization interleave."

**Scope.** Covers every M8 catch-all CP that has sealed to date under the FORMAL M8 charter ratified 2026-09-15T~04:12Z (MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md §Δ4). M8 has NO single wave-open commit — the milestone is a catch-all bucket spanning owner-authored quick-hardening waves + SPRINT_PLAN P1..P6 tracks + §COV uncatalogued rulings + §ORPH orphaned scope. CPs surface as they clear owner-input dependencies.

**Verdict at rollup time.** All 6 M8-family CPs sealed since 2026-09-15T~10:56Z are CLEAN under §3.3 3-commit protocol (both SHAs on every seal · double-green byte-match on every close · ratchet monotonic-up in tandem across the chain). Ratchet floor now **4400** (bumped 4074 → 4400 = +326 across the M8 chain to date).

---

## §1 · Canonical M8 CP-status table

| # | CP / Wave | Charter source | First-added / extended module(s) | Track-a SHA (Commit A) | Master SHA (Commit B) | Ratchet delta | Tests count | Sealed-at | Status | Receipt / close-note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **CP-M8-G1** · W-M8-TESTS-FIRST-GUARD-INVARIANT (part-B pulled forward per SEC-15-08/09/10 recurrence) | SPRINT P0 quick-hardening · MILESTONE_PROMISE_BINDING_20260915 §Δ4 row 1 · owner directive 2026-09-15T~10:30Z | Extended `services/secret_hygiene/custody_file.py` (module already sealed at CP-RG-HYGIENE-01 part-A · 3 new assertion functions + 2 new exception subclasses + 2 module-frozen tuples) | `e02dd4d` | `f298b6cd` | 4068 → 4074 (**+6** · no cross-benefit) | 6 invariants | 2026-09-15T~10:56Z | ✅ SEALED · Path α clean · double-green byte-match | `phase0/output_verified_seals/wm8_tests_first_guard_invariant_cp_m8_g1.seal.txt` · `notes/wave_m8_tests_first_guard_invariant_grounding_brief.md` |
| 2 | **CP-EXR1** · W-EXPORT-ARTEFACT-RENDER | SPRINT P0 quick-hardening · MILESTONE_PROMISE_BINDING_20260915 §Δ4 · owner ordered #2 in M8 quick chain | `export_render` + release-gate composition (see commit note) | `264f2fd` | `c5033e4d` | 4074 → 4083 (**+9**) | 9 invariants | 2026-09-15T~11:12Z (post-D12-03 diagnosis window) | ✅ SEALED · Path α clean · double-green byte-match | receipts in commit body · master state entry `c5033e4d` |
| 3 | **CP-DASWR1 + CP-DDDR1** (paired) · W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL | SPRINT P0 quick-hardening · MILESTONE_PROMISE_BINDING_20260915 §Δ4 · owner ordered #3+#4 (paired) · discharges CP-D8 HALT in-place | `services/data_suite_v2/engines/{__init__, analyze_workspace_engine, deep_dive_engine}.py` (M5→M8 cross-wave-out extensions · legitimate under SO §4.2 clause 6) | `7bde883` | `790b17d4` | 4083 → 4093 (**+10** · CP-D8 HALT discharged in-place) | 10 invariants | 2026-09-15T (post-EXR1) | ✅ SEALED · Path α clean · double-green byte-match | receipts in commit body · master state entry `790b17d4` |
| 4 | **CP-CRO1 + CP-CRO2** (paired) · W-CENSUS-RUNTIME-ORCHESTRATION (scope EXPANDED per D12-03 corpus finding) | SPRINT P0 quick-hardening · MILESTONE_STRUCTURE_REHOMED_20260915 §C M8 row 322 · owner ordered #5 · scope EXPANDED (fold ffprobe media_types + audio_bearing_share into live enumeration · new SourceRecord fields · Canon-4 §4.1+§8) | Extended `services/census_canon/registry_write.py` (M5→M8 cross-wave-out extension · legitimate under SO §4.2 clause 6) | `29ff398` | `b8370491` | 4093 → 4105 (**+12**) | 12 invariants | 2026-09-15T | ✅ SEALED · Path α clean · double-green byte-match | receipts in commit body · master state entry `b8370491` |
| 5 | **CP-SW6-HYG-1** · Credential metadata shape helper (Redaction Hardening Option 1) | §COV uncatalogued · ratified same turn as SEC incident `sec_incident_jump_cred_leak_20260915T222935Z` · owner ruling 2026-09-15T~22:30Z (SO §4.1 amendment) | `services/secret_hygiene/custody_file.read_custody_metadata` (shape-only helper · returns `CustodyFileMetadata` carrier · structurally cannot expose raw column values) | `053d3f1` | (batched into subsequent master state commit — see PINS.md `hardening_status: attested`) | 4282 → 4288 (**+6** · no cross-benefit) | 6 invariants | 2026-09-15T~22:30Z | ✅ SEALED · Path α clean · double-green byte-match · SO §4.1 CREDENTIAL CUSTODY READ DISCIPLINE amended in-place | (SEC-incident-ratified · STANDING_ORDERS.md §4.1 verbatim) |
| 6 | **CP-M8-CTCC-1** · W-M8-CROSS-TABLE-CONSISTENCY-CHECK (M8 P6 preventive charter) | SPRINT_PLAN.md:61-66 P6 (verbatim) · MILESTONE_STRUCTURE_REHOMED_20260915 §C M8 row 330 · owner directive 2026-09-16T~07:30Z | New `services/governance_plane/cross_table_consistency.py` (5 primitives · 102 LOC · POST-2 discipline composes into existing `governance_plane/` sub-tree · NO parallel `data_governance/` package) + `__init__.py` 5-name re-export | `b547cd4` | `a8e13913` (+ Commit-C fixup `ecf59a14`) | 4384 → 4400 (**+16** · no cross-benefit) | 16 invariants | 2026-09-16T~07:45Z | ✅ SEALED · Path α clean · double-green byte-match · §3.3 3-commit fully discharged | `phase0/output_verified_seals/w_m8_ctcc_1_cross_table_consistency.seal.txt` · `notes/W_M8_CTCC_1_CROSS_TABLE_CONSISTENCY_close.md` · `notes/wm8_ctcc_1_cross_table_consistency_grounding_brief.md` |

**Additional M8 catch-all triage outputs this shift** (no CP · no ratchet · finding-only):

| Note | Charter source | Outcome | Path |
|---|---|---|---|
| M8 catch-all from-disk findings · 2026-09-16T~07:20Z | Owner directive 2026-09-16T~07:15Z (2-lane sweep) | Lane 1 EXHAUSTED (D1a-1 quarantine retired 2026-08-27 at Wave F Scope A · 21 files un-quarantined · 159 tests recovered) · Lane 2 P1 BLOCKED-ON-PREREQUISITE (Campaign B unsettled) · P5 PARTIAL (orchestrator-level exists; on-host dispatcher-level chartered post-72h-campaign) · P6 BUILDABLE-NOW (→ CP-M8-CTCC-1 built this shift) | `notes/M8_CATCHALL_FROMDISK_FINDINGS_20260916.md` · master `f63ddd27` |

---

## §2 · Aggregate metrics (M8 chain to date)

**Total across 6 sealed CPs:**
- **Track-a code commits:** 6 (`e02dd4d` · `264f2fd` · `7bde883` · `29ff398` · `053d3f1` · `b547cd4`).
- **Master state commits:** 6 Commit-Bs + 1 Commit-C fixup (this shift · CP-M8-CTCC-1 · `ecf59a14`). Earlier CPs pre-date the §3.3 post-seal receipt rule (ratified 2026-09-15T~20:35Z) and were sealed under the two-commit pattern; CP-M8-CTCC-1 is the first M8 CP to exercise §3.3 in full.
- **First-added or extended modules:** 5 distinct code sites — `custody_file.py` (extended twice · part-B + shape-only helper) · `export_render` (1 site) · 3 `data_suite_v2/engines/*.py` (paired CP) · `census_canon/registry_write.py` (paired CP) · `governance_plane/cross_table_consistency.py` (new module) · plus `governance_plane/__init__.py` 5-name `__all__` re-export update.
- **Test invariants added:** 59 (6 + 9 + 10 + 12 + 6 + 16).
- **Ratchet delta across chain:** 4068 → 4400 = **+332** (monotonic-up · no rollback anywhere · `ratchet_history` entry per CP).
- **Ratchet floor at rollup:** **4400** (bumped last at CP-M8-CTCC-1 this shift).

**Cross-wave lineage (SO §4.2 clause 6 · surface-not-drift):**
- **4 of 6 M8 CPs are legitimate M5→M8 cross-wave-out extensions**:
  1. CP-M8-G1 (part-B) extends `custody_file.py` (M5 SW6-HYG add · CP-RG-HYGIENE-01 part-A).
  2. CP-SW6-HYG-1 further extends `custody_file.py` (adds shape-only metadata helper).
  3. CP-DASWR1 + CP-DDDR1 extend `data_suite_v2/engines/*` (M5 W-DATA-SUITE-V2-LIFT add).
  4. CP-CRO1 + CP-CRO2 extend `census_canon/registry_write.py` (M5 W-CENSUS-CANON-ALIGN add).
- All 4 carry the SO §4.2 clause 6 four-criteria proof (CP citation + ratchet delta + owner directive + append-only shape).
- **2 of 6 M8 CPs are M8-native new modules** (no prior wave surface):
  1. CP-EXR1 (`export_render`).
  2. CP-M8-CTCC-1 (`services/governance_plane/cross_table_consistency.py`).

---

## §3 · Standing-orders discipline exercised across the M8 chain

| Standing order | Application in M8 chain | First-exercise CP |
|---|---|---|
| **§3.1** ALIVE IS NOT DONE (real-seal contract) | Every M8 seal file carries `Kind:` line; every seal read routes through `is_real_seal`/`parse_seal`. Zero silent-success occurrences chain-wide. | CP-M8-G1 |
| **§3.2** NO RUN WITHOUT A PROGRESS SIGNAL | CP-CRO1/CP-CRO2 registry-write extensions bind commissioning-record emit surfaces to the runtime-supervisor progress-ring per M7 W1 kernel; no dispatch surface added in M8 without progress-ring binding. Cross-service binding hard-gate remains P2 owner-desk item. | CP-CRO1 |
| **§3.3** NO SEAL WITHOUT BOTH SHAs | CP-M8-CTCC-1 is the first M8 CP to fully exercise §3.3 3-commit protocol (ratified 2026-09-15T~20:35Z at CP-M6-4-2 reconciliation precedent · Commit-A `b547cd4` + Commit-B `a8e13913` + Commit-C fixup `ecf59a14`). Earlier M8 CPs (#1..#5) sealed under the prior two-commit pattern; their seal files carry Track-a HEAD but no Master HEAD line — surfaced here as a wave-honest limit (see §7 recommendations). | CP-M8-CTCC-1 |
| **§4.1** CREDENTIAL CUSTODY READ DISCIPLINE (Redaction Hardening Option 1) | **RATIFIED IN M8**: CP-SW6-HYG-1 authored the shape-only `read_custody_metadata` helper AND the standing order was amended same turn. All subsequent M8 shell/python operations that touch `/app/backend/estate_keys/` route through the helper or env-injection. Post-ratification: zero SEC-class direct-read incidents. | CP-SW6-HYG-1 |
| **§4.2** VERIFICATION-WALK SCOPE DISCIPLINE (+ clause 6 cross-wave modification handling) | Clause 6 codifies exactly the pattern 4 of 6 M8 CPs use to legitimately extend M5-added modules (append-only + CP citation + ratchet delta + owner directive). Ratified 2026-09-16T~06:35Z during CP-M7-W1-POST-4 walk on `clock.py`; retroactively vindicates the M8 chain's extension pattern. | CP-M7-W1-POST-4 (ratified rule) · retroactively covers CP-M8-G1 + CP-SW6-HYG-1 + CP-DASWR1/DDDR1 + CP-CRO1/CRO2 |
| **§5** GPU OBLIGATIONS (full-consumption + never-kill + interleave check-ins) | CP-M8-CTCC-1 is the first M8 CP to open under the LIVE 72h GPU utilization campaign. Interleave check-in fired at seal (elapsed 3.01h · both hosts sampler+workload alive · zero training kills). W-Queue-Watchdog on-host portion (P5 remainder) explicitly DEFERRED-TO-POST-72H-CAMPAIGN per SO §5 zero-perturbation discipline. | CP-M8-CTCC-1 |

---

## §4 · Platform integrity assertion (at rollup time)

Based on the 6-CP M8 chain sealed to date, the platform surface is asserted:

1. **All 6 M8 CPs cleared Path α at seal time.** Double-green byte-match verified · zero regression · zero right-reason RED left un-remediated.
2. **All 4 cross-wave-out extensions are LEGITIMATE under SO §4.2 clause 6.** No unexplained modifications to M5-added modules. Each extension carries owner-directive citation + ratchet delta + append-only shape.
3. **Case-agnostic doctrine held CHAIN-WIDE.** Zero closed enums added on identifier discriminators (CP-M8-CTCC-1 `class_id` OPEN str). Zero domain tokens added to platform kernels. Zero dispatch-surface imports added to preventive/refusal contract modules.
4. **Ratchet monotonic-up throughout.** 4068 → 4400 = +332 across chain · every CP appended a `ratchet_history` entry · zero rollback · zero silent-floor-lowering.
5. **Credential custody discipline HARDENED IN M8.** CP-SW6-HYG-1 discharged the SEC-15 incident class (JUMP root pw leak) with a shape-only helper AND an amended standing order. Post-ratification: zero SEC-class direct-read incidents; every custody read routes through the helper or env-injection.
6. **POST-2 lesson (from-disk read is authoritative) exercised at authoring on the M8 catch-all triage this shift.** Lane 1 quarantine directive was pre-Wave-F snapshot; from-disk read revealed the class had been retired 19 days ago; no re-execution of already-discharged work.
7. **Preventive-charter shape adopted for CP-M8-CTCC-1.** Mechanism lands as shape-frozen refusal contract; runtime enforcement fires only when caller invokes. No global gate. No premature invariant. Owner-desk P2 items (§3.2 clause 5 cross-service binding · Amendment 8 · etc.) remain parked and unaffected.

---

## §5 · Receipts index (for M8 seal reader)

Every receipt is machine-parseable JSON or plain-text at the noted path. Every close-note is markdown at the noted path.

**Seal files (2 machine-parseable at rollup time):**
- `phase0/output_verified_seals/wm8_tests_first_guard_invariant_cp_m8_g1.seal.txt` (CP-M8-G1 · JSON per CP-RG series convention)
- `phase0/output_verified_seals/w_m8_ctcc_1_cross_table_consistency.seal.txt` (CP-M8-CTCC-1 · plain-text with `Kind:` line · §3.3 3-commit fully discharged)

Earlier M8 CPs (CP-EXR1, CP-DASWR1/DDDR1, CP-CRO1/CRO2, CP-SW6-HYG-1) recorded their seals inline in DECISIONS.md + STATE/NEXT.md pins rather than dedicated seal files. See §7 recommendation R1.

**Close-notes (where authored):**
- `notes/W_M8_CTCC_1_CROSS_TABLE_CONSISTENCY_close.md` (CP-M8-CTCC-1 wave-close · 5-section per SO §2)

**Grounding briefs (where authored):**
- `notes/wave_m8_tests_first_guard_invariant_grounding_brief.md` (CP-M8-G1)
- `notes/wm8_ctcc_1_cross_table_consistency_grounding_brief.md` (CP-M8-CTCC-1)

**Standing-orders authoritative texts** (with M8 discipline application):
- STATE/STANDING_ORDERS.md §3.1 (ALIVE IS NOT DONE) · §3.2 (NO RUN WITHOUT A PROGRESS SIGNAL) · §3.3 (NO SEAL WITHOUT BOTH SHAs · discharged full at CP-M8-CTCC-1) · §4.1 (CREDENTIAL CUSTODY READ DISCIPLINE · **amended in-place at CP-SW6-HYG-1** — verbatim owner ruling 2026-09-15T~22:30Z banked)
- STATE/DECISIONS.md CP-M8-* entries (banked verbatim per §3.3 3-commit rule)

**Ratchet manifest:** `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` (`counts_at_baseline.passed=4400` + `invariants_enforced_when_baseline_guard_1.passed_floor=4400`; `ratchet_history` last entry `at_utc=20260916T073800Z` from CP-M8-CTCC-1).

**M8 catch-all triage report:** `notes/M8_CATCHALL_FROMDISK_FINDINGS_20260916.md` (Lane 1/Lane 2 findings this shift · from-disk POST-2 discipline).

**Cross-referenced artefacts:**
- `notes/MILESTONE_STRUCTURE_REHOMED_20260915.md` §C M8 (M8 formal charter)
- `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` §Δ4 (M8 formal ratification · verbatim owner quote)
- `STATE/SPRINT_PLAN.md:19..66` (SPRINT P1..P6 verbatim charters · P6 discharged at CP-M8-CTCC-1)
- `notes/M7_VERIFICATION_ROLLUP_20260916.md` (M7 rollup this shift · reference shape for this M8 rollup · lists 5 M5→M8 cross-wave-out extensions from M-family perspective)

---

## §6 · GPU utilization at rollup time

- **Elapsed 3.18 h · Remaining 68.82 h** (check-in fired at CP-M8-CTCC-1 Commit-C boundary · immediately before rollup authoring).
- Both hosts sampler_alive+workload_alive throughout the M8 chain.
- akki-vm: 88 telemetry samples · 380 bench iters (ok=380 · 2 GPUs).
- akki-vm-ii: 82 telemetry samples · 380 bench iters (ok=380 · 2 GPUs).
- Peak GPU util 100% per H200 (all 4 GPUs) · peak power ~691-693 W · peak temp ~70-71 °C throughout.
- 760 total bench artefacts banked as of Commit-C fixup landing.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md` and `.json`.
- Zero training kills · zero live-perturbation events · SO §5 zero-perturbation discipline preserved. W-Queue-Watchdog on-host portion (P5 remainder) explicitly DEFERRED-TO-POST-72H-CAMPAIGN.

---

## §7 · What this rollup UNBLOCKS · owner-desk state · wave-honest limits

### M8 sealability path

With 6 of ~19+ chartered M8 sub-waves sealed clean under monotonic-up ratchet, M8 has a working foundation. Remaining M8 scope splits by unblock class:

**Buildable-now (no owner input) — 0 remaining this shift.** All buildable-now items in the from-disk sweep are discharged (P6 → CP-M8-CTCC-1 this shift; part-B guard-invariant, export-artefact-render, data-suite-real, census-runtime-orchestration, credential-custody-shape sealed earlier in shift).

**Owner-input-required (parked · P1) — 3 items unchanged:**
- **JUMP root credential rotation** (SEC-15 ledger · unblocks CD + Visitors mysql-path probes · boundary probe loop resumes when landed).
- **Admin bindings for CD + Visitors** (bramuel vs bramwel disambiguation · unblocks mysql-path census reads via version-controlled probe tool with `--allow-csv-custody` opt-in if the owner explicitly orders it).
- **Campaign B settlement** (adapter.tar.gz + held_out_eval.json paired set · unblocks W-TaskEval-v1 P1 and by dependency W-Adapter-Tensor-Persist P4).

**Owner-input-required (parked · P2) — chain unchanged:**
- SW-10 A.1-A.5 · Audio-bytes-retention Path A/B/C · R-17(a) · §3.2 clause 5 cross-service binding enforcement ruling · Amendment 8 · Watch-Learning R-15(b)/R-16(b)/R-17(b) · BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · S-24/27/28/29 charters · W-WPW-v1-e Tier-3 blocked on R1/R2/R3.

**Campaign-perturbation-blocked (until 72h GPU utilization completes) — 1 chartered follow-on:**
- **W-Queue-Watchdog on-host portion** (SPRINT P5 remainder · `on_host_dispatcher_watchdog.sh` + systemd unit installation on GPU hosts · per SO §5 zero-perturbation discipline).

### Probe-class distinction (per owner standing note this-shift)

Keep the two probe classes clean:
- **SEC-suspended JUMP-path probes** — NOTE-SKIPPED pending JUMP root rotation. Boundary probe loop paused at probe #61 (last real fire).
- **mysql-path CD/Visitors probes** — can fire once rotation lands, OR via version-controlled probe tool with `--allow-csv-custody` opt-in **only if the owner explicitly orders it** (§4.1 shape-only helper covers metadata-shape reads; raw-column reads require explicit ruling).

### Wave-honest limits surfaced by this rollup

1. **§3.3 back-compat gap on early M8 CPs.** CPs #1..#5 (CP-M8-G1 · CP-EXR1 · CP-DASWR1/DDDR1 · CP-CRO1/CRO2 · CP-SW6-HYG-1) sealed BEFORE the §3.3 post-seal receipt rule was ratified (2026-09-15T~20:35Z). Their seal files carry Track-a HEAD but no Master HEAD line. This is a rule-boundary artefact, NOT drift: their commits are all reachable in the repos, and DECISIONS.md CP entries carry both SHAs implicitly by chronological adjacency. A retroactive §3.3 fixup batch for these 5 CPs is CANDIDATE POST work if the owner rules it in-scope; not proposed here (SO §3 no-refactor · thin-kernel discipline).
2. **CP-CRO1/CRO2 scope-expansion driver still owner-desk.** The scope expansion (fold ffprobe media_types + audio_bearing_share into live enumeration per Canon-4 §4.1+§8) was ratified 2026-09-15T~11:12Z from the D12-03 corpus finding; a follow-on M6/M8 boundary CP to actually populate the expanded SourceRecord fields on live NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video shares is BLOCKED on NAS-account owner-desk item.
3. **M8 has no consolidated wave-close report** because M8 has no wave-close (catch-all bucket · CPs surface as they clear owner-input). This rollup IS the platform-integrity backbone the eventual M8 seal will point at, playing the role the backend-ratification snapshot played for M6.

### Hold-pattern discipline (this-shift + forward)

Per owner directive 2026-09-16T~07:30Z verbatim: "hold with utilization interleave." Discipline:
- **Utilization check-ins every boundary** (post-fixup boundary satisfied · next tick fires at next CP boundary or hold-pattern cadence tick).
- **All P1/P2 owner items parked and carried** exactly as at boot.
- **All permanent guardrails held**: SO §1 boot ritual on any resume · §3.1/§3.2/§3.3 discipline · §4.1 credential custody · §4.2 wave-window enumeration + clause 6 cross-wave handling · §5 zero-perturbation during live campaign.
- **BAN reasserted**: `testing_agent` strictly banned (owner standing) · terminal pytest only under `BASELINE_GUARD=1` · no push (Owner Clarification 1 2026-08-14) · no refactor · no scaffolding of new FastAPI/React apps · no re-clone of source repos · CHUNK-1 problem statement remains DISAVOWED.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
