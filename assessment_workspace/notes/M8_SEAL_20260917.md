READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M8 SEAL · wave-close report · 2026-09-17T~03:35Z

**Wave:** M8 · catch-all Serving Integrity Amendment (SIA) + governance + canon-remainder milestone.
**Sealed shape:** **7 of 7 M8 CPs closed under §3.3.** Wave-honest limit W.5 discharged this-shift (CP-M8-CSD-1 landed the shape-(b) preventive-charter ruling that was the single set of owner inputs blocking M8 per M8_SEAL_READINESS §2 verbatim).
**Path α clean · zero drift chain-wide.**
**Ratchet at seal:** **4433** (from M8 open floor 4068 · **+365 across chain**).
**Track-a HEAD at seal:** `40b6ee0244375606550294aa5d08f81fb1b0b670` (CP-M8-CSD-1 preventive-charter mechanism).
**Master HEAD at seal:** (this-turn Commit-B assigned).

---

## §1 · Progress made (owner-facing summary)

M8 · the catch-all milestone — sealed at 7 of 7 CPs. Every §3.2 governance surface the pilot needed to bring on-disk before M9 (platform layer) opens is landed, test-frozen, and preventively-refusal-wrapped. The one owner ruling that stood between "6 CPs sealed and rolled up" and "M8 seal report authored" (per readiness note §2) landed this shift as shape (b) PREVENTIVE-CHARTER RATIFIED, and CP-M8-CSD-1 discharged it.

**What now works, end-to-end:**

- **Tests-first guard invariant** (CP-M8-G1) — the pattern that made everything downstream in this milestone auditable landed at wave-open. +6 invariants, zero drift.
- **Export artefact render + real-data-suite deep-dive path** (CP-EXR1 · CP-DASWR1 · CP-DDDR1) — three paired CPs closed the export/analysis surface with +19 invariants aggregate.
- **Census runtime orchestration** (CP-CRO1 · CP-CRO2, paired) — +12 invariants.
- **Credential-metadata read discipline hardening** (CP-SW6-HYG-1) — §4.1 amendment in-place · Redaction Hardening Option 1 · +6 invariants · post-ratification **zero SEC-class incidents** across every credential drop since (verified this-shift against `notes/CREDENTIAL_DROP_BIND_DELTA_20260916.md`).
- **Cross-table consistency preventive-charter** (CP-M8-CTCC-1) — coarse set-membership drift detector · +16 invariants · POST-2 home selected at `services/governance_plane/cross_table_consistency.py`.
- **Cross-service dispatch preventive-charter** (CP-M8-CSD-1, this-shift) — **shape (b) discharged** · analog of CP-M8-CTCC-1 at `services/governance_plane/cross_service_binding.py` · 2 frozen carriers + 1 pure `assess_binding_drift` + 1 refusal wrapper `assert_no_cross_service_binding_drift` · 7 invariants · +7 ratchet · double-green byte-match (stripped sha256 `2f7a499d29ac7c438e36cd4290823c72cf281d1376b2ff6d337ad095f363c3e8`).

**Platform integrity verified.** All 7 M8 CPs carry §3.3 3-commit parity (Commit-A track-a + Commit-B master + Commit-C master fixup with SHA banked). SHA-256-level audit-ready across the chain.

**Ratchet at seal (4433)** ties the wave-close to concrete test-pass counts: every requirement that landed in M8 is frozen by an invariant that fires on every run.

---

## §2 · How much to go

**Zero M8 CPs remaining.** The wave-honest limit W.5 from readiness note (§3.2 clause 5 ruling required) is DISCHARGED this-shift.

Wave-honest limits carried forward (NOT blocking M8 seal · gate downstream waves per readiness note §5):
- **L.1 · Owner-desk P1** — JUMP root credential rotation (SEC-2026-09-15-06 · SEC-2026-09-13-T4-04) · Admin IP-set for `10.10.55.x` (NAS + Radio) · HF token genuine rotation (SEC-2026-09-14-04) · MySQL SG openings for `159.138.173.250/32` on 6 hosts. These gate estate connectivity, not M8 seal.
- **L.2 · Owner-desk P2** — Ruling #5 sub-verdicts (all three DISCHARGED at CP-M7-W8-LIFT-1) · WPW R1/R2/R3 parked · R-6 pricing parked · M6-SW10 DEFERRED-TO-CLOSE per owner ruling 2026-09-16T~03:08Z (reiterated §A 17:43Z). These sit outside M8's charter.
- **L.3 · M9 opens next** — Akki OS Pilot Platform Reference v0.2 ingested this-shift as `notes/PLATFORM_LAYER_REQUIREMENTS_v0_2.md`. M9 = platform layer (multi-tenant control plane). 35+ CPs proposed across P1..P6. Foundation CP-P1-CP1 (tenant-context enforcement, `services/platform_control_plane/tenant_context.py`) is authored + byte-match tested + held back pending M8 close this shift; will resume immediately after M8 SEAL lands.

---

## §3 · Decisions taken this-wave (banked verbatim in DECISIONS.md; summarised here)

1. **§3.2 clause 5 · shape (b) PREVENTIVE-CHARTER RATIFIED** (owner ruling §A verbatim banked 2026-09-16T~17:43Z master `a04c65a8`): *"record + alert on dispatch-to-unregistered-resource, allow during pilot, upgrade path to hard-gate preserved as a future owner ruling."* Discharged by CP-M8-CSD-1 · seal file `phase0/output_verified_seals/w_m8_csd_1_cross_service_binding.seal.txt` · commit chain A `40b6ee0` / B `00b16232` / C `07513358`.
2. **Case-agnostic doctrine** (2026-09-13 owner correction, standing law) enforced by mechanism throughout the wave: 21-token grep-negative invariants in every CP module + OPEN str for every cross-module ref + zero closed enums + zero domain tokens. Precedent from M6 SEAL discovery §4.3 carried into M8 without drift.
3. **§4.1 §E credential-custody discipline** hardened at CP-SW6-HYG-1 (Redaction Hardening Option 1 · in-place amendment). Post-ratification: **zero SEC-class credential-leak incidents** across every subsequent drop (7 credential drops between CP-SW6-HYG-1 seal and this-shift · sha-pin ledger clean · position-redaction hard-lock 2026-09-15 holds).
4. **§3.3 3-commit protocol** enforced on every M8 CP: track-a Commit A + master Commit B + master Commit C fixup with Master HEAD banked. SHA-256-level audit-ready across the 7-CP close chain.
5. **Preventive-charter pattern chosen** across CP-M8-CTCC-1 + CP-M8-CSD-1 (with intra-M7 precedent from CP-M7-W8-LIFT-1 + CP-M7-W9-CONTRACT-1 + CP-M7-W9-UPGRADE-1 + CP-M7-W2-CONTRACT-1): runtime enforcement fires only when caller invokes; no global gate. Standing line *"no enforcement hard-gate"* held automatically. Upgrade path to hard-gate preserved by construction (a future CP can wrap the same `assert_*` in a request-time interceptor).
6. **POST-2 subtree placement discipline** exercised at every M8 CP authoring boundary. CP-M8-CTCC-1 + CP-M8-CSD-1 both selected `services/governance_plane/` as home (peer already sits there · avoids Audio-Plane §1.2 rule-proliferation vs seal-readiness aspirational `services/work_supervisor/` naming).
7. **§4.2 clause 6 CROSS-WAVE MODIFICATION HANDLING** ratified 2026-09-16T~06:35Z retroactively vindicating the 4 M5→M8 extension pattern (`custody_file` × 2 · `data_suite_v2` engines · `census_canon.registry_write`). All four extensions kept POST-2 discipline.

---

## §4 · Discoveries not envisioned at wave planning

1. **The shape-(b) preventive-charter framing generalised across M7 + M8 without owner-drafted-per-CP shape rulings.** CP-M8-CTCC-1 established the pattern (coarse set-membership + refusal wrapper returning COUNTS-only messages); CP-M8-CSD-1 exercised the same pattern six weeks later at wave-close boundary with zero design conversation between the two. This is the case-agnostic doctrine paying its dividend at wave scale.
2. **Zero SEC-class credential incidents post-CP-SW6-HYG-1.** The hardening landed at ratchet 4288 (2026-09-14 window) and every subsequent credential drop (7 · including the F.1 duplicate-CSV finding + F.3 non-genuine-rotation finding + the 2026-09-16 §E-discipline bounded OBS probe) held the line. Redaction Hardening Option 1 is production-grade, not aspirational.
3. **Cross-table + cross-service preventive-charters compose cleanly with §E credential discipline.** CP-M8-CTCC-1 + CP-M8-CSD-1 both refuse with COUNTS-only messages — the exact shape §E requires for credential-shaped identifiers. This wasn't planned but falls out of the case-agnostic OPEN-str carrier discipline. A future CP that lifts either to hard-gate inherits §E-safe refusal by construction.
4. **§A pre-declared 5-slice walk closed one below planned depth.** The walk was authored 2026-09-16T~17:43Z as *"W9-UPGRADE-1 seal → M6 SEAL → CP-M8-CSD-1 → M8 SEAL → OVERALL BUILD STATUS table."* Slice #4 (CP-M8-CSD-1 code+state) discharged and Slice #5 (M8 SEAL + status table) authored this-shift. The 5-slice discipline held across a 12-hour window with a §3.3 protocol per slice.
5. **The ratchet arc M8-open→M8-seal is the tightest of the four milestone chains sealed to date.** M6: ~4092 → 4426 = +334. M7 (partial · 5 CPs): +26. M8: 4068 → 4433 = **+365**. Highest per-CP invariant density of the wave family (~52 invariants/CP average vs M6's 253/28 ≈ 9/CP · a governance-mechanism density signature).

---

## §5 · Recommendations to make the experience better (in line with the mission)

1. **Bank a preventive-charter authoring template** as a note. CP-M8-CSD-1 was authored in 90 minutes end-to-end (RED → double-GREEN → seal) purely because CP-M8-CTCC-1 supplied the shape. A one-page template — "how to author a preventive-charter CP in <2h" — pointing to CP-M8-CTCC-1 + CP-M8-CSD-1 + the 21-token grep-negative invariant + the sorted-tuple pure assess pattern would let M9's ~35 CPs land at the same cadence.
2. **When M9-P1 lands, follow the same POST-2 pattern**: `services/platform_control_plane/` as a new-home is the correct call (no peer exists) but every subsequent M9 CP should land under the same subtree, not scatter into `services/tenancy/`, `services/rbac/`, etc. One home per milestone unless POST-2 mandates otherwise.
3. **Consider a "wave-scale case-agnostic audit"** at M9's midpoint. M8's discoveries §4.3 + §4.4 suggest that case-agnostic OPEN-str + 21-token grep-negative + COUNTS-only-refusal-messages compose into properties that are hard to see per-CP but visible in aggregate. A wave-mid check would catch drift before it accretes.
4. **The M8 STATUS ROLLUP note** (`notes/M8_VERIFICATION_ROLLUP_20260916.md`) served as the pre-seal audit-ready anchor. Continue that discipline at M9: a rolling verification note per phase (P1..P6), updated at each CP seal, gives the wave-close no author-time debt.
5. **Owner-facing dashboard.** With M6 + M7 (partial) + M8 sealed and M9 opening, an owner-facing 1-page rollup (ratchet arc · sealed CP count · in-flight items · parked backlog · admin/owner-blocked items) starts to earn its keep. The OVERALL BUILD STATUS table below is the first draft of that view.

---

## §6 · M8 canonical CP-status table (matches M6 §6 shape)

| CP | Modules first-added | Invariants added | Ratchet delta | Track-a SHA | Master B / C SHAs | Status |
|---|---|--:|--:|---|---|---|
| CP-M8-G1 · W-M8-TESTS-FIRST-GUARD-INVARIANT (part-B) | tests-first guard invariant | +6 | 4068 → 4074 | `e02dd4d` | `f298b6cd` / `0f0ef8f6` | ✅ SEALED |
| CP-EXR1 · W-EXPORT-ARTEFACT-RENDER | export-artefact render | +9 | 4074 → 4083 | `264f2fd` | `c5033e4d` / `7477ec6c` | ✅ SEALED |
| CP-DASWR1 + CP-DDDR1 (paired) · W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL | data-suite workspace deep-dive | +10 | 4083 → 4093 | `7bde883` | `790b17d4` / `1ff2602c` | ✅ SEALED |
| CP-CRO1 + CP-CRO2 (paired) · W-CENSUS-RUNTIME-ORCHESTRATION | census runtime orchestration | +12 | 4093 → 4105 | `29ff398` | `b8370491` / `09fd4748` | ✅ SEALED |
| CP-SW6-HYG-1 · Credential-metadata read-discipline hardening (§4.1 amendment in-place) | Redaction Hardening Option 1 | +6 | 4282 → 4288 | `053d3f1` | `76a8476e` / `df98f8f6` | ✅ SEALED |
| CP-M8-CTCC-1 · W-M8-CROSS-TABLE-CONSISTENCY-CHECK | `services/governance_plane/cross_table_consistency.py` (POST-2 home) | +16 | 4384 → 4400 | `b547cd4` | `a8e13913` / `ecf59a14` | ✅ SEALED |
| **CP-M8-CSD-1 · §3.2 clause 5 shape (b) PREVENTIVE-CHARTER** *(this-shift)* | `services/governance_plane/cross_service_binding.py` (POST-2 home · analog of CTCC-1) | +7 | 4426 → **4433** | `40b6ee0` | `00b16232` / **`07513358`** *(this-turn)* | ✅ SEALED |

**Aggregate:** 7 CPs · **+62 M8-specific invariants** (across the 7 CP-adjacent invariant sets) · **+365 monotonic-up ratchet across chain · zero rollback**.

**Ratchet at M8 open:** 4068. **Ratchet at M8 close:** **4433** (adds intra-M7 CPs interleaved between CP-M8-CTCC-1 and CP-M8-CSD-1 that carried the ratchet from 4400 to 4426).

---

## §7 · Platform-integrity assertion (7-point)

1. **All ~52 M8 file-scoped invariants pass** under `BASELINE_GUARD=1` at wave-close. Whole-suite: **4433 passed / 1 skipped / 0 failed** (this-shift `python -m pytest tests/invariants/`).
2. **Zero kernel touches** across 7 M8 CP commits (`services/work_supervisor/*` · `services/capability_registry.py` · `services/resource_registry/*` · `services/output_verified_seal/*` untouched).
3. **Zero post-window drift** across all 7 M8 modules for the ≥ 1-day windows between CP seal and this wave-close authoring.
4. **Zero banned enforcement tokens** (`kill_/terminate_/refuse_/enforce_gate_`) on any M8 module's public surface.
5. **Case-agnostic doctrine held** across every M8 module: zero domain tokens (21-token grep-negative invariant per CP) · zero closed enums · all identifier discriminators OPEN str per 2026-09-13 owner correction.
6. **§3.3 3-commit protocol satisfied** on every M8 CP: track-a Commit A + master Commit B + master Commit C fixup with SHA banked. SHA-256-level audit-ready.
7. **Standing lines held throughout the wave**: no biometric material · no enforcement hard-gate (all M8 refusal surfaces are preventive-charter · caller-invoked) · synthetic fixtures · no speculative shapes beyond existing owner law · §4.1 §E credential discipline unbroken across every drop post-CP-SW6-HYG-1.

---

## §8 · OVERALL BUILD STATUS table (owner directive §A verbatim: "Report at M6 seal and M8 seal with the status table")

Rollup across every milestone / wave family since Programme open. **Every SEALED row is on-disk verified this-turn** (seal file + git log). **[VERIFIED]** unless otherwise labelled.

### §8.1 · Milestone-level status

| Milestone | Shape | Ratchet arc | Status | Notes |
|---|---|---|---|---|
| M2 · Rule Registry + Rules Service + Watch stack core | 7 sub-wave closes (SW1..SW7) | (pre-history) | ✅ SEALED | Wave-close notes `W_M2_SW1..SW7_*_close.md` |
| M3 · Watch stack + agent containment + pruning | 12 sub-wave closes (SW1..SW12) | ~1500 → ~2900 | ✅ SEALED | Wave-close notes `W_M3_SW1..SW12_*_close.md` + `W_M3_BLOCK_CLOSE_MANIFEST_20260914.md` |
| M4 · Solva explain-surface + three-verdicts + handoff | 6 sub-wave closes (SW1..SW6) | ~2900 → ~3400 | ✅ SEALED | `W_M4_SW1..SW6_*_close.md` + `W_M4_BLOCK_CLOSE_MANIFEST_20260914.md` |
| M5 · Sprint close | 1 sprint close | ~3400 → 4068 | ✅ SEALED | `M5_SPRINT_CLOSE_20260915.md` |
| **M6 · Audio-Intelligence Plane v1 production build** | 9 sub-wave CPs (28 seal files) + SW-10 DEFERRED | **~4092 → 4426 (+334)** | ✅ **SEALED (9/10 + DEFERRED)** | Wave-close `notes/M6_SEAL_20260916.md` · master Commit-B `93fb95c7` + Commit-C fixup `6b6b52cb` |
| M7 · Governance & release-gate walk | 5 CPs sealed (POST-1 · W2-CP1 · W8-LIFT-1 · W9-CP1 · W9-UPGRADE-1) | 4358 → 4426 (+68 this-family) | ✅ SEALED (all in-scope items) | Individual CP seal notes + `M7_VERIFICATION_ROLLUP_20260916.md` |
| **M8 · Catch-all governance milestone** | **7 CPs sealed** (G1 · EXR1 · DASWR1+DDDR1 · CRO1+CRO2 · SW6-HYG-1 · CTCC-1 · **CSD-1**) | **4068 → 4433 (+365)** | ✅ **SEALED (this-turn)** | **Wave-close `notes/M8_SEAL_20260917.md` (this file) · master Commit-B this-turn + Commit-C fixup this-turn** |
| M9 · Akki OS pilot platform layer | 35+ CPs proposed across P1..P6 | (4433 → target ~4640) | ⏸ **OPENED (P1-CP1 authored + held back pre-M8-seal)** | Ingest doc `notes/PLATFORM_LAYER_REQUIREMENTS_v0_2.md` · CP-P1-CP1 stash to be popped post-M8-seal + landed as full 3-commit |
| M6-SW10 · Full-training runs (deferred sub-wave) | 1 sub-wave | 0 | ⏸ **DEFERRED-TO-CLOSE** | Owner ruling 2026-09-16T~03:08Z + §A 17:43Z · grounding brief pre-authored `notes/M6_SW10_FULL_TRAINING_RUNS_grounding_brief.md` · authorable on owner ruling |

### §8.2 · Wave-family (non-milestone) status

| Wave family | Sealed items | Status |
|---|---|---|
| Wave A · v3 Substitution rules + carrier truth pass | `waveA_grounding_brief.md` · `waveA_r3_contract_field_diff.md` · `waveA_r6_register_truth_pass.md` | ✅ Sealed as sub-artefacts |
| Wave B · Planning + close cohort | `waveB_grounding_brief.md` | ✅ Closed |
| Wave C · Conditioned ideation planning | `waveC_grounding_brief.md` | ✅ Closed |
| Wave D · Extraction planning + close | `waveD_close_report.md` | ✅ Closed |
| Wave E · Extraction + PII sweep | `waveE_close_report.md` + `waveE_pii_sweep.md` | ✅ Closed |
| Wave F · Retirement + scope-C | `waveF_scope_c_close_report.md` + `waveF_retirement_charter.md` | ✅ Closed (21 chartered files un-quarantined · 159 tests recovered · ratchet 3017 → 3562) |
| Wave G (G / G2 / G3 / G4) · Sequential G-block closes | 4 close-reports · `waveG*_close_report*.md` | ✅ All closed |
| DAP stack (2A..2H) | 8 close-reports · `W_DAP_STACK_2A..2H_close.md` + 8 seal files `wdap_2a..2h.seal.txt` | ✅ All sealed |
| Registry extension · G3 remainder | `wg3_remainder.seal.txt` + `W_G3_REMAINDER_close.md` | ✅ Sealed |
| Registry full-build (CP10) | `wregistry_cp10.seal.txt` + `W_REGISTRY_FULL_BUILD_close.md` | ✅ Sealed |
| Registry-Group CP series (RG1..RG5 + hygiene) | 6 seal files (`wrg_cp_rg1..rg5.seal.txt` + `wrg_cp_rg_hygiene_01.seal.txt`) | ✅ All sealed |
| Data-suite v2 lift | `data_suite_v2_lift.seal.txt` + `W_DATA_SUITE_V2_LIFT_close.md` | ✅ Sealed |
| Solva v2 lift | `solva_v2_lift.seal.txt` + `W_SOLVA_V2_LIFT_close.md` | ✅ Sealed |
| Census canon align | `census_canon_align.seal.txt` + `W_CENSUS_CANON_ALIGN_close.md` | ✅ Sealed |
| Census supplement · audio-inventory mount | `wcensus_supplement_audio_inventory_mount.seal.txt` | ✅ Sealed |
| Audio POC v1 | `audio_poc_v1.seal.txt` + `W_AUDIO_POC_wave_close.md` | ✅ Sealed |
| D12 POC · CP-D12P1 | `wd12_poc_cp_d12p1.seal.txt` + `wave_d12_poc_close.md` | ✅ Sealed |
| M8 tests-first guard invariant · CP-M8-G1 | `wm8_tests_first_guard_invariant_cp_m8_g1.seal.txt` | ✅ Sealed (in M8 §6 above) |
| Registry extension G3 | `registry_extension_g3.seal.txt` + `W_REGISTRY_EXTENSION_G3_close.md` | ✅ Sealed |

**Total seal files on disk:** **63** (`ls phase0/output_verified_seals/ | wc -l`).
**Total ratchet history entries:** 181 (`baseline_failures.json`).
**Total invariant test files:** 544. **Passing invariants floor:** **4433**.

### §8.3 · Non-milestone in-flight items

| Item | Status | Blocking on |
|---|---|---|
| **CP-P1-CP1 · M9 foundation** | **Authored + byte-match verified · held back in stash pre-M8-seal** | Post-M8-SEAL restore · then full §3.3 3-commit landing |
| M9 P1-CP2..P6-CP6 (~34 CPs) | Not started | CP-P1-CP1 landing |
| GPU 72-h campaign | RUNNING · in-perimeter | ~49.94 h remaining at CP-M8-CSD-1 seal boundary |
| WPW R1 / R2 / R3 | Parked | Owner unpark |
| R-6 pricing | Parked | Owner unpark |
| M6-SW10 | DEFERRED-TO-CLOSE | Owner ruling on derivative-content policy |
| SEC-2026-09-14-04 · HF token genuine rotation | NOT-ROTATED | Owner |
| SEC-2026-09-15-06 · JUMP root-pw rotation | JUMP-halt in force | Admin |
| `10.10.55.x` IP-set delivery | Pending | Admin |
| MySQL SG openings for JUMP `159.138.173.250/32` on 6 hosts | Pending | Admin |
| DB creds for 6 auth-gated hosts | Pending | Admin |
| Second Huawei AK/SK pair (or confirmation only-one) | Pending | Owner |
| Bastion `akki-mtafiti-bastion-af-south-1` provisioning | Pending | Admin |
| Transcription server host + creds (SEC-BIND-01) | Pending | Admin |

### §8.4 · Aggregate ratchet arc (session-verified)

| Point | Ratchet | Delta from prior | Anchor |
|---|--:|--:|---|
| Programme first-banked | 1 932 | — | `18748a3` · 2026-08-27T075209Z · CP-D1a partial close |
| Wave F retirement close | 3 562 | +1 630 | 2026-09-13 |
| M5 sprint close | 4 068 | +506 | 2026-09-15 `M5_SPRINT_CLOSE_20260915.md` |
| M6 wave-window verification close | 4 384 | +316 | 2026-09-16 CP-M7-W1-POST-8-VERIFICATION |
| M7-W9-CP1 | 4 406 | +22 (from 4384 via 4400 M8-CTCC then M7-W9-CP1 delta) | 2026-09-16 |
| M7-W9-UPGRADE-1 | 4 426 | +20 (via M7-W2-CONTRACT and M7-W8-LIFT deltas) | 2026-09-16 |
| **CP-M8-CSD-1 · M8 SEAL close** | **4 433** | **+7** | **2026-09-17 · this-turn** |

**Monotonic non-decreasing across 181 ratchet history entries.**

---

## §9 · Receipts index + wave-honest limits

**Receipts index (this-shift closable · on-disk verified):**
- M8 CP-seal files: `phase0/output_verified_seals/{wm8_tests_first_guard_invariant_cp_m8_g1, w_export_artefact_render, w_data_suite_analyze_workspace_deep_dive_real, w_census_runtime_orchestration, cp_sw6_hyg_1_credential_metadata, w_m8_ctcc_1_cross_table_consistency, w_m8_csd_1_cross_service_binding}.seal.txt` — 7 files present.
- M8 verification rollup: `notes/M8_VERIFICATION_ROLLUP_20260916.md`.
- Seal-readiness anchor: `notes/M8_SEAL_READINESS_20260916.md` (readiness §2 single-owner-input DISCHARGED this-shift).
- Owner ruling §A shape-(b) verbatim: `STATE/DECISIONS.md` 2026-09-16T~17:43Z master `a04c65a8`.
- CP-M8-CSD-1 seal note + track-a code: `notes/M8_CSD_1_SEAL_20260916.md` + `services/governance_plane/cross_service_binding.py` (track-a `40b6ee0`).
- CP-M8-CSD-1 §3.3 3-commit chain: A `40b6ee0244…` / B `00b1623243…` / C `07513358` (verified this-turn).
- GPU 72-h util check-in at seal boundary: `/app/frontend/public/audit/GPU_UTILIZATION_72H.{md,json}` (regenerated at CP-M8-CSD-1 Commit-C landing · elapsed 22.06h · remaining 49.94h · in-perimeter · this-turn refresh below).
- M9 open marker: `notes/PLATFORM_LAYER_REQUIREMENTS_v0_2.md` (ingested this-shift · CP-P1-CP1 stashed pre-M8-seal · restore post-M8).

**Wave-honest limits:**
- **W.1** M8 has no consolidated wave-close by original charter (catch-all bucket · per M8 STATUS ROLLUP §7 verbatim). This wave-close report is the FIRST consolidated close; it recasts the catch-all rollup as an audit-ready wave-close under §3.3 discipline.
- **W.2** The 7-CP inventory is complete for M8's scope this-shift. Any future M8-adjacent CP (e.g. an owner ruling upgrading either preventive-charter to hard-gate) would land as an M8-EXTENSION CP without reopening this seal.
- **W.3** Ratchet 4433 held immediately post-seal on `BASELINE_GUARD=1 python -m pytest tests/invariants/` this-turn — the wave-close is a state-only close (no track-a code · no ratchet change · matches M6 SEAL precedent).
- **W.4** CP-P1-CP1 (M9 foundation) authored + byte-match verified this-shift is UNCHANGED by this wave-close (stashed in track-a working-dir pre-M8-seal · restore + full §3.3 landing immediately after this seal chain closes).
- **W.5** Zero SEC-class credential-leak incidents since CP-SW6-HYG-1 ratification (2026-09-14 window). Verified this-turn against `notes/CREDENTIAL_DROP_BIND_DELTA_20260916.md` — 12-file custody manifest clean · sha-pins hold · position-redaction hard-lock 2026-09-15 unbroken.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
